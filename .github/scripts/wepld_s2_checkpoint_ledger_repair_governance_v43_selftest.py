#!/usr/bin/env python3
"""Self-tests for the v43 delta resting-view scope repair."""

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

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any, expected: str) -> None:
    try:
        action()
    except base.PolicyError as exc:
        if expected not in str(exc):
            base.fail(f"v43 self-test rejection came from the wrong cause: {label}: {exc}")
        return
    base.fail(f"v43 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_DELTA_RESTING_VIEW_SCOPE_REPAIR_ONLY":
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
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v43 must inherit the documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v43 must inherit the exact two-path transition shape")
    for name in (
        "PRE_CHECKPOINT_BLOB",
        "PRE_LEDGER_BLOB",
        "FINAL_CHECKPOINT_BLOB",
        "FINAL_LEDGER_BLOB",
    ):
        if getattr(p, name) != getattr(p.p, name):
            base.fail(f"v43 must inherit {name} unchanged")
    if p._v37.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v43 must not move the live checkpoint binding")
    if p._v37.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v43 must not move the live ledger binding")


def _check_delta_scope_is_narrow_and_restored() -> None:
    if p._V40.delta is not p._corrected_v40_delta:
        base.fail("v43 corrected v40 delta binding is not installed")

    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v43 narrow resting-view call site already left wrapped before the probe: "
                f"{module.__name__}.{name}"
            )

    v37 = p._v37
    real_pair = (v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB)
    resting_pair = (p._V40.V39_FINAL_CHECKPOINT_BLOB, p._V40.V39_FINAL_LEDGER_BLOB)
    outer_observed: list[tuple[str, str]] = []
    narrow_observed: list[tuple[str, str]] = []

    probe_module, probe_name = p._NARROW_RESTING_VIEW_CALL_SITES[0]
    saved_probe_site = getattr(probe_module, probe_name)
    original_delta_body = p._V40_ORIGINAL_DELTA

    def _site_stand_in(*args: Any, **kwargs: Any) -> None:
        narrow_observed.append((v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB))

    def _delta_body_stand_in(candidate: Any, policy_base: Any) -> None:
        p._V40._with_v39_resting_view(
            lambda: outer_observed.append(
                (v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB)
            )
        )()
        getattr(probe_module, probe_name)()

    setattr(probe_module, probe_name, _site_stand_in)
    p._V40_ORIGINAL_DELTA = _delta_body_stand_in
    try:
        p._corrected_v40_delta(p.raw_root, p.raw_root)
    finally:
        p._V40_ORIGINAL_DELTA = original_delta_body
        setattr(probe_module, probe_name, saved_probe_site)

    if outer_observed != [real_pair]:
        base.fail(f"v43 broad v40 delta seam still presented v39 resting pins: {outer_observed}")
    if narrow_observed != [resting_pair]:
        base.fail(f"v43 narrow delta call site did not observe v39 resting pins: {narrow_observed}")
    if (v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB) != real_pair:
        base.fail("v43 delta scope repair did not restore the real documentation pair")
    if p._V40._with_v39_resting_view is not p._V40_RESTING_VIEW_ORIGINAL:
        base.fail("v43 delta scope repair left v40's resting-view helper replaced")
    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v43 narrow resting-view call site left wrapped after the probe: "
                f"{module.__name__}.{name}"
            )


def _check_delta_scope_restores_on_exception() -> None:
    v37 = p._v37
    real_pair = (v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB)
    original_delta_body = p._V40_ORIGINAL_DELTA

    def _boom(candidate: Any, policy_base: Any) -> None:
        raise RuntimeError("v43 synthetic delta failure")

    p._V40_ORIGINAL_DELTA = _boom
    try:
        try:
            p._corrected_v40_delta(p.raw_root, p.raw_root)
        except RuntimeError as exc:
            if str(exc) != "v43 synthetic delta failure":
                raise
        else:
            base.fail("v43 delta exception-restoration oracle did not raise")
    finally:
        p._V40_ORIGINAL_DELTA = original_delta_body

    if (v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB) != real_pair:
        base.fail("v43 delta exception path left the live documentation pair moved")
    if p._V40._with_v39_resting_view is not p._V40_RESTING_VIEW_ORIGINAL:
        base.fail("v43 delta exception path left v40's resting-view helper replaced")
    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) is not p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS[(module, name)]:
            base.fail(
                "v43 delta exception path left a narrow call site wrapped: "
                f"{module.__name__}.{name}"
            )


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
        b"wepld_unknown_delta_scope_repair_entrypoint.py",
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


def _check_bootstrap_delta_rejects_fifth_path() -> None:
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
    valid_candidate = _ExtraPathView(dict(boot_files))
    smuggled_path = "docs/canonical/UNAUTHORIZED_FIFTH_PATH.md"
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
    p.delta(valid_candidate, _BootBase())
    _expect_failure(
        "bootstrap delta carrying a fifth unauthorized path",
        lambda: p.delta(smuggled_candidate, _BootBase()),
        "v43 bootstrap delta must be exactly two v43 policy files plus two integrity workflows",
    )


def _check_predecessor_package_exactness_rejects_drift() -> None:
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
    _check_delta_scope_is_narrow_and_restored()
    _check_delta_scope_restores_on_exception()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()
    _check_bootstrap_delta_rejects_fifth_path()
    _check_predecessor_package_exactness_rejects_drift()

    print("wepld v43 delta resting-view scope repair self-tests: PASS")
