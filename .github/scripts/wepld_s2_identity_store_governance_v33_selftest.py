#!/usr/bin/env python3
"""Self-tests for the v33 pre-tranche view repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v33_integrity as p


class OverlayView:
    def __init__(
        self,
        view: Any,
        replacements: dict[str, bytes],
        extra_paths: frozenset[str] = frozenset(),
        omit_paths: frozenset[str] = frozenset(),
    ) -> None:
        self._view = view
        self._replacements = replacements
        self._extra_paths = extra_paths
        self._omit_paths = omit_paths

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v33 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def entries(self) -> Any:
        source = [
            entry
            for entry in self._view.entries()
            if entry.path not in self._omit_paths
        ]
        if not self._extra_paths:
            return source
        known = {entry.path for entry in source}
        template = source[0]
        for path in sorted(self._extra_paths - known):
            source.append(_FakeEntry(path, template))
        return source

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


class _FakeEntry:
    """Minimal entry stand-in used only to synthesise a path inventory."""

    def __init__(self, path: str, template: Any) -> None:
        self.path = path
        self.mode = getattr(template, "mode", "100644")


def _expect_failure(label: str, action: Any) -> None:
    try:
        action()
    except base.PolicyError:
        return
    base.fail(f"v33 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_IDENTITY_STORE_PRETRANCHE_VIEW_REPAIR_ONLY":
        base.fail("v33 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v33 must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v33 must not widen dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v33 must not widen source admission")
    if p.SOURCE_ADMISSION != "NONE":
        base.fail("v33 source admission must remain NONE")


def _check_export_acceptance_is_exact() -> None:
    """Inherited exact-byte export acceptance is preserved."""
    baseline_view = OverlayView(p.root, {p.CORE_EXPORT: p.BASE_CORE_EXPORT})
    if p._core_export_baseline(baseline_view) is not None:
        base.fail("v33 must not project an export that is already canonical baseline")

    admitted_view = OverlayView(p.root, {p.CORE_EXPORT: p.ADMITTED_CORE_EXPORT})
    if p._core_export_baseline(admitted_view) != p.BASE_CORE_EXPORT:
        base.fail("v33 authorized export must reverse to the exact canonical baseline")

    registrations = p.p.STORE_REGISTRATION + b"\n" + p.p.IDENTITY_REGISTRATION + b"\n"
    counted_but_edited = (
        p.BASE_CORE_EXPORT.replace(
            b"pub mod project;", registrations + b"pub mod project;", 1
        )
        + b"\npub mod unrelated_addition;\n"
    )
    edited_view = OverlayView(p.root, {p.CORE_EXPORT: counted_but_edited})
    _expect_failure(
        "exactly-registered export carrying an unrelated edit",
        lambda: p._core_export_baseline(edited_view),
    )


def _check_no_omission_without_projection() -> None:
    """A canonical pre-tranche view omits nothing."""
    view = OverlayView(p.root, {p.CORE_EXPORT: p.BASE_CORE_EXPORT})
    if p.pretranche_omissions(view) != frozenset():
        base.fail("v33 must omit nothing when the export is already baseline")


def _check_omission_covers_the_exact_tranche() -> None:
    """The projected view hides exactly the authorized tranche product paths."""
    view = OverlayView(
        p.root,
        {p.CORE_EXPORT: p.ADMITTED_CORE_EXPORT},
        p.TRANCHE_PRODUCT_PATHS,
    )
    omitted = p.pretranche_omissions(view)
    if omitted != p.TRANCHE_PRODUCT_PATHS:
        base.fail(f"v33 omission set is not the exact tranche product set: {sorted(omitted)}")

    projected = p._ProjectionView(
        view, {p.CORE_EXPORT: p.BASE_CORE_EXPORT}, omitted
    )
    paths = p.V25.ps(projected)
    for path in sorted(p.TRANCHE_PRODUCT_PATHS):
        if path in paths:
            base.fail(f"v33 projected view still lists a tranche path: {path}")
    if projected.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES) != p.BASE_CORE_EXPORT:
        base.fail("v33 projected view must report the canonical baseline export")


def _check_view_is_self_consistent() -> None:
    """The projected export and the projected path set must agree.

    This is the defect v33 repairs: a baseline export combined with a
    post-tranche path set makes the frozen product verifier demand registrations
    the projected export no longer has.
    """
    view = OverlayView(
        p.root,
        {p.CORE_EXPORT: p.ADMITTED_CORE_EXPORT},
        p.TRANCHE_PRODUCT_PATHS,
    )
    projected = p._ProjectionView(
        view, {p.CORE_EXPORT: p.BASE_CORE_EXPORT}, p.pretranche_omissions(view)
    )
    paths = p.V25.ps(projected)
    export = projected.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    registers = (
        export.count(p.p.IDENTITY_REGISTRATION) == 1
        and export.count(p.p.STORE_REGISTRATION) == 1
    )
    product_present = p.V25.PRODUCT_NEW_FILES <= paths
    if product_present != registers:
        base.fail(
            "v33 projected view is not self-consistent: "
            f"product_paths_present={product_present} export_registers={registers}"
        )


def _check_partial_tranche_fails_closed() -> None:
    """The authorized export may not appear beside an incomplete product set.

    Constructed by omitting product paths so the case holds on both a
    pre-tranche and a post-tranche tree.
    """
    kept = frozenset({p.V25.IDENTITY_MODULE})
    view = OverlayView(
        p.root,
        {p.CORE_EXPORT: p.ADMITTED_CORE_EXPORT},
        kept,
        p.TRANCHE_PRODUCT_PATHS - kept,
    )
    present = p.TRANCHE_PRODUCT_PATHS & p.V25.ps(view)
    if present != kept:
        base.fail(f"v33 self-test could not construct a partial tranche: {sorted(present)}")
    _expect_failure(
        "authorized export with an incomplete tranche product set",
        lambda: p.pretranche_omissions(view),
    )


def _check_entry_projection_is_wrapper_only() -> None:
    """`LocalRepositoryView` itself must never be filtered.

    The inherited exact-HEAD entry inventory invariant depends on the real view
    reporting every tracked entry, so the omission must live on the wrapper. The
    real inventory is compared against a wrapper that omits the tranche paths.
    """
    real = {entry.path for entry in p.root.entries()}
    view = OverlayView(
        p.root,
        {p.CORE_EXPORT: p.ADMITTED_CORE_EXPORT},
        p.TRANCHE_PRODUCT_PATHS,
    )
    projected = p._ProjectionView(
        view, {p.CORE_EXPORT: p.BASE_CORE_EXPORT}, p.TRANCHE_PRODUCT_PATHS
    )
    if {entry.path for entry in projected.entries()} & p.TRANCHE_PRODUCT_PATHS:
        base.fail("v33 projected wrapper still lists a tranche path")
    unchanged = {entry.path for entry in p.root.entries()}
    if real != unchanged:
        base.fail("v33 must not alter the real repository view entry inventory")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.root)
    for path in (p.FW, p.AW):
        reversed_bytes = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(reversed_bytes) != p.P_WF[path]:
            base.fail(f"v33 workflow projection does not reverse to v32: {path}")
        if p._V33_ENTRYPOINT in reversed_bytes:
            base.fail(f"v33 workflow projection left a v33 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V33_ENTRYPOINT, b"wepld_unknown_entrypoint.py", 1
    )
    view = OverlayView(p.root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
    )


def _check_freeze_still_symmetric() -> None:
    """The inherited v32 S1-005 symmetry repair remains in force."""
    p.P_FREEZE(p.root, p.root)
    register = p.V26.DEPENDENCY_REGISTER
    mutated = p.root.read_bytes(register, base.MAX_POLICY_FILE_BYTES) + b"\ndrift\n"
    view = OverlayView(p.root, {register: mutated})
    _expect_failure(
        "changed frozen S1-005 evidence",
        lambda: p.P_FREEZE(view, p.root),
    )


def run() -> None:
    p.run_predecessor_selftests(p.root)
    p.install()

    _check_authority_markers()
    _check_export_acceptance_is_exact()
    _check_no_omission_without_projection()
    _check_omission_covers_the_exact_tranche()
    _check_view_is_self_consistent()
    _check_partial_tranche_fails_closed()
    _check_entry_projection_is_wrapper_only()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_freeze_still_symmetric()

    print("wepld v33 S2 pre-tranche view repair self-tests: PASS")
