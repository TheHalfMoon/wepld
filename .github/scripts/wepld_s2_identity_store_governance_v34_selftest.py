#!/usr/bin/env python3
"""Self-tests for the v34 canonical-documentation transition successor.

Scope, stated because it is narrower than it looks.

These tests prove that the transition guards fail closed: that the authorized
scope is exactly two non-policy, non-base-controlled paths, that the pinned
pre-transition state is what this policy was frozen against, that any ledger
which is neither the pinned nor the authorized blob is refused, that the
workflow projection reverses exactly to the v33 predecessor, and that the
inherited evidence freeze still holds.

They do **not** prove the positive transition, and cannot. `docs_transition`
compares against pinned post-transition blobs, so constructing a passing case
would need both authorized documents embedded here as literals. v33 could embed
its authorized artifact because a Rust module export is small; these are a
multi-thousand-word checkpoint and a growing ledger, and copying them into the
policy would duplicate the very bytes the pin exists to fix.

The positive path is therefore proven where it actually happens: the transition
pull request either satisfies the pinned blobs at both gates or is refused. That
is a real proof rather than a weaker one, because it runs against the true
candidate and the true base instead of a fixture.
"""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v34_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v34 self-test overlay exceeds read bound: {path}")
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
    base.fail(f"v34 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_CANONICAL_DOCUMENTATION_TRANSITION_ONLY":
        base.fail("v34 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.q.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v34 must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.q.DEPENDENCY_ADMISSION:
        base.fail("v34 must not widen dependency admission")
    if p.SOURCE_ADMISSION != p.q.SOURCE_ADMISSION:
        base.fail("v34 must not widen source admission")
    if p.SOURCE_ADMISSION != "NONE":
        base.fail("v34 source admission must remain NONE")


def _check_transition_scope() -> None:
    """The authorized set is exactly two paths, and neither is protected."""
    if p.DOCS != frozenset({p.CHECKPOINT, p.LEDGER}):
        base.fail("v34 documentation transition scope drifted")
    if p.DOCS & p.ALL_POLICY_FILES:
        base.fail("v34 documentation transition must not overlap any policy file")
    for path in sorted(p.DOCS):
        if path in base.BASE_CONTROLLED_PATHS:
            base.fail(f"v34 must not authorize a base-controlled path: {path}")
    if len(p.DOCS) != 2:
        base.fail("v34 documentation transition must authorize exactly two paths")


def _check_pinned_pre_state() -> None:
    """The tree this policy was frozen against carries the pinned pre bytes."""
    for path, expected in (
        (p.CHECKPOINT, p.PRE_CHECKPOINT_BLOB),
        (p.LEDGER, p.PRE_LEDGER_BLOB),
    ):
        actual = p.V25.blob(p.root.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v34 pinned pre-transition state drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _check_pins_are_distinct() -> None:
    """A transition that changes nothing is not a transition."""
    if p.PRE_CHECKPOINT_BLOB == p.FINAL_CHECKPOINT_BLOB:
        base.fail("v34 checkpoint pins are identical")
    if p.PRE_LEDGER_BLOB == p.FINAL_LEDGER_BLOB:
        base.fail("v34 ledger pins are identical")


def _check_transition_refuses_the_pre_state() -> None:
    """A candidate that still carries the pre bytes is not the transition."""
    _expect_failure(
        "candidate still carrying the pinned pre-transition bytes",
        lambda: p.docs_transition(p.root, p.root),
    )


def _check_transition_refuses_drift() -> None:
    """Any byte other than the pinned pair is refused, on either side."""
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


def _check_ledger_projection() -> None:
    """A pinned ledger is not rewritten; any other ledger fails closed."""
    if p._ledger_baseline(p.root) is not None:
        base.fail("v34 must not project a ledger that is already the pinned bytes")

    drifted = p.root.read_bytes(p.LEDGER, base.MAX_POLICY_FILE_BYTES) + b"\ndrift\n"
    view = OverlayView(p.root, {p.LEDGER: drifted})
    _expect_failure(
        "ledger that is neither the pinned nor the authorized blob",
        lambda: p._ledger_baseline(view),
    )


def _check_workflow_projection_reverses() -> None:
    projected = p._predecessor_projection(p.root)
    for path in (p.FW, p.AW):
        reversed_bytes = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(reversed_bytes) != p.Q_WF[path]:
            base.fail(f"v34 workflow projection does not reverse to v33: {path}")
        if p._V34_ENTRYPOINT in reversed_bytes:
            base.fail(f"v34 workflow projection left a v34 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V34_ENTRYPOINT, b"wepld_unknown_entrypoint.py", 1
    )
    view = OverlayView(p.root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._predecessor_projection(view),
    )


def _check_freeze_still_symmetric() -> None:
    """The inherited S1-005 evidence-freeze symmetry remains in force."""
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
    _check_transition_scope()
    _check_pinned_pre_state()
    _check_pins_are_distinct()
    _check_transition_refuses_the_pre_state()
    _check_transition_refuses_drift()
    _check_ledger_projection()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_freeze_still_symmetric()

    print("wepld v34 S2 canonical-documentation transition self-tests: PASS")
