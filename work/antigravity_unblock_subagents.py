from __future__ import annotations

import time

from antigravity_answer_permission import key
from antigravity_cdp_probe import RawCDP, http_json


NAMES = [
    "Corpus and inventory researcher",
    "AI coordination researcher",
    "Thesis content researcher",
    "Drive structure researcher",
]


def get_page() -> dict:
    return next(
        t for t in http_json("/json/list")
        if t.get("type") == "page" and t.get("url", "").startswith("https://127.0.0.1:")
    )


def eval_text(cdp: RawCDP, expr: str):
    return cdp.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True}).get("result", {}).get("result", {}).get("value")


def main() -> int:
    page = get_page()
    cdp = RawCDP(page["webSocketDebuggerUrl"])
    cdp.send("Runtime.enable")
    for name in NAMES:
        clicked = eval_text(
            cdp,
            f"""
(() => {{
  const target = {name!r};
  const el = [...document.querySelectorAll('*')]
    .filter(e => (e.innerText || '').includes(target) && (e.innerText || '').includes('Needs Attention'))
    .sort((a,b) => a.getBoundingClientRect().height - b.getBoundingClientRect().height)[0];
  if (!el) return false;
  el.scrollIntoView({{block:'center'}});
  el.click();
  return true;
}})()
""",
        )
        print(f"{name}: clicked={clicked}")
        time.sleep(1.5)
        key(cdp, "3", "Digit3", 51, "3")
        time.sleep(0.2)
        key(cdp, "Enter", "Enter", 13, "\r")
        time.sleep(2)
    body = eval_text(cdp, "(document.body.innerText||'').slice(-2000)")
    print(str(body).encode("ascii", "backslashreplace").decode("ascii"))
    cdp.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
