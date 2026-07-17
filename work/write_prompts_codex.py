from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(r"G:\Mi unidad")
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path: Path) -> str | None:
    if not path.exists():
        return None
    bak = path.with_name(path.name + f".bak_codex_{STAMP}")
    shutil.copy2(path, bak)
    return str(bak)


def main() -> int:
    path = ROOT / "02_PROMPTS_DE_CODEX.md"
    text = """# 02_PROMPTS_DE_CODEX

Fecha: 2026-06-08

## Prompt para Claude

Lee `G:\\Mi unidad\\00_INFORME_CODEX.md`, `G:\\Mi unidad\\00_CONTEXTO_COMPARTIDO_3IAS.md`, `G:\\Mi unidad\\00_CHECKLIST_MAESTRO_PENDIENTES.md` y `G:\\Mi unidad\\00_LOG_DESKTOP.md`. Actua como orquestador de bajo consumo: no repitas auditorias ya hechas, no inventes contenido, no borres nada y no toques respaldos. Tu tarea es mantener continuidad, revisar contradicciones, priorizar el cierre de tesis CCA-AAV y coordinar con Codex/Antigravity. Devuelve solo: estado real, bloqueos, siguiente accion de mayor impacto y prompt corto para Antigravity si hace falta.

## Prompt para Codex

Usa Drive como superficie canonica. Verifica evidencia actual antes de afirmar completitud. Mantén `G:\\Mi unidad\\00_INFORME_CODEX.md` actualizado, completa fuentes DOI en `03_FUENTES`, manuscrito M0-M13 en `02_TESIS`, matriz literatura A-D y dedup por contenido sin borrar permanente. Usa CDP para Antigravity cuando aporte; banca cada resultado. Si una plataforma no permite exportar Gemini/NotebookLM, documenta bloqueo honestamente. Optimiza para no colgar la Dell: lotes pequenos, nube/Codespaces para procesos pesados.

## Prompt para Antigravity

Estas coordinado con Codex y Claude en el proyecto NEXUS/CCA-AAV. Lee el contexto bancado en Drive: `00_CONTEXTO_COMPARTIDO_3IAS.md`, `00_INFORME_CODEX.md`, `00_CHECKLIST_MAESTRO_PENDIENTES.md` y `02_TESIS\\BORRADOR_TESIS_CCA-AAV_v1.md` si existen. Tu rol es aportar razonamiento academico con Claude Opus 4.6: critica del manuscrito, pregunta/hipotesis, capitulos M1-M3, matriz de literatura A-D, separacion academico vs forense/SPIA, y roadmap de defensa. Cada afirmacion debe tener DOI o marcarse `POR-VALIDAR`. No pidas aprobacion salvo riesgo de borrado; no borres nada.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    bak = backup(path)
    path.write_text(text, encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(path), "backup": bak, "bytes": path.stat().st_size}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
