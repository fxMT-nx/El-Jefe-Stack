# Aprendizaje del equipo (retro y lecciones)

Inspirado en el ciclo de Skill-3D: los rollouts exitosos se convierten en **workflows reutilizables** y los fallidos en **lecciones correctivas**. El equipo no aprende solo por acumular historia: promueve una lección cuando se repite y se verifica.

## Cuándo

- Al cerrar cada proyecto o hito relevante.
- Después de un fallo que costó tiempo o dinero.
- Cuando una skill o combinación de skills funcionó especialmente bien.

## Cómo (retro en 10 minutos)

1. `documentador` rellena `templates/retro.md` con: objetivo, qué se hizo, qué funcionó, qué falló, skills usadas, decisiones y qué cambiaría.
2. El Jefe distingue **éxito** (workflow a repetir) de **fallo** (lección correctiva); no mezclar.
3. Se guarda en `docs/aprendizaje.md` del proyecto (o en el histórico del stack si es transversal).
4. **Promoción**: una lección se convierte en cambio estable solo si se repite en ≥2 proyectos distintos o es un fallo grave:
   - actualizar la ficha de rol (`references/roles-*.md`),
   - ajustar la matriz o los triggers de `skills-seleccion.md`,
   - o crear una skill nueva (con `agents/new-role-template.md` y validación).
5. Se registra el cambio en `CHANGELOG.md` y, si toca una regla, en un ADR (`docs/adr/`).

## Reglas

- No se aprende de un caso único y raro: se anota como observación, no como regla.
- Nada de lecciones basadas en recuerdos: se apoyan en evidencia (diff, tests, logs, fechas).
- Las lecciones caducan: si el stack o el contexto cambian, se revisan.
- El usuario decide si una lección cambia el comportamiento del equipo cuando afecta a permisos, coste o alcance.

## Formato de lección

```
- fecha: AAAA-MM-DD
- contexto: <proyecto, stack, tarea>
- tipo: éxito | fallo | observación
- lección: <una frase accionable>
- evidencia: <test/log/diff/enlace>
- cambio propuesto: <ficha, matriz, skill, regla>
- estado: propuesta | promovida | descartada
```
