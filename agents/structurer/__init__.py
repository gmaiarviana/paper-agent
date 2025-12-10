"""
Módulo do agente Estruturador.

Este módulo contém o agente responsável por:
- Organizar ideias vagas em questões de pesquisa estruturadas
- Extrair elementos: contexto, problema, contribuição potencial
- Preparar input para validação pelo Metodologista

Componentes:
    - nodes: structurer_node (nó de estruturação)

"""

from .nodes import structurer_node

__all__ = [
    "structurer_node",
]
