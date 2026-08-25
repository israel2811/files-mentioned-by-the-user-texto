# ==============================================================================
# NEXUS NATIVE WINDOWS LAUNCHER (PowerShell Native)
# ==============================================================================
$workspace = "C:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto"

# 1. OpenCode Window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$workspace'; Write-Host '=== OPENCODE MULTI-MODEL AGENT ===' -ForegroundColor Cyan; if (Get-Command opencode -ErrorAction SilentlyContinue) { opencode } else { Write-Host 'OpenCode listo.' -ForegroundColor Yellow }"

# 2. Aider Window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$workspace'; Write-Host '=== AIDER GIT REPO AGENT ===' -ForegroundColor Yellow; if (Get-Command aider -ErrorAction SilentlyContinue) { aider } else { Write-Host 'Aider listo.' }"

# 3. Gemini CLI Bridge Window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$workspace'; Write-Host '=== GEMINI CLI / MULTI-AGENT BRIDGE ===' -ForegroundColor Green; python work\gemini_cli_bridge.py"

# 4. Portales Web Oficiales
Start-Process "https://opencode.ai"
Start-Process "https://openhands.dev"
Start-Process "https://aider.chat"
