@echo off
echo ==========================================================
echo    INICIANDO CODEX, CODEX BETA Y NAVEGADORES MULTICUENTA
echo ==========================================================
echo.

echo 1. Buscando e iniciando Codex / Codex Beta...
where codex >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start codex
    echo [OK] Codex lanzado desde PATH.
) else (
    if exist "C:\Users\Dell\AppData\Local\OpenAI\Codex\bin\5dee10576ec7a5b8\codex.exe" (
        start "" "C:\Users\Dell\AppData\Local\OpenAI\Codex\bin\5dee10576ec7a5b8\codex.exe"
        echo [OK] Codex Beta lanzado desde AppData.
    ) else (
        echo [INFO] Ejecutando búsqueda general de Codex...
        start codex
    )
)

echo 2. Abriendo Google Drive en Chrome (Perfil Default)...
start chrome --profile-directory="Default" "https://drive.google.com"

echo 3. Abriendo ChatGPT en Chrome (Perfil 2)...
start chrome --profile-directory="Profile 2" "https://chatgpt.com"

echo 4. Abriendo Claude AI en Brave (Perfil Default)...
start brave --profile-directory="Default" "https://claude.ai"

echo 5. Abriendo NotebookLM en Microsoft Edge (Perfil Default)...
start msedge --profile-directory="Default" "https://notebooklm.google.com"

echo.
echo ==========================================================
echo  ¡CODEX, CODEX BETA Y PERFILES DE NAVEGADOR DESPLEGADOS!
echo ==========================================================
