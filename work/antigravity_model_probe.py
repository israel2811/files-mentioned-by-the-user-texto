from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from antigravity_cdp_probe import RawCDP, http_json


def eval_value(cdp: RawCDP, expr: str):
    resp = cdp.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return resp.get("result", {}).get("result", {}).get("value", resp)


def click_rect(cdp: RawCDP, rect: dict) -> None:
    x = rect["x"] + rect["w"] / 2
    y = rect["y"] + rect["h"] / 2
    cdp.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    cdp.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    cdp.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def main() -> int:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    targets = http_json("/json/list")
    page = next(
        t for t in targets
        if t.get("type") == "page" and t.get("url", "").startswith("https://127.0.0.1:")
    )
    report = {"timestamp": stamp, "target": page}
    cdp = RawCDP(page["webSocketDebuggerUrl"])
    try:
        cdp.send("Runtime.enable")
        cdp.send("Page.enable")
        before = eval_value(
            cdp,
            r"""
(() => {
  const btns=[...document.querySelectorAll('button')].map((b,i)=>({i,testid:b.getAttribute('data-testid'),aria:b.getAttribute('aria-label'),text:(b.innerText||'').trim(),disabled:b.disabled||b.getAttribute('aria-disabled'),rect:(()=>{const r=b.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height};})()}));
  return {buttons:btns.filter(b=>b.testid==='send-button'||/model|Gemini|Claude|Opus/i.test((b.aria||'')+' '+(b.text||''))), body:(document.body.innerText||'').slice(-3000)};
})()
""",
        )
        report["before"] = before
        send_btn = next((b for b in before.get("buttons", []) if b.get("testid") == "send-button"), None)
        if send_btn and "Stop recording" in (send_btn.get("aria") or ""):
            click_rect(cdp, send_btn["rect"])
            report["stopped_recording"] = True
            time.sleep(1)
        model_btn = next(
            (
                b for b in before.get("buttons", [])
                if "Select model" in (b.get("aria") or "") or "Gemini" in (b.get("text") or "")
            ),
            None,
        )
        if model_btn:
            click_rect(cdp, model_btn["rect"])
            time.sleep(2)
        report["after_model_click"] = eval_value(
            cdp,
            r"""
(() => {
  const text=document.body.innerText||'';
  const btns=[...document.querySelectorAll('button,[role="option"],[role="menuitem"],[cmdk-item]')].map((b,i)=>({i,role:b.getAttribute('role'),aria:b.getAttribute('aria-label'),text:(b.innerText||'').trim().slice(0,200),disabled:b.disabled||b.getAttribute('aria-disabled'),rect:(()=>{const r=b.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height};})()})).filter(x=>x.rect.w>0&&x.rect.h>0);
  return {bodyTail:text.slice(-5000), visibleOptions:btns.filter(b=>/Gemini|Claude|Opus|Flash|Pro|High|Low|model/i.test((b.text||'')+' '+(b.aria||''))).slice(0,80)};
})()
""",
        )
    except Exception as exc:
        report["error"] = repr(exc)
    finally:
        cdp.close()
    path = Path("outputs") / f"antigravity_model_probe_{stamp}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": "error" not in report, "report_path": str(path), **report}, indent=2, ensure_ascii=True))
    return 0 if "error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
