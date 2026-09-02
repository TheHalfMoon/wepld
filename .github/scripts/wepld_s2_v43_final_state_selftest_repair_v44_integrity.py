#!/usr/bin/env python3
"""Repair v43's documentation-transition self-test fixture without moving authority.

v43's production admission repair is correct, but one v43 self-test still assumes
that the checkout running the test carries the PRE documentation bytes. That is true
on canonical main before the authorized documentation transition, but false on the
PR that carries the exact FINAL bytes the policy is supposed to admit. The result is
a self-test failure before candidate admission runs:

    v43 docs_transition must accept a candidate whose checkpoint/ledger bytes
    genuinely match the live FINAL identity: v37 documentation transition base
    bytes drifted ... expected=<PRE> actual=<FINAL>

v44 changes no documentation identity, product path, route decision, dependency,
source admission, process/network/model authority, Doctor/CLI authority, or future
slice authority. It supersedes only that test fixture for the dynamic extent of the
v43 predecessor self-test run. The repaired oracle synthesizes both PRE and FINAL
sides and temporarily binds v37's four transition pins to those synthetic identities,
so the test proves candidate-side drift rejection and valid FINAL acceptance without
depending on whether the live checkout itself is PRE or FINAL.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_v43_final_state_selftest_repair_v44_integrity.py"
T = ".github/scripts/wepld_s2_v43_final_state_selftest_repair_v44_selftest.py"
T_BLOB = "6c85726b8f9719c7cfb842e90556097bc03e1f2d"

V43_P_BLOB = "7be3076b0f6522e3ec1fb064b04ba497eb70a284"
V43_T_BLOB = "49d388068824ee466738dccadbbd9e131bc90ff9"

_V44_ENTRYPOINT = b"wepld_s2_v43_final_state_selftest_repair_v44_integrity.py"
_V43_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v43_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v43_workflow_projection(view: Any) -> dict[str, bytes]:
    """Reverse the v44 entrypoint migration back to exact canonical v43 bytes."""
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V44_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v44 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V44_ENTRYPOINT, _V43_ENTRYPOINT)
    return replacements


_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v43_workflow_projection(raw_root))
try:
    import wepld_s2_checkpoint_ledger_repair_governance_v43_integrity as p
finally:
    _v35.root = _ORIGINAL_V35_ROOT

V25 = p.V25
root = p.root
P_WF = dict(p.WF)

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False

CHECKPOINT = p.CHECKPOINT
LEDGER = p.LEDGER
DOCS = p.DOCS
PRE_CHECKPOINT_BLOB = p.PRE_CHECKPOINT_BLOB
PRE_LEDGER_BLOB = p.PRE_LEDGER_BLOB
FINAL_CHECKPOINT_BLOB = p.FINAL_CHECKPOINT_BLOB
FINAL_LEDGER_BLOB = p.FINAL_LEDGER_BLOB

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_V43_FINAL_STATE_SELFTEST_FIXTURE_REPAIR_ONLY"
S2_IMPLEMENTATION_AUTHORITY = p.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = p.SOURCE_ADMISSION
GIT_ROUTE_DECISION = p.GIT_ROUTE_DECISION
GIT_PROCESS_ADMISSION = "NONE"
EXTERNAL_PROCESS_AUTHORITY = "NONE"
GIT_EXECUTION_AUTHORITY = "NONE"
NETWORK_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
DOCTOR_CLI_AUTHORITY = "NONE"
S3_PLUS_AUTHORITY = "NONE"
NEXT_AUTHORITY_GATE = "S2-AUTH-014"

for _path, _expected in ((p.P, V43_P_BLOB), (p.T, V43_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v44 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


class _OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v44 overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return self._view.entries()

    def tree_identity(self, path: str) -> Any:
        return self._view.tree_identity(path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _corrected_v43_docs_transition_selftest() -> None:
    """Exercise v37 transition semantics without assuming the live checkout is PRE."""
    v37 = p._v37

    pre_checkpoint = b"# v44 synthetic PRE checkpoint\n"
    pre_ledger = b"# v44 synthetic PRE ledger\n"
    final_checkpoint = b"# v44 synthetic FINAL checkpoint\n"
    final_ledger = b"# v44 synthetic FINAL ledger\n"
    drifted_checkpoint = b"# v44 synthetic DRIFTED checkpoint\n"

    identities = {
        V25.blob(pre_checkpoint),
        V25.blob(pre_ledger),
        V25.blob(final_checkpoint),
        V25.blob(final_ledger),
        V25.blob(drifted_checkpoint),
    }
    if len(identities) != 5:
        base.fail("v44 synthetic documentation identities collided")

    base_view = _OverlayView(
        raw_root,
        {CHECKPOINT: pre_checkpoint, LEDGER: pre_ledger},
    )
    final_view = _OverlayView(
        raw_root,
        {CHECKPOINT: final_checkpoint, LEDGER: final_ledger},
    )
    drifted_view = _OverlayView(
        raw_root,
        {CHECKPOINT: drifted_checkpoint, LEDGER: final_ledger},
    )

    saved = (
        v37.PRE_CHECKPOINT_BLOB,
        v37.PRE_LEDGER_BLOB,
        v37.FINAL_CHECKPOINT_BLOB,
        v37.FINAL_LEDGER_BLOB,
    )
    try:
        v37.PRE_CHECKPOINT_BLOB = V25.blob(pre_checkpoint)
        v37.PRE_LEDGER_BLOB = V25.blob(pre_ledger)
        v37.FINAL_CHECKPOINT_BLOB = V25.blob(final_checkpoint)
        v37.FINAL_LEDGER_BLOB = V25.blob(final_ledger)

        try:
            v37.docs_transition(drifted_view, base_view)
        except base.PolicyError as exc:
            if "documentation transition candidate bytes drifted" not in str(exc):
                base.fail(
                    "v44 drift oracle rejected for the wrong cause: "
                    f"{exc}"
                )
        else:
            base.fail("v44 drift oracle accepted an unrecognized candidate checkpoint")

        try:
            v37.docs_transition(final_view, base_view)
        except base.PolicyError as exc:
            base.fail(
                "v44 state-independent transition fixture must accept its exact FINAL side: "
                f"{exc}"
            )
    finally:
        (
            v37.PRE_CHECKPOINT_BLOB,
            v37.PRE_LEDGER_BLOB,
            v37.FINAL_CHECKPOINT_BLOB,
            v37.FINAL_LEDGER_BLOB,
        ) = saved


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements = _v43_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v44 workflow does not reverse to exact canonical v43 predecessor: "
                f"{path} expected={P_WF[path]} actual={actual}"
            )
    return replacements


def _derive_candidate_workflow_hash(path: str) -> str:
    data = raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    _workflow_replacements(raw_root)
    return V25.sha(data)


WF = {
    FW: _derive_candidate_workflow_hash(FW),
    AW: _derive_candidate_workflow_hash(AW),
    CW: p.WF[CW],
}


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v43(view: Any) -> None:
    for path, expected in ((p.P, V43_P_BLOB), (p.T, V43_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v44 candidate/base is missing frozen v43 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v43 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _workflow_predecessor_projection(view: Any) -> Any:
    return _v35._ProjectionView(view, _workflow_replacements(view))


def _predecessor_view(view: Any, policy_base: Any) -> tuple[Any, Any]:
    candidate = _workflow_predecessor_projection(view)
    if bootbase(policy_base):
        return candidate, policy_base
    return candidate, _workflow_predecessor_projection(policy_base)


def run_predecessor_selftests() -> None:
    """Run the exact v43 suite with only its state-dependent fixture superseded."""
    import wepld_s2_checkpoint_ledger_repair_governance_v43_selftest as v43_st

    original_fixture = v43_st._check_docs_transition_rejects_drifted_checkpoint
    original_root = p.root
    original_raw = p.raw_root
    projected = _workflow_predecessor_projection(raw_root)

    v43_st._check_docs_transition_rejects_drifted_checkpoint = (
        _corrected_v43_docs_transition_selftest
    )
    p.root = projected
    p.raw_root = projected
    try:
        p.selftest()
    finally:
        p.root = original_root
        p.raw_root = original_raw
        v43_st._check_docs_transition_rejects_drifted_checkpoint = original_fixture


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v44 bootstrap delta must be exactly two v44 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v44 bootstrap base authorizes only the v43 FINAL-state self-test "
                "fixture repair activation"
            )
        req_v43(candidate)
        req_v43(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v44 policy files are frozen after activation")

    projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
    p.delta(projected_candidate, projected_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
        p.basectrl(projected_candidate, projected_base)
        return

    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != P_WF[path]:
                base.fail(f"v44 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v44 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v44 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v44 steady-state controlled file drifted: {path}")

    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
        p.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        p.allowed(remaining, stage)


def files(view: Any) -> None:
    p.files(_workflow_predecessor_projection(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v44 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v44 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v44 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    p.printer(stage, mode_)
    print("wepld_policy_successor_v44=V43_FINAL_STATE_SELFTEST_FIXTURE_REPAIR_ONLY")
    print(f"v44_authority={AUTH}")
    print(f"s2_implementation_authority_v44={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v44={GIT_ROUTE_DECISION}")
    print(f"git_process_admission_v44={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v44={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v44={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v44={NETWORK_AUTHORITY}")
    print(f"source_admission_v44={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v44={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (p,) + p._chain()


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v44 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.p.p.p.p.p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v44 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v44 workflow identity projection drifted")
    if p.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v44 must not move the inherited checkpoint target")
    if p.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v44 must not move the inherited ledger target")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v44 inherited S2-AUTH-013 route decision drifted")


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    p.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v43 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v43 S1-005 evidence-freeze hook"),
            p.p.p.p.p.p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v43 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v43 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v43 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v43 files hook"), p.files),
        (_attr(shell, "print_success", "v43 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v44 predecessor hook drifted")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v44 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v44 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v44 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v44 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v44 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v44 allowed hook")
    _bind(shell, "verify_policy_files", files, "v44 files hook")
    _bind(shell, "print_success", printer, "v44 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_v43_final_state_selftest_repair_v44_selftest import run

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
