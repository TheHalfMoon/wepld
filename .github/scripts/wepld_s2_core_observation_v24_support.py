#!/usr/bin/env python3
"""Fail-closed utility helpers for the v24 S2 Core observation successor."""

import hashlib
from typing import Any

import wepld_integrity as base
import wepld_s1_execution_integrity as execution

FORBIDDEN_CORE_TOKENS = (
    b"unsafe {", b"std::process", b"std::net", b"std::env", b"Command::",
    b"TcpStream", b"TcpListener", b"UdpSocket", b"OpenOptions", b"File::create",
    b"File::options", b"fs::write", b"fs::remove", b"fs::rename", b"fs::copy",
    b"create_dir", b"set_permissions", b"hard_link", b"std::thread", b"tokio", b"tauri",
)

def blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def ps(view: Any) -> set[str]:
    return {entry.path for entry in view.entries()}

def mode(view: Any, path: str) -> str:
    for entry in view.entries():
        if entry.path == path:
            return entry.mode
    base.fail(f"missing path: {path}")

def call(label: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(fn):
        base.fail(f"v24 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v24 {label} topology/layout drifted: {exc}")

def attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v24 {label} topology/layout drifted: {exc}")

def bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v24 {label} topology/layout drifted: {exc}")

def extset(component: Any) -> frozenset[str]:
    value = attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v24 extension topology drifted")
    return frozenset(value)

def changed(predecessor: Any, candidate: Any, policy_base: Any) -> frozenset[str]:
    value = call("changed-path", getattr(predecessor, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v24 changed-path topology drifted")
    return frozenset(value)

def verify_core_files(view: Any, core_files: frozenset[str], core_module: str) -> None:
    paths = ps(view)
    for path in sorted(core_files & paths):
        if mode(view, path) != "100644":
            base.fail(f"v24 S2 Core file mode invalid: {path}")
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if not data or b"\x00" in data:
            base.fail(f"v24 S2 Core file invalid: {path}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            base.fail(f"v24 S2 Core file is not UTF-8: {path}")
    if core_module in paths:
        source = view.read_bytes(core_module, base.MAX_POLICY_FILE_BYTES)
        if not source.startswith(b"#![forbid(unsafe_code)]"):
            base.fail("v24 Core project module must forbid unsafe code")
        try:
            scrubbed = execution.strip_rust_comments_and_strings(source.decode("utf-8"))
        except UnicodeDecodeError:
            base.fail(f"v24 S2 Core file is not UTF-8: {core_module}")
        normalized = "".join(scrubbed.split()).encode("utf-8")
        for token in FORBIDDEN_CORE_TOKENS:
            normalized_token = b"".join(token.split())
            if normalized_token in normalized:
                base.fail(
                    "v24 Core observation tranche contains unauthorized runtime effect token: "
                    + token.decode("ascii", errors="replace")
                )
