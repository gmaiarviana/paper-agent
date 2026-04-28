"""
Providers de LLM (Language Model Providers).

Este módulo contém implementações de diferentes providers de LLM:
- Anthropic (Claude)

A abstração permite trocar providers sem modificar o código dos agentes.
"""

from .anthropic import AnthropicProvider

__all__ = ["AnthropicProvider"]
