#!/usr/bin/env python3
"""Monograph Chapters VIII-X Generator for Tesis CCA-AAV.

Generates the complete draft for:
- Chapter VIII:  Evaluacion Clinica Diferencial
- Chapter IX:   Intervenciones y Abordajes Terapeuticos
- Chapter X:    Marco Etico y Forense
"""

from __future__ import annotations
from pathlib import Path

OUT_FILE = Path(__file__).parent.parent / "outputs" / "CAPITULOS_MONOGRAFICOS_VIII_X_CCA.md"

TEXT = r"""# Capitulos Monograficos de Tesis Doctoral: VIII, IX y X
**Titulo:** La Convergencia Cyber-Acustica (CCA) y la Pareidolia Algoritmica en el Continuum de la Psicosis
**Doctorando:** Israel Realivazquez Mancillas
**Institucion:** Universidad Autonoma de Ciudad Juarez (UACJ)

---

## CAPITULO VIII: EVALUACION CLINICA DIFERENCIAL DE LAS AAV EN CONTEXTO CCA

### 8.1 Diagnostico Diferencial Ampliado
El diagnostico diferencial de las AAV debe considerar no solo las categorias psiquiatricas clasicas (esquizofrenia, trastorno esquizoafectivo, trastorno limite de la personalidad, TEPT) sino tambien los inductores ambientales y tecnologicos que el modelo CCA introduce como variables causales.

Slotema et al. (2018, DOI: 10.3389/fpsyt.2018.00347) documentaron la presencia de AAV en pacientes con trastorno limite de la personalidad (TLP), encontrando que hasta el 50% de los pacientes con TLP reportan voces, frecuentemente en contextos de disociacion. Este hallazgo es relevante porque la disociacion (medida por la Dissociative Experiences Scale, DES) ha sido identificada como un factor de riesgo independiente para las AAV (Pilton et al., 2015, DOI: 10.1016/j.cpr.2015.06.004).

### 8.2 Arbol de Decision Diagnostica CCA

El siguiente arbol de decision incorpora los escenarios A-D del modelo CCA al protocolo de evaluacion clinica estandar:

```
Paciente reporta AAV
         |
    [1] Evaluacion psiquiatrica estandar
         |
    +--- Cumple criterios DSM-5-TR para trastorno psicotico?
    |    SI --> Escenario A (patologia primaria)
    |           + Tratamiento farmacologico estandar
    |           + Considerar contribucion CCA como factor agravante
    |
    NO
    |
    +--- [2] Evaluacion audiologica (audiograma + QuickSIN + DPOAE + ABR Wave I)
    |
    +--- Evidencia de neuropatia auditiva oculta?
    |    SI --> Factor de riesgo periferico identificado
    |    NO --> Sensory gating intacto
    |
    +--- [3] Evaluacion de exposicion tecnologica
    |    Historia de uso de VoIP/celular: ____ hrs/dia
    |    Correlacion temporal AAV-uso de telefono?
    |
    +--- [4] Evaluacion de prior predictivo
    |    CAPS (Cardiff Anomalous Perceptions Scale): ____
    |    LSHS-R (Launay-Slade Hallucination Scale): ____
    |    DES-II (Dissociative Experiences Scale): ____
    |
    CLASIFICACION:
    - Neuropatia + Exposicion + Prior alto --> CCA Escenario C probable
    - Sin neuropatia + Sin exposicion + Prior alto --> AAV endogenas no clinicas
    - Cualquier perfil + Relevancia aberrante alta --> Riesgo de transicion C-D
```

### 8.3 Instrumentos Recomendados

| Dominio | Instrumento | Que Mide | Umbral CCA |
|---------|------------|----------|------------|
| Alucinaciones | PSYRATS-AH (Haddock et al., 1999) | Frecuencia, duracion, control, malestar | >= 12/60 |
| Percepciones anomalas | CAPS (Bell et al., 2006) | Experiencias perceptivas inusuales | >= 7/32 |
| Disociacion | DES-II (Carlson & Putnam, 1993) | Disociacion dimensional | >= 20/100 |
| Habla en ruido | QuickSIN (Killion et al., 2004) | SNR loss | >= 3 dB SNR loss |
| Metacognicion | MCQ-30 (Wells & Cartwright-Hatton, 2004) | Creencias metacognitivas | Subescala confianza cognitiva >= 15 |

---

## CAPITULO IX: INTERVENCIONES Y ABORDAJES TERAPEUTICOS

### 9.1 Intervenciones Farmacologicas
La evidencia actual sobre intervenciones farmacologicas para AAV se centra en el uso de antipsicoticos, que actuan primariamente sobre la via dopaminergica mesolimbica. Sin embargo, como el modelo CCA distingue entre la pareidolia perceptiva (independiente de dopamina) y la relevancia aberrante (dependiente de dopamina), el enfoque farmacologico debe diferenciarse:

#### Para el componente perceptivo (Escenario C puro):
- Los antipsicoticos clasicos son **ineficaces** contra la pareidolia per se, ya que la codificacion predictiva cortical no depende directamente de la dopamina.
- **Alternativa propuesta**: Moduladores glutamatergicos (e.g., memantina, D-serina) que actuan sobre receptores NMDA en la corteza auditiva, modificando la precision del prior predictivo.
- Bohlken et al. (2017, DOI: 10.1017/s003329171600115x) revisaron las alternativas de tratamiento para AAV, incluyendo estimulacion magnetica transcraneal (EMT) sobre el area temporal izquierda, con resultados mixtos pero prometedores para voces resistentes a farmacoterapia.

#### Para el componente motivacional (Transicion C-D):
- Los antipsicoticos de segunda generacion (risperidona, aripiprazol) reducen la relevancia aberrante sin sedar completamente al paciente.
- La dosis debe ser la minima efectiva para reducir la significacion personal de las voces sin eliminar la pareidolia (que podria ser irrelevante clinicamente si no genera malestar).

### 9.2 Intervenciones Psicologicas

#### Terapia Cognitivo-Conductual para Voces (CBTv)
Thomas et al. (2014, DOI: 10.1093/schbul/sbu037) revisaron sistematicamente las terapias psicologicas para AAV y concluyeron que la CBTv es la intervencion con mayor evidencia para reducir el malestar asociado a las voces (aunque no necesariamente su frecuencia o intensidad). Los componentes especificos relevantes para la CCA incluyen:

1. **Normalizacion**: Explicar al paciente que la pareidolia es un fenomeno perceptivo normal amplificado por condiciones tecnicas especificas.
2. **Reestructuracion de atribuciones**: Cambiar la interpretacion de "alguien me habla intencionalmente" a "mi cerebro esta rellenando huecos en una senal degradada".
3. **Entrenamiento en reality testing**: Ensayar al paciente a verificar activamente si las voces correlacionan con el uso de telecomunicaciones.

#### Terapia de Aceptacion y Compromiso (ACT)
Para pacientes en los que la pareidolia persiste, la ACT ofrece un marco alternativo centrado en reducir la fusion cognitiva con el contenido de las voces sin intentar eliminarlas.

### 9.3 Intervenciones Tecnologicas (Ingenieriles)

#### Modificacion del Comportamiento de Uso
- Reducir el tiempo de llamada VoIP en entornos ruidosos.
- Utilizar auriculares con cancelacion activa de ruido (ANC) que reduzcan el ruido ambiental, aumentando la SNR efectiva.
- Evitar el uso de altavoz del telefono en ambientes silenciosos (donde el CNG es mas perceptible).

#### Modificacion del Codec
- Solicitar a los operadores de telecomunicaciones el uso de codecs con CNG mejorado (ruido modulado en amplitud aleatoria en lugar de constante).
- Desactivar el CNG cuando es posible en aplicaciones VoIP (e.g., Signal, WhatsApp permiten configuracion avanzada en algunos casos).

---

## CAPITULO X: MARCO ETICO Y FORENSE

### 10.1 Etica de la Investigacion con Poblaciones Vulnerables
La investigacion con sujetos que experimentan AAV requiere consideraciones eticas especiales:

1. **Capacidad de consentimiento**: Los participantes deben demostrar comprension del proposito del estudio y de la naturaleza experimental de la exposicion al CNG.
2. **No maleficencia**: La exposicion al CNG no debe exceder duraciones que puedan inducir cronificacion de la pareidolia (maximo 5 minutos por condicion, con intervalos de recuperacion).
3. **Confidencialidad reforzada**: Los datos de audio grabados durante las sesiones experimentales constituyen informacion sensible que debe almacenarse con encriptacion AES-256.

### 10.2 Consideraciones Forenses

#### Diferenciacion Pericial
El modelo CCA proporciona herramientas conceptuales para la pericia forense en casos donde un sujeto reporta "ser atacado con voces":

| Escenario | Evidencia que lo respalda | Implicacion forense |
|-----------|--------------------------|-------------------|
| A (Patologia primaria) | Diagnostico psiquiatrico previo, deterioro funcional | Inimputabilidad parcial/total |
| B (Stalkerware real) | Logs de red, malware en dispositivo, trazas ISO 27037 | Delito informatico |
| C (Pareidolia CCA) | Correlacion temporal con uso de telecomunicaciones | Fenomeno ambiental, no delito |
| D (Coexistencia) | Combinacion de evidencia B + A o C | Evaluacion caso por caso |

#### Cadena de Custodia Digital
Toda evidencia de actividad de red, logs de aplicaciones y grabaciones de audio debe manejarse bajo los lineamientos de ISO/IEC 27037:2012 (Guidelines for identification, collection, acquisition and preservation of digital evidence):

1. Documentar hash SHA-256 de cada archivo en el momento de la adquisicion.
2. Almacenar en medio de solo lectura (WORM).
3. Mantener registro cronologico de acceso.

### 10.3 Implicaciones Legales en Mexico

El Codigo Penal Federal de Mexico y los codigos estatales (en particular el de Chihuahua) tipifican los delitos informaticos bajo los articulos 211 bis 1 al 211 bis 7 del CPF. El acceso no autorizado a dispositivos moviles para inyectar audio o modificar el comportamiento del codec constituiria:

- **Acceso ilicito a sistemas informaticos** (Art. 211 bis 1 CPF).
- **Interceptacion de comunicaciones privadas** (Art. 177 CPF, en relacion con el Art. 16 constitucional).

La documentacion forense bajo ISO 27037 es esencial para que la evidencia sea admisible ante el Ministerio Publico y en procedimientos judiciales.
"""


def main() -> int:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(TEXT, encoding="utf-8")
    print(f"SUCCESS: Wrote chapters VIII-X draft to: {OUT_FILE.resolve()}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
