#!/usr/bin/env python3
"""Valida el repo El Jefe Stack: YAML del preset, frontmatter de la skill y enlaces.

Sin dependencias más allá de PyYAML. Pensado para correr en CI y en local:
    python scripts/validate_repo.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"falta el fichero: {path.relative_to(ROOT)}")
        return ""


def check_preset() -> None:
    path = ROOT / "preset" / "el-jefe.patch.yml"
    text = read(path)
    if not text:
        return
    try:
        import yaml
    except ImportError:
        fail("PyYAML no está instalado (pip install pyyaml)")
        return

    # Los patches de DSH usan la etiqueta !!js; para validar YAML la tratamos
    # como texto en lugar de intentar construirla.
    yaml.SafeLoader.add_constructor(
        "tag:yaml.org,2002:js",
        lambda loader, node: loader.construct_scalar(node),
    )

    docs = list(yaml.safe_load_all(text))
    entries = [entry for doc in docs if doc for entry in doc]
    target = [e for e in entries if isinstance(e, dict) and e.get("id") == "preset-standard"]
    if not target:
        fail("el preset no contiene una entrada con id 'preset-standard'")
        return
    cfg = target[0].get("config") or {}
    if cfg.get("id") != "standard":
        fail("el override debe conservar config.id = 'standard'")
    plugins = cfg.get("plugins") or []
    ids = {p.get("id") for p in plugins if isinstance(p, dict)}
    for required in {"persona", "agent-instructions", "tool-fs", "tool-web", "skill-filesystem"}:
        if required not in ids:
            fail(f"al preset le falta el plugin '{required}'")
    persona = next((p for p in plugins if isinstance(p, dict) and p.get("id") == "persona"), {})
    prefix = ((persona.get("config") or {}).get("prefix") or "")
    if "Eres El Jefe" not in prefix:
        fail("la persona no contiene 'Eres El Jefe'")
    if "Fase 0" not in prefix:
        fail("la persona no menciona la fase 0")

    # el ejemplo MCP debe ser YAML válido también
    mcp = ROOT / "preset" / "mcp-browseros.example.yml"
    if mcp.exists():
        try:
            list(yaml.safe_load_all(read(mcp)))
        except yaml.YAMLError as exc:
            fail(f"YAML inválido en {mcp.relative_to(ROOT)}: {exc}")


def check_skill() -> None:
    skill_dir = ROOT / "skills" / "el-jefe-team"
    path = skill_dir / "SKILL.md"
    text = read(path)
    if not text:
        return
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("SKILL.md sin frontmatter YAML")
        return
    try:
        import yaml

        fm = yaml.safe_load(m.group(1))
    except Exception as exc:  # noqa: BLE001 - queremos el mensaje para CI
        fail(f"frontmatter inválido: {exc}")
        return
    if fm.get("name") != "el-jefe-team":
        fail("frontmatter.name debe ser 'el-jefe-team'")
    if not fm.get("description"):
        fail("frontmatter.description vacío")
    if len(text) > 8192:
        fail(f"SKILL.md supera 8192 caracteres ({len(text)}); DSH lo podará al cargarlo")

    refs = sorted((skill_dir / "references").glob("*.md"))
    if len(refs) < 10:
        fail(f"pocas fichas de referencia: {len(refs)}")
    for ref in refs:
        if not read(ref).strip():
            fail(f"referencia vacía: {ref.relative_to(ROOT)}")

    for link in sorted(set(re.findall(r"`(references/[a-z0-9\-]+\.md)`", text))):
        if not (skill_dir / link).exists():
            fail(f"SKILL.md enlaza {link} pero no existe")


def check_relative_links() -> None:
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = read(md)
        for target in re.findall(r"\]\(([^)#][^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            if not (md.parent / clean).resolve().exists():
                fail(f"enlace roto en {md.relative_to(ROOT)}: {target}")


def check_scripts() -> None:
    import py_compile

    scripts = sorted((ROOT / "scripts").glob("*.py"))
    if not scripts:
        fail("no hay scripts Python en scripts/")
    for path in scripts:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(f"script no compila: {path.relative_to(ROOT)}: {exc.msg}")
    if not (ROOT / "scripts" / "skill_router.py").exists():
        fail("falta scripts/skill_router.py")


def main() -> int:
    check_preset()
    check_skill()
    check_scripts()
    check_relative_links()
    if errors:
        print("El Jefe Stack: validación FALLIDA")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("El Jefe Stack: validación OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
