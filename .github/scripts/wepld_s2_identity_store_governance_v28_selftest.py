#!/usr/bin/env python3
"""Self-tests for the v28 exact-head review repair successor."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v28_integrity as p


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(
        values,
        trees={path: p.r.q.p.blob(data) for path, data in values.items()},
    )


def run() -> None:
    p.prepare_r()
    p.r.selftest()
    p.install()

    if (
        p.r.q.p.FILESYSTEM_RUNTIME_AUTHORITY
        != "V24_READ_ONLY_PLUS_LOCAL_STORE_BOUNDED_IO_ONLY"
        or p.r.q.p.DEPENDENCY_ADMISSION
        != "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_ONLY"
        or p.r.q.DEPENDENCY_ADMISSION
        != "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_WITH_REGISTER_ONLY"
        or p.SOURCE_ADMISSION != "NONE"
    ):
        base.fail("v28 inherited authority marker drift")

    for module in (p.r, p.r.q, p.r.q.p):
        if dict(module.WF) != dict(p.WF):
            base.fail("v28 explicit workflow identity projection drifted")

    v24 = p.root.read_bytes(p.r.q.p.V24, base.MAX_POLICY_FILE_BYTES)
    v25_policy = p.root.read_bytes(p.r.q.p.P, base.MAX_POLICY_FILE_BYTES)
    v25_test = p.root.read_bytes(p.r.q.p.T, base.MAX_POLICY_FILE_BYTES)
    v25_support = p.root.read_bytes(p.r.q.p.H, base.MAX_POLICY_FILE_BYTES)
    v26_policy = p.root.read_bytes(p.r.q.P, base.MAX_POLICY_FILE_BYTES)
    v26_test = p.root.read_bytes(p.r.q.T, base.MAX_POLICY_FILE_BYTES)
    v27_policy = p.root.read_bytes(p.r.P, base.MAX_POLICY_FILE_BYTES)
    v27_test = p.root.read_bytes(p.r.T, base.MAX_POLICY_FILE_BYTES)
    v28_policy = p.root.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES)
    v28_test_bytes = p.root.read_bytes(p.T, base.MAX_POLICY_FILE_BYTES)
    core_lib = p.root.read_bytes(p.r.q.p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    core_manifest = p.root.read_bytes(p.r.q.p.CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES)
    cargo_lock = p.root.read_bytes(p.r.q.p.ROOT_CARGO_LOCK, p.r.q.p.MAX_LOCK_BYTES)
    dependency_register = p.root.read_bytes(
        p.r.q.DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES
    )

    base_values = {
        p.r.q.p.V24: v24,
        p.r.q.p.P: v25_policy,
        p.r.q.p.T: v25_test,
        p.r.q.p.H: v25_support,
        p.r.q.P: v26_policy,
        p.r.q.T: v26_test,
        p.r.P: v27_policy,
        p.r.T: v27_test,
        p.P: v28_policy,
        p.T: v28_test_bytes,
        p.r.q.p.CORE_EXPORT: core_lib,
        p.r.q.p.CORE_MANIFEST: core_manifest,
        p.r.q.p.ROOT_CARGO_LOCK: cargo_lock,
        p.r.q.DEPENDENCY_REGISTER: dependency_register,
    }

    dep_candidate = dict(base_values)
    dep_candidate[p.r.q.p.CORE_MANIFEST] = p.r.q.p.ADMITTED_CORE_MANIFEST
    dep_candidate[p.r.q.p.ROOT_CARGO_LOCK] = p.r.q.p.expected_admitted_lock(cargo_lock)
    dep_candidate[p.r.q.DEPENDENCY_REGISTER] = p.r.q.expected_admitted_register(
        dependency_register
    )
    p.delta(mem(dep_candidate), mem(base_values))

    register_only = dict(base_values)
    register_only[p.r.q.DEPENDENCY_REGISTER] = p.r.q.expected_admitted_register(
        dependency_register
    )
    base.expect_failure_matching(
        "v28 register cannot move without exact dependency state",
        "exact manifest/lock/register mutation",
        p.delta,
        mem(register_only),
        mem(base_values),
    )

    changed_history = dict(dep_candidate)
    changed_history[p.r.q.DEPENDENCY_REGISTER] = p.r.q.expected_admitted_register(
        dependency_register.replace(
            b"S1_DIRECT_EXTERNAL_CARGO_DEPENDENCIES = 4",
            b"S1_DIRECT_EXTERNAL_CARGO_DEPENDENCIES = 999",
        )
    )
    base.expect_failure_matching(
        "v28 register must preserve prior bytes",
        "exact S2 dependency-register append",
        p.delta,
        mem(changed_history),
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
fn v28_fixture() { assert!(true); }
"""
    lib = core_lib + b"\npub mod evidence_store;\npub mod identity;\n"
    admitted_base = dict(dep_candidate)
    product = dict(admitted_base)
    product.update(
        {
            p.r.q.p.CORE_EXPORT: lib,
            p.r.q.p.IDENTITY_MODULE: identity,
            p.r.q.p.STORE_MODULE: store,
            p.r.q.p.PRODUCT_TEST: tests,
        }
    )
    p.delta(mem(product), mem(admitted_base))

    mixed_register_product = dict(product)
    mixed_register_product[p.r.q.DEPENDENCY_REGISTER] += b"\n# mixed\n"
    base.expect_failure_matching(
        "v28 product cannot mutate dependency governance",
        "exact manifest/lock/register mutation",
        p.delta,
        mem(mixed_register_product),
        mem(admitted_base),
    )

    missing_forbid = dict(product)
    missing_forbid[p.r.q.p.PRODUCT_TEST] = b"#[test]\nfn missing_forbid() { assert!(true); }\n"
    base.expect_failure_matching(
        "v28 product test must forbid unsafe code",
        "must forbid unsafe code",
        p.delta,
        mem(missing_forbid),
        mem(admitted_base),
    )

    forbidden_effect = dict(product)
    forbidden_effect[p.r.q.p.PRODUCT_TEST] = b"""#![forbid(unsafe_code)]

#[test]
fn forbidden_effect() { let _ = std::process::id(); }
"""
    base.expect_failure_matching(
        "v28 product test must reject forbidden effects",
        "contains unauthorized token",
        p.delta,
        mem(forbidden_effect),
        mem(admitted_base),
    )

    print("wepld v28 S2 exact-head review repair successor self-tests: PASS")
