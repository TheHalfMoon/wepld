#!/usr/bin/env python3
"""Self-tests for the v49 S2-AUTH-015 bounded Doctor + CLI projection authority."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_doctor_cli_authority_v49_integrity as p

_OVERLAY_VIEW_COUNTER = itertools.count()


class OverlayView:
    def __init__(
        self,
        view: Any,
        replacements: dict[str, bytes] | None = None,
        *,
        omitted: frozenset[str] = frozenset(),
    ) -> None:
        self._view = view
        self._replacements = replacements or {}
        self._omitted = omitted
        self._instance_id = next(_OVERLAY_VIEW_COUNTER)

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v49 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        result = [entry for entry in self._view.entries() if entry.path not in self._omitted]
        known = {entry.path for entry in result}
        for path in self._replacements:
            if path not in known and path not in self._omitted:
                result.append(base.TrackedEntry(mode="100644", path=path))
        return result

    def tree_identity(self, path: str) -> Any:
        return (self._instance_id, path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any, expected: str) -> None:
    try:
        action()
    except (base.PolicyError, FileNotFoundError) as exc:
        if expected not in str(exc):
            base.fail(f"v49 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v49 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_AUTH_015_EXACT_DOCTOR_CLI_PROJECTION_TRANCHE":
        base.fail("v49 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != (
        "EXACT_DOCTOR_CLI_PROJECTION_TRANCHE_ONLY_AFTER_V49_ACTIVATION"
    ):
        base.fail("v49 S2 implementation boundary drift")
    if p.DOCTOR_CLI_AUTHORITY != "DETERMINISTIC_LOCAL_PROJECTION_ORCHESTRATION_ONLY":
        base.fail("v49 must grant exactly the bounded Doctor/CLI projection authority")
    if p.q.DOCTOR_CLI_AUTHORITY != "NONE":
        base.fail("v49 predecessor v48 Doctor/CLI denial drift")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v49 next authority gate drift")
    inherited_unchanged = (
        "DEPENDENCY_ADMISSION",
        "SOURCE_ADMISSION",
        "GIT_ROUTE_DECISION",
        "GIT_PROCESS_ADMISSION",
        "EXTERNAL_PROCESS_AUTHORITY",
        "GIT_EXECUTION_AUTHORITY",
        "NETWORK_AUTHORITY",
        "MODEL_PROVIDER_EXECUTION",
        "S3_PLUS_AUTHORITY",
    )
    for name in inherited_unchanged:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v49 widened or changed inherited authority: {name}")
    for name, value in (
        ("NETWORK_AUTHORITY", p.NETWORK_AUTHORITY),
        ("MODEL_PROVIDER_EXECUTION", p.MODEL_PROVIDER_EXECUTION),
        ("S3_PLUS_AUTHORITY", p.S3_PLUS_AUTHORITY),
        ("GENERAL_SHELL_AUTHORITY", p.GENERAL_SHELL_AUTHORITY),
        ("ARBITRARY_PROCESS_AUTHORITY", p.ARBITRARY_PROCESS_AUTHORITY),
        ("PACKAGE_INSTALL_AUTHORITY", p.PACKAGE_INSTALL_AUTHORITY),
        ("PROJECT_NATIVE_COMMAND_EXECUTION", p.PROJECT_NATIVE_COMMAND_EXECUTION),
        ("GIT_MUTATION_AUTHORITY", p.GIT_MUTATION_AUTHORITY),
        ("SAFE_DIRECTORY_MUTATION_AUTHORITY", p.SAFE_DIRECTORY_MUTATION_AUTHORITY),
        ("REMEDIATION_EXECUTION_AUTHORITY", p.REMEDIATION_EXECUTION_AUTHORITY),
    ):
        if value != "NONE":
            base.fail(f"v49 must not grant {name}")


def _check_projection_contract() -> None:
    for invariant in (
        "CONSUME_TYPED_S2_OBSERVATIONS_ONLY",
        "UNAVAILABLE_IS_NOT_HEALTHY",
        "STALE_IS_NOT_FRESH",
        "PARTIAL_IS_NOT_COMPLETE",
        "TRUST_REFUSED_IS_NOT_TRUSTED",
        "PRESERVE_NATIVE_GIT_TRUST_REFUSAL",
        "ALLOWLISTED_STRUCTURED_FIELDS_ONLY",
        "WEPLD_OWNED_TEMPLATES_ONLY",
        "TERMINAL_CONTROL_SEQUENCE_DEFENSE",
        "HUMAN_AND_JSON_FROM_ONE_REDACTED_MODEL",
        "READ_ONLY_TARGET_PROJECT",
        "NO_REQUIRED_NETWORK_EFFECT",
        "DIGEST_EQUALITY_IS_NOT_AUTHENTICITY",
    ):
        if invariant not in p.DOCTOR_CLI_PROJECTION_CONTRACT:
            base.fail(f"v49 projection contract lost invariant: {invariant}")
    if p.DOCTOR_CLI_COMMAND_SURFACE != ("open", "doctor", "status"):
        base.fail("v49 command surface drift")
    if p.DOCTOR_CLI_EXIT_CLASSES[0] != "0:success":
        base.fail("v49 exit-class contract drift")


def _check_product_scope() -> None:
    expected_files = frozenset(
        {
            "crates/core/src/doctor.rs",
            "crates/core/src/cli.rs",
            "crates/core/src/bin/wepld.rs",
            "crates/core/src/lib.rs",
            "crates/core/tests/doctor_v1.rs",
            "crates/core/tests/cli_v1.rs",
        }
    )
    if p.PRODUCT_FILES != expected_files:
        base.fail("v49 product path allowlist drift")
    if p.PRODUCT_NEW_FILES != expected_files - {"crates/core/src/lib.rs"}:
        base.fail("v49 new-product path set drift")
    if p.CORE_MANIFEST in p.PRODUCT_FILES or p.ROOT_CARGO_LOCK in p.PRODUCT_FILES:
        base.fail("v49 product tranche must not authorize dependency mutation")
    if p.ROOT_CARGO in p.PRODUCT_FILES:
        base.fail("v49 product tranche must not authorize workspace manifest mutation")
    for path in p.PRODUCT_FILES:
        if not path.startswith("crates/core/"):
            base.fail(f"v49 product tranche escaped crates/core: {path}")
    if "S2-CLI003" not in p.PRODUCT_TASKS or "S2-D001" not in p.PRODUCT_TASKS:
        base.fail("v49 product task allowlist drift")
    if any(t.startswith("S2-AUTH") for t in p.PRODUCT_TASKS):
        base.fail("v49 product task allowlist must not claim authority tasks")


def _check_predecessor_exact() -> None:
    p.req_v48(p.raw_root)
    if p.V48_P_BLOB != "69ac03eb9174cce9b8807ee071faf526a9b02c8c":
        base.fail("v49 frozen v48 integrity identity drift")
    if p.V48_T_BLOB != "c2ba6d1d976a2a86879e970966291f4d08b98729":
        base.fail("v49 frozen v48 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._project_for_v48(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v49 workflow projection does not reverse to exact v48: {path}")
        if p._V49_ENTRYPOINT in data:
            base.fail(f"v49 workflow projection left v49 entrypoint: {path}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v49 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v49 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V49_BOOTSTRAP.md": b"# smuggled\n"},
    )
    _expect_failure(
        "v49 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v49 policy files plus two integrity workflows",
    )


def _pre_tranche_core_export() -> bytes:
    lib = p.raw_root.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if p._MOD_CLI_LINE in lib or p._MOD_DOCTOR_LINE in lib:
        return p._strip_doctor_cli_exports(lib)
    return lib


def _synthetic_tranche_lib() -> bytes:
    lib = _pre_tranche_core_export()
    anchor = b"pub mod evidence_store;\n"
    if lib.count(anchor) != 1:
        base.fail("v49 self-test could not anchor the synthetic Core export insert")
    return lib.replace(
        anchor, b"pub mod cli;\npub mod doctor;\n" + anchor, 1
    )


def _synthetic_product_candidate(
    *, extra: dict[str, bytes] | None = None, drop: str | None = None
) -> OverlayView:
    replacements = {
        p.CORE_EXPORT: _synthetic_tranche_lib(),
        p.DOCTOR_MODULE: b"#![allow(dead_code)]\npub fn evaluate() -> u8 { 0 }\n",
        p.CLI_MODULE: b"#![allow(dead_code)]\npub fn dispatch() -> u8 { 0 }\n",
        p.CLI_BIN: b"fn main() { let _ = wepld_core::cli::dispatch(); }\n",
        p.DOCTOR_TEST: b"#[test]\nfn doctor_fixture() { assert_eq!(wepld_core::doctor::evaluate(), 0); }\n",
        p.CLI_TEST: b"#[test]\nfn cli_fixture() { assert_eq!(wepld_core::cli::dispatch(), 0); }\n",
    }
    if drop is not None:
        replacements.pop(drop, None)
    if extra:
        replacements.update(extra)
    return OverlayView(p.raw_root, replacements)


def _check_product_delta_shape() -> None:
    if p._product_presence(p.raw_root):
        return

    candidate = _synthetic_product_candidate()
    p.delta(candidate, p.raw_root)

    mixed = _synthetic_product_candidate(
        extra={"docs/canonical/UNAUTHORIZED_DOCTOR_CLI_MIX.md": b"# nope\n"}
    )
    _expect_failure(
        "v49 product mixed with non-product path",
        lambda: p.delta(mixed, p.raw_root),
        "must not mix with non-product paths",
    )

    missing_bin = _synthetic_product_candidate(drop=p.CLI_BIN)
    _expect_failure(
        "v49 initial product tranche missing exact bin path",
        lambda: p.delta(missing_bin, p.raw_root),
        "initial Doctor/CLI delta must change exact module/bin/export/test set",
    )

    lock_mut = _synthetic_product_candidate(extra={p.ROOT_CARGO_LOCK: b"# tampered lock\n"})
    _expect_failure(
        "v49 product tranche must not mutate Cargo.lock",
        lambda: p.delta(lock_mut, p.raw_root),
        "must not mix with non-product paths",
    )

    manifest_mut = _synthetic_product_candidate(
        extra={p.CORE_MANIFEST: b"[package]\nname = \"wepld-core\"\n"}
    )
    _expect_failure(
        "v49 product tranche must not mutate the core manifest",
        lambda: p.delta(manifest_mut, p.raw_root),
        "must not mix with non-product paths",
    )

    extra_core = _synthetic_product_candidate(
        extra={"crates/core/src/net.rs": b"// unauthorized module\n"}
    )
    _expect_failure(
        "v49 product tranche must not add an unauthorized core module",
        lambda: p.delta(extra_core, p.raw_root),
        "must not mix with non-product paths",
    )

    bad_lib = _synthetic_product_candidate(
        extra={p.CORE_EXPORT: _synthetic_tranche_lib() + b"pub mod smuggled;\n"}
    )
    _expect_failure(
        "v49 product tranche Core export carries an unauthorized extra line",
        lambda: p.delta(bad_lib, p.raw_root),
        "not exactly the two authorized module lines",
    )


def _check_post_tranche_projection() -> None:
    """With a synthetic exact product tranche present, the v49->v48 projection
    must strip both module lines, hide the five new files, and reverse the Core
    export byte-exactly to the frozen canonical frontier so the frozen v48
    cascade sees no Doctor/CLI delta at all."""
    if p._product_presence(p.raw_root):
        return
    post_tranche = _synthetic_product_candidate()
    replacements, omitted = p._doctor_cli_product_projection(post_tranche)
    if omitted != p.PRODUCT_NEW_FILES:
        base.fail("v49 post-tranche projection did not hide the five new product paths")
    if p.CORE_EXPORT not in replacements:
        base.fail("v49 post-tranche projection did not strip the Core export")
    if p.V25.blob(replacements[p.CORE_EXPORT]) != p.REQUIRED_PRODUCT_BASE_BLOBS[p.CORE_EXPORT]:
        base.fail("v49 post-tranche Core export does not reverse to the frozen canonical blob")
    projected = p._project_for_v48(post_tranche)
    for path in sorted(p.PRODUCT_NEW_FILES):
        try:
            projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        except FileNotFoundError:
            continue
        base.fail(f"v49 projected view still exposes a hidden product path: {path}")
    if p._V49_ENTRYPOINT in projected.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES):
        base.fail("v49 post-tranche projection left the v49 workflow entrypoint")
    if projected.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES) != replacements[p.CORE_EXPORT]:
        base.fail("v49 post-tranche projected Core export is not the stripped canonical bytes")


def _check_partial_tranche_fails_closed() -> None:
    if p._product_presence(p.raw_root):
        return
    partial = _synthetic_product_candidate(drop=p.DOCTOR_MODULE)
    _expect_failure(
        "v49 partial tranche in a predecessor view fails closed",
        lambda: p._doctor_cli_product_projection(partial),
        "partial Doctor/CLI tranche",
    )


def _check_product_base_frontier() -> None:
    if p._product_presence(p.raw_root):
        return
    drifted_lib = p.raw_root.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES) + b"\n// drift\n"
    drifted_base = OverlayView(p.raw_root, {p.CORE_EXPORT: drifted_lib})
    anchor = b"pub mod evidence_store;\n"
    candidate = OverlayView(
        drifted_base,
        {
            p.CORE_EXPORT: drifted_lib.replace(
                anchor, b"pub mod cli;\npub mod doctor;\n" + anchor, 1
            ),
            p.DOCTOR_MODULE: b"pub fn evaluate() -> u8 { 0 }\n",
            p.CLI_MODULE: b"pub fn dispatch() -> u8 { 0 }\n",
            p.CLI_BIN: b"fn main() {}\n",
            p.DOCTOR_TEST: b"#[test]\nfn x() {}\n",
            p.CLI_TEST: b"#[test]\nfn y() {}\n",
        },
    )
    _expect_failure(
        "v49 product tranche against drifted canonical frontier",
        lambda: p.delta(candidate, drifted_base),
        "product base frontier drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_projection_contract()
    _check_product_scope()
    _check_predecessor_exact()
    _check_workflow_projection()
    _check_bootstrap_scope()
    _check_product_delta_shape()
    _check_post_tranche_projection()
    _check_partial_tranche_fails_closed()
    _check_product_base_frontier()
    p.install()
    p.overlay()
    print("wepld v49 S2-AUTH-015 Doctor/CLI projection authority self-tests: PASS")


if __name__ == "__main__":
    run()
