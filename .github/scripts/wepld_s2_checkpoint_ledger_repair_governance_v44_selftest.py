#!/usr/bin/env python3
"""Self-tests for the v44 self-test-only repair of v43's positive oracle."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_ledger_repair_governance_v44_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v44 self-test overlay exceeds read bound: {path}")
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
                f"v44 self-test rejection came from the wrong cause: {label}: {exc}"
            )
        return
    base.fail(f"v44 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_V43_SELFTEST_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE":
        base.fail("v44 authority marker drift")
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
            base.fail(f"v44 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v44 repair must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v44 repair must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v44 repair must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v44 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v44 next authority gate drift")


def _check_no_target_moved() -> None:
    """v44 makes no functional changes at all - a documentation identity
    included."""
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v44 must inherit the documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v44 must inherit the exact two-path transition shape")
    if p.PRE_CHECKPOINT_BLOB != p.p.PRE_CHECKPOINT_BLOB:
        base.fail("v44 must inherit the PRE checkpoint unchanged")
    if p.PRE_LEDGER_BLOB != p.p.PRE_LEDGER_BLOB:
        base.fail("v44 must inherit the PRE ledger unchanged")
    if p.FINAL_CHECKPOINT_BLOB != p.p.FINAL_CHECKPOINT_BLOB:
        base.fail("v44 must inherit v43's corrected checkpoint target unchanged")
    if p.FINAL_LEDGER_BLOB != p.p.FINAL_LEDGER_BLOB:
        base.fail("v44 must inherit v43's corrected ledger target unchanged")
    real_checkpoint = p._v37.FINAL_CHECKPOINT_BLOB
    real_ledger = p._v37.FINAL_LEDGER_BLOB
    if real_checkpoint != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v44 must not move the live checkpoint binding")
    if real_ledger != p.FINAL_LEDGER_BLOB:
        base.fail("v44 must not move the live ledger binding")


def _check_docs_transition_rejects_drifted_checkpoint() -> None:
    """Negative and positive oracle for `docs_transition`, fully independent
    of whatever documentation content the checked-out tree happens to carry.

    v43's own version of this oracle passed `p.raw_root` directly as the
    *base* argument, assuming its checkpoint/ledger bytes always equal
    PRE_CHECKPOINT_BLOB/PRE_LEDGER_BLOB. That held when v43's self-test ran
    against v43's own branch (no documentation change in that tree), but not
    against any real candidate that itself carries the corrected FINAL
    documentation content - exactly PR #263's shape, and exactly the
    scenario this whole successor chain exists to admit. Reproduced
    directly: v43's self-test, run against PR #263's rebased tree, failed
    with "v37 documentation transition base bytes drifted" - not the real
    admission logic (`s1-admission-integrity` genuinely succeeded on that
    exact candidate), but v43's own self-test asserting a false property
    about `raw_root`.

    This version temporarily rebinds v37's live PRE_CHECKPOINT_BLOB/
    PRE_LEDGER_BLOB *and* FINAL_CHECKPOINT_BLOB/FINAL_LEDGER_BLOB to match
    fully synthetic content it constructs itself, so neither the base nor
    the candidate depends on what `raw_root` actually contains.
    """
    drifted_checkpoint = b"# v44 self-test synthetic WRONG checkpoint\n"
    view = OverlayView(p.raw_root, {p.CHECKPOINT: drifted_checkpoint})
    _expect_failure(
        "docs_transition accepting a checkpoint that matches no recognized identity",
        lambda: p._v37.docs_transition(view, p.raw_root),
        "bytes drifted",
    )

    synthetic_pre_checkpoint = b"# v44 self-test synthetic PRE checkpoint\n"
    synthetic_pre_ledger = b"# v44 self-test synthetic PRE ledger\n"
    synthetic_final_checkpoint = b"# v44 self-test synthetic FINAL checkpoint\n"
    synthetic_final_ledger = b"# v44 self-test synthetic FINAL ledger\n"
    synthetic_pre_checkpoint_blob = p.V25.blob(synthetic_pre_checkpoint)
    synthetic_pre_ledger_blob = p.V25.blob(synthetic_pre_ledger)
    synthetic_final_checkpoint_blob = p.V25.blob(synthetic_final_checkpoint)
    synthetic_final_ledger_blob = p.V25.blob(synthetic_final_ledger)
    synthetic_blobs = {
        synthetic_pre_checkpoint_blob,
        synthetic_pre_ledger_blob,
        synthetic_final_checkpoint_blob,
        synthetic_final_ledger_blob,
    }
    if len(synthetic_blobs) != 4:
        base.fail("v44 self-test synthetic PRE/FINAL identities collided with each other")

    v37 = p._v37
    saved_pre_checkpoint = v37.PRE_CHECKPOINT_BLOB
    saved_pre_ledger = v37.PRE_LEDGER_BLOB
    saved_final_checkpoint = v37.FINAL_CHECKPOINT_BLOB
    saved_final_ledger = v37.FINAL_LEDGER_BLOB
    v37.PRE_CHECKPOINT_BLOB = synthetic_pre_checkpoint_blob
    v37.PRE_LEDGER_BLOB = synthetic_pre_ledger_blob
    v37.FINAL_CHECKPOINT_BLOB = synthetic_final_checkpoint_blob
    v37.FINAL_LEDGER_BLOB = synthetic_final_ledger_blob
    try:
        synthetic_base = OverlayView(
            p.raw_root,
            {p.CHECKPOINT: synthetic_pre_checkpoint, p.LEDGER: synthetic_pre_ledger},
        )
        synthetic_candidate = OverlayView(
            p.raw_root,
            {p.CHECKPOINT: synthetic_final_checkpoint, p.LEDGER: synthetic_final_ledger},
        )
        try:
            p._v37.docs_transition(synthetic_candidate, synthetic_base)
        except base.PolicyError as exc:
            base.fail(
                "v44 docs_transition must accept a candidate/base pair whose "
                f"checkpoint/ledger bytes genuinely match the live PRE/FINAL identity: {exc}"
            )
    finally:
        v37.PRE_CHECKPOINT_BLOB = saved_pre_checkpoint
        v37.PRE_LEDGER_BLOB = saved_pre_ledger
        v37.FINAL_CHECKPOINT_BLOB = saved_final_checkpoint
        v37.FINAL_LEDGER_BLOB = saved_final_ledger

    if (
        v37.PRE_CHECKPOINT_BLOB != saved_pre_checkpoint
        or v37.PRE_LEDGER_BLOB != saved_pre_ledger
        or v37.FINAL_CHECKPOINT_BLOB != saved_final_checkpoint
        or v37.FINAL_LEDGER_BLOB != saved_final_ledger
    ):
        base.fail("v44 self-test left the live checkpoint/ledger pin moved")


def _check_v43_wraps_still_installed() -> None:
    """v44 makes no functional changes - every one of v43's six wrapped v40
    attributes must still be superseded, exactly as v43 left them."""
    for attr_name in p.p._NARROWED_V40_ATTRS:
        wrapped = getattr(p.p._V40, attr_name)
        if wrapped is p.p._ORIGINAL_V40_ATTR_FUNCTIONS[attr_name]:
            base.fail(f"v44 lost v43's wrap of v40's {attr_name}")


def _check_admission_cascade_leaves_everything_restored() -> None:
    """After a real `files()` call over the real tree, every wrapped v40
    attribute and the six narrow call sites must be exactly what they were
    before."""
    v37 = p._v37
    real_checkpoint = v37.FINAL_CHECKPOINT_BLOB
    real_ledger = v37.FINAL_LEDGER_BLOB

    p.files(p.raw_root)

    if v37.FINAL_CHECKPOINT_BLOB != real_checkpoint or v37.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v44 admission cascade left the live pin moved after returning")
    for module, name in p.p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p.p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v44 narrow resting-view call site left wrapped after the admission "
                f"cascade: {module.__name__}.{name}"
            )
    if p.p._V40._with_v39_resting_view is not p.p._with_v39_resting_view_original:
        base.fail("v44 left v40's _with_v39_resting_view reference permanently replaced")
    for attr_name in p.p._NARROWED_V40_ATTRS:
        if getattr(p.p._V40, attr_name) is p.p._ORIGINAL_V40_ATTR_FUNCTIONS[attr_name]:
            base.fail(f"v44 lost its wrap of v40's {attr_name} after the admission cascade")


def _check_predecessor_is_exact() -> None:
    p.req_v43(p.raw_root)
    if p.V43_P_BLOB != "7be3076b0f6522e3ec1fb064b04ba497eb70a284":
        base.fail("v44 frozen v43 integrity identity drift")
    if p.V43_T_BLOB != "49d388068824ee466738dccadbbd9e131bc90ff9":
        base.fail("v44 frozen v43 self-test identity drift")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v44 workflow projection does not reverse to v43: {path}")
        if p._V44_ENTRYPOINT in data:
            base.fail(f"v44 workflow projection left a v44 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V44_ENTRYPOINT,
        b"wepld_unknown_v43_selftest_repair_entrypoint.py",
        1,
    )
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
        "v44 workflow entrypoint count drifted",
    )


def _check_workflow_projection_rejects_extra_content() -> None:
    padded = p.raw_root.read_bytes(p.AW, base.MAX_POLICY_FILE_BYTES) + b"\n# smuggled\n"
    view = OverlayView(p.raw_root, {p.AW: padded})
    _expect_failure(
        "workflow carries content beyond the entrypoint migration",
        lambda: p._workflow_predecessor_projection(view),
        "v44 workflow does not reverse to exact canonical v43 predecessor",
    )


def _check_bootstrap_scope_is_closed() -> None:
    expected = frozenset({p.P, p.T, p.FW, p.AW})
    if p.BOOT != expected:
        base.fail(f"v44 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v44 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v44 bootstrap must not carry any documentation transition")


def _check_bootstrap_delta_rejects_third_path() -> None:
    """The bootstrap delta must be exactly the four boot files, never a fifth."""
    projected_workflows = p._v43_workflow_projection(p.raw_root)

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
        base.fail("v44 self-test bootstrap-base fixture is not recognized as a boot base")

    changed = p.V25.changed(p.V25.v24.v23, valid_candidate, _BootBase())
    if changed != p.BOOT:
        base.fail(
            f"v44 self-test valid-candidate delta is not exactly p.BOOT: {sorted(changed)}"
        )

    try:
        p.delta(valid_candidate, _BootBase())
    except base.PolicyError as exc:
        base.fail(f"v44 bootstrap delta must accept exactly the four boot files: {exc}")

    _expect_failure(
        "bootstrap delta carrying a fifth (unauthorized) path",
        lambda: p.delta(smuggled_candidate, _BootBase()),
        "v44 bootstrap delta must be exactly two v44 policy files plus two integrity workflows",
    )


def _check_predecessor_package_exactness_rejects_drift() -> None:
    """v44 requires exactly the frozen v43 package; any drift must fail closed."""
    drifted_view = OverlayView(
        p.raw_root,
        {p.p.P: p.raw_root.read_bytes(p.p.P, base.MAX_POLICY_FILE_BYTES) + b"\n# drift\n"},
    )
    _expect_failure(
        "predecessor v43 integrity file drifted",
        lambda: p.req_v43(drifted_view),
        "frozen v43 predecessor drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_no_target_moved()
    _check_docs_transition_rejects_drifted_checkpoint()
    _check_v43_wraps_still_installed()
    _check_admission_cascade_leaves_everything_restored()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()
    _check_bootstrap_delta_rejects_third_path()
    _check_predecessor_package_exactness_rejects_drift()

    print(
        "wepld v44 v43-selftest-only repair "
        "self-tests: PASS"
    )
