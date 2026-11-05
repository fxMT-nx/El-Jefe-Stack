# Triaje obligatorio de skills y herramientas

**Ley.** Ninguna fase, tarea ni entregable sin **triaje explícito** de skills y herramientas. Es una decisión razonada y registrada, nunca un trámite: "no aplica" se escribe y se justifica, jamás es un olvido. No usar la skill o herramienta que tocaba en cualquier tramo degrada todo el proyecto y es inaceptable. Usar la de costumbre tampoco es triaje.

## Qué significa "usar"

Usar una skill es **cargarla/leerla y aplicar sus reglas** al trabajo real; nombrarla sin leerla no cuenta y es incumplimiento. Usar una herramienta es elegir la correcta, ejecutarla y aportar su salida como evidencia. Declarar no es usar.

## Protocolo T-R-I-A-J-E

| Paso | Qué se hace |
|---|---|
| **T** — Tarea | Descompón el encargo en fases y entregables concretos (F1, F2…). |
| **R** — Revisar catálogo | Mira lo que **existe de verdad**: skills instaladas y herramientas/MCP disponibles en la sesión. |
| **I** — Identificar | Lee `description` y disparadores de las candidatas; no adivines por el nombre. Apóyate en `scripts/skill_router.py` y en la matriz de `skills-seleccion.md`. |
| **A** — Aplicar | Carga y sigue **1–3** skills complementarias por fase (más solo si el trabajo abarca más disciplinas). |
| **J** — Justificar | Escribe por qué esas y por qué no las descartadas; si una fase no lleva skill, declara el waiver. |
| **E** — Evidencia | Deja el bloque `## Skills y herramientas` en el reporte y la fila en `docs/memoria/40-skills.md`. |

Apoyo: `python scripts/skills_check.py --inventory` (catálogo real) y `python scripts/skill_router.py "<tarea>" --top 5` (candidatas puntuadas).

## Cuándo se hace

1. **Fase 0**: mapa fase → skills y herramientas de todo el plan, incluido lo previsto (UI, datos, deploy, publicación).
2. **Antes de cada tarea**, aunque la fase ya esté mapeada.
3. **Al cambiar de fase**: el trabajo cambia (p. ej. de construir a publicar).
4. **Ante algo nuevo**: bug raro, dependencia desconocida, datos reales, deploy, publicación externa, entregable documental.
5. **Al cerrar**: auditoría de cierre y actualización del registro.

## Mínimos por tipo de trabajo

| Tipo de trabajo | Mínimo exigible (skills) | Herramientas típicas |
|---|---|---|
| UI nueva | 1 de diseño (`design-taste-frontend`, `frontend-design`, `ui-design`) + 1 de verificación (`ui-verification`, `webapp-testing`, `web-design-guidelines`) | browseros-neo, playwright |
| Animación / motion | `animate`, `motion-design` o `ui-animation` + verificación visual | browseros-neo, playwright |
| API / backend | `security-best-practices` o `supabase-postgres-best-practices` + `vitest` | tests, curl |
| Base de datos | `supabase-postgres-best-practices` (+ `security-best-practices` si hay auth o RLS) | psql/supabase, migraciones |
| Seguridad / auth | `security-threat-model` + `security-best-practices` | auditoría de deps, playwright |
| Deploy / infra | `security-best-practices` + `playwright` (smoke) o `vitest` | CI, logs, rollback |
| Documentación de entrega | `brand` o `office-*`/`changelog-automation` según el entregable | office-*, wordcraft |
| SEO / GEO | `seo` o `seo-technical` + `seo-geo` + `ui-verification` (CWV) | browseros-neo, playwright |
| Marketing | `product-marketing` o `copywriting` + `cro`/`launch` | browseros-neo |
| 3D | `threejs` (web) o `media-use`/`canvas-design` (assets) + verificación del export | threejs, visor |
| QA | `code-review-and-quality` + `playwright`/`vitest`/`ui-verification` | navegador, tests |

La tabla fija el **mínimo**, no el máximo. Si ninguna encaja, se busca (fuentes en `skills-seleccion.md`) y se propone instalar; improvisar sin declararlo es incumplimiento.

## Herramientas: la misma ley

Comprueba **qué herramienta existe** y usa la correcta: `browseros-neo` (web real y logins), `playwright` (e2e), `agent-desktop` (GUI), `office-*`/`wordcraft` (documentos), `pdfcraft` (PDF), `threejs` (3D web), `cadcraft`/`solidcraft` (CAD). Declara cuáles usaste y con qué resultado: hacer a mano lo que una herramienta disponible hace mejor también es un fallo de proceso.

## Waivers (excepciones)

Solo cubren trabajo **trivial o mecánico**: renombrar, copiar texto, formatear, ajustar un enlace. **Nunca** diseño, seguridad, datos reales, publicación, QA ni documentación de entrega. Sin waiver aprobado por El Jefe **no se empieza**; el registro va en `docs/memoria/40-skills.md`:

```markdown
| ID | Tarea | Motivo | Alternativa aplicada | Aprueba | Fecha |
|---|---|---|---|---|---|
| W-01 | Renombrar campos del JSON de ejemplo | mecánico, sin lógica | revisión manual del diff | El Jefe | 2025-01-31 |
```

## Evidencia en el reporte

Todo entregable termina con este bloque; sin él, El Jefe lo devuelve:

```markdown
## Skills y herramientas
| Skill | Por qué | Dónde se aplicó | Resultado |
|---|---|---|---|
| `ui-design` | jerarquía visual y responsive | `src/pages/*` | aplicado; auditoría sin hallazgos |
| `ui-verification` | probar foco y overflow | navegador | 6 comprobaciones, 2 fallos corregidos |

Descartadas: `motion-design` — no había movimiento implicado.
Waivers: ninguno. Herramientas: browseros-neo (capturas), vitest (12 tests).
```

## Puerta de El Jefe

Por hito: revisa el registro y la evidencia, **muestrea un entregable** contra lo que la skill declarada exige y devuelve lo que no lo cumpla. Una fase sin skill y sin waiver es **fallo de proceso**, no un detalle: se repite el trabajo o se documenta la excepción aprobada. No vale "lo hice de memoria" ni una lista de skills sin efecto en el entregable.

## Registro persistente

`docs/memoria/40-skills.md` guarda el mapa fase → skills/herramientas/evidencia, los waivers y los huecos. Se crea con `python scripts/skills_check.py --init <proyecto>`, se actualiza con la memoria y **sobrevive a compactaciones y sesiones nuevas**. `python scripts/skills_check.py <proyecto>` falla (exit 1) si falta el fichero, si una fila no declara skills y herramientas y no tiene waiver, o si quedan `TBD`/`pendiente`/celdas vacías.

## Descubrimiento e instalación

Fuentes: las de `skills-seleccion.md`. Flujo: **propuesta** (skill, fase, fuente y licencia) → **aprobación de El Jefe** (🟡 local) → **usuario** (🔴 global o licencia dudosa). Tras instalar: verifica `name:`/`description:`, añádela a la matriz y re-ejecuta el inventario.

## Auditoría de cierre

1. ¿Cada fase cerrada tiene fila con skills, herramientas y evidencia real?
2. ¿Se muestreó algún entregable contra la skill declarada, o se aceptó a ciegas?
3. ¿Faltó alguna skill o se aplicó mal? → hueco o propuesta en `40-skills.md`.

## Anti-patrones

- **"Yo ya sé hacerlo"**: no cargar la skill y trabajar de memoria.
- **Cargar 6 skills y no aplicar ninguna**: coleccionismo, no triaje.
- **Declarar sin leer**: listar skills en el reporte sin haberlas abierto.
- **Saltarse el triaje por prisa**: el atajo de hoy es la deuda de mañana.
- **Usar solo la skill de costumbre**: elegir por hábito, no por tarea.
