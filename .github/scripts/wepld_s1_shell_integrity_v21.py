#!/usr/bin/env python3
"""Make S1-011 qualification deterministic and rustfmt-compatible.

Canonical v20 repaired trusted-base selection and remote Git-object identity.
Two independently observed blockers remain before the frozen S1-011 candidate
can be qualified:

1. foundation-integrity local qualification reads the trusted base through
   unauthenticated GitHub REST calls and can fail on API rate limits; and
2. the byte-exact v19 Rust templates predate the pinned rustfmt result, so the
   otherwise-authorized candidate cannot pass the repository format gates.

v21 keeps privileged pull_request_target admission remote/data-only, keeps the
reviewed v19 templates immutable, derives one exact rustfmt projection from
those templates, and uses the locally fetched canonical Git history for the
unprivileged foundation self-check. No product/runtime/dependency/UI bytes or
S1-012+ authority are added.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v21.py"
PRIOR_V20_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v20.py"
EXPECTED_PRIOR_V20_RUNNER_GIT_BLOB_SHA1 = "6ecb667a00771b813ffe046c48396ca9ffd6deac"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "01a0c843fb738baf9553af7fe0ff9f8abba42eb4ea22ff71754cebbd61b64005",
    ".github/workflows/s1-admission-integrity.yml": "0a6e2164e8bbe08495eefdce6f420ac61e37104c01c37f02812fce8b089a46bc",
    ".github/workflows/s1-contracts.yml": "2ab777e867c60ef545e1b96dd4ff01546ca268eb794ce5bc620c98e9af0fbc27",
}

CORE_RUSTFMT_REPLACEMENTS = (
    (
        b"""        send_wire(
            &mut child,
            &((MAX_PAYLOAD_BYTES as u32) + 1).to_be_bytes(),
        );
""",
        b"""        send_wire(&mut child, &((MAX_PAYLOAD_BYTES as u32) + 1).to_be_bytes());
""",
    ),
    (
        b"""    send(
        &mut child,
        &observe_request(MAX_HEALTH_WATCHES as u64 + 1),
    );
""",
        b"""    send(&mut child, &observe_request(MAX_HEALTH_WATCHES as u64 + 1));
""",
    ),
)

DESKTOP_RUSTFMT_REPLACEMENTS = (
    (
        b"""const FAKE_CORE_HELPER_TEST: &str =
    "core_client::s1_011_tests::fake_core_stderr_flood_helper";
""",
        b"""const FAKE_CORE_HELPER_TEST: &str = "core_client::s1_011_tests::fake_core_stderr_flood_helper";
""",
    ),
    (
        b"""    stdout.flush().expect("fake Core health response must flush");
""",
        b"""    stdout
        .flush()
        .expect("fake Core health response must flush");
""",
    ),
    (
        b"""    client.child.kill().expect("owned Core must accept termination");
""",
        b"""    client
        .child
        .kill()
        .expect("owned Core must accept termination");
""",
    ),
    (
        b"""    client.stop_child().expect("owned child cleanup must succeed");
""",
        b"""    client
        .stop_child()
        .expect("owned child cleanup must succeed");
""",
    ),
    (
        b"""    let mut client =
        spawn_stderr_flood_client().expect("frozen stderr-flood helper must start");
""",
        b"""    let mut client = spawn_stderr_flood_client().expect("frozen stderr-flood helper must start");
""",
    ),
)

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v20_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v20.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-011 v20 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V20_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v20 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V20_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v20_runner_before_import()
import wepld_s1_shell_integrity_v20 as v20  # noqa: E402

v19 = v20.v19
v18 = v20.v18
v17 = v20.v17
v16 = v20.v16
v15 = v20.v15
v14 = v20.v14
v13 = v20.v13
v12 = v20.v12
v11 = v20.v11
v10 = v20.v10
v9 = v20.v9
v8 = v20.v8
v7 = v20.v7
v6 = v20.v6
v5 = v20.v5
v4 = v20.v4
v3 = v20.v3
v2 = v20.v2
shell = v20.shell


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V20_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V20_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v20 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V20_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v20._verify_policy_files(view)


def _replace_exactly_once(data: bytes, before: bytes, after: bytes, label: str) -> bytes:
    count = data.count(before)
    if count != 1:
        base.fail(
            f"S1-011 rustfmt projection source drifted for {label}: "
            f"expected_occurrences=1 actual={count}"
        )
    return data.replace(before, after, 1)


def _rustfmt_projection(template_path: str, data: bytes) -> bytes:
    if template_path == v19.CORE_TEST_TEMPLATE_PATH:
        replacements = CORE_RUSTFMT_REPLACEMENTS
        label = "core"
    elif template_path == v19.DESKTOP_TEST_TEMPLATE_PATH:
        replacements = DESKTOP_RUSTFMT_REPLACEMENTS
        label = "desktop"
    else:
        base.fail(f"unexpected S1-011 rustfmt projection template: {template_path}")

    projected = data
    for index, (before, after) in enumerate(replacements, start=1):
        projected = _replace_exactly_once(
            projected,
            before,
            after,
            f"{label}:{index}",
        )
    if projected == data:
        base.fail(f"S1-011 rustfmt projection made no change: {template_path}")
    return projected


def _verify_rustfmt_projected_test_source(
    candidate: base.RepositoryView,
    candidate_path: str,
    trusted_templates: base.RepositoryView,
    template_path: str,
) -> None:
    template = trusted_templates.read_bytes(
        template_path,
        v19.MAX_S1_011_SOURCE_BYTES,
    )
    expected = _rustfmt_projection(template_path, template)
    actual = candidate.read_bytes(candidate_path, v19.MAX_S1_011_SOURCE_BYTES)
    if actual != expected:
        base.fail(
            "S1-011 test source must match the exact rustfmt projection of the "
            f"frozen reviewed template byte-for-byte: {candidate_path}"
        )


class GitCommitRepositoryView(base.RepositoryView):
    """Read one exact commit from the already-fetched local Git object store."""

    def __init__(self, root: Path, commit_sha: str):
        self.root = root.resolve()
        if not (self.root / ".git").exists():
            base.fail(f"root is not a Git checkout: {self.root}")
        if not base.OBJECT_SHA_RE.fullmatch(commit_sha):
            base.fail(f"local trusted commit SHA is malformed: {commit_sha!r}")
        self.commit_sha = commit_sha.lower()
        resolved = self._git_text("rev-parse", "--verify", f"{self.commit_sha}^{{commit}}")
        if resolved.lower() != self.commit_sha:
            base.fail(
                "local trusted commit identity mismatch: "
                f"expected={self.commit_sha} actual={resolved.lower()}"
            )

    def _git_bytes(self, *args: str) -> bytes:
        try:
            return subprocess.check_output(
                ["git", "-C", str(self.root), *args],
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode("utf-8", errors="replace").strip()
            base.fail(f"local Git object query failed: {' '.join(args)}: {output}")

    def _git_text(self, *args: str) -> str:
        try:
            return subprocess.check_output(
                ["git", "-C", str(self.root), *args],
                stderr=subprocess.STDOUT,
                text=True,
            ).strip()
        except subprocess.CalledProcessError as exc:
            output = exc.output
            if not isinstance(output, str):
                output = output.decode("utf-8", errors="replace")
            base.fail(f"local Git object query failed: {' '.join(args)}: {output.strip()}")

    def entries(self) -> list[base.TrackedEntry]:
        raw = self._git_bytes(
            "ls-tree",
            "-r",
            "-z",
            "--full-tree",
            self.commit_sha,
        )
        result: list[base.TrackedEntry] = []
        for record in raw.split(b"\0"):
            if not record:
                continue
            try:
                metadata, raw_path = record.split(b"\t", 1)
                mode_b, object_type_b, object_sha_b = metadata.split(b" ", 2)
                object_type = object_type_b.decode("ascii", errors="strict")
                object_sha = object_sha_b.decode("ascii", errors="strict")
                if object_type not in {"blob", "commit"}:
                    base.fail(
                        "unexpected local trusted Git object type "
                        f"{object_type!r}: {raw_path!r}"
                    )
                if not base.OBJECT_SHA_RE.fullmatch(object_sha):
                    base.fail(f"local trusted object SHA is malformed: {raw_path!r}")
                result.append(
                    base.TrackedEntry(
                        mode=mode_b.decode("ascii", errors="strict"),
                        path=raw_path.decode("utf-8", errors="strict"),
                    )
                )
            except (ValueError, UnicodeError) as exc:
                base.fail(f"malformed local trusted tree record: {record!r}: {exc}")
        return result

    def tree_identity(self, relative: str) -> str | None:
        try:
            raw = subprocess.check_output(
                [
                    "git",
                    "-C",
                    str(self.root),
                    "rev-parse",
                    "--verify",
                    f"{self.commit_sha}:{relative}",
                ],
                stderr=subprocess.STDOUT,
                text=True,
            ).strip()
        except subprocess.CalledProcessError:
            return None
        if not base.OBJECT_SHA_RE.fullmatch(raw):
            base.fail(
                f"local trusted object identity is malformed: {relative}: {raw!r}"
            )
        return raw.lower()

    def read_bytes(self, relative: str, limit: int) -> bytes:
        object_spec = f"{self.commit_sha}:{relative}"
        raw_size = self._git_text("cat-file", "-s", object_spec)
        try:
            size = int(raw_size)
        except ValueError:
            base.fail(f"local trusted blob size is malformed: {relative}: {raw_size!r}")
        if size < 0 or size > limit:
            base.fail(f"local trusted blob exceeds bounded size {limit}: {relative}")
        data = self._git_bytes("cat-file", "blob", object_spec)
        if len(data) != size:
            base.fail(f"local trusted blob size disagrees with Git metadata: {relative}")
        return data


def _verify_local_immutable_baseline(root: Path, comparison_sha: str) -> None:
    comparison = base.require_comparison_sha(comparison_sha)
    GitCommitRepositoryView(root, comparison)

    baseline_view = GitCommitRepositoryView(root, base.BASELINE_COMMIT_SHA)
    baseline_identity = baseline_view.tree_identity(base.BASELINE_PATH)
    if baseline_identity != base.BASELINE_BLOB_SHA:
        base.fail(
            "immutable baseline blob identity mismatch: "
            f"expected={base.BASELINE_BLOB_SHA} actual={baseline_identity}"
        )
    try:
        baseline = json.loads(
            baseline_view.read_text(base.BASELINE_PATH, base.MAX_POLICY_FILE_BYTES)
        )
    except json.JSONDecodeError as exc:
        base.fail(f"immutable baseline payload is invalid: {exc}")
    for key, expected in base.EXPECTED_BASELINE.items():
        if baseline.get(key) != expected:
            base.fail(f"immutable baseline mismatch for {key}")

    GitCommitRepositoryView(root, base.BASELINE_BASE_MAIN_SHA)
    if comparison != base.BASELINE_BASE_MAIN_SHA:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root.resolve()),
                "merge-base",
                "--is-ancestor",
                base.BASELINE_BASE_MAIN_SHA,
                comparison,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode == 1:
            base.fail("PR base is not the immutable foundation base or a descendant")
        if result.returncode != 0:
            base.fail(
                "local immutable-baseline ancestry query failed: "
                f"{result.stderr.strip()}"
            )


def _install_v21_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v20._install_v20_policy()

    # Keep the reviewed v19 templates immutable. Only their deterministic
    # rustfmt projection is authorized as executable S1-011 candidate source.
    v19._verify_exact_test_source = _verify_rustfmt_projected_test_source

    for module in (
        v20,
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
    _INSTALLED = True


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _selftest_rustfmt_projection() -> None:
    view = base.LocalRepositoryView(_repository_root())
    for path in (
        v19.CORE_TEST_TEMPLATE_PATH,
        v19.DESKTOP_TEST_TEMPLATE_PATH,
    ):
        template = view.read_bytes(path, v19.MAX_S1_011_SOURCE_BYTES)
        projected = _rustfmt_projection(path, template)
        if projected == template:
            base.fail(f"rustfmt projection self-test made no change: {path}")


def _selftest_local_commit_view() -> None:
    root = _repository_root()
    head = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    candidate = base.LocalRepositoryView(root)
    committed = GitCommitRepositoryView(root, head)
    candidate_entries = {entry.path: entry.mode for entry in candidate.entries()}
    committed_entries = {entry.path: entry.mode for entry in committed.entries()}
    if candidate_entries != committed_entries:
        base.fail("local commit view entry inventory differs from exact HEAD")
    for path in (
        PRIOR_V20_RUNNER_PATH,
        v19.CORE_TEST_TEMPLATE_PATH,
        v19.DESKTOP_TEST_TEMPLATE_PATH,
    ):
        if candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != committed.read_bytes(
            path,
            base.MAX_POLICY_FILE_BYTES,
        ):
            base.fail(f"local commit view byte identity self-test failed: {path}")
        if candidate.tree_identity(path) != committed.tree_identity(path):
            base.fail(f"local commit view object identity self-test failed: {path}")


def selftest() -> None:
    v20.selftest()
    _install_v21_policy()
    _selftest_rustfmt_projection()
    _selftest_local_commit_view()

    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )

    print("wepld S1-011 deterministic/rustfmt qualification policy self-tests: PASS")


def _verify_local(argv: list[str]) -> int:
    args = base.parse_args(argv)
    try:
        root = Path(args.root)
        view = base.LocalRepositoryView(root)

        if v20._is_s1_011_candidate(view):
            if not args.remote_baseline:
                base.fail(
                    "S1-011 local qualification requires immutable-baseline "
                    "verification and an exact trusted PR base"
                )
            comparison_sha = base.require_comparison_sha(args.pr_base_sha)
            if base.REPOSITORY != CANONICAL_REPOSITORY:
                base.fail(
                    "canonical repository identity drifted: "
                    f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
                )
            policy_base = GitCommitRepositoryView(root, comparison_sha)
            stage = v20.verify_view(view, policy_base=policy_base)
        else:
            stage = v20.verify_view(view)

        if args.remote_baseline:
            _verify_local_immutable_baseline(root, args.pr_base_sha)

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

    _install_v21_policy()
    if argv and argv[0] == "verify-local":
        return _verify_local(argv)
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
