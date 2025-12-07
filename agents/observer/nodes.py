"""
Nos do grafo do agente Observador.

Este modulo implementa o no principal do Observador:
- process_turn: Processa cada turno e atualiza CognitiveModel

O Observador trabalha SILENCIOSAMENTE em paralelo ao Orquestrador,
monitorando a conversa e catalogando a evolucao do raciocinio.

Versao: 1.0 (Epico 10.2)
Data: 05/12/2025
"""

import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from .state import ObserverState, ObserverInsight, create_initial_observer_state
from .extractors import extract_all
from .metrics import calculate_metrics, evaluate_maturity

logger = logging.getLogger(__name__)


def process_turn(
    user_input: str,
    conversation_history: List[Dict[str, Any]],
    previous_cognitive_model: Optional[Dict[str, Any]] = None,
    session_id: Optional[str] = None,
    turn_number: int = 1,
    # Parametros opcionais para Agentic RAG (Epic 12)
    extract_claims: bool = True,
    extract_concepts: bool = True,
    extract_fundamentos: bool = True,
    detect_contradictions: bool = True,
    calculate_metrics_flag: bool = True
) -> Dict[str, Any]:
    """
    Processa um turno completo e atualiza o CognitiveModel.

    Esta e a funcao principal do Observador. Ela:
    1. Extrai informacoes semanticas via LLM (claims, conceitos, etc)
    2. Atualiza o CognitiveModel em memoria
    3. Calcula metricas (solidez, completude)
    4. Publica eventos para Dashboard
    5. Retorna estado atualizado

    IMPORTANTE: Esta funcao e SILENCIOSA - nao interfere no fluxo
    conversacional do Orquestrador.

    Args:
        user_input: Mensagem atual do usuario.
        conversation_history: Historico completo da conversa.
        previous_cognitive_model: CognitiveModel do turno anterior.
        session_id: ID da sessao (para eventos).
        turn_number: Numero do turno atual.
        extract_claims: Se deve extrair claims (default True).
        extract_concepts: Se deve extrair conceitos (default True).
        extract_fundamentos: Se deve extrair fundamentos (default True).
        detect_contradictions: Se deve detectar contradicoes (default True).
        calculate_metrics_flag: Se deve calcular metricas (default True).

    Returns:
        Dict com:
        - cognitive_model: CognitiveModel atualizado
        - extracted: Informacoes extraidas neste turno
        - metrics: Metricas calculadas (solidez, completude)
        - maturity: Avaliacao de maturidade
        - processing_time_ms: Tempo de processamento
        - skipped: Lista de etapas puladas (se houver)

    Example:
        >>> result = process_turn(
        ...     user_input="LLMs aumentam produtividade em 30%",
        ...     conversation_history=[...],
        ...     turn_number=1
        ... )
        >>> print(result['metrics']['solidez'])
        0.35

    Notes:
        Os parametros opcionais (extract_*, calculate_*) permitem
        bypass de etapas especificas para otimizacao (Agentic RAG).
        Por padrao, todas as etapas sao executadas.
    """
    start_time = time.time()
    skipped = []

    logger.info(f"=== OBSERVADOR: Processando turno {turn_number} ===")
    logger.debug(f"Input: {user_input[:100]}...")

    # Verificar quais etapas serao executadas (para Agentic RAG no Epic 12)
    if not extract_claims:
        skipped.append("extract_claims")
    if not extract_concepts:
        skipped.append("extract_concepts")
    if not extract_fundamentos:
        skipped.append("extract_fundamentos")
    if not detect_contradictions:
        skipped.append("detect_contradictions")
    if not calculate_metrics_flag:
        skipped.append("calculate_metrics")

    if skipped:
        logger.info(f"Etapas puladas (Agentic RAG): {skipped}")

    # 1. Extrair informacoes semanticas via LLM
    # TODO (Epic 12): Usar flags para chamar extratores individuais
    logger.info("Extraindo informacoes semanticas...")
    extracted = extract_all(
        user_input=user_input,
        conversation_history=conversation_history
    )

    # 2. Mesclar com CognitiveModel anterior (se existir)
    cognitive_model = _merge_cognitive_model(
        previous=previous_cognitive_model,
        extracted=extracted
    )

    # 3. Calcular metricas
    metrics = calculate_metrics(
        claim=cognitive_model.get("claim", ""),
        claims=extracted.get("claims", []),
        fundamentos=cognitive_model.get("premises", []),
        assumptions=cognitive_model.get("assumptions", []),
        open_questions=cognitive_model.get("open_questions", []),
        contradictions=cognitive_model.get("contradictions", []),
        context=cognitive_model.get("context", {}),
        solid_grounds=cognitive_model.get("solid_grounds", [])
    )

    # 4. Avaliar maturidade (via LLM com contexto completo)
    maturity = evaluate_maturity(
        solidez=metrics["solidez"],
        completude=metrics["completude"],
        open_questions=cognitive_model.get("open_questions", []),
        contradictions=cognitive_model.get("contradictions", []),
        claims=extracted.get("claims", []),
        fundamentos=cognitive_model.get("premises", [])
    )

    # 5. Publicar eventos (se session_id fornecido)
    if session_id:
        _publish_cognitive_model_event(
            session_id=session_id,
            cognitive_model=cognitive_model,
            metrics=metrics,
            turn_number=turn_number
        )

    # Calcular tempo de processamento
    processing_time_ms = (time.time() - start_time) * 1000

    logger.info(
        f"=== OBSERVADOR: Turno {turn_number} processado em {processing_time_ms:.0f}ms ==="
    )
    logger.info(
        f"Metricas: solidez={metrics['solidez']:.0%}, completude={metrics['completude']:.0%}"
    )

    return {
        "cognitive_model": cognitive_model,
        "extracted": extracted,
        "metrics": metrics,
        "maturity": maturity,
        "processing_time_ms": processing_time_ms,
        "turn_number": turn_number,
        "skipped": skipped  # Etapas puladas (para Agentic RAG)
    }


def _merge_cognitive_model(
    previous: Optional[Dict[str, Any]],
    extracted: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Mescla CognitiveModel anterior com informacoes extraidas.

    Esta funcao implementa a logica de acumulacao do CognitiveModel:
    - Claims novos substituem anteriores (evolucao)
    - Conceitos acumulam (nao perde conceitos anteriores)
    - Fundamentos acumulam
    - Open questions sao substituidas (refletem estado atual)
    - Contradicoes acumulam (historico)

    Args:
        previous: CognitiveModel do turno anterior.
        extracted: Informacoes extraidas neste turno.

    Returns:
        CognitiveModel mesclado.
    """
    if not previous:
        # Primeiro turno - criar modelo inicial
        return {
            "claim": extracted.get("claims", [""])[0] if extracted.get("claims") else "",
            "premises": extracted.get("fundamentos", []),
            "assumptions": [],  # Sera preenchido pelo Orquestrador
            "open_questions": extracted.get("open_questions", []),
            "contradictions": [
                {
                    "description": c.get("explanation", ""),
                    "confidence": c.get("confidence", 0.80),
                    "suggested_resolution": None
                }
                for c in extracted.get("contradictions", [])
            ],
            "solid_grounds": [],
            "context": {},
            # Campos adicionais do Observador
            "concepts_detected": extracted.get("concepts", [])
        }

    # Mesclar com modelo anterior
    merged = previous.copy()

    # Claims: pegar o mais recente (se houver)
    new_claims = extracted.get("claims", [])
    if new_claims:
        merged["claim"] = new_claims[0]

    # Premises/Fundamentos: acumular (evitar duplicatas)
    existing_premises = set(merged.get("premises", []))
    for fundamento in extracted.get("fundamentos", []):
        if fundamento not in existing_premises:
            merged.setdefault("premises", []).append(fundamento)

    # Open questions: substituir (refletem estado atual)
    new_questions = extracted.get("open_questions", [])
    if new_questions:
        merged["open_questions"] = new_questions

    # Contradicoes: acumular (evitar duplicatas por descricao)
    existing_descriptions = {c.get("description", "") for c in merged.get("contradictions", [])}
    for contradiction in extracted.get("contradictions", []):
        desc = contradiction.get("explanation", "")
        if desc and desc not in existing_descriptions:
            merged.setdefault("contradictions", []).append({
                "description": desc,
                "confidence": contradiction.get("confidence", 0.80),
                "suggested_resolution": None
            })

    # Conceitos: acumular (biblioteca global)
    existing_concepts = set(merged.get("concepts_detected", []))
    for concept in extracted.get("concepts", []):
        if concept not in existing_concepts:
            merged.setdefault("concepts_detected", []).append(concept)

    return merged


def _publish_cognitive_model_event(
    session_id: str,
    cognitive_model: Dict[str, Any],
    metrics: Dict[str, Any],
    turn_number: int
) -> None:
    """
    Publica evento CognitiveModelUpdatedEvent no EventBus.

    Args:
        session_id: ID da sessao.
        cognitive_model: CognitiveModel atualizado.
        metrics: Metricas calculadas.
        turn_number: Numero do turno.
    """
    try:
        from utils.event_bus import get_event_bus
        from .metrics import evaluate_maturity

        event_bus = get_event_bus()

        # Avaliar maturidade para o evento (via LLM)
        maturity = evaluate_maturity(
            solidez=metrics["solidez"],
            completude=metrics["completude"],
            open_questions=cognitive_model.get("open_questions", []),
            contradictions=cognitive_model.get("contradictions", []),
            claims=[cognitive_model.get("claim", "")] if cognitive_model.get("claim") else [],
            fundamentos=cognitive_model.get("premises", [])
        )

        # Publicar evento especifico do CognitiveModel (Epico 10.2)
        event_bus.publish_cognitive_model_updated(
            session_id=session_id,
            turn_number=turn_number,
            solidez=metrics["solidez"],
            completude=metrics["completude"],
            claims_count=1 if cognitive_model.get("claim") else 0,
            premises_count=len(cognitive_model.get("premises", [])),
            concepts_count=len(cognitive_model.get("concepts_detected", [])),
            open_questions_count=len(cognitive_model.get("open_questions", [])),
            contradictions_count=len(cognitive_model.get("contradictions", [])),
            is_mature=maturity["is_mature"],
            metadata={
                "claim": cognitive_model.get("claim", "")[:100],  # Truncar para nao poluir evento
                "maturity_reason": maturity.get("reason", "")
            }
        )

        logger.debug(f"CognitiveModelUpdatedEvent publicado para sessao {session_id}")

    except Exception as e:
        # Silencioso - nao bloqueia fluxo se evento falhar
        logger.debug(f"Nao foi possivel publicar evento: {e}")


class ObserverProcessor:
    """
    Processador de turnos do Observador com estado persistente.

    Esta classe encapsula o processamento de turnos mantendo
    o CognitiveModel em memoria entre chamadas.

    Attributes:
        cognitive_model: CognitiveModel atual.
        concepts: Lista de conceitos detectados.
        turn_count: Numero de turnos processados.
        session_id: ID da sessao (para eventos).

    Example:
        >>> processor = ObserverProcessor(session_id="session-123")
        >>> result = processor.process("LLMs aumentam produtividade")
        >>> print(processor.get_solidez())
        0.35
    """

    def __init__(self, session_id: Optional[str] = None):
        """
        Inicializa processador.

        Args:
            session_id: ID da sessao (opcional, para eventos).
        """
        self.cognitive_model: Dict[str, Any] = {}
        self.concepts: List[str] = []
        self.turn_count: int = 0
        self.session_id = session_id
        self._conversation_history: List[Dict[str, Any]] = []

        logger.info(f"ObserverProcessor inicializado (session={session_id})")

    def process(self, user_input: str) -> Dict[str, Any]:
        """
        Processa um turno e retorna resultado.

        Args:
            user_input: Mensagem do usuario.

        Returns:
            Resultado do processamento (cognitive_model, metrics, etc).
        """
        self.turn_count += 1

        # Adicionar ao historico
        self._conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Processar turno
        result = process_turn(
            user_input=user_input,
            conversation_history=self._conversation_history,
            previous_cognitive_model=self.cognitive_model,
            session_id=self.session_id,
            turn_number=self.turn_count
        )

        # Atualizar estado interno
        self.cognitive_model = result["cognitive_model"]
        self.concepts = self.cognitive_model.get("concepts_detected", [])

        return result

    def add_assistant_message(self, content: str) -> None:
        """
        Adiciona mensagem do assistente ao historico.

        Args:
            content: Conteudo da mensagem.
        """
        self._conversation_history.append({
            "role": "assistant",
            "content": content
        })

    def get_cognitive_model(self) -> Dict[str, Any]:
        """Retorna CognitiveModel atual."""
        return self.cognitive_model.copy()

    def get_solidez(self) -> float:
        """Retorna solidez atual."""
        metrics = calculate_metrics(
            claim=self.cognitive_model.get("claim", ""),
            claims=[self.cognitive_model.get("claim", "")] if self.cognitive_model.get("claim") else [],
            fundamentos=self.cognitive_model.get("premises", []),
            assumptions=self.cognitive_model.get("assumptions", []),
            open_questions=self.cognitive_model.get("open_questions", []),
            contradictions=self.cognitive_model.get("contradictions", []),
            context=self.cognitive_model.get("context", {})
        )
        return metrics["solidez"]

    def get_completude(self) -> float:
        """Retorna completude atual."""
        metrics = calculate_metrics(
            claim=self.cognitive_model.get("claim", ""),
            claims=[self.cognitive_model.get("claim", "")] if self.cognitive_model.get("claim") else [],
            fundamentos=self.cognitive_model.get("premises", []),
            assumptions=self.cognitive_model.get("assumptions", []),
            open_questions=self.cognitive_model.get("open_questions", []),
            contradictions=self.cognitive_model.get("contradictions", []),
            context=self.cognitive_model.get("context", {})
        )
        return metrics["completude"]

    def get_concepts(self) -> List[str]:
        """Retorna conceitos detectados."""
        return self.concepts.copy()

    def reset(self) -> None:
        """Reseta estado para nova conversa."""
        self.cognitive_model = {}
        self.concepts = []
        self.turn_count = 0
        self._conversation_history = []
        logger.info("ObserverProcessor resetado")
