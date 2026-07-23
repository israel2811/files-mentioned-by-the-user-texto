import os
import sys
import subprocess
import glob
from pathlib import Path

def find_codex_executables():
    """Finds all available Codex / Codex Beta executables on the system."""
    user_profile = os.environ.get("USERPROFILE", r"C:\Users\Dell")
    search_patterns = [
        os.path.join(user_profile, r"AppData\Local\OpenAI\Codex\**\codex.exe"),
        os.path.join(user_profile, r"AppData\Local\Programs\**\codex.exe"),
        os.path.join(user_profile, r"AppData\Local\Programs\**\Codex*.exe"),
        os.path.join(user_profile, r"AppData\Local\OpenAI\**\*.exe")
    ]
    found = []
    for pattern in search_patterns:
        for p in glob.glob(pattern, recursive=True):
            if os.path.isfile(p) and p not in found:
                found.append(p)
    return found

def main():
    print("==================================================")
    print("      INICIANDO SUITE DE NAVEGADORES Y CODEX      ")
    print("==================================================")

    # 1. Encontrar e iniciar Codex / Codex Beta
    codex_paths = find_codex_executables()
    if codex_paths:
        for exe in codex_paths:
            print(f"[+] Iniciando ejecutable Codex: {exe}")
            try:
                os.startfile(exe)
            except Exception as e:
                print(f"[!] Error al iniciar {exe}: {e}")
    else:
        print("[!] No se encontró ejecutable directo de Codex en rutas predefinidas. Intentando comando de sistema 'codex'...")
        try:
            subprocess.Popen(["cmd.exe", "/c", "start", "codex"], shell=True)
        except Exception as e:
            print(f"[!] Error al iniciar codex vía cmd: {e}")

    # 2. Abrir Navegadores con Perfiles Diferentes vía os.startfile / cmd start
    browsers = [
        ("Chrome Default (Google Drive)", 'start chrome --profile-directory="Default" "https://drive.google.com"'),
        ("Chrome Profile 2 (ChatGPT)", 'start chrome --profile-directory="Profile 2" "https://chatgpt.com"'),
        ("Brave Default (Claude AI)", 'start brave --profile-directory="Default" "https://claude.ai"'),
        ("Edge Default (NotebookLM)", 'start msedge --profile-directory="Default" "https://notebooklm.google.com"')
    ]

    for name, cmd in browsers:
        print(f"[+] Abriendo {name}...")
        try:
            subprocess.Popen(["cmd.exe", "/c", cmd], shell=True)
        except Exception as e:
            print(f"[!] Error abriendo {name}: {e}")

    # 3. Inicializar base de datos DuckDB de la tesis
    try:
        from nexus_duckdb_corpus import init_duckdb_corpus
        init_duckdb_corpus()
    except Exception as e:
        print(f"[!] Error ejecutando DuckDB corpus: {e}")

    print("==================================================")
    print("  ¡TODOS LOS PROCESOS (CODEX + NAVEGADORES) INICIADOS!")
    print("==================================================")

if __name__ == "__main__":
    main()
