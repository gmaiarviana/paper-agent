"""
Testes para _build_context - construção de contexto para LLM.

Cobre:
- Construção de contexto com input inicial
- Integração com histórico de conversa
- Preservação de ordem cronológica
- Formatação adequada para LLM
"""

from langchain_core.messages import AIMessage, HumanMessage
from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.orchestrator.nodes import _build_context

class TestBuildContext:
    """Testes para _build_context - construção de contexto para LLM."""

    def test_with_initial_input_only(self):
        """Contexto com apenas input inicial."""
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )

        context = _build_context(state)

        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "Observei que LLMs aumentam produtividade" in context
        assert "HISTÓRICO DA CONVERSA:" in context

    def test_with_conversation_history(self):
        """Contexto com histórico de conversa."""
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )
        state['messages'] = [
            HumanMessage(content="Quero validar essa observação"),
            AIMessage(content="Vou organizar sua ideia em uma questão de pesquisa."),
            HumanMessage(content="Perfeito, obrigado")
        ]

        context = _build_context(state)

        assert "[Usuário]: Quero validar essa observação" in context
        assert "[Assistente]: Vou organizar sua ideia em uma questão de pesquisa." in context
        assert "[Usuário]: Perfeito, obrigado" in context

    def test_preserves_chronological_order(self):
        """Contexto preserva ordem cronológica."""
        state = create_initial_multi_agent_state(user_input="Input", session_id="test")
        state['messages'] = [
            HumanMessage(content="Mensagem 1"),
            AIMessage(content="Resposta 1"),
            HumanMessage(content="Mensagem 2"),
            AIMessage(content="Resposta 2")
        ]

        context = _build_context(state)
        lines = context.split("\n")

        msg1_idx = next(i for i, line in enumerate(lines) if "Mensagem 1" in line)
        resp1_idx = next(i for i, line in enumerate(lines) if "Resposta 1" in line)
        msg2_idx = next(i for i, line in enumerate(lines) if "Mensagem 2" in line)
        resp2_idx = next(i for i, line in enumerate(lines) if "Resposta 2" in line)

        assert msg1_idx < resp1_idx < msg2_idx < resp2_idx

    def test_empty_messages_omits_history_section(self):
        """Lista vazia de mensagens omite seção de histórico."""
        state = create_initial_multi_agent_state(user_input="Input", session_id="test")
        state['messages'] = []

        context = _build_context(state)

        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "HISTÓRICO DA CONVERSA:" not in context

    def test_format_is_llm_friendly(self):
        """Formato é adequado para LLM (estrutura clara)."""
        state = create_initial_multi_agent_state(user_input="Observei X", session_id="test")
        state['messages'] = [
            AIMessage(content="Pergunta"),
            HumanMessage(content="Resposta")
        ]

        context = _build_context(state)

        assert context.startswith("INPUT INICIAL DO USUÁRIO:")
        assert "[Usuário]:" in context
        assert "[Assistente]:" in context

    def test_preserves_direction_change_context(self):
        """Contexto preserva mudanças de direção para detecção pelo LLM."""
        state = create_initial_multi_agent_state(
            user_input="Quero estudar impacto de LLMs em produtividade",
            session_id="test"
        )
        state['messages'] = [
            AIMessage(content="Vamos explorar produtividade então"),
            HumanMessage(content="Na verdade, quero focar em qualidade de código")
        ]

        context = _build_context(state)

        assert "produtividade" in context
        assert "qualidade de código" in context

