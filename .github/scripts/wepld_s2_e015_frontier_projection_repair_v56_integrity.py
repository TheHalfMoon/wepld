#!/usr/bin/env python3
"""Repair one incorrect predecessor-selftest assumption in canonical v55 so the
already-authorized S2-E015 `identity_store_v1.rs` reopen can actually land.

v56 is an append-only policy successor over canonical v55 at main
decda273b27d1e9363382029afb8522a234ab649. It changes no product rule, grants no
new product or runtime authority, widens no path, and admits no source, process,
network, model/provider, or S3+ capability. Every v55 / v54 authority value is
inherited by reference and asserted unchanged, including
`TEST_CHILD_PROCESS_AUTHORITY = RE_EXEC_CURRENT_TEST_BINARY_ONLY` and every
`NONE` denial.

The defect. v55's `run_predecessor_selftests` (and `_project_for_v54`) state
that "the reopened path is not subject to any frozen-content check downstream",
and therefore reverse only the v55->v54 workflow entrypoint bytes before running
the frozen predecessor self-test cascade. That assumption is wrong. v36's
`REQUIRED_CANONICAL_FRONTIER_BLOBS` pins `crates/core/tests/identity_store_v1.rs`
to its exact pre-reopen blob, and v37's re-anchored `_req_canonical_frontier`
enforces that pin:

  * through v36's own self-test `_check_predecessor_and_frontier_are_exact`,
    which calls `req_canonical_frontier(root)` on every cascade;
  * through v38's self-test `p.p._req_canonical_frontier(final_view)` and v40's
    self-test `v37._req_canonical_frontier(final_view)`, whose views overlay
    only the two documentation paths and read every other frontier path,
    including this one, straight from the real tree.

So once the authorized reopened content is canonical, `foundation-integrity`
(candidate policy self-tests) and `s1-admission-integrity` fail closed with
`v37 canonical S2 frontier drifted: crates/core/tests/identity_store_v1.rs`,
even though v55 already authorized exactly this one transition. The reopens in
v52/v53/v54 did not hit this because `git_topology_v1.rs` and `project_v1.rs`
are not in v36's frontier set; `identity_store_v1.rs` is.

The repair. v56 replaces v55's `run_predecessor_selftests` with one that runs
the identical cascade but, for the single reopened path only, presents each
frozen predecessor with the exact historical pre-reopen bytes it was frozen
against - and it does so only after first proving the real tree is in an exact
allowed transition state.

  * `IDENTITY_STORE_TEST` must hash to exactly `PRE_REOPEN_BLOB` (the pin v36
    holds today, identical to v55's `EXACT_FROZEN_BLOB`) or to exactly
    `AUTHORIZED_POST_REOPEN_BLOB` (the exact blob of the finalized S2-E015
    fixture file). Any third value fails closed before any projection.
  * Only in the authorized POST state is the one path projected back, to the
    exact pre-reopen bytes carried inline here (zlib+base64, self-checked at
    load to hash to `PRE_REOPEN_BLOB`), so the projection needs no historical
    Git object (s1-admission checks out shallow).
  * Every other path - `identity.rs`, `evidence_store.rs`, `lib.rs`, the two
    documentation frontier paths, manifests, lockfiles, sources, workflows
    beyond the standard entrypoint migration - reads straight through, so no
    unrelated change is ever concealed from any predecessor, and every other
    frozen check still bites exactly as before.
  * `read_bytes` is method-wrapped (the class object is never rebound) and
    restored in `finally`.

Invariants this file makes explicit:

    HISTORICAL_PROJECTION != LIVE_STATE_ACCEPTANCE
    POLICY_PROJECTION_REPAIR != PRODUCT_CHANGE
    POLICY_PROJECTION_REPAIR != EVIDENCE
    AUTHORIZED_REOPEN != UNBOUNDED_FILE_MUTATION
    V56_POLICY_REPAIR != NEW_RUNTIME_AUTHORITY

Once `AUTHORIZED_POST_REOPEN_BLOB` is canonical the reopen is spent: v55's own
`_require_reopen_base` rejects any further change to the path (the base no
longer holds `EXACT_FROZEN_BLOB`), and v56's `_live_transition_side` rejects any
tree whose reopened path is neither pinned side. A later change to that path
needs a new explicit successor.

Package-load / resting-view note: v56 follows the v45..v55 discipline. It owns a
fresh `LocalRepositoryView` of the exact checked-out head, imports frozen v55
under an exact v56->v55 workflow-entrypoint reversal, and inherits every v55
hook by reference.
"""

from __future__ import annotations

import argparse
import base64
import importlib
import sys
import zlib
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_e015_frontier_projection_repair_v56_integrity.py"
T = ".github/scripts/wepld_s2_e015_frontier_projection_repair_v56_selftest.py"
T_BLOB = "aa19021f5a4f23ecc8730a1ca19b39cc237d1ae2"

V55_P_BLOB = "deea05f7f8a487637b1166d8ea7b5b5607ea597e"
V55_T_BLOB = "039f094549168357f6542537bcd6641c28f449e3"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V56_ENTRYPOINT = b"wepld_s2_e015_frontier_projection_repair_v56_integrity.py"
_V55_ENTRYPOINT = b"wepld_s2_git_topology_evidence_reopen_v55_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Do not inherit a predecessor module's resting/projection view. v56 bases all
# of its own exact-head and predecessor projections on the actual checked-out
# repository bytes.
raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v55_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V56_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v56 workflow entrypoint count drifted before v55 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V56_ENTRYPOINT, _V55_ENTRYPOINT)


def _import_v55_under_workflow_projection() -> Any:
    """Import frozen v55 while it observes exact v55 workflow bytes.

    v55 (hence v54..v36) reads workflow bytes while its module is imported, and
    the v55->v56 entrypoint migration ships in this same candidate, so v55 must
    not observe its own successor's bytes. Only ``LocalRepositoryView.read_bytes``
    is wrapped for the duration of the import and then restored in ``finally`` -
    the class object itself is never rebound.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v55_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v55_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v56 v55-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v55_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_git_topology_evidence_reopen_v55_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v55_under_workflow_projection()

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

# --- the one repair: exact S2-E015 canonical-frontier historical projection ---
IDENTITY_STORE_TEST = "crates/core/tests/identity_store_v1.rs"

# The exact pre-reopen blob v36's REQUIRED_CANONICAL_FRONTIER_BLOBS holds for the
# reopened path, identical to v55's EXACT_FROZEN_BLOB. This is the historical
# view every frozen predecessor was written against.
PRE_REOPEN_BLOB = "fc1fd55c47e5bb6879b8c5bb03cd0500bedcff0f"

# The single authorized post-reopen blob: git hash-object of the finalized
# S2-E015 fixture file (module docstring updated + one appended test). No third
# blob is ever accepted.
AUTHORIZED_POST_REOPEN_BLOB = "ebf56a37b17d3802c7de072093518ae55a1222bb"

# Exact pre-reopen bytes of the one projected path, carried inline so the
# historical projection is hermetic and needs no historical Git object. The
# post-reopen bytes are carried too so the authorized transition target is fully
# auditable and self-checked; only the pre-reopen bytes are ever presented
# downstream.
_PRE_REOPEN_B64 = (
    "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"
)
_POST_REOPEN_B64 = (
    "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"
)
_PRE_REOPEN_BYTES = zlib.decompress(base64.b64decode(_PRE_REOPEN_B64))
_POST_REOPEN_BYTES = zlib.decompress(base64.b64decode(_POST_REOPEN_B64))

if V25.blob(_PRE_REOPEN_BYTES) != PRE_REOPEN_BLOB:
    base.fail("v56 embedded pre-reopen bytes do not hash to PRE_REOPEN_BLOB")
if V25.blob(_POST_REOPEN_BYTES) != AUTHORIZED_POST_REOPEN_BLOB:
    base.fail("v56 embedded post-reopen bytes do not hash to AUTHORIZED_POST_REOPEN_BLOB")
if PRE_REOPEN_BLOB != q.EXACT_FROZEN_BLOB:
    base.fail(
        "v56 PRE_REOPEN_BLOB must equal the inherited v55 EXACT_FROZEN_BLOB: "
        f"{PRE_REOPEN_BLOB} != {q.EXACT_FROZEN_BLOB}"
    )
if AUTHORIZED_POST_REOPEN_BLOB == PRE_REOPEN_BLOB:
    base.fail("v56 authorized post-reopen blob must differ from the pre-reopen blob")
if not base.OBJECT_SHA_RE.fullmatch(AUTHORIZED_POST_REOPEN_BLOB):
    base.fail("v56 authorized post-reopen blob is malformed")
if len(_POST_REOPEN_BYTES) > q.MAX_REOPEN_FILE_BYTES:
    base.fail("v56 embedded post-reopen bytes exceed the v55 reopen size bound")

AUTH = "S2_E015_CANONICAL_FRONTIER_PROJECTION_REPAIR_ONLY"
HISTORICAL_PROJECTION = "HISTORICAL_VIEW_ONLY"
POLICY_PROJECTION_REPAIR = "NOT_PRODUCT_CHANGE_NOT_EVIDENCE"
V56_POLICY_REPAIR = "NOT_NEW_RUNTIME_AUTHORITY"
AUTHORIZED_REOPEN_BOUND = "NOT_UNBOUNDED_FILE_MUTATION"
NEXT_AUTHORITY_GATE = "S2-ACCEPTANCE"

# Every authority value is inherited from frozen v55 by reference and asserted
# unchanged in overlay().
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
)
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(q, _name)

for _path, _expected in ((q.P, V55_P_BLOB), (q.T, V55_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v56 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v55_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v56 workflow does not reverse to exact canonical v55 predecessor: "
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


def req_v55(view: Any) -> None:
    for path, expected in ((q.P, V55_P_BLOB), (q.T, V55_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v56 candidate/base is missing frozen v55 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v55 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v55(view: Any) -> Any:
    """Project a candidate/base view to exactly v55's expected view: the
    standard v56->v55 workflow-entrypoint reversal, and v56's own two policy
    files hidden. The reopened path is deliberately not touched here - v55's
    own `delta()` / `files()` / `ext()` handle it, and every other frozen
    check must still see the real bytes."""
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v55_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    projected_candidate = _project_for_v55(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v55(policy_base)


def _live_transition_side(view: Any) -> str:
    """Prove the real tree's one reopened path is in an exact allowed
    transition state. HISTORICAL_PROJECTION != LIVE_STATE_ACCEPTANCE: no
    historical view is ever presented downstream until this has passed.
    """
    if IDENTITY_STORE_TEST not in V25.ps(view):
        base.fail(f"v56 requires the reopened frontier path: {IDENTITY_STORE_TEST}")
    actual = V25.blob(view.read_bytes(IDENTITY_STORE_TEST, base.MAX_POLICY_FILE_BYTES))
    if actual == PRE_REOPEN_BLOB:
        return "PRE"
    if actual == AUTHORIZED_POST_REOPEN_BLOB:
        return "POST"
    base.fail(
        "v56 S2-E015 identity_store_v1.rs is neither pinned transition side: "
        f"expected {PRE_REOPEN_BLOB} or {AUTHORIZED_POST_REOPEN_BLOB} "
        f"actual={actual}"
    )
    raise AssertionError("unreachable")


def _selftest_read_bytes_wrapper(
    original: Any, workflow_reversal: dict[str, bytes], side: str
) -> Any:
    """Return a `LocalRepositoryView.read_bytes` replacement for the predecessor
    self-test cascade: the v56->v55 workflow reversal always, plus - only when
    the live tree already holds the authorized post-reopen content - the single
    reopened path projected back to its exact pre-reopen bytes. Every other path
    reads straight through the original.
    """

    def _wrapped(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v56 self-test workflow projection exceeds read bound: {relative}"
                )
            return data
        if side == "POST" and relative == IDENTITY_STORE_TEST:
            if len(_PRE_REOPEN_BYTES) > limit:
                base.fail(
                    "v56 historical frontier projection exceeds read bound: "
                    f"{relative}"
                )
            return _PRE_REOPEN_BYTES
        return original(local_view, relative, limit)

    return _wrapped


def run_predecessor_selftests() -> None:
    """Run frozen v55's own self-tests once, under the v56->v55 workflow
    reversal plus the exact S2-E015 canonical-frontier historical projection.

    The live transition state is proven first (`_live_transition_side`): the
    reopened path must hash to exactly `PRE_REOPEN_BLOB` or exactly
    `AUTHORIZED_POST_REOPEN_BLOB`, or this fails closed before any wrap is
    installed - a predecessor projection can never conceal an unauthorized
    underlying blob. Only the authorized POST state projects the one path back
    to its exact pre-reopen bytes; PRE needs no projection and the wrap is then
    byte-identical to what v55 already does. `read_bytes` is method-wrapped and
    restored in `finally`.
    """
    side = _live_transition_side(raw_root)
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes
    base.LocalRepositoryView.read_bytes = _selftest_read_bytes_wrapper(
        original_read_bytes, workflow_reversal, side
    )
    try:
        _call(
            "v55 self-tests under v56->v55 workflow reversal + S2-E015 frontier projection",
            q.selftest,
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v56 bootstrap delta must be exactly two v56 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v56 bootstrap base authorizes only exact frontier-projection-repair "
                "policy activation"
            )
        req_v55(candidate)
        req_v55(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v56 policy files are frozen after activation")

    q.delta(_project_for_v55(candidate), _project_for_v55(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v55_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v56 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v56 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(
                    f"v56 controlled file unexpectedly exists in bootstrap base: {path}"
                )
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v56 steady-state controlled file drifted: {path}")

    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _v55_views(candidate, policy_base)
        q.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        q.allowed(remaining, stage)


def files(view: Any) -> None:
    q.files(_project_for_v55(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v56 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v56 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v56 controlled file content drifted: {path}")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v56 predecessor component-base hook unavailable")
    _call(
        "v56 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v55(view),
        set(paths) - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v56 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v55_views(candidate, policy_base)
    _call(
        "v56 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v56=S2_E015_CANONICAL_FRONTIER_PROJECTION_REPAIR_ONLY")
    print(f"v56_authority={AUTH}")
    print(f"v56_policy_repair={V56_POLICY_REPAIR}")
    print(f"historical_projection_v56={HISTORICAL_PROJECTION}")
    print(f"policy_projection_repair_v56={POLICY_PROJECTION_REPAIR}")
    print(f"authorized_reopen_bound_v56={AUTHORIZED_REOPEN_BOUND}")
    print(f"pre_reopen_blob_v56={PRE_REOPEN_BLOB}")
    print(f"authorized_post_reopen_blob_v56={AUTHORIZED_POST_REOPEN_BLOB}")
    print(f"live_transition_side_v56={_live_transition_side(raw_root)}")
    print(f"test_child_process_authority_v56={TEST_CHILD_PROCESS_AUTHORITY}")
    print(f"general_shell_authority_v56={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v56={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v56={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v56={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v56={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v56={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v56={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v56={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v56={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v56={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v56={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v56={MODEL_PROVIDER_EXECUTION}")
    print(f"doctor_cli_authority_v56={DOCTOR_CLI_AUTHORITY}")
    print(f"source_admission_v56={SOURCE_ADMISSION}")
    print(f"dependency_admission_v56={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v56={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v56={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v56 predecessor workflow identity map drifted: actual={current}")
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
        (
            _attr(execution, "_verify_component_base", "component-base hook"),
            verify_component_base,
        ),
        (
            _attr(execution, "freeze_s1_007_state", "S1 state freeze hook"),
            freeze_s1_007_state,
        ),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v56 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v56 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(q, name) != globals()[name]:
            base.fail(f"v56 inherited authority drifted: {name}")
    if q.EXACT_FROZEN_BLOB != PRE_REOPEN_BLOB:
        base.fail("v56 inherited v55 reopen pin drifted")
    if getattr(q, "run_predecessor_selftests", None) is None:
        base.fail("v56 predecessor selftest driver unavailable")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v55 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (
            _attr(desktop, "verify_extension_controlled_paths", "v55 desktop hook"),
            q.dext,
        ),
        (
            _attr(execution, "verify_extension_controlled_paths", "v55 execution hook"),
            q.eext,
        ),
        (_attr(shell, "validate_allowed_paths", "v55 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v55 files hook"), q.files),
        (_attr(shell, "print_success", "v55 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v56 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v56 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v56 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v56 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v56 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v56 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v56 allowed hook")
    _bind(shell, "verify_policy_files", files, "v56 files hook")
    _bind(shell, "print_success", printer, "v56 printer hook")
    _bind(
        execution,
        "_verify_component_base",
        verify_component_base,
        "v56 component-base hook",
    )
    _bind(
        execution,
        "freeze_s1_007_state",
        freeze_s1_007_state,
        "v56 S1 state freeze hook",
    )
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_e015_frontier_projection_repair_v56_selftest import run

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
