# alt_key_watchdog.py
# Vigilante de 1 hora para evitar que la tecla ALT (o modificadores) quede bloqueada
# Monitorea GetAsyncKeyState y emite KEYUP automático si detecta bloqueo persistente.

import ctypes
import time
import sys
from datetime import datetime

user32 = ctypes.windll.user32

VK_LMENU = 0xA4    # Left ALT
VK_RMENU = 0xA5    # Right ALT
VK_MENU = 0x12     # General ALT
KEYEVENTF_KEYUP = 0x0002

def is_alt_pressed():
    # El bit más significativo indica si la tecla está abajo
    state_menu = user32.GetAsyncKeyState(VK_MENU) & 0x8000
    state_lmenu = user32.GetAsyncKeyState(VK_LMENU) & 0x8000
    state_rmenu = user32.GetAsyncKeyState(VK_RMENU) & 0x8000
    return (state_menu != 0) or (state_lmenu != 0) or (state_rmenu != 0)

def force_release_alt():
    user32.keybd_event(VK_LMENU, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_RMENU, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)

def run_watchdog(duration_seconds=3600, check_interval=0.5, max_stuck_time=2.0):
    start_time = time.time()
    end_time = start_time + duration_seconds
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando Vigilante de Tecla ALT por {duration_seconds/60:.1f} minutos...")
    
    # Liberar inmediatamente al inicio
    force_release_alt()
    
    stuck_counter = 0.0
    releases_count = 0

    while time.time() < end_time:
        if is_alt_pressed():
            stuck_counter += check_interval
            # Si la tecla permanece abajo por más de max_stuck_time continuo, forzar liberación
            if stuck_counter >= max_stuck_time:
                force_release_alt()
                releases_count += 1
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Detectado bloqueo continuo de ALT (> {max_stuck_time}s). Liberación forzada enviada! (Total: {releases_count})")
                stuck_counter = 0.0
        else:
            stuck_counter = 0.0
            
        time.sleep(check_interval)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Vigilancia de 1 hora completada. Total de liberaciones automáticas: {releases_count}.")

if __name__ == "__main__":
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
    run_watchdog(duration_seconds=duration)
