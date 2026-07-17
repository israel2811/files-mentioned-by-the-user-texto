from __future__ import annotations

import csv
from pathlib import Path


MANIFEST = Path(r"G:\Mi unidad\00_INVENTARIO\00_GDOCS_CONVERSION_MANIFEST.csv")
PILOT_SOURCE = Path(
    r"G:\Mi unidad\01_CONVERSACIONES_POR_IA\ClaudeCode_DesktopLive_20260607\_desktop_metadata\2026-06-07_claude_desktop_code_sessions_PC performance optimization and MCP setup_local_6a0b2762-d90e-437e-9ba4-679197947576.md"
)
PILOT_URL = "https://docs.google.com/document/d/1NmLcAXs5tYanVJOkry8KDyGcF2OP25XO7HVjal0WiuM/edit?usp=drivesdk"
REPORT = Path(r"G:\Mi unidad\00_INVENTARIO\00_GDOCS_IMPORT_PILOT_20260607.md")


def main() -> None:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig")))
    touched = 0
    for row in rows:
        if Path(row["source_path"]) == PILOT_SOURCE:
            row["output_gdoc_url"] = PILOT_URL
            row["status"] = "imported_pilot_native_gdoc"
            row["notes"] = (row.get("notes", "") + "; pilot import succeeded from TXT wrapper").strip("; ")
            touched += 1
    if touched != 1:
        raise SystemExit(f"Expected to update 1 row, updated {touched}")
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    REPORT.write_text(
        "\n".join(
            [
                "# GDocs Import Pilot - 2026-06-07",
                "",
                "- Status: success",
                "- Upload mode: native Google Docs",
                f"- Source markdown: `{PILOT_SOURCE}`",
                "- Wrapper: local TXT generated in workspace `work/gdoc_pilot/`",
                f"- Native Google Doc: {PILOT_URL}",
                "",
                "Finding: the current Google Drive import tool converts TXT/HTML/DOCX to native Docs, but does not expose a target parent folder. For the full corpus, use TXT/HTML wrappers plus either a later move step or Apps Script with folder placement.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"updated_rows={touched}")
    print(f"report={REPORT}")


if __name__ == "__main__":
    main()
