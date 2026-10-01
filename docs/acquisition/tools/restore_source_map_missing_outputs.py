#!/usr/bin/env python3
"""Restore only source-map-declared outputs missing from the committed candidate.

The original importer proved the complete working-tree mapping before staging. Imported
.gitignore rules can nevertheless cause `git add` to omit mapped hidden files. This
repair reads the committed source maps, identifies paths absent from HEAD, fetches only
the corresponding pinned Git blobs, reproduces the original deterministic import bytes,
and requires the reconstructed Git blob SHA to equal the source-map-recorded WePLD SHA.

No donor code is executed. No dependency is installed or admitted.
"""
from __future__ import annotations

import base64
import importlib.util
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path.cwd()
IMPORTER = ROOT / "docs/acquisition/tools/import_pictorial_agile_source_snapshot.py"
spec = importlib.util.spec_from_file_location("wepld_original_importer", IMPORTER)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load original pinned-source importer")
orig = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = orig
spec.loader.exec_module(orig)

META = {
    "pictorial": {"component": "Pictorial", "repo": "pbakaus/impeccable"},
    "agile": {"component": "Agile", "repo": "github/spec-kit"},
}


def committed_paths() -> set[str]:
    out = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "HEAD"], text=True)
    return {line for line in out.splitlines() if line}


def git_blob(repo: str, sha: str) -> bytes:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/git/blobs/{sha}",
        headers={"User-Agent": "WePLD-source-map-restore/2026-08-23", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        obj = json.load(r)
    if obj.get("sha") != sha or obj.get("encoding") != "base64":
        raise RuntimeError(f"unexpected Git blob response for {repo}@{sha}")
    return base64.b64decode(obj["content"])


def reproduce_original(component: str, slug: str, row: dict, raw: bytes) -> bytes:
    up = row["upstream_path"]
    if orig.blob_sha(raw) != row["upstream_object_sha"]:
        raise RuntimeError(f"{component}: upstream blob identity mismatch: {up}")

    if up == "LICENSE":
        expected_dest = f"legal/third-party/{component.upper()}_LICENSE.txt"
        data = raw
    elif component == "Pictorial" and up == "NOTICE.md":
        expected_dest = "legal/third-party/PICTORIAL_NOTICE.md"
        data = raw
    else:
        mapped = orig.pmap(component, up)
        expected_dest = f"vendor/{slug}/{mapped}"
        data = raw
        try:
            raw_text = raw.decode("utf-8")
        except UnicodeDecodeError:
            raw_text = None
        if raw_text is not None and not orig.raw_only(up):
            text2 = orig.tmap(component, raw_text)
            if text2 != raw_text:
                if component == "Pictorial":
                    text2 = orig.apache_notice(mapped, text2)
                data = text2.encode()
        if row["upstream_git_mode"] == "120000":
            data = orig.pmap(component, data.decode()).encode()

    if expected_dest != row["wepld_path"]:
        raise RuntimeError(
            f"{component}: source-map destination no longer matches original importer: "
            f"{up}: map={row['wepld_path']} original={expected_dest}"
        )
    actual = orig.blob_sha(data)
    if actual != row["wepld_object_sha"]:
        raise RuntimeError(
            f"{component}: reconstructed original-import object mismatch for {up}: "
            f"expected={row['wepld_object_sha']} actual={actual}"
        )
    return data


def main() -> None:
    committed = committed_paths()
    restored: list[dict] = []
    missing_total: list[tuple[str, dict]] = []

    for slug, meta in META.items():
        map_path = ROOT / f"docs/acquisition/source-maps/{slug}-source-map-2026-08-23.jsonl"
        rows = [json.loads(line) for line in map_path.read_text().splitlines() if line]
        for row in rows:
            if row["import_disposition"] == "excluded":
                continue
            path = row["wepld_path"]
            if not path:
                raise RuntimeError(f"{meta['component']}: non-excluded row has no destination: {row['upstream_path']}")
            if path not in committed:
                missing_total.append((slug, row))

    for slug, row in missing_total:
        meta = META[slug]
        if row["upstream_git_object_type"] != "blob":
            raise RuntimeError(f"unsupported missing mapped object type: {row}")
        raw = git_blob(meta["repo"], row["upstream_object_sha"])
        data = reproduce_original(meta["component"], slug, row, raw)
        dest = ROOT / row["wepld_path"]
        if dest.exists() or dest.is_symlink():
            raise RuntimeError(f"missing-from-HEAD output unexpectedly exists before restoration: {dest}")
        orig.write(dest, row["upstream_git_mode"], data)
        restored.append(
            {
                "component": meta["component"],
                "upstream_path": row["upstream_path"],
                "wepld_path": row["wepld_path"],
                "upstream_object_sha": row["upstream_object_sha"],
                "reconstructed_wepld_object_sha": orig.blob_sha(data),
            }
        )

    for item in restored:
        p = ROOT / item["wepld_path"]
        if not p.exists() and not p.is_symlink():
            raise RuntimeError(f"restored path missing from working tree: {item['wepld_path']}")

    evidence = {
        "status": "PASS",
        "head_before_restore": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "missing_committed_outputs_detected": len(missing_total),
        "restored_outputs": restored,
        "dependency_admission": "NONE",
        "dependencies_installed": False,
        "donor_code_execution": "NONE",
    }
    out = ROOT / "docs/acquisition/WEPLD_PICTORIAL_AGILE_COMMITTED_TREE_RESTORE_EVIDENCE_2026-08-23.json"
    out.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()
