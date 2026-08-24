#!/usr/bin/env python3
"""Repair trusted-base S1 steady-state routing for planning-only PRs.

Canonical Pictorial/Agile source-admission v8 correctly preserves frozen source,
dependency, runtime, and model boundaries, but its inherited S1-011 transition
gate is still applied to unrelated post-S1 planning PRs. That makes every
documentation/specification-only candidate fail as though it were attempting
the old three-path S1-011 transition.

This successor adds one fail-closed steady-state route for planning-only
Markdown deltas while preserving every existing S1/source transition validator.
Mixed scopes, product/source/workflow/dependency changes, canonical authority
index changes, and unknown paths continue through the prior admission chain and
therefore remain closed unless an existing exact validator authorizes them.

No product, source, dependency, donor-execution, runtime, model, roadmap, merge,
or canonicalization authority is added.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v1_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_source_admission_v8_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "1101596adb075fad21340e482d8b152460121e49"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "9f4d321f4a5e8f37c3db31227157db61cf066e4acc4ea4513f12aae691f0067f",
    ADMISSION_WORKFLOW: "83c9e65e67d07fa0788d12d57937b37e18dec2249230575682d3ddd9132c675c",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "eb1f9e10706fd290f81f85fcc63590d287f42bec98f879464c76310b483fc405",
    ADMISSION_WORKFLOW: "8ced24cb3c5bb40e4da8ee842b268ff6d72c26c6dc2b368a4c69550ae3f1667d",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})

ROUTE = "PLANNING_DOCS_SPECS_STEADY_STATE_ONLY"
AUTHORITY_EXPANSION = "NONE"
SOURCE_ADMISSION = "UNCHANGED_EXACT_SOURCE_ONLY"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
PRODUCT_RUNTIME_ADMISSION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
V2_3_CANONICALIZATION = "NONE"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(files, trees={path: _git_blob_sha1(data) for path, data in files.items()})


def _bind_prior_policy_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile source-admission-v8 policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_source_admission_v8_integrity as prior  # noqa: E402


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    topology = prior._topology()
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("S1 steady-state routing inherited topology is malformed")
    return topology


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"S1 steady-state routing {label} topology is malformed")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"S1 steady-state routing {label} contains non-string path")
    return frozenset(value)


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail("S1 steady-state routing requires canonical Pictorial/Agile v8 predecessor")
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "S1 steady-state routing predecessor policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _is_planning_path(path: str) -> bool:
    if path == "docs/canonical/MASTER_PLAN_INDEX.md":
        return False
    if path.startswith("specs/") and path.endswith(".md"):
        return True
    if path.startswith("docs/acquisition/") and path.endswith(".md"):
        return True
    if path.startswith("docs/canonical/MASTER_PLAN_") and path.endswith("_CANDIDATE.md"):
        return True
    return False


def _validate_planning_delta(candidate: base.RepositoryView, changed: frozenset[str]) -> None:
    if not changed:
        base.fail("planning steady-state route requires a non-empty delta")
    unsafe = sorted(path for path in changed if not _is_planning_path(path))
    if unsafe:
        base.fail("planning steady-state route contains non-planning path(s): " + ", ".join(unsafe))

    entries = {entry.path: entry.mode for entry in candidate.entries()}
    for path in sorted(changed):
        mode = entries.get(path)
        if mode is None:
            base.fail(f"planning steady-state route does not authorize deletion: {path}")
        if mode != "100644":
            base.fail(f"planning steady-state route requires regular non-executable file: {path}")


def _require_exact_delta_v1(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, impl, _, _ = _topology()
    changed = _require_path_set(impl._changed_paths(candidate, policy_base), "changed-path")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            if prior.prior._snapshot_present(candidate) and not prior.prior._snapshot_present(policy_base):
                base.fail("source snapshot cannot transition during S1 routing bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 steady-state routing bootstrap delta must be exactly "
                "the successor policy plus two workflows"
            )
        prior._require_exact_delta_v8(candidate, policy_base)
        return

    if changed and all(_is_planning_path(path) for path in changed):
        _validate_planning_delta(candidate, changed)
        return

    prior._require_exact_delta_v8(candidate, policy_base)


def _compare_base_controlled_v1(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    controlled = _require_path_set(base.BASE_CONTROLLED_PATHS, "base-controlled-path")

    for relative in sorted(controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "S1 steady-state routing workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                base.fail(
                    "S1 steady-state routing trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"S1 steady-state routing steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    snapshot_present = prior.prior._snapshot_present
    verify_snapshot = prior.prior._verify_snapshot
    base_has_snapshot = snapshot_present(policy_base)
    candidate_has_snapshot = snapshot_present(candidate)
    if base_has_snapshot:
        if not candidate_has_snapshot:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        verify_snapshot(policy_base, transition=False)
        verify_snapshot(candidate, transition=False)
    elif candidate_has_snapshot:
        if policy_base.tree_identity("docs/acquisition") != prior.prior.BASE_ACQUISITION_TREE:
            base.fail("source-admission trusted-base acquisition identity drifted")
        verify_snapshot(candidate, transition=True)


def _verify_extension_paths_v1(candidate: base.RepositoryView, policy_base: base.RepositoryView, controlled: frozenset[str]) -> None:
    safe = _require_path_set(controlled, "extension-controlled-path")
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in safe:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("S1 steady-state routing policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 steady-state routing wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 steady-state routing steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 steady-state routing steady-state wrapper changed")

    delegated = frozenset(safe - {POLICY_SCRIPT})
    if delegated:
        prior._verify_extension_paths_v8(candidate, policy_base, delegated)


def _verify_desktop_extension_paths_v1(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v1(
        candidate,
        policy_base,
        _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension"),
    )


def _verify_execution_extension_paths_v1(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v1(
        candidate,
        policy_base,
        _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension"),
    )


def _validate_allowed_paths_v1(paths: set[str], stage: str) -> None:
    projected = {path for path in paths if path != POLICY_SCRIPT and not _is_planning_path(path)}
    prior._validate_allowed_paths_v8(projected, stage)


def _verify_policy_files_v1(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile source-admission-v8 predecessor policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._verify_policy_files_v8(view)


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("S1 steady-state routing predecessor success printer is unavailable")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"s1_admission_steady_state_route={ROUTE}")
    print(f"s1_admission_authority_expansion={AUTHORITY_EXPANSION}")
    print(f"effective_source_admission={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution={DONOR_EXECUTION}")
    print(f"effective_product_runtime_admission={PRODUCT_RUNTIME_ADMISSION}")
    print(f"effective_model_provider_execution={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference={MODEL_INFERENCE}")
    print(f"v2_3_canonicalization={V2_3_CANONICALIZATION}")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior._install_policy()

    shell, retention, _, desktop, execution = _topology()
    expected_hooks = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, prior._require_exact_delta_v8, "exact-delta"),
        (base.compare_base_controlled, prior._compare_base_controlled_v8, "base-control"),
        (shell.validate_allowed_paths, prior._validate_allowed_paths_v8, "tracked-path"),
        (shell.verify_policy_files, prior._verify_policy_files_v8, "policy-file"),
        (desktop.verify_extension_controlled_paths, prior._verify_desktop_extension_paths_v8, "desktop-extension"),
        (execution.verify_extension_controlled_paths, prior._verify_execution_extension_paths_v8, "execution-extension"),
    )
    for actual, wanted, label in expected_hooks:
        if actual is not wanted:
            base.fail(f"S1 steady-state routing predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = shell.print_success
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(set(desktop.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT})
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(set(execution.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT})
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v1
    base.compare_base_controlled = _compare_base_controlled_v1
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v1
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v1
    shell.validate_allowed_paths = _validate_allowed_paths_v1
    shell.verify_policy_files = _verify_policy_files_v1
    shell.print_success = _print_success
    _INSTALLED = True


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                "S1 steady-state routing workflow drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _selftest_path_routing() -> None:
    allowed = (
        "specs/003-agent-control-plane-architecture-enrichment/spec.md",
        "specs/003-agent-control-plane-architecture-enrichment/checklists/requirements.md",
        "docs/acquisition/WEPLD_AGENT_CONTROL_PLANE_MAJOR_RECONNAISSANCE_2026-08-24.md",
        "docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE_CANDIDATE.md",
    )
    for path in allowed:
        if not _is_planning_path(path):
            base.fail(f"planning route failed to classify allowed path: {path}")

    rejected = (
        "docs/canonical/MASTER_PLAN_INDEX.md",
        "docs/canonical/MASTER_PLAN_V2_2.md",
        "specs/003-agent-control-plane-architecture-enrichment/tool.py",
        ".github/workflows/foundation-integrity.yml",
        "vendor/pictorial/src/index.ts",
    )
    for path in rejected:
        if _is_planning_path(path):
            base.fail(f"planning route misclassified forbidden path: {path}")


def _selftest_bootstrap_delta() -> None:
    base_files = {
        PRIOR_POLICY_PATH: Path(__file__).resolve().with_name(
            "wepld_pictorial_agile_source_admission_v8_integrity.py"
        ).read_bytes(),
        FOUNDATION_WORKFLOW: b"old-f",
        ADMISSION_WORKFLOW: b"old-a",
    }
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            POLICY_SCRIPT: b"policy",
            FOUNDATION_WORKFLOW: b"new-f",
            ADMISSION_WORKFLOW: b"new-a",
        }
    )
    candidate = _memory_view(candidate_files)
    policy_base = _memory_view(base_files)
    _require_exact_delta_v1(candidate, policy_base)

    candidate_files["README.md"] = b"mixed"
    base.expect_failure_matching(
        "S1 routing mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v1,
        _memory_view(candidate_files),
        policy_base,
    )


def _selftest_steady_planning_delta() -> None:
    common = {
        POLICY_SCRIPT: b"policy",
        FOUNDATION_WORKFLOW: b"new-f",
        ADMISSION_WORKFLOW: b"new-a",
        "README.md": b"base",
    }
    policy_base = _memory_view(dict(common))
    candidate_files = dict(common)
    candidate_files["specs/003-agent-control-plane-architecture-enrichment/spec.md"] = b"# spec\n"
    candidate = _memory_view(candidate_files)
    _require_exact_delta_v1(candidate, policy_base)

    mixed_files = dict(candidate_files)
    mixed_files["README.md"] = b"changed"
    changed = _require_path_set(
        _topology()[2]._changed_paths(_memory_view(mixed_files), policy_base),
        "mixed-selftest",
    )
    if changed and all(_is_planning_path(path) for path in changed):
        base.fail("mixed planning/product delta was incorrectly eligible for planning route")


def _selftest_authority() -> None:
    if (
        AUTHORITY_EXPANSION,
        DEPENDENCY_ADMISSION,
        DONOR_EXECUTION,
        PRODUCT_RUNTIME_ADMISSION,
        MODEL_PROVIDER_EXECUTION,
        MODEL_WEIGHT_ACCESS,
        MODEL_INFERENCE,
        V2_3_CANONICALIZATION,
    ) != ("NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"):
        base.fail("S1 steady-state routing authority boundary drifted")


def selftest() -> None:
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior.selftest()
    _selftest_path_routing()
    _selftest_bootstrap_delta()
    _install_policy()
    _selftest_workflows()
    _selftest_steady_planning_delta()
    _selftest_authority()
    print("wepld S1 steady-state planning-route policy self-tests: PASS")


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0

        _install_policy()
        shell, retention, impl, _, _ = _topology()

        if argv and argv[0] == "verify-local":
            args = base.parse_args(argv)
            if args.remote_baseline:
                return prior._call_trusted_local_runner(args, shell, impl)

        runner = retention.main
        if not callable(runner):
            base.fail("S1 steady-state routing runtime main is not callable")
        return runner(argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
