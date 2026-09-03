#!/usr/bin/env python3
"""Correct the pinned FINAL ledger identity again; widen nothing else.

Canonical v38 corrected one v37 target after finding 257-M1. Before that transition was
accepted, the independent review of PR #259 found a second material defect in the frozen
FINAL ledger blob: BL-0016 asserted an exact status timestamp its own citations could not
support, and a superseded commit status is not retained by the API, so no reader could
verify it. A self-audit of every remaining row then found the same class in BL-0019.

v39 supersedes exactly one v38 target: the FINAL ledger blob. The FINAL checkpoint target,
both PRE identities, the two-path transition shape, the ledger widening chain, the
predecessor supersessions, the inherited S2-AUTH-013 route decision, and every other
inherited guard are unchanged. The superseded v38 FINAL ledger is not accepted by v39.

One structural note, because this is the second successor spent on document content. Each
successor in this chain asserts literals about its own pins, so a later successor cannot
simply move the shared value: v38 hard-codes its own FINAL ledger identity in its self-test.
v39 therefore re-anchors rather than overwrites. It rebinds the effective consumer in v37,
and wraps the v38 checks that compare v37 against v38 so they run with v38 temporarily
reporting the corrected identity, restoring it immediately. Every check v38 performs still
runs, and every literal v38 asserts about itself still holds.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v39_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v39_selftest.py"
T_BLOB = "a4c4b43744a57f4c98aa48bf130867c1902c5b88"

V38_P_BLOB = "cd8bb3670e19c11a4f5ccbdc4ed8cfe27a9d620a"
V38_T_BLOB = "4f4862ec952f1670e8d726f5858396aed98da13f"

_V39_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v39_integrity.py"
_V38_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v38_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v38_workflow_projection(view: Any) -> dict[str, bytes]:
    """Reverse the v39 entrypoint migration back to exact canonical v38 bytes."""
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V39_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v39 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V39_ENTRYPOINT, _V38_ENTRYPOINT)
    return replacements


# v37, like v36 before it, reads the workflows at package load. Load it against the
# projected predecessor view and restore the raw view afterwards.
_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v38_workflow_projection(raw_root))
try:
    import wepld_s2_checkpoint_ledger_repair_governance_v38_integrity as p
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
V38_FINAL_LEDGER_BLOB = "ffd0d2f9264cae5d4ddf24985e5571a87f03fc04"
FINAL_LEDGER_BLOB = "cbd6f7bca4f8f33435320be2d153e59b4588f073"

if PRE_LEDGER_BLOB == FINAL_LEDGER_BLOB:
    base.fail("v39 corrected ledger target equals the PRE ledger")
if FINAL_LEDGER_BLOB == V38_FINAL_LEDGER_BLOB:
    base.fail("v39 corrected ledger target equals the superseded v38 target")
if FINAL_LEDGER_BLOB == FINAL_CHECKPOINT_BLOB:
    base.fail("v39 transition targets collapsed onto one identity")


def _bind_corrected_ledger_target() -> None:
    """Bind v38 to exactly the corrected ledger target, idempotently.

    The v39 script can be executed as ``__main__`` and then imported by its self-test
    module under its canonical module name in the same interpreter. That second import
    must not be mistaken for predecessor drift. Exactly two values are valid at this
    seam: the frozen v38 target before the first bind, or the corrected v39 target after
    an earlier bind. Any third value fails closed.

    The attribute lives on v37, not v38. v38 rebound it there and asserts its own copy as a
    literal in its self-test, so overwriting v38's copy would break a check that is still
    correct about itself. Rebinding the v37 attribute is sufficient because every consumer of
    the FINAL ledger identity - the transition check, the local documentation state assertion,
    the canonical frontier check, and the inherited ledger widening - lives in v37 and reads it
    as a module global at call time rather than capturing it.
    """
    actual = p.p.FINAL_LEDGER_BLOB
    if actual == V38_FINAL_LEDGER_BLOB:
        p.p.FINAL_LEDGER_BLOB = FINAL_LEDGER_BLOB
        return
    if actual == FINAL_LEDGER_BLOB:
        return
    base.fail(
        "v39 inherited ledger target is outside the exact old/corrected set: "
        f"old={V38_FINAL_LEDGER_BLOB} corrected={FINAL_LEDGER_BLOB} actual={actual}"
    )


# In-memory successor binding only. The frozen v38 repository bytes are unchanged and
# are verified below.
_bind_corrected_ledger_target()

# v38 compares the effective v37 identity against its own literal in three places: its overlay,
# and two of its self-test checks. Those comparisons are correct about v38 and would now fail
# only because v39 moved the shared value. They are re-anchored rather than removed: each is
# wrapped so it runs with v38 temporarily reporting the corrected identity, and the literal is
# restored immediately afterwards so every assertion v38 makes about itself still holds.
#
# `overlay` is looked up as a module global inside `install`, and the self-test functions are
# looked up as module globals inside `run`, so replacing the attributes reaches every call site.
import wepld_s2_checkpoint_ledger_repair_governance_v38_selftest as _v38_st


def _with_corrected_identity(func: Any) -> Any:
    def _wrapped(*args: Any, **kwargs: Any) -> Any:
        original = p.FINAL_LEDGER_BLOB
        p.FINAL_LEDGER_BLOB = FINAL_LEDGER_BLOB
        try:
            return func(*args, **kwargs)
        finally:
            p.FINAL_LEDGER_BLOB = original

    return _wrapped


_V38_REANCHORED = (
    (p, "overlay"),
    (_v38_st, "_check_binding_is_exact_and_idempotent"),
    (_v38_st, "_check_correction_reaches_every_consumer"),
)

_V38_ORIGINALS = {}
for _module, _name in _V38_REANCHORED:
    _original = _attr(_module, _name, f"v38 {_name}")
    _V38_ORIGINALS[_name] = _original
    setattr(_module, _name, _with_corrected_identity(_original))


POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_CANONICAL_DOCUMENTATION_LEDGER_TARGET_SECOND_CORRECTION_ONLY"
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

for _path, _expected in ((p.P, V38_P_BLOB), (p.T, V38_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v39 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    """Project to v38 bytes and prove the projection lands on the canonical predecessor."""
    replacements = _v38_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v39 workflow does not reverse to exact canonical v38 predecessor: "
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


def req_v38(view: Any) -> None:
    for path, expected in ((p.P, V38_P_BLOB), (p.T, V38_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v39 candidate/base is missing frozen v38 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v38 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def req_pre_docs(view: Any) -> None:
    for path, expected in ((CHECKPOINT, PRE_CHECKPOINT_BLOB), (LEDGER, PRE_LEDGER_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v39 requires the canonical documentation path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v39 bootstrap documentation state drifted: {path}: "
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
                    "v39 bootstrap delta must be exactly two v39 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v39 bootstrap base authorizes only corrected canonical-documentation "
                "ledger-target activation"
            )
        req_v38(candidate)
        req_v38(policy_base)
        req_pre_docs(candidate)
        req_pre_docs(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v39 policy files are frozen after activation")

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
                base.fail(f"v39 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v39 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v39 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v39 steady-state controlled file drifted: {path}")

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
            base.fail(f"v39 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v39 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v39 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    _call("v38 success printer", p.printer, stage, mode_)
    print("wepld_policy_successor_v39=S2_CANONICAL_DOCUMENTATION_LEDGER_TARGET_CORRECTION_ONLY")
    print(f"v39_authority={AUTH}")
    print(f"s2_implementation_authority_v39={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v39={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v39={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v39={NETWORK_AUTHORITY}")
    print(f"source_admission_v39={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v39={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (p, p.p, p.p.p, p.p.p.p) + tuple(p.p.p.p.PREDECESSOR_CHAIN)


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v39 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v39 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v39 workflow identity projection drifted")
    if p.p.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v39 inherited ledger target binding drifted")
    if p.FINAL_LEDGER_BLOB != V38_FINAL_LEDGER_BLOB:
        base.fail("v39 must leave the v38 self-literal intact between calls")
    if p.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v39 inherited checkpoint target drifted")
    for module, name in _V38_REANCHORED:
        if getattr(module, name) is _V38_ORIGINALS[name]:
            base.fail(f"v39 re-anchoring of v38 {name} is missing")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v39 inherited S2-AUTH-013 route decision drifted")


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    p.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v38 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v38 S1-005 evidence-freeze hook"),
            p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v38 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v38 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v38 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v38 files hook"), p.files),
        (_attr(shell, "print_success", "v38 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v39 predecessor hook drifted")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v39 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v39 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v39 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v39 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v39 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v39 allowed hook")
    _bind(shell, "verify_policy_files", files, "v39 files hook")
    _bind(shell, "print_success", printer, "v39 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_checkpoint_ledger_repair_governance_v39_selftest import run

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
