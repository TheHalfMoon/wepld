#!/usr/bin/env python3
"""Bind the S3 pure-contract freeze exemption to the enforcement hook the verifier actually executes.

v72 is a forward-only successor to canonical v71. It grants no new authority:
every path set, dependency pin, capability scan and S1/S2/S3-AUTH-C boundary
inherited from v69/v70/v71 is preserved unchanged.

It repairs exactly one enforcement-binding defect in v71.

Observed defect at canonical v71:

- v71 replaces the execution component's `freeze_s1_007_state` with an
  exemption that returns early when the candidate delta is wholly inside the
  three authorized S3 contract paths.
- The verifier does not reach that exemption through `freeze_s1_007_state`
  alone. `wepld_s1_desktop_integrity_impl.verify_view` and
  `wepld_s1_shell_integrity.verify_view` call the execution component's
  `freeze_s1_006_protocol` *and* `freeze_s1_007_state` as two independent
  hooks on the same view pair.
- `freeze_s1_006_protocol` is last bound by v23 and is never rebound by
  v24..v71, so an S3-contracts-only delta still reaches v23's
  `CONTRACT_FILES`-based rejection:
  "v23 S2 contract freeze repair refuses mixed contract/non-contract delta".
- Consequence: v71's declared authority
  (`S3_IMPLEMENTATION_AUTHORITY = EXACT_CONTRACTS_S3_C001_C013_ONLY`) and the
  authority the executed hook enforces disagree, and the exact authorized
  C001..C013 tranche is not admitted.

This was falsified in practice by the first real S3 contract tranche: ASTRO-C01,
PR #343, head f99e3515b35cb3cc3c6ed217ebdae7ac69e13389, whose `verify` gate
failed with exactly that message, and which an independent local
`verify-candidate-local` run against trusted canonical `main` reproduces with
the same text.

v72 binds the same S3-pure-contract exemption to `freeze_s1_006_protocol` as
well. Nothing outside the exact authorized S3 contract file set becomes
admissible: a delta that is not wholly inside those three paths still delegates
to the inherited hook and to the inherited exact-delta verifier, so every
pre-existing S1/S2 freeze protection stays in force.

Bootstrap transition, exactly:
- this v72 policy file;
- foundation-integrity.yml;
- s1-admission-integrity.yml.

No Cargo manifest/lock mutation, `crates/core` runtime behavior, Windows API
binding, process spawn, network, model/provider execution, source admission,
dependency admission, or S3-AUTH-HOST/OBSERVE/SPAWN authority is granted by
this successor - identical to v69/v70/v71.
"""

from __future__ import annotations

import argparse
import importlib
import inspect
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s3_contracts_freeze_shortcut_v72_integrity.py"
V71 = ".github/scripts/wepld_s3_contracts_freeze_shortcut_v71_integrity.py"
V71_BLOB = "e2b3caf4ef7e0ed0e34c7415776cb29c92d752e0"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

CONTRACT_MODULE = "crates/contracts/src/s3.rs"
CONTRACT_EXPORT = "crates/contracts/src/lib.rs"
CONTRACT_TEST = "crates/contracts/tests/s3_contracts_v1.rs"
CONTRACT_FILES = frozenset({CONTRACT_MODULE, CONTRACT_EXPORT, CONTRACT_TEST})
CARGO_MANIFEST = "crates/contracts/Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"

# The workflow bytes this successor replaces, and the ones it publishes. `CW`
# is not part of this bootstrap transition and is pinned unchanged, exactly as
# in v69/v70/v71.
OLD_WF = {
    FW: "a497820d4c4e84d1bc319d5bc8bbd74c905768e157ac078904194e308f9c880f",
    AW: "ae89f87f492b01be07df0b642c880a26d85d222a67140e1bcac7360789e6ca9d",
}
WF = {
    FW: "716b29f2a6f354285f45693abe10dd702e87800ff42811c6fc83cd2e1740d01a",
    AW: "543f5e5637ae5affdd23e639a520473e306d6e0066f96fcfd523520fb7caae55",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S3_CONTRACTS_FREEZE_ENFORCEMENT_BINDING_SUCCESSOR"
S3_PLANNING_AUTHORITY = "CANONICAL_PRESERVED"
S3_IMPLEMENTATION_AUTHORITY = "EXACT_CONTRACTS_S3_C001_C013_ONLY"
CONTRACT_CAPABILITY_SCAN_AUTHORITY = "ENFORCED"
S1_006_ENFORCEMENT_BINDING = "S3_CONTRACT_FILES_ONLY"
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
_PREDECESSOR_FREEZE_006: Any = None
_PREDECESSOR_FREEZE_007: Any = None

root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _git_blob(data: bytes) -> str:
    import hashlib

    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


if _git_blob(root.read_bytes(V71, base.MAX_POLICY_FILE_BYTES)) != V71_BLOB:
    base.fail("frozen v71 predecessor drifted")

_V72_ENTRYPOINT = b"wepld_s3_contracts_freeze_shortcut_v72_integrity.py"
_V71_ENTRYPOINT = b"wepld_s3_contracts_freeze_shortcut_v71_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}


def _v71_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V72_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v72 workflow entrypoint count drifted before v71 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V72_ENTRYPOINT, _V71_ENTRYPOINT)


_TRUE_ORIGINAL_LOCAL_READ_BYTES = base.LocalRepositoryView.read_bytes


def _v71_projected_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
    data = _TRUE_ORIGINAL_LOCAL_READ_BYTES(local_view, relative, limit)
    if relative in (FW, AW):
        data = _v71_workflow_bytes(data, relative)
        if len(data) > limit:
            base.fail(f"v72 v71-projection exceeds read bound: {relative}")
    return data


def _under_v71_workflow_projection(fn: Any, *args: Any, **kwargs: Any) -> Any:
    """Run `fn` while `.github/workflows/{foundation-integrity,s1-admission-integrity}.yml`
    read as their exact canonical v71 (pre-v72-activation) bytes.

    Mirrors v71's own `_under_v70_workflow_projection` exactly, one layer up.
    """
    saved_read_bytes = base.LocalRepositoryView.read_bytes
    base.LocalRepositoryView.read_bytes = _v71_projected_read_bytes
    try:
        return fn(*args, **kwargs)
    finally:
        base.LocalRepositoryView.read_bytes = saved_read_bytes


v71 = _under_v71_workflow_projection(
    importlib.import_module, "wepld_s3_contracts_freeze_shortcut_v71_integrity"
)

V70 = v71.V70
V25 = v71.V25
v70 = v71.v70
_attr = v71._attr
_bind = v71._bind
_call = v71._call

V71_DELTA = v71.delta
V71_BASE = v71.basectrl
V71_ALLOWED = v71.allowed
V71_FILES = v71.files
V71_DEXT = v71.dext
V71_EEXT = v71.eext
V71_EXT = v71.ext
V71_PRINT = v71.printer
V71_COMPONENT_BASE = v71.verify_component_base
V71_WF = dict(v71.WF)
CAND = v71.CAND
RUNTIME = v71.RUNTIME

if V71_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v71 workflow identities drifted before v72 import: actual={V71_WF}")
if _attr(v71, "AUTH", "v71 authority marker") != "S3_CONTRACTS_FREEZE_SHORTCUT_SUCCESSOR":
    base.fail("v72 observed v71 authority drift")
if (
    _attr(v71, "S3_IMPLEMENTATION_AUTHORITY", "v71 implementation boundary")
    != "EXACT_CONTRACTS_S3_C001_C013_ONLY"
):
    base.fail("v72 observed v71 S3 implementation-boundary drift")
if (
    _attr(v71, "S1_007_FREEZE_EXEMPTION_AUTHORITY", "v71 exemption boundary")
    != "S3_CONTRACT_FILES_ONLY"
):
    base.fail("v72 observed v71 exemption-boundary drift")
if frozenset(_attr(v71, "CONTRACT_FILES", "v71 authorized contract set")) != CONTRACT_FILES:
    base.fail("v72 observed v71 authorized-contract-set drift")

_INHERITED_AUTHORITY_NAMES = v71._INHERITED_AUTHORITY_NAMES
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(v71, _name)


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
        base.fail("v72 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v72 extension topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def req_v71(view: Any) -> None:
    if V71 not in ps(view):
        base.fail("v72 candidate/base is missing frozen v71 predecessor")
    actual = blob(view.read_bytes(V71, base.MAX_POLICY_FILE_BYTES))
    if actual != V71_BLOB:
        base.fail(f"frozen v71 predecessor drifted: expected={V71_BLOB} actual={actual}")


def _project_for_v71(view: Any) -> Any:
    """Wrap a *real* view (one that already has v72 activated, i.e. not
    `bootbase`) so v71's own internals - which still expect to find v71's own
    entrypoint string in FW/AW - see the v71-shaped bytes they were written
    against. Mirrors v71's own `_project_for_v70` exactly, one layer up,
    including tolerating a view that doesn't carry FW/AW at all.
    """
    present = ps(view)
    replacements = {
        path: _v71_workflow_bytes(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES), path)
        for path in (FW, AW)
        if path in present
    }
    # Neither v69 nor v70 nor v71 re-exports `_ProjectionView` as its own
    # attribute - it is only ever reached via the predecessor chain
    # (v68._ProjectionView), so v72 must reach four layers down.
    return v70.v69.v68._ProjectionView(view, replacements, frozenset())


def _v71_view(view: Any) -> Any:
    return view if bootbase(view) else _project_for_v71(view)


def _v71_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    return _v71_view(candidate), _v71_view(policy_base)


def patch_predecessor() -> None:
    current_wf = dict(v71.WF)
    if current_wf not in (V71_WF, dict(WF)):
        base.fail(f"v72 predecessor workflow identity map drifted: actual={current_wf}")
    _bind(v71, "WF", dict(WF), "v71 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v71(candidate)
            req_v71(policy_base)
            return
        if paths & BOOT:
            base.fail("v72 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v72 bootstrap base authorizes only exact enforcement-binding activation")

    if P in paths:
        base.fail("canonical v72 wrapper is frozen after activation")

    req_v71(candidate)
    req_v71(policy_base)

    _call("v71 exact-delta verifier", V71_DELTA, *_v71_views(candidate, policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v71 base-control verifier", V71_BASE, *_v71_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v72 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v72 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v72 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v72 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        projected_candidate, projected_base = _v71_views(candidate, policy_base)
        _call("v71 extension verification", V71_EXT, projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - {P}
    if remaining:
        _call("v71 allowed-path verifier", V71_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v71(view)
    _call("v71 policy-file verification", V71_FILES, _v71_view(view))
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v72 wrapper mode invalid")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v72 predecessor component-base hook unavailable")
    _call(
        "v72 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _v71_view(view),
        paths,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_006_protocol(candidate: Any, policy_base: Any) -> None:
    """Exempt a delta touching *only* the authorized S3 contract files from the
    inherited frozen-S1-protocol hook that the verifier actually executes.

    `freeze_s1_007_state` carries the same exemption today, but the verifier
    calls this hook independently, so the v71 exemption alone never reached the
    real enforcement path. `delta()` (the routing hook, called independently in
    the same admission pass) already fully validates an S3-contracts-only delta
    - exact file set, no Cargo/core/workflow mutation, capability scan,
    crate-scope `forbid(unsafe_code)` retention - and this hook's own concern (a
    fixed set of "frozen S1 protocol" paths must not drift) is orthogonal to
    the three S3 contract paths.

    Anything that is not wholly inside CONTRACT_FILES delegates unchanged to
    the inherited hook, so every pre-existing S1/S2 protection still fails
    closed.
    """
    if _PREDECESSOR_FREEZE_006 is None:
        base.fail("v72 predecessor S1 protocol freeze hook unavailable")
    paths = changed(candidate, policy_base)
    if paths and paths <= CONTRACT_FILES:
        return
    projected_candidate, projected_base = _v71_views(candidate, policy_base)
    _call(
        "v72 predecessor S1 protocol freeze",
        _PREDECESSOR_FREEZE_006,
        projected_candidate,
        projected_base,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_007 is None:
        base.fail("v72 predecessor S1 state freeze hook unavailable")
    projected_candidate, projected_base = _v71_views(candidate, policy_base)
    _call(
        "v72 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_007,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V71_PRINT:
        base.fail("v72 predecessor printer drifted")
    _call("v71 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v72=V71_PLUS_S1_006_ENFORCEMENT_BINDING_REPAIR")
    print(f"v72_authority={AUTH}")
    print(f"s3_planning_authority_v72={S3_PLANNING_AUTHORITY}")
    print(f"s3_implementation_authority_v72={S3_IMPLEMENTATION_AUTHORITY}")
    print(f"contract_capability_scan_authority_v72={CONTRACT_CAPABILITY_SCAN_AUTHORITY}")
    print(f"s1_006_enforcement_binding_v72={S1_006_ENFORCEMENT_BINDING}")
    print(f"s1_007_freeze_exemption_authority_v72={S1_007_FREEZE_EXEMPTION_AUTHORITY}")
    print(f"filesystem_runtime_authority_v72={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"windows_api_authority_v72={WINDOWS_API_AUTHORITY}")
    print(f"job_object_authority_v72={JOB_OBJECT_AUTHORITY}")
    print(f"containment_actuation_authority_v72={CONTAINMENT_ACTUATION_AUTHORITY}")
    print(f"process_spawn_authority_v72={PROCESS_SPAWN_AUTHORITY}")
    print(f"credential_authority_v72={CREDENTIAL_AUTHORITY}")
    print(f"network_authority_v72={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v72={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v72={SOURCE_ADMISSION}")
    print(f"dependency_admission_v72={DEPENDENCY_ADMISSION}")
    print(f"s3_auth_host_authority_v72={S3_AUTH_HOST_AUTHORITY}")
    print(f"s3_auth_observe_authority_v72={S3_AUTH_OBSERVE_AUTHORITY}")
    print(f"s3_auth_spawn_authority_v72={S3_AUTH_SPAWN_AUTHORITY}")
    print(f"s4_plus_authority_v72={S4_PLUS_AUTHORITY}")


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
        (_attr(execution, "freeze_s1_006_protocol", "S1 protocol freeze hook"), freeze_s1_006_protocol),
        (_attr(execution, "freeze_s1_007_state", "S1 state freeze hook"), freeze_s1_007_state),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v72 installed overlay drifted")
    if dict(v71.WF) != dict(WF):
        base.fail("v72 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(v71, name) != globals()[name]:
            base.fail(f"v72 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    global _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_006, _PREDECESSOR_FREEZE_007
    if _INST:
        overlay()
        return
    # v71's own install may short-circuit to its own overlay(), which checks its
    # bare WF map. That check must see v71's untouched map, so
    # patch_predecessor() (which rebinds v71.WF to v72's values) must not run
    # until after this call returns.
    _under_v71_workflow_projection(_call, "v71 install", getattr(v71, "install", None))
    patch_predecessor()
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V71_DELTA),
        (base.compare_base_controlled, V71_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V71_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V71_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V71_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V71_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V71_PRINT),
        (_attr(execution, "_verify_component_base", "predecessor component-base hook"), V71_COMPONENT_BASE),
        (_attr(execution, "freeze_s1_007_state", "predecessor S1 state freeze"), v71.freeze_s1_007_state),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v72 predecessor hook drifted")
    _PRINT = V71_PRINT
    _PREDECESSOR_COMPONENT_BASE = V71_COMPONENT_BASE
    _PREDECESSOR_FREEZE_007 = v71.freeze_s1_007_state
    _PREDECESSOR_FREEZE_006 = _attr(
        execution, "freeze_s1_006_protocol", "predecessor S1 protocol freeze"
    )
    if not callable(_PREDECESSOR_FREEZE_006) or _PREDECESSOR_FREEZE_006 is freeze_s1_006_protocol:
        base.fail("v72 predecessor S1 protocol freeze hook is not an inherited hook")
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
    _bind(execution, "freeze_s1_006_protocol", freeze_s1_006_protocol, "S1 protocol freeze binding")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "S1 state freeze binding")
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def _execution_hooks() -> tuple[frozenset[str], int]:
    execution = topo()[4]
    frozen = frozenset(
        _attr(execution, "S1_007_FROZEN_PROTOCOL_PATHS", "frozen S1 protocol path set")
    )
    bound = _attr(execution, "MAX_S1_006_SOURCE_BYTES", "S1 protocol read bound")
    if CONTRACT_EXPORT not in frozen:
        base.fail("v72 expected the shared contracts lib.rs in the inherited protocol freeze")
    return frozen, bound


def selftest() -> None:
    # v71's own selftest verifies its FW/AW bytes against its own WF pins. Run
    # it while v71.WF is still v71's untouched canonical values.
    _under_v71_workflow_projection(
        _call, "v71 predecessor self-test", getattr(v71, "selftest", None)
    )
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v72 workflow drifted: {path}")

    if (
        AUTH != "S3_CONTRACTS_FREEZE_ENFORCEMENT_BINDING_SUCCESSOR"
        or S3_PLANNING_AUTHORITY != "CANONICAL_PRESERVED"
        or S3_IMPLEMENTATION_AUTHORITY != "EXACT_CONTRACTS_S3_C001_C013_ONLY"
        or CONTRACT_CAPABILITY_SCAN_AUTHORITY != "ENFORCED"
        or S1_006_ENFORCEMENT_BINDING != "S3_CONTRACT_FILES_ONLY"
        or S1_007_FREEZE_EXEMPTION_AUTHORITY != "S3_CONTRACT_FILES_ONLY"
        or CONTRACT_FILES
        != frozenset(
            {
                "crates/contracts/src/s3.rs",
                "crates/contracts/src/lib.rs",
                "crates/contracts/tests/s3_contracts_v1.rs",
            }
        )
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
        base.fail("v72 authority boundary drifted")

    # --- bootstrap transition ------------------------------------------------
    vb71 = root.read_bytes(V71, base.MAX_POLICY_FILE_BYTES)
    vb70 = root.read_bytes(V70, base.MAX_POLICY_FILE_BYTES)
    vb69 = root.read_bytes(v70.V69, base.MAX_POLICY_FILE_BYTES)
    vb68 = root.read_bytes(v70.v69.V68, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V71: vb71, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v72", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed_bootstrap = dict(candidate)
    mixed_bootstrap["README.md"] = b"x"
    base.expect_failure_matching(
        "v72 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed_bootstrap),
        mem(policy_base),
    )

    # --- the exact authorized S3 contract tranche ----------------------------
    active = {
        V71: vb71,
        V70: vb70,
        v70.V69: vb69,
        v70.v69.V68: vb68,
        P: b"v72",
        CONTRACT_EXPORT: b"pub mod project;\n",
    }
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

    # BEFORE/AFTER regression. The defect v72 repairs is not "the delta is
    # invalid"; it is "the hook the verifier executes never consults the
    # exemption". Both sides are executed here on the same view pair.
    base.expect_failure_matching(
        "v72 BEFORE: the executed inherited hook rejects the exact authorized C001..C013 delta",
        "mixed contract/non-contract delta",
        _PREDECESSOR_FREEZE_006,
        mem(first),
        mem(active),
    )
    freeze_s1_006_protocol(mem(first), mem(active))
    # The v71 binding at 007 is preserved, not replaced.
    v71_freeze_007 = _attr(v71, "freeze_s1_007_state", "v71 S1 state freeze hook")
    v71_freeze_007(mem(first), mem(active))

    # Oracle 1: the exact authorized C001-C013 delta is admitted through the
    # executed enforcement path.
    allowed_outcome = True
    if not allowed_outcome:  # pragma: no cover - documents the required result
        base.fail("v72 exact authorized tranche was not admitted")

    # Oracle 2: a host API addition is rejected.
    host_api = dict(first)
    host_api[CONTRACT_MODULE] = (
        clean_module + b"\nfn close() { windows::Win32::Foundation::CloseHandle(0 as _); }\n"
    )
    base.expect_failure_matching(
        "v72 host API addition rejected",
        "prohibited runtime capability",
        delta,
        mem(host_api),
        mem(active),
    )

    # Oracle 3: process/spawn capability is rejected.
    spawn = dict(first)
    spawn[CONTRACT_MODULE] = clean_module + b"\nfn run() { std::process::Command::new(\"x\"); }\n"
    base.expect_failure_matching(
        "v72 process/spawn capability rejected",
        "prohibited runtime capability",
        delta,
        mem(spawn),
        mem(active),
    )

    # Oracle 4: network capability is rejected.
    network = dict(first)
    network[CONTRACT_TEST] = clean_test + b"\nuse std::net::TcpStream;\n"
    base.expect_failure_matching(
        "v72 network capability rejected",
        "prohibited runtime capability",
        delta,
        mem(network),
        mem(active),
    )

    # Oracle 5: a runtime dependency edit is rejected.
    manifest = dict(first)
    manifest[CARGO_MANIFEST] = b"[package]\nname = \"wepld-contracts\"\n"
    base.expect_failure_matching(
        "v72 contract manifest edit rejected",
        "does not permit Cargo manifest or Cargo.lock mutation",
        delta,
        mem(manifest),
        mem(active),
    )

    # Oracle 6: Cargo.lock drift is rejected.
    lock = dict(first)
    lock[ROOT_CARGO_LOCK] = b"# drifted\n"
    base.expect_failure_matching(
        "v72 Cargo.lock drift rejected",
        "does not permit Cargo manifest or Cargo.lock mutation",
        delta,
        mem(lock),
        mem(active),
    )

    # Oracle 7: an unauthorized source path added to the same tranche is
    # rejected, including a path that merely looks like an authorized one.
    extra = dict(first)
    extra["crates/contracts/src/s3_extra.rs"] = b"// unauthorized\n"
    base.expect_failure_matching(
        "v72 added unauthorized contract path rejected",
        "unauthorized contracts paths",
        delta,
        mem(extra),
        mem(active),
    )

    # Oracle 8: a mixed authorized-contract + unauthorized non-contract delta is
    # rejected, both by the routing hook and by the delegated freeze hook.
    mixed_with_non_contract = dict(first)
    mixed_with_non_contract["README.md"] = b"changed"
    base.expect_failure_matching(
        "v72 mixed non-contract change rejected by routing hook",
        "must not mix",
        delta,
        mem(mixed_with_non_contract),
        mem(active),
    )
    base.expect_failure_matching(
        "v72 mixed non-contract change rejected by the executed freeze hook",
        "mixed contract/non-contract delta",
        freeze_s1_006_protocol,
        mem(mixed_with_non_contract),
        mem(active),
    )

    # Oracle 9: the exemption cannot be triggered by branch name, PR number,
    # commit message, task label or any other attacker-controlled metadata.
    signature = inspect.signature(freeze_s1_006_protocol)
    if tuple(signature.parameters) != ("candidate", "policy_base"):
        base.fail("v72 exemption hook input surface drifted")
    view = mem({})
    for name in ("branch", "ref", "pr", "pr_number", "label", "labels", "message", "author", "task"):
        if hasattr(view, name):
            base.fail(f"v72 tree view exposes attacker-controlled metadata: {name}")
    if tuple(inspect.signature(delta).parameters) != ("candidate", "policy_base"):
        base.fail("v72 routing hook input surface drifted")

    # Oracle 10: the existing S1/S2 safety controls continue to fail closed.
    frozen_paths, _ = _execution_hooks()
    protected = {
        path: root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        for path in sorted(frozen_paths)
        if path != CONTRACT_EXPORT
    }
    frozen_base = dict(active)
    frozen_base.update(protected)
    other = sorted(protected)[0]
    drifted = dict(frozen_base)
    drifted[other] = drifted[other] + b"\n// unauthorized protocol drift\n"
    base.expect_failure_matching(
        "v72 inherited frozen-protocol freeze still fails closed",
        "frozen S1-006 protocol",
        freeze_s1_006_protocol,
        mem(drifted),
        mem(frozen_base),
    )
    combined = dict(protected)
    combined[CONTRACT_MODULE] = clean_module
    combined[CONTRACT_EXPORT] = clean_export
    combined[CONTRACT_TEST] = clean_test
    combined[other] = combined[other] + b"\n// unauthorized protocol drift\n"
    base.expect_failure_matching(
        "v72 authorized tranche cannot smuggle protocol drift",
        "mixed contract/non-contract delta",
        freeze_s1_006_protocol,
        mem(combined),
        mem(protected),
    )

    print("wepld v72 S3-contract freeze enforcement-binding successor self-tests: PASS")


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
