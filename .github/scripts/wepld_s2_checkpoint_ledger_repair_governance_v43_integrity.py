#!/usr/bin/env python3
"""Narrow v40's six remaining over-broad resting-view call sites; correct no
target.

v41 (PR #264) and v42 (PR #265) each corrected one instance of the identical
code defect in v40: a call site wrapped an entire predecessor cascade in
`_with_v39_resting_view`, temporarily resetting v37's live
FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB to v39's resting (pre-v40) values for
the whole call, letting some downstream check that classifies the *real*
candidate content observe the stale pre-v40 pin instead of the real one. v41
fixed `run_predecessor_selftests`; v42 fixed `files`. Both are call sites v40
itself defines.

v40 defines **eight** such broad wraps in total:

    run_predecessor_selftests   (v41 fixed)
    files                        (v42 fixed)
    delta                        (unfixed until now)
    basectrl                     (unfixed until now)
    ext                          (unfixed until now)
    allowed                      (unfixed until now)
    printer                      (unfixed until now)
    install                      (unfixed until now)

Root cause (reproduced by direct interpreter trace against PR #263, which
carries PR #261's exact-head reviewed bytes and, after v42 merged, still
failed both `foundation-integrity` and `s1-admission-integrity` - no longer
with "S1-016 Build Learning bytes drifted", v42 genuinely closed that one,
but with a *different* message from the identical defect class in a
different call site):

    v37 documentation transition candidate bytes drifted:
    docs/canonical/CURRENT_STATE.md:
    expected=dc749635fc6b7094bc414da18c982941bbed91a6
    actual=c76985050e796ae7553d88c856c4f4e90e6bbbb6

`wepld_s2_checkpoint_transition_governance_v37_integrity.docs_transition`
reads v37's own `FINAL_CHECKPOINT_BLOB`/`FINAL_LEDGER_BLOB` module globals to
decide what an admitted candidate's documentation bytes must equal. Reached
through v40's `delta(candidate, policy_base)`, which - like `files` before
the v42 fix - wraps its entire predecessor `delta()` cascade in
`_with_v39_resting_view`, so `docs_transition` observes v39's resting
(pre-v40) checkpoint identity (`dc749635...`) instead of v40's real,
permanently-bound one (`c76985...`) for any real candidate reaching it
through an ordinary `verify-candidate-local`/`verify-remote` admission check.

`basectrl`, `ext`, and `allowed` share the identical shape and are reached by
the same real admission path (`_verify_with_policy_base`, which runs `delta`,
`basectrl`, extension checks, and `files` in sequence for an ordinary
candidate) - each one poses the identical risk for any downstream check
inside its own predecessor cascade that classifies real candidate content
against a live pin. `printer` and `install` wrap narrower predecessor calls
that v41's own docstring already reasoned do not reach the live-tree
classification chain, but this successor closes all six uniformly rather
than relying on that reasoning holding for every future predecessor change:
the whole point of this defect class is that a broad wrap is unsafe by
default, not that any particular one happens not to matter today.

The fix generalizes v41's and v42's identical technique into one reusable
wrapper, applied uniformly to all six remaining v40 attributes (`delta`,
`basectrl`, `ext`, `allowed`, `printer`, `install` - `files` is left alone,
already correctly narrowed by v42): for the dynamic extent of one call,
install the same six call sites v41 already proved necessary
(`_NARROW_RESTING_VIEW_CALL_SITES`, inherited unchanged), neutralize v40's
own `_with_v39_resting_view` reference so the wrapped function's own body
does not re-apply the broad wrap, delegate to the real predecessor logic,
and restore everything - narrow wraps and the reference alike - in a
`finally`, exception or not.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v43_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v43_selftest.py"
T_BLOB = "49d388068824ee466738dccadbbd9e131bc90ff9"

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
    """Reverse the v43 entrypoint migration back to exact canonical v42 bytes."""
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

# A plain top-level import here, not chain traversal, for the exact reason
# v42 recorded for its own `_v37` import: at three nested predecessor-
# projection levels a `.p` chain can settle to a different module object
# than Python's own import cache. This import must come after the chain
# above has already run once.
import wepld_s2_checkpoint_transition_governance_v37_integrity as _v37

V25 = p.V25
root = p.root
P_WF = dict(p.WF)

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False

# Inherited unchanged. v43 corrects a resting-view scoping defect in five more
# call sites, not a documentation identity, so every one of these stays
# exactly what v42 left it.
CHECKPOINT = p.CHECKPOINT
LEDGER = p.LEDGER
DOCS = p.DOCS
PRE_CHECKPOINT_BLOB = p.PRE_CHECKPOINT_BLOB
PRE_LEDGER_BLOB = p.PRE_LEDGER_BLOB
FINAL_CHECKPOINT_BLOB = p.FINAL_CHECKPOINT_BLOB
FINAL_LEDGER_BLOB = p.FINAL_LEDGER_BLOB

if _v37.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
    base.fail("v43 inherited checkpoint target does not match v42's corrected pin")
if _v37.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
    base.fail("v43 inherited ledger target does not match v42's corrected pin")


# ---------------------------------------------------------------------------
# The fix. Supersede v40's remaining five over-broad call sites with versions
# whose resting-view window covers only v41's already-proven six call sites,
# generalizing v41's and v42's identical technique into one reusable wrapper.
# ---------------------------------------------------------------------------

_V40 = p.p.p

_NARROW_RESTING_VIEW_CALL_SITES = p._NARROW_RESTING_VIEW_CALL_SITES
_ORIGINAL_NARROW_CALL_SITE_FUNCTIONS = p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS

_NARROWED_V40_ATTRS: tuple[str, ...] = (
    "delta",
    "basectrl",
    "ext",
    "allowed",
    "printer",
    "install",
)

_ORIGINAL_V40_ATTR_FUNCTIONS = {name: getattr(_V40, name) for name in _NARROWED_V40_ATTRS}
_with_v39_resting_view_original = _V40._with_v39_resting_view


def _narrow_wrap(original: Any) -> Any:
    """Wrap ``original`` so that, for the dynamic extent of one call, the six
    narrow call sites observe v39's resting pair (exactly as they do when
    reached through v41's `run_predecessor_selftests` or v42's `files`), v40's
    own `_with_v39_resting_view` reference is neutralized so ``original``'s
    body does not re-apply the broad wrap it would otherwise perform, and
    everything is restored - narrow wraps and the reference alike - in a
    `finally`, exception or not.
    """

    def _wrapped(*args: Any, **kwargs: Any) -> Any:
        saved_sites = {
            (module, name): getattr(module, name)
            for module, name in _NARROW_RESTING_VIEW_CALL_SITES
        }
        for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
            setattr(module, name, _V40._with_v39_resting_view(saved_sites[(module, name)]))

        original_resting_view = _V40._with_v39_resting_view
        _V40._with_v39_resting_view = lambda func: func
        try:
            return original(*args, **kwargs)
        finally:
            _V40._with_v39_resting_view = original_resting_view
            for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
                setattr(module, name, saved_sites[(module, name)])

    return _wrapped


# Bound at import, for the reason v34/v37/v39/v41/v42 each record for their
# own rebinds: an ordinary candidate's admission check reaches these five
# call sites directly (`_verify_with_policy_base` runs `delta`, `basectrl`,
# extension checks, and `files` for every candidate), so a fix installed only
# inside some later, conditionally-reached branch would still leave them on
# the broad wrap for the common case.
for _name in _NARROWED_V40_ATTRS:
    setattr(_V40, _name, _narrow_wrap(_ORIGINAL_V40_ATTR_FUNCTIONS[_name]))


POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_REMAINING_RESTING_VIEW_SCOPE_REPAIR_ONLY"
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
    """Project to v42 bytes and prove the projection lands on the canonical predecessor."""
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
                "v43 bootstrap base authorizes only the remaining resting-view "
                "scope repair activation"
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
    print("wepld_policy_successor_v43=S2_REMAINING_RESTING_VIEW_SCOPE_REPAIR_ONLY")
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
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.p.p.p.p.p.p.p.Q_FREEZE,
        ),
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
    for _name in _NARROWED_V40_ATTRS:
        if getattr(_V40, _name) is _ORIGINAL_V40_ATTR_FUNCTIONS[_name]:
            base.fail(f"v43 remaining resting-view scope repair is not installed: {_name}")
    for module, name in _NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not _ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v43 narrow resting-view call site left wrapped (or cross-restored to a "
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
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v42 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v42 S1-005 evidence-freeze hook"),
            p.p.p.p.p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v42 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v42 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v42 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v42 files hook"), p.files),
        (_attr(shell, "print_success", "v42 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v43 predecessor hook drifted")
    for _name in _NARROWED_V40_ATTRS:
        if getattr(_V40, _name) is _ORIGINAL_V40_ATTR_FUNCTIONS[_name]:
            base.fail(f"v43 remaining resting-view scope repair is not installed: {_name}")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v43 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v43 execution registration",
    )
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
