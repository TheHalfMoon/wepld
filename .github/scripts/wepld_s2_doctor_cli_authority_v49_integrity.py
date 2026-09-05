#!/usr/bin/env python3
"""Authorize only the bounded S2-AUTH-015 Doctor + CLI local projection tranche.

v49 is an append-only policy successor over canonical v48 at main
24791b11196106f0440ca01aa5344a5168e650f8. It executes S2-AUTH-015 only.

It grants deterministic-projection / orchestration authority for the Project
Doctor and the ``wepld open|doctor|status`` command surface: consuming
already-qualified S2 observations (locator, Git topology, identity, local
evidence store) and rendering typed human/JSON results and stable exit classes.

It does NOT grant a general terminal/process facility, shell execution,
project-native command execution, package installation, model/provider
execution, network access, Git mutation, ``safe.directory`` mutation, executable
remediation, source/dependency admission, or S3+ authority. Every one of those
remains ``NONE`` and is asserted unchanged against the inherited v48 chain.

The product tranche is a second stage after policy activation. The initial
product candidate must change exactly:

    crates/core/src/doctor.rs
    crates/core/src/cli.rs
    crates/core/src/bin/wepld.rs
    crates/core/src/lib.rs
    crates/core/tests/doctor_v1.rs
    crates/core/tests/cli_v1.rs

and must be based on the exact frozen S2 frontier. ``lib.rs`` may gain exactly
two lines - ``pub mod cli;`` and ``pub mod doctor;`` - and nothing else; the
rest of ``lib.rs`` must byte-equal the frozen canonical blob. No
``pub use cli::{...}`` / ``pub use doctor::{...}`` re-export block: tests import
via ``wepld_core::cli::`` / ``wepld_core::doctor::``. Once that tranche lands,
v49 freezes it until a later authority successor.

Package-load / resting-view note: v49 follows the v46..v48 discipline. It owns a
fresh ``LocalRepositoryView`` of the exact checked-out head, imports frozen v48
under an exact v49->v48 workflow-entrypoint reversal, inherits every v48 hook by
reference, and projects its own Doctor/CLI tranche away (the two ``lib.rs``
lines stripped, the five new files hidden, failing closed on a partial tranche)
before delegating to the frozen v48 cascade - exactly the projection every
runtime/admission path uses. The class object is never rebound; only
``LocalRepositoryView.read_bytes`` is method-wrapped and each ``wepld_*`` module
root is wrapped in v47's ``_EntryHidingView``; every wrap is restored in
``finally``.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_doctor_cli_authority_v49_integrity.py"
T = ".github/scripts/wepld_s2_doctor_cli_authority_v49_selftest.py"
T_BLOB = "a5eec317d93e8e316a23c06b9ee1b94a6faf5565"

V48_P_BLOB = "69ac03eb9174cce9b8807ee071faf526a9b02c8c"
V48_T_BLOB = "c2ba6d1d976a2a86879e970966291f4d08b98729"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V49_ENTRYPOINT = b"wepld_s2_doctor_cli_authority_v49_integrity.py"
_V48_ENTRYPOINT = b"wepld_s2_git_topology_product_selftest_repair_v48_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Do not inherit a predecessor module's resting/projection view. v49 bases all
# of its own exact-head and predecessor projections on the actual checked-out
# repository bytes.
raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v48_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V49_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v49 workflow entrypoint count drifted before v48 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V49_ENTRYPOINT, _V48_ENTRYPOINT)


def _import_v48_under_workflow_projection() -> Any:
    """Import frozen v48 while it observes exact v48 workflow bytes.

    v48 (hence v47..v45..v36) reads workflow bytes while its module is imported,
    and the v48->v49 entrypoint migration ships in this same candidate, so v48
    must not observe its own successor's bytes. Only
    ``LocalRepositoryView.read_bytes`` is wrapped for the duration of the import
    and then restored in ``finally`` - the class object itself is never rebound,
    so v20's frozen constructor guard still captures and later sees the exact
    canonical ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v48_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v48_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v49 v48-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v48_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_git_topology_product_selftest_repair_v48_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v48_under_workflow_projection()

V25 = q.V25
CW = q.CW
Q_WF = dict(q.WF)
_attr = q._attr
_bind = q._bind
_call = q._call
_ProjectionView = q._ProjectionView
_EntryHidingView = q.q._EntryHidingView
_INST = False
_PREDECESSOR_COMPONENT_BASE: Any = None
_PREDECESSOR_FREEZE_S1: Any = None

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

# --- Doctor/CLI product tranche path allowlist (second stage) ---
CORE_EXPORT = "crates/core/src/lib.rs"
DOCTOR_MODULE = "crates/core/src/doctor.rs"
CLI_MODULE = "crates/core/src/cli.rs"
CLI_BIN = "crates/core/src/bin/wepld.rs"
DOCTOR_TEST = "crates/core/tests/doctor_v1.rs"
CLI_TEST = "crates/core/tests/cli_v1.rs"
PRODUCT_FILES = frozenset(
    {CORE_EXPORT, DOCTOR_MODULE, CLI_MODULE, CLI_BIN, DOCTOR_TEST, CLI_TEST}
)
PRODUCT_NEW_FILES = frozenset(
    {DOCTOR_MODULE, CLI_MODULE, CLI_BIN, DOCTOR_TEST, CLI_TEST}
)
CORE_PREFIX = "crates/core/"
CORE_MANIFEST = "crates/core/Cargo.toml"
ROOT_CARGO = "Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"

MAX_PRODUCT_FILE_BYTES = 262_144

PRODUCT_TASKS = frozenset(
    {
        "S2-D001",
        "S2-D002",
        "S2-D003",
        "S2-D004",
        "S2-D005",
        "S2-D006",
        "S2-D007",
        "S2-D008",
        "S2-D009",
        "S2-D010",
        "S2-D011",
        "S2-D012",
        "S2-D013",
        "S2-D014",
        "S2-D015",
        "S2-CLI001",
        "S2-CLI002",
        "S2-CLI003",
        "S2-CLI004",
        "S2-CLI005",
        "S2-CLI006",
        "S2-CLI007",
        "S2-CLI008",
        "S2-CLI009",
        "S2-CLI010",
        "S2-S008",
        "S2-S013",
        "S2-S014",
        "S2-S015",
    }
)

REQUIRED_PRODUCT_BASE_BLOBS = {
    CORE_EXPORT: "47b5a4cf1749ab4adb16d27d93f87b3c85ee6427",
}

AUTH = "S2_AUTH_015_EXACT_DOCTOR_CLI_PROJECTION_TRANCHE"
S2_IMPLEMENTATION_AUTHORITY = (
    "EXACT_DOCTOR_CLI_PROJECTION_TRANCHE_ONLY_AFTER_V49_ACTIVATION"
)
DEPENDENCY_ADMISSION = q.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = q.SOURCE_ADMISSION
GIT_ROUTE_DECISION = q.GIT_ROUTE_DECISION
GIT_PROCESS_ADMISSION = q.GIT_PROCESS_ADMISSION
EXTERNAL_PROCESS_AUTHORITY = q.EXTERNAL_PROCESS_AUTHORITY
GIT_EXECUTION_AUTHORITY = q.GIT_EXECUTION_AUTHORITY
NETWORK_AUTHORITY = q.NETWORK_AUTHORITY
MODEL_PROVIDER_EXECUTION = q.MODEL_PROVIDER_EXECUTION
DOCTOR_CLI_AUTHORITY = "DETERMINISTIC_LOCAL_PROJECTION_ORCHESTRATION_ONLY"
S3_PLUS_AUTHORITY = q.S3_PLUS_AUTHORITY
NEXT_AUTHORITY_GATE = "S2-ACCEPTANCE"

# Standing denials this successor must not relax.
GENERAL_SHELL_AUTHORITY = "NONE"
ARBITRARY_PROCESS_AUTHORITY = "NONE"
PACKAGE_INSTALL_AUTHORITY = "NONE"
PROJECT_NATIVE_COMMAND_EXECUTION = "NONE"
GIT_MUTATION_AUTHORITY = "NONE"
SAFE_DIRECTORY_MUTATION_AUTHORITY = "NONE"
REMEDIATION_EXECUTION_AUTHORITY = "NONE"

DOCTOR_CLI_PROJECTION_CONTRACT = (
    "CONSUME_TYPED_S2_OBSERVATIONS_ONLY",
    "UNAVAILABLE_IS_NOT_HEALTHY",
    "STALE_IS_NOT_FRESH",
    "PARTIAL_IS_NOT_COMPLETE",
    "TRUST_REFUSED_IS_NOT_TRUSTED",
    "NO_IMPLICIT_INSTALL_UPDATE_FIX_BUILD_TEST_RUN_FETCH",
    "NO_REMOTE_OR_SAFE_DIRECTORY_MUTATION",
    "PRESERVE_NATIVE_GIT_TRUST_REFUSAL",
    "ALLOWLISTED_STRUCTURED_FIELDS_ONLY",
    "WEPLD_OWNED_TEMPLATES_ONLY",
    "TERMINAL_CONTROL_SEQUENCE_DEFENSE",
    "VERSIONED_DETERMINISTIC_JSON",
    "HUMAN_AND_JSON_FROM_ONE_REDACTED_MODEL",
    "READ_ONLY_TARGET_PROJECT",
    "NO_REQUIRED_NETWORK_EFFECT",
    "DIGEST_EQUALITY_IS_NOT_AUTHENTICITY",
)
DOCTOR_CLI_COMMAND_SURFACE = ("open", "doctor", "status")
DOCTOR_CLI_EXIT_CLASSES = (
    "0:success",
    "2:usage_or_input_error",
    "3:project_resolution_or_identity_error",
    "4:evidence_store_integrity_error",
    "5:doctor_completed_with_blocking_findings",
    "6:required_capability_unavailable",
    "1:unexpected_internal_failure",
)

for _path, _expected in ((q.P, V48_P_BLOB), (q.T, V48_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v49 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v48_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v49 workflow does not reverse to exact canonical v48 predecessor: "
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


def req_v48(view: Any) -> None:
    for path, expected in ((q.P, V48_P_BLOB), (q.T, V48_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v49 candidate/base is missing frozen v48 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v48 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _product_presence(view: Any) -> frozenset[str]:
    return frozenset(PRODUCT_NEW_FILES & V25.ps(view))


_MOD_CLI_LINE = b"pub mod cli;\n"
_MOD_DOCTOR_LINE = b"pub mod doctor;\n"


def _strip_doctor_cli_exports(lib: bytes) -> bytes:
    """Reverse exactly the two authorized ``pub mod`` additions, position
    independent, from whatever bytes are actually present. Fail closed on any
    other shape so a malformed post-tranche ``lib.rs`` stops here rather than
    reaching the frozen v48 cascade."""
    out = lib
    for line in (_MOD_CLI_LINE, _MOD_DOCTOR_LINE):
        if out.count(line) != 1:
            base.fail("v49 Doctor/CLI tranche export lines have an unexpected shape")
        out = out.replace(line, b"", 1)
    return out


def _doctor_cli_product_projection(view: Any) -> tuple[dict[str, bytes], frozenset[str]]:
    present = _product_presence(view)
    if not present:
        return {}, frozenset()
    if present != PRODUCT_NEW_FILES:
        base.fail(
            f"v49 predecessor view contains partial Doctor/CLI tranche: {sorted(present)}"
        )
    lib = view.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if lib.count(_MOD_CLI_LINE) != 1 or lib.count(_MOD_DOCTOR_LINE) != 1:
        base.fail("v49 Doctor/CLI tranche must register cli and doctor exactly once each")
    return {CORE_EXPORT: _strip_doctor_cli_exports(lib)}, PRODUCT_NEW_FILES


def _project_for_v48(view: Any) -> Any:
    replacements = _workflow_replacements(view)
    product_replacements, omitted = _doctor_cli_product_projection(view)
    replacements.update(product_replacements)
    return _ProjectionView(view, replacements, POLICY_FILES | omitted)


def _v48_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v48's view always; project the policy base only
    when it is a real post-v49 base. A pre-v49 bootstrap base predates the
    v48->v49 workflow migration and carries no v49 policy files, so it must
    reach v48's frozen hooks unprojected."""
    projected_candidate = _project_for_v48(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v48(policy_base)


def _boot_base_for_selftest() -> Any:
    return _project_for_v48(raw_root)


def run_predecessor_selftests() -> None:
    """Run frozen v48's own self-tests once, under a v49->v48 workflow reversal.

    v48's corrected hooks are inherited by reference. Only ``read_bytes`` is
    wrapped here for the v49->v48 workflow reversal; the wrap is restored in
    ``finally``. The Doctor/CLI product projection is not layered here: v49's
    dedicated self-tests exercise the tracked-tranche state directly, and on a
    real post-tranche head the five new files are genuinely tracked so a fresh
    ``LocalRepositoryView`` inventory still matches exact HEAD.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v48_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    "v49 v48-selftest workflow projection exceeds read bound: "
                    f"{relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v48_selftest_read_bytes
    try:
        _call("v48 self-tests under v49->v48 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def _require_product_base(view: Any) -> None:
    paths = V25.ps(view)
    if _product_presence(view):
        base.fail(
            "v49 product base already contains the Doctor/CLI tranche; "
            "later edits require successor authority"
        )
    for path, expected in REQUIRED_PRODUCT_BASE_BLOBS.items():
        if path not in paths:
            base.fail(f"v49 product base frontier missing: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v49 product base frontier drifted: {path}: "
                f"expected={expected} actual={actual}"
            )
    for path in sorted(PRODUCT_NEW_FILES):
        if path in paths:
            base.fail(f"v49 product base frontier unexpectedly contains new path: {path}")


def _verify_text_product_file(view: Any, path: str) -> None:
    if path not in V25.ps(view):
        base.fail(f"v49 product path missing: {path}")
    if V25.mode(view, path) != "100644":
        base.fail(f"v49 product path mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data:
        base.fail(f"v49 product path must not be empty: {path}")
    if len(data) > MAX_PRODUCT_FILE_BYTES:
        base.fail(f"v49 product path exceeds bounded size: {path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"v49 product path must be UTF-8: {path}: {exc}")


def _verify_product_candidate(candidate: Any, policy_base: Any) -> None:
    _require_product_base(policy_base)
    if _product_presence(candidate) != PRODUCT_NEW_FILES:
        base.fail("v49 candidate must contain the complete Doctor/CLI module/bin/test set")
    for path in sorted(PRODUCT_FILES):
        _verify_text_product_file(candidate, path)
    lib = candidate.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if lib.count(_MOD_CLI_LINE) != 1 or lib.count(_MOD_DOCTOR_LINE) != 1:
        base.fail("v49 Core export must register cli and doctor exactly once each")
    stripped = _strip_doctor_cli_exports(lib)
    if V25.blob(stripped) != REQUIRED_PRODUCT_BASE_BLOBS[CORE_EXPORT]:
        base.fail(
            "v49 Doctor/CLI Core-export delta is not exactly the two authorized module lines"
        )
    changed = V25.changed(V25.v24.v23, candidate, policy_base)
    for path in (CORE_MANIFEST, ROOT_CARGO, ROOT_CARGO_LOCK):
        if path in changed:
            base.fail(
                f"v49 Doctor/CLI tranche must not change dependency/manifest path: {path}"
            )
    for relative in sorted(set(V25.FROZEN_STATE_PATHS) - {CORE_EXPORT}):
        if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, V25.MAX_S1_STATE_BYTES
        ):
            base.fail(f"v49 Doctor/CLI candidate changed frozen S1 state: {relative}")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v49 bootstrap delta must be exactly two v49 policy files plus two integrity workflows"
                )
            base.fail("v49 bootstrap base authorizes only exact S2-AUTH-015 policy activation")
        req_v48(candidate)
        req_v48(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v49 policy files are frozen after activation")

    product_changed = frozenset(paths & PRODUCT_FILES)
    if product_changed:
        if _product_presence(policy_base):
            base.fail("v49 Doctor/CLI product tranche is frozen after first canonical landing")
        if paths != PRODUCT_FILES or product_changed != PRODUCT_FILES:
            if paths - PRODUCT_FILES:
                base.fail("v49 Doctor/CLI product must not mix with non-product paths")
            base.fail("v49 initial Doctor/CLI delta must change exact module/bin/export/test set")
        _verify_product_candidate(candidate, policy_base)
        return

    q.delta(_project_for_v48(candidate), _project_for_v48(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v48_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v49 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v49 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v49 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v49 steady-state controlled file drifted: {path}")

    product_safe = PRODUCT_FILES & safe_paths & V25.ps(candidate)
    for path in sorted(product_safe):
        _verify_text_product_file(candidate, path)

    rest = frozenset(safe_paths - CONTROLLED_FILES - PRODUCT_FILES)
    if rest:
        projected_candidate, projected_base = _v48_views(candidate, policy_base)
        q.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES - PRODUCT_FILES
    if remaining:
        q.allowed(remaining, stage)


def files(view: Any) -> None:
    q.files(_project_for_v48(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v49 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v49 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v49 controlled file content drifted: {path}")
    present = _product_presence(view)
    if present:
        if present != PRODUCT_NEW_FILES:
            base.fail("v49 canonical view contains partial Doctor/CLI product tranche")
        for path in sorted(PRODUCT_FILES):
            _verify_text_product_file(view, path)
        lib = view.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
        if lib.count(_MOD_CLI_LINE) != 1 or lib.count(_MOD_DOCTOR_LINE) != 1:
            base.fail("v49 canonical Core export must register cli and doctor exactly once each")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v49 predecessor component-base hook unavailable")
    path_set = set(paths)
    if path_set & PRODUCT_FILES:
        if not PRODUCT_NEW_FILES <= V25.ps(view):
            base.fail("v49 component-base view contains incomplete Doctor/CLI tranche")
        remaining = path_set - PRODUCT_FILES
        _call(
            "v49 projected predecessor component-base verifier",
            _PREDECESSOR_COMPONENT_BASE,
            _project_for_v48(view),
            remaining - CONTROLLED_FILES,
            allow_core_main_change=False,
        )
        return
    _call(
        "v49 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v48(view),
        path_set - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v49 predecessor S1 freeze hook unavailable")
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if paths == PRODUCT_FILES:
        for relative in sorted(set(V25.FROZEN_STATE_PATHS) - {CORE_EXPORT}):
            if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
                relative, V25.MAX_S1_STATE_BYTES
            ):
                base.fail(f"v49 Doctor/CLI candidate changed frozen S1 state: {relative}")
        return
    projected_candidate, projected_base = _v48_views(candidate, policy_base)
    _call(
        "v49 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v49=S2_AUTH_015_EXACT_DOCTOR_CLI_PROJECTION_TRANCHE")
    print(f"v49_authority={AUTH}")
    print(f"s2_implementation_authority_v49={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"doctor_cli_authority_v49={DOCTOR_CLI_AUTHORITY}")
    print(f"general_shell_authority_v49={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v49={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v49={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v49={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v49={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v49={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v49={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v49={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v49={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v49={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v49={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v49={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v49={SOURCE_ADMISSION}")
    print(f"dependency_admission_v49={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v49={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v49={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v49 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v49 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v49 workflow identity projection drifted")
    if q.DOCTOR_CLI_AUTHORITY != "NONE":
        base.fail("v49 inherited v48 Doctor/CLI denial drifted")
    for name in (
        "NETWORK_AUTHORITY",
        "MODEL_PROVIDER_EXECUTION",
        "S3_PLUS_AUTHORITY",
        "GIT_PROCESS_ADMISSION",
        "GIT_EXECUTION_AUTHORITY",
        "EXTERNAL_PROCESS_AUTHORITY",
        "GIT_ROUTE_DECISION",
        "SOURCE_ADMISSION",
        "DEPENDENCY_ADMISSION",
    ):
        if getattr(q, name) != globals()[name]:
            base.fail(f"v49 inherited authority drifted: {name}")


def _install_predecessor_under_doctor_cli_projection(_install_run: Any = None) -> None:
    """Run the frozen v48 (hence v47..v45) ``install()`` under v49's own
    Doctor/CLI product projection when the tranche is tracked.

    Frozen v45's ``_core_export_baseline`` (via v33) is re-evaluated on every
    install-time path; once ``lib.rs`` carries the two ``pub mod`` lines in the
    tracked tree it would be rejected. The projection here is exactly the one
    every verification hook uses: the two lines stripped, the five new files
    hidden from each ``wepld_*`` module root via v47's ``_EntryHidingView``.
    ``read_bytes`` is method-wrapped (class object untouched); both are restored
    in ``finally``. When no tranche is tracked the delegation is bare.
    """
    run = q.install if _install_run is None else _install_run
    product_replacements, product_omitted = _doctor_cli_product_projection(
        _ProjectionView(raw_root, {}, POLICY_FILES)
    )
    if not product_replacements and not product_omitted:
        run()
        return

    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in product_replacements:
            data = product_replacements[relative]
            if len(data) > limit:
                base.fail(
                    f"v49 install product projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    patched_roots: list[tuple[Any, str, Any]] = []
    for name, module in list(sys.modules.items()):
        if not name.startswith("wepld_") or module is None:
            continue
        for attr in ("root", "raw_root"):
            current = getattr(module, attr, None)
            if current is None:
                continue
            patched_roots.append((module, attr, current))
            setattr(module, attr, _EntryHidingView(current, product_omitted))

    base.LocalRepositoryView.read_bytes = _read_bytes
    try:
        run()
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes
        for module, attr, original in reversed(patched_roots):
            setattr(module, attr, original)


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    _install_predecessor_under_doctor_cli_projection()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v48 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v48 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v48 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v48 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v48 files hook"), q.files),
        (_attr(shell, "print_success", "v48 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v49 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v49 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v49 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v49 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v49 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v49 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v49 allowed hook")
    _bind(shell, "verify_policy_files", files, "v49 files hook")
    _bind(shell, "print_success", printer, "v49 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v49 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v49 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_doctor_cli_authority_v49_selftest import run

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
