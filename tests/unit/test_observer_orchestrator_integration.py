"""
Testes de integracao Observer-Orchestrator (Epico 13.3 + 13.4).

Valida a integracao entre o Observer e o Orchestrator:
- _consult_observer() chama funcoes do Observer corretamente
- Resultados do Observer sao armazenados no state
- Checkpoints contextuais funcionam como esperado

Usa mocks para LLM - nao faz chamadas reais.

Versao: 1.0
Data: 09/12/2025
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import json

# Mock chromadb e langgraph antes de importar modulos que dependem deles
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()
sys.modules['langgraph'] = MagicMock()
sys.modules['langgraph.graph'] = MagicMock()
sys.modules['langgraph.graph.message'] = MagicMock()
sys.modules['langgraph.graph.message'].add_messages = lambda x: x


class TestConsultObserverFunction:
    """Testes para a funcao _consult_observer."""

    def test_function_exists(self):
        """Valida que funcao existe e e importavel."""
        from agents.orchestrator.nodes import _consult_observer
        assert callable(_consult_observer)

    def test_returns_dict_with_required_fields(self):
        """Valida que retorno contem campos obrigatorios."""
        from agents.orchestrator.nodes import _consult_observer

        # Mock state minimo
        state = {
            "user_input": "LLMs aumentam produtividade",
            "messages": [],
            "focal_argument": None
        }

        # Mock das funcoes do Observer
        mock_clarity = {
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Conversa fluindo bem",
            "needs_checkpoint": False,
            "factors": {
                "claim_definition": "parcial",
                "coherence": "alta",
                "direction_stability": "estavel"
            },
            "suggestion": None
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = mock_clarity

            result = _consult_observer(
                state=state,
                user_input="teste",
                cognitive_model={"claim": "LLMs"}
            )

        # Campos obrigatorios
        assert "clarity_evaluation" in result
        assert "variation_analysis" in result
        assert "needs_checkpoint" in result
        assert "checkpoint_reason" in result

    def test_calls_evaluate_clarity_when_cognitive_model_exists(self):
        """Testa que evaluate_conversation_clarity e chamado com cognitive_model."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}
        cognitive_model = {"claim": "LLMs aumentam produtividade"}

        mock_clarity_result = {
            "clarity_level": "cristalina",
            "clarity_score": 5,
            "needs_checkpoint": False,
            "description": "OK",
            "factors": {},
            "suggestion": None
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = mock_clarity_result

            result = _consult_observer(
                state=state,
                user_input="novo input",
                cognitive_model=cognitive_model
            )

        mock_eval.assert_called_once()
        assert result["clarity_evaluation"] == mock_clarity_result

    def test_calls_detect_variation_when_previous_claim_exists(self):
        """Testa que detect_variation e chamado quando ha claim anterior."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "novo input", "messages": [], "focal_argument": None}
        cognitive_model = {"claim": "LLMs aumentam produtividade"}

        mock_variation_result = {
            "classification": "variation",
            "analysis": "Mesmo tema",
            "shared_concepts": ["LLMs"],
            "new_concepts": [],
            "reasoning": "Apenas refinamento"
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = {
                "clarity_level": "clara",
                "clarity_score": 4,
                "needs_checkpoint": False,
                "factors": {},
                "suggestion": None
            }

            with patch('agents.orchestrator.nodes.detect_variation') as mock_detect:
                mock_detect.return_value = mock_variation_result

                result = _consult_observer(
                    state=state,
                    user_input="LLMs melhoram velocidade",
                    cognitive_model=cognitive_model
                )

        mock_detect.assert_called_once()
        assert result["variation_analysis"] == mock_variation_result

    def test_sets_needs_checkpoint_when_clarity_low(self):
        """Testa que needs_checkpoint e True quando clareza e baixa."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}
        cognitive_model = {"claim": "Algo vago"}

        mock_clarity_result = {
            "clarity_level": "confusa",
            "clarity_score": 1,
            "needs_checkpoint": True,
            "description": "Conversa confusa",
            "factors": {
                "claim_definition": "vago",
                "coherence": "baixa",
                "direction_stability": "instavel"
            },
            "suggestion": "Definir melhor o objetivo"
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = mock_clarity_result

            result = _consult_observer(
                state=state,
                user_input="???",
                cognitive_model=cognitive_model
            )

        assert result["needs_checkpoint"] is True
        assert "confusa" in result["checkpoint_reason"]

    def test_sets_needs_checkpoint_when_real_change_detected(self):
        """Testa que needs_checkpoint e True quando mudanca real detectada."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}
        cognitive_model = {"claim": "LLMs aumentam produtividade"}

        mock_clarity_result = {
            "clarity_level": "clara",
            "clarity_score": 4,
            "needs_checkpoint": False,
            "factors": {},
            "suggestion": None
        }

        mock_variation_result = {
            "classification": "real_change",
            "analysis": "Mudanca de topico completa",
            "shared_concepts": [],
            "new_concepts": ["bugs", "testes"],
            "reasoning": "Usuario mudou de assunto"
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = mock_clarity_result

            with patch('agents.orchestrator.nodes.detect_variation') as mock_detect:
                mock_detect.return_value = mock_variation_result

                result = _consult_observer(
                    state=state,
                    user_input="Bugs sao causados por falta de testes",
                    cognitive_model=cognitive_model
                )

        assert result["needs_checkpoint"] is True
        # Aceita com ou sem acentos
        assert "Mudan" in result["checkpoint_reason"] and "dire" in result["checkpoint_reason"]

    def test_handles_empty_cognitive_model(self):
        """Testa que funcao lida com cognitive_model vazio."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}

        result = _consult_observer(
            state=state,
            user_input="novo input",
            cognitive_model=None
        )

        # Deve retornar sem erro
        assert result["clarity_evaluation"] is None
        assert result["variation_analysis"] is None
        assert result["needs_checkpoint"] is False

    def test_handles_observer_errors_gracefully(self):
        """Testa que erros no Observer nao quebram a funcao."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}
        cognitive_model = {"claim": "teste"}

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.side_effect = Exception("LLM timeout")

            # Nao deve levantar excecao
            result = _consult_observer(
                state=state,
                user_input="novo input",
                cognitive_model=cognitive_model
            )

        # Deve retornar estrutura valida mesmo com erro
        assert "clarity_evaluation" in result
        assert "needs_checkpoint" in result


class TestStateHasObserverFields:
    """Testes para validar que state tem os novos campos do Observer."""

    def test_state_has_clarity_evaluation_field(self):
        """Valida que MultiAgentState tem campo clarity_evaluation."""
        import os
        # Usar caminho relativo ao projeto
        state_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', 'agents', 'orchestrator', 'state.py'
        )

        with open(state_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "clarity_evaluation" in content
        assert "Optional[dict]" in content

    def test_state_has_variation_analysis_field(self):
        """Valida que MultiAgentState tem campo variation_analysis."""
        import os
        state_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', 'agents', 'orchestrator', 'state.py'
        )

        with open(state_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "variation_analysis" in content


class TestCheckpointContextual:
    """Testes para checkpoints contextuais (Epico 13.4)."""

    def test_checkpoint_adjusts_next_step_to_clarify(self):
        """Testa que checkpoint ajusta next_step para clarify."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "???", "messages": [], "focal_argument": None}
        cognitive_model = {"claim": "Algo vago e confuso"}

        mock_clarity = {
            "clarity_level": "confusa",
            "clarity_score": 1,
            "needs_checkpoint": True,
            "description": "Conversa muito confusa",
            "factors": {
                "claim_definition": "vago",
                "coherence": "baixa",
                "direction_stability": "instavel"
            },
            "suggestion": "Volte ao inicio e defina o objetivo"
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = mock_clarity

            result = _consult_observer(
                state=state,
                user_input="???",
                cognitive_model=cognitive_model
            )

        # O checkpoint deve ser True e ter sugestao
        assert result["needs_checkpoint"] is True
        assert result["clarity_evaluation"]["suggestion"] is not None

    def test_no_checkpoint_for_cristalina_clarity(self):
        """Testa que nao ha checkpoint quando clareza e cristalina."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}
        cognitive_model = {
            "claim": "LLMs aumentam produtividade de desenvolvedores em 30%"
        }

        mock_clarity = {
            "clarity_level": "cristalina",
            "clarity_score": 5,
            "needs_checkpoint": False,
            "description": "Conversa excepcional",
            "factors": {
                "claim_definition": "bem definido",
                "coherence": "alta",
                "direction_stability": "estavel"
            },
            "suggestion": None
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = mock_clarity

            result = _consult_observer(
                state=state,
                user_input="Mais detalhes sobre o estudo",
                cognitive_model=cognitive_model
            )

        assert result["needs_checkpoint"] is False
        assert result["checkpoint_reason"] is None


class TestVariationDetectionIntegration:
    """Testes para integracao da deteccao de variacao."""

    def test_variation_uses_focal_argument_as_fallback(self):
        """Testa que usa focal_argument quando claim nao existe."""
        from agents.orchestrator.nodes import _consult_observer

        state = {
            "user_input": "teste",
            "messages": [],
            "focal_argument": {"subject": "LLMs e produtividade"}
        }

        # cognitive_model sem claim
        cognitive_model = {"proposicoes": []}

        mock_variation = {
            "classification": "variation",
            "analysis": "Mesmo tema",
            "shared_concepts": ["LLMs"],
            "new_concepts": [],
            "reasoning": "OK"
        }

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = {
                "clarity_level": "clara",
                "clarity_score": 4,
                "needs_checkpoint": False,
                "factors": {},
                "suggestion": None
            }

            with patch('agents.orchestrator.nodes.detect_variation') as mock_detect:
                mock_detect.return_value = mock_variation

                result = _consult_observer(
                    state=state,
                    user_input="LLMs sao rapidos",
                    cognitive_model=cognitive_model
                )

        # Deve ter chamado detect_variation usando focal_argument
        mock_detect.assert_called_once()
        call_args = mock_detect.call_args
        assert call_args[1]["previous_text"] == "LLMs e produtividade"

    def test_no_variation_detection_without_previous_claim(self):
        """Testa que nao detecta variacao sem claim anterior."""
        from agents.orchestrator.nodes import _consult_observer

        state = {
            "user_input": "teste",
            "messages": [],
            "focal_argument": None
        }

        cognitive_model = {}  # Sem claim

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = {
                "clarity_level": "clara",
                "clarity_score": 4,
                "needs_checkpoint": False,
                "factors": {},
                "suggestion": None
            }

            with patch('agents.orchestrator.nodes.detect_variation') as mock_detect:
                result = _consult_observer(
                    state=state,
                    user_input="Primeiro input",
                    cognitive_model=cognitive_model
                )

        # Nao deve ter chamado detect_variation
        mock_detect.assert_not_called()
        assert result["variation_analysis"] is None


class TestClarityLevelMappings:
    """Testes para validar mapeamento de niveis de clareza."""

    def test_cristalina_no_checkpoint(self):
        """Cristalina nao precisa de checkpoint."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = {
                "clarity_level": "cristalina",
                "clarity_score": 5,
                "needs_checkpoint": False,
                "factors": {},
                "suggestion": None
            }

            result = _consult_observer(
                state=state,
                user_input="teste",
                cognitive_model={"claim": "teste"}
            )

        assert result["needs_checkpoint"] is False

    def test_clara_no_checkpoint(self):
        """Clara nao precisa de checkpoint."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = {
                "clarity_level": "clara",
                "clarity_score": 4,
                "needs_checkpoint": False,
                "factors": {},
                "suggestion": None
            }

            result = _consult_observer(
                state=state,
                user_input="teste",
                cognitive_model={"claim": "teste"}
            )

        assert result["needs_checkpoint"] is False

    def test_nebulosa_needs_checkpoint(self):
        """Nebulosa precisa de checkpoint."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "teste", "messages": [], "focal_argument": None}

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = {
                "clarity_level": "nebulosa",
                "clarity_score": 3,
                "needs_checkpoint": True,
                "description": "Ha pontos a esclarecer",
                "factors": {},
                "suggestion": "Defina melhor"
            }

            result = _consult_observer(
                state=state,
                user_input="teste",
                cognitive_model={"claim": "teste"}
            )

        assert result["needs_checkpoint"] is True

    def test_confusa_needs_checkpoint(self):
        """Confusa precisa de checkpoint."""
        from agents.orchestrator.nodes import _consult_observer

        state = {"user_input": "???", "messages": [], "focal_argument": None}

        with patch('agents.orchestrator.nodes.evaluate_conversation_clarity') as mock_eval:
            mock_eval.return_value = {
                "clarity_level": "confusa",
                "clarity_score": 1,
                "needs_checkpoint": True,
                "description": "Conversa muito confusa",
                "factors": {},
                "suggestion": "Recomece do zero"
            }

            result = _consult_observer(
                state=state,
                user_input="???",
                cognitive_model={"claim": "???"}
            )

        assert result["needs_checkpoint"] is True
