#!/usr/bin/env python3
"""Repair v25 so S2 dependency admission includes its exact governance record.

v26 is an append-only repair successor layered over the reviewed v25 candidate.
It preserves the v25 trust/effect boundaries and changes one future transition:
S2-AUTH-012 is an exact three-path dependency-admission tranche consisting of
the Core manifest, Cargo.lock, and the canonical dependency register. The
register mutation is byte-exact: all prior S1 evidence is preserved verbatim
and one closed S2 decision section is appended.

No dependency is admitted by this policy bootstrap itself. The exact
manifest/lock/register candidate still requires deterministic qualification,
independent exact-head review, authorized Ready/merge, and post-merge
canonical activation before identity/store product code may rely on it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_bootstrap_v25_integrity as p

P = ".github/scripts/wepld_s2_identity_store_governance_v26_integrity.py"
T = ".github/scripts/wepld_s2_identity_store_governance_v26_selftest.py"
T_BLOB = "55bcace4105a834c516ed671a83ecf57530b9fe9"
V25_P_BLOB = "8e567ee0f866de00b055bd8c8d1b38a6fd960b60"
V25_T_BLOB = "d297032a3ce9564b276dba2f026b039d24142a45"
V25_H_BLOB = "5251b0a67b4ac18b69edafa55112b5caf25cb4ee"

DEPENDENCY_REGISTER = "docs/governance/DEPENDENCY_REGISTER.md"
DEPENDENCY_FILES = frozenset(set(p.DEPENDENCY_FILES) | {DEPENDENCY_REGISTER})
POLICY_FILES = frozenset({P, T})
ALL_POLICY_FILES = frozenset(set(p.POLICY_FILES) | set(POLICY_FILES))
BOOT = frozenset(set(p.BOOT) | set(POLICY_FILES))

S2_DEPENDENCY_REGISTER_APPEND = b"""
## S2-AUTH-012 exact direct Core dependency decision

This append-only section governs the S2 identity/evidence-store dependency edge. All
preceding S1 evidence remains historical and byte-preserved. This section does not
admit product code, source imports, Git/process/network/model authority, or S3+ scope.

```text
TASK = S2-AUTH-012
DECISION_CLASS = FOCUSED_DIRECT_RUNTIME_DEPENDENCY_ADMISSION
CANONICALIZATION_RULE = EXACT_HEAD_REVIEW_ACCEPTANCE_AND_MERGE_REQUIRED
DIRECT_CORE_DEPENDENCIES = getrandom 0.4.3, sha2 0.10.9
DIRECT_UUID_CORE_EDGE = REJECTED
SOURCE_ADMISSION = NONE
PACKAGE_IDENTITY_DELTA = 0
LOCK_PACKAGE_COUNT = 417_UNCHANGED
TRANSITIVE_PACKAGE_SET_DELTA = 0
PRODUCT_IMPLEMENTATION_AUTHORITY = NONE_FROM_DEPENDENCY_ADMISSION_ALONE
```

The exact lock transition changes only the `wepld-core 0.0.0` dependency stanza.
The `getrandom 0.4.3` and `sha2 0.10.9` package identities and checksums already exist
in the canonical lock graph; transitive presence did not previously grant direct API
authority. The exact candidate therefore adds direct Core edges without adding a new
package identity.

### getrandom 0.4.3

```text
ROLE = OS_RANDOMNESS_FOR_WEPLD_OWNED_OPAQUE_PROJECT_IDS
VERSION = 0.4.3
CRATES_IO_CHECKSUM = 300e883d756b2e4ec94e02791f39b04b522276138852cfc41d9fb7e904106099
SOURCE_REPOSITORY = rust-random/getrandom
SOURCE_REVISION = eeb6a3d4ade21087c0f7bd560192e4bfb8357670
LICENSE = MIT OR Apache-2.0
DIRECT_FEATURES = NONE
CAPABILITY_BOUNDARY = RESULT_BEARING_OS_RANDOMNESS_ONLY
FALLBACK_RANDOMNESS = NONE
TIMESTAMP_PID_PATH_ID_FALLBACK = PROHIBITED
UPDATE_PLAN = PINNED_VERSION_CHANGE_REQUIRES_FRESH_S2_DEPENDENCY_GATES
EXIT_STRATEGY = REPLACE_BEHIND_WEPLD_OWNED_OPAQUE_ID_ALLOCATOR
```

`getrandom` is not identity authority. WePLD owns `ProjectId` semantics, allocation
error handling, catalog reservation, collision/conflict behavior, persistence, and
reassociation. OS-random acquisition failure must remain a typed failure.

### sha2 0.10.9

```text
ROLE = SHA_256_FOR_GENERATION_RECORD_AND_MANIFEST_COHERENCE_DIGESTS
VERSION = 0.10.9
CRATES_IO_CHECKSUM = a7507d819769d01a365ab707794a4084392c824f54a7a6a7862f8c3d0892b283
SOURCE_REPOSITORY = RustCrypto/hashes
SOURCE_REVISION = 82c36a428f8d6f05f3bfccdedb243e9d1f85359d
LICENSE = MIT OR Apache-2.0
DIRECT_FEATURES = default(std)
OPTIONAL_ASM_FEATURE = NOT_ENABLED
AUTHENTICITY_CLAIM = NONE
UPDATE_PLAN = PINNED_VERSION_CHANGE_REQUIRES_FRESH_S2_DEPENDENCY_GATES
EXIT_STRATEGY = REPLACE_BEHIND_WEPLD_OWNED_DIGEST_AND_MANIFEST_CONTRACTS
```

The SHA-256 digest is an unkeyed corruption/coherence mechanism only. It does not
authenticate a store against an actor with writer access.

### Acquisition, security, SBOM, and maintenance accounting

```text
SOURCE_ACQUISITION_LEDGER = ISSUE_212
S1_EXISTING_PACKAGE_SECURITY_LICENSE_EVIDENCE = REUSED_FOR_IDENTICAL_PACKAGE_IDENTITIES
PACKAGE_IDENTITY_DELTA = 0
NEW_LICENSE_IDENTIFIER_DELTA = 0
NEW_CRATE_SOURCE_DELTA = 0
SBOM_COMPONENT_SET_DELTA = 0
SBOM_DEPENDENCY_EDGE_DELTA = wepld-core -> getrandom 0.4.3, sha2 0.10.9
RUSTSEC_SHA2_2021_0100 = NOT_APPLICABLE_TO_0_10_9_PATCHED_RANGE_STARTS_0_9_8
GETRANDOM_SECURITY_BOUNDARY = FAIL_ON_OS_RANDOMNESS_FAILURE
MAINTENANCE_RECHECK = REQUIRED_ON_EVERY_PIN_CHANGE_OR_NEW_ADVISORY
```

Because the exact package set is unchanged, prior target-scoped license and package
security evidence remains applicable to these identical crate identities. The direct
edge change itself is bound by the exact manifest and whole-lock delta and must still
pass the repository's cross-platform Core build/test gates before admission. Any
package/version/feature/package-set drift requires a new dependency decision rather
than inheriting this record.

## S2 dependency authority invariant

```text
DEPENDENCY_REVIEW_OUTCOME != COMPLETION_DECISION
DEPENDENCY_CANDIDATE != CANONICAL_ADMISSION
MERGE_REQUIRED_BEFORE_DIRECT_RUNTIME_ADMISSION = YES
DIRECT_DEPENDENCY_ADMISSION != PRODUCT_IMPLEMENTATION_AUTHORITY
SOURCE_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
GIT_EXECUTION_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
S3_PLUS_AUTHORITY = NONE
```
"""

AUTH = "S2_IDENTITY_STORE_DEPENDENCY_GOVERNANCE_REPAIR"
S2_IMPLEMENTATION_AUTHORITY = "STAGED_EXACT_DEPENDENCY_REGISTER_THEN_IDENTITY_STORE_PATHS_ONLY"
DEPENDENCY_ADMISSION = "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_WITH_REGISTER_ONLY"
SOURCE_ADMISSION = "NONE"

V25_WF = dict(p.WF)
WF = {
    p.FW: "cd7c19d1c7f942f5b558dcf4ca8925c71779933c02327c6d3b87c55c23101407",
    p.AW: "9383de7754a31613cd94ed47499eadab454cac58ae4356b46843ab1ee01fcda4",
    p.CW: p.WF[p.CW],
}

V25_DELTA = p.delta
V25_BASE = p.basectrl
V25_EXT = p.ext
V25_DEXT = p.dext
V25_EEXT = p.eext
V25_ALLOWED = p.allowed
V25_FILES = p.files
V25_PRINTER = p.printer
V25_DEPS_READY = p.deps_ready
V25_BASELINE_DEPENDENCY_STATE = p._baseline_dependency_state

root = p.root
for _path, _expected in (
    (p.P, V25_P_BLOB),
    (p.T, V25_T_BLOB),
    (p.H, V25_H_BLOB),
    (T, T_BLOB),
):
    _actual = p.blob(root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v26 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

_call = p._call
_attr = p._attr
_bind = p._bind
_INST = False
_PRINT: Any = None
_EXPECTED_DESKTOP_EXTENSIONS: frozenset[str] | None = None
_EXPECTED_EXECUTION_EXTENSIONS: frozenset[str] | None = None


def prepare_v25() -> None:
    current = dict(p.WF)
    if current not in (V25_WF, dict(WF)):
        base.fail(f"v26 predecessor workflow identity map drifted: actual={current}")
    p.WF = dict(WF)


def _read_register(view: Any) -> bytes:
    return view.read_bytes(DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES)


def expected_admitted_register(base_register: bytes) -> bytes:
    if S2_DEPENDENCY_REGISTER_APPEND in base_register:
        base.fail("v26 baseline dependency register already contains S2-AUTH-012 decision")
    if not base_register.startswith(b"# Dependency Register\n"):
        base.fail("v26 baseline dependency register header drifted")
    if b"FRESH_IMPLEMENTATION_DEPENDENCIES = 0" not in base_register:
        base.fail("v26 frozen P0 dependency-register evidence is missing")
    if b"UUID/random-ID crate = NOT_ADMITTED" not in base_register:
        base.fail("v26 inherited direct-uuid/random-id non-admission marker drifted")
    return base_register + S2_DEPENDENCY_REGISTER_APPEND


def _baseline_dependency_state(view: Any) -> bool:
    if not V25_BASELINE_DEPENDENCY_STATE(view):
        return False
    register = _read_register(view)
    return S2_DEPENDENCY_REGISTER_APPEND not in register


def deps_ready(view: Any) -> bool:
    if not V25_DEPS_READY(view):
        return False
    register = _read_register(view)
    return (
        register.count(S2_DEPENDENCY_REGISTER_APPEND) == 1
        and register.endswith(S2_DEPENDENCY_REGISTER_APPEND)
    )


def _verify_dependency_candidate(candidate: Any, policy_base: Any) -> None:
    if not _baseline_dependency_state(policy_base):
        base.fail(
            "v26 dependency candidate requires exact canonical baseline "
            "manifest/lock/register state"
        )
    p._verify_dependency_candidate(candidate, policy_base)
    expected = expected_admitted_register(_read_register(policy_base))
    if _read_register(candidate) != expected:
        base.fail("v26 dependency candidate must use exact S2 dependency-register append")
    if not deps_ready(candidate):
        base.fail("v26 dependency candidate did not establish exact governed dependency state")


def delta(candidate: Any, policy_base: Any) -> None:
    paths = p.changed(p.v24.v23, candidate, policy_base)

    if p.bootbase(policy_base):
        if paths == BOOT:
            p.req_v24(candidate)
            p.req_v24(policy_base)
            if not _baseline_dependency_state(candidate) or not _baseline_dependency_state(
                policy_base
            ):
                base.fail(
                    "v26 bootstrap requires unchanged canonical baseline "
                    "manifest/lock/register state"
                )
            return
        if paths & BOOT:
            base.fail(
                "v26 bootstrap delta must be exactly five policy files plus two workflows"
            )
        base.fail(
            "v26 bootstrap base authorizes only exact dependency-governance policy activation"
        )

    if paths & ALL_POLICY_FILES:
        base.fail("canonical v26/v25 policy files are frozen after activation")

    p.req_v24(candidate)
    p.req_v24(policy_base)

    if paths & DEPENDENCY_FILES:
        if paths != DEPENDENCY_FILES:
            base.fail(
                "v26 dependency admission must be exact manifest/lock/register mutation"
            )
        _verify_dependency_candidate(candidate, policy_base)
        return

    V25_DELTA(candidate, policy_base)


def basectrl(candidate: Any, policy_base: Any) -> None:
    V25_BASE(candidate, policy_base)


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(POLICY_FILES & safe_paths):
        if path not in p.ps(candidate):
            base.fail(f"v26 policy file missing: {path}")
        if p.bootbase(policy_base):
            if path in p.ps(policy_base):
                base.fail(f"v26 policy file unexpectedly in bootstrap base: {path}")
        elif path not in p.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v26 steady-state policy file drifted: {path}")
    rest = frozenset(safe_paths - POLICY_FILES)
    if rest:
        V25_EXT(candidate, policy_base, rest)


def dext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, p.extset(p.topo()[3]))


def eext(candidate: Any, policy_base: Any) -> None:
    ext(candidate, policy_base, p.extset(p.topo()[4]))


def allowed(paths: Any, stage: str) -> None:
    remaining = set(paths) - POLICY_FILES - {DEPENDENCY_REGISTER}
    if remaining:
        V25_ALLOWED(remaining, stage)


def files(view: Any) -> None:
    V25_FILES(view)
    missing = POLICY_FILES - p.ps(view)
    if missing:
        base.fail(f"v26 policy files missing: {sorted(missing)}")
    for path in sorted(POLICY_FILES):
        if p.mode(view, path) != "100644":
            base.fail(f"v26 policy file mode invalid: {path}")
    if not (_baseline_dependency_state(view) or deps_ready(view)):
        base.fail(
            "v26 dependency state is neither exact baseline nor exact governed admitted form"
        )


def printer(stage: str, mode_: str) -> None:
    if _PRINT is not V25_PRINTER:
        base.fail("v26 predecessor printer drifted")
    _call("v25 success printer", _PRINT, stage, mode_)
    print("wepld_policy_successor_v26=V25_PLUS_EXACT_DEPENDENCY_GOVERNANCE")
    print(f"v26_authority={AUTH}")
    print(f"s2_implementation_authority_v26={S2_IMPLEMENTATION_AUTHORITY}")
    print(f"dependency_admission_v26={DEPENDENCY_ADMISSION}")
    print(f"source_admission_v26={SOURCE_ADMISSION}")


def overlay() -> None:
    shell, routing, _, desktop, execution = p.topo()
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
        base.fail("v26 installed overlay drifted")
    if p.deps_ready is not deps_ready:
        base.fail("v26 dependency-state hook drifted")
    if dict(p.WF) != dict(WF):
        base.fail("v26 workflow identity projection drifted")


def install() -> None:
    global _INST, _PRINT, _EXPECTED_DESKTOP_EXTENSIONS, _EXPECTED_EXECUTION_EXTENSIONS
    if _INST:
        overlay()
        return

    prepare_v25()
    p.install()
    shell, routing, _, desktop, execution = p.topo()

    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v25 routing hook"), V25_DELTA),
        (base.compare_base_controlled, V25_BASE),
        (_attr(desktop, "verify_extension_controlled_paths", "v25 desktop hook"), V25_DEXT),
        (_attr(execution, "verify_extension_controlled_paths", "v25 execution hook"), V25_EEXT),
        (_attr(shell, "validate_allowed_paths", "v25 allowed hook"), V25_ALLOWED),
        (_attr(shell, "verify_policy_files", "v25 files hook"), V25_FILES),
        (_attr(shell, "print_success", "v25 printer"), V25_PRINTER),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v26 predecessor hook drifted")

    _PRINT = V25_PRINTER
    p.deps_ready = deps_ready
    _EXPECTED_DESKTOP_EXTENSIONS = frozenset(set(p.extset(desktop)) | set(POLICY_FILES))
    _EXPECTED_EXECUTION_EXTENSIONS = frozenset(set(p.extset(execution)) | set(POLICY_FILES))
    _bind(
        desktop,
        "EXTENSION_CONTROLLED_PATHS",
        _EXPECTED_DESKTOP_EXTENSIONS,
        "v26 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        _EXPECTED_EXECUTION_EXTENSIONS,
        "v26 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v26 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v26 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v26 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v26 allowed hook")
    _bind(shell, "verify_policy_files", files, "v26 files hook")
    _bind(shell, "print_success", printer, "v26 printer hook")
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_identity_store_governance_v26_selftest import run

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
                    p.CAND,
                    args.root,
                    args.policy_base_root,
                    args.policy_base_sha,
                )
            )
        return int(_call("runtime verifier", p.RUNTIME, argv))
    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
