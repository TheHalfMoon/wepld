#!/usr/bin/env python3
"""Authorize one exact review-finding repair of MiniMax donor research.

This wrapper is a bounded, non-self-authorizing policy transition layered over
canonical MiniMax agent research authorization. It authorizes only:

1. this policy/workflow bootstrap; and
2. after canonical activation, one exact repaired research document.

The pre-repair reviewed document is retained as an explicit negative oracle.
This grants no source admission, dependency admission, product implementation
authority, roadmap mutation, H0-014+, H0-SCREEN execution, model/provider
execution, model-weight access, or inference authority.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = (
    ".github/scripts/"
    "wepld_minimax_agent_research_review_repair_integrity.py"
)
PRIOR_POLICY_PATH = ".github/scripts/wepld_minimax_agent_research_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "82e03388670599f8b3cb2aa7bff2ebeaa7dd4761"


def _bind_prior_policy_before_import() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    header = f"blob {len(data)}\0".encode("ascii")
    actual = hashlib.sha1(header + data).hexdigest()
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen MiniMax agent research policy runner drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_minimax_agent_research_integrity as prior  # noqa: E402

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

TARGET_PATH = (
    "docs/acquisition/"
    "WEPLD_MINIMAX_UNIVERSAL_AGENT_AUTOMATION_DONOR_RECONNAISSANCE_2026-08-21.md"
)
REJECTED_TARGET_GIT_BLOB_SHA1 = "feb054cb2c0897d7c283c8b6a35a0843081c5692"
TARGET_GIT_BLOB_SHA1 = "3e19041b0482e9d106e5e839fc6294c53febc649"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "f7342ef02ff83b20170246f0bfb09ce9c48006b914410ba3b62f9919d3e7f97c",
    ADMISSION_WORKFLOW: "19ff5fc3a48470939c7ada75b0d103075bd8a1ae2490783c533fe0e64f46c379",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "c581fef7322ab364b196c3b1759c564b71c5ce37a13545a808879ee1e5562d3a",
    ADMISSION_WORKFLOW: "6ef424253d43934b821f27ac4df24d3beae79f49a81b2088ef6d67cf27593c14",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

MINIMAX_AGENT_RESEARCH_REVIEW_REPAIR_AUTHORIZATION = (
    "EXACT_TWO_MAJOR_REVIEW_FINDING_REPAIR"
)
REVIEW_REPAIR_SOURCE_HEAD = "701fcf71185b859d825863a5dfddf55dab9dd0aa"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
PRODUCT_IMPLEMENTATION_AUTHORITY = "NONE"
ROADMAP_MUTATION = "NONE"
H0_014_PLUS = "NOT_STARTED"
H0_SCREEN_EXECUTION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_minimax_research
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_minimax_research

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


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


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(policy_base)


def _activate_contract() -> None:
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior.prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior.prior.prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior.prior.prior.retention.EXPECTED_WORKFLOW_SHA256 = dict(
        EXPECTED_WORKFLOW_SHA256
    )
    prior.prior.prior.retention.impl.EXPECTED_WORKFLOW_SHA256 = dict(
        EXPECTED_WORKFLOW_SHA256
    )


def _validate_target_candidate(candidate: base.RepositoryView) -> None:
    data = candidate.read_bytes(TARGET_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual == REJECTED_TARGET_GIT_BLOB_SHA1:
        base.fail(
            "pre-repair MiniMax research blob remains rejected after review: "
            f"{TARGET_PATH}: rejected={REJECTED_TARGET_GIT_BLOB_SHA1}"
        )
    if actual != TARGET_GIT_BLOB_SHA1:
        base.fail(
            "repaired MiniMax universal-agent donor research document drifted: "
            f"{TARGET_PATH}: expected={TARGET_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_exact_delta_minimax_review_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = prior.prior.prior.impl._changed_paths(candidate, policy_base)
    base_paths = _paths(policy_base)
    bootstrap = _is_bootstrap_base(policy_base)

    if bootstrap:
        if changed == set(BOOTSTRAP_DELTA_PATHS):
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
                "MiniMax research review-repair bootstrap delta must be exactly "
                "the repair policy wrapper plus two workflows: "
                + ("; ".join(detail) if detail else "delta mismatch")
            )
        PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    if TARGET_PATH in changed:
        if TARGET_PATH in base_paths:
            base.fail(
                "repaired MiniMax donor research document is frozen "
                "after canonicalization"
            )
        if changed != {TARGET_PATH}:
            unexpected = sorted(changed - {TARGET_PATH})
            detail = (
                "unexpected=" + ",".join(unexpected)
                if unexpected
                else "delta mismatch"
            )
            base.fail(
                "MiniMax review-repair canonicalization delta must be exactly "
                f"one file: {detail}"
            )
        _validate_target_candidate(candidate)
        return

    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_minimax_review_repair(
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
                    "MiniMax review-repair workflow candidate drifted: "
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
                    "MiniMax review-repair "
                    f"{phase} trusted-base workflow drifted: {relative}: "
                    f"expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "MiniMax review-repair steady-state workflow changed: "
                    f"{relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_minimax_review_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("MiniMax review-repair policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail(
                    "MiniMax review-repair wrapper unexpectedly exists "
                    "in bootstrap base"
                )
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail(
                    "MiniMax review-repair steady-state base is missing wrapper"
                )
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail(
                    "MiniMax review-repair steady-state policy wrapper changed"
                )

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        actual_candidate = _sha256(candidate_bytes)
        if actual_candidate != expected_candidate:
            base.fail(
                "MiniMax review-repair controlled workflow candidate drifted: "
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
                "MiniMax review-repair controlled workflow "
                f"{phase} base drifted: {relative}: "
                f"expected={expected_base} actual={actual_base}"
            )

        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(
                "MiniMax review-repair steady-state workflow changed: "
                f"{relative}"
            )

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        prior._verify_extension_paths_minimax_research(
            candidate,
            policy_base,
            delegated,
        )


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_minimax_review_repair(
        candidate,
        policy_base,
        prior.prior.prior.shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_minimax_review_repair(
        candidate,
        policy_base,
        prior.prior.prior.shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _validate_allowed_paths_minimax_review_repair(
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
            "frozen MiniMax agent research policy drifted in repository view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._verify_policy_files(view)


def _require_overlay_identity() -> None:
    if (
        prior.prior.prior.retention.IMPL_REQUIRE_EXACT_DELTA
        is not _require_exact_delta_minimax_review_repair
    ):
        base.fail("MiniMax review-repair exact-delta delegate drifted")
    prior.prior.prior.retention._require_exact_delta_hook_identity(
        prior.prior.prior.retention._require_exact_delta_retention,
        "minimax-agent-research-review-repair-overlay",
    )
    if (
        prior.prior.prior.shell.validate_allowed_paths
        is not _validate_allowed_paths_minimax_review_repair
    ):
        base.fail("MiniMax review-repair tracked-path hook drifted")
    if (
        base.compare_base_controlled
        is not _compare_base_controlled_minimax_review_repair
    ):
        base.fail("MiniMax review-repair base-control hook drifted")
    if prior.prior.prior.shell.verify_policy_files is not _verify_policy_files:
        base.fail("MiniMax review-repair policy-file hook drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior MiniMax research success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(
        "minimax_agent_research_review_repair_authorization="
        f"{MINIMAX_AGENT_RESEARCH_REVIEW_REPAIR_AUTHORIZATION}"
    )
    print(f"minimax_agent_research_review_repair_target={TARGET_PATH}")
    print(
        "minimax_agent_research_review_repair_rejected_blob="
        f"{REJECTED_TARGET_GIT_BLOB_SHA1}"
    )
    print(
        "minimax_agent_research_review_repair_target_blob="
        f"{TARGET_GIT_BLOB_SHA1}"
    )
    print(
        "minimax_agent_research_review_repair_source_head="
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


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity()
        return

    _activate_contract()
    prior._install_policy()
    prior._require_overlay_identity()
    _PRIOR_PRINT_SUCCESS = prior.prior.prior.shell.print_success

    prior.prior.prior.retention.IMPL_REQUIRE_EXACT_DELTA = (
        _require_exact_delta_minimax_review_repair
    )
    base.compare_base_controlled = _compare_base_controlled_minimax_review_repair

    prior.prior.prior.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(prior.prior.prior.shell.prior.EXTENSION_CONTROLLED_PATHS)
        | {POLICY_SCRIPT}
    )
    prior.prior.prior.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(prior.prior.prior.shell.prior.prior.EXTENSION_CONTROLLED_PATHS)
        | {POLICY_SCRIPT}
    )
    prior.prior.prior.shell.prior.verify_extension_controlled_paths = (
        _verify_desktop_extension_paths
    )
    prior.prior.prior.shell.prior.prior.verify_extension_controlled_paths = (
        _verify_execution_extension_paths
    )

    prior.prior.prior.shell.validate_allowed_paths = (
        _validate_allowed_paths_minimax_review_repair
    )
    prior.prior.prior.shell.verify_policy_files = _verify_policy_files
    prior.prior.prior.shell.print_success = _print_success

    _INSTALLED = True
    _require_overlay_identity()


def _selftest_workflow_binding() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for relative in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "MiniMax review-repair workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_bootstrap_delta() -> None:
    base_files = {
        PRIOR_POLICY_PATH: b"canonical-minimax-agent-research-policy",
        FOUNDATION_WORKFLOW: b"prior-foundation",
        ADMISSION_WORKFLOW: b"prior-admission",
    }
    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"minimax-agent-review-repair-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"new-admission"

    _require_exact_delta_minimax_review_repair(
        _memory_view(candidate_files),
        _memory_view(base_files),
    )

    mixed = dict(candidate_files)
    mixed[TARGET_PATH] = b"not part of bootstrap"
    base.expect_failure_matching(
        "MiniMax review-repair mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_minimax_review_repair,
        _memory_view(mixed),
        _memory_view(base_files),
    )


def _selftest_target_transition() -> None:
    global TARGET_GIT_BLOB_SHA1, REJECTED_TARGET_GIT_BLOB_SHA1
    repaired = b"exact-repaired-minimax-research-fixture\n"
    rejected = b"reviewed-pre-repair-minimax-research-fixture\n"
    original_target = TARGET_GIT_BLOB_SHA1
    original_rejected = REJECTED_TARGET_GIT_BLOB_SHA1
    TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(repaired)
    REJECTED_TARGET_GIT_BLOB_SHA1 = _git_blob_sha1(rejected)
    try:
        base_files = {POLICY_SCRIPT: b"canonical-review-repair-policy"}

        candidate_files = dict(base_files)
        candidate_files[TARGET_PATH] = repaired
        _require_exact_delta_minimax_review_repair(
            _memory_view(candidate_files),
            _memory_view(base_files),
        )

        old = dict(base_files)
        old[TARGET_PATH] = rejected
        base.expect_failure_matching(
            "MiniMax pre-repair reviewed-blob rejection",
            "remains rejected after review",
            _require_exact_delta_minimax_review_repair,
            _memory_view(old),
            _memory_view(base_files),
        )

        wrong = dict(base_files)
        wrong[TARGET_PATH] = b"wrong\n"
        base.expect_failure_matching(
            "MiniMax repaired research wrong-blob rejection",
            "document drifted",
            _require_exact_delta_minimax_review_repair,
            _memory_view(wrong),
            _memory_view(base_files),
        )

        extra = dict(candidate_files)
        extra["docs/acquisition/UNAUTHORIZED_MINIMAX_REPAIR.md"] = b"extra\n"
        base.expect_failure_matching(
            "MiniMax repaired research extra-path rejection",
            "canonicalization delta must be exactly one file",
            _require_exact_delta_minimax_review_repair,
            _memory_view(extra),
            _memory_view(base_files),
        )

        frozen_base = dict(candidate_files)
        frozen_candidate = dict(frozen_base)
        frozen_candidate[TARGET_PATH] = repaired + b"drift\n"
        base.expect_failure_matching(
            "MiniMax repaired research post-canonical mutation rejection",
            "frozen after canonicalization",
            _require_exact_delta_minimax_review_repair,
            _memory_view(frozen_candidate),
            _memory_view(frozen_base),
        )
    finally:
        TARGET_GIT_BLOB_SHA1 = original_target
        REJECTED_TARGET_GIT_BLOB_SHA1 = original_rejected


def _selftest_allowlist_projection() -> None:
    global PRIOR_VALIDATE_ALLOWED_PATHS
    seen: list[tuple[set[str], str]] = []
    original = PRIOR_VALIDATE_ALLOWED_PATHS

    def capture(paths: set[str], stage: str) -> None:
        seen.append((set(paths), stage))

    PRIOR_VALIDATE_ALLOWED_PATHS = capture
    try:
        _validate_allowed_paths_minimax_review_repair(
            {"README.md", TARGET_PATH},
            "fixture-stage",
        )
        if seen != [({"README.md"}, "fixture-stage")]:
            base.fail(
                "MiniMax review-repair allowlist projection drifted: "
                f"{seen}"
            )
    finally:
        PRIOR_VALIDATE_ALLOWED_PATHS = original


def _selftest_overlay_identity() -> None:
    _require_overlay_identity()

    installed_delta = prior.prior.prior.retention.IMPL_REQUIRE_EXACT_DELTA
    prior.prior.prior.retention.IMPL_REQUIRE_EXACT_DELTA = PRIOR_REQUIRE_EXACT_DELTA
    try:
        base.expect_failure_matching(
            "MiniMax review-repair exact-delta hook identity mismatch",
            "exact-delta delegate drifted",
            _require_overlay_identity,
        )
    finally:
        prior.prior.prior.retention.IMPL_REQUIRE_EXACT_DELTA = installed_delta

    installed_allowlist = prior.prior.prior.shell.validate_allowed_paths
    prior.prior.prior.shell.validate_allowed_paths = PRIOR_VALIDATE_ALLOWED_PATHS
    try:
        base.expect_failure_matching(
            "MiniMax review-repair tracked-path hook identity mismatch",
            "tracked-path hook drifted",
            _require_overlay_identity,
        )
    finally:
        prior.prior.prior.shell.validate_allowed_paths = installed_allowlist

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
    if base.REPOSITORY != prior.prior.prior.impl.CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={prior.prior.prior.impl.CANONICAL_REPOSITORY} "
            f"actual={base.REPOSITORY}"
        )
    print("wepld MiniMax review-repair authorization self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_policy()
    return prior.prior.prior.retention.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
