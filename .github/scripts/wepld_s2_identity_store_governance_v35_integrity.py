#!/usr/bin/env python3
"""Correct the one-shot canonical-documentation transition target; widen nothing else.

Canonical v34 authorized one exact two-document transition. Before that transition
was accepted, an author self-audit of PR #248 found two material defects in the
frozen CURRENT_STATE.md FINAL blob: stale Build Learning continuation state and
an incorrect platform/project classification of an at-acceptance review-thread
claim.

v35 does not authorize a second documentation write route and does not broaden
v34. It supersedes exactly one v34 target identity: the checkpoint FINAL blob.
The PRE checkpoint, PRE ledger, FINAL ledger, two-path transition shape, ledger
widening, dependency/source/product/effect authority, and every inherited guard
remain unchanged. The superseded v34 FINAL checkpoint is not accepted by v35.

The correction is content-addressed and one-shot. The corrected checkpoint bytes
were frozen separately after a bounded authoring diff containing only the two
validated findings. The real documentation candidate must still satisfy both
pinned FINAL blobs at the deterministic gates and receive independent review.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

import wepld_integrity as base
import wepld_s2_identity_store_governance_v34_integrity as q

V34 = q
V33 = q.V33
V32 = q.V32
V31 = q.V31
V30 = q.V30
V29 = q.V29
V28 = q.V28
V27 = q.V27
V26 = q.V26
V25 = q.V25

PREDECESSOR_CHAIN = (q,) + q.PREDECESSOR_CHAIN

P = ".github/scripts/wepld_s2_identity_store_governance_v35_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v35_selftest.py"
T_BLOB = "8284914739d1842f5100480fed969ec04d8667c7"
V34_P_BLOB = "4f8fd136df3841f3427cc28cb543aa9da4afb03a"
V34_T_BLOB = "dcfae36aee07fcd5eac9119a049ee0cdc1d6c13c"

FW = q.FW
AW = q.AW
CW = q.CW

CHECKPOINT = q.CHECKPOINT
LEDGER = q.LEDGER
DOCS = frozenset({CHECKPOINT, LEDGER})

PRE_CHECKPOINT_BLOB = q.PRE_CHECKPOINT_BLOB
PRE_LEDGER_BLOB = q.PRE_LEDGER_BLOB
FINAL_LEDGER_BLOB = q.FINAL_LEDGER_BLOB
V34_FINAL_CHECKPOINT_BLOB = "2620c272d99eebe36d3756f12f3fe0ff611207a9"
FINAL_CHECKPOINT_BLOB = "28c50353718f4b836daf67df2a52f6d9471e847b"

if PRE_CHECKPOINT_BLOB == FINAL_CHECKPOINT_BLOB:
    base.fail("v35 corrected checkpoint target equals the PRE checkpoint")
if FINAL_CHECKPOINT_BLOB == V34_FINAL_CHECKPOINT_BLOB:
    base.fail("v35 corrected checkpoint target equals the superseded v34 target")


def _bind_corrected_checkpoint_target() -> None:
    """Bind v34 to exactly the corrected checkpoint target, idempotently.

    The v35 script can be executed as ``__main__`` and then imported by its
    self-test module under its canonical module name in the same interpreter.
    That second import must not be mistaken for predecessor drift. Exactly two
    values are valid at this seam: the frozen v34 target before the first bind,
    or the corrected v35 target after an earlier bind. Any third value fails
    closed.
    """
    actual = q.FINAL_CHECKPOINT_BLOB
    if actual == V34_FINAL_CHECKPOINT_BLOB:
        q.FINAL_CHECKPOINT_BLOB = FINAL_CHECKPOINT_BLOB
        return
    if actual == FINAL_CHECKPOINT_BLOB:
        return
    base.fail(
        "v35 inherited v34 checkpoint target is outside the exact old/corrected set: "
        f"old={V34_FINAL_CHECKPOINT_BLOB} corrected={FINAL_CHECKPOINT_BLOB} "
        f"actual={actual}"
    )


# v34 self-tests and inherited transition logic must evaluate the corrected
# target while v35 is active. This is an in-memory successor binding only; the
# frozen v34 repository bytes are unchanged and are verified below.
_bind_corrected_checkpoint_target()

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_CANONICAL_DOCUMENTATION_TRANSITION_CORRECTION_ONLY"
S2_IMPLEMENTATION_AUTHORITY = q.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = q.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = q.SOURCE_ADMISSION

Q_WF = dict(q.WF)
WF = {
    FW: "3d03db5e9afcf8c2b0c58acac121005a9acc808c22028ddb83e11f45c213ac6f",
    AW: "e560dfa90aa26aa3c665fe4e7b2083b4e86f100d47e19e4e6b9f70fa00dd73bc",
    CW: q.WF[CW],
}

Q_DELTA = q.delta
Q_BASE = q.basectrl
Q_EXT = q.ext
Q_DEXT = q.dext
Q_EEXT = q.eext
Q_ALLOWED = q.allowed
Q_FILES = q.files
Q_PRINTER = q.printer
Q_FREEZE = q.Q_FREEZE

_V35_ENTRYPOINT = b"wepld_s2_identity_store_governance_v35_integrity.py"
_V34_ENTRYPOINT = b"wepld_s2_identity_store_governance_v34_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

root = q.root
for _path, _expected in ((q.P, V34_P_BLOB), (q.T, V34_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v35 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = q._call
_attr = q._attr
_bind = q._bind
_ProjectionView = q._ProjectionView
_INST = False
_PRINT: Any = None


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v34(view: Any) -> None:
    for path, expected in ((q.P, V34_P_BLOB), (q.T, V34_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v35 candidate/base is missing frozen v34 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v34 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V35_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v35 workflow entrypoint count drifted before predecessor "
                f"projection: {path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} "
                f"actual={count}"
            )
        predecessor = data.replace(_V35_ENTRYPOINT, _V34_ENTRYPOINT)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v35 workflow does not reverse to exact canonical v34 "
                f"predecessor: {path} expected={Q_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return replacements


def _predecessor_replacements(view: Any) -> dict[str, bytes]:
    return _workflow_replacements(view)


def _predecessor_projection(view: Any) -> Any:
    return _ProjectionView(view, _predecessor_replacements(view))


def _run_under_predecessor_projection(
    view: Any, label: str, fn: Callable[[], Any]
) -> Any:
    replacements = _predecessor_replacements(view)
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
                base.fail(f"v35 predecessor projection exceeds read bound: {path}")
            return data
        return original_local_read(local_view, path, limit)

    base.LocalRepositoryView.read_bytes = projected_local_read
    try:
        return _call(label, fn)
    finally:
        base.LocalRepositoryView.read_bytes = original_local_read
        for module, original in reversed(patched_roots):
            setattr(module, "root", original)


def docs_transition(candidate: Any, policy_base: Any) -> None:
    """Verify the corrected exact two-document transition and nothing else."""
    expected = (
        (CHECKPOINT, PRE_CHECKPOINT_BLOB, FINAL_CHECKPOINT_BLOB),
        (LEDGER, PRE_LEDGER_BLOB, FINAL_LEDGER_BLOB),
    )
    for path, pre, final in expected:
        for view, label, wanted in (
            (policy_base, "base", pre),
            (candidate, "candidate", final),
        ):
            if path not in V25.ps(view):
                base.fail(f"v35 documentation transition {label} is missing: {path}")
            if V25.mode(view, path) != "100644":
                base.fail(f"v35 documentation transition file mode invalid: {path}")
            actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
            if actual != wanted:
                base.fail(
                    f"v35 documentation transition {label} bytes drifted: {path}: "
                    f"expected={wanted} actual={actual}"
                )


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths == BOOT:
            req_v34(candidate)
            req_v34(policy_base)
            return
        if paths & BOOT:
            base.fail(
                "v35 bootstrap delta must be exactly two v35 policy files plus "
                "two integrity workflows"
            )
        base.fail(
            "v35 bootstrap base authorizes only corrected canonical-documentation "
            "transition activation"
        )

    if paths & ALL_POLICY_FILES:
        base.fail(
            "canonical v35 and every frozen predecessor policy file are frozen "
            "after activation"
        )

    if paths == DOCS:
        docs_transition(candidate, policy_base)
        return
    if paths & DOCS:
        base.fail(
            "v35 documentation transition must be exactly the two corrected "
            "canonical documentation paths and nothing else"
        )

    Q_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        Q_BASE(_predecessor_projection(candidate), _predecessor_projection(policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v35 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v35 policy file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v35 policy file unexpectedly in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v35 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        Q_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES
    if remaining:
        Q_ALLOWED(remaining, stage)


def files(view: Any) -> None:
    Q_FILES(_predecessor_projection(view))
    missing = POLICY_FILES - V25.ps(view)
    if missing:
        base.fail(f"v35 policy files missing: {sorted(missing)}")
    approved = {
        P: root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(POLICY_FILES):
        if V25.mode(view, path) != "100644":
            base.fail(f"v35 policy file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v35 policy file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not Q_PRINTER:
        base.fail("v35 predecessor printer drifted")
    _call("v34 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v35=CANONICAL_DOCUMENTATION_TRANSITION_CORRECTION_ONLY")
    print(f"v35_authority={AUTH}")
    print(f"s2_implementation_authority_v35={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v35={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v35={SOURCE_ADMISSION}")
    print("v35_checkpoint_target=CORRECTED_EXACT_BLOB")
    print("v35_ledger_target=UNCHANGED_FROM_V34")


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v35 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in PREDECESSOR_CHAIN):
        base.fail("v35 workflow identity projection drifted")
    if q.FINAL_CHECKPOINT_BLOB != FINAL_CHECKPOINT_BLOB:
        base.fail("v35 inherited v34 checkpoint target binding drifted")
    if q.FINAL_LEDGER_BLOB != FINAL_LEDGER_BLOB:
        base.fail("v35 inherited v34 ledger target drifted")
    if _attr(q._V18, "state", "S1-016 state hook") is not q._state:
        base.fail("v35 inherited ledger widening hook drifted")
    if q._V18.FINAL_LEARNING_BLOB != PRE_LEDGER_BLOB:
        base.fail("v35 left the inherited ledger pin widened after a call")


def prepare_q() -> None:
    current = dict(q.WF)
    if current not in (Q_WF, dict(WF)):
        base.fail(f"v35 predecessor workflow identity map drifted: actual={current}")
    for module in PREDECESSOR_CHAIN:
        module.WF = dict(WF)


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    _run_under_predecessor_projection(root, "v34 predecessor install", q.install)
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v34 routing hook"), Q_DELTA),
        (base.compare_base_controlled, Q_BASE),
        (
            _attr(execution, "freeze_s1_005_evidence", "v34 S1-005 evidence-freeze hook"),
            Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v34 desktop hook"), Q_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v34 execution hook"), Q_EEXT),
        (_attr(shell, "validate_allowed_paths", "v34 allowed hook"), Q_ALLOWED),
        (_attr(shell, "verify_policy_files", "v34 files hook"), Q_FILES),
        (_attr(shell, "print_success", "v34 printer"), Q_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v35 predecessor hook drifted")

    _PRINT = Q_PRINTER
    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(POLICY_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(POLICY_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v35 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v35 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v35 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v35 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v35 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v35 allowed hook")
    _bind(shell, "verify_policy_files", files, "v35 files hook")
    _bind(shell, "print_success", printer, "v35 printer hook")
    _INST = True
    overlay()


def run_predecessor_selftests(view: Any) -> None:
    _run_under_predecessor_projection(view, "v34 predecessor self-tests", q.selftest)


def selftest() -> None:
    from wepld_s2_identity_store_governance_v35_selftest import run

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
