#!/usr/bin/env python3
"""Select the S2 Git topology route without granting Git/process execution.

v34 is an append-only policy successor layered over canonical v33 after the
identity/evidence-store product tranche became canonical at merge
`a6edc3af9e0435ed6283b2bf42ab0aff240b10db`.

It executes S2-AUTH-013 only: WePLD selects a narrow, qualified system-Git
adapter as the future repository-topology route and freezes the qualification
contract that S2-AUTH-014 must satisfy. This policy bootstrap does not execute
Git, admit a process, widen product paths, admit a source/dependency, authorize
Doctor/CLI, enable network/model/provider effects, or pull S3 Terminal Fabric
backward into S2.

The separation is intentional:

    route decision -> canonical activation -> separate process qualification

A selected route is not execution authority.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v33_integrity as p

V25 = p.V25

P = ".github/scripts/wepld_s2_git_route_governance_v34_integrity.py"
T = ".github/scripts/wepld_s2_git_route_governance_v34_selftest.py"
DECISION = "specs/005-s2-open-project-doctor-local-identity-storage/decisions/S2_AUTH_013_GIT_ROUTE.md"

V33_P_BLOB = "f2a7626fcead2984749457b203dcd2523f6982a2"
V33_T_BLOB = "e2eb9fa5a6393305a6465be71aea53bb2193a586"
T_BLOB = "312401509eaec8a82ef8a19a5c3dc37a1144daab"
DECISION_BLOB = "439fad7df33a442a976fe5cf47bebddb2144ea53"

REQUIRED_PREDECESSOR_BLOBS = {
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
CONTROLLED_FILES = frozenset({P, T, DECISION})
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, DECISION, FW, AW})

AUTH = "S2_GIT_TOPOLOGY_ROUTE_DECISION_ONLY"
S2_IMPLEMENTATION_AUTHORITY = p.S2_IMPLEMENTATION_AUTHORITY
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = "NONE"
GIT_ROUTE_DECISION = "SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER"
GIT_PROCESS_ADMISSION = "NONE"
EXTERNAL_PROCESS_AUTHORITY = "NONE"
GIT_EXECUTION_AUTHORITY = "NONE"
NETWORK_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
DOCTOR_CLI_AUTHORITY = "NONE"
S3_PLUS_AUTHORITY = "NONE"
NEXT_AUTHORITY_GATE = "S2-AUTH-014"

_V34_ENTRYPOINT = b"wepld_s2_git_route_governance_v34_integrity.py"
_V33_ENTRYPOINT = b"wepld_s2_identity_store_governance_v33_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

root = p.root

for _path, _expected in (
    (p.P, V33_P_BLOB),
    (p.T, V33_T_BLOB),
    (T, T_BLOB),
    (DECISION, DECISION_BLOB),
):
    _actual = V25.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v34 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

DECISION_BYTES = root.read_bytes(DECISION, base.MAX_POLICY_FILE_BYTES)


def _derive_candidate_workflow_hash(path: str) -> str:
    data = root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    count = data.count(_V34_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v34 workflow entrypoint count drifted at package load: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    predecessor = data.replace(_V34_ENTRYPOINT, _V33_ENTRYPOINT)
    actual = V25.sha(predecessor)
    if actual != P_WF[path]:
        base.fail(
            "v34 workflow carries changes beyond the exact entrypoint migration: "
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


def req_v33(view: Any) -> None:
    for path, expected in ((p.P, V33_P_BLOB), (p.T, V33_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v34 candidate/base is missing frozen v33 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v33 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def req_canonical_identity_store(view: Any) -> None:
    paths = V25.ps(view)
    for path, expected in REQUIRED_PREDECESSOR_BLOBS.items():
        if path not in paths:
            base.fail(f"v34 requires canonical #240 predecessor path: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v34 canonical #240 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def verify_decision(view: Any) -> None:
    if DECISION not in V25.ps(view):
        base.fail("v34 Git-route decision artifact is missing")
    if V25.mode(view, DECISION) != "100644":
        base.fail("v34 Git-route decision mode must be 100644")
    data = view.read_bytes(DECISION, base.MAX_POLICY_FILE_BYTES)
    actual = V25.blob(data)
    if actual != DECISION_BLOB:
        base.fail(
            "v34 Git-route decision bytes drifted: "
            f"expected={DECISION_BLOB} actual={actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V34_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v34 workflow entrypoint count drifted before predecessor projection: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        predecessor = data.replace(_V34_ENTRYPOINT, _V33_ENTRYPOINT)
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v34 workflow does not reverse to exact canonical v33 predecessor: "
                f"{path} expected={P_WF[path]} actual={actual}"
            )
        replacements[path] = predecessor
    return replacements


class _ProjectionView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v34 projected file exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def entries(self) -> Any:
        return self._view.entries()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _workflow_predecessor_projection(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view))


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
                    "v34 bootstrap delta must be exactly decision + two v34 policy "
                    "files + two integrity workflows"
                )
            base.fail("v34 bootstrap base authorizes only exact S2-AUTH-013 policy activation")
        req_v33(candidate)
        req_v33(policy_base)
        req_canonical_identity_store(candidate)
        req_canonical_identity_store(policy_base)
        if DECISION in V25.ps(policy_base):
            base.fail("v34 Git-route decision unexpectedly exists in bootstrap base")
        verify_decision(candidate)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v34 Git-route policy/decision files are frozen after activation")

    p.delta(candidate, policy_base)


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
                base.fail(f"v34 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v34 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v34 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v34 steady-state controlled file drifted: {path}")

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
    verify_decision(view)
    approved = {
        P: root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
        DECISION: DECISION_BYTES,
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v34 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v34 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v34 controlled file content drifted: {path}")


def printer(stage: str, mode_: str) -> None:
    _call("v33 success printer", p.printer, stage, mode_)
    print("wepld_policy_successor_v34=S2_GIT_TOPOLOGY_ROUTE_DECISION_ONLY")
    print(f"v34_authority={AUTH}")
    print(f"s2_implementation_authority_v34={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v34={GIT_ROUTE_DECISION}")
    print(f"git_process_admission_v34={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v34={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v34={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v34={NETWORK_AUTHORITY}")
    print(f"source_admission_v34={SOURCE_ADMISSION}")
    print(f"next_authority_gate_v34={NEXT_AUTHORITY_GATE}")


def prepare_p() -> None:
    current = dict(p.WF)
    if current not in (P_WF, dict(WF)):
        base.fail(f"v34 predecessor workflow identity map drifted: actual={current}")
    p.WF = dict(WF)
    for module in p.PREDECESSOR_CHAIN:
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
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v34 installed overlay drifted")
    if dict(p.WF) != dict(WF) or any(
        dict(module.WF) != dict(WF) for module in p.PREDECESSOR_CHAIN
    ):
        base.fail("v34 workflow identity projection drifted")


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
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v33 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v33 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v33 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v33 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v33 files hook"), p.files),
        (_attr(shell, "print_success", "v33 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v34 predecessor hook drifted")

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        desktop_extensions,
        "v34 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v34 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v34 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v34 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v34 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v34 allowed hook")
    _bind(shell, "verify_policy_files", files, "v34 files hook")
    _bind(shell, "print_success", printer, "v34 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_git_route_governance_v34_selftest import run

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
