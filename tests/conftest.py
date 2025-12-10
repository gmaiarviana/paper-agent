"""
Shared test configuration and reusable fixtures.

Carrega o .env da raiz uma vez por sessão de testes e expõe fixtures comuns.

Nota: Fixtures do multi-agent graph (multi_agent_graph, multi_turn_executor)
só estão disponíveis quando langgraph está instalado.
"""

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env na raiz do projeto (se existir)
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

@pytest.fixture(autouse=True)
def reset_anthropic_circuit_breaker():
    """
    Reset circuit breaker antes de cada teste.

    O circuit breaker é um singleton global que persiste entre testes.
    Sem esse reset, um teste que falha pode abrir o circuit breaker
    e causar falhas em cascata em todos os testes subsequentes.
    """
    from core.utils.providers.anthropic import _circuit_breaker
    _circuit_breaker._consecutive_failures = 0
    _circuit_breaker._is_open = False
    yield
    # Reset também após o teste (cleanup)
    _circuit_breaker._consecutive_failures = 0
    _circuit_breaker._is_open = False

# Import condicional: multi-agent graph requer langgraph
# Se langgraph não estiver instalado, fixtures não estarão disponíveis
# mas testes unitários (Observer, etc) continuam funcionando
try:
    from agents.multi_agent_graph import create_multi_agent_graph
    from core.utils.test_executor import MultiTurnExecutor
    MULTI_AGENT_AVAILABLE = True
except ImportError as e:
    MULTI_AGENT_AVAILABLE = False
    import logging
    logging.debug(f"Multi-agent fixtures não disponíveis: {e}")

@pytest.fixture
def multi_agent_graph():
    """Fixture que cria o super-grafo multi-agente para testes."""
    if not MULTI_AGENT_AVAILABLE:
        pytest.skip("langgraph não instalado - fixture multi_agent_graph indisponível")
    return create_multi_agent_graph()

@pytest.fixture
def multi_turn_executor(multi_agent_graph):
    """Fixture que cria executor multi-turn para testes."""
    if not MULTI_AGENT_AVAILABLE:
        pytest.skip("langgraph não instalado - fixture multi_turn_executor indisponível")
    return MultiTurnExecutor(multi_agent_graph)

