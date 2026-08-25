import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
WORK_DIR = WORKSPACE / "work"
OUTPUT_DIR = WORKSPACE / "outputs"
EXTRACTED_KNOWLEDGE_FILE = OUTPUT_DIR / "nexus_extracted_knowledge.json"

def extract_categories_from_text(text, source_name="unknown"):
    """
    Extracts knowledge items into 7 structured categories using fast linear streaming:
    1. Prompts
    2. Respuestas
    3. Errores / Tracebacks
    4. Decisiones
    5. Código
    6. Ideas / Hipótesis [POR-VALIDAR]
    7. Resultados
    """
    categories = {
        "prompts": [],
        "respuestas": [],
        "errores": [],
        "decisiones": [],
        "codigo": [],
        "ideas_hipotesis": [],
        "resultados": []
    }

    in_code = False
    current_code = []

    for line in text.splitlines():
        trimmed = line.strip()
        if not trimmed:
            continue

        # Code block tracking
        if trimmed.startswith("```"):
            if in_code:
                in_code = False
                if current_code and len(current_code) < 300:
                    code_str = "\n".join(current_code).strip()
                    if len(code_str) > 10:
                        categories["codigo"].append({"source": source_name, "content": code_str[:500]})
                current_code = []
            else:
                in_code = True
            continue

        if in_code:
            if len(current_code) < 100:
                current_code.append(line)
            continue

        # Error tracking
        lower_line = trimmed.lower()
        if any(w in lower_line for w in ["traceback", "failed", "exception", "acceso denegado"]) and len(trimmed) < 200:
            categories["errores"].append({"source": source_name, "content": trimmed})

        # Hypotheses tagged with [POR-VALIDAR]
        if "[por-validar]" in lower_line:
            categories["ideas_hipotesis"].append({"source": source_name, "content": trimmed[:300]})

        # DOIs / Scientific claims
        if "doi:" in lower_line or "10." in lower_line and "doi" in lower_line:
            categories["resultados"].append({"source": source_name, "content": trimmed[:300]})

    return categories

def run_extraction():
    print("[NEXUS Extractor] Iniciando extracción multi-fuente de conocimiento...")
    extracted_db = {
        "timestamp": datetime.now().isoformat(),
        "summary": {},
        "data": {
            "prompts": [],
            "respuestas": [],
            "errores": [],
            "decisiones": [],
            "codigo": [],
            "ideas_hipotesis": [],
            "resultados": []
        }
    }

    # 1. Parse Codex local session logs
    codex_sessions_dir = Path(os.environ.get("USERPROFILE", r"C:\Users\Dell")) / ".codex" / "sessions"
    if codex_sessions_dir.exists():
        for jsonl_path in list(codex_sessions_dir.rglob("*.jsonl"))[:25]:
            try:
                content = jsonl_path.read_text(encoding="utf-8", errors="ignore")
                cats = extract_categories_from_text(content, source_name=f"Codex:{jsonl_path.name}")
                for key in cats:
                    extracted_db["data"][key].extend(cats[key])
            except Exception as e:
                print(f"[!] Error leyendo {jsonl_path}: {e}")

    # 1b. Parse outputs/conversaciones_completas/*.md
    convs_dir = OUTPUT_DIR / "conversaciones_completas"
    if convs_dir.exists():
        for md_file in convs_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                cats = extract_categories_from_text(content, source_name=f"Conversacion:{md_file.name}")
                for key in cats:
                    extracted_db["data"][key].extend(cats[key])
            except Exception as e:
                print(f"[!] Error leyendo {md_file}: {e}")

    # 2. Parse Thesis manuscript and Epidemiology tables
    manuscript_path = WORK_DIR / "MANUSCRITO_TESIS_CCA_AAV_M0_M17_v4_EXPANSION_MECANISTICA.md"
    if manuscript_path.exists():
        text = manuscript_path.read_text(encoding="utf-8", errors="ignore")
        cats = extract_categories_from_text(text, source_name="Manuscrito_v4")
        for key in cats:
            extracted_db["data"][key].extend(cats[key])

    tables_path = OUTPUT_DIR / "TABLAS_EPIDEMIOLOGICAS_CAP_IV_NEXUS.md"
    if tables_path.exists():
        text = tables_path.read_text(encoding="utf-8", errors="ignore")
        cats = extract_categories_from_text(text, source_name="Tablas_Cap_IV")
        for key in cats:
            extracted_db["data"][key].extend(cats[key])

    # Summarize counts
    for k in extracted_db["data"]:
        extracted_db["summary"][k] = len(extracted_db["data"][k])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACTED_KNOWLEDGE_FILE.write_text(json.dumps(extracted_db, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Extracción completada. Resumen: {extracted_db['summary']}")
    print(f"[+] Archivo guardado en {EXTRACTED_KNOWLEDGE_FILE}")
    return extracted_db

if __name__ == "__main__":
    run_extraction()
