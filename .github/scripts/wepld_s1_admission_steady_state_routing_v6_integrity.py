#!/usr/bin/env python3
"""Authorize only the bounded S1-013 performance-measurement route over canonical v5.

This successor preserves all canonical v5 routes. It adds:
1. one exact v5->v6 selector bootstrap; and
2. after v6 is canonical, one exact two-file S1-013 measurement transition.

It grants no new source, dependency, donor, product-runtime, network-listener,
provider, model, S1-014+, merge, Ready, or completion authority.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v6_integrity.py"
V5_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v5_integrity.py"
EXPECTED_V5_POLICY_GIT_BLOB_SHA1 = "b6c4687eb7d3ef5439358a0b728c1f2874152df5"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
PERFORMANCE_WORKFLOW = ".github/workflows/s1-performance.yml"
PERFORMANCE_PROBE = ".github/scripts/wepld_s1_performance_probe.py"
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
EXPECTED_PERFORMANCE_WORKFLOW_SHA256 = "b8069f188a8d7a1e284537509a0938a99563c05e735e3d8d516a913e778dbd14"
EXPECTED_PERFORMANCE_PROBE_SHA256 = "762fa487044b2c9975088915632c9573d631db40abf0486c75d459251f228986"
EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1 = "d331b7f167fe67ae9061ed553cf0949fab12aae0"

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
PERFORMANCE_DELTA_PATHS = frozenset({PERFORMANCE_WORKFLOW, PERFORMANCE_PROBE})

AUTHORITY_EXPANSION = "S1_013_PERFORMANCE_MEASUREMENT_ONLY"
EXISTING_RUNTIME_MEASUREMENT = "EXACT_ADMITTED_S1_GRAPH_ONLY"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
NEW_PRODUCT_RUNTIME_AUTHORITY = "NONE"
NETWORK_LISTENER_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
S1_013_EVIDENCE_CLOSEOUT = "NOT_AUTHORIZED_BY_V6"
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
_EXPECTED_CANDIDATE_LOCAL = v5.v4.verify_candidate_local
_EXPECTED_RUNTIME_MAIN = v5.v4.main


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        value = v5._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 routing v6 topology/layout drifted: {exc}")
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("S1 routing v6 inherited topology is malformed")
    return value


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail(f"S1 routing v6 {label} topology is malformed")
    return frozenset(value)


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 routing v6 {label} topology/layout drifted: {exc}")


def _call(label: str, function: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(function):
        base.fail(f"S1 routing v6 {label} topology/layout drifted: not callable")
    try:
        return function(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 routing v6 {label} topology/layout drifted: {exc}")


def _extension_paths(component: Any, label: str) -> frozenset[str]:
    return _require_path_set(_attr(component, "EXTENSION_CONTROLLED_PATHS", label), label)


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


def _require_exact_performance_transition(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    if _git_blob_sha1(policy_base.read_bytes(TASKS_PATH, base.MAX_POLICY_FILE_BYTES)) != (
        EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1
    ):
        base.fail("S1-013 measurement transition requires exact unreconciled S1 ledger")

    base_paths = _paths(policy_base)
    candidate_paths = _paths(candidate)
    for path, digest, label in (
        (PERFORMANCE_WORKFLOW, EXPECTED_PERFORMANCE_WORKFLOW_SHA256, "S1-013 performance workflow"),
        (PERFORMANCE_PROBE, EXPECTED_PERFORMANCE_PROBE_SHA256, "S1-013 performance probe"),
    ):
        if path in base_paths:
            base.fail(f"{label} already exists in trusted base")
        if path not in candidate_paths:
            base.fail(f"{label} is missing from candidate")
        _require_sha256(candidate, path, digest, label)


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
            if _call("source-snapshot presence", snapshot_present, candidate) and not _call(
                "source-snapshot presence", snapshot_present, policy_base
            ):
                base.fail("source snapshot cannot transition during S1 routing v6 bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 routing v6 bootstrap delta must be exactly "
                "the v6 policy plus Foundation and admission workflows"
            )

    if changed == PERFORMANCE_DELTA_PATHS:
        _require_exact_performance_transition(candidate, policy_base)
        return
    if changed & PERFORMANCE_DELTA_PATHS:
        base.fail(
            "S1-013 measurement delta must be exactly the performance workflow and probe"
        )

    _call(
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
    for relative in sorted(_require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "S1 routing v6 workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                base.fail(
                    "S1 routing v6 trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"S1 routing v6 steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    snapshot_present, verify_snapshot, base_acquisition_tree = v5._source_snapshot_api()
    base_has = _call("source-snapshot presence", snapshot_present, policy_base)
    candidate_has = _call("source-snapshot presence", snapshot_present, candidate)
    if base_has:
        if not candidate_has:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        _call("source-snapshot base verification", verify_snapshot, policy_base, transition=False)
        _call("source-snapshot candidate verification", verify_snapshot, candidate, transition=False)
    elif candidate_has:
        if policy_base.tree_identity("docs/acquisition") != base_acquisition_tree:
            base.fail("source-admission trusted-base acquisition identity drifted")
        _call("source-snapshot transition verification", verify_snapshot, candidate, transition=True)


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
            base.fail("S1 routing v6 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 routing v6 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 routing v6 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 routing v6 steady-state wrapper changed")

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
        _call(
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
    projected = set(paths) - {POLICY_SCRIPT, PERFORMANCE_WORKFLOW, PERFORMANCE_PROBE}
    _call(
        "predecessor tracked-path verifier",
        _EXPECTED_V5_VALIDATE_ALLOWED_PATHS,
        projected,
        stage,
    )


def _verify_policy_files_v6(view: base.RepositoryView) -> None:
    _require_v5(view, "S1 routing v6 policy verification")
    _call("predecessor policy-file verifier", _EXPECTED_V5_VERIFY_POLICY_FILES, view)
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
        base.fail("S1 routing v6 predecessor success-printer drifted")
    _call("predecessor success-printer", _PRIOR_PRINT_SUCCESS, stage, mode)
    print("s1_admission_steady_state_route_v6=V5_PRESERVED_PLUS_S1_013_MEASUREMENT")
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
    print(f"s1_013_evidence_closeout_v6={S1_013_EVIDENCE_CLOSEOUT}")
    print(f"s1_014_plus_v6={S1_014_PLUS}")


def _require_overlay_identity_v6() -> None:
    shell, retention, _, desktop, execution = _topology()
    expected = (
        (_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "overlay exact-delta"), _require_exact_delta_v6, "exact-delta"),
        (base.compare_base_controlled, _compare_base_controlled_v6, "base-control"),
        (_attr(desktop, "verify_extension_controlled_paths", "overlay desktop-extension"), _verify_desktop_extension_paths_v6, "desktop-extension"),
        (_attr(execution, "verify_extension_controlled_paths", "overlay execution-extension"), _verify_execution_extension_paths_v6, "execution-extension"),
        (_attr(shell, "validate_allowed_paths", "overlay tracked-path"), _validate_allowed_paths_v6, "tracked-path"),
        (_attr(shell, "verify_policy_files", "overlay policy-file"), _verify_policy_files_v6, "policy-file"),
        (_attr(shell, "print_success", "overlay success-printer"), _print_success, "success-printer"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 routing v6 overlay {label} hook drifted")
    if _PRIOR_PRINT_SUCCESS is not _EXPECTED_V5_PRINT_SUCCESS:
        base.fail("S1 routing v6 predecessor success-printer drifted")
    for component, label in ((desktop, "desktop"), (execution, "execution")):
        paths = _extension_paths(component, f"{label}-extension")
        if POLICY_SCRIPT not in paths or PERFORMANCE_PROBE not in paths:
            base.fail(f"S1 routing v6 {label} extension registration drifted")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity_v6()
        return

    v5.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    _call("predecessor policy install", v5._install_policy)

    shell, retention, _, desktop, execution = _topology()
    predecessor = (
        (_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "predecessor exact-delta"), _EXPECTED_V5_REQUIRE_EXACT_DELTA, "exact-delta"),
        (base.compare_base_controlled, _EXPECTED_V5_COMPARE_BASE_CONTROLLED, "base-control"),
        (_attr(shell, "validate_allowed_paths", "predecessor tracked-path"), _EXPECTED_V5_VALIDATE_ALLOWED_PATHS, "tracked-path"),
        (_attr(shell, "verify_policy_files", "predecessor policy-file"), _EXPECTED_V5_VERIFY_POLICY_FILES, "policy-file"),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop-extension"), _EXPECTED_V5_DESKTOP_EXTENSION, "desktop-extension"),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution-extension"), _EXPECTED_V5_EXECUTION_EXTENSION, "execution-extension"),
        (_attr(shell, "print_success", "predecessor success-printer"), _EXPECTED_V5_PRINT_SUCCESS, "success-printer"),
    )
    for actual, wanted, label in predecessor:
        if actual is not wanted:
            base.fail(f"S1 routing v6 predecessor {label} hook drifted")

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


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(
        files,
        trees={path: _git_blob_sha1(data) for path, data in files.items()},
    )


def _selftest_bootstrap_contract() -> None:
    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    v5_bytes = local.read_bytes(V5_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        V5_POLICY_PATH: v5_bytes,
        FOUNDATION_WORKFLOW: b"old-foundation",
        ADMISSION_WORKFLOW: b"old-admission",
    }
    candidate_files = {
        **base_files,
        POLICY_SCRIPT: b"policy-v6",
        FOUNDATION_WORKFLOW: b"new-foundation",
        ADMISSION_WORKFLOW: b"new-admission",
    }
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


def _selftest_authority_and_bindings() -> None:
    expected_none = (
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
    if expected_none != ("NONE",) * len(expected_none):
        base.fail("S1 routing v6 prohibited authority boundary drifted")
    if AUTHORITY_EXPANSION != "S1_013_PERFORMANCE_MEASUREMENT_ONLY":
        base.fail("S1 routing v6 authority expansion drifted")
    if EXISTING_RUNTIME_MEASUREMENT != "EXACT_ADMITTED_S1_GRAPH_ONLY":
        base.fail("S1 routing v6 measurement boundary drifted")
    if S1_013_EVIDENCE_CLOSEOUT != "NOT_AUTHORIZED_BY_V6" or S1_014_PLUS != "NOT_AUTHORIZED":
        base.fail("S1 routing v6 future authority boundary drifted")
    if TRUSTED_BASE_V5_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":
        base.fail("S1 routing v6 old-base classification drifted")
    if CANDIDATE_POLICY_BASE_SOURCE != "LOCAL_FETCHED_GIT_WORKTREE":
        base.fail("S1 routing v6 candidate base-source contract drifted")
    for digest, label in (
        (EXPECTED_PERFORMANCE_WORKFLOW_SHA256, "performance workflow"),
        (EXPECTED_PERFORMANCE_PROBE_SHA256, "performance probe"),
    ):
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            base.fail(f"S1 routing v6 {label} digest is malformed")
    if not callable(_EXPECTED_CANDIDATE_LOCAL) or not callable(_EXPECTED_RUNTIME_MAIN):
        base.fail("S1 routing v6 predecessor execution entrypoint drifted")


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in (FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW):
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                f"S1 routing v6 workflow drifted: {path}: expected={expected} actual={actual}"
            )


def _selftest_overlay_reentry() -> None:
    shell, _, _, _, _ = _topology()
    original = _attr(shell, "print_success", "self-test success-printer")
    try:
        shell.print_success = lambda *_args, **_kwargs: None
        base.expect_failure_matching(
            "S1 routing v6 post-install success-printer drift",
            "overlay success-printer hook drifted",
            _install_policy,
        )
    finally:
        shell.print_success = original
    _require_overlay_identity_v6()


def selftest() -> None:
    v5.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v5.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_authority_and_bindings()
    _selftest_bootstrap_contract()
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
            return _call(
                "predecessor candidate-local verifier",
                _EXPECTED_CANDIDATE_LOCAL,
                args.root,
                args.policy_base_root,
                args.policy_base_sha,
            )
        return _call("predecessor runtime main", _EXPECTED_RUNTIME_MAIN, argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
