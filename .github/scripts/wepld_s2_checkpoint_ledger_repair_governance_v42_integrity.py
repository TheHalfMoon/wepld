#!/usr/bin/env python3
"""Narrow v40's own `files()` resting window; correct no target.

v42 is an append-only successor over canonical v41. It corrects a second, separate
instance of the same code defect v41 already corrected once: neither
FINAL_CHECKPOINT_BLOB nor FINAL_LEDGER_BLOB moves. Both stay exactly v40's corrected
pair, matching PR #261's exact-head reviewed bytes.

Root cause (reproduced by direct interpreter trace against a clean checkout of PR
#263, which carries those exact bytes and, after v41 merged, still failed both
`foundation-integrity` and `s1-admission-integrity` with `S1-016 Build Learning bytes
drifted`):

v41 fixed `run_predecessor_selftests` - the resting-view window that surrounds the
*selftest* cascade - but never touched `wepld_s2_checkpoint_ledger_repair_governance_
v40_integrity.files`, a completely separate call site with the identical defect:

    def files(view: Any) -> None:
        _with_v39_resting_view(p.files)(_workflow_predecessor_projection(view))
        ...

This wraps the *entire* predecessor `files()` verification cascade (`p` there is
v39, cascading through v38, v37, ..., v18) in `_with_v39_resting_view`, which
temporarily resets v37's live FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB to v39's
resting (pre-v40) values for the whole call. That cascade reaches
`wepld_s1_admission_steady_state_routing_v18_integrity.py`'s `files()` -> `state
(view)` (line ~334), which classifies the *real* candidate content via
`v34._state` -> `v37._state` -> falls through to `_INHERITED_STATE` (raw v18
`state`) -> compares against `_V18.FINAL_LEARNING_BLOB`, still poisoned to the old
value because the whole cascade sits inside the resting window. Any real candidate
whose committed bytes carry v40's genuinely-corrected identity - including PR #263,
which is exactly the paired positive this defect blocks - is misclassified and
`wepld_s1_admission_steady_state_routing_v18_integrity.state` fails closed with
"S1-016 Build Learning bytes drifted", rejecting exactly the content v40 was
written to accept.

Confirmed by direct interpreter trace (base.fail instrumented to print a full
stack): the failure frame is `wepld_s1_admission_steady_state_routing_v18_
integrity.py:242 (state) <- wepld_s2_checkpoint_transition_governance_v37_
integrity.py:201 (_state, falling through to _INHERITED_STATE) <- wepld_s2_
identity_store_governance_v34_integrity.py:162 (_state) <- wepld_s1_admission_
steady_state_routing_v18_integrity.py:334 (files, calling state(view)) <- ... <-
wepld_s2_checkpoint_ledger_repair_governance_v40_integrity.py:393 (files, the
broad `_with_v39_resting_view(p.files)(...)` call) <- wepld_s2_checkpoint_ledger_
repair_governance_v41_integrity.py:369 (files, delegating to `p.files`) <- the
`verify_policy_files` hook, reached from an ordinary `verify-candidate-local` /
`verify-remote` invocation - never from `selftest`, which is exactly why v41's
fix to `run_predecessor_selftests` did not close this gap.

An experiment ruled out the simplest possible repair (removing the resting view
from `files()` entirely, with no narrowing): with `_with_v39_resting_view`
neutralized everywhere, `wepld_s2_checkpoint_ledger_repair_governance_v38_
integrity.overlay` - one of the six call sites v41 already proved genuinely need
v37's live pins presented as v39's resting values - fails with "v38 inherited v37
ledger target binding drifted" the first time `install()` re-enters it. A blanket
removal is therefore not safe; the six-function narrow list v41 already built and
proved is the correct scope, it simply needs to cover this second call site too.

v42's fix does for `files()` exactly what v41 did for `run_predecessor_
selftests`: it replaces v40's own `files` (via `setattr`, the same append-only
technique v34 used on `_V18.state`, v37 used on `_V34._V18_STATE`, v39 used on
three v38 functions, and v41 used on v40's `run_predecessor_selftests`) with a
version that installs the same six proven-necessary narrow resting-view wraps for
the dynamic extent of one call, neutralizes v40's own outer (over-broad) resting-
view call for that same extent so it does not re-wrap the whole cascade, delegates
to v40's real `files()` logic, and restores everything - narrow wraps and v40's
`_with_v39_resting_view` reference alike - in a `finally`. Every function reached
during the cascade that is not one of the six - v18's real content classification
included - now observes v37's real, permanently-bound pins throughout, exactly as
it does outside any resting-view call. The replacement is bound at import, for the
same reason v34/v37/v39/v41 each record for their own rebinds: `install()` calls
`files()` before returning on an already-installed process, and predecessor
self-tests and `files()` alike must never observe the live-tree S1-016
classification through an over-wide resting-view window.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v42_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v42_selftest.py"
T_BLOB = "9691772fb016b8b4c21b92c4921c7e9799d44821"

V41_P_BLOB = "951e3210a90e19c8c09b708ab9dea7dbbd2f04cc"
V41_T_BLOB = "6376c146f6d4fd4f96dc8ad11741a994ada33325"

_V42_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v42_integrity.py"
_V41_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v41_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v41_workflow_projection(view: Any) -> dict[str, bytes]:
    """Reverse the v42 entrypoint migration back to exact canonical v41 bytes."""
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V42_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v42 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V42_ENTRYPOINT, _V41_ENTRYPOINT)
    return replacements


# v37, like v36 before it, reads the workflows at package load. Load the whole chain
# against the projected predecessor view and restore the raw view afterwards.
_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v41_workflow_projection(raw_root))
try:
    import wepld_s2_checkpoint_ledger_repair_governance_v41_integrity as p
finally:
    _v35.root = _ORIGINAL_V35_ROOT

# A plain top-level import here - not chain traversal (`p.p.p.p.p`) - is the
# reliable way to reference v37's live pin. At two nested predecessor-
# projection levels (v42 wrapping v41's own import of v40, which itself wraps
# its import of v39, ...), each layer's `.p` attribute can settle to a
# *different* v37 module object than the one this import (and Python's own
# import cache) resolves to - reproduced directly: `p.p.p.p.p is
# sys.modules["wepld_s2_checkpoint_transition_governance_v37_integrity"]` is
# `False` immediately after import, even though both compare equal in value
# at that instant, and the *actual* production call path (`files()`
# dispatched through the real predecessor chain, exercised by
# `_check_files_cascade_accepts_real_tree_and_rejects_drifted_ledger` in the
# self-test) is unaffected by this. This import must come after the chain
# above has already run once (populating `sys.modules` with a fully
# initialized v37) - importing v37 any earlier reruns its own workflow-
# projection self-check against the *unprojected* live workflow files, which
# still reference v42's entrypoint rather than v37's expected v36-era one,
# and fails closed.
import wepld_s2_checkpoint_transition_governance_v37_integrity as _v37

V25 = p.V25
root = p.root
P_WF = dict(p.WF)

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False

# Inherited unchanged. v42 corrects a second files()-verification scoping defect,
# not a documentation identity, so every one of these stays exactly what v41 left it.
CHECKPOINT = p.CHECKPOINT
LEDGER = p.LEDGER
DOCS = p.DOCS
PRE_CHECKPOINT_BLOB = p.PRE_CHECKPOINT_BLOB
PRE_LEDGER_BLOB = p.PRE_LEDGER_BLOB
FINAL_CHECKPOINT_BLOB = p.FINAL_CHECKPOINT_BLOB
FINAL_LEDGER_BLOB = p.FINAL_LEDGER_BLOB

if _v37.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
    base.fail("v42 inherited checkpoint target does not match v41's corrected pin")
if _v37.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
    base.fail("v42 inherited ledger target does not match v41's corrected pin")


# ---------------------------------------------------------------------------
# The fix. Supersede v40's own `files` with a version whose resting-view window
# covers only v41's already-proven six call sites, instead of the entire
# predecessor `files()` cascade.
# ---------------------------------------------------------------------------

_V40 = p.p

_NARROW_RESTING_VIEW_CALL_SITES = p._NARROW_RESTING_VIEW_CALL_SITES
_ORIGINAL_NARROW_CALL_SITE_FUNCTIONS = p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS

_V40_ORIGINAL_FILES = _V40.files
_with_v39_resting_view_original = _V40._with_v39_resting_view


def _corrected_v40_files(view: Any) -> None:
    """Supersedes ``wepld_s2_checkpoint_ledger_repair_governance_v40_integrity
    .files``.

    The original wraps the *entire* predecessor `files()` verification cascade
    (``p.files()``, where ``p`` there is v39) in v40's own `_with_v39_resting_view`.
    This version instead installs v41's already-proven six narrow call-site wraps
    for the dynamic extent of one call, neutralizes v40's own outer resting-view
    reference for that same extent (so v40's real `files()` body does not re-apply
    the broad wrap it would otherwise perform), and runs v40's real `files()` logic
    with every other function - v18's live-tree S1-016 classification included -
    observing v37's real, permanently-bound pins throughout.
    """
    saved_sites = {
        (module, name): getattr(module, name)
        for module, name in _NARROW_RESTING_VIEW_CALL_SITES
    }
    for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
        setattr(module, name, _V40._with_v39_resting_view(saved_sites[(module, name)]))

    original_resting_view = _V40._with_v39_resting_view
    _V40._with_v39_resting_view = lambda func: func
    try:
        _V40_ORIGINAL_FILES(view)
    finally:
        _V40._with_v39_resting_view = original_resting_view
        for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
            setattr(module, name, saved_sites[(module, name)])


# Bound at import, for the reason v34/v37/v39/v41 each record for their own
# rebinds: `install()` calls `files()` before returning on an already-installed
# process (the `overlay()` idempotency path), and an ordinary `verify-candidate-
# local`/`verify-remote` invocation reaches `files()` directly - a fix installed
# only inside `install()`'s first-time branch would still leave this call site on
# the broad wrap.
_V40.files = _corrected_v40_files


POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_FILES_RESTING_VIEW_SCOPE_REPAIR_ONLY"
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

for _path, _expected in ((p.P, V41_P_BLOB), (p.T, V41_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v42 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    """Project to v41 bytes and prove the projection lands on the canonical predecessor."""
    replacements = _v41_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v42 workflow does not reverse to exact canonical v41 predecessor: "
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


def req_v41(view: Any) -> None:
    for path, expected in ((p.P, V41_P_BLOB), (p.T, V41_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v42 candidate/base is missing frozen v41 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v41 predecessor drifted: {path}: "
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
                    "v42 bootstrap delta must be exactly two v42 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v42 bootstrap base authorizes only the files resting-view scope "
                "repair activation"
            )
        req_v41(candidate)
        req_v41(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v42 policy files are frozen after activation")

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
                base.fail(f"v42 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v42 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v42 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v42 steady-state controlled file drifted: {path}")

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
            base.fail(f"v42 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v42 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v42 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    p.printer(stage, mode_)
    print("wepld_policy_successor_v42=S2_FILES_RESTING_VIEW_SCOPE_REPAIR_ONLY")
    print(f"v42_authority={AUTH}")
    print(f"s2_implementation_authority_v42={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v42={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v42={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v42={NETWORK_AUTHORITY}")
    print(f"source_admission_v42={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v42={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (p,) + p._chain()


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v42 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            _v35.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v42 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v42 workflow identity projection drifted")
    if _v37.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v42 must not move the inherited checkpoint target")
    if _v37.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v42 must not move the inherited ledger target")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v42 inherited S2-AUTH-013 route decision drifted")
    if _V40.files is not _corrected_v40_files:
        base.fail("v42 files resting-view scope repair is not installed")
    for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not _ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v42 narrow resting-view call site left wrapped (or cross-restored to a "
                f"different original) outside a call: {module.__name__}.{name}"
            )


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    p.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v41 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v41 S1-005 evidence-freeze hook"),
            _v35.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v41 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v41 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v41 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v41 files hook"), p.files),
        (_attr(shell, "print_success", "v41 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v42 predecessor hook drifted")
    if _V40.files is not _corrected_v40_files:
        base.fail("v42 files resting-view scope repair is not installed")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v42 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v42 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v42 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v42 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v42 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v42 allowed hook")
    _bind(shell, "verify_policy_files", files, "v42 files hook")
    _bind(shell, "print_success", printer, "v42 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_checkpoint_ledger_repair_governance_v42_selftest import run

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
