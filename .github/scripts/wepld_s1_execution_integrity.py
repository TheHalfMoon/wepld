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
S1_006_MARKER_PATHS = frozenset(
    {
        "crates/contracts/src/frame.rs",
        "crates/contracts/src/protocol.rs",
        "crates/contracts/tests/protocol_v1.rs",
    }
)
S1_006_ALLOWED_PATHS = S1_006_MARKER_PATHS | {"crates/contracts/src/lib.rs"}
S1_005_EVIDENCE_PATH = (
    "specs/001-desktop-rust-trusted-core-handshake/"
    "s1-005-component-admission-evidence.md"
)
S1_006_FROZEN_EVIDENCE_PATHS = frozenset(
    {"docs/governance/DEPENDENCY_REGISTER.md", S1_005_EVIDENCE_PATH}
)
MAX_S1_006_SOURCE_BYTES = 256_000

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": (
        "ea999efbe2a5b4226eb008d1517469c7ade1d5b99fb9179f3fca6a6c8a17310e"
    ),
    ".github/workflows/s1-admission-integrity.yml": (
        "d3c34c3cfdee9849ca94ede21ea9d20df5d8fe68cabea1e620fe853e029a9e71"
    ),
    CONTRACTS_WORKFLOW: (
        "059b6178d3d6b045ed24715f7eff938f88967c55a5478d1b254c5723a9c8051e"
    ),
}

# Defense-in-depth source-scope vocabulary. This is deliberately checked only
# after comments and literals are stripped, and unsafe code is also rejected by
# the Rust compiler in the separate unprivileged contracts workflow.
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
FORBID_UNSAFE_ATTRIBUTE = re.compile(
    r"\A#!\s*\[\s*forbid\s*\(\s*unsafe_code\s*\)\s*\]"
)
PATH_ATTRIBUTE = re.compile(r"#\s*\[\s*path\b")
RUST_IDENTIFIER = re.compile(r"(?:r#)?([A-Za-z_][A-Za-z0-9_]*)")


def classify_stage(paths: set[str]) -> str:
    markers = paths & S1_006_MARKER_PATHS
    if markers:
        missing_markers = S1_006_MARKER_PATHS - paths
        if missing_markers:
            base.fail(
                "partial S1-006 protocol candidate is prohibited; missing: "
                + ", ".join(sorted(missing_markers))
            )
        missing_component = base.STAGE_B_ALL_PATHS - paths
        if missing_component:
            base.fail(
                "S1-006 protocol candidate is missing frozen component inputs: "
                + ", ".join(sorted(missing_component))
            )
        if not any(
            path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/") for path in paths
        ):
            base.fail("S1-006 protocol candidate is missing frozen glib vendor subtree")
        return PROTOCOL_STAGE

    return base.classify_stage(paths - EXTENSION_CONTROLLED_PATHS)


def validate_allowed_paths(paths: set[str], stage: str) -> None:
    if stage != PROTOCOL_STAGE:
        base.validate_allowed_paths(paths - EXTENSION_CONTROLLED_PATHS, stage)
        return

    allowed = {path for path in paths if base.is_common_allowed(path)}
    allowed |= EXTENSION_CONTROLLED_PATHS
    allowed |= base.STAGE_B_ALL_PATHS
    allowed |= S1_006_ALLOWED_PATHS
    allowed |= {
        path
        for path in paths
        if path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/")
    }

    unexpected = sorted(paths - allowed)
    if unexpected:
        base.fail("tracked path outside S1-006 allowlist: " + ", ".join(unexpected))

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


def verify_protocol_component_base(
    view: base.RepositoryView,
    paths: set[str],
) -> None:
    expected_text = dict(base.STAGE_B_TEXT)
    expected_text["Cargo.toml"] = base.ROOT_CARGO_COMPONENT
    expected_text.pop("crates/contracts/src/lib.rs")

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
            out.append(_blank_non_newlines(text[start:i]))
            continue

        raw = re.match(r"(?:br|r)(#{0,255})\"", text[i:])
        if raw is not None:
            start = i
            hashes = raw.group(1)
            i += raw.end()
            close = '"' + hashes
            end = text.find(close, i)
            i = length if end == -1 else end + len(close)
            out.append(_blank_non_newlines(text[start:i]))
            continue

        if text.startswith('b"', i) or text[i] == '"':
            start = i
            i += 2 if text.startswith('b"', i) else 1
            escaped = False
            while i < length:
                char = text[i]
                i += 1
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    break
            out.append(_blank_non_newlines(text[start:i]))
            continue

        out.append(text[i])
        i += 1

    return "".join(out)


def verify_protocol_sources(view: base.RepositoryView) -> None:
    code_by_path: dict[str, str] = {}
    for relative in sorted(S1_006_ALLOWED_PATHS):
        data = view.read_bytes(relative, MAX_S1_006_SOURCE_BYTES)
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"S1-006 Rust source is not UTF-8: {relative}: {exc}")
        if "\x00" in text:
            base.fail(f"S1-006 Rust source contains NUL: {relative}")
        code_by_path[relative] = strip_rust_comments_and_strings(text)

    for required_forbid in (
        "crates/contracts/src/lib.rs",
        "crates/contracts/tests/protocol_v1.rs",
    ):
        code = code_by_path[required_forbid].lstrip()
        if FORBID_UNSAFE_ATTRIBUTE.match(code) is None:
            base.fail(
                "S1-006 crate/test root must begin with an actual "
                f"#![forbid(unsafe_code)] attribute: {required_forbid}"
            )

    for relative, code in code_by_path.items():
        identifiers = set(RUST_IDENTIFIER.findall(code))
        forbidden = sorted(identifiers & PROHIBITED_EFFECT_IDENTIFIERS)
        if forbidden:
            base.fail(
                "S1-006 prohibited effect identifier(s) found in code: "
                f"{relative}: {', '.join(forbidden)}"
            )
        if PATH_ATTRIBUTE.search(code):
            base.fail(f"S1-006 #[path] module indirection is prohibited: {relative}")


def freeze_s1_005_evidence(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(S1_006_FROZEN_EVIDENCE_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if candidate_bytes != base_bytes:
            base.fail(f"S1-006 candidate changed frozen S1-005 evidence: {relative}")


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

    if stage == PROTOCOL_STAGE:
        verify_protocol_component_base(view, paths)
        verify_protocol_sources(view)
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
        if stage == PROTOCOL_STAGE:
            freeze_s1_005_evidence(view, policy_base)

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

    print("wepld S1 execution integrity policy self-tests: PASS")


def print_success(stage: str, mode: str) -> None:
    if stage != PROTOCOL_STAGE:
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
