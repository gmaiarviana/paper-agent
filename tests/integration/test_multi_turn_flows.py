"""
Testes de integração para fluxos multi-turn (Épico 8.1).

Estes testes usam API real e validam cenários completos end-to-end
que não foram completamente testados no Épico 7.
"""

import pytest

from agents.multi_agent_graph import create_multi_agent_graph
from utils.test_executor import MultiTurnExecutor
from utils.test_scenarios import ConversationScenario


@pytest.fixture
def multi_turn_executor(multi_agent_graph):
    """Fixture para executor multi-turn."""
    return MultiTurnExecutor(multi_agent_graph)


@pytest.mark.integration
def test_cenario_3_refinement_flow(multi_turn_executor):
    """
    Valida fluxo completo do Cenário 3 (refinamento).
    
    Fluxo esperado:
    - User: ideia vaga
    - Orchestrator: explora
    - User: fornece contexto
    - Orchestrator → Structurer: estrutura V1
    - Orchestrator → Methodologist: valida
    - Methodologist: needs_refinement
    """
    scenario = ConversationScenario.from_epic7_scenario(3)
    result = multi_turn_executor.execute_scenario(scenario)
    
    # Validações estruturais
    assert result["success"], f"Cenário não executou conforme esperado: {result['validation_errors']}"
    assert "structurer" in result["agents_called"], "Estruturador não foi chamado"
    assert "methodologist" in result["agents_called"], "Metodologista não foi chamado"
    
    # Validar estado final
    final_state = result["final_state"]
    assert final_state.get("methodologist_output", {}).get("status") == "needs_refinement", \
        f"Status esperado: needs_refinement, obtido: {final_state.get('methodologist_output', {}).get('status')}"


@pytest.mark.integration
def test_cenario_6_reasoning_loop(multi_turn_executor):
    """
    Valida fluxo completo do Cenário 6 (reasoning loop).
    
    Fluxo esperado:
    - User: hipótese vaga
    - Orchestrator: explora
    - User: fornece contexto
    - Orchestrator → Methodologist: valida
    - Methodologist: entra em loop (pede clarificação)
    - User: responde
    - Methodologist: decide
    """
    scenario = ConversationScenario.from_epic7_scenario(6)
    result = multi_turn_executor.execute_scenario(scenario)
    
    # Validações estruturais
    assert result["success"], f"Cenário não executou conforme esperado: {result['validation_errors']}"
    assert "methodologist" in result["agents_called"], "Metodologista não foi chamado"
    
    # Validar que loop funcionou (múltiplas chamadas ao Methodologist)
    # EventBus deve ter > 1 evento agent_started para methodologist
    # (não validamos aqui pois _get_agents_from_events não diferencia múltiplas chamadas)


@pytest.mark.integration
def test_cenario_7_context_preservation(multi_turn_executor):
    """
    Valida fluxo completo do Cenário 7 (preservação de contexto).
    
    Fluxo esperado:
    - 5 turnos de conversa
    - focal_argument evolui a cada turno
    - Contexto não se perde
    """
    scenario = ConversationScenario.from_epic7_scenario(7)
    result = multi_turn_executor.execute_scenario(scenario)
    
    # Validações estruturais
    assert result["success"], f"Cenário não executou conforme esperado: {result['validation_errors']}"
    
    # Validar número de turnos
    assert len(result["turns"]) == 5, f"Esperado 5 turnos, obtido {len(result['turns'])}"
    
    # Validar que focal_argument evoluiu
    final_state = result["final_state"]
    focal_arg = final_state.get("focal_argument", {})
    
    assert focal_arg.get("subject") == "LLMs impact on sprint time and code quality", \
        f"Subject não evoluiu corretamente: {focal_arg.get('subject')}"
    assert focal_arg.get("population") == "teams of 2-5 developers", \
        f"Population não evoluiu corretamente: {focal_arg.get('population')}"
    assert "sprint time" in focal_arg.get("metrics", ""), \
        f"Métrica 'sprint time' não está presente: {focal_arg.get('metrics')}"

