#!/usr/bin/env python3
"""Authorize one exact S1-013 evidence/ledger closeout; keep S1-014 closed."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v10_integrity.py"
V9 = ".github/scripts/wepld_s1_admission_steady_state_routing_v9_integrity.py"
V9_BLOB = "69d187415b68bc4d4ab1a64244370749bc71113f"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
PW = ".github/workflows/s1-performance.yml"
PP = ".github/scripts/wepld_s1_performance_probe.py"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"
EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-013-performance-evidence.md"
OLD_WF = {
    FW: "c49e76220a3d514ae8abca79034f65c444a8363c072c9d76e032f7483cd6c2d9",
    AW: "3e4453bb8f53f1baeefb5953bf62501a8311627fc3cffc4fe6ce6f219ce7af7d",
}
WF = {
    FW: "97d6f3bc5c6f668ebaa795f144e979c25b443fa3cc4d06d894e6d4a3a2f52f94",
    AW: "faa5c2c528378397117b6acaa5a8ed3ec23a51005b7d442e86d4cd9aa02e0273",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
PW_SHA = "7dd7f670740b651e30700a0fe10b4f1dcd8d51a46b257789e54a02c74df98784"
PW_BLOB = "b16d57b42e617808d4b5d2547c1677e9ef7c3535"
PP_SHA = "e3eb6572b7cd4e35f07abaadb460907919acc091e27db94e4ebbd8ee0b83d6af"
PP_BLOB = "1b33c84c266ecab89af1b6e63f9677875fd5ecf5"
PRE_TASKS = "d331b7f167fe67ae9061ed553cf0949fab12aae0"
CLOSE_TASKS = "f8d9d09dc2e02861246614f374173a0a2bfff9c2"
EVID_SHA = "cbbf6361a8e4bbc10a7d7426e361dd5b48ef6ee34d159763d1ce8aa23e62da46"
EVID_BLOB = "bd79c1e64b397fda3677fb549e9a7feb0c5a8c3d"
BOOT = frozenset({P, FW, AW})
CLOSE = frozenset({TASKS, EVID})
AUTH = "S1_013_EVIDENCE_LEDGER_CLOSEOUT_ONLY"
S1_014 = "NOT_AUTHORIZED"
MERGE = "96fa229610f31598326493b75b40a3353b46bbbf"
RUNS = ("32955349075", "32955348827", "32955348872")
_INST = False
_PRINT: Any = None


def blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()  # noqa: S324


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ps(view: Any) -> set[str]:
    return {entry.path for entry in view.entries()}


def mode(view: Any, path: str) -> str:
    for entry in view.entries():
        if entry.path == path:
            return entry.mode
    base.fail(f"missing path: {path}")


def exact_art(view: Any, path: str, sha256: str, git_blob: str, label: str) -> None:
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if sha(data) != sha256 or blob(data) != git_blob:
        base.fail(f"{label} identity drifted")


def req_v9(view: Any) -> None:
    if V9 not in ps(view):
        base.fail("v9 predecessor missing")
    if blob(view.read_bytes(V9, base.MAX_POLICY_FILE_BYTES)) != V9_BLOB:
        base.fail("v9 predecessor drifted")


def _call(label: str, function: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(function):
        base.fail(f"v10 {label} drifted: not callable")
    try:
        return function(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v10 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v10 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v10 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V9, base.MAX_POLICY_FILE_BYTES)) != V9_BLOB:
    base.fail("local v9 predecessor drifted")
import wepld_s1_admission_steady_state_routing_v9_integrity as v9  # noqa: E402

V9_DELTA = getattr(v9, "_require_exact_delta_v9", None)
V9_BASE = getattr(v9, "_compare_base_controlled_v9", None)
V9_ALLOWED = getattr(v9, "_validate_allowed_paths_v9", None)
V9_FILES = getattr(v9, "_verify_policy_files_v9", None)
V9_EXT = getattr(v9, "_verify_extension_paths_v9", None)
V9_D = getattr(v9, "_verify_desktop_extension_paths_v9", None)
V9_E = getattr(v9, "_verify_execution_extension_paths_v9", None)
V9_PRINT = getattr(v9, "_print_success", None)
CAND = getattr(v9, "_EXPECTED_CANDIDATE_LOCAL", None)
RUNTIME = getattr(v9, "_EXPECTED_RUNTIME_MAIN", None)


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v9, "_topology", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v10 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v10 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v9, "_changed_paths", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v10 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def closeout(
    candidate: Any,
    policy_base: Any,
    pre: str = PRE_TASKS,
    tasks: str = CLOSE_TASKS,
    es: str = EVID_SHA,
    eb: str = EVID_BLOB,
) -> None:
    if blob(policy_base.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != pre:
        base.fail("S1-013 closeout trusted ledger drifted")
    if EVID in ps(policy_base) or EVID not in ps(candidate):
        base.fail("S1-013 closeout evidence state invalid")
    if mode(candidate, TASKS) != "100644" or mode(candidate, EVID) != "100644":
        base.fail("S1-013 closeout Markdown mode invalid")
    for view in (policy_base, candidate):
        exact_art(view, PW, PW_SHA, PW_BLOB, "performance workflow")
        exact_art(view, PP, PP_SHA, PP_BLOB, "performance probe")
    if blob(candidate.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != tasks:
        base.fail("S1-013 reconciled ledger identity drifted")
    exact_art(candidate, EVID, es, eb, "S1-013 performance evidence")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v9(candidate)
            req_v9(policy_base)
            return
        if paths & BOOT:
            base.fail("v10 bootstrap delta must be exactly policy plus two workflows")
    if paths == CLOSE:
        closeout(candidate, policy_base)
        return
    if paths & CLOSE:
        base.fail("S1-013 closeout delta must be exactly tasks plus evidence")
    _call("predecessor exact-delta", V9_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("predecessor base-control", V9_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v10 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v10 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v10 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v10 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("predecessor extension verification", V9_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    _call("predecessor allowed-path verification", V9_ALLOWED, set(paths) - {P}, stage)


def files(view: Any) -> None:
    req_v9(view)
    _call("predecessor policy-file verification", V9_FILES, view)
    if P not in ps(view):
        base.fail("v10 wrapper missing")
    if EVID in ps(view):
        if mode(view, TASKS) != "100644" or mode(view, EVID) != "100644":
            base.fail("S1-013 canonical closeout Markdown mode invalid")
        if blob(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != CLOSE_TASKS:
            base.fail("S1-013 canonical ledger drifted")
        exact_art(view, EVID, EVID_SHA, EVID_BLOB, "S1-013 canonical evidence")
    elif blob(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)) != PRE_TASKS:
        base.fail("S1-013 ledger changed before closeout")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V9_PRINT:
        base.fail("v10 predecessor printer drifted")
    _call("predecessor success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v10=V9_PRESERVED_PLUS_S1_013_CLOSEOUT")
    print(f"s1_admission_authority_expansion_v10={AUTH}")
    print(f"s1_013_measurement_merge_v10={MERGE}")
    print(f"s1_013_foundation_run_v10={RUNS[0]}")
    print(f"s1_013_contracts_run_v10={RUNS[1]}")
    print(f"s1_013_performance_run_v10={RUNS[2]}")
    print("effective_source_admission_v10=NONE")
    print("effective_dependency_admission_v10=NONE")
    print("effective_donor_execution_v10=NONE")
    print("new_product_runtime_authority_v10=NONE")
    print("network_listener_authority_v10=NONE")
    print("effective_model_provider_execution_v10=NONE")
    print("effective_model_weight_access_v10=NONE")
    print("effective_model_inference_v10=NONE")
    print("s1_013_evidence_closeout_v10=EXACT_CONTENT_ADDRESSED_TRANSITION_AFTER_V10_CANONICAL_ACTIVATION")
    print(f"s1_014_plus_v10={S1_014}")


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
        base.fail("v10 overlay hook drifted")
    if P not in extset(desktop) or P not in extset(execution):
        base.fail("v10 extension registration drifted")


def patch() -> None:
    _bind(v9, "EXPECTED_WORKFLOW_SHA256", dict(WF), "workflow identity binding")


def install() -> None:
    global _INST, _PRINT
    if _INST:
        overlay()
        return
    patch()
    _call("predecessor policy installation", getattr(v9, "_install_policy", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor exact-delta hook"), V9_DELTA),
        (base.compare_base_controlled, V9_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop extension hook"), V9_D),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution extension hook"), V9_E),
        (_attr(shell, "validate_allowed_paths", "predecessor shell allowed-path hook"), V9_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor shell policy-file hook"), V9_FILES),
        (_attr(shell, "print_success", "predecessor shell success hook"), V9_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v10 predecessor hook drifted")
    _PRINT = V9_PRINT
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", frozenset(set(extset(desktop)) | {P}), "desktop extension registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", frozenset(set(extset(execution)) | {P}), "execution extension registration")
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


def selftest() -> None:
    patch()
    _call("predecessor self-test", getattr(v9, "selftest", None))
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v10 workflow drifted: {path}")
    if AUTH != "S1_013_EVIDENCE_LEDGER_CLOSEOUT_ONLY" or S1_014 != "NOT_AUTHORIZED":
        base.fail("v10 authority drifted")

    base.expect_failure_matching(
        "v10 missing topology attribute",
        "topology/layout drifted",
        _attr,
        object(),
        "missing",
        "self-test attribute",
    )
    base.expect_failure_matching(
        "v10 non-callable topology hook",
        "not callable",
        _call,
        "self-test call",
        None,
    )

    vb = root.read_bytes(V9, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V9: vb, FW: b"o", AW: b"o"}
    candidate = dict(policy_base)
    candidate.update({P: b"v10", FW: b"n", AW: b"n"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v10 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    pt = b"prior"
    ct = b"close"
    ev = b"evidence"
    pw = b"pw"
    pp = b"pp"
    policy_base = {P: b"v10", TASKS: pt, PW: pw, PP: pp}
    candidate = dict(policy_base)
    candidate[TASKS] = ct
    candidate[EVID] = ev
    global PW_SHA, PW_BLOB, PP_SHA, PP_BLOB
    old = (PW_SHA, PW_BLOB, PP_SHA, PP_BLOB)
    PW_SHA, PW_BLOB, PP_SHA, PP_BLOB = sha(pw), blob(pw), sha(pp), blob(pp)
    try:
        closeout(mem(candidate), mem(policy_base), blob(pt), blob(ct), sha(ev), blob(ev))
        wrong = dict(candidate)
        wrong[EVID] = b"wrong"
        base.expect_failure_matching(
            "v10 wrong evidence",
            "performance evidence identity drifted",
            closeout,
            mem(wrong),
            mem(policy_base),
            pre=blob(pt),
            tasks=blob(ct),
            es=sha(ev),
            eb=blob(ev),
        )
    finally:
        PW_SHA, PW_BLOB, PP_SHA, PP_BLOB = old
    print("wepld S1 steady-state routing v10 policy self-tests: PASS")


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
