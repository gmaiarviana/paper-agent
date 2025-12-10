"""
EventBus para comunicação entre CLI/Graph e Dashboard.

Este módulo gerencia publicação e consumo de eventos usando arquivos JSON
temporários. Fornece canal de comunicação entre processo principal (CLI/Graph)
e Dashboard Streamlit.

Estrutura modular:
- core.py: Classe base com persistência (EventBusCore)
- publishers.py: Métodos publish_* (EventBusPublishers)
- readers.py: Métodos get_* e list_* (EventBusReaders)
- singleton.py: Classe EventBus completa e função get_event_bus()

Data: 2025-12-XX
"""

# Importar classe EventBus e função get_event_bus para manter compatibilidade
from .singleton import EventBus, get_event_bus

# Exportar tudo para manter compatibilidade com imports existentes
__all__ = ['EventBus', 'get_event_bus']

