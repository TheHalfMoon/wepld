#!/usr/bin/env python3
"""Authorize only S1-012 platform qualification evidence over canonical S1-011.

Canonical v22 freezes the exact Clippy-safe S1-011 source projection and grants no
S1-012+ product authority. S1-012 now requires Windows-first package/runtime
qualification plus bounded Linux/macOS secondary compile/protocol evidence.

This wrapper changes no product/runtime/dependency/UI bytes. It binds the exact v22
runner before import, advances only the three already-controlled workflow byte
identities, and permits the existing token-minimal `s1-contracts` workflow to produce
S1-012 qualification evidence. The workflow uses the already-admitted Tauri source
commit only as a pinned CI build-tool source, does not add a runtime dependency, and
must not turn secondary-platform compile evidence into containment/process-ownership
claims. S1-013+ remains unauthorized.

Bootstrap note: the candidate-head foundation path is an unprivileged self-check, not
acceptance authority. A new wrapper cannot recursively pin its own bytes from within
itself. The v22->v23 transition is therefore bound by the exact four-path bootstrap
surface plus external exact-head qualification/review. Once v23 is canonical, its
steady-state path requires the wrapper and all controlled workflows to remain
byte-identical to the trusted v23 base.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v23.py"
PRIOR_V22_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v22.py"
EXPECTED_PRIOR_V22_RUNNER_GIT_BLOB_SHA1 = "0ef3aeb849ceba21dc50bd29df8ed27e6ebb3586"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "7a1fca2b32ffa843f596dab608f580d2f32a226f9867f7081be45516791e7219",
    ".github/workflows/s1-admission-integrity.yml": "efb01f78dace2db331fa4bedcad3ed46e0a60e3f5ad1ff7d6c60cc820247453f",
    ".github/workflows/s1-contracts.yml": "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

TAURI_SOURCE_COMMIT = "7cd71369c00978a3783b6ae3e9972358abbe4ae6"
TAURI_CLI_VERSION = "2.11.4"
PLATFORM_WORKFLOW = ".github/workflows/s1-contracts.yml"
BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS = frozenset(
    {
        ".github/workflows/foundation-integrity.yml",
        ".github/workflows/s1-admission-integrity.yml",
    }
)
S1_012_QUALIFICATION_AUTHORIZED = "YES"
S1_013_PLUS = "NOT_STARTED"
BOOTSTRAP_DELTA_PATHS = frozenset(
    {
        POLICY_SCRIPT,
        ".github/workflows/foundation-integrity.yml",
        ".github/workflows/s1-admission-integrity.yml",
        PLATFORM_WORKFLOW,
    }
)

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v22_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v22.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-011 v22 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V22_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v22 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V22_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v22_runner_before_import()
import wepld_s1_shell_integrity_v22 as v22  # noqa: E402

PRIOR_V22_WORKFLOW_SHA256 = dict(v22.EXPECTED_WORKFLOW_SHA256)

v21 = v22.v21
v20 = v22.v20
v19 = v22.v19
v18 = v22.v18
v17 = v22.v17
v16 = v22.v16
v15 = v22.v15
v14 = v22.v14
v13 = v22.v13
v12 = v22.v12
v11 = v22.v11
v10 = v22.v10
v9 = v22.v9
v8 = v22.v8
v7 = v22.v7
v6 = v22.v6
v5 = v22.v5
v4 = v22.v4
v3 = v22.v3
v2 = v22.v2
shell = v22.shell
PRIOR_V19_REQUIRE_EXACT_DELTA = v19._require_exact_delta


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V22_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V22_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v22 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V22_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v22._verify_policy_files(view)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
            changed.add(relative)
    return changed


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    """True only while the trusted base is pre-v23."""
    return policy_base.tree_identity(POLICY_SCRIPT) is None


def _require_exact_delta_v23(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    """Admit the exact four-path bootstrap only from pre-v23; otherwise delegate."""
    if _is_bootstrap_base(policy_base):
        changed = _changed_paths(candidate, policy_base)
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            return
    PRIOR_V19_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_v23(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    """Permit exact v22->v23 workflow transitions, then require v23 steady-state equality."""
    bootstrap = _is_bootstrap_base(policy_base)

    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "S1-012 workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )

            if bootstrap:
                expected_base = PRIOR_V22_WORKFLOW_SHA256[relative]
                actual_base = _sha256(base_bytes)
                if actual_base != expected_base:
                    base.fail(
                        "S1-012 bootstrap trusted-base workflow drifted: "
                        f"{relative}: expected={expected_base} actual={actual_base}"
                    )
            else:
                actual_base = _sha256(base_bytes)
                if actual_base != expected_candidate:
                    base.fail(
                        "S1-012 steady-state trusted-base workflow drifted: "
                        f"{relative}: expected={expected_candidate} actual={actual_base}"
                    )
                if candidate_bytes != base_bytes:
                    base.fail(
                        f"S1-012 steady-state base-controlled workflow changed: {relative}"
                    )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_v23(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    """Permit bootstrap transition once; require byte equality after v23 is trusted base."""
    bootstrap = _is_bootstrap_base(policy_base)

    for relative in sorted(controlled_paths):
        if relative == POLICY_SCRIPT:
            candidate_identity = candidate.tree_identity(relative)
            if candidate_identity is None:
                base.fail("S1-012 v23 policy wrapper is missing from candidate")

            if bootstrap:
                # The candidate self-check is deliberately non-authoritative. The
                # new wrapper cannot contain a non-recursive digest of its own final
                # bytes; exact-head external qualification/review binds bootstrap.
                if policy_base.tree_identity(relative) is not None:
                    base.fail(
                        "S1-012 bootstrap policy wrapper unexpectedly exists in trusted base"
                    )
            else:
                base_identity = policy_base.tree_identity(relative)
                if base_identity is None:
                    base.fail("S1-012 steady-state trusted base is missing v23 wrapper")
                candidate_bytes = candidate.read_bytes(
                    relative, base.MAX_POLICY_FILE_BYTES
                )
                base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
                if candidate_bytes != base_bytes:
                    base.fail("S1-012 steady-state v23 policy wrapper changed")
            continue

        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative == PLATFORM_WORKFLOW:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "S1-012 platform workflow candidate drifted: "
                    f"expected={expected_candidate} actual={actual_candidate}"
                )

            if bootstrap:
                expected_base = PRIOR_V22_WORKFLOW_SHA256[relative]
                actual_base = _sha256(base_bytes)
                if actual_base != expected_base:
                    base.fail(
                        "S1-012 platform workflow bootstrap trusted base drifted: "
                        f"expected={expected_base} actual={actual_base}"
                    )
            else:
                actual_base = _sha256(base_bytes)
                if actual_base != expected_candidate:
                    base.fail(
                        "S1-012 platform workflow steady-state trusted base drifted: "
                        f"expected={expected_candidate} actual={actual_base}"
                    )
                if candidate_bytes != base_bytes:
                    base.fail("S1-012 steady-state platform workflow changed")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled S1 execution policy path changed: {relative}")


def _verify_execution_extension_controlled_paths_v23(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_v23(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_controlled_paths_v23(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_v23(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("S1-012 prior success printer is not installed")

    _PRIOR_PRINT_SUCCESS(stage, mode)

    if stage == v19.S1_011_STAGE:
        print(f"s1_012_platform_qualification_authorized={S1_012_QUALIFICATION_AUTHORIZED}")
        print(f"s1_012_platform_qualification_workflow={PLATFORM_WORKFLOW}")
        print(f"s1_012_tauri_cli_source_commit={TAURI_SOURCE_COMMIT}")
        print(f"s1_012_tauri_cli_version={TAURI_CLI_VERSION}")
        print(f"s1_013_plus={S1_013_PLUS}")


def _install_v23_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v22._install_v22_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    # The bootstrap candidate may advance only the exact workflow bytes pinned
    # above. Once v23 is in the trusted base, the same hooks become strict
    # steady-state equality checks. Every other base/extension-controlled path
    # remains byte-identical throughout.
    base.compare_base_controlled = _compare_base_controlled_v23
    v19._require_exact_delta = _require_exact_delta_v23
    shell.prior.verify_extension_controlled_paths = (
        _verify_desktop_extension_controlled_paths_v23
    )
    shell.prior.prior.verify_extension_controlled_paths = (
        _verify_execution_extension_controlled_paths_v23
    )

    for module in (
        v22,
        v21,
        v20,
        v19,
        v18,
        v17,
        v16,
        v15,
        v14,
        v13,
        v12,
        v11,
        v10,
        v9,
        v8,
        v7,
        v6,
        v5,
        v4,
        v3,
        v2,
        shell,
        shell.prior,
    ):
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    # The workflow path itself is already an exact extension-controlled path
    # inherited from S1 execution policy. Only this new wrapper path is added.
    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success
    _INSTALLED = True


def _selftest_platform_workflow_binding() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    workflow = view.read_bytes(PLATFORM_WORKFLOW, base.MAX_POLICY_FILE_BYTES)
    actual = hashlib.sha256(workflow).hexdigest()
    expected = EXPECTED_WORKFLOW_SHA256[PLATFORM_WORKFLOW]
    if actual != expected:
        base.fail(
            "S1-012 platform qualification workflow drifted: "
            f"expected={expected} actual={actual}"
        )

    required = (
        b"runs-on: windows-latest",
        b"os: [ubuntu-latest, macos-latest]",
        b"runs-on: ${{ matrix.os }}",
        b"permissions: {}",
        b"7cd71369c00978a3783b6ae3e9972358abbe4ae6",
        b"2\\.11\\.4",
        b"cargo tauri build --ci --bundles nsis",
        b"WINDOWS_RUNTIME_CONTAINMENT_CLAIM=NONE",
        b'case "$RUNNER_OS" in',
        b"${platform}_RUNTIME_CONTAINMENT_CLAIM=NONE",
        b"Copy-Item -Force target\\debug\\wepld-core.exe apps\\desktop\\src-tauri\\binaries\\wepld-core-x86_64-pc-windows-msvc.exe",
        b"WINDOWS_PREEXEC_BINARY_IDENTITY_ATTESTATION=NOT_IMPLEMENTED_NOT_CLAIMED",
        b"$installerPattern = Join-Path $repoRoot 'target\\release\\bundle\\nsis\\*.exe'",
    )
    missing = [token.decode("utf-8") for token in required if token not in workflow]
    if missing:
        base.fail(
            "S1-012 platform workflow is missing frozen qualification invariant(s): "
            + ", ".join(missing)
        )


def _selftest_v23_steady_state() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)

    current_workflows = {
        relative: view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        for relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS | {PLATFORM_WORKFLOW}
    }
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)

    base_files = {
        relative: b"unchanged"
        for relative in base.BASE_CONTROLLED_PATHS
        if relative not in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS
    }
    base_files.update(current_workflows)
    base_files[POLICY_SCRIPT] = policy_bytes

    candidate_files = dict(base_files)
    steady_base = base.MemoryView(base_files)
    steady_candidate = base.MemoryView(candidate_files)

    if _is_bootstrap_base(steady_base):
        base.fail("S1-012 steady-state self-test misclassified v23 trusted base")

    _compare_base_controlled_v23(steady_candidate, steady_base)
    _verify_extension_paths_v23(
        steady_candidate,
        steady_base,
        frozenset({POLICY_SCRIPT, PLATFORM_WORKFLOW}),
    )

    mutated = dict(candidate_files)
    mutated[POLICY_SCRIPT] = policy_bytes + b"\n# unauthorized steady-state drift\n"
    base.expect_failure_matching(
        "v23 steady-state wrapper drift",
        "steady-state v23 policy wrapper changed",
        _verify_extension_paths_v23,
        base.MemoryView(mutated),
        steady_base,
        frozenset({POLICY_SCRIPT, PLATFORM_WORKFLOW}),
    )

    mutated_workflow = dict(candidate_files)
    mutated_workflow[PLATFORM_WORKFLOW] = current_workflows[PLATFORM_WORKFLOW] + b"\n"
    base.expect_failure_matching(
        "v23 steady-state platform workflow drift",
        "platform workflow candidate drifted",
        _verify_extension_paths_v23,
        base.MemoryView(mutated_workflow),
        steady_base,
        frozenset({POLICY_SCRIPT, PLATFORM_WORKFLOW}),
    )

    bootstrap_base = base.MemoryView({})
    if not _is_bootstrap_base(bootstrap_base):
        base.fail("S1-012 bootstrap self-test failed to identify pre-v23 trusted base")


def selftest() -> None:
    v22.selftest()
    _install_v23_policy()
    _selftest_platform_workflow_binding()
    _selftest_v23_steady_state()

    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )

    print("wepld S1-012 platform-qualification policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v23_policy()
    return v22.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
