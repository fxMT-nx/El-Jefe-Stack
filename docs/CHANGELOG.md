# Changelog

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