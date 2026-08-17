#!/usr/bin/env python3
"""Rust function-boundary hardening wrapper for bounded S1-010 Tauri admission.

This wrapper binds the exact reviewed v4 policy before import and repairs the
remaining function-body parser escape: Rust character/byte-character literals
may contain braces and therefore must not affect structural brace accounting.

It also carries a regression proof that inherited S1-010 policy already rejects
`extern crate` aliases through the frozen `extern` prohibited identifier.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v5.py"
PRIOR_V4_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v4.py"
EXPECTED_PRIOR_V4_RUNNER_GIT_BLOB_SHA1 = "c37bad53d5c8ddc4a3f5debc0a74d5cf8dc8ccce"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "6f66a1e2b2ba4b4511fc4c631bd21782e654e5f78b171ded70070a2ba10517a5",
    ".github/workflows/s1-admission-integrity.yml": "dd13a19619c742231f11b76d23b82ad0008da53318b6c602b3acf4863bb40120",
    ".github/workflows/s1-contracts.yml": "97a356f93e8a7a9527b5fbcc00923b39fa7af1e91256037ae985bf0bb56d41a7",
}

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v4_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v4.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v4 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V4_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v4 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V4_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v4_runner_before_import()
import wepld_s1_shell_integrity_v4 as v4  # noqa: E402


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V4_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V4_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v4 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V4_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v4._verify_policy_files(view)


def _rust_char_literal_end(code: str, index: int) -> int | None:
    """Return the end offset for a Rust char/byte-char literal, else None.

    The input has already had comments and string literals blanked. This helper
    intentionally distinguishes character literals from lifetimes: a lifetime
    such as `'a` has no immediate closing quote and is therefore left intact.
    """

    if code.startswith("b'", index):
        cursor = index + 2
    elif index < len(code) and code[index] == "'":
        cursor = index + 1
    else:
        return None

    if cursor >= len(code) or code[cursor] in "\r\n":
        return None

    if code[cursor] == "\\":
        cursor += 1
        if cursor >= len(code) or code[cursor] in "\r\n":
            return None

        if code[cursor] == "u" and cursor + 1 < len(code) and code[cursor + 1] == "{":
            close = code.find("}", cursor + 2)
            if close == -1:
                return None
            cursor = close + 1
        elif code[cursor] == "x":
            if cursor + 2 >= len(code):
                return None
            digits = code[cursor + 1 : cursor + 3]
            if re.fullmatch(r"[0-9A-Fa-f]{2}", digits) is None:
                return None
            cursor += 3
        else:
            cursor += 1
    else:
        cursor += 1

    if cursor < len(code) and code[cursor] == "'":
        return cursor + 1
    return None


def _function_body(code: str, name: str) -> str:
    match = re.search(rf"\bfn\s+{re.escape(name)}\s*\(", code)
    if match is None:
        base.fail(f"S1-010 Tauri main missing expected function body: {name}")
    brace = code.find("{", match.end())
    if brace == -1:
        base.fail(f"S1-010 Tauri main missing function body brace: {name}")

    depth = 0
    index = brace
    while index < len(code):
        literal_end = _rust_char_literal_end(code, index)
        if literal_end is not None:
            index = literal_end
            continue

        char = code[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return code[brace + 1 : index]
        index += 1

    base.fail(f"S1-010 Tauri main has unterminated function body: {name}")
    raise AssertionError("unreachable")


def _install_v5_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v4._install_v4_policy()

    v4.v3.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v4.v3.v2.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v4.v3.v2.shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v4.v3.v2.shell.prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    v4.v3.v2.shell.verify_policy_files = _verify_policy_files
    v4.v3.v2._function_body = _function_body
    _INSTALLED = True


def _char_literal_bypass_fixture(literal: str) -> str:
    return (
        "\nfn core_observe_health() {\n"
        "    let request_id = client.send_observe_health()?;\n"
        f"    let _ = {literal};\n"
        "    let _ = client.receive();\n"
        "    Ok(request_id)\n"
        "}\n\n"
        "fn core_cancel_observation() {\n"
        "    let request_id = client.send_cancel(target_request_id)?;\n"
        "    Ok(request_id)\n"
        "}\n"
    )


def selftest() -> None:
    # Preserve all inherited expected rejection reasons before installing the
    # parser hardening layer.
    v4.selftest()
    _install_v5_policy()

    safe = v4.v3._safe_v3_fixture()
    fixture = base.MemoryView(safe)
    v4._verify_shell_rust(fixture)
    v4.v3._verify_frontend(fixture)
    v4.v3.v2.shell.verify_shell_config(fixture)

    # CodeRabbit raised `extern crate tauri as t;` as an alias concern. The
    # inherited v1 Rust verifier already rejects every `extern` identifier.
    extern_alias = dict(safe)
    extern_alias["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"#![forbid(unsafe_code)]\n",
        b"#![forbid(unsafe_code)]\nextern crate tauri as t;\n",
        1,
    )
    base.expect_failure_matching(
        "extern crate tauri alias",
        "prohibited effect identifier(s): extern",
        v4._verify_shell_rust,
        base.MemoryView(extern_alias),
    )

    for label, literal in (
        ("char close brace", "'}'"),
        ("byte char close brace", "b'}'"),
        ("char open brace", "'{'"),
        ("byte char open brace", "b'{'"),
        ("escaped quote char", r"'\''"),
        ("unicode close brace escape", r"'\u{7d}'"),
        ("hex close brace escape", r"'\x7d'"),
    ):
        base.expect_failure_matching(
            label,
            "core_observe_health may not call or alias receive",
            v4.v3.v2._verify_observation_handler_semantics,
            _char_literal_bypass_fixture(literal),
        )

    lifetime = "fn example() { let _value: &'a str; }"
    body = _function_body(lifetime, "example")
    if "_value" not in body:
        base.fail("S1-010 v5 function-body parser confused a Rust lifetime with a char literal")

    print("wepld S1 Tauri shell char-literal boundary policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v5_policy()
    return v4.v3.v2.shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
