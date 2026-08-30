#!/usr/bin/env python3
"""Repair two frozen-policy defects exposed by canonical dependency admission.

Canonical v31 activated the admitted-dependency self-test projection, and the
S2-AUTH-012 dependency admission then merged, so canonical `main` now carries the
exact admitted manifest, lock, and dependency register. Two inherited policy
defects only become reachable in that state, and both block the authorized
identity/evidence-store tranche rather than expressing any candidate defect.

Defect 1 - asymmetric S1-005 evidence freeze. v30 wraps the inherited S1-005
evidence freeze and projects the admitted dependency state back to its canonical
baseline for the candidate only, leaving the policy base unprojected. While the
base predated dependency admission both sides read as baseline and agreed. Now
that the base itself is the admitted state, the projected candidate and the
unprojected base disagree on `docs/governance/DEPENDENCY_REGISTER.md`, so every
candidate built on canonical `main` fails with a frozen-evidence violation it did
not cause. v32 projects the policy base through the same transformation.

Defect 2 - self-test fixture derivation over the Core export. The frozen v25
self-test derives its synthetic product fixture by appending the identity and
evidence-store module registrations to the live `crates/core/src/lib.rs`, then
asserts that each registration appears exactly once. That holds only while the
live export registers neither module. The authorized identity/evidence-store
tranche legitimately registers both exactly once, which makes the derived fixture
contain two of each and fails the frozen assertion. v32 projects the Core export
back to its exact canonical pre-tranche bytes for the duration of predecessor
self-tests, exactly as v31 already projects the dependency files and workflows.

v32 changes policy verification only. Real candidate delta verification, trusted
admission, product verification, and every runtime authority continue to operate
on the true repository view. No dependency, product, source, filesystem,
process/Git, network, model/provider, Doctor/CLI, or S3+ authority is added.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

import wepld_integrity as base
import wepld_s2_identity_store_governance_v31_integrity as p

V31 = p
V30 = p.p
V29 = p.V29
V26 = p.V26
V25 = p.V25

P = ".github/scripts/wepld_s2_identity_store_governance_v32_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v32_selftest.py"
T_BLOB = "f34f832c892a32c186c78cdcfb3807892784ebf7"
V31_P_BLOB = "b522d929f6f1d6ce7166b79afecb1045a89bfd28"
V31_T_BLOB = "8c8ce95e428f332a29a4060b52cd2edf015d5b96"

FW = V25.FW
AW = V25.AW
CW = V25.CW

CORE_EXPORT = V25.CORE_EXPORT

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_IDENTITY_STORE_FROZEN_POLICY_PROJECTION_REPAIR_ONLY"
S2_IMPLEMENTATION_AUTHORITY = p.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = p.SOURCE_ADMISSION

P_WF = dict(p.WF)
WF = {
    FW: "42e14a4a3a7ee15be5ddff4c008e9ebd25ecf44c79078f32974bf42a5cfa776f",
    AW: "b93e638abbcca1e1f87302e4c9bc4f215c40910c6d19453db39fbf9b13c27841",
    CW: p.WF[CW],
}

P_DELTA = p.delta
P_BASE = p.basectrl
P_EXT = p.ext
P_DEXT = p.dext
P_EEXT = p.eext
P_ALLOWED = p.allowed
P_FILES = p.files
P_PRINTER = p.printer
P_FREEZE = V30.freeze_s1_005_evidence
P_SHELL_COMPONENT_BASE = V30.shell_component_base

_V32_ENTRYPOINT = b"wepld_s2_identity_store_governance_v32_integrity.py"
_V31_ENTRYPOINT = b"wepld_s2_identity_store_governance_v31_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Exact canonical pre-tranche bytes of the Core export. The frozen v25 self-test
# derives its product fixture from this file, so predecessor self-tests must
# observe exactly these bytes even after the tranche registers its modules.
BASE_CORE_EXPORT = b"""#![forbid(unsafe_code)]

pub mod project;
pub mod state;

pub use project::{
    DataRootInputs, DataRootObservation, DataRootSource, MAX_PATH_COMPONENT_OBSERVATIONS,
    NonGitProjectRoot, PathEntryKind, PathMetadataObservation, PathMetadataTrail,
    ProjectObservationError, ProjectRootBasis, classify_path_io_error, lexical_absolute_path,
    machine_path_from_path, observe_non_git_project_root, observe_path_metadata,
    observe_project_locator, platform_data_root,
};
pub use state::{
    CoreProfile, HandshakeState, MAX_HEALTH_WATCHES, MAX_IN_FLIGHT_REQUESTS, MAX_TERMINAL_RESULTS,
    PendingRequest, StateError,
};
"""

CORE_EXPORT_BASE_BLOB = "ca9909da8f8d04a8c618b4ee96fc9e89fbe9e8b0"

# Exact bytes of the single authorized post-tranche Core export. Acceptance is
# bound to these bytes rather than to registration occurrence counts, so an
# export that registers both modules but also carries an unrelated edit is
# rejected instead of being projected away.
ADMITTED_CORE_EXPORT = b"""#![forbid(unsafe_code)]

pub mod evidence_store;
pub mod identity;
pub mod project;
pub mod state;

pub use evidence_store::{
    EvidenceStore, Freshness, LOCK_ACQUIRE_DEADLINE_MS, LOCK_POLL_INTERVAL_MS, MAX_CURRENT_BYTES,
    MAX_MANIFEST_BYTES, MAX_RECORD_BYTES, PRODUCER_CONTRACT_VERSION, PublishedGeneration,
    StoreDefect, StoreError, StoreLock, build_manifest, busy_error_code, content_digest,
    now_unix_millis, redacted_summary, safe_path_segment,
};
pub use identity::{
    IdentityCandidate, IdentityError, OPAQUE_ID_RANDOM_BYTES, ProjectMatchFacts,
    RESERVATION_KEY_VERSION, ReservationRecovery, allocate_generation_id, allocate_project_id,
    allocate_record_id, allocate_worktree_id, build_identity_record, build_reservation, busy,
    compare_match_strength, complete_reservation, match_strength_rank, recover_reservation,
    resolve_identity,
};
pub use project::{
    DataRootInputs, DataRootObservation, DataRootSource, MAX_PATH_COMPONENT_OBSERVATIONS,
    NonGitProjectRoot, PathEntryKind, PathMetadataObservation, PathMetadataTrail,
    ProjectObservationError, ProjectRootBasis, classify_path_io_error, lexical_absolute_path,
    machine_path_from_path, observe_non_git_project_root, observe_path_metadata,
    observe_project_locator, platform_data_root,
};
pub use state::{
    CoreProfile, HandshakeState, MAX_HEALTH_WATCHES, MAX_IN_FLIGHT_REQUESTS, MAX_TERMINAL_RESULTS,
    PendingRequest, StateError,
};
"""

CORE_EXPORT_ADMITTED_BLOB = "3180ae22cb29dbcc807418580c0062bab18c0a2e"

IDENTITY_REGISTRATION = b"pub mod identity;"
STORE_REGISTRATION = b"pub mod evidence_store;"

root = p.root
for _path, _expected in ((p.P, V31_P_BLOB), (p.T, V31_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v32 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

if V25.blob(BASE_CORE_EXPORT) != CORE_EXPORT_BASE_BLOB:
    base.fail("v32 frozen canonical Core export baseline drifted")

if V25.blob(ADMITTED_CORE_EXPORT) != CORE_EXPORT_ADMITTED_BLOB:
    base.fail("v32 frozen authorized Core export drifted")

_call = p._call
_attr = p._attr
_bind = p._bind
_INST = False
_PRINT: Any = None


class _ProjectionView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v32 projected file exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v31(view: Any) -> None:
    for path, expected in ((p.P, V31_P_BLOB), (p.T, V31_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v32 candidate/base is missing frozen v31 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v31 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _core_export_baseline(view: Any) -> bytes | None:
    """Reverse the authorized Core export registration to its canonical bytes.

    Returns `None` when the view already carries the canonical baseline, so the
    pre-tranche base is never rewritten. Otherwise the export must equal the
    exact authorized tranche bytes. Registration occurrence counts are not a
    sufficient acceptance condition: an export that registers both modules and
    also carries an unrelated edit would satisfy a count-based predicate and be
    projected away, hiding a real export change during predecessor self-tests.
    Binding to exact bytes keeps this projection fail-closed.
    """
    if CORE_EXPORT not in V25.ps(view):
        return None
    data = view.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if data == BASE_CORE_EXPORT:
        return None
    if data != ADMITTED_CORE_EXPORT:
        base.fail(
            "v32 Core export is neither the exact canonical baseline nor the "
            "exact authorized tranche export"
        )
    return BASE_CORE_EXPORT


def _project_core_export(view: Any) -> Any:
    baseline = _core_export_baseline(view)
    if baseline is None:
        return view
    return _ProjectionView(view, {CORE_EXPORT: baseline})


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V32_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v32 workflow entrypoint count drifted before predecessor "
                f"projection: {path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} "
                f"actual={count}"
            )
        predecessor = data.replace(_V32_ENTRYPOINT, _V31_ENTRYPOINT)
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v32 workflow does not reverse to exact canonical v31 "
                f"predecessor: {path} expected={P_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return replacements


def _workflow_predecessor_projection(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view))


def _predecessor_view(view: Any) -> Any:
    return _workflow_predecessor_projection(_project_core_export(view))


def _run_under_predecessor_projection(
    view: Any, label: str, fn: Callable[[], Any]
) -> Any:
    """Run a predecessor entry point with the Core export projected to baseline.

    v31 installs its own dependency and workflow projection inside this call.
    That inner projection captures the patched reader below as its fall-through,
    so the two projections compose: v31 resolves the dependency files and
    workflows, and this layer resolves the Core export.
    """
    replacements = _workflow_replacements(view)
    baseline = _core_export_baseline(view)
    if baseline is not None:
        replacements[CORE_EXPORT] = baseline
    target = _ProjectionView(view, replacements)

    patched_roots: list[tuple[Any, Any]] = []
    for name, module in list(sys.modules.items()):
        if not name.startswith("wepld_") or module is None or not hasattr(module, "root"):
            continue
        patched_roots.append((module, getattr(module, "root")))
        setattr(module, "root", target)

    original_local_read = base.LocalRepositoryView.read_bytes

    def projected_local_read(local_view: Any, path: str, limit: int) -> bytes:
        if path in replacements:
            data = replacements[path]
            if len(data) > limit:
                base.fail(f"v32 predecessor projection exceeds read bound: {path}")
            return data
        return original_local_read(local_view, path, limit)

    base.LocalRepositoryView.read_bytes = projected_local_read
    try:
        return _call(label, fn)
    finally:
        base.LocalRepositoryView.read_bytes = original_local_read
        for module, original in reversed(patched_roots):
            setattr(module, "root", original)


def freeze_s1_005_evidence(candidate: Any, policy_base: Any) -> None:
    """Freeze S1-005 evidence symmetrically across candidate and policy base.

    v30 projects the admitted dependency state back to its canonical baseline for
    the candidate only. Now that canonical `main` is itself the admitted state,
    the unprojected base no longer agrees with the projected candidate. Projecting
    both sides restores the intended comparison: an unchanged register compares
    equal, and a genuine change to frozen evidence still fails.
    """
    projected_base = policy_base
    if V26.deps_ready(policy_base):
        projected_base = V30.project_admitted_dependency_state(policy_base)
    _call("v30 S1-005 evidence freeze", P_FREEZE, candidate, projected_base)


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths == BOOT:
            req_v31(candidate)
            req_v31(policy_base)
            if not V26.deps_ready(candidate) or not V26.deps_ready(policy_base):
                base.fail(
                    "v32 bootstrap requires the exact canonical admitted "
                    "dependency state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v32 bootstrap delta must be exactly two v32 policy files "
                "plus two integrity workflows"
            )
        base.fail(
            "v32 bootstrap base authorizes only exact frozen-policy projection repair"
        )

    if paths & ALL_POLICY_FILES:
        base.fail(
            "canonical v32/v31/v30/v29/v28/v27/v26/v25 policy files are frozen "
            "after activation"
        )

    P_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        P_BASE(
            _workflow_predecessor_projection(candidate),
            _workflow_predecessor_projection(policy_base),
        )
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != P_WF[path]:
                base.fail(f"v32 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v32 policy file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v32 policy file unexpectedly in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v32 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        P_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES
    if remaining:
        P_ALLOWED(remaining, stage)


def files(view: Any) -> None:
    P_FILES(_workflow_predecessor_projection(view))
    missing = POLICY_FILES - V25.ps(view)
    if missing:
        base.fail(f"v32 policy files missing: {sorted(missing)}")
    approved = {
        P: root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(POLICY_FILES):
        if V25.mode(view, path) != "100644":
            base.fail(f"v32 policy file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v32 policy file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not P_PRINTER:
        base.fail("v32 predecessor printer drifted")
    _call("v31 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v32=FROZEN_POLICY_PROJECTION_REPAIR_ONLY")
    print(f"v32_authority={AUTH}")
    print(f"s2_implementation_authority_v32={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v32={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v32={SOURCE_ADMISSION}")
    print("v32_s1_005_freeze_projection=CANDIDATE_AND_POLICY_BASE")
    print("v32_predecessor_selftest_projection=EXACT_CANONICAL_CORE_EXPORT")


def run_predecessor_selftests(view: Any) -> None:
    _run_under_predecessor_projection(view, "v31 predecessor self-tests", p.selftest)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(shell, "_verify_shell_component_base", "shell component-base hook"),
            P_SHELL_COMPONENT_BASE,
        ),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            freeze_s1_005_evidence,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v32 installed overlay drifted")
    if any(
        dict(module.WF) != dict(WF)
        for module in (p, V30, V29, V26, V25)
    ):
        base.fail("v32 workflow identity projection drifted")


def prepare_p() -> None:
    current = dict(p.WF)
    if current not in (P_WF, dict(WF)):
        base.fail(f"v32 predecessor workflow identity map drifted: actual={current}")
    for module in (p, V30, V29, V26, V25):
        module.WF = dict(WF)


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    _run_under_predecessor_projection(root, "v31 predecessor install", p.install)
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v31 routing hook"), P_DELTA),
        (base.compare_base_controlled, P_BASE),
        (
            _attr(execution, "freeze_s1_005_evidence", "v31 S1-005 evidence-freeze hook"),
            P_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v31 desktop hook"), P_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v31 execution hook"), P_EEXT),
        (_attr(shell, "validate_allowed_paths", "v31 allowed hook"), P_ALLOWED),
        (_attr(shell, "verify_policy_files", "v31 files hook"), P_FILES),
        (_attr(shell, "print_success", "v31 printer"), P_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v32 predecessor hook drifted")

    _PRINT = P_PRINTER
    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(POLICY_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(POLICY_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v32 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v32 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v32 routing hook")
    base.compare_base_controlled = basectrl
    _bind(
        execution,
        "freeze_s1_005_evidence",
        freeze_s1_005_evidence,
        "v32 S1-005 evidence-freeze hook",
    )
    _bind(desktop, "verify_extension_controlled_paths", dext, "v32 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v32 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v32 allowed hook")
    _bind(shell, "verify_policy_files", files, "v32 files hook")
    _bind(shell, "print_success", printer, "v32 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v32_selftest import run

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
