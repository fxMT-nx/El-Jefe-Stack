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

Límites: `maxMembers: 8` (Lead + 7 teammates), `maxTasks: 256`. Los nombres son permanentes y no se reutilizan.

### Memoria

- **Dentro de la sesión**: roster y tareas se persisten en el log de la sesión de El Jefe; cada teammate tiene su propia Session con historial y se reanuda al recibir un mensaje.
- **Entre sesiones nuevas** no hay recuerdo automático: la continuidad la da la **memoria en disco**.
- **Estructura**: `docs/estado.md` (snapshot ≤1.5 KB) + `docs/memoria/` (`00-indice`, `10-proyecto`, `20-usuario`, `30-decisiones`, `50-tecnico`, `60-tareas`, `70-riesgos`, `80-preguntas`, `90-historial`), más `GLOSSARY.md`, `docs/adr/`, `docs/trabajo.md` y `CHANGELOG.md`.
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

El límite de 7 teammates vivos sigue aplicando: crear un agente no es excusa para saltarse dependencias ni scopes.

## Selección de skills

Cada rol tiene skills preferidas (no exclusivas). El especialista elige 1–3 complementarias, las declara en su reporte y puede buscar otras en las fuentes de descubrimiento. Matriz completa: `skills/el-jefe-team/references/skills-seleccion.md`.

Cuando haya duda, el **router** puntúa las skills instaladas contra la tarea:

```bash
python scripts/skill_router.py "auditar SEO técnico de una landing" --top 5
```

Inspirado en la recuperación de skills de Skill-3D (`skill_retrieval.py`): skills como unidades con nombre, cuándo, estrategia y herramientas; el ranking es explicable (nombre, descripción, triggers, tamaño) y sustituye a la intuición.

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
