#!/usr/bin/env python3
"""H0-012 Repair-3: bridge the exact H0 implementation paths through the inherited S1 allowlist.

The canonical H0 implementation/retention policies already own the exact
research/harness_h0/ path set, stage order, Cargo contract, lock identity,
file modes/sizes, and monotonic retention. Their first real H0-013 candidate
proved a composition defect: the older S1 tracked-path allowlist rejected the
bounded H0 paths before the H0 policy could evaluate them.

This wrapper repairs only that composition boundary. It does not widen S1,
does not authorize arbitrary research paths, and grants no screening/runtime,
provider/model, Harbor, product-integration, roadmap, or H0-014+ authority.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_harness_h0_implementation_allowlist_repair_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_harness_h0_implementation_retention_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "b5ff578cf6fb7aeb309ecc7259c259d2c870da76"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "814ba290b91db185e15147ac10c1c2db301fb56bdd208f4c9cc0998fe895d6c7",
    ADMISSION_WORKFLOW: "c361695482ad1986aefd5c49c3b571f104c64ea8bd3208cd98cfa985655f979a",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "ea2ab8b1e4944da9f46106ad03b61551855659657151ddd15a2002e1147eda56",
    ADMISSION_WORKFLOW: "7fb52746a4abe457d426baed7bab34c36fc53c40c9d7d9e550a69b65c1be18ac",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

H0_012_REPAIR_3 = "BOUNDED_H0_TRACKED_PATH_ALLOWLIST_BRIDGE"
H0_TRACKED_PATH_ALLOWLIST = "EXACT_IMPLEMENTATION_PATHS_ONLY"
PRODUCT_HARNESS_INTEGRATION = "NO"
H0_CONFIRMATORY_EXECUTION = "NO"
HARBOR_ADMISSION = "NONE"
ROADMAP_MUTATION = "NONE"
H0_014_PLUS = "NOT_STARTED"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _bind_prior_policy_before_import() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0-012 retention policy runner drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_harness_h0_implementation_retention_integrity as retention  # noqa: E402

impl = retention.impl
shell = retention.shell
PRIOR_IMPL_REQUIRE_EXACT_DELTA = retention.IMPL_REQUIRE_EXACT_DELTA
PRIOR_VALIDATE_ALLOWED_PATHS = shell.validate_allowed_paths


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(policy_base)


def _activate_allowlist_repair_contract() -> None:
    retention.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)


def _require_exact_delta_allowlist_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = impl._changed_paths(candidate, policy_base)
    if _is_bootstrap_base(policy_base):
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            return
    PRIOR_IMPL_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_allowlist_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "H0 allowlist-repair workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
                if bootstrap
                else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"H0 allowlist-repair {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    f"H0 allowlist-repair steady-state workflow changed: {relative}"
                )
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_allowlist_repair(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("H0 allowlist-repair policy wrapper is missing from candidate")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail(
                    "H0 allowlist-repair bootstrap wrapper unexpectedly exists in trusted base"
                )
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("H0 allowlist-repair steady-state base is missing wrapper")
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("H0 allowlist-repair steady-state policy wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        actual_candidate = _sha256(candidate_bytes)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if actual_candidate != expected_candidate:
            base.fail(
                "H0 allowlist-repair controlled workflow candidate drifted: "
                f"{relative}: expected={expected_candidate} actual={actual_candidate}"
            )
        expected_base = (
            PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
            if bootstrap
            else expected_candidate
        )
        actual_base = _sha256(base_bytes)
        if actual_base != expected_base:
            phase = "bootstrap" if bootstrap else "steady-state"
            base.fail(
                "H0 allowlist-repair controlled workflow "
                f"{phase} base drifted: {relative}: "
                f"expected={expected_base} actual={actual_base}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(
                f"H0 allowlist-repair steady-state workflow changed: {relative}"
            )

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        retention._verify_extension_paths_retention(
            candidate,
            policy_base,
            delegated,
        )


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_allowlist_repair(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_allowlist_repair(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _validate_allowed_paths_h0_bridge(paths: set[str], stage: str) -> None:
    h0_paths = {
        path for path in paths if path.startswith(impl.IMPLEMENTATION_ROOT)
    }
    unknown = sorted(h0_paths - set(impl.IMPLEMENTATION_PATHS))
    if unknown:
        base.fail(
            "tracked H0 implementation path outside exact bounded allowlist: "
            + ", ".join(unknown)
        )

    PRIOR_VALIDATE_ALLOWED_PATHS(paths - h0_paths, stage)


def _verify_policy_files(view: base.RepositoryView) -> None:
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0-012 retention policy drifted in repository view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    retention._verify_policy_files(view)


def _require_overlay_identity() -> None:
    if retention.IMPL_REQUIRE_EXACT_DELTA is not _require_exact_delta_allowlist_repair:
        base.fail("H0 allowlist-repair exact-delta delegate drifted")
    retention._require_exact_delta_hook_identity(
        retention._require_exact_delta_retention,
        "allowlist-repair-overlay",
    )
    if shell.validate_allowed_paths is not _validate_allowed_paths_h0_bridge:
        base.fail("H0 allowlist-repair tracked-path hook drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior H0 retention success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"h0_012_repair_3={H0_012_REPAIR_3}")
    print(f"h0_tracked_path_allowlist={H0_TRACKED_PATH_ALLOWLIST}")
    print(f"product_harness_integration={PRODUCT_HARNESS_INTEGRATION}")
    print(f"h0_confirmatory_execution={H0_CONFIRMATORY_EXECUTION}")
    print(f"harbor_admission={HARBOR_ADMISSION}")
    print(f"harness_roadmap_mutation={ROADMAP_MUTATION}")
    print(f"h0_014_plus={H0_014_PLUS}")


def _install_allowlist_repair_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity()
        return

    _activate_allowlist_repair_contract()
    retention._install_retention_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_allowlist_repair
    base.compare_base_controlled = _compare_base_controlled_allowlist_repair

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.verify_extension_controlled_paths = _verify_desktop_extension_paths
    shell.prior.prior.verify_extension_controlled_paths = _verify_execution_extension_paths

    shell.validate_allowed_paths = _validate_allowed_paths_h0_bridge
    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success

    _INSTALLED = True
    _require_overlay_identity()


def _selftest_workflow_binding() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for relative in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "H0 allowlist-repair workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _selftest_bootstrap_delta() -> None:
    base_files = {
        PRIOR_POLICY_PATH: b"canonical-retention-policy",
        FOUNDATION_WORKFLOW: b"prior-foundation",
        ADMISSION_WORKFLOW: b"prior-admission",
    }
    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"allowlist-repair-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"new-admission"
    trees = {
        POLICY_SCRIPT: "1" * 40,
        FOUNDATION_WORKFLOW: "2" * 40,
        ADMISSION_WORKFLOW: "3" * 40,
    }
    _require_exact_delta_allowlist_repair(
        base.MemoryView(candidate_files, trees=trees),
        base.MemoryView(base_files),
    )

    mixed = dict(candidate_files)
    mixed[impl.IMPLEMENTATION_ROOT + "src/lib.rs"] = b"#![forbid(unsafe_code)]\n"
    base.expect_failure_matching(
        "H0 allowlist-repair mixed implementation bootstrap",
        "H0 implementation PR cannot mix research implementation with other paths",
        _require_exact_delta_allowlist_repair,
        base.MemoryView(mixed),
        base.MemoryView(base_files),
    )


def _selftest_allowlist_bridge() -> None:
    global PRIOR_VALIDATE_ALLOWED_PATHS
    known = impl.CARGO_TOML_PATH
    unknown = impl.IMPLEMENTATION_ROOT + "src/not-authorized.rs"
    seen: list[tuple[set[str], str]] = []

    original = PRIOR_VALIDATE_ALLOWED_PATHS

    def capture(paths: set[str], stage: str) -> None:
        seen.append((set(paths), stage))

    PRIOR_VALIDATE_ALLOWED_PATHS = capture
    try:
        _validate_allowed_paths_h0_bridge({"README.md", known}, "fixture-stage")
        if seen != [({"README.md"}, "fixture-stage")]:
            base.fail(f"H0 allowlist bridge projection self-test drifted: {seen}")
        base.expect_failure_matching(
            "H0 unknown implementation path rejection",
            "outside exact bounded allowlist",
            _validate_allowed_paths_h0_bridge,
            {"README.md", unknown},
            "fixture-stage",
        )
    finally:
        PRIOR_VALIDATE_ALLOWED_PATHS = original


def _selftest_hook_identity() -> None:
    _require_overlay_identity()

    installed_delta = retention.IMPL_REQUIRE_EXACT_DELTA
    retention.IMPL_REQUIRE_EXACT_DELTA = PRIOR_IMPL_REQUIRE_EXACT_DELTA
    try:
        base.expect_failure_matching(
            "H0 allowlist-repair exact-delta hook identity mismatch",
            "exact-delta delegate drifted",
            _require_overlay_identity,
        )
    finally:
        retention.IMPL_REQUIRE_EXACT_DELTA = installed_delta

    installed_allowlist = shell.validate_allowed_paths
    shell.validate_allowed_paths = PRIOR_VALIDATE_ALLOWED_PATHS
    try:
        base.expect_failure_matching(
            "H0 allowlist-repair tracked-path hook identity mismatch",
            "tracked-path hook drifted",
            _require_overlay_identity,
        )
    finally:
        shell.validate_allowed_paths = installed_allowlist

    _require_overlay_identity()


def selftest() -> None:
    _activate_allowlist_repair_contract()
    retention.selftest()
    _install_allowlist_repair_policy()
    _selftest_workflow_binding()
    _selftest_bootstrap_delta()
    _selftest_allowlist_bridge()
    _selftest_hook_identity()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={impl.CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness H0 implementation allowlist-repair policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_allowlist_repair_policy()
    return retention.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
