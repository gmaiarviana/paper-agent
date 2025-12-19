"""
Testes unitários para a tool ask_user do agente Metodologista.

"""

import pytest
import sys
from unittest.mock import patch, MagicMock

# Mock langgraph antes de importar módulos que dependem dele
# Criar estrutura completa de mocks para evitar problemas de __path__
_mock_langgraph = MagicMock()
_mock_checkpoint = MagicMock()
_mock_memory = MagicMock()
_mock_memory.MemorySaver = MagicMock()

sys.modules['langgraph'] = _mock_langgraph
sys.modules['langgraph.checkpoint'] = _mock_checkpoint
sys.modules['langgraph.checkpoint.memory'] = _mock_memory

# Configurar __path__ nos mocks para evitar AttributeError
_mock_langgraph.__path__ = []
_mock_checkpoint.__path__ = []
_mock_memory.__path__ = []

from core.agents.methodologist.tools import ask_user

class TestAskUserTool:
    """Suite de testes para a tool ask_user."""

    def test_ask_user_has_correct_name(self):
        """Verifica que a tool tem o nome correto."""
        assert ask_user.name == "ask_user"

    def test_ask_user_has_description(self):
        """Verifica que a tool tem uma descrição."""
        assert ask_user.description is not None
        assert len(ask_user.description) > 0

    def test_ask_user_type_hints(self):
        """Verifica que a função tem type hints corretos."""
        annotations = ask_user.func.__annotations__
        assert annotations['question'] == str
        assert annotations['return'] == str

    @patch('core.agents.methodologist.tools.interrupt')
    @patch('core.agents.methodologist.tools.logger')
    def test_ask_user_calls_interrupt(self, mock_logger, mock_interrupt):
        """Verifica que ask_user chama interrupt() com a pergunta."""
        mock_interrupt.return_value = "Resposta mockada"
        question = "Qual é a população-alvo?"

        result = ask_user.invoke({"question": question})

        mock_interrupt.assert_called_once_with(question)
        assert result == "Resposta mockada"

    @patch('core.agents.methodologist.tools.interrupt')
    @patch('core.agents.methodologist.tools.logger')
    def test_ask_user_logs_question(self, mock_logger, mock_interrupt):
        """Verifica que ask_user loga a pergunta enviada."""
        mock_interrupt.return_value = "Resposta mockada"
        question = "Qual é a métrica de avaliação?"

        ask_user.invoke({"question": question})

        # Verifica que logger.info foi chamado com a pergunta
        assert mock_logger.info.call_count == 2
        first_call_args = mock_logger.info.call_args_list[0][0][0]
        assert question in first_call_args
        assert "Pergunta enviada" in first_call_args

    @patch('core.agents.methodologist.tools.interrupt')
    @patch('core.agents.methodologist.tools.logger')
    def test_ask_user_logs_response(self, mock_logger, mock_interrupt):
        """Verifica que ask_user loga a resposta recebida."""
        response = "Adultos de 18-40 anos"
        mock_interrupt.return_value = response

        ask_user.invoke({"question": "Qual a população?"})

        # Verifica que logger.info foi chamado com a resposta
        assert mock_logger.info.call_count == 2
        second_call_args = mock_logger.info.call_args_list[1][0][0]
        assert response in second_call_args
        assert "Resposta recebida" in second_call_args

    @patch('core.agents.methodologist.tools.interrupt')
    @patch('core.agents.methodologist.tools.logger')
    def test_ask_user_returns_user_response(self, mock_logger, mock_interrupt):
        """Verifica que ask_user retorna a resposta do usuário."""
        expected_response = "Tempo de reação em milissegundos"
        mock_interrupt.return_value = expected_response

        result = ask_user.invoke({"question": "Qual a métrica?"})

        assert result == expected_response

    @patch('core.agents.methodologist.tools.interrupt')
    @patch('core.agents.methodologist.tools.logger')
    def test_ask_user_with_empty_question(self, mock_logger, mock_interrupt):
        """Verifica comportamento com pergunta vazia."""
        mock_interrupt.return_value = "Resposta"

        result = ask_user.invoke({"question": ""})

        mock_interrupt.assert_called_once_with("")
        assert result == "Resposta"

    @patch('core.agents.methodologist.tools.interrupt')
    @patch('core.agents.methodologist.tools.logger')
    def test_ask_user_with_long_question(self, mock_logger, mock_interrupt):
        """Verifica comportamento com pergunta longa."""
        long_question = "Poderia especificar " * 50  # Pergunta muito longa
        mock_interrupt.return_value = "Resposta detalhada"

        result = ask_user.invoke({"question": long_question})

        mock_interrupt.assert_called_once_with(long_question)
        assert result == "Resposta detalhada"

    def test_ask_user_docstring_exists(self):
        """Verifica que a função tem docstring detalhada."""
        assert ask_user.func.__doc__ is not None
        docstring = ask_user.func.__doc__

        # Verifica elementos essenciais na docstring
        assert "pergunta" in docstring.lower()
        assert "usuário" in docstring.lower()
        assert "interrupt" in docstring.lower()
        assert "Args:" in docstring
        assert "Returns:" in docstring
        assert "Example:" in docstring
