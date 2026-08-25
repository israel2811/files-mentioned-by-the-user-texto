# fix_stuck_keys.py
# Libera inmediatamente cualquier tecla modificadora (ALT, CTRL, SHIFT, WIN) que haya quedado presionada en Windows
# y deshabilita StickyKeys en el registro para evitar bloqueos recurrentes.

import ctypes
import time
import winreg

user32 = ctypes.windll.user32

# Constantes Win32 Virtual Key
VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4    # Left ALT
VK_RMENU = 0xA5    # Right ALT
VK_MENU = 0x12     # General ALT
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1
VK_LWIN = 0x5B
VK_RWIN = 0x5C

KEYEVENTF_KEYUP = 0x0002

def release_all_modifier_keys():
    """Envía eventos de KEYUP para todas las teclas modificadoras."""
    keys = [VK_LMENU, VK_RMENU, VK_MENU, VK_LCONTROL, VK_RCONTROL, VK_LSHIFT, VK_RSHIFT, VK_LWIN, VK_RWIN]
    for vk in keys:
        # Enviar key up
        user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
    print("[Fix Keys] Eventos KEYUP emitidos para ALT, CTRL, SHIFT y WIN.")

def disable_sticky_keys_registry():
    """Desactiva las teclas especiales (Sticky Keys) en el Registro de Windows."""
    try:
        key_path = r"Control Panel\Accessibility\StickyKeys"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            # Flags: 506 (desactiva el atajo de 5 shifts y el sonido/anclaje)
            winreg.SetValueEx(key, "Flags", 0, winreg.REG_SZ, "506")
        print("[Fix Keys] Sticky Keys desactivado en el Registro de Windows.")
    except Exception as e:
        print(f"[Fix Keys Warning] No se pudo alterar registro de Sticky Keys: {e}")

if __name__ == "__main__":
    print("="*60)
    print("   DESBLOQUEADOR DE TECLAS MODIFICADORAS (ALT/CTRL/SHIFT)")
    print("="*60)
    release_all_modifier_keys()
    disable_sticky_keys_registry()
    print("[OK] Teclas liberadas exitosamente.")
