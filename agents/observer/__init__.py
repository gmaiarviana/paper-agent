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
- catalog: ConceptCatalog - Persistencia ChromaDB + SQLite (10.3)
- embeddings: Geracao de embeddings semanticos (10.3)
- concept_pipeline: Pipeline de deteccao e persistencia de conceitos (10.4)

Versao: 2.2 (Epico 10.4 - Pipeline de Conceitos)
Data: 07/12/2025

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

    # Catalogo de Conceitos (10.3)
    "ConceptCatalog",
    "Concept",
    "SimilarConcept",
    "get_concept_catalog",
    "SIMILARITY_THRESHOLD_SAME",
    "SIMILARITY_THRESHOLD_AUTO",

    # Embeddings (10.3)
    "generate_embedding",
    "generate_embeddings_batch",
    "calculate_similarity",
    "get_embedding_dimensions",
    "get_model_name",

    # Pipeline de Conceitos (10.4)
    "persist_concepts",
    "persist_concepts_batch",
    "ConceptPersistResult",
]

__version__ = "2.2.0"
__author__ = "Paper Agent Team"
