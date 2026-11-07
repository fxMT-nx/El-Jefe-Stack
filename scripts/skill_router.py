#!/usr/bin/env python3
"""Router de skills para El Jefe.

Inspirado en la recuperación de skills de Skill-3D: puntúa las skills instaladas
contra una tarea y devuelve un ranking corto y explicable. Sin dependencias.

Uso:
    python scripts/skill_router.py "auditar SEO técnico de una landing"
    python scripts/skill_router.py "animar un botón" --top 5 --json
    python scripts/skill_router.py --build-index        # skills/index.json
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Clases de intención (inspirado en question-class de Skill-3D): si la tarea
# menciona estos términos, se refuerzan las skills del grupo aunque el nombre de
# la skill no contenga la palabra exacta de la consulta.
INTENT_RULES = [
    (
        "animacion",
        ("animar", "animacion", "transicion", "easing", "motion", "microinteraccion", "spring", "hover"),
        (
            "motion-design", "ui-animation", "animate", "apple-design", "emil-design-eng",
            "find-animation-opportunities", "improve-animations", "review-animations",
            "animation-vocabulary",
        ),
    ),
    (
        "diseno",
        ("disenar", "diseno", "landing", "tipografia", "paleta", "visual", "estilo"),
        ("design-taste-frontend", "frontend-design", "ui-design", "apple-design", "web-design-guidelines", "antfu-web-design-guidelines"),
    ),
    (
        "seo",
        ("seo", "posicionamiento", "schema", "geo", "buscadores", "serp", "citabilidad"),
        ("seo", "seo-technical", "seo-content", "seo-schema", "seo-geo"),
    ),
    (
        "seguridad",
        ("seguridad", "security", "auth", "owasp", "vulnerabilidad", "permisos", "threat"),
        ("security-best-practices", "security-threat-model"),
    ),
    (
        "marketing",
        ("marketing", "cro", "conversion", "email", "lanzamiento", "launch", "competencia", "campana"),
        ("cro", "emails", "launch", "product-marketing", "brand"),
    ),
    (
        # El stack trabaja en español: "precio" no aparece en las descripciones
        # inglesas de pricing, así que la intención cubre la tarea en ambos idiomas.
        # founder-pricing manda al fijar un número; monetizing-innovation entra
        # como segunda lectura de packaging/modelo.
        "precio",
        (
            "precio", "precios", "pricing", "price", "tarifa", "tarifas",
            "cuanto cobrar", "monetiz", "packaging", "freemium",
            "willingness to pay", "disposicion a pagar", "plan de precios",
            "planes de precios", "pagar por", "good-better-best",
        ),
        (("founder-pricing", 5.0), ("monetizing-innovation", 4.0)),
    ),
    (
        "copy",
        (
            "copy", "copywriting", "microcopy", "texto", "textos", "redactar",
            "redaccion", "titular", "titulares", "reescribir",
        ),
        ("copy-editing", "copywriting"),
    ),
    (
        "documentacion",
        ("documentacion", "readme", "changelog", "adr", "documentar", "bitacora", "guia"),
        ("changelog-automation", "architecture-decision-records", "domain-modeling", "writing-plans"),
    ),
    (
        "pruebas",
        ("test", "pruebas", "qa", "testing", "e2e", "regresion", "aceptacion"),
        ("playwright", "webapp-testing", "vitest", "ui-verification", "code-review-and-quality"),
    ),
    (
        "3d",
        ("3d", "modelado", "blender", "gltf", "pbr", "textur", "escena"),
        ("media-use", "motion-design", "canvas-design", "algorithmic-art", "hyperframes-animation"),
    ),
    (
        "web3d",
        ("threejs", "three.js", "webgl", "r3f", "react three fiber", "shader", "gltf viewer", "escena web"),
        ("threejs",),
    ),
]


def fold(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(c) != "Mn"
    )


STOPWORDS = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "o", "en",
    "con", "para", "por", "que", "del", "al", "se", "su", "sus", "mi", "me",
    "es", "son", "como", "más", "mas", "pero", "si", "no", "a", "the", "a", "an",
    "and", "or", "for", "with", "to", "of", "in", "on", "use", "using", "when",
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-záéíóúñü0-9]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def parse_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data: dict[str, str] = {}
    key = None
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z0-9_-]+:\s*", line):
            key, _, value = line.partition(":")
            key = key.strip()
            data[key] = value.strip().strip(">|-").strip()
        elif key and line.startswith((" ", "\t")):
            data[key] = (data.get(key, "") + " " + line.strip()).strip()
    return data


def load_skills(dirs: list[Path]) -> list[dict]:
    skills = []
    seen = set()
    for base in dirs:
        if not base.exists():
            continue
        candidates = sorted(base.glob("*/SKILL.md"))
        if (base / "SKILL.md").exists():
            candidates.append(base / "SKILL.md")
        for path in candidates:
            text = path.read_text(encoding="utf-8", errors="replace")
            fm = parse_frontmatter(text)
            name = fm.get("name") or path.parent.name
            if name in seen:
                continue
            seen.add(name)
            body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
            skills.append(
                {
                    "name": name,
                    "description": fm.get("description", ""),
                    "when": fm.get("whenToUse", "") or fm.get("when", ""),
                    "dir": str(path.parent),
                    "chars": len(text),
                    "triggers": tokenize(
                        " ".join(
                            [
                                name.replace("-", " "),
                                fm.get("description", ""),
                                fm.get("whenToUse", ""),
                                fm.get("when", ""),
                                body[:2000],
                            ]
                        )
                    ),
                }
            )
    return skills


def intent_weights(names: tuple) -> dict[str, float]:
    """Nombre de skill -> refuerzo. Una entrada suelta vale 4; una tupla, su peso."""
    weights: dict[str, float] = {}
    for entry in names:
        if isinstance(entry, str):
            weights[entry] = 4.0
        else:
            name, weight = entry
            weights[name] = float(weight)
    return weights


def score(query_tokens: set[str], skill: dict) -> tuple[float, list[str]]:
    name_tokens = set(tokenize(skill["name"].replace("-", " ")))
    desc_tokens = set(tokenize(skill["description"]))
    when_tokens = set(tokenize(skill["when"]))
    trig_tokens = set(skill["triggers"])
    hits: list[str] = []
    score = 0.0
    for token in query_tokens:
        if token in name_tokens:
            score += 6.0
            hits.append(token)
        elif token in when_tokens:
            score += 4.0
            hits.append(token)
        elif token in desc_tokens:
            score += 2.0
            hits.append(token)
        elif token in trig_tokens:
            score += 0.5
        # coincidencias parciales (stemming pobre)
        else:
            for cand in name_tokens | when_tokens | desc_tokens:
                if len(token) >= 5 and (cand.startswith(token[:5]) or token.startswith(cand[:5])):
                    score += 0.8
                    break
    if score > 0:
        score = score / math.log2(2 + skill["chars"] / 4000)
    return score, sorted(set(hits))


def main() -> int:
    ap = argparse.ArgumentParser(description="Ranking de skills para una tarea")
    ap.add_argument("query", nargs="?", default="", help="tarea a resolver")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--build-index", action="store_true")
    ap.add_argument("--dirs", nargs="*", default=None, help="directorios de skills extra")
    args = ap.parse_args()

    home = Path.home()
    dirs = [
        ROOT / "skills" / "el-jefe-team",
        home / ".agents" / "skills",
    ]
    if args.dirs:
        dirs += [Path(d) for d in args.dirs]

    skills = load_skills(dirs)
    if args.build_index:
        out = ROOT / "skills" / "index.json"
        payload = [
            {
                "name": s["name"],
                "description": s["description"],
                "when": s["when"],
                "dir": s["dir"],
                "chars": s["chars"],
            }
            for s in sorted(skills, key=lambda s: s["name"])
        ]
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"index escrito: {out} ({len(payload)} skills)")
        return 0

    if not args.query.strip():
        ap.error("indica una tarea o usa --build-index")

    q = set(tokenize(args.query))
    qfold = fold(args.query)
    intents = [
        (label, intent_weights(names))
        for label, keywords, names in INTENT_RULES
        if any(k in qfold for k in keywords)
    ]
    ranked = []
    for s in skills:
        sc, hits = score(q, s)
        boosts = [(label, weights[s["name"]]) for label, weights in intents if s["name"] in weights]
        intent_hits = [label for label, _ in boosts]
        if boosts:
            sc += sum(weight for _, weight in boosts)
        if sc > 0:
            ranked.append((sc, hits, intent_hits, s))
    ranked.sort(key=lambda item: (-item[0], item[3]["name"]))

    if args.json:
        print(
            json.dumps(
                [
                    {
                        "skill": s["name"],
                        "score": round(sc, 2),
                        "hits": hits,
                        "intents": intent_hits,
                        "description": s["description"][:200],
                    }
                    for sc, hits, intent_hits, s in ranked[: args.top]
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(f"Tarea: {args.query}\nSkills candidatas (top {args.top}):\n")
    if intents:
        print(f"Intención detectada: {', '.join(label for label, _ in intents)}\n")
    for i, (sc, hits, intent_hits, s) in enumerate(ranked[: args.top], 1):
        print(f"{i}. {s['name']}  (score {sc:.1f})")
        if s["description"]:
            print(f"   {s['description'][:180]}")
        if hits:
            print(f"   coincide: {', '.join(hits[:8])}")
        if intent_hits:
            print(f"   refuerzo de intención: {', '.join(intent_hits)}")
        print()
    if not ranked:
        print("Sin coincidencias. Busca fuera (ver skills/catalog.md) y propón instalar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
