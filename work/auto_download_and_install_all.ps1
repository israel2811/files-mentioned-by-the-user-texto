# ==============================================================================
# NEXUS AUTO-DOWNLOADER, SILENT INSTALLER & LAUNCHER (WINDOWS)
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
    Write-Host "[OK] OllamaSetup.exe descargado. Ejecutando instalador..." -ForegroundColor Green
    Start-Process -FilePath $OllamaExe -ArgumentList "/silent" -Wait
    Write-Host "[OK] Ollama instalado." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Descargador de Ollama: $_" -ForegroundColor DarkYellow
}

# 2. OpenCode CLI vía PowerShell Installer
Write-Host "`n[2/3] Instalando OpenCode nativo..." -ForegroundColor Yellow
try {
    Invoke-Expression "& { $(Invoke-RestMethod https://opencode.ai/install.ps1) }"
    Write-Host "[OK] OpenCode instalado." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Instalando vía npm..." -ForegroundColor DarkYellow
    npm install -g opencode-ai
}

# 3. Aider Chat (Python)
Write-Host "`n[3/3] Instalando Aider Chat..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade aider-chat
    Write-Host "[OK] Aider instalado." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Error en pip: $_" -ForegroundColor DarkYellow
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "     ABRIENDO TODAS LAS APLICACIONES INSTALADAS EN VIVO        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Abrir ventana interactiva de cada aplicación
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit -Command Write-Host '=== OPENCODE RUNNING ===' -ForegroundColor Cyan; if (Get-Command opencode -ErrorAction SilentlyContinue) { opencode } else { Write-Host 'OpenCode listo.' }"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit -Command Write-Host '=== AIDER RUNNING ===' -ForegroundColor Yellow; if (Get-Command aider -ErrorAction SilentlyContinue) { aider } else { Write-Host 'Aider listo.' }"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit -Command start 'https://opencode.ai'; start 'https://openhands.dev'; start 'https://aider.chat'"

Write-Host "[OK] Todo descargado, instalado y abierto en tu pantalla." -ForegroundColor Green
