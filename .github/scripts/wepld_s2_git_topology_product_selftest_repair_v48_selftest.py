#!/usr/bin/env python3
"""Self-tests for the v48 v47-install product-projection repair."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v33_integrity as v33
import wepld_s2_git_topology_product_selftest_repair_v48_integrity as p

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
                base.fail(f"v48 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v48 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v48 self-test expected fail-closed rejection: {label}")


def _check_authority_is_unchanged() -> None:
    if p.AUTH != "S2_V47_INSTALL_PRODUCT_PROJECTION_REPAIR_ONLY":
        base.fail("v48 authority marker drift")
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
            base.fail(f"v48 widened or changed inherited authority: {name}")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-015":
        base.fail("v48 next authority gate drift")


def _check_predecessor_exact() -> None:
    p.req_v47(p.raw_root)
    if p.V47_P_BLOB != "c6bf99c9829c101568ae651bd35d94bcb689d641":
        base.fail("v48 frozen v47 integrity identity drift")
    if p.V47_T_BLOB != "0508165f3baef0953f940feb4ed7f340e0d90b88":
        base.fail("v48 frozen v47 self-test identity drift")


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v48 bootstrap path set drift")
    p.delta(p.raw_root, p._boot_base_for_selftest())
    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V48_BOOTSTRAP.md": b"# no\n"},
    )
    _expect_failure(
        "v48 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, p._boot_base_for_selftest()),
        "v48 bootstrap delta must be exactly two v48 policy files plus two integrity workflows",
    )


def _check_install_projection_repairs_v33() -> None:
    """The exact class of failure this successor repairs.

    Frozen v45's ``install()`` delegates to the predecessor cascade bare, so
    once ``lib.rs`` carries ``pub mod git_topology;`` in the tracked tree v33's
    install-time ``_core_export_baseline`` rejects it (the Foundation
    ``verify-candidate-local`` failure for the reconciled product PR).

    Simulate a tracked post-tranche tree by pointing ``p.raw_root`` at a
    synthetic overlay, then drive ``_install_predecessor_under_product_projection``
    with a probe instead of the real ``q.install`` and assert:
      * the raw post-tranche ``lib.rs`` is rejected by frozen v33 with the exact
        Foundation message;
      * under the projection the same v33 check accepts the stripped export and
        returns the canonical baseline;
      * the two product paths are hidden from a wrapped module root;
      * ``read_bytes`` and every module root are restored afterwards.
    """
    admitted = v33.ADMITTED_CORE_EXPORT
    post_tranche_lib = admitted + b"pub mod git_topology;\n"
    core_export = p._Q45.CORE_EXPORT
    module_path = p._Q45.GIT_TOPOLOGY_MODULE
    test_path = p._Q45.PRODUCT_TEST
    product_new = p._Q45.PRODUCT_NEW_FILES

    synthetic = OverlayView(
        p.raw_root,
        {
            core_export: post_tranche_lib,
            module_path: b"#![forbid(unsafe_code)]\npub fn fixture() {}\n",
            test_path: b"#[test]\nfn fixture() { assert!(true); }\n",
        },
    )

    fresh = base.LocalRepositoryView(p.Path(__file__).resolve().parents[2])

    # Raw post-tranche export is rejected by the frozen v33 install-time check.
    _expect_failure(
        "v48 install oracle reproduces the frozen v33 install-time rejection",
        lambda: v33._core_export_baseline(synthetic),
        "neither the exact canonical baseline nor the exact authorized tranche export",
    )

    entries_sentinel = base.LocalRepositoryView.entries
    read_bytes_sentinel = base.LocalRepositoryView.read_bytes
    observations: dict[str, Any] = {}

    def _probe() -> None:
        observations["projected_export"] = fresh.read_bytes(core_export, base.MAX_POLICY_FILE_BYTES)
        observations["v33_baseline"] = v33._core_export_baseline(fresh)
        observations["entries_untouched"] = base.LocalRepositoryView.entries is entries_sentinel
        v45_module = __import__("wepld_s2_git_topology_authority_v45_integrity")
        wrapped = getattr(v45_module, "raw_root", None)
        observations["module_root_hides_product"] = wrapped is not None and not any(
            entry.path in product_new for entry in wrapped.entries()
        )

    original_raw_root = p.raw_root
    try:
        p.raw_root = synthetic
        p._install_predecessor_under_product_projection(_probe)
    finally:
        p.raw_root = original_raw_root

    if observations.get("projected_export") != admitted:
        base.fail("v48 install projection did not strip the Git-topology Core export to the baseline")
    if observations.get("v33_baseline") != v33.BASE_CORE_EXPORT:
        base.fail("v48 install projection: frozen v33 _core_export_baseline did not accept the projected export")
    if not observations.get("entries_untouched"):
        base.fail("v48 install projection reassigned base.LocalRepositoryView.entries")
    if not observations.get("module_root_hides_product"):
        base.fail("v48 install projection did not hide the product paths from the wrapped module root")
    if base.LocalRepositoryView.read_bytes is not read_bytes_sentinel:
        base.fail("v48 install projection left base.LocalRepositoryView.read_bytes reassigned")
    v45_module = __import__("wepld_s2_git_topology_authority_v45_integrity")
    if isinstance(getattr(v45_module, "raw_root", None), p.q._EntryHidingView):
        base.fail("v48 install projection left a module root wrapped after finally")
    # No tranche tracked here: the real helper must take the bare path.
    p._install_predecessor_under_product_projection(lambda: observations.__setitem__("bare_ran", True))
    if not observations.get("bare_ran"):
        base.fail("v48 install projection did not run the bare install path when no tranche is tracked")


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_is_unchanged()
    _check_predecessor_exact()
    _check_bootstrap_scope()
    _check_install_projection_repairs_v33()
    p.install()
    p.overlay()
    print("wepld v48 v47-install product-projection repair: PASS")


if __name__ == "__main__":
    run()
