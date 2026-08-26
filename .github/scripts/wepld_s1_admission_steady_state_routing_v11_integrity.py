#!/usr/bin/env python3
"""Repair S1-013 closeout compatibility with frozen Harness ledger checks.

v11 is an append-only successor to canonical v10. It preserves the exact
content-addressed S1-013 closeout authorized by v10 and changes no Harness,
runtime, source, dependency, provider, or S1-014 authority.

The repair is deliberately narrow: inherited Harness research/H0 policy may
recognize the canonical S1 ledger in exactly two states:

1. pre-closeout ledger d331... with no S1-013 evidence file; or
2. closeout ledger f8d9... with the exact v10-pinned S1-013 evidence blob.

Any other ledger/evidence combination fails closed. Original Harness research
document checks and all descendant H0 policy checks still run unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any, Callable

import wepld_integrity as base

P = ".github/scripts/wepld_s1_admission_steady_state_routing_v11_integrity.py"
V10 = ".github/scripts/wepld_s1_admission_steady_state_routing_v10_integrity.py"
V10_BLOB = "d1e585ee063dbc4dfe0a13591438916c6c043c30"
HR = ".github/scripts/wepld_harness_research_integrity.py"
HR_BLOB = "f62e57b5f4ca702fd37525a81bd3fd303944b584"
H0 = ".github/scripts/wepld_harness_h0_spec_integrity.py"
H0_BLOB = "6e08d9e8bbb67903ba11a8157f45f32fdbfb0f7a"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
CW = ".github/workflows/s1-contracts.yml"
TASKS = "specs/001-desktop-rust-trusted-core-handshake/tasks.md"
EVID = "specs/001-desktop-rust-trusted-core-handshake/s1-013-performance-evidence.md"

OLD_WF = {
    FW: "97d6f3bc5c6f668ebaa795f144e979c25b443fa3cc4d06d894e6d4a3a2f52f94",
    AW: "faa5c2c528378397117b6acaa5a8ed3ec23a51005b7d442e86d4cd9aa02e0273",
}
WF = {
    FW: "b26645b136df346a2563dcf5d18d875efc66c7e637e3929bfd521e76f152ecdc",
    AW: "f84d843d050e144bd96e668137568047fb8ba120e204a3338ac766651f25633f",
    CW: "008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7",
}

PRE_TASKS = "d331b7f167fe67ae9061ed553cf0949fab12aae0"
CLOSE_TASKS = "f8d9d09dc2e02861246614f374173a0a2bfff9c2"
EVID_BLOB = "bd79c1e64b397fda3677fb549e9a7feb0c5a8c3d"

BOOT = frozenset({P, FW, AW})
AUTH = "S1_013_CLOSEOUT_HARNESS_LEDGER_COMPATIBILITY_REPAIR_ONLY"
S1_014 = "NOT_AUTHORIZED"
TRUSTED_BASE_V10_CLASS = "EXPECTED_BOOTSTRAP_FAILURE"
OLD_BASE_S1_PASS = "NO"

_INST = False
_PRINT: Any = None
_COMPAT = False


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


def _call(label: str, function: Any, *args: Any, **kwargs: Any) -> Any:
    if not callable(function):
        base.fail(f"v11 {label} drifted: not callable")
    try:
        return function(*args, **kwargs)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v11 {label} topology/layout drifted: {exc}")


def _attr(obj: Any, name: str, label: str) -> Any:
    try:
        return getattr(obj, name)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v11 {label} topology/layout drifted: {exc}")


def _bind(obj: Any, name: str, value: Any, label: str) -> None:
    try:
        setattr(obj, name, value)
    except (AttributeError, TypeError) as exc:
        base.fail(f"v11 {label} topology/layout drifted: {exc}")


root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _require_local(path: str, expected: str, label: str) -> None:
    actual = blob(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
    if actual != expected:
        base.fail(f"{label} drifted before import: expected={expected} actual={actual}")


_require_local(V10, V10_BLOB, "frozen v10 predecessor")
_require_local(HR, HR_BLOB, "frozen Harness research policy")
_require_local(H0, H0_BLOB, "frozen Harness H0 Spec Kit policy")

import wepld_s1_admission_steady_state_routing_v10_integrity as v10  # noqa: E402
import wepld_harness_research_integrity as hr  # noqa: E402
import wepld_harness_h0_spec_integrity as h0  # noqa: E402

V10_DELTA = v10.delta
V10_BASE = v10.basectrl
V10_ALLOWED = v10.allowed
V10_FILES = v10.files
V10_DEXT = v10.dext
V10_EEXT = v10.eext
V10_EXT = v10.ext
V10_PRINT = v10.printer
V10_WF = dict(v10.WF)
CAND = v10.CAND
RUNTIME = v10.RUNTIME

HR_LEDGER = hr._require_reconciled_ledger_base
H0_BASE = h0._require_canonical_h0_base
HR_EXPECTED_LEDGER = hr.EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1


def req_v10(view: Any) -> None:
    if V10 not in ps(view):
        base.fail("v11 candidate/base is missing frozen v10 predecessor")
    actual = blob(view.read_bytes(V10, base.MAX_POLICY_FILE_BYTES))
    if actual != V10_BLOB:
        base.fail(f"frozen v10 predecessor drifted: expected={V10_BLOB} actual={actual}")


def topo() -> tuple[Any, Any, Any, Any, Any]:
    value = _call("topology", getattr(v10, "topo", None))
    if not isinstance(value, tuple) or len(value) != 5:
        base.fail("v11 topology drifted")
    return value


def extset(component: Any) -> frozenset[str]:
    value = _attr(component, "EXTENSION_CONTROLLED_PATHS", "extension-path set")
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v11 extension topology drifted")
    return frozenset(value)


def changed(candidate: Any, policy_base: Any) -> frozenset[str]:
    value = _call("changed-path", getattr(v10, "changed", None), candidate, policy_base)
    if not isinstance(value, (set, frozenset)) or any(not isinstance(path, str) for path in value):
        base.fail("v11 changed-path topology drifted")
    return frozenset(value)


def bootbase(view: Any) -> bool:
    return P not in ps(view)


def _ledger_state(view: Any, hasher: Callable[[bytes], str]) -> str:
    paths = ps(view)
    if TASKS not in paths:
        base.fail("S1-013/Harness compatibility requires canonical S1 ledger")

    actual = hasher(view.read_bytes(TASKS, base.MAX_POLICY_FILE_BYTES))
    if actual == PRE_TASKS:
        if EVID in paths:
            base.fail("pre-closeout S1 ledger must not contain S1-013 closeout evidence")
        return PRE_TASKS

    if actual == CLOSE_TASKS:
        if EVID not in paths:
            base.fail("closed S1-013 ledger requires exact closeout evidence")
        if mode(view, TASKS) != "100644" or mode(view, EVID) != "100644":
            base.fail("S1-013 closeout ledger/evidence mode invalid")
        evidence = hasher(view.read_bytes(EVID, base.MAX_POLICY_FILE_BYTES))
        if evidence != EVID_BLOB:
            base.fail(
                "S1-013 closeout evidence identity drifted: "
                f"expected={EVID_BLOB} actual={evidence}"
            )
        return CLOSE_TASKS

    base.fail(
        "S1-013/Harness compatibility rejects unknown S1 ledger: "
        f"actual={actual}"
    )


def _with_expected_ledger(expected: str, function: Any, view: Any, label: str) -> None:
    prior = hr.EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1
    if prior != HR_EXPECTED_LEDGER:
        base.fail(
            "Harness reconciled-ledger constant drifted before compatibility call: "
            f"expected={HR_EXPECTED_LEDGER} actual={prior}"
        )
    hr.EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1 = expected
    try:
        _call(label, function, view)
    finally:
        hr.EXPECTED_RECONCILED_LEDGER_GIT_BLOB_SHA1 = prior


def _compat_hr_ledger(view: Any) -> None:
    expected = _ledger_state(view, hr._git_blob_sha1)
    _with_expected_ledger(expected, HR_LEDGER, view, "Harness research ledger verifier")


def _compat_h0_base(view: Any) -> None:
    expected = _ledger_state(view, h0._git_blob_sha1)
    _with_expected_ledger(expected, H0_BASE, view, "Harness H0 base verifier")


def patch_workflows() -> None:
    expected = {FW: OLD_WF[FW], AW: OLD_WF[AW], CW: WF[CW]}
    current = dict(v10.WF)
    if current not in (expected, dict(WF)):
        base.fail(f"v11 predecessor workflow identity map drifted: actual={current}")
    _bind(v10, "WF", dict(WF), "v10 workflow identity projection")


def patch_compat() -> None:
    global _COMPAT
    if _COMPAT:
        if hr._require_reconciled_ledger_base is not _compat_hr_ledger:
            base.fail("v11 Harness research compatibility hook drifted")
        if h0._require_canonical_h0_base is not _compat_h0_base:
            base.fail("v11 Harness H0 compatibility hook drifted")
        return

    if hr._require_reconciled_ledger_base is not HR_LEDGER:
        base.fail("v11 Harness research ledger verifier identity drifted")
    if h0._require_canonical_h0_base is not H0_BASE:
        base.fail("v11 Harness H0 base verifier identity drifted")

    hr._require_reconciled_ledger_base = _compat_hr_ledger
    h0._require_canonical_h0_base = _compat_h0_base
    _COMPAT = True


def delta(candidate: Any, policy_base: Any) -> None:
    paths = changed(candidate, policy_base)
    if bootbase(policy_base):
        if paths == BOOT:
            req_v10(candidate)
            req_v10(policy_base)
            return
        if paths & BOOT:
            base.fail("v11 bootstrap delta must be exactly policy plus two workflows")
    _call("v10 exact-delta verifier", V10_DELTA, candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        _call("v10 base-control verifier", V10_BASE, candidate, policy_base)
        return

    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if sha(candidate_bytes) != WF[path] or sha(base_bytes) != OLD_WF[path]:
                base.fail(f"v11 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    if P in safe_paths:
        if P not in ps(candidate):
            base.fail("v11 wrapper missing")
        if bootbase(policy_base):
            if P in ps(policy_base):
                base.fail("v11 wrapper unexpectedly in bootstrap base")
        elif P not in ps(policy_base) or candidate.read_bytes(
            P, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(P, base.MAX_POLICY_FILE_BYTES):
            base.fail("v11 steady-state wrapper drifted")

    rest = frozenset(safe_paths - {P})
    if rest:
        _call("v10 extension verification", V10_EXT, candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, extset(topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    _call("v10 allowed-path verification", V10_ALLOWED, set(paths) - {P}, stage)


def files(view: Any) -> None:
    req_v10(view)
    _call("v10 policy-file verification", V10_FILES, view)
    if P not in ps(view):
        base.fail("v11 wrapper missing")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V10_PRINT:
        base.fail("v11 predecessor printer drifted")
    _call("v10 success printer", _PRINT, stage, mode_)
    print("s1_admission_steady_state_route_v11=V10_PLUS_HARNESS_LEDGER_COMPATIBILITY")
    print(f"s1_admission_authority_expansion_v11={AUTH}")
    print("s1_013_pre_closeout_ledger_v11=EXACT_D331_WITHOUT_EVIDENCE")
    print("s1_013_post_closeout_ledger_v11=EXACT_F8D9_WITH_EXACT_EVIDENCE")
    print("harness_research_authority_expansion_v11=NONE")
    print("harness_h0_authority_expansion_v11=NONE")
    print("effective_source_admission_v11=NONE")
    print("effective_dependency_admission_v11=NONE")
    print("effective_donor_execution_v11=NONE")
    print("new_product_runtime_authority_v11=NONE")
    print("effective_model_provider_execution_v11=NONE")
    print("effective_model_weight_access_v11=NONE")
    print("effective_model_inference_v11=NONE")
    print(f"s1_014_plus_v11={S1_014}")


def install() -> None:
    global _INST, _PRINT
    if _INST:
        patch_compat()
        return

    patch_compat()
    patch_workflows()
    _call("v10 install", getattr(v10, "install", None))
    shell, routing, _, desktop, execution = topo()

    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing exact-delta hook"), V10_DELTA),
        (base.compare_base_controlled, V10_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop extension hook"), V10_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "execution extension hook"), V10_EEXT),
        (_attr(shell, "validate_allowed_paths", "shell allowed-path hook"), V10_ALLOWED),
        (_attr(shell, "verify_policy_files", "shell policy-file hook"), V10_FILES),
        (_attr(shell, "print_success", "shell success hook"), V10_PRINT),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v11 predecessor hook drifted")

    _PRINT = V10_PRINT
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        frozenset(set(extset(desktop)) | {P}),
        "desktop extension registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        frozenset(set(extset(execution)) | {P}),
        "execution extension registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "routing exact-delta binding")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "desktop extension hook binding")
    _bind(execution, "verify_extension_controlled_paths", eext, "execution extension hook binding")
    _bind(shell, "validate_allowed_paths", allowed, "shell allowed-path hook binding")
    _bind(shell, "verify_policy_files", files, "shell policy-file hook binding")
    _bind(shell, "print_success", printer, "shell success hook binding")
    _INST = True


def mem(values: dict[str, bytes]) -> Any:
    return base.MemoryView(values, trees={path: blob(data) for path, data in values.items()})


def _selftest_ledger_compatibility() -> None:
    pre = b"pre-ledger"
    close = b"close-ledger"
    evidence = b"close-evidence"
    other = b"other-ledger"
    mapping = {
        pre: PRE_TASKS,
        close: CLOSE_TASKS,
        evidence: EVID_BLOB,
        other: "1" * 40,
    }
    original_hr = hr._git_blob_sha1
    original_h0 = h0._git_blob_sha1

    def fake(data: bytes) -> str:
        if data in mapping:
            return mapping[data]
        return original_hr(data)

    try:
        hr._git_blob_sha1 = fake
        h0._git_blob_sha1 = fake

        if _ledger_state(mem({TASKS: pre}), hr._git_blob_sha1) != PRE_TASKS:
            base.fail("v11 pre-closeout ledger compatibility self-test failed")
        if _ledger_state(
            mem({TASKS: close, EVID: evidence}), hr._git_blob_sha1
        ) != CLOSE_TASKS:
            base.fail("v11 closeout ledger compatibility self-test failed")

        base.expect_failure_matching(
            "v11 pre-closeout evidence prohibition",
            "must not contain",
            _ledger_state,
            mem({TASKS: pre, EVID: evidence}),
            hr._git_blob_sha1,
        )
        base.expect_failure_matching(
            "v11 closeout missing evidence",
            "requires exact closeout evidence",
            _ledger_state,
            mem({TASKS: close}),
            hr._git_blob_sha1,
        )
        base.expect_failure_matching(
            "v11 unknown ledger",
            "rejects unknown",
            _ledger_state,
            mem({TASKS: other}),
            hr._git_blob_sha1,
        )

        h0_files = {TASKS: close, EVID: evidence}
        for index, (path, expected) in enumerate(sorted(hr.RESEARCH_DOC_BLOBS.items()), start=1):
            data = f"research-{index}".encode("ascii")
            h0_files[path] = data
            mapping[data] = expected
        _compat_h0_base(mem(h0_files))
    finally:
        hr._git_blob_sha1 = original_hr
        h0._git_blob_sha1 = original_h0


def selftest() -> None:
    patch_compat()
    patch_workflows()
    _call("v10 self-test", getattr(v10, "selftest", None))
    install()

    for path in (FW, AW):
        if sha(root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != WF[path]:
            base.fail(f"v11 workflow drifted: {path}")

    if AUTH != "S1_013_CLOSEOUT_HARNESS_LEDGER_COMPATIBILITY_REPAIR_ONLY":
        base.fail("v11 authority drifted")
    if S1_014 != "NOT_AUTHORIZED":
        base.fail("v11 S1-014 boundary drifted")
    if TRUSTED_BASE_V10_CLASS != "EXPECTED_BOOTSTRAP_FAILURE" or OLD_BASE_S1_PASS != "NO":
        base.fail("v11 bootstrap status semantics drifted")

    vb = root.read_bytes(V10, base.MAX_POLICY_FILE_BYTES)
    policy_base = {V10: vb, FW: b"old-foundation", AW: b"old-admission"}
    candidate = dict(policy_base)
    candidate.update({P: b"v11", FW: b"new-foundation", AW: b"new-admission"})
    delta(mem(candidate), mem(policy_base))

    mixed = dict(candidate)
    mixed["README.md"] = b"x"
    base.expect_failure_matching(
        "v11 mixed bootstrap",
        "bootstrap delta must be exactly",
        delta,
        mem(mixed),
        mem(policy_base),
    )

    _selftest_ledger_compatibility()
    print("wepld S1 steady-state routing v11 policy self-tests: PASS")


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
