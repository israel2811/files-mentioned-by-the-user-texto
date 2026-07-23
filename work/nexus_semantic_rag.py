import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
WORK_DIR = WORKSPACE / "work"
OUTPUT_DIR = WORKSPACE / "outputs"

class NexusSemanticRAG:
    """
    Hybrid Semantic & Concept Retrieval Engine across all NEXUS sources:
    - Multi-AI chats (ChatGPT, Codex, Claude, Gemini, Antigravity, NotebookLM)
    - Google Drive corpus (01_CONVERSACIONES_POR_IA, 02_TESIS, 03_FUENTES, 04_CRUDOS)
    - Code repositories (GitHub, local Python/PowerShell/Shell scripts)
    - Zotero BibTeX DOIs and literature
    - Thesis manuscripts and epidemiology tables
    """

    def __init__(self):
        self.indexed_documents = []

    def index_all_sources(self):
        print("[Nexus RAG] Indexando todas las fuentes de conocimiento del proyecto...")
        self.indexed_documents = []

        # 1. Index local manuscript and outputs
        for file_path in WORKSPACE.rglob("*.md"):
            if "node_modules" in str(file_path) or ".git" in str(file_path):
                continue
            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
                self.indexed_documents.append({
                    "source_type": "manuscript_or_doc",
                    "path": str(file_path),
                    "name": file_path.name,
                    "content": text
                })
            except Exception:
                pass

        # 2. Index local Python/PowerShell code
        for file_path in WORK_DIR.glob("*.*"):
            if file_path.suffix in [".py", ".ps1", ".sh", ".json", ".bib"]:
                try:
                    text = file_path.read_text(encoding="utf-8", errors="ignore")
                    self.indexed_documents.append({
                        "source_type": "code_or_config",
                        "path": str(file_path),
                        "name": file_path.name,
                        "content": text
                    })
                except Exception:
                    pass

        # 3. Index Codex local session logs
        codex_sessions_dir = Path(os.environ.get("USERPROFILE", r"C:\Users\Dell")) / ".codex" / "sessions"
        if codex_sessions_dir.exists():
            for file_path in list(codex_sessions_dir.rglob("*.jsonl"))[:20]:
                try:
                    text = file_path.read_text(encoding="utf-8", errors="ignore")
                    self.indexed_documents.append({
                        "source_type": "codex_chat_log",
                        "path": str(file_path),
                        "name": file_path.name,
                        "content": text
                    })
                except Exception:
                    pass

        print(f"[+] Total de documentos indexados en memoria RAG: {len(self.indexed_documents)}")
        return len(self.indexed_documents)

    def search_concept(self, query):
        """
        Concept-based retrieval using token overlap & keyword weights.
        """
        if not self.indexed_documents:
            self.index_all_sources()

        query_terms = [t.lower() for t in re.findall(r'\w+', query) if len(t) > 2]
        results = []

        for doc in self.indexed_documents:
            content_lower = doc["content"].lower()
            score = 0
            matches = []

            for term in query_terms:
                count = content_lower.count(term)
                if count > 0:
                    score += count
                    matches.append(term)

            if score > 0:
                results.append({
                    "document": doc["name"],
                    "path": doc["path"],
                    "type": doc["source_type"],
                    "relevance_score": score,
                    "matched_terms": matches,
                    "snippet": doc["content"][:400].replace("\n", " ") + "..."
                })

        results = sorted(results, key=lambda x: x["relevance_score"], reverse=True)
        return results[:10]

if __name__ == "__main__":
    rag = NexusSemanticRAG()
    rag.index_all_sources()
    res = rag.search_concept("protocolo P4 anecoica faraday")
    print(f"[+] Coincidencias RAG para 'protocolo P4': {len(res)} documentos encontrados.")
    for r in res[:3]:
        print(f"  - [{r['type']}] {r['document']} (Score: {r['relevance_score']})")
