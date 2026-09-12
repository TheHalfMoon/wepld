#!/usr/bin/env python3
"""Repair a second self-test/admission defect in v66/v67; no functional or
authority changes.

v68 makes **no functional changes** to what v66/v67 grant: it wraps nothing
new, moves no target, and widens no authority. It repairs a second instance
of the same class of defect v67 already fixed once for `run_predecessor_
selftests()`, this time in the `files()` hook chain (bound to `shell.
verify_policy_files`), reached from a different entrypoint than the one v67
fixed.

Root cause, reproduced directly against v67's own merged head with a real
`verify-candidate-local` invocation (worktree-based, not synthetic):
`python wepld_s2_a009_selftest_repair_v67_integrity.py verify-candidate-local
--root . --policy-base-root <worktree-at-c622cc9> --policy-base-sha c622cc9...`
fails with the identical "S1-016 Build Learning bytes drifted" error v67
already fixed once - but through a *different* call path than `selftest`'s
`run_predecessor_selftests()`, which v67's fix does not cover:

```
verify_candidate_local -> V25.CAND -> _verify_with_policy_base ->
shell.verify_view -> ... -> shell.verify_policy_files(view) ->
v67.files -> v66.files -> ... -> v18.files -> current = state(view)
```

`shell.verify_policy_files` is the `files()` hook every successor overrides
(the same hook v66/v67's own `files()` function is bound to), and v18's own
`files()` implementation calls `state(view)` directly against whatever view
it is handed, as part of determining which S1 bootstrap phase that view is
in - the same frozen S1-016 ledger-content pin `run_predecessor_selftests()`
already had to work around, reached this time via a *view the candidate
verifier itself constructs* rather than via the self-test cascade.

The fix is scoped narrowly to avoid a real correctness hazard: projecting
`CHECKPOINT`/`LEDGER` for the *entire* `verify-candidate-local`/`verify-
remote` call (rather than only around this specific delegation) would also
blind this successor's own `delta()`/`_verify_reopen_candidate` to the
candidate's real new bytes, making the content-authorization check itself
vacuous - always validating the old content, never the actual candidate.
`files()` and `delta()` are separate, independently-invoked hook chains (one
verifies a single tree's own internal self-consistency; the other compares
two trees), so `files()` can safely project `CHECKPOINT`/`LEDGER` to their
pre-reopen bytes for the exact duration of its own delegation to the
predecessor `files()` chain, without ever touching what `delta()` sees. Both
`LocalRepositoryView.read_bytes` (used by `foundation-integrity`'s self-check
and local `verify-candidate-local`) and `RemoteRepositoryView.read_bytes`
(used by `s1-admission-integrity`'s privileged `verify-remote`) are patched
for that duration, since either view class can reach this same call
depending on which check is running.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_a009_files_hook_repair_v68_integrity.py"
T = ".github/scripts/wepld_s2_a009_files_hook_repair_v68_selftest.py"
T_BLOB = "701f4635fa906609bdbdf93d4f23f365373ef069"

V67_P_BLOB = "5c2e0f178a8e37ddfe4e9480088e643c7daa229b"
V67_T_BLOB = "dbc78ba0dc7269126a353c28aa01bca42f0845d5"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V68_ENTRYPOINT = b"wepld_s2_a009_files_hook_repair_v68_integrity.py"
_V67_ENTRYPOINT = b"wepld_s2_a009_selftest_repair_v67_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v67_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V68_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v68 workflow entrypoint count drifted before v67 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V68_ENTRYPOINT, _V67_ENTRYPOINT)


def _import_v67_under_workflow_projection() -> Any:
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v67_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v67_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v68 v67-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v67_import_read_bytes
    try:
        return importlib.import_module("wepld_s2_a009_selftest_repair_v67_integrity")
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v67_under_workflow_projection()

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

# Inherited unchanged. v68 makes no functional/production changes beyond the
# files() hook repair below.
CHECKPOINT = q.CHECKPOINT
LEDGER = q.LEDGER
REOPEN_FILES = q.REOPEN_FILES
MAX_REOPEN_FILE_BYTES = q.MAX_REOPEN_FILE_BYTES
REOPEN_TASKS = q.REOPEN_TASKS
EXACT_FROZEN_BLOBS = q.EXACT_FROZEN_BLOBS
S2_A009_BUILD_LEARNING_REOPEN_AUTHORITY = q.S2_A009_BUILD_LEARNING_REOPEN_AUTHORITY
S2_A009_BUILD_LEARNING_REOPEN_CONTRACT = q.S2_A009_BUILD_LEARNING_REOPEN_CONTRACT

# The exact pre-reopen bytes v67 already embedded and verified against
# EXACT_FROZEN_BLOBS. Reused by reference rather than re-embedded, so there
# is exactly one copy of this ~50KB of literal content in the whole tower.
_PRE_REOPEN_CHECKPOINT_BYTES = q._PRE_REOPEN_CHECKPOINT_BYTES
_PRE_REOPEN_LEDGER_BYTES = q._PRE_REOPEN_LEDGER_BYTES
if V25.blob(_PRE_REOPEN_CHECKPOINT_BYTES) != EXACT_FROZEN_BLOBS[CHECKPOINT]:
    base.fail("v68 inherited pre-reopen checkpoint bytes do not match the pinned PRE blob")
if V25.blob(_PRE_REOPEN_LEDGER_BYTES) != EXACT_FROZEN_BLOBS[LEDGER]:
    base.fail("v68 inherited pre-reopen ledger bytes do not match the pinned PRE blob")

AUTH = "S2_A009_FILES_HOOK_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE"
NEXT_AUTHORITY_GATE = q.NEXT_AUTHORITY_GATE

_INHERITED_AUTHORITY_NAMES = q._INHERITED_AUTHORITY_NAMES
for _name in _INHERITED_AUTHORITY_NAMES:
    globals()[_name] = getattr(q, _name)

for _path, _expected in ((q.P, V67_P_BLOB), (q.T, V67_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v68 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v67_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v68 workflow does not reverse to exact canonical v67 predecessor: "
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


def req_v67(view: Any) -> None:
    for path, expected in ((q.P, V67_P_BLOB), (q.T, V67_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v68 candidate/base is missing frozen v67 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v67 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v67(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v67_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    projected_candidate = _project_for_v67(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v67(policy_base)


def run_predecessor_selftests() -> None:
    """Unchanged from v67: run frozen v67's own self-tests once, under a
    v68->v67 workflow reversal. v67's own fix already projects `CHECKPOINT`/
    `LEDGER` for the self-test cascade; this repair's own fix lives in
    `files()` below, for a different call path entirely."""
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v67_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v68 v67-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v67_selftest_read_bytes
    try:
        _call("v67 self-tests under v68->v67 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def _reopen_available(view: Any) -> bool:
    return q._reopen_available(view)


def _verify_reopen_candidate(candidate: Any, policy_base: Any) -> None:
    q._verify_reopen_candidate(candidate, policy_base)


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v68 bootstrap delta must be exactly two v68 policy files plus two integrity workflows"
                )
            base.fail("v68 bootstrap base authorizes only exact files()-hook repair activation")
        req_v67(candidate)
        req_v67(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v68 policy files are frozen after activation")

    projected_candidate, projected_base = _v67_views(candidate, policy_base)
    q.delta(projected_candidate, projected_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v67_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v68 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v68 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v68 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v68 steady-state controlled file drifted: {path}")

    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _v67_views(candidate, policy_base)
        q.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        q.allowed(remaining, stage)


def _files_predecessor_read_bytes_override(
    original: Any,
) -> Any:
    def _read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative == CHECKPOINT:
            data = _PRE_REOPEN_CHECKPOINT_BYTES
        elif relative == LEDGER:
            data = _PRE_REOPEN_LEDGER_BYTES
        else:
            return original(local_view, relative, limit)
        if len(data) > limit:
            base.fail(
                f"v68 files-hook pre-reopen documentation projection exceeds read bound: {relative}"
            )
        return data

    return _read_bytes


def files(view: Any) -> None:
    """This is the repair. Every other hook is inherited unchanged.

    `q.files(...)` (and everything it delegates to, all the way down to
    v18's own `files()`, which calls `state(view)` directly) is invoked
    under a projection of `CHECKPOINT`/`LEDGER` back to their exact
    pre-reopen bytes - scoped to exactly this delegation call via a
    class-level monkeypatch of both view classes, restored in `finally`
    regardless of outcome. This successor's own checks below (`CONTROLLED_
    FILES` byte-identity) run against the real, unprojected `view`
    afterward, and `delta()`/`_verify_reopen_candidate` elsewhere in this
    module never run under this projection at all - only `files()`'s own
    predecessor delegation does.
    """
    original_local_read_bytes = base.LocalRepositoryView.read_bytes
    original_remote_read_bytes = base.RemoteRepositoryView.read_bytes
    base.LocalRepositoryView.read_bytes = _files_predecessor_read_bytes_override(
        original_local_read_bytes
    )
    base.RemoteRepositoryView.read_bytes = _files_predecessor_read_bytes_override(
        original_remote_read_bytes
    )
    try:
        q.files(_project_for_v67(view))
    finally:
        base.LocalRepositoryView.read_bytes = original_local_read_bytes
        base.RemoteRepositoryView.read_bytes = original_remote_read_bytes

    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v68 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v68 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v68 controlled file content drifted: {path}")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v68 predecessor component-base hook unavailable")
    _call(
        "v68 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v67(view),
        set(paths) - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v68 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v67_views(candidate, policy_base)
    _call(
        "v68 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v68=S2_A009_FILES_HOOK_ONLY_REPAIR_NO_FUNCTIONAL_CHANGE")
    print(f"v68_authority={AUTH}")
    print(f"s2_implementation_authority_v68={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v68={GIT_ROUTE_DECISION}")
    print(f"git_execution_authority_v68={GIT_EXECUTION_AUTHORITY}")
    print(f"network_authority_v68={NETWORK_AUTHORITY}")
    print(f"source_admission_v68={SOURCE_ADMISSION}")
    print(f"reopen_available_v68={_reopen_available(raw_root)}")
    print(f"next_authority_gate_v68={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v68 predecessor workflow identity map drifted: actual={current}")
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
        (_attr(execution, "_verify_component_base", "component-base hook"), verify_component_base),
        (_attr(execution, "freeze_s1_007_state", "S1 state freeze hook"), freeze_s1_007_state),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v68 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v68 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(q, name) != globals()[name]:
            base.fail(f"v68 inherited authority drifted: {name}")
    if q.EXACT_FROZEN_BLOBS != EXACT_FROZEN_BLOBS:
        base.fail("v68 must not move the inherited reopen pins")
    if base.LocalRepositoryView.read_bytes is not original_local_read_bytes_at_import:
        base.fail("v68 left the LocalRepositoryView.read_bytes monkeypatch installed")
    if base.RemoteRepositoryView.read_bytes is not original_remote_read_bytes_at_import:
        base.fail("v68 left the RemoteRepositoryView.read_bytes monkeypatch installed")


original_local_read_bytes_at_import = base.LocalRepositoryView.read_bytes
original_remote_read_bytes_at_import = base.RemoteRepositoryView.read_bytes


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v67 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v67 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v67 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v67 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v67 files hook"), q.files),
        (_attr(shell, "print_success", "v67 printer"), q.printer),
        (_attr(execution, "_verify_component_base", "v67 component-base hook"), q.verify_component_base),
        (_attr(execution, "freeze_s1_007_state", "v67 S1 state freeze hook"), q.freeze_s1_007_state),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v68 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v68 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v68 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v68 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v68 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v68 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v68 allowed hook")
    _bind(shell, "verify_policy_files", files, "v68 files hook")
    _bind(shell, "print_success", printer, "v68 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v68 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v68 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_a009_files_hook_repair_v68_selftest import run

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
