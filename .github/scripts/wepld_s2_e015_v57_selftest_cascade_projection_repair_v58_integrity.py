#!/usr/bin/env python3
"""Extend v57's identity/store token-scan projection to the predecessor
self-test cascade.

v58 is an append-only policy successor over canonical v57 at main
076054bef80f12a8744338f874686d997c4e9576. It changes no product rule, grants no
new authority, widens no path, and admits nothing. Every v57 / v56 / v55
authority value is inherited by reference and asserted unchanged.

The gap. v57 rebinds `wepld_s2_identity_store_bootstrap_v25_integrity._verify_product_files`
(and v28's `_hardened_product_verify`) to `_v57_hardened_product_verify` inside
`install()`. That covers every runtime and admission path
(`verify-candidate-local`, `verify-remote`), but not the `selftest` entrypoint:
`v57_integrity.py selftest` runs `run()`, which runs the frozen predecessor
self-test cascade and then v57's own checks *before* `install()`. v56's frozen
`_check_v56_delta_and_files_freeze` calls `p.files(p.raw_root)`, which cascades
to the still-unprojected v28 scan. Once the S2-E015 fixture is canonical the
real tree holds `std::process` in `identity_store_v1.rs`, so
`foundation-integrity` on `main` would fail forever with
`v25 identity/store tranche contains unauthorized token: std::process` - exactly
the class of self-test-only gap v56 had for the frontier check.

The repair. v58 does NOT rebind `_verify_product_files` (pre-binding it would
trip v57's own `install()` consistency check, which asserts the installed hook
is still v28's). Instead - exactly as v56 does for the frontier pin - v58's
`run_predecessor_selftests` installs a `read_bytes` replacement that, for the
whole frozen v57 self-test `run()` (its cascade *and* its and v56's own
post-cascade `_check_*`), projects the reopened path's *bytes* back to their
exact pre-reopen form whenever the real tree already holds the authorized
post-reopen blob. The inherited v28 token scan then simply never observes
`std::process` in the tranche; `identity.rs` / `evidence_store.rs` and every
other path are read unchanged and stay fully scanned. The projection is only
ever applied for the exact authorized post-reopen blob, and is restored in
`finally`.

Invariant: `V58_POLICY_REPAIR != NEW_RUNTIME_AUTHORITY`.

Package-load / resting-view note: v58 follows the v45..v57 discipline. It owns a
fresh `LocalRepositoryView` of the exact checked-out head, imports frozen v57
under an exact v58->v57 workflow-entrypoint reversal, and inherits every v57
hook by reference.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_e015_v57_selftest_cascade_projection_repair_v58_integrity.py"
T = ".github/scripts/wepld_s2_e015_v57_selftest_cascade_projection_repair_v58_selftest.py"
T_BLOB = "8f5f2cc6a4ddac75c1f67c68685e300ec5dcd7b2"

V57_P_BLOB = "aaa97e34aaa98574727f53608a4828a4e0f54778"
V57_T_BLOB = "9dfe73d145ace7e96eb30583bcae2a4109167968"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V58_ENTRYPOINT = b"wepld_s2_e015_v57_selftest_cascade_projection_repair_v58_integrity.py"
_V57_ENTRYPOINT = b"wepld_s2_e015_reopen_token_scan_projection_repair_v57_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v57_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V58_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v58 workflow entrypoint count drifted before v57 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V58_ENTRYPOINT, _V57_ENTRYPOINT)


def _import_v57_under_workflow_projection() -> Any:
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v57_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v57_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v58 v57-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v57_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_e015_reopen_token_scan_projection_repair_v57_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v57_under_workflow_projection()

V25 = q.V25
CW = q.CW
Q_WF = dict(q.WF)
_attr = q._attr
_bind = q._bind
_call = q._call
_ProjectionView = q._ProjectionView
_INST = False
_PREDECESSOR_COMPONENT_BASE: Any = None
_PREDECESSOR_FREEZE_S1: Any = None

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(q.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

IDENTITY_STORE_TEST = q.IDENTITY_STORE_TEST
AUTHORIZED_POST_REOPEN_BLOB = q.AUTHORIZED_POST_REOPEN_BLOB

AUTH = "S2_E015_V57_SELFTEST_CASCADE_PROJECTION_REPAIR_ONLY"
V58_POLICY_REPAIR = "NOT_NEW_RUNTIME_AUTHORITY"
NEXT_AUTHORITY_GATE = "S2-ACCEPTANCE"

_INHERITED_AUTHORITY_NAMES = (
    "DEPENDENCY_ADMISSION",
    "SOURCE_ADMISSION",
    "GIT_ROUTE_DECISION",
    "GIT_PROCESS_ADMISSION",
    "EXTERNAL_PROCESS_AUTHORITY",
    "GIT_EXECUTION_AUTHORITY",
    "NETWORK_AUTHORITY",
    "MODEL_PROVIDER_EXECUTION",
    "DOCTOR_CLI_AUTHORITY",
    "S3_PLUS_AUTHORITY",
    "GENERAL_SHELL_AUTHORITY",
    "ARBITRARY_PROCESS_AUTHORITY",
    "PACKAGE_INSTALL_AUTHORITY",
    "PROJECT_NATIVE_COMMAND_EXECUTION",
    "GIT_MUTATION_AUTHORITY",
    "SAFE_DIRECTORY_MUTATION_AUTHORITY",
    "REMEDIATION_EXECUTION_AUTHORITY",
    "TEST_CHILD_PROCESS_AUTHORITY",
    "S2_IMPLEMENTATION_AUTHORITY",
    "GIT_TOPOLOGY_EVIDENCE_REOPEN_AUTHORITY",
)
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(q, _name)

for _path, _expected in ((q.P, V57_P_BLOB), (q.T, V57_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v58 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

import wepld_s2_identity_store_bootstrap_v25_integrity as _v25mod
import wepld_s2_identity_store_governance_v28_integrity as _v28mod

# v57's projected identity/store product verifier and v28's raw one - kept for
# reference/assertions only. v58 does NOT rebind either (v57's `install()`
# already does, and pre-binding would trip v57's own predecessor consistency
# check). v58 instead projects the reopened path's *bytes* back to PRE for the
# self-test cascade, so the inherited v28 scan simply never sees `std::process`.
_V57_HARDENED_PRODUCT_VERIFY = q._v57_hardened_product_verify
_V28_HARDENED = q._V28_HARDENED
if q._v25mod is not _v25mod or q._v28mod is not _v28mod:
    base.fail("v58 did not resolve the same identity/store modules v57 uses")

# Exact pre-reopen bytes of the reopened path, carried by v56 (self-checked
# there to hash to PRE_REOPEN_BLOB).
_PRE_REOPEN_BYTES = q.q._PRE_REOPEN_BYTES
PRE_REOPEN_BLOB = q.PRE_REOPEN_BLOB
if V25.blob(_PRE_REOPEN_BYTES) != PRE_REOPEN_BLOB:
    base.fail("v58 inherited pre-reopen bytes do not hash to PRE_REOPEN_BLOB")


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v57_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v58 workflow does not reverse to exact canonical v57 predecessor: "
                f"{path} expected={Q_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return replacements


def _derive_candidate_workflow_hash(path: str) -> str:
    _workflow_replacements(raw_root)
    return V25.sha(raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES))


WF = {
    FW: _derive_candidate_workflow_hash(FW),
    AW: _derive_candidate_workflow_hash(AW),
    CW: q.WF[CW],
}


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v57(view: Any) -> None:
    for path, expected in ((q.P, V57_P_BLOB), (q.T, V57_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v58 candidate/base is missing frozen v57 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v57 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v57(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v57_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    projected_candidate = _project_for_v57(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v57(policy_base)


def _identity_store_pre_projected(original: Any, workflow_reversal: dict[str, bytes]) -> Any:
    """`read_bytes` replacement for the whole frozen v57 self-test `run()`: the
    v58->v57 workflow reversal, plus - only when the real tree already holds the
    exact authorized post-reopen blob at the reopened path - that one path
    projected back to its exact pre-reopen bytes. Every other read passes
    straight through. This is v56's frontier-projection mechanism, widened in
    scope so v56's and v57's own post-cascade `_check_*` (which call
    `p.files(p.raw_root)`) also see the pre-reopen bytes and the inherited v28
    token scan never observes `std::process` in the tranche.
    """
    project = (
        V25.blob(original(raw_root, IDENTITY_STORE_TEST, base.MAX_POLICY_FILE_BYTES))
        == AUTHORIZED_POST_REOPEN_BLOB
    )

    def _wrapped(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v58 v57-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        if project and relative == IDENTITY_STORE_TEST:
            if len(_PRE_REOPEN_BYTES) > limit:
                base.fail(
                    "v58 identity-store pre-reopen projection exceeds read bound: "
                    f"{relative}"
                )
            return _PRE_REOPEN_BYTES
        return original(local_view, relative, limit)

    return _wrapped


def run_predecessor_selftests() -> None:
    """Run frozen v57's own self-tests once, under the v58->v57 workflow
    reversal plus the identity-store pre-reopen projection, so every
    `files()` / `delta()` call in the frozen v57 -> v56 -> ... self-tests and in
    their own post-cascade checks sees the reopened path as its pre-reopen bytes
    and the inherited v28 token scan passes.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes
    base.LocalRepositoryView.read_bytes = _identity_store_pre_projected(
        original_read_bytes, workflow_reversal
    )
    try:
        _call(
            "v57 self-tests under v58->v57 reversal + identity-store pre-reopen projection",
            q.selftest,
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v58 bootstrap delta must be exactly two v58 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v58 bootstrap base authorizes only exact selftest-cascade "
                "projection-repair policy activation"
            )
        req_v57(candidate)
        req_v57(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v58 policy files are frozen after activation")

    q.delta(_project_for_v57(candidate), _project_for_v57(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v57_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v58 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v58 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(
                    f"v58 controlled file unexpectedly exists in bootstrap base: {path}"
                )
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v58 steady-state controlled file drifted: {path}")

    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _v57_views(candidate, policy_base)
        q.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        q.allowed(remaining, stage)


def files(view: Any) -> None:
    q.files(_project_for_v57(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v58 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v58 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v58 controlled file content drifted: {path}")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v58 predecessor component-base hook unavailable")
    _call(
        "v58 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v57(view),
        set(paths) - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v58 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v57_views(candidate, policy_base)
    _call(
        "v58 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v58=S2_E015_V57_SELFTEST_CASCADE_PROJECTION_REPAIR_ONLY")
    print(f"v58_authority={AUTH}")
    print(f"v58_policy_repair={V58_POLICY_REPAIR}")
    print(f"authorized_post_reopen_blob_v58={AUTHORIZED_POST_REOPEN_BLOB}")
    print(f"test_child_process_authority_v58={TEST_CHILD_PROCESS_AUTHORITY}")
    print(f"general_shell_authority_v58={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v58={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"network_authority_v58={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v58={MODEL_PROVIDER_EXECUTION}")
    print(f"s3_plus_authority_v58={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v58={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v58 predecessor workflow identity map drifted: actual={current}")
    for module in _chain():
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
        (
            _attr(execution, "_verify_component_base", "component-base hook"),
            verify_component_base,
        ),
        (
            _attr(execution, "freeze_s1_007_state", "S1 state freeze hook"),
            freeze_s1_007_state,
        ),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v58 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v58 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(q, name) != globals()[name]:
            base.fail(f"v58 inherited authority drifted: {name}")
    if _v25mod._verify_product_files is not _V57_HARDENED_PRODUCT_VERIFY:
        base.fail("v58 identity/store product-verify projection drifted")
    if _v28mod._hardened_product_verify is not _V57_HARDENED_PRODUCT_VERIFY:
        base.fail("v58 v28 hardened-verify supersession drifted")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v57 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (
            _attr(desktop, "verify_extension_controlled_paths", "v57 desktop hook"),
            q.dext,
        ),
        (
            _attr(execution, "verify_extension_controlled_paths", "v57 execution hook"),
            q.eext,
        ),
        (_attr(shell, "validate_allowed_paths", "v57 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v57 files hook"), q.files),
        (_attr(shell, "print_success", "v57 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v58 predecessor hook drifted")
    if _v25mod._verify_product_files is not _V57_HARDENED_PRODUCT_VERIFY:
        base.fail("v58 predecessor product-verify projection drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v58 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v58 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v58 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v58 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v58 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v58 allowed hook")
    _bind(shell, "verify_policy_files", files, "v58 files hook")
    _bind(shell, "print_success", printer, "v58 printer hook")
    _bind(
        execution,
        "_verify_component_base",
        verify_component_base,
        "v58 component-base hook",
    )
    _bind(
        execution,
        "freeze_s1_007_state",
        freeze_s1_007_state,
        "v58 S1 state freeze hook",
    )
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_e015_v57_selftest_cascade_projection_repair_v58_selftest import run

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
                    V25.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", V25.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
