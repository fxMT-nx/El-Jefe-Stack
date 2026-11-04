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
│   └── catalog.md          # Skills externas, de dónde vienen y cómo se instalan
├── docs/
│   ├── INSTALL.md          # Instalación paso a paso y troubleshooting
│   ├── ARQUITECTURA.md     # Cómo funciona el equipo por dentro
│   └── CHANGELOG.md
├── templates/              # estado.md, GLOSSARY.md, ADR, bitácora
├── scripts/
│   ├── install.ps1         # Instala skill + aplica el preset (con backups)
│   ├── verify.ps1          # Comprueba que todo está en su sitio
│   └── skill_router.py     # Ranking explicable de skills para una tarea
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
3. **Delegación.** Un especialista por pieza, scopes de escritura disjuntos; FE y BE contra el contrato. Máximo 7 teammates vivos (límite del perfil).
4. **Calidad.** QA crítico, seguridad e infra revisan antes de entregar.
5. **Memoria.** `docs/estado.md`, `GLOSSARY.md` y ADR en `docs/adr/` para que el proyecto se pueda retomar en otra sesión.
6. **Permisos.** Los especialistas piden permiso a El Jefe; lo rojo o excepcional te lo pregunta él a ti. Detalle en `skills/el-jefe-team/references/permisos.md`.
7. **Agentes bajo demanda.** Si falta una especialidad, El Jefe **crea el rol que hace falta**: ficha completa (misión, brief, entregable, checklist, límites), 1–3 skills elegidas o buscadas e instaladas, y brief autocontenido. Si el rol se reutiliza, su ficha vive en `agents/custom/`. Procedimiento y dónde buscar skills: `skills/el-jefe-team/references/agentes-nuevos.md`.
8. **Router de skills.** Antes de encargar, el equipo puede rankear las skills instaladas contra la tarea: `python scripts/skill_router.py "<tarea>"` (mecánica de recuperación inspirada en Skill-3D). Declara la combinación elegida.
9. **Retro y aprendizaje.** Al cerrar un proyecto, `templates/retro.md`: éxitos → workflows a repetir, fallos → lecciones correctivas. Lo repetido en ≥2 proyectos se promueve a la ficha del rol, a la matriz o a una skill nueva. Detalle: `skills/el-jefe-team/references/aprendizaje.md`.

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
