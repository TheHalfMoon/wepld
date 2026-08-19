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
    ".github/workflows/s1-contracts.yml": "d0b6cd82688e0e4538b31413b6fccd65629c89d043dc9e122342fb543fc0cc1f",
}

TAURI_SOURCE_COMMIT = "7cd71369c00978a3783b6ae3e9972358abbe4ae6"
TAURI_CLI_VERSION = "2.11.4"
PLATFORM_WORKFLOW = ".github/workflows/s1-contracts.yml"
S1_012_QUALIFICATION_AUTHORIZED = "YES"
S1_013_PLUS = "NOT_STARTED"

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


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V22_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V22_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v22 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V22_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v22._verify_policy_files(view)


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
        b"runs-on: ubuntu-latest",
        b"runs-on: macos-latest",
        b"permissions: {}",
        b"7cd71369c00978a3783b6ae3e9972358abbe4ae6",
        b"2\\.11\\.4",
        b"cargo tauri build --ci --bundles nsis",
        b"WINDOWS_RUNTIME_CONTAINMENT_CLAIM=NONE",
        b"LINUX_RUNTIME_CONTAINMENT_CLAIM=NONE",
        b"MACOS_RUNTIME_CONTAINMENT_CLAIM=NONE",
    )
    missing = [token.decode("utf-8") for token in required if token not in workflow]
    if missing:
        base.fail(
            "S1-012 platform workflow is missing frozen qualification invariant(s): "
            + ", ".join(missing)
        )


def selftest() -> None:
    v22.selftest()
    _install_v23_policy()
    _selftest_platform_workflow_binding()

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
