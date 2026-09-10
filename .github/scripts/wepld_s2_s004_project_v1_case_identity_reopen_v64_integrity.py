#!/usr/bin/env python3
"""Authorize a bounded, single-use reopen of the frozen S2-S004
`crates/core/tests/project_v1.rs` case-only path identity-collision test
evidence gap.

v64 is an append-only policy successor over canonical v63 at main
c24a5132d0030a71dfa46e7c13e54086f7333f88. Founder standing authorization for
the smallest bounded append-only policy successors required to obtain missing
mandatory S2 test/evidence authorizes exactly this: reopen one already-frozen
test path so a real fixture for the S2-S004 case-only *identity* half can be
recorded -- two paths that differ only by ASCII case are driven through
`observe_project_locator` and turned into `ProjectMatchFacts`, proving that
identity is bound to the *resolved* path: on a case-insensitive filesystem
(macOS APFS on the S2 CI matrix) the two spellings canonicalize to the same
real directory, produce the same `facts_digest`, and a reservation built under
one spelling recovers as the same project under the other -- one identity, no
spurious second project, no fabrication; on a case-sensitive filesystem (Linux
ext4) only the exact-case directory exists, so the other spelling is a bounded
`NotFound` in `resolved_path` and never a fabricated resolution to the
directory that does exist. This is the identity-collision half that S2-S004's
existing `machine_path_preserves_exact_case_and_never_lowercases` (case
*preservation*, threat model T-003, PR #295) explicitly does not cover.

`crates/core/tests/project_v1.rs` was reopened before by v54 (S2-S004 case
preservation, PR #295), v59 (S2-S001 TOCTOU, PR #307), and v63 (S2-S001
locator `..`-escape / invalid-byte, PR #321); all three grants are consumed,
so the path is frozen again by the same v25 Core-observation-tranche freeze
mechanism those successors themselves reopened against. A fresh single-use
reopen is required. It is not a wholly new file.

v64 grants exactly one thing and nothing else:

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
project-locator observation and identity-facts surface through its existing
public functions (`observe_project_locator`, `machine_path_from_path`,
`ProjectMatchFacts`, `allocate_project_id`, `build_reservation`,
`recover_reservation`), using only ordinary filesystem fixture setup under a
Cargo tmpdir. No new process, network, model, or S3+ authority. No `unsafe`
code (the file keeps `#![forbid(unsafe_code)]`). Every dangerous authority
(general shell,
arbitrary process, package install, project-native command execution, Git
mutation, `safe.directory` mutation, remediation execution, network,
model/provider execution, S3+) remains `NONE`/unchanged and is asserted
against the inherited v63 chain.

Package-load / resting-view note: v64 follows the v45..v63 discipline. It
owns a fresh `LocalRepositoryView` of the exact checked-out head, imports
frozen v63 under an exact v64->v63 workflow-entrypoint reversal, and inherits
every v63 hook by reference, plus v60's, v61's and v63's own reopen-authority
markers carried forward in the inherited-authority list. The one path this
successor reopens is subject to v25's Core-observation-tranche freeze inside
the inherited cascade's `delta()`, which this successor's `delta()`
intercepts directly before any predecessor delegation, exactly the way
v45/v52/v53/v54/v60/v61/v63 intercept their own reopened paths - so no
further predecessor-facing projection is required (v25's freeze is
delta()-only; its files() check on the path is structural). This grant needs
no pre-reopen-bytes token-scan projection: the new test exercises only the
locator observation and identity-facts surface (filesystem fixture setup plus
`ProjectMatchFacts` / reservation calls) and adds no `std::process::Command`,
`std::net`, or other token the inherited v28 scan forbids, so the reopened
content is scanned exactly as written, exactly like v54's, v59's and v63's own
project_v1.rs grants.
"""
from __future__ import annotations


import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_s004_project_v1_case_identity_reopen_v64_integrity.py"
T = ".github/scripts/wepld_s2_s004_project_v1_case_identity_reopen_v64_selftest.py"
T_BLOB = "8f45103e0776245bee174456cddf1fb6e66f02f6"

V63_P_BLOB = "6bba90376b012530f561fd4856f726991b009189"
V63_T_BLOB = "a39e62208d8771c81a37a198c1dcf7384816df1a"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V64_ENTRYPOINT = b"wepld_s2_s004_project_v1_case_identity_reopen_v64_integrity.py"
_V63_ENTRYPOINT = b"wepld_s2_s001_project_v1_locator_reopen_v63_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Do not inherit a predecessor module's resting/projection view. v64 bases
# all of its own exact-head and predecessor projections on the actual
# checked-out repository bytes.
raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v63_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V64_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v64 workflow entrypoint count drifted before v63 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V64_ENTRYPOINT, _V63_ENTRYPOINT)


def _import_v63_under_workflow_projection() -> Any:
    """Import frozen v63 while it observes exact v63 workflow bytes.

    v63 (hence v57..v45..v36) reads workflow bytes while its module is
    imported, and the v63->v64 entrypoint migration ships in this same
    candidate, so v63 must not observe its own successor's bytes. Only
    ``LocalRepositoryView.read_bytes`` is wrapped for the duration of the
    import and then restored in ``finally`` - the class object itself is
    never rebound, so v20's frozen constructor guard still captures and
    later sees the exact canonical ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v63_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v63_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v64 v63-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v63_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_s001_project_v1_locator_reopen_v63_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v63_under_workflow_projection()

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

# --- S2-S004 project_v1.rs test-evidence reopen allowlist ---
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

REOPEN_TASKS = frozenset({"S2-S004"})

# The exact pre-reopen frontier blob of the one reopened path, at canonical
# main c24a5132d0030a71dfa46e7c13e54086f7333f88 (project_v1.rs as it stands
# after the S2-S001 `..`-escape / invalid-byte locator fixture landed via the
# v63 reopen, PR #321; the same v25 Core-observation-tranche freeze re-closed
# the path when that content became canonical).
# While a candidate/base view's blob for `REOPEN_TEST` still equals this exact
# value, the reopen grant is unused and available. The instant it differs
# (because the reopened content became canonical), the grant is permanently
# consumed.
EXACT_FROZEN_BLOB = "0d34032de07af074709b1747c9db3b500e751c7a"

AUTH = "S2_S004_PROJECT_V1_CASE_IDENTITY_REOPEN_ONLY"
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
    "S2_S001_PROJECT_V1_LOCATOR_REOPEN_AUTHORITY",
)
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(q, _name)

# The one new grant this successor makes. Scoped to exactly one file, exactly
# once. It does not widen any runtime authority merely because the reopened
# test drives `observe_project_locator` with `..` / traversal / invalid-path
# inputs, proving the project-locator layer clamps parent-dir escapes at root,
# preserves the raw spelling, and reports an unresolvable path as a bounded
# typed `Observation::Unavailable` rather than panicking or fabricating one.
S2_S004_PROJECT_V1_CASE_IDENTITY_REOPEN_AUTHORITY = (
    "SINGLE_USE_TEST_ONLY_REOPEN_OF_PROJECT_V1_RS_FOR_S2_S004_CASE_IDENTITY"
)

S2_S004_PROJECT_V1_CASE_IDENTITY_REOPEN_CONTRACT = (
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

for _path, _expected in ((q.P, V63_P_BLOB), (q.T, V63_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v64 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v63_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v64 workflow does not reverse to exact canonical v63 predecessor: "
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


def req_v63(view: Any) -> None:
    for path, expected in ((q.P, V63_P_BLOB), (q.T, V63_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v64 candidate/base is missing frozen v63 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v63 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v63(view: Any) -> Any:
    """The reopened path is not subject to any frozen-content check anywhere
    in the inherited cascade below v45's own product-tranche freeze, which
    this successor's `delta()` intercepts directly rather than delegating -
    so the only projection any predecessor delegation ever needs is the
    ordinary workflow-entrypoint reversal every successor performs."""
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v63_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v63's view always; project the policy base
    only when it is a real post-v64 base. A pre-v64 bootstrap base predates
    the v63->v64 workflow migration and carries no v64 policy files, so it
    must reach v63's frozen hooks unprojected."""
    projected_candidate = _project_for_v63(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v63(policy_base)


def run_predecessor_selftests() -> None:
    """Run frozen v63's own self-tests once, under a v64->v63 workflow
    reversal.

    v63's corrected hooks are inherited by reference. Only ``read_bytes`` is
    wrapped here for the v64->v63 workflow reversal; the wrap is restored in
    ``finally``. No reopen-path projection is layered here: the reopened
    path is not subject to any frozen-content check downstream, so a fresh
    ``LocalRepositoryView`` inventory of the real post-tranche head still
    matches what the frozen cascade expects.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v63_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v64 v63-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v63_selftest_read_bytes
    try:
        _call("v63 self-tests under v64->v63 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def _reopen_available(view: Any) -> bool:
    if REOPEN_TEST not in V25.ps(view):
        base.fail(f"v64 reopen base is missing the frozen reopened path: {REOPEN_TEST}")
    actual = V25.blob(view.read_bytes(REOPEN_TEST, base.MAX_POLICY_FILE_BYTES))
    return actual == EXACT_FROZEN_BLOB


def _require_reopen_base(view: Any) -> None:
    if not _reopen_available(view):
        base.fail(
            "v64 S2-S004 project_v1.rs evidence reopen already consumed; "
            "further changes require a new successor"
        )


def _verify_text_reopen_file(view: Any, path: str) -> None:
    if path not in V25.ps(view):
        base.fail(f"v64 reopen path missing: {path}")
    if V25.mode(view, path) != "100644":
        base.fail(f"v64 reopen path mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data:
        base.fail(f"v64 reopen path must not be empty: {path}")
    if len(data) > MAX_REOPEN_FILE_BYTES:
        base.fail(f"v64 reopen path exceeds bounded size: {path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"v64 reopen path must be UTF-8: {path}: {exc}")


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
            base.fail(f"v64 S2-S004 project_v1.rs evidence reopen must not change frozen path: {path}")
    for relative in sorted(V25.FROZEN_STATE_PATHS):
        if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, V25.MAX_S1_STATE_BYTES
        ):
            base.fail(f"v64 candidate changed frozen S1 state: {relative}")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v64 bootstrap delta must be exactly two v64 policy files plus two integrity workflows"
                )
            base.fail("v64 bootstrap base authorizes only exact S2-S004 project_v1.rs reopen policy activation")
        req_v63(candidate)
        req_v63(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v64 policy files are frozen after activation")

    reopen_changed = frozenset(paths & REOPEN_FILES)
    if reopen_changed:
        if paths != REOPEN_FILES:
            base.fail("v64 S2-S004 project_v1.rs evidence reopen must not mix with non-reopen paths")
        _verify_reopen_candidate(candidate, policy_base)
        return

    q.delta(_project_for_v63(candidate), _project_for_v63(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v63_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v64 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v64 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v64 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v64 steady-state controlled file drifted: {path}")

    reopen_safe = REOPEN_FILES & safe_paths & V25.ps(candidate)
    for path in sorted(reopen_safe):
        _verify_text_reopen_file(candidate, path)

    rest = frozenset(safe_paths - CONTROLLED_FILES - REOPEN_FILES)
    if rest:
        projected_candidate, projected_base = _v63_views(candidate, policy_base)
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
    q.files(_project_for_v63(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v64 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v64 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v64 controlled file content drifted: {path}")
    if not _reopen_available(view):
        _verify_text_reopen_file(view, REOPEN_TEST)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v64 predecessor component-base hook unavailable")
    path_set = set(paths)
    if path_set & REOPEN_FILES:
        remaining = path_set - REOPEN_FILES
        _call(
            "v64 projected predecessor component-base verifier",
            _PREDECESSOR_COMPONENT_BASE,
            _project_for_v63(view),
            remaining - CONTROLLED_FILES,
            allow_core_main_change=False,
        )
        return
    _call(
        "v64 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v63(view),
        path_set - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v64 predecessor S1 freeze hook unavailable")
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if paths == REOPEN_FILES:
        for relative in sorted(V25.FROZEN_STATE_PATHS):
            if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
                relative, V25.MAX_S1_STATE_BYTES
            ):
                base.fail(f"v64 candidate changed frozen S1 state: {relative}")
        return
    projected_candidate, projected_base = _v63_views(candidate, policy_base)
    _call(
        "v64 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v64=S2_S004_PROJECT_V1_CASE_IDENTITY_REOPEN_ONLY")
    print(f"v64_authority={AUTH}")
    print(f"s2_implementation_authority_v64={S2_IMPLEMENTATION_AUTHORITY}")
    print(
        "s2_s004_project_v1_case_identity_reopen_authority_v64="
        f"{S2_S004_PROJECT_V1_CASE_IDENTITY_REOPEN_AUTHORITY}"
    )
    print(f"reopen_available_v64={_reopen_available(raw_root)}")
    print(f"doctor_cli_authority_v64={DOCTOR_CLI_AUTHORITY}")
    print(f"general_shell_authority_v64={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v64={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v64={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v64={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v64={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v64={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v64={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v64={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v64={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v64={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v64={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v64={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v64={SOURCE_ADMISSION}")
    print(f"dependency_admission_v64={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v64={S3_PLUS_AUTHORITY}")
    print(f"test_child_process_authority_v64={TEST_CHILD_PROCESS_AUTHORITY}")
    print(f"next_authority_gate_v64={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v64 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v64 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v64 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(q, name) != globals()[name]:
            base.fail(f"v64 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v63 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v63 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v63 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v63 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v63 files hook"), q.files),
        (_attr(shell, "print_success", "v63 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v64 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v64 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v64 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v64 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v64 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v64 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v64 allowed hook")
    _bind(shell, "verify_policy_files", files, "v64 files hook")
    _bind(shell, "print_success", printer, "v64 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v64 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v64 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_s004_project_v1_case_identity_reopen_v64_selftest import run

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
