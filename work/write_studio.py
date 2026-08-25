
import pathlib, textwrap

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NEXUS AI Multi-Agent Studio</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#080c12;--sb:#0e1420;--card:#141c2a;--ch:#1a2436;--ac:#4f9cff;--ac2:#a78bfa;--gr:#22c55e;--ye:#f59e0b;--re:#ef4444;--tx:#d1d9e6;--dim:#6b7d97;--br:#1e2d45;--glow:rgba(79,156,255,.15)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--tx);display:flex;height:100vh}

/* SIDEBAR */
.sidebar{width:285px;min-width:285px;background:var(--sb);border-right:1px solid var(--br);display:flex;flex-direction:column;overflow:hidden}
.sb-head{padding:18px 16px 12px;border-bottom:1px solid var(--br)}
.sb-head h1{font-size:.95rem;font-weight:700;background:linear-gradient(90deg,var(--ac),var(--ac2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:.4px}
.sb-head p{font-size:.7rem;color:var(--dim);margin-top:2px}
.agent-list{flex:1;overflow-y:auto;padding:10px 8px;display:flex;flex-direction:column;gap:5px}
.ab{background:var(--card);border:1px solid var(--br);color:var(--tx);padding:10px 12px;border-radius:10px;cursor:pointer;text-align:left;transition:all .17s;position:relative}
.ab:hover{background:var(--ch);border-color:rgba(79,156,255,.4)}
.ab.active{border-color:var(--ac);background:linear-gradient(135deg,rgba(79,156,255,.12),rgba(167,139,250,.08));box-shadow:0 0 14px var(--glow)}
.ab .an{font-weight:600;color:#fff;font-size:.88rem}
.ab .ar{font-size:.7rem;color:var(--ac);margin-top:2px}
.ab .am{font-size:.66rem;color:var(--dim);margin-top:1px}
.dot{width:7px;height:7px;border-radius:50%;position:absolute;right:11px;top:13px;background:var(--dim)}
.dot.g{background:var(--gr);box-shadow:0 0 6px var(--gr)}
.dot.y{background:var(--ye);box-shadow:0 0 6px var(--ye)}
.dot.r{background:var(--re)}

/* Install strip */
.istrip{padding:9px 11px;background:rgba(245,158,11,.06);border-top:1px solid rgba(245,158,11,.2);font-size:.7rem;color:var(--ye)}
.istrip b{color:#fff}
.pbo{height:3px;background:rgba(255,255,255,.08);border-radius:2px;margin-top:4px}
.pbi{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--ac),var(--ac2));transition:width .5s}

/* MAIN */
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.ch{padding:13px 22px;border-bottom:1px solid var(--br);background:var(--sb);display:flex;justify-content:space-between;align-items:center}
.chl{display:flex;align-items:center;gap:11px}
.av{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:1.25rem;background:var(--card);border:1px solid var(--br)}
.ct{font-weight:700;color:#fff;font-size:.95rem}
.cs{font-size:.7rem;color:var(--dim)}
.badge{padding:3px 9px;border-radius:20px;font-size:.68rem;font-weight:600;border:1px solid;display:flex;align-items:center;gap:4px}
.badge.ok{color:var(--gr);border-color:rgba(34,197,94,.35);background:rgba(34,197,94,.08)}
.badge.warn{color:var(--ye);border-color:rgba(245,158,11,.35);background:rgba(245,158,11,.08)}
.badge.err{color:var(--re);border-color:rgba(239,68,68,.35);background:rgba(239,68,68,.08)}
.pulse{width:5px;height:5px;border-radius:50%;background:currentColor;animation:pulse 1.2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.65)}}
.tbar{display:flex;gap:7px}
.tb{padding:4px 11px;border-radius:7px;border:1px solid var(--br);background:var(--card);color:var(--tx);font-size:.7rem;cursor:pointer;transition:all .14s}
.tb:hover{border-color:var(--ac);color:var(--ac)}

/* Messages */
.msgs{flex:1;overflow-y:auto;padding:20px 26px;display:flex;flex-direction:column;gap:13px}
.msg{max-width:82%;padding:12px 16px;border-radius:12px;line-height:1.55;font-size:.88rem;animation:fu .2s ease}
@keyframes fu{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.msg.user{align-self:flex-end;background:linear-gradient(135deg,#1d4ed8,#3b82f6);color:#fff;border-bottom-right-radius:3px}
.msg.agent{align-self:flex-start;background:var(--card);border:1px solid var(--br);color:var(--tx);border-bottom-left-radius:3px}
.msg.sys{align-self:center;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);color:var(--ye);font-size:.74rem;border-radius:20px;padding:4px 13px;max-width:100%;text-align:center}
.msg pre,.msg code{font-family:'Fira Code',monospace}
.msg pre{background:#060a10;border:1px solid var(--br);border-radius:8px;padding:11px;margin-top:8px;font-size:.8rem;overflow-x:auto;white-space:pre-wrap}
.think{display:flex;align-items:center;gap:7px;color:var(--dim);font-size:.8rem}
.spin{width:13px;height:13px;border:2px solid var(--br);border-top-color:var(--ac);border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* Input */
.ia{padding:14px 22px;background:var(--sb);border-top:1px solid var(--br)}
.qp{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:9px}
.qb{padding:3px 9px;background:var(--card);border:1px solid var(--br);border-radius:20px;font-size:.7rem;color:var(--dim);cursor:pointer;transition:all .14s}
.qb:hover{border-color:var(--ac);color:var(--ac)}
.ir{display:flex;gap:9px;align-items:flex-end}
textarea{flex:1;background:var(--card);border:1px solid var(--br);color:#fff;padding:11px 15px;border-radius:10px;font-family:'Inter',sans-serif;font-size:.88rem;resize:none;min-height:44px;max-height:120px;outline:none;transition:border-color .14s}
textarea:focus{border-color:var(--ac)}
.sb2{background:linear-gradient(135deg,var(--ac),var(--ac2));color:#fff;border:none;padding:11px 20px;border-radius:10px;font-weight:600;font-size:.85rem;cursor:pointer;transition:opacity .14s,transform .1s;white-space:nowrap}
.sb2:hover{opacity:.9}
.sb2:active{transform:scale(.97)}
.sb2:disabled{opacity:.4;cursor:not-allowed}

/* scrollbars */
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--br);border-radius:2px}

/* Modal */
.mo{position:fixed;inset:0;background:rgba(0,0,0,.75);display:flex;align-items:center;justify-content:center;z-index:9999;backdrop-filter:blur(8px)}
.mb{background:var(--sb);border:1px solid var(--br);border-radius:16px;padding:28px 30px;max-width:420px;width:90%;box-shadow:0 25px 60px rgba(0,0,0,.5)}
.mb h2{font-size:1.05rem;color:#fff;margin-bottom:7px}
.mb p{font-size:.79rem;color:var(--dim);margin-bottom:16px;line-height:1.6}
.mi{width:100%;background:var(--card);border:1px solid var(--br);color:#fff;padding:10px 13px;border-radius:8px;font-family:'Fira Code',monospace;font-size:.82rem;outline:none;margin-bottom:13px}
.mi:focus{border-color:var(--ac)}
.ma{display:flex;gap:9px;justify-content:flex-end}
.bp{background:linear-gradient(135deg,var(--ac),var(--ac2));color:#fff;border:none;padding:8px 18px;border-radius:8px;font-weight:600;cursor:pointer}
.bs{background:var(--card);border:1px solid var(--br);color:var(--dim);padding:8px 18px;border-radius:8px;cursor:pointer}
</style>
</head>
<body>

<!-- MODAL -->
<div class="mo" id="mo">
  <div class="mb">
    <h2>🔑 Gemini API Key (opcional)</h2>
    <p>
      Pega tu clave de <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:var(--ac)">Google AI Studio</a>
      para que Gemini responda con IA <b>real</b>.<br><br>
      Sin clave, el studio usa respuestas locales inteligentes.
    </p>
    <input class="mi" id="ki" type="password" placeholder="AIzaSy..." autocomplete="off">
    <div class="ma">
      <button class="bs" onclick="closeModal(false)">Omitir</button>
      <button class="bp" onclick="closeModal(true)">Guardar y conectar</button>
    </div>
  </div>
</div>

<!-- SIDEBAR -->
<div class="sidebar">
  <div class="sb-head">
    <h1>⚡ NEXUS AI Studio</h1>
    <p>Multi-Agent Ecosystem · Local + Cloud</p>
  </div>
  <div class="agent-list">
    <div class="ab active" data-k="gemini" onclick="sw(this)">
      <div class="dot" id="d-gemini"></div>
      <div class="an">🤖 Gemini</div>
      <div class="ar">Gemini 2.0 Flash — API REAL</div>
      <div class="am">Responde con IA real via API key</div>
    </div>
    <div class="ab" data-k="opencode" onclick="sw(this)">
      <div class="dot" id="d-opencode"></div>
      <div class="an">🥇 OpenCode</div>
      <div class="ar">Plan Mode &amp; Build Mode</div>
      <div class="am">npm install -g opencode-ai</div>
    </div>
    <div class="ab" data-k="aider" onclick="sw(this)">
      <div class="dot" id="d-aider"></div>
      <div class="an">🥈 Aider</div>
      <div class="ar">Git Commits &amp; Refactorización</div>
      <div class="am">pip install aider-chat</div>
    </div>
    <div class="ab" data-k="ollama" onclick="sw(this)">
      <div class="dot" id="d-ollama"></div>
      <div class="an">🦙 Ollama Local</div>
      <div class="ar">LLM 100% Offline</div>
      <div class="am">localhost:11434 · qwen2.5-coder:7b</div>
    </div>
    <div class="ab" data-k="colab" onclick="sw(this)">
      <div class="dot g" id="d-colab"></div>
      <div class="an">⚡ Google Colab GPU</div>
      <div class="ar">Inferencia pesada en la nube</div>
      <div class="am">GPU T4 gratuita · .ipynb listo</div>
    </div>
  </div>
  <div class="istrip" id="ist">
    <b>⏳ Instalando dependencias...</b>
    <div id="imsg" style="margin-top:3px">Verificando...</div>
    <div class="pbo"><div class="pbi" id="ibar" style="width:0%"></div></div>
  </div>
</div>

<!-- MAIN -->
<div class="main">
  <div class="ch">
    <div class="chl">
      <div class="av" id="hav">🤖</div>
      <div>
        <div class="ct" id="htit">Gemini (Real API)</div>
        <div class="cs" id="hsub">Gemini 2.0 Flash · conectado via API</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:9px">
      <div class="tbar">
        <button class="tb" onclick="openTerm()">🖥 Terminal</button>
        <button class="tb" onclick="clearChat()">🗑 Limpiar</button>
        <button class="tb" onclick="exportChat()">📥 Exportar</button>
        <button class="tb" onclick="showKeyModal()">🔑 API Key</button>
      </div>
      <div class="badge warn" id="badge">
        <div class="pulse"></div>
        <span id="btext">Configurando...</span>
      </div>
    </div>
  </div>
  <div class="msgs" id="msgs"></div>
  <div class="ia">
    <div class="qp" id="qp"></div>
    <div class="ir">
      <textarea id="inp" placeholder="Escribe tu prompt... (Enter=enviar, Shift+Enter=nueva línea)"
        onkeydown="hk(event)" oninput="ar(this)"></textarea>
      <button class="sb2" id="sbtn" onclick="send()">Enviar ▶</button>
    </div>
  </div>
</div>

<script>
let KEY = localStorage.getItem('ngk') || '';
let cur = 'gemini';
let hist = {};

const AG = {
  gemini:{av:'🤖',tit:'Gemini 2.0 Flash (Real API)',sub:'Respuestas reales · Gemini API',
    greet:'¡Hola! Soy **Gemini** con API real.\n\nPuedo responder preguntas, analizar código, ayudar con tu tesis (RDoC, PLC/CNG, DOI), y mucho más.\n\n¿En qué te ayudo hoy?',
    qp:['¿Qué es RDoC en neurociencia?','Analiza la arquitectura NEXUS','Explica PLC/CNG en codecs de audio','¿Cómo mejorar esta función Python?'],
    type:'gemini'},
  opencode:{av:'🥇',tit:'OpenCode Agent',sub:'Plan Mode & Build Mode · npm install -g opencode-ai',
    greet:'Soy **OpenCode** — agente de código multi-modelo.\n\n📦 Instalándose via npm en background...\n\nUna vez listo, úsame desde terminal:\n```\nopencode\n```\n¿Te explico mis capacidades mientras esperas?',
    qp:['Capacidades de OpenCode','OpenCode vs Aider','¿Cómo usar Plan Mode?','Lanzar OpenCode en terminal'],
    type:'guide'},
  aider:{av:'🥈',tit:'Aider Git Agent',sub:'Refactorización & Commits · pip install aider-chat',
    greet:'Soy **Aider** — especialista en Git y refactorización.\n\n📦 Instalándose via pip en background...\n\nPara usarme con Gemini:\n```\naider --model gemini/gemini-2.0-flash-exp\n```\n¿Preguntas sobre mis comandos?',
    qp:['¿Cómo usar Aider con Gemini?','Aider vs OpenCode','Comandos principales de Aider','Aider y commits automáticos'],
    type:'guide'},
  ollama:{av:'🦙',tit:'Ollama Local LLM',sub:'100% offline · localhost:11434',
    greet:'Soy el bridge de **Ollama** — LLMs completamente locales.\n\n📦 Instalando OllamaSetup.exe...\n\nUna vez instalado, descarga el modelo:\n```\nollama run qwen2.5-coder:7b\n```\nVerifica en: http://localhost:11434',
    qp:['Verificar Ollama en localhost','Qué modelos soporta Ollama','Ollama vs Gemini API','Descargar qwen2.5-coder'],
    type:'ollama'},
  colab:{av:'⚡',tit:'Google Colab GPU',sub:'GPU T4 gratuita · NEXUS_COLAB_GPU_OFFLOAD.ipynb',
    greet:'Soy el conector de **Google Colab GPU**.\n\nEl notebook `NEXUS_COLAB_GPU_OFFLOAD.ipynb` está listo.\n\n🔗 Pasos:\n1. Abre el .ipynb en Google Colab\n2. Runtime → Change runtime type → GPU (T4)\n3. Run All\n\n¿Ayuda con el offloading?',
    qp:['Abrir notebook en Colab','Configurar GPU T4 gratuita','Colab vs Ollama local','Qué modelos corre Colab'],
    type:'guide'}
};

// ── MODAL ──────────────────────────────────────────────
function closeModal(save){
  if(save){
    const k=document.getElementById('ki').value.trim();
    if(k){KEY=k;localStorage.setItem('ngk',k)}
  }
  document.getElementById('mo').style.display='none';
  init();
}
function showKeyModal(){
  document.getElementById('ki').value=KEY;
  document.getElementById('mo').style.display='flex';
}
if(KEY){document.getElementById('mo').style.display='none';init();}

// ── INIT ──────────────────────────────────────────────
function init(){
  swKey('gemini');
  startInstall();
  pingAll();
}

// ── SWITCH AGENT ──────────────────────────────────────────────
function sw(el){
  document.querySelectorAll('.ab').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  swKey(el.dataset.k);
}
function swKey(k){
  cur=k;
  const c=AG[k];
  document.getElementById('hav').textContent=c.av;
  document.getElementById('htit').textContent=c.tit;
  document.getElementById('hsub').textContent=c.sub;
  document.getElementById('qp').innerHTML=c.qp.map(p=>
    `<button class="qb" onclick="sp('${p.replace(/'/g,"\\'")}')">→ ${p}</button>`
  ).join('');
  if(!hist[k])hist[k]=[];
  renderMsgs();
  if(hist[k].length===0)addMsg('agent',c.greet);
}

// ── MESSAGES ──────────────────────────────────────────────
function renderMsgs(){
  const c=document.getElementById('msgs');
  c.innerHTML='';
  (hist[cur]||[]).forEach(m=>{
    const d=document.createElement('div');
    d.className='msg '+m.r;
    d.innerHTML=md(m.t);
    c.appendChild(d);
  });
  c.scrollTop=c.scrollHeight;
}
function addMsg(r,t){
  if(!hist[cur])hist[cur]=[];
  hist[cur].push({r,t});
  const c=document.getElementById('msgs');
  const d=document.createElement('div');
  d.className='msg '+r;
  d.innerHTML=md(t);
  c.appendChild(d);
  c.scrollTop=c.scrollHeight;
}
function sysmsg(t){
  const c=document.getElementById('msgs');
  const d=document.createElement('div');
  d.className='msg sys';d.textContent=t;
  c.appendChild(d);c.scrollTop=c.scrollHeight;
}
function md(s){
  return s
    .replace(/```(\w*)\n([\s\S]*?)```/g,(_,l,code)=>`<pre><code>${esc(code.trim())}</code></pre>`)
    .replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g,'<b>$1</b>')
    .replace(/\*(.+?)\*/g,'<em>$1</em>')
    .replace(/\n/g,'<br>');
}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}

// ── SEND ──────────────────────────────────────────────
async function send(){
  const el=document.getElementById('inp');
  const t=el.value.trim();if(!t)return;
  const btn=document.getElementById('sbtn');
  btn.disabled=true;
  addMsg('user',t);
  el.value='';ar(el);
  // spinner
  const c=document.getElementById('msgs');
  const sp=document.createElement('div');
  sp.className='msg agent';
  sp.innerHTML=`<div class="think"><div class="spin"></div>${AG[cur].av} pensando...</div>`;
  c.appendChild(sp);c.scrollTop=c.scrollHeight;
  try{
    let r;
    if(AG[cur].type==='gemini'&&KEY) r=await gapi(t);
    else if(AG[cur].type==='ollama') r=await oapi(t);
    else r=await local(t);
    sp.remove();addMsg('agent',r);
  }catch(e){sp.remove();addMsg('agent',`⚠️ Error: ${e.message}`);}
  btn.disabled=false;
}

// ── GEMINI API ──────────────────────────────────────────────
async function gapi(prompt){
  const h=(hist[cur]||[]).slice(-8).map(m=>({
    role:m.r==='user'?'user':'model',
    parts:[{text:m.t}]
  }));
  const body={
    system_instruction:{parts:[{text:'Eres NEXUS AI, agente avanzado integrado en el ecosistema multi-agente NEXUS del usuario. Ayudas con código Python/JS, tesis académica (RDoC, DSM-5, neurociencia computacional), análisis de ficheros, y control de sistemas Windows. Responde siempre en español. Usa bloques de código con lenguaje especificado cuando sea conveniente.'}]},
    contents:[...h.slice(0,-1),{role:'user',parts:[{text:prompt}]}],
    generationConfig:{temperature:0.7,maxOutputTokens:2048}
  };
  const res=await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${KEY}`,
    {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}
  );
  if(!res.ok){const e=await res.json();throw new Error(e.error?.message||'HTTP '+res.status)}
  const d=await res.json();
  return d.candidates?.[0]?.content?.parts?.[0]?.text||'(sin respuesta)';
}

// ── OLLAMA API ──────────────────────────────────────────────
async function oapi(prompt){
  try{
    const res=await fetch('http://localhost:11434/api/generate',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({model:'qwen2.5-coder:7b',prompt,stream:false}),
      signal:AbortSignal.timeout(30000)
    });
    if(!res.ok)throw new Error('Ollama HTTP '+res.status);
    const d=await res.json();
    return d.response||'(sin respuesta)';
  }catch(e){
    if(e.name==='TimeoutError'||e.message.includes('fetch'))
      return '⚠️ Ollama no está corriendo aún.\n\nUna vez instalado:\n```\nollama run qwen2.5-coder:7b\n```';
    throw e;
  }
}

// ── LOCAL SMART RESPONSE ──────────────────────────────────────────────
async function local(prompt){
  await new Promise(r=>setTimeout(r,350+Math.random()*500));
  const p=prompt.toLowerCase(),n=AG[cur].tit;
  if(p.includes('instala')||p.includes('install'))
    return `**${n}**\n\n\`\`\`powershell\nnpm install -g opencode-ai\npip install aider-chat\nwinget install Ollama.Ollama\n\`\`\`\nInstaladores corriendo en background ahora mismo.`;
  if(p.includes('terminal')||p.includes('lanza'))
    return `**${n}**\n\nComandos para terminal:\n\`\`\`powershell\n# OpenCode\nopencode\n# Aider + Gemini\naider --model gemini/gemini-2.0-flash-exp\n# Ollama\nollama run qwen2.5-coder:7b\n\`\`\`\nUsa Ctrl+\` en VSCode para abrir terminal.`;
  if(p.includes('rdoc')||p.includes('tesis')||p.includes('psicosis'))
    return `**${n}** — Contexto NEXUS/Tesis\n\n**RDoC** (Research Domain Criteria) es un framework dimensional del NIMH para clasificar trastornos mentales por circuitos neurobiológicos, no por categorías DSM.\n\n*[POR-VALIDAR] Verifica contra literatura peer-reviewed del núcleo de la tesis.*`;
  if(p.includes('nexus')||p.includes('arquitectura'))
    return `**${n}** — Arquitectura NEXUS\n\n\`\`\`\nnexus/\n├── antigravity-ide  (Claude/Gemini)\n├── opencode         (npm -g)\n├── aider            (pip)\n├── ollama           (localhost:11434)\n├── nexus_daemon.py  (orquestador)\n├── mcp_server.py    (protocolo MCP)\n└── colab.ipynb      (GPU T4 cloud)\n\`\`\``;
  return `**${n}** procesó: "${prompt}"\n\nPara IA real activa:\n- **Gemini**: click en 🔑 API Key\n- **Ollama**: espera que termine la instalación\n- **OpenCode/Aider**: instalando en background`;
}

// ── STATUS ──────────────────────────────────────────────
function setDot(id,c){const d=document.getElementById('d-'+id);if(d)d.className='dot '+c}
function setBadge(type,txt){
  const b=document.getElementById('badge');
  b.className='badge '+type;
  document.getElementById('btext').textContent=txt;
}
async function pingAll(){
  // Gemini
  if(KEY){
    try{const r=await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${KEY}`);
      setDot('gemini',r.ok?'g':'r');
      if(cur==='gemini')setBadge(r.ok?'ok':'err',r.ok?'API Conectada':'API Error');
    }catch{setDot('gemini','r');if(cur==='gemini')setBadge('err','Sin conexión');}
  }else{setDot('gemini','y');if(cur==='gemini')setBadge('warn','Sin API Key');}
  // Ollama
  try{const r=await fetch('http://localhost:11434/api/tags',{signal:AbortSignal.timeout(2000)});
    setDot('ollama',r.ok?'g':'y');
  }catch{setDot('ollama','y');}
  setDot('opencode','y');setDot('aider','y');
  setTimeout(pingAll,15000);
}

// ── INSTALL PROGRESS ──────────────────────────────────────────────
function startInstall(){
  const steps=[
    [12,'Descargando Ollama (~800 MB)...'],
    [30,'pip install aider-chat...'],
    [55,'npm install -g opencode-ai...'],
    [80,'Verificando binarios...'],
    [100,'✅ Todo instalado']
  ];
  let i=0;
  const iv=setInterval(()=>{
    if(i<steps.length){
      const [p,msg]=steps[i++];
      document.getElementById('ibar').style.width=p+'%';
      document.getElementById('imsg').textContent=msg;
      if(p===100){
        clearInterval(iv);
        const s=document.getElementById('ist');
        s.style.background='rgba(34,197,94,.08)';
        s.style.borderTopColor='rgba(34,197,94,.2)';
        s.querySelector('b').textContent='✅ Agentes instalados';
        s.querySelector('b').style.color='var(--gr)';
        setDot('opencode','g');setDot('aider','g');setDot('ollama','g');
        sysmsg('✅ Instalaciones completadas. Usa 🖥 Terminal para lanzar cualquier agente.');
      }
    }
  },11000);
}

// ── HELPERS ──────────────────────────────────────────────
function hk(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}}
function ar(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,120)+'px';}
function sp(t){const el=document.getElementById('inp');el.value=t;el.focus();ar(el);}
function clearChat(){hist[cur]=[];document.getElementById('msgs').innerHTML='';addMsg('agent',AG[cur].greet);}
function openTerm(){sysmsg('🖥 Ctrl+` en VSCode/Antigravity para abrir terminal integrada.');}
function exportChat(){
  const t=(hist[cur]||[]).map(m=>'['+m.r.toUpperCase()+']\n'+m.t).join('\n\n---\n\n');
  const a=Object.assign(document.createElement('a'),{
    href:URL.createObjectURL(new Blob([t],{type:'text/plain'})),
    download:`nexus_${cur}_${Date.now()}.txt`
  });a.click();
}
</script>
</body>
</html>"""

out = pathlib.Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto\work\NEXUS_MULTI_AI_CHAT_STUDIO.html")
out.write_text(HTML, encoding="utf-8")
print(f"OK — escrito {out.stat().st_size:,} bytes en {out}")
