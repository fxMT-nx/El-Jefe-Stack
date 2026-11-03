# Permisos y escalado

Ningún especialista decide por su cuenta una acción sensible: primero pide permiso a El Jefe y espera respuesta. El Jefe aprueba lo local y reversible dentro del plan y escala al usuario lo que no le corresponde decidir. **Ningún teammate pregunta directamente al usuario**: todas las preguntas suben por El Jefe.

**El usuario es la última autoridad: no hay acciones vetadas de antemano por el equipo.** Lo que normalmente no se hace no es un "nunca": es una decisión del usuario, que se consulta por acción antes de ejecutarla y que solo él puede autorizar.

## Zonas de riesgo

| Zona | Ejemplos | Quién decide |
|---|---|---|
| 🟢 Verde | leer, editar dentro de su scope, tests, formato, crear archivos del proyecto | el trabajador (lo deja en su reporte) |
| 🟡 Amarilla | tocar fuera de su scope, dependencia nueva, migración/BD local, borrar archivos ajenos, levantar servidores o puertos, instalar herramientas del proyecto, `git commit`/rama de su trabajo, web con login | pide permiso a **El Jefe** |
| 🔴 Roja | producción/deploy, dinero o coste cloud, datos reales o personales, credenciales/secretos, push a ramas protegidas o releases, publicar hacia fuera, instalar software global o del sistema, comandos destructivos (drop DB, force push, borrados masivos), emails/mensajes en nombre del usuario, compras, sistemas de terceros, y cualquier acción excepcional o con consecuencias serias no cubierta arriba | **El Jefe pregunta al usuario** antes, por acción |

## Acciones excepcionales

Si el usuario autoriza expresamente algo que normalmente no se hace, se ejecuta **solo esa acción y solo dentro de ese alcance**, y queda registrado quién la autorizó y cuándo. Sin autorización explícita, no se ejecuta. Si la acción tiene implicaciones legales, de seguridad o sobre terceros, El Jefe expone las consecuencias antes de pedir la autorización.

## Flujo

1. El especialista detecta una acción amarilla o roja y **no la ejecuta**. Manda a El Jefe: qué quiere hacer, por qué, alcance, riesgo y plan alternativo si se niega.
2. El Jefe responde: **aprobado** (con condiciones), **denegado** (con alternativa) o **lo consulto al usuario**. Si queda bloqueado, que siga con otra cosa.
3. Si es roja, excepcional o El Jefe lo considera necesario, El Jefe pregunta al usuario: acción propuesta, impacto, coste, si es reversible y su recomendación. Preguntas cortas y concretas, una decisión por bloque.
4. Toda aprobación queda registrada: en el tablero si afecta a una tarea y en `docs/estado.md`/ADR si cambia el proyecto (lo deja `memoria`).

## Criterio de El Jefe al aprobar

¿Está en el plan? ¿Es local? ¿Es reversible? ¿Cabe en el alcance del encargo? Si falla una, para y escala.

## Plantilla de solicitud (teammate → El Jefe)

```
quiero: <acción concreta>
por qué: <para qué sirve en la tarea>
alcance: <archivos/sistemas/entorno afectados>
riesgo: <qué puede romper, coste, reversibilidad>
alternativa: <si se deniega, qué haré>
```

## Plantilla de escalado (El Jefe → usuario)

```
necesito tu permiso para: <acción>
quién lo pide y para qué: <miembro + tarea>
impacto: <datos/sistemas/usuarios afectados>
coste: <dinero/tiempo/recursos>
reversible: <sí/no + cómo>
mi recomendación: <sí/no + por qué>
```

> Nota: esta política es del equipo, no un sandbox. El límite duro lo pone la política de permisos de DSH (Settings → Permission preset: sandbox y aprobaciones). Si quieres cinturón y tirantes, el usuario puede bajar el preset a `workspace-write`.
