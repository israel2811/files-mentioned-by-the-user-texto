import nbformat as nbf
from pathlib import Path

def generate_notebook():
    nb = nbf.v4.new_notebook()
    
    text_cell_1 = nbf.v4.new_markdown_cell("""# Simulación Computacional de Inferencia Activa (CCA-AAV)
Este notebook fue auto-generado para ejecución en **Google Colab**. 
Contiene el modelo de divergencia del filtro predictivo para la Convergencia Cyber-Acústica.""")
    
    code_cell_1 = nbf.v4.new_code_cell("""import numpy as np
import matplotlib.pyplot as plt

def active_inference_step(mu, prior_mean, sensory_input, pi_p, pi_s, dt=0.1):
    # Free Energy Gradients
    prediction_error_s = sensory_input - mu
    prediction_error_p = mu - prior_mean
    
    dmu_dt = (pi_s * prediction_error_s) - (pi_p * prediction_error_p)
    return mu + dmu_dt * dt

# Simulación de la Cascada de Doble Falla
mu = 0.1 # Creencia inicial
prior = 1.0 # Expectativa (Prior fuerte)
sensory = 0.0 # Input sensorial (Ruido blanco/CNG)
pi_p = 15.0 # Precisión del prior (Alta)
pi_s = 0.5 # Precisión sensorial (Baja, e.g. Neuropatía oculta)

history = []
for _ in range(200):
    mu = active_inference_step(mu, prior, sensory, pi_p, pi_s)
    history.append(mu)

plt.plot(history, label='Evolución de la Creencia ($\mu$)')
plt.axhline(y=1.0, color='r', linestyle='--', label='Alucinación Completa')
plt.title('Divergencia Hacia la Pareidolia')
plt.legend()
plt.show()
""")

    nb['cells'] = [text_cell_1, code_cell_1]
    
    out_path = Path(__file__).parent.parent / "outputs" / "Active_Inference_Colab.ipynb"
    with open(out_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
        
    print(f"[OK] Jupyter Notebook (Google Colab) generado en: {out_path}")

if __name__ == "__main__":
    generate_notebook()
