"""
Agente Writer (C-ENSAIO-2).

Writer simples em uma passada: recebe contexto conversacional + argumento focal
e devolve um artigo completo em markdown. Pode ser reinvocado com previous_article
preenchido para regenerar o artigo inteiro incorporando feedback do histórico.
"""

from core.agents.writer.nodes import writer_node

__all__ = ["writer_node"]
