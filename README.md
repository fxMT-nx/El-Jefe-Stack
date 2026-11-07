# El Jefe Stack

Un stack de **agentes, skills, presets y plantillas** para [DeepSeek Harness (DSH)](https://github.com/deepseek-ai) que convierte a un agente en **El Jefe**: un lead que razona, decide, delega, revisa e integra —sin implementar— y que coordina un equipo de 15 especialistas con el plugin Agent Team.

El usuario manda. El Jefe manda al equipo. Y el Jefe habla conmigo, nunca al revés.

## Qué incluye

```
.
├── agents/                 # Roster + plantilla para crear agentes nuevos
├── preset/
│   ├── el-jefe.patch.yml   # Override del preset `standard` (persona + herramientas)
│   ├── mcp-browseros.example.yml
│   └── README.md
├── skills/
│   ├── el-jefe-team/       # Skill de orquestación (SKILL.md + references/)
│   ├── threejs/            # Paraguas 3D web (instalable con scripts/install_threejs_skill.py)
│   └── catalog.md          # Skills externas, de dónde vienen y cómo se instalan
├── docs/
│   ├── INSTALL.md          # Instalación paso a paso y troubleshooting
│   ├── ARQUITECTURA.md     # Cómo funciona el equipo por dentro
│   └── CHANGELOG.md
├── templates/              # estado.md (snapshot), memoria/, skills-plan, retro, GLOSSARY, ADR, bitácora, revisión de acabados
├── scripts/
│   ├── install.ps1         # Instala skill + aplica el preset (con backups)
│   ├── verify.ps1          # Comprueba que todo está en su sitio
│   ├── skill_router.py     # Ranking explicable de skills para una tarea
│   ├── skills_check.py     # Valida/inicializa el triaje de skills (40-skills) e inventaría el catálogo
│   ├── skill_pack.py       # Trocea las skills largas (>8192) para que no se trunquen al cargarlas
│   └── memory_check.py     # Valida/inicializa la memoria viva de un proyecto
└── LICENSE
```

## Equipo

| Especialista | Para qué |
|---|---|
| `movil-ui` / `movil-api` | frontend y backend móvil |
| `web-ui` / `web-api` | frontend y backend web |
| `investigador` | research con fuentes (librerías, APIs, estado del arte) |
| `infra` / `seguridad` | CI/CD, cloud, entornos / threat model, authz, secretos |
| `escritor` | READMEs, guías, docs de API, changelogs, copy |
| `documentador` | bitácora del trabajo: cambios, decisiones e ideas |
| `memoria` | estado del proyecto, glosario y ADR |
| `seo-geo` | SEO técnico y visibilidad en buscadores con IA |
| `marketing` | posicionamiento, copy, CRO, lanzamientos |
| `qa-critico` | pruebas adversariales, regresión, aceptación |
| `disenador-3d` | modelado, PBR, glTF y export |
| `becario` | encargos sueltos que no encajan en nadie |

Detalle completo en [`agents/README.md`](agents/README.md).

## Cómo trabaja

1. **Fase 0 — Grilling.** Antes de planificar algo no trivial, El Jefe te interroga por rondas (`grilling`): preguntas numeradas con su respuesta recomendada, un "sí" la acepta, y los hechos los busca él con subagentes. No se avanza hasta entendimiento compartido.
2. **Plan y tablero.** Crea tareas con criterios de aceptación y dependencias en el tablero del equipo.
3. **Triaje obligatorio.** Ninguna fase ni entregable sin triaje explícito de skills y herramientas: se revisa el catálogo real, se aplican 1–3, se justifican descartes y se exige evidencia en el reporte (`## Skills y herramientas`). El registro por fase vive en `docs/memoria/40-skills.md` y se valida con `python scripts/skills_check.py <proyecto>`. Fase sin skill y sin waiver aprobado = fallo de proceso. Detalle: `skills/el-jefe-team/references/triaje-skills.md`.
4. **Delegación.** Un especialista por pieza, scopes de escritura disjuntos; FE y BE contra el contrato. Teammates sin tope práctico: el perfil admite hasta 1000 entradas de roster (antes 8).
5. **Calidad.** QA crítico, seguridad e infra revisan antes de entregar.
6. **Memoria.** `docs/estado.md`, `GLOSSARY.md` y ADR en `docs/adr/` para que el proyecto se pueda retomar en otra sesión.
7. **Permisos.** Los especialistas piden permiso a El Jefe; lo rojo o excepcional te lo pregunta él a ti. Detalle en `skills/el-jefe-team/references/permisos.md`.
8. **Agentes bajo demanda.** Si falta una especialidad, El Jefe **crea el rol que hace falta**: ficha completa (misión, brief, entregable, checklist, límites), 1–3 skills elegidas o buscadas e instaladas, y brief autocontenido. Si el rol se reutiliza, su ficha vive en `agents/custom/`. Procedimiento y dónde buscar skills: `skills/el-jefe-team/references/agentes-nuevos.md`.
9. **Router de skills.** Antes de encargar, el equipo puede rankear las skills instaladas contra la tarea: `python scripts/skill_router.py "<tarea>"` (mecánica de recuperación inspirada en Skill-3D). Declara la combinación elegida.
10. **Retro y aprendizaje.** Al cerrar un proyecto, `templates/retro.md`: éxitos → workflows a repetir, fallos → lecciones correctivas. Lo repetido en ≥2 proyectos se promueve a la ficha del rol, a la matriz o a una skill nueva. Detalle: `skills/el-jefe-team/references/aprendizaje.md`.

## Criterio y acabados

El equipo no solo ejecuta: **decide y rechaza**. Dos referencias nuevas sostienen esa capa y se aplican a cualquier entrega, sin gastar cupo de triaje:

- `skills/el-jefe-team/references/criterio.md` — **cómo se decide**: jerarquía cuando hay conflicto (**confianza → accesibilidad → corrección técnica → psicología**), negocio (SBA, ICP con disqualifying, unit economics LTV/CAC ≥ 3 y payback ≤ 12 meses), psicología ética frente a dark patterns, producto (JTBD, time-to-value, retención por cohorte), decisiones (rúbrica 0–10, muestra precomprometida, una sola fuente de verdad) y un interrogatorio de 10 preguntas antes de aprobar.
- `skills/el-jefe-team/references/acabados.md` — **lo que el usuario juzga**: lo que se nota sin poder nombrarlo. Review en 8 segundos, capturas a 1440/768/390 con estados forzados, severidad **P0–P3**, checklist por capas y rúbrica. Se publica con **media ≥ 8**, **ninguna capa < 7** y **cero P0/P1**; «se ve bien» no es una revisión.
- Plantilla para no improvisar el veredicto: `templates/revision-acabados.md`.
- Puerta por entregable y anti-patrones: `skills/el-jefe-team/references/puertas-calidad.md`.

## Skills sin truncar (`skill_pack.py`)

El pruner de sesión recorta los resultados de herramienta a **8.192 caracteres**: una skill más larga llegaba al agente a medias y el agente no veía las reglas del medio. `scripts/skill_pack.py` lo arregla troceando la skill, no recortándola:

```bash
python scripts/skill_pack.py --audit                      # tamaño y estado de cada skill
python scripts/skill_pack.py --split <skill> [--inline "Encabezado"]
python scripts/skill_pack.py --verify                     # límites, partes e índice
python scripts/skill_pack.py --restore <skill>            # deshace el troceo
```

Deja en `SKILL.md` frontmatter, intro, las reglas clave y un índice con enlaces relativos; el cuerpo va a `references/parte-NN-<slug>.md` (≤7.000 caracteres) y el original se conserva en `references/00-original.md`. No duplica ni pierde texto: cada sección acaba en un solo sitio y el script lo comprueba antes de escribir. En la v1.6.0 pasaron de 43 skills por encima del límite a **0 de 84**.

## Memoria viva

El Jefe es el dueño último de la memoria; `memoria` la escribe y `documentador` deja la bitácora. Regla: **si no está en disco, no existe**.

- `docs/estado.md` — snapshot ≤1.5 KB (objetivo, fase, hecho, siguiente, decisiones vigentes, riesgos, preguntas, cómo retomar).
- `docs/memoria/` — `00-indice`, `10-proyecto`, `20-usuario` (preferencias, vetos y aprobaciones del usuario), `30-decisiones`, `40-skills` (triaje obligatorio por fase), `50-tecnico`, `60-tareas`, `70-riesgos`, `80-preguntas`, `90-historial` (una entrada por sesión).
- `GLOSSARY.md`, `docs/adr/`, `docs/trabajo.md`, `CHANGELOG.md`, `docs/ideas.md` — vocabulario, decisiones duras y bitácora.

Protocolo: leer al arrancar, actualizar tras cada decisión, **antes de compactar** y al cerrar sesión. Detalle en `skills/el-jefe-team/references/memoria-viva.md`; validación con `python scripts/memory_check.py <proyecto>` (`--init` crea el esqueleto, incluido `40-skills.md`) y `python scripts/skills_check.py <proyecto>` para el triaje de skills.

## Inicio rápido

1. Copia `skills/el-jefe-team/` en `~/.agents/skills/` (o ejecuta `scripts/install.ps1`).
2. Añade el bloque de `preset/el-jefe.patch.yml` al final de tu `cordis.patch.yml` de perfil.
3. Reinicia DSH (o deja que el HMR recargue).
4. Crea una sesión nueva: el chip debe decir **El Jefe**. Salúdalo y pídele un proyecto.

Instalación detallada: [`docs/INSTALL.md`](docs/INSTALL.md).

## Requisitos

- DSH Desktop (probado con perfil `desktop` y el bundle experimental **Agent Team** habilitado).
- Skills de entrevista (`grilling`, `grill-me`, `grill-with-docs`, `domain-modeling`) y las de `skills/catalog.md`.
- Opcional: MCP de navegador (BrowserOS neo) para research y QA web.

## Licencia

MIT para el contenido propio. Las skills de terceros no se vendorizan aquí: se instalan desde sus repos originales (ver `skills/catalog.md`), cada una con su licencia.
