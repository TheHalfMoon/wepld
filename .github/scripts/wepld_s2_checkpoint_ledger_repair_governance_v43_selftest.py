#!/usr/bin/env python3
"""Self-tests for the v43 remaining resting-view scope repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_ledger_repair_governance_v43_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v43 self-test overlay exceeds read bound: {path}")
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


def _expect_failure(label: str, action: Any, expected: str) -> None:
    """Assert `action` raises PolicyError, and that it raised for the expected
    reason - not merely that some PolicyError, from any cause, was raised.
    """
    try:
        action()
    except base.PolicyError as exc:
        if expected not in str(exc):
            base.fail(
                f"v43 self-test rejection came from the wrong cause: {label}: {exc}"
            )
        return
    base.fail(f"v43 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_REMAINING_RESTING_VIEW_SCOPE_REPAIR_ONLY":
        base.fail("v43 authority marker drift")
    for value, label in (
        (p.GIT_PROCESS_ADMISSION, "Git process admission"),
        (p.EXTERNAL_PROCESS_AUTHORITY, "external process authority"),
        (p.GIT_EXECUTION_AUTHORITY, "Git execution authority"),
        (p.NETWORK_AUTHORITY, "network authority"),
        (p.MODEL_PROVIDER_EXECUTION, "model/provider execution"),
        (p.DOCTOR_CLI_AUTHORITY, "Doctor/CLI authority"),
        (p.S3_PLUS_AUTHORITY, "S3+ authority"),
    ):
        if value != "NONE":
            base.fail(f"v43 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v43 scope repair must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v43 scope repair must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v43 scope repair must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v43 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v43 next authority gate drift")


def _check_no_target_moved() -> None:
    """v43 corrects five resting-view scoping defects, not a documentation
    identity."""
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v43 must inherit the documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v43 must inherit the exact two-path transition shape")
    if p.PRE_CHECKPOINT_BLOB != p.p.PRE_CHECKPOINT_BLOB:
        base.fail("v43 must inherit the PRE checkpoint unchanged")
    if p.PRE_LEDGER_BLOB != p.p.PRE_LEDGER_BLOB:
        base.fail("v43 must inherit the PRE ledger unchanged")
    if p.FINAL_CHECKPOINT_BLOB != p.p.FINAL_CHECKPOINT_BLOB:
        base.fail("v43 must inherit v42's corrected checkpoint target unchanged")
    if p.FINAL_LEDGER_BLOB != p.p.FINAL_LEDGER_BLOB:
        base.fail("v43 must inherit v42's corrected ledger target unchanged")
    real_checkpoint = p._v37.FINAL_CHECKPOINT_BLOB
    real_ledger = p._v37.FINAL_LEDGER_BLOB
    if real_checkpoint != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v43 must not move the live checkpoint binding")
    if real_ledger != p.FINAL_LEDGER_BLOB:
        base.fail("v43 must not move the live ledger binding")


def _check_docs_transition_rejects_drifted_checkpoint() -> None:
    """Negative oracle for the actual defect, exercised directly against
    `docs_transition` - the exact function root-caused against PR #263 -
    rather than through the full `delta()` cascade: `V25.changed()` walks the
    entire real repository tree via per-path `tree_identity()` calls that
    shell out to `git`, which is fast on real CI (already proven by every
    prior successor's own `verify-candidate-local` qualification step) but
    prohibitively slow, and observed to hang outright, against this
    repository from a local Windows interactive shell - an environmental
    difference, not a defect in `delta()` itself. `delta()`'s own accept path
    for a real candidate is exercised by CI qualification instead; see the PR
    record for the run ID.

    An `OverlayView` that does not also override `tree_identity` (this
    project's own recurring pitfall - see the `_check_bootstrap_delta_
    rejects_third_path` fix in the v42 predecessor) would make every path
    outside the overlay compare identity-equal to `raw_root`, so this fixture
    does not rely on identity-based short-circuiting at all: it calls
    `docs_transition` directly rather than a full-tree diff.
    """
    drifted_checkpoint = b"# v43 self-test synthetic WRONG checkpoint\n"
    view = OverlayView(p.raw_root, {p.CHECKPOINT: drifted_checkpoint})
    _expect_failure(
        "docs_transition accepting a checkpoint that matches no recognized identity",
        lambda: p._v37.docs_transition(view, p.raw_root),
        "bytes drifted",
    )

    # Positive oracle: `raw_root` (main, as checked out) still carries the
    # PRE-transition documentation - PR #263, which lands the reviewed FINAL
    # bytes, has not merged yet - so `raw_root` is a valid *base* but can
    # never itself be a valid *candidate* for `docs_transition`. Rather than
    # fetch PR #261's real reviewed bytes (which would need a `git`
    # subprocess call - unprecedented in any self-test in this codebase, and
    # in tension with this successor's own declared GIT_EXECUTION_AUTHORITY =
    # NONE), this uses v41's own established technique from `_check_widening_
    # chain_still_discriminates`: temporarily rebind v37's live
    # FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB to match synthetic content this
    # test fully controls, so no external fetch of any kind is needed to
    # prove `docs_transition` accepts a candidate whose bytes genuinely equal
    # whatever the live target currently is.
    synthetic_checkpoint = b"# v43 self-test synthetic FINAL checkpoint\n"
    synthetic_ledger = b"# v43 self-test synthetic FINAL ledger\n"
    synthetic_checkpoint_blob = p.V25.blob(synthetic_checkpoint)
    synthetic_ledger_blob = p.V25.blob(synthetic_ledger)
    if synthetic_checkpoint_blob == p.PRE_CHECKPOINT_BLOB or synthetic_ledger_blob == p.PRE_LEDGER_BLOB:
        base.fail("v43 self-test synthetic FINAL identity collided with the real PRE identity")

    v37 = p._v37
    saved_checkpoint = v37.FINAL_CHECKPOINT_BLOB
    saved_ledger = v37.FINAL_LEDGER_BLOB
    v37.FINAL_CHECKPOINT_BLOB = synthetic_checkpoint_blob
    v37.FINAL_LEDGER_BLOB = synthetic_ledger_blob
    try:
        final_candidate = OverlayView(
            p.raw_root, {p.CHECKPOINT: synthetic_checkpoint, p.LEDGER: synthetic_ledger}
        )
        try:
            p._v37.docs_transition(final_candidate, p.raw_root)
        except base.PolicyError as exc:
            base.fail(
                "v43 docs_transition must accept a candidate whose checkpoint/ledger "
                f"bytes genuinely match the live FINAL identity: {exc}"
            )
    finally:
        v37.FINAL_CHECKPOINT_BLOB = saved_checkpoint
        v37.FINAL_LEDGER_BLOB = saved_ledger

    if v37.FINAL_CHECKPOINT_BLOB != saved_checkpoint or v37.FINAL_LEDGER_BLOB != saved_ledger:
        base.fail("v43 self-test left the live checkpoint/ledger pin moved")


def _check_all_five_attrs_are_wrapped() -> None:
    """Every one of the five remaining v40 attributes must actually be
    superseded by `_narrow_wrap`'s output, not left as the original."""
    for attr_name in p._NARROWED_V40_ATTRS:
        wrapped = getattr(p._V40, attr_name)
        if wrapped is p._ORIGINAL_V40_ATTR_FUNCTIONS[attr_name]:
            base.fail(f"v43 did not wrap v40's {attr_name}")


def _check_admission_cascade_leaves_everything_restored() -> None:
    """After a real `files()` call over the real tree (see the module
    docstring on `_check_docs_transition_rejects_drifted_checkpoint` for why
    `delta()` itself is not exercised locally here), every wrapped v40
    attribute and the six narrow call sites must be exactly what they were
    before."""
    v37 = p._v37
    real_checkpoint = v37.FINAL_CHECKPOINT_BLOB
    real_ledger = v37.FINAL_LEDGER_BLOB

    p.files(p.raw_root)

    if v37.FINAL_CHECKPOINT_BLOB != real_checkpoint or v37.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v43 admission cascade left the live pin moved after returning")
    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v43 narrow resting-view call site left wrapped after the admission "
                f"cascade: {module.__name__}.{name}"
            )
    if p._V40._with_v39_resting_view is not p._with_v39_resting_view_original:
        base.fail("v43 left v40's _with_v39_resting_view reference permanently replaced")
    for attr_name in p._NARROWED_V40_ATTRS:
        if getattr(p._V40, attr_name) is p._ORIGINAL_V40_ATTR_FUNCTIONS[attr_name]:
            base.fail(f"v43 lost its wrap of v40's {attr_name} after the admission cascade")


def _check_predecessor_is_exact() -> None:
    p.req_v42(p.raw_root)
    if p.V42_P_BLOB != "598dda532393aaf2927ea91a745169b8f90e3987":
        base.fail("v43 frozen v42 integrity identity drift")
    if p.V42_T_BLOB != "9691772fb016b8b4c21b92c4921c7e9799d44821":
        base.fail("v43 frozen v42 self-test identity drift")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v43 workflow projection does not reverse to v42: {path}")
        if p._V43_ENTRYPOINT in data:
            base.fail(f"v43 workflow projection left a v43 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V43_ENTRYPOINT,
        b"wepld_unknown_remaining_scope_repair_entrypoint.py",
        1,
    )
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
        "v43 workflow entrypoint count drifted",
    )


def _check_workflow_projection_rejects_extra_content() -> None:
    padded = p.raw_root.read_bytes(p.AW, base.MAX_POLICY_FILE_BYTES) + b"\n# smuggled\n"
    view = OverlayView(p.raw_root, {p.AW: padded})
    _expect_failure(
        "workflow carries content beyond the entrypoint migration",
        lambda: p._workflow_predecessor_projection(view),
        "v43 workflow does not reverse to exact canonical v42 predecessor",
    )


def _check_bootstrap_scope_is_closed() -> None:
    expected = frozenset({p.P, p.T, p.FW, p.AW})
    if p.BOOT != expected:
        base.fail(f"v43 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v43 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v43 bootstrap must not carry any documentation transition")


def _check_bootstrap_delta_rejects_third_path() -> None:
    """The bootstrap delta must be exactly the four boot files, never a fifth."""
    projected_workflows = p._v42_workflow_projection(p.raw_root)

    class _ExtraPathView:
        def __init__(self, extra: dict[str, bytes]) -> None:
            self._extra = extra

        def read_bytes(self, path: str, max_bytes: int) -> bytes:
            if path in self._extra:
                return self._extra[path]
            return p.raw_root.read_bytes(path, max_bytes)

        def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
            return self.read_bytes(path, limit).decode("utf-8", errors="strict")

        def entries(self) -> Any:
            base_paths = {entry.path for entry in p.raw_root.entries()}
            result = list(p.raw_root.entries())
            for name in self._extra:
                if name not in base_paths:
                    result.append(base.TrackedEntry(mode="100644", path=name))
            return result

        def tree_identity(self, path: str) -> Any:
            return (id(self), path)

        def __getattr__(self, name: str) -> Any:
            return getattr(p.raw_root, name)

    boot_files = {
        path: p.raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES) for path in p.BOOT
    }
    smuggled_path = "docs/canonical/UNAUTHORIZED_THIRD_PATH.md"
    valid_candidate = _ExtraPathView(dict(boot_files))
    smuggled_candidate = _ExtraPathView({**boot_files, smuggled_path: b"# smuggled\n"})

    class _BootBase:
        def read_bytes(self, path: str, max_bytes: int) -> bytes:
            if path in projected_workflows:
                return projected_workflows[path]
            return p.raw_root.read_bytes(path, max_bytes)

        def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
            return self.read_bytes(path, limit).decode("utf-8", errors="strict")

        def entries(self) -> Any:
            excluded = set(p.POLICY_FILES)
            return [entry for entry in p.raw_root.entries() if entry.path not in excluded]

        def tree_identity(self, path: str) -> Any:
            return (id(self), path)

        def __getattr__(self, name: str) -> Any:
            return getattr(p.raw_root, name)

    if not p.bootbase(_BootBase()):
        base.fail("v43 self-test bootstrap-base fixture is not recognized as a boot base")

    changed = p.V25.changed(p.V25.v24.v23, valid_candidate, _BootBase())
    if changed != p.BOOT:
        base.fail(
            f"v43 self-test valid-candidate delta is not exactly p.BOOT: {sorted(changed)}"
        )

    try:
        p.delta(valid_candidate, _BootBase())
    except base.PolicyError as exc:
        base.fail(f"v43 bootstrap delta must accept exactly the four boot files: {exc}")

    _expect_failure(
        "bootstrap delta carrying a fifth (unauthorized) path",
        lambda: p.delta(smuggled_candidate, _BootBase()),
        "v43 bootstrap delta must be exactly two v43 policy files plus two integrity workflows",
    )


def _check_predecessor_package_exactness_rejects_drift() -> None:
    """v43 requires exactly the frozen v42 package; any drift must fail closed."""
    drifted_view = OverlayView(
        p.raw_root,
        {p.p.P: p.raw_root.read_bytes(p.p.P, base.MAX_POLICY_FILE_BYTES) + b"\n# drift\n"},
    )
    _expect_failure(
        "predecessor v42 integrity file drifted",
        lambda: p.req_v42(drifted_view),
        "frozen v42 predecessor drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_no_target_moved()
    _check_docs_transition_rejects_drifted_checkpoint()
    _check_all_five_attrs_are_wrapped()
    _check_admission_cascade_leaves_everything_restored()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()
    _check_bootstrap_delta_rejects_third_path()
    _check_predecessor_package_exactness_rejects_drift()

    print(
        "wepld v43 remaining resting-view scope repair "
        "self-tests: PASS"
    )
