#!/usr/bin/env python3
"""Fail-closed utility helpers for the v25 S2 identity/store staged successor."""

import hashlib
from typing import Any

import wepld_integrity as base
import wepld_s1_execution_integrity as execution

FORBIDDEN_PRODUCT_TOKENS = (
    b"unsafe {",
    b"std::process",
    b"Command::",
    b"std::net",
    b"TcpStream",
    b"TcpListener",
    b"UdpSocket",
    b"std::env",
    b"remove_file",
    b"remove_dir",
    b"remove_dir_all",
    b"fs::copy",
    b"hard_link",
    b"symlink",
    b"tokio",
    b"tauri",
    b"git2",
    b"rusqlite",
    b"sqlite",
    b"reqwest",
    b"uuid::",
    b"panic!",
    b"unwrap(",
    b"expect(",
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
        base.fail(f"v25 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v25 {label} topology/layout drifted: {exc}")

def attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v25 {label} topology/layout drifted: {exc}")

def bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v25 {label} topology/layout drifted: {exc}")

def extset(component: Any) -> frozenset[str]:
    value = attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v25 extension topology drifted")
    return frozenset(value)

def changed(predecessor: Any, candidate: Any, policy_base: Any) -> frozenset[str]:
    value = call("changed-path", getattr(predecessor, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v25 changed-path topology drifted")
    return frozenset(value)

def verify_text_file(view: Any, path: str) -> bytes:
    if mode(view, path) != "100644":
        base.fail(f"v25 file mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data or b"\x00" in data:
        base.fail(f"v25 file invalid: {path}")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        base.fail(f"v25 file is not UTF-8: {path}")
    return data

def verify_product_modules(view: Any, modules: frozenset[str]) -> None:
    paths = ps(view)
    for path in sorted(modules & paths):
        source = verify_text_file(view, path)
        if not source.startswith(b"#![forbid(unsafe_code)]"):
            base.fail(f"v25 Core product module must forbid unsafe code: {path}")
        try:
            scrubbed = execution.strip_rust_comments_and_strings(source.decode("utf-8"))
        except UnicodeDecodeError:
            base.fail(f"v25 product file is not UTF-8: {path}")
        normalized = "".join(scrubbed.split()).encode("utf-8")
        for token in FORBIDDEN_PRODUCT_TOKENS:
            normalized_token = b"".join(token.split())
            if normalized_token in normalized:
                base.fail(
                    "v25 identity/store tranche contains unauthorized token: "
                    + token.decode("ascii", errors="replace")
                )
