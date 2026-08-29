#!/usr/bin/env python3
"""Self-tests for the v29 getrandom provenance repair successor."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v29_integrity as p


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(
        values,
        trees={path: p.s.r.q.p.blob(data) for path, data in values.items()},
    )


def run() -> None:
    p.prepare_s()
    p.s.selftest()
    p.install()

    corrected = p.s.r.q.S2_DEPENDENCY_REGISTER_APPEND
    if corrected.count(p.CORRECT_GETRANDOM_SOURCE_REVISION) != 1:
        base.fail("v29 corrected getrandom source revision is not unique")
    if p.INCORRECT_GETRANDOM_SOURCE_REVISION in corrected:
        base.fail("v29 incorrect getrandom source revision remains present")
    if corrected.count(p.SHA2_SOURCE_REVISION) != 1:
        base.fail("v29 sha2 source revision drifted during getrandom repair")

    if (
        p.S2_IMPLEMENTATION_AUTHORITY
        != "STAGED_EXACT_DEPENDENCY_REGISTER_THEN_IDENTITY_STORE_PATHS_ONLY"
        or p.DEPENDENCY_ADMISSION
        != "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_WITH_REGISTER_ONLY"
        or p.SOURCE_ADMISSION != "NONE"
        or p.s.r.q.p.DIRECT_UUID_CORE_EDGE != "REJECTED"
    ):
        base.fail("v29 inherited authority marker drift")

    for module in (p.s, p.s.r, p.s.r.q, p.s.r.q.p):
        if dict(module.WF) != dict(p.WF):
            base.fail("v29 explicit workflow identity projection drifted")

    v24 = p.root.read_bytes(p.s.r.q.p.V24, base.MAX_POLICY_FILE_BYTES)
    v25_policy = p.root.read_bytes(p.s.r.q.p.P, base.MAX_POLICY_FILE_BYTES)
    v25_test = p.root.read_bytes(p.s.r.q.p.T, base.MAX_POLICY_FILE_BYTES)
    v25_support = p.root.read_bytes(p.s.r.q.p.H, base.MAX_POLICY_FILE_BYTES)
    v26_policy = p.root.read_bytes(p.s.r.q.P, base.MAX_POLICY_FILE_BYTES)
    v26_test = p.root.read_bytes(p.s.r.q.T, base.MAX_POLICY_FILE_BYTES)
    v27_policy = p.root.read_bytes(p.s.r.P, base.MAX_POLICY_FILE_BYTES)
    v27_test = p.root.read_bytes(p.s.r.T, base.MAX_POLICY_FILE_BYTES)
    v28_policy = p.root.read_bytes(p.s.P, base.MAX_POLICY_FILE_BYTES)
    v28_test = p.root.read_bytes(p.s.T, base.MAX_POLICY_FILE_BYTES)
    v29_policy = p.root.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES)
    v29_test = p.root.read_bytes(p.T, base.MAX_POLICY_FILE_BYTES)
    core_lib = p.root.read_bytes(p.s.r.q.p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    core_manifest = p.root.read_bytes(
        p.s.r.q.p.CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES
    )
    cargo_lock = p.root.read_bytes(
        p.s.r.q.p.ROOT_CARGO_LOCK, p.s.r.q.p.MAX_LOCK_BYTES
    )
    dependency_register = p.root.read_bytes(
        p.s.r.q.DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES
    )

    base_values = {
        p.s.r.q.p.V24: v24,
        p.s.r.q.p.P: v25_policy,
        p.s.r.q.p.T: v25_test,
        p.s.r.q.p.H: v25_support,
        p.s.r.q.P: v26_policy,
        p.s.r.q.T: v26_test,
        p.s.r.P: v27_policy,
        p.s.r.T: v27_test,
        p.s.P: v28_policy,
        p.s.T: v28_test,
        p.P: v29_policy,
        p.T: v29_test,
        p.s.r.q.p.CORE_EXPORT: core_lib,
        p.s.r.q.p.CORE_MANIFEST: core_manifest,
        p.s.r.q.p.ROOT_CARGO_LOCK: cargo_lock,
        p.s.r.q.DEPENDENCY_REGISTER: dependency_register,
    }

    dep_candidate = dict(base_values)
    dep_candidate[p.s.r.q.p.CORE_MANIFEST] = p.s.r.q.p.ADMITTED_CORE_MANIFEST
    dep_candidate[p.s.r.q.p.ROOT_CARGO_LOCK] = p.s.r.q.p.expected_admitted_lock(
        cargo_lock
    )
    dep_candidate[p.s.r.q.DEPENDENCY_REGISTER] = p.s.r.q.expected_admitted_register(
        dependency_register
    )
    p.delta(mem(dep_candidate), mem(base_values))

    wrong_revision = dict(dep_candidate)
    wrong_revision[p.s.r.q.DEPENDENCY_REGISTER] = (
        dependency_register
        + corrected.replace(
            p.CORRECT_GETRANDOM_SOURCE_REVISION,
            p.INCORRECT_GETRANDOM_SOURCE_REVISION,
            1,
        )
    )
    base.expect_failure_matching(
        "v29 rejects old getrandom provenance",
        "exact S2 dependency-register append",
        p.delta,
        mem(wrong_revision),
        mem(base_values),
    )

    register_only = dict(base_values)
    register_only[p.s.r.q.DEPENDENCY_REGISTER] = p.s.r.q.expected_admitted_register(
        dependency_register
    )
    base.expect_failure_matching(
        "v29 register cannot move without exact dependency state",
        "exact manifest/lock/register mutation",
        p.delta,
        mem(register_only),
        mem(base_values),
    )

    changed_history = dict(dep_candidate)
    changed_history[p.s.r.q.DEPENDENCY_REGISTER] = p.s.r.q.expected_admitted_register(
        dependency_register.replace(
            b"S1_DIRECT_EXTERNAL_CARGO_DEPENDENCIES = 4",
            b"S1_DIRECT_EXTERNAL_CARGO_DEPENDENCIES = 999",
        )
    )
    base.expect_failure_matching(
        "v29 register must preserve prior bytes",
        "exact S2 dependency-register append",
        p.delta,
        mem(changed_history),
        mem(base_values),
    )

    print("wepld v29 S2 getrandom provenance repair successor self-tests: PASS")
