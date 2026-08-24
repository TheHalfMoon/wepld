#!/usr/bin/env python3
"""Harden the S1 steady-state planning route and prove successor bootstrap.

v1 repaired the structural defect where post-S1 planning PRs were forced through
the already-completed S1-011 three-path transition. This successor narrows the
planning route so acquisition contracts or other broad Markdown surfaces cannot
accidentally inherit that route, and adds candidate-side bootstrap verification
through Foundation.

Only three planning classes are eligible in steady state:
1. Markdown files inside a numbered Spec Kit package under ``specs/``;
2. dated ``WEPLD_*_RECONNAISSANCE_YYYY-MM-DD.md`` acquisition reports; and
3. non-canonical ``MASTER_PLAN_*_CANDIDATE.md`` documents.

Everything else, including canonical indexes/plans, contracts, evidence files,
workflows, product/source/dependency/runtime files, mixed scopes, deletions, and
executable modes, delegates to the predecessor admission chain and remains fail
closed unless an existing exact validator authorizes it.

No source, dependency, donor-execution, runtime, model, roadmap, merge, Ready,
or canonicalization authority is added.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v2_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v1_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "d9f8c5778a728d9ddc5fa3339dfbf50eb7f45172"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "eb1f9e10706fd290f81f85fcc63590d287f42bec98f879464c76310b483fc405",
    ADMISSION_WORKFLOW: "8ced24cb3c5bb40e4da8ee842b268ff6d72c26c6dc2b368a4c69550ae3f1667d",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "dfd1186a6e8d69bb1a35b30d6a48a4a81451ed51d3d7934aa45027879a8c5b40",
    ADMISSION_WORKFLOW: "80d5fb2c7305377328c43ff3da15882f690bdf6c9c5f16b9455d0141a20e9b86",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {PRIOR_POLICY_PATH, POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

SPEC_MARKDOWN_RE = re.compile(
    r"^specs/[0-9]{3}-[a-z0-9-]+/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.md$"
)
RECONNAISSANCE_RE = re.compile(
    r"^docs/acquisition/WEPLD_[A-Z0-9_]+_RECONNAISSANCE_[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$"
)
CANDIDATE_PLAN_RE = re.compile(
    r"^docs/canonical/MASTER_PLAN_V[A-Z0-9_]+_CANDIDATE\.md$"
)

ROUTE = "BOUNDED_PLANNING_PACKAGE_STEADY_STATE_ONLY"
AUTHORITY_EXPANSION = "NONE"
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
            "frozen S1 steady-state routing v1 policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_s1_admission_steady_state_routing_v1_integrity as v1  # noqa: E402


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    topology = v1._topology()
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("S1 steady-state routing v2 inherited topology is malformed")
    return topology


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"S1 steady-state routing v2 {label} topology is malformed")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"S1 steady-state routing v2 {label} contains non-string path")
    return frozenset(value)


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _is_planning_path_v2(path: str) -> bool:
    return bool(
        SPEC_MARKDOWN_RE.fullmatch(path)
        or RECONNAISSANCE_RE.fullmatch(path)
        or CANDIDATE_PLAN_RE.fullmatch(path)
    )


def _require_v1_candidate(candidate: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(candidate):
        base.fail("S1 steady-state routing v2 bootstrap requires frozen v1 predecessor")
    actual = _git_blob_sha1(candidate.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "S1 steady-state routing v1 candidate policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_exact_delta_v2(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, impl, _, _ = _topology()
    changed = _require_path_set(impl._changed_paths(candidate, policy_base), "changed-path")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_v1_candidate(candidate)
            v1._require_prior_policy_base(policy_base)
            snapshot_present = v1.prior.prior._snapshot_present
            if snapshot_present(candidate) and not snapshot_present(policy_base):
                base.fail("source snapshot cannot transition during S1 routing v2 bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 steady-state routing v2 bootstrap delta must be exactly "
                "v1 + v2 successor policies plus two workflows"
            )
        v1._require_exact_delta_v1(candidate, policy_base)
        return

    if changed and all(_is_planning_path_v2(path) for path in changed):
        v1._validate_planning_delta(candidate, changed)
        return

    v1._require_exact_delta_v1(candidate, policy_base)


def _verify_extension_paths_v2(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled: frozenset[str],
) -> None:
    safe = _require_path_set(controlled, "extension-controlled-path")
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in safe:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("S1 steady-state routing v2 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 steady-state routing v2 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 steady-state routing v2 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 steady-state routing v2 steady-state wrapper changed")

    delegated = frozenset(safe - {POLICY_SCRIPT})
    if delegated:
        v1._verify_extension_paths_v1(candidate, policy_base, delegated)


def _verify_desktop_extension_paths_v2(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v2(
        candidate,
        policy_base,
        _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension"),
    )


def _verify_execution_extension_paths_v2(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v2(
        candidate,
        policy_base,
        _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension"),
    )


def _validate_allowed_paths_v2(paths: set[str], stage: str) -> None:
    projected = {path for path in paths if path != POLICY_SCRIPT}
    v1._validate_allowed_paths_v1(projected, stage)


def _verify_policy_files_v2(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 steady-state routing v1 predecessor policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    v1._verify_policy_files_v1(view)


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("S1 steady-state routing v2 predecessor success printer is unavailable")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"s1_admission_steady_state_route_v2={ROUTE}")
    print(f"s1_admission_authority_expansion_v2={AUTHORITY_EXPANSION}")
    print(f"effective_dependency_admission_v2={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution_v2={DONOR_EXECUTION}")
    print(f"effective_product_runtime_admission_v2={PRODUCT_RUNTIME_ADMISSION}")
    print(f"effective_model_provider_execution_v2={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access_v2={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference_v2={MODEL_INFERENCE}")
    print(f"v2_3_canonicalization_v2={V2_3_CANONICALIZATION}")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v1.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v1._install_policy()

    # Tighten both the exact-delta route and v1's repository-path projection.
    v1._is_planning_path = _is_planning_path_v2

    shell, retention, _, desktop, execution = _topology()
    expected_hooks = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, v1._require_exact_delta_v1, "exact-delta"),
        (base.compare_base_controlled, v1._compare_base_controlled_v1, "base-control"),
        (shell.validate_allowed_paths, v1._validate_allowed_paths_v1, "tracked-path"),
        (shell.verify_policy_files, v1._verify_policy_files_v1, "policy-file"),
        (desktop.verify_extension_controlled_paths, v1._verify_desktop_extension_paths_v1, "desktop-extension"),
        (execution.verify_extension_controlled_paths, v1._verify_execution_extension_paths_v1, "execution-extension"),
    )
    for actual, wanted, label in expected_hooks:
        if actual is not wanted:
            base.fail(f"S1 steady-state routing v2 predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = shell.print_success
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(desktop.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(execution.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v2
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v2
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v2
    shell.validate_allowed_paths = _validate_allowed_paths_v2
    shell.verify_policy_files = _verify_policy_files_v2
    shell.print_success = _print_success
    _INSTALLED = True


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                "S1 steady-state routing v2 workflow drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _selftest_tight_routing() -> None:
    allowed = (
        "specs/003-agent-control-plane-architecture-enrichment/spec.md",
        "specs/003-agent-control-plane-architecture-enrichment/checklists/requirements.md",
        "docs/acquisition/WEPLD_AGENT_CONTROL_PLANE_MAJOR_RECONNAISSANCE_2026-08-24.md",
        "docs/acquisition/WEPLD_TRAE_AGENT_RECONNAISSANCE_2026-08-24.md",
        "docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE_CANDIDATE.md",
    )
    for path in allowed:
        if not _is_planning_path_v2(path):
            base.fail(f"S1 routing v2 failed to classify allowed planning path: {path}")

    rejected = (
        "docs/canonical/MASTER_PLAN_INDEX.md",
        "docs/canonical/MASTER_PLAN_V2_2.md",
        "docs/acquisition/WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md",
        "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_REPORT_2026-08-23.md",
        "specs/003-agent-control-plane-architecture-enrichment/tool.py",
        ".github/workflows/foundation-integrity.yml",
        "vendor/pictorial/src/index.ts",
    )
    for path in rejected:
        if _is_planning_path_v2(path):
            base.fail(f"S1 routing v2 misclassified forbidden path: {path}")


def _selftest_bootstrap_delta() -> None:
    root = Path(__file__).resolve().parents[2]
    local = base.LocalRepositoryView(root)
    v8_path = v1.PRIOR_POLICY_PATH
    base_files = {
        v8_path: local.read_bytes(v8_path, base.MAX_POLICY_FILE_BYTES),
        FOUNDATION_WORKFLOW: b"old-f",
        ADMISSION_WORKFLOW: b"old-a",
    }
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            PRIOR_POLICY_PATH: local.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES),
            POLICY_SCRIPT: b"policy-v2",
            FOUNDATION_WORKFLOW: b"new-f",
            ADMISSION_WORKFLOW: b"new-a",
        }
    )
    candidate = _memory_view(candidate_files)
    policy_base = _memory_view(base_files)
    _require_exact_delta_v2(candidate, policy_base)

    mixed = dict(candidate_files)
    mixed["README.md"] = b"unexpected"
    base.expect_failure_matching(
        "S1 routing v2 mixed bootstrap rejection",
        "bootstrap delta must be exactly",
        _require_exact_delta_v2,
        _memory_view(mixed),
        policy_base,
    )


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
        base.fail("S1 steady-state routing v2 authority boundary drifted")


def selftest() -> None:
    v1.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v1.selftest()
    _selftest_tight_routing()
    _selftest_bootstrap_delta()
    _install_policy()
    _selftest_workflows()
    _selftest_authority()
    print("wepld S1 steady-state planning-route v2 policy self-tests: PASS")


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
                return v1.prior._call_trusted_local_runner(args, shell, impl)

        runner = retention.main
        if not callable(runner):
            base.fail("S1 steady-state routing v2 runtime main is not callable")
        return runner(argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
