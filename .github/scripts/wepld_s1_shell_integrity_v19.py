#!/usr/bin/env python3
"""Authorize the bounded S1-011 cross-process adversarial test stage.

This wrapper binds canonical v18 before import. It opens exactly two new
test-only paths for the future S1-011 candidate and preserves every canonical
S1-010 production/runtime/dependency/UI byte through inherited verification.

No product behavior, dependency, plugin, workflow execution authority, shell,
filesystem/network authority, branding work, or S1-012+ scope is authorized.
"""

from __future__ import annotations

import hashlib
import re
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
CORE_ADVERSARIAL_TEST_PATH = "crates/core/tests/s1_011_adversarial_v1.rs"
DESKTOP_ADVERSARIAL_TEST_PATH = "apps/desktop/src-tauri/tests/s1_011_cross_process_v1.rs"
S1_011_TEST_PATHS = frozenset(
    {
        CORE_ADVERSARIAL_TEST_PATH,
        DESKTOP_ADVERSARIAL_TEST_PATH,
    }
)
MAX_S1_011_TEST_BYTES = 192_000

PROHIBITED_TEST_TEXT = re.compile(
    r"(?i)(?:https?://|wss?://|TcpStream|TcpListener|UdpSocket|"
    r"reqwest|ureq|hyper|tokio|async[_-]std|"
    r"cmd\.exe|powershell(?:\.exe)?|/bin/(?:sh|bash|zsh)|"
    r"tauri[_-]plugin[_-](?:shell|fs|http))"
)

CORE_REQUIRED_TOKENS = (
    '#![forbid(unsafe_code)]',
    'CARGO_BIN_EXE_wepld-core',
    'ProtocolVersion',
    'Principal',
    'CancelEnvelope',
    'MAX_PAYLOAD_BYTES',
    '#[test]',
)

DESKTOP_REQUIRED_TOKENS = (
    '#![forbid(unsafe_code)]',
    'CoreClient',
    'CoreClientError',
    'send_health',
    'send_observe_health',
    'send_cancel',
    'diagnostics_truncated',
    'drain_diagnostics',
    'is_ready',
    '#[test]',
)

_INSTALLED = False
_PRIOR_VERIFY_VIEW = None


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


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


class _WithoutS1011Tests(base.RepositoryView):
    def __init__(self, inner: base.RepositoryView):
        self._inner = inner

    def entries(self) -> list[base.TrackedEntry]:
        return [
            entry
            for entry in self._inner.entries()
            if entry.path not in S1_011_TEST_PATHS
        ]

    def read_bytes(self, relative: str, limit: int) -> bytes:
        if relative in S1_011_TEST_PATHS:
            base.fail(f"S1-011 filtered prior-stage view attempted test read: {relative}")
        return self._inner.read_bytes(relative, limit)

    def tree_identity(self, relative: str) -> str | None:
        if relative in S1_011_TEST_PATHS:
            return None
        return self._inner.tree_identity(relative)


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V18_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V18_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v18 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V18_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v18._verify_policy_files(view)


def _read_test_source(
    view: base.RepositoryView,
    relative: str,
    required_tokens: tuple[str, ...],
) -> str:
    data = view.read_bytes(relative, MAX_S1_011_TEST_BYTES)
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"S1-011 test source is not UTF-8: {relative}: {exc}")
    if "\x00" in text:
        base.fail(f"S1-011 test source contains NUL: {relative}")
    if PROHIBITED_TEST_TEXT.search(text):
        base.fail(
            "S1-011 tests may exercise only the admitted local process/stdio boundary; "
            f"prohibited external/shell/network material found: {relative}"
        )
    if "#[ignore]" in text:
        base.fail(f"S1-011 adversarial tests may not be ignored: {relative}")
    if "#[should_panic" in text:
        base.fail(f"S1-011 adversarial tests must assert outcomes explicitly: {relative}")
    missing = [token for token in required_tokens if token not in text]
    if missing:
        base.fail(
            f"S1-011 test source missing required boundary token(s) in {relative}: "
            + ", ".join(missing)
        )
    return text


def _verify_s1_011_tests(view: base.RepositoryView) -> None:
    core = _read_test_source(view, CORE_ADVERSARIAL_TEST_PATH, CORE_REQUIRED_TOKENS)
    desktop = _read_test_source(
        view, DESKTOP_ADVERSARIAL_TEST_PATH, DESKTOP_REQUIRED_TOKENS
    )

    if core.count("#[test]") < 8:
        base.fail("S1-011 Core adversarial suite must contain at least eight explicit tests")
    if desktop.count("#[test]") < 6:
        base.fail("S1-011 Desktop/Core adversarial suite must contain at least six explicit tests")


def _has_s1_011_markers(paths: set[str]) -> bool:
    present = paths & S1_011_TEST_PATHS
    if not present:
        return False
    missing = S1_011_TEST_PATHS - paths
    if missing:
        base.fail(
            "partial S1-011 cross-process adversarial candidate is prohibited; missing: "
            + ", ".join(sorted(missing))
        )
    return True


def _require_test_only_delta(
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

    unexpected = sorted(changed - S1_011_TEST_PATHS)
    if unexpected:
        base.fail(
            "S1-011 candidate delta must be test-only; unexpected changed path(s): "
            + ", ".join(unexpected)
        )

    missing = sorted(S1_011_TEST_PATHS - set(candidate_entries))
    if missing:
        base.fail(
            "S1-011 candidate is missing required adversarial test path(s): "
            + ", ".join(missing)
        )


def verify_view(
    view: base.RepositoryView,
    *,
    policy_base: base.RepositoryView | None = None,
) -> str:
    paths = base.validate_entries(view.entries())
    if not _has_s1_011_markers(paths):
        if _PRIOR_VERIFY_VIEW is None:
            base.fail("S1-011 prior verifier is not installed")
        return _PRIOR_VERIFY_VIEW(view, policy_base=policy_base)

    if _PRIOR_VERIFY_VIEW is None:
        base.fail("S1-011 prior verifier is not installed")

    prior_view = _WithoutS1011Tests(view)
    prior_policy_base = (
        _WithoutS1011Tests(policy_base) if policy_base is not None else None
    )
    prior_stage = _PRIOR_VERIFY_VIEW(
        prior_view,
        policy_base=prior_policy_base,
    )
    if prior_stage != shell.SHELL_STAGE:
        base.fail(
            "S1-011 candidate must extend the canonical S1-010 shell stage; "
            f"observed prior stage={prior_stage}"
        )

    _verify_s1_011_tests(view)
    if policy_base is not None:
        _require_test_only_delta(view, policy_base)
    return S1_011_STAGE


def _install_v19_policy() -> None:
    global _INSTALLED, _PRIOR_VERIFY_VIEW
    if _INSTALLED:
        return

    v18._install_v18_policy()
    _PRIOR_VERIFY_VIEW = shell.verify_view

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
    _INSTALLED = True


def selftest() -> None:
    v18.selftest()
    _install_v19_policy()

    core_good = (
        '#![forbid(unsafe_code)]\n'
        'use std::process::{Command, Stdio};\n'
        'use wepld_contracts::{CancelEnvelope, MAX_PAYLOAD_BYTES, Principal, ProtocolVersion};\n'
        'const CORE: &str = env!("CARGO_BIN_EXE_wepld-core");\n'
        + ''.join(f'#[test]\nfn core_case_{i}() {{ let _ = (CORE, MAX_PAYLOAD_BYTES, ProtocolVersion::V1, Principal::DesktopHost); }}\n' for i in range(8))
    )
    desktop_good = (
        '#![forbid(unsafe_code)]\n'
        'use wepld_desktop::{CoreClient, CoreClientError};\n'
        + ''.join(
            f'#[test]\nfn desktop_case_{i}() {{ let _ = CoreClient::start; let _ = CoreClient::send_health; let _ = CoreClient::send_observe_health; let _ = CoreClient::send_cancel; let _ = CoreClient::diagnostics_truncated; let _ = CoreClient::drain_diagnostics; let _ = CoreClient::is_ready; let _: Option<CoreClientError> = None; }}\n'
            for i in range(6)
        )
    )
    fixture = base.MemoryView(
        {
            CORE_ADVERSARIAL_TEST_PATH: core_good.encode("utf-8"),
            DESKTOP_ADVERSARIAL_TEST_PATH: desktop_good.encode("utf-8"),
        }
    )
    _verify_s1_011_tests(fixture)

    partial = {CORE_ADVERSARIAL_TEST_PATH}
    base.expect_failure_matching(
        "partial S1-011 test stage",
        "partial S1-011 cross-process adversarial candidate is prohibited",
        _has_s1_011_markers,
        partial,
    )

    ignored = core_good.replace("#[test]", "#[ignore]\n#[test]", 1)
    bad_fixture = base.MemoryView(
        {
            CORE_ADVERSARIAL_TEST_PATH: ignored.encode("utf-8"),
            DESKTOP_ADVERSARIAL_TEST_PATH: desktop_good.encode("utf-8"),
        }
    )
    base.expect_failure_matching(
        "ignored S1-011 adversarial test",
        "may not be ignored",
        _verify_s1_011_tests,
        bad_fixture,
    )

    print("wepld S1-011 cross-process adversarial-stage policy self-tests: PASS")


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
