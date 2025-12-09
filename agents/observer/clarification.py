"""
Modulo de clarification (esclarecimento) do Observador.

Este modulo implementa a logica de consultas inteligentes:
- Identificar pontos que precisam esclarecimento
- Sugerir perguntas para contradicoes e gaps
- Decidir timing de intervencao
- Analisar respostas de esclarecimento

Filosofia:
- Observer identifica O QUE precisa esclarecimento
- Orquestrador formula perguntas NATURAIS (nao roboticas)
- Tom de parceiro pensante, nao fiscalizador
- Perguntas ajudam a AVANCAR, nao apenas apontam problemas

Epico 14: Observer - Consultas Inteligentes
Data: 2025-12-09
"""

import logging
import json
from typing import Dict, Any, Optional, List

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from agents.models.clarification import (
    ClarificationNeed,
    ClarificationContext,
    ClarificationTimingDecision,
    ClarificationResponse,
    ClarificationUpdates,
    QuestionSuggestion,
)
from agents.models.proposition import Proposicao

from .clarification_prompts import (
    IDENTIFY_CLARIFICATION_NEEDS_PROMPT,
    CONTRADICTION_QUESTION_PROMPT,
    GAP_QUESTION_PROMPT,
    ANALYZE_CLARIFICATION_RESPONSE_PROMPT,
    TIMING_DECISION_PROMPT,
    CLARIFICATION_MODEL,
    IDENTIFICATION_TEMPERATURE,
    QUESTION_GENERATION_TEMPERATURE,
    RESPONSE_ANALYSIS_TEMPERATURE,
    MAX_IDENTIFICATION_TOKENS,
    MAX_QUESTION_TOKENS,
    MAX_RESPONSE_ANALYSIS_TOKENS,
    MIN_CONTRADICTION_PERSISTENCE_TURNS,
    MIN_TURNS_BETWEEN_QUESTIONS,
)
from utils.config import invoke_with_retry, create_anthropic_client
from utils.json_parser import extract_json_from_llm_response

logger = logging.getLogger(__name__)


def _get_llm(
    temperature: float = IDENTIFICATION_TEMPERATURE,
    max_tokens: int = MAX_IDENTIFICATION_TOKENS
) -> ChatAnthropic:
    """Retorna instancia do LLM para clarification."""
    return create_anthropic_client(
        model=CLARIFICATION_MODEL,
        temperature=temperature,
        max_tokens=max_tokens
    )


def _format_proposicoes(proposicoes: List[Any]) -> str:
    """Formata lista de proposicoes para incluir no prompt."""
    if not proposicoes:
        return "(nenhuma proposicao)"

    lines = []
    for i, p in enumerate(proposicoes, 1):
        if isinstance(p, dict):
            texto = p.get("texto", "")
            solidez = p.get("solidez")
        elif hasattr(p, "texto"):
            texto = p.texto
            solidez = p.solidez if hasattr(p, "solidez") else None
        else:
            texto = str(p)
            solidez = None

        solidez_str = f" (solidez: {solidez:.2f})" if solidez is not None else " (solidez: pendente)"
        lines.append(f"{i}. {texto}{solidez_str}")

    return "\n".join(lines)


def _format_contradictions(contradictions: List[Dict[str, Any]]) -> str:
    """Formata lista de contradicoes para incluir no prompt."""
    if not contradictions:
        return "(nenhuma contradicao)"

    lines = []
    for i, c in enumerate(contradictions, 1):
        desc = c.get("description", c.get("explanation", ""))
        confidence = c.get("confidence", 0)
        lines.append(f"{i}. {desc} (confianca: {confidence:.0%})")

    return "\n".join(lines)


def _format_open_questions(open_questions: List[str]) -> str:
    """Formata lista de questoes abertas para incluir no prompt."""
    if not open_questions:
        return "(nenhuma questao aberta)"

    return "\n".join(f"{i}. {q}" for i, q in enumerate(open_questions, 1))


def _format_history(conversation_history: List[Dict[str, Any]], limit: int = 5) -> str:
    """Formata historico recente para incluir no prompt."""
    if not conversation_history:
        return "(sem historico)"

    lines = []
    for msg in conversation_history[-limit:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")[:200]  # Truncar
        lines.append(f"[{role}]: {content}")

    return "\n".join(lines)


# =============================================================================
# 14.1 - IDENTIFICAR NECESSIDADES DE ESCLARECIMENTO
# =============================================================================

def identify_clarification_needs(
    cognitive_model: Dict[str, Any],
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    turn_number: int = 0,
    llm: Optional[ChatAnthropic] = None
) -> ClarificationNeed:
    """
    Analisa CognitiveModel e identifica pontos que precisam esclarecimento.

    Esta e a funcao principal do sistema de consultas inteligentes. Ela
    analisa o estado atual do argumento e determina se ha algo que
    precisa ser esclarecido com o usuario.

    Tipos de esclarecimento:
    - contradiction: Tensao entre proposicoes
    - gap: Informacao faltante para o claim
    - confusion: Confusao geral detectada
    - direction_change: Mudanca de direcao nao confirmada

    Args:
        cognitive_model: CognitiveModel atual contendo claim, proposicoes,
                        contradictions, open_questions, etc.
        conversation_history: Historico da conversa (opcional).
        turn_number: Numero do turno atual.
        llm: Instancia do LLM (opcional, cria se nao fornecido).

    Returns:
        ClarificationNeed: Objeto descrevendo a necessidade de esclarecimento.

    Example:
        >>> cm = {
        ...     "claim": "LLMs aumentam produtividade",
        ...     "proposicoes": [...],
        ...     "contradictions": [{"description": "X vs Y"}]
        ... }
        >>> need = identify_clarification_needs(cm)
        >>> if need.needs_clarification:
        ...     print(f"Tipo: {need.clarification_type}")
        ...     print(f"Descricao: {need.description}")
    """
    if llm is None:
        llm = _get_llm(
            temperature=IDENTIFICATION_TEMPERATURE,
            max_tokens=MAX_IDENTIFICATION_TOKENS
        )

    # Extrair campos do cognitive_model
    claim = cognitive_model.get("claim", "")
    proposicoes = cognitive_model.get("proposicoes", [])
    contradictions = cognitive_model.get("contradictions", [])
    open_questions = cognitive_model.get("open_questions", [])

    # Construir prompt
    prompt = IDENTIFY_CLARIFICATION_NEEDS_PROMPT.format(
        claim=claim or "(claim nao definido)",
        proposicoes=_format_proposicoes(proposicoes),
        contradictions=_format_contradictions(contradictions),
        open_questions=_format_open_questions(open_questions),
        recent_history=_format_history(conversation_history or [])
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(
            llm=llm,
            messages=messages,
            agent_name="observer_clarification_identify"
        )

        data = extract_json_from_llm_response(response.content)

        # Construir contexto relevante
        relevant_context = ClarificationContext(
            proposicoes=data.get("relevant_context", {}).get("proposicoes", []),
            contradictions=data.get("relevant_context", {}).get("contradictions", []),
            open_questions=data.get("relevant_context", {}).get("open_questions", []),
            claim_excerpt=data.get("relevant_context", {}).get("claim_excerpt")
        )

        # Criar ClarificationNeed
        need = ClarificationNeed(
            needs_clarification=data.get("needs_clarification", False),
            clarification_type=data.get("clarification_type", "confusion"),
            description=data.get("description", "Esclarecimento necessario"),
            relevant_context=relevant_context,
            suggested_approach=data.get("suggested_approach", "Perguntar naturalmente"),
            priority=data.get("priority", "medium"),
            turn_detected=turn_number
        )

        logger.info(
            f"Necessidade identificada: needs={need.needs_clarification}, "
            f"type={need.clarification_type}, priority={need.priority}"
        )

        return need

    except Exception as e:
        logger.warning(f"Erro ao identificar necessidade de esclarecimento: {e}")
        # Fallback: sem necessidade de esclarecimento
        return ClarificationNeed(
            needs_clarification=False,
            clarification_type="confusion",
            description="Erro ao analisar - assumindo sem necessidade",
            suggested_approach="",
            turn_detected=turn_number
        )


# =============================================================================
# 14.3 - PERGUNTA SOBRE CONTRADICAO (TENSAO EPISTEMOLOGICA)
# =============================================================================

def generate_contradiction_question(
    contradiction: Dict[str, Any],
    propositions: List[Any],
    conversation_context: str,
    llm: Optional[ChatAnthropic] = None
) -> QuestionSuggestion:
    """
    Gera sugestao de pergunta para explorar uma contradicao como tensao.

    Importante: Contradicoes nao sao tratadas como ERROS, mas como
    TENSOES EPISTEMOLOGICAS que podem refletir contextos diferentes.

    Args:
        contradiction: Dict com descricao da contradicao.
        propositions: Lista de proposicoes envolvidas.
        conversation_context: Contexto da conversa para referencia.
        llm: Instancia do LLM (opcional).

    Returns:
        QuestionSuggestion: Sugestao de pergunta com tom adequado.

    Example:
        >>> contradiction = {
        ...     "description": "Usuario disse X e Y que parecem contraditorios"
        ... }
        >>> suggestion = generate_contradiction_question(
        ...     contradiction, propositions, context
        ... )
        >>> print(suggestion.question_text)
        'Voce mencionou X e Y. Eles se aplicam em situacoes diferentes?'
    """
    if llm is None:
        llm = _get_llm(
            temperature=QUESTION_GENERATION_TEMPERATURE,
            max_tokens=MAX_QUESTION_TOKENS
        )

    # Formatar descricao da contradicao
    contradiction_desc = contradiction.get(
        "description",
        contradiction.get("explanation", "Tensao detectada")
    )

    # Construir prompt
    prompt = CONTRADICTION_QUESTION_PROMPT.format(
        conversation_context=conversation_context[:1000],  # Truncar
        contradiction_description=contradiction_desc,
        propositions=_format_proposicoes(propositions)
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(
            llm=llm,
            messages=messages,
            agent_name="observer_clarification_contradiction"
        )

        data = extract_json_from_llm_response(response.content)

        suggestion = QuestionSuggestion(
            question_text=data.get("question", "Poderia elaborar mais sobre isso?"),
            target_type="contradiction",
            related_proposicoes=[
                p.get("texto", str(p)) if isinstance(p, dict) else str(p)
                for p in propositions[:3]
            ],
            expected_outcome="; ".join(data.get("expected_outcomes", ["Esclarecimento do contexto"])),
            tone_guidance=data.get("tone_check", "Curiosidade genuina")
        )

        logger.info(f"Pergunta sobre contradicao gerada: {suggestion.question_text[:50]}...")
        return suggestion

    except Exception as e:
        logger.warning(f"Erro ao gerar pergunta sobre contradicao: {e}")
        # Fallback generico
        return QuestionSuggestion(
            question_text="Interessante - esses pontos parecem ter nuances. Poderia me ajudar a entender melhor?",
            target_type="contradiction",
            expected_outcome="Esclarecimento geral",
            tone_guidance="Curiosidade genuina"
        )


# =============================================================================
# 14.4 - PERGUNTA SOBRE GAP (LACUNA)
# =============================================================================

def suggest_question_for_gap(
    cognitive_model: Dict[str, Any],
    gap_index: int = 0,
    conversation_context: str = "",
    llm: Optional[ChatAnthropic] = None
) -> Optional[QuestionSuggestion]:
    """
    Sugere pergunta para preencher gap especifico no raciocinio.

    Gaps sao aspectos mencionados mas nao desenvolvidos, ou informacoes
    faltantes para sustentar o claim. Esta funcao gera perguntas que
    ajudam a AVANCAR o argumento, nao apenas coletar dados.

    Args:
        cognitive_model: CognitiveModel atual.
        gap_index: Indice do gap (open_question) a abordar (default: primeiro).
        conversation_context: Contexto da conversa.
        llm: Instancia do LLM (opcional).

    Returns:
        QuestionSuggestion: Sugestao de pergunta, ou None se gap nao e critico.

    Example:
        >>> cm = {
        ...     "claim": "LLMs aumentam produtividade",
        ...     "open_questions": ["Qual baseline de comparacao?"]
        ... }
        >>> suggestion = suggest_question_for_gap(cm, gap_index=0)
        >>> if suggestion:
        ...     print(suggestion.question_text)
    """
    open_questions = cognitive_model.get("open_questions", [])

    if not open_questions:
        logger.debug("Nenhum gap para sugerir pergunta")
        return None

    if gap_index >= len(open_questions):
        gap_index = 0

    gap = open_questions[gap_index]
    claim = cognitive_model.get("claim", "")

    if llm is None:
        llm = _get_llm(
            temperature=QUESTION_GENERATION_TEMPERATURE,
            max_tokens=MAX_QUESTION_TOKENS
        )

    # Construir prompt
    prompt = GAP_QUESTION_PROMPT.format(
        conversation_context=conversation_context[:1000],
        claim=claim or "(claim nao definido)",
        gap_description=gap,
        open_questions=_format_open_questions(open_questions)
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(
            llm=llm,
            messages=messages,
            agent_name="observer_clarification_gap"
        )

        data = extract_json_from_llm_response(response.content)

        suggestion = QuestionSuggestion(
            question_text=data.get("question", "O que te levou a essa conclusao?"),
            target_type="gap",
            related_proposicoes=[],  # Gaps geralmente nao tem proposicoes especificas
            expected_outcome=data.get("connection_to_claim", "Fortalecimento do argumento"),
            tone_guidance="Curiosidade genuina e parceria intelectual"
        )

        logger.info(f"Pergunta sobre gap gerada: {suggestion.question_text[:50]}...")
        return suggestion

    except Exception as e:
        logger.warning(f"Erro ao gerar pergunta sobre gap: {e}")
        return None


# =============================================================================
# 14.5 - DECISAO DE TIMING (QUANDO PERGUNTAR)
# =============================================================================

def should_ask_clarification(
    clarification_need: ClarificationNeed,
    turn_history: List[Dict[str, Any]],
    current_turn: int,
    turns_since_last_question: int = 0,
    is_user_flowing: bool = True
) -> ClarificationTimingDecision:
    """
    Decide se e quando fazer pergunta de esclarecimento.

    Esta funcao implementa as regras de timing para evitar interromper
    o usuario desnecessariamente enquanto garante que confusoes
    importantes sejam abordadas.

    Regras de timing:
    - NAO pergunta apos cada input
    - Pergunta quando confusao se acumula
    - Pergunta quando contradicao persiste 2+ turns
    - NAO pergunta quando usuario esta fluindo bem

    Args:
        clarification_need: Necessidade de esclarecimento identificada.
        turn_history: Historico de turnos para analise.
        current_turn: Numero do turno atual.
        turns_since_last_question: Turnos desde ultima pergunta de esclarecimento.
        is_user_flowing: Se usuario esta adicionando proposicoes consistentes.

    Returns:
        ClarificationTimingDecision: Decisao com justificativa.

    Example:
        >>> need = ClarificationNeed(
        ...     needs_clarification=True,
        ...     clarification_type="contradiction",
        ...     turns_persisted=3
        ... )
        >>> decision = should_ask_clarification(
        ...     need, turn_history, current_turn=5
        ... )
        >>> if decision.should_ask:
        ...     print("Hora de perguntar!")
    """
    # Regra 1: Se nao precisa esclarecimento, nao perguntar
    if not clarification_need.needs_clarification:
        return ClarificationTimingDecision(
            should_ask=False,
            reason="Nao ha necessidade de esclarecimento identificada",
            delay_turns=0,
            urgency="low"
        )

    # Regra 2: Se perguntou recentemente, esperar
    if turns_since_last_question < MIN_TURNS_BETWEEN_QUESTIONS:
        wait_turns = MIN_TURNS_BETWEEN_QUESTIONS - turns_since_last_question
        return ClarificationTimingDecision(
            should_ask=False,
            reason=f"Pergunta recente - esperar {wait_turns} turno(s)",
            delay_turns=wait_turns,
            urgency="low"
        )

    # Regra 3: Prioridade alta sempre pergunta
    if clarification_need.priority == "high":
        return ClarificationTimingDecision(
            should_ask=True,
            reason=f"Prioridade alta: {clarification_need.description[:50]}",
            delay_turns=0,
            urgency="high"
        )

    # Regra 4: Contradicao persistente por 2+ turnos
    if (clarification_need.clarification_type == "contradiction" and
            clarification_need.turns_persisted >= MIN_CONTRADICTION_PERSISTENCE_TURNS):
        return ClarificationTimingDecision(
            should_ask=True,
            reason=f"Contradicao persiste ha {clarification_need.turns_persisted} turnos",
            delay_turns=0,
            urgency="medium"
        )

    # Regra 5: Usuario fluindo bem - nao interromper
    if is_user_flowing and clarification_need.priority != "high":
        return ClarificationTimingDecision(
            should_ask=False,
            reason="Usuario fluindo bem - nao interromper",
            delay_turns=2,
            urgency="low"
        )

    # Regra 6: Prioridade media - perguntar se timing ok
    if clarification_need.priority == "medium":
        return ClarificationTimingDecision(
            should_ask=True,
            reason=f"Esclarecimento medio necessario: {clarification_need.clarification_type}",
            delay_turns=0,
            urgency="medium"
        )

    # Default: prioridade baixa - adiar
    return ClarificationTimingDecision(
        should_ask=False,
        reason="Prioridade baixa - aguardando momento melhor",
        delay_turns=3,
        urgency="low"
    )


# =============================================================================
# 14.6 - ANALISAR RESPOSTA DE ESCLARECIMENTO
# =============================================================================

def analyze_clarification_response(
    user_response: str,
    question_asked: str,
    original_need: ClarificationNeed,
    cognitive_model: Dict[str, Any],
    llm: Optional[ChatAnthropic] = None
) -> ClarificationResponse:
    """
    Analisa resposta do usuario a pergunta de esclarecimento.

    Apos o Orquestrador fazer uma pergunta de esclarecimento, esta funcao
    analisa se a resposta do usuario esclareceu a duvida e que atualizacoes
    fazer no CognitiveModel.

    Status de resolucao:
    - resolved: Esclarecimento completo
    - partially_resolved: Algumas duvidas permanecem
    - unresolved: Resposta nao esclareceu

    Args:
        user_response: Resposta do usuario a pergunta.
        question_asked: Pergunta que foi feita.
        original_need: Necessidade original de esclarecimento.
        cognitive_model: CognitiveModel atual.
        llm: Instancia do LLM (opcional).

    Returns:
        ClarificationResponse: Analise com status e atualizacoes sugeridas.

    Example:
        >>> response = analyze_clarification_response(
        ...     user_response="Sim, quando falo de produtividade...",
        ...     question_asked="Voce mencionou X e Y...",
        ...     original_need=need,
        ...     cognitive_model=cm
        ... )
        >>> if response.resolution_status == "resolved":
        ...     apply_updates(response.updates)
    """
    if llm is None:
        llm = _get_llm(
            temperature=RESPONSE_ANALYSIS_TEMPERATURE,
            max_tokens=MAX_RESPONSE_ANALYSIS_TOKENS
        )

    # Formatar cognitive_model para prompt
    cm_summary = json.dumps({
        "claim": cognitive_model.get("claim", ""),
        "proposicoes_count": len(cognitive_model.get("proposicoes", [])),
        "contradictions_count": len(cognitive_model.get("contradictions", [])),
        "open_questions": cognitive_model.get("open_questions", [])[:3]
    }, ensure_ascii=False, indent=2)

    # Construir prompt
    prompt = ANALYZE_CLARIFICATION_RESPONSE_PROMPT.format(
        question_asked=question_asked,
        clarification_type=original_need.clarification_type,
        original_need=original_need.description,
        user_response=user_response,
        cognitive_model=cm_summary
    )

    try:
        messages = [HumanMessage(content=prompt)]
        response = invoke_with_retry(
            llm=llm,
            messages=messages,
            agent_name="observer_clarification_analyze"
        )

        data = extract_json_from_llm_response(response.content)

        # Extrair updates
        updates_data = data.get("updates", {})
        updates = ClarificationUpdates(
            proposicoes_to_add=updates_data.get("proposicoes_to_add", []),
            proposicoes_to_update=updates_data.get("proposicoes_to_update", {}),
            contradictions_to_resolve=updates_data.get("contradictions_to_resolve", []),
            open_questions_to_close=updates_data.get("open_questions_to_close", []),
            context_to_add=updates_data.get("context_to_add", {})
        )

        clarification_response = ClarificationResponse(
            resolution_status=data.get("resolution_status", "unresolved"),
            summary=data.get("summary", "Analise da resposta"),
            updates=updates,
            needs_followup=data.get("needs_followup", False),
            followup_suggestion=data.get("followup_suggestion")
        )

        logger.info(
            f"Resposta analisada: status={clarification_response.resolution_status}, "
            f"followup={clarification_response.needs_followup}"
        )

        return clarification_response

    except Exception as e:
        logger.warning(f"Erro ao analisar resposta de esclarecimento: {e}")
        # Fallback conservador
        return ClarificationResponse(
            resolution_status="unresolved",
            summary="Erro ao analisar - status incerto",
            updates=ClarificationUpdates(),
            needs_followup=False
        )


# =============================================================================
# FUNCOES AUXILIARES
# =============================================================================

def update_clarification_persistence(
    clarification_need: ClarificationNeed,
    still_relevant: bool = True
) -> ClarificationNeed:
    """
    Atualiza contagem de turnos que uma necessidade persiste.

    Chamada a cada turno para rastrear ha quanto tempo uma
    necessidade de esclarecimento esta pendente.

    Args:
        clarification_need: Necessidade atual.
        still_relevant: Se a necessidade ainda e relevante.

    Returns:
        ClarificationNeed: Necessidade com turns_persisted atualizado.
    """
    if not still_relevant:
        # Reseta contagem se nao e mais relevante
        return ClarificationNeed(
            needs_clarification=False,
            clarification_type=clarification_need.clarification_type,
            description="Necessidade resolvida ou nao mais relevante",
            suggested_approach="",
            turn_detected=clarification_need.turn_detected,
            turns_persisted=0
        )

    # Incrementa contagem
    return ClarificationNeed(
        id=clarification_need.id,
        needs_clarification=clarification_need.needs_clarification,
        clarification_type=clarification_need.clarification_type,
        description=clarification_need.description,
        relevant_context=clarification_need.relevant_context,
        suggested_approach=clarification_need.suggested_approach,
        priority=clarification_need.priority,
        turn_detected=clarification_need.turn_detected,
        turns_persisted=clarification_need.turns_persisted + 1
    )


def get_clarification_summary_for_timeline(
    clarification_response: ClarificationResponse,
    clarification_type: str
) -> str:
    """
    Gera resumo de esclarecimento para exibir na timeline.

    Args:
        clarification_response: Resposta do esclarecimento.
        clarification_type: Tipo de esclarecimento.

    Returns:
        str: Texto formatado para timeline.

    Example:
        >>> summary = get_clarification_summary_for_timeline(response, "contradiction")
        >>> print(summary)
        'Esclarecimento obtido: Usuario explicou que X e Y se aplicam em contextos diferentes'
    """
    status_emoji = {
        "resolved": "✅",
        "partially_resolved": "🔶",
        "unresolved": "❓"
    }

    emoji = status_emoji.get(clarification_response.resolution_status, "📝")
    type_label = {
        "contradiction": "Tensao",
        "gap": "Lacuna",
        "confusion": "Confusao",
        "direction_change": "Mudanca de direcao"
    }.get(clarification_type, "Esclarecimento")

    if clarification_response.resolution_status == "resolved":
        return f"{emoji} {type_label} esclarecida: {clarification_response.summary[:100]}"
    elif clarification_response.resolution_status == "partially_resolved":
        return f"{emoji} {type_label} parcialmente esclarecida: {clarification_response.summary[:80]}"
    else:
        return f"{emoji} {type_label} pendente: {clarification_response.summary[:80]}"
