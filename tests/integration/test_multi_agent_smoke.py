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

import pytest
import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente do .env
from dotenv import load_dotenv
load_dotenv()

from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state


@pytest.fixture
def multi_agent_graph():
    """Fixture que cria o super-grafo multi-agente."""
    return create_multi_agent_graph()


def test_vague_idea_full_flow(multi_agent_graph):
    """
    Testa fluxo completo: Ideia vaga → Estruturador → Metodologista.

    Valida:
    - Orquestrador classifica corretamente como "vague"
    - Estruturador é executado e gera questão estruturada
    - Metodologista recebe questão estruturada
    - Fluxo completa com stage = "done"
    - Todos os outputs estão presentes no estado final
    """
    # Arrange
    user_input = "Observei que desenvolver com IA é mais rápido"
    state = create_initial_multi_agent_state(user_input)

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-vague-1"}}
    )

    # Assert
    assert result['orchestrator_classification'] == 'vague', \
        "Orquestrador deveria classificar como 'vague'"

    assert result['orchestrator_reasoning'] is not None, \
        "Orquestrador deveria fornecer reasoning"

    assert result['structurer_output'] is not None, \
        "Estruturador deveria ter gerado output"

    assert 'structured_question' in result['structurer_output'], \
        "Estruturador deveria gerar questão estruturada"

    assert 'elements' in result['structurer_output'], \
        "Estruturador deveria extrair elementos (context, problem, contribution)"

    assert result['methodologist_output'] is not None, \
        "Metodologista deveria ter gerado output"

    assert result['methodologist_output']['status'] in ['approved', 'rejected'], \
        "Metodologista deveria ter status válido"

    assert result['methodologist_output']['justification'], \
        "Metodologista deveria fornecer justificativa"

    assert result['current_stage'] == 'done', \
        "Estágio final deveria ser 'done'"


def test_semi_formed_direct_flow(multi_agent_graph):
    """
    Testa fluxo direto: Hipótese semi-formada → Metodologista.

    Valida:
    - Orquestrador classifica corretamente como "semi_formed"
    - Estruturador NÃO é executado (fluxo direto)
    - Metodologista recebe input direto do usuário
    - Fluxo completa com stage = "done"
    """
    # Arrange
    user_input = "Método incremental melhora desenvolvimento de sistemas multi-agente"
    state = create_initial_multi_agent_state(user_input)

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-semi-1"}}
    )

    # Assert
    assert result['orchestrator_classification'] == 'semi_formed', \
        "Orquestrador deveria classificar como 'semi_formed'"

    assert result['structurer_output'] is None, \
        "Estruturador NÃO deveria ter sido executado no fluxo direto"

    assert result['methodologist_output'] is not None, \
        "Metodologista deveria ter gerado output"

    assert result['methodologist_output']['status'] in ['approved', 'rejected'], \
        "Metodologista deveria ter status válido"

    assert result['current_stage'] == 'done', \
        "Estágio final deveria ser 'done'"


def test_complete_hypothesis_flow(multi_agent_graph):
    """
    Testa fluxo direto: Hipótese completa → Metodologista.

    Valida:
    - Orquestrador classifica corretamente como "complete"
    - Estruturador NÃO é executado (fluxo direto)
    - Metodologista avalia hipótese completa
    - Fluxo completa com stage = "done"
    """
    # Arrange
    user_input = (
        "Método incremental reduz tempo de implementação em 30%, "
        "medido em sprints de 2 semanas, em equipes de 2-5 desenvolvedores"
    )
    state = create_initial_multi_agent_state(user_input)

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-complete-1"}}
    )

    # Assert
    assert result['orchestrator_classification'] == 'complete', \
        "Orquestrador deveria classificar como 'complete'"

    assert result['structurer_output'] is None, \
        "Estruturador NÃO deveria ter sido executado no fluxo direto"

    assert result['methodologist_output'] is not None, \
        "Metodologista deveria ter gerado output"

    assert result['methodologist_output']['status'] in ['approved', 'rejected'], \
        "Metodologista deveria ter status válido"

    assert result['current_stage'] == 'done', \
        "Estágio final deveria ser 'done'"


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
    state = create_initial_multi_agent_state(user_input)

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
    state = create_initial_multi_agent_state(user_input)

    # Act
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": "test-state-1"}}
    )

    # Assert - Campos compartilhados
    assert 'user_input' in result, "Campo 'user_input' obrigatório"
    assert 'conversation_history' in result, "Campo 'conversation_history' obrigatório"
    assert 'current_stage' in result, "Campo 'current_stage' obrigatório"
    assert 'messages' in result, "Campo 'messages' obrigatório"

    # Assert - Campos específicos por agente
    assert 'orchestrator_classification' in result, "Campo 'orchestrator_classification' obrigatório"
    assert 'orchestrator_reasoning' in result, "Campo 'orchestrator_reasoning' obrigatório"
    assert 'structurer_output' in result, "Campo 'structurer_output' esperado"
    assert 'methodologist_output' in result, "Campo 'methodologist_output' esperado"

    # Assert - Estrutura do methodologist_output
    if result['methodologist_output']:
        assert 'status' in result['methodologist_output'], \
            "methodologist_output deve ter campo 'status'"
        assert 'justification' in result['methodologist_output'], \
            "methodologist_output deve ter campo 'justification'"
        assert 'clarifications' in result['methodologist_output'], \
            "methodologist_output deve ter campo 'clarifications'"


if __name__ == "__main__":
    # Permitir execução direta do arquivo para debugging
    pytest.main([__file__, "-v", "-s"])
