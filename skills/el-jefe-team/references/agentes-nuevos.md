# Agentes bajo demanda

Cuando el roster no cubre una especialidad, El Jefe **crea el agente que falta**; no improvisa ni fuerza a un especialista a hacer algo fuera de su rol.

## Cuándo crear uno

- La tarea pide experiencia que ningún rol cubre (audio/DSP, contratos, bioinformática, SAP, i18n, accesibilidad especializada, hardware, compliance…).
- Un rol existente se queda corto de forma recurrente.
- Hay una responsabilidad nueva que necesita criterios propios.

## Cómo (5 pasos)

1. **Nombre y misión.** Nombre kebab-case único (no reutilizar nombres), misión en una frase, cuándo usarlo y cuándo no.
2. **Ficha de rol.** Copia `agents/new-role-template.md` o la estructura de `references/roles-*.md`: misión, cuándo, brief mínimo, entregable y evidencia, checklist, límites y prompt de arranque.
3. **Skills.** Busca 1–3 skills que cubran el rol (primero lo instalado; si no hay, busca fuera y propón instalación). Anota en la ficha qué skills usa y por qué.
4. **Brief y spawn.** Redacta un brief autocontenido (plantilla del manual) y lanza `spawn_teammate` con `context: fresh`.
5. **Revisión y persistencia.** Revisa el resultado como cualquier entrega. Si el rol se va a reutilizar, guarda la ficha en `agents/custom/<nombre>.md` del repo del proyecto (o en este stack si es transversal) y añádela al roster.

## Cómo buscar skills

1. **Lo instalado primero**: catálogo de la sesión o `~/.agents/skills`. Usa `find`/lectura de frontmatter para ver qué hay.
2. **Fuentes externas**: `skillsagents.com`, `ComposioHQ/awesome-claude-skills`, `hesreallyhim/awesome-claude-code`, `VoltAgent/awesome-claude-code-subagents`, `ykdojo/claude-code-tips` y el índice `kraayenjon/agent-skills-es`.
3. **Búsquedas GitHub**: `topic:agent-skills`, `"SKILL.md" <tema>`, `claude skill <tema>`, `owner/repo`. API útil:
   - `https://api.github.com/search/repositories?q=<tema>+skills`
   - árbol del repo (`/git/trees/<branch>?recursive=1`) para localizar `SKILL.md`.
4. **Evalúa antes de instalar**: licencia permisiva (MIT/Apache), último push, estrellas/uso, tamaño, calidad del `SKILL.md` (¿brief, pasos, límites?), duplicados locales.
5. **Instala**: `npx skills add owner/repo --skill nombre` o clon shallow + copia a `~/.agents/skills/<nombre>/`; verifica frontmatter (`name:` == directorio, `description:`) y que el catálogo la liste.
6. **Permisos**: instalar una skill local es 🟡 (la aprueba El Jefe). Si es instalación global, toca el sistema o la licencia es dudosa, El Jefe te lo consulta (🔴).

## Calidad mínima de un agente nuevo

- Ficha con brief, entregable, evidencia, checklist y límites, como las existentes.
- Skills elegidas con justificación y declaradas en el reporte.
- Criterios de aceptación verificables.
- Nada de agentes genéricos sin especialidad: si no aporta criterio propio, usa `becario`.

## Plantilla

La plantilla de ficha está en `agents/new-role-template.md` (repo). Para el brief, usa la plantilla de encargo del `SKILL.md`.
