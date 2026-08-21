#!/usr/bin/env python3
"""Authorize only the exact bounded WePLD Harness H0-SCREEN research implementation surface.

This policy is layered over the canonical H0 Spec Kit two-finding repair policy.
The candidate policy itself grants no implementation authority until H0-012 has
qualified, merged, and activation-proven this exact policy/workflow bootstrap.

After canonical activation, the policy permits only the finite research-only
`research/harness_h0/` surface enumerated below. It freezes the H0-010 direct
dependency set and the exact 53-package crates.io lock graph, forbids product
workspace integration, provider SDKs, Harbor, cloud/distributed machinery, and
all paths outside the bounded research package.

Canonical task prerequisites remain authoritative. This policy is a path,
dependency, and trust-boundary guard; it does not mark H0-013+ complete and does
not authorize H0-SCREEN or H0-CONFIRM execution.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_harness_h0_implementation_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_harness_h0_spec_two_finding_repair_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "64087cb40d6b673cc9a06fbee62c35faec9f7955"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"

# External H0-010 closeout evidence. This is provenance, not a network lookup.
H0_010_CLOSEOUT_COMMENT_ID = 5363275860
H0_010_EVIDENCE_ZIP_SHA256 = "f6b12fba3b81018709f64513c31aab5d260ad3da7b2017cf985b77dc2a29f696"
H0_010_WITNESS_LOCK_SHA256 = "eea531f1a03f599e10d2a350656089653839483ca3f31e8a112147c66a058b35"

IMPLEMENTATION_ROOT = "research/harness_h0/"
IMPLEMENTATION_PATHS = frozenset(
    {
        'research/harness_h0/Cargo.toml',
        'research/harness_h0/Cargo.lock',
        'research/harness_h0/.cargo/config.toml',
        'research/harness_h0/src/lib.rs',
        'research/harness_h0/src/canonical.rs',
        'research/harness_h0/src/manifests.rs',
        'research/harness_h0/src/identity.rs',
        'research/harness_h0/src/recipe.rs',
        'research/harness_h0/src/calibration.rs',
        'research/harness_h0/src/runner.rs',
        'research/harness_h0/src/evidence.rs',
        'research/harness_h0/src/verifier.rs',
        'research/harness_h0/src/screening.rs',
        'research/harness_h0/tests/synthetic_runner.rs',
        'research/harness_h0/tests/recipe_conformance.rs',
        'research/harness_h0/tests/evidence_contract.rs',
        'research/harness_h0/tests/isolation.rs',
        'research/harness_h0/tests/hard_gates.rs',
        'research/harness_h0/fixtures/synthetic/cases.json',
        'research/harness_h0/fixtures/synthetic/fixture_driver.sh',
        'research/harness_h0/fixtures/calibration/suite.json',
        'research/harness_h0/fixtures/recipe_conformance/cases.json',
    }
)

CARGO_TOML_PATH = IMPLEMENTATION_ROOT + "Cargo.toml"
CARGO_LOCK_PATH = IMPLEMENTATION_ROOT + "Cargo.lock"
CARGO_CONFIG_PATH = IMPLEMENTATION_ROOT + ".cargo/config.toml"
LIB_RS_PATH = IMPLEMENTATION_ROOT + "src/lib.rs"

H0_013_INITIAL_PATHS = frozenset(
    {
        CARGO_TOML_PATH,
        CARGO_LOCK_PATH,
        CARGO_CONFIG_PATH,
        LIB_RS_PATH,
        IMPLEMENTATION_ROOT + "src/canonical.rs",
        IMPLEMENTATION_ROOT + "src/identity.rs",
    }
)
H0_014_INITIAL_PATHS = frozenset(
    {
        LIB_RS_PATH,
        IMPLEMENTATION_ROOT + "src/manifests.rs",
    }
)
H0_015_INITIAL_PATHS = frozenset(
    {
        LIB_RS_PATH,
        IMPLEMENTATION_ROOT + "src/evidence.rs",
        IMPLEMENTATION_ROOT + "src/verifier.rs",
        IMPLEMENTATION_ROOT + "tests/evidence_contract.rs",
        IMPLEMENTATION_ROOT + "tests/hard_gates.rs",
    }
)
H0_016_INITIAL_PATHS = frozenset(
    {
        LIB_RS_PATH,
        IMPLEMENTATION_ROOT + "src/recipe.rs",
        IMPLEMENTATION_ROOT + "tests/recipe_conformance.rs",
    }
)

RECIPE_CASES_PATH = IMPLEMENTATION_ROOT + "fixtures/recipe_conformance/cases.json"
CALIBRATION_PATHS = frozenset(
    {
        IMPLEMENTATION_ROOT + "src/calibration.rs",
        IMPLEMENTATION_ROOT + "fixtures/calibration/suite.json",
    }
)
RUNNER_PATHS = frozenset(
    {
        IMPLEMENTATION_ROOT + "src/runner.rs",
        IMPLEMENTATION_ROOT + "src/screening.rs",
        IMPLEMENTATION_ROOT + "tests/synthetic_runner.rs",
    }
)
ISOLATION_PATH = IMPLEMENTATION_ROOT + "tests/isolation.rs"
SYNTHETIC_FIXTURE_PATHS = frozenset(
    {
        IMPLEMENTATION_ROOT + "fixtures/synthetic/cases.json",
        IMPLEMENTATION_ROOT + "fixtures/synthetic/fixture_driver.sh",
    }
)

MAX_IMPLEMENTATION_FILE_BYTES = 256_000
MAX_IMPLEMENTATION_TOTAL_BYTES = 2_000_000
MAX_IMPLEMENTATION_DELTA_PATHS = 10

EXPECTED_CARGO_CONFIG = (
    '[build]\n'
    'rustflags = [\n'
    '  "--cfg",\n'
    '  "sha2_backend=\\\"soft\\\"",\n'
    '  "--cfg",\n'
    '  "sha2_backend_soft=\\\"compact\\\"",\n'
    ']\n'
).encode("utf-8")

EXPECTED_PACKAGE = {
    "name": "wepld-harness-h0",
    "version": "0.0.0",
    "edition": "2024",
    "rust-version": "1.97.1",
    "publish": False,
}
EXPECTED_WORKSPACE = {"resolver": "3"}
EXPECTED_DIRECT_DEPENDENCIES = {
    "serde": {
        "version": "=1.0.229",
        "default-features": False,
        "features": ["std", "derive"],
    },
    "serde_json": {
        "version": "=1.0.151",
        "default-features": False,
        "features": ["std"],
    },
    "sha2": {
        "version": "=0.11.0",
        "default-features": False,
    },
    "ureq": {
        "version": "=3.4.0",
        "default-features": False,
        "features": ["rustls"],
    },
}

H0_IMPLEMENTATION_LOCK_SHA256 = "5ab13b3bbb94c8245bea6b7ba7d76f84ef642996dd6c4b31e08def1796b6943a"


EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "a40431a9c248934b9d6912d5c87955bdbef2c2ede4bae4001b046bba4632332a",
    ADMISSION_WORKFLOW: "5ec4d1efc3af34651de48b08e95b768f9a3c12bfafaab5ad34d32485961e25e7",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "33058592087a0e8f44ba05bc27653c2c039a9eae9110a92918f6511ce6d4cd7a",
    ADMISSION_WORKFLOW: "23b370d1e0ff14c04abd9a19d0a087010cfbabda6a0aa5854bdb7863494b6192",
    ".github/workflows/s1-contracts.yml":
        "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})

H0_IMPLEMENTATION_POLICY_SURFACE = "EXACT_BOUNDED_RESEARCH_HARNESS_H0"
H0_DIRECT_COMPONENT_SET = "EXACT_AND_MINIMUM"
H0_SCREEN_IMPLEMENTATION_AUTHORIZED = "NO_UNTIL_H0_012_CANONICAL_ACTIVATION"
PRODUCT_HARNESS_INTEGRATION = "NO"
H0_CONFIRMATORY_EXECUTION = "NO"
HARBOR_ADMISSION = "NONE"
PROVIDER_SDK_ADMISSION = "NONE"
CLOUD_SDK_ADMISSION = "NONE"
DISTRIBUTED_SCHEDULER_ADMISSION = "NONE"
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


def _entry_modes(view: base.RepositoryView) -> dict[str, str]:
    return {entry.path: entry.mode for entry in view.entries()}


def _bind_prior_policy_before_import() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0 Spec Kit two-finding policy runner drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_harness_h0_spec_two_finding_repair_integrity as prior  # noqa: E402

shell = prior.shell
PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_two_finding_repair


def _activate_implementation_contract() -> None:
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior._activate_two_finding_contract()


def _verify_policy_files(view: base.RepositoryView) -> None:
    data = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen H0 Spec Kit two-finding policy drifted in repository view: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    prior._verify_policy_files(view)


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    paths = _paths(view)
    return POLICY_SCRIPT not in paths and PRIOR_POLICY_PATH in paths


def _changed_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> set[str]:
    return prior._changed_paths(candidate, policy_base)


def _require_canonical_h0_010_base(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if PRIOR_POLICY_PATH not in paths:
        base.fail("H0 implementation policy requires canonical two-finding policy")
    prior_bytes = view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES)
    actual_prior = _git_blob_sha1(prior_bytes)
    if actual_prior != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "H0 implementation policy base prior policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual_prior}"
        )

    for relative, expected in sorted(prior.TWO_FINDING_SPEC_KIT_BLOBS.items()):
        if relative not in paths:
            base.fail(f"H0 implementation policy requires canonical Spec Kit: missing={relative}")
        data = view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        actual = _git_blob_sha1(data)
        if actual != expected:
            base.fail(
                "canonical H0 Spec Kit drifted before implementation policy bootstrap: "
                f"{relative}: expected={expected} actual={actual}"
            )

    existing = sorted(path for path in paths if path.startswith(IMPLEMENTATION_ROOT))
    if existing:
        base.fail(
            "H0 implementation policy bootstrap requires no pre-existing implementation tree: "
            + ",".join(existing)
        )


def _decode_toml(data: bytes, label: str) -> dict:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        base.fail(f"{label} is not UTF-8: {exc}")
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        base.fail(f"{label} is invalid TOML: {exc}")


def _validate_cargo_toml(data: bytes) -> None:
    doc = _decode_toml(data, CARGO_TOML_PATH)
    expected_keys = {"package", "workspace", "dependencies"}
    if set(doc) != expected_keys:
        base.fail(
            "H0 Cargo.toml top-level surface drifted: "
            f"expected={sorted(expected_keys)} actual={sorted(doc)}"
        )
    if doc["package"] != EXPECTED_PACKAGE:
        base.fail(f"H0 Cargo package contract drifted: {doc['package']}")
    if doc["workspace"] != EXPECTED_WORKSPACE:
        base.fail(f"H0 nested workspace contract drifted: {doc['workspace']}")
    if doc["dependencies"] != EXPECTED_DIRECT_DEPENDENCIES:
        base.fail(f"H0 direct dependency contract drifted: {doc['dependencies']}")


def _validate_cargo_lock(data: bytes) -> None:
    actual = _sha256(data)
    if actual != H0_IMPLEMENTATION_LOCK_SHA256:
        base.fail(
            "H0 Cargo.lock exact acquired graph drifted: "
            f"expected={H0_IMPLEMENTATION_LOCK_SHA256} actual={actual}"
        )


def _validate_fixture_file(path: str, data: bytes) -> None:
    if path.endswith(".json"):
        try:
            json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            base.fail(f"H0 fixture JSON invalid: {path}: {exc}")
    elif path.endswith(".sh"):
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            base.fail(f"H0 fixture shell is not UTF-8: {path}: {exc}")
        if not text.startswith("#!/bin/sh\n"):
            base.fail(f"H0 fixture shell must use bounded /bin/sh shebang: {path}")


def _validate_implementation_candidate(candidate: base.RepositoryView) -> None:
    paths = _paths(candidate)
    root_paths = {path for path in paths if path.startswith(IMPLEMENTATION_ROOT)}
    unknown = sorted(root_paths - set(IMPLEMENTATION_PATHS))
    if unknown:
        base.fail("H0 implementation tree contains unauthorized paths: " + ",".join(unknown))

    if not root_paths:
        return

    trio = {CARGO_TOML_PATH, CARGO_LOCK_PATH, CARGO_CONFIG_PATH}
    present_trio = trio & root_paths
    if present_trio != trio:
        base.fail(
            "H0 implementation Cargo contract must be introduced atomically: "
            f"present={sorted(present_trio)} required={sorted(trio)}"
        )

    total = 0
    modes = _entry_modes(candidate)
    for relative in sorted(root_paths):
        if modes.get(relative) != "100644":
            base.fail(f"H0 implementation path must be regular mode 100644: {relative}={modes.get(relative)}")
        data = candidate.read_bytes(relative, MAX_IMPLEMENTATION_FILE_BYTES)
        total += len(data)
        if len(data) > MAX_IMPLEMENTATION_FILE_BYTES:
            base.fail(f"H0 implementation file exceeds bounded size: {relative}")
        if relative.endswith(".rs"):
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError as exc:
                base.fail(f"H0 Rust source is not UTF-8: {relative}: {exc}")
            if relative == LIB_RS_PATH and "#![forbid(unsafe_code)]" not in text:
                base.fail("H0 lib.rs must contain #![forbid(unsafe_code)]")
        if "/fixtures/" in relative:
            _validate_fixture_file(relative, data)

    if total > MAX_IMPLEMENTATION_TOTAL_BYTES:
        base.fail(f"H0 implementation tree exceeds total byte bound: {total}")

    _validate_cargo_toml(candidate.read_bytes(CARGO_TOML_PATH, MAX_IMPLEMENTATION_FILE_BYTES))
    _validate_cargo_lock(candidate.read_bytes(CARGO_LOCK_PATH, MAX_IMPLEMENTATION_FILE_BYTES))
    config = candidate.read_bytes(CARGO_CONFIG_PATH, MAX_IMPLEMENTATION_FILE_BYTES)
    if config != EXPECTED_CARGO_CONFIG:
        base.fail(
            "H0 sha2 backend config drifted: "
            f"expected_sha256={_sha256(EXPECTED_CARGO_CONFIG)} actual_sha256={_sha256(config)}"
        )


def _require_implementation_stage_order(
    changed: set[str],
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    base_paths = _paths(policy_base)

    if CARGO_TOML_PATH not in base_paths:
        if changed != set(H0_013_INITIAL_PATHS):
            base.fail(
                "first H0 implementation delta must be exact H0-013 bootstrap surface: "
                f"expected={sorted(H0_013_INITIAL_PATHS)} actual={sorted(changed)}"
            )
        return

    manifests = IMPLEMENTATION_ROOT + "src/manifests.rs"
    if manifests not in base_paths:
        if changed != set(H0_014_INITIAL_PATHS):
            base.fail(
                "next H0 implementation delta must be exact H0-014 manifest surface: "
                f"expected={sorted(H0_014_INITIAL_PATHS)} actual={sorted(changed)}"
            )
        return

    evidence = IMPLEMENTATION_ROOT + "src/evidence.rs"
    if evidence not in base_paths:
        if changed != set(H0_015_INITIAL_PATHS):
            base.fail(
                "next H0 implementation delta must be exact H0-015 evidence/finalizer surface: "
                f"expected={sorted(H0_015_INITIAL_PATHS)} actual={sorted(changed)}"
            )
        return

    recipe = IMPLEMENTATION_ROOT + "src/recipe.rs"
    if recipe not in base_paths:
        if changed != set(H0_016_INITIAL_PATHS):
            base.fail(
                "next H0 implementation delta must be exact H0-016 option-library surface: "
                f"expected={sorted(H0_016_INITIAL_PATHS)} actual={sorted(changed)}"
            )
        return

    if len(changed) > MAX_IMPLEMENTATION_DELTA_PATHS:
        base.fail(
            "H0 implementation delta exceeds bounded per-PR path count: "
            f"count={len(changed)} max={MAX_IMPLEMENTATION_DELTA_PATHS}"
        )

    if changed & set(CALIBRATION_PATHS):
        if RECIPE_CASES_PATH not in base_paths:
            base.fail("H0 calibration implementation is blocked until recipe conformance cases are canonical")

    if changed & set(RUNNER_PATHS):
        calibration_suite = IMPLEMENTATION_ROOT + "fixtures/calibration/suite.json"
        if calibration_suite not in base_paths:
            base.fail("H0 runner implementation is blocked until calibration suite is canonical")

    if ISOLATION_PATH in changed:
        runner = IMPLEMENTATION_ROOT + "src/runner.rs"
        if runner not in base_paths:
            base.fail("H0 isolation work is blocked until the runner is canonical")

    if changed & set(SYNTHETIC_FIXTURE_PATHS):
        if ISOLATION_PATH not in base_paths:
            base.fail("H0 synthetic fixture package is blocked until isolation work is canonical")


def _require_exact_delta_h0_implementation(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths(candidate, policy_base)
    bootstrap = _is_bootstrap_base(policy_base)

    if bootstrap:
        if changed == set(BOOTSTRAP_DELTA_PATHS):
            _require_canonical_h0_010_base(policy_base)
            return
        if any(path.startswith(IMPLEMENTATION_ROOT) for path in changed):
            base.fail("H0 implementation cannot transition before H0-012 policy activation")
        PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)
        return

    root_changed = {path for path in changed if path.startswith(IMPLEMENTATION_ROOT)}
    if root_changed:
        if root_changed != changed:
            unexpected = sorted(changed - root_changed)
            base.fail(
                "H0 implementation PR cannot mix research implementation with other paths: "
                + ",".join(unexpected)
            )
        unknown = sorted(root_changed - set(IMPLEMENTATION_PATHS))
        if unknown:
            base.fail("H0 implementation delta contains unauthorized paths: " + ",".join(unknown))
        _require_implementation_stage_order(changed, candidate, policy_base)
        _validate_implementation_candidate(candidate)
        return

    PRIOR_REQUIRE_EXACT_DELTA(candidate, policy_base)


def _compare_base_controlled_h0_implementation(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    for relative in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)

        if relative in BOOTSTRAP_WORKFLOWS:
            candidate_hash = _sha256(candidate_bytes)
            expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
            if candidate_hash != expected_candidate:
                base.fail(
                    "H0 implementation policy workflow candidate drifted: "
                    f"{relative}: expected={expected_candidate} actual={candidate_hash}"
                )
            expected_base = (
                PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
                if bootstrap
                else expected_candidate
            )
            base_hash = _sha256(base_bytes)
            if base_hash != expected_base:
                phase = "bootstrap" if bootstrap else "steady-state"
                base.fail(
                    f"H0 implementation policy {phase} trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={base_hash}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"H0 implementation policy steady-state workflow changed: {relative}")
            continue

        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")


def _verify_extension_paths_h0_implementation(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled_paths: frozenset[str],
) -> None:
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in controlled_paths:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("H0 implementation policy wrapper is missing from candidate")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("H0 implementation wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("H0 implementation steady-state base is missing wrapper")
            if candidate.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("H0 implementation steady-state policy wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & controlled_paths):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        candidate_hash = _sha256(candidate_bytes)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if candidate_hash != expected_candidate:
            base.fail(
                "H0 implementation controlled workflow candidate drifted: "
                f"{relative}: expected={expected_candidate} actual={candidate_hash}"
            )
        expected_base = (
            PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
            if bootstrap
            else expected_candidate
        )
        base_hash = _sha256(base_bytes)
        if base_hash != expected_base:
            phase = "bootstrap" if bootstrap else "steady-state"
            base.fail(
                "H0 implementation controlled workflow "
                f"{phase} base drifted: {relative}: expected={expected_base} actual={base_hash}"
            )
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"H0 implementation steady-state workflow changed: {relative}")

    delegated = frozenset(
        set(controlled_paths) - {POLICY_SCRIPT} - set(BOOTSTRAP_WORKFLOWS)
    )
    if delegated:
        prior._verify_extension_paths_two_finding_repair(candidate, policy_base, delegated)


def _verify_execution_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_h0_implementation(
        candidate,
        policy_base,
        shell.prior.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _verify_desktop_extension_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _verify_extension_paths_h0_implementation(
        candidate,
        policy_base,
        shell.prior.EXTENSION_CONTROLLED_PATHS,
    )


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None:
        base.fail("prior H0 Spec Kit success printer is not installed")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"h0_010_closeout_comment_id={H0_010_CLOSEOUT_COMMENT_ID}")
    print(f"h0_direct_component_set={H0_DIRECT_COMPONENT_SET}")
    print(f"h0_implementation_policy_surface={H0_IMPLEMENTATION_POLICY_SURFACE}")
    print(
        "h0_screen_implementation_authorized="
        f"{H0_SCREEN_IMPLEMENTATION_AUTHORIZED}"
    )
    print(f"product_harness_integration={PRODUCT_HARNESS_INTEGRATION}")
    print(f"h0_confirmatory_execution={H0_CONFIRMATORY_EXECUTION}")
    print(f"harbor_admission={HARBOR_ADMISSION}")
    print(f"provider_sdk_admission={PROVIDER_SDK_ADMISSION}")
    print(f"cloud_sdk_admission={CLOUD_SDK_ADMISSION}")
    print(f"distributed_scheduler_admission={DISTRIBUTED_SCHEDULER_ADMISSION}")
    print(f"harness_roadmap_mutation={ROADMAP_MUTATION}")
    print(f"s1_013_plus={S1_013_PLUS}")


def _install_h0_implementation_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    _activate_implementation_contract()
    prior._install_two_finding_repair_policy()
    _PRIOR_PRINT_SUCCESS = shell.print_success

    base.compare_base_controlled = _compare_base_controlled_h0_implementation
    prior.prior.prior.prior.prior.prior.v24.v19._require_exact_delta = (
        _require_exact_delta_h0_implementation
    )
    shell.prior.verify_extension_controlled_paths = _verify_desktop_extension_paths
    shell.prior.prior.verify_extension_controlled_paths = _verify_execution_extension_paths

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
    for relative in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[relative]
        if actual != expected:
            base.fail(
                "H0 implementation policy workflow drifted: "
                f"{relative}: expected={expected} actual={actual}"
            )


def _fixture_canonical_base() -> dict[str, bytes]:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    files = {
        PRIOR_POLICY_PATH: view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES),
    }
    for relative in prior.TWO_FINDING_SPEC_KIT_BLOBS:
        files[relative] = view.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
    return files


def _manifest_fixture_bytes() -> bytes:
    return (
        '[package]\n'
        'name = "wepld-harness-h0"\n'
        'version = "0.0.0"\n'
        'edition = "2024"\n'
        'rust-version = "1.97.1"\n'
        'publish = false\n'
        '\n'
        '[workspace]\n'
        'resolver = "3"\n'
        '\n'
        '[dependencies]\n'
        'serde = { version = "=1.0.229", default-features = false, features = ["std", "derive"] }\n'
        'serde_json = { version = "=1.0.151", default-features = false, features = ["std"] }\n'
        'sha2 = { version = "=0.11.0", default-features = false }\n'
        'ureq = { version = "=3.4.0", default-features = false, features = ["rustls"] }\n'
    ).encode("utf-8")


def _selftest_bootstrap_delta() -> None:
    base_files = _fixture_canonical_base()
    base_files[FOUNDATION_WORKFLOW] = b"prior-foundation"
    base_files[ADMISSION_WORKFLOW] = b"prior-admission"

    candidate_files = dict(base_files)
    candidate_files[POLICY_SCRIPT] = b"h0-implementation-policy"
    candidate_files[FOUNDATION_WORKFLOW] = b"new-foundation"
    candidate_files[ADMISSION_WORKFLOW] = b"new-admission"
    trees = {
        POLICY_SCRIPT: "1" * 40,
        FOUNDATION_WORKFLOW: "2" * 40,
        ADMISSION_WORKFLOW: "3" * 40,
    }
    _require_exact_delta_h0_implementation(
        base.MemoryView(candidate_files, trees=trees),
        base.MemoryView(base_files),
    )

    premature = dict(base_files)
    premature[IMPLEMENTATION_ROOT + "src/lib.rs"] = b"#![forbid(unsafe_code)]\n"
    base.expect_failure_matching(
        "H0 implementation premature transition",
        "cannot transition before H0-012 policy activation",
        _require_exact_delta_h0_implementation,
        base.MemoryView(premature),
        base.MemoryView(base_files),
    )


def _selftest_manifest_contract() -> None:
    _validate_cargo_toml(_manifest_fixture_bytes())
    bad_manifest = _manifest_fixture_bytes().replace(
        b'features = ["rustls"]',
        b'features = ["rustls", "json"]',
    )
    base.expect_failure_matching(
        "H0 provider transport feature expansion",
        "direct dependency contract drifted",
        _validate_cargo_toml,
        bad_manifest,
    )


def _selftest_initial_implementation_surface() -> None:
    base_files = {POLICY_SCRIPT: b"canonical-policy"}
    candidate_files = dict(base_files)
    candidate_files.update(
        {
            CARGO_TOML_PATH: _manifest_fixture_bytes(),
            CARGO_LOCK_PATH: b"synthetic-lock-not-used-for-positive-validation\n",
            CARGO_CONFIG_PATH: EXPECTED_CARGO_CONFIG,
            LIB_RS_PATH: b"#![forbid(unsafe_code)]\n",
            IMPLEMENTATION_ROOT + "src/canonical.rs": b"",
            IMPLEMENTATION_ROOT + "src/identity.rs": b"",
        }
    )
    _require_implementation_stage_order(
        set(H0_013_INITIAL_PATHS),
        base.MemoryView(candidate_files),
        base.MemoryView(base_files),
    )
    unknown = set(H0_013_INITIAL_PATHS) | {IMPLEMENTATION_ROOT + "src/extra.rs"}
    extra = sorted(unknown - set(IMPLEMENTATION_PATHS))
    if extra != [IMPLEMENTATION_ROOT + "src/extra.rs"]:
        base.fail(f"H0 unauthorized-path self-test drifted: {extra}")


def _selftest_authority_boundaries() -> None:
    expected = {
        "H0_SCREEN_IMPLEMENTATION_AUTHORIZED": "NO_UNTIL_H0_012_CANONICAL_ACTIVATION",
        "PRODUCT_HARNESS_INTEGRATION": "NO",
        "H0_CONFIRMATORY_EXECUTION": "NO",
        "HARBOR_ADMISSION": "NONE",
        "PROVIDER_SDK_ADMISSION": "NONE",
        "CLOUD_SDK_ADMISSION": "NONE",
        "DISTRIBUTED_SCHEDULER_ADMISSION": "NONE",
        "ROADMAP_MUTATION": "NONE",
        "S1_013_PLUS": "NOT_STARTED",
    }
    actual = {
        "H0_SCREEN_IMPLEMENTATION_AUTHORIZED": H0_SCREEN_IMPLEMENTATION_AUTHORIZED,
        "PRODUCT_HARNESS_INTEGRATION": PRODUCT_HARNESS_INTEGRATION,
        "H0_CONFIRMATORY_EXECUTION": H0_CONFIRMATORY_EXECUTION,
        "HARBOR_ADMISSION": HARBOR_ADMISSION,
        "PROVIDER_SDK_ADMISSION": PROVIDER_SDK_ADMISSION,
        "CLOUD_SDK_ADMISSION": CLOUD_SDK_ADMISSION,
        "DISTRIBUTED_SCHEDULER_ADMISSION": DISTRIBUTED_SCHEDULER_ADMISSION,
        "ROADMAP_MUTATION": ROADMAP_MUTATION,
        "S1_013_PLUS": S1_013_PLUS,
    }
    if actual != expected:
        base.fail(f"H0 implementation authority boundary drifted: {actual}")


def _selftest_steady_state_wrapper() -> None:
    root = Path(__file__).resolve().parents[2]
    view = base.LocalRepositoryView(root)
    policy_bytes = view.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES)
    base_view = base.MemoryView({POLICY_SCRIPT: policy_bytes})
    if _is_bootstrap_base(base_view):
        base.fail("H0 implementation steady-state self-test misclassified base")
    mutated = base.MemoryView({POLICY_SCRIPT: policy_bytes + b"\n# drift\n"})
    base.expect_failure_matching(
        "H0 implementation wrapper refreeze",
        "steady-state policy wrapper changed",
        _verify_extension_paths_h0_implementation,
        mutated,
        base_view,
        frozenset({POLICY_SCRIPT}),
    )


def selftest() -> None:
    _activate_implementation_contract()
    prior.selftest()
    _install_h0_implementation_policy()
    _selftest_workflow_binding()
    _selftest_bootstrap_delta()
    _selftest_manifest_contract()
    _selftest_initial_implementation_surface()
    _selftest_authority_boundaries()
    _selftest_steady_state_wrapper()
    if len(IMPLEMENTATION_PATHS) != 22:
        base.fail(f"H0 implementation path set drifted: {len(IMPLEMENTATION_PATHS)}")
    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )
    print("wepld Harness H0 implementation integrity policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1
    _install_h0_implementation_policy()
    return prior.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
