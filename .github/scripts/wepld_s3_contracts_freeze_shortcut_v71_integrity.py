#!/usr/bin/env python3
"""Exempt pure S3-contracts deltas from the inherited frozen-S1-protocol check.

v71 is an append-only successor to canonical v70. It preserves every
inherited S1/S2/S3-AUTH-C boundary unchanged - it grants no new authority -
and fixes exactly one interaction gap: `freeze_s1_007_state` (protecting a
fixed set of "frozen S1 protocol" paths from drifting) delegates
unconditionally down through the whole predecessor chain, including to
v23's `freeze_s1_006_protocol`, whose own `CONTRACT_FILES` is frozen to
its own three files from years before S3 existed. A delta touching only
`crates/contracts/src/s3.rs`, `crates/contracts/src/lib.rs`, and
`crates/contracts/tests/s3_contracts_v1.rs` - exactly the set `delta()`
(the routing hook) already validates and admits on its own - reaches v23
carrying paths v23 has never heard of, and v23 fails it as a "mixed
contract/non-contract delta", even though nothing outside the S3 contracts
scope was touched.

This was not previously reachable: neither v69 (PR #337) nor v70 (PR #338)
ever included an actual `crates/contracts/**` change, so this interaction
was never exercised by real candidate verification before this successor.
It surfaced when the first genuine S3 contracts tranche was locally
verified via `verify-candidate-local` against trusted `main` ahead of
opening that PR.

The bootstrap transition is exactly:
- this v71 policy file;
- foundation-integrity.yml;
- s1-admission-integrity.yml.

No Cargo manifest/lock mutation, `crates/core` runtime behavior, Windows
API binding, process spawn, network, model/provider execution, source
admission, dependency admission, or any S3-AUTH-HOST/OBSERVE/SPAWN
authority is granted by this successor - identical to v69/v70.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s3_contracts_freeze_shortcut_v71_integrity.py"
V70 = ".github/scripts/wepld_s3_auth_c_contracts_capability_scan_v70_integrity.py"
V70_BLOB = "177617d9ddc759c2c9d8b278859b91062266c362"
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

OLD_WF = {
    FW: "be7d361bbd5390c3dd5a080d8dfba3c72090a5fbd1269e2ea73f52fc803394e2",
    AW: "577d181f8d6f9af0df2abb41ac417ff8e961f3c1a791c0032e4e521930a70958",
}
WF = {
    FW: "a497820d4c4e84d1bc319d5bc8bbd74c905768e157ac078904194e308f9c880f",
    AW: "ae89f87f492b01be07df0b642c880a26d85d222a67140e1bcac7360789e6ca9d",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S3_CONTRACTS_FREEZE_SHORTCUT_SUCCESSOR"
S3_PLANNING_AUTHORITY = "CANONICAL_PRESERVED"
S3_IMPLEMENTATION_AUTHORITY = "EXACT_CONTRACTS_S3_C001_C013_ONLY"
CONTRACT_CAPABILITY_SCAN_AUTHORITY = "ENFORCED"
S1_007_FREEZE_EXEMPTION_AUTHORITY = "S3_CONTRACT_FILES_ONLY"
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


if _git_blob(root.read_bytes(V70, base.MAX_POLICY_FILE_BYTES)) != V70_BLOB:
    base.fail("frozen v70 predecessor drifted")

_V71_ENTRYPOINT = b"wepld_s3_contracts_freeze_shortcut_v71_integrity.py"
_V70_ENTRYPOINT = b"wepld_s3_auth_c_contracts_capability_scan_v70_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}


def _v70_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V71_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v71 workflow entrypoint count drifted before v70 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V71_ENTRYPOINT, _V70_ENTRYPOINT)


_TRUE_ORIGINAL_LOCAL_READ_BYTES = base.LocalRepositoryView.read_bytes


def _v70_projected_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
    data = _TRUE_ORIGINAL_LOCAL_READ_BYTES(local_view, relative, limit)
    if relative in (FW, AW):
        data = _v70_workflow_bytes(data, relative)
        if len(data) > limit:
            base.fail(f"v71 v70-projection exceeds read bound: {relative}")
    return data


def _under_v70_workflow_projection(fn: Any, *args: Any, **kwargs: Any) -> Any:
    """Run `fn` while `.github/workflows/{foundation-integrity,s1-admission-integrity}.yml`
    read as their exact canonical v70 (pre-v71-activation) bytes.

    Mirrors v70's own `_under_v69_workflow_projection` exactly, one layer
    up.
    """
    saved_read_bytes = base.LocalRepositoryView.read_bytes
    base.LocalRepositoryView.read_bytes = _v70_projected_read_bytes
    try:
        return fn(*args, **kwargs)
    finally:
        base.LocalRepositoryView.read_bytes = saved_read_bytes


v70 = _under_v70_workflow_projection(
    importlib.import_module, "wepld_s3_auth_c_contracts_capability_scan_v70_integrity"
)

V25 = v70.V25
_attr = v70._attr
_bind = v70._bind
_call = v70._call

V70_DELTA = v70.delta
V70_BASE = v70.basectrl
V70_ALLOWED = v70.allowed
V70_FILES = v70.files
V70_DEXT = v70.dext
V70_EEXT = v70.eext
V70_EXT = v70.ext
V70_PRINT = v70.printer
V70_COMPONENT_BASE = v70.verify_component_base
V70_FREEZE_STATE = v70.freeze_s1_007_state
V70_WF = dict(v70.WF)
CAND = V25.CAND
RUNTIME = V25.RUNTIME

if V70_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v70 workflow identities drifted before v71 import: actual={V70_WF}")
if _attr(v70, "AUTH", "v70 authority marker") != "S3_AUTH_C_CONTRACTS_CAPABILITY_SCAN_SUCCESSOR":
    base.fail("v71 observed v70 authority drift")
if _attr(v70, "FILESYSTEM_RUNTIME_AUTHORITY", "v70 filesystem authority") != "NONE":
    base.fail("v71 observed v70 filesystem-authority drift")

_INHERITED_AUTHORITY_NAMES = v70._INHERITED_AUTHORITY_NAMES
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(v70, _name)


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
        base.fail("v71 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v71 extension topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def req_v70(view: Any) -> None:
    if V70 not in ps(view):
        base.fail("v71 candidate/base is missing frozen v70 predecessor")
    actual = blob(view.read_bytes(V70, base.MAX_POLICY_FILE_BYTES))
    if actual != V70_BLOB:
        base.fail(f"frozen v70 predecessor drifted: expected={V70_BLOB} actual={actual}")


def _project_for_v70(view: Any) -> Any:
    """Wrap a *real* view (one that already has v71 activated, i.e. not
    `bootbase`) so v70's own internals - which still expect to find v70's
    own entrypoint string in FW/AW - see the v70-shaped bytes they were
    written against. Mirrors v70's own `_project_for_v69` exactly, one
    layer up, including tolerating a view that doesn't carry FW/AW at all
    (e.g. a minimal contracts-only fixture).
    """
    present = ps(view)
    replacements = {
        path: _v70_workflow_bytes(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES), path)
        for path in (FW, AW)
        if path in present
    }
    # Neither v69 nor v70 re-exports `_ProjectionView` as its own
    # attribute - it is only ever reached via the predecessor chain
    # (v68._ProjectionView), so v71 must reach three layers down.
    return v70.v69.v68._ProjectionView(view, replacements, frozenset())


def _v70_view(view: Any) -> Any:
    return view if bootbase(view) else _project_for_v70(view)


def _v70_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    return _v70_view(candidate), _v70_view(policy_base)


def _new_contract_presence(view: Any) -> frozenset[str]:
    paths = ps(view)
    return frozenset(path for path in CONTRACT_NEW_FILES if path in paths)


def patch_predecessor() -> None:
    current_wf = dict(v70.WF)
    if current_wf not in (V70_WF, dict(WF)):
        base.fail(f"v71 predecessor workflow identity map drifted: actual={current_wf}")
    _bind(v70, "WF", dict(WF), "v70 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v70(candidate)
            req_v70(policy_base)
            return
        if paths & BOOT:
            base.fail("v71 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v71 bootstrap base authorizes only exact freeze-shortcut policy/workflow activation")

    if P in paths:
        base.fail("canonical v71 wrapper is frozen after activation")

    req_v70(candidate)
    req_v70(policy_base)

    _call("v70 exact-delta verifier", V70_DELTA, *_v70_views(candidate, policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v70 base-control verifier", V70_BASE, *_v70_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v71 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v71 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v71 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v71 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        projected_candidate, projected_base = _v70_views(candidate, policy_base)
        _call("v70 extension verification", V70_EXT, projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - {P}
    if remaining:
        _call("v70 allowed-path verifier", V70_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v70(view)
    _call("v70 policy-file verification", V70_FILES, _v70_view(view))
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v71 wrapper mode invalid")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v71 predecessor component-base hook unavailable")
    _call(
        "v71 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _v70_view(view),
        paths,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    """Exempt a delta touching *only* S3 contract files from the inherited
    frozen-S1-protocol delegation.

    `delta()` (the routing hook, called independently in the same
    admission pass) already fully validates an S3-contracts-only delta -
    exact file set, no Cargo/core/workflow mutation, capability scan,
    forbid(unsafe_code) retention. This hook's own concern (a fixed set of
    "frozen S1 protocol" paths must not drift) is orthogonal to and
    unaffected by S3 contract files, which the older predecessor chain
    (v23 and earlier) has no concept of at all - delegating to it for a
    delta that touches nothing outside CONTRACT_FILES would only ever
    produce a false "mixed contract/non-contract delta" rejection, never
    a real frozen-protocol violation.
    """
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v71 predecessor S1 freeze hook unavailable")
    paths = changed(candidate, policy_base)
    if paths and paths <= CONTRACT_FILES:
        return
    projected_candidate, projected_base = _v70_views(candidate, policy_base)
    _call("v71 predecessor S1 state freeze", _PREDECESSOR_FREEZE_S1, projected_candidate, projected_base)


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V70_PRINT:
        base.fail("v71 predecessor printer drifted")
    _call("v70 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v71=V70_PLUS_S1_007_FREEZE_S3_CONTRACT_EXEMPTION")
    print(f"v71_authority={AUTH}")
    print(f"s3_planning_authority_v71={S3_PLANNING_AUTHORITY}")
    print(f"s3_implementation_authority_v71={S3_IMPLEMENTATION_AUTHORITY}")
    print(f"contract_capability_scan_authority_v71={CONTRACT_CAPABILITY_SCAN_AUTHORITY}")
    print(f"s1_007_freeze_exemption_authority_v71={S1_007_FREEZE_EXEMPTION_AUTHORITY}")
    print(f"filesystem_runtime_authority_v71={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"windows_api_authority_v71={WINDOWS_API_AUTHORITY}")
    print(f"job_object_authority_v71={JOB_OBJECT_AUTHORITY}")
    print(f"containment_actuation_authority_v71={CONTAINMENT_ACTUATION_AUTHORITY}")
    print(f"process_spawn_authority_v71={PROCESS_SPAWN_AUTHORITY}")
    print(f"credential_authority_v71={CREDENTIAL_AUTHORITY}")
    print(f"network_authority_v71={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v71={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v71={SOURCE_ADMISSION}")
    print(f"dependency_admission_v71={DEPENDENCY_ADMISSION}")
    print(f"s3_auth_host_authority_v71={S3_AUTH_HOST_AUTHORITY}")
    print(f"s3_auth_observe_authority_v71={S3_AUTH_OBSERVE_AUTHORITY}")
    print(f"s3_auth_spawn_authority_v71={S3_AUTH_SPAWN_AUTHORITY}")
    print(f"s4_plus_authority_v71={S4_PLUS_AUTHORITY}")


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
        base.fail("v71 installed overlay drifted")
    if dict(v70.WF) != dict(WF):
        base.fail("v71 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(v70, name) != globals()[name]:
            base.fail(f"v71 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    global _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return
    # v70.install() may short-circuit to v70's own overlay() (if v70 was
    # already installed earlier, e.g. during its own predecessor selftest),
    # which checks its bare WF against v69.WF. That check must see v70's
    # own untouched WF, so patch_predecessor() (which rebinds v70.WF to
    # v71's values) must not run until after this call returns.
    _under_v70_workflow_projection(_call, "v70 install", getattr(v70, "install", None))
    patch_predecessor()
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V70_DELTA),
        (base.compare_base_controlled, V70_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V70_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V70_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V70_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V70_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V70_PRINT),
        (_attr(execution, "_verify_component_base", "predecessor component-base hook"), V70_COMPONENT_BASE),
        (_attr(execution, "freeze_s1_007_state", "predecessor S1 state freeze"), V70_FREEZE_STATE),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v71 predecessor hook drifted")
    _PRINT = V70_PRINT
    _PREDECESSOR_COMPONENT_BASE = V70_COMPONENT_BASE
    _PREDECESSOR_FREEZE_S1 = V70_FREEZE_STATE
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
    # v70's own selftest verifies its FW/AW bytes against its own WF pins.
    # Run it while v70.WF is still v70's untouched canonical values -
    # patch_predecessor() (called by install() right below) must not
    # rebind v70.WF until after this returns.
    _under_v70_workflow_projection(
        _call, "v70 predecessor self-test", getattr(v70, "selftest", None)
    )
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v71 workflow drifted: {path}")

    if (
        AUTH != "S3_CONTRACTS_FREEZE_SHORTCUT_SUCCESSOR"
        or S3_PLANNING_AUTHORITY != "CANONICAL_PRESERVED"
        or S3_IMPLEMENTATION_AUTHORITY != "EXACT_CONTRACTS_S3_C001_C013_ONLY"
        or CONTRACT_CAPABILITY_SCAN_AUTHORITY != "ENFORCED"
        or S1_007_FREEZE_EXEMPTION_AUTHORITY != "S3_CONTRACT_FILES_ONLY"
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
        base.fail("v71 authority boundary drifted")

    vb = root.read_bytes(V70, base.MAX_POLICY_FILE_BYTES)
    vb69 = root.read_bytes(v70.V69, base.MAX_POLICY_FILE_BYTES)
    vb68 = root.read_bytes(v70.v69.V68, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V70: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v71", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed_bootstrap = dict(candidate)
    mixed_bootstrap["README.md"] = b"x"
    base.expect_failure_matching(
        "v71 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed_bootstrap),
        mem(policy_base),
    )

    active = {V70: vb, v70.V69: vb69, v70.v69.V68: vb68, P: b"v71", CONTRACT_EXPORT: b"pub mod project;\n"}
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

    # This is the exact scenario v71 exists to fix: an s3-contracts-only
    # delta must not be rejected by the inherited frozen-S1-protocol check
    # as a "mixed contract/non-contract delta" (v23's CONTRACT_FILES has
    # no concept of S3 contract paths at all).
    freeze_s1_007_state(mem(first), mem(active))

    # A delta mixing an S3 contract file with an unrelated non-contract
    # change must still delegate to (and can still be caught by) the
    # inherited frozen-S1-protocol check, not silently exempted.
    mixed_with_non_contract = dict(active)
    mixed_with_non_contract.update(
        {
            CONTRACT_MODULE: clean_module,
            CONTRACT_EXPORT: clean_export,
            CONTRACT_TEST: clean_test,
            "README.md": b"changed",
        }
    )
    base.expect_failure_matching(
        "v71 freeze exemption does not cover mixed non-contract changes",
        "must not mix",
        delta,
        mem(mixed_with_non_contract),
        mem(active),
    )

    partial = dict(active)
    partial[CONTRACT_MODULE] = clean_module
    partial[CONTRACT_EXPORT] = b"pub mod s3;\n"
    base.expect_failure_matching(
        "v71 partial initial contracts",
        "exact C001..C013 contract/export/test set",
        delta,
        mem(partial),
        mem(active),
    )

    predecessor = dict(active)
    predecessor[V70] = b"drift"
    base.expect_failure_matching(
        "v71 predecessor wrapper frozen",
        "frozen v70 predecessor drifted",
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
        "v71 contract test deletion",
        "may not be deleted",
        delta,
        mem(deletion),
        mem(repair_base),
    )

    poisoned = dict(first)
    poisoned[CONTRACT_MODULE] = poisoned[CONTRACT_MODULE] + b"\nfn read() { std::fs::read(\"x\").unwrap(); }\n"
    base.expect_failure_matching(
        "v71 prohibited capability still rejected",
        "prohibited runtime capability",
        delta,
        mem(poisoned),
        mem(active),
    )

    print("wepld v71 S1-007 freeze S3-contract exemption successor self-tests: PASS")


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
