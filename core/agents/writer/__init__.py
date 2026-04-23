"""Agente Escritor (Writer) — C-ENSAIO-2.

Gera artigos em markdown a partir de contexto conversacional + argumento focal.
Nó simples, stateless, invocável isoladamente pelo produto consumidor.
"""

from core.agents.writer.nodes import writer_node

__all__ = ["writer_node"]
