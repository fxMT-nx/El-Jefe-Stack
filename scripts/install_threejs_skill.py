#!/usr/bin/env python3
"""Instala la skill 'threejs' adaptada a DSH.

- Descarga los SKILL.md del bundle CloudAI-X/threejs-skills (MIT).
- Trocea cada documento en referencias <= --max-chars para que quepan en el
  presupuesto de resultados de herramientas de DSH (evita la poda a 8 KB).
- Copia el SKILL.md paraguas del repo y genera references/SOURCE.md.

Uso:
    python scripts/install_threejs_skill.py
    python scripts/install_threejs_skill.py --dest "C:/ruta/skills/threejs"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "CloudAI-X/threejs-skills"
BRANCH = "main"
TOPICS = [
    "threejs-fundamentals",
    "threejs-geometry",
    "threejs-materials",
    "threejs-textures",
    "threejs-lighting",
    "threejs-loaders",
    "threejs-asset-pipeline",
    "threejs-animation",
    "threejs-interaction",
    "threejs-shaders",
    "threejs-postprocessing",
    "threejs-performance",
    "threejs-react-three-fiber",
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "el-jefe-stack"})
    with urllib.request.urlopen(req, timeout=30) as res:  # noqa: S310 - URL fija de GitHub
        return res.read()


def api(url: str) -> dict:
    return json.loads(fetch(url).decode("utf-8"))


def split_units(text: str) -> list[str]:
    """Divide en unidades: párrafos o bloques de código completos."""
    units: list[str] = []
    buf: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            buf.append(line)
            continue
        buf.append(line)
        if not in_fence and line.strip() == "":
            units.append("".join(buf))
            buf = []
    if buf:
        units.append("".join(buf))
    return units


def hard_split(unit: str, max_chars: int) -> list[str]:
    """Parte una unidad demasiado grande respetando fences cuando se puede."""
    lines = unit.splitlines(keepends=True)
    if lines and lines[0].lstrip().startswith("```") and lines[-1].strip() == "```":
        fence = lines[0].rstrip("\n")
        closing = lines[-1]
        inner = lines[1:-1]
        pieces, buf = [], []
        size = len(fence) + len(closing)
        for line in inner:
            if size + len(line) > max_chars and buf:
                pieces.append(fence + "\n" + "".join(buf) + closing)
                buf, size = [], len(fence) + len(closing)
            buf.append(line)
            size += len(line)
        if buf:
            pieces.append(fence + "\n" + "".join(buf) + closing)
        return pieces
    chunks, buf = [], []
    size = 0
    for line in lines:
        if size + len(line) > max_chars and buf:
            chunks.append("".join(buf))
            buf, size = [], 0
        buf.append(line)
        size += len(line)
    if buf:
        chunks.append("".join(buf))
    return chunks


def chunk_doc(text: str, max_chars: int) -> list[str]:
    units = split_units(text)
    chunks: list[str] = []
    buf: list[str] = []
    size = 0
    for unit in units:
        if len(unit) > max_chars:
            if buf:
                chunks.append("".join(buf))
                buf, size = [], 0
            chunks.extend(hard_split(unit, max_chars))
            continue
        if size + len(unit) > max_chars and buf:
            chunks.append("".join(buf))
            buf, size = [], 0
        buf.append(unit)
        size += len(unit)
    if buf:
        chunks.append("".join(buf))
    return [c.strip() + "\n" for c in chunks if c.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default=str(Path.home() / ".agents" / "skills" / "threejs"))
    ap.add_argument("--max-chars", type=int, default=7000)
    ap.add_argument("--branch", default=BRANCH)
    args = ap.parse_args()

    dest = Path(args.dest)
    (dest / "references").mkdir(parents=True, exist_ok=True)

    umbrella = ROOT / "skills" / "threejs" / "SKILL.md"
    if not umbrella.exists():
        print(f"falta {umbrella}", file=sys.stderr)
        return 1
    (dest / "SKILL.md").write_text(umbrella.read_text(encoding="utf-8"), encoding="utf-8")

    repo_info = api(f"https://api.github.com/repos/{REPO}")
    commit = api(f"https://api.github.com/repos/{REPO}/commits/{args.branch}")["sha"][:12]
    license_name = (repo_info.get("license") or {}).get("spdx_id", "?")

    total = 0
    for topic in TOPICS:
        raw = f"https://raw.githubusercontent.com/{REPO}/{args.branch}/skills/{topic}/SKILL.md"
        try:
            text = fetch(raw).decode("utf-8")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR {topic}: {exc}", file=sys.stderr)
            continue
        body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S).strip() + "\n"
        chunks = chunk_doc(body, args.max_chars)
        short = topic.removeprefix("threejs-")
        for i, chunk in enumerate(chunks, 1):
            header = (
                f"<!-- Fuente: {REPO}/skills/{topic} (MIT); parte {i}/{len(chunks)}; "
                f"adaptado a DSH -->\n\n"
            )
            out = dest / "references" / f"{short}-{i}.md"
            out.write_text(header + chunk, encoding="utf-8")
            total += 1
        print(f"{topic}: {len(chunks)} trozos")

    source = (
        f"# Fuente\n\n"
        f"- Repo: https://github.com/{REPO}\n"
        f"- Rama: {args.branch} @ {commit}\n"
        f"- Licencia: {license_name}\n"
        f"- Instalado: {total} referencias troceadas (max {args.max_chars} chars)\n"
        f"- Adaptación: paraguas `SKILL.md` propio; contenido upstream troceado para el\n"
        f"  presupuesto de herramientas de DSH (8 KB).\n"
    )
    (dest / "references" / "SOURCE.md").write_text(source, encoding="utf-8")

    size = len((dest / "SKILL.md").read_text(encoding="utf-8"))
    print(f"\nOK: {dest}")
    print(f"SKILL.md {size} chars · {total} referencias")
    if size > 8192:
        print("AVISO: SKILL.md supera 8192 chars y DSH lo podará", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
