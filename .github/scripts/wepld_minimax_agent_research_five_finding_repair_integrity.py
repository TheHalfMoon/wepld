#!/usr/bin/env python3
"""Authorize one exact five-finding repair of MiniMax donor research.

This wrapper is a bounded, non-self-authorizing policy transition layered over
the canonical MiniMax review-repair authorization. It authorizes only:

1. this policy/workflow bootstrap; and
2. after canonical activation, one exact repaired research document closing the
   five material findings from the fresh exact-head CodeRabbit review of PR #88:
   - governance-owned bounded long-horizon execution;
   - retry-safe idempotency for externally visible side effects;
   - exact immutable non-reusable permission-scope binding;
   - monotonic DATA_EGRESS_CLASS derivation as stricter data enters; and
   - atomic active-candidate/completion reconciliation.

The previously authorized document blob is retained as an explicit negative
oracle for this repair cycle. The older pre-repair blob remains a historical
negative oracle. This grants no source admission, dependency admission, product
implementation authority, roadmap mutation, H0-014+, H0-SCREEN execution,
model/provider execution, model-weight access, or inference authority.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = (
    ".github/scripts/"
    "wepld_minimax_agent_research_five_finding_repair_integrity.py"
)
PRIOR_POLICY_PATH = (
    ".github/scripts/"
    "wepld_minimax_agent_research_review_repair_integrity.py"
)
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "b49d45abb2115c94a7e3d53889e3cf7a71de4472"


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
            "frozen MiniMax review-repair policy runner drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_minimax_agent_research_review_repair_integrity as prior  # noqa: E402

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

TARGET_PATH = (
    "docs/acquisition/"
    "WEPLD_MINIMAX_UNIVERSAL_AGENT_AUTOMATION_DONOR_RECONNAISSANCE_2026-08-21.md"
)
HISTORICAL_REJECTED_TARGET_GIT_BLOB_SHA1 = (
    "feb054cb2c0897d7c283c8b6a35a0843081c5692"
)
REJECTED_TARGET_GIT_BLOB_SHA1 = "3e19041b0482e9d106e5e839fc6294c53febc649"
TARGET_GIT_BLOB_SHA1 = "aeaed6edc659ccca4da73db488443f7c1f9593ff"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "083a1727006708e4b9141c30bf394d3bd7c195819ac6556d96deecb11953e880",
    ADMISSION_WORKFLOW: "2d9d4558a703c76c97d87660c787c6200953e5b6987eabea4e5797f0beabd2a3",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "6f02d618c575f2440c0f1812c5d0d3bd98c7a5254ec7ab2dae83c84ab85f74eb",
    ADMISSION_WORKFLOW: "fe8a9dcc05adbfdf2a5e06c912a6e8835a028a5dea670d6491746cb795a9270b",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

MINIMAX_AGENT_RESEARCH_FIVE_FINDING_REPAIR_AUTHORIZATION = (
    "EXACT_FIVE_MAJOR_REVIEW_FINDING_REPAIR"
)
REVIEW_REPAIR_SOURCE_HEAD = "16d0569c98b952a34a989c9e3248e9404402f8ff"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
PRODUCT_IMPLEMENTATION_AUTHORITY = "NONE"
ROADMAP_MUTATION = "NONE"
H0_014_PLUS = "NOT_STARTED"
H0_SCREEN_EXECUTION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_minimax_review_repair
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_minimax_review_repair

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    """Resolve the inherited owners used by this overlay or fail closed."""
    try:
        root = prior.prior.prior.prior
        shell = root.shell
        retention = root.retention
        impl = root.impl
        desktop = shell.prior
        execution = desktop.prior
    except AttributeError as exc:
        base.fail(
            "MiniMax five-finding inherited policy topology is missing or stale: "
            f"{exc}"
        )
    return shell, retention, impl, desktop, execution


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(policy_base)


def _activate_contract() -> None:
    try:
        prior.TARGET_GIT_BLOB_SHA1 = TARGET_GIT_BLOB_SHA1
        prior.REJECTED_TARGET_GIT_BLOB_SHA1 = REJECTED_TARGET_GIT_BLOB_SHA1
        prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
        prior._activate_contract()
    except AttributeError as exc:
        base.fail(
            "MiniMax five-finding inherited contract topology is missing or stale: "
            f"{exc}"
        )


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if PRIOR_POLICY_PATH not in paths:
        base.fail(
            "MiniMax five-finding repair requires the canonical review-repair policy"
        )
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "MiniMax five-finding repair base review-repair policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_exact_delta_minimax_five_finding_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed = impl._changed_paths(candidate, policy_base)
    except AttributeError as exc:
        base.fail(
            "MiniMax five-finding inherited change detector is missing or stale: "
            f"{exc}"
        )
    bootstrap = _is_bootstrap_base(policy_base)

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
                "MiniMax five-finding repair bootstrap delta must be exactly "
                "the new repair policy wrapper plus two workflows: "
                + ("; ".join(detail) if detail else "delta mismatch")
            )
        if TARGET_PATH in changed:
            base.fail(
                "MiniMax five-finding document repair cannot transition before "
                "five-finding repair policy activation"
            )
        PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_minimax_five_finding_repair(
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
                    "MiniMax five-finding workflow candidate drifted: "
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
                    "MiniMax five-finding repair "
                    f"{phase} trusted-base workflow drifted: {relative}: "
                    f"expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "MiniMax five-finding repair steady-state workflow changed: "
                    f"{relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_minimax_five_finding_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("MiniMax five-finding repair policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail(
                    "MiniMax five-finding repair wrapper unexpectedly exists "
                    "in bootstrap base"
                )
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail(
                    "MiniMax five-finding repair steady-state base is missing wrapper"
                )
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail(
                    "MiniMax five-finding repair steady-state policy wrapper changed"
                )

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        actual_candidate = _sha256(candidate_bytes)
        if actual_candidate != expected_candidate:
            base.fail(
                "MiniMax five-finding controlled workflow candidate drifted: "
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
                "MiniMax five-finding controlled workflow "
                f"{phase} base drifted: {relative}: "
                f"expected={expected_base} actual={actual_base}"
            )

        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(
                "MiniMax five-finding repair steady-state workflow changed: "
                f"{relative}"
            )

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        prior._verify_extension_paths_minimax_review_repair(
            candidate,
            policy_base,
            delegated,
        )


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_minimax_five_finding_repair(
        candidate,
        policy_base,
        execution.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_minimax_five_finding_repair(
        candidate,
        policy_base,
        desktop.EXTENSION_CONTROLLED_PATHS,
    )


def _validate_allowed_paths_minimax_five_finding_repair(
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
            "frozen MiniMax review-repair policy drifted in repository view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._verify_policy_files(view)


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    try:
        if retention.IMPL_REQUIRE_EXACT_DELTA is not _require_exact_delta_minimax_five_finding_repair:
            base.fail("MiniMax five-finding exact-delta delegate drifted")
        retention._require_exact_delta_hook_identity(
            retention._require_exact_delta_retention,
            "minimax-agent-research-five-finding-repair-overlay",
        )
        if shell.validate_allowed_paths is not _validate_allowed_paths_minimax_five_finding_repair:
            base.fail("MiniMax five-finding tracked-path hook drifted")
        if base.compare_base_controlled is not _compare_base_controlled_minimax_five_finding_repair:
            base.fail("MiniMax five-finding base-control hook drifted")
        if shell.verify_policy_files is not _verify_policy_files:
            base.fail("MiniMax five-finding policy-file hook drifted")
        if desktop.verify_extension_controlled_paths is not _verify_desktop_extension_paths:
            base.fail("MiniMax five-finding desktop extension hook drifted")
        if execution.verify_extension_controlled_paths is not _verify_execution_extension_paths:
            base.fail("MiniMax five-finding execution extension hook drifted")
        if shell.print_success is not _print_success:
            base.fail("MiniMax five-finding success-printer hook drifted")
        if POLICY_SCRIPT not in desktop.EXTENSION_CONTROLLED_PATHS:
            base.fail("MiniMax five-finding desktop controlled-path registration drifted")
        if POLICY_SCRIPT not in execution.EXTENSION_CONTROLLED_PATHS:
            base.fail("MiniMax five-finding execution controlled-path registration drifted")
        if _PRIOR_PRINT_SUCCESS is None or _PRIOR_PRINT_SUCCESS is not prior._PRIOR_PRINT_SUCCESS:
            base.fail("MiniMax five-finding prior success-printer delegate drifted")
    except AttributeError as exc:
        base.fail(
            "MiniMax five-finding overlay identity topology is missing or stale: "
            f"{exc}"
        )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior MiniMax research success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(
        "minimax_agent_research_five_finding_repair_authorization="
        f"{MINIMAX_AGENT_RESEARCH_FIVE_FINDING_REPAIR_AUTHORIZATION}"
    )
    print(f"minimax_agent_research_five_finding_repair_target={TARGET_PATH}")
    print(
        "minimax_agent_research_five_finding_repair_historical_rejected_blob="
        f"{HISTORICAL_REJECTED_TARGET_GIT_BLOB_SHA1}"
    )
    print(
        "minimax_agent_research_five_finding_repair_rejected_blob="
        f"{REJECTED_TARGET_GIT_BLOB_SHA1}"
    )
    print(
        "minimax_agent_research_five_finding_repair_target_blob="
        f"{TARGET_GIT_BLOB_SHA1}"
    )
    print(
        "minimax_agent_research_five_finding_repair_source_head="
        f"{REVIEW_REPAIR_SOURCE_HEAD}"
    )
    print(f"source_admission={SOURCE_ADMISSION}")
    print(f"dependency_admission={DEPENDENCY_ADMISSION}")
    print(f"product_implementation_authority={PRODUCT_IMPLEMENTATION_AUTHORITY}")
    print(f"roadmap_mutation={ROADMAP_MUTATION}")
    print(f"h0_014_plus={H0_014_PLUS}")
    print(f"h0_screen_execution={H0_SCREEN_EXECUTION}")
    print(f"model_provider_execution={MODEL_PROVIDER_EXECUTION}")
    print(f"model_weight_access={MODEL_WEIGHT_ACCESS}")
    print(f"model_inference={MODEL_INFERENCE}")


def _require_prebind_identity(shell: Any, retention: Any, desktop: Any, execution: Any) -> None:
    """Prove the canonical predecessor owns every hook before rebinding it."""
    try:
        expected = (
            (retention.IMPL_REQUIRE_EXACT_DELTA, prior._require_exact_delta_minimax_review_repair, "exact-delta"),
            (base.compare_base_controlled, prior._compare_base_controlled_minimax_review_repair, "base-control"),
            (desktop.verify_extension_controlled_paths, prior._verify_desktop_extension_paths, "desktop-extension"),
            (execution.verify_extension_controlled_paths, prior._verify_execution_extension_paths, "execution-extension"),
            (shell.validate_allowed_paths, prior._validate_allowed_paths_minimax_review_repair, "tracked-path"),
            (shell.verify_policy_files, prior._verify_policy_files, "policy-file"),
            (shell.print_success, prior._print_success, "success-printer"),
        )
    except AttributeError as exc:
        base.fail(
            "MiniMax five-finding pre-bind topology is missing or stale: "
            f"{exc}"
        )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"MiniMax five-finding pre-bind {label} hook drifted")


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
        underlying_printer = prior._PRIOR_PRINT_SUCCESS
        if underlying_printer is None or not callable(underlying_printer):
            base.fail("prior MiniMax research success printer is unavailable")

        desktop_paths = desktop.EXTENSION_CONTROLLED_PATHS
        execution_paths = execution.EXTENSION_CONTROLLED_PATHS
    except AttributeError as exc:
        base.fail(
            "MiniMax five-finding installer topology is missing or stale: "
            f"{exc}"
        )

    _PRIOR_PRINT_SUCCESS = underlying_printer
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_minimax_five_finding_repair
    base.compare_base_controlled = _compare_base_controlled_minimax_five_finding_repair
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(set(desktop_paths) | {POLICY_SCRIPT})
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(set(execution_paths) | {POLICY_SCRIPT})
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths
    shell.validate_allowed_paths = _validate_allowed_paths_minimax_five_finding_repair
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
                "MiniMax five-finding repair workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


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
    candidate_files[POLICY_SCRIPT] = b"five-finding-repair-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"new-admission"

    _require_exact_delta_minimax_five_finding_repair(
        _memory_view(candidate_files),
        _memory_view(base_files),
    )

    mixed = dict(candidate_files)
    mixed[TARGET_PATH] = b"not part of bootstrap"
    base.expect_failure_matching(
        "MiniMax five-finding mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_minimax_five_finding_repair,
        _memory_view(mixed),
        _memory_view(base_files),
    )


def _selftest_target_transition() -> None:
    global TARGET_GIT_BLOB_SHA1, REJECTED_TARGET_GIT_BLOB_SHA1
    repaired = b"exact-five-finding-repaired-minimax-research-fixture\n"
    rejected = b"previously-authorized-minimax-research-fixture\n"
    original_target = TARGET_GIT_BLOB_SHA1
    original_rejected = REJECTED_TARGET_GIT_BLOB_SHA1
    prior_original_target = prior.TARGET_GIT_BLOB_SHA1
    prior_original_rejected = prior.REJECTED_TARGET_GIT_BLOB_SHA1
    TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(repaired)
    REJECTED_TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(rejected)
    prior.TARGET_GIT_BLOB_SHA1 = TARGET_GIT_BLOB_SHA1
    prior.REJECTED_TARGET_GIT_BLOB_SHA1 = REJECTED_TARGET_GIT_BLOB_SHA1
    try:
        base_files = {
            PRIOR_POLICY_PATH: b"canonical-review-repair-policy",
            POLICY_SCRIPT: b"canonical-five-finding-policy",
        }

        candidate_files = dict(base_files)
        candidate_files[TARGET_PATH] = repaired
        _require_exact_delta_minimax_five_finding_repair(
            _memory_view(candidate_files),
            _memory_view(base_files),
        )

        old = dict(base_files)
        old[TARGET_PATH] = rejected
        base.expect_failure_matching(
            "MiniMax previous-blob rejection",
            "remains rejected after review",
            _require_exact_delta_minimax_five_finding_repair,
            _memory_view(old),
            _memory_view(base_files),
        )

        wrong = dict(base_files)
        wrong[TARGET_PATH] = b"wrong\n"
        base.expect_failure_matching(
            "MiniMax five-finding wrong-blob rejection",
            "document drifted",
            _require_exact_delta_minimax_five_finding_repair,
            _memory_view(wrong),
            _memory_view(base_files),
        )

        extra = dict(candidate_files)
        extra["docs/acquisition/UNAUTHORIZED_MINIMAX_FIVE_FINDING_REPAIR.md"] = (
            b"extra\n"
        )
        base.expect_failure_matching(
            "MiniMax five-finding extra-path rejection",
            "canonicalization delta must be exactly one file",
            _require_exact_delta_minimax_five_finding_repair,
            _memory_view(extra),
            _memory_view(base_files),
        )

        frozen_base = dict(candidate_files)
        frozen_candidate = dict(frozen_base)
        frozen_candidate[TARGET_PATH] = repaired + b"drift\n"
        base.expect_failure_matching(
            "MiniMax five-finding post-canonical mutation rejection",
            "frozen after canonicalization",
            _require_exact_delta_minimax_five_finding_repair,
            _memory_view(frozen_candidate),
            _memory_view(frozen_base),
        )
    finally:
        TARGET_GIT_BLOB_SHA1 = original_target
        REJECTED_TARGET_GIT_BLOB_SHA1 = original_rejected
        prior.TARGET_GIT_BLOB_SHA1 = prior_original_target
        prior.REJECTED_TARGET_GIT_BLOB_SHA1 = prior_original_rejected


def _selftest_allowlist_projection() -> None:
    global PRIOR_VALIDATE_ALLOWED_PATHS
    seen: list[tuple[set[str], str]] = []
    original = PRIOR_VALIDATE_ALLOWED_PATHS

    def capture(paths: set[str], stage: str) -> None:
        seen.append((set(paths), stage))

    PRIOR_VALIDATE_ALLOWED_PATHS = capture
    try:
        _validate_allowed_paths_minimax_five_finding_repair(
            {"README.md", TARGET_PATH},
            "fixture-stage",
        )
        if seen != [({"README.md"}, "fixture-stage")]:
            base.fail(
                "MiniMax five-finding allowlist projection drifted: "
                f"{seen}"
            )
    finally:
        PRIOR_VALIDATE_ALLOWED_PATHS = original


def _selftest_overlay_identity() -> None:
    _require_overlay_identity()
    shell, retention, _, desktop, execution = _topology()

    cases = (
        (
            retention,
            "IMPL_REQUIRE_EXACT_DELTA",
            PRIOR_REQUIRE_EXACT_DELTA,
            "exact-delta delegate drifted",
        ),
        (
            shell,
            "validate_allowed_paths",
            PRIOR_VALIDATE_ALLOWED_PATHS,
            "tracked-path hook drifted",
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
            "print_success",
            prior._print_success,
            "success-printer hook drifted",
        ),
    )
    for owner, attribute, replacement, expected_message in cases:
        installed = getattr(owner, attribute)
        setattr(owner, attribute, replacement)
        try:
            base.expect_failure_matching(
                f"MiniMax five-finding {attribute} hook identity mismatch",
                expected_message,
                _require_overlay_identity,
            )
        finally:
            setattr(owner, attribute, installed)

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
    try:
        retention.IMPL_REQUIRE_EXACT_DELTA = prior._require_exact_delta_minimax_review_repair
        base.compare_base_controlled = prior._compare_base_controlled_minimax_review_repair
        desktop.verify_extension_controlled_paths = prior._verify_desktop_extension_paths
        execution.verify_extension_controlled_paths = prior._verify_execution_extension_paths
        shell.validate_allowed_paths = prior._validate_allowed_paths_minimax_review_repair
        shell.verify_policy_files = prior._verify_policy_files
        shell.print_success = prior._print_success
        _require_prebind_identity(shell, retention, desktop, execution)

        shell.print_success = _print_success
        base.expect_failure_matching(
            "MiniMax five-finding pre-bind hook mismatch",
            "pre-bind success-printer hook drifted",
            _require_prebind_identity,
            shell,
            retention,
            desktop,
            execution,
        )
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
    _selftest_bootstrap_delta()
    _selftest_target_transition()
    _selftest_allowlist_projection()
    _selftest_overlay_identity()
    _selftest_prebind_identity()
    shell, retention, impl, desktop, execution = _topology()
    del shell, retention, desktop, execution
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={impl.CANONICAL_REPOSITORY} "
            f"actual={base.REPOSITORY}"
        )
    print("wepld MiniMax five-finding repair authorization self-tests: PASS")


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
