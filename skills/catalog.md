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
