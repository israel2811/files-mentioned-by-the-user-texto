import os
import re
from pathlib import Path

WORKSPACE_OUT = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto\outputs\conversaciones_completas")
OUTPUT_FILE = Path(r"C:\Users\Dell\.gemini\antigravity-ide\brain\d12f6ed3-dcff-4940-98a2-8621009a2906\priorities_and_next_steps.md")

def extract():
    results = []
    
    # List all MD files ordered by name (which has the date)
    if not WORKSPACE_OUT.exists():
        print(f"Error: {WORKSPACE_OUT} does not exist.")
        return
        
    md_files = sorted(WORKSPACE_OUT.glob("*.md"))
    
    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        
        # Look for checklists, headings with priorities, tasks, edge-tts, etc.
        lines = content.splitlines()
        file_matches = []
        capture = False
        captured_lines = []
        
        for idx, line in enumerate(lines):
            # Check if we hit a priority/checklist section
            if re.search(r'(###.*Prioridades|###.*Pendientes|##.*Estado Final|##.*Hecho|###.*Grial|###.*Rescate)', line, re.IGNORECASE):
                capture = True
                captured_lines.append(f"\n#### Sección: {line} (de {f.name})\n")
                continue
                
            if capture:
                # If we hit another major section header not related, stop
                if line.startswith("### ") and not re.search(r'(prioridad|pendiente|task|hecho|grial|rescate)', line, re.IGNORECASE):
                    capture = False
                    if captured_lines:
                        file_matches.extend(captured_lines)
                        captured_lines = []
                    continue
                # Also stop if we reach the next message
                if line.startswith("---"):
                    capture = False
                    if captured_lines:
                        file_matches.extend(captured_lines)
                        captured_lines = []
                    continue
                captured_lines.append(line)
        
        # Also capture any markdown task list items anywhere
        task_items = []
        for line in lines:
            if re.match(r'^\s*-\s*\[[ x/]\]', line) or "prioridad" in line.lower() or "pendiente" in line.lower() or "edge-tts" in line.lower() or "g glowing-couscous" in line.lower() or "codespace" in line.lower():
                # Avoid capturing the entire file, just relevant lines
                if len(line) < 200 and not line.startswith("#"):
                    task_items.append(f"* {line.strip()} (de *{f.name}*)")
                    
        if file_matches or task_items:
            results.append(f"### Archivo: [{f.name}](file:///{f.as_posix()})")
            if file_matches:
                results.append("\n".join(file_matches))
            if task_items:
                results.append("\n**Líneas y tareas sueltas detectadas:**\n" + "\n".join(task_items))
            results.append("\n---\n")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(results), encoding="utf-8")
    print(f"Extraction saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract()
