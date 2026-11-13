# El Jefe Stack

![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-blue)
![DSH: DeepSeek Harness](https://img.shields.io/badge/DSH-DeepSeek%20Harness-4b32c3)
![Estado: experimental](https://img.shields.io/badge/estado-experimental-orange)

> **English overview**
> El Jefe Stack configures DeepSeek Harness (DSH) as an orchestrator: a lead agent that interviews
> the brief before planning, delegates to specialist teammates through a shared task board, and asks
> every deliverable for evidence. The repo ships the preset patch, the `el-jefe-team` skill, install
> and validation scripts, and the templates for project memory. It is experimental and not
> affiliated with DeepSeek. Own content is MIT; third-party skills are installed from their
> repositories, never vendored.

## Qué es

Un stack de configuración para [DeepSeek Harness (DSH)](https://github.com/deepseek-ai): convierte el preset `standard` en **El Jefe**, un lead que razona, decide, delega, revisa e integra, y que coordina un equipo de especialistas con el bundle experimental **Agent Team**. El trabajo de implementación lo hacen los especialistas; El Jefe responde del resultado.

El usuario manda. El Jefe manda al equipo, habla con el usuario y mantiene la continuidad del proyecto en disco. Ningún especialista habla directamente con el usuario: sus dudas suben a El Jefe.

Incluye:

- **`preset/el-jefe.patch.yml`**, un override del preset `standard` con persona, permisos, fase 0 y criterio de calidad.
- **`skills/el-jefe-team/`**, el manual de orquestación: roster de 15 especialistas, plantillas de encargo, triaje de skills, puertas de calidad, memoria y criterio.
- **Scripts** de instalación, verificación, validación, enrutado de skills y empaquetado de skills largas.
- **Plantillas** para el estado del proyecto, el glosario, los ADR, la bitácora, la retro y la revisión de acabados.
- Una skill **`threejs`** de 3D web, escrita para este repo, que se nutre de las referencias de un bundle externo al instalarse.

## Qué no es

- **No es un producto oficial de DeepSeek.** DSH es de DeepSeek; este repo es configuración y documentación mantenidas aparte, sin afiliación ni respaldo.
- **No incluye las skills de terceros.** Las de diseño, SEO, marketing, documentación y criterio se instalan desde sus repositorios y conservan su licencia ([`skills/catalog.md`](skills/catalog.md), [`NOTICE.md`](NOTICE.md)).
- **No es estable.** Depende de DSH Desktop y de un bundle experimental, así que una actualización de DSH puede cambiar el formato del preset o de las herramientas. El CHANGELOG cuenta qué se probó en cada versión.
- **No es un framework de código.** Son ficheros de configuración, Markdown y unos scripts de apoyo.

## Cómo funciona

1. **Fase 0: grilling.** Antes de planificar algo no trivial, El Jefe entrevista al usuario por rondas: preguntas numeradas con una respuesta recomendada, un «sí» la acepta, y los hechos los busca él en vez de preguntarlos. Deja el glosario (`GLOSSARY.md`) y los ADR (`docs/adr/`) antes de pasar al plan.
2. **Plan y tablero.** Crea tareas con criterios de aceptación y dependencias en el tablero del equipo; cada especialista reclama la suya y la cierra con evidencia.
3. **Triaje de skills.** Ninguna fase ni entregable sale sin declarar qué skills y herramientas se aplicaron, por qué y con qué evidencia. Se aplican de 1 a 3 (4 o 5 exigen justificación escrita de qué disciplina extra lo pide; más de 5 no se admiten), los descartes se justifican y el reporte termina con un bloque `## Skills y herramientas`. El registro por fase vive en `docs/memoria/40-skills.md` y se valida con `python scripts/skills_check.py <proyecto>`.
4. **Delegación.** Un especialista por pieza disjunta, con brief autocontenido (no ve la conversación de El Jefe) y nombre permanente. Cada miembro escribe en su scope; el Lead revisa e integra.
5. **Permisos.** Lo local y reversible lo aprueba El Jefe. Producción, dinero, datos reales o personales, credenciales, publicación externa e instalaciones globales los decide el usuario, acción por acción, con opciones, impacto y recomendación.
6. **Criterio y acabados.** Antes de entregar, una revisión P0–P3 con nota media de 8 o más, ninguna capa por debajo de 7 y cero P0/P1. Quien construye no firma su propia revisión.
7. **Memoria en disco.** `docs/estado.md` (snapshot corto) más `docs/memoria/`, `GLOSSARY.md` y los ADR. Regla: si no está en disco, no existe. La memoria se actualiza tras cada decisión, antes de compactar y al cerrar sesión.
8. **Sin tope práctico de agentes.** El patch de Agent Team sube el límite del bundle a 1000 entradas de roster. Aun así, cada miembro necesita una pieza disjunta: se reutilizan nombres antes que acumular gente sin trabajo. Si falta una especialidad, se crea el rol con ficha completa y 1 a 3 skills, y se guarda en `agents/custom/` si se va a repetir.
9. **Retro.** Al cerrar, `templates/retro.md`: éxitos que se convierten en workflow y fallos que se convierten en lección. Lo que se repite en dos proyectos se promueve a la ficha de un rol o a una skill.

Detalle técnico: [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md). El manual completo, en [`skills/el-jefe-team/SKILL.md`](skills/el-jefe-team/SKILL.md).

## El equipo

Quince especialistas con nombre permanente. La tabla agrupa algunos por disciplina.

| Especialista | Para qué |
|---|---|
| `movil-ui` / `movil-api` | frontend y backend móvil |
| `web-ui` / `web-api` | frontend y backend web |
| `investigador` | research con fuentes: librerías, APIs, estado del arte |
| `infra` / `seguridad` | CI/CD, cloud y entornos / threat model, authz, secretos |
| `escritor` | READMEs, guías, documentación de API, changelogs, copy |
| `documentador` | bitácora del trabajo: cambios, decisiones, ideas |
| `memoria` | estado del proyecto, glosario y ADR |
| `seo-geo` | SEO técnico y visibilidad en buscadores con IA |
| `marketing` | posicionamiento, copy, conversión, lanzamientos |
| `qa-critico` | pruebas adversariales, regresión, aceptación |
| `disenador-3d` | modelado, PBR, glTF y export |
| `becario` | encargos sueltos que no encajan en nadie |

Fichas, skills preferidas y reglas del roster: [`agents/README.md`](agents/README.md).

## Criterio y acabados

Dos referencias sostienen la capa de decisión y se aplican siempre, sin gastar cupo de triaje:

- **[`criterio.md`](skills/el-jefe-team/references/criterio.md)**: cómo se decide. Jerarquía en conflicto (confianza, accesibilidad, corrección técnica, psicología), negocio (LTV/CAC ≥ 3, payback ≤ 12 meses, ICP con criterios de descarte), psicología ética frente a dark patterns, producto (JTBD, time-to-value, retención por cohorte) y un interrogatorio de 10 preguntas antes de aprobar.
- **[`acabados.md`](skills/el-jefe-team/references/acabados.md)**: cómo se juzga. Review en 8 segundos, capturas a 1440/768/390 con estados forzados, severidad P0–P3, checklist por capas y rúbrica canónica de 0 a 10.

La puerta es la misma para todo: media ≥ 8, ninguna capa < 7, cero P0/P1. La rúbrica, las bandas y la tabla de conversión desde otras escalas están en `acabados.md` §4. Plantilla para no improvisar el veredicto: [`templates/revision-acabados.md`](templates/revision-acabados.md).

## Estructura del repo

```
.
├── agents/                    # Roster y plantilla para crear roles nuevos
├── preset/
│   ├── el-jefe.patch.yml      # Override del preset `standard`
│   ├── agent-team.patch.yml   # Sube el tope de miembros del bundle Agent Team
│   ├── mcp-browseros.example.yml
│   └── README.md
├── skills/
│   ├── el-jefe-team/          # SKILL.md + 21 fichas de referencia + plantilla de revisión
│   ├── threejs/               # Skill paraguas de 3D web
│   └── catalog.md             # Skills externas: repo, licencia y cómo se instalan
├── docs/
│   ├── INSTALL.md             # Instalación paso a paso y troubleshooting
│   ├── ARQUITECTURA.md        # Cómo funciona el equipo por dentro
│   └── CHANGELOG.md
├── templates/                 # estado, memoria, skills-plan, retro, GLOSSARY, ADR, trabajo, revisión
├── scripts/                   # Instalación, verificación y validación
├── CONTRIBUTING.md
├── SECURITY.md
├── NOTICE.md                  # Atribuciones de terceros
├── LICENSE
└── README.md
```

## Requisitos

- **Windows**, el sistema donde está probado. En macOS y Linux los pasos son los mismos cambiando las rutas, pero no se ha probado.
- **DSH Desktop** con el bundle experimental **Agent Team** habilitado. El preset se ha verificado con DSH 0.2.2-rc.1; en versiones anteriores falla por el paquete `tool-subagent-list-agents` (ver el troubleshooting de [`docs/INSTALL.md`](docs/INSTALL.md)).
- **Python 3.11 o superior** con **PyYAML** para los validadores (`python -m pip install pyyaml`). La skill `seo` de terceros pide Python 3.11–3.14 para sus propios scripts.
- **PowerShell** para `scripts/install.ps1` y `scripts/verify.ps1`.
- Opcional: un MCP de navegador (por ejemplo BrowserOS neo) para research y QA web. El ejemplo de configuración está en [`preset/mcp-browseros.example.yml`](preset/mcp-browseros.example.yml).

## Inicio rápido

Cinco pasos. La versión larga, con troubleshooting, está en [`docs/INSTALL.md`](docs/INSTALL.md).

**1. Clona el repo.**

```powershell
git clone https://github.com/fxMT-nx/El-Jefe-Stack.git
cd El-Jefe-Stack
```

**2. Instala la skill del equipo** en `%USERPROFILE%\.agents\skills\el-jefe-team`. Puedes copiar la carpeta a mano o usar el script, que hace copia de seguridad si ya existe:

```powershell
.\scripts\install.ps1 -SkipPreset
```

**3. Aplica el preset.** Haz una copia de `%USERPROFILE%\.dsh\profiles\desktop\cordis.patch.yml` y pega **al final** el contenido de `preset/el-jefe.patch.yml`. Si quieres más de 7 especialistas vivos, pega también `preset/agent-team.patch.yml` y reinicia DSH.

**4. Instala las skills externas** que uses, desde sus repos originales: la lista y los comandos están en [`skills/catalog.md`](skills/catalog.md).

**5. Verifica y arranca.** Comprueba la instalación y crea una sesión nueva:

```powershell
.\scripts\verify.ps1
```

El chip del preset debe decir **El Jefe**. Salúdalo y pídele un proyecto.

`verify.ps1` mira la instalación viva, incluidas las skills externas: si aún no has instalado ninguna, te dirá qué falta con `[FALTA]`. Es información, no un error de la instalación del preset.

## Skills externas

El repo **no vendoriza** las skills de terceros. [`skills/catalog.md`](skills/catalog.md) dice cuáles usa el stack, de qué repositorio vienen, qué aporta cada una y cómo se instalan (`npx skills add owner/repo --skill nombre`, o copiando el directorio a `%USERPROFILE%\.agents\skills\`). Cada una conserva su licencia; las atribuciones están en [`NOTICE.md`](NOTICE.md).

Dos detalles que ahorran tiempo:

- **Skills largas.** En las versiones probadas de DSH, los resultados de herramienta se recortan a 8192 caracteres, así que una skill más larga llega al agente a medias. `python scripts/skill_pack.py --audit` mide y `--split <skill>` trocea el `SKILL.md` en `references/parte-NN-*.md` sin perder texto. `--verify` comprueba el resultado y `--restore` lo deshace.
- **3D web.** `python scripts/install_threejs_skill.py` instala la skill `threejs` de este repo y descarga las referencias del bundle `CloudAI-X/threejs-skills` (MIT), ya troceadas.

## Scripts

| Script | Qué hace |
|---|---|
| `scripts/install.ps1` | Copia la skill a `~/.agents/skills` y añade el preset al patch del perfil, con backups. Admite `-DryRun` y `-SkipPreset`. |
| `scripts/verify.ps1` | Comprueba la instalación viva: ficheros, límites de tamaño, referencias, plantillas y skills externas. |
| `scripts/validate_repo.py` | Valida el repo: YAML del preset y de la skill, enlaces relativos, scripts, protocolo de triaje y empaquetador. Se ejecuta en local antes de enviar un cambio. |
| `scripts/skill_router.py` | Rankea las skills instaladas contra una tarea y explica por qué. |
| `scripts/skills_check.py` | Crea (`--init`) y valida el registro de triaje `docs/memoria/40-skills.md`; `--inventory` lista las skills instaladas. |
| `scripts/skill_pack.py` | Trocea skills largas sin perder texto: `--audit`, `--split`, `--verify`, `--restore`. |
| `scripts/memory_check.py` | Crea (`--init`) y valida la memoria viva de un proyecto. |
| `scripts/install_threejs_skill.py` | Instala la skill `threejs` con sus referencias descargadas y troceadas. |

Ninguno de estos scripts necesita permisos de administrador ni escribe fuera de tu carpeta de usuario y del repo.

## Seguridad y privacidad

- **El preset toca la configuración de DSH.** El paso 3 modifica `cordis.patch.yml`, que decide la persona y las herramientas de tus sesiones. `install.ps1` guarda una copia `*.bak-<fecha>` antes de escribir; si pegas el bloque a mano, haz tú la copia.
- **Sin telemetría.** Los scripts de validación, router, memoria y empaquetado trabajan con ficheros locales. El único que sale a la red es `install_threejs_skill.py`, que descarga documentos de `raw.githubusercontent.com`.
- **Skills de terceros, bajo tu criterio.** Una skill son instrucciones que tu agente sigue: léela antes de instalarla y fija el commit si puedes. Las atribuciones y licencias están en [`NOTICE.md`](NOTICE.md).
- **Vulnerabilidades.** Se reportan en privado por GitHub Security Advisories; el alcance y el proceso están en [`SECURITY.md`](SECURITY.md).

## Estado y compatibilidad

Versión actual: **1.7.3** (ver [`docs/CHANGELOG.md`](docs/CHANGELOG.md)). El proyecto es experimental: el preset depende de DSH Desktop, del bundle Agent Team y de la versión instalada. Se ha probado en Windows con DSH Desktop 0.2.2-rc.1; no hay compromiso de compatibilidad con otras versiones ni con otros sistemas. Si actualizas DSH y algo deja de arrancar, el troubleshooting de [`docs/INSTALL.md`](docs/INSTALL.md) cubre los fallos conocidos.

## Créditos y licencia

- **DeepSeek Harness** y sus paquetes son de DeepSeek. Este repo no está afiliado a DeepSeek.
- **Skills de terceros**: cada una pertenece a su autor y conserva su licencia. La lista con repositorios, licencias y commits está en [`NOTICE.md`](NOTICE.md) y [`skills/catalog.md`](skills/catalog.md).
- **Contenido propio** (preset, skill `el-jefe-team`, scripts, plantillas y documentación): **MIT**, ver [`LICENSE`](LICENSE). La skill `threejs` se apoya en el bundle `CloudAI-X/threejs-skills` (MIT).

## Contribuir

Las propuestas de skills, roles, correcciones y mejoras son bienvenidas. Antes de enviar nada, [`CONTRIBUTING.md`](CONTRIBUTING.md): estándar de fichas, validación obligatoria, estilo de commits y licencia de las contribuciones.
