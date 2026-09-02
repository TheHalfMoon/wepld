#!/usr/bin/env python3
"""Narrow v40's steady-state `delta()` resting-view window; correct no target.

v43 is an append-only successor over canonical v42. It fixes the next independently
reproduced instance of v40's over-broad `_with_v39_resting_view` mechanism and grants
no product, process, network, model, dependency, source, Doctor/CLI, or S3+ authority.

After v42 merged, PR #263's exact documentation transition still failed candidate
verification with:

    v37 documentation transition candidate bytes drifted:
    docs/canonical/CURRENT_STATE.md:
    expected=dc749635fc6b7094bc414da18c982941bbed91a6
    actual=c76985050e796ae7553d88c856c4f4e90e6bbbb6

The failure is distinct from the predecessor-selftest seam fixed by v41 and the
`files()` seam fixed by v42. v40's steady-state `delta()` still contains:

    _with_v39_resting_view(p.delta)(projected_candidate, projected_base)

That outer wrapper temporarily changes v37's live FINAL checkpoint/ledger pair back to
the superseded v39 pair for the entire predecessor delta cascade. v37's real
documentation-transition check therefore compares a valid v40-corrected candidate
against the old v39 target and fails closed.

v43 supersedes only v40's `delta` function. For one call it installs the same six
narrow resting-view wrappers already qualified by v41, neutralizes only v40's broad
outer helper reference, delegates to v40's original delta body, then restores every
binding in `finally`. All unrelated predecessor validation therefore sees the real
v40-corrected pair, while the six proven legacy consumers still see the v39 resting
pair for only their own dynamic extent.

Neither documentation target moves. NEXT_AUTHORITY_GATE remains S2-AUTH-014.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v43_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v43_selftest.py"
T_BLOB = "67bb8a9142a69399df15aaaef8b249379f6577d6"

V42_P_BLOB = "598dda532393aaf2927ea91a745169b8f90e3987"
V42_T_BLOB = "9691772fb016b8b4c21b92c4921c7e9799d44821"

_V43_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v43_integrity.py"
_V42_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v42_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v42_workflow_projection(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V43_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v43 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V43_ENTRYPOINT, _V42_ENTRYPOINT)
    return replacements


_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v42_workflow_projection(raw_root))
try:
    import wepld_s2_checkpoint_ledger_repair_governance_v42_integrity as p
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
_v37 = p._v37

if _v37.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
    base.fail("v43 inherited checkpoint target does not match v42's corrected pin")
if _v37.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
    base.fail("v43 inherited ledger target does not match v42's corrected pin")


# Fix only v40.delta. Reuse the six call sites v41 already proved need the resting pair.
_V40 = p._V40
_NARROW_RESTING_VIEW_CALL_SITES = p._NARROW_RESTING_VIEW_CALL_SITES
_ORIGINAL_NARROW_CALL_SITE_FUNCTIONS = p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS

_V40_ORIGINAL_DELTA = _V40.delta
_V40_RESTING_VIEW_ORIGINAL = _V40._with_v39_resting_view


def _corrected_v40_delta(candidate: Any, policy_base: Any) -> None:
    saved_sites = {
        (module, name): getattr(module, name)
        for module, name in _NARROW_RESTING_VIEW_CALL_SITES
    }
    for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
        setattr(module, name, _V40._with_v39_resting_view(saved_sites[(module, name)]))

    original_resting_view = _V40._with_v39_resting_view
    _V40._with_v39_resting_view = lambda func: func
    try:
        _V40_ORIGINAL_DELTA(candidate, policy_base)
    finally:
        _V40._with_v39_resting_view = original_resting_view
        for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
            setattr(module, name, saved_sites[(module, name)])


_V40.delta = _corrected_v40_delta


POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_DELTA_RESTING_VIEW_SCOPE_REPAIR_ONLY"
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

for _path, _expected in ((p.P, V42_P_BLOB), (p.T, V42_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v43 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements = _v42_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v43 workflow does not reverse to exact canonical v42 predecessor: "
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


def req_v42(view: Any) -> None:
    for path, expected in ((p.P, V42_P_BLOB), (p.T, V42_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v43 candidate/base is missing frozen v42 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v42 predecessor drifted: {path}: "
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
    original_root = p.root
    original_raw = p.raw_root
    projected = _workflow_predecessor_projection(raw_root)
    p.root = projected
    p.raw_root = projected
    try:
        p.selftest()
    finally:
        p.root = original_root
        p.raw_root = original_raw


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v43 bootstrap delta must be exactly two v43 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v43 bootstrap base authorizes only the delta resting-view scope "
                "repair activation"
            )
        req_v42(candidate)
        req_v42(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v43 policy files are frozen after activation")

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
                base.fail(f"v43 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v43 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v43 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v43 steady-state controlled file drifted: {path}")

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
            base.fail(f"v43 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v43 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v43 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    p.printer(stage, mode_)
    print("wepld_policy_successor_v43=S2_DELTA_RESTING_VIEW_SCOPE_REPAIR_ONLY")
    print(f"v43_authority={AUTH}")
    print(f"s2_implementation_authority_v43={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v43={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v43={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v43={NETWORK_AUTHORITY}")
    print(f"source_admission_v43={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v43={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (p,) + p._chain()


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v43 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"), _v35.Q_FREEZE),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v43 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v43 workflow identity projection drifted")
    if _v37.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v43 must not move the inherited checkpoint target")
    if _v37.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v43 must not move the inherited ledger target")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v43 inherited S2-AUTH-013 route decision drifted")
    if _V40.delta is not _corrected_v40_delta:
        base.fail("v43 delta resting-view scope repair is not installed")
    if _V40._with_v39_resting_view is not _V40_RESTING_VIEW_ORIGINAL:
        base.fail("v43 v40 resting-view helper is not restored outside a delta call")
    for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not _ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v43 narrow resting-view call site left wrapped outside a call: "
                f"{module.__name__}.{name}"
            )


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    p.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v42 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (_attr(execution, "freeze_s1_005_evidence", "v42 S1-005 evidence-freeze hook"), _v35.Q_FREEZE),
        (_attr(desktop, "verify_extension_controlled_paths", "v42 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v42 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v42 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v42 files hook"), p.files),
        (_attr(shell, "print_success", "v42 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v43 predecessor hook drifted")
    if _V40.delta is not _corrected_v40_delta:
        base.fail("v43 delta resting-view scope repair is not installed")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v43 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v43 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v43 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v43 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v43 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v43 allowed hook")
    _bind(shell, "verify_policy_files", files, "v43 files hook")
    _bind(shell, "print_success", printer, "v43 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_checkpoint_ledger_repair_governance_v43_selftest import run

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
