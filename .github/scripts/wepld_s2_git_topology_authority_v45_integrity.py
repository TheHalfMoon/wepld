#!/usr/bin/env python3
"""Authorize only the bounded S2-AUTH-014 local Git topology adapter tranche.

v45 is an append-only policy successor over canonical v44 at main
53d8883418d9c9ab1c2081de8d7c9436aacdeba3. It executes S2-AUTH-014 only.

It grants a narrowly qualified local process boundary for one resolved absolute
system Git executable and only two closed topology command families. It also
grants exactly three Core product/test paths for the first Git-topology tracer
bullet after this policy becomes canonical.

It does NOT grant a general terminal/process facility, shell execution, user
supplied Git argv, Git mutation, hooks, network access, Doctor/CLI authority,
model/provider execution, source/dependency admission, or S3+ authority.

The product tranche is a second stage after policy activation. The initial
product candidate must change exactly:

    crates/core/src/git_topology.rs
    crates/core/src/lib.rs
    crates/core/tests/git_topology_v1.rs

and must be based on the exact frozen S2 frontier. Once that tranche lands, v45
freezes it until a later authority successor.

Package-load note: v36 reads workflow bytes while its Python module is imported.
A simple v45->v44 projected import is therefore insufficient across the deep
v44..v36 successor chain: nested module-load projections can expose the wrong
resting workflow image to v36 before v45 itself gets control. v45 preloads each
workflow-reading successor from v36 through v44 under the exact workflow image
for that version, oldest to newest. This is an import-time fixture/projection
repair only; repository workflow bytes remain the candidate v45 bytes and all
runtime/admission checks still bind exact v45/v44 identities.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v35_integrity as _v35

P = ".github/scripts/wepld_s2_git_topology_authority_v45_integrity.py"
T = ".github/scripts/wepld_s2_git_topology_authority_v45_selftest.py"
T_BLOB = "a1c3787c5351fba0e4302459d37dd71f43e6bdb5"

V44_P_BLOB = "bc11c7f89ad383625e4ea65200494361070f27a1"
V44_T_BLOB = "3d6c293804802a87a45ffdca4d106f293aec9fbd"

_V45_ENTRYPOINT = b"wepld_s2_git_topology_authority_v45_integrity.py"
_V44_ENTRYPOINT = b"wepld_s2_checkpoint_ledger_repair_governance_v44_integrity.py"

FW = _v35.FW
AW = _v35.AW
CW = _v35.CW
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = _v35.root

_PRELOAD_CHAIN: tuple[tuple[str, bytes], ...] = (
    (
        "wepld_s2_git_route_governance_v36_integrity",
        b"wepld_s2_git_route_governance_v36_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_transition_governance_v37_integrity",
        b"wepld_s2_checkpoint_transition_governance_v37_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_ledger_repair_governance_v38_integrity",
        b"wepld_s2_checkpoint_ledger_repair_governance_v38_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_ledger_repair_governance_v39_integrity",
        b"wepld_s2_checkpoint_ledger_repair_governance_v39_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_ledger_repair_governance_v40_integrity",
        b"wepld_s2_checkpoint_ledger_repair_governance_v40_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_ledger_repair_governance_v41_integrity",
        b"wepld_s2_checkpoint_ledger_repair_governance_v41_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_ledger_repair_governance_v42_integrity",
        b"wepld_s2_checkpoint_ledger_repair_governance_v42_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_ledger_repair_governance_v43_integrity",
        b"wepld_s2_checkpoint_ledger_repair_governance_v43_integrity.py",
    ),
    (
        "wepld_s2_checkpoint_ledger_repair_governance_v44_integrity",
        _V44_ENTRYPOINT,
    ),
)


def _workflow_projection_to(view: Any, entrypoint: bytes) -> dict[str, bytes]:
    """Project exact v45 workflow bytes directly to one predecessor entrypoint."""
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        count = data.count(_V45_ENTRYPOINT)
        if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
            base.fail(
                "v45 workflow entrypoint count drifted: "
                f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
            )
        replacements[path] = data.replace(_V45_ENTRYPOINT, entrypoint)
    return replacements


def _v44_workflow_projection(view: Any) -> dict[str, bytes]:
    return _workflow_projection_to(view, _V44_ENTRYPOINT)


def _preload_predecessor_chain() -> Any:
    """Load v36..v44 oldest-first under each version's exact workflow image."""
    original_root = _v35.root
    loaded: Any = None
    try:
        for module_name, entrypoint in _PRELOAD_CHAIN:
            _v35.root = _v35._ProjectionView(
                raw_root,
                _workflow_projection_to(raw_root, entrypoint),
            )
            loaded = importlib.import_module(module_name)
    finally:
        _v35.root = original_root
    if loaded is None:
        base.fail("v45 predecessor preload produced no v44 module")
    return loaded


# v36 is an import-time workflow reader. Preload the whole workflow-sensitive
# chain against exact per-version projections before binding v44 as predecessor.
p = _preload_predecessor_chain()

V25 = p.V25
P_WF = dict(p.WF)

_attr = p._attr
_bind = p._bind
_call = p._call
_INST = False
_PREDECESSOR_COMPONENT_BASE: Any = None
_PREDECESSOR_FREEZE_S1: Any = None

CORE_EXPORT = "crates/core/src/lib.rs"
GIT_TOPOLOGY_MODULE = "crates/core/src/git_topology.rs"
PRODUCT_TEST = "crates/core/tests/git_topology_v1.rs"
PRODUCT_FILES = frozenset({CORE_EXPORT, GIT_TOPOLOGY_MODULE, PRODUCT_TEST})
PRODUCT_NEW_FILES = frozenset({GIT_TOPOLOGY_MODULE, PRODUCT_TEST})
CORE_MANIFEST = "crates/core/Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"
PROJECT_MODULE = "crates/core/src/project.rs"

PRODUCT_TASKS = frozenset(
    {
        "S2-I005",
        "S2-I006",
        "S2-I007",
        "S2-S005",
        "S2-S006",
        "S2-S007",
        "S2-S013",
        "S2-S014",
        "S2-Q008",
    }
)

REQUIRED_PRODUCT_BASE_BLOBS = {
    CORE_EXPORT: "3180ae22cb29dbcc807418580c0062bab18c0a2e",
    PROJECT_MODULE: "1dce3c082b6021803cbe7129afef17e5ad33ff2a",
    CORE_MANIFEST: "9ff919ab5f05d6aa5b6c179f194eb4611e7b1bd8",
    ROOT_CARGO_LOCK: "d137e3f0c62637e402374880deb5355a878d4a91",
}
BASE_CORE_EXPORT = raw_root.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)

POLICY_FILES = frozenset({P, T})
CONTROLLED_FILES = POLICY_FILES
ALL_POLICY_FILES = frozenset(set(p.ALL_POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset({P, T, FW, AW})

AUTH = "S2_AUTH_014_EXACT_GIT_TOPOLOGY_PROCESS_TRANCHE"
S2_IMPLEMENTATION_AUTHORITY = "EXACT_GIT_TOPOLOGY_TRANCHE_ONLY_AFTER_V45_ACTIVATION"
DEPENDENCY_ADMISSION = p.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = p.SOURCE_ADMISSION
GIT_ROUTE_DECISION = p.GIT_ROUTE_DECISION
GIT_PROCESS_ADMISSION = "EXACT_LOCAL_SYSTEM_GIT_TOPOLOGY_ADAPTER_ONLY"
EXTERNAL_PROCESS_AUTHORITY = "EXACT_QUALIFIED_GIT_EXECUTABLE_CLOSED_TOPOLOGY_ARGV_ONLY"
GIT_EXECUTION_AUTHORITY = "READ_ONLY_TOPOLOGY_OBSERVATION_ONLY"
NETWORK_AUTHORITY = "NONE"
MODEL_PROVIDER_EXECUTION = "NONE"
DOCTOR_CLI_AUTHORITY = "NONE"
S3_PLUS_AUTHORITY = "NONE"
NEXT_AUTHORITY_GATE = "S2-AUTH-015"

GIT_ROUTE_QUALIFICATION_CONTRACT = (
    "RESOLVED_ABSOLUTE_EXECUTABLE_ONLY",
    "REJECT_PROJECT_LOCAL_GIT_SPOOF",
    "CLOSED_ENUM_TO_EXACT_ARGV",
    "NO_SHELL_PAGER_PROMPT_OPTIONAL_LOCKS",
    "NO_LAZY_FETCH",
    "CLOSED_STDIN",
    "BOUNDED_STDOUT_STDERR_HARD_TIMEOUT",
    "CHILD_PROCESS_REAP_ON_TIMEOUT_CANCEL",
    "SCRUB_GIT_CONFIG_AND_REPOSITORY_REDIRECTION_ENV",
    "SCRUB_TRACE_AND_WINDOWS_STD_HANDLE_REDIRECTION_ENV",
    "PRESERVE_NATIVE_SAFE_DIRECTORY_REFUSAL",
    "NO_HOOKS",
    "NO_NETWORK",
    "PROVE_TREE_INDEX_NON_MUTATION",
    "NO_SILENT_BINARY_FALLBACK",
    "RAW_ENV_NOT_PERSISTED",
    "WINDOWS_LINUX_MACOS_OR_EXPLICIT_LIMITATION",
)

GIT_GLOBAL_FLAGS = ("--no-pager", "--no-optional-locks", "--no-lazy-fetch")
GIT_REV_PARSE_QUERY_ENUM = (
    "--path-format=absolute --show-toplevel",
    "--path-format=absolute --absolute-git-dir",
    "--path-format=absolute --git-common-dir",
    "--is-bare-repository",
    "--is-inside-work-tree",
    "--path-format=absolute --show-superproject-working-tree",
)
GIT_WORKTREE_COMMAND = "worktree list --porcelain -z"
GIT_COMMAND_FAMILY = (
    "rev-parse:closed_allowlisted_topology_query",
    "worktree:list:porcelain-z",
)

GIT_ENV_REMOVE = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_INDEX_FILE",
    "GIT_NAMESPACE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_KEY_*",
    "GIT_CONFIG_VALUE_*",
    "GIT_CONFIG_GLOBAL",
    "GIT_CONFIG_SYSTEM",
    "GIT_CONFIG_NOSYSTEM",
    "GIT_ASKPASS",
    "GIT_PAGER",
    "GIT_TRACE*",
    "GIT_REDIRECT_STDIN",
    "GIT_REDIRECT_STDOUT",
    "GIT_REDIRECT_STDERR",
)
GIT_ENV_FORCE = (("GIT_TERMINAL_PROMPT", "0"),)

GIT_TIMEOUT_MS = 10_000
GIT_STDOUT_MAX_BYTES = 1_048_576
GIT_STDERR_MAX_BYTES = 262_144

GIT_FAILURE_TAXONOMY = (
    "not_git_repository",
    "untrusted_repository_refused_by_git",
    "unsupported_git_capability",
    "unqualified_git_executable",
    "git_timeout",
    "git_output_too_large",
    "git_output_malformed",
    "git_process_failed",
    "changed_under_observation",
)

EXECUTABLE_DISCOVERY_CONTRACT = (
    "RESOLVE_ONCE_THEN_ABSOLUTE_PATH_ONLY",
    "RECORD_LEXICAL_AND_RESOLVED_PATH_PLUS_BOUNDED_VERSION_EVIDENCE",
    "REJECT_OPENED_PROJECT_AND_WEPLD_EVIDENCE_ROOT_CANDIDATES",
    "NO_AUTO_INSTALL_UPDATE_OR_PACKAGE_MANAGER_SIDE_EFFECT",
    "NO_PER_INVOCATION_SHELL_LOOKUP",
    "NO_SILENT_FALLBACK",
    "UNAVAILABLE_IS_STABLE_FAIL_CLOSED_STATE",
)

for _path, _expected in ((p.P, V44_P_BLOB), (p.T, V44_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v45 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements = _v44_workflow_projection(view)
    for path, predecessor in replacements.items():
        actual = V25.sha(predecessor)
        if actual != P_WF[path]:
            base.fail(
                "v45 workflow does not reverse to exact canonical v44 predecessor: "
                f"{path} expected={P_WF[path]} actual={actual}"
            )
    return replacements


def _derive_candidate_workflow_hash(path: str) -> str:
    data = raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    _workflow_replacements(raw_root)
    return V25.sha(data)


WF = {
    FW: _derive_candidate_workflow_hash(FW),
    AW: _derive_candidate_workflow_hash(AW),
    CW: p.WF[CW],
}


class _ProjectionView:
    def __init__(
        self,
        view: Any,
        replacements: dict[str, bytes],
        omitted: frozenset[str] = frozenset(),
    ) -> None:
        self._view = view
        self._replacements = replacements
        self._omitted = omitted

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v45 predecessor projection exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return [entry for entry in self._view.entries() if entry.path not in self._omitted]

    def tree_identity(self, path: str) -> Any:
        return (id(self), path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def bootbase(view: Any) -> bool:
    return P not in V25.ps(view)


def req_v44(view: Any) -> None:
    for path, expected in ((p.P, V44_P_BLOB), (p.T, V44_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v45 candidate/base is missing frozen v44 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v44 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _product_presence(view: Any) -> frozenset[str]:
    return frozenset(PRODUCT_NEW_FILES & V25.ps(view))


def _product_projection(view: Any) -> tuple[dict[str, bytes], frozenset[str]]:
    present = _product_presence(view)
    if not present:
        return {}, frozenset()
    if present != PRODUCT_NEW_FILES:
        base.fail(f"v45 predecessor view contains partial Git-topology tranche: {sorted(present)}")
    lib = view.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if lib.count(b"pub mod git_topology;") != 1:
        base.fail("v45 Git-topology tranche must export git_topology exactly once")
    return {CORE_EXPORT: BASE_CORE_EXPORT}, PRODUCT_NEW_FILES


def _project_for_predecessor(view: Any) -> Any:
    replacements = _workflow_replacements(view)
    product_replacements, omitted = _product_projection(view)
    replacements.update(product_replacements)
    return _ProjectionView(view, replacements, omitted)


def _predecessor_view(view: Any, policy_base: Any) -> tuple[Any, Any]:
    candidate = _project_for_predecessor(view)
    if bootbase(policy_base):
        return candidate, policy_base
    return candidate, _project_for_predecessor(policy_base)


def run_predecessor_selftests() -> None:
    p.selftest()


def _workflow_predecessor_projection(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view))


def _require_product_base(view: Any) -> None:
    paths = V25.ps(view)
    if _product_presence(view):
        base.fail("v45 product base already contains Git-topology tranche; later edits require successor authority")
    for path, expected in REQUIRED_PRODUCT_BASE_BLOBS.items():
        if path not in paths:
            base.fail(f"v45 product base frontier missing: {path}")
        limit = 2_000_000 if path == ROOT_CARGO_LOCK else base.MAX_POLICY_FILE_BYTES
        actual = V25.blob(view.read_bytes(path, limit))
        if actual != expected:
            base.fail(
                f"v45 product base frontier drifted: {path}: expected={expected} actual={actual}"
            )


def _verify_text_product_file(view: Any, path: str) -> None:
    if path not in V25.ps(view):
        base.fail(f"v45 product path missing: {path}")
    if V25.mode(view, path) != "100644":
        base.fail(f"v45 product path mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data:
        base.fail(f"v45 product path must not be empty: {path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"v45 product path must be UTF-8: {path}: {exc}")


def _verify_product_candidate(candidate: Any, policy_base: Any) -> None:
    _require_product_base(policy_base)
    if _product_presence(candidate) != PRODUCT_NEW_FILES:
        base.fail("v45 candidate must contain the complete Git-topology module/test pair")
    for path in sorted(PRODUCT_FILES):
        _verify_text_product_file(candidate, path)
    lib = candidate.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if lib.count(b"pub mod git_topology;") != 1:
        base.fail("v45 Core export must register git_topology exactly once")
    for path in (CORE_MANIFEST, ROOT_CARGO_LOCK, PROJECT_MODULE):
        limit = 2_000_000 if path == ROOT_CARGO_LOCK else base.MAX_POLICY_FILE_BYTES
        if candidate.read_bytes(path, limit) != policy_base.read_bytes(path, limit):
            base.fail(f"v45 Git-topology tranche must not change frozen frontier path: {path}")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v45 bootstrap delta must be exactly two v45 policy files plus two integrity workflows"
                )
            base.fail("v45 bootstrap base authorizes only exact S2-AUTH-014 policy activation")
        req_v44(candidate)
        req_v44(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v45 policy files are frozen after activation")

    product_changed = frozenset(paths & PRODUCT_FILES)
    if product_changed:
        if _product_presence(policy_base):
            base.fail("v45 Git-topology product tranche is frozen after first canonical landing")
        if paths != PRODUCT_FILES or product_changed != PRODUCT_FILES:
            if paths - PRODUCT_FILES:
                base.fail("v45 Git-topology product must not mix with non-product paths")
            base.fail("v45 initial Git-topology delta must change exact module/export/test set")
        _verify_product_candidate(candidate, policy_base)
        return

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
                base.fail(f"v45 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v45 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v45 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v45 steady-state controlled file drifted: {path}")

    product_safe = PRODUCT_FILES & safe_paths & V25.ps(candidate)
    for path in sorted(product_safe):
        _verify_text_product_file(candidate, path)

    rest = frozenset(safe_paths - CONTROLLED_FILES - PRODUCT_FILES)
    if rest:
        projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
        p.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES - PRODUCT_FILES
    if remaining:
        p.allowed(remaining, stage)


def files(view: Any) -> None:
    p.files(_project_for_predecessor(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v45 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v45 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v45 controlled file content drifted: {path}")
    present = _product_presence(view)
    if present:
        if present != PRODUCT_NEW_FILES:
            base.fail("v45 canonical view contains partial Git-topology product tranche")
        for path in sorted(PRODUCT_FILES):
            _verify_text_product_file(view, path)
        lib = view.read_bytes(CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
        if lib.count(b"pub mod git_topology;") != 1:
            base.fail("v45 canonical Core export must register git_topology exactly once")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v45 predecessor component-base hook unavailable")
    path_set = set(paths)
    if path_set & PRODUCT_FILES:
        if not PRODUCT_NEW_FILES <= V25.ps(view):
            base.fail("v45 component-base view contains incomplete Git-topology tranche")
        projected = _project_for_predecessor(view)
        remaining = path_set - PRODUCT_FILES
        _call(
            "v45 projected predecessor component-base verifier",
            _PREDECESSOR_COMPONENT_BASE,
            projected,
            remaining,
            allow_core_main_change=False,
        )
        return
    _call(
        "v45 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        view,
        path_set,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v45 predecessor S1 freeze hook unavailable")
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if paths == PRODUCT_FILES:
        for relative in sorted(V25.FROZEN_STATE_PATHS - {CORE_EXPORT}):
            if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
                relative, V25.MAX_S1_STATE_BYTES
            ):
                base.fail(f"v45 Git-topology candidate changed frozen S1 state: {relative}")
        return
    projected_candidate, projected_base = _predecessor_view(candidate, policy_base)
    _call(
        "v45 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    p.printer(stage, mode_)
    print("wepld_policy_successor_v45=S2_AUTH_014_EXACT_GIT_TOPOLOGY_PROCESS_TRANCHE")
    print(f"v45_authority={AUTH}")
    print(f"s2_implementation_authority_v45={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"git_route_decision_v45={GIT_ROUTE_DECISION}")
    print(f"git_process_admission_v45={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v45={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v45={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v45={NETWORK_AUTHORITY}")
    print(f"source_admission_v45={SOURCE_ADMISSION}")
    print(f"dependency_admission_v45={DEPENDENCY_ADMISSION}")
    print(f"doctor_cli_authority_v45={DOCTOR_CLI_AUTHORITY}")
    print(f"s3_plus_authority_v45={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v45={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (p,) + p._chain()


def prepare_p() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (P_WF, dict(WF)):
            base.fail(f"v45 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v45 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v45 workflow identity projection drifted")
    if p.GIT_ROUTE_DECISION != GIT_ROUTE_DECISION:
        base.fail("v45 inherited S2-AUTH-013 route decision drifted")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    p.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v44 routing hook"), p.delta),
        (base.compare_base_controlled, p.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v44 desktop hook"), p.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v44 execution hook"), p.eext),
        (_attr(shell, "validate_allowed_paths", "v44 allowed hook"), p.allowed),
        (_attr(shell, "verify_policy_files", "v44 files hook"), p.files),
        (_attr(shell, "print_success", "v44 printer"), p.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v45 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_p()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v45 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v45 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v45 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v45 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v45 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v45 allowed hook")
    _bind(shell, "verify_policy_files", files, "v45 files hook")
    _bind(shell, "print_success", printer, "v45 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v45 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v45 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_git_topology_authority_v45_selftest import run

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
