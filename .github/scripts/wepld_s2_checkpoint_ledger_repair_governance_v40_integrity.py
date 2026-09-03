#!/usr/bin/env python3
"""Correct both pinned FINAL documentation identities; widen nothing else.

Canonical v39 corrected the FINAL ledger blob a second time. Before that corrected
transition could be accepted, five rounds of independent review and self-audit on PR
#261 (`261-M1` .. `261-M5`) repaired further evidence-integrity defects in the ledger
content itself, and one of those repairs (`261-M3`) also corrected prose in the
checkpoint document. Both documents moved past the v39 pin as a result. v39 pins the
FINAL checkpoint identity as well as the FINAL ledger identity, so the twice-repaired
candidate fails the transition closed - the mechanism working, not a fault. The
authorized route is again to supersede the frozen target(s), this time both of them.

v40 does not authorize a second documentation route and does not broaden v39. It
supersedes exactly two v39 targets: the FINAL checkpoint blob and the FINAL ledger
blob. Both PRE identities, the two-path transition shape, the ledger widening chain,
the four predecessor supersessions (v34 through v39), the inherited S2-AUTH-013 route
decision, and every other inherited guard are unchanged. Neither superseded v39 FINAL
identity is accepted by v40.

The checkpoint identity has never moved before: v37 minted it, and v38/v39 each left it
untouched because only the ledger needed correction at the time. v40 is the first
successor to correct it, so the re-anchoring this file performs is deliberately more
general than v39's: v39 only had to reconcile a single moving identity (the ledger)
against the checks that assume it is fixed; v40 reconciles two, one of which (the
checkpoint) had never been treated as movable by any predecessor's self-test before now.

Structural note inherited from v37/v38/v39: v37 reads its own predecessor's workflow
identity at package load, and every successor since projects the tree to the exact
predecessor entrypoint before importing it, restoring the raw view afterward.

Re-anchoring strategy. v39 re-anchored three specific v38 functions by permanently
replacing them (via `setattr`) with wrapped versions, because those functions compare
v37's live FINAL_LEDGER_BLOB against v38's own frozen self-literal. v40 needs the same
treatment, but the set of affected functions is now v38's `overlay`, two v38 self-test
checks, v39's own `overlay`, and one v39 self-test check - five call sites across four
modules, several of which reference v37's live checkpoint identity as well as the
ledger. Rather than duplicate `setattr`-based replacement five times over (a mechanism
that must then itself be proven installed, delegating, and restoring, five times over),
v40 establishes the equivalent property at its two actual entry seams instead: every
one of those five functions is reached only through `wepld_s2_checkpoint_ledger_repair
_governance_v39_integrity`'s own `selftest()` or `install()`, both of which v40 already
calls exactly once each (`run_predecessor_selftests` and the predecessor `install()`
call inside `install`). Wrapping those two call sites so that, for their exact dynamic
extent, v37's live FINAL_CHECKPOINT_BLOB and FINAL_LEDGER_BLOB read as the values v39
was frozen expecting - and restoring the real v40-corrected values immediately
afterward, exception or not - reaches every nested v38/v39 consumer without touching
their code, and is proven directly: the self-test calls the wrapper itself and asserts
what it presents, that it delegates, and that it restores under both normal return and
raised exception, then separately asserts that the permanent binding is exactly v40's
corrected pair everywhere outside that narrow window.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v40_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v40_selftest.py"
T_BLOB = "9f6ca73a3e03a7704cf8608224750d37355a32d2"

V39_P_BLOB = "f789b29431c58669449b3119cfe5dc9ffe6f8741"
V39_T_BLOB = "a4c4b43744a57f4c98aa48bf130867c1902c5b88"

_V40_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v40_integrity.py"
_V39_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v39_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root


def _v39_workflow_projection(view: Any) -> dict[str, bytes]:
    """Reverse the v40 entrypoint migration back to exact canonical v39 bytes."""
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V40_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v40 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V40_ENTRYPOINT, _V39_ENTRYPOINT)
    return replacements


# v37, like v36 before it, reads the workflows at package load. Load the whole chain
# against the projected predecessor view and restore the raw view afterwards.
_ORIGINAL_V35_ROOT = _v35.root
_v35.root = _v35._ProjectionView(raw_root, _v39_workflow_projection(raw_root))
try:
    import wepld_s2_checkpoint_ledger_repair_governance_v39_integrity as p
finally:
    _v35.root = _ORIGINAL_V35_ROOT

import wepld_s2_checkpoint_ledger_repair_governance_v39_selftest as _v39_st

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

# The values effective on v37 immediately after v39 has finished loading: the
# checkpoint identity v37 minted and no successor has ever moved, and the ledger
# identity v39 corrected it to.
V39_FINAL_CHECKPOINT_BLOB = "dc749635fc6b7094bc414da18c982941bbed91a6"
V39_FINAL_LEDGER_BLOB = "cbd6f7bca4f8f33435320be2d153e59b4588f073"

# v40's corrected pair, matching PR #261's exact-head reviewed bytes.
FINAL_CHECKPOINT_BLOB = "c76985050e796ae7553d88c856c4f4e90e6bbbb6"
FINAL_LEDGER_BLOB = "688f776b9097ab5ede9f7810218b2985753e0355"

if p.FINAL_CHECKPOINT_BLOB != V39_FINAL_CHECKPOINT_BLOB:
    base.fail("v40 frozen predecessor checkpoint identity drift")
if p.FINAL_LEDGER_BLOB != V39_FINAL_LEDGER_BLOB:
    base.fail("v40 frozen predecessor ledger identity drift")
if PRE_CHECKPOINT_BLOB == FINAL_CHECKPOINT_BLOB:
    base.fail("v40 corrected checkpoint target equals the PRE checkpoint")
if PRE_LEDGER_BLOB == FINAL_LEDGER_BLOB:
    base.fail("v40 corrected ledger target equals the PRE ledger")
if FINAL_CHECKPOINT_BLOB == V39_FINAL_CHECKPOINT_BLOB:
    base.fail("v40 corrected checkpoint target equals the superseded v39 target")
if FINAL_LEDGER_BLOB == V39_FINAL_LEDGER_BLOB:
    base.fail("v40 corrected ledger target equals the superseded v39 target")
if FINAL_CHECKPOINT_BLOB == FINAL_LEDGER_BLOB:
    base.fail("v40 transition targets collapsed onto one identity")


def _bind_corrected_targets() -> None:
    """Bind v37 to exactly the corrected pair, idempotently, one identity at a time.

    Mirrors v39's `_bind_corrected_ledger_target`, generalized to two independent
    identities. Each identity accepts exactly two values at this seam: the value
    effective immediately after v39 finished loading (old), or v40's corrected value
    (already bound). Any third value fails closed. Loading v40 as ``__main__`` and then
    importing it again under its canonical module name in the same interpreter (as its
    own self-test module does) must not be mistaken for predecessor drift; the
    idempotent second branch is what keeps that safe.
    """
    actual_checkpoint = p.p.p.FINAL_CHECKPOINT_BLOB
    if actual_checkpoint == V39_FINAL_CHECKPOINT_BLOB:
        p.p.p.FINAL_CHECKPOINT_BLOB = FINAL_CHECKPOINT_BLOB
    elif actual_checkpoint != FINAL_CHECKPOINT_BLOB:
        base.fail(
            "v40 inherited checkpoint target is outside the exact old/corrected set: "
            f"old={V39_FINAL_CHECKPOINT_BLOB} corrected={FINAL_CHECKPOINT_BLOB} "
            f"actual={actual_checkpoint}"
        )

    actual_ledger = p.p.p.FINAL_LEDGER_BLOB
    if actual_ledger == V39_FINAL_LEDGER_BLOB:
        p.p.p.FINAL_LEDGER_BLOB = FINAL_LEDGER_BLOB
    elif actual_ledger != FINAL_LEDGER_BLOB:
        base.fail(
            "v40 inherited ledger target is outside the exact old/corrected set: "
            f"old={V39_FINAL_LEDGER_BLOB} corrected={FINAL_LEDGER_BLOB} "
            f"actual={actual_ledger}"
        )


# In-memory successor binding only. The frozen v39 (and v38, v37) repository bytes are
# unchanged and are verified below and by the predecessor self-tests.
_bind_corrected_targets()


def _with_v39_resting_view(func: Any) -> Any:
    """Run ``func`` with v37's live pair presented as v39 was frozen expecting.

    Every v38/v39 consumer of FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB is reached only
    through v39's own ``selftest()`` or ``install()``. For the exact dynamic extent of
    one such call, v37's live attributes are swapped to the values effective right
    after v39 finished loading (v39's own resting state), then restored to v40's real,
    permanently-bound values in a ``finally`` - so a raised exception cannot leave the
    binding moved.
    """

    def _wrapped(*args: Any, **kwargs: Any) -> Any:
        original_checkpoint = p.p.p.FINAL_CHECKPOINT_BLOB
        original_ledger = p.p.p.FINAL_LEDGER_BLOB
        p.p.p.FINAL_CHECKPOINT_BLOB = V39_FINAL_CHECKPOINT_BLOB
        p.p.p.FINAL_LEDGER_BLOB = V39_FINAL_LEDGER_BLOB
        try:
            return func(*args, **kwargs)
        finally:
            p.p.p.FINAL_CHECKPOINT_BLOB = original_checkpoint
            p.p.p.FINAL_LEDGER_BLOB = original_ledger

    return _wrapped


POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_CANONICAL_DOCUMENTATION_CHECKPOINT_AND_LEDGER_TARGET_CORRECTION"
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

for _path, _expected in ((p.P, V39_P_BLOB), (p.T, V39_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v40 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    """Project to v39 bytes and prove the projection lands on the canonical predecessor."""
    replacements = _v39_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v40 workflow does not reverse to exact canonical v39 predecessor: "
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


def req_v39(view: Any) -> None:
    for path, expected in ((p.P, V39_P_BLOB), (p.T, V39_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v40 candidate/base is missing frozen v39 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v39 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def req_pre_docs(view: Any) -> None:
    for path, expected in ((CHECKPOINT, PRE_CHECKPOINT_BLOB), (LEDGER, PRE_LEDGER_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v40 requires the canonical documentation path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v40 bootstrap documentation state drifted: {path}: "
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
        _with_v39_resting_view(p.selftest)()
    finally:
        p.root = original_root
        p.raw_root = original_raw


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v40 bootstrap delta must be exactly two v40 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v40 bootstrap base authorizes only corrected canonical-documentation "
                "checkpoint/ledger-target activation"
            )
        req_v39(candidate)
        req_v39(policy_base)
        req_pre_docs(candidate)
        req_pre_docs(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v40 policy files are frozen after activation")

    projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
    _with_v39_resting_view(p.delta)(projected_candidate, projected_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
        _with_v39_resting_view(p.basectrl)(projected_candidate, projected_base)
        return

    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != P_WF[path]:
                base.fail(f"v40 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v40 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v40 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v40 steady-state controlled file drifted: {path}")

    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
        _with_v39_resting_view(p.ext)(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        _with_v39_resting_view(p.allowed)(remaining, stage)


def files(view: Any) -> None:
    _with_v39_resting_view(p.files)(_workflow_predecessor_projection(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v40 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v40 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v40 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    _with_v39_resting_view(_call)("v39 success printer", p.printer, stage, mode_)
    print("wepld_policy_successor_v40=S2_CANONICAL_DOCUMENTATION_CHECKPOINT_AND_LEDGER_TARGET_CORRECTION")
    print(f"v40_authority={AUTH}")
    print(f"s2_implementation_authority_v40={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v40={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v40={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v40={NETWORK_AUTHORITY}")
    print(f"source_admission_v40={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v40={NEXT_AUTHORITY_GATE}")
    # Cosmetic annotation only: canonical v39's activation output prints a hardcoded
    # literal ("..._CORRECTION_ONLY") that does not match its own authoritative
    # v39_authority value ("..._SECOND_CORRECTION_ONLY"). Recorded in PR #260 comment
    # 5494918249 and PR #261. It grants nothing, moves no pin, and changes no gate;
    # v39's own frozen output line above (printed by the predecessor call) is left
    # exactly as it is. This line documents the known mismatch without editing frozen
    # v39 bytes.
    print(
        "wepld_v39_activation_label_known_defect="
        "PRINTED_CORRECTION_ONLY_AUTHORITATIVE_SECOND_CORRECTION_ONLY_COSMETIC_NO_AUTHORITY_CHANGE"
    )


def _chain() -> tuple[Any, ...]:
    return (p, p.p, p.p.p, p.p.p.p, p.p.p.p.p) + tuple(p.p.p.p.p.PREDECESSOR_CHAIN)


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v40 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v40 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v40 workflow identity projection drifted")
    if p.p.p.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v40 inherited checkpoint target binding drifted")
    if p.FINAL_CHECKPOINT_BLOB != V39_FINAL_CHECKPOINT_BLOB:
        base.fail("v40 must leave the v39 checkpoint self-literal intact between calls")
    if p.p.p.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v40 inherited ledger target binding drifted")
    if p.FINAL_LEDGER_BLOB != V39_FINAL_LEDGER_BLOB:
        base.fail("v40 must leave the v39 ledger self-literal intact between calls")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v40 inherited S2-AUTH-013 route decision drifted")


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    _with_v39_resting_view(p.install)()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v39 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v39 S1-005 evidence-freeze hook"),
            p.p.p.p.p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v39 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v39 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v39 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v39 files hook"), p.files),
        (_attr(shell, "print_success", "v39 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v40 predecessor hook drifted")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v40 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v40 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v40 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v40 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v40 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v40 allowed hook")
    _bind(shell, "verify_policy_files", files, "v40 files hook")
    _bind(shell, "print_success", printer, "v40 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_checkpoint_ledger_repair_governance_v40_selftest import run

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
