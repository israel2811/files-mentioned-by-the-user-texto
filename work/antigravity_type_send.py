from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from antigravity_cdp_probe import RawCDP, http_json


PROMPT = (
    "ANTIGRAVITY_CDP_TEST: responde con ANTIGRAVITY_CDP_OK y en una frase "
    "di que paso concreto ayudaria mas a la tesis CCA-AAV ahora."
)


def eval_value(cdp: RawCDP, expr: str):
    resp = cdp.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return resp.get("result", {}).get("result", {}).get("value", resp)


def key(cdp: RawCDP, event_type: str, key_name: str, code: str, vk: int, modifiers: int = 0) -> None:
    cdp.send(
        "Input.dispatchKeyEvent",
        {
            "type": event_type,
            "key": key_name,
            "code": code,
            "windowsVirtualKeyCode": vk,
            "nativeVirtualKeyCode": vk,
            "modifiers": modifiers,
        },
    )


def main() -> int:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    targets = http_json("/json/list")
    page = next(
        t for t in targets
        if t.get("type") == "page"
        and t.get("webSocketDebuggerUrl")
        and t.get("url", "").startswith("https://127.0.0.1:")
    )
    report = {"timestamp": stamp, "target": page, "prompt": PROMPT}
    cdp = RawCDP(page["webSocketDebuggerUrl"])
    try:
        cdp.send("Runtime.enable")
        cdp.send("Page.enable")
        info = eval_value(
            cdp,
            r"""
(() => {
  const el = document.querySelector('[aria-label="Message input"], textarea, [role="textbox"], [contenteditable="true"]');
  if (!el) return {found:false, body:(document.body.innerText||'').slice(0,2000)};
  const r = el.getBoundingClientRect();
  return {found:true, tag:el.tagName, role:el.getAttribute('role'), aria:el.getAttribute('aria-label'),
    text:(el.innerText||el.value||'').slice(0,500), rect:{x:r.x,y:r.y,w:r.width,h:r.height},
    button:[...document.querySelectorAll('button')].map(b=>({testid:b.getAttribute('data-testid'), aria:b.getAttribute('aria-label'), text:(b.innerText||'').trim(), disabled:b.disabled, rect:(()=>{const r=b.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height};})()})).filter(b=>b.testid==='send-button')[0] || null,
    body:(document.body.innerText||'').slice(0,2500)};
})()
""",
        )
        report["before"] = info
        if not info.get("found"):
            raise RuntimeError("message input not found")
        r = info["rect"]
        x = r["x"] + min(30, r["w"] / 2)
        y = r["y"] + r["h"] / 2
        cdp.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        cdp.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        cdp.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})
        time.sleep(0.4)
        key(cdp, "keyDown", "a", "KeyA", 65, modifiers=2)
        key(cdp, "keyUp", "a", "KeyA", 65, modifiers=2)
        key(cdp, "keyDown", "Backspace", "Backspace", 8)
        key(cdp, "keyUp", "Backspace", "Backspace", 8)
        cdp.send("Input.insertText", {"text": PROMPT})
        time.sleep(0.8)
        after_type = eval_value(
            cdp,
            r"""
(() => {
  const input = document.querySelector('[aria-label="Message input"], textarea, [role="textbox"], [contenteditable="true"]');
  const btn = document.querySelector('button[data-testid="send-button"]');
  return {inputText:(input?.innerText||input?.value||'').slice(0,1000),
    buttonAria:btn?.getAttribute('aria-label'), buttonText:(btn?.innerText||'').trim(), buttonDisabled:btn?.disabled || btn?.getAttribute('aria-disabled'),
    body:(document.body.innerText||'').slice(-2500)};
})()
""",
        )
        report["after_type"] = after_type
        btn = info.get("button") or {}
        if after_type.get("buttonDisabled") not in (True, "true"):
            br = btn.get("rect") or {}
            bx = br.get("x", r["x"] + r["w"] - 30) + br.get("w", 28) / 2
            by = br.get("y", r["y"] + r["h"] + 30) + br.get("h", 28) / 2
            cdp.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": bx, "y": by})
            cdp.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": bx, "y": by, "button": "left", "clickCount": 1})
            cdp.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": bx, "y": by, "button": "left", "clickCount": 1})
            report["send_method"] = "send_button_click"
        else:
            key(cdp, "keyDown", "Enter", "Enter", 13)
            key(cdp, "keyUp", "Enter", "Enter", 13)
            report["send_method"] = "enter_key"
        time.sleep(12)
        report["after_send"] = eval_value(
            cdp,
            "(() => ({url:location.href,title:document.title,body:(document.body.innerText||'').slice(-6000)}))()",
        )
    except Exception as exc:
        report["error"] = repr(exc)
    finally:
        cdp.close()
    path = out_dir / f"antigravity_type_send_{stamp}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": "error" not in report, "report_path": str(path), **report}, indent=2, ensure_ascii=True))
    return 0 if "error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
