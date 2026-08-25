# ==============================================================================
# NEXUS Resilient AI Agent Installer & Auto-Launcher (Anti-Lag & Auto-Retry)
# ==============================================================================
# Diseñado para conexiones inestables y hardware con recursos limitados.
# Incluye:
# 1. Prioridad de CPU moderada (BelowNormal) para no congelar la PC.
# 2. Reintentos automáticos continuos con espera activa hasta que vuelva internet.
# 3. Instalación y apertura automática de OpenCode, Aider, Cline y herramientas.
# ==============================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " NEXUS RESILIENT AI AGENT INSTALLER & LAUNCHER (AUTO-RETRY)    " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Reducir prioridad del proceso actual para no saturar la máquina
try {
    [System.Diagnostics.Process]::GetCurrentProcess().PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
    Write-Host "[+] Prioridad de CPU ajustada a 'BelowNormal' para fluidez del sistema." -ForegroundColor Green
} catch {}

function Wait-ForInternet {
    param([int]$MaxAttempts = 120, [int]$DelaySeconds = 5)
    Write-Host "[*] Comprobando conexión a Internet..." -ForegroundColor Yellow
    $attempt = 1
    while ($attempt -le $MaxAttempts) {
        try {
            $test = Test-Connection -ComputerName "8.8.8.8" -Count 1 -Quiet -ErrorAction SilentlyContinue
            if ($test) {
                Write-Host "[✓] Conexión a Internet activa y verificada." -ForegroundColor Green
                return $true
            }
        } catch {}
        Write-Host "[-] Sin conexión o reconectando... reintentando en $DelaySeconds seg (Intento $attempt/$MaxAttempts)" -ForegroundColor DarkYellow
        Start-Sleep -Seconds $DelaySeconds
        $attempt++
    }
    return $false
}

function Install-WithRetry {
    param(
        [string]$Name,
        [scriptblock]$ActionScript,
        [int]$MaxRetries = 10
    )
    Write-Host "`n>>> [PROCESANDO]: $Name" -ForegroundColor Cyan
    $success = $false
    $retry = 1
    while (-not $success -and $retry -le $MaxRetries) {
        Wait-ForInternet
        try {
            Write-Host "Ejecutando instalación de $Name (Intento $retry)..." -ForegroundColor Gray
            & $ActionScript
            $success = $true
            Write-Host "[✓] Éxito instalando $Name." -ForegroundColor Green
        } catch {
            Write-Host "[!] Error temporal o interrupción de red al instalar $Name. Reintentando en 6s..." -ForegroundColor Red
            Start-Sleep -Seconds 6
            $retry++
        }
    }
}

# 1. OpenCode (Instalador oficial)
Install-WithRetry -Name "OpenCode CLI / Desktop" -ActionScript {
    Invoke-Expression "& { $(Invoke-RestMethod https://opencode.ai/install.ps1 -TimeoutSec 30) }"
}

# 2. Aider (Python Package)
Install-WithRetry -Name "Aider (Git Multi-File Agent)" -ActionScript {
    python -m pip install --upgrade --timeout 60 --retries 10 aider-chat
}

# 3. Kilo Code CLI
Install-WithRetry -Name "Kilo Code CLI" -ActionScript {
    npm install -g @kilocode/cli --fetch-retries=5 --fetch-retry-mintimeout=20000
}

# 4. Cline para VS Code
Install-WithRetry -Name "Cline Extension (VS Code)" -ActionScript {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        code --install-extension saoudrizwan.claude-dev
    }
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   LANZANDO AGENTES Y PANELES EN EJECUCIÓN (LISTOS PARA USAR)  " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Lanzar OpenCode si está disponible
if (Get-Command opencode -ErrorAction SilentlyContinue) {
    Write-Host "[+] Abriendo ventana de terminal para OpenCode..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '=== OPENCODE AGENT SESSION ===' -ForegroundColor Cyan; opencode"
}

# Lanzar Aider si está disponible
if (Get-Command aider -ErrorAction SilentlyContinue) {
    Write-Host "[+] Abriendo ventana de terminal para Aider..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '=== AIDER AGENT SESSION ===' -ForegroundColor Yellow; aider"
}

Write-Host "`n[✓] Todos los agentes han sido configurados y están listos." -ForegroundColor Green
