import os
import sys
import subprocess
import json

def get_usb_drives():
    """
    Scans Windows system for removable USB drives using PowerShell.
    """
    ps_cmd = "Get-Volume | Where-Object DriveType -eq 'Removable' | Select-Object DriveLetter, FriendlyName, Size, SizeRemaining | ConvertTo-Json"
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            drives = json.loads(res.stdout)
            if isinstance(drives, dict):
                drives = [drives]
            return drives
    except Exception as e:
        print(f"Error querying USB drives: {e}")
    return []

def print_preparation_guide():
    print("==========================================================================")
    print("         GUIA Y SCRIPT DE PREPARACION DE USB BOOTEABLE (LIVE OS)          ")
    print("==========================================================================")
    print("\n1. ESCANEO DE UNIDADES USB CONECTADAS:")
    drives = get_usb_drives()
    if drives:
        for d in drives:
            letter = d.get('DriveLetter', 'Unknown')
            name = d.get('FriendlyName', 'USB Drive')
            size_gb = round(d.get('Size', 0) / (1024**3), 2)
            print(f"   [+] Unidad detectada: {letter}: ({name}) - {size_gb} GB")
    else:
        print("   [!] No se detectó automáticamente la unidad USB (o requiere confirmación manual).")
        print("   Por favor verifica la letra de la unidad en 'Este equipo' (ej. E:, F:, G:).")

    print("\n2. PASOS RECOMENDADOS PARA CONFIGURAR LA USB:")
    print("   A) Herramienta de Flasheo: Ventoy (Recomendado)")
    print("      - Descarga Ventoy de: https://github.com/ventoy/Ventoy/releases")
    print("      - Ejecuta Ventoy2Disk.exe y selecciona tu memoria USB.")
    print("      - Haz clic en 'Instalar'. Esto dejará la USB lista para arrancar cualquier ISO.")
    print("\n   B) Sistema Operativo Recomendado (ISO):")
    print("      - Linux Mint 21 Cinnamon (ISO): https://linuxmint.com/download.php")
    print("      - Copia el archivo .iso descargado directamente dentro de la memoria USB.")
    print("\n   C) Herramientas Pre-cargadas al Arrancar (Brave, Antigravity, Codex):")
    print("      - Una vez que la PC arranque desde la USB, abre el navegador (Brave/Firefox) e ingresa a:")
    print("        1. Antigravity IDE / Codespaces Web: https://github.com/codespaces")
    print("        2. Google Drive: https://drive.google.com")
    print("        3. Codex CLI: 'pip install codex-cli' o vía terminal web")

if __name__ == "__main__":
    print_preparation_guide()
