# Criterio: cómo se decide

Del equipo: **no enseña a ejecutar, enseña a elegir y a rechazar.** Si no sobrevive aquí, no se construye. Review: [`acabados.md`](acabados.md) · Triaje: [`triaje-skills.md`](triaje-skills.md).

## 1. Jerarquía cuando hay conflicto

**1. Confianza y marca** (que nos crea mañana) → **2. Accesibilidad** (que lo use quien lo necesita) → **3. Corrección técnica** (que lo dicho sea verdad) → **4. Psicología y crecimiento** (que más gente lo use).

Manda el de la izquierda: los tres primeros cuestan años; el cuarto se itera. La psicología entra **al final, como lente sobre algo ya construido** (ux-psychology-skill).

**Conflicto resuelto.** Cuenta atrás falsa de 24 h en el descuento anual y renovación premarcada (+15%): rompe el nivel 3. La casilla premarcada vende algo que nadie pidió: rompe el nivel 1. **Veredicto: se caen las dos; queda el descuento real con fecha publicada y cancelación en un clic.** Regla: **si para subir la métrica hay que engañar a alguien, el nivel 1 ya respondió.**

## 2. Negocio

- **Precio entre la siguiente mejor alternativa (SBA) y el valor percibido**; el coste es suelo, nunca base (`pricing`). Pregunta: *¿qué usa hoy si no existiéramos?* Casi siempre gana **no hacer nada**.
- **Posicionamiento = contexto, no mensaje** (Dunford): **categoría** (en qué caja nos meten), **alternativa** (qué sustituimos), **valor único** (lo que nadie más puede decir). Si falta una, es eslogan.
- **ICP con must / nice / disqualifying.** Sin disqualifying no hay ICP, hay lista de deseos: nombra 3 clientes que **no** lo son.
- **Unit economics:** LTV/CAC ≥ 3 · payback ≤ 12 meses (≤ 6 self-serve) · margen bruto ≥ 70% software, ≥ 40% servicio. **Un CAC que no se puede medir no es un canal: es una esperanza.**
- **No aplican** en enterprise > 12 meses (payback), marketplace (contribución por transacción), SEO (coste por visita) ni pre-PMF (retención, no LTV).
- **Kernel** (Rumelt): **diagnóstico** (el obstáculo en una frase) → **apuesta** (política que descarta, no una meta) → **acciones coherentes**; una mediocre que encaja gana a una brillante que contradice. No-estrategia: relleno, no nombrar el desafío, metas por estrategia, puré de iniciativas.
- **Señal vs vanidad.** Señal cambia una decisión (activación, retención por cohorte, margen); vanidad sube sin cambiar nada (visitas, seguidores). Test: *si bajara un 30%, ¿harías algo distinto?* Si no, es vanidad.

## 3. Psicología

- **Carga cognitiva.** Hick (1952): más opciones, más tiempo. Miller (1956) mide **chunks**, no pantallas: tope de grupos, no permiso para 7 ítems. Regla: **1 decisión por pantalla, ≤ 5 opciones visibles, ≤ 7 en menú**.
- **Fricción con número:** 3 campos = base; 4–6 → −10/−25% de completado; 7+ → −25/−50% (`cro`). Antes de añadir un campo: ¿hace falta *antes* de ayudar?, ¿se obtiene de otro modo?, ¿se pide después?
- **Confianza = prueba específica:** autoridad (quién lo dice y por qué le crees), prueba social concreta («4.812 pedidos en Madrid en 2025» > «miles de clientes»), transparencia (precio final, datos, cómo cancelar, contacto). Si necesitas «líder» o «innovador», no tienes prueba (Cialdini).
- **Pérdida y anclaje.** Una pérdida pesa ~2× la ganancia (Kahneman-Tversky, 1979: heurística, no dato citable). El primer número fija el juicio: referencia antes del precio, tres planes con el medio como objetivo.
- **Fogg, B = MAP.** Falla el que falta. Antes de «motivar más», **sube habilidad** (quita pasos) o mueve el prompt al momento: un CTA que falla es habilidad o prompt, no deseo.
- **Hábitos** (Eyal): disparador → acción → recompensa variable → inversión. Solo en uso diario; **nunca en facturación ni en lo irreversible.**

| Persuasión | Dark pattern |
|---|---|
| escasez real, con stock y fecha | cuenta atrás que se reinicia |
| recomendar lo que de verdad encaja | casilla premarcada, opt-out escondido |
| recordar lo que el usuario empezó | culpa, miedo, «lo vas a perder todo» |
| cancelar tan fácil como contratar | laberinto de retención, «llama tú» |

**Test único: ¿el usuario, al entender exactamente lo que hiciste, te lo agradecería?** Si no, es dark pattern; y si solo funciona mientras no entiende, no es persuasión: es engaño.

## 4. Producto

- **JTBD.** «Cuando <situación>, quiero <motivación>, para <resultado>»: funcional, emocional y social. Sin trabajo nombrado no se puede juzgar una feature.
- **Time-to-value:** minutos del alta al primer resultado real; < 5 min self-serve o el onboarding fabrica uno intermedio.
- **Onboarding:** un camino, no un tour; primer estado con datos reales. Se mide **activación**, no el % que acabó el tour.
- **Retención por cohorte.** La media global sube aunque la retención empeore si creces. Semana 1 y mes 1; curva que no se aplana = no es hábito (`improve-retention`).
- **Churn causal.** Instrumenta el evento previo a la baja (última acción, ticket, uso) y entrevista a 5 bajas separando motivo declarado del real: «es caro» casi siempre es «no llegó al valor».

## 5. Decisiones

- **Regla escrita antes de los datos:** Promote / Rollback / Keep-testing con umbral y ventana fijados antes de mirar; lo demás es racionalización.
- **Expected / Reads / Writes / Done** en cada encargo: qué se espera, qué se lee, qué se escribe y cuándo termina. Sin contrato no hay veredicto.
- **Compute, don't eyeball.** Totales, tasas y deltas salen de filas con script; nunca gasto de un periodo completo entre conversiones de uno parcial (`analytics`).
- **Muestra precomprometida.** Parar cuando «ya gana» es *peeking*: 1% de base × 20% de mejora ≈ 43.000 por variante (`ab-testing`). Cohorte dentro de su ventana = pendiente, no fracasada.
- **Rúbrica 0–10 canónica, con el hueco declarado:** la de [`acabados.md`](acabados.md) §4 (9–10 publicable · 7–8 retoques · 5–6 otra pasada · 3–4 rehacer capas · 0–2 no es un entregable), con nota por capa, filas que fallan y arreglo para llegar a 10. No hay otra escala: la de `ux-heuristics` y cualquier externa se traducen a esa antes de decidir. Sin nota es opinión.
- **Antes de culpar al cliente, revisa tu proceso.** La explicación por defecto («no entiende») casi nunca es la buena.
- **Una sola fuente de verdad para contar:** Google 50, Meta 40, GA 60 y el CRM 35 **no suman**. Una cuenta (backend/CRM), las demás explican de dónde vino, y la brecha se declara (`attribution`).

## 6. Interrogatorio antes de aprobar

1. **Negocio:** ¿qué cambia, en qué número y en cuánto tiempo?
2. **Usuario:** ¿quién exactamente y qué trabajo intenta hacer?
3. **Alternativa:** ¿qué usa hoy y por qué se cambiaría?
4. **Evidencia:** ¿qué lo prueba, y si es opinión, qué dato la haría hecho?
5. **Trade-off:** ¿qué empeora si sale bien? Si nada, no lo entiendes.
6. **Coste de error:** si falla, ¿qué se rompe y cómo se revierte?
7. **Ética:** ¿lo entendería y lo agradecería?
8. **Métrica:** señal, umbral y cuándo se lee.
9. **Reversibilidad:** ¿abre o cierra puertas? Irreversible = más evidencia.
10. **Fracaso:** ¿qué lo haría fracasar aun bien ejecutado, y lo comprobamos?

Un «no lo sé» no se tapa con entusiasmo: **no se aprueba la propuesta, se aprueba la investigación.**
