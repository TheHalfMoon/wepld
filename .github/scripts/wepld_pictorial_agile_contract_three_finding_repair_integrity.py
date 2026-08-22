#!/usr/bin/env python3
"""Authorize one exact three-finding repair of the Pictorial + Agile contract.

This module is repository CI/evidence-policy machinery, not product Trusted
Core runtime. It layers over the canonically activated Pictorial/Agile import-
contract authorization and adds only:

1. this policy/workflow bootstrap; and
2. one exact content-addressed repair that closes the three material findings
   from the exact-head CodeRabbit review of PR #96.

The repair does not admit donor source bytes, dependencies, donor workflows,
product runtime behavior, H0-SCREEN execution, H0-014+, or model/provider
execution. Inherited predecessor authority is preserved unchanged and is not
new authority granted by this wrapper.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = (
    ".github/scripts/"
    "wepld_pictorial_agile_contract_three_finding_repair_integrity.py"
)
PRIOR_POLICY_PATH = (
    ".github/scripts/"
    "wepld_pictorial_agile_full_import_authorization_integrity.py"
)
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "6df23c3c48faf5560e36698aa5344d012a050293"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

TARGET_PATH = (
    "docs/acquisition/"
    "WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"
)
REJECTED_TARGET_GIT_BLOB_SHA1 = "3ede8efbd32c00bd0623924879a645964bd622ee"
TARGET_GIT_BLOB_SHA1 = "f3aedc464392d666ec55ae01d717207307c4c582"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "4fa977235329c1b05d7a0899c2dec994789c2263f49ffdfae6f588483d75a008",
    ADMISSION_WORKFLOW: "fc7cddfdd874acb86bca4da06e70644a181a2a6b8d02574d69ea4fdf9b6f5791",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "c9660932f3b0204f2f30d434a08b516b1caf90f58b5d453391d6e9aa3a44ad78",
    ADMISSION_WORKFLOW: "2e7743132294d8cd6d5108e58a2b198b23e99b0cfb91dadad66b0b4c34be8eb5",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

PICTORIAL_AGILE_CONTRACT_REPAIR_AUTHORIZATION = "EXACT_THREE_REVIEW_FINDING_REPAIR"
REPAIR_FINDINGS = (
    "PROVENANCE_SCHEMA_CONSISTENCY",
    "FAIL_CLOSED_RECURSIVE_TREE_EXACT_SET_ACCOUNTING",
    "SPECIFY_UNDERSCORE_BRANDING_GATE_COVERAGE",
)
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


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    trees = {relative: _git_blob_sha1(data) for relative, data in files.items()}
    return base.MemoryView(files, trees=trees)


def _bind_prior_policy_before_import() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile authorization policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_full_import_authorization_integrity as prior  # noqa: E402

try:
    PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_pictorial_agile
    PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_pictorial_agile
except AttributeError as exc:
    base.fail(
        "Pictorial/Agile repair predecessor API is missing or stale before bind: "
        f"{exc}"
    )

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        return prior._topology()
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair inherited topology is missing or stale: "
            f"{exc}"
        )


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(policy_base)


def _activate_contract() -> None:
    """Retarget only the exact contract blob and workflow identities."""
    try:
        existing_target = prior.TARGET_GIT_BLOB_SHA1
        existing_workflows = prior.EXPECTED_WORKFLOW_SHA256
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair activation topology is missing or stale: "
            f"{exc}"
        )
    if existing_target not in {
        REJECTED_TARGET_GIT_BLOB_SHA1,
        TARGET_GIT_BLOB_SHA1,
    }:
        base.fail(
            "Pictorial/Agile repair predecessor target drifted before activation: "
            f"expected_one_of={REJECTED_TARGET_GIT_BLOB_SHA1},{TARGET_GIT_BLOB_SHA1} "
            f"actual={existing_target}"
        )
    if not isinstance(existing_workflows, dict):
        base.fail(
            "Pictorial/Agile repair predecessor workflow topology is malformed"
        )
    allowed_workflows = (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    )
    if dict(existing_workflows) not in allowed_workflows:
        base.fail("Pictorial/Agile repair predecessor workflow hashes drifted")

    prior.TARGET_GIT_BLOB_SHA1 = TARGET_GIT_BLOB_SHA1
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    try:
        prior._activate_contract()
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair predecessor activation hook is missing: "
            f"{exc}"
        )


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail(
            "Pictorial/Agile three-finding repair requires the canonical "
            "Pictorial/Agile authorization policy"
        )
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile repair base policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _validate_target_candidate(candidate: base.RepositoryView) -> None:
    data = candidate.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual == REJECTED_TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile rejected contract blob remains present: "
            f"{REJECTED_TARGET_GIT_BLOB_SHA1}"
        )
    if actual != TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile repaired contract drifted: "
            f"{TARGET_PATH}: expected={TARGET_GIT_BLOB_SHA1} actual={actual}"
        )


def _delegate_inherited_exact_delta(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    try:
        expected = prior._require_exact_delta_pictorial_agile
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair inherited exact-delta topology is missing: "
            f"{exc}"
        )
    if PRIOR_REQUIRE_EXACT_DELTA is not expected:
        base.fail("Pictorial/Agile repair inherited exact-delta delegate drifted")
    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _require_exact_delta_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed = impl._changed_paths(candidate, policy_base)
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair inherited change detector is missing: "
            f"{exc}"
        )

    bootstrap = _is_bootstrap_base(policy_base)
    base_paths = _paths(policy_base)

    if bootstrap:
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            _require_prior_policy_base(policy_base)
            return
        if changed & set(BOOTSTRAP_DELTA_PATHS):
            missing = sorted(set(BOOTSTRAP_DELTA_PATHS) - changed)
            unexpected = sorted(changed - set(BOOTSTRAP_DELTA_PATHS))
            detail: list[str] = []
            if missing:
                detail.append("missing=" + ",".join(missing))
            if unexpected:
                detail.append("unexpected=" + ",".join(unexpected))
            base.fail(
                "Pictorial/Agile repair bootstrap delta must be exactly the "
                "repair wrapper plus two workflows: "
                + ("; ".join(detail) if detail else "delta mismatch")
            )
        if TARGET_PATH in changed:
            base.fail(
                "Pictorial/Agile repaired contract cannot transition before "
                "three-finding repair policy activation"
            )
        _delegate_inherited_exact_delta(candidate, policy_base)
        return

    if TARGET_PATH in changed:
        if TARGET_PATH in base_paths:
            base.fail(
                "Pictorial/Agile repaired contract is frozen after canonicalization"
            )
        if changed != {TARGET_PATH}:
            unexpected = sorted(changed - {TARGET_PATH})
            base.fail(
                "Pictorial/Agile repaired contract delta must be exactly one file"
                + (": unexpected=" + ",".join(unexpected) if unexpected else "")
            )
        _validate_target_candidate(candidate)
        return

    _delegate_inherited_exact_delta(candidate, policy_base)


def _compare_base_controlled_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "Pictorial/Agile repair workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} "
                    f"actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
                if bootstrap
                else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    "Pictorial/Agile repair "
                    f"{phase} trusted-base workflow drifted: {relative}: "
                    f"expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "Pictorial/Agile repair steady-state workflow changed: "
                    f"{relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Pictorial/Agile repair policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Pictorial/Agile repair wrapper unexpectedly exists in base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Pictorial/Agile repair steady-state base lacks wrapper")
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("Pictorial/Agile repair steady-state wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        actual_candidate = _sha256(candidate_bytes)
        if actual_candidate != expected_candidate:
            base.fail(
                "Pictorial/Agile repair controlled workflow candidate drifted: "
                f"{relative}: expected={expected_candidate} actual={actual_candidate}"
            )
        expected_base = (
            PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
            if bootstrap
            else expected_candidate
        )
        actual_base = _sha256(base_bytes)
        if actual_base != expected_base:
            phase = "bootstrap" if bootstrap else "steady-state"
            base.fail(
                "Pictorial/Agile repair controlled workflow "
                f"{phase} base drifted: {relative}: "
                f"expected={expected_base} actual={actual_base}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(
                "Pictorial/Agile repair steady-state workflow changed: "
                f"{relative}"
            )

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        try:
            prior._verify_extension_paths_pictorial_agile(
                candidate,
                policy_base,
                delegated,
            )
        except AttributeError as exc:
            base.fail(
                "Pictorial/Agile repair inherited extension topology is missing: "
                f"{exc}"
            )


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    try:
        controlled = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair execution extension topology is missing: "
            f"{exc}"
        )
    _verify_extension_paths_repair(candidate, policy_base, controlled)


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    try:
        controlled = desktop.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair desktop extension topology is missing: "
            f"{exc}"
        )
    _verify_extension_paths_repair(candidate, policy_base, controlled)


def _validate_allowed_paths_repair(paths: set[str], stage: str) -> None:
    delegated = set(paths)
    delegated.discard(TARGET_PATH)
    if PRIOR_VALIDATE_ALLOWED_PATHS is not prior._validate_allowed_paths_pictorial_agile:
        base.fail("Pictorial/Agile repair inherited allowlist delegate drifted")
    PRIOR_VALIDATE_ALLOWED_PATHS(delegated, stage)


def _verify_policy_files(view: base.RepositoryView) -> None:
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile authorization policy drifted in view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    try:
        prior._verify_policy_files(view)
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair inherited policy-file topology is missing: "
            f"{exc}"
        )


def _require_prebind_identity(
    shell: Any,
    retention: Any,
    desktop: Any,
    execution: Any,
) -> None:
    try:
        expected = (
            (
                retention.IMPL_REQUIRE_EXACT_DELTA,
                prior._require_exact_delta_pictorial_agile,
                "exact-delta",
            ),
            (
                base.compare_base_controlled,
                prior._compare_base_controlled_pictorial_agile,
                "base-control",
            ),
            (
                desktop.verify_extension_controlled_paths,
                prior._verify_desktop_extension_paths,
                "desktop-extension",
            ),
            (
                execution.verify_extension_controlled_paths,
                prior._verify_execution_extension_paths,
                "execution-extension",
            ),
            (
                shell.validate_allowed_paths,
                prior._validate_allowed_paths_pictorial_agile,
                "tracked-path",
            ),
            (shell.verify_policy_files, prior._verify_policy_files, "policy-file"),
            (shell.print_success, prior._print_success, "success-printer"),
        )
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair pre-bind topology is missing or stale: "
            f"{exc}"
        )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile repair pre-bind {label} hook drifted")


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    try:
        if retention.IMPL_REQUIRE_EXACT_DELTA is not _require_exact_delta_repair:
            base.fail("Pictorial/Agile repair exact-delta delegate drifted")
        retention._require_exact_delta_hook_identity(
            retention._require_exact_delta_retention,
            "pictorial-agile-contract-three-finding-repair-overlay",
        )
        if base.compare_base_controlled is not _compare_base_controlled_repair:
            base.fail("Pictorial/Agile repair base-control hook drifted")
        if desktop.verify_extension_controlled_paths is not _verify_desktop_extension_paths:
            base.fail("Pictorial/Agile repair desktop extension hook drifted")
        if execution.verify_extension_controlled_paths is not _verify_execution_extension_paths:
            base.fail("Pictorial/Agile repair execution extension hook drifted")
        if shell.validate_allowed_paths is not _validate_allowed_paths_repair:
            base.fail("Pictorial/Agile repair tracked-path hook drifted")
        if shell.verify_policy_files is not _verify_policy_files:
            base.fail("Pictorial/Agile repair policy-file hook drifted")
        if shell.print_success is not _print_success:
            base.fail("Pictorial/Agile repair success-printer hook drifted")
        if POLICY_SCRIPT not in desktop.EXTENSION_CONTROLLED_PATHS:
            base.fail("Pictorial/Agile repair desktop path registration drifted")
        if POLICY_SCRIPT not in execution.EXTENSION_CONTROLLED_PATHS:
            base.fail("Pictorial/Agile repair execution path registration drifted")
        if _PRIOR_PRINT_SUCCESS is None or _PRIOR_PRINT_SUCCESS is not prior._print_success:
            base.fail("Pictorial/Agile repair prior success-printer drifted")
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair overlay topology is missing or stale: "
            f"{exc}"
        )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior Pictorial/Agile success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(
        "pictorial_agile_contract_review_repair_authorization="
        f"{PICTORIAL_AGILE_CONTRACT_REPAIR_AUTHORIZATION}"
    )
    print(
        "pictorial_agile_contract_review_repair_rejected_blob="
        f"{REJECTED_TARGET_GIT_BLOB_SHA1}"
    )
    print(
        "pictorial_agile_contract_review_repair_target_blob="
        f"{TARGET_GIT_BLOB_SHA1}"
    )
    print("pictorial_agile_contract_review_repair_findings=" + ",".join(REPAIR_FINDINGS))
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

    _activate_contract()
    try:
        prior._install_policy()
        prior._require_overlay_identity()
        shell, retention, _, desktop, execution = _topology()
        _require_prebind_identity(shell, retention, desktop, execution)
        desktop_paths = desktop.EXTENSION_CONTROLLED_PATHS
        execution_paths = execution.EXTENSION_CONTROLLED_PATHS
        predecessor_printer = prior._print_success
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair installer topology is missing or stale: "
            f"{exc}"
        )
    if not callable(predecessor_printer):
        base.fail("prior Pictorial/Agile success printer is unavailable")

    _PRIOR_PRINT_SUCCESS = predecessor_printer
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_repair
    base.compare_base_controlled = _compare_base_controlled_repair
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(desktop_paths) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(execution_paths) | {POLICY_SCRIPT}
    )
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths
    shell.validate_allowed_paths = _validate_allowed_paths_repair
    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success

    _INSTALLED = True
    _require_overlay_identity()


def _selftest_workflow_binding() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for relative in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "Pictorial/Agile repair workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_bootstrap_delta() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    prior_bytes = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        PRIOR_POLICY_PATH: prior_bytes,
        FOUNDATION_WORKFLOW: b"prior-foundation",
        ADMISSION_WORKFLOW: b"prior-admission",
    }
    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"repair-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"repair-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"repair-admission"
    _require_exact_delta_repair(
        _memory_view(candidate_files),
        _memory_view(base_files),
    )

    mixed = dict(candidate_files)
    mixed[TARGET_PATH] = b"not-authorized-during-bootstrap\n"
    base.expect_failure_matching(
        "Pictorial/Agile repair mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_repair,
        _memory_view(mixed),
        _memory_view(base_files),
    )


def _selftest_target_transition() -> None:
    global TARGET_GIT_BLOB_SHA1, REJECTED_TARGET_GIT_BLOB_SHA1
    target = b"exact-three-finding-repair-fixture\n"
    rejected = b"rejected-three-finding-contract-fixture\n"
    original_target = TARGET_GIT_BLOB_SHA1
    original_rejected = REJECTED_TARGET_GIT_BLOB_SHA1
    TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(target)
    REJECTED_TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(rejected)
    try:
        base_files = {
            PRIOR_POLICY_PATH: b"canonical-prior-policy",
            POLICY_SCRIPT: b"canonical-repair-policy",
        }
        candidate_files = dict(base_files)
        candidate_files[TARGET_PATH] = target
        _require_exact_delta_repair(
            _memory_view(candidate_files),
            _memory_view(base_files),
        )

        old = dict(base_files)
        old[TARGET_PATH] = rejected
        base.expect_failure_matching(
            "Pictorial/Agile rejected blob rejection",
            "rejected contract blob remains present",
            _require_exact_delta_repair,
            _memory_view(old),
            _memory_view(base_files),
        )

        wrong = dict(base_files)
        wrong[TARGET_PATH] = b"wrong\n"
        base.expect_failure_matching(
            "Pictorial/Agile wrong repaired blob rejection",
            "repaired contract drifted",
            _require_exact_delta_repair,
            _memory_view(wrong),
            _memory_view(base_files),
        )

        extra = dict(candidate_files)
        extra["docs/acquisition/UNAUTHORIZED_REPAIR_EXTRA.md"] = b"extra\n"
        base.expect_failure_matching(
            "Pictorial/Agile repaired extra path rejection",
            "delta must be exactly one file",
            _require_exact_delta_repair,
            _memory_view(extra),
            _memory_view(base_files),
        )

        frozen_base = dict(candidate_files)
        frozen_candidate = dict(frozen_base)
        frozen_candidate[TARGET_PATH] = target + b"drift\n"
        base.expect_failure_matching(
            "Pictorial/Agile repaired post-canonical mutation rejection",
            "frozen after canonicalization",
            _require_exact_delta_repair,
            _memory_view(frozen_candidate),
            _memory_view(frozen_base),
        )
    finally:
        TARGET_GIT_BLOB_SHA1 = original_target
        REJECTED_TARGET_GIT_BLOB_SHA1 = original_rejected


def _selftest_allowlist_projection() -> None:
    global PRIOR_VALIDATE_ALLOWED_PATHS
    original = PRIOR_VALIDATE_ALLOWED_PATHS
    seen: list[tuple[set[str], str]] = []

    def capture(paths: set[str], stage: str) -> None:
        seen.append((set(paths), stage))

    PRIOR_VALIDATE_ALLOWED_PATHS = capture
    try:
        _validate_allowed_paths_repair(
            {"README.md", TARGET_PATH},
            "fixture-stage",
        )
        if seen != [({"README.md"}, "fixture-stage")]:
            base.fail(
                "Pictorial/Agile repair allowlist projection drifted: "
                f"{seen}"
            )
    finally:
        PRIOR_VALIDATE_ALLOWED_PATHS = original


def _selftest_overlay_identity() -> None:
    global _PRIOR_PRINT_SUCCESS
    _require_overlay_identity()
    shell, retention, _, desktop, execution = _topology()

    hook_cases = (
        (retention, "IMPL_REQUIRE_EXACT_DELTA", PRIOR_REQUIRE_EXACT_DELTA, "exact-delta delegate drifted"),
        (base, "compare_base_controlled", prior._compare_base_controlled_pictorial_agile, "base-control hook drifted"),
        (desktop, "verify_extension_controlled_paths", prior._verify_desktop_extension_paths, "desktop extension hook drifted"),
        (execution, "verify_extension_controlled_paths", prior._verify_execution_extension_paths, "execution extension hook drifted"),
        (shell, "validate_allowed_paths", PRIOR_VALIDATE_ALLOWED_PATHS, "tracked-path hook drifted"),
        (shell, "verify_policy_files", prior._verify_policy_files, "policy-file hook drifted"),
        (shell, "print_success", prior._print_success, "success-printer hook drifted"),
    )
    for owner, attribute, replacement, expected_message in hook_cases:
        installed = getattr(owner, attribute)
        setattr(owner, attribute, replacement)
        try:
            base.expect_failure_matching(
                f"Pictorial/Agile repair overlay {attribute} tamper",
                expected_message,
                _require_overlay_identity,
            )
        finally:
            setattr(owner, attribute, installed)

    desktop_paths = desktop.EXTENSION_CONTROLLED_PATHS
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(desktop_paths) - {POLICY_SCRIPT}
    )
    try:
        base.expect_failure_matching(
            "Pictorial/Agile repair desktop registration tamper",
            "desktop path registration drifted",
            _require_overlay_identity,
        )
    finally:
        desktop.EXTENSION_CONTROLLED_PATHS = desktop_paths

    execution_paths = execution.EXTENSION_CONTROLLED_PATHS
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(execution_paths) - {POLICY_SCRIPT}
    )
    try:
        base.expect_failure_matching(
            "Pictorial/Agile repair execution registration tamper",
            "execution path registration drifted",
            _require_overlay_identity,
        )
    finally:
        execution.EXTENSION_CONTROLLED_PATHS = execution_paths

    printer = _PRIOR_PRINT_SUCCESS
    _PRIOR_PRINT_SUCCESS = None
    try:
        base.expect_failure_matching(
            "Pictorial/Agile repair prior printer tamper",
            "prior success-printer drifted",
            _require_overlay_identity,
        )
    finally:
        _PRIOR_PRINT_SUCCESS = printer

    _require_overlay_identity()


def _selftest_prebind_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    installed = (
        retention.IMPL_REQUIRE_EXACT_DELTA,
        base.compare_base_controlled,
        desktop.verify_extension_controlled_paths,
        execution.verify_extension_controlled_paths,
        shell.validate_allowed_paths,
        shell.verify_policy_files,
        shell.print_success,
    )
    predecessor = (
        prior._require_exact_delta_pictorial_agile,
        prior._compare_base_controlled_pictorial_agile,
        prior._verify_desktop_extension_paths,
        prior._verify_execution_extension_paths,
        prior._validate_allowed_paths_pictorial_agile,
        prior._verify_policy_files,
        prior._print_success,
    )
    try:
        (
            retention.IMPL_REQUIRE_EXACT_DELTA,
            base.compare_base_controlled,
            desktop.verify_extension_controlled_paths,
            execution.verify_extension_controlled_paths,
            shell.validate_allowed_paths,
            shell.verify_policy_files,
            shell.print_success,
        ) = predecessor
        _require_prebind_identity(shell, retention, desktop, execution)

        cases = (
            (retention, "IMPL_REQUIRE_EXACT_DELTA", _require_exact_delta_repair, "pre-bind exact-delta hook drifted"),
            (base, "compare_base_controlled", _compare_base_controlled_repair, "pre-bind base-control hook drifted"),
            (desktop, "verify_extension_controlled_paths", _verify_desktop_extension_paths, "pre-bind desktop-extension hook drifted"),
            (execution, "verify_extension_controlled_paths", _verify_execution_extension_paths, "pre-bind execution-extension hook drifted"),
            (shell, "validate_allowed_paths", _validate_allowed_paths_repair, "pre-bind tracked-path hook drifted"),
            (shell, "verify_policy_files", _verify_policy_files, "pre-bind policy-file hook drifted"),
            (shell, "print_success", _print_success, "pre-bind success-printer hook drifted"),
        )
        for owner, attribute, replacement, expected_message in cases:
            predecessor_value = getattr(owner, attribute)
            setattr(owner, attribute, replacement)
            try:
                base.expect_failure_matching(
                    f"Pictorial/Agile repair pre-bind {attribute} tamper",
                    expected_message,
                    _require_prebind_identity,
                    shell,
                    retention,
                    desktop,
                    execution,
                )
            finally:
                setattr(owner, attribute, predecessor_value)
    finally:
        (
            retention.IMPL_REQUIRE_EXACT_DELTA,
            base.compare_base_controlled,
            desktop.verify_extension_controlled_paths,
            execution.verify_extension_controlled_paths,
            shell.validate_allowed_paths,
            shell.verify_policy_files,
            shell.print_success,
        ) = installed
    _require_overlay_identity()


def selftest() -> None:
    _activate_contract()
    try:
        prior.selftest()
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile repair predecessor selftest topology is missing: "
            f"{exc}"
        )
    _install_policy()
    _selftest_workflow_binding()
    _selftest_bootstrap_delta()
    _selftest_target_transition()
    _selftest_allowlist_projection()
    _selftest_overlay_identity()
    _selftest_prebind_identity()
    _require_overlay_identity()

    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={impl.CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Pictorial/Agile three-finding repair self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_policy()
    _, retention, _, _, _ = _topology()
    return retention.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
