#!/usr/bin/env python3
"""Repair accepted-S1 inherited policy-root projection; grant no new product or S2 authority.

v20 is an append-only successor to canonical v19. It repairs only the
accepted-state predecessor self-test projection discovered by the exact S1-016
candidate: reachable WePLD policy modules outside the `wepld_s1_*` namespace
can also own repository `root` views and must observe the exact pre-S1-016 task
ledger while v19 validates the accepted transition.

The repair generalizes the bounded predecessor traversal from S1-only modules
to reachable `wepld_*` policy modules with roots. It preserves v19's exact
delegated S1-016 authority and keeps S2, roadmap, source, dependency, runtime,
provider, model, and effect authority closed.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v20_integrity.py"
V19 = ".github/scripts/wepld_s1_admission_steady_state_routing_v19_integrity.py"
V19_BLOB = "be0504049258234e910c17e10622d2012316d95e"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

OLD_WF = {
    FW: "f1de24d95ce654e1cd6de5618d556d76dd7d07165945fce96ff7a0e3a0722085",
    AW: "d96f36e574475e300ca38eb0590170d740554afb8e437704d61004b87a639016",
}
WF = {
    FW: "fdbebf7b904f99c2ac02a941a361e6b7bcc443bd9958faebc5d64ea585d276bb",
    AW: "a8284f5f2d603fe12c7e1bcae9f36762d6776684fd3c6fd85acf86c0dbb6db56",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S1_016_ACCEPTED_STATE_POLICY_GRAPH_PROJECTION_REPAIR_ONLY"
S1_016 = "EXACT_V19_DELEGATED_TRANSITION_ONLY"
S2 = "NOT_AUTHORIZED"
ROADMAP = "NOT_AUTHORIZED"
TRUSTED_BASE_V19_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"  # noqa: S105
MAX_POLICY_MODULES = 128

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
        base.fail(f"v20 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v20 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v20 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v20 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V19, base.MAX_POLICY_FILE_BYTES)) != V19_BLOB:
    base.fail("frozen v19 predecessor drifted")

import wepld_s1_admission_steady_state_routing_v19_integrity as v19  # noqa: E402

V19_DELTA = v19.delta
V19_BASE = v19.basectrl
V19_ALLOWED = v19.allowed
V19_FILES = v19.files
V19_DEXT = v19.dext
V19_EEXT = v19.eext
V19_EXT = v19.ext
V19_PRINT = v19.printer
V19_WF = dict(v19.WF)
V19_POLICY_DESCENDANTS = v19._policy_descendants
CAND = v19.CAND
RUNTIME = v19.RUNTIME

if V19_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v19 workflow identities drifted before v20 import: actual={V19_WF}")
if _attr(v19, "AUTH", "v19 authority marker") != "S1_016_ACCEPTED_STATE_SELFTEST_PROJECTION_REPAIR_ONLY":
    base.fail("v20 observed v19 authority drift")
if _attr(v19, "S1_016", "v19 S1-016 boundary") != "EXACT_V18_TRANSITION_ONLY":
    base.fail("v20 observed v19 S1-016 boundary drift")
if _attr(v19, "S2", "v19 S2 boundary") != "NOT_AUTHORIZED":
    base.fail("v20 observed v19 S2 boundary drift")


def req_v19(view: Any) -> None:
    if V19 not in ps(view):
        base.fail("v20 candidate/base is missing frozen v19 predecessor")
    actual = blob(view.read_bytes(V19, base.MAX_POLICY_FILE_BYTES))
    if actual != V19_BLOB:
        base.fail(f"frozen v19 predecessor drifted: expected={V19_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v19, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v20 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v20 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v19, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v20 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _policy_modules(module: ModuleType) -> list[ModuleType]:
    stack = [module]
    seen: set[int] = set()
    result: list[ModuleType] = []
    while stack:
        current = stack.pop()
        identity = id(current)
        if identity in seen:
            continue
        seen.add(identity)
        if len(seen) > MAX_POLICY_MODULES:
            base.fail("v20 predecessor policy-module traversal exceeded bound")
        for value in vars(current).values():
            if not isinstance(value, ModuleType):
                continue
            name = getattr(value, "__name__", "")
            if not name.startswith("wepld_"):
                continue
            if value is v19:
                continue
            stack.append(value)
        if current is not module and current is not v19 and hasattr(current, "root"):
            result.append(current)
    result.sort(key=lambda item: getattr(item, "__name__", ""))
    return result


def _policy_graph_regression() -> None:
    v18 = _attr(v19, "v18", "v19 v18 predecessor module")
    start = _attr(v18, "v17", "v18 v17 predecessor module")
    modules = _policy_modules(start)
    names = {getattr(module, "__name__", "") for module in modules}
    if not any(name.endswith("v14_integrity") for name in names):
        base.fail("v20 policy projection does not reach S1-014 predecessor module")
    if "wepld_harness_h0_spec_integrity" not in names:
        base.fail("v20 policy projection does not reach Harness H0 Spec Kit module")
    if "wepld_harness_research_integrity" not in names:
        base.fail("v20 policy projection does not reach Harness research module")


def patch_predecessor() -> None:
    current_wf = dict(v19.WF)
    if current_wf not in (V19_WF, dict(WF)):
        base.fail(f"v20 predecessor workflow identity map drifted: actual={current_wf}")
    current_traversal = _attr(v19, "_policy_descendants", "v19 policy traversal")
    if current_traversal not in (V19_POLICY_DESCENDANTS, _policy_modules):
        base.fail("v20 predecessor policy traversal drifted")
    _bind(v19, "WF", dict(WF), "v19 workflow identity projection")
    _bind(v19, "_policy_descendants", _policy_modules, "v19 policy-graph traversal repair")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v19(candidate)
            req_v19(policy_base)
            return
        if paths & BOOT:
            base.fail("v20 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v20 bootstrap base authorizes only exact policy/workflow activation")
    if P in paths:
        base.fail("canonical v20 wrapper is frozen after activation")
    _call("v19 exact-delta verifier", V19_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v19 base-control verifier", V19_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v20 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v20 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v20 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v20 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v19 extension verification", V19_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - {P}
    if remaining:
        _call("v19 allowed-path verifier", V19_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v19(view)
    _call("v19 policy-file verification", V19_FILES, view)
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v20 wrapper mode invalid")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V19_PRINT:
        base.fail("v20 predecessor printer drifted")
    _call("v19 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v20=V19_PLUS_POLICY_GRAPH_ROOT_PROJECTION_REPAIR")
    print(f"s1_admission_authority_expansion_v20={AUTH}")
    print(f"s1_016_authority_v20={S1_016}")
    print(f"s2_authority_v20={S2}")
    print(f"roadmap_mutation_authority_v20={ROADMAP}")
    print("effective_source_admission_v20=NONE")
    print("effective_dependency_admission_v20=NONE")
    print("new_product_runtime_authority_v20=NONE")
    print("effective_model_provider_execution_v20=NONE")


def overlay() -> None:
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v20 installed overlay drifted")
    if dict(v19.WF) != dict(WF):
        base.fail("v20 workflow identity projection drifted")
    if _attr(v19, "_policy_descendants", "v19 repaired traversal") is not _policy_modules:
        base.fail("v20 policy-graph traversal repair drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v19 install", getattr(v19, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V19_DELTA),
        (base.compare_base_controlled, V19_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V19_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V19_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V19_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V19_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V19_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v20 predecessor hook drifted")
    _PRINT = V19_PRINT
    _EXPECTED_DESKTOP_EXTENSIONS = frozenset(set(extset(desktop)) | {P})
    _EXPECTED_EXECUTION_EXTENSIONS = frozenset(set(extset(execution)) | {P})
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_DESKTOP_EXTENSIONS, "desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", _EXPECTED_EXECUTION_EXTENSIONS, "execution registration")
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


def selftest() -> None:
    patch_predecessor()
    _policy_graph_regression()
    _call("v19 predecessor self-test", getattr(v19, "selftest", None))
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v20 workflow drifted: {path}")
    if AUTH != "S1_016_ACCEPTED_STATE_POLICY_GRAPH_PROJECTION_REPAIR_ONLY":
        base.fail("v20 repair authority drifted")
    if (
        S1_016 != "EXACT_V19_DELEGATED_TRANSITION_ONLY"
        or S2 != "NOT_AUTHORIZED"
        or ROADMAP != "NOT_AUTHORIZED"
    ):
        base.fail("v20 authority boundary drifted")
    if TRUSTED_BASE_V19_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":  # noqa: S105
        base.fail("v20 bootstrap status semantics drifted")

    vb = root.read_bytes(V19, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V19: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v20", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v20 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    print("wepld S1 steady-state routing v20 policy-graph projection-repair self-tests: PASS")


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
                    CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
