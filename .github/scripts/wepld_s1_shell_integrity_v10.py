#!/usr/bin/env python3
"""Windows icon identity repair for bounded S1-010 Tauri shell admission.

This wrapper binds the exact reviewed v9 policy before import and closes the
Windows tauri-build resource gap discovered by the S1-010 product qualification
job. The future product candidate must carry exactly one frozen application icon
at the Tauri default Windows resource path. No new dependency, plugin, package
manager, process, filesystem, network, or sidecar authority is introduced.

This file authorizes one repaired future stage only. It does not implement
S1-010 product bytes.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v10.py"
PRIOR_V9_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v9.py"
EXPECTED_PRIOR_V9_RUNNER_GIT_BLOB_SHA1 = "1b858b59215021d867f19322fd4efdf97c1fd66d"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "bd293353ba2e301e809d9d40234572dbf4288dc0c1d15a4dbe1a5ceb515fd796",
    ".github/workflows/s1-admission-integrity.yml": "7ee94c4cf15c748761ff84088dc5f45206d7c5ff6aa74774ba1fd20f4a23c412",
    ".github/workflows/s1-contracts.yml": "d307e6b11a1385e1257098d318bf8912812167b5f6517080493df73beb18e8b2",
}

ICON_PATH = "apps/desktop/src-tauri/icons/icon.ico"
EXPECTED_ICON_BYTES = 4286
EXPECTED_ICON_SHA256 = "e598c151776122e15f426798fddb4ed9c400085ce83623718b58841e25bac38b"
MAX_ICON_BYTES = 64_000

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v9_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v9.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v9 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V9_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v9 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V9_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v9_runner_before_import()
import wepld_s1_shell_integrity_v9 as v9  # noqa: E402

shell = v9.v8.v7.v6.v5.v4.v3.v2.shell


def _check_icon_identity(data: bytes, expected_bytes: int, expected_sha256: str) -> None:
    if len(data) != expected_bytes:
        base.fail(
            "S1-010 Tauri icon size drifted: "
            f"expected={expected_bytes} actual={len(data)}"
        )
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_sha256:
        base.fail(
            "S1-010 Tauri icon must equal the frozen Windows resource fixture: "
            f"expected_sha256={expected_sha256} actual_sha256={actual}"
        )


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V9_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V9_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v9 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V9_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v9._verify_policy_files(view)


def _verify_shell_icon(view: base.RepositoryView) -> None:
    data = view.read_bytes(ICON_PATH, MAX_ICON_BYTES)
    _check_icon_identity(data, EXPECTED_ICON_BYTES, EXPECTED_ICON_SHA256)


def _verify_shell_sources(view: base.RepositoryView) -> None:
    shell.verify_build_script(view)
    shell.verify_shell_config(view)
    shell.verify_shell_rust(view)
    shell.verify_frontend(view)
    _verify_shell_icon(view)


def _install_v10_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v9._install_v9_policy()

    hash_modules = (
        v9,
        v9.v8,
        v9.v8.v7,
        v9.v8.v7.v6,
        v9.v8.v7.v6.v5,
        v9.v8.v7.v6.v5.v4.v3,
        v9.v8.v7.v6.v5.v4.v3.v2,
        shell,
        shell.prior,
    )
    for module in hash_modules:
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    shell.S1_010_MARKER_PATHS = frozenset(
        set(shell.S1_010_MARKER_PATHS) | {ICON_PATH}
    )
    shell.S1_010_ALLOWED_PATHS = frozenset(
        set(shell.S1_010_ALLOWED_PATHS) | {ICON_PATH}
    )

    shell.verify_policy_files = _verify_policy_files
    shell.verify_shell_sources = _verify_shell_sources
    _INSTALLED = True


def selftest() -> None:
    v9.selftest()
    _install_v10_policy()

    sample = b"wepld-icon-policy-selftest"
    _check_icon_identity(sample, len(sample), hashlib.sha256(sample).hexdigest())

    base.expect_failure_matching(
        "S1-010 icon size mutation",
        "icon size drifted",
        _check_icon_identity,
        b"x",
        2,
        hashlib.sha256(b"x").hexdigest(),
    )
    base.expect_failure_matching(
        "S1-010 icon byte mutation",
        "must equal the frozen Windows resource fixture",
        _check_icon_identity,
        sample + b"x",
        len(sample) + 1,
        hashlib.sha256(sample + b"y").hexdigest(),
    )

    markers_without_icon = set(shell.S1_010_MARKER_PATHS) - {ICON_PATH}
    base.expect_failure_matching(
        "S1-010 icon omission",
        "partial S1-010 Tauri shell candidate is prohibited",
        shell.classify_stage,
        markers_without_icon,
    )

    if len(EXPECTED_ICON_SHA256) != 64:
        base.fail("S1-010 frozen icon SHA-256 must be 64 lowercase hexadecimal characters")
    if EXPECTED_ICON_SHA256.lower() != EXPECTED_ICON_SHA256:
        base.fail("S1-010 frozen icon SHA-256 must be lowercase")

    print("wepld S1 Tauri shell Windows-icon identity policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v10_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
