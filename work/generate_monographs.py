#!/usr/bin/env python3
"""Monograph Chapters Generator for Tesis CCA-AAV.

Generates the complete draft for Chapter I (Introduction & Problem), Chapter II 
(Differential Diagnoses), and Chapter III (Psychosis Continuum & FPI Model) 
with strict DOI-based academic citations.
"""

from __future__ import annotations

from pathlib import Path

OUT_FILE = Path(__file__).parent.parent / "outputs" / "CAPITULOS_MONOGRAFICOS_I_II_III_CCA.md"

TEXT = """# Capítulos Monográficos de Tesis Doctoral: I, II y III
**Título Tentativo:** La Convergencia Cyber-Acústica (CCA) y la Pareidolia Algorítmica en el Continuum de la Psicosis
**Doctorando:** Israel Realivázquez Mancillas
**Institución:** Universidad Autónoma de Ciudad Juárez (UACJ)

---

## CAPÍTULO I: INTRODUCCIÓN Y PLANTEAMIENTO DEL PROBLEMA

### 1.1 Contextualización y Frontera del Objeto de Estudio
El estudio de las Alucinaciones Auditivas Verbales (AAV) ha experimentado un giro paradigmático en las últimas décadas. Tradicionalmente confinadas al ámbito de la psicopatología primaria de tipo esquizofrénico, las aproximaciones contemporáneas sugieren la existencia de un continuum fenomenológico y cognitivo que distribuye estas experiencias a lo largo de la población general (Johns & van Os, 2001, DOI: 10.1016/s0272-7358(01)00103-9). Una AAV se define en este marco como una experiencia sensoperceptiva de voz o habla sin un estímulo físico externamente compartido que la origine. Sin embargo, el surgimiento de infraestructuras digitales de telecomunicaciones y el procesamiento móvil de señales introduce una nueva dimensión empírica que desafía el deslinde puramente psicopatológico: la hipótesis de la Convergencia Cyber-Acústica (CCA).

La CCA se postula en este trabajo como una interfaz acústico-cognitiva donde imperfecciones intrínsecas del procesamiento digital de señales (tales como retardos de red, paquetes perdidos y la inyección de ruido de confort en codecs VoIP) interactúan con cerebros dotados de predicciones bayesianas vulnerables o "priors" fuertes, detonando pareidolia auditiva estructurada (Corlett et al., 2019, DOI: 10.1016/j.tics.2018.12.001). Así, es crucial deslindar conceptualmente tres planos fenomenológicos:
1.  **Dimensión Clínica Endógena**: Alucinaciones auditivas asociadas a fallos de monitoreo de fuente interna y disfuncionalidad clínica sin estímulo físico subyacente.
2.  **Dimensión Técnico-Aislada**: Estimulación real generada por fugas acústicas, inducciones electromagnéticas o software malicioso (stalkerware) infiltrado en el dispositivo del sujeto.
3.  **Dimensión Intermedia (Pareidolia Algorítmica)**: La degradación física de señales telefónicas/digitales (degradadas por códecs PLC/CNG) que actúan como estímulos inductores de pareidolia acústica verbal en sujetos vulnerables (Richards et al., 2021, DOI: 10.1016/j.neubiorev.2021.09.006).

### 1.2 Formulación del Problema y Pregunta de Investigación
La literatura epidemiológica confirma que la prevalencia transnacional de experiencias psicóticas subclínicas en población adulta oscila entre el 5% y el 8% (McGrath et al., 2015, DOI: 10.1001/jamapsychiatry.2015.0575). El problema surge cuando el clínico, al evaluar a un sujeto que oye voces, aplica un reduccionismo nosológico (Error Tipo I), asumiendo una etiología psicótica primaria debido a que el estímulo físico/técnico no es perceptible de forma directa o inmediata por el evaluador. Por otro lado, una tecnificación excesiva (Error Tipo II) atribuye erróneamente toda experiencia a la interceptación o stalkerware, omitiendo la posibilidad de un trastorno sensoperceptivo de origen biológico.

La pregunta de investigación que guía esta tesis queda planteada en los siguientes términos: *¿Cuáles son los parámetros acústicos, algorítmicos y de procesamiento cognitivo que permiten diferenciar sistemáticamente las AAV de etiología endógena de aquellas inducidas por pareidolia algorítmica (CCA) bajo condiciones de transmisión VoIP degrada?*

---

## CAPÍTULO II: DIAGNÓSTICO DIFERENCIAL MÉDICO, AUDIOLÓGICO Y NEUROLÓGICO

### 2.1 Fronteras Orgánicas y Sensoriales de la Alucinación
El diagnóstico diferencial de las AAV exige descartar en primera instancia cualquier etiología orgánica o déficit periférico. Las investigaciones audiológicas demuestran que la deaferentación sensorial (pérdida de la entrada auditiva debido a daño coclear o presbiacusia) induce mecanismos de compensación central que pueden manifestarse como alucinaciones auditivas complejas (Marschall et al., 2020, DOI: 10.1097/yco.0000000000000586). Este fenómeno, análogo al síndrome de Charles Bonnet en el sistema visual, resalta la necesidad de realizar pruebas audiométricas exhaustivas y potenciales evocados auditivos de tronco cerebral (PEATC) (Musiek et al., 2021, DOI: 10.1055/s-0041-1722989).

### 2.2 Diferencial Neurológico y Fisiológico
Junto con el descarte audiológico, se debe evaluar la actividad bioeléctrica cerebral. Las crisis epilépticas focales temporales representan una causa neurológica clásica de alucinaciones auditivas episódicas estructuradas, a menudo acompañadas de distorsiones temporales, sensaciones de *déjà vu* o auras autonómicas (Serino et al., 2014, DOI: 10.1016/j.yebeh.2013.12.014). El registro electroencefalográfico (EEG) y, en casos específicos, el mapeo metabólico por resonancia magnética funcional (fMRI) son indispensables para la exclusión formal de focos epileptógenos activos antes de postular una hipótesis de pareidolia tecnológica o psicosis primaria.

La hipótesis CCA se formula aquí de forma estrictamente complementaria a estos protocolos:
```
                                +---------------------------+
                                |  Sujeto Reporta Voces /   |
                                |     Alucinaciones         |
                                +-------------+-------------+
                                              |
                       +----------------------+----------------------+
                       |                                             |
         +-------------v-------------+                 +-------------v-------------+
         |    Evaluación Médica      |                 |   Monitoreo Instrumental  |
         |        Estándar           |                 |         Forense           |
         +-------------+-------------+                 +-------------+-------------+
                       |                                             |
        +--------------+--------------+                       +------+------+
        |                             |                       |             |
+-------v-------+             +-------v-------+       +-------v-------+     v
| Otorrino /    |             | Psiquiatría / |       | Protocolo P4  |  (Faraday /
| Audiología    |             | RDoC Heurista |       | (UDP Sniffer) |   Anecoica)
+---------------+             +---------------+       +---------------+
```

---

## CAPÍTULO III: EL MODELO DE CONTINUUM Y LA HEURÍSTICA FUENTE-PERCEPCIÓN-INTERPRETACIÓN (FPI)

### 3.1 Fundamentos del Continuum de la Psicosis
El continuum de la psicosis postula que los síntomas psicóticos no constituyen categorías diagnósticas binarias y discretas, sino dimensiones continuas que van desde experiencias perceptivas inusuales en la población general sana hasta trastornos clínicamente graves que requieren intervención médica (van Os et al., 2009, DOI: 10.1017/s0033291708003814). Esta aproximación epidemiológica es esencial para el estudio de la CCA, ya que permite explicar cómo estímulos auditivos liminales causan interpretaciones delirantes complejas en individuos sin patología psiquiátrica grave, pero con priorizaciones perceptivas sesgadas (Linscott & van Os, 2013, DOI: 10.1017/s0033291712001626).

### 3.2 La Heurística FPI y la Integración Multimodal
Para estructurar el análisis fenomenológico de las voces y sus atribuciones causales, se propone el modelo heurístico Fuente-Percepción-Interpretación (FPI):
1.  **Fuente**: La señal acústica de entrada, que en el caso de la CCA consiste en flujos VoIP degradados con pérdida de paquetes y retardos de buffer de jitter (~150 ms de latencia típica).
2.  **Percepción**: La transducción neurofisiológica y el procesamiento predictivo cortical, donde los "priors" bayesianos procesan la señal ruidosa de confort como habla estructurada (Alderson-Day et al., 2017, DOI: 10.1093/brain/awx206).
3.  **Interpretación**: La atribución causal posterior efectuada por el sujeto, modulada por factores metacognitivos y de monitoreo de fuente (Badcock et al., 2012, DOI: 10.1016/j.neubiorev.2011.07.010).

Este modelo multidimensional permite integrar hallazgos de neuroimagen, estudios ecológicos diarios y la fenomenología intercultural de las voces, proporcionando un marco sólido para la validación teórica de la Convergencia Cyber-Acústica.
"""


def main() -> int:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(TEXT, encoding="utf-8")
    print(f"SUCCESS: Wrote chapters I, II, and III draft to: {OUT_FILE.resolve()}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
