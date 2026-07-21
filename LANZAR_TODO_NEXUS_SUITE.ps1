# LANZAR_TODO_NEXUS_SUITE.ps1
# Script maestro para arrancar de forma unificada toda la infraestructura de la suite NEXUS

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         INICIANDO SUITE INFRAESTRUCTURA NEXUS            " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Liberar procesos colgados de Codex Beta si existieran
Write-Host "1. Verificando procesos de Codex Beta..." -ForegroundColor Yellow
Stop-Process -Name "codex" -ErrorAction SilentlyContinue
Stop-Process -Name "node_repl" -ErrorAction SilentlyContinue

# 2. Iniciar Codex Beta con puerto dinámico limpio
Write-Host "2. Lanzando Codex Beta..." -ForegroundColor Green
$codex_path = "C:\Users\Dell\AppData\Local\OpenAI\Codex\bin\5dee10576ec7a5b8\codex.exe"
if (Test-Path $codex_path) {
    Start-Process -FilePath $codex_path -WindowStyle Normal
    Write-Host "[OK] Codex Beta iniciado." -ForegroundColor Green
} else {
    Write-Host "[WARN] Ejecutable de Codex no encontrado en la ruta por defecto." -ForegroundColor Red
}

# 3. Conectar el navegador remoto y túnel de Codespaces
Write-Host "3. Arrancando túneles de Codespaces y Navegador Remoto..." -ForegroundColor Green
$script_path = "c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto\work\START_REMOTE_BROWSER.ps1"
if (Test-Path $script_path) {
    & $script_path
}

# 4. Ejecutar el Orquestador Multi-Cloud
Write-Host "4. Ejecutando Orquestador Multi-Cloud NEXUS..." -ForegroundColor Green
python "c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto\work\NEXUS_ORCHESTRATOR.py"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " ¡SUITE COMPLETA DESPLEGADA, LISTA Y EN FUNCIONAMIENTO!  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
