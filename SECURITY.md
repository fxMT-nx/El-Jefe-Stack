# Seguridad

## Versiones cubiertas

Este proyecto es experimental y no tiene ramas de mantenimiento. Solo se atienden vulnerabilidades en la última revisión de `main` (o en el último tag publicado, si lo hay). Si usas una copia antigua, actualiza antes de reportar.

## Cómo reportar una vulnerabilidad

Usa el **reporte privado de GitHub Security Advisories**: en este repositorio, pestaña **Security** → **Advisories** → **Report a vulnerability**. El aviso llega solo a los mantenedores y permite hablar del fallo sin publicarlo.

No abras una incidencia pública con los detalles ni los publiques en otro sitio antes de que haya una corrección. Si el formulario no está disponible, abre una incidencia **sin detalles técnicos** pidiendo un canal privado.

Incluye lo que puedas de esto: versión de DSH y de este repo, sistema operativo, pasos para reproducir, impacto que le ves, y si tienes una prueba de concepto. Si el fallo está en una skill de terceros o en DSH, dilo: se redirige a quien corresponde en vez de duplicarlo.

No hay correo de seguridad ni recompensas económicas. La respuesta es en el mejor plazo posible, sin SLA.

## Qué cubre este aviso

| Dentro del alcance | Fuera del alcance |
|---|---|
| `preset/*.yml`: composición de plugins, persona y permisos del preset | DSH, sus paquetes `@deepseek-ai/*` y el bundle Agent Team (repórtalo a DeepSeek) |
| `scripts/*.ps1` y `scripts/*.py`: copia de ficheros, backups, rutas, descargas, validación | Skills de terceros instaladas desde otros repos (repórtalo a su mantenedor) |
| `skills/el-jefe-team/`: contenido que puede inducir al agente a una acción insegura | Tu propia configuración de DSH, tu red o tu máquina |
| `templates/` y documentación: instrucciones que terminan en acciones del agente | Ingeniería social contra ti o contra tu equipo |

## Qué hace este stack en tu máquina

Para que puedas valorar el riesgo antes de ejecutarlo:

- `scripts/install.ps1` copia `skills/el-jefe-team` a `%USERPROFILE%\.agents\skills\el-jefe-team`. Si ya existe, guarda una copia `*.bak-<fecha>` antes de sobrescribir.
- El mismo script **añade** el bloque de `preset/el-jefe.patch.yml` al final de `%USERPROFILE%\.dsh\profiles\<perfil>\cordis.patch.yml`, con copia de seguridad previa. Ese fichero es la configuración de DSH: el preset cambia la persona del agente y la lista de herramientas disponibles.
- `scripts/validate_repo.py`, `verify.ps1`, `skill_router.py`, `skills_check.py`, `skill_pack.py` y `memory_check.py` trabajan solo con ficheros locales. No envían datos a ningún sitio.
- `scripts/install_threejs_skill.py` es el único script del repo que sale a la red: descarga documentos de `raw.githubusercontent.com` del repo `CloudAI-X/threejs-skills`.
- El repo no incluye telemetría, analítica ni cuentas de servicio.

Los pasos manuales de instalación (pegar el preset, instalar skills con `npx skills add`) los ejecuta quien instala, con su criterio.

## Instalar skills de terceros es tu decisión

Una skill es un conjunto de instrucciones que tu agente lee y sigue. Una skill maliciosa o descuidada puede pedirle que lea, escriba o publique cosas que tú no querías. Por eso este repo **no vendoriza** las skills externas ([`NOTICE.md`](NOTICE.md)):

- instálalas desde su repositorio original y, si puedes, fija el commit;
- lee el `SKILL.md` antes de instalarla, sobre todo si pide credenciales, red o permisos de escritura;
- conserva el `SOURCE.md` y la licencia que deja la instalación;
- si una skill se comporta raro, quítala y revísala: el problema es de la skill, no de este stack.

## Si encuentras un fallo en este repo

Además del reporte privado, agradecemos un PR con la corrección y una prueba que la demuestre (un caso en `validate_repo.py` o un paso reproducible en el PR). Las correcciones de seguridad se publican en [`docs/CHANGELOG.md`](docs/CHANGELOG.md) cuando ya hay arreglo disponible.
