# Changelog

## 1.7.1

- **El Jefe ya no delega con subagentes**: el preset `standard` de El Jefe reintroducía `tool-subagent`, `tool-subagent-fork` y `tool-subagent-control` dentro de su lista de plugins, así que una sesión nueva veía `subagent` y lo elegía en vez de `spawn_teammate`. Se eliminan del preset (el bundle de Agent Team ya los desactiva a nivel global); quedan solo `workflow-ptc`/`tool-workflow` y las herramientas de Agent Team. La persona añade: «Delegas solo con `spawn_teammate` (Agent Team): no uses `subagent` ni `subagent_fork`».
- **Verificado tras DSH 0.2.2-rc.1**: sesión nueva con 12 miembros (1 lead + 11 teammates) —por encima del antiguo tope de 8—, `spawn_teammate` fresh y fork, `send_message`, `team_task_*`, `list_agents` y reanudación de un teammate inactivo; `task-9` reclamada y completada por un teammate. Requiere recargar/crear sesión nueva para que el preset sin subagentes entre en vigor.

## 1.7.0

- **Compatible con DSH 0.2.2-rc.1**: el preset `standard` ya no declara `tool-subagent-list-agents` (paquete eliminado; `list_agents` vive dentro de `tool-subagent-control`) y `tool-subagent` usa `modelSelection: true` + `modelDiscovery: true` en vez de `modelSelectionSettings`. Sin esto, cualquier sesión nueva falla con `agent-preset/invalid: tool-subagent-list-agents ... never started`. Actualizado el preset vivo y `preset/el-jefe.patch.yml`; requiere **reiniciar DSH** (el preset se compone al arrancar).
- **Diagnóstico**: si tras actualizar DSH aparece ese error, el fichero de perfil puede estar ya corregido pero el proceso conserva el preset en memoria; un reinicio completo lo resuelve.

## 1.6.3

- **Packer con medición real (B1)**: `skill_pack.py` lee con `newline=""` y cuenta los code points que ve el pruner (CRLF suma 2); escribe en LF con presupuesto 7.800 (SKILL.md) / 6.900 (partes). Re-troceadas 44 skills: **0 de 84 superan 8.192 reales** (antes 17). `--audit` informa también el peor caso CRLF y `--verify` mide el fichero real.
- **`--verify` con integridad (B2)**: reconstruye el cuerpo (inline + partes) y lo compara con `00-original.md`; detecta secciones perdidas, duplicadas o texto añadido. Prueba de corrupción: añadir texto a una parte ⇒ exit 1 con la diferencia exacta. El smoke de `validate_repo.py` cubre CRLF real y corrupción; `verify.ps1` ejecuta `--audit` y `--verify` y falla si algo supera el límite o pierde integridad.
- **Rúbrica canónica (B3)**: `acabados.md` §4 es la única escala (9–10 / 7–8 / 5–6 / 3–4 / 0–2); `criterio.md` remite a ella, `puertas-calidad.md` y la plantilla usan las mismas bandas, y hay tabla de conversión para escalas externas (`ux-heuristics`, `influence-psychology`, `copy-editing`).
- **Plantilla en la skill viva (B4)**: `templates/revision-acabados.md` dentro de `el-jefe-team` (repo y `~/.agents/skills`), referenciada relativa a la skill; `verify.ps1` comprueba existencia y hash repo=vivo.
- **Persona**: «exige revisión P0–P3 con nota media ≥8, ninguna capa <7 y cero P0/P1». Router con intenciones en español (`precio`, `copy`) que ya encuentra `founder-pricing`/`copy-editing`; precedencia de solapes documentada en `skills-seleccion.md`.
- **21 referencias**: la coordinación sale del `SKILL.md` a `references/coordinacion.md` (SKILL 7.975 chars, incluso con CRLF 8.077 < 8.192). `.gitattributes` fija `*.md`/`*.yml`/`*.py`/`*.ps1` en LF para que un checkout Windows no vuelva a truncar. `memory_check.py` informa una sola vez por fichero con UTF-8 inválido. README/ARQUITECTURA documentan la excepción 4–5 skills por fase.

## 1.6.2

- **Persona sin tope**: la viñeta «Máximo 6 especialistas vivos» pasa a «Sin tope de especialistas vivos: crea los que el trabajo necesite, con una pieza disjunta cada uno».

## 1.6.1

- **Agent Team sin tope práctico**: el bundle fija `maxMembers: 8` (Lead + 7). Nuevo `preset/agent-team.patch.yml` con `- id: agent-team` / `maxMembers: 1000` (roster por equipo, incluye fallidos), `maxTasks: 256`, `maxMessageBytes: 65536` y `disposalTimeoutMs: 5000`; el patch va al final del patch de perfil y sustituye el `config` del bundle. Verificado con `dsh --dump-config` sobre una copia del perfil (la fila aparece «patched by …cordis.patch.yml» con 1000); en `desktop` requiere reiniciar y probar con >7 teammates en sesión nueva.
- **Doctrina**: `SKILL.md` pasa de «Máximo 6 especialistas vivos» a «Sin tope de especialistas; reutiliza nombres». `README.md`, `docs/ARQUITECTURA.md` y `agents/README.md` reflejan el nuevo límite y mantienen el criterio de una pieza disjunta por miembro. `docs/INSTALL.md` gana el paso 2b.

## 1.6.0

- **17 skills curadas de criterio instaladas**, cada una con su `SOURCE.md` (repo, commit exacto, licencia MIT y fecha): `copy-editing`, `marketing-psychology`, `analytics`, `attribution`, `customer-research` (`coreyhaines31/marketingskills` @ `88c79f65`); `ux-heuristics`, `obviously-awesome`, `influence-psychology`, `jobs-to-be-done`, `monetizing-innovation`, `improve-retention` (`wondelai/skills` @ `d8d5d75f`); `founder-cfo`, `founder-pricing`, `founder-offer` (`Jakeschincariol/founder-skill` @ `fd9385b0`); `taste-design-review`, `taste-ux-copy`, `taste-accessibility` (`madebymustafa/design-taste` @ `c4a6bff0`). Inventario: **84 skills** (`python scripts/skills_check.py --inventory`).
- **Truncado silencioso de skills, arreglado** (nuevo `scripts/skill_pack.py`): el pruner de sesión recorta los resultados de herramienta a 8.192 caracteres, así que las skills largas llegaban al agente a medias. `--audit` mide, `--split` trocea el `SKILL.md` por encabezados `##` en `references/parte-NN-<slug>.md` (≤7.000 caracteres) y deja frontmatter + intro + reglas clave + índice con enlaces relativos, conserva el original en `references/00-original.md` (`--restore` lo deshace) y `--verify` comprueba límites, partes e índice. Sin dependencias externas. **Antes: 43 de 84 skills superaban el límite; después: 0 de 84.** Cada carácter del original acaba exactamente en un sitio (sha256 del cuerpo comprobado antes de escribir) y los enlaces relativos se reescriben al bajar de nivel.
- **Criterio y acabados** (nuevo): `references/criterio.md` (jerarquía confianza → accesibilidad → corrección técnica → psicología, negocio, psicología, decisiones e interrogatorio de 10 preguntas) y `references/acabados.md` (proceso de review, checklist por capas, rúbrica 0–10, evidencia exigible y anti-patrones), con `templates/revision-acabados.md`. La sección «Puertas de calidad» sale del `SKILL.md` a `references/puertas-calidad.md`, ampliada con la puerta por entregable y la revisión P0–P3 (media ≥ 8, ninguna capa < 7, cero P0/P1).
- **`SKILL.md`** (8.180 caracteres, límite 8.192): nueva sección corta «Criterio y acabados», `criterio aplicable:` en la plantilla de encargo y anti-patrón «entregar genérico o de plantilla sin criterio». Referencias: 17 → 20.
- **Persona** (repo y perfil vivo): viñeta «Juzga con criterio de negocio, psicología y acabados; exige revisión P0–P3 y devuelve lo genérico.». Ambos YAML siguen con `id: standard` y parsean.
- **Fichas de rol**: `roles-web.md`, `roles-movil.md`, `roles-qa-3d.md`, `roles-escritor.md` y `roles-seo-marketing.md` añaden una línea «Criterio y acabado» con el mínimo exigible (UI: revisión de acabados con capturas; copy: microcopy sin slop; marketing: claims con evidencia y unit economics).
- **Matriz** (`skills-seleccion.md`): las nuevas skills entran por rol (El Jefe: `analytics`, `attribution`, `customer-research`; `web-ui`: `ux-heuristics`, `taste-*`; `marketing`: posicionamiento, persuasión, precio, oferta y unit economics; `qa-critico`: `taste-design-review`) y los mínimos por fase ganan la revisión de acabados y los claims con evidencia. `memoria` y `documentador` no reciben skills: la capa de criterio no consume cupo de triaje.
- **Validación**: `validate_repo.py` prueba el packer con un troceo real en un temporal (límite, índice, idempotencia y `--restore` exacto), exige 20 referencias y los ficheros de criterio, y comprueba la viñeta de persona; los enlaces de `docs/research/` (material de trabajo, no entregable) quedan fuera de la validación. `verify.ps1` sube a 20 referencias y comprueba las 17 skills curadas con su `SOURCE.md`.

## 1.5.2

- **`memory_check.py` sin traceback (B5)**: `read()` captura `UnicodeDecodeError` y `OSError` y devuelve una línea («docs/… no está en UTF-8 válido»), exit 1 y sigue revisando el resto de `docs/`; red de seguridad en el arranque. Cubre `40-skills.md`, `estado.md` y cualquier `.md` de `docs/`.
- **Evidencia real (B6)**: `Evidencia: no aplica`/`ninguna`/`n/a` es error duro en `skills_check.py`, igual que vacío o `TBD`/`pendiente`; la evidencia **no se hereda** del waiver. `memory_check.py` aplica el mismo criterio al validar las filas del registro.
- **Waiver completo (B7)**: un waiver citado exige `Tarea`, `Motivo`, `Alternativa aplicada`, `Aprueba` y `Fecha` no vacíos (ni marcadores); si falta cualquiera, error. Un waiver definido y no usado sigue siendo aviso.
- **Smoke del repo**: `validate_repo.py` prueba además B6, B7 y `Fecha` vacía, y su `read()` informa de un `.md` con UTF-8 inválido sin traceback (I2 de la reauditoría).
- **`SKILL.md`** (8.173 caracteres, límite 8.192): la ley exige «1 regla concreta **y el cambio que provocó**», admite 4–5 con justificación y concreta el cierre («sin bloque, waiver o efecto comprobable, se devuelve»).
- **`triaje-skills.md`**: waiver con sus cinco campos, evidencia `no aplica` = incumplimiento y `memory_check` en el registro; anti-patrón de evidencia de relleno. `templates/skills-plan.md` refleja ambas reglas.

## 1.5.1

- **Validador sin los falsos OK conocidos (B1–B4)** (`scripts/skills_check.py`): errores duros (exit 1) para skills y herramientas vacías, `no aplica`/`ninguna` sin waiver, evidencia vacía o en `TBD`/`pendiente`, y waiver citado con `Aprueba` o `Fecha` vacías; un waiver definido y no usado solo avisa, igual que un registro recién creado sin filas. Un registro con UTF-8 inválido se informa con un mensaje claro y sin traceback (validación, `--init` e `--inventory`). Se conservan `--init`, `--inventory`, `--json`, `--project`/posicional y `--force`.
- **Smoke interno ampliado** (`scripts/validate_repo.py`): dos positivos (fase con skills, herramientas y evidencia; waiver válido cubriendo una fase sin skills), los cuatro negativos B1–B4 (skills `no aplica`, herramientas `no aplica`, evidencia vacía/`TBD`, waiver citado sin aprobador) y un registro con UTF-8 inválido (exit 1 sin traceback).
- **`memory_check.py`**: si existe `docs/estado.md` y falta `docs/memoria/40-skills.md` avisa con el comando que lo crea; si existe, valida sus filas con las reglas de `skills_check` y reporta error si están mal.
- **Doctrina** (`triaje-skills.md`): antídoto anti-fake (cada skill declarada cita 1 regla concreta y el cambio que provocó; sin efecto comprobable es incumplimiento), búsqueda obligatoria cuando no hay candidata (router → catálogo por descripción → al menos 2 fuentes externas, dejando consultas y enlaces en el reporte) y tope **1–3 skills por fase** (4–5 exige justificación escrita). `skills-seleccion.md` queda alineado: el ejemplo de landing baja a 3.
- **`SKILL.md`** (8.132 caracteres, límite 8.192): el paso 2 del protocolo indica que cada tarea declara skills y herramientas, la plantilla de encargo añade `herramientas esperadas:` y la ley exige **citar 1 regla concreta aplicada**. Recortes de prosa para no superar el límite.
- **Preset versionado**: se añaden a `preset/el-jefe.patch.yml` las dos viñetas de persona que solo existían en el perfil vivo (memoria del proyecto y agentes bajo demanda); ambos YAML quedan con 15 viñetas y `id: standard` intacto, con el mismo texto de persona.

## 1.5.0

- **Triaje obligatorio de skills y herramientas**: nueva referencia `references/triaje-skills.md` con la ley, el protocolo T-R-I-A-J-E (Tarea, Revisar catálogo, Identificar, Aplicar 1–3, Justificar, Evidencia), mínimos por tipo de trabajo, waivers, puerta de El Jefe, auditoría de cierre y anti-patrones. "No aplica" pasa a ser una decisión explícita, nunca un olvido.
- **Evidencia**: todo reporte termina con el bloque `## Skills y herramientas` (skill, por qué, dónde se aplicó, resultado) más descartadas, waivers y herramientas; sin él, El Jefe devuelve el entregable.
- **Registro persistente** `docs/memoria/40-skills.md` (mapa fase → skills/herramientas/evidencia, waivers y huecos) con plantilla `templates/skills-plan.md`; `memory_check.py --init` lo crea y su ausencia solo avisa.
- **`scripts/skills_check.py`**: `--init` crea el registro, la validación detecta fases sin skills/herramientas y sin waiver, marcadores `TBD`/`pendiente` y celdas vacías, y `--inventory` lista el catálogo real instalado (texto o `--json`).
- **SKILL.md** (≤8192 caracteres): sección `## Skills` reescrita con la ley, la evidencia y la puerta; `skills esperadas:` en la plantilla de encargo; anti-patrones nuevos.
- `skills-seleccion.md` pasa a "Skills: triaje obligatorio y selección" (ley, mínimos por fase, evidencia); `memoria-viva.md` y `roles-memoria.md` incorporan `40-skills.md`.
- Persona del preset (repo y perfil vivo): "Ninguna fase sin triaje de skills y herramientas…". `validate_repo.py` y `verify.ps1` comprueban los ficheros, el tamaño, el registro (smoke positivo y negativo) y la viñeta.

## 1.4.0

- **Memoria viva**: protocolo completo en `references/memoria-viva.md` (estructura `docs/estado.md` + `docs/memoria/`, snapshot ≤1.5 KB, qué guardar y qué no, actualización antes de compactar y al cerrar, sesiones nuevas).
- **`scripts/memory_check.py`**: valida estructura, snapshot, tamaño, enlaces, secretos y frescura; `--init` crea el esqueleto.
- El Jefe es el dueño último de la memoria (persona) y `memoria`/`documentador` se alinean con el nuevo formato; README y arquitectura actualizados.

## 1.3.0

- **Three.js**: skill paraguas `threejs` (r186) con 53 referencias troceadas (≤7 KB) a partir del bundle `CloudAI-X/threejs-skills` (MIT), más instalador reproducible `scripts/install_threejs_skill.py`.
- Enganches: `web-ui` y `disenador-3d` en la matriz y el roster; intención `web3d` en el router; catálogo y verificación actualizados.

## 1.2.0

- **Router de skills** (`scripts/skill_router.py`): ranking explicable de skills instaladas por tarea, inspirado en `skill_retrieval.py` de Skill-3D. Salida humana o JSON y `--build-index`.
- **Aprendizaje (retro)**: `references/aprendizaje.md` + `templates/retro.md`; éxitos → workflows, fallos → lecciones; promoción solo si se repite (≥2 proyectos) o es grave.
- **Toolkit 3D opcional**: `references/toolkit-3d.md` (Depth Anything 3, SAM 3, Grounding DINO, Pi3, SwinIR, Orient Anything) y ficha de `disenador-3d` actualizada, con permisos de instalación.
- Validación local ampliada a los scripts Python.

## 1.1.0

- **Agentes bajo demanda**: El Jefe puede crear roles nuevos con calidad (ficha completa, skills elegidas/buscadas, brief autocontenido) cuando falta una especialidad; plantilla en `agents/new-role-template.md` y procedimiento en `skills/el-jefe-team/references/agentes-nuevos.md`.
- CI (`validate.yml` + `scripts/validate_repo.py`): valida YAML del preset, frontmatter y tamaño de la skill, referencias y enlaces relativos.
- Persona actualizada con la regla de agentes bajo demanda.

## 1.0.0

- Preset "El Jefe" (override de `standard`) con persona cercana y adaptativa, jerarquía usuario > Jefe > equipo, permisos con escalado y sin vetos absolutos, y "no se mancha las manos".
- Skill `el-jefe-team` con 15 roles, fichas, protocolo de proyecto, puertas de calidad, permisos, preferencias de skills y descubrimiento.
- Fase 0 de grilling (`grilling`, `grill-with-docs`, `domain-modeling`) y formato de memoria: `docs/estado.md`, `GLOSSARY.md`, ADR en `docs/adr/`.
- Plantillas y scripts de instalación/verificación.