from __future__ import annotations

import json
import re
import time
from datetime import datetime
from pathlib import Path

from antigravity_cdp_probe import RawCDP, http_json


OUT = Path(r"G:\Mi unidad\02_TESIS")
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


PROMPTS = [
    (
        "P01_entendimiento",
        "Lee o infiere desde el contexto disponible: G:\\Mi unidad\\00_CHECKLIST_MAESTRO_PENDIENTES.md y G:\\Mi unidad\\02_TESIS\\BORRADOR_TESIS_CCA-AAV_v1.md. Resume tu entendimiento del proyecto NEXUS/CCA-AAV en exactamente 5 lineas. Si no puedes leer esos archivos desde Antigravity, dilo explicitamente y trabaja con el contexto visible.",
    ),
    (
        "P02_pregunta_hipotesis",
        "Define en 1 parrafo la pregunta de investigacion y la hipotesis central de la tesis CCA-AAV: Convergencia Cyber-Acustica y Alucinaciones Auditivas Verbales. Debe ser defendible academicamente y separar evidencia medica de hipotesis forense.",
    ),
    (
        "P03_revision_critica",
        "Revisa criticamente el borrador de tesis CCA-AAV y lista sus 5 debilidades mayores y como corregirlas. Marca cualquier afirmacion sin respaldo como POR-VALIDAR.",
    ),
    (
        "P04_M1_introduccion",
        "Redacta el capitulo M1 Introduccion en prosa academica. Usa citas DOI reales cuando las conozcas y marca POR-VALIDAR donde falte verificacion. No inventes DOI.",
    ),
    (
        "P05_M2_mecanismo_diferencial",
        "Redacta el capitulo M2: mecanismo y diferencial medico de alucinaciones auditivas verbales, prediccion perceptiva, psicosis, trauma, sustancias, neurologia y audicion. Cita DOI reales o marca POR-VALIDAR.",
    ),
    (
        "P06_M3_epidemiologia",
        "Redacta el capitulo M3: crono-demografia y epidemiologia de psicosis y alucinaciones auditivas verbales. Cita DOI reales o marca POR-VALIDAR; elimina cifras dudosas si no puedes citarlas.",
    ),
    (
        "P07_matriz_literatura",
        "Construye una matriz de literatura A-D cruzando fuentes DOI por tema: A epidemiologia/prevalencia, B mecanismo neurocognitivo, C diferencial clinico, D tecnologia/forense/SPIA como anexo no central. Incluye DOI cuando los conozcas.",
    ),
    (
        "P08_claims_no_validados",
        "Detecta afirmaciones numericas o tecnicas no validadas tipicas del borrador (por ejemplo 70%, 150ms, prevalencias especificas, causalidades tecnologicas). Para cada una: cita real, POR-VALIDAR o eliminar.",
    ),
    (
        "P09_separacion_academico_forense",
        "Separa el material academico defendible de la tesis CCA-AAV del material forense/SPIA/personal. Propón estructura de cuerpo principal y anexo restringido sin mezclar niveles de evidencia.",
    ),
    (
        "P10_resumen_defensa_roadmap",
        "Escribe un resumen ejecutivo, esquema de defensa oral y roadmap de siguientes pasos para terminar la tesis CCA-AAV. Prioriza tareas verificables con DOI y entregables en Drive.",
    ),
]


def eval_value(cdp: RawCDP, expr: str):
    resp = cdp.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return resp.get("result", {}).get("result", {}).get("value", resp)


def click(cdp: RawCDP, rect: dict) -> None:
    x = rect["x"] + rect["w"] / 2
    y = rect["y"] + rect["h"] / 2
    cdp.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    cdp.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    cdp.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def js_fill_prompt(cdp: RawCDP, prompt: str) -> bool:
    return bool(
        eval_value(
            cdp,
            f"""
(() => {{
  const text = {json.dumps(prompt)};
  const input = document.querySelector('[aria-label="Message input"], textarea, [role="textbox"], [contenteditable="true"]');
  if (!input) return false;
  input.focus();
  if (input.isContentEditable) {{
    input.textContent = '';
  }} else {{
    const proto = input.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
    setter ? setter.call(input, '') : (input.value = '');
  }}
  input.dispatchEvent(new InputEvent('input', {{bubbles:true, inputType:'deleteContentBackward', data:null}}));
  input.dispatchEvent(new Event('change', {{bubbles:true}}));
  return true;
}})()
""",
        )
    )


def js_click_send(cdp: RawCDP) -> bool:
    return bool(
        eval_value(
            cdp,
            r"""
(() => {
  const btn = document.querySelector('button[data-testid="send-button"]');
  if (!btn || btn.disabled || btn.getAttribute('aria-disabled') === 'true') return false;
  btn.click();
  return true;
})()
""",
        )
    )


def get_page() -> dict:
    return next(
        t for t in http_json("/json/list")
        if t.get("type") == "page" and t.get("url", "").startswith("https://127.0.0.1:")
    )


def get_state(cdp: RawCDP) -> dict:
    return eval_value(
        cdp,
        r"""
(() => {
  const input=document.querySelector('[aria-label="Message input"], textarea, [role="textbox"], [contenteditable="true"]');
  const btn=document.querySelector('button[data-testid="send-button"]');
  const rectOf=el=>{if(!el)return null; const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height};};
  const body=document.body.innerText||'';
  return {url:location.href,title:document.title,bodyLen:body.length,bodyTail:body.slice(-12000),
    working:/Working\.\.\.|Thinking|Thought for|Working/.test(body.slice(-1000)),
    inputText:(input?.innerText||input?.value||'').slice(0,1000), inputRect:rectOf(input),
    buttonAria:btn?.getAttribute('aria-label'), buttonDisabled:btn?.disabled||btn?.getAttribute('aria-disabled'), buttonRect:rectOf(btn),
    model:([...document.querySelectorAll('button')].find(b=>/Select model/.test(b.getAttribute('aria-label')||''))?.innerText||'').trim()};
})()
""",
    )


def clear_and_type(cdp: RawCDP, prompt: str, state: dict) -> None:
    if not js_fill_prompt(cdp, prompt):
        raise RuntimeError("Antigravity message input was not found")
    cdp.send("Input.insertText", {"text": prompt})
    time.sleep(0.8)


def send_prompt(cdp: RawCDP, label: str, prompt: str) -> dict:
    start = get_state(cdp)
    before_len = start["bodyLen"]
    clear_and_type(cdp, f"[{label}] {prompt}", start)
    typed = get_state(cdp)
    sent = False
    if typed.get("buttonRect") and typed.get("buttonDisabled") not in (True, "true"):
        sent = js_click_send(cdp)
    else:
        sent = js_click_send(cdp)
    if not sent:
        raise RuntimeError(
            f"Antigravity send button was not ready: aria={typed.get('buttonAria')!r}, "
            f"disabled={typed.get('buttonDisabled')!r}, input={typed.get('inputText')[:80]!r}"
        )
    final = None
    for _ in range(18):
        time.sleep(10)
        final = get_state(cdp)
        tail = final.get("bodyTail", "")
        if label in tail and not tail.rstrip().endswith(prompt[-80:]) and "Working..." not in tail[-1200:]:
            break
    return {"label": label, "prompt": prompt, "sent": sent, "before": start, "typed": typed, "final": final, "before_len": before_len}


def save_result(result: dict, index: int) -> Path:
    label = result["label"]
    tail = result.get("final", {}).get("bodyTail", "")
    md = f"""# Antigravity {label}

Fecha: 2026-06-08
Modelo visible: {result.get('final', {}).get('model', 'DESCONOCIDO')}
Enviado por CDP: {result.get('sent')}

## Prompt

{result['prompt']}

## Respuesta / DOM observado

```text
{tail}
```

## Nota

Este archivo fue capturado por Codex via CDP desde Antigravity. Si el texto incluye historial anterior, usar la parte posterior al marcador `{label}` como respuesta mas reciente.
"""
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", label)
    path = OUT / f"ANTIGRAVITY_{index:02d}_{safe}_{STAMP}.md"
    path.write_text(md, encoding="utf-8")
    return path


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    page = get_page()
    cdp = RawCDP(page["webSocketDebuggerUrl"])
    summary = {"timestamp": STAMP, "target": page, "results": []}
    try:
        cdp.send("Runtime.enable")
        cdp.send("Page.enable")
        for i, (label, prompt) in enumerate(PROMPTS, 1):
            safe = re.sub(r"[^A-Za-z0-9_-]+", "_", label)
            existing = sorted(OUT.glob(f"ANTIGRAVITY_{i:02d}_{safe}_*.md"))
            if existing:
                summary["results"].append({"label": label, "path": str(existing[-1]), "sent": False, "skipped_existing": True})
                continue
            result = send_prompt(cdp, label, prompt)
            path = save_result(result, i)
            summary["results"].append({"label": label, "path": str(path), "sent": result.get("sent"), "bodyLen": result.get("final", {}).get("bodyLen")})
    finally:
        cdp.close()
    summary_path = OUT / f"ANTIGRAVITY_10_PROMPTS_SUMMARY_{STAMP}.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": True, "summary_path": str(summary_path), **summary}, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
