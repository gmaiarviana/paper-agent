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
- prompts: Prompts de extracao via LLM

Versao: 1.0 (Epico 10.1 - Mitose do Orquestrador)
Data: 05/12/2025

Example:
    >>> from agents.observer import ObservadorAPI, ObserverInsight
    >>> api = ObservadorAPI()
    >>> api.update_cognitive_model({"claim": "LLMs aumentam produtividade", ...})
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

__all__ = [
    # API principal
    "ObservadorAPI",

    # Estado e tipos
    "ObserverState",
    "ObserverInsight",
    "create_initial_observer_state",
]

__version__ = "1.0.0"
__author__ = "Paper Agent Team"
