from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak_codex_repair_{STAMP}")
    shutil.copy2(path, bak)
    return bak


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_powercfg(args: list[str], timeout: int = 8) -> dict:
    try:
        p = subprocess.run(
            ["powercfg", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "args": args,
            "returncode": p.returncode,
            "stdout": p.stdout.strip(),
            "stderr": p.stderr.strip(),
        }
    except Exception as exc:
        return {"args": args, "error": repr(exc)}


def main() -> int:
    report: dict = {"stamp": STAMP, "actions": [], "warnings": []}

    filesystem_settings = Path(
        r"C:\Users\Dell\AppData\Roaming\Claude\Claude Extensions Settings"
        r"\ant.dir.ant.anthropic.filesystem.json"
    )
    auth_cache = Path(r"C:\Users\Dell\.claude\mcp-needs-auth-cache.json")
    claude_code_settings = Path(r"C:\Users\Dell\.claude\settings.json")

    if filesystem_settings.exists():
        old = read_json(filesystem_settings)
        bak = backup(filesystem_settings)
        new = {
            "isEnabled": True,
            "userConfig": {
                "allowed_directories": [
                    r"C:\Users\Dell",
                    r"G:\Mi unidad",
                    r"C:\tmp",
                ]
            },
        }
        write_json(filesystem_settings, new)
        report["actions"].append(
            {
                "target": str(filesystem_settings),
                "backup": str(bak),
                "change": "Restricted Claude Desktop Filesystem from whole drives to user, Drive root, and temp.",
                "before": old,
                "after": new,
            }
        )
    else:
        report["warnings"].append(f"Missing filesystem settings: {filesystem_settings}")

    if auth_cache.exists():
        old_cache = read_json(auth_cache)
        bak = backup(auth_cache)
        keys_to_clear = ["plugin:pdf-viewer:pdf"]
        new_cache = {k: v for k, v in old_cache.items() if k not in keys_to_clear}
        write_json(auth_cache, new_cache)
        report["actions"].append(
            {
                "target": str(auth_cache),
                "backup": str(bak),
                "change": "Removed stale pdf-viewer auth-needed cache entry only.",
                "removed_keys": [k for k in keys_to_clear if k in old_cache],
                "remaining_keys": len(new_cache),
            }
        )
    else:
        report["warnings"].append(f"Missing MCP auth cache: {auth_cache}")

    if claude_code_settings.exists():
        settings = read_json(claude_code_settings)
        lowload = dict(settings)
        mcp = dict(settings.get("mcpServers") or {})
        keep = {"filesystem", "google-drive", "desktop-commander", "chrome-devtools-mcp"}
        lowload["mcpServers"] = {k: v for k, v in mcp.items() if k in keep}
        suggestion = claude_code_settings.with_name(
            f"settings.codex_lowload_suggestion_{STAMP}.json"
        )
        write_json(suggestion, lowload)
        report["actions"].append(
            {
                "target": str(suggestion),
                "change": "Created optional low-load Claude Code settings profile; active settings.json was not replaced.",
                "kept_mcp_servers": sorted(lowload["mcpServers"].keys()),
                "original_mcp_servers": sorted(mcp.keys()),
            }
        )

    report["powercfg_before"] = run_powercfg(["/getactivescheme"], timeout=5)
    report["powercfg_set_high_performance"] = run_powercfg(
        ["/setactive", "SCHEME_MIN"], timeout=10
    )
    report["powercfg_after"] = run_powercfg(["/getactivescheme"], timeout=5)

    out_dir = Path(r"C:\tmp")
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"nexus_mcp_repair_report_{STAMP}.json"
    write_json(report_path, report)
    print(json.dumps({"ok": True, "report": str(report_path), **report}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
