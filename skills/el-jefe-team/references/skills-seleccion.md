# Skills: triaje obligatorio y selección

## Ley de triaje

Ninguna fase, tarea ni entregable sin **triaje explícito** de skills y herramientas: "no aplica" se decide y se escribe, nunca se olvida. Nombrar una skill sin leerla no cuenta; usarla es cargarla y aplicar sus reglas. El protocolo completo —T-R-I-A-J-E, mínimos por tipo de trabajo, waivers, evidencia y puerta de El Jefe— está en [triaje-skills.md](triaje-skills.md). Esta página aporta la matriz de afinidad, el catálogo y las fuentes de descubrimiento.

## Principios

- **La matriz orienta; el mínimo obliga.** Cualquier especialista puede usar otra skill si encaja mejor, pero los mínimos de `triaje-skills.md` por tipo de trabajo no son opcionales: UI nueva exige diseño **y** verificación; datos y auth exigen seguridad **y** pruebas.
- **Elegir por tarea, no por costumbre.** Antes de actuar: entiende el encargo, revisa el catálogo **real** instalado (`python scripts/skills_check.py --inventory`) y elige **1–3 complementarias**. No cargues cinco skills redundantes.
- **Declarar con evidencia.** El reporte lleva el bloque `## Skills y herramientas` con tabla `skill | por qué | dónde se aplicó | resultado`, las descartadas y los waivers. Sin bloque, El Jefe devuelve el entregable.
- **Combinar.** Una tarea real suele abarcar varias: p. ej. una landing = `frontend-design` + `design-taste-frontend` + `motion-design` + `ui-verification` + (si toca publicar) `seo-geo`/`marketing`.
- **Cuando no haya skill que encaje:** búscala en las fuentes de descubrimiento de abajo y propón su instalación a El Jefe antes de improvisar.

## Mínimos por fase (resumen)

| Fase | Mínimo |
|---|---|
| Fase 0 / plan | `grilling` (+ `writing-plans` al planificar) y mapa de skills en `docs/memoria/40-skills.md` |
| Diseño / UI | 1 skill de diseño + 1 de verificación (`ui-verification`/`webapp-testing`/`web-design-guidelines`) |
| Construcción API/BD | `security-best-practices`/`supabase-postgres-best-practices` + `vitest` |
| Seguridad | `security-threat-model` + `security-best-practices` |
| Deploy / publicación | `playwright`/`vitest` (smoke) + `seo-geo`/`marketing` si hay visibilidad |
| Entrega / documentación | `office-*`/`changelog-automation`/`brand` según el entregable |

Detalle por tipo de trabajo, ejemplos y waivers: [triaje-skills.md](triaje-skills.md). Validación del registro: `python scripts/skills_check.py <proyecto>`.

## Matriz de afinidad

| Rol | Skills preferidas (no exclusivas) |
|---|---|
| El Jefe | `grilling`, `grill-with-docs`, `domain-modeling`, `el-jefe-team` (obligatoria al empezar), `writing-plans` (planificar), `brand` (tono de producto) |
| `movil-ui` | `apple-design` (iOS), `ui-animation`, `motion-design`, `ui-design`, `frontend-design`, `emil-design-eng`, `design-taste-frontend`, `modern-web-guidance`, `find-animation-opportunities`, `review-animations` |
| `movil-api` | `supabase-postgres-best-practices`, `security-best-practices`, `vitest` (móvil/backend), `playwright` (e2e) |
| `web-ui` | `design-taste-frontend`, `frontend-design`, `ui-design`, `apple-design`, `emil-design-eng`, `motion-design`, `ui-animation`, `animate`, `animation-vocabulary`, `find-animation-opportunities`, `improve-animations`, `review-animations`, `web-design-guidelines` o `antfu-web-design-guidelines`, `modern-web-guidance`, `vercel-react-best-practices`, `vite`, `vitest`, `ui-verification`, `webapp-testing`, `code-simplification`, `threejs` (3D web), `algorithmic-art`/`canvas-design` (assets visuales) |
| `web-api` | `supabase-postgres-best-practices`, `security-best-practices`, `vitest`, `playwright`, `modern-web-guidance` (APIs web), `code-review-and-quality`, `code-simplification` |
| `investigador` | `browseros-neo`, `playwright`, `webapp-testing`, `modern-web-guidance`; fuentes de descubrimiento de abajo |
| `infra` | `security-best-practices`, `security-threat-model`, `playwright` (smoke e2e), `vitest` |
| `seguridad` | `security-threat-model`, `security-best-practices`, `supabase-postgres-best-practices` (RLS), `playwright` (authz), `browseros-neo` (exposición web) |
| `escritor` | `brand` (voz), `copywriting` (copy), `office-*` (entregables), `changelog-automation` (notas de release) |
| `documentador` | `changelog-automation`, `domain-modeling` (términos), `architecture-decision-records`, `office-*` (informes), `writing-plans` |
| `memoria` | `domain-modeling` (glosario + ADR), `architecture-decision-records`, `writing-plans`, `office-*` (resúmenes) |
| `seo-geo` | `seo`, `seo-technical`, `seo-content`, `seo-schema`, `seo-geo`, `ui-verification` (CWV), `webapp-testing`/`playwright` (render), `browseros-neo` (SERP y visibilidad IA), `modern-web-guidance` |
| `marketing` | `product-marketing`, `copywriting`, `cro`, `emails`, `launch`, `brand`, `design-taste-frontend` (landing), `product-launch-video`, `media-use`, `browseros-neo` (competencia), `office-*` |
| `qa-critico` | `code-review-and-quality`, `playwright`, `webapp-testing`, `ui-verification`, `vitest`, `agent-desktop` (apps de escritorio), `security-best-practices` (casos de abuso) |
| `disenador-3d` | `media-use`, `motion-design`, `hyperframes-animation` (cámara/motion), `canvas-design`, `algorithmic-art`, `threejs` (visor/3D web) |
| `becario` | `agent-desktop`, `office-*`, `browseros-neo`, `playwright`; cualquier otra según el encargo |

> Nota: `web-design-guidelines`, `antfu-web-design-guidelines` y `vercel-labs-web-design-guidelines` se solapan (las dos primeras comparten `name:` y el catálogo solo registra una). Usa la que esté disponible y, si hace falta la otra, léela del directorio `~/.agents/skills/...` directamente.

## Grilling (fase 0 del proyecto)

`grilling` es el motor de entrevista: árbol de decisiones, rondas de preguntas numeradas con respuesta recomendada (un "sí" la acepta), hechos buscados por subagentes y parada hasta entendimiento compartido. `grill-me` es el atajo manual; `grill-with-docs` = `grilling` + `domain-modeling`, que además deja `GLOSSARY.md` y ADR en `docs/adr/`.

- **Quién:** solo el Lead (El Jefe) interroga al usuario; los teammates no hablan con él directamente.
- **Cuándo:** fase 0 de todo proyecto o feature no trivial, antes de `writing-plans`; también cuando el usuario diga "grill-me", "interrógame" o "estresa esto".
- **Salida:** decisiones cerradas, glosario actualizado y, si aplica, ADR; después se pasa al protocolo de proyecto.
- **Regla:** no se implementa ni se planifica a fondo hasta que el usuario confirme el entendimiento compartido.

## Descubrimiento de skills (cuando no hay una instalada)

Fuentes donde buscar antes de inventar:

- **skillsagents.com** — directorio en español, 1.800+ skills y MCP con buscador y ranking.
- **github.com/ComposioHQ/awesome-claude-skills** — la lista awesome más grande.
- **github.com/hesreallyhim/awesome-claude-code** — recursos seleccionados a mano.
- **github.com/VoltAgent/awesome-claude-code-subagents** — 100+ subagentes especializados.
- **github.com/ykdojo/claude-code-tips** — trucos y patrones.
- **github.com/kraayenjon/agent-skills-es** — índice en español de repos con skills.

**Cómo buscar:** describe la tarea en 3–5 palabras clave (p. ej. "SEO técnico schema", "CRO pricing copy"), busca en esas fuentes y en GitHub (`topic:agent-skills`, `claude skill <tema>`), y compara 2–3 candidatos por licencia, estrellas, mantenimiento y calidad del SKILL.md.

**Cómo instalar:** preferible `npx skills add owner/repo --skill nombre`; si no, clon shallow y copia el directorio de skill a `~/.agents/skills/<nombre>/` verificando frontmatter (`name:` y `description:`).

**Procedencia de lo instalado:** las skills SEO/GEO, marketing, documentación y calidad vienen de `AgriciDaniel/claude-seo` (MIT), `coreyhaines31/marketingskills` (MIT), `wshobson/agents` (MIT), `addyosmani/agent-skills` (MIT) y `dmmulroy/anti-slop`. `grilling`, `grill-me`, `grill-with-docs` y `domain-modeling` vienen de `mattpocock/skills` (MIT). El repo `kraayenjon/agent-skills-es` resultó ser un **índice**, no un pack de skills: se usa como fuente de descubrimiento, no como origen.

**Permisos:** instalar una skill local es zona 🟡 para el especialista que la propone (la aprueba El Jefe). Si implica instalar software global, tocar el sistema o una licencia dudosa, El Jefe te lo consulta antes (🔴).
