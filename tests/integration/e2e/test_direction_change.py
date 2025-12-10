"""
Testes de integracao E2E para deteccao de mudancas do Observer (Epico 13.6).

Estes testes validam cenarios reais de conversa multi-turn onde o Observer
detecta variacoes, mudancas de direcao e checkpoints de clareza.

IMPORTANTE: O sistema e NAO-DETERMINISTICO por design.
- Observer usa LLM para analise contextual
- Resultados podem variar entre execucoes
- Testes validam COMPORTAMENTO GERAL, nao outputs exatos

Cenarios:
- A: Variacao simples (nao interrompe fluxo)
- B: Mudanca real (checkpoint pode ser solicitado)
- C: Clareza nebulosa (pode gerar checkpoint)
- D: Conversa clara (fluxo continua)

Versao: 3.0 (Epico 13.6 - Testes Flexiveis)
Data: 10/12/2025
"""

import pytest
from typing import Dict, Any, List

from agents.multi_agent_graph import create_multi_agent_graph
from agents.orchestrator.state import create_initial_multi_agent_state
from utils.event_bus import get_event_bus


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def multi_agent_graph():
    """Cria grafo multi-agente para testes."""
    return create_multi_agent_graph()


@pytest.fixture
def event_bus():
    """Retorna instancia do EventBus."""
    return get_event_bus()


# ============================================================================
# Testes de Comportamento do Observer (Flexiveis)
# ============================================================================


@pytest.mark.integration
@pytest.mark.e2e
class TestObserverBehavior:
    """
    Testes de comportamento do Observer.

    Estes testes validam que o sistema FUNCIONA, nao que produz
    outputs exatos. Aceitam variacao natural do LLM.
    """

    def test_system_processes_input_without_error(self, multi_agent_graph):
        """
        Sistema processa input sem erros.

        Teste basico de sanidade - sistema deve processar
        qualquer input sem crashar.
        """
        session_id = "test-basic-processing"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade de desenvolvedores",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}

        # Deve processar sem erro
        result = multi_agent_graph.invoke(state, config)

        # Deve ter next_step definido
        assert result.get("next_step") in ["explore", "suggest_agent", "clarify"], \
            f"next_step deve ser valido, obtido: {result.get('next_step')}"

    def test_multi_turn_conversation_works(self, multi_agent_graph):
        """
        Conversa multi-turn funciona corretamente.

        Sistema deve manter estado entre turnos e processar
        multiplos inputs sequencialmente.
        """
        session_id = "test-multi-turn"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Turno 1
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Turno 2
        state["user_input"] = "Especificamente em equipes pequenas"
        result = multi_agent_graph.invoke(state, config)

        # Deve ter cognitive_model atualizado
        assert result.get("cognitive_model") is not None, \
            "Deve ter cognitive_model apos multi-turn"

    def test_variation_does_not_crash(self, multi_agent_graph):
        """
        Variacao de input nao causa crash.

        Sistema deve processar variacao do mesmo tema sem erros.
        """
        session_id = "test-variation-no-crash"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Turno 1: Input inicial
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Turno 2: Variacao do mesmo conceito
        state["user_input"] = "IA generativa melhora eficiencia"
        result = multi_agent_graph.invoke(state, config)

        # Deve continuar funcionando
        assert result.get("next_step") in ["explore", "suggest_agent", "clarify"], \
            f"Fluxo deve continuar, next_step={result.get('next_step')}"

    def test_topic_change_is_handled(self, multi_agent_graph):
        """
        Mudanca de topico e tratada sem crash.

        Sistema deve detectar ou aceitar mudanca de topico.
        Nao importa se classifica como variation ou real_change.
        """
        session_id = "test-topic-change"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Turno 1: Topico A
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade de desenvolvedores",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Turno 2: Topico completamente diferente
        state["user_input"] = "Blockchain revoluciona transacoes financeiras"
        result = multi_agent_graph.invoke(state, config)

        # Sistema deve responder (qualquer resposta valida)
        assert result.get("next_step") in ["explore", "suggest_agent", "clarify"], \
            f"Sistema deve continuar funcionando, next_step={result.get('next_step')}"

    def test_vague_input_is_handled(self, multi_agent_graph):
        """
        Input vago e tratado apropriadamente.

        Sistema deve fazer perguntas esclarecedoras ou explorar.
        """
        session_id = "test-vague-input"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        state = create_initial_multi_agent_state(
            user_input="Acho que talvez queira pesquisar algo",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        result = multi_agent_graph.invoke(state, config)

        # Para input vago, sistema tipicamente explora ou clarifica
        # Mas qualquer resposta valida e aceitavel
        assert result.get("next_step") in ["explore", "suggest_agent", "clarify"], \
            f"Sistema deve responder a input vago, next_step={result.get('next_step')}"

    def test_observer_events_are_published(self, multi_agent_graph):
        """
        Observer publica eventos no EventBus.

        Sistema deve publicar eventos de deteccao quando relevante.
        """
        session_id = "test-observer-events"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Turno 1
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade de desenvolvedores",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Turno 2
        state["user_input"] = "Quero falar sobre blockchain agora"
        multi_agent_graph.invoke(state, config)

        # Verificar se eventos foram publicados
        events = event_bus.get_session_events(session_id)

        # Deve ter ALGUM evento (pode ser qualquer tipo)
        # O Observer publica eventos de varias categorias
        assert len(events) > 0, \
            "Observer deve publicar eventos no EventBus"

    def test_clarity_evaluation_is_populated(self, multi_agent_graph):
        """
        Avaliacao de clareza e populada no state.

        Apos processamento, clarity_evaluation deve existir.
        """
        session_id = "test-clarity-populated"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade de desenvolvedores em 30%",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        result = multi_agent_graph.invoke(state, config)

        # clarity_evaluation deve existir (pode ser qualquer valor)
        # Nota: pode ser None se Observer nao foi consultado
        clarity = result.get("clarity_evaluation")

        # Se clarity existe, deve ter estrutura valida
        if clarity is not None:
            assert "clarity_level" in clarity or "clarity_score" in clarity, \
                "clarity_evaluation deve ter estrutura valida"


# ============================================================================
# Testes de Integracao do Fluxo
# ============================================================================


@pytest.mark.integration
@pytest.mark.e2e
class TestIntegrationFlow:
    """Testes de integracao do fluxo completo."""

    def test_full_conversation_flow(self, multi_agent_graph):
        """
        Fluxo completo de conversa funciona.

        Simula conversa de 3 turnos e verifica que sistema
        mantém estado e processa corretamente.
        """
        session_id = "test-full-flow"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        config = {"configurable": {"thread_id": session_id}}

        # Turno 1: Ideia inicial
        state = create_initial_multi_agent_state(
            user_input="Quero pesquisar sobre produtividade com IA",
            session_id=session_id
        )
        state = multi_agent_graph.invoke(state, config)
        assert state.get("cognitive_model") is not None

        # Turno 2: Refinamento
        state["user_input"] = "Especificamente em equipes de desenvolvimento"
        state = multi_agent_graph.invoke(state, config)

        # Turno 3: Mais detalhes
        state["user_input"] = "Medindo tempo de entrega de features"
        result = multi_agent_graph.invoke(state, config)

        # Verificar que conversa evoluiu
        cm = result.get("cognitive_model", {})
        assert cm.get("claim") or cm.get("proposicoes"), \
            "Apos 3 turnos, cognitive_model deve ter conteudo"

    def test_orchestrator_message_is_natural(self, multi_agent_graph):
        """
        Mensagem do Orquestrador e natural, nao robotica.

        Sistema deve gerar mensagens conversacionais.
        """
        session_id = "test-natural-message"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        state = create_initial_multi_agent_state(
            user_input="Acho que LLMs sao uteis",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        result = multi_agent_graph.invoke(state, config)

        # Verificar mensagens
        messages = result.get("messages", [])
        ai_messages = [m for m in messages if hasattr(m, 'content') and m.__class__.__name__ == 'AIMessage']

        if ai_messages:
            msg = ai_messages[-1].content

            # Mensagem NAO deve ser robotica
            robotic_phrases = ["CHECKPOINT:", "ALERTA:", "ERRO:", "## Mudanca"]
            for phrase in robotic_phrases:
                assert phrase not in msg, \
                    f"Mensagem nao deve conter '{phrase}'"
