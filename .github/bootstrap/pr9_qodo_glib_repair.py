#!/usr/bin/env python3
from pathlib import Path
from textwrap import dedent

SCRIPT = Path(".github/scripts/wepld_integrity.py")
SPEC = Path("specs/001-desktop-rust-trusted-core-handshake/s1-005-component-admission-integrity.md")

text = SCRIPT.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"ABORT: {label} anchor count={count}")
    text = text.replace(old, new, 1)


def replace_function(start_marker: str, end_marker: str, replacement: str, label: str) -> None:
    global text
    if text.count(start_marker) != 1:
        raise SystemExit(f"ABORT: {label} start count={text.count(start_marker)}")
    if text.count(end_marker) != 1:
        raise SystemExit(f"ABORT: {label} end count={text.count(end_marker)}")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    text = text[:start] + dedent(replacement).lstrip("\n").rstrip() + "\n" + text[end:]


replace_once(
    dedent(
        '''
        FROZEN_GLIB_VENDOR_PREFIX = "third_party/glib-0.18.5-wepld1"
        FROZEN_GLIB_VENDOR_TREE_SHA = "c064fcd71830730d12645b54228326cefefd6188"
        FROZEN_GLIB_PATCHED_VARIANT_BLOB_SHA = "e0997f651b103f7b198e528ee41137ad374e19b8"
        FROZEN_GLIB_LOCK_PACKAGE = ("glib", "0.18.5")
        '''
    ).lstrip("\n"),
    dedent(
        '''
        FROZEN_GLIB_VENDOR_PREFIX = "third_party/glib-0.18.5-wepld1"
        FROZEN_GLIB_VENDOR_TREE_SHA = "c064fcd71830730d12645b54228326cefefd6188"
        # Corroborative acquisition identity only. Enforcement is transitive:
        # the exact vendor tree SHA above binds this descendant blob and every
        # other path/mode/blob in the 121-file frozen subtree.
        FROZEN_GLIB_PATCHED_VARIANT_BLOB_SHA = "e0997f651b103f7b198e528ee41137ad374e19b8"
        FROZEN_GLIB_LOCK_PACKAGE = ("glib", "0.18.5")
        FROZEN_GLIB_REACHABILITY_ROOT = ("wepld-desktop", "0.0.0")
        FROZEN_GLIB_COMPONENT_LOCK_SHA256 = (
            "3816d2befde7412f5a64b2015e437683dcd9876259fd756e7082b0d9c331cbc9"
        )
        '''
    ).lstrip("\n"),
    "frozen component constants",
)

replace_function(
    "def verify_stage_b_templates(view: RepositoryView, stage: str) -> None:\n",
    "\ndef validate_lock_bytes",
    '''
    def require_frozen_component_lock_identity(data: bytes) -> None:
        actual = hashlib.sha256(data).hexdigest()
        if actual != FROZEN_GLIB_COMPONENT_LOCK_SHA256:
            fail(f"component candidate Cargo.lock SHA-256 mismatch: {actual}")


    def verify_stage_b_templates(view: RepositoryView, stage: str) -> None:
        if stage == "S1_PLANNING_ONLY":
            return

        expected_text = dict(STAGE_B_TEXT)
        if stage == COMPONENT_STAGE:
            expected_text["Cargo.toml"] = ROOT_CARGO_COMPONENT

        for relative, expected in expected_text.items():
            read_text_exact(view, relative, expected)

        if stage in {"S1_DEPENDENCY_RESOLUTION_LOCKED", COMPONENT_STAGE}:
            lock_bytes = view.read_bytes(STAGE_B_LOCK_PATH, MAX_LOCKFILE_BYTES)
            if stage == COMPONENT_STAGE:
                require_frozen_component_lock_identity(lock_bytes)
            validate_lock_bytes(
                lock_bytes,
                allow_frozen_glib=(stage == COMPONENT_STAGE),
            )
    ''',
    "stage-b template verifier",
)

replace_once(
    "    validate_lock_graph(observed, declared_edges, source_by_identity)\n",
    """    validate_lock_graph(\n        observed,\n        declared_edges,\n        source_by_identity,\n        required_reachable=(FROZEN_GLIB_LOCK_PACKAGE if allow_frozen_glib else None),\n    )\n""",
    "lock graph invocation",
)

replace_function(
    "def validate_lock_graph(\n",
    "\ndef verify_dependency_register",
    '''
    def validate_lock_graph(
        observed: set[tuple[str, str]],
        declared_edges: Mapping[tuple[str, str], list[str]],
        source_by_identity: Mapping[tuple[str, str], str | None],
        *,
        required_reachable: tuple[str, str] | None = None,
    ) -> None:
        """Require dependency references to resolve uniquely and preserve the
        direct workspace edges implied by exact Stage-B manifests.

        The frozen component stage additionally proves that the source-less glib
        package is transitively reachable from the desktop workspace root.

        STRUCTURALLY_CONSISTENT_LOCK != CARGO_GENERATION_PROVENANCE
        """
        versions_by_name: dict[str, set[str]] = {}
        for name, version in observed:
            versions_by_name.setdefault(name, set()).add(version)

        resolved_edges: dict[tuple[str, str], set[tuple[str, str]]] = {}
        for owner, references in declared_edges.items():
            resolved: set[tuple[str, str]] = set()
            for reference in references:
                name, version, source_qualifier = parse_lock_dependency(owner, reference)
                known = versions_by_name.get(name)
                if not known:
                    fail(
                        "Cargo.lock dependency does not resolve to any package in the "
                        f"lock: {owner[0]} {owner[1]} -> {reference!r}"
                    )
                if version is None:
                    if len(known) != 1:
                        fail(
                            "ambiguous unversioned Cargo.lock dependency reference: "
                            f"{owner[0]} {owner[1]} -> {reference!r}"
                        )
                    version = next(iter(known))
                elif version not in known:
                    fail(
                        "Cargo.lock dependency version does not resolve to a package "
                        f"in the lock: {owner[0]} {owner[1]} -> {reference!r}"
                    )
                target = (name, version)
                if source_qualifier is not None:
                    actual_source = source_by_identity.get(target)
                    if actual_source != source_qualifier:
                        fail(
                            "Cargo.lock dependency source qualifier does not match "
                            f"resolved package: {owner[0]} {owner[1]} -> {reference!r}"
                        )
                resolved.add(target)
            resolved_edges[owner] = resolved

        for owner, required in REQUIRED_LOCK_EDGES.items():
            absent = sorted(required - resolved_edges.get(owner, set()))
            if absent:
                fail(
                    "Cargo.lock is missing required direct dependency edges for "
                    f"{owner[0]} {owner[1]}: " + repr(absent)
                )

        if required_reachable is not None:
            root = FROZEN_GLIB_REACHABILITY_ROOT
            if root not in observed:
                fail("component candidate reachability root is missing from Cargo.lock")

            reachable: set[tuple[str, str]] = set()
            pending = [root]
            while pending:
                current = pending.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                pending.extend(sorted(resolved_edges.get(current, set()) - reachable))

            if required_reachable not in reachable:
                fail(
                    "component candidate frozen glib 0.18.5 is not reachable "
                    "from wepld-desktop"
                )
    ''',
    "lock graph validator",
)

replace_function(
    "def selftest_frozen_glib_component() -> None:\n",
    "\ndef selftest_helper_contract",
    '''
    def selftest_frozen_glib_component() -> None:
        """S1-005: only the exact frozen glib component may enter this stage."""
        base_paths = set(REQUIRED_PATHS) | {"README.md", "src/.gitkeep"}
        stage_b_locked = base_paths | set(STAGE_B_ALL_PATHS)
        vendor_file = FROZEN_GLIB_VENDOR_PREFIX + "/src/variant_iter.rs"
        component_paths = stage_b_locked | {vendor_file}

        if classify_stage(component_paths) != COMPONENT_STAGE:
            fail("self-test: frozen vendor candidate did not enter component stage")
        validate_allowed_paths(component_paths, COMPONENT_STAGE)

        expect_failure_matching(
            "arbitrary third-party subtree",
            "tracked path outside stage allowlist",
            validate_allowed_paths,
            stage_b_locked | {"third_party/evil/payload.rs"},
            COMPONENT_STAGE,
        )

        exact_tree_view = MemoryView(
            {vendor_file: b"patched"},
            trees={FROZEN_GLIB_VENDOR_PREFIX: FROZEN_GLIB_VENDOR_TREE_SHA},
        )
        verify_frozen_glib_vendor(exact_tree_view, {vendor_file}, COMPONENT_STAGE)

        expect_failure_matching(
            "missing frozen vendor subtree identity",
            "returned frozen glib vendor tree object identity is malformed",
            verify_frozen_glib_vendor,
            MemoryView({vendor_file: b"patched"}),
            {vendor_file},
            COMPONENT_STAGE,
        )
        expect_failure_matching(
            "wrong frozen vendor subtree identity",
            "returned frozen glib vendor tree object identity does not match the requested object",
            verify_frozen_glib_vendor,
            MemoryView(
                {vendor_file: b"patched"},
                trees={FROZEN_GLIB_VENDOR_PREFIX: "b" * 40},
            ),
            {vendor_file},
            COMPONENT_STAGE,
        )
        expect_failure_matching(
            "malformed frozen vendor subtree identity",
            "returned frozen glib vendor tree object identity is malformed",
            verify_frozen_glib_vendor,
            MemoryView(
                {vendor_file: b"patched"},
                trees={FROZEN_GLIB_VENDOR_PREFIX: "not-a-sha"},
            ),
            {vendor_file},
            COMPONENT_STAGE,
        )

        disconnected_packages = [dict(package) for package in VALID_LOCK_PACKAGES] + [
            {"name": "glib", "version": "0.18.5"}
        ]
        disconnected_lock = lock_document(disconnected_packages)
        expect_failure_matching(
            "disconnected frozen glib",
            "component candidate frozen glib 0.18.5 is not reachable from wepld-desktop",
            validate_lock_bytes,
            disconnected_lock,
            allow_frozen_glib=True,
        )

        component_packages: list[dict[str, object]] = []
        for package in VALID_LOCK_PACKAGES:
            copied = dict(package)
            if "dependencies" in copied:
                copied["dependencies"] = list(copied["dependencies"])
            if (copied["name"], copied["version"]) == ("tauri", "2.11.5"):
                copied.setdefault("dependencies", [])
                copied["dependencies"].append("glib")
            component_packages.append(copied)
        component_packages.append({"name": "glib", "version": "0.18.5"})
        component_lock = lock_document(component_packages)
        validate_lock_bytes(component_lock, allow_frozen_glib=True)

        expect_failure_matching(
            "source-less glib in ordinary Stage B2",
            "source-less Cargo.lock package is not an expected Stage-B workspace member",
            validate_lock_bytes,
            component_lock,
        )

        registry_glib = [dict(package) for package in component_packages[:-1]] + [
            {"name": "glib", "version": "0.18.5", "source": CRATES_IO_SOURCE}
        ]
        expect_failure_matching(
            "registry glib in frozen component stage",
            "frozen glib 0.18.5 must be source-less in the component candidate",
            validate_lock_bytes,
            lock_document(registry_glib),
            allow_frozen_glib=True,
        )

        component_files = {
            relative: expected.encode("utf-8")
            for relative, expected in STAGE_B_TEXT.items()
        }
        component_files["Cargo.toml"] = ROOT_CARGO_COMPONENT.encode("utf-8")
        component_files[STAGE_B_LOCK_PATH] = component_lock

        expect_failure_matching(
            "synthetic component lock is not the independently frozen exact lock",
            "component candidate Cargo.lock SHA-256 mismatch",
            verify_stage_b_templates,
            MemoryView(component_files),
            COMPONENT_STAGE,
        )

        old_root = dict(component_files)
        old_root["Cargo.toml"] = ROOT_CARGO.encode("utf-8")
        expect_failure_matching(
            "vendor present without exact root patch",
            "exact policy content drifted: Cargo.toml",
            verify_stage_b_templates,
            MemoryView(old_root),
            COMPONENT_STAGE,
        )

        expect_failure_matching(
            "patched root Cargo without component stage",
            "exact policy content drifted: Cargo.toml",
            verify_stage_b_templates,
            MemoryView(component_files),
            "S1_DEPENDENCY_RESOLUTION_LOCKED",
        )
    ''',
    "frozen component selftest",
)

SCRIPT.write_text(text, encoding="utf-8")

spec = SPEC.read_text(encoding="utf-8")

old = """The exact `glib 0.18.5` package entry has no `source` and no `checksum`, as Cargo requires for the selected path source.\n\n## Lock fail-closed rule\n"""
new = """The exact `glib 0.18.5` package entry has no `source` and no `checksum`, as Cargo requires for the selected path source. The component stage additionally requires the complete `Cargo.lock` bytes to match the independently reproduced SHA-256 `3816d2befde7412f5a64b2015e437683dcd9876259fd756e7082b0d9c331cbc9`. A structurally plausible but hand-edited component lock is rejected.\n\nThe policy also requires the exact source-less `glib 0.18.5` identity to be transitively reachable from the `wepld-desktop 0.0.0` workspace root in the resolved lock graph. Mere presence of a disconnected source-less glib table is not component-acquisition evidence.\n\n## Lock fail-closed rule\n"""
if spec.count(old) != 1:
    raise SystemExit(f"ABORT: spec exact-lock anchor count={spec.count(old)}")
spec = spec.replace(old, new, 1)

old = """SOURCELESS_GLIB_WITH_EXACT_FROZEN_TREE = COMPONENT_CANDIDATE_EVIDENCE\nSOURCELESS_GLIB_WITHOUT_EXACT_FROZEN_TREE = REJECT\nARBITRARY_SOURCELESS_PACKAGE = REJECT\n"""
new = """SOURCELESS_GLIB_WITH_EXACT_FROZEN_TREE_AND_EXACT_LOCK_AND_REACHABILITY = COMPONENT_CANDIDATE_EVIDENCE\nDISCONNECTED_SOURCELESS_GLIB = REJECT\nCOMPONENT_LOCK_SHA256_DRIFT = REJECT\nSOURCELESS_GLIB_WITHOUT_EXACT_FROZEN_TREE = REJECT\nARBITRARY_SOURCELESS_PACKAGE = REJECT\n"""
if spec.count(old) != 1:
    raise SystemExit(f"ABORT: spec invariant anchor count={spec.count(old)}")
spec = spec.replace(old, new, 1)

old = """That tree identity binds the complete descendant path set, file modes, and blob identities. The independently verified patched `src/variant_iter.rs` blob inside that tree is:\n"""
new = """That tree identity binds the complete descendant path set, file modes, and blob identities. The independently verified patched `src/variant_iter.rs` blob inside that tree is recorded as corroborative acquisition evidence; enforcement of that file identity is transitive through the exact subtree SHA rather than a second independent runtime check:\n"""
if spec.count(old) != 1:
    raise SystemExit(f"ABORT: spec blob anchor count={spec.count(old)}")
spec = spec.replace(old, new, 1)

old = """- registry-sourced `glib 0.18.5` rejected in the component stage;\n- positive exact frozen-component lock fixture;\n"""
new = """- registry-sourced `glib 0.18.5` rejected in the component stage;\n- disconnected source-less `glib 0.18.5` rejected for missing workspace reachability;\n- synthetic/hand-edited component lock bytes rejected unless the exact frozen lock SHA-256 matches;\n- positive reachable frozen-component graph fixture, with the exact production lock exercised by the remote-object canary;\n"""
if spec.count(old) != 1:
    raise SystemExit(f"ABORT: spec probe anchor count={spec.count(old)}")
spec = spec.replace(old, new, 1)

spec += """\n\n## Exact-head review reconciliation — Qodo\n\nOn exact PR head `95aaf017c8af1dca41aa663283b63dc77cc94d7c`, Qodo identified that a disconnected source-less `glib 0.18.5` table could satisfy the component lock validator because structural edge resolution did not establish workspace reachability. The finding was independently reconciled as `VALID / MATERIAL / SECURITY_RELEVANT`. The repair requires both transitive reachability from `wepld-desktop` and the exact independently reproduced component-lock SHA-256.\n\nQodo also noted that `FROZEN_GLIB_PATCHED_VARIANT_BLOB_SHA` was not read by policy logic. That finding is `VALID / NON-MATERIAL`: the exact vendor subtree identity already transitively binds the patched blob. The constant remains as corroborative acquisition evidence and is now explicitly documented as such.\n"""

SPEC.write_text(spec, encoding="utf-8")
