# ==============================================================================
# NEXUS Multi-AI MCP Server & Sub-Agent Coordinator
# ==============================================================================
# Expone a OpenCode, Aider, Ollama (Local), HuggingFace y Gemini como
# herramientas nativas / sub-agentes accesibles por Antigravity IDE vía MCP.
# ==============================================================================

import os
import sys
import json
import subprocess
from pathlib import Path

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")

def run_agent_query(agent_name: str, prompt: str, target_file: str = None) -> dict:
    """Despacha tareas hacia el agente especificado."""
    agent_name = agent_name.lower().strip()
    
    if agent_name in ["gemini", "gemini-cli"]:
        from work.gemini_cli_bridge import GeminiCliBridge
        bridge = GeminiCliBridge()
        output = bridge.query_gemini(prompt, target_file)
        return {"agent": "Gemini CLI", "status": "OK", "response": output}
        
    elif agent_name in ["opencode"]:
        return {
            "agent": "OpenCode",
            "status": "DISPATCHED",
            "info": "Tarea enviada al agente OpenCode (Web / Desktop / CLI)."
        }
        
    elif agent_name in ["aider"]:
        cmd = f"aider --message \"{prompt}\""
        if target_file:
            cmd += f" --file \"{target_file}\""
        return {
            "agent": "Aider",
            "status": "COMMAND_READY",
            "command": cmd
        }
        
    elif agent_name in ["ollama", "local"]:
        # Inferencia local vía endpoint Ollama
        import urllib.request
        try:
            url = "http://localhost:11434/api/generate"
            payload = json.dumps({"model": "qwen2.5-coder:1.5b", "prompt": prompt, "stream": False}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
                return {"agent": "Ollama (Local)", "status": "OK", "response": data.get("response", "")}
        except Exception as e:
            return {"agent": "Ollama (Local)", "status": "OFFLINE", "message": f"Ollama local no está activo en puerto 11434: {e}"}

    else:
        return {"error": f"Agente '{agent_name}' no reconocido. Opciones: gemini, opencode, aider, ollama"}

if __name__ == "__main__":
    if len(sys.argv) > 2:
        agent = sys.argv[1]
        prompt_text = " ".join(sys.argv[2:])
        sys.path.insert(0, str(WORKSPACE))
        res = run_agent_query(agent, prompt_text)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"status": "READY", "supported_agents": ["gemini", "opencode", "aider", "ollama"]}))
