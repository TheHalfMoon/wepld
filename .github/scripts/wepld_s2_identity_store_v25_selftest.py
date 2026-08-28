#!/usr/bin/env python3
"""Self-tests for the v25 S2 identity/store staged successor."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_bootstrap_v25_integrity as p


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: p.blob(data) for path, data in values.items()})


def run() -> None:
    p.patch_predecessor()
    p._call("v24 predecessor self-test", getattr(p.v24, "selftest", None))
    p.install()

    for path in (p.FW, p.AW):
        if p.sha(p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != p.WF[path]:
            base.fail(f"v25 workflow drifted: {path}")

    if (
        p.AUTH != "S2_IDENTITY_STORE_STAGED_SUCCESSOR"
        or p.S2_IMPLEMENTATION_AUTHORITY
        != "STAGED_EXACT_DEPENDENCY_THEN_IDENTITY_STORE_PATHS_ONLY"
        or p.FILESYSTEM_WRITE_AUTHORITY
        != "WEPLD_LOCAL_DATA_ROOT_CATALOG_GENERATION_ONLY"
        or p.ENVIRONMENT_READ_AUTHORITY != "NONE"
        or p.IDENTITY_ALLOCATION_AUTHORITY
        != "WEPLD_OPAQUE_128_BIT_OS_RANDOM_ONLY_AFTER_DEPENDENCY_ADMISSION"
        or p.EVIDENCE_STORE_MUTATION_AUTHORITY
        != "BOUNDED_CATALOG_IMMUTABLE_GENERATION_CURRENT_ONLY"
        or p.LOCKING_AUTHORITY != "STDLIB_FILE_TRY_LOCK_2000MS_25MS_ONLY"
        or p.EXTERNAL_PROCESS_AUTHORITY != "NONE"
        or p.GIT_EXECUTION_AUTHORITY != "NONE"
        or p.NETWORK_AUTHORITY != "NONE"
        or p.MODEL_PROVIDER_EXECUTION != "NONE"
        or p.SOURCE_ADMISSION != "NONE"
        or p.S3_PLUS_AUTHORITY != "NONE"
        or p.DIRECT_UUID_CORE_EDGE != "REJECTED"
        or p.DIRECT_GETRANDOM_CORE_EDGE != "EXACT_0_4_3_CANDIDATE"
        or p.DIRECT_SHA2_CORE_EDGE != "EXACT_0_10_9_CANDIDATE"
    ):
        base.fail("v25 authority marker drift")

    predecessor = p.root.read_bytes(p.V24, base.MAX_POLICY_FILE_BYTES)
    policy = p.root.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES)
    test_policy = p.root.read_bytes(p.T, base.MAX_POLICY_FILE_BYTES)
    support_policy = p.root.read_bytes(p.H, base.MAX_POLICY_FILE_BYTES)
    core_lib = p.root.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    core_manifest = p.root.read_bytes(p.CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES)
    cargo_lock = p.root.read_bytes(p.ROOT_CARGO_LOCK, p.MAX_LOCK_BYTES)

    base_values = {
        p.V24: predecessor,
        p.P: policy,
        p.T: test_policy,
        p.H: support_policy,
        p.CORE_EXPORT: core_lib,
        p.CORE_MANIFEST: core_manifest,
        p.ROOT_CARGO_LOCK: cargo_lock,
    }

    dep_candidate = dict(base_values)
    dep_candidate[p.CORE_MANIFEST] = p.ADMITTED_CORE_MANIFEST
    dep_candidate[p.ROOT_CARGO_LOCK] = p.expected_admitted_lock(cargo_lock)
    p.delta(mem(dep_candidate), mem(base_values))

    uuid_candidate = dict(dep_candidate)
    uuid_candidate[p.CORE_MANIFEST] = dep_candidate[p.CORE_MANIFEST].replace(
        b'getrandom = "=0.4.3"\n',
        b'getrandom = "=0.4.3"\nuuid = { version = "=1.24.1", features = ["v4"] }\n',
    )
    base.expect_failure_matching(
        "v25 direct uuid edge rejected",
        "exact admitted Core manifest",
        p.delta,
        mem(uuid_candidate),
        mem(base_values),
    )

    lock_drift = dict(dep_candidate)
    lock_drift[p.ROOT_CARGO_LOCK] += b"\n# unauthorized lock drift\n"
    base.expect_failure_matching(
        "v25 lock drift rejected",
        "exact generated lock delta",
        p.delta,
        mem(lock_drift),
        mem(base_values),
    )

    identity = b"""#![forbid(unsafe_code)]

pub fn id_fixture() -> bool { true }
"""
    store = b"""#![forbid(unsafe_code)]

pub fn store_fixture() -> bool { true }
"""
    tests = b"""#![forbid(unsafe_code)]

#[test]
fn v25_fixture() { assert!(true); }
"""
    lib = core_lib + b"\npub mod evidence_store;\npub mod identity;\n"

    predep_product = dict(base_values)
    predep_product.update(
        {
            p.CORE_EXPORT: lib,
            p.IDENTITY_MODULE: identity,
            p.STORE_MODULE: store,
            p.PRODUCT_TEST: tests,
        }
    )
    base.expect_failure_matching(
        "v25 product before dependency admission",
        "requires canonical exact dependency admission",
        p.delta,
        mem(predep_product),
        mem(base_values),
    )

    admitted_base = dict(base_values)
    admitted_base[p.CORE_MANIFEST] = p.ADMITTED_CORE_MANIFEST
    admitted_base[p.ROOT_CARGO_LOCK] = p.expected_admitted_lock(cargo_lock)

    product = dict(admitted_base)
    product.update(
        {
            p.CORE_EXPORT: lib,
            p.IDENTITY_MODULE: identity,
            p.STORE_MODULE: store,
            p.PRODUCT_TEST: tests,
        }
    )
    p.delta(mem(product), mem(admitted_base))

    extra = dict(product)
    extra["crates/core/src/extra_identity.rs"] = b"#![forbid(unsafe_code)]\n"
    base.expect_failure_matching(
        "v25 extra Core path",
        "unauthorized Core paths",
        p.delta,
        mem(extra),
        mem(admitted_base),
    )

    mixed = dict(product)
    mixed[p.CORE_MANIFEST] = admitted_base[p.CORE_MANIFEST] + b"\n# mixed\n"
    base.expect_failure_matching(
        "v25 mixed product/dependency mutation",
        "must not mix",
        p.delta,
        mem(mixed),
        mem(admitted_base),
    )

    env_effect = dict(product)
    env_effect[p.IDENTITY_MODULE] += b'\nfn bad() { let _ = std::env::var("HOME"); }\n'
    base.expect_failure_matching(
        "v25 ambient environment read rejected",
        "unauthorized token",
        p.delta,
        mem(env_effect),
        mem(admitted_base),
    )

    panic_effect = dict(product)
    panic_effect[p.IDENTITY_MODULE] += b'\nfn bad() { panic!("rng"); }\n'
    base.expect_failure_matching(
        "v25 panic path rejected",
        "unauthorized token",
        p.delta,
        mem(panic_effect),
        mem(admitted_base),
    )

    freeze_base = {
        path: p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES) for path in p.FROZEN_STATE_PATHS
    }
    freeze_base.update(
        {
            p.CORE_MANIFEST: p.ADMITTED_CORE_MANIFEST,
            p.ROOT_CARGO_LOCK: p.expected_admitted_lock(cargo_lock),
        }
    )
    freeze_candidate = dict(freeze_base)
    freeze_candidate.update(
        {
            p.CORE_EXPORT: lib,
            p.IDENTITY_MODULE: identity,
            p.STORE_MODULE: store,
            p.PRODUCT_TEST: tests,
        }
    )
    base.expect_failure_matching(
        "v24 inherited freeze rejects identity/store export",
        "mixed Core/non-Core delta",
        p.V24_FREEZE_STATE,
        mem(freeze_candidate),
        mem(freeze_base),
    )
    p.freeze_s1_007_state(mem(freeze_candidate), mem(freeze_base))

    frozen_other = next(path for path in sorted(p.FROZEN_STATE_PATHS) if path != p.CORE_EXPORT)
    bad_freeze = dict(freeze_candidate)
    bad_freeze[frozen_other] = freeze_base[frozen_other] + b"\n// unauthorized drift\n"
    base.expect_failure_matching(
        "v25 freeze repair refuses mixed S2/S1 state drift",
        "mixed identity/store and frozen S1 state drift",
        p.freeze_s1_007_state,
        mem(bad_freeze),
        mem(freeze_base),
    )

    print("wepld v25 S2 identity/store staged successor self-tests: PASS")
