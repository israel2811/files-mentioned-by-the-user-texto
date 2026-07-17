#!/usr/bin/env python3
"""Chunk huge text/markdown/html files into Google-Docs-friendly pieces."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path


BOUNDARY_RE = re.compile(r"(?m)^(#{1,3}\s+|---+\s*$|={3,}\s*$)")


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)[:100].strip("._-") or "chunk"


def split_text(text: str, max_bytes: int) -> list[str]:
    chunks: list[str] = []
    pos = 0
    n = len(text)
    while pos < n:
        end = min(n, pos + max_bytes)
        candidate = text[pos:end]
        if end < n:
            matches = list(BOUNDARY_RE.finditer(candidate))
            if matches and matches[-1].start() > max_bytes // 3:
                end = pos + matches[-1].start()
                candidate = text[pos:end]
            else:
                nl = candidate.rfind("\n")
                if nl > max_bytes // 2:
                    end = pos + nl
                    candidate = text[pos:end]
        chunks.append(candidate.strip() + "\n")
        pos = max(end, pos + 1)
    return chunks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-kb", type=int, default=500)
    args = parser.parse_args()
    in_dir = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    max_bytes = args.max_kb * 1024
    rows = []
    files = [p for p in in_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt", ".html", ".htm"}]
    for src in sorted(files):
        text = src.read_text(encoding="utf-8", errors="replace")
        original_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        chunks = split_text(text, max_bytes)
        stem = safe_name(src.stem)
        platform_dir = out_dir / stem
        platform_dir.mkdir(parents=True, exist_ok=True)
        for i, chunk in enumerate(chunks, 1):
            dest = platform_dir / f"{stem}_part_{i:04d}_of_{len(chunks):04d}.md"
            dest.write_text(chunk, encoding="utf-8")
            rows.append(
                {
                    "source_path": str(src),
                    "source_bytes": src.stat().st_size,
                    "source_sha256": original_sha,
                    "part": i,
                    "parts_total": len(chunks),
                    "output_path": str(dest),
                    "output_bytes": dest.stat().st_size,
                    "output_sha256": hashlib.sha256(chunk.encode("utf-8")).hexdigest(),
                }
            )
    manifest = out_dir / "00_CHUNK_MANIFEST.csv"
    with manifest.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys()) if rows else ["source_path"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

