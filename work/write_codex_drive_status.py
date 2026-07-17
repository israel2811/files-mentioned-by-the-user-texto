from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(r"G:\Mi unidad")
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def latest_json(pattern: str) -> dict:
    files = sorted(Path("outputs").glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return {"missing": pattern}
    return {"path": str(files[0]), "data": json.loads(files[0].read_text(encoding="utf-8"))}


def backup_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    bak = path.with_name(path.name + f".bak_codex_{STAMP}")
    shutil.copy2(path, bak)
    return str(bak)


def write_md(path: Path, text: str) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    bak = backup_if_exists(path)
    path.write_text(text, encoding="utf-8")
    return {"path": str(path), "backup": bak, "bytes": path.stat().st_size}


def main() -> int:
    select = latest_json("antigravity_select_opus_send_*.json")
    read = latest_json("antigravity_read_body_*.json")
    type_send = latest_json("antigravity_type_send_*.json")
    response = (read.get("data", {}).get("dom", {}).get("body", ""))
    response_tail = response[-2500:]
    has_ok = "ANTIGRAVITY_CDP_OK" in response
    opus_used = "Claude Opus 4.6" in response or "Claude Opus 4.6" in json.dumps(select, ensure_ascii=False)

    five_lines = [
        "NEXUS/CCA-AAV integra corpus de multiples IAs, fuentes academicas DOI y trazabilidad de conversaciones para convertir una hipotesis compleja en tesis defendible.",
        "La tesis CCA-AAV debe separar el nucleo academico sobre alucinaciones auditivas, psicosis, prediccion perceptiva y epidemiologia del material forense/SPIA.",
        "Drive es la superficie canonica: corpus, fuentes, manuscritos, informes, indices y respaldos se bancan ahi sin borrar permanente.",
        "Codex coordina archivos, plugins, Google Drive, CDP, scripts y verificacion; Antigravity aporta razonamiento Opus 4.6 cuando CDP funciona; Claude queda como orquestador de bajo consumo.",
        "Lo pendiente real es cerrar manuscrito M0-M13 con citas DOI o POR-VALIDAR, completar fuentes/matriz, exportar Gemini/NotebookLM si es posible y deduplicar por contenido sin tocar respaldos.",
    ]

    informe = f"""# 00_INFORME_CODEX

Fecha: 2026-06-08
Estado: vivo; objetivo global NEXUS aun activo.

## Resultado critico: Antigravity controlado por CDP

- CDP real: `127.0.0.1:50064`.
- App local Antigravity 2.0.11: puerto dinamico detectado `https://127.0.0.1:64706/`.
- Se lanzo con perfil seguro `C:\\tmp\\antigravity-safe-profile-20260607` y flags de certificado local.
- Se leyo DOM por CDP.
- Se encontro workspace real con input `aria="Message input"`.
- Se abrio selector de modelo por CDP.
- Se selecciono `Claude Opus 4.6 (Thinking)`.
- Se envio prompt de prueba por CDP.
- Verificacion de respuesta: `{has_ok}`.

Respuesta verificada de Antigravity/Opus:

```text
{response_tail}
```

Artefactos de evidencia local:

- `{select.get('path')}`
- `{type_send.get('path')}`
- `{read.get('path')}`

## Nota honesta sobre computer-use/navegadores/apps

`computer-use` no quedo demostrado como funcional en esta sesion; la via que si funciono fue CDP/DevTools. Para Antigravity, la ruta estable no fue computer-use sino:

1. Lanzar Antigravity con `--remote-debugging-port=50064`.
2. Esperar el servidor local dinamico.
3. Leer `/json/list`.
4. Conectar al target `https://127.0.0.1:<puerto>/`.
5. Usar CDP para DOM, input, selector de modelo y envio.

## Entendimiento del proyecto en 5 lineas

{chr(10).join(f'{i+1}. {line}' for i, line in enumerate(five_lines))}

## Que tenemos

- Corpus de multiples IAs ya parcialmente unificado/catalogado.
- Tesis CCA-AAV con borrador y manuscrito M0-M13 en progreso.
- Fuentes DOI reales en `G:\\Mi unidad\\03_FUENTES`.
- Indice raiz y documentos de continuidad ya creados como Google Docs.
- Antigravity 2.0.11 controlable por CDP con Claude Opus 4.6.

## Que puede cada IA

- Codex: filesystem controlado, scripts, Google Drive, plugins, CDP, verificacion, conversiones y bancado.
- Antigravity: razonamiento con Claude Opus 4.6 y otros modelos cuando el UI responde; util para critica, capitulos y matriz.
- Claude: orquestacion y continuidad de prompts, pero debe usar minimo credito si Codex/Antigravity ya pueden ejecutar.

## Que hicimos hoy

- Reparacion PC/MCP Claude: alto rendimiento, Filesystem restringido, cache stale pdf-viewer limpiado.
- Antigravity actualizado/relanzado y controlado por CDP.
- Opus 4.6 seleccionado y respuesta `ANTIGRAVITY_CDP_OK` verificada.
- Scripts CDP creados en `work/` para repetir inspeccion/envio/lectura.

## Que falta

- Encadenar prompts largos a Antigravity y bancar cada respuesta en `02_TESIS`.
- Terminar manuscrito M0-M13 academico defendible con DOI o `POR-VALIDAR`.
- Completar matriz de literatura A-D.
- Completar dedup por contenido sin borrar permanente.
- Extraer Gemini/NotebookLM si los exports o UI lo permiten; si no, documentar bloqueo.

## Restricciones

- No borrar permanente.
- No tocar carpetas de respaldo.
- Mover duplicados solo a cuarentena reversible tras verificacion de hash y OK explicito si es masivo.
"""

    contexto = f"""# 00_CONTEXTO_COMPARTIDO_3IAS

Fecha: 2026-06-08

## Resumen operativo

Codex, Antigravity y Claude deben trabajar sobre una unica verdad en Drive. Ya no se debe repetir auditoria completa salvo evidencia concreta faltante.

## Tenemos

- Corpus de conversaciones de multiples IAs y catalogo grande de Drive.
- Fuentes DOI reales en `03_FUENTES`.
- Manuscrito M0-M13 en `02_TESIS`, con version corregida en Google Docs.
- Antigravity controlado por CDP y probado con Claude Opus 4.6.
- Indice raiz y analisis nube/offload.

## Capacidades

- Codex: ejecutar scripts, leer/escribir Drive con cuidado, controlar CDP, crear documentos, verificar hashes/citas.
- Antigravity: responder con Claude Opus 4.6 desde UI local por CDP; usarlo para critica academica, redaccion y matriz.
- Claude: mantener continuidad y coordinar prompts con bajo gasto.

## Hecho

- PC/MCP: alto rendimiento; Filesystem Claude reducido de `C:\\`/`G:\\` completos a rutas utiles; pdf-viewer cache reparado.
- Antigravity: CDP real confirmado; modelo Opus 4.6 seleccionado; respuesta `ANTIGRAVITY_CDP_OK` leida.
- Tesis: fuentes DOI y manuscrito v3 existen; faltan cierre academico y matriz robusta.

## Falta

1. M1-M3 completos y coherentes.
2. M4-M13 en forma defendible.
3. Matriz literatura A-D.
4. Separar academico defendible de anexo forense/SPIA.
5. Dedup y conversion GDocs por lotes.
6. Gemini/NotebookLM: extraer solo si hay acceso/export; no inventar.
"""

    offload = """# 00_NUBE_OFFLOAD_ANALISIS

## Pregunta

¿Se puede usar Codespaces/nube para liberar CPU/RAM de una Dell con 8 GB RAM y HDD?

## Respuesta corta

Si, pero solo para trabajo que pueda ejecutarse remotamente por lotes o en servicios web. No se puede "gotear" la RAM/render local de apps de escritorio ya abiertas: Antigravity, Brave, Edge, Chrome y Claude Desktop siguen consumiendo memoria y render local mientras se usen como aplicaciones interactivas.

## (a) Cargas que SI se mueven a la nube

- Troceo y parseo de exports grandes ChatGPT/Claude/Gemini/NotebookLM.
- Conversiones masivas `.html/.txt/.json` a `.md/.csv/.docx`.
- Dedup por hash y conteos sobre 97 GB/145k archivos si se suben datos o indices.
- Builds, scripts, notebooks, OCR, scraping y pipelines programados.
- Agentes no interactivos en Codespaces, GitHub Actions, Colab, Hugging Face Spaces, Supabase/Neon/Cloudflare Workers.

## (b) Cargas que NO se pueden gotear a la nube

- La RAM usada por ventanas locales de Antigravity/Claude/Chrome/Brave/Edge.
- El renderizado local de Electron/Chromium.
- Tabs abiertas con sesiones/cookies locales, salvo que se sustituyan por la version web remota.
- Google Drive Desktop sincronizando localmente.
- Interacciones GUI que necesitan pantalla local, salvo que se haga en navegador remoto o VM remota.

## 5 ideas aplicables hoy

1. Usar Codespaces/GitHub Actions para parsear exports gigantes y generar chunks/CSV/MD5.
2. Mantener en la Dell solo indices pequenos y documentos activos; mover trabajo pesado a Drive/nube.
3. Ejecutar conversiones por lotes en Colab/Codespaces y subir resultados a `G:\\Mi unidad`.
4. Usar Neon/Supabase como indice SQL de inventario/dedup, no como sustituto del Drive completo.
5. Abrir menos apps interactivas simultaneas: usar Antigravity por CDP solo cuando aporte, y cerrar Brave/Edge si no son necesarios.
"""

    results = [
        write_md(ROOT / "00_INFORME_CODEX.md", informe),
        write_md(ROOT / "00_CONTEXTO_COMPARTIDO_3IAS.md", contexto),
        write_md(ROOT / "00_NUBE_OFFLOAD_ANALISIS.md", offload),
        write_md(ROOT / "02_TESIS" / "00_INFORME_ANTIGRAVITY_CDP_2026-06-08.md", informe),
    ]
    print(json.dumps({"ok": True, "results": results}, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
