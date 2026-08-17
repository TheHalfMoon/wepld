#!/usr/bin/env python3
"""Rust lexical-sanitizer and attribute-surface hardening for S1-010 admission.

This wrapper binds the exact reviewed v7 policy before import and closes three
remaining source-analysis gaps without changing product bytes:

- Rust char/byte-char literals are blanked before string recognition so quote
  characters cannot hide code from function-body checks.
- bang macros require a real token-tree delimiter; `!=` is never a macro, while
  `macro_rules!` definitions remain explicitly prohibited.
- the attribute surface is exact: one crate-level `forbid(unsafe_code)` plus
  exactly six `#[tauri::command]` attributes. Derive/procedural/cfg attributes
  are not admitted.

Raw identifiers are also prohibited for this intentionally bounded ASCII-only
host fixture so lexical identity cannot be re-spelled around the frozen checks.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v8.py"
PRIOR_V7_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v7.py"
EXPECTED_PRIOR_V7_RUNNER_GIT_BLOB_SHA1 = "43901cd5b215948b0e3fcc138d8550c6bff63830"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "eeebf282c6d0a52ed7a06eff6c6559dfdd4ded64b8c2af8b18203199a74dbdaf",
    ".github/workflows/s1-admission-integrity.yml": "c63f3096d391b0b45c75d9fcfd579e67e7b77db0b325785bb41b647c4d52ddf2",
    ".github/workflows/s1-contracts.yml": "9708cd763086bba388d1a604491d2d934e9fc41ba928ee311a6d5d345fbeb642",
}

MACRO_INVOCATION = re.compile(
    r"(?<![#A-Za-z0-9_])"
    r"((?:::)?(?:r#)?[A-Za-z_][A-Za-z0-9_]*"
    r"(?:\s*::\s*(?:r#)?[A-Za-z_][A-Za-z0-9_]*)*)"
    r"\s*!\s*(?=[(\[{])"
)
MACRO_RULES_DEFINITION = re.compile(
    r"\bmacro_rules\s*!\s*(?:r#)?[A-Za-z_][A-Za-z0-9_]*"
)
MACRO_2_DEFINITION = re.compile(r"\bmacro\s+(?:r#)?[A-Za-z_][A-Za-z0-9_]*")
RAW_IDENTIFIER = re.compile(r"\br#[A-Za-z_][A-Za-z0-9_]*")
ATTRIBUTE = re.compile(r"#\s*(!?)\s*\[\s*([^\]]*?)\s*\]", re.DOTALL)
EXPECTED_ATTRIBUTES = (
    ("!", "forbid(unsafe_code)"),
    ("", "tauri::command"),
    ("", "tauri::command"),
    ("", "tauri::command"),
    ("", "tauri::command"),
    ("", "tauri::command"),
    ("", "tauri::command"),
)

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v7_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v7.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v7 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V7_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v7 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V7_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v7_runner_before_import()
import wepld_s1_shell_integrity_v7 as v7  # noqa: E402

execution = v7.v6.v5.v4.v3.v2.shell.prior.prior


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V7_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V7_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v7 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V7_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v7._verify_policy_files(view)


def _blank_non_newlines(text: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in text)


def _char_literal_end(text: str, index: int) -> int | None:
    if text.startswith("b'", index):
        cursor = index + 2
    elif index < len(text) and text[index] == "'":
        cursor = index + 1
    else:
        return None

    if cursor >= len(text) or text[cursor] in "\r\n":
        return None

    if text[cursor] == "\\":
        cursor += 1
        if cursor >= len(text) or text[cursor] in "\r\n":
            return None

        if text[cursor] == "u" and cursor + 1 < len(text) and text[cursor + 1] == "{":
            close = text.find("}", cursor + 2)
            if close == -1:
                return None
            cursor = close + 1
        elif text[cursor] == "x":
            if cursor + 2 >= len(text):
                return None
            digits = text[cursor + 1 : cursor + 3]
            if re.fullmatch(r"[0-9A-Fa-f]{2}", digits) is None:
                return None
            cursor += 3
        else:
            cursor += 1
    else:
        cursor += 1

    if cursor < len(text) and text[cursor] == "'":
        return cursor + 1
    return None


def _strip_rust_comments_strings_and_chars(text: str) -> str:
    """Blank Rust comments/string/char literals while preserving offsets."""

    out: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        if text.startswith("//", index):
            end = text.find("\n", index + 2)
            if end == -1:
                out.append(" " * (length - index))
                break
            out.append(" " * (end - index))
            out.append("\n")
            index = end + 1
            continue

        if text.startswith("/*", index):
            start = index
            depth = 1
            index += 2
            while index < length and depth:
                if text.startswith("/*", index):
                    depth += 1
                    index += 2
                elif text.startswith("*/", index):
                    depth -= 1
                    index += 2
                else:
                    index += 1
            if depth != 0:
                base.fail("unterminated block comment")
            out.append(_blank_non_newlines(text[start:index]))
            continue

        char_end = _char_literal_end(text, index)
        if char_end is not None:
            out.append(_blank_non_newlines(text[index:char_end]))
            index = char_end
            continue

        raw = execution.RAW_STRING_PREFIX.match(text, index)
        if raw is not None:
            start = index
            hashes = raw.group(1)
            index = raw.end()
            close = '"' + hashes
            end = text.find(close, index)
            if end == -1:
                base.fail("unterminated raw string literal")
            index = end + len(close)
            out.append(_blank_non_newlines(text[start:index]))
            continue

        if text.startswith('b"', index) or text[index] == '"':
            start = index
            index += 2 if text.startswith('b"', index) else 1
            escaped = False
            closed = False
            while index < length:
                char = text[index]
                index += 1
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    closed = True
                    break
            if not closed:
                base.fail("unterminated string literal")
            out.append(_blank_non_newlines(text[start:index]))
            continue

        out.append(text[index])
        index += 1

    return "".join(out)


def _canonical_macro_name(raw: str) -> str:
    name = re.sub(r"\s+", "", raw)
    name = re.sub(r"r#(?=[A-Za-z_])", "", name)
    if name.startswith("::"):
        name = name[2:]
    return name


def _macro_invocations(code: str) -> list[str]:
    invocations = [
        _canonical_macro_name(match.group(1))
        for match in MACRO_INVOCATION.finditer(code)
    ]
    if MACRO_RULES_DEFINITION.search(code) is not None:
        invocations.append("macro_rules")
    if MACRO_2_DEFINITION.search(code) is not None:
        invocations.append("macro")
    return invocations


def _normalize_attribute(inner: str) -> str:
    return re.sub(r"\s+", "", inner)


def _verify_shell_rust(view: base.RepositoryView) -> None:
    v7._verify_shell_rust(view)

    _, code = execution._read_rust(
        view,
        "apps/desktop/src-tauri/src/main.rs",
        v7.v6.v5.v4.v3.v2.shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )

    raw_identifiers = sorted(set(RAW_IDENTIFIER.findall(code)))
    if raw_identifiers:
        base.fail(
            "S1-010 Tauri main raw identifiers are prohibited in the bounded lexical surface: "
            + ", ".join(raw_identifiers)
        )

    attributes = tuple(
        (match.group(1), _normalize_attribute(match.group(2)))
        for match in ATTRIBUTE.finditer(code)
    )
    if attributes != EXPECTED_ATTRIBUTES:
        rendered = ", ".join(
            ("#!" if bang else "#") + f"[{inner}]"
            for bang, inner in attributes
        )
        base.fail(
            "S1-010 Tauri main attribute surface must be exactly "
            "#![forbid(unsafe_code)] plus six #[tauri::command] attributes; "
            f"actual={rendered}"
        )


def _install_v8_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v7._install_v7_policy()

    v7.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v7.v6.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v7.v6.v5.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v7.v6.v5.v4.v3.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v7.v6.v5.v4.v3.v2.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v7.v6.v5.v4.v3.v2.shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v7.v6.v5.v4.v3.v2.shell.prior.EXPECTED_WORKFLOW_SHA256 = (
        EXPECTED_WORKFLOW_SHA256
    )

    v7.v6.v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v7.v6.v5.v4.v3.v2.shell.prior.EXTENSION_CONTROLLED_PATHS)
        | {POLICY_SCRIPT}
    )
    v7.v6.v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v7.v6.v5.v4.v3.v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS)
        | {POLICY_SCRIPT}
    )

    execution.strip_rust_comments_and_strings = _strip_rust_comments_strings_and_chars
    v7.v6._macro_invocations = _macro_invocations
    v7.v6.v5.v4.v3.v2.shell.verify_policy_files = _verify_policy_files
    v7.v6.v5.v4.v3.v2.shell.verify_shell_rust = _verify_shell_rust
    _INSTALLED = True


def selftest() -> None:
    # Preserve inherited rejection reasons before installing the stricter
    # sanitizer/macro/attribute layer.
    v7.selftest()
    _install_v8_policy()

    safe = v7.v6.v5.v4.v3._safe_v3_fixture()
    fixture = base.MemoryView(safe)
    _verify_shell_rust(fixture)
    v7.v6.v5.v4.v3._verify_frontend(fixture)
    v7.v6.v5.v4.v3.v2.shell.verify_shell_config(fixture)

    quote_hide = dict(safe)
    quote_hide["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b'    client.send_observe_health().map_err(|error| format!("{error:?}"))\n',
        b"    let _before = '\"';\n"
        b"    let _ = client.receive();\n"
        b"    let _after = '\"';\n"
        b'    client.send_observe_health().map_err(|error| format!("{error:?}"))\n',
        1,
    )
    base.expect_failure_matching(
        "double-quote char literals may not hide receive",
        "core_observe_health may not call or alias receive",
        _verify_shell_rust,
        base.MemoryView(quote_hide),
    )

    byte_quote_hide = dict(safe)
    byte_quote_hide["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b'    client.send_observe_health().map_err(|error| format!("{error:?}"))\n',
        b"    let _before = b'\"';\n"
        b"    let _ = client.receive();\n"
        b"    let _after = b'\"';\n"
        b'    client.send_observe_health().map_err(|error| format!("{error:?}"))\n',
        1,
    )
    base.expect_failure_matching(
        "double-quote byte-char literals may not hide receive",
        "core_observe_health may not call or alias receive",
        _verify_shell_rust,
        base.MemoryView(byte_quote_hide),
    )

    if _macro_invocations("request_id != 0") != []:
        base.fail("S1-010 v8 macro parser confused != with a bang macro")

    inequality = dict(safe)
    inequality["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b'    let client = guard.as_mut().ok_or_else(|| String::from("core unavailable"))?;\n'
        b"    client.send_cancel(request_id)",
        b'    let client = guard.as_mut().ok_or_else(|| String::from("core unavailable"))?;\n'
        b"    let _nonzero = request_id != 0;\n"
        b"    client.send_cancel(request_id)",
        1,
    )
    _verify_shell_rust(base.MemoryView(inequality))

    macro_rules_probe = "macro_rules! hidden { () => {} }"
    if "macro_rules" not in _macro_invocations(macro_rules_probe):
        base.fail("S1-010 v8 macro parser stopped detecting macro_rules definitions")

    derive = dict(safe)
    derive["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"struct AppState {\n",
        b"#[derive(Default)]\nstruct AppState {\n",
        1,
    )
    base.expect_failure_matching(
        "derive attribute macro",
        "attribute surface must be exactly",
        _verify_shell_rust,
        base.MemoryView(derive),
    )

    raw_identifier = dict(safe)
    raw_identifier["apps/desktop/src-tauri/src/main.rs"] = (
        safe["apps/desktop/src-tauri/src/main.rs"]
        + b"fn r#hidden() {}\n"
    )
    base.expect_failure_matching(
        "raw identifier hidden function",
        "raw identifiers are prohibited",
        _verify_shell_rust,
        base.MemoryView(raw_identifier),
    )

    print(
        "wepld S1 Tauri shell lexical sanitizer/macro/attribute policy self-tests: PASS"
    )


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v8_policy()
    return v7.v6.v5.v4.v3.v2.shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
