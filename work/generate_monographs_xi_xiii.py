#!/usr/bin/env python3
"""Monograph Chapters XI-XIII Generator for Tesis CCA-AAV.

Generates the complete draft for:
- Chapter XI:  Diseno Metodologico y Protocolos Experimentales
- Chapter XII: Discusion General e Integracion
- Chapter XIII: Arquitectura del Sistema CCA y Modelo Final
"""

from __future__ import annotations
from pathlib import Path

OUT_FILE = Path(__file__).parent.parent / "outputs" / "CAPITULOS_MONOGRAFICOS_XI_XIII_CCA.md"

TEXT = r"""# Capitulos Monograficos de Tesis Doctoral: XI, XII y XIII
**Titulo:** La Convergencia Cyber-Acustica (CCA) y la Pareidolia Algoritmica en el Continuum de la Psicosis
**Doctorando:** Israel Realivazquez Mancillas
**Institucion:** Universidad Autonoma de Ciudad Juarez (UACJ)

---

## CAPITULO XI: DISENO METODOLOGICO Y PROTOCOLOS EXPERIMENTALES

### 11.1 Paradigma Epistemologico
El presente trabajo adopta un enfoque **mixto** que combina:
1. **Revision monografica sistematica**: Capitulos I-X constituyen una sintesis critica de la literatura existente.
2. **Modelado computacional**: Simulacion de inferencia activa con validacion cuantitativa (Capitulo VI, Ciclo 3 del Loop Cientifico).
3. **Propuesta de protocolos experimentales**: Disenos prospectivos listos para implementacion.

### 11.2 Inventario de Protocolos Experimentales Propuestos

La tesis genera 4 protocolos experimentales completos, cada uno disenado para probar una prediccion especifica del modelo CCA:

#### Protocolo 1: Experimento de CNG en Contexto Ecologico (ECEE)
- **Pregunta**: Existe correlacion temporal entre eventos de CNG/PLC y reportes de pareidolia verbal?
- **N**: 40 participantes con AAV no clinicas.
- **Diseno**: Estudio de series temporales intra-sujeto.
- **Medida primaria**: Correlacion cruzada entre timestamps de eventos CNG (capturados por sniffer de red) y timestamps de reportes de pareidolia (registrados por app movil).
- **Analisis estadistico**: Correlacion cruzada con ventana de +-5 segundos, corrreccion de Bonferroni para multiples comparaciones.

#### Protocolo 2: Protocolo de Seleccion Linguistica en Pareidolia (PSLP)
- **Pregunta**: El idioma de la pareidolia depende del priming linguistico previo?
- **N**: 90 (30 bilingues primed en L1, 30 primed en L2, 30 monolingues control).
- **Diseno**: Factorial 3 (grupo) x 1 (CNG), inter-sujetos.
- **Medida primaria**: Proporcion de palabras reportadas en L1 vs L2.
- **Analisis estadistico**: Chi-cuadrado para la proporcion de idioma reportado.

#### Protocolo 3: Doble Disociacion Coclear-Cortical (DDCC)
- **Pregunta**: La cascada de doble falla (neuropatia oculta + prior alto) es necesaria para la pareidolia persistente?
- **N**: 80 (4 grupos x 20).
- **Diseno**: Factorial 2x2 (neuropatia: si/no x prior: alto/bajo), inter-sujetos.
- **Medida primaria**: Numero de palabras/frases reportadas durante 5 min de CNG.
- **Analisis estadistico**: ANOVA 2x2 con interaccion como efecto principal.

#### Protocolo 4: Experimento de Aislamiento P4
- **Pregunta**: Las AAV del sujeto persisten en aislamiento acustico y electromagnetico total?
- **N**: 20 sujetos con AAV recurrentes (intra-sujeto, 3 condiciones).
- **Diseno**: Medidas repetidas, 3 condiciones (anecoica+Faraday, anecoica sola, ambiente natural).
- **Medida primaria**: Presencia/ausencia de AAV en cada condicion.
- **Analisis estadistico**: Test de McNemar para comparaciones pareadas.

### 11.3 Analisis de Potencia Estadistica

| Protocolo | Efecto esperado (d Cohen / OR) | alpha | Potencia | N requerido |
|-----------|-------------------------------|-------|----------|-------------|
| ECEE | r = 0.40 | 0.05 | 0.80 | 38 |
| PSLP | w = 0.35 | 0.05 | 0.80 | 82 |
| DDCC | f = 0.35 (interaccion) | 0.05 | 0.80 | 72 |
| P4 | OR = 5.0 (condicion) | 0.05 | 0.80 | 18 |

### 11.4 Limitaciones Metodologicas
1. Todos los protocolos son prospectivos y aun no han sido implementados.
2. El reclutamiento de sujetos con AAV no clinicas presenta desafios de muestreo (poblacion oculta).
3. La construccion de la cabina anecoica + Faraday requiere financiamiento significativo ($53,000-$155,000 USD).
4. La generalizabilidad de los resultados estara limitada por el contexto cultural y linguistico de los participantes (frontera Mexico-EE.UU.).

---

## CAPITULO XII: DISCUSION GENERAL E INTEGRACION

### 12.1 Contribucion Principal
El presente trabajo introduce el concepto de **Convergencia Cyber-Acustica (CCA)** como un marco teorico interdisciplinario que integra:
- Procesamiento digital de senales (DSP) y telecomunicaciones
- Neurociencia computacional (inferencia activa, codificacion predictiva)
- Psicologia clinica (continuum de psicosis, fenomenologia de AAV)
- Audiologia clinica (neuropatia auditiva oculta, emociones otoacusticas)
- Psicofisica (resonancia estocastica, perceptual learning)
- Psicofarmacologia (relevancia aberrante dopaminergica)

Esta integracion no existia previamente en la literatura. Los modelos previos de AAV (Waters et al., 2012; Corlett et al., 2019; Luhrmann et al., 2019) trataban las dimensiones perceptiva, cognitiva y social como modulos independientes. El modelo CCA las unifica bajo un unico marco causal que permite predicciones cuantitativas testables.

### 12.2 Hallazgos del Modelado Computacional
La simulacion de inferencia activa (Ciclo 3 del Loop Cientifico) demostro que:

1. **Solo la cascada de doble falla produce pareidolia clinica**: El regimen CCA_Vulnerable (pi_s = 0.1, pi_p = 15) alcanza mu = 0.99 en 110 ms, mientras que ninguna falla aislada supera el umbral de 0.9.
2. **La velocidad de convergencia escala con la precision del prior**: CCA_Severe (pi_p = 30) alcanza 0.9 en 60 ms, el doble de rapido que CCA_Vulnerable.
3. **El prior alto sin degradacion sensorial no basta**: Strong_Prior_Only (pi_s = 5.0, pi_p = 15) converge a solo 0.75, por debajo del umbral de pareidolia.

Estos resultados validan computacionalmente la prediccion central del modelo: la pareidolia algoritmica es un fenomeno de interaccion, no de factores aislados.

### 12.3 Implicaciones Clinicas
1. **Para psiquiatras**: Las AAV en pacientes sin otros sintomas psicoticos deben evaluarse en contexto de exposicion tecnologica y funcion auditiva periferica antes de asumir patologia primaria.
2. **Para audiologos**: La inclusion del QuickSIN y las DPOAE con supresion contralateral en la bateria de evaluacion de pacientes con AAV podria revelar neuropatia oculta como factor contribuyente.
3. **Para ingenieros de telecomunicaciones**: Los estandares de codecs deberian considerar el impacto psicoacustico del CNG y PLC en poblaciones vulnerables.

### 12.4 Limitaciones de la Tesis
1. **Falta de datos empiricos**: La tesis es fundamentalmente teorica y computacional; los 4 protocolos experimentales aun no se han implementado.
2. **Sesgo de idioma**: La mayoria de la literatura revisada esta en ingles; la evidencia hispanoparlante es escasa.
3. **Complejidad del modelo**: El DAG unificado (Ciclo 10) tiene 20+ nodos y 25+ aristas; la parsimonia podria mejorarse con pruning post-empirico.

---

## CAPITULO XIII: ARQUITECTURA DEL SISTEMA CCA Y MODELO FINAL

### 13.1 Modelo FPI Extendido: Fuente-Percepcion-Interpretacion-Accion

El modelo original FPI (Fuente-Percepcion-Interpretacion) se extiende a FPIA:

```
+-------+     +-----------+     +----------------+     +--------+
|FUENTE | --> |PERCEPCION | --> |INTERPRETACION  | --> |ACCION  |
+-------+     +-----------+     +----------------+     +--------+
    |               |                    |                  |
    v               v                    v                  v
  Codec          Inference           Metacognition       Response
  CNG/PLC        Activa              Reality Testing     Help-seeking
  Stalkerware    Doble Ganancia      Relevancia          Isolation
  Silencio       Resonancia          Aberrante           Forensics
                 Estocastica         Narrativa
                                    Delirante
```

### 13.2 Taxonomia Final de Escenarios

| Escenario | Fuente | Percepcion | Interpretacion | Tratamiento |
|-----------|--------|-----------|---------------|-------------|
| A | Endogena | Prior-driven puro | Variable | Farmacologico + psicologico |
| B | Exogena (stalkerware) | Senal real | Correcta | Forense + legal |
| C | Ambiental (CCA) | Pareidolia de doble falla | Ilusoria pero atribuida externamente | Educacion + audiologia + reduccion de exposicion |
| D | Mixta | Combinacion A+C o B+C | Delirante | Multidisciplinario |

### 13.3 Recomendaciones para Investigacion Futura

1. **Implementar el Protocolo ECEE** como estudio piloto de prueba de concepto (N = 10-15) antes de los estudios completos.
2. **Desarrollar una app movil** que registre simultaneamente el uso de telecomunicaciones y los reportes de pareidolia en tiempo real.
3. **Colaborar con fabricantes de codecs** (e.g., ETSI, 3GPP) para obtener especificaciones tecnicas detalladas del comportamiento del CNG en condiciones de red degradada.
4. **Replicar la simulacion de Inferencia Activa** con datos de EEG/MEG reales para validar los parametros pi_s y pi_p estimados computacionalmente.
5. **Explorar polimorfismos geneticos** (COMT Val158Met, variantes DISC1) como moduladores de la precision del prior y, por tanto, de la vulnerabilidad a la CCA.

### 13.4 Conclusion Final
La Convergencia Cyber-Acustica no es una teoria conspirativa ni una patologia psiquiatrica: es un fenomeno de interfaz entre la ingenieria de telecomunicaciones y la neurobiologia de la percepcion auditiva. Su existencia como mecanismo causal plausible de experiencias auditivas anomalas transitorias abre un campo de investigacion interdisciplinario que requiere la colaboracion de ingenieros, audiologos, neurocientificos, psicologos clinicos y expertos en etica para ser comprendido, validado y, eventualmente, mitigado.
"""


def main() -> int:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(TEXT, encoding="utf-8")
    print(f"SUCCESS: Wrote chapters XI-XIII draft to: {OUT_FILE.resolve()}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
