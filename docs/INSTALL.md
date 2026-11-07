# Instalación

Probado en Windows con DSH Desktop y perfil `desktop`. En macOS/Linux los pasos son los mismos cambiando rutas.

## 1. Copia la skill del equipo

PowerShell:

```powershell
$dest = Join-Path $HOME '.agents\skills\el-jefe-team'
if (Test-Path $dest) { Copy-Item $dest "$dest.bak-$(Get-Date -Format yyyyMMddHHmmss)" -Recurse }
Copy-Item '.\skills\el-jefe-team' $dest -Recurse -Force
```

Bash:

```bash
mkdir -p ~/.agents/skills
cp -R skills/el-jefe-team ~/.agents/skills/
```

DSH escanea `~/.agents/skills` y recarga el catálogo en caliente, sin reiniciar.

## 2. Aplica el preset

El archivo `preset/el-jefe.patch.yml` **no declara un preset nuevo**: redefine el preset `standard` sustituyendo su `config.plugins` (vía documentada). Declarar un preset nuevo desde la capa de usuario provoca `dsh-scope: scope key is already bound to a parent` al crear sesiones; no lo hagas.

1. Haz backup del patch de perfil:
   - Windows: `C:\Users\<usuario>\.dsh\profiles\desktop\cordis.patch.yml`
   - Si usas otro perfil: `~/.dsh/profiles/<perfil>/cordis.patch.yml`
2. Pega **al final** el contenido de `preset/el-jefe.patch.yml`.
3. Guarda. El HMR recompone el perfil; si tu build no tiene HMR, reinicia DSH.

Validación opcional (perfil no-`desktop`):

```bash
dsh --profile <perfil> --dump-config | grep -n "El Jefe"
```

En `desktop` el binario CLI no permite `--dump-config`; la prueba real es crear una sesión nueva y ver el chip **El Jefe**.

## 2b. Quita el tope de teammates

El bundle de Agent Team fija `maxMembers: 8` (Lead + 7). Para que El Jefe no tenga tope práctico, pega `preset/agent-team.patch.yml` **al final** del patch de perfil y reinicia DSH. Queda en 1000 entradas de roster por equipo (incluye fallidos). Sin reinicio no se aplica. Verifícalo en una sesión nueva creando más de 7 teammates.

## 3. Instala las skills externas

Las del equipo propio ya van en el paso 1. Las de diseño, SEO/GEO, marketing, documentación y calidad se instalan desde sus repos (elige `npx skills add` o copia manual):

```bash
# Entrevistas (fase 0)
npx skills add mattpocock/skills --skill grilling
npx skills add mattpocock/skills --skill grill-me
npx skills add mattpocock/skills --skill grill-with-docs
npx skills add mattpocock/skills --skill domain-modeling

# Diseño y animación
npx skills add emilkowalski/skills --skill emil-design-eng
npx skills add emilkowalski/skills --skill find-animation-opportunities
npx skills add emilkowalski/skills --skill apple-design
npx skills add LottieFiles/motion-design-skill
npx skills add mblode/agent-skills --skill ui-animation
npx skills add anthropics/skills --skill frontend-design
npx skills add anthropics/skills --skill algorithmic-art
npx skills add anthropics/skills --skill canvas-design
npx skills add JetBrains/skills --skill antfu-web-design-guidelines

# SEO/GEO y marketing
npx skills add AgriciDaniel/claude-seo
npx skills add coreyhaines31/marketingskills --skill copywriting ...
```

La lista completa con qué aporta cada una está en [`../skills/catalog.md`](../skills/catalog.md).

## 4. Comprueba

```powershell
.\scripts\verify.ps1
```

Y después, en DSH: **New session → chip "El Jefe" → "Hola, Jefe"**. Si el chip sigue diciendo "Standard", el override no se aplicó o no se recargó.

## Troubleshooting

| Síntoma | Causa / solución |
|---|---|
| `Could not switch to El Jefe: dsh-scope...` | Se declaró un preset nuevo desde patch de usuario. Quita ese bloque: usa solo el override de `standard`. |
| New session falla tras aplicar el patch | YAML inválido o `config` incompleto: restaura el backup y vuelve a pegar el bloque completo. |
| `agent-preset/invalid: tool-subagent-list-agents ... never started` | DSH ≥ 0.2.2-rc.1 eliminó ese paquete. Quita la fila `tool-subagent-list-agents` del preset y usa `modelSelection: true` + `modelDiscovery: true` en `tool-subagent`. Si el fichero ya está corregido, **reinicia DSH**: el preset se compone al arrancar. |
| El chip dice "Standard" | Override no aplicado (perfil equivocado) o DSH sin recarga: reinicia. |
| El Jefe no encuentra la skill | `~/.agents/skills/el-jefe-team/SKILL.md` no existe o el frontmatter está roto. |
| No aparecen `grilling`/`domain-modeling` en el catálogo | `grill-me` y `grill-with-docs` llevan `disable-model-invocation: true` (solo invocación manual); `grilling` y `domain-modeling` sí deben aparecer. |

Restaurar el patch:

```powershell
Copy-Item "$HOME\.dsh\profiles\desktop\cordis.patch.yml.bak-*" "$HOME\.dsh\profiles\desktop\cordis.patch.yml"
```
