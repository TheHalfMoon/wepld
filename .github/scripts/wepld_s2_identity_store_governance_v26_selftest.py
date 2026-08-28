#!/usr/bin/env python3
"""Self-tests for the v26 S2 dependency-governance repair successor."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v26_integrity as q


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: q.p.blob(data) for path, data in values.items()})


def run() -> None:
    q.prepare_v25()
    q._call("v25 predecessor self-test", getattr(q.p, "selftest", None))
    q.install()

    for path in (q.p.FW, q.p.AW):
        if q.p.sha(q.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != q.WF[path]:
            base.fail(f"v26 workflow drifted: {path}")

    if (
        q.AUTH != "S2_IDENTITY_STORE_DEPENDENCY_GOVERNANCE_REPAIR"
        or q.S2_IMPLEMENTATION_AUTHORITY
        != "STAGED_EXACT_DEPENDENCY_REGISTER_THEN_IDENTITY_STORE_PATHS_ONLY"
        or q.DEPENDENCY_ADMISSION
        != "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_WITH_REGISTER_ONLY"
        or q.SOURCE_ADMISSION != "NONE"
    ):
        base.fail("v26 authority marker drift")

    v24_predecessor = q.root.read_bytes(q.p.V24, base.MAX_POLICY_FILE_BYTES)
    predecessor = q.root.read_bytes(q.p.P, base.MAX_POLICY_FILE_BYTES)
    predecessor_test = q.root.read_bytes(q.p.T, base.MAX_POLICY_FILE_BYTES)
    predecessor_support = q.root.read_bytes(q.p.H, base.MAX_POLICY_FILE_BYTES)
    policy = q.root.read_bytes(q.P, base.MAX_POLICY_FILE_BYTES)
    test_policy = q.root.read_bytes(q.T, base.MAX_POLICY_FILE_BYTES)
    core_lib = q.root.read_bytes(q.p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    core_manifest = q.root.read_bytes(q.p.CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES)
    cargo_lock = q.root.read_bytes(q.p.ROOT_CARGO_LOCK, q.p.MAX_LOCK_BYTES)
    dependency_register = q.root.read_bytes(q.DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES)

    base_values = {
        q.p.V24: v24_predecessor,
        q.p.P: predecessor,
        q.p.T: predecessor_test,
        q.p.H: predecessor_support,
        q.P: policy,
        q.T: test_policy,
        q.p.CORE_EXPORT: core_lib,
        q.p.CORE_MANIFEST: core_manifest,
        q.p.ROOT_CARGO_LOCK: cargo_lock,
        q.DEPENDENCY_REGISTER: dependency_register,
    }

    dep_candidate = dict(base_values)
    dep_candidate[q.p.CORE_MANIFEST] = q.p.ADMITTED_CORE_MANIFEST
    dep_candidate[q.p.ROOT_CARGO_LOCK] = q.p.expected_admitted_lock(cargo_lock)
    dep_candidate[q.DEPENDENCY_REGISTER] = q.expected_admitted_register(dependency_register)
    q.delta(mem(dep_candidate), mem(base_values))

    manifest_lock_only = dict(base_values)
    manifest_lock_only[q.p.CORE_MANIFEST] = q.p.ADMITTED_CORE_MANIFEST
    manifest_lock_only[q.p.ROOT_CARGO_LOCK] = q.p.expected_admitted_lock(cargo_lock)
    base.expect_failure_matching(
        "v26 dependency candidate without governance register",
        "exact manifest/lock/register mutation",
        q.delta,
        mem(manifest_lock_only),
        mem(base_values),
    )

    register_only = dict(base_values)
    register_only[q.DEPENDENCY_REGISTER] = q.expected_admitted_register(dependency_register)
    base.expect_failure_matching(
        "v26 governance register cannot move without exact dependency state",
        "exact manifest/lock/register mutation",
        q.delta,
        mem(register_only),
        mem(base_values),
    )

    register_drift = dict(dep_candidate)
    register_drift[q.DEPENDENCY_REGISTER] += b"\nunauthorized = drift\n"
    base.expect_failure_matching(
        "v26 dependency register drift rejected",
        "exact S2 dependency-register append",
        q.delta,
        mem(register_drift),
        mem(base_values),
    )

    changed_history = dict(dep_candidate)
    changed_history[q.DEPENDENCY_REGISTER] = q.expected_admitted_register(
        dependency_register.replace(
            b"S1_DIRECT_EXTERNAL_CARGO_DEPENDENCIES = 4",
            b"S1_DIRECT_EXTERNAL_CARGO_DEPENDENCIES = 999",
        )
    )
    base.expect_failure_matching(
        "v26 dependency register must preserve prior bytes",
        "exact S2 dependency-register append",
        q.delta,
        mem(changed_history),
        mem(base_values),
    )

    uuid_candidate = dict(dep_candidate)
    uuid_candidate[q.p.CORE_MANIFEST] = dep_candidate[q.p.CORE_MANIFEST].replace(
        b'getrandom = "=0.4.3"\n',
        b'getrandom = "=0.4.3"\nuuid = { version = "=1.24.1", features = ["v4"] }\n',
    )
    base.expect_failure_matching(
        "v26 direct uuid edge rejected",
        "exact admitted Core manifest",
        q.delta,
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
fn v26_fixture() { assert!(true); }
"""
    lib = core_lib + b"\npub mod evidence_store;\npub mod identity;\n"

    predep_product = dict(base_values)
    predep_product.update(
        {
            q.p.CORE_EXPORT: lib,
            q.p.IDENTITY_MODULE: identity,
            q.p.STORE_MODULE: store,
            q.p.PRODUCT_TEST: tests,
        }
    )
    base.expect_failure_matching(
        "v26 product before governed dependency admission",
        "requires canonical exact dependency admission",
        q.delta,
        mem(predep_product),
        mem(base_values),
    )

    admitted_base = dict(dep_candidate)
    product = dict(admitted_base)
    product.update(
        {
            q.p.CORE_EXPORT: lib,
            q.p.IDENTITY_MODULE: identity,
            q.p.STORE_MODULE: store,
            q.p.PRODUCT_TEST: tests,
        }
    )
    q.delta(mem(product), mem(admitted_base))

    mixed_register_product = dict(product)
    mixed_register_product[q.DEPENDENCY_REGISTER] += b"\n# mixed\n"
    base.expect_failure_matching(
        "v26 product cannot mutate dependency governance",
        "exact manifest/lock/register mutation",
        q.delta,
        mem(mixed_register_product),
        mem(admitted_base),
    )

    print("wepld v26 S2 dependency-governance repair successor self-tests: PASS")
