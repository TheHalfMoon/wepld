#!/usr/bin/env python3
"""Authorize one exact Harness H0 Spec Kit planning package over canonical research policy.

This wrapper grants no Harness implementation, source admission, dependency admission,
roadmap mutation, confirmatory execution, or S1-013+ authority. It authorizes only:

1. one bounded policy/workflow bootstrap from the canonical Harness research policy; and
2. after this wrapper is canonical and activation-proven, one exact ten-file
   `specs/002-harness-h0-screening/` planning-package addition.

After that exact package is canonical, those Spec Kit paths refreeze. All unrelated
candidate semantics continue through the prior canonical Harness research policy.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_harness_h0_spec_integrity.py"
PRIOR_HARNESS_RUNNER_PATH = ".github/scripts/wepld_harness_research_integrity.py"
EXPECTED_PRIOR_HARNESS_RUNNER_GIT_BLOB_SHA1 = (
    "f62e57b5f4ca702fd37525a81bd3fd303944b584"
)
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"

SPEC_KIT_BLOBS = {
    "specs/002-harness-h0-screening/constitution.md":
        "bf530e264f4d4876beb2ea8c8913df3ffdd6f1da",
    "specs/002-harness-h0-screening/spec.md":
        "444b420e15d72b238e6230f05d187abec3425785",
    "specs/002-harness-h0-screening/clarify.md":
        "c839ac24e10d921963f476389a38850bd5438458",
    "specs/002-harness-h0-screening/plan.md":
        "560e09b0369fb322bea08c0f51cdd76e9239ef1e",
    "specs/002-harness-h0-screening/checklists/requirements.md":
        "fc9620cba951519c18fa4eea14b85e48363209da",
    "specs/002-harness-h0-screening/analyze.md":
        "abe2ec11a23ddf071fcefe5e14eae62ae3fec4aa",
    "specs/002-harness-h0-screening/tasks.md":
        "04812902156229ef936a389a893d28164815ac85",
    "specs/002-harness-h0-screening/acceptance.md":
        "e48005131a18b4dd89953352f59e4bd17a073937",
    "specs/002-harness-h0-screening/ponytail.md":
        "e9351ef6df7d76676c290ca694dbe68f242d0cb3",
    "specs/002-harness-h0-screening/source-acquisition.md":
        "dec73a131c1343565f4aea4f583344acc90ff2b5",
}
SPEC_KIT_PATHS = frozenset(SPEC_KIT_BLOBS)

EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "214a3871975b242ba5b2e7cb138f3cb323e0deb2c2efef525dd990b1580f61a7",
    ADMISSION_WORKFLOW: "920efa95286cbbb7393ed904fbcca3a77a9d41ff3a3df21e44360258cf867cbd",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS = frozenset(
    {FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW}
)

HARNESS_H0_SPEC_KIT_AUTHORIZED = "EXACT_ONE_TIME_PACKAGE"
HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED = "NO"
HARNESS_SOURCE_ADMISSION = "NONE"
HARNESS_DEPENDENCY_ADMISSION = "NONE"
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


def _bind_prior_harness_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_harness_research_integrity.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen Harness research policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_HARNESS_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen Harness research policy runner drifted: "
            f"expected={EXPECTED_PRIOR_HARNESS_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_harness_runner_before_import()
import wepld_harness_research_integrity as prior  # noqa: E402

PRIOR_WORKFLOW_SHA256 = dict(prior.EXPECTED_WORKFLOW_SHA256)
PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_harness
shell = prior.shell


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_HARNESS_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_HARNESS_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen Harness research policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_HARNESS_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._verify_policy_files(view)


def _is_bootstrap_base(policy_base: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(policy_base)


def _changed_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> set[str]:
    candidate_entries = {entry.path: entry.mode for entry in candidate.entries()}
    base_entries = {entry.path: entry.mode for entry in policy_base.entries()}
    changed: set[str] = set(candidate_entries) ^ set(base_entries)
    for relative in set(candidate_entries) & set(base_entries):
        if candidate_entries[relative] != base_entries[relative]:
            changed.add(relative)
            continue
        if candidate.tree_identity(relative) != policy_base.tree_identity(relative):
            if candidate.read_bytes(
                relative, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES):
                changed.add(relative)
    return changed


def _require_canonical_h0_base(view: base.RepositoryView) -> None:
    paths = _paths(view)

    ledger_path = prior.CANONICAL_LEDGER_PATH
    if ledger_path not in paths:
        base.fail("Harness H0 Spec Kit authorization requires canonical S1 ledger")
    ledger = view.read_bytes(ledger_path, base.MAX_POLICY_FILE_BYTES)
    actual_ledger = _git_blob_sha1(ledger)
    expected_ledger = prior.EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1
    if actual_ledger != expected_ledger:
        base.fail(
            "Harness H0 Spec Kit authorization requires reconciled canonical ledger: "
            f"expected={expected_ledger} actual={actual_ledger}"
        )

    for relative, expected in sorted(prior.RESEARCH_DOC_BLOBS.items()):
        if relative not in paths:
            base.fail(
                "Harness H0 Spec Kit authorization requires canonical research bundle; "
                f"missing={relative}"
            )
        data = view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        actual = _git_blob_sha1(data)
        if actual != expected:
            base.fail(
                "canonical Harness research document drifted before H0 Spec Kit: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _validate_spec_kit_candidate(candidate: base.RepositoryView) -> None:
    candidate_paths = _paths(candidate)
    missing = sorted(SPEC_KIT_PATHS - candidate_paths)
    if missing:
        base.fail(
            "Harness H0 Spec Kit canonicalization is partial; missing="
            + ",".join(missing)
        )
    for relative, expected in sorted(SPEC_KIT_BLOBS.items()):
        data = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        actual = _git_blob_sha1(data)
        if actual != expected:
            base.fail(
                "Harness H0 Spec Kit candidate drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _require_exact_delta_h0_spec(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)
    base_paths = _paths(policy_base)

    if _is_bootstrap_base(policy_base):
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            _require_canonical_h0_base(policy_base)
            if base_paths & set(SPEC_KIT_PATHS):
                base.fail("Harness H0 Spec Kit paths unexpectedly exist before policy bootstrap")
            return
        PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    spec_touched = changed & set(SPEC_KIT_PATHS)
    if spec_touched:
        _require_canonical_h0_base(policy_base)
        if base_paths & set(SPEC_KIT_PATHS):
            base.fail("Harness H0 Spec Kit package is frozen after canonicalization")
        if changed != set(SPEC_KIT_PATHS):
            missing = sorted(set(SPEC_KIT_PATHS) - changed)
            unexpected = sorted(changed - set(SPEC_KIT_PATHS))
            detail: list[str] = []
            if missing:
                detail.append("missing=" + ",".join(missing))
            if unexpected:
                detail.append("unexpected=" + ",".join(unexpected))
            base.fail(
                "Harness H0 Spec Kit delta must be exactly ten files: "
                + ("; ".join(detail) if detail else "delta mismatch")
            )
        _validate_spec_kit_candidate(candidate)
        return

    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_h0_spec(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS:
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            actual_candidate = _sha256(candidate_bytes)
            if actual_candidate != expected_candidate:
                base.fail(
                    "Harness H0 Spec Kit workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={actual_candidate}"
                )

            expected_base = (
                PRIOR_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            )
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"Harness H0 Spec Kit {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"Harness H0 Spec Kit steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_h0_spec(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Harness H0 Spec Kit policy wrapper is missing from candidate")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Harness H0 Spec Kit bootstrap wrapper unexpectedly exists in base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Harness H0 Spec Kit steady-state base is missing wrapper")
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("Harness H0 Spec Kit steady-state policy wrapper changed")

    for relative in sorted(BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        actual_candidate = _sha256(candidate_bytes)
        if actual_candidate != expected_candidate:
            base.fail(
                "Harness H0 Spec Kit controlled workflow candidate drifted: "
                f"{relative}: expected={expected_candidate} actual={actual_candidate}"
            )
        expected_base = (
            PRIOR_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
        )
        actual_base = _sha256(base_bytes)
        if actual_base != expected_base:
            phase = "bootstrap" if bootstrap else "steady-state"
            base.fail(
                f"Harness H0 Spec Kit controlled workflow {phase} base drifted: "
                f"{relative}: expected={expected_base} actual={actual_base}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"Harness H0 Spec Kit steady-state workflow changed: {relative}")

    delegated = frozenset(
        set(controlled_paths)
        - {POLICY_SCRIPT}
        - set(BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS)
    )
    if delegated:
        prior._verify_extension_paths_harness(candidate, policy_base, delegated)


def _verify_execution_extension_controlled_paths_h0_spec(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_h0_spec(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_controlled_paths_h0_spec(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_h0_spec(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior Harness research success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"harness_h0_spec_kit_authorized={HARNESS_H0_SPEC_KIT_AUTHORIZED}")
    print(
        "harness_h0_screen_implementation_authorized="
        f"{HARNESS_H0_SCREEN_IMPLEMENTATION_AUTHORIZED}"
    )
    print(f"harness_source_admission={HARNESS_SOURCE_ADMISSION}")
    print(f"harness_dependency_admission={HARNESS_DEPENDENCY_ADMISSION}")
    print(f"harness_roadmap_mutation={ROADMAP_MUTATION}")
    print(f"s1_013_plus={S1_013_PLUS}")


def _propagate_expected_workflow_hashes() -> None:
    prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    prior._propagate_expected_workflow_hashes()


def _install_h0_spec_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    prior._install_harness_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    base.compare_base_controlled = _compare_base_controlled_h0_spec
    prior.v24.v19._require_exact_delta = _require_exact_delta_h0_spec
    shell.prior.verify_extension_controlled_paths = (
        _verify_desktop_extension_controlled_paths_h0_spec
    )
    shell.prior.prior.verify_extension_controlled_paths = (
        _verify_execution_extension_controlled_paths_h0_spec
    )

    _propagate_expected_workflow_hashes()

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success
    _INSTALLED = True


def _selftest_workflow_binding() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for relative in BOOTSTRAP_BASE_CONTROLLED_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "Harness H0 Spec Kit workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _fixture_files() -> tuple[dict[str, bytes], dict[bytes, str]]:
    files: dict[str, bytes] = {}
    identities: dict[bytes, str] = {}

    ledger = b"canonical-ledger-fixture"
    files[prior.CANONICAL_LEDGER_PATH] = ledger
    identities[ledger] = prior.EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1

    for relative, expected in prior.RESEARCH_DOC_BLOBS.items():
        data = ("research:" + relative).encode("utf-8")
        files[relative] = data
        identities[data] = expected

    return files, identities


def _selftest_bootstrap_delta() -> None:
    base_files, identities = _fixture_files()
    base_files[FOUNDATION_WORKFLOW] = b"prior-foundation"
    base_files[ADMISSION_WORKFLOW] = b"prior-admission"

    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"h0-spec-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"new-admission"

    original = globals()["_git_blob_sha1"]
    try:
        def fake_git_blob_sha1(data: bytes) -> str:
            if data in identities:
                return identities[data]
            return original(data)

        globals()["_git_blob_sha1"] = fake_git_blob_sha1
        _require_exact_delta_h0_spec(
            base.MemoryView(candidate_files),
            base.MemoryView(base_files),
        )
    finally:
        globals()["_git_blob_sha1"] = original


def _selftest_spec_transition() -> None:
    base_files, identities = _fixture_files()
    base_files[POLICY_SCRIPT] = b"h0-spec-policy"

    spec_fixtures = {
        relative: ("spec:" + relative).encode("utf-8")
        for relative in SPEC_KIT_PATHS
    }
    for relative, data in spec_fixtures.items():
        identities[data] = SPEC_KIT_BLOBS[relative]

    candidate_files = dict(base_files)
    candidate_files.update(spec_fixtures)

    original = globals()["_git_blob_sha1"]
    try:
        def fake_git_blob_sha1(data: bytes) -> str:
            if data in identities:
                return identities[data]
            return original(data)

        globals()["_git_blob_sha1"] = fake_git_blob_sha1

        _require_exact_delta_h0_spec(
            base.MemoryView(candidate_files),
            base.MemoryView(base_files),
        )

        first_path = sorted(SPEC_KIT_PATHS)[0]
        partial = dict(base_files)
        partial[first_path] = spec_fixtures[first_path]
        base.expect_failure_matching(
            "Harness H0 Spec Kit partial transition",
            "delta must be exactly ten files",
            _require_exact_delta_h0_spec,
            base.MemoryView(partial),
            base.MemoryView(base_files),
        )

        wrong_path = sorted(SPEC_KIT_PATHS)[-1]
        wrong = dict(candidate_files)
        wrong[wrong_path] = b"wrong-h0-spec-doc"
        base.expect_failure_matching(
            "Harness H0 Spec Kit wrong blob",
            "candidate drifted",
            _require_exact_delta_h0_spec,
            base.MemoryView(wrong),
            base.MemoryView(base_files),
        )

        post_base = dict(candidate_files)
        post_candidate = dict(post_base)
        post_candidate[first_path] = b"later-h0-spec-drift"
        base.expect_failure_matching(
            "Harness H0 Spec Kit refreeze",
            "frozen after canonicalization",
            _require_exact_delta_h0_spec,
            base.MemoryView(post_candidate),
            base.MemoryView(post_base),
        )
    finally:
        globals()["_git_blob_sha1"] = original


def _selftest_steady_state_wrapper() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)

    candidate = base.MemoryView({POLICY_SCRIPT: policy_bytes})
    policy_base = base.MemoryView({POLICY_SCRIPT: policy_bytes})
    if _is_bootstrap_base(policy_base):
        base.fail("Harness H0 Spec Kit steady-state self-test misclassified base")

    mutated = base.MemoryView({POLICY_SCRIPT: policy_bytes + b"\n# drift\n"})
    base.expect_failure_matching(
        "Harness H0 Spec Kit wrapper refreeze",
        "steady-state policy wrapper changed",
        _verify_extension_paths_h0_spec,
        mutated,
        policy_base,
        frozenset({POLICY_SCRIPT}),
    )


def selftest() -> None:
    _propagate_expected_workflow_hashes()
    prior.selftest()
    _install_h0_spec_policy()
    _selftest_workflow_binding()
    _selftest_bootstrap_delta()
    _selftest_spec_transition()
    _selftest_steady_state_wrapper()
    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness H0 Spec Kit authorization policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_h0_spec_policy()
    return prior.v24.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
