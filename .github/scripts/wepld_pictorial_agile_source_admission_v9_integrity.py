#!/usr/bin/env python3
"""Content-addressed Pictorial lock-metadata overlay policy candidate v9.

v9 preserves the canonical v8 Pictorial + Agile exact pinned source snapshot as
immutable provenance and adds exactly one bounded WePLD-owned metadata overlay:
`vendor/pictorial/bun.lock` may transition from one exact original Git blob to
one exact repaired Git blob on one exact predecessor->candidate commit lineage.

No dependency admission, package execution, donor execution, product runtime,
H0, provider/model, credential-content, or merge authority is granted here.
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

POLICY_SCRIPT = ".github/scripts/wepld_pictorial_agile_source_admission_v9_integrity.py"
PRIOR_POLICY_PATH = ".github/scripts/wepld_pictorial_agile_source_admission_v8_integrity.py"
EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1 = "1101596adb075fad21340e482d8b152460121e49"

FOUNDATION_WORKFLOW = ".github/workflows/foundation-integrity.yml"
ADMISSION_WORKFLOW = ".github/workflows/s1-admission-integrity.yml"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
EVIDENCE_PATH = "docs/acquisition/WEPLD_PICTORIAL_LOCK_METADATA_OVERLAY_V9_EVIDENCE_2026-08-24.md"
EXPECTED_EVIDENCE_GIT_BLOB_SHA1 = "f065f04e0234d0a4dcbaf90be08b59f677331158"

PRIOR_EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "9f4d321f4a5e8f37c3db31227157db61cf066e4acc4ea4513f12aae691f0067f",
    ADMISSION_WORKFLOW: "83c9e65e67d07fa0788d12d57937b37e18dec2249230575682d3ddd9132c675c",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
EXPECTED_WORKFLOW_SHA256 = {
    FOUNDATION_WORKFLOW: "c88e9c156c4afd70202709efdfc082449182287d930ba6aec79b7f61f60cce39",
    ADMISSION_WORKFLOW: "4eebbfc76a5c967a3e44ac98bc0bfe44166afd056aaa34c9682c6c70e920a2ff",
    CONTRACTS_WORKFLOW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOTSTRAP_WORKFLOWS = frozenset({FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW})
BOOTSTRAP_DELTA_PATHS = frozenset(
    {POLICY_SCRIPT, FOUNDATION_WORKFLOW, ADMISSION_WORKFLOW, EVIDENCE_PATH}
)

LOCK_PATH = "vendor/pictorial/bun.lock"
PACKAGE_JSON_PATH = "vendor/pictorial/package.json"
PREDECESSOR_SOURCE_HEAD = "28f0023b8ffb90c585213762dae5f4c1d57322ef"
PREDECESSOR_SOURCE_TREE = "ed9ee4e0b1065e73909adbb2b4f02a0464ea44fc"
REPAIR_CANDIDATE_HEAD = "04cc279133d536e2b4b68e01c019d7b595f0ed42"
REPAIR_CANDIDATE_TREE = "5397b0f31719703e1f346f41b52bb5cd53bca2f7"
ORIGINAL_VENDOR_TREE = "4c5259bd1d0fdbdd827d433f01767686ff418cc0"
REPAIRED_VENDOR_TREE = "88b58da55a3696feccef89fad3865ce3317fc6fa"
ORIGINAL_PICTORIAL_TREE = "066be2ce78c19d1830b8a8e76ea3afeaa85bb2ff"
REPAIRED_PICTORIAL_TREE = "3416c629e4b972765e0e00d3f6cb0ece56460481"
AGILE_TREE = "6248b8de14bb49cb70ebe51838c5e0564ebbf3cf"
PACKAGE_JSON_BLOB = "ba646522c498af6e9bfa02fd1dba2f098d9f6d42"
ORIGINAL_LOCK_BLOB = "f7114d1b93f26eb9d7796fc15ae3d639d2209c9d"
REPAIRED_LOCK_BLOB = "0045fb246c6ffac5375f7272f4f88b3dd7ef53d6"
REPAIRED_LOCK_SHA256 = "92d73b6b1c491fd9c800c0243d6652b4287a4edd625d34ea5fd3af99021d3733"
REPAIRED_CYCLONEDX_SHA256 = "4999c6af6eba6f6eefaebdc325ccf9d57a4cb837f75bbda5bb4a88a5244255de"
REPAIRED_OSV_RESPONSE_SHA256 = "c955b897cd3c3d7469c43716f9e54bbe6aff48d68d0fc8da47ee5f0f219e16a4"

SOURCE_IMPORT_AUTHORITY = "EXACT_PINNED_PICTORIAL_AGILE_SOURCE_SNAPSHOT_PLUS_ONE_CONTENT_ADDRESSED_LOCK_METADATA_OVERLAY"
SOURCE_ADMISSION = "EXACT_SOURCE_PLUS_ONE_BOUND_LOCK_METADATA_OVERLAY"
DEPENDENCY_ADMISSION = "NONE"
PACKAGE_INSTALLATION = "NONE"
PACKAGE_IMPORT_OR_EXECUTION = "NONE"
DONOR_CODE_EXECUTION = "NONE"
DONOR_WORKFLOW_EXECUTION = "NONE"
DONOR_HOOK_EXECUTION = "NONE"
DONOR_INSTALL_SCRIPT_EXECUTION = "NONE"
DONOR_PARITY_TEST_EXECUTION = "NONE"
DONOR_LIVE_TEST_EXECUTION = "NONE"
PRODUCT_IMPLEMENTATION_AUTHORITY = "NONE"
PRODUCT_RUNTIME_ADMISSION = "NONE"
ROADMAP_MUTATION = "NONE"
H0_014_PLUS = "NOT_STARTED"
H0_SCREEN_EXECUTION = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
MODEL_WEIGHT_ACCESS = "NONE"
MODEL_INFERENCE = "NONE"
CREDENTIAL_CONTENT_ACCESS = "NONE"
CANONICAL_POLICY_MERGE = "NOT_AUTHORIZED"
PR136_SOURCE_HEAD_REPLACEMENT = "NOT_AUTHORIZED"
PR162_MERGE = "NOT_AUTHORIZED"
PR136_MERGE = "NOT_AUTHORIZED"

_INSTALLED = False
_PRIOR_PRINT_SUCCESS: Any = None
_LOCAL_REMOTE_CLIENT: Any = None


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _paths(view: base.RepositoryView) -> set[str]:
    return {entry.path for entry in view.entries()}


def _require_path_set(value: Any, label: str) -> frozenset[str]:
    if not isinstance(value, (set, frozenset)):
        base.fail(f"Pictorial/Agile source-admission-v9 {label} topology is malformed")
    if any(not isinstance(path, str) for path in value):
        base.fail(f"Pictorial/Agile source-admission-v9 {label} contains non-string path")
    return frozenset(value)


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

PRIOR_REQUIRE_EXACT_DELTA = prior._require_exact_delta_v8
PRIOR_COMPARE_BASE_CONTROLLED = prior._compare_base_controlled_v8
PRIOR_VALIDATE_ALLOWED_PATHS = prior._validate_allowed_paths_v8
PRIOR_VERIFY_EXTENSION_PATHS = prior._verify_extension_paths_v8
PRIOR_VERIFY_POLICY_FILES = prior._verify_policy_files_v8
PRIOR_DESKTOP_VERIFY_EXTENSION_PATHS = prior._verify_desktop_extension_paths_v8
PRIOR_EXECUTION_VERIFY_EXTENSION_PATHS = prior._verify_execution_extension_paths_v8
PRIOR_VALIDATE_ENTRIES = prior.PRIOR_VALIDATE_ENTRIES
PRIOR_PRINT_SUCCESS = prior._print_success
PRIOR_SNAPSHOT_PRESENT = prior.PRIOR_SNAPSHOT_PRESENT
PRIOR_VERIFY_SNAPSHOT = prior.PRIOR_VERIFY_SNAPSHOT
PRIOR_IS_SOURCE_PATH = prior.PRIOR_IS_SOURCE_PATH


def _topology() -> tuple[Any, Any, Any, Any, Any]:
    try:
        topology = prior._topology()
    except (AttributeError, TypeError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v9 inherited topology malformed: {exc}")
    if not isinstance(topology, tuple) or len(topology) != 5:
        base.fail("Pictorial/Agile source-admission-v9 inherited topology malformed")
    return topology


def _activate_predecessor() -> None:
    try:
        current = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v9 predecessor workflow topology malformed: {exc}")
    if current not in (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    ):
        base.fail("Pictorial/Agile source-admission-v9 predecessor workflow hashes drifted")
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior._install_policy()
    prior._require_overlay_identity()


def _is_bootstrap_base(view: base.RepositoryView) -> bool:
    return POLICY_SCRIPT not in _paths(view)


def _require_prior_policy_base(view: base.RepositoryView) -> None:
    if PRIOR_POLICY_PATH not in _paths(view):
        base.fail("Pictorial/Agile source-admission-v9 requires canonical v8 predecessor")
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile source-admission-v9 base policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )


def _local_blob_map(view: base.LocalRepositoryView) -> dict[str, tuple[str, str]]:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(view.root), "ls-files", "--stage", "-z"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        base.fail(f"unable to enumerate local Git blob identities: {exc}")
    result: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode_b, object_b, stage_b = metadata.split(b" ", 2)
            if int(stage_b) != 0:
                base.fail("unmerged index stage is prohibited during v9 overlay comparison")
            path = raw_path.decode("utf-8", errors="strict")
            mode = mode_b.decode("ascii", errors="strict")
            object_id = object_b.decode("ascii", errors="strict").lower()
        except (ValueError, UnicodeError) as exc:
            base.fail(f"malformed local Git index record during v9 overlay comparison: {exc}")
        result[path] = (mode, object_id)
    return result


def _blob_map(view: base.RepositoryView) -> dict[str, tuple[str, str]]:
    if isinstance(view, base.LocalRepositoryView):
        return _local_blob_map(view)
    if isinstance(view, base.RemoteRepositoryView):
        entries = {entry.path: entry.mode for entry in view.entries()}
        raw_blobs = getattr(view, "_blobs", None)
        if not isinstance(raw_blobs, dict):
            base.fail("remote blob topology unavailable for v9 exact-overlay comparison")
        result: dict[str, tuple[str, str]] = {}
        for path, mode in entries.items():
            raw = raw_blobs.get(path)
            if raw is None:
                result[path] = (mode, "")
                continue
            if (
                not isinstance(raw, tuple)
                or len(raw) != 2
                or not isinstance(raw[0], str)
                or not isinstance(raw[1], int)
            ):
                base.fail(f"malformed remote blob identity for {path}")
            result[path] = (mode, raw[0].lower())
        return result

    result = {}
    for entry in view.entries():
        data = view.read_bytes(entry.path, 16_000_000)
        result[entry.path] = (entry.mode, _git_blob_sha1(data))
    return result


def _changed_paths_exact(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> frozenset[str]:
    candidate_map = _blob_map(candidate)
    base_map = _blob_map(policy_base)
    all_paths = set(candidate_map) | set(base_map)
    return frozenset(
        path for path in all_paths if candidate_map.get(path) != base_map.get(path)
    )


def _blob_identity(view: base.RepositoryView, path: str) -> str:
    mapping = _blob_map(view)
    item = mapping.get(path)
    if item is None or not item[1]:
        base.fail(f"required v9 overlay blob identity missing: {path}")
    return item[1]


def _memory_view(files: dict[str, bytes]) -> base.MemoryView:
    return base.MemoryView(
        files,
        trees={path: _git_blob_sha1(data) for path, data in files.items()},
    )


def _local_commit_sha(view: base.LocalRepositoryView) -> str:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(view.root), "rev-parse", "HEAD"],
            stderr=subprocess.STDOUT,
            text=True,
        ).strip().lower()
    except subprocess.CalledProcessError as exc:
        base.fail(f"unable to resolve local v9 commit identity: {exc}")
    if len(raw) != 40 or any(ch not in "0123456789abcdef" for ch in raw):
        base.fail(f"malformed local v9 commit identity: {raw!r}")
    return raw


def _view_commit_sha(view: base.RepositoryView) -> str:
    if isinstance(view, base.RemoteRepositoryView):
        raw = view.commit_sha.lower()
    elif isinstance(view, base.LocalRepositoryView):
        raw = _local_commit_sha(view)
    else:
        base.fail("v9 admission lineage requires local or remote repository view")
    if len(raw) != 40 or any(ch not in "0123456789abcdef" for ch in raw):
        base.fail(f"malformed v9 repository-view commit identity: {raw!r}")
    return raw


def _shared_trusted_client(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> object:
    clients = [view.client for view in (candidate, policy_base) if isinstance(view, base.RemoteRepositoryView)]
    if clients:
        first = clients[0]
        if any(client is not first for client in clients[1:]):
            base.fail("v9 repaired-source admission remote views do not share trusted client")
        return first
    if _LOCAL_REMOTE_CLIENT is None:
        base.fail("v9 repaired-source admission requires trusted remote-baseline client scope")
    return _LOCAL_REMOTE_CLIENT


def _source_surface_map(view: base.RepositoryView) -> dict[str, tuple[str, str]]:
    return {path: identity for path, identity in _blob_map(view).items() if PRIOR_IS_SOURCE_PATH(path)}


def _require_source_surface_equal(actual: dict[str, tuple[str, str]], expected: dict[str, tuple[str, str]], label: str) -> None:
    if actual == expected:
        return
    all_paths = sorted(set(actual) | set(expected))
    drift = [path for path in all_paths if actual.get(path) != expected.get(path)]
    preview = ", ".join(drift[:12])
    suffix = "" if len(drift) <= 12 else f" (+{len(drift) - 12} more)"
    base.fail(f"{label} source surface drifted: {preview}{suffix}")


def _commit_payload(client: object, sha: str, label: str) -> dict[str, Any]:
    payload = client.json(f"https://api.github.com/repos/{base.REPOSITORY}/git/commits/{sha}")
    if not isinstance(payload, dict) or payload.get("sha") != sha:
        base.fail(f"{label} commit API identity drifted")
    return payload


def _parent_shas(payload: dict[str, Any], label: str) -> tuple[str, ...]:
    parents = payload.get("parents")
    if not isinstance(parents, list):
        base.fail(f"{label} parent topology is malformed")
    shas: list[str] = []
    for parent in parents:
        if not isinstance(parent, dict) or not isinstance(parent.get("sha"), str):
            base.fail(f"{label} parent topology is malformed")
        shas.append(parent["sha"].lower())
    return tuple(shas)


def _require_exact_parent_set(payload: dict[str, Any], expected: frozenset[str], label: str) -> None:
    actual = _parent_shas(payload, label)
    if len(actual) != len(expected) or frozenset(actual) != expected:
        base.fail(f"{label} parent lineage drifted: expected={sorted(expected)} actual={list(actual)}")


def _require_initial_admission_path_shape(changed: frozenset[str]) -> None:
    if not changed:
        base.fail("v9 initial repaired-source admission has empty delta")
    unexpected = sorted(path for path in changed if not PRIOR_IS_SOURCE_PATH(path))
    if unexpected:
        base.fail("v9 initial repaired-source admission changed non-source paths: " + ", ".join(unexpected))
    if LOCK_PATH not in changed:
        base.fail("v9 initial repaired-source admission is missing repaired bun.lock")


def _require_initial_repaired_admission(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    changed = _changed_paths_exact(candidate, policy_base)
    _require_initial_admission_path_shape(changed)

    client = _shared_trusted_client(candidate, policy_base)
    reference = base.RemoteRepositoryView(base.REPOSITORY, REPAIR_CANDIDATE_HEAD, client)
    predecessor = base.RemoteRepositoryView(base.REPOSITORY, PREDECESSOR_SOURCE_HEAD, client)
    _require_remote_lineage(reference, predecessor)

    _require_source_surface_equal(_source_surface_map(candidate), _source_surface_map(reference), "v9 initial repaired-source candidate")
    if candidate.tree_identity("vendor") != REPAIRED_VENDOR_TREE:
        base.fail("v9 initial repaired-source vendor tree drifted")
    if candidate.tree_identity("vendor/pictorial") != REPAIRED_PICTORIAL_TREE:
        base.fail("v9 initial repaired-source Pictorial tree drifted")
    if candidate.tree_identity("vendor/agile") != AGILE_TREE:
        base.fail("v9 initial repaired-source Agile tree drifted")
    if _blob_identity(candidate, PACKAGE_JSON_PATH) != PACKAGE_JSON_BLOB:
        base.fail("v9 initial repaired-source package.json drifted")
    lock_bytes = candidate.read_bytes(LOCK_PATH, base.MAX_LOCKFILE_BYTES)
    if _git_blob_sha1(lock_bytes) != REPAIRED_LOCK_BLOB:
        base.fail("v9 initial repaired-source lock Git blob drifted")
    if _sha256(lock_bytes) != REPAIRED_LOCK_SHA256:
        base.fail("v9 initial repaired-source lock SHA-256 drifted")

    policy_sha = _view_commit_sha(policy_base)
    candidate_sha = _view_commit_sha(candidate)
    if isinstance(candidate, base.RemoteRepositoryView):
        payload = _commit_payload(client, candidate_sha, "v9 pre-merge admission candidate")
        _require_exact_parent_set(payload, frozenset({REPAIR_CANDIDATE_HEAD, policy_sha}), "v9 pre-merge admission candidate")
        return

    pushed = _commit_payload(client, candidate_sha, "v9 post-merge pushed head")
    pushed_parents = _parent_shas(pushed, "v9 post-merge pushed head")
    if len(pushed_parents) != 2 or policy_sha not in pushed_parents:
        base.fail("v9 post-merge pushed head must merge trusted policy base with qualified admission candidate")
    admission_sha = next(sha for sha in pushed_parents if sha != policy_sha)
    admission_payload = _commit_payload(client, admission_sha, "v9 qualified admission candidate")
    _require_exact_parent_set(admission_payload, frozenset({REPAIR_CANDIDATE_HEAD, policy_sha}), "v9 qualified admission candidate")
    admission_view = base.RemoteRepositoryView(base.REPOSITORY, admission_sha, client)
    _require_source_surface_equal(_source_surface_map(admission_view), _source_surface_map(reference), "v9 qualified admission candidate")


def _validate_overlay_shape(
    *,
    changed: frozenset[str],
    predecessor_lock_blob: str,
    candidate_lock_blob: str,
    predecessor_package_blob: str,
    candidate_package_blob: str,
) -> None:
    if changed != frozenset({LOCK_PATH}):
        base.fail(
            "Pictorial/Agile v9 overlay delta must be exactly vendor/pictorial/bun.lock; "
            + ", ".join(sorted(changed))
        )
    if predecessor_lock_blob != ORIGINAL_LOCK_BLOB:
        base.fail(
            "Pictorial/Agile v9 overlay predecessor lock drifted: "
            f"expected={ORIGINAL_LOCK_BLOB} actual={predecessor_lock_blob}"
        )
    if candidate_lock_blob != REPAIRED_LOCK_BLOB:
        base.fail(
            "Pictorial/Agile v9 overlay repaired lock drifted: "
            f"expected={REPAIRED_LOCK_BLOB} actual={candidate_lock_blob}"
        )
    if predecessor_package_blob != PACKAGE_JSON_BLOB or candidate_package_blob != PACKAGE_JSON_BLOB:
        base.fail("Pictorial/Agile v9 overlay package.json drifted")


def _require_bound_overlay(
    candidate: base.RepositoryView,
    predecessor: base.RepositoryView,
    *,
    require_remote_lineage: bool,
) -> None:
    if predecessor.tree_identity("vendor") != ORIGINAL_VENDOR_TREE:
        base.fail("Pictorial/Agile v9 predecessor vendor tree drifted")
    if predecessor.tree_identity("vendor/pictorial") != ORIGINAL_PICTORIAL_TREE:
        base.fail("Pictorial/Agile v9 predecessor Pictorial tree drifted")
    if predecessor.tree_identity("vendor/agile") != AGILE_TREE:
        base.fail("Pictorial/Agile v9 predecessor Agile tree drifted")

    PRIOR_VERIFY_SNAPSHOT(predecessor, transition=False)

    changed = _changed_paths_exact(candidate, predecessor)
    _validate_overlay_shape(
        changed=changed,
        predecessor_lock_blob=_blob_identity(predecessor, LOCK_PATH),
        candidate_lock_blob=_blob_identity(candidate, LOCK_PATH),
        predecessor_package_blob=_blob_identity(predecessor, PACKAGE_JSON_PATH),
        candidate_package_blob=_blob_identity(candidate, PACKAGE_JSON_PATH),
    )

    if candidate.tree_identity("vendor") != REPAIRED_VENDOR_TREE:
        base.fail("Pictorial/Agile v9 repaired vendor tree drifted")
    if candidate.tree_identity("vendor/pictorial") != REPAIRED_PICTORIAL_TREE:
        base.fail("Pictorial/Agile v9 repaired Pictorial tree drifted")
    if candidate.tree_identity("vendor/agile") != AGILE_TREE:
        base.fail("Pictorial/Agile v9 repair changed Agile tree")

    lock_bytes = candidate.read_bytes(LOCK_PATH, base.MAX_LOCKFILE_BYTES)
    if _git_blob_sha1(lock_bytes) != REPAIRED_LOCK_BLOB:
        base.fail("Pictorial/Agile v9 repaired lock Git blob does not match bound identity")
    if _sha256(lock_bytes) != REPAIRED_LOCK_SHA256:
        base.fail("Pictorial/Agile v9 repaired lock SHA-256 does not match qualified identity")

    if require_remote_lineage:
        _require_remote_lineage(candidate, predecessor)


def _require_remote_lineage(
    candidate: base.RepositoryView,
    predecessor: base.RepositoryView,
) -> None:
    if not isinstance(candidate, base.RemoteRepositoryView) or not isinstance(
        predecessor, base.RemoteRepositoryView
    ):
        base.fail("Pictorial/Agile v9 remote lineage requires remote repository views")
    if candidate.repository != base.REPOSITORY or predecessor.repository != base.REPOSITORY:
        base.fail("Pictorial/Agile v9 remote lineage repository drifted")
    if candidate.commit_sha != REPAIR_CANDIDATE_HEAD:
        base.fail("Pictorial/Agile v9 repair candidate commit drifted")
    if predecessor.commit_sha != PREDECESSOR_SOURCE_HEAD:
        base.fail("Pictorial/Agile v9 predecessor source commit drifted")
    if candidate.client is not predecessor.client:
        base.fail("Pictorial/Agile v9 remote views do not share the trusted client")

    candidate_commit = candidate.client.json(
        f"https://api.github.com/repos/{candidate.repository}/git/commits/{candidate.commit_sha}"
    )
    if candidate_commit.get("sha") != REPAIR_CANDIDATE_HEAD:
        base.fail("Pictorial/Agile v9 candidate commit API identity drifted")
    tree = candidate_commit.get("tree")
    if not isinstance(tree, dict) or tree.get("sha") != REPAIR_CANDIDATE_TREE:
        base.fail("Pictorial/Agile v9 candidate root tree drifted")
    parents = candidate_commit.get("parents")
    if (
        not isinstance(parents, list)
        or len(parents) != 1
        or not isinstance(parents[0], dict)
        or parents[0].get("sha") != PREDECESSOR_SOURCE_HEAD
    ):
        base.fail("Pictorial/Agile v9 candidate parent lineage drifted")

    predecessor_commit = predecessor.client.json(
        f"https://api.github.com/repos/{predecessor.repository}/git/commits/{predecessor.commit_sha}"
    )
    if predecessor_commit.get("sha") != PREDECESSOR_SOURCE_HEAD:
        base.fail("Pictorial/Agile v9 predecessor commit API identity drifted")
    predecessor_tree = predecessor_commit.get("tree")
    if not isinstance(predecessor_tree, dict) or predecessor_tree.get("sha") != PREDECESSOR_SOURCE_TREE:
        base.fail("Pictorial/Agile v9 predecessor root tree drifted")


def _delegate_exact_delta(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    delegated = prior._require_exact_delta_v8
    if delegated is not PRIOR_REQUIRE_EXACT_DELTA or not callable(delegated):
        base.fail("Pictorial/Agile source-admission-v9 inherited exact-delta delegate drifted")
    delegated(candidate, policy_base)


def _require_exact_delta_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths_exact(candidate, policy_base)

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            if any(PRIOR_IS_SOURCE_PATH(path) for path in changed):
                base.fail("Pictorial/Agile v9 policy bootstrap cannot mutate source")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "Pictorial/Agile source-admission-v9 bootstrap delta must be exactly "
                "the v9 policy, two workflows, and bound evidence record"
            )
        if any(PRIOR_IS_SOURCE_PATH(path) for path in changed):
            base.fail("Pictorial/Agile source cannot transition before v9 is canonical")
        _delegate_exact_delta(candidate, policy_base)
        return

    base_has_snapshot = PRIOR_SNAPSHOT_PRESENT(policy_base)
    candidate_has_snapshot = PRIOR_SNAPSHOT_PRESENT(candidate)
    if not base_has_snapshot and candidate_has_snapshot:
        _require_initial_repaired_admission(candidate, policy_base)
        return

    if changed == frozenset({LOCK_PATH}):
        _require_bound_overlay(
            candidate,
            policy_base,
            require_remote_lineage=(isinstance(candidate, base.RemoteRepositoryView) and isinstance(policy_base, base.RemoteRepositoryView)),
        )
        return

    if any(PRIOR_IS_SOURCE_PATH(path) for path in changed):
        base.fail(
            "Pictorial/Agile source remains frozen after v8 except the exact "
            "v9 repaired-source admission or one bound bun.lock overlay"
        )
    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_v9(
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
                    "Pictorial/Agile source-admission-v9 workflow candidate drifted: "
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
                    "Pictorial/Agile source-admission-v9 trusted-base workflow drifted: "
                    f"{relative}: expected={expected_base} actual={actual_base}"
                )
            if not bootstrap and candidate_bytes != base_bytes:
                base.fail(
                    "Pictorial/Agile source-admission-v9 steady-state workflow changed: "
                    f"{relative}"
                )
            continue
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {relative}")

    base_has_snapshot = PRIOR_SNAPSHOT_PRESENT(policy_base)
    candidate_has_snapshot = PRIOR_SNAPSHOT_PRESENT(candidate)
    if base_has_snapshot:
        if not candidate_has_snapshot:
            base.fail("canonical Pictorial/Agile source snapshot was deleted")
        PRIOR_VERIFY_SNAPSHOT(policy_base, transition=False)
        changed = _changed_paths_exact(candidate, policy_base)
        if changed == frozenset({LOCK_PATH}):
            _require_bound_overlay(candidate, policy_base, require_remote_lineage=True)
        else:
            PRIOR_VERIFY_SNAPSHOT(candidate, transition=False)
    elif candidate_has_snapshot:
        _require_initial_repaired_admission(candidate, policy_base)


def _verify_extension_paths_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
    controlled: frozenset[str],
) -> None:
    safe_controlled = _require_path_set(controlled, "extension-controlled-path")
    bootstrap = _is_bootstrap_base(policy_base)
    candidate_paths = _paths(candidate)
    base_paths = _paths(policy_base)

    if POLICY_SCRIPT in safe_controlled:
        if POLICY_SCRIPT not in candidate_paths:
            base.fail("Pictorial/Agile source-admission-v9 policy wrapper is missing")
        if bootstrap:
            if POLICY_SCRIPT in base_paths:
                base.fail("Pictorial/Agile source-admission-v9 wrapper unexpectedly exists in bootstrap base")
        else:
            if POLICY_SCRIPT not in base_paths:
                base.fail("Pictorial/Agile source-admission-v9 steady-state base lacks wrapper")
            if candidate.read_bytes(POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
                POLICY_SCRIPT, base.MAX_POLICY_FILE_BYTES
            ):
                base.fail("Pictorial/Agile source-admission-v9 steady-state wrapper changed")

    for relative in sorted(BOOTSTRAP_WORKFLOWS & safe_controlled):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if _sha256(candidate_bytes) != EXPECTED_WORKFLOW_SHA256[relative]:
            base.fail(f"Pictorial/Agile source-admission-v9 controlled workflow candidate drifted: {relative}")
        expected_base = (
            PRIOR_EXPECTED_WORKFLOW_SHA256[relative]
            if bootstrap
            else EXPECTED_WORKFLOW_SHA256[relative]
        )
        if _sha256(base_bytes) != expected_base:
            base.fail(f"Pictorial/Agile source-admission-v9 controlled workflow base drifted: {relative}")
        if not bootstrap and candidate_bytes != base_bytes:
            base.fail(f"Pictorial/Agile source-admission-v9 controlled workflow changed: {relative}")

    delegated = frozenset(safe_controlled - {POLICY_SCRIPT} - BOOTSTRAP_WORKFLOWS)
    if delegated:
        verifier = prior._verify_extension_paths_v8
        if verifier is not PRIOR_VERIFY_EXTENSION_PATHS or not callable(verifier):
            base.fail("Pictorial/Agile source-admission-v9 inherited extension verifier drifted")
        verifier(candidate, policy_base, delegated)


def _verify_desktop_extension_paths_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, desktop, _ = _topology()
    _verify_extension_paths_v9(
        candidate,
        policy_base,
        _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension"),
    )


def _verify_execution_extension_paths_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    _, _, _, _, execution = _topology()
    _verify_extension_paths_v9(
        candidate,
        policy_base,
        _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension"),
    )


def _validate_allowed_paths_v9(paths: set[str], stage: str) -> None:
    projected = {path for path in paths if path != POLICY_SCRIPT}
    delegated = prior._validate_allowed_paths_v8
    if delegated is not PRIOR_VALIDATE_ALLOWED_PATHS or not callable(delegated):
        base.fail("Pictorial/Agile source-admission-v9 inherited allowlist delegate drifted")
    delegated(projected, stage)


def _require_evidence_record(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if POLICY_SCRIPT not in paths:
        return
    if EVIDENCE_PATH not in paths:
        base.fail("Pictorial/Agile source-admission-v9 evidence record is missing")
    evidence = view.read_bytes(EVIDENCE_PATH, base.MAX_POLICY_FILE_BYTES)
    if _git_blob_sha1(evidence) != EXPECTED_EVIDENCE_GIT_BLOB_SHA1:
        base.fail("Pictorial/Agile source-admission-v9 evidence record drifted")


def _verify_policy_files_v9(view: base.RepositoryView) -> None:
    actual = _git_blob_sha1(view.read_bytes(PRIOR_POLICY_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1:
        base.fail(
            "frozen Pictorial/Agile source-admission-v8 predecessor policy drifted: "
            f"expected={EXPECTED_PRIOR_POLICY_GIT_BLOB_SHA1} actual={actual}"
        )
    verifier = prior._verify_policy_files_v8
    if verifier is not PRIOR_VERIFY_POLICY_FILES or not callable(verifier):
        base.fail("Pictorial/Agile source-admission-v9 inherited policy-file verifier drifted")
    verifier(view)
    _require_evidence_record(view)


def _require_prebind_identity(
    shell: Any,
    retention: Any,
    desktop: Any,
    execution: Any,
) -> None:
    checks = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, PRIOR_REQUIRE_EXACT_DELTA, "exact-delta"),
        (base.compare_base_controlled, PRIOR_COMPARE_BASE_CONTROLLED, "base-control"),
        (base.validate_entries, PRIOR_VALIDATE_ENTRIES, "tracked-mode"),
        (desktop.verify_extension_controlled_paths, PRIOR_DESKTOP_VERIFY_EXTENSION_PATHS, "desktop-extension"),
        (execution.verify_extension_controlled_paths, PRIOR_EXECUTION_VERIFY_EXTENSION_PATHS, "execution-extension"),
        (shell.validate_allowed_paths, PRIOR_VALIDATE_ALLOWED_PATHS, "tracked-path"),
        (shell.verify_policy_files, PRIOR_VERIFY_POLICY_FILES, "policy-file"),
        (shell.print_success, PRIOR_PRINT_SUCCESS, "success-printer"),
    )
    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile source-admission-v9 pre-bind {label} hook drifted")


def _require_overlay_identity() -> None:
    shell, retention, _, desktop, execution = _topology()
    checks = (
        (retention.IMPL_REQUIRE_EXACT_DELTA, _require_exact_delta_v9, "exact-delta"),
        (base.compare_base_controlled, _compare_base_controlled_v9, "base-control"),
        (base.validate_entries, PRIOR_VALIDATE_ENTRIES, "tracked-mode"),
        (desktop.verify_extension_controlled_paths, _verify_desktop_extension_paths_v9, "desktop-extension"),
        (execution.verify_extension_controlled_paths, _verify_execution_extension_paths_v9, "execution-extension"),
        (shell.validate_allowed_paths, _validate_allowed_paths_v9, "tracked-path"),
        (shell.verify_policy_files, _verify_policy_files_v9, "policy-file"),
        (shell.print_success, _print_success, "success-printer"),
    )
    for actual, wanted, label in checks:
        if actual is not wanted:
            base.fail(f"Pictorial/Agile source-admission-v9 {label} hook drifted")
    desktop_paths = _require_path_set(desktop.EXTENSION_CONTROLLED_PATHS, "desktop-extension")
    execution_paths = _require_path_set(execution.EXTENSION_CONTROLLED_PATHS, "execution-extension")
    if POLICY_SCRIPT not in desktop_paths or POLICY_SCRIPT not in execution_paths:
        base.fail("Pictorial/Agile source-admission-v9 controlled-path registration drifted")


def _print_success(stage: str, mode: str) -> None:
    if _PRIOR_PRINT_SUCCESS is None or not callable(_PRIOR_PRINT_SUCCESS):
        base.fail("Pictorial/Agile source-admission-v9 prior success printer unavailable")
    _PRIOR_PRINT_SUCCESS(stage, mode)
    print(f"pictorial_agile_source_admission_v9_authority={SOURCE_IMPORT_AUTHORITY}")
    print(f"effective_source_admission={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission={DEPENDENCY_ADMISSION}")
    print(f"effective_package_installation={PACKAGE_INSTALLATION}")
    print(f"effective_package_import_or_execution={PACKAGE_IMPORT_OR_EXECUTION}")
    print(f"effective_donor_code_execution={DONOR_CODE_EXECUTION}")
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
    prior_print_success = prior._print_success
    if prior_print_success is not PRIOR_PRINT_SUCCESS or not callable(prior_print_success):
        base.fail("Pictorial/Agile source-admission-v9 predecessor success printer drifted")

    _PRIOR_PRINT_SUCCESS = prior_print_success
    retention.IMPL_REQUIRE_EXACT_DELTA = _require_exact_delta_v9
    base.compare_base_controlled = _compare_base_controlled_v9
    desktop.EXTENSION_CONTROLLED_PATHS = frozenset(desktop_paths | {POLICY_SCRIPT})
    execution.EXTENSION_CONTROLLED_PATHS = frozenset(execution_paths | {POLICY_SCRIPT})
    desktop.verify_extension_controlled_paths = _verify_desktop_extension_paths_v9
    execution.verify_extension_controlled_paths = _verify_execution_extension_paths_v9
    shell.validate_allowed_paths = _validate_allowed_paths_v9
    shell.verify_policy_files = _verify_policy_files_v9
    shell.print_success = _print_success

    _INSTALLED = True
    _require_overlay_identity()


def _selftest_workflows() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    for path in BOOTSTRAP_WORKFLOWS:
        actual = _sha256(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        expected = EXPECTED_WORKFLOW_SHA256[path]
        if actual != expected:
            base.fail(
                "Pictorial/Agile source-admission-v9 workflow drifted: "
                f"{path}: expected={expected} actual={actual}"
            )


def _selftest_evidence() -> None:
    view = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    actual = _git_blob_sha1(view.read_bytes(EVIDENCE_PATH, base.MAX_POLICY_FILE_BYTES))
    if actual != EXPECTED_EVIDENCE_GIT_BLOB_SHA1:
        base.fail(
            "Pictorial/Agile source-admission-v9 evidence record drifted: "
            f"expected={EXPECTED_EVIDENCE_GIT_BLOB_SHA1} actual={actual}"
        )


def _expect_shape_failure(label: str, expected: str, **kwargs: Any) -> None:
    base.expect_failure_matching(label, expected, _validate_overlay_shape, **kwargs)


def _selftest_overlay_contract() -> None:
    valid = dict(
        changed=frozenset({LOCK_PATH}),
        predecessor_lock_blob=ORIGINAL_LOCK_BLOB,
        candidate_lock_blob=REPAIRED_LOCK_BLOB,
        predecessor_package_blob=PACKAGE_JSON_BLOB,
        candidate_package_blob=PACKAGE_JSON_BLOB,
    )
    _validate_overlay_shape(**valid)

    second_vendor = dict(valid)
    second_vendor["changed"] = frozenset({LOCK_PATH, "vendor/pictorial/package.json"})
    _expect_shape_failure(
        "v9 second-vendor-path rejection",
        "must be exactly vendor/pictorial/bun.lock",
        **second_vendor,
    )

    different_lock = dict(valid)
    different_lock["candidate_lock_blob"] = "0" * 40
    _expect_shape_failure(
        "v9 different-lock-blob rejection",
        "repaired lock drifted",
        **different_lock,
    )

    package_drift = dict(valid)
    package_drift["candidate_package_blob"] = "1" * 40
    _expect_shape_failure(
        "v9 package-json rejection",
        "package.json drifted",
        **package_drift,
    )

    agile_drift = dict(valid)
    agile_drift["changed"] = frozenset({LOCK_PATH, "vendor/agile/pyproject.toml"})
    _expect_shape_failure(
        "v9 Agile-drift rejection",
        "must be exactly vendor/pictorial/bun.lock",
        **agile_drift,
    )

    provenance_rewrite = dict(valid)
    provenance_rewrite["changed"] = frozenset(
        {LOCK_PATH, "docs/acquisition/source-maps/pictorial-source-map-2026-08-23.jsonl"}
    )
    _expect_shape_failure(
        "v9 source-map provenance-rewrite rejection",
        "must be exactly vendor/pictorial/bun.lock",
        **provenance_rewrite,
    )


def _selftest_review_repairs() -> None:
    _require_initial_admission_path_shape(frozenset({LOCK_PATH}))
    base.expect_failure_matching(
        "v9 initial admission non-source rejection",
        "changed non-source paths",
        _require_initial_admission_path_shape,
        frozenset({LOCK_PATH, FOUNDATION_WORKFLOW}),
    )
    base.expect_failure_matching(
        "v9 initial admission missing-lock rejection",
        "missing repaired bun.lock",
        _require_initial_admission_path_shape,
        frozenset({next(iter(prior.prior.SOURCE_ARTIFACT_BLOBS))}),
    )

    policy_parent = "a" * 40
    _require_exact_parent_set(
        {"parents": [{"sha": REPAIR_CANDIDATE_HEAD}, {"sha": policy_parent}]},
        frozenset({REPAIR_CANDIDATE_HEAD, policy_parent}),
        "v9 parent-shape positive",
    )
    base.expect_failure_matching(
        "v9 wrong-parent rejection",
        "parent lineage drifted",
        _require_exact_parent_set,
        {"parents": [{"sha": REPAIR_CANDIDATE_HEAD}, {"sha": "b" * 40}]},
        frozenset({REPAIR_CANDIDATE_HEAD, policy_parent}),
        "v9 parent-shape negative",
    )

    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    evidence = local.read_bytes(EVIDENCE_PATH, base.MAX_POLICY_FILE_BYTES)
    _require_evidence_record(_memory_view({POLICY_SCRIPT: b"policy", EVIDENCE_PATH: evidence}))
    base.expect_failure_matching(
        "v9 evidence deletion rejection",
        "evidence record is missing",
        _require_evidence_record,
        _memory_view({POLICY_SCRIPT: b"policy"}),
    )
    base.expect_failure_matching(
        "v9 evidence mutation rejection",
        "evidence record drifted",
        _require_evidence_record,
        _memory_view({POLICY_SCRIPT: b"policy", EVIDENCE_PATH: evidence + b"x"}),
    )


def _selftest_local_remote_client_bridge() -> None:
    global _LOCAL_REMOTE_CLIENT
    if _LOCAL_REMOTE_CLIENT is not None:
        base.fail("v9 scoped remote-baseline client leaked into selftest")
    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    sentinel = object()
    _LOCAL_REMOTE_CLIENT = sentinel
    try:
        if _shared_trusted_client(local, local) is not sentinel:
            base.fail("v9 scoped remote-baseline client bridge returned wrong identity")
    finally:
        _LOCAL_REMOTE_CLIENT = None
    base.expect_failure_matching(
        "v9 local/local outside remote-baseline scope rejection",
        "requires trusted remote-baseline client scope",
        _shared_trusted_client,
        local,
        local,
    )


def _selftest_authority() -> None:
    actual = (
        SOURCE_ADMISSION,
        DEPENDENCY_ADMISSION,
        PACKAGE_INSTALLATION,
        PACKAGE_IMPORT_OR_EXECUTION,
        DONOR_CODE_EXECUTION,
        DONOR_WORKFLOW_EXECUTION,
        DONOR_HOOK_EXECUTION,
        DONOR_INSTALL_SCRIPT_EXECUTION,
        DONOR_PARITY_TEST_EXECUTION,
        DONOR_LIVE_TEST_EXECUTION,
        PRODUCT_IMPLEMENTATION_AUTHORITY,
        PRODUCT_RUNTIME_ADMISSION,
        H0_014_PLUS,
        H0_SCREEN_EXECUTION,
        MODEL_PROVIDER_EXECUTION,
        MODEL_WEIGHT_ACCESS,
        MODEL_INFERENCE,
        CREDENTIAL_CONTENT_ACCESS,
        CANONICAL_POLICY_MERGE,
        PR136_SOURCE_HEAD_REPLACEMENT,
        PR162_MERGE,
        PR136_MERGE,
    )
    wanted = (
        "EXACT_SOURCE_PLUS_ONE_BOUND_LOCK_METADATA_OVERLAY",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NOT_STARTED",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NONE",
        "NOT_AUTHORIZED",
        "NOT_AUTHORIZED",
        "NOT_AUTHORIZED",
        "NOT_AUTHORIZED",
    )
    if actual != wanted:
        base.fail("Pictorial/Agile source-admission-v9 authority boundary drifted")


def selftest() -> None:
    try:
        current = dict(prior.EXPECTED_WORKFLOW_SHA256)
    except (AttributeError, TypeError, ValueError) as exc:
        base.fail(f"Pictorial/Agile source-admission-v9 predecessor selftest topology malformed: {exc}")
    if current not in (
        dict(PRIOR_EXPECTED_WORKFLOW_SHA256),
        dict(EXPECTED_WORKFLOW_SHA256),
    ):
        base.fail("Pictorial/Agile source-admission-v9 predecessor selftest hashes drifted")
    prior.EXPECTED_WORKFLOW_SHA256 = dict(EXPECTED_WORKFLOW_SHA256)
    prior.selftest()

    _selftest_overlay_contract()
    _selftest_review_repairs()
    _selftest_local_remote_client_bridge()
    _selftest_authority()
    _install_policy()
    _selftest_workflows()
    _selftest_evidence()
    _require_overlay_identity()
    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    _require_prior_policy_base(local)
    print("wepld Pictorial/Agile source admission v9 bounded-lock-overlay self-tests: PASS")


def _qualify_overlay_remote(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="qualify-overlay-remote")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--predecessor-sha", required=True)
    parser.add_argument("--candidate-sha", required=True)
    args = parser.parse_args(argv)

    if args.repository != base.REPOSITORY:
        base.fail("Pictorial/Agile v9 qualification repository drifted")
    if args.predecessor_sha != PREDECESSOR_SOURCE_HEAD:
        base.fail("Pictorial/Agile v9 qualification predecessor SHA drifted")
    if args.candidate_sha != REPAIR_CANDIDATE_HEAD:
        base.fail("Pictorial/Agile v9 qualification candidate SHA drifted")

    token = os.environ.get("GITHUB_TOKEN")
    client = base.GitHubClient(token)
    predecessor = base.RemoteRepositoryView(args.repository, args.predecessor_sha, client)
    candidate = base.RemoteRepositoryView(args.repository, args.candidate_sha, client)
    _require_bound_overlay(candidate, predecessor, require_remote_lineage=True)

    print("pictorial_agile_v9_overlay_remote_qualification=PASS")
    print(f"predecessor_source_head={PREDECESSOR_SOURCE_HEAD}")
    print(f"repair_candidate_head={REPAIR_CANDIDATE_HEAD}")
    print(f"original_lock_blob={ORIGINAL_LOCK_BLOB}")
    print(f"repaired_lock_blob={REPAIRED_LOCK_BLOB}")
    print(f"repaired_lock_sha256={REPAIRED_LOCK_SHA256}")
    print(f"repaired_cyclonedx_sha256={REPAIRED_CYCLONEDX_SHA256}")
    print(f"repaired_osv_response_sha256={REPAIRED_OSV_RESPONSE_SHA256}")
    print(f"effective_source_admission={SOURCE_ADMISSION}")
    print(f"effective_dependency_admission={DEPENDENCY_ADMISSION}")
    print(f"effective_product_runtime_admission={PRODUCT_RUNTIME_ADMISSION}")
    return 0


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0
        if argv and argv[0] == "qualify-overlay-remote":
            _install_policy()
            return _qualify_overlay_remote(argv[1:])

        _install_policy()
        shell, retention, impl, _, _ = _topology()

        if argv and argv[0] == "verify-local":
            args = base.parse_args(argv)
            if args.remote_baseline:
                global _LOCAL_REMOTE_CLIENT
                if _LOCAL_REMOTE_CLIENT is not None:
                    base.fail("v9 remote-baseline client scope is already active")
                token = os.environ.get(args.github_token_env) or None
                _LOCAL_REMOTE_CLIENT = base.GitHubClient(token)
                try:
                    return prior._call_trusted_local_runner(args, shell, impl)
                finally:
                    _LOCAL_REMOTE_CLIENT = None

        runner = retention.main
        if not callable(runner):
            base.fail("Pictorial/Agile source-admission-v9 runtime main is not callable")
        return runner(argv)
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
