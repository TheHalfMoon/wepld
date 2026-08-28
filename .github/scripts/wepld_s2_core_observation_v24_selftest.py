#!/usr/bin/env python3
"""Self-tests for the v24 S2 Core observation-foundations successor."""

from typing import Any

import wepld_integrity as base
import wepld_s2_core_observation_bootstrap_v24_integrity as p


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: p.blob(data) for path, data in values.items()})


def run() -> None:
    p.patch_predecessor()
    p._call("v23 predecessor self-test", getattr(p.v23, "selftest", None))
    p.install()

    for path in (p.FW, p.AW):
        if p.sha(p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != p.WF[path]:
            base.fail(f"v24 workflow drifted: {path}")

    if (
        p.AUTH != "S2_CORE_OBSERVATION_FOUNDATIONS_SUCCESSOR"
        or p.S2_IMPLEMENTATION_AUTHORITY != "EXACT_CORE_S2_I001_I004_E001_E002_ONLY"
        or p.FILESYSTEM_RUNTIME_AUTHORITY != "READ_ONLY_CANONICALIZE_SYMLINK_METADATA_ONLY"
        or p.FILESYSTEM_WRITE_AUTHORITY != "NONE"
        or p.ENVIRONMENT_READ_AUTHORITY != "NONE"
        or p.IDENTITY_ALLOCATION_AUTHORITY != "NONE"
        or p.EVIDENCE_STORE_MUTATION_AUTHORITY != "NONE"
        or p.LOCKING_AUTHORITY != "NONE"
        or p.EXTERNAL_PROCESS_AUTHORITY != "NONE"
        or p.GIT_EXECUTION_AUTHORITY != "NONE"
        or p.NETWORK_AUTHORITY != "NONE"
        or p.MODEL_PROVIDER_EXECUTION != "NONE"
        or p.SOURCE_ADMISSION != "NONE"
        or p.DEPENDENCY_ADMISSION != "NONE"
        or p.S3_PLUS_AUTHORITY != "NONE"
    ):
        base.fail("v24 authority marker drift")

    predecessor = p.root.read_bytes(p.V23, base.MAX_POLICY_FILE_BYTES)
    policy = p.root.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES)
    test_policy = p.root.read_bytes(p.T, base.MAX_POLICY_FILE_BYTES)
    support_policy = p.root.read_bytes(p.H, base.MAX_POLICY_FILE_BYTES)
    contract_values = {
        path: p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES) for path in p.CONTRACT_FILES
    }
    core_lib = p.root.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    base_values = {
        p.V23: predecessor, p.P: policy, p.T: test_policy, p.H: support_policy, p.CORE_EXPORT: core_lib, **contract_values
    }
    candidate_values = dict(base_values)
    candidate_values[p.CORE_EXPORT] = core_lib + b"\npub mod project;\npub use project::*;\n"
    candidate_values[p.CORE_MODULE] = b"#![forbid(unsafe_code)]\n\npub fn lexical_only() -> bool { true }\n"
    candidate_values[p.CORE_TEST] = b"#![forbid(unsafe_code)]\n\n#[test]\nfn v24_fixture() { assert!(true); }\n"
    p.delta(mem(candidate_values), mem(base_values))

    extra = dict(candidate_values)
    extra["crates/core/src/extra.rs"] = b"#![forbid(unsafe_code)]\n"
    base.expect_failure_matching(
        "v24 extra Core path", "unauthorized Core paths", p.delta, mem(extra), mem(base_values)
    )

    manifest = dict(candidate_values)
    manifest[p.CORE_MANIFEST] = b"[package]\nname='drift'\n"
    base.expect_failure_matching(
        "v24 dependency/manifest widening",
        "Cargo manifest or lock mutation",
        p.delta,
        mem(manifest),
        mem(base_values),
    )

    process = dict(candidate_values)
    process[p.CORE_MODULE] += b"\nfn bad() { let _ = std::process::Command::new(\"git\"); }\n"
    base.expect_failure_matching(
        "v24 external process effect",
        "unauthorized runtime effect token",
        p.delta,
        mem(process),
        mem(base_values),
    )

    freeze_base = {
        path: p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES) for path in p.FROZEN_STATE_PATHS
    }
    freeze_candidate = dict(freeze_base)
    freeze_candidate[p.CORE_EXPORT] = freeze_base[p.CORE_EXPORT] + b"\npub mod project;\n"
    freeze_candidate[p.CORE_MODULE] = candidate_values[p.CORE_MODULE]
    freeze_candidate[p.CORE_TEST] = candidate_values[p.CORE_TEST]
    base.expect_failure_matching(
        "v23 inherited state freeze rejects shared Core export",
        "frozen S1-007 state",
        p.V23_FREEZE_STATE,
        mem(freeze_candidate),
        mem(freeze_base),
    )
    p.freeze_s1_007_state(mem(freeze_candidate), mem(freeze_base))

    mixed = dict(freeze_candidate)
    frozen_other = next(path for path in sorted(p.FROZEN_STATE_PATHS) if path != p.CORE_EXPORT)
    mixed[frozen_other] = freeze_base[frozen_other] + b"\n// unauthorized drift\n"
    base.expect_failure_matching(
        "v24 freeze repair refuses mixed S2/S1 state drift",
        "mixed Core/non-Core delta",
        p.freeze_s1_007_state,
        mem(mixed),
        mem(freeze_base),
    )

    print("wepld v24 S2 Core observation-foundations successor self-tests: PASS")
