#!/usr/bin/env python3
"""Repair the bounded S1-013 performance probe identity without widening authority.

v9 is an append-only successor to canonical v8. It preserves every still-eligible
v8 route and changes only the content-addressed identity of the future S1-013
performance probe after exact-head independent review found three material
measurement-integrity defects. The repaired performance workflow is unchanged.
Evidence closeout and S1-014+ remain closed.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v9_integrity.py"
V8_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v8_integrity.py"
EXPECTED_V8_POLICY_GIT_BLOB_SHA1 = "f5f2500a7fff0480cc97ee6148273e5b7d8d6792"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
PERFORMANCE_WORKFLOW = ".github/workflows/s1-performance.yml"
PERFORMANCE_PROBE = ".github/scripts/wepld_s1_performance_probe.py"
TASKS_PATH = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "0ef7a516e35342c4742476601b937d244101ca7c8775f40393af6504077452da",
    ADMISSION_WORKFLOW: "1f24486dbed564b7d065fcd61641d3106433345ea58975ccb87db058afb69758",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "c49e76220a3d514ae8abca79034f65c444a8363c072c9d76e032f7483cd6c2d9",
    ADMISSION_WORKFLOW: "3e4453bb8f53f1baeefb5953bf62501a8311627fc3cffc4fe6ce6f219ce7af7d",
    ".github/workflows/s1-contracts.yml": "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

EXPECTED_PERFORMANCE_WORKFLOW_SHA256 = "7dd7f670740b651e30700a0fe10b4f1dcd8d51a46b257789e54a02c74df98784"
EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1 = "b16d57b42e617808d4b5d2547c1677e9ef7c3535"
REJECTED_PERFORMANCE_PROBE_SHA256 = "4aa961c62a47fda9a560bd2928d6a3414d72cefacad00666b094cbaac91bfd57"
REJECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1 = "b7326bc0656469d77e5f99fd7a9cf42958efe5fd"
EXPECTED_PERFORMANCE_PROBE_SHA256 = "57e6f977fb31995a78ad902efd8ee024087cfabd9d22595c2256730b7352d860"
EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1 = "f72837df9a88824dae530746e17d6be31904580d"
EXPECTED_PRE_S1_013_TASKS_GIT_BLOB_SHA1 = "d331b7f167fe67ae9061ed553cf0949fab12aae0"

REJECTED_MEASUREMENT_HEAD = "56f03eea9a8a2eeaa39c79821f9ae0b8e1d9c3f6"
REJECTED_MEASUREMENT_RUN = "32929228402"
REJECTED_MEASUREMENT_CLASS = "EXACT_HEAD_MEASUREMENT_INVALIDATED_BY_THREE_MATERIAL_REVIEW_FINDINGS"
REVIEW_FINDING_IDS = (
    "3860338193",
    "3860338199",
    "3860338204",
)

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
PERFORMANCE_DELTA_PATHS = frozenset({PERFORMANCE_WORKFLOW, PERFORMANCE_PROBE})

AUTHORITY_EXPANSION = "S1_013_PERFORMANCE_PROBE_REVIEW_REPAIR_ONLY"
EXISTING_RUNTIME_MEASUREMENT = "EXACT_ADMITTED_S1_GRAPH_ONLY"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
NEW_PRODUCT_RUNTIME_AUTHORITY = "NONE"
NETWORK_LISTENER_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
S1_013_EVIDENCE_CLOSEOUT = "NOT_AUTHORIZED_BY_V9"
S1_014_PLUS = "NOT_AUTHORIZED"
TRUSTED_BASE_V8_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_v8_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(V8_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V8_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 routing v8 predecessor drifted before import: "
            f"expected={EXPECTED_V8_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_v8_before_import()
import wepld_s1_admission_steady_state_routing_v8_integrity as v8  # noqa: E402

_EXPECTED_V8_REQUIRE_EXACT_DELTA = v8._require_exact_delta_v8
_EXPECTED_V8_COMPARE_BASE_CONTROLLED = v8._compare_base_controlled_v8
_EXPECTED_V8_VALIDATE_ALLOWED_PATHS = v8._validate_allowed_paths_v8
_EXPECTED_V8_VERIFY_POLICY_FILES = v8._verify_policy_files_v8
_EXPECTED_V8_DESKTOP_EXTENSION = v8._verify_desktop_extension_paths_v8
_EXPECTED_V8_EXECUTION_EXTENSION = v8._verify_execution_extension_paths_v8
_EXPECTED_V8_EXTENSION_HELPER = v8._verify_extension_paths_v8
_EXPECTED_V8_PRINT_SUCCESS = v8._print_success
_EXPECTED_V8_PREDECESSOR_IDENTITY = v8._require_predecessor_identity
_EXPECTED_CANDIDATE_LOCAL = v8._EXPECTED_CANDIDATE_LOCAL
_EXPECTED_RUNTIME_MAIN = v8._EXPECTED_RUNTIME_MAIN


def _call(label: str, function: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(function):
        base.fail(f"S1 routing v9 {label} drifted: not callable")
    try:
        return function(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 routing v9 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"S1 routing v9 {label} topology/layout drifted: {exc}")


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", v8._topology)
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("S1 routing v9 inherited topology is malformed")
    return value


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail(f"S1 routing v9 {label} topology is malformed")
    return frozenset(value)


def _extension_paths(component: Any, label: str) -> frozenset[str]:
    return _require_path_set(_attr(component, "EXTENSION_CONTROLLED_PATHS", label), label)


def _changed_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> frozenset[str]:
    return _require_path_set(
        _call("changed-path", v8._changed_paths, candidate, policy_base),
        "changed-path",
    )


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_v8(view: base.RepositoryView, label: str) -> None:
    if V8_POLICY_PATH not in _paths(view):
        base.fail(f"{label} is missing frozen v8 predecessor")
    actual = _git_blob_sha1(view.read_bytes(V8_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V8_POLICY_GIT_BLOB_SHA1:
        base.fail(
            f"{label} v8 predecessor drifted: "
            f"expected={EXPECTED_V8_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_predecessor_identity() -> None:
    if _attr(v8, "_verify_extension_paths_v8", "v8 extension verifier") is not _EXPECTED_V8_EXTENSION_HELPER:
        base.fail("S1 routing v9 v8 extension verifier identity drifted")
    if (
        _attr(v8, "_require_predecessor_identity", "v8 predecessor identity verifier")
        is not _EXPECTED_V8_PREDECESSOR_IDENTITY
    ):
        base.fail("S1 routing v9 v8 predecessor identity verifier drifted")
    _call("v8 predecessor identity verifier", _EXPECTED_V8_PREDECESSOR_IDENTITY)


def _require_artifact(
    view: base.RepositoryView,
    path: str,
    sha256: str,
    git_blob: str,
    label: str,
) -> None:
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
        base.fail("S1-013 repaired measurement transition requires exact unreconciled S1 ledger")
    base_paths = _paths(policy_base)
    candidate_paths = _paths(candidate)
    for path, sha256, git_blob, label in (
        (
            PERFORMANCE_WORKFLOW,
            EXPECTED_PERFORMANCE_WORKFLOW_SHA256,
            EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1,
            "repaired S1-013 performance workflow",
        ),
        (
            PERFORMANCE_PROBE,
            EXPECTED_PERFORMANCE_PROBE_SHA256,
            EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1,
            "review-repaired S1-013 performance probe",
        ),
    ):
        if path in base_paths:
            base.fail(f"{label} already exists in trusted base")
        if path not in candidate_paths:
            base.fail(f"{label} is missing from candidate")
        _require_artifact(candidate, path, sha256, git_blob, label)


def _require_exact_delta_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)
    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_v8(candidate, "S1 routing v9 bootstrap candidate")
            _require_v8(policy_base, "S1 routing v9 trusted base")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 routing v9 bootstrap delta must be exactly "
                "the v9 policy plus Foundation and admission workflows"
            )

    if changed == PERFORMANCE_DELTA_PATHS:
        _require_exact_performance_transition(candidate, policy_base)
        return
    if changed & PERFORMANCE_DELTA_PATHS:
        base.fail(
            "S1-013 review-repaired measurement delta must be exactly "
            "the performance workflow and probe"
        )
    _call(
        "predecessor exact-delta verifier",
        _EXPECTED_V8_REQUIRE_EXACT_DELTA,
        candidate,
        policy_base,
    )


def _compare_base_controlled_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    if not _is_bootstrap_base(policy_base):
        _call(
            "predecessor base-controlled verifier",
            _EXPECTED_V8_COMPARE_BASE_CONTROLLED,
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
                    f"S1 routing v9 workflow candidate drifted: {relative}: "
                    f"expected={EXPECTED_WORKFLOW_SHA256[relative]} actual={actual_candidate}"
                )
            if actual_base != PRIOR_EXPECTED_WORKFLOW_SHA256[relative]:
                base.fail(
                    f"S1 routing v9 trusted-base workflow drifted: {relative}: "
                    f"expected={PRIOR_EXPECTED_WORKFLOW_SHA256[relative]} actual={actual_base}"
                )
            continue
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_v9(
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
            base.fail("S1 routing v9 policy wrapper is missing")
        if _is_bootstrap_base(policy_base):
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 routing v9 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 routing v9 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 routing v9 steady-state wrapper changed")

    delegated = frozenset(safe - {POLICY_SCRIPT})
    if delegated:
        _call(
            "pinned v8 extension verifier",
            _EXPECTED_V8_EXTENSION_HELPER,
            candidate,
            policy_base,
            delegated,
        )


def _verify_desktop_extension_paths_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v9(
        candidate,
        policy_base,
        _extension_paths(desktop, "desktop-extension"),
    )


def _verify_execution_extension_paths_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v9(
        candidate,
        policy_base,
        _extension_paths(execution, "execution-extension"),
    )


def _validate_allowed_paths_v9(paths: set[str], stage: str) -> None:
    projected = set(paths) - {POLICY_SCRIPT}
    _call(
        "predecessor tracked-path verifier",
        _EXPECTED_V8_VALIDATE_ALLOWED_PATHS,
        projected,
        stage,
    )


def _verify_policy_files_v9(view: base.RepositoryView) -> None:
    _require_v8(view, "S1 routing v9 policy verification")
    _require_predecessor_identity()
    _call("predecessor policy-file verifier", _EXPECTED_V8_VERIFY_POLICY_FILES, view)
    if POLICY_SCRIPT not in _paths(view):
        base.fail("S1 routing v9 policy wrapper is missing")
    if PERFORMANCE_WORKFLOW in _paths(view):
        _require_artifact(
            view,
            PERFORMANCE_WORKFLOW,
            EXPECTED_PERFORMANCE_WORKFLOW_SHA256,
            EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1,
            "repaired S1-013 performance workflow",
        )
    if PERFORMANCE_PROBE in _paths(view):
        _require_artifact(
            view,
            PERFORMANCE_PROBE,
            EXPECTED_PERFORMANCE_PROBE_SHA256,
            EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1,
            "review-repaired S1-013 performance probe",
        )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is not _EXPECTED_V8_PRINT_SUCCESS:
        base.fail("S1 routing v9 predecessor success-printer drifted")
    _call("predecessor success-printer", _PRIOR_PRINT_SUCCESS, stage, mode)
    print("s1_admission_steady_state_route_v9=V8_PRESERVED_PLUS_S1_013_PROBE_REVIEW_REPAIR")
    print(f"s1_admission_authority_expansion_v9={AUTHORITY_EXPANSION}")
    print(f"s1_013_existing_runtime_measurement_v9={EXISTING_RUNTIME_MEASUREMENT}")
    print(f"rejected_measurement_head_v9={REJECTED_MEASUREMENT_HEAD}")
    print(f"rejected_measurement_run_v9={REJECTED_MEASUREMENT_RUN}")
    print(f"rejected_measurement_class_v9={REJECTED_MEASUREMENT_CLASS}")
    print(f"review_finding_ids_v9={','.join(REVIEW_FINDING_IDS)}")
    print(f"effective_source_admission_v9={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission_v9={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution_v9={DONOR_EXECUTION}")
    print(f"new_product_runtime_authority_v9={NEW_PRODUCT_RUNTIME_AUTHORITY}")
    print(f"network_listener_authority_v9={NETWORK_LISTENER_AUTHORITY}")
    print(f"effective_model_provider_execution_v9={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access_v9={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference_v9={MODEL_INFERENCE}")
    print(f"s1_013_evidence_closeout_v9={S1_013_EVIDENCE_CLOSEOUT}")
    print(f"s1_014_plus_v9={S1_014_PLUS}")


def _require_overlay_identity_v9() -> None:
    _require_predecessor_identity()
    shell, retention, _, desktop, execution = _topology()
    expected = (
        (_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "overlay exact-delta"), _require_exact_delta_v9, "exact-delta"),
        (base.compare_base_controlled, _compare_base_controlled_v9, "base-control"),
        (_attr(desktop, "verify_extension_controlled_paths", "overlay desktop-extension"), _verify_desktop_extension_paths_v9, "desktop-extension"),
        (_attr(execution, "verify_extension_controlled_paths", "overlay execution-extension"), _verify_execution_extension_paths_v9, "execution-extension"),
        (_attr(shell, "validate_allowed_paths", "overlay tracked-path"), _validate_allowed_paths_v9, "tracked-path"),
        (_attr(shell, "verify_policy_files", "overlay policy-file"), _verify_policy_files_v9, "policy-file"),
        (_attr(shell, "print_success", "overlay success-printer"), _print_success, "success-printer"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 routing v9 overlay {label} hook drifted")
    if _PRIOR_PRINT_SUCCESS is not _EXPECTED_V8_PRINT_SUCCESS:
        base.fail("S1 routing v9 predecessor success-printer drifted")
    for component, label in ((desktop, "desktop"), (execution, "execution")):
        if POLICY_SCRIPT not in _extension_paths(component, f"{label}-extension"):
            base.fail(f"S1 routing v9 {label} extension registration drifted")


def _patch_v8_expected_identities() -> None:
    v8.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v8.EXPECTED_PERFORMANCE_WORKFLOW_SHA256 = EXPECTED_PERFORMANCE_WORKFLOW_SHA256
    v8.EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1 = EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1
    v8.EXPECTED_PERFORMANCE_PROBE_SHA256 = EXPECTED_PERFORMANCE_PROBE_SHA256
    v8.EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1 = EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity_v9()
        return

    _patch_v8_expected_identities()
    _call("predecessor policy install", v8._install_policy)

    _require_predecessor_identity()
    shell, retention, _, desktop, execution = _topology()
    predecessor = (
        (_attr(retention, "IMPL_REQUIRE_EXACT_DELTA", "predecessor exact-delta"), _EXPECTED_V8_REQUIRE_EXACT_DELTA, "exact-delta"),
        (base.compare_base_controlled, _EXPECTED_V8_COMPARE_BASE_CONTROLLED, "base-control"),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop-extension"), _EXPECTED_V8_DESKTOP_EXTENSION, "desktop-extension"),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution-extension"), _EXPECTED_V8_EXECUTION_EXTENSION, "execution-extension"),
        (_attr(shell, "validate_allowed_paths", "predecessor tracked-path"), _EXPECTED_V8_VALIDATE_ALLOWED_PATHS, "tracked-path"),
        (_attr(shell, "verify_policy_files", "predecessor policy-file"), _EXPECTED_V8_VERIFY_POLICY_FILES, "policy-file"),
        (_attr(shell, "print_success", "predecessor success-printer"), _EXPECTED_V8_PRINT_SUCCESS, "success-printer"),
    )
    for actual, wanted, label in predecessor:
        if actual is not wanted:
            base.fail(f"S1 routing v9 predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = _EXPECTED_V8_PRINT_SUCCESS
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(_extension_paths(desktop, "desktop-extension")) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(_extension_paths(execution, "execution-extension")) | {POLICY_SCRIPT}
    )
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v9
    base.compare_base_controlled = _compare_base_controlled_v9
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v9
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v9
    shell.validate_allowed_paths = _validate_allowed_paths_v9
    shell.verify_policy_files = _verify_policy_files_v9
    shell.print_success = _print_success
    _INSTALLED = True
    _require_overlay_identity_v9()


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
                f"S1 routing v9 workflow drifted: {path}: "
                f"expected={EXPECTED_WORKFLOW_SHA256[path]} actual={actual}"
            )


def _selftest_authority_and_bindings() -> None:
    if AUTHORITY_EXPANSION != "S1_013_PERFORMANCE_PROBE_REVIEW_REPAIR_ONLY":
        base.fail("S1 routing v9 authority boundary drifted")
    if EXISTING_RUNTIME_MEASUREMENT != "EXACT_ADMITTED_S1_GRAPH_ONLY":
        base.fail("S1 routing v9 runtime-measurement boundary drifted")
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
        base.fail("S1 routing v9 prohibited authority boundary drifted")
    if S1_013_EVIDENCE_CLOSEOUT != "NOT_AUTHORIZED_BY_V9" or S1_014_PLUS != "NOT_AUTHORIZED":
        base.fail("S1 routing v9 future-slice boundary drifted")
    if TRUSTED_BASE_V8_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":
        base.fail("S1 routing v9 old-base truth classification drifted")
    if REJECTED_MEASUREMENT_CLASS != (
        "EXACT_HEAD_MEASUREMENT_INVALIDATED_BY_THREE_MATERIAL_REVIEW_FINDINGS"
    ):
        base.fail("S1 routing v9 rejected-measurement classification drifted")
    if len(REVIEW_FINDING_IDS) != 3 or len(set(REVIEW_FINDING_IDS)) != 3:
        base.fail("S1 routing v9 review-finding identity set drifted")
    if EXPECTED_PERFORMANCE_PROBE_SHA256 == REJECTED_PERFORMANCE_PROBE_SHA256:
        base.fail("S1 routing v9 repaired probe SHA-256 did not change")
    if EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1 == REJECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1:
        base.fail("S1 routing v9 repaired probe Git blob did not change")
    for value, length, label in (
        (EXPECTED_PERFORMANCE_WORKFLOW_SHA256, 64, "performance workflow SHA-256"),
        (EXPECTED_PERFORMANCE_PROBE_SHA256, 64, "performance probe SHA-256"),
        (EXPECTED_PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1, 40, "performance workflow Git blob"),
        (EXPECTED_PERFORMANCE_PROBE_GIT_BLOB_SHA1, 40, "performance probe Git blob"),
    ):
        if len(value) != length or any(char not in "0123456789abcdef" for char in value):
            base.fail(f"S1 routing v9 {label} identity is malformed")
    _require_predecessor_identity()


def _selftest_bootstrap_contract() -> None:
    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    v8_bytes = local.read_bytes(V8_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        V8_POLICY_PATH: v8_bytes,
        FOUNDATION_WORKFLOW: b"old-foundation",
        ADMISSION_WORKFLOW: b"old-admission",
    }
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            POLICY_SCRIPT: b"policy-v9",
            FOUNDATION_WORKFLOW: b"new-foundation",
            ADMISSION_WORKFLOW: b"new-admission",
        }
    )
    _require_exact_delta_v9(_memory_view(candidate_files), _memory_view(base_files))
    mixed = dict(candidate_files)
    mixed["README.md"] = b"unexpected"
    base.expect_failure_matching(
        "S1 routing v9 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v9,
        _memory_view(mixed),
        _memory_view(base_files),
    )


def _selftest_identity_hardening() -> None:
    original = _attr(v8, "_verify_extension_paths_v8", "self-test v8 extension verifier")
    try:
        v8._verify_extension_paths_v8 = lambda *_args, **_kwargs: None
        base.expect_failure_matching(
            "S1 routing v9 predecessor late-lookup rejection",
            "v8 extension verifier identity drifted",
            _require_predecessor_identity,
        )
    finally:
        v8._verify_extension_paths_v8 = original
    _require_predecessor_identity()

    delattr(v8, "_verify_extension_paths_v8")
    try:
        base.expect_failure_matching(
            "S1 routing v9 missing predecessor verifier rejection",
            "v8 extension verifier topology/layout drifted",
            _require_predecessor_identity,
        )
    finally:
        setattr(v8, "_verify_extension_paths_v8", original)
    _require_predecessor_identity()


def _selftest_overlay_reentry() -> None:
    shell, _, _, _, _ = _topology()
    original = _attr(shell, "print_success", "self-test success-printer")
    try:
        shell.print_success = lambda *_args, **_kwargs: None
        base.expect_failure_matching(
            "S1 routing v9 post-install success-printer drift",
            "overlay success-printer hook drifted",
            _install_policy,
        )
    finally:
        shell.print_success = original
    _require_overlay_identity_v9()


def selftest() -> None:
    _patch_v8_expected_identities()
    v8.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_authority_and_bindings()
    _selftest_bootstrap_contract()
    _selftest_identity_hardening()
    _selftest_overlay_reentry()
    print("wepld S1 steady-state routing v9 policy self-tests: PASS")


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
