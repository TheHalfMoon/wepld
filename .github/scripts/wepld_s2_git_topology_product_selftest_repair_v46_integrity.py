#!/usr/bin/env python3
"""Repair v45 predecessor self-tests for the authorized post-tranche state only.

Foundation run #1017 against the first real v45-authorized Git-topology product
candidate proved that v45's own predecessor-selftest call bypasses the product
projection that every runtime/admission path already uses. Once `lib.rs` contains
`pub mod git_topology;`, v33 therefore observes an export identity it never
admitted and fails before Rust qualification begins.

v46 changes no product rule and grants no new authority. It supersedes only that
self-test seam: while v45 runs its frozen predecessor self-test cascade, the
already-authorized Git-topology module/test and one-line Core export are projected
back to the exact predecessor view, along with the ordinary workflow projection.
All temporary roots/classes/functions are restored in `finally` blocks.

The v45 product authority, closed Git argv, process/environment bounds, no-network
rule, Doctor/CLI denial, and S3+ denial are inherited byte-for-byte as authority
values. The product tranche remains the exact three paths v45 already granted.
"""

from __future__ import annotations

import argparse
import importlib
import itertools
from pathlib import Path
import sys
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_git_topology_product_selftest_repair_v46_integrity.py"
T = ".github/scripts/wepld_s2_git_topology_product_selftest_repair_v46_selftest.py"
T_BLOB = "6ee7cd6f9ef8862d38a0ced5d2a163053284b72c"

V45_P_BLOB = "a9b77d8d981871730a7de4c1f5f2f0661176f9a7"
V45_T_BLOB = "70673c5f1324c8a06e7f36c0f8412aa3d9f57880"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V46_ENTRYPOINT = b"wepld_s2_git_topology_product_selftest_repair_v46_integrity.py"
_V45_ENTRYPOINT = b"wepld_s2_git_topology_authority_v45_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v45_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V46_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v46 workflow entrypoint count drifted before v45 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V46_ENTRYPOINT, _V45_ENTRYPOINT)


def _import_v45_under_workflow_projection() -> Any:
    """Import frozen v45 while it observes exact v45 workflow bytes.

    v45 reads workflow bytes while its module is imported, and the v45->v46
    entrypoint migration ships in this same candidate, so v45 must not observe
    its own successor's bytes. Only ``LocalRepositoryView.read_bytes`` is wrapped
    for the duration of the import and then restored in ``finally`` - the class
    object itself is never rebound, so v20's frozen constructor/class-identity
    guard still captures and later sees the exact canonical
    ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v45_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v45_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v46 v45-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v45_import_read_bytes
    try:
        return importlib.import_module("wepld_s2_git_topology_authority_v45_integrity")
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v45_under_workflow_projection()

V25 = q.V25
CW = q.CW
Q_WF = dict(q.WF)
_attr = q._attr
_bind = q._bind
_call = q._call
_INST = False
_PREDECESSOR_COMPONENT_BASE: Any = None
_PREDECESSOR_FREEZE_S1: Any = None

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_V45_PRODUCT_SELFTEST_PROJECTION_REPAIR_ONLY"
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

for _path, _expected in ((q.P, V45_P_BLOB), (q.T, V45_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v46 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v45_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v46 workflow does not reverse to exact canonical v45 predecessor: "
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
                base.fail(f"v46 predecessor projection exceeds read bound: {path}")
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


def req_v45(view: Any) -> None:
    for path, expected in ((q.P, V45_P_BLOB), (q.T, V45_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v46 candidate/base is missing frozen v45 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v45 predecessor drifted: {path}: expected={expected} actual={actual}"
            )


def _project_for_v45(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _boot_base_for_selftest() -> Any:
    return _project_for_v45(raw_root)


def _v45_predecessor_projection(
    view: Any, workflow_reversal: dict[str, bytes] | None = None
) -> tuple[dict[str, bytes], frozenset[str]]:
    """v46->v45 workflow reversal plus v45's own Git-topology product projection.

    ``view`` MUST expose the true on-disk (migrated) bytes; ``_workflow_replacements``
    re-verifies the exact v46 entrypoint counts and would reject an already
    reversed view. Pass ``workflow_reversal`` to reuse an already-derived,
    already-verified map instead of deriving it again.

    Fail-closed: ``q._product_projection`` rejects a partial tranche product set
    (including the incoherent authorized-export-with-no-product state) rather
    than hiding it, so a malformed post-tranche candidate stops here instead of
    reaching the predecessor cascade.
    """
    if workflow_reversal is None:
        workflow_reversal = _workflow_replacements(view)
    v45_view = _ProjectionView(view, workflow_reversal, POLICY_FILES)
    product_replacements, product_omitted = q._product_projection(v45_view)
    replacements = dict(workflow_reversal)
    replacements.update(product_replacements)
    # Only the Git-topology product paths are hidden. v46's own policy files are
    # left visible: they exist identically in the working tree and at HEAD, and
    # hiding them from the class-wide entries wrap would desync a fresh
    # LocalRepositoryView inventory from the exact-HEAD commit view that some
    # predecessor self-tests cross-check.
    omitted = frozenset(product_omitted)
    return replacements, omitted


def _method_patch(
    replacements: dict[str, bytes],
    omitted: frozenset[str],
    label: str,
    run: Any,
) -> None:
    """Run ``run`` with only ``base.LocalRepositoryView.read_bytes`` /
    ``entries`` temporarily wrapped to serve ``replacements`` and hide
    ``omitted`` from every view - fresh or projected.

    This is the sanctioned method-level wrap already used by v31..v35: the
    ``base.LocalRepositoryView`` class object is never replaced or subclassed,
    so v20's frozen constructor/class-identity guard keeps passing. Module
    roots are left untouched - v45's import already gave each predecessor its
    exact per-version workflow projection over the true root. Nesting composes:
    the fallthrough and the ``finally`` both route through whatever wrap an
    outer call already installed.
    """
    outer_read_bytes = base.LocalRepositoryView.read_bytes
    outer_entries = base.LocalRepositoryView.entries

    def _read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in omitted:
            base.fail(
                "v46 predecessor projection forbids reading an omitted path from "
                f"a fresh local view: {relative}"
            )
        if relative in replacements:
            data = replacements[relative]
            if len(data) > limit:
                base.fail(
                    f"v46 predecessor projection exceeds read bound: {relative}"
                )
            return data
        return outer_read_bytes(local_view, relative, limit)

    def _entries(local_view: Any) -> Any:
        return [
            entry
            for entry in outer_entries(local_view)
            if entry.path not in omitted
        ]

    base.LocalRepositoryView.read_bytes = _read_bytes
    base.LocalRepositoryView.entries = _entries
    try:
        _call(label, run)
    finally:
        base.LocalRepositoryView.entries = outer_entries
        base.LocalRepositoryView.read_bytes = outer_read_bytes


def predecessor_view_for(view: Any) -> Any:
    """The exact pre-Git-topology-tranche, exact-v45-workflow view a frozen
    predecessor self-test must observe, derived from ``view`` (true on-disk
    bytes). The v46 self-test uses this to prove the exact Foundation #1017
    seam: v33's frozen Core-export check rejects a raw post-tranche ``lib.rs``
    and accepts the projected one.
    """
    replacements, omitted = _v45_predecessor_projection(view)
    return _ProjectionView(view, replacements, omitted)


def run_predecessor_selftests() -> None:
    """Run frozen v45's own self-tests once, with (a) the v45->v46 entrypoint
    migration reversed for every workflow read, since that migration ships in
    this same candidate, and (b) only v45's defective predecessor-cascade seam
    replaced so the frozen v44 cascade also observes v45's Git-topology product
    projection.

    Both projection sets are derived once, from the true unpatched ``raw_root``,
    before anything is wrapped. Only ``LocalRepositoryView`` methods are wrapped
    and every wrap is restored in ``finally``. Like every vN self-test this runs
    the cascade exactly once and ends with a normal install; the v46 self-test
    does not re-enter it.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    cascade_replacements, cascade_omitted = _v45_predecessor_projection(
        raw_root, workflow_reversal
    )

    def _corrected_v45_run_predecessor_selftests() -> None:
        """Replacement for frozen ``v45.run_predecessor_selftests``: layer v45's
        Git-topology product projection on top of the active workflow reversal
        for the frozen v44 cascade only."""
        _method_patch(
            cascade_replacements,
            cascade_omitted,
            "v45 predecessor self-test cascade",
            q.p.selftest,
        )

    original_run = q.run_predecessor_selftests
    q.run_predecessor_selftests = _corrected_v45_run_predecessor_selftests
    try:
        _method_patch(
            workflow_reversal,
            frozenset(),
            "v45 self-tests under v46->v45 workflow reversal",
            q.selftest,
        )
    finally:
        q.run_predecessor_selftests = original_run


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v46 bootstrap delta must be exactly two v46 policy files plus two integrity workflows"
                )
            base.fail("v46 bootstrap authorizes only the self-test repair successor")
        req_v45(candidate)
        req_v45(policy_base)
        return
    if paths & CONTROLLED_FILES:
        base.fail("canonical v46 policy files are frozen after activation")
    q.delta(_project_for_v45(candidate), _project_for_v45(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(_project_for_v45(candidate), _project_for_v45(policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v46 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v46 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v46 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v46 steady-state controlled file drifted: {path}")
    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        q.ext(_project_for_v45(candidate), _project_for_v45(policy_base), rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        q.allowed(remaining, stage)


def files(view: Any) -> None:
    q.files(_project_for_v45(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v46 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v46 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v46 controlled file content drifted: {path}")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v46 predecessor component-base hook unavailable")
    _call(
        "v46 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v45(view),
        set(paths) - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v46 predecessor S1 freeze hook unavailable")
    _call(
        "v46 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        _project_for_v45(candidate),
        _project_for_v45(policy_base),
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v46=S2_V45_PRODUCT_SELFTEST_PROJECTION_REPAIR_ONLY")
    print(f"v46_authority={AUTH}")
    print(f"s2_implementation_authority_v46={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_process_admission_v46={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v46={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v46={NETWORK_AUTHORITY}")
    print(f"doctor_cli_authority_v46={DOCTOR_CLI_AUTHORITY}")
    print(f"s3_plus_authority_v46={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v46={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v46 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v46 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v46 workflow identity projection drifted")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v45 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v45 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v45 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v45 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v45 files hook"), q.files),
        (_attr(shell, "print_success", "v45 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v46 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v46 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v46 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v46 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v46 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v46 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v46 allowed hook")
    _bind(shell, "verify_policy_files", files, "v46 files hook")
    _bind(shell, "print_success", printer, "v46 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v46 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v46 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_git_topology_product_selftest_repair_v46_selftest import run

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
