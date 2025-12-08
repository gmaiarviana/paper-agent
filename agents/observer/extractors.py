"""
Extratores semanticos do Observador via LLM.

Este modulo contem funcoes que usam LLM para extrair informacoes
semanticas de cada turno da conversa:
- Claims (proposicoes centrais)
- Conceitos (essencias semanticas)
- Proposicoes/Fundamentos (argumentos de suporte com solidez)
- Contradicoes (inconsistencias logicas)
- Open questions (lacunas)

Versao: 2.0 (Epico 11.4 - Migracao para Proposicoes)
Data: 08/12/2025
"""

import logging
import json
from typing import List, Dict, Any, Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from agents.models.proposition import Proposicao

from .prompts import (
    EXTRACT_CLAIMS_PROMPT,
    EXTRACT_CONCEPTS_PROMPT,
    DETECT_CONTRADICTIONS_PROMPT,
    IDENTIFY_GAPS_PROMPT,
    RECOMMENDED_MODEL,
    EXTRACTION_TEMPERATURE,
    MAX_EXTRACTION_TOKENS,
    CONTRADICTION_CONFIDENCE_THRESHOLD
)
from utils.config import invoke_with_retry
from utils.json_parser import extract_json_from_llm_response

logger = logging.getLogger(__name__)


def _get_llm() -> ChatAnthropic:
    """Retorna instancia do LLM para extracao."""
    return ChatAnthropic(
        model=RECOMMENDED_MODEL,
        temperature=EXTRACTION_TEMPERATURE,
        max_tokens=MAX_EXTRACTION_TOKENS
    )


def extract_claims(
    user_input: str,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> List[str]:
    """
    Extrai claims (proposicoes centrais) do turno atual.

    Claims sao afirmacoes centrais que o usuario esta fazendo ou defendendo.
    Sao o "nucleo" do que o usuario quer comunicar.

    Args:
        user_input: Mensagem atual do usuario.
        conversation_history: Historico da conversa (opcional).
        llm: Instancia do LLM (opcional, cria se nao fornecido).

    Returns:
        Lista de claims extraidos (strings).

    Example:
        >>> claims = extract_claims("LLMs aumentam produtividade em 30%")
        >>> print(claims)
        ['LLMs aumentam produtividade em 30%']
    """
    if llm is None:
        llm = _get_llm()

    # Formatar historico
    history_str = ""
    if conversation_history:
        history_lines = []
        for msg in conversation_history[-5:]:  # Ultimas 5 mensagens
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history_lines.append(f"[{role}]: {content}")
        history_str = "\n".join(history_lines)

    # Construir prompt
    prompt = EXTRACT_CLAIMS_PROMPT.format(
        user_input=user_input,
        history=history_str or "(sem historico)"
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_claims")

        # Parse JSON
        data = extract_json_from_llm_response(response.content)
        claims = data.get("claims", [])

        logger.debug(f"Claims extraidos: {claims}")
        return claims[:3]  # Maximo 3 claims

    except Exception as e:
        logger.warning(f"Erro ao extrair claims: {e}")
        return []


def extract_concepts(
    user_input: str,
    llm: Optional[ChatAnthropic] = None
) -> List[str]:
    """
    Extrai conceitos-chave (essencias semanticas) do turno atual.

    Conceitos sao abstracoes reutilizaveis que poderiam aparecer
    em outras discussoes. Ex: "LLMs", "produtividade", "metodologia".

    Args:
        user_input: Mensagem atual do usuario.
        llm: Instancia do LLM (opcional).

    Returns:
        Lista de conceitos extraidos (strings).

    Example:
        >>> concepts = extract_concepts("LLMs aumentam produtividade")
        >>> print(concepts)
        ['LLMs', 'produtividade']
    """
    if llm is None:
        llm = _get_llm()

    prompt = EXTRACT_CONCEPTS_PROMPT.format(user_input=user_input)

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_concepts")

        data = extract_json_from_llm_response(response.content)
        concepts = data.get("concepts", [])

        logger.debug(f"Conceitos extraidos: {concepts}")
        return concepts[:5]  # Maximo 5 conceitos

    except Exception as e:
        logger.warning(f"Erro ao extrair conceitos: {e}")
        return []


def extract_fundamentos(
    claims: List[str],
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> List[Proposicao]:
    """
    Extrai fundamentos (argumentos de suporte) para os claims como Proposicoes.

    Fundamentos sao afirmacoes que sustentam os claims principais.
    Sao a base logica do argumento. Retornados como Proposicao com solidez=None.

    Epico 11.4: Migrado para retornar List[Proposicao] ao inves de List[str].

    Args:
        claims: Lista de claims extraidos.
        conversation_history: Historico da conversa.
        llm: Instancia do LLM (opcional).

    Returns:
        Lista de Proposicao com solidez=None (nao avaliadas).

    Example:
        >>> proposicoes = extract_fundamentos(
        ...     ["LLMs aumentam produtividade"],
        ...     conversation_history
        ... )
        >>> print(proposicoes[0].texto)
        'Equipes usam LLMs para desenvolvimento'
        >>> print(proposicoes[0].solidez)
        None
    """
    if not claims:
        return []

    if llm is None:
        llm = _get_llm()

    # Formatar historico
    history_str = ""
    if conversation_history:
        history_lines = []
        for msg in conversation_history[-5:]:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history_lines.append(f"[{role}]: {content}")
        history_str = "\n".join(history_lines)

    # Prompt para extrair fundamentos
    prompt = f"""Analise os claims e o historico para identificar fundamentos (argumentos de suporte).

Fundamentos sao afirmacoes que:
- Sustentam logicamente os claims
- Sao assumidas como verdadeiras
- Formam a base do argumento

CLAIMS:
{json.dumps(claims, ensure_ascii=False)}

HISTORICO:
{history_str or "(sem historico)"}

RETORNE APENAS JSON:
{{
    "fundamentos": [
        "fundamento 1",
        "fundamento 2"
    ]
}}

REGRAS:
- Extraia apenas fundamentos explicitos ou fortemente implicitos
- Maximo de 3 fundamentos
- Se nao houver fundamentos claros, retorne lista vazia
"""

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_fundamentos")

        data = extract_json_from_llm_response(response.content)
        fundamentos_text = data.get("fundamentos", [])

        # Converter strings para Proposicao com solidez=None
        proposicoes = [
            Proposicao.from_text(texto=f, solidez=None)
            for f in fundamentos_text[:3]
        ]

        logger.debug(f"Proposicoes extraidas: {len(proposicoes)}")
        return proposicoes

    except Exception as e:
        logger.warning(f"Erro ao extrair fundamentos: {e}")
        return []


def detect_contradictions(
    claims: List[str],
    fundamentos: Optional[List[str]] = None,
    llm: Optional[ChatAnthropic] = None
) -> List[Dict[str, Any]]:
    """
    Detecta contradicoes logicas entre claims e fundamentos.

    Contradicao ocorre quando dois claims sao mutuamente exclusivos
    ou um nega diretamente outro.

    Args:
        claims: Lista de claims extraidos.
        fundamentos: Lista de fundamentos (opcional).
        llm: Instancia do LLM (opcional).

    Returns:
        Lista de contradicoes detectadas. Cada contradicao tem:
        - claim_a: Primeiro claim
        - claim_b: Segundo claim
        - explanation: Por que sao contraditorios
        - confidence: Confianca da deteccao (0-1)

    Example:
        >>> contradictions = detect_contradictions([
        ...     "LLMs sao rapidos",
        ...     "Velocidade nao importa"
        ... ])
        >>> print(contradictions)
        [{'claim_a': 'LLMs sao rapidos', 'claim_b': 'Velocidade nao importa', ...}]
    """
    # Precisa de pelo menos 2 claims para detectar contradicao
    all_claims = claims.copy()
    if fundamentos:
        all_claims.extend(fundamentos)

    if len(all_claims) < 2:
        return []

    if llm is None:
        llm = _get_llm()

    prompt = DETECT_CONTRADICTIONS_PROMPT.format(
        claims=json.dumps(all_claims, ensure_ascii=False)
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_contradictions")

        data = extract_json_from_llm_response(response.content)
        contradictions = data.get("contradictions", [])

        # Filtrar por threshold de confianca
        filtered = [
            c for c in contradictions
            if c.get("confidence", 0) >= CONTRADICTION_CONFIDENCE_THRESHOLD
        ]

        logger.debug(f"Contradicoes detectadas: {len(filtered)}")
        return filtered

    except Exception as e:
        logger.warning(f"Erro ao detectar contradicoes: {e}")
        return []


def identify_open_questions(
    claims: List[str],
    fundamentos: Optional[List[str]] = None,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> List[str]:
    """
    Identifica open questions (lacunas) no raciocinio.

    Lacunas sao aspectos mencionados mas nao desenvolvidos,
    ou perguntas que surgem naturalmente dos claims.

    Args:
        claims: Lista de claims extraidos.
        fundamentos: Lista de fundamentos (opcional).
        conversation_history: Historico da conversa.
        llm: Instancia do LLM (opcional).

    Returns:
        Lista de questoes abertas (strings).

    Example:
        >>> questions = identify_open_questions(
        ...     ["LLMs aumentam produtividade"]
        ... )
        >>> print(questions)
        ['Como medir produtividade?', 'Qual baseline de comparacao?']
    """
    if not claims:
        return []

    if llm is None:
        llm = _get_llm()

    # Formatar historico
    history_str = ""
    if conversation_history:
        history_lines = []
        for msg in conversation_history[-5:]:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history_lines.append(f"[{role}]: {content}")
        history_str = "\n".join(history_lines)

    # Combinar claims e fundamentos
    all_claims = claims.copy()
    if fundamentos:
        all_claims.extend(fundamentos)

    prompt = IDENTIFY_GAPS_PROMPT.format(
        claims=json.dumps(all_claims, ensure_ascii=False),
        history=history_str or "(sem historico)"
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_gaps")

        data = extract_json_from_llm_response(response.content)
        questions = data.get("open_questions", [])

        logger.debug(f"Open questions identificadas: {questions}")
        return questions[:3]  # Maximo 3 questoes

    except Exception as e:
        logger.warning(f"Erro ao identificar open questions: {e}")
        return []


def extract_all(
    user_input: str,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> Dict[str, Any]:
    """
    Extrai todas as informacoes semanticas de um turno em uma unica chamada.

    Esta funcao combina todos os extratores em uma unica chamada LLM
    para eficiencia. Retorna um dicionario com todos os campos extraidos.

    Epico 11.4: Agora retorna 'proposicoes' como List[Proposicao] ao inves
    de 'fundamentos' como List[str].

    Args:
        user_input: Mensagem atual do usuario.
        conversation_history: Historico da conversa.
        llm: Instancia do LLM (opcional).

    Returns:
        Dicionario com:
        - claims: Lista de claims (strings)
        - concepts: Lista de conceitos (strings)
        - proposicoes: Lista de Proposicao com solidez=None
        - contradictions: Lista de contradicoes (dicts)
        - open_questions: Lista de questoes abertas (strings)

    Example:
        >>> result = extract_all("LLMs aumentam produtividade em 30%")
        >>> print(result['claims'])
        ['LLMs aumentam produtividade em 30%']
        >>> print(result['proposicoes'][0].texto)
        'Equipes usam LLMs'
    """
    if llm is None:
        llm = _get_llm()

    # Formatar historico
    history_str = ""
    if conversation_history:
        history_lines = []
        for msg in conversation_history[-5:]:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history_lines.append(f"[{role}]: {content}")
        history_str = "\n".join(history_lines)

    # Prompt unificado para eficiencia
    prompt = f"""Voce e o Observador (Mente Analitica) do sistema Paper Agent.

Analise o input do usuario e extraia informacoes semanticas completas.

INPUT DO USUARIO:
{user_input}

HISTORICO DA CONVERSA:
{history_str or "(sem historico)"}

EXTRAIA e RETORNE APENAS JSON no formato:
{{
    "claims": [
        "proposicao central 1",
        "proposicao central 2"
    ],
    "concepts": [
        "conceito-chave 1",
        "conceito-chave 2"
    ],
    "proposicoes": [
        "fundamento/argumento de suporte 1",
        "fundamento/argumento de suporte 2"
    ],
    "contradictions": [
        {{
            "claim_a": "primeiro claim",
            "claim_b": "segundo claim",
            "explanation": "por que sao contraditorios",
            "confidence": 0.85
        }}
    ],
    "open_questions": [
        "questao aberta 1",
        "questao aberta 2"
    ],
    "reasoning": "Breve explicacao da analise"
}}

REGRAS:
- Claims: proposicoes centrais que o usuario defende (max 3)
- Concepts: abstracoes reutilizaveis (max 5)
- Proposicoes: fundamentos que sustentam os claims (max 3)
- Contradictions: apenas se confianca >= 0.80
- Open questions: lacunas relevantes (max 3)
- Se nao houver itens em alguma categoria, retorne lista vazia
"""

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="observer_extract_all")

        data = extract_json_from_llm_response(response.content)

        # Extrair fundamentos/proposicoes do JSON (campo pode ser 'proposicoes' ou 'fundamentos')
        fundamentos_text = data.get("proposicoes", data.get("fundamentos", []))[:3]

        # Converter strings para Proposicao com solidez=None
        proposicoes = [
            Proposicao.from_text(texto=f, solidez=None)
            for f in fundamentos_text
        ]

        # Extrair e validar cada campo
        result = {
            "claims": data.get("claims", [])[:3],
            "concepts": data.get("concepts", [])[:5],
            "proposicoes": proposicoes,
            "contradictions": [
                c for c in data.get("contradictions", [])
                if c.get("confidence", 0) >= CONTRADICTION_CONFIDENCE_THRESHOLD
            ],
            "open_questions": data.get("open_questions", [])[:3]
        }

        logger.info(
            f"Extracao completa: {len(result['claims'])} claims, "
            f"{len(result['concepts'])} conceitos, "
            f"{len(result['proposicoes'])} proposicoes, "
            f"{len(result['contradictions'])} contradicoes, "
            f"{len(result['open_questions'])} questoes"
        )

        return result

    except Exception as e:
        logger.error(f"Erro na extracao completa: {e}")
        return {
            "claims": [],
            "concepts": [],
            "proposicoes": [],
            "contradictions": [],
            "open_questions": []
        }
