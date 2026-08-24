#!/usr/bin/env python3
"""Dependency-free adapter for Pictorial + Agile rebrand repair.

This wrapper deliberately admits no renderer/package dependency. Pictorial raster
icons are generated as deterministic PNGs with Python stdlib only. Agile donor
marketing/demo binaries are replaced by WePLD-owned SVG equivalents and every
text reference is rewritten to the new SVG destination. The canonical second-stage
repair then performs source-map, legal, exact-set, and branding validation.
"""
from __future__ import annotations

import binascii
import importlib.util
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path.cwd()
BASE_TOOL = ROOT / "docs/acquisition/tools/repair_pictorial_agile_rebrand.py"
spec = importlib.util.spec_from_file_location("wepld_rebrand_base", BASE_TOOL)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load canonical rebrand repair")
base = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)

AGILE_VISUAL_DESTS = {
    "docs/images/spec-kit-logo.webp": "docs/images/agile-logo.svg",
    "media/bootstrap-claude-code.gif": "media/agile-bootstrap.svg",
    "media/logo_large.webp": "media/agile-logo-large.svg",
    "media/logo_small.webp": "media/agile-logo-small.svg",
    "media/spec-kit-video-header.jpg": "media/agile-video-header.svg",
    "media/specify_cli.gif": "media/agile-cli.svg",
}

_original_desired_path = base.desired_path
_original_repair_agile = base.repair_agile


def desired_path(component: str, upstream: str) -> str:
    if component == "Agile" and upstream in AGILE_VISUAL_DESTS:
        return "vendor/agile/" + AGILE_VISUAL_DESTS[upstream]
    return _original_desired_path(component, upstream)


def repair_agile(text: str) -> str:
    text = _original_repair_agile(text)
    for old, new in (
        ("docs/images/agile-logo.webp", "docs/images/agile-logo.svg"),
        ("media/bootstrap-claude-code.gif", "media/agile-bootstrap.svg"),
        ("media/logo_large.webp", "media/agile-logo-large.svg"),
        ("media/logo_small.webp", "media/agile-logo-small.svg"),
        ("media/agile-video-header.jpg", "media/agile-video-header.svg"),
        ("media/agile_cli.gif", "media/agile-cli.svg"),
        ("agile-logo.webp", "agile-logo.svg"),
        ("bootstrap-claude-code.gif", "agile-bootstrap.svg"),
        ("logo_large.webp", "agile-logo-large.svg"),
        ("logo_small.webp", "agile-logo-small.svg"),
        ("agile-video-header.jpg", "agile-video-header.svg"),
        ("agile_cli.gif", "agile-cli.svg"),
    ):
        text = text.replace(old, new)
    return text


def chunk(kind: bytes, data: bytes) -> bytes:
    crc = binascii.crc32(kind)
    crc = binascii.crc32(data, crc) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)


def set_px(buf: bytearray, width: int, height: int, x: int, y: int, rgb: tuple[int, int, int]) -> None:
    if 0 <= x < width and 0 <= y < height:
        i = (y * width + x) * 3
        buf[i:i+3] = bytes(rgb)


def fill_rect(buf: bytearray, width: int, height: int, x0: int, y0: int, x1: int, y1: int, rgb: tuple[int, int, int]) -> None:
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(width, x1), min(height, y1)
    row = bytes(rgb) * max(0, x1 - x0)
    for y in range(y0, y1):
        i = (y * width + x0) * 3
        buf[i:i+len(row)] = row


def line(buf: bytearray, width: int, height: int, x0: int, y0: int, x1: int, y1: int, rgb: tuple[int, int, int], thick: int) -> None:
    dx = abs(x1-x0); sx = 1 if x0 < x1 else -1
    dy = -abs(y1-y0); sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        fill_rect(buf, width, height, x0-thick//2, y0-thick//2, x0+(thick+1)//2, y0+(thick+1)//2, rgb)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy


FONT = {
    "A": ["01110","10001","10001","11111","10001","10001","10001"],
    "C": ["01111","10000","10000","10000","10000","10000","01111"],
    "E": ["11111","10000","10000","11110","10000","10000","11111"],
    "I": ["11111","00100","00100","00100","00100","00100","11111"],
    "L": ["10000","10000","10000","10000","10000","10000","11111"],
    "O": ["01110","10001","10001","10001","10001","10001","01110"],
    "P": ["11110","10001","10001","11110","10000","10000","10000"],
    "R": ["11110","10001","10001","11110","10100","10010","10001"],
    "T": ["11111","00100","00100","00100","00100","00100","00100"],
    "W": ["10001","10001","10001","10101","10101","10101","01010"],
    "D": ["11110","10001","10001","10001","10001","10001","11110"],
}


def draw_text(buf: bytearray, width: int, height: int, text: str, x: int, y: int, scale: int, rgb: tuple[int, int, int]) -> None:
    cx = x
    for ch in text.upper():
        if ch == " ":
            cx += 4 * scale
            continue
        glyph = FONT.get(ch)
        if glyph is None:
            cx += 6 * scale
            continue
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "1":
                    fill_rect(buf, width, height, cx+gx*scale, y+gy*scale, cx+(gx+1)*scale, y+(gy+1)*scale, rgb)
        cx += 6 * scale


def pictorial_pixels(width: int, height: int, promo: bool) -> bytes:
    bg = (24, 23, 29); white = (245, 243, 239); magenta = (202, 46, 130); gray = (154, 149, 161)
    buf = bytearray(bytes(bg) * width * height)
    if promo:
        margin = max(12, min(width, height)//12)
        fill_rect(buf, width, height, margin, margin, width-margin, margin+3, magenta)
        fill_rect(buf, width, height, margin, height-margin-3, width-margin, height-margin, magenta)
        scale = max(2, min(width//65, height//35))
        draw_text(buf, width, height, "PICTORIAL", margin+12, height//3, scale, white)
        draw_text(buf, width, height, "WEPLD", margin+12, height*2//3, max(1, scale//2), gray)
        return bytes(buf)
    m = max(2, min(width, height)//4)
    thick = max(1, min(width, height)//18)
    cx, cy = width//2, height//2
    span = max(2, min(width, height)//5)
    line(buf, width, height, m, m, cx-span//2, m, white, thick)
    line(buf, width, height, m, m, m, cy-span//2, white, thick)
    line(buf, width, height, width-m-1, m, cx+span//2, m, white, thick)
    line(buf, width, height, width-m-1, m, width-m-1, cy-span//2, white, thick)
    line(buf, width, height, m, height-m-1, cx-span//2, height-m-1, white, thick)
    line(buf, width, height, m, height-m-1, m, cy+span//2, white, thick)
    line(buf, width, height, width-m-1, height-m-1, cx+span//2, height-m-1, white, thick)
    line(buf, width, height, width-m-1, height-m-1, width-m-1, cy+span//2, white, thick)
    r = max(1, min(width, height)//10)
    for y in range(cy-r, cy+r+1):
        for x in range(cx-r, cx+r+1):
            if (x-cx)*(x-cx)+(y-cy)*(y-cy) <= r*r:
                set_px(buf, width, height, x, y, magenta)
    return bytes(buf)


def write_png(dest: Path, width: int, height: int, pixels: bytes) -> None:
    raw = b"".join(b"\x00" + pixels[y*width*3:(y+1)*width*3] for y in range(height))
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"tEXt", b"WePLD-Modification-Notice\x00" + base.P_VISUAL_MOD.encode("latin-1"))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    dest.write_bytes(png)


def render_visual(component: str, upstream: str, dest: Path, dims: tuple[int, int]) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    width, height = dims
    if component == "Agile":
        if dest.suffix.lower() != ".svg":
            raise RuntimeError(f"Agile visual replacement must be SVG: {dest}")
        dest.write_text(base.svg_for(component, upstream, width, height) + "\n")
        return
    if dest.suffix.lower() == ".svg":
        dest.write_text(base.svg_for(component, upstream, width, height) + "\n")
        return
    if dest.suffix.lower() != ".png":
        raise RuntimeError(f"unsupported Pictorial visual destination: {dest}")
    write_png(dest, width, height, pictorial_pixels(width, height, upstream.endswith("promo-small.png")))


base.desired_path = desired_path
base.repair_agile = repair_agile
base.render_visual = render_visual

base.main()

# Correct the base report's renderer wording to the actual dependency-free path used.
surface_path = ROOT / "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_SURFACE_INVENTORY_2026-08-23.json"
surface = __import__("json").loads(surface_path.read_text())
surface["rebrand_repair"]["host_visual_renderer"] = "Python 3 stdlib only; no repository/runtime dependency"
surface_path.write_text(__import__("json").dumps(surface, indent=2, sort_keys=True) + "\n")

report_path = ROOT / "docs/acquisition/WEPLD_PICTORIAL_AGILE_SOURCE_IMPORT_REPORT_2026-08-23.md"
report = report_path.read_text().replace(
    "ImageMagick, when present on the GitHub-hosted runner, is used only as an ephemeral host renderer for WePLD-owned replacement artwork and is not admitted as a WePLD dependency.",
    "WePLD-owned visual replacements are generated with Python 3 standard-library code only; no renderer package is installed or admitted as a WePLD dependency."
)
report_path.write_text(report)
