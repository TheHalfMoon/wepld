#!/usr/bin/env python3
"""Repair v49 predecessor self-tests for the authorized Doctor/CLI post-tranche state.

Canonical v49 authorizes the S2-AUTH-015 Doctor + CLI product tranche. Its
``run_predecessor_selftests`` reverses only the v49->v48 workflow entrypoint
migration before delegating to frozen v48's own self-tests; it does not layer
v49's Doctor/CLI product projection. Once the tranche is tracked (``lib.rs``
carries ``pub mod cli;`` + ``pub mod doctor;`` and the five new module/bin/test
files exist), the frozen v33 Core-export self-test inside that cascade therefore
observes an export identity it never admitted and fails with
``v33 Core export is neither the exact canonical baseline nor the exact
authorized tranche export`` before Rust qualification begins. ``foundation-
integrity`` runs ``v49_integrity.py selftest`` unconditionally on
``pull_request``, so the first real Doctor/CLI product candidate's CI would be
red without this repair.

v50 changes no product rule and grants no new authority. It supersedes only that
one self-test seam: while frozen v49 runs its predecessor self-test cascade,
v49's own Doctor/CLI product projection (the two ``lib.rs`` export lines stripped,
the five new files hidden, failing closed on a partial tranche) is layered on
top of the ordinary v49->v48 workflow reversal, exactly the projection every
runtime/admission path already uses. All temporary roots/classes/functions are
restored in ``finally`` blocks; the ``base.LocalRepositoryView`` class object is
never rebound.

Every inherited v49 value -- the Doctor/CLI projection authority, the standing
``NONE`` denials for shell / arbitrary process / package install / project-native
command execution / Git mutation / ``safe.directory`` mutation / executable
remediation / network / model-provider execution / S3+, the closed Git argv, the
staged dependency admission, and ``next_authority_gate = S2-ACCEPTANCE`` -- is
carried through byte-for-byte and asserted unchanged. The product tranche
remains the exact six paths v49 already granted.
"""

from __future__ import annotations

import argparse
import importlib
import itertools
from pathlib import Path
import sys
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_v49_doctor_cli_selftest_projection_repair_v50_integrity.py"
T = ".github/scripts/wepld_s2_v49_doctor_cli_selftest_projection_repair_v50_selftest.py"
T_BLOB = "418645059a4625fb2734f97ee1a5e909d4512615"

V49_P_BLOB = "23c2aa08ed5b9c6310e0f72414982342ddaec8ba"
V49_T_BLOB = "a5eec317d93e8e316a23c06b9ee1b94a6faf5565"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V50_ENTRYPOINT = b"wepld_s2_v49_doctor_cli_selftest_projection_repair_v50_integrity.py"
_V49_ENTRYPOINT = b"wepld_s2_doctor_cli_authority_v49_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v49_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V50_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v50 workflow entrypoint count drifted before v49 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V50_ENTRYPOINT, _V49_ENTRYPOINT)


def _import_v49_under_workflow_projection() -> Any:
    """Import frozen v49 while it observes exact v49 workflow bytes.

    v49 (hence v48..v45..v36) reads workflow bytes while its module is imported,
    and the v49->v50 entrypoint migration ships in this same candidate, so v49
    must not observe its own successor's bytes. Only
    ``LocalRepositoryView.read_bytes`` is wrapped for the duration of the import
    and then restored in ``finally`` - the class object itself is never rebound,
    so v20's frozen constructor guard still captures and later sees the exact
    canonical ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v49_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v49_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v50 v49-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v49_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_doctor_cli_authority_v49_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v49_under_workflow_projection()

V25 = q.V25
CW = q.CW
Q_WF = dict(q.WF)
_attr = q._attr
_bind = q._bind
_call = q._call
_EntryHidingView = q._EntryHidingView
_INST = False
_PREDECESSOR_COMPONENT_BASE: Any = None
_PREDECESSOR_FREEZE_S1: Any = None

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_V49_DOCTOR_CLI_SELFTEST_PROJECTION_REPAIR_ONLY"
S2_IMPLEMENTATION_AUTHORITY = q.S2_IMPLEMENTATION_AUTHORITY
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
NEXT_AUTHORITY_GATE = q.NEXT_AUTHORITY_GATE
GENERAL_SHELL_AUTHORITY = q.GENERAL_SHELL_AUTHORITY
ARBITRARY_PROCESS_AUTHORITY = q.ARBITRARY_PROCESS_AUTHORITY
PACKAGE_INSTALL_AUTHORITY = q.PACKAGE_INSTALL_AUTHORITY
PROJECT_NATIVE_COMMAND_EXECUTION = q.PROJECT_NATIVE_COMMAND_EXECUTION
GIT_MUTATION_AUTHORITY = q.GIT_MUTATION_AUTHORITY
SAFE_DIRECTORY_MUTATION_AUTHORITY = q.SAFE_DIRECTORY_MUTATION_AUTHORITY
REMEDIATION_EXECUTION_AUTHORITY = q.REMEDIATION_EXECUTION_AUTHORITY

for _path, _expected in ((q.P, V49_P_BLOB), (q.T, V49_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v50 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v49_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v50 workflow does not reverse to exact canonical v49 predecessor: "
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


_PROJECTION_COUNTER = itertools.count()


class _ProjectionView:
    def __init__(
        self,
        view: Any,
        replacements: dict[str, bytes] | None = None,
        omitted: frozenset[str] = frozenset(),
    ) -> None:
        self._view = view
        self._replacements = replacements or {}
        self._omitted = omitted
        self._instance_id = next(_PROJECTION_COUNTER)

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v50 predecessor projection exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return [entry for entry in self._view.entries() if entry.path not in self._omitted]

    def tree_identity(self, path: str) -> Any:
        return (self._instance_id, path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v49(view: Any) -> None:
    for path, expected in ((q.P, V49_P_BLOB), (q.T, V49_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v50 candidate/base is missing frozen v49 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v49 predecessor drifted: {path}: expected={expected} actual={actual}"
            )


def _project_for_v49(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v49_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v49's view always; project the policy base only
    when it is a real post-v50 base.

    A pre-v50 (bootstrap) policy base predates the v49->v50 workflow entrypoint
    migration and does not carry v50's policy files, so ``_project_for_v49``
    cannot reverse a migration that is not there. It must reach v49's frozen
    hooks unprojected, exactly as v49's own ``_v48_views`` passes a pre-v49
    bootstrap base straight through.
    """
    projected_candidate = _project_for_v49(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v49(policy_base)


def _boot_base_for_selftest() -> Any:
    return _project_for_v49(raw_root)


def _doctor_cli_projection(view: Any) -> tuple[dict[str, bytes], frozenset[str]]:
    """v49's own Doctor/CLI product projection over ``view``: the ``lib.rs``
    export stripped of the two authorized ``pub mod`` lines, and the five new
    module/bin/test paths listed for hiding.

    Fail-closed: ``q._doctor_cli_product_projection`` rejects a partial tranche
    rather than hiding it. When no tranche is tracked it returns an empty
    projection.
    """
    product_replacements, product_omitted = q._doctor_cli_product_projection(
        _ProjectionView(view, {}, POLICY_FILES)
    )
    return dict(product_replacements), frozenset(product_omitted)


def predecessor_view_for(view: Any) -> Any:
    """The exact pre-Doctor/CLI-tranche, exact-v49-workflow view a frozen
    predecessor self-test must observe, derived from ``view`` (true on-disk
    bytes). The v50 self-test uses this to prove the exact regression seam:
    v33's frozen Core-export check rejects a raw post-tranche ``lib.rs`` and
    accepts the projected one.
    """
    replacements, omitted = _doctor_cli_projection(view)
    replacements.update(_workflow_replacements(view))
    return _ProjectionView(view, replacements, omitted)


_LIB_RS = "crates/core/src/lib.rs"


def _corrected_v49_run_predecessor_selftests() -> None:
    """Drop-in replacement for frozen ``v49.run_predecessor_selftests``.

    Frozen v49 wraps ``base.LocalRepositoryView.read_bytes`` for a v49->v48
    workflow entrypoint reversal, then runs frozen v48's whole self-test. It
    does not project its own Doctor/CLI tranche away, so once ``lib.rs`` carries
    the two ``pub mod`` lines the frozen v33 Core-export self-test (and v46's
    own synthetic-fixture regression self-test, which reads the real ``lib.rs``)
    reject it.

    This replacement reproduces v49's behaviour and additionally strips the two
    ``pub mod cli;`` / ``pub mod doctor;`` lines from every ``lib.rs`` read for
    the duration of frozen v48's self-test. Only
    ``base.LocalRepositoryView.read_bytes`` is wrapped - the class object,
    ``entries``, and every ``wepld_*`` module root are untouched, so a freshly
    constructed view still lists the tranche and v21's exact-HEAD inventory
    cross-check and v47's ``_method_patch`` self-assertion both stay valid. The
    five new module/bin/test files are not hidden: no frozen predecessor check
    rejects an unknown ``crates/core`` path, only the Core-export identity.

    Frozen v49's own selftest checks (``_pre_tranche_core_export`` and the
    post-tranche projection checks) run after this returns, outside the wrap, so
    they still observe the real ``lib.rs`` with both lines present.

    When the tranche is not tracked this is byte-for-byte frozen v49 behaviour.
    """
    workflow_reversal = q._workflow_replacements(q.raw_root)
    product_replacements, _product_omitted = _doctor_cli_projection(q.raw_root)
    lib_strip = product_replacements.get(_LIB_RS)

    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _cascade_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v50 v48-cascade workflow projection exceeds read bound: {relative}"
                )
            return data
        if lib_strip is not None and relative == _LIB_RS:
            # Force the real read first so a missing/oversized lib.rs still fails
            # through the canonical path, then serve the Doctor/CLI-stripped bytes.
            original_read_bytes(local_view, relative, limit)
            if len(lib_strip) > limit:
                base.fail("v50 v48-cascade Core-export strip exceeds read bound")
            return lib_strip
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _cascade_read_bytes
    try:
        _call(
            "v48 self-tests under v49->v48 workflow reversal + Doctor/CLI Core-export strip",
            q.q.selftest,
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def run_predecessor_selftests() -> None:
    """Run frozen v49's own self-tests once, under the v49->v50 workflow
    entrypoint reversal, with frozen ``v49.run_predecessor_selftests`` replaced
    for the duration by :func:`_corrected_v49_run_predecessor_selftests` so the
    frozen v48->...->v33 cascade (and v46's synthetic regression self-test) also
    observe v49's Doctor/CLI Core-export strip.

    Only ``base.LocalRepositoryView.read_bytes`` and
    ``q.run_predecessor_selftests`` are wrapped; both are restored in
    ``finally``. No module root and no class attribute is rebound, so v20's
    frozen constructor guard, v21's inventory cross-check, and v47's
    ``_method_patch`` self-assertion all keep passing. Like every vN self-test
    this runs the cascade exactly once and ends with a normal install; the v50
    self-test does not re-enter it.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes
    original_run = q.run_predecessor_selftests

    def _v50_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v50 v49-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v50_selftest_read_bytes
    q.run_predecessor_selftests = _corrected_v49_run_predecessor_selftests
    try:
        _call("v49 self-tests under v50->v49 workflow reversal", q.selftest)
    finally:
        q.run_predecessor_selftests = original_run
        base.LocalRepositoryView.read_bytes = original_read_bytes


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v50 bootstrap delta must be exactly two v50 policy files plus two integrity workflows"
                )
            base.fail("v50 bootstrap authorizes only the self-test repair successor")
        req_v49(candidate)
        req_v49(policy_base)
        return
    if paths & CONTROLLED_FILES:
        base.fail("canonical v50 policy files are frozen after activation")
    q.delta(_project_for_v49(candidate), _project_for_v49(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v49_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v50 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v50 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v50 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v50 steady-state controlled file drifted: {path}")
    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _v49_views(candidate, policy_base)
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
    q.files(_project_for_v49(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v50 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v50 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v50 controlled file content drifted: {path}")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v50 predecessor component-base hook unavailable")
    _call(
        "v50 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v49(view),
        set(paths) - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v50 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v49_views(candidate, policy_base)
    _call(
        "v50 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v50=S2_V49_DOCTOR_CLI_SELFTEST_PROJECTION_REPAIR_ONLY")
    print(f"v50_authority={AUTH}")
    print(f"s2_implementation_authority_v50={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"doctor_cli_authority_v50={DOCTOR_CLI_AUTHORITY}")
    print(f"general_shell_authority_v50={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v50={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v50={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v50={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v50={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v50={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v50={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v50={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v50={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v50={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v50={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v50={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v50={SOURCE_ADMISSION}")
    print(f"dependency_admission_v50={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v50={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v50={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v50 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v50 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v50 workflow identity projection drifted")
    for name in (
        "S2_IMPLEMENTATION_AUTHORITY",
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
        "NEXT_AUTHORITY_GATE",
        "GENERAL_SHELL_AUTHORITY",
        "ARBITRARY_PROCESS_AUTHORITY",
        "PACKAGE_INSTALL_AUTHORITY",
        "PROJECT_NATIVE_COMMAND_EXECUTION",
        "GIT_MUTATION_AUTHORITY",
        "SAFE_DIRECTORY_MUTATION_AUTHORITY",
        "REMEDIATION_EXECUTION_AUTHORITY",
    ):
        if getattr(q, name) != globals()[name]:
            base.fail(f"v50 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v49 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v49 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v49 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v49 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v49 files hook"), q.files),
        (_attr(shell, "print_success", "v49 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v50 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v50 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v50 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v50 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v50 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v50 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v50 allowed hook")
    _bind(shell, "verify_policy_files", files, "v50 files hook")
    _bind(shell, "print_success", printer, "v50 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v50 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v50 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_v49_doctor_cli_selftest_projection_repair_v50_selftest import run

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
