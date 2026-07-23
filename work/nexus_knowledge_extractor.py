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
    Extracts knowledge items into 7 structured categories:
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

    # Code blocks
    code_blocks = re.findall(r'```(?:[a-zA-Z0-9]+)?\n(.*?)```', text, re.DOTALL)
    for code in code_blocks:
        if len(code.strip()) > 10:
            categories["codigo"].append({"source": source_name, "content": code.strip()})

    # Error / tracebacks
    error_matches = re.findall(r'(?:Error|Exception|Traceback|FAILED|Acceso denegado|FAILED)[^\n]*', text, re.IGNORECASE)
    for err in error_matches:
        categories["errores"].append({"source": source_name, "content": err.strip()})

    # Hypotheses tagged with [POR-VALIDAR]
    hypotheses = re.findall(r'[^\n]*\[POR-VALIDAR\][^\n]*', text)
    for hyp in hypotheses:
        categories["ideas_hipotesis"].append({"source": source_name, "content": hyp.strip()})

    # DOIs / Scientific claims
    doi_claims = re.findall(r'[^\n]*DOI:\s*10\.\d{4,9}/[-._;()/:A-Z0-9]+[^\n]*', text, re.IGNORECASE)
    for claim in doi_claims:
        categories["resultados"].append({"source": source_name, "content": claim.strip()})

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
        for jsonl_path in list(codex_sessions_dir.rglob("*.jsonl"))[:15]:
            try:
                content = jsonl_path.read_text(encoding="utf-8", errors="ignore")
                cats = extract_categories_from_text(content, source_name=f"Codex:{jsonl_path.name}")
                for key in cats:
                    extracted_db["data"][key].extend(cats[key])
            except Exception as e:
                print(f"[!] Error leyendo {jsonl_path}: {e}")

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
