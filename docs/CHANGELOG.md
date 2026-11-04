# Changelog

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