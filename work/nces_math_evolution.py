import os
import json
from datetime import datetime

class NCESMathEvolutionEngine:
    """
    Motor Matemático (Evolución de Fórmulas) - Nivel NCES.
    En lugar de solo ajustar parámetros, este motor propone cambios estructurales
    a las hipótesis (ej. pasar de un modelo aditivo a uno multiplicativo o condicional).
    """
    
    def __init__(self):
        self.formulas_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nces_formula_evolution.json')
        self.formulas = self.load_formulas()

    def load_formulas(self):
        if os.path.exists(self.formulas_path):
            try:
                with open(self.formulas_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
                
        # Fórmula inicial de la Hipótesis CCA
        return {
            "CCA_Hypothesis": {
                "current_structure": "AAV_Prob = Vulnerabilidad_Endogena + Ruido_Subumbral",
                "variables_known": ["Vulnerabilidad_Endogena", "Ruido_Subumbral"],
                "evolution_history": [
                    {
                        "version": "1.0",
                        "structure": "AAV_Prob = Vulnerabilidad_Endogena",
                        "timestamp": "2024-01-01T00:00:00",
                        "justification": "Modelo psiquiátrico clásico"
                    }
                ]
            }
        }

    def propose_structural_change(self, formula_name, new_variable, interaction_type, condition=None):
        """
        Propose a structural mathematical change based on a newly discovered variable.
        interaction_type: 'additive' (+), 'multiplicative' (*), 'conditional' (if/else)
        """
        if formula_name not in self.formulas:
            return None
            
        target = self.formulas[formula_name]
        old_structure = target["current_structure"]
        
        # Guardar la versión anterior en la memoria reversible
        target["evolution_history"].append({
            "version": f"v_pre_{datetime.now().strftime('%Y%m%d%H%M')}",
            "structure": old_structure,
            "timestamp": datetime.now().isoformat(),
            "justification": "Archivado para evolución reversible"
        })
        
        # Evolucionar la estructura
        if interaction_type == "additive":
            new_structure = f"{old_structure} + {new_variable}"
        elif interaction_type == "multiplicative":
            new_structure = f"({old_structure}) * {new_variable}"
        elif interaction_type == "conditional":
            new_structure = f"{old_structure} (SI {condition}) SINO ({old_structure} + {new_variable})"
        else:
            new_structure = old_structure
            
        target["current_structure"] = new_structure
        if new_variable not in target["variables_known"]:
            target["variables_known"].append(new_variable)
            
        self.save_formulas()
        return new_structure

    def save_formulas(self):
        os.makedirs(os.path.dirname(self.formulas_path), exist_ok=True)
        with open(self.formulas_path, 'w', encoding='utf-8') as f:
            json.dump(self.formulas, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    engine = NCESMathEvolutionEngine()
    print("Fórmula Actual:", engine.formulas["CCA_Hypothesis"]["current_structure"])
    
    # Simulación de un descubrimiento
    print("\nDescubrimiento: 'Deaferentacion_Focal' interactúa multiplicativamente.")
    new_form = engine.propose_structural_change(
        "CCA_Hypothesis", 
        "Deaferentacion_Focal", 
        "multiplicative"
    )
    print("Nueva Estructura Propuesta:", new_form)
