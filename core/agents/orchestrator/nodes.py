"""
Nos do grafo do agente Orquestrador.

Este modulo implementa o no principal do Orquestrador:
- orchestrator_node: Facilitador conversacional MVP com argumento focal explicito
- _build_context: Constroi contexto incluindo outputs de agentes para curadoria

=== SEPARACAO DE RESPONSABILIDADES (Epico 10.1) ===

Apos a "mitose" do Orquestrador, as responsabilidades foram separadas:

ORQUESTRADOR (este modulo):
- Facilitar conversa com usuario
- Negociar caminhos e apresentar opcoes
- Provocar reflexao sobre lacunas
- Decidir next_step (explore, suggest_agent, clarify)
- Consultar Observador quando incerto

OBSERVADOR (agents/observer/):
- Monitorar TODA conversa (todo turno)
- Atualizar CognitiveModel completo
- Extrair conceitos para catalogo
- Calcular metricas (solidez, completude)
- Responder consultas do Orquestrador (insights, nao comandos)

NOTA: Na versao atual (10.1), o Orquestrador ainda gera cognitive_model
diretamente. Em versoes futuras (10.2+), o Observador assumira essa
responsabilidade e o Orquestrador apenas consultara.

Versao: 5.4 (Epico 10.1 - Mitose do Orquestrador)
Data: 05/12/2025
"""

import logging
import json
import time
from typing import Optional, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_anthropic import ChatAnthropic
from pydantic import ValidationError

from .state import MultiAgentState
from core.utils.json_parser import extract_json_from_llm_response
from core.utils.config import get_anthropic_model, invoke_with_retry, create_anthropic_client
from core.agents.memory.config_loader import get_agent_prompt, get_agent_model, ConfigLoadError
from core.agents.memory.execution_tracker import register_execution
from core.utils.token_extractor import extract_tokens_and_cost
from core.agents.models.cognitive_model import CognitiveModel
from core.agents.models.proposition import Proposicao
from core.utils.event_bus import get_event_bus
from core.agents.persistence import create_snapshot_if_mature
from core.utils.structured_logger import StructuredLogger

logger = logging.getLogger(__name__)


def _create_fallback_cognitive_model(state: MultiAgentState) -> Dict[str, Any]:
    """
    Cria cognitive_model de fallback quando LLM não retorna ou retorna inválido.

    Usa o user_input para criar um modelo mínimo.

    Args:
        state: Estado atual do sistema

    Returns:
        Dict com cognitive_model mínimo válido
    """
    user_input = state.get("user_input", "")

    return {
        "claim": user_input[:200] if user_input else "",
        "proposicoes": [],
        "open_questions": ["O que você quer explorar sobre isso?"],
        "contradictions": [],
        "solid_grounds": [],
        "context": {}
    }


def _validate_cognitive_model(
    cognitive_model_raw: Optional[Dict[str, Any]],
    state: MultiAgentState
) -> Dict[str, Any]:
    """
    Valida cognitive_model usando schema Pydantic e retorna dict válido.

    Esta função:
    1. Se cognitive_model_raw for None, cria fallback
    2. Valida contra schema CognitiveModel (Pydantic)
    3. Se validação falhar, loga erro e cria fallback
    4. Retorna dict (não instância Pydantic) para compatibilidade com state

    Args:
        cognitive_model_raw: Dict extraído do JSON do LLM (pode ser None)
        state: Estado atual do sistema (para criar fallback)

    Returns:
        Dict[str, Any]: cognitive_model validado como dict

    Example:
        >>> raw = {"claim": "LLMs aumentam produtividade", "proposicoes": [...], ...}
        >>> validated = _validate_cognitive_model(raw, state)
        >>> validated["claim"]
        'LLMs aumentam produtividade'
    """
    # Se não veio cognitive_model, cria fallback
    if not cognitive_model_raw:
        logger.warning("cognitive_model não fornecido pelo LLM. Usando fallback.")
        return _create_fallback_cognitive_model(state)

    # Tentar validar com Pydantic
    try:
        # Garantir que contradictions tenha estrutura correta
        # LLM pode retornar contradictions vazio como [] ou com items sem confidence
        contradictions = cognitive_model_raw.get("contradictions", [])
        validated_contradictions = []
        for c in contradictions:
            if isinstance(c, dict):
                # Garantir confidence >= 0.80 (regra do schema)
                confidence = c.get("confidence", 0.85)
                if confidence >= 0.80:
                    validated_contradictions.append({
                        "description": c.get("description", ""),
                        "confidence": confidence,
                        "suggested_resolution": c.get("suggested_resolution")
                    })

        # Processar proposições (Épico 11.5)
        # LLM pode retornar proposicoes como lista de objetos ou lista de strings (legado)
        proposicoes_raw = cognitive_model_raw.get("proposicoes", [])
        validated_proposicoes = []
        for p in proposicoes_raw:
            if isinstance(p, dict):
                # Formato novo: {"texto": "...", "solidez": 0.8}
                validated_proposicoes.append(
                    Proposicao(
                        texto=p.get("texto", ""),
                        solidez=p.get("solidez")  # None se não fornecido
                    )
                )
            elif isinstance(p, str):
                # Formato legado: string simples → proposição com solidez=None
                validated_proposicoes.append(Proposicao.from_text(p))

        # Construir dict para validação
        model_dict = {
            "claim": cognitive_model_raw.get("claim", ""),
            "proposicoes": validated_proposicoes,
            "open_questions": cognitive_model_raw.get("open_questions", []),
            "contradictions": validated_contradictions,
            "solid_grounds": cognitive_model_raw.get("solid_grounds", []),
            "context": cognitive_model_raw.get("context", {})
        }

        # Validar com Pydantic
        validated_model = CognitiveModel.model_validate(model_dict)
        logger.info(f"✅ cognitive_model validado: claim={validated_model.claim[:50]}...")

        # Retornar como dict para compatibilidade com TypedDict state
        return validated_model.model_dump()

    except ValidationError as e:
        logger.error(f"❌ Falha na validação do cognitive_model: {e}")
        logger.warning("Usando cognitive_model fallback.")
        return _create_fallback_cognitive_model(state)
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao validar cognitive_model: {e}")
        return _create_fallback_cognitive_model(state)


def _merge_focal_argument(previous_focal: Optional[dict], new_focal: dict) -> dict:
    """
    Faz merge inteligente do focal_argument preservando valores anteriores quando novos são vagos.

    Regras de merge:
    - Se novo valor é "not specified" ou "unclear" → preserva valor anterior (se existir)
    - Se novo valor é específico → usa novo valor
    - Se não havia valor anterior → usa novo valor

    Args:
        previous_focal: Argumento focal anterior (pode ser None)
        new_focal: Argumento focal novo extraído do LLM

    Returns:
        dict: Argumento focal mesclado preservando contexto anterior
    """
    if not previous_focal:
        # Sem valor anterior, usa novo valor diretamente
        return new_focal.copy()

    merged = {}

    # Campos que devem ser mesclados
    fields_to_merge = ['intent', 'subject', 'population', 'metrics', 'article_type']

    for field in fields_to_merge:
        new_value = new_focal.get(field)
        previous_value = previous_focal.get(field)

        # EXPANDIDO: Reconhecer variações naturais de "vago" que o LLM pode retornar
        empty_values = [
            # Valores padronizados
            'not specified', 'unclear', None, '',
            # Variações naturais que o LLM inventa
            'not operationalized', 'undefined', 'not defined',
            'vague', 'ambiguous', 'to be determined', 'tbd',
            'not clear', 'unspecified', 'unknown'
        ]

        # Se novo valor é vago e havia valor anterior específico → preserva anterior
        if new_value in empty_values and previous_value and previous_value not in empty_values:
            merged[field] = previous_value
            logger.debug(f"Preservando {field} anterior: '{previous_value}' (novo valor era vago: '{new_value}')")
        # Se novo valor é específico → usa novo valor
        elif new_value and new_value not in empty_values:
            merged[field] = new_value
        # Se novo valor existe mas é vago e não havia anterior → usa novo valor
        elif new_value:
            merged[field] = new_value
        # Fallback: usa anterior se existir
        elif previous_value:
            merged[field] = previous_value
        else:
            # Último fallback: valor padrão
            if field in ['intent', 'article_type']:
                merged[field] = 'unclear'
            else:
                merged[field] = 'not specified'

    return merged


def _build_cognitive_model_context(cognitive_model: Dict[str, Any]) -> str:
    """
    Formata cognitive_model do Observer para o prompt do Orquestrador (Épico 12.2).

    Esta função prepara o cognitive_model gerado pelo Observer para inclusão
    no contexto do Orquestrador, permitindo que ele use as análises semânticas
    para tomar decisões mais informadas.

    Limites para evitar sobrecarga do prompt:
    - Proposições: 5 primeiras (ordenadas por solidez)
    - Conceitos: 10 primeiros
    - Contradições: 3 primeiras
    - Questões abertas: 5 primeiras

    Args:
        cognitive_model: Dict com CognitiveModel do Observer contendo:
            - claim: Afirmação central
            - proposicoes: Lista de proposições com solidez
            - concepts_detected: Conceitos extraídos
            - contradictions: Contradições detectadas
            - open_questions: Questões em aberto
            - overall_solidez/overall_completude: Métricas (opcional)

    Returns:
        str: Seção formatada para inclusão no prompt

    Example:
        >>> cm = {"claim": "LLMs aumentam produtividade", "proposicoes": [...]}
        >>> context = _build_cognitive_model_context(cm)
        >>> "COGNITIVE MODEL DISPONÍVEL" in context
        True
    """
    parts = ["## COGNITIVE MODEL DISPONÍVEL (via Observer)"]
    parts.append("")
    parts.append("O Observador analisou o diálogo e extraiu:")
    parts.append("")

    # Afirmação atual
    claim = cognitive_model.get("claim", "")
    if claim:
        parts.append(f"**Afirmação central:** {claim}")
        parts.append("")

    # Fundamentos (proposições) - ordenar por solidez decrescente, limitar a 5
    proposicoes = cognitive_model.get("proposicoes", [])
    if proposicoes:
        # Ordenar por solidez (maior primeiro)
        # BUGFIX: solidez pode ser None mesmo quando key existe, usar `or 0.0` para garantir float
        sorted_props = sorted(
            proposicoes,
            key=lambda p: (p.get("solidez") if isinstance(p, dict) else getattr(p, "solidez", None)) or 0.0,
            reverse=True
        )[:5]

        parts.append("**Fundamentos (proposições com solidez):**")
        for prop in sorted_props:
            texto = prop.get("texto", "") if isinstance(prop, dict) else getattr(prop, "texto", "")
            solidez = prop.get("solidez", None) if isinstance(prop, dict) else getattr(prop, "solidez", None)
            solidez_str = f" (solidez: {solidez:.2f})" if solidez is not None else " (solidez: pendente)"
            parts.append(f"- {texto}{solidez_str}")

        if len(proposicoes) > 5:
            parts.append(f"- ... e mais {len(proposicoes) - 5} fundamentos")
        parts.append("")

    # Conceitos detectados - limitar a 10
    concepts = cognitive_model.get("concepts_detected", [])
    if concepts:
        concepts_str = ", ".join(concepts[:10])
        if len(concepts) > 10:
            concepts_str += f" (+{len(concepts) - 10} mais)"
        parts.append(f"**Conceitos detectados:** {concepts_str}")
        parts.append("")

    # Contradições - limitar a 3
    contradictions = cognitive_model.get("contradictions", [])
    if contradictions:
        parts.append("**Contradições detectadas:**")
        for c in contradictions[:3]:
            desc = c.get("description", "") if isinstance(c, dict) else str(c)
            confidence = c.get("confidence", 0.0) if isinstance(c, dict) else 0.0
            parts.append(f"- {desc} (confiança: {confidence:.0%})")

        if len(contradictions) > 3:
            parts.append(f"- ... e mais {len(contradictions) - 3} contradições")
        parts.append("")

    # Questões em aberto - limitar a 5
    open_questions = cognitive_model.get("open_questions", [])
    if open_questions:
        parts.append("**Questões em aberto:**")
        for q in open_questions[:5]:
            parts.append(f"- {q}")

        if len(open_questions) > 5:
            parts.append(f"- ... e mais {len(open_questions) - 5} questões")
        parts.append("")

    # Métricas (se disponíveis)
    solidez = cognitive_model.get("overall_solidez")
    completude = cognitive_model.get("overall_completude")

    # Fallback: calcular solidez/completude se não estiverem no dict
    if solidez is None and proposicoes:
        solidez_values = [
            (p.get("solidez") if isinstance(p, dict) else getattr(p, "solidez", None))
            for p in proposicoes
        ]
        valid_values = [v for v in solidez_values if v is not None]
        solidez = sum(valid_values) / len(valid_values) if valid_values else 0.0

    if solidez is not None or completude is not None:
        parts.append("**Métricas:**")
        if solidez is not None:
            parts.append(f"- Solidez: {solidez:.0%} (quão bem fundamentada está a afirmação)")
        if completude is not None:
            parts.append(f"- Completude: {completude:.0%} (quanto do argumento foi desenvolvido)")
        parts.append("")

    # Instrução de uso
    parts.append("Use este modelo cognitivo para:")
    parts.append("- Identificar lacunas no raciocínio")
    parts.append("- Detectar contradições a resolver")
    parts.append("- Sugerir próximos passos baseados nas questões abertas")
    parts.append("- Avaliar se o argumento está maduro para estruturação")

    return "\n".join(parts)


def _consult_observer(
    state: MultiAgentState,
    user_input: str,
    cognitive_model: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Consulta o Observer para análise de clareza e variação (Épico 13.3).

    Esta função encapsula as chamadas ao Observer para:
    1. Avaliar clareza da conversa atual
    2. Detectar se houve variação ou mudança real (se houver claim anterior)

    O Observer é consultivo - fornece insights que o Orquestrador usa
    para tomar decisões. O Observer NÃO decide interromper a conversa.

    Filosofia (Épico 13):
    - Observer detecta; Orchestrator decide
    - Análise 100% contextual via LLM
    - Sem thresholds fixos

    Args:
        state: Estado atual do sistema.
        user_input: Input atual do usuário.
        cognitive_model: CognitiveModel atual (pode ser None no início).

    Returns:
        Dict com análises do Observer:
        - clarity_evaluation: Avaliação de clareza da conversa
        - variation_analysis: Análise de variação (se houver claim anterior)
        - needs_checkpoint: bool indicando se precisa checkpoint
        - checkpoint_reason: Razão do checkpoint (se aplicável)

    Example:
        >>> result = _consult_observer(state, "novo input", cognitive_model)
        >>> if result['needs_checkpoint']:
        ...     # Orquestrador decide como intervir
        ...     suggestion = result['clarity_evaluation']['suggestion']
    """
    # Import lazy para evitar dependência circular com chromadb (Épico 13.3)
    from core.agents.observer.extractors import (
        evaluate_conversation_clarity,
        detect_variation
    )

    logger.info("🔍 Consultando Observer para análise contextual...")

    result = {
        "clarity_evaluation": None,
        "variation_analysis": None,
        "needs_checkpoint": False,
        "checkpoint_reason": None
    }

    # Obter session_id e calcular turn_number para publicação de eventos (Épico 13.5)
    session_id = state.get("session_id", "unknown-session")
    messages = state.get("messages", [])
    turn_number = max(1, len([m for m in messages if m.__class__.__name__ == "HumanMessage"]))

    # 1. Avaliar clareza da conversa
    if cognitive_model:
        try:
            # Preparar histórico de conversação
            conversation_history = []
            for msg in messages[-6:]:  # Últimas 6 mensagens
                if hasattr(msg, 'content'):
                    role = "user" if msg.__class__.__name__ == "HumanMessage" else "assistant"
                    conversation_history.append({
                        "role": role,
                        "content": msg.content[:500]  # Truncar
                    })

            clarity_result = evaluate_conversation_clarity(
                cognitive_model=cognitive_model,
                conversation_history=conversation_history
            )

            result["clarity_evaluation"] = clarity_result

            # Checkpoint se clareza baixa
            if clarity_result.get("needs_checkpoint"):
                result["needs_checkpoint"] = True
                result["checkpoint_reason"] = f"Clareza '{clarity_result.get('clarity_level')}': {clarity_result.get('description', '')}"

                # === PUBLICAR EVENTO: ClarityCheckpoint (Épico 13.5) ===
                try:
                    event_bus = get_event_bus()
                    event_bus.publish_clarity_checkpoint(
                        session_id=session_id,
                        turn_number=turn_number,
                        clarity_level=clarity_result.get("clarity_level", "nebulosa"),
                        clarity_score=clarity_result.get("clarity_score", 2),
                        checkpoint_reason=result["checkpoint_reason"],
                        factors=clarity_result.get("factors", {}),
                        suggestion=clarity_result.get("suggestion", "")
                    )
                    logger.debug(f"⚠️ Evento clarity_checkpoint publicado para turno {turn_number}")
                except Exception as pub_err:
                    logger.warning(f"Erro ao publicar clarity_checkpoint: {pub_err}")

            logger.info(
                f"📊 Clareza: {clarity_result.get('clarity_level')} "
                f"(score={clarity_result.get('clarity_score')}, checkpoint={clarity_result.get('needs_checkpoint')})"
            )

        except Exception as e:
            logger.warning(f"⚠️ Erro ao avaliar clareza: {e}")

    # 2. Detectar variação vs mudança real (se houver claim anterior)
    previous_claim = None
    if cognitive_model and cognitive_model.get("claim"):
        previous_claim = cognitive_model.get("claim")
    else:
        focal = state.get("focal_argument")
        if focal and isinstance(focal, dict) and focal.get("subject"):
            previous_claim = focal.get("subject")

    if previous_claim and user_input:
        try:
            variation_result = detect_variation(
                previous_text=previous_claim,
                new_text=user_input,
                cognitive_model=cognitive_model
            )

            result["variation_analysis"] = variation_result

            # Se mudança real detectada, adicionar ao checkpoint reason
            if variation_result.get("classification") == "real_change":
                logger.info(f"🔄 Mudança real detectada: {variation_result.get('reasoning', '')[:100]}")
                if not result["needs_checkpoint"]:
                    result["needs_checkpoint"] = True
                    result["checkpoint_reason"] = f"Mudança de direção detectada: {variation_result.get('analysis', '')[:150]}"

                # === PUBLICAR EVENTO: DirectionChangeConfirmed (Épico 13.5) ===
                try:
                    event_bus = get_event_bus()
                    event_bus.publish_direction_change_confirmed(
                        session_id=session_id,
                        turn_number=turn_number,
                        previous_claim=previous_claim,
                        new_claim=user_input[:200],  # Truncar para evitar eventos muito grandes
                        user_confirmed=False,  # Será True após confirmação do usuário
                        reasoning=variation_result.get("reasoning", "")
                    )
                    logger.debug(f"🔄 Evento direction_change_confirmed publicado para turno {turn_number}")
                except Exception as pub_err:
                    logger.warning(f"Erro ao publicar direction_change_confirmed: {pub_err}")

            elif variation_result.get("classification") == "variation":
                # === PUBLICAR EVENTO: VariationDetected (Épico 13.5) ===
                try:
                    event_bus = get_event_bus()
                    event_bus.publish_variation_detected(
                        session_id=session_id,
                        turn_number=turn_number,
                        essence_previous=variation_result.get("essence_previous", previous_claim[:100]),
                        essence_new=variation_result.get("essence_new", user_input[:100]),
                        shared_concepts=variation_result.get("shared_concepts", []),
                        new_concepts=variation_result.get("new_concepts", []),
                        analysis=variation_result.get("analysis", "")
                    )
                    logger.debug(f"↪️ Evento variation_detected publicado para turno {turn_number}")
                except Exception as pub_err:
                    logger.warning(f"Erro ao publicar variation_detected: {pub_err}")

            logger.info(
                f"🎯 Variação: {variation_result.get('classification')} "
                f"(shared={len(variation_result.get('shared_concepts', []))}, "
                f"new={len(variation_result.get('new_concepts', []))})"
            )

        except Exception as e:
            logger.warning(f"⚠️ Erro ao detectar variação: {e}")

    return result


def _build_context(state: MultiAgentState) -> str:
    """
    Constrói contexto completo para o Orquestrador, incluindo outputs de agentes.

    Esta função helper constrói o contexto que será enviado ao LLM, incluindo:
    - Input inicial do usuário
    - Histórico de mensagens da conversa
    - Outputs de agentes (para curadoria - Épico 1.1)

    Quando structurer_output ou methodologist_output existem no state,
    o Orquestrador está em MODO CURADORIA e deve apresentar o resultado
    ao usuário de forma coesa.

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        str: Contexto formatado para análise pelo LLM.
            Formato:
            ```
            INPUT INICIAL DO USUÁRIO:
            {user_input}

            HISTÓRICO DA CONVERSA:
            [Usuário]: {mensagem 1}
            [Assistente]: {resposta 1}
            ...

            RESULTADO DO ESTRUTURADOR (você deve fazer curadoria):
            {structurer_output em JSON}

            RESULTADO DO METODOLOGISTA (você deve fazer curadoria):
            {methodologist_output em JSON}
            ```

    Example:
        >>> state = create_initial_multi_agent_state("Observei X", "session-123")
        >>> context = _build_context(state)
        >>> "INPUT INICIAL DO USUÁRIO" in context
        True

        >>> # Com output de agente (modo curadoria)
        >>> state['structurer_output'] = {"research_question": "Como X impacta Y?"}
        >>> context = _build_context(state)
        >>> "RESULTADO DO ESTRUTURADOR" in context
        True

    Notes:
        - Se não houver mensagens, retorna apenas o input inicial
        - Se houver outputs de agentes, Orquestrador deve fazer curadoria
        - Formato é otimizado para análise contextual pelo LLM
    """
    # Input inicial do usuário
    context_parts = [
        "INPUT INICIAL DO USUÁRIO:",
        state["user_input"],
        ""  # linha em branco
    ]

    # Histórico de mensagens (se houver)
    messages = state.get("messages", [])
    if messages:
        context_parts.append("HISTÓRICO DA CONVERSA:")

        for msg in messages:
            # Identificar tipo de mensagem
            if hasattr(msg, '__class__'):
                msg_type = msg.__class__.__name__
            else:
                msg_type = "Unknown"

            # Formatar conforme tipo
            if msg_type == "HumanMessage":
                context_parts.append(f"[Usuário]: {msg.content}")
            elif msg_type == "AIMessage":
                context_parts.append(f"[Assistente]: {msg.content}")
            else:
                # Fallback para outros tipos de mensagem
                context_parts.append(f"[{msg_type}]: {msg.content}")

        context_parts.append("")  # linha em branco final

    # Cognitive Model do Observer (se existir - Épico 12.2)
    # Disponibiliza análise semântica do Observador para o Orquestrador
    cognitive_model = state.get("cognitive_model")
    if cognitive_model and (cognitive_model.get("claim") or cognitive_model.get("proposicoes")):
        context_parts.append(_build_cognitive_model_context(cognitive_model))
        context_parts.append("")

    # Output do Estruturador (se existir - Épico 1.1 Curadoria)
    structurer_output = state.get("structurer_output")
    if structurer_output:
        context_parts.append("RESULTADO DO ESTRUTURADOR (você deve fazer curadoria):")
        context_parts.append(json.dumps(structurer_output, indent=2, ensure_ascii=False))
        context_parts.append("")

    # Output do Metodologista (se existir - Épico 1.1 Curadoria)
    methodologist_output = state.get("methodologist_output")
    if methodologist_output:
        context_parts.append("RESULTADO DO METODOLOGISTA (você deve fazer curadoria):")
        context_parts.append(json.dumps(methodologist_output, indent=2, ensure_ascii=False))
        context_parts.append("")

    return "\n".join(context_parts)


def orchestrator_node(state: MultiAgentState, config: Optional[RunnableConfig] = None) -> dict:
    """
    No socratico que facilita dialogo provocativo com exposicao de assumptions implicitas.

    Este no e o FACILITADOR CONVERSACIONAL do sistema multi-agente. Ele:
    1. Analisa input + historico completo da conversa
    2. Extrai e atualiza ARGUMENTO FOCAL explicito a cada turno (7.8)
    3. Explora contexto atraves de perguntas abertas
    4. Provoca REFLEXAO sobre lacunas quando relevante (7.9)
    5. Detecta EMERGENCIA de novo estagio naturalmente (7.10)
    6. Sugere proximos passos com justificativas claras
    7. Negocia com o usuario antes de chamar agentes
    8. Detecta mudancas de direcao comparando focal_argument (7.8)
    9. Registra execucao no MemoryManager (se configurado - Epico 6.2)
    10. Cria snapshot automatico quando argumento amadurece (Epico 9.3)

    === SEPARACAO DE RESPONSABILIDADES (Epico 10.1) ===

    ORQUESTRADOR (este no):
    - Facilitar conversa (perguntas abertas, negociacao)
    - Decidir next_step (explore, suggest_agent, clarify)
    - Consultar Observador quando incerto (futuro - 10.2+)

    OBSERVADOR (agents/observer/ - futuro):
    - Monitorar conversa e atualizar CognitiveModel
    - Extrair conceitos para catalogo
    - Calcular metricas (solidez, completude)

    NOTA: Atualmente, cognitive_model ainda e gerado aqui.
    Em 10.2+, sera responsabilidade do Observador.

    Comportamento Conversacional:
    - "explore": Fazer perguntas abertas para entender contexto
    - "suggest_agent": Sugerir agente especifico com justificativa
    - "clarify": Esclarecer ambiguidade ou contradicao detectada

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.
        config (RunnableConfig, optional): Configuração do LangGraph.
            Campos suportados em config["configurable"]:
            - memory_manager: MemoryManager para tracking de tokens (Épico 6.2)
            - active_idea_id: UUID da ideia ativa para persistência (Épico 9.2)

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - orchestrator_analysis: Raciocínio detalhado sobre contexto e histórico
            - focal_argument: Argumento focal extraído/atualizado (OBRIGATÓRIO)
            - cognitive_model: Modelo cognitivo do argumento (Épico 9.1 - OBRIGATÓRIO)
            - next_step: Próxima ação ("explore", "suggest_agent", "clarify")
            - agent_suggestion: Sugestão de agente com justificativa (se next_step="suggest_agent")
            - reflection_prompt: Provocação de reflexão (se lacuna detectada)
            - stage_suggestion: Sugestão de mudança de estágio (se evolução detectada)
            - clarity_evaluation: Avaliação de clareza da conversa pelo Observer (Épico 13.3)
            - variation_analysis: Análise de variação vs mudança real (Épico 13.3)
            - messages: Mensagem conversacional adicionada ao histórico

    Example:
        >>> state = create_initial_multi_agent_state("Observei que LLMs aumentam produtividade", "session-1")
        >>> result = orchestrator_node(state)
        >>> result['focal_argument']['intent']
        'unclear'
        >>> result['focal_argument']['subject']
        'LLMs impact on productivity'
        >>> result['next_step']
        'explore'
    """
    logger.info("=== NÓ ORCHESTRATOR SOCRÁTICO: Iniciando análise contextual (Épico 10) ===")
    logger.info(f"Input do usuário: {state['user_input']}")

    # Extrair trace_id do config para logging estruturado
    trace_id = "unknown"
    if config:
        trace_id = config.get("configurable", {}).get("thread_id", "unknown")
    
    # Inicializar logger estruturado
    structured_logger = StructuredLogger()
    
    # Log de início
    start_time = time.time()
    structured_logger.log_agent_start(
        trace_id=trace_id,
        agent="orchestrator",
        node="orchestrator_node",
        metadata={"messages_count": len(state.get("messages", []))}
    )

    # Verificar se já existe argumento focal anterior (para detectar mudança de direção)
    previous_focal = state.get("focal_argument")
    if previous_focal:
        logger.info(f"Argumento focal anterior: intent={previous_focal.get('intent')}, subject={previous_focal.get('subject')}")

    # Usar prompt socrático do Épico 10
    from core.prompts import ORCHESTRATOR_SOCRATIC_PROMPT_V1

    # Injeção opcional de contexto de produto (E-POC-2.3)
    product_context = None
    if config:
        product_context = config.get("configurable", {}).get("product_context")
    product_context_section = (
        f"\n## CONTEXTO DO PRODUTO\n\n{product_context.strip()}\n\n---\n"
        if product_context and product_context.strip()
        else ""
    )
    system_prompt = ORCHESTRATOR_SOCRATIC_PROMPT_V1.replace(
        "{product_context_section}", product_context_section
    )

    # Construir contexto completo (histórico + input atual)
    full_context = _build_context(state)
    logger.info("Contexto construído com histórico completo")
    logger.debug(f"Contexto:\n{full_context}")

    # Adicionar argumento focal anterior ao contexto (se existir)
    focal_context = ""
    if previous_focal:
        focal_context = f"""
ARGUMENTO FOCAL ANTERIOR:
{json.dumps(previous_focal, indent=2, ensure_ascii=False)}

(Compare com novo input para detectar mudança de direção)
"""

    # Construir prompt completo
    conversational_prompt = f"""{system_prompt}

CONTEXTO DA CONVERSA:
{full_context}
{focal_context}
Analise o contexto completo acima e responda APENAS com JSON estruturado conforme especificado."""

    # Chamar LLM para análise conversacional
    # DECISÃO: Tentar usar modelo mais potente para raciocínio complexo (Épico 7)
    # Fallback: Se não disponível, usa modelo do YAML (config/agents/orchestrator.yaml)
    # Razão: Análise contextual complexa requer raciocínio avançado
    #        (detecção de mudança de direção, reconstrução de argumento focal)
    try:
        # Tentar carregar modelo do YAML primeiro (mais flexível)
        model_name = get_agent_model("orchestrator")
        logger.info(f"Usando modelo do YAML: {model_name}")
    except ConfigLoadError:
        # Fallback: modelo padrão centralizado (mais econômico e sempre disponível)
        model_name = get_anthropic_model()
        logger.warning(f"Config YAML não disponível. Usando fallback: {model_name}")

    try:
        llm = create_anthropic_client(model=model_name, temperature=0)
        messages = [HumanMessage(content=conversational_prompt)]
        response = invoke_with_retry(llm=llm, messages=messages, agent_name="orchestrator")

        logger.info(f"Resposta do LLM (primeiros 200 chars): {response.content[:200]}...")
    except Exception as e:
        # Log de erro na chamada do LLM
        structured_logger.log_error(
            trace_id=trace_id,
            agent="orchestrator",
            node="orchestrator_node",
            error=e,
            metadata={"model_name": model_name}
        )
        raise

    # Registrar execução no MemoryManager (Épico 6.2)
    if config:
        memory_manager = config.get("configurable", {}).get("memory_manager")
        if memory_manager:
            # Extrair next_step antes de registrar (será usada no summary)
            try:
                temp_data = extract_json_from_llm_response(response.content)
                temp_next_step = temp_data.get("next_step", "unknown")
            except Exception:
                temp_next_step = "unknown"

            register_execution(
                memory_manager=memory_manager,
                config=config,
                agent_name="orchestrator",
                response=response,
                summary=f"Próximo passo: {temp_next_step}",
                model_name=model_name,
                extra_metadata={
                    "next_step": temp_next_step,
                    "context_length": len(full_context)
                }
            )

    # Extrair active_idea_id do config (Épico 9.2)
    # Usado pelo SnapshotManager para persistência (Épico 9.3)
    active_idea_id = None
    if config:
        active_idea_id = config.get("configurable", {}).get("active_idea_id")
        if active_idea_id:
            logger.info(f"📝 Processando ideia: {active_idea_id[:8]}...")
        else:
            logger.debug("active_idea_id não fornecido no config (opcional)")

    # Parse da resposta JSON
    try:
        orchestrator_response = extract_json_from_llm_response(response.content)

        reasoning = orchestrator_response.get("reasoning", "Raciocínio não fornecido")
        focal_argument = orchestrator_response.get("focal_argument")
        cognitive_model_raw = orchestrator_response.get("cognitive_model")
        next_step = orchestrator_response.get("next_step", "explore")
        message = orchestrator_response.get("message", "Entendi. Como posso ajudar?")
        agent_suggestion = orchestrator_response.get("agent_suggestion", None)
        reflection_prompt = orchestrator_response.get("reflection_prompt", None)
        stage_suggestion = orchestrator_response.get("stage_suggestion", None)
        
        # Log de decisão após receber resposta do LLM
        # Extrair métricas da resposta (se disponível)
        decision_metadata = {}
        if hasattr(response, 'response_metadata') and response.response_metadata:
            usage = response.response_metadata.get("usage_metadata", {})
            decision_metadata = {
                "tokens_input": usage.get("input_tokens", 0),
                "tokens_output": usage.get("output_tokens", 0),
                "tokens_total": usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
            }
        
        structured_logger.log_decision(
            trace_id=trace_id,
            agent="orchestrator",
            node="orchestrator_node",
            decision={
                "next_step": next_step,
                "agent_suggestion": agent_suggestion,
                "focal_argument_intent": focal_argument.get("intent") if focal_argument else None
            },
            reasoning=reasoning,
            metadata=decision_metadata
        )

        # Validar e processar cognitive_model (Épico 9.1 - OBRIGATÓRIO)
        cognitive_model_dict = _validate_cognitive_model(cognitive_model_raw, state)

        # Validar focal_argument (OBRIGATÓRIO no MVP)
        if not focal_argument:
            logger.error("ERRO: focal_argument é obrigatório no MVP mas não foi fornecido pelo LLM!")
            # Fallback: criar focal_argument mínimo
            focal_argument = {
                "intent": "unclear",
                "subject": "not specified",
                "population": "not specified",
                "metrics": "not specified",
                "article_type": "unclear"
            }
            logger.warning(f"Usando focal_argument fallback: {focal_argument}")

        # BUGFIX: Merge inteligente com focal_argument anterior para preservar contexto
        # Evita perda de informações como população e métricas entre turnos
        # IMPORTANTE: Preserva valores anteriores mesmo após rejeição do Methodologist
        if previous_focal:
            logger.info("Mesclando focal_argument novo com anterior para preservar contexto...")
            focal_argument_before_merge = focal_argument.copy()
            focal_argument = _merge_focal_argument(previous_focal, focal_argument)
            # Log se algum valor foi preservado
            if focal_argument != focal_argument_before_merge:
                logger.info("✅ Valores preservados do focal_argument anterior após merge")
            logger.debug(f"Focal argument após merge: {json.dumps(focal_argument, indent=2, ensure_ascii=False)}")

        # Validar next_step
        valid_next_steps = ["explore", "suggest_agent", "clarify"]
        if next_step not in valid_next_steps:
            logger.warning(f"next_step inválido '{next_step}'. Usando 'explore' como padrão.")
            next_step = "explore"

        # Validar consistência: se next_step="suggest_agent", agent_suggestion deve existir
        if next_step == "suggest_agent" and not agent_suggestion:
            logger.warning("next_step='suggest_agent' mas agent_suggestion é None. Mudando para 'explore'.")
            next_step = "explore"
            message = "Preciso entender melhor o contexto. Me conta mais sobre sua ideia?"

        # Detectar mudança de direção (7.8)
        if previous_focal and focal_argument:
            prev_intent = previous_focal.get('intent')
            new_intent = focal_argument.get('intent')
            if prev_intent and new_intent and prev_intent != new_intent and prev_intent != 'unclear' and new_intent != 'unclear':
                logger.info(f"🔄 MUDANÇA DE DIREÇÃO DETECTADA: {prev_intent} → {new_intent}")

        # Logs MVP
        logger.info(f"Raciocínio: {reasoning[:100]}...")
        logger.info(f"Argumento focal: intent={focal_argument.get('intent')}, subject={focal_argument.get('subject', 'N/A')[:50]}")
        logger.info(f"🧠 Modelo cognitivo: claim={cognitive_model_dict.get('claim', 'N/A')[:50]}...")
        logger.info(f"Próximo passo: {next_step}")
        logger.info(f"Mensagem ao usuário: {message[:100]}...")
        if agent_suggestion:
            logger.info(f"Sugestão de agente: {agent_suggestion.get('agent', 'N/A')}")
        if reflection_prompt:
            logger.info(f"💭 Provocação de reflexão: {reflection_prompt[:80]}...")
        if stage_suggestion:
            logger.info(f"🎯 Sugestão de estágio: {stage_suggestion.get('from_stage')} → {stage_suggestion.get('to_stage')}")

        # === CONSULTA AO OBSERVER (Épico 13.3) ===
        # Observer fornece insights; Orquestrador decide como agir
        observer_analysis = _consult_observer(
            state=state,
            user_input=state["user_input"],
            cognitive_model=cognitive_model_dict
        )

        clarity_evaluation = observer_analysis.get("clarity_evaluation")
        variation_analysis = observer_analysis.get("variation_analysis")

        # Checkpoint contextual (Épico 13.4)
        # Se Observer detectou que precisa checkpoint, ajustar resposta
        if observer_analysis.get("needs_checkpoint"):
            checkpoint_reason = observer_analysis.get("checkpoint_reason", "")
            logger.info(f"⚠️ Checkpoint sugerido: {checkpoint_reason[:100]}...")

            # Se clarity_evaluation tem sugestão, incluir na mensagem
            if clarity_evaluation and clarity_evaluation.get("suggestion"):
                # Ajustar next_step para clarify se ainda não era
                if next_step != "clarify":
                    logger.info("📋 Ajustando next_step para 'clarify' devido ao checkpoint")
                    next_step = "clarify"

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON do orquestrador: {e}")
        logger.error(f"Resposta recebida: {response.content[:300]}...")
        
        # Log de erro
        structured_logger.log_error(
            trace_id=trace_id,
            agent="orchestrator",
            node="orchestrator_node",
            error=e,
            metadata={"response_preview": response.content[:200] if hasattr(response, 'content') else "N/A"}
        )
        
        # Fallback seguro
        reasoning = "Erro ao processar resposta do orquestrador"
        # BUGFIX: Preservar focal_argument anterior mesmo em caso de erro
        if previous_focal:
            logger.warning("Erro ao parsear JSON, mas preservando focal_argument anterior")
            focal_argument = previous_focal.copy()
        else:
            focal_argument = {
                "intent": "unclear",
                "subject": "not specified",
                "population": "not specified",
                "metrics": "not specified",
                "article_type": "unclear"
            }
        # Fallback para cognitive_model (Épico 9.1)
        cognitive_model_dict = _create_fallback_cognitive_model(state)
        next_step = "explore"
        message = "Desculpe, tive dificuldade em processar. Pode reformular sua ideia?"
        agent_suggestion = None
        reflection_prompt = None
        stage_suggestion = None
        # Fallback para Observer (Épico 13.3)
        clarity_evaluation = None
        variation_analysis = None

    # Extrair tokens e custo da resposta (Épico 8.3)
    try:
        logger.debug(f"[TOKEN EXTRACTION] Tentando extrair tokens de response (tipo: {type(response)})")
        metrics = extract_tokens_and_cost(response, model_name)
        logger.debug(f"[TOKEN EXTRACTION] ✅ Métricas extraídas: {metrics['tokens_total']} tokens, ${metrics['cost']:.6f}")
    except Exception as e:
        logger.error(f"[TOKEN EXTRACTION] ❌ Erro ao extrair tokens: {e}")
        import traceback
        traceback.print_exc()
        # Fallback: métricas zeradas
        metrics = {"tokens_input": 0, "tokens_output": 0, "tokens_total": 0, "cost": 0.0}
    
    # Calcular duração
    duration_ms = (time.time() - start_time) * 1000
    
    # Log de conclusão
    structured_logger.log_agent_complete(
        trace_id=trace_id,
        agent="orchestrator",
        node="orchestrator_node",
        metadata={
            "duration_ms": duration_ms,
            "tokens_input": metrics.get("tokens_input", 0),
            "tokens_output": metrics.get("tokens_output", 0),
            "tokens_total": metrics.get("tokens_total", 0),
            "cost": metrics.get("cost", 0.0)
        }
    )

    logger.info("=== NÓ ORCHESTRATOR SOCRÁTICO: Finalizado ===\n")

    # E-PROTO2-3.3: manchete "🎯 Foco atualizado" quando o focal_argument
    # efetivamente muda em relação ao turno anterior (em ao menos um campo
    # não-vazio relevante). Turno conversacional puro não preenche o campo
    # — Revelar não lê change_summary, mudança é puramente aditiva.
    ak: dict = {"agent": "orchestrator"}
    if previous_focal and focal_argument:
        relevant_keys = ("intent", "subject", "population", "metrics", "article_type")
        for k in relevant_keys:
            old_v = (previous_focal.get(k) or "")
            new_v = (focal_argument.get(k) or "")
            if new_v and new_v not in ("not specified", "unclear") and new_v != old_v:
                ak["change_summary"] = "🎯 Foco atualizado"
                break
    elif focal_argument and not previous_focal:
        # Primeiro foco da sessão também é uma mudança de estado.
        for k in ("intent", "subject", "population", "metrics", "article_type"):
            v = focal_argument.get(k) or ""
            if v and v not in ("not specified", "unclear"):
                ak["change_summary"] = "🎯 Foco atualizado"
                break

    ai_message = AIMessage(content=message, additional_kwargs=ak)

    # Criar snapshot se argumento maduro (Épico 9.3)
    # Silencioso: não notifica usuário, apenas log interno
    if active_idea_id and cognitive_model_dict:
        try:
            cognitive_model_instance = CognitiveModel(**cognitive_model_dict)
            snapshot_id = create_snapshot_if_mature(
                idea_id=active_idea_id,
                cognitive_model=cognitive_model_instance,
                confidence_threshold=0.8  # Threshold configurável
            )
            if snapshot_id:
                logger.info(f"📸 Snapshot automático criado: {snapshot_id[:8]}...")
        except Exception as e:
            # Silencioso: falha não bloqueia fluxo
            logger.debug(f"Snapshot não criado: {e}")

    return {
        "orchestrator_analysis": reasoning,
        "focal_argument": focal_argument,
        "cognitive_model": cognitive_model_dict,
        "next_step": next_step,
        "agent_suggestion": agent_suggestion,
        "reflection_prompt": reflection_prompt,
        "stage_suggestion": stage_suggestion,
        # Observer analysis (Épico 13.3)
        "clarity_evaluation": clarity_evaluation,
        "variation_analysis": variation_analysis,
        # Métricas
        "last_agent_tokens_input": metrics["tokens_input"],
        "last_agent_tokens_output": metrics["tokens_output"],
        "last_agent_cost": metrics["cost"],
        "messages": [ai_message]
    }
