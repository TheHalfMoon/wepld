#!/usr/bin/env python3
"""Bounded authorization for three Qodo contract-review repairs to Pictorial/Agile."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_pictorial_agile_contract_three_finding_repair_v4_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_contract_three_finding_repair_v3_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "d91b4a11ca3d651d9262f7628e3cde1ab95bbc2c"
FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
TARGET_PATH = "docs/acquisition/WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"
REJECTED_TARGET_GIT_BLOB_SHA1 = "f3aedc464392d666ec55ae01d717207307c4c582"
TARGET_GIT_BLOB_SHA1 = "3af6496adaaf2ce6a16f92bf808102afaf137040"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "069014e970b4ce4c187cda886132e63b77505f72507c74e1347803fbd31db164",
    ADMISSION_WORKFLOW: "ae06e3e9db8ffca947d5eac24dfe461e39c3ed3082ec772ad8e5468b990736a2",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "ae541117dca18094a56d539c059391c1cd8303d29af58395d35b029c0a1b8410",
    ADMISSION_WORKFLOW: "ea77f2fc19cd6ca5194ad9f6437651269b581bfb64bf6c04260b90479f2b0e67",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
REPAIR_AUTHORIZATION = "EXACT_THREE_QODO_CONTRACT_FINDING_REPAIR"
REPAIR_FINDINGS = (
    "SOURCE_MAP_OBJECT_SHA_SCHEMA_CONSISTENCY",
    "FAIL_CLOSED_EXCLUSION_FIELD_NULLABILITY",
    "BRANDING_WHITESPACE_VARIANT_COVERAGE",
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
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(files, trees={path: _git_blob_sha1(data) for path, data in files.items()})


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"Pictorial/Agile contract repair-v4 {label} topology is malformed: expected path set")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"Pictorial/Agile contract repair-v4 {label} topology is malformed: non-string path")
    return frozenset(value)


def _bind_prior_policy_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile repair-v3 policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_contract_three_finding_repair_v3_integrity as prior  # noqa: E402

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_repair
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_repair
PRIOR_VERIFY_EXTENSION_PATHS = prior._verify_extension_paths
_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        topology = prior._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 inherited topology is missing or malformed: {exc}")
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("Pictorial/Agile contract repair-v4 inherited topology is malformed: expected five components")
    return topology


def _activate_contract() -> None:
    try:
        current_target = prior.EXPECTED_TARGET_GIT_BLOB_SHA1
        current_workflows = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 activation topology is missing or malformed: {exc}")

    if current_target != REJECTED_TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile contract repair-v4 predecessor target drifted: "
            f"expected={REJECTED_TARGET_GIT_BLOB_SHA1} actual={current_target}"
        )
    if current_workflows not in (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    ):
        base.fail("Pictorial/Agile contract repair-v4 predecessor workflow hashes drifted")

    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    try:
        prior._activate_contract()
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 activation delegate is missing or malformed: {exc}")


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail("Pictorial/Agile contract repair-v4 requires the canonical repair-v3 predecessor policy")
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile contract repair-v4 base policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _validate_target(candidate: base.RepositoryView) -> None:
    if TARGET_PATH not in _paths(candidate):
        base.fail("Pictorial/Agile contract repair-v4 target is missing")
    actual = _git_blob_sha1(candidate.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual == REJECTED_TARGET_GIT_BLOB_SHA1:
        base.fail(f"Pictorial/Agile rejected contract blob remains present: {actual}")
    if actual != TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile repaired contract drifted: "
            f"expected={TARGET_GIT_BLOB_SHA1} actual={actual}"
        )


def _delegate_exact_delta(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    try:
        delegated = prior._require_exact_delta_repair
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 inherited exact-delta topology is missing: {exc}")
    if delegated is not PRIOR_REQUIRE_EXACT_DELTA:
        base.fail("Pictorial/Agile contract repair-v4 inherited exact-delta delegate drifted")
    if not callable(delegated):
        base.fail("Pictorial/Agile contract repair-v4 inherited exact-delta delegate is not callable")
    try:
        delegated(candidate, policy_base)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 inherited exact-delta topology is malformed: {exc}")


def _require_exact_delta_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed_paths = impl._changed_paths
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 changed-path topology is missing: {exc}")
    if not callable(changed_paths):
        base.fail("Pictorial/Agile contract repair-v4 changed-path delegate is not callable")
    try:
        changed = _require_path_set(changed_paths(candidate, policy_base), "changed-path")
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 changed-path topology is malformed: {exc}")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "Pictorial/Agile contract repair-v4 bootstrap delta must be exactly "
                "the repair policy plus two workflows"
            )
        if TARGET_PATH in changed:
            base.fail("Pictorial/Agile contract cannot transition during repair-v4 bootstrap")
        _delegate_exact_delta(candidate, policy_base)
        return

    if TARGET_PATH in changed:
        if TARGET_PATH in _paths(policy_base):
            base.fail("Pictorial/Agile repaired contract is frozen after canonicalization")
        if changed != frozenset({TARGET_PATH}):
            base.fail("Pictorial/Agile repaired contract delta must be exactly one file")
        _validate_target(candidate)
        return

    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    try:
        controlled_paths = _require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 base-control topology is missing: {exc}")

    for relative in sorted(controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            if _sha256(candidate_bytes) != expected_candidate:
                base.fail(f"Pictorial/Agile contract repair-v4 workflow candidate drifted: {relative}")
            expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            if _sha256(base_bytes) != expected_base:
                base.fail(f"Pictorial/Agile contract repair-v4 trusted-base workflow drifted: {relative}")
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"Pictorial/Agile contract repair-v4 steady-state workflow changed: {relative}")
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
            base.fail("Pictorial/Agile contract repair-v4 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Pictorial/Agile contract repair-v4 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Pictorial/Agile contract repair-v4 steady-state base lacks wrapper")
            if (
                candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
                != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
            ):
                base.fail("Pictorial/Agile contract repair-v4 steady-state wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & safe_controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if _sha256(candidate_bytes) != expected_candidate:
            base.fail(f"Pictorial/Agile contract repair-v4 controlled workflow candidate drifted: {relative}")
        expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
        if _sha256(base_bytes) != expected_base:
            base.fail(f"Pictorial/Agile contract repair-v4 controlled workflow base drifted: {relative}")
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"Pictorial/Agile contract repair-v4 controlled workflow changed: {relative}")

    delegated = frozenset(safe_controlled - {POLICY_SCRIPT} - BOOTSTRAP_WORKFLOWS)
    if delegated:
        try:
            verifier = prior._verify_extension_paths
        except AttributeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v4 inherited extension topology is missing: {exc}")
        if verifier is not PRIOR_VERIFY_EXTENSION_PATHS:
            base.fail("Pictorial/Agile contract repair-v4 inherited extension verifier drifted")
        if not callable(verifier):
            base.fail("Pictorial/Agile contract repair-v4 inherited extension verifier is not callable")
        try:
            verifier(candidate, policy_base, delegated)
        except TypeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v4 inherited extension topology is malformed: {exc}")


def _verify_execution_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, _, execution = _topology()
    try:
        controlled = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 execution extension topology is missing: {exc}")
    _verify_extension_paths(candidate, policy_base, _require_path_set(controlled, "execution-extension"))


def _verify_desktop_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, desktop, _ = _topology()
    try:
        controlled = desktop.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 desktop extension topology is missing: {exc}")
    _verify_extension_paths(candidate, policy_base, _require_path_set(controlled, "desktop-extension"))


def _validate_allowed_paths_repair(paths: set[str], stage: str) -> None:
    try:
        delegated = prior._validate_allowed_paths_repair
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 inherited allowlist topology is missing: {exc}")
    if delegated is not PRIOR_VALIDATE_ALLOWED_PATHS:
        base.fail("Pictorial/Agile contract repair-v4 inherited allowlist delegate drifted")
    if not callable(delegated):
        base.fail("Pictorial/Agile contract repair-v4 inherited allowlist delegate is not callable")
    try:
        delegated(paths, stage)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 inherited allowlist topology is malformed: {exc}")


def _verify_policy_files(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(f"frozen Pictorial/Agile repair-v3 predecessor policy drifted: {actual}")
    try:
        verifier = prior._verify_policy_files
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 inherited policy-file topology is missing: {exc}")
    if not callable(verifier):
        base.fail("Pictorial/Agile contract repair-v4 inherited policy-file verifier is not callable")
    try:
        verifier(view)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 inherited policy-file topology is malformed: {exc}")


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
        base.fail(f"Pictorial/Agile contract repair-v4 pre-bind topology is missing: {exc}")

    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile contract repair-v4 pre-bind {label} hook drifted")


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
        base.fail(f"Pictorial/Agile contract repair-v4 overlay topology is missing: {exc}")

    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile contract repair-v4 {label} hook drifted")

    if not callable(hook_identity):
        base.fail("Pictorial/Agile contract repair-v4 hook identity is not callable")
    if not callable(retention_exact_delta):
        base.fail("Pictorial/Agile contract repair-v4 retention exact-delta is not callable")
    if not callable(prior_print_success):
        base.fail("Pictorial/Agile contract repair-v4 prior success-printer is not callable")

    safe_desktop_paths = _require_path_set(desktop_paths, "desktop-extension")
    safe_execution_paths = _require_path_set(execution_paths, "execution-extension")

    try:
        hook_identity(retention_exact_delta, "pictorial-agile-contract-three-finding-repair-v4-overlay")
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 overlay topology is malformed: {exc}")

    if POLICY_SCRIPT not in safe_desktop_paths:
        base.fail("Pictorial/Agile contract repair-v4 desktop path registration drifted")
    if POLICY_SCRIPT not in safe_execution_paths:
        base.fail("Pictorial/Agile contract repair-v4 execution path registration drifted")
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("Pictorial/Agile contract repair-v4 prior success-printer is missing or malformed")
    if _PRIOR_PRINT_SUCCESS is not prior_print_success:
        base.fail("Pictorial/Agile contract repair-v4 prior success-printer drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("prior Pictorial/Agile repair-v3 success printer is missing or malformed")
    try:
        _PRIOR_PRINT_SUCCESS(stage, mode)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 success-printer topology is malformed: {exc}")

    print(f"pictorial_agile_contract_three_finding_repair_v4_authorization={REPAIR_AUTHORIZATION}")
    print("pictorial_agile_contract_three_finding_repair_v4_findings=" + ",".join(REPAIR_FINDINGS))
    print(f"pictorial_agile_contract_three_finding_repair_v4_rejected_blob={REJECTED_TARGET_GIT_BLOB_SHA1}")
    print(f"pictorial_agile_contract_three_finding_repair_v4_target_blob={TARGET_GIT_BLOB_SHA1}")
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
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 predecessor installation is missing or malformed: {exc}")

    shell, retention, _, desktop, execution = _topology()
    _require_prebind_identity(shell, retention, desktop, execution)

    try:
        desktop_paths = _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension")
        execution_paths = _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension")
        prior_print_success = prior._print_success
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 installation topology is missing: {exc}")
    if not callable(prior_print_success):
        base.fail("Pictorial/Agile contract repair-v4 predecessor success printer is not callable")

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
            base.fail(f"Pictorial/Agile contract repair-v4 workflow drifted: {path}")


def _bootstrap_views() -> tuple[base.MemoryView, base.MemoryView]:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    prior_bytes = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        PRIOR_POLICY_PATH: prior_bytes,
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


def _steady_target_views(target_bytes: bytes, *, extra: bool = False) -> tuple[base.MemoryView, base.MemoryView]:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    prior_bytes = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    base_files = {
        PRIOR_POLICY_PATH: prior_bytes,
        POLICY_SCRIPT: policy_bytes,
    }
    candidate_files = dict(base_files)
    candidate_files[TARGET_PATH] = target_bytes
    if extra:
        candidate_files["UNEXPECTED"] = b"x"
    return _memory_view(candidate_files), _memory_view(base_files)


def _selftest_deltas() -> None:
    candidate, policy_base = _bootstrap_views()
    _require_exact_delta_repair(candidate, policy_base)

    mixed_files = {
        entry.path: candidate.read_bytes(entry.path, base.MAX_POLICY_FILE_BYTES)
        for entry in candidate.entries()
    }
    mixed_files[TARGET_PATH] = b"premature\n"
    base.expect_failure_matching(
        "contract repair-v4 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_repair,
        _memory_view(mixed_files),
        policy_base,
    )

    wrong_candidate, steady_base = _steady_target_views(b"wrong-target\n")
    base.expect_failure_matching(
        "contract repair-v4 wrong target rejection",
        "repaired contract drifted",
        _require_exact_delta_repair,
        wrong_candidate,
        steady_base,
    )

    mixed_target, steady_base = _steady_target_views(b"wrong-target\n", extra=True)
    base.expect_failure_matching(
        "contract repair-v4 mixed target rejection",
        "repaired contract delta must be exactly one file",
        _require_exact_delta_repair,
        mixed_target,
        steady_base,
    )

    frozen_base_files = {
        entry.path: steady_base.read_bytes(entry.path, base.MAX_POLICY_FILE_BYTES)
        for entry in steady_base.entries()
    }
    frozen_base_files[TARGET_PATH] = b"old\n"
    frozen_candidate_files = dict(frozen_base_files)
    frozen_candidate_files[TARGET_PATH] = b"new\n"
    base.expect_failure_matching(
        "contract repair-v4 frozen target rejection",
        "frozen after canonicalization",
        _require_exact_delta_repair,
        _memory_view(frozen_candidate_files),
        _memory_view(frozen_base_files),
    )


def _selftest_identity_drift() -> None:
    original_prior_print_success = prior._print_success
    prior._print_success = lambda stage, mode: None
    try:
        base.expect_failure_matching(
            "contract repair-v4 rebound prior success printer",
            "prior success-printer drifted",
            _require_overlay_identity,
        )
    finally:
        prior._print_success = original_prior_print_success

    _require_overlay_identity()


def selftest() -> None:
    _activate_contract()
    try:
        prior.selftest()
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v4 predecessor selftest topology is malformed: {exc}")
    _install_policy()
    _selftest_workflows()
    _selftest_deltas()
    _selftest_identity_drift()

    if REJECTED_TARGET_GIT_BLOB_SHA1 == TARGET_GIT_BLOB_SHA1:
        base.fail("Pictorial/Agile contract repair-v4 target did not change")
    if len(REPAIR_FINDINGS) != 3 or len(set(REPAIR_FINDINGS)) != 3:
        base.fail("Pictorial/Agile contract repair-v4 finding set must contain exactly three unique findings")

    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail("canonical repository identity drifted")
    print("wepld Pictorial/Agile three-Qodo-finding contract repair v4 self-tests: PASS")


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0

        _install_policy()
        _, retention, _, _, _ = _topology()
        try:
            runner = retention.main
        except AttributeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v4 runtime topology is missing: {exc}")
        if not callable(runner):
            base.fail("Pictorial/Agile contract repair-v4 runtime main is not callable")
        try:
            return runner(argv)
        except TypeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v4 runtime topology is malformed: {exc}")
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
