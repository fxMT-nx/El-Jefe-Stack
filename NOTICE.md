# Avisos de terceros (NOTICE)

El contenido propio de este repositorio (preset, skill `el-jefe-team`, scripts, plantillas y documentación) está bajo **MIT** (ver [`LICENSE`](LICENSE)).

Este fichero reúne lo que no es propio. Nada de lo aquí listado se distribuye dentro del repositorio salvo que se diga expresamente: las skills externas se instalan desde sus repos originales y cada una conserva su licencia. Si redistribuyes alguna, cumple su licencia y conserva sus avisos.

## 1. DeepSeek Harness (DSH)

- **Qué es:** el producto sobre el que funciona este stack. El preset de El Jefe es un *patch* de configuración que compone plugins de `@deepseek-ai/dsh-*` y activa el bundle experimental **Agent Team**. Esos paquetes no se incluyen aquí.
- **Titularidad:** DSH y sus paquetes son de DeepSeek. Este repo no está afiliado, patrocinado ni respaldado por DeepSeek.
- **Estado:** Agent Team es un bundle experimental y su comportamiento puede cambiar entre versiones de DSH.
- **Marcas:** «DeepSeek» y «DeepSeek Harness» pertenecen a sus titulares. «El Jefe Stack» es el nombre de este proyecto no oficial.

## 2. Skills de terceros (no incluidas en el repo)

Las skills se instalan desde su repositorio original con `npx skills add` o copiando el directorio a `~/.agents/skills/`. La lista de qué aporta cada una y cómo se instalan está en [`skills/catalog.md`](skills/catalog.md).

| Repositorio | Licencia | Skills que usa este stack |
|---|---|---|
| [`mattpocock/skills`](https://github.com/mattpocock/skills) | MIT | `grilling`, `grill-me`, `grill-with-docs`, `domain-modeling` |
| [`wshobson/agents`](https://github.com/wshobson/agents) | MIT | `architecture-decision-records`, `changelog-automation` |
| [`emilkowalski/skills`](https://github.com/emilkowalski/skills) | MIT | `emil-design-eng`, `find-animation-opportunities`, `apple-design` |
| [`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill) | MIT | `motion-design` |
| [`mblode/agent-skills`](https://github.com/mblode/agent-skills) | MIT | `ui-animation` |
| [`anthropics/skills`](https://github.com/anthropics/skills) | Apache-2.0 (un `LICENSE.txt` por skill) | `frontend-design`, `algorithmic-art`, `canvas-design` |
| [`JetBrains/skills`](https://github.com/JetBrains/skills) | Sin licencia en la raíz del repo; ver §5 | `antfu-web-design-guidelines` |
| [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo) | MIT | `seo`, `seo-technical`, `seo-content`, `seo-schema`, `seo-geo` |
| [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills) | MIT | `product-marketing`, `copywriting`, `cro`, `emails`, `launch`, `copy-editing`, `marketing-psychology`, `analytics`, `attribution`, `customer-research` |
| [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) | MIT | `code-review-and-quality`, `code-simplification` |
| [`dmmulroy/anti-slop`](https://github.com/dmmulroy/anti-slop) | MIT | `install-anti-slop` |
| [`wondelai/skills`](https://github.com/wondelai/skills) | MIT | `ux-heuristics`, `obviously-awesome`, `influence-psychology`, `jobs-to-be-done`, `monetizing-innovation`, `improve-retention` |
| [`Jakeschincariol/founder-skill`](https://github.com/Jakeschincariol/founder-skill) | MIT | `founder-cfo`, `founder-pricing`, `founder-offer` |
| [`madebymustafa/design-taste`](https://github.com/madebymustafa/design-taste) | MIT | `taste-design-review`, `taste-ux-copy`, `taste-accessibility` |

**Las 17 skills curadas** (las cinco de `coreyhaines31/marketingskills`, las seis de `wondelai/skills`, las tres de `Jakeschincariol/founder-skill` y las tres de `madebymustafa/design-taste`) se instalan con un `SOURCE.md` que anota repo, commit exacto, licencia y fecha. Los commits usados en la verificación original:

- `coreyhaines31/marketingskills` @ `88c79f65`
- `wondelai/skills` @ `d8d5d75f`
- `Jakeschincariol/founder-skill` @ `fd9385b0`
- `madebymustafa/design-taste` @ `c4a6bff0`

## 3. Skill `threejs` de este repo

`skills/threejs/` es una skill **paraguas escrita para este proyecto**: frontmatter y reglas propias que remiten a las referencias del bundle [`CloudAI-X/threejs-skills`](https://github.com/CloudAI-X/threejs-skills) (MIT). `scripts/install_threejs_skill.py` descarga esos documentos originales en la instalación y los trocea; no se copian aquí. Three.js es de three.js authors, bajo licencia MIT.

## 4. Otros trabajos citados

- **Navegador de agentes (BrowserOS neo):** MCP opcional para research y QA web. Se configura en `preset/mcp-browseros.example.yml`; no se distribuye su software.
- **Skill-3D:** las mecánicas de recuperación y aprendizaje que inspiran `scripts/skill_router.py` y la retro se citan en `docs/ARQUITECTURA.md`; no se incluye su código.

## 5. Cómo se verificaron las licencias

Consulta del 2026-11-11 a los metadatos de licencia de cada repositorio en GitHub, más lectura del `LICENSE.txt` que algunas skills llevan dentro cuando el repo no tiene licencia en la raíz:

- **`anthropics/skills`**: sin licencia en la raíz. Las tres skills usadas (`frontend-design`, `algorithmic-art`, `canvas-design`) llevan su `LICENSE.txt` con **Apache-2.0**.
- **`JetBrains/skills`**: sin licencia en la raíz. Algunas skills del repo llevan `LICENSE.txt` con **Apache-2.0**, pero `antfu-web-design-guidelines` no incluye ninguno, así que su licencia **no está verificada** aquí. Trátala como texto de referencia: si la redistribuyes, comprueba sus términos en el repo original.

Los metadatos pueden cambiar. Si una skill o el catálogo de este repo indican otra licencia, prevalece la del repositorio original; este fichero recoge la verificación más reciente y no es asesoramiento legal.

## 6. Aviso

Este fichero es informativo y no sustituye a las licencias originales. Si encuentras una atribución incorrecta o incompleta, abre una incidencia en este repositorio y se corrige.
