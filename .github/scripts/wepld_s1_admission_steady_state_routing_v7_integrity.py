#!/usr/bin/env python3
"""Bound v6 to recoverable S1-013 measurement artifacts without widening authority.

v7 is an append-only successor to canonical v6. It preserves all still-eligible
v6 routes, closes the predecessor late-lookup hardening gap, and replaces only
the future S1-013 performance workflow/probe identities with immutable,
recoverable Git-object identities. Evidence closeout and S1-014+ remain closed.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v7_integrity.py"
V6_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v6_integrity.py"
EXPECTED_V6_POLICY_GIT_BLOB_SHA1 = "7e33708e41ee75540c57a652e2898b52e18fc153"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
PERFORMANCE_WORKFLOW = ".github/workflows/s1-performance.yml"
PERFORMANCE_PROBE = ".github/scripts/wepld_s1_performance_probe.py"
TASKS_PATH = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "4938d6bf46f1789b376f1bc45a5993c8270f7208dbb1ee85646d55f92b2a5978",
    ADMISSION_WORKFLOW: "8ccf32a8618054ee969e5ed1eb17cc95c0adfe0bf381d59f488255db08000bf8",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "f33f139ad72f15caa02a95d54376f0c44451ce5deabfa26c406103fd10fd7c9a",
    ADMISSION_WORKFLOW: "acaf3a58ff825e194a964b4003947506759d6ecfcdb75711d2ca8d138c84fdbd",
    ".github/workflows/s1-contracts.yml": "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

EXPECTED_PERFORMANCE_WORKFLOW_SHA256 = "5d1e52667f2c00b4076d059dcf495e271b2dfa18bf91ee59d553fb6846f4e846"
EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1 = "86a4e77abe5ac8d59a86f593088af6d044a4c861"
EXPECTED_PERFORMANCE_PROBE_SHA256 = "2299fe3e041e86338deb9ef2b25af86db33a15fedf0b749cc09af813dfbe7ca5"
EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1 = "6df27f3c798f12aa04939e77a436fcf8de18dd90"
EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1 = "d331b7f167fe67ae9061ed553cf0949fab12aae0"

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
PERFORMANCE_DELTA_PATHS = frozenset({PERFORMANCE_WORKFLOW, PERFORMANCE_PROBE})

AUTHORITY_EXPANSION = "S1_013_PERFORMANCE_MEASUREMENT_IDENTITY_REBIND_ONLY"
EXISTING_RUNTIME_MEASUREMENT = "EXACT_ADMITTED_S1_GRAPH_ONLY"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
NEW_PRODUCT_RUNTIME_AUTHORITY = "NONE"
NETWORK_LISTENER_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
S1_013_EVIDENCE_CLOSEOUT = "NOT_AUTHORIZED_BY_V7"
S1_014_PLUS = "NOT_AUTHORIZED"
TRUSTED_BASE_V6_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_v6_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(V6_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V6_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 routing v6 predecessor drifted before import: "
            f"expected={EXPECTED_V6_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_v6_before_import()
import wepld_s1_admission_steady_state_routing_v6_integrity as v6  # noqa: E402

_EXPECTED_V6_REQUIRE_EXACT_DELTA = v6._require_exact_delta_v6
_EXPECTED_V6_COMPARE_BASE_CONTROLLED = v6._compare_base_controlled_v6
_EXPECTED_V6_VALIDATE_ALLOWED_PATHS = v6._validate_allowed_paths_v6
_EXPECTED_V6_VERIFY_POLICY_FILES = v6._verify_policy_files_v6
_EXPECTED_V6_DESKTOP_EXTENSION = v6._verify_desktop_extension_paths_v6
_EXPECTED_V6_EXECUTION_EXTENSION = v6._verify_execution_extension_paths_v6
_EXPECTED_V6_EXTENSION_HELPER = v6._verify_extension_paths_v6
_EXPECTED_V6_PRINT_SUCCESS = v6._print_success
_EXPECTED_V5_EXTENSION_HELPER = v6.v5._verify_extension_paths_v5
_EXPECTED_CANDIDATE_LOCAL = v6._EXPECTED_CANDIDATE_LOCAL
_EXPECTED_RUNTIME_MAIN = v6._EXPECTED_RUNTIME_MAIN


def _call(label: str, function: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(function):
        base.fail(f"S1 routing v7 {label} drifted: not callable")
    try:
        return function(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 routing v7 {label} topology/layout drifted: {exc}")


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", v6._topology)
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("S1 routing v7 inherited topology is malformed")
    return value


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail(f"S1 routing v7 {label} topology is malformed")
    return frozenset(value)


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 routing v7 {label} topology/layout drifted: {exc}")


def _extension_paths(component: Any, label: str) -> frozenset[str]:
    return _require_path_set(_attr(component, "EXTENSION_CONTROLLED_PATHS", label), label)


def _changed_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> frozenset[str]:
    return _require_path_set(
        _call("changed-path", v6._changed_paths, candidate, policy_base),
        "changed-path",
    )


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_v6(view: base.RepositoryView, label: str) -> None:
    if V6_POLICY_PATH not in _paths(view):
        base.fail(f"{label} is missing frozen v6 predecessor")
    actual = _git_blob_sha1(view.read_bytes(V6_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V6_POLICY_GIT_BLOB_SHA1:
        base.fail(
            f"{label} v6 predecessor drifted: "
            f"expected={EXPECTED_V6_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_predecessor_identity() -> None:
    if v6._verify_extension_paths_v6 is not _EXPECTED_V6_EXTENSION_HELPER:
        base.fail("S1 routing v7 v6 extension verifier identity drifted")
    if v6.v5._verify_extension_paths_v5 is not _EXPECTED_V5_EXTENSION_HELPER:
        base.fail("S1 routing v7 frozen v5 extension verifier identity drifted")


def _require_artifact(view: base.RepositoryView, path: str, sha256: str, git_blob: str, label: str) -> None:
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    actual_sha256 = _sha256(data)
    actual_blob = _git_blob_sha1(data)
    if actual_sha256 != sha256 or actual_blob != git_blob:
        base.fail(
            f"{label} identity drifted: "
            f"sha256 expected={sha256} actual={actual_sha256}; "
            f"git_blob expected={git_blob} actual={actual_blob}"
        )


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
    for path, sha256, git_blob, label in (
        (
            PERFORMANCE_WORKFLOW,
            EXPECTED_PERFORMANCE_WORKFLOW_SHA256,
            EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1,
            "S1-013 performance workflow",
        ),
        (
            PERFORMANCE_PROBE,
            EXPECTED_PERFORMANCE_PROBE_SHA256,
            EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1,
            "S1-013 performance probe",
        ),
    ):
        if path in base_paths:
            base.fail(f"{label} already exists in trusted base")
        if path not in candidate_paths:
            base.fail(f"{label} is missing from candidate")
        _require_artifact(candidate, path, sha256, git_blob, label)


def _require_exact_delta_v7(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)
    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_v6(candidate, "S1 routing v7 bootstrap candidate")
            _require_v6(policy_base, "S1 routing v7 trusted base")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 routing v7 bootstrap delta must be exactly "
                "the v7 policy plus Foundation and admission workflows"
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
        _EXPECTED_V6_REQUIRE_EXACT_DELTA,
        candidate,
        policy_base,
    )


def _compare_base_controlled_v7(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    if not _is_bootstrap_base(policy_base):
        _call(
            "predecessor base-controlled verifier",
            _EXPECTED_V6_COMPARE_BASE_CONTROLLED,
            candidate,
            policy_base,
        )
        return

    for relative in sorted(_require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if relative in BOOTSTRAP_WORKFLOWS:
            actual_candidate = _sha256(candidate_bytes)
            actual_base = _sha256(base_bytes)
            if actual_candidate != EXPECTED_WORKFLOW_SHA256[relative]:
                base.fail(
                    f"S1 routing v7 workflow candidate drifted: {relative}: "
                    f"expected={EXPECTED_WORKFLOW_SHA256[relative]} actual={actual_candidate}"
                )
            if actual_base != PRIOR_EXPECTED_WORKFLOW_SHA256[relative]:
                base.fail(
                    f"S1 routing v7 trusted-base workflow drifted: {relative}: "
                    f"expected={PRIOR_EXPECTED_WORKFLOW_SHA256[relative]} actual={actual_base}"
                )
            continue
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_v7(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled: frozenset[str],
) -> None:
    _require_predecessor_identity()
    safe = _require_path_set(controlled, "extension-controlled-path")
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in safe:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("S1 routing v7 policy wrapper is missing")
        if _is_bootstrap_base(policy_base):
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 routing v7 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 routing v7 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 routing v7 steady-state wrapper changed")

    delegated = frozenset(safe - {POLICY_SCRIPT})
    if delegated:
        _call(
            "pinned v6 extension verifier",
            _EXPECTED_V6_EXTENSION_HELPER,
            candidate,
            policy_base,
            delegated,
        )


def _verify_desktop_extension_paths_v7(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v7(
        candidate,
        policy_base,
        _extension_paths(desktop, "desktop-extension"),
    )


def _verify_execution_extension_paths_v7(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v7(
        candidate,
        policy_base,
        _extension_paths(execution, "execution-extension"),
    )


def _validate_allowed_paths_v7(paths: set[str], stage: str) -> None:
    projected = set(paths) - {POLICY_SCRIPT}
    _call(
        "predecessor tracked-path verifier",
        _EXPECTED_V6_VALIDATE_ALLOWED_PATHS,
        projected,
        stage,
    )


def _verify_policy_files_v7(view: base.RepositoryView) -> None:
    _require_v6(view, "S1 routing v7 policy verification")
    _require_predecessor_identity()
    _call("predecessor policy-file verifier", _EXPECTED_V6_VERIFY_POLICY_FILES, view)
    if POLICY_SCRIPT not in _paths(view):
        base.fail("S1 routing v7 policy wrapper is missing")
    if PERFORMANCE_WORKFLOW in _paths(view):
        _require_artifact(
            view,
            PERFORMANCE_WORKFLOW,
            EXPECTED_PERFORMANCE_WORKFLOW_SHA256,
            EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1,
            "S1-013 performance workflow",
        )
    if PERFORMANCE_PROBE in _paths(view):
        _require_artifact(
            view,
            PERFORMANCE_PROBE,
            EXPECTED_PERFORMANCE_PROBE_SHA256,
            EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1,
            "S1-013 performance probe",
        )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is not _EXPECTED_V6_PRINT_SUCCESS:
        base.fail("S1 routing v7 predecessor success-printer drifted")
    _call("predecessor success-printer", _PRIOR_PRINT_SUCCESS, stage, mode)
    print("s1_admission_steady_state_route_v7=V6_PRESERVED_PLUS_RECOVERABLE_S1_013_MEASUREMENT")
    print(f"s1_admission_authority_expansion_v7={AUTHORITY_EXPANSION}")
    print(f"s1_013_existing_runtime_measurement_v7={EXISTING_RUNTIME_MEASUREMENT}")
    print(f"effective_source_admission_v7={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission_v7={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution_v7={DONOR_EXECUTION}")
    print(f"new_product_runtime_authority_v7={NEW_PRODUCT_RUNTIME_AUTHORITY}")
    print(f"network_listener_authority_v7={NETWORK_LISTENER_AUTHORITY}")
    print(f"effective_model_provider_execution_v7={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access_v7={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference_v7={MODEL_INFERENCE}")
    print(f"s1_013_evidence_closeout_v7={S1_013_EVIDENCE_CLOSEOUT}")
    print(f"s1_014_plus_v7={S1_014_PLUS}")


def _require_overlay_identity_v7() -> None:
    _require_predecessor_identity()
    shell, retention, _, desktop, execution = _topology()
    expected = (
        (_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "overlay exact-delta"), _require_exact_delta_v7, "exact-delta"),
        (base.compare_base_controlled, _compare_base_controlled_v7, "base-control"),
        (_attr(desktop, "verify_extension_controlled_paths", "overlay desktop-extension"), _verify_desktop_extension_paths_v7, "desktop-extension"),
        (_attr(execution, "verify_extension_controlled_paths", "overlay execution-extension"), _verify_execution_extension_paths_v7, "execution-extension"),
        (_attr(shell, "validate_allowed_paths", "overlay tracked-path"), _validate_allowed_paths_v7, "tracked-path"),
        (_attr(shell, "verify_policy_files", "overlay policy-file"), _verify_policy_files_v7, "policy-file"),
        (_attr(shell, "print_success", "overlay success-printer"), _print_success, "success-printer"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 routing v7 overlay {label} hook drifted")
    if _PRIOR_PRINT_SUCCESS is not _EXPECTED_V6_PRINT_SUCCESS:
        base.fail("S1 routing v7 predecessor success-printer drifted")
    for component, label in ((desktop, "desktop"), (execution, "execution")):
        if POLICY_SCRIPT not in _extension_paths(component, f"{label}-extension"):
            base.fail(f"S1 routing v7 {label} extension registration drifted")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity_v7()
        return

    v6.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v6.EXPECTED_PERFORMANCE_WORKFLOW_SHA256 = EXPECTED_PERFORMANCE_WORKFLOW_SHA256
    v6.EXPECTED_PERFORMANCE_PROBE_SHA256 = EXPECTED_PERFORMANCE_PROBE_SHA256
    _call("predecessor policy install", v6._install_policy)

    _require_predecessor_identity()
    shell, retention, _, desktop, execution = _topology()
    predecessor = (
        (_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "predecessor exact-delta"), _EXPECTED_V6_REQUIRE_EXACT_DELTA, "exact-delta"),
        (base.compare_base_controlled, _EXPECTED_V6_COMPARE_BASE_CONTROLLED, "base-control"),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop-extension"), _EXPECTED_V6_DESKTOP_EXTENSION, "desktop-extension"),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution-extension"), _EXPECTED_V6_EXECUTION_EXTENSION, "execution-extension"),
        (_attr(shell, "validate_allowed_paths", "predecessor tracked-path"), _EXPECTED_V6_VALIDATE_ALLOWED_PATHS, "tracked-path"),
        (_attr(shell, "verify_policy_files", "predecessor policy-file"), _EXPECTED_V6_VERIFY_POLICY_FILES, "policy-file"),
        (_attr(shell, "print_success", "predecessor success-printer"), _EXPECTED_V6_PRINT_SUCCESS, "success-printer"),
    )
    for actual, wanted, label in predecessor:
        if actual is not wanted:
            base.fail(f"S1 routing v7 predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = _EXPECTED_V6_PRINT_SUCCESS
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(_extension_paths(desktop, "desktop-extension")) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(_extension_paths(execution, "execution-extension")) | {POLICY_SCRIPT}
    )
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v7
    base.compare_base_controlled = _compare_base_controlled_v7
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v7
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v7
    shell.validate_allowed_paths = _validate_allowed_paths_v7
    shell.verify_policy_files = _verify_policy_files_v7
    shell.print_success = _print_success
    _INSTALLED = True
    _require_overlay_identity_v7()


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(
        files,
        trees={path: _git_blob_sha1(data) for path, data in files.items()},
    )


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != EXPECTED_WORKFLOW_SHA256[path]:
            base.fail(
                f"S1 routing v7 workflow drifted: {path}: "
                f"expected={EXPECTED_WORKFLOW_SHA256[path]} actual={actual}"
            )


def _selftest_authority_and_bindings() -> None:
    if AUTHORITY_EXPANSION != "S1_013_PERFORMANCE_MEASUREMENT_IDENTITY_REBIND_ONLY":
        base.fail("S1 routing v7 authority boundary drifted")
    if EXISTING_RUNTIME_MEASUREMENT != "EXACT_ADMITTED_S1_GRAPH_ONLY":
        base.fail("S1 routing v7 runtime-measurement boundary drifted")
    expected_none = (
        SOURCE_ADMISSION,
        DEPENDENCY_ADMISSION,
        DONOR_EXECUTION,
        NEW_PRODUCT_RUNTIME_AUTHORITY,
        NETWORK_LISTENER_AUTHORITY,
        MODEL_PROVIDER_EXECUTION,
        MODEL_WEIGHT_ACCESS,
        MODEL_INFERENCE,
    )
    if expected_none != ("NONE",) * len(expected_none):
        base.fail("S1 routing v7 prohibited authority boundary drifted")
    if S1_013_EVIDENCE_CLOSEOUT != "NOT_AUTHORIZED_BY_V7" or S1_014_PLUS != "NOT_AUTHORIZED":
        base.fail("S1 routing v7 future-slice boundary drifted")
    if TRUSTED_BASE_V6_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":
        base.fail("S1 routing v7 old-base truth classification drifted")
    for value, length, label in (
        (EXPECTED_PERFORMANCE_WORKFLOW_SHA256, 64, "performance workflow SHA-256"),
        (EXPECTED_PERFORMANCE_PROBE_SHA256, 64, "performance probe SHA-256"),
        (EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1, 40, "performance workflow Git blob"),
        (EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1, 40, "performance probe Git blob"),
    ):
        if len(value) != length or any(char not in "0123456789abcdef" for char in value):
            base.fail(f"S1 routing v7 {label} identity is malformed")
    _require_predecessor_identity()


def _selftest_bootstrap_contract() -> None:
    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    v6_bytes = local.read_bytes(V6_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        V6_POLICY_PATH: v6_bytes,
        FOUNDATION_WORKFLOW: b"old-foundation",
        ADMISSION_WORKFLOW: b"old-admission",
    }
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            POLICY_SCRIPT: b"policy-v7",
            FOUNDATION_WORKFLOW: b"new-foundation",
            ADMISSION_WORKFLOW: b"new-admission",
        }
    )
    _require_exact_delta_v7(_memory_view(candidate_files), _memory_view(base_files))
    mixed = dict(candidate_files)
    mixed["README.md"] = b"unexpected"
    base.expect_failure_matching(
        "S1 routing v7 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v7,
        _memory_view(mixed),
        _memory_view(base_files),
    )


def _selftest_identity_hardening() -> None:
    original = v6.v5._verify_extension_paths_v5
    try:
        v6.v5._verify_extension_paths_v5 = lambda *_args, **_kwargs: None
        base.expect_failure_matching(
            "S1 routing v7 predecessor late-lookup rejection",
            "frozen v5 extension verifier identity drifted",
            _require_predecessor_identity,
        )
    finally:
        v6.v5._verify_extension_paths_v5 = original
    _require_predecessor_identity()


def _selftest_overlay_reentry() -> None:
    shell, _, _, _, _ = _topology()
    original = _attr(shell, "print_success", "self-test success-printer")
    try:
        shell.print_success = lambda *_args, **_kwargs: None
        base.expect_failure_matching(
            "S1 routing v7 post-install success-printer drift",
            "overlay success-printer hook drifted",
            _install_policy,
        )
    finally:
        shell.print_success = original
    _require_overlay_identity_v7()


def selftest() -> None:
    v6.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v6.EXPECTED_PERFORMANCE_WORKFLOW_SHA256 = EXPECTED_PERFORMANCE_WORKFLOW_SHA256
    v6.EXPECTED_PERFORMANCE_PROBE_SHA256 = EXPECTED_PERFORMANCE_PROBE_SHA256
    v6.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_authority_and_bindings()
    _selftest_bootstrap_contract()
    _selftest_identity_hardening()
    _selftest_overlay_reentry()
    print("wepld S1 steady-state routing v7 policy self-tests: PASS")


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
