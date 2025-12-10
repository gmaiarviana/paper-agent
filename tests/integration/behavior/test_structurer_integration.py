"""
Testes de integração para o agente Estruturador com API real.

Valida comportamento real de estruturação de ideias vagas em questões de pesquisa,
sem mocks, usando API real do Claude (Haiku).

Testes:
- test_structurer_structures_vague_observation_real_api: Observação vaga → questão estruturada
- test_structurer_extracts_all_elements_real_api: Extrai todos os elementos (context, problem, contribution)
- test_structurer_generates_meaningful_question_real_api: Questão estruturada faz sentido
- test_structurer_is_collaborative_real_api: Não rejeita ideias vagas, tenta estruturar

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

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.structurer.nodes import structurer_node
from langchain_core.messages import AIMessage

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

requires_anthropic = pytest.mark.skipif(
    not ANTHROPIC_API_KEY,
    reason="Integration test skipped: ANTHROPIC_API_KEY not set (requires real API)",
)

# Todos os testes deste módulo são de integração que usam API real
pytestmark = [pytest.mark.integration, requires_anthropic]

def test_structurer_structures_vague_observation_real_api():
    """
    Testa estruturação real de observação vaga com API real.
    
    Valida:
    - structurer_output não é None
    - structured_question não está vazia e é diferente do input original
    - elements contém context, problem, contribution
    - current_stage atualizado para "validating"
    - Mensagem adicionada ao histórico
    """
    # Arrange
    user_input = "Observei que desenvolver com Claude Code é mais rápido"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-structurer-vague-1",
    )
    
    # Act
    result = structurer_node(state)
    
    # Assert - Validar comportamento real (não apenas estrutura)
    assert "structurer_output" in result, \
        "Estruturador deveria gerar structurer_output"
    
    output = result["structurer_output"]
    assert output is not None, \
        "structurer_output não deveria ser None"
    
    # Validar structured_question
    assert "structured_question" in output, \
        "Output deveria conter 'structured_question'"
    
    structured_question = output["structured_question"]
    assert structured_question is not None, \
        "structured_question não deveria ser None"
    
    assert len(structured_question) > 10, \
        "Questão estruturada deveria ter conteúdo substancial"
    
    # Questão deve ser diferente do input original
    assert structured_question != user_input, \
        "Questão estruturada deveria ser diferente do input original"
    
    # Validar elements
    assert "elements" in output, \
        "Output deveria conter 'elements'"
    
    elements = output["elements"]
    assert "context" in elements, \
        "Elements deveria conter 'context'"
    
    assert "problem" in elements, \
        "Elements deveria conter 'problem'"
    
    assert "contribution" in elements, \
        "Elements deveria conter 'contribution'"
    
    # Validar que elementos têm conteúdo
    assert elements["context"] is not None and len(str(elements["context"])) > 0, \
        "Context deveria ter conteúdo"
    
    assert elements["problem"] is not None and len(str(elements["problem"])) > 0, \
        "Problem deveria ter conteúdo"
    
    assert elements["contribution"] is not None and len(str(elements["contribution"])) > 0, \
        "Contribution deveria ter conteúdo"
    
    # Validar transição de estado
    assert result["current_stage"] == "validating", \
        f"current_stage deveria ser 'validating', mas foi '{result['current_stage']}'"
    
    # Validar que mensagem foi adicionada
    assert len(result["messages"]) == 1, \
        "Deveria ter 1 mensagem (AIMessage do estruturador)"
    
    assert isinstance(result["messages"][0], AIMessage), \
        "Mensagem deveria ser AIMessage"
    
    # Mensagem deve conter informações estruturadas
    message_content = result["messages"][0].content
    assert len(message_content) > 20, \
        "Mensagem deveria ter conteúdo substancial"

def test_structurer_extracts_all_elements_real_api():
    """
    Testa que estruturador extrai todos os elementos corretamente com API real.
    
    Valida:
    - Todos os elementos (context, problem, contribution) são extraídos
    - Elementos têm conteúdo relevante e não são placeholders
    - Elementos são diferentes entre si (não são cópias)
    """
    # Arrange
    user_input = "Notei que alunos se engajam mais em aulas interativas"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-structurer-elements-1",
    )
    
    # Act
    result = structurer_node(state)
    
    # Assert - Validar comportamento real
    output = result["structurer_output"]
    elements = output["elements"]
    
    # Validar que todos os elementos existem e têm conteúdo
    context = str(elements["context"])
    problem = str(elements["problem"])
    contribution = str(elements["contribution"])
    
    assert len(context) > 5, \
        "Context deveria ter conteúdo substancial"
    
    assert len(problem) > 5, \
        "Problem deveria ter conteúdo substancial"
    
    assert len(contribution) > 5, \
        "Contribution deveria ter conteúdo substancial"
    
    # Elementos devem ser diferentes entre si (não são cópias)
    assert context != problem, \
        "Context e Problem deveriam ser diferentes"
    
    assert context != contribution, \
        "Context e Contribution deveriam ser diferentes"
    
    assert problem != contribution, \
        "Problem e Contribution deveriam ser diferentes"
    
    # Validar que structured_question faz referência aos elementos
    structured_question = output["structured_question"].lower()
    # Não validar palavras exatas, mas validar que questão existe e tem conteúdo
    assert len(structured_question) > 10, \
        "Questão estruturada deveria ter conteúdo substancial"

def test_structurer_generates_meaningful_question_real_api():
    """
    Testa que estruturador gera questão estruturada que faz sentido com API real.
    
    Valida:
    - Questão estruturada tem formato apropriado (termina com ? ou contém ?)
    - Questão é relevante ao input original
    - Questão tem comprimento razoável
    """
    # Arrange
    user_input = "Método X funciona melhor"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-structurer-meaningful-1",
    )
    
    # Act
    result = structurer_node(state)
    
    # Assert - Validar comportamento real
    output = result["structurer_output"]
    structured_question = output["structured_question"]
    
    # Questão deve ter comprimento razoável
    assert len(structured_question) > 10, \
        "Questão estruturada deveria ter comprimento razoável"
    
    # Questão deve parecer uma questão (contém ?)
    assert "?" in structured_question, \
        "Questão estruturada deveria conter '?'"
    
    # Questão deve ser diferente do input original
    assert structured_question != user_input, \
        "Questão estruturada deveria ser diferente do input original"
    
    # Questão deve ter conteúdo relevante (não apenas placeholder)
    # Não validar palavras exatas, mas validar que questão existe e tem conteúdo
    assert len(structured_question.split()) > 3, \
        "Questão estruturada deveria ter múltiplas palavras"

def test_structurer_is_collaborative_real_api():
    """
    Testa que estruturador é colaborativo e não rejeita ideias vagas com API real.
    
    Valida:
    - Estruturador tenta estruturar mesmo input muito vago
    - Não rejeita ideias (não contém palavras como "rejeitado", "inválido")
    - Gera questão estruturada mesmo para input vago
    """
    # Arrange - Input muito vago
    user_input = "Coisas são interessantes"
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id="test-structurer-collaborative-1",
    )
    
    # Act
    result = structurer_node(state)
    
    # Assert - Validar comportamento real
    output = result["structurer_output"]
    
    # Deve ter estruturado, não rejeitado
    assert output["structured_question"] is not None, \
        "Estruturador deveria gerar questão estruturada mesmo para input vago"
    
    assert len(output["structured_question"]) > 0, \
        "Questão estruturada não deveria estar vazia"
    
    # Mensagem não deve conter palavras de rejeição
    message_content = result["messages"][0].content.lower()
    
    # Validar que mensagem não contém palavras de rejeição
    rejection_words = ["rejeita", "inválid", "não é possível", "impossível", "não posso"]
    for word in rejection_words:
        assert word not in message_content, \
            f"Mensagem não deveria conter palavra de rejeição: '{word}'"
    
    # Validar que elementos foram extraídos (mesmo que vagos)
    elements = output["elements"]
    assert elements["context"] is not None, \
        "Context deveria ser extraído mesmo para input vago"
    
    assert elements["problem"] is not None, \
        "Problem deveria ser extraído mesmo para input vago"
    
    assert elements["contribution"] is not None, \
        "Contribution deveria ser extraído mesmo para input vago"
    
    # Validar que current_stage foi atualizado
    assert result["current_stage"] == "validating", \
        "current_stage deveria ser 'validating' após estruturação"

