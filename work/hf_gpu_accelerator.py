# hf_gpu_accelerator.py
# Acelerador Serverless GPU en Hugging Face para procesamiento de texto, embeddings e inferencia

import os
import json
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

MODELS = {
    "instruct": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
    "llama3": "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct",
    "embeddings": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
}

def query_hf_gpu(prompt: str, model_type: str = "instruct", max_tokens: int = 512):
    """
    Envía consultas de inferencia pesada a Hugging Face Serverless GPU.
    """
    url = MODELS.get(model_type, MODELS["instruct"])
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    
    if model_type == "embeddings":
        payload = {"inputs": prompt}
    else:
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7}
        }
        
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return {"status": "success", "result": response.json()}
        else:
            return {"status": "error", "code": response.status_code, "msg": response.text}
    except Exception as e:
        return {"status": "offline_fallback", "msg": str(e)}

if __name__ == "__main__":
    print("Módulo de aceleración por GPU / Hugging Face Serverless activo.")
    res = query_hf_gpu("NEXUS Test Ingesta GPU", model_type="instruct", max_tokens=64)
    print(f"Estado de conexión: {res.get('status')}")
