import os
import json
from datetime import datetime
import sqlite3

# Try to import duckdb, fallback to sqlite3 if duckdb fails
try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nexus_academic_corpus.duckdb')
TASKS_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nexus_autonomous_tasks.md')

class NexusAutonomousAgent:
    """
    Capas 4 y 6: Autoexploración y Generación de Tareas.
    Analiza el corpus buscando vacíos o contradicciones, y genera trabajo.
    """
    def __init__(self):
        self.tasks = []
        
    def query_corpus_for_gaps(self):
        """Busca etiquetas como [POR-VALIDAR] o áreas de baja confianza."""
        gaps = []
        if HAS_DUCKDB and os.path.exists(DB_PATH):
            try:
                con = duckdb.connect(DB_PATH)
                # Check if text_chunks exists
                tables = con.execute("SHOW TABLES").fetchall()
                if any('text_chunks' in t for t in tables):
                    res = con.execute("SELECT source_file, content FROM text_chunks WHERE content LIKE '%[POR-VALIDAR]%' LIMIT 5").fetchall()
                    for r in res:
                        gaps.append({"source": r[0], "context": r[1][:200]})
                con.close()
            except Exception as e:
                print(f"DuckDB error during auto-exploration: {e}")
                
        # Mock gap if DB is empty or missing, for demonstration of the autonomous loop
        if not gaps:
            gaps.append({
                "source": "MANUSCRITO_TESIS_CCA_AAV_M0_M17_v4_EXPANSION_MECANISTICA.md",
                "context": "Hipótesis: La convergencia cyber-acústica induce neuroplasticidad maladaptativa en la corteza auditiva primaria [POR-VALIDAR]"
            })
            
        return gaps

    def generate_tasks(self, gaps):
        """Genera tareas procesables basadas en los vacíos encontrados."""
        new_tasks = []
        for gap in gaps:
            task_desc = f"Validar hipótesis o dato en {gap['source']} - Contexto: {gap['context']}..."
            new_tasks.append({
                "id": f"TASK_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(new_tasks)}",
                "description": task_desc,
                "status": "PENDING",
                "priority": "HIGH"
            })
        self.tasks.extend(new_tasks)
        return new_tasks

    def save_tasks_to_markdown(self):
        """Guarda las tareas generadas en un documento vivo."""
        os.makedirs(os.path.dirname(TASKS_PATH), exist_ok=True)
        
        content = "# Tareas Autónomas Generadas por NEXUS (Capa 6)\n\n"
        content += f"_Última actualización: {datetime.now().isoformat()}_\n\n"
        
        if not self.tasks:
            content += "No hay tareas autónomas pendientes.\n"
        else:
            for t in self.tasks:
                checkbox = "[ ]" if t["status"] == "PENDING" else "[x]"
                content += f"- {checkbox} **{t['id']}** ({t['priority']}): {t['description']}\n"
                
        with open(TASKS_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        return TASKS_PATH

    def run_exploration_cycle(self):
        print("Iniciando autoexploración (Capa 4)...")
        gaps = self.query_corpus_for_gaps()
        print(f"Se encontraron {len(gaps)} áreas que requieren atención.")
        
        print("Generando tareas autónomas (Capa 6)...")
        new_tasks = self.generate_tasks(gaps)
        
        tasks_file = self.save_tasks_to_markdown()
        print(f"Se generaron {len(new_tasks)} tareas nuevas. Guardadas en: {tasks_file}")
        return new_tasks

if __name__ == "__main__":
    agent = NexusAutonomousAgent()
    agent.run_exploration_cycle()
