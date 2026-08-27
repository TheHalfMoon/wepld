#!/usr/bin/env python3
"""Authorize one exact S1-014 review/ledger closeout; keep S1-015 repair closed.

v14 is an append-only successor to canonical v13. It preserves all inherited
runtime, source, dependency, provider, and S1-013 authority. Its only new
steady-state authority is one content-addressed S1-014 review evidence/ledger
transition after v14 is canonically activated.

The transition is fail-closed:
- trusted base must contain the exact canonical S1-013 ledger/evidence state;
- candidate delta must be exactly tasks.md plus s1-014-review-evidence.md;
- both candidate blobs and Markdown modes are pinned;
- frozen Harness compatibility remains active and is extended only to recognize
  the exact post-S1-014 ledger state;
- S1-015 repair authority remains unavailable.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any, Callable

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v14_integrity.py"
V13 = ".github/scripts/wepld_s1_admission_steady_state_routing_v13_integrity.py"
V13_BLOB = "370bbebfe38719b3be91bbe9147729916fbb3f85"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"
S1_013_EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-013-performance-evidence.md"
S1_014_EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-014-review-evidence.md"

OLD_WF = {
    FW: "d3bd0c52afefa27672a2016d0596a3c2a08f26ef08ab5f9e7bf8cdbeb3e518be",
    AW: "b2e5aed34aa4c3f7be6056ec36376749b1c3c0851259d9f6c2ff948c5b020aa8",
}
WF = {
    FW: "81cca9767055dbbf90e76a4a77191ebe068fd8e3b0902005a20821cc550b71f6",
    AW: "cd61b3cd17c7834bd83cb55b5dfe8bfdf66da6060a6bedc574fb5f50429349e8",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
PRE_TASKS = "f8d9d09dc2e02861246614f374173a0a2bfff9c2"
CLOSE_TASKS = "d85892c252be0b3731b88bd97fae6af40d3776db"
S1_013_EVID_BLOB = "bd79c1e64b397fda3677fb549e9a7feb0c5a8c3d"
S1_014_EVID_BLOB = "4fd85d2a1f829a63b840020c0e434aeb12f20328"
REVIEWED_HEAD = "58ad0d166b6177ae69d04ff59da17aa8cc0e3c28"
REVIEW_PR = "191"
REVIEW_COMMENT = "5434723966"
BOOT = frozenset({P, FW, AW})
CLOSE = frozenset({TASKS, S1_014_EVID})
AUTH = "S1_014_EXACT_REVIEW_LEDGER_CLOSEOUT_ONLY"
S1_015 = "NOT_AUTHORIZED"
TRUSTED_BASE_V13_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"  # noqa: S105

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
        base.fail(f"v14 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v14 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v14 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v14 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
actual_v13 = blob(root.read_bytes(V13, base.MAX_POLICY_FILE_BYTES))
if actual_v13 != V13_BLOB:
    base.fail(f"frozen v13 predecessor drifted: expected={V13_BLOB} actual={actual_v13}")

import wepld_s1_admission_steady_state_routing_v13_integrity as v13  # noqa: E402

V13_DELTA = v13.delta
V13_BASE = v13.basectrl
V13_ALLOWED = v13.allowed
V13_FILES = v13.files
V13_DEXT = v13.dext
V13_EEXT = v13.eext
V13_EXT = v13.ext
V13_PRINT = v13.printer
V13_WF = dict(v13.WF)
CAND = v13.CAND
RUNTIME = v13.RUNTIME

v12 = _attr(v13, "v12", "v13 v12 predecessor module")
v11 = _attr(v12, "v11", "v12 v11 predecessor module")
v10 = _attr(v11, "v10", "v11 v10 predecessor module")
V11_LEDGER = _attr(v11, "_ledger_state", "v11 ledger-state verifier")
V10_CLOSE_TASKS = _attr(v10, "CLOSE_TASKS", "v10 closeout ledger identity")

if V13_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v13 workflow identities drifted before v14 import: actual={V13_WF}")
if V10_CLOSE_TASKS != PRE_TASKS:
    base.fail(
        "v10 canonical closeout ledger identity drifted before v14 import: "
        f"expected={PRE_TASKS} actual={V10_CLOSE_TASKS}"
    )


def req_v13(view: Any) -> None:
    if V13 not in ps(view):
        base.fail("v14 candidate/base is missing frozen v13 predecessor")
    actual = blob(view.read_bytes(V13, base.MAX_POLICY_FILE_BYTES))
    if actual != V13_BLOB:
        base.fail(f"frozen v13 predecessor drifted: expected={V13_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v13, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v14 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v14 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v13, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v14 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def review_state(view: Any, hasher: Callable[[bytes], str] = blob) -> str:
    paths = ps(view)
    if TASKS not in paths or S1_013_EVID not in paths:
        base.fail("S1-014 review state requires canonical S1-013 ledger/evidence")
    if mode(view, TASKS) != "100644" or mode(view, S1_013_EVID) != "100644":
        base.fail("S1-014 inherited ledger/evidence mode invalid")
    if hasher(view.read_bytes(S1_013_EVID, base.MAX_POLICY_FILE_BYTES)) != S1_013_EVID_BLOB:
        base.fail("S1-013 inherited evidence identity drifted")

    tasks = hasher(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES))
    if tasks == PRE_TASKS:
        if S1_014_EVID in paths:
            base.fail("pre-S1-014 ledger must not contain S1-014 review evidence")
        return "PRE_S1_014"
    if tasks == CLOSE_TASKS:
        if S1_014_EVID not in paths:
            base.fail("closed S1-014 ledger requires exact review evidence")
        if mode(view, S1_014_EVID) != "100644":
            base.fail("S1-014 review evidence mode invalid")
        actual = hasher(view.read_bytes(S1_014_EVID, base.MAX_POLICY_FILE_BYTES))
        if actual != S1_014_EVID_BLOB:
            base.fail(
                "S1-014 review evidence identity drifted: "
                f"expected={S1_014_EVID_BLOB} actual={actual}"
            )
        return "CLOSED_S1_014"
    base.fail(f"S1-014 review state rejects unknown S1 ledger: actual={tasks}")


def ledger_state(view: Any, hasher: Callable[[bytes], str]) -> str:
    if TASKS not in ps(view):
        return _call("v11 ledger-state verifier", V11_LEDGER, view, hasher)
    actual = hasher(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES))
    if actual != CLOSE_TASKS:
        return _call("v11 ledger-state verifier", V11_LEDGER, view, hasher)
    if review_state(view, hasher) != "CLOSED_S1_014":
        base.fail("S1-014 extended Harness ledger state drifted")
    return CLOSE_TASKS


def patch_predecessor() -> None:
    current = dict(v13.WF)
    if current not in (V13_WF, dict(WF)):
        base.fail(f"v14 predecessor workflow identity map drifted: actual={current}")
    _bind(v13, "WF", dict(WF), "v13 workflow identity projection")
    current_ledger = _attr(v11, "_ledger_state", "v11 ledger-state verifier")
    if current_ledger not in (V11_LEDGER, ledger_state):
        base.fail("v14 predecessor ledger compatibility hook drifted")
    _bind(v11, "_ledger_state", ledger_state, "v11 ledger-state extension")


def closeout(
    candidate: Any,
    policy_base: Any,
    pre: str = PRE_TASKS,
    post: str = CLOSE_TASKS,
    inherited_evidence: str = S1_013_EVID_BLOB,
    review_evidence: str = S1_014_EVID_BLOB,
) -> None:
    if blob(policy_base.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != pre:
        base.fail("S1-014 closeout trusted ledger drifted")
    if S1_014_EVID in ps(policy_base) or S1_014_EVID not in ps(candidate):
        base.fail("S1-014 closeout review-evidence state invalid")
    for view in (policy_base, candidate):
        if mode(view, TASKS) != "100644" or mode(view, S1_013_EVID) != "100644":
            base.fail("S1-014 closeout inherited Markdown mode invalid")
        if blob(view.read_bytes(S1_013_EVID, base.MAX_POLICY_FILE_BYTES)) != inherited_evidence:
            base.fail("S1-014 closeout inherited S1-013 evidence drifted")
    if mode(candidate, S1_014_EVID) != "100644":
        base.fail("S1-014 closeout review evidence mode invalid")
    if blob(candidate.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != post:
        base.fail("S1-014 reconciled ledger identity drifted")
    if blob(candidate.read_bytes(S1_014_EVID, base.MAX_POLICY_FILE_BYTES)) != review_evidence:
        base.fail("S1-014 review evidence identity drifted")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v13(candidate)
            req_v13(policy_base)
            return
        if paths & BOOT:
            base.fail("v14 bootstrap delta must be exactly policy plus two workflows")
    if paths == CLOSE:
        closeout(candidate, policy_base)
        return
    if paths & CLOSE:
        base.fail("S1-014 closeout delta must be exactly tasks plus review evidence")
    _call("v13 exact-delta verifier", V13_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v13 base-control verifier", V13_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v14 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v14 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v14 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v14 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v13 extension verification", V13_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    current = set(paths)
    if current == set(CLOSE):
        return
    _call("v13 allowed-path verification", V13_ALLOWED, current - {P}, stage)


def _call_v13_files_with_ledger(view: Any, expected: str) -> None:
    prior = _attr(v10, "CLOSE_TASKS", "v10 closeout ledger identity")
    if prior != V10_CLOSE_TASKS:
        base.fail(
            "v10 closeout ledger identity drifted before projection: "
            f"expected={V10_CLOSE_TASKS} actual={prior}"
        )
    _bind(v10, "CLOSE_TASKS", expected, "v10 S1 ledger projection")
    try:
        _call("v13 policy-file verification", V13_FILES, view)
    finally:
        _bind(v10, "CLOSE_TASKS", prior, "v10 S1 ledger restoration")


def files(view: Any) -> None:
    req_v13(view)
    state = review_state(view)
    if state == "PRE_S1_014":
        _call("v13 policy-file verification", V13_FILES, view)
    elif state == "CLOSED_S1_014":
        _call_v13_files_with_ledger(view, CLOSE_TASKS)
    else:
        base.fail(f"unknown S1-014 review state: {state}")
    if P not in ps(view):
        base.fail("v14 wrapper missing")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V13_PRINT:
        base.fail("v14 predecessor printer drifted")
    _call("v13 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v14=V13_PLUS_EXACT_S1_014_REVIEW_CLOSEOUT")
    print(f"s1_admission_authority_expansion_v14={AUTH}")
    print(f"s1_014_reviewed_head_v14={REVIEWED_HEAD}")
    print(f"s1_014_review_only_pr_v14={REVIEW_PR}")
    print(f"s1_014_qodo_comment_v14={REVIEW_COMMENT}")
    print("s1_014_valid_material_findings_v14=1")
    print("s1_014_security_pass_v14=NO")
    print("codex_security_status_v14=NOT_RUN_NON_BLOCKING")
    print("effective_source_admission_v14=NONE")
    print("effective_dependency_admission_v14=NONE")
    print("new_product_runtime_authority_v14=NONE")
    print("effective_model_provider_execution_v14=NONE")
    print(f"s1_015_repair_authority_v14={S1_015}")


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
        base.fail("v14 installed overlay drifted")
    if dict(v13.WF) != dict(WF):
        base.fail("v14 workflow identity projection drifted")
    if _attr(v11, "_ledger_state", "v11 ledger-state verifier") is not ledger_state:
        base.fail("v14 Harness ledger extension drifted")
    if _PRINT is not V13_PRINT:
        base.fail("v14 predecessor printer identity drifted")
    if _EXPECTED_DESKTOP_EXTENSIONS is None or _EXPECTED_EXECUTION_EXTENSIONS is None:
        base.fail("v14 extension registration unavailable")
    if extset(desktop) != _EXPECTED_DESKTOP_EXTENSIONS:
        base.fail("v14 desktop extension registration drifted")
    if extset(execution) != _EXPECTED_EXECUTION_EXTENSIONS:
        base.fail("v14 execution extension registration drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v13 install", getattr(v13, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook"), V13_DELTA),
        (base.compare_base_controlled, V13_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop extension hook"), V13_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "execution extension hook"), V13_EEXT),
        (_attr(shell, "validate_allowed_paths", "shell allowed-path hook"), V13_ALLOWED),
        (_attr(shell, "verify_policy_files", "shell policy-file hook"), V13_FILES),
        (_attr(shell, "print_success", "shell success hook"), V13_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v14 predecessor hook drifted")
    _PRINT = V13_PRINT
    _EXPECTED_DESKTOP_EXTENSIONS = frozenset(set(extset(desktop)) | {P})
    _EXPECTED_EXECUTION_EXTENSIONS = frozenset(set(extset(execution)) | {P})
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_DESKTOP_EXTENSIONS, "desktop extension registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_EXECUTION_EXTENSIONS, "execution extension registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "routing exact-delta binding")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "desktop extension hook binding")
    _bind(execution, "verify_extension_controlled_paths", eext, "execution extension hook binding")
    _bind(shell, "validate_allowed_paths", allowed, "shell allowed-path hook binding")
    _bind(shell, "verify_policy_files", files, "shell policy-file hook binding")
    _bind(shell, "print_success", printer, "shell success hook binding")
    _INST = True
    overlay()


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def corrected_v13_selftest() -> None:
    patch_predecessor()
    state = review_state(root)
    prior = _attr(v10, "CLOSE_TASKS", "v10 closeout ledger identity")
    if prior != V10_CLOSE_TASKS:
        base.fail("v14 observed v10 closeout ledger drift before predecessor self-test")
    if state == "CLOSED_S1_014":
        _bind(v10, "CLOSE_TASKS", CLOSE_TASKS, "v10 local-ledger self-test projection")
    try:
        _call("v13 predecessor self-test", getattr(v13, "selftest", None))
    finally:
        _bind(v10, "CLOSE_TASKS", prior, "v10 local-ledger self-test restoration")


def selftest() -> None:
    corrected_v13_selftest()
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v14 workflow drifted: {path}")
    if AUTH != "S1_014_EXACT_REVIEW_LEDGER_CLOSEOUT_ONLY":
        base.fail("v14 authority drifted")
    if S1_015 != "NOT_AUTHORIZED":
        base.fail("v14 S1-015 boundary drifted")
    if TRUSTED_BASE_V13_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":  # noqa: S105
        base.fail("v14 bootstrap status semantics drifted")
    if _attr(v13, "AUTH", "v13 authority marker") != (
        "S1_013_CLOSEOUT_CANDIDATE_SELFTEST_LEDGER_PROJECTION_REPAIR_ONLY"
    ):
        base.fail("v14 observed v13 authority drift")
    if _attr(v13, "S1_014", "v13 S1-014 boundary") != "NOT_AUTHORIZED":
        base.fail("v14 observed v13 S1-014 boundary drift")

    vb = root.read_bytes(V13, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V13: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v14", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v14 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    pre = b"pre-ledger"
    post = b"post-ledger"
    inherited = b"s1-013-evidence"
    review = b"s1-014-evidence"
    policy_base = {TASKS: pre, S1_013_EVID: inherited}
    candidate = {TASKS: post, S1_013_EVID: inherited, S1_014_EVID: review}
    closeout(
        mem(candidate),
        mem(policy_base),
        pre=blob(pre),
        post=blob(post),
        inherited_evidence=blob(inherited),
        review_evidence=blob(review),
    )
    wrong = dict(candidate)
    wrong[S1_014_EVID] = b"wrong-review"
    base.expect_failure_matching(
        "v14 wrong review evidence",
        "review evidence identity drifted",
        closeout,
        mem(wrong),
        mem(policy_base),
        pre=blob(pre),
        post=blob(post),
        inherited_evidence=blob(inherited),
        review_evidence=blob(review),
    )
    print("wepld S1 steady-state routing v14 policy self-tests: PASS")


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
