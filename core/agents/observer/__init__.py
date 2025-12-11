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
- Identificar necessidades de esclarecimento e sugerir perguntas

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
- catalog: ConceptCatalog - Persistencia ChromaDB + SQLite
- embeddings: Geracao de embeddings semanticos
- concept_pipeline: Pipeline de deteccao e persistencia de conceitos
- clarification: Consultas inteligentes e perguntas de esclarecimento
- clarification_prompts: Prompts para esclarecimento

Example:
    >>> from core.agents.observer import ObservadorAPI
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
    - core/docs/architecture/agents/observer/architecture.md - Arquitetura tecnica
    - core/docs/architecture/data-models/ontology.md - CognitiveModel e Conceitos
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
from .catalog import (
    ConceptCatalog,
    Concept,
    SimilarConcept,
    get_concept_catalog,
    SIMILARITY_THRESHOLD_SAME,
    SIMILARITY_THRESHOLD_AUTO
)
from .embeddings import (
    generate_embedding,
    generate_embeddings_batch,
    calculate_similarity,
    get_embedding_dimensions,
    get_model_name
)
from .concept_pipeline import (
    persist_concepts,
    persist_concepts_batch,
    ConceptPersistResult
)
from .clarification import (
    identify_clarification_needs,
    generate_contradiction_question,
    suggest_question_for_gap,
    should_ask_clarification,
    analyze_clarification_response,
    update_clarification_persistence,
    get_clarification_summary_for_timeline,
)

__all__ = [
    # API principal
    "ObservadorAPI",

    # Estado e tipos
    "ObserverState",
    "ObserverInsight",
    "create_initial_observer_state",

    # Processamento
    "process_turn",
    "ObserverProcessor",

    # Metricas
    "calculate_solidez",
    "calculate_completude",
    "calculate_metrics",
    "evaluate_maturity",

    # Extratores
    "extract_claims",
    "extract_concepts",
    "extract_fundamentos",
    "detect_contradictions",
    "identify_open_questions",
    "extract_all",

    # Catalogo de Conceitos
    "ConceptCatalog",
    "Concept",
    "SimilarConcept",
    "get_concept_catalog",
    "SIMILARITY_THRESHOLD_SAME",
    "SIMILARITY_THRESHOLD_AUTO",

    # Embeddings
    "generate_embedding",
    "generate_embeddings_batch",
    "calculate_similarity",
    "get_embedding_dimensions",
    "get_model_name",

    # Pipeline de Conceitos
    "persist_concepts",
    "persist_concepts_batch",
    "ConceptPersistResult",

    # Clarification - Consultas Inteligentes
    "identify_clarification_needs",
    "generate_contradiction_question",
    "suggest_question_for_gap",
    "should_ask_clarification",
    "analyze_clarification_response",
    "update_clarification_persistence",
    "get_clarification_summary_for_timeline",
]

__version__ = "3.0.0"
__author__ = "Paper Agent Team"
