param(
  [string]$ProfileName = 'desktop',
  [string]$AgentsSkillsDir = (Join-Path $HOME '.agents\skills')
)

$script:ok = $true
function Check {
  param([string]$Label, [bool]$Cond)
  if ($Cond) { Write-Host "[OK]    $Label" -ForegroundColor Green }
  else { Write-Host "[FALTA] $Label" -ForegroundColor Red; $script:ok = $false }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$dshHome = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $HOME '.dsh' }
$profilePatch = Join-Path $dshHome "profiles\$ProfileName\cordis.patch.yml"

Write-Host "El Jefe Stack - verificacion" -ForegroundColor Cyan

$skill = Join-Path $AgentsSkillsDir 'el-jefe-team\SKILL.md'
Check "skill el-jefe-team instalada" (Test-Path $skill)
if (Test-Path $skill) {
  $refs = (Get-ChildItem (Join-Path $AgentsSkillsDir 'el-jefe-team\references') -File -ErrorAction SilentlyContinue | Measure-Object).Count
  Check "fichas de referencia ($refs/21)" ($refs -eq 21)
  foreach ($ref in @('triaje-skills.md','skills-seleccion.md','criterio.md','acabados.md','puertas-calidad.md','coordinacion.md')) {
    Check "referencia $ref" (Test-Path (Join-Path $AgentsSkillsDir "el-jefe-team\references\$ref"))
  }
  $txt = [System.IO.File]::ReadAllText($skill)
  Check "SKILL.md dentro del limite de 8192" ($txt.Length -le 8192)
  Check "roster completo (becario, seo-geo, documentador)" ($txt -match 'becario' -and $txt -match 'seo-geo' -and $txt -match 'documentador')
  Check "fase 0 grilling en el manual" ($txt -match 'Fase 0: Grilling')
  Check "ley de triaje en el manual" ($txt -match 'triaje' -and $txt -match '40-skills.md')
  Check "seccion criterio y acabados" ($txt -match 'Criterio y acabados')
  Check "anti-patron de entregar generico" ($txt -match 'Entregar gen')
  Check "plantilla de revision de acabados" (Test-Path (Join-Path $repoRoot 'templates\revision-acabados.md'))
  $tplRepo = Join-Path $repoRoot 'templates\revision-acabados.md'
  $tplLive = Join-Path $AgentsSkillsDir 'el-jefe-team\templates\revision-acabados.md'
  Check "plantilla de revision en la skill viva" (Test-Path $tplLive)
  if ((Test-Path $tplRepo) -and (Test-Path $tplLive)) {
    Check "plantilla repo=vivo (sha256)" ((Get-FileHash $tplRepo -Algorithm SHA256).Hash -eq (Get-FileHash $tplLive -Algorithm SHA256).Hash)
  }
}

Check "script skills_check.py" (Test-Path (Join-Path $repoRoot 'scripts\skills_check.py'))
Check "script skill_pack.py" (Test-Path (Join-Path $repoRoot 'scripts\skill_pack.py'))
Check "plantilla skills-plan.md" (Test-Path (Join-Path $repoRoot 'templates\skills-plan.md'))

# Skills curadas de criterio (v1.6.0): 17 instaladas, cada una con su SOURCE.md
$curadas = @(
  'copy-editing','marketing-psychology','analytics','attribution','customer-research',
  'ux-heuristics','obviously-awesome','influence-psychology','jobs-to-be-done','monetizing-innovation','improve-retention',
  'founder-cfo','founder-pricing','founder-offer',
  'taste-design-review','taste-ux-copy','taste-accessibility'
)
$instaladas = 0
$conFuente = 0
foreach ($s in $curadas) {
  if (Test-Path (Join-Path $AgentsSkillsDir "$s\SKILL.md")) { $instaladas++ }
  if (Test-Path (Join-Path $AgentsSkillsDir "$s\SOURCE.md")) { $conFuente++ }
}
Check "17 skills curadas instaladas ($instaladas/17)" ($instaladas -eq 17)
Check "SOURCE.md de las curadas ($conFuente/17)" ($conFuente -eq 17)

Check "patch de perfil existe" (Test-Path $profilePatch)
if (Test-Path $profilePatch) {
  $p = [System.IO.File]::ReadAllText($profilePatch)
  Check "override de preset aplicado (marcador presente)" ($p -match 'Preset standard redefinido')
  Check "persona El Jefe presente" ($p -match 'Eres El Jefe')
  Check "fase 0 grilling en la persona" ($p -match 'Fase 0: antes de planificar')
  Check "triaje obligatorio en la persona" ($p -match 'Ninguna fase sin triaje')
  Check "criterio y acabados en la persona" ($p -match 'Juzga con criterio de negocio')
  Check "sin preset nuevo declarado (evita dsh-scope)" (-not ($p -match 'id: preset-jefe'))
}

foreach ($s in @('grilling','domain-modeling','seo','copywriting','emil-design-eng','ui-animation','threejs')) {
  Check "skill externa: $s" (Test-Path (Join-Path $AgentsSkillsDir "$s\SKILL.md"))
}

$packer = Join-Path $repoRoot 'scripts\skill_pack.py'
if (Test-Path $packer) {
  & python $packer --audit | Out-Null
  Check "ninguna skill supera 8192 caracteres reales" ($LASTEXITCODE -eq 0)
  & python $packer --verify | Out-Null
  Check "paquetes de skills integros (--verify)" ($LASTEXITCODE -eq 0)
}

Write-Host ""
if ($script:ok) {
  Write-Host "Todo listo. Abre DSH, crea sesion nueva y comprueba que el chip dice 'El Jefe'." -ForegroundColor Green
} else {
  Write-Host "Faltan cosas: revisa docs/INSTALL.md." -ForegroundColor Yellow
  exit 1
}
