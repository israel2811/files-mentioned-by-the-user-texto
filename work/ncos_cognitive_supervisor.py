import os
import json
from datetime import datetime

class NCESCognitiveSupervisor:
    """
    NCES Nivel 10 (Evolucionado): Tribunal Científico / Motor Crítico.
    No solo verifica las reglas de preservación, sino que actúa como un adversario.
    Por cada hipótesis que la IA genera, exige automáticamente la refutación.
    """
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.objetivos_path = os.path.join(self.base_dir, '..', 'OBJETIVOS.md')
        self.audit_trail_path = os.path.join(self.base_dir, '..', 'outputs', 'NCES_AUDIT_TRAIL.md')
        
    def load_objetivos(self):
        try:
            with open(self.objetivos_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return "ERROR: OBJETIVOS.md no encontrado. El sistema debe detenerse."

    def validate_knowledge_object(self, proposed_object):
        """
        Evalúa un 'Objeto de Conocimiento' antes de permitir su ingreso a la Memoria Evolutiva (DuckDB).
        """
        print("[Nivel 10 - Adversarial] Evaluando Objeto de Conocimiento...")
        
        rejection_reasons = []
        adversarial_tasks_generated = []
        
        # Evaluar la presencia de refutación
        if proposed_object.get("estado") == "VALIDADA":
            if not proposed_object.get("evidencia_refutatoria_considerada"):
                rejection_reasons.append(
                    "Fallo Crítico: Se intentó marcar un objeto como 'VALIDADA' sin considerar "
                    "formalmente la evidencia refutatoria. Falta el análisis adversario."
                )
                
        # Evaluar evolución estructural (Si hay un cambio, exige historial)
        if proposed_object.get("es_cambio_estructural", False):
            if not proposed_object.get("hash_padre"):
                rejection_reasons.append("Violación de Regla NCES: Evolución no trazable. Falta el hash_padre.")

        # Motor Adversario proactivo: Generar tareas de refutación
        if proposed_object.get("estado") == "HIPÓTESIS":
            adversarial_task = f"Buscar en PubMed evidencia cruzada que REFUTE la hipótesis: '{proposed_object.get('concepto_central')}'"
            adversarial_tasks_generated.append(adversarial_task)
            
        if rejection_reasons:
            self._log_audit("RECHAZADO_OBJETO", rejection_reasons)
            return False, rejection_reasons, adversarial_tasks_generated
        else:
            self._log_audit("APROBADO_OBJETO", ["Objeto epistemológicamente robusto."])
            return True, ["Aprobado para ingreso a DuckDB."], adversarial_tasks_generated

    def _log_audit(self, status, reasons):
        os.makedirs(os.path.dirname(self.audit_trail_path), exist_ok=True)
        timestamp = datetime.now().isoformat()
        
        log_entry = f"\n### Auditoría NCES: {timestamp}\n"
        log_entry += f"- **Estado:** {status}\n"
        log_entry += "- **Razones / Observaciones Adversarias:**\n"
        for r in reasons:
            log_entry += f"  - {r}\n"
            
        with open(self.audit_trail_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

if __name__ == "__main__":
    supervisor = NCESCognitiveSupervisor()
    
    # Simulación 1: Rechazo de IA sobre-confiada
    obj_fallido = {
        "concepto_central": "La AAV es siempre un déficit de copia eferente",
        "estado": "VALIDADA",
        "evidencia_refutatoria_considerada": None
    }
    print("Probando objeto sobre-confiado...")
    aprobado, razones, tareas = supervisor.validate_knowledge_object(obj_fallido)
    print(f"Estado: {aprobado} | Razones: {razones}")
    
    # Simulación 2: Aprobación de Hipótesis y generación de tarea adversaria
    obj_valido = {
        "concepto_central": "La deaferentación focal aumenta la ganancia cortical independientemente de la dopamina",
        "estado": "HIPÓTESIS"
    }
    print("\nProbando nueva hipótesis...")
    aprobado, razones, tareas = supervisor.validate_knowledge_object(obj_valido)
    print(f"Estado: {aprobado} | Tareas Adversarias Generadas: {tareas}")
