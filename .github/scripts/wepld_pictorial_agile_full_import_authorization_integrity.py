#!/usr/bin/env python3
"""Add one exact Pictorial + Agile import-contract authorization.

This module is repository CI/evidence-policy machinery. It is not the product
Trusted Core runtime: the product Trusted Core remains the separate Rust Core.

This wrapper is a bounded, non-self-authorizing policy transition layered over
the canonical MiniMax five-finding repair authorization. It adds only:

1. this policy/workflow bootstrap; and
2. after canonical activation, one exact content-addressed Pictorial + Agile
   full donor import / derivative rebrand contract document.

The wrapper intentionally preserves, but does not widen, authorizations already
owned by the exact pinned predecessor. A non-Pictorial/Agile delta may therefore
continue only when that predecessor itself accepts it. Such inherited authority
is not newly granted by this wrapper.

This wrapper does not itself admit donor source bytes, dependencies, workflows,
hooks, executables, model/provider calls, runtime behavior, or product
authority. Those require later explicit qualification/admission gates.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = (
    ".github/scripts/"
    "wepld_pictorial_agile_full_import_authorization_integrity.py"
)
PRIOR_POLICY_PATH = (
    ".github/scripts/"
    "wepld_minimax_agent_research_five_finding_repair_integrity.py"
)
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "02e597ef88820b7b75034574673d8e361d88e62c"


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
            "frozen MiniMax five-finding policy runner drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_minimax_agent_research_five_finding_repair_integrity as prior  # noqa: E402

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

TARGET_PATH = (
    "docs/acquisition/"
    "WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"
)
TARGET_GIT_BLOB_SHA1 = "3ede8efbd32c00bd0623924879a645964bd622ee"

PICTORIAL_UPSTREAM_REVISION = "56f44523f76efdcec813e67b38ee550e49b16f48"
PICTORIAL_UPSTREAM_TREE = "3626999bc9c8be4d31f3028c37c74cf544576d15"
AGILE_UPSTREAM_REVISION = "27f50f7e6b618ea14d74dd4037f9e7c60218b16c"
AGILE_UPSTREAM_TREE = "5622442d5ff74d21b2cb4349f255d08380f3d69d"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "6f02d618c575f2440c0f1812c5d0d3bd98c7a5254ec7ab2dae83c84ab85f74eb",
    ADMISSION_WORKFLOW: "fe8a9dcc05adbfdf2a5e06c912a6e8835a028a5dea670d6491746cb795a9270b",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "4fa977235329c1b05d7a0899c2dec994789c2263f49ffdfae6f588483d75a008",
    ADMISSION_WORKFLOW: "fc7cddfdd874acb86bca4da06e70644a181a2a6b8d02574d69ea4fdf9b6f5791",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

PICTORIAL_AGILE_FULL_IMPORT_CONTRACT_AUTHORIZATION = (
    "EXACT_ONE_FILE_ONE_TIME_NEW_AUTHORITY"
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

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_minimax_five_finding_repair
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_minimax_five_finding_repair

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        return prior._topology()
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile inherited policy topology is missing or stale: "
            f"{exc}"
        )


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(policy_base)


def _activate_contract() -> None:
    try:
        existing = prior.EXPECTED_WORKFLOW_SHA256
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile inherited contract topology is missing or stale: "
            f"{exc}"
        )
    if not isinstance(existing, dict):
        base.fail(
            "Pictorial/Agile inherited contract topology is malformed: "
            "EXPECTED_WORKFLOW_SHA256 is not a dict"
        )
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if PRIOR_POLICY_PATH not in paths:
        base.fail(
            "Pictorial/Agile authorization requires the canonical "
            "MiniMax five-finding policy"
        )
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile authorization base policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _validate_target_candidate(candidate: base.RepositoryView) -> None:
    data = candidate.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != TARGET_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile full-import contract drifted: "
            f"{TARGET_PATH}: expected={TARGET_GIT_BLOB_SHA1} actual={actual}"
        )


def _delegate_inherited_exact_delta(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    """Preserve predecessor authority exactly; never widen it here."""
    try:
        expected = prior._require_exact_delta_minimax_five_finding_repair
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile inherited exact-delta topology is missing or stale: "
            f"{exc}"
        )
    if PRIOR_REQUIRE_EXACT_DELTA is not expected:
        base.fail("Pictorial/Agile inherited exact-delta delegate drifted")
    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _require_exact_delta_pictorial_agile(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed = impl._changed_paths(candidate, policy_base)
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile inherited change detector is missing or stale: "
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
                "Pictorial/Agile authorization bootstrap delta must be exactly "
                "the policy wrapper plus two workflows: "
                + ("; ".join(detail) if detail else "delta mismatch")
            )
        if TARGET_PATH in changed:
            base.fail(
                "Pictorial/Agile contract cannot transition before "
                "authorization policy activation"
            )
        _delegate_inherited_exact_delta(candidate, policy_base)
        return

    if TARGET_PATH in changed:
        if TARGET_PATH in base_paths:
            base.fail(
                "Pictorial/Agile full-import contract is frozen after "
                "canonicalization"
            )
        if changed != {TARGET_PATH}:
            unexpected = sorted(changed - {TARGET_PATH})
            base.fail(
                "Pictorial/Agile contract canonicalization delta must be "
                "exactly one file"
                + (": unexpected=" + ",".join(unexpected) if unexpected else "")
            )
        _validate_target_candidate(candidate)
        return

    _delegate_inherited_exact_delta(candidate, policy_base)


def _compare_base_controlled_pictorial_agile(
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
                    "Pictorial/Agile workflow candidate drifted: "
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
                    "Pictorial/Agile "
                    f"{phase} trusted-base workflow drifted: {relative}: "
                    f"expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "Pictorial/Agile steady-state workflow changed: "
                    f"{relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_pictorial_agile(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Pictorial/Agile policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail(
                    "Pictorial/Agile wrapper unexpectedly exists in bootstrap base"
                )
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail(
                    "Pictorial/Agile steady-state base is missing wrapper"
                )
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("Pictorial/Agile steady-state policy wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        actual_candidate = _sha256(candidate_bytes)
        if actual_candidate != expected_candidate:
            base.fail(
                "Pictorial/Agile controlled workflow candidate drifted: "
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
                "Pictorial/Agile controlled workflow "
                f"{phase} base drifted: {relative}: "
                f"expected={expected_base} actual={actual_base}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(
                "Pictorial/Agile steady-state workflow changed: "
                f"{relative}"
            )

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        try:
            prior._verify_extension_paths_minimax_five_finding_repair(
                candidate,
                policy_base,
                delegated,
            )
        except AttributeError as exc:
            base.fail(
                "Pictorial/Agile inherited extension topology is missing or stale: "
                f"{exc}"
            )


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    try:
        controlled_paths = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile execution extension topology is missing or stale: "
            f"{exc}"
        )
    _verify_extension_paths_pictorial_agile(
        candidate,
        policy_base,
        controlled_paths,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    try:
        controlled_paths = desktop.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile desktop extension topology is missing or stale: "
            f"{exc}"
        )
    _verify_extension_paths_pictorial_agile(
        candidate,
        policy_base,
        controlled_paths,
    )


def _validate_allowed_paths_pictorial_agile(
    paths: set[str],
    stage: str,
) -> None:
    delegated = set(paths)
    delegated.discard(TARGET_PATH)
    PRIOR_VALIDATE_ALLOWED_PATHS(delegated, stage)


def _verify_policy_files(view: base.RepositoryView) -> None:
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen MiniMax five-finding policy drifted in repository view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    try:
        prior._verify_policy_files(view)
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile inherited policy-file topology is missing or stale: "
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
                prior._require_exact_delta_minimax_five_finding_repair,
                "exact-delta",
            ),
            (
                base.compare_base_controlled,
                prior._compare_base_controlled_minimax_five_finding_repair,
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
                prior._validate_allowed_paths_minimax_five_finding_repair,
                "tracked-path",
            ),
            (shell.verify_policy_files, prior._verify_policy_files, "policy-file"),
            (shell.print_success, prior._print_success, "success-printer"),
        )
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile pre-bind topology is missing or stale: "
            f"{exc}"
        )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile pre-bind {label} hook drifted")


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    try:
        if PRIOR_REQUIRE_EXACT_DELTA is not prior._require_exact_delta_minimax_five_finding_repair:
            base.fail("Pictorial/Agile inherited exact-delta delegate drifted")
        if retention.IMPL_REQUIRE_EXACT_DELTA is not _require_exact_delta_pictorial_agile:
            base.fail("Pictorial/Agile exact-delta delegate drifted")
        retention._require_exact_delta_hook_identity(
            retention._require_exact_delta_retention,
            "pictorial-agile-full-import-authorization-overlay",
        )
        if shell.validate_allowed_paths is not _validate_allowed_paths_pictorial_agile:
            base.fail("Pictorial/Agile tracked-path hook drifted")
        if base.compare_base_controlled is not _compare_base_controlled_pictorial_agile:
            base.fail("Pictorial/Agile base-control hook drifted")
        if shell.verify_policy_files is not _verify_policy_files:
            base.fail("Pictorial/Agile policy-file hook drifted")
        if desktop.verify_extension_controlled_paths is not _verify_desktop_extension_paths:
            base.fail("Pictorial/Agile desktop extension hook drifted")
        if execution.verify_extension_controlled_paths is not _verify_execution_extension_paths:
            base.fail("Pictorial/Agile execution extension hook drifted")
        if shell.print_success is not _print_success:
            base.fail("Pictorial/Agile success-printer hook drifted")
        if POLICY_SCRIPT not in desktop.EXTENSION_CONTROLLED_PATHS:
            base.fail("Pictorial/Agile desktop controlled-path registration drifted")
        if POLICY_SCRIPT not in execution.EXTENSION_CONTROLLED_PATHS:
            base.fail("Pictorial/Agile execution controlled-path registration drifted")
        if _PRIOR_PRINT_SUCCESS is None or _PRIOR_PRINT_SUCCESS is not prior._print_success:
            base.fail("Pictorial/Agile prior success-printer delegate drifted")
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile overlay identity topology is missing or stale: "
            f"{exc}"
        )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior canonical success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(
        "pictorial_agile_full_import_contract_authorization="
        f"{PICTORIAL_AGILE_FULL_IMPORT_CONTRACT_AUTHORIZATION}"
    )
    print(f"inherited_policy_authority={INHERITED_POLICY_AUTHORITY}")
    print(f"policy_runtime_class={POLICY_RUNTIME_CLASS}")
    print(f"pictorial_agile_full_import_contract_target={TARGET_PATH}")
    print(f"pictorial_agile_full_import_contract_blob={TARGET_GIT_BLOB_SHA1}")
    print(f"pictorial_upstream_revision={PICTORIAL_UPSTREAM_REVISION}")
    print(f"pictorial_upstream_tree={PICTORIAL_UPSTREAM_TREE}")
    print(f"agile_upstream_revision={AGILE_UPSTREAM_REVISION}")
    print(f"agile_upstream_tree={AGILE_UPSTREAM_TREE}")
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
        underlying_printer = prior._print_success
        if not callable(underlying_printer):
            base.fail("prior canonical success printer is unavailable")
        desktop_paths = desktop.EXTENSION_CONTROLLED_PATHS
        execution_paths = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(
            "Pictorial/Agile installer topology is missing or stale: "
            f"{exc}"
        )

    _PRIOR_PRINT_SUCCESS = underlying_printer
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_pictorial_agile
    base.compare_base_controlled = _compare_base_controlled_pictorial_agile
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(desktop_paths) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(execution_paths) | {POLICY_SCRIPT}
    )
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths
    shell.validate_allowed_paths = _validate_allowed_paths_pictorial_agile
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
                "Pictorial/Agile authorization workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_activation_topology() -> None:
    """Prove inherited contract activation reads topology before mutation."""
    original = prior.EXPECTED_WORKFLOW_SHA256
    try:
        delattr(prior, "EXPECTED_WORKFLOW_SHA256")
        base.expect_failure_matching(
            "Pictorial/Agile activation missing topology",
            "inherited contract topology is missing or stale",
            _activate_contract,
        )
        prior.EXPECTED_WORKFLOW_SHA256 = ()
        base.expect_failure_matching(
            "Pictorial/Agile activation malformed topology",
            "inherited contract topology is malformed",
            _activate_contract,
        )
    finally:
        prior.EXPECTED_WORKFLOW_SHA256 = original
    _activate_contract()


def _selftest_bootstrap_delta() -> None:
    root = Path(__file__).resolve().parents[2]
    repository_view = base.LocalRepositoryView(root)
    prior_bytes = repository_view.read_bytes(
        PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES
    )
    base_files = {
        PRIOR_POLICY_PATH: prior_bytes,
        FOUNDATION_WORKFLOW: b"prior-foundation",
        ADMISSION_WORKFLOW: b"prior-admission",
    }
    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"pictorial-agile-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"new-admission"

    _require_exact_delta_pictorial_agile(
        _memory_view(candidate_files),
        _memory_view(base_files),
    )

    mixed = dict(candidate_files)
    mixed[TARGET_PATH] = b"not part of bootstrap\n"
    base.expect_failure_matching(
        "Pictorial/Agile mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_pictorial_agile,
        _memory_view(mixed),
        _memory_view(base_files),
    )


def _selftest_target_transition() -> None:
    global TARGET_GIT_BLOB_SHA1
    target = b"exact-pictorial-agile-import-contract-fixture\n"
    original = TARGET_GIT_BLOB_SHA1
    TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(target)
    try:
        base_files = {
            PRIOR_POLICY_PATH: b"canonical-prior-policy",
            POLICY_SCRIPT: b"canonical-pictorial-agile-policy",
        }
        candidate_files = dict(base_files)
        candidate_files[TARGET_PATH] = target
        _require_exact_delta_pictorial_agile(
            _memory_view(candidate_files),
            _memory_view(base_files),
        )

        wrong = dict(base_files)
        wrong[TARGET_PATH] = b"wrong\n"
        base.expect_failure_matching(
            "Pictorial/Agile wrong-blob rejection",
            "contract drifted",
            _require_exact_delta_pictorial_agile,
            _memory_view(wrong),
            _memory_view(base_files),
        )

        extra = dict(candidate_files)
        extra["docs/acquisition/UNAUTHORIZED_PICTORIAL_AGILE.md"] = b"extra\n"
        base.expect_failure_matching(
            "Pictorial/Agile extra-path rejection",
            "canonicalization delta must be exactly one file",
            _require_exact_delta_pictorial_agile,
            _memory_view(extra),
            _memory_view(base_files),
        )

        frozen_base = dict(candidate_files)
        frozen_candidate = dict(frozen_base)
        frozen_candidate[TARGET_PATH] = target + b"drift\n"
        base.expect_failure_matching(
            "Pictorial/Agile post-canonical mutation rejection",
            "frozen after canonicalization",
            _require_exact_delta_pictorial_agile,
            _memory_view(frozen_candidate),
            _memory_view(frozen_base),
        )
    finally:
        TARGET_GIT_BLOB_SHA1 = original


def _selftest_allowlist_projection() -> None:
    global PRIOR_VALIDATE_ALLOWED_PATHS
    seen: list[tuple[set[str], str]] = []
    original = PRIOR_VALIDATE_ALLOWED_PATHS

    def capture(paths: set[str], stage: str) -> None:
        seen.append((set(paths), stage))

    PRIOR_VALIDATE_ALLOWED_PATHS = capture
    try:
        _validate_allowed_paths_pictorial_agile(
            {"README.md", TARGET_PATH},
            "fixture-stage",
        )
        if seen != [({"README.md"}, "fixture-stage")]:
            base.fail(
                "Pictorial/Agile allowlist projection drifted: "
                f"{seen}"
            )
    finally:
        PRIOR_VALIDATE_ALLOWED_PATHS = original


def _selftest_inherited_authority_boundary() -> None:
    """Prove inherited authority is preserved exactly, not newly widened."""
    global PRIOR_REQUIRE_EXACT_DELTA

    original_global = PRIOR_REQUIRE_EXACT_DELTA
    original_attr = prior._require_exact_delta_minimax_five_finding_repair
    candidate = _memory_view({"README.md": b"candidate\n"})
    policy_base = _memory_view({"README.md": b"base\n"})
    seen: list[str] = []

    def accept(
        candidate_view: base.RepositoryView,
        base_view: base.RepositoryView,
    ) -> None:
        del candidate_view, base_view
        seen.append("accepted-by-predecessor")

    def reject(
        candidate_view: base.RepositoryView,
        base_view: base.RepositoryView,
    ) -> None:
        del candidate_view, base_view
        base.fail("sentinel predecessor rejection")

    try:
        prior._require_exact_delta_minimax_five_finding_repair = accept
        PRIOR_REQUIRE_EXACT_DELTA = accept
        _delegate_inherited_exact_delta(candidate, policy_base)
        if seen != ["accepted-by-predecessor"]:
            base.fail(
                "Pictorial/Agile inherited-authority delegation did not reach "
                "the exact predecessor"
            )

        prior._require_exact_delta_minimax_five_finding_repair = reject
        PRIOR_REQUIRE_EXACT_DELTA = reject
        base.expect_failure_matching(
            "Pictorial/Agile predecessor rejection propagation",
            "sentinel predecessor rejection",
            _delegate_inherited_exact_delta,
            candidate,
            policy_base,
        )

        PRIOR_REQUIRE_EXACT_DELTA = accept
        prior._require_exact_delta_minimax_five_finding_repair = reject
        base.expect_failure_matching(
            "Pictorial/Agile inherited delegate identity tamper",
            "inherited exact-delta delegate drifted",
            _delegate_inherited_exact_delta,
            candidate,
            policy_base,
        )
    finally:
        PRIOR_REQUIRE_EXACT_DELTA = original_global
        prior._require_exact_delta_minimax_five_finding_repair = original_attr


def _selftest_overlay_identity() -> None:
    """Prove every new overlay hook and registration fails closed on tamper."""
    global _PRIOR_PRINT_SUCCESS

    _require_overlay_identity()
    shell, retention, _, desktop, execution = _topology()

    hook_cases = (
        (
            retention,
            "IMPL_REQUIRE_EXACT_DELTA",
            PRIOR_REQUIRE_EXACT_DELTA,
            "exact-delta delegate drifted",
        ),
        (
            base,
            "compare_base_controlled",
            prior._compare_base_controlled_minimax_five_finding_repair,
            "base-control hook drifted",
        ),
        (
            desktop,
            "verify_extension_controlled_paths",
            prior._verify_desktop_extension_paths,
            "desktop extension hook drifted",
        ),
        (
            execution,
            "verify_extension_controlled_paths",
            prior._verify_execution_extension_paths,
            "execution extension hook drifted",
        ),
        (
            shell,
            "validate_allowed_paths",
            PRIOR_VALIDATE_ALLOWED_PATHS,
            "tracked-path hook drifted",
        ),
        (
            shell,
            "verify_policy_files",
            prior._verify_policy_files,
            "policy-file hook drifted",
        ),
        (
            shell,
            "print_success",
            prior._print_success,
            "success-printer hook drifted",
        ),
    )
    for owner, attribute, replacement, expected_message in hook_cases:
        installed = getattr(owner, attribute)
        setattr(owner, attribute, replacement)
        try:
            base.expect_failure_matching(
                f"Pictorial/Agile overlay {attribute} tamper",
                expected_message,
                _require_overlay_identity,
            )
        finally:
            setattr(owner, attribute, installed)

    original_desktop_paths = desktop.EXTENSION_CONTROLLED_PATHS
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(original_desktop_paths) - {POLICY_SCRIPT}
    )
    try:
        base.expect_failure_matching(
            "Pictorial/Agile desktop registration tamper",
            "desktop controlled-path registration drifted",
            _require_overlay_identity,
        )
    finally:
        desktop.EXTENSION_CONTROLLED_PATHS = original_desktop_paths

    original_execution_paths = execution.EXTENSION_CONTROLLED_PATHS
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(original_execution_paths) - {POLICY_SCRIPT}
    )
    try:
        base.expect_failure_matching(
            "Pictorial/Agile execution registration tamper",
            "execution controlled-path registration drifted",
            _require_overlay_identity,
        )
    finally:
        execution.EXTENSION_CONTROLLED_PATHS = original_execution_paths

    original_printer = _PRIOR_PRINT_SUCCESS
    _PRIOR_PRINT_SUCCESS = None
    try:
        base.expect_failure_matching(
            "Pictorial/Agile prior printer delegate tamper",
            "prior success-printer delegate drifted",
            _require_overlay_identity,
        )
    finally:
        _PRIOR_PRINT_SUCCESS = original_printer

    original_validate = shell.validate_allowed_paths
    delattr(shell, "validate_allowed_paths")
    try:
        base.expect_failure_matching(
            "Pictorial/Agile overlay missing-attribute topology",
            "overlay identity topology is missing or stale",
            _require_overlay_identity,
        )
    finally:
        shell.validate_allowed_paths = original_validate

    _require_overlay_identity()


def _selftest_prebind_identity() -> None:
    """Prove each expected predecessor hook is identity-checked before rebinding."""
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
        prior._require_exact_delta_minimax_five_finding_repair,
        prior._compare_base_controlled_minimax_five_finding_repair,
        prior._verify_desktop_extension_paths,
        prior._verify_execution_extension_paths,
        prior._validate_allowed_paths_minimax_five_finding_repair,
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
            (
                retention,
                "IMPL_REQUIRE_EXACT_DELTA",
                _require_exact_delta_pictorial_agile,
                "pre-bind exact-delta hook drifted",
            ),
            (
                base,
                "compare_base_controlled",
                _compare_base_controlled_pictorial_agile,
                "pre-bind base-control hook drifted",
            ),
            (
                desktop,
                "verify_extension_controlled_paths",
                _verify_desktop_extension_paths,
                "pre-bind desktop-extension hook drifted",
            ),
            (
                execution,
                "verify_extension_controlled_paths",
                _verify_execution_extension_paths,
                "pre-bind execution-extension hook drifted",
            ),
            (
                shell,
                "validate_allowed_paths",
                _validate_allowed_paths_pictorial_agile,
                "pre-bind tracked-path hook drifted",
            ),
            (
                shell,
                "verify_policy_files",
                _verify_policy_files,
                "pre-bind policy-file hook drifted",
            ),
            (
                shell,
                "print_success",
                _print_success,
                "pre-bind success-printer hook drifted",
            ),
        )

        for owner, attribute, replacement, expected_message in cases:
            predecessor_value = getattr(owner, attribute)
            setattr(owner, attribute, replacement)
            try:
                base.expect_failure_matching(
                    f"Pictorial/Agile pre-bind {attribute} tamper",
                    expected_message,
                    _require_prebind_identity,
                    shell,
                    retention,
                    desktop,
                    execution,
                )
            finally:
                setattr(owner, attribute, predecessor_value)

        original_validate = shell.validate_allowed_paths
        delattr(shell, "validate_allowed_paths")
        try:
            base.expect_failure_matching(
                "Pictorial/Agile pre-bind missing-attribute topology",
                "pre-bind topology is missing or stale",
                _require_prebind_identity,
                shell,
                retention,
                desktop,
                execution,
            )
        finally:
            shell.validate_allowed_paths = original_validate
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
    prior.selftest()
    _install_policy()
    _selftest_workflow_binding()
    _selftest_activation_topology()
    _selftest_bootstrap_delta()
    _selftest_target_transition()
    _selftest_allowlist_projection()
    _selftest_inherited_authority_boundary()
    _selftest_overlay_identity()
    _selftest_prebind_identity()
    _require_overlay_identity()

    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={impl.CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Pictorial/Agile import-contract authorization self-tests: PASS")


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
