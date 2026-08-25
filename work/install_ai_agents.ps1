# ==============================================================================
# NEXUS AI Coding Agents - Suite de Instalación y Lanzamiento Modular (Windows)
# ==============================================================================
# Este script permite instalar y lanzar selectivamente los agentes de código
# recomendados para tu entorno de desarrollo en Windows.
# ==============================================================================

param(
    [Parameter(Position=0)]
    [ValidateSet('menu', 'opencode', 'aider', 'cline', 'kilocode', 'goose', 'qwen', 'ollama', 'all_light')]
    [string]$Action = 'menu'
)

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     NEXUS / AI Coding Agents Setup & Launcher (Windows)        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

function Test-CommandExists ($cmd) {
    return [bool](Get-Command $cmd -ErrorAction SilentlyContinue)
}

function Install-OpenCode {
    Write-Host "`n[1/7] Instalando / Actualizando OpenCode (CLI)..." -ForegroundColor Yellow
    try {
        # Intento de instalador oficial de OpenCode para Windows
        Write-Host "Descargando e instalando OpenCode vía instalador oficial..." -ForegroundColor Gray
        Invoke-Expression "& { $(Invoke-RestMethod https://opencode.ai/install.ps1) }"
        Write-Host "✓ OpenCode instalado exitosamente." -ForegroundColor Green
    } catch {
        Write-Host "Reintentando instalación vía npm..." -ForegroundColor Yellow
        npm install -g opencode-ai
    }
}

function Install-Aider {
    Write-Host "`n[2/7] Instalando / Actualizando Aider (Git-Centric Coding Agent)..." -ForegroundColor Yellow
    python -m pip install --upgrade aider-chat
    if (Test-CommandExists "aider") {
        Write-Host "✓ Aider instalado correctamente. Ejecuta 'aider' en tu terminal." -ForegroundColor Green
    }
}

function Install-KiloCode {
    Write-Host "`n[3/7] Instalando Kilo Code CLI..." -ForegroundColor Yellow
    npm install -g @kilocode/cli
    Write-Host "✓ Kilo Code CLI instalado." -ForegroundColor Green
}

function Install-ClineVSCode {
    Write-Host "`n[4/7] Instalando extensión Cline en Visual Studio Code..." -ForegroundColor Yellow
    if (Test-CommandExists "code") {
        code --install-extension saoudrizwan.claude-dev
        Write-Host "✓ Extensión Cline instalada en VS Code." -ForegroundColor Green
    } else {
        Write-Host "VS Code ('code') no detectado en el PATH. Instala la extensión buscando 'Cline' en la pestaña Extensiones de VS Code." -ForegroundColor Yellow
    }
}

function Install-QwenCode {
    Write-Host "`n[5/7] Instalando Qwen Code CLI..." -ForegroundColor Yellow
    try {
        npm install -g @qwen-code/cli
        Write-Host "✓ Qwen Code instalado." -ForegroundColor Green
    } catch {
        Write-Host "Nota: Si falla el paquete npm de Qwen Code, consulta el repositorio oficial https://github.com/QwenLM/qwen-code" -ForegroundColor Yellow
    }
}

function Install-Goose {
    Write-Host "`n[6/7] Instalando Goose (Block AI Developer Agent)..." -ForegroundColor Yellow
    Write-Host "Para Windows, el instalador oficial de Goose se obtiene mediante:" -ForegroundColor Gray
    Write-Host "Descarga: https://github.com/block/goose/releases" -ForegroundColor Cyan
    try {
        # Descarga o instalación alternativa si scoop o winget están disponibles
        winget install Block.Goose --silent --accept-package-agreements --accept-source-agreements
    } catch {
        Write-Host "Abriendo página de releases de Goose en el navegador..." -ForegroundColor Gray
        Start-Process "https://github.com/block/goose/releases"
    }
}

function Install-Ollama {
    Write-Host "`n[7/7] Instalando Ollama (Para modelos locales ligeros)..." -ForegroundColor Yellow
    try {
        winget install Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements
        Write-Host "✓ Ollama instalado. Modelos recomendados para tu hardware: qwen2.5-coder:1.5b o deepseek-r1:1.5b" -ForegroundColor Green
    } catch {
        Write-Host "Abriendo instalador oficial de Ollama..." -ForegroundColor Gray
        Start-Process "https://ollama.com/download/OllamaSetup.exe"
    }
}

switch ($Action) {
    'opencode'    { Install-OpenCode }
    'aider'       { Install-Aider }
    'kilocode'    { Install-KiloCode }
    'cline'       { Install-ClineVSCode }
    'qwen'        { Install-QwenCode }
    'goose'       { Install-Goose }
    'ollama'      { Install-Ollama }
    'all_light'   {
        Install-OpenCode
        Install-Aider
        Install-KiloCode
        Install-ClineVSCode
    }
    'menu' {
        Write-Host "`nSelecciona qué IA / Agente deseas instalar en tu equipo:" -ForegroundColor White
        Write-Host "  1. OpenCode (Recomendado #1: Terminal + Desktop + Modelos Gratuitos / BYOK)" -ForegroundColor Green
        Write-Host "  2. Aider (Recomendado #2: Control preciso de Git + Multi-archivo)" -ForegroundColor Green
        Write-Host "  3. Kilo Code (CLI rápido y ligero con npm)" -ForegroundColor Yellow
        Write-Host "  4. Cline (Extensión visual para Visual Studio Code)" -ForegroundColor Yellow
        Write-Host "  5. Qwen Code (Agent Teams y Sub-agentes)" -ForegroundColor Yellow
        Write-Host "  6. Goose (Agente extensible de Block)" -ForegroundColor Yellow
        Write-Host "  7. Ollama (Motor para ejecutar modelos de 1.5B/3B/7B 100% offline)" -ForegroundColor Magenta
        Write-Host "  8. Instalar Pack Ligero (OpenCode + Aider + Kilo + Cline)" -ForegroundColor Cyan
        Write-Host "  0. Salir" -ForegroundColor Gray
        
        $opt = Read-Host "`nIngresa una opción [1-8 o 0]"
        switch ($opt) {
            '1' { Install-OpenCode }
            '2' { Install-Aider }
            '3' { Install-KiloCode }
            '4' { Install-ClineVSCode }
            '5' { Install-QwenCode }
            '6' { Install-Goose }
            '7' { Install-Ollama }
            '8' { 
                Install-OpenCode
                Install-Aider
                Install-KiloCode
                Install-ClineVSCode
            }
            default { Write-Host "Operación finalizada." -ForegroundColor Gray }
        }
    }
}
