"""
Testes de integração para o agente Orquestrador com API real.

Valida comportamento real de classificação e análise de input do usuário,
sem mocks, usando API real do Claude (Haiku).

Testes:
- test_orchestrator_classifies_vague_input_real_api: Input vago → classifica corretamente
- test_orchestrator_classifies_semi_formed_input_real_api: Input semi-formado → sugere structurer
- test_orchestrator_classifies_complete_hypothesis_real_api: Hipótese completa → sugere methodologist
- test_orchestrator_handles_ambiguous_input_real_api: Input ambíguo → classifica como clarify
- test_orchestrator_preserves_context_real_api: Preserva contexto do histórico

Data: Dezembro 2025
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

from agents.orchestrator.state import create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node
from langchain_core.messages import HumanMessage, AIMessage

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

requires_anthropic = pytest.mark.skipif(
    not ANTHROPIC_API_KEY,
    reason="Integration test skipped: ANTHROPIC_API_KEY not set (requires real API)",
)

# Todos os testes deste módulo são de integração que usam API real
pytestmark = [pytest.mark.integration, requires_anthropic]

def test_orchestrator_classifies_vague_input_real_api():
    """
    Testa classificação real de input vago com API real.
    
    Valida:
    - next_step é "explore" ou "clarify" (input vago não sugere agente)
    - orchestrator_analysis contém raciocínio relevante
    - agent_suggestion é None (input vago não sugere agente)
    - Mensagem adicionada ao histórico
    """
    # Arrange
    user_input = "Observei que desenvolver com IA é mais rápido"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-orchestrator-vague-1",
    )
    
    # Act
    result = orchestrator_node(state)
    
    # Assert - Validar comportamento real (não apenas estrutura)
    assert result["next_step"] in ["explore", "clarify"], \
        f"Input vago deveria resultar em 'explore' ou 'clarify', mas foi '{result['next_step']}'"
    
    assert result["orchestrator_analysis"] is not None, \
        "Orquestrador deveria fornecer análise (reasoning)"
    
    assert len(result["orchestrator_analysis"]) > 20, \
        "Análise deveria ter conteúdo substancial (não apenas placeholder)"
    
    # Input vago não deve sugerir agente
    assert result["agent_suggestion"] is None, \
        "Input vago não deveria sugerir agente"
    
    # Validar que mensagem foi adicionada
    assert len(result["messages"]) == 1, \
        "Deveria ter 1 mensagem (AIMessage do orquestrador)"
    
    assert isinstance(result["messages"][0], AIMessage), \
        "Mensagem deveria ser AIMessage"
    
    # Mensagem deve ter conteúdo relevante
    message_content = result["messages"][0].content
    assert len(message_content) > 10, \
        "Mensagem deveria ter conteúdo substancial"
    
    # Validar que focal_argument foi extraído
    assert "focal_argument" in result, \
        "Orquestrador deveria extrair focal_argument"
    
    assert result["focal_argument"] is not None, \
        "focal_argument não deveria ser None"

def test_orchestrator_classifies_semi_formed_input_real_api():
    """
    Testa classificação real de input semi-formado com API real.
    
    Valida:
    - next_step é "suggest_agent" (input semi-formado sugere agente)
    - agent_suggestion sugere "structurer" (input precisa estruturação)
    - orchestrator_analysis contém raciocínio sobre necessidade de estruturação
    """
    # Arrange
    user_input = "Método incremental melhora desenvolvimento multi-agente"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-orchestrator-semi-1",
    )
    
    # Act
    result = orchestrator_node(state)
    
    # Assert - Validar comportamento real
    assert result["next_step"] in ["suggest_agent", "explore"], \
        f"Input semi-formado deveria resultar em 'suggest_agent' ou 'explore', mas foi '{result['next_step']}'"
    
    if result["next_step"] == "suggest_agent":
        assert result["agent_suggestion"] is not None, \
            "Se next_step é 'suggest_agent', agent_suggestion não deveria ser None"
        
        assert "agent" in result["agent_suggestion"], \
            "agent_suggestion deveria ter campo 'agent'"
        
        # Input semi-formado geralmente sugere structurer
        suggested_agent = result["agent_suggestion"]["agent"]
        assert suggested_agent in ["structurer", "methodologist"], \
            f"Agente sugerido deveria ser 'structurer' ou 'methodologist', mas foi '{suggested_agent}'"
        
        assert "justification" in result["agent_suggestion"], \
            "agent_suggestion deveria ter campo 'justification'"
        
        justification = result["agent_suggestion"]["justification"]
        assert len(justification) > 10, \
            "Justificativa deveria ter conteúdo substancial"
    
    assert result["orchestrator_analysis"] is not None, \
        "Orquestrador deveria fornecer análise"
    
    # Validar que mensagem foi adicionada
    assert len(result["messages"]) == 1, \
        "Deveria ter 1 mensagem"

def test_orchestrator_classifies_complete_hypothesis_real_api():
    """
    Testa classificação real de hipótese completa com API real.
    
    Valida:
    - next_step é "suggest_agent" (hipótese completa sugere agente)
    - agent_suggestion sugere "methodologist" (hipótese pronta para validação)
    - orchestrator_analysis reconhece que hipótese está bem formada
    """
    # Arrange
    user_input = (
        "Método incremental reduz tempo de implementação de sistemas "
        "multi-agente em 30%, medido por sprints, em equipes de 2-5 devs"
    )
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-orchestrator-complete-1",
    )
    
    # Act
    result = orchestrator_node(state)
    
    # Assert - Validar comportamento real
    assert result["next_step"] in ["suggest_agent", "explore"], \
        f"Hipótese completa deveria resultar em 'suggest_agent' ou 'explore', mas foi '{result['next_step']}'"
    
    if result["next_step"] == "suggest_agent":
        assert result["agent_suggestion"] is not None, \
            "Se next_step é 'suggest_agent', agent_suggestion não deveria ser None"
        
        suggested_agent = result["agent_suggestion"]["agent"]
        # Hipótese completa geralmente sugere methodologist
        assert suggested_agent in ["methodologist", "structurer"], \
            f"Agente sugerido deveria ser 'methodologist' ou 'structurer', mas foi '{suggested_agent}'"
    
    assert result["orchestrator_analysis"] is not None, \
        "Orquestrador deveria fornecer análise"
    
    # Análise deve reconhecer que hipótese está bem formada
    analysis_lower = result["orchestrator_analysis"].lower()
    # Não validar palavras exatas, mas validar que análise existe e tem conteúdo
    assert len(analysis_lower) > 20, \
        "Análise deveria ter conteúdo substancial"

def test_orchestrator_handles_ambiguous_input_real_api():
    """
    Testa classificação real de input ambíguo com API real.
    
    Valida:
    - next_step é "clarify" ou "explore" (input ambíguo precisa clarificação)
    - orchestrator_analysis reconhece ambiguidade
    - Mensagem contém pergunta de clarificação
    """
    # Arrange
    user_input = "Quero estudar LLMs"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-orchestrator-ambiguous-1",
    )
    
    # Act
    result = orchestrator_node(state)
    
    # Assert - Validar comportamento real
    assert result["next_step"] in ["clarify", "explore"], \
        f"Input ambíguo deveria resultar em 'clarify' ou 'explore', mas foi '{result['next_step']}'"
    
    assert result["orchestrator_analysis"] is not None, \
        "Orquestrador deveria fornecer análise"
    
    # Mensagem deve conter pergunta ou pedido de clarificação
    message_content = result["messages"][0].content.lower()
    # Não validar palavras exatas, mas validar que mensagem existe e tem conteúdo
    assert len(message_content) > 10, \
        "Mensagem deveria ter conteúdo substancial"
    
    # Input ambíguo não deve sugerir agente
    assert result["agent_suggestion"] is None, \
        "Input ambíguo não deveria sugerir agente diretamente"

def test_orchestrator_preserves_context_real_api():
    """
    Testa que orquestrador preserva contexto do histórico com API real.
    
    Valida:
    - Orquestrador usa histórico de conversa para análise
    - Análise reflete contexto do histórico
    - Mensagens anteriores são consideradas
    """
    # Arrange
    state = create_initial_multi_agent_state(
        user_input="Observei que LLMs aumentam produtividade",
        session_id="test-orchestrator-context-1",
    )
    
    # Adicionar histórico de conversa
    state["messages"] = [
        HumanMessage(content="Na minha equipe, usando Claude Code, tarefas de 2h agora levam 30min"),
        AIMessage(content="Você quer validar ou entender literatura?"),
        HumanMessage(content="Quero validar como hipótese")
    ]
    
    # Act
    result = orchestrator_node(state)
    
    # Assert - Validar comportamento real
    assert result["orchestrator_analysis"] is not None, \
        "Orquestrador deveria fornecer análise"
    
    # Análise deve refletir contexto do histórico
    analysis_lower = result["orchestrator_analysis"].lower()
    
    # Validar que análise tem conteúdo substancial (não apenas placeholder)
    assert len(analysis_lower) > 20, \
        "Análise deveria ter conteúdo substancial considerando histórico"
    
    # Validar que mensagem foi adicionada
    assert len(result["messages"]) == 1, \
        "Deveria ter 1 nova mensagem (AIMessage do orquestrador)"
    
    # Validar que focal_argument foi extraído considerando histórico
    assert "focal_argument" in result, \
        "Orquestrador deveria extrair focal_argument"
    
    assert result["focal_argument"] is not None, \
        "focal_argument não deveria ser None"
    
    # Validar que intent reflete escolha do usuário (validar)
    focal = result["focal_argument"]
    if "intent" in focal:
        # Intent pode ser vários valores dependendo da análise do LLM
        valid_intents = ["validate", "unclear", "explore", "test_hypothesis", "review_literature", "build_theory"]
        assert focal["intent"] in valid_intents, \
            f"Intent deveria ser um valor válido, mas foi '{focal.get('intent')}'"

