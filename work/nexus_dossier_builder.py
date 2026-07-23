import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
OUTPUT_DIR = WORKSPACE / "outputs"
DOSSIER_FILE = OUTPUT_DIR / "nexus_research_dossier.md"

def build_research_dossier(query, rag_results, confidence_data, classified_items):
    """
    Constructs the structured 'Expediente de Investigación NEXUS' before answering.
    Includes:
    - Context Confidence Score table
    - Verified facts with DOIs
    - Cross-AI comparisons (Claude vs Codex vs Gemini)
    - Contradictions & open tasks
    - 9-tier priority classification
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = f"# Expediente de Investigación NEXUS\n"
    md += f"**Consulta recibida:** `{query}`  \n"
    md += f"**Fecha de generación:** {now_str}  \n"
    md += f"**Índice de Confianza del Contexto Global:** `{confidence_data['overall_confidence_score']}%`  \n\n"

    md += "---\n\n"
    md += "## 1. Tabla de Índice de Confianza del Contexto por Fuente\n\n"
    md += "| Fuente | Coincidencia (%) | Cobertura | Estado |\n"
    md += "| :--- | ---: | :--- | :--- |\n"

    for src_name, info in confidence_data["sources_table"].items():
        md += f"| {src_name} | {info['confidence']}% | {'Alta' if info['matched'] else 'En exploración'} | {info['status']} |\n"

    md += "\n---\n\n"
    md += "## 2. Documentos e Historial de Trabajo Relacionados (RAG Concept-Match)\n\n"
    for idx, item in enumerate(rag_results[:5], 1):
        md += f"{idx}. **[{item['type']}]** `{item['document']}` (Score: {item['relevance_score']})\n"
        md += f"   - *Coincidencias:* `{', '.join(item['matched_terms'])}`  \n"
        md += f"   - *Snippet:* {item['snippet']}\n\n"

    md += "---\n\n"
    md += "## 3. Matriz de Clasificación Jerárquica por Prioridades (9 Niveles)\n\n"
    for tier, items in classified_items.items():
        if items:
            md += f"### `{tier}` ({len(items)} elementos)\n"
            for it in items[:3]:
                md += f"- **[{it['source']}]**: {it['content']}\n"
            md += "\n"

    md += "---\n\n"
    md += "## 4. Comparación de Aportes entre IAs (Claude vs. Codex vs. Gemini vs. ChatGPT)\n\n"
    md += "- **Claude**: Proporciona el marco conceptual bayesiano, fenomenología clínica/no-clínica (*Waters et al., 2012; Corlett et al., 2019*) y rigor DOI en cada oración.\n"
    md += "- **Codex / Codex Beta**: Ejecuta scripts de sistema, control por CDP, automatización de base de datos DuckDB e ingesta de rollouts.\n"
    md += "- **Gemini**: Sintetiza volúmenes extensos de Google Drive y resúmenes ejecutivos.\n"
    md += "- **ChatGPT**: Mantiene coherencia conceptual interdisciplinaria e integración de prioridades de diseño.\n\n"

    md += "---\n\n"
    md += "## 5. Dictamen del Director de Investigación\n\n"
    if confidence_data["overall_confidence_score"] >= 85.0:
        md += "✅ **Expediente Completo**: El nivel de cobertura supera el 85%. Se autoriza la generación de la respuesta profunda fundamentada en el historial acumulado.\n"
    else:
        md += "🔍 **Autoexploración Requerida**: Cobertura parcial. Se recomienda ejecutar exploración adicional en fuentes Zotero / Google Drive antes de cerrar conclusiones.\n"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOSSIER_FILE.write_text(md, encoding="utf-8")
    print(f"[NEXUS Dossier Builder] Expediente guardado en {DOSSIER_FILE}")
    return DOSSIER_FILE

if __name__ == "__main__":
    dummy_conf = {
        "overall_confidence_score": 94.5,
        "sources_table": {
            "Google Drive": {"confidence": 100, "matched": True, "status": "✅ Listo"},
            "Claude Sessions": {"confidence": 95, "matched": True, "status": "✅ Listo"},
            "Codex Sessions": {"confidence": 91, "matched": True, "status": "✅ Listo"}
        }
    }
    build_research_dossier("continúa con el protocolo P4", [], dummy_conf, {})
