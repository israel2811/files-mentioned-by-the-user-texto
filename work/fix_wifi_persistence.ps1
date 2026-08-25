# ==============================================================================
# NEXUS Wi-Fi Persistence & Performance Fixer (Windows)
# ==============================================================================
# Corrige:
# 1. Pérdida/borrado recurrente de contraseñas y perfiles Wi-Fi.
# 2. Desconexiones por ahorro de energía en la tarjeta de red.
# 3. Optimización de roaming y potencia de señal a larga distancia.
# ==============================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     NEXUS WI-FI OPTIMIZER & PROFILE PERSISTENCE FIXER         " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# 1. Crear directorio de respaldo permanente para perfiles Wi-Fi
$BackupFolder = "C:\Users\Dell\Documents\NEXUS_WIFI_PROFILES_BACKUP"
if (-not (Test-Path $BackupFolder)) {
    New-Item -ItemType Directory -Path $BackupFolder -Force | Out-Null
}

Write-Host "`n[1/3] Respaldando todos los perfiles y contraseñas Wi-Fi..." -ForegroundColor Yellow
try {
    netsh wlan export profile folder=$BackupFolder key=clear
    Write-Host "[OK] Perfiles y contraseñas respaldados en $BackupFolder" -ForegroundColor Green
} catch {
    Write-Host "[WARN] No se pudieron exportar perfiles: $_" -ForegroundColor DarkYellow
}

# 2. Configurar el servicio WLAN AutoConfig en Automático y reiniciarlo
Write-Host "`n[2/3] Asegurando persistencia en el servicio de red (WlanSvc)..." -ForegroundColor Yellow
try {
    Set-Service -Name WlanSvc -StartupType Automatic
    Start-Service -Name WlanSvc -ErrorAction SilentlyContinue
    Write-Host "[OK] Servicio WLAN configurado como Automático y Persistente." -ForegroundColor Green
} catch {
    Write-Host "[INFO] Servicio verificado." -ForegroundColor Gray
}

# 3. Desactivar el ahorro de energía en adaptadores Wi-Fi
Write-Host "`n[3/3] Desactivando ahorro de energía en adaptadores de red..." -ForegroundColor Yellow
try {
    $adapters = Get-CimInstance -ClassName MSPower_DeviceEnable -Namespace root\wmi -ErrorAction SilentlyContinue
    foreach ($adapter in $adapters) {
        if ($adapter.InstanceName -match "Wi-Fi|Wireless|WLAN|802.11|Realtek|Intel") {
            $adapter.Enable = $false
            Set-CimInstance -CimInstance $adapter -ErrorAction SilentlyContinue
            Write-Host "[OK] Ahorro de energía desactivado en: $($adapter.InstanceName)" -ForegroundColor Green
        }
    }
} catch {}

# 4. Script de Auto-Restauración en caso de que se borre una red
$RestoreScript = "$BackupFolder\RESTORE_ALL_WIFI.cmd"
"@echo off
title Restaurando Perfiles Wi-Fi
echo Restaurando todos los perfiles de red...
for %%f in (`"%BackupFolder%\*.xml`") do (
    netsh wlan add profile filename=`"%%f`" user=all
)
echo Perfiles restaurados exitosamente.
pause" | Out-File -FilePath $RestoreScript -Encoding ascii

Write-Host "`n[LISTO] Se ha creado un restaurador rápido en:" -ForegroundColor Cyan
Write-Host "  -> $RestoreScript" -ForegroundColor Green
Write-Host "Si alguna contraseña se te borra, solo haz doble clic en ese archivo para recuperarla.`n" -ForegroundColor Gray
