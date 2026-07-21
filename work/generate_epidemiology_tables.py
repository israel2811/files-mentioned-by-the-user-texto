# CAPÍTULO IV — Tablas Epidemiológicas Expandidas
# Expansión Académica: Síntesis de Prevalencia AAV / CCA (2026-07-21)
# Genera el archivo de tablas como complemento a CAPITULOS_MONOGRAFICOS_IV_VII_CCA.md

TABLAS_EPIDEMIOLOGICAS = """
# TABLAS EPIDEMIOLÓGICAS EXPANDIDAS — CAPÍTULO IV
## Tesis: La CCA y la Pareidolia Algorítmica en el Continuum de la Psicosis
### Doctorando: Israel Realivázquez Mancillas — UACJ

---

## Tabla 4.1 — Prevalencia de AAV/Experiencias Psicóticas en Población General
| Estudio | N | Grupo Etario | Prevalencia (%) | DOI |
|:---|---:|:---|---:|:---|
| McGrath et al. (2015) | 31,261 | Adultos 18+ / 18 países | 5.8 | 10.1001/jamapsychiatry.2015.0575 |
| Beavan et al. (2011) | Revisión | Adultos Generales | 5–28 | 10.3109/09638237.2011.562262 |
| Linscott & van Os (2013) | Meta-análisis | Niños y Adultos | 7.2 | 10.1017/s0033291712001626 |
| Kråkvik et al. (2015) | 30,889 | Adultos Noruegos | 7.3 | 10.1111/sjop.12236 |

## Tabla 4.2 — Prevalencia de AAV en Infancia y Adolescencia
| Estudio | N | Grupo Etario | Prevalencia (%) | Seguimiento | DOI |
|:---|---:|:---|---:|:---|:---|
| Bartels-Velthuis et al. (2010) | 3,870 | 7–8 años | 9.0 | Longitudinal 2 años | 10.1192/bjp.bp.109.065953 |
| Kompus et al. (2015) | Poblacional | Adolescentes Noruegos | 7.3 | Transversal | 10.1111/sjop.12219 |
| Maijer et al. (2018, Meta-análisis) | 19 estudios | Ciclo vital completo | 12.0 (mediana) | Ciclo vital | 10.1017/s0033291717002367 |

## Tabla 4.3 — Diferenciación Fenomenológica Clínica vs. No Clínica (Waters et al., 2012)
| Eje Fenomenológico | Voces Clínicas | Voces No Clínicas | Fuente |
|:---|:---|:---|:---|
| Contenido predominante | Negativo / Imperativo / Crítico | Neutral o Positivo | Waters et al., 2012 DOI: 10.1093/schbul/sbs045 |
| Control percibido | Bajo (< control del sujeto) | Alto (sujeto puede ignorar o modular) | Waters et al., 2012 |
| Malestar subjetivo | Alto (afecta funcionamiento) | Bajo–Moderado | Waters et al., 2012 |
| Atribución de fuente | Externa (agente externo) | Interna o mixta | Waters et al., 2012 |
| Deterioro funcional | Consistente | Ausente o mínimo | Johns et al., 2014 DOI: 10.1093/schbul/sbu005 |
| Claridad perceptiva | Alta | **Similar** a voces clínicas | Daalman et al., 2011 DOI: 10.4088/jcp.09m05797yel |

> **[POR-VALIDAR]**: La posición de las AAV inducidas por CCA/Pareidolia Algorítmica en esta tabla
> requiere validación instrumental (Protocolo P4) antes de ser incorporada al cuerpo académico.

## Tabla 4.4 — Matriz de Decisión Clínica Inicial (M8)
| Categoría | Criterio | Evaluación Requerida | Instrumento |
|:---|:---|:---|:---|
| Orgánico-Auditivo | Pérdida auditiva / deaferentación | Audiometría, PEATC | Audiograma clínico |
| Neurológico | Crisis focales temporales | EEG, fMRI | EEG de registro nocturno |
| Psiquiátrico-Disociativo | Trauma, TLP, TLP-disociativo | PTSD / DES / PANSS | Entrevista clínica semiestructurada |
| Técnico-CCA [POR-VALIDAR] | Señales degradadas VoIP | UDP Sniffer / Faraday / Anecóica | Protocolo P4 forense independiente |
"""

from pathlib import Path
out_path = Path(r"c:\Users\Dell\Documents\Codex\2026-06-07\files-mentioned-by-the-user-texto\outputs\TABLAS_EPIDEMIOLOGICAS_CAP_IV_NEXUS.md")
out_path.write_text(TABLAS_EPIDEMIOLOGICAS, encoding="utf-8")
print(f"[OK] Tablas epidemiológicas escritas en: {out_path}")
