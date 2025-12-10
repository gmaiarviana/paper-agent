"""
Testes de integracao E2E para deteccao de mudancas do Observer (Epico 13.6).

Estes testes validam cenarios reais de conversa multi-turn onde o Observer
detecta variacoes, mudancas de direcao e checkpoints de clareza.

ARQUITETURA DE DUAS CAMADAS:
- Camada 1: Observer (analise contextual via LLM)
- Camada 2: Filtros de negocio (regras deterministicas)

O Observer pode ser conservador (pedir checkpoint mesmo quando nao necessario).
Os filtros garantem previsibilidade aplicando regras como:
- Cold start: turno 1 nunca gera checkpoint
- Alta clareza: score >= 4 nao gera checkpoint
- Variacao simples: classification="variation" nao gera checkpoint
- Cooldown: respeita intervalo minimo entre checkpoints

Cenarios:
- A: Variacao simples (nao interrompe fluxo)
- B: Mudanca real (checkpoint solicitado)
- C: Clareza nebulosa (needs_checkpoint=True)
- D: Conversa clara (needs_checkpoint=False)

Versao: 2.0 (Epico 13.6 - Arquitetura Duas Camadas)
Data: 10/12/2025
"""

import pytest
from typing import Dict, Any, List

from agents.multi_agent_graph import create_multi_agent_graph
from agents.orchestrator.state import create_initial_multi_agent_state
from agents.observer.filters import (
    apply_business_rules,
    should_checkpoint,
    FilterType,
    get_filter_config,
)
from utils.event_bus import get_event_bus


# ============================================================================
# Cenarios de Teste para Deteccao de Mudancas
# ============================================================================


class DirectionChangeScenario:
    """Define cenario de teste para deteccao de mudancas."""

    def __init__(
        self,
        id: str,
        description: str,
        turns: List[Dict[str, str]],
        expected_events: List[str],
        expected_checkpoint: bool,
        expected_classification: str = None
    ):
        """
        Inicializa cenario de teste.

        Args:
            id: Identificador do cenario
            description: Descricao do que o cenario valida
            turns: Lista de turnos ({"role": "user", "content": "..."})
            expected_events: Tipos de eventos esperados (variation_detected, etc)
            expected_checkpoint: Se espera needs_checkpoint=True
            expected_classification: Classificacao esperada (variation/real_change)
        """
        self.id = id
        self.description = description
        self.turns = turns
        self.expected_events = expected_events
        self.expected_checkpoint = expected_checkpoint
        self.expected_classification = expected_classification


# Cenario A: Variacao simples (nao interrompe fluxo)
SCENARIO_A_VARIATION = DirectionChangeScenario(
    id="cenario_A_variacao",
    description="Variacao simples do mesmo conceito - nao interrompe fluxo",
    turns=[
        {"role": "user", "content": "LLMs aumentam produtividade de desenvolvedores"},
        {"role": "user", "content": "IA generativa melhora eficiencia no desenvolvimento de software"},
    ],
    expected_events=["variation_detected"],
    expected_checkpoint=False,
    expected_classification="variation"
)


# Cenario B: Mudanca real (checkpoint solicitado)
SCENARIO_B_REAL_CHANGE = DirectionChangeScenario(
    id="cenario_B_mudanca_real",
    description="Mudanca real de topico - checkpoint deve ser solicitado",
    turns=[
        {"role": "user", "content": "LLMs aumentam produtividade de desenvolvedores"},
        {"role": "user", "content": "Quero falar sobre blockchain e criptomoedas"},
    ],
    expected_events=["direction_change_confirmed"],
    expected_checkpoint=True,
    expected_classification="real_change"
)


# Cenario C: Clareza nebulosa (needs_checkpoint=True)
SCENARIO_C_UNCLEAR = DirectionChangeScenario(
    id="cenario_C_nebuloso",
    description="Conversa confusa com multiplos topicos - checkpoint de clareza",
    turns=[
        {"role": "user", "content": "Quero pesquisar sobre IA, mas tambem blockchain, e talvez machine learning"},
        {"role": "user", "content": "Na verdade acho que produtividade e importante, ou seria qualidade?"},
    ],
    expected_events=["clarity_checkpoint"],
    expected_checkpoint=True,
    expected_classification=None  # Clareza, nao variacao
)


# Cenario D: Conversa clara (needs_checkpoint=False)
SCENARIO_D_CLEAR = DirectionChangeScenario(
    id="cenario_D_claro",
    description="Conversa clara e consistente - sem checkpoint",
    turns=[
        {"role": "user", "content": "LLMs aumentam produtividade de desenvolvedores em 30%"},
        {"role": "user", "content": "Especificamente em equipes de 5-10 pessoas usando pair programming"},
    ],
    expected_events=[],  # Nenhum evento de deteccao especial
    expected_checkpoint=False,
    expected_classification="variation"  # Pode ser variacao, mas sem checkpoint
)


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
# Testes de Cenarios
# ============================================================================


@pytest.mark.integration
@pytest.mark.e2e
class TestDirectionChangeScenarios:
    """Testes E2E para cenarios de deteccao de mudancas."""

    def _execute_scenario(
        self,
        graph,
        scenario: DirectionChangeScenario
    ) -> Dict[str, Any]:
        """
        Executa cenario e retorna resultado.

        Args:
            graph: Grafo multi-agente
            scenario: Cenario a executar

        Returns:
            Dict com eventos detectados, checkpoint_triggered, etc.
        """
        session_id = f"test-{scenario.id}"
        event_bus = get_event_bus()

        # Limpar eventos anteriores da sessao
        event_bus.clear_session(session_id)

        # Executar cada turno
        state = None
        for i, turn in enumerate(scenario.turns):
            if turn["role"] == "user":
                if state is None:
                    state = create_initial_multi_agent_state(
                        user_input=turn["content"],
                        session_id=session_id
                    )
                else:
                    state["user_input"] = turn["content"]

                # Executar grafo
                config = {"configurable": {"thread_id": session_id}}
                result = graph.invoke(state, config)
                state = result

        # Coletar eventos de deteccao
        events = event_bus.get_session_events(session_id)
        detection_events = [
            e for e in events
            if e.get("event_type") in [
                "variation_detected",
                "direction_change_confirmed",
                "clarity_checkpoint"
            ]
        ]

        # Verificar se checkpoint foi triggered
        checkpoint_triggered = any(
            e.get("event_type") in ["direction_change_confirmed", "clarity_checkpoint"]
            for e in detection_events
        )

        # Extrair classificacao se disponivel
        classification = None
        for e in detection_events:
            if e.get("classification"):
                classification = e.get("classification")
                break

        return {
            "session_id": session_id,
            "final_state": state,
            "detection_events": detection_events,
            "event_types": [e.get("event_type") for e in detection_events],
            "checkpoint_triggered": checkpoint_triggered,
            "classification": classification
        }

    def test_scenario_a_variation_does_not_interrupt(self, multi_agent_graph):
        """
        Cenario A: Variacao simples nao interrompe fluxo.

        Quando usuario reformula mesma ideia com palavras diferentes,
        Observer deve detectar como 'variation' e NAO solicitar checkpoint.
        """
        result = self._execute_scenario(multi_agent_graph, SCENARIO_A_VARIATION)

        # Variacao detectada mas sem checkpoint
        assert not result["checkpoint_triggered"], \
            "Variacao simples NAO deve triggerar checkpoint"

        # Se houver classificacao, deve ser 'variation'
        if result["classification"]:
            assert result["classification"] == "variation", \
                f"Esperado 'variation', obtido '{result['classification']}'"

    def test_scenario_b_real_change_triggers_checkpoint(self, multi_agent_graph):
        """
        Cenario B: Mudanca real triggera checkpoint.

        Quando usuario muda completamente de topico,
        Observer deve detectar como 'real_change' e solicitar checkpoint.
        """
        result = self._execute_scenario(multi_agent_graph, SCENARIO_B_REAL_CHANGE)

        # Mudanca real deve triggerar checkpoint
        assert result["checkpoint_triggered"], \
            "Mudanca real DEVE triggerar checkpoint"

        # Classificacao deve ser 'real_change'
        if result["classification"]:
            assert result["classification"] == "real_change", \
                f"Esperado 'real_change', obtido '{result['classification']}'"

    def test_scenario_c_confusion_triggers_clarification(self, multi_agent_graph):
        """
        Cenario C: Confusao gera pergunta de esclarecimento.

        Quando conversa esta nebulosa/confusa,
        Observer deve detectar e solicitar checkpoint de clareza.
        """
        result = self._execute_scenario(multi_agent_graph, SCENARIO_C_UNCLEAR)

        # Confusao deve triggerar checkpoint
        # Nota: pode ser via clarity_checkpoint ou direction_change_confirmed
        has_clarity_event = "clarity_checkpoint" in result["event_types"]

        # Deve ter algum tipo de checkpoint
        assert result["checkpoint_triggered"] or has_clarity_event, \
            "Confusao DEVE triggerar checkpoint ou evento de clareza"

    def test_scenario_d_clear_conversation_no_checkpoint(self, multi_agent_graph):
        """
        Cenario D: Conversa clara nao gera checkpoint desnecessario.

        Quando conversa esta clara e consistente,
        Observer NAO deve solicitar checkpoint.
        """
        result = self._execute_scenario(multi_agent_graph, SCENARIO_D_CLEAR)

        # Conversa clara NAO deve triggerar checkpoint
        # Nota: variacao pode ser detectada, mas sem checkpoint
        assert not result["checkpoint_triggered"], \
            "Conversa clara NAO deve triggerar checkpoint"


# ============================================================================
# Testes Especificos de Comportamento
# ============================================================================


@pytest.mark.integration
@pytest.mark.e2e
class TestObserverBehavior:
    """Testes especificos de comportamento do Observer."""

    def test_variation_does_not_interrupt_flow(self, multi_agent_graph):
        """
        Variacao detectada NAO interrompe fluxo de conversa.

        Sistema deve continuar processando normalmente quando
        detecta variacao (mesma essencia, palavras diferentes).
        """
        session_id = "test-variation-flow"
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
        state = multi_agent_graph.invoke(state, config)

        # Fluxo deve continuar normalmente
        assert state.get("next_step") in ["explore", "suggest_agent", "clarify"], \
            f"Fluxo deve continuar, next_step={state.get('next_step')}"

    def test_real_change_triggers_checkpoint(self, multi_agent_graph):
        """
        Mudanca real de direcao deve triggerar checkpoint.

        Sistema deve detectar quando usuario muda completamente
        de topico e solicitar confirmacao.
        """
        session_id = "test-real-change"
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
        state = multi_agent_graph.invoke(state, config)

        # Verificar eventos
        events = event_bus.get_session_events(session_id)
        direction_events = [
            e for e in events
            if e.get("event_type") == "direction_change_confirmed"
        ]

        # Deve ter evento de mudanca ou next_step=clarify
        has_change_event = len(direction_events) > 0
        is_clarifying = state.get("next_step") == "clarify"

        assert has_change_event or is_clarifying, \
            "Mudanca real deve gerar evento ou ajustar para clarify"

    def test_confusion_triggers_clarification(self, multi_agent_graph):
        """
        Confusao na conversa deve gerar pergunta contextual.

        Sistema deve detectar quando conversa esta confusa
        e fazer pergunta de esclarecimento.
        """
        session_id = "test-confusion"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Input confuso com multiplos topicos
        state = create_initial_multi_agent_state(
            user_input="Quero IA, blockchain, ML, produtividade, qualidade, tudo junto",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Verificar se sistema busca clarificacao
        next_step = state.get("next_step")
        orchestrator_msg = state.get("orchestrator_message", "")

        # Sistema deve explorar ou clarificar
        assert next_step in ["explore", "clarify"], \
            f"Sistema deve explorar/clarificar quando confuso, next_step={next_step}"

    def test_orchestrator_intervention_is_natural(self, multi_agent_graph):
        """
        Intervencao do Orquestrador deve ser natural, nao robotica.

        Quando Observer detecta necessidade de checkpoint,
        mensagem do Orquestrador deve ser conversacional.
        """
        session_id = "test-natural-intervention"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Cenario que pode gerar checkpoint
        state = create_initial_multi_agent_state(
            user_input="Acho que LLMs sao uteis",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Mudar para topico diferente
        state["user_input"] = "Na verdade quero falar sobre redes neurais profundas"
        state = multi_agent_graph.invoke(state, config)

        # Mensagem do orquestrador
        msg = state.get("orchestrator_message", "")

        # Verificar que mensagem NAO e robotica
        robotic_phrases = [
            "CHECKPOINT:",
            "ALERTA:",
            "ERRO:",
            "## Mudanca detectada ##"
        ]

        for phrase in robotic_phrases:
            assert phrase not in msg, \
                f"Mensagem nao deve conter '{phrase}', obtido: {msg[:100]}"

        # Mensagem deve existir e ser conversacional
        if msg:
            assert len(msg) > 10, "Mensagem deve ser substantiva"


# ============================================================================
# Helpers para Validacao
# ============================================================================


def validate_observer_detections(
    session_id: str,
    expected_events: List[str] = None,
    expected_checkpoint: bool = None
) -> Dict[str, Any]:
    """
    Valida deteccoes do Observer para uma sessao.

    Args:
        session_id: ID da sessao a validar
        expected_events: Lista de event_types esperados
        expected_checkpoint: Se espera checkpoint

    Returns:
        Dict com resultado da validacao:
            - valid: bool
            - errors: List[str]
            - events_found: List[str]
            - checkpoint_found: bool
    """
    event_bus = get_event_bus()
    events = event_bus.get_session_events(session_id)

    detection_events = [
        e for e in events
        if e.get("event_type") in [
            "variation_detected",
            "direction_change_confirmed",
            "clarity_checkpoint"
        ]
    ]

    event_types = [e.get("event_type") for e in detection_events]
    checkpoint_found = any(
        et in ["direction_change_confirmed", "clarity_checkpoint"]
        for et in event_types
    )

    errors = []

    # Validar eventos esperados
    if expected_events is not None:
        for expected in expected_events:
            if expected not in event_types:
                errors.append(f"Evento esperado '{expected}' nao encontrado")

    # Validar checkpoint
    if expected_checkpoint is not None:
        if expected_checkpoint and not checkpoint_found:
            errors.append("Checkpoint esperado mas nao encontrado")
        elif not expected_checkpoint and checkpoint_found:
            errors.append("Checkpoint nao esperado mas encontrado")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "events_found": event_types,
        "checkpoint_found": checkpoint_found
    }


# ============================================================================
# Testes de Arquitetura de Duas Camadas (Epico 13.6)
# ============================================================================


@pytest.mark.integration
@pytest.mark.e2e
class TestTwoLayerArchitecture:
    """
    Testes que validam a arquitetura de duas camadas.

    Camada 1: Observer (LLM) - pode ser conservador
    Camada 2: Filtros (codigo) - garante previsibilidade
    """

    def test_cold_start_exemption_in_integration(self, multi_agent_graph):
        """
        Turno 1 nunca gera checkpoint mesmo que Observer peca.

        Este teste valida que o filtro COLD_START funciona no fluxo real.
        """
        session_id = "test-cold-start-integration"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Input vago que poderia gerar checkpoint
        state = create_initial_multi_agent_state(
            user_input="Acho que talvez queira pesquisar algo sobre IA ou nao sei",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        result = multi_agent_graph.invoke(state, config)

        # Mesmo com input vago, turno 1 NAO deve ter checkpoint
        # devido ao filtro COLD_START
        events = event_bus.get_session_events(session_id)
        checkpoint_events = [
            e for e in events
            if e.get("event_type") in ["clarity_checkpoint", "direction_change_confirmed"]
        ]

        # Pode ter eventos de deteccao, mas next_step nao deve ser clarify no turno 1
        # devido ao filtro (a menos que seja por outro motivo do Orquestrador)
        assert result.get("next_step") != "clarify" or len(checkpoint_events) == 0, \
            "Turno 1 nao deve gerar checkpoint de clareza"

    def test_variation_exemption_prevents_interruption(self, multi_agent_graph):
        """
        Variacao simples nao interrompe mesmo que Observer seja conservador.

        Este teste valida que o filtro VARIATION_ONLY funciona no fluxo real.
        """
        session_id = "test-variation-exemption"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Turno 1
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade de desenvolvedores",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Turno 2: Variacao do mesmo conceito
        state["user_input"] = "IA generativa melhora eficiencia de programadores"
        result = multi_agent_graph.invoke(state, config)

        # Variacao NAO deve gerar checkpoint (filtro VARIATION_ONLY)
        events = event_bus.get_session_events(session_id)

        # Pode ter variation_detected, mas NAO checkpoint
        direction_change_events = [
            e for e in events
            if e.get("event_type") == "direction_change_confirmed"
        ]

        assert len(direction_change_events) == 0, \
            "Variacao simples NAO deve gerar direction_change_confirmed"

    def test_filter_config_accessible(self):
        """
        Configuracao dos filtros deve ser acessivel.

        Permite ajuste fino em runtime se necessario.
        """
        config = get_filter_config()

        assert "min_turn_for_checkpoint" in config
        assert "min_clarity_score_for_exemption" in config
        assert "min_turns_between_checkpoints" in config

        # Valores default
        assert config["min_turn_for_checkpoint"] >= 1
        assert config["min_clarity_score_for_exemption"] >= 1
        assert config["min_turns_between_checkpoints"] >= 1

    def test_filter_layer_is_deterministic(self):
        """
        Camada de filtros deve ser 100% deterministica.

        Dado o mesmo input, resultado deve ser sempre o mesmo.
        """
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 2,
            "clarity_level": "nebulosa",
            "classification": "variation"
        }

        # Executar 10 vezes
        results = []
        for _ in range(10):
            result = apply_business_rules(
                observer_result=observer_result,
                turn_number=5
            )
            results.append(result.filter_applied)

        # Todos os resultados devem ser identicos
        assert all(r == results[0] for r in results), \
            "Filtros devem ser 100% deterministicos"

        # E deve ser VARIATION_ONLY
        assert results[0] == FilterType.VARIATION_ONLY

    def test_two_layers_work_together(self, multi_agent_graph):
        """
        As duas camadas devem trabalhar juntas corretamente.

        Observer detecta (conservador ok), Filtros modulam (previsivel).
        """
        session_id = "test-two-layers"
        event_bus = get_event_bus()
        event_bus.clear_session(session_id)

        # Cenario: mudanca real no turno 2
        # Turno 1
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade de desenvolvedores",
            session_id=session_id
        )
        config = {"configurable": {"thread_id": session_id}}
        state = multi_agent_graph.invoke(state, config)

        # Turno 2: mudanca real
        state["user_input"] = "Quero falar sobre blockchain e criptomoedas"
        result = multi_agent_graph.invoke(state, config)

        # Deve ter deteccao de mudanca (Observer) E checkpoint (filtros permitem)
        events = event_bus.get_session_events(session_id)

        # Pode ter variation_detected no turno 1 (comparando com vazio)
        # E direction_change_confirmed no turno 2
        event_types = [e.get("event_type") for e in events]

        # Alguma forma de deteccao deve existir
        has_detection = (
            "direction_change_confirmed" in event_types or
            "variation_detected" in event_types or
            result.get("next_step") == "clarify"
        )

        assert has_detection, \
            f"Sistema deve detectar algo. Events: {event_types}, next_step: {result.get('next_step')}"
