"""
Smoke tests para o agente Estruturador.

Valida comportamento básico do Estruturador com API real:
- structurer_node: Organiza ideias vagas em questões estruturadas

IMPORTANTE: Estes testes fazem chamadas REAIS à API da Anthropic.
Certifique-se de ter configurado ANTHROPIC_API_KEY no arquivo .env
"""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente
load_dotenv()

from agents.orchestrator.state import create_initial_multi_agent_state
from agents.structurer.nodes import structurer_node

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

requires_anthropic = pytest.mark.skipif(
    not ANTHROPIC_API_KEY,
    reason="Smoke test skipped: ANTHROPIC_API_KEY not set (requires real API)",
)

# Todos os testes deste módulo são smoke tests de integração que usam API real
pytestmark = [pytest.mark.smoke, pytest.mark.integration, requires_anthropic]


@pytest.mark.smoke
@requires_anthropic
def test_vague_observation_tech():
    """Testa estruturação de observação vaga sobre tecnologia."""

    user_input = "Observei que desenvolver com Claude Code é mais rápido que métodos tradicionais"

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    # Validações
    output = result['structurer_output']
    assert 'structured_question' in output, "Falta structured_question"
    assert 'elements' in output, "Falta elements"
    assert 'context' in output['elements'], "Falta context"
    assert 'problem' in output['elements'], "Falta problem"
    assert 'contribution' in output['elements'], "Falta contribution"
    assert result['current_stage'] == "validating", "current_stage deveria ser 'validating'"
    assert len(result['messages']) == 1, "Deveria ter 1 mensagem"


@pytest.mark.smoke
@requires_anthropic
def test_vague_observation_education():
    """Testa estruturação de observação vaga sobre educação."""

    user_input = "Notei que alunos se engajam mais em aulas com elementos interativos"

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    # Validações
    output = result['structurer_output']
    assert len(output['structured_question']) > 10, "Questão muito curta"
    assert output['structured_question'] != user_input, "Questão igual ao input"
    assert result['current_stage'] == "validating", "Estágio incorreto"


@pytest.mark.smoke
@requires_anthropic
def test_very_vague_observation():
    """Testa estruturação de observação muito vaga."""

    user_input = "Algumas coisas funcionam melhor do que outras em certos contextos"

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    # Validações - Deve estruturar mesmo input muito vago (comportamento colaborativo)
    output = result['structurer_output']
    assert output['structured_question'] is not None, "Falta questão estruturada"
    assert len(output['structured_question']) > 0, "Questão vazia"

    # Não deve ter linguagem de rejeição
    message_content = result['messages'][0].content.lower()
    assert "rejeita" not in message_content, "Estruturador não deve rejeitar"
    assert "inválid" not in message_content, "Estruturador não deve invalidar"


@pytest.mark.smoke
@requires_anthropic
def test_output_structure():
    """Testa estrutura consistente do output."""

    user_input = "Percebo que equipes pequenas entregam mais rápido"

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    # Validar estrutura completa
    assert 'structurer_output' in result, "Falta structurer_output no result"
    assert 'current_stage' in result, "Falta current_stage no result"
    assert 'messages' in result, "Falta messages no result"

    output = result['structurer_output']
    assert isinstance(output, dict), "structurer_output deve ser dict"
    assert isinstance(output['elements'], dict), "elements deve ser dict"
    assert isinstance(output['structured_question'], str), "structured_question deve ser str"
    assert isinstance(output['elements']['context'], str), "context deve ser str"
    assert isinstance(output['elements']['problem'], str), "problem deve ser str"
    assert isinstance(output['elements']['contribution'], str), "contribution deve ser str"
