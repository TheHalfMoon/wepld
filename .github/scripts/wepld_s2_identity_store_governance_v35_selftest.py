#!/usr/bin/env python3
"""Self-tests for the v35 corrected canonical-documentation transition target.

v35 exists only because the author self-audit of PR #248 found two material
checkpoint defects after v34 had already frozen the original FINAL checkpoint
blob. These tests prove that v35 changes exactly that target, preserves the
ledger target and every inherited authority boundary, rejects the superseded
v34 checkpoint target, binds the correction idempotently across module re-entry,
reverses its workflows exactly to v34, and remains valid on either side of the
corrected one-shot transition.

As with v34, the positive transition itself is proven by the real two-document
candidate at both exact-head gates rather than by copying the large canonical
checkpoint and ledger into a fixture.
"""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v35 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def entries(self) -> Any:
        return self._view.entries()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any) -> None:
    try:
        action()
    except base.PolicyError:
        return
    base.fail(f"v35 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_CANONICAL_DOCUMENTATION_TRANSITION_CORRECTION_ONLY":
        base.fail("v35 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.q.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v35 must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.q.DEPENDENCY_ADMISSION:
        base.fail("v35 must not widen dependency admission")
    if p.SOURCE_ADMISSION != p.q.SOURCE_ADMISSION:
        base.fail("v35 must not widen source admission")
    if p.SOURCE_ADMISSION != "NONE":
        base.fail("v35 source admission must remain NONE")


def _check_target_correction_is_exact() -> None:
    if p.PRE_CHECKPOINT_BLOB != p.q.PRE_CHECKPOINT_BLOB:
        base.fail("v35 changed the checkpoint PRE pin")
    if p.PRE_LEDGER_BLOB != p.q.PRE_LEDGER_BLOB:
        base.fail("v35 changed the ledger PRE pin")
    if p.FINAL_LEDGER_BLOB != p.q.FINAL_LEDGER_BLOB:
        base.fail("v35 changed the ledger FINAL pin")
    if p.V34_FINAL_CHECKPOINT_BLOB != "2620c272d99eebe36d3756f12f3fe0ff611207a9":
        base.fail("v35 superseded v34 checkpoint identity drifted")
    if p.FINAL_CHECKPOINT_BLOB != "28c50353718f4b836daf67df2a52f6d9471e847b":
        base.fail("v35 corrected checkpoint target drifted")
    if p.FINAL_CHECKPOINT_BLOB == p.V34_FINAL_CHECKPOINT_BLOB:
        base.fail("v35 correction does not change the defective checkpoint target")
    if p.q.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v35 did not bind the inherited v34 target to the correction")


def _check_checkpoint_binding_is_exact_and_idempotent() -> None:
    """Re-entry is a no-op; any target outside the exact pair fails closed."""
    p._bind_corrected_checkpoint_target()
    if p.q.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v35 first idempotent checkpoint bind drifted")
    p._bind_corrected_checkpoint_target()
    if p.q.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v35 second idempotent checkpoint bind drifted")

    original = p.q.FINAL_CHECKPOINT_BLOB
    p.q.FINAL_CHECKPOINT_BLOB = "0" * 40
    try:
        _expect_failure(
            "checkpoint target outside old/corrected exact set",
            p._bind_corrected_checkpoint_target,
        )
    finally:
        p.q.FINAL_CHECKPOINT_BLOB = original
    p._bind_corrected_checkpoint_target()
    if p.q.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v35 checkpoint bind did not recover after negative oracle")


def _check_transition_scope() -> None:
    if p.DOCS != frozenset({p.CHECKPOINT, p.LEDGER}):
        base.fail("v35 documentation transition scope drifted")
    if p.DOCS & p.ALL_POLICY_FILES:
        base.fail("v35 documentation transition must not overlap policy files")
    for path in sorted(p.DOCS):
        if path in base.BASE_CONTROLLED_PATHS:
            base.fail(f"v35 must not authorize a base-controlled path: {path}")
    if len(p.DOCS) != 2:
        base.fail("v35 documentation transition must authorize exactly two paths")


def _check_local_state_is_one_of_the_corrected_pinned_states() -> None:
    sides = []
    for path, pre, final in (
        (p.CHECKPOINT, p.PRE_CHECKPOINT_BLOB, p.FINAL_CHECKPOINT_BLOB),
        (p.LEDGER, p.PRE_LEDGER_BLOB, p.FINAL_LEDGER_BLOB),
    ):
        actual = p.V25.blob(p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual == pre:
            sides.append("PRE")
        elif actual == final:
            sides.append("FINAL")
        else:
            base.fail(
                f"v35 local documentation state is neither corrected pinned side: "
                f"{path}: actual={actual}"
            )
    if len(set(sides)) != 1:
        base.fail(f"v35 local documentation state is half-applied: {sides}")


def _check_superseded_v34_target_is_rejected() -> None:
    old = p.root.read_bytes(p.CHECKPOINT, base.MAX_POLICY_FILE_BYTES)
    if p.V25.blob(old) == p.V34_FINAL_CHECKPOINT_BLOB:
        base.fail("v35 self-test unexpectedly runs on the superseded v34 FINAL")
    if p.V34_FINAL_CHECKPOINT_BLOB == p.FINAL_CHECKPOINT_BLOB:
        base.fail("v35 accepts the superseded v34 FINAL checkpoint identity")


def _check_transition_refuses_no_op_and_drift() -> None:
    _expect_failure(
        "candidate identical to base",
        lambda: p.docs_transition(p.root, p.root),
    )
    for path in sorted(p.DOCS):
        drifted = p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES) + b"\ndrift\n"
        view = OverlayView(p.root, {path: drifted})
        _expect_failure(
            f"candidate carrying drifted bytes for {path}",
            lambda view=view: p.docs_transition(view, p.root),
        )
        _expect_failure(
            f"base carrying drifted bytes for {path}",
            lambda view=view: p.docs_transition(p.root, view),
        )


def _check_workflow_projection_reverses() -> None:
    projected = p._predecessor_projection(p.root)
    for path in (p.FW, p.AW):
        reversed_bytes = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(reversed_bytes) != p.Q_WF[path]:
            base.fail(f"v35 workflow projection does not reverse to v34: {path}")
        if p._V35_ENTRYPOINT in reversed_bytes:
            base.fail(f"v35 workflow projection left a v35 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V35_ENTRYPOINT, b"wepld_unknown_entrypoint.py", 1
    )
    view = OverlayView(p.root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._predecessor_projection(view),
    )


def _check_inherited_ledger_and_evidence_guards_remain() -> None:
    if p.FINAL_LEDGER_BLOB != p.q.FINAL_LEDGER_BLOB:
        base.fail("v35 widened or changed the ledger FINAL target")
    p.q._state(p.root)
    if p.q._V18.FINAL_LEARNING_BLOB != p.PRE_LEDGER_BLOB:
        base.fail("v35 left inherited ledger widening active after evaluation")
    p.Q_FREEZE(p.root, p.root)
    register = p.V26.DEPENDENCY_REGISTER
    mutated = p.root.read_bytes(register, base.MAX_POLICY_FILE_BYTES) + b"\ndrift\n"
    view = OverlayView(p.root, {register: mutated})
    _expect_failure(
        "changed frozen S1-005 evidence",
        lambda: p.Q_FREEZE(view, p.root),
    )


def run() -> None:
    p.run_predecessor_selftests(p.root)
    p.install()

    _check_authority_markers()
    _check_target_correction_is_exact()
    _check_checkpoint_binding_is_exact_and_idempotent()
    _check_transition_scope()
    _check_local_state_is_one_of_the_corrected_pinned_states()
    _check_superseded_v34_target_is_rejected()
    _check_transition_refuses_no_op_and_drift()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_inherited_ledger_and_evidence_guards_remain()

    print("wepld v35 corrected canonical-documentation transition self-tests: PASS")
