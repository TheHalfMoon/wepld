#!/usr/bin/env python3
"""Tauri Builder identity hardening for bounded S1-010 admission.

This wrapper binds the exact reviewed v8 policy before import and closes the
remaining UFCS/type-indirection escape around the frozen Builder chain. The
future S1-010 Rust host may mention `tauri::Builder` exactly once. Inherited
policy already requires that occurrence to be the single `Builder::default()`
construction, so `Builder::setup`, `Builder::plugin`, function-value rebinding,
type aliases, and other second Builder paths fail closed even when they avoid
dot-method syntax.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v9.py"
PRIOR_V8_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v8.py"
EXPECTED_PRIOR_V8_RUNNER_GIT_BLOB_SHA1 = "57ddc7e530ed88bc0ecc709376e217e83f828691"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "d3bef712efdd55df9a22facb610ddcb08554b8b9b1e3d487914f8f35c6131b86",
    ".github/workflows/s1-admission-integrity.yml": "1a7e7e23a5d8f596f1e9e622d6a3dbb1f62ea9987ea3954d84ee8664374e28b7",
    ".github/workflows/s1-contracts.yml": "e8d6cd4a5794c086823f2ffda1d5ae2a417824a38e7b429b4a8b8671e2213a71",
}

TAURI_BUILDER = re.compile(r"\btauri\s*::\s*Builder\b")
_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v8_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v8.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v8 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V8_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v8 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V8_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v8_runner_before_import()
import wepld_s1_shell_integrity_v8 as v8  # noqa: E402

execution = v8.execution


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V8_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V8_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v8 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V8_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v8._verify_policy_files(view)


def _verify_shell_rust(view: base.RepositoryView) -> None:
    v8._verify_shell_rust(view)

    _, code = execution._read_rust(
        view,
        "apps/desktop/src-tauri/src/main.rs",
        v8.v7.v6.v5.v4.v3.v2.shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )
    builder_mentions = len(TAURI_BUILDER.findall(code))
    if builder_mentions != 1:
        base.fail(
            "S1-010 Tauri main must mention tauri::Builder exactly once; "
            "the inherited policy binds that occurrence to Builder::default(), "
            f"actual={builder_mentions}"
        )


def _install_v9_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v8._install_v8_policy()

    v8.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v8.v7.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v8.v7.v6.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v8.v7.v6.v5.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v8.v7.v6.v5.v4.v3.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v8.v7.v6.v5.v4.v3.v2.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v8.v7.v6.v5.v4.v3.v2.shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v8.v7.v6.v5.v4.v3.v2.shell.prior.EXPECTED_WORKFLOW_SHA256 = (
        EXPECTED_WORKFLOW_SHA256
    )

    v8.v7.v6.v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v8.v7.v6.v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS)
        | {POLICY_SCRIPT}
    )
    v8.v7.v6.v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v8.v7.v6.v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS)
        | {POLICY_SCRIPT}
    )

    v8.v7.v6.v5.v4.v3.v2.shell.verify_policy_files = _verify_policy_files
    v8.v7.v6.v5.v4.v3.v2.shell.verify_shell_rust = _verify_shell_rust
    _INSTALLED = True


def selftest() -> None:
    v8.selftest()
    _install_v9_policy()

    safe = v8.v7.v6.v5.v4.v3._safe_v3_fixture()
    fixture = base.MemoryView(safe)
    _verify_shell_rust(fixture)
    v8.v7.v6.v5.v4.v3._verify_frontend(fixture)
    v8.v7.v6.v5.v4.v3.v2.shell.verify_shell_config(fixture)

    ufcs_setup = dict(safe)
    ufcs_setup["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"    tauri::Builder::default()\n        .manage(state)",
        b"    let builder = tauri::Builder::default();\n"
        b"    let builder = tauri::Builder::setup(builder, |_app| Ok(()));\n"
        b"    builder\n        .manage(state)",
        1,
    )
    base.expect_failure_matching(
        "UFCS Tauri Builder setup hook",
        "must mention tauri::Builder exactly once",
        _verify_shell_rust,
        base.MemoryView(ufcs_setup),
    )

    function_value = dict(safe)
    function_value["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"    tauri::Builder::default()\n        .manage(state)",
        b"    let _setup_method = tauri::Builder::setup;\n"
        b"    tauri::Builder::default()\n        .manage(state)",
        1,
    )
    base.expect_failure_matching(
        "Tauri Builder method function-value rebinding",
        "must mention tauri::Builder exactly once",
        _verify_shell_rust,
        base.MemoryView(function_value),
    )

    print("wepld S1 Tauri shell Builder-identity policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v9_policy()
    return v8.v7.v6.v5.v4.v3.v2.shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
