#!/usr/bin/env python3
"""Self-tests for the v32 frozen-policy projection repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v32_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v32 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any) -> None:
    try:
        action()
    except base.PolicyError:
        return
    base.fail(f"v32 self-test expected a fail-closed rejection: {label}")


def _tranche_export() -> bytes:
    """The single authorized post-tranche Core export."""
    return p.ADMITTED_CORE_EXPORT


def _check_baseline_projection_is_identity() -> None:
    """The canonical pre-tranche export is never rewritten."""
    view = OverlayView(p.root, {p.CORE_EXPORT: p.BASE_CORE_EXPORT})
    if p._core_export_baseline(view) is not None:
        base.fail("v32 must not project an export that is already canonical baseline")
    if p._project_core_export(view) is not view:
        base.fail("v32 baseline export projection must be an identity projection")


def _check_tranche_projection_reverses() -> None:
    """An exact single registration of both modules reverses to the baseline."""
    tranche = _tranche_export()
    if tranche == p.BASE_CORE_EXPORT:
        base.fail("v32 self-test tranche fixture did not change the export")
    if tranche.count(p.IDENTITY_REGISTRATION) != 1:
        base.fail("v32 self-test tranche fixture identity registration is not exact")
    if tranche.count(p.STORE_REGISTRATION) != 1:
        base.fail("v32 self-test tranche fixture store registration is not exact")

    view = OverlayView(p.root, {p.CORE_EXPORT: tranche})
    projected = p._core_export_baseline(view)
    if projected != p.BASE_CORE_EXPORT:
        base.fail("v32 tranche export must reverse to the exact canonical baseline")
    if p.V25.blob(projected) != p.CORE_EXPORT_BASE_BLOB:
        base.fail("v32 projected export does not match the frozen baseline blob")
    if p.V25.blob(tranche) != p.CORE_EXPORT_ADMITTED_BLOB:
        base.fail("v32 authorized export does not match the frozen admitted blob")

    reader = p._project_core_export(view)
    if reader.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES) != p.BASE_CORE_EXPORT:
        base.fail("v32 export projection did not supply canonical baseline bytes")


def _check_duplicate_registration_fails_closed() -> None:
    """A doubled registration is a real defect and must not be projected away."""
    doubled = _tranche_export() + b"\npub mod identity;\n"
    view = OverlayView(p.root, {p.CORE_EXPORT: doubled})
    _expect_failure(
        "duplicate identity registration",
        lambda: p._core_export_baseline(view),
    )


def _check_registered_but_edited_export_fails_closed() -> None:
    """Registration counts alone are not a sufficient acceptance condition.

    An export that registers each module exactly once but also carries an
    unrelated edit satisfies a count-based predicate. Acceptance is bound to the
    exact authorized bytes so this is rejected rather than projected away.
    """
    registrations = p.STORE_REGISTRATION + b"\n" + p.IDENTITY_REGISTRATION + b"\n"
    counted_but_edited = (
        p.BASE_CORE_EXPORT.replace(
            b"pub mod project;", registrations + b"pub mod project;", 1
        )
        + b"\npub mod unrelated_addition;\n"
    )
    if counted_but_edited.count(p.IDENTITY_REGISTRATION) != 1:
        base.fail("v32 self-test fixture identity registration is not exact")
    if counted_but_edited.count(p.STORE_REGISTRATION) != 1:
        base.fail("v32 self-test fixture store registration is not exact")
    if counted_but_edited == p.ADMITTED_CORE_EXPORT:
        base.fail("v32 self-test fixture must differ from the authorized export")
    view = OverlayView(p.root, {p.CORE_EXPORT: counted_but_edited})
    _expect_failure(
        "exactly-registered export carrying an unrelated edit",
        lambda: p._core_export_baseline(view),
    )


def _check_missing_registration_fails_closed() -> None:
    """A partial tranche is a real defect and must not be projected away."""
    partial = p.BASE_CORE_EXPORT.replace(
        b"pub mod project;\n", b"pub mod identity;\npub mod project;\n", 1
    )
    view = OverlayView(p.root, {p.CORE_EXPORT: partial})
    _expect_failure(
        "missing evidence-store registration",
        lambda: p._core_export_baseline(view),
    )


def _check_unrelated_export_edit_fails_closed() -> None:
    """An export that is neither baseline nor the exact tranche is rejected."""
    edited = p.BASE_CORE_EXPORT + b"\npub mod something_else;\n"
    view = OverlayView(p.root, {p.CORE_EXPORT: edited})
    _expect_failure(
        "unauthorized export edit",
        lambda: p._core_export_baseline(view),
    )


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.root)
    for path in (p.FW, p.AW):
        reversed_bytes = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(reversed_bytes) != p.P_WF[path]:
            base.fail(f"v32 workflow projection does not reverse to v31: {path}")
        if p._V32_ENTRYPOINT in reversed_bytes:
            base.fail(f"v32 workflow projection left a v32 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V32_ENTRYPOINT, b"wepld_unknown_entrypoint.py", 1
    )
    view = OverlayView(p.root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
    )


def _check_freeze_projects_both_sides() -> None:
    """The S1-005 freeze must compare like with like.

    This is exercised behaviourally rather than by stubbing the delegate, because
    the delegate is the layer that projects the candidate: replacing it would
    hide the very asymmetry under repair.

    On canonical `main` both the candidate and the policy base carry the admitted
    dependency state. An unchanged register must compare equal, which is exactly
    what fails before this repair. A genuinely changed register must still be
    rejected.
    """
    # Admitted base, admitted candidate, frozen evidence unchanged: must pass.
    p.freeze_s1_005_evidence(p.root, p.root)

    # Frozen evidence genuinely changed: must still fail closed.
    register = p.V26.DEPENDENCY_REGISTER
    mutated = p.root.read_bytes(register, base.MAX_POLICY_FILE_BYTES) + b"\ndrift\n"
    view = OverlayView(p.root, {register: mutated})
    _expect_failure(
        "changed frozen S1-005 evidence",
        lambda: p.freeze_s1_005_evidence(view, p.root),
    )


def _check_authority_markers() -> None:
    if p.AUTH != "S2_IDENTITY_STORE_FROZEN_POLICY_PROJECTION_REPAIR_ONLY":
        base.fail("v32 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v32 must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v32 must not widen dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v32 must not widen source admission")
    if p.SOURCE_ADMISSION != "NONE":
        base.fail("v32 source admission must remain NONE")


def run() -> None:
    p.run_predecessor_selftests(p.root)
    p.install()

    _check_authority_markers()
    _check_baseline_projection_is_identity()
    _check_tranche_projection_reverses()
    _check_duplicate_registration_fails_closed()
    _check_registered_but_edited_export_fails_closed()
    _check_missing_registration_fails_closed()
    _check_unrelated_export_edit_fails_closed()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_freeze_projects_both_sides()

    print("wepld v32 S2 frozen-policy projection repair self-tests: PASS")
