#!/usr/bin/env python3
"""Authorize a bounded, single-use reopen of the frozen S2-S001
`crates/core/tests/project_v1.rs` project-locator adversarial test evidence gap.

v63 is an append-only policy successor over canonical v62 at main
7857416388ae8c544a20d0b3c2c520ffc64332ee. Founder standing authorization for
the smallest bounded append-only policy successors required to obtain missing
mandatory S2 test/evidence authorizes exactly this: reopen one already-frozen
test path so a real adversarial fixture for the S2-S001 project-locator layer
can be recorded -- a `..` / path-traversal and separator/invalid-path attack is
driven through `observe_project_locator` (the project-locator observation, not
the already-covered `safe_path_segment` store-ID layer), proving the lexical
normalizer clamps parent-dir escapes at root, records the raw traversal-bearing
spelling verbatim in `input_path` without hiding it, reflects the deterministic
lexical form in `lexical_absolute_path`, and turns an unresolvable / invalid
path into a bounded typed `Observation::Unavailable` in `resolved_path` -- never
a panic, never a fabricated resolution, never a path escape above root.

`crates/core/tests/project_v1.rs` was reopened before by v54 (S2-S004 case
preservation) and v59 (S2-S001 TOCTOU, PR #307); both grants are consumed, so
the path is frozen again by the same v25 Core-observation-tranche freeze
mechanism those successors themselves reopened against. A fresh single-use
reopen is required. It is not a wholly new file.

v63 grants exactly one thing and nothing else:

  - a single-use reopen of `crates/core/tests/project_v1.rs` only, gated on
    that path's exact pre-reopen blob still being canonical (so the grant can
    be exercised exactly once; the instant the reopened content becomes
    canonical, this same check freezes the path again, forever).

It does NOT grant any change to `crates/core/src/project.rs`,
`crates/core/src/identity.rs`, `crates/core/src/git_topology.rs`,
`crates/core/src/bin/wepld.rs`, `crates/core/src/cli.rs`,
`crates/core/src/doctor.rs`, `crates/core/src/lib.rs`,
`crates/core/Cargo.toml`, root `Cargo.toml`/`Cargo.lock`, or any workflow
beyond the standard vNN entrypoint migration. It does NOT widen any
authority: the reopened test may only exercise the already-qualified
project-locator observation surface through its existing public functions
(`observe_project_locator`, `machine_path_from_path`), using only ordinary
filesystem fixture setup under a Cargo tmpdir. No new process, network,
model, or S3+ authority. No `unsafe` code (the file keeps
`#![forbid(unsafe_code)]`). Every dangerous authority (general shell,
arbitrary process, package install, project-native command execution, Git
mutation, `safe.directory` mutation, remediation execution, network,
model/provider execution, S3+) remains `NONE`/unchanged and is asserted
against the inherited v62 chain.

Package-load / resting-view note: v63 follows the v45..v62 discipline. It
owns a fresh `LocalRepositoryView` of the exact checked-out head, imports
frozen v62 under an exact v63->v62 workflow-entrypoint reversal, and inherits
every v62 hook by reference, plus v60's, v61's and v62's own reopen-authority
markers carried forward in the inherited-authority list. The one path this
successor reopens is subject to v25's Core-observation-tranche freeze inside
the inherited cascade's `delta()`, which this successor's `delta()`
intercepts directly before any predecessor delegation, exactly the way
v45/v52/v53/v54/v60/v61/v62 intercept their own reopened paths - so no
further predecessor-facing projection is required (v25's freeze is
delta()-only; its files() check on the path is structural). This grant needs
no pre-reopen-bytes token-scan projection: `project_v1.rs` already contains
`std::process::id()` (a numeric PID read, admitted with v59's TOCTOU
fixture), and the new test adds no `std::process::Command` or other token the
inherited v28 scan forbids -- it exercises the locator observation only --
so the reopened content is scanned exactly as written, exactly like v54's and
v59's own project_v1.rs grants.
"""
from __future__ import annotations


import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_s001_project_v1_locator_reopen_v63_integrity.py"
T = ".github/scripts/wepld_s2_s001_project_v1_locator_reopen_v63_selftest.py"
T_BLOB = "a39e62208d8771c81a37a198c1dcf7384816df1a"

V62_P_BLOB = "724c6abb5bc1a37a08a8e552aa9957fe08755690"
V62_T_BLOB = "8ef0b4c7b6410345e731a00c8432627f399ecf70"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V63_ENTRYPOINT = b"wepld_s2_s001_project_v1_locator_reopen_v63_integrity.py"
_V62_ENTRYPOINT = b"wepld_s2_q004_cli_large_repo_reopen_v62_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Do not inherit a predecessor module's resting/projection view. v63 bases
# all of its own exact-head and predecessor projections on the actual
# checked-out repository bytes.
raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v62_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V63_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v63 workflow entrypoint count drifted before v62 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V63_ENTRYPOINT, _V62_ENTRYPOINT)


def _import_v62_under_workflow_projection() -> Any:
    """Import frozen v62 while it observes exact v62 workflow bytes.

    v62 (hence v57..v45..v36) reads workflow bytes while its module is
    imported, and the v62->v63 entrypoint migration ships in this same
    candidate, so v62 must not observe its own successor's bytes. Only
    ``LocalRepositoryView.read_bytes`` is wrapped for the duration of the
    import and then restored in ``finally`` - the class object itself is
    never rebound, so v20's frozen constructor guard still captures and
    later sees the exact canonical ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v62_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v62_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v63 v62-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v62_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_q004_cli_large_repo_reopen_v62_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v62_under_workflow_projection()

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

# --- S2-S001 project_v1.rs test-evidence reopen allowlist ---
# Exactly one already-tracked, already-frozen path is reopened. Nothing else.
REOPEN_TEST = "crates/core/tests/project_v1.rs"
REOPEN_FILES = frozenset({REOPEN_TEST})

CORE_MANIFEST = "crates/core/Cargo.toml"
ROOT_CARGO = "Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"
GIT_TOPOLOGY_MODULE = "crates/core/src/git_topology.rs"
PROJECT_MODULE = "crates/core/src/project.rs"
CORE_EXPORT = "crates/core/src/lib.rs"
BIN_MODULE = "crates/core/src/bin/wepld.rs"
CLI_MODULE = "crates/core/src/cli.rs"
DOCTOR_MODULE = "crates/core/src/doctor.rs"

MAX_REOPEN_FILE_BYTES = 262_144

REOPEN_TASKS = frozenset({"S2-S001"})

# The exact pre-reopen frontier blob of the one reopened path, at canonical
# main 595b474c4ee5ee6d58c036e2689f2f788dbb7b8f (project_v1.rs as frozen by the
# S2-AUTH-015 Doctor/CLI product tranche, PR #280).
# While a candidate/base view's blob for `REOPEN_TEST` still equals this exact
# value, the reopen grant is unused and available. The instant it differs
# (because the reopened content became canonical), the grant is permanently
# consumed.
EXACT_FROZEN_BLOB = "1127bfa667508dec9b92b9e78bc0269301c45390"

AUTH = "S2_S001_PROJECT_V1_LOCATOR_REOPEN_ONLY"
NEXT_AUTHORITY_GATE = "S2-ACCEPTANCE"

_INHERITED_AUTHORITY_NAMES = (
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
    "S2_IMPLEMENTATION_AUTHORITY",
    "GIT_TOPOLOGY_EVIDENCE_REOPEN_AUTHORITY",
    "S2_S006_S007_GIT_TOPOLOGY_REOPEN_AUTHORITY",
    "S2_S006_GITFILE_REOPEN_AUTHORITY",
    "S2_Q004_CLI_LARGE_REPO_REOPEN_AUTHORITY",
)
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(q, _name)

# The one new grant this successor makes. Scoped to exactly one file, exactly
# once. It does not widen any runtime authority merely because the reopened
# test drives `observe_project_locator` with `..` / traversal / invalid-path
# inputs, proving the project-locator layer clamps parent-dir escapes at root,
# preserves the raw spelling, and reports an unresolvable path as a bounded
# typed `Observation::Unavailable` rather than panicking or fabricating one.
S2_S001_PROJECT_V1_LOCATOR_REOPEN_AUTHORITY = (
    "SINGLE_USE_TEST_ONLY_REOPEN_OF_PROJECT_V1_RS_FOR_S2_S001_LOCATOR"
)

S2_S001_PROJECT_V1_LOCATOR_REOPEN_CONTRACT = (
    "TEST_FILE_ONLY",
    "SINGLE_PATH_SCOPE",
    "SINGLE_USE_REOPEN",
    "NO_SOURCE_CHANGE",
    "NO_MANIFEST_OR_LOCKFILE_CHANGE",
    "NO_NEW_RUNTIME_AUTHORITY",
    "REAL_GIT_FIXTURE_REQUIRED_NOT_MOCKED",
    "NO_NETWORK_EFFECT",
    "NO_PROCESS_AUTHORITY_GRANTED",
    "REUSES_QUALIFIED_GIT_TOPOLOGY_ADAPTER_ONLY",
)

for _path, _expected in ((q.P, V62_P_BLOB), (q.T, V62_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v63 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v62_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v63 workflow does not reverse to exact canonical v62 predecessor: "
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


def req_v62(view: Any) -> None:
    for path, expected in ((q.P, V62_P_BLOB), (q.T, V62_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v63 candidate/base is missing frozen v62 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v62 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v62(view: Any) -> Any:
    """The reopened path is not subject to any frozen-content check anywhere
    in the inherited cascade below v45's own product-tranche freeze, which
    this successor's `delta()` intercepts directly rather than delegating -
    so the only projection any predecessor delegation ever needs is the
    ordinary workflow-entrypoint reversal every successor performs."""
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v62_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v62's view always; project the policy base
    only when it is a real post-v63 base. A pre-v63 bootstrap base predates
    the v62->v63 workflow migration and carries no v63 policy files, so it
    must reach v62's frozen hooks unprojected."""
    projected_candidate = _project_for_v62(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v62(policy_base)


def run_predecessor_selftests() -> None:
    """Run frozen v62's own self-tests once, under a v63->v62 workflow
    reversal.

    v62's corrected hooks are inherited by reference. Only ``read_bytes`` is
    wrapped here for the v63->v62 workflow reversal; the wrap is restored in
    ``finally``. No reopen-path projection is layered here: the reopened
    path is not subject to any frozen-content check downstream, so a fresh
    ``LocalRepositoryView`` inventory of the real post-tranche head still
    matches what the frozen cascade expects.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v62_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v63 v62-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v62_selftest_read_bytes
    try:
        _call("v62 self-tests under v63->v62 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def _reopen_available(view: Any) -> bool:
    if REOPEN_TEST not in V25.ps(view):
        base.fail(f"v63 reopen base is missing the frozen reopened path: {REOPEN_TEST}")
    actual = V25.blob(view.read_bytes(REOPEN_TEST, base.MAX_POLICY_FILE_BYTES))
    return actual == EXACT_FROZEN_BLOB


def _require_reopen_base(view: Any) -> None:
    if not _reopen_available(view):
        base.fail(
            "v63 S2-S001 project_v1.rs evidence reopen already consumed; "
            "further changes require a new successor"
        )


def _verify_text_reopen_file(view: Any, path: str) -> None:
    if path not in V25.ps(view):
        base.fail(f"v63 reopen path missing: {path}")
    if V25.mode(view, path) != "100644":
        base.fail(f"v63 reopen path mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data:
        base.fail(f"v63 reopen path must not be empty: {path}")
    if len(data) > MAX_REOPEN_FILE_BYTES:
        base.fail(f"v63 reopen path exceeds bounded size: {path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"v63 reopen path must be UTF-8: {path}: {exc}")


def _verify_reopen_candidate(candidate: Any, policy_base: Any) -> None:
    _require_reopen_base(policy_base)
    _verify_text_reopen_file(candidate, REOPEN_TEST)
    for path in (
        CORE_MANIFEST,
        ROOT_CARGO,
        ROOT_CARGO_LOCK,
        GIT_TOPOLOGY_MODULE,
        PROJECT_MODULE,
        CORE_EXPORT,
        BIN_MODULE,
        CLI_MODULE,
        DOCTOR_MODULE,
    ):
        if candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ):
            base.fail(f"v63 S2-S001 project_v1.rs evidence reopen must not change frozen path: {path}")
    for relative in sorted(V25.FROZEN_STATE_PATHS):
        if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, V25.MAX_S1_STATE_BYTES
        ):
            base.fail(f"v63 candidate changed frozen S1 state: {relative}")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v63 bootstrap delta must be exactly two v63 policy files plus two integrity workflows"
                )
            base.fail("v63 bootstrap base authorizes only exact S2-S001 project_v1.rs reopen policy activation")
        req_v62(candidate)
        req_v62(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v63 policy files are frozen after activation")

    reopen_changed = frozenset(paths & REOPEN_FILES)
    if reopen_changed:
        if paths != REOPEN_FILES:
            base.fail("v63 S2-S001 project_v1.rs evidence reopen must not mix with non-reopen paths")
        _verify_reopen_candidate(candidate, policy_base)
        return

    q.delta(_project_for_v62(candidate), _project_for_v62(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v62_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v63 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v63 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v63 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v63 steady-state controlled file drifted: {path}")

    reopen_safe = REOPEN_FILES & safe_paths & V25.ps(candidate)
    for path in sorted(reopen_safe):
        _verify_text_reopen_file(candidate, path)

    rest = frozenset(safe_paths - CONTROLLED_FILES - REOPEN_FILES)
    if rest:
        projected_candidate, projected_base = _v62_views(candidate, policy_base)
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
    q.files(_project_for_v62(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v63 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v63 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v63 controlled file content drifted: {path}")
    if not _reopen_available(view):
        _verify_text_reopen_file(view, REOPEN_TEST)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v63 predecessor component-base hook unavailable")
    path_set = set(paths)
    if path_set & REOPEN_FILES:
        remaining = path_set - REOPEN_FILES
        _call(
            "v63 projected predecessor component-base verifier",
            _PREDECESSOR_COMPONENT_BASE,
            _project_for_v62(view),
            remaining - CONTROLLED_FILES,
            allow_core_main_change=False,
        )
        return
    _call(
        "v63 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v62(view),
        path_set - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v63 predecessor S1 freeze hook unavailable")
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if paths == REOPEN_FILES:
        for relative in sorted(V25.FROZEN_STATE_PATHS):
            if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
                relative, V25.MAX_S1_STATE_BYTES
            ):
                base.fail(f"v63 candidate changed frozen S1 state: {relative}")
        return
    projected_candidate, projected_base = _v62_views(candidate, policy_base)
    _call(
        "v63 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v63=S2_S001_PROJECT_V1_LOCATOR_REOPEN_ONLY")
    print(f"v63_authority={AUTH}")
    print(f"s2_implementation_authority_v63={S2_IMPLEMENTATION_AUTHORITY}")
    print(
        "s2_s001_project_v1_locator_reopen_authority_v63="
        f"{S2_S001_PROJECT_V1_LOCATOR_REOPEN_AUTHORITY}"
    )
    print(f"reopen_available_v63={_reopen_available(raw_root)}")
    print(f"doctor_cli_authority_v63={DOCTOR_CLI_AUTHORITY}")
    print(f"general_shell_authority_v63={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v63={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v63={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v63={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v63={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v63={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v63={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v63={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v63={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v63={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v63={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v63={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v63={SOURCE_ADMISSION}")
    print(f"dependency_admission_v63={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v63={S3_PLUS_AUTHORITY}")
    print(f"test_child_process_authority_v63={TEST_CHILD_PROCESS_AUTHORITY}")
    print(f"next_authority_gate_v63={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v63 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v63 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v63 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(q, name) != globals()[name]:
            base.fail(f"v63 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v62 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v62 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v62 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v62 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v62 files hook"), q.files),
        (_attr(shell, "print_success", "v62 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v63 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v63 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v63 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v63 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v63 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v63 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v63 allowed hook")
    _bind(shell, "verify_policy_files", files, "v63 files hook")
    _bind(shell, "print_success", printer, "v63 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v63 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v63 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_s001_project_v1_locator_reopen_v63_selftest import run

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
