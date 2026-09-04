#!/usr/bin/env python3
"""Self-tests for the v51 S2-D012 bounded security-sensitive Git-config observation authority."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_security_sensitive_config_observation_v51_integrity as p

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
                base.fail(f"v51 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v51 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v51 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_D012_BOUNDED_SECURITY_SENSITIVE_GIT_CONFIG_OBSERVATION_ONLY":
        base.fail("v51 authority marker drift")
    if p.S2_IMPLEMENTATION_AUTHORITY != (
        "EXACT_SECURITY_SENSITIVE_GIT_CONFIG_OBSERVATION_TRANCHE_ONLY_AFTER_V51_ACTIVATION"
    ):
        base.fail("v51 S2 implementation boundary drift")
    if p.SECURITY_SENSITIVE_CONFIG_OBSERVATION_AUTHORITY != (
        "BOUNDED_CLOSED_LOCAL_GIT_CONFIG_GET_REGEXP_CLASSIFICATION_ONLY"
    ):
        base.fail("v51 must grant exactly the bounded security-sensitive config observation authority")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v51 next authority gate drift")
    inherited_unchanged = (
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
    )
    for name in inherited_unchanged:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v51 widened or changed inherited authority: {name}")
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
            base.fail(f"v51 must not grant {name}")


def _check_config_query_contract() -> None:
    for query in (
        "REMOTE_URL",
        "REMOTE_PUSHURL",
        "CREDENTIAL_HELPER",
        "HTTP_EXTRAHEADER",
        "HTTP_PROXY",
        "URL_INSTEADOF",
        "URL_PUSHINSTEADOF",
        "CORE_SSHCOMMAND",
    ):
        if query not in p.CLOSED_CONFIG_QUERY_FAMILY:
            base.fail(f"v51 closed config-query family lost a member: {query}")
    if len(p.CLOSED_CONFIG_QUERY_FAMILY) != 8:
        base.fail("v51 closed config-query family must be exactly the eight authorized classes")
    for invariant in (
        "LOCAL_SCOPE_ONLY",
        "NO_INCLUDES",
        "NO_USER_SUPPLIED_KEY_PATTERN",
        "TRANSIENT_CLASSIFICATION_RAW_VALUE_DISCARDED",
        "SAFE_COUNT_CLASS_OUTPUT_ONLY",
        "NO_NETWORK_EFFECT",
        "REUSES_QUALIFIED_GIT_EXECUTABLE",
        "NO_NEW_GIT_EXECUTABLE_DISCOVERY_PATH",
    ):
        if invariant not in p.SECURITY_SENSITIVE_CONFIG_OBSERVATION_CONTRACT:
            base.fail(f"v51 observation contract lost invariant: {invariant}")


def _check_product_scope() -> None:
    expected_new = frozenset({"crates/core/tests/security_sensitive_config_v1.rs"})
    expected_existing = frozenset(
        {
            "crates/core/src/git_topology.rs",
            "crates/core/src/doctor.rs",
            "crates/core/src/bin/wepld.rs",
            "crates/core/tests/doctor_v1.rs",
            "crates/core/tests/cli_v1.rs",
        }
    )
    if p.PRODUCT_NEW_FILES != expected_new:
        base.fail("v51 new-product path set drift")
    if p.PRODUCT_EXISTING_FILES != expected_existing:
        base.fail("v51 second-stage product path set drift")
    if p.PRODUCT_FILES != expected_new | expected_existing:
        base.fail("v51 product path allowlist drift")
    if p.CORE_MANIFEST in p.PRODUCT_FILES or p.ROOT_CARGO_LOCK in p.PRODUCT_FILES:
        base.fail("v51 product tranche must not authorize dependency mutation")
    if p.ROOT_CARGO in p.PRODUCT_FILES:
        base.fail("v51 product tranche must not authorize workspace manifest mutation")
    if "crates/core/src/lib.rs" in p.PRODUCT_FILES:
        base.fail("v51 product tranche must not touch the shared Core export")
    for path in p.PRODUCT_FILES:
        if not path.startswith("crates/core/"):
            base.fail(f"v51 product tranche escaped crates/core: {path}")
    if "S2-D012" not in p.PRODUCT_TASKS:
        base.fail("v51 product task allowlist must claim S2-D012")
    if any(t.startswith("S2-AUTH") for t in p.PRODUCT_TASKS):
        base.fail("v51 product task allowlist must not claim authority tasks")
    if set(p.REQUIRED_PRODUCT_BASE_BLOBS) != p.PRODUCT_EXISTING_FILES:
        base.fail("v51 frozen product-base blob set does not match the second-stage file set")


def _check_predecessor_exact() -> None:
    p.req_v50(p.raw_root)
    if p.V50_P_BLOB != "4569222135e4ae85075368d73270d46e7453f18d":
        base.fail("v51 frozen v50 integrity identity drift")
    if p.V50_T_BLOB != "418645059a4625fb2734f97ee1a5e909d4512615":
        base.fail("v51 frozen v50 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._project_for_v50(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v51 workflow projection does not reverse to exact v50: {path}")
        if p._V51_ENTRYPOINT in data:
            base.fail(f"v51 workflow projection left the v51 entrypoint: {path}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v51 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v51 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V51_BOOTSTRAP.md": b"# smuggled\n"},
    )
    _expect_failure(
        "v51 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v51 policy files plus two integrity workflows",
    )


def _synthetic_new_test_file() -> bytes:
    return (
        b"#![forbid(unsafe_code)]\n"
        b"#[test]\n"
        b"fn security_sensitive_config_fixture() { assert_eq!(1 + 1, 2); }\n"
    )


def _synthetic_product_candidate(*, extra: dict[str, bytes] | None = None) -> OverlayView:
    """An exact-shape synthetic candidate: the one wholly new file, plus a
    trivial (comment-only) touch to each of the five already-landed
    second-stage files, so its changed-path set is exactly `PRODUCT_FILES` -
    matching what `delta()` requires of a genuine initial candidate.
    """
    replacements: dict[str, bytes] = {p.SEC_CONFIG_TEST: _synthetic_new_test_file()}
    for path in p.PRODUCT_EXISTING_FILES:
        original = p.raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        replacements[path] = original + b"\n// v51 synthetic second-stage touch\n"
    if extra:
        replacements.update(extra)
    return OverlayView(p.raw_root, replacements)


def _check_product_delta_shape() -> None:
    """Exercises `delta()`'s product-grant branch. When the tranche is already
    tracked in the actual checkout (true once this candidate lands), the real
    frontier check (`_require_product_base`) legitimately rejects a synthetic
    base built on top of `raw_root`, so this — like every other successor's
    equivalent self-test — is a no-op past that point; `verify-candidate-local`
    against the real pre-tranche commit is the authoritative proof.
    """
    if p._product_presence(p.raw_root):
        return

    candidate = _synthetic_product_candidate()
    p.delta(candidate, p.raw_root)

    mixed = _synthetic_product_candidate(
        extra={"docs/canonical/UNAUTHORIZED_D012_MIX.md": b"# nope\n"}
    )
    _expect_failure(
        "v51 product mixed with non-product path",
        lambda: p.delta(mixed, p.raw_root),
        "must not mix with non-product paths",
    )

    lock_mut = _synthetic_product_candidate(extra={p.ROOT_CARGO_LOCK: b"# tampered lock\n"})
    _expect_failure(
        "v51 product tranche must not mutate Cargo.lock",
        lambda: p.delta(lock_mut, p.raw_root),
        "must not mix with non-product paths",
    )

    manifest_mut = _synthetic_product_candidate(
        extra={p.CORE_MANIFEST: b"[package]\nname = \"wepld-core\"\n"}
    )
    _expect_failure(
        "v51 product tranche must not mutate the core manifest",
        lambda: p.delta(manifest_mut, p.raw_root),
        "must not mix with non-product paths",
    )

    extra_core = _synthetic_product_candidate(
        extra={"crates/core/src/net.rs": b"// unauthorized module\n"}
    )
    _expect_failure(
        "v51 product tranche must not add an unauthorized core module",
        lambda: p.delta(extra_core, p.raw_root),
        "must not mix with non-product paths",
    )

    missing_new_file = OverlayView(
        p.raw_root,
        {
            path: p.raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
            + b"\n// v51 synthetic second-stage touch\n"
            for path in p.PRODUCT_EXISTING_FILES
        },
    )
    _expect_failure(
        "v51 candidate touching only the second-stage files, missing the new file",
        lambda: p.delta(missing_new_file, p.raw_root),
        "must change exact module/test set",
    )


def _check_product_base_frontier() -> None:
    """Rejects a candidate built over a policy base whose pinned second-stage
    frontier blobs have drifted. Guarded the same way as
    `_check_product_delta_shape` — see its docstring.
    """
    if p._product_presence(p.raw_root):
        return
    drifted_topology = (
        p.raw_root.read_bytes(p.GIT_TOPOLOGY_MODULE, base.MAX_POLICY_FILE_BYTES) + b"\n// drift\n"
    )
    drifted_base = OverlayView(p.raw_root, {p.GIT_TOPOLOGY_MODULE: drifted_topology})
    candidate = _synthetic_product_candidate()
    candidate = OverlayView(drifted_base, dict(candidate._replacements))
    _expect_failure(
        "v51 product tranche against a drifted second-stage frontier",
        lambda: p.delta(candidate, drifted_base),
        "product base frontier drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_config_query_contract()
    _check_product_scope()
    _check_predecessor_exact()
    _check_workflow_projection()
    _check_bootstrap_scope()
    _check_product_delta_shape()
    _check_product_base_frontier()
    p.install()
    p.overlay()
    print("wepld v51 S2-D012 security-sensitive config observation authority self-tests: PASS")


if __name__ == "__main__":
    run()
