#!/usr/bin/env python3
"""Authorize one exact S1-015 repair/evidence ledger closeout; keep S1-016 closed.

v17 is an append-only successor to canonical v16. It preserves every inherited
runtime, source, dependency, provider, S1-013, S1-014, and S1-015 repair
boundary. Its only new steady-state authority is one exact two-file transition
that records the already-proven S1-015 repair and advances the execution ledger
to S1-016 NOT_STARTED.

The transition is fail-closed:
- trusted base must contain frozen canonical v16 and the exact closed S1-014
  ledger/review-evidence state with the canonical S1-015 repair already merged;
- candidate delta must be exactly tasks.md plus s1-015-repair-evidence.md;
- the candidate ledger must equal one deterministic transformation of the exact
  predecessor ledger;
- repair evidence bytes are embedded and content-checked;
- inherited policy verification sees an exact projection of the predecessor
  ledger only after v17 independently proves the closeout bytes;
- S1-016, S1 acceptance, Build Learning mutation, S2, and roadmap mutation
  remain unavailable.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import types
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v17_integrity.py"
V16 = ".github/scripts/wepld_s1_admission_steady_state_routing_v16_integrity.py"
V16_BLOB = "b628905c3adadc71fb68df909116dbf01bcbcbd4"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
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
REPAIR_HEAD = "1229bdd9a411c70cce5494185c1f6c7814fa2085"
REPAIR_MERGE = "9ae784106f36c2234e3cdf6befdb03449a224c34"
BOOT = frozenset({P, FW, AW})
CLOSE = frozenset({TASKS, S1_015_EVID})
AUTH = "S1_015_EXACT_REPAIR_LEDGER_CLOSEOUT_ONLY"
S1_016 = "NOT_AUTHORIZED"
S1_ACCEPTANCE = "NO"
TRUSTED_BASE_V16_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"  # noqa: S105

EVIDENCE_TEXT = """# S1-015 — Bounded repair and rerun evidence

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
EVIDENCE_BYTES = EVIDENCE_TEXT.encode("utf-8")
EVIDENCE_SHA256 = "096583a8230714dfa697ce60e4c83bb391b32a20f6cb2faac2a9ebd7da0bd539"

_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None
_POLICY_BASE_TASKS: bytes | None = None


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

if V16_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v16 workflow identities drifted before v17 import: actual={V16_WF}")
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


def _replace_exact(text: str, old: str, new: str, expected_count: int = 1) -> str:
    count = text.count(old)
    if count != expected_count:
        base.fail(
            "S1-015 closeout predecessor ledger marker drifted: "
            f"marker={old!r} expected_count={expected_count} actual_count={count}"
        )
    return text.replace(old, new)


def expected_tasks(predecessor: bytes) -> bytes:
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("S1-015 closeout requires exact canonical S1-014 ledger predecessor")
    try:
        text = predecessor.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"S1-015 predecessor ledger is not UTF-8: {exc}")

    text = _replace_exact(
        text,
        "CANONICAL_EXECUTION_HEAD = 96fa229610f31598326493b75b40a3353b46bbbf",
        f"CANONICAL_EXECUTION_HEAD = {REPAIR_MERGE}",
        expected_count=2,
    )
    text = _replace_exact(
        text,
        "LEDGER_RECONCILIATION_BASE = 96fa229610f31598326493b75b40a3353b46bbbf",
        f"LEDGER_RECONCILIATION_BASE = {REPAIR_MERGE}",
    )
    text = _replace_exact(text, "NEXT_TASK = S1-015_NOT_STARTED", "NEXT_TASK = S1-016_NOT_STARTED")
    text = text.replace(
        "S1_015_PLUS = NOT_STARTED",
        "S1_015 = CLOSED_CANONICAL_PROVEN\nS1_016 = NOT_STARTED",
        1,
    )

    insertion = f"""
## Canonical S1-015 repair reconciliation checkpoint — 2026-08-27

This checkpoint closes only the bounded repair/rerun task created by the
S1-014 finding reconciliation. The repair bytes were already merged and
post-merge activated before this ledger transition; this checkpoint does not
grant S1-016 or S1 acceptance authority.

```text
S1-015 = CLOSED_CANONICAL_PROVEN
S1-015_FINDING = F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE
S1-015_REPAIR_PR = #197
S1-015_REPAIR_HEAD = {REPAIR_HEAD}
S1-015_REPAIR_MERGE = {REPAIR_MERGE}
S1-015_EXACT_HEAD_FOUNDATION = run 33068200273 / #737 / PASS
S1-015_EXACT_HEAD_TRUSTED_ADMISSION_FINAL = run 33069378037 / #576 / PASS
S1-015_EXACT_HEAD_PERFORMANCE = run 33068200332 / #7 / PASS
S1-015_EXACT_HEAD_QODO = comment 5438445407 / 0_BUGS / 0_RULE_VIOLATIONS / 0_REQUIREMENT_GAPS
S1-015_CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING
S1-015_SECURITY_PASS = NO
S1-015_POST_MERGE_FOUNDATION = run 33069506354 / #738 / PASS
S1-015_POST_MERGE_PERFORMANCE = run 33069506387 / #8 / PASS
S1-015_UNRESOLVED_MATERIAL_FINDINGS = 0
S1-015_STALE_EVIDENCE_INHERITANCE = 0
S1-015_EVIDENCE = {S1_015_EVID}
S1-016 = NOT_STARTED
S1_ACCEPTED = NO
```

The repaired workflow is content-addressed by SHA-256
`6c0b8cb346730a6865a6a2e5b9af2dbccb788c572fa6d36d36860814cabd008e`
and Git blob `3ccd118aea80fd31866973371babc329913aafb8`. No product source,
dependency, runtime, provider/model, or later-slice authority is inferred from
the repair or this closeout.

"""
    marker = "## S1-001 — Establish planning baseline\n"
    text = _replace_exact(text, marker, insertion + marker)

    old_s1_015 = """## S1-015 — Finding reconciliation / bounded repair / rerun

- [ ] Validate each finding against exact current code.
- [ ] Repair only valid findings within bounded scope.
- [ ] Rerun every affected deterministic/dependency/platform/security/review/benchmark gate on the resulting exact head.
- [ ] Zero unresolved material findings.
- [ ] Zero stale-evidence inheritance across changed heads.
"""
    new_s1_015 = f"""## S1-015 — Finding reconciliation / bounded repair / rerun

- [x] Validate each finding against exact current code.
- [x] Repair only valid findings within bounded scope.
- [x] Rerun every affected deterministic/dependency/platform/security/review/benchmark gate on the resulting exact head.
- [x] Zero unresolved material findings.
- [x] Zero stale-evidence inheritance across changed heads.

Evidence: `{S1_015_EVID}` binds the exact repair head, exact one-file repair,
exact-head deterministic/admission/performance/review evidence, merge identity,
and post-merge Foundation/performance activation. Codex Security remains
`NOT_RUN_NON_BLOCKING`; `SECURITY_PASS=NO` is preserved and is not relabeled PASS.
"""
    text = _replace_exact(text, old_s1_015, new_s1_015)

    text = _replace_exact(
        text,
        "COMPLETED = S1-001 THROUGH S1-014",
        "COMPLETED = S1-001 THROUGH S1-015",
    )
    text = _replace_exact(text, "NEXT = S1-015", "NEXT = S1-016")
    text = text.replace(
        "S1_015_PLUS = NOT_STARTED",
        "S1_015 = CLOSED_CANONICAL_PROVEN\nS1_016 = NOT_STARTED",
        1,
    )
    if "S1_015_PLUS = NOT_STARTED" in text:
        base.fail("S1-015 closeout left stale S1_015_PLUS marker")
    return text.encode("utf-8")


def _inherited_tasks_bytes() -> bytes:
    global _POLICY_BASE_TASKS
    if _POLICY_BASE_TASKS is not None:
        if blob(_POLICY_BASE_TASKS) != PRE_TASKS_BLOB:
            base.fail("cached S1-015 policy-base ledger identity drifted")
        return _POLICY_BASE_TASKS

    current = root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    if blob(current) == PRE_TASKS_BLOB:
        _POLICY_BASE_TASKS = current
        return current

    candidate_base = os.environ.get("WEPLD_POLICY_BASE_SHA", "").strip()
    refs = [candidate_base] if candidate_base else []
    refs.append("HEAD^")
    for ref in refs:
        if not ref:
            continue
        try:
            data = subprocess.check_output(
                ["git", "-C", str(root.root), "show", f"{ref}:{TASKS}"],
                stderr=subprocess.STDOUT,
            )
        except (OSError, subprocess.CalledProcessError):
            continue
        if len(data) > base.MAX_POLICY_FILE_BYTES:
            continue
        if blob(data) == PRE_TASKS_BLOB:
            _POLICY_BASE_TASKS = data
            return data

    base.fail("unable to recover exact pre-S1-015-closeout ledger for inherited verification")


class _InheritedProjection:
    def __init__(self, view: Any, inherited_tasks: bytes) -> None:
        self._view = view
        self._tasks = inherited_tasks

    def entries(self) -> list[Any]:
        return [
            entry
            for entry in self._view.entries()
            if entry.path not in {P, S1_015_EVID}
        ]

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path == TASKS:
            if len(self._tasks) > max_bytes:
                base.fail("projected predecessor tasks exceed read bound")
            return self._tasks
        return self._view.read_bytes(path, max_bytes)

    def tree_identity(self, path: str) -> str | None:
        if path == TASKS:
            return blob(self._tasks)
        if path in {P, S1_015_EVID}:
            return None
        return self._view.tree_identity(path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _project_for_v16(view: Any) -> Any:
    paths = ps(view)
    if TASKS not in paths or mode(view, TASKS) != "100644":
        base.fail("v17 requires canonical S1 tasks ledger path/mode")
    actual = view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    actual_blob = blob(actual)

    inherited = _inherited_tasks_bytes()
    if blob(inherited) != PRE_TASKS_BLOB:
        base.fail("v17 inherited ledger projection drifted")

    if actual_blob == PRE_TASKS_BLOB:
        if S1_015_EVID in paths:
            base.fail("pre-closeout ledger must not contain S1-015 repair evidence")
    else:
        if actual != expected_tasks(inherited):
            base.fail("S1-015 closeout ledger bytes are outside deterministic v17 transition")
        if S1_015_EVID not in paths or mode(view, S1_015_EVID) != "100644":
            base.fail("closed S1-015 ledger requires exact repair evidence path/mode")
        evidence = view.read_bytes(S1_015_EVID, base.MAX_POLICY_FILE_BYTES)
        if evidence != EVIDENCE_BYTES or sha(evidence) != EVIDENCE_SHA256:
            base.fail("S1-015 repair evidence bytes drifted")

    return _InheritedProjection(view, inherited)


def patch_predecessor() -> None:
    current = dict(v16.WF)
    if current not in (V16_WF, dict(WF)):
        base.fail(f"v17 predecessor workflow identity map drifted: actual={current}")
    _bind(v16, "WF", dict(WF), "v16 workflow identity projection")


def closeout(candidate: Any, policy_base: Any) -> None:
    for view in (policy_base, candidate):
        if TASKS not in ps(view) or mode(view, TASKS) != "100644":
            base.fail("S1-015 closeout requires canonical tasks path/mode")
        if S1_014_EVID not in ps(view) or mode(view, S1_014_EVID) != "100644":
            base.fail("S1-015 closeout requires canonical S1-014 review evidence")
        if blob(view.read_bytes(S1_014_EVID, base.MAX_POLICY_FILE_BYTES)) != S1_014_EVID_BLOB:
            base.fail("S1-015 closeout inherited S1-014 review evidence drifted")

    predecessor = policy_base.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    if blob(predecessor) != PRE_TASKS_BLOB:
        base.fail("S1-015 closeout trusted ledger drifted")
    if S1_015_EVID in ps(policy_base):
        base.fail("S1-015 closeout trusted base unexpectedly contains repair evidence")
    if S1_015_EVID not in ps(candidate) or mode(candidate, S1_015_EVID) != "100644":
        base.fail("S1-015 closeout candidate repair-evidence state invalid")

    expected = expected_tasks(predecessor)
    actual_tasks = candidate.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    if actual_tasks != expected:
        base.fail("S1-015 reconciled ledger bytes drifted")

    evidence = candidate.read_bytes(S1_015_EVID, base.MAX_POLICY_FILE_BYTES)
    if evidence != EVIDENCE_BYTES or sha(evidence) != EVIDENCE_SHA256:
        base.fail("S1-015 repair evidence bytes drifted")


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
    _call("v16 allowed-path verification", V16_ALLOWED, current - {P}, stage)


def files(view: Any) -> None:
    req_v16(view)
    projected = _project_for_v16(view)
    _call("v16 policy-file verification", V16_FILES, projected)
    if P not in ps(view) or mode(view, P) != "100644":
        base.fail("v17 wrapper path/mode invalid")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V16_PRINT:
        base.fail("v17 predecessor printer drifted")
    _call("v16 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v17=V16_PLUS_EXACT_S1_015_REPAIR_LEDGER_CLOSEOUT")
    print(f"s1_admission_authority_expansion_v17={AUTH}")
    print(f"s1_015_repair_head_v17={REPAIR_HEAD}")
    print(f"s1_015_repair_merge_v17={REPAIR_MERGE}")
    print("s1_015_post_merge_foundation_v17=33069506354_SUCCESS")
    print("s1_015_post_merge_performance_v17=33069506387_SUCCESS")
    print("s1_015_unresolved_material_findings_v17=0")
    print("effective_source_admission_v17=NONE")
    print("effective_dependency_admission_v17=NONE")
    print("new_product_runtime_authority_v17=NONE")
    print("effective_model_provider_execution_v17=NONE")
    print(f"s1_acceptance_v17={S1_ACCEPTANCE}")
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


def _predecessor_modules() -> list[types.ModuleType]:
    seen: set[int] = set()
    stack: list[types.ModuleType] = [v16]
    out: list[types.ModuleType] = []
    while stack:
        module = stack.pop()
        if id(module) in seen:
            continue
        seen.add(id(module))
        out.append(module)
        for value in vars(module).values():
            if (
                isinstance(value, types.ModuleType)
                and value.__name__.startswith("wepld_s1_")
                and value.__name__ != __name__
            ):
                stack.append(value)
    return out


def corrected_v16_selftest() -> None:
    patch_predecessor()
    inherited = _inherited_tasks_bytes()
    projected_roots: list[tuple[types.ModuleType, Any]] = []
    try:
        for module in _predecessor_modules():
            prior_root = getattr(module, "root", None)
            if prior_root is None:
                continue
            projected_roots.append((module, prior_root))
            setattr(module, "root", _InheritedProjection(prior_root, inherited))
        _call("v16 predecessor self-test", getattr(v16, "selftest", None))
    finally:
        for module, prior_root in reversed(projected_roots):
            setattr(module, "root", prior_root)


def selftest() -> None:
    corrected_v16_selftest()
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v17 workflow drifted: {path}")
    if sha(EVIDENCE_BYTES) != EVIDENCE_SHA256:
        base.fail("v17 embedded S1-015 evidence digest drifted")
    if AUTH != "S1_015_EXACT_REPAIR_LEDGER_CLOSEOUT_ONLY":
        base.fail("v17 authority drifted")
    if S1_016 != "NOT_AUTHORIZED" or S1_ACCEPTANCE != "NO":
        base.fail("v17 S1-016/acceptance boundary drifted")
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

    if expected_tasks(_inherited_tasks_bytes()) == _inherited_tasks_bytes():
        base.fail("v17 closeout constructor failed to change canonical ledger")

    canonical_pre = _inherited_tasks_bytes()
    canonical_post = expected_tasks(canonical_pre)
    review = root.read_bytes(S1_014_EVID, base.MAX_POLICY_FILE_BYTES)
    policy_base = {TASKS: canonical_pre, S1_014_EVID: review}
    candidate = {
        TASKS: canonical_post,
        S1_014_EVID: review,
        S1_015_EVID: EVIDENCE_BYTES,
    }
    closeout(mem(candidate), mem(policy_base))
    wrong = dict(candidate)
    wrong[S1_015_EVID] = EVIDENCE_BYTES + b"\n"
    base.expect_failure_matching(
        "v17 wrong repair evidence",
        "repair evidence bytes drifted",
        closeout,
        mem(wrong),
        mem(policy_base),
    )
    widened = dict(candidate)
    widened["README.md"] = b"x"
    base.expect_failure_matching(
        "v17 widened closeout",
        "closeout delta must be exactly",
        delta,
        mem(widened),
        mem(policy_base),
    )
    print("wepld S1 steady-state routing v17 policy self-tests: PASS")


def main(argv: list[str]) -> int:
    global _POLICY_BASE_TASKS
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
            policy_base_path = Path(args.policy_base_root) / TASKS
            data = policy_base_path.read_bytes()
            if len(data) > base.MAX_POLICY_FILE_BYTES or blob(data) != PRE_TASKS_BLOB:
                base.fail("verify-candidate-local policy-base ledger identity drifted")
            _POLICY_BASE_TASKS = data
            return int(
                _call(
                    "candidate-local verifier",
                    CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", RUNTIME, argv))
    except (base.PolicyError, OSError) as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
