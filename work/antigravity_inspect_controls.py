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
    result = cdp.send(
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
  const nodes = [...document.querySelectorAll('button,[role="button"],input,label,textarea,[contenteditable="true"]')];
  return {
    title: document.title,
    url: location.href,
    controls: nodes.map((el, i) => ({
      i,
      tag: el.tagName,
      role: el.getAttribute('role'),
      type: el.getAttribute('type'),
      text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 240),
      aria: el.getAttribute('aria-label'),
      dataTestid: el.getAttribute('data-testid'),
      checked: el.checked,
      disabled: el.disabled || el.getAttribute('aria-disabled'),
      rect: rectOf(el)
    })).filter(x => x.text || x.aria || x.dataTestid)
  };
})()
""",
        },
    )
    value = result["result"]["result"].get("value", {})
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "antigravity_controls_latest.json"
    out_path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(out_path), "count": len(value.get("controls", []))}, ensure_ascii=False, indent=2))
    cdp.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
