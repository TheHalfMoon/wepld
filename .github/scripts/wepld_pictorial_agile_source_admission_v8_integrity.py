#!/usr/bin/env python3
"""Post-merge activation repair for exact Pictorial + Agile source admission v7.

This successor fixes only the canonical push/local-runner dispatch defect exposed
by post-merge Foundation run 32693189380. It preserves v7's exact source-only
authority and keeps dependency, donor execution, product runtime, H0, and model
authority closed.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_pictorial_agile_source_admission_v8_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_source_admission_v7_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "fa9bf0fa6d35678206fc7b6f5c2e322a553d0205"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "0eadccff79f8cbd296230c353f3c0735d4c54a28a05689ba9bac99c1e2600491",
    ADMISSION_WORKFLOW: "5860ad868a62a63a97a29cf70b352c4e26c72a6ee81a3fbd4ce848253db7ecc5",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "9f4d321f4a5e8f37c3db31227157db61cf066e4acc4ea4513f12aae691f0067f",
    ADMISSION_WORKFLOW: "83c9e65e67d07fa0788d12d57937b37e18dec2249230575682d3ddd9132c675c",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
REPAIR_AUTHORIZATION = "EXACT_ONE_POST_MERGE_V7_LOCAL_RUNNER_TOPOLOGY_REPAIR"
REPAIR_FINDING = "POST_MERGE_V7_LOCAL_RUNNER_TOPOLOGY_DRIFT"

SOURCE_IMPORT_AUTHORITY = "EXACT_PINNED_PICTORIAL_AGILE_SOURCE_SNAPSHOT"
SOURCE_ADMISSION = "EXACT_SOURCE_ONLY"
DEPENDENCY_ADMISSION = "NONE"
DONOR_WORKFLOW_EXECUTION = "NONE"
DONOR_HOOK_EXECUTION = "NONE"
DONOR_INSTALL_SCRIPT_EXECUTION = "NONE"
PRODUCT_IMPLEMENTATION_AUTHORITY = "NONE"
PRODUCT_RUNTIME_ADMISSION = "NONE"
ROADMAP_MUTATION = "NONE"
H0_014_PLUS = "NOT_STARTED"
H0_SCREEN_EXECUTION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(
        files,
        trees={path: _git_blob_sha1(data) for path, data in files.items()},
    )


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(
            f"Pictorial/Agile source-admission-v8 {label} topology is malformed: "
            "expected path set"
        )
    if any(not isinstance(path, str) for path in value):
        base.fail(
            f"Pictorial/Agile source-admission-v8 {label} topology is malformed: "
            "non-string path"
        )
    return frozenset(value)


def _bind_prior_policy_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(
        view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    )
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile source-admission-v7 policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_source_admission_v7_integrity as prior  # noqa: E402

try:
    _v5_owner = prior.prior.prior
    V5_LOCAL_RUNNER = _v5_owner._verify_local_with_remote_policy_base
except (AttributeError, TypeError) as exc:
    base.fail(
        "Pictorial/Agile source-admission-v8 canonical v5 local-runner topology "
        f"is missing or malformed at import: {exc}"
    )

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_source
PRIOR_COMPARE_BASE_CONTROLLED = prior._compare_base_controlled_source
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_source
PRIOR_VERIFY_EXTENSION_PATHS = prior._verify_extension_paths
PRIOR_VERIFY_POLICY_FILES = prior._verify_policy_files
PRIOR_DESKTOP_VERIFY_EXTENSION_PATHS = prior._verify_desktop_extension_paths
PRIOR_EXECUTION_VERIFY_EXTENSION_PATHS = prior._verify_execution_extension_paths
PRIOR_VALIDATE_ENTRIES = prior._validate_entries_source
PRIOR_PRINT_SUCCESS = prior._print_success
PRIOR_SNAPSHOT_PRESENT = prior._snapshot_present
PRIOR_VERIFY_SNAPSHOT = prior._verify_snapshot
PRIOR_IS_SOURCE_PATH = prior._is_source_path


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        topology = prior._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited topology is missing "
            f"or malformed: {exc}"
        )
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited topology is malformed"
        )
    return topology


def _activate_predecessor() -> None:
    try:
        current = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 predecessor workflow topology "
            f"is malformed: {exc}"
        )
    if current not in (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    ):
        base.fail(
            "Pictorial/Agile source-admission-v8 predecessor workflow hashes drifted"
        )
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    try:
        prior._install_policy()
        prior._require_overlay_identity()
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 predecessor activation is "
            f"missing or malformed: {exc}"
        )


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail(
            "Pictorial/Agile source-admission-v8 requires canonical v7 predecessor"
        )
    actual = _git_blob_sha1(
        view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    )
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile source-admission-v8 base policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _delegate_exact_delta(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    try:
        delegated = prior._require_exact_delta_source
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited exact-delta topology "
            f"is missing or malformed: {exc}"
        )
    if delegated is not PRIOR_REQUIRE_EXACT_DELTA or not callable(delegated):
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited exact-delta delegate drifted"
        )
    try:
        delegated(candidate, policy_base)
    except TypeError as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited exact-delta topology "
            f"is malformed: {exc}"
        )


def _require_exact_delta_v8(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed = _require_path_set(
            impl._changed_paths(candidate, policy_base),
            "changed-path",
        )
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 changed-path topology is malformed: "
            f"{exc}"
        )

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            if prior._snapshot_present(candidate) and not prior._snapshot_present(policy_base):
                base.fail(
                    "Pictorial/Agile source snapshot cannot transition during "
                    "v8 activation-repair bootstrap"
                )
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "Pictorial/Agile source-admission-v8 bootstrap delta must be exactly "
                "the v8 policy plus two workflows"
            )
        if any(PRIOR_IS_SOURCE_PATH(path) for path in changed):
            base.fail(
                "Pictorial/Agile source snapshot cannot transition before "
                "v8 activation repair is canonical"
            )

    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_v8(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    try:
        controlled = _require_path_set(
            base.BASE_CONTROLLED_PATHS,
            "base-controlled-path",
        )
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 base-control topology is missing "
            f"or malformed: {exc}"
        )

    for relative in sorted(controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "Pictorial/Agile source-admission-v8 workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
                if bootstrap
                else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                base.fail(
                    "Pictorial/Agile source-admission-v8 trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "Pictorial/Agile source-admission-v8 steady-state workflow changed: "
                    f"{relative}"
                )
            continue
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    try:
        snapshot_present = prior._snapshot_present
        verify_snapshot = prior._verify_snapshot
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited snapshot topology is "
            f"missing or malformed: {exc}"
        )
    if snapshot_present is not PRIOR_SNAPSHOT_PRESENT:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited snapshot predicate drifted"
        )
    if verify_snapshot is not PRIOR_VERIFY_SNAPSHOT:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited snapshot verifier drifted"
        )

    base_has_snapshot = snapshot_present(policy_base)
    candidate_has_snapshot = snapshot_present(candidate)
    if base_has_snapshot:
        if not candidate_has_snapshot:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        verify_snapshot(policy_base, transition=False)
        verify_snapshot(candidate, transition=False)
    elif candidate_has_snapshot:
        if policy_base.tree_identity("docs/acquisition") != prior.BASE_ACQUISITION_TREE:
            base.fail("source-admission trusted-base acquisition identity drifted")
        verify_snapshot(candidate, transition=True)


def _verify_extension_paths_v8(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled: frozenset[str],
) -> None:
    safe_controlled = _require_path_set(controlled, "extension-controlled-path")
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in safe_controlled:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Pictorial/Agile source-admission-v8 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail(
                    "Pictorial/Agile source-admission-v8 wrapper unexpectedly exists "
                    "in bootstrap base"
                )
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail(
                    "Pictorial/Agile source-admission-v8 steady-state base lacks wrapper"
                )
            if (
                candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
                != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
            ):
                base.fail(
                    "Pictorial/Agile source-admission-v8 steady-state wrapper changed"
                )

    for relative in sorted(BOOTSTRAP_WORKFLOWS & safe_controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if _sha256(candidate_bytes) != EXPECTED_WORKFLOW_SHA256[relative]:
            base.fail(
                "Pictorial/Agile source-admission-v8 controlled workflow candidate "
                f"drifted: {relative}"
            )
        expected_base = (
            PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
            if bootstrap
            else EXPECTED_WORKFLOW_SHA256[relative]
        )
        if _sha256(base_bytes) != expected_base:
            base.fail(
                "Pictorial/Agile source-admission-v8 controlled workflow base "
                f"drifted: {relative}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(
                "Pictorial/Agile source-admission-v8 controlled workflow changed: "
                f"{relative}"
            )

    delegated = frozenset(
        safe_controlled - {POLICY_SCRIPT} - BOOTSTRAP_WORKFLOWS
    )
    if delegated:
        try:
            verifier = prior._verify_extension_paths
        except (AttributeError, TypeError) as exc:
            base.fail(
                "Pictorial/Agile source-admission-v8 inherited extension topology "
                f"is missing or malformed: {exc}"
            )
        if verifier is not PRIOR_VERIFY_EXTENSION_PATHS or not callable(verifier):
            base.fail(
                "Pictorial/Agile source-admission-v8 inherited extension verifier drifted"
            )
        try:
            verifier(candidate, policy_base, delegated)
        except TypeError as exc:
            base.fail(
                "Pictorial/Agile source-admission-v8 inherited extension topology "
                f"is malformed: {exc}"
            )


def _verify_desktop_extension_paths_v8(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    try:
        controlled = desktop.EXTENSION_CONTROLLED_PATHS
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 desktop extension topology is "
            f"missing or malformed: {exc}"
        )
    _verify_extension_paths_v8(
        candidate,
        policy_base,
        _require_path_set(controlled, "desktop-extension"),
    )


def _verify_execution_extension_paths_v8(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    try:
        controlled = execution.EXTENSION_CONTROLLED_PATHS
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 execution extension topology is "
            f"missing or malformed: {exc}"
        )
    _verify_extension_paths_v8(
        candidate,
        policy_base,
        _require_path_set(controlled, "execution-extension"),
    )


def _validate_allowed_paths_v8(paths: set[str], stage: str) -> None:
    projected = {path for path in paths if path != POLICY_SCRIPT}
    try:
        delegated = prior._validate_allowed_paths_source
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited allowlist topology is "
            f"missing or malformed: {exc}"
        )
    if delegated is not PRIOR_VALIDATE_ALLOWED_PATHS or not callable(delegated):
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited allowlist delegate drifted"
        )
    try:
        delegated(projected, stage)
    except TypeError as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited allowlist topology is "
            f"malformed: {exc}"
        )


def _verify_policy_files_v8(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(
        view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    )
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile source-admission-v7 predecessor policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    try:
        verifier = prior._verify_policy_files
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited policy-file topology is "
            f"missing or malformed: {exc}"
        )
    if verifier is not PRIOR_VERIFY_POLICY_FILES or not callable(verifier):
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited policy-file verifier drifted"
        )
    try:
        verifier(view)
    except TypeError as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 inherited policy-file topology is "
            f"malformed: {exc}"
        )


def _require_prebind_identity(
    shell: Any,
    retention: Any,
    desktop: Any,
    execution: Any,
) -> None:
    try:
        checks = (
            (retention.IMPL_REQUIRE_EXACT_DELTA, PRIOR_REQUIRE_EXACT_DELTA, "exact-delta"),
            (base.compare_base_controlled, PRIOR_COMPARE_BASE_CONTROLLED, "base-control"),
            (base.validate_entries, PRIOR_VALIDATE_ENTRIES, "tracked-mode"),
            (
                desktop.verify_extension_controlled_paths,
                PRIOR_DESKTOP_VERIFY_EXTENSION_PATHS,
                "desktop-extension",
            ),
            (
                execution.verify_extension_controlled_paths,
                PRIOR_EXECUTION_VERIFY_EXTENSION_PATHS,
                "execution-extension",
            ),
            (shell.validate_allowed_paths, PRIOR_VALIDATE_ALLOWED_PATHS, "tracked-path"),
            (shell.verify_policy_files, PRIOR_VERIFY_POLICY_FILES, "policy-file"),
            (shell.print_success, PRIOR_PRINT_SUCCESS, "success-printer"),
        )
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 pre-bind topology is missing or "
            f"malformed: {exc}"
        )
    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(
                f"Pictorial/Agile source-admission-v8 pre-bind {label} hook drifted"
            )


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    try:
        checks = (
            (retention.IMPL_REQUIRE_EXACT_DELTA, _require_exact_delta_v8, "exact-delta"),
            (base.compare_base_controlled, _compare_base_controlled_v8, "base-control"),
            (base.validate_entries, PRIOR_VALIDATE_ENTRIES, "tracked-mode"),
            (
                desktop.verify_extension_controlled_paths,
                _verify_desktop_extension_paths_v8,
                "desktop-extension",
            ),
            (
                execution.verify_extension_controlled_paths,
                _verify_execution_extension_paths_v8,
                "execution-extension",
            ),
            (shell.validate_allowed_paths, _validate_allowed_paths_v8, "tracked-path"),
            (shell.verify_policy_files, _verify_policy_files_v8, "policy-file"),
            (shell.print_success, _print_success, "success-printer"),
        )
        desktop_paths = _require_path_set(
            desktop.EXTENSION_CONTROLLED_PATHS,
            "desktop-extension",
        )
        execution_paths = _require_path_set(
            execution.EXTENSION_CONTROLLED_PATHS,
            "execution-extension",
        )
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 overlay topology is missing or "
            f"malformed: {exc}"
        )
    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile source-admission-v8 {label} hook drifted")
    if POLICY_SCRIPT not in desktop_paths or POLICY_SCRIPT not in execution_paths:
        base.fail(
            "Pictorial/Agile source-admission-v8 controlled-path registration drifted"
        )
    _trusted_local_runner()


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail(
            "Pictorial/Agile source-admission-v8 prior success printer is unavailable"
        )
    try:
        _PRIOR_PRINT_SUCCESS(stage, mode)
    except TypeError as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 success-printer topology is malformed: "
            f"{exc}"
        )
    print(f"pictorial_agile_source_admission_v8_repair={REPAIR_FINDING}")
    print(f"pictorial_agile_source_admission_v8_authority={SOURCE_IMPORT_AUTHORITY}")
    print(f"effective_source_admission={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_workflow_execution={DONOR_WORKFLOW_EXECUTION}")
    print(f"effective_donor_hook_execution={DONOR_HOOK_EXECUTION}")
    print(f"effective_donor_install_script_execution={DONOR_INSTALL_SCRIPT_EXECUTION}")
    print(f"effective_product_runtime_admission={PRODUCT_RUNTIME_ADMISSION}")
    print(f"effective_h0_014_plus={H0_014_PLUS}")
    print(f"effective_h0_screen_execution={H0_SCREEN_EXECUTION}")
    print(f"effective_model_provider_execution={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference={MODEL_INFERENCE}")


def _trusted_local_runner() -> Any:
    try:
        owner = prior.prior.prior
        live = owner._verify_local_with_remote_policy_base
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 canonical v5 local-runner topology "
            f"is missing or malformed: {exc}"
        )
    if live is not V5_LOCAL_RUNNER:
        base.fail(
            "Pictorial/Agile source-admission-v8 canonical v5 local runner drifted"
        )
    if not callable(live):
        base.fail(
            "Pictorial/Agile source-admission-v8 canonical v5 local runner is not callable"
        )
    return live


def _call_trusted_local_runner(
    args: Any,
    shell: Any,
    impl: Any,
    *,
    runner: Any | None = None,
) -> int:
    selected = _trusted_local_runner() if runner is None else runner
    if not callable(selected):
        base.fail(
            "Pictorial/Agile source-admission-v8 trusted local runner is not callable"
        )
    try:
        result = selected(args, shell, impl)
    except TypeError as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 trusted local runner topology is "
            f"malformed: {exc}"
        )
    if not isinstance(result, int):
        base.fail(
            "Pictorial/Agile source-admission-v8 trusted local runner returned "
            "non-integer status"
        )
    return result


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity()
        return

    _activate_predecessor()
    shell, retention, _, desktop, execution = _topology()
    _require_prebind_identity(shell, retention, desktop, execution)

    try:
        desktop_paths = _require_path_set(
            desktop.EXTENSION_CONTROLLED_PATHS,
            "desktop-extension",
        )
        execution_paths = _require_path_set(
            execution.EXTENSION_CONTROLLED_PATHS,
            "execution-extension",
        )
        prior_print_success = prior._print_success
    except (AttributeError, TypeError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 installation topology is missing "
            f"or malformed: {exc}"
        )
    if prior_print_success is not PRIOR_PRINT_SUCCESS or not callable(prior_print_success):
        base.fail(
            "Pictorial/Agile source-admission-v8 predecessor success printer drifted"
        )

    _PRIOR_PRINT_SUCCESS = prior_print_success
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v8
    base.compare_base_controlled = _compare_base_controlled_v8
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(desktop_paths | {POLICY_SCRIPT})
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(execution_paths | {POLICY_SCRIPT})
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v8
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v8
    shell.validate_allowed_paths = _validate_allowed_paths_v8
    shell.verify_policy_files = _verify_policy_files_v8
    shell.print_success = _print_success

    _INSTALLED = True
    _require_overlay_identity()


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                "Pictorial/Agile source-admission-v8 workflow drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _bootstrap_views() -> tuple[base.MemoryView, base.MemoryView]:
    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    base_files = {
        PRIOR_POLICY_PATH: local.read_bytes(
            PRIOR_POLICY_PATH,
            base.MAX_POLICY_FILE_BYTES,
        ),
        FOUNDATION_WORKFLOW: b"old-f",
        ADMISSION_WORKFLOW: b"old-a",
    }
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            POLICY_SCRIPT: b"policy",
            FOUNDATION_WORKFLOW: b"new-f",
            ADMISSION_WORKFLOW: b"new-a",
        }
    )
    return _memory_view(candidate_files), _memory_view(base_files)


def _selftest_bootstrap_delta() -> None:
    candidate, policy_base = _bootstrap_views()
    _require_exact_delta_v8(candidate, policy_base)

    mixed_files = {
        entry.path: candidate.read_bytes(entry.path, base.MAX_POLICY_FILE_BYTES)
        for entry in candidate.entries()
    }
    mixed_files["README.md"] = b"unexpected"
    base.expect_failure_matching(
        "source-admission-v8 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v8,
        _memory_view(mixed_files),
        policy_base,
    )


def _selftest_local_runner_binding() -> None:
    runner = _trusted_local_runner()

    sentinel_args = object()
    sentinel_shell = object()
    sentinel_impl = object()
    calls: list[tuple[Any, Any, Any]] = []

    def fake(args: Any, shell: Any, impl: Any) -> int:
        calls.append((args, shell, impl))
        return 0

    result = _call_trusted_local_runner(
        sentinel_args,
        sentinel_shell,
        sentinel_impl,
        runner=fake,
    )
    if result != 0 or calls != [(sentinel_args, sentinel_shell, sentinel_impl)]:
        base.fail(
            "Pictorial/Agile source-admission-v8 local-runner dispatch selftest drifted"
        )

    owner = prior.prior.prior
    original = owner._verify_local_with_remote_policy_base
    owner._verify_local_with_remote_policy_base = lambda *args, **kwargs: 0
    try:
        base.expect_failure_matching(
            "source-admission-v8 rebound canonical v5 local runner",
            "canonical v5 local runner drifted",
            _trusted_local_runner,
        )
    finally:
        owner._verify_local_with_remote_policy_base = original
    if _trusted_local_runner() is not runner:
        base.fail(
            "Pictorial/Agile source-admission-v8 local runner did not restore exactly"
        )


def _selftest_activation_dispatch_source() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    forbidden = "runner = prior._verify_local_with_remote_policy_base"
    if forbidden in source:
        base.fail(
            "Pictorial/Agile source-admission-v8 reintroduced the v7 broken "
            "direct-v6 local-runner lookup"
        )
    required = "_call_trusted_local_runner(args, shell, impl)"
    if required not in source:
        base.fail(
            "Pictorial/Agile source-admission-v8 executable local-runner dispatch "
            "is missing"
        )
    expected_tail = (
        'if __name__ == "__main__":\n'
        '    raise SystemExit(main(sys.argv[1:]))'
    )
    if not source.rstrip().endswith(expected_tail):
        base.fail(
            "Pictorial/Agile source-admission-v8 executable entrypoint is missing "
            "or malformed"
        )


def _selftest_authority() -> None:
    expected = (
        SOURCE_IMPORT_AUTHORITY,
        SOURCE_ADMISSION,
        DEPENDENCY_ADMISSION,
        DONOR_WORKFLOW_EXECUTION,
        DONOR_HOOK_EXECUTION,
        DONOR_INSTALL_SCRIPT_EXECUTION,
        PRODUCT_RUNTIME_ADMISSION,
        H0_014_PLUS,
        H0_SCREEN_EXECUTION,
        MODEL_PROVIDER_EXECUTION,
        MODEL_WEIGHT_ACCESS,
        MODEL_INFERENCE,
    )
    wanted = (
        "EXACT_PINNED_PICTORIAL_AGILE_SOURCE_SNAPSHOT",
        "EXACT_SOURCE_ONLY",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NOT_STARTED",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
    )
    if expected != wanted:
        base.fail(
            "Pictorial/Agile source-admission-v8 authority boundary drifted"
        )
    inherited = (
        prior.SOURCE_IMPORT_AUTHORITY,
        prior.SOURCE_ADMISSION,
        prior.DEPENDENCY_ADMISSION,
        prior.DONOR_WORKFLOW_EXECUTION,
        prior.DONOR_HOOK_EXECUTION,
        prior.DONOR_INSTALL_SCRIPT_EXECUTION,
        prior.PRODUCT_RUNTIME_ADMISSION,
        prior.H0_014_PLUS,
        prior.H0_SCREEN_EXECUTION,
        prior.MODEL_PROVIDER_EXECUTION,
        prior.MODEL_WEIGHT_ACCESS,
        prior.MODEL_INFERENCE,
    )
    if inherited != wanted:
        base.fail(
            "Pictorial/Agile source-admission-v8 predecessor authority drifted"
        )


def selftest() -> None:
    try:
        current = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(
            "Pictorial/Agile source-admission-v8 predecessor selftest workflow "
            f"binding is malformed: {exc}"
        )
    if current not in (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    ):
        base.fail(
            "Pictorial/Agile source-admission-v8 predecessor selftest workflow "
            "hashes drifted"
        )
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior.selftest()

    _selftest_bootstrap_delta()
    _selftest_local_runner_binding()
    _selftest_activation_dispatch_source()
    _selftest_authority()

    _install_policy()
    _selftest_workflows()
    _require_overlay_identity()

    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    _require_prior_policy_base(local)
    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail("canonical repository identity drifted")
    print("wepld Pictorial/Agile source admission v8 activation-repair self-tests: PASS")


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0

        _install_policy()
        shell, retention, impl, _, _ = _topology()

        if argv and argv[0] == "verify-local":
            args = base.parse_args(argv)
            if args.remote_baseline:
                return _call_trusted_local_runner(args, shell, impl)

        try:
            runner = retention.main
        except (AttributeError, TypeError) as exc:
            base.fail(
                "Pictorial/Agile source-admission-v8 runtime main topology is "
                f"missing or malformed: {exc}"
            )
        if not callable(runner):
            base.fail(
                "Pictorial/Agile source-admission-v8 runtime main is not callable"
            )
        try:
            return runner(argv)
        except TypeError as exc:
            base.fail(
                "Pictorial/Agile source-admission-v8 runtime main topology is "
                f"malformed: {exc}"
            )
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
