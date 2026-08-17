#!/usr/bin/env python3
"""S1-009 Desktop-host admission extension over the frozen S1 execution policy.

The privileged pull_request_target path executes this file only from the trusted
PR base and inspects candidate Git objects as data. Candidate Rust is executed
only by the separate token-minimal pull_request workflow.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

import wepld_integrity as base
import wepld_s1_execution_integrity as prior

POLICY_SCRIPT = ".github/scripts/wepld_s1_desktop_integrity.py"
DESKTOP_STAGE = "S1_DESKTOP_LIFECYCLE_CANDIDATE"

S1_009_MARKER_PATHS = frozenset(
    {
        "apps/desktop/src-tauri/src/lib.rs",
        "apps/desktop/src-tauri/src/core_client.rs",
    }
)
S1_009_ALLOWED_PATHS = S1_009_MARKER_PATHS
S1_009_FROZEN_PROCESS_PATHS = prior.S1_008_ALLOWED_PATHS
EXTENSION_CONTROLLED_PATHS = prior.EXTENSION_CONTROLLED_PATHS | {POLICY_SCRIPT}

MAX_S1_009_SOURCE_BYTES = 384_000
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "7481961447f3cb39f3b7162f04397ce9e2cad9ee"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "e5550d5ea5c40f06a26943ecbc14e21e8e2f619cdb4971a6c63bf55cec5aba69",
    ".github/workflows/s1-admission-integrity.yml": "5cc06a61a0cd228fa40fb422df5b7b4605f4f55367ba538b232466cf561cbb56",
    ".github/workflows/s1-contracts.yml": "827d84ad4ad1aa512c35af055c423365fb47f3cf84cb32b08b9bb65b499db38f",
}

DESKTOP_LIB_PROHIBITED_IDENTIFIERS = frozenset(
    {
        "fs",
        "net",
        "process",
        "env",
        "thread",
        "tokio",
        "tauri",
        "Command",
        "File",
        "OpenOptions",
        "TcpStream",
        "TcpListener",
        "UdpSocket",
        "UnixStream",
        "UnixListener",
        "NamedPipe",
        "include",
        "include_bytes",
        "include_str",
        "path",
        "extern",
    }
)

# S1-009 owns one Desktop-managed Core child and its pipe lifecycle. It may use
# std::process/std::thread/std::sync/std::env::current_exe/path mechanics, but it
# may not acquire filesystem, network, Tauri/UI, shell, or arbitrary-command
# authority. S1-010 owns Tauri/UI; later slices own broader effects.
DESKTOP_CLIENT_PROHIBITED_IDENTIFIERS = frozenset(
    {
        "fs",
        "net",
        "os",
        "tokio",
        "tauri",
        "File",
        "OpenOptions",
        "TcpStream",
        "TcpListener",
        "UdpSocket",
        "UnixStream",
        "UnixListener",
        "NamedPipe",
        "canonicalize",
        "read_link",
        "metadata",
        "symlink_metadata",
        "exists",
        "try_exists",
        "is_file",
        "is_dir",
        "include",
        "include_bytes",
        "include_str",
        "extern",
        "return",
    }
)

DESKTOP_FORBIDDEN_COMMAND_MODIFIERS = (
    "arg",
    "args",
    "env",
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
)

COMMAND_NEW = re.compile(r"\bCommand\s*::\s*new\s*\(")
COMMAND_NEW_REFERENCE = re.compile(r"\bCommand\s*::\s*new\b(?!\s*\()")
COMMAND_ALIAS = re.compile(r"\bCommand\s+as\s+[A-Za-z_][A-Za-z0-9_]*")
COMMAND_TYPE_ALIAS = re.compile(
    r"\btype\s+[A-Za-z_][A-Za-z0-9_]*\s*=\s*(?:(?:::)?std\s*::\s*process\s*::\s*)?Command\b"
)
LITERAL_COMMAND_NEW = re.compile(
    r"\bCommand\s*::\s*new\s*\(\s*(?:b|r|br|rb)?[#]*[\"']"
)
STD_ENV_MEMBER = re.compile(
    r"(?:::)?std\s*::\s*env\s*::\s*([A-Za-z_][A-Za-z0-9_]*)"
)
ENV_IMPORT = re.compile(r"\buse\b[^;]*\benv\b[^;]*;", re.DOTALL)
STD_ALIAS = re.compile(r"\buse\s+(?:::)?std\s+as\s+[A-Za-z_][A-Za-z0-9_]*")
SHELL_OR_PATH_TEXT = re.compile(
    r"(?i)(?:\"PATH\"|\"COMSPEC\"|cmd\.exe|powershell(?:\.exe)?|"
    r"/bin/(?:sh|bash|zsh)|(?:^|[^A-Za-z])sh\s+-c)"
)
CURRENT_EXE = re.compile(r"(?:::)?std\s*::\s*env\s*::\s*current_exe\s*\(")
RESOLVER_DECL = re.compile(
    r"\bfn\s+resolve_owned_core_sibling\s*\(\s*\)[^{]*\{",
    re.MULTILINE,
)
CURRENT_EXE_BINDING = re.compile(
    r"\blet\s+current_exe\s*=\s*(?:::)?std\s*::\s*env\s*::\s*current_exe\s*\(\s*\)"
)
CORE_PARENT_BINDING = re.compile(
    r"\blet\s+core_parent\s*=\s*current_exe\s*\.\s*parent\s*\(\s*\)"
)
CORE_PARENT_JOIN = re.compile(
    r"\bcore_parent\s*\.\s*join\s*\(\s*CORE_EXECUTABLE_FILENAME\s*\)"
)
CORE_FILENAME_DECL = re.compile(
    r"\b(const|static)\s+CORE_EXECUTABLE_FILENAME\s*:\s*&str\s*=\s*\"([^\"]+)\"\s*;"
)
CORE_EXECUTABLE_BINDING = re.compile(
    r"\blet\s+core_executable\s*=\s*resolve_owned_core_sibling\s*\(\s*\)"
)
OWNED_COMMAND_NEW = re.compile(
    r"\bCommand\s*::\s*new\s*\(\s*core_executable\s*\.\s*as_os_str\s*\(\s*\)\s*\)"
)
OWNED_SPAWN_CHAIN = re.compile(
    r"\bCommand\s*::\s*new\s*\(\s*core_executable\s*\.\s*as_os_str\s*\(\s*\)\s*\)"
    r"\s*\.\s*stdin\s*\(\s*Stdio\s*::\s*piped\s*\(\s*\)\s*\)"
    r"\s*\.\s*stdout\s*\(\s*Stdio\s*::\s*piped\s*\(\s*\)\s*\)"
    r"\s*\.\s*stderr\s*\(\s*Stdio\s*::\s*piped\s*\(\s*\)\s*\)"
    r"\s*\.\s*spawn\s*\(\s*\)",
    re.DOTALL,
)
PATH_MUTATION = re.compile(
    r"\b(?:current_exe|core_parent|core_executable)\s*\.\s*"
    r"(?:push|pop|set_file_name|set_extension|as_mut_os_string|clear)\s*\("
)
TEST_MODULE = re.compile(
    r"#\s*\[\s*cfg\s*\(\s*test\s*\)\s*\]\s*mod\s+tests\s*\{",
    re.MULTILINE,
)
MODULE_DECL = re.compile(r"\bmod\s+([A-Za-z_][A-Za-z0-9_]*)")


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _require_process_inputs(paths: set[str], scope: str) -> None:
    missing = prior.S1_008_MARKER_PATHS - paths
    if missing:
        base.fail(
            f"{scope} candidate is missing canonical S1-008 process inputs: "
            + ", ".join(sorted(missing))
        )
    prior._require_state_inputs(paths, scope)
    prior._require_protocol_inputs(paths, scope)
    prior._require_component_inputs(paths, scope)


def classify_stage(paths: set[str]) -> str:
    desktop_markers = paths & S1_009_MARKER_PATHS
    if desktop_markers:
        missing = S1_009_MARKER_PATHS - paths
        if missing:
            base.fail(
                "partial S1-009 Desktop lifecycle candidate is prohibited; missing: "
                + ", ".join(sorted(missing))
            )
        _require_process_inputs(paths, "S1-009 Desktop lifecycle")
        return DESKTOP_STAGE

    return prior.classify_stage(paths - {POLICY_SCRIPT})


def validate_allowed_paths(paths: set[str], stage: str) -> None:
    if stage != DESKTOP_STAGE:
        prior.validate_allowed_paths(paths - {POLICY_SCRIPT}, stage)
        return

    allowed = {path for path in paths if base.is_common_allowed(path)}
    allowed |= EXTENSION_CONTROLLED_PATHS
    allowed |= base.STAGE_B_ALL_PATHS
    allowed |= prior.S1_006_ALLOWED_PATHS
    allowed |= prior.S1_007_ALLOWED_PATHS
    allowed |= prior.S1_008_ALLOWED_PATHS
    allowed |= S1_009_ALLOWED_PATHS
    allowed |= {
        path
        for path in paths
        if path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/")
    }

    unexpected = sorted(paths - allowed)
    if unexpected:
        base.fail("tracked path outside S1-009 allowlist: " + ", ".join(unexpected))

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


def verify_policy_files(view: base.RepositoryView) -> None:
    prior_bytes = view.read_bytes(prior.POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    actual_blob = _git_blob_sha1(prior_bytes)
    if actual_blob != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen prior S1 execution policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual_blob}"
        )

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


def _read_desktop_source(
    view: base.RepositoryView, relative: str
) -> tuple[str, str]:
    raw, scrubbed = prior._read_rust(
        view, relative, MAX_S1_009_SOURCE_BYTES, "S1-009"
    )
    prior._require_forbid(raw, relative, "S1-009")
    return raw, scrubbed


def _reject_command_modifiers(relative: str, scrubbed: str) -> None:
    found = []
    for modifier in DESKTOP_FORBIDDEN_COMMAND_MODIFIERS:
        if re.search(rf"\.\s*{re.escape(modifier)}\s*\(", scrubbed):
            found.append(modifier)
    if found:
        base.fail(
            f"S1-009 Desktop launch prohibited Command modifier(s) in {relative}: "
            + ", ".join(sorted(found))
        )


def _function_body(code: str, name: str) -> str:
    match = re.search(rf"\bfn\s+{re.escape(name)}\s*\(\s*\)[^{{]*\{{", code)
    if match is None:
        base.fail(f"S1-009 Desktop client missing required {name}() helper")
    start = match.end()
    depth = 1
    index = start
    while index < len(code):
        char = code[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return code[start:index]
        index += 1
    base.fail(f"S1-009 Desktop client has unterminated {name}() helper")
    raise AssertionError("unreachable")


def _verify_owned_path_resolution(raw_client: str, client_code: str) -> None:
    declarations = CORE_FILENAME_DECL.findall(raw_client)
    if len(declarations) != 2:
        base.fail(
            "S1-009 Desktop client must define exactly two cfg-gated "
            "CORE_EXECUTABLE_FILENAME constants"
        )
    kinds = [kind for kind, _value in declarations]
    values = [value for _kind, value in declarations]
    if kinds != ["const", "const"] or set(values) != {"wepld-core", "wepld-core.exe"}:
        base.fail(
            "S1-009 Desktop Core filename constants must be exactly "
            "wepld-core and wepld-core.exe"
        )

    env_members = STD_ENV_MEMBER.findall(client_code)
    if env_members != ["current_exe"]:
        base.fail(
            "S1-009 Desktop client std::env access must be exactly one current_exe call"
        )
    if ENV_IMPORT.search(client_code) or STD_ALIAS.search(client_code):
        base.fail("S1-009 Desktop client may not alias/import std::env or std")

    resolver_body = _function_body(client_code, "resolve_owned_core_sibling")
    if len(CURRENT_EXE_BINDING.findall(resolver_body)) != 1:
        base.fail(
            "S1-009 Desktop resolver must bind current_exe exactly once from std::env::current_exe"
        )
    if len(CORE_PARENT_BINDING.findall(resolver_body)) != 1:
        base.fail(
            "S1-009 Desktop resolver must bind core_parent exactly once from current_exe.parent()"
        )
    joins = CORE_PARENT_JOIN.findall(resolver_body)
    if len(joins) != 1:
        base.fail(
            "S1-009 Desktop resolver must derive exactly one Core path from "
            "core_parent.join(CORE_EXECUTABLE_FILENAME)"
        )
    if re.search(r"\breturn\b", resolver_body):
        base.fail("S1-009 Desktop resolver may not use early return path substitution")
    tail = resolver_body.rstrip()
    if re.search(
        r"(?:Ok\s*\(\s*)?core_parent\s*\.\s*join\s*\(\s*CORE_EXECUTABLE_FILENAME\s*\)\s*\)?\s*$",
        tail,
    ) is None:
        base.fail(
            "S1-009 Desktop resolver final value must be the owned Core sibling path"
        )

    bindings = re.findall(
        r"\blet\s+(?:mut\s+)?core_executable\s*=", client_code
    )
    if len(bindings) != 1 or "let mut core_executable" in client_code:
        base.fail(
            "S1-009 Desktop client must bind immutable core_executable exactly once"
        )
    if CORE_EXECUTABLE_BINDING.search(client_code) is None:
        base.fail(
            "S1-009 Desktop client must bind core_executable from resolve_owned_core_sibling()"
        )
    if PATH_MUTATION.search(client_code):
        base.fail("S1-009 Desktop owned executable path may not be mutated after derivation")


def verify_desktop_sources(view: base.RepositoryView) -> None:
    lib_path = "apps/desktop/src-tauri/src/lib.rs"
    client_path = "apps/desktop/src-tauri/src/core_client.rs"

    _raw_lib, lib_code = _read_desktop_source(view, lib_path)
    raw_client, client_code = _read_desktop_source(view, client_path)

    prior._reject_identifiers(
        lib_path,
        lib_code,
        DESKTOP_LIB_PROHIBITED_IDENTIFIERS,
        "S1-009 Desktop lib",
    )
    prior._reject_identifiers(
        client_path,
        client_code,
        DESKTOP_CLIENT_PROHIBITED_IDENTIFIERS,
        "S1-009 Desktop client",
    )

    if prior.PATH_ATTRIBUTE.search(lib_code) or prior.PATH_ATTRIBUTE.search(client_code):
        base.fail("S1-009 Desktop source may not use #[path]/cfg_attr path indirection")

    client_modules = MODULE_DECL.findall(client_code)
    if client_modules:
        if client_modules != ["tests"] or TEST_MODULE.search(client_code) is None:
            base.fail(
                "S1-009 Desktop client may declare only one #[cfg(test)] mod tests module"
            )

    if CURRENT_EXE.search(client_code) is None:
        base.fail(
            "S1-009 Desktop client must resolve the owned Core sibling from std::env::current_exe"
        )

    command_sites = list(COMMAND_NEW.finditer(client_code))
    if len(command_sites) != 1:
        base.fail(
            "S1-009 Desktop client must contain exactly one owned Core Command::new launch site"
        )

    raw_client_text = raw_client
    if LITERAL_COMMAND_NEW.search(raw_client_text):
        base.fail("S1-009 Desktop client may not launch a string-literal command")
    if COMMAND_NEW_REFERENCE.search(client_code):
        base.fail("S1-009 Desktop client may not rebind Command::new as a function value")
    if COMMAND_ALIAS.search(client_code) or COMMAND_TYPE_ALIAS.search(client_code):
        base.fail("S1-009 Desktop client may not alias/rebind std::process::Command")
    if SHELL_OR_PATH_TEXT.search(raw_client_text):
        base.fail("S1-009 Desktop client contains shell/PATH launch material")

    _verify_owned_path_resolution(raw_client_text, client_code)

    if OWNED_COMMAND_NEW.search(client_code) is None:
        base.fail(
            "S1-009 Desktop launch must consume the immutable owned Core sibling path"
        )
    if len(OWNED_SPAWN_CHAIN.findall(client_code)) != 1:
        base.fail(
            "S1-009 Desktop launch must pipe stdin/stdout/stderr and spawn exactly once "
            "from the owned Core sibling path"
        )

    _reject_command_modifiers(client_path, client_code)

    required_identifiers = {
        "Child",
        "ChildStdin",
        "ChildStdout",
        "Command",
        "Stdio",
        "thread",
        "mpsc",
    }
    present = {match.group(1) for match in prior.RUST_IDENTIFIER.finditer(client_code)}
    missing = sorted(required_identifiers - present)
    if missing:
        base.fail(
            "S1-009 Desktop client missing required bounded lifecycle primitive(s): "
            + ", ".join(missing)
        )

    lib_modules = MODULE_DECL.findall(lib_code)
    if lib_modules != ["core_client"]:
        base.fail("S1-009 Desktop lib must declare exactly the core_client module")


def freeze_s1_008_process(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(S1_009_FROZEN_PROCESS_PATHS):
        if candidate.read_bytes(relative, prior.MAX_S1_008_SOURCE_BYTES) != policy_base.read_bytes(
            relative, prior.MAX_S1_008_SOURCE_BYTES
        ):
            base.fail(f"S1-009 candidate changed frozen S1-008 process: {relative}")


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
    verify_policy_files(view)

    product_stages = {
        prior.PROTOCOL_STAGE,
        prior.STATE_STAGE,
        prior.PROCESS_STAGE,
        DESKTOP_STAGE,
    }
    if stage in product_stages:
        prior._verify_component_base(
            view,
            paths,
            allow_core_main_change=stage in {prior.PROCESS_STAGE, DESKTOP_STAGE},
        )
        prior.verify_protocol_sources(view)
        if stage in {prior.STATE_STAGE, prior.PROCESS_STAGE, DESKTOP_STAGE}:
            prior.verify_state_sources(view)
        if stage in {prior.PROCESS_STAGE, DESKTOP_STAGE}:
            prior.verify_process_sources(view)
        if stage == DESKTOP_STAGE:
            verify_desktop_sources(view)
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
        if stage in product_stages:
            prior.freeze_s1_005_evidence(view, policy_base)
        if stage in {prior.STATE_STAGE, prior.PROCESS_STAGE, DESKTOP_STAGE}:
            prior.freeze_s1_006_protocol(view, policy_base)
        if stage in {prior.PROCESS_STAGE, DESKTOP_STAGE}:
            prior.freeze_s1_007_state(view, policy_base)
        if stage == DESKTOP_STAGE:
            freeze_s1_008_process(view, policy_base)

    return stage


def selftest() -> None:
    prior.selftest()

    base_paths = set(base.REQUIRED_PATHS) | {"README.md", "src/.gitkeep"}
    component_paths = (
        base_paths
        | set(base.STAGE_B_ALL_PATHS)
        | {base.FROZEN_GLIB_VENDOR_PREFIX + "/src/variant_iter.rs"}
        | set(EXTENSION_CONTROLLED_PATHS)
    )
    protocol_paths = component_paths | set(prior.S1_006_MARKER_PATHS)
    state_paths = protocol_paths | set(prior.S1_007_MARKER_PATHS)
    process_paths = state_paths | set(prior.S1_008_MARKER_PATHS)
    desktop_paths = process_paths | set(S1_009_MARKER_PATHS)

    if classify_stage(process_paths) != prior.PROCESS_STAGE:
        base.fail("S1-009 self-test: prior process-stage compatibility failed")
    validate_allowed_paths(process_paths, prior.PROCESS_STAGE)

    if classify_stage(desktop_paths) != DESKTOP_STAGE:
        base.fail("S1-009 self-test: Desktop-stage classification failed")
    validate_allowed_paths(desktop_paths, DESKTOP_STAGE)

    base.expect_failure_matching(
        "partial S1-009 Desktop candidate",
        "partial S1-009 Desktop lifecycle candidate is prohibited",
        classify_stage,
        process_paths | {"apps/desktop/src-tauri/src/lib.rs"},
    )
    base.expect_failure_matching(
        "extra S1-009 Desktop module",
        "tracked path outside S1-009 allowlist",
        validate_allowed_paths,
        desktop_paths | {"apps/desktop/src-tauri/src/escape.rs"},
        DESKTOP_STAGE,
    )

    safe_lib = b"""#![forbid(unsafe_code)]
mod core_client;
pub use core_client::CoreClient;
"""
    safe_client = b"""#![forbid(unsafe_code)]
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::mpsc;
use std::thread;

#[cfg(target_os = "windows")]
const CORE_EXECUTABLE_FILENAME: &str = "wepld-core.exe";
#[cfg(not(target_os = "windows"))]
const CORE_EXECUTABLE_FILENAME: &str = "wepld-core";

pub struct CoreClient;

fn resolve_owned_core_sibling() -> std::path::PathBuf {
    let current_exe = std::env::current_exe().unwrap();
    let core_parent = current_exe.parent().unwrap();
    core_parent.join(CORE_EXECUTABLE_FILENAME)
}

fn spawn_owned() -> (Child, ChildStdin, ChildStdout) {
    let core_executable = resolve_owned_core_sibling();
    let mut child = Command::new(core_executable.as_os_str())
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let input = child.stdin.take().unwrap();
    let output = child.stdout.take().unwrap();
    let (_tx, _rx) = mpsc::channel::<()>();
    thread::spawn(|| {});
    (child, input, output)
}
"""
    safe = {
        "apps/desktop/src-tauri/src/lib.rs": safe_lib,
        "apps/desktop/src-tauri/src/core_client.rs": safe_client,
    }
    verify_desktop_sources(base.MemoryView(safe))

    network = dict(safe)
    network["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b'fn escape() { let _ = std::net::TcpStream::connect("127.0.0.1:1"); }\n'
    )
    base.expect_failure_matching(
        "network in S1-009 Desktop client",
        "S1-009 Desktop client prohibited effect identifier(s) found in code",
        verify_desktop_sources,
        base.MemoryView(network),
    )

    literal_command = dict(safe)
    literal_command["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"Command::new(core_executable.as_os_str())", b'Command::new("cmd.exe")'
    )
    base.expect_failure_matching(
        "literal command in S1-009 Desktop client",
        "S1-009 Desktop client may not launch a string-literal command",
        verify_desktop_sources,
        base.MemoryView(literal_command),
    )

    argument_escape = dict(safe)
    argument_escape["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b".stdin(Stdio::piped())", b'.arg("--escape").stdin(Stdio::piped())'
    )
    base.expect_failure_matching(
        "argument escape in S1-009 Desktop client",
        "S1-009 Desktop launch prohibited Command modifier(s)",
        verify_desktop_sources,
        base.MemoryView(argument_escape),
    )

    environment_escape = dict(safe)
    environment_escape["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b'fn escape() { let _ = std::env::var("HOME"); }\n'
    )
    base.expect_failure_matching(
        "environment escape in S1-009 Desktop client",
        "S1-009 Desktop client std::env access must be exactly one current_exe call",
        verify_desktop_sources,
        base.MemoryView(environment_escape),
    )

    environment_alias = dict(safe)
    environment_alias["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b"use std::env as host_env;\n"
        b'fn escape() { let _ = host_env::var("HOME"); }\n'
    )
    base.expect_failure_matching(
        "environment alias escape in S1-009 Desktop client",
        "S1-009 Desktop client may not alias/import std::env or std",
        verify_desktop_sources,
        base.MemoryView(environment_alias),
    )

    arbitrary_program = dict(safe)
    arbitrary_program["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"let core_executable = resolve_owned_core_sibling();",
        b'let core_executable = std::path::PathBuf::from("other-program");',
    )
    base.expect_failure_matching(
        "detached Command path in S1-009 Desktop client",
        "S1-009 Desktop client must bind core_executable from resolve_owned_core_sibling()",
        verify_desktop_sources,
        base.MemoryView(arbitrary_program),
    )

    mutable_program = dict(safe)
    mutable_program["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"let core_executable = resolve_owned_core_sibling();",
        b"let mut core_executable = resolve_owned_core_sibling();\n    core_executable.pop();",
    )
    base.expect_failure_matching(
        "mutable owned path in S1-009 Desktop client",
        "S1-009 Desktop client must bind immutable core_executable exactly once",
        verify_desktop_sources,
        base.MemoryView(mutable_program),
    )

    command_alias = dict(safe)
    command_alias["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"Command, Stdio", b"Command as Runner, Stdio"
    ).replace(
        b"Command::new(core_executable.as_os_str())",
        b"Runner::new(core_executable.as_os_str())",
    )
    base.expect_failure_matching(
        "Command alias escape in S1-009 Desktop client",
        "S1-009 Desktop client must contain exactly one owned Core Command::new launch site",
        verify_desktop_sources,
        base.MemoryView(command_alias),
    )

    tauri_escape = dict(safe)
    tauri_escape["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b"fn escape() { let _ = tauri::Builder::default(); }\n"
    )
    base.expect_failure_matching(
        "Tauri leakage into S1-009 Desktop client",
        "S1-009 Desktop client prohibited effect identifier(s) found in code",
        verify_desktop_sources,
        base.MemoryView(tauri_escape),
    )

    module_escape = dict(safe)
    module_escape["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b"mod hidden {}\n"
    )
    base.expect_failure_matching(
        "extra module in S1-009 Desktop client",
        "S1-009 Desktop client may declare only one",
        verify_desktop_sources,
        base.MemoryView(module_escape),
    )

    print("wepld S1 Desktop integrity policy self-tests: PASS")


def print_success(stage: str, mode: str) -> None:
    if stage != DESKTOP_STAGE:
        prior.print_success(stage, mode)
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
    print("product_implementation_authorized=S1_009_ONLY")


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
        base.verify_remote_baseline(
            client, base.require_comparison_sha(args.pr_base_sha)
        )
        print_success(stage, "REMOTE_CANDIDATE_DATA_ONLY")
        return 0

    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))