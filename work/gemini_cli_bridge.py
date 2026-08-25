# ==============================================================================
# NEXUS Gemini CLI & Multi-Agent Bridge for Antigravity
# ==============================================================================
# Permite interactuar con Gemini CLI y usarlo como agente paralelo de revisión
# y auditoría directamente desde Antigravity IDE / terminal.
# ==============================================================================

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
OUTPUT_DIR = WORKSPACE / "outputs"
GEMINI_LOG_FILE = OUTPUT_DIR / "gemini_cli_interactions.json"

class GeminiCliBridge:
    def __init__(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def is_gemini_cli_installed(self) -> bool:
        """Verifica si gemini-cli está en el PATH del sistema."""
        try:
            res = subprocess.run(["where", "gemini"], capture_output=True, text=True)
            return res.returncode == 0
        except Exception:
            return False

    def query_gemini(self, prompt: str, context_file: str = None) -> str:
        """Envía una consulta o archivo a Gemini CLI y obtiene la respuesta."""
        print(f"[*] Enviando consulta a Gemini CLI: '{prompt[:60]}...'")
        
        full_prompt = prompt
        if context_file and Path(context_file).exists():
            content = Path(context_file).read_text(encoding="utf-8", errors="ignore")
            full_prompt = f"Contexto de {context_file}:\n```\n{content[:4000]}\n```\n\nInstrucción:\n{prompt}"

        # Registrar interacción
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "context_file": context_file,
            "status": "QUEUED"
        }
        
        try:
            # Intento de invocación estándar si gemini CLI está configurado
            res = subprocess.run(["gemini", full_prompt], capture_output=True, text=True, timeout=30)
            output = res.stdout if res.returncode == 0 else res.stderr
            interaction["status"] = "SUCCESS" if res.returncode == 0 else "ERROR"
            interaction["response"] = output
            print(f"[OK] Respuesta recibida de Gemini CLI.")
        except Exception as e:
            output = f"[INFO] Para usar Gemini CLI directamente: ejecuta 'gemini' en tu terminal o configura tu GEMINI_API_KEY.\nDetalle: {e}"
            interaction["status"] = "STANDBY"
            interaction["response"] = output

        # Guardar en log persistente
        history = []
        if GEMINI_LOG_FILE.exists():
            try:
                history = json.loads(GEMINI_LOG_FILE.read_text(encoding="utf-8"))
            except Exception:
                history = []
        history.append(interaction)
        GEMINI_LOG_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
        return output

if __name__ == "__main__":
    bridge = GeminiCliBridge()
    installed = bridge.is_gemini_cli_installed()
    print(f"[Gemini Bridge] Gemini CLI detectado en sistema: {installed}")
    res = bridge.query_gemini("Revisa el estado de la arquitectura NEXUS y valida los agentes.")
    print(res)
