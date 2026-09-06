#!/usr/bin/env python3
"""Self-tests for the v55 S2-E015 identity_store_v1.rs evidence reopen +
TEST_CHILD_PROCESS_AUTHORITY."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_git_topology_evidence_reopen_v55_integrity as p

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
                base.fail(f"v55 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v55 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v55 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_GIT_TOPOLOGY_EVIDENCE_REOPEN_ONLY":
        base.fail("v55 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != "TEST_OR_EVIDENCE_REOPEN_ONLY":
        base.fail("v55 S2 implementation boundary drift")
    if p.GIT_TOPOLOGY_EVIDENCE_REOPEN_AUTHORITY != (
        "SINGLE_USE_TEST_ONLY_REOPEN_OF_GIT_TOPOLOGY_V1_RS"
    ):
        base.fail("v55 must grant exactly the single-use Git-topology evidence reopen authority")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v55 next authority gate drift")
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
    )
    for name in inherited_unchanged:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v55 widened or changed inherited authority: {name}")
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
            base.fail(f"v55 must not grant {name}")
    if p.TEST_CHILD_PROCESS_AUTHORITY != "RE_EXEC_CURRENT_TEST_BINARY_ONLY":
        base.fail("v55 TEST_CHILD_PROCESS_AUTHORITY drift")
    if p.TEST_CHILD_PROCESS_AUTHORITY in (
        p.GENERAL_SHELL_AUTHORITY, p.ARBITRARY_PROCESS_AUTHORITY,
        p.PROJECT_NATIVE_COMMAND_EXECUTION,
    ):
        base.fail("v55 TEST_CHILD_PROCESS_AUTHORITY must be distinct from the NONE denials")
    for _inv in (
        "RE_EXEC_CURRENT_TEST_BINARY_ONLY", "NO_ARBITRARY_EXECUTABLE", "NO_SHELL",
        "NO_PROJECT_NATIVE_COMMAND", "BOUNDED_ARGS_AND_ENV", "BOUNDED_CHILD_LIFETIME",
        "NO_CAPABILITY_BEYOND_THE_ISOLATED_TEMP_STORE",
        "DETERMINISTIC_CLEANUP_NO_ORPHAN_CHILD", "CRASH_RECOVERY_SEMANTICS_ONLY",
        "NO_AMBIENT_PROCESS_AUTHORITY_AFTER_THE_FIXTURE",
        "NOT_GENERAL_PROCESS_EXECUTION_AUTHORITY",
    ):
        if _inv not in p.TEST_CHILD_PROCESS_CONTRACT:
            base.fail(f"v55 TEST_CHILD_PROCESS_CONTRACT lost invariant: {_inv}")


def _check_reopen_contract() -> None:
    for invariant in (
        "TEST_FILE_ONLY",
        "SINGLE_PATH_SCOPE",
        "SINGLE_USE_REOPEN",
        "NO_SOURCE_CHANGE",
        "NO_MANIFEST_OR_LOCKFILE_CHANGE",
        "REAL_GIT_FIXTURE_REQUIRED_NOT_MOCKED",
        "NO_NETWORK_EFFECT",
        "NO_GIT_MUTATION_AUTHORITY_GRANTED",
    ):
        if invariant not in p.GIT_TOPOLOGY_EVIDENCE_REOPEN_CONTRACT:
            base.fail(f"v55 reopen contract lost invariant: {invariant}")


def _check_reopen_scope() -> None:
    if p.REOPEN_FILES != frozenset({"crates/core/tests/identity_store_v1.rs"}):
        base.fail("v55 reopen path set drift")
    if p.CORE_MANIFEST in p.REOPEN_FILES or p.ROOT_CARGO_LOCK in p.REOPEN_FILES:
        base.fail("v55 reopen must not authorize dependency mutation")
    if p.ROOT_CARGO in p.REOPEN_FILES:
        base.fail("v55 reopen must not authorize workspace manifest mutation")
    if any(m in p.REOPEN_FILES for m in (p.GIT_TOPOLOGY_MODULE, p.PROJECT_MODULE, p.IDENTITY_MODULE, p.STORE_MODULE)):
        base.fail("v55 reopen must not authorize source module mutation")
    if p.CORE_EXPORT in p.REOPEN_FILES:
        base.fail("v55 reopen must not touch the shared Core export")
    for path in p.REOPEN_FILES:
        if not path.startswith("crates/core/tests/"):
            base.fail(f"v55 reopen escaped crates/core/tests: {path}")
    if len(p.REOPEN_FILES) != 1:
        base.fail("v55 reopen must be a single exact path")
    if "S2-E015" not in p.REOPEN_TASKS:
        base.fail("v55 reopen task allowlist must claim S2-E015")
    if any(t.startswith("S2-AUTH") for t in p.REOPEN_TASKS):
        base.fail("v55 reopen task allowlist must not claim authority tasks")


def _check_predecessor_exact() -> None:
    p.req_v54(p.raw_root)
    if p.V54_P_BLOB != "112ca6fad544743d418789cfe73bd5a4102e57df":
        base.fail("v55 frozen v54 integrity identity drift")
    if p.V54_T_BLOB != "4556d97c9a573b90437bcd37bee7fe473672500f":
        base.fail("v55 frozen v54 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._project_for_v54(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v55 workflow projection does not reverse to exact v54: {path}")
        if p._V55_ENTRYPOINT in data:
            base.fail(f"v55 workflow projection left the v55 entrypoint: {path}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v55 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v55 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V55_BOOTSTRAP.md": b"# smuggled\n"},
    )
    _expect_failure(
        "v55 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v55 policy files plus two integrity workflows",
    )


def _synthetic_reopened_candidate(*, extra: dict[str, bytes] | None = None) -> OverlayView:
    replacements: dict[str, bytes] = {
        p.REOPEN_TEST: (
            p.raw_root.read_bytes(p.REOPEN_TEST, base.MAX_POLICY_FILE_BYTES)
            + b"\n// v55 synthetic reopened touch\n"
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
            "v55 reopen already consumed on real checkout",
            lambda: p.delta(_synthetic_reopened_candidate(), p.raw_root),
            "already consumed",
        )
        return

    candidate = _synthetic_reopened_candidate()
    p.delta(candidate, p.raw_root)

    mixed = _synthetic_reopened_candidate(
        extra={"docs/canonical/UNAUTHORIZED_I006_I007_MIX.md": b"# nope\n"}
    )
    _expect_failure(
        "v55 reopen mixed with non-reopen path",
        lambda: p.delta(mixed, p.raw_root),
        "must not mix with non-reopen paths",
    )

    lock_mut = _synthetic_reopened_candidate(extra={p.ROOT_CARGO_LOCK: b"# tampered lock\n"})
    _expect_failure(
        "v55 reopen must not mutate Cargo.lock",
        lambda: p.delta(lock_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )

    manifest_mut = _synthetic_reopened_candidate(
        extra={p.CORE_MANIFEST: b"[package]\nname = \"wepld-core\"\n"}
    )
    _expect_failure(
        "v55 reopen must not mutate the core manifest",
        lambda: p.delta(manifest_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )

    source_mut = _synthetic_reopened_candidate(
        extra={
            p.GIT_TOPOLOGY_MODULE: (
                p.raw_root.read_bytes(p.GIT_TOPOLOGY_MODULE, base.MAX_POLICY_FILE_BYTES)
                + b"\n// unauthorized\n"
            )
        }
    )
    _expect_failure(
        "v55 reopen must not mutate the Git-topology source module",
        lambda: p.delta(source_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )

    extra_test_file = _synthetic_reopened_candidate(
        extra={"crates/core/tests/unauthorized_v1.rs": b"#[test]\nfn x() {}\n"}
    )
    _expect_failure(
        "v55 reopen must not add an unauthorized extra test file",
        lambda: p.delta(extra_test_file, p.raw_root),
        "must not mix with non-reopen paths",
    )

    workflow_mut = _synthetic_reopened_candidate(
        extra={p.FW: p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES) + b"\n# nope\n"}
    )
    _expect_failure(
        "v55 reopen must not mutate a workflow beyond entrypoint migration",
        lambda: p.delta(workflow_mut, p.raw_root),
        "must not mix with non-reopen paths",
    )


def _check_test_child_process_static_bound() -> None:
    """The static TEST_CHILD_PROCESS_AUTHORITY bound rejects a reopened test that
    spawns a string-literal executable / shell or adds a network capability, and
    accepts a current_exe() re-exec.
    """
    if not p._reopen_available(p.raw_root):
        return
    base_text = p.raw_root.read_bytes(p.REOPEN_TEST, base.MAX_POLICY_FILE_BYTES).decode("utf-8")

    evil_src = base_text + '\nfn _x() { let _ = std::process::Command::new("sh").status(); }\n'
    _expect_failure(
        "v55 rejects a string-literal executable spawn in the reopened test",
        lambda: p.delta(OverlayView(p.raw_root, {p.REOPEN_TEST: evil_src.encode("utf-8")}), p.raw_root),
        "string-literal executable",
    )

    net_src = base_text + '\nfn _n() { let _ = std::net::TcpStream::connect("1"); }\n'
    _expect_failure(
        "v55 rejects a network capability in the reopened test",
        lambda: p.delta(OverlayView(p.raw_root, {p.REOPEN_TEST: net_src.encode("utf-8")}), p.raw_root),
        "capability token",
    )

    # Nonliteral arbitrary executable: `current_exe` appears in the file but the
    # spawn takes an unrelated variable. The tightened bound must still reject it.
    sneaky = base_text + (
        "\n// current_exe\nfn _s() { let evil = std::path::PathBuf::from(\"x\");"
        " let _ = std::process::Command::new(evil).status(); }\n"
    )
    _expect_failure(
        "v55 rejects Command::new(<non-current_exe ident>) even with a stray current_exe token",
        lambda: p.delta(OverlayView(p.raw_root, {p.REOPEN_TEST: sneaky.encode("utf-8")}), p.raw_root),
        "current_exe()",
    )
    # Aliased Command import must be rejected before it can bypass the matcher.
    aliased = base_text + (
        "\nuse std::process::Command as C;\n"
        "fn _a() { let e = std::env::current_exe().unwrap(); let _ = C::new(e).status(); }\n"
    )
    _expect_failure(
        "v55 rejects an aliased Command import in the reopened test",
        lambda: p.delta(OverlayView(p.raw_root, {p.REOPEN_TEST: aliased.encode("utf-8")}), p.raw_root),
        "use std::process",
    )
    # Identifier shadowing: an outer current_exe() binding, then an inner
    # rebinding of the same name to an arbitrary path before the spawn.
    shadowed = base_text + (
        "\nfn _sh() { let exe = std::env::current_exe().unwrap();"
        " { let exe = std::path::PathBuf::from(\"sh\");"
        " let _ = std::process::Command::new(exe).status(); } }\n"
    )
    _expect_failure(
        "v55 rejects identifier shadowing of the current_exe() binding",
        lambda: p.delta(OverlayView(p.raw_root, {p.REOPEN_TEST: shadowed.encode("utf-8")}), p.raw_root),
        "shadowing",
    )
    # Post-binding mutation: a `mut` binding reassigned before the spawn.
    mutated = base_text + (
        "\nfn _mu() { let mut exe = std::env::current_exe().unwrap();"
        " exe = std::path::PathBuf::from(\"sh\");"
        " let _ = std::process::Command::new(exe).status(); }\n"
    )
    _expect_failure(
        "v55 rejects a mutable / reassigned process-argument binding",
        lambda: p.delta(OverlayView(p.raw_root, {p.REOPEN_TEST: mutated.encode("utf-8")}), p.raw_root),
        "immutable",
    )
    ok_src = base_text + (
        "\nfn _c() { let e = std::env::current_exe().unwrap();"
        " let _ = std::process::Command::new(e).status(); }\n"
    )
    p.delta(OverlayView(p.raw_root, {p.REOPEN_TEST: ok_src.encode("utf-8")}), p.raw_root)


def _check_reopen_single_use() -> None:
    """A candidate built over a policy base whose reopened path already
    differs from the pinned pre-reopen blob (the grant already exercised)
    must be rejected, even when the changed-path set is otherwise exactly
    the reopen-only shape."""
    already_used_base = OverlayView(
        p.raw_root,
        {p.REOPEN_TEST: p.raw_root.read_bytes(p.REOPEN_TEST, base.MAX_POLICY_FILE_BYTES) + b"\n// already landed\n"},
    )
    further_candidate = OverlayView(
        already_used_base,
        {p.REOPEN_TEST: p.raw_root.read_bytes(p.REOPEN_TEST, base.MAX_POLICY_FILE_BYTES) + b"\n// second attempt\n"},
    )
    _expect_failure(
        "v55 reopen grant is single-use",
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
    _check_test_child_process_static_bound()
    _check_reopen_single_use()
    p.install()
    p.overlay()
    print("wepld v55 S2-E015 identity_store_v1.rs evidence reopen + TEST_CHILD_PROCESS_AUTHORITY self-tests: PASS")


if __name__ == "__main__":
    run()
