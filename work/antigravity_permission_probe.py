from __future__ import annotations

import json
from pathlib import Path

from antigravity_cdp_probe import RawCDP, http_json


def get_page() -> dict:
    return next(
        t for t in http_json("/json/list")
        if t.get("type") == "page" and t.get("url", "").startswith("https://127.0.0.1:")
    )


def main() -> int:
    page = get_page()
    cdp = RawCDP(page["webSocketDebuggerUrl"])
    cdp.send("Runtime.enable")
    resp = cdp.send(
        "Runtime.evaluate",
        {
            "returnByValue": True,
            "awaitPromise": True,
            "expression": r"""
(() => {
  const rectOf = el => {
    const r = el.getBoundingClientRect();
    return {x:r.x, y:r.y, w:r.width, h:r.height};
  };
  const match = /allow|access|path|submit|skip|yes|no/i;
  const all = [...document.querySelectorAll('*')];
  const hits = all.map((el, i) => ({
    i,
    tag: el.tagName,
    role: el.getAttribute('role'),
    cls: String(el.className || '').slice(0, 200),
    aria: el.getAttribute('aria-label'),
    title: el.getAttribute('title'),
    text: (el.innerText || el.textContent || '').trim().replace(/\s+/g,' ').slice(0, 500),
    disabled: el.disabled || el.getAttribute('aria-disabled'),
    rect: rectOf(el)
  })).filter(x => match.test([x.text,x.aria,x.title,x.role,x.cls].join(' ')) && x.rect.w > 0 && x.rect.h > 0);
  return {bodyTail:(document.body.innerText||'').slice(-3000), hits};
})()
""",
        },
    )
    value = resp["result"]["result"].get("value", {})
    out = Path("outputs") / "antigravity_permission_probe_latest.json"
    out.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(out), "hits": len(value.get("hits", [])), "tail": value.get("bodyTail", "")[-800:]}, ensure_ascii=False, indent=2))
    cdp.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
