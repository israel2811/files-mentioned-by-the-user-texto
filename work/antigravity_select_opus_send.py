from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from antigravity_cdp_probe import RawCDP, http_json


def eval_value(cdp: RawCDP, expr: str):
    resp = cdp.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return resp.get("result", {}).get("result", {}).get("value", resp)


def click(cdp: RawCDP, x: float, y: float) -> None:
    cdp.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    cdp.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    cdp.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def main() -> int:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    page = next(
        t for t in http_json("/json/list")
        if t.get("type") == "page" and t.get("url", "").startswith("https://127.0.0.1:")
    )
    report = {"timestamp": stamp, "target": page}
    cdp = RawCDP(page["webSocketDebuggerUrl"])
    try:
        cdp.send("Runtime.enable")
        cdp.send("Page.enable")
        # Ensure model menu is open.
        model = eval_value(
            cdp,
            r"""
(() => {
  const modelBtn=[...document.querySelectorAll('button')].find(b=>/Select model/.test(b.getAttribute('aria-label')||''));
  const opt=[...document.querySelectorAll('button,[role="option"],[role="menuitem"],[cmdk-item],div')].find(el=>(el.innerText||'').trim()==='Claude Opus 4.6 (Thinking)');
  const rectOf = el => { if(!el) return null; const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; };
  return {modelButton:rectOf(modelBtn), opus:rectOf(opt), body:(document.body.innerText||'').slice(-2500)};
})()
""",
        )
        report["before"] = model
        if not model.get("opus") and model.get("modelButton"):
            r = model["modelButton"]
            click(cdp, r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)
            time.sleep(1)
            model = eval_value(
                cdp,
                r"""
(() => {
  const opt=[...document.querySelectorAll('button,[role="option"],[role="menuitem"],[cmdk-item],div')].find(el=>(el.innerText||'').trim()==='Claude Opus 4.6 (Thinking)');
  const rectOf = el => { if(!el) return null; const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; };
  return {opus:rectOf(opt), body:(document.body.innerText||'').slice(-2500)};
})()
""",
            )
            report["after_open"] = model
        if model.get("opus"):
            r = model["opus"]
            click(cdp, r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)
            report["selected_opus"] = True
            time.sleep(1.5)
        else:
            report["selected_opus"] = False
        send = eval_value(
            cdp,
            r"""
(() => {
  const input=document.querySelector('[aria-label="Message input"], textarea, [role="textbox"], [contenteditable="true"]');
  const btn=document.querySelector('button[data-testid="send-button"]');
  const rectOf = el => { if(!el) return null; const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; };
  return {inputText:(input?.innerText||input?.value||'').slice(0,1000), buttonAria:btn?.getAttribute('aria-label'), buttonDisabled:btn?.disabled||btn?.getAttribute('aria-disabled'), buttonRect:rectOf(btn), body:(document.body.innerText||'').slice(-3000)};
})()
""",
        )
        report["before_send"] = send
        if send.get("buttonRect") and send.get("buttonDisabled") not in (True, "true"):
            r = send["buttonRect"]
            click(cdp, r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)
            report["clicked_send"] = True
        else:
            report["clicked_send"] = False
            cdp.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13})
            cdp.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13})
            report["enter_sent"] = True
        time.sleep(25)
        report["after_send"] = eval_value(
            cdp,
            "(() => ({url:location.href,title:document.title,body:(document.body.innerText||'').slice(-9000)}))()",
        )
    except Exception as exc:
        report["error"] = repr(exc)
    finally:
        cdp.close()
    path = Path("outputs") / f"antigravity_select_opus_send_{stamp}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": "error" not in report, "report_path": str(path), **report}, indent=2, ensure_ascii=True))
    return 0 if "error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
