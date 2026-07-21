# START_REMOTE_BROWSER.ps1
# Script para iniciar y conectar el navegador remoto persistente en Codespaces

$CODESPACE_NAME = "glowing-couscous-q7pwv9xxq647c65x4"

Write-Host "1. Verificando estado del Codespace $CODESPACE_NAME..." -ForegroundColor Cyan
$status = gh codespace list | Where-Object { $_ -match $CODESPACE_NAME }

if ($status -match "Shutdown") {
    Write-Host "El Codespace está apagado. Despertándolo..." -ForegroundColor Yellow
    # Intentar conexión SSH rápida para forzar el arranque
    gh codespace ssh -c $CODESPACE_NAME -- "echo 'Despertando VM...'" | Out-Null
    Start-Sleep -Seconds 5
}

Write-Host "Codespace disponible. Iniciando túneles de puertos..." -ForegroundColor Green
Write-Host "Redireccionando puerto 6080 (Visual NoVNC) y puerto 9222 (Control CDP)..." -ForegroundColor Cyan

# Lanzar el port forward en segundo plano
Start-Process powershell -ArgumentList "-NoProfile -Command `& { gh codespace ports forward 6080:6080 -c $CODESPACE_NAME }`" -WindowStyle Minimized
Start-Process powershell -ArgumentList "-NoProfile -Command `& { gh codespace ports forward 9222:9222 -c $CODESPACE_NAME }`" -WindowStyle Minimized

Start-Sleep -Seconds 3

# Verificar si los servicios gráficos están corriendo en el Codespace; si no, iniciarlos.
Write-Host "Iniciando Xvfb y NoVNC en la VM..." -ForegroundColor Cyan
gh codespace ssh -c $CODESPACE_NAME -- "
    if ! pgrep -x 'Xvfb' > /dev/null; then
        echo 'Iniciando servidor gráfico virtual...';
        Xvfb :1 -screen 0 1280x800x24 &
        sleep 1;
        DISPLAY=:1 fluxbox &
        DISPLAY=:1 x11vnc -forever -shared -nopw -display :1 &
        websockify --web /usr/share/novnc 6080 localhost:5900 &
    else
        echo 'El servidor gráfico ya está corriendo.';
    fi
"

Write-Host "Abriendo la interfaz visual en tu Brave local..." -ForegroundColor Green
Start-Process "brave" "http://localhost:6080/vnc.html"

Write-Host "Listo. Puedes cerrar esta consola. La sesión remota persistirá de fondo." -ForegroundColor Green
