import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("outputs")
PROMPT_EVOLUTION_FILE = OUTPUT_DIR / "nexus_prompt_lineage.json"

class PromptEvolutionEngine:
    """
    Manages versioning and automated refinement of system & user prompts (v1 -> v52+).
    Tracks version changes, rationale, expected metrics gain, and targeted tasks.
    """

    def __init__(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.lineage = self.load_lineage()

    def load_lineage(self):
        if PROMPT_EVOLUTION_FILE.exists():
            try:
                return json.loads(PROMPT_EVOLUTION_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"versions": []}

    def save_lineage(self):
        PROMPT_EVOLUTION_FILE.write_text(json.dumps(self.lineage, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_latest_version(self, prompt_name):
        matches = [v for v in self.lineage["versions"] if v.get("prompt_name") == prompt_name]
        if not matches:
            return 0
        return max(v.get("version_number", 1) for v in matches)

    def evolve_prompt(self, prompt_name, old_text, new_text, rationale, target_ai="Multi-AI"):
        current_v = self.get_latest_version(prompt_name)
        new_v = current_v + 1
        version_id = f"{prompt_name}_v{new_v}"

        entry = {
            "version_id": version_id,
            "prompt_name": prompt_name,
            "version_number": new_v,
            "timestamp": datetime.now().isoformat(),
            "target_ai": target_ai,
            "old_text": old_text,
            "new_text": new_text,
            "rationale": rationale,
            "expected_improvement": "Incremento de precisión, rigor DOI y prevención de respuestas redundantes."
        }

        self.lineage["versions"].append(entry)
        self.save_lineage()
        print(f"[NEXUS Prompt Engine] Prompt '{prompt_name}' evolucionado a Versión v{new_v} ({version_id})")
        return entry

if __name__ == "__main__":
    engine = PromptEvolutionEngine()
    old_p = "Escribe la tesis doctoral sobre AAV y CCA."
    new_p = "Redacta el manuscrito de tesis CCA-AAV mapeando en cada afirmación científica su DOI explícito, marcando hipótesis no verificadas con [POR-VALIDAR] y segregando datos forenses bajo ISO/IEC 27037."
    engine.evolve_prompt("prompt_tesis_orquestador", old_p, new_p, "Integración de reglas académicas estrictas de AGENTS.md y trazabilidad DOI.")
