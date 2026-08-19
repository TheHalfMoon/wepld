#!/usr/bin/env python3
"""Negative-oracle harness repair for S1-010 review reconciliation.

This wrapper binds the exact v13 policy and preserves its product semantics
unchanged. It repairs only one self-test expectation: the inherited v2 frontend
verifier rejects the old racy cancellation shape earlier, with the more specific
"must cancel the exact stored observation request id" reason.

No product template, dependency, process, filesystem, network, plugin, sidecar,
UI-design, branding, or S1-011+ authority is added by this layer.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v14.py"
PRIOR_V13_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v13.py"
EXPECTED_PRIOR_V13_RUNNER_GIT_BLOB_SHA1 = "faff24dab9c1fe151f35e5d55592624aed33e7ce"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "3063053d14841add9b2068209e2285a80bd27e4da1571159a025dc1a51c29908",
    ".github/workflows/s1-admission-integrity.yml": "436e2700e5bd4b731584d614487e072facb9c10ea37c3e076697c4b31d3dedc4",
    ".github/workflows/s1-contracts.yml": "e1e31cf2132e496b45ce610af3385e738be5bb9b7dbb3a59be84ed0144513588",
}


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v13_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v13.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v13 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V13_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v13 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V13_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v13_runner_before_import()
import wepld_s1_shell_integrity_v13 as v13  # noqa: E402

v12 = v13.v12
v11 = v13.v11
v10 = v13.v10
v9 = v13.v9
v8 = v13.v8
v7 = v13.v7
v6 = v13.v6
v5 = v13.v5
v4 = v13.v4
v3 = v13.v3
v2 = v13.v2
shell = v13.shell

_INSTALLED = False


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V13_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V13_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v13 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V13_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v13._verify_policy_files(view)


def _install_v14_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v13._install_v13_policy()

    for module in (
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


def selftest() -> None:
    # Re-run every inherited v1-v12 oracle without entering v13's superseded
    # wrong-reason assertion, then install the unchanged v13 semantics.
    v12.selftest()
    _install_v14_policy()

    safe = v3._safe_v3_fixture()
    safe["apps/desktop/src-tauri/src/main.rs"] = v13.EXPECTED_RECONCILED_MAIN.encode(
        "ascii"
    )
    safe["apps/desktop/ui/app.js"] = v13.EXPECTED_SERIALIZED_JS.encode("ascii")
    fixture = base.MemoryView(safe)

    v12._verify_shell_rust(fixture)
    v3._verify_frontend(fixture)

    old_v12_readiness = dict(safe)
    old_v12_readiness["apps/desktop/src-tauri/src/main.rs"] = (
        v13.PRIOR_V12_STATUS_MAIN.encode("ascii")
    )
    base.expect_failure_matching(
        "S1-010 readiness may not fabricate false on unavailable Core",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(old_v12_readiness),
    )

    old_racy_frontend = dict(safe)
    old_racy_frontend["apps/desktop/ui/app.js"] = v13.PRIOR_V3_JS.encode("ascii")
    base.expect_failure_matching(
        "S1-010 overlapping observation start/cancel race",
        "S1-010 JavaScript must cancel the exact stored observation request id",
        v3._verify_frontend,
        base.MemoryView(old_racy_frontend),
    )

    missing_busy_guard = dict(safe)
    missing_busy_guard["apps/desktop/ui/app.js"] = (
        v13.EXPECTED_SERIALIZED_JS.replace(
            "  if (observationBusy || observationRequestId !== null) return;\n",
            "",
            1,
        ).encode("ascii")
    )
    base.expect_failure_matching(
        "S1-010 observation start serialization guard",
        "frozen direct-invoke/status-projection/request-identity template",
        v3._verify_frontend,
        base.MemoryView(missing_busy_guard),
    )

    missing_target_guard = dict(safe)
    missing_target_guard["apps/desktop/ui/app.js"] = (
        v13.EXPECTED_SERIALIZED_JS.replace(
            "    if (observationRequestId === requestId) observationRequestId = null;\n",
            "    observationRequestId = null;\n",
            1,
        ).encode("ascii")
    )
    base.expect_failure_matching(
        "S1-010 cancellation target identity guard",
        "frozen direct-invoke/status-projection/request-identity template",
        v3._verify_frontend,
        base.MemoryView(missing_target_guard),
    )

    print("wepld S1 Tauri shell negative-oracle harness self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v14_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
