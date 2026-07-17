from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from antigravity_cdp_probe import RawCDP, http_json


def eval_value(cdp: RawCDP, expr: str):
    resp = cdp.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return resp.get("result", {}).get("result", {}).get("value", resp)


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
        report["dom"] = eval_value(
            cdp,
            r"""
(() => ({
  title: document.title,
  url: location.href,
  readyState: document.readyState,
  body: (document.body.innerText || '').slice(-12000),
  hasWorking: /Working\.\.\./.test(document.body.innerText || ''),
  hasOk: /ANTIGRAVITY_CDP_OK/.test(document.body.innerText || ''),
  errors: [...document.querySelectorAll('*')].map(el=>el.innerText||'').filter(t=>/exhausted|error|failed|quota|capacity|rate/i.test(t)).slice(-20)
}))()
""",
        )
    except Exception as exc:
        report["error"] = repr(exc)
    finally:
        cdp.close()
    path = Path("outputs") / f"antigravity_read_body_{stamp}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": "error" not in report, "report_path": str(path), **report}, indent=2, ensure_ascii=True))
    return 0 if "error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
