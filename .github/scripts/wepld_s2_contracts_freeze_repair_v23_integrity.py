#!/usr/bin/env python3
"""Repair the inherited S1 protocol freeze for the already-authorized S2 contracts tranche.

v23 is an append-only successor to canonical v22. It grants no new product path
or effect authority. v22 correctly authorizes S2-C001..S2-C009 in exactly three
contracts paths, but the older S1-007+ verifier still freezes the shared
`crates/contracts/src/lib.rs` export file as part of S1-006. That makes the
v22-authorized initial tranche impossible to qualify end-to-end.

This successor preserves the S1 protocol implementation/test bytes and relaxes
only that historical `lib.rs` freeze while the actual candidate delta is wholly
inside v22's exact S2 contract set. v22 remains responsible for the exact-delta,
path, dependency, and effect boundaries.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_contracts_freeze_repair_v23_integrity.py"
V22 = ".github/scripts/wepld_s2_contracts_bootstrap_v22_integrity.py"
V22_BLOB = "63905ee764c35a4398d61b57c3684d1c84c3980c"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

OLD_WF = {
    FW: "331267630ec9f08053415b97d08886b19a8234cc1edbe2645a3b6282a29a44b1",
    AW: "674b51be041b45dc02c984fd7d2f489a2de8560d915c620b695c7d608380b63f",
}
WF = {
    FW: "fb59854a031ccd8e4e134f9b7f8f1341650bd3be9aa234b831138a0945d330df",
    AW: "366e61f9ca118a79c20c0a624471690060842c88a72f56d95cc0f13c924edaba",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S2_CONTRACTS_INHERITED_PROTOCOL_FREEZE_REPAIR_ONLY"
S2_IMPLEMENTATION_AUTHORITY = "EXACT_CONTRACTS_S2_C001_C009_ONLY_UNCHANGED"
FILESYSTEM_RUNTIME_AUTHORITY = "NONE"
EXTERNAL_PROCESS_AUTHORITY = "NONE"
GIT_EXECUTION_AUTHORITY = "NONE"
NETWORK_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
S3_PLUS_AUTHORITY = "NONE"

_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None


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


def _call(label: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(fn):
        base.fail(f"v23 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v23 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v23 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v23 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V22, base.MAX_POLICY_FILE_BYTES)) != V22_BLOB:
    base.fail("frozen v22 predecessor drifted")

import wepld_s2_contracts_bootstrap_v22_integrity as v22  # noqa: E402

V22_DELTA = v22.delta
V22_BASE = v22.basectrl
V22_ALLOWED = v22.allowed
V22_FILES = v22.files
V22_DEXT = v22.dext
V22_EEXT = v22.eext
V22_EXT = v22.ext
V22_PRINT = v22.printer
V22_WF = dict(v22.WF)
CAND = v22.CAND
RUNTIME = v22.RUNTIME
CONTRACT_FILES = frozenset(v22.CONTRACT_FILES)
CONTRACT_MODULE = v22.CONTRACT_MODULE
CONTRACT_EXPORT = v22.CONTRACT_EXPORT
CONTRACT_TEST = v22.CONTRACT_TEST
S2_FILES = frozenset(v22.S2_FILES)

if V22_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v22 workflow identities drifted before v23 import: actual={V22_WF}")
if _attr(v22, "AUTH", "v22 authority marker") != "S2_CONTRACTS_ONLY_SUCCESSOR":
    base.fail("v23 observed v22 authority drift")
if _attr(v22, "S2_IMPLEMENTATION_AUTHORITY", "v22 implementation boundary") != (
    "EXACT_CONTRACTS_S2_C001_C009_ONLY"
):
    base.fail("v23 observed v22 S2 implementation boundary drift")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v22, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v23 topology drifted")
    return value


_EXECUTION = topo()[4]
V22_FREEZE_PROTOCOL = _attr(_EXECUTION, "freeze_s1_006_protocol", "S1 protocol freeze hook")
FROZEN_PROTOCOL_PATHS = frozenset(
    _attr(_EXECUTION, "S1_007_FROZEN_PROTOCOL_PATHS", "frozen S1 protocol path set")
)
MAX_S1_PROTOCOL_BYTES = _attr(_EXECUTION, "MAX_S1_006_SOURCE_BYTES", "S1 protocol read bound")
if CONTRACT_EXPORT not in FROZEN_PROTOCOL_PATHS:
    base.fail("v23 expected shared contracts lib.rs to be in the inherited S1 protocol freeze")


def req_v22(view: Any) -> None:
    if V22 not in ps(view):
        base.fail("v23 candidate/base is missing frozen v22 predecessor")
    actual = blob(view.read_bytes(V22, base.MAX_POLICY_FILE_BYTES))
    if actual != V22_BLOB:
        base.fail(f"frozen v22 predecessor drifted: expected={V22_BLOB} actual={actual}")


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v23 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v22, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v23 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def patch_predecessor() -> None:
    current = dict(v22.WF)
    if current not in (V22_WF, dict(WF)):
        base.fail(f"v23 predecessor workflow identity map drifted: actual={current}")
    _bind(v22, "WF", dict(WF), "v22 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v22(candidate)
            req_v22(policy_base)
            _call("v22 canonical S2 planning verifier", v22.req_s2_planning, candidate)
            _call("v22 base S2 planning verifier", v22.req_s2_planning, policy_base)
            return
        if paths & BOOT:
            base.fail("v23 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v23 bootstrap base authorizes only exact freeze-repair activation")
    if P in paths:
        base.fail("canonical v23 wrapper is frozen after activation")
    _call("v22 exact-delta verifier", V22_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v22 base-control verifier", V22_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v23 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v23 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v23 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v23 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v22 extension verification", V22_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - {P}
    if remaining:
        _call("v22 allowed-path verifier", V22_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v22(view)
    _call("v22 policy-file verification", V22_FILES, view)
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v23 wrapper mode invalid")


def freeze_s1_006_protocol(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    contract_changed = frozenset(paths & CONTRACT_FILES)
    if not contract_changed:
        _call("v22 inherited S1 protocol freeze", V22_FREEZE_PROTOCOL, candidate, policy_base)
        return
    if paths != contract_changed:
        base.fail("v23 S2 contract freeze repair refuses mixed contract/non-contract delta")

    for relative in sorted(FROZEN_PROTOCOL_PATHS - {CONTRACT_EXPORT}):
        if candidate.read_bytes(relative, MAX_S1_PROTOCOL_BYTES) != policy_base.read_bytes(
            relative, MAX_S1_PROTOCOL_BYTES
        ):
            base.fail(f"v23 S2 contract candidate changed frozen S1 protocol: {relative}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V22_PRINT:
        base.fail("v23 predecessor printer drifted")
    _call("v22 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v23=V22_PLUS_SHARED_LIB_PROTOCOL_FREEZE_REPAIR")
    print(f"v23_authority={AUTH}")
    print(f"s2_implementation_authority_v23={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"filesystem_runtime_authority_v23={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"external_process_authority_v23={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"git_execution_authority_v23={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v23={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v23={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v23={SOURCE_ADMISSION}")
    print(f"dependency_admission_v23={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v23={S3_PLUS_AUTHORITY}")


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
        (_attr(execution, "freeze_s1_006_protocol", "S1 protocol freeze hook"), freeze_s1_006_protocol),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v23 installed overlay drifted")
    if dict(v22.WF) != dict(WF):
        base.fail("v23 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v22 install", getattr(v22, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V22_DELTA),
        (base.compare_base_controlled, V22_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V22_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V22_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V22_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V22_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V22_PRINT),
        (_attr(execution, "freeze_s1_006_protocol", "predecessor S1 protocol freeze"), V22_FREEZE_PROTOCOL),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v23 predecessor hook drifted")

    _PRINT = V22_PRINT
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
    _bind(execution, "freeze_s1_006_protocol", freeze_s1_006_protocol, "S1 protocol freeze repair")
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def selftest() -> None:
    patch_predecessor()
    _call("v22 predecessor self-test", getattr(v22, "selftest", None))
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v23 workflow drifted: {path}")

    if (
        AUTH != "S2_CONTRACTS_INHERITED_PROTOCOL_FREEZE_REPAIR_ONLY"
        or S2_IMPLEMENTATION_AUTHORITY != "EXACT_CONTRACTS_S2_C001_C009_ONLY_UNCHANGED"
        or FILESYSTEM_RUNTIME_AUTHORITY != "NONE"
        or EXTERNAL_PROCESS_AUTHORITY != "NONE"
        or GIT_EXECUTION_AUTHORITY != "NONE"
        or NETWORK_AUTHORITY != "NONE"
        or MODEL_PROVIDER_EXECUTION != "NONE"
        or SOURCE_ADMISSION != "NONE"
        or DEPENDENCY_ADMISSION != "NONE"
        or S3_PLUS_AUTHORITY != "NONE"
    ):
        base.fail("v23 authority boundary drifted")

    execution = topo()[4]
    frozen = {
        path: root.read_bytes(path, MAX_S1_PROTOCOL_BYTES)
        for path in _attr(execution, "S1_007_FROZEN_PROTOCOL_PATHS", "frozen protocol fixture set")
    }
    candidate = dict(frozen)
    candidate[CONTRACT_EXPORT] = frozen[CONTRACT_EXPORT] + b"\npub mod project;\n"
    candidate[CONTRACT_MODULE] = b"pub struct ProjectLocator;\n"
    candidate[CONTRACT_TEST] = b"#[test]\nfn s2_contract_fixture() {}\n"

    base.expect_failure_matching(
        "v23 predecessor freeze rejects v22-authorized shared lib change",
        "frozen S1-006 protocol",
        V22_FREEZE_PROTOCOL,
        mem(candidate),
        mem(frozen),
    )
    freeze_s1_006_protocol(mem(candidate), mem(frozen))

    mixed = dict(candidate)
    protocol_path = next(path for path in FROZEN_PROTOCOL_PATHS if path != CONTRACT_EXPORT)
    mixed[protocol_path] = frozen[protocol_path] + b"\n// unauthorized drift\n"
    base.expect_failure_matching(
        "v23 freeze repair refuses mixed S2/S1 protocol drift",
        "mixed contract/non-contract delta",
        freeze_s1_006_protocol,
        mem(mixed),
        mem(frozen),
    )

    print("wepld v23 S2 contracts inherited-protocol-freeze repair self-tests: PASS")


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
