#!/usr/bin/env python3
"""Bounded authorization for one exact three-finding Pictorial/Agile contract repair."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_pictorial_agile_contract_three_finding_repair_v2_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_full_import_authorization_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "6df23c3c48faf5560e36698aa5344d012a050293"
FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
TARGET_PATH = "docs/acquisition/WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"
REJECTED_TARGET_GIT_BLOB_SHA1 = "3ede8efbd32c00bd0623924879a645964bd622ee"
TARGET_GIT_BLOB_SHA1 = "f3aedc464392d666ec55ae01d717207307c4c582"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "4fa977235329c1b05d7a0899c2dec994789c2263f49ffdfae6f588483d75a008",
    ADMISSION_WORKFLOW: "fc7cddfdd874acb86bca4da06e70644a181a2a6b8d02574d69ea4fdf9b6f5791",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "70afa78e86cee6d257cc18d426f1c010c2b35108da166f2a162702a322d3a047",
    ADMISSION_WORKFLOW: "62d27beed34bd01c40b71b916ae781a9afe04cf8f60446ffb4b046c6f5758a28",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
REPAIR_AUTHORIZATION = "EXACT_THREE_REVIEW_FINDING_REPAIR"
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
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(files, trees={p: _git_blob_sha1(b) for p, b in files.items()})


def _bind_prior_policy_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile authorization policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_full_import_authorization_integrity as prior  # noqa: E402

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_pictorial_agile
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_pictorial_agile
_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        return prior._topology()
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile repair inherited topology is missing or stale: {exc}")


def _activate_contract() -> None:
    try:
        current_target = prior.TARGET_GIT_BLOB_SHA1
        current_workflows = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile repair activation topology is missing or malformed: {exc}")
    if current_target not in {REJECTED_TARGET_GIT_BLOB_SHA1, TARGET_GIT_BLOB_SHA1}:
        base.fail(f"Pictorial/Agile repair predecessor target drifted: {current_target}")
    if current_workflows not in (dict(PRIOR_EXPECTED_WORKFLOW_SHA256), dict(EXPECTED_WORKFLOW_SHA256)):
        base.fail("Pictorial/Agile repair predecessor workflow hashes drifted")
    prior.TARGET_GIT_BLOB_SHA1 = TARGET_GIT_BLOB_SHA1
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior._activate_contract()


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail("Pictorial/Agile three-finding repair requires the canonical predecessor policy")
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(f"Pictorial/Agile repair base policy drifted: expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}")


def _validate_target(candidate: base.RepositoryView) -> None:
    actual = _git_blob_sha1(candidate.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual == REJECTED_TARGET_GIT_BLOB_SHA1:
        base.fail(f"Pictorial/Agile rejected contract blob remains present: {actual}")
    if actual != TARGET_GIT_BLOB_SHA1:
        base.fail(f"Pictorial/Agile repaired contract drifted: expected={TARGET_GIT_BLOB_SHA1} actual={actual}")


def _delegate_exact_delta(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    try:
        delegated = prior._require_exact_delta_pictorial_agile
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile repair inherited exact-delta topology is missing or stale: {exc}")
    if PRIOR_REQUIRE_EXACT_DELTA is not delegated:
        base.fail("Pictorial/Agile repair inherited exact-delta delegate drifted")
    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _require_exact_delta_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed = impl._changed_paths(candidate, policy_base)
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile repair changed-path topology is missing or stale: {exc}")
    if _is_bootstrap_base(policy_base):
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            _require_prior_policy_base(policy_base)
            return
        if changed & set(BOOTSTRAP_DELTA_PATHS):
            base.fail("Pictorial/Agile repair bootstrap delta must be exactly the repair policy plus two workflows")
        if TARGET_PATH in changed:
            base.fail("Pictorial/Agile repaired contract cannot transition before repair policy activation")
        _delegate_exact_delta(candidate, policy_base)
        return

    if TARGET_PATH in changed:
        if TARGET_PATH in _paths(policy_base):
            base.fail("Pictorial/Agile repaired contract is frozen after canonicalization")
        if changed != {TARGET_PATH}:
            base.fail("Pictorial/Agile repaired contract delta must be exactly one file")
        _validate_target(candidate)
        return
    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_repair(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if relative in BOOTSTRAP_WORKFLOWS:
            actual_candidate = _sha256(cb)
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            if actual_candidate != expected_candidate:
                base.fail(f"Pictorial/Agile repair workflow candidate drifted: {relative}")
            expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            if _sha256(bb) != expected_base:
                base.fail(f"Pictorial/Agile repair trusted-base workflow drifted: {relative}")
            if not bootstrap and cb != bb:
                base.fail(f"Pictorial/Agile repair steady-state workflow changed: {relative}")
            continue
        if cb != bb:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView, controlled: frozenset[str]) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)
    if POLICY_SCRIPT in controlled:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Pictorial/Agile repair policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Pictorial/Agile repair wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Pictorial/Agile repair steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("Pictorial/Agile repair steady-state wrapper changed")
    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled):
        cb = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if _sha256(cb) != expected_candidate:
            base.fail(f"Pictorial/Agile repair controlled workflow candidate drifted: {relative}")
        expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
        if _sha256(bb) != expected_base:
            base.fail(f"Pictorial/Agile repair controlled workflow base drifted: {relative}")
        if not bootstrap and cb != bb:
            base.fail(f"Pictorial/Agile repair controlled workflow changed: {relative}")
    delegated = frozenset(set(controlled) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS))
    if delegated:
        try:
            verifier = prior._verify_extension_paths_pictorial_agile
        except AttributeError as exc:
            base.fail(f"Pictorial/Agile repair inherited extension topology is missing or stale: {exc}")
        verifier(candidate, policy_base, delegated)


def _verify_execution_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, _, execution = _topology()
    try:
        controlled = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile repair execution extension topology is missing or stale: {exc}")
    _verify_extension_paths(candidate, policy_base, controlled)


def _verify_desktop_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, desktop, _ = _topology()
    try:
        controlled = desktop.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile repair desktop extension topology is missing or stale: {exc}")
    _verify_extension_paths(candidate, policy_base, controlled)


def _project_allowed_paths(paths: set[str]) -> set[str]:
    projected = set(paths)
    projected.discard(TARGET_PATH)
    return projected


def _validate_allowed_paths_repair(paths: set[str], stage: str) -> None:
    PRIOR_VALIDATE_ALLOWED_PATHS(_project_allowed_paths(paths), stage)


def _verify_policy_files(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(f"frozen Pictorial/Agile predecessor policy drifted: {actual}")
    prior._verify_policy_files(view)


def _require_prebind_identity(shell: Any, retention: Any, desktop: Any, execution: Any) -> None:
    try:
        expected = (
            (retention.IMPL_REQUIRE_EXACT_DELTA, prior._require_exact_delta_pictorial_agile, "exact-delta"),
            (base.compare_base_controlled, prior._compare_base_controlled_pictorial_agile, "base-control"),
            (desktop.verify_extension_controlled_paths, prior._verify_desktop_extension_paths, "desktop-extension"),
            (execution.verify_extension_controlled_paths, prior._verify_execution_extension_paths, "execution-extension"),
            (shell.validate_allowed_paths, prior._validate_allowed_paths_pictorial_agile, "tracked-path"),
            (shell.verify_policy_files, prior._verify_policy_files, "policy-file"),
            (shell.print_success, prior._print_success, "success-printer"),
        )
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile repair pre-bind topology is missing or stale: {exc}")
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile repair pre-bind {label} hook drifted")


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    try:
        prior_exact_delta = prior._require_exact_delta_pictorial_agile
        prior_allowed_paths = prior._validate_allowed_paths_pictorial_agile
        prior_print_success = prior._print_success
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
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile repair overlay topology is missing or stale: {exc}")
    if PRIOR_REQUIRE_EXACT_DELTA is not prior_exact_delta:
        base.fail("Pictorial/Agile repair inherited exact-delta delegate drifted")
    if PRIOR_VALIDATE_ALLOWED_PATHS is not prior_allowed_paths:
        base.fail("Pictorial/Agile repair inherited allowlist delegate drifted")
    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile repair {label} hook drifted")
    hook_identity(retention_exact_delta, "pictorial-agile-contract-three-finding-repair-v2-overlay")
    if POLICY_SCRIPT not in desktop_paths:
        base.fail("Pictorial/Agile repair desktop path registration drifted")
    if POLICY_SCRIPT not in execution_paths:
        base.fail("Pictorial/Agile repair execution path registration drifted")
    if _PRIOR_PRINT_SUCCESS is None or _PRIOR_PRINT_SUCCESS is not prior_print_success:
        base.fail("Pictorial/Agile repair prior success-printer drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior Pictorial/Agile success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"pictorial_agile_contract_review_repair_authorization={REPAIR_AUTHORIZATION}")
    print(f"pictorial_agile_contract_review_repair_rejected_blob={REJECTED_TARGET_GIT_BLOB_SHA1}")
    print(f"pictorial_agile_contract_review_repair_target_blob={TARGET_GIT_BLOB_SHA1}")
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
    prior._install_policy()
    prior._require_overlay_identity()
    shell, retention, _, desktop, execution = _topology()
    _require_prebind_identity(shell, retention, desktop, execution)
    desktop_paths = desktop.EXTENSION_CONTROLLED_PATHS
    execution_paths = execution.EXTENSION_CONTROLLED_PATHS
    _PRIOR_PRINT_SUCCESS = prior._print_success
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_repair
    base.compare_base_controlled = _compare_base_controlled_repair
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(set(desktop_paths) | {POLICY_SCRIPT})
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(set(execution_paths) | {POLICY_SCRIPT})
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
            base.fail(f"Pictorial/Agile repair workflow drifted: {path}")


def _selftest_deltas() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    prior_bytes = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    base_files = {PRIOR_POLICY_PATH: prior_bytes, FOUNDATION_WORKFLOW: b"old-f", ADMISSION_WORKFLOW: b"old-a"}
    candidate = dict(base_files)
    candidate.update({POLICY_SCRIPT: b"policy", FOUNDATION_WORKFLOW: b"new-f", ADMISSION_WORKFLOW: b"new-a"})
    _require_exact_delta_repair(_memory_view(candidate), _memory_view(base_files))
    mixed = dict(candidate)
    mixed[TARGET_PATH] = b"premature\n"
    base.expect_failure_matching("repair mixed bootstrap rejection", "bootstrap delta must be exactly", _require_exact_delta_repair, _memory_view(mixed), _memory_view(base_files))

    global TARGET_GIT_BLOB_SHA1, REJECTED_TARGET_GIT_BLOB_SHA1
    old_target, old_rejected = TARGET_GIT_BLOB_SHA1, REJECTED_TARGET_GIT_BLOB_SHA1
    repaired, rejected = b"repaired\n", b"rejected\n"
    TARGET_GIT_BLOB_SHA1, REJECTED_TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(repaired), _git_blob_sha1(rejected)
    try:
        steady = {PRIOR_POLICY_PATH: b"prior", POLICY_SCRIPT: b"policy"}
        good = dict(steady); good[TARGET_PATH] = repaired
        _require_exact_delta_repair(_memory_view(good), _memory_view(steady))
        bad = dict(steady); bad[TARGET_PATH] = rejected
        base.expect_failure_matching("repair rejected blob", "rejected contract blob", _require_exact_delta_repair, _memory_view(bad), _memory_view(steady))
        extra = dict(good); extra["EXTRA"] = b"x"
        base.expect_failure_matching("repair extra path", "exactly one file", _require_exact_delta_repair, _memory_view(extra), _memory_view(steady))
        frozen = dict(good); drift = dict(frozen); drift[TARGET_PATH] = b"drift\n"
        base.expect_failure_matching("repair frozen target", "frozen after canonicalization", _require_exact_delta_repair, _memory_view(drift), _memory_view(frozen))
    finally:
        TARGET_GIT_BLOB_SHA1, REJECTED_TARGET_GIT_BLOB_SHA1 = old_target, old_rejected


def _selftest_projection_and_identity() -> None:
    if _project_allowed_paths({"README.md", TARGET_PATH}) != {"README.md"}:
        base.fail("Pictorial/Agile repair allowlist projection drifted")
    _require_overlay_identity()
    original = prior._validate_allowed_paths_pictorial_agile
    prior._validate_allowed_paths_pictorial_agile = lambda paths, stage: None
    try:
        base.expect_failure_matching("repair inherited allowlist identity", "inherited allowlist delegate drifted", _require_overlay_identity)
    finally:
        prior._validate_allowed_paths_pictorial_agile = original
    delattr(prior, "_validate_allowed_paths_pictorial_agile")
    try:
        base.expect_failure_matching("repair missing overlay topology", "overlay topology is missing or stale", _require_overlay_identity)
    finally:
        prior._validate_allowed_paths_pictorial_agile = original
    _require_overlay_identity()


def selftest() -> None:
    _activate_contract()
    prior.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_deltas()
    _selftest_projection_and_identity()
    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail("canonical repository identity drifted")
    print("wepld Pictorial/Agile three-finding repair v2 self-tests: PASS")


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
