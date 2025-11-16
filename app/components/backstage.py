"""
Componente "Bastidores" para visualização de reasoning dos agentes (Épico 9.6-9.8).

Responsável por:
- Painel collapsible para reasoning dos agentes
- Exibir agente ativo + reasoning resumido (~280 chars)
- Modal com reasoning completo (JSON estruturado)
- Timeline de agentes anteriores
- Polling de eventos do EventBus (1s)

Versão: 1.0
Data: 16/11/2025
Status: Esqueleto (aguardando Épico 8.2 para reasoning instrumentado)
"""

import streamlit as st
from typing import Dict, Any, List, Optional


def render_backstage(session_id: str) -> None:
    """
    Renderiza painel "Bastidores" com reasoning dos agentes.

    Args:
        session_id: ID da sessão ativa

    Comportamento Protótipo (9.6-9.8):
        - Toggle "🔍 Ver raciocínio" (fechado por padrão)
        - Quando aberto: mostra agente ativo + reasoning resumido
        - Botão "Ver raciocínio completo" abre modal com JSON
        - Métricas do agente (tempo, tokens, custo)
        - Timeline colapsada de agentes anteriores

    TODO (após Épico 8.2):
        - Polling de eventos do EventBus (1s)
        - Consumir reasoning dos agentes (orchestrator, structurer, methodologist)
        - Atualizar em tempo real quando eventos chegam
    """
    # Toggle para mostrar/ocultar bastidores
    show_backstage = st.toggle("🔍 Ver raciocínio", value=False, key="toggle_backstage")

    if not show_backstage:
        return

    st.markdown("---")

    # TODO: Implementar após Épico 8.2
    # reasoning = _get_latest_reasoning(session_id)

    # Placeholder para desenvolvimento
    st.info("🚧 **Em desenvolvimento:** Reasoning dos agentes será exibido após Épico 8.2")

    # Exemplo de estrutura (para referência futura)
    _render_backstage_placeholder()


def _render_backstage_placeholder() -> None:
    """
    Placeholder visual para desenvolvimento.
    Remove após implementação real.
    """
    st.subheader("🧠 Orquestrador (exemplo)")

    # Reasoning resumido
    st.write(
        "Usuário tem observação vaga. Preciso contexto: "
        "onde observou, em que projeto, qual métrica específica..."
    )

    # Botão para ver completo
    if st.button("📄 Ver raciocínio completo", key="view_full_reasoning"):
        with st.expander("Raciocínio Completo", expanded=True):
            example_reasoning = {
                "agent": "orchestrator",
                "reasoning": "Analisei o input do usuário. É uma observação vaga...",
                "next_step": "explore",
                "message": "Interessante! Em que contexto você observou isso?",
                "agent_suggestion": None,
                "tokens": {"input": 120, "output": 95, "total": 215},
                "cost": 0.0012,
                "duration": 1.2,
                "timestamp": "2025-11-16T10:30:00Z"
            }
            st.json(example_reasoning)

    # Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("⏱️ Tempo", "1.2s")
    col2.metric("💰 Custo", "$0.0012")
    col3.metric("📊 Tokens", "215")

    # Timeline colapsada
    with st.expander("▼ Timeline de agentes anteriores"):
        st.caption("Nenhum evento anterior nesta sessão")


def _get_latest_reasoning(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Busca reasoning mais recente do EventBus via polling.

    TODO: Implementar após Épico 8.2

    Args:
        session_id: ID da sessão ativa

    Returns:
        dict ou None: {
            "agent": str,
            "reasoning": str,
            "summary": str (280 chars),
            "tokens": {...},
            "cost": float,
            "duration": float,
            "timestamp": str
        }
    """
    raise NotImplementedError("Aguardando Épico 8.2")


def _render_active_agent(reasoning: Dict[str, Any]) -> None:
    """
    Renderiza informações do agente ativo.

    TODO: Implementar após Épico 8.2

    Args:
        reasoning: Dados do agente ativo
    """
    raise NotImplementedError("Aguardando Épico 8.2")


def _render_agent_timeline(session_id: str) -> None:
    """
    Renderiza timeline de agentes anteriores.

    TODO: Implementar após Épico 8.2

    Args:
        session_id: ID da sessão ativa
    """
    raise NotImplementedError("Aguardando Épico 8.2")


def _poll_events(session_id: str, interval: int = 1) -> List[Dict[str, Any]]:
    """
    Faz polling de novos eventos do EventBus.

    TODO: Implementar na fase POC (9.5)

    Args:
        session_id: ID da sessão ativa
        interval: Intervalo de polling em segundos (default: 1s)

    Returns:
        Lista de novos eventos desde último poll
    """
    raise NotImplementedError("Aguardando implementação de polling (9.5)")
