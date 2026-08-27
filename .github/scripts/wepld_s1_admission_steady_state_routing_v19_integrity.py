#!/usr/bin/env python3
"""Repair accepted-S1 predecessor self-test projection; grant no new product or S2 authority.

v19 is an append-only successor to canonical v18. It repairs only the
accepted-state self-test projection needed to let inherited S1 policy modules
observe the exact pre-S1-016 task ledger while v18 validates the accepted
three-file transition. It preserves v18's exact S1-016 authority and keeps S2,
roadmap, source, dependency, runtime, provider, model, and effect authority
closed.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v19_integrity.py"
V18 = ".github/scripts/wepld_s1_admission_steady_state_routing_v18_integrity.py"
V18_BLOB = "d004fbbee3d01f8c60c2edffaf9a3639277e3a76"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"

OLD_WF = {
    FW: "03d5356769c4d2db4e9d45c44a667681d61395aab87f8a8b814721b5ce98061f",
    AW: "aa35676a8526b12ab15e02cf998caa460b98b8326b0eb5d7dda5285f792f12c0",
}
WF = {
    FW: "f1de24d95ce654e1cd6de5618d556d76dd7d07165945fce96ff7a0e3a0722085",
    AW: "d96f36e574475e300ca38eb0590170d740554afb8e437704d61004b87a639016",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S1_016_ACCEPTED_STATE_SELFTEST_PROJECTION_REPAIR_ONLY"
S1_016 = "EXACT_V18_TRANSITION_ONLY"
S2 = "NOT_AUTHORIZED"
ROADMAP = "NOT_AUTHORIZED"
TRUSTED_BASE_V18_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
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
        base.fail(f"v19 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v19 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v19 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v19 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V18, base.MAX_POLICY_FILE_BYTES)) != V18_BLOB:
    base.fail("frozen v18 predecessor drifted")

import wepld_s1_admission_steady_state_routing_v18_integrity as v18  # noqa: E402

V18_DELTA = v18.delta
V18_BASE = v18.basectrl
V18_ALLOWED = v18.allowed
V18_FILES = v18.files
V18_DEXT = v18.dext
V18_EEXT = v18.eext
V18_EXT = v18.ext
V18_PRINT = v18.printer
V18_WF = dict(v18.WF)
CAND = v18.CAND
RUNTIME = v18.RUNTIME

if V18_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v18 workflow identities drifted before v19 import: actual={V18_WF}")
if _attr(v18, "AUTH", "v18 authority marker") != "S1_016_EXACT_ACCEPTANCE_AND_BUILD_LEARNING_ONLY":
    base.fail("v19 observed v18 authority drift")
if _attr(v18, "S2", "v18 S2 boundary") != "NOT_AUTHORIZED":
    base.fail("v19 observed v18 S2 boundary drift")


def req_v18(view: Any) -> None:
    if V18 not in ps(view):
        base.fail("v19 candidate/base is missing frozen v18 predecessor")
    actual = blob(view.read_bytes(V18, base.MAX_POLICY_FILE_BYTES))
    if actual != V18_BLOB:
        base.fail(f"frozen v18 predecessor drifted: expected={V18_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v18, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v19 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v19 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v18, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v19 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def patch_predecessor() -> None:
    current = dict(v18.WF)
    if current not in (V18_WF, dict(WF)):
        base.fail(f"v19 predecessor workflow identity map drifted: actual={current}")
    _bind(v18, "WF", dict(WF), "v18 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v18(candidate)
            req_v18(policy_base)
            return
        if paths & BOOT:
            base.fail("v19 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v19 bootstrap base authorizes only exact policy/workflow activation")
    if P in paths:
        base.fail("canonical v19 wrapper is frozen after activation")
    _call("v18 exact-delta verifier", V18_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v18 base-control verifier", V18_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v19 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v19 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v19 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v19 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v18 extension verification", V18_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - {P}
    if remaining:
        _call("v18 allowed-path verifier", V18_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v18(view)
    _call("v18 policy-file verification", V18_FILES, view)
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v19 wrapper mode invalid")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V18_PRINT:
        base.fail("v19 predecessor printer drifted")
    _call("v18 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v19=V18_PLUS_ACCEPTED_STATE_SELFTEST_PROJECTION_REPAIR")
    print(f"s1_admission_authority_expansion_v19={AUTH}")
    print(f"s1_016_authority_v19={S1_016}")
    print(f"s2_authority_v19={S2}")
    print(f"roadmap_mutation_authority_v19={ROADMAP}")
    print("effective_source_admission_v19=NONE")
    print("effective_dependency_admission_v19=NONE")
    print("new_product_runtime_authority_v19=NONE")
    print("effective_model_provider_execution_v19=NONE")


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
        base.fail("v19 installed overlay drifted")
    if dict(v18.WF) != dict(WF):
        base.fail("v19 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v18 install", getattr(v18, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V18_DELTA),
        (base.compare_base_controlled, V18_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V18_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V18_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V18_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V18_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V18_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v19 predecessor hook drifted")
    _PRINT = V18_PRINT
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


class _OverlayView:
    def __init__(self, view: Any, overrides: dict[str, bytes]) -> None:
        self._view = view
        self._overrides = dict(overrides)

    def entries(self) -> Any:
        return self._view.entries()

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._overrides:
            data = self._overrides[path]
            if len(data) > max_bytes:
                base.fail(f"v19 overlay fixture exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def tree_identity(self, path: str) -> str | None:
        return self._view.tree_identity(path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _policy_descendants(module: ModuleType) -> list[ModuleType]:
    stack = [module]
    seen: set[int] = set()
    result: list[ModuleType] = []
    while stack:
        current = stack.pop()
        identity = id(current)
        if identity in seen:
            continue
        seen.add(identity)
        if len(seen) > 64:
            base.fail("v19 predecessor module traversal exceeded bound")
        for value in vars(current).values():
            if not isinstance(value, ModuleType):
                continue
            name = getattr(value, "__name__", "")
            if not name.startswith("wepld_s1_"):
                continue
            if value is v18:
                continue
            stack.append(value)
        if current is not module and hasattr(current, "root"):
            result.append(current)
    return result


def _projected_v18_selftest(view: Any) -> None:
    patch_predecessor()
    current = _call("v18 state classifier", getattr(v18, "state", None), view)
    prior_v18_root = _attr(v18, "root", "v18 root")
    _bind(v18, "root", view, "v18 self-test root projection")
    modules: list[ModuleType] = []
    priors: list[tuple[ModuleType, Any]] = []
    try:
        if current == "PRE_S1_016":
            _call("v18 predecessor self-test", getattr(v18, "selftest", None))
            return
        if current != "ACCEPTED_S1":
            base.fail(f"v19 observed unknown v18 state: {current}")

        predecessor = _call(
            "v18 accepted-ledger reversal",
            getattr(v18, "reverse_tasks", None),
            view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES),
        )
        projection_cls = _attr(v18, "_TaskProjection", "v18 task projection class")
        projection = projection_cls(view, predecessor)
        modules = _policy_descendants(_attr(v18, "v17", "v18 v17 predecessor module"))
        for module in modules:
            prior = _attr(module, "root", f"{module.__name__} root")
            priors.append((module, prior))
            _bind(module, "root", projection, f"{module.__name__} accepted-state projection")
        _call("v18 predecessor self-test", getattr(v18, "selftest", None))
    finally:
        for module, prior in reversed(priors):
            _bind(module, "root", prior, f"{module.__name__} root restoration")
        _bind(v18, "root", prior_v18_root, "v18 root restoration")


def corrected_v18_selftest() -> None:
    _projected_v18_selftest(root)


def _accepted_state_projection_regression() -> None:
    if _call("v18 state classifier", getattr(v18, "state", None), root) != "PRE_S1_016":
        return

    pre_tasks = root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    accepted_tasks = _call("v18 accepted-ledger builder", getattr(v18, "expected_tasks", None), pre_tasks)
    acceptance_path = _attr(v18, "ACCEPTANCE", "v18 acceptance path")
    learning_path = _attr(v18, "LEARNING", "v18 learning path")
    acceptance_fixture = b"v19 accepted-state acceptance fixture\n"
    learning_fixture = b"v19 accepted-state learning fixture\n"
    accepted_view = _OverlayView(
        root,
        {
            TASKS: accepted_tasks,
            acceptance_path: acceptance_fixture,
            learning_path: learning_fixture,
        },
    )

    prior_final_acceptance = _attr(v18, "FINAL_ACCEPTANCE_BLOB", "v18 final acceptance identity")
    prior_final_learning = _attr(v18, "FINAL_LEARNING_BLOB", "v18 final learning identity")
    prior_v18_selftest = _attr(v18, "selftest", "v18 selftest")
    prior_v18_root = _attr(v18, "root", "v18 root")
    descendants = _policy_descendants(_attr(v18, "v17", "v18 v17 predecessor module"))
    descendant_priors = [(module, _attr(module, "root", f"{module.__name__} root")) for module in descendants]
    if not descendants or not any(module.__name__.endswith("v14_integrity") for module in descendants):
        base.fail("v19 accepted-state projection does not reach S1-014 predecessor module")

    _bind(v18, "FINAL_ACCEPTANCE_BLOB", blob(acceptance_fixture), "v18 accepted fixture identity")
    _bind(v18, "FINAL_LEARNING_BLOB", blob(learning_fixture), "v18 learning fixture identity")
    try:
        if _call("v18 state classifier", getattr(v18, "state", None), accepted_view) != "ACCEPTED_S1":
            base.fail("v19 accepted-state fixture did not classify as ACCEPTED_S1")

        _projected_v18_selftest(accepted_view)
        for module, prior in descendant_priors:
            if _attr(module, "root", f"{module.__name__} restored root") is not prior:
                base.fail(f"v19 accepted-state success path did not restore {module.__name__}.root")
        if _attr(v18, "root", "v18 restored root") is not prior_v18_root:
            base.fail("v19 accepted-state success path did not restore v18.root")

        def fail_probe() -> None:
            if _attr(v18, "root", "v18 projected root") is not accepted_view:
                base.fail("v19 failure probe did not observe accepted v18 root")
            for module, _prior in descendant_priors:
                observed = _attr(module, "root", f"{module.__name__} projected root").read_bytes(
                    TASKS, base.MAX_POLICY_FILE_BYTES
                )
                if observed != pre_tasks:
                    base.fail(f"v19 failure probe did not project predecessor tasks into {module.__name__}")
            raise base.PolicyError("v19 accepted-state restoration sentinel")

        _bind(v18, "selftest", fail_probe, "v18 failure-probe selftest")
        try:
            _projected_v18_selftest(accepted_view)
        except base.PolicyError as exc:
            if str(exc) != "v19 accepted-state restoration sentinel":
                raise
        else:
            base.fail("v19 accepted-state failure probe unexpectedly succeeded")

        for module, prior in descendant_priors:
            if _attr(module, "root", f"{module.__name__} failure-restored root") is not prior:
                base.fail(f"v19 accepted-state failure path did not restore {module.__name__}.root")
        if _attr(v18, "root", "v18 failure-restored root") is not prior_v18_root:
            base.fail("v19 accepted-state failure path did not restore v18.root")
    finally:
        _bind(v18, "selftest", prior_v18_selftest, "v18 selftest restoration")
        _bind(v18, "FINAL_ACCEPTANCE_BLOB", prior_final_acceptance, "v18 final acceptance restoration")
        _bind(v18, "FINAL_LEARNING_BLOB", prior_final_learning, "v18 final learning restoration")
        _bind(v18, "root", prior_v18_root, "v18 final root restoration")
        for module, prior in descendant_priors:
            _bind(module, "root", prior, f"{module.__name__} final root restoration")


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def selftest() -> None:
    corrected_v18_selftest()
    _accepted_state_projection_regression()
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v19 workflow drifted: {path}")
    if AUTH != "S1_016_ACCEPTED_STATE_SELFTEST_PROJECTION_REPAIR_ONLY":
        base.fail("v19 repair authority drifted")
    if S1_016 != "EXACT_V18_TRANSITION_ONLY" or S2 != "NOT_AUTHORIZED" or ROADMAP != "NOT_AUTHORIZED":
        base.fail("v19 authority boundary drifted")
    if TRUSTED_BASE_V18_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":  # noqa: S105
        base.fail("v19 bootstrap status semantics drifted")

    vb = root.read_bytes(V18, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V18: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v19", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))
    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v19 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    print("wepld S1 steady-state routing v19 projection-repair self-tests: PASS")


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