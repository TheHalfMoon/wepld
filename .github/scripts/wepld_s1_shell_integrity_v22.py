#!/usr/bin/env python3
"""Authorize only the exact Clippy-safe projection of the frozen S1-011 suite.

Canonical v21 keeps the reviewed v19 templates immutable and authorizes their
exact pinned-rustfmt projection. Exact-head S1-011 qualification then proved one
additional deterministic Core-only lint blocker: a `PendingRequest` returned by
`HandshakeState::accept_request()` is intentionally retained only to consume an
in-flight budget slot, but the frozen test discards the must-use value.

v22 preserves v21's trusted-base, local-Git-object, rustfmt, and remote/data-only
admission mechanics. It authorizes exactly one further source rewrite in the
Core adversarial test projection: prefix that already-reviewed call with
`let _ =` so the intentional discard is explicit. Desktop projected bytes are
unchanged. No product/runtime/dependency/UI bytes or S1-012+ authority are added.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v22.py"
PRIOR_V21_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v21.py"
EXPECTED_PRIOR_V21_RUNNER_GIT_BLOB_SHA1 = "61aedc6b53afd677a9d6aef5982f32ae50dd46cf"
CANONICAL_REPOSITORY = "TheHalfMoon/wepld"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "3976ca9a0c98346acb253ba3d2954a4bb6e4af9a39a4c13bd6b430ac605bb481",
    ".github/workflows/s1-admission-integrity.yml": "61e9ca7f3bb3a681f973b13bc9d5620a02086e00cc1ab3e8ddaeec8de31a2fa1",
    ".github/workflows/s1-contracts.yml": "2ab777e867c60ef545e1b96dd4ff01546ca268eb794ce5bc620c98e9af0fbc27",
}

CORE_CLIPPY_BEFORE = b"""        state
            .accept_request(match health_request(request_id) {
                ProtocolEnvelope::Request(request) => request,
                _ => unreachable!(\"health helper always returns a request\"),
            })
            .expect(\"in-flight reservation within budget must succeed\");
"""

CORE_CLIPPY_AFTER = b"""        let _ = state
            .accept_request(match health_request(request_id) {
                ProtocolEnvelope::Request(request) => request,
                _ => unreachable!(\"health helper always returns a request\"),
            })
            .expect(\"in-flight reservation within budget must succeed\");
"""

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v21_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v21.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-011 v21 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V21_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v21 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V21_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v21_runner_before_import()
import wepld_s1_shell_integrity_v21 as v21  # noqa: E402

v20 = v21.v20
v19 = v21.v19
v18 = v21.v18
v17 = v21.v17
v16 = v21.v16
v15 = v21.v15
v14 = v21.v14
v13 = v21.v13
v12 = v21.v12
v11 = v21.v11
v10 = v21.v10
v9 = v21.v9
v8 = v21.v8
v7 = v21.v7
v6 = v21.v6
v5 = v21.v5
v4 = v21.v4
v3 = v21.v3
v2 = v21.v2
shell = v21.shell


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V21_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V21_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-011 v21 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V21_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v21._verify_policy_files(view)


def _clippy_projection(template_path: str, data: bytes) -> bytes:
    projected = v21._rustfmt_projection(template_path, data)
    if template_path == v19.CORE_TEST_TEMPLATE_PATH:
        return v21._replace_exactly_once(
            projected,
            CORE_CLIPPY_BEFORE,
            CORE_CLIPPY_AFTER,
            "core-clippy:1",
        )
    if template_path == v19.DESKTOP_TEST_TEMPLATE_PATH:
        return projected
    base.fail(f"unexpected S1-011 Clippy projection template: {template_path}")


def _verify_clippy_projected_test_source(
    candidate: base.RepositoryView,
    candidate_path: str,
    trusted_templates: base.RepositoryView,
    template_path: str,
) -> None:
    template = trusted_templates.read_bytes(
        template_path,
        v19.MAX_S1_011_SOURCE_BYTES,
    )
    expected = _clippy_projection(template_path, template)
    actual = candidate.read_bytes(candidate_path, v19.MAX_S1_011_SOURCE_BYTES)
    if actual != expected:
        base.fail(
            "S1-011 test source must match the exact Clippy-safe projection of "
            f"the frozen reviewed template byte-for-byte: {candidate_path}"
        )


def _install_v22_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v21._install_v21_policy()

    # v21 already constrains candidate bytes to the exact pinned-rustfmt
    # projection of immutable v19 templates. Tighten that single hook only:
    # Core gets one explicit intentional-discard prefix; Desktop is unchanged.
    v19._verify_exact_test_source = _verify_clippy_projected_test_source

    for module in (
        v21,
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


def _selftest_clippy_projection() -> None:
    view = base.LocalRepositoryView(v21._repository_root())

    core_template = view.read_bytes(
        v19.CORE_TEST_TEMPLATE_PATH,
        v19.MAX_S1_011_SOURCE_BYTES,
    )
    v21_core = v21._rustfmt_projection(v19.CORE_TEST_TEMPLATE_PATH, core_template)
    v22_core = _clippy_projection(v19.CORE_TEST_TEMPLATE_PATH, core_template)
    if v22_core == v21_core:
        base.fail("Core Clippy projection self-test made no change")
    if v21_core.count(CORE_CLIPPY_BEFORE) != 1:
        base.fail("Core Clippy projection source occurrence self-test failed")
    if v22_core.count(CORE_CLIPPY_AFTER) != 1:
        base.fail("Core Clippy projection target occurrence self-test failed")
    if v22_core.replace(CORE_CLIPPY_AFTER, CORE_CLIPPY_BEFORE, 1) != v21_core:
        base.fail("Core Clippy projection changed bytes beyond the one repair")

    desktop_template = view.read_bytes(
        v19.DESKTOP_TEST_TEMPLATE_PATH,
        v19.MAX_S1_011_SOURCE_BYTES,
    )
    v21_desktop = v21._rustfmt_projection(
        v19.DESKTOP_TEST_TEMPLATE_PATH,
        desktop_template,
    )
    v22_desktop = _clippy_projection(
        v19.DESKTOP_TEST_TEMPLATE_PATH,
        desktop_template,
    )
    if v22_desktop != v21_desktop:
        base.fail("Desktop bytes changed in Core-only Clippy projection")


def selftest() -> None:
    v21.selftest()
    _install_v22_policy()
    _selftest_clippy_projection()

    if base.REPOSITORY != CANONICAL_REPOSITORY:
        base.fail(
            "canonical repository identity drifted: "
            f"expected={CANONICAL_REPOSITORY} actual={base.REPOSITORY}"
        )

    print("wepld S1-011 Clippy-safe qualification policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v22_policy()
    return v21.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
