from __future__ import annotations

import base64
import json
import os
import socket
import struct
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


CDP_PORT = 50064
FALLBACK_APP_PORT = 50071
PROMPT = (
    "Prueba de control CDP desde Codex: responde exactamente con una linea que "
    "empiece por ANTIGRAVITY_CDP_OK y luego di el siguiente paso mas util para "
    "NEXUS/CCA-AAV."
)


def http_json(path: str):
    with urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}{path}", timeout=8) as r:
        return json.loads(r.read().decode("utf-8"))


class RawCDP:
    def __init__(self, ws_url: str):
        self.url = urlparse(ws_url)
        self.sock = socket.create_connection((self.url.hostname, self.url.port), timeout=8)
        self.sock.settimeout(2)
        self._id = 0
        self._connect()

    def _connect(self) -> None:
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        req = (
            f"GET {self.url.path} HTTP/1.1\r\n"
            f"Host: {self.url.hostname}:{self.url.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        ).encode("ascii")
        self.sock.sendall(req)
        header = b""
        deadline = time.time() + 8
        while b"\r\n\r\n" not in header and time.time() < deadline:
            try:
                header += self.sock.recv(4096)
            except socket.timeout:
                continue
        if b" 101 " not in header.split(b"\r\n", 1)[0]:
            raise RuntimeError(header.decode("utf-8", "replace")[:2000])

    def _send_frame(self, text: str) -> None:
        payload = text.encode("utf-8")
        length = len(payload)
        if length < 126:
            header = struct.pack("!BB", 0x81, 0x80 | length)
        elif length < 65536:
            header = struct.pack("!BBH", 0x81, 0x80 | 126, length)
        else:
            header = struct.pack("!BBQI", 0x81, 0x80 | 127, 0, length)[0:10]
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def _recv_exact(self, n: int) -> bytes:
        out = b""
        while len(out) < n:
            try:
                chunk = self.sock.recv(n - len(out))
            except socket.timeout as exc:
                raise TimeoutError("websocket recv timeout") from exc
            if not chunk:
                raise RuntimeError("websocket closed")
            out += chunk
        return out

    def _recv_message(self) -> dict:
        while True:
            b1, b2 = self._recv_exact(2)
            opcode = b1 & 0x0F
            length = b2 & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]
            if b2 & 0x80:
                mask = self._recv_exact(4)
                payload = self._recv_exact(length)
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
            else:
                payload = self._recv_exact(length)
            if opcode == 1:
                return json.loads(payload.decode("utf-8"))
            if opcode == 8:
                raise RuntimeError("websocket close frame")

    def send(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        msg_id = self._id
        self._send_frame(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        deadline = time.time() + 8
        while time.time() < deadline:
            try:
                msg = self._recv_message()
            except TimeoutError:
                continue
            if msg.get("id") == msg_id:
                return msg
        raise TimeoutError(method)

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass


INSPECT_EXPR = r"""
(() => {
  function css(el){
    if(!el) return null;
    if(el.id) return '#' + CSS.escape(el.id);
    const parts=[]; let node=el;
    while(node && node.nodeType===1 && parts.length<5){
      let s=node.tagName.toLowerCase();
      const tid=node.getAttribute('data-testid');
      const aria=node.getAttribute('aria-label');
      const ph=node.getAttribute('placeholder');
      if(tid) s += '[data-testid="'+tid.replace(/"/g,'\\"')+'"]';
      else if(aria) s += '[aria-label="'+aria.replace(/"/g,'\\"')+'"]';
      else if(ph) s += '[placeholder="'+ph.replace(/"/g,'\\"')+'"]';
      else if(node.className && typeof node.className === 'string') {
        s += '.' + node.className.trim().split(/\s+/).slice(0,2).map(c=>CSS.escape(c)).join('.');
      }
      parts.unshift(s); node=node.parentElement;
    }
    return parts.join(' > ');
  }
  const visible = el => {
    const r=el.getBoundingClientRect(); const st=getComputedStyle(el);
    return r.width>0 && r.height>0 && st.visibility!=='hidden' && st.display!=='none';
  };
  const inputs=[...document.querySelectorAll('textarea,input,[contenteditable="true"],[role="textbox"]')]
    .filter(visible)
    .map((el,i)=>({i,tag:el.tagName,type:el.getAttribute('type'),role:el.getAttribute('role'),
      aria:el.getAttribute('aria-label'),placeholder:el.getAttribute('placeholder'),
      disabled:!!el.disabled || el.getAttribute('aria-disabled'), readonly:!!el.readOnly,
      text:(el.innerText || el.value || '').slice(0,300), selector:css(el),
      rect:(()=>{const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height};})()}));
  const buttons=[...document.querySelectorAll('button,[role="button"]')]
    .filter(visible)
    .map((el,i)=>({i,text:(el.innerText||el.getAttribute('aria-label')||el.title||'').trim().slice(0,160),
      aria:el.getAttribute('aria-label'), disabled:!!el.disabled || el.getAttribute('aria-disabled'),
      selector:css(el), rect:(()=>{const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height};})()}))
    .slice(0,120);
  const bodyText=document.body.innerText || '';
  let state='unknown';
  if(/sign in|log in|iniciar sesi[oó]n|acceder|login/i.test(bodyText)) state='login';
  else if(/loading|cargando|please wait|spinner/i.test(bodyText) && bodyText.trim().length<800) state='loading';
  else if(inputs.length || /prompt|chat|agent|workspace|proyecto|nexus/i.test(bodyText)) state='workspace';
  else if(/error|failed|could not|no se pudo/i.test(bodyText)) state='error';
  return {title:document.title,url:location.href,readyState:document.readyState,state,
    bodyLen:bodyText.length,bodyText:bodyText.slice(0,7000),inputs,buttons};
})()
"""


def send_expr(prompt: str) -> str:
    return rf"""
(() => {{
  const prompt = {json.dumps(prompt)};
  const visible = el => {{
    const r=el.getBoundingClientRect(); const st=getComputedStyle(el);
    return r.width>0 && r.height>0 && st.visibility!=='hidden' && st.display!=='none';
  }};
  const candidates=[...document.querySelectorAll('textarea,[contenteditable="true"],[role="textbox"],input:not([type]),input[type="text"],input[type="search"]')]
    .filter(el=>visible(el)&&!el.disabled&&!el.readOnly&&el.getAttribute('aria-disabled')!=='true');
  const input=candidates.sort((a,b)=>b.getBoundingClientRect().y-a.getBoundingClientRect().y)[0];
  if(!input) return {{attempted:false,reason:'no visible editable input'}};
  input.focus();
  if(input.isContentEditable || input.getAttribute('contenteditable')==='true' || input.getAttribute('role')==='textbox') {{
    input.textContent='';
    if(document.execCommand) document.execCommand('insertText', false, prompt);
    if(!((input.innerText||input.textContent||'').includes(prompt))) input.textContent=prompt;
  }} else {{
    const setter = Object.getOwnPropertyDescriptor(input.tagName==='TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype, 'value')?.set;
    if(setter) setter.call(input, prompt); else input.value=prompt;
  }}
  input.dispatchEvent(new InputEvent('input', {{bubbles:true,inputType:'insertText',data:prompt}}));
  input.dispatchEvent(new Event('change', {{bubbles:true}}));
  const btns=[...document.querySelectorAll('button,[role="button"]')]
    .filter(el=>visible(el)&&!el.disabled&&el.getAttribute('aria-disabled')!=='true');
  const inputRect = input.getBoundingClientRect();
  const sendButton = document.querySelector('button[data-testid="send-button"]');
  const nearInput = el => {{
    const r=el.getBoundingClientRect();
    return r.x >= inputRect.x - 10 && r.x <= inputRect.x + inputRect.width + 20 &&
      r.y >= inputRect.y - 20 && r.y <= inputRect.y + 90;
  }};
  const labelMatch=(sendButton && visible(sendButton) && !sendButton.disabled && sendButton.getAttribute('aria-disabled')!=='true')
    ? sendButton
    : btns.find(el=>nearInput(el) && /send|submit|enviar|arrow|generar|start/i.test((el.innerText||el.getAttribute('aria-label')||el.title||'')));
  let clicked=false, clickedLabel=null;
  if(labelMatch) {{
    labelMatch.click();
    clicked=true;
    clickedLabel=(labelMatch.innerText||labelMatch.getAttribute('aria-label')||labelMatch.title||'').trim();
  }}
  const r=input.getBoundingClientRect();
  return {{attempted:true,filled:true,clicked,clickedLabel,inputTag:input.tagName,inputRole:input.getAttribute('role'),
    inputAria:input.getAttribute('aria-label'),inputPlaceholder:input.getAttribute('placeholder'),
    inputRect:{{x:r.x,y:r.y,w:r.width,h:r.height}},
    visibleButtonLabels:btns.map(b=>(b.innerText||b.getAttribute('aria-label')||b.title||'').trim()).filter(Boolean).slice(0,60)}};
}})()
"""


def eval_value(cdp: RawCDP, expr: str):
    resp = cdp.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return resp.get("result", {}).get("result", {}).get("value", resp)


def main() -> int:
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    targets = http_json("/json/list")
    dynamic_port = FALLBACK_APP_PORT
    for target in targets:
        url = target.get("url", "")
        if "127.0.0.1:" in url:
            try:
                dynamic_port = int(url.split("127.0.0.1:", 1)[1].split("/", 1)[0])
                break
            except Exception:
                pass
    if dynamic_port == FALLBACK_APP_PORT:
        main_log = Path(r"C:\tmp\antigravity-safe-profile-20260607\logs\main.log")
        if main_log.exists():
            text = main_log.read_text(encoding="utf-8", errors="replace")
            marker = "Local:       https://127.0.0.1:"
            if marker in text:
                tail = text.rsplit(marker, 1)[1]
                try:
                    dynamic_port = int(tail.split("/", 1)[0])
                except Exception:
                    pass
    page = next(
        (t for t in targets if t.get("type") == "page" and f"127.0.0.1:{dynamic_port}" in t.get("url", "")),
        next((t for t in targets if t.get("type") == "page" and t.get("webSocketDebuggerUrl")), targets[0]),
    )
    report = {
        "timestamp": stamp,
        "cdp_port": CDP_PORT,
        "app_port": dynamic_port,
        "chosen_target": page,
        "prompt": PROMPT,
    }
    cdp = None
    try:
        cdp = RawCDP(page["webSocketDebuggerUrl"])
        cdp.send("Runtime.enable")
        cdp.send("Page.enable")
        cdp.send("Security.enable")
        cdp.send("Security.setIgnoreCertificateErrors", {"ignore": True})
        current = eval_value(cdp, "location.href")
        report["initial_url"] = current
        desired_url = f"https://127.0.0.1:{dynamic_port}/"
        if not isinstance(current, str) or current.startswith("chrome-error://") or f"127.0.0.1:{dynamic_port}" not in current:
            report["navigation"] = cdp.send("Page.navigate", {"url": desired_url})
            time.sleep(4)
        inspected = eval_value(cdp, INSPECT_EXPR)
        report["inspected"] = inspected
        report["state"] = inspected.get("state") if isinstance(inspected, dict) else "unknown"
        send_attempt = {"attempted": False, "reason": "not workspace/login or no input"}
        if isinstance(inspected, dict) and inspected.get("state") in {"workspace", "login"} and inspected.get("inputs"):
            send_attempt = eval_value(cdp, send_expr(PROMPT))
            if isinstance(send_attempt, dict) and send_attempt.get("attempted") and not send_attempt.get("clicked"):
                cdp.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13})
                cdp.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13})
                send_attempt["enterDispatched"] = True
            time.sleep(5)
        report["send_attempt"] = send_attempt
        report["post"] = eval_value(cdp, "(() => ({title:document.title,url:location.href,bodyText:(document.body.innerText||'').slice(0,10000)}))()")
    except Exception as exc:
        report["error"] = repr(exc)
    finally:
        if cdp:
            cdp.close()
    path = out_dir / f"antigravity_cdp_probe_{stamp}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": "error" not in report, "report_path": str(path), **report}, indent=2, ensure_ascii=True))
    return 0 if "error" not in report else 2


if __name__ == "__main__":
    raise SystemExit(main())
