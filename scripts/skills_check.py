#!/usr/bin/env python3
"""Triaje obligatorio de skills: valida, inicializa o inventaría su registro.

Uso:
    python scripts/skills_check.py <proyecto>
    python scripts/skills_check.py --project <proyecto>
    python scripts/skills_check.py --init <proyecto> [--force]
    python scripts/skills_check.py --inventory [--root DIR] [--json]

Sin dependencias externas (solo biblioteca estándar).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REGISTRY = "docs/memoria/40-skills.md"
TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "skills-plan.md"
DEFAULT_SKILLS_DIR = Path.home() / ".agents" / "skills"
MAX_DESC = 160
PLACEHOLDERS = {"tbd", "pendiente", "todo", "por hacer", "por definir", "xxx", "???"}
NO_APLICA = {"no aplica", "n/a", "na", "ninguna", "ninguno"}
WAIVER_RE = re.compile(r"\bW-\d+\b", re.I)
FALLBACK_TEMPLATE = """# Triaje de skills y herramientas — {project}

> Actualizado: {today} · Responsable: El Jefe

## Mapa fase → skills y herramientas

| Fase | Tarea / entregable | Skills | Herramientas | Evidencia | Estado |
|---|---|---|---|---|---|

## Waivers

| ID | Tarea | Motivo | Alternativa aplicada | Aprueba | Fecha |
|---|---|---|---|---|---|

## Huecos y propuestas

- (ninguno)
"""


class ReadError(Exception):
    """Error de lectura que se reporta con un mensaje, nunca con un traceback."""


def read(path: Path) -> str:
    """Lee UTF-8; falla con ReadError (no OSError/UnicodeDecodeError) para poder informar limpio."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ReadError(f"{path.name} no está en UTF-8 válido; vuelve a guardarlo en UTF-8") from None
    except FileNotFoundError:
        raise ReadError(f"no existe {path.name}") from None
    except OSError as exc:
        raise ReadError(f"no se pudo leer {path.name}: {exc.strerror or exc}") from None


def clean(cell: str) -> str:
    return cell.strip().strip("`*_ ").strip()


def is_separator(line: str) -> bool:
    s = line.strip()
    if "|" not in s or "-" not in s:
        return False
    return set(s) <= set("|-: \t")


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [cell.strip() for cell in s.split("|")]


def parse_tables(text: str) -> list[dict]:
    """Tablas markdown del texto, ignorando bloques de código."""
    lines = text.splitlines()
    tables: list[dict] = []
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("```") or line.startswith("~~~"):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            i += 1
            continue
        if "|" in line and i + 1 < len(lines) and is_separator(lines[i + 1]):
            header = split_row(line)
            rows: list[list[str]] = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            tables.append({"header": header, "rows": rows})
            i = j
            continue
        i += 1
    return tables


def norm(cell: str) -> str:
    return clean(cell).casefold()


def find_column(header: list[str], words: tuple[str, ...]) -> int | None:
    for idx, cell in enumerate(header):
        low = norm(cell)
        if any(word in low for word in words):
            return idx
    return None


def cell_at(cells: list[str], index: int | None) -> str:
    if index is None or index >= len(cells):
        return ""
    return clean(cells[index])


def is_waiver_table(header: list[str]) -> bool:
    low = [norm(cell) for cell in header]
    return any("motivo" in c or "alternativa" in c or "aprueba" in c for c in low)


def parse_waivers(header: list[str], rows: list[list[str]]) -> tuple[dict[str, dict[str, str]], list[str]]:
    cols = {
        "motivo": find_column(header, ("motivo", "razón", "razon")),
        "alternativa": find_column(header, ("alternativa",)),
        "aprueba": find_column(header, ("aprueba", "aprob")),
        "fecha": find_column(header, ("fecha",)),
    }
    waivers: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for row in rows:
        match = WAIVER_RE.search(" | ".join(row))
        if not match:
            continue
        wid = match.group(0).upper()
        if wid in waivers:
            duplicates.append(wid)
            continue
        waivers[wid] = {
            "motivo": cell_at(row, cols["motivo"]),
            "alternativa": cell_at(row, cols["alternativa"]),
            "aprueba": cell_at(row, cols["aprueba"]),
            "fecha": cell_at(row, cols["fecha"]),
        }
    return waivers, duplicates


def collect(root: Path) -> dict:
    """Analiza el registro sin imprimir: {errors, warnings, phases, waivers}."""
    errors: list[str] = []
    warnings: list[str] = []
    report: dict = {"errors": errors, "warnings": warnings, "phases": 0, "waivers": 0}
    path = root / REGISTRY
    try:
        text = read(path)
    except ReadError as exc:
        errors.append(f"falta o no se puede leer {REGISTRY} ({exc}); créalo con --init")
        return report
    if not text.strip():
        errors.append(f"falta {REGISTRY} (créalo con --init)")
        return report

    tables = parse_tables(text)
    phase_tables: list[tuple[dict, int, int, int | None]] = []
    waivers: dict[str, dict[str, str]] = {}
    has_waiver_section = bool(re.search(r"(?im)^#{1,6}\s*waivers?\b", text))
    for table in tables:
        header = table["header"]
        skills_idx = find_column(header, ("skill",))
        tools_idx = find_column(header, ("herramient", "tool", "mcp"))
        if skills_idx is not None and tools_idx is not None:
            evidence_idx = find_column(header, ("evidencia", "evidence"))
            phase_tables.append((table, skills_idx, tools_idx, evidence_idx))
        if is_waiver_table(header):
            has_waiver_section = True
            found, duplicates = parse_waivers(header, table["rows"])
            for wid in dict.fromkeys(duplicates):
                warnings.append(f"waiver {wid} duplicado en la tabla; cuenta la primera fila")
            for wid, data in found.items():
                waivers.setdefault(wid, data)

    if not phase_tables:
        errors.append("no encuentro la tabla de fases (columnas Fase + Skills + Herramientas)")
    if not has_waiver_section:
        warnings.append("no hay sección de waivers (obligatoria aunque esté vacía)")

    total_rows = 0
    cited_any: set[str] = set()
    for table, skills_idx, tools_idx, evidence_idx in phase_tables:
        rows = [row for row in table["rows"] if any(clean(cell) for cell in row)]
        if rows and evidence_idx is None:
            errors.append("la tabla de fases no tiene columna 'Evidencia'")
        for row in rows:
            total_rows += 1
            cells = row + [""] * (max(len(table["header"]), len(row)) - len(row))
            fase = clean(cells[0]) or f"fila {total_rows}"
            row_text = " | ".join(cells)
            cited = {match.group(0).upper() for match in WAIVER_RE.finditer(row_text)}
            cited_any |= cited
            for waiver in sorted(cited - set(waivers)):
                errors.append(f"{fase}: cita el waiver {waiver}, que no existe en la tabla de waivers")
            covered = bool(cited & set(waivers))
            skills = cell_at(cells, skills_idx)
            tools = cell_at(cells, tools_idx)
            evidence = cell_at(cells, evidence_idx)

            for label, value, index in (
                ("skills", skills, skills_idx),
                ("herramientas", tools, tools_idx),
                ("evidencia", evidence, evidence_idx),
            ):
                if norm(value) in PLACEHOLDERS:
                    col = clean(table["header"][index]) if index is not None and index < len(table["header"]) else label
                    errors.append(f"{fase}: '{col}' sigue con marcador «{value}»")

            if not evidence and evidence_idx is not None:
                errors.append(f"{fase}: sin evidencia (la ley exige evidencia real por fase)")
            if not covered:
                if not skills:
                    errors.append(f"{fase}: sin skills y sin waiver que la cubra")
                if not tools:
                    errors.append(f"{fase}: sin herramientas y sin waiver que la cubra")
                if norm(skills) in NO_APLICA:
                    errors.append(f"{fase}: skills «{skills}» sin waiver aprobado que la cubra")
                if norm(tools) in NO_APLICA:
                    errors.append(f"{fase}: herramientas «{tools}» sin waiver aprobado que la cubra")

    for wid, data in sorted(waivers.items()):
        if wid not in cited_any:
            warnings.append(f"waiver {wid} definido y no usado por ninguna fase")
            continue
        if not data["aprueba"] or norm(data["aprueba"]) in PLACEHOLDERS:
            errors.append(f"waiver {wid}: 'Aprueba' vacío; la ley exige aprobación de El Jefe")
        if not data["fecha"] or norm(data["fecha"]) in PLACEHOLDERS:
            errors.append(f"waiver {wid}: 'Fecha' vacía")

    if total_rows == 0:
        warnings.append("sin fases registradas todavía; añade una fila por fase antes de empezar")

    report["phases"] = total_rows
    report["waivers"] = len(waivers)
    return report


def validate(root: Path) -> int:
    print(f"Triaje de skills — {root.name}")
    report = collect(root)
    for warning in report["warnings"]:
        print(f"  aviso: {warning}")
    if report["errors"]:
        for error in report["errors"]:
            print(f"  ERROR: {error}")
        return 1
    print(f"  OK — {report['phases']} fases, {report['waivers']} waivers")
    return 0


def init_registry(root: Path, force: bool = False) -> int:
    target = root / REGISTRY
    if target.exists() and not force:
        print(f"ya existe {REGISTRY} (usa --force para sobrescribir)")
        return 0
    try:
        template = read(TEMPLATE)
    except ReadError as exc:
        print(f"aviso: no se pudo leer la plantilla ({exc}); uso la plantilla interna", file=sys.stderr)
        template = FALLBACK_TEMPLATE
    if not template.strip():
        template = FALLBACK_TEMPLATE
    content = template.replace("{project}", root.name).replace("{today}", date.today().isoformat())
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    except OSError as exc:
        print(f"no se pudo crear {REGISTRY}: {exc.strerror or exc}", file=sys.stderr)
        return 2
    print(f"creado {REGISTRY}")
    return 0


def parse_frontmatter(text: str) -> dict[str, str]:
    text = text.lstrip("\ufeff")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}
    data: dict[str, object] = {}
    block: str | None = None
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^[A-Za-z0-9_.-]+\s*:", raw):
            key, _, value = raw.partition(":")
            key = key.strip()
            value = value.strip()
            if value in (">", "|", ">-", "|-", ">+", "|+"):
                data[key] = []
                block = key
            else:
                data[key] = value.strip("'\"")
                block = None
        elif block and (raw.startswith("  ") or raw.startswith("\t")):
            assert isinstance(data[block], list)
            data[block].append(raw.strip())
        else:
            block = None
    result: dict[str, str] = {}
    for key, value in data.items():
        if isinstance(value, list):
            result[key] = " ".join(part for part in value if part)
        else:
            result[key] = str(value)
    return result


def inventory(root: Path, as_json: bool = False) -> int:
    if not root.exists() or not root.is_dir():
        print(f"no existe el directorio de skills: {root}", file=sys.stderr)
        return 2
    skills = []
    unreadable: list[str] = []
    for skill_file in sorted(root.glob("*/SKILL.md")):
        try:
            text = read(skill_file)
        except ReadError as exc:
            unreadable.append(f"{skill_file.parent.name}: {exc}")
            continue
        front = parse_frontmatter(text)
        name = front.get("name") or skill_file.parent.name
        description = " ".join(front.get("description", "").split())
        if len(description) > MAX_DESC:
            description = description[: MAX_DESC - 3].rstrip() + "..."
        skills.append(
            {
                "name": name,
                "description": description or "(sin description)",
                "dir": skill_file.parent.name,
                "path": str(skill_file),
            }
        )
    skills.sort(key=lambda item: item["name"].casefold())

    if as_json:
        print(json.dumps(skills, ensure_ascii=False, indent=2))
    else:
        print(f"Skills instaladas en {root} ({len(skills)})")
        for skill in skills:
            print(f"- {skill['name']} — {skill['description']}")
    if unreadable:
        for item in unreadable:
            print(f"error: SKILL.md ilegible — {item}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Valida, inicializa o inventaría el triaje obligatorio de skills y herramientas."
    )
    parser.add_argument("path", nargs="?", help="raíz del proyecto")
    parser.add_argument("--project", help="raíz del proyecto (alternativa al argumento posicional)")
    parser.add_argument("--init", action="store_true", help=f"crea {REGISTRY} desde la plantilla")
    parser.add_argument("--force", action="store_true", help="con --init, sobrescribe el registro")
    parser.add_argument("--inventory", action="store_true", help="lista las skills instaladas")
    parser.add_argument("--root", help="directorio de skills para --inventory (por defecto ~/.agents/skills)")
    parser.add_argument("--json", action="store_true", help="salida JSON para --inventory")
    return parser


def run(args: argparse.Namespace) -> int:
    if args.inventory:
        return inventory(Path(args.root).expanduser().resolve() if args.root else DEFAULT_SKILLS_DIR, args.json)

    if args.path and args.project:
        print("indica el proyecto como argumento o con --project, no ambos", file=sys.stderr)
        return 2
    project = args.project or args.path
    if not project:
        build_parser().print_usage(sys.stderr)
        return 2
    root = Path(project).expanduser().resolve()
    if not root.exists():
        print(f"no existe la ruta: {root}", file=sys.stderr)
        return 2
    if args.init:
        return init_registry(root, args.force)
    return validate(root)


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # consolas muy antiguas
        pass

    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except ReadError as exc:  # red de seguridad: nunca un traceback por un fichero ilegible
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
