# BACKUP_REMOTE_STATE.ps1
# Guarda el estado de la sesión, pestañas y contexto de la VM cloud antes del apagado automático

$CODESPACE_NAME = "glowing-couscous-q7pwv9xxq647c65x4"
$BACKUP_DIR = "c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto\outputs\cloud_state_backups"

if (!(Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$target_file = "$BACKUP_DIR\state_$timestamp.tar.gz"

Write-Host "Creando copia de seguridad del estado de la VM cloud..." -ForegroundColor Cyan

# Extraer estado del navegador, cookies y logs de ejecución
gh codespace ssh -c $CODESPACE_NAME -- "tar -czf - ~/.config/chromium /tmp/*.log 2>/dev/null" > $target_file

Write-Host "Estado remoto empaquetado en: $target_file" -ForegroundColor Green
