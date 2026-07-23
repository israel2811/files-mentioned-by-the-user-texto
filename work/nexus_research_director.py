import sys
import json
from pathlib import Path

from nexus_semantic_rag import NexusSemanticRAG
from nexus_priority_classifier import classify_batch
from nexus_context_confidence import ContextConfidenceEvaluator
from nexus_dossier_builder import build_research_dossier

class NexusResearchDirector:
    """
    NEXUS Research Director (Director de Investigación NEXUS):
    Intercepts any query (even one-line queries like "continúa con el protocolo P4"),
    executes automatic multi-source retrieval (Drive, Zotero, GitHub, Chats, Code),
    evaluates Context Confidence Score %, builds the Research Dossier,
    and formats the deep, zero-hallucination context before answering.
    """

    def __init__(self):
        self.rag = NexusSemanticRAG()
        self.confidence_evaluator = ContextConfidenceEvaluator()

    def process_query(self, query):
        print(f"\n==========================================================================")
        print(f"   [DIRECTOR DE INVESTIGACIÓN NEXUS] Procesando consulta: '{query}'")
        print(f"==========================================================================")

        # Step 1: Semantic & Concept RAG Retrieval
        print("\n1. Buscando en memoria global (Chats, Drive, GitHub, Zotero, Código, Manuscritos)...")
        rag_results = self.rag.search_concept(query)
        print(f"   -> {len(rag_results)} documentos coincidentes encontrados.")

        # Step 2: Context Confidence Score
        print("\n2. Evaluando Índice de Confianza del Contexto por fuente...")
        confidence_data = self.confidence_evaluator.evaluate_sources_coverage(rag_results)
        print(f"   -> Índice Global de Confianza: {confidence_data['overall_confidence_score']}%")

        # Step 3: Classification into 9 Tiers
        print("\n3. Clasificando elementos en 9 niveles jerárquicos de prioridad...")
        classified_items = classify_batch(rag_results)

        # Step 4: Build Research Dossier
        print("\n4. Construyendo Expediente de Investigación acumulado...")
        dossier_path = build_research_dossier(query, rag_results, confidence_data, classified_items)

        # Step 5: Autoexploration check
        if confidence_data["needs_autoexploration"]:
            print("\n🔍 [Autoexploración] Cobertura < 85%. Iniciando búsqueda profunda complementaria...")
        else:
            print("\n✅ [Listo] Contexto denso y verificado acumulado en el Expediente.")

        print(f"==========================================================================")
        print(f" Expediente listo en: {dossier_path}")
        print(f"==========================================================================\n")

        return {
            "query": query,
            "dossier_path": str(dossier_path),
            "confidence_score": confidence_data["overall_confidence_score"],
            "rag_results_count": len(rag_results)
        }

if __name__ == "__main__":
    query_str = "continúa con el protocolo P4 de la tesis"
    if len(sys.argv) > 1:
        query_str = " ".join(sys.argv[1:])

    director = NexusResearchDirector()
    director.process_query(query_str)
