# Changelog

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