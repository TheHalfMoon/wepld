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
EXACT_PROCESS_IMPORT = re.compile(
    r"\buse\s+std\s*::\s*process\s*::\s*\{\s*"
    r"Child\s*,\s*ChildStderr\s*,\s*ChildStdin\s*,\s*ChildStdout\s*,\s*Command\s*,\s*Stdio\s*"
    r"\}\s*;"
)
EXACT_SYNC_IMPORT = re.compile(
    r"\buse\s+std\s*::\s*sync\s*::\s*\{\s*Arc\s*,\s*mpsc\s*\}\s*;"
)
EXACT_ATOMIC_IMPORT = re.compile(
    r"\buse\s+std\s*::\s*sync\s*::\s*atomic\s*::\s*\{\s*AtomicBool\s*,\s*Ordering\s*\}\s*;"
)
EXACT_THREAD_IMPORT = re.compile(r"\buse\s+std\s*::\s*thread\s*;")
PROTECTED_LIFECYCLE_DECL = re.compile(
    r"\b(?:struct|enum|union|trait|type|mod)\s+"
    r"(Arc|AtomicBool|Command|Ordering|Stdio|Child|ChildStderr|ChildStdin|ChildStdout|mpsc|thread)\b"
)
PROTECTED_IMPORT_ALIAS = re.compile(
    r"\bas\s+(Arc|AtomicBool|Command|Ordering|Stdio|Child|ChildStderr|ChildStdin|ChildStdout|mpsc|thread)\b"
)
PROTECTED_IMPORT = re.compile(
    r"\buse\b[^;]*\b(Arc|AtomicBool|Command|Ordering|Stdio|Child|ChildStderr|ChildStdin|ChildStdout|mpsc|thread)\b[^;]*;",
    re.DOTALL,
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
RESOLVER_SIGNATURE = re.compile(
    r"\bfn\s+resolve_owned_core_sibling\s*\(\s*\)\s*->\s*"
    r"Result\s*<\s*std\s*::\s*path\s*::\s*PathBuf\s*,\s*CoreClientError\s*>\s*\{"
)
SPAWN_SIGNATURE = re.compile(
    r"\bfn\s+spawn_owned_core\s*\(\s*\)\s*->\s*Result\s*<\s*\(\s*"
    r"Child\s*,\s*ChildStdin\s*,\s*ChildStdout\s*,\s*"
    r"mpsc\s*::\s*Receiver\s*<\s*Vec\s*<\s*u8\s*>\s*>\s*,\s*"
    r"Arc\s*<\s*AtomicBool\s*>\s*,\s*thread\s*::\s*JoinHandle\s*<\s*\(\s*\)\s*>\s*"
    r"\)\s*,\s*CoreClientError\s*>\s*\{",
    re.MULTILINE,
)
STDERR_DRAIN_SIGNATURE = re.compile(
    r"\bfn\s+spawn_stderr_drain\s*\(\s*"
    r"mut\s+stderr\s*:\s*ChildStderr\s*,\s*"
    r"diagnostic_tx\s*:\s*mpsc\s*::\s*SyncSender\s*<\s*Vec\s*<\s*u8\s*>\s*>\s*,\s*"
    r"diagnostics_truncated\s*:\s*Arc\s*<\s*AtomicBool\s*>\s*"
    r"\)\s*->\s*thread\s*::\s*JoinHandle\s*<\s*\(\s*\)\s*>\s*\{",
    re.MULTILINE,
)
CURRENT_EXE_BINDING = re.compile(
    r"\blet\s+current_exe\s*=\s*(?:::)?std\s*::\s*env\s*::\s*current_exe\s*\(\s*\)\s*\?\s*;"
)
CORE_PARENT_BINDING = re.compile(
    r"\blet\s+core_parent\s*=\s*current_exe\s*\.\s*parent\s*\(\s*\)"
    r"\s*\.\s*ok_or\s*\(\s*CoreClientError\s*::\s*MissingExecutableParent\s*\)\s*\?\s*;"
)
CORE_PARENT_JOIN = re.compile(
    r"\bcore_parent\s*\.\s*join\s*\(\s*CORE_EXECUTABLE_FILENAME\s*\)"
)
CORE_FILENAME_DECL = re.compile(
    r"\b(?:const|static)\s+CORE_EXECUTABLE_FILENAME\s*:\s*&str\s*=\s*\"([^\"]+)\"\s*;"
)
WINDOWS_CORE_FILENAME_DECL = re.compile(
    r"#\s*\[\s*cfg\s*\(\s*target_os\s*=\s*\"windows\"\s*\)\s*\]\s*"
    r"const\s+CORE_EXECUTABLE_FILENAME\s*:\s*&str\s*=\s*\"wepld-core\.exe\"\s*;",
    re.MULTILINE,
)
NONWINDOWS_CORE_FILENAME_DECL = re.compile(
    r"#\s*\[\s*cfg\s*\(\s*not\s*\(\s*target_os\s*=\s*\"windows\"\s*\)\s*\)\s*\]\s*"
    r"const\s+CORE_EXECUTABLE_FILENAME\s*:\s*&str\s*=\s*\"wepld-core\"\s*;",
    re.MULTILINE,
)
DIAGNOSTIC_CHANNEL_CAPACITY_DECL = re.compile(
    r"\bconst\s+DIAGNOSTIC_CHANNEL_CAPACITY\s*:\s*usize\s*=\s*16\s*;"
)
DIAGNOSTIC_READ_CHUNK_BYTES_DECL = re.compile(
    r"\bconst\s+DIAGNOSTIC_READ_CHUNK_BYTES\s*:\s*usize\s*=\s*4_096\s*;"
)
MAX_RETAINED_DIAGNOSTIC_BYTES_DECL = re.compile(
    r"\bconst\s+MAX_RETAINED_DIAGNOSTIC_BYTES\s*:\s*usize\s*=\s*"
    r"DIAGNOSTIC_CHANNEL_CAPACITY\s*\*\s*DIAGNOSTIC_READ_CHUNK_BYTES\s*;"
)
CORE_EXECUTABLE_BINDING = re.compile(
    r"\blet\s+core_executable\s*=\s*resolve_owned_core_sibling\s*\(\s*\)\s*\?\s*;"
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
STDERR_TAKE = re.compile(
    r"\blet\s+stderr\s*=\s*child\s*\.\s*stderr\s*\.\s*take\s*\(\s*\)"
    r"\s*\.\s*ok_or\s*\(\s*CoreClientError\s*::\s*MissingChildStderr\s*\)\s*\?\s*;"
)
DIAGNOSTIC_CHANNEL = re.compile(
    r"\blet\s*\(\s*diagnostic_tx\s*,\s*diagnostic_rx\s*\)\s*=\s*"
    r"mpsc\s*::\s*sync_channel\s*\(\s*DIAGNOSTIC_CHANNEL_CAPACITY\s*\)\s*;"
)
DIAGNOSTIC_TRUNCATION_FLAG = re.compile(
    r"\blet\s+diagnostics_truncated\s*=\s*Arc\s*::\s*new\s*\(\s*AtomicBool\s*::\s*new\s*\(\s*false\s*\)\s*\)\s*;"
)
STDERR_DRAIN_CALL = re.compile(
    r"\blet\s+diagnostic_thread\s*=\s*spawn_stderr_drain\s*\(\s*"
    r"stderr\s*,\s*diagnostic_tx\s*,\s*Arc\s*::\s*clone\s*\(\s*&diagnostics_truncated\s*\)\s*"
    r"\)\s*;"
)
SPAWN_RESULT = re.compile(
    r"Ok\s*\(\s*\(\s*child\s*,\s*input\s*,\s*output\s*,\s*diagnostic_rx\s*,\s*"
    r"diagnostics_truncated\s*,\s*diagnostic_thread\s*\)\s*\)\s*$"
)
STDERR_THREAD_SPAWN = re.compile(r"\bthread\s*::\s*spawn\s*\(\s*move\s*\|\|\s*\{")
STDERR_READ = re.compile(
    r"\bstd\s*::\s*io\s*::\s*Read\s*::\s*read\s*\(\s*&mut\s+stderr\s*,\s*&mut\s+buffer\s*\)"
)
STDERR_BUFFER = re.compile(
    r"\blet\s+mut\s+buffer\s*=\s*\[\s*0_u8\s*;\s*DIAGNOSTIC_READ_CHUNK_BYTES\s*\]\s*;"
)
DIAGNOSTIC_TRY_SEND = re.compile(
    r"diagnostic_tx\s*\.\s*try_send\s*\(\s*buffer\s*\[\s*\.\.read\s*\]\s*\.\s*to_vec\s*\(\s*\)\s*\)"
)
TRUNCATION_STORE = re.compile(
    r"diagnostics_truncated\s*\.\s*store\s*\(\s*true\s*,\s*Ordering\s*::\s*Release\s*\)"
)
MAX_DIAGNOSTIC_ASSERT = re.compile(
    r"\bconst\s*:\s*\(\s*\)\s*=\s*assert!\s*\(\s*MAX_RETAINED_DIAGNOSTIC_BYTES\s*==\s*65_536\s*\)\s*;"
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
        base.fail("required canonical path missing: " + ", ".join(sorted(missing)))

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
    match = re.search(rf"\bfn\s+{re.escape(name)}\s*\([^)]*\)[^{{]*\{{", code)
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
    if declarations != ["wepld-core.exe", "wepld-core"]:
        base.fail(
            "S1-009 Desktop Core filename declarations must be exactly the Windows and non-Windows canonical sibling names"
        )
    if len(WINDOWS_CORE_FILENAME_DECL.findall(raw_client)) != 1:
        base.fail(
            "S1-009 Desktop Windows Core filename must be cfg(target_os = windows) wepld-core.exe"
        )
    if len(NONWINDOWS_CORE_FILENAME_DECL.findall(raw_client)) != 1:
        base.fail(
            "S1-009 Desktop non-Windows Core filename must be cfg(not(target_os = windows)) wepld-core"
        )
    if re.search(r"\blet\s+(?:mut\s+)?CORE_EXECUTABLE_FILENAME\b", client_code):
        base.fail("S1-009 Desktop client may not shadow CORE_EXECUTABLE_FILENAME")

    env_members = STD_ENV_MEMBER.findall(client_code)
    if env_members != ["current_exe"]:
        base.fail(
            "S1-009 Desktop client std::env access must be exactly one current_exe call"
        )
    if ENV_IMPORT.search(client_code) or STD_ALIAS.search(client_code):
        base.fail("S1-009 Desktop client may not alias/import std::env or std")

    if len(RESOLVER_SIGNATURE.findall(client_code)) != 1:
        base.fail(
            "S1-009 Desktop client must define exactly one canonical resolve_owned_core_sibling() -> Result<PathBuf, CoreClientError> helper"
        )
    resolver_body = _function_body(client_code, "resolve_owned_core_sibling")
    if len(CURRENT_EXE_BINDING.findall(resolver_body)) != 1:
        base.fail(
            "S1-009 Desktop resolver must bind current_exe exactly from std::env::current_exe()?"
        )
    if len(CORE_PARENT_BINDING.findall(resolver_body)) != 1:
        base.fail(
            "S1-009 Desktop resolver must derive core_parent exactly from current_exe.parent()"
        )
    if len(CORE_PARENT_JOIN.findall(resolver_body)) != 1:
        base.fail(
            "S1-009 Desktop resolver must derive exactly one Core path from core_parent.join(CORE_EXECUTABLE_FILENAME)"
        )
    if len(re.findall(r"\bcurrent_exe\b", resolver_body)) != 3:
        base.fail("S1-009 Desktop resolver may not shadow or reuse current_exe")
    if len(re.findall(r"\bcore_parent\b", resolver_body)) != 2:
        base.fail("S1-009 Desktop resolver may not shadow or reuse core_parent")
    if len(re.findall(r"\bCORE_EXECUTABLE_FILENAME\b", resolver_body)) != 1:
        base.fail("S1-009 Desktop resolver may not shadow or reuse CORE_EXECUTABLE_FILENAME")
    if re.search(r"\blet\s+mut\s+(?:current_exe|core_parent)\b", resolver_body):
        base.fail("S1-009 Desktop resolver path bindings must remain immutable")
    if PATH_MUTATION.search(resolver_body):
        base.fail("S1-009 Desktop resolver may not mutate the owned executable path")
    tail = resolver_body.rstrip()
    if re.search(
        r"Ok\s*\(\s*core_parent\s*\.\s*join\s*\(\s*CORE_EXECUTABLE_FILENAME\s*\)\s*\)\s*$",
        tail,
    ) is None:
        base.fail(
            "S1-009 Desktop resolver final value must be Ok(the owned Core sibling path)"
        )


def _verify_bounded_stderr_drain(client_code: str) -> None:
    if len(DIAGNOSTIC_CHANNEL_CAPACITY_DECL.findall(client_code)) != 1:
        base.fail("S1-009 Desktop diagnostics channel capacity must be exactly 16")
    if len(DIAGNOSTIC_READ_CHUNK_BYTES_DECL.findall(client_code)) != 1:
        base.fail("S1-009 Desktop diagnostic read chunk must be exactly 4096 bytes")
    if len(MAX_RETAINED_DIAGNOSTIC_BYTES_DECL.findall(client_code)) != 1:
        base.fail(
            "S1-009 Desktop max retained diagnostic bytes must derive from channel capacity * chunk bytes"
        )
    if len(MAX_DIAGNOSTIC_ASSERT.findall(client_code)) != 1:
        base.fail("S1-009 Desktop retained diagnostic bound must assert exactly 65536 bytes")
    if len(STDERR_DRAIN_SIGNATURE.findall(client_code)) != 1:
        base.fail(
            "S1-009 Desktop client must define exactly one canonical spawn_stderr_drain helper"
        )

    drain_body = _function_body(client_code, "spawn_stderr_drain")
    if len(STDERR_THREAD_SPAWN.findall(drain_body)) != 1:
        base.fail("S1-009 Desktop stderr drain must own exactly one thread::spawn(move || ...) worker")
    if len(STDERR_BUFFER.findall(drain_body)) != 1:
        base.fail("S1-009 Desktop stderr drain must use the bounded diagnostic read buffer")
    if len(STDERR_READ.findall(drain_body)) != 1:
        base.fail("S1-009 Desktop stderr drain must read only from the owned ChildStderr")
    if len(DIAGNOSTIC_TRY_SEND.findall(drain_body)) != 1:
        base.fail("S1-009 Desktop stderr drain must use nonblocking try_send into the bounded channel")
    if len(TRUNCATION_STORE.findall(drain_body)) != 1:
        base.fail("S1-009 Desktop stderr drain must make dropped diagnostics observable")
    if re.search(r"\bdiagnostic_tx\s*\.\s*send\s*\(", drain_body):
        base.fail("S1-009 Desktop stderr drain may not block on a slow diagnostic consumer")


def _verify_launch_scope(client_code: str) -> None:
    if len(SPAWN_SIGNATURE.findall(client_code)) != 1:
        base.fail(
            "S1-009 Desktop client must define exactly one canonical no-argument spawn_owned_core() Result helper"
        )
    spawn_body = _function_body(client_code, "spawn_owned_core")
    if len(CORE_EXECUTABLE_BINDING.findall(spawn_body)) != 1:
        base.fail(
            "S1-009 Desktop launch helper must bind core_executable exactly from resolve_owned_core_sibling()?"
        )
    if len(re.findall(r"\bresolve_owned_core_sibling\b", spawn_body)) != 1:
        base.fail(
            "S1-009 Desktop launch helper may not shadow or reuse resolve_owned_core_sibling"
        )
    if len(re.findall(r"\bcore_executable\b", spawn_body)) != 2:
        base.fail("S1-009 Desktop launch helper may not shadow or reuse core_executable")
    if re.search(r"\blet\s+mut\s+core_executable\b", spawn_body):
        base.fail("S1-009 Desktop owned executable binding must remain immutable")
    if PATH_MUTATION.search(spawn_body):
        base.fail("S1-009 Desktop owned executable path may not be mutated before launch")
    if len(OWNED_COMMAND_NEW.findall(spawn_body)) != 1:
        base.fail(
            "S1-009 Desktop launch helper must consume the owned Core sibling path exactly once"
        )
    if len(OWNED_SPAWN_CHAIN.findall(spawn_body)) != 1:
        base.fail(
            "S1-009 Desktop launch helper must pipe stdin/stdout/stderr and spawn exactly once from the owned Core sibling path"
        )
    if len(STDERR_TAKE.findall(spawn_body)) != 1:
        base.fail("S1-009 Desktop launch helper must take the piped ChildStderr exactly once")
    if len(DIAGNOSTIC_CHANNEL.findall(spawn_body)) != 1:
        base.fail("S1-009 Desktop launch helper must create exactly one bounded diagnostics sync_channel")
    if len(DIAGNOSTIC_TRUNCATION_FLAG.findall(spawn_body)) != 1:
        base.fail("S1-009 Desktop launch helper must create an observable diagnostic truncation flag")
    if len(STDERR_DRAIN_CALL.findall(spawn_body)) != 1:
        base.fail("S1-009 Desktop launch helper must immediately start the canonical stderr drain")
    if SPAWN_RESULT.search(spawn_body.rstrip()) is None:
        base.fail(
            "S1-009 Desktop launch helper must return the diagnostics receiver, truncation flag, and drain handle to the lifecycle owner"
        )


def _verify_std_lifecycle_bindings(client_code: str) -> None:
    if len(EXACT_PROCESS_IMPORT.findall(client_code)) != 1:
        base.fail(
            "S1-009 Desktop client must import Child/ChildStderr/ChildStdin/ChildStdout/Command/Stdio exactly from std::process"
        )
    if len(EXACT_SYNC_IMPORT.findall(client_code)) != 1:
        base.fail("S1-009 Desktop client must import Arc and mpsc exactly from std::sync")
    if len(EXACT_ATOMIC_IMPORT.findall(client_code)) != 1:
        base.fail("S1-009 Desktop client must import AtomicBool and Ordering exactly from std::sync::atomic")
    if len(EXACT_THREAD_IMPORT.findall(client_code)) != 1:
        base.fail("S1-009 Desktop client must import thread exactly from std")
    if PROTECTED_LIFECYCLE_DECL.search(client_code):
        base.fail("S1-009 Desktop client may not shadow protected lifecycle types/modules")
    if PROTECTED_IMPORT_ALIAS.search(client_code):
        base.fail("S1-009 Desktop client may not alias protected lifecycle imports")

    stripped_imports = EXACT_PROCESS_IMPORT.sub("", client_code)
    stripped_imports = EXACT_SYNC_IMPORT.sub("", stripped_imports)
    stripped_imports = EXACT_ATOMIC_IMPORT.sub("", stripped_imports)
    stripped_imports = EXACT_THREAD_IMPORT.sub("", stripped_imports)
    if PROTECTED_IMPORT.search(stripped_imports):
        base.fail("S1-009 Desktop client may not add alternate protected lifecycle imports")

    if len(re.findall(r"\bCommand\b", client_code)) != 2:
        base.fail(
            "S1-009 Desktop client must reference Command only in the canonical std import and owned launch site"
        )
    if len(re.findall(r"\bStdio\b", client_code)) != 4:
        base.fail(
            "S1-009 Desktop client must reference Stdio only in the canonical std import and three piped streams"
        )


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

    _reject_command_modifiers(client_path, client_code)

    if CURRENT_EXE.search(client_code) is None:
        base.fail(
            "S1-009 Desktop client must resolve the owned Core sibling from std::env::current_exe"
        )

    command_sites = list(COMMAND_NEW.finditer(client_code))
    if len(command_sites) != 1:
        base.fail(
            "S1-009 Desktop client must contain exactly one owned Core Command::new launch site"
        )

    if LITERAL_COMMAND_NEW.search(raw_client):
        base.fail("S1-009 Desktop client may not launch a string-literal command")
    if COMMAND_NEW_REFERENCE.search(client_code):
        base.fail("S1-009 Desktop client may not rebind Command::new as a function value")
    if COMMAND_ALIAS.search(client_code) or COMMAND_TYPE_ALIAS.search(client_code):
        base.fail("S1-009 Desktop client may not alias/rebind std::process::Command")
    if SHELL_OR_PATH_TEXT.search(raw_client):
        base.fail("S1-009 Desktop client contains shell/PATH launch material")

    _verify_std_lifecycle_bindings(client_code)
    _verify_owned_path_resolution(raw_client, client_code)
    _verify_bounded_stderr_drain(client_code)
    _verify_launch_scope(client_code)

    required_identifiers = {
        "Arc",
        "AtomicBool",
        "Child",
        "ChildStderr",
        "ChildStdin",
        "ChildStdout",
        "Command",
        "Ordering",
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
        base.verify_base_path_preservation(paths, base.validate_entries(policy_base.entries()))
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
use std::process::{Child, ChildStderr, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, mpsc};
use std::thread;

#[cfg(target_os = "windows")]
const CORE_EXECUTABLE_FILENAME: &str = "wepld-core.exe";
#[cfg(not(target_os = "windows"))]
const CORE_EXECUTABLE_FILENAME: &str = "wepld-core";
const DIAGNOSTIC_CHANNEL_CAPACITY: usize = 16;
const DIAGNOSTIC_READ_CHUNK_BYTES: usize = 4_096;
const MAX_RETAINED_DIAGNOSTIC_BYTES: usize =
    DIAGNOSTIC_CHANNEL_CAPACITY * DIAGNOSTIC_READ_CHUNK_BYTES;
const _: () = assert!(MAX_RETAINED_DIAGNOSTIC_BYTES == 65_536);

#[derive(Debug)]
enum CoreClientError {
    Io(std::io::Error),
    MissingExecutableParent,
    MissingChildStderr,
}

impl From<std::io::Error> for CoreClientError {
    fn from(error: std::io::Error) -> Self {
        Self::Io(error)
    }
}

pub struct CoreClient;

fn resolve_owned_core_sibling() -> Result<std::path::PathBuf, CoreClientError> {
    let current_exe = std::env::current_exe()?;
    let core_parent = current_exe
        .parent()
        .ok_or(CoreClientError::MissingExecutableParent)?;
    Ok(core_parent.join(CORE_EXECUTABLE_FILENAME))
}

fn spawn_stderr_drain(
    mut stderr: ChildStderr,
    diagnostic_tx: mpsc::SyncSender<Vec<u8>>,
    diagnostics_truncated: Arc<AtomicBool>,
) -> thread::JoinHandle<()> {
    thread::spawn(move || {
        let mut buffer = [0_u8; DIAGNOSTIC_READ_CHUNK_BYTES];
        loop {
            let read = match std::io::Read::read(&mut stderr, &mut buffer) {
                Ok(0) => break,
                Ok(read) => read,
                Err(_) => break,
            };
            if diagnostic_tx.try_send(buffer[..read].to_vec()).is_err() {
                diagnostics_truncated.store(true, Ordering::Release);
            }
        }
    })
}

fn spawn_owned_core() -> Result<
    (
        Child,
        ChildStdin,
        ChildStdout,
        mpsc::Receiver<Vec<u8>>,
        Arc<AtomicBool>,
        thread::JoinHandle<()>,
    ),
    CoreClientError,
> {
    let core_executable = resolve_owned_core_sibling()?;
    let mut child = Command::new(core_executable.as_os_str())
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    let input = child.stdin.take().unwrap();
    let output = child.stdout.take().unwrap();
    let stderr = child
        .stderr
        .take()
        .ok_or(CoreClientError::MissingChildStderr)?;
    let (diagnostic_tx, diagnostic_rx) = mpsc::sync_channel(DIAGNOSTIC_CHANNEL_CAPACITY);
    let diagnostics_truncated = Arc::new(AtomicBool::new(false));
    let diagnostic_thread = spawn_stderr_drain(
        stderr,
        diagnostic_tx,
        Arc::clone(&diagnostics_truncated),
    );
    Ok((
        child,
        input,
        output,
        diagnostic_rx,
        diagnostics_truncated,
        diagnostic_thread,
    ))
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
    argument_escape["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b'fn forbidden_modifier(command: &mut Command) { command.arg("--escape"); }\n'
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

    transformed_current_exe = dict(safe)
    transformed_current_exe["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"let current_exe = std::env::current_exe()?;",
        b'let current_exe = std::env::current_exe()?.join("escape");',
    )
    base.expect_failure_matching(
        "transformed current_exe path",
        "S1-009 Desktop resolver must bind current_exe exactly from std::env::current_exe()?",
        verify_desktop_sources,
        base.MemoryView(transformed_current_exe),
    )

    filename_shadow = dict(safe)
    filename_shadow["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"Ok(core_parent.join(CORE_EXECUTABLE_FILENAME))",
        b'let CORE_EXECUTABLE_FILENAME = "other-program";\n    Ok(core_parent.join(CORE_EXECUTABLE_FILENAME))',
    )
    base.expect_failure_matching(
        "Core filename shadow",
        "S1-009 Desktop client may not shadow CORE_EXECUTABLE_FILENAME",
        verify_desktop_sources,
        base.MemoryView(filename_shadow),
    )

    detached_launch_scope = dict(safe)
    detached_launch_scope["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"fn spawn_owned_core()",
        b"fn spawn_owned_core(core_executable: std::path::PathBuf)",
    ).replace(
        b"    let core_executable = resolve_owned_core_sibling()?;\n",
        b"",
    )
    base.expect_failure_matching(
        "detached launch helper path parameter",
        "S1-009 Desktop client must define exactly one canonical no-argument spawn_owned_core() Result helper",
        verify_desktop_sources,
        base.MemoryView(detached_launch_scope),
    )

    mutable_program = dict(safe)
    mutable_program["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"let core_executable = resolve_owned_core_sibling()?;",
        b"let mut core_executable = resolve_owned_core_sibling()?;\n    core_executable.pop();",
    )
    base.expect_failure_matching(
        "mutable owned path in S1-009 Desktop client",
        "S1-009 Desktop launch helper must bind core_executable exactly from resolve_owned_core_sibling()?",
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

    command_shadow = dict(safe)
    command_shadow["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b"fn shadow() { struct Command; let _ = core::mem::size_of::<Command>(); }\n"
    )
    base.expect_failure_matching(
        "Command shadow in S1-009 Desktop client",
        "S1-009 Desktop client may not shadow protected lifecycle types/modules",
        verify_desktop_sources,
        base.MemoryView(command_shadow),
    )

    alternate_thread_import = dict(safe)
    alternate_thread_import["apps/desktop/src-tauri/src/core_client.rs"] = safe_client + (
        b"use crate::fake as thread;\n"
    )
    base.expect_failure_matching(
        "alternate protected lifecycle import",
        "S1-009 Desktop client may not alias protected lifecycle imports",
        verify_desktop_sources,
        base.MemoryView(alternate_thread_import),
    )

    wrong_cfg = dict(safe)
    wrong_cfg["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b'#[cfg(target_os = "windows")]\nconst CORE_EXECUTABLE_FILENAME: &str = "wepld-core.exe";',
        b'#[cfg(unix)]\nconst CORE_EXECUTABLE_FILENAME: &str = "wepld-core.exe";',
    )
    base.expect_failure_matching(
        "wrong Windows Core filename cfg",
        "S1-009 Desktop Windows Core filename must be cfg(target_os = windows)",
        verify_desktop_sources,
        base.MemoryView(wrong_cfg),
    )

    missing_drain = dict(safe)
    missing_drain["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"    let diagnostic_thread = spawn_stderr_drain(\n        stderr,\n        diagnostic_tx,\n        Arc::clone(&diagnostics_truncated),\n    );\n",
        b"",
    )
    base.expect_failure_matching(
        "missing stderr drain",
        "S1-009 Desktop launch helper must immediately start the canonical stderr drain",
        verify_desktop_sources,
        base.MemoryView(missing_drain),
    )

    unbounded_diagnostics = dict(safe)
    unbounded_diagnostics["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"mpsc::sync_channel(DIAGNOSTIC_CHANNEL_CAPACITY)",
        b"mpsc::channel()",
    )
    base.expect_failure_matching(
        "unbounded diagnostic channel",
        "S1-009 Desktop launch helper must create exactly one bounded diagnostics sync_channel",
        verify_desktop_sources,
        base.MemoryView(unbounded_diagnostics),
    )

    hidden_truncation = dict(safe)
    hidden_truncation["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"diagnostics_truncated.store(true, Ordering::Release);",
        b"let _ = &diagnostics_truncated;",
    )
    base.expect_failure_matching(
        "unobservable diagnostic truncation",
        "S1-009 Desktop stderr drain must make dropped diagnostics observable",
        verify_desktop_sources,
        base.MemoryView(hidden_truncation),
    )

    dropped_observability = dict(safe)
    dropped_observability["apps/desktop/src-tauri/src/core_client.rs"] = safe_client.replace(
        b"        diagnostics_truncated,\n        diagnostic_thread,\n",
        b"        Arc::new(AtomicBool::new(false)),\n        diagnostic_thread,\n",
    )
    base.expect_failure_matching(
        "dropped diagnostic observability",
        "S1-009 Desktop launch helper must return the diagnostics receiver, truncation flag, and drain handle to the lifecycle owner",
        verify_desktop_sources,
        base.MemoryView(dropped_observability),
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
        base.verify_remote_baseline(client, base.require_comparison_sha(args.pr_base_sha))
        print_success(stage, "REMOTE_CANDIDATE_DATA_ONLY")
        return 0

    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))