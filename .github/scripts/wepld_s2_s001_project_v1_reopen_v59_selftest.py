#!/usr/bin/env python3
"""Self-tests for the v59 S2-S001 project_v1.rs evidence reopen authority."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_s001_project_v1_reopen_v59_integrity as p

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
                base.fail(f"v59 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v59 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v59 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_S001_PROJECT_V1_REOPEN_ONLY":
        base.fail("v59 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != "TEST_OR_EVIDENCE_REOPEN_ONLY":
        base.fail("v59 S2 implementation boundary drift")
    if p.S2_S001_PROJECT_V1_RS_REOPEN_AUTHORITY != (
        "SINGLE_USE_TEST_ONLY_REOPEN_OF_PROJECT_V1_RS_FOR_S2_S001"
    ):
        base.fail("v59 must grant exactly the single-use S2-S001 project_v1.rs reopen authority")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v59 next authority gate drift")
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
    )
    for name in inherited_unchanged:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v59 widened or changed inherited authority: {name}")
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
            base.fail(f"v59 must not grant {name}")


def _check_reopen_contract() -> None:
    for invariant in (
        "TEST_FILE_ONLY",
        "SINGLE_PATH_SCOPE",
        "SINGLE_USE_REOPEN",
        "NO_SOURCE_CHANGE",
        "NO_MANIFEST_OR_LOCKFILE_CHANGE",
        "NO_NEW_RUNTIME_AUTHORITY",
        "REAL_FILESYSTEM_FIXTURE_REQUIRED_NOT_MOCKED",
        "NO_NETWORK_EFFECT",
        "NO_PROCESS_AUTHORITY_GRANTED",
    ):
        if invariant not in p.S2_S001_PROJECT_V1_REOPEN_CONTRACT:
            base.fail(f"v59 reopen contract lost invariant: {invariant}")


def _check_reopen_scope() -> None:
    if p.REOPEN_FILES != frozenset({"crates/core/tests/project_v1.rs"}):
        base.fail("v59 reopen path set drift")
    if p.CORE_MANIFEST in p.REOPEN_FILES or p.ROOT_CARGO_LOCK in p.REOPEN_FILES:
        base.fail("v59 reopen must not authorize dependency mutation")
    if p.ROOT_CARGO in p.REOPEN_FILES:
        base.fail("v59 reopen must not authorize workspace manifest mutation")
    if p.GIT_TOPOLOGY_MODULE in p.REOPEN_FILES or p.PROJECT_MODULE in p.REOPEN_FILES:
        base.fail("v59 reopen must not authorize source module mutation")
    if p.CORE_EXPORT in p.REOPEN_FILES:
        base.fail("v59 reopen must not touch the shared Core export")
    for path in p.REOPEN_FILES:
        if not path.startswith("crates/core/tests/"):
            base.fail(f"v59 reopen escaped crates/core/tests: {path}")
    if len(p.REOPEN_FILES) != 1:
        base.fail("v59 reopen must be a single exact path")
    if p.REOPEN_TASKS != frozenset({"S2-S001"}):
        base.fail("v59 reopen task allowlist must claim exactly S2-S001")
    if any(t.startswith("S2-AUTH") for t in p.REOPEN_TASKS):
        base.fail("v59 reopen task allowlist must not claim authority tasks")


def _check_predecessor_exact() -> None:
    p.req_v58(p.raw_root)
    if p.V58_P_BLOB != "d171e6b2a89649c90435dcabbe1c288ade15a792":
        base.fail("v59 frozen v58 integrity identity drift")
    if p.V58_T_BLOB != "8f5f2cc6a4ddac75c1f67c68685e300ec5dcd7b2":
        base.fail("v59 frozen v58 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._project_for_v58(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v59 workflow projection does not reverse to exact v58: {path}")
        if p._V59_ENTRYPOINT in data:
            base.fail(f"v59 workflow projection left the v59 entrypoint: {path}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v59 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v59 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V59_BOOTSTRAP.md": b"# smuggled\n"},
    )
    _expect_failure(
        "v59 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v59 policy files plus two integrity workflows",
    )


def _synthetic_reopened_candidate(*, extra: dict[str, bytes] | None = None) -> OverlayView:
    replacements: dict[str, bytes] = {
        p.REOPEN_TEST: (
            p.raw_root.read_bytes(p.REOPEN_TEST, base.MAX_POLICY_FILE_BYTES)
            + b"\n// v59 synthetic reopened touch\n"
        )
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
            "v59 reopen already consumed on real checkout",
            lambda: p.delta(_synthetic_reopened_candidate(), p.raw_root),
            "already consumed",
        )
        return

    candidate = _synthetic_reopened_candidate()
    p.delta(candidate, p.raw_root)

    mixed = _synthetic_reopened_candidate(
        extra={"docs/canonical/UNAUTHORIZED_S001_MIX.md": b"# nope\n"}
    )
    _expect_failure(
        "v59 reopen mixed with non-reopen path",
        lambda: p.delta(mixed, p.raw_root),
        "must not mix with non-reopen paths",
    )

    lock_mut = _synthetic_reopened_candidate(extra={p.ROOT_CARGO_LOCK: b"# tampered lock\n"})
    _expect_failure(
        "v59 reopen must not mutate Cargo.lock",
        lambda: p.delta(lock_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )

    manifest_mut = _synthetic_reopened_candidate(
        extra={p.CORE_MANIFEST: b"[package]\nname = \"wepld-core\"\n"}
    )
    _expect_failure(
        "v59 reopen must not mutate the core manifest",
        lambda: p.delta(manifest_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )

    source_mut = _synthetic_reopened_candidate(
        extra={
            p.PROJECT_MODULE: (
                p.raw_root.read_bytes(p.PROJECT_MODULE, base.MAX_POLICY_FILE_BYTES)
                + b"\n// unauthorized\n"
            )
        }
    )
    _expect_failure(
        "v59 reopen must not mutate the project source module",
        lambda: p.delta(source_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )

    extra_test_file = _synthetic_reopened_candidate(
        extra={"crates/core/tests/unauthorized_v1.rs": b"#[test]\nfn x() {}\n"}
    )
    _expect_failure(
        "v59 reopen must not add an unauthorized extra test file",
        lambda: p.delta(extra_test_file, p.raw_root),
        "must not mix with non-reopen paths",
    )

    workflow_mut = _synthetic_reopened_candidate(
        extra={p.FW: p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES) + b"\n# nope\n"}
    )
    _expect_failure(
        "v59 reopen must not mutate a workflow beyond entrypoint migration",
        lambda: p.delta(workflow_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )


def _check_reopen_single_use() -> None:
    """A candidate built over a policy base whose reopened path already
    differs from the pinned pre-reopen blob (the grant already exercised)
    must be rejected, even when the changed-path set is otherwise exactly
    the reopen-only shape."""
    already_used_base = OverlayView(
        p.raw_root,
        {
            p.REOPEN_TEST: p.raw_root.read_bytes(p.REOPEN_TEST, base.MAX_POLICY_FILE_BYTES)
            + b"\n// already landed\n"
        },
    )
    further_candidate = OverlayView(
        already_used_base,
        {
            p.REOPEN_TEST: p.raw_root.read_bytes(p.REOPEN_TEST, base.MAX_POLICY_FILE_BYTES)
            + b"\n// second attempt\n"
        },
    )
    _expect_failure(
        "v59 reopen grant is single-use",
        lambda: p.delta(further_candidate, already_used_base),
        "already consumed",
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
    p.install()
    p.overlay()
    print("wepld v59 S2-S001 project_v1.rs evidence reopen authority self-tests: PASS")


if __name__ == "__main__":
    run()
