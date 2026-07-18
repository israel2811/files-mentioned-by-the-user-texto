import json
import sys
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower

def calculate_sample_sizes():
    # Parámetros estándar: alfa = 0.05, beta = 0.20 (Poder = 0.80), Cohen's d = 0.5 (Efecto medio)
    alpha = 0.05
    power = 0.80
    effect_size_d = 0.5
    effect_size_f = 0.25 # Equivalente de d=0.5 para ANOVA

    results = {}

    # 1. T-test Independiente (Comparación de latencias Grupo Control vs Grupo Bilingüe)
    ttest_power = TTestIndPower()
    n_ttest = ttest_power.solve_power(effect_size=effect_size_d, alpha=alpha, power=power, ratio=1.0)
    results['protocol_ttest'] = {
        'test': 'Independent T-Test (Control vs Bilingual)',
        'required_n_per_group': int(n_ttest + 1),
        'total_n': int(n_ttest + 1) * 2
    }

    # 2. ANOVA (3 grupos: Healthy, Hearing Loss, Vulnerable)
    anova_power = FTestAnovaPower()
    # k_groups = 3. degrees of freedom = k - 1 = 2
    n_anova = anova_power.solve_power(effect_size=effect_size_f, alpha=alpha, power=power, k_groups=3)
    results['protocol_anova'] = {
        'test': 'One-Way ANOVA (3 Groups)',
        'required_total_n': int(n_anova * 3 + 1) 
    }

    with open('../outputs/power_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    print(f"[OK] Análisis de Potencia (G*Power Automático) completado. T-Test N Total: {results['protocol_ttest']['total_n']}, ANOVA N Total: {results['protocol_anova']['required_total_n']}")
    
if __name__ == "__main__":
    calculate_sample_sizes()
