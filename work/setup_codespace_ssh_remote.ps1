# setup_codespace_ssh_remote.ps1
# Configura el acceso SSH persistente para Codespaces en Windows OpenSSH / VS Code / Antigravity Remote Explorer

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   NEXUS Codespaces Remote SSH Configurator             " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Verificar si GitHub CLI (gh) está instalado
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] GitHub CLI ('gh') no está instalado o no se encuentra en el PATH." -ForegroundColor Red
    Write-Host "Descárgalo de https://cli.github.com/ o instálalo vía 'winget install GitHub.cli'" -ForegroundColor Yellow
    exit 1
}

# 2. Generar configuración SSH de Codespaces
Write-Host "[1/3] Generando configuración SSH para Codespaces..." -ForegroundColor Yellow
try {
    gh codespace ssh --config | Out-File -FilePath "$HOME\.ssh\config_codespaces" -Encoding ascii
    Write-Host "[OK] Configuración guardada en $HOME\.ssh\config_codespaces" -ForegroundColor Green
} catch {
    Write-Host "[WARN] No se pudo exportar directamente. Asegúrate de estar logueado con 'gh auth login'." -ForegroundColor Yellow
}

# 3. Integrar en ~/.ssh/config principal
$mainSshConfig = "$HOME\.ssh\config"
$includeLine = "Include config_codespaces"

if (Test-Path $mainSshConfig) {
    $content = Get-Content $mainSshConfig -Raw
    if ($content -notmatch "config_codespaces") {
        Add-Content -Path $mainSshConfig -Value "`n# NEXUS Codespaces Integration`n$includeLine`n"
        Write-Host "[2/3] Integrado 'Include config_codespaces' en $mainSshConfig" -ForegroundColor Green
    } else {
        Write-Host "[2/3] 'config_codespaces' ya estaba incluido en $mainSshConfig" -ForegroundColor Green
    }
} else {
    New-Item -ItemType File -Path $mainSshConfig -Force | Out-Null
    Set-Content -Path $mainSshConfig -Value "# NEXUS Codespaces Integration`n$includeLine`n"
    Write-Host "[2/3] Creado $mainSshConfig con inclusión de Codespaces" -ForegroundColor Green
}

# 4. Listar Codespaces activos disponibles para conexión
Write-Host "[3/3] Consultando lista de Codespaces disponibles..." -ForegroundColor Yellow
gh codespace list

Write-Host "`n[LISTO] Ahora puedes abrir la barra lateral de 'Remote Explorer' en Antigravity / VS Code" -ForegroundColor Green
Write-Host "y conectarte directamente por SSH a tu VM de Codespaces sin consumir RAM en la laptop.`n" -ForegroundColor Green
