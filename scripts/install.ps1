param(
  [string]$ProfileName = 'desktop',
  [string]$AgentsSkillsDir = (Join-Path $HOME '.agents\skills'),
  [switch]$SkipPreset,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$dshHome = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $HOME '.dsh' }
$profilePatch = Join-Path $dshHome "profiles\$ProfileName\cordis.patch.yml"
$stamp = Get-Date -Format 'yyyyMMddHHmmss'

Write-Host "El Jefe Stack - instalacion" -ForegroundColor Cyan
Write-Host "  DSH_HOME: $dshHome"
Write-Host "  perfil:   $ProfileName"
Write-Host "  skills:   $AgentsSkillsDir"
if ($DryRun) { Write-Host "  (dry run: no se escribe nada)" -ForegroundColor Yellow }

# 1) Skill del equipo
$srcSkill = Join-Path $repoRoot 'skills\el-jefe-team'
$dstSkill = Join-Path $AgentsSkillsDir 'el-jefe-team'
if (-not (Test-Path (Join-Path $srcSkill 'SKILL.md'))) { throw "No encuentro $srcSkill\SKILL.md" }
if ($DryRun) {
  Write-Host "[dry] copiaria $srcSkill -> $dstSkill"
} else {
  New-Item -ItemType Directory -Path $AgentsSkillsDir -Force | Out-Null
  if (Test-Path $dstSkill) {
    $backup = "$dstSkill.bak-$stamp"
    Copy-Item $dstSkill $backup -Recurse -Force
    Write-Host "  backup skill: $backup"
  }
  Copy-Item $srcSkill $dstSkill -Recurse -Force
  Write-Host "  skill instalada: $dstSkill" -ForegroundColor Green
}

# 2) Preset (override de standard)
if ($SkipPreset) {
  Write-Host "  preset: omitido (-SkipPreset)" -ForegroundColor Yellow
} else {
  if (-not (Test-Path $profilePatch)) { throw "No existe el patch del perfil: $profilePatch" }
  $presetPath = Join-Path $repoRoot 'preset\el-jefe.patch.yml'
  $preset = [System.IO.File]::ReadAllText($presetPath)
  $current = [System.IO.File]::ReadAllText($profilePatch)
  $marker = 'Preset standard redefinido'
  if ($current -match [regex]::Escape($marker)) {
    Write-Host "  preset: ya aplicado (se deja como esta)" -ForegroundColor Yellow
  } elseif ($DryRun) {
    Write-Host "[dry] anadiria $presetPath al final de $profilePatch"
  } else {
    $backup = "$profilePatch.bak-$stamp"
    Copy-Item $profilePatch $backup -Force
    Write-Host "  backup patch: $backup"
    $nuevo = $current.TrimEnd() + "`r`n`r`n" + $preset.TrimEnd() + "`r`n"
    [System.IO.File]::WriteAllText($profilePatch, $nuevo, (New-Object System.Text.UTF8Encoding $false))
    Write-Host "  preset aplicado: $profilePatch" -ForegroundColor Green
  }
}

Write-Host ""
Write-Host "Siguiente:" -ForegroundColor Cyan
Write-Host "  1. Instala las skills externas de skills/catalog.md (npx skills add ...)."
Write-Host "  2. Reinicia DSH si no hay HMR y crea una sesion nueva."
Write-Host "  3. El chip debe decir 'El Jefe'. Saluda y pide un proyecto."
