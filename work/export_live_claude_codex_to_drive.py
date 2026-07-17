from __future__ import annotations

import csv
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


WORKSPACE = Path(r"C:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
CSV_IN = WORKSPACE / "work" / "live_claude_codex_sessions.csv"
DRIVE_ROOT = Path(r"G:\Mi unidad")
CONV_ROOT = DRIVE_ROOT / "01_CONVERSACIONES_POR_IA"
INVENTORY_ROOT = DRIVE_ROOT / "00_INVENTARIO"

CLAUDE_OUT = CONV_ROOT / "ClaudeCode_DesktopLive_20260607"
CODEX_OUT = CONV_ROOT / "Codex_Sesiones_Live_20260607"
RAW_OUT = DRIVE_ROOT / "04_CRUDOS_TROCEADOS" / "LIVE_CLAUDE_CODEX_RAW_20260607"
INDEX_OUT = INVENTORY_ROOT / "00_INDICE_LIVE_CLAUDE_CODEX_20260607.csv"
REPORT_OUT = INVENTORY_ROOT / "00_LIVE_CLAUDE_CODEX_EXPORT_20260607.md"


def trim_filename(name: str, limit: int = 130) -> str:
    name = re.sub(r"[^\w\-.() áéíóúÁÉÍÓÚñÑ]+", "_", name, flags=re.UNICODE)
    name = re.sub(r"_+", "_", name).strip("._ ")
    return name[:limit] or "untitled"


def text_from_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
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


def extract_event(obj: dict[str, Any]) -> tuple[str, str, str]:
    timestamp = str(obj.get("timestamp") or obj.get("created_at") or obj.get("createdAt") or "")
    title = ""
    role = str(obj.get("role") or obj.get("type") or "")
    text = ""
    if isinstance(obj.get("aiTitle"), str):
        title = obj["aiTitle"]
    if isinstance(obj.get("title"), str):
        title = obj["title"]
    if isinstance(obj.get("payload"), dict):
        payload = obj["payload"]
        role = str(payload.get("role") or payload.get("type") or role)
        text = text_from_content(payload.get("content"))
        if isinstance(payload.get("timestamp"), str) and not timestamp:
            timestamp = payload["timestamp"]
        if isinstance(payload.get("title"), str):
            title = payload["title"]
    if isinstance(obj.get("message"), dict):
        msg = obj["message"]
        role = str(msg.get("role") or role)
        text = text_from_content(msg.get("content"))
    if not text:
        text = text_from_content(obj.get("content")) or text_from_content(obj.get("text"))
    return role.lower(), text, timestamp or title


def parse_messages(path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    metadata: dict[str, Any] = {
        "title": "",
        "session_id": "",
        "cli_session_id": "",
        "events_total": 0,
        "json_errors": 0,
        "non_message_events": 0,
    }
    messages: list[dict[str, str]] = []
    if path.suffix.lower() == ".jsonl":
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in lines:
            if not line.strip():
                continue
            metadata["events_total"] += 1
            try:
                obj = json.loads(line)
            except Exception:
                metadata["json_errors"] += 1
                continue
            if not isinstance(obj, dict):
                continue
            if isinstance(obj.get("aiTitle"), str):
                metadata["title"] = obj["aiTitle"]
            if isinstance(obj.get("sessionId"), str):
                metadata["session_id"] = obj["sessionId"]
            role, text, timestamp = extract_event(obj)
            if role in {"user", "assistant", "human", "claude"} and text:
                normalized_role = "user" if role in {"user", "human"} else "assistant"
                messages.append({"role": normalized_role, "timestamp": timestamp, "text": text})
            else:
                metadata["non_message_events"] += 1
    else:
        try:
            obj = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:  # noqa: BLE001
            metadata["json_errors"] += 1
            messages.append({"role": "system", "timestamp": "", "text": f"Could not parse JSON metadata: {exc}"})
            return messages, metadata
        if isinstance(obj, dict):
            metadata["title"] = obj.get("title", "")
            metadata["session_id"] = obj.get("sessionId", "")
            metadata["cli_session_id"] = obj.get("cliSessionId", "")
            metadata["events_total"] = 1
            fields = [
                ("title", obj.get("title", "")),
                ("sessionId", obj.get("sessionId", "")),
                ("cliSessionId", obj.get("cliSessionId", "")),
                ("cwd", obj.get("cwd", "")),
                ("model", obj.get("model", "")),
                ("createdAt", obj.get("createdAt", "")),
                ("lastActivityAt", obj.get("lastActivityAt", "")),
            ]
            text = "\n".join(f"- {k}: {v}" for k, v in fields if v not in ("", None))
            messages.append({"role": "metadata", "timestamp": "", "text": text or json.dumps(obj, ensure_ascii=False, indent=2)})
    return messages, metadata


def write_markdown(row: dict[str, str], out_dir: Path) -> dict[str, Any]:
    source_path = Path(row["path"])
    messages, meta = parse_messages(source_path)
    modified = row.get("modified", "")
    date_prefix = modified[:10] if modified else datetime.fromtimestamp(source_path.stat().st_mtime).strftime("%Y-%m-%d")
    title = meta.get("title") or row.get("title") or source_path.stem
    filename = f"{date_prefix}_{trim_filename(row['source'])}_{trim_filename(title or source_path.stem)}_{source_path.stem}.md"
    out_path = out_dir / filename
    raw_copy_path = RAW_OUT / row["source"] / source_path.name

    out_dir.mkdir(parents=True, exist_ok=True)
    raw_copy_path.parent.mkdir(parents=True, exist_ok=True)
    if not raw_copy_path.exists():
        shutil.copy2(source_path, raw_copy_path)

    lines = [
        f"# {title or source_path.stem}",
        "",
        "## Metadata",
        f"- Source family: {row['source']}",
        f"- Original path: `{source_path}`",
        f"- Raw copy: `{raw_copy_path}`",
        f"- Modified: {modified}",
        f"- Bytes: {row.get('bytes', source_path.stat().st_size)}",
        f"- Session id: {meta.get('session_id') or row.get('session_id') or ''}",
        f"- CLI session id: {meta.get('cli_session_id') or row.get('cli_session_id') or ''}",
        f"- Events total: {meta.get('events_total', 0)}",
        f"- Non-message events: {meta.get('non_message_events', 0)}",
        f"- JSON errors: {meta.get('json_errors', 0)}",
        "",
        "## Transcript",
    ]
    if not messages:
        lines.append("_No role/content transcript messages were found in this file. Metadata/raw copy preserved._")
    for i, msg in enumerate(messages, start=1):
        role = msg["role"].upper()
        ts = f" · {msg['timestamp']}" if msg.get("timestamp") else ""
        lines.append("")
        lines.append(f"### {i}. {role}{ts}")
        lines.append("")
        lines.append(msg["text"].replace("\r\n", "\n").strip())
    if not out_path.exists():
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "source": row["source"],
        "source_path": str(source_path),
        "output_md": str(out_path),
        "raw_copy": str(raw_copy_path),
        "title": title,
        "modified": modified,
        "bytes": row.get("bytes", ""),
        "messages": len(messages),
        "user_messages": sum(1 for m in messages if m["role"] == "user"),
        "assistant_messages": sum(1 for m in messages if m["role"] == "assistant"),
        "events_total": meta.get("events_total", 0),
        "json_errors": meta.get("json_errors", 0),
    }


def main() -> None:
    if not DRIVE_ROOT.exists():
        raise SystemExit(f"Drive root not available: {DRIVE_ROOT}")
    rows = list(csv.DictReader(CSV_IN.open(encoding="utf-8")))
    exported: list[dict[str, Any]] = []
    for row in rows:
        if row["source"] == "claude_projects":
            exported.append(write_markdown(row, CLAUDE_OUT))
        elif row["source"] == "codex_sessions":
            exported.append(write_markdown(row, CODEX_OUT))
        elif row["source"] == "claude_desktop_code_sessions":
            exported.append(write_markdown(row, CLAUDE_OUT / "_desktop_metadata"))

    INVENTORY_ROOT.mkdir(parents=True, exist_ok=True)
    with INDEX_OUT.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "source",
            "source_path",
            "output_md",
            "raw_copy",
            "title",
            "modified",
            "bytes",
            "messages",
            "user_messages",
            "assistant_messages",
            "events_total",
            "json_errors",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(exported)

    total_user = sum(int(x["user_messages"]) for x in exported)
    total_assistant = sum(int(x["assistant_messages"]) for x in exported)
    report = [
        "# Live Claude/Codex Export - 2026-06-07",
        "",
        f"- Exported markdown files: {len(exported)}",
        f"- User messages preserved: {total_user}",
        f"- Assistant messages preserved: {total_assistant}",
        f"- Claude output folder: `{CLAUDE_OUT}`",
        f"- Codex output folder: `{CODEX_OUT}`",
        f"- Raw copy folder: `{RAW_OUT}`",
        f"- Index CSV: `{INDEX_OUT}`",
        "",
        "No files were deleted or moved. Existing Drive corpus folders were not overwritten; new folders were added.",
    ]
    REPORT_OUT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"exported={len(exported)}")
    print(f"user_messages={total_user}")
    print(f"assistant_messages={total_assistant}")
    print(f"index={INDEX_OUT}")
    print(f"report={REPORT_OUT}")


if __name__ == "__main__":
    main()
