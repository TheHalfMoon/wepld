#!/usr/bin/env python3
"""Bounded successor policy for S1-013 performance and evidence execution.

v6 preserves canonical v5 and adds only three governed transitions:

1. one-time v5 -> v6 selector bootstrap;
2. one-time addition of the exact S1-013 performance probe/workflow; and
3. one-time S1-013 evidence/ledger reconciliation after the measured execution
   has merged and post-merge evidence exists.

The policy grants no new source, dependency, donor, model, provider, filesystem,
network-listener, agent-host, future-slice, Ready, merge, or completion authority.
S1-013 may execute only the already-admitted S1 Desktop/Core graph for measurement.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
import sys
from typing import Any, Callable

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v6_integrity.py"
V5_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v5_integrity.py"
EXPECTED_V5_POLICY_GIT_BLOB_SHA1 = "b6c4687eb7d3ef5439358a0b728c1f2874152df5"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
PERFORMANCE_WORKFLOW = ".github/workflows/s1-performance.yml"
PERFORMANCE_PROBE = ".github/scripts/wepld_s1_performance_probe.py"
PERFORMANCE_EVIDENCE = "specs/001-desktop-rust-trusted-core-handshake/s1-013-performance-evidence.md"
TASKS_PATH = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "360564599ad04878b3fbf34f79891e1ea8cf44580628208c28797567ef1a37f8",
    ADMISSION_WORKFLOW: "d37d45061d700e58d9ca531fe8636f431d0b51edc3e809487714b4f8ad9f85b0",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "4938d6bf46f1789b376f1bc45a5993c8270f7208dbb1ee85646d55f92b2a5978",
    ADMISSION_WORKFLOW: "8ccf32a8618054ee969e5ed1eb17cc95c0adfe0bf381d59f488255db08000bf8",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_PERFORMANCE_WORKFLOW_SHA256 = "54a363d84444a37d61bf11a1a83071f66697e4c9b86615bf462f1705cc48936e"
EXPECTED_PERFORMANCE_PROBE_SHA256 = "97f434c6cbf4bad156f16cbdd91b6bdd7205473a1e69f9045c6315852fbc0816"
EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1 = "d331b7f167fe67ae9061ed553cf0949fab12aae0"

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
PERFORMANCE_DELTA_PATHS = frozenset({PERFORMANCE_WORKFLOW, PERFORMANCE_PROBE})
EVIDENCE_DELTA_PATHS = frozenset({PERFORMANCE_EVIDENCE, TASKS_PATH})

AUTHORITY_EXPANSION = "S1_013_PERFORMANCE_EVIDENCE_ONLY"
EXISTING_RUNTIME_MEASUREMENT = "EXACT_ADMITTED_S1_GRAPH_ONLY"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
NEW_PRODUCT_RUNTIME_AUTHORITY = "NONE"
NETWORK_LISTENER_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
S1_014_PLUS = "NOT_AUTHORIZED"
CANDIDATE_VERIFY_AUTHORITY = "NONE"
CANDIDATE_POLICY_BASE_SOURCE = "LOCAL_FETCHED_GIT_WORKTREE"
TRUSTED_BASE_V5_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_v5_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(V5_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V5_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 steady-state routing v5 predecessor drifted before import: "
            f"expected={EXPECTED_V5_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_v5_before_import()
import wepld_s1_admission_steady_state_routing_v5_integrity as v5  # noqa: E402

_EXPECTED_V5_REQUIRE_EXACT_DELTA = v5._require_exact_delta_v5
_EXPECTED_V5_COMPARE_BASE_CONTROLLED = v5._compare_base_controlled_v5
_EXPECTED_V5_VALIDATE_ALLOWED_PATHS = v5._validate_allowed_paths_v5
_EXPECTED_V5_VERIFY_POLICY_FILES = v5._verify_policy_files_v5
_EXPECTED_V5_DESKTOP_EXTENSION = v5._verify_desktop_extension_paths_v5
_EXPECTED_V5_EXECUTION_EXTENSION = v5._verify_execution_extension_paths_v5
_EXPECTED_V5_PRINT_SUCCESS = v5._print_success


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        topology = v5._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 steady-state routing v6 topology/layout drifted: {exc}")
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("S1 steady-state routing v6 inherited topology is malformed")
    return topology


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"S1 steady-state routing v6 {label} topology is malformed")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"S1 steady-state routing v6 {label} contains non-string path")
    return frozenset(value)


def _require_attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 steady-state routing v6 {label} topology/layout drifted: {exc}")


def _guard(label: str, callable_obj: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(callable_obj):
        base.fail(f"S1 steady-state routing v6 {label} topology/layout drifted: not callable")
    try:
        return callable_obj(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 steady-state routing v6 {label} topology/layout drifted: {exc}")


def _extension_paths(component: Any, label: str) -> frozenset[str]:
    return _require_path_set(_require_attr(component, "EXTENSION_CONTROLLED_PATHS", label), label)


def _changed_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> frozenset[str]:
    return _require_path_set(v5._changed_paths_v5(candidate, policy_base), "changed-path")


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_v5(view: base.RepositoryView, label: str) -> None:
    if V5_POLICY_PATH not in _paths(view):
        base.fail(f"{label} is missing frozen v5 predecessor")
    actual = _git_blob_sha1(view.read_bytes(V5_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V5_POLICY_GIT_BLOB_SHA1:
        base.fail(
            f"{label} v5 predecessor drifted: "
            f"expected={EXPECTED_V5_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_sha256(view: base.RepositoryView, path: str, expected: str, label: str) -> None:
    actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
    if actual != expected:
        base.fail(f"{label} drifted: expected={expected} actual={actual}")


def _require_performance_files(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    transition: bool,
) -> None:
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)
    for path, digest, label in (
        (PERFORMANCE_WORKFLOW, EXPECTED_PERFORMANCE_WORKFLOW_SHA256, "S1-013 performance workflow"),
        (PERFORMANCE_PROBE, EXPECTED_PERFORMANCE_PROBE_SHA256, "S1-013 performance probe"),
    ):
        if path not in candidate_paths:
            base.fail(f"{label} is missing from candidate")
        _require_sha256(candidate, path, digest, label)
        if transition:
            if path in base_paths:
                base.fail(f"{label} already exists in trusted base")
        else:
            if path not in base_paths:
                base.fail(f"{label} is missing from trusted base")
            _require_sha256(policy_base, path, digest, f"trusted-base {label}")
            if candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                path, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail(f"{label} changed after canonical admission")


def _derive_completed_tasks(base_bytes: bytes) -> bytes:
    if _git_blob_sha1(base_bytes) != EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1:
        base.fail(
            "S1-013 ledger trusted base drifted: "
            f"expected={EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1} "
            f"actual={_git_blob_sha1(base_bytes)}"
        )
    text = base_bytes.decode("utf-8")
    old_top = """ACTIVE_TASK = NONE
NEXT_TASK = S1-013_NOT_STARTED
FOUNDER_STANDING_AUTHORIZATION = GRANTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_PLUS = NOT_STARTED"""
    new_top = """ACTIVE_TASK = NONE
NEXT_TASK = S1-014_NOT_STARTED
FOUNDER_STANDING_AUTHORIZATION = GRANTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_ACTIVATION = PROVEN
S1_014_PLUS = NOT_STARTED"""
    old_section = """## S1-013 — Performance and evidence packet

- [ ] Measure cold Core spawn + handshake.
- [ ] Measure health request p50/p95/p99.
- [ ] Measure bounded small-request throughput.
- [ ] Measure idle Desktop/Core memory and idle CPU.
- [ ] Measure cancellation latency.
- [ ] Measure crash detection + fresh-handshake recovery.
- [ ] Measure malformed/oversized-payload rejection cost.
- [ ] Measure sustained diagnostic-drain behavior and retained-diagnostics truncation.
- [ ] Tighten initial budgets where evidence supports a lower bound.
- [ ] Record exact Desktop/Core binaries, toolchain, lockfile, protocol version, commit and platform identities."""
    new_section = """## S1-013 — Performance and evidence packet

- [x] Measure cold Core spawn + handshake.
- [x] Measure health request p50/p95/p99.
- [x] Measure bounded small-request throughput.
- [x] Measure idle Desktop/Core memory and idle CPU.
- [x] Measure cancellation latency.
- [x] Measure crash detection + fresh-handshake recovery.
- [x] Measure malformed/oversized-payload rejection cost.
- [x] Measure sustained diagnostic-drain behavior and retained-diagnostics truncation.
- [x] Tighten initial budgets where evidence supports a lower bound.
- [x] Record exact Desktop/Core binaries, toolchain, lockfile, protocol version, commit and platform identities.

Evidence: `specs/001-desktop-rust-trusted-core-handshake/s1-013-performance-evidence.md`."""
    old_gate = """COMPLETED = S1-001 THROUGH S1-012
CURRENT = CANONICAL_LEDGER_RECONCILIATION_ONLY
CANONICAL_EXECUTION_HEAD = 848566d89e5995e215295b92d9da4a9cfbe28927
S1_012_CANONICAL_ACTIVATION = PROVEN
NEXT = S1-013_ONLY_AFTER_THIS_LEDGER_RECONCILIATION_IS_QUALIFIED_AND_MERGED
S1_013_PLUS = NOT_STARTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011"""
    new_gate = """COMPLETED = S1-001 THROUGH S1-013
CURRENT = S1-013_CLOSED_CANONICAL_PROVEN
CANONICAL_EXECUTION_HEAD = SEE_S1_013_PERFORMANCE_EVIDENCE
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_ACTIVATION = PROVEN
NEXT = S1-014_NOT_STARTED
S1_014_PLUS = NOT_STARTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011"""
    for old, new, label in (
        (old_top, new_top, "ledger header"),
        (old_section, new_section, "S1-013 checklist"),
        (old_gate, new_gate, "current gate"),
    ):
        if text.count(old) != 1:
            base.fail(f"S1-013 {label} source marker count is not exactly one")
        text = text.replace(old, new, 1)
    return text.encode("utf-8")


_EVIDENCE_REQUIRED_MARKERS = (
    "SUBJECT_MERGE_SHA = ",
    "FOUNDATION_PUSH_RUN = ",
    "S1_CONTRACTS_PUSH_RUN = ",
    "S1_PERFORMANCE_PUSH_RUN = ",
    f"PERFORMANCE_WORKFLOW_SHA256 = {EXPECTED_PERFORMANCE_WORKFLOW_SHA256}",
    f"PERFORMANCE_PROBE_SHA256 = {EXPECTED_PERFORMANCE_PROBE_SHA256}",
    "SOURCE_ADMISSION = NONE",
    "DEPENDENCY_ADMISSION = NONE",
    "NEW_PRODUCT_RUNTIME_AUTHORITY = NONE",
    "MODEL_PROVIDER_EXECUTION = NONE",
    "S1_PERF_COLD_P50_MS = ",
    "S1_PERF_HEALTH_P50_MS = ",
    "S1_PERF_HEALTH_P95_MS = ",
    "S1_PERF_HEALTH_P99_MS = ",
    "S1_PERF_THROUGHPUT_RPS = ",
    "S1_PERF_IDLE_DESKTOP_WORKING_SET_MEAN_BYTES = ",
    "S1_PERF_IDLE_CORE_WORKING_SET_MEAN_BYTES = ",
    "S1_PERF_IDLE_DESKTOP_CPU_SECONDS = ",
    "S1_PERF_IDLE_CORE_CPU_SECONDS = ",
    "S1_PERF_CANCEL_P95_MS = ",
    "S1_PERF_CRASH_DETECT_P95_MS = ",
    "S1_PERF_RECOVERY_P95_MS = ",
    "S1_PERF_OVERSIZED_REJECT_P95_MS = ",
    "S1_PERF_MALFORMED_REJECT_P95_MS = ",
    "S1_PERF_DIAGNOSTIC_DRAIN_ELAPSED_MS = ",
    "S1_PERF_DIAGNOSTIC_TRUNCATION_OBSERVED = PASS",
    "S1_PERF_DESKTOP_SHA256 = ",
    "S1_PERF_CORE_SHA256 = ",
    "S1_PERF_CARGO_LOCK_SHA256 = ",
    "S1_PERF_PROTOCOL_VERSION = 1",
    "BUDGET_TIGHTENING_DECISION = ",
)


def _validate_evidence_bytes(data: bytes) -> None:
    if len(data) > 64_000:
        base.fail("S1-013 performance evidence exceeds 64 KiB")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        base.fail(f"S1-013 performance evidence is not UTF-8: {exc}")
    if not text.startswith("# S1-013 Performance and Evidence Packet\n"):
        base.fail("S1-013 performance evidence title drifted")
    for marker in _EVIDENCE_REQUIRED_MARKERS:
        if marker not in text:
            base.fail(f"S1-013 performance evidence missing marker: {marker}")
    match = re.search(r"^SUBJECT_MERGE_SHA = ([0-9a-f]{40})$", text, re.MULTILINE)
    if match is None:
        base.fail("S1-013 evidence subject merge SHA is malformed")
    for label in ("FOUNDATION_PUSH_RUN", "S1_CONTRACTS_PUSH_RUN", "S1_PERFORMANCE_PUSH_RUN"):
        if re.search(rf"^{label} = [1-9][0-9]*$", text, re.MULTILINE) is None:
            base.fail(f"S1-013 evidence {label} is malformed")


def _require_exact_performance_transition(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    if _git_blob_sha1(policy_base.read_bytes(TASKS_PATH, base.MAX_POLICY_FILE_BYTES)) != (
        EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1
    ):
        base.fail("S1-013 performance transition requires exact unreconciled S1 ledger")
    _require_performance_files(candidate, policy_base, transition=True)


def _require_exact_evidence_transition(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _require_performance_files(candidate, policy_base, transition=False)
    base_paths = _paths(policy_base)
    candidate_paths = _paths(candidate)
    if PERFORMANCE_EVIDENCE in base_paths:
        base.fail("S1-013 evidence transition is one-time; evidence already exists")
    if PERFORMANCE_EVIDENCE not in candidate_paths:
        base.fail("S1-013 evidence candidate is missing evidence packet")
    evidence = candidate.read_bytes(PERFORMANCE_EVIDENCE, base.MAX_POLICY_FILE_BYTES)
    _validate_evidence_bytes(evidence)

    base_tasks = policy_base.read_bytes(TASKS_PATH, base.MAX_POLICY_FILE_BYTES)
    expected_tasks = _derive_completed_tasks(base_tasks)
    candidate_tasks = candidate.read_bytes(TASKS_PATH, base.MAX_POLICY_FILE_BYTES)
    if candidate_tasks != expected_tasks:
        base.fail("S1-013 tasks ledger is not the exact deterministic completion transform")


def _require_exact_delta_v6(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_v5(candidate, "S1 routing v6 bootstrap candidate")
            _require_v5(policy_base, "S1 routing v6 trusted base")
            snapshot_present, _, _ = v5._source_snapshot_api()
            if _guard("source-snapshot presence", snapshot_present, candidate) and not _guard(
                "source-snapshot presence", snapshot_present, policy_base
            ):
                base.fail("source snapshot cannot transition during S1 routing v6 bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 steady-state routing v6 bootstrap delta must be exactly "
                "the v6 policy plus Foundation and admission workflows"
            )

    if changed == PERFORMANCE_DELTA_PATHS:
        _require_exact_performance_transition(candidate, policy_base)
        return
    if changed & PERFORMANCE_DELTA_PATHS:
        base.fail(
            "S1-013 performance execution delta must be exactly the performance workflow and probe"
        )

    if changed == EVIDENCE_DELTA_PATHS:
        _require_exact_evidence_transition(candidate, policy_base)
        return
    if changed & EVIDENCE_DELTA_PATHS:
        base.fail(
            "S1-013 evidence reconciliation delta must be exactly evidence packet plus tasks ledger"
        )

    _guard(
        "predecessor exact-delta verifier",
        _EXPECTED_V5_REQUIRE_EXACT_DELTA,
        candidate,
        policy_base,
    )


def _compare_base_controlled_v6(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    controlled = _require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")

    for relative in sorted(controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "S1 steady-state routing v6 workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                base.fail(
                    "S1 steady-state routing v6 trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"S1 steady-state routing v6 steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    snapshot_present, verify_snapshot, base_acquisition_tree = v5._source_snapshot_api()
    base_has_snapshot = _guard("source-snapshot presence", snapshot_present, policy_base)
    candidate_has_snapshot = _guard("source-snapshot presence", snapshot_present, candidate)
    if base_has_snapshot:
        if not candidate_has_snapshot:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        _guard("source-snapshot base verification", verify_snapshot, policy_base, transition=False)
        _guard("source-snapshot candidate verification", verify_snapshot, candidate, transition=False)
    elif candidate_has_snapshot:
        if policy_base.tree_identity("docs/acquisition") != base_acquisition_tree:
            base.fail("source-admission trusted-base acquisition identity drifted")
        _guard("source-snapshot transition verification", verify_snapshot, candidate, transition=True)


def _verify_extension_paths_v6(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled: frozenset[str],
) -> None:
    safe = _require_path_set(controlled, "extension-controlled-path")
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)
    bootstrap = _is_bootstrap_base(policy_base)

    if POLICY_SCRIPT in safe:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("S1 steady-state routing v6 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 steady-state routing v6 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 steady-state routing v6 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 steady-state routing v6 steady-state wrapper changed")

    if PERFORMANCE_PROBE in safe:
        candidate_has = PERFORMANCE_PROBE in candidate_paths
        base_has = PERFORMANCE_PROBE in base_paths
        if candidate_has:
            _require_sha256(
                candidate,
                PERFORMANCE_PROBE,
                EXPECTED_PERFORMANCE_PROBE_SHA256,
                "S1-013 performance probe",
            )
        if base_has:
            _require_sha256(
                policy_base,
                PERFORMANCE_PROBE,
                EXPECTED_PERFORMANCE_PROBE_SHA256,
                "trusted-base S1-013 performance probe",
            )
        if base_has and not candidate_has:
            base.fail("canonical S1-013 performance probe was deleted")
        if candidate_has and base_has and candidate.read_bytes(
            PERFORMANCE_PROBE, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(PERFORMANCE_PROBE, base.MAX_POLICY_FILE_BYTES):
            base.fail("canonical S1-013 performance probe changed")

    delegated = frozenset(safe - {POLICY_SCRIPT, PERFORMANCE_PROBE})
    if delegated:
        _guard(
            "predecessor extension verifier",
            v5._verify_extension_paths_v5,
            candidate,
            policy_base,
            delegated,
        )


def _verify_desktop_extension_paths_v6(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v6(
        candidate,
        policy_base,
        _extension_paths(desktop, "desktop-extension"),
    )


def _verify_execution_extension_paths_v6(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v6(
        candidate,
        policy_base,
        _extension_paths(execution, "execution-extension"),
    )


def _validate_allowed_paths_v6(paths: set[str], stage: str) -> None:
    projected = set(paths) - {
        POLICY_SCRIPT,
        PERFORMANCE_WORKFLOW,
        PERFORMANCE_PROBE,
        PERFORMANCE_EVIDENCE,
    }
    _guard(
        "predecessor tracked-path verifier",
        _EXPECTED_V5_VALIDATE_ALLOWED_PATHS,
        projected,
        stage,
    )


def _verify_policy_files_v6(view: base.RepositoryView) -> None:
    _require_v5(view, "S1 routing v6 policy verification")
    _guard("predecessor policy-file verifier", _EXPECTED_V5_VERIFY_POLICY_FILES, view)
    if PERFORMANCE_PROBE in _paths(view):
        _require_sha256(
            view,
            PERFORMANCE_PROBE,
            EXPECTED_PERFORMANCE_PROBE_SHA256,
            "S1-013 performance probe",
        )
    if PERFORMANCE_WORKFLOW in _paths(view):
        _require_sha256(
            view,
            PERFORMANCE_WORKFLOW,
            EXPECTED_PERFORMANCE_WORKFLOW_SHA256,
            "S1-013 performance workflow",
        )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is not _EXPECTED_V5_PRINT_SUCCESS:
        base.fail("S1 steady-state routing v6 predecessor success-printer drifted")
    _guard("predecessor success-printer", _PRIOR_PRINT_SUCCESS, stage, mode)
    print("s1_admission_steady_state_route_v6=V5_PRESERVED_PLUS_S1_013_PERFORMANCE_EVIDENCE")
    print(f"s1_admission_authority_expansion_v6={AUTHORITY_EXPANSION}")
    print(f"s1_013_existing_runtime_measurement_v6={EXISTING_RUNTIME_MEASUREMENT}")
    print(f"effective_source_admission_v6={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission_v6={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution_v6={DONOR_EXECUTION}")
    print(f"new_product_runtime_authority_v6={NEW_PRODUCT_RUNTIME_AUTHORITY}")
    print(f"network_listener_authority_v6={NETWORK_LISTENER_AUTHORITY}")
    print(f"effective_model_provider_execution_v6={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access_v6={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference_v6={MODEL_INFERENCE}")
    print(f"s1_014_plus_v6={S1_014_PLUS}")


def _require_overlay_identity_v6() -> None:
    shell, retention, _, desktop, execution = _topology()
    expected = (
        (_require_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "overlay exact-delta"), _require_exact_delta_v6, "exact-delta"),
        (base.compare_base_controlled, _compare_base_controlled_v6, "base-control"),
        (_require_attr(desktop, "verify_extension_controlled_paths", "overlay desktop-extension"), _verify_desktop_extension_paths_v6, "desktop-extension"),
        (_require_attr(execution, "verify_extension_controlled_paths", "overlay execution-extension"), _verify_execution_extension_paths_v6, "execution-extension"),
        (_require_attr(shell, "validate_allowed_paths", "overlay tracked-path"), _validate_allowed_paths_v6, "tracked-path"),
        (_require_attr(shell, "verify_policy_files", "overlay policy-file"), _verify_policy_files_v6, "policy-file"),
        (_require_attr(shell, "print_success", "overlay success-printer"), _print_success, "success-printer"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 steady-state routing v6 overlay {label} hook drifted")
    if _PRIOR_PRINT_SUCCESS is not _EXPECTED_V5_PRINT_SUCCESS:
        base.fail("S1 steady-state routing v6 predecessor success-printer drifted")
    if POLICY_SCRIPT not in _extension_paths(desktop, "desktop-extension"):
        base.fail("S1 steady-state routing v6 desktop extension registration drifted")
    if POLICY_SCRIPT not in _extension_paths(execution, "execution-extension"):
        base.fail("S1 steady-state routing v6 execution extension registration drifted")
    if PERFORMANCE_PROBE not in _extension_paths(desktop, "desktop-extension"):
        base.fail("S1-013 performance probe desktop registration drifted")
    if PERFORMANCE_PROBE not in _extension_paths(execution, "execution-extension"):
        base.fail("S1-013 performance probe execution registration drifted")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity_v6()
        return

    v5.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    _guard("predecessor policy install", v5._install_policy)

    shell, retention, _, desktop, execution = _topology()
    expected = (
        (_require_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "predecessor exact-delta"), _EXPECTED_V5_REQUIRE_EXACT_DELTA, "exact-delta"),
        (base.compare_base_controlled, _EXPECTED_V5_COMPARE_BASE_CONTROLLED, "base-control"),
        (_require_attr(shell, "validate_allowed_paths", "predecessor tracked-path"), _EXPECTED_V5_VALIDATE_ALLOWED_PATHS, "tracked-path"),
        (_require_attr(shell, "verify_policy_files", "predecessor policy-file"), _EXPECTED_V5_VERIFY_POLICY_FILES, "policy-file"),
        (_require_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop-extension"), _EXPECTED_V5_DESKTOP_EXTENSION, "desktop-extension"),
        (_require_attr(execution, "verify_extension_controlled_paths", "predecessor execution-extension"), _EXPECTED_V5_EXECUTION_EXTENSION, "execution-extension"),
        (_require_attr(shell, "print_success", "predecessor success-printer"), _EXPECTED_V5_PRINT_SUCCESS, "success-printer"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 steady-state routing v6 predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = _EXPECTED_V5_PRINT_SUCCESS
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(_extension_paths(desktop, "desktop-extension")) | {POLICY_SCRIPT, PERFORMANCE_PROBE}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(_extension_paths(execution, "execution-extension")) | {POLICY_SCRIPT, PERFORMANCE_PROBE}
    )
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v6
    base.compare_base_controlled = _compare_base_controlled_v6
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v6
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v6
    shell.validate_allowed_paths = _validate_allowed_paths_v6
    shell.verify_policy_files = _verify_policy_files_v6
    shell.print_success = _print_success
    _INSTALLED = True
    _require_overlay_identity_v6()


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in (FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW):
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                "S1 steady-state routing v6 workflow drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _selftest_authority() -> None:
    if AUTHORITY_EXPANSION != "S1_013_PERFORMANCE_EVIDENCE_ONLY":
        base.fail("S1 steady-state routing v6 authority boundary drifted")
    if EXISTING_RUNTIME_MEASUREMENT != "EXACT_ADMITTED_S1_GRAPH_ONLY":
        base.fail("S1-013 existing-runtime measurement boundary drifted")
    prohibited = (
        SOURCE_ADMISSION,
        DEPENDENCY_ADMISSION,
        DONOR_EXECUTION,
        NEW_PRODUCT_RUNTIME_AUTHORITY,
        NETWORK_LISTENER_AUTHORITY,
        MODEL_PROVIDER_EXECUTION,
        MODEL_WEIGHT_ACCESS,
        MODEL_INFERENCE,
        CANDIDATE_VERIFY_AUTHORITY,
    )
    if prohibited != ("NONE",) * len(prohibited):
        base.fail("S1 steady-state routing v6 prohibited authority boundary drifted")
    if S1_014_PLUS != "NOT_AUTHORIZED":
        base.fail("S1-014+ boundary drifted")
    if TRUSTED_BASE_V5_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":
        base.fail("S1 steady-state routing v6 old-base truth classification drifted")
    if CANDIDATE_POLICY_BASE_SOURCE != "LOCAL_FETCHED_GIT_WORKTREE":
        base.fail("S1 steady-state routing v6 candidate base-source contract drifted")


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(
        files,
        trees={path: _git_blob_sha1(data) for path, data in files.items()},
    )


def _selftest_bootstrap_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    local = base.LocalRepositoryView(root)
    v5_bytes = local.read_bytes(V5_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        V5_POLICY_PATH: v5_bytes,
        FOUNDATION_WORKFLOW: b"old-foundation",
        ADMISSION_WORKFLOW: b"old-admission",
    }
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            POLICY_SCRIPT: b"policy-v6",
            FOUNDATION_WORKFLOW: b"new-foundation",
            ADMISSION_WORKFLOW: b"new-admission",
        }
    )
    _require_exact_delta_v6(_memory_view(candidate_files), _memory_view(base_files))

    mixed = dict(candidate_files)
    mixed["README.md"] = b"unexpected"
    base.expect_failure_matching(
        "S1 routing v6 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v6,
        _memory_view(mixed),
        _memory_view(base_files),
    )


def _selftest_task_transform() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    current = view.read_bytes(TASKS_PATH, base.MAX_POLICY_FILE_BYTES)
    transformed = _derive_completed_tasks(current)
    if transformed == current:
        base.fail("S1-013 ledger completion transform made no change")
    if b"NEXT_TASK = S1-014_NOT_STARTED" not in transformed:
        base.fail("S1-013 ledger completion transform lost next-task marker")
    if b"S1_013_CANONICAL_ACTIVATION = PROVEN" not in transformed:
        base.fail("S1-013 ledger completion transform lost activation marker")


def _selftest_overlay_reentry() -> None:
    _require_overlay_identity_v6()
    shell, retention, _, _, _ = _topology()
    original_printer = _require_attr(shell, "print_success", "self-test success-printer")
    try:
        shell.print_success = lambda *_args, **_kwargs: None
        base.expect_failure_matching(
            "S1 routing v6 post-install success-printer drift",
            "overlay success-printer hook drifted",
            _install_policy,
        )
    finally:
        shell.print_success = original_printer

    original_delta = _require_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "self-test exact-delta")
    try:
        retention.IMPL_REQUIRE_EXACT_DELTA = _EXPECTED_V5_REQUIRE_EXACT_DELTA
        base.expect_failure_matching(
            "S1 routing v6 post-install exact-delta drift",
            "overlay exact-delta hook drifted",
            _install_policy,
        )
    finally:
        retention.IMPL_REQUIRE_EXACT_DELTA = original_delta
    _require_overlay_identity_v6()


def selftest() -> None:
    v5.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v5.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_authority()
    _selftest_bootstrap_contract()
    _selftest_task_transform()
    _selftest_overlay_reentry()
    print("wepld S1 steady-state routing v6 policy self-tests: PASS")


def _candidate_parser(argv: list[str]) -> Any:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", required=True)
    parser.add_argument("--policy-base-root", required=True)
    parser.add_argument("--policy-base-sha", required=True)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0

        _install_policy()

        if argv and argv[0] == "verify-candidate-local":
            args = _candidate_parser(argv[1:])
            return _guard(
                "predecessor candidate-local verifier",
                v5.verify_candidate_local,
                args.root,
                args.policy_base_root,
                args.policy_base_sha,
            )

        return _guard("predecessor runtime main", v5.main, argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
