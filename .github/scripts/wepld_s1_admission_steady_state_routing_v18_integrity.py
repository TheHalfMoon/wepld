#!/usr/bin/env python3
"""Authorize one exact S1-016 acceptance/Build Learning transition; keep S2 closed.

v18 is an append-only successor to canonical v17. After canonical activation it
authorizes exactly one three-file S1-016 transition: acceptance.md, tasks.md,
and BUILD_LEARNING_LEDGER.md. No S2, roadmap, source, dependency, runtime,
provider, model, or effect authority is granted.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v18_integrity.py"
V17 = ".github/scripts/wepld_s1_admission_steady_state_routing_v17_integrity.py"
V17_BLOB = "a40f377a08b47a5270194c9d1f77961772a448ac"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"
ACCEPTANCE = "specs/001-desktop-rust-trusted-core-handshake/acceptance.md"
LEARNING = "docs/learning/BUILD_LEARNING_LEDGER.md"
S1_015_EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-015-repair-evidence.md"

OLD_WF = {
    FW: "4082d9037db9123924dce5181124d2b86cb5e4ac8836bad4f6cb90f29af9d17d",
    AW: "201ac44a5597e5f099eab178301f30cf058976b37d48d5bed4a66645dbafe276",
}
WF = {
    FW: "03d5356769c4d2db4e9d45c44a667681d61395aab87f8a8b814721b5ce98061f",
    AW: "aa35676a8526b12ab15e02cf998caa460b98b8326b0eb5d7dda5285f792f12c0",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

PRE_TASKS_BLOB = "559e2ac83600a1a3e38602a29dead366bc950e64"
PRE_ACCEPTANCE_BLOB = "32b01bc699938779341d70fe23fc84f82fd32e05"
PRE_LEARNING_BLOB = "959139ca96eba1133611515c0ec655bc11b6c11d"
FINAL_ACCEPTANCE_BLOB = "565f3d55a0f48bed8d431bac6424c57e3849735c"
FINAL_LEARNING_BLOB = "b18343c12e9e5dcfebcc3694be2e50dc4c9a2405"
S1_015_EVID_BLOB = "384b99d46eef802ef04cb3674bce3fee8a64be83"

BOOT = frozenset({P, FW, AW})
ACCEPT = frozenset({TASKS, ACCEPTANCE, LEARNING})
AUTH = "S1_016_EXACT_ACCEPTANCE_AND_BUILD_LEARNING_ONLY"
S2 = "NOT_AUTHORIZED"
TRUSTED_BASE_V17_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"  # noqa: S105

TOP_PRE = '```text\nSLICE = S1\nS1_ORIGINAL_BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679\nCANONICAL_EXECUTION_HEAD = 9ae784106f36c2234e3cdf6befdb03449a224c34\nLEDGER_RECONCILIATION_BASE = 9ae784106f36c2234e3cdf6befdb03449a224c34\nLIVE_MAIN = MUST_BE_READ_FROM_GITHUB\nACTIVE_TASK = NONE\nNEXT_TASK = S1-016_NOT_STARTED\nFOUNDER_STANDING_AUTHORIZATION = GRANTED\nSOURCE_ACQUISITION_CHECK = PASS\nRUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH\nIMPLEMENTATION = CANONICAL_THROUGH_S1_011\nS1_012_CANONICAL_ACTIVATION = PROVEN\nS1_013_CANONICAL_MEASUREMENT = PROVEN\nS1_013_EVIDENCE_RECONCILIATION = PROVEN\nS1_014_REVIEW_RECONCILIATION = PROVEN_BY_THIS_CANONICAL_LEDGER\nS1_015 = CLOSED_CANONICAL_PROVEN\nS1_016 = NOT_STARTED\n```'
TOP_POST = '```text\nSLICE = S1\nS1_ORIGINAL_BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679\nCANONICAL_EXECUTION_HEAD = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd\nLEDGER_RECONCILIATION_BASE = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd\nLIVE_MAIN = MUST_BE_READ_FROM_GITHUB\nACTIVE_TASK = NONE\nNEXT_TASK = S2_NOT_STARTED_NOT_AUTHORIZED\nFOUNDER_STANDING_AUTHORIZATION = GRANTED\nSOURCE_ACQUISITION_CHECK = PASS\nRUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH\nIMPLEMENTATION = CANONICAL_THROUGH_S1_011\nS1_012_CANONICAL_ACTIVATION = PROVEN\nS1_013_CANONICAL_MEASUREMENT = PROVEN\nS1_013_EVIDENCE_RECONCILIATION = PROVEN\nS1_014_REVIEW_RECONCILIATION = PROVEN_BY_THIS_CANONICAL_LEDGER\nS1_015 = CLOSED_CANONICAL_PROVEN\nS1_016 = CLOSED_CANONICAL_PROVEN\nS1_ACCEPTED = YES\nS2 = NOT_STARTED\nS2_AUTHORITY = NOT_GRANTED\n```'
CHECKPOINT_ANCHOR = 'The Codex Security coverage limitation remains explicit and is not converted into PASS. S1-015 closeout also does not accept S1; S1-016 remains the separate acceptance and Build Learning task.\n\n'
S1_016_CHECKPOINT = '## Canonical S1-016 acceptance and Build Learning reconciliation checkpoint — 2026-08-27\n\nThis checkpoint accepts S1 only after the complete S1 evidence chain, bounded repair, canonical S1-015 closeout, and post-merge Foundation verification are reconciled. It records the accepted execution head and the Build Learning material promoted by this exact transition. It grants no S2 implementation or roadmap-mutation authority.\n\n```text\nS1-016 = CLOSED_CANONICAL_PROVEN\nS1_ACCEPTED = YES\nS1_ACCEPTANCE_EXECUTION_HEAD = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd\nS1_ACCEPTANCE_EXECUTION_TREE = c63bea084edd9cc1f3fcfe5f574518339f510426\nS1-015_CLOSEOUT_PR = #199\nS1-015_CLOSEOUT_MERGE = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd\nS1-015_CLOSEOUT_POST_MERGE_FOUNDATION = run 33083905553 / #744 / PASS\nS1_ACCEPTANCE_RECORD = specs/001-desktop-rust-trusted-core-handshake/acceptance.md\nS1_BUILD_LEARNING_LEDGER = docs/learning/BUILD_LEARNING_LEDGER.md\nS1_BUILD_LEARNING_QUALIFIED = BL-0004..BL-0009\nS1-014_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING\nS1-014_SECURITY_PASS = NO\nS1-015_UNRESOLVED_MATERIAL_FINDINGS = 0\nS2 = NOT_STARTED\nS2_AUTHORITY = NOT_GRANTED\n```\n\nThe accepted head does not erase explicit coverage limitations. Codex Security remains non-PASS, S3 containment is not claimed, and no later-slice authority is inferred from S1 acceptance.\n\n'
S1_016_PRE = '## S1-016 — Accept S1 and capture learning\n\n- [ ] Verify all S1 acceptance criteria on exact head.\n- [ ] Record standing-founder-authority S1 acceptance bound to that exact head.\n- [ ] Do not treat merge/deploy/reviewer output as completion authority.\n- [ ] Capture qualified positive mechanics and negative oracles in Build Learning.\n- [ ] Merge only after exact-head acceptance/evidence and repository merge rules are satisfied.\n- [ ] Do not begin S2 until S1 is accepted and merged or otherwise canonically closed.\n'
S1_016_POST = '## S1-016 — Accept S1 and capture learning\n\n- [x] Verify all S1 acceptance criteria on exact head.\n- [x] Record standing-founder-authority S1 acceptance bound to that exact head.\n- [x] Do not treat merge/deploy/reviewer output as completion authority.\n- [x] Capture qualified positive mechanics and negative oracles in Build Learning.\n- [x] Merge only after exact-head acceptance/evidence and repository merge rules are satisfied.\n- [x] Do not begin S2 until S1 is accepted and merged or otherwise canonically closed.\n\nEvidence: `acceptance.md` binds S1 acceptance to canonical execution head `9a826e14fa2dd213f656b0ea2fec1ff737eb56dd` after post-merge Foundation #744; `docs/learning/BUILD_LEARNING_LEDGER.md` promotes BL-0004 through BL-0009 in the same exact transition. This transition becomes canonical only after v18 exact-head qualification, independent review, guarded merge, and post-merge verification. S2 remains not started and not authorized by S1 acceptance.\n'
GATE_PRE = '```text\nCOMPLETED = S1-001 THROUGH S1-015\nCURRENT = NONE\nCANONICAL_EXECUTION_HEAD = 9ae784106f36c2234e3cdf6befdb03449a224c34\nS1_012_CANONICAL_ACTIVATION = PROVEN\nS1_013_CANONICAL_MEASUREMENT = PROVEN\nS1_013_EVIDENCE_RECONCILIATION = PROVEN\nS1_014_REVIEW_RECONCILIATION = PROVEN\nS1_015_REPAIR_CLOSEOUT = PROVEN\nNEXT = S1-016\nS1_016 = NOT_STARTED\nSOURCE_ACQUISITION_CHECK = PASS\nRUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH\nIMPLEMENTATION = CANONICAL_THROUGH_S1_011\n```'
GATE_POST = '```text\nCOMPLETED = S1-001 THROUGH S1-016\nCURRENT = NONE\nCANONICAL_EXECUTION_HEAD = 9a826e14fa2dd213f656b0ea2fec1ff737eb56dd\nS1_012_CANONICAL_ACTIVATION = PROVEN\nS1_013_CANONICAL_MEASUREMENT = PROVEN\nS1_013_EVIDENCE_RECONCILIATION = PROVEN\nS1_014_REVIEW_RECONCILIATION = PROVEN\nS1_015_REPAIR_CLOSEOUT = PROVEN\nS1_016_ACCEPTANCE_CLOSEOUT = PROVEN\nS1_ACCEPTED = YES\nNEXT = S2\nS2 = NOT_STARTED\nS2_AUTHORITY = NOT_GRANTED\nSOURCE_ACQUISITION_CHECK = PASS\nRUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH\nIMPLEMENTATION = CANONICAL_THROUGH_S1_011\n```'

_INST = False
_PRINT: Any = None


def blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ps(view: Any) -> set[str]:
    return {entry.path for entry in view.entries()}


def mode(view: Any, path: str) -> str:
    for entry in view.entries():
        if entry.path == path:
            return entry.mode
    base.fail(f"missing path: {path}")


def _call(label: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(fn):
        base.fail(f"v18 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v18 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v18 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v18 {label} topology/layout drifted: {exc}")


def _decode_utf8(data: bytes, label: str) -> str:
    try:
        return data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        base.fail(f"S1-016 {label} is not UTF-8: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V17, base.MAX_POLICY_FILE_BYTES)) != V17_BLOB:
    base.fail("frozen v17 predecessor drifted")

import wepld_s1_admission_steady_state_routing_v17_integrity as v17  # noqa: E402

V17_DELTA = v17.delta
V17_BASE = v17.basectrl
V17_ALLOWED = v17.allowed
V17_FILES = v17.files
V17_DEXT = v17.dext
V17_EEXT = v17.eext
V17_EXT = v17.ext
V17_PRINT = v17.printer
V17_WF = dict(v17.WF)
CAND = v17.CAND
RUNTIME = v17.RUNTIME

if V17_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v17 workflow identities drifted before v18 import: actual={V17_WF}")
if _attr(v17, "AUTH", "v17 authority marker") != "S1_015_EXACT_REPAIR_LEDGER_CLOSEOUT_ONLY":
    base.fail("v18 observed v17 authority drift")
if _attr(v17, "S1_016", "v17 S1-016 boundary") != "NOT_AUTHORIZED":
    base.fail("v18 observed v17 S1-016 boundary drift")


def req_v17(view: Any) -> None:
    if V17 not in ps(view) or blob(view.read_bytes(V17, base.MAX_POLICY_FILE_BYTES)) != V17_BLOB:
        base.fail("v18 requires exact frozen v17 predecessor")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v17, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v18 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v18 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v17, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v18 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        base.fail(f"S1-016 {label} occurrence drifted: expected=1 actual={count}")
    return text.replace(old, new, 1)


def expected_tasks(predecessor: bytes) -> bytes:
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("S1-016 predecessor ledger identity drifted")
    text = _decode_utf8(predecessor, "predecessor ledger")
    text = _replace_once(text, TOP_PRE, TOP_POST, "top checkpoint")
    text = _replace_once(text, CHECKPOINT_ANCHOR, CHECKPOINT_ANCHOR + S1_016_CHECKPOINT, "checkpoint")
    text = _replace_once(text, S1_016_PRE, S1_016_POST, "checklist")
    text = _replace_once(text, GATE_PRE, GATE_POST, "current gate")
    return text.encode("utf-8")


def reverse_tasks(accepted: bytes) -> bytes:
    text = _decode_utf8(accepted, "accepted ledger")
    text = _replace_once(text, TOP_POST, TOP_PRE, "reverse top checkpoint")
    text = _replace_once(text, CHECKPOINT_ANCHOR + S1_016_CHECKPOINT, CHECKPOINT_ANCHOR, "reverse checkpoint")
    text = _replace_once(text, S1_016_POST, S1_016_PRE, "reverse checklist")
    text = _replace_once(text, GATE_POST, GATE_PRE, "reverse current gate")
    predecessor = text.encode("utf-8")
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("S1-016 accepted ledger does not reverse to exact predecessor")
    return predecessor


class _TaskProjection:
    def __init__(self, view: Any, predecessor_tasks: bytes) -> None:
        self._view = view
        self._predecessor_tasks = predecessor_tasks

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path == TASKS:
            if len(self._predecessor_tasks) > max_bytes:
                base.fail("projected S1 task ledger exceeds read bound")
            return self._predecessor_tasks
        return self._view.read_bytes(path, max_bytes)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def common(view: Any) -> None:
    for path in (TASKS, ACCEPTANCE, LEARNING, S1_015_EVID):
        if path not in ps(view) or mode(view, path) != "100644":
            base.fail(f"S1-016 requires canonical path/mode: {path}")
    if blob(view.read_bytes(S1_015_EVID, base.MAX_POLICY_FILE_BYTES)) != S1_015_EVID_BLOB:
        base.fail("S1-016 canonical S1-015 evidence drifted")


def state(view: Any) -> str:
    common(view)
    tasks = view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    acceptance = view.read_bytes(ACCEPTANCE, base.MAX_POLICY_FILE_BYTES)
    learning = view.read_bytes(LEARNING, base.MAX_POLICY_FILE_BYTES)
    if (
        blob(tasks) == PRE_TASKS_BLOB
        and blob(acceptance) == PRE_ACCEPTANCE_BLOB
        and blob(learning) == PRE_LEARNING_BLOB
    ):
        return "PRE_S1_016"
    reverse_tasks(tasks)
    if blob(acceptance) != FINAL_ACCEPTANCE_BLOB:
        base.fail("S1-016 acceptance bytes drifted")
    if blob(learning) != FINAL_LEARNING_BLOB:
        base.fail("S1-016 Build Learning bytes drifted")
    return "ACCEPTED_S1"


def accept(candidate: Any, policy_base: Any) -> None:
    if state(policy_base) != "PRE_S1_016":
        base.fail("S1-016 policy base is not exact pre-acceptance state")
    if state(candidate) != "ACCEPTED_S1":
        base.fail("S1-016 candidate did not reach exact accepted state")
    if candidate.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES) != expected_tasks(
        policy_base.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    ):
        base.fail("S1-016 reconciled ledger bytes drifted")


def patch_predecessor() -> None:
    current = dict(v17.WF)
    if current not in (V17_WF, dict(WF)):
        base.fail(f"v18 predecessor workflow map drifted: {current}")
    _bind(v17, "WF", dict(WF), "v17 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v17(candidate)
            req_v17(policy_base)
            return
        if paths & BOOT:
            base.fail("v18 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v18 bootstrap base authorizes only exact policy/workflow activation")
    if P in paths:
        base.fail("canonical v18 wrapper is frozen after activation")
    if paths == ACCEPT:
        accept(candidate, policy_base)
        return
    if paths & ACCEPT:
        base.fail("S1-016 delta must be exactly tasks plus acceptance plus Build Learning")
    _call("v17 exact-delta verifier", V17_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if bootbase(policy_base):
        for path in sorted(base.BASE_CONTROLLED_PATHS):
            cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
            bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
            if path in (FW, AW):
                if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                    base.fail(f"v18 bootstrap workflow drifted: {path}")
            elif cb != bb:
                base.fail(f"base-controlled path changed: {path}")
        return
    _call("v17 base-control verifier", V17_BASE, candidate, policy_base)


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v18 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v18 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(P, base.MAX_POLICY_FILE_BYTES) != policy_base.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ):
            base.fail("v18 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v17 extension verification", V17_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    current = set(paths)
    if current == set(ACCEPT):
        return
    remaining = current - {P}
    if remaining:
        _call("v17 allowed-path verifier", V17_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v17(view)
    current = state(view)
    if current == "PRE_S1_016":
        _call("v17 policy-file verification", V17_FILES, view)
    elif current == "ACCEPTED_S1":
        predecessor = reverse_tasks(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES))
        _call("v17 projected policy-file verification", V17_FILES, _TaskProjection(view, predecessor))
    else:
        base.fail(f"unknown v18 state: {current}")
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v18 wrapper mode invalid")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V17_PRINT:
        base.fail("v18 predecessor printer drifted")
    _call("v17 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v18=V17_PLUS_EXACT_S1_016_ACCEPTANCE")
    print(f"s1_admission_authority_expansion_v18={AUTH}")
    print("s1_015_closeout_merge_v18=9a826e14fa2dd213f656b0ea2fec1ff737eb56dd")
    print("s1_015_closeout_post_merge_foundation_v18=33083905553_SUCCESS")
    print("s1_acceptance_execution_head_v18=9a826e14fa2dd213f656b0ea2fec1ff737eb56dd")
    print("s1_build_learning_rows_v18=BL_0004_THROUGH_BL_0009")
    print("effective_source_admission_v18=NONE")
    print("effective_dependency_admission_v18=NONE")
    print("new_product_runtime_authority_v18=NONE")
    print("effective_model_provider_execution_v18=NONE")
    print("roadmap_mutation_authority_v18=NONE")
    print("s1_acceptance_authority_v18=EXACT_S1_016_TRANSITION_ONLY")
    print(f"s2_authority_v18={S2}")


def overlay() -> None:
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed-path hook"), allowed),
        (_attr(shell, "verify_policy_files", "policy-file hook"), files),
        (_attr(shell, "print_success", "success hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v18 overlay drifted")


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v17 install", getattr(v17, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V17_DELTA),
        (base.compare_base_controlled, V17_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V17_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V17_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V17_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V17_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V17_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v18 predecessor hook drifted")
    _PRINT = V17_PRINT
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", frozenset(set(extset(desktop)) | {P}), "desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", frozenset(set(extset(execution)) | {P}), "execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "routing binding")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "desktop binding")
    _bind(execution, "verify_extension_controlled_paths", eext, "execution binding")
    _bind(shell, "validate_allowed_paths", allowed, "allowed binding")
    _bind(shell, "verify_policy_files", files, "files binding")
    _bind(shell, "print_success", printer, "printer binding")
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def corrected_v17_selftest() -> None:
    patch_predecessor()
    current = state(root)
    if current == "PRE_S1_016":
        _call("v17 predecessor self-test", getattr(v17, "selftest", None))
        return
    predecessor = reverse_tasks(root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES))
    prior_root = _attr(v17, "root", "v17 root")
    _bind(v17, "root", _TaskProjection(root, predecessor), "v17 root projection")
    try:
        _call("v17 predecessor self-test", getattr(v17, "selftest", None))
    finally:
        _bind(v17, "root", prior_root, "v17 root restoration")


def acceptance_path_selftest() -> None:
    global PRE_ACCEPTANCE_BLOB, PRE_LEARNING_BLOB, FINAL_ACCEPTANCE_BLOB, FINAL_LEARNING_BLOB

    vb = root.read_bytes(V17, base.MAX_POLICY_FILE_BYTES)
    root_state = state(root)
    root_tasks = root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    if root_state == "PRE_S1_016":
        pre_tasks = root_tasks
    elif root_state == "ACCEPTED_S1":
        pre_tasks = reverse_tasks(root_tasks)
    else:
        base.fail(f"v18 acceptance self-test root state drifted: {root_state}")
    evidence = root.read_bytes(S1_015_EVID, base.MAX_POLICY_FILE_BYTES)
    if blob(pre_tasks) != PRE_TASKS_BLOB:
        base.fail("v18 acceptance self-test could not recover exact pre-S1-016 task ledger")
    if blob(evidence) != S1_015_EVID_BLOB:
        base.fail("v18 acceptance self-test S1-015 evidence drifted")

    accepted_tasks = expected_tasks(pre_tasks)
    fixture_pre_acceptance = b"v18-selftest-pre-acceptance\n"
    fixture_pre_learning = b"v18-selftest-pre-build-learning\n"
    fixture_acceptance = b"v18-selftest-accepted-acceptance\n"
    fixture_learning = b"v18-selftest-accepted-build-learning\n"
    old_pre_acceptance_blob = PRE_ACCEPTANCE_BLOB
    old_pre_learning_blob = PRE_LEARNING_BLOB
    old_acceptance_blob = FINAL_ACCEPTANCE_BLOB
    old_learning_blob = FINAL_LEARNING_BLOB
    PRE_ACCEPTANCE_BLOB = blob(fixture_pre_acceptance)
    PRE_LEARNING_BLOB = blob(fixture_pre_learning)
    FINAL_ACCEPTANCE_BLOB = blob(fixture_acceptance)
    FINAL_LEARNING_BLOB = blob(fixture_learning)
    try:
        policy_values = {
            P: b"v18-canonical",
            V17: vb,
            TASKS: pre_tasks,
            ACCEPTANCE: fixture_pre_acceptance,
            LEARNING: fixture_pre_learning,
            S1_015_EVID: evidence,
        }
        accepted_values = dict(policy_values)
        accepted_values.update(
            {
                TASKS: accepted_tasks,
                ACCEPTANCE: fixture_acceptance,
                LEARNING: fixture_learning,
            }
        )
        policy_view = mem(policy_values)
        accepted_view = mem(accepted_values)

        if state(policy_view) != "PRE_S1_016" or state(accepted_view) != "ACCEPTED_S1":
            base.fail("v18 acceptance self-test state classification drifted")
        accept(accepted_view, policy_view)
        delta(accepted_view, policy_view)
        projected = _TaskProjection(accepted_view, reverse_tasks(accepted_tasks))
        if projected.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES) != pre_tasks:
            base.fail("v18 accepted-state task projection drifted")

        partial = dict(policy_values)
        partial[TASKS] = accepted_tasks
        base.expect_failure_matching(
            "v18 partial acceptance delta",
            "delta must be exactly tasks plus acceptance plus Build Learning",
            delta,
            mem(partial),
            policy_view,
        )

        mixed = dict(accepted_values)
        mixed["README.md"] = b"unexpected"
        base.expect_failure_matching(
            "v18 mixed acceptance delta",
            "delta must be exactly tasks plus acceptance plus Build Learning",
            delta,
            mem(mixed),
            policy_view,
        )

        drifted = dict(accepted_values)
        drifted[ACCEPTANCE] = fixture_acceptance + b"drift"
        base.expect_failure_matching(
            "v18 acceptance byte drift",
            "acceptance bytes drifted",
            accept,
            mem(drifted),
            policy_view,
        )

        malformed = dict(accepted_values)
        malformed[TASKS] = b"\xff\xfe\xfd"
        base.expect_failure_matching(
            "v18 malformed accepted ledger",
            "accepted ledger is not UTF-8",
            state,
            mem(malformed),
        )
    finally:
        PRE_ACCEPTANCE_BLOB = old_pre_acceptance_blob
        PRE_LEARNING_BLOB = old_pre_learning_blob
        FINAL_ACCEPTANCE_BLOB = old_acceptance_blob
        FINAL_LEARNING_BLOB = old_learning_blob


def selftest() -> None:
    corrected_v17_selftest()
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v18 workflow drifted: {path}")
    if AUTH != "S1_016_EXACT_ACCEPTANCE_AND_BUILD_LEARNING_ONLY" or S2 != "NOT_AUTHORIZED":
        base.fail("v18 authority boundary drifted")
    if TRUSTED_BASE_V17_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":  # noqa: S105
        base.fail("v18 bootstrap status semantics drifted")

    vb = root.read_bytes(V17, base.MAX_POLICY_FILE_BYTES)
    base_view = {V17: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(base_view)
    candidate.update({P: b"v18", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(base_view))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v18 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(base_view),
    )
    if state(root) == "PRE_S1_016":
        predecessor = root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
        if reverse_tasks(expected_tasks(predecessor)) != predecessor:
            base.fail("v18 task round-trip drifted")
    acceptance_path_selftest()
    print("wepld S1 steady-state routing v18 policy self-tests: PASS")


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
            return int(_call("candidate-local verifier", CAND, args.root, args.policy_base_root, args.policy_base_sha))
        return int(_call("runtime verifier", RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))