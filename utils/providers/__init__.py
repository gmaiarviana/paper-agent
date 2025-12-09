"""
Providers de LLM (Language Model Providers).

Este módulo contém implementações de diferentes providers de LLM:
- Anthropic (Claude)
- Maritaca AI (Sabiazinho, Sabiá, etc.)

A abstração permite trocar providers sem modificar o código dos agentes.
"""

from .anthropic import AnthropicProvider
from .maritaca import MaritacaProvider

__all__ = ["AnthropicProvider", "MaritacaProvider"]

