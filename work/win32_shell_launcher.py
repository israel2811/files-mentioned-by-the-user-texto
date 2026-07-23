import ctypes
import os
import sys
import time

def launch_via_shellexecute():
    """
    Form 1: Uses Windows Win32 ShellExecuteW API directly to spawn GUI processes.
    This bypasses stdio redirection to NUL completely.
    """
    print("[Method 1] Launching via Win32 ShellExecuteW API...")
    
    # 1. Codex / Codex Beta
    codex_exe = r"C:\Users\Dell\AppData\Local\OpenAI\Codex\bin\5dee10576ec7a5b8\codex.exe"
    if os.path.exists(codex_exe):
        ctypes.windll.shell32.ShellExecuteW(None, "open", codex_exe, "", None, 1)
    ctypes.windll.shell32.ShellExecuteW(None, "open", "cmd.exe", "/c start codex", None, 0)
    
    # 2. Chrome Default -> Google Drive
    ctypes.windll.shell32.ShellExecuteW(None, "open", "chrome.exe", '--profile-directory="Default" "https://drive.google.com"', None, 1)
    
    # 3. Chrome Profile 2 -> ChatGPT
    ctypes.windll.shell32.ShellExecuteW(None, "open", "chrome.exe", '--profile-directory="Profile 2" "https://chatgpt.com"', None, 1)
    
    # 4. Brave -> Claude AI
    ctypes.windll.shell32.ShellExecuteW(None, "open", "brave.exe", '--profile-directory="Default" "https://claude.ai"', None, 1)
    
    # 5. Edge -> NotebookLM
    ctypes.windll.shell32.ShellExecuteW(None, "open", "msedge.exe", '--profile-directory="Default" "https://notebooklm.google.com"', None, 1)

if __name__ == "__main__":
    launch_via_shellexecute()
