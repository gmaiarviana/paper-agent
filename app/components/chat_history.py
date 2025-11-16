"""
Componente de histórico de chat para interface web conversacional (Épico 9.3).

Responsável por:
- Renderizar histórico de mensagens da sessão
- Exibir métricas inline discretas (tokens, custo, tempo)
- Scroll automático para última mensagem
- Formatação diferenciada para usuário vs sistema

Versão: 2.0
Data: 16/11/2025
Status: Protótipo completo (com localStorage - Épico 9.9)
"""

import streamlit as st
from typing import List, Dict, Any
import logging

# Import localStorage (Épico 9.9 - Protótipo)
from app.components.storage import load_session_messages

logger = logging.getLogger(__name__)


def render_chat_history(session_id: str) -> None:
    """
    Renderiza histórico de mensagens da sessão ativa.

    Args:
        session_id: ID da sessão ativa

    Comportamento POC (9.3):
        - Exibe mensagens de st.session_state.messages
        - Formatação diferenciada (usuário vs sistema)
        - Métricas inline discretas (após 8.3)

    Estrutura de mensagem esperada:
        {
            "role": "user" | "assistant",
            "content": str,
            "tokens": {"input": int, "output": int, "total": int},
            "cost": float,
            "duration": float,
            "timestamp": str (ISO)
        }

    TODO (após Épico 8.2/8.3):
        - Consumir métricas reais do EventBus
        - Sincronizar com localStorage (9.9)
        - Auto-scroll para última mensagem
    """
    # Inicializar histórico se não existir
    if "messages" not in st.session_state:
        # Tentar carregar do localStorage primeiro (Épico 9.9 - Protótipo)
        loaded_messages = load_session_messages(session_id)

        if loaded_messages and len(loaded_messages) > 0:
            # Histórico encontrado no localStorage
            st.session_state.messages = loaded_messages
            logger.info(f"Histórico carregado do localStorage: {len(loaded_messages)} mensagens")
        else:
            # Nenhum histórico salvo - iniciar nova sessão
            st.session_state.messages = []
            # Mensagem de boas-vindas
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Olá! Me conte sobre sua ideia ou observação.",
                "tokens": None,
                "cost": None,
                "duration": None,
                "timestamp": None
            })

    # Renderizar mensagens
    for message in st.session_state.messages:
        _render_message(message)


def _render_message(message: Dict[str, Any]) -> None:
    """
    Renderiza uma mensagem individual com formatação apropriada.

    Args:
        message: Dicionário com role, content e metadados
    """
    role = message.get("role", "assistant")
    content = message.get("content", "")
    tokens = message.get("tokens")
    cost = message.get("cost")
    duration = message.get("duration")

    # Avatar baseado no role
    avatar = "🧑" if role == "user" else "🤖"

    # Container da mensagem
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

        # Métricas inline (se disponíveis)
        if tokens or cost or duration:
            _render_inline_metrics(tokens, cost, duration)


def _render_inline_metrics(
    tokens: Dict[str, int] | None,
    cost: float | None,
    duration: float | None
) -> None:
    """
    Renderiza métricas inline discretas.

    TODO (após Épico 8.3):
        - Integrar com métricas consolidadas do EventBus
        - Formatação compacta e discreta

    Args:
        tokens: {"input": int, "output": int, "total": int}
        cost: Custo em USD
        duration: Tempo em segundos

    Layout:
        💰 $0.0012 · 215 tokens · 1.2s
    """
    metrics_parts = []

    if cost is not None:
        metrics_parts.append(f"💰 ${cost:.4f}")

    if tokens is not None:
        total_tokens = tokens.get("total", 0)
        if total_tokens > 0:
            metrics_parts.append(f"{total_tokens} tokens")

    if duration is not None:
        metrics_parts.append(f"{duration:.1f}s")

    if metrics_parts:
        metrics_text = " · ".join(metrics_parts)
        st.caption(metrics_text)


def clear_history() -> None:
    """
    Limpa histórico de mensagens da sessão atual.

    Útil para "Nova conversa" ou reset de sessão.
    """
    if "messages" in st.session_state:
        st.session_state.messages = []
