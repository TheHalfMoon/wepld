#!/usr/bin/env python3
"""Self-tests for the v44 v43-final-state fixture repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_v43_final_state_selftest_repair_v44_integrity as p


def _expect_failure(label: str, action: Any, expected: str) -> None:
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
    if p.AUTH != "S2_V43_FINAL_STATE_SELFTEST_FIXTURE_REPAIR_ONLY":
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
        base.fail("v44 fixture repair must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v44 fixture repair must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v44 fixture repair must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v44 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v44 next authority gate drift")


def _check_corrected_fixture_is_state_independent() -> None:
    # The repaired oracle synthesizes both PRE and FINAL sides and therefore must
    # succeed regardless of whether the checkout carrying the policy is itself on
    # PRE (canonical main before PR #263) or FINAL (PR #263 and eventual main).
    p._corrected_v43_docs_transition_selftest()


def _check_predecessor_selftest_patch_is_scoped() -> None:
    import wepld_s2_checkpoint_ledger_repair_governance_v43_selftest as v43_st

    original = v43_st._check_docs_transition_rejects_drifted_checkpoint
    p.run_predecessor_selftests()
    if v43_st._check_docs_transition_rejects_drifted_checkpoint is not original:
        base.fail("v44 left the v43 self-test function patched after the predecessor run")


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
        b"wepld_unknown_v43_fixture_repair_entrypoint.py",
        1,
    )
    view = p._OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
        "v44 workflow entrypoint count drifted",
    )


def _check_bootstrap_scope_is_closed() -> None:
    expected = frozenset({p.P, p.T, p.FW, p.AW})
    if p.BOOT != expected:
        base.fail(f"v44 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v44 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v44 bootstrap must not carry the documentation transition")


def _check_bootstrap_delta_rejects_fifth_path() -> None:
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
    valid_candidate = _ExtraPathView(dict(boot_files))
    smuggled_path = "docs/canonical/UNAUTHORIZED_V44_FIFTH_PATH.md"
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

    base_view = _BootBase()
    if not p.bootbase(base_view):
        base.fail("v44 self-test bootstrap-base fixture is not recognized as a boot base")
    changed = p.V25.changed(p.V25.v24.v23, valid_candidate, base_view)
    if changed != p.BOOT:
        base.fail(f"v44 valid bootstrap delta is not exactly p.BOOT: {sorted(changed)}")
    try:
        p.delta(valid_candidate, base_view)
    except base.PolicyError as exc:
        base.fail(f"v44 bootstrap delta must accept exactly the four boot files: {exc}")
    _expect_failure(
        "bootstrap delta carrying a fifth path",
        lambda: p.delta(smuggled_candidate, base_view),
        "v44 bootstrap delta must be exactly two v44 policy files plus two integrity workflows",
    )


def run() -> None:
    # Run once explicitly to prove the repair is sufficient for the whole predecessor
    # cascade, then install v44 and verify the v44-specific properties.
    _check_predecessor_selftest_patch_is_scoped()
    p.install()

    _check_authority_markers()
    _check_corrected_fixture_is_state_independent()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_bootstrap_scope_is_closed()
    _check_bootstrap_delta_rejects_fifth_path()

    print("wepld v44 v43-final-state self-test fixture repair: PASS")
