#!/usr/bin/env python3
"""Bound total event-demultiplex transaction lifetime for S1-010.

This wrapper binds exact v15 and repairs one availability gap: a per-receive
5-second timeout is not a total transaction bound when an endless stream of
valid Events can keep resetting that timeout. The exact future main.rs therefore
uses at most 33 receive attempts, allowing at most 32 interleaved Events before
failing closed.

No product bytes, helper functions, background workers, dependencies, plugins,
process/filesystem/network authority, branding work, or S1-011+ scope is added.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v16.py"
PRIOR_V15_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v15.py"
EXPECTED_PRIOR_V15_RUNNER_GIT_BLOB_SHA1 = "6c517db7ce1a306fc746a853acba1f0e89c820b3"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "c54de02a879acd44e3aac59a0d4e7c97dcca2cb1347f90a3115187ebd2afca67",
    ".github/workflows/s1-admission-integrity.yml": "3bea45cb3d9ea1dc56f90ebdce1f57ca803c01af647efb7af84bfd1cdc4b3209",
    ".github/workflows/s1-contracts.yml": "315932a7f2be05ecb5ac23fe0132ff15245806d768b8c2d793c021717dd404f8",
}

MAX_INTERLEAVED_EVENTS_PER_TRANSACTION = 32


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v15_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v15.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v15 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V15_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v15 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V15_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v15_runner_before_import()
import wepld_s1_shell_integrity_v15 as v15  # noqa: E402

v14 = v15.v14
v13 = v15.v13
v12 = v15.v12
v11 = v15.v11
v10 = v15.v10
v9 = v15.v9
v8 = v15.v8
v7 = v15.v7
v6 = v15.v6
v5 = v15.v5
v4 = v15.v4
v3 = v15.v3
v2 = v15.v2
shell = v15.shell

_INSTALLED = False


def _bounded_main_from_v15() -> str:
    text = v15.EXPECTED_DEMUX_MAIN
    if text.count("    loop {\n") != 6:
        base.fail("unexpected v15 transaction-loop count while constructing v16 template")
    text = text.replace("    loop {\n", "    for _ in 0..=32 {\n")
    errors = (
        "unexpected readiness response",
        "unexpected health response",
        "unexpected version response",
        "unexpected capabilities response",
        "unexpected observation response",
        "unexpected cancellation response",
    )
    for message in errors:
        needle = (
            '            InboundEnvelope::Response(_) => {\n'
            f'                return Err(String::from("{message}"));\n'
            '            }\n'
            '        }\n'
            '    }\n'
            '}\n'
        )
        replacement = (
            '            InboundEnvelope::Response(_) => {\n'
            f'                return Err(String::from("{message}"));\n'
            '            }\n'
            '        }\n'
            '    }\n'
            '    Err(String::from("core response event budget exceeded"))\n'
            '}\n'
        )
        if text.count(needle) != 1:
            base.fail(
                "unexpected v15 transaction tail while constructing v16 template: "
                + message
            )
        text = text.replace(needle, replacement, 1)
    return text


EXPECTED_BOUNDED_DEMUX_MAIN = _bounded_main_from_v15()


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V15_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V15_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v15 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V15_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v15._verify_policy_files(view)


def _install_v16_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v15._install_v15_policy()

    for module in (
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

    shell.SHELL_RUST_PROHIBITED_IDENTIFIERS = frozenset(
        (set(shell.SHELL_RUST_PROHIBITED_IDENTIFIERS) | {"loop"}) - {"for"}
    )

    v15.EXPECTED_DEMUX_MAIN = EXPECTED_BOUNDED_DEMUX_MAIN
    v13.EXPECTED_RECONCILED_MAIN = EXPECTED_BOUNDED_DEMUX_MAIN
    v12.EXPECTED_STATUS_MAIN = EXPECTED_BOUNDED_DEMUX_MAIN

    shell.verify_policy_files = _verify_policy_files
    _INSTALLED = True


def selftest() -> None:
    v15.selftest()
    _install_v16_policy()

    safe = v3._safe_v3_fixture()
    safe["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_BOUNDED_DEMUX_MAIN.encode("ascii")
    safe["apps/desktop/ui/app.js"] = v13.EXPECTED_SERIALIZED_JS.encode("ascii")
    fixture = base.MemoryView(safe)

    v12._verify_shell_rust(fixture)
    v3._verify_frontend(fixture)
    shell.verify_shell_config(fixture)

    exact_v15 = dict(safe)
    exact_v15["apps/desktop/src-tauri/src/main.rs"] = (
        EXPECTED_BOUNDED_DEMUX_MAIN
        .replace("    for _ in 0..=32 {\n", "    loop {\n")
        .replace(
            '    }\n    Err(String::from("core response event budget exceeded"))\n}\n',
            '    }\n}\n',
        )
        .encode("ascii")
    )
    base.expect_failure_matching(
        "S1-010 unbounded transaction loop",
        "prohibited effect identifier(s): loop",
        v12._verify_shell_rust,
        base.MemoryView(exact_v15),
    )

    widened_budget = dict(safe)
    widened_budget["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_BOUNDED_DEMUX_MAIN.replace(
        "0..=32", "0..=33", 1
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 event demux budget widening",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(widened_budget),
    )

    missing_budget_failure = dict(safe)
    missing_budget_failure["apps/desktop/src-tauri/src/main.rs"] = (
        EXPECTED_BOUNDED_DEMUX_MAIN.replace(
            '    Err(String::from("core response event budget exceeded"))\n',
            "",
            1,
        ).encode("ascii")
    )
    base.expect_failure_matching(
        "S1-010 missing bounded event-demux failure",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(missing_budget_failure),
    )

    print("wepld S1 Tauri shell bounded event-demultiplex policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v16_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
