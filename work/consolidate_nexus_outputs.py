from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


DRIVE = Path(r"G:\Mi unidad")
TESIS = DRIVE / "02_TESIS"
FUENTES = DRIVE / "03_FUENTES"
STAMP = datetime.now().strftime("%Y-%m-%d %H:%M")
STAMP_FILE = datetime.now().strftime("%Y%m%d_%H%M%S")


def sha256(path: Path) -> str | None:
    if not path.exists() or path.is_dir():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_text(path: Path, max_chars: int | None = None) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return text if max_chars is None else text[:max_chars]


def md_blocks(md: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    current: list[str] = []
    in_fence = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_fence = not in_fence
            if current:
                blocks.append(("p", " ".join(current).strip()))
                current = []
            continue
        if in_fence:
            continue
        if not line.strip():
            if current:
                blocks.append(("p", " ".join(current).strip()))
                current = []
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            if current:
                blocks.append(("p", " ".join(current).strip()))
                current = []
            blocks.append((f"h{len(m.group(1))}", m.group(2).strip()))
            continue
        if re.match(r"^\s*[-*]\s+", line):
            if current:
                blocks.append(("p", " ".join(current).strip()))
                current = []
            blocks.append(("bullet", re.sub(r"^\s*[-*]\s+", "", line).strip()))
            continue
        current.append(line.strip())
    if current:
        blocks.append(("p", " ".join(current).strip()))
    return [(k, v) for k, v in blocks if v]


def p_xml(kind: str, text: str) -> str:
    style = {
        "h1": '<w:pStyle w:val="Heading1"/>',
        "h2": '<w:pStyle w:val="Heading2"/>',
        "h3": '<w:pStyle w:val="Heading3"/>',
        "bullet": '<w:pStyle w:val="ListParagraph"/>',
        "p": "",
    }.get(kind, "")
    if kind == "bullet":
        text = "- " + text
    return (
        "<w:p><w:pPr>"
        + style
        + "</w:pPr><w:r><w:t xml:space=\"preserve\">"
        + escape(text)
        + "</w:t></w:r></w:p>"
    )


def write_docx(md: str, out: Path) -> None:
    body = "\n".join(p_xml(kind, text) for kind, text in md_blocks(md))
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {body}
    <w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
  </w:body>
</w:document>"""
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document_xml)


def append_antigravity_section(md: str) -> str:
    return md + f"""

# Anexo Operacional Codex/Antigravity 2026-06-08

## Estado Antigravity y CDP

Antigravity Desktop esta instalado y funcional como aplicacion principal en `C:\\Users\\Dell\\AppData\\Local\\Programs\\Antigravity\\Antigravity.exe`, version 2.0.11.0, compania Google. Codex confirmo control real por CDP en `127.0.0.1:50064`, selecciono `Claude Opus 4.6 (Thinking)` y recibio la respuesta `ANTIGRAVITY_CDP_OK`.

El instalador pequeno `C:\\Users\\Dell\\Downloads\\Antigravity IDE.exe` fallo con el error de Windows `The setup files are corrupted`. Ese archivo mide 6,717,174 bytes, no esta firmado y su SHA256 es `B0C9A49032E8678AAD4211046CDD477198C97ED200C779E62D8A9DA87FF3EBEA`; por seguridad no se ejecuto. La fuente oficial del IDE x64 encontrada en el bundle de `https://antigravity.google/download` es `https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.0.4-6381998290370560/windows-x64/Antigravity%20IDE.exe`, con tamano esperado 228,699,760 bytes. La descarga oficial quedo parcial en `C:\\tmp\\Antigravity_IDE_2.0.4_windows_x64.exe` y no debe ejecutarse hasta completarla y verificar firma.

## Uso de Antigravity en la tesis

Antigravity produjo y fue bancado en `02_TESIS` para P01/P02. En P02 propuso una formulacion defendible de pregunta e hipotesis CCA-AAV y marco el vinculo causal CCA -> AAV como `POR-VALIDAR`, criterio que se conserva en este manuscrito. Intento lanzar subagentes de inventario, tesis, coordinacion e inventario de corpus; el modo subagente quedo bloqueado por permisos interactivos y un subagente fue cancelado al responder el dialogo por CDP. Por ello, Antigravity queda documentado como herramienta funcional pero no confiable para ejecucion masiva autonoma sin supervision de permisos.
"""


def main() -> int:
    TESIS.mkdir(parents=True, exist_ok=True)
    fuente_md = FUENTES / "00_FUENTES_CORE_APA7_CCA_AAV_2026-06-07.md"
    manuscrito_md = TESIS / "MANUSCRITO_TESIS_CCA_AAV_M0_M13_v2_2026-06-07.md"
    base = read_text(manuscrito_md)
    consolidated = append_antigravity_section(base)
    out_md = TESIS / f"MANUSCRITO_TESIS_CCA_AAV_M0_M13_v4_CONSOLIDADO_2026-06-08.md"
    out_docx = TESIS / f"MANUSCRITO_TESIS_CCA_AAV_M0_M13_v4_CONSOLIDADO_2026-06-08.docx"
    out_md.write_text(consolidated, encoding="utf-8")
    write_docx(consolidated, out_docx)

    partial = Path(r"C:\tmp\Antigravity_IDE_2.0.4_windows_x64.exe")
    bad = Path(r"C:\Users\Dell\Downloads\Antigravity IDE.exe")
    report = DRIVE / "00_INFORME_CODEX.md"
    report_text = f"""# 00_INFORME_CODEX

Actualizado: {STAMP}

## Estado ejecutivo

- Antigravity principal funciona: `C:\\Users\\Dell\\AppData\\Local\\Programs\\Antigravity\\Antigravity.exe`, Google, version 2.0.11.0.
- Control real por CDP confirmado en `127.0.0.1:50064`; modelo observado: Claude Opus 4.6 (Thinking); respuesta `ANTIGRAVITY_CDP_OK`.
- El instalador `C:\\Users\\Dell\\Downloads\\Antigravity IDE.exe` esta corrupto/no firmado y no debe ejecutarse.
- Se encontro enlace oficial del IDE x64 en el bundle de `https://antigravity.google/download`, pero la descarga quedo parcial por lentitud/timeout de red.
- Fuentes academicas: existen 40 fuentes core DOI en `G:\\Mi unidad\\03_FUENTES\\00_FUENTES_CORE_APA7_CCA_AAV_2026-06-07.md` y BibTeX asociado.
- Manuscrito: generado consolidado Markdown y DOCX en `G:\\Mi unidad\\02_TESIS`.

## Evidencia instalador Antigravity IDE

| Archivo | Bytes | Firma | SHA256 | Estado |
|---|---:|---|---|---|
| `C:\\Users\\Dell\\Downloads\\Antigravity IDE.exe` | 6,717,174 | NotSigned | `B0C9A49032E8678AAD4211046CDD477198C97ED200C779E62D8A9DA87FF3EBEA` | Corrupto; no ejecutar |
| `C:\\Users\\Dell\\Downloads\\Antigravity-x64 (1).exe` | 143,766,400 | metadatos Google Antigravity 2.0.6 | `6BE1F449426AD92880E55C49158F3DFD3DBD7BAC050C1A83DE5ABC3C2FEBF4CF` | Instalador antiguo de la app principal |
| `C:\\tmp\\Antigravity_IDE_2.0.4_windows_x64.exe` | {partial.stat().st_size if partial.exists() else 0} | pendiente | `{sha256(partial) or 'PENDIENTE'}` | Descarga oficial parcial; esperado 228,699,760 bytes |

Enlace oficial detectado en el JS de `https://antigravity.google/download`:
`https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.0.4-6381998290370560/windows-x64/Antigravity%20IDE.exe`

## Antigravity por CDP

Logica demostrada:

1. Conexion CDP a Antigravity por `127.0.0.1:50064`.
2. Lectura DOM y seleccion/confirmacion del modelo `Claude Opus 4.6 (Thinking)`.
3. Envio de prompt de prueba y respuesta `ANTIGRAVITY_CDP_OK`.
4. Envio de prompts P01/P02 y banca de resultados en `02_TESIS`.
5. Lanzamiento de subagentes; bloqueo por permisos interactivos en modo subagente.

## Entregables tesis/fuentes

- `{out_md}`
- `{out_docx}`
- `{fuente_md}`
- `{FUENTES / '00_REFERENCIAS_CORE_CCA_AAV_2026-06-07.bib'}`

## Pendiente honesto

- Completar descarga oficial del Antigravity IDE x64 hasta 228,699,760 bytes; verificar firma; ejecutar solo si la firma es valida.
- Importar `02_PROMPTS_DE_CODEX.md` y el DOCX consolidado como Google Docs nativos si el conector Drive responde de forma estable.
- Gemini/NotebookLM requieren extraccion por Chrome/perfil autenticado o export manual; no se invento contenido.
- Dedup por contenido debe mover a cuarentena reversible solo con hashes identicos y sin tocar backups.
"""
    report.write_text(report_text, encoding="utf-8")

    status = {
        "ok": True,
        "out_md": str(out_md),
        "out_docx": str(out_docx),
        "report": str(report),
        "docx_bytes": out_docx.stat().st_size,
        "partial_installer_bytes": partial.stat().st_size if partial.exists() else 0,
    }
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
