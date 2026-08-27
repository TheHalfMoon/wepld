#!/usr/bin/env python3
"""Repair accepted-S1 fresh local-view projection; grant no new product or S2 authority.

v20 is an append-only successor to canonical v19. The exact S1-016 candidate
proved that v19 correctly projects already-imported S1 predecessor roots, but
some inherited Harness policy self-tests construct a fresh LocalRepositoryView
for the canonical checkout. That fresh view bypasses v19's root projection and
observes the accepted task ledger instead of the exact pre-S1-016 ledger.

This repair temporarily projects only `tasks.md` for fresh LocalRepositoryView
instances whose root is the exact canonical checkout, and only while v19 runs
accepted-state inherited self-tests. Other roots and all other paths remain
unchanged. The original constructor is restored on success and failure.

v19's exact delegated S1-016 authority is preserved. S2, roadmap, source,
dependency, runtime, provider, model, and effect authority remain closed.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v20_integrity.py"
V19 = ".github/scripts/wepld_s1_admission_steady_state_routing_v19_integrity.py"
V19_BLOB = "be0504049258234e910c17e10622d2012316d95e"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"

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
AUTH = "S1_016_ACCEPTED_STATE_FRESH_LOCAL_VIEW_PROJECTION_REPAIR_ONLY"
S1_016 = "EXACT_V19_DELEGATED_TRANSITION_ONLY"
S2 = "NOT_AUTHORIZED"
ROADMAP = "NOT_AUTHORIZED"
TRUSTED_BASE_V19_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
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
REPOSITORY_ROOT = root.root
BASE_LOCAL_REPOSITORY_VIEW = base.LocalRepositoryView
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
V19_PROJECTED_SELFTEST = v19._projected_v18_selftest
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


def _projected_v19_predecessor_selftest(view: Any) -> None:
    v18 = _attr(v19, "v18", "v19 v18 predecessor module")
    current = _call("v18 state classifier", getattr(v18, "state", None), view)
    if current == "PRE_S1_016":
        _call("v19 predecessor projection", V19_PROJECTED_SELFTEST, view)
        return
    if current != "ACCEPTED_S1":
        base.fail(f"v20 observed unknown v18 state: {current}")

    predecessor = _call(
        "v18 accepted-ledger reversal",
        getattr(v18, "reverse_tasks", None),
        view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES),
    )
    prior_local_view = base.LocalRepositoryView
    if prior_local_view is not BASE_LOCAL_REPOSITORY_VIEW:
        base.fail("v20 LocalRepositoryView constructor drifted before accepted-state projection")

    class _AcceptedStateLocalRepositoryView(BASE_LOCAL_REPOSITORY_VIEW):
        def read_bytes(self, relative: str, limit: int) -> bytes:
            if self.root == REPOSITORY_ROOT and relative == TASKS:
                if len(predecessor) > limit:
                    base.fail("v20 projected S1 task ledger exceeds local-view read bound")
                return predecessor
            return super().read_bytes(relative, limit)

    base.LocalRepositoryView = _AcceptedStateLocalRepositoryView
    try:
        _call("v19 predecessor projection", V19_PROJECTED_SELFTEST, view)
    finally:
        base.LocalRepositoryView = prior_local_view


def patch_predecessor() -> None:
    current_wf = dict(v19.WF)
    if current_wf not in (V19_WF, dict(WF)):
        base.fail(f"v20 predecessor workflow identity map drifted: actual={current_wf}")
    current_projection = _attr(v19, "_projected_v18_selftest", "v19 projected selftest")
    if current_projection not in (V19_PROJECTED_SELFTEST, _projected_v19_predecessor_selftest):
        base.fail("v20 predecessor projected-selftest hook drifted")
    _bind(v19, "WF", dict(WF), "v19 workflow identity projection")
    _bind(
        v19,
        "_projected_v18_selftest",
        _projected_v19_predecessor_selftest,
        "v19 fresh-local-view projection repair",
    )


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
    print("s1_admission_steady_state_route_v20=V19_PLUS_FRESH_LOCAL_VIEW_PROJECTION_REPAIR")
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
    if _attr(v19, "_projected_v18_selftest", "v19 repaired projected selftest") is not _projected_v19_predecessor_selftest:
        base.fail("v20 fresh-local-view projection repair drifted")
    if base.LocalRepositoryView is not BASE_LOCAL_REPOSITORY_VIEW:
        base.fail("v20 LocalRepositoryView constructor leaked outside projection scope")


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


def _fresh_local_view_projection_regression() -> None:
    v18 = _attr(v19, "v18", "v19 v18 predecessor module")
    if _call("v18 state classifier", getattr(v18, "state", None), root) != "PRE_S1_016":
        return

    pre_tasks = root.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
    accepted_tasks = _call("v18 accepted-ledger builder", getattr(v18, "expected_tasks", None), pre_tasks)
    acceptance_path = _attr(v18, "ACCEPTANCE", "v18 acceptance path")
    learning_path = _attr(v18, "LEARNING", "v18 learning path")
    acceptance_fixture = b"v20 accepted-state acceptance fixture\n"
    learning_fixture = b"v20 accepted-state learning fixture\n"
    overlay_cls = _attr(v19, "_OverlayView", "v19 overlay view")
    accepted_view = overlay_cls(
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
    prior_local_view = base.LocalRepositoryView

    _bind(v18, "FINAL_ACCEPTANCE_BLOB", blob(acceptance_fixture), "v18 accepted fixture identity")
    _bind(v18, "FINAL_LEARNING_BLOB", blob(learning_fixture), "v18 learning fixture identity")
    try:
        if _call("v18 state classifier", getattr(v18, "state", None), accepted_view) != "ACCEPTED_S1":
            base.fail("v20 accepted-state fixture did not classify as ACCEPTED_S1")

        def success_probe() -> None:
            fresh = base.LocalRepositoryView(REPOSITORY_ROOT)
            observed = fresh.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
            if observed != pre_tasks:
                base.fail("v20 fresh local repository view did not project predecessor tasks")

        _bind(v18, "selftest", success_probe, "v18 fresh-view success probe")
        _projected_v19_predecessor_selftest(accepted_view)
        if base.LocalRepositoryView is not prior_local_view:
            base.fail("v20 success path did not restore LocalRepositoryView constructor")

        def fail_probe() -> None:
            fresh = base.LocalRepositoryView(REPOSITORY_ROOT)
            observed = fresh.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES)
            if observed != pre_tasks:
                base.fail("v20 failure probe did not project predecessor tasks")
            raise base.PolicyError("v20 fresh-local-view restoration sentinel")

        _bind(v18, "selftest", fail_probe, "v18 fresh-view failure probe")
        try:
            _projected_v19_predecessor_selftest(accepted_view)
        except base.PolicyError as exc:
            if str(exc) != "v20 fresh-local-view restoration sentinel":
                raise
        else:
            base.fail("v20 fresh-local-view failure probe unexpectedly succeeded")
        if base.LocalRepositoryView is not prior_local_view:
            base.fail("v20 failure path did not restore LocalRepositoryView constructor")
    finally:
        _bind(v18, "selftest", prior_v18_selftest, "v18 selftest restoration")
        _bind(v18, "FINAL_ACCEPTANCE_BLOB", prior_final_acceptance, "v18 final acceptance restoration")
        _bind(v18, "FINAL_LEARNING_BLOB", prior_final_learning, "v18 final learning restoration")
        base.LocalRepositoryView = prior_local_view


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def selftest() -> None:
    patch_predecessor()
    _fresh_local_view_projection_regression()
    _call("v19 predecessor self-test", getattr(v19, "selftest", None))
    install()
    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v20 workflow drifted: {path}")
    if AUTH != "S1_016_ACCEPTED_STATE_FRESH_LOCAL_VIEW_PROJECTION_REPAIR_ONLY":
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

    print("wepld S1 steady-state routing v20 fresh-local-view projection-repair self-tests: PASS")


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
