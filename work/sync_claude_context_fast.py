#!/usr/bin/env python3
"""Fast NEXUS handoff pack for Claude/Codex/Antigravity.

This is intentionally conservative for a saturated Windows laptop:
- no full-drive scans
- no deletes or moves
- latest files only
- small excerpts plus paths, not huge copies
"""

from __future__ import annotations

import csv
import datetime as dt
import os
import re
from pathlib import Path


NOW = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
DRIVE = Path(r"G:\Mi unidad")
OUT_DIR = DRIVE / "01_CONVERSACIONES_POR_IA" / f"SYNC_FAST_CLAUDE_CODEX_ANTIGRAVITY_{NOW}"
ATTACHMENTS = [
    Path(r"C:\Users\Dell\.codex\attachments\f959bd36-27b7-4fc8-b69c-43144af4f435\pasted-text.txt"),
    Path(r"C:\Users\Dell\.codex\attachments\c6f7b0e6-a27b-4ae6-939d-d0214c8f9f4b\pasted-text.txt"),
]
KEYWORDS = re.compile(
    r"(NEXUS|CCA|AAV|VAH|alucin|tesis|dedup|Gemini|NotebookLM|Antigravity|Claude Code|Codex|Drive|GDocs|ChatGPT)",
    re.IGNORECASE,
)
TEXT_EXTS = {".txt", ".md", ".json", ".jsonl", ".log", ".csv"}
MAX_SCAN_PER_ROOT = 1500
MAX_FILES_PER_ROOT = 60
MAX_READ_BYTES = 180_000


def roots() -> list[Path]:
    home = Path.home()
    appdata = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
    local = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
    return [
        appdata / "Claude",
        home / ".claude",
        home / ".codex" / "sessions",
        home / ".gemini" / "antigravity",
        local / "AnthropicClaude",
    ]


def iter_recent_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    found: list[tuple[float, Path]] = []
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {"Cache", "GPUCache", "Code Cache", "node_modules"}]
        for name in filenames:
            scanned += 1
            if scanned > MAX_SCAN_PER_ROOT:
                break
            path = Path(dirpath) / name
            if path.suffix.lower() not in TEXT_EXTS:
                continue
            try:
                st = path.stat()
            except OSError:
                continue
            if st.st_size <= 0:
                continue
            score = st.st_mtime
            if KEYWORDS.search(str(path)):
                score += 10_000_000
            found.append((score, path))
        if scanned > MAX_SCAN_PER_ROOT:
            break
    found.sort(reverse=True, key=lambda x: x[0])
    return [p for _, p in found[:MAX_FILES_PER_ROOT]]


def read_excerpt(path: Path) -> tuple[str, int, bool]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return f"[READ_ERROR] {exc}", 0, False
    truncated = len(raw) > MAX_READ_BYTES
    if truncated:
        head = raw[: MAX_READ_BYTES // 2]
        tail = raw[-MAX_READ_BYTES // 2 :]
        raw = head + b"\n\n[...TRUNCATED_FAST_SYNC...]\n\n" + tail
    return raw.decode("utf-8", errors="replace"), len(raw), truncated


def write_log(line: str) -> None:
    log = DRIVE / "00_LOG_DESKTOP.md"
    with log.open("a", encoding="utf-8") as f:
        f.write(f"\n- {dt.datetime.now().isoformat(timespec='seconds')} {line}\n")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    handoff = [
        "# SYNC FAST Claude/Codex/Antigravity",
        "",
        f"- created: {dt.datetime.now().isoformat(timespec='seconds')}",
        "- mode: latest/relevant files only",
        "- rule: no deletes, no moves, no backup folders touched",
        "",
        "## Prompt maestro adjunto",
        "",
    ]
    for attachment in ATTACHMENTS:
        if attachment.exists():
            text, read_bytes, truncated = read_excerpt(attachment)
            dest = OUT_DIR / f"PROMPT_ADJUNTO_{attachment.parent.name}.md"
            dest.write_text(text, encoding="utf-8")
            handoff.append(f"- copied: {attachment} -> {dest.name}; truncated={truncated}")
            rows.append(
                {
                    "source": str(attachment),
                    "mtime": attachment.stat().st_mtime,
                    "bytes": attachment.stat().st_size,
                    "copied_excerpt": str(dest),
                    "truncated": truncated,
                    "notes": "attached_user_prompt",
                }
            )
    handoff.extend(
        [
            "",
            "## Instruccion operacional para las 3 IAs",
            "",
            "Tomar como vigente el prompt maestro NEXUS/CCA-AAV: terminar corpus, Drive/GDocs, fuentes DOI, tesis M0-M13, dedup por contenido y trazabilidad, sin borrar permanente y sin tocar respaldos.",
            "",
            "Prioridad inmediata:",
            "1. Usar nube/Codespaces/GitHub Actions para parseo ChatGPT, gigantes e inventario pesado.",
            "2. Usar Drive como superficie final.",
            "3. Marcar bloqueos reales en log, no inventar contenido faltante.",
            "",
            "## Archivos recientes/relevantes detectados",
            "",
        ]
    )
    for root in roots():
        files = iter_recent_files(root)
        handoff.append(f"### {root}")
        handoff.append("")
        if not files:
            handoff.append("- no files found or root missing")
            handoff.append("")
            continue
        for path in files:
            text, read_bytes, truncated = read_excerpt(path)
            rel_name = re.sub(r"[^A-Za-z0-9._-]+", "_", path.name)[:90]
            dest = OUT_DIR / f"EXCERPT_{len(rows)+1:04d}_{rel_name}.md"
            dest.write_text(
                f"# Excerpt\n\n- source: {path}\n- truncated: {truncated}\n\n```text\n{text}\n```\n",
                encoding="utf-8",
            )
            st = path.stat()
            rows.append(
                {
                    "source": str(path),
                    "mtime": st.st_mtime,
                    "bytes": st.st_size,
                    "copied_excerpt": str(dest),
                    "truncated": truncated,
                    "notes": "recent_or_keyword_ranked",
                }
            )
            handoff.append(f"- {path} ({st.st_size} bytes) -> {dest.name}; truncated={truncated}")
        handoff.append("")
    csv_path = OUT_DIR / "00_INDICE_SYNC_FAST.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["source", "mtime", "bytes", "copied_excerpt", "truncated", "notes"],
        )
        writer.writeheader()
        writer.writerows(rows)
    handoff_path = OUT_DIR / "00_HANDOFF_SYNC_FAST_CLAUDE_CODEX_ANTIGRAVITY.md"
    handoff.append("")
    handoff.append(f"Indice CSV: {csv_path.name}")
    handoff_path.write_text("\n".join(handoff), encoding="utf-8")
    write_log(f"SYNC_FAST created {OUT_DIR} with {len(rows)} indexed excerpts.")
    print(f"OUT_DIR={OUT_DIR}")
    print(f"ROWS={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

