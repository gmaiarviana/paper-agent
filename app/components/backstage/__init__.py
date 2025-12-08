"""
Componentes do Painel Direito: Contexto + Bastidores (Épico 3 + 4).

Responsável por:
- Seção "💡 Contexto" (Épico 4): ideia ativa, status, custo acumulado
- Seção "📊 Bastidores" (Épico 3): reasoning dos agentes, histórico
- Card de pensamento: emoji + nome + reasoning resumido (~280 chars) + link "Ver completo"
- Estado vazio: 🤖 + "Aguardando..." centralizado
- Modal de raciocínio completo (JSON estruturado)
- Modal de detalhes da conversa (custos, métricas)

Estrutura:
┌──────────────────────┐
│ 💡 Contexto [▼]      │  ← Expander (expandido por padrão)
│ └─ Ideia ativa       │
│ └─ Custo acumulado   │
├──────────────────────┤
│ 📊 Bastidores [▶]    │  ← Expander (colapsado por padrão)
│ └─ Reasoning         │
│ └─ Histórico         │
└──────────────────────┘

Versão: 4.2 (Refatorado - modularizado)
Data: 14/12/2025
Status: Épico 3 + 4 implementados
"""

from .context import render_context_section
from .reasoning import render_backstage


def render_right_panel(session_id: str) -> None:
    """
    Renderiza painel direito completo: Contexto + Bastidores (Épico 4.1).

    Args:
        session_id: ID da sessão ativa

    Estrutura:
        1. Seção "💡 Contexto" (expandida por padrão)
           - Ideia ativa (título, status, metadados)
           - Custo acumulado
        2. Seção "📊 Bastidores" (colapsada por padrão)
           - Reasoning dos agentes, histórico
    """
    # Seção 1: Contexto (acima)
    render_context_section(session_id)

    # Seção 2: Bastidores (abaixo)
    render_backstage(session_id)


__all__ = [
    "render_right_panel",
    "render_context_section",
    "render_backstage",
]

