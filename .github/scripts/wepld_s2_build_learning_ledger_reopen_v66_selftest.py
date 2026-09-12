#!/usr/bin/env python3
"""Self-tests for the v66 S2-A009 Build Learning documentation-pair reopen authority."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_build_learning_ledger_reopen_v66_integrity as p

_OVERLAY_VIEW_COUNTER = itertools.count()


class OverlayView:
    def __init__(
        self,
        view: Any,
        replacements: dict[str, bytes] | None = None,
        *,
        omitted: frozenset[str] = frozenset(),
    ) -> None:
        self._view = view
        self._replacements = replacements or {}
        self._omitted = omitted
        self._instance_id = next(_OVERLAY_VIEW_COUNTER)

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v66 self-test overlay exceeds read bound: {path}")
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
        return (self._instance_id, path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any, expected: str) -> None:
    try:
        action()
    except (base.PolicyError, FileNotFoundError) as exc:
        if expected not in str(exc):
            base.fail(f"v66 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v66 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_A009_BUILD_LEARNING_LEDGER_REOPEN_ONLY":
        base.fail("v66 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != "TEST_OR_EVIDENCE_REOPEN_ONLY":
        base.fail("v66 S2 implementation boundary drift")
    if p.S2_A009_BUILD_LEARNING_REOPEN_AUTHORITY != (
        "SINGLE_USE_PAIRED_REOPEN_OF_CURRENT_STATE_MD_AND_BUILD_LEARNING_LEDGER_MD"
    ):
        base.fail("v66 must grant exactly the single-use paired documentation reopen authority")
    if p.NEXT_AUTHORITY_GATE != "S3":
        base.fail("v66 next authority gate drift")
    inherited_unchanged = (
        "DEPENDENCY_ADMISSION",
        "SOURCE_ADMISSION",
        "GIT_ROUTE_DECISION",
        "GIT_PROCESS_ADMISSION",
        "EXTERNAL_PROCESS_AUTHORITY",
        "GIT_EXECUTION_AUTHORITY",
        "NETWORK_AUTHORITY",
        "MODEL_PROVIDER_EXECUTION",
        "DOCTOR_CLI_AUTHORITY",
        "S3_PLUS_AUTHORITY",
        "GENERAL_SHELL_AUTHORITY",
        "ARBITRARY_PROCESS_AUTHORITY",
        "PACKAGE_INSTALL_AUTHORITY",
        "PROJECT_NATIVE_COMMAND_EXECUTION",
        "GIT_MUTATION_AUTHORITY",
        "SAFE_DIRECTORY_MUTATION_AUTHORITY",
        "REMEDIATION_EXECUTION_AUTHORITY",
        "TEST_CHILD_PROCESS_AUTHORITY",
        "GIT_TOPOLOGY_EVIDENCE_REOPEN_AUTHORITY",
        "S2_S006_S007_GIT_TOPOLOGY_REOPEN_AUTHORITY",
        "S2_S006_GITFILE_REOPEN_AUTHORITY",
        "S2_Q004_CLI_LARGE_REPO_REOPEN_AUTHORITY",
        "S2_S001_PROJECT_V1_LOCATOR_REOPEN_AUTHORITY",
        "S2_S004_PROJECT_V1_CASE_IDENTITY_REOPEN_AUTHORITY",
        "S2_S006_GITDIR_REOPEN_AUTHORITY",
    )
    for name in inherited_unchanged:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v66 widened or changed inherited authority: {name}")
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
            base.fail(f"v66 must not grant {name}")


def _check_reopen_contract() -> None:
    for invariant in (
        "DOCUMENTATION_FILES_ONLY",
        "PAIRED_TRANSITION_BOTH_OR_NEITHER",
        "SINGLE_USE_REOPEN",
        "NO_SOURCE_CHANGE",
        "NO_MANIFEST_OR_LOCKFILE_CHANGE",
        "NO_WORKFLOW_CHANGE_BEYOND_ENTRYPOINT_MIGRATION",
        "NO_NEW_RUNTIME_AUTHORITY",
        "NO_NETWORK_EFFECT",
        "NO_PROCESS_AUTHORITY_GRANTED",
    ):
        if invariant not in p.S2_A009_BUILD_LEARNING_REOPEN_CONTRACT:
            base.fail(f"v66 reopen contract lost invariant: {invariant}")


def _check_reopen_scope() -> None:
    if p.REOPEN_FILES != frozenset({p.CHECKPOINT, p.LEDGER}):
        base.fail("v66 reopen path set drift")
    if len(p.REOPEN_FILES) != 2:
        base.fail("v66 reopen must be exactly the paired two paths")
    if p.CHECKPOINT != "docs/canonical/CURRENT_STATE.md":
        base.fail("v66 checkpoint path drift")
    if p.LEDGER != "docs/learning/BUILD_LEARNING_LEDGER.md":
        base.fail("v66 ledger path drift")
    if p.REOPEN_TASKS != frozenset({"S2-A009"}):
        base.fail("v66 reopen task allowlist must claim exactly S2-A009")
    if any(t.startswith("S2-AUTH") for t in p.REOPEN_TASKS):
        base.fail("v66 reopen task allowlist must not claim authority tasks")
    if p.EXACT_FROZEN_BLOBS != {
        p.CHECKPOINT: "c76985050e796ae7553d88c856c4f4e90e6bbbb6",
        p.LEDGER: "688f776b9097ab5ede9f7810218b2985753e0355",
    }:
        base.fail("v66 pre-reopen frozen blob identity drift")


def _check_predecessor_exact() -> None:
    p.req_v65(p.raw_root)
    if p.V65_P_BLOB != "a5d8f1655743fc893daa404cd6e9eb063ea917d1":
        base.fail("v66 frozen v65 integrity identity drift")
    if p.V65_T_BLOB != "9551feec8fd6e625facf3e3b160db66f6e25223c":
        base.fail("v66 frozen v65 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._project_for_v65(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v66 workflow projection does not reverse to exact v65: {path}")
        if p._V66_ENTRYPOINT in data:
            base.fail(f"v66 workflow projection left the v66 entrypoint: {path}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v66 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v66 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V66_BOOTSTRAP.md": b"# smuggled\n"},
    )
    _expect_failure(
        "v66 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v66 policy files plus two integrity workflows",
    )


_SYNTHETIC_CHECKPOINT = b"# v66 synthetic checkpoint (self-test only, never landed)\n"
_SYNTHETIC_LEDGER = b"# v66 synthetic ledger (self-test only, never landed)\n"


def _synthetic_reopened_candidate(*, extra: dict[str, bytes] | None = None) -> OverlayView:
    replacements: dict[str, bytes] = {
        p.CHECKPOINT: _SYNTHETIC_CHECKPOINT,
        p.LEDGER: _SYNTHETIC_LEDGER,
    }
    if extra:
        replacements.update(extra)
    return OverlayView(p.raw_root, replacements)


def _check_reopen_delta_shape() -> None:
    """Exercises `delta()`'s reopen-grant branch against the real checked-out
    head. Once this candidate's own content lands (the reopen is consumed),
    `_reopen_available(p.raw_root)` is false and the authoritative proof
    becomes `verify-candidate-local` against the real pre-reopen commit,
    exactly like every other successor's equivalent self-test guard.
    """
    if not p._reopen_available(p.raw_root):
        _expect_failure(
            "v66 reopen already consumed on real checkout",
            lambda: p.delta(_synthetic_reopened_candidate(), p.raw_root),
            "already consumed",
        )
        return

    candidate = _synthetic_reopened_candidate()
    p.delta(candidate, p.raw_root)

    only_checkpoint = OverlayView(p.raw_root, {p.CHECKPOINT: _SYNTHETIC_CHECKPOINT})
    _expect_failure(
        "v66 reopen must reject changing only the checkpoint half",
        lambda: p.delta(only_checkpoint, p.raw_root),
        "must be exactly both paired paths",
    )

    only_ledger = OverlayView(p.raw_root, {p.LEDGER: _SYNTHETIC_LEDGER})
    _expect_failure(
        "v66 reopen must reject changing only the ledger half",
        lambda: p.delta(only_ledger, p.raw_root),
        "must be exactly both paired paths",
    )

    mixed = _synthetic_reopened_candidate(
        extra={"docs/canonical/UNAUTHORIZED_S001_MIX.md": b"# nope\n"}
    )
    _expect_failure(
        "v66 reopen mixed with non-reopen path",
        lambda: p.delta(mixed, p.raw_root),
        "must be exactly both paired paths",
    )

    lock_mut = _synthetic_reopened_candidate(extra={"Cargo.lock": b"# tampered lock\n"})
    _expect_failure(
        "v66 reopen must not mutate Cargo.lock",
        lambda: p.delta(lock_mut, p.raw_root),
        "must be exactly both paired paths",
    )

    workflow_mut = _synthetic_reopened_candidate(
        extra={p.FW: p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES) + b"\n# nope\n"}
    )
    _expect_failure(
        "v66 reopen must not mutate a workflow beyond entrypoint migration",
        lambda: p.delta(workflow_mut, p.raw_root),
        "must be exactly both paired paths",
    )

    empty_ledger = _synthetic_reopened_candidate(extra={p.LEDGER: b""})
    _expect_failure(
        "v66 reopen candidate ledger must not be empty",
        lambda: p.delta(empty_ledger, p.raw_root),
        "must not be empty",
    )

    non_utf8_checkpoint = _synthetic_reopened_candidate(extra={p.CHECKPOINT: b"\xff\xfe\x00bad"})
    _expect_failure(
        "v66 reopen candidate checkpoint must be UTF-8",
        lambda: p.delta(non_utf8_checkpoint, p.raw_root),
        "must be UTF-8",
    )

    oversized_ledger = _synthetic_reopened_candidate(
        extra={p.LEDGER: b"a" * (p.MAX_REOPEN_FILE_BYTES + 1)}
    )
    _expect_failure(
        "v66 reopen candidate ledger must respect the bounded size ceiling",
        lambda: p.delta(oversized_ledger, p.raw_root),
        "exceeds bounded size",
    )


def _check_reopen_single_use() -> None:
    """A candidate built over a policy base whose reopened pair already
    differs from the pinned pre-reopen blobs (the grant already exercised)
    must be rejected, even when the changed-path set is otherwise exactly
    the reopen-only shape."""
    already_used_base = OverlayView(
        p.raw_root,
        {p.CHECKPOINT: _SYNTHETIC_CHECKPOINT, p.LEDGER: _SYNTHETIC_LEDGER},
    )
    further_candidate = OverlayView(
        already_used_base,
        {
            p.CHECKPOINT: _SYNTHETIC_CHECKPOINT + b"\n// second attempt\n",
            p.LEDGER: _SYNTHETIC_LEDGER + b"\n// second attempt\n",
        },
    )
    _expect_failure(
        "v66 reopen grant is single-use",
        lambda: p.delta(further_candidate, already_used_base),
        "already consumed",
    )


def _check_reopen_half_applied_base_fails_closed() -> None:
    """A base where exactly one of the two paired paths has already moved is
    a corrupted/half-applied state, not a legitimate 'unavailable' base - it
    must be rejected loudly rather than silently treated as consumed."""
    half_applied_base = OverlayView(p.raw_root, {p.CHECKPOINT: _SYNTHETIC_CHECKPOINT})
    _expect_failure(
        "v66 half-applied paired base must fail closed",
        lambda: p._reopen_available(half_applied_base),
        "half-applied",
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_reopen_contract()
    _check_reopen_scope()
    _check_predecessor_exact()
    _check_workflow_projection()
    _check_bootstrap_scope()
    _check_reopen_delta_shape()
    _check_reopen_single_use()
    _check_reopen_half_applied_base_fails_closed()
    p.install()
    p.overlay()
    print("wepld v66 S2-A009 Build Learning documentation-pair reopen authority self-tests: PASS")


if __name__ == "__main__":
    run()
