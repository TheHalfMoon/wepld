#!/usr/bin/env python3
"""Repair S1-013 closeout self-test sequencing without expanding authority.

v12 is an append-only successor to canonical v11. It preserves v11 runtime,
admission, Harness-ledger compatibility, source/dependency/runtime/provider,
and S1-014 boundaries. The only intended semantic change is self-test ordering:
the frozen predecessor self-tests run before v11 installs its closeout ledger
compatibility hooks, so predecessor fixtures cannot be reinterpreted as
post-closeout ledgers missing evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v12_integrity.py"
V11 = ".github/scripts/wepld_s1_admission_steady_state_routing_v11_integrity.py"
V11_BLOB = "02f84c4441ef75ea08fb8501adddd123a80ce42f"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

OLD_WF = {
    FW: "b26645b136df346a2563dcf5d18d875efc66c7e637e3929bfd521e76f152ecdc",
    AW: "f84d843d050e144bd96e668137568047fb8ba120e204a3338ac766651f25633f",
}
WF = {
    FW: "bee8dc667a00043ff34f5bba5920946a78c09ef2fdfed6ba186ad5cdc0717943",
    AW: "ab378e3e38ae943f98db92c5ef859338c4c62917d04b3fa7e67b3c8ea70906ca",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S1_013_CLOSEOUT_SELFTEST_SEQUENCING_REPAIR_ONLY"
S1_014 = "NOT_AUTHORIZED"
TRUSTED_BASE_V11_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"  # noqa: S105

_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None


def blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ps(view: Any) -> set[str]:
    return {entry.path for entry in view.entries()}


def _call(label: str, function: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(function):
        base.fail(f"v12 {label} drifted: not callable")
    try:
        return function(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v12 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v12 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v12 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _require_local(path: str, expected: str, label: str) -> None:
    actual = blob(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
    if actual != expected:
        base.fail(f"{label} drifted before import: expected={expected} actual={actual}")


_require_local(V11, V11_BLOB, "frozen v11 predecessor")

import wepld_s1_admission_steady_state_routing_v11_integrity as v11  # noqa: E402

V11_DELTA = v11.delta
V11_BASE = v11.basectrl
V11_ALLOWED = v11.allowed
V11_FILES = v11.files
V11_DEXT = v11.dext
V11_EEXT = v11.eext
V11_EXT = v11.ext
V11_PRINT = v11.printer
V11_WF = dict(v11.WF)
CAND = v11.CAND
RUNTIME = v11.RUNTIME


def req_v11(view: Any) -> None:
    if V11 not in ps(view):
        base.fail("v12 candidate/base is missing frozen v11 predecessor")
    actual = blob(view.read_bytes(V11, base.MAX_POLICY_FILE_BYTES))
    if actual != V11_BLOB:
        base.fail(f"frozen v11 predecessor drifted: expected={V11_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v11, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v12 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v12 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v11, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v12 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def patch_workflows() -> None:
    current = dict(v11.WF)
    expected = {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}
    if current not in (expected, dict(WF)):
        base.fail(f"v12 predecessor workflow identity map drifted: actual={current}")
    _bind(v11, "WF", dict(WF), "v11 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v11(candidate)
            req_v11(policy_base)
            return
        if paths & BOOT:
            base.fail("v12 bootstrap delta must be exactly policy plus two workflows")
    _call("v11 exact-delta verifier", V11_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v11 base-control verifier", V11_BASE, candidate, policy_base)
        return

    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v12 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v12 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v12 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v12 steady-state wrapper drifted")

    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v11 extension verification", V11_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    _call("v11 allowed-path verification", V11_ALLOWED, set(paths) - {P}, stage)


def files(view: Any) -> None:
    req_v11(view)
    _call("v11 policy-file verification", V11_FILES, view)
    if P not in ps(view):
        base.fail("v12 wrapper missing")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V11_PRINT:
        base.fail("v12 predecessor printer drifted")
    _call("v11 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v12=V11_PLUS_SELFTEST_SEQUENCING_REPAIR")
    print(f"s1_admission_authority_expansion_v12={AUTH}")
    print("s1_013_closeout_authority_v12=UNCHANGED_FROM_V11")
    print("harness_research_authority_expansion_v12=NONE")
    print("harness_h0_authority_expansion_v12=NONE")
    print("effective_source_admission_v12=NONE")
    print("effective_dependency_admission_v12=NONE")
    print("effective_donor_execution_v12=NONE")
    print("new_product_runtime_authority_v12=NONE")
    print("effective_model_provider_execution_v12=NONE")
    print("effective_model_weight_access_v12=NONE")
    print("effective_model_inference_v12=NONE")
    print(f"s1_014_plus_v12={S1_014}")


def overlay() -> None:
    """Fail closed if any installed v12 binding drifts between invocations."""
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop extension hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution extension hook"), eext),
        (_attr(shell, "validate_allowed_paths", "shell allowed-path hook"), allowed),
        (_attr(shell, "verify_policy_files", "shell policy-file hook"), files),
        (_attr(shell, "print_success", "shell success hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v12 installed overlay drifted")
    if _PRINT is not V11_PRINT:
        base.fail("v12 predecessor printer identity drifted")
    if dict(v11.WF) != dict(WF):
        base.fail("v12 workflow identity projection drifted")
    if _EXPECTED_DESKTOP_EXTENSIONS is None or _EXPECTED_EXECUTION_EXTENSIONS is None:
        base.fail("v12 installed extension registration is unavailable")
    if extset(desktop) != _EXPECTED_DESKTOP_EXTENSIONS:
        base.fail("v12 desktop extension registration drifted")
    if extset(execution) != _EXPECTED_EXECUTION_EXTENSIONS:
        base.fail("v12 execution extension registration drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return

    patch_workflows()
    _call("v11 install", getattr(v11, "install", None))
    shell, routing, _, desktop, execution = topo()

    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook"), V11_DELTA),
        (base.compare_base_controlled, V11_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop extension hook"), V11_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "execution extension hook"), V11_EEXT),
        (_attr(shell, "validate_allowed_paths", "shell allowed-path hook"), V11_ALLOWED),
        (_attr(shell, "verify_policy_files", "shell policy-file hook"), V11_FILES),
        (_attr(shell, "print_success", "shell success hook"), V11_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v12 predecessor hook drifted")

    _PRINT = V11_PRINT
    _EXPECTED_DESKTOP_EXTENSIONS = frozenset(set(extset(desktop)) | {P})
    _EXPECTED_EXECUTION_EXTENSIONS = frozenset(set(extset(execution)) | {P})
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        _EXPECTED_DESKTOP_EXTENSIONS,
        "desktop extension registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        _EXPECTED_EXECUTION_EXTENSIONS,
        "execution extension registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "routing exact-delta binding")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "desktop extension hook binding")
    _bind(execution, "verify_extension_controlled_paths", eext, "execution extension hook binding")
    _bind(shell, "validate_allowed_paths", allowed, "shell allowed-path hook binding")
    _bind(shell, "verify_policy_files", files, "shell policy-file hook binding")
    _bind(shell, "print_success", printer, "shell success hook binding")
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def _corrected_v11_selftest() -> None:
    """Project candidate workflows, then test predecessors before compat hooks."""
    _call(
        "v11 workflow identity projection",
        _attr(v11, "patch_workflows", "v11 workflow identity projection"),
    )
    predecessor_v10 = _attr(v11, "v10", "v11 v10 predecessor module")
    _call(
        "v10 predecessor self-test",
        _attr(predecessor_v10, "selftest", "v10 predecessor self-test"),
    )
    _call(
        "v11 compatibility hook installation",
        _attr(v11, "patch_compat", "v11 compatibility hook installer"),
    )
    _call(
        "v11 install for corrected self-test",
        _attr(v11, "install", "v11 install"),
    )

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v12 workflow drifted while validating v11 predecessor: {path}")

    if _attr(v11, "AUTH", "v11 authority marker") != (
        "S1_013_CLOSEOUT_HARNESS_LEDGER_COMPATIBILITY_REPAIR_ONLY"
    ):
        base.fail("v12 observed v11 authority drift")
    if _attr(v11, "S1_014", "v11 S1-014 boundary") != "NOT_AUTHORIZED":
        base.fail("v12 observed v11 S1-014 boundary drift")
    if (
        _attr(v11, "TRUSTED_BASE_V10_CLASS", "v11 bootstrap class")
        != "EXPECTED_BOOTSTRAP_FAILURE"
        or _attr(v11, "OLD_BASE_S1_PASS", "v11 old-base status") != "NO"  # noqa: S105
    ):
        base.fail("v12 observed v11 bootstrap status semantics drift")

    vb = root.read_bytes(v11.V10, base.MAX_POLICY_FILE_BYTES)
    policy_base = {v11.V10: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({v11.P: b"v11", FW: b"new-foundation", AW: b"new-admission"})
    v11.delta(mem(candidate), mem(policy_base))

    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v12 corrected v11 mixed bootstrap",
        "bootstrap delta must be exactly",
        v11.delta,
        mem(mixed),
        mem(policy_base),
    )

    _call(
        "v11 ledger compatibility self-test",
        _attr(
            v11,
            "_selftest_ledger_compatibility",
            "v11 ledger compatibility self-test",
        ),
    )
    _call(
        "v11 repeated-install self-test",
        _attr(
            v11,
            "_selftest_repeated_install_drift",
            "v11 repeated-install self-test",
        ),
    )


def _selftest_repeated_install_drift() -> None:
    shell, routing, _, desktop, _ = topo()

    original_delta = _attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook")
    try:
        _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", V11_DELTA, "self-test routing drift")
        base.expect_failure_matching(
            "v12 repeated install routing hook drift",
            "installed overlay drifted",
            install,
        )
    finally:
        _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", original_delta, "self-test routing restore")
    overlay()

    original_desktop_extensions = extset(desktop)
    try:
        _bind(
            desktop,
            "EXTENSION_CONTROLLED_PATHS",
            frozenset(set(original_desktop_extensions) - {P}),
            "self-test desktop extension drift",
        )
        base.expect_failure_matching(
            "v12 repeated install extension registration drift",
            "desktop extension registration drifted",
            install,
        )
    finally:
        _bind(
            desktop,
            "EXTENSION_CONTROLLED_PATHS",
            original_desktop_extensions,
            "self-test desktop extension restore",
        )
    overlay()

    original_workflows = dict(v11.WF)
    try:
        _bind(v11, "WF", dict(V11_WF), "self-test workflow identity drift")
        base.expect_failure_matching(
            "v12 repeated install workflow identity drift",
            "workflow identity projection drifted",
            install,
        )
    finally:
        _bind(v11, "WF", original_workflows, "self-test workflow identity restore")
    overlay()

    if _attr(shell, "print_success", "shell success hook") is not printer:
        base.fail("v12 repeated-install self-test failed to restore installed overlay")


def selftest() -> None:
    patch_workflows()
    _corrected_v11_selftest()
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v12 workflow drifted: {path}")

    if AUTH != "S1_013_CLOSEOUT_SELFTEST_SEQUENCING_REPAIR_ONLY":
        base.fail("v12 authority drifted")
    if S1_014 != "NOT_AUTHORIZED":
        base.fail("v12 S1-014 boundary drifted")
    if (
        TRUSTED_BASE_V11_CLASS != "EXPECTED_BOOTSTRAP_FAILURE"
        or OLD_BASE_S1_PASS != "NO"  # noqa: S105
    ):
        base.fail("v12 bootstrap status semantics drifted")

    vb = root.read_bytes(V11, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V11: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v12", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v12 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    _selftest_repeated_install_drift()
    print("wepld S1 steady-state routing v12 policy self-tests: PASS")


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0
        install()
        if argv and argv[0] == "verify-candidate-local":
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("--root", required=True)
            parser.add_argument("--policy-base-root", required=True)
            parser.add_argument("--policy-base-sha", required=True)
            args = parser.parse_args(argv[1:])
            return int(
                _call(
                    "candidate-local verifier",
                    CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
