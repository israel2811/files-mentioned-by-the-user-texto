import subprocess
import sys
import os

CODESPACE_NAME = "glowing-space-bassoon-x5qqqp5qgvq4h4jr"

def run_remote_command(cmd_str):
    """
    Executes a shell command remotely inside the active GitHub Codespace VM.
    """
    ssh_cmd = ["gh", "codespace", "ssh", "-c", CODESPACE_NAME, "--", cmd_str]
    print(f"[Remote Bridge] Executing on Codespace ({CODESPACE_NAME}): {cmd_str}")
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
        print("[Remote Bridge] Output:")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[Remote Bridge Error] Exit Code {e.returncode}")
        print(e.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_cmd = " ".join(sys.argv[1:])
        run_remote_command(user_cmd)
    else:
        print("Usage: python remote_antigravity_bridge.py <command>")
        print("Example: python remote_antigravity_bridge.py 'uname -a && python3 --version'")
