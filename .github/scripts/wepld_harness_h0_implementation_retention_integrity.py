#!/usr/bin/env python3
"""H0-012 Repair-1: enforce monotonic retention of canonical H0 implementation paths.

This wrapper layers one fail-closed repair over the exact H0-011 implementation
integrity policy candidate. It preserves the H0-010 dependency and authority
boundaries while preventing any already-canonical `research/harness_h0/` path
from being deleted by a later candidate.

The wrapper itself grants no implementation authority until H0-012 has
qualified, merged, and activation-proven this exact bootstrap.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_harness_h0_implementation_retention_integrity.py"
IMPLEMENTATION_POLICY_PATH = ".github/scripts/wepld_harness_h0_implementation_integrity.py"
EXPECTED_IMPLEMENTATION_POLICY_GIT_BLOB_SHA1 = "b5c79744f54227292c447427fa43e7413a58f4c6"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "814ba290b91db185e15147ac10c1c2db301fb56bdd208f4c9cc0998fe895d6c7",
    ADMISSION_WORKFLOW: "c361695482ad1986aefd5c49c3b571f104c64ea8bd3208cd98cfa985655f979a",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

H0_012_REPAIR = "MONOTONIC_CANONICAL_H0_PATH_RETENTION"
H0_SCREEN_IMPLEMENTATION_AUTHORIZED = "NO_UNTIL_H0_012_CANONICAL_ACTIVATION"
PRODUCT_HARNESS_INTEGRATION = "NO"
H0_CONFIRMATORY_EXECUTION = "NO"
HARBOR_ADMISSION = "NONE"
ROADMAP_MUTATION = "NONE"
S1_013_PLUS = "NOT_STARTED"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_implementation_policy_before_import() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    data = view.read_bytes(IMPLEMENTATION_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_IMPLEMENTATION_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0-011 implementation policy runner drifted: "
            f"expected={EXPECTED_IMPLEMENTATION_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_implementation_policy_before_import()
import wepld_harness_h0_implementation_integrity as impl  # noqa: E402

shell = impl.shell
IMPL_REQUIRE_EXACT_DELTA = impl._require_exact_delta_h0_implementation

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {
        IMPLEMENTATION_POLICY_PATH,
        POLICY_SCRIPT,
        FOUNDATION_WORKFLOW,
        ADMISSION_WORKFLOW,
    }
)


def _activate_retention_contract() -> None:
    impl.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)


def _verify_policy_files(view: base.RepositoryView) -> None:
    data = view.read_bytes(IMPLEMENTATION_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_IMPLEMENTATION_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0-011 implementation policy drifted in repository view: "
            f"expected={EXPECTED_IMPLEMENTATION_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    impl._verify_policy_files(view)


def _require_monotonic_h0_retention(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    base_h0_paths = {
        path
        for path in _paths(policy_base)
        if path.startswith(impl.IMPLEMENTATION_ROOT)
    }
    candidate_h0_paths = {
        path
        for path in _paths(candidate)
        if path.startswith(impl.IMPLEMENTATION_ROOT)
    }
    removed = sorted(base_h0_paths - candidate_h0_paths)
    if removed:
        base.fail(
            "canonical H0 implementation paths cannot be removed: "
            + ",".join(removed)
        )


def _require_exact_delta_retention(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = impl._changed_paths(candidate, policy_base)
    bootstrap = impl._is_bootstrap_base(policy_base)

    if bootstrap:
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            impl._require_canonical_h0_010_base(policy_base)
            return
        if any(path.startswith(impl.IMPLEMENTATION_ROOT) for path in changed):
            base.fail("H0 implementation cannot transition before H0-012 policy activation")
        impl.PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    _require_monotonic_h0_retention(candidate, policy_base)
    IMPL_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _verify_extension_paths_retention(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = impl._is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("H0 retention policy wrapper is missing from candidate")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("H0 retention wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("H0 retention steady-state base is missing wrapper")
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("H0 retention steady-state policy wrapper changed")

    delegated = frozenset(set(controlled_paths) - {POLICY_SCRIPT})
    if delegated:
        impl._verify_extension_paths_h0_implementation(
            candidate,
            policy_base,
            delegated,
        )


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_retention(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_retention(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior H0 implementation success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"h0_012_repair={H0_012_REPAIR}")
    print("canonical_h0_path_retention=MONOTONIC_FAIL_CLOSED")
    print(
        "h0_screen_implementation_authorized="
        f"{H0_SCREEN_IMPLEMENTATION_AUTHORIZED}"
    )
    print(f"product_harness_integration={PRODUCT_HARNESS_INTEGRATION}")
    print(f"h0_confirmatory_execution={H0_CONFIRMATORY_EXECUTION}")
    print(f"harbor_admission={HARBOR_ADMISSION}")
    print(f"harness_roadmap_mutation={ROADMAP_MUTATION}")
    print(f"s1_013_plus={S1_013_PLUS}")


def _install_retention_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    _activate_retention_contract()
    impl._install_h0_implementation_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    impl.prior.prior.prior.prior.prior.prior.v24.v19._require_exact_delta = (
        _require_exact_delta_retention
    )

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.verify_extension_controlled_paths = _verify_desktop_extension_paths
    shell.prior.prior.verify_extension_controlled_paths = _verify_execution_extension_paths

    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success
    _INSTALLED = True


def _selftest_workflow_binding() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for relative in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "H0 retention policy workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_bootstrap_delta() -> None:
    base_files = impl._fixture_canonical_base()
    base_files[FOUNDATION_WORKFLOW] = b"prior-foundation"
    base_files[ADMISSION_WORKFLOW] = b"prior-admission"

    candidate_files = dict(base_files)
    candidate_files[IMPLEMENTATION_POLICY_PATH] = b"h0-implementation-policy"
    candidate_files[POLICY_SCRIPT] = b"h0-retention-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"new-admission"
    trees = {
        IMPLEMENTATION_POLICY_PATH: "1" * 40,
        POLICY_SCRIPT: "2" * 40,
        FOUNDATION_WORKFLOW: "3" * 40,
        ADMISSION_WORKFLOW: "4" * 40,
    }
    _require_exact_delta_retention(
        base.MemoryView(candidate_files, trees=trees),
        base.MemoryView(base_files),
    )


def _selftest_monotonic_retention() -> None:
    hard_gate = impl.IMPLEMENTATION_ROOT + "tests/hard_gates.rs"
    base_files = {
        IMPLEMENTATION_POLICY_PATH: b"canonical-implementation-policy",
        POLICY_SCRIPT: b"canonical-retention-policy",
        impl.CARGO_TOML_PATH: b"canonical-cargo",
        impl.IMPLEMENTATION_ROOT + "src/manifests.rs": b"canonical-manifests",
        impl.IMPLEMENTATION_ROOT + "src/evidence.rs": b"canonical-evidence",
        impl.IMPLEMENTATION_ROOT + "src/recipe.rs": b"canonical-recipe",
        hard_gate: b"canonical-hard-gate",
    }
    candidate_files = dict(base_files)
    del candidate_files[hard_gate]

    base.expect_failure_matching(
        "H0 canonical path deletion",
        "canonical H0 implementation paths cannot be removed",
        _require_exact_delta_retention,
        base.MemoryView(candidate_files),
        base.MemoryView(base_files),
    )

    _require_monotonic_h0_retention(
        base.MemoryView(base_files),
        base.MemoryView(base_files),
    )


def _selftest_steady_state_wrapper() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    retention_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    implementation_bytes = view.read_bytes(
        IMPLEMENTATION_POLICY_PATH,
        base.MAX_POLICY_FILE_BYTES,
    )
    base_view = base.MemoryView(
        {
            IMPLEMENTATION_POLICY_PATH: implementation_bytes,
            POLICY_SCRIPT: retention_bytes,
        }
    )
    mutated = base.MemoryView(
        {
            IMPLEMENTATION_POLICY_PATH: implementation_bytes,
            POLICY_SCRIPT: retention_bytes + b"\n# drift\n",
        }
    )
    base.expect_failure_matching(
        "H0 retention wrapper refreeze",
        "steady-state policy wrapper changed",
        _verify_extension_paths_retention,
        mutated,
        base_view,
        frozenset({POLICY_SCRIPT}),
    )


def selftest() -> None:
    _activate_retention_contract()
    impl.selftest()
    _install_retention_policy()
    _selftest_workflow_binding()
    _selftest_bootstrap_delta()
    _selftest_monotonic_retention()
    _selftest_steady_state_wrapper()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={impl.CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness H0 implementation retention integrity policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_retention_policy()
    return impl.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
