#!/usr/bin/env python3
"""Self-tests for the v34 S2 Git-route decision bootstrap."""

from typing import Any

import wepld_integrity as base
import wepld_s2_git_route_governance_v34_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v34 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return self._view.entries()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any) -> None:
    try:
        action()
    except base.PolicyError:
        return
    base.fail(f"v34 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_GIT_TOPOLOGY_ROUTE_DECISION_ONLY":
        base.fail("v34 authority marker drift")
    if p.GIT_ROUTE_DECISION != "SELECT_NARROW_QUALIFIED_SYSTEM_GIT_ADAPTER":
        base.fail("v34 Git-route decision drift")
    for value, label in (
        (p.GIT_PROCESS_ADMISSION, "Git process admission"),
        (p.EXTERNAL_PROCESS_AUTHORITY, "external process authority"),
        (p.GIT_EXECUTION_AUTHORITY, "Git execution authority"),
        (p.NETWORK_AUTHORITY, "network authority"),
        (p.SOURCE_ADMISSION, "source admission"),
        (p.MODEL_PROVIDER_EXECUTION, "model/provider execution"),
        (p.DOCTOR_CLI_AUTHORITY, "Doctor/CLI authority"),
        (p.S3_PLUS_AUTHORITY, "S3+ authority"),
    ):
        if value != "NONE":
            base.fail(f"v34 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v34 route decision must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v34 route decision must not change dependency admission")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v34 next authority gate drift")


def _check_qualification_contract_is_closed() -> None:
    required = frozenset(
        {
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
        }
    )
    observed = frozenset(p.GIT_ROUTE_QUALIFICATION_CONTRACT)
    if observed != required:
        base.fail(
            "v34 Git-route qualification contract drifted: "
            f"expected={sorted(required)} actual={sorted(observed)}"
        )
    if len(p.GIT_ROUTE_QUALIFICATION_CONTRACT) != len(observed):
        base.fail("v34 Git-route qualification contract contains duplicates")


def _check_command_family_is_specification_only() -> None:
    if p.GIT_TOPOLOGY_COMMAND_FAMILY != (
        "rev-parse:closed_allowlisted_topology_query",
        "worktree:list:porcelain-z",
    ):
        base.fail("v34 candidate Git command family drift")
    if p.GIT_PROCESS_ADMISSION != "NONE" or p.GIT_EXECUTION_AUTHORITY != "NONE":
        base.fail("v34 command-family specification must not execute itself")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v34 workflow projection does not reverse to v33: {path}")
        if p._V34_ENTRYPOINT in data:
            base.fail(f"v34 workflow projection left a v34 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V34_ENTRYPOINT,
        b"wepld_unknown_git_route_entrypoint.py",
        1,
    )
    view = OverlayView(p.root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
    )


def _check_bootstrap_scope_is_closed() -> None:
    expected = frozenset({p.P, p.T, p.FW, p.AW})
    if p.BOOT != expected:
        base.fail(f"v34 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v34 controlled file set must be exactly the two policy files")


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_qualification_contract_is_closed()
    _check_command_family_is_specification_only()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_bootstrap_scope_is_closed()

    print("wepld v34 S2 Git-route decision self-tests: PASS")
