import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("outputs")
EVAL_FILE = OUTPUT_DIR / "nexus_ai_evaluations.json"

DEFAULT_BENCHMARK_PROFILES = {
    "Claude": {
        "precision": 9.5,
        "novedad": 8.8,
        "rigor_cientifico": 9.9,
        "codigo_funcional": 8.5,
        "fortaleza": "Explicación mecanística profunda, rigor conceptual y fenomenología de alucinaciones."
    },
    "Codex": {
        "precision": 9.2,
        "novedad": 8.0,
        "rigor_cientifico": 8.5,
        "codigo_funcional": 10.0,
        "fortaleza": "Generación de código robusto, refactorización, automatización CDP y scripts de sistema."
    },
    "Gemini": {
        "precision": 8.9,
        "novedad": 8.5,
        "rigor_cientifico": 8.2,
        "codigo_funcional": 8.0,
        "fortaleza": "Síntesis ejecutiva de grandes volúmenes de datos y digestión de contextos masivos."
    },
    "ChatGPT": {
        "precision": 9.6,
        "novedad": 8.2,
        "rigor_cientifico": 9.0,
        "codigo_funcional": 8.8,
        "fortaleza": "Integración interdisciplinaria, detección de inconsistencias y planificación de alto nivel."
    }
}

def evaluate_response(modelo, tarea, precision, novedad, rigor, codigo_funcional, tiempo_sec=1.0, costo_rel=1.0):
    """
    Evaluates and records performance metrics for a model interaction.
    """
    record = {
        "timestamp": datetime.now().isoformat(),
        "modelo": modelo,
        "tarea": tarea,
        "scores": {
            "precision": precision,
            "novedad": novedad,
            "rigor_cientifico": rigor,
            "codigo_funcional": codigo_funcional,
            "tiempo_segundos": tiempo_sec,
            "costo_relativo": costo_rel
        },
        "score_promedio": round((precision + novedad + rigor + codigo_funcional) / 4.0, 2)
    }

    evals = []
    if EVAL_FILE.exists():
        try:
            evals = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
        except Exception:
            evals = []

    evals.append(record)
    EVAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    EVAL_FILE.write_text(json.dumps(evals, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[NEXUS Evaluador] Evaluada respuesta de '{modelo}' para tarea '{tarea}': Promedio {record['score_promedio']}/10")
    return record

def recommend_best_ai(tipo_tarea):
    """
    Recommends the best AI model according to the task type.
    """
    tipo_tarea = tipo_tarea.lower()
    if "codigo" in tipo_tarea or "script" in tipo_tarea or "cdp" in tipo_tarea or "pip" in tipo_tarea:
        return "Codex", DEFAULT_BENCHMARK_PROFILES["Codex"]
    elif "mecanismo" in tipo_tarea or "doi" in tipo_tarea or "fenomenologia" in tipo_tarea or "redaccion" in tipo_tarea:
        return "Claude", DEFAULT_BENCHMARK_PROFILES["Claude"]
    elif "sintesis" in tipo_tarea or "resumen" in tipo_tarea or "lote" in tipo_tarea:
        return "Gemini", DEFAULT_BENCHMARK_PROFILES["Gemini"]
    else:
        return "ChatGPT", DEFAULT_BENCHMARK_PROFILES["ChatGPT"]

if __name__ == "__main__":
    # Test evaluation
    evaluate_response("Claude", "Redacción Módulo M6 Tesis", 9.6, 8.5, 9.9, 8.0)
    evaluate_response("Codex", "Script Extractor de Conocimiento", 9.5, 8.0, 8.5, 10.0)
    model, profile = recommend_best_ai("desarrollo de código python")
    print(f"[NEXUS Enrutador] Modelo recomendado para código: {model} -> {profile['fortaleza']}")
