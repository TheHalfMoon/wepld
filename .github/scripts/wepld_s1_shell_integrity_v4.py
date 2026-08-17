#!/usr/bin/env python3
"""Final Rust-import hardening wrapper for bounded S1-010 Tauri shell admission.

This wrapper binds the exact reviewed v3 policy before import and closes the
remaining Rust import-alias escape without modifying any S1-010 product bytes.
The future Tauri main may reference the frozen direct `tauri::...` surface, but
it may not import, alias, group-import, or raw-ident import the Tauri crate.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v4.py"
PRIOR_V3_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v3.py"
EXPECTED_PRIOR_V3_RUNNER_GIT_BLOB_SHA1 = "aab4346c0deeee08c78022f8aafd6d400bc2155c"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "001f3accde730e3ffd9620f0f18d2224d152524f71e6978e6c10585f330e212d",
    ".github/workflows/s1-admission-integrity.yml": "c7bad8dc05fb1b69093f2356b2267b3a000f7bb67fc959b7a8d2f3b1bcbde6ba",
    ".github/workflows/s1-contracts.yml": "d58b7567e7751c2d7e51985229a2a0a7174308c207834672adddb9c3f7344901",
}

USE_ITEM = re.compile(r"\buse\b(?P<body>[^;]*);", re.DOTALL)
TAURI_USE_TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:r#)?tauri(?![A-Za-z0-9_])")
_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v3_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v3.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v3 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V3_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v3 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V3_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v3_runner_before_import()
import wepld_s1_shell_integrity_v3 as v3  # noqa: E402


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V3_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V3_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v3 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V3_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v3._verify_policy_files(view)


def _verify_shell_rust(view: base.RepositoryView) -> None:
    # Preserve every v1/v2 Rust restriction and v2 observation/cancel lock-scope
    # check, then close the import alias family that remained outside v1's
    # direct tauri:: API scan.
    v3.v2._verify_shell_rust(view)
    _, code = v3.v2.shell.prior.prior._read_rust(
        view,
        "apps/desktop/src-tauri/src/main.rs",
        v3.v2.shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )

    for match in USE_ITEM.finditer(code):
        if TAURI_USE_TOKEN.search(match.group("body")) is not None:
            base.fail(
                "S1-010 Tauri main may not import or alias the tauri crate; "
                "use the frozen direct tauri:: API surface only"
            )


def _install_v4_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v3._install_v3_policy()

    v3.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v3.v2.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v3.v2.shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v3.v2.shell.prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    v3.v2.shell.verify_policy_files = _verify_policy_files
    v3.v2.shell.verify_shell_rust = _verify_shell_rust
    _INSTALLED = True


def selftest() -> None:
    # Preserve all inherited expected rejection reasons before installing the
    # new alias hardening layer.
    v3.selftest()
    _install_v4_policy()

    safe = v3._safe_v3_fixture()
    fixture = base.MemoryView(safe)
    _verify_shell_rust(fixture)
    v3._verify_frontend(fixture)
    v3.v2.shell.verify_shell_config(fixture)

    absolute_alias = dict(safe)
    absolute_alias["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"use std::sync::Mutex;\n",
        b"use std::sync::Mutex;\nuse ::tauri as t;\n",
        1,
    )
    base.expect_failure_matching(
        "absolute tauri import alias",
        "may not import or alias the tauri crate",
        _verify_shell_rust,
        base.MemoryView(absolute_alias),
    )

    grouped_alias = dict(safe)
    grouped_alias["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"use std::sync::Mutex;\n",
        b"use std::sync::Mutex;\nuse {tauri as t};\n",
        1,
    )
    base.expect_failure_matching(
        "grouped tauri import alias",
        "may not import or alias the tauri crate",
        _verify_shell_rust,
        base.MemoryView(grouped_alias),
    )

    raw_alias = dict(safe)
    raw_alias["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"use std::sync::Mutex;\n",
        b"use std::sync::Mutex;\nuse r#tauri as t;\n",
        1,
    )
    base.expect_failure_matching(
        "raw-ident tauri import alias",
        "may not import or alias the tauri crate",
        _verify_shell_rust,
        base.MemoryView(raw_alias),
    )

    print("wepld S1 Tauri shell Rust-import hardening policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v4_policy()
    return v3.v2.shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
