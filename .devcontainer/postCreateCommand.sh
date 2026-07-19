#!/bin/bash
echo "Inicializando el Codespace de NEXUS..."

# Actualizar e instalar dependencias básicas del sistema
sudo apt-get update && sudo apt-get install -y \
    curl \
    git \
    build-essential \
    apt-transport-https \
    ca-certificates \
    gnupg

# Instalar gcloud CLI
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install -y google-cloud-cli

# Instalar los MCP Servers globalmente
echo "Instalando servidores MCP..."
npm install -g @modelcontextprotocol/server-filesystem \
               @modelcontextprotocol/server-memory \
               @modelcontextprotocol/server-sequential-thinking \
               @modelcontextprotocol/server-fetch \
               @modelcontextprotocol/server-puppeteer \
               chrome-devtools-mcp

# Configurar entorno Python
if [ -f "requirements.txt" ]; then
    echo "Instalando paquetes de Python..."
    pip install -r requirements.txt
fi

echo "Codespace configurado y listo."
