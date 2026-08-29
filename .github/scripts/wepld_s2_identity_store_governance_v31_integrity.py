#!/usr/bin/env python3
"""Repair inherited self-tests for the exact admitted S2 dependency state.

Canonical v30 correctly verifies the real S2-AUTH-012 candidate as data and
projects the exact three dependency-governance files to their canonical baseline
for inherited policy verification. Foundation #834 exposed a narrower
candidate-local defect: the inherited predecessor self-test chain still reads
the real admitted Cargo.lock as if it were the frozen v25 baseline before v30's
projection seams are installed.

v31 changes policy/self-test plumbing only. Before invoking the frozen v30
predecessor self-tests, it requires either the exact canonical dependency
baseline or the exact governed admitted dependency state. It then projects the
three admitted dependency files, when present, plus the two v31 workflow
entrypoints back to their exact canonical v30 predecessor bytes solely for the
duration of predecessor self-tests.

Candidate delta verification, trusted admission, product verification, runtime
effects, source admission, dependency versions, and all S3+ authority remain
unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v30_integrity as p

P = ".github/scripts/wepld_s2_identity_store_governance_v31_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v31_selftest.py"
T_BLOB = "9367a12f224bc6aa5ca733d8920046d76adc1b0b"
V30_P_BLOB = "bfd92adbf8cf347f0f2ddf2b7678cafbccb50a46"
V30_T_BLOB = "93a10f49c86d2ce9be2228467169348b8aac057c"

V29 = p.p
V26 = p.p.s.r.q
V25 = p.p.s.r.q.p

FW = V25.FW
AW = V25.AW
CW = V25.CW

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_IDENTITY_STORE_ADMITTED_SELFTEST_PROJECTION_REPAIR_ONLY"
S2_IMPLEMENTATION_AUTHORITY = p.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = p.SOURCE_ADMISSION

P_WF = dict(p.WF)
WF = {
    FW: "27de4281b562e7e271aa5974b6b887f7504d97625e60b4dc1b0cb9874c866f2a",
    AW: "12db352e32ac5ceb99be323dc0b87e86d47bf54f56ba4007969f4b9e42904568",
    CW: p.WF[CW],
}

P_DELTA = p.delta
P_BASE = p.basectrl
P_EXT = p.ext
P_DEXT = p.dext
P_EEXT = p.eext
P_ALLOWED = p.allowed
P_FILES = p.files
P_PRINTER = p.printer
P_SHELL_COMPONENT_BASE = p.shell_component_base
P_S1_005_EVIDENCE_FREEZE = p.freeze_s1_005_evidence

root = p.root
for _path, _expected in ((p.P, V30_P_BLOB), (p.T, V30_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v31 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = p._call
_attr = p._attr
_bind = p._bind
_INST = False
_PRINT: Any = None

_V31_ENTRYPOINT = b"wepld_s2_identity_store_governance_v31_integrity.py"
_V30_ENTRYPOINT = b"wepld_s2_identity_store_governance_v30_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 1}


class _ProjectionView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v31 projected file exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(
        self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES
    ) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v30(view: Any) -> None:
    for path, expected in ((p.P, V30_P_BLOB), (p.T, V30_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v31 candidate/base is missing frozen v30 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v30 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _workflow_predecessor_projection(view: Any) -> Any:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V31_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                f"v31 workflow entrypoint count drifted before predecessor projection: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        predecessor = data.replace(_V31_ENTRYPOINT, _V30_ENTRYPOINT)
        actual = hashlib.sha256(predecessor).hexdigest()
        if actual != P_WF[path]:
            base.fail(
                f"v31 workflow does not reverse to exact canonical v30 predecessor: "
                f"{path} expected={P_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return _ProjectionView(view, replacements)


def predecessor_selftest_view(view: Any) -> Any:
    if V26.deps_ready(view):
        target = p.project_admitted_dependency_state(view)
    elif V26._baseline_dependency_state(view):
        target = view
    else:
        base.fail(
            "v31 self-test source dependency state is neither exact canonical baseline "
            "nor exact governed admitted form"
        )
    return _workflow_predecessor_projection(target)


def run_predecessor_selftests(view: Any) -> None:
    target = predecessor_selftest_view(view)
    patched: list[tuple[Any, Any]] = []
    for name, module in list(sys.modules.items()):
        if not name.startswith("wepld_") or module is None or not hasattr(module, "root"):
            continue
        patched.append((module, getattr(module, "root")))
        setattr(module, "root", target)
    try:
        p.selftest()
    finally:
        for module, original in reversed(patched):
            setattr(module, "root", original)


def prepare_p() -> None:
    current = dict(p.WF)
    if current not in (P_WF, dict(WF)):
        base.fail(f"v31 predecessor workflow identity map drifted: actual={current}")
    for module in (p, p.p, p.p.s, p.p.s.r, p.p.s.r.q, p.p.s.r.q.p):
        module.WF = dict(WF)


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths == BOOT:
            req_v30(candidate)
            req_v30(policy_base)
            if not V26._baseline_dependency_state(
                candidate
            ) or not V26._baseline_dependency_state(policy_base):
                base.fail(
                    "v31 bootstrap requires unchanged canonical baseline "
                    "manifest/lock/register state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v31 bootstrap delta must be exactly two v31 policy files "
                "plus two integrity workflows"
            )
        base.fail(
            "v31 bootstrap base authorizes only exact admitted-selftest projection repair"
        )

    if paths & ALL_POLICY_FILES:
        base.fail(
            "canonical v31/v30/v29/v28/v27/v26/v25 policy files are frozen after activation"
        )

    P_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        P_BASE(candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if (
                V25.sha(candidate_bytes) != WF[path]
                or V25.sha(base_bytes) != P_WF[path]
            ):
                base.fail(f"v31 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v31 policy file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v31 policy file unexpectedly in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v31 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        P_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES
    if remaining:
        P_ALLOWED(remaining, stage)


def files(view: Any) -> None:
    P_FILES(view)
    missing = POLICY_FILES - V25.ps(view)
    if missing:
        base.fail(f"v31 policy files missing: {sorted(missing)}")
    approved = {
        P: root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(POLICY_FILES):
        if V25.mode(view, path) != "100644":
            base.fail(f"v31 policy file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v31 policy file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not P_PRINTER:
        base.fail("v31 predecessor printer drifted")
    _call("v30 success printer", _PRINT, stage, mode_)
    print(
        "wepld_policy_successor_v31="
        "ADMITTED_DEPENDENCY_SELFTEST_PROJECTION_REPAIR_ONLY"
    )
    print(f"v31_authority={AUTH}")
    print(f"s2_implementation_authority_v31={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v31={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v31={SOURCE_ADMISSION}")
    print(
        "v31_predecessor_selftest_projection="
        "EXACT_V30_WORKFLOWS_PLUS_EXACT_THREE_DEPENDENCY_FILES"
    )


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(shell, "_verify_shell_component_base", "shell component-base hook"),
            P_SHELL_COMPONENT_BASE,
        ),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            P_S1_005_EVIDENCE_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v31 installed overlay drifted")
    if any(
        dict(module.WF) != dict(WF)
        for module in (p, p.p, p.p.s, p.p.s.r, p.p.s.r.q, p.p.s.r.q.p)
    ):
        base.fail("v31 workflow identity projection drifted")
    if V26.S2_DEPENDENCY_REGISTER_APPEND != V29.CORRECTED_S2_DEPENDENCY_REGISTER_APPEND:
        base.fail("v31 corrected dependency-register append projection drifted")


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    p.install()
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v30 routing hook"), P_DELTA),
        (base.compare_base_controlled, P_BASE),
        (
            _attr(shell, "_verify_shell_component_base", "v30 shell component-base hook"),
            P_SHELL_COMPONENT_BASE,
        ),
        (
            _attr(execution, "freeze_s1_005_evidence", "v30 S1-005 evidence-freeze hook"),
            P_S1_005_EVIDENCE_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v30 desktop hook"), P_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v30 execution hook"), P_EEXT),
        (_attr(shell, "validate_allowed_paths", "v30 allowed hook"), P_ALLOWED),
        (_attr(shell, "verify_policy_files", "v30 files hook"), P_FILES),
        (_attr(shell, "print_success", "v30 printer"), P_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v31 predecessor hook drifted")

    _PRINT = P_PRINTER
    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(POLICY_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(POLICY_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v31 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v31 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v31 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v31 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v31 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v31 allowed hook")
    _bind(shell, "verify_policy_files", files, "v31 files hook")
    _bind(shell, "print_success", printer, "v31 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v31_selftest import run

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
                    V25.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", V25.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
