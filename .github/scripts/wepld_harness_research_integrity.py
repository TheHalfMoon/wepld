#!/usr/bin/env python3
"""Authorize one exact Harness Program research-doc canonicalization over canonical v24.

This wrapper does not authorize Harness implementation, source admission,
dependency admission, roadmap mutation, or S1-013+. It authorizes only:

1. the one-time v24 -> Harness-research policy/workflow bootstrap; and
2. after this wrapper is canonical, one exact seven-file research-doc addition.

After those exact research blobs are canonical, the research paths refreeze and
all other candidate semantics continue through canonical v24.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_harness_research_integrity.py"
PRIOR_V24_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v24.py"
EXPECTED_PRIOR_V24_RUNNER_GIT_BLOB_SHA1 = "21aa8b4fe46d3f25d108fa4fd9988ff273fc5334"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CANONICAL_LEDGER_PATH = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"
EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1 = "d331b7f167fe67ae9061ed553cf0949fab12aae0"

RESEARCH_DOC_BLOBS = {
    "docs/acquisition/HARNESS_PROGRAM_DONOR_CANDIDATES_2026-08-20.md":
        "0934b118fba8e20fdb87deca471bc1d0355d8d53",
    "docs/acquisition/WEPLD_HARNESS_ARCHITECTURE_AND_FALSIFICATION_DOSSIER_2026-08-20.md":
        "93725e65906d5e65ff55992ae6aa68c8240b13e5",
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

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "0924f523923a12b3feac9f6f637d541d4ec38d12d788c87c6ee57af6e1baa695",
    ADMISSION_WORKFLOW: "bf421b63e1142e59e338e99a14d5c76aec194d7d1a9c8b41651b68ed335b7fb4",
    ".github/workflows/s1-contracts.yml": "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS = frozenset(
    {FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

HARNESS_RESEARCH_DOCS_AUTHORIZED = "EXACT_SEVEN_FILE_ONE_TIME"
HARNESS_IMPLEMENTATION_AUTHORIZED = "NO"
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
PRIOR_V24_REQUIRE_EXACT_DELTA = v24._require_exact_delta_v24
shell = v24.shell


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


def _require_reconciled_ledger_base(view: base.RepositoryView) -> None:
    data = view.read_bytes(CANONICAL_LEDGER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1:
        base.fail(
            "Harness research authorization requires canonical reconciled S1 ledger: "
            f"expected={EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1} actual={actual}"
        )


def _validate_research_doc_candidate(candidate: base.RepositoryView) -> None:
    candidate_paths = _paths(candidate)
    missing = sorted(RESEARCH_DOC_PATHS - candidate_paths)
    if missing:
        base.fail(
            "Harness research canonicalization is partial; missing=" + ",".join(missing)
        )
    for relative, expected in sorted(RESEARCH_DOC_BLOBS.items()):
        data = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        actual = _git_blob_sha1(data)
        if actual != expected:
            base.fail(
                "Harness research document candidate drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _require_exact_delta_harness(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)
    base_paths = _paths(policy_base)

    if _is_bootstrap_base(policy_base):
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            _require_reconciled_ledger_base(policy_base)
            return
        PRIOR_V24_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    research_touched = changed & set(RESEARCH_DOC_PATHS)
    if research_touched:
        _require_reconciled_ledger_base(policy_base)
        if base_paths & set(RESEARCH_DOC_PATHS):
            base.fail("Harness research documents are frozen after canonicalization")
        if changed != set(RESEARCH_DOC_PATHS):
            missing = sorted(set(RESEARCH_DOC_PATHS) - changed)
            unexpected = sorted(changed - set(RESEARCH_DOC_PATHS))
            detail: list[str] = []
            if missing:
                detail.append("missing=" + ",".join(missing))
            if unexpected:
                detail.append("unexpected=" + ",".join(unexpected))
            base.fail(
                "Harness research canonicalization delta must be exactly seven files: "
                + ("; ".join(detail) if detail else "delta mismatch")
            )
        _validate_research_doc_candidate(candidate)
        return

    PRIOR_V24_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_harness(
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
                    "Harness research workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )

            expected_base = (
                PRIOR_V24_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"Harness research {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"Harness research steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_harness(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Harness research policy wrapper is missing from candidate")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail(
                    "Harness research bootstrap wrapper unexpectedly exists in trusted base"
                )
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Harness research steady-state trusted base is missing wrapper")
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("Harness research steady-state policy wrapper changed")

    for relative in sorted(BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        actual_candidate = _sha256(candidate_bytes)
        if actual_candidate != expected_candidate:
            base.fail(
                "Harness research controlled workflow candidate drifted: "
                f"{relative}: expected={expected_candidate} actual={actual_candidate}"
            )
        expected_base = (
            PRIOR_V24_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
        )
        actual_base = _sha256(base_bytes)
        if actual_base != expected_base:
            phase = "bootstrap" if bootstrap else "steady-state"
            base.fail(
                f"Harness research controlled workflow {phase} base drifted: "
                f"{relative}: expected={expected_base} actual={actual_base}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"Harness research steady-state workflow changed: {relative}")

    delegated = frozenset(
        set(controlled_paths)
        - {POLICY_SCRIPT}
        - set(BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS)
    )
    if delegated:
        v24._verify_extension_paths_v24(candidate, policy_base, delegated)


def _verify_execution_extension_controlled_paths_harness(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_harness(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_controlled_paths_harness(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_harness(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"harness_research_docs_authorized={HARNESS_RESEARCH_DOCS_AUTHORIZED}")
    print(f"harness_implementation_authorized={HARNESS_IMPLEMENTATION_AUTHORIZED}")
    print(f"harness_source_admission={HARNESS_SOURCE_ADMISSION}")
    print(f"harness_dependency_admission={HARNESS_DEPENDENCY_ADMISSION}")
    print(f"harness_roadmap_mutation={ROADMAP_MUTATION}")
    print(f"s1_013_plus={S1_013_PLUS}")


def _propagate_expected_workflow_hashes() -> None:
    v24.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    for module in v24._workflow_hash_modules():
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256


def _install_harness_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v24._install_v24_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    base.compare_base_controlled = _compare_base_controlled_harness
    v24.v19._require_exact_delta = _require_exact_delta_harness
    shell.prior.verify_extension_controlled_paths = (
        _verify_desktop_extension_controlled_paths_harness
    )
    shell.prior.prior.verify_extension_controlled_paths = (
        _verify_execution_extension_controlled_paths_harness
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
                "Harness research workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_bootstrap_delta() -> None:
    ledger = b"reconciled-ledger-fixture"
    original = globals()["_git_blob_sha1"]
    try:
        def fake_git_blob_sha1(data: bytes) -> str:
            if data == ledger:
                return EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1
            return original(data)

        globals()["_git_blob_sha1"] = fake_git_blob_sha1

        base_files = {
            CANONICAL_LEDGER_PATH: ledger,
            FOUNDATION_WORKFLOW: b"old-foundation",
            ADMISSION_WORKFLOW: b"old-admission",
        }
        candidate_files = dict(base_files)
        candidate_files[POLICY_SCRIPT] = b"harness-policy"
        candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
        candidate_files[ADMISSION_WORKFLOW] = b"new-admission"
        trees = {
            POLICY_SCRIPT: "1" * 40,
            FOUNDATION_WORKFLOW: "2" * 40,
            ADMISSION_WORKFLOW: "3" * 40,
        }
        _require_exact_delta_harness(
            base.MemoryView(candidate_files, trees=trees),
            base.MemoryView(base_files),
        )
    finally:
        globals()["_git_blob_sha1"] = original


def _selftest_research_transition() -> None:
    ledger = b"reconciled-ledger-fixture"
    fixtures = {
        relative: ("fixture:" + relative).encode("utf-8")
        for relative in RESEARCH_DOC_PATHS
    }
    original = globals()["_git_blob_sha1"]
    try:
        fixture_hashes = {
            data: RESEARCH_DOC_BLOBS[relative]
            for relative, data in fixtures.items()
        }

        def fake_git_blob_sha1(data: bytes) -> str:
            if data == ledger:
                return EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1
            if data in fixture_hashes:
                return fixture_hashes[data]
            return original(data)

        globals()["_git_blob_sha1"] = fake_git_blob_sha1

        base_files = {
            POLICY_SCRIPT: b"harness-policy",
            CANONICAL_LEDGER_PATH: ledger,
        }
        candidate_files = dict(base_files)
        candidate_files.update(fixtures)
        candidate_trees = {
            relative: f"{index:040x}"
            for index, relative in enumerate(sorted(RESEARCH_DOC_PATHS), start=10)
        }
        _require_exact_delta_harness(
            base.MemoryView(candidate_files, trees=candidate_trees),
            base.MemoryView(base_files),
        )

        partial = dict(base_files)
        first_path = sorted(RESEARCH_DOC_PATHS)[0]
        partial[first_path] = fixtures[first_path]
        base.expect_failure_matching(
            "Harness research partial transition",
            "delta must be exactly seven files",
            _require_exact_delta_harness,
            base.MemoryView(partial, trees={first_path: "8" * 40}),
            base.MemoryView(base_files),
        )

        wrong = dict(candidate_files)
        wrong_path = sorted(RESEARCH_DOC_PATHS)[-1]
        wrong[wrong_path] = b"wrong-research-doc"
        base.expect_failure_matching(
            "Harness research wrong document blob",
            "document candidate drifted",
            _require_exact_delta_harness,
            base.MemoryView(wrong, trees=candidate_trees),
            base.MemoryView(base_files),
        )

        post_base = dict(candidate_files)
        post_candidate = dict(post_base)
        drift_path = sorted(RESEARCH_DOC_PATHS)[0]
        post_candidate[drift_path] = b"later-drift"
        post_trees = dict(candidate_trees)
        drift_trees = dict(candidate_trees)
        drift_trees[drift_path] = "9" * 40
        base.expect_failure_matching(
            "Harness research refreeze",
            "frozen after canonicalization",
            _require_exact_delta_harness,
            base.MemoryView(post_candidate, trees=drift_trees),
            base.MemoryView(post_base, trees=post_trees),
        )
    finally:
        globals()["_git_blob_sha1"] = original


def _selftest_steady_state_wrapper() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)

    if POLICY_SCRIPT not in _paths(view):
        base.fail("Harness research policy self-test cannot see its own wrapper")

    candidate = base.MemoryView({POLICY_SCRIPT: policy_bytes})
    policy_base = base.MemoryView({POLICY_SCRIPT: policy_bytes})
    if _is_bootstrap_base(policy_base):
        base.fail("Harness research steady-state self-test misclassified trusted base")

    mutated = base.MemoryView({POLICY_SCRIPT: policy_bytes + b"\n# drift\n"})
    base.expect_failure_matching(
        "Harness research wrapper refreeze",
        "steady-state policy wrapper changed",
        _verify_extension_paths_harness,
        mutated,
        policy_base,
        frozenset({POLICY_SCRIPT}),
    )


def selftest() -> None:
    _propagate_expected_workflow_hashes()
    v24.selftest()
    _install_harness_policy()
    _selftest_workflow_binding()
    _selftest_bootstrap_delta()
    _selftest_research_transition()
    _selftest_steady_state_wrapper()
    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness research authorization policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_harness_policy()
    return v24.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
