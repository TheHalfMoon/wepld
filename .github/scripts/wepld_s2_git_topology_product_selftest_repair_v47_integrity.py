#!/usr/bin/env python3
"""Repair v46's predecessor self-test seam for the tracked post-tranche state.

The first real product candidate against canonical v46 (product PR
`feat/s2-git-topology-v1`, once reconciled onto the v46 main) proved that v46's
``_method_patch`` hides the Git-topology product paths by reassigning
``base.LocalRepositoryView.entries`` for the whole predecessor cascade. A
v21-era self-test cross-checks a fresh ``LocalRepositoryView`` entry inventory
against the exact-HEAD commit view, and once the two product files are actually
tracked the class-wide ``entries`` wrap desyncs that check
(``local commit view entry inventory differs from exact HEAD``).

v47 changes no product rule and grants no new authority. It replaces frozen
v46's defective ``_method_patch`` with one that never touches
``base.LocalRepositoryView.entries``: the Git-topology product paths are hidden
by *wrapping* each ``wepld_*`` module ``root`` / ``raw_root`` in an
entries-only projection (``_EntryHidingView``), mirroring v33's proven
``_ProjectionView`` semantics, so the class-level exact-HEAD inventory
invariant, the per-version workflow projection, and the real subtree object
identities all stay intact. Every wrap is restored in ``finally``.

Every v46 / v45 authority value is inherited by reference and asserted
unchanged: closed Git argv, process/environment bounds, no-network rule,
Doctor/CLI denial, S3+ denial, ``NEXT_AUTHORITY_GATE=S2-AUTH-015``. The product
tranche remains the exact three paths v45 already granted.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_git_topology_product_selftest_repair_v47_integrity.py"
T = ".github/scripts/wepld_s2_git_topology_product_selftest_repair_v47_selftest.py"
T_BLOB = "d4a11006395936c8e648a4a6e5e4ef1f563dcc37"

V46_P_BLOB = "6362667fb13e9e783f859eb5f133dab2e829b0c9"
V46_T_BLOB = "6ee7cd6f9ef8862d38a0ced5d2a163053284b72c"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V47_ENTRYPOINT = b"wepld_s2_git_topology_product_selftest_repair_v47_integrity.py"
_V46_ENTRYPOINT = b"wepld_s2_git_topology_product_selftest_repair_v46_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v46_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V47_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v47 workflow entrypoint count drifted before v46 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V47_ENTRYPOINT, _V46_ENTRYPOINT)


def _import_v46_under_workflow_projection() -> Any:
    """Import frozen v46 while it observes exact v46 workflow bytes.

    v46 reads workflow bytes while its module is imported, and the v46->v47
    entrypoint migration ships in this same candidate, so v46 must not observe
    its own successor's bytes. Only ``LocalRepositoryView.read_bytes`` is
    wrapped for the duration of the import and then restored in ``finally`` -
    the class object itself is never rebound, so v20's frozen constructor guard
    still captures and later sees the exact canonical ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v46_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v46_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v47 v46-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v46_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_git_topology_product_selftest_repair_v46_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v46_under_workflow_projection()

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

AUTH = "S2_V46_PRODUCT_STATE_PREDECESSOR_INVENTORY_REPAIR_ONLY"
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

for _path, _expected in ((q.P, V46_P_BLOB), (q.T, V46_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v47 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v46_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v47 workflow does not reverse to exact canonical v46 predecessor: "
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


class _EntryHidingView:
    """Wrap a view to hide ``omitted`` paths from its entry inventory only.

    Mirrors v33's proven ``_ProjectionView`` semantics for the pre-tranche
    case: ``omitted`` applies to this wrapper's ``entries()`` and nothing else.
    ``read_bytes``, ``read_text``, ``tree_identity`` and every other attribute
    pass straight through to the wrapped view, so the per-version workflow
    projection, the real subtree object identities, and the class-level
    exact-HEAD entry inventory invariant all stay intact.
    """

    def __init__(self, view: Any, omitted: frozenset[str]) -> None:
        self._view = view
        self._omitted = omitted

    def entries(self) -> Any:
        return [entry for entry in self._view.entries() if entry.path not in self._omitted]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _corrected_method_patch(
    replacements: dict[str, bytes],
    omitted: frozenset[str],
    label: str,
    run: Any,
) -> None:
    """Replacement for frozen ``v46._method_patch``.

    ``base.LocalRepositoryView.read_bytes`` is method-wrapped to serve
    ``replacements`` (workflow reversal plus the one-line Core-export strip);
    the class object and ``entries`` attribute are left untouched. The
    Git-topology product paths in ``omitted`` are hidden by wrapping every
    ``wepld_*`` module ``root`` / ``raw_root`` in an additive
    ``_EntryHidingView`` that preserves whatever per-version workflow
    projection v45's import already installed there. Every wrap is restored in
    ``finally``; nesting composes through the previously installed wrap.
    """
    outer_read_bytes = base.LocalRepositoryView.read_bytes

    def _read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in replacements:
            data = replacements[relative]
            if len(data) > limit:
                base.fail(
                    f"v47 predecessor projection exceeds read bound: {relative}"
                )
            return data
        return outer_read_bytes(local_view, relative, limit)

    patched_roots: list[tuple[Any, str, Any]] = []
    if omitted:
        for name, module in list(sys.modules.items()):
            if not name.startswith("wepld_") or module is None:
                continue
            for attr in ("root", "raw_root"):
                current = getattr(module, attr, None)
                if current is None:
                    continue
                patched_roots.append((module, attr, current))
                setattr(module, attr, _EntryHidingView(current, omitted))

    base.LocalRepositoryView.read_bytes = _read_bytes
    try:
        _call(label, run)
    finally:
        base.LocalRepositoryView.read_bytes = outer_read_bytes
        for module, attr, original in reversed(patched_roots):
            setattr(module, attr, original)


_ORIGINAL_V46_METHOD_PATCH = q._method_patch
q._method_patch = _corrected_method_patch


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v46(view: Any) -> None:
    for path, expected in ((q.P, V46_P_BLOB), (q.T, V46_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v47 candidate/base is missing frozen v46 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v46 predecessor drifted: {path}: expected={expected} actual={actual}"
            )


def _project_for_v46(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v46_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v46's view always; project the policy base only
    when it is a real post-v47 base. A pre-v47 bootstrap base predates the
    v46->v47 workflow migration and carries no v47 policy files, so it must
    reach v46's frozen hooks unprojected."""
    projected_candidate = _project_for_v46(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v46(policy_base)


def _boot_base_for_selftest() -> Any:
    return _project_for_v46(raw_root)


def run_predecessor_selftests() -> None:
    """Run frozen v46's own self-tests once, under a v47->v46 workflow reversal.

    v46's ``_method_patch`` has been replaced above by
    :func:`_corrected_method_patch`, so v46's predecessor cascade now hides the
    Git-topology product paths without class-patching
    ``base.LocalRepositoryView.entries``. Only ``read_bytes`` is wrapped here;
    the wrap is restored in ``finally``.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v46_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    "v47 v46-selftest workflow projection exceeds read bound: "
                    f"{relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v46_selftest_read_bytes
    try:
        _call("v46 self-tests under v47->v46 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v47 bootstrap delta must be exactly two v47 policy files plus two integrity workflows"
                )
            base.fail("v47 bootstrap authorizes only the predecessor-inventory repair successor")
        req_v46(candidate)
        req_v46(policy_base)
        return
    if paths & CONTROLLED_FILES:
        base.fail("canonical v47 policy files are frozen after activation")
    q.delta(_project_for_v46(candidate), _project_for_v46(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(_project_for_v46(candidate), _project_for_v46(policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v47 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v47 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v47 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v47 steady-state controlled file drifted: {path}")
    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _v46_views(candidate, policy_base)
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
    q.files(_project_for_v46(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v47 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v47 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v47 controlled file content drifted: {path}")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v47 predecessor component-base hook unavailable")
    _call(
        "v47 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v46(view),
        set(paths) - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v47 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v46_views(candidate, policy_base)
    _call(
        "v47 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v47=S2_V46_PRODUCT_STATE_PREDECESSOR_INVENTORY_REPAIR_ONLY")
    print(f"v47_authority={AUTH}")
    print(f"s2_implementation_authority_v47={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_process_admission_v47={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v47={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v47={NETWORK_AUTHORITY}")
    print(f"doctor_cli_authority_v47={DOCTOR_CLI_AUTHORITY}")
    print(f"s3_plus_authority_v47={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v47={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v47 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v47 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v47 workflow identity projection drifted")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v46 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v46 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v46 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v46 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v46 files hook"), q.files),
        (_attr(shell, "print_success", "v46 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v47 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v47 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v47 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v47 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v47 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v47 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v47 allowed hook")
    _bind(shell, "verify_policy_files", files, "v47 files hook")
    _bind(shell, "print_success", printer, "v47 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v47 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v47 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_git_topology_product_selftest_repair_v47_selftest import run

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
