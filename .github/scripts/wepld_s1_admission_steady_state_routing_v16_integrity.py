#!/usr/bin/env python3
"""Repair v15's inherited performance-workflow identity projection; keep S1-016 closed.

v16 is an append-only successor to canonical v15. It grants no new product,
source, dependency, runtime, provider, model, review-closeout, or acceptance
authority. v15 already authorizes one exact S1-015 change to the trigger path
filters of .github/workflows/s1-performance.yml.

v15's exact-delta verifier correctly accepts those repair bytes, but an older
inherited policy-file verifier still requires the pre-repair S1-013 workflow
identity. v16 fixes only that verifier-integration defect:

- the actual repository view may contain only the exact pre-repair workflow or
  the exact v15-authorized repaired workflow;
- the repaired workflow is independently content-addressed and reversed to the
  exact predecessor bytes solely for inherited policy-file verification;
- every other candidate byte and every other inherited policy gate is preserved;
- S1-016 remains unavailable.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v16_integrity.py"
V15 = ".github/scripts/wepld_s1_admission_steady_state_routing_v15_integrity.py"
V15_BLOB = "8c967d557c762223f1047f855091fa2ce64b2976"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
PW = ".github/workflows/s1-performance.yml"

OLD_WF = {
    FW: "816197dc47bc8876a59bc7f6bec36cadc90d89c431d20ffde0994fc847ceabd4",
    AW: "6f406c11e7e08b4c32eef445c3f1b9dcc7abc5db041c2fce587de2e38b21c16c",
}
WF = {
    FW: "42617be8a808aad53fbd7c157690ef05c6af11befd7ef5a78df5059378d3459b",
    AW: "cdecf78c21462ee45d1cbe889fe816354e327da9894cca1d2b387f6e40aa8a3b",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}
PW_BASE_SHA256 = "7dd7f670740b651e30700a0fe10b4f1dcd8d51a46b257789e54a02c74df98784"
PW_BASE_BLOB = "b16d57b42e617808d4b5d2547c1677e9ef7c3535"
PW_REPAIRED_SHA256 = "6c0b8cb346730a6865a6a2e5b9af2dbccb788c572fa6d36d36860814cabd008e"
PW_REPAIRED_BLOB = "3ccd118aea80fd31866973371babc329913aafb8"

BOOT = frozenset({P, FW, AW})
AUTH = "S1_015_PERFORMANCE_POLICY_FILE_IDENTITY_PROJECTION_REPAIR_ONLY"
FINDING = "F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE"
S1_016 = "NOT_AUTHORIZED"

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
        base.fail(f"v16 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v16 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v16 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v16 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
actual_v15 = blob(root.read_bytes(V15, base.MAX_POLICY_FILE_BYTES))
if actual_v15 != V15_BLOB:
    base.fail(f"frozen v15 predecessor drifted: expected={V15_BLOB} actual={actual_v15}")

import wepld_s1_admission_steady_state_routing_v15_integrity as v15  # noqa: E402

V15_DELTA = v15.delta
V15_BASE = v15.basectrl
V15_ALLOWED = v15.allowed
V15_FILES = v15.files
V15_DEXT = v15.dext
V15_EEXT = v15.eext
V15_EXT = v15.ext
V15_PRINT = v15.printer
V15_WF = dict(v15.WF)
CAND = v15.CAND
RUNTIME = v15.RUNTIME

if V15_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v15 workflow identities drifted before v16 import: actual={V15_WF}")
if _attr(v15, "PW_BASE_BLOB", "v15 performance predecessor blob") != PW_BASE_BLOB:
    base.fail("v15 performance predecessor identity drifted")
if _attr(v15, "AUTH", "v15 authority marker") != "S1_015_EXACT_PERFORMANCE_TRIGGER_COVERAGE_REPAIR_ONLY":
    base.fail("v15 S1-015 authority drifted")
if _attr(v15, "S1_016", "v15 S1-016 boundary") != "NOT_AUTHORIZED":
    base.fail("v15 S1-016 boundary drifted")


def req_v15(view: Any) -> None:
    if V15 not in ps(view):
        base.fail("v16 candidate/base is missing frozen v15 predecessor")
    actual = blob(view.read_bytes(V15, base.MAX_POLICY_FILE_BYTES))
    if actual != V15_BLOB:
        base.fail(f"frozen v15 predecessor drifted: expected={V15_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v15, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v16 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v16 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v15, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v16 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


class _PerformanceWorkflowProjection:
    def __init__(self, view: Any, predecessor_bytes: bytes) -> None:
        self._view = view
        self._predecessor_bytes = predecessor_bytes

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path == PW:
            if len(self._predecessor_bytes) > max_bytes:
                base.fail("projected performance workflow exceeds read bound")
            return self._predecessor_bytes
        return self._view.read_bytes(path, max_bytes)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def project_performance_workflow(view: Any) -> Any:
    if PW not in ps(view) or mode(view, PW) != "100644":
        base.fail("v16 requires canonical S1 performance workflow path/mode")
    actual = view.read_bytes(PW, base.MAX_POLICY_FILE_BYTES)
    actual_sha = sha(actual)
    actual_blob = blob(actual)
    if actual_sha == PW_BASE_SHA256 and actual_blob == PW_BASE_BLOB:
        return view
    if actual_sha != PW_REPAIRED_SHA256 or actual_blob != PW_REPAIRED_BLOB:
        base.fail(
            "S1-015 performance workflow is outside exact v15-authorized identities: "
            f"sha256={actual_sha} git_blob={actual_blob}"
        )
    old_block = _attr(v15, "OLD_PATHS", "v15 old trigger block")
    new_block = _attr(v15, "NEW_PATHS", "v15 repaired trigger block")
    if not isinstance(old_block, bytes) or not isinstance(new_block, bytes):
        base.fail("v15 trigger-block identity topology drifted")
    if actual.count(new_block) != 2:
        base.fail("v16 repaired performance trigger block count drifted")
    predecessor = actual.replace(new_block, old_block)
    if sha(predecessor) != PW_BASE_SHA256 or blob(predecessor) != PW_BASE_BLOB:
        base.fail("v16 repaired workflow does not reverse to exact S1-013 predecessor")
    expected = _call("v15 repair constructor", getattr(v15, "expected_repair", None), predecessor)
    if expected != actual:
        base.fail("v16 repaired workflow does not equal exact v15 repair bytes")
    return _PerformanceWorkflowProjection(view, predecessor)


def patch_predecessor() -> None:
    current = dict(v15.WF)
    if current not in (V15_WF, dict(WF)):
        base.fail(f"v16 predecessor workflow identity map drifted: actual={current}")
    _bind(v15, "WF", dict(WF), "v15 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v15(candidate)
            req_v15(policy_base)
            return
        if paths & BOOT:
            base.fail("v16 bootstrap delta must be exactly policy plus two workflows")
    elif P in paths:
        base.fail("canonical v16 wrapper is frozen after activation")
    _call("v15 exact-delta verifier", V15_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v15 base-control verifier", V15_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v16 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v16 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v16 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v16 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v15 extension verification", V15_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - {P}
    if remaining:
        _call("v15 allowed-path verification", V15_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v15(view)
    projected = project_performance_workflow(view)
    _call("v15 policy-file verification", V15_FILES, projected)
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v16 wrapper mode invalid")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V15_PRINT:
        base.fail("v16 predecessor printer drifted")
    _call("v15 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v16=V15_PLUS_PERFORMANCE_POLICY_FILE_IDENTITY_PROJECTION_REPAIR")
    print(f"s1_admission_authority_expansion_v16={AUTH}")
    print(f"s1_015_validated_finding_v16={FINDING}")
    print("s1_015_repair_bytes_v16=UNCHANGED_FROM_V15")
    print("effective_source_admission_v16=NONE")
    print("effective_dependency_admission_v16=NONE")
    print("new_product_runtime_authority_v16=NONE")
    print("effective_model_provider_execution_v16=NONE")
    print("s1_acceptance_v16=NO")
    print(f"s1_016_authority_v16={S1_016}")


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
        base.fail("v16 installed overlay drifted")
    if dict(v15.WF) != dict(WF):
        base.fail("v16 workflow identity projection drifted")
    if _PRINT is not V15_PRINT:
        base.fail("v16 predecessor printer identity drifted")
    if _EXPECTED_DESKTOP_EXTENSIONS is None or _EXPECTED_EXECUTION_EXTENSIONS is None:
        base.fail("v16 extension registration unavailable")
    if extset(desktop) != _EXPECTED_DESKTOP_EXTENSIONS:
        base.fail("v16 desktop extension registration drifted")
    if extset(execution) != _EXPECTED_EXECUTION_EXTENSIONS:
        base.fail("v16 execution extension registration drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v15 install", getattr(v15, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor exact-delta hook"), V15_DELTA),
        (base.compare_base_controlled, V15_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop extension hook"), V15_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution extension hook"), V15_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed-path hook"), V15_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor policy-file hook"), V15_FILES),
        (_attr(shell, "print_success", "predecessor success hook"), V15_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v16 predecessor hook drifted")
    _PRINT = V15_PRINT
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


def corrected_v15_selftest() -> None:
    patch_predecessor()
    _call("v15 predecessor self-test", getattr(v15, "selftest", None))


def selftest() -> None:
    corrected_v15_selftest()
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v16 workflow drifted: {path}")
    if AUTH != "S1_015_PERFORMANCE_POLICY_FILE_IDENTITY_PROJECTION_REPAIR_ONLY":
        base.fail("v16 authority drifted")
    if FINDING != "F1_PERFORMANCE_WORKFLOW_TRIGGER_COVERAGE":
        base.fail("v16 finding identity drifted")
    if S1_016 != "NOT_AUTHORIZED":
        base.fail("v16 S1-016 boundary drifted")

    v15_bytes = root.read_bytes(V15, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V15: v15_bytes, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v16", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v16 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )
    allowed({P}, "S1_PRODUCT_RUNTIME")
    allowed({P, PW}, "S1_PRODUCT_RUNTIME")

    old = root.read_bytes(PW, base.MAX_POLICY_FILE_BYTES)
    if sha(old) == PW_REPAIRED_SHA256 and blob(old) == PW_REPAIRED_BLOB:
        old_block = _attr(v15, "OLD_PATHS", "v15 old trigger block")
        new_block = _attr(v15, "NEW_PATHS", "v15 repaired trigger block")
        old = old.replace(new_block, old_block)
    if sha(old) != PW_BASE_SHA256 or blob(old) != PW_BASE_BLOB:
        base.fail("v16 self-test could not reconstruct exact pre-repair workflow")
    repaired = _call("v15 repair constructor", getattr(v15, "expected_repair", None), old)
    if sha(repaired) != PW_REPAIRED_SHA256 or blob(repaired) != PW_REPAIRED_BLOB:
        base.fail("v16 repaired workflow content address drifted")
    old_view = mem({PW: old})
    repaired_view = mem({PW: repaired})
    if project_performance_workflow(old_view).read_bytes(PW, base.MAX_POLICY_FILE_BYTES) != old:
        base.fail("v16 pre-repair projection drifted")
    if project_performance_workflow(repaired_view).read_bytes(PW, base.MAX_POLICY_FILE_BYTES) != old:
        base.fail("v16 repaired projection drifted")
    wrong = mem({PW: repaired + b"\n"})
    base.expect_failure_matching(
        "v16 widened performance identity rejection",
        "outside exact v15-authorized identities",
        project_performance_workflow,
        wrong,
    )

    files(root)
    print("wepld S1 steady-state routing v16 policy self-tests: PASS")


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
