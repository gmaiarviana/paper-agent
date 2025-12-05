"""
Agente Observador (Mente Analitica).

O Observador e responsavel por monitorar a conversa e catalogar a evolucao
do raciocinio. Trabalha SILENCIOSAMENTE em paralelo ao Orquestrador.

Analogia:
    Orquestrador = Ator principal (fala, age, decide)
    Observador = Testemunha silenciosa (ve tudo, cataloga, nao interfere)

Responsabilidades do Observador:
- Monitorar TODA conversa (todo turno, nao apenas snapshots)
- Atualizar CognitiveModel completo (claims, fundamentos, contradicoes, conceitos)
- Extrair conceitos para catalogo (ChromaDB + SQLite)
- Calcular metricas (solidez, completude)
- Responder consultas do Orquestrador (insights, nao comandos)
- Publicar eventos para Dashboard (silencioso)

O que o Observador NAO faz:
- Decidir next_step (quem decide: Orquestrador)
- Falar com usuario (quem fala: Orquestrador)
- Negociar caminhos (quem negocia: Orquestrador)
- Interromper fluxo conversacional

Modulos:
- api: ObservadorAPI - Interface de consulta nao-deterministica
- state: ObserverState - Estado interno do processamento
- nodes: process_turn - Processamento de turnos via LLM
- extractors: Extratores semanticos via LLM
- metrics: Calculo de solidez e completude
- prompts: Prompts de extracao via LLM

Versao: 2.0 (Epico 10.2 - Processamento via LLM)
Data: 05/12/2025

Example:
    >>> from agents.observer import ObservadorAPI
    >>> api = ObservadorAPI(session_id="session-123")
    >>> # Processar turno via LLM
    >>> result = api.process_turn("LLMs aumentam produtividade em 30%")
    >>> print(result['metrics']['solidez'])
    0.35
    >>> # Consultar estado
    >>> insight = api.what_do_you_see(
    ...     context="Usuario mudou de direcao",
    ...     question="Conceitos anteriores ainda relevantes?"
    ... )
    >>> print(insight.confidence)
    0.8

See Also:
    - docs/agents/observer.md - Documentacao completa
    - docs/architecture/observer_architecture.md - Arquitetura tecnica
    - docs/architecture/ontology.md - CognitiveModel e Conceitos
"""

from .api import ObservadorAPI
from .state import (
    ObserverState,
    ObserverInsight,
    create_initial_observer_state
)
from .nodes import process_turn, ObserverProcessor
from .metrics import calculate_solidez, calculate_completude, calculate_metrics, evaluate_maturity
from .extractors import (
    extract_claims,
    extract_concepts,
    extract_fundamentos,
    detect_contradictions,
    identify_open_questions,
    extract_all
)

__all__ = [
    # API principal
    "ObservadorAPI",

    # Estado e tipos
    "ObserverState",
    "ObserverInsight",
    "create_initial_observer_state",

    # Processamento (10.2)
    "process_turn",
    "ObserverProcessor",

    # Metricas (10.2)
    "calculate_solidez",
    "calculate_completude",
    "calculate_metrics",
    "evaluate_maturity",

    # Extratores (10.2)
    "extract_claims",
    "extract_concepts",
    "extract_fundamentos",
    "detect_contradictions",
    "identify_open_questions",
    "extract_all",
]

__version__ = "2.0.0"
__author__ = "Paper Agent Team"
