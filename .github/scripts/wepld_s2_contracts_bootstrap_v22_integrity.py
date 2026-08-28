#!/usr/bin/env python3
"""Grant the minimum S2 contracts-only implementation authority for S2-C001..S2-C009.

v22 is an append-only successor to canonical v21. It preserves the complete
canonical S2 planning package and all v21/v20 predecessor boundaries while
authorizing exactly three `crates/contracts` paths for the first S2 contract
tranche:

- crates/contracts/src/project.rs
- crates/contracts/src/lib.rs
- crates/contracts/tests/project_v1.rs

The bootstrap transition is exactly:
- this v22 policy file;
- foundation-integrity.yml;
- s1-admission-integrity.yml.

No Cargo manifest/lock mutation, Core/runtime filesystem behavior, external
process/Git execution, network, model/provider, source admission, dependency
admission, or S3+ authority is granted by this successor.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_contracts_bootstrap_v22_integrity.py"
V21 = ".github/scripts/wepld_s2_planning_bootstrap_v21_integrity.py"
V21_BLOB = "fcfd292c546f17e778fce2397c8a21616aeb4197"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

CONTRACT_MODULE = "crates/contracts/src/project.rs"
CONTRACT_EXPORT = "crates/contracts/src/lib.rs"
CONTRACT_TEST = "crates/contracts/tests/project_v1.rs"
CONTRACT_FILES = frozenset({CONTRACT_MODULE, CONTRACT_EXPORT, CONTRACT_TEST})
CONTRACT_NEW_FILES = frozenset({CONTRACT_MODULE, CONTRACT_TEST})
CONTRACT_PREFIX = "crates/contracts/"
CARGO_MANIFEST = "crates/contracts/Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"

AUTHORIZED_TASKS = frozenset(
    {
        "S2-C001",
        "S2-C002",
        "S2-C003",
        "S2-C004",
        "S2-C005",
        "S2-C006",
        "S2-C007",
        "S2-C008",
        "S2-C009",
    }
)

OLD_WF = {
    FW: "4099ae529de9be5fb653f07e11267e6910f9d2ec05ab40e0775b59d039a845fb",
    AW: "5a8305aca0f10619f6c5dc78c88682ca3cade46d43420da5c76048ba7260c716",
}
WF = {
    FW: "331267630ec9f08053415b97d08886b19a8234cc1edbe2645a3b6282a29a44b1",
    AW: "674b51be041b45dc02c984fd7d2f489a2de8560d915c620b695c7d608380b63f",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S2_CONTRACTS_ONLY_SUCCESSOR"
S2_PLANNING_AUTHORITY = "CANONICAL_PRESERVED"
S2_IMPLEMENTATION_AUTHORITY = "EXACT_CONTRACTS_S2_C001_C009_ONLY"
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
        base.fail(f"v22 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v22 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v22 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v22 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V21, base.MAX_POLICY_FILE_BYTES)) != V21_BLOB:
    base.fail("frozen v21 predecessor drifted")

import wepld_s2_planning_bootstrap_v21_integrity as v21  # noqa: E402

V21_DELTA = v21.delta
V21_BASE = v21.basectrl
V21_ALLOWED = v21.allowed
V21_FILES = v21.files
V21_DEXT = v21.dext
V21_EEXT = v21.eext
V21_EXT = v21.ext
V21_PRINT = v21.printer
V21_WF = dict(v21.WF)
CAND = v21.CAND
RUNTIME = v21.RUNTIME
S2_FILES = frozenset(v21.S2_FILES)
S2_PREFIX = v21.S2_PREFIX

if V21_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v21 workflow identities drifted before v22 import: actual={V21_WF}")
if _attr(v21, "AUTH", "v21 authority marker") != "S2_PLANNING_ONLY_SUCCESSOR":
    base.fail("v22 observed v21 authority drift")
if _attr(v21, "S2_IMPLEMENTATION_AUTHORITY", "v21 S2 implementation boundary") != "NOT_GRANTED":
    base.fail("v22 observed v21 S2 implementation boundary drift")
if _attr(v21, "SOURCE_ADMISSION", "v21 source boundary") != "NONE":
    base.fail("v22 observed v21 source-admission drift")
if _attr(v21, "DEPENDENCY_ADMISSION", "v21 dependency boundary") != "NONE":
    base.fail("v22 observed v21 dependency-admission drift")


def req_v21(view: Any) -> None:
    if V21 not in ps(view):
        base.fail("v22 candidate/base is missing frozen v21 predecessor")
    actual = blob(view.read_bytes(V21, base.MAX_POLICY_FILE_BYTES))
    if actual != V21_BLOB:
        base.fail(f"frozen v21 predecessor drifted: expected={V21_BLOB} actual={actual}")


def req_s2_planning(view: Any) -> None:
    paths = ps(view)
    present = frozenset(path for path in S2_FILES if path in paths)
    unknown = {path for path in paths if path.startswith(S2_PREFIX) and path not in S2_FILES}
    if unknown:
        base.fail(f"v22 canonical S2 planning package contains unauthorized paths: {sorted(unknown)}")
    if present != S2_FILES:
        base.fail("v22 requires the exact complete canonical S2 planning package")
    for path in sorted(S2_FILES):
        if mode(view, path) != "100644":
            base.fail(f"v22 canonical S2 planning file mode invalid: {path}")
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if not data or b"\x00" in data:
            base.fail(f"v22 canonical S2 planning file invalid: {path}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            base.fail(f"v22 canonical S2 planning file is not UTF-8: {path}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v21, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v22 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v22 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v21, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v22 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _new_contract_presence(view: Any) -> frozenset[str]:
    paths = ps(view)
    return frozenset(path for path in CONTRACT_NEW_FILES if path in paths)


def _verify_contract_files(view: Any) -> None:
    paths = ps(view)
    for path in sorted(CONTRACT_FILES & paths):
        if mode(view, path) != "100644":
            base.fail(f"v22 S2 contract file mode invalid: {path}")
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if not data:
            base.fail(f"v22 S2 contract file must be non-empty: {path}")
        if b"\x00" in data:
            base.fail(f"v22 S2 contract file contains NUL bytes: {path}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            base.fail(f"v22 S2 contract file is not UTF-8: {path}")


def patch_predecessor() -> None:
    current_wf = dict(v21.WF)
    if current_wf not in (V21_WF, dict(WF)):
        base.fail(f"v22 predecessor workflow identity map drifted: actual={current_wf}")
    _bind(v21, "WF", dict(WF), "v21 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v21(candidate)
            req_v21(policy_base)
            req_s2_planning(candidate)
            req_s2_planning(policy_base)
            return
        if paths & BOOT:
            base.fail("v22 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v22 bootstrap base authorizes only exact policy/workflow activation")

    if P in paths:
        base.fail("canonical v22 wrapper is frozen after activation")

    req_v21(candidate)
    req_v21(policy_base)
    req_s2_planning(candidate)
    req_s2_planning(policy_base)

    contract_changed = frozenset(paths & CONTRACT_FILES)
    base_contract_presence = _new_contract_presence(policy_base)
    s2_contract_delta = bool(paths & CONTRACT_NEW_FILES) or (
        base_contract_presence == CONTRACT_NEW_FILES and bool(contract_changed)
    )
    if s2_contract_delta:
        if CARGO_MANIFEST in paths or ROOT_CARGO_LOCK in paths:
            base.fail("v22 S2 contracts authority does not permit Cargo manifest or Cargo.lock mutation")
        unknown_contracts = {
            path for path in paths if path.startswith(CONTRACT_PREFIX) and path not in CONTRACT_FILES
        }
        if unknown_contracts:
            base.fail(f"v22 S2 contracts delta contains unauthorized contracts paths: {sorted(unknown_contracts)}")
        if any(path.startswith("crates/core/") for path in paths):
            base.fail("v22 S2 contracts authority does not permit Core/runtime mutation")
        if FW in paths or AW in paths or CW in paths:
            base.fail("v22 S2 contracts authority does not permit workflow mutation")
        if paths != contract_changed:
            base.fail("v22 S2 contracts delta must not mix with any non-contract change")

        base_presence = base_contract_presence
        candidate_presence = _new_contract_presence(candidate)

        if not base_presence:
            if contract_changed != CONTRACT_FILES or candidate_presence != CONTRACT_NEW_FILES:
                base.fail("v22 initial S2 contracts delta must change the exact C001..C009 contract/export/test set")
        elif base_presence == CONTRACT_NEW_FILES:
            if candidate_presence != CONTRACT_NEW_FILES:
                base.fail("v22 canonical S2 contract module/test may not be deleted")
        else:
            base.fail("v22 predecessor contains a partial S2 contract tranche")

        if CONTRACT_EXPORT not in ps(candidate):
            base.fail("v22 S2 contract export file is missing")
        _verify_contract_files(candidate)
        return

    _call("v21 exact-delta verifier", V21_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v21 base-control verifier", V21_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v22 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v22 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v22 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v22 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v21 extension verification", V21_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    path_set = set(paths)
    # Preserve predecessor handling for the already-existing shared lib.rs path;
    # v22 only adds the two new S2 contract-owned paths to the allowlist.
    remaining = path_set - {P, CONTRACT_MODULE, CONTRACT_TEST}
    if remaining:
        _call("v21 allowed-path verifier", V21_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v21(view)
    _call("v21 policy-file verification", V21_FILES, view)
    req_s2_planning(view)
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v22 wrapper mode invalid")
    _verify_contract_files(view)


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V21_PRINT:
        base.fail("v22 predecessor printer drifted")
    _call("v21 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v22=V21_PLUS_S2_CONTRACTS_C001_C009_ONLY")
    print(f"v22_authority={AUTH}")
    print(f"s2_planning_authority_v22={S2_PLANNING_AUTHORITY}")
    print(f"s2_implementation_authority_v22={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"filesystem_runtime_authority_v22={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"external_process_authority_v22={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"git_execution_authority_v22={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v22={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v22={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v22={SOURCE_ADMISSION}")
    print(f"dependency_admission_v22={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v22={S3_PLUS_AUTHORITY}")


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
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v22 installed overlay drifted")
    if dict(v21.WF) != dict(WF):
        base.fail("v22 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v21 install", getattr(v21, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V21_DELTA),
        (base.compare_base_controlled, V21_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V21_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V21_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V21_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V21_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V21_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v22 predecessor hook drifted")
    _PRINT = V21_PRINT
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
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def _planning_fixture() -> dict[str, bytes]:
    return {path: root.read_bytes(path, base.MAX_POLICY_FILE_BYTES) for path in S2_FILES}


def selftest() -> None:
    patch_predecessor()
    _call("v21 predecessor self-test", getattr(v21, "selftest", None))
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v22 workflow drifted: {path}")

    if (
        AUTH != "S2_CONTRACTS_ONLY_SUCCESSOR"
        or S2_PLANNING_AUTHORITY != "CANONICAL_PRESERVED"
        or S2_IMPLEMENTATION_AUTHORITY != "EXACT_CONTRACTS_S2_C001_C009_ONLY"
        or AUTHORIZED_TASKS != frozenset(f"S2-C00{i}" for i in range(1, 10))
        or "S2-C009" not in AUTHORIZED_TASKS
        or CONTRACT_TEST not in CONTRACT_FILES
        or FILESYSTEM_RUNTIME_AUTHORITY != "NONE"
        or EXTERNAL_PROCESS_AUTHORITY != "NONE"
        or GIT_EXECUTION_AUTHORITY != "NONE"
        or NETWORK_AUTHORITY != "NONE"
        or MODEL_PROVIDER_EXECUTION != "NONE"
        or SOURCE_ADMISSION != "NONE"
        or DEPENDENCY_ADMISSION != "NONE"
        or S3_PLUS_AUTHORITY != "NONE"
    ):
        base.fail("v22 authority boundary drifted")

    vb = root.read_bytes(V21, base.MAX_POLICY_FILE_BYTES)
    planning = _planning_fixture()
    policy_base = {V21: vb, FW: b"old-foundation", AW: b"old-admission", **planning}
    candidate = dict(policy_base)
    candidate.update({P: b"v22", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed_bootstrap = dict(candidate)
    mixed_bootstrap["README.md"] = b"x"
    base.expect_failure_matching(
        "v22 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed_bootstrap),
        mem(policy_base),
    )

    active = {V21: vb, P: b"v22", CONTRACT_EXPORT: b"pub mod protocol;\n", **planning}
    first = dict(active)
    first.update(
        {
            CONTRACT_MODULE: b"pub struct ProjectLocator;\n",
            CONTRACT_EXPORT: b"pub mod protocol;\npub mod project;\npub use project::*;\n",
            CONTRACT_TEST: b"#[test]\nfn c009_secret_safe_contract_surface_exists() {}\n",
        }
    )
    delta(mem(first), mem(active))

    partial = dict(active)
    partial[CONTRACT_MODULE] = b"pub struct ProjectLocator;\n"
    partial[CONTRACT_EXPORT] = b"pub mod project;\n"
    base.expect_failure_matching(
        "v22 partial initial contracts",
        "exact C001..C009 contract/export/test set",
        delta,
        mem(partial),
        mem(active),
    )

    unknown = dict(first)
    unknown["crates/contracts/src/unknown_s2.rs"] = b"pub struct Unknown;\n"
    base.expect_failure_matching(
        "v22 unknown contracts path",
        "unauthorized contracts paths",
        delta,
        mem(unknown),
        mem(active),
    )

    mixed = dict(first)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v22 mixed contracts delta",
        "must not mix",
        delta,
        mem(mixed),
        mem(active),
    )

    manifest = dict(first)
    manifest[CARGO_MANIFEST] = b"[package]\nname='changed'\n"
    base.expect_failure_matching(
        "v22 Cargo manifest mutation",
        "Cargo manifest or Cargo.lock",
        delta,
        mem(manifest),
        mem(active),
    )

    lock = dict(first)
    lock[ROOT_CARGO_LOCK] = b"changed"
    base.expect_failure_matching(
        "v22 Cargo.lock mutation",
        "Cargo manifest or Cargo.lock",
        delta,
        mem(lock),
        mem(active),
    )

    core = dict(first)
    core["crates/core/src/project.rs"] = b"pub fn runtime() {}\n"
    base.expect_failure_matching(
        "v22 Core/runtime mutation",
        "Core/runtime mutation",
        delta,
        mem(core),
        mem(active),
    )

    workflow = dict(first)
    workflow[CW] = b"changed"
    base.expect_failure_matching(
        "v22 workflow mutation",
        "workflow mutation",
        delta,
        mem(workflow),
        mem(active),
    )

    predecessor = dict(active)
    predecessor[V21] = b"drift"
    base.expect_failure_matching(
        "v22 predecessor wrapper frozen",
        "frozen v21 predecessor drifted",
        delta,
        mem(predecessor),
        mem(active),
    )

    planning_deleted = dict(first)
    del planning_deleted[sorted(S2_FILES)[0]]
    base.expect_failure_matching(
        "v22 canonical S2 planning package intact",
        "exact complete canonical S2 planning package",
        delta,
        mem(planning_deleted),
        mem(active),
    )

    repair_base = dict(first)
    repair = dict(repair_base)
    repair[CONTRACT_MODULE] = b"pub struct ProjectLocator;\npub struct RepositoryTopology;\n"
    delta(mem(repair), mem(repair_base))

    deletion = dict(repair_base)
    del deletion[CONTRACT_TEST]
    base.expect_failure_matching(
        "v22 contract test deletion",
        "may not be deleted",
        delta,
        mem(deletion),
        mem(repair_base),
    )

    print("wepld v22 S2 contracts-only successor self-tests: PASS")


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
