#!/usr/bin/env python3
"""Authorize one exact S1-012 ledger reconciliation over canonical v23.

Canonical v23 proves S1-012 platform qualification but intentionally leaves the
execution-authoritative S1 ledger frozen at its older checkpoint. This wrapper
does not grant S1-013+ product authority. It authorizes only:

1. the one-time v23->v24 policy/workflow bootstrap; and
2. after v24 is canonical, one exact tasks.md transition from the frozen
   pre-reconciliation blob to the reviewed S1-012 reconciliation blob.

After that exact ledger blob is canonical, the same path is frozen again and
ordinary inherited candidate semantics continue through canonical v23.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v24.py"
PRIOR_V23_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v23.py"
EXPECTED_PRIOR_V23_RUNNER_GIT_BLOB_SHA1 = "08178e4a692a71e60a7195643f9f94b99cf4521f"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
LEDGER_PATH = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "e5495e875bae585fef2ad13c687148ec965e0ed552b7aba8bfc17a69a9c7b2ec",
    ADMISSION_WORKFLOW: "c9de3f71b448a5a5b9ea6a7b83a8a5925d64d0b9e7b7df17fca5d426875bf382",
    ".github/workflows/s1-contracts.yml": "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS = frozenset(
    {FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

EXPECTED_PRIOR_LEDGER_GIT_BLOB_SHA1 = "f7bd1dc2237a21d5117f86a7f807bcb4087c2f5b"
EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1 = "d331b7f167fe67ae9061ed553cf0949fab12aae0"

LEDGER_RECONCILIATION_AUTHORIZED = "EXACT_ONE_TIME"
S1_012_CANONICAL_ACTIVATION = "PROVEN"
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


def _bind_prior_v23_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v23.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-012 v23 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V23_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-012 v23 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V23_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v23_runner_before_import()
import wepld_s1_shell_integrity_v23 as v23  # noqa: E402

PRIOR_V23_WORKFLOW_SHA256 = dict(v23.EXPECTED_WORKFLOW_SHA256)
v22 = v23.v22
v19 = v23.v19
shell = v23.shell
PRIOR_V23_REQUIRE_EXACT_DELTA = v23._require_exact_delta_v23


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V23_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V23_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-012 v23 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V23_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v23._verify_policy_files(view)


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


def _ledger_blob(view: base.RepositoryView) -> str:
    return _git_blob_sha1(view.read_bytes(LEDGER_PATH, base.MAX_POLICY_FILE_BYTES))


def _require_exact_delta_v24(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)

    if _is_bootstrap_base(policy_base):
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            return
        PRIOR_V23_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    if changed == {LEDGER_PATH}:
        actual_base = _ledger_blob(policy_base)
        if actual_base != EXPECTED_PRIOR_LEDGER_GIT_BLOB_SHA1:
            base.fail(
                "S1-012 ledger reconciliation trusted base drifted: "
                f"expected={EXPECTED_PRIOR_LEDGER_GIT_BLOB_SHA1} actual={actual_base}"
            )
        actual_candidate = _ledger_blob(candidate)
        if actual_candidate != EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1:
            base.fail(
                "S1-012 ledger reconciliation candidate drifted: "
                f"expected={EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1} "
                f"actual={actual_candidate}"
            )
        return

    PRIOR_V23_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_v24(
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
                    "S1-012 ledger-reconciliation workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )

            expected_base = (
                PRIOR_V23_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"S1-012 ledger-reconciliation {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "S1-012 ledger-reconciliation steady-state workflow changed: "
                    f"{relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_v24(
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
                base.fail("S1-012 v24 ledger policy wrapper is missing from candidate")
            if bootstrap:
                if relative in base_paths:
                    base.fail(
                        "S1-012 v24 bootstrap wrapper unexpectedly exists in trusted base"
                    )
            else:
                if relative not in base_paths:
                    base.fail("S1-012 v24 steady-state trusted base is missing wrapper")
                if candidate.read_bytes(
                    relative, base.MAX_POLICY_FILE_BYTES
                ) != policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES):
                    base.fail("S1-012 v24 steady-state policy wrapper changed")
            continue

        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "S1-012 v24 controlled workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_V23_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"S1-012 v24 controlled workflow {phase} base drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"S1-012 v24 steady-state workflow changed: {relative}")
            continue

        if relative == v23.POLICY_SCRIPT:
            actual = _git_blob_sha1(candidate_bytes)
            if actual != EXPECTED_PRIOR_V23_RUNNER_GIT_BLOB_SHA1:
                base.fail(
                    "frozen S1-012 v23 wrapper drifted in candidate: "
                    f"expected={EXPECTED_PRIOR_V23_RUNNER_GIT_BLOB_SHA1} actual={actual}"
                )
            if candidate_bytes != base_bytes:
                base.fail("frozen S1-012 v23 wrapper changed")
            continue

        if relative == v23.PLATFORM_WORKFLOW:
            expected = EXPECTED_WORKFLOW_SHA256[relative]
            actual = _sha256(candidate_bytes)
            if actual != expected:
                base.fail(
                    "frozen S1-012 platform workflow drifted: "
                    f"expected={expected} actual={actual}"
                )
            if candidate_bytes != base_bytes:
                base.fail("frozen S1-012 platform workflow changed")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled S1 execution policy path changed: {relative}")


def _verify_execution_extension_controlled_paths_v24(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_v24(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_controlled_paths_v24(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_v24(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("S1-012 prior success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    if stage == v19.S1_011_STAGE:
        print(
            "s1_012_ledger_reconciliation_authorized="
            f"{LEDGER_RECONCILIATION_AUTHORIZED}"
        )
        print(f"s1_012_canonical_activation={S1_012_CANONICAL_ACTIVATION}")
        print(f"s1_013_plus={S1_013_PLUS}")


def _workflow_hash_modules() -> list[object]:
    modules: list[object] = [v23, v22]
    modules.extend(
        getattr(v22, name)
        for name in (
            "v21", "v20", "v19", "v18", "v17", "v16", "v15", "v14", "v13",
            "v12", "v11", "v10", "v9", "v8", "v7", "v6", "v5", "v4", "v3",
            "v2",
        )
    )
    modules.extend((shell, shell.prior))
    return modules


def _propagate_expected_workflow_hashes() -> None:
    for module in _workflow_hash_modules():
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256


def _install_v24_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v23._install_v23_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    base.compare_base_controlled = _compare_base_controlled_v24
    v19._require_exact_delta = _require_exact_delta_v24
    shell.prior.verify_extension_controlled_paths = (
        _verify_desktop_extension_controlled_paths_v24
    )
    shell.prior.prior.verify_extension_controlled_paths = (
        _verify_execution_extension_controlled_paths_v24
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
                "S1-012 v24 workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_ledger_transition() -> None:
    prior_ledger = b"prior-ledger-fixture"
    reconciled_ledger = b"reconciled-ledger-fixture"

    original = globals()["_ledger_blob"]
    try:
        def fake_ledger_blob(view: base.RepositoryView) -> str:
            data = view.read_bytes(LEDGER_PATH, base.MAX_POLICY_FILE_BYTES)
            if data == prior_ledger:
                return EXPECTED_PRIOR_LEDGER_GIT_BLOB_SHA1
            if data == reconciled_ledger:
                return EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1
            return _git_blob_sha1(data)

        globals()["_ledger_blob"] = fake_ledger_blob

        base_files = {
            POLICY_SCRIPT: b"v24",
            LEDGER_PATH: prior_ledger,
        }
        candidate_files = dict(base_files)
        candidate_files[LEDGER_PATH] = reconciled_ledger
        prior_trees = {LEDGER_PATH: "1" * 40}
        reconciled_trees = {LEDGER_PATH: "2" * 40}
        _require_exact_delta_v24(
            base.MemoryView(candidate_files, trees=reconciled_trees),
            base.MemoryView(base_files, trees=prior_trees),
        )

        bad_files = dict(base_files)
        bad_files[LEDGER_PATH] = b"unauthorized-ledger"
        base.expect_failure_matching(
            "v24 wrong ledger projection",
            "ledger reconciliation candidate drifted",
            _require_exact_delta_v24,
            base.MemoryView(bad_files, trees=reconciled_trees),
            base.MemoryView(base_files, trees=prior_trees),
        )

        post_base = {
            POLICY_SCRIPT: b"v24",
            LEDGER_PATH: reconciled_ledger,
        }
        post_candidate = dict(post_base)
        post_candidate[LEDGER_PATH] = b"later-ledger-drift"
        base.expect_failure_matching(
            "v24 ledger refreezes after reconciliation",
            "ledger reconciliation trusted base drifted",
            _require_exact_delta_v24,
            base.MemoryView(post_candidate, trees={LEDGER_PATH: "3" * 40}),
            base.MemoryView(post_base, trees=reconciled_trees),
        )
    finally:
        globals()["_ledger_blob"] = original


def _selftest_v24_steady_state() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    current_workflows = {
        relative: view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        for relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS
    }
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    v23_bytes = view.read_bytes(v23.POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    platform_bytes = view.read_bytes(v23.PLATFORM_WORKFLOW, base.MAX_POLICY_FILE_BYTES)

    steady_files = {
        relative: b"unchanged"
        for relative in base.BASE_CONTROLLED_PATHS
        if relative not in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS
    }
    steady_files.update(current_workflows)
    steady_files[POLICY_SCRIPT] = policy_bytes
    steady_files[v23.POLICY_SCRIPT] = v23_bytes
    steady_files[v23.PLATFORM_WORKFLOW] = platform_bytes

    steady_base = base.MemoryView(steady_files)
    steady_candidate = base.MemoryView(dict(steady_files))

    if _is_bootstrap_base(steady_base):
        base.fail("S1-012 v24 steady-state self-test misclassified trusted base")
    _compare_base_controlled_v24(steady_candidate, steady_base)
    _verify_extension_paths_v24(
        steady_candidate,
        steady_base,
        frozenset(
            {
                POLICY_SCRIPT,
                v23.POLICY_SCRIPT,
                v23.PLATFORM_WORKFLOW,
                FOUNDATION_WORKFLOW,
                ADMISSION_WORKFLOW,
            }
        ),
    )

    mutated = dict(steady_files)
    mutated[POLICY_SCRIPT] = policy_bytes + b"\n# unauthorized steady-state drift\n"
    base.expect_failure_matching(
        "v24 steady-state wrapper drift",
        "steady-state policy wrapper changed",
        _verify_extension_paths_v24,
        base.MemoryView(mutated),
        steady_base,
        frozenset({POLICY_SCRIPT}),
    )

    if not _is_bootstrap_base(base.MemoryView({v23.POLICY_SCRIPT: v23_bytes})):
        base.fail("S1-012 v24 bootstrap self-test failed to identify pre-v24 base")


def selftest() -> None:
    # v24 changes only the two policy-runner workflow references. Project the
    # v24 workflow identities into inherited self-tests before running them;
    # PRIOR_V23_WORKFLOW_SHA256 was captured at import and remains the immutable
    # bootstrap-base identity used by real transition verification.
    _propagate_expected_workflow_hashes()
    v23.selftest()
    _install_v24_policy()
    _selftest_workflow_binding()
    _selftest_ledger_transition()
    _selftest_v24_steady_state()
    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld S1-012 ledger-reconciliation policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_v24_policy()
    return v23.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
