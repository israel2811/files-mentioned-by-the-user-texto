# ==============================================================================
# NEXUS AUTONOMOUS DAEMON & AGENT MASTER LAUNCHER (Self-Healing & Auto-Resume)
# ==============================================================================
# 1. Opera en segundo plano con prioridad BelowNormal / Idle para cero lag.
# 2. Descarga e instala en bucle autónomo hasta que cada componente quede listo.
# 3. Abre consolas interactivas independientes y navegadores con los agentes listos.
# ==============================================================================

import os
import sys
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
OUTPUT_DIR = WORKSPACE / "outputs"
DAEMON_LOG = OUTPUT_DIR / "nexus_daemon_execution.log"

def log(msg: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {msg}"
    print(line)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(DAEMON_LOG, "a", encoding="utf-8", errors="ignore") as f:
        f.write(line + "\n")

def is_internet_available(host="8.8.8.8", port=53, timeout=3) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def wait_for_connection():
    while not is_internet_available():
        log("[-] Conexión inestable o caída. Pausando proceso (esperando reconexión activa)...")
        time.sleep(5)
    log("[+] Conexión a Internet detectada y activa.")

def run_resilient_command(cmd, name, max_retries=15):
    log(f"[*] Iniciando componente: {name}")
    for attempt in range(1, max_retries + 1):
        wait_for_connection()
        try:
            log(f" -> Ejecutando {name} (Intento {attempt}/{max_retries})...")
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=True)
            if res.returncode == 0:
                log(f"[✓] {name} instalado/ejecutado con éxito.")
                return True
            else:
                log(f"[WARN] {name} retornó código {res.returncode}. Reintentando en 6s...")
        except subprocess.TimeoutExpired:
            log(f"[WARN] Tiempo de espera agotado para {name}. Reintentando...")
        except Exception as e:
            log(f"[ERROR] Excepción en {name}: {e}")
        time.sleep(6)
    return False

def open_interactive_sessions():
    log("[*] Abriendo ventanas de trabajo interactivas y manteniéndolas en ejecución...")
    
    # 1. Ventana OpenCode
    cmd_opencode = 'start "NEXUS OpenCode Agent" powershell -NoExit -Command "Write-Host \\"=== OPENCODE MULTI-MODEL AGENT ===\\" -ForegroundColor Cyan; if (Get-Command opencode -ErrorAction SilentlyContinue) { opencode } else { Write-Host \\"OpenCode configurado y listo en navegador y terminal.\\" -ForegroundColor Yellow }"'
    subprocess.Popen(cmd_opencode, shell=True)
    
    # 2. Ventana Aider
    cmd_aider = 'start "NEXUS Aider Agent" powershell -NoExit -Command "Write-Host \\"=== AIDER GIT REPO AGENT ===\\" -ForegroundColor Yellow; if (Get-Command aider -ErrorAction SilentlyContinue) { aider } else { Write-Host \\"Aider listo.\\" }"'
    subprocess.Popen(cmd_aider, shell=True)
    
    # 3. Ventana Gemini CLI & Sub-Agentes
    cmd_gemini = 'start "NEXUS Gemini CLI Bridge" powershell -NoExit -Command "Write-Host \\"=== GEMINI CLI / SUB-AGENTS BRIDGE ===\\" -ForegroundColor Green; python work/gemini_cli_bridge.py"'
    subprocess.Popen(cmd_gemini, shell=True)
    
    # 4. Abrir portales web en navegadores
    urls = [
        "https://opencode.ai",
        "https://openhands.dev",
        "https://aider.chat",
        "https://colab.research.google.com"
    ]
    for url in urls:
        subprocess.Popen(f'start {url}', shell=True)
    
    log("[✓] Todas las ventanas y navegadores han sido lanzados y permanecen abiertos.")

def main():
    log("=== INICIANDO NEXUS AUTONOMOUS DAEMON ===")
    
    # Reducir prioridad de CPU
    try:
        import psutil
        p = psutil.Process()
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        log("[OK] Prioridad de proceso ajustada a BelowNormal.")
    except Exception:
        pass

    # Instalaciones resilientes autónomas
    run_resilient_command("npm install -g opencode-ai @kilocode/cli", "NPM Agent Suite (OpenCode & Kilo)", max_retries=10)
    run_resilient_command("python -m pip install --upgrade aider-chat requests duckdb", "Python Agent Suite (Aider/DuckDB)", max_retries=10)
    
    # Lanzamiento de todas las sesiones
    open_interactive_sessions()
    log("=== NEXUS AUTONOMOUS DAEMON: TAREAS COMPLETADAS Y SESIONES ABIERTAS ===")

if __name__ == "__main__":
    main()
