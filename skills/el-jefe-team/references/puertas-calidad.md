# Puertas de calidad

Una puerta es una condición **verificable** para aceptar un entregable: sin evidencia no se cruza y «debería funcionar» no abre ninguna. Qué decidir y qué rechazar: [`criterio.md`](criterio.md). Cómo se juzga lo que el usuario percibe: [`acabados.md`](acabados.md). Plantilla de revisión: `templates/revision-acabados.md`.

## Regla común

- **Evidencia o no cuenta.** Test, comando, captura o fuente con su ejecución real y su fecha; la salida se pega, no se resume de memoria.
- **Independencia.** Quien construye no firma su propia revisión: la hace otro miembro y, si hay UI o datos, como mínimo `qa-critico`.
- **Criterio declarado en el encargo.** Todo brief dice con qué se aceptará: usuario y trabajo que resuelve, número de negocio que mueve y acabado esperado. Sin esa línea, el especialista entrega lo que le parece.
- **Devolver, no parchear.** Lo que no cumple vuelve a su dueño con el hueco escrito y su severidad; El Jefe no reescribe el trabajo ajeno.

## Por tipo de entregable

| Entregable | Puerta |
|---|---|
| Código nuevo | compila + tests relevantes en verde + sin secretos en el diff + `code-review-and-quality` |
| UI / visual | estados vacío, carga, error y parcial + a11y (foco, teclado, contraste 4,5:1) + responsive 200 % + **revisión de acabados con capturas** 1440/768/390 y nota ≥ 8 sin P0/P1 |
| API | validación de entrada, errores tipados, authz probada (incluye denegaciones), migración reversible |
| Seguridad | permisos mínimos, dependencias auditadas, hallazgos con severidad y fix |
| Datos / infra | despliegue, rollback y backup probados; observabilidad sin PII |
| Documentación | hechos verificados, comandos probados, audiencia declarada |
| Memoria | `docs/estado.md` al día con decisiones, pendientes y siguiente paso |
| SEO / GEO | metadatos, schema y CWV verificados; contenido citable |
| Marketing | claims comprobables con fuente, unit economics (LTV/CAC, payback, margen) y métricas definidas antes de publicar |
| Copy / microcopy | sin muletillas de IA (`copy-editing`, `taste-ux-copy`); verbo + objeto; el error dice qué hacer |
| Diseño / UX | `ux-heuristics` o `taste-design-review` con hallazgos por severidad y arreglo propuesto |
| 3D | escala y unidades, orientación, presupuesto de triángulos, materiales PBR y export probado en el destino |

## Revisión P0–P3 (la que más devuelve)

1. **Lectura de 8 segundos** a 1440 px sin scroll: qué es, para quién y qué se hace aquí.
2. **Capturas** 1440/768/390 del mismo recorrido y de los estados forzados (vacío, error, red lenta).
3. **Severidad:** P0 roto, legal o bloqueante · P1 socava la calidad · P2 pulido · P3 preferencia.
4. **Nota por capa** de 0 a 10 con el hueco declarado: qué falta exactamente para llegar a 10.
5. **Veredicto:** se publica con media ≥ 8, ninguna capa por debajo de 7 y cero P0/P1; si no, vuelve con los huecos escritos y ordenados por impacto.

La media sola engaña: un 9 en copy con un 4 en formularios es 6,5 y no dice nada. Y quien construye no firma el veredicto.

## Anti-patrones de puerta

- Puerta firmada por quien construyó, o «se ve bien» como revisión.
- Captura solo del caso feliz; estados de error «ya se probarán».
- Aceptar un entregable genérico o de plantilla sin una decisión reconocible (ver `criterio.md`).
- Arreglar durante la revisión: se convierte en el informe de lo tocado, no de lo que falla.
- Dar por bueno un P1 abierto porque la media sale alta.
