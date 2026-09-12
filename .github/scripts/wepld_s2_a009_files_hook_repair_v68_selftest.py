#!/usr/bin/env python3
"""Self-tests for the v68 files()-hook repair over v67."""

from __future__ import annotations

from typing import Any

import wepld_integrity as base
import wepld_s2_a009_files_hook_repair_v68_integrity as p


def _check_authority_markers() -> None:
    if p.AUTH != "S2_A009_FILES_HOOK_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE":
        base.fail("v68 authority marker drift")
    if p.NEXT_AUTHORITY_GATE != p.q.NEXT_AUTHORITY_GATE:
        base.fail("v68 must not change the inherited next-authority gate")
    for name in p._INHERITED_AUTHORITY_NAMES:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v68 widened or changed inherited authority: {name}")
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
            base.fail(f"v68 must not grant {name}")


def _check_reopen_state_unchanged() -> None:
    if p.CHECKPOINT != p.q.CHECKPOINT or p.LEDGER != p.q.LEDGER:
        base.fail("v68 documentation path drift")
    if p.REOPEN_FILES != p.q.REOPEN_FILES:
        base.fail("v68 reopen path set drift")
    if p.EXACT_FROZEN_BLOBS != p.q.EXACT_FROZEN_BLOBS:
        base.fail("v68 must not move the inherited reopen pins")
    if p._reopen_available(p.raw_root) != p.q._reopen_available(p.raw_root):
        base.fail("v68 reopen-availability check disagrees with the inherited one")


def _check_predecessor_exact() -> None:
    p.req_v67(p.raw_root)
    if p.V67_P_BLOB != "5c2e0f178a8e37ddfe4e9480088e643c7daa229b":
        base.fail("v68 frozen v67 integrity identity drift")
    if p.V67_T_BLOB != "dbc78ba0dc7269126a353c28aa01bca42f0845d5":
        base.fail("v68 frozen v67 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._project_for_v67(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v68 workflow projection does not reverse to exact v67: {path}")
        if p._V68_ENTRYPOINT in data:
            base.fail(f"v68 workflow projection left the v68 entrypoint: {path}")


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
                base.fail(f"v68 self-test overlay exceeds read bound: {path}")
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
    base.fail(f"v68 self-test expected a fail-closed rejection: {label}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v68 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v68 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(p.raw_root, {"docs/canonical/UNAUTHORIZED_V68_BOOTSTRAP.md": b"# smuggled\n"})
    _expect_failure(
        "v68 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
    )


def _check_files_hook_projects_docs_pair_for_predecessor_only() -> None:
    """The actual repair, exercised at the mechanism level rather than by
    running the full v67..v18 predecessor `files()` cascade against a
    synthetic tree (which hits unrelated frozen checks - e.g. v30's own
    dependency-state validation - that assume a real, fully-formed Git tree
    no ad-hoc synthetic view reliably provides; the real end-to-end proof is
    a genuine `verify-candidate-local` run against a real worktree, recorded
    in this repair's own commit message, not reproduced as a unit test
    here). This checks the installed override function itself: it must
    return the exact pre-reopen bytes for `CHECKPOINT`/`LEDGER` regardless
    of what the wrapped view actually holds, and delegate unchanged for
    every other path - on both view classes `files()` patches."""
    # Exercised once against a real LocalRepositoryView instance/original
    # method pair (the two must match: RemoteRepositoryView.read_bytes
    # assumes Remote-only attributes and cannot be called against a Local
    # instance, or vice versa - the override wrapper itself is identical
    # code installed onto both classes, so proving it once here proves both
    # installations; `files()` itself installs it onto both classes, which
    # `overlay()`'s own restoration check below still verifies for real).
    original = base.LocalRepositoryView.read_bytes
    override = p._files_predecessor_read_bytes_override(original)
    checkpoint_result = override(p.raw_root, p.CHECKPOINT, base.MAX_POLICY_FILE_BYTES)
    if checkpoint_result != p._PRE_REOPEN_CHECKPOINT_BYTES:
        base.fail("v68 files-hook override does not project CHECKPOINT")
    ledger_result = override(p.raw_root, p.LEDGER, base.MAX_POLICY_FILE_BYTES)
    if ledger_result != p._PRE_REOPEN_LEDGER_BYTES:
        base.fail("v68 files-hook override does not project LEDGER")
    other_result = override(p.raw_root, p.T, base.MAX_POLICY_FILE_BYTES)
    if other_result != original(p.raw_root, p.T, base.MAX_POLICY_FILE_BYTES):
        base.fail("v68 files-hook override must delegate unchanged for other paths")

    # `files()`'s own predecessor chain (specifically v30's dependency-state
    # check) depends on global bindings `install()` establishes; every real
    # caller (`verify-candidate-local`/`verify-remote`) always calls
    # `install()` before dispatching to any hook, so this mirrors that
    # rather than calling `files()` in a state no real caller ever produces.
    p.install()
    original_local = base.LocalRepositoryView.read_bytes
    original_remote = base.RemoteRepositoryView.read_bytes
    p.files(p.raw_root)
    if base.LocalRepositoryView.read_bytes is not original_local:
        base.fail("v68 files() left the LocalRepositoryView monkeypatch installed")
    if base.RemoteRepositoryView.read_bytes is not original_remote:
        base.fail("v68 files() left the RemoteRepositoryView monkeypatch installed")


def _check_delta_is_unaffected_by_the_files_hook_projection() -> None:
    """`delta()` must still see a synthetic candidate's *real* new bytes,
    not the pre-reopen projection `files()` uses internally - proving the
    fix is scoped to `files()` alone and does not blind reopen-content
    verification. Exercised by confirming `delta()` genuinely rejects a
    reopen candidate whose new content fails the real bounded-size check,
    which it could not do if it were (incorrectly) seeing projected bytes
    instead of the real oversized ones."""
    if not p._reopen_available(p.raw_root):
        return
    oversized_ledger = OverlayView(
        p.raw_root,
        {
            p.CHECKPOINT: b"# still real new checkpoint content\n",
            p.LEDGER: b"a" * (p.MAX_REOPEN_FILE_BYTES + 1),
        },
    )
    _expect_failure(
        "v68 delta must still see real (oversized) candidate bytes, not the files()-hook projection",
        lambda: p.delta(oversized_ledger, p.raw_root),
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_reopen_state_unchanged()
    _check_predecessor_exact()
    _check_workflow_projection()
    _check_bootstrap_scope()
    _check_files_hook_projects_docs_pair_for_predecessor_only()
    _check_delta_is_unaffected_by_the_files_hook_projection()
    p.install()
    p.overlay()
    print("wepld v68 S2-A009 files()-hook repair self-tests: PASS")


if __name__ == "__main__":
    run()
