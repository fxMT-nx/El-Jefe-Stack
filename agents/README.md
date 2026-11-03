# Roster de agentes

Cada fila es un **nombre permanente** de `spawn_teammate` (el Jefe no puede repetir nombres). La ficha completa vive en `../skills/el-jefe-team/references/`.

| Spawn | Rol | Ficha | Skills preferidas |
|---|---|---|---|
| `movil-ui` | Frontend móvil | `roles-movil.md` | apple-design, ui-animation, motion-design, ui-design, frontend-design, emil-design-eng, design-taste-frontend, modern-web-guidance, find-animation-opportunities, review-animations |
| `movil-api` | Backend móvil | `roles-movil.md` | supabase-postgres-best-practices, security-best-practices, vitest, playwright |
| `web-ui` | Frontend web | `roles-web.md` | design-taste-frontend, frontend-design, ui-design, apple-design, emil-design-eng, motion-design, ui-animation, animate, animation-vocabulary, find-animation-opportunities, improve-animations, review-animations, web-design-guidelines / antfu-web-design-guidelines, modern-web-guidance, vercel-react-best-practices, vite, vitest, ui-verification, webapp-testing, code-simplification, algorithmic-art / canvas-design |
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
| `disenador-3d` | Diseño 3D | `roles-qa-3d.md` | media-use, motion-design, hyperframes-animation, canvas-design, algorithmic-art |
| `becario` | Generalista | `roles-becario.md` | agent-desktop, office-*, browseros-neo, playwright (y cualquiera según el encargo) |

## Reglas

- **Nombres permanentes**: no reutilizar; un nombre fallido queda reservado.
- **Máximo 7 teammates vivos** (el perfil permite 8 miembros: Lead + 7). Rota y reutiliza miembros inactivos.
- **Briefs autocontenidos**: un teammate `fresh` no ve la conversación del Jefe; con `fork` hereda sus turnos completados (usar solo cuando haga falta el historial).
- **Sin usuario directo**: todas las dudas suben a El Jefe, que escala si toca.
