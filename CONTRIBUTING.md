# Contribuir

Gracias por el interés. Este repo es pequeño y experimental, así que el listón es la claridad: un cambio tiene que explicar qué problema resuelve y cómo se comprueba.

## Qué encaja aquí

- **Correcciones** de documentación, rutas, enlaces o scripts.
- **Skills propias** que aporten una disciplina que el roster no cubre, con su ficha y su justificación.
- **Roles nuevos** para `agents/`, siguiendo [`agents/new-role-template.md`](agents/new-role-template.md).
- **Mejoras de las plantillas** de memoria, plan o revisión de acabados.
- **Entradas de catálogo** para skills de terceros que merezcan la pena, con repo, licencia y para qué.

No encaja aquí el contenido de una skill de terceros: eso se corrige en su repositorio original ([`NOTICE.md`](NOTICE.md) tiene la lista).

## Antes de abrir nada

1. Lee [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) para no duplicar una pieza que ya existe.
2. Para cambios en la skill o el preset, instala el stack en local siguiendo [`docs/INSTALL.md`](docs/INSTALL.md).
3. Si propones una skill o un rol, ten claro **qué fase del trabajo mejora** y **qué evidencia lo demuestra**. «Suena útil» no basta.

## Estándar de una skill o un rol

**Skill** (`skills/<nombre>/SKILL.md`):

- Frontmatter YAML con `name` (minúsculas, guiones, igual que la carpeta) y `description` que diga qué hace y cuándo se usa.
- `SKILL.md` de **8.192 caracteres o menos**. DSH recorta los resultados de herramienta a ese tamaño en las versiones probadas, así que una skill más larga llega al agente a medias. Si no cabe, parte el cuerpo en `references/` y deja en `SKILL.md` el frontmatter, la intro, las reglas que no pueden perderse y un índice con enlaces relativos. `python scripts/skill_pack.py --split <nombre>` hace ese troceo y `--verify` comprueba que no se ha perdido texto.
- Referencias en Markdown, con enlaces relativos que resuelvan desde la skill.
- Nada de rutas personales (`C:\Users\...`, `$HOME` de otra máquina), secretos ni tokens.
- Texto en español, como el resto del repo.

**Rol** (`agents/custom/<nombre>.md` si se reutiliza):

- Misión, cuándo sí y cuándo no, brief mínimo, entregable con evidencia, checklist y límites.
- De 1 a 3 skills por rol. Cuatro o cinco exigen justificar qué disciplina extra las pide y qué se descarta; más de cinco no se aceptan.
- Si el rol no aporta criterio propio, es trabajo para el generalista.

**Preset**: los cambios en `preset/el-jefe.patch.yml` deben conservar `config.id: standard` y explicar en el PR por qué el cambio no rompe la composición de plugins ni el arranque de sesiones.

## Validar antes de enviar

```bash
python -m pip install pyyaml
python scripts/validate_repo.py
```

`validate_repo.py` comprueba el YAML del preset y de la skill, los enlaces relativos, que los scripts compilan, el protocolo de triaje y el empaquetador de skills, con casos de prueba reales. Tiene que terminar en `validación OK`.

Si tienes el stack instalado en tu máquina, además:

```powershell
.\scripts\verify.ps1
```

`verify.ps1` mira también tu instalación viva (`~/.agents/skills`, patch del perfil, skills externas). Es normal que falle en un clon recién descargado sin skills externas: en ese caso lee qué marca como `[FALTA]` y compáralo con [`docs/INSTALL.md`](docs/INSTALL.md).

Si tocas una skill larga:

```bash
python scripts/skill_pack.py --audit
python scripts/skill_pack.py --verify
```

Antes de enviar el PR, ejecuta la validación en local: `python scripts/validate_repo.py` tiene que terminar en `validación OK`, y si tienes el stack instalado, `.\scripts\verify.ps1` en verde. Un PR con la validación en rojo no se revisa.

## Commits

- Formato: `tipo: resumen en una línea` con `feat`, `fix`, `docs`, `chore`, `test` o `refactor`. Ejemplo: `fix: corrige el enlace al catálogo en el README`.
- Un tema por commit. Si el cambio mezcla un arreglo y una funcionalidad, sepáralo.
- El cuerpo explica **por qué**, no qué (el diff ya dice qué).
- Cambios visibles para quien usa el stack: añade la entrada en [`docs/CHANGELOG.md`](docs/CHANGELOG.md).
- Nada de binarios, `__pycache__`, backups ni artefactos de editor.

## Lo que no se acepta

- Secretos, tokens, claves, datos personales o rutas de tu máquina.
- Capturas con información privada.
- Promesas de compatibilidad que no se hayan probado.
- Copiar texto de una skill de terceros sin su licencia y su atribución.
- Cambios de formato masivos mezclados con contenido: dificultan la revisión y se rechazan.

## Licencia de las contribuciones

Al enviar un cambio aceptas que se publique bajo la **licencia MIT** de este repositorio (ver [`LICENSE`](LICENSE)). No hay CLA ni cesión de derechos: conservas tu autoría y la atribución queda en el historial de git. Para contenido de terceros, respeta su licencia y añade la entrada en [`NOTICE.md`](NOTICE.md).

## Revisión

- Un mantenedor revisa el PR, comprueba la validación en verde y prueba el cambio si afecta a la instalación.
- Se puede pedir una segunda opinión si el cambio toca el preset o los scripts de instalación.
- Si el PR se queda sin respuesta, vuelve a escribir en el hilo. No abras otro con lo mismo.

## Cómo nos tratamos

Discute el contenido, no a la persona; supón buena fe; explica el desacuerdo con datos. El acoso, los ataques personales y la divulgación de datos privados no tienen sitio aquí. Los problemas de conducta se reportan en privado por el mismo canal que las vulnerabilidades ([`SECURITY.md`](SECURITY.md)).
