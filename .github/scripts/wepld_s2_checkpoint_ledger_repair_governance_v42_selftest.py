#!/usr/bin/env python3
"""Self-tests for the v42 files() resting-view scope repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_ledger_repair_governance_v42_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v42 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return self._view.entries()

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
                f"v42 self-test rejection came from the wrong cause: {label}: {exc}"
            )
        return
    base.fail(f"v42 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_FILES_RESTING_VIEW_SCOPE_REPAIR_ONLY":
        base.fail("v42 authority marker drift")
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
            base.fail(f"v42 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v42 scope repair must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v42 scope repair must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v42 scope repair must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v42 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v42 next authority gate drift")


def _check_no_target_moved() -> None:
    """v42 corrects a second files()-verification scoping defect, not a
    documentation identity."""
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v42 must inherit the documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v42 must inherit the exact two-path transition shape")
    if p.PRE_CHECKPOINT_BLOB != p.p.PRE_CHECKPOINT_BLOB:
        base.fail("v42 must inherit the PRE checkpoint unchanged")
    if p.PRE_LEDGER_BLOB != p.p.PRE_LEDGER_BLOB:
        base.fail("v42 must inherit the PRE ledger unchanged")
    if p.FINAL_CHECKPOINT_BLOB != p.p.FINAL_CHECKPOINT_BLOB:
        base.fail("v42 must inherit v41's corrected checkpoint target unchanged")
    if p.FINAL_LEDGER_BLOB != p.p.FINAL_LEDGER_BLOB:
        base.fail("v42 must inherit v41's corrected ledger target unchanged")
    v37 = p._v37
    if v37.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v42 must not move the live checkpoint binding")
    if v37.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v42 must not move the live ledger binding")


def _check_files_cascade_accepts_real_tree_and_rejects_drifted_ledger() -> None:
    """Positive and negative oracle for the actual defect, exercised through the
    exact entrypoint real CI invokes for an ordinary candidate (`files()`, reached
    from `verify-candidate-local`/`verify-remote` - never from `selftest`, which is
    exactly why v41's fix to `run_predecessor_selftests` left this gap open).

    Positive: the real, unmodified repository tree - whose Build Learning ledger
    genuinely carries v40/v41's corrected identity - must pass `files()` cleanly.
    This is the direct, exact-shape repro of PR #263 failing with "S1-016 Build
    Learning bytes drifted" before this fix.

    Negative: a tree whose ledger content matches nothing recognized must still
    fail closed with that exact message, proving the repair does not silently
    defeat the acceptance check it was careful not to touch.
    """
    try:
        p.files(p.raw_root)
    except base.PolicyError as exc:
        base.fail(f"v42 files() must accept the real, unmodified tree: {exc}")

    drifted_ledger = b"# v42 self-test synthetic WRONG Build Learning ledger\n"
    view = OverlayView(p.raw_root, {p.LEDGER: drifted_ledger})
    _expect_failure(
        "files() cascade accepting a tree whose ledger matches no recognized identity",
        lambda: p.files(view),
        "S1-016 Build Learning bytes drifted",
    )


def _check_narrow_call_sites_still_reconcile_via_direct_probe() -> None:
    """Prove `_corrected_v40_files` (production code, invoked through the real
    `files()` entrypoint - not a synthetic reimplementation of its wrap/unwrap
    logic) presents v39's resting pair to whichever of the six narrow call sites
    a real `files()` cascade actually reaches, and restores the real pair - and
    leaves every site correctly unwrapped - once it returns.

    Each of the six real functions is temporarily replaced with a thin recorder
    that captures v37's live pin at the moment it is called, then delegates to
    the original; `_corrected_v40_files` wraps *those* recorders (whatever it
    finds bound at call time), so what gets observed is genuinely what
    production code presents to them, not a value this test constructed itself.
    """
    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v42 narrow resting-view call site already left wrapped before any "
                f"call: {module.__name__}.{name}"
            )

    v37 = p._v37
    real_checkpoint = v37.FINAL_CHECKPOINT_BLOB
    real_ledger = v37.FINAL_LEDGER_BLOB
    v39_resting_pair = (p.p.p.V39_FINAL_CHECKPOINT_BLOB, p.p.p.V39_FINAL_LEDGER_BLOB)

    # None of the six narrow call sites is actually reached by v40's own
    # `files()` body for this repository's tree shape (verified: a version of
    # this check that only observed sites the cascade happened to call recorded
    # nothing). That's a fact about *this* cascade, not evidence the wraps are
    # unnecessary - `_check_files_cascade_accepts_real_tree_and_rejects_
    # drifted_ledger` already proves v40's real logic still succeeds/fails
    # correctly either way. What this check proves instead: when
    # `_corrected_v40_files` (production code, not a reimplementation) installs
    # its wraps and something *does* call into a wrapped site during that
    # window, the site genuinely observes v39's resting pair. It exercises this
    # by substituting `_V40_ORIGINAL_FILES` with a stand-in that runs inside
    # `_corrected_v40_files`'s own dynamic extent (after its wraps are
    # installed, before they're restored) and calls the first narrow site
    # directly - itself first substituted with a harmless stand-in, so the call
    # is safe regardless of that site's real preconditions.
    probe_site = p._NARROW_RESTING_VIEW_CALL_SITES[0]
    probe_module, probe_name = probe_site
    observed: list[tuple[str, str]] = []

    def _site_stand_in(*args: Any, **kwargs: Any) -> None:
        observed.append((v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB))

    original_files_body = p._V40_ORIGINAL_FILES

    def _files_body_that_also_probes(view: Any) -> Any:
        getattr(probe_module, probe_name)()
        return original_files_body(view)

    saved_probe_site = getattr(probe_module, probe_name)
    setattr(probe_module, probe_name, _site_stand_in)
    p._V40_ORIGINAL_FILES = _files_body_that_also_probes
    try:
        p.files(p.raw_root)
    finally:
        p._V40_ORIGINAL_FILES = original_files_body
        setattr(probe_module, probe_name, saved_probe_site)

    if observed != [v39_resting_pair]:
        base.fail(f"v42 narrow call site did not observe v39's resting pair: {observed}")
    if v37.FINAL_CHECKPOINT_BLOB != real_checkpoint or v37.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v42 narrow resting-view wrapper did not restore the real pair")

    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v42 narrow resting-view call site left wrapped (or cross-restored to "
                f"a different original) after the probe: {module.__name__}.{name}"
            )


def _check_files_call_leaves_everything_restored() -> None:
    """After a real `files()` cascade over the real tree, the six narrow call
    sites and v40's own `_with_v39_resting_view` reference must be exactly what
    they were before the call - proving `_corrected_v40_files` restores its own
    state in every case its actual production call sites exercise, not merely in
    the synthetic probe above.
    """
    v37 = p._v37
    real_checkpoint = v37.FINAL_CHECKPOINT_BLOB
    real_ledger = v37.FINAL_LEDGER_BLOB

    p.files(p.raw_root)

    if v37.FINAL_CHECKPOINT_BLOB != real_checkpoint or v37.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v42 files() cascade left the live pin moved after returning")
    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v42 narrow resting-view call site left wrapped (or cross-restored to "
                f"a different original) after files(): {module.__name__}.{name}"
            )
    if p.p.p._with_v39_resting_view is not p._with_v39_resting_view_original:
        base.fail("v42 left v40's _with_v39_resting_view reference permanently replaced")


def _check_predecessor_is_exact() -> None:
    p.req_v41(p.raw_root)
    if p.V41_P_BLOB != "951e3210a90e19c8c09b708ab9dea7dbbd2f04cc":
        base.fail("v42 frozen v41 integrity identity drift")
    if p.V41_T_BLOB != "6376c146f6d4fd4f96dc8ad11741a994ada33325":
        base.fail("v42 frozen v41 self-test identity drift")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v42 workflow projection does not reverse to v41: {path}")
        if p._V42_ENTRYPOINT in data:
            base.fail(f"v42 workflow projection left a v42 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V42_ENTRYPOINT,
        b"wepld_unknown_files_scope_repair_entrypoint.py",
        1,
    )
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
        "v42 workflow entrypoint count drifted",
    )


def _check_workflow_projection_rejects_extra_content() -> None:
    padded = p.raw_root.read_bytes(p.AW, base.MAX_POLICY_FILE_BYTES) + b"\n# smuggled\n"
    view = OverlayView(p.raw_root, {p.AW: padded})
    _expect_failure(
        "workflow carries content beyond the entrypoint migration",
        lambda: p._workflow_predecessor_projection(view),
        "v42 workflow does not reverse to exact canonical v41 predecessor",
    )


def _check_bootstrap_scope_is_closed() -> None:
    expected = frozenset({p.P, p.T, p.FW, p.AW})
    if p.BOOT != expected:
        base.fail(f"v42 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v42 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v42 bootstrap must not carry any documentation transition")


def _check_bootstrap_delta_rejects_third_path() -> None:
    """The bootstrap delta must be exactly the four boot files, never a fifth.

    `_BootBase` must serve the *v41-projected* (pre-migration) workflow bytes for
    `FW`/`AW`, not the real tree's v42-era bytes - otherwise a genuine candidate's
    workflow files never appear in the changed set at all (their bytes match the
    base's raw, unprojected copy), the computed delta collapses to just `{P, T}`,
    and the fifth-path oracle below would reject for that reason - `{P, T}` already
    differs from and intersects `p.BOOT` - regardless of whether a fifth path was
    ever added. Serving the projected bytes makes the four-file delta genuinely
    equal `p.BOOT`, so the positive assertion proves the valid case is accepted and
    the negative assertion proves the fifth path specifically is what triggers
    rejection.
    """
    projected_workflows = p._v41_workflow_projection(p.raw_root)

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
            # `_changed_paths` only falls back to comparing `read_bytes` when
            # `tree_identity` differs between candidate and base; both fixtures'
            # `__getattr__` would otherwise delegate identically to
            # `p.raw_root.tree_identity`, so the two would always compare equal
            # and the byte comparison this test depends on would never run. A
            # per-instance identity forces the real comparison every time.
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
        base.fail("v42 self-test bootstrap-base fixture is not recognized as a boot base")

    changed = p.V25.changed(p.V25.v24.v23, valid_candidate, _BootBase())
    if changed != p.BOOT:
        base.fail(
            f"v42 self-test valid-candidate delta is not exactly p.BOOT: {sorted(changed)}"
        )

    try:
        p.delta(valid_candidate, _BootBase())
    except base.PolicyError as exc:
        base.fail(f"v42 bootstrap delta must accept exactly the four boot files: {exc}")

    _expect_failure(
        "bootstrap delta carrying a fifth (unauthorized) path",
        lambda: p.delta(smuggled_candidate, _BootBase()),
        "v42 bootstrap delta must be exactly two v42 policy files plus two integrity workflows",
    )


def _check_predecessor_package_exactness_rejects_drift() -> None:
    """v42 requires exactly the frozen v41 package; any drift must fail closed."""
    drifted_view = OverlayView(
        p.raw_root,
        {p.p.P: p.raw_root.read_bytes(p.p.P, base.MAX_POLICY_FILE_BYTES) + b"\n# drift\n"},
    )
    _expect_failure(
        "predecessor v41 integrity file drifted",
        lambda: p.req_v41(drifted_view),
        "frozen v41 predecessor drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_no_target_moved()
    _check_files_cascade_accepts_real_tree_and_rejects_drifted_ledger()
    _check_narrow_call_sites_still_reconcile_via_direct_probe()
    _check_files_call_leaves_everything_restored()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()
    _check_bootstrap_delta_rejects_third_path()
    _check_predecessor_package_exactness_rejects_drift()

    print(
        "wepld v42 files() resting-view scope repair "
        "self-tests: PASS"
    )
