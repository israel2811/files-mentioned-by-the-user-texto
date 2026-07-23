import os
import sys
import json
from pathlib import Path

def init_duckdb_corpus():
    """
    NEXUS Cognitive Evolution System (NCES) - Memoria Evolutiva
    Migración a Objetos de Conocimiento (Knowledge Objects), Evolución Reversible, 
    Relaciones Condicionales y Memoria de Incertidumbre.
    """
    db_path = Path("outputs/nexus_academic_corpus.duckdb")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        import duckdb
        conn = duckdb.connect(str(db_path))
        
        # 1. OBJETOS DE CONOCIMIENTO (Sustituye a texto plano)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_objects (
                id VARCHAR PRIMARY KEY,
                concepto_central VARCHAR,
                nivel_evidencia VARCHAR,
                estado VARCHAR, -- [HIPÓTESIS, VALIDADA, DESCARTADA]
                fecha_creacion TIMESTAMP
            );
        """)
        
        # 2. VERSIONES DEL OBJETO (Evolución Reversible - Git para Ideas)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS object_versions (
                version_id VARCHAR PRIMARY KEY,
                object_id VARCHAR,
                contenido TEXT,
                justificacion_cambio TEXT,
                hash_padre VARCHAR,
                timestamp TIMESTAMP
            );
        """)

        # 3. RELACIONES CONDICIONALES (Grafo Epistemológico)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conditional_relationships (
                origen_id VARCHAR,
                destino_id VARCHAR,
                condicion_logica TEXT, -- ej. "Si A > umbral y B disminuye"
                peso_confianza FLOAT,
                evidencia_doi VARCHAR
            );
        """)

        # 4. MEMORIA DE INCERTIDUMBRE (Lo que NO sabemos)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS uncertainty_memory (
                id VARCHAR PRIMARY KEY,
                pregunta_abierta TEXT,
                variables_ocultas_sospechadas TEXT,
                experimento_requerido TEXT,
                estado VARCHAR -- [PENDIENTE, RESUELTO]
            );
        """)

        # Mantenemos las tablas de evaluación y referencias para compatibilidad
        conn.execute("""
            CREATE TABLE IF NOT EXISTS referencias (
                doi VARCHAR PRIMARY KEY,
                titulo VARCHAR,
                autores VARCHAR,
                año INTEGER,
                resumen TEXT,
                verificado BOOLEAN DEFAULT TRUE
            );
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tabla_evaluacion_ias (
                eval_id VARCHAR PRIMARY KEY,
                modelo VARCHAR,
                tarea VARCHAR,
                precision_score FLOAT,
                fecha_evaluacion TIMESTAMP
            );
        """)

        print(f"[+] NCES: Base de datos DuckDB inicializada con Memoria Evolutiva en {db_path}")
        conn.close()
        return True
    except ImportError:
        print("[!] duckdb no instalado. Generando esquema SQL fallback para NCES...")
        sql_schema = """
        -- Esquema SQL NCES (Cognitive Evolution System)
        CREATE TABLE IF NOT EXISTS knowledge_objects (id VARCHAR PRIMARY KEY, concepto_central VARCHAR, nivel_evidencia VARCHAR, estado VARCHAR, fecha_creacion TIMESTAMP);
        CREATE TABLE IF NOT EXISTS object_versions (version_id VARCHAR PRIMARY KEY, object_id VARCHAR, contenido TEXT, justificacion_cambio TEXT, hash_padre VARCHAR, timestamp TIMESTAMP);
        CREATE TABLE IF NOT EXISTS conditional_relationships (origen_id VARCHAR, destino_id VARCHAR, condicion_logica TEXT, peso_confianza FLOAT, evidencia_doi VARCHAR);
        CREATE TABLE IF NOT EXISTS uncertainty_memory (id VARCHAR PRIMARY KEY, pregunta_abierta TEXT, variables_ocultas_sospechadas TEXT, experimento_requerido TEXT, estado VARCHAR);
        """
        Path("outputs/nexus_academic_corpus_schema.sql").write_text(sql_schema, encoding="utf-8")
        print("[+] Esquema NCES guardado en outputs/nexus_academic_corpus_schema.sql")
        return False
    except Exception as e:
        print(f"[!] Error inicializando DuckDB: {e}")
        return False

if __name__ == "__main__":
    init_duckdb_corpus()
