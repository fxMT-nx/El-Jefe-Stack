# Arquitectura

## Jerarquía

```
Usuario
  └── El Jefe (Lead de la sesión)
        ├── movil-ui / movil-api
        ├── web-ui / web-api
        ├── investigador
        ├── infra / seguridad
        ├── escritor / documentador / memoria
        ├── seo-geo / marketing
        ├── qa-critico
        ├── disenador-3d
        └── becario
```

El usuario es la máxima autoridad. El Jefe manda al equipo y habla con el usuario; **ningún teammate habla directamente con el usuario**.

## Preset

El preset es una composición de plugins de DSH (`@deepseek-ai/dsh-agent-preset`). `preset/el-jefe.patch.yml` **redefine `standard`**:

- `name: El Jefe` y descripción (así aparece el chip).
- `persona.prefix`: identidad doble (Lead vs teammate), tono cercano y adaptativo, "no se mancha las manos", permisos, continuidad, fase 0.
- Mismas herramientas que el preset `standard` de DSH (bash/pwsh, fs, web, skills, plan mode, compaction, workflow, todo, present…).

Mantener el `id: standard` evita el bug de scopes al enlazar presets declarados desde la capa de usuario.

## Equipo (Agent Team)

El bundle experimental monta `@deepseek-ai/dsh-experimental-agent-team` y sus herramientas. Cada miembro recibe:

- `spawn_teammate` (solo Lead), `send_message`, `list_agents`, `wait_agent`, `interrupt_agent`.
- Tablero de tareas: `team_task_create`, `team_task_list`, `team_task_get`, `team_task_update`.

Límites: `maxMembers: 1000` (sin tope práctico; el bundle trae 8 por defecto), `maxTasks: 256`. Los nombres son permanentes y no se reutilizan. El override vive en el patch del perfil (`- id: agent-team`).

### Memoria

- **Dentro de la sesión**: roster y tareas se persisten en el log de la sesión de El Jefe; cada teammate tiene su propia Session con historial y se reanuda al recibir un mensaje.
- **Entre sesiones nuevas** no hay recuerdo automático: la continuidad la da la **memoria en disco**.
- **Estructura**: `docs/estado.md` (snapshot ≤1.5 KB) + `docs/memoria/` (`00-indice`, `10-proyecto`, `20-usuario`, `30-decisiones`, `40-skills`, `50-tecnico`, `60-tareas`, `70-riesgos`, `80-preguntas`, `90-historial`), más `GLOSSARY.md`, `docs/adr/`, `docs/trabajo.md` y `CHANGELOG.md`.
- **Responsable**: El Jefe (verifica antes de cerrar); `memoria` escribe y valida; `documentador` deja la bitácora.
- **Cuándo**: leer al arrancar; actualizar tras cada decisión o requisito, **antes de compactar** y al cerrar sesión.
- **Compactación**: borra contexto, no disco. El snapshot debe bastar para reconstruir el estado; si no, se mejora.
- **Validación**: `python scripts/memory_check.py <proyecto>` (`--init` crea el esqueleto). Detalle: `skills/el-jefe-team/references/memoria-viva.md`.

### Permisos

Zonas 🟢/🟡/🔴: lo local y reversible lo aprueba El Jefe; producción, dinero, datos reales, credenciales, publicación externa, instalación global o acciones irreversibles las decide el usuario por acción. No hay vetos absolutos. Detalle en `skills/el-jefe-team/references/permisos.md`.

## Fase 0: Grilling

Antes de planificar un trabajo no trivial:

1. El Jefe carga `grilling`.
2. Mapea el problema como árbol de decisiones y pregunta por rondas: preguntas numeradas, cada una con su respuesta recomendada. Un "sí" la acepta.
3. Los hechos los busca él (subagentes), no te pregunta lo que puede averiguar.
4. Con `grill-with-docs` + `domain-modeling` deja constancia: `GLOSSARY.md` y ADR en `docs/adr/`.
5. Solo pasa a `writing-plans` y al protocolo de proyecto cuando hay entendimiento compartido.

## Agentes bajo demanda

El roster cubre lo habitual, no todo. Cuando aparece una especialidad que ningún rol cubre (audio/DSP, contratos, bioinformática, i18n, compliance, hardware…), El Jefe **crea el agente**:

1. Escribe una ficha nueva con el formato de las existentes (`agents/new-role-template.md`): misión, cuándo sí/no, brief mínimo, entregable + evidencia, checklist, límites y prompt de arranque.
2. Elige 1–3 skills (instaladas o buscadas en las fuentes de descubrimiento) y anota por qué.
3. Lanza `spawn_teammate` con `context: fresh` y un brief autocontenido.
4. Revisa el resultado como cualquier entrega y, si el rol se va a reutilizar, guarda la ficha en `agents/custom/` del proyecto.

No hay tope de teammates vivos, pero crear un agente no es excusa para saltarse dependencias ni scopes: cada miembro necesita una pieza disjunta y un brief autocontenido.

## Selección de skills

La matriz orienta y los mínimos obligan: cada rol tiene skills preferidas, pero **toda fase pasa por triaje** (ver abajo). El especialista aplica 1–3 complementarias, las declara con evidencia y puede buscar otras en las fuentes de descubrimiento. Matriz completa: `skills/el-jefe-team/references/skills-seleccion.md`.

Cuando haya duda, el **router** puntúa las skills instaladas contra la tarea:

```bash
python scripts/skill_router.py "auditar SEO técnico de una landing" --top 5
```

Inspirado en la recuperación de skills de Skill-3D (`skill_retrieval.py`): skills como unidades con nombre, cuándo, estrategia y herramientas; el ranking es explicable (nombre, descripción, triggers, tamaño) y sustituye a la intuición.

## Triaje obligatorio de skills y herramientas

Ninguna fase, tarea ni entregable sin triaje explícito; "no aplica" se decide y se escribe, nunca se olvida. Usar una skill es cargarla y aplicar sus reglas; nombrarla no cuenta.

- **Protocolo T-R-I-A-J-E**: Tarea, Revisar catálogo real, Identificar candidatas leyendo su `description`, Aplicar 1–3, Justificar descartes y Evidencia. Mínimos por tipo de trabajo (UI, motion, API, BD, seguridad, deploy, documentación, SEO/GEO, marketing, 3D, QA), waivers y anti-patrones: `skills/el-jefe-team/references/triaje-skills.md`.
- **Registro**: `docs/memoria/40-skills.md` guarda el mapa fase → skills/herramientas/evidencia, los waivers aprobados y los huecos; se actualiza con la memoria y sobrevive a compactaciones.
- **Evidencia**: el reporte del especialista termina con `## Skills y herramientas` (skill, por qué, dónde se aplicó, resultado) más descartadas, waivers y herramientas usadas.
- **Puerta de El Jefe**: por hito revisa el registro, muestrea un entregable contra lo que exige la skill declarada y devuelve lo que no lo cumpla. Fase sin skill y sin waiver = fallo de proceso.
- **Herramientas**: la misma ley; se comprueba qué MCP/herramienta existe (browseros-neo, playwright, agent-desktop, office-*, pdfcraft, threejs, CAD…) y se declara cuál se usó.
- **Scripts**: `python scripts/skills_check.py --init <proyecto>` crea el registro desde `templates/skills-plan.md`; `python scripts/skills_check.py <proyecto>` lo valida (falla con fases sin skills/herramientas y sin waiver, o con `TBD`); `--inventory` lista las skills instaladas con su descripción. `memory_check.py --init` crea también el registro.

## Criterio y acabados

El triaje dice **qué skills** se aplican; la capa de criterio dice **cómo se decide y cuándo se rechaza**. No consume cupo de triaje porque no es una skill: se aplica siempre.

- **`references/criterio.md` — decidir.** Jerarquía en conflicto: **confianza → accesibilidad → corrección técnica → psicología**. Negocio (precio entre la SBA y el valor percibido, ICP con *disqualifying*, LTV/CAC ≥ 3, payback ≤ 12 meses, kernel de Rumelt, señal frente a vanidad), psicología (carga cognitiva, fricción con número, confianza como prueba concreta, Fogg, hábitos) con la tabla persuasión / dark pattern, producto (JTBD, time-to-value, retención por cohorte, churn causal), decisiones (rúbrica 0–10 con el hueco declarado, muestra precomprometida, una sola fuente de verdad para contar) y un interrogatorio de 10 preguntas antes de aprobar: **un «no lo sé» no se tapa con entusiasmo, se aprueba la investigación.**
- **`references/acabados.md` — juzgar.** Un entregable *funciona* cuando hace lo que dice; está *acabado* cuando alguien que no lo escribió lo usa sin que le expliquen nada. Review en 8 segundos sin scroll, capturas a 1440/768/390 con estados forzados, severidad **P0–P3**, checklist por capas (arranque, estados, formularios, microcopy, confianza, rendimiento percibido, a11y, responsive, consistencia, datos extremos, modo oscuro, confirmar/deshacer), rúbrica 0–10 y evidencia exigible.
- **Puerta**: se publica con **media ≥ 8**, **ninguna capa < 7** y **cero P0/P1**; sin capturas ni huecos declarados no hay veredicto, y **quien construye no firma** su propia revisión. Plantilla: `templates/revision-acabados.md`. Puerta por entregable y anti-patrones: `references/puertas-calidad.md`.
- **Dónde aterriza**: cada ficha de rol lleva su línea «Criterio y acabado» con el mínimo exigible (UI: revisión de acabados con capturas; copy: microcopy sin slop; marketing: claims con evidencia y unit economics; QA: P0–P3 con nota) y la plantilla de encargo pide `criterio aplicable:`.

## Skills sin truncar (`scripts/skill_pack.py`)

El pruner de sesión recorta los resultados de herramienta a **8.192 caracteres**, así que una skill más larga llegaba al agente truncada y sin las reglas del medio: el agente declaraba la skill y aplicaba solo su introducción. La solución es **trocear, no recortar**:

- `--audit [--root DIR]`: tamaño, estado (ok / EXCEDE / troceada) y número de partes de cada skill.
- `--split <skill> [--inline "Encabezado"] [--keep-original false]`: parte el cuerpo por encabezados `##` en `references/parte-NN-<slug>.md` (≤7.000 caracteres) y reescribe `SKILL.md` (≤8.192) con frontmatter, intro, reglas clave e **índice con enlaces relativos**. El original queda en `references/00-original.md` y `--restore` deshace el troceo exactamente.
- `--verify [--root DIR]`: cada `SKILL.md` ≤8.192, cada parte existe y no está vacía, el índice apunta a ficheros existentes y los enlaces reescritos resuelven; distingue el enlace heredado ya roto (aviso) del relink mal hecho (error).
- **Garantías**: cada sección acaba *exactamente una vez* (inline o en una sola parte) y el cuerpo reconstruido debe ser idéntico —se comprueba con sha256 antes de escribir nada—; los enlaces relativos se recalculan al bajar de nivel, incluidos los que apuntan a skills hermanas; el troceo es idempotente (si ya está troceada, avisa y no toca) y el `SKILL.md` generado se queda con las secciones que caben (la primera siempre, más las cortas imprescindibles).
- **Selección de lo que se queda inline**: primera sección (arranque/protocolo) + las que se piden con `--inline` (para no perder la sección crítica de una skill: p. ej. «No AI Tells» en `copywriting` o «Sections to Capture» —Objeciones y prueba— en `product-marketing`) + relleno con las secciones cortas en orden de documento mientras quepan.
- **Estado en la v1.6.0**: 84 skills instaladas, **43 troceadas, 0 por encima del límite** (`--audit`), y `validate_repo.py` prueba el packer con un troceo real en un directorio temporal en cada validación.

## Aprendizaje (retro)

Tras cada proyecto o hito: `documentador` rellena `templates/retro.md`; el Jefe separa **éxitos** (workflow reutilizable) de **fallos** (lección correctiva). Una lección se **promueve** (a ficha de rol, matriz de skills o skill nueva) solo si se repite en ≥2 proyectos o es un fallo grave; se registra en `docs/aprendizaje.md` y, si cambia una regla, en un ADR. Mecánica inspirada en `skill_learning.py` de Skill-3D.

## Toolkit 3D (opcional)

`disenador-3d` y las tareas de visión 3D pueden apoyarse en el toolkit de Skill-3D (Depth Anything 3, SAM 3, Grounding DINO, Pi3, SwinIR, Orient Anything) como servicios locales con GPU. Detalle, puertos y permisos: `skills/el-jefe-team/references/toolkit-3d.md`.

## Flujo de un proyecto

1. Grilling (fase 0).
2. Intake mínimo → plan y tablero.
3. Descubrimiento con `investigador` si hay dudas de stack.
4. Arquitectura: contratos antes de paralelizar.
5. Construcción en paralelo con scopes disjuntos.
6. Calidad: QA crítico + seguridad + infra.
7. Documentación (`escritor`) y bitácora (`documentador`).
8. Memoria: estado, glosario y ADR (`memoria`).
9. Entrega con evidencia, riesgos y pendientes.
