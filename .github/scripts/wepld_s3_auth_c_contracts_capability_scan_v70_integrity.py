#!/usr/bin/env python3
"""Enforce prohibited-capability rejection on the S3 contracts tranche.

v70 is an append-only successor to canonical v69. It preserves every
inherited S1/S2/S3-AUTH-C boundary unchanged - it grants no new authority -
and adds exactly one thing: `crates/contracts/src/s3.rs` and
`crates/contracts/tests/s3_contracts_v1.rs` are scanned for filesystem,
process, network, environment, and platform-API usage before admission, and
`crates/contracts/src/lib.rs` is required to retain `#![forbid(unsafe_code)]`
whenever it is touched alongside the contract module.

This closes a real gap in v69's `_verify_contract_files`: it validated file
shape (mode/non-empty/no-NUL/UTF-8/single export line) but not file
*content*, even though `s1-contracts.yml` runs
`cargo test --package wepld-contracts --all-targets`, which actually
executes whatever lands under `crates/contracts/`. Since S3-AUTH-C's whole
premise is `FILESYSTEM_RUNTIME_AUTHORITY`/`NETWORK_AUTHORITY`/
`WINDOWS_API_AUTHORITY`/`PROCESS_SPAWN_AUTHORITY` = `NONE`, an admission gate
that never inspects contract-file content for those capabilities is a real
mismatch between claimed and enforced authority (CodeRabbit finding on PR
#337, CWE-863).

The bootstrap transition is exactly:
- this v70 policy file;
- foundation-integrity.yml;
- s1-admission-integrity.yml.

No Cargo manifest/lock mutation, `crates/core` runtime behavior, Windows API
binding, process spawn, network, model/provider execution, source
admission, dependency admission, or any S3-AUTH-HOST/OBSERVE/SPAWN
authority is granted by this successor - identical to v69.
"""

from __future__ import annotations

import argparse
import importlib
import re
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s3_auth_c_contracts_capability_scan_v70_integrity.py"
V69 = ".github/scripts/wepld_s3_auth_c_contracts_bootstrap_v69_integrity.py"
V69_BLOB = "b54ece23cd64eebea3c3a13a083c1b090b59c225"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

CONTRACT_MODULE = "crates/contracts/src/s3.rs"
CONTRACT_EXPORT = "crates/contracts/src/lib.rs"
CONTRACT_TEST = "crates/contracts/tests/s3_contracts_v1.rs"
CONTRACT_FILES = frozenset({CONTRACT_MODULE, CONTRACT_EXPORT, CONTRACT_TEST})
CONTRACT_NEW_FILES = frozenset({CONTRACT_MODULE, CONTRACT_TEST})
CONTRACT_PREFIX = "crates/contracts/"
CARGO_MANIFEST = "crates/contracts/Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"
SCANNED_CONTRACT_PATHS = frozenset({CONTRACT_MODULE, CONTRACT_TEST})

AUTHORIZED_TASKS = frozenset(f"S3-C{i:03d}" for i in range(1, 14))

_FORBID_UNSAFE_MARKER = b"#![forbid(unsafe_code)]"
_PROHIBITED_CAPABILITY_PATTERNS: tuple[bytes, ...] = (
    b"std::fs",
    b"std::net",
    b"std::process",
    b"std::os::",
    b"std::env",
    b"windows::",
    b"winapi::",
    b"libc::",
)

OLD_WF = {
    FW: "f2a5a8f85b0bce3b7cc1398aa0f32d67eb3c1f8f14ea8cecec932687743ee206",
    AW: "80250413652ae9bf89ac39e8e363a9684b56336f234b5ed00a5b92121524a949",
}
WF = {
    FW: "be7d361bbd5390c3dd5a080d8dfba3c72090a5fbd1269e2ea73f52fc803394e2",
    AW: "577d181f8d6f9af0df2abb41ac417ff8e961f3c1a791c0032e4e521930a70958",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S3_AUTH_C_CONTRACTS_CAPABILITY_SCAN_SUCCESSOR"
S3_PLANNING_AUTHORITY = "CANONICAL_PRESERVED"
S3_IMPLEMENTATION_AUTHORITY = "EXACT_CONTRACTS_S3_C001_C013_ONLY"
CONTRACT_CAPABILITY_SCAN_AUTHORITY = "ENFORCED"
FILESYSTEM_RUNTIME_AUTHORITY = "NONE"
WINDOWS_API_AUTHORITY = "NONE"
JOB_OBJECT_AUTHORITY = "NONE"
CONTAINMENT_ACTUATION_AUTHORITY = "NONE"
PROCESS_SPAWN_AUTHORITY = "NONE"
CREDENTIAL_AUTHORITY = "NONE"
S3_AUTH_HOST_AUTHORITY = "NOT_GRANTED"
S3_AUTH_OBSERVE_AUTHORITY = "NOT_GRANTED"
S3_AUTH_SPAWN_AUTHORITY = "NOT_GRANTED"
S4_PLUS_AUTHORITY = "NONE"

_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None
_PREDECESSOR_COMPONENT_BASE: Any = None
_PREDECESSOR_FREEZE_S1: Any = None

root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _git_blob(data: bytes) -> str:
    import hashlib

    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


if _git_blob(root.read_bytes(V69, base.MAX_POLICY_FILE_BYTES)) != V69_BLOB:
    base.fail("frozen v69 predecessor drifted")

_V70_ENTRYPOINT = b"wepld_s3_auth_c_contracts_capability_scan_v70_integrity.py"
_V69_ENTRYPOINT = b"wepld_s3_auth_c_contracts_bootstrap_v69_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}


def _v69_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V70_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v70 workflow entrypoint count drifted before v69 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V70_ENTRYPOINT, _V69_ENTRYPOINT)


_TRUE_ORIGINAL_LOCAL_READ_BYTES = base.LocalRepositoryView.read_bytes


def _v69_projected_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
    data = _TRUE_ORIGINAL_LOCAL_READ_BYTES(local_view, relative, limit)
    if relative in (FW, AW):
        data = _v69_workflow_bytes(data, relative)
        if len(data) > limit:
            base.fail(f"v70 v69-projection exceeds read bound: {relative}")
    return data


def _under_v69_workflow_projection(fn: Any, *args: Any, **kwargs: Any) -> Any:
    """Run `fn` while `.github/workflows/{foundation-integrity,s1-admission-integrity}.yml`
    read as their exact canonical v69 (pre-v70-activation) bytes.

    Mirrors v69's own `_under_v68_workflow_projection` exactly, one layer
    up: v69's own module-level code and its `run_predecessor_selftests()`
    both re-derive a v69->v68 workflow projection from the *live* working
    tree at the moment they run, so both call sites need this same
    v70->v69 reversal applied around them. Both call sites share the exact
    same `_v69_projected_read_bytes` function object because v69's own
    `overlay()` identity-checks `base.LocalRepositoryView.read_bytes`
    against the value it captured at its own import time - which, imported
    under this wrapper, is this singleton.
    """
    saved_read_bytes = base.LocalRepositoryView.read_bytes
    base.LocalRepositoryView.read_bytes = _v69_projected_read_bytes
    try:
        return fn(*args, **kwargs)
    finally:
        base.LocalRepositoryView.read_bytes = saved_read_bytes


v69 = _under_v69_workflow_projection(
    importlib.import_module, "wepld_s3_auth_c_contracts_bootstrap_v69_integrity"
)

V25 = v69.V25
_attr = v69._attr
_bind = v69._bind
_call = v69._call

V69_DELTA = v69.delta
V69_BASE = v69.basectrl
V69_ALLOWED = v69.allowed
V69_FILES = v69.files
V69_DEXT = v69.dext
V69_EEXT = v69.eext
V69_EXT = v69.ext
V69_PRINT = v69.printer
V69_COMPONENT_BASE = v69.verify_component_base
V69_FREEZE_STATE = v69.freeze_s1_007_state
V69_WF = dict(v69.WF)
CAND = V25.CAND
RUNTIME = V25.RUNTIME

if V69_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v69 workflow identities drifted before v70 import: actual={V69_WF}")
if _attr(v69, "AUTH", "v69 authority marker") != "S3_AUTH_C_CONTRACTS_ONLY_SUCCESSOR":
    base.fail("v70 observed v69 authority drift")
if _attr(v69, "FILESYSTEM_RUNTIME_AUTHORITY", "v69 filesystem authority") != "NONE":
    base.fail("v70 observed v69 filesystem-authority drift")

_INHERITED_AUTHORITY_NAMES = v69._INHERITED_AUTHORITY_NAMES
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(v69, _name)


def ps(view: Any) -> set[str]:
    return set(V25.ps(view))


def mode(view: Any, path: str) -> str:
    return V25.mode(view, path)


def blob(data: bytes) -> str:
    return V25.blob(data)


def sha(data: bytes) -> str:
    return V25.sha(data)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    return frozenset(V25.changed(V25.v24.v23, candidate, policy_base))


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(V25, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v70 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v70 extension topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def req_v69(view: Any) -> None:
    if V69 not in ps(view):
        base.fail("v70 candidate/base is missing frozen v69 predecessor")
    actual = blob(view.read_bytes(V69, base.MAX_POLICY_FILE_BYTES))
    if actual != V69_BLOB:
        base.fail(f"frozen v69 predecessor drifted: expected={V69_BLOB} actual={actual}")


def _project_for_v69(view: Any) -> Any:
    """Wrap a *real* view (one that already has v70 activated, i.e. not
    `bootbase`) so v69's own internals - which still expect to find v69's
    own entrypoint string in FW/AW - see the v69-shaped bytes they were
    written against. Mirrors v69's own `_project_for_v68` exactly, one
    layer up: a per-view `_ProjectionView` wrapper computed from that
    view's own real bytes, never a global monkeypatch. Only ever applied
    to a view that is genuinely not `bootbase`.
    """
    present = ps(view)
    replacements = {
        path: _v69_workflow_bytes(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES), path)
        for path in (FW, AW)
        if path in present
    }
    # v69 never re-exports `_ProjectionView` as its own attribute (unlike
    # v45..v68, which each do `_ProjectionView = q._ProjectionView`) - it
    # only reaches it via `v68._ProjectionView` directly, so v70 must do
    # the same one layer further down.
    return v69.v68._ProjectionView(view, replacements, frozenset())


def _v69_view(view: Any) -> Any:
    return view if bootbase(view) else _project_for_v69(view)


def _v69_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    return _v69_view(candidate), _v69_view(policy_base)


def _new_contract_presence(view: Any) -> frozenset[str]:
    paths = ps(view)
    return frozenset(path for path in CONTRACT_NEW_FILES if path in paths)


def _scan_prohibited_capabilities(path: str, data: bytes) -> None:
    for pattern in _PROHIBITED_CAPABILITY_PATTERNS:
        if pattern in data:
            base.fail(
                f"v70 S3 contract file uses a prohibited runtime capability: {path}: {pattern.decode()}"
            )


_UNSAFE_TOKEN = re.compile(rb"\bunsafe\b")


def _verify_contract_capabilities(view: Any) -> None:
    paths = ps(view)
    for path in sorted(SCANNED_CONTRACT_PATHS & paths):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        _scan_prohibited_capabilities(path, data)
        if _UNSAFE_TOKEN.search(data):
            base.fail(f"v70 S3 contract file uses a prohibited runtime capability: {path}: unsafe")
    if CONTRACT_EXPORT in paths and CONTRACT_MODULE in paths:
        lib = view.read_bytes(CONTRACT_EXPORT, base.MAX_POLICY_FILE_BYTES)
        if _FORBID_UNSAFE_MARKER not in lib:
            base.fail("v70 Contracts export must retain #![forbid(unsafe_code)]")


def patch_predecessor() -> None:
    current_wf = dict(v69.WF)
    if current_wf not in (V69_WF, dict(WF)):
        base.fail(f"v70 predecessor workflow identity map drifted: actual={current_wf}")
    _bind(v69, "WF", dict(WF), "v69 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v69(candidate)
            req_v69(policy_base)
            return
        if paths & BOOT:
            base.fail("v70 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v70 bootstrap base authorizes only exact capability-scan policy/workflow activation")

    if P in paths:
        base.fail("canonical v70 wrapper is frozen after activation")

    req_v69(candidate)
    req_v69(policy_base)

    _call("v69 exact-delta verifier", V69_DELTA, *_v69_views(candidate, policy_base))

    contract_changed = frozenset(paths & CONTRACT_FILES)
    if contract_changed or _new_contract_presence(candidate):
        _verify_contract_capabilities(candidate)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v69 base-control verifier", V69_BASE, *_v69_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v70 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v70 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v70 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v70 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        projected_candidate, projected_base = _v69_views(candidate, policy_base)
        _call("v69 extension verification", V69_EXT, projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    path_set = set(paths)
    remaining = path_set - {P, CONTRACT_MODULE, CONTRACT_TEST}
    if remaining:
        _call("v69 allowed-path verifier", V69_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v69(view)
    _call("v69 policy-file verification", V69_FILES, _v69_view(view))
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v70 wrapper mode invalid")
    _verify_contract_capabilities(view)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v70 predecessor component-base hook unavailable")
    _call(
        "v70 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _v69_view(view),
        paths,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v70 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v69_views(candidate, policy_base)
    _call("v70 predecessor S1 state freeze", _PREDECESSOR_FREEZE_S1, projected_candidate, projected_base)


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V69_PRINT:
        base.fail("v70 predecessor printer drifted")
    _call("v69 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v70=V69_PLUS_S3_CONTRACT_CAPABILITY_SCAN")
    print(f"v70_authority={AUTH}")
    print(f"s3_planning_authority_v70={S3_PLANNING_AUTHORITY}")
    print(f"s3_implementation_authority_v70={S3_IMPLEMENTATION_AUTHORITY}")
    print(f"contract_capability_scan_authority_v70={CONTRACT_CAPABILITY_SCAN_AUTHORITY}")
    print(f"filesystem_runtime_authority_v70={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"windows_api_authority_v70={WINDOWS_API_AUTHORITY}")
    print(f"job_object_authority_v70={JOB_OBJECT_AUTHORITY}")
    print(f"containment_actuation_authority_v70={CONTAINMENT_ACTUATION_AUTHORITY}")
    print(f"process_spawn_authority_v70={PROCESS_SPAWN_AUTHORITY}")
    print(f"credential_authority_v70={CREDENTIAL_AUTHORITY}")
    print(f"network_authority_v70={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v70={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v70={SOURCE_ADMISSION}")
    print(f"dependency_admission_v70={DEPENDENCY_ADMISSION}")
    print(f"s3_auth_host_authority_v70={S3_AUTH_HOST_AUTHORITY}")
    print(f"s3_auth_observe_authority_v70={S3_AUTH_OBSERVE_AUTHORITY}")
    print(f"s3_auth_spawn_authority_v70={S3_AUTH_SPAWN_AUTHORITY}")
    print(f"s4_plus_authority_v70={S4_PLUS_AUTHORITY}")


def overlay() -> None:
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
        (_attr(execution, "_verify_component_base", "component-base hook"), verify_component_base),
        (_attr(execution, "freeze_s1_007_state", "S1 state freeze hook"), freeze_s1_007_state),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v70 installed overlay drifted")
    if dict(v69.WF) != dict(WF):
        base.fail("v70 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(v69, name) != globals()[name]:
            base.fail(f"v70 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    global _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return
    # v69.install() may short-circuit to v69's own overlay() (if v69 was
    # already installed earlier, e.g. during its own predecessor selftest),
    # which checks its bare WF against v68.WF. That check must see v69's
    # own untouched WF, so patch_predecessor() (which rebinds v69.WF to
    # v70's values) must not run until after this call returns.
    _under_v69_workflow_projection(_call, "v69 install", getattr(v69, "install", None))
    patch_predecessor()
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V69_DELTA),
        (base.compare_base_controlled, V69_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V69_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V69_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V69_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V69_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V69_PRINT),
        (_attr(execution, "_verify_component_base", "predecessor component-base hook"), V69_COMPONENT_BASE),
        (_attr(execution, "freeze_s1_007_state", "predecessor S1 state freeze"), V69_FREEZE_STATE),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v70 predecessor hook drifted")
    _PRINT = V69_PRINT
    _PREDECESSOR_COMPONENT_BASE = V69_COMPONENT_BASE
    _PREDECESSOR_FREEZE_S1 = V69_FREEZE_STATE
    _EXPECTED_DESKTOP_EXTENSIONS = frozenset(set(extset(desktop)) | {P})
    _EXPECTED_EXECUTION_EXTENSIONS = frozenset(set(extset(execution)) | {P})
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_DESKTOP_EXTENSIONS, "desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_EXECUTION_EXTENSIONS, "execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "routing binding")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "desktop binding")
    _bind(execution, "verify_extension_controlled_paths", eext, "execution binding")
    _bind(shell, "validate_allowed_paths", allowed, "allowed binding")
    _bind(shell, "verify_policy_files", files, "files binding")
    _bind(shell, "print_success", printer, "printer binding")
    _bind(execution, "_verify_component_base", verify_component_base, "component-base binding")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "S1 state freeze binding")
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def selftest() -> None:
    # v69's own selftest verifies its FW/AW bytes against its own WF pins
    # (a self-check v68 does not have). Run it while v69.WF is still v69's
    # untouched canonical values - patch_predecessor() (called by install()
    # right below) must not rebind v69.WF until after this returns.
    _under_v69_workflow_projection(
        _call, "v69 predecessor self-test", getattr(v69, "selftest", None)
    )
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v70 workflow drifted: {path}")

    if (
        AUTH != "S3_AUTH_C_CONTRACTS_CAPABILITY_SCAN_SUCCESSOR"
        or S3_PLANNING_AUTHORITY != "CANONICAL_PRESERVED"
        or S3_IMPLEMENTATION_AUTHORITY != "EXACT_CONTRACTS_S3_C001_C013_ONLY"
        or CONTRACT_CAPABILITY_SCAN_AUTHORITY != "ENFORCED"
        or AUTHORIZED_TASKS != frozenset(f"S3-C{i:03d}" for i in range(1, 14))
        or "S3-C013" not in AUTHORIZED_TASKS
        or CONTRACT_TEST not in CONTRACT_FILES
        or FILESYSTEM_RUNTIME_AUTHORITY != "NONE"
        or WINDOWS_API_AUTHORITY != "NONE"
        or JOB_OBJECT_AUTHORITY != "NONE"
        or CONTAINMENT_ACTUATION_AUTHORITY != "NONE"
        or PROCESS_SPAWN_AUTHORITY != "NONE"
        or CREDENTIAL_AUTHORITY != "NONE"
        or NETWORK_AUTHORITY != "NONE"
        or MODEL_PROVIDER_EXECUTION != "NONE"
        or SOURCE_ADMISSION != "NONE"
        or S3_AUTH_HOST_AUTHORITY != "NOT_GRANTED"
        or S3_AUTH_OBSERVE_AUTHORITY != "NOT_GRANTED"
        or S3_AUTH_SPAWN_AUTHORITY != "NOT_GRANTED"
        or S4_PLUS_AUTHORITY != "NONE"
    ):
        base.fail("v70 authority boundary drifted")

    vb = root.read_bytes(V69, base.MAX_POLICY_FILE_BYTES)
    # V69_DELTA calls req_v68() unconditionally near its top (not only in
    # its non-contract "else" branch), so every fixture that reaches
    # V69_DELTA - i.e. every non-bootstrap `active`-derived fixture below -
    # must also carry v69's own frozen v68 predecessor, exactly as v69's
    # own selftest fixtures did for v68's req_v67-equivalent.
    vb68 = root.read_bytes(v69.V68, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V69: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v70", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed_bootstrap = dict(candidate)
    mixed_bootstrap["README.md"] = b"x"
    base.expect_failure_matching(
        "v70 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed_bootstrap),
        mem(policy_base),
    )

    active = {V69: vb, v69.V68: vb68, P: b"v70", CONTRACT_EXPORT: b"pub mod project;\n"}
    clean_module = (
        b"use serde::{Deserialize, Serialize};\n\n"
        b"#[derive(Debug, Clone, Serialize, Deserialize)]\n"
        b"pub struct ServerDescriptor;\n"
    )
    clean_export = b"#![forbid(unsafe_code)]\n\npub mod project;\npub mod s3;\npub use s3::*;\n"
    clean_test = b"#[test]\nfn s3_c013_secret_safety_contract_surface_exists() {}\n"

    first = dict(active)
    first.update(
        {
            CONTRACT_MODULE: clean_module,
            CONTRACT_EXPORT: clean_export,
            CONTRACT_TEST: clean_test,
        }
    )
    delta(mem(first), mem(active))

    for label, path, poison in (
        ("filesystem", CONTRACT_MODULE, b"\nfn read() { std::fs::read(\"x\").unwrap(); }\n"),
        ("network", CONTRACT_MODULE, b"\nfn conn() { std::net::TcpStream::connect(\"x\").unwrap(); }\n"),
        ("process", CONTRACT_TEST, b"\nfn run() { std::process::Command::new(\"x\").spawn().unwrap(); }\n"),
        ("environment", CONTRACT_TEST, b"\nfn env() { std::env::var(\"X\").unwrap(); }\n"),
        ("platform", CONTRACT_MODULE, b"\nfn raw() { unsafe { libc::getpid(); } }\n"),
        ("unsafe", CONTRACT_MODULE, b"\nunsafe fn raw() {}\n"),
    ):
        poisoned = dict(first)
        poisoned[path] = poisoned[path] + poison
        base.expect_failure_matching(
            f"v70 prohibited capability rejected: {label}",
            "prohibited runtime capability",
            delta,
            mem(poisoned),
            mem(active),
        )

    # The synthetic "active"/"first" fixtures above never carried
    # `#![forbid(unsafe_code)]` in their export content (real lib.rs does).
    # Exercise the dedicated retention guard directly: a view missing the
    # marker must fail even with an otherwise-clean module/test pair, and
    # adding the marker back must pass.
    no_forbid_active = {V69: vb, v69.V68: vb68, P: b"v70"}
    no_forbid_first = dict(no_forbid_active)
    no_forbid_first.update(
        {
            CONTRACT_MODULE: clean_module,
            CONTRACT_EXPORT: b"pub mod s3;\npub use s3::*;\n",
            CONTRACT_TEST: clean_test,
        }
    )
    base.expect_failure_matching(
        "v70 forbid(unsafe_code) retention required",
        "forbid(unsafe_code)",
        delta,
        mem(no_forbid_first),
        mem(no_forbid_active),
    )

    with_forbid_first = dict(no_forbid_first)
    with_forbid_first[CONTRACT_EXPORT] = b"#![forbid(unsafe_code)]\n\npub mod s3;\npub use s3::*;\n"
    delta(mem(with_forbid_first), mem(no_forbid_active))

    partial = dict(active)
    partial[CONTRACT_MODULE] = clean_module
    partial[CONTRACT_EXPORT] = b"pub mod s3;\n"
    base.expect_failure_matching(
        "v70 partial initial contracts",
        "exact C001..C013 contract/export/test set",
        delta,
        mem(partial),
        mem(active),
    )

    predecessor = dict(active)
    predecessor[V69] = b"drift"
    base.expect_failure_matching(
        "v70 predecessor wrapper frozen",
        "frozen v69 predecessor drifted",
        delta,
        mem(predecessor),
        mem(active),
    )

    repair_base = dict(first)
    repair = dict(repair_base)
    repair[CONTRACT_MODULE] = clean_module + b"pub struct HostDescriptor;\n"
    delta(mem(repair), mem(repair_base))

    deletion = dict(repair_base)
    del deletion[CONTRACT_TEST]
    base.expect_failure_matching(
        "v70 contract test deletion",
        "may not be deleted",
        delta,
        mem(deletion),
        mem(repair_base),
    )

    print("wepld v70 S3 contract capability-scan successor self-tests: PASS")


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0
        install()
        if argv and argv[0] == "verify-candidate-local":
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("--root", required=True)
            parser.add_argument("--policy-base-root", required=True)
            parser.add_argument("--policy-base-sha", required=True)
            args = parser.parse_args(argv[1:])
            return int(
                _call(
                    "candidate-local verifier",
                    CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
