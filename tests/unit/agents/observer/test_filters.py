"""
Testes unitarios para filtros de regras de negocio do Observer.

Este modulo testa a arquitetura de duas camadas:
- Camada 1: Observer (analise contextual via LLM) - mockada nos testes
- Camada 2: Filtros (regras de negocio deterministicas) - testadas aqui

Os filtros garantem previsibilidade em cenarios especificos:
- Cold start: turno 1 nunca gera checkpoint
- Alta clareza: score >= 4 nao gera checkpoint
- Variacao simples: classification="variation" nao gera checkpoint
- Cooldown: respeita intervalo minimo entre checkpoints

Epico 13.6: Arquitetura de Duas Camadas
Data: 2025-12-10
"""

import pytest
from agents.observer.filters import (
    apply_business_rules,
    should_checkpoint,
    FilterType,
    FilterResult,
    get_filter_config,
    update_filter_config,
    MIN_TURN_FOR_CHECKPOINT,
    MIN_CLARITY_SCORE_FOR_EXEMPTION,
    MIN_TURNS_BETWEEN_CHECKPOINTS,
)


class TestApplyBusinessRules:
    """Testes para apply_business_rules()."""

    def test_no_checkpoint_when_observer_says_no(self):
        """Se Observer nao pede checkpoint, filtro nao muda nada."""
        observer_result = {
            "needs_checkpoint": False,
            "clarity_score": 2,
            "clarity_level": "nebulosa"
        }

        result = apply_business_rules(
            observer_result=observer_result,
            turn_number=5
        )

        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.NONE
        assert result.original_needs_checkpoint is False

    def test_cold_start_exemption_turn_1(self):
        """Turno 1 nunca gera checkpoint (cold start)."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 1,
            "clarity_level": "confusa"
        }

        result = apply_business_rules(
            observer_result=observer_result,
            turn_number=1
        )

        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.COLD_START
        assert result.original_needs_checkpoint is True
        assert "cold start" in result.reason.lower()

    def test_high_clarity_exemption(self):
        """Clareza alta (score >= 4) nao gera checkpoint."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 4,
            "clarity_level": "clara"
        }

        result = apply_business_rules(
            observer_result=observer_result,
            turn_number=5
        )

        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.HIGH_CLARITY
        assert result.original_needs_checkpoint is True

    def test_variation_exemption(self):
        """Classificacao 'variation' nao gera checkpoint."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 2,
            "clarity_level": "nebulosa",
            "classification": "variation"
        }

        result = apply_business_rules(
            observer_result=observer_result,
            turn_number=5
        )

        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.VARIATION_ONLY
        assert result.original_needs_checkpoint is True

    def test_cooldown_exemption(self):
        """Respeita intervalo minimo entre checkpoints."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 2,
            "clarity_level": "nebulosa",
            "classification": "real_change"
        }

        # Ultimo checkpoint foi ha 1 turno (menos que MIN_TURNS_BETWEEN_CHECKPOINTS)
        result = apply_business_rules(
            observer_result=observer_result,
            turn_number=5,
            turns_since_last_checkpoint=1
        )

        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.COOLDOWN
        assert result.original_needs_checkpoint is True

    def test_checkpoint_confirmed_when_no_exemption(self):
        """Checkpoint confirmado quando nenhum filtro se aplica."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 2,
            "clarity_level": "nebulosa",
            "classification": "real_change"
        }

        result = apply_business_rules(
            observer_result=observer_result,
            turn_number=5,
            turns_since_last_checkpoint=10
        )

        assert result.needs_checkpoint is True
        assert result.filter_applied == FilterType.NONE
        assert result.original_needs_checkpoint is True

    def test_filter_priority_cold_start_first(self):
        """Cold start tem prioridade sobre outros filtros."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 4,  # Seria HIGH_CLARITY
            "clarity_level": "clara",
            "classification": "variation"  # Seria VARIATION_ONLY
        }

        result = apply_business_rules(
            observer_result=observer_result,
            turn_number=1  # Cold start
        )

        # Cold start deve ter prioridade
        assert result.filter_applied == FilterType.COLD_START


class TestShouldCheckpoint:
    """Testes para should_checkpoint() - funcao de conveniencia."""

    def test_combines_clarity_and_variation(self):
        """Combina clarity_evaluation e variation_analysis."""
        clarity = {
            "needs_checkpoint": False,
            "clarity_score": 3,
            "clarity_level": "nebulosa"
        }
        variation = {
            "classification": "real_change"
        }

        result = should_checkpoint(
            clarity_evaluation=clarity,
            variation_analysis=variation,
            turn_number=5
        )

        # real_change deve triggerar checkpoint (mas pode ser filtrado)
        assert result.original_needs_checkpoint is True

    def test_variation_without_clarity(self):
        """Funciona apenas com variation_analysis."""
        variation = {
            "classification": "variation"
        }

        result = should_checkpoint(
            clarity_evaluation=None,
            variation_analysis=variation,
            turn_number=5
        )

        # Variation simples nao deve gerar checkpoint
        assert result.needs_checkpoint is False

    def test_clarity_without_variation(self):
        """Funciona apenas com clarity_evaluation."""
        clarity = {
            "needs_checkpoint": True,
            "clarity_score": 2,
            "clarity_level": "nebulosa"
        }

        result = should_checkpoint(
            clarity_evaluation=clarity,
            variation_analysis=None,
            turn_number=5,
            turns_since_last_checkpoint=10
        )

        # Clareza baixa deve gerar checkpoint
        assert result.needs_checkpoint is True


class TestFilterResult:
    """Testes para FilterResult dataclass."""

    def test_to_dict(self):
        """to_dict() retorna dict correto."""
        result = FilterResult(
            needs_checkpoint=False,
            filter_applied=FilterType.COLD_START,
            original_needs_checkpoint=True,
            reason="Turno 1 em cold start"
        )

        d = result.to_dict()

        assert d["needs_checkpoint"] is False
        assert d["filter_applied"] == "cold_start_exemption"
        assert d["original_needs_checkpoint"] is True
        assert d["was_filtered"] is True

    def test_was_filtered_false(self):
        """was_filtered e False quando nao houve mudanca."""
        result = FilterResult(
            needs_checkpoint=True,
            filter_applied=FilterType.NONE,
            original_needs_checkpoint=True,
            reason="Checkpoint necessario"
        )

        d = result.to_dict()
        assert d["was_filtered"] is False


class TestFilterConfig:
    """Testes para configuracao dinamica dos filtros."""

    def test_get_filter_config(self):
        """get_filter_config() retorna valores atuais."""
        config = get_filter_config()

        assert "min_turn_for_checkpoint" in config
        assert "min_clarity_score_for_exemption" in config
        assert "min_turns_between_checkpoints" in config

    def test_update_filter_config(self):
        """update_filter_config() atualiza valores."""
        # Salvar valores originais
        original = get_filter_config()

        try:
            # Atualizar
            new_config = update_filter_config(
                min_turn=5,
                min_clarity=3,
                min_cooldown=5
            )

            assert new_config["min_turn_for_checkpoint"] == 5
            assert new_config["min_clarity_score_for_exemption"] == 3
            assert new_config["min_turns_between_checkpoints"] == 5

        finally:
            # Restaurar valores originais
            update_filter_config(
                min_turn=original["min_turn_for_checkpoint"],
                min_clarity=original["min_clarity_score_for_exemption"],
                min_cooldown=original["min_turns_between_checkpoints"]
            )


class TestScenariosCenarioA:
    """
    Cenario A: Variacao Simples
    Input 1: "LLMs aumentam produtividade de desenvolvedores"
    Input 2: "LLMs aumentam produtividade de desenvolvedores em 30%"
    Esperado: NAO deve interromper (variation)
    """

    def test_scenario_a_turn_1(self):
        """Turno 1 nao gera checkpoint (cold start)."""
        observer_result = {
            "needs_checkpoint": True,  # Observer pode pedir
            "clarity_score": 3,
            "clarity_level": "nebulosa",
            "classification": "variation"
        }

        result = apply_business_rules(observer_result, turn_number=1)
        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.COLD_START

    def test_scenario_a_turn_2(self):
        """Turno 2 com variation nao gera checkpoint."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 3,
            "clarity_level": "nebulosa",
            "classification": "variation"
        }

        result = apply_business_rules(observer_result, turn_number=2)
        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.VARIATION_ONLY


class TestScenariosCenarioB:
    """
    Cenario B: Mudanca Real
    Input 1: "LLMs aumentam produtividade de desenvolvedores"
    Input 2: "Quero falar sobre blockchain e criptomoedas"
    Esperado: DEVE sugerir checkpoint (real_change)
    """

    def test_scenario_b_turn_1(self):
        """Turno 1 nao gera checkpoint mesmo com mudanca (cold start)."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 2,
            "clarity_level": "confusa",
            "classification": "real_change"
        }

        result = apply_business_rules(observer_result, turn_number=1)
        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.COLD_START

    def test_scenario_b_turn_2_real_change(self):
        """Turno 2 com real_change DEVE gerar checkpoint."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 2,
            "clarity_level": "confusa",
            "classification": "real_change"
        }

        result = apply_business_rules(
            observer_result,
            turn_number=2,
            turns_since_last_checkpoint=999  # Sem cooldown
        )
        assert result.needs_checkpoint is True
        assert result.filter_applied == FilterType.NONE


class TestScenariosCenarioD:
    """
    Cenario D: Conversa Clara
    Input 1: "LLMs aumentam produtividade de desenvolvedores em 30%"
    Input 2: "Especificamente em equipes de 5-10 pessoas usando pair programming"
    Esperado: NAO deve gerar checkpoint (conversa clara)
    """

    def test_scenario_d_high_clarity(self):
        """Alta clareza nao gera checkpoint."""
        observer_result = {
            "needs_checkpoint": True,  # Observer pode ser conservador
            "clarity_score": 4,
            "clarity_level": "clara"
        }

        result = apply_business_rules(observer_result, turn_number=2)
        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.HIGH_CLARITY

    def test_scenario_d_variation_refinement(self):
        """Refinamento (variation) nao gera checkpoint."""
        observer_result = {
            "needs_checkpoint": True,
            "clarity_score": 3,
            "clarity_level": "nebulosa",
            "classification": "variation"
        }

        result = apply_business_rules(observer_result, turn_number=2)
        assert result.needs_checkpoint is False
        assert result.filter_applied == FilterType.VARIATION_ONLY
