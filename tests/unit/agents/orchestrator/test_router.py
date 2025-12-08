"""
Testes para route_from_orchestrator - decisão de próximo nó.

Cobre lógica de roteamento baseada em next_step e agent_suggestion:
- Roteamento para usuário (explore, clarify)
- Roteamento para agentes (structurer, methodologist)
- Fallbacks e tratamento de erros
"""

import pytest
from agents.orchestrator.state import create_initial_multi_agent_state
from agents.orchestrator.router import route_from_orchestrator


class TestRouteFromOrchestrator:
    """Testes para route_from_orchestrator - decisão de próximo nó."""

    def test_explore_routes_to_user(self):
        """next_step = explore → retorna para usuário."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "explore"
        state['agent_suggestion'] = None

        assert route_from_orchestrator(state) == "user"

    def test_clarify_routes_to_user(self):
        """next_step = clarify → retorna para usuário."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "clarify"
        state['agent_suggestion'] = None

        assert route_from_orchestrator(state) == "user"

    def test_suggest_structurer_routes_to_structurer(self):
        """Agente sugerido = structurer → roteia para structurer."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = "suggest_agent"
        state["agent_suggestion"] = {
            "agent": "structurer",
            "justification": "Observação não estruturada"
        }

        assert route_from_orchestrator(state) == "structurer"

    def test_suggest_methodologist_routes_to_methodologist(self):
        """Agente sugerido = methodologist → roteia para methodologist."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = "suggest_agent"
        state["agent_suggestion"] = {
            "agent": "methodologist",
            "justification": "Hipótese pronta para validação"
        }

        assert route_from_orchestrator(state) == "methodologist"

    def test_invalid_agent_routes_to_user(self):
        """Agente inválido → fallback para user."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = {
            "agent": "invalid_agent",
            "justification": "Teste"
        }

        assert route_from_orchestrator(state) == "user"

    def test_missing_suggestion_routes_to_user(self):
        """next_step=suggest_agent mas suggestion=None → fallback para user."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = None

        assert route_from_orchestrator(state) == "user"

    def test_none_next_step_raises_error(self):
        """next_step = None → lança ValueError."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = None

        with pytest.raises(ValueError, match="next_step do Orquestrador está None"):
            route_from_orchestrator(state)

    def test_invalid_next_step_raises_error(self):
        """next_step inválido → lança ValueError."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = "invalid_value"

        with pytest.raises(ValueError, match="next_step inválido"):
            route_from_orchestrator(state)

