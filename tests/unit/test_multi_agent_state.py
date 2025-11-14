"""
Testes unitários para MultiAgentState (Épico 7, Task 7.1.5).

Valida estrutura e tipos dos campos do estado compartilhado entre agentes,
especialmente os novos campos do Orquestrador Conversacional.

Versão: 1.0
Data: 14/11/2025
"""

import pytest
from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state


class TestMultiAgentStateStructure:
    """Testes de estrutura e validação do MultiAgentState."""

    def test_state_has_required_fields(self):
        """Valida que MultiAgentState possui todos os campos obrigatórios."""
        # Criar estado inicial
        state = create_initial_multi_agent_state(
            user_input="Teste de input",
            session_id="test-session-123"
        )

        # Campos compartilhados
        assert "user_input" in state
        assert "session_id" in state
        assert "conversation_history" in state
        assert "current_stage" in state
        assert "hypothesis_versions" in state

        # Campos do Orquestrador (Épico 7 - Conversacional)
        assert "orchestrator_analysis" in state
        assert "next_step" in state
        assert "agent_suggestion" in state

        # Campos de outros agentes
        assert "structurer_output" in state
        assert "methodologist_output" in state
        assert "messages" in state

    def test_orchestrator_classification_removed(self):
        """Valida que orchestrator_classification foi removido (obsoleto no POC)."""
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-123"
        )

        # Campos obsoletos não devem existir
        assert "orchestrator_classification" not in state
        assert "orchestrator_reasoning" not in state

    def test_initial_state_values(self):
        """Valida valores iniciais do estado."""
        user_input = "Observei que LLMs aumentam produtividade"
        session_id = "test-session-456"

        state = create_initial_multi_agent_state(user_input, session_id)

        # Compartilhados
        assert state["user_input"] == user_input
        assert state["session_id"] == session_id
        assert state["current_stage"] == "classifying"
        assert len(state["conversation_history"]) == 1
        assert state["conversation_history"][0] == f"Usuário: {user_input}"
        assert state["hypothesis_versions"] == []

        # Orquestrador (Épico 7) - devem começar como None
        assert state["orchestrator_analysis"] is None
        assert state["next_step"] is None
        assert state["agent_suggestion"] is None

        # Outros agentes - devem começar como None
        assert state["structurer_output"] is None
        assert state["methodologist_output"] is None
        assert state["messages"] == []

    def test_orchestrator_analysis_can_be_set(self):
        """Valida que orchestrator_analysis pode ser atualizado."""
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-123"
        )

        # Atualizar campo
        analysis = "Usuário mencionou produtividade mas não especificou métricas"
        state["orchestrator_analysis"] = analysis

        assert state["orchestrator_analysis"] == analysis

    def test_next_step_valid_values(self):
        """Valida que next_step aceita valores válidos."""
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-123"
        )

        # Valores válidos conforme Literal["explore", "suggest_agent", "clarify"]
        valid_values = ["explore", "suggest_agent", "clarify"]

        for value in valid_values:
            state["next_step"] = value
            assert state["next_step"] == value

    def test_agent_suggestion_structure(self):
        """Valida estrutura do campo agent_suggestion."""
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-123"
        )

        # Estrutura esperada: {"agent": str, "justification": str}
        suggestion = {
            "agent": "methodologist",
            "justification": "Usuário definiu população e métricas claras"
        }

        state["agent_suggestion"] = suggestion

        assert state["agent_suggestion"]["agent"] == "methodologist"
        assert state["agent_suggestion"]["justification"] == "Usuário definiu população e métricas claras"

    def test_state_preserves_all_fields_after_update(self):
        """Valida que atualizar um campo não afeta outros."""
        state = create_initial_multi_agent_state(
            user_input="Teste original",
            session_id="test-123"
        )

        original_user_input = state["user_input"]
        original_session_id = state["session_id"]

        # Atualizar campos do Orquestrador
        state["orchestrator_analysis"] = "Análise do contexto"
        state["next_step"] = "explore"
        state["agent_suggestion"] = {"agent": "structurer", "justification": "Input vago"}

        # Campos compartilhados não devem ter mudado
        assert state["user_input"] == original_user_input
        assert state["session_id"] == original_session_id
        assert state["current_stage"] == "classifying"

    def test_conversation_history_is_mutable(self):
        """Valida que conversation_history pode ser expandido."""
        state = create_initial_multi_agent_state(
            user_input="Input inicial",
            session_id="test-123"
        )

        # Adicionar novo item ao histórico
        state["conversation_history"].append("Orquestrador: Explorando contexto")

        assert len(state["conversation_history"]) == 2
        assert state["conversation_history"][1] == "Orquestrador: Explorando contexto"


class TestMultiAgentStateTyping:
    """Testes de typing e anotações do MultiAgentState."""

    def test_state_annotations_exist(self):
        """Valida que MultiAgentState tem anotações de tipo."""
        annotations = MultiAgentState.__annotations__

        # Campos do Orquestrador (Épico 7)
        assert "orchestrator_analysis" in annotations
        assert "next_step" in annotations
        assert "agent_suggestion" in annotations

        # Campos compartilhados
        assert "user_input" in annotations
        assert "session_id" in annotations
        assert "conversation_history" in annotations
        assert "current_stage" in annotations

    def test_next_step_literal_type(self):
        """Valida que next_step usa Literal com valores corretos."""
        annotations = MultiAgentState.__annotations__

        # Obter anotação de next_step
        next_step_annotation = annotations["next_step"]

        # Verificar que é Optional[Literal[...]]
        assert "Literal" in str(next_step_annotation)

    def test_current_stage_literal_type(self):
        """Valida que current_stage usa Literal."""
        annotations = MultiAgentState.__annotations__

        current_stage_annotation = annotations["current_stage"]

        # Verificar que é Literal com valores esperados
        assert "Literal" in str(current_stage_annotation)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
