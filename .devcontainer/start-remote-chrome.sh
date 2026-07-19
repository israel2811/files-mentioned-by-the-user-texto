#!/bin/bash
# start-remote-chrome.sh
# Arranca Chromium headless en el Codespace escuchando en el puerto 9222
# Esto permite que Antigravity controle el navegador remoto desde la PC local via port forward

echo "Instalando Chromium si no está disponible..."
which chromium-browser || which chromium || (sudo apt-get install -y chromium-browser chromium)

CHROME_BIN=$(which chromium-browser 2>/dev/null || which chromium 2>/dev/null || echo "chromium")

echo "Arrancando Chrome Headless en puerto 9222..."
$CHROME_BIN \
    --headless \
    --no-sandbox \
    --disable-gpu \
    --remote-debugging-port=9222 \
    --remote-debugging-address=0.0.0.0 \
    --disable-dev-shm-usage \
    --user-data-dir=/tmp/remote-chrome-profile &

echo "Chrome arrancado con PID: $!"
echo "Para conectar desde tu PC local, ejecuta en PowerShell:"
echo "  gh codespace ports forward 9222:9222 -c glowing-couscous-q7pwv9xxq647c65x4"
echo "Luego apunta Antigravity/Claude al puerto 9222 de tu localhost."
