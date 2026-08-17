#!/usr/bin/env python3
"""Bounded S1 execution extension over the canonical acquisition policy.

The privileged pull_request_target path always executes trusted-base policy and
reads candidate Git objects as data only. Candidate Rust executes only in the
separate token-minimal pull_request contracts workflow.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_execution_integrity.py"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
EXTENSION_CONTROLLED_PATHS = frozenset({POLICY_SCRIPT, CONTRACTS_WORKFLOW})

PROTOCOL_STAGE = "S1_PROTOCOL_CONTRACTS_CANDIDATE"
STATE_STAGE = "S1_HANDSHAKE_STATE_CANDIDATE"
PROCESS_STAGE = "S1_CORE_PROCESS_CANDIDATE"

S1_006_MARKER_PATHS = frozenset(
    {
        "crates/contracts/src/frame.rs",
        "crates/contracts/src/protocol.rs",
        "crates/contracts/tests/protocol_v1.rs",
    }
)
S1_006_ALLOWED_PATHS = S1_006_MARKER_PATHS | {"crates/contracts/src/lib.rs"}
S1_007_MARKER_PATHS = frozenset(
    {
        "crates/core/src/lib.rs",
        "crates/core/src/state.rs",
        "crates/core/tests/state_v1.rs",
    }
)
S1_007_ALLOWED_PATHS = S1_007_MARKER_PATHS

# main.rs is already the frozen Stage-B skeleton. The integration test is the
# structural marker that upgrades a candidate from pure state to S1-008.
S1_008_MARKER_PATHS = frozenset({"crates/core/tests/process_v1.rs"})
S1_008_ALLOWED_PATHS = S1_008_MARKER_PATHS | {"crates/core/src/main.rs"}

S1_005_EVIDENCE_PATH = (
    "specs/001-desktop-rust-trusted-core-handshake/"
    "s1-005-component-admission-evidence.md"
)
S1_006_FROZEN_EVIDENCE_PATHS = frozenset(
    {"docs/governance/DEPENDENCY_REGISTER.md", S1_005_EVIDENCE_PATH}
)
S1_007_FROZEN_PROTOCOL_PATHS = S1_006_ALLOWED_PATHS
S1_008_FROZEN_STATE_PATHS = S1_007_ALLOWED_PATHS

MAX_S1_006_SOURCE_BYTES = 256_000
MAX_S1_007_SOURCE_BYTES = 256_000
MAX_S1_008_SOURCE_BYTES = 256_000

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": (
        "ea999efbe2a5b4226eb008d1517469c7ade1d5b99fb9179f3fca6a6c8a17310e"
    ),
    ".github/workflows/s1-admission-integrity.yml": (
        "d3c34c3cfdee9849ca94ede21ea9d20df5d8fe68cabea1e620fe853e029a9e71"
    ),
    CONTRACTS_WORKFLOW: (
        "039603ff6e84430f1f12a4d2f2732adb73ec4878f0d2a9c1495daa1ac997c7e6"
    ),
}

PROHIBITED_EFFECT_IDENTIFIERS = frozenset(
    {
        "fs",
        "net",
        "process",
        "env",
        "thread",
        "tokio",
        "tauri",
        "Command",
        "TcpStream",
        "TcpListener",
        "UdpSocket",
        "UnixStream",
        "UnixListener",
        "NamedPipe",
        "File",
        "OpenOptions",
        "stdin",
        "stdout",
        "stderr",
        "print",
        "println",
        "eprint",
        "eprintln",
        "include",
        "include_bytes",
        "include_str",
    }
)
S1_007_PROHIBITED_EFFECT_IDENTIFIERS = PROHIBITED_EFFECT_IDENTIFIERS | {"path"}

# Core main may own inherited stdio and diagnostics stderr, but it may not mint
# filesystem/network/process/env/thread/Tauri authority or write unframed text.
# Inline/extern module introduction is prohibited so required external namespaces
# cannot be shadowed or rebound inside the admitted one-file Core process root.
S1_008_MAIN_PROHIBITED_IDENTIFIERS = frozenset(
    {
        "fs",
        "net",
        "process",
        "env",
        "thread",
        "tokio",
        "tauri",
        "Command",
        "TcpStream",
        "TcpListener",
        "UdpSocket",
        "UnixStream",
        "UnixListener",
        "NamedPipe",
        "File",
        "OpenOptions",
        "print",
        "println",
        "include",
        "include_bytes",
        "include_str",
        "path",
        "mod",
        "extern",
    }
)
S1_008_MAIN_OUTPUT_ESCAPE_IDENTIFIERS = frozenset(
    {
        "Write",
        "write",
        "write_all",
        "write_vectored",
        "write_all_vectored",
        "write_fmt",
        "writeln",
        "flush",
        "copy",
        "_print",
        "set_output_capture",
        "BufWriter",
        "LineWriter",
    }
)

# The only direct stdout write authority admitted in Core main is this typed
# framed helper. Leading `::` forces Rust 2018+ path resolution through the
# extern prelude for both std and wepld_contracts, preventing local namespace
# shadowing of the canonical codec or I/O implementation.
S1_008_MAIN_FRAMED_OUTPUT_HELPER = re.compile(
    r"""
    fn\s+write_protocol_frame\s*\(
        \s*stdout\s*:\s*&mut\s*::\s*std\s*::\s*io\s*::\s*StdoutLock\s*<\s*'_\s*>\s*,
        \s*envelope\s*:\s*&\s*::\s*wepld_contracts\s*::\s*ProtocolEnvelope\s*,?\s*
    \)
    \s*->\s*Result\s*<\s*\(\s*\)\s*,\s*::\s*wepld_contracts\s*::\s*FrameError\s*>
    \s*\{
        \s*let\s+wire\s*=\s*::\s*wepld_contracts\s*::\s*encode_frame\s*\(\s*envelope\s*\)\s*\?\s*;
        \s*::\s*std\s*::\s*io\s*::\s*Write\s*::\s*write_all\s*\(\s*stdout\s*,\s*&\s*wire\s*\)
        \s*\.\s*map_err\s*\(\s*\|error\|\s*::\s*wepld_contracts\s*::\s*FrameError\s*::\s*Io\s*\{\s*kind\s*:\s*error\s*\.\s*kind\s*\(\s*\)\s*\}\s*\)\s*\?\s*;
        \s*::\s*std\s*::\s*io\s*::\s*Write\s*::\s*flush\s*\(\s*stdout\s*\)
        \s*\.\s*map_err\s*\(\s*\|error\|\s*::\s*wepld_contracts\s*::\s*FrameError\s*::\s*Io\s*\{\s*kind\s*:\s*error\s*\.\s*kind\s*\(\s*\)\s*\}\s*\)
        \s*
    \}
    """,
    re.VERBOSE | re.DOTALL,
)

# The process integration test may launch exactly the Cargo-built owned Core
# binary and use Child/Stdio/thread test mechanics. It may not widen execution.
S1_008_TEST_PROHIBITED_IDENTIFIERS = frozenset(
    {
        "fs",
        "net",
        "tokio",
        "tauri",
        "option_env",
        "TcpStream",
        "TcpListener",
        "UdpSocket",
        "UnixStream",
        "UnixListener",
        "NamedPipe",
        "File",
        "OpenOptions",
        "include",
        "include_bytes",
        "include_str",
        "path",
    }
)
S1_008_TEST_PROCESS_IMPORT = re.compile(
    r"use\s+std\s*::\s*process\s*::\s*\{\s*Child\s*,\s*Command\s*,\s*Stdio\s*\}\s*;"
)
# This matcher intentionally runs on source whose string contents were blanked
# while preserving offsets. The same matched span is then validated in raw
# source by S1_008_TEST_OWNED_LAUNCH_RAW.
S1_008_TEST_OWNED_LAUNCH_SCRUBBED = re.compile(
    r"Command\s*::\s*new\s*\(\s*env\s*!\s*\(\s*\)\s*\)"
)
S1_008_TEST_OWNED_LAUNCH_RAW = re.compile(
    r'\ACommand\s*::\s*new\s*\(\s*env\s*!\s*\(\s*"CARGO_BIN_EXE_wepld-core"\s*\)\s*\)\Z'
)
S1_008_TEST_FORBIDDEN_COMMAND_MODIFIERS = frozenset(
    {
        "arg",
        "args",
        "envs",
        "env_remove",
        "env_clear",
        "current_dir",
        "uid",
        "gid",
        "groups",
        "arg0",
        "creation_flags",
        "raw_arg",
        "show_window",
    }
)

FORBID_UNSAFE_ATTRIBUTE = re.compile(
    r"\A#!\s*\[\s*forbid\s*\(\s*unsafe_code\s*\)\s*\]"
)
PATH_ATTRIBUTE = re.compile(r"#\s*\[\s*(?:r#)?path\b")
RUST_IDENTIFIER = re.compile(r"(?:r#)?([A-Za-z_][A-Za-z0-9_]*)")
RAW_STRING_PREFIX = re.compile(r'(?:br|r)(#{0,255})"')


def _require_component_inputs(paths: set[str], scope: str) -> None:
    missing = base.STAGE_B_ALL_PATHS - paths
    if missing:
        base.fail(
            f"{scope} candidate is missing frozen component inputs: "
            + ", ".join(sorted(missing))
        )
    if not any(path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/") for path in paths):
        base.fail(f"{scope} candidate is missing frozen glib vendor subtree")


def _require_protocol_inputs(paths: set[str], scope: str) -> None:
    missing = S1_006_MARKER_PATHS - paths
    if missing:
        base.fail(
            f"{scope} candidate is missing canonical S1-006 protocol inputs: "
            + ", ".join(sorted(missing))
        )


def _require_state_inputs(paths: set[str], scope: str) -> None:
    missing = S1_007_MARKER_PATHS - paths
    if missing:
        base.fail(
            f"{scope} candidate is missing canonical S1-007 state inputs: "
            + ", ".join(sorted(missing))
        )


def classify_stage(paths: set[str]) -> str:
    if paths & S1_008_MARKER_PATHS:
        _require_state_inputs(paths, "S1-008 process")
        _require_protocol_inputs(paths, "S1-008 process")
        _require_component_inputs(paths, "S1-008 process")
        return PROCESS_STAGE

    state_markers = paths & S1_007_MARKER_PATHS
    if state_markers:
        missing = S1_007_MARKER_PATHS - paths
        if missing:
            base.fail(
                "partial S1-007 state candidate is prohibited; missing: "
                + ", ".join(sorted(missing))
            )
        _require_protocol_inputs(paths, "S1-007 state")
        _require_component_inputs(paths, "S1-007 state")
        return STATE_STAGE

    markers = paths & S1_006_MARKER_PATHS
    if markers:
        missing = S1_006_MARKER_PATHS - paths
        if missing:
            base.fail(
                "partial S1-006 protocol candidate is prohibited; missing: "
                + ", ".join(sorted(missing))
            )
        _require_component_inputs(paths, "S1-006 protocol")
        return PROTOCOL_STAGE

    return base.classify_stage(paths - EXTENSION_CONTROLLED_PATHS)


def validate_allowed_paths(paths: set[str], stage: str) -> None:
    if stage not in {PROTOCOL_STAGE, STATE_STAGE, PROCESS_STAGE}:
        base.validate_allowed_paths(paths - EXTENSION_CONTROLLED_PATHS, stage)
        return

    allowed = {path for path in paths if base.is_common_allowed(path)}
    allowed |= EXTENSION_CONTROLLED_PATHS
    allowed |= base.STAGE_B_ALL_PATHS
    allowed |= S1_006_ALLOWED_PATHS
    if stage in {STATE_STAGE, PROCESS_STAGE}:
        allowed |= S1_007_ALLOWED_PATHS
    if stage == PROCESS_STAGE:
        allowed |= S1_008_ALLOWED_PATHS
    allowed |= {
        path
        for path in paths
        if path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/")
    }

    unexpected = sorted(paths - allowed)
    if unexpected:
        scope = {
            PROTOCOL_STAGE: "S1-006",
            STATE_STAGE: "S1-007",
            PROCESS_STAGE: "S1-008",
        }[stage]
        base.fail(f"tracked path outside {scope} allowlist: " + ", ".join(unexpected))

    missing = sorted(base.REQUIRED_PATHS - paths)
    if missing:
        base.fail("required canonical path missing: " + ", ".join(missing))

    extra_root_src = sorted(
        path for path in paths if path.startswith("src/") and path != "src/.gitkeep"
    )
    if extra_root_src:
        base.fail(
            "root src/ remains a historical placeholder only: "
            + ", ".join(extra_root_src)
        )


def verify_policy_workflows(view: base.RepositoryView) -> None:
    for relative, expected_sha in sorted(EXPECTED_WORKFLOW_SHA256.items()):
        data = view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected_sha:
            base.fail(
                f"exact workflow bytes drifted: {relative}: "
                f"expected={expected_sha} actual={actual}"
            )


def verify_extension_controlled_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(EXTENSION_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled S1 execution policy path changed: {relative}")


def _verify_component_base(
    view: base.RepositoryView,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    expected_text = dict(base.STAGE_B_TEXT)
    expected_text["Cargo.toml"] = base.ROOT_CARGO_COMPONENT
    expected_text.pop("crates/contracts/src/lib.rs")
    if allow_core_main_change:
        expected_text.pop("crates/core/src/main.rs")

    for relative, expected in expected_text.items():
        base.read_text_exact(view, relative, expected)

    lock_bytes = view.read_bytes(base.STAGE_B_LOCK_PATH, base.MAX_LOCKFILE_BYTES)
    base.require_frozen_component_lock_identity(lock_bytes)
    base.validate_lock_bytes(lock_bytes, allow_frozen_glib=True)
    base.verify_frozen_glib_vendor(view, paths, base.COMPONENT_STAGE)


def _blank_non_newlines(text: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in text)


def strip_rust_comments_and_strings(text: str) -> str:
    """Blank Rust comments and string literals while preserving code offsets."""

    out: list[str] = []
    i = 0
    length = len(text)
    while i < length:
        if text.startswith("//", i):
            end = text.find("\n", i + 2)
            if end == -1:
                out.append(" " * (length - i))
                break
            out.append(" " * (end - i))
            out.append("\n")
            i = end + 1
            continue

        if text.startswith("/*", i):
            start = i
            depth = 1
            i += 2
            while i < length and depth:
                if text.startswith("/*", i):
                    depth += 1
                    i += 2
                elif text.startswith("*/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            if depth != 0:
                base.fail("unterminated block comment")
            out.append(_blank_non_newlines(text[start:i]))
            continue

        raw = RAW_STRING_PREFIX.match(text, i)
        if raw is not None:
            start = i
            hashes = raw.group(1)
            i = raw.end()
            close = '"' + hashes
            end = text.find(close, i)
            if end == -1:
                base.fail("unterminated raw string literal")
            i = end + len(close)
            out.append(_blank_non_newlines(text[start:i]))
            continue

        if text.startswith('b"', i) or text[i] == '"':
            start = i
            i += 2 if text.startswith('b"', i) else 1
            escaped = False
            closed = False
            while i < length:
                char = text[i]
                i += 1
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    closed = True
                    break
            if not closed:
                base.fail("unterminated string literal")
            out.append(_blank_non_newlines(text[start:i]))
            continue

        out.append(text[i])
        i += 1

    return "".join(out)


def _read_rust(
    view: base.RepositoryView,
    relative: str,
    max_bytes: int,
    scope: str,
) -> tuple[str, str]:
    data = view.read_bytes(relative, max_bytes)
    try:
        raw = data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"{scope} Rust source is not UTF-8: {relative}: {exc}")
    if "\x00" in raw:
        base.fail(f"{scope} Rust source contains NUL: {relative}")
    return raw, strip_rust_comments_and_strings(raw)


def _require_forbid(code: str, relative: str, scope: str) -> None:
    if FORBID_UNSAFE_ATTRIBUTE.match(code.lstrip()) is None:
        base.fail(
            f"{scope} crate/test root must begin with an actual "
            f"#![forbid(unsafe_code)] attribute: {relative}"
        )


def _reject_identifiers(
    relative: str,
    code: str,
    forbidden_identifiers: frozenset[str],
    scope: str,
) -> None:
    if PATH_ATTRIBUTE.search(code):
        base.fail(f"{scope} #[path] module indirection is prohibited: {relative}")
    identifiers = set(RUST_IDENTIFIER.findall(code))
    forbidden = sorted(identifiers & forbidden_identifiers)
    if forbidden:
        base.fail(
            f"{scope} prohibited effect identifier(s) found in code: "
            f"{relative}: {', '.join(forbidden)}"
        )


def verify_protocol_sources(view: base.RepositoryView) -> None:
    code_by_path: dict[str, str] = {}
    for relative in sorted(S1_006_ALLOWED_PATHS):
        _, code = _read_rust(view, relative, MAX_S1_006_SOURCE_BYTES, "S1-006")
        code_by_path[relative] = code
    _require_forbid(code_by_path["crates/contracts/src/lib.rs"], "crates/contracts/src/lib.rs", "S1-006")
    _require_forbid(code_by_path["crates/contracts/tests/protocol_v1.rs"], "crates/contracts/tests/protocol_v1.rs", "S1-006")
    for relative, code in code_by_path.items():
        _reject_identifiers(relative, code, PROHIBITED_EFFECT_IDENTIFIERS, "S1-006")


def verify_state_sources(view: base.RepositoryView) -> None:
    code_by_path: dict[str, str] = {}
    for relative in sorted(S1_007_ALLOWED_PATHS):
        _, code = _read_rust(view, relative, MAX_S1_007_SOURCE_BYTES, "S1-007")
        code_by_path[relative] = code
    _require_forbid(code_by_path["crates/core/src/lib.rs"], "crates/core/src/lib.rs", "S1-007")
    _require_forbid(code_by_path["crates/core/tests/state_v1.rs"], "crates/core/tests/state_v1.rs", "S1-007")
    for relative, code in code_by_path.items():
        _reject_identifiers(relative, code, S1_007_PROHIBITED_EFFECT_IDENTIFIERS, "S1-007")


def verify_process_sources(view: base.RepositoryView) -> None:
    main_path = "crates/core/src/main.rs"
    test_path = "crates/core/tests/process_v1.rs"
    _, main_code = _read_rust(view, main_path, MAX_S1_008_SOURCE_BYTES, "S1-008")
    raw_test, test_code = _read_rust(view, test_path, MAX_S1_008_SOURCE_BYTES, "S1-008")

    _require_forbid(main_code, main_path, "S1-008")
    _require_forbid(test_code, test_path, "S1-008")
    _reject_identifiers(
        main_path,
        main_code,
        S1_008_MAIN_PROHIBITED_IDENTIFIERS,
        "S1-008 Core main",
    )

    framed_helpers = list(S1_008_MAIN_FRAMED_OUTPUT_HELPER.finditer(main_code))
    if len(framed_helpers) != 1:
        base.fail(
            "S1-008 Core main must contain exactly one canonical typed framed-output helper"
        )
    helper = framed_helpers[0]
    scrubbed_main = (
        main_code[: helper.start()]
        + _blank_non_newlines(main_code[helper.start() : helper.end()])
        + main_code[helper.end() :]
    )
    _reject_identifiers(
        main_path,
        scrubbed_main,
        S1_008_MAIN_OUTPUT_ESCAPE_IDENTIFIERS,
        "S1-008 Core main output",
    )

    process_imports = list(S1_008_TEST_PROCESS_IMPORT.finditer(test_code))
    owned_launches = list(S1_008_TEST_OWNED_LAUNCH_SCRUBBED.finditer(test_code))
    if len(process_imports) != 1 or len(owned_launches) != 1:
        base.fail(
            "S1-008 process test must use exactly one std::process import "
            "and one owned Core binary launcher"
        )

    owned_launch = owned_launches[0]
    raw_owned_launch = raw_test[owned_launch.start() : owned_launch.end()]
    if S1_008_TEST_OWNED_LAUNCH_RAW.fullmatch(raw_owned_launch) is None:
        base.fail(
            "S1-008 process test launcher must target exactly "
            'env!("CARGO_BIN_EXE_wepld-core")'
        )

    scrubbed_test = S1_008_TEST_PROCESS_IMPORT.sub(" ", test_code, count=1)
    scrubbed_test = S1_008_TEST_OWNED_LAUNCH_SCRUBBED.sub(" ", scrubbed_test, count=1)
    remaining = set(RUST_IDENTIFIER.findall(scrubbed_test))
    escaped = sorted(
        remaining
        & (
            {"process", "Command", "env", "option_env"}
            | S1_008_TEST_FORBIDDEN_COMMAND_MODIFIERS
        )
    )
    if escaped:
        base.fail(
            "S1-008 process test escaped owned-binary launch boundary: "
            + ", ".join(escaped)
        )
    _reject_identifiers(
        test_path,
        scrubbed_test,
        S1_008_TEST_PROHIBITED_IDENTIFIERS,
        "S1-008 process test",
    )


def freeze_s1_005_evidence(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    for relative in sorted(S1_006_FROZEN_EVIDENCE_PATHS):
        if candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
            relative, base.MAX_POLICY_FILE_BYTES
        ):
            base.fail(f"S1 candidate changed frozen S1-005 evidence: {relative}")


def freeze_s1_006_protocol(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    for relative in sorted(S1_007_FROZEN_PROTOCOL_PATHS):
        if candidate.read_bytes(relative, MAX_S1_006_SOURCE_BYTES) != policy_base.read_bytes(
            relative, MAX_S1_006_SOURCE_BYTES
        ):
            base.fail(f"S1-007+ candidate changed frozen S1-006 protocol: {relative}")


def freeze_s1_007_state(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    for relative in sorted(S1_008_FROZEN_STATE_PATHS):
        if candidate.read_bytes(relative, MAX_S1_007_SOURCE_BYTES) != policy_base.read_bytes(
            relative, MAX_S1_007_SOURCE_BYTES
        ):
            base.fail(f"S1-008 candidate changed frozen S1-007 state: {relative}")


def verify_view(
    view: base.RepositoryView,
    *,
    policy_base: base.RepositoryView | None = None,
) -> str:
    paths = base.validate_entries(view.entries())
    stage = classify_stage(paths)
    validate_allowed_paths(paths, stage)

    if view.read_bytes("src/.gitkeep", 1):
        base.fail("src/.gitkeep must be empty")

    base.verify_reviewer_configs(view)
    base.verify_dependency_register(view)
    base.verify_archive(view)
    verify_policy_workflows(view)

    if stage in {PROTOCOL_STAGE, STATE_STAGE, PROCESS_STAGE}:
        _verify_component_base(
            view,
            paths,
            allow_core_main_change=(stage == PROCESS_STAGE),
        )
        verify_protocol_sources(view)
        if stage in {STATE_STAGE, PROCESS_STAGE}:
            verify_state_sources(view)
        if stage == PROCESS_STAGE:
            verify_process_sources(view)
    else:
        base.verify_frozen_glib_vendor(view, paths, stage)
        base.verify_stage_b_templates(view, stage)

    if any(path.startswith(".github/repair-payload/") for path in paths):
        base.fail("repair payload leaked into active tree")
    if "docs/canonical/CODEX_SECURITY_REVIEW_POLICY.md" in paths:
        base.fail("duplicate canonical security-review policy detected")
    for path in paths:
        name = base.PurePosixPath(path).name
        if (
            path.startswith(".github/workflows/")
            and (
                name.startswith("repair-canonical-archive")
                or name.startswith("finalize-canonical-archive")
            )
            and (name.endswith(".yml") or name.endswith(".yaml"))
        ):
            base.fail(f"temporary repair workflow leaked into active tree: {path}")

    if policy_base is not None:
        base.verify_base_path_preservation(paths, base.validate_entries(policy_base.entries()))
        base.compare_base_controlled(view, policy_base)
        verify_extension_controlled_paths(view, policy_base)
        if stage in {PROTOCOL_STAGE, STATE_STAGE, PROCESS_STAGE}:
            freeze_s1_005_evidence(view, policy_base)
        if stage in {STATE_STAGE, PROCESS_STAGE}:
            freeze_s1_006_protocol(view, policy_base)
        if stage == PROCESS_STAGE:
            freeze_s1_007_state(view, policy_base)

    return stage


def _framed_helper_fixture() -> bytes:
    return b"""fn write_protocol_frame(
    stdout: &mut ::std::io::StdoutLock<'_>,
    envelope: &::wepld_contracts::ProtocolEnvelope,
) -> Result<(), ::wepld_contracts::FrameError> {
    let wire = ::wepld_contracts::encode_frame(envelope)?;
    ::std::io::Write::write_all(stdout, &wire)
        .map_err(|error| ::wepld_contracts::FrameError::Io { kind: error.kind() })?;
    ::std::io::Write::flush(stdout)
        .map_err(|error| ::wepld_contracts::FrameError::Io { kind: error.kind() })
}
"""


def selftest() -> None:
    base.selftest()

    base_paths = set(base.REQUIRED_PATHS) | {"README.md", "src/.gitkeep"}
    component_paths = (
        base_paths
        | set(base.STAGE_B_ALL_PATHS)
        | {base.FROZEN_GLIB_VENDOR_PREFIX + "/src/variant_iter.rs"}
        | set(EXTENSION_CONTROLLED_PATHS)
    )
    protocol_paths = component_paths | set(S1_006_MARKER_PATHS)
    state_paths = protocol_paths | set(S1_007_MARKER_PATHS)
    process_paths = state_paths | set(S1_008_MARKER_PATHS)
    if classify_stage(component_paths) != base.COMPONENT_STAGE:
        base.fail("S1 self-test: component-stage compatibility failed")
    if classify_stage(protocol_paths) != PROTOCOL_STAGE:
        base.fail("S1 self-test: protocol-stage classification failed")
    validate_allowed_paths(protocol_paths, PROTOCOL_STAGE)
    if classify_stage(state_paths) != STATE_STAGE:
        base.fail("S1 self-test: state-stage classification failed")
    validate_allowed_paths(state_paths, STATE_STAGE)
    if classify_stage(process_paths) != PROCESS_STAGE:
        base.fail("S1 self-test: process-stage classification failed")
    validate_allowed_paths(process_paths, PROCESS_STAGE)
    base.expect_failure_matching(
        "extra S1-008 runtime module",
        "tracked path outside S1-008 allowlist",
        validate_allowed_paths,
        process_paths | {"crates/core/src/process.rs"},
        PROCESS_STAGE,
    )
    base.expect_failure_matching(
        "S1-008 missing S1-007 state",
        "S1-008 process candidate is missing canonical S1-007 state inputs",
        classify_stage,
        protocol_paths | set(S1_008_MARKER_PATHS),
    )

    safe_protocol = {
        "crates/contracts/src/lib.rs": b"#![forbid(unsafe_code)]\n",
        "crates/contracts/src/frame.rs": b"pub fn frame() {}\n",
        "crates/contracts/src/protocol.rs": b"pub fn protocol() {}\n",
        "crates/contracts/tests/protocol_v1.rs": b"#![forbid(unsafe_code)]\n",
    }
    verify_protocol_sources(base.MemoryView(safe_protocol))
    bad_protocol = dict(safe_protocol)
    bad_protocol["crates/contracts/src/frame.rs"] = b"use std::net::TcpStream;\n"
    base.expect_failure_matching(
        "network effect in S1-006",
        "S1-006 prohibited effect identifier(s) found in code",
        verify_protocol_sources,
        base.MemoryView(bad_protocol),
    )

    safe_state = {
        "crates/core/src/lib.rs": b"#![forbid(unsafe_code)]\npub mod state;\n",
        "crates/core/src/state.rs": b"pub fn pure_state() {}\n",
        "crates/core/tests/state_v1.rs": b"#![forbid(unsafe_code)]\n",
    }
    verify_state_sources(base.MemoryView(safe_state))
    bad_state = dict(safe_state)
    bad_state["crates/core/src/state.rs"] = b"use std::process::Command;\n"
    base.expect_failure_matching(
        "process effect in S1-007",
        "S1-007 prohibited effect identifier(s) found in code",
        verify_state_sources,
        base.MemoryView(bad_state),
    )
    cfg_path_state = dict(safe_state)
    cfg_path_state["crates/core/src/state.rs"] = (
        b'#[cfg_attr(all(), path = "other.rs")]\nmod hidden;\n'
    )
    base.expect_failure_matching(
        "cfg_attr path in S1-007",
        "S1-007 prohibited effect identifier(s) found in code",
        verify_state_sources,
        base.MemoryView(cfg_path_state),
    )

    intended_launcher = 'Command::new(env!("CARGO_BIN_EXE_wepld-core"))'
    stripped_launcher = strip_rust_comments_and_strings(intended_launcher)
    structural = S1_008_TEST_OWNED_LAUNCH_SCRUBBED.fullmatch(stripped_launcher)
    if structural is None:
        base.fail("S1-008 self-test: scrubbed owned-binary launcher did not match")
    if len(stripped_launcher) != len(intended_launcher):
        base.fail("S1-008 self-test: launcher scrubbing changed offsets")
    raw_span = intended_launcher[structural.start() : structural.end()]
    if S1_008_TEST_OWNED_LAUNCH_RAW.fullmatch(raw_span) is None:
        base.fail("S1-008 self-test: raw owned-binary launcher validation failed")

    safe_main = (
        b"#![forbid(unsafe_code)]\n"
        + _framed_helper_fixture()
        + b"fn main() { let _ = (::std::io::stdin(), ::std::io::stdout(), ::std::io::stderr()); eprintln!(\"diag\"); }\n"
    )
    safe_test = (
        b"#![forbid(unsafe_code)]\n"
        b"use std::process::{Child, Command, Stdio};\n"
        b"use std::thread;\n"
        b"fn spawn_core() -> Child { "
        b"Command::new(env!(\"CARGO_BIN_EXE_wepld-core\"))"
        b".stdin(Stdio::piped()).stdout(Stdio::piped()).spawn().unwrap() }\n"
        b"fn probe() { let _ = spawn_core(); thread::yield_now(); }\n"
    )
    safe_process = {
        "crates/core/src/main.rs": safe_main,
        "crates/core/tests/process_v1.rs": safe_test,
    }
    verify_process_sources(base.MemoryView(safe_process))

    shadow_contracts = dict(safe_process)
    shadow_contracts["crates/core/src/main.rs"] = safe_main + (
        b"mod wepld_contracts { pub struct ProtocolEnvelope; }\n"
    )
    base.expect_failure_matching(
        "local contracts namespace shadow in S1-008 main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(shadow_contracts),
    )

    shadow_std = dict(safe_process)
    shadow_std["crates/core/src/main.rs"] = safe_main + b"mod std { pub mod io {} }\n"
    base.expect_failure_matching(
        "local std namespace shadow in S1-008 main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(shadow_std),
    )

    extern_rebind = dict(safe_process)
    extern_rebind["crates/core/src/main.rs"] = safe_main + (
        b"extern crate self as alternate_contracts;\n"
    )
    base.expect_failure_matching(
        "extern namespace rebinding in S1-008 main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(extern_rebind),
    )

    arbitrary_command = dict(safe_process)
    arbitrary_command["crates/core/tests/process_v1.rs"] = safe_test + (
        b"fn escape() { let _ = Command::new(\"curl\"); }\n"
    )
    base.expect_failure_matching(
        "arbitrary command in S1-008 test",
        "S1-008 process test escaped owned-binary launch boundary",
        verify_process_sources,
        base.MemoryView(arbitrary_command),
    )

    wrong_target = dict(safe_process)
    wrong_target["crates/core/tests/process_v1.rs"] = safe_test.replace(
        b"CARGO_BIN_EXE_wepld-core", b"OTHER_BINARY"
    )
    base.expect_failure_matching(
        "wrong owned binary target",
        "S1-008 process test launcher must target exactly",
        verify_process_sources,
        base.MemoryView(wrong_target),
    )

    arg_escape = dict(safe_process)
    arg_escape["crates/core/tests/process_v1.rs"] = safe_test.replace(
        b".stdin(Stdio::piped())", b".arg(\"--escape\").stdin(Stdio::piped())"
    )
    base.expect_failure_matching(
        "argument escape in S1-008 test",
        "S1-008 process test escaped owned-binary launch boundary",
        verify_process_sources,
        base.MemoryView(arg_escape),
    )

    env_escape = dict(safe_process)
    env_escape["crates/core/tests/process_v1.rs"] = safe_test + (
        b"fn escape() { let _ = std::env::vars(); }\n"
    )
    base.expect_failure_matching(
        "environment escape in S1-008 test",
        "S1-008 process test escaped owned-binary launch boundary",
        verify_process_sources,
        base.MemoryView(env_escape),
    )

    main_network = dict(safe_process)
    main_network["crates/core/src/main.rs"] = safe_main + b"fn escape() { let _ = ::std::net::TcpStream::connect(\"127.0.0.1:1\"); }\n"
    base.expect_failure_matching(
        "network in S1-008 main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(main_network),
    )

    nested_process = dict(safe_process)
    nested_process["crates/core/src/main.rs"] = safe_main + b"fn escape() { let _ = ::std::process::Command::new(\"x\"); }\n"
    base.expect_failure_matching(
        "nested process in S1-008 main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(nested_process),
    )

    println_escape = dict(safe_process)
    println_escape["crates/core/src/main.rs"] = safe_main + b"fn escape() { println!(\"raw\"); }\n"
    base.expect_failure_matching(
        "println stdout escape in S1-008 main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(println_escape),
    )

    write_escape = dict(safe_process)
    write_escape["crates/core/src/main.rs"] = safe_main + (
        b"fn escape() { let mut output = ::std::io::stdout(); "
        b"let _ = ::std::io::Write::write_all(&mut output, b\"raw\"); }\n"
    )
    base.expect_failure_matching(
        "direct write_all stdout escape in S1-008 main",
        "S1-008 Core main output prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(write_escape),
    )

    copy_escape = dict(safe_process)
    copy_escape["crates/core/src/main.rs"] = safe_main + (
        b"fn escape() { let mut input = &b\"raw\"[..]; let mut output = ::std::io::stdout(); "
        b"let _ = ::std::io::copy(&mut input, &mut output); }\n"
    )
    base.expect_failure_matching(
        "io copy stdout escape in S1-008 main",
        "S1-008 Core main output prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(copy_escape),
    )

    test_network = dict(safe_process)
    test_network["crates/core/tests/process_v1.rs"] = safe_test + (
        b"fn escape() { let _ = std::net::TcpStream::connect(\"127.0.0.1:1\"); }\n"
    )
    base.expect_failure_matching(
        "network in S1-008 test",
        "S1-008 process test prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(test_network),
    )

    cfg_path_main = dict(safe_process)
    cfg_path_main["crates/core/src/main.rs"] = safe_main + (
        b'#[cfg_attr(all(), path = "other.rs")]\nmod hidden;\n'
    )
    base.expect_failure_matching(
        "cfg_attr path in S1-008 main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(cfg_path_main),
    )

    print("wepld S1 execution integrity policy self-tests: PASS")


def print_success(stage: str, mode: str) -> None:
    if stage not in {PROTOCOL_STAGE, STATE_STAGE, PROCESS_STAGE}:
        base.print_success(stage, mode)
        return

    print("wepld integrity verification: PASS")
    print(f"mode={mode}")
    print(f"stage={stage}")
    print(f"canonical_archive_sha256={base.EXPECTED_ARCHIVE_SHA256}")
    print(f"master_plan_sha256={base.EXPECTED_PLAN_SHA256}")
    print(f"source_registry_entries={base.EXPECTED_SOURCE_REGISTRY_ENTRIES}")
    print("source_admission=0")
    print("source_acquisition_check=PASS")
    print("runtime_dependency_admission=EXACT_S1_GRAPH")
    print("cubic_provider_effective_state=NOT_PROVEN_SAFE_BY_REPOSITORY_POLICY")
    if stage == PROCESS_STAGE:
        print("product_implementation_authorized=S1_008_ONLY")
    elif stage == STATE_STAGE:
        print("product_implementation_authorized=S1_007_ONLY")
    else:
        print("product_implementation_authorized=S1_006_ONLY")


def main(argv: list[str]) -> int:
    args = base.parse_args(argv)
    try:
        if args.command == "selftest":
            selftest()
            return 0

        token = os.environ.get(args.github_token_env) or None
        client = base.GitHubClient(token)

        if args.command == "verify-local":
            view = base.LocalRepositoryView(Path(args.root))
            stage = verify_view(view)
            if args.remote_baseline:
                base.verify_remote_baseline(
                    client, base.require_comparison_sha(args.pr_base_sha)
                )
            print_success(stage, "LOCAL_CHECKOUT")
            return 0

        policy_base = base.LocalRepositoryView(Path(args.policy_root))
        candidate = base.RemoteRepositoryView(args.repository, args.sha, client)
        stage = verify_view(candidate, policy_base=policy_base)
        base.verify_remote_baseline(client, base.require_comparison_sha(args.pr_base_sha))
        print_success(stage, "REMOTE_CANDIDATE_DATA_ONLY")
        return 0

    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
