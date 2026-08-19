#!/usr/bin/env python3
"""Rustfmt-normalize the frozen S1-010 Tauri main template.

This wrapper binds exact canonical v17 and repairs one policy/gate inconsistency:
v17 freezes semantically correct Rust bytes that `cargo fmt --check` rewrites at
six receive/match sites. v18 changes only that formatting, using the exact
rustfmt shape observed on the S1 Windows gate.

No product semantics, dependencies, plugins, process/filesystem/network
authority, background workers, UI behavior, branding work, or S1-011+ scope is
added or removed.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v18.py"
PRIOR_V17_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v17.py"
EXPECTED_PRIOR_V17_RUNNER_GIT_BLOB_SHA1 = "408ca431165a020f6cdc61d136c8aec694181219"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "2e5ee6f68946d3df3b8c08c0fab7455e8e4990c16df13864116b08f1267b5e47",
    ".github/workflows/s1-admission-integrity.yml": "09e7cbf1f3edca65456acca6717526387d5b3715de8af420f88fbfcf9cec950f",
    ".github/workflows/s1-contracts.yml": "2ab777e867c60ef545e1b96dd4ff01546ca268eb794ce5bc620c98e9af0fbc27",
}


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v17_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v17.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v17 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V17_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v17 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V17_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v17_runner_before_import()
import wepld_s1_shell_integrity_v17 as v17  # noqa: E402

v16 = v17.v16
v15 = v17.v15
v14 = v17.v14
v13 = v17.v13
v12 = v17.v12
v11 = v17.v11
v10 = v17.v10
v9 = v17.v9
v8 = v17.v8
v7 = v17.v7
v6 = v17.v6
v5 = v17.v5
v4 = v17.v4
v3 = v17.v3
v2 = v17.v2
shell = v17.shell

PRIOR_V17_MAIN = v17.EXPECTED_FIXED_ERROR_MAIN
_INSTALLED = False


def _rustfmt_main_from_v17() -> str:
    text = PRIOR_V17_MAIN
    old = (
        '        match client.receive().map_err(|_| String::from('
        '"core response unavailable"))? {\n'
    )
    new = (
        '        match client\n'
        '            .receive()\n'
        '            .map_err(|_| String::from("core response unavailable"))?\n'
        '        {\n'
    )
    if text.count(old) != 6:
        base.fail("unexpected v17 receive/match site count while constructing v18 template")
    return text.replace(old, new)


EXPECTED_RUSTFMT_MAIN = _rustfmt_main_from_v17()


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V17_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V17_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v17 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V17_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v17._verify_policy_files(view)


def _install_v18_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v17._install_v17_policy()

    for module in (
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

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    v17.EXPECTED_FIXED_ERROR_MAIN = EXPECTED_RUSTFMT_MAIN
    v16.EXPECTED_BOUNDED_DEMUX_MAIN = EXPECTED_RUSTFMT_MAIN
    v15.EXPECTED_DEMUX_MAIN = EXPECTED_RUSTFMT_MAIN
    v13.EXPECTED_RECONCILED_MAIN = EXPECTED_RUSTFMT_MAIN
    v12.EXPECTED_STATUS_MAIN = EXPECTED_RUSTFMT_MAIN

    shell.verify_policy_files = _verify_policy_files
    _INSTALLED = True


def selftest() -> None:
    # Preserve all canonical v1-v17 behavioral oracles first, then install only
    # the rustfmt-normalized byte template.
    v17.selftest()
    _install_v18_policy()

    safe = v3._safe_v3_fixture()
    safe["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_RUSTFMT_MAIN.encode("ascii")
    safe["apps/desktop/ui/app.js"] = v13.EXPECTED_SERIALIZED_JS.encode("ascii")
    fixture = base.MemoryView(safe)

    v12._verify_shell_rust(fixture)
    v3._verify_frontend(fixture)
    shell.verify_shell_config(fixture)

    old_unformatted = dict(safe)
    old_unformatted["apps/desktop/src-tauri/src/main.rs"] = PRIOR_V17_MAIN.encode("ascii")
    base.expect_failure_matching(
        "S1-010 unformatted v17 main template",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(old_unformatted),
    )

    one_site_reverted = dict(safe)
    one_site_reverted["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_RUSTFMT_MAIN.replace(
        '        match client\n'
        '            .receive()\n'
        '            .map_err(|_| String::from("core response unavailable"))?\n'
        '        {\n',
        '        match client.receive().map_err(|_| String::from('
        '"core response unavailable"))? {\n',
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 partial rustfmt template regression",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(one_site_reverted),
    )

    print("wepld S1 Tauri shell rustfmt-template policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v18_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
