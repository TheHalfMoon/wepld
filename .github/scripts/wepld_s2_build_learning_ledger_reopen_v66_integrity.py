#!/usr/bin/env python3
"""Authorize a bounded, paired reopen of the frozen S2 documentation-transition
route protecting `docs/canonical/CURRENT_STATE.md` and
`docs/learning/BUILD_LEARNING_LEDGER.md`, for exactly one purpose: `S2-A009`
Build Learning capture.

Prior state. The `docs_transition` route these two files share was opened by
v34/v35 (first round, spent on landing), reopened by v37..v44 (second round,
spent on landing PR #261/#263's corrected content: canonical `main` now holds
`FINAL_CHECKPOINT_BLOB=c76985050e796ae7553d88c856c4f4e90e6bbbb6` and
`FINAL_LEDGER_BLOB=688f776b9097ab5ede9f7810218b2985753e0355`, confirmed live via
`git hash-object` against the exact checked-out bytes of both files at this
policy's own base). No script v45..v65 touches `docs_transition`,
`PRE_CHECKPOINT_BLOB`, `PRE_LEDGER_BLOB`, or either documentation path; the
route has been closed, exactly as designed, since the v37..v44 round landed.

Design choice: a new `docs_transition`-style round over the same 20-layer
chain that already needed four corrective successors (v41..v44) to get right
would have to re-derive and correctly wire the exact same
predecessor-projection / local-state re-anchoring / canonical-frontier
re-anchoring / S1-016 ledger-widening machinery `v37` originally built, at a
predecessor depth this codebase has never had to reopen from before. v66
instead follows the simpler, independently-proven "single-use reopen" design
this same tower has already used six times without a single corrective
successor (v52, v53, v60, v61, v64, v65 for `crates/core` test evidence): gate
on the paired path set's pre-reopen bytes still being exactly canonical (so
the grant can be exercised exactly once, for both files together, and the
instant either becomes canonical again the pair re-freezes permanently), plus
bounded UTF-8/size sanity checks on the new bytes. It is a deliberate
deviation from the `docs_transition` precedent for this specific pair, not an
accidental one: the two mechanisms grant the identical capability (write new
canonical bytes to these two frozen files, once), and the single-use-reopen
shape has the stronger track record for a first-attempt, no-iteration
successor.

v66 grants exactly one thing and nothing else:

  - a single-use, paired reopen of `docs/canonical/CURRENT_STATE.md` and
    `docs/learning/BUILD_LEARNING_LEDGER.md` together (both or neither; a
    change to only one is rejected), gated on both paths' exact pre-reopen
    blobs still being canonical.

It does NOT grant any change to any Rust source, manifest, lockfile, or
workflow beyond the standard vNN entrypoint migration. It does NOT widen any
authority: every dangerous authority (general shell, arbitrary process,
package install, project-native command execution, Git mutation/execution,
`safe.directory` mutation, remediation execution, network, model/provider
execution, S3+) remains `NONE`/unchanged, asserted against the inherited v65
chain. It grants no S3 implementation authority and no further S2 product
path.

Package-load / resting-view note: v66 follows the v45..v65 discipline. It
owns a fresh `LocalRepositoryView` of the exact checked-out head, imports
frozen v65 under an exact v66->v65 workflow-entrypoint reversal, and inherits
every v65 hook by reference, plus every reopen-authority marker the v65 chain
already carries forward. The one path-pair this successor reopens is not
subject to any frozen-content check anywhere in the inherited cascade (the
two documentation paths are frozen only by the `docs_transition` route deep
in the chain, which this successor's own `delta()` intercepts directly,
before any predecessor delegation - so no further predecessor-facing
projection of the reopened pair is required, matching v65's own note that its
reopened test path needed none).
"""
from __future__ import annotations


import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_build_learning_ledger_reopen_v66_integrity.py"
T = ".github/scripts/wepld_s2_build_learning_ledger_reopen_v66_selftest.py"
T_BLOB = "ae8ffbaf8272e639da32ac81271bb85e22603cc1"

V65_P_BLOB = "a5d8f1655743fc893daa404cd6e9eb063ea917d1"
V65_T_BLOB = "9551feec8fd6e625facf3e3b160db66f6e25223c"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V66_ENTRYPOINT = b"wepld_s2_build_learning_ledger_reopen_v66_integrity.py"
_V65_ENTRYPOINT = b"wepld_s2_s006_gitdir_reopen_v65_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Do not inherit a predecessor module's resting/projection view. v66 bases
# all of its own exact-head and predecessor projections on the actual
# checked-out repository bytes, exactly as v65 does.
raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v65_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V66_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v66 workflow entrypoint count drifted before v65 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V66_ENTRYPOINT, _V65_ENTRYPOINT)


def _import_v65_under_workflow_projection() -> Any:
    """Import frozen v65 while it observes exact v65 workflow bytes.

    v65 (hence v64..v45..v36) reads workflow bytes while its module is
    imported, and the v65->v66 entrypoint migration ships in this same
    candidate, so v65 must not observe its own successor's bytes. Only
    ``LocalRepositoryView.read_bytes`` is wrapped for the duration of the
    import and then restored in ``finally``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v65_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v65_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v66 v65-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v65_import_read_bytes
    try:
        return importlib.import_module("wepld_s2_s006_gitdir_reopen_v65_integrity")
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v65_under_workflow_projection()

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

# --- S2-A009 Build Learning documentation-pair reopen allowlist ---
# Exactly two already-tracked, already-frozen paths are reopened, together
# only. Nothing else.
CHECKPOINT = "docs/canonical/CURRENT_STATE.md"
LEDGER = "docs/learning/BUILD_LEARNING_LEDGER.md"
REOPEN_FILES = frozenset({CHECKPOINT, LEDGER})

MAX_REOPEN_FILE_BYTES = 262_144

REOPEN_TASKS = frozenset({"S2-A009"})

# The exact pre-reopen frontier blobs of the two reopened paths, at the
# canonical bytes this policy's own base holds today - the same bytes the
# spent v37..v44 `docs_transition` round left canonical. While a
# candidate/base view's blobs for both paths still equal these exact values,
# the reopen grant is unused and available. The instant either differs
# (because the reopened content became canonical), the grant is permanently
# consumed for both.
EXACT_FROZEN_BLOBS = {
    CHECKPOINT: "c76985050e796ae7553d88c856c4f4e90e6bbbb6",
    LEDGER: "688f776b9097ab5ede9f7810218b2985753e0355",
}

AUTH = "S2_A009_BUILD_LEARNING_LEDGER_REOPEN_ONLY"
NEXT_AUTHORITY_GATE = "S3"

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
    "S2_S004_PROJECT_V1_CASE_IDENTITY_REOPEN_AUTHORITY",
    "S2_S006_GITDIR_REOPEN_AUTHORITY",
)
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(q, _name)

# The one new grant this successor makes. Scoped to exactly two paths,
# together, exactly once. It does not widen any product/process/network/
# model authority; the reopened files are Markdown documentation, not
# executable source, and no code reachable from them changes.
S2_A009_BUILD_LEARNING_REOPEN_AUTHORITY = (
    "SINGLE_USE_PAIRED_REOPEN_OF_CURRENT_STATE_MD_AND_BUILD_LEARNING_LEDGER_MD"
)

S2_A009_BUILD_LEARNING_REOPEN_CONTRACT = (
    "DOCUMENTATION_FILES_ONLY",
    "PAIRED_TRANSITION_BOTH_OR_NEITHER",
    "SINGLE_USE_REOPEN",
    "NO_SOURCE_CHANGE",
    "NO_MANIFEST_OR_LOCKFILE_CHANGE",
    "NO_WORKFLOW_CHANGE_BEYOND_ENTRYPOINT_MIGRATION",
    "NO_NEW_RUNTIME_AUTHORITY",
    "NO_NETWORK_EFFECT",
    "NO_PROCESS_AUTHORITY_GRANTED",
)

for _path, _expected in ((q.P, V65_P_BLOB), (q.T, V65_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v66 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v65_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v66 workflow does not reverse to exact canonical v65 predecessor: "
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


def req_v65(view: Any) -> None:
    for path, expected in ((q.P, V65_P_BLOB), (q.T, V65_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v66 candidate/base is missing frozen v65 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v65 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v65(view: Any) -> Any:
    """The reopened pair is not subject to any frozen-content check anywhere
    in the inherited cascade below the `docs_transition` route this
    successor's `delta()` intercepts directly - so the only projection any
    predecessor delegation ever needs is the ordinary workflow-entrypoint
    reversal every successor performs."""
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v65_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v65's view always; project the policy base
    only when it is a real post-v66 base. A pre-v66 bootstrap base predates
    the v65->v66 workflow migration and carries no v66 policy files, so it
    must reach v65's frozen hooks unprojected."""
    projected_candidate = _project_for_v65(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v65(policy_base)


def run_predecessor_selftests() -> None:
    """Run frozen v65's own self-tests once, under a v66->v65 workflow
    reversal.

    v65's corrected hooks are inherited by reference. Only ``read_bytes`` is
    wrapped here for the v66->v65 workflow reversal; the wrap is restored in
    ``finally``. No reopen-path projection is layered here: the reopened
    pair is not subject to any frozen-content check downstream, so a fresh
    ``LocalRepositoryView`` inventory of the real post-tranche head still
    matches what the frozen cascade expects.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v65_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v66 v65-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v65_selftest_read_bytes
    try:
        _call("v65 self-tests under v66->v65 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def _reopen_available(view: Any) -> bool:
    sides = []
    for path in sorted(REOPEN_FILES):
        if path not in V25.ps(view):
            base.fail(f"v66 reopen base is missing the frozen reopened path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        sides.append(actual == EXACT_FROZEN_BLOBS[path])
    if len(set(sides)) != 1:
        base.fail(
            "v66 reopen base is half-applied across the paired documentation "
            "transition: exactly one of the two paths has already moved"
        )
    return sides[0]


def _require_reopen_base(view: Any) -> None:
    if not _reopen_available(view):
        base.fail(
            "v66 S2-A009 Build Learning documentation-pair reopen already "
            "consumed; further changes require a new successor"
        )


def _verify_text_reopen_file(view: Any, path: str) -> None:
    if path not in V25.ps(view):
        base.fail(f"v66 reopen path missing: {path}")
    if V25.mode(view, path) != "100644":
        base.fail(f"v66 reopen path mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data:
        base.fail(f"v66 reopen path must not be empty: {path}")
    if len(data) > MAX_REOPEN_FILE_BYTES:
        base.fail(f"v66 reopen path exceeds bounded size: {path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"v66 reopen path must be UTF-8: {path}: {exc}")


def _verify_reopen_candidate(candidate: Any, policy_base: Any) -> None:
    _require_reopen_base(policy_base)
    for path in sorted(REOPEN_FILES):
        _verify_text_reopen_file(candidate, path)
    for relative in sorted(V25.FROZEN_STATE_PATHS):
        if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, V25.MAX_S1_STATE_BYTES
        ):
            base.fail(f"v66 candidate changed frozen S1 state: {relative}")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v66 bootstrap delta must be exactly two v66 policy files plus two integrity workflows"
                )
            base.fail(
                "v66 bootstrap base authorizes only exact S2-A009 Build "
                "Learning ledger reopen policy activation"
            )
        req_v65(candidate)
        req_v65(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v66 policy files are frozen after activation")

    reopen_changed = frozenset(paths & REOPEN_FILES)
    if reopen_changed:
        if paths != REOPEN_FILES:
            base.fail(
                "v66 Build Learning documentation-pair reopen must be exactly "
                "both paired paths and nothing else"
            )
        _verify_reopen_candidate(candidate, policy_base)
        return

    q.delta(_project_for_v65(candidate), _project_for_v65(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v65_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v66 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v66 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v66 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v66 steady-state controlled file drifted: {path}")

    reopen_safe = REOPEN_FILES & safe_paths & V25.ps(candidate)
    for path in sorted(reopen_safe):
        _verify_text_reopen_file(candidate, path)

    rest = frozenset(safe_paths - CONTROLLED_FILES - REOPEN_FILES)
    if rest:
        projected_candidate, projected_base = _v65_views(candidate, policy_base)
        q.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    # Only this successor's own new policy files are excluded before
    # delegating down. Unlike v65's reopened Rust test path, the reopened
    # documentation pair (`docs/canonical/CURRENT_STATE.md` in particular)
    # is a member of the base module's own `REQUIRED_PATHS`; stripping it
    # here would make the predecessor's stage-allowlist check report it as
    # missing from an otherwise-complete real tree. It is always allowed
    # to exist regardless of this successor, so it needs no special
    # handling at this layer - only `delta()`/`ext()`/`files()` need to
    # treat its *content* specially.
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        q.allowed(remaining, stage)


def files(view: Any) -> None:
    q.files(_project_for_v65(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v66 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v66 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v66 controlled file content drifted: {path}")
    if not _reopen_available(view):
        for path in sorted(REOPEN_FILES):
            _verify_text_reopen_file(view, path)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v66 predecessor component-base hook unavailable")
    path_set = set(paths)
    if path_set & REOPEN_FILES:
        remaining = path_set - REOPEN_FILES
        _call(
            "v66 projected predecessor component-base verifier",
            _PREDECESSOR_COMPONENT_BASE,
            _project_for_v65(view),
            remaining - CONTROLLED_FILES,
            allow_core_main_change=False,
        )
        return
    _call(
        "v66 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v65(view),
        path_set - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v66 predecessor S1 freeze hook unavailable")
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if paths == REOPEN_FILES:
        for relative in sorted(V25.FROZEN_STATE_PATHS):
            if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
                relative, V25.MAX_S1_STATE_BYTES
            ):
                base.fail(f"v66 candidate changed frozen S1 state: {relative}")
        return
    projected_candidate, projected_base = _v65_views(candidate, policy_base)
    _call(
        "v66 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v66=S2_A009_BUILD_LEARNING_LEDGER_REOPEN_ONLY")
    print(f"v66_authority={AUTH}")
    print(f"s2_implementation_authority_v66={S2_IMPLEMENTATION_AUTHORITY}")
    print(
        "s2_a009_build_learning_reopen_authority_v66="
        f"{S2_A009_BUILD_LEARNING_REOPEN_AUTHORITY}"
    )
    print(f"reopen_available_v66={_reopen_available(raw_root)}")
    print(f"doctor_cli_authority_v66={DOCTOR_CLI_AUTHORITY}")
    print(f"general_shell_authority_v66={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v66={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v66={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v66={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v66={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v66={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v66={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v66={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v66={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v66={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v66={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v66={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v66={SOURCE_ADMISSION}")
    print(f"dependency_admission_v66={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v66={S3_PLUS_AUTHORITY}")
    print(f"test_child_process_authority_v66={TEST_CHILD_PROCESS_AUTHORITY}")
    print(f"next_authority_gate_v66={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v66 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v66 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v66 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(q, name) != globals()[name]:
            base.fail(f"v66 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v65 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v65 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v65 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v65 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v65 files hook"), q.files),
        (_attr(shell, "print_success", "v65 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v66 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v66 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v66 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v66 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v66 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v66 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v66 allowed hook")
    _bind(shell, "verify_policy_files", files, "v66 files hook")
    _bind(shell, "print_success", printer, "v66 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v66 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v66 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_build_learning_ledger_reopen_v66_selftest import run

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
