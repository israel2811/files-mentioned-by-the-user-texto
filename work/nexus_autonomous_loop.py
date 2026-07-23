import os
import sys
import time
from datetime import datetime

# Import layer modules
try:
    from nexus_user_profile import NexusUserProfile
    from nexus_autonomous_agent import NexusAutonomousAgent
    from nexus_periodic_reviewer import NexusPeriodicReviewer
    from nexus_dossier_builder import NexusDossierBuilder
    from nexus_semantic_rag import NexusSemanticRAG
except ImportError as e:
    print(f"Error importing NEXUS modules: {e}")
    print("Asegúrate de ejecutar este script desde el directorio 'work'.")
    sys.exit(1)

OUTPUT_REPORT = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nexus_autonomous_report.md')

def run_nexus_autonomous_loop(duration_sim_seconds=2):
    """
    Orquestador Maestro: "Continúa NEXUS".
    Ejecuta el pipeline completo de las 7 capas de forma autónoma.
    """
    start_time = datetime.now()
    print("="*60)
    print("Iniciando NEXUS Autonomous Research Loop (Modo Profundo)")
    print("="*60)
    
    # 1. Cargar Perfil (Capa 3)
    print("\n[1/6] Cargando Perfil Dinámico del Usuario...")
    profile = NexusUserProfile()
    print(profile.get_profile_summary())
    
    # 2. Inicializar Motor RAG (Capas 1 y 2)
    print("\n[2/6] Inicializando Memoria Total y Grafo (DuckDB + RAG)...")
    rag = NexusSemanticRAG(db_path=os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nexus_academic_corpus.duckdb'))
    # Simular carga
    time.sleep(duration_sim_seconds)
    
    # 3. Autoexploración y Generación de Tareas (Capas 4 y 6)
    print("\n[3/6] Ejecutando Autoexploración (Búsqueda de vacíos y contradicciones)...")
    agent = NexusAutonomousAgent()
    new_tasks = agent.run_exploration_cycle()
    if new_tasks:
        profile.record_auto_task()
    
    # 4. Relectura Periódica (Capa 7)
    print("\n[4/6] Ejecutando Relectura Periódica (Evaluación de documentos históricos)...")
    reviewer = NexusPeriodicReviewer()
    alerts = reviewer.run_review_cycle()
    
    # 5. Generar Expediente / Dossier
    print("\n[5/6] Consolidando hallazgos en el Dossier de Investigación...")
    try:
        builder = NexusDossierBuilder()
        # In a real run, this would compile outputs from RAG. 
        # For the autonomous loop, we pass a dummy query to generate a structure.
        dossier_path = builder.build_dossier(
            query="Auto-generated deep execution cycle",
            retrieved_chunks=[{"source_file": "Autonomous Agent", "content": f"Tareas generadas: {len(new_tasks)}"}]
        )
        print(f"Dossier base actualizado: {dossier_path}")
    except Exception as e:
        print(f"Nota: nexus_dossier_builder no está completamente integrado: {e}")
        
    # 6. Guardar Informe Final Autónomo
    print("\n[6/6] Generando Informe Final Autónomo...")
    report_content = f"""# NEXUS Informe de Ejecución Autónoma
_Generado: {start_time.isoformat()}_

## Resumen de la Ejecución
- **Perfil Activo:** {profile.get_profile_summary()}
- **Nuevas Tareas Generadas (Capa 6):** {len(new_tasks)}
- **Alertas de Relectura (Capa 7):** {len(alerts)}

### Tareas Prioritarias Encontradas
"""
    for t in new_tasks:
        report_content += f"- **[{t['id']}]**: {t['description']}\n"
        
    report_content += "\n### Alertas Históricas\n"
    for a in alerts:
        report_content += f"- {a}\n"
        
    report_content += "\n### Siguiente Acción Recomendada\n"
    if new_tasks:
        report_content += "Delegar las tareas prioritarias a Codex/Claude a través de `NEXUS_ORCHESTRATOR.py`.\n"
    else:
        report_content += "El corpus está completamente validado según los parámetros actuales.\n"

    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    # Finalizar ciclo
    profile.record_cycle()
    
    print("\n" + "="*60)
    print(f"Ciclo Autónomo Completado Exitosamente en {(datetime.now() - start_time).total_seconds():.2f} segundos.")
    print(f"Informe consolidado disponible en: {OUTPUT_REPORT}")
    print("="*60)

if __name__ == "__main__":
    run_nexus_autonomous_loop()
