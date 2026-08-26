#!/usr/bin/env python3
"""Measure the admitted S1 Desktop/Core protocol without granting new runtime authority."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import queue
import struct
import subprocess
import threading
import time
from typing import Any

MAX_PAYLOAD_BYTES = 65_536
PROTOCOL_VERSION = 1
PRINCIPAL = "desktop_host"
CORE_RESPONSE_TIMEOUT_SECONDS = 5.0
STDERR_CAPTURE_BYTES = 4_096


class ProbeError(RuntimeError):
    pass


def percentile_ms(samples_ns: list[int], percentile: float) -> float:
    if not samples_ns:
        raise ProbeError("cannot calculate percentile for empty sample set")
    ordered = sorted(samples_ns)
    rank = max(1, math.ceil((percentile / 100.0) * len(ordered)))
    return ordered[rank - 1] / 1_000_000.0


def request(operation: str, launch_id: int, request_id: int) -> dict[str, Any]:
    return {
        "kind": "request",
        "operation": operation,
        "protocol_version": PROTOCOL_VERSION,
        "principal": PRINCIPAL,
        "launch_id": launch_id,
        "request_id": request_id,
        "payload": {},
    }


def cancel(launch_id: int, request_id: int, target_request_id: int) -> dict[str, Any]:
    return {
        "kind": "cancel",
        "protocol_version": PROTOCOL_VERSION,
        "principal": PRINCIPAL,
        "launch_id": launch_id,
        "request_id": request_id,
        "target_request_id": target_request_id,
    }


def encode_frame(envelope: dict[str, Any]) -> bytes:
    payload = json.dumps(envelope, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if len(payload) > MAX_PAYLOAD_BYTES:
        raise ProbeError("probe attempted to emit an oversized valid payload")
    return struct.pack(">I", len(payload)) + payload


def read_exact(stream: Any, size: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < size:
        chunk = stream.read(size - len(chunks))
        if not chunk:
            raise ProbeError(f"unexpected EOF after {len(chunks)} of {size} bytes")
        chunks.extend(chunk)
    return bytes(chunks)


def read_frame(process: subprocess.Popen[bytes]) -> dict[str, Any]:
    if process.stdout is None:
        raise ProbeError("Core stdout is unavailable")
    prefix = read_exact(process.stdout, 4)
    (length,) = struct.unpack(">I", prefix)
    if length > MAX_PAYLOAD_BYTES:
        raise ProbeError(f"Core emitted oversized frame: {length}")
    payload = read_exact(process.stdout, length)
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ProbeError(f"Core emitted malformed JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ProbeError("Core emitted non-object envelope")
    return value


def _capture_stderr_after_stop(process: subprocess.Popen[bytes]) -> str:
    if process.stderr is None:
        return ""
    try:
        data = process.stderr.read(STDERR_CAPTURE_BYTES)
    except OSError:
        return ""
    return data.decode("utf-8", errors="replace")


def read_frame_bounded(
    process: subprocess.Popen[bytes],
    timeout_seconds: float = CORE_RESPONSE_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    if timeout_seconds <= 0:
        raise ProbeError("Core response timeout must be positive")
    result: queue.Queue[tuple[bool, Any]] = queue.Queue(maxsize=1)

    def reader() -> None:
        try:
            result.put((True, read_frame(process)))
        except BaseException as exc:
            result.put((False, exc))

    thread = threading.Thread(target=reader, name="wepld-s1-probe-core-read", daemon=True)
    thread.start()
    try:
        ok, value = result.get(timeout=timeout_seconds)
    except queue.Empty as exc:
        stop_core(process)
        stderr = _capture_stderr_after_stop(process)
        suffix = f"; stderr={stderr!r}" if stderr else ""
        raise ProbeError(
            f"Core response deadline exceeded after {timeout_seconds:.3f}s{suffix}"
        ) from exc
    if not ok:
        if isinstance(value, BaseException):
            raise value
        raise ProbeError("Core response reader failed without an exception")
    if not isinstance(value, dict):
        raise ProbeError("Core response reader returned non-object envelope")
    return value


def write_frame(process: subprocess.Popen[bytes], envelope: dict[str, Any]) -> None:
    if process.stdin is None:
        raise ProbeError("Core stdin is unavailable")
    process.stdin.write(encode_frame(envelope))
    process.stdin.flush()


def start_core(core: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        [str(core)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
    )


def stop_core(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2)


def _require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ProbeError(
            f"{label} field set mismatch: expected={sorted(expected)!r} actual={sorted(actual)!r}"
        )


def _require_exact_u64(value: Any, expected: int, label: str) -> None:
    if type(value) is not int or value < 0 or value > (2**64 - 1) or value != expected:
        raise ProbeError(f"{label} mismatch: expected={expected!r} observed={value!r}")


def validate_response(
    response: dict[str, Any],
    expected_operation: str,
    launch_id: int,
    request_id: int,
    expected_payload: dict[str, Any],
) -> None:
    _require_exact_keys(
        response,
        {
            "kind",
            "operation",
            "protocol_version",
            "principal",
            "launch_id",
            "request_id",
            "payload",
        },
        "response",
    )
    if response["kind"] != "response":
        raise ProbeError(f"expected response envelope, observed={response['kind']!r}")
    if response["operation"] != expected_operation:
        raise ProbeError(
            f"expected operation {expected_operation!r}, observed={response['operation']!r}"
        )
    if type(response["protocol_version"]) is not int or response["protocol_version"] != PROTOCOL_VERSION:
        raise ProbeError(
            f"expected protocol_version={PROTOCOL_VERSION}, observed={response['protocol_version']!r}"
        )
    if response["principal"] != PRINCIPAL:
        raise ProbeError(
            f"expected principal={PRINCIPAL!r}, observed={response['principal']!r}"
        )
    _require_exact_u64(response["launch_id"], launch_id, "launch_id")
    _require_exact_u64(response["request_id"], request_id, "request_id")
    payload = response["payload"]
    if not isinstance(payload, dict):
        raise ProbeError(f"response payload must be an object, observed={type(payload).__name__}")
    _require_exact_keys(payload, set(expected_payload), f"{expected_operation} payload")
    if payload != expected_payload:
        raise ProbeError(
            f"{expected_operation} payload mismatch: expected={expected_payload!r} observed={payload!r}"
        )


def roundtrip(
    process: subprocess.Popen[bytes],
    envelope: dict[str, Any],
    expected_operation: str,
    launch_id: int,
    request_id: int,
    expected_payload: dict[str, Any],
) -> int:
    started = time.perf_counter_ns()
    write_frame(process, envelope)
    response = read_frame_bounded(process)
    elapsed = time.perf_counter_ns() - started
    validate_response(
        response,
        expected_operation,
        launch_id,
        request_id,
        expected_payload,
    )
    return elapsed


def prove_health(process: subprocess.Popen[bytes], launch_id: int, request_id: int) -> int:
    return roundtrip(
        process,
        request("health", launch_id, request_id),
        "health",
        launch_id,
        request_id,
        {"status": "healthy"},
    )


def measure_cold(core: Path, samples: int) -> list[int]:
    values: list[int] = []
    for index in range(samples):
        started = time.perf_counter_ns()
        process = start_core(core)
        try:
            prove_health(process, index + 1, 1)
            values.append(time.perf_counter_ns() - started)
        finally:
            stop_core(process)
    return values


def measure_steady(core: Path, health_samples: int, cancel_samples: int) -> tuple[list[int], float, list[int]]:
    process = start_core(core)
    try:
        launch_id = 100_001
        next_id = 1
        prove_health(process, launch_id, next_id)
        next_id += 1

        health: list[int] = []
        throughput_started = time.perf_counter_ns()
        for _ in range(health_samples):
            health.append(prove_health(process, launch_id, next_id))
            next_id += 1
        throughput_elapsed = (time.perf_counter_ns() - throughput_started) / 1_000_000_000.0
        throughput = health_samples / throughput_elapsed

        cancellations: list[int] = []
        for _ in range(cancel_samples):
            observe_id = next_id
            roundtrip(
                process,
                request("observe_health", launch_id, observe_id),
                "observe_health",
                launch_id,
                observe_id,
                {},
            )
            next_id += 1
            cancel_id = next_id
            cancellations.append(
                roundtrip(
                    process,
                    cancel(launch_id, cancel_id, observe_id),
                    "cancel",
                    launch_id,
                    cancel_id,
                    {"outcome": "cancelled"},
                )
            )
            next_id += 1
        return health, throughput, cancellations
    finally:
        stop_core(process)


def measure_process_termination_and_replacement(core: Path, samples: int) -> tuple[list[int], list[int]]:
    termination: list[int] = []
    replacement: list[int] = []
    for index in range(samples):
        process = start_core(core)
        prove_health(process, 200_000 + index, 1)

        terminate_started = time.perf_counter_ns()
        process.kill()
        process.wait(timeout=2)
        termination.append(time.perf_counter_ns() - terminate_started)

        replacement_started = time.perf_counter_ns()
        replacement_process = start_core(core)
        try:
            prove_health(replacement_process, 300_000 + index, 1)
            replacement.append(time.perf_counter_ns() - replacement_started)
        finally:
            stop_core(replacement_process)
    return termination, replacement


def measure_rejection(core: Path, malformed: bool, samples: int) -> list[int]:
    values: list[int] = []
    for _ in range(samples):
        process = start_core(core)
        try:
            if process.stdin is None:
                raise ProbeError("Core stdin is unavailable")
            started = time.perf_counter_ns()
            if malformed:
                payload = b"{"
                process.stdin.write(struct.pack(">I", len(payload)) + payload)
            else:
                process.stdin.write(struct.pack(">I", MAX_PAYLOAD_BYTES + 1))
            process.stdin.flush()
            process.stdin.close()
            process.wait(timeout=2)
            values.append(time.perf_counter_ns() - started)
            if process.returncode == 0:
                raise ProbeError("invalid protocol input unexpectedly exited successfully")
        finally:
            if process.poll() is None:
                stop_core(process)
    return values


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_input_identities(
    core: Path,
    cargo_lock: Path,
    core_sha256: str,
    cargo_lock_sha256: str,
) -> None:
    final_core_sha256 = sha256_file(core)
    final_cargo_lock_sha256 = sha256_file(cargo_lock)
    if final_core_sha256 != core_sha256:
        raise ProbeError(
            f"Core identity drifted during measurement: before={core_sha256} after={final_core_sha256}"
        )
    if final_cargo_lock_sha256 != cargo_lock_sha256:
        raise ProbeError(
            "Cargo.lock identity drifted during measurement: "
            f"before={cargo_lock_sha256} after={final_cargo_lock_sha256}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", required=True)
    parser.add_argument("--cargo-lock", default="Cargo.lock")
    parser.add_argument("--output", required=True)
    parser.add_argument("--cold-samples", type=int, default=20)
    parser.add_argument("--health-samples", type=int, default=200)
    parser.add_argument("--cancel-samples", type=int, default=40)
    parser.add_argument("--failure-samples", type=int, default=10)
    args = parser.parse_args()

    for label, value in (
        ("cold-samples", args.cold_samples),
        ("health-samples", args.health_samples),
        ("cancel-samples", args.cancel_samples),
        ("failure-samples", args.failure_samples),
    ):
        if value <= 0:
            raise ProbeError(f"{label} must be positive")

    core = Path(args.core).resolve()
    cargo_lock = Path(args.cargo_lock).resolve()
    if not core.is_file():
        raise ProbeError(f"Core binary is missing: {core}")
    if not cargo_lock.is_file():
        raise ProbeError(f"Cargo.lock is missing: {cargo_lock}")

    core_sha256 = sha256_file(core)
    cargo_lock_sha256 = sha256_file(cargo_lock)

    cold = measure_cold(core, args.cold_samples)
    health, throughput, cancellations = measure_steady(
        core, args.health_samples, args.cancel_samples
    )
    process_termination, replacement = measure_process_termination_and_replacement(
        core, args.failure_samples
    )
    malformed = measure_rejection(core, True, args.failure_samples)
    oversized = measure_rejection(core, False, args.failure_samples)

    _verify_input_identities(core, cargo_lock, core_sha256, cargo_lock_sha256)

    result = {
        "protocol_version": PROTOCOL_VERSION,
        "core_sha256": core_sha256,
        "cargo_lock_sha256": cargo_lock_sha256,
        "cold_measurement_scope": "process_spawn_plus_first_health_roundtrip",
        "cold_samples": len(cold),
        "cold_p50_ms": percentile_ms(cold, 50),
        "cold_p95_ms": percentile_ms(cold, 95),
        "health_samples": len(health),
        "health_p50_ms": percentile_ms(health, 50),
        "health_p95_ms": percentile_ms(health, 95),
        "health_p99_ms": percentile_ms(health, 99),
        "throughput_rps": throughput,
        "cancel_samples": len(cancellations),
        "cancel_p95_ms": percentile_ms(cancellations, 95),
        "core_process_termination_p95_ms": percentile_ms(process_termination, 95),
        "core_replacement_handshake_p95_ms": percentile_ms(replacement, 95),
        "malformed_reject_p95_ms": percentile_ms(malformed, 95),
        "oversized_reject_p95_ms": percentile_ms(oversized, 95),
    }
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
