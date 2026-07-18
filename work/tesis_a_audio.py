import asyncio
import os
import re
from pathlib import Path

# Need edge-tts installed: pip install edge-tts
# We use a subprocess call to edge-tts to avoid complex asyncio loop issues in some environments.

OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
AUDIO_DIR = OUTPUTS_DIR / "Audioteca_NEXUS"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Select a high-quality Mexican Spanish neural voice
VOICE = "es-MX-JorgeNeural" # or es-MX-DaliaNeural

def clean_markdown(text: str) -> str:
    """Removes markdown formatting to make text speech-friendly."""
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Replace markdown headers with pauses
    text = re.sub(r'#+\s*(.*)', r'\1. ', text)
    # Remove bold/italic markers
    text = re.sub(r'[*_]{1,2}', '', text)
    # Remove markdown links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    # Remove table formatting (keep it simple)
    text = re.sub(r'\|.*\|', '', text)
    return text.strip()

async def generate_audio(text: str, output_path: str):
    import edge_tts
    max_retries = 5
    for attempt in range(max_retries):
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(output_path)
            print(f"[+] Generado: {output_path}")
            return
        except Exception as e:
            print(f"[!] Intento {attempt+1}/{max_retries} fallido: {e}")
            await asyncio.sleep(5 * (attempt + 1))
    print(f"[-] Falla definitiva al generar {output_path}")

async def main():
    print(f"Iniciando generacion de Audioteca NEXUS (Tesis) con voz: {VOICE}")
    
    files = [
        "CAPITULOS_MONOGRAFICOS_I_II_III_CCA.md",
        "CAPITULOS_MONOGRAFICOS_IV_VII_CCA.md",
        "CAPITULOS_MONOGRAFICOS_VIII_X_CCA.md",
        "CAPITULOS_MONOGRAFICOS_XI_XIII_CCA.md"
    ]
    
    for filename in files:
        filepath = OUTPUTS_DIR / filename
        if not filepath.exists():
            print(f"[-] Archivo no encontrado: {filename}")
            continue
            
        print(f"Procesando: {filename}")
        text = filepath.read_text(encoding="utf-8")
        clean_text = clean_markdown(text)
        
        # Split into chunks if too long (edge-tts handles large text well, but just in case)
        out_name = filename.replace(".md", ".mp3")
        out_path = AUDIO_DIR / out_name
        
        try:
            await generate_audio(clean_text, str(out_path))
        except Exception as e:
            print(f"[!] Error generando audio para {filename}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
