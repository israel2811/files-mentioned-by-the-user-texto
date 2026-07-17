from __future__ import annotations

import csv
import json
from pathlib import Path

WORKSPACE = Path(r"C:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
CSV_IN = WORKSPACE / "work" / "live_claude_codex_sessions.csv"


def shape(value, depth=0):
    if depth > 3:
        return "..."
    if isinstance(value, dict):
        return {k: shape(v, depth + 1) for k, v in list(value.items())[:12]}
    if isinstance(value, list):
        return [shape(value[0], depth + 1)] if value else []
    if isinstance(value, str):
        return f"str[{len(value)}]"
    return type(value).__name__


def first_json_values(path: Path, limit=3):
    values = []
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    values.append(json.loads(line))
                except Exception as exc:  # noqa: BLE001
                    values.append({"parse_error": str(exc), "line_preview": line[:120]})
                if len(values) >= limit:
                    break
    else:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            values.append(json.load(f))
    return values


def main():
    rows = list(csv.DictReader(CSV_IN.open(encoding="utf-8")))
    targets = []
    for source in ["codex_sessions", "claude_desktop_code_sessions", "claude_desktop_local_agent", "claude_projects"]:
        match = next((r for r in rows if r["source"] == source), None)
        if match:
            targets.append(match)
    for row in targets:
        path = Path(row["path"])
        print(f"\n=== {row['source']} :: {path.name} ===")
        print(path)
        for i, value in enumerate(first_json_values(path), start=1):
            print(f"-- object {i} shape --")
            print(json.dumps(shape(value), ensure_ascii=False, indent=2)[:6000])


if __name__ == "__main__":
    main()
