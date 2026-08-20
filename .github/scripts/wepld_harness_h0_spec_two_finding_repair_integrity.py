#!/usr/bin/env python3
"""Authorize one exact two-finding repair of the Harness H0 Spec Kit package.

This wrapper is intentionally layered over the canonical H0 Spec Kit four-finding
repair policy. It grants no Harness implementation, source/dependency admission,
roadmap mutation, confirmatory execution, H0 promotion, or S1-013+ authority.

It permits only:

1. one bounded two-finding-repair policy/workflow bootstrap over the exact canonical
   four-finding repair policy; and
2. after canonical activation of this wrapper, one exact ten-file
   `specs/002-harness-h0-screening/` package that closes the two material findings
   proven by fresh exact-head review of rejected PR #55:
   - normalize the accepted-unauthorized-effect hard-gate key to
     `ACCEPTED_UNAUTHORIZED_EFFECTS`; and
   - normalize H0 Ponytail state under the single `PONYTAIL_FULL` key while
     preserving the distinction between planning review completion and the later
     implementation-boundary closeout.

After canonicalization, the repaired package refreezes and unrelated changes continue
through the prior canonical policy chain.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_harness_h0_spec_two_finding_repair_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_harness_h0_spec_four_finding_repair_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "bb5c84977213973555e59691c8358e56d9e63962"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"

TWO_FINDING_SPEC_KIT_BLOBS = {
    "specs/002-harness-h0-screening/constitution.md":
        "bf530e264f4d4876beb2ea8c8913df3ffdd6f1da",
    "specs/002-harness-h0-screening/spec.md":
        "8cdf4a72e5589e73bcf50f1247eaf64f598196a5",
    "specs/002-harness-h0-screening/clarify.md":
        "159634d0effc44816a45a7bb567e376afdec1845",
    "specs/002-harness-h0-screening/plan.md":
        "36c5b4790f88ad6c8462ee9149dfcc260db3f24c",
    "specs/002-harness-h0-screening/checklists/requirements.md":
        "c840fb33fabbd1b1bfaeff7118329d60ded88539",
    "specs/002-harness-h0-screening/analyze.md":
        "e16d3cb0fbc8941faae6a252c2a2d9379e8856e1",
    "specs/002-harness-h0-screening/tasks.md":
        "b7af4eb48fb31a32dd5e66758d43460e91577517",
    "specs/002-harness-h0-screening/acceptance.md":
        "e156f99152be388757ce8271c492b147245a0073",
    "specs/002-harness-h0-screening/ponytail.md":
        "73c97850b1c25e067281bcb84c2865f1d694c714",
    "specs/002-harness-h0-screening/source-acquisition.md":
        "223c0beb0ee8c41eaab787d8daadeeb8c5a23458",
}
TWO_FINDING_SPEC_KIT_PATHS = frozenset(TWO_FINDING_SPEC_KIT_BLOBS)

# Rejected PR #55 package identities are retained only as negative-oracle constants.
REJECTED_PR55_SPEC_KIT_BLOBS = {
    "specs/002-harness-h0-screening/constitution.md":
        "bf530e264f4d4876beb2ea8c8913df3ffdd6f1da",
    "specs/002-harness-h0-screening/spec.md":
        "8cdf4a72e5589e73bcf50f1247eaf64f598196a5",
    "specs/002-harness-h0-screening/clarify.md":
        "159634d0effc44816a45a7bb567e376afdec1845",
    "specs/002-harness-h0-screening/plan.md":
        "5c04f3f323354e8744dc4392a58ff5abb8ab261f",
    "specs/002-harness-h0-screening/checklists/requirements.md":
        "c840fb33fabbd1b1bfaeff7118329d60ded88539",
    "specs/002-harness-h0-screening/analyze.md":
        "3445d81522680fbd1841659a394a8e299e54622d",
    "specs/002-harness-h0-screening/tasks.md":
        "fdde02d4cc1e4d98d23b48623cbf979e1999ea48",
    "specs/002-harness-h0-screening/acceptance.md":
        "73176e4dd3551c90a79f1e1c3063cd15c4927a34",
    "specs/002-harness-h0-screening/ponytail.md":
        "e9351ef6df7d76676c290ca694dbe68f242d0cb3",
    "specs/002-harness-h0-screening/source-acquisition.md":
        "dec73a131c1343565f4aea4f583344acc90ff2b5",
}

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "33058592087a0e8f44ba05bc27653c2c039a9eae9110a92918f6511ce6d4cd7a",
    ADMISSION_WORKFLOW: "23b370d1e0ff14c04abd9a19d0a087010cfbabda6a0aa5854bdb7863494b6192",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "1c1127ed0bd65d90684e5df82d9d0b8ea1a5b020e1b8b7866811b97444c22db0",
    ADMISSION_WORKFLOW: "389f7edffe655b1aecc0a0f566d9c7e4b3ece3f497249a53b28b73e1302e5fed",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})

HARNESS_H0_SPEC_TWO_FINDING_REPAIR_AUTHORIZED = "EXACT_TWO_REVIEW_FINDING_REPAIR_PACKAGE"
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
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0 Spec Kit four-finding repair policy runner drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_harness_h0_spec_four_finding_repair_integrity as prior  # noqa: E402

shell = prior.shell
PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_four_finding_repair


def _activate_two_finding_contract() -> None:
    prior.FOUR_FINDING_SPEC_KIT_BLOBS = dict(TWO_FINDING_SPEC_KIT_BLOBS)
    prior.FOUR_FINDING_SPEC_KIT_PATHS = frozenset(TWO_FINDING_SPEC_KIT_PATHS)
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior._activate_four_finding_contract()


def _verify_policy_files(view: base.RepositoryView) -> None:
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0 Spec Kit four-finding repair policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._verify_policy_files(view)


def _is_two_finding_bootstrap_base(view: base.RepositoryView) -> bool:
    paths = _paths(view)
    return POLICY_SCRIPT not in paths and PRIOR_POLICY_PATH in paths


def _changed_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> set[str]:
    return prior._changed_paths(candidate, policy_base)


def _require_prior_four_finding_base(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if PRIOR_POLICY_PATH not in paths:
        base.fail("H0 Spec Kit two-finding repair requires the canonical four-finding policy")
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "H0 Spec Kit two-finding repair base four-finding policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._require_prior_recovery_base(view)
    if paths & set(TWO_FINDING_SPEC_KIT_PATHS):
        base.fail(
            "H0 Spec Kit two-finding repair bootstrap requires package paths to remain absent"
        )


def _require_exact_delta_two_finding_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)
    bootstrap = _is_two_finding_bootstrap_base(policy_base)

    if bootstrap:
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            _require_prior_four_finding_base(policy_base)
            return
        if changed & set(TWO_FINDING_SPEC_KIT_PATHS):
            base.fail(
                "two-finding H0 Spec Kit package cannot transition before "
                "two-finding repair policy activation"
            )
        PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_two_finding_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_two_finding_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            candidate_hash = _sha256(candidate_bytes)
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            if candidate_hash != expected_candidate:
                base.fail(
                    "H0 Spec Kit two-finding repair workflow candidate drifted: "
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
                    f"H0 Spec Kit two-finding repair {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={base_hash}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    f"H0 Spec Kit two-finding repair steady-state workflow changed: {relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_two_finding_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_two_finding_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("H0 Spec Kit two-finding repair policy wrapper is missing from candidate")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail(
                    "H0 Spec Kit two-finding repair wrapper unexpectedly exists in bootstrap base"
                )
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail(
                    "H0 Spec Kit two-finding repair steady-state base is missing wrapper"
                )
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("H0 Spec Kit two-finding repair steady-state policy wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        candidate_hash = _sha256(candidate_bytes)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if candidate_hash != expected_candidate:
            base.fail(
                "H0 Spec Kit two-finding repair controlled workflow candidate drifted: "
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
                "H0 Spec Kit two-finding repair controlled workflow "
                f"{phase} base drifted: {relative}: expected={expected_base} actual={base_hash}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(
                f"H0 Spec Kit two-finding repair steady-state workflow changed: {relative}"
            )

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        prior._verify_extension_paths_four_finding_repair(
            candidate, policy_base, delegated
        )


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_two_finding_repair(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_two_finding_repair(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior H0 Spec Kit four-finding repair success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(
        "harness_h0_spec_two_finding_repair_authorized="
        f"{HARNESS_H0_SPEC_TWO_FINDING_REPAIR_AUTHORIZED}"
    )
    print(
        "harness_h0_screen_implementation_authorized="
        f"{HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED}"
    )
    print(f"harness_source_admission={HARNESS_SOURCE_ADMISSION}")
    print(f"harness_dependency_admission={HARNESS_DEPENDENCY_ADMISSION}")
    print(f"harness_roadmap_mutation={ROADMAP_MUTATION}")
    print(f"s1_013_plus={S1_013_PLUS}")


def _install_two_finding_repair_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    _activate_two_finding_contract()
    prior._install_four_finding_repair_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    base.compare_base_controlled = _compare_base_controlled_two_finding_repair
    prior.prior.prior.prior.prior.v24.v19._require_exact_delta = (
        _require_exact_delta_two_finding_repair
    )
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
                "H0 Spec Kit two-finding repair workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _fixture_canonical_base() -> tuple[dict[str, bytes], dict[bytes, str]]:
    files, identities = prior._fixture_canonical_base()
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    files[PRIOR_POLICY_PATH] = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    return files, identities


def _selftest_two_finding_bootstrap_delta() -> None:
    base_files, _ = _fixture_canonical_base()
    base_files[FOUNDATION_WORKFLOW] = b"four-finding-foundation"
    base_files[ADMISSION_WORKFLOW] = b"four-finding-admission"

    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"two-finding-repair-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"two-finding-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"two-finding-admission"
    trees = {
        POLICY_SCRIPT: "a" * 40,
        FOUNDATION_WORKFLOW: "b" * 40,
        ADMISSION_WORKFLOW: "c" * 40,
    }

    _require_exact_delta_two_finding_repair(
        base.MemoryView(candidate_files, trees=trees),
        base.MemoryView(base_files),
    )

    premature = dict(base_files)
    first_path = sorted(TWO_FINDING_SPEC_KIT_PATHS)[0]
    premature[first_path] = b"premature-two-finding-package"
    base.expect_failure_matching(
        "H0 Spec Kit two-finding premature package transition",
        "cannot transition before two-finding repair policy activation",
        _require_exact_delta_two_finding_repair,
        base.MemoryView(premature),
        base.MemoryView(base_files),
    )


def _selftest_rejected_package_is_distinct() -> None:
    if set(REJECTED_PR55_SPEC_KIT_BLOBS) != set(TWO_FINDING_SPEC_KIT_BLOBS):
        base.fail("rejected PR #55 package path set drifted")
    changed = {
        path
        for path in TWO_FINDING_SPEC_KIT_BLOBS
        if TWO_FINDING_SPEC_KIT_BLOBS[path] != REJECTED_PR55_SPEC_KIT_BLOBS[path]
    }
    expected_changed = {
        "specs/002-harness-h0-screening/plan.md",
        "specs/002-harness-h0-screening/analyze.md",
        "specs/002-harness-h0-screening/tasks.md",
        "specs/002-harness-h0-screening/acceptance.md",
        "specs/002-harness-h0-screening/ponytail.md",
        "specs/002-harness-h0-screening/source-acquisition.md",
    }
    if changed != expected_changed:
        base.fail(
            "two-finding repair package identity delta drifted: "
            f"expected={sorted(expected_changed)} actual={sorted(changed)}"
        )


def _selftest_authority_boundaries() -> None:
    expected = {
        "HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED": "NO",
        "HARNESS_SOURCE_ADMISSION": "NONE",
        "HARNESS_DEPENDENCY_ADMISSION": "NONE",
        "ROADMAP_MUTATION": "NONE",
        "S1_013_PLUS": "NOT_STARTED",
    }
    actual = {
        "HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED":
            HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED,
        "HARNESS_SOURCE_ADMISSION": HARNESS_SOURCE_ADMISSION,
        "HARNESS_DEPENDENCY_ADMISSION": HARNESS_DEPENDENCY_ADMISSION,
        "ROADMAP_MUTATION": ROADMAP_MUTATION,
        "S1_013_PLUS": S1_013_PLUS,
    }
    if actual != expected:
        base.fail(f"two-finding repair authority boundary drifted: {actual}")


def _selftest_steady_state_wrapper() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    base_view = base.MemoryView({POLICY_SCRIPT: policy_bytes})
    if _is_two_finding_bootstrap_base(base_view):
        base.fail("H0 Spec Kit two-finding steady-state self-test misclassified base")
    mutated = base.MemoryView({POLICY_SCRIPT: policy_bytes + b"\n# drift\n"})
    base.expect_failure_matching(
        "H0 Spec Kit two-finding wrapper refreeze",
        "steady-state policy wrapper changed",
        _verify_extension_paths_two_finding_repair,
        mutated,
        base_view,
        frozenset({POLICY_SCRIPT}),
    )


def selftest() -> None:
    _activate_two_finding_contract()
    prior.selftest()
    _install_two_finding_repair_policy()
    _selftest_workflow_binding()
    _selftest_two_finding_bootstrap_delta()
    _selftest_rejected_package_is_distinct()
    _selftest_authority_boundaries()
    _selftest_steady_state_wrapper()
    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness H0 Spec Kit two-finding repair policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_two_finding_repair_policy()
    return prior.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
