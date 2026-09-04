#!/usr/bin/env python3
"""Self-tests for the v50 v49-Doctor/CLI predecessor-selftest projection repair."""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_v49_doctor_cli_selftest_projection_repair_v50_integrity as p
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
                base.fail(f"v50 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v50 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v50 self-test expected fail-closed rejection: {label}")


def _check_authority_is_unchanged() -> None:
    if p.AUTH != "S2_V49_DOCTOR_CLI_SELFTEST_PROJECTION_REPAIR_ONLY":
        base.fail("v50 authority marker drift")
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
        "GENERAL_SHELL_AUTHORITY",
        "ARBITRARY_PROCESS_AUTHORITY",
        "PACKAGE_INSTALL_AUTHORITY",
        "PROJECT_NATIVE_COMMAND_EXECUTION",
        "GIT_MUTATION_AUTHORITY",
        "SAFE_DIRECTORY_MUTATION_AUTHORITY",
        "REMEDIATION_EXECUTION_AUTHORITY",
    )
    for name in inherited:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v50 widened or changed inherited authority: {name}")
    if p.DOCTOR_CLI_AUTHORITY != "DETERMINISTIC_LOCAL_PROJECTION_ORCHESTRATION_ONLY":
        base.fail("v50 inherited Doctor/CLI authority value drift")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v50 inherited next-authority-gate drift")
    for name in (
        "GENERAL_SHELL_AUTHORITY",
        "ARBITRARY_PROCESS_AUTHORITY",
        "PACKAGE_INSTALL_AUTHORITY",
        "PROJECT_NATIVE_COMMAND_EXECUTION",
        "GIT_MUTATION_AUTHORITY",
        "SAFE_DIRECTORY_MUTATION_AUTHORITY",
        "REMEDIATION_EXECUTION_AUTHORITY",
        "NETWORK_AUTHORITY",
        "MODEL_PROVIDER_EXECUTION",
        "S3_PLUS_AUTHORITY",
    ):
        if getattr(p, name) != "NONE":
            base.fail(f"v50 standing denial relaxed: {name}")


def _check_predecessor_exact() -> None:
    p.req_v49(p.raw_root)
    if p.V49_P_BLOB != "23c2aa08ed5b9c6310e0f72414982342ddaec8ba":
        base.fail("v50 frozen v49 integrity identity drift")
    if p.V49_T_BLOB != "a5eec317d93e8e316a23c06b9ee1b94a6faf5565":
        base.fail("v50 frozen v49 self-test identity drift")


def _check_bootstrap_scope() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v50 bootstrap path set drift")
    p.delta(p.raw_root, p._boot_base_for_selftest())
    smuggled = OverlayView(
        p.raw_root,
        {"docs/canonical/UNAUTHORIZED_V50_BOOTSTRAP.md": b"# no\n"},
    )
    _expect_failure(
        "v50 bootstrap mixed with fifth path",
        lambda: p.delta(smuggled, p._boot_base_for_selftest()),
        "v50 bootstrap delta must be exactly two v50 policy files plus two integrity workflows",
    )


def _synthetic_post_tranche_view() -> OverlayView:
    lib = p.q.raw_root.read_bytes(p.q.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    # Normalise: whether or not the real tree already carries the Doctor/CLI
    # tranche (state B), the fixture starts from a pre-tranche Core export and
    # re-adds exactly the two authorized lines.
    pre = lib
    if p.q._MOD_CLI_LINE in pre or p.q._MOD_DOCTOR_LINE in pre:
        pre = p.q._strip_doctor_cli_exports(pre)
    if p.q._MOD_CLI_LINE in pre or p.q._MOD_DOCTOR_LINE in pre:
        base.fail("v50 regression fixture base still carries a Doctor/CLI export line")
    product_lib = pre
    if product_lib and not product_lib.endswith(b"\n"):
        product_lib += b"\n"
    product_lib += p.q._MOD_CLI_LINE + p.q._MOD_DOCTOR_LINE
    stub_module = b"#![forbid(unsafe_code)]\npub fn fixture() {}\n"
    stub_test = b"#[test]\nfn fixture() { assert!(true); }\n"
    return OverlayView(
        p.q.raw_root,
        {
            p.q.CORE_EXPORT: product_lib,
            p.q.DOCTOR_MODULE: stub_module,
            p.q.CLI_MODULE: stub_module,
            p.q.CLI_BIN: b"#![forbid(unsafe_code)]\nfn main() {}\n",
            p.q.DOCTOR_TEST: stub_test,
            p.q.CLI_TEST: stub_test,
        },
    )


def _check_projection_repairs_doctor_cli_export() -> None:
    candidate = _synthetic_post_tranche_view()
    if p.q._product_presence(candidate) != p.q.PRODUCT_NEW_FILES:
        base.fail("v50 regression fixture does not represent the complete v49 product tranche")

    raw_lib = candidate.read_bytes(p.q.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    if raw_lib.count(p.q._MOD_CLI_LINE) != 1 or raw_lib.count(p.q._MOD_DOCTOR_LINE) != 1:
        base.fail("v50 regression fixture Core export is malformed")

    # The frozen v33 Core-export self-test rejects a lib.rs that carries the
    # Doctor/CLI module lines: it is neither v33's canonical baseline nor v33's
    # authorized identity-store tranche export. Reproduce that exact rejection
    # against the raw post-tranche candidate.
    _expect_failure(
        "v50 reproduces the v33 Core-export rejection on the raw Doctor/CLI tranche",
        lambda: v33._core_export_baseline(candidate),
        "neither the exact canonical baseline nor the exact authorized tranche export",
    )

    # v50's predecessor projection strips exactly the two authorized Doctor/CLI
    # export lines and hides exactly the five new module/bin/test files, leaving
    # the rest of the tree (including the already-canonical Git-topology export
    # that the deeper v46 projection then handles) untouched.
    replacements, omitted = p._doctor_cli_projection(candidate)
    if omitted != p.q.PRODUCT_NEW_FILES:
        base.fail("v50 predecessor projection did not hide exactly the five new product paths")
    if p.q.CORE_EXPORT not in replacements:
        base.fail("v50 predecessor projection did not strip the Doctor/CLI Core export")
    projected_lib = replacements[p.q.CORE_EXPORT]
    if p.q._MOD_CLI_LINE in projected_lib or p.q._MOD_DOCTOR_LINE in projected_lib:
        base.fail("v50 predecessor projection left a Doctor/CLI export line visible")
    real_lib = p.q.raw_root.read_bytes(p.q.CORE_EXPORT, base.MAX_POLICY_FILE_BYTES)
    pre_tranche_real = (
        p.q._strip_doctor_cli_exports(real_lib)
        if (p.q._MOD_CLI_LINE in real_lib or p.q._MOD_DOCTOR_LINE in real_lib)
        else real_lib
    )
    if projected_lib != pre_tranche_real:
        base.fail("v50 predecessor projection did not restore the exact pre-tranche Core export")

    projected = p.predecessor_view_for(candidate)
    if p.q._product_presence(projected):
        base.fail("v50 predecessor projection left Doctor/CLI product-only paths visible")

    # A partial tranche in a predecessor view fails closed rather than being
    # silently hidden. Present exactly two of the five new paths in both tree
    # states: supply two as overlay replacements and omit the other three so a
    # real post-tranche tree (state B) is trimmed back to the same partial shape.
    stub_module = b"#![forbid(unsafe_code)]\npub fn fixture() {}\n"
    partial = OverlayView(
        p.q.raw_root,
        {p.q.DOCTOR_MODULE: stub_module, p.q.CLI_MODULE: stub_module},
        omitted=frozenset({p.q.CLI_BIN, p.q.DOCTOR_TEST, p.q.CLI_TEST}),
    )
    if p.q._product_presence(partial) != frozenset({p.q.DOCTOR_MODULE, p.q.CLI_MODULE}):
        base.fail("v50 partial-tranche fixture did not present exactly two of the five new paths")
    _expect_failure(
        "v50 partial Doctor/CLI tranche in a predecessor view fails closed",
        lambda: p._doctor_cli_projection(partial),
        "partial Doctor/CLI tranche",
    )


def _check_workflow_projection() -> None:
    reversal = p._workflow_replacements(p.raw_root)
    for path in (p.FW, p.AW):
        if p._V50_ENTRYPOINT in reversal[path]:
            base.fail(f"v50 workflow projection left the v50 entrypoint: {path}")
        if p._V49_ENTRYPOINT not in reversal[path]:
            base.fail(f"v50 workflow projection did not restore the v49 entrypoint: {path}")
        if p.V25.sha(reversal[path]) != p.Q_WF[path]:
            base.fail(f"v50 workflow projection does not reverse to exact canonical v49: {path}")


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_is_unchanged()
    _check_predecessor_exact()
    _check_bootstrap_scope()
    _check_workflow_projection()
    _check_projection_repairs_doctor_cli_export()
    p.install()
    p.overlay()
    print("wepld v50 v49-Doctor/CLI predecessor self-test projection repair: PASS")


if __name__ == "__main__":
    run()
