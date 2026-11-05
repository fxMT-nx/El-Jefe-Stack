# Memoria viva del proyecto

**Regla:** si no está en disco, no existe. La conversación se compacta y las sesiones se cierran; la memoria del proyecto no.

## Quién la mantiene

- **El Jefe es el responsable último**: ninguna sesión termina sin que la memoria esté al día.
- `memoria` la escribe y valida; `documentador` deja la bitácora de cambios; el resto de especialistas aportan datos verificados.
- El Jefe puede delegar la escritura, pero **verifica** el resultado antes de cerrar.

## Cuándo se actualiza

- Al **arrancar** una sesión (leer, no escribir).
- Tras cada **decisión**, requisito nuevo o preferencia del usuario.
- Antes de una **compactación** de contexto.
- Tras cada **hito**.
- Al **cerrar** sesión (obligatorio).
- Al cambiar alcance, stack, entorno o descubrir un riesgo.

## Estructura

```
docs/
├── estado.md              # SNAPSHOT (≤1.5 KB) + dashboard del proyecto
├── memoria/
│   ├── 00-indice.md       # cómo leer/actualizar, fecha, orden de lectura
│   ├── 10-proyecto.md     # objetivo, alcance, no-objetivos, usuarios
│   ├── 20-usuario.md      # lo que el usuario quiere y decide (ver abajo)
│   ├── 30-decisiones.md   # registro de decisiones; enlaces a ADR
│   ├── 50-tecnico.md      # stack, mapa del repo, comandos, entornos, trampas
│   ├── 60-tareas.md       # hecho / en curso / siguiente; enlace al tablero
│   ├── 70-riesgos.md      # riesgos, dependencias, supuestos, bloqueos
│   ├── 80-preguntas.md    # preguntas abiertas para el usuario
│   └── 90-historial.md    # sesiones: fecha, qué pasó, cómo se retoma
├── adr/                   # decisiones duras (formato ADR)
├── trabajo.md             # bitácora de cambios (documentador)
└── ideas.md               # ideas y backlog
GLOSSARY.md                # vocabulario del dominio (raíz)
```

Crea solo los ficheros que hagan falta; el núcleo mínimo es `estado.md`, `00-indice.md`, `10-proyecto.md`, `20-usuario.md`, `60-tareas.md`, `80-preguntas.md` y `90-historial.md`.

## Snapshot de `docs/estado.md` (obligatorio, ≤1.5 KB)

Es lo primero que lee una sesión nueva tras una compactación. Sin esto, la memoria es un archivo muerto.

```markdown
# Estado — <proyecto>
> Actualizado: AAAA-MM-DD HH:MM · Sesión: <nombre/id> · Fase: <...>

## Objetivo
<una frase>

## Hecho
- <hito verificable>

## En curso
- <trabajo + quién>

## Siguiente paso
- <acción concreta>

## Decisiones vigentes
- <decisión> (ADR-000X)

## Riesgos / bloqueos
- <riesgo + mitigación>

## Preguntas abiertas
- <pregunta> (ver 80-preguntas)

## Cómo retomar
<comandos, rutas, entorno>
```

## Qué guardar

- Requisitos, no-objetivos y criterios de aceptación.
- **Lo del usuario**: preferencias de tono/idioma, stack que quiere o veta, plazos, aprobaciones dadas, cosas que no se tocan, decisiones que solo él puede tomar, contexto personal relevante. Sepáralo de las decisiones técnicas: es su carril.
- Decisiones con porqué y alternativa descartada (ADR si es difícil de revertir).
- Contratos, modelos, glosario, comandos y entornos.
- Trampas conocidas, riesgos, dependencias y supuestos.
- Pendientes con dueño y siguiente acción.
- Registro de sesiones (fecha, qué se hizo, cómo se retoma).

## Qué NO guardar

- Secretos, tokens, contraseñas o claves (solo referencia a dónde están).
- PII innecesaria o volcados de logs conversaciones completas y material efímero.
- Datos sin verificar como si fueran hechos: si no se comprobó, se marca como supuesto.

## Protocolo por sesión

1. **Arranque.** Lee `docs/estado.md`, `docs/memoria/00-indice.md`, `GLOSSARY.md`, `80-preguntas.md` y la última entrada de `90-historial.md`. Saluda con un resumen de 5 líneas y el siguiente paso. No preguntes lo que ya está escrito.
2. **Durante.** Cada decisión, requisito o preferencia se escribe **en el momento** (o se encarga y se verifica). Las tareas van al tablero.
3. **Antes de compactar.** Actualiza el snapshot y `60/70/80`. Nada importante debe quedar solo en el chat.
4. **Cierre.** Actualiza `90-historial.md` (fecha, objetivo, hecho, decisiones, archivos tocados, siguiente paso, preguntas abiertas) y el snapshot. Si el proyecto usa git y el usuario lo permite, commit con mensaje claro.
5. **Sesión nueva.** Repite el paso 1; continúa desde el siguiente paso. No re-preguntes ni re-decidas lo ya cerrado.

## Compactación y sesiones nuevas

- La compactación borra contexto, **no disco**. El snapshot debe bastar para reconstruir el estado.
- Después de compactar, El Jefe relee estado + índice; si el snapshot no basta, lo mejora antes de seguir.
- Una sesión nueva no hereda el chat: hereda la memoria. Si falta algo, se escribe ahora para la próxima.

## Calidad

- Hechos verificados (comando, ruta, enlace), fechas reales, enlaces relativos correctos.
- Snapshot ≤1.5 KB; el resto se lee en 2 minutos.
- Sin secretos; sin duplicar: enlaza a `GLOSSARY.md`, ADR, `trabajo.md` e `ideas.md`.
- Una decisión reemplazada se marca, no se borra.
- Validación: `python scripts/memory_check.py <ruta-del-proyecto>` revisa estructura, snapshot, tamaño, enlaces, secretos y frescura; `--init` crea el esqueleto.
