#!/usr/bin/env python3
"""Authorize one exact S1-015 repair/ledger closeout; keep S1-016 closed.

v17 is an append-only successor to canonical v16. It preserves every inherited
source, dependency, runtime, provider, model, S1-014, and S1-015 repair boundary.
Its only new steady-state authority is one exact two-file S1-015 closeout after
v17 is canonically activated:

- specs/001-desktop-rust-trusted-core-handshake/tasks.md
- specs/001-desktop-rust-trusted-core-handshake/s1-015-repair-evidence.md

The closeout binds the exact repaired workflow and exact PR/run/review evidence,
performs a deterministic ledger transformation from the frozen pre-closeout
tasks blob, and projects that ledger back to its predecessor only for inherited
policy-file verification. It grants no S1 acceptance or S1-016 authority.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v17_integrity.py"
V16 = ".github/scripts/wepld_s1_admission_steady_state_routing_v16_integrity.py"
V16_BLOB = "b628905c3adadc71fb68df909116dbf01bcbcbd4"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
PW = ".github/workflows/s1-performance.yml"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"
S1_014_EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-014-review-evidence.md"
S1_015_EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-015-repair-evidence.md"

OLD_WF = {
    FW: "42617be8a808aad53fbd7c157690ef05c6af11befd7ef5a78df5059378d3459b",
    AW: "cdecf78c21462ee45d1cbe889fe816354e327da9894cca1d2b387f6e40aa8a3b",
}
WF = {
    FW: "4082d9037db9123924dce5181124d2b86cb5e4ac8836bad4f6cb90f29af9d17d",
    AW: "201ac44a5597e5f099eab178301f30cf058976b37d48d5bed4a66645dbafe276",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

PRE_TASKS_BLOB = "d85892c252be0b3731b88bd97fae6af40d3776db"
S1_014_EVID_BLOB = "4fd85d2a1f829a63b840020c0e434aeb12f20328"
PW_REPAIRED_BLOB = "3ccd118aea80fd31866973371babc329913aafb8"

BOOT = frozenset({P, FW, AW})
CLOSE = frozenset({TASKS, S1_015_EVID})
AUTH = "S1_015_EXACT_REPAIR_LEDGER_CLOSEOUT_ONLY"
FINDING = "F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE"
S1_016 = "NOT_AUTHORIZED"
TRUSTED_BASE_V16_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"  # noqa: S105

EXPECTED_EVIDENCE_TEXT = r"""# S1-015 — Bounded repair and rerun evidence

```text
STATUS = S1_015_CLOSEOUT_EVIDENCE
DATE = 2026-08-27
FINDING = F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE

S1_014_ACCEPTANCE_CANDIDATE = 58ad0d166b6177ae69d04ff59da17aa8cc0e3c28
REPAIR_BASE = fd5afdbd6cc034a1623feb2e2c94b34468cab06c
REPAIR_PR = #197
REPAIR_HEAD = 1229bdd9a411c70cce5494185c1f6c7814fa2085
REPAIR_HEAD_TREE = 063a5bef4d053636efd486cb5f5d50ac886b984b
REPAIR_CHANGED_FILES = 1_EXACT
REPAIR_PATH = .github/workflows/s1-performance.yml
REPAIR_MERGE = 9ae784106f36c2234e3cdf6befdb03449a224c34
REPAIR_MERGE_TREE = 063a5bef4d053636efd486cb5f5d50ac886b984b

PRE_REPAIR_WORKFLOW_SHA256 = 7dd7f670740b651e30700a0fe10b4f1dcd8d51a46b257789e54a02c74df98784
PRE_REPAIR_WORKFLOW_GIT_BLOB = b16d57b42e617808d4b5d2547c1677e9ef7c3535
REPAIRED_WORKFLOW_SHA256 = 6c0b8cb346730a6865a6a2e5b9af2dbccb788c572fa6d36d36860814cabd008e
REPAIRED_WORKFLOW_GIT_BLOB = 3ccd118aea80fd31866973371babc329913aafb8

EXACT_HEAD_FOUNDATION = 33068200273 / #737 / SUCCESS
EXACT_HEAD_TRUSTED_ADMISSION_INITIAL = 33068200340 / #575 / SUCCESS
EXACT_HEAD_TRUSTED_ADMISSION_FINAL = 33069378037 / #576 / SUCCESS
EXACT_HEAD_PERFORMANCE = 33068200332 / #7 / SUCCESS
EXACT_HEAD_QODO_REVIEW = issuecomment-5438445407 / 0_BUGS / 0_RULE_VIOLATIONS / 0_REQUIREMENT_GAPS
CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
SECURITY_PASS = NO
CODERABBIT = NOT_COUNTED_AS_REVIEW

POST_MERGE_FOUNDATION = 33069506354 / #738 / SUCCESS
POST_MERGE_PERFORMANCE = 33069506387 / #8 / SUCCESS
POST_MERGE_HEAD = 9ae784106f36c2234e3cdf6befdb03449a224c34

UNRESOLVED_MATERIAL_FINDINGS = 0
STALE_EVIDENCE_INHERITANCE = 0
S1_015_CLOSEOUT_AUTHORITY = REQUIRES_CANONICAL_V17_SUCCESSOR_POLICY
S1_016_AUTHORITY = NOT_GRANTED_BY_THIS_EVIDENCE
S1_ACCEPTED = NO
```

## Finding reconciliation

S1-014 normalized one valid material finding: the `s1-performance` workflow
path filters did not cover every measured build input. PR #197 changed only
`.github/workflows/s1-performance.yml`, adding the missing measured build-input
paths to both pull-request and push trigger filters. No product source,
dependency, runtime, model/provider, or later-slice authority was added.

## Exact-head qualification

The exact repair head `1229bdd9a411c70cce5494185c1f6c7814fa2085`
passed Foundation, trusted-base admission, and the S1 performance workflow. The
final trusted-base admission rerun also passed on the same exact head. Qodo
reviewed that exact head and reported zero bugs, zero rule violations, and zero
requirement gaps. CodeRabbit did not provide counted review evidence. Codex
Security remained unavailable for this bounded repair and is recorded as
`NOT_RUN_NON_BLOCKING`, never PASS.

## Canonical activation

PR #197 merged as `9ae784106f36c2234e3cdf6befdb03449a224c34`.
On that exact canonical merge commit, post-merge Foundation #738 and
`s1-performance` #8 both succeeded. The post-merge performance run is the
activation proof that the repaired path filters trigger and execute on the
canonical measured build-input tree.

## Closeout boundary

This evidence counts as S1-015 closeout evidence only after the exact
two-file ledger/evidence transition is admitted and merged under the separately
qualified v17 successor policy. It does not authorize S1-016, S1 acceptance,
Build Learning mutation, S2, roadmap mutation, provider/model execution, source
admission, dependency expansion, or product-runtime expansion.
"""

TOP_PRE = r"""```text
SLICE = S1
S1_ORIGINAL_BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
CANONICAL_EXECUTION_HEAD = 96fa229610f31598326493b75b40a3353b46bbbf
LEDGER_RECONCILIATION_BASE = 96fa229610f31598326493b75b40a3353b46bbbf
LIVE_MAIN = MUST_BE_READ_FROM_GITHUB
ACTIVE_TASK = NONE
NEXT_TASK = S1-015_NOT_STARTED
FOUNDER_STANDING_AUTHORIZATION = GRANTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN
S1_014_REVIEW_RECONCILIATION = PROVEN_BY_THIS_CANONICAL_LEDGER
S1_015_PLUS = NOT_STARTED
```"""
TOP_POST = r"""```text
SLICE = S1
S1_ORIGINAL_BASE_MAIN = 6eff72319cad99c878a80f0d5bce9f107d213679
CANONICAL_EXECUTION_HEAD = 9ae784106f36c2234e3cdf6befdb03449a224c34
LEDGER_RECONCILIATION_BASE = 9ae784106f36c2234e3cdf6befdb03449a224c34
LIVE_MAIN = MUST_BE_READ_FROM_GITHUB
ACTIVE_TASK = NONE
NEXT_TASK = S1-016_NOT_STARTED
FOUNDER_STANDING_AUTHORIZATION = GRANTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN
S1_014_REVIEW_RECONCILIATION = PROVEN_BY_THIS_CANONICAL_LEDGER
S1_015 = CLOSED_CANONICAL_PROVEN
S1_016 = NOT_STARTED
```"""
S1_015_PRE = r"""## S1-015 — Finding reconciliation / bounded repair / rerun

- [ ] Validate each finding against exact current code.
- [ ] Repair only valid findings within bounded scope.
- [ ] Rerun every affected deterministic/dependency/platform/security/review/benchmark gate on the resulting exact head.
- [ ] Zero unresolved material findings.
- [ ] Zero stale-evidence inheritance across changed heads.
"""
S1_015_POST = r"""## S1-015 — Finding reconciliation / bounded repair / rerun

- [x] Validate each finding against exact current code.
- [x] Repair only valid findings within bounded scope.
- [x] Rerun every affected deterministic/dependency/platform/security/review/benchmark gate on the resulting exact head.
- [x] Zero unresolved material findings.
- [x] Zero stale-evidence inheritance across changed heads.

Evidence: PR #197 repaired exactly `F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE` at head `1229bdd9a411c70cce5494185c1f6c7814fa2085` and merged as `9ae784106f36c2234e3cdf6befdb03449a224c34`. Exact-head Foundation #737, authoritative admission #576, performance #7, and Qodo review comment `5438445407` were clean for the repair; post-merge Foundation #738 and performance #8 passed on the canonical merge. Durable closeout evidence is `s1-015-repair-evidence.md`.
"""
GATE_PRE = r"""```text
COMPLETED = S1-001 THROUGH S1-014
CURRENT = NONE
CANONICAL_EXECUTION_HEAD = 96fa229610f31598326493b75b40a3353b46bbbf
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN
S1_014_REVIEW_RECONCILIATION = PROVEN
NEXT = S1-015
S1_015_PLUS = NOT_STARTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
```"""
GATE_POST = r"""```text
COMPLETED = S1-001 THROUGH S1-015
CURRENT = NONE
CANONICAL_EXECUTION_HEAD = 9ae784106f36c2234e3cdf6befdb03449a224c34
S1_012_CANONICAL_ACTIVATION = PROVEN
S1_013_CANONICAL_MEASUREMENT = PROVEN
S1_013_EVIDENCE_RECONCILIATION = PROVEN
S1_014_REVIEW_RECONCILIATION = PROVEN
S1_015_REPAIR_CLOSEOUT = PROVEN
NEXT = S1-016
S1_016 = NOT_STARTED
SOURCE_ACQUISITION_CHECK = PASS
RUNTIME_DEPENDENCY_ADMISSION = EXACT_S1_GRAPH
IMPLEMENTATION = CANONICAL_THROUGH_S1_011
```"""
S1_014_ANCHOR = r"""The review-only PR intentionally used the original S1 base solely to expose the complete 427-commit / 286-file range to hosted review and was closed without merge. Its synthetic-base Foundation failure is not acceptance evidence. The exact candidate remains the canonical `main` commit above, whose Foundation #723 passed. Findings were validated against that exact candidate: one performance-workflow trigger-coverage defect is material and requires bounded S1-015 repair; two machine-readable-report rule findings are non-material external policy rules with canonical rejection precedent; and the alleged missing-v13 admission script is a synthetic-review-base false positive contradicted by genuine trusted-base admission runs #561 and #562.

"""
S1_015_CHECKPOINT = r"""## Canonical S1-015 repair reconciliation checkpoint — 2026-08-27

This checkpoint closes only the bounded repair/reconciliation task after the exact repair was qualified, reviewed, merged, and exercised by the canonical post-merge performance workflow.

```text
S1-015 = CLOSED_CANONICAL_PROVEN
S1-015_FINDING = F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE
S1-015_REPAIR_PR = #197
S1-015_REPAIR_HEAD = 1229bdd9a411c70cce5494185c1f6c7814fa2085
S1-015_REPAIR_MERGE = 9ae784106f36c2234e3cdf6befdb03449a224c34
S1-015_REPAIRED_WORKFLOW_BLOB = 3ccd118aea80fd31866973371babc329913aafb8
S1-015_EXACT_HEAD_FOUNDATION = run 33068200273 / #737 / PASS
S1-015_EXACT_HEAD_ADMISSION = run 33069378037 / #576 / PASS
S1-015_EXACT_HEAD_PERFORMANCE = run 33068200332 / #7 / PASS
S1-015_QODO_REVIEW = comment 5438445407 / 0_BUGS / 0_RULE_VIOLATIONS / 0_REQUIREMENT_GAPS
S1-015_POST_MERGE_FOUNDATION = run 33069506354 / #738 / PASS
S1-015_POST_MERGE_PERFORMANCE = run 33069506387 / #8 / PASS
S1-015_UNRESOLVED_MATERIAL_FINDINGS = 0
S1-015_EVIDENCE = specs/001-desktop-rust-trusted-core-handshake/s1-015-repair-evidence.md
S1-014_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
S1-014_SECURITY_PASS = NO
S1_ACCEPTED = NO
S1-016 = NOT_STARTED
```

The Codex Security coverage limitation remains explicit and is not converted into PASS. S1-015 closeout also does not accept S1; S1-016 remains the separate acceptance and Build Learning task.

"""

_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None


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
        base.fail(f"v17 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v17 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v17 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v17 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
actual_v16 = blob(root.read_bytes(V16, base.MAX_POLICY_FILE_BYTES))
if actual_v16 != V16_BLOB:
    base.fail(f"frozen v16 predecessor drifted: expected={V16_BLOB} actual={actual_v16}")

import wepld_s1_admission_steady_state_routing_v16_integrity as v16  # noqa: E402

V16_DELTA = v16.delta
V16_BASE = v16.basectrl
V16_ALLOWED = v16.allowed
V16_FILES = v16.files
V16_DEXT = v16.dext
V16_EEXT = v16.eext
V16_EXT = v16.ext
V16_PRINT = v16.printer
V16_WF = dict(v16.WF)
CAND = v16.CAND
RUNTIME = v16.RUNTIME

v15 = _attr(v16, "v15", "v16 v15 predecessor module")
v14 = _attr(v15, "v14", "v15 v14 predecessor module")
V14_CLOSE_TASKS = _attr(v14, "CLOSE_TASKS", "v14 S1-014 closeout ledger identity")

if V16_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v16 workflow identities drifted before v17 import: actual={V16_WF}")
if V14_CLOSE_TASKS != PRE_TASKS_BLOB:
    base.fail(
        "v14 canonical S1-014 ledger identity drifted before v17 import: "
        f"expected={PRE_TASKS_BLOB} actual={V14_CLOSE_TASKS}"
    )
if _attr(v16, "AUTH", "v16 authority marker") != (
    "S1_015_PERFORMANCE_POLICY_FILE_IDENTITY_PROJECTION_REPAIR_ONLY"
):
    base.fail("v17 observed v16 authority drift")
if _attr(v16, "S1_016", "v16 S1-016 boundary") != "NOT_AUTHORIZED":
    base.fail("v17 observed v16 S1-016 boundary drift")


def req_v16(view: Any) -> None:
    if V16 not in ps(view):
        base.fail("v17 candidate/base is missing frozen v16 predecessor")
    actual = blob(view.read_bytes(V16, base.MAX_POLICY_FILE_BYTES))
    if actual != V16_BLOB:
        base.fail(f"frozen v16 predecessor drifted: expected={V16_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v16, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v17 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v17 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v16, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v17 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        base.fail(f"S1-015 closeout {label} occurrence drifted: expected=1 actual={count}")
    return text.replace(old, new, 1)


def expected_tasks(predecessor: bytes) -> bytes:
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("S1-015 closeout predecessor ledger identity drifted")
    try:
        text = predecessor.decode("utf-8")
    except UnicodeDecodeError as exc:
        base.fail(f"S1-015 closeout predecessor ledger is not UTF-8: {exc}")

    text = _replace_once(text, TOP_PRE, TOP_POST, "top checkpoint")
    text = _replace_once(
        text,
        S1_014_ANCHOR,
        S1_014_ANCHOR + S1_015_CHECKPOINT,
        "S1-015 reconciliation checkpoint",
    )
    text = _replace_once(text, S1_015_PRE, S1_015_POST, "S1-015 checklist")
    text = _replace_once(text, GATE_PRE, GATE_POST, "current gate")
    return text.encode("utf-8")


def reverse_tasks(closed: bytes) -> bytes:
    try:
        text = closed.decode("utf-8")
    except UnicodeDecodeError as exc:
        base.fail(f"S1-015 closed ledger is not UTF-8: {exc}")

    text = _replace_once(text, TOP_POST, TOP_PRE, "reverse top checkpoint")
    text = _replace_once(
        text,
        S1_014_ANCHOR + S1_015_CHECKPOINT,
        S1_014_ANCHOR,
        "reverse S1-015 reconciliation checkpoint",
    )
    text = _replace_once(text, S1_015_POST, S1_015_PRE, "reverse S1-015 checklist")
    text = _replace_once(text, GATE_POST, GATE_PRE, "reverse current gate")
    predecessor = text.encode("utf-8")
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("S1-015 closed ledger does not reverse to exact canonical predecessor")
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


def _verify_inherited_closeout_inputs(view: Any) -> None:
    paths = ps(view)
    for path in (TASKS, S1_014_EVID, PW):
        if path not in paths or mode(view, path) != "100644":
            base.fail(f"S1-015 closeout requires canonical path/mode: {path}")
    if blob(view.read_bytes(S1_014_EVID, base.MAX_POLICY_FILE_BYTES)) != S1_014_EVID_BLOB:
        base.fail("S1-015 closeout inherited S1-014 review evidence drifted")
    if blob(view.read_bytes(PW, base.MAX_POLICY_FILE_BYTES)) != PW_REPAIRED_BLOB:
        base.fail("S1-015 closeout requires exact repaired performance workflow")


def ledger_state(view: Any) -> str:
    _verify_inherited_closeout_inputs(view)
    tasks = view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    if blob(tasks) == PRE_TASKS_BLOB:
        if S1_015_EVID in ps(view):
            base.fail("pre-S1-015-closeout ledger must not contain S1-015 evidence")
        return "PRE_S1_015_CLOSEOUT"

    predecessor = reverse_tasks(tasks)
    if S1_015_EVID not in ps(view) or mode(view, S1_015_EVID) != "100644":
        base.fail("closed S1-015 ledger requires exact S1-015 evidence")
    evidence = view.read_bytes(S1_015_EVID, base.MAX_POLICY_FILE_BYTES)
    if evidence != EXPECTED_EVIDENCE_TEXT.encode("utf-8"):
        base.fail("S1-015 repair evidence bytes drifted")
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("S1-015 predecessor projection identity drifted")
    return "CLOSED_S1_015"


def closeout(candidate: Any, policy_base: Any) -> None:
    _verify_inherited_closeout_inputs(policy_base)
    _verify_inherited_closeout_inputs(candidate)
    if blob(policy_base.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != PRE_TASKS_BLOB:
        base.fail("S1-015 closeout trusted ledger drifted")
    if S1_015_EVID in ps(policy_base) or S1_015_EVID not in ps(candidate):
        base.fail("S1-015 closeout evidence state invalid")
    if mode(candidate, S1_015_EVID) != "100644":
        base.fail("S1-015 closeout evidence mode invalid")

    predecessor = policy_base.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    expected = expected_tasks(predecessor)
    actual = candidate.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    if actual != expected:
        base.fail("S1-015 reconciled ledger bytes drifted")
    if candidate.read_bytes(S1_015_EVID, base.MAX_POLICY_FILE_BYTES) != EXPECTED_EVIDENCE_TEXT.encode("utf-8"):
        base.fail("S1-015 repair evidence bytes drifted")
    if ledger_state(candidate) != "CLOSED_S1_015":
        base.fail("S1-015 closeout state did not close")


def patch_predecessor() -> None:
    current = dict(v16.WF)
    if current not in (V16_WF, dict(WF)):
        base.fail(f"v17 predecessor workflow identity map drifted: actual={current}")
    _bind(v16, "WF", dict(WF), "v16 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v16(candidate)
            req_v16(policy_base)
            return
        if paths & BOOT:
            base.fail("v17 bootstrap delta must be exactly policy plus two workflows")
    elif P in paths:
        base.fail("canonical v17 wrapper is frozen after activation")

    if paths == CLOSE:
        closeout(candidate, policy_base)
        return
    if paths & CLOSE:
        base.fail("S1-015 closeout delta must be exactly tasks plus repair evidence")
    _call("v16 exact-delta verifier", V16_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v16 base-control verifier", V16_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v17 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v17 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v17 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v17 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v16 extension verification", V16_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    current = set(paths)
    if current == set(CLOSE):
        return
    remaining = current - {P}
    if remaining:
        _call("v16 allowed-path verification", V16_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v16(view)
    state = ledger_state(view)
    if state == "PRE_S1_015_CLOSEOUT":
        _call("v16 policy-file verification", V16_FILES, view)
    elif state == "CLOSED_S1_015":
        predecessor = reverse_tasks(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES))
        _call("v16 policy-file verification", V16_FILES, _TaskProjection(view, predecessor))
    else:
        base.fail(f"unknown S1-015 ledger state: {state}")
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v17 wrapper mode invalid")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V16_PRINT:
        base.fail("v17 predecessor printer drifted")
    _call("v16 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v17=V16_PLUS_EXACT_S1_015_CLOSEOUT")
    print(f"s1_admission_authority_expansion_v17={AUTH}")
    print(f"s1_015_validated_finding_v17={FINDING}")
    print("s1_015_repair_merge_v17=9ae784106f36c2234e3cdf6befdb03449a224c34")
    print("s1_015_post_merge_foundation_v17=33069506354_SUCCESS")
    print("s1_015_post_merge_performance_v17=33069506387_SUCCESS")
    print("effective_source_admission_v17=NONE")
    print("effective_dependency_admission_v17=NONE")
    print("new_product_runtime_authority_v17=NONE")
    print("effective_model_provider_execution_v17=NONE")
    print("roadmap_mutation_authority_v17=NONE")
    print("s1_acceptance_v17=NO")
    print(f"s1_016_authority_v17={S1_016}")


def overlay() -> None:
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop extension hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution extension hook"), eext),
        (_attr(shell, "validate_allowed_paths", "shell allowed-path hook"), allowed),
        (_attr(shell, "verify_policy_files", "shell policy-file hook"), files),
        (_attr(shell, "print_success", "shell success hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v17 installed overlay drifted")
    if dict(v16.WF) != dict(WF):
        base.fail("v17 workflow identity projection drifted")
    if _PRINT is not V16_PRINT:
        base.fail("v17 predecessor printer identity drifted")
    if _EXPECTED_DESKTOP_EXTENSIONS is None or _EXPECTED_EXECUTION_EXTENSIONS is None:
        base.fail("v17 extension registration unavailable")
    if extset(desktop) != _EXPECTED_DESKTOP_EXTENSIONS:
        base.fail("v17 desktop extension registration drifted")
    if extset(execution) != _EXPECTED_EXECUTION_EXTENSIONS:
        base.fail("v17 execution extension registration drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v16 install", getattr(v16, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor exact-delta hook"), V16_DELTA),
        (base.compare_base_controlled, V16_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop extension hook"), V16_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution extension hook"), V16_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed-path hook"), V16_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor policy-file hook"), V16_FILES),
        (_attr(shell, "print_success", "predecessor success hook"), V16_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v17 predecessor hook drifted")
    _PRINT = V16_PRINT
    _EXPECTED_DESKTOP_EXTENSIONS = frozenset(set(extset(desktop)) | {P})
    _EXPECTED_EXECUTION_EXTENSIONS = frozenset(set(extset(execution)) | {P})
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_DESKTOP_EXTENSIONS, "desktop extension registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_EXECUTION_EXTENSIONS, "execution extension registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "routing exact-delta binding")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "desktop extension hook binding")
    _bind(execution, "verify_extension_controlled_paths", eext, "execution extension hook binding")
    _bind(shell, "validate_allowed_paths", allowed, "shell allowed-path binding")
    _bind(shell, "verify_policy_files", files, "shell policy-file binding")
    _bind(shell, "print_success", printer, "shell success binding")
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def _with_v14_close_tasks(tasks_blob: str, fn: Any) -> Any:
    prior = _attr(v14, "CLOSE_TASKS", "v14 closeout ledger identity")
    _bind(v14, "CLOSE_TASKS", tasks_blob, "v14 closeout ledger compatibility projection")
    try:
        return fn()
    finally:
        _bind(v14, "CLOSE_TASKS", prior, "v14 closeout ledger compatibility restoration")


def corrected_v16_selftest() -> None:
    tasks = root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    current_blob = blob(tasks)
    if current_blob == PRE_TASKS_BLOB:
        _call("v16 predecessor self-test", getattr(v16, "selftest", None))
        return

    predecessor = reverse_tasks(tasks)
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("v17 could not establish closed-ledger predecessor for v16 self-test")
    _with_v14_close_tasks(current_blob, lambda: _call("v16 predecessor self-test", getattr(v16, "selftest", None)))


def selftest() -> None:
    corrected_v16_selftest()
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v17 workflow drifted: {path}")
    if AUTH != "S1_015_EXACT_REPAIR_LEDGER_CLOSEOUT_ONLY":
        base.fail("v17 authority drifted")
    if S1_016 != "NOT_AUTHORIZED":
        base.fail("v17 S1-016 boundary drifted")
    if TRUSTED_BASE_V16_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":  # noqa: S105
        base.fail("v17 bootstrap status semantics drifted")

    vb = root.read_bytes(V16, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V16: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v17", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v17 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    predecessor = root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    if blob(predecessor) == PRE_TASKS_BLOB:
        closed = expected_tasks(predecessor)
        if reverse_tasks(closed) != predecessor:
            base.fail("v17 task closeout round-trip drifted")

    print("wepld S1 steady-state routing v17 policy self-tests: PASS")


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
