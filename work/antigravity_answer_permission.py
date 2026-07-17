from __future__ import annotations

import time

from antigravity_cdp_probe import RawCDP, http_json


def get_page() -> dict:
    return next(
        t for t in http_json("/json/list")
        if t.get("type") == "page" and t.get("url", "").startswith("https://127.0.0.1:")
    )


def key(cdp: RawCDP, key_name: str, code: str, vk: int, text: str | None = None) -> None:
    down = {"type": "keyDown", "key": key_name, "code": code, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk}
    if text is not None:
        down["text"] = text
        down["unmodifiedText"] = text
    cdp.send("Input.dispatchKeyEvent", down)
    cdp.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": key_name, "code": code, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk})


def main() -> int:
    page = get_page()
    cdp = RawCDP(page["webSocketDebuggerUrl"])
    cdp.send("Runtime.enable")
    cdp.send("Runtime.evaluate", {"expression": "document.body.focus && document.body.focus()", "awaitPromise": True})
    key(cdp, "3", "Digit3", 51, "3")
    time.sleep(0.2)
    key(cdp, "Enter", "Enter", 13, "\r")
    time.sleep(2)
    resp = cdp.send("Runtime.evaluate", {"expression": "(document.body.innerText||'').slice(-2000)", "returnByValue": True})
    print(resp.get("result", {}).get("result", {}).get("value", "").encode("ascii", "backslashreplace").decode("ascii"))
    cdp.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
