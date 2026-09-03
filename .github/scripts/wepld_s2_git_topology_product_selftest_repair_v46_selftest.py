#!/usr/bin/env python3
"""Self-tests for the v46 v45-product-state predecessor-selftest repair."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_git_topology_product_selftest_repair_v46_integrity as p
import wepld_s2_identity_store_governance_v33_integrity as v33

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
                base.fail(f"v46 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v46 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v46 self-test expected fail-closed rejection: {label}")


def _check_authority_is_unchanged() -> None:
    if p.AUTH != "S2_V45_PRODUCT_SELFTEST_PROJECTION_REPAIR_ONLY":
        base.fail("v46 authority marker drift")
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
            base.fail(f"v46 widened or changed inherited authority: {name}")


def _check_predecessor_exact() -> None:
    p.req_v45(p.raw_root)
    if p.V45_P_BLOB != "a9b77d8d981871730a7de4c1f5f2f0661176f9a7":
        base.fail("v46 frozen v45 integrity identity drift")
    if p.V45_T_BLOB != "70673c5f1324c8a06e7f36c0f8412aa3d9f57880":
        base.fail("v46 frozen v45 self-test identity drift")


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v46 bootstrap path set drift")
    p.delta(p.raw_root, p._boot_base_for_selftest())
    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V46_BOOTSTRAP.md": b"# no\n"},
    )
    _expect_failure(
        "v46 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, p._boot_base_for_selftest()),
        "v46 bootstrap delta must be exactly two v46 policy files plus two integrity workflows",
    )


def _synthetic_post_tranche_view() -> OverlayView:
    lib = p.q.raw_root.read_bytes(p.q.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if p.q._GIT_TOPOLOGY_EXPORT_LINE in lib:
        pre = p.q._strip_git_topology_export(lib)
    else:
        pre = lib
    product_lib = pre
    if product_lib and not product_lib.endswith(b"\n"):
        product_lib += b"\n"
    product_lib += p.q._GIT_TOPOLOGY_EXPORT_LINE + b"\n"
    return OverlayView(
        p.q.raw_root,
        {
            p.q.CORE_EXPORT: product_lib,
            p.q.GIT_TOPOLOGY_MODULE: b"#![forbid(unsafe_code)]\npub fn fixture() {}\n",
            p.q.PRODUCT_TEST: b"#[test]\nfn fixture() { assert!(true); }\n",
        },
    )


def _check_exact_regression_is_repaired() -> None:
    candidate = _synthetic_post_tranche_view()
    if p.q._product_presence(candidate) != p.q.PRODUCT_NEW_FILES:
        base.fail("v46 regression fixture does not represent the complete v45 product tranche")

    # Foundation run #1017 failed inside v33's frozen Core-export self-test:
    # `_core_export_baseline` rejects a `lib.rs` that carries `pub mod
    # git_topology;` because it is neither v33's canonical baseline nor v33's
    # authorized identity-store tranche export. Reproduce that exact rejection
    # against the raw post-tranche candidate...
    _expect_failure(
        "v46 reproduces the Foundation #1017 v33 Core-export rejection",
        lambda: v33._core_export_baseline(candidate),
        "neither the exact canonical baseline nor the exact authorized tranche export",
    )

    # ...then prove v46's predecessor projection repairs it: the same frozen
    # v33 check now sees the Git-topology export line reversed away and accepts
    # the projected view, returning the canonical baseline rather than failing.
    projected = p.predecessor_view_for(candidate)
    if p.q._product_presence(projected):
        base.fail("v46 predecessor projection left v45 product-only paths visible")
    lib = projected.read_bytes(p.q.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if p.q._GIT_TOPOLOGY_EXPORT_LINE in lib:
        base.fail("v46 predecessor projection left the Git-topology Core export visible")
    if v33._core_export_baseline(projected) != v33.BASE_CORE_EXPORT:
        base.fail("v46 predecessor projection did not restore v33's canonical Core-export baseline")


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_is_unchanged()
    _check_predecessor_exact()
    _check_bootstrap_scope()
    _check_exact_regression_is_repaired()
    p.install()
    p.overlay()
    print("wepld v46 v45-product-state predecessor self-test repair: PASS")


if __name__ == "__main__":
    run()
