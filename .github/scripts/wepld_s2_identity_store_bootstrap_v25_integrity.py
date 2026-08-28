#!/usr/bin/env python3
"""Authorize staged S2 identity/evidence-store machinery after canonical v24.

v25 is an append-only successor to canonical v24. It does not immediately
combine dependency admission with runtime mutation. Instead it enforces three
separate canonical states:

1. policy-only v25 activation;
2. one focused Core dependency edge candidate for exact getrandom 0.4.3 and
   sha2 0.10.9, explicitly rejecting a direct uuid edge;
3. only after that dependency state is canonical, an exact four-path Core
   identity/store product tranche.

The product tranche keeps ambient environment reads, external process/Git,
network, model/provider, source admission, Doctor/CLI, and S3+ authority denied.
Filesystem writes are limited by policy and review to the WePLD local data-root
catalog/immutable-generation design frozen by Spec 005. Locking is the bounded
stdlib try-lock protocol only. Opaque IDs use result-bearing OS randomness and
the existing WePLD-owned token contracts; no timestamp/PID/path fallback exists.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_identity_store_bootstrap_v25_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_v25_selftest.py"
H = ".github/scripts/wepld_s2_identity_store_v25_support.py"
T_BLOB = "d297032a3ce9564b276dba2f026b039d24142a45"
H_BLOB = "5251b0a67b4ac18b69edafa55112b5caf25cb4ee"
V24 = ".github/scripts/wepld_s2_core_observation_bootstrap_v24_integrity.py"
V24_BLOB = "a547b48a0517b3cac2b33aaa832a0f31be2b585e"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

CORE_EXPORT = "crates/core/src/lib.rs"
IDENTITY_MODULE = "crates/core/src/identity.rs"
STORE_MODULE = "crates/core/src/evidence_store.rs"
PRODUCT_TEST = "crates/core/tests/identity_store_v1.rs"
PRODUCT_FILES = frozenset({CORE_EXPORT, IDENTITY_MODULE, STORE_MODULE, PRODUCT_TEST})
PRODUCT_NEW_FILES = frozenset({IDENTITY_MODULE, STORE_MODULE, PRODUCT_TEST})
PRODUCT_MODULES = frozenset({IDENTITY_MODULE, STORE_MODULE})
CORE_PREFIX = "crates/core/"
CORE_MANIFEST = "crates/core/Cargo.toml"
ROOT_CARGO = "Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"
DEPENDENCY_FILES = frozenset({CORE_MANIFEST, ROOT_CARGO_LOCK})
MAX_LOCK_BYTES = 2_000_000

BASE_CORE_MANIFEST = b"""[package]
name = "wepld-core"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
wepld-contracts = { path = "../contracts" }
"""
ADMITTED_CORE_MANIFEST = b"""[package]
name = "wepld-core"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
getrandom = "=0.4.3"
sha2 = "=0.10.9"
wepld-contracts = { path = "../contracts" }
"""
BASE_CORE_LOCK_STANZA = b"""[[package]]
name = "wepld-core"
version = "0.0.0"
dependencies = [
 "wepld-contracts",
]
"""
ADMITTED_CORE_LOCK_STANZA = b"""[[package]]
name = "wepld-core"
version = "0.0.0"
dependencies = [
 "getrandom 0.4.3",
 "sha2",
 "wepld-contracts",
]
"""
GETRANDOM_LOCK_IDENTITY = b"""[[package]]
name = "getrandom"
version = "0.4.3"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "300e883d756b2e4ec94e02791f39b04b522276138852cfc41d9fb7e904106099"
"""
SHA2_LOCK_IDENTITY = b"""[[package]]
name = "sha2"
version = "0.10.9"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "a7507d819769d01a365ab707794a4084392c824f54a7a6a7862f8c3d0892b283"
"""
UUID_DIRECT_EDGE_TOKEN = b'uuid = '

AUTHORIZED_PRODUCT_TASKS = frozenset(
    {
        "S2-I008", "S2-I009", "S2-I010", "S2-I011", "S2-I012", "S2-I013", "S2-I014",
        "S2-E003", "S2-E004", "S2-E005", "S2-E006", "S2-E007", "S2-E008",
        "S2-E009", "S2-E010", "S2-E011", "S2-E012", "S2-E013", "S2-E014",
        "S2-E015", "S2-E016", "S2-E017",
    }
)

OLD_WF = {
    FW: "013ec9eb13aad9d9cdc675cb2f241861e92dd0185e6bdcd988bbf0340652aa24",
    AW: "97ac9899044ff8f9f0d57ea9c30afe819ad91ba09637be0ee33d3130a3a624b4",
}
WF = {
    FW: "0e243d84e5776d76ea282dca6b9a3aec8be621204641e570a96b2e843f2cc5e5",
    AW: "15b6351211687876bd3be60a583f09267ee52f3875f3c29b7356b20b8373a762",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

POLICY_FILES = frozenset({P, T, H})
BOOT = frozenset({P, T, H, FW, AW})
AUTH = "S2_IDENTITY_STORE_STAGED_SUCCESSOR"
S2_IMPLEMENTATION_AUTHORITY = "STAGED_EXACT_DEPENDENCY_THEN_IDENTITY_STORE_PATHS_ONLY"
FILESYSTEM_RUNTIME_AUTHORITY = "V24_READ_ONLY_PLUS_LOCAL_STORE_BOUNDED_IO_ONLY"
FILESYSTEM_WRITE_AUTHORITY = "WEPLD_LOCAL_DATA_ROOT_CATALOG_GENERATION_ONLY"
ENVIRONMENT_READ_AUTHORITY = "NONE"
IDENTITY_ALLOCATION_AUTHORITY = "WEPLD_OPAQUE_128_BIT_OS_RANDOM_ONLY_AFTER_DEPENDENCY_ADMISSION"
EVIDENCE_STORE_MUTATION_AUTHORITY = "BOUNDED_CATALOG_IMMUTABLE_GENERATION_CURRENT_ONLY"
LOCKING_AUTHORITY = "STDLIB_FILE_TRY_LOCK_2000MS_25MS_ONLY"
EXTERNAL_PROCESS_AUTHORITY = "NONE"
GIT_EXECUTION_AUTHORITY = "NONE"
NETWORK_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_ONLY"
DIRECT_UUID_CORE_EDGE = "REJECTED"
DIRECT_GETRANDOM_CORE_EDGE = "EXACT_0_4_3_CANDIDATE"
DIRECT_SHA2_CORE_EDGE = "EXACT_0_10_9_CANDIDATE"
S3_PLUS_AUTHORITY = "NONE"


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
for _path, _expected in ((V24, V24_BLOB), (T, T_BLOB), (H, H_BLOB)):
    _actual = _git_blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(f"frozen v25 package input drifted: {_path}: expected={_expected} actual={_actual}")

from wepld_s2_identity_store_v25_support import (  # noqa: E402
    attr as _attr,
    bind as _bind,
    blob,
    call as _call,
    changed,
    extset,
    mode,
    ps,
    sha,
    verify_product_modules as _support_verify_product_modules,
    verify_text_file as _verify_text_file,
)

_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None


import wepld_s2_core_observation_bootstrap_v24_integrity as v24  # noqa: E402

V24_DELTA = v24.delta
V24_BASE = v24.basectrl
V24_ALLOWED = v24.allowed
V24_FILES = v24.files
V24_DEXT = v24.dext
V24_EEXT = v24.eext
V24_EXT = v24.ext
V24_PRINT = v24.printer
V24_COMPONENT_BASE = v24.verify_component_base
V24_FREEZE_STATE = v24.freeze_s1_007_state
V24_WF = dict(v24.WF)
CAND = v24.CAND
RUNTIME = v24.RUNTIME
V24_CORE_FILES = frozenset(v24.CORE_FILES)
FROZEN_STATE_PATHS = frozenset(v24.FROZEN_STATE_PATHS)
MAX_S1_STATE_BYTES = v24.MAX_S1_STATE_BYTES

if V24_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v24 workflow identities drifted before v25 import: actual={V24_WF}")
if _attr(v24, "AUTH", "v24 authority marker") != "S2_CORE_OBSERVATION_FOUNDATIONS_SUCCESSOR":
    base.fail("v25 observed v24 authority drift")
if _attr(v24, "S2_IMPLEMENTATION_AUTHORITY", "v24 implementation boundary") != (
    "EXACT_CORE_S2_I001_I004_E001_E002_ONLY"
):
    base.fail("v25 observed v24 S2 implementation boundary drift")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v24, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v25 topology drifted")
    return value


def req_v24(view: Any) -> None:
    if V24 not in ps(view):
        base.fail("v25 candidate/base is missing frozen v24 predecessor")
    actual = blob(view.read_bytes(V24, base.MAX_POLICY_FILE_BYTES))
    if actual != V24_BLOB:
        base.fail(f"frozen v24 predecessor drifted: expected={V24_BLOB} actual={actual}")


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _read_lock(view: Any) -> bytes:
    return view.read_bytes(ROOT_CARGO_LOCK, MAX_LOCK_BYTES)


def _require_package_identities(lock_bytes: bytes) -> None:
    if lock_bytes.count(GETRANDOM_LOCK_IDENTITY) != 1:
        base.fail("v25 exact getrandom 0.4.3 lock identity drifted")
    if lock_bytes.count(SHA2_LOCK_IDENTITY) != 1:
        base.fail("v25 exact sha2 0.10.9 lock identity drifted")


def _baseline_dependency_state(view: Any) -> bool:
    paths = ps(view)
    if CORE_MANIFEST not in paths or ROOT_CARGO_LOCK not in paths:
        return False
    manifest = view.read_bytes(CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES)
    lock_bytes = _read_lock(view)
    _require_package_identities(lock_bytes)
    return (
        manifest == BASE_CORE_MANIFEST
        and lock_bytes.count(BASE_CORE_LOCK_STANZA) == 1
        and ADMITTED_CORE_LOCK_STANZA not in lock_bytes
    )


def expected_admitted_lock(base_lock: bytes) -> bytes:
    _require_package_identities(base_lock)
    if base_lock.count(BASE_CORE_LOCK_STANZA) != 1:
        base.fail("v25 baseline wepld-core lock stanza drifted")
    if ADMITTED_CORE_LOCK_STANZA in base_lock:
        base.fail("v25 baseline unexpectedly already contains admitted Core lock stanza")
    return base_lock.replace(BASE_CORE_LOCK_STANZA, ADMITTED_CORE_LOCK_STANZA, 1)


def deps_ready(view: Any) -> bool:
    paths = ps(view)
    if CORE_MANIFEST not in paths or ROOT_CARGO_LOCK not in paths:
        return False
    manifest = view.read_bytes(CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES)
    lock_bytes = _read_lock(view)
    _require_package_identities(lock_bytes)
    if UUID_DIRECT_EDGE_TOKEN in manifest:
        return False
    return (
        manifest == ADMITTED_CORE_MANIFEST
        and lock_bytes.count(ADMITTED_CORE_LOCK_STANZA) == 1
        and BASE_CORE_LOCK_STANZA not in lock_bytes
    )


def _verify_dependency_candidate(candidate: Any, policy_base: Any) -> None:
    if not _baseline_dependency_state(policy_base):
        base.fail("v25 dependency candidate requires exact canonical baseline dependency state")
    candidate_manifest = candidate.read_bytes(CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES)
    if candidate_manifest != ADMITTED_CORE_MANIFEST or UUID_DIRECT_EDGE_TOKEN in candidate_manifest:
        base.fail("v25 dependency candidate must use exact admitted Core manifest without uuid")
    base_lock = _read_lock(policy_base)
    candidate_lock = _read_lock(candidate)
    if candidate_lock != expected_admitted_lock(base_lock):
        base.fail("v25 dependency candidate must use exact generated lock delta")
    if not deps_ready(candidate):
        base.fail("v25 dependency candidate did not establish exact admitted dependency state")


def _new_product_presence(view: Any) -> frozenset[str]:
    paths = ps(view)
    return frozenset(path for path in PRODUCT_NEW_FILES if path in paths)


def _verify_product_files(view: Any) -> None:
    paths = ps(view)
    for path in sorted(PRODUCT_FILES & paths):
        _verify_text_file(view, path)
    _support_verify_product_modules(view, PRODUCT_MODULES)
    if PRODUCT_NEW_FILES <= paths:
        lib = view.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
        if lib.count(b"pub mod identity;") != 1 or lib.count(b"pub mod evidence_store;") != 1:
            base.fail("v25 Core export must register identity and evidence_store exactly once")


def patch_predecessor() -> None:
    current = dict(v24.WF)
    if current not in (V24_WF, dict(WF)):
        base.fail(f"v25 predecessor workflow identity map drifted: actual={current}")
    _bind(v24, "WF", dict(WF), "v24 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(v24.v23, candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v24(candidate)
            req_v24(policy_base)
            if not _baseline_dependency_state(candidate) or not _baseline_dependency_state(policy_base):
                base.fail("v25 bootstrap requires unchanged canonical baseline dependency state")
            return
        if paths & BOOT:
            base.fail("v25 bootstrap delta must be exactly three policy files plus two workflows")
        base.fail("v25 bootstrap base authorizes only exact staged identity/store policy activation")

    if paths & POLICY_FILES:
        base.fail("canonical v25 policy files are frozen after activation")

    req_v24(candidate)
    req_v24(policy_base)

    if paths & DEPENDENCY_FILES:
        if paths != DEPENDENCY_FILES:
            base.fail("v25 dependency admission must not mix with any other mutation")
        _verify_dependency_candidate(candidate, policy_base)
        return

    product_changed = frozenset(paths & PRODUCT_FILES)
    base_presence = _new_product_presence(policy_base)
    product_delta = bool(paths & PRODUCT_NEW_FILES) or bool(product_changed) or (
        base_presence == PRODUCT_NEW_FILES and bool(paths & PRODUCT_FILES)
    )
    if product_delta:
        if not deps_ready(policy_base) or not deps_ready(candidate):
            base.fail("v25 identity/store product requires canonical exact dependency admission")
        unknown_core = {
            path
            for path in paths
            if path.startswith(CORE_PREFIX)
            and path not in PRODUCT_FILES
            and path not in V24_CORE_FILES
            and path != CORE_MANIFEST
        }
        if unknown_core:
            base.fail(f"v25 S2 identity/store delta contains unauthorized Core paths: {sorted(unknown_core)}")
        if paths & (DEPENDENCY_FILES | {FW, AW, CW}):
            base.fail("v25 identity/store product must not mix dependency/workflow mutation")
        if paths & (V24_CORE_FILES - {CORE_EXPORT}):
            base.fail("v25 freezes the canonical v24 observation module/test")
        if paths != product_changed:
            base.fail("v25 identity/store product must not mix with non-product paths")

        candidate_presence = _new_product_presence(candidate)
        if not base_presence:
            if product_changed != PRODUCT_FILES or candidate_presence != PRODUCT_NEW_FILES:
                base.fail("v25 initial identity/store delta must change exact module/export/test set")
        elif base_presence == PRODUCT_NEW_FILES:
            if candidate_presence != PRODUCT_NEW_FILES:
                base.fail("v25 canonical identity/store module/test files may not be deleted")
        else:
            base.fail("v25 predecessor contains a partial identity/store product tranche")

        _verify_product_files(candidate)
        return

    if paths & (V24_CORE_FILES - {CORE_EXPORT}):
        base.fail("v25 freezes the completed canonical v24 Core observation tranche")

    _call("v24 exact-delta verifier", V24_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v24 base-control verifier", V24_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v25 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in ps(candidate):
            base.fail(f"v25 policy file missing: {path}")
        if bootbase(policy_base):
            if path in ps(policy_base):
                base.fail(f"v25 policy file unexpectedly in bootstrap base: {path}")
        elif path not in ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v25 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        _call("v24 extension verification", V24_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES - PRODUCT_NEW_FILES - DEPENDENCY_FILES
    if remaining:
        _call("v24 allowed-path verifier", V24_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v24(view)
    _call("v24 policy-file verification", V24_FILES, view)
    missing_policy = POLICY_FILES - ps(view)
    if missing_policy:
        base.fail(f"v25 policy files missing: {sorted(missing_policy)}")
    for path in sorted(POLICY_FILES):
        if mode(view, path) != "100644":
            base.fail(f"v25 policy file mode invalid: {path}")
    if not (_baseline_dependency_state(view) or deps_ready(view)):
        base.fail("v25 Core dependency state is neither exact baseline nor exact admitted form")
    _verify_product_files(view)


def _require_admitted_component_lock_identity(data: bytes) -> None:
    _require_package_identities(data)
    if data.count(ADMITTED_CORE_LOCK_STANZA) != 1 or BASE_CORE_LOCK_STANZA in data:
        base.fail("v25 admitted component Cargo.lock identity drifted")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if not deps_ready(view):
        _call(
            "v24 component-base verifier",
            V24_COMPONENT_BASE,
            view,
            paths,
            allow_core_main_change=allow_core_main_change,
        )
        return

    original_text = base.STAGE_B_TEXT
    original_lock_check = base.require_frozen_component_lock_identity
    patched_text = dict(original_text)
    patched_text.pop(CORE_MANIFEST, None)
    base.STAGE_B_TEXT = patched_text
    base.require_frozen_component_lock_identity = _require_admitted_component_lock_identity
    try:
        _call(
            "v24 admitted-dependency component-base verifier",
            V24_COMPONENT_BASE,
            view,
            paths,
            allow_core_main_change=allow_core_main_change,
        )
    finally:
        base.STAGE_B_TEXT = original_text
        base.require_frozen_component_lock_identity = original_lock_check


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    paths = changed(v24.v23, candidate, policy_base)
    product_changed = frozenset(paths & PRODUCT_FILES)
    if not product_changed:
        _call("v24 inherited S1 state freeze", V24_FREEZE_STATE, candidate, policy_base)
        return
    if paths != product_changed:
        base.fail("v25 Core freeze repair refuses mixed identity/store and frozen S1 state drift")
    if not PRODUCT_NEW_FILES <= ps(candidate):
        _call("v24 inherited S1 state freeze", V24_FREEZE_STATE, candidate, policy_base)
        return
    for relative in sorted(FROZEN_STATE_PATHS - {CORE_EXPORT}):
        if candidate.read_bytes(relative, MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, MAX_S1_STATE_BYTES
        ):
            base.fail(f"v25 S2 identity/store candidate changed frozen S1 state: {relative}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V24_PRINT:
        base.fail("v25 predecessor printer drifted")
    _call("v24 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v25=V24_PLUS_STAGED_S2_IDENTITY_STORE")
    print(f"v25_authority={AUTH}")
    print(f"s2_implementation_authority_v25={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"filesystem_runtime_authority_v25={FILESYSTEM_RUNTIME_AUTHORITY}")
    print(f"filesystem_write_authority_v25={FILESYSTEM_WRITE_AUTHORITY}")
    print(f"environment_read_authority_v25={ENVIRONMENT_READ_AUTHORITY}")
    print(f"identity_allocation_authority_v25={IDENTITY_ALLOCATION_AUTHORITY}")
    print(f"evidence_store_mutation_authority_v25={EVIDENCE_STORE_MUTATION_AUTHORITY}")
    print(f"locking_authority_v25={LOCKING_AUTHORITY}")
    print(f"external_process_authority_v25={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"git_execution_authority_v25={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v25={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v25={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v25={SOURCE_ADMISSION}")
    print(f"dependency_admission_v25={DEPENDENCY_ADMISSION}")
    print(f"direct_uuid_core_edge_v25={DIRECT_UUID_CORE_EDGE}")
    print(f"direct_getrandom_core_edge_v25={DIRECT_GETRANDOM_CORE_EDGE}")
    print(f"direct_sha2_core_edge_v25={DIRECT_SHA2_CORE_EDGE}")
    print(f"s3_plus_authority_v25={S3_PLUS_AUTHORITY}")


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
        base.fail("v25 installed overlay drifted")
    if dict(v24.WF) != dict(WF):
        base.fail("v25 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return

    patch_predecessor()
    _call("v24 install", getattr(v24, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V24_DELTA),
        (base.compare_base_controlled, V24_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V24_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V24_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V24_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V24_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V24_PRINT),
        (_attr(execution, "_verify_component_base", "predecessor component-base hook"), V24_COMPONENT_BASE),
        (_attr(execution, "freeze_s1_007_state", "predecessor S1 state freeze"), V24_FREEZE_STATE),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v25 predecessor hook drifted")

    _PRINT = V24_PRINT
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
    from wepld_s2_identity_store_v25_selftest import run

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