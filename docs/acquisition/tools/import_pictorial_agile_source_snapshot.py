#!/usr/bin/env python3
"""One-shot deterministic source importer for the pinned Pictorial + Agile donors.

This script fetches public Git metadata + commit tarballs only. It never executes
donor code, installs dependencies, or activates donor workflows/hooks/installers.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tarfile
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path.cwd()
DATE = "2026-08-23"
EXPECTED_MAIN = os.environ.get(
    "EXPECTED_MAIN", "2ab2fae14bc3b3b1f1e9bc2059972456955aeff7"
)
DONORS = (
    dict(
        component="Pictorial",
        slug="pictorial",
        repo="pbakaus/impeccable",
        revision="56f44523f76efdcec813e67b38ee550e49b16f48",
        tree="3626999bc9c8be4d31f3028c37c74cf544576d15",
        license="Apache-2.0",
        license_blob="bb3f6d23b1f8025514a62a12b51b47d73e3c9aa9",
        notice_blob="0468271c904ae334cfaf27da6f8df3d5f419a1f0",
    ),
    dict(
        component="Agile",
        slug="agile",
        repo="github/spec-kit",
        revision="27f50f7e6b618ea14d74dd4037f9e7c60218b16c",
        tree="5622442d5ff74d21b2cb4349f255d08380f3d69d",
        license="MIT",
        license_blob="28a50fa22639e32febe14e4ffc7a732b0ba8c90a",
        notice_blob=None,
    ),
)
UA = "WePLD-pinned-source-import/2026-08-23"
P_MOD = (
    "Modified by WePLD on 2026-08-23: deterministic Pictorial rebrand/path "
    "integration from the pinned upstream source."
)


def get(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/vnd.github+json"}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def jget(url: str):
    return json.loads(get(url))


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(data)}".encode("ascii") + b"\0" + data
    ).hexdigest()


def inv_digest(rows: list[dict]) -> str:
    payload = "".join(
        json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n"
        for x in sorted(rows, key=lambda r: (r["path"], r["mode"], r["type"], r["sha"]))
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def is_lock(path: str) -> bool:
    return PurePosixPath(path).name.lower() in {
        "bun.lock", "bun.lockb", "package-lock.json", "pnpm-lock.yaml",
        "yarn.lock", "poetry.lock", "uv.lock", "pipfile.lock",
    }


def raw_only(path: str) -> bool:
    return path in {"LICENSE", "NOTICE.md"} or path.startswith(".github/") or is_lock(path)


def pmap(component: str, path: str) -> str:
    if component == "Pictorial":
        for a, b in (
            (".impeccable", ".pictorial"),
            ("IMPECCABLE", "PICTORIAL"),
            ("Impeccable", "Pictorial"),
            ("impeccable", "pictorial"),
        ):
            path = path.replace(a, b)
        return path
    for a, b in (
        (".specify", ".agile"),
        ("SPECIFY_CLI", "AGILE_CLI"),
        ("specify_cli", "agile_cli"),
        ("specify-cli", "wepld-agile"),
        ("SPEC-KIT", "AGILE"), ("SPEC_KIT", "AGILE"), ("SPEC KIT", "AGILE"),
        ("Spec-Kit", "Agile"), ("Spec_Kit", "Agile"), ("Spec Kit", "Agile"),
        ("spec-kit", "agile"), ("spec_kit", "agile"), ("spec kit", "agile"),
        ("SPECKIT", "AGILE"), ("Speckit", "Agile"), ("speckit", "agile"),
    ):
        path = path.replace(a, b)
    path = re.sub(r"(?i)spec(?:[-_]|\s)+kit", "agile", path)
    path = re.sub(r"(?i)speckit", "agile", path)
    path = re.sub(r"(?i)specify(?:[-_]|\s)+cli", "wepld-agile", path)
    return path


def tmap(component: str, text: str) -> str:
    if component == "Pictorial":
        pairs = (
            ("https://github.com/pbakaus/impeccable", "https://github.com/TheHalfMoon/wepld"),
            ("github.com/pbakaus/impeccable", "github.com/TheHalfMoon/wepld"),
            ("https://impeccable.style", "https://github.com/TheHalfMoon/wepld"),
            ("impeccable.style", "github.com/TheHalfMoon/wepld"),
            ("IMPECCABLE", "PICTORIAL"), ("Impeccable", "Pictorial"),
            ("impeccable", "pictorial"),
        )
    else:
        pairs = (
            ("https://github.com/github/spec-kit", "https://github.com/TheHalfMoon/wepld"),
            ("github.com/github/spec-kit", "github.com/TheHalfMoon/wepld"),
            (".specify", ".agile"),
            ("SPECIFY_CLI", "AGILE_CLI"), ("specify_cli", "agile_cli"),
            ("Specify CLI", "Agile CLI"), ("specify CLI", "agile CLI"),
            ("specify-cli", "wepld-agile"),
            ("SPEC-KIT", "AGILE"), ("SPEC_KIT", "AGILE"), ("SPEC KIT", "AGILE"),
            ("Spec-Kit", "Agile"), ("Spec_Kit", "Agile"), ("Spec Kit", "Agile"),
            ("spec-kit", "agile"), ("spec_kit", "agile"), ("spec kit", "agile"),
            ("SPECKIT", "AGILE"), ("Speckit", "Agile"), ("speckit", "agile"),
        )
    for a, b in pairs:
        text = text.replace(a, b)
    if component == "Agile":
        text = text.replace('"specify"', '"agile"').replace("'specify'", "'agile'")
        text = text.replace("`specify`", "`agile`")
        text = re.sub(r"(?m)^(\s*)specify(\s*=)", r"\1agile\2", text)
        text = re.sub(
            r"(?<![A-Za-z0-9_])specify(?=\s+(?:init|check|version|extension|bundle|doctor|help)\b)",
            "agile", text,
        )
        text = re.sub(r"(?i)spec(?:[-_]|\s)+kit", "Agile", text)
        text = re.sub(r"(?i)speckit", "Agile", text)
        text = re.sub(r"(?i)specify(?:[-_]|\s)+cli", "wepld-agile", text)
    return text


def apache_notice(path: str, text: str) -> str:
    p, suf = PurePosixPath(path), PurePosixPath(path).suffix.lower()
    name = p.name.lower()
    if suf in {".md", ".markdown", ".mdx"}:
        mark = "{/* " + P_MOD + " */}" if suf == ".mdx" else f"<!-- {P_MOD} -->"
        if text.startswith("---\n"):
            end = text.find("\n---\n", 4)
            if end >= 0:
                cut = end + 5
                return text[:cut] + mark + "\n" + text[cut:]
        return mark + "\n" + text
    if suf in {".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".rs", ".go", ".java", ".c", ".h", ".cpp", ".hpp"}:
        if text.startswith("#!"):
            first, sep, rest = text.partition("\n")
            return first + "\n// " + P_MOD + ("\n" + rest if sep else "\n")
        return "// " + P_MOD + "\n" + text
    if suf in {".css", ".scss", ".sass", ".less"}:
        return "/* " + P_MOD + " */\n" + text
    if suf in {".html", ".htm", ".xml", ".svg", ".vue", ".svelte"}:
        mark = f"<!-- {P_MOD} -->"
        if suf in {".xml", ".svg"} and text.startswith("<?xml"):
            first, sep, rest = text.partition("\n")
            return first + "\n" + mark + ("\n" + rest if sep else "\n")
        return mark + "\n" + text
    if suf in {".py", ".sh", ".bash", ".zsh", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".conf", ".graphql", ".gql"} or name.startswith("."):
        if text.startswith("#!"):
            first, sep, rest = text.partition("\n")
            return first + "\n# " + P_MOD + ("\n" + rest if sep else "\n")
        return "# " + P_MOD + "\n" + text
    if suf == ".sql":
        return "-- " + P_MOD + "\n" + text
    if suf in {".txt", ".text"}:
        return P_MOD + "\n\n" + text
    if suf == ".json":
        obj = json.loads(text)
        if not isinstance(obj, dict) or "_wepldModificationNotice" in obj:
            raise RuntimeError(f"unsafe Apache JSON modification notice: {path}")
        return json.dumps({"_wepldModificationNotice": P_MOD, **obj}, ensure_ascii=False, indent=2) + "\n"
    raise RuntimeError(f"FAIL_CLOSED_UNSUPPORTED_APACHE_NOTICE_FORMAT: {path}")


def write(dest: Path, mode: str, data: bytes) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if mode == "120000":
        dest.symlink_to(data.decode())
    elif mode in {"100644", "100755"}:
        dest.write_bytes(data)
        dest.chmod(0o755 if mode == "100755" else 0o644)
    else:
        raise RuntimeError(f"unsupported blob mode {mode}: {dest}")


def archive(repo: str, rev: str):
    raw = get(f"https://codeload.github.com/{repo}/tar.gz/{rev}")
    bio = io.BytesIO(raw)
    tf = tarfile.open(fileobj=bio, mode="r:gz")
    members = {}
    for m in tf.getmembers():
        bits = m.name.split("/", 1)
        if len(bits) != 2 or not bits[1]:
            continue
        rel = bits[1]
        if rel.startswith("/") or ".." in PurePosixPath(rel).parts:
            raise RuntimeError(f"unsafe archive path: {rel}")
        members[rel] = m
    return tf, members, bio


def read_blob(tf, members, row) -> bytes:
    m = members.get(row["path"])
    if not m:
        raise RuntimeError(f"archive missing tracked blob: {row['path']}")
    if row["mode"] == "120000":
        if not m.issym():
            raise RuntimeError(f"expected symlink: {row['path']}")
        return m.linkname.encode()
    if not m.isfile():
        raise RuntimeError(f"expected regular file: {row['path']}")
    f = tf.extractfile(m)
    if f is None:
        raise RuntimeError(f"unreadable archive member: {row['path']}")
    return f.read()


def tags(path: str, mode: str, text: str | None) -> set[str]:
    out, low, name = set(), path.lower(), PurePosixPath(path).name.lower()
    if is_lock(path): out.add("lockfile")
    if name in {"package.json", "pyproject.toml", "requirements.txt", "cargo.toml", "go.mod", "gemfile"}:
        out.add("dependency_manifest")
    if low.startswith(".github/workflows/"): out.add("workflow")
    if "hooks" in PurePosixPath(low).parts or "hook" in PurePosixPath(low).parts: out.add("hook")
    if "install" in name or name in {"setup.py", "setup.cfg"}: out.add("install_surface")
    if mode == "100755": out.add("executable")
    if text:
        t = text.lower()
        if any(x in t for x in ("http://", "https://", "fetch(", "urllib.", "requests.", "axios", "curl ", "wget ")): out.add("network_or_egress_marker")
        if any(x in t for x in ("openai", "anthropic", "claude", "gemini", "copilot", "api key")): out.add("model_or_provider_marker")
        if any(x in t for x in ("playwright", "puppeteer", "selenium", "browser", "chrome")): out.add("browser_marker")
        if any(x in t for x in ("telemetry", "analytics", "sentry", "posthog")): out.add("telemetry_marker")
    return out


def branding(component: str, text: str) -> list[str]:
    pats = [r"(?i)impeccable"] if component == "Pictorial" else [
        r"(?i)spec(?:[-_]|\s)+kit", r"(?i)speckit", r"(?i)specify(?:[-_]|\s)+cli"
    ]
    return [p for p in pats if re.search(p, text)]


def main() -> None:
    cargo = (ROOT / "Cargo.toml").read_text()
    if re.search(r'(?i)vendor[/\\*]', cargo):
        raise RuntimeError("FAIL_CLOSED_ROOT_WORKSPACE_ALREADY_REFERENCES_VENDOR")
    for p in (ROOT / "vendor/pictorial", ROOT / "vendor/agile"):
        if p.exists():
            raise RuntimeError(f"FAIL_CLOSED_DESTINATION_EXISTS: {p}")

    (ROOT / "legal/third-party").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/acquisition/source-maps").mkdir(parents=True, exist_ok=True)
    reports, surfaces = {}, {}

    for d in DONORS:
        comp, slug, repo, rev, tree_sha = (
            d["component"], d["slug"], d["repo"], d["revision"], d["tree"]
        )
        commit = jget(f"https://api.github.com/repos/{repo}/git/commits/{rev}")
        if commit["tree"]["sha"] != tree_sha:
            raise RuntimeError(f"{comp}: commit/tree pin mismatch")
        tree = jget(f"https://api.github.com/repos/{repo}/git/trees/{tree_sha}?recursive=1")
        if tree.get("sha") != tree_sha or tree.get("truncated") is not False:
            raise RuntimeError(f"{comp}: recursive tree not exact/non-truncated")
        leaves = [
            dict(path=e["path"], mode=e["mode"], type=e["type"], sha=e["sha"])
            for e in tree["tree"] if e["type"] != "tree"
        ]
        canon = {(x["path"], x["mode"], x["type"], x["sha"]) for x in leaves}
        if len(canon) != len(leaves) or len({x["path"] for x in leaves}) != len(leaves):
            raise RuntimeError(f"{comp}: duplicate canonical inventory identity/path")
        by_path = {x["path"]: x for x in leaves}
        if by_path.get("LICENSE", {}).get("sha") != d["license_blob"]:
            raise RuntimeError(f"{comp}: license pin mismatch")
        if comp == "Pictorial" and by_path.get("NOTICE.md", {}).get("sha") != d["notice_blob"]:
            raise RuntimeError("Pictorial: NOTICE pin mismatch")

        tf, members, bio = archive(repo, rev)
        smap, seen, surf = [], set(), defaultdict(list)
        dispositions, modes, types = Counter(), Counter(), Counter()
        modified = binary = gitlinks = 0
        visual = []
        try:
            for e in sorted(leaves, key=lambda x: x["path"]):
                up = e["path"]; modes[e["mode"]] += 1; types[e["type"]] += 1
                if e["type"] == "commit" or e["mode"] == "160000":
                    gitlinks += 1; dispositions["excluded"] += 1
                    smap.append(dict(
                        upstream_repository=repo, upstream_revision=rev, upstream_tree=tree_sha,
                        upstream_path=up, upstream_git_mode=e["mode"],
                        upstream_git_object_type=e["type"], upstream_object_sha=e["sha"],
                        import_disposition="excluded", wepld_path=None, wepld_object_sha=None,
                        renamed_or_modified=False, license=d["license"],
                        modification_notice_status="not_applicable_gitlink_excluded",
                        exclusion_reason="Tracked gitlink targets nested repository content outside this pinned donor tree snapshot; nested repository retrieval is not authorized by this source-import gate.",
                    ))
                    continue
                if e["type"] != "blob":
                    raise RuntimeError(f"{comp}: unsupported non-tree type: {e}")
                raw = read_blob(tf, members, e)
                if blob_sha(raw) != e["sha"]:
                    raise RuntimeError(f"{comp}: archive/blob SHA mismatch: {up}")
                try: raw_text = raw.decode("utf-8")
                except UnicodeDecodeError: raw_text = None; binary += 1
                for tag in tags(up, e["mode"], raw_text): surf[tag].append(up)

                if up == "LICENSE":
                    dest_rel = f"legal/third-party/{comp.upper()}_LICENSE.txt"
                    data, nstat = raw, "preserved_verbatim"
                elif comp == "Pictorial" and up == "NOTICE.md":
                    dest_rel = "legal/third-party/PICTORIAL_NOTICE.md"
                    data, nstat = raw, "preserved_verbatim"
                else:
                    mapped = pmap(comp, up); dest_rel = f"vendor/{slug}/{mapped}"
                    data = raw
                    nstat = "not_required_mit" if comp == "Agile" else "unmodified_upstream_content"
                    if raw_text is not None and not raw_only(up):
                        text2 = tmap(comp, raw_text)
                        if text2 != raw_text:
                            if comp == "Pictorial":
                                text2 = apache_notice(mapped, text2)
                                nstat = "prominent_notice_embedded_in_modified_file"
                            else:
                                nstat = "mit_rebrand_modified"
                            data = text2.encode(); modified += 1
                    if raw_text is None and PurePosixPath(mapped).suffix.lower() in {
                        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".mp4", ".mov", ".pdf"
                    }:
                        visual.append(up)

                if dest_rel in seen:
                    raise RuntimeError(f"{comp}: destination collision: {dest_rel}")
                seen.add(dest_rel)
                if e["mode"] == "120000":
                    data = pmap(comp, data.decode()).encode()
                write(ROOT / dest_rel, e["mode"], data)
                dispositions["imported"] += 1
                smap.append(dict(
                    upstream_repository=repo, upstream_revision=rev, upstream_tree=tree_sha,
                    upstream_path=up, upstream_git_mode=e["mode"],
                    upstream_git_object_type=e["type"], upstream_object_sha=e["sha"],
                    import_disposition="imported", wepld_path=dest_rel,
                    wepld_object_sha=blob_sha(data),
                    renamed_or_modified=(dest_rel != f"vendor/{slug}/{up}" or data != raw),
                    license=d["license"], modification_notice_status=nstat, exclusion_reason=None,
                ))
        finally:
            tf.close(); bio.close()

        mapped = {
            (r["upstream_path"], r["upstream_git_mode"], r["upstream_git_object_type"], r["upstream_object_sha"])
            for r in smap
        }
        if mapped != canon or len(smap) != len(leaves):
            raise RuntimeError(f"{comp}: FAIL_CLOSED_EXACT_SET_EQUALITY")

        violations = []
        for r in smap:
            dest = r["wepld_path"]
            if not dest or not dest.startswith(f"vendor/{slug}/"):
                continue
            rel = dest[len(f"vendor/{slug}/"):]
            if rel.startswith(".github/") or is_lock(rel):
                continue
            if branding(comp, dest):
                violations.append((dest, "path")); continue
            p = ROOT / dest
            try:
                txt = os.readlink(p) if p.is_symlink() else p.read_text()
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            hit = branding(comp, txt)
            if hit: violations.append((dest, hit))
        if violations:
            raise RuntimeError(f"{comp}: FAIL_CLOSED_PRODUCT_BRANDING_GATE: {violations[:20]}")

        mp = ROOT / f"docs/acquisition/source-maps/{slug}-source-map-2026-08-23.jsonl"
        mp.write_text("".join(
            json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"
            for r in sorted(smap, key=lambda x: x["upstream_path"])
        ))
        reread = [json.loads(x) for x in mp.read_text().splitlines() if x]
        serialized = {
            (r["upstream_path"], r["upstream_git_mode"], r["upstream_git_object_type"], r["upstream_object_sha"])
            for r in reread
        }
        if serialized != canon or len(reread) != len(leaves):
            raise RuntimeError(f"{comp}: serialized map exact-set failure")

        reports[comp] = dict(
            repository=repo, revision=rev, root_tree=tree_sha,
            tracked_non_tree_entries=len(leaves), source_map_records=len(smap),
            inventory_sha256=inv_digest(leaves), exact_set_equality=True,
            dispositions=dict(sorted(dispositions.items())),
            git_modes=dict(sorted(modes.items())), git_types=dict(sorted(types.items())),
            modified_text_entries=modified, binary_entries=binary, excluded_gitlinks=gitlinks,
            binary_visual_branding_review_candidates=sorted(visual),
        )
        surfaces[comp] = {k: sorted(v) for k, v in sorted(surf.items())}

    (ROOT / "legal/third-party/PICTORIAL_MODIFICATIONS.md").write_text(
        "# Pictorial modification record\n\n"
        "WePLD imported pinned `pbakaus/impeccable` revision "
        "`56f44523f76efdcec813e67b38ee550e49b16f48` on 2026-08-23. "
        "Every Pictorial text file changed by the deterministic rebrand carries an "
        "embedded modification notice. The Apache-2.0 license and upstream NOTICE "
        "are preserved verbatim beside this record; source maps identify each result.\n"
    )
    (ROOT / "legal/third-party/AGILE_MODIFICATIONS.md").write_text(
        "# Agile modification record\n\n"
        "WePLD imported pinned `github/spec-kit` revision "
        "`27f50f7e6b618ea14d74dd4037f9e7c60218b16c` on 2026-08-23. "
        "The MIT license is preserved verbatim; source maps identify each rebranded result.\n"
    )
    (ROOT / "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_SURFACE_INVENTORY_2026-08-23.json").write_text(
        json.dumps(dict(
            generated=DATE,
            method="static lexical inventory only; no donor code executed and no dependencies installed",
            dependency_admission="NONE", donor_workflow_execution="NONE", surfaces=surfaces,
        ), indent=2, sort_keys=True) + "\n"
    )
    (ROOT / "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_REPORT_2026-08-23.md").write_text(
        "# WePLD Pictorial + Agile source import report\n\n"
        "```text\n"
        f"BASE_MAIN={EXPECTED_MAIN}\n"
        "BRANCH=import/pictorial-agile-full-source-snapshot-2026-08-23\n"
        "SOURCE_IMPORT_EXECUTION=COMPLETE\nSOURCE_BYTES_IMPORTED=YES\n"
        "SOURCE_ADMISSION=SOURCE_ONLY\nDEPENDENCY_ADMISSION=NONE\n"
        "DEPENDENCIES_INSTALLED=NO\nDONOR_WORKFLOW_EXECUTION=NONE\n"
        "IMPORTED_WORKFLOW_ACTIVATION=NONE\nIMPORTED_HOOK_EXECUTION=NONE\n"
        "IMPORTED_INSTALL_SCRIPT_EXECUTION=NONE\nIMPORTED_TELEMETRY_ACTIVATION=NONE\n"
        "IMPORTED_NETWORK_ACTIVATION=NONE\nH0_014_PLUS=NOT_STARTED\n"
        "H0_SCREEN_EXECUTION=NONE\nMODEL_PROVIDER_EXECUTION=NONE\n"
        "MODEL_WEIGHT_ACCESS=NONE\nMODEL_INFERENCE=NONE\n"
        "PR88_MINIMAX_CHAIN=SEPARATE_UNCHANGED_BY_IMPORTER\n"
        "PR126_DIAGNOSTIC=LEFT_CLOSED_UNCHANGED\n```\n\n"
        "## Exact-set accounting\n\n```json\n"
        + json.dumps(reports, indent=2, sort_keys=True)
        + "\n```\n\n## Inertness\n\n"
        "Donor workflows, hooks, install surfaces, lockfiles, release/telemetry/network "
        "material remain nested under `vendor/**` as inert source data. The importer "
        "does not execute them, install dependencies, register vendor packages in the "
        "root Cargo workspace, or add donor workflows to the WePLD root workflow surface.\n\n"
        "## Merge readiness\n\n"
        "`NOT_READY_FOR_MERGE`. Independent exact-head review, listed binary visual-branding "
        "review, repository policy/security qualification, and remaining canonical contract "
        "gates are still required. Dependency/runtime admission remains separately unauthorized.\n"
    )
    for needed in (
        "vendor/pictorial", "vendor/agile", "legal/third-party/PICTORIAL_LICENSE.txt",
        "legal/third-party/PICTORIAL_NOTICE.md", "legal/third-party/AGILE_LICENSE.txt",
    ):
        if not (ROOT / needed).exists():
            raise RuntimeError(f"missing required output: {needed}")
    print(json.dumps(reports, sort_keys=True))


if __name__ == "__main__":
    main()
