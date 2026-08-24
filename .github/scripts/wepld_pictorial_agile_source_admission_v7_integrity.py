#!/usr/bin/env python3
"""Canonical source-only admission for the exact pinned Pictorial + Agile snapshot.

This is repository CI/evidence-policy machinery, not Trusted Core runtime.
It authorizes exactly one already-built, content-addressed source snapshot and
keeps donor execution, dependency/runtime admission, H0, and model authority
closed.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_pictorial_agile_source_admission_v7_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_contract_notice_provenance_repair_v6_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "e91584dd7824af6804a9686ecf99e8c3c0a5856a"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
CONTRACT_PATH = "docs/acquisition/WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"
CONTRACT_GIT_BLOB_SHA1 = "05e58e331fa6a119227127cb146e135f5b9789b7"

PICTORIAL_UPSTREAM_REVISION = "56f44523f76efdcec813e67b38ee550e49b16f48"
PICTORIAL_UPSTREAM_TREE = "3626999bc9c8be4d31f3028c37c74cf544576d15"
AGILE_UPSTREAM_REVISION = "27f50f7e6b618ea14d74dd4037f9e7c60218b16c"
AGILE_UPSTREAM_TREE = "5622442d5ff74d21b2cb4349f255d08380f3d69d"

EXPECTED_SOURCE_HEAD = "e637aa0b2427a9f2ed793d50f738106cee0f4ec1"
EXPECTED_SOURCE_TREE = "60d75b98de30c9e9e1792898160f2a56c9955649"
BASE_ACQUISITION_TREE = "02484292cbf6ff97bf88da03ae0079ba2245e6c7"
SOURCE_ACQUISITION_TREE = "2548a300d96a31506cc2008ef38dabb22bc79d2d"
SOURCE_VENDOR_TREE = "4c5259bd1d0fdbdd827d433f01767686ff418cc0"
SOURCE_PICTORIAL_TREE = "066be2ce78c19d1830b8a8e76ea3afeaa85bb2ff"
SOURCE_AGILE_TREE = "6248b8de14bb49cb70ebe51838c5e0564ebbf3cf"
SOURCE_LEGAL_TREE = "9b65277fa56081435196f21e1c6e5f8e9130a0a5"
SOURCE_LEGAL_THIRD_PARTY_TREE = "959d26daa7f8a872aee8710a25a4afb017a40c8c"
SOURCE_MAPS_TREE = "34fbb6a69a9e4dfa03ed20cc0f94d9814883ad58"
SOURCE_TOOLS_TREE = "444f9361eb3d204231f18e9148d073a01e04df3d"

SOURCE_ARTIFACT_BLOBS = {
    "docs/acquisition/WEPLD_PICTORIAL_AGILE_COMMITTED_TREE_RESTORE_EVIDENCE_2026-08-23.json": "581cb047a9553b0b309a32226773c7bc77211cb1",
    "docs/acquisition/WEPLD_PICTORIAL_AGILE_INDEX_EXACT_SET_EVIDENCE_2026-08-23.json": "bcbd761289f8abcfb835c49f5100e02f846207bf",
    "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_REPORT_2026-08-23.md": "f099f2414b20590ff32fc3301044e1da0f1d7b05",
    "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_SURFACE_INVENTORY_2026-08-23.json": "8ed19c529affb00665df06ff2e170c51a045d5e9",
    "docs/acquisition/source-maps/agile-source-map-2026-08-23.jsonl": "c4fd14524467ebe457bb7196eba64df9f5e364c5",
    "docs/acquisition/source-maps/pictorial-source-map-2026-08-23.jsonl": "c869686f0b97ee1660879b8ff82072952ec96d6c",
    "docs/acquisition/tools/.gitignore": "43ae0e2a6c6d8fca34872506ca0f2e64194fec7c",
    "docs/acquisition/tools/import_pictorial_agile_source_snapshot.py": "e93df85e1d5ae7161c7039493d8cefbd885f082c",
    "docs/acquisition/tools/repair_pictorial_agile_rebrand.py": "9c84a9819b4a0b4bec7655f988355340d9fc5003",
    "docs/acquisition/tools/repair_pictorial_agile_rebrand_stdlib.py": "d9f06c2c494ecdf47572a453df327b271e6fc99d",
    "docs/acquisition/tools/restore_source_map_missing_outputs.py": "7d2d7c3e4329510f5ef1da62e6e02166a3beb0e5",
    "legal/third-party/AGILE_LICENSE.txt": "28a50fa22639e32febe14e4ffc7a732b0ba8c90a",
    "legal/third-party/AGILE_MODIFICATIONS.md": "ef6708db5289b2d5ed6373fb1b78d465e6af2781",
    "legal/third-party/PICTORIAL_LICENSE.txt": "bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9",
    "legal/third-party/PICTORIAL_MODIFICATIONS.md": "dbb8e6a455872f9af12f4ec24f8de0f11e840df0",
    "legal/third-party/PICTORIAL_NOTICE.md": "0468271c904ae334cfaf27da6f8df3d5f419a1f0",
}
MAX_SOURCE_ARTIFACT_BYTES = 3_000_000

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "940bb8b57c5eba27c9e3f2dde21e3728968a7783a52aa2e3ed7e8ad1f2c100c4",
    ADMISSION_WORKFLOW: "67e216ed07d47ea2cbbd2f6039869ae6617a9cfb8446d9916b4a4a9543ec0589",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "0eadccff79f8cbd296230c353f3c0735d4c54a28a05689ba9bac99c1e2600491",
    ADMISSION_WORKFLOW: "5860ad868a62a63a97a29cf70b352c4e26c72a6ee81a3fbd4ce848253db7ecc5",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset({POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
VENDOR_PREFIXES = ("vendor/pictorial/", "vendor/agile/")

SOURCE_IMPORT_AUTHORITY = "EXACT_PINNED_PICTORIAL_AGILE_SOURCE_SNAPSHOT"
SOURCE_ADMISSION = "EXACT_SOURCE_ONLY"
DEPENDENCY_ADMISSION = "NONE"
DONOR_WORKFLOW_EXECUTION = "NONE"
DONOR_HOOK_EXECUTION = "NONE"
DONOR_INSTALL_SCRIPT_EXECUTION = "NONE"
PRODUCT_IMPLEMENTATION_AUTHORITY = "NONE"
PRODUCT_RUNTIME_ADMISSION = "NONE"
ROADMAP_MUTATION = "NONE"
H0_014_PLUS = "NOT_STARTED"
H0_SCREEN_EXECUTION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(files, trees={path: _git_blob_sha1(data) for path, data in files.items()})


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"Pictorial/Agile source-admission-v7 {label} topology is malformed: expected path set")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"Pictorial/Agile source-admission-v7 {label} topology is malformed: non-string path")
    return frozenset(value)


def _bind_prior_policy_before_import() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile repair-v6 policy drifted before import: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_policy_before_import()
import wepld_pictorial_agile_contract_notice_provenance_repair_v6_integrity as prior  # noqa: E402

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_repair
PRIOR_COMPARE_BASE_CONTROLLED = prior._compare_base_controlled_repair
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_repair
PRIOR_VERIFY_EXTENSION_PATHS = prior._verify_extension_paths
PRIOR_VERIFY_POLICY_FILES = prior._verify_policy_files
PRIOR_VALIDATE_ENTRIES = base.validate_entries

_INSTALLED = False
_PRIOR_PRINT_SUCCESS = None


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        topology = prior._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v7 inherited topology is missing or malformed: {exc}")
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("Pictorial/Agile source-admission-v7 inherited topology is malformed")
    return topology


def _activate_predecessor() -> None:
    try:
        current = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v7 predecessor workflow topology is malformed: {exc}")
    if current not in (dict(PRIOR_EXPECTED_WORKFLOW_SHA256), dict(EXPECTED_WORKFLOW_SHA256)):
        base.fail("Pictorial/Agile source-admission-v7 predecessor workflow hashes drifted")
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    try:
        prior._install_policy()
        prior._require_overlay_identity()
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v7 predecessor activation is malformed: {exc}")


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if PRIOR_POLICY_PATH not in paths:
        base.fail("Pictorial/Agile source-admission-v7 requires canonical repair-v6 predecessor")
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile source-admission-v7 predecessor policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    if CONTRACT_PATH not in paths:
        base.fail("canonical Pictorial/Agile contract is missing")
    contract = _git_blob_sha1(view.read_bytes(CONTRACT_PATH, base.MAX_POLICY_FILE_BYTES))
    if contract != CONTRACT_GIT_BLOB_SHA1:
        base.fail(
            "canonical Pictorial/Agile contract drifted: "
            f"expected={CONTRACT_GIT_BLOB_SHA1} actual={contract}"
        )


def _is_source_path(path: str) -> bool:
    return path in SOURCE_ARTIFACT_BLOBS or path.startswith(VENDOR_PREFIXES)


def _snapshot_present(view: base.RepositoryView) -> bool:
    return any(entry.path.startswith(VENDOR_PREFIXES) for entry in view.entries())


def _validate_entries_source(entries: Iterable[base.TrackedEntry]) -> set[str]:
    paths: list[str] = []
    for entry in entries:
        if entry.mode == "120000":
            base.fail(f"symbolic link is prohibited: {entry.path}")
        if entry.mode == "160000":
            base.fail(f"gitlink/submodule is prohibited: {entry.path}")
        if entry.mode == "100755":
            if not entry.path.startswith(VENDOR_PREFIXES):
                base.fail(f"executable mode is permitted only inside frozen Pictorial/Agile vendor source: {entry.path}")
        elif entry.mode != "100644":
            base.fail(f"unexpected tracked mode {entry.mode}: {entry.path}")
        if "\\" in entry.path:
            base.fail(f"backslash in tracked path is prohibited: {entry.path}")
        pure = PurePosixPath(entry.path)
        if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
            base.fail(f"unsafe tracked path: {entry.path}")
        paths.append(entry.path)

    if len(paths) != len(set(paths)):
        base.fail("duplicate tracked path detected")
    folded = [path.casefold() for path in paths]
    if len(folded) != len(set(folded)):
        base.fail("case-insensitive duplicate tracked path detected")
    return set(paths)


def _require_tree(view: base.RepositoryView, path: str, expected: str) -> None:
    actual = view.tree_identity(path)
    if actual != expected:
        base.fail(f"Pictorial/Agile frozen subtree drifted: {path}: expected={expected} actual={actual}")


def _verify_artifact_blobs(view: base.RepositoryView) -> None:
    paths = _paths(view)
    missing = sorted(set(SOURCE_ARTIFACT_BLOBS) - paths)
    if missing:
        base.fail("Pictorial/Agile source-admission artifact missing: " + ", ".join(missing))
    for path, expected in SOURCE_ARTIFACT_BLOBS.items():
        data = view.read_bytes(path, MAX_SOURCE_ARTIFACT_BYTES)
        actual = _git_blob_sha1(data)
        if actual != expected:
            base.fail(
                "Pictorial/Agile source-admission artifact blob drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _verify_snapshot(view: base.RepositoryView, *, transition: bool) -> None:
    _require_tree(view, "vendor", SOURCE_VENDOR_TREE)
    _require_tree(view, "vendor/pictorial", SOURCE_PICTORIAL_TREE)
    _require_tree(view, "vendor/agile", SOURCE_AGILE_TREE)
    _require_tree(view, "docs/acquisition/source-maps", SOURCE_MAPS_TREE)
    _require_tree(view, "docs/acquisition/tools", SOURCE_TOOLS_TREE)
    _require_tree(view, "legal", SOURCE_LEGAL_TREE)
    _require_tree(view, "legal/third-party", SOURCE_LEGAL_THIRD_PARTY_TREE)
    if transition:
        _require_tree(view, "docs/acquisition", SOURCE_ACQUISITION_TREE)
    contract = _git_blob_sha1(view.read_bytes(CONTRACT_PATH, base.MAX_POLICY_FILE_BYTES))
    if contract != CONTRACT_GIT_BLOB_SHA1:
        base.fail("Pictorial/Agile source admission requires the exact canonical contract")
    _verify_artifact_blobs(view)


def _delegate_exact_delta(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    try:
        delegated = prior._require_exact_delta_repair
    except AttributeError as exc:
        base.fail(f"Pictorial/Agile source-admission-v7 inherited exact-delta topology is missing: {exc}")
    if delegated is not PRIOR_REQUIRE_EXACT_DELTA or not callable(delegated):
        base.fail("Pictorial/Agile source-admission-v7 inherited exact-delta delegate drifted")
    try:
        delegated(candidate, policy_base)
    except TypeError as exc:
        base.fail(f"Pictorial/Agile source-admission-v7 inherited exact-delta topology is malformed: {exc}")


def _require_exact_delta_source(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, impl, _, _ = _topology()
    try:
        changed = _require_path_set(impl._changed_paths(candidate, policy_base), "changed-path")
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v7 changed-path topology is malformed: {exc}")

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            if _snapshot_present(candidate):
                base.fail("Pictorial/Agile source snapshot cannot be admitted during v7 bootstrap")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "Pictorial/Agile source-admission-v7 bootstrap delta must be exactly "
                "the v7 policy plus two workflows"
            )
        if any(_is_source_path(path) for path in changed):
            base.fail("Pictorial/Agile source snapshot cannot transition before v7 activation")
        _delegate_exact_delta(candidate, policy_base)
        return

    source_changed = frozenset(path for path in changed if _is_source_path(path))
    if source_changed:
        if _snapshot_present(policy_base):
            base.fail("canonical Pictorial/Agile source snapshot is frozen after admission")
        unexpected = sorted(changed - source_changed)
        if unexpected:
            base.fail(
                "Pictorial/Agile source-admission transition contains unrelated paths: "
                + ", ".join(unexpected)
            )
        if policy_base.tree_identity("docs/acquisition") != BASE_ACQUISITION_TREE:
            base.fail(
                "Pictorial/Agile source-admission trusted-base acquisition tree drifted: "
                f"expected={BASE_ACQUISITION_TREE} actual={policy_base.tree_identity('docs/acquisition')}"
            )
        _verify_snapshot(candidate, transition=True)
        return

    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_source(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
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
                    f"Pictorial/Agile source-admission-v7 workflow candidate drifted: {relative}: "
                    f"expected={expected_candidate} actual={actual_candidate}"
                )
            expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
            actual_base = _sha256(base_bytes)
            if actual_base != expected_base:
                base.fail(
                    f"Pictorial/Agile source-admission-v7 trusted-base workflow drifted: {relative}: "
                    f"expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(f"Pictorial/Agile source-admission-v7 steady-state workflow changed: {relative}")
            continue
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    base_has_snapshot = _snapshot_present(policy_base)
    candidate_has_snapshot = _snapshot_present(candidate)
    if base_has_snapshot:
        if not candidate_has_snapshot:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        _verify_snapshot(policy_base, transition=False)
        _verify_snapshot(candidate, transition=False)
    elif candidate_has_snapshot:
        if policy_base.tree_identity("docs/acquisition") != BASE_ACQUISITION_TREE:
            base.fail("source-admission trusted-base acquisition identity drifted")
        _verify_snapshot(candidate, transition=True)


def _verify_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView, controlled: frozenset[str]) -> None:
    safe_controlled = _require_path_set(controlled, "extension-controlled-path")
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in safe_controlled:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Pictorial/Agile source-admission-v7 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Pictorial/Agile source-admission-v7 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Pictorial/Agile source-admission-v7 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES):
                base.fail("Pictorial/Agile source-admission-v7 steady-state wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & safe_controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        expected_candidate = EXPECTED_WORKFLOW_SHA256[relative]
        if _sha256(candidate_bytes) != expected_candidate:
            base.fail(f"Pictorial/Agile source-admission-v7 controlled workflow candidate drifted: {relative}")
        expected_base = PRIOR_EXPECTED_WORKFLOW_SHA256[relative] if bootstrap else expected_candidate
        if _sha256(base_bytes) != expected_base:
            base.fail(f"Pictorial/Agile source-admission-v7 controlled workflow base drifted: {relative}")
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"Pictorial/Agile source-admission-v7 controlled workflow changed: {relative}")

    delegated = frozenset(safe_controlled - {POLICY_SCRIPT} - BOOTSTRAP_WORKFLOWS)
    if delegated:
        verifier = prior._verify_extension_paths
        if verifier is not PRIOR_VERIFY_EXTENSION_PATHS or not callable(verifier):
            base.fail("Pictorial/Agile source-admission-v7 inherited extension verifier drifted")
        verifier(candidate, policy_base, delegated)


def _verify_execution_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths(candidate, policy_base, _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension"))


def _verify_desktop_extension_paths(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths(candidate, policy_base, _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension"))


def _validate_allowed_paths_source(paths: set[str], stage: str) -> None:
    projected = {path for path in paths if not _is_source_path(path)}
    delegated = prior._validate_allowed_paths_repair
    if delegated is not PRIOR_VALIDATE_ALLOWED_PATHS or not callable(delegated):
        base.fail("Pictorial/Agile source-admission-v7 inherited allowlist delegate drifted")
    delegated(projected, stage)


def _verify_policy_files(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(f"frozen Pictorial/Agile repair-v6 predecessor policy drifted: {actual}")
    verifier = prior._verify_policy_files
    if verifier is not PRIOR_VERIFY_POLICY_FILES or not callable(verifier):
        base.fail("Pictorial/Agile source-admission-v7 inherited policy-file verifier drifted")
    verifier(view)


def _require_prebind_identity(shell: Any, retention: Any, desktop: Any, execution: Any) -> None:
    expected = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, prior._require_exact_delta_repair, "exact-delta"),
        (base.compare_base_controlled, prior._compare_base_controlled_repair, "base-control"),
        (base.validate_entries, PRIOR_VALIDATE_ENTRIES, "tracked-mode"),
        (desktop.verify_extension_controlled_paths, prior._verify_desktop_extension_paths, "desktop-extension"),
        (execution.verify_extension_controlled_paths, prior._verify_execution_extension_paths, "execution-extension"),
        (shell.validate_allowed_paths, prior._validate_allowed_paths_repair, "tracked-path"),
        (shell.verify_policy_files, prior._verify_policy_files, "policy-file"),
        (shell.print_success, prior._print_success, "success-printer"),
    )
    for actual, wanted, label in expected:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile source-admission-v7 pre-bind {label} hook drifted")


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    checks = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, _require_exact_delta_source, "exact-delta"),
        (base.compare_base_controlled, _compare_base_controlled_source, "base-control"),
        (base.validate_entries, _validate_entries_source, "tracked-mode"),
        (desktop.verify_extension_controlled_paths, _verify_desktop_extension_paths, "desktop-extension"),
        (execution.verify_extension_controlled_paths, _verify_execution_extension_paths, "execution-extension"),
        (shell.validate_allowed_paths, _validate_allowed_paths_source, "tracked-path"),
        (shell.verify_policy_files, _verify_policy_files, "policy-file"),
        (shell.print_success, _print_success, "success-printer"),
    )
    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile source-admission-v7 {label} hook drifted")

    retention._require_exact_delta_hook_identity(retention._require_exact_delta_retention, "pictorial-agile-source-admission-v7-overlay")
    if POLICY_SCRIPT not in desktop.EXTENSION_CONTROLLED_PATHS:
        base.fail("Pictorial/Agile source-admission-v7 desktop path registration drifted")
    if POLICY_SCRIPT not in execution.EXTENSION_CONTROLLED_PATHS:
        base.fail("Pictorial/Agile source-admission-v7 execution path registration drifted")
    if _PRIOR_PRINT_SUCCESS is None or _PRIOR_PRINT_SUCCESS is not prior._print_success:
        base.fail("Pictorial/Agile source-admission-v7 prior success-printer drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("Pictorial/Agile source-admission-v7 prior success printer is unavailable")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"pictorial_agile_source_admission_v7_authority={SOURCE_IMPORT_AUTHORITY}")
    print(f"effective_source_admission={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission={DEPENDENCY_ADMISSION}")
    print(f"effective_donor_workflow_execution={DONOR_WORKFLOW_EXECUTION}")
    print(f"effective_donor_hook_execution={DONOR_HOOK_EXECUTION}")
    print(f"effective_donor_install_script_execution={DONOR_INSTALL_SCRIPT_EXECUTION}")
    print(f"effective_product_runtime_admission={PRODUCT_RUNTIME_ADMISSION}")
    print(f"effective_h0_014_plus={H0_014_PLUS}")
    print(f"effective_h0_screen_execution={H0_SCREEN_EXECUTION}")
    print(f"effective_model_provider_execution={MODEL_PROVIDER_EXECUTION}")
    print(f"effective_model_weight_access={MODEL_WEIGHT_ACCESS}")
    print(f"effective_model_inference={MODEL_INFERENCE}")


def _install_policy() -> None:
    global _INSTALLED, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        _require_overlay_identity()
        return

    _activate_predecessor()
    shell, retention, _, desktop, execution = _topology()
    _require_prebind_identity(shell, retention, desktop, execution)

    desktop_paths = _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension")
    execution_paths = _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension")
    if not callable(prior._print_success):
        base.fail("Pictorial/Agile source-admission-v7 predecessor success printer is not callable")

    _PRIOR_PRINT_SUCCESS = prior._print_success
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_source
    base.compare_base_controlled = _compare_base_controlled_source
    base.validate_entries = _validate_entries_source
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(desktop_paths | {POLICY_SCRIPT})
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(execution_paths | {POLICY_SCRIPT})
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths
    shell.validate_allowed_paths = _validate_allowed_paths_source
    shell.verify_policy_files = _verify_policy_files
    shell.print_success = _print_success

    _INSTALLED = True
    _require_overlay_identity()


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != EXPECTED_WORKFLOW_SHA256[path]:
            base.fail(f"Pictorial/Agile source-admission-v7 workflow drifted: {path}: expected={EXPECTED_WORKFLOW_SHA256[path]} actual={actual}")


def _selftest_modes() -> None:
    _validate_entries_source([
        base.TrackedEntry(mode="100644", path="README.md"),
        base.TrackedEntry(mode="100755", path="vendor/agile/bin/tool.sh"),
        base.TrackedEntry(mode="100755", path="vendor/pictorial/scripts/tool.sh"),
    ])
    base.expect_failure_matching("source-admission-v7 executable outside vendor", "executable mode is permitted only", _validate_entries_source, [base.TrackedEntry(mode="100755", path="scripts/tool.sh")])
    base.expect_failure_matching("source-admission-v7 symlink rejection", "symbolic link is prohibited", _validate_entries_source, [base.TrackedEntry(mode="120000", path="vendor/agile/link")])
    base.expect_failure_matching("source-admission-v7 gitlink rejection", "gitlink/submodule is prohibited", _validate_entries_source, [base.TrackedEntry(mode="160000", path="vendor/pictorial/submodule")])


def _bootstrap_views() -> tuple[base.MemoryView, base.MemoryView]:
    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    base_files = {
        PRIOR_POLICY_PATH: local.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES),
        CONTRACT_PATH: local.read_bytes(CONTRACT_PATH, base.MAX_POLICY_FILE_BYTES),
        FOUNDATION_WORKFLOW: b"old-f",
        ADMISSION_WORKFLOW: b"old-a",
    }
    candidate = dict(base_files)
    candidate.update({POLICY_SCRIPT: b"policy", FOUNDATION_WORKFLOW: b"new-f", ADMISSION_WORKFLOW: b"new-a"})
    return _memory_view(candidate), _memory_view(base_files)


def _selftest_deltas() -> None:
    candidate, policy_base = _bootstrap_views()
    _require_exact_delta_source(candidate, policy_base)
    mixed = {entry.path: candidate.read_bytes(entry.path, base.MAX_POLICY_FILE_BYTES) for entry in candidate.entries()}
    mixed["vendor/pictorial/unexpected.sh"] = b"x"
    base.expect_failure_matching("source-admission-v7 mixed bootstrap/source rejection", "bootstrap delta must be exactly", _require_exact_delta_source, _memory_view(mixed), policy_base)


def _selftest_tree_binding() -> None:
    trees = {"vendor": SOURCE_VENDOR_TREE, "vendor/pictorial": SOURCE_PICTORIAL_TREE, "vendor/agile": SOURCE_AGILE_TREE}
    view = base.MemoryView({"vendor/pictorial/a": b"a", "vendor/agile/b": b"b"}, trees=trees)
    _require_tree(view, "vendor", SOURCE_VENDOR_TREE)
    _require_tree(view, "vendor/pictorial", SOURCE_PICTORIAL_TREE)
    _require_tree(view, "vendor/agile", SOURCE_AGILE_TREE)
    bad = base.MemoryView({"vendor/pictorial/a": b"a", "vendor/agile/b": b"b"}, trees={**trees, "vendor/agile": "0" * 40})
    base.expect_failure_matching("source-admission-v7 wrong Agile subtree", "frozen subtree drifted", _require_tree, bad, "vendor/agile", SOURCE_AGILE_TREE)


def _selftest_constants() -> None:
    if len(SOURCE_ARTIFACT_BLOBS) != 16 or len(set(SOURCE_ARTIFACT_BLOBS)) != 16:
        base.fail("Pictorial/Agile source-admission-v7 artifact set must contain exactly 16 unique paths")
    for path, sha in SOURCE_ARTIFACT_BLOBS.items():
        if not path or not base.OBJECT_SHA_RE.fullmatch(sha):
            base.fail(f"Pictorial/Agile source-admission-v7 malformed artifact identity: {path}")
    if PICTORIAL_UPSTREAM_REVISION != "56f44523f76efdcec813e67b38ee550e49b16f48" or PICTORIAL_UPSTREAM_TREE != "3626999bc9c8be4d31f3028c37c74cf544576d15":
        base.fail("Pictorial identity drifted")
    if AGILE_UPSTREAM_REVISION != "27f50f7e6b618ea14d74dd4037f9e7c60218b16c" or AGILE_UPSTREAM_TREE != "5622442d5ff74d21b2cb4349f255d08380f3d69d":
        base.fail("Agile identity drifted")
    if DEPENDENCY_ADMISSION != "NONE" or PRODUCT_RUNTIME_ADMISSION != "NONE":
        base.fail("Pictorial/Agile source-admission-v7 widened runtime/dependency authority")


def _selftest_identity_drift() -> None:
    original = prior._print_success
    prior._print_success = lambda stage, mode: None
    try:
        base.expect_failure_matching("source-admission-v7 rebound prior success printer", "prior success-printer drifted", _require_overlay_identity)
    finally:
        prior._print_success = original
    _require_overlay_identity()


def selftest() -> None:
    try:
        current = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v7 predecessor selftest binding is malformed: {exc}")
    if current not in (dict(PRIOR_EXPECTED_WORKFLOW_SHA256), dict(EXPECTED_WORKFLOW_SHA256)):
        base.fail("Pictorial/Agile source-admission-v7 predecessor selftest workflow hashes drifted")
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior.selftest()

    _install_policy()
    _selftest_workflows()
    _selftest_modes()
    _selftest_deltas()
    _selftest_tree_binding()
    _selftest_constants()
    _selftest_identity_drift()

    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    _require_prior_policy_base(local)
    _, _, impl, _, _ = _topology()
    if base.REPOSITORY != impl.CANONICAL_REPOSITORY:
        base.fail("canonical repository identity drifted")
    print("wepld Pictorial/Agile source admission v7 self-tests: PASS")


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
                runner = prior._verify_local_with_remote_policy_base
                if not callable(runner):
                    base.fail("Pictorial/Agile source-admission-v7 trusted-base local runner is not callable")
                return runner(args, shell, impl)
        runner = retention.main
        if not callable(runner):
            base.fail("Pictorial/Agile source-admission-v7 runtime main is not callable")
        return runner(argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
