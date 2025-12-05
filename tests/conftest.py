"""
Shared test configuration and reusable fixtures.

Carrega o .env da raiz uma vez por sessão de testes e expõe fixtures comuns.
"""

from pathlib import Path

import pytest
from dotenv import load_dotenv


# Carregar variáveis de ambiente do .env na raiz do projeto (se existir)
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


from agents.multi_agent_graph import create_multi_agent_graph
from utils.test_executor import MultiTurnExecutor


@pytest.fixture
def multi_agent_graph():
    """Fixture que cria o super-grafo multi-agente para testes."""
    return create_multi_agent_graph()


@pytest.fixture
def multi_turn_executor(multi_agent_graph):
    """Fixture que cria executor multi-turn para testes."""
    return MultiTurnExecutor(multi_agent_graph)


