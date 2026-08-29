#!/usr/bin/env python3
"""Append-only provenance repair for the future S2 dependency decision.

v29 preserves the canonical v28 staged authority and changes no dependency or
product bytes. It repairs exactly one future dependency-register provenance
datum before S2-AUTH-012 can be presented: rust-random/getrandom tag v0.4.3
resolves to commit 5e7cd5733536844a9856dc7259bd4696bbe5e3ae, not the unrelated
later Cargo.lock update commit recorded by v26.

The repair is applied at the active policy layer by replacing exactly one
SOURCE_REVISION line in the future S2 dependency-register append template.
Everything else in the v26 decision template remains byte-identical.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v28_integrity as s

P = ".github/scripts/wepld_s2_identity_store_governance_v29_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v29_selftest.py"
T_BLOB = "38721c4c5bccc3716105e44a4aad2b0cec63cd69"
V28_P_BLOB = "ebd00a15ac4df9d8f94a01c6a2e9c9b7316dc879"
V28_T_BLOB = "c1cdffff534372554269afc33e43c00486a16b97"

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(s.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, s.r.q.p.FW, s.r.q.p.AW})

AUTH = "S2_IDENTITY_STORE_GETRANDOM_PROVENANCE_REPAIR"
S2_IMPLEMENTATION_AUTHORITY = s.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = s.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = s.SOURCE_ADMISSION

INCORRECT_GETRANDOM_SOURCE_REVISION = (
    b"SOURCE_REVISION = eeb6a3d4ade21087c0f7bd560192e4bfb8357670"
)
CORRECT_GETRANDOM_SOURCE_REVISION = (
    b"SOURCE_REVISION = 5e7cd5733536844a9856dc7259bd4696bbe5e3ae"
)
SHA2_SOURCE_REVISION = (
    b"SOURCE_REVISION = 82c36a428f8d6f05f3bfccdedb243e9d1f85359d"
)
ORIGINAL_S2_DEPENDENCY_REGISTER_APPEND = s.r.q.S2_DEPENDENCY_REGISTER_APPEND

if ORIGINAL_S2_DEPENDENCY_REGISTER_APPEND.count(
    INCORRECT_GETRANDOM_SOURCE_REVISION
) != 1:
    base.fail("v29 predecessor getrandom source revision marker drifted")
if CORRECT_GETRANDOM_SOURCE_REVISION in ORIGINAL_S2_DEPENDENCY_REGISTER_APPEND:
    base.fail("v29 predecessor unexpectedly already contains corrected getrandom revision")
if ORIGINAL_S2_DEPENDENCY_REGISTER_APPEND.count(SHA2_SOURCE_REVISION) != 1:
    base.fail("v29 predecessor sha2 source revision marker drifted")

CORRECTED_S2_DEPENDENCY_REGISTER_APPEND = (
    ORIGINAL_S2_DEPENDENCY_REGISTER_APPEND.replace(
        INCORRECT_GETRANDOM_SOURCE_REVISION,
        CORRECT_GETRANDOM_SOURCE_REVISION,
        1,
    )
)
if (
    CORRECTED_S2_DEPENDENCY_REGISTER_APPEND.count(
        CORRECT_GETRANDOM_SOURCE_REVISION
    )
    != 1
    or INCORRECT_GETRANDOM_SOURCE_REVISION
    in CORRECTED_S2_DEPENDENCY_REGISTER_APPEND
    or CORRECTED_S2_DEPENDENCY_REGISTER_APPEND.count(SHA2_SOURCE_REVISION) != 1
):
    base.fail("v29 corrected dependency-register append construction drifted")

S_WF = dict(s.WF)
WF = {
    s.r.q.p.FW: "9bc7e787b4dda6cd3e770522d79c54203ebf0838a7579eaf49e1a74242a0e4fe",
    s.r.q.p.AW: "438c60f7e543a8945c58c387498c7a91ad72c18c27c57443f274a20563ebb59d",
    s.r.q.p.CW: s.WF[s.r.q.p.CW],
}

S_DELTA = s.delta
S_BASE = s.basectrl
S_EXT = s.ext
S_DEXT = s.dext
S_EEXT = s.eext
S_ALLOWED = s.allowed
S_FILES = s.files
S_PRINTER = s.printer

root = s.root
for _path, _expected in (
    (s.P, V28_P_BLOB),
    (s.T, V28_T_BLOB),
    (T, T_BLOB),
):
    _actual = s.r.q.p.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v29 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = s._call
_attr = s._attr
_bind = s._bind
_INST = False
_PRINT: Any = None


def bootbase(view: Any) -> bool:
    return P not in s.r.q.p.ps(view)


def req_v28(view: Any) -> None:
    for path, expected in ((s.P, V28_P_BLOB), (s.T, V28_T_BLOB)):
        if path not in s.r.q.p.ps(view):
            base.fail(f"v29 candidate/base is missing frozen v28 predecessor: {path}")
        actual = s.r.q.p.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v28 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def prepare_s() -> None:
    current = dict(s.WF)
    if current not in (S_WF, dict(WF)):
        base.fail(f"v29 predecessor workflow identity map drifted: actual={current}")

    current_append = s.r.q.S2_DEPENDENCY_REGISTER_APPEND
    if current_append not in (
        ORIGINAL_S2_DEPENDENCY_REGISTER_APPEND,
        CORRECTED_S2_DEPENDENCY_REGISTER_APPEND,
    ):
        base.fail("v29 predecessor dependency-register append drifted before repair")

    s.WF = dict(WF)
    s.r.WF = dict(WF)
    s.r.q.WF = dict(WF)
    s.r.q.p.WF = dict(WF)
    s.r.q.S2_DEPENDENCY_REGISTER_APPEND = (
        CORRECTED_S2_DEPENDENCY_REGISTER_APPEND
    )


def delta(candidate: Any, policy_base: Any) -> None:
    paths = s.r.q.p.changed(s.r.q.p.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths == BOOT:
            req_v28(candidate)
            req_v28(policy_base)
            if not s.r.q._baseline_dependency_state(
                candidate
            ) or not s.r.q._baseline_dependency_state(policy_base):
                base.fail(
                    "v29 bootstrap requires unchanged canonical baseline "
                    "manifest/lock/register state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v29 bootstrap delta must be exactly two v29 policy files "
                "plus two integrity workflows"
            )
        base.fail(
            "v29 bootstrap base authorizes only exact getrandom provenance repair activation"
        )

    if paths & ALL_POLICY_FILES:
        base.fail("canonical v29/v28/v27/v26/v25 policy files are frozen after activation")

    S_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    S_BASE(candidate, policy_base)


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in s.r.q.p.ps(candidate):
            base.fail(f"v29 policy file missing: {path}")
        if bootbase(policy_base):
            if path in s.r.q.p.ps(policy_base):
                base.fail(f"v29 policy file unexpectedly in bootstrap base: {path}")
        elif path not in s.r.q.p.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v29 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        S_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, s.r.q.p.extset(s.r.q.p.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, s.r.q.p.extset(s.r.q.p.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES
    if remaining:
        S_ALLOWED(remaining, stage)


def files(view: Any) -> None:
    S_FILES(view)
    missing = POLICY_FILES - s.r.q.p.ps(view)
    if missing:
        base.fail(f"v29 policy files missing: {sorted(missing)}")
    for path in sorted(POLICY_FILES):
        if s.r.q.p.mode(view, path) != "100644":
            base.fail(f"v29 policy file mode invalid: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not S_PRINTER:
        base.fail("v29 predecessor printer drifted")
    _call("v28 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v29=GETRANDOM_PROVENANCE_REPAIR_ONLY")
    print(f"v29_authority={AUTH}")
    print(f"s2_implementation_authority_v29={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v29={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v29={SOURCE_ADMISSION}")
    print(
        "getrandom_v0_4_3_source_revision_v29="
        "5e7cd5733536844a9856dc7259bd4696bbe5e3ae"
    )


def overlay() -> None:
    shell, routing, _, desktop, execution = s.r.q.p.topo()
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
        base.fail("v29 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in (s, s.r, s.r.q, s.r.q.p)):
        base.fail("v29 workflow identity projection drifted")
    if s.r.q.S2_DEPENDENCY_REGISTER_APPEND != CORRECTED_S2_DEPENDENCY_REGISTER_APPEND:
        base.fail("v29 corrected dependency-register append projection drifted")


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    prepare_s()
    s.install()
    shell, routing, _, desktop, execution = s.r.q.p.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v28 routing hook"), S_DELTA),
        (base.compare_base_controlled, S_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "v28 desktop hook"), S_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v28 execution hook"), S_EEXT),
        (_attr(shell, "validate_allowed_paths", "v28 allowed hook"), S_ALLOWED),
        (_attr(shell, "verify_policy_files", "v28 files hook"), S_FILES),
        (_attr(shell, "print_success", "v28 printer"), S_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v29 predecessor hook drifted")

    _PRINT = S_PRINTER
    desktop_extensions = frozenset(
        set(s.r.q.p.extset(desktop)) | set(POLICY_FILES)
    )
    execution_extensions = frozenset(
        set(s.r.q.p.extset(execution)) | set(POLICY_FILES)
    )
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v29 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v29 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v29 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v29 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v29 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v29 allowed hook")
    _bind(shell, "verify_policy_files", files, "v29 files hook")
    _bind(shell, "print_success", printer, "v29 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v29_selftest import run

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
                    s.r.q.p.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", s.r.q.p.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
