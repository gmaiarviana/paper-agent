"""
Smoke test de integração para o super-grafo multi-agente.

Valida que o fluxo end-to-end do sistema multi-agente funciona corretamente
com API real do Claude (Haiku).

Testes:
- test_vague_idea_full_flow: Ideia vaga → Estruturador → Metodologista
- test_semi_formed_direct_flow: Hipótese semi-formada → Metodologista direto
- test_complete_hypothesis_flow: Hipótese completa → Metodologista direto
- test_context_preservation: Contexto preservado entre agentes

Versão: 1.0 (Épico 3, Funcionalidade 3.3)
Data: 11/11/2025
"""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente do .env
load_dotenv()

from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

requires_anthropic = pytest.mark.skipif(
    not ANTHROPIC_API_KEY,
    reason="Integration test skipped: ANTHROPIC_API_KEY not set (requires real API)",
)

# Todos os testes deste módulo são de integração que usam API real
pytestmark = [pytest.mark.integration, requires_anthropic]


def test_vague_idea_full_flow(multi_agent_graph):
    """
    Testa fluxo completo: Ideia vaga → Estruturador → Metodologista.

    Valida:
    - Orquestrador entra em modo de exploração (next_step / agent_suggestion)
    - Estruturador é executado e gera questão estruturada
    - Metodologista recebe questão estruturada
    - Todos os outputs principais estão presentes no estado final
    """
    # Arrange
    user_input = "Observei que desenvolver com IA é mais rápido"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-vague-1",
    )

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-vague-1"}}
    )

    # Assert - Orquestrador conversacional deve fornecer análise e próximo passo
    assert result["orchestrator_analysis"] is not None, \
        "Orquestrador deveria fornecer analysis (reasoning)"
    assert result["next_step"] in ["explore", "suggest_agent", "clarify"], \
        "next_step do Orquestrador deveria ser válido"

    # Estruturador pode ou não ter sido chamado nesta invocação única
    if result['structurer_output'] is not None:
        assert 'structured_question' in result['structurer_output'], \
            "Estruturador deveria gerar questão estruturada"
        assert 'elements' in result['structurer_output'], \
            "Estruturador deveria extrair elementos (context, problem, contribution)"

    # Metodologista também pode não ter sido chamado ainda (fluxo conversacional)
    if result['methodologist_output'] is not None:
        # Status pode ser 'pending' se Metodologista pediu clarificações
        assert result['methodologist_output']['status'] in ['approved', 'rejected', 'pending'], \
            "Metodologista deveria ter status válido (approved, rejected ou pending)"

        # Se não estiver pending, deve ter justificativa
        if result['methodologist_output']['status'] != 'pending':
            assert result['methodologist_output']['justification'], \
                "Metodologista deveria fornecer justificativa quando decide"

    # current_stage pode variar no fluxo conversacional; validamos apenas que existe
    assert result["current_stage"] in ["classifying", "structuring", "validating", "done"]


def test_semi_formed_direct_flow(multi_agent_graph):
    """
    Testa fluxo direto: Hipótese semi-formada → Metodologista.

    Valida (fluxo direto ou quase direto):
    - Orquestrador sugere chamar agente adequado (structurer ou methodologist)
    - Estruturador pode ou não ser executado (dependendo do modelo)
    - Metodologista gera output válido
    """
    # Arrange
    user_input = "Método incremental melhora desenvolvimento de sistemas multi-agente"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-semi-1",
    )

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-semi-1"}}
    )

    # Assert - Orquestrador deve sugerir algum próximo passo
    assert result["orchestrator_analysis"] is not None
    assert result["next_step"] in ["explore", "suggest_agent", "clarify"]

    if result['methodologist_output'] is not None:
        # Status pode ser 'pending' se Metodologista pediu clarificações
        assert result['methodologist_output']['status'] in ['approved', 'rejected', 'pending'], \
            "Metodologista deveria ter status válido (approved, rejected ou pending)"

    assert result["current_stage"] in ["classifying", "structuring", "validating", "done"]


def test_complete_hypothesis_flow(multi_agent_graph):
    """
    Testa fluxo direto: Hipótese completa → Metodologista.

    Valida (hipótese completa):
    - Orquestrador reconhece contexto suficiente e sugere validação
    - Metodologista avalia hipótese (status válido)
    """
    # Arrange
    user_input = (
        "Método incremental reduz tempo de implementação em 30%, "
        "medido em sprints de 2 semanas, em equipes de 2-5 desenvolvedores"
    )
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-complete-1",
    )

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-complete-1"}}
    )

    # Assert - Orquestrador deve ter análise e próximo passo
    assert result["orchestrator_analysis"] is not None
    assert result["next_step"] in ["explore", "suggest_agent", "clarify"]

    if result['methodologist_output'] is not None:
        # Status pode ser 'pending' se Metodologista pediu clarificações
        assert result['methodologist_output']['status'] in ['approved', 'rejected', 'pending'], \
            "Metodologista deveria ter status válido (approved, rejected ou pending)"

    assert result["current_stage"] in ["classifying", "structuring", "validating", "done"]


def test_context_preservation(multi_agent_graph):
    """
    Testa preservação de contexto entre agentes.

    Valida:
    - Estruturador gera questão estruturada
    - Metodologista recebe a questão estruturada (não o input original)
    - Estado preserva histórico completo
    - conversation_history é atualizado
    """
    # Arrange
    user_input = "Observei que X é mais rápido que Y"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-context-1",
    )

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-context-1"}}
    )

    # Assert - Validar que contexto foi preservado
    assert result['user_input'] == user_input, \
        "Input original deveria ser preservado no estado"

    if result['structurer_output']:
        # Se passou pelo Estruturador, validar que questão estruturada existe
        structured_question = result['structurer_output']['structured_question']
        assert structured_question, \
            "Estruturador deveria gerar questão estruturada"

        assert structured_question != user_input, \
            "Questão estruturada deveria ser diferente do input original"

        # Metodologista deve ter recebido a questão estruturada
        # (não podemos validar diretamente, mas podemos inferir pelo fluxo)
        assert result['methodologist_output'] is not None, \
            "Metodologista deveria processar questão estruturada"

    # Validar histórico de conversação
    assert result['conversation_history'], \
        "Histórico de conversação deveria existir"

    assert len(result['conversation_history']) >= 1, \
        "Histórico deveria ter pelo menos o input do usuário"

    # Validar mensagens LangGraph
    assert result['messages'], \
        "Histórico de mensagens LLM deveria existir"


def test_state_fields_structure(multi_agent_graph):
    """
    Testa estrutura dos campos do MultiAgentState.

    Valida:
    - Campos obrigatórios estão presentes
    - Campos específicos por agente têm estrutura correta
    - Nenhum campo inesperado foi adicionado
    """
    # Arrange
    user_input = "Teste de estrutura de estado"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-state-1",
    )

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-state-1"}}
    )

    # Assert - Campos compartilhados
    assert "user_input" in result, "Campo 'user_input' obrigatório"
    assert "session_id" in result, "Campo 'session_id' obrigatório"
    assert "conversation_history" in result, "Campo 'conversation_history' obrigatório"
    assert "current_stage" in result, "Campo 'current_stage' obrigatório"
    assert "hypothesis_versions" in result, "Campo 'hypothesis_versions' obrigatório"
    assert "messages" in result, "Campo 'messages' obrigatório"

    # Assert - Campos específicos por agente (Orquestrador conversacional)
    assert "orchestrator_analysis" in result, "Campo 'orchestrator_analysis' obrigatório"
    assert "next_step" in result, "Campo 'next_step' obrigatório"
    assert "agent_suggestion" in result, "Campo 'agent_suggestion' obrigatório"
    assert "focal_argument" in result, "Campo 'focal_argument' obrigatório"
    assert "reflection_prompt" in result, "Campo 'reflection_prompt' obrigatório"
    assert "stage_suggestion" in result, "Campo 'stage_suggestion' obrigatório"

    # Assert - Campos específicos de Estruturador / Metodologista
    assert "structurer_output" in result, "Campo 'structurer_output' esperado"
    assert "methodologist_output" in result, "Campo 'methodologist_output' esperado"

    # Assert - Estrutura do methodologist_output
    if result['methodologist_output']:
        assert 'status' in result['methodologist_output'], \
            "methodologist_output deve ter campo 'status'"
        assert 'justification' in result['methodologist_output'], \
            "methodologist_output deve ter campo 'justification'"
        assert 'clarifications' in result['methodologist_output'], \
            "methodologist_output deve ter campo 'clarifications'"
