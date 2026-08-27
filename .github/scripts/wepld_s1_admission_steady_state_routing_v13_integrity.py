#!/usr/bin/env python3
"""Repair S1-013 closeout candidate self-tests without expanding authority.

v13 is an append-only successor to canonical v12. Runtime/admission behavior and
all source/dependency/provider/S1-014 boundaries remain delegated to v12. The
only change is self-test state handling: while frozen v10 predecessor self-tests
inspect the local repository, Harness ledger expectation is temporarily projected
to the exact v11-recognized local S1-013 state, then restored before v11
compatibility hooks run. Unknown ledger/evidence states still fail closed.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any, Callable

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v13_integrity.py"
V12 = ".github/scripts/wepld_s1_admission_steady_state_routing_v12_integrity.py"
V12_BLOB = "91668a3817b86edbf87e55b96f0742f53171e8a0"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
OLD_WF = {
    FW: "bee8dc667a00043ff34f5bba5920946a78c09ef2fdfed6ba186ad5cdc0717943",
    AW: "ab378e3e38ae943f98db92c5ef859338c4c62917d04b3fa7e67b3c8ea70906ca",
}
WF = {
    FW: "d3bd0c52afefa27672a2016d0596a3c2a08f26ef08ab5f9e7bf8cdbeb3e518be",
    AW: "b2e5aed34aa4c3f7be6056ec36376749b1c3c0851259d9f6c2ff948c5b020aa8",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
BOOT = frozenset({P, FW, AW})
AUTH = "S1_013_CLOSEOUT_CANDIDATE_SELFTEST_LEDGER_PROJECTION_REPAIR_ONLY"
S1_014 = "NOT_AUTHORIZED"
TRUSTED_BASE_V12_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
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


def _call(label: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(fn):
        base.fail(f"v13 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v13 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v13 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v13 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
actual_v12 = blob(root.read_bytes(V12, base.MAX_POLICY_FILE_BYTES))
if actual_v12 != V12_BLOB:
    base.fail(f"frozen v12 predecessor drifted: expected={V12_BLOB} actual={actual_v12}")

import wepld_s1_admission_steady_state_routing_v12_integrity as v12  # noqa: E402

V12_DELTA = v12.delta
V12_BASE = v12.basectrl
V12_ALLOWED = v12.allowed
V12_FILES = v12.files
V12_DEXT = v12.dext
V12_EEXT = v12.eext
V12_EXT = v12.ext
V12_PRINT = v12.printer
V12_WF = dict(v12.WF)
CAND = v12.CAND
RUNTIME = v12.RUNTIME


def req_v12(view: Any) -> None:
    if V12 not in ps(view):
        base.fail("v13 candidate/base is missing frozen v12 predecessor")
    actual = blob(view.read_bytes(V12, base.MAX_POLICY_FILE_BYTES))
    if actual != V12_BLOB:
        base.fail(f"frozen v12 predecessor drifted: expected={V12_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v12, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v13 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v13 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v12, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v13 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def patch_workflows() -> None:
    current = dict(v12.WF)
    expected = {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}
    if current not in (expected, dict(WF)):
        base.fail(f"v13 predecessor workflow identity map drifted: actual={current}")
    _bind(v12, "WF", dict(WF), "v12 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v12(candidate)
            req_v12(policy_base)
            return
        if paths & BOOT:
            base.fail("v13 bootstrap delta must be exactly policy plus two workflows")
    _call("v12 exact-delta verifier", V12_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v12 base-control verifier", V12_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v13 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v13 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v13 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v13 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v12 extension verification", V12_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    _call("v12 allowed-path verification", V12_ALLOWED, set(paths) - {P}, stage)


def files(view: Any) -> None:
    req_v12(view)
    _call("v12 policy-file verification", V12_FILES, view)
    if P not in ps(view):
        base.fail("v13 wrapper missing")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V12_PRINT:
        base.fail("v13 predecessor printer drifted")
    _call("v12 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v13=V12_PLUS_CANDIDATE_SELFTEST_LEDGER_PROJECTION_REPAIR")
    print(f"s1_admission_authority_expansion_v13={AUTH}")
    print("s1_013_closeout_authority_v13=UNCHANGED_FROM_V12")
    print("candidate_selftest_ledger_states_v13=PRE_OR_EXACT_CLOSEOUT_ONLY")
    print("harness_authority_expansion_v13=NONE")
    print("effective_source_admission_v13=NONE")
    print("effective_dependency_admission_v13=NONE")
    print("new_product_runtime_authority_v13=NONE")
    print("effective_model_provider_execution_v13=NONE")
    print(f"s1_014_plus_v13={S1_014}")


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
        base.fail("v13 installed overlay drifted")
    if dict(v12.WF) != dict(WF):
        base.fail("v13 workflow identity projection drifted")
    if _PRINT is not V12_PRINT:
        base.fail("v13 predecessor printer identity drifted")
    if _EXPECTED_DESKTOP_EXTENSIONS is None or _EXPECTED_EXECUTION_EXTENSIONS is None:
        base.fail("v13 extension registration unavailable")
    if extset(desktop) != _EXPECTED_DESKTOP_EXTENSIONS:
        base.fail("v13 desktop extension registration drifted")
    if extset(execution) != _EXPECTED_EXECUTION_EXTENSIONS:
        base.fail("v13 execution extension registration drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_workflows()
    _call("v12 install", getattr(v12, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook"), V12_DELTA),
        (base.compare_base_controlled, V12_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop extension hook"), V12_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "execution extension hook"), V12_EEXT),
        (_attr(shell, "validate_allowed_paths", "shell allowed-path hook"), V12_ALLOWED),
        (_attr(shell, "verify_policy_files", "shell policy-file hook"), V12_FILES),
        (_attr(shell, "print_success", "shell success hook"), V12_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v13 predecessor hook drifted")
    _PRINT = V12_PRINT
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


def _with_local_ledger_projection(fn: Callable[[], Any]) -> Any:
    v11 = _attr(v12, "v11", "v12 v11 predecessor module")
    hr = _attr(v11, "hr", "v11 Harness research module")
    expected = _call(
        "local ledger-state verification",
        _attr(v11, "_ledger_state", "v11 ledger-state verifier"),
        root,
        _attr(hr, "_git_blob_sha1", "Harness ledger blob hasher"),
    )
    frozen = _attr(v11, "HR_EXPECTED_LEDGER", "v11 frozen Harness ledger identity")
    prior = _attr(hr, "EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1", "Harness reconciled-ledger identity")
    if prior != frozen:
        base.fail(f"v13 Harness ledger constant drifted before projection: expected={frozen} actual={prior}")
    _bind(hr, "EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1", expected, "candidate self-test ledger projection")
    try:
        return _call("projected frozen predecessor self-test", fn)
    finally:
        _bind(hr, "EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1", prior, "candidate self-test ledger restoration")


def corrected_v12_selftest() -> None:
    v11 = _attr(v12, "v11", "v12 v11 predecessor module")
    v10 = _attr(v11, "v10", "v11 v10 predecessor module")
    original = _attr(v10, "selftest", "v10 predecessor self-test")

    def projected() -> Any:
        return _with_local_ledger_projection(original)

    _bind(v10, "selftest", projected, "v10 self-test projection hook")
    try:
        _call("v12 predecessor self-test", _attr(v12, "selftest", "v12 predecessor self-test"))
    finally:
        _bind(v10, "selftest", original, "v10 self-test restoration")


def selftest() -> None:
    patch_workflows()
    corrected_v12_selftest()
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v13 workflow drifted: {path}")
    if AUTH != "S1_013_CLOSEOUT_CANDIDATE_SELFTEST_LEDGER_PROJECTION_REPAIR_ONLY":
        base.fail("v13 authority drifted")
    if S1_014 != "NOT_AUTHORIZED":
        base.fail("v13 S1-014 boundary drifted")
    if TRUSTED_BASE_V12_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":  # noqa: S105
        base.fail("v13 bootstrap status semantics drifted")
    if _attr(v12, "AUTH", "v12 authority marker") != "S1_013_CLOSEOUT_SELFTEST_SEQUENCING_REPAIR_ONLY":
        base.fail("v13 observed v12 authority drift")
    if _attr(v12, "S1_014", "v12 S1-014 boundary") != "NOT_AUTHORIZED":
        base.fail("v13 observed v12 S1-014 boundary drift")

    vb = root.read_bytes(V12, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V12: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v13", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v13 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )
    print("wepld S1 steady-state routing v13 policy self-tests: PASS")


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
