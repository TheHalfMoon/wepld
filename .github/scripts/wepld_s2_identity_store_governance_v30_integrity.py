#!/usr/bin/env python3
"""Repair the S2 dependency policy-file projection without widening authority.

Canonical v29 already authorizes exactly one governed S2-AUTH-012 dependency
transition (Core manifest, root lock, dependency register). Trusted run #660
proved an integration defect: v29 exact-delta accepts those bytes, but the
inherited policy-file verifier still observes the admitted Core manifest as a
frozen S1 manifest before the existing dependency/component seams are applied.

v30 changes policy verification only. For the exact governed admitted dependency
state, v30 first verifies the real manifest/lock/register bytes against the
content-addressed canonical v29 baseline transformation, then projects only those
three files back to their exact canonical baseline bytes for inherited
policy-file verification. Candidate delta, component verification, product
verification, state freeze, and all runtime authority continue to operate on the
real repository view.

No dependency, product, source, filesystem, process/Git, network, model/provider,
Doctor/CLI, or S3+ authority is added by this successor.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v29_integrity as p

P = ".github/scripts/wepld_s2_identity_store_governance_v30_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v30_selftest.py"
T_BLOB = "8f3d423957b4af3a3b5970c51f24ec35cbbab037"
V29_P_BLOB = "a3c55e8ecd7420794b1536239d1ebeac21f43e4f"
V29_T_BLOB = "38721c4c5bccc3716105e44a4aad2b0cec63cd69"

CORE_MANIFEST_BASE_BLOB = "22381d52678796f8cab1aedea0bf78100f3e5323"
ROOT_LOCK_BASE_BLOB = "29510dbc4554111770ddfae2a3840ef6432573d2"
DEPENDENCY_REGISTER_BASE_BLOB = "13e410d218b4ff07d81495124b6a00b632fb9879"

POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, p.s.r.q.p.FW, p.s.r.q.p.AW})

AUTH = "S2_IDENTITY_STORE_POLICY_FILE_PROJECTION_REPAIR_ONLY"
S2_IMPLEMENTATION_AUTHORITY = p.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = p.SOURCE_ADMISSION

P_WF = dict(p.WF)
WF = {
    p.s.r.q.p.FW: "258091af7edda9d78295b4dbdca8be6edef0e85c9c40169e98e72739755aec76",
    p.s.r.q.p.AW: "ef6bd65e8391a38b12dd69b8d08a2de346b6df3d5fee9e5679ee23de09b8f7ab",
    p.s.r.q.p.CW: p.WF[p.s.r.q.p.CW],
}

P_DELTA = p.delta
P_BASE = p.basectrl
P_EXT = p.ext
P_DEXT = p.dext
P_EEXT = p.eext
P_ALLOWED = p.allowed
P_FILES = p.files
P_PRINTER = p.printer

root = p.root
for _path, _expected in ((p.P, V29_P_BLOB), (p.T, V29_T_BLOB), (T, T_BLOB)):
    _actual = p.s.r.q.p.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v30 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = p._call
_attr = p._attr
_bind = p._bind
_INST = False
_PRINT: Any = None
_SHELL_COMPONENT_BASE: Any = None


def bootbase(view: Any) -> bool:
    return P not in p.s.r.q.p.ps(view)


def req_v29(view: Any) -> None:
    for path, expected in ((p.P, V29_P_BLOB), (p.T, V29_T_BLOB)):
        if path not in p.s.r.q.p.ps(view):
            base.fail(f"v30 candidate/base is missing frozen v29 predecessor: {path}")
        actual = p.s.r.q.p.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v29 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def prepare_p() -> None:
    current = dict(p.WF)
    if current not in (P_WF, dict(WF)):
        base.fail(f"v30 predecessor workflow identity map drifted: actual={current}")
    p.WF = dict(WF)
    p.s.WF = dict(WF)
    p.s.r.WF = dict(WF)
    p.s.r.q.WF = dict(WF)
    p.s.r.q.p.WF = dict(WF)


class _DependencyBaselineProjection:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v30 projected dependency file exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _require_git_blob(label: str, data: bytes, expected: str) -> None:
    actual = p.s.r.q.p.blob(data)
    if actual != expected:
        base.fail(
            f"v30 {label} does not reverse to exact canonical v29 baseline: "
            f"expected={expected} actual={actual}"
        )


def project_admitted_dependency_state(view: Any) -> Any:
    if not p.s.r.q.deps_ready(view):
        base.fail("v30 projection requires exact governed admitted dependency state")

    manifest_path = p.s.r.q.p.CORE_MANIFEST
    lock_path = p.s.r.q.p.ROOT_CARGO_LOCK
    register_path = p.s.r.q.DEPENDENCY_REGISTER

    manifest = view.read_bytes(manifest_path, base.MAX_POLICY_FILE_BYTES)
    if manifest != p.s.r.q.p.ADMITTED_CORE_MANIFEST:
        base.fail("v30 admitted Core manifest drifted before projection")
    baseline_manifest = p.s.r.q.p.BASE_CORE_MANIFEST
    _require_git_blob("Core manifest", baseline_manifest, CORE_MANIFEST_BASE_BLOB)

    lock_bytes = view.read_bytes(lock_path, p.s.r.q.p.MAX_LOCK_BYTES)
    admitted_stanza = p.s.r.q.p.ADMITTED_CORE_LOCK_STANZA
    baseline_stanza = p.s.r.q.p.BASE_CORE_LOCK_STANZA
    if lock_bytes.count(admitted_stanza) != 1 or baseline_stanza in lock_bytes:
        base.fail("v30 admitted Core lock stanza drifted before projection")
    baseline_lock = lock_bytes.replace(admitted_stanza, baseline_stanza, 1)
    if p.s.r.q.p.expected_admitted_lock(baseline_lock) != lock_bytes:
        base.fail("v30 admitted Cargo.lock is not the exact reversible v25 transition")
    _require_git_blob("Cargo.lock", baseline_lock, ROOT_LOCK_BASE_BLOB)

    register = view.read_bytes(register_path, base.MAX_POLICY_FILE_BYTES)
    append = p.CORRECTED_S2_DEPENDENCY_REGISTER_APPEND
    if register.count(append) != 1 or not register.endswith(append):
        base.fail("v30 admitted dependency register append drifted before projection")
    baseline_register = register[: -len(append)]
    if p.s.r.q.expected_admitted_register(baseline_register) != register:
        base.fail(
            "v30 admitted dependency register is not the exact reversible v29 transition"
        )
    _require_git_blob(
        "dependency register", baseline_register, DEPENDENCY_REGISTER_BASE_BLOB
    )

    return _DependencyBaselineProjection(
        view,
        {
            manifest_path: baseline_manifest,
            lock_path: baseline_lock,
            register_path: baseline_register,
        },
    )


def shell_component_base(view: Any, paths: Any) -> None:
    if _SHELL_COMPONENT_BASE is None:
        base.fail("v30 predecessor shell component-base verifier is not installed")
    target = view
    if p.s.r.q.deps_ready(view):
        target = project_admitted_dependency_state(view)
    _call("v29 shell component-base verifier", _SHELL_COMPONENT_BASE, target, paths)


def delta(candidate: Any, policy_base: Any) -> None:
    paths = p.s.r.q.p.changed(p.s.r.q.p.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths == BOOT:
            req_v29(candidate)
            req_v29(policy_base)
            if not p.s.r.q._baseline_dependency_state(
                candidate
            ) or not p.s.r.q._baseline_dependency_state(policy_base):
                base.fail(
                    "v30 bootstrap requires unchanged canonical baseline "
                    "manifest/lock/register state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v30 bootstrap delta must be exactly two v30 policy files "
                "plus two integrity workflows"
            )
        base.fail(
            "v30 bootstrap base authorizes only exact policy-file projection repair activation"
        )

    if paths & ALL_POLICY_FILES:
        base.fail("canonical v30/v29/v28/v27/v26/v25 policy files are frozen after activation")

    P_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        P_BASE(candidate, policy_base)
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (p.s.r.q.p.FW, p.s.r.q.p.AW):
            if (
                p.s.r.q.p.sha(candidate_bytes) != WF[path]
                or p.s.r.q.p.sha(base_bytes) != P_WF[path]
            ):
                base.fail(f"v30 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in p.s.r.q.p.ps(candidate):
            base.fail(f"v30 policy file missing: {path}")
        if bootbase(policy_base):
            if path in p.s.r.q.p.ps(policy_base):
                base.fail(f"v30 policy file unexpectedly in bootstrap base: {path}")
        elif path not in p.s.r.q.p.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v30 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        P_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, p.s.r.q.p.extset(p.s.r.q.p.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, p.s.r.q.p.extset(p.s.r.q.p.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES
    if remaining:
        P_ALLOWED(remaining, stage)


def files(view: Any) -> None:
    if p.s.r.q.deps_ready(view):
        P_FILES(project_admitted_dependency_state(view))
    elif p.s.r.q._baseline_dependency_state(view):
        P_FILES(view)
    else:
        base.fail(
            "v30 dependency state is neither exact canonical baseline "
            "nor exact governed admitted form"
        )

    missing = POLICY_FILES - p.s.r.q.p.ps(view)
    if missing:
        base.fail(f"v30 policy files missing: {sorted(missing)}")
    for path in sorted(POLICY_FILES):
        if p.s.r.q.p.mode(view, path) != "100644":
            base.fail(f"v30 policy file mode invalid: {path}")


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not P_PRINTER:
        base.fail("v30 predecessor printer drifted")
    _call("v29 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v30=DEPENDENCY_POLICY_FILE_PROJECTION_REPAIR_ONLY")
    print(f"v30_authority={AUTH}")
    print(f"s2_implementation_authority_v30={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v30={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v30={SOURCE_ADMISSION}")
    print("v30_real_candidate_delta_projection=NONE")
    print("v30_inherited_policy_file_projection=EXACT_THREE_DEPENDENCY_FILES_ONLY")


def overlay() -> None:
    shell, routing, _, desktop, execution = p.s.r.q.p.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(shell, "_verify_shell_component_base", "shell component-base hook"), shell_component_base),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v30 installed overlay drifted")
    if any(
        dict(module.WF) != dict(WF)
        for module in (p, p.s, p.s.r, p.s.r.q, p.s.r.q.p)
    ):
        base.fail("v30 workflow identity projection drifted")
    if p.s.r.q.S2_DEPENDENCY_REGISTER_APPEND != p.CORRECTED_S2_DEPENDENCY_REGISTER_APPEND:
        base.fail("v30 corrected dependency-register append projection drifted")


def install() -> None:
    global _INST, _PRINT, _SHELL_COMPONENT_BASE
    if _INST:
        overlay()
        return

    prepare_p()
    p.install()
    shell, routing, _, desktop, execution = p.s.r.q.p.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v29 routing hook"), P_DELTA),
        (base.compare_base_controlled, P_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "v29 desktop hook"), P_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v29 execution hook"), P_EEXT),
        (_attr(shell, "validate_allowed_paths", "v29 allowed hook"), P_ALLOWED),
        (_attr(shell, "verify_policy_files", "v29 files hook"), P_FILES),
        (_attr(shell, "print_success", "v29 printer"), P_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v30 predecessor hook drifted")

    _SHELL_COMPONENT_BASE = _attr(
        shell, "_verify_shell_component_base", "v29 shell component-base verifier"
    )
    _PRINT = P_PRINTER
    desktop_extensions = frozenset(
        set(p.s.r.q.p.extset(desktop)) | set(POLICY_FILES)
    )
    execution_extensions = frozenset(
        set(p.s.r.q.p.extset(execution)) | set(POLICY_FILES)
    )
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v30 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v30 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v30 routing hook")
    base.compare_base_controlled = basectrl
    _bind(
        shell,
        "_verify_shell_component_base",
        shell_component_base,
        "v30 shell component-base hook",
    )
    _bind(desktop, "verify_extension_controlled_paths", dext, "v30 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v30 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v30 allowed hook")
    _bind(shell, "verify_policy_files", files, "v30 files hook")
    _bind(shell, "print_success", printer, "v30 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v30_selftest import run

    run()


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
                    p.s.r.q.p.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", p.s.r.q.p.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
