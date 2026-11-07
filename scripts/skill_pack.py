#!/usr/bin/env python3
"""Empaqueta skills largas: trocea el SKILL.md y deja un índice navegable.

El pruner de sesión recorta los resultados de herramienta a 8.192 caracteres del
fichero **real**: cuenta code points tal cual están en disco, así que un fichero
guardado en CRLF suma `\\r` + `\\n` (dos caracteres) por cada salto de línea. Por
eso este script:

- **mide el fichero real**, con `open(..., newline="")` (sin traducir saltos),
  nunca el texto normalizado que devuelve `Path.read_text`; informa además de
  los bytes y del peor caso CRLF (caracteres + líneas);
- **escribe en LF** (`newline="\\n"`) con presupuesto de 7.800 caracteres para el
  `SKILL.md` y 6.900 para cada `references/parte-*.md`, de modo que sigan por
  debajo de 8.192 incluso si un editor los vuelve a guardar en CRLF;
- guarda el original **íntegro** (frontmatter + cuerpo, con sus saltos de línea)
  en `references/00-original.md`, así que `--restore` lo devuelve byte a byte;
- `--verify` **reconstruye el cuerpo** (secciones inline + partes en orden) y lo
  compara con `references/00-original.md`: detecta secciones perdidas,
  duplicadas y texto añadido dentro de una parte. Un solo problema ⇒ exit 1.

Cada carácter del original acaba exactamente en un sitio: o inline en el
`SKILL.md` o en una sola parte. El script lo comprueba antes de escribir.

Uso:
    python scripts/skill_pack.py --audit [--root DIR]
    python scripts/skill_pack.py --split <skill> [--root DIR] [--keep-original false]
                                  [--inline "Encabezado"]...
    python scripts/skill_pack.py --split-all [--root DIR] [--dry-run]
    python scripts/skill_pack.py --resplit <skill> [--root DIR]   (re-trocea con el presupuesto actual)
    python scripts/skill_pack.py --resplit-all [--root DIR] [--dry-run]
    python scripts/skill_pack.py --verify [--root DIR]
    python scripts/skill_pack.py --restore <skill> [--root DIR]

Códigos de salida: 0 bien, 1 problemas (auditoría o verificación), 2 error de uso.

Sin dependencias externas (solo biblioteca estándar). Mensajes en español, UTF-8.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import unicodedata
from collections import deque
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

MAX_SKILL = 8192          # límite del pruner de DSH: lo que pase de aquí se recorta
SAFE_SKILL = 7800         # presupuesto de escritura del SKILL.md, en LF
SAFE_PARTE = 6900         # presupuesto de escritura de cada parte, en LF
HEADER_MARGIN = 200       # hueco para la cabecera de trazabilidad de cada trozo
INTRO_MAX = 1500          # la intro se queda entera hasta aquí; el resto se trocea
INLINE_SINGLE_MAX = 4200  # una sección mayor no se queda inline: se trocea
HINT_MAX = 70             # caracteres de pista por entrada del índice
DEFAULT_ROOT = Path.home() / ".agents" / "skills"
LINK_RE = re.compile(r"(!?\[[^\]]*\]\()\s*<?([^)\s>]+)>?\s*(\))")
DEF_RE = re.compile(r"(?m)^(\s*\[[^\]]+\]:\s*)(\S+)")
# marca del comentario que deja el troceo, para reconocer un SKILL.md empaquetado
NOTE_MARK = "<!-- Troceado por scripts/skill_pack.py"
INDEX_LINE = "\n## Índice de referencias\n"
INDEX_HEAD = (
    "## Índice de referencias\n\n"
    "El cuerpo largo vive en `references/` para que no se trunque al cargar la skill "
    f"(el límite son {MAX_SKILL} caracteres). Carga la parte que necesites; no hace falta leerlas todas.\n\n"
    "| Fichero | Contenido |\n|---|---|\n"
)
INLINE_HEAD = "## Reglas clave\n\n"
NOTE = ("<!-- Troceado por scripts/skill_pack.py: cada sección vive en un solo sitio. "
        "Carga solo la parte que necesites. -->\n")
ORIGINAL_NAME = "00-original.md"
ORIGINAL = f"references/{ORIGINAL_NAME}"


# ── errores, medidas y lectura/escritura ──────────────────────────────────────

class PackError(Exception):
    """Error de empaquetado que se informa con un mensaje, nunca con traceback."""


@dataclass(frozen=True)
class Size:
    """Tamaño de un fichero tal cual está en disco (lo que cuenta el pruner)."""

    chars: int   # code points del fichero: CRLF cuenta 2
    nbytes: int  # bytes en UTF-8
    lines: int   # saltos de línea `\n`
    crlf: int    # saltos que ya son `\r\n`

    @property
    def worst_crlf(self) -> int:
        """Caracteres si un editor guarda el fichero en CRLF (cada `\\n` pasa a `\\r\\n`)."""
        return self.chars - self.crlf + 2 * self.lines

    def row(self) -> str:
        return f"{self.chars} caracteres / {self.nbytes} bytes / peor CRLF {self.worst_crlf}"


def measure(text: str) -> Size:
    """Tamaño de un texto que se va a escribir tal cual."""
    return Size(chars=len(text), nbytes=len(text.encode("utf-8")),
                lines=text.count("\n"), crlf=text.count("\r\n"))


def to_lf(text: str) -> str:
    """Forma canónica para analizar: solo se normaliza CRLF (nunca se toca el texto)."""
    return text.replace("\r\n", "\n")


def read_raw(path: Path) -> str:
    """Lee el fichero sin traducir saltos: el texto que ve el pruner."""
    try:
        with open(path, "r", encoding="utf-8", newline="") as handle:
            return handle.read()
    except FileNotFoundError:
        raise PackError(f"no existe {path}") from None
    except UnicodeDecodeError:
        raise PackError(f"{path} no está en UTF-8 válido; vuelve a guardarlo en UTF-8") from None
    except OSError as exc:
        raise PackError(f"no se pudo leer {path}: {exc.strerror or exc}") from None


def read_lf(path: Path) -> str:
    """Lee normalizando CRLF: para analizar y trocear (nunca para medir)."""
    return to_lf(read_raw(path))


def write_lf(path: Path, text: str) -> None:
    """Escribe en LF exacto: `newline="\\n"` no traduce, así que no añade `\\r`."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    except OSError as exc:
        raise PackError(f"no se pudo escribir {path}: {exc.strerror or exc}") from None


def write_exact(path: Path, text: str) -> None:
    """Escribe el texto tal cual, conservando sus saltos de línea (restore byte a byte)."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
    except OSError as exc:
        raise PackError(f"no se pudo escribir {path}: {exc.strerror or exc}") from None


def measure_file(path: Path) -> Size:
    return measure(read_raw(path))


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── utilidades de texto ───────────────────────────────────────────────────────

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


def strip_header_comment(text: str) -> str:
    """Quita el comentario de cabecera que el troceo deja en 00-original.md."""
    match = re.match(r"<!--.*?-->\r?\n?", text, re.S)
    return text[match.end():] if match else text


def first_difference(expected: str, actual: str) -> str:
    """Describe dónde empiezan a diferir dos textos, para el mensaje de error."""
    limit = min(len(expected), len(actual))
    position = limit
    for index in range(limit):
        if expected[index] != actual[index]:
            position = index
            break
    line = expected.count("\n", 0, position) + 1
    fragment = actual[max(0, position - 20):position + 45].replace("\n", "⏎")
    if len(actual) == len(expected):
        detail = "mismo tamaño, distinto contenido"
    elif len(actual) > len(expected):
        detail = f"sobran {len(actual) - len(expected)} caracteres"
    else:
        detail = f"faltan {len(expected) - len(actual)} caracteres"
    return f"difiere en el carácter {position} (línea ~{line}): «…{fragment}…» ({detail})"


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
    fuera de la skill no se toca. La operación inversa (`references` → raíz)
    devuelve el texto original, y es la que usa `--verify` para reconstruir.
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

    def rewrite(match: re.Match) -> str:
        """Sustituye solo el destino: conserva el espaciado y los `<>` del original."""
        whole = match.group(0)
        start = match.start(2) - match.start(0)
        end = match.end(2) - match.start(0)
        return whole[:start] + fix(match.group(2)) + whole[end:]

    return DEF_RE.sub(rewrite, LINK_RE.sub(rewrite, text))


# ── construcción del paquete ───────────────────────────────────────────────────

@dataclass
class Part:
    name: str      # parte-01-titulo.md
    title: str     # encabezado original
    label: str     # etiqueta con (i/n) si la sección va en varias piezas
    hint: str
    source: str    # texto original de la pieza, sin comentarios ni relink (para integridad)
    content: str   # lo que se escribe en disco: cabecera + relink
    position: int = 1   # i de (i/n)
    total: int = 1      # n de (i/n)


@dataclass
class Package:
    skill: str
    original: Size
    final: Size = field(default_factory=lambda: Size(0, 0, 0, 0))
    parts: list[Part] = field(default_factory=list)
    inline: list[str] = field(default_factory=list)
    intro_kept: str = ""
    intro_rest: str = ""
    files: dict[str, str] = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)

    @property
    def final_chars(self) -> int:
        return self.final.chars


def _split_intro(intro: str, intro_max: int = INTRO_MAX) -> tuple[str, str]:
    """Parte la intro si es enorme, cortando en un salto de párrafo (corte exacto)."""
    if len(intro) <= intro_max:
        return intro, ""
    cut = intro.rfind("\n\n", 0, intro_max)
    cut = cut if cut > intro_max // 2 else intro_max
    return intro[:cut], intro[cut:]


def _part_header(skill: str, title: str, position: int = 1, total: int = 1) -> str:
    header = f"<!-- skill: {skill} · sección «{title}»"
    if total > 1:
        header += f" · pieza {position}/{total}"
    return header + " · origen: SKILL.md antes del troceo -->\n"


def _section_parts(section: Section, skill_dir: Path) -> list[Part]:
    """Piezas de una sección, cada una ≤ SAFE_PARTE ya con cabecera y enlaces."""
    limit = SAFE_PARTE - HEADER_MARGIN
    for _ in range(6):
        pieces = chunk_section(section, limit)
        total = len(pieces)
        parts = [Part(name="", title=section.title, label="", hint="", source=piece,
                      content=(_part_header(skill_dir.name, section.title, position, total)
                               + relink(piece, skill_dir, "", "references")),
                      position=position, total=total)
                 for position, piece in enumerate(pieces, start=1)]
        biggest = max((measure(part.content).chars for part in parts), default=0)
        if biggest <= SAFE_PARTE:
            return parts
        # el relink pudo engordar la pieza: se re-trocea con menos presupuesto
        limit = max(1200, limit - (biggest - SAFE_PARTE) - 40)
    raise PackError(f"«{section.title}» no cabe en partes de {SAFE_PARTE} caracteres "
                    f"(siguen siendo {biggest}); revisa el texto")


def _make_parts(sections: list[Section], inline_idx: set[int], skill_dir: Path,
                intro_rest: str) -> list[Part]:
    """Piezas de todas las secciones que no se quedan inline, en orden de documento."""
    parts: list[Part] = []
    number = 0
    if intro_rest.strip():
        number += 1
        content = (f"<!-- skill: {skill_dir.name} · resto de la introducción -->\n"
                   + relink(intro_rest, skill_dir, "", "references"))
        size = measure(content).chars
        if size > SAFE_PARTE:
            raise PackError(f"el resto de la introducción mide {size} caracteres y el máximo por "
                            f"parte es {SAFE_PARTE}; acorta la intro del SKILL.md")
        parts.append(Part(name=f"parte-{number:02d}-introduccion.md", title="Introducción",
                          label="Introducción", hint=clean_md(intro_rest)[:HINT_MAX] + "…",
                          source=intro_rest, content=content))
    for index, section in enumerate(sections):
        if index in inline_idx:
            continue
        for part in _section_parts(section, skill_dir):
            number += 1
            part.name = f"parte-{number:02d}-{slug(section.title)}.md"
            part.label = (section.title if part.total == 1
                          else f"{section.title} ({part.position}/{part.total})")
            part.hint = section.hint if part.position == 1 else ""
            parts.append(part)
    return parts


def _original_note(skill: str, raw: str, existing: str | None) -> str:
    """Contenido de 00-original.md: el original íntegro con una cabecera.

    Si el paquete ya existía y el original no ha cambiado, se reutiliza el fichero
    tal cual: así `--resplit` es idempotente y no cambia la fecha de la cabecera.
    """
    if existing is not None and strip_header_comment(existing) == raw:
        return existing
    return (f"<!-- Copia íntegra de SKILL.md antes del troceo ({len(raw)} caracteres, "
            f"{len(raw.encode('utf-8'))} bytes) · {date.today().isoformat()} · "
            f"generado por scripts/skill_pack.py -->\n" + raw)


def build_package(skill_dir: Path, keep_original: bool = True,
                  forced_inline: list[str] | None = None, raw: str | None = None,
                  original_note: str | None = None) -> Package:
    """Calcula los ficheros del empaquetado sin escribir nada en disco.

    `raw` es el SKILL.md original tal cual (con sus saltos de línea); si no se da,
    se lee del disco. `original_note` es el 00-original.md existente, para no
    reescribirlo cuando el contenido no cambia.
    """
    skill_dir = skill_dir.resolve()
    if raw is None:
        raw = read_raw(skill_dir / "SKILL.md")
    text = to_lf(raw)
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

    mandatory = sorted({0} | {i for i, s in enumerate(sections) if i and s.title.casefold() in requested})
    inline_idx = [i for i in mandatory if len(sections[i].raw) <= INLINE_SINGLE_MAX]
    dropped_big = [sections[i].title for i in mandatory if i not in inline_idx]

    def index_row(part: Part, compact: int) -> str:
        """Fila del índice. `compact` recorta la pista (y luego la etiqueta) si no cabe."""
        if compact == 0:
            extra = f" — {part.hint}" if part.hint else ""
            return f"| `references/{part.name}` | **{part.label}**{extra} |"
        if compact == 1:
            return f"| `references/{part.name}` | **{part.label}** |"
        return f"| `references/{part.name}` | **{part.label[:40]}** |"

    def assemble(chosen: list[int], compact: int = 0, intro_max: int = INTRO_MAX) -> Package:
        chosen_set = set(chosen)
        kept, rest = _split_intro(intro, intro_max)
        parts = _make_parts(sections, chosen_set, skill_dir, rest)
        rows = [index_row(part, compact) for part in parts]
        note = ""
        if keep_original:
            note = _original_note(skill_dir.name, raw, original_note)
            rows.append(f"| `{ORIGINAL}` | Copia íntegra del original "
                        f"({len(raw)} caracteres) — trazabilidad; no hace falta cargarla |")
        index = INDEX_HEAD + "\n".join(rows) + "\n"
        inline_text = "".join(sections[i].raw for i in sorted(chosen_set))
        pieces = [frontmatter, kept, NOTE, "\n", INLINE_HEAD,
                  inline_text, "\n", index]
        content = "".join(pieces)
        package = Package(skill=skill_dir.name, original=measure(raw), final=measure(content),
                          parts=parts, inline=[sections[i].title for i in sorted(chosen_set)],
                          intro_kept=kept, intro_rest=rest)
        package.files["SKILL.md"] = content
        for part in parts:
            package.files[f"references/{part.name}"] = part.content
        if keep_original:
            package.files[ORIGINAL] = note
        return package

    def fits(package: Package) -> bool:
        """Cabe en el presupuesto y, aun pasado a CRLF, no llega al límite del pruner."""
        return package.final.chars <= SAFE_SKILL and package.final.worst_crlf <= MAX_SKILL

    package = assemble(inline_idx)

    # Relleno: mientras quepa, se quedan inline las secciones más cortas en orden
    # de documento (las "reglas cortas imprescindibles" del manual).
    for index in range(len(sections)):
        if index in inline_idx or len(sections[index].raw) > INLINE_SINGLE_MAX:
            continue
        trial = sorted(inline_idx + [index])
        candidate = assemble(trial)
        if fits(candidate):
            inline_idx, package = trial, candidate

    # Presupuesto: si aun así no cabe, van cayendo las inline no obligatorias,
    # de la última a la primera, hasta entrar en el límite.
    droppable = [i for i in inline_idx if i != 0]
    while not fits(package) and droppable:
        inline_idx = [i for i in inline_idx if i != droppable.pop()]
        package = assemble(inline_idx)

    # Último recurso: se acorta la intro que se queda inline (el resto va a la parte 1,
    # no se pierde nada) y se comprime el índice (sin pistas); el índice sigue completo.
    if not fits(package):
        for intro_max, compact in ((900, 0), (600, 0), (300, 0), (300, 1), (0, 1), (0, 2)):
            candidate = assemble(inline_idx, compact=compact, intro_max=intro_max)
            if fits(candidate):
                package = candidate
                package.checks.append(f"índice comprimido e intro ajustada para caber "
                                      f"(intro inline {intro_max}, índice compact={compact})")
                break

    if not fits(package):
        raise PackError(f"{skill_dir.name}: ni con solo la primera sección cabe en {SAFE_SKILL} "
                        f"caracteres en LF (siguen siendo {package.final.chars}); revisa la intro "
                        f"y reduce el número de secciones")

    _check_integrity(package, sections, intro, skill_dir)
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
                     skill_dir: Path) -> None:
    """Cada sección, exactamente una vez; y el cuerpo reconstruido == el original."""
    inline_set = set(package.inline)
    intro_kept, intro_rest = package.intro_kept, package.intro_rest
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
        joined = "".join(found)
        if joined != section.raw:
            package.problems.append(f"«{section.title}» no se reconstruye igual que el original: "
                                    + first_difference(section.raw, joined))
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

    # los enlaces: lo escrito tiene que ser exactamente el original con los destinos movidos
    # (si un enlace quedara partido entre dos piezas, --verify no podría reconstruirlo)
    for section in sections:
        if section.title in inline_set:
            continue
        group = [part for part in package.parts if part.title == section.title]
        expected = relink(section.raw, skill_dir, "", "references")
        actual = "".join(strip_header_comment(part.content) for part in group)
        if actual != expected:
            package.problems.append(
                f"«{section.title}»: los enlaces del trozo no reconstruyen el texto escrito "
                f"({first_difference(expected, actual)}); puede haber un enlace partido entre piezas")
    intro_part = [part for part in package.parts if part.title == "Introducción"]
    if intro_part:
        expected = relink(intro_rest, skill_dir, "", "references")
        actual = "".join(strip_header_comment(part.content) for part in intro_part)
        if actual != expected:
            package.problems.append("«Introducción»: los enlaces del trozo no reconstruyen el "
                                    "texto escrito (" + first_difference(expected, actual) + ")")

    if not package.problems:
        digest = sha256(_strip("".join(s.raw for s in sections)))[:12]
        package.checks.append(
            f"{len(sections)} secciones: {len(package.inline)} inline + {len(package.parts)} trozos; "
            f"ninguna repetida ni perdida (sha256 del cuerpo {digest})")


# ── lectura de un paquete ya escrito (para --verify y --restore) ───────────────

@dataclass
class DiskPart:
    name: str
    title: str
    position: int | None   # i de (i/n); None si la parte no declara numeración
    total: int | None
    raw: str               # lo escrito, sin la cabecera de trazabilidad
    source: str            # el mismo texto con los enlaces devueltos a la raíz (para los enlaces)


@dataclass
class DiskPackage:
    frontmatter: str
    intro_kept: str
    inline: list[Section]
    parts: list[DiskPart]
    original: str | None   # original íntegro tal cual (con sus saltos de línea)
    index_rows: list[str]
    notes: list[str] = field(default_factory=list)


def _parse_part_header(first_line: str) -> tuple[str, int | None, int | None] | None:
    """Título y numeración de la cabecera de una parte, o None si no la tiene."""
    match = re.match(r"<!-- skill: [^ ]+ · (.+?) -->\s*$", first_line)
    if not match:
        return None
    text = match.group(1)
    if "resto de la introducción" in text:
        return "Introducción", None, None
    title = re.search(r"sección «(.+?)»", text)
    if not title:
        return None
    piece = re.search(r"pieza (\d+)/(\d+)", text)
    if piece:
        return title.group(1), int(piece.group(1)), int(piece.group(2))
    return title.group(1), None, None


def read_package(skill_dir: Path) -> DiskPackage:
    """Lee el paquete escrito en disco: SKILL.md, partes y 00-original.md."""
    skill_dir = skill_dir.resolve()
    text = to_lf(read_raw(skill_dir / "SKILL.md"))
    frontmatter, body = split_frontmatter(text)
    notes: list[str] = []
    marker = body.find(NOTE_MARK)
    if marker >= 0:
        intro_kept = body[:marker]
        rest = body[marker:]
        end = rest.find("\n", rest.find("-->") + 3)
        rest = rest[end + 1:] if end >= 0 else ""
    else:
        notes.append("no lleva el comentario de cabecera del troceo; se busca el índice igualmente")
        intro_kept, rest = "", body
    cut = rest.rfind(INDEX_LINE)
    if cut < 0 and rest.startswith("## Índice de referencias"):
        cut = 0
    inline_region = rest[:cut] if cut >= 0 else rest
    index_text = rest[cut:] if cut >= 0 else ""
    start = inline_region.find(INLINE_HEAD)
    if start >= 0:
        if inline_region[:start].strip():
            notes.append("hay texto suelto entre la cabecera y «## Reglas clave»")
        inline_region = inline_region[start + len(INLINE_HEAD):]
    inline_intro, inline = parse_sections(inline_region)
    if inline_intro.strip():
        notes.append("hay texto suelto fuera de sección en la zona inline")
    index_rows = re.findall(r"(?m)^\|\s*`(references/[^`]+)`", index_text)

    parts: list[DiskPart] = []
    refs = skill_dir / "references"
    for path in sorted(refs.glob("parte-*.md")) if refs.exists() else []:
        content = to_lf(read_raw(path))
        first, _, remainder = content.partition("\n")
        parsed = _parse_part_header(first.strip())
        if parsed is None:
            notes.append(f"references/{path.name} no lleva cabecera de trazabilidad")
            title, position, total = path.stem, None, None
            remainder = content
        else:
            title, position, total = parsed
        parts.append(DiskPart(name=path.name, title=title, position=position, total=total,
                              raw=remainder,
                              source=relink(remainder, skill_dir, "references", "")))

    original_path = refs / ORIGINAL_NAME
    original = strip_header_comment(read_raw(original_path)) if original_path.exists() else None
    return DiskPackage(frontmatter=frontmatter, intro_kept=intro_kept, inline=inline,
                       parts=parts, original=original, index_rows=index_rows, notes=notes)


def _take_pieces(queue: deque[DiskPart]) -> tuple[list[DiskPart], str]:
    """Saca de la cola las piezas consecutivas de una sección y valida su numeración."""
    first = queue.popleft()
    total = first.total or 1
    group = [first]
    while queue and len(group) < total:
        group.append(queue.popleft())
    declared = [(piece.position or 1, piece.total or 1) for piece in group]
    expected = [(index, total) for index in range(1, len(group) + 1)]
    if len(group) != total:
        return group, f"la sección declara {total} pieza(s) y hay {len(group)}"
    if declared != expected:
        return group, f"numeración de piezas inesperada: {declared} (se esperaba {expected})"
    return group, ""


def _check_package(skill_dir: Path, disk: DiskPackage) -> tuple[list[str], list[str], str | None]:
    """Reconstruye el cuerpo (inline + partes) y lo compara con 00-original.md.

    Devuelve (problemas, avisos, sha256 del cuerpo reconstruido).
    """
    problems: list[str] = []
    warnings: list[str] = []
    name = skill_dir.name
    if not disk.parts:
        return problems, warnings, None
    if disk.original is None:
        warnings.append(f"{name}: sin references/00-original.md; no se puede comprobar la integridad "
                        f"(vuelve a trocearla con --resplit)")
        return problems, warnings, None

    original_lf = to_lf(disk.original)
    _, body = split_frontmatter(original_lf)
    intro, sections = parse_sections(body)
    if not sections:
        problems.append(f"{name}: el original no tiene secciones `##`; no se puede reconstruir")
        return problems, warnings, None

    inline_q: dict[str, deque[Section]] = {}
    for section in disk.inline:
        inline_q.setdefault(section.title, deque()).append(section)
    parts_q: dict[str, deque[DiskPart]] = {}
    for part in disk.parts:
        if part.title != "Introducción":
            parts_q.setdefault(part.title, deque()).append(part)
    intro_parts = [part for part in disk.parts if part.title == "Introducción"]

    def moved(text: str) -> str:
        """El texto como debe quedar al bajar a references/ (misma transformación al crear y al leer)."""
        return relink(text, skill_dir, "", "references")

    # la intro: lo que se queda inline, tal cual; el resto, en parte-01 y con los enlaces movidos
    if not intro.startswith(disk.intro_kept):
        problems.append(f"{name}: la introducción inline de SKILL.md no es el principio de la "
                        f"introducción del original (" + first_difference(intro, disk.intro_kept) + ")")
        intro_rest = ""
    else:
        intro_rest = intro[len(disk.intro_kept):]
        intro_written = "".join(part.raw for part in intro_parts)
        if moved(intro_rest) != intro_written:
            problems.append(f"{name}: el resto de la introducción no coincide con 00-original.md en "
                            f"references/{intro_parts[0].name if intro_parts else 'parte-01'} ("
                            + first_difference(moved(intro_rest), intro_written) + ")")

    moved_pieces: list[str] = []
    for section in sections:
        queue = inline_q.get(section.title)
        if queue:
            block = queue.popleft()
            if block.raw != section.raw and block.raw.strip("\n") != section.raw.strip("\n"):
                problems.append(f"{name}: la sección «{section.title}» inline no coincide con el "
                                f"original (" + first_difference(section.raw, block.raw) + ")")
            continue
        pieces = parts_q.get(section.title)
        if pieces:
            group, error = _take_pieces(pieces)
            if error:
                problems.append(f"{name}: «{section.title}» {error}")
            joined = "".join(piece.raw for piece in group)
            if moved(section.raw) != joined:
                where = f"references/{group[0].name}"
                if len(group) > 1:
                    where += f" (+{len(group) - 1} pieza(s) más)"
                problems.append(f"{name}: «{section.title}» no se reconstruye igual que el original "
                                f"en {where} — texto añadido, duplicado o perdido ("
                                + first_difference(moved(section.raw), joined) + ")")
            moved_pieces.append(moved(section.raw))
            continue
        problems.append(f"{name}: la sección «{section.title}» se ha perdido: no está inline "
                        f"ni en ninguna parte")

    leftovers = [section.title for queue in inline_q.values() for section in queue]
    leftovers += [part.title for queue in parts_q.values() for part in queue]
    if leftovers:
        problems.append(f"{name}: hay contenido que no está en el original (secciones de más): "
                        + ", ".join(f"«{title}»" for title in leftovers))

    # reconstrucción del cuerpo que vive en references/: intro movida + secciones troceadas,
    # en orden de documento, contra lo que hay escrito en las partes (nombradas por su número)
    if not problems:
        written = "".join(part.raw for part in disk.parts)
        expected = moved(intro_rest) + "".join(moved_pieces)
        if written != expected:
            problems.append(f"{name}: las partes, en orden, no reconstruyen el cuerpo de "
                            f"00-original.md (" + first_difference(expected, written) + ")")
        else:
            return problems, warnings, sha256(_strip(body))
    return problems, warnings, None


# ── comandos ───────────────────────────────────────────────────────────────────

def iter_skills(root: Path) -> list[Path]:
    if not root.exists():
        raise PackError(f"no existe el directorio de skills: {root}")
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def partes_of(skill_dir: Path) -> list[Path]:
    refs = skill_dir / "references"
    return sorted(refs.glob("parte-*.md")) if refs.exists() else []


def _skill_row(skill_dir: Path) -> dict:
    size = measure_file(skill_dir / "SKILL.md")
    partes = partes_of(skill_dir)
    part_sizes = [measure_file(path) for path in partes]
    return {
        "name": skill_dir.name,
        "size": size,
        "partes": len(partes),
        "max_parte": max((item.chars for item in part_sizes), default=0),
        "over_parte": [path.name for path, item in zip(partes, part_sizes) if item.chars > SAFE_PARTE],
    }


def audit(root: Path) -> int:
    skills = iter_skills(root)
    rows = [_skill_row(skill_dir) for skill_dir in skills]
    rows.sort(key=lambda row: (-row["size"].chars, row["name"]))
    over = [row for row in rows if row["size"].chars > MAX_SKILL]
    split = [row for row in rows if row["partes"]]
    risky = [row for row in rows if row["size"].chars <= MAX_SKILL
             and row["size"].worst_crlf > MAX_SKILL]
    print(f"Auditoría de skills — {root}")
    print("Caracteres medidos sobre el fichero real (newline=\"\"), como los cuenta el pruner: "
          "CRLF suma 2.")
    print(f"límite {MAX_SKILL} caracteres · {len(rows)} skills · {len(over)} lo superan · "
          f"{len(split)} troceadas · presupuesto de escritura {SAFE_SKILL} (SKILL.md) / "
          f"{SAFE_PARTE} (partes) en LF")
    if risky:
        print(f"aviso: {len(risky)} por debajo del límite pero sin margen si se guardan en CRLF: "
              + ", ".join(row["name"] for row in risky))
    print()
    print(f"{'caracteres':>10} {'bytes':>7} {'peorCRLF':>9}  {'estado':<11} {'partes':>6} "
          f"{'parte+':>7}  skill")
    for row in rows:
        size = row["size"]
        if size.chars > MAX_SKILL:
            estado = "EXCEDE"
        elif row["over_parte"]:
            estado = "parte larga"
        elif row["partes"]:
            estado = "troceada"
        else:
            estado = "ok"
        print(f"{size.chars:>10} {size.nbytes:>7} {size.worst_crlf:>9}  {estado:<11} "
              f"{row['partes']:>6} {row['max_parte']:>7}  {row['name']}")
    if over:
        print("\nPendientes de trocear (superan el límite en caracteres reales):")
        for row in over:
            extra = " (ya tiene partes: re-trocea con --resplit)" if row["partes"] else ""
            print(f"  - {row['name']} ({row['size'].chars} caracteres){extra}")
    if split:
        print(f"\nYa troceadas ({len(split)}): " + ", ".join(row["name"] for row in split))
    if over:
        print(f"\nFALLO: {len(over)} skill(s) superan {MAX_SKILL} caracteres reales; "
              f"el pruner las recortaría al cargarlas")
        return 1
    print(f"\nOK: ninguna SKILL.md supera {MAX_SKILL} caracteres reales")
    return 0


def _write_package(skill_dir: Path, package: Package, dry_run: bool,
                   keep_original: bool) -> int:
    """Escribe el paquete y borra las partes que ya no forman parte de él."""
    refs = skill_dir / "references"
    written = 0
    deleted = 0
    if not dry_run:
        for rel, content in package.files.items():
            write_lf(skill_dir / rel, content)
            written += 1
        for path in sorted(refs.glob("parte-*.md")):
            if f"references/{path.name}" not in package.files:
                path.unlink()
                deleted += 1
        if not keep_original and (refs / ORIGINAL_NAME).exists():
            (refs / ORIGINAL_NAME).unlink()
    print(f"  escrito: SKILL.md + {len(package.parts)} parte(s)"
          + (" + 00-original.md" if keep_original else "")
          + (f" · {deleted} parte(s) obsoleta(s) borrada(s)" if deleted else "")
          + (" (dry-run: no se escribe nada)" if dry_run else ""))
    return written


def _report_package(package: Package, keep_original: bool) -> None:
    print(f"{package.skill}: {package.original.chars} → {package.final.chars} caracteres reales "
          f"({package.final.chars / max(package.original.chars, 1) * 100:.0f}% del original; "
          f"peor caso CRLF {package.final.worst_crlf})")
    print(f"  inline: {', '.join(package.inline) if package.inline else '(sin secciones)'}")
    for part in package.parts:
        print(f"  references/{part.name:<40} {measure(part.content).chars:>6}  {part.label[:50]}")
    if keep_original:
        print(f"  {ORIGINAL:<51} {measure(package.files[ORIGINAL]).chars:>6}  copia íntegra del original")
    for check in package.checks:
        print(f"  {check}")


def _bridge_package(skill_dir: Path, keep_original: bool,
                    forced_inline: list[str] | None) -> Package:
    """Paquete a partir del original guardado (si ya estaba troceada) o del SKILL.md."""
    original_path = skill_dir / "references" / ORIGINAL_NAME
    existing = read_raw(original_path) if original_path.exists() else None
    raw = strip_header_comment(existing) if existing is not None else read_raw(skill_dir / "SKILL.md")
    if existing is not None and not split_frontmatter(to_lf(raw))[0]:
        # paquete antiguo: 00-original.md guardaba solo el cuerpo
        frontmatter, _ = split_frontmatter(read_lf(skill_dir / "SKILL.md"))
        raw = frontmatter + raw
    package = build_package(skill_dir, keep_original=keep_original, forced_inline=forced_inline,
                            raw=raw, original_note=existing)
    if package.problems:
        for problem in package.problems:
            print(f"  ERROR integridad: {problem}")
        raise PackError(f"{skill_dir.name}: el troceo perdería contenido; no escribo nada")
    return package


def split_one(skill_dir: Path, keep_original: bool, forced_inline: list[str] | None,
              dry_run: bool = False, quiet: bool = False) -> bool:
    """Trocea una skill. Devuelve False si no hacía falta; lanza PackError si no puede."""
    partes = partes_of(skill_dir)
    if partes:
        print(f"{skill_dir.name}: ya está troceada ({len(partes)} partes en references/); "
              f"no toco nada (usa --resplit para re-trocear)")
        return False
    current = measure_file(skill_dir / "SKILL.md")
    if current.chars <= MAX_SKILL and current.worst_crlf <= MAX_SKILL:
        if not quiet:
            print(f"{skill_dir.name}: {current.chars} caracteres reales, cabe en {MAX_SKILL}; "
                  f"no necesita troceo")
        return False

    package = _bridge_package(skill_dir, keep_original, forced_inline)
    _report_package(package, keep_original)
    _write_package(skill_dir, package, dry_run, keep_original)
    return True


def resplit_one(skill_dir: Path, keep_original: bool, forced_inline: list[str] | None,
                dry_run: bool = False) -> bool:
    """Re-trocea una skill ya troceada con el presupuesto actual. Devuelve True si cambió algo."""
    if not partes_of(skill_dir):
        return split_one(skill_dir, keep_original, forced_inline, dry_run)
    # si el paquete actual ya divergía del original, se avisa antes de rehacerlo
    old_problems, _, _ = _check_package(skill_dir, read_package(skill_dir))
    for problem in old_problems[:5]:
        print(f"  aviso: el paquete actual ya no cuadra con 00-original.md: {problem}")
    package = _bridge_package(skill_dir, keep_original, forced_inline)
    changes: list[str] = []
    for rel, content in package.files.items():
        path = skill_dir / rel
        if not path.exists() or read_raw(path) != content:
            changes.append(rel)
    for path in sorted((skill_dir / "references").glob("parte-*.md")):
        if f"references/{path.name}" not in package.files:
            changes.append(f"references/{path.name} (obsoleta)")
    if not changes:
        print(f"{skill_dir.name}: sin cambios ({package.final.chars} caracteres reales en "
              f"{len(package.parts)} parte(s)); no reescribo")
        return False
    print(f"{skill_dir.name}: {len(changes)} fichero(s) a reescribir")
    for rel in changes:
        print(f"  {rel}")
    _report_package(package, keep_original)
    _write_package(skill_dir, package, dry_run, keep_original)
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
    verified = 0
    total_sections = 0
    for skill_dir in skills:
        name = skill_dir.name
        size = measure_file(skill_dir / "SKILL.md")
        partes = partes_of(skill_dir)
        if size.chars > MAX_SKILL:
            problems.append(f"{name}: SKILL.md tiene {size.chars} caracteres reales (> {MAX_SKILL})"
                            + (" y ya está troceada: re-trocea con --resplit" if partes
                               else "; trocéala con --split"))
        elif size.worst_crlf > MAX_SKILL:
            warnings.append(f"{name}: {size.chars} caracteres, pero {size.worst_crlf} si se guarda en "
                            f"CRLF (>{MAX_SKILL}); conviene trocearla")
        # el índice que genera el script: cada fila de la tabla debe existir
        for target in re.findall(r"(?m)^\|\s*`(references/[^`]+)`", read_lf(skill_dir / "SKILL.md")):
            if not (skill_dir / target).exists():
                problems.append(f"{name}: el índice enlaza {target}, que no existe")
        if not partes:
            for target in relative_links(read_lf(skill_dir / "SKILL.md")):
                if not (skill_dir / target).exists():
                    warnings.append(f"{name}: enlace relativo heredado roto en SKILL.md: {target}")
            continue
        troceadas += 1
        if size.chars > SAFE_SKILL:
            problems.append(f"{name}: SKILL.md tiene {size.chars} caracteres en LF y el presupuesto "
                            f"seguro es {SAFE_SKILL} (re-trocea con --resplit)")
        disk = read_package(skill_dir)
        for note in disk.notes:
            warnings.append(f"{name}: {note}")
        if f"`{ORIGINAL}`" not in read_lf(skill_dir / "SKILL.md"):
            warnings.append(f"{name}: el índice no menciona {ORIGINAL}")
        indexed = [row for row in disk.index_rows if "/parte-" in row]
        expected = [f"references/{part.name}" for part in disk.parts]
        if indexed != expected:
            missing = [item for item in expected if item not in indexed]
            extra = [item for item in indexed if item not in expected]
            detail = []
            if missing:
                detail.append(f"el índice no apunta a {', '.join(missing)}")
            if extra:
                detail.append(f"el índice apunta a ficheros que no existen: {', '.join(extra)}")
            if not detail:
                detail.append("el orden del índice no coincide con el de las partes")
            problems.append(f"{name}: índice incoherente: " + "; ".join(detail))
        for part in disk.parts:
            path = skill_dir / "references" / part.name
            size_part = measure_file(path)
            if not part.source.strip():
                problems.append(f"{name}: references/{part.name} está vacía")
            elif size_part.chars > SAFE_PARTE:
                problems.append(f"{name}: references/{part.name} tiene {size_part.chars} caracteres en "
                                f"LF y el presupuesto seguro es {SAFE_PARTE}")
            for target in relative_links(part.source):
                if (skill_dir / target).exists():
                    continue
                if (path.parent / target).exists():
                    problems.append(f"{name}: {part.name} enlaza {target}, que no se reescribió bien "
                                    f"(existe dentro de references/ pero el enlace no se devolvió a la raíz)")
                else:
                    warnings.append(f"{name}: {part.name} enlaza {target}, que ya no existía antes "
                                    f"del troceo")
        integrity_problems, integrity_warnings, digest = _check_package(skill_dir, disk)
        problems.extend(integrity_problems)
        warnings.extend(integrity_warnings)
        if digest:
            verified += 1
            total_sections += len(disk.inline) + len(disk.parts)
    print(f"Verificación — {root}")
    print(f"  caracteres medidos sobre el fichero real (CRLF suma 2) · límite {MAX_SKILL} · "
          f"presupuesto {SAFE_SKILL}/{SAFE_PARTE} en LF")
    print(f"  skills: {len(skills)} · troceadas: {troceadas} · problemas: {len(problems)} · "
          f"avisos: {len(warnings)}")
    if verified:
        print(f"  integridad: {verified} paquete(s) reconstruidos (inline + partes) == 00-original.md, "
              f"{total_sections} secciones en total")
    for warning in warnings:
        print(f"  aviso: {warning}")
    for problem in problems:
        print(f"  ERROR: {problem}")
    if problems:
        return 1
    print(f"  OK — todas las SKILL.md caben en {MAX_SKILL} caracteres reales, las partes en "
          f"{SAFE_PARTE} en LF, el cuerpo se reconstruye contra 00-original.md y los índices "
          f"apuntan a ficheros existentes")
    return 0


def restore_one(skill_dir: Path) -> bool:
    """Deshace el troceo: SKILL.md vuelve a ser el original íntegro, byte a byte."""
    partes = partes_of(skill_dir)
    original = skill_dir / "references" / ORIGINAL_NAME
    if not partes or not original.exists():
        print(f"{skill_dir.name}: no está troceada con 00-original.md; no hay nada que restaurar")
        return False
    stored = strip_header_comment(read_raw(original))
    frontmatter, body = split_frontmatter(stored)
    if frontmatter:
        restored = stored  # formato actual: 00-original guarda el fichero completo
    else:
        # paquete antiguo: 00-original guardaba solo el cuerpo
        current_frontmatter, _ = split_frontmatter(read_raw(skill_dir / "SKILL.md"))
        restored = current_frontmatter + body
        print(f"{skill_dir.name}: paquete en formato antiguo (00-original sin frontmatter); "
              f"se recompone con el frontmatter actual")
    write_exact(skill_dir / "SKILL.md", restored)
    for parte in partes:
        parte.unlink()
    original.unlink()
    print(f"{skill_dir.name}: restaurada a {measure(restored).row()}; "
          f"{len(partes)} parte(s) eliminadas")
    return True


def split_all(root: Path, keep_original: bool, dry_run: bool) -> int:
    targets = [skill_dir for skill_dir in iter_skills(root)
               if not partes_of(skill_dir)
               and measure_file(skill_dir / "SKILL.md").chars > MAX_SKILL]
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


def resplit_all(root: Path, keep_original: bool, dry_run: bool) -> int:
    targets = [skill_dir for skill_dir in iter_skills(root) if partes_of(skill_dir)]
    print(f"Re-trocear {len(targets)} skill(s) de {root}{' (dry-run)' if dry_run else ''}\n")
    changed, failed = 0, []
    for skill_dir in targets:
        try:
            if resplit_one(skill_dir, keep_original, None, dry_run):
                changed += 1
        except PackError as exc:
            failed.append(f"{skill_dir.name}: {exc}")
            print(f"  ERROR: {exc}")
        print()
    print(f"Re-troceadas con cambios: {changed}/{len(targets)}")
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
        description=f"Trocea SKILL.md largas (>{MAX_SKILL} caracteres reales) en "
                    f"references/parte-NN y deja un índice navegable."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit", action="store_true",
                       help="lista el tamaño real de cada skill (exit 1 si alguna supera el límite)")
    group.add_argument("--split", metavar="SKILL", help="trocea una skill (nombre de su carpeta)")
    group.add_argument("--split-all", action="store_true", help="trocea todas las que superen el límite")
    group.add_argument("--resplit", metavar="SKILL",
                       help="re-trocea con el presupuesto actual una skill ya troceada")
    group.add_argument("--resplit-all", action="store_true", help="re-trocea todas las troceadas")
    group.add_argument("--restore", metavar="SKILL",
                       help="deshace el troceo usando references/00-original.md")
    group.add_argument("--verify", action="store_true",
                       help="comprueba límites, presupuesto, índice e integridad contra 00-original.md")
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
    if args.resplit_all:
        return resplit_all(root, args.keep_original, args.dry_run)
    if args.restore:
        skill_dir = root / args.restore
        if not (skill_dir / "SKILL.md").exists():
            raise PackError(f"no existe la skill {args.restore} en {root}")
        restore_one(skill_dir)
        return 0
    skill_dir = root / (args.split or args.resplit)
    if not (skill_dir / "SKILL.md").exists():
        raise PackError(f"no existe la skill {args.split or args.resplit} en {root}")
    if args.resplit:
        resplit_one(skill_dir, args.keep_original, args.inline, args.dry_run)
    else:
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
