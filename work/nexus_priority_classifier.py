import re
from pathlib import Path

TIERS = [
    "1_MUY_IMPORTANTE",
    "2_IMPORTANTE",
    "3_RELACIONADO",
    "4_HISTORICO",
    "5_DUPLICADO",
    "6_OBSOLETO",
    "7_CONTRADICTORIO",
    "8_PENDIENTE",
    "9_VALIDADO_DOI"
]

def classify_knowledge_item(item_text, source_name="unknown"):
    """
    Classifies any knowledge fragment into 1 of the 9 hierarchical tiers.
    """
    text_lower = item_text.lower()

    # Rule 9: Validated with DOI
    if "doi:" in text_lower or "https://doi.org/" in text_lower:
        return "9_VALIDADO_DOI"

    # Rule 8: Pending / Open task / [POR-VALIDAR]
    if "[por-validar]" in text_lower or "pendiente" in text_lower or "todo" in text_lower:
        return "8_PENDIENTE"

    # Rule 7: Contradiction / Discrepancy
    if "contradiction" in text_lower or "discrepancia" in text_lower or "conflicto" in text_lower:
        return "7_CONTRADICTORIO"

    # Rule 6: Obsolete / Backup
    if "bak" in text_lower or "obsoleto" in text_lower or "quarantine" in text_lower or "99_" in text_lower:
        return "6_OBSOLETO"

    # Rule 5: Duplicate
    if "duplicado" in text_lower or "copy" in text_lower or "copia" in text_lower:
        return "5_DUPLICADO"

    # Rule 1: Very Important Core (Manuscript, Master thesis, Protocol P4)
    if "manuscrito" in text_lower or "protocolo p4" in text_lower or "tesis" in text_lower or "cca-aav" in text_lower:
        return "1_MUY_IMPORTANTE"

    # Rule 2: Important (Tables, Pipelines, DB)
    if "tabla" in text_lower or "duckdb" in text_lower or "pipeline" in text_lower or "orchestrator" in text_lower:
        return "2_IMPORTANTE"

    # Rule 3: Related (Code, Configs)
    if "script" in text_lower or "python" in text_lower or "json" in text_lower:
        return "3_RELACIONADO"

    # Default Rule 4: Historical
    return "4_HISTORICO"

def classify_batch(items):
    results = {tier: [] for tier in TIERS}
    for item in items:
        text = item.get("content", str(item))
        src = item.get("source", "desconocido")
        tier = classify_knowledge_item(text, src)
        results[tier].append({"source": src, "content": text[:200]})
    return results

if __name__ == "__main__":
    sample = [
        {"source": "M0", "content": "Waters et al., 2012, DOI: 10.1093/schbul/sbs045"},
        {"source": "M14", "content": "Hipótesis CCA de interfaz [POR-VALIDAR]"},
        {"source": "OldScript", "content": "copia de respaldo obsoleto bak"}
    ]
    res = classify_batch(sample)
    print(f"[+] Clasificación en 9 niveles realizada: { {k: len(v) for k, v in res.items() if len(v) > 0} }")
