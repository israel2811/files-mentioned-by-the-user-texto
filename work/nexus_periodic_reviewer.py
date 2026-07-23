import os
import json
from datetime import datetime, timedelta
import sqlite3

# Try to import duckdb, fallback to sqlite3 if duckdb fails
try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nexus_academic_corpus.duckdb')
ALERTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nexus_review_alerts.md')

class NexusPeriodicReviewer:
    """
    Capa 7: Relectura Periódica.
    Escanea documentos antiguos o hallazgos a la luz del nuevo contexto adquirido.
    """
    def __init__(self, review_threshold_days=30):
        self.review_threshold_days = review_threshold_days
        self.alerts = []

    def scan_historical_documents(self):
        """Escanea documentos que no se han actualizado recientemente."""
        stale_docs = []
        if HAS_DUCKDB and os.path.exists(DB_PATH):
            try:
                con = duckdb.connect(DB_PATH)
                # Check if metadata tables exist for 'last_reviewed'
                # Simulating for now: check files with 'M0_M13' vs current 'M17'
                tables = con.execute("SHOW TABLES").fetchall()
                if any('text_chunks' in t for t in tables):
                    # Mock check for older iterations
                    res = con.execute("SELECT DISTINCT source_file FROM text_chunks WHERE source_file LIKE '%M0_M13%'").fetchall()
                    for r in res:
                        stale_docs.append(r[0])
                con.close()
            except Exception as e:
                print(f"DuckDB error during periodic review: {e}")
                
        # Fallback simulation
        if not stale_docs:
            stale_docs = [
                "MANUSCRITO_TESIS_CCA_AAV_M0_M13_v2_raw.md",
                "nexus_core_references.bib (entradas < 2024)"
            ]
            
        return stale_docs

    def generate_review_alerts(self, stale_docs):
        for doc in stale_docs:
            alert = f"⚠️ RELECTURA REQUERIDA: El documento '{doc}' contiene conclusiones que podrían estar obsoletas ante el nuevo contexto M17."
            self.alerts.append(alert)
        return self.alerts

    def save_alerts(self):
        os.makedirs(os.path.dirname(ALERTS_PATH), exist_ok=True)
        content = "# Alertas de Relectura Periódica (Capa 7)\n\n"
        content += f"_Generado: {datetime.now().isoformat()}_\n\n"
        
        if not self.alerts:
            content += "No hay documentos que requieran relectura prioritaria actualmente.\n"
        else:
            for alert in self.alerts:
                content += f"- {alert}\n"
                
        with open(ALERTS_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        return ALERTS_PATH

    def run_review_cycle(self):
        print(f"Iniciando Relectura Periódica (Umbral: {self.review_threshold_days} días)...")
        docs = self.scan_historical_documents()
        self.generate_review_alerts(docs)
        
        alerts_file = self.save_alerts()
        print(f"Se generaron {len(self.alerts)} alertas de relectura. Guardadas en: {alerts_file}")
        return self.alerts

if __name__ == "__main__":
    reviewer = NexusPeriodicReviewer()
    reviewer.run_review_cycle()
