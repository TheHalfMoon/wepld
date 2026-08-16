#!/usr/bin/env python3
"""Bounded S1 execution extension over the canonical acquisition integrity policy.

This file exists to make the first product-code stage explicit without weakening the
S1-003/S1-005 fail-closed machinery. The privileged pull_request_target workflow still
checks candidate Git objects as data only; candidate Rust is compiled/tested only in the
separate unprivileged pull_request workflow.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_execution_integrity.py"
CONTRACTS_WORKFLOW = ".github/workflows/s1-contracts.yml"
EXTENSION_CONTROLLED_PATHS = frozenset({POLICY_SCRIPT, CONTRACTS_WORKFLOW})

PROTOCOL_STAGE = "S1_PROTOCOL_CONTRACTS_CANDIDATE"
S1_006_MARKER_PATHS = frozenset(
    {
        "crates/contracts/src/frame.rs",
        "crates/contracts/src/protocol.rs",
        "crates/contracts/tests/protocol_v1.rs",
    }
)
S1_006_ALLOWED_PATHS = S1_006_MARKER_PATHS | {"crates/contracts/src/lib.rs"}
S1_005_EVIDENCE_PATH = (
    "specs/001-desktop-rust-trusted-core-handshake/"
    "s1-005-component-admission-evidence.md"
)
S1_006_FROZEN_EVIDENCE_PATHS = frozenset(
    {
        "docs/governance/DEPENDENCY_REGISTER.md",
        S1_005_EVIDENCE_PATH,
    }
)
MAX_S1_006_SOURCE_BYTES = 256_000

PROHIBITED_EFFECT_TOKENS = (
    "std::fs",
    "std::net",
    "std::process",
    "tokio::",
    "tauri::",
    "Command::new",
    "TcpStream",
    "TcpListener",
    "UdpSocket",
    "UnixStream",
    "UnixListener",
    "NamedPipe",
    "File::open",
    "File::create",
    "OpenOptions",
    "include!(",
    "include_bytes!(",
    "include_str!(",
    "#[path",
)

EXPECTED_FOUNDATION_WORKFLOW = """name: foundation-integrity

on:
  pull_request:
  push:
    branches:
      - main

permissions: {}

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout exact revision
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
          persist-credentials: false
          fetch-depth: 1
          lfs: false
          submodules: false

      - name: Run integrity policy self-tests
        shell: bash
        run: |
          set -euo pipefail
          python .github/scripts/wepld_s1_execution_integrity.py selftest

      # The checked-out policy must never be the sole owner of its own expected
      # digests, so both events also verify the separately governed immutable
      # baseline. The request is unauthenticated on purpose: the repository and
      # the baseline object are public, and no GITHUB_TOKEN may reach the policy
      # script.
      - name: Verify exact checked-out tree against the immutable baseline
        shell: bash
        env:
          WEPLD_COMPARISON_SHA: ${{ github.event.pull_request.base.sha || github.sha }}
        run: |
          set -euo pipefail
          if [ -z "${WEPLD_COMPARISON_SHA:-}" ]; then
            echo 'immutable baseline comparison SHA could not be established' >&2
            exit 1
          fi
          python .github/scripts/wepld_s1_execution_integrity.py verify-local \
            --root . \
            --remote-baseline \
            --pr-base-sha "$WEPLD_COMPARISON_SHA"
"""

EXPECTED_ADMISSION_WORKFLOW = """name: s1-admission-integrity

on:
  pull_request_target:
    branches:
      - main
    types:
      - opened
      - synchronize
      - reopened
      - ready_for_review

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout trusted base policy only
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          ref: ${{ github.event.pull_request.base.sha }}
          persist-credentials: false
          fetch-depth: 1
          lfs: false
          submodules: false

      - name: Run trusted policy self-tests
        shell: bash
        run: |
          set -euo pipefail
          python .github/scripts/wepld_s1_execution_integrity.py selftest

      - name: Inspect candidate Git objects as data only
        shell: bash
        env:
          GITHUB_TOKEN: ${{ github.token }}
          CANDIDATE_REPOSITORY: ${{ github.event.pull_request.head.repo.full_name }}
          CANDIDATE_SHA: ${{ github.event.pull_request.head.sha }}
          PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}
        run: |
          set -euo pipefail
          python .github/scripts/wepld_s1_execution_integrity.py verify-remote \
            --repository "$CANDIDATE_REPOSITORY" \
            --sha "$CANDIDATE_SHA" \
            --policy-root . \
            --pr-base-sha "$PR_BASE_SHA"
"""

EXPECTED_CONTRACTS_WORKFLOW = """name: s1-contracts

on:
  pull_request:
    branches:
      - main
    paths:
      - "Cargo.toml"
      - "Cargo.lock"
      - "rust-toolchain.toml"
      - "crates/contracts/**"
      - ".github/scripts/wepld_s1_execution_integrity.py"
      - ".github/workflows/s1-contracts.yml"

permissions: {}

jobs:
  contracts:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout exact candidate
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false
          fetch-depth: 1
          lfs: false
          submodules: false

      - name: Verify pinned Rust toolchain
        shell: bash
        run: |
          set -euo pipefail
          rustc --version --verbose
          cargo --version --verbose

      - name: Format contracts
        shell: bash
        run: |
          set -euo pipefail
          cargo fmt --package wepld-contracts -- --check

      - name: Clippy contracts
        shell: bash
        run: |
          set -euo pipefail
          cargo clippy --locked --package wepld-contracts --all-targets -- -D warnings

      - name: Test contracts
        shell: bash
        run: |
          set -euo pipefail
          cargo test --locked --package wepld-contracts --all-targets
"""


def classify_stage(paths: set[str]) -> str:
    markers = paths & S1_006_MARKER_PATHS
    if markers:
        missing_markers = S1_006_MARKER_PATHS - paths
        if missing_markers:
            base.fail(
                "partial S1-006 protocol candidate is prohibited; missing: "
                + ", ".join(sorted(missing_markers))
            )
        missing_component = base.STAGE_B_ALL_PATHS - paths
        if missing_component:
            base.fail(
                "S1-006 protocol candidate is missing frozen component inputs: "
                + ", ".join(sorted(missing_component))
            )
        if not any(
            path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/") for path in paths
        ):
            base.fail("S1-006 protocol candidate is missing frozen glib vendor subtree")
        return PROTOCOL_STAGE

    return base.classify_stage(paths - EXTENSION_CONTROLLED_PATHS)


def validate_allowed_paths(paths: set[str], stage: str) -> None:
    if stage != PROTOCOL_STAGE:
        base.validate_allowed_paths(paths - EXTENSION_CONTROLLED_PATHS, stage)
        return

    allowed = {path for path in paths if base.is_common_allowed(path)}
    allowed |= EXTENSION_CONTROLLED_PATHS
    allowed |= base.STAGE_B_ALL_PATHS
    allowed |= S1_006_ALLOWED_PATHS
    allowed |= {
        path
        for path in paths
        if path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/")
    }

    unexpected = sorted(paths - allowed)
    if unexpected:
        base.fail("tracked path outside S1-006 allowlist: " + ", ".join(unexpected))

    missing = sorted(base.REQUIRED_PATHS - paths)
    if missing:
        base.fail("required canonical path missing: " + ", ".join(missing))

    extra_root_src = sorted(
        path for path in paths if path.startswith("src/") and path != "src/.gitkeep"
    )
    if extra_root_src:
        base.fail(
            "root src/ remains a historical placeholder only: "
            + ", ".join(extra_root_src)
        )


def verify_policy_workflows(view: base.RepositoryView) -> None:
    base.read_text_exact(view, ".github/workflows/foundation-integrity.yml", EXPECTED_FOUNDATION_WORKFLOW)
    base.read_text_exact(view, ".github/workflows/s1-admission-integrity.yml", EXPECTED_ADMISSION_WORKFLOW)
    base.read_text_exact(view, CONTRACTS_WORKFLOW, EXPECTED_CONTRACTS_WORKFLOW)


def verify_extension_controlled_paths(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(EXTENSION_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if candidate_bytes != base_bytes:
            base.fail(f"base-controlled S1 execution policy path changed: {relative}")


def verify_protocol_component_base(
    view: base.RepositoryView,
    paths: set[str],
) -> None:
    expected_text = dict(base.STAGE_B_TEXT)
    expected_text["Cargo.toml"] = base.ROOT_CARGO_COMPONENT
    expected_text.pop("crates/contracts/src/lib.rs")

    for relative, expected in expected_text.items():
        base.read_text_exact(view, relative, expected)

    lock_bytes = view.read_bytes(base.STAGE_B_LOCK_PATH, base.MAX_LOCKFILE_BYTES)
    base.require_frozen_component_lock_identity(lock_bytes)
    base.validate_lock_bytes(lock_bytes, allow_frozen_glib=True)
    base.verify_frozen_glib_vendor(view, paths, base.COMPONENT_STAGE)


def verify_protocol_sources(view: base.RepositoryView) -> None:
    texts: dict[str, str] = {}
    for relative in sorted(S1_006_ALLOWED_PATHS):
        data = view.read_bytes(relative, MAX_S1_006_SOURCE_BYTES)
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"S1-006 Rust source is not UTF-8: {relative}: {exc}")
        if "\x00" in text:
            base.fail(f"S1-006 Rust source contains NUL: {relative}")
        texts[relative] = text

    for required_forbid in (
        "crates/contracts/src/lib.rs",
        "crates/contracts/tests/protocol_v1.rs",
    ):
        if "#![forbid(unsafe_code)]" not in texts[required_forbid]:
            base.fail(f"S1-006 crate/test root must forbid unsafe code: {required_forbid}")

    for relative, text in texts.items():
        for token in PROHIBITED_EFFECT_TOKENS:
            if token in text:
                base.fail(
                    f"S1-006 prohibited effect token {token!r} found in {relative}"
                )


def freeze_s1_005_evidence(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(S1_006_FROZEN_EVIDENCE_PATHS):
        candidate_bytes = candidate.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(relative, base.MAX_POLICY_FILE_BYTES)
        if candidate_bytes != base_bytes:
            base.fail(f"S1-006 candidate changed frozen S1-005 evidence: {relative}")


def verify_view(
    view: base.RepositoryView,
    *,
    policy_base: base.RepositoryView | None = None,
) -> str:
    paths = base.validate_entries(view.entries())
    stage = classify_stage(paths)
    validate_allowed_paths(paths, stage)

    if view.read_bytes("src/.gitkeep", 1):
        base.fail("src/.gitkeep must be empty")

    base.verify_reviewer_configs(view)
    base.verify_dependency_register(view)
    base.verify_archive(view)
    verify_policy_workflows(view)

    if stage == PROTOCOL_STAGE:
        verify_protocol_component_base(view, paths)
        verify_protocol_sources(view)
    else:
        base.verify_frozen_glib_vendor(view, paths, stage)
        base.verify_stage_b_templates(view, stage)

    if any(path.startswith(".github/repair-payload/") for path in paths):
        base.fail("repair payload leaked into active tree")
    if "docs/canonical/CODEX_SECURITY_REVIEW_POLICY.md" in paths:
        base.fail("duplicate canonical security-review policy detected")
    for path in paths:
        name = base.PurePosixPath(path).name
        if (
            path.startswith(".github/workflows/")
            and (
                name.startswith("repair-canonical-archive")
                or name.startswith("finalize-canonical-archive")
            )
            and (name.endswith(".yml") or name.endswith(".yaml"))
        ):
            base.fail(f"temporary repair workflow leaked into active tree: {path}")

    if policy_base is not None:
        base.verify_base_path_preservation(
            paths, base.validate_entries(policy_base.entries())
        )
        base.compare_base_controlled(view, policy_base)
        verify_extension_controlled_paths(view, policy_base)
        if stage == PROTOCOL_STAGE:
            freeze_s1_005_evidence(view, policy_base)

    return stage


def selftest() -> None:
    base.selftest()

    base_paths = set(base.REQUIRED_PATHS) | {"README.md", "src/.gitkeep"}
    component_paths = (
        base_paths
        | set(base.STAGE_B_ALL_PATHS)
        | {base.FROZEN_GLIB_VENDOR_PREFIX + "/src/variant_iter.rs"}
        | set(EXTENSION_CONTROLLED_PATHS)
    )

    if classify_stage(component_paths) != base.COMPONENT_STAGE:
        base.fail("S1 execution self-test: component stage compatibility failed")

    protocol_paths = component_paths | set(S1_006_MARKER_PATHS)
    if classify_stage(protocol_paths) != PROTOCOL_STAGE:
        base.fail("S1 execution self-test: protocol stage classification failed")
    validate_allowed_paths(protocol_paths, PROTOCOL_STAGE)

    one_marker = component_paths | {next(iter(S1_006_MARKER_PATHS))}
    base.expect_failure_matching(
        "partial S1-006 protocol stage",
        "partial S1-006 protocol candidate is prohibited",
        classify_stage,
        one_marker,
    )

    base.expect_failure_matching(
        "extra S1-006 Rust module",
        "tracked path outside S1-006 allowlist",
        validate_allowed_paths,
        protocol_paths | {"crates/contracts/src/extra.rs"},
        PROTOCOL_STAGE,
    )

    safe_sources = {
        "crates/contracts/src/lib.rs": b"#![forbid(unsafe_code)]\n",
        "crates/contracts/src/frame.rs": b"pub fn frame() {}\n",
        "crates/contracts/src/protocol.rs": b"pub fn protocol() {}\n",
        "crates/contracts/tests/protocol_v1.rs": b"#![forbid(unsafe_code)]\n",
    }
    verify_protocol_sources(base.MemoryView(safe_sources))

    unsafe_effect = dict(safe_sources)
    unsafe_effect["crates/contracts/src/frame.rs"] = b"use std::net::TcpStream;\n"
    base.expect_failure_matching(
        "network effect in S1-006",
        "S1-006 prohibited effect token",
        verify_protocol_sources,
        base.MemoryView(unsafe_effect),
    )

    print("wepld S1 execution integrity policy self-tests: PASS")


def print_success(stage: str, mode: str) -> None:
    if stage != PROTOCOL_STAGE:
        base.print_success(stage, mode)
        return

    print("wepld integrity verification: PASS")
    print(f"mode={mode}")
    print(f"stage={stage}")
    print(f"canonical_archive_sha256={base.EXPECTED_ARCHIVE_SHA256}")
    print(f"master_plan_sha256={base.EXPECTED_PLAN_SHA256}")
    print(f"source_registry_entries={base.EXPECTED_SOURCE_REGISTRY_ENTRIES}")
    print("source_admission=0")
    print("source_acquisition_check=PASS")
    print("runtime_dependency_admission=EXACT_S1_GRAPH")
    print("cubic_provider_effective_state=NOT_PROVEN_SAFE_BY_REPOSITORY_POLICY")
    print("product_implementation_authorized=S1_006_ONLY")


def main(argv: list[str]) -> int:
    args = base.parse_args(argv)
    try:
        if args.command == "selftest":
            selftest()
            return 0

        token = os.environ.get(args.github_token_env) or None
        client = base.GitHubClient(token)

        if args.command == "verify-local":
            view = base.LocalRepositoryView(Path(args.root))
            stage = verify_view(view)
            if args.remote_baseline:
                base.verify_remote_baseline(
                    client, base.require_comparison_sha(args.pr_base_sha)
                )
            print_success(stage, "LOCAL_CHECKOUT")
            return 0

        policy_base = base.LocalRepositoryView(Path(args.policy_root))
        candidate = base.RemoteRepositoryView(args.repository, args.sha, client)
        stage = verify_view(candidate, policy_base=policy_base)
        base.verify_remote_baseline(
            client, base.require_comparison_sha(args.pr_base_sha)
        )
        print_success(stage, "REMOTE_CANDIDATE_DATA_ONLY")
        return 0

    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
