#!/usr/bin/env python3
"""Self-tests for the v45 S2-AUTH-014 bounded Git topology authority successor."""

from __future__ import annotations

from typing import Any

import wepld_integrity as base
import wepld_s2_git_topology_authority_v45_integrity as p


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

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v45 self-test overlay exceeds read bound: {path}")
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
        return (id(self), path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any, expected: str) -> None:
    try:
        action()
    except (base.PolicyError, FileNotFoundError) as exc:
        if expected not in str(exc):
            base.fail(f"v45 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v45 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_AUTH_014_EXACT_GIT_TOPOLOGY_PROCESS_TRANCHE":
        base.fail("v45 authority marker drift")
    if p.GIT_ROUTE_DECISION != "SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER":
        base.fail("v45 route decision drift")
    if p.GIT_PROCESS_ADMISSION != "EXACT_LOCAL_SYSTEM_GIT_TOPOLOGY_ADAPTER_ONLY":
        base.fail("v45 Git process admission drift")
    if p.EXTERNAL_PROCESS_AUTHORITY != "EXACT_QUALIFIED_GIT_EXECUTABLE_CLOSED_TOPOLOGY_ARGV_ONLY":
        base.fail("v45 external process authority drift")
    if p.GIT_EXECUTION_AUTHORITY != "READ_ONLY_TOPOLOGY_OBSERVATION_ONLY":
        base.fail("v45 Git execution authority drift")
    for value, label in (
        (p.NETWORK_AUTHORITY, "network authority"),
        (p.MODEL_PROVIDER_EXECUTION, "model/provider execution"),
        (p.DOCTOR_CLI_AUTHORITY, "Doctor/CLI authority"),
        (p.S3_PLUS_AUTHORITY, "S3+ authority"),
    ):
        if value != "NONE":
            base.fail(f"v45 must not grant {label}")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v45 must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v45 must not change source admission")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-015":
        base.fail("v45 next authority gate drift")


def _check_process_contract() -> None:
    if p.GIT_GLOBAL_FLAGS != ("--no-pager", "--no-optional-locks", "--no-lazy-fetch"):
        base.fail("v45 Git global flag contract drift")
    expected_queries = (
        "--path-format=absolute --show-toplevel",
        "--path-format=absolute --absolute-git-dir",
        "--path-format=absolute --git-common-dir",
        "--is-bare-repository",
        "--is-inside-work-tree",
        "--path-format=absolute --show-superproject-working-tree",
    )
    if p.GIT_REV_PARSE_QUERY_ENUM != expected_queries:
        base.fail("v45 closed rev-parse query enum drift")
    if p.GIT_WORKTREE_COMMAND != "worktree list --porcelain -z":
        base.fail("v45 worktree command contract drift")
    required_env = {
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
    }
    if set(p.GIT_ENV_REMOVE) != required_env:
        base.fail("v45 Git environment scrub contract drift")
    if p.GIT_ENV_FORCE != (("GIT_TERMINAL_PROMPT", "0"),):
        base.fail("v45 Git forced environment contract drift")
    if p.GIT_TIMEOUT_MS <= 0 or p.GIT_STDOUT_MAX_BYTES <= 0 or p.GIT_STDERR_MAX_BYTES <= 0:
        base.fail("v45 Git execution bounds must be positive")
    if p.GIT_TIMEOUT_MS > 10_000:
        base.fail("v45 Git timeout must remain narrowly bounded")
    if "NO_NETWORK" not in p.GIT_ROUTE_QUALIFICATION_CONTRACT:
        base.fail("v45 qualification contract lost no-network invariant")
    if "NO_HOOKS" not in p.GIT_ROUTE_QUALIFICATION_CONTRACT:
        base.fail("v45 qualification contract lost no-hook invariant")
    if "PRESERVE_NATIVE_SAFE_DIRECTORY_REFUSAL" not in p.GIT_ROUTE_QUALIFICATION_CONTRACT:
        base.fail("v45 qualification contract lost native trust refusal")


def _check_product_scope() -> None:
    expected = frozenset(
        {
            "crates/core/src/git_topology.rs",
            "crates/core/src/lib.rs",
            "crates/core/tests/git_topology_v1.rs",
        }
    )
    if p.PRODUCT_FILES != expected:
        base.fail("v45 product path allowlist drift")
    if p.PRODUCT_NEW_FILES != frozenset(
        {"crates/core/src/git_topology.rs", "crates/core/tests/git_topology_v1.rs"}
    ):
        base.fail("v45 new-product path set drift")
    if p.PRODUCT_TASKS != frozenset(
        {"S2-I005", "S2-I006", "S2-I007", "S2-S005", "S2-S006", "S2-S007", "S2-S013", "S2-S014", "S2-Q008"}
    ):
        base.fail("v45 product task allowlist drift")
    if p.CORE_MANIFEST in p.PRODUCT_FILES or p.ROOT_CARGO_LOCK in p.PRODUCT_FILES:
        base.fail("v45 product tranche must not authorize dependency mutation")


def _check_predecessor_exact() -> None:
    p.req_v44(p.raw_root)
    if p.V44_P_BLOB != "bc11c7f89ad383625e4ea65200494361070f27a1":
        base.fail("v45 frozen v44 integrity identity drift")
    if p.V44_T_BLOB != "3d6c293804802a87a45ffdca4d106f293aec9fbd":
        base.fail("v45 frozen v44 self-test identity drift")


def _check_workflow_projection() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v45 workflow projection does not reverse to exact v44: {path}")
        if p._V45_ENTRYPOINT in data:
            base.fail(f"v45 workflow projection left v45 entrypoint: {path}")


def _boot_base() -> OverlayView:
    replacements = p._workflow_replacements(p.raw_root)
    return OverlayView(p.raw_root, replacements, omitted=p.POLICY_FILES)


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v45 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v45 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())

    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V45_BOOTSTRAP.md": b"# smuggled\n"},
    )
    _expect_failure(
        "v45 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v45 policy files plus two integrity workflows",
    )


def _synthetic_product_candidate(*, extra: dict[str, bytes] | None = None) -> OverlayView:
    lib = p.raw_root.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if b"pub mod git_topology;" in lib:
        base.fail("v45 self-test baseline unexpectedly already exports git_topology")
    replacements = {
        p.CORE_EXPORT: lib + b"\npub mod git_topology;\n",
        p.GIT_TOPOLOGY_MODULE: b"#![allow(dead_code)]\npub fn topology_fixture() -> &'static str { \"ok\" }\n",
        p.PRODUCT_TEST: b"#[test]\nfn git_topology_fixture() { assert!(true); }\n",
    }
    if extra:
        replacements.update(extra)
    return OverlayView(p.raw_root, replacements)


def _check_product_delta_shape() -> None:
    candidate = _synthetic_product_candidate()
    p.delta(candidate, p.raw_root)

    mixed = _synthetic_product_candidate(
        extra={"docs/canonical/UNAUTHORIZED_GIT_TOPOLOGY_MIX.md": b"# nope\n"}
    )
    _expect_failure(
        "v45 product mixed with non-product path",
        lambda: p.delta(mixed, p.raw_root),
        "must not mix with non-product paths",
    )

    missing_test = OverlayView(
        p.raw_root,
        {
            p.CORE_EXPORT: p.raw_root.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
            + b"\npub mod git_topology;\n",
            p.GIT_TOPOLOGY_MODULE: b"pub fn x() {}\n",
        },
    )
    _expect_failure(
        "v45 initial product tranche missing exact test path",
        lambda: p.delta(missing_test, p.raw_root),
        "initial Git-topology delta must change exact module/export/test set",
    )


def _check_product_base_frontier() -> None:
    drifted_lib = p.raw_root.read_bytes(p.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES) + b"\n// drift\n"
    drifted_base = OverlayView(p.raw_root, {p.CORE_EXPORT: drifted_lib})
    candidate = OverlayView(
        drifted_base,
        {
            p.CORE_EXPORT: drifted_lib + b"\npub mod git_topology;\n",
            p.GIT_TOPOLOGY_MODULE: b"pub fn x() {}\n",
            p.PRODUCT_TEST: b"#[test]\nfn x() {}\n",
        },
    )
    _expect_failure(
        "v45 product tranche against drifted canonical frontier",
        lambda: p.delta(candidate, drifted_base),
        "product base frontier drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_process_contract()
    _check_product_scope()
    _check_predecessor_exact()
    _check_workflow_projection()
    _check_bootstrap_scope()
    _check_product_delta_shape()
    _check_product_base_frontier()
    p.install()
    p.overlay()
    print("wepld v45 S2-AUTH-014 Git-topology authority self-tests: PASS")


if __name__ == "__main__":
    run()
