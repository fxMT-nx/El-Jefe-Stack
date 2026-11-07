# Roster de agentes

Cada fila es un **nombre permanente** de `spawn_teammate` (el Jefe no puede repetir nombres). La ficha completa vive en `../skills/el-jefe-team/references/`.

| Spawn | Rol | Ficha | Skills preferidas |
|---|---|---|---|
| `movil-ui` | Frontend móvil | `roles-movil.md` | apple-design, ui-animation, motion-design, ui-design, frontend-design, emil-design-eng, design-taste-frontend, modern-web-guidance, find-animation-opportunities, review-animations |
| `movil-api` | Backend móvil | `roles-movil.md` | supabase-postgres-best-practices, security-best-practices, vitest, playwright |
| `web-ui` | Frontend web | `roles-web.md` | design-taste-frontend, frontend-design, ui-design, apple-design, emil-design-eng, motion-design, ui-animation, animate, animation-vocabulary, find-animation-opportunities, improve-animations, review-animations, web-design-guidelines / antfu-web-design-guidelines, modern-web-guidance, vercel-react-best-practices, vite, vitest, ui-verification, webapp-testing, code-simplification, threejs (3D web), algorithmic-art / canvas-design |
| `web-api` | Backend web | `roles-web.md` | supabase-postgres-best-practices, security-best-practices, vitest, playwright, modern-web-guidance, code-review-and-quality, code-simplification |
| `investigador` | Research con fuentes | `roles-research.md` | browseros-neo, playwright, webapp-testing, modern-web-guidance + fuentes de descubrimiento |
| `infra` | Infraestructura | `roles-infra-seguridad.md` | security-best-practices, security-threat-model, playwright, vitest |
| `seguridad` | Seguridad aplicada | `roles-infra-seguridad.md` | security-threat-model, security-best-practices, supabase-postgres-best-practices, playwright, browseros-neo |
| `escritor` | Documentación y redacción | `roles-escritor.md` | brand, copywriting, office-*, changelog-automation |
| `documentador` | Bitácora del trabajo | `roles-documentador.md` | changelog-automation, domain-modeling, architecture-decision-records, office-*, writing-plans |
| `memoria` | Estado, glosario y ADR | `roles-memoria.md` | domain-modeling, architecture-decision-records, writing-plans, office-* |
| `seo-geo` | SEO técnico y GEO | `roles-seo-marketing.md` | seo, seo-technical, seo-content, seo-schema, seo-geo, ui-verification, webapp-testing, playwright, browseros-neo, modern-web-guidance |
| `marketing` | Posicionamiento y crecimiento | `roles-seo-marketing.md` | product-marketing, copywriting, cro, emails, launch, brand, design-taste-frontend, product-launch-video, media-use, browseros-neo, office-* |
| `qa-critico` | QA crítico | `roles-qa-3d.md` | code-review-and-quality, playwright, webapp-testing, ui-verification, vitest, agent-desktop, security-best-practices |
| `disenador-3d` | Diseño 3D | `roles-qa-3d.md` | media-use, motion-design, hyperframes-animation, canvas-design, algorithmic-art, threejs (visor/3D web) |
| `becario` | Generalista | `roles-becario.md` | agent-desktop, office-*, browseros-neo, playwright (y cualquiera según el encargo) |

## Reglas

- **Nombres permanentes**: no reutilizar; un nombre fallido queda reservado.
- **Sin tope de teammates**: el perfil admite hasta 1000 entradas de roster (antes 8). Aun así, cada miembro necesita una pieza disjunta; rota y reutiliza nombres en vez de acumular gente sin trabajo.
- **Briefs autocontenidos**: un teammate `fresh` no ve la conversación del Jefe; con `fork` hereda sus turnos completados (usar solo cuando haga falta el historial).
- **Skills esperadas y evidencia**: todo encargo declara en el brief las 1–3 skills esperadas —4–5 exige justificación escrita de qué disciplina extra lo pide y qué se descarta; más de 5 no se admite— (o el waiver aprobado) y exige el bloque `## Skills y herramientas` en el reporte. Sin ese bloque, el entregable se devuelve. Triaje obligatorio: `../skills/el-jefe-team/references/triaje-skills.md`.
- **Sin usuario directo**: todas las dudas suben a El Jefe, que escala si toca.

## Crear un agente nuevo

Si la tarea requiere una especialidad que el roster no cubre, **no se fuerza a un rol existente**: se crea un agente.

1. Copia `new-role-template.md` a `agents/custom/<nombre>.md` y rellena misión, cuándo, brief mínimo, entregable + evidencia, checklist y límites.
2. Elige 1–3 skills para el rol (4–5 exige justificación escrita; más de 5 no se admite; primero las instaladas); si falta alguna, búscala (fuentes en `../skills/el-jefe-team/references/agentes-nuevos.md`) y propón su instalación.
3. Redacta el brief autocontenido con la plantilla del manual y lanza `spawn_teammate` con `context: fresh`.
4. Revisa el resultado como cualquier entrega; si el rol se repite, guarda la ficha y añádelo al roster.

Si al rol le falta criterio propio, no es un rol: es trabajo para `becario`.
