#!/usr/bin/env python3
"""Monograph Chapters IV-VII Generator for Tesis CCA-AAV.

Generates the complete draft for:
- Chapter IV: Epidemiología y Prevalencia
- Chapter V: Fenomenología de las AAV
- Chapter VI: Mecanismos Cognitivos y Neurobiológicos
- Chapter VII: Interfaz Técnica CCA y Criterios de Validación
"""

from __future__ import annotations
from pathlib import Path

OUT_FILE = Path(__file__).parent.parent / "outputs" / "CAPITULOS_MONOGRAFICOS_IV_VII_CCA.md"

TEXT = r"""# Capítulos Monográficos de Tesis Doctoral: IV, V, VI y VII
**Título:** La Convergencia Cyber-Acústica (CCA) y la Pareidolia Algorítmica en el Continuum de la Psicosis
**Doctorando:** Israel Realivázquez Mancillas
**Institución:** Universidad Autónoma de Ciudad Juárez (UACJ)

---

## CAPÍTULO IV: EPIDEMIOLOGÍA Y PREVALENCIA DE LAS EXPERIENCIAS PSICÓTICAS Y LAS ALUCINACIONES AUDITIVAS VERBALES

### 4.1 Prevalencia en Población General
La evidencia epidemiológica contemporánea demuestra de forma consistente que las experiencias psicóticas subclínicas, incluyendo las alucinaciones auditivas verbales (AAV), se distribuyen en la población general con tasas significativamente superiores a las de los trastornos psicóticos diagnosticados formalmente. La revisión sistemática de Beavan, Read y Cartwright (2011, DOI: 10.3109/09638237.2011.562262) estimó que entre el 5% y el 28% de la población general reporta haber escuchado voces al menos una vez en su vida, dependiendo de la metodología de medición utilizada y el umbral de inclusión. Esta amplia variabilidad resalta la importancia de operacionalizar con precisión el constructo de "oír voces" antes de extraer conclusiones clínicas.

McGrath et al. (2015, DOI: 10.1001/jamapsychiatry.2015.0575), en un análisis transnacional basado en 31,261 respondientes de 18 países, reportaron una prevalencia global de experiencias psicóticas del 5.8% (IC 95%: 5.2%-6.3%). Este hallazgo es particularmente relevante para la tesis CCA porque demuestra que el fenómeno perceptivo no es exclusivo de muestras clínicas psiquiátricas, lo cual abre el espacio epistemológico para investigar inductores ambientales y tecnológicos como factores contribuyentes.

### 4.2 Prevalencia en Desarrollo Infantil y Adolescente
Las estimaciones del fenómeno varían sustancialmente cuando se segmentan por grupo etario. Bartels-Velthuis et al. (2010, DOI: 10.1192/bjp.bp.109.065953) documentaron una prevalencia de alucinaciones vocales auditivas del 9% en niños de 7-8 años en una muestra poblacional holandesa (N = 3,870), con un seguimiento longitudinal que mostró que la mayoría de estas experiencias remitían espontáneamente antes de la adolescencia.

En la población adolescente, Kompus et al. (2015, DOI: 10.1111/sjop.12219) reportaron una prevalencia del 7.3% en una muestra poblacional noruega. Estos datos permiten argumentar que una proporción significativa de la población juvenil experimenta AAV transitorias sin desarrollar trastornos psicóticos, lo cual es consistente con el modelo de continuum de psicosis.

### 4.3 Meta-análisis del Ciclo Vital
El meta-análisis de Maijer et al. (2018, DOI: 10.1017/s0033291717002367) integró datos de 19 estudios que cubrían el espectro completo de edad (infancia a vejez) y documentó una prevalencia mediana del 12% para AAV a lo largo de la vida, con una curva de prevalencia que muestra picos en la infancia media (7-8 años), una disminución durante la adolescencia tardía, y un segundo incremento en la vejez asociado a la deaferentación sensorial auditiva.

### 4.4 Implicaciones para la CCA
La prevalencia de CCA, a diferencia de las AAV endógenas, no puede estimarse directamente a partir de estudios epidemiológicos psiquiátricos porque el fenómeno requiere la co-ocurrencia simultánea de: (a) exposición activa a señales degradadas de telecomunicaciones, y (b) vulnerabilidad neurobiológica del prior predictivo. Por lo tanto, la CCA se conceptualiza como una variable dependiente condicional cuya prevalencia está acotada por la intersección de la exposición tecnológica y la susceptibilidad cognitiva individual.

---

## CAPÍTULO V: FENOMENOLOGÍA DE LAS ALUCINACIONES AUDITIVAS VERBALES

### 5.1 Caracterización Clínica vs. No Clínica
Waters et al. (2012, DOI: 10.1093/schbul/sbs045) propusieron un modelo integrado de mecanismos cognitivos para las AAV que distingue sistemáticamente las experiencias clínicas (asociadas a esquizofrenia y otros trastornos psicóticos) de las no clínicas (presentes en la población general sin diagnóstico psiquiátrico). Este modelo identificó cinco ejes de diferenciación fenomenológica:

1. **Contenido**: Las voces clínicas tienden a ser más negativas, imperativas y críticas; las no clínicas son más neutras o positivas.
2. **Control percibido**: Los oyentes no clínicos reportan mayor sensación de control sobre las voces.
3. **Malestar asociado**: El malestar subjetivo es significativamente mayor en las poblaciones clínicas.
4. **Atribución de fuente**: Los oyentes clínicos atribuyen las voces a agentes externos con mayor frecuencia.
5. **Deterioro funcional**: Solo las voces clínicas se asocian consistentemente a deterioro en el funcionamiento social, laboral y personal.

### 5.2 Comparación Fenomenológica Directa
Daalman et al. (2011, DOI: 10.4088/jcp.09m05797yel) realizaron una comparación fenomenológica directa entre pacientes con esquizofrenia (N = 118) e individuos sanos que oyen voces (N = 111) utilizando la Auditory Vocal Hallucination Rating Scale (AVHRS). Los resultados mostraron que las voces no clínicas tenían menor frecuencia, menor duración por episodio, mayor control percibido y menor contenido negativo. Sin embargo, un hallazgo crucial fue que la **claridad perceptiva** (cuán vívida y real se percibe la voz) no difería significativamente entre ambos grupos, lo cual implica que la fenomenología del percepto en sí misma es insuficiente como criterio diagnóstico diferencial.

### 5.3 Modulación Cultural
Luhrmann et al. (2015, DOI: 10.1192/bjp.bp.113.139048) demostraron en un estudio intercultural (EE.UU., India, Ghana) que el significado social y la respuesta comunitaria hacia las voces modulan profundamente la interpretación y el sufrimiento asociado. Los participantes en Chennai y Accra reportaron relaciones más positivas con sus voces y menor angustia que los participantes en San Mateo, EE.UU. Este hallazgo es relevante para la tesis CCA porque demuestra que la **capa interpretativa** del modelo FPI (la "I") no es un artefacto clínico sino un constructo modulado socioculturalmente.

### 5.4 Fenomenología Específica de la CCA
La hipótesis de que el estímulo CCA pueda generar marcadores fenomenológicos distintivos se fundamenta en las propiedades físicas del portador. A diferencia de las AAV endógenas puras, la pareidolia inducida por CNG/PLC debería presentar:

- **Latencia fija**: Las voces deberían aparecer con una latencia predecible ligada al retardo de red y al tamaño del buffer de jitter (~20-200 ms).
- **Dependencia contextual de conectividad**: Las experiencias deberían correlacionar temporalmente con períodos de uso activo de telecomunicaciones.
- **Firma espectral reproducible**: El contenido fonético percibido debería mostrar patrones repetitivos ligados a la periodicidad algorítmica del CNG.

Estas predicciones son proposiciones físicas sujetas a validación instrumental (Richards et al., 2021, DOI: 10.1016/j.neubiorev.2021.09.006; Alderson-Day et al., 2017, DOI: 10.1093/brain/awx206).

---

## CAPÍTULO VI: MECANISMOS COGNITIVOS Y NEUROBIOLÓGICOS

### 6.1 Modelos Cognitivos de las AAV
Badcock y Hugdahl (2012, DOI: 10.1016/j.neubiorev.2011.07.010) sintetizaron los mecanismos cognitivos implicados en las AAV en grupos psicóticos y no psicóticos. Los principales mecanismos identificados incluyen:

1. **Monitoreo de fuente (*source monitoring*)**: Fallas en la capacidad de discriminar entre el habla interna auto-generada y las percepciones auditivas de origen externo.
2. **Sesgo de externalización**: Tendencia sistemática a atribuir experiencias perceptivas internas a fuentes externas, documentada por el meta-análisis de Brookwell, Bentall y Varese (2013, DOI: 10.1017/s0033291712002760).
3. **Procesamiento predictivo y priors fuertes**: Corlett et al. (2019, DOI: 10.1016/j.tics.2018.12.001) formalizaron el modelo de "priors fuertes", argumentando que las alucinaciones surgen cuando las expectativas perceptivas dominan sobre la evidencia sensorial entrante.

### 6.2 Neuroanatomía Funcional
Di Biase et al. (2020, DOI: 10.1017/s0033291719000205) revisaron la evidencia de neuroimagen en pacientes con AAV y en poblaciones sanas, identificando convergencias en la activación del giro temporal superior (STG), la ínsula anterior y la corteza prefrontal durante episodios de AAV. Sin embargo, los autores enfatizaron las limitaciones metodológicas de los estudios existentes, incluyendo tamaños de muestra pequeños y heterogeneidad en los paradigmas experimentales.

Garrison et al. (2019, DOI: 10.1093/schbul/sby157) demostraron que la morfología del surco paracingulado (PCS) difería significativamente entre grupos clínicos y no clínicos que experimentan AAV. La ausencia o reducción del PCS se asoció con mayor severidad de las alucinaciones, proporcionando un potencial biomarcador neuroanatómico de vulnerabilidad.

### 6.3 Procesamiento de Habla Ambigua
Alderson-Day et al. (2017, DOI: 10.1093/brain/awx206) investigaron cómo los oyentes de voces no clínicos procesan estímulos de habla ambigua, encontrando que estos individuos muestran una activación atípica en las redes de procesamiento del lenguaje cuando se enfrentan a señales acústicas degradadas. Este hallazgo es directamente relevante para la hipótesis CCA, ya que el CNG y el PLC generan precisamente este tipo de señales ambiguas.

### 6.4 El Modelo de Codificación Predictiva Aplicado a la CCA
La contribución central del presente trabajo consiste en formalizar la divergencia del filtro predictivo cerebral como mecanismo unificador. Cuando la precisión sensorial $\pi_s$ disminuye por cualquier causa (degradación del códec, neuropatía auditiva oculta, aislamiento acústico extremo), la ganancia relativa del prior $\pi_p$ crece de forma proporcional inversa. El sistema cortical, operando como un filtro de Kalman adaptativo, amplifica las fluctuaciones del ruido de entrada y las proyecta como percepciones estructuradas coherentes con la hipótesis interna más probable.

---

## CAPÍTULO VII: INTERFAZ TÉCNICA CCA Y CRITERIOS DE VALIDACIÓN INSTRUMENTAL

### 7.1 Vectores de Inserción Digital
Los sistemas modernos de transmisión de voz sobre IP (VoIP) y redes celulares LTE/5G emplean codificación adaptativa (AMR-WB, EVS, Opus) diseñada para optimizar el ancho de banda disponible. Esta optimización introduce tres mecanismos que generan estímulos acústicos subumbrales con potencial inductivo de pareidolia:

1. **Packet Loss Concealment (PLC)**: Interpolación predictiva de paquetes perdidos que genera micro-oscilaciones cuasi-fonéticas.
2. **Comfort Noise Generation (CNG)**: Inyección de ruido artificial constante durante silencios para evitar la percepción de "llamada caída".
3. **Vocoders Neuronales**: Sistemas de síntesis basados en redes profundas que pueden imponer firmas de formantes humanos sobre el ruido ambiental.

### 7.2 Diseño del Protocolo de Control Negativo (P4)
El hito experimental definitivo de la tesis consiste en el experimento de aislamiento en condiciones controladas:

**Condición 1 — Cabina Anecoica con Jaula de Faraday**:
- Aislamiento acústico completo (norma ISO 3745).
- Blindaje electromagnético calibrado con atenuación mínima de 80 dB en el rango de 100 MHz a 6 GHz.
- Predicción: Si las AAV del sujeto persisten en esta condición, la fuente es endógena (Escenario A).

**Condición 2 — Cabina Anecoica sin Blindaje RF**:
- Aislamiento acústico pero permeabilidad electromagnética.
- Predicción: Si las AAV aparecen solo en esta condición, existe un componente RF potencial (requiere investigación adicional del Escenario B).

**Condición 3 — Entorno Natural con Dispositivo Activo**:
- Sin aislamiento, con smartphone activo y conectado a red celular.
- Monitoreo concurrente de tráfico UDP y actividad del códec.
- Predicción: Si las AAV correlacionan temporalmente con eventos de CNG/PLC del códec, se respalda la hipótesis del Escenario C.

### 7.3 Criterios de Falsabilidad
Siguiendo el principio popperiano de demarcación, la hipótesis CCA produce las siguientes predicciones falsables:

| # | Predicción | Condición de Falsación |
|---|-----------|----------------------|
| P1 | Las AAV correlacionan temporalmente con eventos CNG/PLC | No existe correlación significativa en series temporales (p > 0.05) |
| P2 | La pareidolia verbal es mayor ante CNG algorítmico que ante ruido térmico puro | No hay diferencia significativa en reportes entre ambos estímulos |
| P3 | Las AAV cesan completamente en la Condición 1 (Faraday + anecoica) | Las AAV persisten en aislamiento total, indicando origen endógeno |
| P4 | Sujetos con neuropatía oculta + prior alto muestran más pareidolia que controles | No hay interacción significativa entre neuropatía y prior en ANOVA 2x2 |
"""


def main() -> int:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(TEXT, encoding="utf-8")
    print(f"SUCCESS: Wrote chapters IV-VII draft to: {OUT_FILE.resolve()}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
