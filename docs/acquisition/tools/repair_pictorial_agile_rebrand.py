#!/usr/bin/env python3
"""Fail-closed second-stage rebrand repair for the pinned Pictorial + Agile import.

This tool operates only on the already-imported source snapshot. It executes no donor
code, installs no dependencies, and grants no runtime/dependency authority. Public
GitHub Git-tree metadata is re-read only to re-prove exact upstream accounting.
Visual replacements are rendered from WePLD-owned inline SVGs with the preinstalled
ImageMagick host tool; no donor visual bytes are executed or transformed in place.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.request
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT = Path.cwd()
DATE = "2026-08-23"
BRANCH = "import/pictorial-agile-full-source-snapshot-2026-08-23"
BASE_MAIN = "2ab2fae14bc3b3b1f1e9bc2059972456955aeff7"
P_MOD = (
    "Modified by WePLD on 2026-08-23: deterministic Pictorial rebrand/path "
    "integration from the pinned upstream source."
)
P_VISUAL_MOD = (
    "Modified by WePLD on 2026-08-23: replaced upstream visual branding with "
    "a WePLD-owned Pictorial brand asset."
)

DONORS = {
    "Pictorial": {
        "slug": "pictorial",
        "repo": "pbakaus/impeccable",
        "revision": "56f44523f76efdcec813e67b38ee550e49b16f48",
        "tree": "3626999bc9c8be4d31f3028c37c74cf544576d15",
        "license": "Apache-2.0",
        "inventory_sha256": "1fdcb041c9883ab670a35b0f2107a6c7320ceec62b144deaca20f365e31ceb3b",
        "count": 3267,
    },
    "Agile": {
        "slug": "agile",
        "repo": "github/spec-kit",
        "revision": "27f50f7e6b618ea14d74dd4037f9e7c60218b16c",
        "tree": "5622442d5ff74d21b2cb4349f255d08380f3d69d",
        "license": "MIT",
        "inventory_sha256": "ed2f9e5e5892b980cc45a920f2c8e8f70264f603e70dbe136af0d796c722385c",
        "count": 545,
    },
}

VISUALS = {
    "Pictorial": {
        "extension/icons/icon.svg": (128, 128),
        "extension/icons/icon-16.png": (16, 16),
        "extension/icons/icon-32.png": (32, 32),
        "extension/icons/icon-48.png": (48, 48),
        "extension/icons/icon-128.png": (128, 128),
        "extension/icons/promo-small.png": (440, 280),
        "scripts/lib/assets/plugin-icon.png": (180, 180),
    },
    "Agile": {
        "docs/images/spec-kit-logo.webp": (1080, 1080),
        "media/bootstrap-claude-code.gif": (1080, 806),
        "media/logo_large.webp": (1080, 1080),
        "media/logo_small.webp": (200, 200),
        "media/spec-kit-video-header.jpg": (1280, 720),
        "media/specify_cli.gif": (1280, 720),
    },
}

BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".mp4", ".mov", ".pdf"}
LOCKS = {"bun.lock", "bun.lockb", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "uv.lock", "pipfile.lock"}
CLI_SUBCOMMANDS = "init|check|version|extension|bundle|doctor|help|self|integration|preset"
AGILE_PROHIBITED = [
    re.compile(r"(?i)spec(?:[-_]|\s)+kit"),
    re.compile(r"(?i)speckit"),
    re.compile(r"(?i)specify(?:[-_]|\s)+cli"),
]
PICTORIAL_PROHIBITED = [re.compile(r"(?i)impeccable")]


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}".encode("ascii") + b"\0" + data).hexdigest()


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "WePLD-rebrand-repair/2026-08-23"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def is_lock(path: str) -> bool:
    return PurePosixPath(path).name.lower() in LOCKS


def raw_only(path: str) -> bool:
    return path in {"LICENSE", "NOTICE.md"} or path.startswith(".github/") or is_lock(path)


def desired_path(component: str, upstream: str) -> str:
    if upstream == "LICENSE":
        return f"legal/third-party/{component.upper()}_LICENSE.txt"
    if component == "Pictorial" and upstream == "NOTICE.md":
        return "legal/third-party/PICTORIAL_NOTICE.md"
    parts = list(PurePosixPath(upstream).parts)
    if component == "Pictorial":
        parts = [
            p.replace(".impeccable", ".pictorial")
             .replace("IMPECCABLE", "PICTORIAL")
             .replace("Impeccable", "Pictorial")
             .replace("impeccable", "pictorial")
            for p in parts
        ]
        return "vendor/pictorial/" + "/".join(parts)

    # IMPORTANT: .specify is a config-directory identity only when it is a whole
    # path segment. Do not turn speckit.specify.md into agile.agile.md.
    parts = [".agile" if p == ".specify" else p for p in parts]
    path = "/".join(parts)
    path = path.replace("SPECIFY_CLI", "AGILE_CLI").replace("specify_cli", "agile_cli")
    path = path.replace("specify-cli", "wepld-agile")
    path = re.sub(r"(?i)spec(?:[-_]|\s)+kit", "agile", path)
    path = re.sub(r"(?i)speckit", "agile", path)
    return "vendor/agile/" + path


def repair_pictorial(text: str, rel: str) -> str:
    text = text.replace("pbakaus/pictorial", "TheHalfMoon/wepld")
    text = text.replace("https://www.npmjs.com/package/pictorial", "https://www.npmjs.com/package/@wepld/pictorial")
    text = re.sub(r"\bnpx\s+pictorial\b", "npx @wepld/pictorial", text)
    text = re.sub(r"\b(npm\s+(?:install|i)|pnpm\s+add|bun\s+add)\s+pictorial\b", r"\1 @wepld/pictorial", text)
    if rel == "package.json":
        obj = json.loads(text)
        obj["name"] = "@wepld/pictorial"
        text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    return text


def repair_agile(text: str) -> str:
    # Repair malformed repository/docs identities created by naive donor-name substitution.
    text = re.sub(
        r"https://raw\.githubusercontent\.com/github/(?:spec-kit|agile)/([^/]+)/",
        r"https://raw.githubusercontent.com/TheHalfMoon/wepld/\1/vendor/agile/",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"https://github\.github\.io/(?:spec-kit|agile)/?",
        "https://github.com/TheHalfMoon/wepld/tree/main/vendor/agile/docs/",
        text,
        flags=re.I,
    )
    text = re.sub(r"(?i)github/(?:spec-kit|agile)", "TheHalfMoon/wepld", text)
    text = text.replace("GitHub Agile", "Agile")

    # Contract identities.
    text = re.sub(r"(?i)spec(?:[-_]|\s)+kit", "Agile", text)
    text = re.sub(r"(?i)speckit", "Agile", text)
    text = re.sub(r"(?i)specify(?:[-_]|\s)+cli", "wepld-agile", text)
    text = text.replace("SPECIFY_", "AGILE_")
    text = text.replace("specify_cli", "agile_cli")
    text = text.replace("agile.agile", "agile.specify")
    text = text.replace("agile-agile", "agile-specify")

    # Bare 'specify' is ordinary English and remains allowed, except when it is the
    # executable immediately followed by one of the pinned CLI's known subcommands.
    text = re.sub(
        rf"(?<![A-Za-z0-9_./-])specify(?=\s+(?:{CLI_SUBCOMMANDS})\b)",
        "agile",
        text,
        flags=re.I,
    )
    return text


def ensure_pictorial_notice(text: str, rel: str) -> str:
    if "Modified by WePLD on 2026-08-23" in text:
        return text
    suffix = PurePosixPath(rel).suffix.lower()
    if suffix == ".json":
        obj = json.loads(text)
        if not isinstance(obj, dict):
            raise RuntimeError(f"cannot embed Apache modification notice in non-object JSON: {rel}")
        return json.dumps({"_wepldModificationNotice": P_MOD, **obj}, ensure_ascii=False, indent=2) + "\n"
    if suffix in {".md", ".markdown"}:
        return f"<!-- {P_MOD} -->\n{text}"
    if suffix == ".mdx":
        return "{/* " + P_MOD + " */}\n" + text
    if suffix in {".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".rs", ".go", ".java", ".c", ".h", ".cpp", ".hpp"}:
        if text.startswith("#!"):
            first, _, rest = text.partition("\n")
            return first + "\n// " + P_MOD + "\n" + rest
        return "// " + P_MOD + "\n" + text
    if suffix in {".html", ".htm", ".xml", ".svg", ".vue", ".svelte"}:
        return f"<!-- {P_MOD} -->\n{text}"
    if suffix in {".py", ".sh", ".bash", ".zsh", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".conf"} or PurePosixPath(rel).name.startswith("."):
        if text.startswith("#!"):
            first, _, rest = text.partition("\n")
            return first + "\n# " + P_MOD + "\n" + rest
        return "# " + P_MOD + "\n" + text
    if suffix in {".css", ".scss", ".sass", ".less"}:
        return "/* " + P_MOD + " */\n" + text
    if suffix == ".sql":
        return "-- " + P_MOD + "\n" + text
    if suffix in {".txt", ".text"}:
        return P_MOD + "\n\n" + text
    raise RuntimeError(f"FAIL_CLOSED_UNSUPPORTED_APACHE_REPAIR_NOTICE_FORMAT: {rel}")


def svg_for(component: str, upstream: str, width: int, height: int) -> str:
    if component == "Pictorial":
        label = "Pictorial" if width >= 180 else ""
        sub = "Design intelligence · WePLD source snapshot" if width >= 400 else ""
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<!-- {P_VISUAL_MOD} -->
<rect width="100%" height="100%" rx="{max(3, min(width,height)//8)}" fill="#18171d"/>
<path d="M {width*.28:.1f} {height*.30:.1f} H {width*.45:.1f} M {width*.28:.1f} {height*.30:.1f} V {height*.47:.1f} M {width*.72:.1f} {height*.30:.1f} H {width*.55:.1f} M {width*.72:.1f} {height*.30:.1f} V {height*.47:.1f} M {width*.28:.1f} {height*.70:.1f} H {width*.45:.1f} M {width*.28:.1f} {height*.70:.1f} V {height*.53:.1f} M {width*.72:.1f} {height*.70:.1f} H {width*.55:.1f} M {width*.72:.1f} {height*.70:.1f} V {height*.53:.1f}" stroke="#f5f3ef" stroke-width="{max(1,width//40)}" stroke-linecap="round"/>
<circle cx="50%" cy="50%" r="{max(2,min(width,height)//12)}" fill="#ca2e82"/>
<text x="8%" y="28%" fill="#f5f3ef" font-family="DejaVu Sans" font-size="{max(12,min(width,height)//7)}" font-weight="700">{label}</text>
<text x="8%" y="82%" fill="#aaa5b0" font-family="DejaVu Sans" font-size="{max(9,min(width,height)//18)}">{sub}</text>
</svg>'''

    label = "Agile" if width >= 180 else ""
    sub = "Specification &amp; delivery method · WePLD source snapshot" if width >= 600 else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" rx="{max(3,min(width,height)//12)}" fill="#f5f7f6"/>
<rect x="{width*.16:.1f}" y="{height*.18:.1f}" width="{width*.34:.1f}" height="{height*.64:.1f}" rx="{max(4,min(width,height)//24)}" fill="#142232"/>
<path d="M {width*.22:.1f} {height*.67:.1f} L {width*.32:.1f} {height*.54:.1f} L {width*.43:.1f} {height*.36:.1f}" stroke="#248b8b" stroke-width="{max(2,min(width,height)//45)}" fill="none"/>
<circle cx="{width*.22:.1f}" cy="{height*.67:.1f}" r="{max(2,min(width,height)//50)}" fill="#f5f7f6"/><circle cx="{width*.32:.1f}" cy="{height*.54:.1f}" r="{max(2,min(width,height)//50)}" fill="#f5f7f6"/><circle cx="{width*.43:.1f}" cy="{height*.36:.1f}" r="{max(2,min(width,height)//45)}" fill="#54b48c"/>
<text x="55%" y="46%" fill="#142232" font-family="DejaVu Sans" font-size="{max(12,min(width,height)//8)}" font-weight="700">{label}</text>
<text x="55%" y="56%" fill="#49646a" font-family="DejaVu Sans" font-size="{max(9,min(width,height)//26)}">{sub}</text>
</svg>'''


def render_visual(component: str, upstream: str, dest: Path, dims: tuple[int, int]) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    svg = svg_for(component, upstream, *dims)
    if dest.suffix.lower() == ".svg":
        dest.write_text(svg + "\n")
        return
    tool = shutil.which("magick") or shutil.which("convert")
    if not tool:
        raise RuntimeError("FAIL_CLOSED_IMAGEMAGICK_HOST_TOOL_NOT_AVAILABLE")
    cmd = [tool, "svg:-", "-strip"]
    if component == "Pictorial" and dest.suffix.lower() == ".png":
        cmd += ["-set", "comment", P_VISUAL_MOD]
    cmd.append(str(dest))
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = "0"
    subprocess.run(cmd, input=svg.encode(), check=True, env=env)
    if not dest.exists() or dest.stat().st_size == 0:
        raise RuntimeError(f"visual renderer produced no output: {dest}")


def data_for(path: Path, mode: str) -> bytes:
    if mode == "120000":
        return os.readlink(path).encode()
    return path.read_bytes()


def scan_user_surface(component: str, slug: str) -> list[tuple[str, str]]:
    failures: list[tuple[str, str]] = []
    base = ROOT / "vendor" / slug
    for p in base.rglob("*"):
        if not p.is_file() and not p.is_symlink():
            continue
        rel = p.relative_to(base).as_posix()
        parts = set(PurePosixPath(rel).parts)
        if rel.startswith(".github/") or is_lock(rel) or parts & {"test", "tests", "fixture", "fixtures"}:
            continue
        if p.suffix.lower() in BINARY_SUFFIXES:
            continue
        try:
            text = os.readlink(p) if p.is_symlink() else p.read_text()
        except UnicodeDecodeError:
            continue
        pats = PICTORIAL_PROHIBITED if component == "Pictorial" else AGILE_PROHIBITED
        for pat in pats:
            if pat.search(text) or pat.search(rel):
                failures.append((rel, pat.pattern))
        if component == "Pictorial":
            for pat in (r"(?i)pbakaus/pictorial", r"(?i)\bnpx\s+pictorial\b"):
                if re.search(pat, text):
                    failures.append((rel, pat))
        else:
            residuals = [
                r"(?i)github/(?:spec-kit|agile)",
                r"(?i)github\.github\.io/(?:spec-kit|agile)",
                r"\bSPECIFY_[A-Z0-9_]+",
                r"(?i)\bagile[.-]agile\b",
                rf"(?i)(?<![A-Za-z0-9_./-])specify(?=\s+(?:{CLI_SUBCOMMANDS})\b)",
            ]
            for pat in residuals:
                if re.search(pat, text) or re.search(pat, rel):
                    failures.append((rel, pat))
    return failures


def negative_fixture_selftest() -> None:
    agile_bad = [
        "specify-cli", "specify_cli", "specify cli", "specify  cli", "specify\tcli",
        "specify_cli_adapter", "speckit2", "speckit_extension", "spec-kit2",
        "Spec  Kit", "Spec\tKit",
    ]
    for sample in agile_bad:
        if not any(p.search(sample) for p in AGILE_PROHIBITED):
            raise RuntimeError(f"branding negative fixture escaped Agile gate: {sample!r}")
    if not PICTORIAL_PROHIBITED[0].search("impeccable-extension"):
        raise RuntimeError("branding negative fixture escaped Pictorial gate")


def main() -> None:
    negative_fixture_selftest()
    report_rows: dict[str, list[dict]] = {}
    visual_results: dict[str, list[dict]] = {}

    for component, meta in DONORS.items():
        slug = meta["slug"]
        map_path = ROOT / f"docs/acquisition/source-maps/{slug}-source-map-2026-08-23.jsonl"
        rows = [json.loads(line) for line in map_path.read_text().splitlines() if line]
        if len(rows) != meta["count"]:
            raise RuntimeError(f"{component}: source-map count drift before repair")

        upstream_tree = get_json(
            f"https://api.github.com/repos/{meta['repo']}/git/trees/{meta['tree']}?recursive=1"
        )
        if upstream_tree.get("sha") != meta["tree"] or upstream_tree.get("truncated") is not False:
            raise RuntimeError(f"{component}: upstream recursive tree no longer exact/non-truncated")
        canon = {
            (e["path"], e["mode"], e["type"], e["sha"])
            for e in upstream_tree["tree"] if e["type"] != "tree"
        }
        mapped = {
            (r["upstream_path"], r["upstream_git_mode"], r["upstream_git_object_type"], r["upstream_object_sha"])
            for r in rows
        }
        if mapped != canon or len(mapped) != meta["count"]:
            raise RuntimeError(f"{component}: FAIL_CLOSED_EXACT_SET_PRE_REPAIR")

        desired = {}
        for r in rows:
            if r["import_disposition"] == "excluded":
                continue
            d = desired_path(component, r["upstream_path"])
            if d in desired and desired[d] != r["upstream_path"]:
                raise RuntimeError(f"{component}: corrected destination collision: {d}")
            desired[d] = r["upstream_path"]

        # Move path identities first.
        for r in rows:
            if r["import_disposition"] == "excluded":
                continue
            old = ROOT / r["wepld_path"]
            new_rel = desired_path(component, r["upstream_path"])
            new = ROOT / new_rel
            if old != new:
                new.parent.mkdir(parents=True, exist_ok=True)
                if new.exists() and new.resolve() != old.resolve():
                    raise RuntimeError(f"{component}: corrected destination already exists: {new_rel}")
                os.replace(old, new)
                r["wepld_path"] = new_rel

        visuals = []
        for r in rows:
            if r["import_disposition"] == "excluded":
                continue
            up = r["upstream_path"]
            dest = ROOT / r["wepld_path"]
            if up in VISUALS[component]:
                render_visual(component, up, dest, VISUALS[component][up])
                data = data_for(dest, r["upstream_git_mode"])
                r["import_disposition"] = "replaced"
                r["wepld_object_sha"] = blob_sha(data)
                r["renamed_or_modified"] = True
                r["modification_notice_status"] = (
                    "wepld_owned_visual_replacement_with_embedded_modification_notice"
                    if component == "Pictorial" else "wepld_owned_visual_replacement_mit"
                )
                visuals.append({"upstream_path": up, "wepld_path": r["wepld_path"], "wepld_object_sha": r["wepld_object_sha"]})
                continue

            if r["upstream_git_object_type"] != "blob" or raw_only(up):
                data = data_for(dest, r["upstream_git_mode"])
                r["wepld_object_sha"] = blob_sha(data)
                r["renamed_or_modified"] = (
                    r["wepld_path"] != f"vendor/{slug}/{up}" or r["wepld_object_sha"] != r["upstream_object_sha"]
                )
                continue

            try:
                before = dest.read_text()
            except UnicodeDecodeError:
                before = None
            if before is not None:
                rel = dest.relative_to(ROOT / "vendor" / slug).as_posix()
                after = repair_pictorial(before, rel) if component == "Pictorial" else repair_agile(before)
                if after != before:
                    if component == "Pictorial":
                        after = ensure_pictorial_notice(after, rel)
                        r["modification_notice_status"] = "prominent_notice_embedded_in_modified_file"
                    else:
                        r["modification_notice_status"] = "mit_rebrand_modified"
                    dest.write_text(after)
            data = data_for(dest, r["upstream_git_mode"])
            r["wepld_object_sha"] = blob_sha(data)
            r["renamed_or_modified"] = (
                r["wepld_path"] != f"vendor/{slug}/{up}" or r["wepld_object_sha"] != r["upstream_object_sha"]
            )

        # Re-prove exact-set identity and destination/object accounting after repair.
        mapped2 = {
            (r["upstream_path"], r["upstream_git_mode"], r["upstream_git_object_type"], r["upstream_object_sha"])
            for r in rows
        }
        if mapped2 != canon or len(rows) != meta["count"]:
            raise RuntimeError(f"{component}: FAIL_CLOSED_EXACT_SET_POST_REPAIR")
        dests = [r["wepld_path"] for r in rows if r["wepld_path"]]
        if len(dests) != len(set(dests)):
            raise RuntimeError(f"{component}: duplicate destination after repair")
        for r in rows:
            if r["import_disposition"] == "excluded":
                if r["wepld_path"] is not None or r["wepld_object_sha"] is not None or not r["exclusion_reason"]:
                    raise RuntimeError(f"{component}: malformed exclusion: {r['upstream_path']}")
                continue
            p = ROOT / r["wepld_path"]
            if not p.exists() and not p.is_symlink():
                raise RuntimeError(f"{component}: mapped destination missing: {r['wepld_path']}")
            actual = blob_sha(data_for(p, r["upstream_git_mode"]))
            if actual != r["wepld_object_sha"]:
                raise RuntimeError(f"{component}: destination object SHA mismatch: {r['wepld_path']}")

        map_path.write_text("".join(
            json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"
            for r in sorted(rows, key=lambda x: x["upstream_path"])
        ))
        report_rows[component] = rows
        visual_results[component] = visuals

    # Contract-specific identity assertions.
    p_pkg = json.loads((ROOT / "vendor/pictorial/package.json").read_text())
    if p_pkg.get("name") != "@wepld/pictorial" or p_pkg.get("bin", {}).get("pictorial") != "cli/bin/cli.js":
        raise RuntimeError("Pictorial package/CLI identity does not match contract")
    agile_py = (ROOT / "vendor/agile/pyproject.toml").read_text()
    if 'name = "wepld-agile"' not in agile_py or 'agile = "agile_cli:main"' not in agile_py:
        raise RuntimeError("Agile distribution/module/CLI identity does not match contract")
    if (ROOT / "vendor/agile/presets/lean/commands/agile.agile.md").exists():
        raise RuntimeError("Agile path regression: agile.agile.md still exists")
    if not (ROOT / "vendor/agile/presets/lean/commands/agile.specify.md").exists():
        raise RuntimeError("Agile semantic specify command was not preserved")

    failures = scan_user_surface("Pictorial", "pictorial") + scan_user_surface("Agile", "agile")
    if failures:
        raise RuntimeError(f"FAIL_CLOSED_STRICT_PRODUCT_BRANDING_GATE: {failures[:40]}")

    # Legal byte identity remains unchanged.
    legal_expected = {
        "legal/third-party/PICTORIAL_LICENSE.txt": "bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9",
        "legal/third-party/PICTORIAL_NOTICE.md": "0468271c904ae334cfaf27da6f8df3d5f419a1f0",
        "legal/third-party/AGILE_LICENSE.txt": "28a50fa22639e32febe14e4ffc7a732b0ba8c90a",
    }
    for path, expected in legal_expected.items():
        if blob_sha((ROOT / path).read_bytes()) != expected:
            raise RuntimeError(f"legal provenance byte drift: {path}")

    (ROOT / "legal/third-party/PICTORIAL_MODIFICATIONS.md").write_text(
        "# Pictorial modification record\n\n"
        "WePLD imported pinned `pbakaus/impeccable` revision `56f44523f76efdcec813e67b38ee550e49b16f48` on 2026-08-23. "
        "Deterministically rebranded Pictorial text files carry embedded Apache modification notices. "
        "The upstream visual identity in the extension icons, promotional tile, plugin icon, and SVG icon was replaced with WePLD-owned Pictorial artwork; PNG replacements carry embedded modification metadata and the SVG carries an embedded modification comment. "
        "The Apache-2.0 license and upstream NOTICE are preserved verbatim; the source map records every resulting object.\n"
    )
    (ROOT / "legal/third-party/AGILE_MODIFICATIONS.md").write_text(
        "# Agile modification record\n\n"
        "WePLD imported pinned `github/spec-kit` revision `27f50f7e6b618ea14d74dd4037f9e7c60218b16c` on 2026-08-23. "
        "The deterministic rebrand maps the distribution to `wepld-agile`, the module namespace to `agile_cli`, the CLI to `agile`, and the product capability to Agile. "
        "Upstream logo/demo/video binary branding was replaced with WePLD-owned Agile artwork. The MIT license is preserved verbatim; the source map records every resulting object.\n"
    )

    surface_path = ROOT / "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_SURFACE_INVENTORY_2026-08-23.json"
    surface = json.loads(surface_path.read_text())
    surface["dependency_admission"] = "NONE"
    surface["donor_workflow_execution"] = "NONE"
    surface["rebrand_repair"] = {
        "method": "deterministic second-stage static repair; WePLD-owned visuals rendered locally; no donor code executed",
        "strict_product_branding_gate": "PASS",
        "negative_fixture_gate": "PASS",
        "visual_replacements": visual_results,
        "host_visual_renderer": "preinstalled ImageMagick only; not a repository/runtime dependency",
    }
    surface_path.write_text(json.dumps(surface, indent=2, sort_keys=True) + "\n")

    accounting = {}
    for component, rows in report_rows.items():
        meta = DONORS[component]
        disp = Counter(r["import_disposition"] for r in rows)
        modified_nonbinary = sum(
            1 for r in rows
            if r["wepld_path"] and PurePosixPath(r["wepld_path"]).suffix.lower() not in BINARY_SUFFIXES
            and r["wepld_object_sha"] != r["upstream_object_sha"]
        )
        accounting[component] = {
            "repository": meta["repo"],
            "revision": meta["revision"],
            "root_tree": meta["tree"],
            "tracked_non_tree_entries": len(rows),
            "source_map_records": len(rows),
            "inventory_sha256": meta["inventory_sha256"],
            "exact_set_equality": True,
            "dispositions": dict(sorted(disp.items())),
            "modified_nonbinary_entries": modified_nonbinary,
            "wepld_owned_visual_replacements": visual_results[component],
            "binary_visual_branding_review_candidates": [],
        }

    report = ROOT / "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_REPORT_2026-08-23.md"
    report.write_text(
        "# WePLD Pictorial + Agile source import report\n\n"
        "```text\n"
        f"BASE_MAIN={BASE_MAIN}\nBRANCH={BRANCH}\n"
        "SOURCE_IMPORT_EXECUTION=COMPLETE\nSOURCE_BYTES_IMPORTED=YES\nSOURCE_ADMISSION=SOURCE_ONLY\n"
        "DERIVATIVE_REBRAND_REPAIR=COMPLETE\nSTRICT_PRODUCT_BRANDING_GATE=PASS\nBRANDING_NEGATIVE_FIXTURES=PASS\n"
        "BINARY_VISUAL_BRANDING_REVIEW=RESOLVED_BY_WEPLD_OWNED_REPLACEMENTS\n"
        "DEPENDENCY_ADMISSION=NONE\nDEPENDENCIES_INSTALLED=NO\nDONOR_WORKFLOW_EXECUTION=NONE\n"
        "IMPORTED_WORKFLOW_ACTIVATION=NONE\nIMPORTED_HOOK_EXECUTION=NONE\nIMPORTED_INSTALL_SCRIPT_EXECUTION=NONE\n"
        "IMPORTED_TELEMETRY_ACTIVATION=NONE\nIMPORTED_NETWORK_ACTIVATION=NONE\n"
        "H0_014_PLUS=NOT_STARTED\nH0_SCREEN_EXECUTION=NONE\nMODEL_PROVIDER_EXECUTION=NONE\nMODEL_WEIGHT_ACCESS=NONE\nMODEL_INFERENCE=NONE\n"
        "PR88_MINIMAX_CHAIN=SEPARATE_UNCHANGED_BY_REPAIR\nPR126_DIAGNOSTIC=LEFT_CLOSED_UNCHANGED\n"
        "MERGE_READY=NO\nFOUNDATION_INTEGRITY_EXACT_HEAD=REQUIRES_FRESH_QUALIFICATION\n"
        "```\n\n## Exact-set accounting after rebrand repair\n\n```json\n"
        + json.dumps(accounting, indent=2, sort_keys=True)
        + "\n```\n\n## Inertness\n\n"
        "All imported workflow/release/hook/install/telemetry/network/provider surfaces remain nested under `vendor/**` as inert source data. "
        "This repair executes no donor code and installs no dependencies. ImageMagick, when present on the GitHub-hosted runner, is used only as an ephemeral host renderer for WePLD-owned replacement artwork and is not admitted as a WePLD dependency.\n\n"
        "## Merge readiness\n\n"
        "`NOT_READY_FOR_MERGE`. Source accounting, legal preservation, deterministic identity repair, negative branding fixtures, and the source-import branding gate pass in this repair stage. "
        "A fresh exact-head foundation/repository-policy qualification and the remaining canonical security/parity/review gates are still required. Dependency/runtime admission remains separately unauthorized.\n"
    )

    print(json.dumps({
        "status": "PASS",
        "accounting": accounting,
        "dependency_admission": "NONE",
        "donor_workflow_execution": "NONE",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
