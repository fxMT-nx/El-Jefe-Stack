# Catálogo de skills

El repo incluye la skill propia (`el-jefe-team`). Las externas **no se vendorizan**: se instalan desde sus repos originales con `npx skills add owner/repo --skill nombre` o copiando el directorio a `~/.agents/skills/`. Licencias verificadas de los repos usados: MIT (ver excepciones al final).

## Entrevistas y modelo del dominio (fase 0)

| Skill | Repo | Aporta |
|---|---|---|
| `grilling` | `mattpocock/skills` | entrevista por rondas con respuestas recomendadas; hechos por subagentes |
| `grill-me` | `mattpocock/skills` | atajo manual del usuario (`disable-model-invocation`) |
| `grill-with-docs` | `mattpocock/skills` | `grilling` + `domain-modeling` |
| `domain-modeling` | `mattpocock/skills` | glosario del dominio + ADR |
| `architecture-decision-records` | `wshobson/agents` | formato y mantenimiento de ADRs |

## Diseño y animación

| Skill | Repo |
|---|---|
| `emil-design-eng`, `find-animation-opportunities`, `apple-design` | `emilkowalski/skills` |
| `motion-design` | `LottieFiles/motion-design-skill` |
| `ui-animation` | `mblode/agent-skills` |
| `frontend-design`, `algorithmic-art`, `canvas-design` | `anthropics/skills` |
| `antfu-web-design-guidelines` | `JetBrains/skills` |

## 3D web

| Skill | Repo | Aporta |
|---|---|---|
| `threejs` | `CloudAI-X/threejs-skills` (MIT, ~3.9k★, r186) | bundle de 13 docs (fundamentals, geometry, materials, textures, lighting, loaders, asset-pipeline, animation, interaction, shaders, postprocessing, performance, R3F). Aquí se instala como **skill paraguas** con 53 referencias troceadas: `python scripts/install_threejs_skill.py` |

## SEO/GEO, marketing y contenido

| Skill | Repo | Aporta |
|---|---|---|
| `seo`, `seo-technical`, `seo-content`, `seo-schema`, `seo-geo` | `AgriciDaniel/claude-seo` | auditoría SEO/GEO, schema, contenido citable (el hub `seo` trae runtime Python) |
| `product-marketing`, `copywriting`, `cro`, `emails`, `launch` | `coreyhaines31/marketingskills` | posicionamiento, copy, conversión, email y lanzamiento |

## Documentación y calidad

| Skill | Repo | Aporta |
|---|---|---|
| `changelog-automation`, `architecture-decision-records` | `wshobson/agents` | changelog y ADR |
| `code-review-and-quality`, `code-simplification` | `addyosmani/agent-skills` | revisión multi-eje y simplificación |
| `install-anti-slop` | `dmmulroy/anti-slop` | reglas Oxlint contra patrones de código generado por IA |

## Criterio, negocio y acabados (v1.6.0)

Las 17 skills que sostienen la capa de criterio: negocio, psicología, posicionamiento, precio, oferta, usabilidad y acabado visual. **Vendorizadas** en `~/.agents/skills/<nombre>/` con su `SOURCE.md` (repo, commit, licencia, fecha) y el `LICENSE` del repo al lado. Las cuatro licencias verificadas: **MIT**.

| Skill | Repo | Commit | Aporta |
|---|---|---|---|
| `copy-editing` | `coreyhaines31/marketingskills` | `88c79f65` | editar copy existente, quitar slop de IA |
| `marketing-psychology` | `coreyhaines31/marketingskills` | `88c79f65` | sesgos y modelos mentales aplicados a marketing |
| `analytics` | `coreyhaines31/marketingskills` | `88c79f65` | plan de medición, eventos, UTMs, qué se mide |
| `attribution` | `coreyhaines31/marketingskills` | `88c79f65` | modelos de atribución y reconciliar números que no cuadran |
| `customer-research` | `coreyhaines31/marketingskills` | `88c79f65` | entrevistas, VOC, personas, minería de reviews |
| `ux-heuristics` | `wondelai/skills` | `d8d5d75f` | Nielsen + leyes de Krug, severidad, dark patterns |
| `obviously-awesome` | `wondelai/skills` | `d8d5d75f` | posicionamiento (canvas, categoría, alternativas) |
| `influence-psychology` | `wondelai/skills` | `d8d5d75f` | 7 principios de persuasión ética |
| `jobs-to-be-done` | `wondelai/skills` | `d8d5d75f` | el trabajo que contrata al producto |
| `monetizing-innovation` | `wondelai/skills` | `d8d5d75f` | willingness to pay, packaging, good-better-best |
| `improve-retention` | `wondelai/skills` | `d8d5d75f` | activación, cohortes, B=MAP |
| `founder-cfo` | `Jakeschincariol/founder-skill` | `fd9385b0` | unit economics, margen, break-even, caja |
| `founder-pricing` | `Jakeschincariol/founder-skill` | `fd9385b0` | Van Westendorp, escalera de precios |
| `founder-offer` | `Jakeschincariol/founder-skill` | `fd9385b0` | oferta, bonos, garantía, urgencia honesta |
| `taste-design-review` | `madebymustafa/design-taste` | `c4a6bff0` | review visual P0–P3 con capturas |
| `taste-ux-copy` | `madebymustafa/design-taste` | `c4a6bff0` | microcopy: botones, errores, vacíos |
| `taste-accessibility` | `madebymustafa/design-taste` | `c4a6bff0` | WCAG 2.2 AA dentro de la generación |

Instalación de estas 17 (clon superficial y copia del directorio, verificando `name`/`description` del frontmatter):

```powershell
$t = Join-Path $env:TEMP 'jefe-skills'
git clone --depth 1 https://github.com/coreyhaines31/marketingskills.git "$t/corey"
git clone --depth 1 https://github.com/wondelai/skills.git "$t/wondelai"
git clone --depth 1 https://github.com/Jakeschincariol/founder-skill.git "$t/founder"
git clone --depth 1 https://github.com/madebymustafa/design-taste.git "$t/mustafa"
# copiar "skills/<nombre>" (o "<nombre>" en wondelai) a ~/.agents/skills/<nombre>/ + SOURCE.md
```

## Empaquetado de skills largas (`scripts/skill_pack.py`)

El pruner de sesión recorta los resultados de herramienta a **8.192 caracteres**: una skill más larga llegaba al agente truncada. El packer trocea en vez de recortar y deja un índice navegable.

```bash
python scripts/skill_pack.py --audit      # antes/después: 84 skills, 43 superaban el límite → 0
python scripts/skill_pack.py --verify     # límites, partes e índice
python scripts/skill_pack.py --split apple-design
python scripts/skill_pack.py --split copywriting --inline "No AI Tells"
python scripts/skill_pack.py --restore apple-design
```

- **Antes** (v1.5.2, 67 skills): 34 superaban 8.192 caracteres. **Al instalar las 17** (84 skills): 43. **Después del troceo: 0 de 84.**
- **Troceadas (43)**: `algorithmic-art`, `analytics`, `animate`, `animation-vocabulary`, `apple-design`, `attribution`, `canvas-design`, `code-review-and-quality`, `code-simplification`, `copy-editing`, `copywriting`, `customer-research`, `design-taste-frontend`, `emails`, `emil-design-eng`, `find-animation-opportunities`, `frontend-design`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-core`, `hyperframes-keyframes`, `improve-retention`, `influence-psychology`, `install-anti-slop`, `jobs-to-be-done`, `launch`, `marketing-psychology`, `monetizing-innovation`, `motion-design`, `obviously-awesome`, `product-launch-video`, `product-marketing`, `review-animations`, `security-best-practices`, `seo`, `seo-content`, `seo-geo`, `seo-technical`, `ui-animation`, `ui-design`, `ui-verification`, `ux-heuristics`, `writing-plans`.
- **Con `--inline`** (sección crítica que no puede perderse): `copywriting` → «No AI Tells»; `product-marketing` → «Sections to Capture» (dentro están «Objections & Anti-Personas» y «Proof Points»).
- Cada troceo deja `SKILL.md` + `references/parte-NN-<slug>.md` + `references/00-original.md`; la instalación original no se pierde y `--restore` la devuelve byte a byte.

## Instalación en bloque

```bash
npx skills add mattpocock/skills --skill grilling
npx skills add mattpocock/skills --skill grill-me
npx skills add mattpocock/skills --skill grill-with-docs
npx skills add mattpocock/skills --skill domain-modeling
npx skills add AgriciDaniel/claude-seo
npx skills add coreyhaines31/marketingskills
npx skills add wshobson/agents
npx skills add addyosmani/agent-skills
npx skills add dmmulroy/anti-slop
```

## Notas

- **`grill-me` y `grill-with-docs`** llevan `disable-model-invocation: true`: solo los invoca el usuario; para automático usa `grilling`.
- **Runtime de `seo`**: scripts Python (3.11–3.14) con `CLAUDE_PLUGIN_ROOT=~/.agents/skills/seo`.
- **`canvas-design`** incluye fuentes .ttf (~5.5 MB).
- `mattpocock/skills`, `obra/superpowers`, `AgriciDaniel/claude-seo`, `coreyhaines31/marketingskills`, `wshobson/agents`, `addyosmani/agent-skills` y `dmmulroy/anti-slop` declaran licencias permisivas (MIT en la verificación de estos repos). Respeta la licencia de cada repo si redistribuyes.
- Fuentes para buscar más: `skillsagents.com`, `ComposioHQ/awesome-claude-skills`, `hesreallyhim/awesome-claude-code`, `VoltAgent/awesome-claude-code-subagents`, `ykdojo/claude-code-tips` y el índice `kraayenjon/agent-skills-es`.
