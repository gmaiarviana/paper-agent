# ==============================================================================
# setup-opencode.ps1
# Carrega OPENWEBUI_API_KEY e OPENWEBUI_BASE_URL do .env da raiz do projeto
# para a sessao atual do PowerShell. O opencode.json (na raiz) referencia
# essas duas variaveis via {env:VAR_NAME}, falando OpenAI direto com o
# OpenWebUI da Atlantico (sem passar pelo proxy LiteLLM, que so e necessario
# para clientes Anthropic-format como Claude Code).
#
# Uso:
#   .\infra\litellm-proxy\setup-opencode.ps1
#   opencode  # abre a TUI interativa
#   # ou: opencode run "sua tarefa aqui"
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

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Configurando OpenCode para usar OpenWebUI" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

Set-Item -Path "Env:OPENWEBUI_API_KEY" -Value $openWebUiApiKey
Set-Item -Path "Env:OPENWEBUI_BASE_URL" -Value $openWebUiBaseUrl

Write-Host ""
Write-Host "[OK] Variaveis configuradas:" -ForegroundColor Green
Write-Host "     OPENWEBUI_BASE_URL = $env:OPENWEBUI_BASE_URL" -ForegroundColor Gray
Write-Host "     OPENWEBUI_API_KEY  = [carregada do .env]" -ForegroundColor Gray
Write-Host ""
Write-Host "Provider 'atlantico' configurado em opencode.json (raiz do repo)." -ForegroundColor Cyan
Write-Host "Modelos disponiveis: gpt-oss:20b (default), qwen3.6:35b, llama3.2:3b" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para usar:" -ForegroundColor Cyan
Write-Host "     opencode                      # abre TUI interativa" -ForegroundColor White
Write-Host "     opencode run 'sua tarefa'     # modo headless" -ForegroundColor White
Write-Host "     opencode models atlantico     # lista modelos" -ForegroundColor White
Write-Host ""
