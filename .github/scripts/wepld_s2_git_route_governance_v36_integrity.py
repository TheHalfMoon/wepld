#!/usr/bin/env python3
"""Select the S2 Git topology route without granting Git/process execution.

v36 is an append-only successor over canonical v35 after the corrected S2
checkpoint and Build Learning transition became canonical at merge
`0bdddf875a8ac8b53404f28d2be2e24dba520599`.

It executes S2-AUTH-013 only: WePLD selects a narrow, qualified system-Git
adapter as the future repository-topology route and freezes the qualification
contract that S2-AUTH-014 must satisfy. This policy bootstrap does not execute
Git, admit a process, widen product paths, admit source/dependency authority,
authorize Doctor/CLI, enable network/model/provider effects, or pull S3 Terminal
Fabric backward into S2.

The separation is intentional:

    route decision -> canonical activation -> separate process qualification

A selected route is not execution authority. Issue #243 is the coordination
record; canonical authority is this exact content-addressed successor surface.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as p

V25 = p.V25

P = ".github/scripts/wepld_s2_git_route_governance_v36_integrity.py"
T = ".github/scripts/wepld_s2_git_route_governance_v36_selftest.py"

V35_P_BLOB = "e5377d3d546106adb250e9915af667f4bb080eb6"
V35_T_BLOB = "8284914739d1842f5100480fed969ec04d8667c7"
T_BLOB = "cd807991928c2d3a413d0ab52cee36224d9737d9"

REQUIRED_CANONICAL_FRONTIER_BLOBS = {
    p.CHECKPOINT: p.FINAL_CHECKPOINT_BLOB,
    p.LEDGER: p.FINAL_LEDGER_BLOB,
    "crates/core/src/identity.rs": "16c835f894620b97e136e40a2f2512c257d1879b",
    "crates/core/src/evidence_store.rs": "8a38a079dd6bab8d0ab268db82079f9e7542379e",
    "crates/core/src/lib.rs": "3180ae22cb29dbcc807418580c0062bab18c0a2e",
    "crates/core/tests/identity_store_v1.rs": "fc1fd55c47e5bb6879b8c5bb03cd0500bedcff0f",
}

FW = p.FW
AW = p.AW
CW = p.CW
P_WF = dict(p.WF)

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_GIT_TOPOLOGY_ROUTE_DECISION_ONLY"
S2_IMPLEMENTATION_AUTHORITY = p.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = p.SOURCE_ADMISSION
GIT_ROUTE_DECISION = "SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER"
GIT_PROCESS_ADMISSION = "NONE"
EXTERNAL_PROCESS_AUTHORITY = "NONE"
GIT_EXECUTION_AUTHORITY = "NONE"
NETWORK_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
DOCTOR_CLI_AUTHORITY = "NONE"
S3_PLUS_AUTHORITY = "NONE"
NEXT_AUTHORITY_GATE = "S2-AUTH-014"

GIT_ROUTE_QUALIFICATION_CONTRACT = (
    "RESOLVED_ABSOLUTE_EXECUTABLE_ONLY",
    "REJECT_PROJECT_LOCAL_GIT_SPOOF",
    "CLOSED_ENUM_TO_EXACT_ARGV",
    "NO_SHELL_PAGER_PROMPT_OPTIONAL_LOCKS",
    "BOUNDED_STDOUT_STDERR_HARD_TIMEOUT",
    "SCRUB_GIT_CONFIG_AND_REPOSITORY_REDIRECTION_ENV",
    "PRESERVE_NATIVE_SAFE_DIRECTORY_REFUSAL",
    "NO_HOOKS",
    "NO_NETWORK",
    "PROVE_TREE_INDEX_NON_MUTATION",
    "NO_SILENT_BINARY_FALLBACK",
    "WINDOWS_LINUX_MACOS_OR_EXPLICIT_LIMITATION",
)

GIT_TOPOLOGY_COMMAND_FAMILY = (
    "rev-parse:closed_allowlisted_topology_query",
    "worktree:list:porcelain-z",
)

_V36_ENTRYPOINT = b"wepld_s2_git_route_governance_v36_integrity.py"
_V35_ENTRYPOINT = b"wepld_s2_identity_store_governance_v35_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

root = p.root

for _path, _expected in (
    (p.P, V35_P_BLOB),
    (p.T, V35_T_BLOB),
    (T, T_BLOB),
):
    _actual = V25.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v36 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _derive_candidate_workflow_hash(path: str) -> str:
    data = root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    count = data.count(_V36_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v36 workflow entrypoint count drifted at package load: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    predecessor = data.replace(_V36_ENTRYPOINT, _V35_ENTRYPOINT)
    actual = V25.sha(predecessor)
    if actual != P_WF[path]:
        base.fail(
            "v36 workflow carries changes beyond the exact entrypoint migration: "
            f"{path} expected_predecessor={P_WF[path]} actual={actual}"
        )
    return V25.sha(data)


WF = {
    FW: _derive_candidate_workflow_hash(FW),
    AW: _derive_candidate_workflow_hash(AW),
    CW: p.WF[CW],
}

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v35(view: Any) -> None:
    for path, expected in ((p.P, V35_P_BLOB), (p.T, V35_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v36 candidate/base is missing frozen v35 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v35 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def req_canonical_frontier(view: Any) -> None:
    paths = V25.ps(view)
    for path, expected in REQUIRED_CANONICAL_FRONTIER_BLOBS.items():
        if path not in paths:
            base.fail(f"v36 requires canonical S2 frontier path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v36 canonical S2 frontier drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V36_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v36 workflow entrypoint count drifted before predecessor projection: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        predecessor = data.replace(_V36_ENTRYPOINT, _V35_ENTRYPOINT)
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v36 workflow does not reverse to exact canonical v35 predecessor: "
                f"{path} expected={P_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return replacements


def _workflow_predecessor_projection(view: Any) -> Any:
    return p._ProjectionView(view, _workflow_replacements(view))


def _predecessor_view(view: Any, policy_base: Any) -> tuple[Any, Any]:
    candidate = _workflow_predecessor_projection(view)
    if bootbase(policy_base):
        return candidate, policy_base
    return candidate, _workflow_predecessor_projection(policy_base)


def run_predecessor_selftests() -> None:
    original_root = p.root
    p.root = _workflow_predecessor_projection(root)
    try:
        p.selftest()
    finally:
        p.root = original_root


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v36 bootstrap delta must be exactly two v36 policy files plus "
                    "two integrity workflows"
                )
            base.fail("v36 bootstrap base authorizes only exact S2-AUTH-013 policy activation")
        req_v35(candidate)
        req_v35(policy_base)
        req_canonical_frontier(candidate)
        req_canonical_frontier(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v36 Git-route policy files are frozen after activation")

    projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
    p.delta(projected_candidate, projected_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
        p.basectrl(projected_candidate, projected_base)
        return

    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != P_WF[path]:
                base.fail(f"v36 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v36 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v36 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v36 steady-state controlled file drifted: {path}")

    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
        p.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES
    if remaining:
        p.allowed(remaining, stage)


def files(view: Any) -> None:
    p.files(_workflow_predecessor_projection(view))
    approved = {
        P: root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v36 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v36 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v36 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    _call("v35 success printer", p.printer, stage, mode_)
    print("wepld_policy_successor_v36=S2_GIT_TOPOLOGY_ROUTE_DECISION_ONLY")
    print(f"v36_authority={AUTH}")
    print(f"s2_implementation_authority_v36={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v36={GIT_ROUTE_DECISION}")
    print(f"git_process_admission_v36={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v36={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v36={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v36={NETWORK_AUTHORITY}")
    print(f"source_admission_v36={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v36={NEXT_AUTHORITY_GATE}")


def prepare_p() -> None:
    current = dict(p.WF)
    if current not in (P_WF, dict(WF)):
        base.fail(f"v36 predecessor workflow identity map drifted: actual={current}")
    p.WF = dict(WF)
    for module in p.PREDECESSOR_CHAIN:
        module.WF = dict(WF)


def overlay() -> None:
    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "routing hook"), delta),
        (base.compare_base_controlled, basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "S1-005 evidence-freeze hook"),
            p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "desktop hook"), dext),
        (_attr(execution, "verify_extension_controlled_paths", "execution hook"), eext),
        (_attr(shell, "validate_allowed_paths", "allowed hook"), allowed),
        (_attr(shell, "verify_policy_files", "files hook"), files),
        (_attr(shell, "print_success", "printer hook"), printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v36 installed overlay drifted")
    if dict(p.WF) != dict(WF) or any(
        dict(module.WF) != dict(WF) for module in p.PREDECESSOR_CHAIN
    ):
        base.fail("v36 workflow identity projection drifted")


def install() -> None:
    global _INST
    if _INST:
        overlay()
        return

    original_root = p.root
    p.root = _workflow_predecessor_projection(root)
    try:
        p.install()
    finally:
        p.root = original_root

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v35 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (
            _attr(execution, "freeze_s1_005_evidence", "v35 S1-005 evidence-freeze hook"),
            p.Q_FREEZE,
        ),
        (_attr(desktop, "verify_extension_controlled_paths", "v35 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v35 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v35 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v35 files hook"), p.files),
        (_attr(shell, "print_success", "v35 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v36 predecessor hook drifted")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v36 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v36 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v36 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v36 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v36 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v36 allowed hook")
    _bind(shell, "verify_policy_files", files, "v36 files hook")
    _bind(shell, "print_success", printer, "v36 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_git_route_governance_v36_selftest import run

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
