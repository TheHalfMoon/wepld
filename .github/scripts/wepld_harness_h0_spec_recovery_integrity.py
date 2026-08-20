#!/usr/bin/env python3
"""Authorize one exact second-stage review-finding recovery of the Harness H0 Spec Kit package.

This wrapper is intentionally layered over the canonical H0 Spec Kit review-repair policy.
It grants no Harness implementation, source/dependency admission, roadmap mutation,
confirmatory execution, H0 promotion, or S1-013+ authority. It permits only:

1. one bounded recovery-policy/workflow bootstrap over the exact canonical repair policy; and
2. after canonical activation of this recovery wrapper, one exact ten-file
   `specs/002-harness-h0-screening/` package whose manual-recovery denominator is
   mechanically defined after independent review of the prior corrected package.

After canonicalization, the recovered package refreezes and unrelated changes continue
through the prior canonical policy chain.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_harness_h0_spec_recovery_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_harness_h0_spec_repair_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "ad42030d166a77f70616fb0996ff42d63623817b"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"

RECOVERED_SPEC_KIT_BLOBS = {
    "specs/002-harness-h0-screening/constitution.md":
        "bf530e264f4d4876beb2ea8c8913df3ffdd6f1da",
    "specs/002-harness-h0-screening/spec.md":
        "8cdf4a72e5589e73bcf50f1247eaf64f598196a5",
    "specs/002-harness-h0-screening/clarify.md":
        "159634d0effc44816a45a7bb567e376afdec1845",
    "specs/002-harness-h0-screening/plan.md":
        "560e09b0369fb322bea08c0f51cdd76e9239ef1e",
    "specs/002-harness-h0-screening/checklists/requirements.md":
        "5375a3e615a7b6d9d0026c15ce5265173439c235",
    "specs/002-harness-h0-screening/analyze.md":
        "dfbb8ff6fd378ed54a66c54423411c45ca1cdc1b",
    "specs/002-harness-h0-screening/tasks.md":
        "87a848b5de0dfcd689e00c65f0f0934e5013beff",
    "specs/002-harness-h0-screening/acceptance.md":
        "73176e4dd3551c90a79f1e1c3063cd15c4927a34",
    "specs/002-harness-h0-screening/ponytail.md":
        "e9351ef6df7d76676c290ca694dbe68f242d0cb3",
    "specs/002-harness-h0-screening/source-acquisition.md":
        "dec73a131c1343565f4aea4f583344acc90ff2b5",
}
RECOVERED_SPEC_KIT_PATHS = frozenset(RECOVERED_SPEC_KIT_BLOBS)

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "8a162fce1dbdf3cb8f6eb3b02d81d794531b8d663f50dc70d566b6bfca414088",
    ADMISSION_WORKFLOW: "7696209008f1cd0e3fd91ea389e0d80be05d008b12daf0ed55824a6329adee22",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "6b8beb1beca2257d7a28643f5a24bd150fbc0500c5d9bd8d81955f554179e615",
    ADMISSION_WORKFLOW: "a4270ae106c5f708686d7c13861f5058574d9ba25233df0cd4d9ac85809cb5e2",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})

HARNESS_H0_SPEC_RECOVERY_AUTHORIZED = "EXACT_REVIEW_FINDING_RECOVERY_PACKAGE"
HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED = "NO"
HARNESS_SOURCE_ADMISSION = "NONE"
HARNESS_DEPENDENCY_ADMISSION = "NONE"
ROADMAP_MUTATION = "NONE"
S1_013_PLUS = "NOT_STARTED"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_prior_policy_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_harness_h0_spec_repair_integrity.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen H0 Spec Kit repair policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0 Spec Kit repair policy runner drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_harness_h0_spec_repair_integrity as prior  # noqa: E402

shell = prior.shell
PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_repair


def _activate_recovered_contract() -> None:
    prior.CORRECTED_SPEC_KIT_BLOBS = dict(RECOVERED_SPEC_KIT_BLOBS)
    prior.CORRECTED_SPEC_KIT_PATHS = frozenset(RECOVERED_SPEC_KIT_PATHS)
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior._activate_corrected_contract()


def _verify_policy_files(view: base.RepositoryView) -> None:
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0 Spec Kit repair policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._verify_policy_files(view)


def _is_recovery_bootstrap_base(view: base.RepositoryView) -> bool:
    paths = _paths(view)
    return POLICY_SCRIPT not in paths and PRIOR_POLICY_PATH in paths


def _changed_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> set[str]:
    return prior._changed_paths(candidate, policy_base)


def _require_prior_repair_base(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if PRIOR_POLICY_PATH not in paths:
        base.fail("H0 Spec Kit recovery requires the canonical prior repair policy")
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "H0 Spec Kit recovery base repair policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._require_prior_h0_base(view)
    if paths & set(RECOVERED_SPEC_KIT_PATHS):
        base.fail("H0 Spec Kit recovery bootstrap requires package paths to remain absent")


def _require_exact_delta_recovery(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)
    bootstrap = _is_recovery_bootstrap_base(policy_base)

    if bootstrap:
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            _require_prior_repair_base(policy_base)
            return
        if changed & set(RECOVERED_SPEC_KIT_PATHS):
            base.fail(
                "recovered H0 Spec Kit package cannot transition before recovery policy activation"
            )
        PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_recovery(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_recovery_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            candidate_hash = _sha256(candidate_bytes)
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            if candidate_hash != expected_candidate:
                base.fail(
                    "H0 Spec Kit recovery workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={candidate_hash}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
                if bootstrap
                else expected_candidate
            )
            base_hash = _sha256(base_bytes)
            if base_hash != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"H0 Spec Kit recovery {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={base_hash}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"H0 Spec Kit recovery steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_recovery(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_recovery_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("H0 Spec Kit recovery policy wrapper is missing from candidate")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("H0 Spec Kit recovery wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("H0 Spec Kit recovery steady-state base is missing wrapper")
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("H0 Spec Kit recovery steady-state policy wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        candidate_hash = _sha256(candidate_bytes)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if candidate_hash != expected_candidate:
            base.fail(
                "H0 Spec Kit recovery controlled workflow candidate drifted: "
                f"{relative}: expected={expected_candidate} actual={candidate_hash}"
            )
        expected_base = (
            PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
            if bootstrap
            else expected_candidate
        )
        base_hash = _sha256(base_bytes)
        if base_hash != expected_base:
            phase = "bootstrap" if bootstrap else "steady-state"
            base.fail(
                f"H0 Spec Kit recovery controlled workflow {phase} base drifted: "
                f"{relative}: expected={expected_base} actual={base_hash}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"H0 Spec Kit recovery steady-state workflow changed: {relative}")

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        prior._verify_extension_paths_repair(candidate, policy_base, delegated)


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_recovery(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_recovery(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior H0 Spec Kit repair success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"harness_h0_spec_recovery_authorized={HARNESS_H0_SPEC_RECOVERY_AUTHORIZED}")
    print(
        "harness_h0_screen_implementation_authorized="
        f"{HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED}"
    )
    print(f"harness_source_admission={HARNESS_SOURCE_ADMISSION}")
    print(f"harness_dependency_admission={HARNESS_DEPENDENCY_ADMISSION}")
    print(f"harness_roadmap_mutation={ROADMAP_MUTATION}")
    print(f"s1_013_plus={S1_013_PLUS}")


def _install_recovery_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    _activate_recovered_contract()
    prior._install_repair_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    base.compare_base_controlled = _compare_base_controlled_recovery
    prior.prior.prior.v24.v19._require_exact_delta = _require_exact_delta_recovery
    shell.prior.verify_extension_controlled_paths = _verify_desktop_extension_paths
    shell.prior.prior.verify_extension_controlled_paths = _verify_execution_extension_paths

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success
    _INSTALLED = True


def _selftest_workflow_binding() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for relative in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "H0 Spec Kit recovery workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _fixture_canonical_base() -> tuple[dict[str, bytes], dict[bytes, str]]:
    files, identities = prior._fixture_canonical_base()
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    files[PRIOR_POLICY_PATH] = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    return files, identities


def _selftest_recovery_bootstrap_delta() -> None:
    base_files, _ = _fixture_canonical_base()
    base_files[FOUNDATION_WORKFLOW] = b"repair-foundation"
    base_files[ADMISSION_WORKFLOW] = b"repair-admission"

    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"recovery-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"recovery-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"recovery-admission"
    trees = {
        POLICY_SCRIPT: "a" * 40,
        FOUNDATION_WORKFLOW: "b" * 40,
        ADMISSION_WORKFLOW: "c" * 40,
    }

    _require_exact_delta_recovery(
        base.MemoryView(candidate_files, trees=trees),
        base.MemoryView(base_files),
    )


def _selftest_recovered_spec_transition() -> None:
    base_files, identities = _fixture_canonical_base()
    base_files[POLICY_SCRIPT] = b"recovery-policy"

    fixtures = {
        relative: ("recovered:" + relative).encode("utf-8")
        for relative in RECOVERED_SPEC_KIT_PATHS
    }
    for relative, data in fixtures.items():
        identities[data] = RECOVERED_SPEC_KIT_BLOBS[relative]

    candidate_files = dict(base_files)
    candidate_files.update(fixtures)
    trees = {
        relative: f"{index:040x}"
        for index, relative in enumerate(sorted(RECOVERED_SPEC_KIT_PATHS), start=30)
    }

    original_prior = prior.prior._git_blob_sha1
    try:
        def fake_prior_git_blob_sha1(data: bytes) -> str:
            if data in identities:
                return identities[data]
            return original_prior(data)

        prior.prior._git_blob_sha1 = fake_prior_git_blob_sha1
        _require_exact_delta_recovery(
            base.MemoryView(candidate_files, trees=trees),
            base.MemoryView(base_files),
        )

        wrong_path = "specs/002-harness-h0-screening/spec.md"
        wrong = dict(candidate_files)
        wrong[wrong_path] = b"stale-or-wrong-recovery"
        base.expect_failure_matching(
            "H0 Spec Kit recovery wrong recovered blob",
            "candidate drifted",
            _require_exact_delta_recovery,
            base.MemoryView(wrong, trees=trees),
            base.MemoryView(base_files),
        )
    finally:
        prior.prior._git_blob_sha1 = original_prior


def _selftest_steady_state_wrapper() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    base_view = base.MemoryView({POLICY_SCRIPT: policy_bytes})
    if _is_recovery_bootstrap_base(base_view):
        base.fail("H0 Spec Kit recovery steady-state self-test misclassified base")
    mutated = base.MemoryView({POLICY_SCRIPT: policy_bytes + b"\n# drift\n"})
    base.expect_failure_matching(
        "H0 Spec Kit recovery wrapper refreeze",
        "steady-state policy wrapper changed",
        _verify_extension_paths_recovery,
        mutated,
        base_view,
        frozenset({POLICY_SCRIPT}),
    )


def selftest() -> None:
    _activate_recovered_contract()
    prior.selftest()
    _install_recovery_policy()
    _selftest_workflow_binding()
    _selftest_recovery_bootstrap_delta()
    _selftest_recovered_spec_transition()
    _selftest_steady_state_wrapper()
    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness H0 Spec Kit recovery policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_recovery_policy()
    return prior.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
