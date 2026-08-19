#!/usr/bin/env python3
"""Repair S1-011 trusted-base qualification without widening product scope.

Canonical v19 freezes the reviewed S1-011 Rust templates and correctly uses the
trusted PR base in the privileged verify-remote path. Two qualification edges
need tightening before an S1-011 candidate can be accepted:

1. local candidate self-checks must not treat candidate-view template bytes as
   the trusted S1-011 policy source; and
2. RemoteRepositoryView.tree_identity() must expose blob identities as well as
   subtree identities so v19's exact trusted-base three-path delta compares the
   same Git object identity on remote candidates and local policy bases.

v20 preserves all v1-v19 behavior and repairs only those admission mechanics.
Policy/bootstrap candidates without S1-011 markers retain the existing local
self-check semantics. No product/runtime/dependency/UI bytes or S1-012+ authority
are added.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v20.py"
PRIOR_V19_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v19.py"
EXPECTED_PRIOR_V19_RUNNER_GIT_BLOB_SHA1 = "59d0d38ce3581a526906c4562f7a1b694af6cff4"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "17d47138679b15162f1f383057f760d61457a6bc30d883f990a6c2e7992019ad",
    ".github/workflows/s1-admission-integrity.yml": "1d3e067078d5554ee8c1b86b76e492b99f638bcac0793c57b20b851129d1dda7",
    ".github/workflows/s1-contracts.yml": "2ab777e867c60ef545e1b96dd4ff01546ca268eb794ce5bc620c98e9af0fbc27",
}

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v19_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v19.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-011 v19 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V19_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v19 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V19_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v19_runner_before_import()
import wepld_s1_shell_integrity_v19 as v19  # noqa: E402

v18 = v19.v18
v17 = v18.v17
v16 = v17.v16
v15 = v16.v15
v14 = v15.v14
v13 = v14.v13
v12 = v13.v12
v11 = v12.v11
v10 = v11.v10
v9 = v10.v9
v8 = v9.v8
v7 = v8.v7
v6 = v7.v6
v5 = v6.v5
v4 = v5.v4
v3 = v4.v3
v2 = v3.v2
shell = v19.shell


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V19_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V19_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v19 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V19_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v19._verify_policy_files(view)


def _remote_tree_identity(
    view: base.RemoteRepositoryView,
    relative: str,
) -> str | None:
    """Return the Git object identity for either a remote blob or subtree.

    LocalRepositoryView uses `git rev-parse HEAD:<path>`, which returns a blob
    SHA for files and a tree SHA for directories. Canonical RemoteRepositoryView
    stored both identities while loading the recursive tree, but its
    tree_identity() accessor exposed only `_trees`. v19's exact-delta comparison
    therefore saw every common candidate file as changed when the candidate was
    remote and the trusted base was local. Expose the already-validated blob SHA
    first, then the subtree SHA, preserving `None` for an absent path.
    """
    blob = view._blobs.get(relative)
    if blob is not None:
        blob_sha, _declared_size = blob
        if not base.OBJECT_SHA_RE.fullmatch(blob_sha):
            base.fail(f"candidate blob SHA is malformed: {relative}")
        return blob_sha.lower()

    tree_sha = view._trees.get(relative)
    if tree_sha is not None:
        if not base.OBJECT_SHA_RE.fullmatch(tree_sha):
            base.fail(f"candidate subtree SHA is malformed: {relative}")
        return tree_sha.lower()
    return None


def _is_s1_011_candidate(view: base.RepositoryView) -> bool:
    paths = base.validate_entries(view.entries())
    return v19._has_s1_011_markers(view, paths)


def verify_view(
    view: base.RepositoryView,
    *,
    policy_base: base.RepositoryView | None = None,
) -> str:
    if _is_s1_011_candidate(view) and policy_base is None:
        base.fail(
            "S1-011 authorization requires trusted policy base; "
            "candidate-view policy templates are not authority"
        )
    return v19.verify_view(view, policy_base=policy_base)


def _install_v20_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v19._install_v19_policy()

    # Repair the generic remote object-identity accessor before either the
    # local trusted-base path or privileged verify-remote path compares deltas.
    base.RemoteRepositoryView.tree_identity = _remote_tree_identity

    for module in (
        v19,
        v18,
        v17,
        v16,
        v15,
        v14,
        v13,
        v12,
        v11,
        v10,
        v9,
        v8,
        v7,
        v6,
        v5,
        v4,
        v3,
        v2,
        shell,
        shell.prior,
    ):
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    shell.verify_policy_files = _verify_policy_files
    shell.verify_view = verify_view
    _INSTALLED = True


def _selftest_remote_blob_identity() -> None:
    remote = object.__new__(base.RemoteRepositoryView)
    remote._blobs = {"file.txt": ("a" * 40, 7)}
    remote._trees = {"dir": "b" * 40}

    if remote.tree_identity("file.txt") != "a" * 40:
        base.fail("remote blob identity accessor self-test failed")
    if remote.tree_identity("dir") != "b" * 40:
        base.fail("remote subtree identity accessor self-test failed")
    if remote.tree_identity("missing") is not None:
        base.fail("remote absent-path identity accessor self-test failed")

    remote._blobs["bad.txt"] = ("not-a-sha", 1)
    base.expect_failure_matching(
        "malformed remote blob identity accessor",
        "candidate blob SHA is malformed",
        remote.tree_identity,
        "bad.txt",
    )


def selftest() -> None:
    v19.selftest()
    _install_v20_policy()
    _selftest_remote_blob_identity()

    marker_fixture = base.MemoryView(
        {
            v19.CORE_ADVERSARIAL_TEST_PATH: b"candidate core test\n",
            v19.DESKTOP_ADVERSARIAL_TEST_PATH: b"candidate desktop test\n",
            v19.CORE_CLIENT_PATH: b"candidate CoreClient extension\n",
        }
    )
    if not _is_s1_011_candidate(marker_fixture):
        base.fail("S1-011 trusted-base guard marker self-test failed")

    base.expect_failure_matching(
        "S1-011 candidate without trusted policy base",
        "S1-011 authorization requires trusted policy base",
        verify_view,
        marker_fixture,
    )

    print("wepld S1-011 trusted-base qualification policy self-tests: PASS")


def _verify_local(argv: list[str]) -> int:
    args = base.parse_args(argv)
    try:
        view = base.LocalRepositoryView(Path(args.root))
        token = os.environ.get(args.github_token_env) or None
        client = base.GitHubClient(token)

        if _is_s1_011_candidate(view):
            if not args.remote_baseline:
                base.fail(
                    "S1-011 local qualification requires --remote-baseline "
                    "and an exact trusted PR base"
                )
            comparison_sha = base.require_comparison_sha(args.pr_base_sha)
            repository = os.environ.get("GITHUB_REPOSITORY")
            if not repository or not base.REPOSITORY_SLUG_RE.fullmatch(repository):
                base.fail(
                    "S1-011 local qualification requires canonical "
                    "GITHUB_REPOSITORY identity"
                )
            policy_base = base.RemoteRepositoryView(repository, comparison_sha, client)
            stage = verify_view(view, policy_base=policy_base)
        else:
            stage = verify_view(view)

        if args.remote_baseline:
            shell.desktop_runner.verify_remote_baseline(client, args.pr_base_sha)
        shell.print_success(stage, "LOCAL_CHECKOUT")
        return 0

    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v20_policy()
    if argv and argv[0] == "verify-local":
        return _verify_local(argv)
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
