#!/usr/bin/env python3
"""Export all local AI conversations to human-readable Markdown files.

Scans:
- Claude Code sessions (AppData/Roaming/Claude/claude-code-sessions)
- Claude Projects (.claude/projects)
- Codex sessions (.codex/sessions)
- Antigravity Brain logs (.gemini/antigravity-ide/brain)

Generates clean Markdown logs saved to Dropbox and the workspace output folder.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path

# Target directories
DROPBOX_OUT = Path(r"C:\Users\Dell\Dropbox\NEXUS_CONVERSACIONES_COMPLETAS")
WORKSPACE_OUT = Path(r"C:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto\outputs\conversaciones_completas")

# Source directories
CLAUDE_PROJECTS = Path(r"C:\Users\Dell\.claude\projects")
CLAUDE_CODE = Path(r"C:\Users\Dell\AppData\Roaming\Claude\claude-code-sessions")
ANTIGRAVITY_BRAIN = Path(r"C:\Users\Dell\.gemini\antigravity-ide\brain")
CODEX_SESSIONS = Path(r"C:\Users\Dell\.codex\sessions")


def clean_text(text: str) -> str:
    if not text:
        return ""
    # Strip excessive base64 blocks or huge data blocks to keep it readable
    text = re.sub(r"data:image/[a-zA-Z]+;base64,[a-zA-Z0-9+/=]+", "[IMAGE_BASE64_DATA]", text)
    return text.strip()


def format_msg(role: str, text: str) -> str:
    role_str = "USER" if role.lower() in {"user", "user_input"} else "ASSISTANT"
    return f"### **{role_str}**\n\n{text}\n\n---\n\n"


def parse_jsonl_turns(path: Path) -> list[tuple[str, str]]:
    turns = []
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    # Check for Antigravity Brain log
                    if "type" in obj and "content" in obj:
                        t = obj["type"]
                        if t == "USER_INPUT":
                            turns.append(("user", obj.get("content", "")))
                        elif t == "PLANNER_RESPONSE":
                            turns.append(("assistant", obj.get("content", "")))
                        continue
                    
                    # Check for Codex/Claude Project turns
                    role = obj.get("role") or ""
                    # Check in payload
                    payload = obj.get("payload") or {}
                    if not role and isinstance(payload, dict):
                        role = payload.get("role") or payload.get("type") or ""
                    
                    # Extract text content
                    text = ""
                    content = obj.get("content") or payload.get("content")
                    if isinstance(content, list):
                        text = "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and "text" in c)
                    elif isinstance(content, str):
                        text = content
                    
                    if not text:
                        text = obj.get("text") or payload.get("text") or ""
                        
                    if text and role:
                        turns.append((role.lower(), text))
                except Exception:
                    pass
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return [(r, clean_text(t)) for r, t in turns if t]


def parse_json_turns(path: Path) -> list[tuple[str, str]]:
    turns = []
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        # Standard array of messages
        if isinstance(data, list):
            for item in data:
                role = item.get("role") or ""
                text = item.get("content") or item.get("text") or ""
                if isinstance(text, list):
                    text = "\n".join(t.get("text", "") for t in text if isinstance(t, dict) and "text" in t)
                if role and text:
                    turns.append((role.lower(), text))
        elif isinstance(data, dict):
            # Check for turns key
            messages = data.get("messages") or data.get("turns") or data.get("events") or []
            if isinstance(messages, list):
                for item in messages:
                    role = item.get("role") or item.get("type") or ""
                    text = item.get("content") or item.get("text") or ""
                    if role and text:
                        turns.append((role.lower(), text))
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return [(r, clean_text(t)) for r, t in turns if t]


def save_conversation(name: str, date_str: str, source: str, turns: list[tuple[str, str]], orig_path: Path):
    if not turns:
        return
    
    filename = f"{source}_{date_str}_{name}.md".replace(":", "-").replace(" ", "_")
    header = f"""# Conversación Completa: {name}
- **Fuente**: {source}
- **Fecha**: {date_str}
- **Archivo Original**: {orig_path.resolve()}
- **Mensajes Totales**: {len(turns)}

---

"""
    body = "".join(format_msg(role, text) for role, text in turns)
    content = header + body
    
    # Save to both locations
    for out_dir in [DROPBOX_OUT, WORKSPACE_OUT]:
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            p = out_dir / filename
            p.write_text(content, encoding="utf-8")
        except Exception as e:
            print(f"Error writing to {out_dir}: {e}")


def main():
    print("Starting conversion of local raw logs to Markdown...")
    count = 0
    
    # 1. Claude Projects
    if CLAUDE_PROJECTS.exists():
        print("Parsing Claude Projects...")
        for p in CLAUDE_PROJECTS.glob("*.jsonl"):
            mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
            turns = parse_jsonl_turns(p)
            if turns:
                save_conversation(p.stem, mtime, "ClaudeProject", turns, p)
                count += 1

    # 2. Claude Code Sessions
    if CLAUDE_CODE.exists():
        print("Parsing Claude Code Sessions...")
        for p in CLAUDE_CODE.rglob("*.json"):
            mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
            turns = parse_json_turns(p)
            if turns:
                save_conversation(p.stem, mtime, "ClaudeCode", turns, p)
                count += 1

    # 3. Antigravity Brain (Local Agent Logs)
    if ANTIGRAVITY_BRAIN.exists():
        print("Parsing Antigravity Brain logs...")
        for transcript_path in ANTIGRAVITY_BRAIN.rglob("transcript.jsonl"):
            mtime = datetime.fromtimestamp(transcript_path.stat().st_mtime).strftime("%Y-%m-%d")
            conv_id = transcript_path.parents[2].name  # brain/<conv-id>
            turns = parse_jsonl_turns(transcript_path)
            if turns:
                save_conversation(conv_id[:8], mtime, "AntigravityAgent", turns, transcript_path)
                count += 1

    # 4. Codex Sessions
    if CODEX_SESSIONS.exists():
        print("Parsing Codex Sessions...")
        for p in CODEX_SESSIONS.rglob("*.jsonl"):
            mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
            turns = parse_jsonl_turns(p)
            if turns:
                save_conversation(p.stem[:12], mtime, "CodexSession", turns, p)
                count += 1

    print(f"\nFinished! Converted {count} conversations successfully.")


if __name__ == "__main__":
    main()
