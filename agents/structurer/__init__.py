"""
Módulo do agente Estruturador.

Este módulo contém o agente responsável por:
- Organizar ideias vagas em questões de pesquisa estruturadas
- Extrair elementos: contexto, problema, contribuição potencial
- Preparar input para validação pelo Metodologista

Componentes:
    - nodes: structurer_node (nó de estruturação)

Versão: 1.0 (Épico 3, Funcionalidade 3.2)
Data: 11/11/2025
"""

from .nodes import structurer_node

__all__ = [
    "structurer_node",
]
