#!/usr/bin/env python3
"""Bounded v5 successor policy for the one-time V2.3 canonicalization route.

v5 is an append-only successor to the frozen v4 S1 admission policy. It preserves
all ordinary v4 routes and trust properties, while adding exactly one
base-controlled transition: the two-file V2.3 canonicalization defined by
canonical Spec 004.

The v5 bootstrap is intentionally self-limiting:
- v4 is bound by exact Git blob identity before import;
- the two selector workflows are bound by exact predecessor/candidate digests;
- bootstrap changes are exactly v5 + the two selector workflows;
- the later canonicalization route requires the exact frozen V2.3 candidate and
  exact V2.2 index, derives exact output bytes, and rejects every extra path;
- no source, dependency, donor-execution, runtime, provider, model-weight, or
  inference authority is added.

The old canonical v4 trusted-base policy is expected to reject the unseen v5
successor. That result remains EXPECTED_BOOTSTRAP_FAILURE and is never PASS.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
from typing import Any, Callable

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v5_integrity.py"
V4_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v4_integrity.py"
EXPECTED_V4_POLICY_GIT_BLOB_SHA1 = "2b7954e9d7bc6ae007d47e75319da3e76df3331f"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "96e56fad757c73d4d960e6dfcc17912aebe5d28669e46ef6cf740d3936edc937",
    ADMISSION_WORKFLOW: "bf36b9b2552c0ad32a4c321c496c9ddabe0f353934ff537b82f766a5133f90be",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "360564599ad04878b3fbf34f79891e1ea8cf44580628208c28797567ef1a37f8",
    ADMISSION_WORKFLOW: "d37d45061d700e58d9ca531fe8636f431d0b51edc3e809487714b4f8ad9f85b0",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})

V2_3_CANDIDATE_PATH = "docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE_CANDIDATE.md"
EXPECTED_V2_3_CANDIDATE_GIT_BLOB_SHA1 = "dec247a463f05764a69ceb9e3c7553c2456a1a68"
MASTER_PLAN_INDEX = "docs/canonical/MASTER_PLAN_INDEX.md"
EXPECTED_V2_2_INDEX_GIT_BLOB_SHA1 = "d9fdef3e24d45995101275c23dc7aabb2a27711e"
CANONICAL_PLAN_PATH = "docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md"
CANONICALIZATION_DELTA_PATHS = frozenset({CANONICAL_PLAN_PATH, MASTER_PLAN_INDEX})

AUTHORITY_EXPANSION = "V2_3_EXACT_TWO_FILE_CANONICALIZATION_ROUTE_ONLY"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
PRODUCT_RUNTIME_ADMISSION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
CANDIDATE_VERIFY_AUTHORITY = "NONE"
CANDIDATE_POLICY_BASE_SOURCE = "LOCAL_FETCHED_GIT_WORKTREE"

TRUSTED_BASE_V4_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(
        files,
        trees={path: _git_blob_sha1(data) for path, data in files.items()},
    )


def _bind_v4_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(V4_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V4_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 steady-state routing v4 predecessor drifted before import: "
            f"expected={EXPECTED_V4_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_v4_before_import()
import wepld_s1_admission_steady_state_routing_v4_integrity as v4  # noqa: E402


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    topology = v4._topology()
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("S1 steady-state routing v5 inherited topology is malformed")
    return topology


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"S1 steady-state routing v5 {label} topology is malformed")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"S1 steady-state routing v5 {label} contains non-string path")
    return frozenset(value)


def _replace_once(data: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if data.count(old) != 1:
        base.fail(f"V2.3 canonicalization {label} source marker count is not exactly one")
    return data.replace(old, new, 1)


def _require_blob(data: bytes, expected: str, label: str) -> None:
    actual = _git_blob_sha1(data)
    if actual != expected:
        base.fail(f"{label} drifted: expected={expected} actual={actual}")


def _derive_canonical_plan(candidate_bytes: bytes) -> bytes:
    _require_blob(
        candidate_bytes,
        EXPECTED_V2_3_CANDIDATE_GIT_BLOB_SHA1,
        "frozen V2.3 candidate plan",
    )
    result = candidate_bytes
    replacements = (
        (
            b"# WePLD Master Architecture & Execution Plan \xe2\x80\x94 V2.3 Agent Control Plane Candidate\n",
            b"# WePLD Master Architecture & Execution Plan \xe2\x80\x94 V2.3 Agent Control Plane\n",
            "title",
        ),
        (
            b"STATUS = CANDIDATE / NON-CANONICAL\n",
            b"STATUS = CANONICAL\n",
            "status",
        ),
        (
            b"TRUSTED_CANONICAL_PLAN = V2.2\n",
            b"PREDECESSOR_CANONICAL_PLAN = V2.2\n",
            "predecessor-plan",
        ),
        (
            b"TRUSTED_CANONICAL_BASE = 08a06e9f2664735eb55db5b2f49f95d3d3f91c3f\n",
            b"PREDECESSOR_CANONICAL_BASE = 08a06e9f2664735eb55db5b2f49f95d3d3f91c3f\n",
            "predecessor-base",
        ),
        (
            b"CANDIDATE_NAME = V2.3-AGENT-CONTROL-PLANE\n",
            b"CANONICAL_PLAN_NAME = V2.3-AGENT-CONTROL-PLANE\n",
            "plan-name",
        ),
    )
    for old, new, label in replacements:
        result = _replace_once(result, old, new, label)
    return result


def _derive_index(canonical_plan: bytes) -> bytes:
    digest = _sha256(canonical_plan)
    text = f"""# Master Architecture & Execution Plan Index

```text
CANONICAL_PLAN_VERSION = V2.3
FULL_PLAN_SHA256 = {digest}
CANONICAL_PLAN_PATH = {CANONICAL_PLAN_PATH}
ROADMAP = P0 + S1..S10
NON_PRIMARY_GATE = S3-D
ARCHITECTURE_REOPENED = NO
ENRICHMENT_CLASS = BOUNDED_ENRICHMENT
```

## Roadmap

- P0 — architecture/governance/minimal contracts/acquisition/benchmark/build-method.
- S1 — Desktop ↔ Rust Trusted Core handshake.
- S2 — Open Project + Project Doctor + local identity/storage.
- S3 — Terminal Fabric + trusted process ownership + Windows qualification foundation.
- S3-D — non-primary deterministic assurance seed gate.
- S4 — Fehrest Minimum / Project Brain bootstrap.
- S5 — Spec Kit mechanics + AGILLE + Plan Qualification + Ponytail sufficiency.
- S6 — UWC + Mirefa Minimum + Edara Minimum.
- S7 — Native Review & Assurance.
- S8 — Controlled Repair + bounded fallback/reassignment + Trusted Completion.
- S9 — Quality Passport + Recovery Time Machine + ChangeUnit/Delivery evidence.
- S10 — Fehrest expansion + Byan outcome/benchmark analytics candidate.

The exact canonical V2.3 plan is identified by the path and SHA-256 above. V2.3 is a bounded enrichment of V2.2 and preserves the P0 + S1..S10 roadmap. This index remains the lightweight restoration entrypoint; source, dependency, runtime, provider, model, and future-slice authority remain separately governed.
"""
    return text.encode("utf-8")


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _is_canonicalization_delta(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> bool:
    _, _, impl, _, _ = _topology()
    changed = _require_path_set(impl._changed_paths(candidate, policy_base), "changed-path")
    return changed == CANONICALIZATION_DELTA_PATHS


def _require_v4_candidate(candidate: base.RepositoryView) -> None:
    if V4_POLICY_PATH not in _paths(candidate):
        base.fail("S1 steady-state routing v5 bootstrap requires frozen v4 predecessor")
    actual = _git_blob_sha1(candidate.read_bytes(V4_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V4_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "S1 steady-state routing v4 candidate policy drifted: "
            f"expected={EXPECTED_V4_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_exact_canonicalization(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    base_paths = _paths(policy_base)
    candidate_paths = _paths(candidate)

    if CANONICAL_PLAN_PATH in base_paths:
        base.fail("V2.3 canonicalization is one-time; canonical plan already exists in trusted base")
    if CANONICAL_PLAN_PATH not in candidate_paths:
        base.fail("V2.3 canonicalization candidate is missing canonical plan")

    base_candidate_bytes = policy_base.read_bytes(
        V2_3_CANDIDATE_PATH, base.MAX_POLICY_FILE_BYTES
    )
    candidate_source_bytes = candidate.read_bytes(
        V2_3_CANDIDATE_PATH, base.MAX_POLICY_FILE_BYTES
    )
    _require_blob(
        base_candidate_bytes,
        EXPECTED_V2_3_CANDIDATE_GIT_BLOB_SHA1,
        "trusted-base V2.3 candidate plan",
    )
    if candidate_source_bytes != base_candidate_bytes:
        base.fail("frozen V2.3 candidate plan changed during canonicalization")

    base_index = policy_base.read_bytes(MASTER_PLAN_INDEX, base.MAX_POLICY_FILE_BYTES)
    _require_blob(
        base_index,
        EXPECTED_V2_2_INDEX_GIT_BLOB_SHA1,
        "trusted-base V2.2 master-plan index",
    )

    expected_plan = _derive_canonical_plan(base_candidate_bytes)
    actual_plan = candidate.read_bytes(CANONICAL_PLAN_PATH, base.MAX_POLICY_FILE_BYTES)
    if actual_plan != expected_plan:
        base.fail("V2.3 canonical plan bytes are not the deterministic metadata-only transform")

    expected_index = _derive_index(expected_plan)
    actual_index = candidate.read_bytes(MASTER_PLAN_INDEX, base.MAX_POLICY_FILE_BYTES)
    if actual_index != expected_index:
        base.fail("V2.3 master-plan index bytes are not the deterministic canonical index")


def _require_exact_delta_v5(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, impl, _, _ = _topology()
    changed = _require_path_set(impl._changed_paths(candidate, policy_base), "changed-path")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_v4_candidate(candidate)
            actual_base_v4 = _git_blob_sha1(
                policy_base.read_bytes(V4_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
            )
            if actual_base_v4 != EXPECTED_V4_POLICY_GIT_BLOB_SHA1:
                base.fail(
                    "S1 steady-state routing v5 trusted-base v4 predecessor drifted: "
                    f"expected={EXPECTED_V4_POLICY_GIT_BLOB_SHA1} actual={actual_base_v4}"
                )
            snapshot_present = v4.v3.v2.v1.prior.prior._snapshot_present
            if snapshot_present(candidate) and not snapshot_present(policy_base):
                base.fail("source snapshot cannot transition during S1 routing v5 bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 steady-state routing v5 bootstrap delta must be exactly "
                "the v5 policy plus Foundation and admission workflows"
            )

    if changed == CANONICALIZATION_DELTA_PATHS:
        _require_exact_canonicalization(candidate, policy_base)
        return
    if changed & CANONICALIZATION_DELTA_PATHS:
        base.fail(
            "V2.3 canonicalization delta must be exactly the canonical plan plus master-plan index"
        )

    v4._require_exact_delta_v4(candidate, policy_base)


def _compare_base_controlled_v5(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    canonicalizing = _is_canonicalization_delta(candidate, policy_base)
    if canonicalizing:
        _require_exact_canonicalization(candidate, policy_base)

    controlled = _require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")
    expected_index = None
    if canonicalizing:
        base_candidate = policy_base.read_bytes(V2_3_CANDIDATE_PATH, base.MAX_POLICY_FILE_BYTES)
        expected_index = _derive_index(_derive_canonical_plan(base_candidate))

    for relative in sorted(controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "S1 steady-state routing v5 workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                base.fail(
                    "S1 steady-state routing v5 trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"S1 steady-state routing v5 steady-state workflow changed: {relative}")
            continue

        if canonicalizing and relative == MASTER_PLAN_INDEX:
            if expected_index is None or candidate_bytes != expected_index:
                base.fail("V2.3 master-plan index failed exact base-controlled transform")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    snapshot_present = v4.v3.v2.v1.prior.prior._snapshot_present
    verify_snapshot = v4.v3.v2.v1.prior.prior._verify_snapshot
    base_has_snapshot = snapshot_present(policy_base)
    candidate_has_snapshot = snapshot_present(candidate)
    if base_has_snapshot:
        if not candidate_has_snapshot:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        verify_snapshot(policy_base, transition=False)
        verify_snapshot(candidate, transition=False)
    elif candidate_has_snapshot:
        if policy_base.tree_identity("docs/acquisition") != v4.v3.v2.v1.prior.prior.BASE_ACQUISITION_TREE:
            base.fail("source-admission trusted-base acquisition identity drifted")
        verify_snapshot(candidate, transition=True)


def _verify_extension_paths_v5(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled: frozenset[str],
) -> None:
    safe = _require_path_set(controlled, "extension-controlled-path")
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)
    bootstrap = _is_bootstrap_base(policy_base)

    if POLICY_SCRIPT in safe:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("S1 steady-state routing v5 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 steady-state routing v5 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 steady-state routing v5 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 steady-state routing v5 steady-state wrapper changed")

    delegated = frozenset(safe - {POLICY_SCRIPT})
    if delegated:
        v4._verify_extension_paths_v4(candidate, policy_base, delegated)


def _verify_desktop_extension_paths_v5(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v5(
        candidate,
        policy_base,
        _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension"),
    )


def _verify_execution_extension_paths_v5(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v5(
        candidate,
        policy_base,
        _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension"),
    )


def _validate_allowed_paths_v5(paths: set[str], stage: str) -> None:
    projected = {path for path in paths if path != POLICY_SCRIPT}
    original: Callable[[str], bool] = base.is_common_allowed

    def routed(path: str) -> bool:
        return original(path) or path == CANONICAL_PLAN_PATH

    base.is_common_allowed = routed
    try:
        v4._validate_allowed_paths_v4(projected, stage)
    finally:
        base.is_common_allowed = original


def _verify_policy_files_v5(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(V4_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V4_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 steady-state routing v4 predecessor policy drifted: "
            f"expected={EXPECTED_V4_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    v4._verify_policy_files_v4(view)


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("S1 steady-state routing v5 predecessor success printer is unavailable")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print("s1_admission_steady_state_route_v5=V4_PRESERVED_PLUS_EXACT_V2_3_CANONICALIZATION")
    print(f"s1_admission_authority_expansion_v5={AUTHORITY_EXPANSION}")
    print(f"effective_source_admission_v5={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission_v5={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution_v5={DONOR_EXECUTION}")
    print(f"effective_product_runtime_admission_v5={PRODUCT_RUNTIME_ADMISSION}")
    print(f"effective_model_provider_execution_v5={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access_v5={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference_v5={MODEL_INFERENCE}")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v4.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v4._install_policy()

    shell, retention, _, desktop, execution = _topology()
    expected = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, v4._require_exact_delta_v4, "exact-delta"),
        (base.compare_base_controlled, v4._compare_base_controlled_v4, "base-control"),
        (shell.validate_allowed_paths, v4._validate_allowed_paths_v4, "tracked-path"),
        (shell.verify_policy_files, v4._verify_policy_files_v4, "policy-file"),
        (
            desktop.verify_extension_controlled_paths,
            v4._verify_desktop_extension_paths_v4,
            "desktop-extension",
        ),
        (
            execution.verify_extension_controlled_paths,
            v4._verify_execution_extension_paths_v4,
            "execution-extension",
        ),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 steady-state routing v5 predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = shell.print_success
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(desktop.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(execution.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v5
    base.compare_base_controlled = _compare_base_controlled_v5
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v5
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v5
    shell.validate_allowed_paths = _validate_allowed_paths_v5
    shell.verify_policy_files = _verify_policy_files_v5
    shell.print_success = _print_success
    _INSTALLED = True


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in (FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW):
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                "S1 steady-state routing v5 workflow drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _selftest_authority() -> None:
    values = (
        SOURCE_ADMISSION,
        DEPENDENCY_ADMISSION,
        DONOR_EXECUTION,
        PRODUCT_RUNTIME_ADMISSION,
        MODEL_PROVIDER_EXECUTION,
        MODEL_WEIGHT_ACCESS,
        MODEL_INFERENCE,
        CANDIDATE_VERIFY_AUTHORITY,
    )
    if values != ("NONE",) * len(values):
        base.fail("S1 steady-state routing v5 prohibited authority boundary drifted")
    if AUTHORITY_EXPANSION != "V2_3_EXACT_TWO_FILE_CANONICALIZATION_ROUTE_ONLY":
        base.fail("S1 steady-state routing v5 canonicalization authority boundary drifted")
    if TRUSTED_BASE_V4_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":
        base.fail("S1 steady-state routing v5 old-base truth classification drifted")
    if CANDIDATE_POLICY_BASE_SOURCE != "LOCAL_FETCHED_GIT_WORKTREE":
        base.fail("S1 steady-state routing v5 candidate base-source contract drifted")


def _expect_policy_error(callable_obj: Callable[[], Any], label: str) -> None:
    try:
        callable_obj()
    except base.PolicyError:
        return
    base.fail(f"S1 steady-state routing v5 negative self-test did not fail: {label}")


def _selftest_bootstrap_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    local = base.LocalRepositoryView(root)
    base_files = {
        V4_POLICY_PATH: local.read_bytes(V4_POLICY_PATH, base.MAX_POLICY_FILE_BYTES),
        FOUNDATION_WORKFLOW: b"old-f",
        ADMISSION_WORKFLOW: b"old-a",
    }
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            POLICY_SCRIPT: b"policy-v5",
            FOUNDATION_WORKFLOW: b"new-f",
            ADMISSION_WORKFLOW: b"new-a",
        }
    )
    candidate = _memory_view(candidate_files)
    policy_base = _memory_view(base_files)
    _require_exact_delta_v5(candidate, policy_base)

    mixed = dict(candidate_files)
    mixed["README.md"] = b"unexpected"
    base.expect_failure_matching(
        "S1 routing v5 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v5,
        _memory_view(mixed),
        policy_base,
    )

    partial = dict(candidate_files)
    partial[ADMISSION_WORKFLOW] = base_files[ADMISSION_WORKFLOW]
    base.expect_failure_matching(
        "S1 routing v5 partial bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v5,
        _memory_view(partial),
        policy_base,
    )


def _selftest_canonicalization_contract() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    candidate = view.read_bytes(V2_3_CANDIDATE_PATH, base.MAX_POLICY_FILE_BYTES)
    index = view.read_bytes(MASTER_PLAN_INDEX, base.MAX_POLICY_FILE_BYTES)
    _require_blob(candidate, EXPECTED_V2_3_CANDIDATE_GIT_BLOB_SHA1, "self-test V2.3 candidate")
    _require_blob(index, EXPECTED_V2_2_INDEX_GIT_BLOB_SHA1, "self-test V2.2 index")

    canonical = _derive_canonical_plan(candidate)
    if canonical == candidate:
        base.fail("V2.3 canonicalization transform made no change")
    if not canonical.startswith(
        b"# WePLD Master Architecture & Execution Plan \xe2\x80\x94 V2.3 Agent Control Plane\n"
    ):
        base.fail("V2.3 canonicalization title transform drifted")
    if b"STATUS = CANONICAL\n" not in canonical:
        base.fail("V2.3 canonicalization status transform drifted")
    derived_index = _derive_index(canonical)
    if f"FULL_PLAN_SHA256 = {_sha256(canonical)}\n".encode("utf-8") not in derived_index:
        base.fail("V2.3 canonicalization index digest binding drifted")
    if f"CANONICAL_PLAN_PATH = {CANONICAL_PLAN_PATH}\n".encode("utf-8") not in derived_index:
        base.fail("V2.3 canonicalization index path binding drifted")
    if b"ROADMAP = P0 + S1..S10\n" not in derived_index:
        base.fail("V2.3 canonicalization roadmap preservation drifted")

    _expect_policy_error(
        lambda: _derive_canonical_plan(candidate + b"\n"),
        "candidate-byte mutation",
    )
    _expect_policy_error(
        lambda: _require_blob(index + b"\n", EXPECTED_V2_2_INDEX_GIT_BLOB_SHA1, "mutated index"),
        "index-byte mutation",
    )


def selftest() -> None:
    v4.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v4.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_authority()
    _selftest_bootstrap_contract()
    _selftest_canonicalization_contract()
    print("wepld S1 steady-state planning-route v5 policy self-tests: PASS")


def _candidate_parser(argv: list[str]) -> Any:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", required=True)
    parser.add_argument("--policy-base-root", required=True)
    parser.add_argument("--policy-base-sha", required=True)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0

        _install_policy()

        if argv and argv[0] == "verify-candidate-local":
            args = _candidate_parser(argv[1:])
            return v4.verify_candidate_local(
                args.root,
                args.policy_base_root,
                args.policy_base_sha,
            )

        return v4.main(argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
