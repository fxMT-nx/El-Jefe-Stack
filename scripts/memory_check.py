#!/usr/bin/env python3
"""Valida (o inicializa) la memoria viva de un proyecto de El Jefe.

Uso:
    python scripts/memory_check.py <ruta-proyecto>
    python scripts/memory_check.py <ruta-proyecto> --init
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

CORE = [
    "docs/estado.md",
    "docs/memoria/00-indice.md",
    "docs/memoria/10-proyecto.md",
    "docs/memoria/20-usuario.md",
    "docs/memoria/60-tareas.md",
    "docs/memoria/80-preguntas.md",
    "docs/memoria/90-historial.md",
]
OPTIONAL = [
    "docs/memoria/30-decisiones.md",
    "docs/memoria/50-tecnico.md",
    "docs/memoria/70-riesgos.md",
    "docs/adr",
    "docs/trabajo.md",
    "docs/ideas.md",
    "GLOSSARY.md",
]
SKILLS_REGISTRY = "docs/memoria/40-skills.md"
SECRET_RE = re.compile(
    r"(?i)\b(api[_-]?key|secret|password|passwd|token|bearer)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-\.]{12,}"
)
LINK_RE = re.compile(r"\]\(([^)#][^)]+)\)")
SNAPSHOT_LIMIT = 1600
ESTADO_LIMIT = 6000
STALE_DAYS = 45

TEMPLATES = {
    "docs/estado.md": """# Estado — {name}
> Actualizado: {today} · Sesión: — · Fase: inicio

## Objetivo

## Hecho

## En curso

## Siguiente paso

## Decisiones vigentes

## Riesgos / bloqueos

## Preguntas abiertas

## Cómo retomar
""",
    "docs/memoria/00-indice.md": """# Índice de memoria — {name}

> Actualizado: {today}

Orden de lectura al retomar: `docs/estado.md` → este índice → `10-proyecto.md` → `20-usuario.md` → `80-preguntas.md` → última entrada de `90-historial.md`.

| Fichero | Contenido | Última actualización |
|---|---|---|
| `../estado.md` | snapshot y dashboard | {today} |
| `10-proyecto.md` | objetivo y alcance | {today} |
| `20-usuario.md` | preferencias, vetos y decisiones del usuario | {today} |
| `30-decisiones.md` | registro de decisiones | {today} |
| `40-skills.md` | triaje de skills y herramientas | {today} |
| `50-tecnico.md` | stack, comandos, trampas | {today} |
| `60-tareas.md` | hecho / en curso / siguiente | {today} |
| `70-riesgos.md` | riesgos y bloqueos | {today} |
| `80-preguntas.md` | preguntas abiertas | {today} |
| `90-historial.md` | sesiones y cómo retomar | {today} |
""",
    "docs/memoria/10-proyecto.md": """# Proyecto — {name}

> Actualizado: {today}

## Objetivo

## Alcance

## No-objetivos

## Usuarios

## Criterios de éxito
""",
    "docs/memoria/20-usuario.md": """# El usuario — {name}

> Actualizado: {today}

Aquí va **lo del usuario**, no las decisiones técnicas: preferencias, requisitos, vetos, aprobaciones y contexto relevante.

## Preferencias
- Idioma:
- Tono:
- Stack que quiere:
- Stack que veta:

## Cosas que no se tocan

## Aprobaciones dadas
| Fecha | Acción aprobada | Alcance | Quién |
|---|---|---|---|

## Decisiones que solo puede tomar el usuario
""",
    "docs/memoria/60-tareas.md": """# Tareas — {name}

> Actualizado: {today}

## Hecho
- [ ]

## En curso
- [ ] (dueño: )

## Siguiente
- [ ]

## Enlaces al tablero
""",
    "docs/memoria/80-preguntas.md": """# Preguntas abiertas — {name}

> Actualizado: {today}

| Pregunta | Por qué importa | Estado | Respuesta |
|---|---|---|---|
""",
    "docs/memoria/90-historial.md": """# Historial de sesiones — {name}

## {today} — sesión inicial

- **Objetivo:**
- **Hecho:**
- **Decisiones:**
- **Archivos tocados:**
- **Siguiente paso:**
- **Preguntas abiertas:**
""",
}


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def init_memory(root: Path) -> None:
    today = date.today().isoformat()
    for rel, tpl in TEMPLATES.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(tpl.format(name=root.name, today=today), encoding="utf-8")
            print(f"creado {rel}")
    init_skills_registry(root)
    print("memoria inicializada")


def init_skills_registry(root: Path) -> None:
    """Crea docs/memoria/40-skills.md delegando en skills_check (hermano)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import skills_check  # noqa: PLC0415 - script hermano del mismo repo

        skills_check.init_registry(root)
        return
    except ImportError:
        pass
    target = root / "docs/memoria/40-skills.md"
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "# Triaje de skills y herramientas — "
        + root.name
        + f"\n\n> Actualizado: {date.today().isoformat()} · Responsable: El Jefe\n\n"
        "## Mapa fase → skills y herramientas\n\n"
        "| Fase | Tarea / entregable | Skills | Herramientas | Evidencia | Estado |\n"
        "|---|---|---|---|---|---|\n\n"
        "## Waivers\n\n"
        "| ID | Tarea | Motivo | Alternativa aplicada | Aprueba | Fecha |\n"
        "|---|---|---|---|---|---|\n\n"
        "## Huecos y propuestas\n\n- (ninguno)\n",
        encoding="utf-8",
    )
    print("creado docs/memoria/40-skills.md (esqueleto mínimo)")


def check_skills_registry(root: Path, errors: list[str], warnings: list[str]) -> None:
    """40-skills.md: obligatorio si hay estado.md; sus filas se validan con skills_check."""
    registry = root / SKILLS_REGISTRY
    if not registry.exists():
        if (root / "docs/estado.md").exists():
            warnings.append(
                f"{SKILLS_REGISTRY} ausente: el triaje de skills es obligatorio "
                "(créalo con `python scripts/skills_check.py --init .`)"
            )
        return
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import skills_check  # noqa: PLC0415 - script hermano del mismo repo
    except ImportError:
        warnings.append(f"no se pudo validar {SKILLS_REGISTRY}: falta scripts/skills_check.py")
        return
    try:
        report = skills_check.collect(root)
    except skills_check.ReadError as exc:
        errors.append(f"{SKILLS_REGISTRY}: {exc}")
        return
    for error in report["errors"]:
        errors.append(f"{SKILLS_REGISTRY}: {error}")
    for warning in report["warnings"]:
        warnings.append(f"{SKILLS_REGISTRY}: {warning}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="raíz del proyecto")
    ap.add_argument("--init", action="store_true", help="crea el esqueleto si falta")
    args = ap.parse_args()
    root = Path(args.path).resolve()
    if not root.exists():
        print(f"no existe: {root}", file=sys.stderr)
        return 2

    if args.init:
        init_memory(root)

    errors: list[str] = []
    warnings: list[str] = []

    for rel in CORE:
        if not (root / rel).exists():
            errors.append(f"falta {rel}")
    for rel in OPTIONAL:
        if not (root / rel).exists():
            warnings.append(f"opcional ausente: {rel}")

    estado_path = root / "docs/estado.md"
    if estado_path.exists():
        text = read(estado_path)
        if len(text) > ESTADO_LIMIT:
            errors.append(f"docs/estado.md demasiado largo ({len(text)} > {ESTADO_LIMIT}): mueve detalle a memoria/")
        if not re.search(r"(?im)^>\s*Actualizado:", text):
            errors.append("docs/estado.md sin línea '> Actualizado:'")
        m = re.search(r"(?im)^>\s*Actualizado:\s*(\d{4}-\d{2}-\d{2})", text)
        if m:
            try:
                age = (date.today() - date.fromisoformat(m.group(1))).days
                if age > STALE_DAYS:
                    warnings.append(f"estado.md actualizado hace {age} días")
            except ValueError:
                warnings.append("fecha de actualización inválida")
        snapshot = text.split("## Hecho", 1)[0]
        if len(snapshot) > SNAPSHOT_LIMIT:
            warnings.append(f"snapshot inicial > {SNAPSHOT_LIMIT} chars ({len(snapshot)})")

    check_skills_registry(root, errors, warnings)

    for md in root.glob("docs/**/*.md") if (root / "docs").exists() else []:
        text = read(md)
        if SECRET_RE.search(text):
            errors.append(f"posible secreto en {md.relative_to(root)}")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (md.parent / clean).resolve().exists():
                warnings.append(f"enlace roto en {md.relative_to(root)}: {target}")

    print(f"Memoria de {root.name}")
    for w in warnings:
        print(f"  aviso: {w}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        return 1
    print("  OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
