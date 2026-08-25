@echo off
title NEXUS - AI CODING AGENTS LAUNCHER
color 0b
echo ================================================================
echo        NEXUS / LANZADOR DE AGENTES DE CODIGO EN VIVO
echo ================================================================
echo.
echo Ajustando prioridad de procesos y abriendo sesiones de trabajo...
echo.

:: 1. Lanzar OpenCode
where opencode >nul 2>nul
if %errorlevel% equ 0 (
    echo [+] Lanzando OpenCode Terminal...
    start "NEXUS - OpenCode Agent" powershell -NoExit -Command "Write-Host '=== OPENCODE AGENT (MULTI-MODEL) ===' -ForegroundColor Cyan; opencode"
) else (
    echo [-] OpenCode no detectado en PATH. Abriendo sitio web...
    start https://opencode.ai
)

:: 2. Lanzar Aider
where aider >nul 2>nul
if %errorlevel% equ 0 (
    echo [+] Lanzando Aider...
    start "NEXUS - Aider Agent" powershell -NoExit -Command "Write-Host '=== AIDER AGENT (GIT CODING) ===' -ForegroundColor Yellow; aider"
) else (
    echo [-] Aider no detectado en PATH.
)

:: 3. Abrir Portales Web Activos
start https://opencode.ai
start https://openhands.dev
start https://aider.chat

echo.
echo ================================================================
echo  Ventanas de trabajo y portales abiertos exitosamente.
echo ================================================================
pause
