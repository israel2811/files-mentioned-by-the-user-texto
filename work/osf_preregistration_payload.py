import json
from pathlib import Path

def generate_osf_payload():
    payload = {
        "data": {
            "type": "draft_registrations",
            "attributes": {
                "registration_metadata": {
                    "Title": {
                        "value": "Convergencia Cyber-Acústica (CCA): Pareidolia Algorítmica por Linear Predictive Coding y Reducción Sensorial"
                    },
                    "Description": {
                        "value": "Estudio preregistrado de los efectos del Comfort Noise Generation (CNG) en la inducción de pareidolia auditiva severa (CCA), evaluando vulnerabilidades previas (neuropatía oculta, bilingüismo) bajo el modelo de Inferencia Activa."
                    },
                    "Hypothesis": {
                        "value": "El CNG simula formantes vocálicos fantasma (LPC artifacts) que el cerebro decodifica erróneamente debido a una divergencia del filtro predictivo. Sujetos con neuropatía oculta y priors lingüísticos fuertes transicionarán a pareidolia bajo <0.5 SNR."
                    },
                    "Design": {
                        "value": "Diseño experimental mixto (intra-sujetos y entre-sujetos) usando la cámara de aislamiento P4 (Faraday/Anecoica)."
                    },
                    "Sample Size": {
                        "value": "128 sujetos (calculado vía statsmodels power analysis, d=0.5, power=0.8)."
                    }
                },
                "registration_schema_id": "prereg_challenge"
            }
        }
    }

    out_path = Path(__file__).parent.parent / "outputs" / "OSF_Preregistration_Payload.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)
        
    print(f"[OK] Payload OSF API generado en: {out_path}")

if __name__ == "__main__":
    generate_osf_payload()
