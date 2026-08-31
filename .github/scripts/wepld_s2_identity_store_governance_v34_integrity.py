#!/usr/bin/env python3
"""Authorize one exact canonical-documentation transition; widen nothing else.

Two documents that governance requires currently have no write route.

`docs/learning/BUILD_LEARNING_LEDGER.md` is pinned by
`wepld_s1_admission_steady_state_routing_v18_integrity.py`, whose `state()` is
called from `files()` against every view. The pin is therefore global rather
than delta-scoped: any candidate carrying different ledger bytes fails whatever
else it changes. `AGENTS.md` nonetheless makes Build Learning capture required,
and S2-A009 asks for it on this slice, so the requirement and the mechanism
contradict each other.

`docs/canonical/CURRENT_STATE.md` fails differently. It matches no authorized
delta class at all and falls through to the innermost frozen expectation, which
reports it as an unexpected path in the S1-011 test-only surface. `AGENTS.md`
lists that file first in its mandatory read order, and the file itself is the
project's durable continuation memory, so it cannot be corrected either.

v34 authorizes exactly one two-file transition between exact pinned blobs, and
widens the inherited S1-016 ledger pin by exactly one value so the evaluation
accepts the authorized post-transition ledger as well as the pinned one. Nothing
else changes: no dependency, product, source, filesystem, process, Git, network,
model/provider, Doctor/CLI, or S3+ authority is added, and no other path becomes
writable.

The pin is widened rather than the bytes reconstructed. Reconstruction was the
first design and it was wrong: it could only work on a tree that still carried
the pre-transition ledger, so the policy would have failed on canonical main the
moment its own transition merged.

The transition is one-way and exact. After it merges, the only ledger and
checkpoint bytes this policy accepts are the post-transition ones, so this
successor cannot be reused to write those files again.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

import wepld_integrity as base
import wepld_s2_identity_store_governance_v33_integrity as q

V33 = q
V32 = q.V32
V31 = q.V31
V30 = q.V30
V29 = q.V29
V28 = q.V28
V27 = q.V27
V26 = q.V26
V25 = q.V25

# The complete frozen predecessor chain, ordered newest first. The workflow
# identity projection must cover every level, exactly as v33 does, or an
# inherited level compares against a stale map.
PREDECESSOR_CHAIN = (q,) + q.PREDECESSOR_CHAIN

P = ".github/scripts/wepld_s2_identity_store_governance_v34_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v34_selftest.py"
T_BLOB = "44fa31fdffc8657fd47cc4b8170f9dcb71959a79"
V33_P_BLOB = "f2a7626fcead2984749457b203dcd2523f6982a2"
V33_T_BLOB = "e2eb9fa5a6393305a6465be71aea53bb2193a586"

FW = V25.FW
AW = V25.AW
CW = V25.CW

# The exact authorized documentation transition.
CHECKPOINT = "docs/canonical/CURRENT_STATE.md"
LEDGER = "docs/learning/BUILD_LEARNING_LEDGER.md"
DOCS = frozenset({CHECKPOINT, LEDGER})

PRE_CHECKPOINT_BLOB = "ec89f1203c03fe453336f5a7199b092a92b63c65"
FINAL_CHECKPOINT_BLOB = "2620c272d99eebe36d3756f12f3fe0ff611207a9"
PRE_LEDGER_BLOB = "b18343c12e9e5dcfebcc3694be2e50dc4c9a2405"
FINAL_LEDGER_BLOB = "f06e42dbd2a5e658cc1dc7c9ea7d768ceae458fb"

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_CANONICAL_DOCUMENTATION_TRANSITION_ONLY"
S2_IMPLEMENTATION_AUTHORITY = q.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = q.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = q.SOURCE_ADMISSION

Q_WF = dict(q.WF)
WF = {
    FW: "ae4fd77e4d1b111a33c92a8b07882516e3fd8518cbd08cbe2a5f5be4bb6f456d",
    AW: "730028d4c9214f8ea4bffd49a8675f40b8bc037394c8cba5adc810fadb2ee81c",
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
Q_FREEZE = q.P_FREEZE

_V34_ENTRYPOINT = b"wepld_s2_identity_store_governance_v34_integrity.py"
_V33_ENTRYPOINT = b"wepld_s2_identity_store_governance_v33_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

root = q.root
for _path, _expected in ((q.P, V33_P_BLOB), (q.T, V33_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v34 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = q._call
_attr = q._attr
_bind = q._bind
_ProjectionView = q._ProjectionView
_INST = False
_PRINT: Any = None

# The inherited S1-016 evaluation that pins the ledger.
#
# `state()` is reached from `files()`, which runs against every view, so the pin
# is global rather than delta-scoped. v34 has to widen it by exactly one value
# and no more.
_V18_NAME = "wepld_s1_admission_steady_state_routing_v18_integrity"
_V18 = sys.modules.get(_V18_NAME)
if _V18 is None:
    base.fail(f"v34 could not observe the inherited S1-016 evaluation: {_V18_NAME}")
_V18_STATE = _attr(_V18, "state", "S1-016 state evaluation")
if _attr(_V18, "FINAL_LEARNING_BLOB", "S1-016 ledger pin") != PRE_LEDGER_BLOB:
    base.fail(
        "v34 expected the inherited S1-016 ledger pin to equal the pinned "
        "pre-transition blob"
    )
if _attr(_V18, "LEARNING", "S1-016 ledger path") != LEDGER:
    base.fail("v34 expected the inherited S1-016 ledger path to match")


def _state(view: Any) -> Any:
    """Accept the authorized post-transition ledger, and nothing else new.

    The inherited evaluation pins one ledger blob. Rather than reconstructing the
    pinned bytes, which a tree carrying the transition no longer has, this widens
    the pin to the authorized post-transition value for the duration of one call
    and restores it immediately. Every other check inside the inherited
    evaluation runs unchanged, and any ledger that is neither pinned blob reaches
    the original failure.

    Reconstructing bytes was the first design and it was wrong: it could only
    work on a tree that still carried the pre-transition ledger, so the policy
    would have failed on canonical main the moment its own transition merged.
    """
    actual = V25.blob(view.read_bytes(LEDGER, base.MAX_POLICY_FILE_BYTES))
    if actual != FINAL_LEDGER_BLOB:
        return _V18_STATE(view)
    original = _V18.FINAL_LEARNING_BLOB
    _V18.FINAL_LEARNING_BLOB = FINAL_LEDGER_BLOB
    try:
        return _V18_STATE(view)
    finally:
        _V18.FINAL_LEARNING_BLOB = original


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v33(view: Any) -> None:
    for path, expected in ((q.P, V33_P_BLOB), (q.T, V33_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v34 candidate/base is missing frozen v33 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v33 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V34_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v34 workflow entrypoint count drifted before predecessor "
                f"projection: {path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} "
                f"actual={count}"
            )
        predecessor = data.replace(_V34_ENTRYPOINT, _V33_ENTRYPOINT)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v34 workflow does not reverse to exact canonical v33 "
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
    """Run a predecessor entry point against the projected workflow view."""
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
                base.fail(f"v34 predecessor projection exceeds read bound: {path}")
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
    """Verify the exact authorized documentation transition and nothing else."""
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
                base.fail(f"v34 documentation transition {label} is missing: {path}")
            if V25.mode(view, path) != "100644":
                base.fail(f"v34 documentation transition file mode invalid: {path}")
            actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
            if actual != wanted:
                base.fail(
                    f"v34 documentation transition {label} bytes drifted: {path}: "
                    f"expected={wanted} actual={actual}"
                )


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths == BOOT:
            req_v33(candidate)
            req_v33(policy_base)
            return
        if paths & BOOT:
            base.fail(
                "v34 bootstrap delta must be exactly two v34 policy files plus "
                "two integrity workflows"
            )
        base.fail(
            "v34 bootstrap base authorizes only exact canonical-documentation "
            "transition activation"
        )

    if paths & ALL_POLICY_FILES:
        base.fail(
            "canonical v34 and every frozen predecessor policy file are frozen "
            "after activation"
        )

    if paths == DOCS:
        docs_transition(candidate, policy_base)
        return
    if paths & DOCS:
        base.fail(
            "v34 documentation transition must be exactly the two authorized "
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
                base.fail(f"v34 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v34 policy file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v34 policy file unexpectedly in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v34 steady-state policy file drifted: {path}")
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
        base.fail(f"v34 policy files missing: {sorted(missing)}")
    approved = {
        P: root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(POLICY_FILES):
        if V25.mode(view, path) != "100644":
            base.fail(f"v34 policy file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v34 policy file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not Q_PRINTER:
        base.fail("v34 predecessor printer drifted")
    _call("v33 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v34=CANONICAL_DOCUMENTATION_TRANSITION_ONLY")
    print(f"v34_authority={AUTH}")
    print(f"s2_implementation_authority_v34={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v34={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v34={SOURCE_ADMISSION}")
    print("v34_documentation_transition=EXACT_TWO_PATH_PINNED_ONE_WAY")
    print("v34_ledger_pin=WIDENED_BY_EXACTLY_ONE_AUTHORIZED_BLOB")


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
        base.fail("v34 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in PREDECESSOR_CHAIN):
        base.fail("v34 workflow identity projection drifted")
    if _attr(_V18, "state", "S1-016 state hook") is not _state:
        base.fail("v34 S1-016 ledger-pin widening drifted")
    if _V18.FINAL_LEARNING_BLOB != PRE_LEDGER_BLOB:
        base.fail("v34 left the inherited S1-016 ledger pin widened after a call")


def prepare_q() -> None:
    current = dict(q.WF)
    if current not in (Q_WF, dict(WF)):
        base.fail(f"v34 predecessor workflow identity map drifted: actual={current}")
    for module in PREDECESSOR_CHAIN:
        module.WF = dict(WF)


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return

    _run_under_predecessor_projection(root, "v33 predecessor install", q.install)
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v33 routing hook"), Q_DELTA),
        (base.compare_base_controlled, Q_BASE),
        (
            _attr(execution, "freeze_s1_005_evidence", "v33 S1-005 evidence-freeze hook"),
            Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v33 desktop hook"), Q_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v33 execution hook"), Q_EEXT),
        (_attr(shell, "validate_allowed_paths", "v33 allowed hook"), Q_ALLOWED),
        (_attr(shell, "verify_policy_files", "v33 files hook"), Q_FILES),
        (_attr(shell, "print_success", "v33 printer"), Q_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v34 predecessor hook drifted")

    _PRINT = Q_PRINTER
    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(POLICY_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(POLICY_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v34 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v34 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v34 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v34 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v34 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v34 allowed hook")
    _bind(shell, "verify_policy_files", files, "v34 files hook")
    _bind(shell, "print_success", printer, "v34 printer hook")
    _bind(_V18, "state", _state, "v34 S1-016 ledger-pin widening")
    _INST = True
    overlay()


def run_predecessor_selftests(view: Any) -> None:
    _run_under_predecessor_projection(view, "v33 predecessor self-tests", q.selftest)


def selftest() -> None:
    from wepld_s2_identity_store_governance_v34_selftest import run

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
