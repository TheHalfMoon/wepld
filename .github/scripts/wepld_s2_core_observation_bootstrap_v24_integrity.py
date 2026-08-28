#!/usr/bin/env python3
"""Authorize the minimum S2 Core observation-foundations tranche.

v24 is an append-only successor to canonical v23 after S2-C001..S2-C009 are
canonical. It authorizes exactly three Core paths for S2-I001..S2-I004 and
S2-E001..S2-E002, with runtime filesystem authority limited to read-only path
observation (`canonicalize` / `symlink_metadata`) and no environment reads,
filesystem writes, external process/Git execution, network, model/provider,
source admission, dependency admission, identity allocation, evidence-store
mutation, or locking authority.

The successor also repairs the inherited S1 state freeze only for the shared
`crates/core/src/lib.rs` export while the candidate delta is wholly inside the
exact v24 Core tranche. All other frozen S1 state paths remain byte-identical.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_core_observation_bootstrap_v24_integrity.py"
T = ".github/scripts/wepld_s2_core_observation_v24_selftest.py"
H = ".github/scripts/wepld_s2_core_observation_v24_support.py"
T_BLOB = "1e0c3db0a6204631ec512123f0ee3d79d7a507b7"
H_BLOB = "c61b85446af799857f4c983333b04a9ebfcf27ab"
V23 = ".github/scripts/wepld_s2_contracts_freeze_repair_v23_integrity.py"
V23_BLOB = "5e5ff96b7887cb48bcbd4105676d02a9b41b28a8"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

CORE_MODULE = "crates/core/src/project.rs"
CORE_EXPORT = "crates/core/src/lib.rs"
CORE_TEST = "crates/core/tests/project_v1.rs"
CORE_FILES = frozenset({CORE_MODULE, CORE_EXPORT, CORE_TEST})
CORE_NEW_FILES = frozenset({CORE_MODULE, CORE_TEST})
CORE_PREFIX = "crates/core/"
CORE_MANIFEST = "crates/core/Cargo.toml"
ROOT_CARGO = "Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"

AUTHORIZED_TASKS = frozenset(
    {"S2-I001", "S2-I002", "S2-I003", "S2-I004", "S2-E001", "S2-E002"}
)

OLD_WF = {
    FW: "fb59854a031ccd8e4e134f9b7f8f1341650bd3be9aa234b831138a0945d330df",
    AW: "366e61f9ca118a79c20c0a624471690060842c88a72f56d95cc0f13c924edaba",
}
# Filled with the exact generated workflow SHA-256 identities below.
WF = {
    FW: "013ec9eb13aad9d9cdc675cb2f241861e92dd0185e6bdcd988bbf0340652aa24",
    AW: "97ac9899044ff8f9f0d57ea9c30afe819ad91ba09637be0ee33d3130a3a624b4",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

POLICY_FILES = frozenset({P, T, H})
BOOT = frozenset({P, T, H, FW, AW})
AUTH = "S2_CORE_OBSERVATION_FOUNDATIONS_SUCCESSOR"
S2_IMPLEMENTATION_AUTHORITY = "EXACT_CORE_S2_I001_I004_E001_E002_ONLY"
FILESYSTEM_RUNTIME_AUTHORITY = "READ_ONLY_CANONICALIZE_SYMLINK_METADATA_ONLY"
FILESYSTEM_WRITE_AUTHORITY = "NONE"
ENVIRONMENT_READ_AUTHORITY = "NONE"
IDENTITY_ALLOCATION_AUTHORITY = "NONE"
EVIDENCE_STORE_MUTATION_AUTHORITY = "NONE"
LOCKING_AUTHORITY = "NONE"
EXTERNAL_PROCESS_AUTHORITY = "NONE"
GIT_EXECUTION_AUTHORITY = "NONE"
NETWORK_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
S3_PLUS_AUTHORITY = "NONE"


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
for _path, _expected in ((V23, V23_BLOB), (T, T_BLOB), (H, H_BLOB)):
    _actual = _git_blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(f"frozen v24 package input drifted: {_path}: expected={_expected} actual={_actual}")

from wepld_s2_core_observation_v24_support import (  # noqa: E402
    attr as _attr,
    bind as _bind,
    blob,
    call as _call,
    changed,
    extset,
    mode,
    ps,
    sha,
    verify_core_files as _support_verify_core_files,
)

_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None


import wepld_s2_contracts_freeze_repair_v23_integrity as v23  # noqa: E402

V23_DELTA = v23.delta
V23_BASE = v23.basectrl
V23_ALLOWED = v23.allowed
V23_FILES = v23.files
V23_DEXT = v23.dext
V23_EEXT = v23.eext
V23_EXT = v23.ext
V23_PRINT = v23.printer
V23_WF = dict(v23.WF)
CAND = v23.CAND
RUNTIME = v23.RUNTIME
CONTRACT_FILES = frozenset(v23.CONTRACT_FILES)

if V23_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v23 workflow identities drifted before v24 import: actual={V23_WF}")
if _attr(v23, "AUTH", "v23 authority marker") != (
    "S2_CONTRACTS_INHERITED_PROTOCOL_FREEZE_REPAIR_ONLY"
):
    base.fail("v24 observed v23 authority drift")
if _attr(v23, "S2_IMPLEMENTATION_AUTHORITY", "v23 implementation boundary") != (
    "EXACT_CONTRACTS_S2_C001_C009_ONLY_UNCHANGED"
):
    base.fail("v24 observed v23 S2 implementation boundary drift")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v23, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v24 topology drifted")
    return value


_EXECUTION = topo()[4]
V23_FREEZE_STATE = _attr(_EXECUTION, "freeze_s1_007_state", "S1 state freeze hook")
V23_COMPONENT_BASE = _attr(_EXECUTION, "_verify_component_base", "component-base verifier")
FROZEN_STATE_PATHS = frozenset(
    _attr(_EXECUTION, "S1_008_FROZEN_STATE_PATHS", "frozen S1 state path set")
)
MAX_S1_STATE_BYTES = _attr(_EXECUTION, "MAX_S1_007_SOURCE_BYTES", "S1 state read bound")
if CORE_EXPORT not in FROZEN_STATE_PATHS:
    base.fail("v24 expected shared Core lib.rs to be in the inherited S1 state freeze")


def req_v23(view: Any) -> None:
    if V23 not in ps(view):
        base.fail("v24 candidate/base is missing frozen v23 predecessor")
    actual = blob(view.read_bytes(V23, base.MAX_POLICY_FILE_BYTES))
    if actual != V23_BLOB:
        base.fail(f"frozen v23 predecessor drifted: expected={V23_BLOB} actual={actual}")


def req_contracts(view: Any) -> None:
    paths = ps(view)
    missing = CONTRACT_FILES - paths
    if missing:
        base.fail(f"v24 requires canonical S2 contracts: missing={sorted(missing)}")


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _new_core_presence(view: Any) -> frozenset[str]:
    paths = ps(view)
    return frozenset(path for path in CORE_NEW_FILES if path in paths)


def _verify_core_files(view: Any) -> None:
    _support_verify_core_files(view, CORE_FILES, CORE_MODULE)


def patch_predecessor() -> None:
    current = dict(v23.WF)
    if current not in (V23_WF, dict(WF)):
        base.fail(f"v24 predecessor workflow identity map drifted: actual={current}")
    _bind(v23, "WF", dict(WF), "v23 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(v23, candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v23(candidate)
            req_v23(policy_base)
            req_contracts(candidate)
            req_contracts(policy_base)
            return
        if paths & BOOT:
            base.fail("v24 bootstrap delta must be exactly three policy files plus two workflows")
        base.fail("v24 bootstrap base authorizes only exact Core-observation policy activation")

    if paths & POLICY_FILES:
        base.fail("canonical v24 policy files are frozen after activation")

    req_v23(candidate)
    req_v23(policy_base)
    req_contracts(candidate)
    req_contracts(policy_base)

    core_changed = frozenset(paths & CORE_FILES)
    base_presence = _new_core_presence(policy_base)
    s2_core_delta = bool(paths & CORE_NEW_FILES) or (
        base_presence == CORE_NEW_FILES and bool(core_changed)
    )
    if s2_core_delta:
        if CORE_MANIFEST in paths or ROOT_CARGO in paths or ROOT_CARGO_LOCK in paths:
            base.fail("v24 Core observation authority does not permit Cargo manifest or lock mutation")
        unknown_core = {
            path for path in paths if path.startswith(CORE_PREFIX) and path not in CORE_FILES
        }
        if unknown_core:
            base.fail(f"v24 S2 Core delta contains unauthorized Core paths: {sorted(unknown_core)}")
        if paths & CONTRACT_FILES:
            base.fail("v24 S2 Core delta may not mutate canonical S2 contracts")
        if FW in paths or AW in paths or CW in paths:
            base.fail("v24 S2 Core product authority does not permit workflow mutation")
        if paths != core_changed:
            base.fail("v24 S2 Core observation delta must not mix with any non-Core change")

        candidate_presence = _new_core_presence(candidate)
        if not base_presence:
            if core_changed != CORE_FILES or candidate_presence != CORE_NEW_FILES:
                base.fail("v24 initial Core observation delta must change exact module/export/test set")
        elif base_presence == CORE_NEW_FILES:
            if candidate_presence != CORE_NEW_FILES:
                base.fail("v24 canonical S2 Core project module/test may not be deleted")
        else:
            base.fail("v24 predecessor contains a partial Core observation tranche")

        _verify_core_files(candidate)
        return

    _call("v23 exact-delta verifier", V23_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v23 base-control verifier", V23_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v24 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in ps(candidate):
            base.fail(f"v24 policy file missing: {path}")
        if bootbase(policy_base):
            if path in ps(policy_base):
                base.fail(f"v24 policy file unexpectedly in bootstrap base: {path}")
        elif path not in ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v24 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        _call("v23 extension verification", V23_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES - {CORE_MODULE, CORE_TEST}
    if remaining:
        _call("v23 allowed-path verifier", V23_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v23(view)
    _call("v23 policy-file verification", V23_FILES, view)
    req_contracts(view)
    missing_policy = POLICY_FILES - ps(view)
    if missing_policy:
        base.fail(f"v24 policy files missing: {sorted(missing_policy)}")
    for path in sorted(POLICY_FILES):
        if mode(view, path) != "100644":
            base.fail(f"v24 policy file mode invalid: {path}")
    _verify_core_files(view)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    # S1's component baseline freezes Core lib.rs. v24 relaxes only that shared
    # export seam; exact-delta and state-freeze checks still guard every byte.
    original = base.STAGE_B_TEXT
    patched = dict(original)
    patched.pop(CORE_EXPORT, None)
    base.STAGE_B_TEXT = patched
    try:
        _call(
            "inherited component-base verifier",
            V23_COMPONENT_BASE,
            view,
            paths,
            allow_core_main_change=allow_core_main_change,
        )
    finally:
        base.STAGE_B_TEXT = original


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    paths = changed(v23, candidate, policy_base)
    core_changed = frozenset(paths & CORE_FILES)
    if not core_changed:
        _call("v23 inherited S1 state freeze", V23_FREEZE_STATE, candidate, policy_base)
        return
    if paths != core_changed:
        base.fail("v24 Core freeze repair refuses mixed Core/non-Core delta")
    if not CORE_NEW_FILES <= ps(candidate):
        _call("v23 inherited S1 state freeze", V23_FREEZE_STATE, candidate, policy_base)
        return

    for relative in sorted(FROZEN_STATE_PATHS - {CORE_EXPORT}):
        if candidate.read_bytes(relative, MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, MAX_S1_STATE_BYTES
        ):
            base.fail(f"v24 S2 Core candidate changed frozen S1 state: {relative}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V23_PRINT:
        base.fail("v24 predecessor printer drifted")
    _call("v23 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v24=V23_PLUS_S2_CORE_OBSERVATION_FOUNDATIONS")
    print(f"v24_authority={AUTH}")
    print(f"s2_implementation_authority_v24={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"filesystem_runtime_authority_v24={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"filesystem_write_authority_v24={FILESYSTEM_WRITE_AUTHORITY}")
    print(f"environment_read_authority_v24={ENVIRONMENT_READ_AUTHORITY}")
    print(f"identity_allocation_authority_v24={IDENTITY_ALLOCATION_AUTHORITY}")
    print(f"evidence_store_mutation_authority_v24={EVIDENCE_STORE_MUTATION_AUTHORITY}")
    print(f"locking_authority_v24={LOCKING_AUTHORITY}")
    print(f"external_process_authority_v24={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"git_execution_authority_v24={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v24={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v24={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v24={SOURCE_ADMISSION}")
    print(f"dependency_admission_v24={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v24={S3_PLUS_AUTHORITY}")


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
        base.fail("v24 installed overlay drifted")
    if dict(v23.WF) != dict(WF):
        base.fail("v24 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return

    patch_predecessor()
    _call("v23 install", getattr(v23, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V23_DELTA),
        (base.compare_base_controlled, V23_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V23_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V23_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V23_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V23_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V23_PRINT),
        (_attr(execution, "_verify_component_base", "predecessor component-base hook"), V23_COMPONENT_BASE),
        (_attr(execution, "freeze_s1_007_state", "predecessor S1 state freeze"), V23_FREEZE_STATE),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v24 predecessor hook drifted")

    _PRINT = V23_PRINT
    _EXPECTED_DESKTOP_EXTENSIONS = frozenset(set(extset(desktop)) | set(POLICY_FILES))
    _EXPECTED_EXECUTION_EXTENSIONS = frozenset(set(extset(execution)) | set(POLICY_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_DESKTOP_EXTENSIONS, "desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_EXECUTION_EXTENSIONS, "execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "allowed hook")
    _bind(shell, "verify_policy_files", files, "files hook")
    _bind(shell, "print_success", printer, "printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_core_observation_v24_selftest import run

    run()


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
