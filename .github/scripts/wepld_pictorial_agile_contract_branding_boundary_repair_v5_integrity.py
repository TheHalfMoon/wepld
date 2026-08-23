#!/usr/bin/env python3
"""Bounded authorization for the Qodo branding-boundary contract repair to Pictorial/Agile."""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_pictorial_agile_contract_branding_boundary_repair_v5_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_contract_three_finding_repair_v4_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "cc9026d16e529fde8fc4d5ad1c65e4dc4e2417a5"
FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
TARGET_PATH = "docs/acquisition/WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"
REJECTED_TARGET_GIT_BLOB_SHA1 = "3af6496adaaf2ce6a16f92bf808102afaf137040"
TARGET_GIT_BLOB_SHA1 = "60e17357f7026a1568b9607a85a25a5abcfe5e5d"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "ae541117dca18094a56d539c059391c1cd8303d29af58395d35b029c0a1b8410",
    ADMISSION_WORKFLOW: "ea77f2fc19cd6ca5194ad9f6437651269b581bfb64bf6c04260b90479f2b0e67",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "e5f527231d516579f5b957d4fba857dc6f9a118bd52a3d58b48a399f26076685",
    ADMISSION_WORKFLOW: "cff1183a888771fee76fdde063af76b7c964eff488ac050baa35cd0ae841145f",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
REPAIR_AUTHORIZATION = "EXACT_ONE_QODO_BRANDING_BOUNDARY_REPAIR"
REPAIR_FINDINGS = ("BRANDING_BOUNDARY_BYPASS",)

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
POLICY_BASE_SHA_ENV = "WEPLD_POLICY_BASE_SHA"
MAX_COMPARE_READ_ATTEMPTS = 3


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
        base.fail(f"Pictorial/Agile contract repair-v5 {label} topology is malformed: expected path set")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"Pictorial/Agile contract repair-v5 {label} topology is malformed: non-string path")
    return frozenset(value)


def _bind_prior_policy_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile repair-v4 policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_contract_three_finding_repair_v4_integrity as prior  # noqa: E402

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_repair
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_repair
PRIOR_VERIFY_EXTENSION_PATHS = prior._verify_extension_paths
_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        topology = prior._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 inherited topology is missing or malformed: {exc}")
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("Pictorial/Agile contract repair-v5 inherited topology is malformed: expected five components")
    return topology


def _activate_predecessor() -> None:
    try:
        if prior.TARGET_GIT_BLOB_SHA1 != REJECTED_TARGET_GIT_BLOB_SHA1:
            base.fail(
                "Pictorial/Agile contract repair-v5 predecessor target drifted: "
                f"expected={REJECTED_TARGET_GIT_BLOB_SHA1} actual={prior.TARGET_GIT_BLOB_SHA1}"
            )
        current_workflows = dict(prior.EXPECTED_WORKFLOW_SHA256)
        if current_workflows not in (
            dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
            dict(EXPECTED_WORKFLOW_SHA256),
        ):
            base.fail("Pictorial/Agile contract repair-v5 predecessor workflow hashes drifted")
        prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
        prior._install_policy()
        prior._require_overlay_identity()
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 predecessor activation is missing or malformed: {exc}")


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail("Pictorial/Agile contract repair-v5 requires the canonical repair-v4 predecessor policy")
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile contract repair-v5 base policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _validate_target(candidate: base.RepositoryView) -> None:
    if TARGET_PATH not in _paths(candidate):
        base.fail("Pictorial/Agile contract repair-v5 target is missing")
    actual = _git_blob_sha1(candidate.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual == REJECTED_TARGET_GIT_BLOB_SHA1:
        base.fail(f"Pictorial/Agile rejected contract blob remains present: {actual}")
    if actual != TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile branding-boundary repaired contract drifted: "
            f"expected={TARGET_GIT_BLOB_SHA1} actual={actual}"
        )


def _delegate_exact_delta(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    try:
        delegated = prior._require_exact_delta_repair
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 inherited exact-delta topology is missing: {exc}")
    if delegated is not PRIOR_REQUIRE_EXACT_DELTA:
        base.fail("Pictorial/Agile contract repair-v5 inherited exact-delta delegate drifted")
    if not callable(delegated):
        base.fail("Pictorial/Agile contract repair-v5 inherited exact-delta delegate is not callable")
    try:
        delegated(candidate, policy_base)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 inherited exact-delta topology is malformed: {exc}")


def _require_exact_delta_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed_paths = impl._changed_paths
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 changed-path topology is missing: {exc}")
    if not callable(changed_paths):
        base.fail("Pictorial/Agile contract repair-v5 changed-path delegate is not callable")
    try:
        changed = _require_path_set(changed_paths(candidate, policy_base), "changed-path")
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 changed-path topology is malformed: {exc}")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "Pictorial/Agile contract repair-v5 bootstrap delta must be exactly "
                "the repair policy plus two workflows"
            )
        if TARGET_PATH in changed:
            base.fail("Pictorial/Agile contract cannot transition during repair-v5 bootstrap")
        _delegate_exact_delta(candidate, policy_base)
        return

    if TARGET_PATH in changed:
        if TARGET_PATH in _paths(policy_base):
            base.fail("Pictorial/Agile repaired contract is frozen after canonicalization")
        if changed != frozenset({TARGET_PATH}):
            base.fail("Pictorial/Agile branding-boundary repair delta must be exactly one file")
        _validate_target(candidate)
        return

    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    try:
        controlled_paths = _require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 base-control topology is missing: {exc}")

    for relative in sorted(controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            if _sha256(candidate_bytes) != expected_candidate:
                base.fail(f"Pictorial/Agile contract repair-v5 workflow candidate drifted: {relative}")
            expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            if _sha256(base_bytes) != expected_base:
                base.fail(f"Pictorial/Agile contract repair-v5 trusted-base workflow drifted: {relative}")
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"Pictorial/Agile contract repair-v5 steady-state workflow changed: {relative}")
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
            base.fail("Pictorial/Agile contract repair-v5 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Pictorial/Agile contract repair-v5 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Pictorial/Agile contract repair-v5 steady-state base lacks wrapper")
            if (
                candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
                != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
            ):
                base.fail("Pictorial/Agile contract repair-v5 steady-state wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & safe_controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if _sha256(candidate_bytes) != expected_candidate:
            base.fail(f"Pictorial/Agile contract repair-v5 controlled workflow candidate drifted: {relative}")
        expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
        if _sha256(base_bytes) != expected_base:
            base.fail(f"Pictorial/Agile contract repair-v5 controlled workflow base drifted: {relative}")
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"Pictorial/Agile contract repair-v5 controlled workflow changed: {relative}")

    delegated = frozenset(safe_controlled - {POLICY_SCRIPT} - BOOTSTRAP_WORKFLOWS)
    if delegated:
        try:
            verifier = prior._verify_extension_paths
        except AttributeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v5 inherited extension topology is missing: {exc}")
        if verifier is not PRIOR_VERIFY_EXTENSION_PATHS:
            base.fail("Pictorial/Agile contract repair-v5 inherited extension verifier drifted")
        if not callable(verifier):
            base.fail("Pictorial/Agile contract repair-v5 inherited extension verifier is not callable")
        try:
            verifier(candidate, policy_base, delegated)
        except TypeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v5 inherited extension topology is malformed: {exc}")


def _verify_execution_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, _, execution = _topology()
    try:
        controlled = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 execution extension topology is missing: {exc}")
    _verify_extension_paths(candidate, policy_base, _require_path_set(controlled, "execution-extension"))


def _verify_desktop_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, desktop, _ = _topology()
    try:
        controlled = desktop.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 desktop extension topology is missing: {exc}")
    _verify_extension_paths(candidate, policy_base, _require_path_set(controlled, "desktop-extension"))


def _validate_allowed_paths_repair(paths: set[str], stage: str) -> None:
    try:
        delegated = prior._validate_allowed_paths_repair
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 inherited allowlist topology is missing: {exc}")
    if delegated is not PRIOR_VALIDATE_ALLOWED_PATHS:
        base.fail("Pictorial/Agile contract repair-v5 inherited allowlist delegate drifted")
    if not callable(delegated):
        base.fail("Pictorial/Agile contract repair-v5 inherited allowlist delegate is not callable")
    try:
        delegated(paths, stage)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 inherited allowlist topology is malformed: {exc}")


def _verify_policy_files(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(f"frozen Pictorial/Agile repair-v4 predecessor policy drifted: {actual}")
    try:
        verifier = prior._verify_policy_files
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 inherited policy-file topology is missing: {exc}")
    if not callable(verifier):
        base.fail("Pictorial/Agile contract repair-v5 inherited policy-file verifier is not callable")
    try:
        verifier(view)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 inherited policy-file topology is malformed: {exc}")


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
        base.fail(f"Pictorial/Agile contract repair-v5 pre-bind topology is missing: {exc}")

    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile contract repair-v5 pre-bind {label} hook drifted")


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
        base.fail(f"Pictorial/Agile contract repair-v5 overlay topology is missing: {exc}")

    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile contract repair-v5 {label} hook drifted")

    if not callable(hook_identity):
        base.fail("Pictorial/Agile contract repair-v5 hook identity is not callable")
    if not callable(retention_exact_delta):
        base.fail("Pictorial/Agile contract repair-v5 retention exact-delta is not callable")
    if not callable(prior_print_success):
        base.fail("Pictorial/Agile contract repair-v5 prior success-printer is not callable")

    safe_desktop_paths = _require_path_set(desktop_paths, "desktop-extension")
    safe_execution_paths = _require_path_set(execution_paths, "execution-extension")

    try:
        hook_identity(retention_exact_delta, "pictorial-agile-contract-branding-boundary-repair-v5-overlay")
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 overlay topology is malformed: {exc}")

    if POLICY_SCRIPT not in safe_desktop_paths:
        base.fail("Pictorial/Agile contract repair-v5 desktop path registration drifted")
    if POLICY_SCRIPT not in safe_execution_paths:
        base.fail("Pictorial/Agile contract repair-v5 execution path registration drifted")
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("Pictorial/Agile contract repair-v5 prior success-printer is missing or malformed")
    if _PRIOR_PRINT_SUCCESS is not prior_print_success:
        base.fail("Pictorial/Agile contract repair-v5 prior success-printer drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("prior Pictorial/Agile repair-v4 success printer is missing or malformed")
    try:
        _PRIOR_PRINT_SUCCESS(stage, mode)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 success-printer topology is malformed: {exc}")

    print(f"pictorial_agile_contract_branding_boundary_repair_v5_authorization={REPAIR_AUTHORIZATION}")
    print("pictorial_agile_contract_branding_boundary_repair_v5_findings=" + ",".join(REPAIR_FINDINGS))
    print(f"pictorial_agile_contract_branding_boundary_repair_v5_rejected_blob={REJECTED_TARGET_GIT_BLOB_SHA1}")
    print(f"pictorial_agile_contract_branding_boundary_repair_v5_target_blob={TARGET_GIT_BLOB_SHA1}")
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
        base.fail(f"Pictorial/Agile contract repair-v5 installation topology is missing: {exc}")
    if not callable(prior_print_success):
        base.fail("Pictorial/Agile contract repair-v5 predecessor success printer is not callable")

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


def _verify_with_policy_base(
    shell: Any,
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> str:
    try:
        verifier = shell.verify_view
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 verify-view topology is missing: {exc}")
    if not callable(verifier):
        base.fail("Pictorial/Agile contract repair-v5 verify-view topology is not callable")
    try:
        stage = verifier(candidate, policy_base=policy_base)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 verify-view topology is malformed: {exc}")
    if not isinstance(stage, str):
        base.fail("Pictorial/Agile contract repair-v5 verify-view returned a non-string stage")
    return stage


def _activation_shas(args: Any) -> tuple[str, str]:
    policy_base_sha = base.require_comparison_sha(
        os.environ.get(POLICY_BASE_SHA_ENV)
    ).lower()
    baseline_check_sha = base.require_comparison_sha(args.pr_base_sha).lower()
    if policy_base_sha == baseline_check_sha:
        base.fail("Pictorial/Agile contract repair-v5 activation predecessor equals pushed head")
    return policy_base_sha, baseline_check_sha


def _compare_url(
    canonical_repository: str,
    policy_base_sha: str,
    baseline_check_sha: str,
) -> str:
    return (
        f"https://api.github.com/repos/{canonical_repository}/compare/"
        f"{policy_base_sha}...{baseline_check_sha}"
    )


def _is_transient_compare_failure(exc: base.PolicyError, url: str) -> bool:
    text = str(exc)
    prefix = f"GitHub API request failed for {url}:"
    if not text.startswith(prefix):
        return False
    detail = text[len(prefix):].lstrip()
    http_marker = "HTTP Error "
    if not detail.startswith(http_marker):
        return True
    code_text = detail[len(http_marker):len(http_marker) + 3]
    return code_text.isdigit() and 500 <= int(code_text) <= 599


def _read_compare_with_bounded_retry(client: Any, url: str) -> dict[str, Any]:
    last_error: base.PolicyError | None = None
    for _attempt in range(MAX_COMPARE_READ_ATTEMPTS):
        try:
            response = client.json(url)
        except base.PolicyError as exc:
            if not _is_transient_compare_failure(exc, url):
                raise
            last_error = exc
            continue
        if not isinstance(response, dict):
            base.fail(
                "Pictorial/Agile contract repair-v5 compare response is malformed: "
                f"url={url}"
            )
        return response
    if last_error is None:
        base.fail(
            "Pictorial/Agile contract repair-v5 bounded compare retry exhausted "
            "without an error"
        )
    raise last_error


def _require_push_activation_ancestry(
    client: Any,
    canonical_repository: str,
    policy_base_sha: str,
    baseline_check_sha: str,
) -> None:
    url = _compare_url(
        canonical_repository,
        policy_base_sha,
        baseline_check_sha,
    )
    response = _read_compare_with_bounded_retry(client, url)
    status = response.get("status")
    if status != "ahead":
        base.fail(
            "Pictorial/Agile contract repair-v5 pushed head is not a descendant "
            "of the immutable activation predecessor: "
            f"status={status!r} "
            f"policy_base_sha={policy_base_sha} "
            f"baseline_check_sha={baseline_check_sha} "
            f"compare_url={url}"
        )


def _verify_local_with_remote_policy_base(args: Any, shell: Any, impl: Any) -> int:
    if args.command != "verify-local" or not args.remote_baseline:
        base.fail("Pictorial/Agile contract repair-v5 trusted-base local verifier invoked outside remote-baseline mode")

    policy_base_sha, baseline_check_sha = _activation_shas(args)
    try:
        canonical_repository = impl.CANONICAL_REPOSITORY
        desktop_runner = shell.desktop_runner
        install_desktop_path = desktop_runner._install_desktop_path_attribute
        verify_remote_baseline = desktop_runner.verify_remote_baseline
        print_success = shell.print_success
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 trusted-base local topology is missing: {exc}")

    if canonical_repository != base.REPOSITORY:
        base.fail(
            "Pictorial/Agile contract repair-v5 canonical repository drifted: "
            f"expected={base.REPOSITORY} actual={canonical_repository}"
        )
    for func, label in (
        (install_desktop_path, "desktop path installer"),
        (verify_remote_baseline, "remote baseline verifier"),
        (print_success, "success printer"),
    ):
        if not callable(func):
            base.fail(f"Pictorial/Agile contract repair-v5 {label} is not callable")

    try:
        install_desktop_path()
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 desktop path topology is malformed: {exc}")

    token = os.environ.get(args.github_token_env) or None
    client = base.GitHubClient(token)
    _require_push_activation_ancestry(
        client,
        canonical_repository,
        policy_base_sha,
        baseline_check_sha,
    )
    candidate = base.LocalRepositoryView(Path(args.root))
    policy_base = base.RemoteRepositoryView(canonical_repository, policy_base_sha, client)
    stage = _verify_with_policy_base(shell, candidate, policy_base)
    try:
        verify_remote_baseline(client, baseline_check_sha)
        print_success(stage, "LOCAL_CHECKOUT")
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 trusted-base local topology is malformed: {exc}")
    return 0


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != EXPECTED_WORKFLOW_SHA256[path]:
            base.fail(f"Pictorial/Agile contract repair-v5 workflow drifted: {path}")


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
        "contract repair-v5 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_repair,
        _memory_view(mixed_files),
        policy_base,
    )

    wrong_candidate, steady_base = _steady_target_views(b"wrong-target\n")
    base.expect_failure_matching(
        "contract repair-v5 wrong target rejection",
        "branding-boundary repaired contract drifted",
        _require_exact_delta_repair,
        wrong_candidate,
        steady_base,
    )

    mixed_target, steady_base = _steady_target_views(b"wrong-target\n", extra=True)
    base.expect_failure_matching(
        "contract repair-v5 mixed target rejection",
        "branding-boundary repair delta must be exactly one file",
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
        "contract repair-v5 frozen target rejection",
        "frozen after canonicalization",
        _require_exact_delta_repair,
        _memory_view(frozen_candidate_files),
        _memory_view(frozen_base_files),
    )


def _selftest_policy_base_forwarding() -> None:
    shell, _, _, _, _ = _topology()
    try:
        original_verify_view = shell.verify_view
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 verify-view selftest topology is missing: {exc}")
    if not callable(original_verify_view):
        base.fail("Pictorial/Agile contract repair-v5 verify-view selftest topology is not callable")

    candidate = _memory_view({"candidate": b"candidate"})
    trusted = _memory_view({"trusted": b"trusted"})
    calls = 0

    def probe(view: base.RepositoryView, *, policy_base: base.RepositoryView | None = None) -> str:
        nonlocal calls
        calls += 1
        if view is not candidate:
            base.fail("Pictorial/Agile contract repair-v5 policy-base selftest candidate drifted")
        if policy_base is not trusted:
            base.fail("Pictorial/Agile contract repair-v5 verify-local skipped trusted policy base")
        return "POLICY_BASE_BOUND"

    shell.verify_view = probe
    try:
        stage = _verify_with_policy_base(shell, candidate, trusted)
    finally:
        shell.verify_view = original_verify_view

    if calls != 1 or stage != "POLICY_BASE_BOUND":
        base.fail("Pictorial/Agile contract repair-v5 policy-base forwarding selftest drifted")


def _selftest_activation_sha_split() -> None:
    class Args:
        pr_base_sha = "B" * 40

    class SameCommitDifferentCaseArgs:
        pr_base_sha = "A" * 40

    previous = os.environ.get(POLICY_BASE_SHA_ENV)
    os.environ[POLICY_BASE_SHA_ENV] = "A" * 40
    try:
        policy_base_sha, baseline_check_sha = _activation_shas(Args())
        os.environ[POLICY_BASE_SHA_ENV] = "a" * 40
        base.expect_failure_matching(
            "contract repair-v5 mixed-case identical activation SHA rejection",
            "activation predecessor equals pushed head",
            _activation_shas,
            SameCommitDifferentCaseArgs(),
        )
    finally:
        if previous is None:
            os.environ.pop(POLICY_BASE_SHA_ENV, None)
        else:
            os.environ[POLICY_BASE_SHA_ENV] = previous

    if policy_base_sha != "a" * 40 or baseline_check_sha != "b" * 40:
        base.fail("Pictorial/Agile contract repair-v5 activation SHA normalization drifted")

    class ProbeClient:
        def __init__(self, status: str) -> None:
            self.status = status
            self.url = ""
            self.calls = 0

        def json(self, url: str) -> dict[str, str]:
            self.url = url
            self.calls += 1
            return {"status": self.status}

    probe = ProbeClient("ahead")
    _require_push_activation_ancestry(
        probe,
        base.REPOSITORY,
        "a" * 40,
        "b" * 40,
    )
    expected_url = _compare_url(
        base.REPOSITORY,
        "a" * 40,
        "b" * 40,
    )
    if probe.url != expected_url or probe.calls != 1:
        base.fail("Pictorial/Agile contract repair-v5 activation ancestry URL drifted")

    diverged = ProbeClient("diverged")
    try:
        _require_push_activation_ancestry(
            diverged,
            base.REPOSITORY,
            "a" * 40,
            "b" * 40,
        )
    except base.PolicyError as exc:
        message = str(exc)
        for fragment in (
            "pushed head is not a descendant",
            "status='diverged'",
            f"policy_base_sha={'a' * 40}",
            f"baseline_check_sha={'b' * 40}",
            f"compare_url={expected_url}",
        ):
            if fragment not in message:
                base.fail(
                    "Pictorial/Agile contract repair-v5 ancestry failure evidence "
                    f"is incomplete: missing={fragment}"
                )
    else:
        base.fail("Pictorial/Agile contract repair-v5 rewritten history was accepted")

    class TransientProbeClient:
        def __init__(self) -> None:
            self.calls = 0
            self.url = ""

        def json(self, url: str) -> dict[str, str]:
            self.url = url
            self.calls += 1
            if self.calls < MAX_COMPARE_READ_ATTEMPTS:
                raise base.PolicyError(
                    f"GitHub API request failed for {url}: "
                    "HTTP Error 503: Service Unavailable"
                )
            return {"status": "ahead"}

    transient = TransientProbeClient()
    _require_push_activation_ancestry(
        transient,
        base.REPOSITORY,
        "a" * 40,
        "b" * 40,
    )
    if transient.url != expected_url or transient.calls != MAX_COMPARE_READ_ATTEMPTS:
        base.fail("Pictorial/Agile contract repair-v5 transient compare retry drifted")

    class NetworkTransientProbeClient:
        def __init__(self) -> None:
            self.calls = 0
            self.url = ""

        def json(self, url: str) -> dict[str, str]:
            self.url = url
            self.calls += 1
            if self.calls < MAX_COMPARE_READ_ATTEMPTS:
                raise base.PolicyError(
                    f"GitHub API request failed for {url}: timed out"
                )
            return {"status": "ahead"}

    network_transient = NetworkTransientProbeClient()
    _require_push_activation_ancestry(
        network_transient,
        base.REPOSITORY,
        "a" * 40,
        "b" * 40,
    )
    if (
        network_transient.url != expected_url
        or network_transient.calls != MAX_COMPARE_READ_ATTEMPTS
    ):
        base.fail(
            "Pictorial/Agile contract repair-v5 non-HTTP transient compare retry drifted"
        )

    class PermanentProbeClient:
        def __init__(self) -> None:
            self.calls = 0

        def json(self, url: str) -> dict[str, str]:
            self.calls += 1
            raise base.PolicyError(
                f"GitHub API request failed for {url}: HTTP Error 404: Not Found"
            )

    permanent = PermanentProbeClient()
    try:
        _require_push_activation_ancestry(
            permanent,
            base.REPOSITORY,
            "a" * 40,
            "b" * 40,
        )
    except base.PolicyError as exc:
        if "HTTP Error 404:" not in str(exc):
            raise
    else:
        base.fail("Pictorial/Agile contract repair-v5 permanent compare failure was accepted")
    if permanent.calls != 1:
        base.fail("Pictorial/Agile contract repair-v5 retried a non-transient compare failure")


def _selftest_identity_drift() -> None:
    original_prior_print_success = prior._print_success
    prior._print_success = lambda stage, mode: None
    try:
        base.expect_failure_matching(
            "contract repair-v5 rebound prior success printer",
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
        base.fail(f"Pictorial/Agile contract repair-v5 predecessor selftest binding is malformed: {exc}")
    if current_workflows not in (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    ):
        base.fail("Pictorial/Agile contract repair-v5 predecessor selftest workflow hashes drifted")
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    try:
        prior.selftest()
    except TypeError as exc:
        base.fail(f"Pictorial/Agile contract repair-v5 predecessor selftest topology is malformed: {exc}")
    _install_policy()
    _selftest_workflows()
    _selftest_deltas()
    _selftest_policy_base_forwarding()
    _selftest_activation_sha_split()
    _selftest_identity_drift()

    if REJECTED_TARGET_GIT_BLOB_SHA1 == TARGET_GIT_BLOB_SHA1:
        base.fail("Pictorial/Agile contract repair-v5 target did not change")
    if len(REPAIR_FINDINGS) != 1 or len(set(REPAIR_FINDINGS)) != 1:
        base.fail("Pictorial/Agile contract repair-v5 finding set must contain exactly one unique finding")
    if REPAIR_FINDINGS != ("BRANDING_BOUNDARY_BYPASS",):
        base.fail("Pictorial/Agile contract repair-v5 finding identity drifted")

    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail("canonical repository identity drifted")
    print("wepld Pictorial/Agile branding-boundary contract repair v5 self-tests: PASS")


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
                return _verify_local_with_remote_policy_base(args, shell, impl)

        try:
            runner = retention.main
        except AttributeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v5 runtime topology is missing: {exc}")
        if not callable(runner):
            base.fail("Pictorial/Agile contract repair-v5 runtime main is not callable")
        try:
            return runner(argv)
        except TypeError as exc:
            base.fail(f"Pictorial/Agile contract repair-v5 runtime topology is malformed: {exc}")
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
