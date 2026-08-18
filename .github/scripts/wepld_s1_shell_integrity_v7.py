#!/usr/bin/env python3
"""ASCII source-boundary hardening wrapper for bounded S1-010 Tauri admission.

This wrapper binds the exact reviewed v6 policy before import and closes the
remaining Unicode-identifier escape. The future S1-010 Rust host fixture is
intentionally ASCII-only; non-ASCII source is rejected before it can evade the
ASCII lexical scanners inherited by the bounded admission chain.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v7.py"
PRIOR_V6_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v6.py"
EXPECTED_PRIOR_V6_RUNNER_GIT_BLOB_SHA1 = "6f976a6056ce05475c802ee132a0d7206fab3e31"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "3d2ad66aa64c75d3b350205285390e08f0c3ebdcbff92d1152228e532ae6cabc",
    ".github/workflows/s1-admission-integrity.yml": "7252f233608c9ce0830e412addc0969f51ccd971576efee9fb86b7bc8a11885c",
    ".github/workflows/s1-contracts.yml": "18291cef5587407bf1699ecf146e5ca08031e4a6dac8b9362d85a84a2084dcac",
}

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v6_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v6.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v6 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V6_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v6 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V6_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v6_runner_before_import()
import wepld_s1_shell_integrity_v6 as v6  # noqa: E402


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V6_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V6_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v6 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V6_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v6._verify_policy_files(view)


def _verify_shell_rust(view: base.RepositoryView) -> None:
    # Preserve every v1-v6 Rust restriction first. Then reject any non-ASCII
    # source byte so Unicode identifiers cannot hide from the intentionally
    # bounded ASCII lexical scanners used by this stage.
    v6._verify_shell_rust(view)
    raw, _ = v6.v5.v4.v3.v2.shell.prior.prior._read_rust(
        view,
        "apps/desktop/src-tauri/src/main.rs",
        v6.v5.v4.v3.v2.shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )
    if not raw.isascii():
        base.fail(
            "S1-010 Tauri main must remain ASCII-only so bounded lexical admission "
            "cannot be bypassed by Unicode identifiers"
        )


def _install_v7_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v6._install_v6_policy()

    v6.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v6.v5.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v6.v5.v4.v3.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v6.v5.v4.v3.v2.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v6.v5.v4.v3.v2.shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v6.v5.v4.v3.v2.shell.prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    v6.v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v6.v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    v6.v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v6.v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS)
        | {POLICY_SCRIPT}
    )

    v6.v5.v4.v3.v2.shell.verify_policy_files = _verify_policy_files
    v6.v5.v4.v3.v2.shell.verify_shell_rust = _verify_shell_rust
    _INSTALLED = True


def selftest() -> None:
    # Preserve all inherited expected rejection reasons before installing the
    # ASCII source-boundary hardening layer.
    v6.selftest()
    _install_v7_policy()

    safe = v6.v5.v4.v3._safe_v3_fixture()
    fixture = base.MemoryView(safe)
    _verify_shell_rust(fixture)
    v6.v5.v4.v3._verify_frontend(fixture)
    v6.v5.v4.v3.v2.shell.verify_shell_config(fixture)

    unicode_macro_alias = dict(safe)
    unicode_macro_alias["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"use std::sync::Mutex;\n",
        "use std::println as 出力;\nuse std::sync::Mutex;\n".encode("utf-8"),
        1,
    ).replace(
        b"fn core_ready(_state: tauri::State<'_, AppState>) -> bool { false }",
        "fn core_ready(_state: tauri::State<'_, AppState>) -> bool { 出力!(\"message\"); false }".encode("utf-8"),
        1,
    )
    base.expect_failure_matching(
        "Unicode macro alias",
        "must remain ASCII-only",
        _verify_shell_rust,
        base.MemoryView(unicode_macro_alias),
    )

    unicode_function = dict(safe)
    unicode_function["apps/desktop/src-tauri/src/main.rs"] = (
        safe["apps/desktop/src-tauri/src/main.rs"]
        + "fn 秘密() {}\n".encode("utf-8")
    )
    base.expect_failure_matching(
        "Unicode hidden function",
        "must remain ASCII-only",
        _verify_shell_rust,
        base.MemoryView(unicode_function),
    )

    print("wepld S1 Tauri shell ASCII source-boundary policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v7_policy()
    return v6.v5.v4.v3.v2.shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
