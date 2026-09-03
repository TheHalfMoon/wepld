#!/usr/bin/env python3
"""Repair a self-test-only defect in v43; no production logic changes.

v44 makes **no functional changes**: it wraps nothing new, moves no target,
and widens no authority. Its only purpose is to replace v43's own self-test
file with one whose positive oracle for `docs_transition` does not depend on
whatever documentation content happens to be checked out.

Root cause: v43's positive oracle
(`_check_docs_transition_rejects_drifted_checkpoint`) called
`p._v37.docs_transition(final_candidate, p.raw_root)`, passing the real,
unmodified `raw_root` as the *base* argument and assuming its checkpoint/
ledger bytes always equal `PRE_CHECKPOINT_BLOB`/`PRE_LEDGER_BLOB`. That
assumption holds when v43's own self-test runs against v43's own branch (no
documentation change), but not against any real candidate that itself
carries the corrected FINAL documentation content - exactly PR #263's shape,
and exactly the scenario this whole successor chain exists to admit
correctly. Reproduced directly: v43's self-test, run against PR #263's
rebased tree (which legitimately carries PR #261's reviewed FINAL bytes),
failed with `v37 documentation transition base bytes drifted` - not the
admission logic (`s1-admission-integrity` genuinely succeeded on that exact
candidate, proving the v40-v43 fix chain is correct), but v43's own
self-test asserting a false property about what `raw_root` must contain.

Because `foundation-integrity`'s "Run candidate policy self-tests" step is a
required check for every candidate, this defect would fail-close the exact
kind of candidate this project's whole S2-AUTH-013/documentation-transition
work exists to admit.

The fix generalizes the technique v43's own positive oracle already used for
FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB to the PRE side as well: temporarily
rebind v37's live PRE_CHECKPOINT_BLOB/PRE_LEDGER_BLOB (in addition to
FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB, as before) to match fully synthetic
content this test constructs itself, so the oracle is provably correct
regardless of what real documentation content the checked-out tree happens
to carry - proven by re-running it directly against PR #263's own tree
locally before this successor's own PR is opened.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v44_integrity.py"
T = ".github/scripts/wepld_s2_checkpoint_ledger_repair_governance_v44_selftest.py"
T_BLOB = "3d6c293804802a87a45ffdca4d106f293aec9fbd"

V43_P_BLOB = "7be3076b0f6522e3ec1fb064b04ba497eb70a284"
V43_T_BLOB = "49d388068824ee466738dccadbbd9e131bc90ff9"

_V44_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v44_integrity.py"
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

# A plain top-level import here, not chain traversal, for the reason v42's
# own `_v37` import records: at nested predecessor-projection levels a `.p`
# chain can settle to a different module object than Python's own import
# cache. Must come after the chain above has already run once.
import wepld_s2_checkpoint_transition_governance_v37_integrity as _v37

V25 = p.V25
root = p.root
P_WF = dict(p.WF)

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False

# Inherited unchanged. v44 makes no functional/production changes at all.
CHECKPOINT = p.CHECKPOINT
LEDGER = p.LEDGER
DOCS = p.DOCS
PRE_CHECKPOINT_BLOB = p.PRE_CHECKPOINT_BLOB
PRE_LEDGER_BLOB = p.PRE_LEDGER_BLOB
FINAL_CHECKPOINT_BLOB = p.FINAL_CHECKPOINT_BLOB
FINAL_LEDGER_BLOB = p.FINAL_LEDGER_BLOB

if _v37.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
    base.fail("v44 inherited checkpoint target does not match v43's corrected pin")
if _v37.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
    base.fail("v44 inherited ledger target does not match v43's corrected pin")


# ---------------------------------------------------------------------------
# The fix. v43's own self-test file is frozen (append-only; it cannot be
# edited), and its own `run()` - reached through `run_predecessor_
# selftests()`'s recursive cascade, which every future successor's own
# selftest must run - unconditionally calls v43's broken positive oracle for
# `docs_transition`. Confirmed by direct call-stack trace: `v44.run_
# predecessor_selftests -> p.selftest() (p = v43) -> wepld_s2_checkpoint_
# ledger_repair_governance_v43_integrity.selftest -> wepld_s2_checkpoint_
# ledger_repair_governance_v43_selftest.run -> _check_docs_transition_
# rejects_drifted_checkpoint -> base.fail`. That check assumed `raw_root`
# always carries PRE-transition documentation content, which is false for
# any real candidate that itself carries the corrected FINAL content -
# exactly PR #263's shape. Left unpatched, this permanently fail-closes that
# entire class of candidate for every future successor, since the broken
# check reruns on every `foundation-integrity` "Run candidate policy
# self-tests" step forever.
#
# Superseded via the same `setattr` technique used throughout this chain
# (v34 on `_V18.state`, v41 on `run_predecessor_selftests`, v42/v43 on
# `files`/`delta` and friends) - but on a *self-test* module's own check
# function, not a production one. v43's `run()` resolves `_check_docs_
# transition_rejects_drifted_checkpoint` as a bare name from its own module
# globals at call time, so replacing that module attribute before `run()`
# ever executes is sufficient.
import wepld_s2_checkpoint_ledger_repair_governance_v43_selftest as _v43_selftest


class _V44OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v44 override overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return self._view.entries()

    def tree_identity(self, path: str) -> Any:
        return (id(self), path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _corrected_v43_docs_transition_check() -> None:
    """Supersedes ``wepld_s2_checkpoint_ledger_repair_governance_v43_selftest
    ._check_docs_transition_rejects_drifted_checkpoint``.

    Identical negative oracle; a corrected positive oracle that rebinds
    v37's live PRE_CHECKPOINT_BLOB/PRE_LEDGER_BLOB *and*
    FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB to fully synthetic content, so
    neither the base nor the candidate depends on what `raw_root` actually
    contains.
    """
    drifted_checkpoint = b"# v44 override synthetic WRONG checkpoint\n"
    view = _V44OverlayView(p.raw_root, {p.CHECKPOINT: drifted_checkpoint})
    try:
        _v37.docs_transition(view, p.raw_root)
    except base.PolicyError as exc:
        if "bytes drifted" not in str(exc):
            base.fail(
                "v44 override: docs_transition rejection came from the wrong "
                f"cause: {exc}"
            )
    else:
        base.fail(
            "v44 override: docs_transition must reject a checkpoint that "
            "matches no recognized identity"
        )

    synthetic_pre_checkpoint = b"# v44 override synthetic PRE checkpoint\n"
    synthetic_pre_ledger = b"# v44 override synthetic PRE ledger\n"
    synthetic_final_checkpoint = b"# v44 override synthetic FINAL checkpoint\n"
    synthetic_final_ledger = b"# v44 override synthetic FINAL ledger\n"
    synthetic_pre_checkpoint_blob = V25.blob(synthetic_pre_checkpoint)
    synthetic_pre_ledger_blob = V25.blob(synthetic_pre_ledger)
    synthetic_final_checkpoint_blob = V25.blob(synthetic_final_checkpoint)
    synthetic_final_ledger_blob = V25.blob(synthetic_final_ledger)
    synthetic_blobs = {
        synthetic_pre_checkpoint_blob,
        synthetic_pre_ledger_blob,
        synthetic_final_checkpoint_blob,
        synthetic_final_ledger_blob,
    }
    if len(synthetic_blobs) != 4:
        base.fail("v44 override: synthetic PRE/FINAL identities collided with each other")

    saved_pre_checkpoint = _v37.PRE_CHECKPOINT_BLOB
    saved_pre_ledger = _v37.PRE_LEDGER_BLOB
    saved_final_checkpoint = _v37.FINAL_CHECKPOINT_BLOB
    saved_final_ledger = _v37.FINAL_LEDGER_BLOB
    _v37.PRE_CHECKPOINT_BLOB = synthetic_pre_checkpoint_blob
    _v37.PRE_LEDGER_BLOB = synthetic_pre_ledger_blob
    _v37.FINAL_CHECKPOINT_BLOB = synthetic_final_checkpoint_blob
    _v37.FINAL_LEDGER_BLOB = synthetic_final_ledger_blob
    try:
        synthetic_base = _V44OverlayView(
            p.raw_root,
            {p.CHECKPOINT: synthetic_pre_checkpoint, p.LEDGER: synthetic_pre_ledger},
        )
        synthetic_candidate = _V44OverlayView(
            p.raw_root,
            {p.CHECKPOINT: synthetic_final_checkpoint, p.LEDGER: synthetic_final_ledger},
        )
        try:
            _v37.docs_transition(synthetic_candidate, synthetic_base)
        except base.PolicyError as exc:
            base.fail(
                "v44 override: docs_transition must accept a candidate/base pair "
                f"whose bytes genuinely match the live PRE/FINAL identity: {exc}"
            )
    finally:
        _v37.PRE_CHECKPOINT_BLOB = saved_pre_checkpoint
        _v37.PRE_LEDGER_BLOB = saved_pre_ledger
        _v37.FINAL_CHECKPOINT_BLOB = saved_final_checkpoint
        _v37.FINAL_LEDGER_BLOB = saved_final_ledger

    if (
        _v37.PRE_CHECKPOINT_BLOB != saved_pre_checkpoint
        or _v37.PRE_LEDGER_BLOB != saved_pre_ledger
        or _v37.FINAL_CHECKPOINT_BLOB != saved_final_checkpoint
        or _v37.FINAL_LEDGER_BLOB != saved_final_ledger
    ):
        base.fail("v44 override: left the live checkpoint/ledger pin moved")


_ORIGINAL_V43_DOCS_TRANSITION_CHECK = (
    _v43_selftest._check_docs_transition_rejects_drifted_checkpoint
)
_v43_selftest._check_docs_transition_rejects_drifted_checkpoint = (
    _corrected_v43_docs_transition_check
)


POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_V43_SELFTEST_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE"
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


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    """Project to v43 bytes and prove the projection lands on the canonical predecessor."""
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
                    "v44 bootstrap delta must be exactly two v44 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v44 bootstrap base authorizes only the v43 self-test-only repair "
                "activation"
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
    print("wepld_policy_successor_v44=S2_V43_SELFTEST_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE")
    print(f"v44_authority={AUTH}")
    print(f"s2_implementation_authority_v44={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v44={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v44={GIT_EXECUTION_AUTHORITY}")
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
    if _v37.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v44 must not move the inherited checkpoint target")
    if _v37.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v44 must not move the inherited ledger target")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v44 inherited S2-AUTH-013 route decision drifted")
    for _name in p._NARROWED_V40_ATTRS:
        if getattr(p._V40, _name) is p._ORIGINAL_V40_ATTR_FUNCTIONS[_name]:
            base.fail(f"v44 lost v43's resting-view scope repair: {_name}")
    if (
        _v43_selftest._check_docs_transition_rejects_drifted_checkpoint
        is not _corrected_v43_docs_transition_check
    ):
        base.fail("v44 lost its override of v43's broken positive oracle")


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
    for _name in p._NARROWED_V40_ATTRS:
        if getattr(p._V40, _name) is p._ORIGINAL_V40_ATTR_FUNCTIONS[_name]:
            base.fail(f"v44 lost v43's resting-view scope repair: {_name}")
    if (
        _v43_selftest._check_docs_transition_rejects_drifted_checkpoint
        is not _corrected_v43_docs_transition_check
    ):
        base.fail("v44 lost its override of v43's broken positive oracle")

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
    from wepld_s2_checkpoint_ledger_repair_governance_v44_selftest import run

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
