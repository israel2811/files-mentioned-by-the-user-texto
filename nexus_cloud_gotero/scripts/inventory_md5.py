#!/usr/bin/env python3
"""Create inventory and verified duplicate report by content hash."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
from collections import defaultdict
from pathlib import Path


SKIP_PARTS = {
    ".git",
    "node_modules",
    "__pycache__",
}


def md5_file(path: Path, block_size: int = 1024 * 1024) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        while True:
            block = f.read(block_size)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & SKIP_PARTS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dupes", required=True)
    parser.add_argument("--hash", action="store_true", help="Calculate MD5. Without this, inventory only.")
    args = parser.parse_args()
    root = Path(args.root)
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_PARTS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if should_skip(path):
                continue
            try:
                st = path.stat()
                digest = md5_file(path) if args.hash else ""
                rows.append(
                    {
                        "path": str(path),
                        "name": path.name,
                        "suffix": path.suffix.lower(),
                        "bytes": st.st_size,
                        "mtime_epoch": int(st.st_mtime),
                        "md5": digest,
                    }
                )
            except OSError as exc:
                rows.append(
                    {
                        "path": str(path),
                        "name": path.name,
                        "suffix": path.suffix.lower(),
                        "bytes": "",
                        "mtime_epoch": "",
                        "md5": "",
                        "error": str(exc),
                    }
                )
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["path", "name", "suffix", "bytes", "mtime_epoch", "md5", "error"]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    groups = defaultdict(list)
    for row in rows:
        if row.get("md5") and row.get("bytes") not in ("", 0, "0"):
            groups[(row["md5"], row["bytes"])].append(row)
    duplicate_rows = []
    for (digest, size), group in groups.items():
        if len(group) < 2:
            continue
        group.sort(key=lambda r: (int(r["mtime_epoch"]), r["path"]))
        keep = group[0]
        for dup in group[1:]:
            duplicate_rows.append(
                {
                    "md5": digest,
                    "bytes": size,
                    "keep_path": keep["path"],
                    "duplicate_path": dup["path"],
                    "status": "verified_identical_hash_do_not_delete_without_ok",
                }
            )
    dupes = Path(args.dupes)
    dupes.parent.mkdir(parents=True, exist_ok=True)
    with dupes.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["md5", "bytes", "keep_path", "duplicate_path", "status"],
        )
        writer.writeheader()
        writer.writerows(duplicate_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

