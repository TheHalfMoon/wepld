#!/usr/bin/env python3
"""Bounded S1 execution extension over the canonical acquisition integrity policy.

The privileged pull_request_target path still treats candidate Git objects as data only.
Candidate Rust executes only in the separate token-minimal pull_request contracts gate.
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

# `crates/core/src/main.rs` already exists as the frozen Stage-B skeleton. The
# process integration test is the structural marker that upgrades a candidate
# from pure state to the S1-008 Core-process stage. No extra runtime module is
# admitted by this bootstrap.
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

# Defense-in-depth source-scope vocabulary. Checks run only after comments and
# literals are stripped; unsafe code is also rejected by rustc/clippy in the
# separate unprivileged contracts workflow.
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

# The Core child may use inherited stdio and diagnostics stderr, but S1-008
# itself still may not open files, access environment-derived authority, spawn
# child processes, create threads, or use networking/Tauri/async frameworks.
# stdout must remain framed protocol bytes only, so print!/println! stay banned;
# eprint!/eprintln! are allowed solely for diagnostics stderr.
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
    }
)

# The integration test may spawn the owned test binary and use threads/timeouts,
# but it still may not introduce filesystem/network/Tauri/dependency behavior.
S1_008_TEST_PROHIBITED_IDENTIFIERS = frozenset(
    {
        "fs",
        "net",
        "tokio",
        "tauri",
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

FORBID_UNSAFE_ATTRIBUTE = re.compile(
    r"\A#!\s*\[\s*forbid\s*\(\s*unsafe_code\s*\)\s*\]"
)
PATH_ATTRIBUTE = re.compile(r"#\s*\[\s*(?:r#)?path\b")
RUST_IDENTIFIER = re.compile(r"(?:r#)?([A-Za-z_][A-Za-z0-9_]*)")
RAW_STRING_PREFIX = re.compile(r'(?:br|r)(#{0,255})"')


def _require_component_inputs(paths: set[str], scope: str) -> None:
    missing_component = base.STAGE_B_ALL_PATHS - paths
    if missing_component:
        base.fail(
            f"{scope} candidate is missing frozen component inputs: "
            + ", ".join(sorted(missing_component))
        )
    if not any(
        path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/") for path in paths
    ):
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
    process_markers = paths & S1_008_MARKER_PATHS
    if process_markers:
        missing_process = S1_008_MARKER_PATHS - paths
        if missing_process:
            base.fail(
                "partial S1-008 process candidate is prohibited; missing: "
                + ", ".join(sorted(missing_process))
            )
        _require_state_inputs(paths, "S1-008 process")
        _require_protocol_inputs(paths, "S1-008 process")
        _require_component_inputs(paths, "S1-008 process")
        return PROCESS_STAGE

    state_markers = paths & S1_007_MARKER_PATHS
    if state_markers:
        missing_state = S1_007_MARKER_PATHS - paths
        if missing_state:
            base.fail(
                "partial S1-007 state candidate is prohibited; missing: "
                + ", ".join(sorted(missing_state))
            )
        _require_protocol_inputs(paths, "S1-007 state")
        _require_component_inputs(paths, "S1-007 state")
        return STATE_STAGE

    markers = paths & S1_006_MARKER_PATHS
    if markers:
        missing_markers = S1_006_MARKER_PATHS - paths
        if missing_markers:
            base.fail(
                "partial S1-006 protocol candidate is prohibited; missing: "
                + ", ".join(sorted(missing_markers))
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
    """Blank Rust comments and string literals while preserving code/newlines."""

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


def _read_rust_code(
    view: base.RepositoryView,
    paths: frozenset[str],
    max_bytes: int,
    scope: str,
) -> dict[str, str]:
    code_by_path: dict[str, str] = {}
    for relative in sorted(paths):
        data = view.read_bytes(relative, max_bytes)
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"{scope} Rust source is not UTF-8: {relative}: {exc}")
        if "\x00" in text:
            base.fail(f"{scope} Rust source contains NUL: {relative}")
        code_by_path[relative] = strip_rust_comments_and_strings(text)
    return code_by_path


def _require_forbid(code_by_path: dict[str, str], paths: tuple[str, ...], scope: str) -> None:
    for relative in paths:
        code = code_by_path[relative].lstrip()
        if FORBID_UNSAFE_ATTRIBUTE.match(code) is None:
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
    code_by_path = _read_rust_code(
        view, S1_006_ALLOWED_PATHS, MAX_S1_006_SOURCE_BYTES, "S1-006"
    )
    _require_forbid(
        code_by_path,
        ("crates/contracts/src/lib.rs", "crates/contracts/tests/protocol_v1.rs"),
        "S1-006",
    )
    for relative, code in code_by_path.items():
        _reject_identifiers(relative, code, PROHIBITED_EFFECT_IDENTIFIERS, "S1-006")


def verify_state_sources(view: base.RepositoryView) -> None:
    code_by_path = _read_rust_code(
        view, S1_007_ALLOWED_PATHS, MAX_S1_007_SOURCE_BYTES, "S1-007"
    )
    _require_forbid(
        code_by_path,
        ("crates/core/src/lib.rs", "crates/core/tests/state_v1.rs"),
        "S1-007",
    )
    for relative, code in code_by_path.items():
        _reject_identifiers(
            relative, code, S1_007_PROHIBITED_EFFECT_IDENTIFIERS, "S1-007"
        )


def verify_process_sources(view: base.RepositoryView) -> None:
    code_by_path = _read_rust_code(
        view, S1_008_ALLOWED_PATHS, MAX_S1_008_SOURCE_BYTES, "S1-008"
    )
    _require_forbid(
        code_by_path,
        ("crates/core/src/main.rs", "crates/core/tests/process_v1.rs"),
        "S1-008",
    )
    _reject_identifiers(
        "crates/core/src/main.rs",
        code_by_path["crates/core/src/main.rs"],
        S1_008_MAIN_PROHIBITED_IDENTIFIERS,
        "S1-008 Core main",
    )
    _reject_identifiers(
        "crates/core/tests/process_v1.rs",
        code_by_path["crates/core/tests/process_v1.rs"],
        S1_008_TEST_PROHIBITED_IDENTIFIERS,
        "S1-008 process test",
    )


def freeze_s1_005_evidence(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(S1_006_FROZEN_EVIDENCE_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if candidate_bytes != base_bytes:
            base.fail(f"S1 candidate changed frozen S1-005 evidence: {relative}")


def freeze_s1_006_protocol(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(S1_007_FROZEN_PROTOCOL_PATHS):
        candidate_bytes = candidate.read_bytes(relative, MAX_S1_006_SOURCE_BYTES)
        base_bytes = policy_base.read_bytes(relative, MAX_S1_006_SOURCE_BYTES)
        if candidate_bytes != base_bytes:
            base.fail(f"S1-007+ candidate changed frozen S1-006 protocol: {relative}")


def freeze_s1_007_state(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(S1_008_FROZEN_STATE_PATHS):
        candidate_bytes = candidate.read_bytes(relative, MAX_S1_007_SOURCE_BYTES)
        base_bytes = policy_base.read_bytes(relative, MAX_S1_007_SOURCE_BYTES)
        if candidate_bytes != base_bytes:
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
        base.verify_base_path_preservation(
            paths, base.validate_entries(policy_base.entries())
        )
        base.compare_base_controlled(view, policy_base)
        verify_extension_controlled_paths(view, policy_base)
        if stage in {PROTOCOL_STAGE, STATE_STAGE, PROCESS_STAGE}:
            freeze_s1_005_evidence(view, policy_base)
        if stage in {STATE_STAGE, PROCESS_STAGE}:
            freeze_s1_006_protocol(view, policy_base)
        if stage == PROCESS_STAGE:
            freeze_s1_007_state(view, policy_base)

    return stage


def selftest() -> None:
    base.selftest()

    base_paths = set(base.REQUIRED_PATHS) | {"README.md", "src/.gitkeep"}
    component_paths = (
        base_paths
        | set(base.STAGE_B_ALL_PATHS)
        | {base.FROZEN_GLIB_VENDOR_PREFIX + "/src/variant_iter.rs"}
        | set(EXTENSION_CONTROLLED_PATHS)
    )
    if classify_stage(component_paths) != base.COMPONENT_STAGE:
        base.fail("S1 execution self-test: component stage compatibility failed")

    protocol_paths = component_paths | set(S1_006_MARKER_PATHS)
    if classify_stage(protocol_paths) != PROTOCOL_STAGE:
        base.fail("S1 execution self-test: protocol stage classification failed")
    validate_allowed_paths(protocol_paths, PROTOCOL_STAGE)

    one_marker = component_paths | {next(iter(S1_006_MARKER_PATHS))}
    base.expect_failure_matching(
        "partial S1-006 protocol stage",
        "partial S1-006 protocol candidate is prohibited",
        classify_stage,
        one_marker,
    )
    base.expect_failure_matching(
        "extra S1-006 Rust module",
        "tracked path outside S1-006 allowlist",
        validate_allowed_paths,
        protocol_paths | {"crates/contracts/src/extra.rs"},
        PROTOCOL_STAGE,
    )

    state_paths = protocol_paths | set(S1_007_MARKER_PATHS)
    if classify_stage(state_paths) != STATE_STAGE:
        base.fail("S1 execution self-test: state stage classification failed")
    validate_allowed_paths(state_paths, STATE_STAGE)

    one_state_marker = protocol_paths | {next(iter(S1_007_MARKER_PATHS))}
    base.expect_failure_matching(
        "partial S1-007 state stage",
        "partial S1-007 state candidate is prohibited",
        classify_stage,
        one_state_marker,
    )
    base.expect_failure_matching(
        "S1-007 missing S1-006 protocol",
        "S1-007 state candidate is missing canonical S1-006 protocol inputs",
        classify_stage,
        component_paths | set(S1_007_MARKER_PATHS),
    )
    base.expect_failure_matching(
        "extra S1-007 Rust module",
        "tracked path outside S1-007 allowlist",
        validate_allowed_paths,
        state_paths | {"crates/core/src/process.rs"},
        STATE_STAGE,
    )

    process_paths = state_paths | set(S1_008_MARKER_PATHS)
    if classify_stage(process_paths) != PROCESS_STAGE:
        base.fail("S1 execution self-test: process stage classification failed")
    validate_allowed_paths(process_paths, PROCESS_STAGE)
    base.expect_failure_matching(
        "S1-008 missing S1-007 state",
        "S1-008 process candidate is missing canonical S1-007 state inputs",
        classify_stage,
        protocol_paths | set(S1_008_MARKER_PATHS),
    )
    base.expect_failure_matching(
        "extra S1-008 runtime module",
        "tracked path outside S1-008 allowlist",
        validate_allowed_paths,
        process_paths | {"crates/core/src/process.rs"},
        PROCESS_STAGE,
    )

    safe_sources = {
        "crates/contracts/src/lib.rs": b"// policy comment\n#![forbid(unsafe_code)]\n",
        "crates/contracts/src/frame.rs": (
            b'const DOC: &str = "std::net::TcpStream include!(x)";\n'
            b"// use std::{net::TcpStream};\n"
            b"pub fn frame() {}\n"
        ),
        "crates/contracts/src/protocol.rs": b"pub fn protocol() {}\n",
        "crates/contracts/tests/protocol_v1.rs": b"#![forbid(unsafe_code)]\n",
    }
    verify_protocol_sources(base.MemoryView(safe_sources))

    comment_only_forbid = dict(safe_sources)
    comment_only_forbid["crates/contracts/src/lib.rs"] = (
        b"// #![forbid(unsafe_code)]\npub fn not_forbidden() {}\n"
    )
    base.expect_failure_matching(
        "comment-only forbid attribute",
        "must begin with an actual #![forbid(unsafe_code)] attribute",
        verify_protocol_sources,
        base.MemoryView(comment_only_forbid),
    )

    grouped_network_effect = dict(safe_sources)
    grouped_network_effect["crates/contracts/src/frame.rs"] = (
        b"use std::{net::TcpStream};\npub fn frame() {}\n"
    )
    base.expect_failure_matching(
        "grouped network effect in S1-006",
        "S1-006 prohibited effect identifier(s) found in code",
        verify_protocol_sources,
        base.MemoryView(grouped_network_effect),
    )

    spaced_include = dict(safe_sources)
    spaced_include["crates/contracts/src/protocol.rs"] = b'include ! ("other.rs");\n'
    base.expect_failure_matching(
        "spaced include macro in S1-006",
        "S1-006 prohibited effect identifier(s) found in code",
        verify_protocol_sources,
        base.MemoryView(spaced_include),
    )

    path_indirection = dict(safe_sources)
    path_indirection["crates/contracts/src/protocol.rs"] = (
        b'#[path = "other.rs"]\nmod hidden;\n'
    )
    base.expect_failure_matching(
        "path indirection in S1-006",
        "S1-006 #[path] module indirection is prohibited",
        verify_protocol_sources,
        base.MemoryView(path_indirection),
    )

    unterminated_block_comment = dict(safe_sources)
    unterminated_block_comment["crates/contracts/src/protocol.rs"] = (
        b"/* unterminated block comment\nTcpStream\n"
    )
    base.expect_failure_matching(
        "unterminated block comment in S1-006",
        "unterminated block comment",
        verify_protocol_sources,
        base.MemoryView(unterminated_block_comment),
    )

    unterminated_raw_string = dict(safe_sources)
    unterminated_raw_string["crates/contracts/src/protocol.rs"] = b'r#"unterminated\n'
    base.expect_failure_matching(
        "unterminated raw string in S1-006",
        "unterminated raw string literal",
        verify_protocol_sources,
        base.MemoryView(unterminated_raw_string),
    )

    unterminated_string = dict(safe_sources)
    unterminated_string["crates/contracts/src/protocol.rs"] = b'"unterminated\n'
    base.expect_failure_matching(
        "unterminated string in S1-006",
        "unterminated string literal",
        verify_protocol_sources,
        base.MemoryView(unterminated_string),
    )

    safe_state_sources = {
        "crates/core/src/lib.rs": b"#![forbid(unsafe_code)]\npub mod state;\n",
        "crates/core/src/state.rs": b"pub fn pure_state() {}\n",
        "crates/core/tests/state_v1.rs": b"#![forbid(unsafe_code)]\n",
    }
    verify_state_sources(base.MemoryView(safe_state_sources))

    state_process_effect = dict(safe_state_sources)
    state_process_effect["crates/core/src/state.rs"] = (
        b"use std::process::Command;\npub fn pure_state() {}\n"
    )
    base.expect_failure_matching(
        "process effect in S1-007",
        "S1-007 prohibited effect identifier(s) found in code",
        verify_state_sources,
        base.MemoryView(state_process_effect),
    )

    state_path_indirection = dict(safe_state_sources)
    state_path_indirection["crates/core/src/state.rs"] = (
        b'#[path = "other.rs"]\nmod hidden;\n'
    )
    base.expect_failure_matching(
        "path indirection in S1-007",
        "S1-007 #[path] module indirection is prohibited",
        verify_state_sources,
        base.MemoryView(state_path_indirection),
    )

    state_raw_path_indirection = dict(safe_state_sources)
    state_raw_path_indirection["crates/core/src/state.rs"] = (
        b'#[r#path = "other.rs"]\nmod hidden;\n'
    )
    base.expect_failure_matching(
        "raw path indirection in S1-007",
        "S1-007 #[path] module indirection is prohibited",
        verify_state_sources,
        base.MemoryView(state_raw_path_indirection),
    )

    state_cfg_attr_path_indirection = dict(safe_state_sources)
    state_cfg_attr_path_indirection["crates/core/src/state.rs"] = (
        b'#[cfg_attr(all(), path = "other.rs")]\nmod hidden;\n'
    )
    base.expect_failure_matching(
        "cfg_attr path indirection in S1-007",
        "S1-007 prohibited effect identifier(s) found in code",
        verify_state_sources,
        base.MemoryView(state_cfg_attr_path_indirection),
    )

    safe_process_sources = {
        "crates/core/src/main.rs": (
            b"#![forbid(unsafe_code)]\n"
            b"use std::io::{stdin, stdout, stderr};\n"
            b"fn main() { let _ = (stdin(), stdout(), stderr()); eprintln!(\"diag\"); }\n"
        ),
        "crates/core/tests/process_v1.rs": (
            b"#![forbid(unsafe_code)]\n"
            b"use std::process::{Command, Stdio};\n"
            b"use std::thread;\n"
            b"fn probe() { let _ = (Command::new(\"x\"), Stdio::piped()); "
            b"thread::yield_now(); }\n"
        ),
    }
    verify_process_sources(base.MemoryView(safe_process_sources))

    process_network_effect = dict(safe_process_sources)
    process_network_effect["crates/core/src/main.rs"] = (
        b"#![forbid(unsafe_code)]\nuse std::net::TcpStream;\nfn main() {}\n"
    )
    base.expect_failure_matching(
        "network effect in S1-008 Core main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(process_network_effect),
    )

    process_spawn_effect = dict(safe_process_sources)
    process_spawn_effect["crates/core/src/main.rs"] = (
        b"#![forbid(unsafe_code)]\nuse std::process::Command;\nfn main() {}\n"
    )
    base.expect_failure_matching(
        "nested process effect in S1-008 Core main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(process_spawn_effect),
    )

    process_stdout_text_effect = dict(safe_process_sources)
    process_stdout_text_effect["crates/core/src/main.rs"] = (
        b"#![forbid(unsafe_code)]\nfn main() { println!(\"not framed\"); }\n"
    )
    base.expect_failure_matching(
        "unframed stdout text in S1-008 Core main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(process_stdout_text_effect),
    )

    process_test_network_effect = dict(safe_process_sources)
    process_test_network_effect["crates/core/tests/process_v1.rs"] = (
        b"#![forbid(unsafe_code)]\nuse std::net::TcpStream;\n"
    )
    base.expect_failure_matching(
        "network effect in S1-008 process test",
        "S1-008 process test prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(process_test_network_effect),
    )

    process_cfg_attr_path = dict(safe_process_sources)
    process_cfg_attr_path["crates/core/src/main.rs"] = (
        b'#![forbid(unsafe_code)]\n#[cfg_attr(all(), path = "other.rs")]\nmod hidden;\nfn main() {}\n'
    )
    base.expect_failure_matching(
        "cfg_attr path indirection in S1-008 Core main",
        "S1-008 Core main prohibited effect identifier(s) found in code",
        verify_process_sources,
        base.MemoryView(process_cfg_attr_path),
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
