#!/usr/bin/env python3
"""Empaqueta skills largas: trocea el SKILL.md y deja un índice navegable.

El pruner de sesión recorta los resultados de herramienta a 8.192 caracteres, así
que una skill que pase de ahí llega al agente a medias: el `skill` tool devuelve
el principio y el agente nunca ve las reglas del medio. Este script parte el
cuerpo por encabezados `##` en `references/parte-NN-<slug>.md` (≤7.000 caracteres
cada uno), deja en `SKILL.md` (≤8.192) el frontmatter, la intro, las reglas
imprescindibles y un índice con enlaces relativos, y conserva el original en
`references/00-original.md` para trazabilidad.

Cada carácter del original acaba exactamente en un sitio: o inline en el
`SKILL.md` o en una sola parte. El script lo comprueba antes de escribir.

Uso:
    python scripts/skill_pack.py --audit [--root DIR]
    python scripts/skill_pack.py --split <skill> [--root DIR] [--keep-original false]
                                  [--inline "Encabezado"]...
    python scripts/skill_pack.py --split-all [--root DIR] [--dry-run]
    python scripts/skill_pack.py --verify [--root DIR]

Sin dependencias externas (solo biblioteca estándar). Mensajes en español, UTF-8.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

MAX_SKILL = 8192          # límite del pruner de DSH: lo que pase de aquí se recorta
MAX_PARTE = 7000          # tamaño máximo de cada trozo
HEADER_MARGIN = 200       # hueco para la cabecera de trazabilidad de cada trozo
INTRO_MAX = 1500          # la intro se queda entera hasta aquí; el resto se trocea
INLINE_SINGLE_MAX = 4200  # una sección mayor no se queda inline: se trocea
HINT_MAX = 70             # caracteres de pista por entrada del índice
DEFAULT_ROOT = Path.home() / ".agents" / "skills"
LINK_RE = re.compile(r"(!?\[[^\]]*\]\()\s*<?([^)\s>]+)>?\s*(\))")
DEF_RE = re.compile(r"(?m)^(\s*\[[^\]]+\]:\s*)(\S+)")


# ── lectura/escritura y utilidades de texto ────────────────────────────────────

class PackError(Exception):
    """Error de empaquetado que se informa con un mensaje, nunca con traceback."""


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise PackError(f"no existe {path}") from None
    except UnicodeDecodeError:
        raise PackError(f"{path} no está en UTF-8 válido; vuelve a guardarlo en UTF-8") from None
    except OSError as exc:
        raise PackError(f"no se pudo leer {path}: {exc.strerror or exc}") from None


def write(path: Path, text: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise PackError(f"no se pudo escribir {path}: {exc.strerror or exc}") from None


def clean_md(text: str) -> str:
    """Quita marcas markdown mínimas para usar un título o una línea como etiqueta."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"[*_>#]", "", text)
    return " ".join(text.split()).strip()


def slug(text: str, limit: int = 40) -> str:
    """Slug ASCII estable: sin acentos, minúsculas y guiones."""
    normalised = unicodedata.normalize("NFKD", text)
    ascii_text = normalised.encode("ascii", "ignore").decode("ascii").lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return (ascii_text[:limit].rstrip("-") or "seccion")


def split_frontmatter(text: str) -> tuple[str, str]:
    """Devuelve (frontmatter con sus `---`, cuerpo). Sin frontmatter: ('', texto)."""
    text = text.lstrip("\ufeff")
    match = re.match(r"(---\s*\n.*?\n---\s*\n)", text, re.S)
    if not match:
        return "", text
    return match.group(1), text[match.end():]


def toggle_fence(line: str, state: bool) -> bool:
    stripped = line.lstrip()
    if stripped.startswith("```") or stripped.startswith("~~~"):
        return not state
    return state


def level_of(line: str, in_fence: bool) -> int:
    """Nivel de encabezado markdown de la línea, o 0. Ignora lo que hay en fences."""
    if in_fence:
        return 0
    match = re.match(r"^(#{1,6})\s+\S", line)
    return len(match.group(1)) if match else 0


# ── modelo de secciones ────────────────────────────────────────────────────────

@dataclass
class Section:
    heading: str  # línea `## …` con su salto de línea
    body: str     # texto hasta la siguiente sección

    @property
    def raw(self) -> str:
        return self.heading + self.body

    @property
    def title(self) -> str:
        return clean_md(self.heading.strip().lstrip("#").strip())

    @property
    def hint(self) -> str:
        """Primera frase del cuerpo, para el índice: salta cabeceras y filas de tabla."""
        short: list[str] = []
        for line in self.body.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "<!--", "|", ">", "```", "~~~")):
                continue
            if stripped.endswith("|") or stripped.count("|") >= 2:  # fila de tabla
                continue
            stripped = clean_md(re.sub(r"^[-*]\s+|^\d+[.)]\s+", "", stripped))
            if len(stripped) >= 30:
                return stripped[:HINT_MAX] + ("…" if len(stripped) > HINT_MAX else "")
            if stripped:
                short.append(stripped)
        return (short[0][:HINT_MAX] if short else "")


def parse_sections(body: str) -> tuple[str, list[Section]]:
    """Separa intro y secciones `##`, respetando los bloques de código."""
    intro: list[str] = []
    sections: list[Section] = []
    current: Section | None = None
    fence = False
    for line in body.splitlines(keepends=True):
        in_fence = fence
        fence = toggle_fence(line, fence)
        if level_of(line, in_fence) == 2:
            if current is not None:
                sections.append(current)
            current = Section(heading=line, body="")
            continue
        if current is None:
            intro.append(line)
        else:
            current.body += line
    if current is not None:
        sections.append(current)
    return "".join(intro), sections


def split_units(text: str) -> list[str]:
    """Unidades troceables de un texto: sus `###` y, si no hay, sus párrafos."""
    lines = text.splitlines(keepends=True)
    fence = False
    has_sub = False
    for line in lines:
        in_fence = fence
        fence = toggle_fence(line, fence)
        if level_of(line, in_fence) == 3:
            has_sub = True
            break
    key_level = 3 if has_sub else 0
    units: list[str] = []
    current: list[str] = []
    fence = False
    for line in lines:
        in_fence = fence
        fence = toggle_fence(line, fence)
        boundary = False
        if key_level == 3:
            boundary = level_of(line, in_fence) == 3
        else:
            boundary = not in_fence and not line.strip() and bool(current)
        if boundary and current:
            units.append("".join(current))
            current = []
        current.append(line)
    if current:
        units.append("".join(current))
    return [unit for unit in units if unit]


def hard_split(text: str, limit: int) -> list[str]:
    """Último recurso: corta por líneas completas (nunca por la mitad de una línea)."""
    pieces: list[str] = []
    current = ""
    for line in text.splitlines(keepends=True):
        while len(line) > limit:
            if current:
                pieces.append(current)
                current = ""
            pieces.append(line[:limit])
            line = line[limit:]
        if len(current) + len(line) > limit:
            if current:
                pieces.append(current)
            current = line
        else:
            current += line
    if current:
        pieces.append(current)
    return [piece for piece in pieces if piece]


def chunk_section(section: Section, limit: int) -> list[str]:
    """Trocea una sección en piezas ≤limit, sin solapar y sin perder texto.

    La primera pieza empieza por el encabezado `##`; las siguientes continúan el
    cuerpo justo donde se cortó. La unión de las piezas es exactamente `section.raw`.
    """
    if len(section.raw) <= limit:
        return [section.raw]
    units = split_units(section.body) or hard_split(section.body, limit)
    expanded: list[str] = []
    for unit in units:  # una unidad mayor que el límite se corta antes de empaquetar
        if len(unit) > limit:
            expanded.extend(hard_split(unit, limit))
        else:
            expanded.append(unit)
    pieces: list[str] = []
    current = section.heading
    for unit in expanded:
        if len(current) + len(unit) > limit and current:
            pieces.append(current)
            current = ""
        current += unit
    if current:
        pieces.append(current)
    return [piece for piece in pieces if piece]


# ── reescritura de enlaces relativos ───────────────────────────────────────────

def relink(text: str, skill_dir: Path, from_sub: str, to_sub: str) -> str:
    """Reescribe enlaces relativos al mover texto entre subcarpetas de la skill.

    Al bajar texto de la raíz a `references/`, sus enlaces `references/x.md`
    dejarían de resolver: se recalculan desde la nueva ubicación. Lo que apunta
    fuera de la skill no se toca.
    """
    if from_sub == to_sub:
        return text
    skill_dir = skill_dir.resolve()
    base_dir = (skill_dir / from_sub).resolve()
    new_dir = (skill_dir / to_sub).resolve()

    def fix(target: str) -> str:
        if not target or target.startswith(("http://", "https://", "mailto:", "#", "/", "data:")):
            return target
        path_part, _, anchor = target.partition("#")
        resolved = (base_dir / path_part).resolve()
        # Se reescribe también lo que apunta fuera de la skill (p. ej. a una skill
        # hermana): desde `references/` hay que subir un nivel más.
        relative = os.path.relpath(resolved, new_dir).replace("\\", "/")
        return relative + (f"#{anchor}" if anchor else "")

    text = LINK_RE.sub(lambda match: f"{match.group(1)}{fix(match.group(2))}{match.group(3)}", text)
    return DEF_RE.sub(lambda match: f"{match.group(1)}{fix(match.group(2))}", text)


# ── construcción del paquete ───────────────────────────────────────────────────

@dataclass
class Part:
    name: str      # parte-01-titulo.md
    title: str     # encabezado original
    label: str     # etiqueta con (i/n) si la sección va en varias piezas
    hint: str
    source: str    # texto original de la pieza, sin comentarios ni relink (para integridad)
    content: str   # lo que se escribe en disco: cabecera + relink


@dataclass
class Package:
    skill: str
    original_chars: int
    final_chars: int = 0
    parts: list[Part] = field(default_factory=list)
    inline: list[str] = field(default_factory=list)
    files: dict[str, str] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)


NOTE = ("<!-- Troceado por scripts/skill_pack.py: cada sección vive en un solo sitio. "
        "Carga solo la parte que necesites. -->\n")

INDEX_HEAD = (
    "## Índice de referencias\n\n"
    "El cuerpo largo vive en `references/` para que no se trunque al cargar la skill "
    f"(el límite son {MAX_SKILL} caracteres). Carga la parte que necesites; no hace falta leerlas todas.\n\n"
    "| Fichero | Contenido |\n|---|---|\n"
)

INLINE_HEAD = "## Reglas clave\n\n"


def _split_intro(intro: str) -> tuple[str, str]:
    """Parte la intro si es enorme, cortando en un salto de párrafo (corte exacto)."""
    if len(intro) <= INTRO_MAX:
        return intro, ""
    cut = intro.rfind("\n\n", 0, INTRO_MAX)
    cut = cut if cut > INTRO_MAX // 2 else INTRO_MAX
    return intro[:cut], intro[cut:]


def _make_parts(sections: list[Section], inline_idx: set[int], skill_dir: Path,
                intro_rest: str) -> list[Part]:
    """Piezas de todas las secciones que no se quedan inline, en orden de documento."""
    parts: list[Part] = []
    number = 0
    if intro_rest.strip():
        number += 1
        name = f"parte-{number:02d}-introduccion.md"
        parts.append(Part(name=name, title="Introducción", label="Introducción",
                          hint=clean_md(intro_rest)[:HINT_MAX] + "…",
                          source=intro_rest,
                          content=(f"<!-- skill: {skill_dir.name} · resto de la introducción -->\n"
                                   + relink(intro_rest, skill_dir, "", "references"))))
    for index, section in enumerate(sections):
        if index in inline_idx:
            continue
        pieces = chunk_section(section, MAX_PARTE - HEADER_MARGIN)
        for position, piece in enumerate(pieces, start=1):
            number += 1
            name = f"parte-{number:02d}-{slug(section.title)}.md"
            label = section.title if len(pieces) == 1 else f"{section.title} ({position}/{len(pieces)})"
            header = (f"<!-- skill: {skill_dir.name} · sección «{section.title}»"
                      + (f" · pieza {position}/{len(pieces)}" if len(pieces) > 1 else "")
                      + " · origen: SKILL.md antes del troceo -->\n")
            parts.append(Part(name=name, title=section.title, label=label,
                              hint=section.hint if position == 1 else "",
                              source=piece,
                              content=header + relink(piece, skill_dir, "", "references")))
    return parts


def build_package(skill_dir: Path, keep_original: bool = True,
                  forced_inline: list[str] | None = None) -> Package:
    """Calcula los ficheros del empaquetado sin escribir nada en disco."""
    skill_dir = skill_dir.resolve()
    text = read(skill_dir / "SKILL.md")
    frontmatter, body = split_frontmatter(text)
    intro, sections = parse_sections(body)
    if not sections:
        raise PackError(f"{skill_dir.name}: no hay secciones `##` que trocear; no se puede empaquetar")

    titles = {section.title.casefold() for section in sections}
    requested = [clean_md(item).casefold() for item in (forced_inline or [])]
    unknown = [item for item in requested if item not in titles]
    if unknown:
        available = "; ".join(section.title for section in sections[:12])
        raise PackError(f"{skill_dir.name}: --inline no encuentra {', '.join(repr(u) for u in unknown)}. "
                        f"Encabezados disponibles: {available}")

    intro_kept, intro_rest = _split_intro(intro)
    mandatory = sorted({0} | {i for i, s in enumerate(sections) if i and s.title.casefold() in requested})
    inline_idx = [i for i in mandatory if len(sections[i].raw) <= INLINE_SINGLE_MAX]
    dropped_big = [sections[i].title for i in mandatory if i not in inline_idx]

    def assemble(chosen: list[int]) -> Package:
        chosen_set = set(chosen)
        parts = _make_parts(sections, chosen_set, skill_dir, intro_rest)
        rows = [f"| `references/{p.name}` | **{p.label}**" + (f" — {p.hint}" if p.hint else "") + " |"
                for p in parts]
        if keep_original:
            rows.append(f"| `references/00-original.md` | Copia íntegra del original "
                        f"({len(text)} caracteres) — trazabilidad; no hace falta cargarla |")
        index = INDEX_HEAD + "\n".join(rows) + "\n"
        inline_text = "".join(sections[i].raw for i in sorted(chosen_set))
        pieces = [frontmatter, intro_kept, NOTE, "\n", INLINE_HEAD,
                  inline_text.strip("\n") + "\n" if inline_text else "", "\n", index]
        content = "".join(pieces)
        package = Package(skill=skill_dir.name, original_chars=len(text), final_chars=len(content),
                          parts=parts, inline=[sections[i].title for i in sorted(chosen_set)])
        package.files["SKILL.md"] = content
        for part in parts:
            package.files[f"references/{part.name}"] = part.content
        if keep_original:
            package.files["references/00-original.md"] = (
                f"<!-- Copia íntegra de SKILL.md antes del troceo ({len(text)} caracteres) · "
                f"{date.today().isoformat()} · generado por scripts/skill_pack.py -->\n" + body)
        return package

    package = assemble(inline_idx)

    # Relleno: mientras quepa, se quedan inline las secciones más cortas en orden
    # de documento (las "reglas cortas imprescindibles" del manual).
    for index in range(len(sections)):
        if index in inline_idx or len(sections[index].raw) > INLINE_SINGLE_MAX:
            continue
        trial = sorted(inline_idx + [index])
        candidate = assemble(trial)
        if candidate.final_chars <= MAX_SKILL:
            inline_idx, package = trial, candidate

    # Presupuesto: si aun así no cabe, van cayendo las inline no obligatorias,
    # de la última a la primera, hasta entrar en el límite.
    droppable = [i for i in inline_idx if i != 0]
    while package.final_chars > MAX_SKILL and droppable:
        inline_idx = [i for i in inline_idx if i != droppable.pop()]
        package = assemble(inline_idx)

    if package.final_chars > MAX_SKILL:
        raise PackError(f"{skill_dir.name}: ni con solo la primera sección cabe en {MAX_SKILL} "
                        f"caracteres (siguen siendo {package.final_chars}); revisa la intro")

    _check_integrity(package, sections, intro, intro_kept, intro_rest)
    if dropped_big:
        package.checks.append(
            f"aviso: {len(dropped_big)} sección(es) pedida(s) inline no cabían solas y quedan troceadas: "
            + ", ".join(dropped_big))
    return package


def _strip(text: str) -> str:
    """Normaliza para comparar: sin comentarios de trazabilidad ni espacios de sobra."""
    text = re.sub(r"(?m)^\s*<!--.*?-->\s*$", "", text)
    return " ".join(text.split())


def _check_integrity(package: Package, sections: list[Section], intro: str,
                     intro_kept: str, intro_rest: str) -> None:
    """Cada sección, exactamente una vez; y el cuerpo reconstruido == el original."""
    inline_set = set(package.inline)
    by_title: dict[str, list[str]] = {}
    for part in package.parts:
        if part.title != "Introducción":
            by_title.setdefault(part.title, []).append(part.source)

    for section in sections:
        found = by_title.get(section.title, [])
        if section.title in inline_set:
            if found:
                package.problems.append(f"«{section.title}» está inline y además troceada")
            continue
        if not found:
            package.problems.append(f"«{section.title}» no aparece en ninguna parte")
            continue
        if _strip("".join(found)) != _strip(section.raw):
            package.problems.append(f"«{section.title}» no se reconstruye igual que el original")
    extra = set(by_title) - {s.title for s in sections}
    if extra:
        package.problems.append(f"trozos de secciones inexistentes: {', '.join(sorted(extra))}")

    rebuilt: list[str] = []
    for section in sections:
        if section.title in inline_set:
            rebuilt.append(section.raw)
        else:
            rebuilt.append("".join(by_title.get(section.title, [])))
    if "".join(rebuilt) != "".join(section.raw for section in sections):
        package.problems.append("la reconstrucción del cuerpo no coincide con el original")
    if intro_kept + intro_rest != intro:
        package.problems.append("la intro no se conserva exacta")

    if not package.problems:
        digest = hashlib.sha256(_strip("".join(s.raw for s in sections)).encode()).hexdigest()[:12]
        package.checks.append(
            f"{len(sections)} secciones: {len(package.inline)} inline + {len(package.parts)} trozos; "
            f"ninguna repetida ni perdida (sha256 del cuerpo {digest})")


# ── comandos ───────────────────────────────────────────────────────────────────

def iter_skills(root: Path) -> list[Path]:
    if not root.exists():
        raise PackError(f"no existe el directorio de skills: {root}")
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def partes_of(skill_dir: Path) -> list[Path]:
    refs = skill_dir / "references"
    return sorted(refs.glob("parte-*.md")) if refs.exists() else []


def audit(root: Path) -> int:
    skills = iter_skills(root)
    rows = []
    for skill_dir in skills:
        size = len(read(skill_dir / "SKILL.md"))
        partes = partes_of(skill_dir)
        rows.append((size, skill_dir.name, len(partes)))
    rows.sort(key=lambda row: (-row[0], row[1]))
    over = [row for row in rows if row[0] > MAX_SKILL]
    split = [row for row in rows if row[2]]
    print(f"Auditoría de skills — {root}")
    print(f"límite {MAX_SKILL} caracteres · {len(rows)} skills · {len(over)} lo superan · "
          f"{len(split)} troceadas\n")
    print(f"{'caracteres':>10}  {'estado':<9} {'partes':>6}  skill")
    for size, name, n_partes in rows:
        estado = "EXCEDE" if size > MAX_SKILL else ("troceada" if n_partes else "ok")
        print(f"{size:>10}  {estado:<9} {n_partes:>6}  {name}")
    if over:
        print("\nPendientes de trocear (superan el límite):")
        for size, name, n_partes in over:
            extra = " (ya tiene partes: revisa el índice)" if n_partes else ""
            print(f"  - {name} ({size} caracteres){extra}")
    if split:
        print(f"\nYa troceadas ({len(split)}): " + ", ".join(row[1] for row in split))
    return 0


def split_one(skill_dir: Path, keep_original: bool, forced_inline: list[str] | None,
              dry_run: bool = False, quiet: bool = False) -> bool:
    """Trocea una skill. Devuelve False si no hacía falta; lanza PackError si no puede."""
    partes = partes_of(skill_dir)
    if partes:
        print(f"{skill_dir.name}: ya está troceada ({len(partes)} partes en references/); no toco nada")
        return False
    current = read(skill_dir / "SKILL.md")
    if len(current) <= MAX_SKILL:
        if not quiet:
            print(f"{skill_dir.name}: {len(current)} caracteres, cabe en {MAX_SKILL}; no necesita troceo")
        return False

    package = build_package(skill_dir, keep_original=keep_original, forced_inline=forced_inline)
    if package.problems:
        for problem in package.problems:
            print(f"  ERROR integridad: {problem}")
        raise PackError(f"{skill_dir.name}: el troceo perdería contenido; no escribo nada")
    print(f"{skill_dir.name}: {package.original_chars} → {package.final_chars} caracteres "
          f"({package.final_chars / package.original_chars * 100:.0f}% del original)")
    print(f"  inline: {', '.join(package.inline) if package.inline else '(sin secciones)'}")
    for part in package.parts:
        print(f"  references/{part.name:<40} {len(part.content):>6}  {part.label[:50]}")
    if keep_original:
        size = len(package.files["references/00-original.md"])
        print(f"  references/00-original.md{'':<19} {size:>6}  copia íntegra del original")
    for check in package.checks:
        print(f"  {check}")
    if dry_run:
        print("  (dry-run: no se escribe nada)")
        return True
    for rel, content in package.files.items():
        write(skill_dir / rel, content)
    print(f"  escrito: SKILL.md + {len(package.parts)} parte(s)"
          + (" + 00-original.md" if keep_original else ""))
    return True


SKIP_PREFIXES = ("http://", "https://", "mailto:", "data:", "#", "/")


def relative_links(text: str) -> list[str]:
    """Enlaces y definiciones markdown de destino relativo (sin anclas externas)."""
    targets = [match.group(2) for match in LINK_RE.finditer(text)]
    targets += [match.group(2) for match in DEF_RE.finditer(text)]
    clean: list[str] = []
    for target in targets:
        if not target or target.startswith(SKIP_PREFIXES):
            continue
        path = target.split("#", 1)[0].split("?", 1)[0]
        if path and not any(char.isspace() for char in path):
            clean.append(path)
    return clean


def verify(root: Path) -> int:
    skills = iter_skills(root)
    problems: list[str] = []
    warnings: list[str] = []
    troceadas = 0
    for skill_dir in skills:
        name = skill_dir.name
        text = read(skill_dir / "SKILL.md")
        partes = partes_of(skill_dir)
        if len(text) > MAX_SKILL:
            problems.append(f"{name}: SKILL.md tiene {len(text)} caracteres (> {MAX_SKILL})"
                            + (" y ya está troceada: revisa el índice" if partes else "; trocéala"))
        # el índice que genera el script: cada fila de la tabla debe existir
        for target in re.findall(r"(?m)^\|\s*`(references/[^`]+)`", text):
            if not (skill_dir / target).exists():
                problems.append(f"{name}: el índice enlaza {target}, que no existe")
        if not partes:
            for target in relative_links(text):
                if not (skill_dir / target).exists():
                    warnings.append(f"{name}: enlace relativo heredado roto en SKILL.md: {target}")
            continue
        troceadas += 1
        for parte in partes:
            content = read(parte)
            if not content.strip():
                problems.append(f"{name}: references/{parte.name} está vacía")
            elif len(content) > MAX_PARTE:
                warnings.append(f"{name}: references/{parte.name} tiene {len(content)} caracteres (> {MAX_PARTE})")
            if f"references/{parte.name}" not in text:
                problems.append(f"{name}: el índice no apunta a references/{parte.name}")
            for target in relative_links(content):
                if (parte.parent / target).exists():
                    continue
                if (skill_dir / target).exists():
                    problems.append(f"{name}: {parte.name} enlaza {target} y no se reescribió bien "
                                    f"(el destino existe; revisa el relink)")
                else:
                    warnings.append(f"{name}: {parte.name} enlaza {target}, que ya no existía antes del troceo")
    print(f"Verificación — {root}")
    print(f"  skills: {len(skills)} · troceadas: {troceadas} · problemas: {len(problems)} · "
          f"avisos: {len(warnings)}")
    for warning in warnings:
        print(f"  aviso: {warning}")
    for problem in problems:
        print(f"  ERROR: {problem}")
    if problems:
        return 1
    print(f"  OK — todas las SKILL.md caben en {MAX_SKILL} caracteres y los índices apuntan a ficheros existentes")
    return 0


def restore_one(skill_dir: Path) -> bool:
    """Deshace el troceo: SKILL.md vuelve a ser frontmatter + 00-original.md."""
    partes = partes_of(skill_dir)
    original = skill_dir / "references" / "00-original.md"
    if not partes or not original.exists():
        print(f"{skill_dir.name}: no está troceada con 00-original.md; no hay nada que restaurar")
        return False
    frontmatter, _ = split_frontmatter(read(skill_dir / "SKILL.md"))
    body = re.sub(r"(?m)^\s*<!--.*?-->\s*$\n?", "", read(original), count=1)
    write(skill_dir / "SKILL.md", frontmatter + body)
    for parte in partes:
        parte.unlink()
    original.unlink()
    print(f"{skill_dir.name}: restaurada a {len(frontmatter + body)} caracteres; "
          f"{len(partes)} parte(s) eliminadas")
    return True


def split_all(root: Path, keep_original: bool, dry_run: bool) -> int:
    targets = [skill_dir for skill_dir in iter_skills(root)
               if not partes_of(skill_dir) and len(read(skill_dir / "SKILL.md")) > MAX_SKILL]
    print(f"Trocear {len(targets)} skill(s) de {root}{' (dry-run)' if dry_run else ''}\n")
    done, failed = 0, []
    for skill_dir in targets:
        try:
            if split_one(skill_dir, keep_original, None, dry_run, quiet=True):
                done += 1
        except PackError as exc:
            failed.append(f"{skill_dir.name}: {exc}")
            print(f"  ERROR: {exc}")
        print()
    print(f"Troceadas: {done}/{len(targets)}")
    if failed:
        print("Fallos:")
        for item in failed:
            print(f"  - {item}")
        return 1
    return 0


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_bool(value: str) -> bool:
    low = str(value).strip().casefold()
    if low in {"true", "1", "si", "sí", "yes", "on"}:
        return True
    if low in {"false", "0", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"valor booleano no válido: {value} (usa true o false)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Trocea SKILL.md largas (>8192 caracteres) en references/parte-NN y deja un índice navegable."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit", action="store_true", help="lista tamaño y estado de cada skill")
    group.add_argument("--split", metavar="SKILL", help="trocea una skill (nombre de su carpeta)")
    group.add_argument("--split-all", action="store_true", help="trocea todas las que superen el límite")
    group.add_argument("--restore", metavar="SKILL", help="deshace el troceo usando references/00-original.md")
    group.add_argument("--verify", action="store_true", help="comprueba límites, partes e índice")
    parser.add_argument("--root", help=f"directorio de skills (por defecto {DEFAULT_ROOT})")
    parser.add_argument("--keep-original", nargs="?", const="true", default="true", type=parse_bool,
                        metavar="true|false",
                        help="conserva references/00-original.md (por defecto true)")
    parser.add_argument("--inline", action="append", default=[], metavar="ENCABEZADO",
                        help="sección que debe quedarse en SKILL.md; repite el flag para varias")
    parser.add_argument("--dry-run", action="store_true", help="calcula y muestra sin escribir")
    return parser


def run(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else DEFAULT_ROOT
    if args.audit:
        return audit(root)
    if args.verify:
        return verify(root)
    if args.split_all:
        return split_all(root, args.keep_original, args.dry_run)
    if args.restore:
        skill_dir = root / args.restore
        if not (skill_dir / "SKILL.md").exists():
            raise PackError(f"no existe la skill {args.restore} en {root}")
        restore_one(skill_dir)
        return 0
    skill_dir = root / args.split
    if not (skill_dir / "SKILL.md").exists():
        raise PackError(f"no existe la skill {args.split} en {root}")
    split_one(skill_dir, args.keep_original, args.inline, args.dry_run)
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except PackError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
