#!/usr/bin/env python3
"""Fail-closed WePLD repository integrity policy for S1 planning/acquisition stages.

The policy supports two modes:
- verify-local: advisory/head and canonical-main verification of a checked-out tree.
- verify-remote: authoritative base-controlled inspection of a PR candidate through
  GitHub's Git data API. Candidate files are treated strictly as data and are never
  checked out or executed by the privileged pull_request_target workflow.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tarfile
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterable, Mapping

REPOSITORY = "TheHalfMoon/wepld"
REPOSITORY_ID = 1334408699
BASELINE_COMMIT_SHA = "421c769b47fd8ad4f5bcba67ff8b00ba0adfc6c3"
BASELINE_PATH = ".wepld/foundation-integrity-baseline-v1.json"
BASELINE_BLOB_SHA = "a7c1423c95683f94479fb4a166ec73b3c35149ed"
BASELINE_BASE_MAIN_SHA = "7813dea9c53863378a5ae2fefcaf66f6b5d43103"
EXPECTED_ARCHIVE_SHA256 = "35dee10e7526d1958c5b3b88a1a9b569b0d1a464f5eec4e20e16c19c99f1c6b0"
EXPECTED_PLAN_SHA256 = "e269b10ef711731c4ad3af7b1135546f92d82a78975cabc9ff52c2dea4b5bf44"
EXPECTED_SOURCE_REGISTRY_ENTRIES = 402

ARCHIVE_RELATIVE_PATH = "docs/canonical/artifacts/WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz"
PLAN_MEMBER = "WEPLD_MASTER_ARCHITECTURE_EXECUTION_PLAN_2026-08-12_V2_2.md"
REGISTRY_JSON_MEMBER = "WEPLD_MASTER_SOURCE_REGISTRY_2026-08-14_V1.json"
REGISTRY_CSV_MEMBER = "WEPLD_MASTER_SOURCE_REGISTRY_2026-08-14_V1.csv"
EXPECTED_ARCHIVE_MEMBERS = {
    PLAN_MEMBER,
    REGISTRY_JSON_MEMBER,
    REGISTRY_CSV_MEMBER,
    "WEPLD_SOURCE_ARTIFACT_PIN_LEDGER_2026-08-14_V1.md",
    "WEPLD_SOURCE_CAPABILITY_MINING_PRIORITY_MATRIX_2026-08-14_V1.md",
}
MAX_ARCHIVE_BYTES = 1_000_000
MAX_ARCHIVE_MEMBER_BYTES = 1_000_000
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 2_000_000
MAX_LOCKFILE_BYTES = 2_000_000
MAX_LOCK_PACKAGES = 1_000
MAX_POLICY_FILE_BYTES = 512_000

EXPECTED_BASELINE = {
    "schema": "wepld.foundation-integrity-baseline.v1",
    "baseline_class": "BOOTSTRAP_INTEGRITY_EVIDENCE_NOT_ACCEPTANCE",
    "repository_id": REPOSITORY_ID,
    "repository": REPOSITORY,
    "base_main_sha": BASELINE_BASE_MAIN_SHA,
    "canonical_artifact_archive_sha256": EXPECTED_ARCHIVE_SHA256,
    "master_plan_v2_2_sha256": EXPECTED_PLAN_SHA256,
    "source_registry_entries": EXPECTED_SOURCE_REGISTRY_ENTRIES,
    "source_admission": 0,
}

EXPECTED_CODERABBIT = """# External hosted review is manual-only until WePLD has a machine-enforced
# pre-egress classification/screening/approval gate. Manual CodeRabbit review
# commands remain available after the canonical egress preflight is recorded.
reviews:
  auto_review:
    enabled: false
    auto_incremental_review: false
"""

EXPECTED_CUBIC = """# yaml-language-server: $schema=https://cubic.dev/schema/cubic-repository-config.schema.json

version: 1

# WePLD requires a recorded exact-scope pre-egress gate before any hosted review.
# Keep Cubic connected if desired, but do not let repository events transmit
# repository content automatically.
reviews:
  enabled: false
  incremental_commits: false
  check_drafts: false
  resolve_threads_when_addressed: false
  auto_approve_behavior: disabled
  auto_approve: disabled
  ultrareview: disabled
  auto_ultrareview: disabled
  custom_rules: []

pr_descriptions:
  generate: false

issues:
  fix_with_cubic_buttons: false
  pr_comment_fixes: false
  fix_commits_to_pr: false
"""

ROOT_CARGO = """[workspace]
resolver = "2"
members = [
  "apps/desktop/src-tauri",
  "crates/contracts",
  "crates/core",
]
"""

DESKTOP_CARGO = """[package]
name = "wepld-desktop"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
tauri = { version = "=2.11.5", default-features = false, features = ["wry"] }
wepld-contracts = { path = "../../../crates/contracts" }

[build-dependencies]
tauri-build = { version = "=2.6.3", default-features = false }
"""

CONTRACTS_CARGO = """[package]
name = "wepld-contracts"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
serde = { version = "=1.0.229", features = ["derive"] }
serde_json = "=1.0.151"
"""

CORE_CARGO = """[package]
name = "wepld-core"
version = "0.0.0"
edition = "2024"
publish = false

[dependencies]
wepld-contracts = { path = "../contracts" }
"""

RUST_TOOLCHAIN = """[toolchain]
channel = "1.97.1"
profile = "minimal"
components = ["clippy", "rustfmt"]
targets = ["x86_64-pc-windows-msvc"]
"""

MAIN_SKELETON = """#![forbid(unsafe_code)]

fn main() {}
"""
CONTRACTS_SKELETON = """#![forbid(unsafe_code)]
"""

STAGE_B_TEXT = {
    "Cargo.toml": ROOT_CARGO,
    "rust-toolchain.toml": RUST_TOOLCHAIN,
    "apps/desktop/src-tauri/Cargo.toml": DESKTOP_CARGO,
    "apps/desktop/src-tauri/src/main.rs": MAIN_SKELETON,
    "crates/contracts/Cargo.toml": CONTRACTS_CARGO,
    "crates/contracts/src/lib.rs": CONTRACTS_SKELETON,
    "crates/core/Cargo.toml": CORE_CARGO,
    "crates/core/src/main.rs": MAIN_SKELETON,
}
STAGE_B_INPUT_PATHS = frozenset(STAGE_B_TEXT)
STAGE_B_LOCK_PATH = "Cargo.lock"
STAGE_B_ALL_PATHS = STAGE_B_INPUT_PATHS | {STAGE_B_LOCK_PATH}

COMMON_EXACT_ALLOWED = {
    ".coderabbit.yaml",
    ".github/scripts/wepld_integrity.py",
    ".github/workflows/foundation-integrity.yml",
    ".github/workflows/s1-admission-integrity.yml",
    "AGENTS.md",
    "README.md",
    "cubic.yaml",
    "src/.gitkeep",
    ARCHIVE_RELATIVE_PATH,
}

REQUIRED_PATHS = {
    "AGENTS.md",
    ".coderabbit.yaml",
    "cubic.yaml",
    ".github/scripts/wepld_integrity.py",
    ".github/workflows/foundation-integrity.yml",
    ".github/workflows/s1-admission-integrity.yml",
    "docs/canonical/CURRENT_STATE.md",
    "docs/canonical/ARCHITECTURE_INVARIANTS.md",
    "docs/canonical/MASTER_PLAN_INDEX.md",
    "docs/canonical/FOUNDER_RATIFICATION.md",
    "docs/canonical/BUILD_METHOD.md",
    "docs/canonical/SECURITY_REVIEW_POLICY.md",
    "docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md",
    "docs/canonical/artifacts/README.md",
    ARCHIVE_RELATIVE_PATH,
    "docs/acquisition/SOURCE_REGISTRY_INDEX.md",
    "docs/governance/DEPENDENCY_REGISTER.md",
    "docs/governance/REPOSITORY_AUTHORITY_EVIDENCE_2026-08-14.md",
    "docs/governance/REPOSITORY_IP_STATE.md",
    "docs/governance/FOUNDATION_INTEGRITY_BASELINE.md",
    "specs/000-wepld-fresh-reconstitution/spec.md",
    "specs/000-wepld-fresh-reconstitution/plan.md",
    "specs/000-wepld-fresh-reconstitution/tasks.md",
    "specs/000-wepld-fresh-reconstitution/acceptance.md",
    "specs/001-desktop-rust-trusted-core-handshake/spec.md",
    "specs/001-desktop-rust-trusted-core-handshake/plan.md",
    "specs/001-desktop-rust-trusted-core-handshake/tasks.md",
    "specs/001-desktop-rust-trusted-core-handshake/source-acquisition.md",
    "specs/001-desktop-rust-trusted-core-handshake/s1-003-integrity-migration.md",
}

# Ordinary future candidate PRs are not allowed to mutate the mechanism or the
# core governance contracts used to judge them. A legitimate future policy
# migration must be handled as an explicitly governed bootstrap/override event.
BASE_CONTROLLED_PATHS = {
    ".coderabbit.yaml",
    "cubic.yaml",
    ".github/scripts/wepld_integrity.py",
    ".github/workflows/foundation-integrity.yml",
    ".github/workflows/s1-admission-integrity.yml",
    "AGENTS.md",
    "docs/canonical/ARCHITECTURE_INVARIANTS.md",
    "docs/canonical/BUILD_METHOD.md",
    "docs/canonical/SECURITY_REVIEW_POLICY.md",
    "docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md",
    "docs/canonical/FOUNDER_RATIFICATION.md",
    "docs/canonical/MASTER_PLAN_INDEX.md",
    "docs/governance/FOUNDATION_INTEGRITY_BASELINE.md",
}

CRATES_IO_SOURCE = "registry+https://github.com/rust-lang/crates.io-index"
REQUIRED_LOCK_PACKAGES = {
    ("tauri", "2.11.5"),
    ("tauri-build", "2.6.3"),
    ("serde", "1.0.229"),
    ("serde_json", "1.0.151"),
    ("wepld-desktop", "0.0.0"),
    ("wepld-contracts", "0.0.0"),
    ("wepld-core", "0.0.0"),
}

# Only the workspace members declared by the exact Stage-B manifests may appear
# without a `source`. Any other source-less identity is an unresolved or
# fabricated package masquerading as a local path crate.
WORKSPACE_LOCK_PACKAGES = {
    ("wepld-desktop", "0.0.0"),
    ("wepld-contracts", "0.0.0"),
    ("wepld-core", "0.0.0"),
}

# Direct dependency edges implied by the exact Stage-B manifests. Cargo.lock
# merges normal and build dependencies into one `dependencies` array, so
# `tauri-build` is expected on `wepld-desktop`. Transitive edges are not
# asserted here; they are not implied by WePLD-owned manifests.
REQUIRED_LOCK_EDGES = {
    ("wepld-desktop", "0.0.0"): frozenset(
        {
            ("tauri", "2.11.5"),
            ("wepld-contracts", "0.0.0"),
            ("tauri-build", "2.6.3"),
        }
    ),
    ("wepld-contracts", "0.0.0"): frozenset(
        {
            ("serde", "1.0.229"),
            ("serde_json", "1.0.151"),
        }
    ),
    ("wepld-core", "0.0.0"): frozenset({("wepld-contracts", "0.0.0")}),
}

REPOSITORY_SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
OBJECT_SHA_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")


class PolicyError(RuntimeError):
    pass


@dataclass(frozen=True)
class TrackedEntry:
    mode: str
    path: str


def fail(message: str) -> None:
    raise PolicyError(message)


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(
            req.full_url,
            code,
            f"redirect refused: {newurl}",
            headers,
            fp,
        )


class GitHubClient:
    def __init__(self, token: str | None):
        self.token = token
        self.opener = urllib.request.build_opener(RejectRedirects())

    def json(self, url: str) -> Mapping[str, object]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        try:
            with self.opener.open(request, timeout=30) as response:
                if response.geturl() != url:
                    fail(f"GitHub API target changed unexpectedly: {url}")
                data = json.load(response)
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"GitHub API request failed for {url}: {exc}")
        if not isinstance(data, dict):
            fail(f"GitHub API response is not an object: {url}")
        return data


class RepositoryView:
    def entries(self) -> list[TrackedEntry]:
        raise NotImplementedError

    def read_bytes(self, relative: str, limit: int) -> bytes:
        raise NotImplementedError

    def read_text(self, relative: str, limit: int = MAX_POLICY_FILE_BYTES) -> str:
        data = self.read_bytes(relative, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            fail(f"tracked file is not UTF-8: {relative}: {exc}")


class LocalRepositoryView(RepositoryView):
    def __init__(self, root: Path):
        self.root = root.resolve()
        if not (self.root / ".git").exists():
            fail(f"root is not a Git checkout: {self.root}")

    def entries(self) -> list[TrackedEntry]:
        try:
            raw = subprocess.check_output(
                ["git", "-C", str(self.root), "ls-files", "--stage", "-z"],
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode("utf-8", errors="replace")
            fail(f"git ls-files failed: {output.strip()}")

        result: list[TrackedEntry] = []
        for record in raw.split(b"\0"):
            if not record:
                continue
            try:
                metadata, raw_path = record.split(b"\t", 1)
                mode_b, _object_b, stage_b = metadata.split(b" ", 2)
                stage = int(stage_b)
                if stage != 0:
                    fail(
                        "unmerged index stage is prohibited: "
                        f"{raw_path!r} stage={stage}"
                    )
                result.append(
                    TrackedEntry(
                        mode=mode_b.decode("ascii", errors="strict"),
                        path=raw_path.decode("utf-8", errors="strict"),
                    )
                )
            except (ValueError, UnicodeError) as exc:
                fail(f"malformed tracked-index record: {record!r}: {exc}")
        return result

    def read_bytes(self, relative: str, limit: int) -> bytes:
        path = self.root / relative
        try:
            info = path.lstat()
        except OSError as exc:
            fail(f"unable to lstat {relative}: {exc}")
        if not stat.S_ISREG(info.st_mode):
            fail(f"file must be a regular non-symlink: {relative}")

        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            fd = os.open(path, flags)
        except OSError as exc:
            fail(f"unable to open safely {relative}: {exc}")
        try:
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode):
                fail(f"opened path is not regular: {relative}")
            with os.fdopen(fd, "rb", closefd=False) as handle:
                data = handle.read(limit + 1)
        finally:
            os.close(fd)
        if len(data) > limit:
            fail(f"file exceeds bounded size {limit}: {relative}")
        return data


def require_object_identity(kind: str, requested: str, returned: object) -> None:
    """Bind a Git data API response to the exact object identity requested.

    Without this the policy would trust the request URL rather than the answer,
    and would consume whatever tree entries or blob content came back. Object IDs
    compare case-insensitively, matching the existing SHA normalization policy
    (`OBJECT_SHA_RE` accepts either case; the candidate commit SHA is lowercased).
    """
    if not OBJECT_SHA_RE.fullmatch(requested):
        fail(f"requested {kind} object SHA is malformed: {requested!r}")
    if not isinstance(returned, str) or not OBJECT_SHA_RE.fullmatch(returned):
        fail(f"returned {kind} object identity is malformed: {returned!r}")
    if returned.lower() != requested.lower():
        fail(
            f"returned {kind} object identity does not match the requested object: "
            f"requested={requested.lower()} returned={returned.lower()}"
        )


class RemoteRepositoryView(RepositoryView):
    """Read a candidate Git object graph through GitHub API without checkout."""

    def __init__(
        self,
        repository: str,
        commit_sha: str,
        client: GitHubClient,
    ):
        if not REPOSITORY_SLUG_RE.fullmatch(repository):
            fail(f"invalid candidate repository slug: {repository!r}")
        if not OBJECT_SHA_RE.fullmatch(commit_sha):
            fail(f"invalid candidate commit SHA: {commit_sha!r}")

        self.repository = repository
        self.commit_sha = commit_sha.lower()
        self.client = client
        self._blobs: dict[str, tuple[str, int]] = {}
        self._entries: list[TrackedEntry] = []
        self._cache: dict[str, bytes] = {}
        self._load_tree()

    def _load_tree(self) -> None:
        commit = self.client.json(
            f"https://api.github.com/repos/{self.repository}/git/commits/{self.commit_sha}"
        )
        returned_sha = commit.get("sha")
        if not isinstance(returned_sha, str) or returned_sha.lower() != self.commit_sha:
            fail("GitHub returned an unexpected candidate commit identity")
        tree_info = commit.get("tree")
        if not isinstance(tree_info, dict):
            fail("candidate commit has no tree object")
        tree_sha = tree_info.get("sha")
        if not isinstance(tree_sha, str) or not OBJECT_SHA_RE.fullmatch(tree_sha):
            fail("candidate commit tree SHA is malformed")

        tree = self.client.json(
            f"https://api.github.com/repos/{self.repository}/git/trees/{tree_sha}?recursive=1"
        )
        # Bind the response to the requested tree before any entry is consumed.
        require_object_identity("tree", tree_sha, tree.get("sha"))
        if tree.get("truncated") is True:
            fail("candidate Git tree response is truncated")
        raw_entries = tree.get("tree")
        if not isinstance(raw_entries, list):
            fail("candidate Git tree payload is malformed")

        for item in raw_entries:
            if not isinstance(item, dict):
                fail("candidate Git tree contains a malformed entry")
            item_type = item.get("type")
            if item_type == "tree":
                continue
            path = item.get("path")
            mode = item.get("mode")
            object_sha = item.get("sha")
            if not isinstance(path, str) or not isinstance(mode, str):
                fail("candidate Git tree path/mode is malformed")
            self._entries.append(TrackedEntry(mode=mode, path=path))

            if item_type == "blob":
                size = item.get("size")
                if not isinstance(object_sha, str) or not OBJECT_SHA_RE.fullmatch(object_sha):
                    fail(f"candidate blob SHA is malformed: {path}")
                if not isinstance(size, int) or size < 0:
                    fail(f"candidate blob size is malformed: {path}")
                self._blobs[path] = (object_sha, size)
            elif item_type == "commit":
                # Gitlink/submodule; validate_entries() rejects mode 160000.
                continue
            else:
                fail(f"unexpected candidate Git object type {item_type!r}: {path}")

    def entries(self) -> list[TrackedEntry]:
        return list(self._entries)

    def read_bytes(self, relative: str, limit: int) -> bytes:
        if relative in self._cache:
            data = self._cache[relative]
            if len(data) > limit:
                fail(f"file exceeds bounded size {limit}: {relative}")
            return data

        blob = self._blobs.get(relative)
        if blob is None:
            fail(f"required candidate blob is missing: {relative}")
        blob_sha, declared_size = blob
        if declared_size > limit:
            fail(f"candidate blob exceeds bounded size {limit}: {relative}")

        payload = self.client.json(
            f"https://api.github.com/repos/{self.repository}/git/blobs/{blob_sha}"
        )
        # Bind the response to the requested blob before any content is decoded.
        require_object_identity("blob", blob_sha, payload.get("sha"))
        encoding = payload.get("encoding")
        content = payload.get("content")
        if encoding != "base64" or not isinstance(content, str):
            fail(f"candidate blob API payload is not base64: {relative}")
        try:
            data = base64.b64decode(content, validate=False)
        except ValueError as exc:
            fail(f"candidate blob base64 is invalid: {relative}: {exc}")
        if len(data) != declared_size:
            fail(f"candidate blob size disagrees with tree metadata: {relative}")
        if len(data) > limit:
            fail(f"candidate blob exceeds bounded size after decode: {relative}")
        self._cache[relative] = data
        return data


def validate_entries(entries: Iterable[TrackedEntry]) -> set[str]:
    paths: list[str] = []
    for entry in entries:
        if entry.mode == "120000":
            fail(f"symbolic link is prohibited: {entry.path}")
        if entry.mode == "160000":
            fail(f"gitlink/submodule is prohibited: {entry.path}")
        if entry.mode != "100644":
            fail(f"unexpected tracked mode {entry.mode}: {entry.path}")
        if "\\" in entry.path:
            fail(f"backslash in tracked path is prohibited: {entry.path}")
        pure = PurePosixPath(entry.path)
        if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
            fail(f"unsafe tracked path: {entry.path}")
        paths.append(entry.path)

    if len(paths) != len(set(paths)):
        fail("duplicate tracked path detected")
    folded = [path.casefold() for path in paths]
    if len(folded) != len(set(folded)):
        fail("case-insensitive duplicate tracked path detected")
    return set(paths)


def is_common_allowed(path: str) -> bool:
    if path in COMMON_EXACT_ALLOWED:
        return True
    return (path.startswith("docs/") or path.startswith("specs/")) and path.endswith(".md")


def classify_stage(paths: set[str]) -> str:
    present = paths & STAGE_B_ALL_PATHS
    if not present:
        return "S1_PLANNING_ONLY"

    missing_inputs = STAGE_B_INPUT_PATHS - paths
    if missing_inputs:
        fail(
            "partial dependency-resolution candidate is prohibited; missing: "
            + ", ".join(sorted(missing_inputs))
        )

    if STAGE_B_LOCK_PATH in paths:
        return "S1_DEPENDENCY_RESOLUTION_LOCKED"
    return "S1_DEPENDENCY_RESOLUTION_INPUT"


def validate_allowed_paths(paths: set[str], stage: str) -> None:
    allowed = {path for path in paths if is_common_allowed(path)}
    if stage in {"S1_DEPENDENCY_RESOLUTION_INPUT", "S1_DEPENDENCY_RESOLUTION_LOCKED"}:
        allowed |= STAGE_B_INPUT_PATHS
        if stage == "S1_DEPENDENCY_RESOLUTION_LOCKED":
            allowed.add(STAGE_B_LOCK_PATH)

    unexpected = sorted(paths - allowed)
    if unexpected:
        fail("tracked path outside stage allowlist: " + ", ".join(unexpected))

    missing = sorted(REQUIRED_PATHS - paths)
    if missing:
        fail("required canonical path missing: " + ", ".join(missing))

    extra_root_src = sorted(
        path for path in paths if path.startswith("src/") and path != "src/.gitkeep"
    )
    if extra_root_src:
        fail(
            "root src/ remains a historical placeholder only: "
            + ", ".join(extra_root_src)
        )


def read_text_exact(view: RepositoryView, relative: str, expected: str) -> None:
    actual = view.read_text(relative, max(MAX_POLICY_FILE_BYTES, len(expected.encode("utf-8"))))
    if actual != expected:
        fail(f"exact policy content drifted: {relative}")


def verify_reviewer_configs(view: RepositoryView) -> None:
    read_text_exact(view, ".coderabbit.yaml", EXPECTED_CODERABBIT)
    read_text_exact(view, "cubic.yaml", EXPECTED_CUBIC)


def verify_stage_b_templates(view: RepositoryView, stage: str) -> None:
    if stage == "S1_PLANNING_ONLY":
        return
    for relative, expected in STAGE_B_TEXT.items():
        read_text_exact(view, relative, expected)
    if stage == "S1_DEPENDENCY_RESOLUTION_LOCKED":
        validate_lock_bytes(view.read_bytes(STAGE_B_LOCK_PATH, MAX_LOCKFILE_BYTES))


def validate_lock_bytes(data: bytes) -> None:
    if len(data) > MAX_LOCKFILE_BYTES:
        fail("Cargo.lock exceeds bounded size")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        fail(f"Cargo.lock is not UTF-8: {exc}")
    try:
        lock = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        fail(f"Cargo.lock is not parseable TOML: {exc}")

    if lock.get("version") != 4:
        fail(f"Cargo.lock version must be 4, got {lock.get('version')!r}")
    packages = lock.get("package")
    if not isinstance(packages, list) or not packages:
        fail("Cargo.lock package list is missing")
    if len(packages) > MAX_LOCK_PACKAGES:
        fail("Cargo.lock package count exceeds bounded maximum")

    identities: list[tuple[str, str, str | None]] = []
    declared_edges: dict[tuple[str, str], list[str]] = {}
    for package in packages:
        if not isinstance(package, dict):
            fail("Cargo.lock contains a non-table package")
        name = package.get("name")
        version = package.get("version")
        if not isinstance(name, str) or not isinstance(version, str):
            fail("Cargo.lock package name/version is malformed")
        if not name or not version:
            fail("Cargo.lock package name/version is empty")
        identity = (name, version)

        source = package.get("source")
        if source is not None and not isinstance(source, str):
            fail(f"Cargo.lock package source is malformed: {name}")
        # Identity includes source so two entries differing only by source are
        # still caught as a duplicate package identity.
        identities.append((name, version, source))

        raw_dependencies = package.get("dependencies")
        if raw_dependencies is not None:
            if not isinstance(raw_dependencies, list):
                fail(f"Cargo.lock dependencies field is not an array: {name}")
            references: list[str] = []
            for reference in raw_dependencies:
                if not isinstance(reference, str) or not reference.strip():
                    fail(f"Cargo.lock dependency reference is malformed: {name}")
                references.append(reference)
            declared_edges[identity] = references

        if source is None:
            if identity not in WORKSPACE_LOCK_PACKAGES:
                fail(
                    "source-less Cargo.lock package is not an expected Stage-B "
                    f"workspace member: {name} {version}"
                )
            if package.get("checksum") is not None:
                fail(f"workspace/path package unexpectedly carries checksum: {name}")
            continue
        if source != CRATES_IO_SOURCE:
            fail(f"unapproved Cargo.lock source for {name}: {source}")
        checksum = package.get("checksum")
        if not isinstance(checksum, str) or len(checksum) != 64:
            fail(f"registry package checksum is missing/malformed: {name}")
        try:
            int(checksum, 16)
        except ValueError:
            fail(f"registry package checksum is not hexadecimal: {name}")

    name_versions = [(name, version) for name, version, _source in identities]
    if len(name_versions) != len(set(name_versions)):
        duplicates = sorted(
            {item for item in name_versions if name_versions.count(item) > 1}
        )
        fail("duplicate Cargo.lock package identity: " + repr(duplicates))

    observed = set(name_versions)
    missing = sorted(REQUIRED_LOCK_PACKAGES - observed)
    if missing:
        fail("Cargo.lock missing required candidate packages: " + repr(missing))
    if any(name == "tauri-plugin-shell" for name, _version in observed):
        fail("tauri-plugin-shell is prohibited in the S1 dependency candidate")

    missing_workspace = sorted(WORKSPACE_LOCK_PACKAGES - observed)
    if missing_workspace:
        fail("Cargo.lock missing expected workspace members: " + repr(missing_workspace))

    validate_lock_graph(observed, declared_edges)


def parse_lock_dependency(owner: tuple[str, str], reference: str) -> tuple[str, str | None]:
    """Split a Cargo.lock dependency reference into `name` and optional `version`.

    Cargo has written `"name"`, `"name version"`, and `"name version (source)"`.
    """
    parts = reference.split()
    if not parts or len(parts) > 3:
        fail(
            "malformed Cargo.lock dependency reference: "
            f"{owner[0]} {owner[1]} -> {reference!r}"
        )
    if len(parts) == 3 and not (parts[2].startswith("(") and parts[2].endswith(")")):
        fail(
            "malformed Cargo.lock dependency source qualifier: "
            f"{owner[0]} {owner[1]} -> {reference!r}"
        )
    return parts[0], parts[1] if len(parts) >= 2 else None


def validate_lock_graph(
    observed: set[tuple[str, str]],
    declared_edges: Mapping[tuple[str, str], list[str]],
) -> None:
    """Require each dependency reference to resolve uniquely, and require the
    direct workspace edges implied by the exact Stage-B manifests.

    This establishes structural consistency only:

        STRUCTURALLY_CONSISTENT_LOCK != CARGO_GENERATION_PROVENANCE
    """
    versions_by_name: dict[str, set[str]] = {}
    for name, version in observed:
        versions_by_name.setdefault(name, set()).add(version)

    resolved_edges: dict[tuple[str, str], set[tuple[str, str]]] = {}
    for owner, references in declared_edges.items():
        resolved: set[tuple[str, str]] = set()
        for reference in references:
            name, version = parse_lock_dependency(owner, reference)
            known = versions_by_name.get(name)
            if not known:
                fail(
                    "Cargo.lock dependency does not resolve to any package in the "
                    f"lock: {owner[0]} {owner[1]} -> {reference!r}"
                )
            if version is None:
                if len(known) != 1:
                    fail(
                        "ambiguous unversioned Cargo.lock dependency reference: "
                        f"{owner[0]} {owner[1]} -> {reference!r}"
                    )
                version = next(iter(known))
            elif version not in known:
                fail(
                    "Cargo.lock dependency version does not resolve to a package "
                    f"in the lock: {owner[0]} {owner[1]} -> {reference!r}"
                )
            resolved.add((name, version))
        resolved_edges[owner] = resolved

    for owner, required in REQUIRED_LOCK_EDGES.items():
        absent = sorted(required - resolved_edges.get(owner, set()))
        if absent:
            fail(
                "Cargo.lock is missing required direct dependency edges for "
                f"{owner[0]} {owner[1]}: " + repr(absent)
            )


def verify_dependency_register(view: RepositoryView) -> None:
    lines = view.read_text(
        "docs/governance/DEPENDENCY_REGISTER.md", MAX_POLICY_FILE_BYTES
    ).splitlines()
    if "FRESH_IMPLEMENTATION_DEPENDENCIES = 0" not in lines:
        fail("frozen P0 dependency-register evidence is missing")


def verify_archive(view: RepositoryView) -> None:
    archive_bytes = view.read_bytes(ARCHIVE_RELATIVE_PATH, MAX_ARCHIVE_BYTES)
    actual_archive_sha = hashlib.sha256(archive_bytes).hexdigest()
    if actual_archive_sha != EXPECTED_ARCHIVE_SHA256:
        fail(f"canonical archive SHA-256 mismatch: {actual_archive_sha}")

    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
            members = archive.getmembers()
            names = [member.name for member in members]
            if len(names) != len(EXPECTED_ARCHIVE_MEMBERS) or set(names) != EXPECTED_ARCHIVE_MEMBERS:
                fail("canonical archive member set/count mismatch")
            if any(not member.isfile() for member in members):
                fail("canonical archive contains a non-regular member")
            if any(member.size > MAX_ARCHIVE_MEMBER_BYTES for member in members):
                fail("canonical archive member exceeds bounded size")
            if sum(member.size for member in members) > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                fail("canonical archive exceeds bounded uncompressed total")

            payloads: dict[str, bytes] = {}
            for member in members:
                extracted = archive.extractfile(member)
                if extracted is None:
                    fail(f"unable to read canonical archive member: {member.name}")
                payload = extracted.read(MAX_ARCHIVE_MEMBER_BYTES + 1)
                if len(payload) != member.size:
                    fail(f"canonical archive member truncated/oversized: {member.name}")
                payloads[member.name] = payload
    except (tarfile.TarError, OSError) as exc:
        fail(f"unable to parse canonical archive: {exc}")

    plan_sha = hashlib.sha256(payloads[PLAN_MEMBER]).hexdigest()
    if plan_sha != EXPECTED_PLAN_SHA256:
        fail(f"master plan SHA-256 mismatch: {plan_sha}")

    try:
        registry = json.loads(payloads[REGISTRY_JSON_MEMBER].decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        fail(f"JSON source registry is invalid: {exc}")
    rows = registry.get("registry")
    if not isinstance(rows, list) or len(rows) != EXPECTED_SOURCE_REGISTRY_ENTRIES:
        fail("JSON source registry row count mismatch")

    names: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            fail("JSON source registry contains non-object row")
        name = row.get("name")
        if not isinstance(name, str) or not name:
            fail("JSON source registry contains missing/malformed name")
        names.append(name.casefold())
        if row.get("admission_status") != "NOT_ADMITTED":
            fail("frozen JSON source registry unexpectedly admits a source")
    if len(set(names)) != EXPECTED_SOURCE_REGISTRY_ENTRIES:
        fail("JSON source registry names are not unique")

    counts = registry.get("counts")
    if not isinstance(counts, dict):
        fail("JSON source registry counts missing")
    if counts.get("frozen_v1_5_named_entries") != 397:
        fail("frozen V1.5 source count mismatch")
    if counts.get("post_v1_5_new_top_level_named_entries") != 5:
        fail("post-V1.5 source count mismatch")
    if counts.get("current_accounted_named_entries") != EXPECTED_SOURCE_REGISTRY_ENTRIES:
        fail("current accounted source count mismatch")

    try:
        csv_rows = list(
            csv.DictReader(
                io.StringIO(payloads[REGISTRY_CSV_MEMBER].decode("utf-8"))
            )
        )
    except UnicodeError as exc:
        fail(f"CSV source registry is not UTF-8: {exc}")
    if len(csv_rows) != EXPECTED_SOURCE_REGISTRY_ENTRIES:
        fail("CSV source registry row count mismatch")
    csv_names = [row.get("name", "").casefold() for row in csv_rows]
    if any(not name for name in csv_names) or len(set(csv_names)) != EXPECTED_SOURCE_REGISTRY_ENTRIES:
        fail("CSV source registry names are missing/non-unique")
    if set(csv_names) != set(names):
        fail("CSV/JSON source registry names disagree")

    for name in EXPECTED_ARCHIVE_MEMBERS - {
        PLAN_MEMBER,
        REGISTRY_JSON_MEMBER,
        REGISTRY_CSV_MEMBER,
    }:
        if not payloads[name].strip():
            fail(f"canonical archive member is empty: {name}")


def require_comparison_sha(value: str | None) -> str:
    """Resolve the commit whose ancestry the immutable baseline must cover.

    On `pull_request` this is the exact PR base SHA; on `push` to `main` it is
    the pushed canonical commit. Baseline verification must never silently
    degrade to identity-only checking, so a missing or malformed comparison SHA
    fails closed.
    """
    candidate = (value or "").strip()
    if not candidate:
        fail("immutable baseline comparison SHA could not be established")
    if not OBJECT_SHA_RE.fullmatch(candidate):
        fail(f"immutable baseline comparison SHA is malformed: {candidate!r}")
    return candidate


def verify_remote_baseline(
    client: GitHubClient,
    pr_base_sha: str | None,
) -> None:
    response = client.json(
        f"https://api.github.com/repos/{REPOSITORY}/contents/"
        f"{urllib.parse.quote(BASELINE_PATH, safe='/')}?ref={BASELINE_COMMIT_SHA}"
    )
    require_object_identity(
        "immutable baseline blob", BASELINE_BLOB_SHA, response.get("sha")
    )
    if response.get("encoding") != "base64":
        fail("immutable baseline API response encoding is not base64")
    encoded = response.get("content")
    if not isinstance(encoded, str):
        fail("immutable baseline API response has no content")
    try:
        baseline = json.loads(base64.b64decode(encoded).decode("utf-8"))
    except (ValueError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"immutable baseline payload is invalid: {exc}")
    for key, expected in EXPECTED_BASELINE.items():
        if baseline.get(key) != expected:
            fail(f"immutable baseline mismatch for {key}")

    if pr_base_sha:
        if not OBJECT_SHA_RE.fullmatch(pr_base_sha):
            fail(f"PR base SHA is malformed: {pr_base_sha!r}")
        if pr_base_sha.lower() != BASELINE_BASE_MAIN_SHA:
            compare = client.json(
                f"https://api.github.com/repos/{REPOSITORY}/compare/"
                f"{BASELINE_BASE_MAIN_SHA}...{pr_base_sha.lower()}"
            )
            if compare.get("status") not in {"ahead", "identical"}:
                fail("PR base is not the immutable foundation base or a descendant")


def compare_base_controlled(
    candidate: RepositoryView,
    policy_base: RepositoryView,
) -> None:
    for relative in sorted(BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, MAX_POLICY_FILE_BYTES)
        if candidate_bytes != base_bytes:
            fail(f"base-controlled policy/governance path changed: {relative}")


def verify_base_path_preservation(
    candidate_paths: set[str],
    base_paths: set[str],
) -> None:
    """Every tracked path present in the trusted base must still be present.

    `REQUIRED_PATHS` is a deliberate subset, not a complete inventory, so
    presence is derived from the trusted base checkout itself:

        TRUSTED_BASE_EXISTING_PATH -> candidate may preserve
        TRUSTED_BASE_EXISTING_PATH -> candidate may modify only if other policy permits
        TRUSTED_BASE_EXISTING_PATH -> candidate may not silently delete
        NEW_CANDIDATE_PATH         -> allowed only through the stage allowlist

    This is presence preservation, not a content freeze, and it states the S1
    admission policy's current fail-closed behavior rather than an eternal
    prohibition; a separately governed future migration may define deletion
    semantics.
    """
    deleted = sorted(base_paths - candidate_paths)
    if deleted:
        fail("trusted-base tracked path deleted by candidate: " + ", ".join(deleted))


def compare_against_policy_base(
    candidate: RepositoryView,
    candidate_paths: set[str],
    policy_base: RepositoryView,
) -> None:
    """Authoritative comparison: presence preservation for every trusted-base
    tracked path, plus byte equality for base-controlled paths."""
    verify_base_path_preservation(
        candidate_paths, validate_entries(policy_base.entries())
    )
    compare_base_controlled(candidate, policy_base)


def verify_view(
    view: RepositoryView,
    *,
    policy_base: RepositoryView | None = None,
) -> str:
    paths = validate_entries(view.entries())
    stage = classify_stage(paths)
    validate_allowed_paths(paths, stage)

    if view.read_bytes("src/.gitkeep", 1):
        fail("src/.gitkeep must be empty")

    verify_reviewer_configs(view)
    verify_dependency_register(view)
    verify_archive(view)
    verify_stage_b_templates(view, stage)

    if any(path.startswith(".github/repair-payload/") for path in paths):
        fail("repair payload leaked into active tree")
    if "docs/canonical/CODEX_SECURITY_REVIEW_POLICY.md" in paths:
        fail("duplicate canonical security-review policy detected")
    for path in paths:
        name = PurePosixPath(path).name
        if (
            path.startswith(".github/workflows/")
            and (
                name.startswith("repair-canonical-archive")
                or name.startswith("finalize-canonical-archive")
            )
            and (name.endswith(".yml") or name.endswith(".yaml"))
        ):
            fail(f"temporary repair workflow leaked into active tree: {path}")

    if policy_base is not None:
        compare_against_policy_base(view, paths, policy_base)

    return stage


def expect_failure(label: str, func, *args, **kwargs) -> None:
    try:
        func(*args, **kwargs)
    except PolicyError:
        return
    fail(f"negative self-test unexpectedly passed: {label}")


def expect_failure_matching(label: str, expected_reason: str, func, *args, **kwargs) -> None:
    """Assert both that the policy rejects and that it rejects for the intended
    reason, so a probe cannot pass incidentally."""
    try:
        func(*args, **kwargs)
    except PolicyError as exc:
        if expected_reason not in str(exc):
            fail(
                f"negative self-test failed for the wrong reason: {label}: "
                f"expected {expected_reason!r} in {str(exc)!r}"
            )
        return
    fail(f"negative self-test unexpectedly passed: {label}")


class MemoryView(RepositoryView):
    def __init__(
        self,
        files: dict[str, bytes],
        modes: dict[str, str] | None = None,
    ):
        self.files = dict(files)
        self.modes = dict(modes or {})

    def entries(self) -> list[TrackedEntry]:
        return [
            TrackedEntry(mode=self.modes.get(path, "100644"), path=path)
            for path in self.files
        ]

    def read_bytes(self, relative: str, limit: int) -> bytes:
        if relative not in self.files:
            fail(f"memory view missing file: {relative}")
        data = self.files[relative]
        if len(data) > limit:
            fail(f"memory-view file exceeds bound: {relative}")
        return data


class StubGitHubClient(GitHubClient):
    """Serve canned Git data API responses so object-identity binding can be
    proven deterministically against the real RemoteRepositoryView logic."""

    def __init__(self, responses: Mapping[str, Mapping[str, object]]):
        super().__init__(None)
        self.responses = dict(responses)

    def json(self, url: str) -> Mapping[str, object]:
        if url not in self.responses:
            fail(f"stub GitHub client has no canned response for: {url}")
        return self.responses[url]


def lock_document(packages: Iterable[Mapping[str, object]]) -> bytes:
    """Render a Cargo.lock-shaped TOML document for deterministic self-tests."""
    lines = ["version = 4", ""]
    for package in packages:
        lines.append("[[package]]")
        lines.append(f'name = "{package["name"]}"')
        lines.append(f'version = "{package["version"]}"')
        source = package.get("source")
        if source is not None:
            lines.append(f'source = "{source}"')
            lines.append(f'checksum = "{"a" * 64}"')
        dependencies = package.get("dependencies")
        if dependencies is not None:
            rendered = ", ".join(f'"{item}"' for item in dependencies)
            lines.append(f"dependencies = [{rendered}]")
        lines.append("")
    return "\n".join(lines).encode("utf-8")


# A structurally valid Stage-B2 fixture. Hardening must not degrade into
# "reject every lock", so this must keep passing.
VALID_LOCK_PACKAGES = [
    {
        "name": "wepld-desktop",
        "version": "0.0.0",
        "dependencies": ["tauri", "tauri-build", "wepld-contracts"],
    },
    {
        "name": "wepld-contracts",
        "version": "0.0.0",
        "dependencies": ["serde", "serde_json"],
    },
    {"name": "wepld-core", "version": "0.0.0", "dependencies": ["wepld-contracts"]},
    {
        "name": "tauri",
        "version": "2.11.5",
        "source": CRATES_IO_SOURCE,
        "dependencies": ["serde", "serde_json"],
    },
    {"name": "tauri-build", "version": "2.6.3", "source": CRATES_IO_SOURCE},
    {"name": "serde", "version": "1.0.229", "source": CRATES_IO_SOURCE},
    {"name": "serde_json", "version": "1.0.151", "source": CRATES_IO_SOURCE},
]


def selftest() -> None:
    base_paths = set(REQUIRED_PATHS) | {"README.md", "src/.gitkeep"}
    if classify_stage(base_paths) != "S1_PLANNING_ONLY":
        fail("self-test: planning stage classification failed")
    validate_allowed_paths(base_paths, "S1_PLANNING_ONLY")

    expect_failure(
        "partial Stage B candidate",
        classify_stage,
        base_paths | {"Cargo.toml"},
    )

    stage_b = base_paths | set(STAGE_B_INPUT_PATHS)
    if classify_stage(stage_b) != "S1_DEPENDENCY_RESOLUTION_INPUT":
        fail("self-test: Stage B input classification failed")
    validate_allowed_paths(stage_b, "S1_DEPENDENCY_RESOLUTION_INPUT")

    stage_b_locked = stage_b | {STAGE_B_LOCK_PATH}
    if classify_stage(stage_b_locked) != "S1_DEPENDENCY_RESOLUTION_LOCKED":
        fail("self-test: Stage B locked classification failed")
    validate_allowed_paths(stage_b_locked, "S1_DEPENDENCY_RESOLUTION_LOCKED")

    for label, bad_path in {
        "arbitrary package manager": "package.json",
        "root implementation": "src/main.rs",
        "extra Rust module": "crates/core/src/extra.rs",
        "later-slice crate": "crates/worker/Cargo.toml",
        "extra workflow": ".github/workflows/unreviewed.yml",
    }.items():
        expect_failure(
            label,
            validate_allowed_paths,
            stage_b | {bad_path},
            "S1_DEPENDENCY_RESOLUTION_INPUT",
        )

    expect_failure(
        "symlink index mode",
        validate_entries,
        [TrackedEntry(mode="120000", path="docs/x.md")],
    )
    expect_failure(
        "gitlink index mode",
        validate_entries,
        [TrackedEntry(mode="160000", path="vendor/x")],
    )
    expect_failure(
        "case-fold path collision",
        validate_entries,
        [
            TrackedEntry(mode="100644", path="docs/A.md"),
            TrackedEntry(mode="100644", path="docs/a.md"),
        ],
    )

    markdown_only = base_paths | {"docs/claim-SOURCE_ACQUISITION_CHECK-PASS.md"}
    if classify_stage(markdown_only) != "S1_PLANNING_ONLY":
        fail("self-test: Markdown claim changed stage")

    files = {
        relative: expected.encode("utf-8")
        for relative, expected in STAGE_B_TEXT.items()
    }
    view = MemoryView(files)
    verify_stage_b_templates(view, "S1_DEPENDENCY_RESOLUTION_INPUT")

    mutations = {
        "tauri-plugin-shell": (
            "apps/desktop/src-tauri/Cargo.toml",
            DESKTOP_CARGO + '\ntauri-plugin-shell = "=2.3.5"\n',
        ),
        "direct Core tokio": (
            "crates/core/Cargo.toml",
            CORE_CARGO + '\ntokio = "=1.0.0"\n',
        ),
        "network dependency": (
            "crates/core/Cargo.toml",
            CORE_CARGO + '\nreqwest = "=0.13.0"\n',
        ),
        "wildcard dependency": (
            "crates/core/Cargo.toml",
            CORE_CARGO + '\nserde = "*"\n',
        ),
        "git dependency": (
            "crates/core/Cargo.toml",
            CORE_CARGO + '\nserde = { git = "https://example.invalid/x" }\n',
        ),
        "product behavior in skeleton": (
            "crates/core/src/main.rs",
            '#![forbid(unsafe_code)]\n\nfn main() { println!("product"); }\n',
        ),
    }
    for label, (path, bad_text) in mutations.items():
        mutated = dict(files)
        mutated[path] = bad_text.encode("utf-8")
        expect_failure(
            label,
            verify_stage_b_templates,
            MemoryView(mutated),
            "S1_DEPENDENCY_RESOLUTION_INPUT",
        )

    bad_git_lock = b"""version = 4

[[package]]
name = "x"
version = "1.0.0"
source = "git+https://example.invalid/x"
checksum = "0000000000000000000000000000000000000000000000000000000000000000"
"""
    expect_failure("git Cargo.lock source", validate_lock_bytes, bad_git_lock)

    bad_alt_registry_lock = b"""version = 4

[[package]]
name = "x"
version = "1.0.0"
source = "registry+https://example.invalid/index"
checksum = "0000000000000000000000000000000000000000000000000000000000000000"
"""
    expect_failure(
        "alternate Cargo registry",
        validate_lock_bytes,
        bad_alt_registry_lock,
    )

    # Base-controlled comparison must fail closed on a changed policy file.
    control_files = {path: b"same" for path in BASE_CONTROLLED_PATHS}
    candidate_files = dict(control_files)
    candidate_files[".github/scripts/wepld_integrity.py"] = b"changed"
    expect_failure_matching(
        "base-controlled policy mutation",
        "base-controlled policy/governance path changed",
        compare_base_controlled,
        MemoryView(candidate_files),
        MemoryView(control_files),
    )

    selftest_helper_contract()
    selftest_baseline_comparison_sha()
    selftest_baseline_blob_identity()
    selftest_object_identity()
    selftest_lock_graph()
    selftest_base_path_preservation()

    print("wepld integrity policy self-tests: PASS")


def selftest_helper_contract() -> None:
    """The reason-asserting helper must not accept a correct failure that
    failed for the wrong reason, nor a non-failure."""
    try:
        expect_failure_matching(
            "meta", "UNRELATED_REASON", require_comparison_sha, ""
        )
    except PolicyError as exc:
        if "failed for the wrong reason" not in str(exc):
            fail("self-test: helper mis-reported a wrong-reason failure")
    else:
        fail("self-test: helper accepted a failure with the wrong reason")

    try:
        expect_failure_matching("meta", "anything", require_comparison_sha, "a" * 40)
    except PolicyError as exc:
        if "unexpectedly passed" not in str(exc):
            fail("self-test: helper mis-reported a missing failure")
    else:
        fail("self-test: helper accepted a non-failure")


def selftest_baseline_comparison_sha() -> None:
    """R1: baseline verification must never run without a comparison identity."""
    expect_failure_matching(
        "absent baseline comparison SHA",
        "comparison SHA could not be established",
        require_comparison_sha,
        "",
    )
    expect_failure_matching(
        "missing baseline comparison SHA",
        "comparison SHA could not be established",
        require_comparison_sha,
        None,
    )
    expect_failure_matching(
        "malformed baseline comparison SHA",
        "comparison SHA is malformed",
        require_comparison_sha,
        "not-a-sha",
    )
    if require_comparison_sha("a" * 40) != "a" * 40:
        fail("self-test: a valid comparison SHA must be preserved")


def selftest_baseline_blob_identity() -> None:
    """R5: baseline Contents response must bind to the canonical blob identity."""
    baseline_url = (
        f"https://api.github.com/repos/{REPOSITORY}/contents/"
        f"{urllib.parse.quote(BASELINE_PATH, safe='/')}?ref={BASELINE_COMMIT_SHA}"
    )
    baseline_content = base64.b64encode(
        json.dumps(EXPECTED_BASELINE, sort_keys=True).encode("utf-8")
    ).decode("ascii")

    def client_for(
        blob_identity: object,
        encoding: object = "base64",
    ) -> StubGitHubClient:
        return StubGitHubClient(
            {
                baseline_url: {
                    "sha": blob_identity,
                    "encoding": encoding,
                    "content": baseline_content,
                }
            }
        )

    expect_failure_matching(
        "immutable baseline wrong returned blob SHA",
        "returned immutable baseline blob object identity does not match the requested object",
        verify_remote_baseline,
        client_for("b" * 40),
        BASELINE_BASE_MAIN_SHA,
    )
    expect_failure_matching(
        "immutable baseline missing returned blob SHA",
        "returned immutable baseline blob object identity is malformed",
        verify_remote_baseline,
        client_for(None),
        BASELINE_BASE_MAIN_SHA,
    )
    expect_failure_matching(
        "immutable baseline malformed returned blob SHA",
        "returned immutable baseline blob object identity is malformed",
        verify_remote_baseline,
        client_for("not-a-sha"),
        BASELINE_BASE_MAIN_SHA,
    )
    expect_failure_matching(
        "immutable baseline wrong encoding",
        "immutable baseline API response encoding is not base64",
        verify_remote_baseline,
        client_for(BASELINE_BLOB_SHA, "utf-8"),
        BASELINE_BASE_MAIN_SHA,
    )
    verify_remote_baseline(client_for(BASELINE_BLOB_SHA), BASELINE_BASE_MAIN_SHA)


def selftest_object_identity() -> None:
    """R2: tree/blob responses must be bound to the requested object identity."""
    expect_failure_matching(
        "mismatched returned identity",
        "does not match the requested object",
        require_object_identity,
        "tree",
        "a" * 40,
        "b" * 40,
    )
    expect_failure_matching(
        "malformed returned identity",
        "returned blob object identity is malformed",
        require_object_identity,
        "blob",
        "a" * 40,
        "zz",
    )
    expect_failure_matching(
        "absent returned identity",
        "returned blob object identity is malformed",
        require_object_identity,
        "blob",
        "a" * 40,
        None,
    )
    # Case-insensitive equality is the existing SHA normalization policy.
    require_object_identity("tree", "a" * 40, "A" * 40)

    repository = "TheHalfMoon/wepld"
    commit_sha, tree_sha, blob_sha = "1" * 40, "2" * 40, "3" * 40
    commit_url = f"https://api.github.com/repos/{repository}/git/commits/{commit_sha}"
    tree_url = (
        f"https://api.github.com/repos/{repository}/git/trees/{tree_sha}?recursive=1"
    )
    blob_url = f"https://api.github.com/repos/{repository}/git/blobs/{blob_sha}"
    payload = b"canonical"
    entries = [
        {
            "type": "blob",
            "path": "docs/example.md",
            "mode": "100644",
            "sha": blob_sha,
            "size": len(payload),
        }
    ]

    def responses(tree_identity: str, blob_identity: str):
        return {
            commit_url: {"sha": commit_sha, "tree": {"sha": tree_sha}},
            tree_url: {"sha": tree_identity, "truncated": False, "tree": entries},
            blob_url: {
                "sha": blob_identity,
                "encoding": "base64",
                "content": base64.b64encode(payload).decode("ascii"),
            },
        }

    # A syntactically valid tree response with the wrong identity is rejected
    # before any of its entries are consumed.
    expect_failure_matching(
        "tree response with wrong returned SHA",
        "returned tree object identity does not match the requested object",
        RemoteRepositoryView,
        repository,
        commit_sha,
        StubGitHubClient(responses("4" * 40, blob_sha)),
    )

    # A syntactically valid blob response with the wrong identity is rejected
    # before its content is decoded.
    wrong_blob = RemoteRepositoryView(
        repository, commit_sha, StubGitHubClient(responses(tree_sha, "5" * 40))
    )
    expect_failure_matching(
        "blob response with wrong returned SHA",
        "returned blob object identity does not match the requested object",
        wrong_blob.read_bytes,
        "docs/example.md",
        MAX_POLICY_FILE_BYTES,
    )

    honest = RemoteRepositoryView(
        repository, commit_sha, StubGitHubClient(responses(tree_sha, blob_sha))
    )
    if honest.read_bytes("docs/example.md", MAX_POLICY_FILE_BYTES) != payload:
        fail("self-test: honest tree/blob responses must remain readable")


def selftest_lock_graph() -> None:
    """R3: structural constraints a fabricated package list cannot satisfy."""
    validate_lock_bytes(lock_document(VALID_LOCK_PACKAGES))

    expect_failure_matching(
        "fabricated minimal lock",
        "source-less Cargo.lock package is not an expected Stage-B workspace member",
        validate_lock_bytes,
        lock_document(
            [
                {"name": name, "version": version}
                for name, version in sorted(REQUIRED_LOCK_PACKAGES)
            ]
        ),
    )
    expect_failure_matching(
        "duplicate lock package identity",
        "duplicate Cargo.lock package identity",
        validate_lock_bytes,
        lock_document(VALID_LOCK_PACKAGES + [VALID_LOCK_PACKAGES[-1]]),
    )
    expect_failure_matching(
        "unexpected source-less package",
        "source-less Cargo.lock package is not an expected Stage-B workspace member",
        validate_lock_bytes,
        lock_document(VALID_LOCK_PACKAGES + [{"name": "smuggled", "version": "0.1.0"}]),
    )

    missing_edge = [dict(package) for package in VALID_LOCK_PACKAGES]
    missing_edge[0]["dependencies"] = ["tauri", "wepld-contracts"]
    expect_failure_matching(
        "missing required direct workspace edge",
        "missing required direct dependency edges for wepld-desktop",
        validate_lock_bytes,
        lock_document(missing_edge),
    )

    # A second `tauri` in the lock must not let the workspace edge point at the
    # unexpected version.
    wrong_edge_version = [dict(package) for package in VALID_LOCK_PACKAGES]
    wrong_edge_version[0]["dependencies"] = [
        "tauri 2.11.6",
        "tauri-build",
        "wepld-contracts",
    ]
    wrong_edge_version.append(
        {"name": "tauri", "version": "2.11.6", "source": CRATES_IO_SOURCE}
    )
    expect_failure_matching(
        "required edge resolving to the wrong version",
        "missing required direct dependency edges for wepld-desktop",
        validate_lock_bytes,
        lock_document(wrong_edge_version),
    )

    dangling = [dict(package) for package in VALID_LOCK_PACKAGES]
    dangling[1]["dependencies"] = ["serde", "serde_json", "nonexistent-crate"]
    expect_failure_matching(
        "dependency reference to a nonexistent package",
        "does not resolve to any package in the lock",
        validate_lock_bytes,
        lock_document(dangling),
    )

    unresolved = [dict(package) for package in VALID_LOCK_PACKAGES]
    unresolved[1]["dependencies"] = ["serde 9.9.9", "serde_json"]
    expect_failure_matching(
        "dependency reference to an unresolved version",
        "does not resolve to a package in the lock",
        validate_lock_bytes,
        lock_document(unresolved),
    )

    ambiguous = [dict(package) for package in VALID_LOCK_PACKAGES]
    ambiguous.append({"name": "serde", "version": "1.0.230", "source": CRATES_IO_SOURCE})
    expect_failure_matching(
        "ambiguous unversioned dependency reference",
        "ambiguous unversioned Cargo.lock dependency reference",
        validate_lock_bytes,
        lock_document(ambiguous),
    )

    malformed = [dict(package) for package in VALID_LOCK_PACKAGES]
    malformed[2]["dependencies"] = [""]
    expect_failure_matching(
        "malformed dependency reference",
        "Cargo.lock dependency reference is malformed",
        validate_lock_bytes,
        lock_document(malformed),
    )


def selftest_base_path_preservation() -> None:
    """R4: trusted-base tracked evidence cannot silently disappear."""
    optional_evidence = (
        "docs/acquisition/evidence/GREPTILE_OFFICIAL_BEHAVIOR_EVIDENCE_2026-08-15.md"
    )
    base_files = {path: b"same" for path in BASE_CONTROLLED_PATHS}
    base_files[optional_evidence] = b"evidence"

    candidate_files = {path: b"same" for path in BASE_CONTROLLED_PATHS}
    expect_failure_matching(
        "silently deleted optional trusted-base evidence",
        f"trusted-base tracked path deleted by candidate: {optional_evidence}",
        compare_against_policy_base,
        MemoryView(candidate_files),
        set(candidate_files),
        MemoryView(base_files),
    )

    # Preserving every base path while adding one is allowed here; additions are
    # governed by the stage allowlist elsewhere.
    added = dict(base_files)
    added["docs/new-note.md"] = b"added"
    compare_against_policy_base(MemoryView(added), set(added), MemoryView(base_files))

    # Modifying a non-base-controlled document remains allowed.
    modified = dict(base_files)
    modified[optional_evidence] = b"revised evidence"
    compare_against_policy_base(
        MemoryView(modified), set(modified), MemoryView(base_files)
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("selftest")

    local = subparsers.add_parser("verify-local")
    local.add_argument("--root", required=True)
    local.add_argument("--remote-baseline", action="store_true")
    local.add_argument("--github-token-env", default="GITHUB_TOKEN")
    local.add_argument("--pr-base-sha")

    remote = subparsers.add_parser("verify-remote")
    remote.add_argument("--repository", required=True)
    remote.add_argument("--sha", required=True)
    remote.add_argument("--policy-root", required=True)
    remote.add_argument("--github-token-env", default="GITHUB_TOKEN")
    remote.add_argument("--pr-base-sha", required=True)

    return parser.parse_args(argv)


def print_success(stage: str, mode: str) -> None:
    print("wepld integrity verification: PASS")
    print(f"mode={mode}")
    print(f"stage={stage}")
    print(f"canonical_archive_sha256={EXPECTED_ARCHIVE_SHA256}")
    print(f"master_plan_sha256={EXPECTED_PLAN_SHA256}")
    print(f"source_registry_entries={EXPECTED_SOURCE_REGISTRY_ENTRIES}")
    print("source_admission=0")
    print("cubic_provider_effective_state=NOT_PROVEN_SAFE_BY_REPOSITORY_POLICY")
    print("product_implementation_authorized=NO")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.command == "selftest":
            selftest()
            return 0

        token = os.environ.get(args.github_token_env) or None
        client = GitHubClient(token)

        if args.command == "verify-local":
            view = LocalRepositoryView(Path(args.root))
            stage = verify_view(view)
            if args.remote_baseline:
                verify_remote_baseline(client, require_comparison_sha(args.pr_base_sha))
            print_success(stage, "LOCAL_CHECKOUT")
            return 0

        policy_base = LocalRepositoryView(Path(args.policy_root))
        candidate = RemoteRepositoryView(args.repository, args.sha, client)
        stage = verify_view(candidate, policy_base=policy_base)
        verify_remote_baseline(client, require_comparison_sha(args.pr_base_sha))
        print_success(stage, "REMOTE_CANDIDATE_DATA_ONLY")
        return 0

    except PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
