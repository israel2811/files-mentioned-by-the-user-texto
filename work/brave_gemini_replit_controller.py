# brave_gemini_replit_controller.py
# Controlador Remoto CDP para Brave Browser (Sesión Activa del Usuario)
# Interactúa con Google Gemini (gemini.google.com) y Replit (replit.com) a través del puerto CDP 50064 / 9222

import os
import sys
import json
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

CDP_PORTS = [50064, 9222, 50071]

class BraveCDPController:
    """
    Controla el navegador Brave activo usando Chrome DevTools Protocol (CDP).
    Reutiliza las pestañas abiertas de Gemini y Replit en la sesión autenticada del usuario.
    """
    def __init__(self, ports=None):
        self.ports = ports or CDP_PORTS
        self.active_port = None
        self.browser_version = None

    def discover_active_cdp(self) -> int:
        """
        Escanea los puertos CDP disponibles para encontrar la sesión activa de Brave.
        """
        for port in self.ports:
            try:
                url = f"http://127.0.0.1:{port}/json/version"
                req = urllib.request.Request(url, headers={"User-Agent": "NEXUS-CDP-Probe"})
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        self.active_port = port
                        self.browser_version = data.get("Browser", "Unknown Browser")
                        print(f"[Brave CDP] Conectado a {self.browser_version} en el puerto {port}")
                        return port
            except Exception:
                continue
        return None

    def list_open_tabs(self) -> list:
        """
        Obtiene la lista de pestañas abiertas en el navegador.
        """
        if not self.active_port:
            self.discover_active_cdp()
        if not self.active_port:
            print("[Brave CDP] No se detectó ningún puerto CDP abierto. Lanza Brave con --remote-debugging-port=50064.")
            return []

        try:
            url = f"http://127.0.0.1:{self.active_port}/json/list"
            req = urllib.request.Request(url, headers={"User-Agent": "NEXUS-CDP-Probe"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                tabs = json.loads(resp.read().decode("utf-8"))
                return tabs
        except Exception as e:
            print(f"[Brave CDP Error] Error al listar pestañas: {e}")
            return []

    def inspect_gemini_and_replit(self) -> dict:
        """
        Filtra las pestañas de Gemini y Replit y reporta su estado.
        """
        tabs = self.list_open_tabs()
        gemini_tabs = []
        replit_tabs = []
        other_tabs = []

        for tab in tabs:
            tab_url = tab.get("url", "")
            title = tab.get("title", "Sin título")
            tab_info = {
                "id": tab.get("id"),
                "title": title,
                "url": tab_url,
                "ws_debugger_url": tab.get("webSocketDebuggerUrl")
            }
            if "gemini.google.com" in tab_url:
                gemini_tabs.append(tab_info)
            elif "replit.com" in tab_url:
                replit_tabs.append(tab_info)
            else:
                other_tabs.append(tab_info)

        report = {
            "browser": self.browser_version or "Brave",
            "cdp_port": self.active_port,
            "gemini_active_tabs": len(gemini_tabs),
            "replit_active_tabs": len(replit_tabs),
            "total_open_tabs": len(tabs),
            "gemini_details": gemini_tabs,
            "replit_details": replit_tabs
        }
        return report

if __name__ == "__main__":
    print("=" * 60)
    print("      CONTROLADOR BRAVE CDP (GEMINI + REPLIT)         ")
    print("=" * 60)
    controller = BraveCDPController()
    port = controller.discover_active_cdp()
    if port:
        status = controller.inspect_gemini_and_replit()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    else:
        print("[INFO] Para habilitar control en vivo de tu ventana actual de Brave:")
        print("1. Cierra las instancias en segundo plano o lanza:")
        print('   & "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe" --remote-debugging-port=50064')
        print("2. Abre tus pestañas habituales de Gemini y Replit.")
        print("3. Este controlador se conectará a ellas directamente sin re-autenticar.")
