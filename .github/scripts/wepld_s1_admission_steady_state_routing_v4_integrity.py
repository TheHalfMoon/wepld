#!/usr/bin/env python3
"""Eliminate candidate-side GitHub API dependency from S1 planning verification.

v3 removed bearer-token exposure from candidate-controlled pull-request code, but
its non-authoritative Foundation verifier still built the trusted-base view
through unauthenticated GitHub API calls. That made deterministic qualification
dependent on public API rate limits.

v4 keeps the token-isolation security property and removes that availability
dependency. Foundation already checks out full canonical history with
``fetch-depth: 0``; it now materializes the exact pull-request base as a detached
local Git worktree and supplies that worktree to candidate verification.

The authoritative ``pull_request_target`` path is unchanged in trust model: it
executes policy from the trusted base and inspects candidate Git objects as data
through the GitHub API using the trusted read-only workflow token.

No source, dependency, donor-execution, runtime, model, roadmap, Ready, merge, or
V2.3 canonicalization authority is added.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v4_integrity.py"
V3_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v3_integrity.py"
EXPECTED_V3_POLICY_GIT_BLOB_SHA1 = "f5aeed2584f721b954d827083825787c9c3e28d0"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "759c8cfbcba67f478b1e7b03c74cd13f7a9427b8ba31ae976c52cd00c896bd08",
    ADMISSION_WORKFLOW: "0d854d243ffe3e5301bfa8be4c25a847a641cff8cf9d1ebea9af69b6170ae224",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "96e56fad757c73d4d960e6dfcc17912aebe5d28669e46ef6cf740d3936edc937",
    ADMISSION_WORKFLOW: "bf36b9b2552c0ad32a4c321c496c9ddabe0f353934ff537b82f766a5133f90be",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})

AUTHORITY_EXPANSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
PRODUCT_RUNTIME_ADMISSION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
V2_3_CANONICALIZATION = "NONE"
CANDIDATE_VERIFY_AUTHORITY = "NONE"
CANDIDATE_POLICY_BASE_SOURCE = "LOCAL_FETCHED_GIT_WORKTREE"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_v3_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(V3_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V3_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 steady-state routing v3 predecessor drifted before import: "
            f"expected={EXPECTED_V3_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_v3_before_import()
import wepld_s1_admission_steady_state_routing_v3_integrity as v3  # noqa: E402


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    topology = v3._topology()
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("S1 steady-state routing v4 inherited topology is malformed")
    return topology


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"S1 steady-state routing v4 {label} topology is malformed")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"S1 steady-state routing v4 {label} contains non-string path")
    return frozenset(value)


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_v3_candidate(candidate: base.RepositoryView) -> None:
    if V3_POLICY_PATH not in _paths(candidate):
        base.fail("S1 steady-state routing v4 bootstrap requires frozen v3 predecessor")
    actual = _git_blob_sha1(candidate.read_bytes(V3_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V3_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "S1 steady-state routing v3 candidate policy drifted: "
            f"expected={EXPECTED_V3_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _require_exact_delta_v4(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, impl, _, _ = _topology()
    changed = _require_path_set(impl._changed_paths(candidate, policy_base), "changed-path")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_v3_candidate(candidate)
            actual_base_v3 = _git_blob_sha1(
                policy_base.read_bytes(V3_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
            )
            if actual_base_v3 != EXPECTED_V3_POLICY_GIT_BLOB_SHA1:
                base.fail(
                    "S1 steady-state routing v4 trusted-base v3 predecessor drifted: "
                    f"expected={EXPECTED_V3_POLICY_GIT_BLOB_SHA1} actual={actual_base_v3}"
                )
            snapshot_present = v3.v2.v1.prior.prior._snapshot_present
            if snapshot_present(candidate) and not snapshot_present(policy_base):
                base.fail("source snapshot cannot transition during S1 routing v4 bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 steady-state routing v4 bootstrap delta must be exactly "
                "the v4 policy plus Foundation and admission workflows"
            )

    v3._require_exact_delta_v3(candidate, policy_base)


def _compare_base_controlled_v4(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
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
                    "S1 steady-state routing v4 workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
                if bootstrap
                else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                base.fail(
                    "S1 steady-state routing v4 trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"S1 steady-state routing v4 steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    snapshot_present = v3.v2.v1.prior.prior._snapshot_present
    verify_snapshot = v3.v2.v1.prior.prior._verify_snapshot
    base_has_snapshot = snapshot_present(policy_base)
    candidate_has_snapshot = snapshot_present(candidate)
    if base_has_snapshot:
        if not candidate_has_snapshot:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        verify_snapshot(policy_base, transition=False)
        verify_snapshot(candidate, transition=False)
    elif candidate_has_snapshot:
        if policy_base.tree_identity("docs/acquisition") != v3.v2.v1.prior.prior.BASE_ACQUISITION_TREE:
            base.fail("source-admission trusted-base acquisition identity drifted")
        verify_snapshot(candidate, transition=True)


def _verify_extension_paths_v4(
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
            base.fail("S1 steady-state routing v4 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 steady-state routing v4 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 steady-state routing v4 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 steady-state routing v4 steady-state wrapper changed")

    delegated = frozenset(safe - {POLICY_SCRIPT})
    if delegated:
        v3._verify_extension_paths_v3(candidate, policy_base, delegated)


def _verify_desktop_extension_paths_v4(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v4(
        candidate,
        policy_base,
        _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension"),
    )


def _verify_execution_extension_paths_v4(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v4(
        candidate,
        policy_base,
        _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension"),
    )


def _validate_allowed_paths_v4(paths: set[str], stage: str) -> None:
    projected = {path for path in paths if path != POLICY_SCRIPT}
    v3._validate_allowed_paths_v3(projected, stage)


def _verify_policy_files_v4(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(V3_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V3_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 steady-state routing v3 predecessor policy drifted: "
            f"expected={EXPECTED_V3_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    v3._verify_policy_files_v3(view)


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("S1 steady-state routing v4 predecessor success printer is unavailable")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print("s1_admission_steady_state_route_v4=LOCAL_BASE_VIEW_NO_CANDIDATE_TOKEN")
    print(f"s1_admission_authority_expansion_v4={AUTHORITY_EXPANSION}")
    print(f"effective_dependency_admission_v4={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution_v4={DONOR_EXECUTION}")
    print(f"effective_product_runtime_admission_v4={PRODUCT_RUNTIME_ADMISSION}")
    print(f"effective_model_provider_execution_v4={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access_v4={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference_v4={MODEL_INFERENCE}")
    print(f"v2_3_canonicalization_v4={V2_3_CANONICALIZATION}")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v3.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v3._install_policy()

    shell, retention, _, desktop, execution = _topology()
    expected = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, v3._require_exact_delta_v3, "exact-delta"),
        (base.compare_base_controlled, v3.v2.v1._compare_base_controlled_v1, "base-control"),
        (shell.validate_allowed_paths, v3._validate_allowed_paths_v3, "tracked-path"),
        (shell.verify_policy_files, v3._verify_policy_files_v3, "policy-file"),
        (desktop.verify_extension_controlled_paths, v3._verify_desktop_extension_paths_v3, "desktop-extension"),
        (execution.verify_extension_controlled_paths, v3._verify_execution_extension_paths_v3, "execution-extension"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 steady-state routing v4 predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = shell.print_success
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(desktop.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(execution.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v4
    base.compare_base_controlled = _compare_base_controlled_v4
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v4
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v4
    shell.validate_allowed_paths = _validate_allowed_paths_v4
    shell.verify_policy_files = _verify_policy_files_v4
    shell.print_success = _print_success
    _INSTALLED = True


def _git_head(root: Path) -> str:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--verify", "HEAD"],
            stderr=subprocess.STDOUT,
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        output = exc.output.strip()
        base.fail(f"unable to resolve local policy-base HEAD: {output}")
    if not base.OBJECT_SHA_RE.fullmatch(raw):
        base.fail(f"local policy-base HEAD is malformed: {raw!r}")
    return raw.lower()


def _require_clean(root: Path, label: str) -> None:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
            stderr=subprocess.STDOUT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        output = exc.output.strip()
        base.fail(f"unable to inspect {label} worktree cleanliness: {output}")
    if raw:
        base.fail(f"{label} worktree is not clean")


def verify_candidate_local(
    root: str,
    policy_base_root: str,
    policy_base_sha: str,
) -> int:
    policy_base_sha = base.require_comparison_sha(policy_base_sha).lower()
    if os.environ.get("GITHUB_TOKEN"):
        base.fail("candidate-local verifier refuses a token-bearing environment")

    candidate_root = Path(root).resolve()
    trusted_root = Path(policy_base_root).resolve()
    if candidate_root == trusted_root:
        base.fail("candidate and policy-base worktrees must be distinct")

    actual_base_sha = _git_head(trusted_root)
    if actual_base_sha != policy_base_sha:
        base.fail(
            "local policy-base worktree identity mismatch: "
            f"expected={policy_base_sha} actual={actual_base_sha}"
        )

    _require_clean(candidate_root, "candidate")
    _require_clean(trusted_root, "policy-base")

    candidate = base.LocalRepositoryView(candidate_root)
    policy_base = base.LocalRepositoryView(trusted_root)
    stage = v3._verify_with_policy_base(candidate, policy_base)

    print(f"candidate_policy_base_sha={policy_base_sha}")
    print(f"candidate_policy_base_source={CANDIDATE_POLICY_BASE_SOURCE}")
    print(f"candidate_stage={stage}")
    print(f"candidate_policy_authority={CANDIDATE_VERIFY_AUTHORITY}")
    print("candidate_bootstrap_verification=PASS")
    return 0


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in (FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW):
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                "S1 steady-state routing v4 workflow drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _selftest_authority() -> None:
    values = (
        AUTHORITY_EXPANSION,
        DEPENDENCY_ADMISSION,
        DONOR_EXECUTION,
        PRODUCT_RUNTIME_ADMISSION,
        MODEL_PROVIDER_EXECUTION,
        MODEL_WEIGHT_ACCESS,
        MODEL_INFERENCE,
        V2_3_CANONICALIZATION,
        CANDIDATE_VERIFY_AUTHORITY,
    )
    if values != ("NONE",) * len(values):
        base.fail("S1 steady-state routing v4 authority boundary drifted")
    if CANDIDATE_POLICY_BASE_SOURCE != "LOCAL_FETCHED_GIT_WORKTREE":
        base.fail("S1 steady-state routing v4 candidate base-source contract drifted")


def selftest() -> None:
    v3.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v3.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_authority()
    print("wepld S1 steady-state planning-route v4 policy self-tests: PASS")


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
            return verify_candidate_local(
                args.root,
                args.policy_base_root,
                args.policy_base_sha,
            )

        return v3.main(argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
