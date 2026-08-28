#!/usr/bin/env python3
"""Grant exact S2 Spec Kit planning authority only; preserve all implementation denials.

v21 is an append-only successor to canonical v20. It authorizes exactly the
planning artifact surface for S2 — Open Project + Project Doctor + local
identity/storage — while preserving v20's closed source, dependency, product
runtime, provider/model, roadmap-mutation, and effect boundaries.

The bootstrap transition is exactly:
- this v21 policy file;
- foundation-integrity.yml;
- s1-admission-integrity.yml.

After canonical activation, an S2 planning candidate may create the exact
Spec Kit package, or later repair files inside that already-canonical package.
Any mixed product/runtime/source/dependency change fails closed.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_planning_bootstrap_v21_integrity.py"
V20 = ".github/scripts/wepld_s1_admission_steady_state_routing_v20_integrity.py"
V20_BLOB = "3d1f62a6938c3024f119a2a69cd79a4f4a977914"
FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"

S2_DIR = "specs/005-s2-open-project-doctor-local-identity-storage"
S2_FILES = frozenset(
    {
        f"{S2_DIR}/constitution.md",
        f"{S2_DIR}/spec.md",
        f"{S2_DIR}/clarify.md",
        f"{S2_DIR}/plan.md",
        f"{S2_DIR}/checklists/requirements.md",
        f"{S2_DIR}/analyze.md",
        f"{S2_DIR}/tasks.md",
        f"{S2_DIR}/ponytail.md",
        f"{S2_DIR}/source-acquisition.md",
        f"{S2_DIR}/threat-model.md",
        f"{S2_DIR}/acceptance.md",
    }
)
S2_PREFIX = f"{S2_DIR}/"

OLD_WF = {
    FW: "fdbebf7b904f99c2ac02a941a361e6b7bcc443bd9958faebc5d64ea585d276bb",
    AW: "a8284f5f2d603fe12c7e1bcae9f36762d6776684fd3c6fd85acf86c0dbb6db56",
}
WF = {
    FW: "4099ae529de9be5fb653f07e11267e6910f9d2ec05ab40e0775b59d039a845fb",
    AW: "5a8305aca0f10619f6c5dc78c88682ca3cade46d43420da5c76048ba7260c716",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

BOOT = frozenset({P, FW, AW})
AUTH = "S2_PLANNING_ONLY_SUCCESSOR"
S2_PLANNING_AUTHORITY = "EXACT_SPEC_KIT_PACKAGE_ONLY"
S2_IMPLEMENTATION_AUTHORITY = "NOT_GRANTED"
SOURCE_ADMISSION = "NONE"
DEPENDENCY_ADMISSION = "NONE"
PRODUCT_RUNTIME_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
ROADMAP_MUTATION = "NONE"

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
        base.fail(f"v21 {label} drifted: not callable")
    try:
        return fn(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v21 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v21 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v21 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V20, base.MAX_POLICY_FILE_BYTES)) != V20_BLOB:
    base.fail("frozen v20 predecessor drifted")

import wepld_s1_admission_steady_state_routing_v20_integrity as v20  # noqa: E402

V20_DELTA = v20.delta
V20_BASE = v20.basectrl
V20_ALLOWED = v20.allowed
V20_FILES = v20.files
V20_DEXT = v20.dext
V20_EEXT = v20.eext
V20_EXT = v20.ext
V20_PRINT = v20.printer
V20_WF = dict(v20.WF)
CAND = v20.CAND
RUNTIME = v20.RUNTIME

if V20_WF != {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}:
    base.fail(f"v20 workflow identities drifted before v21 import: actual={V20_WF}")
if _attr(v20, "AUTH", "v20 authority marker") != "S1_016_ACCEPTED_STATE_FRESH_LOCAL_VIEW_PROJECTION_REPAIR_ONLY":
    base.fail("v21 observed v20 authority drift")
if _attr(v20, "S2", "v20 S2 boundary") != "NOT_AUTHORIZED":
    base.fail("v21 observed v20 S2 boundary drift")
if _attr(v20, "ROADMAP", "v20 roadmap boundary") != "NOT_AUTHORIZED":
    base.fail("v21 observed v20 roadmap boundary drift")


def req_v20(view: Any) -> None:
    if V20 not in ps(view):
        base.fail("v21 candidate/base is missing frozen v20 predecessor")
    actual = blob(view.read_bytes(V20, base.MAX_POLICY_FILE_BYTES))
    if actual != V20_BLOB:
        base.fail(f"frozen v20 predecessor drifted: expected={V20_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v20, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v21 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v21 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v20, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v21 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _s2_presence(view: Any) -> frozenset[str]:
    paths = ps(view)
    return frozenset(path for path in S2_FILES if path in paths)


def _verify_s2_files(view: Any) -> None:
    paths = ps(view)
    unknown = {path for path in paths if path.startswith(S2_PREFIX) and path not in S2_FILES}
    if unknown:
        base.fail(f"v21 S2 planning package contains unauthorized paths: {sorted(unknown)}")
    for path in sorted(S2_FILES & paths):
        if mode(view, path) != "100644":
            base.fail(f"v21 S2 planning file mode invalid: {path}")
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if not data:
            base.fail(f"v21 S2 planning file must be non-empty: {path}")
        if b"\x00" in data:
            base.fail(f"v21 S2 planning file contains NUL bytes: {path}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            base.fail(f"v21 S2 planning file is not UTF-8: {path}")


def patch_predecessor() -> None:
    current_wf = dict(v20.WF)
    if current_wf not in (V20_WF, dict(WF)):
        base.fail(f"v21 predecessor workflow identity map drifted: actual={current_wf}")
    _bind(v20, "WF", dict(WF), "v20 workflow identity projection")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v20(candidate)
            req_v20(policy_base)
            return
        if paths & BOOT:
            base.fail("v21 bootstrap delta must be exactly policy plus two workflows")
        base.fail("v21 bootstrap base authorizes only exact policy/workflow activation")

    if P in paths:
        base.fail("canonical v21 wrapper is frozen after activation")

    req_v20(candidate)
    req_v20(policy_base)

    unauthorized_s2 = {path for path in paths if path.startswith(S2_PREFIX) and path not in S2_FILES}
    if unauthorized_s2:
        base.fail(f"v21 unauthorized S2 planning path: {sorted(unauthorized_s2)}")

    s2_changed = frozenset(paths & S2_FILES)
    if s2_changed:
        if paths != s2_changed:
            base.fail("v21 S2 planning delta must not mix with any non-planning change")

        base_presence = _s2_presence(policy_base)
        candidate_presence = _s2_presence(candidate)

        if not base_presence:
            if s2_changed != S2_FILES or candidate_presence != S2_FILES:
                base.fail("v21 initial S2 planning delta must create the exact complete Spec Kit package")
        elif base_presence == S2_FILES:
            if candidate_presence != S2_FILES:
                base.fail("v21 canonical S2 planning package files may not be deleted")
        else:
            base.fail("v21 predecessor contains a partial S2 planning package")

        _verify_s2_files(candidate)
        return

    _call("v20 exact-delta verifier", V20_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v20 base-control verifier", V20_BASE, candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        cb = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        bb = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(cb) != WF[path] or sha(bb) != OLD_WF[path]:
                base.fail(f"v21 bootstrap workflow drifted: {path}")
        elif cb != bb:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v21 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v21 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v21 steady-state wrapper drifted")
    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v20 extension verification", V20_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    path_set = set(paths)
    unauthorized_s2 = {path for path in path_set if path.startswith(S2_PREFIX) and path not in S2_FILES}
    if unauthorized_s2:
        base.fail(f"v21 unauthorized S2 path in allowlist evaluation: {sorted(unauthorized_s2)}")
    remaining = path_set - {P} - set(S2_FILES)
    if remaining:
        _call("v20 allowed-path verifier", V20_ALLOWED, remaining, stage)


def files(view: Any) -> None:
    req_v20(view)
    _call("v20 policy-file verification", V20_FILES, view)
    if P in ps(view) and mode(view, P) != "100644":
        base.fail("v21 wrapper mode invalid")
    _verify_s2_files(view)


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V20_PRINT:
        base.fail("v21 predecessor printer drifted")
    _call("v20 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v21=V20_PLUS_S2_SPEC_KIT_PLANNING_ONLY")
    print(f"v21_authority={AUTH}")
    print(f"s2_planning_authority_v21={S2_PLANNING_AUTHORITY}")
    print(f"s2_implementation_authority_v21={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"source_admission_v21={SOURCE_ADMISSION}")
    print(f"dependency_admission_v21={DEPENDENCY_ADMISSION}")
    print(f"product_runtime_authority_v21={PRODUCT_RUNTIME_AUTHORITY}")
    print(f"model_provider_execution_v21={MODEL_PROVIDER_EXECUTION}")
    print(f"roadmap_mutation_v21={ROADMAP_MUTATION}")


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
        base.fail("v21 installed overlay drifted")
    if dict(v20.WF) != dict(WF):
        base.fail("v21 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return
    patch_predecessor()
    _call("v20 install", getattr(v20, "install", None))
    shell, routing, _, desktop, execution = topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "predecessor routing hook"), V20_DELTA),
        (base.compare_base_controlled, V20_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "predecessor desktop hook"), V20_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "predecessor execution hook"), V20_EEXT),
        (_attr(shell, "validate_allowed_paths", "predecessor allowed hook"), V20_ALLOWED),
        (_attr(shell, "verify_policy_files", "predecessor files hook"), V20_FILES),
        (_attr(shell, "print_success", "predecessor printer"), V20_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v21 predecessor hook drifted")
    _PRINT = V20_PRINT
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


def _fixture_docs() -> dict[str, bytes]:
    return {path: f"# v21 fixture: {path}\n".encode("utf-8") for path in S2_FILES}


def selftest() -> None:
    patch_predecessor()
    _call("v20 predecessor self-test", getattr(v20, "selftest", None))
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v21 workflow drifted: {path}")

    if (
        AUTH != "S2_PLANNING_ONLY_SUCCESSOR"
        or S2_PLANNING_AUTHORITY != "EXACT_SPEC_KIT_PACKAGE_ONLY"
        or S2_IMPLEMENTATION_AUTHORITY != "NOT_GRANTED"
        or SOURCE_ADMISSION != "NONE"
        or DEPENDENCY_ADMISSION != "NONE"
        or PRODUCT_RUNTIME_AUTHORITY != "NONE"
        or MODEL_PROVIDER_EXECUTION != "NONE"
        or ROADMAP_MUTATION != "NONE"
    ):
        base.fail("v21 authority boundary drifted")

    vb = root.read_bytes(V20, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V20: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v21", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed_bootstrap = dict(candidate)
    mixed_bootstrap["README.md"] = b"x"
    base.expect_failure_matching(
        "v21 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed_bootstrap),
        mem(policy_base),
    )

    steady_base = {V20: vb, P: b"v21"}
    initial = dict(steady_base)
    initial.update(_fixture_docs())
    delta(mem(initial), mem(steady_base))

    partial = dict(steady_base)
    one = sorted(S2_FILES)[0]
    partial[one] = b"# partial\n"
    base.expect_failure_matching(
        "v21 partial initial S2 package",
        "exact complete Spec Kit package",
        delta,
        mem(partial),
        mem(steady_base),
    )

    mixed = dict(initial)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v21 mixed S2 planning delta",
        "must not mix",
        delta,
        mem(mixed),
        mem(steady_base),
    )

    unknown = dict(steady_base)
    unknown[f"{S2_DIR}/src/main.rs"] = b"fn main() {}\n"
    base.expect_failure_matching(
        "v21 unknown S2 path",
        "unauthorized S2 planning path",
        delta,
        mem(unknown),
        mem(steady_base),
    )

    repair_base = dict(initial)
    repair = dict(repair_base)
    repair[one] = b"# repaired planning fixture\n"
    delta(mem(repair), mem(repair_base))

    deletion = dict(repair_base)
    del deletion[one]
    base.expect_failure_matching(
        "v21 S2 package deletion",
        "may not be deleted",
        delta,
        mem(deletion),
        mem(repair_base),
    )

    print("wepld v21 S2 planning-only successor self-tests: PASS")


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
