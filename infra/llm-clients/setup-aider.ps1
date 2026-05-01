# ==============================================================================
# setup-aider.ps1
# Configura env vars na sessao atual do PowerShell para o Aider falar
# diretamente com o OpenWebUI usando a chave do .env da raiz do projeto.
#
# Uso:
#   .\infra\litellm-proxy\setup-aider.ps1
#   .\.venv-aider\Scripts\aider.exe --model openai/gpt-oss:20b
# ==============================================================================

$ErrorActionPreference = 'Stop'

$projectRoot = Resolve-Path "$PSScriptRoot\..\.."
$envFile = Join-Path $projectRoot ".env"

if (-not (Test-Path $envFile)) {
    Write-Host "[FAIL] .env nao encontrado em $envFile" -ForegroundColor Red
    exit 1
}

$envMap = @{}
foreach ($line in (Get-Content $envFile)) {
    if ($line -match '^\s*#' -or $line -match '^\s*$') { continue }
    $parts = $line -split '=', 2
    if ($parts.Count -ne 2) { continue }
    $envMap[$parts[0].Trim()] = $parts[1].Trim().Trim('"')
}

$openWebUiApiKey = $envMap['OPENWEBUI_API_KEY']
$openWebUiBaseUrl = $envMap['OPENWEBUI_BASE_URL']

if (-not $openWebUiApiKey) {
    Write-Host "[FAIL] OPENWEBUI_API_KEY nao encontrada no .env" -ForegroundColor Red
    exit 1
}

if (-not $openWebUiBaseUrl) {
    Write-Host "[FAIL] OPENWEBUI_BASE_URL nao encontrada no .env" -ForegroundColor Red
    exit 1
}

$aiderApiBase = if ($openWebUiBaseUrl.EndsWith('/v1')) {
    $openWebUiBaseUrl
} else {
    "$openWebUiBaseUrl/v1"
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Configurando Aider para usar OpenWebUI" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

Set-Item -Path "Env:OPENAI_API_KEY" -Value $openWebUiApiKey
Set-Item -Path "Env:OPENAI_API_BASE" -Value $aiderApiBase
Set-Item -Path "Env:AIDER_OPENAI_API_KEY" -Value $openWebUiApiKey
Set-Item -Path "Env:AIDER_OPENAI_API_BASE" -Value $aiderApiBase

Write-Host ""
Write-Host "[OK] Variaveis configuradas:" -ForegroundColor Green
Write-Host "     OPENAI_API_BASE      = $env:OPENAI_API_BASE" -ForegroundColor Gray
Write-Host "     OPENAI_API_KEY       = [carregada do .env]" -ForegroundColor Gray
Write-Host "     AIDER_OPENAI_API_BASE = $env:AIDER_OPENAI_API_BASE" -ForegroundColor Gray
Write-Host "     AIDER_OPENAI_API_KEY  = [carregada do .env]" -ForegroundColor Gray
Write-Host ""
Write-Host "Agora rode o Aider nesta mesma sessao:" -ForegroundColor Cyan
Write-Host "     .\.venv-aider\Scripts\aider.exe --model openai/gpt-oss:20b" -ForegroundColor White
Write-Host ""