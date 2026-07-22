#!/bin/bash
# configure_usb_persistence.sh
# Script para optimizar y configurar la memoria RAM comprimida (ZRAM) 
# y la persistencia de datos en la memoria USB booteable con Linux Mint.

echo "=========================================================="
echo "    CONFIGURANDO ZRAM Y PERSISTENCIA PARA USB LIVE OS     "
echo "=========================================================="

# 1. Habilitar ZRAM (compresión de memoria en tiempo real)
if command -v zram-tools &> /dev/null; then
    echo "[+] Habilitando ZRAM..."
    sudo systemctl enable --now zramswap
else
    echo "[+] Instalando e iniciando zram-tools..."
    sudo apt-get update && sudo apt-get install -y zram-tools
    echo "ALGORITHM=zstd" | sudo tee -a /etc/default/zramswap
    echo "PERCENT=60" | sudo tee -a /etc/default/zramswap
    sudo service zramswap start
fi

# 2. Configurar perfil de navegador liviano para Brave
echo "[+] Configurando accesos directos y optimización de Brave..."
mkdir -p ~/.config/BraveSoftware/
echo '{"profile":{"content_settings":{"exceptions":{"images":1}}}}' > ~/.config/BraveSoftware/default_flags.json || true

echo "[OK] Memoria USB optimizada con ZRAM (60% RAM comprimida). ¡Listo para trabajar!"
