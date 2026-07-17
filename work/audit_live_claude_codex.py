from __future__ import annotations

import csv
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


WORKSPACE = Path(r"C:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
OUT_DIR = WORKSPACE / "outputs"
WORK_DIR = WORKSPACE / "work"
OUT_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

REPORT = OUT_DIR / "NEXUS_LIVE_CLAUDE_CODE_AUDIT.md"
CSV_OUT = WORK_DIR / "live_claude_codex_sessions.csv"

USER = Path(os.environ.get("USERPROFILE", r"C:\Users\Dell"))
APPDATA = Path(os.environ.get("APPDATA", r"C:\Users\Dell\AppData\Roaming"))

SOURCES = {
    "claude_projects": USER / ".claude" / "projects",
    "claude_desktop_code_sessions": APPDATA / "Claude" / "claude-code-sessions",
    "claude_desktop_local_agent": APPDATA / "Claude" / "local-agent-mode-sessions",
    "codex_sessions": USER / ".codex" / "sessions",
}

KEYWORDS = [
    "NEXUS",
    "CCA",
    "AAV",
    "ChatGPT",
    "Claude",
    "Claude Code",
    "Gemini",
    "NotebookLM",
    "Codex",
    "Antigravity",
    "Google Drive",
    "gdoc",
    "Google Docs",
    "Drive",
    "inventario",
    "duplicados",
    "MD5",
    "tesis",
    "fuentes",
    "PubMed",
    "bioRxiv",
    "ChEMBL",
    "ClinicalTrials",
    "MCP",
    "Codespaces",
    "Browser",
    "Edge",
    "Brave",
    "Chrome",
]


def trim(text: str, limit: int = 520) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[: limit - 1] + "..." if len(text) > limit else text


def text_from_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if isinstance(item.get("text"), str):
                    parts.append(item["text"])
                elif isinstance(item.get("content"), str):
                    parts.append(item["content"])
        return "\n".join(parts)
    if isinstance(content, dict):
        if isinstance(content.get("text"), str):
            return content["text"]
        if isinstance(content.get("content"), str):
            return content["content"]
    return ""


def extract_role_text(obj: dict[str, Any]) -> tuple[str, str]:
    # Claude Code JSONL often stores either {type,user/message} or nested message objects.
    role = str(obj.get("role") or obj.get("type") or "")
    text = ""
    if "payload" in obj and isinstance(obj["payload"], dict):
        payload = obj["payload"]
        payload_role = str(payload.get("role") or payload.get("type") or "")
        payload_text = text_from_content(payload.get("content"))
        if payload_text:
            return payload_role.lower(), payload_text
    if "message" in obj and isinstance(obj["message"], dict):
        msg = obj["message"]
        role = str(msg.get("role") or role)
        text = text_from_content(msg.get("content"))
    if not text:
        text = text_from_content(obj.get("content"))
    if not text:
        text = text_from_content(obj.get("text"))
    return role.lower(), text


def parse_jsonl(path: Path) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "path": str(path),
        "source": "",
        "bytes": path.stat().st_size,
        "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        "line_count": 0,
        "json_errors": 0,
        "user_messages": 0,
        "assistant_messages": 0,
        "tool_results": 0,
        "first_user": "",
        "last_user": "",
        "last_assistant": "",
        "keyword_hits": "",
        "title": "",
        "session_id": "",
        "cli_session_id": "",
        "timestamps": [],
    }
    keyword_counts: Counter[str] = Counter()
    first_user = ""
    last_user = ""
    last_assistant = ""
    timestamps: list[str] = []

    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                summary["line_count"] += 1
                try:
                    obj = json.loads(line)
                except Exception:
                    summary["json_errors"] += 1
                    continue
                if isinstance(obj, dict):
                    if isinstance(obj.get("aiTitle"), str):
                        summary["title"] = obj["aiTitle"]
                    if isinstance(obj.get("title"), str):
                        summary["title"] = obj["title"]
                    if isinstance(obj.get("sessionId"), str):
                        summary["session_id"] = obj["sessionId"]
                    if isinstance(obj.get("cliSessionId"), str):
                        summary["cli_session_id"] = obj["cliSessionId"]
                    if isinstance(obj.get("payload"), dict):
                        payload = obj["payload"]
                        if isinstance(payload.get("id"), str) and not summary["session_id"]:
                            summary["session_id"] = payload["id"]
                        if isinstance(payload.get("title"), str) and not summary["title"]:
                            summary["title"] = payload["title"]
                    for tkey in ("timestamp", "created_at", "createdAt", "date"):
                        if isinstance(obj.get(tkey), str):
                            timestamps.append(obj[tkey])
                            break
                    role, text = extract_role_text(obj)
                    if not text and isinstance(obj.get("toolUseResult"), (dict, list, str)):
                        summary["tool_results"] += 1
                    if role in {"user", "human"}:
                        summary["user_messages"] += 1
                        if text:
                            if not first_user:
                                first_user = text
                            last_user = text
                    elif role in {"assistant", "claude"}:
                        summary["assistant_messages"] += 1
                        if text:
                            last_assistant = text
                    haystack = text or json.dumps(obj, ensure_ascii=False)[:2000]
                    for kw in KEYWORDS:
                        if re.search(re.escape(kw), haystack, flags=re.IGNORECASE):
                            keyword_counts[kw] += 1
    except Exception as exc:  # noqa: BLE001
        summary["json_errors"] += 1
        summary["last_user"] = f"READ_ERROR: {exc}"

    summary["first_user"] = trim(first_user)
    summary["last_user"] = trim(last_user)
    summary["last_assistant"] = trim(last_assistant)
    summary["keyword_hits"] = "; ".join(f"{k}:{v}" for k, v in keyword_counts.most_common(15))
    summary["timestamps"] = timestamps[:3] + (["..."] if len(timestamps) > 6 else []) + timestamps[-3:]
    return summary


def collect_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for source, root in SOURCES.items():
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".jsonl", ".json"}:
                continue
            # Avoid known config/credential state. This pass is about transcripts.
            name = path.name.lower()
            if "credential" in name or "auth" in name or "token" in name:
                continue
            files.append((source, path))
    files.sort(key=lambda item: item[1].stat().st_mtime, reverse=True)
    return files


def existing_drive_counts() -> dict[str, int]:
    drive_root = Path(r"G:\Mi unidad\01_CONVERSACIONES_POR_IA")
    counts: dict[str, int] = {}
    if not drive_root.exists():
        return counts
    for sub in drive_root.iterdir():
        if sub.is_dir():
            counts[sub.name] = sum(1 for p in sub.rglob("*") if p.is_file())
    return counts


def main() -> None:
    rows = []
    for source, path in collect_files():
        row = parse_jsonl(path)
        row["source"] = source
        row["basename"] = path.name
        rows.append(row)

    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "source",
            "basename",
            "path",
            "bytes",
            "modified",
            "line_count",
            "json_errors",
            "user_messages",
            "assistant_messages",
            "tool_results",
            "keyword_hits",
            "first_user",
            "last_user",
            "last_assistant",
            "title",
            "session_id",
            "cli_session_id",
            "timestamps",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["timestamps"] = " | ".join(map(str, out.get("timestamps", [])))
            writer.writerow({k: out.get(k, "") for k in fieldnames})

    source_counts = Counter(row["source"] for row in rows)
    drive_counts = existing_drive_counts()
    nexus_rows = [
        row
        for row in rows
        if re.search(
            r"NEXUS|CCA|AAV|Drive|Google|gdoc|ChatGPT|Claude|Gemini|NotebookLM|Antigravity|Codex|tesis|duplicados|inventario",
            " ".join(str(row.get(k, "")) for k in ("keyword_hits", "first_user", "last_user", "last_assistant")),
            flags=re.IGNORECASE,
        )
    ]

    lines = [
        "# NEXUS Live Claude/Codex Audit",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## What Was Checked",
        "- Claude Desktop local app data: transcript/session folders only; config/auth/token files skipped.",
        "- Claude Code project JSONL files under `.claude/projects`.",
        "- Claude Desktop `claude-code-sessions` / local-agent session files.",
        "- Codex local rollout JSONL files under `.codex/sessions`.",
        "- Existing Drive corpus counts under `G:\\Mi unidad\\01_CONVERSACIONES_POR_IA`.",
        "",
        "## Session File Counts",
    ]
    for source, count in sorted(source_counts.items()):
        lines.append(f"- {source}: {count} transcript/state files")
    lines.append("")
    lines.append("## Existing Drive Corpus Counts")
    if drive_counts:
        for name, count in sorted(drive_counts.items()):
            lines.append(f"- {name}: {count} files")
    else:
        lines.append("- Drive corpus folder not reachable in this pass.")

    lines.extend(
        [
            "",
            "## NEXUS-Relevant Recent Sessions",
            "These are not full transcripts; they are pointers plus prompt excerpts so the full source can be processed without losing context.",
        ]
    )
    for row in nexus_rows[:30]:
        lines.extend(
            [
                "",
                f"### {row['source']} / {row['basename']}",
                f"- Path: `{row['path']}`",
                f"- Title/session: {row.get('title') or '(untitled)'} · session `{row.get('session_id') or '(none)'}` · cli `{row.get('cli_session_id') or '(none)'}`",
                f"- Modified: {row['modified']} · Bytes: {row['bytes']} · Lines: {row['line_count']}",
                f"- Messages: user {row['user_messages']}, assistant {row['assistant_messages']}, parse errors {row['json_errors']}",
                f"- Keyword hits: {row['keyword_hits'] or '(none)'}",
                f"- First user excerpt: {row['first_user'] or '(none found)'}",
                f"- Last user excerpt: {row['last_user'] or '(none found)'}",
                f"- Last assistant excerpt: {row['last_assistant'] or '(none found)'}",
            ]
        )

    lines.extend(
        [
            "",
            "## Revised Plan Impact",
            "- Do not continue as if Drive already contains every Claude Code/Desktop conversation.",
            "- First export/import the local Claude Code session JSONL files found here into `01_CONVERSACIONES_POR_IA\\ClaudeCode` or a new `ClaudeCode_DesktopLive` subfolder.",
            "- Keep browser live audit separate: Chrome extension saw a live `claude.ai/recents` tab, but DOM extraction timed out; Brave/Edge need Computer Use or another browser extension path.",
            "- Only after this live-state pass should the GDocs conversion manifest and duplicate analysis resume.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report={REPORT}")
    print(f"csv={CSV_OUT}")
    print(f"rows={len(rows)}")
    print(f"nexus_rows={len(nexus_rows)}")


if __name__ == "__main__":
    main()
