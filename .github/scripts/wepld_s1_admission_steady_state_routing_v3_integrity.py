#!/usr/bin/env python3
"""Final steady-state S1 planning-route repair over the v2 bootstrap candidate.

This successor keeps the complete repository path set visible to the inherited
validators. It does not delete planning paths from validation. Instead, only the
bounded planning classes already defined by v2 are treated as common-allowed
paths for the duration of tracked-path validation, after which the original
predicate is restored.

It also provides a PR-candidate-only, non-authoritative verifier that compares
the exact local candidate against the exact remote trusted base directly. Push
activation remains on the inherited canonical activation runner.

No source, dependency, donor-execution, runtime, model, roadmap, Ready, merge,
or canonicalization authority is added.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Any, Callable

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_admission_steady_state_routing_v3_integrity.py"
V2_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v2_integrity.py"
V1_POLICY_PATH = ".github/scripts/wepld_s1_admission_steady_state_routing_v1_integrity.py"
EXPECTED_V2_POLICY_GIT_BLOB_SHA1 = "98d1be60afabe66ffb0e98b2f56e74ca9649efa6"
EXPECTED_V1_POLICY_GIT_BLOB_SHA1 = "d9f8c5778a728d9ddc5fa3339dfbf50eb7f45172"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "759c8cfbcba67f478b1e7b03c74cd13f7a9427b8ba31ae976c52cd00c896bd08",
    ADMISSION_WORKFLOW: "0d854d243ffe3e5301bfa8be4c25a847a641cff8cf9d1ebea9af69b6170ae224",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_DELTA_PATHS = frozenset(
    {
        V1_POLICY_PATH,
        V2_POLICY_PATH,
        POLICY_SCRIPT,
        FOUNDATION_WORKFLOW,
        ADMISSION_WORKFLOW,
    }
)

AUTHORITY_EXPANSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
DONOR_EXECUTION = "NONE"
PRODUCT_RUNTIME_ADMISSION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
V2_3_CANONICALIZATION = "NONE"
CANDIDATE_VERIFY_AUTHORITY = "NONE"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_predecessors_before_import() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    for path, expected in (
        (V2_POLICY_PATH, EXPECTED_V2_POLICY_GIT_BLOB_SHA1),
        (V1_POLICY_PATH, EXPECTED_V1_POLICY_GIT_BLOB_SHA1),
    ):
        actual = _git_blob_sha1(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                "frozen S1 steady-state predecessor drifted before import: "
                f"path={path} expected={expected} actual={actual}"
            )


_bind_predecessors_before_import()
import wepld_s1_admission_steady_state_routing_v2_integrity as v2  # noqa: E402


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    topology = v2._topology()
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("S1 steady-state routing v3 inherited topology is malformed")
    return topology


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"S1 steady-state routing v3 {label} topology is malformed")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"S1 steady-state routing v3 {label} contains non-string path")
    return frozenset(value)


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_candidate_predecessors(candidate: base.RepositoryView) -> None:
    for path, expected in (
        (V1_POLICY_PATH, EXPECTED_V1_POLICY_GIT_BLOB_SHA1),
        (V2_POLICY_PATH, EXPECTED_V2_POLICY_GIT_BLOB_SHA1),
    ):
        if path not in _paths(candidate):
            base.fail(f"S1 steady-state routing v3 bootstrap predecessor missing: {path}")
        actual = _git_blob_sha1(candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                "S1 steady-state routing v3 bootstrap predecessor drifted: "
                f"path={path} expected={expected} actual={actual}"
            )


def _require_exact_delta_v3(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, impl, _, _ = _topology()
    changed = _require_path_set(impl._changed_paths(candidate, policy_base), "changed-path")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_candidate_predecessors(candidate)
            v2.v1._require_prior_policy_base(policy_base)
            snapshot_present = v2.v1.prior.prior._snapshot_present
            if snapshot_present(candidate) and not snapshot_present(policy_base):
                base.fail("source snapshot cannot transition during S1 routing v3 bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "S1 steady-state routing v3 bootstrap delta must be exactly "
                "v1 + v2 + v3 policies plus two workflows"
            )

    v2._require_exact_delta_v2(candidate, policy_base)


def _verify_extension_paths_v3(
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
            base.fail("S1 steady-state routing v3 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("S1 steady-state routing v3 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("S1 steady-state routing v3 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("S1 steady-state routing v3 steady-state wrapper changed")

    delegated = frozenset(safe - {POLICY_SCRIPT})
    if delegated:
        v2._verify_extension_paths_v2(candidate, policy_base, delegated)


def _verify_desktop_extension_paths_v3(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v3(
        candidate,
        policy_base,
        _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension"),
    )


def _verify_execution_extension_paths_v3(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v3(
        candidate,
        policy_base,
        _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension"),
    )


def _validate_allowed_paths_v3(paths: set[str], stage: str) -> None:
    original: Callable[[str], bool] = base.is_common_allowed

    def routed(path: str) -> bool:
        return original(path) or v2._is_planning_path_v2(path)

    base.is_common_allowed = routed
    try:
        # Keep the full repository path set intact. v8/v7 remove only their
        # own frozen policy/source surfaces before reaching the inherited
        # stage validator; all canonical REQUIRED_PATHS remain visible.
        v2.v1.prior._validate_allowed_paths_v8(paths, stage)
    finally:
        base.is_common_allowed = original


def _verify_policy_files_v3(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(V2_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_V2_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1 steady-state routing v2 predecessor policy drifted: "
            f"expected={EXPECTED_V2_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    v2._verify_policy_files_v2(view)


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("S1 steady-state routing v3 predecessor success printer is unavailable")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print("s1_admission_steady_state_route_v3=FULL_PATH_PRESERVING_BOUNDED_PLANNING")
    print(f"s1_admission_authority_expansion_v3={AUTHORITY_EXPANSION}")
    print(f"effective_dependency_admission_v3={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_execution_v3={DONOR_EXECUTION}")
    print(f"effective_product_runtime_admission_v3={PRODUCT_RUNTIME_ADMISSION}")
    print(f"effective_model_provider_execution_v3={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access_v3={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference_v3={MODEL_INFERENCE}")
    print(f"v2_3_canonicalization_v3={V2_3_CANONICALIZATION}")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v2.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v2._install_policy()

    shell, retention, _, desktop, execution = _topology()
    expected = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, v2._require_exact_delta_v2, "exact-delta"),
        (base.compare_base_controlled, v2.v1._compare_base_controlled_v1, "base-control"),
        (shell.validate_allowed_paths, v2._validate_allowed_paths_v2, "tracked-path"),
        (shell.verify_policy_files, v2._verify_policy_files_v2, "policy-file"),
        (desktop.verify_extension_controlled_paths, v2._verify_desktop_extension_paths_v2, "desktop-extension"),
        (execution.verify_extension_controlled_paths, v2._verify_execution_extension_paths_v2, "execution-extension"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"S1 steady-state routing v3 predecessor {label} hook drifted")

    _PRIOR_PRINT_SUCCESS = shell.print_success
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(desktop.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(execution.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v3
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v3
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v3
    shell.validate_allowed_paths = _validate_allowed_paths_v3
    shell.verify_policy_files = _verify_policy_files_v3
    shell.print_success = _print_success
    _INSTALLED = True


def _verify_with_policy_base(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> str:
    shell, _, _, _, _ = _topology()
    verifier = shell.verify_view
    if not callable(verifier):
        base.fail("S1 steady-state routing v3 verify-view topology is not callable")
    stage = verifier(candidate, policy_base=policy_base)
    if not isinstance(stage, str):
        base.fail("S1 steady-state routing v3 verify-view returned non-string stage")
    return stage


def verify_candidate_local(root: str, policy_base_sha: str) -> int:
    policy_base_sha = base.require_comparison_sha(policy_base_sha).lower()
    token = os.environ.get("GITHUB_TOKEN") or None
    client = base.GitHubClient(token)
    candidate = base.LocalRepositoryView(Path(root))
    policy_base = base.RemoteRepositoryView(base.REPOSITORY, policy_base_sha, client)
    stage = _verify_with_policy_base(candidate, policy_base)
    print(f"candidate_policy_base_sha={policy_base_sha}")
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
                "S1 steady-state routing v3 workflow drifted: "
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
        base.fail("S1 steady-state routing v3 authority boundary drifted")


def selftest() -> None:
    v2.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    v2.selftest()
    _install_policy()
    _selftest_workflows()
    _selftest_authority()
    print("wepld S1 steady-state planning-route v3 policy self-tests: PASS")


def _candidate_parser(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", required=True)
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
            return verify_candidate_local(args.root, args.policy_base_sha)

        shell, retention, impl, _, _ = _topology()
        if argv and argv[0] == "verify-local":
            args = base.parse_args(argv)
            if args.remote_baseline:
                return v2.v1.prior._call_trusted_local_runner(args, shell, impl)

        runner = retention.main
        if not callable(runner):
            base.fail("S1 steady-state routing v3 runtime main is not callable")
        return runner(argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
