#!/usr/bin/env python3
"""Self-tests for the v67 self-test-only repair over v66."""

from __future__ import annotations

from typing import Any

import wepld_integrity as base
import wepld_s2_a009_selftest_repair_v67_integrity as p


def _check_authority_markers() -> None:
    if p.AUTH != "S2_A009_SELFTEST_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE":
        base.fail("v67 authority marker drift")
    if p.NEXT_AUTHORITY_GATE != p.q.NEXT_AUTHORITY_GATE:
        base.fail("v67 must not change the inherited next-authority gate")
    for name in p._INHERITED_AUTHORITY_NAMES:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v67 widened or changed inherited authority: {name}")
    for name, value in (
        ("NETWORK_AUTHORITY", p.NETWORK_AUTHORITY),
        ("MODEL_PROVIDER_EXECUTION", p.MODEL_PROVIDER_EXECUTION),
        ("S3_PLUS_AUTHORITY", p.S3_PLUS_AUTHORITY),
        ("GENERAL_SHELL_AUTHORITY", p.GENERAL_SHELL_AUTHORITY),
        ("ARBITRARY_PROCESS_AUTHORITY", p.ARBITRARY_PROCESS_AUTHORITY),
        ("PACKAGE_INSTALL_AUTHORITY", p.PACKAGE_INSTALL_AUTHORITY),
        ("PROJECT_NATIVE_COMMAND_EXECUTION", p.PROJECT_NATIVE_COMMAND_EXECUTION),
        ("GIT_MUTATION_AUTHORITY", p.GIT_MUTATION_AUTHORITY),
        ("SAFE_DIRECTORY_MUTATION_AUTHORITY", p.SAFE_DIRECTORY_MUTATION_AUTHORITY),
        ("REMEDIATION_EXECUTION_AUTHORITY", p.REMEDIATION_EXECUTION_AUTHORITY),
    ):
        if value != "NONE":
            base.fail(f"v67 must not grant {name}")


def _check_reopen_state_unchanged() -> None:
    if p.CHECKPOINT != p.q.CHECKPOINT:
        base.fail("v67 checkpoint path drift")
    if p.LEDGER != p.q.LEDGER:
        base.fail("v67 ledger path drift")
    if p.REOPEN_FILES != p.q.REOPEN_FILES:
        base.fail("v67 reopen path set drift")
    if p.EXACT_FROZEN_BLOBS != p.q.EXACT_FROZEN_BLOBS:
        base.fail("v67 must not move the inherited reopen pins")
    if p.S2_A009_BUILD_LEARNING_REOPEN_AUTHORITY != p.q.S2_A009_BUILD_LEARNING_REOPEN_AUTHORITY:
        base.fail("v67 must not change the inherited reopen authority marker")
    if p._reopen_available(p.raw_root) != p.q._reopen_available(p.raw_root):
        base.fail("v67 reopen-availability check disagrees with the inherited one")


def _check_embedded_pre_reopen_bytes() -> None:
    if p.V25.blob(p._PRE_REOPEN_CHECKPOINT_BYTES) != p.EXACT_FROZEN_BLOBS[p.CHECKPOINT]:
        base.fail("v67 embedded pre-reopen checkpoint bytes drift")
    if p.V25.blob(p._PRE_REOPEN_LEDGER_BYTES) != p.EXACT_FROZEN_BLOBS[p.LEDGER]:
        base.fail("v67 embedded pre-reopen ledger bytes drift")


def _check_predecessor_exact() -> None:
    p.req_v66(p.raw_root)
    if p.V66_P_BLOB != "1472cd04c6443231655f49f6a35a722e58ee4de4":
        base.fail("v67 frozen v66 integrity identity drift")
    if p.V66_T_BLOB != "ae8ffbaf8272e639da32ac81271bb85e22603cc1":
        base.fail("v67 frozen v66 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._project_for_v66(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v67 workflow projection does not reverse to exact v66: {path}")
        if p._V67_ENTRYPOINT in data:
            base.fail(f"v67 workflow projection left the v67 entrypoint: {path}")


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes], *, omitted: frozenset[str] = frozenset()) -> None:
        self._view = view
        self._replacements = replacements
        self._omitted = omitted

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v67 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        result = [entry for entry in self._view.entries() if entry.path not in self._omitted]
        known = {entry.path for entry in result}
        for path in self._replacements:
            if path not in known and path not in self._omitted:
                result.append(base.TrackedEntry(mode="100644", path=path))
        return result

    def tree_identity(self, path: str) -> Any:
        return (id(self), path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any) -> None:
    try:
        action()
    except (base.PolicyError, FileNotFoundError):
        return
    base.fail(f"v67 self-test expected a fail-closed rejection: {label}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v67 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v67 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(p.raw_root, {"docs/canonical/UNAUTHORIZED_V67_BOOTSTRAP.md": b"# smuggled\n"})
    _expect_failure(
        "v67 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
    )


def _check_delta_delegates_to_predecessor_for_ordinary_paths() -> None:
    """A change to neither this successor's own files nor the reopened
    pair must delegate unchanged to v66's own `delta()` - proven by
    confirming an unrelated new path is rejected the same way it would be
    if v66's own `delta()` were called directly."""
    candidate = OverlayView(p.raw_root, {"docs/canonical/UNAUTHORIZED_V67_ORDINARY.md": b"# nope\n"})
    direct_exc = None
    delegated_exc = None
    try:
        p.q.delta(p._project_for_v66(candidate), p._project_for_v66(p.raw_root))
    except base.PolicyError as exc:
        direct_exc = str(exc)
    try:
        p.delta(candidate, p.raw_root)
    except base.PolicyError as exc:
        delegated_exc = str(exc)
    if direct_exc is None or delegated_exc is None:
        base.fail("v67 delta delegation self-test did not observe a rejection on either path")
    if direct_exc != delegated_exc:
        base.fail(
            "v67 delta does not delegate identically to the inherited v66 delta: "
            f"direct={direct_exc!r} delegated={delegated_exc!r}"
        )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_reopen_state_unchanged()
    _check_embedded_pre_reopen_bytes()
    _check_predecessor_exact()
    _check_workflow_projection()
    _check_bootstrap_scope()
    _check_delta_delegates_to_predecessor_for_ordinary_paths()
    p.install()
    p.overlay()
    print("wepld v67 S2-A009 self-test-only repair self-tests: PASS")


if __name__ == "__main__":
    run()
