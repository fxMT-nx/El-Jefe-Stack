# Toolkit 3D (opcional)

Inspirado en [Skill-3D](https://github.com/skill-3d/Skill-3D) (Apache-2.0): agentes que razonan sobre escenas 3D combinando herramientas de percepción y geometría, con una librería de skills y memoria de escena. Aquí se usa como **toolkit opcional** para `disenador-3d` y para tareas de visión 3D; no es necesario para modelado/export normal.

## Herramientas (servicios locales)

| Herramienta | Para qué | Env var / puerto |
|---|---|---|
| Depth Anything 3 | profundidad métrica, nearest/farthest, front/back | `DEPTH_SERVER_URL` / 20019 |
| SAM 3 | segmentación por máscaras, bordes, contactos | `SEGMENTATION_SERVER_URL` / 20020 |
| Grounding DINO | detección open-vocabulary con cajas reutilizables | `DETECTION_SERVER_URL` / 20022 |
| Pi3 | reconstrucción/geometría multi-vista (pesada) | `PI3_SERVER_URL` / 20030 |
| SwinIR | super-resolución/restauración de recortes pequeños o borrosos | `SWINIR_SERVER_URL` / 20032 |
| Orient Anything v2 | orientación/pose de objetos | `ORIENT_ANYTHING_SERVER_URL` / 20034 |

## Estrategia (por orden de coste)

1. **Localiza** los objetos relevantes (detección/segmentación) antes de medir.
2. **Mide profundidad** con recortes (`crop_box`, `crop_boxes`, puntos) en vez de imagen completa.
3. **Resuelve orientación** con Orient Anything sobre el recorte del objeto, no sobre la escena.
4. **Reconstruye** (Pi3) solo si la evidencia 2D no basta (oclusión, cambio de vista, layout).
5. **Restaura** (SwinIR) recortes pequeños/borrosos antes de concluir.
6. Verifica con una segunda fuente; si no hay acuerdo, dilo.

## Coste, permisos y límites

- Descargar checkpoints/modelos y instalar dependencias CUDA es **🔴**: lo decide el usuario (GBs, GPU, tiempo).
- Levantar servicios locales es **🟡**: lo aprueba El Jefe si es reversible y el equipo tiene GPU/RAM suficientes.
- Si no hay GPU o modelos, **no improvises**: usa el pipeline Blender/glTF (`disenador-3d`) y deja constancia de lo que falta.
- Los benchmarks de Skill-3D (VSI-Bench, BLINK, CV-Bench, MMSI-Bench) pueden servir para evaluar calidad de razonamiento espacial, no para producción.

## Referencias

- Repo: `skill-3d/Skill-3D` — `skill3d/core/skill_retrieval.py` (ranking de skills), `skill_learning.py` (éxitos → workflows, fallos → lecciones), `prompts_with_skills.py` (tool cards con cuándo usar cada herramienta).
- Nuestro ciclo de aprendizaje: `references/aprendizaje.md`.
