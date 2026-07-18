import asyncio
import re
from pathlib import Path

OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
AUDIO_DIR = OUTPUTS_DIR / "Audioteca_NEXUS"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
BIB_FILE = Path(__file__).parent / "nexus_core_references.bib"

VOICE = "es-MX-JorgeNeural" # Use Spanish voice as user requested translations or native reading

def parse_bibtex(file_path: Path):
    """Extremely basic bibtex parser for Title and Abstract."""
    if not file_path.exists():
        return []
    
    content = file_path.read_text(encoding="utf-8")
    entries = content.split('@article{')
    
    parsed = []
    for entry in entries[1:]:
        # Extract title
        title_match = re.search(r'title\s*=\s*{(.*?)}', entry, re.DOTALL | re.IGNORECASE)
        # Extract abstract if present
        abstract_match = re.search(r'abstract\s*=\s*{(.*?)}', entry, re.DOTALL | re.IGNORECASE)
        
        if title_match:
            title = title_match.group(1).replace('\n', ' ').strip()
            abstract = abstract_match.group(1).replace('\n', ' ').strip() if abstract_match else "Abstract no disponible localmente."
            parsed.append((title, abstract))
            
    return parsed

async def generate_audio(text: str, output_path: str, voice: str):
    import edge_tts
    max_retries = 5
    for attempt in range(max_retries):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_path))
            print(f"[+] Generado: {output_path}")
            return
        except Exception as e:
            print(f"[!] Intento {attempt+1}/{max_retries} fallido: {e}")
            await asyncio.sleep(5 * (attempt + 1))
    print(f"[-] Falla definitiva al generar {output_path}")

async def main():
    print("Iniciando Audioteca NEXUS - Extraccion de Zotero/BibTeX")
    entries = parse_bibtex(BIB_FILE)
    print(f"Se encontraron {len(entries)} referencias.")
    
    if not entries:
        print("No hay entradas para procesar.")
        return
        
    combined_text = "Audioteca Nexus. Resúmenes de Literatura Científica.\n\n"
    
    for i, (title, abstract) in enumerate(entries, 1):
        # We process it as a single compiled audio to avoid 40 small files
        # Translate or keep as is? Let's keep as is, but read by Spanish voice might sound funny for English.
        # Edge-TTS handles english decently with a Spanish voice, just with an accent. 
        # For a truly premium feel, we could use an English voice for the abstracts. Let's use en-US-ChristopherNeural for the abstracts since the papers are in English.
        combined_text += f"Referencia {i}. Título: {title}.\nResumen: {abstract}\n\n"
        
    out_path = AUDIO_DIR / "NEXUS_Abstracts_Compilados.mp3"
    print(f"Generando compilado de {len(entries)} abstracts...")
    await generate_audio(combined_text, out_path, "en-US-ChristopherNeural")

if __name__ == "__main__":
    asyncio.run(main())
