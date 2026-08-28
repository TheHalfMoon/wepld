#!/usr/bin/env python3
"""Append-only repair for the v26 dependency-governance regression fixture.

v27 does not broaden v26 authority. It preserves the exact v26 dependency
manifest/lock/register transition and identity/store product boundary. Its only
purpose is to replace the defective v26 self-test entrypoint with a successor
self-test whose in-memory fixtures include the frozen v24 predecessor required
by the inherited fail-closed verifier chain.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v26_integrity as q

P = ".github/scripts/wepld_s2_identity_store_governance_v27_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v27_selftest.py"
T_BLOB = "62750c6a740a18dfa8a88e5de257569a0c19b560"
V26_P_BLOB = "cfa0c10386bd04cc3721902a7de063defdd754f8"
V26_T_BLOB = "55bcace4105a834c516ed671a83ecf57530b9fe9"

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset(set(q.BOOT) | set(POLICY_FILES))

AUTH = "S2_IDENTITY_STORE_V26_SELFTEST_REPAIR"
S2_IMPLEMENTATION_AUTHORITY = q.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = q.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = q.SOURCE_ADMISSION

Q_WF = dict(q.WF)
WF = {
    q.p.FW: "c76955379b14f19a5ef930ddc1c83d1e07d07603251c917b6dca879d62d68a4d",
    q.p.AW: "4b09cffbcdb39a9fdefa71a4265ae855a287b989ca77b90577ec1be04480f3d9",
    q.p.CW: q.WF[q.p.CW],
}

Q_DELTA = q.delta
Q_BASE = q.basectrl
Q_EXT = q.ext
Q_DEXT = q.dext
Q_EEXT = q.eext
Q_ALLOWED = q.allowed
Q_FILES = q.files
Q_PRINTER = q.printer

root = q.root
for _path, _expected in (
    (q.P, V26_P_BLOB),
    (q.T, V26_T_BLOB),
    (T, T_BLOB),
):
    _actual = q.p.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v27 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = q._call
_attr = q._attr
_bind = q._bind
_INST = False
_PRINT: Any = None


def prepare_q() -> None:
    current = dict(q.WF)
    if current not in (Q_WF, dict(WF)):
        base.fail(f"v27 predecessor workflow identity map drifted: actual={current}")
    q.WF = dict(WF)


def delta(candidate: Any, policy_base: Any) -> None:
    paths = q.p.changed(q.p.v24.v23, candidate, policy_base)

    if q.p.bootbase(policy_base):
        if paths == BOOT:
            q.p.req_v24(candidate)
            q.p.req_v24(policy_base)
            if not q._baseline_dependency_state(candidate) or not q._baseline_dependency_state(
                policy_base
            ):
                base.fail(
                    "v27 bootstrap requires unchanged canonical baseline "
                    "manifest/lock/register state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v27 bootstrap delta must be exactly seven policy files plus two workflows"
            )
        base.fail("v27 bootstrap base authorizes only exact self-test repair activation")

    if paths & ALL_POLICY_FILES:
        base.fail("canonical v27/v26/v25 policy files are frozen after activation")

    Q_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    Q_BASE(candidate, policy_base)


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in q.p.ps(candidate):
            base.fail(f"v27 policy file missing: {path}")
        if q.p.bootbase(policy_base):
            if path in q.p.ps(policy_base):
                base.fail(f"v27 policy file unexpectedly in bootstrap base: {path}")
        elif path not in q.p.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v27 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        Q_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, q.p.extset(q.p.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, q.p.extset(q.p.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES
    if remaining:
        Q_ALLOWED(remaining, stage)


def files(view: Any) -> None:
    Q_FILES(view)
    missing = POLICY_FILES - q.p.ps(view)
    if missing:
        base.fail(f"v27 policy files missing: {sorted(missing)}")
    for path in sorted(POLICY_FILES):
        if q.p.mode(view, path) != "100644":
            base.fail(f"v27 policy file mode invalid: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not Q_PRINTER:
        base.fail("v27 predecessor printer drifted")
    _call("v26 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v27=V26_SELFTEST_FIXTURE_REPAIR_ONLY")
    print(f"v27_authority={AUTH}")
    print(f"s2_implementation_authority_v27={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v27={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v27={SOURCE_ADMISSION}")


def overlay() -> None:
    shell, routing, _, desktop, execution = q.p.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v27 installed overlay drifted")
    if dict(q.WF) != dict(WF) or dict(q.p.WF) != dict(WF):
        base.fail("v27 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    prepare_q()
    q.install()
    shell, routing, _, desktop, execution = q.p.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v26 routing hook"), Q_DELTA),
        (base.compare_base_controlled, Q_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "v26 desktop hook"), Q_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v26 execution hook"), Q_EEXT),
        (_attr(shell, "validate_allowed_paths", "v26 allowed hook"), Q_ALLOWED),
        (_attr(shell, "verify_policy_files", "v26 files hook"), Q_FILES),
        (_attr(shell, "print_success", "v26 printer"), Q_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v27 predecessor hook drifted")

    _PRINT = Q_PRINTER
    desktop_extensions = frozenset(set(q.p.extset(desktop)) | set(POLICY_FILES))
    execution_extensions = frozenset(set(q.p.extset(execution)) | set(POLICY_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v27 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v27 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v27 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v27 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v27 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v27 allowed hook")
    _bind(shell, "verify_policy_files", files, "v27 files hook")
    _bind(shell, "print_success", printer, "v27 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v27_selftest import run

    run()


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0
        install()
        if argv and argv[0] == "verify-candidate-local":
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("--root", required=True)
            parser.add_argument("--policy-base-root", required=True)
            parser.add_argument("--policy-base-sha", required=True)
            args = parser.parse_args(argv[1:])
            return int(
                _call(
                    "candidate-local verifier",
                    q.p.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", q.p.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
