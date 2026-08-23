#!/usr/bin/env python3
"""Bounded authorization for the pinned Pictorial NOTICE provenance contract repair."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_pictorial_agile_contract_notice_provenance_repair_v6_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_contract_branding_boundary_repair_v5_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "61dd39245623e3c91644e9b2785e244e7ee6beb4"
FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
TARGET_PATH = "docs/acquisition/WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"
REJECTED_TARGET_GIT_BLOB_SHA1 = "60e17357f7026a1568b9607a85a25a5abcfe5e5d"
TARGET_GIT_BLOB_SHA1 = "05e58e331fa6a119227127cb146e135f5b9789b7"
PICTORIAL_NOTICE_FILE = "NOTICE.md"
PICTORIAL_NOTICE_GIT_BLOB_SHA1 = "0468271c904ae334cfaf27da6f8df3d5f419a1f0"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "e5f527231d516579f5b957d4fba857dc6f9a118bd52a3d58b48a399f26076685",
    ADMISSION_WORKFLOW: "cff1183a888771fee76fdde063af76b7c964eff488ac050baa35cd0ae841145f",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "940bb8b57c5eba27c9e3f2dde21e3728968a7783a52aa2e3ed7e8ad1f2c100c4",
    ADMISSION_WORKFLOW: "67e216ed07d47ea2cbbd2f6039869ae6617a9cfb8446d9916b4a4a9543ec0589",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
REPAIR_AUTHORIZATION = "EXACT_ONE_PICTORIAL_NOTICE_PROVENANCE_REPAIR"
REPAIR_FINDINGS = ("PICTORIAL_NOTICE_PROVENANCE_OMISSION",)

INHERITED_POLICY_AUTHORITY = "PRESERVED_UNCHANGED_NOT_NEW"
POLICY_RUNTIME_CLASS = "CI_EVIDENCE_POLICY_NOT_TRUSTED_CORE_RUNTIME"
SOURCE_IMPORT_AUTHORITY = "NONE"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_WORKFLOW_EXECUTION = "NONE"
PRODUCT_IMPLEMENTATION_AUTHORITY = "NONE"
ROADMAP_MUTATION = "NONE"
H0_014_PLUS = "NOT_STARTED"
H0_SCREEN_EXECUTION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"

_NOTICE_REPAIRS = (
    (
        b"PICTORIAL_LICENSE = Apache-2.0\n"
        b"PICTORIAL_LICENSE_BLOB = bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9\n",
        b"PICTORIAL_LICENSE = Apache-2.0\n"
        b"PICTORIAL_LICENSE_BLOB = bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9\n"
        b"PICTORIAL_NOTICE_FILE = NOTICE.md\n"
        b"PICTORIAL_NOTICE_BLOB = 0468271c904ae334cfaf27da6f8df3d5f419a1f0\n",
    ),
    (
        b"Pictorial's donor is Apache-2.0. Redistribution therefore must preserve the Apache-2.0 license, relevant copyright/patent/trademark/attribution notices, and modification notices required by the license. The current upstream `LICENSE` contains `Copyright 2025 Paul Bakaus`. No upstream `NOTICE` file was present at the pinned revision when checked.\n",
        b"Pictorial's donor is Apache-2.0. Redistribution therefore must preserve the Apache-2.0 license, relevant copyright/patent/trademark/attribution notices, and modification notices required by the license. The current upstream `LICENSE` contains `Copyright 2025 Paul Bakaus`. The exact pinned upstream root tree contains `NOTICE.md` at Git blob `0468271c904ae334cfaf27da6f8df3d5f419a1f0`. That notice records MIT-derived material in `skill/reference/ios.md` and `skill/reference/android.md` from `ehmo/platform-design-skills` (author `ehmo`). The notice and applicable attribution must remain preserved in WePLD legal/provenance handling; product-surface rebranding does not erase that provenance.\n",
    ),
    (
        b'  "upstream_license_blob": "bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9",\n'
        b'  "upstream_notice_file": null,\n',
        b'  "upstream_license_blob": "bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9",\n'
        b'  "upstream_notice_file": "NOTICE.md",\n'
        b'  "upstream_notice_blob": "0468271c904ae334cfaf27da6f8df3d5f419a1f0",\n',
    ),
    (
        b'  "upstream_license_blob": "28a50fa22639e32febe14e4ffc7a732b0ba8c90a",\n'
        b'  "upstream_notice_file": null,\n',
        b'  "upstream_license_blob": "28a50fa22639e32febe14e4ffc7a732b0ba8c90a",\n'
        b'  "upstream_notice_file": null,\n'
        b'  "upstream_notice_blob": null,\n',
    ),
)


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(files, trees={path: _git_blob_sha1(data) for path, data in files.items()})


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"Pictorial/Agile contract repair-v6 {label} topology is malformed: expected path set")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"Pictorial/Agile contract repair-v6 {label} topology is malformed: non-string path")
    return frozenset(value)


def _bind_prior_policy_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile repair-v5 policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_contract_branding_boundary_repair_v5_integrity as prior  # noqa: E402

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_repair
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_repair
PRIOR_VERIFY_EXTENSION_PATHS = prior._verify_extension_paths
_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        topology = prior._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 inherited topology is missing or malformed: {exc}")
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("Pictorial/Agile contract repair-v6 inherited topology is malformed: expected five components")
    return topology


def _activate_predecessor() -> None:
    try:
        if prior.TARGET_GIT_BLOB_SHA1 != REJECTED_TARGET_GIT_BLOB_SHA1:
            base.fail(
                "Pictorial/Agile contract repair-v6 predecessor target drifted: "
                f"expected={REJECTED_TARGET_GIT_BLOB_SHA1} actual={prior.TARGET_GIT_BLOB_SHA1}"
            )
        current_workflows = dict(prior.EXPECTED_WORKFLOW_SHA256)
        if current_workflows not in (
            dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
            dict(EXPECTED_WORKFLOW_SHA256),
        ):
            base.fail("Pictorial/Agile contract repair-v6 predecessor workflow hashes drifted")
        prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
        prior._install_policy()
        prior._require_overlay_identity()
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 predecessor activation is missing or malformed: {exc}")


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail("Pictorial/Agile contract repair-v6 requires the canonical repair-v5 predecessor policy")
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile contract repair-v6 base policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _authorized_target_bytes(rejected_bytes: bytes) -> bytes:
    actual_rejected = _git_blob_sha1(rejected_bytes)
    if actual_rejected != REJECTED_TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile contract repair-v6 rejected base blob drifted: "
            f"expected={REJECTED_TARGET_GIT_BLOB_SHA1} actual={actual_rejected}"
        )
    repaired = rejected_bytes
    for index, (old, new) in enumerate(_NOTICE_REPAIRS, start=1):
        count = repaired.count(old)
        if count != 1:
            base.fail(
                "Pictorial/Agile contract repair-v6 deterministic NOTICE transform is ambiguous: "
                f"replacement={index} count={count}"
            )
        repaired = repaired.replace(old, new, 1)
    actual_target = _git_blob_sha1(repaired)
    if actual_target != TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile contract repair-v6 deterministic target blob drifted: "
            f"expected={TARGET_GIT_BLOB_SHA1} actual={actual_target}"
        )
    return repaired


def _validate_repair_base(policy_base: base.RepositoryView) -> bytes:
    if TARGET_PATH not in _paths(policy_base):
        base.fail("Pictorial/Agile contract repair-v6 canonical target is missing from trusted base")
    rejected = policy_base.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)
    _authorized_target_bytes(rejected)
    return rejected


def _validate_target(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    if TARGET_PATH not in _paths(candidate):
        base.fail("Pictorial/Agile contract repair-v6 target is missing")
    rejected = _validate_repair_base(policy_base)
    expected = _authorized_target_bytes(rejected)
    actual = candidate.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)
    if actual == rejected:
        base.fail(f"Pictorial/Agile rejected contract blob remains present: {REJECTED_TARGET_GIT_BLOB_SHA1}")
    if actual != expected:
        base.fail(
            "Pictorial/Agile NOTICE-provenance repaired contract drifted: "
            f"expected={TARGET_GIT_BLOB_SHA1} actual={_git_blob_sha1(actual)}"
        )


def _delegate_exact_delta(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    try:
        delegated = prior._require_exact_delta_repair
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 inherited exact-delta topology is missing: {exc}")
    if delegated is not PRIOR_REQUIRE_EXACT_DELTA:
        base.fail("Pictorial/Agile contract repair-v6 inherited exact-delta delegate drifted")
    if not callable(delegated):
        base.fail("Pictorial/Agile contract repair-v6 inherited exact-delta delegate is not callable")
    try:
        delegated(candidate, policy_base)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 inherited exact-delta topology is malformed: {exc}")


def _require_exact_delta_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed_paths = impl._changed_paths
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 changed-path topology is missing: {exc}")
    if not callable(changed_paths):
        base.fail("Pictorial/Agile contract repair-v6 changed-path delegate is not callable")
    try:
        changed = _require_path_set(changed_paths(candidate, policy_base), "changed-path")
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 changed-path topology is malformed: {exc}")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            _validate_repair_base(policy_base)
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "Pictorial/Agile contract repair-v6 bootstrap delta must be exactly "
                "the repair policy plus two workflows"
            )
        if TARGET_PATH in changed:
            base.fail("Pictorial/Agile contract cannot transition during repair-v6 bootstrap")
        _delegate_exact_delta(candidate, policy_base)
        return

    if TARGET_PATH in changed:
        if changed != frozenset({TARGET_PATH}):
            base.fail("Pictorial/Agile NOTICE-provenance repair delta must be exactly one file")
        _validate_target(candidate, policy_base)
        return

    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    try:
        controlled_paths = _require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 base-control topology is missing: {exc}")

    for relative in sorted(controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            if _sha256(candidate_bytes) != expected_candidate:
                base.fail(f"Pictorial/Agile contract repair-v6 workflow candidate drifted: {relative}")
            expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            if _sha256(base_bytes) != expected_base:
                base.fail(f"Pictorial/Agile contract repair-v6 trusted-base workflow drifted: {relative}")
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"Pictorial/Agile contract repair-v6 steady-state workflow changed: {relative}")
            continue
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths(
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
            base.fail("Pictorial/Agile contract repair-v6 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Pictorial/Agile contract repair-v6 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Pictorial/Agile contract repair-v6 steady-state base lacks wrapper")
            if (
                candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
                != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
            ):
                base.fail("Pictorial/Agile contract repair-v6 steady-state wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & safe_controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if _sha256(candidate_bytes) != expected_candidate:
            base.fail(f"Pictorial/Agile contract repair-v6 controlled workflow candidate drifted: {relative}")
        expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
        if _sha256(base_bytes) != expected_base:
            base.fail(f"Pictorial/Agile contract repair-v6 controlled workflow base drifted: {relative}")
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"Pictorial/Agile contract repair-v6 controlled workflow changed: {relative}")

    delegated = frozenset(safe_controlled - {POLICY_SCRIPT} - BOOTSTRAP_WORKFLOWS)
    if delegated:
        try:
            verifier = prior._verify_extension_paths
        except AttributeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v6 inherited extension topology is missing: {exc}")
        if verifier is not PRIOR_VERIFY_EXTENSION_PATHS:
            base.fail("Pictorial/Agile contract repair-v6 inherited extension verifier drifted")
        if not callable(verifier):
            base.fail("Pictorial/Agile contract repair-v6 inherited extension verifier is not callable")
        try:
            verifier(candidate, policy_base, delegated)
        except TypeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v6 inherited extension topology is malformed: {exc}")


def _verify_execution_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, _, execution = _topology()
    try:
        controlled = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 execution extension topology is missing: {exc}")
    _verify_extension_paths(candidate, policy_base, _require_path_set(controlled, "execution-extension"))


def _verify_desktop_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, desktop, _ = _topology()
    try:
        controlled = desktop.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 desktop extension topology is missing: {exc}")
    _verify_extension_paths(candidate, policy_base, _require_path_set(controlled, "desktop-extension"))


def _validate_allowed_paths_repair(paths: set[str], stage: str) -> None:
    try:
        delegated = prior._validate_allowed_paths_repair
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 inherited allowlist topology is missing: {exc}")
    if delegated is not PRIOR_VALIDATE_ALLOWED_PATHS:
        base.fail("Pictorial/Agile contract repair-v6 inherited allowlist delegate drifted")
    if not callable(delegated):
        base.fail("Pictorial/Agile contract repair-v6 inherited allowlist delegate is not callable")
    try:
        delegated(paths, stage)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 inherited allowlist topology is malformed: {exc}")


def _verify_policy_files(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(f"frozen Pictorial/Agile repair-v5 predecessor policy drifted: {actual}")
    try:
        verifier = prior._verify_policy_files
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 inherited policy-file topology is missing: {exc}")
    if not callable(verifier):
        base.fail("Pictorial/Agile contract repair-v6 inherited policy-file verifier is not callable")
    try:
        verifier(view)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 inherited policy-file topology is malformed: {exc}")


def _require_prebind_identity(shell: Any, retention: Any, desktop: Any, execution: Any) -> None:
    try:
        expected = (
            (retention.IMPL_REQUIRE_EXACT_DELTA, prior._require_exact_delta_repair, "exact-delta"),
            (base.compare_base_controlled, prior._compare_base_controlled_repair, "base-control"),
            (desktop.verify_extension_controlled_paths, prior._verify_desktop_extension_paths, "desktop-extension"),
            (execution.verify_extension_controlled_paths, prior._verify_execution_extension_paths, "execution-extension"),
            (shell.validate_allowed_paths, prior._validate_allowed_paths_repair, "tracked-path"),
            (shell.verify_policy_files, prior._verify_policy_files, "policy-file"),
            (shell.print_success, prior._print_success, "success-printer"),
        )
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 pre-bind topology is missing: {exc}")

    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile contract repair-v6 pre-bind {label} hook drifted")


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    try:
        checks = (
            (retention.IMPL_REQUIRE_EXACT_DELTA, _require_exact_delta_repair, "exact-delta"),
            (base.compare_base_controlled, _compare_base_controlled_repair, "base-control"),
            (desktop.verify_extension_controlled_paths, _verify_desktop_extension_paths, "desktop-extension"),
            (execution.verify_extension_controlled_paths, _verify_execution_extension_paths, "execution-extension"),
            (shell.validate_allowed_paths, _validate_allowed_paths_repair, "tracked-path"),
            (shell.verify_policy_files, _verify_policy_files, "policy-file"),
            (shell.print_success, _print_success, "success-printer"),
        )
        hook_identity = retention._require_exact_delta_hook_identity
        retention_exact_delta = retention._require_exact_delta_retention
        desktop_paths = desktop.EXTENSION_CONTROLLED_PATHS
        execution_paths = execution.EXTENSION_CONTROLLED_PATHS
        prior_print_success = prior._print_success
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 overlay topology is missing: {exc}")

    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile contract repair-v6 {label} hook drifted")

    if not callable(hook_identity):
        base.fail("Pictorial/Agile contract repair-v6 hook identity is not callable")
    if not callable(retention_exact_delta):
        base.fail("Pictorial/Agile contract repair-v6 retention exact-delta is not callable")
    if not callable(prior_print_success):
        base.fail("Pictorial/Agile contract repair-v6 prior success-printer is not callable")

    safe_desktop_paths = _require_path_set(desktop_paths, "desktop-extension")
    safe_execution_paths = _require_path_set(execution_paths, "execution-extension")

    try:
        hook_identity(retention_exact_delta, "pictorial-agile-contract-notice-provenance-repair-v6-overlay")
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 overlay topology is malformed: {exc}")

    if POLICY_SCRIPT not in safe_desktop_paths:
        base.fail("Pictorial/Agile contract repair-v6 desktop path registration drifted")
    if POLICY_SCRIPT not in safe_execution_paths:
        base.fail("Pictorial/Agile contract repair-v6 execution path registration drifted")
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("Pictorial/Agile contract repair-v6 prior success-printer is missing or malformed")
    if _PRIOR_PRINT_SUCCESS is not prior_print_success:
        base.fail("Pictorial/Agile contract repair-v6 prior success-printer drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("prior Pictorial/Agile repair-v5 success printer is missing or malformed")
    try:
        _PRIOR_PRINT_SUCCESS(stage, mode)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 success-printer topology is malformed: {exc}")

    print(f"pictorial_agile_contract_notice_provenance_repair_v6_authorization={REPAIR_AUTHORIZATION}")
    print("pictorial_agile_contract_notice_provenance_repair_v6_findings=" + ",".join(REPAIR_FINDINGS))
    print(f"pictorial_agile_contract_notice_provenance_repair_v6_rejected_blob={REJECTED_TARGET_GIT_BLOB_SHA1}")
    print(f"pictorial_agile_contract_notice_provenance_repair_v6_target_blob={TARGET_GIT_BLOB_SHA1}")
    print(f"pictorial_notice_file={PICTORIAL_NOTICE_FILE}")
    print(f"pictorial_notice_blob={PICTORIAL_NOTICE_GIT_BLOB_SHA1}")
    print(f"inherited_policy_authority={INHERITED_POLICY_AUTHORITY}")
    print(f"policy_runtime_class={POLICY_RUNTIME_CLASS}")
    print(f"source_import_authority={SOURCE_IMPORT_AUTHORITY}")
    print(f"source_admission={SOURCE_ADMISSION}")
    print(f"dependency_admission={DEPENDENCY_ADMISSION}")
    print(f"donor_workflow_execution={DONOR_WORKFLOW_EXECUTION}")
    print(f"product_implementation_authority={PRODUCT_IMPLEMENTATION_AUTHORITY}")
    print(f"roadmap_mutation={ROADMAP_MUTATION}")
    print(f"h0_014_plus={H0_014_PLUS}")
    print(f"h0_screen_execution={H0_SCREEN_EXECUTION}")
    print(f"model_provider_execution={MODEL_PROVIDER_EXECUTION}")
    print(f"model_weight_access={MODEL_WEIGHT_ACCESS}")
    print(f"model_inference={MODEL_INFERENCE}")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity()
        return

    _activate_predecessor()
    shell, retention, _, desktop, execution = _topology()
    _require_prebind_identity(shell, retention, desktop, execution)

    try:
        desktop_paths = _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension")
        execution_paths = _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension")
        prior_print_success = prior._print_success
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 installation topology is missing: {exc}")
    if not callable(prior_print_success):
        base.fail("Pictorial/Agile contract repair-v6 predecessor success printer is not callable")

    _PRIOR_PRINT_SUCCESS = prior_print_success
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_repair
    base.compare_base_controlled = _compare_base_controlled_repair
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(desktop_paths | {POLICY_SCRIPT})
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(execution_paths | {POLICY_SCRIPT})
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths
    shell.validate_allowed_paths = _validate_allowed_paths_repair
    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success
    _INSTALLED = True
    _require_overlay_identity()


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != EXPECTED_WORKFLOW_SHA256[path]:
            base.fail(f"Pictorial/Agile contract repair-v6 workflow drifted: {path}")


def _selftest_target_transform() -> str:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    current = view.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)
    current_blob = _git_blob_sha1(current)
    if current_blob == REJECTED_TARGET_GIT_BLOB_SHA1:
        repaired = _authorized_target_bytes(current)
        if _git_blob_sha1(repaired) != TARGET_GIT_BLOB_SHA1:
            base.fail("Pictorial/Agile contract repair-v6 target transform hash drifted")
        return "PRE_REPAIR"
    if current_blob == TARGET_GIT_BLOB_SHA1:
        required = (
            b"PICTORIAL_NOTICE_FILE = NOTICE.md",
            b"PICTORIAL_NOTICE_BLOB = 0468271c904ae334cfaf27da6f8df3d5f419a1f0",
            b'"upstream_notice_file": "NOTICE.md"',
            b'"upstream_notice_blob": "0468271c904ae334cfaf27da6f8df3d5f419a1f0"',
            b'"upstream_notice_blob": null',
            b"ehmo/platform-design-skills",
        )
        for fragment in required:
            if fragment not in current:
                base.fail(f"Pictorial/Agile contract repair-v6 repaired target evidence missing: {fragment!r}")
        if b"No upstream `NOTICE` file was present at the pinned revision when checked." in current:
            base.fail("Pictorial/Agile contract repair-v6 false NOTICE absence statement remains")
        return "POST_REPAIR"
    base.fail(
        "Pictorial/Agile contract repair-v6 canonical target has an unrecognized blob: "
        f"actual={current_blob}"
    )


def _bootstrap_views() -> tuple[base.MemoryView, base.MemoryView]:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    prior_bytes = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    target_bytes = view.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        PRIOR_POLICY_PATH: prior_bytes,
        TARGET_PATH: target_bytes,
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


def _steady_target_views(
    base_target: bytes,
    candidate_target: bytes,
    *,
    extra: bool = False,
) -> tuple[base.MemoryView, base.MemoryView]:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    prior_bytes = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        PRIOR_POLICY_PATH: prior_bytes,
        POLICY_SCRIPT: policy_bytes,
        TARGET_PATH: base_target,
    }
    candidate_files = dict(base_files)
    candidate_files[TARGET_PATH] = candidate_target
    if extra:
        candidate_files["UNEXPECTED"] = b"x"
    return _memory_view(candidate_files), _memory_view(base_files)


def _selftest_deltas(target_state: str) -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    current = view.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)

    if target_state == "PRE_REPAIR":
        candidate, policy_base = _bootstrap_views()
        _require_exact_delta_repair(candidate, policy_base)

        mixed_files = {
            entry.path: candidate.read_bytes(entry.path, base.MAX_POLICY_FILE_BYTES)
            for entry in candidate.entries()
        }
        mixed_files[TARGET_PATH] = b"premature\n"
        base.expect_failure_matching(
            "contract repair-v6 mixed bootstrap rejection",
            "bootstrap delta must be exactly",
            _require_exact_delta_repair,
            _memory_view(mixed_files),
            policy_base,
        )

        repaired = _authorized_target_bytes(current)
        repaired_candidate, repaired_base = _steady_target_views(current, repaired)
        _require_exact_delta_repair(repaired_candidate, repaired_base)

        wrong_candidate, wrong_base = _steady_target_views(current, b"wrong-target\n")
        base.expect_failure_matching(
            "contract repair-v6 wrong target rejection",
            "NOTICE-provenance repaired contract drifted",
            _require_exact_delta_repair,
            wrong_candidate,
            wrong_base,
        )

        mixed_target, mixed_base = _steady_target_views(current, repaired, extra=True)
        base.expect_failure_matching(
            "contract repair-v6 mixed target rejection",
            "NOTICE-provenance repair delta must be exactly one file",
            _require_exact_delta_repair,
            mixed_target,
            mixed_base,
        )
        return

    if target_state == "POST_REPAIR":
        frozen_candidate, frozen_base = _steady_target_views(current, b"newer-target\n")
        base.expect_failure_matching(
            "contract repair-v6 post-repair refreeze",
            "rejected base blob drifted",
            _require_exact_delta_repair,
            frozen_candidate,
            frozen_base,
        )
        return

    base.fail(f"Pictorial/Agile contract repair-v6 unknown selftest target state: {target_state}")


def _selftest_identity_drift() -> None:
    original_prior_print_success = prior._print_success
    prior._print_success = lambda stage, mode: None
    try:
        base.expect_failure_matching(
            "contract repair-v6 rebound prior success printer",
            "prior success-printer drifted",
            _require_overlay_identity,
        )
    finally:
        prior._print_success = original_prior_print_success
    _require_overlay_identity()


def selftest() -> None:
    try:
        current_workflows = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 predecessor selftest binding is malformed: {exc}")
    if current_workflows not in (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    ):
        base.fail("Pictorial/Agile contract repair-v6 predecessor selftest workflow hashes drifted")
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    try:
        prior.selftest()
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v6 predecessor selftest topology is malformed: {exc}")

    _install_policy()
    _selftest_workflows()
    target_state = _selftest_target_transform()
    _selftest_deltas(target_state)
    _selftest_identity_drift()

    if REJECTED_TARGET_GIT_BLOB_SHA1 == TARGET_GIT_BLOB_SHA1:
        base.fail("Pictorial/Agile contract repair-v6 target did not change")
    if len(REPAIR_FINDINGS) != 1 or len(set(REPAIR_FINDINGS)) != 1:
        base.fail("Pictorial/Agile contract repair-v6 finding set must contain exactly one unique finding")
    if REPAIR_FINDINGS != ("PICTORIAL_NOTICE_PROVENANCE_OMISSION",):
        base.fail("Pictorial/Agile contract repair-v6 finding identity drifted")
    if PICTORIAL_NOTICE_FILE != "NOTICE.md":
        base.fail("Pictorial/Agile contract repair-v6 NOTICE path drifted")
    if PICTORIAL_NOTICE_GIT_BLOB_SHA1 != "0468271c904ae334cfaf27da6f8df3d5f419a1f0":
        base.fail("Pictorial/Agile contract repair-v6 NOTICE blob drifted")

    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail("canonical repository identity drifted")
    print(f"wepld Pictorial/Agile NOTICE provenance contract repair v6 self-tests: PASS state={target_state}")


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
                try:
                    runner = prior._verify_local_with_remote_policy_base
                except AttributeError as exc:
                    base.fail(f"Pictorial/Agile contract repair-v6 trusted-base local topology is missing: {exc}")
                if not callable(runner):
                    base.fail("Pictorial/Agile contract repair-v6 trusted-base local runner is not callable")
                return runner(args, shell, impl)

        try:
            runner = retention.main
        except AttributeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v6 runtime topology is missing: {exc}")
        if not callable(runner):
            base.fail("Pictorial/Agile contract repair-v6 runtime main is not callable")
        try:
            return runner(argv)
        except TypeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v6 runtime topology is malformed: {exc}")
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
