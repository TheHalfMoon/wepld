#!/usr/bin/env python3
"""Authorize one exact S1-015 performance-trigger coverage repair; keep S1-016 closed.

v15 is an append-only successor to canonical v14. It preserves every inherited
runtime, source, dependency, provider, S1-013, and S1-014 boundary. Its only new
steady-state authority is one exact repair to the path filters of
.github/workflows/s1-performance.yml after v15 is canonically activated.

The repair is fail-closed:
- trusted base must contain frozen canonical v14 and the exact closed S1-014
  ledger/review-evidence state;
- candidate delta must be exactly s1-performance.yml;
- the base performance workflow must be the exact pre-repair blob;
- candidate bytes must equal the base workflow with exactly two path-filter
  blocks replaced by the bounded dependency/input coverage block;
- benchmark commands, jobs, permissions, timeouts, and all other workflow bytes
  remain unchanged;
- S1-016 acceptance authority remains unavailable.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any, Callable

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v15_integrity.py"
V14 = ".github/scripts/wepld_s1_admission_steady_state_routing_v14_integrity.py"
V14_BLOB = "9c2a7e7ef6b7c4210b1ceaae6ee18af66e4d960b"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
PW = ".github/workflows/s1-performance.yml"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"
S1_014_EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-014-review-evidence.md"

OLD_WF = {
    FW: "81cca9767055dbbf90e76a4a77191ebe068fd8e3b0902005a20821cc550b71f6",
    AW: "cd61b3cd17c7834bd83cb55b5dfe8bfdf66da6060a6bedc574fb5f50429349e8",
}
WF = {
    FW: "816197dc47bc8876a59bc7f6bec36cadc90d89c431d20ffde0994fc847ceabd4",
    AW: "6f406c11e7e08b4c32eef445c3f1b9dcc7abc5db041c2fce587de2e38b21c16c",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
CLOSED_TASKS = "d85892c252be0b3731b88bd97fae6af40d3776db"
S1_014_EVID_BLOB = "4fd85d2a1f829a63b840020c0e434aeb12f20328"
PW_BASE_BLOB = "b16d57b42e617808d4b5d2547c1677e9ef7c3535"
BOOT = frozenset({P, FW, AW})
REPAIR = frozenset({PW})
AUTH = "S1_015_EXACT_PERFORMANCE_TRIGGER_COVERAGE_REPAIR_ONLY"
FINDING = "F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE"
S1_016 = "NOT_AUTHORIZED"

OLD_PATHS = b"""    paths:
      - ".github/scripts/wepld_s1_performance_probe.py"
      - ".github/workflows/s1-performance.yml"
"""
NEW_PATHS = b"""    paths:
      - ".github/scripts/wepld_s1_performance_probe.py"
      - ".github/workflows/s1-performance.yml"
      - "Cargo.toml"
      - "Cargo.lock"
      - "rust-toolchain.toml"
      - "crates/contracts/**"
      - "crates/core/**"
      - "apps/desktop/**"
      - "third_party/glib-0.18.5-wepld1/**"
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
        base.fail(f"v15 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v15 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v15 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v15 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
actual_v14 = blob(root.read_bytes(V14, base.MAX_POLICY_FILE_BYTES))
if actual_v14 != V14_BLOB:
    base.fail(f"frozen v14 predecessor drifted: expected={V14_BLOB} actual={actual_v14}")

import wepld_s1_admission_steady_state_routing_v14_integrity as v14  # noqa: E402

V14_DELTA = v14.delta
V14_BASE = v14.basectrl
V14_ALLOWED = v14.allowed
V14_FILES = v14.files
V14_DEXT = v14.dext
V14_EEXT = v14.eext
V14_EXT = v14.ext
V14_PRINT = v14.printer
V14_WF = dict(v14.WF)
CAND = v14.CAND
RUNTIME = v14.RUNTIME

if V14_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v14 workflow identities drifted before v15 import: actual={V14_WF}")


def req_v14(view: Any) -> None:
    if V14 not in ps(view):
        base.fail("v15 candidate/base is missing frozen v14 predecessor")
    actual = blob(view.read_bytes(V14, base.MAX_POLICY_FILE_BYTES))
    if actual != V14_BLOB:
        base.fail(f"frozen v14 predecessor drifted: expected={V14_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v14, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v15 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v15 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v14, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v15 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def closed_s1_014(
    view: Any,
    hasher: Callable[[bytes], str] = blob,
    tasks_blob: str = CLOSED_TASKS,
    evidence_blob: str = S1_014_EVID_BLOB,
) -> None:
    paths = ps(view)
    for path in (TASKS, S1_014_EVID):
        if path not in paths or mode(view, path) != "100644":
            base.fail(f"S1-015 repair requires canonical S1-014 path/mode: {path}")
    if hasher(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != tasks_blob:
        base.fail("S1-015 repair requires exact closed S1-014 ledger")
    if hasher(view.read_bytes(S1_014_EVID, base.MAX_POLICY_FILE_BYTES)) != evidence_blob:
        base.fail("S1-015 repair requires exact S1-014 review evidence")


def expected_repair(base_bytes: bytes, old: bytes = OLD_PATHS, new: bytes = NEW_PATHS) -> bytes:
    count = base_bytes.count(old)
    if count != 2:
        base.fail(f"S1-015 performance trigger predecessor block count drifted: expected=2 actual={count}")
    candidate = base_bytes.replace(old, new)
    if candidate.count(new) != 2:
        base.fail("S1-015 performance trigger replacement count drifted")
    return candidate


def repair(
    candidate: Any,
    policy_base: Any,
    base_workflow_blob: str = PW_BASE_BLOB,
    tasks_blob: str = CLOSED_TASKS,
    evidence_blob: str = S1_014_EVID_BLOB,
    old: bytes = OLD_PATHS,
    new: bytes = NEW_PATHS,
) -> None:
    for view in (policy_base, candidate):
        closed_s1_014(view, tasks_blob=tasks_blob, evidence_blob=evidence_blob)
        if PW not in ps(view) or mode(view, PW) != "100644":
            base.fail("S1-015 performance workflow path/mode invalid")
    base_bytes = policy_base.read_bytes(PW, base.MAX_POLICY_FILE_BYTES)
    if blob(base_bytes) != base_workflow_blob:
        base.fail("S1-015 performance workflow predecessor identity drifted")
    expected = expected_repair(base_bytes, old=old, new=new)
    actual = candidate.read_bytes(PW, base.MAX_POLICY_FILE_BYTES)
    if actual != expected:
        base.fail("S1-015 performance trigger repair bytes drifted")


def patch_predecessor() -> None:
    current = dict(v14.WF)
    if current not in (V14_WF, dict(WF)):
        base.fail(f"v15 predecessor workflow identity map drifted: actual={current}")
    _bind(v14, "WF", dict(WF), "v14 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v14(candidate)
            req_v14(policy_base)
            return
        if paths & BOOT:
            base.fail("v15 bootstrap delta must be exactly policy plus two workflows")
    elif P in paths:
        base.fail("canonical v15 wrapper is frozen after activation")
    if paths == REPAIR:
        repair(candidate, policy_base)
        return
    if paths & REPAIR:
        base.fail("S1-015 repair delta must be exactly s1-performance.yml")
    _call("v14 exact-delta verifier", V14_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v14 base-control verifier", V14_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v15 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v15 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v15 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v15 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v14 extension verification", V14_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    current = set(paths)
    if current in (set(BOOT), set(REPAIR)):
        return
    if P in current:
        base.fail("v15 wrapper may change only in exact bootstrap")
    _call("v14 allowed-path verification", V14_ALLOWED, current, stage)


def files(view: Any) -> None:
    req_v14(view)
    _call("v14 policy-file verification", V14_FILES, view)
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v15 wrapper mode invalid")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V14_PRINT:
        base.fail("v15 predecessor printer drifted")
    _call("v14 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v15=V14_PLUS_EXACT_S1_015_PERFORMANCE_TRIGGER_REPAIR")
    print(f"s1_admission_authority_expansion_v15={AUTH}")
    print(f"s1_015_validated_finding_v15={FINDING}")
    print("s1_015_repair_scope_v15=.github/workflows/s1-performance.yml_TRIGGER_PATHS_ONLY")
    print("effective_source_admission_v15=NONE")
    print("effective_dependency_admission_v15=NONE")
    print("new_product_runtime_authority_v15=NONE")
    print("effective_model_provider_execution_v15=NONE")
    print("s1_acceptance_v15=NO")
    print(f"s1_016_authority_v15={S1_016}")


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
        base.fail("v15 installed overlay drifted")
    if dict(v14.WF) != dict(WF):
        base.fail("v15 workflow identity projection drifted")
    if _PRINT is not V14_PRINT:
        base.fail("v15 predecessor printer identity drifted")
    if _EXPECTED_DESKTOP_EXTENSIONS is None or _EXPECTED_EXECUTION_EXTENSIONS is None:
        base.fail("v15 extension registration unavailable")
    if extset(desktop) != _EXPECTED_DESKTOP_EXTENSIONS:
        base.fail("v15 desktop extension registration drifted")
    if extset(execution) != _EXPECTED_EXECUTION_EXTENSIONS:
        base.fail("v15 execution extension registration drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v14 install", getattr(v14, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook"), V14_DELTA),
        (base.compare_base_controlled, V14_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop extension hook"), V14_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "execution extension hook"), V14_EEXT),
        (_attr(shell, "validate_allowed_paths", "shell allowed-path hook"), V14_ALLOWED),
        (_attr(shell, "verify_policy_files", "shell policy-file hook"), V14_FILES),
        (_attr(shell, "print_success", "shell success hook"), V14_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v15 predecessor hook drifted")
    _PRINT = V14_PRINT
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


def corrected_v14_selftest() -> None:
    patch_predecessor()
    _call("v14 predecessor self-test", getattr(v14, "selftest", None))


def selftest() -> None:
    corrected_v14_selftest()
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v15 workflow drifted: {path}")
    if AUTH != "S1_015_EXACT_PERFORMANCE_TRIGGER_COVERAGE_REPAIR_ONLY":
        base.fail("v15 authority drifted")
    if FINDING != "F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE":
        base.fail("v15 finding identity drifted")
    if S1_016 != "NOT_AUTHORIZED":
        base.fail("v15 S1-016 boundary drifted")
    if _attr(v14, "AUTH", "v14 authority marker") != "S1_014_EXACT_REVIEW_LEDGER_CLOSEOUT_ONLY":
        base.fail("v15 observed v14 authority drift")
    if _attr(v14, "S1_015", "v14 S1-015 boundary") != "NOT_AUTHORIZED":
        base.fail("v15 observed v14 S1-015 boundary drift")

    vb = root.read_bytes(V14, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V14: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v15", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v15 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    tasks = b"closed-s1-014-ledger"
    review = b"s1-014-review-evidence"
    old_block = b"paths-old\n"
    new_block = b"paths-new\n"
    workflow = b"start\n" + old_block + b"middle\n" + old_block + b"end\n"
    repaired = workflow.replace(old_block, new_block)
    policy_base = {TASKS: tasks, S1_014_EVID: review, PW: workflow}
    candidate = {TASKS: tasks, S1_014_EVID: review, PW: repaired}
    repair(
        mem(candidate),
        mem(policy_base),
        base_workflow_blob=blob(workflow),
        tasks_blob=blob(tasks),
        evidence_blob=blob(review),
        old=old_block,
        new=new_block,
    )
    wrong = dict(candidate)
    wrong[PW] = repaired + b"extra"
    base.expect_failure_matching(
        "v15 widened performance repair",
        "repair bytes drifted",
        repair,
        mem(wrong),
        mem(policy_base),
        base_workflow_blob=blob(workflow),
        tasks_blob=blob(tasks),
        evidence_blob=blob(review),
        old=old_block,
        new=new_block,
    )
    missing = dict(policy_base)
    missing[PW] = b"start\n" + old_block + b"end\n"
    base.expect_failure_matching(
        "v15 missing trigger block",
        "predecessor block count drifted",
        repair,
        mem(candidate),
        mem(missing),
        base_workflow_blob=blob(missing[PW]),
        tasks_blob=blob(tasks),
        evidence_blob=blob(review),
        old=old_block,
        new=new_block,
    )
    print("wepld S1 steady-state routing v15 policy self-tests: PASS")


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
