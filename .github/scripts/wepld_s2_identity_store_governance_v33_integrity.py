#!/usr/bin/env python3
"""Complete the predecessor pre-tranche view so self-tests stay self-consistent.

v32 correctly identified that the frozen v25 self-test derives its synthetic
product fixture from the live Core export, and projected that export back to its
canonical pre-tranche bytes for the duration of predecessor self-tests. That
projection was necessary but incomplete, and the resulting view is incoherent.

Inside the same predecessor self-test pass, the frozen chain performs two reads
that disagree under a partial projection:

* the v25 self-test derives `lib = core_lib + registrations`, which is only
  correct when `core_lib` carries no registration; and
* `_verify_product_files` requires the export to register both modules exactly
  once whenever `PRODUCT_NEW_FILES` are present in the view's path set.

Projecting only the export bytes satisfies the first read and breaks the second:
the export reads as the canonical baseline with zero registrations while the path
set still lists the tranche modules, so the frozen verifier demands registrations
the projected export no longer has and fails with

    v25 Core export must register identity and evidence_store exactly once

The two requirements are contradictory for any projection that changes the export
without also changing the path set, because an export carrying one registration
of each module necessarily carries two once the fixture appends its own.

v33 therefore presents a complete pre-tranche view rather than a partial one:
during predecessor self-tests the projected view reports the canonical baseline
export **and** omits exactly the three authorized tranche product paths from its
entry inventory. Both frozen reads then agree, because they observe the same
self-consistent canonical pre-tranche tree.

The entry filter is applied only to the projection wrapper. `LocalRepositoryView`
itself is never filtered, so the inherited invariant that a local commit view's
entry inventory matches the exact HEAD tree continues to hold and continues to
reject genuine view tampering.

v33 changes policy verification only. Real candidate delta verification, trusted
admission, product verification, and every runtime authority continue to operate
on the true repository view. No dependency, product, source, filesystem,
process/Git, network, model/provider, Doctor/CLI, or S3+ authority is added.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

import wepld_integrity as base
import wepld_s2_identity_store_governance_v32_integrity as p

V32 = p
V31 = p.V31
V30 = p.V30
V29 = p.V29
V28 = V29.s
V27 = V28.r
V26 = p.V26
V25 = p.V25

# The complete frozen predecessor chain, ordered newest first. The workflow
# identity projection must cover every level: a partial projection leaves an
# inherited level comparing against a stale map.
PREDECESSOR_CHAIN = (p, V31, V30, V29, V28, V27, V26, V25)

P = ".github/scripts/wepld_s2_identity_store_governance_v33_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v33_selftest.py"
T_BLOB = "8b969d85b61164f8874b9d05c8743b057f8e16c1"
V32_P_BLOB = "dc8ef1f96a9134d3355958ff663a8c42c68ee19c"
V32_T_BLOB = "f34f832c892a32c186c78cdcfb3807892784ebf7"

FW = V25.FW
AW = V25.AW
CW = V25.CW

CORE_EXPORT = V25.CORE_EXPORT
BASE_CORE_EXPORT = p.BASE_CORE_EXPORT
ADMITTED_CORE_EXPORT = p.ADMITTED_CORE_EXPORT
CORE_EXPORT_BASE_BLOB = p.CORE_EXPORT_BASE_BLOB
CORE_EXPORT_ADMITTED_BLOB = p.CORE_EXPORT_ADMITTED_BLOB

# The exact authorized tranche product paths. Only these three may be omitted
# from a projected pre-tranche entry inventory, and only while the Core export is
# exactly the authorized post-tranche form.
TRANCHE_PRODUCT_PATHS = frozenset(
    {V25.IDENTITY_MODULE, V25.STORE_MODULE, V25.PRODUCT_TEST}
)

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_IDENTITY_STORE_PRETRANCHE_VIEW_REPAIR_ONLY"
S2_IMPLEMENTATION_AUTHORITY = p.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = p.SOURCE_ADMISSION

P_WF = dict(p.WF)
WF = {
    FW: "4c484672553b970a4a004db2bdc3d07d92adc30fc0648f8e6aa60aeffc6a69ce",
    AW: "4471e75b811036629c288c175cb6c8f627640047bba2f6bbb112fe5c87bd215e",
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
P_FREEZE = p.freeze_s1_005_evidence

_V33_ENTRYPOINT = b"wepld_s2_identity_store_governance_v33_integrity.py"
_V32_ENTRYPOINT = b"wepld_s2_identity_store_governance_v32_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

root = p.root
for _path, _expected in ((p.P, V32_P_BLOB), (p.T, V32_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v33 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = p._call
_attr = p._attr
_bind = p._bind
_INST = False
_PRINT: Any = None


class _ProjectionView:
    """A projected view that may also omit exact pre-tranche entries.

    `omitted` is applied to this wrapper's entry inventory only. The underlying
    `LocalRepositoryView` is never filtered, so the inherited exact-HEAD entry
    inventory invariant is unaffected.
    """

    def __init__(
        self,
        view: Any,
        replacements: dict[str, bytes],
        omitted: frozenset[str] = frozenset(),
    ) -> None:
        self._view = view
        self._replacements = replacements
        self._omitted = omitted

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v33 projected file exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def entries(self) -> Any:
        source = self._view.entries()
        if not self._omitted:
            return source
        return [entry for entry in source if entry.path not in self._omitted]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v32(view: Any) -> None:
    for path, expected in ((p.P, V32_P_BLOB), (p.T, V32_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v33 candidate/base is missing frozen v32 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v32 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _core_export_baseline(view: Any) -> bytes | None:
    """Reverse the authorized Core export to its canonical bytes.

    Returns `None` when the view already carries the canonical baseline, so a
    pre-tranche view is never rewritten. Otherwise the export must equal the
    exact authorized tranche bytes; every other export fails closed.
    """
    if CORE_EXPORT not in V25.ps(view):
        return None
    data = view.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if data == BASE_CORE_EXPORT:
        return None
    if data != ADMITTED_CORE_EXPORT:
        base.fail(
            "v33 Core export is neither the exact canonical baseline nor the "
            "exact authorized tranche export"
        )
    return BASE_CORE_EXPORT


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V33_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v33 workflow entrypoint count drifted before predecessor "
                f"projection: {path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} "
                f"actual={count}"
            )
        predecessor = data.replace(_V33_ENTRYPOINT, _V32_ENTRYPOINT)
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v33 workflow does not reverse to exact canonical v32 "
                f"predecessor: {path} expected={P_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return replacements


def _workflow_predecessor_projection(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view))


def pretranche_omissions(view: Any) -> frozenset[str]:
    """Exact tranche paths to omit so the projected view stays self-consistent.

    Nothing is omitted unless the export is exactly the authorized post-tranche
    form. When it is, every tranche product path present in the view is omitted
    together with the export projection, so the frozen fixture derivation and the
    frozen product verifier observe the same canonical pre-tranche tree.

    A partially present tranche is rejected rather than partially hidden: the
    authorized export exists only alongside the complete product set.
    """
    if _core_export_baseline(view) is None:
        return frozenset()
    present = frozenset(TRANCHE_PRODUCT_PATHS & V25.ps(view))
    if present and present != TRANCHE_PRODUCT_PATHS:
        base.fail(
            "v33 authorized Core export is present with an incomplete tranche "
            f"product set: {sorted(present)}"
        )
    return present


def _predecessor_replacements(view: Any) -> dict[str, bytes]:
    replacements = _workflow_replacements(view)
    baseline = _core_export_baseline(view)
    if baseline is not None:
        replacements[CORE_EXPORT] = baseline
    return replacements


def _run_under_predecessor_projection(
    view: Any, label: str, fn: Callable[[], Any]
) -> Any:
    """Run a predecessor entry point against a coherent pre-tranche view."""
    replacements = _predecessor_replacements(view)
    omitted = pretranche_omissions(view)
    target = _ProjectionView(view, replacements, omitted)

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
                base.fail(f"v33 predecessor projection exceeds read bound: {path}")
            return data
        return original_local_read(local_view, path, limit)

    base.LocalRepositoryView.read_bytes = projected_local_read
    try:
        return _call(label, fn)
    finally:
        base.LocalRepositoryView.read_bytes = original_local_read
        for module, original in reversed(patched_roots):
            setattr(module, "root", original)


def run_predecessor_selftests(view: Any) -> None:
    _run_under_predecessor_projection(view, "v32 predecessor self-tests", p.selftest)


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths == BOOT:
            req_v32(candidate)
            req_v32(policy_base)
            if not V26.deps_ready(candidate) or not V26.deps_ready(policy_base):
                base.fail(
                    "v33 bootstrap requires the exact canonical admitted "
                    "dependency state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v33 bootstrap delta must be exactly two v33 policy files "
                "plus two integrity workflows"
            )
        base.fail(
            "v33 bootstrap base authorizes only exact pre-tranche view repair"
        )

    if paths & ALL_POLICY_FILES:
        base.fail(
            "canonical v33/v32/v31/v30/v29/v28/v27/v26/v25 policy files are "
            "frozen after activation"
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
                base.fail(f"v33 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v33 policy file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v33 policy file unexpectedly in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v33 steady-state policy file drifted: {path}")
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
        base.fail(f"v33 policy files missing: {sorted(missing)}")
    approved = {
        P: root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(POLICY_FILES):
        if V25.mode(view, path) != "100644":
            base.fail(f"v33 policy file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v33 policy file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not P_PRINTER:
        base.fail("v33 predecessor printer drifted")
    _call("v32 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v33=PRETRANCHE_VIEW_REPAIR_ONLY")
    print(f"v33_authority={AUTH}")
    print(f"s2_implementation_authority_v33={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v33={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v33={SOURCE_ADMISSION}")
    print("v33_predecessor_view=EXACT_CANONICAL_PRETRANCHE_EXPORT_AND_ENTRIES")
    print("v33_entry_projection_scope=PROJECTION_WRAPPER_ONLY")


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            P_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v33 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in PREDECESSOR_CHAIN):
        base.fail("v33 workflow identity projection drifted")


def prepare_p() -> None:
    current = dict(p.WF)
    if current not in (P_WF, dict(WF)):
        base.fail(f"v33 predecessor workflow identity map drifted: actual={current}")
    for module in PREDECESSOR_CHAIN:
        module.WF = dict(WF)


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    _run_under_predecessor_projection(root, "v32 predecessor install", p.install)
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v32 routing hook"), P_DELTA),
        (base.compare_base_controlled, P_BASE),
        (
            _attr(execution, "freeze_s1_005_evidence", "v32 S1-005 evidence-freeze hook"),
            P_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v32 desktop hook"), P_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v32 execution hook"), P_EEXT),
        (_attr(shell, "validate_allowed_paths", "v32 allowed hook"), P_ALLOWED),
        (_attr(shell, "verify_policy_files", "v32 files hook"), P_FILES),
        (_attr(shell, "print_success", "v32 printer"), P_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v33 predecessor hook drifted")

    _PRINT = P_PRINTER
    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(POLICY_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(POLICY_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v33 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v33 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v33 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v33 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v33 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v33 allowed hook")
    _bind(shell, "verify_policy_files", files, "v33 files hook")
    _bind(shell, "print_success", printer, "v33 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v33_selftest import run

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
