"""
Testes unitários para os nós do grafo do agente Metodologista.

Este módulo testa os 3 nós principais do fluxo de raciocínio:
- analyze: Avalia hipótese e decide se precisa de clarificações
- ask_clarification: Solicita informação ao usuário
- decide: Toma decisão final sobre a hipótese

Os testes usam mocks para isolar o comportamento dos nós sem fazer
chamadas reais à API da Anthropic.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.messages import AIMessage, HumanMessage

from agents.methodologist import (
    MethodologistState,
    create_initial_state
)
from agents.methodologist.nodes import (
    analyze,
    ask_clarification,
    decide
)


# ==============================================================================
# TESTES DO NÓ ANALYZE
# ==============================================================================

class TestAnalyzeNode:
    """Testes para o nó analyze."""

    def test_analyze_needs_clarification_when_info_insufficient(self):
        """Testa que analyze marca needs_clarification=True quando informação é insuficiente."""
        state = create_initial_state("Café aumenta produtividade")

        # Mock da resposta do LLM indicando informação insuficiente
        mock_response = AIMessage(content='{"has_sufficient_info": false, "reasoning": "Faltam detalhes", "missing_info": "população e métricas"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = analyze(state)

        assert result['needs_clarification'] is True
        assert 'messages' in result
        assert len(result['messages']) == 1

    def test_analyze_does_not_need_clarification_when_info_sufficient(self):
        """Testa que analyze marca needs_clarification=False quando informação é suficiente."""
        state = create_initial_state("O consumo de 200mg de cafeína melhora tempo de reação em 10% no teste PVT")

        # Mock da resposta do LLM indicando informação suficiente
        mock_response = AIMessage(content='{"has_sufficient_info": true, "reasoning": "Hipótese bem especificada"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = analyze(state)

        assert result['needs_clarification'] is False
        assert 'messages' in result

    def test_analyze_handles_json_parse_error(self):
        """Testa que analyze trata erro de parse do JSON assumindo que precisa de clarificação."""
        state = create_initial_state("Café aumenta produtividade")

        # Mock da resposta do LLM com JSON inválido
        mock_response = AIMessage(content='Resposta sem JSON válido')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = analyze(state)

        # Deve assumir que precisa de clarificação por segurança
        assert result['needs_clarification'] is True

    def test_analyze_considers_existing_clarifications(self):
        """Testa que analyze considera clarificações já obtidas no contexto."""
        state = create_initial_state("Café aumenta produtividade")
        state['clarifications'] = {"População?": "Adultos 18-40 anos"}

        mock_response = AIMessage(content='{"has_sufficient_info": false, "reasoning": "Ainda faltam métricas"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            # Capturar o prompt enviado ao LLM
            result = analyze(state)
            call_args = mock_llm.invoke.call_args

            # Verificar que o prompt inclui as clarificações
            prompt_content = call_args[0][0][0].content
            assert "Clarificações obtidas:" in prompt_content
            assert "Adultos 18-40 anos" in prompt_content

    def test_analyze_logs_decision(self, caplog):
        """Testa que analyze registra logs informativos."""
        state = create_initial_state("Café aumenta produtividade")
        mock_response = AIMessage(content='{"has_sufficient_info": false}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            with caplog.at_level('INFO'):
                analyze(state)

            # Verificar que logs foram registrados
            assert "NÓ ANALYZE: Iniciando análise" in caplog.text
            assert "NÓ ANALYZE: Finalizado" in caplog.text


# ==============================================================================
# TESTES DO NÓ ASK_CLARIFICATION
# ==============================================================================

class TestAskClarificationNode:
    """Testes para o nó ask_clarification."""

    def test_ask_clarification_calls_ask_user_and_updates_state(self):
        """Testa que ask_clarification chama ask_user e atualiza o estado corretamente."""
        state = create_initial_state("Café aumenta produtividade")

        # Mock da resposta do LLM gerando a pergunta
        mock_question_response = AIMessage(content="Qual é a população-alvo do estudo?")

        # Mock da resposta do usuário
        mock_user_answer = "Adultos de 18-40 anos"

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM, \
             patch('agents.methodologist.nodes.ask_user') as mock_ask_user:

            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_question_response
            mock_ask_user.return_value = mock_user_answer

            result = ask_clarification(state)

        # Verificar que ask_user foi chamado
        mock_ask_user.assert_called_once()

        # Verificar updates do estado
        assert 'clarifications' in result
        assert "Qual é a população-alvo do estudo?" in result['clarifications']
        assert result['clarifications']["Qual é a população-alvo do estudo?"] == mock_user_answer

        assert 'iterations' in result
        assert result['iterations'] == 1

        assert 'messages' in result
        assert len(result['messages']) == 2  # Pergunta do LLM + resposta do usuário

    def test_ask_clarification_increments_iterations(self):
        """Testa que ask_clarification incrementa o contador de iterações."""
        state = create_initial_state("Café aumenta produtividade")
        state['iterations'] = 1

        mock_question_response = AIMessage(content="Quais são as variáveis dependentes?")
        mock_user_answer = "Tempo de reação"

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM, \
             patch('agents.methodologist.nodes.ask_user') as mock_ask_user:

            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_question_response
            mock_ask_user.return_value = mock_user_answer

            result = ask_clarification(state)

        assert result['iterations'] == 2

    def test_ask_clarification_stops_at_max_iterations(self):
        """Testa que ask_clarification para quando atinge max_iterations."""
        state = create_initial_state("Café aumenta produtividade", max_iterations=3)
        state['iterations'] = 3  # Já atingiu o limite

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM, \
             patch('agents.methodologist.nodes.ask_user') as mock_ask_user:

            result = ask_clarification(state)

        # Não deve chamar ask_user
        mock_ask_user.assert_not_called()

        # Deve retornar mensagem indicando que atingiu o limite
        assert 'messages' in result
        assert "Limite de perguntas atingido" in result['messages'][0].content

    def test_ask_clarification_avoids_duplicate_questions(self):
        """Testa que ask_clarification considera perguntas já feitas."""
        state = create_initial_state("Café aumenta produtividade")
        state['clarifications'] = {"População?": "Adultos"}

        mock_question_response = AIMessage(content="Quais métricas serão usadas?")

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM, \
             patch('agents.methodologist.nodes.ask_user') as mock_ask_user:

            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_question_response
            mock_ask_user.return_value = "Tempo de reação no teste PVT"

            result = ask_clarification(state)
            call_args = mock_llm.invoke.call_args

            # Verificar que o prompt inclui perguntas já feitas
            prompt_content = call_args[0][0][0].content
            assert "Perguntas já feitas:" in prompt_content
            assert "População?" in prompt_content

    def test_ask_clarification_logs_interaction(self, caplog):
        """Testa que ask_clarification registra logs da interação."""
        state = create_initial_state("Café aumenta produtividade")

        mock_question_response = AIMessage(content="Qual é a população?")
        mock_user_answer = "Adultos"

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM, \
             patch('agents.methodologist.nodes.ask_user') as mock_ask_user:

            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_question_response
            mock_ask_user.return_value = mock_user_answer

            with caplog.at_level('INFO'):
                ask_clarification(state)

            assert "NÓ ASK_CLARIFICATION: Solicitando clarificação" in caplog.text
            assert "Pergunta formulada:" in caplog.text
            assert "Resposta do usuário:" in caplog.text
            assert "NÓ ASK_CLARIFICATION: Finalizado" in caplog.text


# ==============================================================================
# TESTES DO NÓ DECIDE
# ==============================================================================

class TestDecideNode:
    """Testes para o nó decide."""

    def test_decide_approves_good_hypothesis(self):
        """Testa que decide aprova uma hipótese bem formulada."""
        state = create_initial_state("O consumo de 200mg de cafeína melhora tempo de reação em 10% no teste PVT em adultos 18-40 anos")

        mock_response = AIMessage(content='{"decision": "approved", "justification": "Hipótese testável, falseável e específica"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = decide(state)

        assert result['status'] == 'approved'
        assert 'justification' in result
        assert len(result['justification']) > 0
        assert 'messages' in result

    def test_decide_rejects_bad_hypothesis(self):
        """Testa que decide rejeita uma hipótese mal formulada."""
        state = create_initial_state("Café faz bem")

        mock_response = AIMessage(content='{"decision": "rejected", "justification": "Hipótese vaga, não-testável e sem métricas"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = decide(state)

        assert result['status'] == 'rejected'
        assert 'justification' in result
        assert 'vaga' in result['justification'].lower()

    def test_decide_considers_clarifications(self):
        """Testa que decide considera clarificações obtidas."""
        state = create_initial_state("Café aumenta produtividade")
        state['clarifications'] = {
            "População?": "Adultos 18-40 anos",
            "Métricas?": "Tempo de reação no teste PVT",
            "Dose?": "200mg de cafeína"
        }

        mock_response = AIMessage(content='{"decision": "approved", "justification": "Com as clarificações, a hipótese se tornou testável"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = decide(state)
            call_args = mock_llm.invoke.call_args

            # Verificar que o prompt inclui as clarificações
            prompt_content = call_args[0][0][0].content
            assert "Clarificações obtidas:" in prompt_content
            assert "Adultos 18-40 anos" in prompt_content
            assert "Tempo de reação no teste PVT" in prompt_content

    def test_decide_handles_json_parse_error(self):
        """Testa que decide trata erro de parse do JSON rejeitando por segurança."""
        state = create_initial_state("Café aumenta produtividade")

        mock_response = AIMessage(content='Resposta sem JSON válido')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = decide(state)

        # Deve rejeitar por segurança
        assert result['status'] == 'rejected'
        assert 'Erro ao processar' in result['justification']

    def test_decide_validates_status(self):
        """Testa que decide valida o status retornado pelo LLM."""
        state = create_initial_state("Café aumenta produtividade")

        # Status inválido
        mock_response = AIMessage(content='{"decision": "maybe", "justification": "Não tenho certeza"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            result = decide(state)

        # Deve usar "rejected" como padrão
        assert result['status'] == 'rejected'

    def test_decide_logs_decision(self, caplog):
        """Testa que decide registra logs da decisão."""
        state = create_initial_state("Café aumenta produtividade")

        mock_response = AIMessage(content='{"decision": "approved", "justification": "Hipótese adequada"}')

        with patch('agents.methodologist.nodes.ChatAnthropic') as MockLLM:
            mock_llm = MockLLM.return_value
            mock_llm.invoke.return_value = mock_response

            with caplog.at_level('INFO'):
                decide(state)

            assert "NÓ DECIDE: Tomando decisão final" in caplog.text
            assert "Decisão final: approved" in caplog.text
            assert "NÓ DECIDE: Finalizado" in caplog.text
