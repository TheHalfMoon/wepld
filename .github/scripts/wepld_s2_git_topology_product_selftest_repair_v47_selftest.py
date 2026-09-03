#!/usr/bin/env python3
"""Self-tests for the v47 v46-predecessor-inventory repair."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s1_shell_integrity_v21 as v21
import wepld_s2_git_topology_product_selftest_repair_v47_integrity as p

_OVERLAY_COUNTER = itertools.count()


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
        self._instance_id = next(_OVERLAY_COUNTER)

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v47 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return [entry for entry in self._view.entries() if entry.path not in self._omitted]

    def tree_identity(self, path: str) -> Any:
        return (self._instance_id, path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any, expected: str) -> None:
    try:
        action()
    except (base.PolicyError, FileNotFoundError) as exc:
        if expected not in str(exc):
            base.fail(f"v47 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v47 self-test expected fail-closed rejection: {label}")


def _check_authority_is_unchanged() -> None:
    if p.AUTH != "S2_V46_PRODUCT_STATE_PREDECESSOR_INVENTORY_REPAIR_ONLY":
        base.fail("v47 authority marker drift")
    inherited = (
        "S2_IMPLEMENTATION_AUTHORITY",
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
        "NEXT_AUTHORITY_GATE",
    )
    for name in inherited:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v47 widened or changed inherited authority: {name}")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-015":
        base.fail("v47 next authority gate drift")


def _check_predecessor_exact() -> None:
    p.req_v46(p.raw_root)
    if p.V46_P_BLOB != "6362667fb13e9e783f859eb5f133dab2e829b0c9":
        base.fail("v47 frozen v46 integrity identity drift")
    if p.V46_T_BLOB != "6ee7cd6f9ef8862d38a0ced5d2a163053284b72c":
        base.fail("v47 frozen v46 self-test identity drift")


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v47 bootstrap path set drift")
    p.delta(p.raw_root, p._boot_base_for_selftest())
    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V47_BOOTSTRAP.md": b"# no\n"},
    )
    _expect_failure(
        "v47 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, p._boot_base_for_selftest()),
        "v47 bootstrap delta must be exactly two v47 policy files plus two integrity workflows",
    )


def _check_method_patch_is_installed() -> None:
    if p.q._method_patch is not p._corrected_method_patch:
        base.fail("v47 did not install the corrected _method_patch onto frozen v46")
    if p._ORIGINAL_V46_METHOD_PATCH is p._corrected_method_patch:
        base.fail("v47 recorded its own replacement as the original v46 _method_patch")


def _check_inventory_is_not_desynced() -> None:
    """The exact class of failure this successor repairs.

    Frozen v46's ``_method_patch`` reassigned ``base.LocalRepositoryView.entries``
    for the whole predecessor cascade, so once the Git-topology product paths
    are actually tracked a v21-era self-test that cross-checks a fresh
    ``LocalRepositoryView`` inventory against the exact-HEAD commit view failed
    with ``local commit view entry inventory differs from exact HEAD``.

    The corrected ``_method_patch`` must never touch that class attribute; it
    hides ``omitted`` paths only by wrapping each ``wepld_*`` module root.
    """
    entries_sentinel = base.LocalRepositoryView.entries
    read_bytes_sentinel = base.LocalRepositoryView.read_bytes
    probe_path = ".github/scripts/wepld_integrity.py"
    omitted = frozenset({probe_path})
    root = base.LocalRepositoryView(str(p.Path(__file__).resolve().parents[2]))

    observations: dict[str, Any] = {}

    def _inside() -> None:
        observations["entries_untouched"] = (
            base.LocalRepositoryView.entries is entries_sentinel
        )
        observations["fresh_view_still_lists_probe"] = any(
            entry.path == probe_path for entry in root.entries()
        )
        module = __import__("wepld_s2_git_topology_authority_v45_integrity")
        wrapped = getattr(module, "raw_root", None)
        observations["module_root_hides_probe"] = wrapped is not None and not any(
            entry.path == probe_path for entry in wrapped.entries()
        )
        # v21's exact cross-check must pass with the class attribute intact.
        v21._selftest_local_commit_view()

    p._corrected_method_patch({}, omitted, "v47 inventory oracle", _inside)

    if not observations.get("entries_untouched"):
        base.fail("v47 _method_patch reassigned base.LocalRepositoryView.entries")
    if not observations.get("fresh_view_still_lists_probe"):
        base.fail("v47 _method_patch hid a path from a fresh LocalRepositoryView inventory")
    if not observations.get("module_root_hides_probe"):
        base.fail("v47 _method_patch did not hide the omitted path from the wrapped module root")
    if base.LocalRepositoryView.entries is not entries_sentinel:
        base.fail("v47 _method_patch left base.LocalRepositoryView.entries reassigned")
    if base.LocalRepositoryView.read_bytes is not read_bytes_sentinel:
        base.fail("v47 _method_patch left base.LocalRepositoryView.read_bytes reassigned")
    module = __import__("wepld_s2_git_topology_authority_v45_integrity")
    if isinstance(getattr(module, "raw_root", None), p._EntryHidingView):
        base.fail("v47 _method_patch left a module root wrapped after finally")


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_is_unchanged()
    _check_predecessor_exact()
    _check_bootstrap_scope()
    _check_method_patch_is_installed()
    _check_inventory_is_not_desynced()
    p.install()
    p.overlay()
    print("wepld v47 v46-predecessor-inventory repair: PASS")


if __name__ == "__main__":
    run()
