"""
Singleton pattern para EventBus.

Este módulo fornece a função get_event_bus() que retorna uma instância
global única do EventBus.
"""

import logging
from typing import Optional

from .core import EventBusCore
from .publishers import EventBusPublishers
from .readers import EventBusReaders

logger = logging.getLogger(__name__)

# Classe EventBus completa combinando todos os mixins
class EventBus(EventBusCore, EventBusPublishers, EventBusReaders):
    r"""
    Barramento de eventos baseado em arquivos temporários.

    Publica eventos em arquivos JSON temporários que podem ser lidos pelo
    Dashboard Streamlit em tempo real. Cada sessão tem seu próprio arquivo.

    Estrutura do arquivo:
        {temp_dir}/paper-agent-events/events-{session_id}.json
        Onde {temp_dir} é:
        - Windows: C:\Users\{user}\AppData\Local\Temp\
        - Linux: /tmp/
        - Mac: /var/folders/.../

        Conteúdo:
        {
            "session_id": "cli-session-abc123",
            "events": [
                {...},  # AgentStartedEvent
                {...},  # AgentCompletedEvent
                ...
            ]
        }

    Example:
        >>> bus = EventBus()
        >>> bus.publish_agent_started("session-1", "orchestrator")
        >>> bus.publish_agent_completed(
        ...     "session-1", "orchestrator",
        ...     summary="Classificou como vague",
        ...     tokens_input=100, tokens_output=50
        ... )
        >>> events = bus.get_session_events("session-1")
        >>> len(events)
        2
    """

    pass  # Herda todos os métodos dos mixins

# Instância global do EventBus (singleton pattern)
_event_bus_instance: Optional[EventBus] = None

def get_event_bus() -> EventBus:
    """
    Retorna instância global do EventBus (singleton).

    Returns:
        EventBus: Instância única do EventBus

    Example:
        >>> bus1 = get_event_bus()
        >>> bus2 = get_event_bus()
        >>> bus1 is bus2
        True
    """
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = EventBus()
    return _event_bus_instance

