from __future__ import annotations

import csv
from pathlib import Path


WORKSPACE = Path(r"C:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
MANIFEST = Path(r"G:\Mi unidad\00_INVENTARIO\00_GDOCS_CONVERSION_MANIFEST.csv")
PILOT_DIR = WORKSPACE / "work" / "gdoc_pilot"
PILOT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig")))
    candidates = [
        r
        for r in rows
        if r["status"] == "needs_txt_or_html_wrapper"
        and int(float(r["bytes"] or 0)) > 1000
        and int(float(r["bytes"] or 0)) < 80_000
        and Path(r["source_path"]).suffix.lower() == ".md"
    ]
    candidates.sort(key=lambda r: (r["platform"] != "ClaudeCode_DesktopLive_20260607", int(float(r["bytes"] or 0))))
    if not candidates:
        raise SystemExit("No pilot candidates found.")
    row = candidates[0]
    src = Path(row["source_path"])
    text = src.read_text(encoding="utf-8", errors="replace")
    out = PILOT_DIR / f"{src.stem}.txt"
    out.write_text(text, encoding="utf-8")
    print(f"source={src}")
    print(f"pilot_txt={out}")
    print(f"title=NEXUS_PILOT_GDOC_{src.stem}")
    print(f"bytes={out.stat().st_size}")


if __name__ == "__main__":
    main()
