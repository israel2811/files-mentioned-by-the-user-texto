# jules_agent_bridge.py
# Integración y Despachador de Tareas para Jules (Google/GitHub Autonomous Software Engineer)
# Permite a NEXUS delegar tareas de codificación, refactorización y resolución de issues a Jules.

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto")
OUTPUT_DIR = WORKSPACE / "outputs"
JULES_TASKS_FILE = OUTPUT_DIR / "jules_dispatched_tasks.json"

class JulesAgentBridge:
    """
    Bridge para interactuar con Jules (Google/GitHub Coding Agent).
    Permite:
    1. Generar directivas de código reproducibles para Jules.
    2. Crear y asignar issues estructurados en GitHub para que Jules los resuelva.
    3. Monitorear ramas creadas por agentes autónomos y preparar validaciones de PRs.
    """
    def __init__(self, repo_slug="israel2811/files-mentioned-by-the-user-texto"):
        self.repo_slug = repo_slug

    def create_jules_directive(self, title: str, description: str, affected_files: list = None, priority: str = "medium") -> dict:
        """
        Estructura una especificación formal de tarea en formato comprensible por Jules.
        """
        directive = {
            "task_id": f"JULES_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "target_repo": self.repo_slug,
            "title": title,
            "priority": priority,
            "affected_files": affected_files or [],
            "instructions": description,
            "status": "QUEUED",
            "academic_rigor_enforced": True
        }
        return directive

    def save_task(self, directive: dict):
        tasks = []
        if JULES_TASKS_FILE.exists():
            try:
                tasks = json.loads(JULES_TASKS_FILE.read_text(encoding="utf-8"))
            except Exception:
                tasks = []
        tasks.append(directive)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        JULES_TASKS_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[Jules Bridge] Tarea {directive['task_id']} registrada en {JULES_TASKS_FILE}")

    def dispatch_to_github_issue(self, directive: dict, dry_run: bool = True):
        """
        Crea un issue etiquetado con 'jules' en el repositorio GitHub vía `gh issue create`.
        """
        body = f"""### Tarea Delegada a Jules (NEXUS Multi-Cloud)

**ID:** `{directive['task_id']}`
**Prioridad:** `{directive['priority']}`
**Archivos Afectados:** {', '.join([f'`{f}`' for f in directive['affected_files']]) if directive['affected_files'] else 'Global'}

#### Descripción e Instrucciones:
{directive['instructions']}

---
*Generado automáticamente por NEXUS Jules Agent Bridge.*
"""
        if dry_run:
            print("[Jules Bridge - Dry Run] Simulación de creación de issue:")
            print(f"Título: {directive['title']}")
            print(f"Cuerpo:\n{body}")
            return {"status": "dry_run_ok", "task_id": directive["task_id"]}
        else:
            try:
                cmd = [
                    "gh", "issue", "create",
                    "-R", self.repo_slug,
                    "--title", f"[Jules] {directive['title']}",
                    "--body", body,
                    "--label", "jules,automated"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"[Jules Bridge] Issue creado exitosamente: {result.stdout.strip()}")
                return {"status": "created", "url": result.stdout.strip()}
            except Exception as e:
                print(f"[Jules Bridge Error] No se pudo crear el issue en GitHub: {e}")
                return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    bridge = JulesAgentBridge()
    task = bridge.create_jules_directive(
        title="Validación de consistencia y linaje en manuscrito M0-M17 v4",
        description="Verificar que todas las menciones a hipótesis CCA lleven la etiqueta [POR-VALIDAR] y que las citas DOIs coincidan con la base de Zotero.",
        affected_files=["work/MANUSCRITO_TESIS_CCA_AAV_M0_M17_v4_EXPANSION_MECANISTICA.md", "work/nexus_core_references.bib"],
        priority="high"
    )
    bridge.save_task(task)
    bridge.dispatch_to_github_issue(task, dry_run=True)
