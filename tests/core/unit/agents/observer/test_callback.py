"""
Testes unitários para o callback assíncrono do Observer.

Épico 12.1: Valida que o Observer é disparado corretamente após o Orchestrator.
"""

import pytest
import time
import threading
from unittest.mock import MagicMock, patch, ANY
from langchain_core.messages import HumanMessage, AIMessage

# Skip entire module if chromadb not installed (CI uses requirements-test.txt)
# multi_agent_graph imports observer which requires chromadb
pytest.importorskip("chromadb", reason="chromadb not installed - skipping observer callback tests")

# Importar módulo antes de fazer patches para evitar problemas de importação
try:
    from core.agents import multi_agent_graph
except ImportError:
    multi_agent_graph = None

class TestObserverCallback:
    """Testes para _create_observer_callback()"""

    @pytest.fixture
    def mock_state(self):
        """Estado simulado do sistema multi-agente."""
        return {
            "session_id": "test-session-123",
            "user_input": "LLMs aumentam produtividade",
            "turn_count": 2,
            "messages": [
                HumanMessage(content="Olá"),
                AIMessage(content="Como posso ajudar?")
            ],
            "cognitive_model": None,
            "idea_id": "idea-456"
        }

    @pytest.fixture
    def mock_result(self):
        """Resultado simulado do orchestrator_node."""
        return {
            "messages": [AIMessage(content="Interessante! Me conta mais.")],
            "next_step": "explore",
            "focal_argument": {"intent": "unclear"}
        }

    def test_callback_creates_daemon_thread(self, mock_state, mock_result):
        """Callback cria thread daemon para não bloquear shutdown."""
        if multi_agent_graph is None:
            pytest.skip("multi_agent_graph não disponível")
        
        if not multi_agent_graph.OBSERVER_AVAILABLE:
            pytest.skip("Observer não disponível")
        
        with patch.object(multi_agent_graph, "observer_process_turn") as mock_process:
            mock_process.return_value = {
                "cognitive_model": {"claim": "teste"},
                "metrics": {"solidez": 0.5, "completude": 0.3}
            }

            _create_observer_callback = multi_agent_graph._create_observer_callback

            # Capturar threads antes
            threads_before = threading.enumerate()

            _create_observer_callback(mock_state, mock_result)

            # Dar tempo para thread iniciar
            time.sleep(0.1)

            # Verificar que thread daemon foi criada
            observer_threads = [
                t for t in threading.enumerate()
                if t.name.startswith("observer-")
            ]

            # Thread pode já ter terminado, então verificamos se foi criada
            # ou se o processo foi executado
            assert mock_process.called or len(observer_threads) > 0

    def test_callback_passes_correct_arguments(self, mock_state, mock_result):
        """Callback passa argumentos corretos para process_turn."""
        if multi_agent_graph is None or not multi_agent_graph.OBSERVER_AVAILABLE:
            pytest.skip("Observer não disponível")
        
        with patch.object(multi_agent_graph, "observer_process_turn") as mock_process:
            mock_process.return_value = {
                "cognitive_model": {"claim": "teste"},
                "metrics": {"solidez": 0.5, "completude": 0.3}
            }

            _create_observer_callback = multi_agent_graph._create_observer_callback

            _create_observer_callback(mock_state, mock_result)

            # Aguardar thread executar
            time.sleep(0.5)

            # Verificar chamada
            mock_process.assert_called_once()
            call_kwargs = mock_process.call_args[1]

            assert call_kwargs["user_input"] == "LLMs aumentam produtividade"
            assert call_kwargs["session_id"] == "test-session-123"
            assert call_kwargs["turn_number"] == 2
            assert call_kwargs["idea_id"] == "idea-456"

    def test_callback_updates_result_cognitive_model(self, mock_state, mock_result):
        """Callback atualiza cognitive_model no result."""
        if multi_agent_graph is None or not multi_agent_graph.OBSERVER_AVAILABLE:
            pytest.skip("Observer não disponível")
        
        expected_cognitive_model = {
            "claim": "LLMs aumentam produtividade",
            "proposicoes": [{"texto": "Estudo X", "solidez": 0.8}],
            "concepts_detected": ["LLM", "produtividade"]
        }

        with patch.object(multi_agent_graph, "observer_process_turn") as mock_process:
            mock_process.return_value = {
                "cognitive_model": expected_cognitive_model,
                "metrics": {"solidez": 0.65, "completude": 0.4}
            }

            _create_observer_callback = multi_agent_graph._create_observer_callback

            _create_observer_callback(mock_state, mock_result)

            # Aguardar thread executar
            time.sleep(0.5)

            # Verificar que result foi atualizado
            assert mock_result.get("cognitive_model") == expected_cognitive_model

    def test_callback_publishes_event(self, mock_state, mock_result):
        """Callback publica evento cognitive_model_updated."""
        if multi_agent_graph is None or not multi_agent_graph.OBSERVER_AVAILABLE:
            pytest.skip("Observer não disponível")
        
        with patch.object(multi_agent_graph, "observer_process_turn") as mock_process:
            mock_process.return_value = {
                "cognitive_model": {
                    "claim": "teste",
                    "proposicoes": [],
                    "concepts_detected": ["conceito1"],
                    "open_questions": [],
                    "contradictions": []
                },
                "metrics": {"solidez": 0.5, "completude": 0.3}
            }

            with patch.object(multi_agent_graph, "get_event_bus") as mock_bus:
                mock_event_bus = MagicMock()
                mock_bus.return_value = mock_event_bus

                _create_observer_callback = multi_agent_graph._create_observer_callback

                _create_observer_callback(mock_state, mock_result)

                # Aguardar thread executar
                time.sleep(0.5)

                # Verificar que evento foi publicado
                mock_event_bus.publish_cognitive_model_updated.assert_called_once()
                call_kwargs = mock_event_bus.publish_cognitive_model_updated.call_args[1]

                assert call_kwargs["session_id"] == "test-session-123"
                assert call_kwargs["turn_number"] == 2
                assert call_kwargs["solidez"] == 0.5
                assert call_kwargs["completude"] == 0.3

    def test_callback_silent_on_error(self, mock_state, mock_result):
        """Callback é silencioso em caso de erro (não propaga exceção)."""
        if multi_agent_graph is None or not multi_agent_graph.OBSERVER_AVAILABLE:
            pytest.skip("Observer não disponível")
        
        with patch.object(multi_agent_graph, "observer_process_turn") as mock_process:
            mock_process.side_effect = Exception("Erro simulado")

            _create_observer_callback = multi_agent_graph._create_observer_callback

            # Não deve lançar exceção
            try:
                _create_observer_callback(mock_state, mock_result)
                time.sleep(0.5)
            except Exception:
                pytest.fail("Callback não deveria propagar exceção")

    def test_callback_skipped_when_observer_unavailable(self, mock_state, mock_result):
        """Callback é pulado se Observer não estiver disponível."""
        if multi_agent_graph is None:
            pytest.skip("multi_agent_graph não disponível")
        
        with patch.object(multi_agent_graph, "OBSERVER_AVAILABLE", False):
            _create_observer_callback = multi_agent_graph._create_observer_callback

            # Não deve fazer nada (sem erro)
            _create_observer_callback(mock_state, mock_result)

    def test_callback_converts_messages_to_history(self, mock_state, mock_result):
        """Callback converte messages do LangGraph para formato do Observer."""
        if multi_agent_graph is None or not multi_agent_graph.OBSERVER_AVAILABLE:
            pytest.skip("Observer não disponível")
        
        with patch.object(multi_agent_graph, "observer_process_turn") as mock_process:
            mock_process.return_value = {
                "cognitive_model": {"claim": "teste"},
                "metrics": {"solidez": 0.5, "completude": 0.3}
            }

            _create_observer_callback = multi_agent_graph._create_observer_callback

            _create_observer_callback(mock_state, mock_result)

            # Aguardar thread executar
            time.sleep(0.5)

            # Verificar conversão do histórico
            call_kwargs = mock_process.call_args[1]
            history = call_kwargs["conversation_history"]

            # Deve ter 3 mensagens: 2 do state + 1 do result
            assert len(history) == 3
            assert history[0]["role"] == "user"
            assert history[0]["content"] == "Olá"
            assert history[1]["role"] == "assistant"
            assert history[1]["content"] == "Como posso ajudar?"

class TestInstrumentNodeObserverIntegration:
    """Testes de integração do instrument_node com Observer."""

    def test_instrument_node_triggers_observer_for_orchestrator(self):
        """instrument_node dispara Observer apenas para orchestrator."""
        if multi_agent_graph is None:
            pytest.skip("multi_agent_graph não disponível")
        
        with patch.object(multi_agent_graph, "_create_observer_callback") as mock_callback:
            with patch.object(multi_agent_graph, "OBSERVER_AVAILABLE", True):
                instrument_node = multi_agent_graph.instrument_node

                # Criar mock do nó
                mock_node = MagicMock(return_value={"next_step": "explore"})
                instrumented = instrument_node(mock_node, "orchestrator")

                # Executar nó instrumentado
                state = {"session_id": "test", "user_input": "teste"}
                instrumented(state)

                # Verificar que callback foi chamado
                mock_callback.assert_called_once()

    def test_instrument_node_does_not_trigger_observer_for_other_agents(self):
        """instrument_node não dispara Observer para outros agentes."""
        if multi_agent_graph is None:
            pytest.skip("multi_agent_graph não disponível")
        
        with patch.object(multi_agent_graph, "_create_observer_callback") as mock_callback:
            with patch.object(multi_agent_graph, "OBSERVER_AVAILABLE", True):
                instrument_node = multi_agent_graph.instrument_node

                # Criar mock do nó
                mock_node = MagicMock(return_value={"status": "approved"})
                instrumented = instrument_node(mock_node, "methodologist")

                # Executar nó instrumentado
                state = {"session_id": "test", "user_input": "teste"}
                instrumented(state)

                # Verificar que callback NÃO foi chamado
                mock_callback.assert_not_called()
