from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


DRIVE = Path(r"G:\Mi unidad")
FUENTES_DIR = DRIVE / "03_FUENTES"
TESIS_DIR = DRIVE / "02_TESIS"
LOG_PATH = DRIVE / "00_LOG_DESKTOP.md"

SOURCE_JSON = FUENTES_DIR / "00_FUENTES_ACADEMICAS_DOI_VERIFICADAS_2026-06-07.json"

CORE_DOIS = [
    "10.1093/schbul/15.2.209",
    "10.1192/bjp.bp.113.139048",
    "10.1016/s0272-7358(01)00103-9",
    "10.1017/s0033291708003814",
    "10.1017/s0033291712001626",
    "10.1001/jamapsychiatry.2015.0575",
    "10.3109/09638237.2011.562262",
    "10.1017/s0033291717002367",
    "10.1192/bjp.bp.109.065953",
    "10.1111/sjop.12219",
    "10.1111/sjop.12236",
    "10.1016/j.cpr.2016.10.010",
    "10.1093/schbul/sbs045",
    "10.1093/schbul/sbs061",
    "10.1093/schbul/sbu005",
    "10.1111/acps.12531",
    "10.1093/schbul/sbw078",
    "10.1016/j.neubiorev.2021.09.006",
    "10.1017/s0033291719000205",
    "10.1017/s003329171600115x",
    "10.1016/j.tics.2018.12.001",
    "10.1093/schbul/sby157",
    "10.1093/brain/awx206",
    "10.1016/j.schres.2011.07.013",
    "10.4088/jcp.09m05797yel",
    "10.1017/s0033291712000761",
    "10.1016/j.neubiorev.2011.07.010",
    "10.1017/s0033291712002760",
    "10.1016/j.cpr.2015.06.004",
    "10.1017/s003329170700253x",
    "10.1016/j.cpr.2011.05.004",
    "10.1093/schbul/sbu037",
    "10.3389/fpsyt.2018.00347",
    "10.1016/b978-0-444-62630-1.00024-x",
    "10.1016/j.yebeh.2013.12.014",
    "10.1097/yco.0000000000000586",
    "10.1055/s-0041-1722989",
    "10.1093/schizbullopen/sgaa060",
    "10.1093/schbul/sbz002",
    "10.1093/schbul/sby110",
]

USE_OVERRIDES = {
    "10.1192/bjp.bp.113.139048": "Comparacion cultural de voces en Estados Unidos, India y Ghana para separar fenomenologia, significado social y sufrimiento.",
    "10.1016/s0272-7358(01)00103-9": "Continuum psicotico y base historica para no tratar toda experiencia psicotica subclinica como psicosis clinica.",
    "10.1017/s0033291708003814": "Meta-analisis del continuum de psicosis y marco de transicion entre experiencias subclinicas y necesidad de cuidado.",
    "10.1017/s0033291712001626": "Estimaciones conservadoras de incidencia/prevalencia de experiencias psicoticas en poblacion general.",
    "10.1001/jamapsychiatry.2015.0575": "Prevalencia transnacional de experiencias psicoticas en poblacion general adulta.",
    "10.3109/09638237.2011.562262": "Revision de prevalencia de personas que oyen voces en poblacion general.",
    "10.1017/s0033291717002367": "Meta-analisis especifico de alucinaciones auditivas a lo largo de la vida.",
    "10.1192/bjp.bp.109.065953": "Prevalencia y correlatos de alucinaciones vocales auditivas en infancia media.",
    "10.1111/sjop.12219": "Prevalencia poblacional adolescente de alucinaciones auditivas.",
    "10.1111/sjop.12236": "Comparacion poblacional entre oyentes de voces y grupos clinicos.",
    "10.1016/j.cpr.2016.10.010": "Revision sistematica de AVH y modelos de continuum.",
    "10.1093/schbul/sbs045": "Comparacion de alucinaciones auditivas en esquizofrenia y poblaciones no esquizofrenicas.",
    "10.1093/schbul/sbs061": "Rasgos caracteristicos de AVH en grupos clinicos y no clinicos.",
    "10.1093/schbul/sbu005": "Diferencia entre AVH con y sin necesidad de cuidado.",
    "10.1111/acps.12531": "Revision de evidencia sobre AVH para marco de mecanismos y clinica.",
    "10.1093/schbul/sbw078": "Redes cerebrales en reposo y AVH.",
    "10.1016/j.neubiorev.2021.09.006": "Procesamiento de habla externa y AVH.",
    "10.1017/s0033291719000205": "Meta-analisis de neuroimagen AVH en pacientes y poblacion sana.",
    "10.1017/s003329171600115x": "Neuroimagen y tratamiento de AVH.",
    "10.1016/j.tics.2018.12.001": "Modelo predictivo de alucinaciones y priors fuertes.",
    "10.1093/schbul/sby157": "Morfologia del surco paracingulado y alucinaciones clinicas/no clinicas.",
    "10.1093/brain/awx206": "Procesamiento de habla ambigua en personas con AVH no clinicas.",
    "10.1016/j.schres.2011.07.013": "AVH y funcionamiento cognitivo en individuos sanos.",
    "10.4088/jcp.09m05797yel": "Comparacion fenomenologica de AVH en esquizofrenia y no pacientes.",
    "10.1017/s0033291712000761": "Trauma infantil y AVH.",
    "10.1016/j.neubiorev.2011.07.010": "Mecanismos cognitivos de AVH en grupos psicoticos y no psicoticos.",
    "10.1017/s0033291712002760": "Sesgos de externalizacion, monitoreo de fuente y alucinaciones.",
    "10.1016/j.cpr.2015.06.004": "Revision/meta-analisis de disociacion y voces.",
    "10.1017/s003329170700253x": "Trauma y creencias sobre voces.",
    "10.1016/j.cpr.2011.05.004": "Revision critica de estudios cuantitativos de AVH.",
    "10.1093/schbul/sbu037": "Terapias psicologicas para voces.",
    "10.3389/fpsyt.2018.00347": "AVH en trastorno limite de personalidad y respuesta a antipsicoticos.",
    "10.1016/b978-0-444-62630-1.00024-x": "Diferencial neurologico y semiologia amplia de alucinaciones auditivas.",
    "10.1016/j.yebeh.2013.12.014": "AVH de origen epileptico como diferencial neurologico.",
    "10.1097/yco.0000000000000586": "Deaferentacion como causa de alucinaciones.",
    "10.1055/s-0041-1722989": "Horizonte audiologico de las alucinaciones auditivas.",
    "10.1093/schizbullopen/sgaa060": "Evaluacion digital/ecologica de AVH y afecto.",
    "10.1093/schbul/sbz002": "Debate sobre continuidad de severidad frente a continuidad de mecanismos.",
    "10.1093/schbul/sby110": "Modelo de multiples vias para AVH clinicas y no clinicas.",
}


def normalize_doi(doi: str) -> str:
    return doi.strip().lower()


def sentence_case(title: str) -> str:
    title = re.sub(r"\s+", " ", title.strip())
    title = title.rstrip(" .")
    return title[:1].upper() + title[1:]


def format_author_apa(author: str) -> str:
    author = re.sub(r"\s+", " ", author.strip())
    if not author:
        return ""
    if "," in author:
        return author
    parts = author.split(" ")
    initials = parts[-1]
    if len(parts) > 1 and re.fullmatch(r"[A-Z]{1,6}", initials):
        surname = " ".join(parts[:-1])
        formatted_initials = " ".join(f"{ch}." for ch in initials)
        return f"{surname}, {formatted_initials}"
    return author


def apa_authors(authors: list[str]) -> str:
    clean = [a.strip() for a in authors if a and a.strip()]
    if not clean:
        return "Autor no identificado"
    clean = [format_author_apa(author) for author in clean]
    if len(clean) == 1:
        return clean[0]
    if len(clean) <= 20:
        return ", ".join(clean[:-1]) + ", & " + clean[-1]
    return ", ".join(clean[:19]) + ", ... " + clean[-1]


def cite_label(item: dict) -> str:
    authors = item.get("authors") or []
    if not authors:
        lead = "Autor no identificado"
    else:
        lead = authors[0].split()[0]
    return f"{lead} et al., {item.get('year', 's.f.')}, DOI: {item['doi']}"


def apa_reference(item: dict) -> str:
    authors = apa_authors(item.get("authors") or [])
    author_part = authors if authors.endswith(".") else f"{authors}."
    year = item.get("year") or "s.f."
    title = sentence_case(item.get("title") or "Titulo no identificado")
    journal = (item.get("journal") or "Publicacion no identificada").rstrip(" .")
    doi = item["doi"]
    return f"{author_part} ({year}). {title}. {journal}. https://doi.org/{doi}"


def bibtex_key(item: dict) -> str:
    authors = item.get("authors") or ["anon"]
    lead = re.sub(r"[^A-Za-z0-9]+", "", authors[0].split()[0]).lower() or "anon"
    year = re.sub(r"[^0-9]+", "", str(item.get("year") or "")) or "nd"
    title_words = re.findall(r"[A-Za-z0-9]+", item.get("title") or "")
    stem = "".join(w.lower() for w in title_words[:3]) or "source"
    return f"{lead}_{stem}_{year}"


def bibtex_escape(text: str) -> str:
    return (text or "").replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def bibtex_entry(item: dict) -> str:
    authors = " and ".join(item.get("authors") or ["Unknown"])
    fields = {
        "title": item.get("title") or "",
        "author": authors,
        "year": item.get("year") or "",
        "journal": item.get("journal") or "",
        "doi": item.get("doi") or "",
        "url": item.get("doi_url") or f"https://doi.org/{item.get('doi')}",
        "pmid": item.get("pmid") or "",
    }
    lines = [f"@article{{{bibtex_key(item)},"]
    for key, value in fields.items():
        if value:
            lines.append(f"  {key} = {{{bibtex_escape(str(value))}}},")
    lines.append("}")
    return "\n".join(lines)


def require_sources() -> list[dict]:
    data = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    by_doi = {normalize_doi(item["doi"]): item for item in data if item.get("doi")}
    missing = [doi for doi in CORE_DOIS if normalize_doi(doi) not in by_doi]
    if missing:
        raise SystemExit("Missing expected DOI entries: " + ", ".join(missing))
    selected = [by_doi[normalize_doi(doi)] for doi in CORE_DOIS]
    for item in selected:
        doi = normalize_doi(item["doi"])
        item["use_note_core"] = USE_OVERRIDES.get(doi, item.get("use_note") or "Fuente core para tesis CCA-AAV.")
    return selected


def render_sources_md(selected: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# FASE 2 - Fuentes core APA7 CCA-AAV",
        "",
        f"Generado: {now}",
        "",
        "Alcance: seleccion curada de fuentes reales con DOI sobre alucinaciones auditivas verbales, fenomenologia de voces, prevalencia de experiencias psicoticas, continuum clinico/no clinico, mecanismos, diferenciales audiologicos/neurologicos e intervenciones.",
        "",
        "Estado de verificacion: cada entrada fue tomada de `00_FUENTES_ACADEMICAS_DOI_VERIFICADAS_2026-06-07.json`, que contiene DOI marcados `crossref_verified=true`; las URLs DOI y PubMed disponibles se conservan en cada ficha.",
        "",
        "Bloqueo de plugin: Zotero local no respondio en `127.0.0.1:23119` durante esta fase; Elicit/life-science pidio reautenticacion. Por eso se entrega salida Zotero-compatible en BibTeX junto con APA7 manual, sin inventar registros.",
        "",
        f"Total core: {len(selected)} fuentes con DOI.",
        "",
        "## Referencias APA7",
        "",
    ]
    for index, item in enumerate(selected, 1):
        lines.extend(
            [
                f"{index}. {apa_reference(item)}",
                f"   - DOI: https://doi.org/{item['doi']}",
                f"   - PMID: {item.get('pmid') or 'n/a'}",
                f"   - PubMed: {item.get('pubmed_url') or 'n/a'}",
                f"   - Tema: {', '.join(item.get('themes') or [])}",
                f"   - Uso en tesis: {item['use_note_core']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Cobertura por eje",
            "",
            "- Prevalencia/continuum: Johns & van Os 2001; van Os et al. 2009; Linscott & van Os 2013; McGrath et al. 2015; Beavan et al. 2011; Maijer et al. 2018.",
            "- Fenomenologia clinica/no clinica: Waters et al. 2012; Laroi et al. 2012; Johns et al. 2014; Daalman et al. 2011.",
            "- Mecanismos y neuroimagen: Badcock & Hugdahl 2012; Alderson-Day et al. 2016/2017; Bohlken et al. 2017; Di Biase et al. 2020; Richards et al. 2021; Corlett et al. 2019.",
            "- Trauma/disociacion: Varese et al. 2012; Pilton et al. 2015; Andrew et al. 2008; McCarthy-Jones 2011.",
            "- Diferencial e intervenciones: Blom 2015; Serino et al. 2014; Marschall et al. 2020; Musiek et al. 2021; Thomas et al. 2014; Slotema et al. 2018.",
        ]
    )
    return "\n".join(lines) + "\n"


def c(selected: list[dict], doi: str) -> str:
    item = next(item for item in selected if normalize_doi(item["doi"]) == normalize_doi(doi))
    return f"({cite_label(item)})"


def render_manuscript(selected: list[dict]) -> str:
    C = lambda doi: c(selected, doi)
    refs = "\n".join(f"- {apa_reference(item)}" for item in selected)
    return f"""# Manuscrito de tesis CCA-AAV M0-M13 v2

Fecha: 2026-06-07

Regla de trazabilidad: las afirmaciones academicas llevan DOI explicito en la misma oracion; las afirmaciones que aun no tienen respaldo verificable quedan marcadas `[POR-VALIDAR]`.

## M0 - Glosario operativo y frontera del objeto

Una alucinacion auditiva verbal (AAV) se trata aqui como experiencia de voz o habla percibida sin fuente externa compartida, y su comparacion entre poblaciones clinicas y no clinicas exige no identificar automaticamente la experiencia con esquizofrenia o psicosis clinica {C("10.1093/schbul/sbs045")}.

El termino CCA se usa en este manuscrito como una hipotesis tecnica y fenomenologica de interfaz acustico-cognitiva, no como diagnostico medico reconocido ni entidad nosologica establecida [POR-VALIDAR].

La tesis separa tres planos: fenomenologia de voces, riesgo o expresion psicotica, y atribuciones personales/forenses sobre origen externo de la experiencia; esta separacion es necesaria porque las revisiones muestran continuidad clinica/no clinica y heterogeneidad mecanistica {C("10.1093/schbul/sbz002")}.

## M1 - Problema de investigacion

Las experiencias psicoticas y las voces pueden observarse fuera de trastornos psicoticos diagnosticados, por lo que una tesis defendible debe explicar prevalencia, necesidad de cuidado y deterioro sin convertir toda voz en patologia {C("10.1016/s0272-7358(01)00103-9")}.

La prevalencia transnacional de experiencias psicoticas en poblacion general adulta muestra que el fenomeno es epidemiologicamente distribuido y no se limita a muestras clinicas {C("10.1001/jamapsychiatry.2015.0575")}.

La pregunta central queda formulada asi: que distingue una AAV no clinica, una AAV con necesidad de cuidado y una hipotesis CCA que requiere validacion tecnica externa [POR-VALIDAR].

## M2 - Diferencial medico, audiologico y neurologico

El diferencial debe incluir perdida auditiva, tinnitus, musicalidad perceptiva y fenomenos por deaferentacion porque la literatura audiologica y neurologica describe alucinaciones auditivas fuera del marco psicotico primario {C("10.1055/s-0041-1722989")}.

El diferencial tambien debe incluir origen epileptico cuando la fenomenologia, temporalidad o hallazgos neurologicos lo sugieran, porque las AAV de origen epileptico estan documentadas clinicamente {C("10.1016/j.yebeh.2013.12.014")}.

La hipotesis CCA no debe sustituir exploracion otorrinolaringologica, audiologica, neurologica o psiquiatrica estandar [POR-VALIDAR].

## M3 - Marco conceptual: continuum, necesidad de cuidado y FPI

El modelo de continuum de psicosis permite situar experiencias subclinicas y clinicas en un espacio compartido sin asumir equivalencia diagnostica directa {C("10.1017/s0033291708003814")}.

Las revisiones conservadoras estiman que las experiencias psicoticas tienen distribucion poblacional medible y que solo una parte progresa hacia presentaciones clinicas o necesidad de cuidado {C("10.1017/s0033291712001626")}.

La diferencia entre voces con y sin necesidad de cuidado debe tratarse como eje clinico central, porque la literatura compara personas con AAV con y sin demanda asistencial {C("10.1093/schbul/sbu005")}.

FPI se usa aqui como marco interno para ordenar fenomenologia, predisposicion, interpretacion y carga funcional, no como constructo clinico validado [POR-VALIDAR].

## M4 - Epidemiologia y prevalencia

La revision de Beavan et al. sobre personas que oyen voces en poblacion general respalda que la voz no es exclusiva del diagnostico psicotico {C("10.3109/09638237.2011.562262")}.

El meta-analisis de AAV a lo largo de la vida permite discutir variacion por edad y desarrollo sin extrapolar linealmente datos adultos a infancia o adolescencia {C("10.1017/s0033291717002367")}.

En infancia media existen estimaciones poblacionales y correlatos de alucinaciones vocales auditivas que obligan a distinguir desarrollo, malestar y persistencia {C("10.1192/bjp.bp.109.065953")}.

En adolescentes, los estudios poblacionales noruegos muestran prevalencia de alucinaciones auditivas y permiten un eje separado para edad escolar y adolescencia {C("10.1111/sjop.12219")}.

La cifra exacta de prevalencia CCA, si se define como fenomeno tecnico externo y no como AAV, permanece sin fuente epidemiologica directa [POR-VALIDAR].

## M5 - Fenomenologia de las AAV

Las voces clinicas y no clinicas comparten rasgos fenomenologicos, pero la comparacion de caracteristicas muestra que contenido, control, malestar, atribucion y deterioro pueden diferenciar trayectorias {C("10.1093/schbul/sbs061")}.

La comparacion fenomenologica entre pacientes con esquizofrenia y no pacientes muestra que similitud subjetiva no equivale automaticamente a misma etiologia o mismo riesgo clinico {C("10.4088/jcp.09m05797yel")}.

Las experiencias culturales de escuchar voces muestran que significado social y respuesta comunitaria pueden modular interpretacion y sufrimiento {C("10.1192/bjp.bp.113.139048")}.

La afirmacion de que CCA pueda producir marcadores fenomenologicos especificos, como latencia fija o patron linguistico externo reproducible, requiere validacion instrumental [POR-VALIDAR].

## M6 - Mecanismos cognitivos y neurobiologicos

Los modelos cognitivos de AVH incluyen monitoreo de fuente, monitoreo propio, sesgos de externalizacion y procesamiento de senal, con evidencia sintetizada en revisiones de grupos psicoticos y no psicoticos {C("10.1016/j.neubiorev.2011.07.010")}.

Las revisiones sobre sesgos de externalizacion y monitoreo de fuente apoyan que algunos errores de atribucion pueden contribuir a experiencias alucinatorias {C("10.1017/s0033291712002760")}.

Los modelos de priors fuertes situan las alucinaciones dentro de inferencia perceptiva predictiva y ayudan a explicar percepciones con alta confianza pese a evidencia sensorial ambigua {C("10.1016/j.tics.2018.12.001")}.

Los estudios de habla ambigua en oyentes de voces no clinicos sugieren que el procesamiento de habla externa puede relacionarse con experiencias de voz {C("10.1093/brain/awx206")}.

La neuroimagen de AAV en pacientes y poblaciones sanas muestra convergencias y limites metodologicos, por lo que no se debe presentar un unico biomarcador como diagnostico suficiente {C("10.1017/s0033291719000205")}.

## M7 - Interfaz tecnica CCA y criterios de validacion

Una hipotesis tecnica CCA solo seria academicamente defendible si produce predicciones medibles, protocolos reproducibles y controles negativos frente a explicaciones audiologicas, neurologicas y psiquiatricas [POR-VALIDAR].

La revision sobre procesamiento de habla externa y AAV justifica usar tareas auditivas, habla ambigua y medidas de procesamiento de senal como analogias experimentales, pero no valida por si misma una fuente externa CCA {C("10.1016/j.neubiorev.2021.09.006")}.

Los registros de smartphone y evaluacion ecologica pueden servir como metodologia de seguimiento temporal de voces, afecto y contexto, pero no prueban causalidad tecnica externa sin instrumentacion independiente {C("10.1093/schizbullopen/sgaa060")}.

Las cifras operativas tipo "70 por ciento", "150 ms", "firma acustica unica" o "patron externo identificable" quedan excluidas del nucleo academico hasta que exista medicion verificable [POR-VALIDAR].

## M8 - Evaluacion clinica y matriz diferencial

La evaluacion debe clasificar presencia de voz, frecuencia, control, malestar, creencias, deterioro, comorbilidad, trauma, disociacion, audicion y signos neurologicos porque las revisiones integran AVH como fenomeno multifactorial {C("10.1111/acps.12531")}.

La asociacion entre trauma infantil y AVH respalda incluir historia traumatica como variable, pero no autoriza inferir causalidad unica en un caso individual {C("10.1017/s0033291712000761")}.

La relacion entre disociacion y voces tiene apoyo de revision y meta-analisis, por lo que debe diferenciarse de psicosis primaria y de hipotesis tecnicas externas {C("10.1016/j.cpr.2015.06.004")}.

Las AAV en trastorno limite de personalidad requieren evaluacion propia porque la literatura revisa fenomenologia y respuesta a antipsicoticos en ese grupo {C("10.3389/fpsyt.2018.00347")}.

## M9 - Intervenciones y evidencia

Las terapias psicologicas para voces tienen un cuerpo de revision que permite discutir objetivos como malestar, relacion con la voz, afrontamiento y funcionamiento {C("10.1093/schbul/sbu037")}.

La evidencia sobre neuroimagen y tratamiento de AVH permite presentar neuromodulacion y dianas cerebrales como areas de investigacion, no como solucion unica garantizada {C("10.1017/s003329171600115x")}.

La evidencia de deafferentacion exige considerar intervenciones auditivas o rehabilitacion cuando la evaluacion encuentre perdida sensorial relevante {C("10.1097/yco.0000000000000586")}.

La tesis no debe recomendar acciones clinicas personalizadas sin evaluacion profesional individual [POR-VALIDAR].

## M10 - Etica, riesgo y separacion SPIA/personal-forense

La parte academica debe evitar atribuir intencionalidad externa, persecucion o autoria tecnica sin evidencia independiente porque los modelos de AAV ya ofrecen explicaciones psicologicas, neurobiologicas, audiologicas y sociales verificables {C("10.1093/schbul/sby110")}.

El material SPIA/personal-forense debe quedar como anexo separado, con cadena de custodia, fecha, fuente, metodo de captura y nivel de corroboracion, porque no pertenece automaticamente al argumento epidemiologico o clinico [POR-VALIDAR].

La proteccion de la persona investigada exige no convertir experiencias subjetivas en acusaciones identificables sin verificacion externa [POR-VALIDAR].

## M11 - Metodos P0-P4

P0 consiste en separar corpus academico, corpus personal y corpus tecnico para evitar mezcla de evidencias de distinta naturaleza [POR-VALIDAR].

P1 consiste en busqueda bibliografica por DOI, PMID, ensayo clinico y revision sistematica, y queda respaldado por el corpus DOI reunido en FASE 2 {C("10.1017/s0033291717002367")}.

P2 consiste en matriz diferencial clinico-audiologico-neurologica usando fuentes sobre audiologia, epilepsia, deaferentacion y fenomenologia clinica {C("10.1055/s-0041-1722989")}.

P3 consiste en protocolo de diario/ecologia temporal para voces, afecto, contexto y carga funcional, inspirado en metodos moviles de evaluacion de AVH {C("10.1093/schizbullopen/sgaa060")}.

P4 consiste en protocolo CCA de validacion instrumental con controles, replicacion y analisis externo, que permanece no validado hasta datos instrumentales [POR-VALIDAR].

## M12 - Discusion y limites

El nucleo defendible de la tesis es que las AAV y experiencias psicoticas existen en un continuum poblacional heterogeneo, y que la necesidad de cuidado depende de malestar, control, deterioro, contexto y factores de riesgo {C("10.1017/s0033291708003814")}.

La tesis debe evitar una equivalencia simple entre severidad y mecanismo porque la continuidad de severidad no implica necesariamente continuidad causal {C("10.1093/schbul/sbz002")}.

La parte CCA puede mantenerse como hipotesis de investigacion si se formula con predicciones falsables y si cada afirmacion tecnica no verificada queda marcada [POR-VALIDAR].

## M13 - Arquitectura editorial y trazabilidad

El manuscrito final debe separar citas DOI, afirmaciones POR-VALIDAR, anexos personales/SPIA y evidencias instrumentales porque la mezcla de niveles probatorios debilita la defendibilidad academica [POR-VALIDAR].

La bibliografia core de FASE 2 contiene mas de 30 DOI y debe convertirse en base Zotero cuando el servicio local responda en `127.0.0.1:23119` [POR-VALIDAR].

El siguiente hito editorial es expandir cada modulo con parrafos de revision sistematica, tablas de prevalencia y matriz de decision clinica sin borrar ni mover respaldos [POR-VALIDAR].

## Afirmaciones bloqueadas o deliberadamente POR-VALIDAR

- CCA como entidad tecnica o clinica establecida [POR-VALIDAR].
- Cifras especificas de latencia, porcentaje de deteccion, firma acustica o causalidad externa [POR-VALIDAR].
- Atribuciones personales/forenses sobre autores, dispositivos o intencionalidad [POR-VALIDAR].
- Recomendaciones clinicas individuales [POR-VALIDAR].
- Prevalencia epidemiologica de CCA como categoria separada de AAV o experiencias psicoticas [POR-VALIDAR].

## Referencias core

{refs}
"""


def main() -> None:
    selected = require_sources()
    FUENTES_DIR.mkdir(parents=True, exist_ok=True)
    TESIS_DIR.mkdir(parents=True, exist_ok=True)

    sources_path = FUENTES_DIR / "00_FUENTES_CORE_APA7_CCA_AAV_2026-06-07.md"
    bib_path = FUENTES_DIR / "00_REFERENCIAS_CORE_CCA_AAV_2026-06-07.bib"
    thesis_path = TESIS_DIR / "MANUSCRITO_TESIS_CCA_AAV_M0_M13_v2_2026-06-07.md"

    sources_path.write_text(render_sources_md(selected), encoding="utf-8", newline="\n")
    bib_path.write_text("\n\n".join(bibtex_entry(item) for item in selected) + "\n", encoding="utf-8", newline="\n")
    thesis_path.write_text(render_manuscript(selected), encoding="utf-8", newline="\n")

    log_line = (
        f"\n\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} - FASE 2/3 Codex\n"
        f"- Generadas {len(selected)} fuentes core APA7 con DOI: {sources_path}\n"
        f"- Generado BibTeX core Zotero-compatible: {bib_path}\n"
        f"- Redactado manuscrito M0-M13 v2 con DOI/POR-VALIDAR: {thesis_path}\n"
        "- Sin borrar, mover ni tocar carpetas de respaldo.\n"
    )
    with LOG_PATH.open("a", encoding="utf-8", newline="\n") as log_file:
        log_file.write(log_line)

    print(f"sources={sources_path}")
    print(f"bibtex={bib_path}")
    print(f"thesis={thesis_path}")
    print(f"count={len(selected)}")


if __name__ == "__main__":
    main()
