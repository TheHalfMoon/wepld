#!/usr/bin/env python3
"""Correct the pinned FINAL ledger identity; widen nothing else.

Canonical v37 authorized one exact two-document transition. Before that transition
was accepted, the independent review of PR #257 found a material defect in the frozen
FINAL ledger blob: Build Learning row BL-0017 cited comment `5485133994`, which does
not exist. A row marked QUALIFIED whose cited evidence cannot be reached is a claim
that reads as verifiable and is not, so the bytes could not be accepted.

The defect could not be patched into the blocked candidate. v37 pins the FINAL ledger
identity, so a repaired file fails the transition closed - the mechanism working, not a
fault. The authorized route is to supersede exactly one target.

v38 does not authorize a second documentation route and does not broaden v37. It
supersedes exactly one v37 target: the FINAL ledger blob. The FINAL checkpoint target,
both PRE identities, the two-path transition shape, the ledger widening chain, the three
predecessor supersessions, the inherited S2-AUTH-013 route decision, and every other
inherited guard are unchanged. The superseded v37 FINAL ledger is not accepted by v38.

The correction is content-addressed and one-shot. The corrected ledger bytes were frozen
after a bounded authoring diff containing only the repaired citation, and every commit,
blob, run and comment identifier in both documents was re-verified against the live API
rather than only the one reported. The real documentation candidate must still satisfy
both pinned FINAL blobs at the deterministic gates and receive independent review.

This file follows the same structure as v37 and inherits its import-time note: a
successor over a predecessor that reads the repository root at package load must install
a predecessor projection of the root before importing it.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v38_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v38_selftest.py"
T_BLOB = "a635f05c8d70942559d26457912902d339d332c4"

V37_P_BLOB = "68012fa0da575a194e8907cb600b49ed51720a04"
V37_T_BLOB = "7ad57d2be748cc20d1a4d7084a49ca9ca291c21e"

_V38_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v38_integrity.py"
_V37_ENTRYPOINT = b"wepld_s2_checkpoint_transition_governance_v37_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v37_workflow_projection(view: Any) -> dict[str, bytes]:
    """Reverse the v38 entrypoint migration back to exact canonical v37 bytes."""
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V38_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v38 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V38_ENTRYPOINT, _V37_ENTRYPOINT)
    return replacements


# v37, like v36 before it, reads the workflows at package load. Load it against the
# projected predecessor view and restore the raw view afterwards.
_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v37_workflow_projection(raw_root))
try:
    import wepld_s2_checkpoint_transition_governance_v37_integrity as p
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
V37_FINAL_LEDGER_BLOB = "f9b2872639a20c46db4adcde4bf2a4372f4c117e"
FINAL_LEDGER_BLOB = "ffd0d2f9264cae5d4ddf24985e5571a87f03fc04"

if PRE_LEDGER_BLOB == FINAL_LEDGER_BLOB:
    base.fail("v38 corrected ledger target equals the PRE ledger")
if FINAL_LEDGER_BLOB == V37_FINAL_LEDGER_BLOB:
    base.fail("v38 corrected ledger target equals the superseded v37 target")
if FINAL_LEDGER_BLOB == FINAL_CHECKPOINT_BLOB:
    base.fail("v38 transition targets collapsed onto one identity")


def _bind_corrected_ledger_target() -> None:
    """Bind v37 to exactly the corrected ledger target, idempotently.

    The v38 script can be executed as ``__main__`` and then imported by its self-test
    module under its canonical module name in the same interpreter. That second import
    must not be mistaken for predecessor drift. Exactly two values are valid at this
    seam: the frozen v37 target before the first bind, or the corrected v38 target after
    an earlier bind. Any third value fails closed.

    Rebinding this one attribute is sufficient because every v37 consumer of the FINAL
    ledger identity - the transition check, the local documentation state assertion, the
    canonical frontier check, and the inherited ledger widening - reads it as a module
    global at call time rather than capturing it.
    """
    actual = p.FINAL_LEDGER_BLOB
    if actual == V37_FINAL_LEDGER_BLOB:
        p.FINAL_LEDGER_BLOB = FINAL_LEDGER_BLOB
        return
    if actual == FINAL_LEDGER_BLOB:
        return
    base.fail(
        "v38 inherited v37 ledger target is outside the exact old/corrected set: "
        f"old={V37_FINAL_LEDGER_BLOB} corrected={FINAL_LEDGER_BLOB} actual={actual}"
    )


# In-memory successor binding only. The frozen v37 repository bytes are unchanged and
# are verified below.
_bind_corrected_ledger_target()

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_CANONICAL_DOCUMENTATION_LEDGER_TARGET_CORRECTION_ONLY"
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

for _path, _expected in ((p.P, V37_P_BLOB), (p.T, V37_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v38 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    """Project to v37 bytes and prove the projection lands on the canonical predecessor."""
    replacements = _v37_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v38 workflow does not reverse to exact canonical v37 predecessor: "
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


def req_v37(view: Any) -> None:
    for path, expected in ((p.P, V37_P_BLOB), (p.T, V37_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v38 candidate/base is missing frozen v37 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v37 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def req_pre_docs(view: Any) -> None:
    for path, expected in ((CHECKPOINT, PRE_CHECKPOINT_BLOB), (LEDGER, PRE_LEDGER_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v38 requires the canonical documentation path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v38 bootstrap documentation state drifted: {path}: "
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
                    "v38 bootstrap delta must be exactly two v38 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v38 bootstrap base authorizes only corrected canonical-documentation "
                "ledger-target activation"
            )
        req_v37(candidate)
        req_v37(policy_base)
        req_pre_docs(candidate)
        req_pre_docs(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v38 policy files are frozen after activation")

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
                base.fail(f"v38 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v38 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v38 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v38 steady-state controlled file drifted: {path}")

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
            base.fail(f"v38 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v38 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v38 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    _call("v37 success printer", p.printer, stage, mode_)
    print("wepld_policy_successor_v38=S2_CANONICAL_DOCUMENTATION_LEDGER_TARGET_CORRECTION_ONLY")
    print(f"v38_authority={AUTH}")
    print(f"s2_implementation_authority_v38={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v38={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v38={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v38={NETWORK_AUTHORITY}")
    print(f"source_admission_v38={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v38={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (p, p.p, p.p.p) + tuple(p.p.p.PREDECESSOR_CHAIN)


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v38 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v38 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v38 workflow identity projection drifted")
    if p.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v38 inherited v37 ledger target binding drifted")
    if p.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v38 inherited v37 checkpoint target drifted")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v38 inherited S2-AUTH-013 route decision drifted")


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    p.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v37 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v37 S1-005 evidence-freeze hook"),
            p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v37 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v37 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v37 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v37 files hook"), p.files),
        (_attr(shell, "print_success", "v37 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v38 predecessor hook drifted")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v38 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v38 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v38 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v38 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v38 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v38 allowed hook")
    _bind(shell, "verify_policy_files", files, "v38 files hook")
    _bind(shell, "print_success", printer, "v38 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_checkpoint_ledger_repair_governance_v38_selftest import run

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
