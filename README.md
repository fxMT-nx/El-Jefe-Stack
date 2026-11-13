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

## QuÃ© es

Un stack de configuraciÃ³n para [DeepSeek Harness (DSH)](https://github.com/deepseek-ai): convierte el preset `standard` en **El Jefe**, un lead que razona, decide, delega, revisa e integra, y que coordina un equipo de especialistas con el bundle experimental **Agent Team**. El trabajo de implementaciÃ³n lo hacen los especialistas; El Jefe responde del resultado.

El usuario manda. El Jefe manda al equipo, habla con el usuario y mantiene la continuidad del proyecto en disco. NingÃºn especialista habla directamente con el usuario: sus dudas suben a El Jefe.

Incluye:

- **`preset/el-jefe.patch.yml`**, un override del preset `standard` con persona, permisos, fase 0 y criterio de calidad.
- **`skills/el-jefe-team/`**, el manual de orquestaciÃ³n: roster de 15 especialistas, plantillas de encargo, triaje de skills, puertas de calidad, memoria y criterio.
- **Scripts** de instalaciÃ³n, verificaciÃ³n, validaciÃ³n, enrutado de skills y empaquetado de skills largas.
- **Plantillas** para el estado del proyecto, el glosario, los ADR, la bitÃ¡cora, la retro y la revisiÃ³n de acabados.
- Una skill **`threejs`** de 3D web, escrita para este repo, que se nutre de las referencias de un bundle externo al instalarse.

## QuÃ© no es

- **No es un producto oficial de DeepSeek.** DSH es de DeepSeek; este repo es configuraciÃ³n y documentaciÃ³n mantenidas aparte, sin afiliaciÃ³n ni respaldo.
- **No incluye las skills de terceros.** Las de diseÃ±o, SEO, marketing, documentaciÃ³n y criterio se instalan desde sus repositorios y conservan su licencia ([`skills/catalog.md`](skills/catalog.md), [`NOTICE.md`](NOTICE.md)).
- **No es estable.** Depende de DSH Desktop y de un bundle experimental, asÃ­ que una actualizaciÃ³n de DSH puede cambiar el formato del preset o de las herramientas. El CHANGELOG cuenta quÃ© se probÃ³ en cada versiÃ³n.
- **No es un framework de cÃ³digo.** Son ficheros de configuraciÃ³n, Markdown y unos scripts de apoyo.

## CÃ³mo funciona

1. **Fase 0: grilling.** Antes de planificar algo no trivial, El Jefe entrevista al usuario por rondas: preguntas numeradas con una respuesta recomendada, un Â«sÃ­Â» la acepta, y los hechos los busca Ã©l en vez de preguntarlos. Deja el glosario (`GLOSSARY.md`) y los ADR (`docs/adr/`) antes de pasar al plan.
2. **Plan y tablero.** Crea tareas con criterios de aceptaciÃ³n y dependencias en el tablero del equipo; cada especialista reclama la suya y la cierra con evidencia.
3. **Triaje de skills.** Ninguna fase ni entregable sale sin declarar quÃ© skills y herramientas se aplicaron, por quÃ© y con quÃ© evidencia. Se aplican de 1 a 3 (4 o 5 exigen justificaciÃ³n escrita de quÃ© disciplina extra lo pide; mÃ¡s de 5 no se admiten), los descartes se justifican y el reporte termina con un bloque `## Skills y herramientas`. El registro por fase vive en `docs/memoria/40-skills.md` y se valida con `python scripts/skills_check.py <proyecto>`.
4. **DelegaciÃ³n.** Un especialista por pieza disjunta, con brief autocontenido (no ve la conversaciÃ³n de El Jefe) y nombre permanente. Cada miembro escribe en su scope; el Lead revisa e integra.
5. **Permisos.** Lo local y reversible lo aprueba El Jefe. ProducciÃ³n, dinero, datos reales o personales, credenciales, publicaciÃ³n externa e instalaciones globales los decide el usuario, acciÃ³n por acciÃ³n, con opciones, impacto y recomendaciÃ³n.
6. **Criterio y acabados.** Antes de entregar, una revisiÃ³n P0â€“P3 con nota media de 8 o mÃ¡s, ninguna capa por debajo de 7 y cero P0/P1. Quien construye no firma su propia revisiÃ³n.
7. **Memoria en disco.** `docs/estado.md` (snapshot corto) mÃ¡s `docs/memoria/`, `GLOSSARY.md` y los ADR. Regla: si no estÃ¡ en disco, no existe. La memoria se actualiza tras cada decisiÃ³n, antes de compactar y al cerrar sesiÃ³n.
8. **Sin tope prÃ¡ctico de agentes.** El patch de Agent Team sube el lÃ­mite del bundle a 1000 entradas de roster. Aun asÃ­, cada miembro necesita una pieza disjunta: se reutilizan nombres antes que acumular gente sin trabajo. Si falta una especialidad, se crea el rol con ficha completa y 1 a 3 skills, y se guarda en `agents/custom/` si se va a repetir.
9. **Retro.** Al cerrar, `templates/retro.md`: Ã©xitos que se convierten en workflow y fallos que se convierten en lecciÃ³n. Lo que se repite en dos proyectos se promueve a la ficha de un rol o a una skill.

Detalle tÃ©cnico: [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md). El manual completo, en [`skills/el-jefe-team/SKILL.md`](skills/el-jefe-team/SKILL.md).

## El equipo

Quince especialistas con nombre permanente. La tabla agrupa algunos por disciplina.

| Especialista | Para quÃ© |
|---|---|
| `movil-ui` / `movil-api` | frontend y backend mÃ³vil |
| `web-ui` / `web-api` | frontend y backend web |
| `investigador` | research con fuentes: librerÃ­as, APIs, estado del arte |
| `infra` / `seguridad` | CI/CD, cloud y entornos / threat model, authz, secretos |
| `escritor` | READMEs, guÃ­as, documentaciÃ³n de API, changelogs, copy |
| `documentador` | bitÃ¡cora del trabajo: cambios, decisiones, ideas |
| `memoria` | estado del proyecto, glosario y ADR |
| `seo-geo` | SEO tÃ©cnico y visibilidad en buscadores con IA |
| `marketing` | posicionamiento, copy, conversiÃ³n, lanzamientos |
| `qa-critico` | pruebas adversariales, regresiÃ³n, aceptaciÃ³n |
| `disenador-3d` | modelado, PBR, glTF y export |
| `becario` | encargos sueltos que no encajan en nadie |

Fichas, skills preferidas y reglas del roster: [`agents/README.md`](agents/README.md).

## Criterio y acabados

Dos referencias sostienen la capa de decisiÃ³n y se aplican siempre, sin gastar cupo de triaje:

- **[`criterio.md`](skills/el-jefe-team/references/criterio.md)**: cÃ³mo se decide. JerarquÃ­a en conflicto (confianza, accesibilidad, correcciÃ³n tÃ©cnica, psicologÃ­a), negocio (LTV/CAC â‰¥ 3, payback â‰¤ 12 meses, ICP con criterios de descarte), psicologÃ­a Ã©tica frente a dark patterns, producto (JTBD, time-to-value, retenciÃ³n por cohorte) y un interrogatorio de 10 preguntas antes de aprobar.
- **[`acabados.md`](skills/el-jefe-team/references/acabados.md)**: cÃ³mo se juzga. Review en 8 segundos, capturas a 1440/768/390 con estados forzados, severidad P0â€“P3, checklist por capas y rÃºbrica canÃ³nica de 0 a 10.

La puerta es la misma para todo: media â‰¥ 8, ninguna capa < 7, cero P0/P1. La rÃºbrica, las bandas y la tabla de conversiÃ³n desde otras escalas estÃ¡n en `acabados.md` Â§4. Plantilla para no improvisar el veredicto: [`templates/revision-acabados.md`](templates/revision-acabados.md).

## Estructura del repo

```
.
â”œâ”€â”€ agents/                    # Roster y plantilla para crear roles nuevos
â”œâ”€â”€ preset/
â”‚   â”œâ”€â”€ el-jefe.patch.yml      # Override del preset `standard`
â”‚   â”œâ”€â”€ agent-team.patch.yml   # Sube el tope de miembros del bundle Agent Team
â”‚   â”œâ”€â”€ mcp-browseros.example.yml
â”‚   â””â”€â”€ README.md
â”œâ”€â”€ skills/
â”‚   â”œâ”€â”€ el-jefe-team/          # SKILL.md + 21 fichas de referencia + plantilla de revisiÃ³n
â”‚   â”œâ”€â”€ threejs/               # Skill paraguas de 3D web
â”‚   â””â”€â”€ catalog.md             # Skills externas: repo, licencia y cÃ³mo se instalan
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ INSTALL.md             # InstalaciÃ³n paso a paso y troubleshooting
â”‚   â”œâ”€â”€ ARQUITECTURA.md        # CÃ³mo funciona el equipo por dentro
â”‚   â””â”€â”€ CHANGELOG.md
â”œâ”€â”€ templates/                 # estado, memoria, skills-plan, retro, GLOSSARY, ADR, trabajo, revisiÃ³n
â”œâ”€â”€ scripts/                   # InstalaciÃ³n, verificaciÃ³n y validaciÃ³n
â”œâ”€â”€ CONTRIBUTING.md
â”œâ”€â”€ SECURITY.md
â”œâ”€â”€ NOTICE.md                  # Atribuciones de terceros
â”œâ”€â”€ LICENSE
â””â”€â”€ README.md
```

## Requisitos

- **Windows**, el sistema donde estÃ¡ probado. En macOS y Linux los pasos son los mismos cambiando las rutas, pero no se ha probado.
- **DSH Desktop** con el bundle experimental **Agent Team** habilitado. El preset se ha verificado con DSH 0.2.2-rc.1; en versiones anteriores falla por el paquete `tool-subagent-list-agents` (ver el troubleshooting de [`docs/INSTALL.md`](docs/INSTALL.md)).
- **Python 3.11 o superior** con **PyYAML** para los validadores (`python -m pip install pyyaml`). La skill `seo` de terceros pide Python 3.11â€“3.14 para sus propios scripts.
- **PowerShell** para `scripts/install.ps1` y `scripts/verify.ps1`.
- Opcional: un MCP de navegador (por ejemplo BrowserOS neo) para research y QA web. El ejemplo de configuraciÃ³n estÃ¡ en [`preset/mcp-browseros.example.yml`](preset/mcp-browseros.example.yml).

## Inicio rÃ¡pido

Cinco pasos. La versiÃ³n larga, con troubleshooting, estÃ¡ en [`docs/INSTALL.md`](docs/INSTALL.md).

**1. Clona el repo.**

```powershell
git clone https://github.com/fxMT-nx/El-Jefe-Stack.git
cd El-Jefe-Stack
```

**2. Instala la skill del equipo** en `%USERPROFILE%\.agents\skills\el-jefe-team`. Puedes copiar la carpeta a mano o usar el script, que hace copia de seguridad si ya existe:

```powershell
.\scripts\install.ps1 -SkipPreset
```

**3. Aplica el preset.** Haz una copia de `%USERPROFILE%\.dsh\profiles\desktop\cordis.patch.yml` y pega **al final** el contenido de `preset/el-jefe.patch.yml`. Si quieres mÃ¡s de 7 especialistas vivos, pega tambiÃ©n `preset/agent-team.patch.yml` y reinicia DSH.

**4. Instala las skills externas** que uses, desde sus repos originales: la lista y los comandos estÃ¡n en [`skills/catalog.md`](skills/catalog.md).

**5. Verifica y arranca.** Comprueba la instalaciÃ³n y crea una sesiÃ³n nueva:

```powershell
.\scripts\verify.ps1
```

El chip del preset debe decir **El Jefe**. SalÃºdalo y pÃ­dele un proyecto.

`verify.ps1` mira la instalaciÃ³n viva, incluidas las skills externas: si aÃºn no has instalado ninguna, te dirÃ¡ quÃ© falta con `[FALTA]`. Es informaciÃ³n, no un error de la instalaciÃ³n del preset.

## Skills externas

El repo **no vendoriza** las skills de terceros. [`skills/catalog.md`](skills/catalog.md) dice cuÃ¡les usa el stack, de quÃ© repositorio vienen, quÃ© aporta cada una y cÃ³mo se instalan (`npx skills add owner/repo --skill nombre`, o copiando el directorio a `%USERPROFILE%\.agents\skills\`). Cada una conserva su licencia; las atribuciones estÃ¡n en [`NOTICE.md`](NOTICE.md).

Dos detalles que ahorran tiempo:

- **Skills largas.** En las versiones probadas de DSH, los resultados de herramienta se recortan a 8192 caracteres, asÃ­ que una skill mÃ¡s larga llega al agente a medias. `python scripts/skill_pack.py --audit` mide y `--split <skill>` trocea el `SKILL.md` en `references/parte-NN-*.md` sin perder texto. `--verify` comprueba el resultado y `--restore` lo deshace.
- **3D web.** `python scripts/install_threejs_skill.py` instala la skill `threejs` de este repo y descarga las referencias del bundle `CloudAI-X/threejs-skills` (MIT), ya troceadas.

## Scripts

| Script | QuÃ© hace |
|---|---|
| `scripts/install.ps1` | Copia la skill a `~/.agents/skills` y aÃ±ade el preset al patch del perfil, con backups. Admite `-DryRun` y `-SkipPreset`. |
| `scripts/verify.ps1` | Comprueba la instalaciÃ³n viva: ficheros, lÃ­mites de tamaÃ±o, referencias, plantillas y skills externas. |
| `scripts/validate_repo.py` | Valida el repo: YAML del preset y de la skill, enlaces relativos, scripts, protocolo de triaje y empaquetador. Se ejecuta en local antes de enviar un cambio. |
| `scripts/skill_router.py` | Rankea las skills instaladas contra una tarea y explica por quÃ©. |
| `scripts/skills_check.py` | Crea (`--init`) y valida el registro de triaje `docs/memoria/40-skills.md`; `--inventory` lista las skills instaladas. |
| `scripts/skill_pack.py` | Trocea skills largas sin perder texto: `--audit`, `--split`, `--verify`, `--restore`. |
| `scripts/memory_check.py` | Crea (`--init`) y valida la memoria viva de un proyecto. |
| `scripts/install_threejs_skill.py` | Instala la skill `threejs` con sus referencias descargadas y troceadas. |

Ninguno de estos scripts necesita permisos de administrador ni escribe fuera de tu carpeta de usuario y del repo.

## Seguridad y privacidad

- **El preset toca la configuraciÃ³n de DSH.** El paso 3 modifica `cordis.patch.yml`, que decide la persona y las herramientas de tus sesiones. `install.ps1` guarda una copia `*.bak-<fecha>` antes de escribir; si pegas el bloque a mano, haz tÃº la copia.
- **Sin telemetrÃ­a.** Los scripts de validaciÃ³n, router, memoria y empaquetado trabajan con ficheros locales. El Ãºnico que sale a la red es `install_threejs_skill.py`, que descarga documentos de `raw.githubusercontent.com`.
- **Skills de terceros, bajo tu criterio.** Una skill son instrucciones que tu agente sigue: lÃ©ela antes de instalarla y fija el commit si puedes. Las atribuciones y licencias estÃ¡n en [`NOTICE.md`](NOTICE.md).
- **Vulnerabilidades.** Se reportan en privado por GitHub Security Advisories; el alcance y el proceso estÃ¡n en [`SECURITY.md`](SECURITY.md).

## Estado y compatibilidad

VersiÃ³n actual: **1.7.2** (ver [`docs/CHANGELOG.md`](docs/CHANGELOG.md)). El proyecto es experimental: el preset depende de DSH Desktop, del bundle Agent Team y de la versiÃ³n instalada. Se ha probado en Windows con DSH Desktop 0.2.2-rc.1; no hay compromiso de compatibilidad con otras versiones ni con otros sistemas. Si actualizas DSH y algo deja de arrancar, el troubleshooting de [`docs/INSTALL.md`](docs/INSTALL.md) cubre los fallos conocidos.

## CrÃ©ditos y licencia

- **DeepSeek Harness** y sus paquetes son de DeepSeek. Este repo no estÃ¡ afiliado a DeepSeek.
- **Skills de terceros**: cada una pertenece a su autor y conserva su licencia. La lista con repositorios, licencias y commits estÃ¡ en [`NOTICE.md`](NOTICE.md) y [`skills/catalog.md`](skills/catalog.md).
- **Contenido propio** (preset, skill `el-jefe-team`, scripts, plantillas y documentaciÃ³n): **MIT**, ver [`LICENSE`](LICENSE). La skill `threejs` se apoya en el bundle `CloudAI-X/threejs-skills` (MIT).

## Contribuir

Las propuestas de skills, roles, correcciones y mejoras son bienvenidas. Antes de enviar nada, [`CONTRIBUTING.md`](CONTRIBUTING.md): estÃ¡ndar de fichas, validaciÃ³n obligatoria, estilo de commits y licencia de las contribuciones.

