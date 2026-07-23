import json
import os
from datetime import datetime

PROFILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'nexus_user_profile.json')

class NexusUserProfile:
    """
    Capa 3: Perfil Dinámico del Usuario.
    Mantiene un perfil vivo que aprende de la interacción.
    """
    def __init__(self):
        self.profile = self.load_profile()

    def load_profile(self):
        if os.path.exists(PROFILE_PATH):
            try:
                with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading profile: {e}")
        
        # Default profile
        return {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "depth_preference": 0.95, # 95% rigor
            "complexity_tolerance": "high",
            "primary_interests": ["CCA-AAV", "fenomenología clínica", "RDoC", "audio codecs", "PLC", "CNG"],
            "ai_preferences": {
                "coding": "Codex",
                "reasoning": "Claude",
                "orchestration": "Antigravity",
                "data_extraction": "Gemini"
            },
            "interaction_stats": {
                "total_cycles_run": 0,
                "tasks_auto_generated": 0
            }
        }
    
    def save_profile(self):
        self.profile["last_updated"] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
        with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)

    def update_preference(self, key, value):
        self.profile[key] = value
        self.save_profile()
        
    def add_interest(self, interest):
        if interest not in self.profile["primary_interests"]:
            self.profile["primary_interests"].append(interest)
            self.save_profile()

    def record_cycle(self):
        self.profile["interaction_stats"]["total_cycles_run"] += 1
        self.save_profile()

    def record_auto_task(self):
        self.profile["interaction_stats"]["tasks_auto_generated"] += 1
        self.save_profile()

    def get_profile_summary(self):
        return f"Perfil Dinámico: Tolerancia {self.profile['complexity_tolerance']}, Rigor: {self.profile['depth_preference']*100}%"

if __name__ == "__main__":
    profile = NexusUserProfile()
    print("Perfil cargado:")
    print(json.dumps(profile.profile, indent=2))
