# ==============================================================================
# start-proxy.ps1
# Inicia o proxy LiteLLM na porta 4000 com a config local.
# Pode ser invocado de qualquer diretorio: resolve a raiz via $PSScriptRoot.
# ==============================================================================

$ErrorActionPreference = 'Stop'

# Raiz do projeto = duas pastas acima deste script (infra/litellm-proxy/..)
$projectRoot = Resolve-Path "$PSScriptRoot\..\.."
$venvActivate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"
$litellmExe   = Join-Path $projectRoot ".venv\Scripts\litellm.exe"
$envFile      = Join-Path $projectRoot ".env"
$configFile   = Join-Path $PSScriptRoot "litellm-config.yaml"

Write-Host "=== Iniciando LiteLLM Proxy na porta 4000 ===" -ForegroundColor Cyan
Write-Host "    projectRoot: $projectRoot" -ForegroundColor DarkGray

# 1. Ativar venv da raiz do projeto
if (-not (Test-Path $venvActivate)) {
    Write-Host "[FAIL] venv nao encontrada: $venvActivate" -ForegroundColor Red
    Write-Host "       Crie a venv e instale deps: pip install -r infra\litellm-proxy\requirements.txt" -ForegroundColor Yellow
    exit 1
}
& $venvActivate

# 2. Carregar .env da raiz (sem exportar ANTHROPIC_BASE_URL — essa eh do Claude
#    Code, nao do LiteLLM. Se vazar pro env do proxy, ele chama a si mesmo em loop)
if (-not (Test-Path $envFile)) {
    Write-Host "[FAIL] .env nao encontrado em $envFile" -ForegroundColor Red
    exit 1
}
$skipKeys = @('ANTHROPIC_BASE_URL')
foreach ($line in (Get-Content $envFile)) {
    if ($line -match '^\s*#' -or $line -match '^\s*$') { continue }
    $parts = $line -split '=', 2
    $k = $parts[0].Trim()
    $v = $parts[1].Trim().Trim('"')
    if ($skipKeys -contains $k) {
        Write-Host "[SKIP] $k nao sera exportado pro LiteLLM" -ForegroundColor Yellow
        continue
    }
    Set-Item -Path "Env:$k" -Value $v
    if ($k -eq 'ANTHROPIC_API_KEY_BACKEND') {
        Write-Host "[OK] ANTHROPIC_API_KEY_BACKEND carregada" -ForegroundColor Green
    }
}
Remove-Item Env:ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue

# 3. Liberar porta 4000 se ja estiver em uso
$conns = Get-NetTCPConnection -LocalPort 4000 -State Listen -ErrorAction SilentlyContinue
if ($conns) {
    foreach ($c in $conns) {
        Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    Write-Host "[OK] Porta 4000 liberada" -ForegroundColor Green
} else {
    Write-Host "     Porta 4000 ja estava livre"
}

# 4. UTF-8 e unbuffered: sem isso o banner ASCII-art do LiteLLM explode com
#    UnicodeEncodeError no console CP1252 do Windows
$env:LITELLM_LOG = "INFO"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$env:PYTHONUNBUFFERED = "1"

Write-Host ""
Write-Host "Iniciando: litellm --config $configFile --port 4000"
Write-Host "Pressione Ctrl+C para parar."
Write-Host ""

& $litellmExe --config $configFile --port 4000
