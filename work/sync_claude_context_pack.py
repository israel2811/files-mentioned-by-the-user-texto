from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path


ROOTS = [
    ("claude_desktop", Path(os.environ.get("APPDATA", "")) / "Claude"),
    ("claude_code_appdata", Path(os.environ.get("APPDATA", "")) / "Claude" / "claude-code-sessions"),
    ("claude_cli", Path(os.environ.get("USERPROFILE", "")) / ".claude"),
    ("codex", Path(os.environ.get("USERPROFILE", "")) / ".codex" / "sessions"),
]

DRIVE = Path(r"G:\Mi unidad")
OUT_DIR = DRIVE / "01_CONVERSACIONES_POR_IA" / "SYNC_CLAUDE_CODEX_ANTIGRAVITY_20260608"
LOG = DRIVE / "00_LOG_DESKTOP.md"
ATTACHMENT = Path(r"C:\Users\Dell\.codex\attachments\c6f7b0e6-a27b-4ae6-939d-d0214c8f9f4b\pasted-text.txt")

TEXT_EXTS = {".json", ".jsonl", ".md", ".txt", ".log"}
MAX_FILES_PER_ROOT = 250
MAX_BYTES_READ = 8_000_000
KEYWORDS = re.compile(
    r"NEXUS|CCA|AAV|VAH|alucin|tesis|M0|M13|dedup|duplicad|Gemini|NotebookLM|Antigravity|Claude Code|Codex|Google Drive|G:\\\\Mi unidad|03_FUENTES|02_TESIS|01_CONVERSACIONES",
    re.I,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_read(path: Path) -> str:
    try:
        data = path.read_bytes()[:MAX_BYTES_READ]
    except Exception as exc:
        return f"[READ_ERROR] {exc}"
    for enc in ("utf-8", "utf-16", "latin-1"):
        try:
            return data.decode(enc, errors="replace")
        except Exception:
            continue
    return data.decode("utf-8", errors="replace")


def iter_candidate_files(root: Path):
    if not root.exists():
        return []
    files = []
    try:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_EXTS:
                try:
                    st = path.stat()
                except OSError:
                    continue
                files.append((path, st.st_size, st.st_mtime))
    except Exception:
        return files
    files.sort(key=lambda item: item[2], reverse=True)
    return files[:MAX_FILES_PER_ROOT]


def extract_jsonl_messages(text: str):
    messages = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        role = obj.get("role") or obj.get("type") or obj.get("event") or ""
        content = obj.get("content") or obj.get("message") or obj.get("text") or ""
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(str(item.get("text") or item.get("content") or ""))
                else:
                    parts.append(str(item))
            content = "\n".join(p for p in parts if p)
        elif isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        if content:
            messages.append({"role": str(role), "content": str(content)[:6000]})
    return messages


def excerpt_relevant(text: str, max_chars: int = 14000) -> str:
    hits = []
    for match in KEYWORDS.finditer(text):
        start = max(0, match.start() - 900)
        end = min(len(text), match.end() + 1800)
        hits.append(text[start:end])
        if sum(len(h) for h in hits) > max_chars:
            break
    if hits:
        return "\n\n--- excerpt ---\n\n".join(hits)[:max_chars]
    return text[:4000]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    relevant = []
    newest = []

    for source, root in ROOTS:
        for path, size, mtime in iter_candidate_files(root):
            rel = str(path)
            sha = ""
            if size <= MAX_BYTES_READ:
                try:
                    sha = sha256_file(path)
                except Exception:
                    sha = ""
            text = safe_read(path) if size <= MAX_BYTES_READ else ""
            is_relevant = bool(text and KEYWORDS.search(text))
            row = {
                "source": source,
                "path": rel,
                "bytes": size,
                "mtime_iso": datetime.fromtimestamp(mtime).isoformat(timespec="seconds"),
                "sha256": sha,
                "relevant": str(is_relevant),
            }
            rows.append(row)
            newest.append(row)
            if is_relevant:
                messages = extract_jsonl_messages(text) if path.suffix.lower() == ".jsonl" else []
                relevant.append((row, text, messages))

    newest.sort(key=lambda r: r["mtime_iso"], reverse=True)
    relevant.sort(key=lambda item: item[0]["mtime_iso"], reverse=True)

    if ATTACHMENT.exists():
        att_text = safe_read(ATTACHMENT)
        att_path = OUT_DIR / "00_PROMPT_ADJUNTO_USUARIO_20260608.md"
        att_path.write_text("# Prompt adjunto del usuario\n\n" + att_text, encoding="utf-8", newline="\n")
    else:
        att_text = ""

    with (OUT_DIR / "00_INDICE_SESIONES_CLAUDE_CODEX_20260608.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "path", "bytes", "mtime_iso", "sha256", "relevant"])
        writer.writeheader()
        writer.writerows(rows)

    md_lines = [
        "# SYNC Claude/Codex/Antigravity 2026-06-08",
        "",
        "Objetivo: poner al corriente a Codex, Claude Desktop/Claude Code y Antigravity usando conversaciones locales recientes, especialmente prompts de Claude Code relacionados con NEXUS/CCA.",
        "",
        "Reglas heredadas del usuario:",
        "- NO borrar nada permanente.",
        "- NO tocar carpetas de respaldo.",
        "- Cuarentenas o duplicados solo en carpetas `99_` y de forma reversible.",
        "- Bancar todo en `G:\\Mi unidad`.",
        "- Prioridad: Gemini/NotebookLM, fuentes DOI, manuscrito M0-M13, dedup por contenido.",
        "",
        f"Archivos indexados: {len(rows)}",
        f"Archivos relevantes por keyword: {len(relevant)}",
        "",
        "## Mas recientes",
        "",
    ]
    for row in newest[:30]:
        md_lines.append(f"- `{row['mtime_iso']}` `{row['source']}` `{row['bytes']}` {row['path']}")

    md_lines.extend(["", "## Extractos relevantes recientes", ""])
    for idx, (row, text, messages) in enumerate(relevant[:20], 1):
        md_lines.extend(
            [
                f"### {idx}. {row['source']} - {row['mtime_iso']}",
                "",
                f"- Path: `{row['path']}`",
                f"- Bytes: {row['bytes']}",
                f"- SHA256: `{row['sha256']}`",
                "",
            ]
        )
        user_msgs = [m for m in messages if re.search(r"user|human", m["role"], re.I)]
        if user_msgs:
            md_lines.append("#### Ultimos prompts de usuario detectados")
            for msg in user_msgs[-8:]:
                md_lines.append("")
                md_lines.append("> " + msg["content"].replace("\n", "\n> ")[:2500])
            md_lines.append("")
        md_lines.append("#### Extracto por keyword")
        md_lines.append("")
        md_lines.append(excerpt_relevant(text))
        md_lines.append("")

    if att_text:
        md_lines.extend(["## Prompt adjunto actual", "", att_text[:12000], ""])

    handoff = "\n".join(md_lines) + "\n"
    (OUT_DIR / "00_HANDOFF_SYNC_CLAUDE_CODEX_ANTIGRAVITY_20260608.md").write_text(
        handoff, encoding="utf-8", newline="\n"
    )

    prompt_for_agents = f"""# Prompt de sincronizacion para Claude Code / Antigravity / Codex

Lee primero:
`{OUT_DIR / "00_HANDOFF_SYNC_CLAUDE_CODEX_ANTIGRAVITY_20260608.md"}`

Objetivo comun:
1. Mantener continuidad NEXUS/CCA sin repetir auditorias ya hechas.
2. Extraer Gemini y NotebookLM a `G:\\Mi unidad\\01_CONVERSACIONES_POR_IA`.
3. Completar fuentes DOI en `G:\\Mi unidad\\03_FUENTES`.
4. Mantener/manuscrito M0-M13 en `G:\\Mi unidad\\02_TESIS`, con DOI o POR-VALIDAR.
5. Completar dedup por contenido; no borrar permanente; cuarentena reversible en `99_`.
6. No tocar carpetas de respaldo.

Trabaja desde evidencia actual y registra cada avance en `G:\\Mi unidad\\00_LOG_DESKTOP.md`.
"""
    (OUT_DIR / "01_PROMPT_PARA_LAS_3_IAS_20260608.md").write_text(
        prompt_for_agents, encoding="utf-8", newline="\n"
    )

    with LOG.open("a", encoding="utf-8", newline="\n") as f:
        f.write(
            f"\n\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} - SYNC Claude/Codex/Antigravity\n"
            f"- Generado paquete de sincronizacion: {OUT_DIR}\n"
            f"- Indexados {len(rows)} archivos locales; relevantes {len(relevant)}.\n"
            "- Sin borrar, mover ni tocar respaldos.\n"
        )

    print(f"OUT_DIR={OUT_DIR}")
    print(f"ROWS={len(rows)}")
    print(f"RELEVANT={len(relevant)}")


if __name__ == "__main__":
    main()
