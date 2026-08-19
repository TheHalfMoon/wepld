#!/usr/bin/env python3
"""Authorize only the frozen S1-011 adversarial test candidate.

This wrapper binds canonical v18 before import. It does not authorize arbitrary
Rust test code. The future S1-011 candidate must use two byte-exact Rust test
templates reviewed with this policy plus one exact test-only module declaration
appended to the frozen S1-010 CoreClient source.

Production/runtime/dependency/UI bytes remain inherited from canonical S1-010.
No S1-012+ scope is authorized.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v19.py"
PRIOR_V18_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v18.py"
EXPECTED_PRIOR_V18_RUNNER_GIT_BLOB_SHA1 = "99d11b409bd96a383c978d0e03454347da95ebe6"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "1c8457d67f10d401674c99e4bf3e43a170f7d9477150d2c65fccbf265bda8dad",
    ".github/workflows/s1-admission-integrity.yml": "534cc7dd2c0d3712ea4cab5e733135180c87df1945acd962abee8f49a1f466d5",
    ".github/workflows/s1-contracts.yml": "2ab777e867c60ef545e1b96dd4ff01546ca268eb794ce5bc620c98e9af0fbc27",
}

S1_011_STAGE = "S1_CROSS_PROCESS_ADVERSARIAL_CANDIDATE"

CORE_TEST_TEMPLATE_PATH = ".github/policy/s1_011_core_adversarial_v1.rs"
DESKTOP_TEST_TEMPLATE_PATH = ".github/policy/s1_011_desktop_adversarial_v1.rs"
POLICY_TEMPLATE_PATHS = frozenset(
    {
        CORE_TEST_TEMPLATE_PATH,
        DESKTOP_TEST_TEMPLATE_PATH,
    }
)

CORE_ADVERSARIAL_TEST_PATH = "crates/core/tests/s1_011_adversarial_v1.rs"
DESKTOP_ADVERSARIAL_TEST_PATH = "apps/desktop/src-tauri/src/s1_011_tests.rs"
CORE_CLIENT_PATH = "apps/desktop/src-tauri/src/core_client.rs"

S1_011_NEW_TEST_PATHS = frozenset(
    {
        CORE_ADVERSARIAL_TEST_PATH,
        DESKTOP_ADVERSARIAL_TEST_PATH,
    }
)
S1_011_DELTA_PATHS = frozenset(set(S1_011_NEW_TEST_PATHS) | {CORE_CLIENT_PATH})

EXPECTED_CORE_TEST_TEMPLATE_SHA256 = "25d25fe42c0ce7be2d22fa8d61d93e6de550de306c1121cb777a27584c065067"
EXPECTED_DESKTOP_TEST_TEMPLATE_SHA256 = "49f7fbdf7e1193b1cc3c5f1a3f71cbb83aae3e3d4096abc226088aa8d794b550"
EXPECTED_CANONICAL_CORE_CLIENT_GIT_BLOB_SHA1 = "5c5822ee60865caae5f86444cc037f9079d892a0"

CORE_CLIENT_TEST_SUFFIX = (
    b'\n#[cfg(test)]\n'
    b'#[path = "s1_011_tests.rs"]\n'
    b'mod s1_011_tests;\n'
)

MAX_S1_011_SOURCE_BYTES = 256_000
MAX_CORE_CLIENT_BYTES = 384_000

_INSTALLED = False
_PRIOR_VERIFY_VIEW = None
_PRIOR_PRINT_SUCCESS = None


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _bind_prior_v18_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v18.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v18 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V18_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v18 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V18_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v18_runner_before_import()
import wepld_s1_shell_integrity_v18 as v18  # noqa: E402

shell = v18.shell


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V18_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V18_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v18 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V18_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v18._verify_policy_files(view)


def _verify_policy_templates(view: base.RepositoryView) -> None:
    expected = {
        CORE_TEST_TEMPLATE_PATH: EXPECTED_CORE_TEST_TEMPLATE_SHA256,
        DESKTOP_TEST_TEMPLATE_PATH: EXPECTED_DESKTOP_TEST_TEMPLATE_SHA256,
    }
    for relative, digest in expected.items():
        data = view.read_bytes(relative, MAX_S1_011_SOURCE_BYTES)
        actual = _sha256(data)
        if actual != digest:
            base.fail(
                f"S1-011 frozen policy template drifted: {relative}: "
                f"expected_sha256={digest} actual_sha256={actual}"
            )


def _canonical_core_client_bytes(data: bytes, expected_base_sha1: str) -> bytes:
    actual = _git_blob_sha1(data)
    if actual == expected_base_sha1:
        return data
    if not data.endswith(CORE_CLIENT_TEST_SUFFIX):
        base.fail(
            "S1-011 CoreClient may change only by the frozen test-module suffix"
        )
    canonical = data[: -len(CORE_CLIENT_TEST_SUFFIX)]
    actual_base = _git_blob_sha1(canonical)
    if actual_base != expected_base_sha1:
        base.fail(
            "S1-011 CoreClient prefix drifted from canonical S1-010 bytes: "
            f"expected={expected_base_sha1} actual={actual_base}"
        )
    return canonical


def _verify_core_client_extension(view: base.RepositoryView) -> None:
    data = view.read_bytes(CORE_CLIENT_PATH, MAX_CORE_CLIENT_BYTES)
    if _git_blob_sha1(data) == EXPECTED_CANONICAL_CORE_CLIENT_GIT_BLOB_SHA1:
        base.fail("S1-011 candidate is missing the frozen CoreClient test-module suffix")
    canonical = _canonical_core_client_bytes(
        data, EXPECTED_CANONICAL_CORE_CLIENT_GIT_BLOB_SHA1
    )
    if len(data) != len(canonical) + len(CORE_CLIENT_TEST_SUFFIX):
        base.fail("S1-011 CoreClient contains material beyond the frozen test-only suffix")


def _verify_exact_test_source(
    candidate: base.RepositoryView,
    candidate_path: str,
    trusted_templates: base.RepositoryView,
    template_path: str,
) -> None:
    expected = trusted_templates.read_bytes(template_path, MAX_S1_011_SOURCE_BYTES)
    actual = candidate.read_bytes(candidate_path, MAX_S1_011_SOURCE_BYTES)
    if actual != expected:
        base.fail(
            f"S1-011 test source must match frozen reviewed template byte-for-byte: "
            f"{candidate_path}"
        )


class _PriorV18View(base.RepositoryView):
    """Hide v19-only policy/test files and project CoreClient back to v18."""

    def __init__(self, inner: base.RepositoryView):
        self._inner = inner

    def entries(self) -> list[base.TrackedEntry]:
        hidden = POLICY_TEMPLATE_PATHS | S1_011_NEW_TEST_PATHS
        return [entry for entry in self._inner.entries() if entry.path not in hidden]

    def read_bytes(self, relative: str, limit: int) -> bytes:
        if relative in POLICY_TEMPLATE_PATHS or relative in S1_011_NEW_TEST_PATHS:
            base.fail(f"v19-only path leaked into prior-stage read: {relative}")
        data = self._inner.read_bytes(relative, limit)
        if relative == CORE_CLIENT_PATH:
            return _canonical_core_client_bytes(
                data, EXPECTED_CANONICAL_CORE_CLIENT_GIT_BLOB_SHA1
            )
        return data

    def tree_identity(self, relative: str) -> str | None:
        if relative in POLICY_TEMPLATE_PATHS or relative in S1_011_NEW_TEST_PATHS:
            return None
        if relative == CORE_CLIENT_PATH:
            data = self._inner.read_bytes(relative, MAX_CORE_CLIENT_BYTES)
            _canonical_core_client_bytes(
                data, EXPECTED_CANONICAL_CORE_CLIENT_GIT_BLOB_SHA1
            )
            return EXPECTED_CANONICAL_CORE_CLIENT_GIT_BLOB_SHA1
        return self._inner.tree_identity(relative)


def _has_s1_011_markers(view: base.RepositoryView, paths: set[str]) -> bool:
    present_tests = paths & S1_011_NEW_TEST_PATHS
    core_identity = view.tree_identity(CORE_CLIENT_PATH)
    core_changed = core_identity != EXPECTED_CANONICAL_CORE_CLIENT_GIT_BLOB_SHA1

    if not present_tests and not core_changed:
        return False

    missing_tests = S1_011_NEW_TEST_PATHS - paths
    if missing_tests:
        base.fail(
            "partial S1-011 adversarial candidate is prohibited; missing test path(s): "
            + ", ".join(sorted(missing_tests))
        )
    if not core_changed:
        base.fail(
            "partial S1-011 adversarial candidate is prohibited; "
            "CoreClient test-module suffix is missing"
        )
    return True


def _require_exact_delta(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    candidate_entries = {entry.path: entry.mode for entry in candidate.entries()}
    base_entries = {entry.path: entry.mode for entry in policy_base.entries()}

    changed: set[str] = set(candidate_entries) ^ set(base_entries)
    for relative in set(candidate_entries) & set(base_entries):
        if candidate_entries[relative] != base_entries[relative]:
            changed.add(relative)
            continue
        if candidate.tree_identity(relative) != policy_base.tree_identity(relative):
            changed.add(relative)

    if changed != set(S1_011_DELTA_PATHS):
        missing = sorted(set(S1_011_DELTA_PATHS) - changed)
        unexpected = sorted(changed - set(S1_011_DELTA_PATHS))
        details: list[str] = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if unexpected:
            details.append("unexpected=" + ",".join(unexpected))
        base.fail(
            "S1-011 trusted-base delta must be exactly the frozen three-path "
            "test-only surface"
            + (": " + " ".join(details) if details else "")
        )


def verify_view(
    view: base.RepositoryView,
    *,
    policy_base: base.RepositoryView | None = None,
) -> str:
    paths = base.validate_entries(view.entries())
    _verify_policy_templates(view)
    if policy_base is not None:
        _verify_policy_templates(policy_base)

    is_s1_011 = _has_s1_011_markers(view, paths)

    prior_view = _PriorV18View(view)
    prior_policy_base = _PriorV18View(policy_base) if policy_base is not None else None

    if _PRIOR_VERIFY_VIEW is None:
        base.fail("S1-011 prior verifier is not installed")

    prior_stage = _PRIOR_VERIFY_VIEW(
        prior_view,
        policy_base=prior_policy_base,
    )

    if not is_s1_011:
        return prior_stage

    if prior_stage != shell.SHELL_STAGE:
        base.fail(
            "S1-011 candidate must extend canonical S1-010 shell state; "
            f"observed prior stage={prior_stage}"
        )

    trusted_templates = policy_base if policy_base is not None else view
    _verify_exact_test_source(
        view,
        CORE_ADVERSARIAL_TEST_PATH,
        trusted_templates,
        CORE_TEST_TEMPLATE_PATH,
    )
    _verify_exact_test_source(
        view,
        DESKTOP_ADVERSARIAL_TEST_PATH,
        trusted_templates,
        DESKTOP_TEST_TEMPLATE_PATH,
    )
    _verify_core_client_extension(view)

    if policy_base is not None:
        _require_exact_delta(view, policy_base)

    return S1_011_STAGE


def print_success(stage: str, mode: str) -> None:
    if stage != S1_011_STAGE:
        if _PRIOR_PRINT_SUCCESS is None:
            base.fail("S1-011 prior success printer is not installed")
        _PRIOR_PRINT_SUCCESS(stage, mode)
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
    print("product_implementation_authorized=S1_011_TEST_ONLY")
    print("production_runtime_authority_expansion=NONE")
    print("s1_012_plus=NOT_STARTED")


def _install_v19_policy() -> None:
    global _INSTALLED, _PRIOR_VERIFY_VIEW, _PRIOR_PRINT_SUCCESS
    if _INSTALLED:
        return

    v18._install_v18_policy()
    _PRIOR_VERIFY_VIEW = shell.verify_view
    _PRIOR_PRINT_SUCCESS = shell.print_success

    for module in (
        v18,
        v18.v17,
        v18.v16,
        v18.v15,
        v18.v14,
        v18.v13,
        v18.v12,
        v18.v11,
        v18.v10,
        v18.v9,
        v18.v8,
        v18.v7,
        v18.v6,
        v18.v5,
        v18.v4,
        v18.v3,
        v18.v2,
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
    shell.print_success = print_success
    _INSTALLED = True


def selftest() -> None:
    v18.selftest()
    _install_v19_policy()

    core_template = b"canonical core adversarial test\n"
    desktop_template = b"canonical desktop adversarial test\n"
    fixture = base.MemoryView(
        {
            CORE_TEST_TEMPLATE_PATH: core_template,
            DESKTOP_TEST_TEMPLATE_PATH: desktop_template,
            CORE_ADVERSARIAL_TEST_PATH: core_template,
            DESKTOP_ADVERSARIAL_TEST_PATH: desktop_template,
        }
    )
    _verify_exact_test_source(
        fixture,
        CORE_ADVERSARIAL_TEST_PATH,
        fixture,
        CORE_TEST_TEMPLATE_PATH,
    )
    _verify_exact_test_source(
        fixture,
        DESKTOP_ADVERSARIAL_TEST_PATH,
        fixture,
        DESKTOP_TEST_TEMPLATE_PATH,
    )

    for name, mutation in (
        ("comment decoy", b"\n// #[test] CoreClient Command::new(\"sh\")\n"),
        ("ignored-test decoy", b"\n#[ignore = \"skip\"]\n"),
        ("cfg-attribute decoy", b"\n#[cfg_attr(all(), ignore)]\n"),
        ("panic-only decoy", b"\n#[ should_panic ]\n"),
        ("socket escape decoy", b"\n// UnixListener\n"),
    ):
        bad = base.MemoryView(
            {
                CORE_TEST_TEMPLATE_PATH: core_template,
                CORE_ADVERSARIAL_TEST_PATH: core_template + mutation,
            }
        )
        base.expect_failure_matching(
            f"S1-011 frozen-template rejection: {name}",
            "must match frozen reviewed template byte-for-byte",
            _verify_exact_test_source,
            bad,
            CORE_ADVERSARIAL_TEST_PATH,
            bad,
            CORE_TEST_TEMPLATE_PATH,
        )

    fake_canonical = b"canonical core client\n"
    fake_sha = _git_blob_sha1(fake_canonical)
    projected = _canonical_core_client_bytes(fake_canonical, fake_sha)
    if projected != fake_canonical:
        base.fail("S1-011 CoreClient canonical projection self-test failed")

    extended = fake_canonical + CORE_CLIENT_TEST_SUFFIX
    projected = _canonical_core_client_bytes(extended, fake_sha)
    if projected != fake_canonical:
        base.fail("S1-011 CoreClient test-only projection self-test failed")

    base.expect_failure_matching(
        "S1-011 CoreClient arbitrary code after canonical prefix",
        "may change only by the frozen test-module suffix",
        _canonical_core_client_bytes,
        fake_canonical + b"\nfn escape() {}\n",
        fake_sha,
    )

    print("wepld S1-011 frozen adversarial-stage policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v19_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
