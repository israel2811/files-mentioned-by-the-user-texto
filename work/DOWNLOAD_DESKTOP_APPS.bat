@echo off
title NEXUS - INSTALADOR Y LANZADOR DE VERSIONES DE ESCRITORIO
color 0a
echo ==============================================================================
echo     NEXUS / DESCARGA E INSTALACION DE VERSIONES DE ESCRITORIO (WINDOWS)
echo ==============================================================================
echo.
echo Abriendo los instaladores y ejecutables oficiales de escritorio...
echo.

:: 1. OpenCode Desktop para Windows (Instalador .exe / Releases)
echo [1/4] Abriendo instalador de OpenCode Desktop para Windows...
start https://github.com/anomalyco/opencode/releases

:: 2. Qwen Code Desktop / Releases oficiales
echo [2/4] Abriendo instalador de Qwen Code Desktop...
start https://github.com/QwenLM/qwen-code/releases

:: 3. Goose Desktop para Windows (Block)
echo [3/4] Abriendo instalador de Goose Desktop (Block)...
start https://github.com/block/goose/releases

:: 4. Ollama Windows GUI / Setup
echo [4/4] Abriendo instalador de Ollama para Windows...
start https://ollama.com/download/OllamaSetup.exe

echo.
echo ==============================================================================
echo  Paginas de descarga e instaladores abiertos en el navegador.
echo ==============================================================================
pause
