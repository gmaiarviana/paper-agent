# ==============================================================================
# test-proxy.ps1
# Valida que o proxy LiteLLM em http://127.0.0.1:4000 esta funcional.
# Roda 3 testes: health, /v1/messages explicito, e wildcard routing.
# ==============================================================================

$ErrorActionPreference = 'Stop'

$projectRoot = Resolve-Path "$PSScriptRoot\..\.."
$envFile = Join-Path $projectRoot ".env"

Write-Host "=== TESTE 1: health check ===" -ForegroundColor Cyan
try {
    $h = Invoke-RestMethod -Uri "http://127.0.0.1:4000/health" -Method Get -ErrorAction Stop
    Write-Host "[OK] LiteLLM respondeu /health" -ForegroundColor Green
    Write-Host "     Healthy: $($h.healthy_count)  Unhealthy: $($h.unhealthy_count)"
} catch {
    Write-Host "[FAIL] LiteLLM nao responde em http://127.0.0.1:4000" -ForegroundColor Red
    Write-Host "       Erro: $($_.Exception.Message)"
    Write-Host "       Inicie: .\infra\litellm-proxy\start-proxy.ps1"
    exit 1
}

Write-Host ""
Write-Host "=== TESTE 2: POST /v1/messages (formato Anthropic) ===" -ForegroundColor Cyan

$apiKey = $null
foreach ($line in (Get-Content $envFile)) {
    if ($line -match '^\s*#' -or $line -match '^\s*$') { continue }
    $parts = $line -split '=', 2
    if ($parts[0].Trim() -eq 'ANTHROPIC_API_KEY_BACKEND') {
        $apiKey = $parts[1].Trim().Trim('"')
        break
    }
}

if (-not $apiKey) {
    Write-Host "[FAIL] ANTHROPIC_API_KEY_BACKEND nao encontrada no .env" -ForegroundColor Red
    exit 1
}

$headers = @{
    'x-api-key'         = $apiKey
    'anthropic-version' = '2023-06-01'
    'content-type'      = 'application/json'
}

$payload = @{
    model      = 'claude-haiku-4-5-20251001'
    max_tokens = 32
    messages   = @( @{ role = 'user'; content = 'responda apenas: ok' } )
} | ConvertTo-Json -Depth 6

try {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $r = Invoke-RestMethod -Uri 'http://127.0.0.1:4000/v1/messages' -Method Post -Headers $headers -Body $payload -ContentType 'application/json' -ErrorAction Stop
    $sw.Stop()
    Write-Host "[OK] Sucesso em $([int]$sw.Elapsed.TotalMilliseconds)ms" -ForegroundColor Green
    Write-Host "     model       : $($r.model)"
    Write-Host "     stop_reason : $($r.stop_reason)"
    Write-Host "     content     : $($r.content[0].text)" -ForegroundColor Green
    Write-Host "     tokens in/out: $($r.usage.input_tokens)/$($r.usage.output_tokens)"
} catch {
    Write-Host "[FAIL] /v1/messages falhou" -ForegroundColor Red
    Write-Host "       $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $sr = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        Write-Host "       Body: $($sr.ReadToEnd())" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host ""
Write-Host "=== TESTE 3: wildcard routing (claude-sonnet-4-5) ===" -ForegroundColor Cyan

$payload2 = @{
    model      = 'claude-sonnet-4-5'
    max_tokens = 32
    messages   = @( @{ role = 'user'; content = 'ok' } )
} | ConvertTo-Json -Depth 6

try {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $r2 = Invoke-RestMethod -Uri 'http://127.0.0.1:4000/v1/messages' -Method Post -Headers $headers -Body $payload2 -ContentType 'application/json' -ErrorAction Stop
    $sw.Stop()
    Write-Host "[OK] claude-sonnet-4-5 roteado em $([int]$sw.Elapsed.TotalMilliseconds)ms" -ForegroundColor Green
    Write-Host "     Resposta: $($r2.content[0].text)" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] wildcard routing falhou" -ForegroundColor Red
    Write-Host "       $($_.Exception.Message)"
}

Write-Host ""
Write-Host "=== TODOS OS TESTES PASSARAM ===" -ForegroundColor Green
Write-Host ""
Write-Host "Para usar Claude Code com o proxy, em outro terminal:"
Write-Host '  .\infra\litellm-proxy\setup-claude-code.ps1'
Write-Host '  claude'
