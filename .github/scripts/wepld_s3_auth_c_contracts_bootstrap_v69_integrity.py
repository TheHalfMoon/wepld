#!/usr/bin/env python3
"""Grant the minimum S3-AUTH-C contracts-only implementation authority.

v69 is an append-only successor to canonical v68. It preserves every
inherited S1/S2 boundary unchanged and authorizes exactly three
`crates/contracts` paths for the first S3 contract tranche
(`specs/007-s3-terminal-fabric-trusted-process-ownership/tasks.md` S3-C001..
S3-C013):

- crates/contracts/src/s3.rs
- crates/contracts/src/lib.rs
- crates/contracts/tests/s3_contracts_v1.rs

The bootstrap transition is exactly:
- this v69 policy file;
- foundation-integrity.yml;
- s1-admission-integrity.yml.

No Cargo manifest/lock mutation, `crates/core` runtime behavior, Windows API
binding, process spawn, network, model/provider execution, source admission,
dependency admission, or any S3-AUTH-HOST/OBSERVE/SPAWN authority is granted
by this successor. It grants contract *shape* only, per
`specs/007-s3-terminal-fabric-trusted-process-ownership/plan.md` SS10.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s3_auth_c_contracts_bootstrap_v69_integrity.py"
V68 = ".github/scripts/wepld_s2_a009_files_hook_repair_v68_integrity.py"
V68_BLOB = "d05c95aa30d527e8b2564aea318c23b6ff8288e9"
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

AUTHORIZED_TASKS = frozenset(f"S3-C{i:03d}" for i in range(1, 14))

OLD_WF = {
    FW: "8927b51324b386353e4b10062aff6f066b211bccbb5a5f0d3f9494915e8ea9c3",
    AW: "3e5a5a3a3de437c138847227825f21fb6d164bddf3fc73274ea6460c8fa1781c",
}
WF = {
    FW: "f2a5a8f85b0bce3b7cc1398aa0f32d67eb3c1f8f14ea8cecec932687743ee206",
    AW: "80250413652ae9bf89ac39e8e363a9684b56336f234b5ed00a5b92121524a949",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S3_AUTH_C_CONTRACTS_ONLY_SUCCESSOR"
S3_PLANNING_AUTHORITY = "CANONICAL_PRESERVED"
S3_IMPLEMENTATION_AUTHORITY = "EXACT_CONTRACTS_S3_C001_C013_ONLY"
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


if _git_blob(root.read_bytes(V68, base.MAX_POLICY_FILE_BYTES)) != V68_BLOB:
    base.fail("frozen v68 predecessor drifted")

_V69_ENTRYPOINT = b"wepld_s3_auth_c_contracts_bootstrap_v69_integrity.py"
_V68_ENTRYPOINT = b"wepld_s2_a009_files_hook_repair_v68_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}


def _v68_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V69_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v69 workflow entrypoint count drifted before v68 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V69_ENTRYPOINT, _V68_ENTRYPOINT)


_TRUE_ORIGINAL_LOCAL_READ_BYTES = base.LocalRepositoryView.read_bytes


def _v68_projected_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
    data = _TRUE_ORIGINAL_LOCAL_READ_BYTES(local_view, relative, limit)
    if relative in (FW, AW):
        data = _v68_workflow_bytes(data, relative)
        if len(data) > limit:
            base.fail(f"v69 v68-projection exceeds read bound: {relative}")
    return data


def _under_v68_workflow_projection(fn: Any, *args: Any, **kwargs: Any) -> Any:
    """Run `fn` while `.github/workflows/{foundation-integrity,s1-admission-integrity}.yml`
    read as their exact canonical v68 (pre-v69-activation) bytes.

    v68's own module-level code and its `run_predecessor_selftests()` both
    re-derive a v68->v67 workflow projection from the *live* working tree at
    the moment they run, not only at v69's own import time. Once v69 is
    active, the real files read back as v69's entrypoint, not v68's, so both
    of those call sites need this same v69->v68 reversal applied around
    them - exactly mirroring how v68 itself reversed to v67. Both call sites
    share the exact same `_v68_projected_read_bytes` function object (rather
    than each installing its own fresh closure) because v68's own `overlay()`
    identity-checks `base.LocalRepositoryView.read_bytes` against the value
    it captured at its own import time - which, imported under this wrapper,
    is this singleton.
    """
    saved_read_bytes = base.LocalRepositoryView.read_bytes
    base.LocalRepositoryView.read_bytes = _v68_projected_read_bytes
    try:
        return fn(*args, **kwargs)
    finally:
        base.LocalRepositoryView.read_bytes = saved_read_bytes


v68 = _under_v68_workflow_projection(
    importlib.import_module, "wepld_s2_a009_files_hook_repair_v68_integrity"
)

V25 = v68.V25
_attr = v68._attr
_bind = v68._bind
_call = v68._call

V68_DELTA = v68.delta
V68_BASE = v68.basectrl
V68_ALLOWED = v68.allowed
V68_FILES = v68.files
V68_DEXT = v68.dext
V68_EEXT = v68.eext
V68_EXT = v68.ext
V68_PRINT = v68.printer
V68_COMPONENT_BASE = v68.verify_component_base
V68_FREEZE_STATE = v68.freeze_s1_007_state
V68_WF = dict(v68.WF)
CAND = V25.CAND
RUNTIME = V25.RUNTIME

if V68_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v68 workflow identities drifted before v69 import: actual={V68_WF}")
if _attr(v68, "AUTH", "v68 authority marker") != "S2_A009_FILES_HOOK_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE":
    base.fail("v69 observed v68 authority drift")
if _attr(v68, "SOURCE_ADMISSION", "v68 source boundary") != "NONE":
    base.fail("v69 observed v68 source-admission drift")

_INHERITED_AUTHORITY_NAMES = v68._INHERITED_AUTHORITY_NAMES
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(v68, _name)


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
        base.fail("v69 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v69 extension topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def req_v68(view: Any) -> None:
    if V68 not in ps(view):
        base.fail("v69 candidate/base is missing frozen v68 predecessor")
    actual = blob(view.read_bytes(V68, base.MAX_POLICY_FILE_BYTES))
    if actual != V68_BLOB:
        base.fail(f"frozen v68 predecessor drifted: expected={V68_BLOB} actual={actual}")


def _project_for_v68(view: Any) -> Any:
    """Wrap a *real* view (one that already has v69 activated, i.e. not
    `bootbase`) so v68's own internals - which still expect to find v68's own
    entrypoint string in FW/AW, exactly as `_project_for_v67` expects to find
    v68's - see the v68-shaped bytes they were written against.

    This mirrors v68's own `_v67_views`/`_project_for_v67` exactly, just one
    layer up: a per-view `_ProjectionView` wrapper computed from that view's
    own real bytes, never a global monkeypatch. It must only ever be applied
    to a view that is genuinely not `bootbase` - a `bootbase` view (e.g. the
    real canonical `main` during this very activation) is already v68-shaped
    natively and must pass through unprojected.
    """
    replacements = {
        path: _v68_workflow_bytes(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES), path)
        for path in (FW, AW)
    }
    return v68._ProjectionView(view, replacements, frozenset())


def _v68_view(view: Any) -> Any:
    return view if bootbase(view) else _project_for_v68(view)


def _v68_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    return _v68_view(candidate), _v68_view(policy_base)


def _new_contract_presence(view: Any) -> frozenset[str]:
    paths = ps(view)
    return frozenset(path for path in CONTRACT_NEW_FILES if path in paths)


def _verify_contract_files(view: Any) -> None:
    paths = ps(view)
    for path in sorted(CONTRACT_FILES & paths):
        if mode(view, path) != "100644":
            base.fail(f"v69 S3 contract file mode invalid: {path}")
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if not data:
            base.fail(f"v69 S3 contract file must be non-empty: {path}")
        if b"\x00" in data:
            base.fail(f"v69 S3 contract file contains NUL bytes: {path}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            base.fail(f"v69 S3 contract file is not UTF-8: {path}")
    if CONTRACT_NEW_FILES <= paths:
        lib = view.read_bytes(CONTRACT_EXPORT, base.MAX_POLICY_FILE_BYTES)
        if lib.count(b"pub mod s3;") != 1:
            base.fail("v69 Contracts export must register the s3 module exactly once")


def patch_predecessor() -> None:
    current_wf = dict(v68.WF)
    if current_wf not in (V68_WF, dict(WF)):
        base.fail(f"v69 predecessor workflow identity map drifted: actual={current_wf}")
    _bind(v68, "WF", dict(WF), "v68 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v68(candidate)
            req_v68(policy_base)
            return
        if paths & BOOT:
            base.fail("v69 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v69 bootstrap base authorizes only exact S3-AUTH-C policy/workflow activation")

    if P in paths:
        base.fail("canonical v69 wrapper is frozen after activation")

    req_v68(candidate)
    req_v68(policy_base)

    contract_changed = frozenset(paths & CONTRACT_FILES)
    base_contract_presence = _new_contract_presence(policy_base)
    s3_contract_delta = bool(paths & CONTRACT_NEW_FILES) or (
        base_contract_presence == CONTRACT_NEW_FILES and bool(contract_changed)
    )
    if s3_contract_delta:
        if CARGO_MANIFEST in paths or ROOT_CARGO_LOCK in paths:
            base.fail("v69 S3 contracts authority does not permit Cargo manifest or Cargo.lock mutation")
        unknown_contracts = {
            path for path in paths if path.startswith(CONTRACT_PREFIX) and path not in CONTRACT_FILES
        }
        if unknown_contracts:
            base.fail(f"v69 S3 contracts delta contains unauthorized contracts paths: {sorted(unknown_contracts)}")
        if any(path.startswith("crates/core/") for path in paths):
            base.fail("v69 S3 contracts authority does not permit Core/runtime mutation")
        if FW in paths or AW in paths or CW in paths:
            base.fail("v69 S3 contracts authority does not permit workflow mutation")
        if paths != contract_changed:
            base.fail("v69 S3 contracts delta must not mix with any non-contract change")

        candidate_presence = _new_contract_presence(candidate)
        if not base_contract_presence:
            if contract_changed != CONTRACT_FILES or candidate_presence != CONTRACT_NEW_FILES:
                base.fail("v69 initial S3 contracts delta must change the exact C001..C013 contract/export/test set")
        elif base_contract_presence == CONTRACT_NEW_FILES:
            if candidate_presence != CONTRACT_NEW_FILES:
                base.fail("v69 canonical S3 contract module/test may not be deleted")
        else:
            base.fail("v69 predecessor contains a partial S3 contract tranche")

        if CONTRACT_EXPORT not in ps(candidate):
            base.fail("v69 S3 contract export file is missing")
        _verify_contract_files(candidate)
        return

    _call("v68 exact-delta verifier", V68_DELTA, *_v68_views(candidate, policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v68 base-control verifier", V68_BASE, *_v68_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v69 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v69 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v69 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v69 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        projected_candidate, projected_base = _v68_views(candidate, policy_base)
        _call("v68 extension verification", V68_EXT, projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    path_set = set(paths)
    remaining = path_set - {P, CONTRACT_MODULE, CONTRACT_TEST}
    if remaining:
        _call("v68 allowed-path verifier", V68_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v68(view)
    _call("v68 policy-file verification", V68_FILES, _v68_view(view))
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v69 wrapper mode invalid")
    _verify_contract_files(view)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v69 predecessor component-base hook unavailable")
    _call(
        "v69 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _v68_view(view),
        paths,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v69 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v68_views(candidate, policy_base)
    _call("v69 predecessor S1 state freeze", _PREDECESSOR_FREEZE_S1, projected_candidate, projected_base)


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V68_PRINT:
        base.fail("v69 predecessor printer drifted")
    _call("v68 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v69=V68_PLUS_S3_AUTH_C_CONTRACTS_C001_C013_ONLY")
    print(f"v69_authority={AUTH}")
    print(f"s3_planning_authority_v69={S3_PLANNING_AUTHORITY}")
    print(f"s3_implementation_authority_v69={S3_IMPLEMENTATION_AUTHORITY}")
    print(f"filesystem_runtime_authority_v69={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"windows_api_authority_v69={WINDOWS_API_AUTHORITY}")
    print(f"job_object_authority_v69={JOB_OBJECT_AUTHORITY}")
    print(f"containment_actuation_authority_v69={CONTAINMENT_ACTUATION_AUTHORITY}")
    print(f"process_spawn_authority_v69={PROCESS_SPAWN_AUTHORITY}")
    print(f"credential_authority_v69={CREDENTIAL_AUTHORITY}")
    print(f"network_authority_v69={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v69={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v69={SOURCE_ADMISSION}")
    print(f"dependency_admission_v69={DEPENDENCY_ADMISSION}")
    print(f"s3_auth_host_authority_v69={S3_AUTH_HOST_AUTHORITY}")
    print(f"s3_auth_observe_authority_v69={S3_AUTH_OBSERVE_AUTHORITY}")
    print(f"s3_auth_spawn_authority_v69={S3_AUTH_SPAWN_AUTHORITY}")
    print(f"s4_plus_authority_v69={S4_PLUS_AUTHORITY}")


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
        base.fail("v69 installed overlay drifted")
    if dict(v68.WF) != dict(WF):
        base.fail("v69 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(v68, name) != globals()[name]:
            base.fail(f"v69 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    global _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return
    patch_predecessor()
    _under_v68_workflow_projection(_call, "v68 install", getattr(v68, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V68_DELTA),
        (base.compare_base_controlled, V68_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V68_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V68_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V68_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V68_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V68_PRINT),
        (_attr(execution, "_verify_component_base", "predecessor component-base hook"), V68_COMPONENT_BASE),
        (_attr(execution, "freeze_s1_007_state", "predecessor S1 state freeze"), V68_FREEZE_STATE),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v69 predecessor hook drifted")
    _PRINT = V68_PRINT
    _PREDECESSOR_COMPONENT_BASE = V68_COMPONENT_BASE
    _PREDECESSOR_FREEZE_S1 = V68_FREEZE_STATE
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
    patch_predecessor()
    _under_v68_workflow_projection(
        _call, "v68 predecessor self-test", getattr(v68, "selftest", None)
    )
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v69 workflow drifted: {path}")

    if (
        AUTH != "S3_AUTH_C_CONTRACTS_ONLY_SUCCESSOR"
        or S3_PLANNING_AUTHORITY != "CANONICAL_PRESERVED"
        or S3_IMPLEMENTATION_AUTHORITY != "EXACT_CONTRACTS_S3_C001_C013_ONLY"
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
        base.fail("v69 authority boundary drifted")

    vb = root.read_bytes(V68, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V68: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v69", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed_bootstrap = dict(candidate)
    mixed_bootstrap["README.md"] = b"x"
    base.expect_failure_matching(
        "v69 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed_bootstrap),
        mem(policy_base),
    )

    active = {V68: vb, P: b"v69", CONTRACT_EXPORT: b"pub mod project;\n"}
    first = dict(active)
    first.update(
        {
            CONTRACT_MODULE: b"pub struct ServerDescriptor;\n",
            CONTRACT_EXPORT: b"pub mod project;\npub mod s3;\npub use s3::*;\n",
            CONTRACT_TEST: b"#[test]\nfn s3_c013_secret_safety_contract_surface_exists() {}\n",
        }
    )
    delta(mem(first), mem(active))

    partial = dict(active)
    partial[CONTRACT_MODULE] = b"pub struct ServerDescriptor;\n"
    partial[CONTRACT_EXPORT] = b"pub mod s3;\n"
    base.expect_failure_matching(
        "v69 partial initial contracts",
        "exact C001..C013 contract/export/test set",
        delta,
        mem(partial),
        mem(active),
    )

    unknown = dict(first)
    unknown["crates/contracts/src/unknown_s3.rs"] = b"pub struct Unknown;\n"
    base.expect_failure_matching(
        "v69 unknown contracts path",
        "unauthorized contracts paths",
        delta,
        mem(unknown),
        mem(active),
    )

    mixed = dict(first)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v69 mixed contracts delta",
        "must not mix",
        delta,
        mem(mixed),
        mem(active),
    )

    manifest = dict(first)
    manifest[CARGO_MANIFEST] = b"[package]\nname='changed'\n"
    base.expect_failure_matching(
        "v69 Cargo manifest mutation",
        "Cargo manifest or Cargo.lock",
        delta,
        mem(manifest),
        mem(active),
    )

    lock = dict(first)
    lock[ROOT_CARGO_LOCK] = b"changed"
    base.expect_failure_matching(
        "v69 Cargo.lock mutation",
        "Cargo manifest or Cargo.lock",
        delta,
        mem(lock),
        mem(active),
    )

    core = dict(first)
    core["crates/core/src/s3.rs"] = b"pub fn runtime() {}\n"
    base.expect_failure_matching(
        "v69 Core/runtime mutation",
        "Core/runtime mutation",
        delta,
        mem(core),
        mem(active),
    )

    workflow = dict(first)
    workflow[CW] = b"changed"
    base.expect_failure_matching(
        "v69 workflow mutation",
        "workflow mutation",
        delta,
        mem(workflow),
        mem(active),
    )

    predecessor = dict(active)
    predecessor[V68] = b"drift"
    base.expect_failure_matching(
        "v69 predecessor wrapper frozen",
        "frozen v68 predecessor drifted",
        delta,
        mem(predecessor),
        mem(active),
    )

    repair_base = dict(first)
    repair = dict(repair_base)
    repair[CONTRACT_MODULE] = b"pub struct ServerDescriptor;\npub struct HostDescriptor;\n"
    delta(mem(repair), mem(repair_base))

    deletion = dict(repair_base)
    del deletion[CONTRACT_TEST]
    base.expect_failure_matching(
        "v69 contract test deletion",
        "may not be deleted",
        delta,
        mem(deletion),
        mem(repair_base),
    )

    print("wepld v69 S3-AUTH-C contracts-only successor self-tests: PASS")


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
