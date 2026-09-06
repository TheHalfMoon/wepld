#!/usr/bin/env python3
"""Complete the v55 S2-E015 reopen authorization across the two frozen checks it
was never projected past, and correct one PRE-only assumption in v56's self-test.

v57 is an append-only policy successor over canonical v56 at main
cad321d16cd682ba40bd6b59961cbaccd76a7876. It changes no product rule, grants no
new product or runtime authority, widens no path, and admits no source, process,
network, model/provider, or S3+ capability. Every v56 / v55 authority value is
inherited by reference and asserted unchanged, including
`TEST_CHILD_PROCESS_AUTHORITY = RE_EXEC_CURRENT_TEST_BINARY_ONLY` and every
`NONE` denial.

Two frozen checks still reject the exact S2-E015 fixture that v55 authorized.

1. v28's `_hardened_product_verify`
   (`wepld_s2_identity_store_governance_v28_integrity`, bound over
   `wepld_s2_identity_store_bootstrap_v25_integrity._verify_product_files`)
   extends the v25 `FORBIDDEN_PRODUCT_TOKENS` scan to
   `crates/core/tests/identity_store_v1.rs`. That token list forbids
   `std::process`, `Command::`, `std::env`, `expect(` (among many others).
   v55's `_verify_test_child_process_bounds` *requires*
   `std::process::Command::new(std::env::current_exe())` in that exact file for
   the S2-E015 process-crash oracle - the two are directly contradictory.
   v55's `delta()` intercepts `REOPEN_FILES` so the scan is skipped there, but
   v55's `files()` delegates the reopened path unprojected, so
   `verify-remote` / `verify-candidate-local` fail
   `v25 identity/store tranche contains unauthorized token: std::process`.

   v57 rebinds `_verify_product_files` so that, and only when, the reopened
   path's blob is exactly v56's `AUTHORIZED_POST_REOPEN_BLOB`, the test file is
   scanned against `FORBIDDEN_PRODUCT_TOKENS` minus exactly
   `{std::process, Command::, std::env, expect(}` - the constructs v55's
   `TEST_CHILD_PROCESS_AUTHORITY` static bound already governs, plus `expect(`
   for the child role that re-execs and then `std::process::abort()`s without a
   return path. Every other forbidden token (`unwrap(`, `panic!`, `std::net`,
   `Tcp*`, `remove_file`, `symlink`, `tokio`, `reqwest`, `unsafe {`, ...) stays
   enforced, and v57 also re-runs v55's `_verify_test_child_process_bounds` on
   that file so the permitted tokens are proven to be exactly the bounded
   re-exec pattern. For every other path, and for the reopened path in any
   other state, the inherited v28 `_hardened_product_verify` runs byte-for-byte
   unchanged, including the full scan of `identity.rs` and `evidence_store.rs`.

2. v56's own self-test hard-asserts that the real tree's reopened path is the
   PRE transition side (`_check_live_transition_side`, and the `gated_pre`
   branch of `_check_projection_is_one_path_and_gated`). v56's *integrity*
   module already handles PRE and POST correctly - only these two self-test
   checks assumed PRE. Once the fixture is canonical the tree is POST, so on
   every subsequent run those checks would fail and red-line
   `foundation-integrity` on `main`. v57 replaces exactly those two check
   functions, for the duration of the frozen v56 self-test cascade, with
   versions that accept PRE or POST for the real tree and keep every other
   assertion (POST accepted only for the exact authorized blob, PRE accepted
   only for the exact pre-reopen blob, a third blob rejected, a missing path
   rejected, the projection scoped to exactly one path).

Invariants this file makes explicit:

    V57_POLICY_REPAIR != NEW_RUNTIME_AUTHORITY
    TOKEN_SCAN_EXCEPTION != TOKEN_SCAN_REMOVAL
    AUTHORIZED_REOPEN != UNBOUNDED_FILE_MUTATION

Package-load / resting-view note: v57 follows the v45..v56 discipline. It owns a
fresh `LocalRepositoryView` of the exact checked-out head, imports frozen v56
under an exact v57->v56 workflow-entrypoint reversal, and inherits every v56
hook by reference.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

import wepld_integrity as base

P = ".github/scripts/wepld_s2_e015_reopen_token_scan_projection_repair_v57_integrity.py"
T = ".github/scripts/wepld_s2_e015_reopen_token_scan_projection_repair_v57_selftest.py"
T_BLOB = "9dfe73d145ace7e96eb30583bcae2a4109167968"

V56_P_BLOB = "e70a9f5d122dfcce29d6470ad3226bfa4a834115"
V56_T_BLOB = "8a6d32d6bee55ea0b61bf97eebb497c27563bfaf"

FW = ".github/workflows/foundation-integrity.yml"
AW = ".github/workflows/s1-admission-integrity.yml"
_V57_ENTRYPOINT = b"wepld_s2_e015_reopen_token_scan_projection_repair_v57_integrity.py"
_V56_ENTRYPOINT = b"wepld_s2_e015_frontier_projection_repair_v56_integrity.py"
_WORKFLOW_ENTRYPOINT_COUNTS = {FW: 3, AW: 2}

raw_root = base.LocalRepositoryView(Path(__file__).resolve().parents[2])


def _v56_workflow_bytes(data: bytes, path: str) -> bytes:
    count = data.count(_V57_ENTRYPOINT)
    if count != _WORKFLOW_ENTRYPOINT_COUNTS[path]:
        base.fail(
            "v57 workflow entrypoint count drifted before v56 projection: "
            f"{path} expected={_WORKFLOW_ENTRYPOINT_COUNTS[path]} actual={count}"
        )
    return data.replace(_V57_ENTRYPOINT, _V56_ENTRYPOINT)


def _import_v56_under_workflow_projection() -> Any:
    """Import frozen v56 while it observes exact v56 workflow bytes."""
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v56_import_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        data = original_read_bytes(local_view, relative, limit)
        if relative in (FW, AW):
            data = _v56_workflow_bytes(data, relative)
            if len(data) > limit:
                base.fail(
                    f"v57 v56-import workflow projection exceeds read bound: {relative}"
                )
        return data

    base.LocalRepositoryView.read_bytes = _v56_import_read_bytes
    try:
        return importlib.import_module(
            "wepld_s2_e015_frontier_projection_repair_v56_integrity"
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes


q = _import_v56_under_workflow_projection()

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
PRE_REOPEN_BLOB = q.PRE_REOPEN_BLOB
AUTHORIZED_POST_REOPEN_BLOB = q.AUTHORIZED_POST_REOPEN_BLOB

AUTH = "S2_E015_REOPEN_TOKEN_SCAN_PROJECTION_REPAIR_ONLY"
V57_POLICY_REPAIR = "NOT_NEW_RUNTIME_AUTHORITY"
TOKEN_SCAN_EXCEPTION = "NOT_TOKEN_SCAN_REMOVAL"
AUTHORIZED_REOPEN_BOUND = "NOT_UNBOUNDED_FILE_MUTATION"
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

for _path, _expected in ((q.P, V56_P_BLOB), (q.T, V56_T_BLOB), (T, T_BLOB)):
    _actual = V25.blob(raw_root.read_bytes(_path, base.MAX_POLICY_FILE_BYTES))
    if _actual != _expected:
        base.fail(
            f"frozen v57 package input drifted: {_path}: "
            f"expected={_expected} actual={_actual}"
        )

# --- inherited identity/store token-scan machinery -------------------------
import wepld_s1_execution_integrity as _execution
import wepld_s2_identity_store_v25_support as _v25support
import wepld_s2_identity_store_bootstrap_v25_integrity as _v25mod
import wepld_s2_identity_store_governance_v28_integrity as _v28mod

# The v28 hardened verifier as canonical `main` installs it, captured before
# v57 rebinds anything.
_V28_HARDENED = _v28mod._hardened_product_verify
# v25's original product verifier (structural for every PRODUCT_FILE plus the
# full FORBIDDEN_PRODUCT_TOKENS scan of identity.rs and evidence_store.rs, but
# not the test file), captured by v28 at its own import.
_V25_ORIGINAL_PRODUCT_VERIFY = _v28mod.R_V25_PRODUCT_VERIFY
_PRODUCT_TEST = _v25mod.PRODUCT_TEST

if _PRODUCT_TEST != IDENTITY_STORE_TEST:
    base.fail("v57 v25 PRODUCT_TEST is not the reopened S2-E015 path")
# The installed identity of `_verify_product_files` is only meaningful after the
# cascade's `install()` has run; v57's own `install()` asserts it equals
# `_V28_HARDENED` before rebinding.

# The tokens permitted in the reopened test file, and only in the exact
# authorized post-reopen state. These are the constructs v55's
# `_verify_test_child_process_bounds` already governs, plus `expect(` for the
# child role that re-execs and `std::process::abort()`s.
_AUTHORIZED_TEST_TOKEN_EXCEPTIONS = frozenset(
    {b"std::process", b"Command::", b"std::env", b"expect("}
)
for _tok in _AUTHORIZED_TEST_TOKEN_EXCEPTIONS:
    if _tok not in _v25support.FORBIDDEN_PRODUCT_TOKENS:
        base.fail(f"v57 exception token is not in the inherited forbidden set: {_tok!r}")

# v55's static child-process bound, reached through the inherited chain.
_V55 = q.q
_V55_CHILD_PROCESS_BOUND = _V55._verify_test_child_process_bounds


def _scan_authorized_reopen_test(view: Any) -> None:
    """Scan the reopened S2-E015 test file against the inherited forbidden-token
    set minus exactly the authorized re-exec exceptions, and re-assert v55's
    child-process static bound on it. Only ever reached for the exact
    authorized post-reopen blob.
    """
    src = view.read_bytes(_PRODUCT_TEST, base.MAX_POLICY_FILE_BYTES)
    if V25.blob(src) != AUTHORIZED_POST_REOPEN_BLOB:
        base.fail("v57 authorized-reopen scan reached a non-authorized blob")
    if _v25support.mode(view, _PRODUCT_TEST) != "100644":
        base.fail(f"v57 reopened test file mode invalid: {_PRODUCT_TEST}")
    if not src.startswith(b"#![forbid(unsafe_code)]"):
        base.fail(f"v57 reopened test file must forbid unsafe code: {_PRODUCT_TEST}")
    try:
        scrubbed = _execution.strip_rust_comments_and_strings(src.decode("utf-8"))
    except UnicodeDecodeError:
        base.fail(f"v57 reopened test file is not UTF-8: {_PRODUCT_TEST}")
    normalized = "".join(scrubbed.split()).encode("utf-8")
    for token in _v25support.FORBIDDEN_PRODUCT_TOKENS:
        if token in _AUTHORIZED_TEST_TOKEN_EXCEPTIONS:
            continue
        if b"".join(token.split()) in normalized:
            base.fail(
                "v57 S2-E015 fixture contains a token not permitted even for the "
                "authorized reopen: " + token.decode("ascii", errors="replace")
            )
    _call(
        "v57 re-assert v55 TEST_CHILD_PROCESS_AUTHORITY static bound on the fixture",
        _V55_CHILD_PROCESS_BOUND,
        view,
    )


def _v57_hardened_product_verify(view: Any) -> None:
    """Replacement for the installed `_verify_product_files` (v28's hardened
    one). For every path and state except the reopened test file at the exact
    authorized post-reopen blob, this is v28's verifier byte-for-byte. For that
    one file in that one state, the full-forbidden-token scan of the test file
    is replaced by `_scan_authorized_reopen_test`; identity.rs and
    evidence_store.rs are still fully scanned by `_V25_ORIGINAL_PRODUCT_VERIFY`.
    """
    paths = _v25support.ps(view)
    if _PRODUCT_TEST not in paths:
        _V28_HARDENED(view)
        return
    actual = V25.blob(view.read_bytes(_PRODUCT_TEST, base.MAX_POLICY_FILE_BYTES))
    if actual != AUTHORIZED_POST_REOPEN_BLOB:
        _V28_HARDENED(view)
        return
    _V25_ORIGINAL_PRODUCT_VERIFY(view)
    _scan_authorized_reopen_test(view)


def _workflow_replacements(view: Any) -> dict[str, bytes]:
    replacements: dict[str, bytes] = {}
    for path in (FW, AW):
        data = view.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        predecessor = _v56_workflow_bytes(data, path)
        actual = V25.sha(predecessor)
        if actual != Q_WF[path]:
            base.fail(
                "v57 workflow does not reverse to exact canonical v56 predecessor: "
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


def req_v56(view: Any) -> None:
    for path, expected in ((q.P, V56_P_BLOB), (q.T, V56_T_BLOB)):
        if path not in V25.ps(view):
            base.fail(f"v57 candidate/base is missing frozen v56 predecessor: {path}")
        actual = V25.blob(view.read_bytes(path, base.MAX_POLICY_FILE_BYTES))
        if actual != expected:
            base.fail(
                f"frozen v56 predecessor drifted: {path}: "
                f"expected={expected} actual={actual}"
            )


def _project_for_v56(view: Any) -> Any:
    return _ProjectionView(view, _workflow_replacements(view), POLICY_FILES)


def _v56_views(candidate: Any, policy_base: Any) -> tuple[Any, Any]:
    projected_candidate = _project_for_v56(candidate)
    if bootbase(policy_base):
        return projected_candidate, policy_base
    return projected_candidate, _project_for_v56(policy_base)


# --- v56 self-test PRE-only-assumption correction -------------------------
def _v57_check_live_transition_side() -> None:
    import wepld_s2_e015_frontier_projection_repair_v56_selftest as v56st

    p = v56st.p
    OverlayView = v56st.OverlayView
    idpath = v56st.IDPATH
    _expect_failure = v56st._expect_failure

    side = p._live_transition_side(p.raw_root)
    if side not in ("PRE", "POST"):
        base.fail(f"v56 real tree must be a pinned transition side: got {side}")

    post_view = OverlayView(p.raw_root, {idpath: p._POST_REOPEN_BYTES})
    if p._live_transition_side(post_view) != "POST":
        base.fail("v56 must accept the exact authorized post-reopen blob as POST")
    pre_view = OverlayView(p.raw_root, {idpath: p._PRE_REOPEN_BYTES})
    if p._live_transition_side(pre_view) != "PRE":
        base.fail("v56 must accept the exact pre-reopen blob as PRE")

    third = OverlayView(p.raw_root, {idpath: b"// v57 self-test: an arbitrary third state\n"})
    _expect_failure(
        "v56 rejects a third blob for the reopened path",
        lambda: p._live_transition_side(third),
        "neither pinned transition side",
    )
    gone = OverlayView(p.raw_root, {}, omitted=frozenset({idpath}))
    _expect_failure(
        "v56 rejects a tree missing the reopened frontier path",
        lambda: p._live_transition_side(gone),
        "requires the reopened frontier path",
    )


def _v57_check_projection_is_one_path_and_gated() -> None:
    import wepld_s2_e015_frontier_projection_repair_v56_selftest as v56st
    import wepld_s2_git_route_governance_v36_integrity as v36

    p = v56st.p
    OverlayView = v56st.OverlayView
    idpath = v56st.IDPATH
    identity_src = v56st.IDENTITY_SRC
    store_src = v56st.STORE_SRC
    core_export = v56st.CORE_EXPORT
    _expect_failure = v56st._expect_failure

    original = base.LocalRepositoryView.read_bytes
    limit = base.MAX_POLICY_FILE_BYTES

    real_id = p.raw_root.read_bytes(idpath, limit)
    real_identity_src = p.raw_root.read_bytes(identity_src, limit)
    real_store_src = p.raw_root.read_bytes(store_src, limit)
    real_export = p.raw_root.read_bytes(core_export, limit)
    side = p._live_transition_side(p.raw_root)

    if v36.REQUIRED_CANONICAL_FRONTIER_BLOBS[idpath] != p.PRE_REOPEN_BLOB:
        base.fail("v56 PRE_REOPEN_BLOB is not the live v36 frontier pin for the reopened path")

    # Gate + wrapper together, authorized POST tree: gate resolves POST, the
    # wrapper projects exactly the one reopened path back to the v36 pin.
    post_tree = OverlayView(p.raw_root, {idpath: p._POST_REOPEN_BYTES})
    gated_post = p._gated_selftest_read_bytes_wrapper(post_tree, original)
    projected = gated_post(p.raw_root, idpath, limit)
    if p.V25.blob(projected) != v36.REQUIRED_CANONICAL_FRONTIER_BLOBS[idpath]:
        base.fail("v56 POST projection did not restore exactly the v36-pinned pre-reopen bytes")

    # Gate + wrapper together, third-blob tree: fails closed at the gate.
    third_tree = OverlayView(p.raw_root, {idpath: b"// v57 self-test: a third state\n"})
    _expect_failure(
        "v56 gate rejects a third blob before a wrapper is built",
        lambda: p._gated_selftest_read_bytes_wrapper(third_tree, original),
        "neither pinned transition side",
    )

    # Gate + wrapper together, explicit PRE tree: no projection - passthrough to
    # whatever the real tree holds.
    pre_tree = OverlayView(p.raw_root, {idpath: p._PRE_REOPEN_BYTES})
    gated_pre = p._gated_selftest_read_bytes_wrapper(pre_tree, original)
    if gated_pre(p.raw_root, idpath, limit) != real_id:
        base.fail("v56 PRE gate must not project the reopened path")

    # Gate + wrapper on the REAL tree, whichever pinned side it is.
    gated_real = p._gated_selftest_read_bytes_wrapper(p.raw_root, original)
    got_real = gated_real(p.raw_root, idpath, limit)
    if side == "PRE":
        if got_real != real_id:
            base.fail("v56 PRE real tree must not project the reopened path")
    elif p.V25.blob(got_real) != v36.REQUIRED_CANONICAL_FRONTIER_BLOBS[idpath]:
        base.fail("v56 POST real tree must project the reopened path to the v36 pin")

    # Nothing else moves under the POST gate+wrapper.
    if gated_post(p.raw_root, identity_src, limit) != real_identity_src:
        base.fail("v56 projection altered crates/core/src/identity.rs")
    if gated_post(p.raw_root, store_src, limit) != real_store_src:
        base.fail("v56 projection altered crates/core/src/evidence_store.rs")
    if gated_post(p.raw_root, core_export, limit) != real_export:
        base.fail("v56 projection altered crates/core/src/lib.rs")

    wf_replacements = p._workflow_replacements(p.raw_root)
    for wf in (p.FW, p.AW):
        gated_wf = gated_post(p.raw_root, wf, limit)
        if gated_wf != wf_replacements[wf]:
            base.fail(f"v56 gate+wrapper workflow bytes are not the v55 reversal: {wf}")
        if p._V56_ENTRYPOINT in gated_wf:
            base.fail(f"v56 gate+wrapper left the v56 workflow entrypoint: {wf}")

    _expect_failure(
        "v56 projection respects the read bound",
        lambda: gated_post(p.raw_root, idpath, 16),
        "exceeds read bound",
    )


def run_predecessor_selftests() -> None:
    """Run frozen v56's own self-tests once, under the v57->v56 workflow
    reversal, with v56's two PRE-only real-tree assertions replaced for the
    duration by PRE-or-POST-agnostic equivalents. v56's own
    `run_predecessor_selftests` (invoked inside `q.selftest`) still applies the
    S2-E015 frontier projection for the deeper v55..v21 cascade.
    """
    import wepld_s2_e015_frontier_projection_repair_v56_selftest as v56st

    workflow_reversal = _workflow_replacements(raw_root)
    original_read_bytes = base.LocalRepositoryView.read_bytes

    def _v56_selftest_read_bytes(local_view: Any, relative: str, limit: int) -> bytes:
        if relative in workflow_reversal:
            data = workflow_reversal[relative]
            if len(data) > limit:
                base.fail(
                    f"v57 v56-selftest workflow projection exceeds read bound: {relative}"
                )
            return data
        return original_read_bytes(local_view, relative, limit)

    _orig_lts = v56st._check_live_transition_side
    _orig_proj = v56st._check_projection_is_one_path_and_gated
    v56st._check_live_transition_side = _v57_check_live_transition_side
    v56st._check_projection_is_one_path_and_gated = _v57_check_projection_is_one_path_and_gated
    base.LocalRepositoryView.read_bytes = _v56_selftest_read_bytes
    try:
        _call(
            "v56 self-tests under v57->v56 reversal + PRE-or-POST real-tree assertions",
            q.selftest,
        )
    finally:
        base.LocalRepositoryView.read_bytes = original_read_bytes
        v56st._check_live_transition_side = _orig_lts
        v56st._check_projection_is_one_path_and_gated = _orig_proj


def delta(candidate: Any, policy_base: Any) -> None:
    paths = V25.changed(V25.v24.v23, candidate, policy_base)

    if bootbase(policy_base):
        if paths != BOOT:
            if paths & BOOT:
                base.fail(
                    "v57 bootstrap delta must be exactly two v57 policy files plus "
                    "two integrity workflows"
                )
            base.fail(
                "v57 bootstrap base authorizes only exact reopen-token-scan "
                "projection-repair policy activation"
            )
        req_v56(candidate)
        req_v56(policy_base)
        return

    if paths & CONTROLLED_FILES:
        base.fail("canonical v57 policy files are frozen after activation")

    q.delta(_project_for_v56(candidate), _project_for_v56(policy_base))


def basectrl(candidate: Any, policy_base: Any) -> None:
    if not bootbase(policy_base):
        q.basectrl(*_v56_views(candidate, policy_base))
        return
    for path in sorted(base.BASE_CONTROLLED_PATHS):
        candidate_bytes = candidate.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        base_bytes = policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if path in (FW, AW):
            if V25.sha(candidate_bytes) != WF[path] or V25.sha(base_bytes) != Q_WF[path]:
                base.fail(f"v57 bootstrap workflow drifted: {path}")
        elif candidate_bytes != base_bytes:
            base.fail(f"base-controlled policy/governance path changed: {path}")


def ext(candidate: Any, policy_base: Any, safe: Any) -> None:
    safe_paths = frozenset(safe)
    for path in sorted(CONTROLLED_FILES & safe_paths):
        if path not in V25.ps(candidate):
            base.fail(f"v57 controlled file missing: {path}")
        if bootbase(policy_base):
            if path in V25.ps(policy_base):
                base.fail(
                    f"v57 controlled file unexpectedly exists in bootstrap base: {path}"
                )
        elif path not in V25.ps(policy_base) or candidate.read_bytes(
            path, base.MAX_POLICY_FILE_BYTES
        ) != policy_base.read_bytes(path, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v57 steady-state controlled file drifted: {path}")

    rest = frozenset(safe_paths - CONTROLLED_FILES)
    if rest:
        projected_candidate, projected_base = _v56_views(candidate, policy_base)
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
    q.files(_project_for_v56(view))
    approved = {
        P: raw_root.read_bytes(P, base.MAX_POLICY_FILE_BYTES),
        T: raw_root.read_bytes(T, base.MAX_POLICY_FILE_BYTES),
    }
    for path in sorted(CONTROLLED_FILES):
        if path not in V25.ps(view):
            base.fail(f"v57 controlled file missing: {path}")
        if V25.mode(view, path) != "100644":
            base.fail(f"v57 controlled file mode invalid: {path}")
        if view.read_bytes(path, base.MAX_POLICY_FILE_BYTES) != approved[path]:
            base.fail(f"v57 controlled file content drifted: {path}")


def verify_component_base(
    view: Any,
    paths: set[str],
    *,
    allow_core_main_change: bool,
) -> None:
    if _PREDECESSOR_COMPONENT_BASE is None:
        base.fail("v57 predecessor component-base hook unavailable")
    _call(
        "v57 predecessor component-base verifier",
        _PREDECESSOR_COMPONENT_BASE,
        _project_for_v56(view),
        set(paths) - CONTROLLED_FILES,
        allow_core_main_change=allow_core_main_change,
    )


def freeze_s1_007_state(candidate: Any, policy_base: Any) -> None:
    if _PREDECESSOR_FREEZE_S1 is None:
        base.fail("v57 predecessor S1 freeze hook unavailable")
    projected_candidate, projected_base = _v56_views(candidate, policy_base)
    _call(
        "v57 predecessor S1 state freeze",
        _PREDECESSOR_FREEZE_S1,
        projected_candidate,
        projected_base,
    )


def printer(stage: str, mode_: str) -> None:
    q.printer(stage, mode_)
    print("wepld_policy_successor_v57=S2_E015_REOPEN_TOKEN_SCAN_PROJECTION_REPAIR_ONLY")
    print(f"v57_authority={AUTH}")
    print(f"v57_policy_repair={V57_POLICY_REPAIR}")
    print(f"token_scan_exception_v57={TOKEN_SCAN_EXCEPTION}")
    print(
        "authorized_test_token_exceptions_v57="
        + ",".join(sorted(t.decode("ascii") for t in _AUTHORIZED_TEST_TOKEN_EXCEPTIONS))
    )
    print(f"authorized_post_reopen_blob_v57={AUTHORIZED_POST_REOPEN_BLOB}")
    print(f"test_child_process_authority_v57={TEST_CHILD_PROCESS_AUTHORITY}")
    print(f"general_shell_authority_v57={GENERAL_SHELL_AUTHORITY}")
    print(f"arbitrary_process_authority_v57={ARBITRARY_PROCESS_AUTHORITY}")
    print(f"package_install_authority_v57={PACKAGE_INSTALL_AUTHORITY}")
    print(f"project_native_command_execution_v57={PROJECT_NATIVE_COMMAND_EXECUTION}")
    print(f"git_mutation_authority_v57={GIT_MUTATION_AUTHORITY}")
    print(f"network_authority_v57={NETWORK_AUTHORITY}")
    print(f"model_provider_execution_v57={MODEL_PROVIDER_EXECUTION}")
    print(f"s3_plus_authority_v57={S3_PLUS_AUTHORITY}")
    print(f"next_authority_gate_v57={NEXT_AUTHORITY_GATE}")


def _chain() -> tuple[Any, ...]:
    return (q,) + q._chain()


def prepare_q() -> None:
    for module in _chain():
        current = dict(module.WF)
        if current not in (Q_WF, dict(WF)):
            base.fail(f"v57 predecessor workflow identity map drifted: actual={current}")
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
        base.fail("v57 installed overlay drifted")
    if any(dict(module.WF) != dict(WF) for module in _chain()):
        base.fail("v57 workflow identity projection drifted")
    for name in _INHERITED_AUTHORITY_NAMES:
        if getattr(q, name) != globals()[name]:
            base.fail(f"v57 inherited authority drifted: {name}")
    if _v25mod._verify_product_files is not _v57_hardened_product_verify:
        base.fail("v57 product-verify projection drifted")
    if _v28mod._hardened_product_verify is not _v57_hardened_product_verify:
        base.fail("v57 v28 hardened-verify supersession drifted")
    if q.AUTHORIZED_POST_REOPEN_BLOB != AUTHORIZED_POST_REOPEN_BLOB:
        base.fail("v57 inherited v56 authorized-post-reopen blob drifted")


def install() -> None:
    global _INST, _PREDECESSOR_COMPONENT_BASE, _PREDECESSOR_FREEZE_S1
    if _INST:
        overlay()
        return

    q.install()

    shell, routing, _, desktop, execution = V25.topo()
    pairs = (
        (_attr(routing, "IMPL_REQUIRE_EXACT_DELTA", "v56 routing hook"), q.delta),
        (base.compare_base_controlled, q.basectrl),
        (
            _attr(desktop, "verify_extension_controlled_paths", "v56 desktop hook"),
            q.dext,
        ),
        (
            _attr(execution, "verify_extension_controlled_paths", "v56 execution hook"),
            q.eext,
        ),
        (_attr(shell, "validate_allowed_paths", "v56 allowed hook"), q.allowed),
        (_attr(shell, "verify_policy_files", "v56 files hook"), q.files),
        (_attr(shell, "print_success", "v56 printer"), q.printer),
    )
    if any(actual is not expected for actual, expected in pairs):
        base.fail("v57 predecessor hook drifted")
    if _v25mod._verify_product_files is not _V28_HARDENED:
        base.fail("v57 predecessor product-verify hook drifted")

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
        "v57 desktop registration",
    )
    _bind(
        execution,
        "EXTENSION_CONTROLLED_PATHS",
        execution_extensions,
        "v57 execution registration",
    )
    _bind(routing, "IMPL_REQUIRE_EXACT_DELTA", delta, "v57 routing hook")
    base.compare_base_controlled = basectrl
    _bind(desktop, "verify_extension_controlled_paths", dext, "v57 desktop hook")
    _bind(execution, "verify_extension_controlled_paths", eext, "v57 execution hook")
    _bind(shell, "validate_allowed_paths", allowed, "v57 allowed hook")
    _bind(shell, "verify_policy_files", files, "v57 files hook")
    _bind(shell, "print_success", printer, "v57 printer hook")
    _bind(
        execution,
        "_verify_component_base",
        verify_component_base,
        "v57 component-base hook",
    )
    _bind(
        execution,
        "freeze_s1_007_state",
        freeze_s1_007_state,
        "v57 S1 state freeze hook",
    )
    _bind(
        _v25mod,
        "_verify_product_files",
        _v57_hardened_product_verify,
        "v57 identity/store product-verify projection",
    )
    _bind(
        _v28mod,
        "_hardened_product_verify",
        _v57_hardened_product_verify,
        "v57 v28 hardened-verify supersession",
    )
    _INST = True
    overlay()


def selftest() -> None:
    from wepld_s2_e015_reopen_token_scan_projection_repair_v57_selftest import run

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
