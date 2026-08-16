#!/usr/bin/env python3
from pathlib import Path

path = Path(".github/scripts/wepld_integrity.py")
text = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"ABORT: patch anchor {label!r} count={count}, expected 1")
    text = text.replace(old, new, 1)


replace_once(
    '''ROOT_CARGO = """[workspace]
resolver = "2"
members = [
  "apps/desktop/src-tauri",
  "crates/contracts",
  "crates/core",
]
"""

DESKTOP_CARGO =''',
    '''ROOT_CARGO = """[workspace]
resolver = "2"
members = [
  "apps/desktop/src-tauri",
  "crates/contracts",
  "crates/core",
]
"""

ROOT_CARGO_COMPONENT = ROOT_CARGO + """
[patch.crates-io]
glib = { path = "third_party/glib-0.18.5-wepld1" }
"""

DESKTOP_CARGO =''',
    "root component template",
)

replace_once(
    '''STAGE_B_INPUT_PATHS = frozenset(STAGE_B_TEXT)
STAGE_B_LOCK_PATH = "Cargo.lock"
STAGE_B_ALL_PATHS = STAGE_B_INPUT_PATHS | {STAGE_B_LOCK_PATH}

COMMON_EXACT_ALLOWED =''',
    '''STAGE_B_INPUT_PATHS = frozenset(STAGE_B_TEXT)
STAGE_B_LOCK_PATH = "Cargo.lock"
STAGE_B_ALL_PATHS = STAGE_B_INPUT_PATHS | {STAGE_B_LOCK_PATH}

COMPONENT_STAGE = "S1_COMPONENT_ACQUISITION_CANDIDATE"
FROZEN_GLIB_VENDOR_PREFIX = "third_party/glib-0.18.5-wepld1"
FROZEN_GLIB_VENDOR_TREE_SHA = "c064fcd71830730d12645b54228326cefefd6188"
FROZEN_GLIB_PATCHED_VARIANT_BLOB_SHA = "e0997f651b103f7b198e528ee41137ad374e19b8"
FROZEN_GLIB_LOCK_PACKAGE = ("glib", "0.18.5")

COMMON_EXACT_ALLOWED =''',
    "frozen vendor constants",
)

replace_once(
    '''class RepositoryView:
    def entries(self) -> list[TrackedEntry]:
        raise NotImplementedError

    def read_bytes(self, relative: str, limit: int) -> bytes:
        raise NotImplementedError

    def read_text''',
    '''class RepositoryView:
    def entries(self) -> list[TrackedEntry]:
        raise NotImplementedError

    def read_bytes(self, relative: str, limit: int) -> bytes:
        raise NotImplementedError

    def tree_identity(self, relative: str) -> str | None:
        raise NotImplementedError

    def read_text''',
    "repository view tree identity",
)

replace_once(
    '''        if len(data) > limit:
            fail(f"file exceeds bounded size {limit}: {relative}")
        return data


def require_object_identity''',
    '''        if len(data) > limit:
            fail(f"file exceeds bounded size {limit}: {relative}")
        return data

    def tree_identity(self, relative: str) -> str | None:
        try:
            raw = subprocess.check_output(
                ["git", "-C", str(self.root), "rev-parse", "--verify", f"HEAD:{relative}"],
                stderr=subprocess.STDOUT,
                text=True,
            ).strip()
        except subprocess.CalledProcessError:
            return None
        if not OBJECT_SHA_RE.fullmatch(raw):
            fail(f"local subtree object identity is malformed: {relative}: {raw!r}")
        return raw.lower()


def require_object_identity''',
    "local tree identity",
)

replace_once(
    '''        self._blobs: dict[str, tuple[str, int]] = {}
        self._entries: list[TrackedEntry] = []
        self._cache: dict[str, bytes] = {}
        self._load_tree()''',
    '''        self._blobs: dict[str, tuple[str, int]] = {}
        self._trees: dict[str, str] = {}
        self._entries: list[TrackedEntry] = []
        self._cache: dict[str, bytes] = {}
        self._load_tree()''',
    "remote tree cache",
)

replace_once(
    '''            item_type = item.get("type")
            if item_type == "tree":
                continue
            path = item.get("path")
            mode = item.get("mode")
            object_sha = item.get("sha")
            if not isinstance(path, str) or not isinstance(mode, str):
                fail("candidate Git tree path/mode is malformed")
            self._entries.append(TrackedEntry(mode=mode, path=path))

            if item_type == "blob":''',
    '''            item_type = item.get("type")
            path = item.get("path")
            mode = item.get("mode")
            object_sha = item.get("sha")
            if not isinstance(path, str) or not isinstance(mode, str):
                fail("candidate Git tree path/mode is malformed")

            if item_type == "tree":
                if mode != "040000":
                    fail(f"candidate subtree has unexpected mode {mode}: {path}")
                if not isinstance(object_sha, str) or not OBJECT_SHA_RE.fullmatch(object_sha):
                    fail(f"candidate subtree SHA is malformed: {path}")
                self._trees[path] = object_sha.lower()
                continue

            self._entries.append(TrackedEntry(mode=mode, path=path))

            if item_type == "blob":''',
    "remote subtree identity capture",
)

replace_once(
    '''    def entries(self) -> list[TrackedEntry]:
        return list(self._entries)

    def read_bytes(self, relative: str, limit: int) -> bytes:''',
    '''    def entries(self) -> list[TrackedEntry]:
        return list(self._entries)

    def tree_identity(self, relative: str) -> str | None:
        return self._trees.get(relative)

    def read_bytes(self, relative: str, limit: int) -> bytes:''',
    "remote tree identity reader",
)

replace_once(
    '''def classify_stage(paths: set[str]) -> str:
    present = paths & STAGE_B_ALL_PATHS
    if not present:
        return "S1_PLANNING_ONLY"

    missing_inputs = STAGE_B_INPUT_PATHS - paths
    if missing_inputs:
        fail(
            "partial dependency-resolution candidate is prohibited; missing: "
            + ", ".join(sorted(missing_inputs))
        )

    if STAGE_B_LOCK_PATH in paths:
        return "S1_DEPENDENCY_RESOLUTION_LOCKED"
    return "S1_DEPENDENCY_RESOLUTION_INPUT"
''',
    '''def classify_stage(paths: set[str]) -> str:
    third_party_paths = {path for path in paths if path.startswith("third_party/")}
    if third_party_paths:
        missing_component_inputs = STAGE_B_ALL_PATHS - paths
        if missing_component_inputs:
            fail(
                "partial component-acquisition candidate is prohibited; missing: "
                + ", ".join(sorted(missing_component_inputs))
            )
        return COMPONENT_STAGE

    present = paths & STAGE_B_ALL_PATHS
    if not present:
        return "S1_PLANNING_ONLY"

    missing_inputs = STAGE_B_INPUT_PATHS - paths
    if missing_inputs:
        fail(
            "partial dependency-resolution candidate is prohibited; missing: "
            + ", ".join(sorted(missing_inputs))
        )

    if STAGE_B_LOCK_PATH in paths:
        return "S1_DEPENDENCY_RESOLUTION_LOCKED"
    return "S1_DEPENDENCY_RESOLUTION_INPUT"
''',
    "component stage classification",
)

replace_once(
    '''    if stage in {"S1_DEPENDENCY_RESOLUTION_INPUT", "S1_DEPENDENCY_RESOLUTION_LOCKED"}:
        allowed |= STAGE_B_INPUT_PATHS
        if stage == "S1_DEPENDENCY_RESOLUTION_LOCKED":
            allowed.add(STAGE_B_LOCK_PATH)

    unexpected = sorted(paths - allowed)''',
    '''    if stage in {"S1_DEPENDENCY_RESOLUTION_INPUT", "S1_DEPENDENCY_RESOLUTION_LOCKED"}:
        allowed |= STAGE_B_INPUT_PATHS
        if stage == "S1_DEPENDENCY_RESOLUTION_LOCKED":
            allowed.add(STAGE_B_LOCK_PATH)
    elif stage == COMPONENT_STAGE:
        allowed |= STAGE_B_ALL_PATHS
        allowed |= {
            path
            for path in paths
            if path.startswith(FROZEN_GLIB_VENDOR_PREFIX + "/")
        }

    unexpected = sorted(paths - allowed)''',
    "component stage allowlist",
)

replace_once(
    '''def verify_stage_b_templates(view: RepositoryView, stage: str) -> None:
    if stage == "S1_PLANNING_ONLY":
        return
    for relative, expected in STAGE_B_TEXT.items():
        read_text_exact(view, relative, expected)
    if stage == "S1_DEPENDENCY_RESOLUTION_LOCKED":
        validate_lock_bytes(view.read_bytes(STAGE_B_LOCK_PATH, MAX_LOCKFILE_BYTES))


def validate_lock_bytes(data: bytes) -> None:''',
    '''def verify_frozen_glib_vendor(view: RepositoryView, paths: set[str], stage: str) -> None:
    if stage != COMPONENT_STAGE:
        return

    vendor_paths = {
        path
        for path in paths
        if path.startswith(FROZEN_GLIB_VENDOR_PREFIX + "/")
    }
    if not vendor_paths:
        fail("component-acquisition candidate is missing the frozen glib vendor subtree")

    returned_tree = view.tree_identity(FROZEN_GLIB_VENDOR_PREFIX)
    require_object_identity(
        "frozen glib vendor tree",
        FROZEN_GLIB_VENDOR_TREE_SHA,
        returned_tree,
    )


def verify_stage_b_templates(view: RepositoryView, stage: str) -> None:
    if stage == "S1_PLANNING_ONLY":
        return

    expected_text = dict(STAGE_B_TEXT)
    if stage == COMPONENT_STAGE:
        expected_text["Cargo.toml"] = ROOT_CARGO_COMPONENT

    for relative, expected in expected_text.items():
        read_text_exact(view, relative, expected)

    if stage in {"S1_DEPENDENCY_RESOLUTION_LOCKED", COMPONENT_STAGE}:
        validate_lock_bytes(
            view.read_bytes(STAGE_B_LOCK_PATH, MAX_LOCKFILE_BYTES),
            allow_frozen_glib=(stage == COMPONENT_STAGE),
        )


def validate_lock_bytes(data: bytes, *, allow_frozen_glib: bool = False) -> None:''',
    "component template and vendor verification",
)

replace_once(
    '''        if identity in WORKSPACE_LOCK_PACKAGES:
            if source is not None:
                fail(
                    "expected Stage-B workspace package unexpectedly has source: "
                    f"{name} {version}: {source}"
                )
            if checksum is not None:
                fail(f"workspace/path package unexpectedly carries checksum: {name}")
            continue

        if source is None:
            fail(
                "source-less Cargo.lock package is not an expected Stage-B "
                f"workspace member: {name} {version}"
            )''',
    '''        if identity in WORKSPACE_LOCK_PACKAGES:
            if source is not None:
                fail(
                    "expected Stage-B workspace package unexpectedly has source: "
                    f"{name} {version}: {source}"
                )
            if checksum is not None:
                fail(f"workspace/path package unexpectedly carries checksum: {name}")
            continue

        if allow_frozen_glib and identity == FROZEN_GLIB_LOCK_PACKAGE:
            if source is not None:
                fail(
                    "frozen glib 0.18.5 must be source-less in the component candidate: "
                    f"{source}"
                )
            if checksum is not None:
                fail("frozen glib 0.18.5 must be checksum-less in the component candidate")
            continue

        if source is None:
            fail(
                "source-less Cargo.lock package is not an expected Stage-B "
                f"workspace member: {name} {version}"
            )''',
    "source-less frozen glib lock rule",
)

replace_once(
    '''    source_by_identity = {
        (name, version): source for name, version, source in identities
    }
    observed = set(name_versions)
    missing = sorted(REQUIRED_LOCK_PACKAGES - observed)''',
    '''    source_by_identity = {
        (name, version): source for name, version, source in identities
    }
    observed = set(name_versions)

    if allow_frozen_glib:
        if FROZEN_GLIB_LOCK_PACKAGE not in observed:
            fail("component candidate Cargo.lock is missing frozen glib 0.18.5")
        if source_by_identity.get(FROZEN_GLIB_LOCK_PACKAGE) is not None:
            fail("component candidate glib 0.18.5 did not resolve to the frozen path source")

    missing = sorted(REQUIRED_LOCK_PACKAGES - observed)''',
    "component glib lock presence",
)

replace_once(
    '''    verify_dependency_register(view)
    verify_archive(view)
    verify_stage_b_templates(view, stage)
''',
    '''    verify_dependency_register(view)
    verify_archive(view)
    verify_frozen_glib_vendor(view, paths, stage)
    verify_stage_b_templates(view, stage)
''',
    "verify frozen vendor in main flow",
)

replace_once(
    '''class MemoryView(RepositoryView):
    def __init__(
        self,
        files: dict[str, bytes],
        modes: dict[str, str] | None = None,
    ):
        self.files = dict(files)
        self.modes = dict(modes or {})

    def entries(self) -> list[TrackedEntry]:
        return [
            TrackedEntry(mode=self.modes.get(path, "100644"), path=path)
            for path in self.files
        ]

    def read_bytes(self, relative: str, limit: int) -> bytes:
        if relative not in self.files:
            fail(f"memory view missing file: {relative}")
        data = self.files[relative]
        if len(data) > limit:
            fail(f"memory-view file exceeds bound: {relative}")
        return data
''',
    '''class MemoryView(RepositoryView):
    def __init__(
        self,
        files: dict[str, bytes],
        modes: dict[str, str] | None = None,
        trees: dict[str, str] | None = None,
    ):
        self.files = dict(files)
        self.modes = dict(modes or {})
        self.trees = dict(trees or {})

    def entries(self) -> list[TrackedEntry]:
        return [
            TrackedEntry(mode=self.modes.get(path, "100644"), path=path)
            for path in self.files
        ]

    def read_bytes(self, relative: str, limit: int) -> bytes:
        if relative not in self.files:
            fail(f"memory view missing file: {relative}")
        data = self.files[relative]
        if len(data) > limit:
            fail(f"memory-view file exceeds bound: {relative}")
        return data

    def tree_identity(self, relative: str) -> str | None:
        return self.trees.get(relative)
''',
    "memory tree identity",
)

replace_once(
    '''    selftest_helper_contract()
    selftest_baseline_comparison_sha()''',
    '''    selftest_frozen_glib_component()
    selftest_helper_contract()
    selftest_baseline_comparison_sha()''',
    "component selftest call",
)

insert_before = '''def selftest_helper_contract() -> None:
'''
component_tests = '''def selftest_frozen_glib_component() -> None:
    """S1-005: only the exact frozen glib subtree may enter the component stage."""
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

    component_packages = [dict(package) for package in VALID_LOCK_PACKAGES] + [
        {"name": "glib", "version": "0.18.5"}
    ]
    component_lock = lock_document(component_packages)
    validate_lock_bytes(component_lock, allow_frozen_glib=True)

    expect_failure_matching(
        "source-less glib in ordinary Stage B2",
        "source-less Cargo.lock package is not an expected Stage-B workspace member",
        validate_lock_bytes,
        component_lock,
    )

    registry_glib = [dict(package) for package in VALID_LOCK_PACKAGES] + [
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
        relative: expected.encode("utf-8") for relative, expected in STAGE_B_TEXT.items()
    }
    component_files["Cargo.toml"] = ROOT_CARGO_COMPONENT.encode("utf-8")
    component_files[STAGE_B_LOCK_PATH] = component_lock
    verify_stage_b_templates(MemoryView(component_files), COMPONENT_STAGE)

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


'''
if text.count(insert_before) != 1:
    raise SystemExit("ABORT: component selftest insertion anchor mismatch")
text = text.replace(insert_before, component_tests + insert_before, 1)

path.write_text(text, encoding="utf-8")
