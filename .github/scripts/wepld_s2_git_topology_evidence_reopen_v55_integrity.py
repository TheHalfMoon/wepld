#!/usr/bin/env python3
"""Authorize a bounded, single-use reopen of the frozen S2-E015
`crates/core/tests/identity_store_v1.rs` test evidence gap, plus a narrowly
bounded `TEST_CHILD_PROCESS_AUTHORITY` needed to observe process-crash lock
release directly.

v55 is an append-only policy successor over canonical v54 at main
1f7d1bf646825e624a5ed1f768c206c2890a8185. Founder standing authorization
authorizes exactly this: reopen one already-frozen test path so the S2-E015
process-crash half -- a child process acquires a store lock, terminates
without an orderly unlock, and the operating-system-owned lock releases so a
second process can acquire it, while the stale lock file alone is not
ownership -- can actually be recorded. `identity_store_v1.rs` is frozen by
v25 (`PRODUCT_TEST`), so a fresh single-use reopen is required.

v55 grants exactly two things and nothing else:

  1. a single-use reopen of `crates/core/tests/identity_store_v1.rs` only,
     gated on that path's exact pre-reopen blob still being canonical (one
     exercise, then re-frozen forever).
  2. `TEST_CHILD_PROCESS_AUTHORITY = RE_EXEC_CURRENT_TEST_BINARY_ONLY`: the
     reopened test may spawn a child process ONLY by re-executing
     `std::env::current_exe()` (the test binary itself), with bounded
     arguments/environment, bounded lifetime, deterministic cleanup, no
     orphan child, no network / filesystem / process capability beyond the
     isolated temporary store, and no ambient process authority after the
     fixture. This is NOT general process-execution authority
     (`TEST_CHILD_PROCESS_AUTHORITY != GENERAL_PROCESS_EXECUTION_AUTHORITY`);
     `GENERAL_SHELL_AUTHORITY`, `ARBITRARY_PROCESS_AUTHORITY`,
     `PROJECT_NATIVE_COMMAND_EXECUTION` all remain `NONE`. The policy
     statically checks the reopened file re-execs `current_exe()` only (no
     string-literal executable, no shell, no network token); the eight
     runtime invariants above are proven by the fixture's own assertions,
     exact-head CI execution, and independent review.

It does NOT grant any change to `crates/core/src/identity.rs`,
`crates/core/src/evidence_store.rs`, `crates/core/src/project.rs`,
`crates/core/src/git_topology.rs`, `crates/core/src/lib.rs`, any Cargo
manifest/lock, Doctor/CLI files, or any workflow beyond the standard vNN
entrypoint migration. Every other dangerous authority (network,
model/provider, S3+, Git mutation, safe.directory mutation, remediation
execution, package install) remains `NONE`/unchanged and is asserted against
the inherited v54 chain.

Package-load / resting-view note: v55 follows the v45..v54 discipline. It
owns a fresh `LocalRepositoryView` of the exact checked-out head, imports
frozen v54 under an exact v55->v54 workflow-entrypoint reversal, and inherits
every v54 hook by reference. v25's `identity_store_v1.rs` freeze is
`delta()`-only (its `files()` check on the path is structural), which this
successor's `delta()` intercepts directly before any predecessor delegation,
so no further predecessor-facing projection is required.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_git_topology_evidence_reopen_v55_integrity.py"
T = ".github/scripts/wepld_s2_git_topology_evidence_reopen_v55_selftest.py"
T_BLOB = "b694f3171a3ad57e5b78eb2779b2ef49c0e6fea4"

V54_P_BLOB = "112ca6fad544743d418789cfe73bd5a4102e57df"
V54_T_BLOB = "4556d97c9a573b90437bcd37bee7fe473672500f"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V55_ENTRYPOINT = b"wepld_s2_git_topology_evidence_reopen_v55_integrity.py"
_V54_ENTRYPOINT = b"wepld_s2_git_topology_evidence_reopen_v54_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Do not inherit a predecessor module's resting/projection view. v55 bases
# all of its own exact-head and predecessor projections on the actual
# checked-out repository bytes.
raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v54_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V55_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v55 workflow entrypoint count drifted before v54 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V55_ENTRYPOINT, _V54_ENTRYPOINT)


def _import_v54_under_workflow_projection() -> Any:
    """Import frozen v54 while it observes exact v54 workflow bytes.

    v54 (hence v50..v45..v36) reads workflow bytes while its module is
    imported, and the v54->v55 entrypoint migration ships in this same
    candidate, so v54 must not observe its own successor's bytes. Only
    ``LocalRepositoryView.read_bytes`` is wrapped for the duration of the
    import and then restored in ``finally`` - the class object itself is
    never rebound, so v20's frozen constructor guard still captures and
    later sees the exact canonical ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v54_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v54_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v55 v54-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v54_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_git_topology_evidence_reopen_v54_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v54_under_workflow_projection()

V25 = q.V25
CW = q.CW
Q_WF = dict(q.WF)
_attr = q._attr
_bind = q._bind
_call = q._call
_ProjectionView = q._ProjectionView
_INST = False
_PREDECESSOR_COMPONENT_BASE: Any = None
_PREDECESSOR_FREEZE_S1: Any = None

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

# --- S2-E015 identity_store_v1.rs test-evidence reopen allowlist ---
# Exactly one already-tracked, already-frozen path is reopened. Nothing else.
REOPEN_TEST = "crates/core/tests/identity_store_v1.rs"
REOPEN_FILES = frozenset({REOPEN_TEST})

CORE_MANIFEST = "crates/core/Cargo.toml"
ROOT_CARGO = "Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"
GIT_TOPOLOGY_MODULE = "crates/core/src/git_topology.rs"
PROJECT_MODULE = "crates/core/src/project.rs"
IDENTITY_MODULE = "crates/core/src/identity.rs"
STORE_MODULE = "crates/core/src/evidence_store.rs"
CORE_EXPORT = "crates/core/src/lib.rs"

MAX_REOPEN_FILE_BYTES = 262_144

REOPEN_TASKS = frozenset({"S2-E015"})

# The exact pre-reopen frontier blob of the one reopened path, at canonical
# main 1f7d1bf646825e624a5ed1f768c206c2890a8185 (identity_store_v1.rs as
# frozen by v25's PRODUCT_TEST freeze).
# While a candidate/base view's blob for `REOPEN_TEST` still equals this exact
# value, the reopen grant is unused and available. The instant it differs
# (because the reopened content became canonical), the grant is permanently
# consumed.
EXACT_FROZEN_BLOB = "fc1fd55c47e5bb6879b8c5bb03cd0500bedcff0f"

AUTH = "S2_GIT_TOPOLOGY_EVIDENCE_REOPEN_ONLY"
S2_IMPLEMENTATION_AUTHORITY = "TEST_OR_EVIDENCE_REOPEN_ONLY"
DEPENDENCY_ADMISSION = q.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = q.SOURCE_ADMISSION
GIT_ROUTE_DECISION = q.GIT_ROUTE_DECISION
GIT_PROCESS_ADMISSION = q.GIT_PROCESS_ADMISSION
EXTERNAL_PROCESS_AUTHORITY = q.EXTERNAL_PROCESS_AUTHORITY
GIT_EXECUTION_AUTHORITY = q.GIT_EXECUTION_AUTHORITY
NETWORK_AUTHORITY = q.NETWORK_AUTHORITY
MODEL_PROVIDER_EXECUTION = q.MODEL_PROVIDER_EXECUTION
DOCTOR_CLI_AUTHORITY = q.DOCTOR_CLI_AUTHORITY
S3_PLUS_AUTHORITY = q.S3_PLUS_AUTHORITY
NEXT_AUTHORITY_GATE = "S2-ACCEPTANCE"

# The one new grant this successor makes. Scoped to exactly one file, exactly
# once. It does not widen `GIT_EXECUTION_AUTHORITY` or grant any new runtime
# behavior merely because the reopened tests invoke existing
# `git_topology.rs` functions through real Git fixtures.
GIT_TOPOLOGY_EVIDENCE_REOPEN_AUTHORITY = (
    "SINGLE_USE_TEST_ONLY_REOPEN_OF_GIT_TOPOLOGY_V1_RS"
)

# Standing denials this successor must not relax.
GENERAL_SHELL_AUTHORITY = "NONE"
ARBITRARY_PROCESS_AUTHORITY = "NONE"
PACKAGE_INSTALL_AUTHORITY = "NONE"
PROJECT_NATIVE_COMMAND_EXECUTION = "NONE"
GIT_MUTATION_AUTHORITY = "NONE"
SAFE_DIRECTORY_MUTATION_AUTHORITY = "NONE"
REMEDIATION_EXECUTION_AUTHORITY = "NONE"

# The one narrow new grant this successor makes beyond the reopen. Bounded to
# re-execution of the test binary itself for the S2-E015 process-crash fixture.
TEST_CHILD_PROCESS_AUTHORITY = "RE_EXEC_CURRENT_TEST_BINARY_ONLY"
TEST_CHILD_PROCESS_CONTRACT = (
    "RE_EXEC_CURRENT_TEST_BINARY_ONLY",
    "NO_ARBITRARY_EXECUTABLE",
    "NO_SHELL",
    "NO_PROJECT_NATIVE_COMMAND",
    "BOUNDED_ARGS_AND_ENV",
    "BOUNDED_CHILD_LIFETIME",
    "NO_CAPABILITY_BEYOND_THE_ISOLATED_TEMP_STORE",
    "DETERMINISTIC_CLEANUP_NO_ORPHAN_CHILD",
    "CRASH_RECOVERY_SEMANTICS_ONLY",
    "NO_AMBIENT_PROCESS_AUTHORITY_AFTER_THE_FIXTURE",
    "NOT_GENERAL_PROCESS_EXECUTION_AUTHORITY",
)

GIT_TOPOLOGY_EVIDENCE_REOPEN_CONTRACT = (
    "TEST_FILE_ONLY",
    "SINGLE_PATH_SCOPE",
    "SINGLE_USE_REOPEN",
    "NO_SOURCE_CHANGE",
    "NO_MANIFEST_OR_LOCKFILE_CHANGE",
    "NO_RUNTIME_AUTHORITY_FROM_THE_REOPEN_ITSELF",
    "REAL_GIT_FIXTURE_REQUIRED_NOT_MOCKED",
    "NO_NETWORK_EFFECT",
    "NO_GIT_MUTATION_AUTHORITY_GRANTED",
    "REUSES_QUALIFIED_GIT_EXECUTION_AUTHORITY_ONLY",
)

for _path, _expected in ((q.P, V54_P_BLOB), (q.T, V54_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v55 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v54_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v55 workflow does not reverse to exact canonical v54 predecessor: "
                f"{path} expected={Q_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return replacements


def _derive_candidate_workflow_hash(path: str) -> str:
    _workflow_replacements(raw_root)
    return V25.sha(raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES))


WF = {
    FW: _derive_candidate_workflow_hash(FW),
    AW: _derive_candidate_workflow_hash(AW),
    CW: q.WF[CW],
}


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v54(view: Any) -> None:
    for path, expected in ((q.P, V54_P_BLOB), (q.T, V54_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v55 candidate/base is missing frozen v54 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v54 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v54(view: Any) -> Any:
    """The reopened path is not subject to any frozen-content check anywhere
    in the inherited cascade below v45's own product-tranche freeze, which
    this successor's `delta()` intercepts directly rather than delegating -
    so the only projection any predecessor delegation ever needs is the
    ordinary workflow-entrypoint reversal every successor performs."""
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v54_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v54's view always; project the policy base
    only when it is a real post-v55 base. A pre-v55 bootstrap base predates
    the v54->v55 workflow migration and carries no v55 policy files, so it
    must reach v54's frozen hooks unprojected."""
    projected_candidate = _project_for_v54(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v54(policy_base)


def _boot_base_for_selftest() -> Any:
    return _project_for_v54(raw_root)


def run_predecessor_selftests() -> None:
    """Run frozen v54's own self-tests once, under a v55->v54 workflow
    reversal.

    v54's corrected hooks are inherited by reference. Only ``read_bytes`` is
    wrapped here for the v55->v54 workflow reversal; the wrap is restored in
    ``finally``. No reopen-path projection is layered here: the reopened
    path is not subject to any frozen-content check downstream, so a fresh
    ``LocalRepositoryView`` inventory of the real post-tranche head still
    matches what the frozen cascade expects.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v54_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v55 v54-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v54_selftest_read_bytes
    try:
        _call("v54 self-tests under v55->v54 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def _reopen_available(view: Any) -> bool:
    if REOPEN_TEST not in V25.ps(view):
        base.fail(f"v55 reopen base is missing the frozen reopened path: {REOPEN_TEST}")
    actual = V25.blob(view.read_bytes(REOPEN_TEST, base.MAX_POLICY_FILE_BYTES))
    return actual == EXACT_FROZEN_BLOB


def _require_reopen_base(view: Any) -> None:
    if not _reopen_available(view):
        base.fail(
            "v55 Git-topology evidence reopen already consumed; "
            "further changes require a new successor"
        )


def _verify_text_reopen_file(view: Any, path: str) -> None:
    if path not in V25.ps(view):
        base.fail(f"v55 reopen path missing: {path}")
    if V25.mode(view, path) != "100644":
        base.fail(f"v55 reopen path mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data:
        base.fail(f"v55 reopen path must not be empty: {path}")
    if len(data) > MAX_REOPEN_FILE_BYTES:
        base.fail(f"v55 reopen path exceeds bounded size: {path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"v55 reopen path must be UTF-8: {path}: {exc}")


def _verify_test_child_process_bounds(candidate: Any) -> None:
    """Static bound on TEST_CHILD_PROCESS_AUTHORITY: the reopened test file may
    spawn a child ONLY by re-executing std::env::current_exe(); never a
    string-literal executable, a shell, or a network capability."""
    text = candidate.read_bytes(REOPEN_TEST, base.MAX_POLICY_FILE_BYTES).decode("utf-8")
    import re as _re
    for _m in _re.finditer(r"Command::new\s*\(", text):
        _tail = text[_m.end():_m.end() + 96].lstrip()
        if _tail[:1] in ('"', "'") or _tail[:2] in ('r"', "b\"") or _tail.startswith("r#"):
            base.fail(
                "v55 TEST_CHILD_PROCESS_AUTHORITY: Command::new must not take a "
                "string-literal executable; re-exec std::env::current_exe() only"
            )
    if ("std::process::Command" in text or "process::Command" in text or "Command::new" in text):
        if "current_exe" not in text:
            base.fail(
                "v55 TEST_CHILD_PROCESS_AUTHORITY: a process spawn in the reopened "
                "test must re-exec std::env::current_exe() only"
            )
    for _tok in ("TcpStream", "TcpListener", "UdpSocket", "std::net", "reqwest",
                 "std::os::unix::process", "CommandExt", "pre_exec"):
        if _tok in text:
            base.fail(f"v55 reopened test must not add capability token: {_tok}")


def _verify_reopen_candidate(candidate: Any, policy_base: Any) -> None:
    _require_reopen_base(policy_base)
    _verify_text_reopen_file(candidate, REOPEN_TEST)
    _verify_test_child_process_bounds(candidate)
    for path in (CORE_MANIFEST, ROOT_CARGO, ROOT_CARGO_LOCK, GIT_TOPOLOGY_MODULE, PROJECT_MODULE, IDENTITY_MODULE, STORE_MODULE, CORE_EXPORT):
        if candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ):
            base.fail(f"v55 Git-topology evidence reopen must not change frozen path: {path}")
    for relative in sorted(V25.FROZEN_STATE_PATHS):
        if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, V25.MAX_S1_STATE_BYTES
        ):
            base.fail(f"v55 candidate changed frozen S1 state: {relative}")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v55 bootstrap delta must be exactly two v55 policy files plus two integrity workflows"
                )
            base.fail("v55 bootstrap base authorizes only exact Git-topology evidence reopen policy activation")
        req_v54(candidate)
        req_v54(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v55 policy files are frozen after activation")

    reopen_changed = frozenset(paths & REOPEN_FILES)
    if reopen_changed:
        if paths != REOPEN_FILES:
            base.fail(
                "v55 Git-topology evidence reopen must not mix with non-reopen paths"
            )
        _verify_reopen_candidate(candidate, policy_base)
        return

    q.delta(_project_for_v54(candidate), _project_for_v54(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v54_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v55 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v55 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v55 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v55 steady-state controlled file drifted: {path}")

    reopen_safe = REOPEN_FILES & safe_paths & V25.ps(candidate)
    for path in sorted(reopen_safe):
        _verify_text_reopen_file(candidate, path)

    rest = frozenset(safe_paths - CONTROLLED_FILES - REOPEN_FILES)
    if rest:
        projected_candidate, projected_base = _v54_views(candidate, policy_base)
        q.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES - REOPEN_FILES
    if remaining:
        q.allowed(remaining, stage)


def files(view: Any) -> None:
    q.files(_project_for_v54(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v55 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v55 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v55 controlled file content drifted: {path}")
    if not _reopen_available(view):
        _verify_text_reopen_file(view, REOPEN_TEST)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v55 predecessor component-base hook unavailable")
    path_set = set(paths)
    if path_set & REOPEN_FILES:
        remaining = path_set - REOPEN_FILES
        _call(
            "v55 projected predecessor component-base verifier",
            _PREDECESSOR_COMPONENT_BASE,
            _project_for_v54(view),
            remaining - CONTROLLED_FILES,
            allow_core_main_change=False,
        )
        return
    _call(
        "v55 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v54(view),
        path_set - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v55 predecessor S1 freeze hook unavailable")
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if paths == REOPEN_FILES:
        for relative in sorted(V25.FROZEN_STATE_PATHS):
            if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
                relative, V25.MAX_S1_STATE_BYTES
            ):
                base.fail(f"v55 candidate changed frozen S1 state: {relative}")
        return
    projected_candidate, projected_base = _v54_views(candidate, policy_base)
    _call(
        "v55 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v55=S2_GIT_TOPOLOGY_EVIDENCE_REOPEN_ONLY")
    print(f"v55_authority={AUTH}")
    print(f"s2_implementation_authority_v55={S2_IMPLEMENTATION_AUTHORITY}")
    print(
        "git_topology_evidence_reopen_authority_v55="
        f"{GIT_TOPOLOGY_EVIDENCE_REOPEN_AUTHORITY}"
    )
    print(f"reopen_available_v55={_reopen_available(raw_root)}")
    print(f"test_child_process_authority_v55={TEST_CHILD_PROCESS_AUTHORITY}")
    print(f"doctor_cli_authority_v55={DOCTOR_CLI_AUTHORITY}")
    print(f"general_shell_authority_v55={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v55={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v55={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v55={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v55={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v55={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v55={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v55={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v55={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v55={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v55={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v55={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v55={SOURCE_ADMISSION}")
    print(f"dependency_admission_v55={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v55={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v55={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v55 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
        (_attr(execution, "_verify_component_base", "component-base hook"), verify_component_base),
        (_attr(execution, "freeze_s1_007_state", "S1 state freeze hook"), freeze_s1_007_state),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v55 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v55 workflow identity projection drifted")
    for name in (
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
    ):
        if getattr(q, name) != globals()[name]:
            base.fail(f"v55 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v54 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v54 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v54 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v54 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v54 files hook"), q.files),
        (_attr(shell, "print_success", "v54 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v55 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v55 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v55 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v55 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v55 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v55 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v55 allowed hook")
    _bind(shell, "verify_policy_files", files, "v55 files hook")
    _bind(shell, "print_success", printer, "v55 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v55 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v55 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_git_topology_evidence_reopen_v55_selftest import run

    run()


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "selftest":
            selftest()
            return 0
        install()
        if argv and argv[0] == "verify-candidate-local":
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("--root", required=True)
            parser.add_argument("--policy-base-root", required=True)
            parser.add_argument("--policy-base-sha", required=True)
            args = parser.parse_args(argv[1:])
            return int(
                _call(
                    "candidate-local verifier",
                    V25.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", V25.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
