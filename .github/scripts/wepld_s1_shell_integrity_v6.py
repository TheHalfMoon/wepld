#!/usr/bin/env python3
"""Rust macro-surface hardening wrapper for bounded S1-010 Tauri admission.

This wrapper binds the exact reviewed v5 policy before import and closes the
remaining lexical/code-generation escape: future S1-010 Rust may invoke only
the three macros required by the frozen shell template. Declarative macro
definitions, aliases, and every other macro invocation fail closed.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v6.py"
PRIOR_V5_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v5.py"
EXPECTED_PRIOR_V5_RUNNER_GIT_BLOB_SHA1 = "eee94df43a1077b9b2acd2d646f3b6bb3c31a207"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "a55e79861415a5e4110ed47b4a8699399a8ac5b46c993b9509c93b12b6197503",
    ".github/workflows/s1-admission-integrity.yml": "61107f572ad3bd489b2bfa237b8235ce26955f587dbc48f32a3758204290b77b",
    ".github/workflows/s1-contracts.yml": "2133daf21137af750369e180b7682ef176ae64277c5b2c66dc69d8f6b39d19e0",
}

ALLOWED_MACRO_INVOCATIONS = frozenset(
    {
        "format",
        "tauri::generate_handler",
        "tauri::generate_context",
    }
)
EXPECTED_MAIN_DOT_MEMBERS = (
    "ok",
    "manage",
    "invoke_handler",
    "run",
    "expect",
)
DOT_MEMBER = re.compile(r"\.\s*((?:r#)?[A-Za-z_][A-Za-z0-9_]*)\b")
MACRO_INVOCATION = re.compile(
    r"(?<![#A-Za-z0-9_])"
    r"((?:::)?(?:r#)?[A-Za-z_][A-Za-z0-9_]*"
    r"(?:\s*::\s*(?:r#)?[A-Za-z_][A-Za-z0-9_]*)*)"
    r"\s*!"
)
_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v5_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v5.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v5 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V5_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v5 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V5_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v5_runner_before_import()
import wepld_s1_shell_integrity_v5 as v5  # noqa: E402


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V5_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V5_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v5 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V5_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v5._verify_policy_files(view)


def _canonical_macro_name(raw: str) -> str:
    name = re.sub(r"\s+", "", raw)
    name = re.sub(r"r#(?=[A-Za-z_])", "", name)
    if name.startswith("::"):
        name = name[2:]
    return name


def _macro_invocations(code: str) -> list[str]:
    return [
        _canonical_macro_name(match.group(1))
        for match in MACRO_INVOCATION.finditer(code)
    ]


def _verify_shell_rust(view: base.RepositoryView) -> None:
    # Preserve v1-v5 Rust verification first, including import aliases and the
    # char-aware observation/cancel function-boundary parser.
    v5.v4._verify_shell_rust(view)

    _, code = v5.v4.v3.v2.shell.prior.prior._read_rust(
        view,
        "apps/desktop/src-tauri/src/main.rs",
        v5.v4.v3.v2.shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )
    invocations = _macro_invocations(code)
    unexpected = sorted(set(invocations) - ALLOWED_MACRO_INVOCATIONS)
    if unexpected:
        base.fail(
            "S1-010 Tauri main unexpected Rust macro invocation(s): "
            + ", ".join(unexpected)
        )

    present = set(invocations)
    missing = sorted(ALLOWED_MACRO_INVOCATIONS - present)
    if missing:
        base.fail(
            "S1-010 Tauri main missing required frozen macro invocation(s): "
            + ", ".join(missing)
        )

    main_body = v5._function_body(code, "main")
    dot_members = tuple(
        re.sub(r"^r#", "", match.group(1))
        for match in DOT_MEMBER.finditer(main_body)
    )
    if dot_members != EXPECTED_MAIN_DOT_MEMBERS:
        base.fail(
            "S1-010 Tauri main dot-member surface must be exactly "
            + ", ".join(EXPECTED_MAIN_DOT_MEMBERS)
            + "; actual="
            + ", ".join(dot_members)
        )


def _install_v6_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v5._install_v5_policy()

    v5.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v5.v4.v3.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v5.v4.v3.v2.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v5.v4.v3.v2.shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v5.v4.v3.v2.shell.prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    v5.v4.v3.v2.shell.verify_policy_files = _verify_policy_files
    v5.v4.v3.v2.shell.verify_shell_rust = _verify_shell_rust
    _INSTALLED = True


def selftest() -> None:
    # Preserve every inherited expected rejection reason before installing the
    # macro-surface hardening layer.
    v5.selftest()
    _install_v6_policy()

    safe = v5.v4.v3._safe_v3_fixture()
    fixture = base.MemoryView(safe)
    _verify_shell_rust(fixture)
    v5.v4.v3._verify_frontend(fixture)
    v5.v4.v3.v2.shell.verify_shell_config(fixture)

    safe_code = v5.v4.v3.v2.shell.prior.prior._read_rust(
        fixture,
        "apps/desktop/src-tauri/src/main.rs",
        v5.v4.v3.v2.shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )[1]
    if set(_macro_invocations(safe_code)) != ALLOWED_MACRO_INVOCATIONS:
        base.fail("S1-010 v6 safe fixture macro surface drifted")

    macro_alias = dict(safe)
    macro_alias["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"use wepld_desktop::CoreClient;\n",
        b"""use wepld_desktop::CoreClient;

macro_rules! access_tauri {
    ($crate_name:ident) => {{
        use $crate_name as t;
        let _: Option<t::AppHandle> = None;
    }};
}
""",
        1,
    ).replace(
        b"fn core_ready(_state: tauri::State<'_, AppState>) -> bool { false }",
        b"""fn core_ready(_state: tauri::State<'_, AppState>) -> bool {
    access_tauri!(tauri);
    false
}""",
        1,
    )
    base.expect_failure_matching(
        "macro-generated Tauri import alias",
        "unexpected Rust macro invocation(s)",
        _verify_shell_rust,
        base.MemoryView(macro_alias),
    )

    aliased_macro = dict(safe)
    aliased_macro["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"use std::sync::Mutex;\n",
        b"use std::format as render;\nuse std::sync::Mutex;\n",
        1,
    ).replace(
        b'format!("{error:?}")',
        b'render!("{error:?}")',
        1,
    )
    base.expect_failure_matching(
        "aliased macro invocation",
        "unexpected Rust macro invocation(s): render",
        _verify_shell_rust,
        base.MemoryView(aliased_macro),
    )

    builder_setup = dict(safe)
    builder_setup["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"tauri::Builder::default()\n        .manage(state)",
        b"tauri::Builder::default()\n        .setup(|_app| Ok(()))\n        .manage(state)",
        1,
    )
    base.expect_failure_matching(
        "extra Tauri Builder setup hook",
        "dot-member surface must be exactly",
        _verify_shell_rust,
        base.MemoryView(builder_setup),
    )

    builder_event_hook = dict(safe)
    builder_event_hook["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"tauri::Builder::default()\n        .manage(state)",
        b"tauri::Builder::default()\n        .on_window_event(|_, _| {})\n        .manage(state)",
        1,
    )
    base.expect_failure_matching(
        "extra Tauri Builder event hook",
        "dot-member surface must be exactly",
        _verify_shell_rust,
        base.MemoryView(builder_event_hook),
    )

    print("wepld S1 Tauri shell macro/main-surface hardening policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v6_policy()
    return v5.v4.v3.v2.shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
