#!/usr/bin/env python3
"""Self-tests for the v27 repair of the v26 regression fixture."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v27_integrity as r


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(
        values,
        trees={path: r.q.p.blob(data) for path, data in values.items()},
    )


def run() -> None:
    r.prepare_q()
    r.q.prepare_v25()
    r._call("v25 predecessor self-test", getattr(r.q.p, "selftest", None))
    r.install()

    for path in (r.q.p.FW, r.q.p.AW):
        if r.q.p.sha(r.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != r.WF[path]:
            base.fail(f"v27 workflow drifted: {path}")

    if (
        r.AUTH != "S2_IDENTITY_STORE_V26_SELFTEST_REPAIR"
        or r.q.AUTH != "S2_IDENTITY_STORE_DEPENDENCY_GOVERNANCE_REPAIR"
        or r.q.S2_IMPLEMENTATION_AUTHORITY
        != "STAGED_EXACT_DEPENDENCY_REGISTER_THEN_IDENTITY_STORE_PATHS_ONLY"
        or r.q.DEPENDENCY_ADMISSION
        != "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_WITH_REGISTER_ONLY"
        or r.q.SOURCE_ADMISSION != "NONE"
    ):
        base.fail("v27 inherited v26 authority marker drift")

    v24_predecessor = r.root.read_bytes(r.q.p.V24, base.MAX_POLICY_FILE_BYTES)
    v25_policy = r.root.read_bytes(r.q.p.P, base.MAX_POLICY_FILE_BYTES)
    v25_test = r.root.read_bytes(r.q.p.T, base.MAX_POLICY_FILE_BYTES)
    v25_support = r.root.read_bytes(r.q.p.H, base.MAX_POLICY_FILE_BYTES)
    v26_policy = r.root.read_bytes(r.q.P, base.MAX_POLICY_FILE_BYTES)
    v26_test = r.root.read_bytes(r.q.T, base.MAX_POLICY_FILE_BYTES)
    v27_policy = r.root.read_bytes(r.P, base.MAX_POLICY_FILE_BYTES)
    v27_test = r.root.read_bytes(r.T, base.MAX_POLICY_FILE_BYTES)
    core_lib = r.root.read_bytes(r.q.p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    core_manifest = r.root.read_bytes(r.q.p.CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES)
    cargo_lock = r.root.read_bytes(r.q.p.ROOT_CARGO_LOCK, r.q.p.MAX_LOCK_BYTES)
    dependency_register = r.root.read_bytes(
        r.q.DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES
    )

    base_values = {
        r.q.p.V24: v24_predecessor,
        r.q.p.P: v25_policy,
        r.q.p.T: v25_test,
        r.q.p.H: v25_support,
        r.q.P: v26_policy,
        r.q.T: v26_test,
        r.P: v27_policy,
        r.T: v27_test,
        r.q.p.CORE_EXPORT: core_lib,
        r.q.p.CORE_MANIFEST: core_manifest,
        r.q.p.ROOT_CARGO_LOCK: cargo_lock,
        r.q.DEPENDENCY_REGISTER: dependency_register,
    }

    dep_candidate = dict(base_values)
    dep_candidate[r.q.p.CORE_MANIFEST] = r.q.p.ADMITTED_CORE_MANIFEST
    dep_candidate[r.q.p.ROOT_CARGO_LOCK] = r.q.p.expected_admitted_lock(cargo_lock)
    dep_candidate[r.q.DEPENDENCY_REGISTER] = r.q.expected_admitted_register(
        dependency_register
    )
    r.delta(mem(dep_candidate), mem(base_values))

    manifest_lock_only = dict(base_values)
    manifest_lock_only[r.q.p.CORE_MANIFEST] = r.q.p.ADMITTED_CORE_MANIFEST
    manifest_lock_only[r.q.p.ROOT_CARGO_LOCK] = r.q.p.expected_admitted_lock(cargo_lock)
    base.expect_failure_matching(
        "v27 preserves exact dependency-governance tranche",
        "exact manifest/lock/register mutation",
        r.delta,
        mem(manifest_lock_only),
        mem(base_values),
    )

    register_drift = dict(dep_candidate)
    register_drift[r.q.DEPENDENCY_REGISTER] += b"\nunauthorized = drift\n"
    base.expect_failure_matching(
        "v27 preserves exact dependency-register bytes",
        "exact S2 dependency-register append",
        r.delta,
        mem(register_drift),
        mem(base_values),
    )

    uuid_candidate = dict(dep_candidate)
    uuid_candidate[r.q.p.CORE_MANIFEST] = dep_candidate[r.q.p.CORE_MANIFEST].replace(
        b'getrandom = "=0.4.3"\n',
        b'getrandom = "=0.4.3"\nuuid = { version = "=1.24.1", features = ["v4"] }\n',
    )
    base.expect_failure_matching(
        "v27 preserves direct uuid rejection",
        "exact admitted Core manifest",
        r.delta,
        mem(uuid_candidate),
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
fn v27_fixture() { assert!(true); }
"""
    lib = core_lib + b"\npub mod evidence_store;\npub mod identity;\n"

    predep_product = dict(base_values)
    predep_product.update(
        {
            r.q.p.CORE_EXPORT: lib,
            r.q.p.IDENTITY_MODULE: identity,
            r.q.p.STORE_MODULE: store,
            r.q.p.PRODUCT_TEST: tests,
        }
    )
    base.expect_failure_matching(
        "v27 product remains blocked before governed dependency admission",
        "requires canonical exact dependency admission",
        r.delta,
        mem(predep_product),
        mem(base_values),
    )

    admitted_base = dict(dep_candidate)
    product = dict(admitted_base)
    product.update(
        {
            r.q.p.CORE_EXPORT: lib,
            r.q.p.IDENTITY_MODULE: identity,
            r.q.p.STORE_MODULE: store,
            r.q.p.PRODUCT_TEST: tests,
        }
    )
    r.delta(mem(product), mem(admitted_base))

    print("wepld v27 S2 v26-selftest repair successor self-tests: PASS")
