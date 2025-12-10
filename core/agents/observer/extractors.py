"""
Extratores semanticos do Observador via LLM.

Este modulo contem funcoes que usam LLM para extrair informacoes
semanticas de cada turno da conversa:
- Claims (proposicoes centrais)
- Conceitos (essencias semanticas)
- Proposicoes/Fundamentos (argumentos de suporte com solidez)
- Contradicoes (inconsistencias logicas)
- Open questions (lacunas)

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
    VARIATION_DETECTION_PROMPT,
    CLARITY_EVALUATION_PROMPT,
    RECOMMENDED_MODEL,
    EXTRACTION_TEMPERATURE,
    MAX_EXTRACTION_TOKENS,
    CONTRADICTION_CONFIDENCE_THRESHOLD
)
from core.utils.config import invoke_with_retry, create_anthropic_client
from core.utils.json_parser import extract_json_from_llm_response

logger = logging.getLogger(__name__)

def _get_llm() -> ChatAnthropic:
    """Retorna instancia do LLM para extracao."""
    return create_anthropic_client(
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

def detect_variation(
    previous_text: str,
    new_text: str,
    cognitive_model: Optional[Dict[str, Any]] = None,
    llm: Optional[ChatAnthropic] = None
) -> Dict[str, Any]:
    """
    Detecta se mudanca entre textos e variacao ou mudanca real (Epico 13.1).

    Esta funcao analisa contextualmente dois textos para determinar se
    representam a mesma essencia (variacao) ou uma mudanca de foco real.

    IMPORTANTE: Esta funcao e DESCRITIVA - retorna analise contextual
    sem thresholds fixos. O Orquestrador decide como agir baseado na analise.

    Filosofia (Epico 13):
    - Analise 100% contextual via LLM
    - Sem thresholds numericos (0.8, 0.3, etc.)
    - Observer detecta; Orchestrator decide

    Args:
        previous_text: Texto/claim anterior.
        new_text: Texto/claim novo.
        cognitive_model: CognitiveModel atual para contexto (opcional).
        llm: Instancia do LLM (opcional, cria se nao fornecido).

    Returns:
        Dict com analise contextual:
        - analysis: Explicacao natural da relacao entre textos
        - classification: "variation" ou "real_change"
        - essence_previous: Nucleo semantico do texto anterior
        - essence_new: Nucleo semantico do texto novo
        - shared_concepts: Conceitos mantidos
        - new_concepts: Conceitos novos introduzidos
        - reasoning: Justificativa da classificacao

    Example:
        >>> result = detect_variation(
        ...     previous_text="LLMs aumentam produtividade",
        ...     new_text="LLMs aumentam produtividade em 30%",
        ...     cognitive_model={}
        ... )
        >>> print(result['classification'])
        'variation'
        >>> print(result['analysis'])
        'Ambos focam em LLMs e produtividade, novo texto apenas quantifica'

        >>> result = detect_variation(
        ...     previous_text="LLMs aumentam produtividade",
        ...     new_text="Bugs sao causados por falta de testes"
        ... )
        >>> print(result['classification'])
        'real_change'

    Notes:
        - Versao 1.0 (Epico 13.1): Implementacao inicial
        - Observer detecta APENAS; NAO decide interromper
    """
    if llm is None:
        llm = _get_llm()

    # Preparar cognitive_model como string para o prompt
    cm_str = "(modelo vazio)"
    if cognitive_model:
        cm_parts = []
        if cognitive_model.get("claim"):
            cm_parts.append(f"Claim atual: {cognitive_model['claim']}")
        if cognitive_model.get("proposicoes"):
            props = cognitive_model["proposicoes"][:3]  # Limitar a 3
            props_text = [
                p.get("texto", "") if isinstance(p, dict) else str(p)
                for p in props
            ]
            cm_parts.append(f"Proposicoes: {props_text}")
        if cognitive_model.get("concepts_detected"):
            concepts = cognitive_model["concepts_detected"][:5]
            cm_parts.append(f"Conceitos: {concepts}")
        cm_str = "\n".join(cm_parts) if cm_parts else "(modelo vazio)"

    # Construir prompt
    prompt = VARIATION_DETECTION_PROMPT.format(
        previous_text=previous_text,
        new_text=new_text,
        cognitive_model=cm_str
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(
            llm=llm,
            messages=messages,
            agent_name="observer_variation_detection"
        )

        # Parse JSON
        data = extract_json_from_llm_response(response.content)

        # Validar campos obrigatorios
        result = {
            "analysis": data.get("analysis", "Analise nao disponivel"),
            "classification": data.get("classification", "variation"),
            "essence_previous": data.get("essence_previous", previous_text[:100]),
            "essence_new": data.get("essence_new", new_text[:100]),
            "shared_concepts": data.get("shared_concepts", []),
            "new_concepts": data.get("new_concepts", []),
            "reasoning": data.get("reasoning", "")
        }

        # Garantir que classification seja um dos valores validos
        if result["classification"] not in ("variation", "real_change"):
            result["classification"] = "variation"

        logger.info(
            f"Variacao detectada: {result['classification']} - "
            f"shared={len(result['shared_concepts'])}, new={len(result['new_concepts'])}"
        )

        return result

    except Exception as e:
        logger.warning(f"Erro ao detectar variacao: {e}")
        # Fallback conservador: assume variacao em caso de erro
        return {
            "analysis": f"Erro na analise: {str(e)}",
            "classification": "variation",
            "essence_previous": previous_text[:100] if previous_text else "",
            "essence_new": new_text[:100] if new_text else "",
            "shared_concepts": [],
            "new_concepts": [],
            "reasoning": "Fallback devido a erro - assumindo variacao"
        }

def evaluate_conversation_clarity(
    cognitive_model: Dict[str, Any],
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    llm: Optional[ChatAnthropic] = None
) -> Dict[str, Any]:
    """
    Avalia a clareza da conversa atual (Epico 13.2).

    Esta funcao analisa o CognitiveModel e historico para determinar
    se a conversa esta fluindo bem ou precisa de um checkpoint.

    Escala de clareza (do melhor ao pior):
    - "cristalina": Conversa excepcional, claim bem definido, coerente
    - "clara": Conversa boa, pode continuar
    - "nebulosa": Ha pontos que merecem esclarecimento
    - "confusa": Precisa parar e clarificar

    Filosofia (Epico 13):
    - Analise contextual via LLM
    - Indice numerico (1-5) para parametrizacao
    - Observer avalia; Orchestrator decide se/como intervir

    Args:
        cognitive_model: CognitiveModel atual com claim, proposicoes,
            contradictions, open_questions, concepts_detected.
        conversation_history: Historico recente da conversa (opcional).
        llm: Instancia do LLM (opcional, cria se nao fornecido).

    Returns:
        Dict com avaliacao de clareza:
        - clarity_level: str - "cristalina", "clara", "nebulosa" ou "confusa"
        - clarity_score: int - 1 a 5 (5=cristalina, 1=confusa)
        - description: str - Descricao de como a conversa esta fluindo
        - needs_checkpoint: bool - Se precisa parar e esclarecer
        - factors: dict - Fatores que influenciam a clareza
            - claim_definition: "bem definido", "parcial" ou "vago"
            - coherence: "alta", "media" ou "baixa"
            - direction_stability: "estavel", "algumas mudancas" ou "instavel"
        - suggestion: str|None - Sugestao para melhorar clareza

    Example:
        >>> result = evaluate_conversation_clarity(
        ...     cognitive_model={
        ...         "claim": "LLMs aumentam produtividade em 30%",
        ...         "proposicoes": [{"texto": "Estudos mostram ganho", "solidez": 0.8}]
        ...     }
        ... )
        >>> print(result['clarity_level'])
        'clara'
        >>> print(result['needs_checkpoint'])
        False

        >>> result = evaluate_conversation_clarity(
        ...     cognitive_model={"claim": "", "proposicoes": []}
        ... )
        >>> print(result['clarity_level'])
        'confusa'
        >>> print(result['needs_checkpoint'])
        True

    Notes:
        - Versao 2.0 (Epico 13.2): Substituiu calculate_confusion_level
        - Foco em "clareza" ao inves de "confusao"
        - Observer avalia APENAS; NAO decide interromper
    """
    if llm is None:
        llm = _get_llm()

    # Extrair dados do CognitiveModel
    claim = cognitive_model.get("claim", "")
    proposicoes = cognitive_model.get("proposicoes", [])
    contradictions = cognitive_model.get("contradictions", [])
    open_questions = cognitive_model.get("open_questions", [])
    concepts = cognitive_model.get("concepts_detected", [])

    # Formatar proposicoes para o prompt
    props_str = "(nenhuma)"
    if proposicoes:
        props_lines = []
        for i, p in enumerate(proposicoes[:5], 1):  # Limitar a 5
            if isinstance(p, dict):
                texto = p.get("texto", "")
                solidez = p.get("solidez")
                solidez_str = f" (solidez: {solidez:.0%})" if solidez is not None else " (solidez: nao avaliada)"
                props_lines.append(f"{i}. {texto}{solidez_str}")
            else:
                props_lines.append(f"{i}. {str(p)}")
        props_str = "\n".join(props_lines)

    # Formatar contradicoes
    contradictions_str = "(nenhuma)"
    if contradictions:
        contr_lines = []
        for i, c in enumerate(contradictions[:3], 1):  # Limitar a 3
            desc = c.get("description", str(c)) if isinstance(c, dict) else str(c)
            contr_lines.append(f"{i}. {desc}")
        contradictions_str = "\n".join(contr_lines)

    # Formatar questoes abertas
    questions_str = "(nenhuma)"
    if open_questions:
        questions_str = "\n".join(f"{i}. {q}" for i, q in enumerate(open_questions[:5], 1))

    # Formatar conceitos
    concepts_str = ", ".join(concepts[:7]) if concepts else "(nenhum)"

    # Formatar historico recente
    history_str = "(sem historico)"
    if conversation_history:
        recent = conversation_history[-4:]  # Ultimas 4 mensagens
        history_lines = []
        for msg in recent:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:200]  # Truncar
            history_lines.append(f"[{role}]: {content}")
        history_str = "\n".join(history_lines)

    # Construir prompt
    prompt = CLARITY_EVALUATION_PROMPT.format(
        claim=claim or "(nenhum claim definido)",
        proposicoes=props_str,
        contradictions=contradictions_str,
        open_questions=questions_str,
        concepts=concepts_str,
        recent_history=history_str
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(
            llm=llm,
            messages=messages,
            agent_name="observer_clarity_evaluation"
        )

        # Parse JSON
        data = extract_json_from_llm_response(response.content)

        # Extrair e validar clarity_level
        clarity_level = data.get("clarity_level", "nebulosa")
        valid_levels = ("cristalina", "clara", "nebulosa", "confusa")
        if clarity_level not in valid_levels:
            clarity_level = "nebulosa"

        # Extrair e validar clarity_score
        clarity_score = data.get("clarity_score", 3)
        if not isinstance(clarity_score, int) or clarity_score < 1 or clarity_score > 5:
            # Inferir score do level
            score_map = {"cristalina": 5, "clara": 4, "nebulosa": 3, "confusa": 1}
            clarity_score = score_map.get(clarity_level, 3)

        # Extrair needs_checkpoint
        needs_checkpoint = data.get("needs_checkpoint", clarity_level in ("nebulosa", "confusa"))

        # Extrair factors com defaults
        factors = data.get("factors", {})
        default_factors = {
            "claim_definition": "parcial",
            "coherence": "media",
            "direction_stability": "algumas mudancas"
        }
        for key, default_value in default_factors.items():
            if key not in factors:
                factors[key] = default_value

        # Validar valores dos factors
        valid_claim_def = ("bem definido", "parcial", "vago")
        valid_coherence = ("alta", "media", "baixa")
        valid_stability = ("estavel", "algumas mudancas", "instavel")

        if factors.get("claim_definition") not in valid_claim_def:
            factors["claim_definition"] = "parcial"
        if factors.get("coherence") not in valid_coherence:
            factors["coherence"] = "media"
        if factors.get("direction_stability") not in valid_stability:
            factors["direction_stability"] = "algumas mudancas"

        # Construir resultado
        result = {
            "clarity_level": clarity_level,
            "clarity_score": clarity_score,
            "description": data.get("description", "Avaliacao de clareza nao disponivel"),
            "needs_checkpoint": bool(needs_checkpoint),
            "factors": factors,
            "suggestion": data.get("suggestion")
        }

        logger.info(
            f"Clareza avaliada: level={result['clarity_level']}, "
            f"score={result['clarity_score']}, "
            f"checkpoint={result['needs_checkpoint']}"
        )

        return result

    except Exception as e:
        logger.warning(f"Erro ao avaliar clareza: {e}")
        # Fallback: assume clareza media (nebulosa)
        return {
            "clarity_level": "nebulosa",
            "clarity_score": 3,
            "description": f"Erro na analise: {str(e)}",
            "needs_checkpoint": True,
            "factors": {
                "claim_definition": "parcial",
                "coherence": "media",
                "direction_stability": "algumas mudancas"
            },
            "suggestion": "Verificar se ha pontos a esclarecer"
        }
