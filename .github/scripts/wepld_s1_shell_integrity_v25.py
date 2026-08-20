#!/usr/bin/env python3
"""Authorize one exact Harness H0 research-document bundle over canonical v24.

This wrapper does not authorize Harness implementation, source/dependency
admission, roadmap mutation, or S1-013+. It authorizes only:

1. the one-time v24->v25 policy/workflow bootstrap; and
2. after v25 is canonical, one exact addition of the frozen Harness Program
   research/falsification document bundle.

After that exact bundle becomes canonical, those document paths refreeze and
ordinary inherited candidate semantics continue through canonical v24.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v25.py"
PRIOR_V24_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v24.py"
EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1 = "21aa8b4fe46d3f25d108fa4fd9988ff273fc5334"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
S1_CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "4f03f0ecf07b30e3b5b2c8cdf62a6f7047fcd4f219894ae188b50e1f6dc83b6f",
    ADMISSION_WORKFLOW: "bca7fe623f22dfedb1f360cf931341ddd41f40f8b8f433f0fbd3361f9c889092",
    S1_CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS = frozenset(
    {FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

RESEARCH_DOC_BLOBS = {
    "docs/acquisition/HARNESS_PROGRAM_DONOR_CANDIDATES_2026-08-20.md":
        "0934b118fba8e20fdb87deca471bc1d0355d8d53",
    "docs/acquisition/WEPLD_HARNESS_ARCHITECTURE_AND_FALSIFICATION_DOSSIER_2026-08-20.md":
        "93725e65906d5e65ff55992ae6aa68c8240b13e5",
    "docs/acquisition/WEPLD_HARNESS_PROGRAM_CONTINUATION_HANDOFF_2026-08-20.md":
        "db26cca7637d6616ac95863a789d27aa0ee4d822",
    "docs/acquisition/WEPLD_HARNESS_H0_THESIS_TOURNAMENT_CONTRACT_2026-08-20.md":
        "73b752d6add47f51cdfe78f99be5fe4454f6a94c",
    "docs/acquisition/WEPLD_HARNESS_H0_EVALUATION_DONOR_RECONNAISSANCE_2026-08-20.md":
        "181baf7988ff7e9c1fee1836318d80dc2e0f48eb",
    "docs/acquisition/WEPLD_HARNESS_H0_EVIDENCE_AND_RUNNER_CONTRACT_2026-08-20.md":
        "5c52ca59ee0c9dccc54e5456ea10cd4fc242d508",
    "docs/acquisition/WEPLD_HARNESS_H0_RUNNER_DECISION_REVIEW_2026-08-20.md":
        "cd097f79de90d721a5d710d6f4f88aa3728d2725",
    "docs/acquisition/WEPLD_HARNESS_H0_SCREENING_FIXTURE_AND_RECIPE_BOUNDARY_2026-08-20.md":
        "f044eb2104b31d797d443338518f9aab9ae95e68",
}
RESEARCH_DOC_PATHS = frozenset(RESEARCH_DOC_BLOBS)

HARNESS_RESEARCH_BUNDLE_AUTHORIZED = "EXACT_ONE_TIME"
HARNESS_PROGRAM = "GO_FOR_RESEARCH_ONLY"
H0_IMPLEMENTATION = "NOT_STARTED"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
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


def _bind_prior_v24_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v24.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen v24 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen v24 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v24_runner_before_import()
import wepld_s1_shell_integrity_v24 as v24  # noqa: E402

PRIOR_V24_WORKFLOW_SHA256 = dict(v24.EXPECTED_WORKFLOW_SHA256)
v23 = v24.v23
v22 = v24.v22
v19 = v24.v19
shell = v24.shell
PRIOR_V24_REQUIRE_EXACT_DELTA = v24._require_exact_delta_v24


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V24_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen v24 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v24._verify_policy_files(view)


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(policy_base)


def _changed_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> set[str]:
    candidate_entries = {entry.path: entry.mode for entry in candidate.entries()}
    base_entries = {entry.path: entry.mode for entry in policy_base.entries()}
    changed: set[str] = set(candidate_entries) ^ set(base_entries)
    for relative in set(candidate_entries) & set(base_entries):
        if candidate_entries[relative] != base_entries[relative]:
            changed.add(relative)
            continue
        if candidate.tree_identity(relative) != policy_base.tree_identity(relative):
            if candidate.read_bytes(
                relative, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES):
                changed.add(relative)
    return changed


def _doc_blob(view: base.RepositoryView, relative: str) -> str:
    return _git_blob_sha1(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))


def _verify_exact_research_bundle(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    base_paths = _paths(policy_base)
    already_present = sorted(base_paths & RESEARCH_DOC_PATHS)
    if already_present:
        base.fail(
            "Harness H0 research bundle is one-time only; trusted base already "
            "contains research path(s): " + ", ".join(already_present)
        )

    candidate_paths = _paths(candidate)
    missing = sorted(RESEARCH_DOC_PATHS - candidate_paths)
    if missing:
        base.fail(
            "Harness H0 research bundle candidate is incomplete; missing: "
            + ", ".join(missing)
        )

    for relative, expected in sorted(RESEARCH_DOC_BLOBS.items()):
        actual = _doc_blob(candidate, relative)
        if actual != expected:
            base.fail(
                "Harness H0 research document drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _require_exact_delta_v25(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)

    if _is_bootstrap_base(policy_base):
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            return
        PRIOR_V24_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    if changed == set(RESEARCH_DOC_PATHS):
        _verify_exact_research_bundle(candidate, policy_base)
        return

    PRIOR_V24_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_v25(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "v25 Harness-research workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )

            expected_base = (
                PRIOR_V24_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"v25 Harness-research {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "v25 Harness-research steady-state workflow changed: "
                    f"{relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_v25(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    for relative in sorted(controlled_paths):
        if relative == POLICY_SCRIPT:
            if relative not in candidate_paths:
                base.fail("v25 Harness-research policy wrapper is missing from candidate")
            if bootstrap:
                if relative in base_paths:
                    base.fail(
                        "v25 Harness-research bootstrap wrapper unexpectedly exists "
                        "in trusted base"
                    )
            else:
                if relative not in base_paths:
                    base.fail(
                        "v25 Harness-research steady-state trusted base is missing wrapper"
                    )
                if candidate.read_bytes(
                    relative, base.MAX_POLICY_FILE_BYTES
                ) != policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES):
                    base.fail("v25 Harness-research steady-state policy wrapper changed")
            continue

        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "v25 Harness-research controlled workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_V24_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"v25 Harness-research controlled workflow {phase} base drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    f"v25 Harness-research steady-state workflow changed: {relative}"
                )
            continue

        if relative == v24.POLICY_SCRIPT:
            actual = _git_blob_sha1(candidate_bytes)
            if actual != EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1:
                base.fail(
                    "frozen v24 wrapper drifted in candidate: "
                    f"expected={EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1} actual={actual}"
                )
            if candidate_bytes != base_bytes:
                base.fail("frozen v24 wrapper changed")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled inherited policy path changed: {relative}")


def _verify_execution_extension_controlled_paths_v25(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_v25(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_controlled_paths_v25(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_v25(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("v25 prior success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    if stage == v19.S1_011_STAGE:
        print(
            "harness_h0_research_bundle_authorized="
            f"{HARNESS_RESEARCH_BUNDLE_AUTHORIZED}"
        )
        print(f"harness_program={HARNESS_PROGRAM}")
        print(f"h0_implementation={H0_IMPLEMENTATION}")
        print(f"source_admission={SOURCE_ADMISSION}")
        print(f"dependency_admission={DEPENDENCY_ADMISSION}")
        print(f"s1_013_plus={S1_013_PLUS}")


def _propagate_expected_workflow_hashes() -> None:
    v24.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    for module in v24._workflow_hash_modules():
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256


def _install_v25_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v24._install_v24_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    base.compare_base_controlled = _compare_base_controlled_v25
    v19._require_exact_delta = _require_exact_delta_v25
    shell.prior.verify_extension_controlled_paths = (
        _verify_desktop_extension_controlled_paths_v25
    )
    shell.prior.prior.verify_extension_controlled_paths = (
        _verify_execution_extension_controlled_paths_v25
    )

    _propagate_expected_workflow_hashes()

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
    for relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "v25 Harness-research workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_research_bundle_transition() -> None:
    fixtures = {
        relative: ("fixture:" + relative).encode("utf-8")
        for relative in RESEARCH_DOC_PATHS
    }

    original = globals()["_doc_blob"]
    try:
        def fake_doc_blob(view: base.RepositoryView, relative: str) -> str:
            data = view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
            if data == fixtures[relative]:
                return RESEARCH_DOC_BLOBS[relative]
            return _git_blob_sha1(data)

        globals()["_doc_blob"] = fake_doc_blob

        base_files = {POLICY_SCRIPT: b"v25"}
        candidate_files = dict(base_files)
        candidate_files.update(fixtures)
        _require_exact_delta_v25(
            base.MemoryView(candidate_files),
            base.MemoryView(base_files),
        )

        bad_files = dict(candidate_files)
        bad_path = sorted(RESEARCH_DOC_PATHS)[0]
        bad_files[bad_path] = b"unauthorized-drift"
        base.expect_failure_matching(
            "v25 wrong research document projection",
            "research document drifted",
            _require_exact_delta_v25,
            base.MemoryView(bad_files),
            base.MemoryView(base_files),
        )

        post_base = dict(candidate_files)
        replay = dict(post_base)
        for relative in RESEARCH_DOC_PATHS:
            replay[relative] = b"later-drift:" + relative.encode("utf-8")
        base.expect_failure_matching(
            "v25 research bundle refreezes after canonicalization",
            "one-time only",
            _require_exact_delta_v25,
            base.MemoryView(replay),
            base.MemoryView(post_base),
        )
    finally:
        globals()["_doc_blob"] = original


def _selftest_v25_steady_state() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    current_workflows = {
        relative: view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        for relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS
    }
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    v24_bytes = view.read_bytes(v24.POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)

    steady_files = {
        relative: b"unchanged"
        for relative in base.BASE_CONTROLLED_PATHS
        if relative not in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS
    }
    steady_files.update(current_workflows)
    steady_files[POLICY_SCRIPT] = policy_bytes
    steady_files[v24.POLICY_SCRIPT] = v24_bytes

    steady_base = base.MemoryView(steady_files)
    steady_candidate = base.MemoryView(dict(steady_files))

    if _is_bootstrap_base(steady_base):
        base.fail("v25 steady-state self-test misclassified trusted base")
    _compare_base_controlled_v25(steady_candidate, steady_base)
    _verify_extension_paths_v25(
        steady_candidate,
        steady_base,
        frozenset(
            {
                POLICY_SCRIPT,
                v24.POLICY_SCRIPT,
                FOUNDATION_WORKFLOW,
                ADMISSION_WORKFLOW,
            }
        ),
    )

    mutated = dict(steady_files)
    mutated[POLICY_SCRIPT] = policy_bytes + b"\n# unauthorized steady-state drift\n"
    base.expect_failure_matching(
        "v25 steady-state wrapper drift",
        "steady-state policy wrapper changed",
        _verify_extension_paths_v25,
        base.MemoryView(mutated),
        steady_base,
        frozenset({POLICY_SCRIPT}),
    )

    if not _is_bootstrap_base(base.MemoryView({v24.POLICY_SCRIPT: v24_bytes})):
        base.fail("v25 bootstrap self-test failed to identify pre-v25 base")


def selftest() -> None:
    # v25 changes only the two policy-runner workflow references. Project the
    # v25 workflow identities into inherited v24/v23/... self-tests before
    # running them. PRIOR_V24_WORKFLOW_SHA256 remains the immutable bootstrap
    # base identity captured before projection.
    _propagate_expected_workflow_hashes()
    v24.selftest()
    _install_v25_policy()
    _selftest_workflow_binding()
    _selftest_research_bundle_transition()
    _selftest_v25_steady_state()
    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness H0 research-bundle policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_v25_policy()
    return v24.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
