#!/usr/bin/env python3
"""Canonical S1-009 policy runner with fail-closed baseline ancestry proof.

The large S1-009 admission implementation is frozen as a sibling Git blob. This
runner binds that blob before import, extends the controlled-path set to cover
it, validates the immutable baseline artifact through the frozen foundation
policy, and proves PR-base ancestry through bounded identity-bound Git metadata.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import wepld_integrity as foundation

IMPL_SCRIPT = ".github/scripts/wepld_s1_desktop_integrity_impl.py"
EXPECTED_IMPL_GIT_BLOB_SHA1 = "ff2b21630c98ba9f001b45554e95116889e83141"
MAX_BASELINE_ANCESTRY_COMMITS = 512
MAX_BASELINE_PARENTS_PER_COMMIT = 16
MAX_GIT_OBJECT_READ_ATTEMPTS = 3
TRANSIENT_GITHUB_HTTP_ERRORS = (
    "HTTP Error 502:",
    "HTTP Error 503:",
    "HTTP Error 504:",
)


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

# Harden path-indirection detection for the S1-009 runner without mutating the
# frozen prior-stage policy bytes. This rejects both direct #[path = ...] and
# cfg_attr(..., path = ...) / cfg_attr(..., r#path = ...) forms.
DESKTOP_PATH_ATTRIBUTE = re.compile(
    r"#\s*\[\s*(?:(?:r#)?path\b|cfg_attr\s*\([^\]]*?\b(?:r#)?path\s*=)",
    re.DOTALL,
)


def _install_desktop_path_attribute() -> None:
    impl.prior.PATH_ATTRIBUTE = DESKTOP_PATH_ATTRIBUTE


def _commit_url(commit_sha: str) -> str:
    return (
        f"https://api.github.com/repos/{foundation.REPOSITORY}/git/commits/"
        f"{commit_sha.lower()}"
    )


def _commit_list_url(commit_sha: str) -> str:
    return (
        f"https://api.github.com/repos/{foundation.REPOSITORY}/commits"
        f"?sha={commit_sha.lower()}&per_page=1"
    )


def _baseline_contents_url() -> str:
    return (
        f"https://api.github.com/repos/{foundation.REPOSITORY}/contents/"
        f"{urllib.parse.quote(foundation.BASELINE_PATH, safe='/')}"
        f"?ref={foundation.BASELINE_COMMIT_SHA}"
    )


def _is_transient_api_failure(
    exc: foundation.PolicyError,
    url: str,
) -> bool:
    text = str(exc)
    prefix = f"GitHub API request failed for {url}:"
    return text.startswith(prefix) and any(
        marker in text for marker in TRANSIENT_GITHUB_HTTP_ERRORS
    )


def _is_transient_git_object_failure(
    exc: foundation.PolicyError,
    commit_sha: str,
) -> bool:
    return _is_transient_api_failure(exc, _commit_url(commit_sha))


def _json_list(
    client: foundation.GitHubClient,
    url: str,
) -> list[object]:
    """Read one GitHub JSON-list endpoint with the foundation client's trust envelope."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if client.token:
        headers["Authorization"] = f"Bearer {client.token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with client.opener.open(request, timeout=30) as response:
            if response.geturl() != url:
                foundation.fail(f"GitHub API target changed unexpectedly: {url}")
            data = json.load(response)
    except (OSError, json.JSONDecodeError) as exc:
        foundation.fail(f"GitHub API request failed for {url}: {exc}")
    if not isinstance(data, list):
        foundation.fail(f"GitHub API response is not a list: {url}")
    return data


def _read_object_with_bounded_retry(
    client: foundation.GitHubClient,
    url: str,
) -> object:
    last_error: foundation.PolicyError | None = None
    for _attempt in range(MAX_GIT_OBJECT_READ_ATTEMPTS):
        try:
            return client.json(url)
        except foundation.PolicyError as exc:
            if not _is_transient_api_failure(exc, url):
                raise
            last_error = exc
    if last_error is None:
        foundation.fail("bounded GitHub object retry exhausted without an error")
    raise last_error


def _read_list_with_bounded_retry(
    client: foundation.GitHubClient,
    url: str,
) -> list[object]:
    last_error: foundation.PolicyError | None = None
    for _attempt in range(MAX_GIT_OBJECT_READ_ATTEMPTS):
        try:
            return _json_list(client, url)
        except foundation.PolicyError as exc:
            if not _is_transient_api_failure(exc, url):
                raise
            last_error = exc
    if last_error is None:
        foundation.fail("bounded GitHub list retry exhausted without an error")
    raise last_error


def _read_commit_object_with_bounded_retry(
    client: foundation.GitHubClient,
    commit_sha: str,
) -> object:
    primary_url = _commit_url(commit_sha)
    try:
        return _read_object_with_bounded_retry(client, primary_url)
    except foundation.PolicyError as exc:
        if not _is_transient_api_failure(exc, primary_url):
            raise

    # Only after the exact Git-object route exhausts bounded 502/503/504 retries,
    # query the lighter commits-list route for exactly one item beginning at the
    # same immutable SHA. Identity and parent validation still occur below.
    secondary_url = _commit_list_url(commit_sha)
    payload = _read_list_with_bounded_retry(client, secondary_url)
    if len(payload) != 1:
        foundation.fail("secondary baseline commit metadata payload must contain exactly one item")
    commit = payload[0]
    if not isinstance(commit, dict):
        foundation.fail("secondary baseline commit metadata item is malformed")
    return commit


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

        commit = _read_commit_object_with_bounded_retry(client, current)
        if not isinstance(commit, dict):
            foundation.fail("baseline ancestry commit payload is malformed")
        foundation.require_object_identity(
            "baseline ancestry commit", current, commit.get("sha")
        )
        parents = commit.get("parents")
        if not isinstance(parents, list):
            foundation.fail("baseline ancestry commit parents payload is malformed")
        if len(parents) > MAX_BASELINE_PARENTS_PER_COMMIT:
            foundation.fail("baseline ancestry commit exceeds bounded parent fanout")

        # GitHub orders merge parents with the prior base first. Push in reverse
        # so the LIFO stack follows canonical first-parent history before side
        # branches while retaining complete backtracking over every parent.
        for parent in reversed(parents):
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
    """Validate baseline artifact, then prove ancestry without interpreting Compare errors."""
    comparison = foundation.require_comparison_sha(comparison_sha).lower()

    # Reuse the frozen foundation verifier for the immutable baseline artifact,
    # but pass the immutable base itself so its optional Compare branch is never
    # entered. Authorization/client errors from Compare therefore cannot be
    # converted into success by this runner because this runner never requests
    # the Compare endpoint.
    foundation.verify_remote_baseline(client, foundation.BASELINE_BASE_MAIN_SHA)

    if comparison != foundation.BASELINE_BASE_MAIN_SHA.lower():
        _verify_baseline_ancestry_by_parent_walk(client, comparison)


def selftest_runner() -> None:
    target = foundation.BASELINE_BASE_MAIN_SHA.lower()
    descendant = "a" * 40
    root = "b" * 40

    direct = foundation.StubGitHubClient(
        {
            _commit_url(descendant): {
                "sha": descendant,
                "parents": [{"sha": target}],
            }
        }
    )
    _verify_baseline_ancestry_by_parent_walk(direct, descendant)

    missing = foundation.StubGitHubClient(
        {
            _commit_url(root): {
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
            _commit_url(descendant): {
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
            _commit_url(descendant): {
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

    transient = foundation.PolicyError(
        f"GitHub API request failed for {_commit_url(descendant)}: "
        "HTTP Error 504: Gateway Timeout"
    )
    if not _is_transient_git_object_failure(transient, descendant):
        foundation.fail("runner self-test: transient Git object failure was not recognized")
    for status, reason in (
        (401, "Unauthorized"),
        (403, "Forbidden"),
        (404, "Not Found"),
        (429, "Too Many Requests"),
    ):
        permanent = foundation.PolicyError(
            f"GitHub API request failed for {_commit_url(descendant)}: "
            f"HTTP Error {status}: {reason}"
        )
        if _is_transient_git_object_failure(permanent, descendant):
            foundation.fail(
                f"runner self-test: permanent Git object HTTP {status} triggered retry"
            )

    class FlakyGitHubClient:
        def __init__(self) -> None:
            self.calls = 0

        def json(self, url: str) -> object:
            self.calls += 1
            if self.calls < 2:
                raise foundation.PolicyError(
                    f"GitHub API request failed for {url}: HTTP Error 504: Gateway Timeout"
                )
            return {"sha": descendant, "parents": [{"sha": target}]}

    flaky = FlakyGitHubClient()
    _verify_baseline_ancestry_by_parent_walk(flaky, descendant)  # type: ignore[arg-type]
    if flaky.calls != 2:
        foundation.fail("runner self-test: transient Git object read was not retried exactly once")

    class FakeListResponse:
        def __init__(self, url: str, payload: object) -> None:
            self.url = url
            self.payload = payload

        def __enter__(self) -> "FakeListResponse":
            return self

        def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
            return False

        def geturl(self) -> str:
            return self.url

        def read(self, _size: int = -1) -> bytes:
            return json.dumps(self.payload).encode("utf-8")

    class SecondaryRouteGitHubClient:
        token = None

        def __init__(self, secondary_payload: object) -> None:
            self.primary_calls = 0
            self.secondary_calls = 0
            self.secondary_payload = secondary_payload
            self.opener = self

        def json(self, url: str) -> object:
            if url == _commit_url(descendant):
                self.primary_calls += 1
                raise foundation.PolicyError(
                    f"GitHub API request failed for {url}: HTTP Error 504: Gateway Timeout"
                )
            raise foundation.PolicyError(f"unexpected self-test object URL: {url}")

        def open(self, request: urllib.request.Request, timeout: int) -> FakeListResponse:
            if timeout != 30:
                foundation.fail("runner self-test: secondary timeout drifted")
            url = request.full_url
            if url != _commit_list_url(descendant):
                raise OSError(f"unexpected self-test list URL: {url}")
            self.secondary_calls += 1
            return FakeListResponse(url, self.secondary_payload)

    secondary = SecondaryRouteGitHubClient(
        [{"sha": descendant, "parents": [{"sha": target}]}]
    )
    _verify_baseline_ancestry_by_parent_walk(secondary, descendant)  # type: ignore[arg-type]
    if secondary.primary_calls != MAX_GIT_OBJECT_READ_ATTEMPTS:
        foundation.fail("runner self-test: primary Git object route did not exhaust bounded retries")
    if secondary.secondary_calls != 1:
        foundation.fail("runner self-test: secondary commit metadata route was not used exactly once")

    foundation.expect_failure_matching(
        "malformed secondary baseline payload",
        "secondary baseline commit metadata payload must contain exactly one item",
        _verify_baseline_ancestry_by_parent_walk,
        SecondaryRouteGitHubClient([]),  # type: ignore[arg-type]
        descendant,
    )
    foundation.expect_failure_matching(
        "wrong-type secondary baseline payload",
        "GitHub API response is not a list",
        _verify_baseline_ancestry_by_parent_walk,
        SecondaryRouteGitHubClient({"sha": descendant}),  # type: ignore[arg-type]
        descendant,
    )

    baseline_content = base64.b64encode(
        json.dumps(foundation.EXPECTED_BASELINE).encode("utf-8")
    ).decode("ascii")
    no_compare = foundation.StubGitHubClient(
        {
            _baseline_contents_url(): {
                "sha": foundation.BASELINE_BLOB_SHA,
                "encoding": "base64",
                "content": baseline_content,
            },
            _commit_url(descendant): {
                "sha": descendant,
                "parents": [{"sha": target}],
            },
        }
    )
    # StubGitHubClient fails on any unmapped URL. Passing here proves the runner
    # validates the baseline artifact and ancestry without issuing Compare.
    verify_remote_baseline(no_compare, descendant)  # type: ignore[arg-type]

    _install_desktop_path_attribute()
    path_cases = (
        '#[path = "escape.rs"]',
        '#[r#path = "escape.rs"]',
        '#[cfg_attr(target_os = "windows", path = "escape.rs")]',
        '#[cfg_attr(any(), r#path = "escape.rs")]',
        '#[cfg_attr(\n    target_os = "windows",\n    path = "escape.rs",\n)]',
    )
    for case in path_cases:
        if DESKTOP_PATH_ATTRIBUTE.search(case) is None:
            foundation.fail(
                "runner self-test: Desktop path-indirection detector missed prohibited attribute"
            )
    if DESKTOP_PATH_ATTRIBUTE.search('#[cfg_attr(test, allow(dead_code))]') is not None:
        foundation.fail(
            "runner self-test: Desktop path-indirection detector rejected benign cfg_attr"
        )


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
        _install_desktop_path_attribute()

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
