#!/usr/bin/env python3
"""Freeze fixed Core error values at the S1-010 Tauri boundary.

This wrapper binds exact v16 and repairs one reviewed error-boundary gap. The
future frozen main.rs may not forward Debug-formatted CoreClient errors into the
WebView. Request-send failures use one fixed value and receive failures use one
fixed value while all v16 transaction/correlation/boundedness semantics remain
unchanged.

No product bytes, dependencies, plugins, process/filesystem/network authority,
background workers, UI redesign, branding work, or S1-011+ scope is added.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v17.py"
PRIOR_V16_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v16.py"
EXPECTED_PRIOR_V16_RUNNER_GIT_BLOB_SHA1 = "deccc700c4a2f399326f9f3bcf38686c9d954106"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "f840e3a6e030fb05d1c018aac134ce2dbfd88d6dc9695f018950e995191673f2",
    ".github/workflows/s1-admission-integrity.yml": "50c59afd451ab5884a055b1b45c1d03be5c6700a8f8eb5b0de9e0584b84ce007",
    ".github/workflows/s1-contracts.yml": "e4c93efe1fa8813e43c5ce5e90c296dad0cefd8f366a33e5ee69791734298e91",
}

FIXED_REQUEST_ERROR = "core request failed"
FIXED_RESPONSE_ERROR = "core response unavailable"


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v16_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v16.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v16 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V16_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v16 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V16_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v16_runner_before_import()
import wepld_s1_shell_integrity_v16 as v16  # noqa: E402

v15 = v16.v15
v14 = v16.v14
v13 = v16.v13
v12 = v16.v12
v11 = v16.v11
v10 = v16.v10
v9 = v16.v9
v8 = v16.v8
v7 = v16.v7
v6 = v16.v6
v5 = v16.v5
v4 = v16.v4
v3 = v16.v3
v2 = v16.v2
shell = v16.shell

PRIOR_V16_MAIN = v16.EXPECTED_BOUNDED_DEMUX_MAIN
_INSTALLED = False


def _fixed_error_main_from_v16() -> str:
    text = PRIOR_V16_MAIN
    send_error = '.map_err(|error| format!("{error:?}"))?;'
    receive_error = 'client.receive().map_err(|error| format!("{error:?}"))?'

    if text.count(send_error) != 6:
        base.fail("unexpected v16 request-error site count while constructing v17 template")
    if text.count(receive_error) != 6:
        base.fail("unexpected v16 receive-error site count while constructing v17 template")

    text = text.replace(
        send_error,
        f'.map_err(|_| String::from("{FIXED_REQUEST_ERROR}"))?;',
    )
    text = text.replace(
        receive_error,
        f'client.receive().map_err(|_| String::from("{FIXED_RESPONSE_ERROR}"))?',
    )
    if 'format!("{error:?}")' in text:
        base.fail("variable Core error formatting remained in v17 template")
    return text


EXPECTED_FIXED_ERROR_MAIN = _fixed_error_main_from_v16()


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V16_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V16_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v16 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V16_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v16._verify_policy_files(view)


def _install_v17_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v16._install_v16_policy()

    for module in (
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

    v16.EXPECTED_BOUNDED_DEMUX_MAIN = EXPECTED_FIXED_ERROR_MAIN
    v15.EXPECTED_DEMUX_MAIN = EXPECTED_FIXED_ERROR_MAIN
    v13.EXPECTED_RECONCILED_MAIN = EXPECTED_FIXED_ERROR_MAIN
    v12.EXPECTED_STATUS_MAIN = EXPECTED_FIXED_ERROR_MAIN

    shell.verify_policy_files = _verify_policy_files
    _INSTALLED = True


def selftest() -> None:
    v16.selftest()
    _install_v17_policy()

    safe = v3._safe_v3_fixture()
    safe["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_FIXED_ERROR_MAIN.encode("ascii")
    safe["apps/desktop/ui/app.js"] = v13.EXPECTED_SERIALIZED_JS.encode("ascii")
    fixture = base.MemoryView(safe)

    v12._verify_shell_rust(fixture)
    v3._verify_frontend(fixture)
    shell.verify_shell_config(fixture)

    old_debug_template = dict(safe)
    old_debug_template["apps/desktop/src-tauri/src/main.rs"] = PRIOR_V16_MAIN.encode("ascii")
    base.expect_failure_matching(
        "S1-010 variable Core error forwarding",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(old_debug_template),
    )

    debug_send = dict(safe)
    debug_send["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_FIXED_ERROR_MAIN.replace(
        f'.map_err(|_| String::from("{FIXED_REQUEST_ERROR}"))?;',
        '.map_err(|error| format!("{error:?}"))?;',
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 Debug-formatted request failure",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(debug_send),
    )

    debug_receive = dict(safe)
    debug_receive["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_FIXED_ERROR_MAIN.replace(
        f'client.receive().map_err(|_| String::from("{FIXED_RESPONSE_ERROR}"))?',
        'client.receive().map_err(|error| format!("{error:?}"))?',
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 Debug-formatted response failure",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(debug_receive),
    )

    alternate_request_error = dict(safe)
    alternate_request_error["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_FIXED_ERROR_MAIN.replace(
        FIXED_REQUEST_ERROR,
        "request failed with detail",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 request error contract drift",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(alternate_request_error),
    )

    print("wepld S1 Tauri shell fixed error-boundary policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v17_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
