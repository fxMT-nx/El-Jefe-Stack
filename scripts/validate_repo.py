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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"falta el fichero: {rel(path)}")
        return ""
    except UnicodeDecodeError:
        fail(f"{rel(path)} no está en UTF-8 válido")
        return ""
    except OSError as exc:
        fail(f"no se pudo leer {rel(path)}: {exc.strerror or exc}")
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


def check_threejs() -> None:
    path = ROOT / "skills" / "threejs" / "SKILL.md"
    text = read(path)
    if not text:
        return
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("skills/threejs/SKILL.md sin frontmatter")
    else:
        try:
            import yaml

            fm = yaml.safe_load(m.group(1))
        except Exception as exc:  # noqa: BLE001
            fail(f"frontmatter de threejs inválido: {exc}")
            fm = {}
        if fm.get("name") != "threejs":
            fail("skills/threejs/SKILL.md debe declarar name: threejs")
    if len(text) > 8192:
        fail(f"skills/threejs/SKILL.md supera 8192 caracteres ({len(text)})")
    if not (ROOT / "scripts" / "install_threejs_skill.py").exists():
        fail("falta scripts/install_threejs_skill.py")


SMOKE_HEADER = """# Triaje de skills y herramientas — smoke

## Mapa fase → skills y herramientas

| Fase | Tarea / entregable | Skills | Herramientas | Evidencia | Estado |
|---|---|---|---|---|---|
"""
SMOKE_WAIVERS = """
## Waivers

| ID | Tarea | Motivo | Alternativa aplicada | Aprueba | Fecha |
|---|---|---|---|---|---|
"""
# (etiqueta, filas de fase, filas de waiver, exit esperado)
SMOKE_CASES: tuple[tuple[str, list[str], list[str], int], ...] = (
    (
        "positivo: skills + herramientas + evidencia",
        ["| F1 | UI | `ui-design` | browseros-neo | capturas | hecho |"],
        [],
        0,
    ),
    (
        "positivo: waiver válido cubre una fase sin skills",
        ["| F1 | Copiar textos (W-01) | no aplica | no aplica | diff revisado | hecho |"],
        ["| W-01 | Copiar textos | mecánico | revisión manual | El Jefe | 2026-11-05 |"],
        0,
    ),
    (
        "B1: skills «no aplica» sin waiver",
        ["| F1 | UI | no aplica | browseros-neo | capturas | hecho |"],
        [],
        1,
    ),
    (
        "B2: herramientas «no aplica» sin waiver",
        ["| F1 | UI | `ui-design` | no aplica | capturas | hecho |"],
        [],
        1,
    ),
    (
        "B3: evidencia vacía",
        ["| F1 | UI | `ui-design` | browseros-neo |  | hecho |"],
        [],
        1,
    ),
    (
        "B3: evidencia «TBD»",
        ["| F1 | UI | `ui-design` | browseros-neo | TBD | hecho |"],
        [],
        1,
    ),
    (
        "B4: waiver citado sin aprobador",
        ["| F1 | Copiar textos (W-01) | no aplica | no aplica | diff revisado | hecho |"],
        ["| W-01 | Copiar textos | mecánico | revisión manual |  | 2026-11-05 |"],
        1,
    ),
    (
        "B4: waiver citado con Fecha vacía",
        ["| F1 | Copiar textos (W-01) | no aplica | no aplica | diff revisado | hecho |"],
        ["| W-01 | Copiar textos | mecánico | revisión manual | El Jefe |  |"],
        1,
    ),
    (
        "B6: evidencia «no aplica»",
        ["| F1 | UI | `ui-design` | browseros-neo | no aplica | hecho |"],
        [],
        1,
    ),
    (
        "B7: waiver citado sin motivo",
        ["| F1 | Copiar textos (W-01) | no aplica | no aplica | diff revisado | hecho |"],
        ["| W-01 | Copiar textos |  | revisión manual | El Jefe | 2026-11-05 |"],
        1,
    ),
)


def smoke_registry(phases: list[str], waivers: list[str]) -> str:
    return SMOKE_HEADER + "\n".join(phases) + "\n" + SMOKE_WAIVERS + "\n".join(waivers) + "\n"


def check_skills_protocol() -> None:
    """Ficheros del triaje obligatorio + smoke test de skills_check.py (positivos y B1–B7)."""
    skill_dir = ROOT / "skills" / "el-jefe-team"
    reference = skill_dir / "references" / "triaje-skills.md"
    script = ROOT / "scripts" / "skills_check.py"
    template = ROOT / "templates" / "skills-plan.md"
    for required in (reference, script, template):
        if not required.exists():
            fail(f"falta el fichero del triaje: {required.relative_to(ROOT)}")
    if reference.exists() and "T-R-I-A-J-E" not in read(reference):
        fail("triaje-skills.md no contiene el protocolo T-R-I-A-J-E")
    if not script.exists() or not template.exists():
        return

    import subprocess
    import tempfile

    def run(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )

    try:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            init = run("--init", str(base))
            if init.returncode != 0:
                fail(f"skills_check --init falla: {(init.stderr or init.stdout).strip()[:400]}")
                return
            if not (base / "docs" / "memoria" / "40-skills.md").exists():
                fail("skills_check --init no creó docs/memoria/40-skills.md")
                return
            seed = run(str(base))
            if seed.returncode != 0:
                fail(f"skills_check no valida un registro recién creado: {(seed.stdout or seed.stderr).strip()[:400]}")
                return

            for index, (label, phases, waivers, expected) in enumerate(SMOKE_CASES, 1):
                case = base / f"caso{index}"
                (case / "docs" / "memoria").mkdir(parents=True, exist_ok=True)
                (case / "docs" / "memoria" / "40-skills.md").write_text(
                    smoke_registry(phases, waivers), encoding="utf-8"
                )
                result = run(str(case))
                if result.returncode != expected:
                    detail = " | ".join((result.stdout or result.stderr).strip().splitlines())[:300]
                    fail(f"smoke «{label}»: esperaba exit {expected}, dio {result.returncode} ({detail})")

            broken = base / "utf8"
            (broken / "docs" / "memoria").mkdir(parents=True, exist_ok=True)
            (broken / "docs" / "memoria" / "40-skills.md").write_bytes(b"# Triaje " + bytes([0xFF, 0xFE]))
            result = run(str(broken))
            if result.returncode != 1 or "Traceback" in (result.stderr or ""):
                fail("skills_check no informa limpio (exit 1, sin traceback) un registro con UTF-8 inválido")
    except (OSError, subprocess.SubprocessError) as exc:
        fail(f"smoke test de skills_check falló: {exc}")


def check_skills_reference_links() -> None:
    skill_dir = ROOT / "skills" / "el-jefe-team"
    text = read(skill_dir / "SKILL.md")
    for name in ("triaje-skills.md", "skills-seleccion.md", "40-skills.md"):
        if name not in text:
            fail(f"SKILL.md no menciona {name}")


def main() -> int:
    try:  # misma convención de salida que skills_check y memory_check: UTF-8
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # consolas muy antiguas
        pass
    check_preset()
    check_skill()
    check_threejs()
    check_scripts()
    check_skills_protocol()
    check_skills_reference_links()
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
