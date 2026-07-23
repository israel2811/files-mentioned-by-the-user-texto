import subprocess
import os
import sys

def launch_browsers():
    """
    Launches Chrome, Brave, and Edge with their respective profiles and URLs
    to access multiple accounts and sessions simultaneously.
    """
    commands = [
        # Chrome Default Profile -> Google Drive
        r'start chrome --profile-directory="Default" "https://drive.google.com"',
        
        # Chrome Profile 2 -> ChatGPT
        r'start chrome --profile-directory="Profile 2" "https://chatgpt.com"',
        
        # Brave Default Profile -> Claude
        r'start brave --profile-directory="Default" "https://claude.ai"',
        
        # Edge Default Profile -> NotebookLM
        r'start msedge --profile-directory="Default" "https://notebooklm.google.com"'
    ]

    print("[+] Abriendo navegadores con perfiles y cuentas independientes...")
    for cmd in commands:
        try:
            print(f"Ejecutando: {cmd}")
            subprocess.run(f"cmd.exe /c {cmd}", shell=True)
        except Exception as e:
            print(f"Error al abrir {cmd}: {e}")

if __name__ == "__main__":
    launch_browsers()
