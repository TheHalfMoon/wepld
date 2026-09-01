#!/usr/bin/env python3
"""Authorize one exact canonical-documentation transition; widen nothing else.

The v34/v35 documentation route is spent. That route required the base to hold the
`PRE` blobs, so the merge that landed `FINAL` also closed it, and canonical durable
memory became unwritable. That is correct fail-closed behavior, but it means a
checkpoint update is never an edit: it is a paired policy-then-documentation unit.

v37 is that policy half. It authorizes exactly one two-document transition, from the
bytes canonical `main` actually holds today to a frozen successor pair, and nothing
else. It grants no product path, no Git or process admission, no network, no source or
dependency admission, no Doctor/CLI authority, and no S3+ authority. The S2-AUTH-013
route decision is inherited unchanged; `S2-AUTH-014` remains the next authority gate
and is untouched here.

One structural note for whoever writes v38. v36 derives its workflow identity from the
repository root at *package load*, not at verification time. A successor whose workflows
name the successor therefore breaks v36's import before any successor code can run. v37
resolves this by installing a predecessor projection of the root before importing v36
and restoring the raw view afterwards, so v36 loads against the exact v36 bytes it was
frozen against while the real tree keeps the v37 entrypoints. Any later successor over a
predecessor that reads the root at import time must do the same.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_transition_governance_v37_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_transition_governance_v37_selftest.py"
T_BLOB = "7ad57d2be748cc20d1a4d7084a49ca9ca291c21e"

V36_P_BLOB = "8980b61efac9e8e2a246d603b9e8ff6d07512b51"
V36_T_BLOB = "cd807991928c2d3a413d0ab52cee36224d9737d9"

_V37_ENTRYPOINT = b"wepld_s2_checkpoint_transition_governance_v37_integrity.py"
_V36_ENTRYPOINT = b"wepld_s2_git_route_governance_v36_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v36_workflow_projection(view: Any) -> dict[str, bytes]:
    """Reverse the v37 entrypoint migration back to exact canonical v36 bytes.

    Only the entrypoint filename may differ. The replacement lengthens rather than
    deletes, so any byte the candidate added survives into the projected bytes and
    fails the predecessor hash comparison performed by the caller.
    """
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V37_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v37 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V37_ENTRYPOINT, _V36_ENTRYPOINT)
    return replacements


# v36 reads the workflows at import time and would reject a tree whose workflows name
# v37. Load it against the projected predecessor view, then restore the raw view so no
# other importer inherits the projection by accident. v36 keeps the projected root it
# captured, which is exactly what its own predecessor projection expects.
_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v36_workflow_projection(raw_root))
try:
    import wepld_s2_git_route_governance_v36_integrity as p
finally:
    _v35.root = _ORIGINAL_V35_ROOT

V25 = p.V25
root = p.root
P_WF = dict(p.WF)

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False

CHECKPOINT = "docs/canonical/CURRENT_STATE.md"
LEDGER = "docs/learning/BUILD_LEARNING_LEDGER.md"
DOCS = frozenset({CHECKPOINT, LEDGER})

PRE_CHECKPOINT_BLOB = "28c50353718f4b836daf67df2a52f6d9471e847b"
PRE_LEDGER_BLOB = "f06e42dbd2a5e658cc1dc7c9ea7d768ceae458fb"
FINAL_CHECKPOINT_BLOB = "dc749635fc6b7094bc414da18c982941bbed91a6"
FINAL_LEDGER_BLOB = "f9b2872639a20c46db4adcde4bf2a4372f4c117e"

if PRE_CHECKPOINT_BLOB == FINAL_CHECKPOINT_BLOB:
    base.fail("v37 checkpoint transition target equals its own PRE state")
if PRE_LEDGER_BLOB == FINAL_LEDGER_BLOB:
    base.fail("v37 ledger transition target equals its own PRE state")
if PRE_CHECKPOINT_BLOB != p.p.FINAL_CHECKPOINT_BLOB:
    base.fail("v37 PRE checkpoint is not the canonical v35 FINAL checkpoint")
if PRE_LEDGER_BLOB != p.p.FINAL_LEDGER_BLOB:
    base.fail("v37 PRE ledger is not the canonical v35 FINAL ledger")

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_CANONICAL_DOCUMENTATION_TRANSITION_ONLY"
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

for _path, _expected in ((p.P, V36_P_BLOB), (p.T, V36_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v37 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    """Project to v36 bytes and prove the projection lands on the canonical predecessor.

    The pre-import projection above cannot do this, because v36's own workflow identity
    map does not exist until v36 has loaded. It is not left unverified: v36 re-derives
    the same bytes at its package load and compares them against the v35 identity it was
    frozen with, so the pre-import step is hash-checked one layer down. Every runtime
    path goes through this function, which checks it directly.
    """
    replacements = _v36_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v37 workflow does not reverse to exact canonical v36 predecessor: "
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


# The inherited S1-016 ledger pin.
#
# `state()` is reached from `files()`, which runs against every view, so the pin is
# global rather than delta-scoped. v34 already widened it once, by exactly one value,
# and bound its widening to `_V18.state`. v35 asserts that `_V18.state` is still v34's
# function and that the pin is back at its original value between calls, so v37 must not
# rebind `_V18.state` and must not leave the pin widened.
#
# v37 therefore inserts itself one layer further in: it replaces the *original* state
# function that v34 delegates to. v34's hook identity and the resting pin value are both
# left exactly as v35 expects, and each layer widens the pin only for the duration of one
# call and only for its own authorized blob. Any ledger that is none of the three known
# values still reaches the original failure.
_V34 = p.p.q
_V18 = _attr(_V34, "_V18", "inherited S1-016 evaluation")
_INHERITED_STATE = _attr(_V34, "_V18_STATE", "inherited S1-016 state evaluation")
_V18_RESTING_PIN = "b18343c12e9e5dcfebcc3694be2e50dc4c9a2405"

if _attr(_V18, "LEARNING", "S1-016 ledger path") != LEDGER:
    base.fail("v37 expected the inherited S1-016 ledger path to match")
if _attr(_V18, "FINAL_LEARNING_BLOB", "S1-016 ledger pin") != _V18_RESTING_PIN:
    base.fail("v37 expected the inherited S1-016 ledger pin at its resting value")
if _attr(_V18, "state", "S1-016 state hook") is not _attr(_V34, "_state", "v34 widening"):
    base.fail("v37 expected the inherited v34 ledger widening hook to be installed")


def _state(view: Any) -> Any:
    """Accept the authorized post-v37 ledger, and nothing else new."""
    actual = V25.blob(view.read_bytes(LEDGER, base.MAX_POLICY_FILE_BYTES))
    if actual != FINAL_LEDGER_BLOB:
        return _INHERITED_STATE(view)
    original = _V18.FINAL_LEARNING_BLOB
    _V18.FINAL_LEARNING_BLOB = FINAL_LEDGER_BLOB
    try:
        return _INHERITED_STATE(view)
    finally:
        _V18.FINAL_LEARNING_BLOB = original


# Bound at import for the reason v34 records: predecessor self-tests run before
# `install()`, and on a tree that already carries the authorized transition they evaluate
# the post-transition ledger. A widening installed later would arrive too late.
_V34._V18_STATE = _state


# Superseding the inherited local-documentation-state assertions.
#
# v34 and v35 each assert that the live tree sits on exactly one of *their* two pinned
# sides, and reject a half-applied tree. The property is right and is kept. The pins are
# not: they name the bytes of the transition that has already landed, so they can only
# ever be satisfied by one transition. The moment a second authorized transition merges,
# an unsuperseded predecessor self-test fails on the canonical `main` it just produced -
# which is the same defect v34 recorded when its first ledger design reconstructed bytes
# the post-transition tree no longer has.
#
# v37 re-anchors the assertion instead of deleting it. The replacement enforces the same
# two properties against the currently authorized pins: the tree must be on exactly one
# recognized side, and a half-applied tree is still rejected. Because v37's PRE side *is*
# the v35 FINAL side, the accepted set is exactly the two states the repository can
# legitimately hold from here. Every other inherited check in those self-tests runs
# untouched, and v37's own self-test asserts this same property independently.
#
# `_attr` is used to look the functions up so a rename upstream fails closed rather than
# silently leaving an unsuperseded check installed.
import wepld_s2_identity_store_governance_v34_selftest as _v34_st
import wepld_s2_identity_store_governance_v35_selftest as _v35_st


def _check_local_state_is_one_of_the_v37_pinned_states(view: Any = None) -> None:
    # The inherited callers pass nothing and mean the live tree. The parameter exists so
    # a re-anchored governance check can be exercised against a constructed state rather
    # than only against whichever side the repository happens to be on today.
    target = raw_root if view is None else view
    sides = []
    for path, pre, final in (
        (CHECKPOINT, PRE_CHECKPOINT_BLOB, FINAL_CHECKPOINT_BLOB),
        (LEDGER, PRE_LEDGER_BLOB, FINAL_LEDGER_BLOB),
    ):
        actual = V25.blob(target.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual == pre:
            sides.append("PRE")
        elif actual == final:
            sides.append("FINAL")
        else:
            base.fail(
                "v37 local documentation state is neither pinned side: "
                f"{path}: actual={actual}"
            )
    if len(set(sides)) != 1:
        base.fail(f"v37 local documentation state is half-applied: {sides}")


_SUPERSEDED_LOCAL_STATE_CHECKS = (
    (_v34_st, "_check_local_state_is_one_of_the_two_pinned_states", "v34"),
    (_v35_st, "_check_local_state_is_one_of_the_corrected_pinned_states", "v35"),
)

for _module, _name, _label in _SUPERSEDED_LOCAL_STATE_CHECKS:
    _attr(_module, _name, f"{_label} local documentation state check")
    setattr(_module, _name, _check_local_state_is_one_of_the_v37_pinned_states)


# v36 pins the same two documents in its canonical-frontier check, with the same
# one-transition-only limitation. Its self-test separately asserts that the pinned dict
# still names the v35 FINAL identities, so the dict is left exactly as it is and the
# check itself is re-anchored instead.
#
# Only the two documentation paths become two-sided. Every other frontier path - the
# merged S2 identity and evidence-store sources and their test - keeps its exact single
# pin, because nothing in this transition may move them.
_attr(p, "req_canonical_frontier", "v36 canonical frontier check")


def _req_canonical_frontier(view: Any) -> None:
    paths = V25.ps(view)
    sides = []
    for path, pre, final in (
        (CHECKPOINT, PRE_CHECKPOINT_BLOB, FINAL_CHECKPOINT_BLOB),
        (LEDGER, PRE_LEDGER_BLOB, FINAL_LEDGER_BLOB),
    ):
        if path not in paths:
            base.fail(f"v37 requires canonical S2 frontier path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual == pre:
            sides.append("PRE")
        elif actual == final:
            sides.append("FINAL")
        else:
            base.fail(f"v37 canonical S2 frontier drifted: {path}: actual={actual}")
    if len(set(sides)) != 1:
        base.fail(f"v37 canonical S2 frontier is half-applied: {sides}")

    for path, expected in p.REQUIRED_CANONICAL_FRONTIER_BLOBS.items():
        if path in DOCS:
            continue
        if path not in paths:
            base.fail(f"v37 requires canonical S2 frontier path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v37 canonical S2 frontier drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


p.req_canonical_frontier = _req_canonical_frontier


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v36(view: Any) -> None:
    for path, expected in ((p.P, V36_P_BLOB), (p.T, V36_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v37 candidate/base is missing frozen v36 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v36 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def req_pre_docs(view: Any) -> None:
    for path, expected in ((CHECKPOINT, PRE_CHECKPOINT_BLOB), (LEDGER, PRE_LEDGER_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v37 requires the canonical documentation path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v37 bootstrap documentation state drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def docs_transition(candidate: Any, policy_base: Any) -> None:
    """Verify the exact authorized documentation transition and nothing else."""
    expected = (
        (CHECKPOINT, PRE_CHECKPOINT_BLOB, FINAL_CHECKPOINT_BLOB),
        (LEDGER, PRE_LEDGER_BLOB, FINAL_LEDGER_BLOB),
    )
    for path, pre, final in expected:
        for view, label, wanted in (
            (policy_base, "base", pre),
            (candidate, "candidate", final),
        ):
            if path not in V25.ps(view):
                base.fail(f"v37 documentation transition {label} is missing: {path}")
            if V25.mode(view, path) != "100644":
                base.fail(f"v37 documentation transition file mode invalid: {path}")
            actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
            if actual != wanted:
                base.fail(
                    f"v37 documentation transition {label} bytes drifted: {path}: "
                    f"expected={wanted} actual={actual}"
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
    p.root = _workflow_predecessor_projection(raw_root)
    try:
        p.selftest()
    finally:
        p.root = original_root


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v37 bootstrap delta must be exactly two v37 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v37 bootstrap base authorizes only exact canonical-documentation "
                "transition activation"
            )
        req_v36(candidate)
        req_v36(policy_base)
        req_pre_docs(candidate)
        req_pre_docs(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v37 policy files are frozen after activation")

    if paths == DOCS:
        docs_transition(candidate, policy_base)
        return
    if paths & DOCS:
        base.fail(
            "v37 documentation transition must be exactly the two canonical "
            "documentation paths and nothing else"
        )

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
                base.fail(f"v37 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v37 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v37 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v37 steady-state controlled file drifted: {path}")

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
            base.fail(f"v37 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v37 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v37 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    _call("v36 success printer", p.printer, stage, mode_)
    print("wepld_policy_successor_v37=S2_CANONICAL_DOCUMENTATION_TRANSITION_ONLY")
    print(f"v37_authority={AUTH}")
    print(f"s2_implementation_authority_v37={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v37={GIT_ROUTE_DECISION}")
    print(f"git_process_admission_v37={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v37={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v37={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v37={NETWORK_AUTHORITY}")
    print(f"source_admission_v37={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v37={NEXT_AUTHORITY_GATE}")


def prepare_p() -> None:
    chain = (p, p.p) + tuple(p.p.PREDECESSOR_CHAIN)
    for module in chain:
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(
                f"v37 predecessor workflow identity map drifted: actual={current}"
            )
    for module in chain:
        module.WF = dict(WF)


def _chain() -> tuple[Any, ...]:
    return (p, p.p) + tuple(p.p.PREDECESSOR_CHAIN)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v37 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v37 workflow identity projection drifted")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v37 inherited S2-AUTH-013 route decision drifted")
    if _attr(_V34, "_V18_STATE", "inherited state hook") is not _state:
        base.fail("v37 ledger widening hook drifted")
    if _attr(_V18, "state", "S1-016 state hook") is not _attr(_V34, "_state", "v34 widening"):
        base.fail("v37 must not displace the inherited v34 ledger widening hook")
    if _V18.FINAL_LEARNING_BLOB != _V18_RESTING_PIN:
        base.fail("v37 left the inherited ledger pin widened after a call")
    for module, name, label in _SUPERSEDED_LOCAL_STATE_CHECKS:
        if getattr(module, name) is not _check_local_state_is_one_of_the_v37_pinned_states:
            base.fail(f"v37 local documentation state supersession drifted: {label}")
    if _attr(p, "req_canonical_frontier", "v36 frontier check") is not _req_canonical_frontier:
        base.fail("v37 canonical frontier supersession drifted")
    for path in sorted(DOCS):
        if p.REQUIRED_CANONICAL_FRONTIER_BLOBS.get(path) not in (
            PRE_CHECKPOINT_BLOB,
            PRE_LEDGER_BLOB,
        ):
            base.fail(f"v37 must leave the inherited v36 frontier pin intact: {path}")


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    p.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v36 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v36 S1-005 evidence-freeze hook"),
            p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v36 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v36 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v36 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v36 files hook"), p.files),
        (_attr(shell, "print_success", "v36 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v37 predecessor hook drifted")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v37 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v37 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v37 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v37 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v37 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v37 allowed hook")
    _bind(shell, "verify_policy_files", files, "v37 files hook")
    _bind(shell, "print_success", printer, "v37 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_checkpoint_transition_governance_v37_selftest import run

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
