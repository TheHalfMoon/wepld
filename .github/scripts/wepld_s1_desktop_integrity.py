#!/usr/bin/env python3
"""Canonical S1-009 policy runner with fail-closed baseline ancestry fallback.

The large S1-009 admission implementation is frozen as a sibling Git blob. This
runner binds that blob before import, extends the controlled-path set to cover
it, and preserves the immutable-baseline invariant if GitHub's compare endpoint
is unavailable by walking bounded, identity-bound Git commit parents.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import wepld_integrity as foundation

IMPL_SCRIPT = ".github/scripts/wepld_s1_desktop_integrity_impl.py"
EXPECTED_IMPL_GIT_BLOB_SHA1 = "ff2b21630c98ba9f001b45554e95116889e83141"
MAX_BASELINE_ANCESTRY_COMMITS = 512
MAX_BASELINE_PARENTS_PER_COMMIT = 16


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_impl_before_import() -> None:
    impl_path = Path(__file__).resolve().with_name("wepld_s1_desktop_integrity_impl.py")
    try:
        data = impl_path.read_bytes()
    except OSError as exc:
        foundation.fail(f"unable to read frozen S1-009 policy implementation: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_IMPL_GIT_BLOB_SHA1:
        foundation.fail(
            "frozen S1-009 policy implementation drifted: "
            f"expected={EXPECTED_IMPL_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_impl_before_import()
import wepld_s1_desktop_integrity_impl as impl  # noqa: E402

impl.EXTENSION_CONTROLLED_PATHS = frozenset(
    set(impl.EXTENSION_CONTROLLED_PATHS) | {IMPL_SCRIPT}
)
impl.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
    set(impl.prior.EXTENSION_CONTROLLED_PATHS) | {IMPL_SCRIPT}
)


def _compare_url(comparison_sha: str) -> str:
    return (
        f"https://api.github.com/repos/{foundation.REPOSITORY}/compare/"
        f"{foundation.BASELINE_BASE_MAIN_SHA}...{comparison_sha.lower()}"
    )


def _is_compare_transport_failure(
    exc: foundation.PolicyError,
    comparison_sha: str,
) -> bool:
    return str(exc).startswith(
        f"GitHub API request failed for {_compare_url(comparison_sha)}:"
    )


def _verify_baseline_ancestry_by_parent_walk(
    client: foundation.GitHubClient,
    descendant_sha: str,
) -> None:
    descendant = foundation.require_comparison_sha(descendant_sha).lower()
    target = foundation.BASELINE_BASE_MAIN_SHA.lower()
    pending = [descendant]
    visited: set[str] = set()

    while pending:
        current = pending.pop()
        if current == target:
            return
        if current in visited:
            continue
        if len(visited) >= MAX_BASELINE_ANCESTRY_COMMITS:
            foundation.fail(
                "immutable baseline ancestry traversal exceeded bounded commit limit"
            )
        visited.add(current)

        commit = client.json(
            f"https://api.github.com/repos/{foundation.REPOSITORY}/git/commits/{current}"
        )
        foundation.require_object_identity(
            "baseline ancestry commit", current, commit.get("sha")
        )
        parents = commit.get("parents")
        if not isinstance(parents, list):
            foundation.fail("baseline ancestry commit parents payload is malformed")
        if len(parents) > MAX_BASELINE_PARENTS_PER_COMMIT:
            foundation.fail("baseline ancestry commit exceeds bounded parent fanout")

        for parent in parents:
            if not isinstance(parent, dict):
                foundation.fail("baseline ancestry parent payload is malformed")
            parent_sha = parent.get("sha")
            if (
                not isinstance(parent_sha, str)
                or not foundation.OBJECT_SHA_RE.fullmatch(parent_sha)
            ):
                foundation.fail("baseline ancestry parent SHA is malformed")
            normalized = parent_sha.lower()
            if normalized == current:
                foundation.fail("baseline ancestry commit self-parent detected")
            if normalized not in visited:
                pending.append(normalized)

    foundation.fail("PR base is not the immutable foundation base or a descendant")


def verify_remote_baseline(
    client: foundation.GitHubClient,
    comparison_sha: str | None,
) -> None:
    comparison = foundation.require_comparison_sha(comparison_sha).lower()
    try:
        foundation.verify_remote_baseline(client, comparison)
        return
    except foundation.PolicyError as exc:
        if not _is_compare_transport_failure(exc, comparison):
            raise

    _verify_baseline_ancestry_by_parent_walk(client, comparison)


def selftest_runner() -> None:
    target = foundation.BASELINE_BASE_MAIN_SHA.lower()
    descendant = "a" * 40
    root = "b" * 40

    direct = foundation.StubGitHubClient(
        {
            f"https://api.github.com/repos/{foundation.REPOSITORY}/git/commits/{descendant}": {
                "sha": descendant,
                "parents": [{"sha": target}],
            }
        }
    )
    _verify_baseline_ancestry_by_parent_walk(direct, descendant)

    missing = foundation.StubGitHubClient(
        {
            f"https://api.github.com/repos/{foundation.REPOSITORY}/git/commits/{root}": {
                "sha": root,
                "parents": [],
            }
        }
    )
    foundation.expect_failure_matching(
        "baseline ancestry missing",
        "PR base is not the immutable foundation base or a descendant",
        _verify_baseline_ancestry_by_parent_walk,
        missing,
        root,
    )

    malformed = foundation.StubGitHubClient(
        {
            f"https://api.github.com/repos/{foundation.REPOSITORY}/git/commits/{descendant}": {
                "sha": descendant,
                "parents": [{"sha": "not-a-sha"}],
            }
        }
    )
    foundation.expect_failure_matching(
        "malformed baseline parent",
        "baseline ancestry parent SHA is malformed",
        _verify_baseline_ancestry_by_parent_walk,
        malformed,
        descendant,
    )

    self_parent = foundation.StubGitHubClient(
        {
            f"https://api.github.com/repos/{foundation.REPOSITORY}/git/commits/{descendant}": {
                "sha": descendant,
                "parents": [{"sha": descendant}],
            }
        }
    )
    foundation.expect_failure_matching(
        "baseline self-parent",
        "baseline ancestry commit self-parent detected",
        _verify_baseline_ancestry_by_parent_walk,
        self_parent,
        descendant,
    )

    transport = foundation.PolicyError(
        f"GitHub API request failed for {_compare_url(descendant)}: "
        "HTTP Error 404: Not Found"
    )
    if not _is_compare_transport_failure(transport, descendant):
        foundation.fail("runner self-test: compare transport failure was not recognized")
    semantic = foundation.PolicyError(
        "PR base is not the immutable foundation base or a descendant"
    )
    if _is_compare_transport_failure(semantic, descendant):
        foundation.fail("runner self-test: semantic ancestry rejection triggered fallback")
    unrelated = foundation.PolicyError(
        "GitHub API request failed for https://api.github.com/repos/"
        f"{foundation.REPOSITORY}/contents/x: HTTP Error 404: Not Found"
    )
    if _is_compare_transport_failure(unrelated, descendant):
        foundation.fail("runner self-test: unrelated GitHub API failure triggered fallback")


def main(argv: list[str]) -> int:
    args = foundation.parse_args(argv)
    try:
        if args.command == "selftest":
            impl.selftest()
            selftest_runner()
            print("wepld S1 Desktop integrity runner self-tests: PASS")
            return 0

        token = os.environ.get(args.github_token_env) or None
        client = foundation.GitHubClient(token)

        if args.command == "verify-local":
            view = foundation.LocalRepositoryView(Path(args.root))
            stage = impl.verify_view(view)
            if args.remote_baseline:
                verify_remote_baseline(client, args.pr_base_sha)
            impl.print_success(stage, "LOCAL_CHECKOUT")
            return 0

        policy_base = foundation.LocalRepositoryView(Path(args.policy_root))
        candidate = foundation.RemoteRepositoryView(args.repository, args.sha, client)
        stage = impl.verify_view(candidate, policy_base=policy_base)
        verify_remote_baseline(client, args.pr_base_sha)
        impl.print_success(stage, "REMOTE_CANDIDATE_DATA_ONLY")
        return 0

    except foundation.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
