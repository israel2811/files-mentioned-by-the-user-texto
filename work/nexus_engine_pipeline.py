import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Import components
from nexus_knowledge_extractor import run_extraction
from nexus_duckdb_corpus import init_duckdb_corpus
from nexus_ai_evaluator_comparator import evaluate_response, recommend_best_ai
from nexus_prompt_evolution_engine import PromptEvolutionEngine
from nexus_supervisor_loop import SupervisorAgent

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
WORK_DIR = WORKSPACE / "work"
OUTPUT_DIR = WORKSPACE / "outputs"

def run_full_nexus_engine_loop():
    print("==========================================================================")
    print("      EJECUTANDO MOTOR NEXUS DE MEJORA CONTINUA Y MEMORIA EXTERNA        ")
    print("==========================================================================")

    # Paso 1: Ingestión y Extracción de Conocimiento
    print("\n[Paso 1/5] Extracción Multi-Fuente...")
    knowledge_db = run_extraction()

    # Paso 2: Inicialización / Actualización de Base de Conocimiento Viva (DuckDB)
    print("\n[Paso 2/5] Actualización de Memoria DuckDB y Grafo...")
    init_duckdb_corpus()

    # Paso 3: Evaluación y Enrutamiento Comparativo entre IAs
    print("\n[Paso 3/5] Evaluación Cuantitativa y Matriz de IAs...")
    model_recomm, profile = recommend_best_ai("redaccion de manuscrito y revision mecanistica doi")
    print(f" -> Modelo sugerido para Manuscrito: {model_recomm} ({profile['fortaleza']})")

    # Paso 4: Evolución Automática de Prompts
    print("\n[Paso 4/5] Registro y Evolución del Linaje de Prompts...")
    prompt_engine = PromptEvolutionEngine()
    current_ver = prompt_engine.get_latest_version("nexus_thesis_master_prompt")
    prompt_engine.evolve_prompt(
        prompt_name="nexus_thesis_master_prompt",
        old_text=f"Borrador Tesis Version {current_ver}",
        new_text=f"Manuscrito Tesis Version v{current_ver+1} con Ingesta de Memoria Viva DuckDB y Supervisor Activo",
        rationale="Integración del loop de retroalimentación continua del Motor NEXUS.",
        target_ai=model_recomm
    )

    # Paso 5: Supervisión y Verificación de Coherencia
    print("\n[Paso 5/5] Inspección del Supervisor Autónomo...")
    supervisor = SupervisorAgent()
    target_files = [
        WORK_DIR / "MANUSCRITO_TESIS_CCA_AAV_M0_M17_v4_EXPANSION_MECANISTICA.md",
        OUTPUT_DIR / "TABLAS_EPIDEMIOLOGICAS_CAP_IV_NEXUS.md",
        WORK_DIR / "nexus_duckdb_corpus.py"
    ]
    report_path = supervisor.generate_report(target_files)

    print("\n==========================================================================")
    print(f" ¡CICLO COMPLETO DEL MOTOR NEXUS EJECUTADO Y SINTETIZADO CON ÉXITO! ")
    print(f" Reporte del Supervisor disponible en: {report_path}")
    print("==========================================================================")

if __name__ == "__main__":
    run_full_nexus_engine_loop()
