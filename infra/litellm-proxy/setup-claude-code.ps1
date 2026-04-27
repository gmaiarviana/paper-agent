# ==============================================================================
# setup-claude-code.ps1
# Configura env vars na sessao atual do PowerShell para o Claude Code falar
# com o proxy LiteLLM local em vez de api.anthropic.com.
#
# Uso:
#   .\infra\litellm-proxy\setup-claude-code.ps1
#   claude
# ==============================================================================

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Configurando Claude Code para usar proxy LiteLLM local" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

Set-Item -Path "Env:ANTHROPIC_BASE_URL" -Value "http://localhost:4000"
# Chave dummy: o LiteLLM ignora e usa ANTHROPIC_API_KEY_BACKEND do .env
Set-Item -Path "Env:ANTHROPIC_API_KEY"  -Value "sk-litellm-master-dummy"

Write-Host ""
Write-Host "[OK] Variaveis configuradas:" -ForegroundColor Green
Write-Host "     ANTHROPIC_BASE_URL = $env:ANTHROPIC_BASE_URL" -ForegroundColor Gray
Write-Host "     ANTHROPIC_API_KEY  = sk-litellm-master-dummy" -ForegroundColor Gray
Write-Host ""
Write-Host "Agora rode o Claude Code nesta mesma sessao:" -ForegroundColor Cyan
Write-Host "     claude" -ForegroundColor White
Write-Host ""
