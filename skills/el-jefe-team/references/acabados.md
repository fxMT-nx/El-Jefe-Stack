# Acabados: lo que el usuario juzga

Criterio y review de calidad **percibida**. Para decidir qué se construye: [`criterio.md`](criterio.md). Triaje: [`triaje-skills.md`](triaje-skills.md). Plantilla: `revision-acabados.md`, en `templates/` del repo del stack.

## 1. Qué es un acabado

**Definición operativa:** el conjunto de decisiones que el usuario nota sin poder nombrarlas. Un entregable *funciona* cuando hace lo que dice el brief; está *acabado* cuando alguien que no lo escribió lo usa sin que le expliquen nada y sin desconfiar.

- **Es lo último que se nota y lo primero que se juzga.** Nadie evalúa tu arquitectura ni tus horas: en ~50 ms decide si esto parece serio (Lindgaard et al., 2006) y en 8 segundos si entiende qué es y qué hacer.
- **No se compara con el ideal, sino con la última buena app que usó** (ley de Jakob). El acabado no compite con la perfección: compite con lo de al lado.
- **Un defecto de acabado cuesta más que su arreglo**, porque el usuario no reporta «tiene un bug»: concluye «esto no me da confianza» y se va en silencio.

## 2. Proceso de review

**No se arregla mientras se revisa.** Mezclar las dos cosas produce un informe de lo que tocaste, no de lo que falla (taste-design-review).

1. **8 segundos, sin scroll:** ¿qué es, para quién y qué se hace aquí? Si no puedes nombrar las tres, es P1 y ya sabes por dónde empezar.
2. **Captura:** 1440 · 768 · 390 px. Los estados se **fuerzan** (vacío, error, red lenta), no se esperan.
3. **Severidad:** **P0** roto, legal o bloqueante · **P1** socava la calidad · **P2** pulido · **P3** preferencia.
4. **Arreglo después**, por severidad y en cambios atómicos. Un P3 no se toca en la misma sesión que un P1.
5. **Verificación:** captura del mismo encuadre tras el arreglo, y comprobar que no rompió otra capa.
6. **Independencia:** quien construye no firma el veredicto. Como mínimo, lo revisa otro miembro del equipo con la plantilla delante.

## 3. Checklist por capas

| Capa | Se comprueba | Fallo típico |
|---|---|---|
| **Arranque y onboarding** | valor visible antes de pedir registro; datos de ejemplo; el primer estado enseña cómo se llena | registro obligatorio antes de ver nada |
| **Estados** | vacío (con acción), carga (esqueleto con la forma real), error (qué pasó + qué hacer + reintentar), parcial (qué falta), offline (qué se guarda) | spinner sin fin, que es un error disfrazado |
| **Formularios** | etiqueta visible (el placeholder no es etiqueta), error junto al campo y en texto, nunca solo en color, no se pierde lo escrito, `type` y autocomplete correctos | validar en rojo sin decir qué corregir |
| **Microcopy** | verbo + objeto («Guardar cambios», no «Aceptar»), específico con número o plazo, error que dice qué hacer; sin muletillas de IA («no es X, es Y», listas de negaciones) | «Algo salió mal», lorem ipsum, jerga interna |
| **Confianza** | precio total con impuestos antes de pagar, qué haces con los datos, cómo cancelar, quién está detrás, contacto | letra pequeña al final del embudo |
| **Rendimiento percibido** | esqueleto con la forma final, progreso si > 1 s, actualización optimista con reversión, espacio reservado (cero saltos de layout) | la pantalla salta cuando llega el dato |
| **Accesibilidad** | recorrido de teclado completo y en orden, foco visible en cada parada (2 px, 3:1, offset ≥ 2 px), etiqueta en cada campo, contraste 4.5:1 texto / 3:1 grande y UI, objetivos ≥ 24×24 px, `prefers-reduced-motion`, nada solo por color | `outline: none` sin sustituto |
| **Responsive y zoom** | 200 % sin scroll horizontal ni recortes; a 390 px nada cortado ni fuera de pantalla | tabla que empuja la página a lo ancho |
| **Consistencia** | mismo verbo para la misma acción, un solo botón primario por pantalla, mismo patrón en diálogos y vacíos | dos nombres para lo mismo |
| **Datos extremos** | 0, 1 y 10.000 filas; nombres de 60 caracteres; emoji, acentos, RTL; números grandes y negativos | columna que rompe el layout con un nombre largo |
| **Modo oscuro** | no es invertir: se revisan contraste, bordes, sombras e imágenes con fondo blanco | texto gris que desaparece |
| **Confirmar y deshacer** | destructivo confirmado nombrando el objeto; mejor `undo` que diálogo | borrar todo sin preguntar |

## 4. Rúbrica 0–10

| Banda | Significa | Qué se hace |
|:--:|---|---|
| 9–10 | se publica | nada |
| 7–8 | publicable con retoques | P2/P3 a la lista, se publica y se agenda |
| 5–6 | otra pasada | no se publica |
| 3–4 | capas a rehacer | vuelve al dueño con el hueco escrito |
| 0–2 | no es un entregable | se replantea |

**Condición de publicación:** ninguna P0/P1 abierta · **media ≥ 8** · **ninguna capa por debajo de 7** · evidencia adjunta. La media sola engaña: un 9 en copy con un 4 en formularios da 6,5 y no dice nada. Toda nota lleva **el hueco declarado** (qué falta exactamente para llegar a 10) o es una opinión.

## 5. Evidencia exigible

- Capturas a 1440/768/390 del **mismo recorrido**, antes y después.
- Recorrido de teclado: dónde está el foco en cada parada, si algo se queda atrapado o inalcanzable.
- Estados forzados: red lenta, error de servidor, vacío, permiso denegado.
- Contraste medido en los pares reales: texto/fondo, texto de botón, borde de input, placeholder.
- Nota por capa y lista de huecos con severidad.

Sin esto no hay veredicto: **«se ve bien» no es una revisión.**

## 6. Anti-patrones

| Anti-patrón | Por qué falla | Qué poner |
|---|---|---|
| «Algo salió mal» | no dice qué pasó ni qué hacer | qué falló, qué se conservó, botón de reintento |
| Lorem ipsum o «texto de ejemplo» | declara que nadie lo revisó | contenido real o vacío honesto |
| Botón deshabilitado sin motivo | el usuario no sabe qué le falta | habilitado con validación al enviar, o el motivo al lado |
| Éxito sin confirmación | el usuario repite la acción | confirmación explícita y el estado nuevo visible |
| 404 genérico | pierde la navegación | qué buscabas, enlaces útiles, buscador |
| Spinner infinito | es un error disfrazado | estado de error con reintento y tiempo |
| Placeholder como etiqueta | desaparece al escribir | etiqueta persistente |
| «Próximamente» en el menú | promesa vacía que ocupa sitio | se quita o se dice cuándo |
| Precio sin impuestos hasta el final | rompe la confianza justo al pagar | total antes de pagar |
| Modal para todo | interrumpe y acumula | en línea si cabe |

## 7. El veredicto

Cierra en un párrafo con **la nota por capa**, la **lista de huecos con severidad** y los cambios ordenados por impacto. Y nombra **un solo cambio** como el que más mueve la aguja: si no puedes elegirlo, la revisión no encontró el problema real (taste-design-review). Se publica con P0/P1 en cero y evidencia adjunta; si no, se devuelve con el hueco escrito, no con un «dale una vuelta».
