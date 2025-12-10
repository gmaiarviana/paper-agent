"""
Calculo de metricas do Observador via LLM.

Este modulo contem funcoes que usam LLM para avaliar a qualidade
do argumento em construcao de forma NAO-DETERMINISTICA:
- Solidez: quao bem fundamentado esta o argumento (via LLM)
- Completude: quanto do argumento esta desenvolvido (via LLM)
- Maturidade: se o argumento esta pronto para snapshot (via LLM)

FILOSOFIA:
- Sistema NAO usa formulas deterministicas
- Sistema avalia CONTEXTO e QUALIDADE, nao apenas conta elementos
- Proposicoes tem SOLIDEZ (nao sao "verdadeiras" ou "falsas")
- Sistema mapeia SUSTENTACAO, nao julga verdade

"""

import logging
import json
from typing import List, Dict, Any, Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from .prompts import (
    EVALUATE_SOLIDEZ_PROMPT,
    EVALUATE_COMPLETUDE_PROMPT,
    EVALUATE_MATURITY_PROMPT,
    RECOMMENDED_MODEL,
    METRICS_TEMPERATURE,
    MAX_METRICS_TOKENS
)
from utils.config import invoke_with_retry, create_anthropic_client
from utils.json_parser import extract_json_from_llm_response

logger = logging.getLogger(__name__)

def _get_metrics_llm() -> ChatAnthropic:
    """
    Retorna instancia do LLM para avaliacao de metricas.

    Usa temperature > 0 para permitir variacao contextual
    (nao-determinismo controlado).
    """
    return create_anthropic_client(
        model=RECOMMENDED_MODEL,
        temperature=METRICS_TEMPERATURE,
        max_tokens=MAX_METRICS_TOKENS
    )

def _extract_proposicoes_texts(proposicoes: List[Dict[str, Any]]) -> List[str]:
    """
    Extrai textos de uma lista de proposicoes (dicts ou objetos).

    Helper para converter proposicoes para lista de strings para prompts.

    Args:
        proposicoes: Lista de dicts com campo 'texto' ou objetos Proposicao.

    Returns:
        Lista de strings com os textos das proposicoes.
    """
    texts = []
    for p in proposicoes:
        if isinstance(p, dict):
            texts.append(p.get("texto", str(p)))
        elif hasattr(p, "texto"):
            texts.append(p.texto)
        else:
            texts.append(str(p))
    return texts

def _extract_proposicoes_with_solidez(proposicoes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extrai proposicoes com texto e solidez para analise.

    Helper para formatar proposicoes para prompts mostrando solidez quando avaliada.

    Args:
        proposicoes: Lista de dicts com campos 'texto' e 'solidez'.

    Returns:
        Lista de dicts formatados para prompt.
    """
    formatted = []
    for p in proposicoes:
        if isinstance(p, dict):
            texto = p.get("texto", str(p))
            solidez = p.get("solidez")
        elif hasattr(p, "texto"):
            texto = p.texto
            solidez = getattr(p, "solidez", None)
        else:
            texto = str(p)
            solidez = None

        formatted.append({
            "texto": texto,
            "solidez": solidez if solidez is not None else "nao avaliada"
        })
    return formatted

def calculate_solidez(
    claim: str,
    proposicoes: List[Dict[str, Any]],
    contradictions: List[Dict[str, Any]],
    solid_grounds: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> Dict[str, Any]:
    """
    Avalia solidez do argumento via LLM (0-1).

    Epico 11.4: Recebe proposicoes unificadas ao inves de fundamentos/assumptions.

    Solidez mede QUAO BEM FUNDAMENTADO esta o argumento.
    Diferente de contagem deterministica, analisa QUALIDADE
    da sustentacao em contexto.

    Args:
        claim: Afirmacao central do argumento.
        proposicoes: Lista de proposicoes (dicts com 'texto' e 'solidez').
        contradictions: Lista de contradicoes detectadas.
        solid_grounds: Lista de evidencias bibliograficas (opcional).
        llm: Instancia do LLM (opcional, cria se nao fornecido).

    Returns:
        Dict com:
        - solidez: float (0-1)
        - analysis: str explicando avaliacao
        - strengths: List[str] pontos fortes
        - weaknesses: List[str] pontos fracos
        - critical_gaps: List[str] lacunas criticas

    Example:
        >>> result = calculate_solidez(
        ...     claim="LLMs aumentam produtividade em 30%",
        ...     proposicoes=[
        ...         {"texto": "Equipes usam LLMs", "solidez": 0.8},
        ...         {"texto": "Qualidade nao e afetada", "solidez": None}
        ...     ],
        ...     contradictions=[]
        ... )
        >>> print(f"Solidez: {result['solidez']:.0%}")
        Solidez: 45%
    """
    if llm is None:
        llm = _get_metrics_llm()

    # Formatar proposicoes com solidez para o prompt
    proposicoes_formatted = _extract_proposicoes_with_solidez(proposicoes)
    proposicoes_str = json.dumps(proposicoes_formatted, ensure_ascii=False) if proposicoes_formatted else "(nenhuma)"
    contradictions_str = json.dumps(contradictions, ensure_ascii=False) if contradictions else "(nenhuma)"
    solid_grounds_str = json.dumps(solid_grounds, ensure_ascii=False) if solid_grounds else "(nenhuma)"

    # Construir prompt (adaptado para proposicoes)
    prompt = EVALUATE_SOLIDEZ_PROMPT.format(
        claim=claim or "(claim nao definido)",
        fundamentos=proposicoes_str,  # Proposicoes unificadas (substitui premises/assumptions)
        contradictions=contradictions_str,
        solid_grounds=solid_grounds_str
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_solidez")

        # Parse JSON
        data = extract_json_from_llm_response(response.content)

        # Extrair e validar resultado
        solidez = float(data.get("solidez", 0.0))
        solidez = max(0.0, min(1.0, solidez))  # Garantir range 0-1

        result = {
            "solidez": solidez,
            "analysis": data.get("analysis", "Analise nao disponivel"),
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "critical_gaps": data.get("critical_gaps", [])
        }

        logger.info(
            f"Solidez avaliada via LLM: {solidez:.2f} "
            f"(strengths={len(result['strengths'])}, "
            f"weaknesses={len(result['weaknesses'])})"
        )

        return result

    except Exception as e:
        logger.error(f"Erro ao avaliar solidez via LLM: {e}")
        # Retorna avaliacao conservadora em caso de erro
        return {
            "solidez": 0.1,
            "analysis": f"Erro na avaliacao: {str(e)}",
            "strengths": [],
            "weaknesses": ["Avaliacao nao concluida"],
            "critical_gaps": ["Erro no processamento LLM"]
        }

def calculate_completude(
    claims: List[str],
    proposicoes: List[Dict[str, Any]],
    open_questions: List[str],
    context: Optional[Dict[str, Any]] = None,
    llm: Optional[ChatAnthropic] = None
) -> Dict[str, Any]:
    """
    Avalia completude do argumento via LLM (0-1).

    Epico 11.4: Recebe proposicoes unificadas ao inves de fundamentos.

    Completude mede QUANTO do argumento esta DESENVOLVIDO.
    Analisa estrutura, articulacao e cobertura do raciocinio.

    Args:
        claims: Lista de claims extraidos.
        proposicoes: Lista de proposicoes (dicts com 'texto' e 'solidez').
        open_questions: Lista de questoes abertas.
        context: Contexto do argumento (opcional).
        llm: Instancia do LLM (opcional).

    Returns:
        Dict com:
        - completude: float (0-1)
        - analysis: str explicando avaliacao
        - developed_aspects: List[str] aspectos desenvolvidos
        - missing_aspects: List[str] aspectos faltantes
        - next_steps_suggested: List[str] proximos passos

    Example:
        >>> result = calculate_completude(
        ...     claims=["LLMs aumentam produtividade"],
        ...     proposicoes=[{"texto": "Equipes usam LLMs", "solidez": 0.8}],
        ...     open_questions=["Como medir?", "Qual baseline?"]
        ... )
        >>> print(f"Completude: {result['completude']:.0%}")
        Completude: 35%
    """
    if llm is None:
        llm = _get_metrics_llm()

    # Formatar dados para o prompt
    claims_str = json.dumps(claims, ensure_ascii=False) if claims else "(nenhum)"
    proposicoes_texts = _extract_proposicoes_texts(proposicoes)
    proposicoes_str = json.dumps(proposicoes_texts, ensure_ascii=False) if proposicoes_texts else "(nenhum)"
    questions_str = json.dumps(open_questions, ensure_ascii=False) if open_questions else "(nenhuma)"
    context_str = json.dumps(context, ensure_ascii=False) if context else "(nao definido)"

    # Construir prompt
    prompt = EVALUATE_COMPLETUDE_PROMPT.format(
        claims=claims_str,
        fundamentos=proposicoes_str,  # Usar mesmo placeholder para compatibilidade
        open_questions=questions_str,
        context=context_str
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_completude")

        # Parse JSON
        data = extract_json_from_llm_response(response.content)

        # Extrair e validar resultado
        completude = float(data.get("completude", 0.0))
        completude = max(0.0, min(1.0, completude))  # Garantir range 0-1

        result = {
            "completude": completude,
            "analysis": data.get("analysis", "Analise nao disponivel"),
            "developed_aspects": data.get("developed_aspects", []),
            "missing_aspects": data.get("missing_aspects", []),
            "next_steps_suggested": data.get("next_steps_suggested", [])
        }

        logger.info(
            f"Completude avaliada via LLM: {completude:.2f} "
            f"(developed={len(result['developed_aspects'])}, "
            f"missing={len(result['missing_aspects'])})"
        )

        return result

    except Exception as e:
        logger.error(f"Erro ao avaliar completude via LLM: {e}")
        # Retorna avaliacao conservadora em caso de erro
        return {
            "completude": 0.1,
            "analysis": f"Erro na avaliacao: {str(e)}",
            "developed_aspects": [],
            "missing_aspects": ["Avaliacao nao concluida"],
            "next_steps_suggested": ["Resolver erro no processamento"]
        }

def calculate_metrics(
    claim: str,
    claims: List[str],
    proposicoes: List[Dict[str, Any]],
    open_questions: List[str],
    contradictions: List[Dict[str, Any]],
    context: Optional[Dict[str, Any]] = None,
    solid_grounds: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> Dict[str, Any]:
    """
    Calcula todas as metricas do CognitiveModel via LLM.

    Epico 11.4: Recebe proposicoes unificadas ao inves de fundamentos/assumptions.

    Funcao de conveniencia que avalia solidez e completude
    em chamadas LLM separadas para analise mais precisa.

    Args:
        claim: Afirmacao central.
        claims: Lista de claims extraidos.
        proposicoes: Lista de proposicoes (dicts com 'texto' e 'solidez').
        open_questions: Lista de questoes abertas.
        contradictions: Lista de contradicoes.
        context: Contexto do argumento.
        solid_grounds: Evidencias bibliograficas.
        llm: Instancia do LLM (opcional).

    Returns:
        Dict com:
        - solidez: float (0-1)
        - completude: float (0-1)
        - solidez_details: Dict com analise detalhada
        - completude_details: Dict com analise detalhada

    Example:
        >>> metrics = calculate_metrics(
        ...     claim="LLMs aumentam produtividade",
        ...     claims=["LLMs aumentam produtividade"],
        ...     proposicoes=[{"texto": "Equipes usam LLMs", "solidez": 0.8}],
        ...     open_questions=["Como medir?"],
        ...     contradictions=[]
        ... )
        >>> print(f"Solidez: {metrics['solidez']:.0%}")
        Solidez: 40%
    """
    if llm is None:
        llm = _get_metrics_llm()

    # Avaliar solidez
    solidez_result = calculate_solidez(
        claim=claim,
        proposicoes=proposicoes,
        contradictions=contradictions,
        solid_grounds=solid_grounds,
        llm=llm
    )

    # Avaliar completude
    completude_result = calculate_completude(
        claims=claims,
        proposicoes=proposicoes,
        open_questions=open_questions,
        context=context,
        llm=llm
    )

    return {
        "solidez": solidez_result["solidez"],
        "completude": completude_result["completude"],
        "solidez_details": solidez_result,
        "completude_details": completude_result
    }

def evaluate_maturity(
    solidez: float,
    completude: float,
    open_questions: List[str],
    contradictions: List[Dict[str, Any]],
    claims: Optional[List[str]] = None,
    proposicoes: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> Dict[str, Any]:
    """
    Avalia maturidade do argumento para potencial snapshot via LLM.

    Epico 11.4: Recebe proposicoes unificadas ao inves de fundamentos.

    Determina contextualmente se o argumento esta maduro o suficiente
    para criar um snapshot (persisti-lo como marco evolutivo).

    Diferente de thresholds rigidos, usa analise contextual LLM.

    Args:
        solidez: Solidez calculada (0-1).
        completude: Completude calculada (0-1).
        open_questions: Lista de questoes abertas.
        contradictions: Lista de contradicoes.
        claims: Lista de claims (opcional).
        proposicoes: Lista de proposicoes (dicts com 'texto' e 'solidez').
        llm: Instancia do LLM (opcional).

    Returns:
        Dict com:
        - is_mature: bool indicando se esta maduro
        - confidence: float indicando confianca (0-1)
        - reason: str explicando a avaliacao contextual
        - blocking_issues: List[str] questoes bloqueadoras
        - recommendation: str recomendacao de acao

    Example:
        >>> result = evaluate_maturity(
        ...     solidez=0.65,
        ...     completude=0.70,
        ...     open_questions=["Detalhe menor?"],
        ...     contradictions=[],
        ...     claims=["LLMs aumentam produtividade"],
        ...     proposicoes=[{"texto": "Equipes usam LLMs", "solidez": 0.8}]
        ... )
        >>> print(f"Maduro: {result['is_mature']}")
        Maduro: True
    """
    if llm is None:
        llm = _get_metrics_llm()

    # Formatar dados para o prompt
    questions_str = json.dumps(open_questions, ensure_ascii=False) if open_questions else "(nenhuma)"
    contradictions_str = json.dumps(contradictions, ensure_ascii=False) if contradictions else "(nenhuma)"
    claims_str = json.dumps(claims, ensure_ascii=False) if claims else "(nenhum)"

    # Extrair textos das proposicoes para o prompt
    proposicoes_texts = _extract_proposicoes_texts(proposicoes or [])
    proposicoes_str = json.dumps(proposicoes_texts, ensure_ascii=False) if proposicoes_texts else "(nenhum)"

    # Construir prompt
    prompt = EVALUATE_MATURITY_PROMPT.format(
        solidez=f"{solidez:.2f}",
        completude=f"{completude:.2f}",
        open_questions=questions_str,
        contradictions=contradictions_str,
        claims=claims_str,
        fundamentos=proposicoes_str  # Usar mesmo placeholder para compatibilidade
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_maturity")

        # Parse JSON
        data = extract_json_from_llm_response(response.content)

        # Extrair resultado
        result = {
            "is_mature": data.get("is_mature", False),
            "confidence": float(data.get("confidence", 0.5)),
            "reason": data.get("reason", "Avaliacao nao disponivel"),
            "blocking_issues": data.get("blocking_issues", []),
            "recommendation": data.get("recommendation", "Continuar desenvolvimento")
        }

        # Garantir confidence no range 0-1
        result["confidence"] = max(0.0, min(1.0, result["confidence"]))

        logger.info(
            f"Maturidade avaliada via LLM: is_mature={result['is_mature']}, "
            f"confidence={result['confidence']:.2f}"
        )

        return result

    except Exception as e:
        logger.error(f"Erro ao avaliar maturidade via LLM: {e}")
        # Retorna avaliacao conservadora em caso de erro
        return {
            "is_mature": False,
            "confidence": 0.3,
            "reason": f"Erro na avaliacao: {str(e)}",
            "blocking_issues": ["Erro no processamento LLM"],
            "recommendation": "Resolver erro antes de continuar"
        }
