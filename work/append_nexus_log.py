from __future__ import annotations

from datetime import datetime
from pathlib import Path


LOG = Path(r"G:\Mi unidad\00_LOG_DESKTOP.md")


def main() -> None:
    entry = f"""

## ACTUALIZACION CODEX LIVE-AUDIT + EXPORT (2026-06-07)
- Cambio de prioridad solicitado por Israel: antes de seguir GDocs/dedup, revisar estado vivo de Claude Desktop, Claude Code en Claude Desktop, navegadores y prompts recibidos.
- Computer Use: no disponible en esta sesion (`Computer Use native pipe path is unavailable`), por lo que no se pudo observar/clicar Claude Desktop visualmente.
- Chrome extension: respondio y detecto pestana viva `https://claude.ai/recents`; DOM/visible extraction de Claude SPA agoto timeout. Brave/Edge siguen requiriendo Computer Use funcional u otra extension.
- Proceso vivo confirmado: Claude Desktop `Claude_1.11187.4.0` y Claude Code dentro de Claude Desktop `AppData\\Roaming\\Claude\\claude-code\\2.1.165\\claude.exe`.
- Auditoria local creada: `outputs\\NEXUS_LIVE_CLAUDE_CODE_AUDIT.md` y `work\\live_claude_codex_sessions.csv`.
- Hallazgo clave: Drive NO contenia todo el estado vivo. Se encontraron 76 archivos de sesion/estado; 62 relevantes a NEXUS.
- Exportado a Drive sin borrar/mover nada existente:
  - `01_CONVERSACIONES_POR_IA\\ClaudeCode_DesktopLive_20260607`: 19 archivos, 3.12 MB.
  - `01_CONVERSACIONES_POR_IA\\Codex_Sesiones_Live_20260607`: 43 archivos, 7.00 MB.
  - `04_CRUDOS_TROCEADOS\\LIVE_CLAUDE_CODEX_RAW_20260607`: 62 raw JSONL/JSON, 189.24 MB.
- Indice creado: `00_INVENTARIO\\00_INDICE_LIVE_CLAUDE_CODEX_20260607.csv`.
- Mensajes preservados en export live: 1,569 mensajes de usuario + 6,192 mensajes/asistente/eventos conversacionales.
- GDocs manifest actualizado: `00_INVENTARIO\\00_GDOCS_CONVERSION_MANIFEST.csv` con 988 archivos indexados.
- Piloto GDoc nativo exitoso:
  - URL: https://docs.google.com/document/d/1NmLcAXs5tYanVJOkry8KDyGcF2OP25XO7HVjal0WiuM/edit?usp=drivesdk
  - Informe: `00_INVENTARIO\\00_GDOCS_IMPORT_PILOT_20260607.md`.
- Conclusion operativa: la conversion masiva debe usar wrappers TXT/HTML para Markdown; el conector importa a GDocs nativos pero no permite elegir carpeta en `_import_document`, asi que la organizacion posterior requiere move/update_file o Apps Script.
- Seguridad: no hubo borrado, no hubo movimiento de duplicados, no se tocaron credenciales/tokens/cookies/localStorage.
- Timestamp local de registro: {datetime.now().isoformat(timespec='seconds')}.
"""
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(LOG)


if __name__ == "__main__":
    main()
