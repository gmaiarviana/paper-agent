"""
Testes para MultiAgentState e create_initial_multi_agent_state.

Cobre:
- Campos obrigatórios do estado inicial
- Mutabilidade do estado
- Estrutura de dados compartilhada
"""

from langchain_core.messages import HumanMessage
from agents.orchestrator.state import create_initial_multi_agent_state


class TestMultiAgentState:
    """Testes para MultiAgentState e create_initial_multi_agent_state."""

    def test_initial_state_has_required_fields(self):
        """Estado inicial possui todos os campos obrigatórios."""
        state = create_initial_multi_agent_state(
            user_input="Teste de input",
            session_id="test-session-1",
        )

        # Campos compartilhados
        assert state['user_input'] == "Teste de input"
        assert state['session_id'] == "test-session-1"
        assert state['conversation_history'] == ["Usuário: Teste de input"]
        assert state['current_stage'] == "classifying"
        assert state['hypothesis_versions'] == []

        # Campos específicos (devem começar None)
        assert state['orchestrator_analysis'] is None
        assert state['next_step'] is None
        assert state['agent_suggestion'] is None
        assert state['focal_argument'] is None
        assert state['reflection_prompt'] is None
        assert state['stage_suggestion'] is None
        assert state['structurer_output'] is None
        assert state['methodologist_output'] is None

        # Mensagens (1 HumanMessage inicial)
        assert len(state['messages']) == 1
        assert isinstance(state['messages'][0], HumanMessage)
        assert state['messages'][0].content == "Teste de input"

    def test_state_is_mutable(self):
        """Campos do estado podem ser atualizados."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        state['next_step'] = "explore"
        state['current_stage'] = "structuring"

        assert state['next_step'] == "explore"
        assert state['current_stage'] == "structuring"

