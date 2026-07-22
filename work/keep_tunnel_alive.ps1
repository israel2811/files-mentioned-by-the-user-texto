# keep_tunnel_alive.ps1
# Mantiene los puertos de Codespaces (6080 noVNC y 9222 CDP) siempre redirigidos a localhost.

$CODESPACE_NAME = "glowing-space-bassoon-x5qqqp5qgvq4h4jr"

Write-Host "Iniciando servicio de túnel persistente para Codespaces: $CODESPACE_NAME..." -ForegroundColor Cyan

while ($true) {
    # Verificar si los puertos están escuchando localmente; si no, reconectar
    $port6080 = Get-NetTCPConnection -LocalPort 6080 -ErrorAction SilentlyContinue
    if (-not $port6080) {
        Write-Host "[+] Reenviando puerto 6080 (noVNC Remote Screen)..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoProfile -Command `& { gh codespace ports forward 6080:6080 -c $CODESPACE_NAME }`" -WindowStyle Minimized
    }
    
    $port9222 = Get-NetTCPConnection -LocalPort 9222 -ErrorAction SilentlyContinue
    if (-not $port9222) {
        Write-Host "[+] Reenviando puerto 9222 (Control CDP)..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoProfile -Command `& { gh codespace ports forward 9222:9222 -c $CODESPACE_NAME }`" -WindowStyle Minimized
    }
    
    Start-Sleep -Seconds 30
}
