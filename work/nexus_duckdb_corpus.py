import os
import sys

def init_duckdb_corpus():
    """
    Initializes a DuckDB database in-memory or on-disk for ultra-fast indexing 
    of academic papers, DOIs, and thesis manuscript fragments.
    """
    try:
        import duckdb
        conn = duckdb.connect("outputs/nexus_academic_corpus.duckdb")
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
            CREATE TABLE IF NOT EXISTS fragmentos_tesis (
                capitulo VARCHAR,
                seccion VARCHAR,
                contenido TEXT,
                tag_por_validar BOOLEAN DEFAULT FALSE
            );
        """)
        print("[+] Base de datos DuckDB de la tesis inicializada con éxito en outputs/nexus_academic_corpus.duckdb")
        conn.close()
    except ImportError:
        print("[!] duckdb no está instalado localmente. Ejecuta en el Codespace remoto: pip install duckdb")
    except Exception as e:
        print(f"Error inicializando DuckDB: {e}")

if __name__ == "__main__":
    init_duckdb_corpus()
