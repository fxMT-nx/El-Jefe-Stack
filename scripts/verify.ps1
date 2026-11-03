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
  Check "fichas de roles presentes ($refs ficheros)" ($refs -ge 10)
  $txt = [System.IO.File]::ReadAllText($skill)
  Check "roster completo (becario, seo-geo, documentador)" ($txt -match 'becario' -and $txt -match 'seo-geo' -and $txt -match 'documentador')
  Check "fase 0 grilling en el manual" ($txt -match 'Fase 0: Grilling')
}

Check "patch de perfil existe" (Test-Path $profilePatch)
if (Test-Path $profilePatch) {
  $p = [System.IO.File]::ReadAllText($profilePatch)
  Check "override de preset aplicado (marcador presente)" ($p -match 'Preset standard redefinido')
  Check "persona El Jefe presente" ($p -match 'Eres El Jefe')
  Check "fase 0 grilling en la persona" ($p -match 'Fase 0: antes de planificar')
  Check "sin preset nuevo declarado (evita dsh-scope)" (-not ($p -match 'id: preset-jefe'))
}

foreach ($s in @('grilling','domain-modeling','seo','copywriting','emil-design-eng','ui-animation')) {
  Check "skill externa: $s" (Test-Path (Join-Path $AgentsSkillsDir "$s\SKILL.md"))
}

Write-Host ""
if ($script:ok) {
  Write-Host "Todo listo. Abre DSH, crea sesion nueva y comprueba que el chip dice 'El Jefe'." -ForegroundColor Green
} else {
  Write-Host "Faltan cosas: revisa docs/INSTALL.md." -ForegroundColor Yellow
  exit 1
}
