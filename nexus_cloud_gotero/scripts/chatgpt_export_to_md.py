#!/usr/bin/env python3
"""Convert OpenAI ChatGPT export JSON files into chronological markdown files.

Designed for Codespaces/GitHub Actions, not for low-RAM local runs.
It uses only the Python standard library and writes:
- one markdown file per conversation
- 00_INDICE_CHATGPT_CRONOLOGICO.csv
- 00_RESUMEN_CHATGPT_EXPORT.md
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any


URL_RE = re.compile(r"https?://[^\s<>)\]\"']+")
SAFE_RE = re.compile(r"[^A-Za-z0-9._-]+")


def iso_from_epoch(value: Any) -> str:
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return "undated"
    if ts <= 0:
        return "undated"
    return dt.datetime.fromtimestamp(ts, tz=dt.UTC).strftime("%Y-%m-%dT%H-%M-%SZ")


def date_prefix(value: Any) -> str:
    iso = iso_from_epoch(value)
    return iso[:10] if iso != "undated" else "undated"


def clean_title(title: str, fallback: str) -> str:
    title = (title or fallback or "sin_titulo").strip()
    title = SAFE_RE.sub("_", title)
    title = title.strip("._-")
    return title[:90] or "sin_titulo"


def content_to_text(content: Any) -> str:
    if not content:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(content_to_text(x) for x in content if x is not None)
    if isinstance(content, dict):
        ctype = content.get("content_type") or content.get("type") or ""
        if ctype == "text" and isinstance(content.get("parts"), list):
            return "\n".join(content_to_text(x) for x in content["parts"])
        if isinstance(content.get("text"), str):
            return content["text"]
        if isinstance(content.get("parts"), list):
            return "\n".join(content_to_text(x) for x in content["parts"])
        return json.dumps(content, ensure_ascii=False, sort_keys=True)
    return str(content)


def extract_messages(conv: dict[str, Any]) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    mapping = conv.get("mapping")
    if isinstance(mapping, dict):
        for node_id, node in mapping.items():
            if not isinstance(node, dict):
                continue
            msg = node.get("message")
            if not isinstance(msg, dict):
                continue
            author = msg.get("author") or {}
            role = author.get("role") or "unknown"
            text = content_to_text(msg.get("content")).strip()
            if not text:
                continue
            create_time = msg.get("create_time") or conv.get("create_time")
            messages.append(
                {
                    "node_id": node_id,
                    "role": role,
                    "create_time": create_time,
                    "text": text,
                }
            )
    elif isinstance(conv.get("messages"), list):
        for i, msg in enumerate(conv["messages"]):
            if not isinstance(msg, dict):
                continue
            role = msg.get("role") or (msg.get("author") or {}).get("role") or "unknown"
            text = content_to_text(msg.get("content") or msg.get("text")).strip()
            if not text:
                continue
            messages.append(
                {
                    "node_id": str(i),
                    "role": role,
                    "create_time": msg.get("create_time") or conv.get("create_time"),
                    "text": text,
                }
            )
    messages.sort(key=lambda x: (float(x["create_time"] or 0), x["node_id"]))
    return messages


def load_conversations(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ("conversations", "items", "data"):
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
    return []


def write_conversation(out_dir: Path, conv: dict[str, Any], source_file: Path, ordinal: int) -> dict[str, Any]:
    title = conv.get("title") or f"chatgpt_{ordinal:05d}"
    create_time = conv.get("create_time") or conv.get("update_time")
    update_time = conv.get("update_time")
    messages = extract_messages(conv)
    urls = sorted({u.rstrip(".,;") for m in messages for u in URL_RE.findall(m["text"])})
    body_parts = [
        f"# {title}",
        "",
        f"- platform: ChatGPT",
        f"- source_file: {source_file.name}",
        f"- conversation_id: {conv.get('id', '')}",
        f"- create_time: {iso_from_epoch(create_time)}",
        f"- update_time: {iso_from_epoch(update_time)}",
        f"- message_count: {len(messages)}",
        f"- url_count: {len(urls)}",
        "",
        "## URLs citadas",
        "",
    ]
    body_parts.extend([f"- {u}" for u in urls] or ["- (ninguna detectada)"])
    body_parts.append("")
    body_parts.append("## Dialogo")
    body_parts.append("")
    for m in messages:
        role = m["role"].upper()
        when = iso_from_epoch(m["create_time"])
        body_parts.append(f"### {role} - {when}")
        body_parts.append("")
        body_parts.append(m["text"])
        body_parts.append("")
    body = "\n".join(body_parts).rstrip() + "\n"
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    fname = f"{date_prefix(create_time)}_CHATGPT_{clean_title(str(title), conv.get('id', str(ordinal)))}_{ordinal:05d}.md"
    path = out_dir / fname
    path.write_text(body, encoding="utf-8")
    return {
        "platform": "ChatGPT",
        "date": date_prefix(create_time),
        "create_time": iso_from_epoch(create_time),
        "update_time": iso_from_epoch(update_time),
        "title": title,
        "conversation_id": conv.get("id", ""),
        "messages": len(messages),
        "urls": len(urls),
        "bytes": path.stat().st_size,
        "sha256": digest,
        "source_file": source_file.name,
        "output_file": str(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Folder with conversations*.json files")
    parser.add_argument("--output", required=True, help="Output folder")
    args = parser.parse_args()
    in_dir = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_files = sorted(in_dir.glob("conversations*.json")) or sorted(in_dir.glob("*.json"))
    rows: list[dict[str, Any]] = []
    ordinal = 0
    for src in json_files:
        for conv in load_conversations(src):
            ordinal += 1
            rows.append(write_conversation(out_dir, conv, src, ordinal))
    rows.sort(key=lambda r: (r["create_time"], r["title"]))
    index_path = out_dir / "00_INDICE_CHATGPT_CRONOLOGICO.csv"
    with index_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["platform"])
        writer.writeheader()
        writer.writerows(rows)
    summary = [
        "# Resumen ChatGPT export",
        "",
        f"- input: {in_dir}",
        f"- json_files: {len(json_files)}",
        f"- conversations: {len(rows)}",
        f"- total_output_bytes: {sum(int(r['bytes']) for r in rows)}",
        f"- index: {index_path.name}",
        "",
        "Todo archivo generado debe compararse por bytes/sha256 antes de importarse a Google Docs.",
        "",
    ]
    (out_dir / "00_RESUMEN_CHATGPT_EXPORT.md").write_text("\n".join(summary), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

