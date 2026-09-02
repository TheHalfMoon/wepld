#!/usr/bin/env python3
"""Narrow v40's predecessor-selftest resting window; correct no target.

v41 is an append-only successor over canonical v40. It corrects a code defect in
v40's own machinery, not a documentation-target identity: neither FINAL_CHECKPOINT_BLOB
nor FINAL_LEDGER_BLOB moves. Both stay exactly v40's corrected pair, matching PR #261's
exact-head reviewed bytes.

Root cause (reproduced by direct trace against a clean checkout of PR #263, which
carries those exact bytes and, before this fix, failed both `foundation-integrity` and
`s1-admission-integrity` with `S1-016 Build Learning bytes drifted`):

v40's `run_predecessor_selftests` calls
`_with_v39_resting_view(p.selftest)()` - it resets v37's live FINAL_CHECKPOINT_BLOB and
FINAL_LEDGER_BLOB to v39's resting (pre-v40) values for the *entire* dynamic extent of
one call, and that one call is v39's own `selftest()`, which fans out through v38, v37,
v36, v35, v34, ..., v25, ..., v21, all the way down to v20's own predecessor self-test.
v20's `_fresh_local_view_projection_regression` opens with a live-tree classification -
`getattr(v18, "state", None)(root)` against the *real* repository tree, not a synthetic
per-layer fixture. `v18.state` was permanently rebound (at v34 import) to a widening
chain: v34's own `_state` falls through to v37's own `_state` (rebound in by v37 at
import), which reads v37's live FINAL_LEDGER_BLOB directly. While v20's regression runs
inside v40's resting window, that read observes the *old*, pre-v40 pin instead of the
real one - so a real candidate whose committed bytes carry v40's genuinely-corrected
identity is misclassified as neither the PRE state nor any recognized FINAL state, and
`wepld_s1_admission_steady_state_routing_v18_integrity.state` fails closed with
"S1-016 Build Learning bytes drifted", rejecting exactly the content v40 was written to
accept. Confirmed by direct interpreter trace: the failure frame is
`v20._fresh_local_view_projection_regression -> v34._state -> v37._state ->
(raw) v18.state -> base.fail`, reached from `v40.run_predecessor_selftests ->
_with_v39_resting_view(p.selftest) -> ... -> v21.selftest -> v20.selftest`.

v40's own docstring already explains *why* the resting view exists: a small, exact set
of v38/v39 functions compare v37's live pins against their own frozen literal
expectation, and those calls need to observe v39's resting values for their own dynamic
extent. v40 chose to satisfy that need at two broad entry seams (`run_predecessor_
selftests` and predecessor `install()`) instead of setattr-wrapping each call site,
explicitly to avoid "duplicat[ing] setattr-based replacement five times over." That
trade was too broad: `run_predecessor_selftests` reaches far more than those five
call sites, including v20's unrelated live-tree check. `install()` does not have this
defect - it never reaches the predecessor self-test cascade - so it is untouched here.

v41's fix does what v40's docstring considered and declined: it replaces v40's own
`run_predecessor_selftests` (via `setattr`, the same append-only technique v34 used on
`_V18.state`, v37 used on `_V34._V18_STATE`, and v39 used on three v38 functions) with a
version whose resting-view window covers only the six functions actually proven (by
direct experiment against both a clean `main` checkout and the PR #263 tree) to need
it: v38's `overlay`, v38's `_check_correction_is_exactly_one_target`, v38's
`_check_binding_is_exact_and_idempotent`, v38's `_check_correction_reaches_every_
consumer`, v39's own `overlay`, and v39's `_check_the_effective_consumer_moved_and_
the_literal_did_not`. Every other function reached during the cascade - v20's live-tree
S1-016 classification included - now observes v37's real, permanently-bound pins
throughout, exactly as it does outside any predecessor self-test call. The replacement
is bound at import, for the same reason v34/v37/v39 record theirs at import: predecessor
self-tests run before `install()`, and a fix installed only in `install()` would arrive
after they had already failed.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v41_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v41_selftest.py"
T_BLOB = "2dc035ccf3cb5c4f1c648ed0a5d53c2d0484ea81"

V40_P_BLOB = "19c98eb05fbebfc41f7c793ee269a89b1db95880"
V40_T_BLOB = "9f6ca73a3e03a7704cf8608224750d37355a32d2"

_V41_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v41_integrity.py"
_V40_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v40_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v40_workflow_projection(view: Any) -> dict[str, bytes]:
    """Reverse the v41 entrypoint migration back to exact canonical v40 bytes."""
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V41_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v41 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V41_ENTRYPOINT, _V40_ENTRYPOINT)
    return replacements


# v37, like v36 before it, reads the workflows at package load. Load the whole chain
# against the projected predecessor view and restore the raw view afterwards.
_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v40_workflow_projection(raw_root))
try:
    import wepld_s2_checkpoint_ledger_repair_governance_v40_integrity as p
finally:
    _v35.root = _ORIGINAL_V35_ROOT

import wepld_s2_checkpoint_ledger_repair_governance_v38_selftest as _v38_st
import wepld_s2_checkpoint_ledger_repair_governance_v39_selftest as _v39_st

V25 = p.V25
root = p.root
P_WF = dict(p.WF)

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False

# Inherited unchanged. v41 corrects a self-test scoping defect, not a documentation
# identity, so every one of these stays exactly what v40 left it.
CHECKPOINT = p.CHECKPOINT
LEDGER = p.LEDGER
DOCS = p.DOCS
PRE_CHECKPOINT_BLOB = p.PRE_CHECKPOINT_BLOB
PRE_LEDGER_BLOB = p.PRE_LEDGER_BLOB
FINAL_CHECKPOINT_BLOB = p.FINAL_CHECKPOINT_BLOB
FINAL_LEDGER_BLOB = p.FINAL_LEDGER_BLOB

if p.p.p.p.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
    base.fail("v41 inherited checkpoint target does not match v40's corrected pin")
if p.p.p.p.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
    base.fail("v41 inherited ledger target does not match v40's corrected pin")


# ---------------------------------------------------------------------------
# The fix. Supersede v40's own `run_predecessor_selftests` with a version whose
# resting-view window covers only the exact call sites that need it.
# ---------------------------------------------------------------------------

_V38 = p.p.p
_V39 = p.p

_NARROW_RESTING_VIEW_CALL_SITES: tuple[tuple[Any, str], ...] = (
    (_V38, "overlay"),
    (_v38_st, "_check_correction_is_exactly_one_target"),
    (_v38_st, "_check_binding_is_exact_and_idempotent"),
    (_v38_st, "_check_correction_reaches_every_consumer"),
    (_V39, "overlay"),
    (_v39_st, "_check_the_effective_consumer_moved_and_the_literal_did_not"),
)

# Captured once, before any wrapping, so `overlay()` can prove the six call sites are
# never left wrapped outside the dynamic extent of one `run_predecessor_selftests` call.
_ORIGINAL_NARROW_CALL_SITE_FUNCTIONS = {
    (module, name): getattr(module, name) for module, name in _NARROW_RESTING_VIEW_CALL_SITES
}


def _corrected_run_predecessor_selftests() -> None:
    """Supersedes ``wepld_s2_checkpoint_ledger_repair_governance_v40_integrity
    .run_predecessor_selftests``.

    The original wrapped the *entire* predecessor self-test cascade
    (``p.selftest()``, where ``p`` there is v39) in ``_with_v39_resting_view``. This
    version instead wraps only the six functions proven to need v37's live pins
    presented as v39's resting values for their own call, and runs the cascade with
    every other function - v20's live-tree S1-016 classification included -
    observing v37's real, permanently-bound pins throughout.
    """
    saved = {(module, name): getattr(module, name) for module, name in _NARROW_RESTING_VIEW_CALL_SITES}
    for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
        setattr(module, name, p._with_v39_resting_view(saved[(module, name)]))

    original_root = _V39.root
    original_raw = _V39.raw_root
    projected = p._workflow_predecessor_projection(p.raw_root)
    _V39.root = projected
    _V39.raw_root = projected
    try:
        _V39.selftest()
    finally:
        _V39.root = original_root
        _V39.raw_root = original_raw
        for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
            setattr(module, name, saved[(module, name)])


# Bound at import, for the reason v34/v37/v39 each record for their own rebinds:
# predecessor self-tests run before `install()`, and on a tree that already carries
# v40's genuinely corrected bytes they must not observe the live-tree S1-016
# classification through an over-wide resting-view window. A fix installed later,
# only inside `install()`, would arrive after they had already failed.
_V40_ORIGINAL_RUN_PREDECESSOR_SELFTESTS = p.run_predecessor_selftests
p.run_predecessor_selftests = _corrected_run_predecessor_selftests


POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_PREDECESSOR_SELFTEST_RESTING_VIEW_SCOPE_REPAIR_ONLY"
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

for _path, _expected in ((p.P, V40_P_BLOB), (p.T, V40_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v41 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    """Project to v40 bytes and prove the projection lands on the canonical predecessor."""
    replacements = _v40_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v41 workflow does not reverse to exact canonical v40 predecessor: "
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


def req_v40(view: Any) -> None:
    for path, expected in ((p.P, V40_P_BLOB), (p.T, V40_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v41 candidate/base is missing frozen v40 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v40 predecessor drifted: {path}: "
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
                    "v41 bootstrap delta must be exactly two v41 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v41 bootstrap base authorizes only the predecessor-selftest "
                "resting-view scope repair activation"
            )
        req_v40(candidate)
        req_v40(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v41 policy files are frozen after activation")

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
                base.fail(f"v41 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v41 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v41 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v41 steady-state controlled file drifted: {path}")

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
            base.fail(f"v41 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v41 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v41 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    _call("v40 success printer", p.printer, stage, mode_)
    print("wepld_policy_successor_v41=S2_PREDECESSOR_SELFTEST_RESTING_VIEW_SCOPE_REPAIR_ONLY")
    print(f"v41_authority={AUTH}")
    print(f"s2_implementation_authority_v41={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v41={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v41={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v41={NETWORK_AUTHORITY}")
    print(f"source_admission_v41={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v41={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (p,) + p._chain()


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v41 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.p.p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v41 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v41 workflow identity projection drifted")
    if p.p.p.p.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v41 must not move the inherited checkpoint target")
    if p.p.p.p.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v41 must not move the inherited ledger target")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v41 inherited S2-AUTH-013 route decision drifted")
    if p.run_predecessor_selftests is not _corrected_run_predecessor_selftests:
        base.fail("v41 predecessor-selftest resting-view scope repair is not installed")
    for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) not in _ORIGINAL_NARROW_CALL_SITE_FUNCTIONS.values():
            base.fail(
                "v41 narrow resting-view call site left wrapped outside a call: "
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
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v40 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v40 S1-005 evidence-freeze hook"),
            p.p.p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v40 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v40 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v40 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v40 files hook"), p.files),
        (_attr(shell, "print_success", "v40 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v41 predecessor hook drifted")
    if p.run_predecessor_selftests is not _corrected_run_predecessor_selftests:
        base.fail("v41 predecessor-selftest resting-view scope repair is not installed")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v41 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v41 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v41 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v41 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v41 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v41 allowed hook")
    _bind(shell, "verify_policy_files", files, "v41 files hook")
    _bind(shell, "print_success", printer, "v41 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_checkpoint_ledger_repair_governance_v41_selftest import run

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
