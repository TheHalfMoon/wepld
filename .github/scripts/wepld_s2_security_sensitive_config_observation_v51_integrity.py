#!/usr/bin/env python3
"""Authorize only the bounded S2-D012 security-sensitive Git-config observation.

v51 is an append-only policy successor over canonical v50 at main
b6782c38af91bba54979ceec73eba1f2b7739ec0. Founder decision
`FOUNDER_S2_D012_DECISION = REQUIRE_BOUNDED_SECURITY_SENSITIVE_GIT_CONFIG_OBSERVATION_BEFORE_S2_ACCEPTANCE`
authorizes exactly this: the smallest dependency-ordered append-only successor
required to close S2-D012 before the S2 acceptance decision.

`SecuritySensitiveObservation` (the typed, safe-count-only Doctor input), its
`D-SEC-CREDENTIAL-BEARING-CONFIG` rule, and its safe-count-only templates were
already granted and landed by v49. `run_doctor` still fed
`SecuritySensitiveObservation::default()` because no observation source was
ever authorized to populate it. v51 grants exactly that missing observation
source and nothing else:

  - a closed, exact eight-member `git config --get-regexp` query family
    (remote/push URL, credential helper, http.extraHeader, http.proxy,
    url.*.insteadOf/pushInsteadOf, core.sshCommand) added to the already-
    qualified S2-AUTH-014 Git-topology adapter in `git_topology.rs`, reusing
    its existing qualified-executable discovery, environment scrub, timeout,
    and output bounds verbatim;
  - `--local --no-includes` scope only: never global/system config, and a
    malicious repository's own `include`/`includeIf` directives are never
    followed;
  - transient classification only — a raw config value is inspected in-memory
    to produce one safe boolean/class, then discarded; only bounded safe
    counts ever escape the observer;
  - a new `SecuritySensitiveConfigAvailability` distinction in Doctor's
    typed input (`Unavailable` vs `Observed`) and a new
    `D-SEC-OBSERVATION-UNAVAILABLE` informational finding, so a failed/
    bounded/trust-refused observation is never silently indistinguishable
    from a repository that was actually observed and found clean;
  - `bin/wepld.rs` wiring `run_doctor` to the real observation in place of
    the `SecuritySensitiveObservation::default()` placeholder;
  - the S2-S008 secret-redaction proof requalified through this real
    Git-config observation route (a fake credential in an actual
    `.git/config`, not only a descriptor file Doctor's workspace scan reads).

It does NOT grant a general Git-process facility, arbitrary `git config`
execution, free-form argv, a second Git-executable discovery path, shell
execution, project-native command execution, package installation,
model/provider execution, network access, Git mutation, `safe.directory`
mutation, executable remediation, source/dependency admission, or S3+
authority. Every one of those remains `NONE`/unchanged and is asserted
against the inherited v50 chain.

The product tranche is a second stage after policy activation, exactly like
v49 was itself a second stage over v45-48's Git-topology files. Unlike v49, it
does not touch `crates/core/src/lib.rs` at all (no new module is registered;
`crates/core/tests/*.rs` files compile as Cargo integration tests without any
`lib.rs` export line), so no Core-export projection/stripping machinery is
needed anywhere in this successor. The initial product candidate must change
exactly:

    crates/core/src/git_topology.rs   (second stage; landed by v45)
    crates/core/src/doctor.rs         (second stage; landed by v49)
    crates/core/src/bin/wepld.rs      (second stage; landed by v49)
    crates/core/tests/doctor_v1.rs    (second stage; landed by v49)
    crates/core/tests/cli_v1.rs       (second stage; landed by v49)
    crates/core/tests/security_sensitive_config_v1.rs   (wholly new)

and must be based on the exact frozen five-file frontier pinned below. Once
that tranche lands, v51 freezes it until a later authority successor.

Package-load / resting-view note: v51 follows the v45..v50 discipline. It owns
a fresh `LocalRepositoryView` of the exact checked-out head, imports frozen
v50 under an exact v51->v50 workflow-entrypoint reversal, and inherits every
v50 hook by reference. Because no file this successor touches is subject to a
frozen-content check anywhere in the inherited v33..v50 cascade (only
`lib.rs` is, and this successor never changes it), no predecessor-facing
projection beyond the ordinary workflow-entrypoint reversal is required: the
five second-stage files and the one new file are never hidden from a frozen
predecessor self-test, exactly as v49's own docstring already established for
any file that is not the Core export ("no frozen predecessor check rejects an
unknown `crates/core` path, only the Core-export identity").
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_security_sensitive_config_observation_v51_integrity.py"
T = ".github/scripts/wepld_s2_security_sensitive_config_observation_v51_selftest.py"
T_BLOB = "c5755da21821110ae85d0b4ace8a37543b56abb1"

V50_P_BLOB = "4569222135e4ae85075368d73270d46e7453f18d"
V50_T_BLOB = "418645059a4625fb2734f97ee1a5e909d4512615"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V51_ENTRYPOINT = b"wepld_s2_security_sensitive_config_observation_v51_integrity.py"
_V50_ENTRYPOINT = b"wepld_s2_v49_doctor_cli_selftest_projection_repair_v50_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

# Do not inherit a predecessor module's resting/projection view. v51 bases all
# of its own exact-head and predecessor projections on the actual checked-out
# repository bytes.
raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v50_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V51_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v51 workflow entrypoint count drifted before v50 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V51_ENTRYPOINT, _V50_ENTRYPOINT)


def _import_v50_under_workflow_projection() -> Any:
    """Import frozen v50 while it observes exact v50 workflow bytes.

    v50 (hence v49..v45..v36) reads workflow bytes while its module is
    imported, and the v50->v51 entrypoint migration ships in this same
    candidate, so v50 must not observe its own successor's bytes. Only
    ``LocalRepositoryView.read_bytes`` is wrapped for the duration of the
    import and then restored in ``finally`` - the class object itself is
    never rebound, so v20's frozen constructor guard still captures and later
    sees the exact canonical ``base.LocalRepositoryView``.
    """
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v50_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v50_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v51 v50-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v50_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_v49_doctor_cli_selftest_projection_repair_v50_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v50_under_workflow_projection()

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

# --- S2-D012 security-sensitive config observation path allowlist ---
# One wholly new file; five already-landed files entering a second stage.
SEC_CONFIG_TEST = "crates/core/tests/security_sensitive_config_v1.rs"
GIT_TOPOLOGY_MODULE = "crates/core/src/git_topology.rs"
DOCTOR_MODULE = "crates/core/src/doctor.rs"
CLI_BIN = "crates/core/src/bin/wepld.rs"
DOCTOR_TEST = "crates/core/tests/doctor_v1.rs"
CLI_TEST = "crates/core/tests/cli_v1.rs"

PRODUCT_NEW_FILES = frozenset({SEC_CONFIG_TEST})
PRODUCT_EXISTING_FILES = frozenset(
    {GIT_TOPOLOGY_MODULE, DOCTOR_MODULE, CLI_BIN, DOCTOR_TEST, CLI_TEST}
)
PRODUCT_FILES = frozenset(PRODUCT_NEW_FILES | PRODUCT_EXISTING_FILES)

CORE_MANIFEST = "crates/core/Cargo.toml"
ROOT_CARGO = "Cargo.toml"
ROOT_CARGO_LOCK = "Cargo.lock"

MAX_PRODUCT_FILE_BYTES = 262_144

PRODUCT_TASKS = frozenset({"S2-D012", "S2-S008"})

# The exact pre-v51 frontier blobs of the five second-stage files, at
# canonical main b6782c38af91bba54979ceec73eba1f2b7739ec0.
REQUIRED_PRODUCT_BASE_BLOBS = {
    GIT_TOPOLOGY_MODULE: "70c368792a930598c693654dbcc04b41b73c71a3",
    DOCTOR_MODULE: "c9e74aa9a716a7dfb5309b47558e0d482f1da270",
    CLI_BIN: "b27d18a3a21be6d3e9694ba6d3a905227b95de2a",
    DOCTOR_TEST: "8d6268a2cce592f0e9c9875f3fd5b524ce03ad0b",
    CLI_TEST: "a9015ed01dce353439608a603a34f9d8cf804cc3",
}

# The closed `git config --get-regexp` query family. Every pattern is a fixed
# literal in `git_topology.rs::ConfigQuery::key_regexp`; there is no
# variable/user-supplied argv anywhere in this family.
CLOSED_CONFIG_QUERY_FAMILY = frozenset(
    {
        "REMOTE_URL",
        "REMOTE_PUSHURL",
        "CREDENTIAL_HELPER",
        "HTTP_EXTRAHEADER",
        "HTTP_PROXY",
        "URL_INSTEADOF",
        "URL_PUSHINSTEADOF",
        "CORE_SSHCOMMAND",
    }
)

AUTH = "S2_D012_BOUNDED_SECURITY_SENSITIVE_GIT_CONFIG_OBSERVATION_ONLY"
S2_IMPLEMENTATION_AUTHORITY = (
    "EXACT_SECURITY_SENSITIVE_GIT_CONFIG_OBSERVATION_TRANCHE_ONLY_AFTER_V51_ACTIVATION"
)
DEPENDENCY_ADMISSION = q.DEPENDENCY_ADMISSION
SOURCE_ADMISSION = q.SOURCE_ADMISSION
GIT_ROUTE_DECISION = q.GIT_ROUTE_DECISION
GIT_PROCESS_ADMISSION = q.GIT_PROCESS_ADMISSION
EXTERNAL_PROCESS_AUTHORITY = q.EXTERNAL_PROCESS_AUTHORITY
GIT_EXECUTION_AUTHORITY = q.GIT_EXECUTION_AUTHORITY
NETWORK_AUTHORITY = q.NETWORK_AUTHORITY
MODEL_PROVIDER_EXECUTION = q.MODEL_PROVIDER_EXECUTION
DOCTOR_CLI_AUTHORITY = q.DOCTOR_CLI_AUTHORITY
S3_PLUS_AUTHORITY = q.S3_PLUS_AUTHORITY
NEXT_AUTHORITY_GATE = "S2-ACCEPTANCE"

# The one new grant this successor makes. Scoped narrowly: it authorizes only
# the closed eight-member query family above, over `--local --no-includes`
# config, reusing the already-qualified S2-AUTH-014 Git executable. It does
# not widen `GIT_EXECUTION_AUTHORITY` itself.
SECURITY_SENSITIVE_CONFIG_OBSERVATION_AUTHORITY = (
    "BOUNDED_CLOSED_LOCAL_GIT_CONFIG_GET_REGEXP_CLASSIFICATION_ONLY"
)

# Standing denials this successor must not relax.
GENERAL_SHELL_AUTHORITY = "NONE"
ARBITRARY_PROCESS_AUTHORITY = "NONE"
PACKAGE_INSTALL_AUTHORITY = "NONE"
PROJECT_NATIVE_COMMAND_EXECUTION = "NONE"
GIT_MUTATION_AUTHORITY = "NONE"
SAFE_DIRECTORY_MUTATION_AUTHORITY = "NONE"
REMEDIATION_EXECUTION_AUTHORITY = "NONE"

SECURITY_SENSITIVE_CONFIG_OBSERVATION_CONTRACT = (
    "LOCAL_SCOPE_ONLY",
    "NO_INCLUDES",
    "NO_USER_SUPPLIED_KEY_PATTERN",
    "TRANSIENT_CLASSIFICATION_RAW_VALUE_DISCARDED",
    "SAFE_COUNT_CLASS_OUTPUT_ONLY",
    "NO_NETWORK_EFFECT",
    "REUSES_QUALIFIED_GIT_EXECUTABLE",
    "NO_NEW_GIT_EXECUTABLE_DISCOVERY_PATH",
    "UNAVAILABLE_IS_NOT_CLEAN",
    "BOUNDED_RECORD_AND_VALUE_SIZE",
    "PRESERVE_NATIVE_GIT_TRUST_REFUSAL",
)

for _path, _expected in ((q.P, V50_P_BLOB), (q.T, V50_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v51 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v50_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v51 workflow does not reverse to exact canonical v50 predecessor: "
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


def req_v50(view: Any) -> None:
    for path, expected in ((q.P, V50_P_BLOB), (q.T, V50_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v51 candidate/base is missing frozen v50 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v50 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v50(view: Any) -> Any:
    """No file this successor touches is subject to a frozen-content check
    anywhere in the inherited cascade (unlike v49's `lib.rs`), so the only
    projection any predecessor delegation ever needs is the ordinary
    workflow-entrypoint reversal every successor performs."""
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v50_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    """Project the candidate to v50's view always; project the policy base
    only when it is a real post-v51 base. A pre-v51 bootstrap base predates
    the v50->v51 workflow migration and carries no v51 policy files, so it
    must reach v50's frozen hooks unprojected."""
    projected_candidate = _project_for_v50(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v50(policy_base)


def _boot_base_for_selftest() -> Any:
    return _project_for_v50(raw_root)


def run_predecessor_selftests() -> None:
    """Run frozen v50's own self-tests once, under a v51->v50 workflow
    reversal.

    v50's corrected hooks are inherited by reference. Only ``read_bytes`` is
    wrapped here for the v51->v50 workflow reversal; the wrap is restored in
    ``finally``. No product-file projection is layered here: this successor's
    six paths are not subject to any frozen-content check downstream, so a
    fresh ``LocalRepositoryView`` inventory of the real post-tranche head
    still matches what the frozen cascade expects.
    """
    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v50_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v51 v50-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    base.LocalRepositoryView.read_bytes = _v50_selftest_read_bytes
    try:
        _call("v50 self-tests under v51->v50 workflow reversal", q.selftest)
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


def _product_presence(view: Any) -> frozenset[str]:
    return frozenset(PRODUCT_NEW_FILES & V25.ps(view))


def _require_product_base(view: Any) -> None:
    paths = V25.ps(view)
    if _product_presence(view):
        base.fail(
            "v51 product base already contains the security-sensitive config "
            "observation tranche; later edits require successor authority"
        )
    for path, expected in REQUIRED_PRODUCT_BASE_BLOBS.items():
        if path not in paths:
            base.fail(f"v51 product base frontier missing: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"v51 product base frontier drifted: {path}: "
                f"expected={expected} actual={actual}"
            )
    for path in sorted(PRODUCT_NEW_FILES):
        if path in paths:
            base.fail(f"v51 product base frontier unexpectedly contains new path: {path}")


def _verify_text_product_file(view: Any, path: str) -> None:
    if path not in V25.ps(view):
        base.fail(f"v51 product path missing: {path}")
    if V25.mode(view, path) != "100644":
        base.fail(f"v51 product path mode invalid: {path}")
    data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
    if not data:
        base.fail(f"v51 product path must not be empty: {path}")
    if len(data) > MAX_PRODUCT_FILE_BYTES:
        base.fail(f"v51 product path exceeds bounded size: {path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"v51 product path must be UTF-8: {path}: {exc}")


def _verify_product_candidate(candidate: Any, policy_base: Any) -> None:
    _require_product_base(policy_base)
    if _product_presence(candidate) != PRODUCT_NEW_FILES:
        base.fail(
            "v51 candidate must contain the new security-sensitive config observation test file"
        )
    for path in sorted(PRODUCT_FILES):
        _verify_text_product_file(candidate, path)
    changed = V25.changed(V25.v24.v23, candidate, policy_base)
    for path in (CORE_MANIFEST, ROOT_CARGO, ROOT_CARGO_LOCK):
        if path in changed:
            base.fail(
                "v51 security-sensitive config observation tranche must not "
                f"change dependency/manifest path: {path}"
            )
    for relative in sorted(V25.FROZEN_STATE_PATHS):
        if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
            relative, V25.MAX_S1_STATE_BYTES
        ):
            base.fail(f"v51 candidate changed frozen S1 state: {relative}")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v51 bootstrap delta must be exactly two v51 policy files plus two integrity workflows"
                )
            base.fail("v51 bootstrap base authorizes only exact S2-D012 policy activation")
        req_v50(candidate)
        req_v50(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v51 policy files are frozen after activation")

    product_changed = frozenset(paths & PRODUCT_FILES)
    if product_changed:
        if _product_presence(policy_base):
            base.fail(
                "v51 security-sensitive config observation tranche is frozen "
                "after first canonical landing"
            )
        if paths != PRODUCT_FILES or product_changed != PRODUCT_FILES:
            if paths - PRODUCT_FILES:
                base.fail(
                    "v51 security-sensitive config observation product must "
                    "not mix with non-product paths"
                )
            base.fail(
                "v51 initial security-sensitive config observation delta "
                "must change exact module/test set"
            )
        _verify_product_candidate(candidate, policy_base)
        return

    q.delta(_project_for_v50(candidate), _project_for_v50(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v50_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v51 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v51 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(f"v51 controlled file unexpectedly exists in bootstrap base: {path}")
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v51 steady-state controlled file drifted: {path}")

    product_safe = PRODUCT_FILES & safe_paths & V25.ps(candidate)
    for path in sorted(product_safe):
        _verify_text_product_file(candidate, path)

    rest = frozenset(safe_paths - CONTROLLED_FILES - PRODUCT_FILES)
    if rest:
        projected_candidate, projected_base = _v50_views(candidate, policy_base)
        q.ext(projected_candidate, projected_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, V25.extset(V25.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - CONTROLLED_FILES - PRODUCT_FILES
    if remaining:
        q.allowed(remaining, stage)


def files(view: Any) -> None:
    q.files(_project_for_v50(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v51 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v51 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v51 controlled file content drifted: {path}")
    if _product_presence(view):
        for path in sorted(PRODUCT_FILES):
            _verify_text_product_file(view, path)


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v51 predecessor component-base hook unavailable")
    path_set = set(paths)
    if path_set & PRODUCT_FILES:
        if not PRODUCT_NEW_FILES <= V25.ps(view):
            base.fail(
                "v51 component-base view is missing the security-sensitive "
                "config observation tranche"
            )
        remaining = path_set - PRODUCT_FILES
        _call(
            "v51 projected predecessor component-base verifier",
            _PREDECESSOR_COMPONENT_BASE,
            _project_for_v50(view),
            remaining - CONTROLLED_FILES,
            allow_core_main_change=False,
        )
        return
    _call(
        "v51 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v50(view),
        path_set - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v51 predecessor S1 freeze hook unavailable")
    paths = V25.changed(V25.v24.v23, candidate, policy_base)
    if paths == PRODUCT_FILES:
        for relative in sorted(V25.FROZEN_STATE_PATHS):
            if candidate.read_bytes(relative, V25.MAX_S1_STATE_BYTES) != policy_base.read_bytes(
                relative, V25.MAX_S1_STATE_BYTES
            ):
                base.fail(f"v51 candidate changed frozen S1 state: {relative}")
        return
    projected_candidate, projected_base = _v50_views(candidate, policy_base)
    _call(
        "v51 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v51=S2_D012_BOUNDED_SECURITY_SENSITIVE_GIT_CONFIG_OBSERVATION_ONLY")
    print(f"v51_authority={AUTH}")
    print(f"s2_implementation_authority_v51={S2_IMPLEMENTATION_AUTHORITY}")
    print(
        "security_sensitive_config_observation_authority_v51="
        f"{SECURITY_SENSITIVE_CONFIG_OBSERVATION_AUTHORITY}"
    )
    print(f"doctor_cli_authority_v51={DOCTOR_CLI_AUTHORITY}")
    print(f"general_shell_authority_v51={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v51={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v51={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v51={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v51={GIT_MUTATION_AUTHORITY}")
    print(f"safe_directory_mutation_authority_v51={SAFE_DIRECTORY_MUTATION_AUTHORITY}")
    print(f"remediation_execution_authority_v51={REMEDIATION_EXECUTION_AUTHORITY}")
    print(f"git_process_admission_v51={GIT_PROCESS_ADMISSION}")
    print(f"git_execution_authority_v51={GIT_EXECUTION_AUTHORITY}")
    print(f"external_process_authority_v51={EXTERNAL_PROCESS_AUTHORITY}")
    print(f"network_authority_v51={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v51={MODEL_PROVIDER_EXECUTION}")
    print(f"source_admission_v51={SOURCE_ADMISSION}")
    print(f"dependency_admission_v51={DEPENDENCY_ADMISSION}")
    print(f"s3_plus_authority_v51={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v51={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v51 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v51 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v51 workflow identity projection drifted")
    for name in (
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
    ):
        if getattr(q, name) != globals()[name]:
            base.fail(f"v51 inherited authority drifted: {name}")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v50 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (_attr(desktop, "verify_extension_controlled_paths", "v50 desktop hook"), q.dext),
        (_attr(execution, "verify_extension_controlled_paths", "v50 execution hook"), q.eext),
        (_attr(shell, "validate_allowed_paths", "v50 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v50 files hook"), q.files),
        (_attr(shell, "print_success", "v50 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v51 predecessor hook drifted")

    _PREDECESSOR_COMPONENT_BASE = _attr(
        execution, "_verify_component_base", "predecessor component-base hook"
    )
    _PREDECESSOR_FREEZE_S1 = _attr(
        execution, "freeze_s1_007_state", "predecessor S1 state freeze hook"
    )

    prepare_q()
    desktop_extensions = frozenset(set(V25.extset(desktop)) | set(CONTROLLED_FILES))
    execution_extensions = frozenset(set(V25.extset(execution)) | set(CONTROLLED_FILES))
    _bind(desktop, "EXTENSION_CONTROLLED_PATHS", desktop_extensions, "v51 desktop registration")
    _bind(execution, "EXTENSION_CONTROLLED_PATHS", execution_extensions, "v51 execution registration")
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v51 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v51 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v51 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v51 allowed hook")
    _bind(shell, "verify_policy_files", files, "v51 files hook")
    _bind(shell, "print_success", printer, "v51 printer hook")
    _bind(execution, "_verify_component_base", verify_component_base, "v51 component-base hook")
    _bind(execution, "freeze_s1_007_state", freeze_s1_007_state, "v51 S1 state freeze hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_security_sensitive_config_observation_v51_selftest import run

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
