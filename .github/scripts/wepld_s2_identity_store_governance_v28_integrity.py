#!/usr/bin/env python3
"""Append-only exact-head review repair successor for S2 identity/store governance.

v28 preserves the v25 -> v26 -> v27 staged authority model. It narrows the
active policy chain in response to exact-head review by:

1. hardening the future product tranche so the Rust integration test path is
   subject to the same unsafe/effect-token checks as the product modules;
2. explicitly projecting the v28 workflow identities through every predecessor
   module before installation, proving the fresh-install map is coherent;
3. bypassing the historical v26 tracked-path filter so DEPENDENCY_REGISTER stays
   visible to inherited required-path validation; and
4. adding regression coverage for register-only/history/mixed-product cases and
   the published authority markers.

No dependency, product, process, network, model/provider, source-admission, or
S3+ authority is added by this successor.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v27_integrity as r

P = ".github/scripts/wepld_s2_identity_store_governance_v28_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v28_selftest.py"
T_BLOB = "c1cdffff534372554269afc33e43c00486a16b97"
V27_P_BLOB = "2c99ad5844fbeb6d223047394824b0082d41e959"
V27_T_BLOB = "62750c6a740a18dfa8a88e5de257569a0c19b560"

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(r.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset(set(r.BOOT) | set(POLICY_FILES))

AUTH = "S2_IDENTITY_STORE_EXACT_HEAD_REVIEW_REPAIR"
S2_IMPLEMENTATION_AUTHORITY = r.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = r.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = r.SOURCE_ADMISSION

R_WF = dict(r.WF)
WF = {
    r.q.p.FW: "b91a0e0849e173d9cc43eff8d29dc2a2ae064f3078be6668920be76fc50c62ee",
    r.q.p.AW: "d2f5965d7bc0c354f33652bad31bdc3325fce5972b03e2ed08c34ef8e08f2ae1",
    r.q.p.CW: r.WF[r.q.p.CW],
}

R_DELTA = r.delta
R_BASE = r.basectrl
R_EXT = r.ext
R_DEXT = r.dext
R_EEXT = r.eext
R_FILES = r.files
R_PRINTER = r.printer
R_V25_PRODUCT_VERIFY = r.q.p._verify_product_files

root = r.root
for _path, _expected in (
    (r.P, V27_P_BLOB),
    (r.T, V27_T_BLOB),
    (T, T_BLOB),
):
    _actual = r.q.p.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v28 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = r._call
_attr = r._attr
_bind = r._bind
_INST = False
_PRINT: Any = None


def prepare_r() -> None:
    current = dict(r.WF)
    if current not in (R_WF, dict(WF)):
        base.fail(f"v28 predecessor workflow identity map drifted: actual={current}")
    # Bind every shared predecessor module explicitly before installation.
    # This makes the workflow projection order obvious and fail-closed.
    r.WF = dict(WF)
    r.q.WF = dict(WF)
    r.q.p.WF = dict(WF)


def _hardened_product_verify(view: Any) -> None:
    R_V25_PRODUCT_VERIFY(view)
    r.q.p._support_verify_product_modules(
        view,
        frozenset({r.q.p.PRODUCT_TEST}),
    )


def delta(candidate: Any, policy_base: Any) -> None:
    paths = r.q.p.changed(r.q.p.v24.v23, candidate, policy_base)

    if r.q.p.bootbase(policy_base):
        if paths == BOOT:
            r.q.p.req_v24(candidate)
            r.q.p.req_v24(policy_base)
            if not r.q._baseline_dependency_state(
                candidate
            ) or not r.q._baseline_dependency_state(policy_base):
                base.fail(
                    "v28 bootstrap requires unchanged canonical baseline "
                    "manifest/lock/register state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v28 bootstrap delta must be exactly nine predecessor policy/workflow "
                "files plus two v28 policy files"
            )
        base.fail("v28 bootstrap base authorizes only exact review-repair activation")

    if paths & ALL_POLICY_FILES:
        base.fail("canonical v28/v27/v26/v25 policy files are frozen after activation")

    R_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    R_BASE(candidate, policy_base)


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in r.q.p.ps(candidate):
            base.fail(f"v28 policy file missing: {path}")
        if r.q.p.bootbase(policy_base):
            if path in r.q.p.ps(policy_base):
                base.fail(f"v28 policy file unexpectedly in bootstrap base: {path}")
        elif path not in r.q.p.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v28 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        R_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, r.q.p.extset(r.q.p.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, r.q.p.extset(r.q.p.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    # validate_allowed_paths receives the complete tracked tree, not the diff.
    # Remove only v26-v28 successor policy files here, then delegate directly to
    # v25. v25 removes its own policy/product/dependency exceptions and preserves
    # DEPENDENCY_REGISTER for inherited required-path validation.
    successor_policy = frozenset(
        set(POLICY_FILES) | set(r.POLICY_FILES) | set(r.q.POLICY_FILES)
    )
    remaining = set(paths) - successor_policy
    if remaining:
        r.q.p.allowed(remaining, stage)


def files(view: Any) -> None:
    R_FILES(view)
    missing = POLICY_FILES - r.q.p.ps(view)
    if missing:
        base.fail(f"v28 policy files missing: {sorted(missing)}")
    for path in sorted(POLICY_FILES):
        if r.q.p.mode(view, path) != "100644":
            base.fail(f"v28 policy file mode invalid: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not R_PRINTER:
        base.fail("v28 predecessor printer drifted")
    _call("v27 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v28=EXACT_HEAD_REVIEW_REPAIR_ONLY")
    print(f"v28_authority={AUTH}")
    print(f"s2_implementation_authority_v28={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v28={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v28={SOURCE_ADMISSION}")


def overlay() -> None:
    shell, routing, _, desktop, execution = r.q.p.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
        (r.q.p._verify_product_files, _hardened_product_verify),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v28 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in (r, r.q, r.q.p)):
        base.fail("v28 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    prepare_r()
    r.install()
    shell, routing, _, desktop, execution = r.q.p.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v27 routing hook"), R_DELTA),
        (base.compare_base_controlled, R_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "v27 desktop hook"), R_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v27 execution hook"), R_EEXT),
        (_attr(shell, "verify_policy_files", "v27 files hook"), R_FILES),
        (_attr(shell, "print_success", "v27 printer"), R_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v28 predecessor hook drifted")

    _PRINT = R_PRINTER
    r.q.p._verify_product_files = _hardened_product_verify

    desktop_extensions = frozenset(
        set(r.q.p.extset(desktop)) | set(POLICY_FILES)
    )
    execution_extensions = frozenset(
        set(r.q.p.extset(execution)) | set(POLICY_FILES)
    )
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v28 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v28 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v28 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v28 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v28 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v28 allowed hook")
    _bind(shell, "verify_policy_files", files, "v28 files hook")
    _bind(shell, "print_success", printer, "v28 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v28_selftest import run

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
                    r.q.p.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", r.q.p.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
