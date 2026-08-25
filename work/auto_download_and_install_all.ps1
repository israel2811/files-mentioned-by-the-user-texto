# ==============================================================================
# NEXUS AUTO-DOWNLOADER, SILENT INSTALLER & LAUNCHER (WINDOWS .EXE)
# ==============================================================================
$DownloadDir = "C:\Users\Dell\Downloads\NEXUS_AI_INSTALLERS"
if (-not (Test-Path $DownloadDir)) {
    New-Item -ItemType Directory -Path $DownloadDir -Force | Out-Null
}

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     NEXUS AUTO-DOWNLOADER & SILENT INSTALLER (WINDOWS)        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# 1. Ollama Windows Installer
$OllamaExe = "$DownloadDir\OllamaSetup.exe"
Write-Host "`n[1/3] Descargando e instalando Ollama Setup..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $OllamaExe -TimeoutSec 120
    Write-Host "[✓] OllamaSetup.exe descargado. Ejecutando instalador..." -ForegroundColor Green
    Start-Process $OllamaExe -ArgumentList "/silent" -Wait
    Write-Host "[✓] Ollama instalado." -ForegroundColor Green
    Start-Process "ollama" -ArgumentList "app" -ErrorAction SilentlyContinue
} catch {
    Write-Host "[WARN] Descargador de Ollama reintentando o continuando en segundo plano: $_" -ForegroundColor DarkYellow
}

# 2. OpenCode CLI vía PowerShell Installer
Write-Host "`n[2/3] Instalando OpenCode nativo..." -ForegroundColor Yellow
try {
    Invoke-Expression "& { $(Invoke-RestMethod https://opencode.ai/install.ps1) }"
    Write-Host "[✓] OpenCode instalado." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Reintentando vía npm..." -ForegroundColor DarkYellow
    npm install -g opencode-ai
}

# 3. Aider Chat (Python)
Write-Host "`n[3/3] Instalando Aider Chat..." -ForegroundColor Yellow
python -m pip install --upgrade aider-chat

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "     ABRIENDO TODAS LAS APLICACIONES INSTALADAS EN VIVO        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Abrir ventana interactiva de cada aplicación
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '=== OPENCODE RUNNING ===' -ForegroundColor Cyan; if (Get-Command opencode -ErrorAction SilentlyContinue) { opencode } else { Write-Host 'OpenCode listo en terminal.' }"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '=== AIDER RUNNING ===' -ForegroundColor Yellow; if (Get-Command aider -ErrorAction SilentlyContinue) { aider } else { Write-Host 'Aider listo en terminal.' }"
Start-Process "ollama" -ArgumentList "serve" -ErrorAction SilentlyContinue

Write-Host "[✓] Todo descargado, instalado y abierto en tu pantalla." -ForegroundColor Green
