"""
Testes unitários para CognitiveModel.

Testa:
- Criação e validação do modelo
- Método is_mature()
- Método calculate_solidez() (Épico 9.4)

Data: 05/12/2025
"""

import pytest
from agents.models.cognitive_model import CognitiveModel, Contradiction, SolidGround


# =============================================================================
# TESTES DE CRIAÇÃO DO MODELO
# =============================================================================

class TestCognitiveModelCreation:
    """Testes de criação e validação do CognitiveModel."""

    def test_create_empty_model(self):
        """Modelo vazio é válido."""
        model = CognitiveModel()
        assert model.claim == ""
        assert model.premises == []
        assert model.assumptions == []
        assert model.open_questions == []
        assert model.contradictions == []
        assert model.solid_grounds == []
        assert model.context == {}

    def test_create_full_model(self):
        """Modelo completo é criado corretamente."""
        model = CognitiveModel(
            claim="LLMs aumentam produtividade em 30%",
            premises=["Equipes usam LLMs", "Produtividade é mensurável"],
            assumptions=["Qualidade não é comprometida"],
            open_questions=["Como medir qualidade?"],
            contradictions=[],
            solid_grounds=[],
            context={"domain": "software"}
        )
        assert model.claim == "LLMs aumentam produtividade em 30%"
        assert len(model.premises) == 2
        assert len(model.assumptions) == 1


# =============================================================================
# TESTES DE is_mature()
# =============================================================================

class TestIsMature:
    """Testes para o método is_mature()."""

    def test_empty_model_is_not_mature(self):
        """Modelo vazio não é maduro."""
        model = CognitiveModel()
        assert model.is_mature() is False

    def test_complete_model_is_mature(self):
        """Modelo completo com critérios atendidos é maduro."""
        model = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min",
            premises=["Premissa 1", "Premissa 2"],
            assumptions=["Assumption 1"],
            open_questions=[],
            contradictions=[],
            solid_grounds=[]
        )
        assert model.is_mature() is True

    def test_too_many_assumptions_is_not_mature(self):
        """Muitas suposições = não maduro."""
        model = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min",
            premises=["Premissa 1", "Premissa 2"],
            assumptions=["A1", "A2", "A3"],  # > 2
            open_questions=[],
            contradictions=[]
        )
        assert model.is_mature() is False


# =============================================================================
# TESTES DE calculate_solidez() (Épico 9.4)
# =============================================================================

class TestCalculateSolidez:
    """Testes para o método calculate_solidez()."""

    def test_empty_model_has_low_solidez(self):
        """Modelo vazio tem solidez baixa (apenas pontos de ausência)."""
        model = CognitiveModel()
        solidez = model.calculate_solidez()
        # Pontos: 0 claim + 0 premises + 20 assumptions (0) + 20 questions (0) + 15 contradictions (0)
        assert solidez == 55.0

    def test_complete_model_has_high_solidez(self):
        """Modelo completo tem solidez alta."""
        model = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min em equipes Python",
            premises=["Premissa 1", "Premissa 2", "Premissa 3"],
            assumptions=[],
            open_questions=[],
            contradictions=[],
            solid_grounds=[]
        )
        solidez = model.calculate_solidez()
        # 20 (claim > 50) + 25 (3 premises) + 20 (0 assumptions) + 20 (0 questions) + 15 (0 contradictions)
        assert solidez == 100.0

    def test_claim_length_affects_solidez(self):
        """Tamanho do claim afeta solidez."""
        # Claim curto (< 20)
        short = CognitiveModel(claim="LLMs são bons")
        # Claim médio (20-50)
        medium = CognitiveModel(claim="LLMs aumentam produtividade em equipes")
        # Claim longo (> 50)
        long = CognitiveModel(claim="Claude Code reduz tempo de sprint de 2h para 30min em equipes Python de 2-5 desenvolvedores")

        assert short.calculate_solidez() < medium.calculate_solidez()
        assert medium.calculate_solidez() < long.calculate_solidez()

    def test_premises_affect_solidez(self):
        """Número de premises afeta solidez."""
        zero = CognitiveModel(claim="X" * 60)  # 20 pontos de claim
        one = CognitiveModel(claim="X" * 60, premises=["P1"])
        two = CognitiveModel(claim="X" * 60, premises=["P1", "P2"])
        three = CognitiveModel(claim="X" * 60, premises=["P1", "P2", "P3"])

        assert zero.calculate_solidez() < one.calculate_solidez()
        assert one.calculate_solidez() < two.calculate_solidez()
        assert two.calculate_solidez() < three.calculate_solidez()

    def test_assumptions_reduce_solidez(self):
        """Mais suposições = menor solidez."""
        none = CognitiveModel(claim="X" * 60, assumptions=[])
        one = CognitiveModel(claim="X" * 60, assumptions=["A1"])
        two = CognitiveModel(claim="X" * 60, assumptions=["A1", "A2"])
        many = CognitiveModel(claim="X" * 60, assumptions=["A1", "A2", "A3", "A4", "A5"])

        assert none.calculate_solidez() > one.calculate_solidez()
        assert one.calculate_solidez() > two.calculate_solidez()
        assert two.calculate_solidez() > many.calculate_solidez()

    def test_open_questions_reduce_solidez(self):
        """Mais questões abertas = menor solidez."""
        none = CognitiveModel(claim="X" * 60, open_questions=[])
        one = CognitiveModel(claim="X" * 60, open_questions=["Q1"])
        two = CognitiveModel(claim="X" * 60, open_questions=["Q1", "Q2"])

        assert none.calculate_solidez() > one.calculate_solidez()
        assert one.calculate_solidez() > two.calculate_solidez()

    def test_contradictions_reduce_solidez(self):
        """Contradições reduzem solidez."""
        none = CognitiveModel(claim="X" * 60, contradictions=[])
        one = CognitiveModel(
            claim="X" * 60,
            contradictions=[Contradiction(description="Tensão", confidence=0.85)]
        )

        assert none.calculate_solidez() > one.calculate_solidez()

    def test_solid_grounds_increase_solidez(self):
        """Evidências bibliográficas aumentam solidez (bonus)."""
        without = CognitiveModel(claim="X" * 60)
        with_one = CognitiveModel(
            claim="X" * 60,
            solid_grounds=[SolidGround(claim="C1", evidence="E1", source="S1")]
        )
        with_three = CognitiveModel(
            claim="X" * 60,
            solid_grounds=[
                SolidGround(claim="C1", evidence="E1", source="S1"),
                SolidGround(claim="C2", evidence="E2", source="S2"),
                SolidGround(claim="C3", evidence="E3", source="S3")
            ]
        )

        assert with_one.calculate_solidez() > without.calculate_solidez()
        assert with_three.calculate_solidez() > with_one.calculate_solidez()

    def test_solidez_capped_at_100(self):
        """Solidez máxima é 100."""
        model = CognitiveModel(
            claim="X" * 100,  # 20 pontos
            premises=["P1", "P2", "P3", "P4"],  # 25 pontos
            assumptions=[],  # 20 pontos
            open_questions=[],  # 20 pontos
            contradictions=[],  # 15 pontos
            solid_grounds=[  # 10 pontos bonus
                SolidGround(claim="C1", evidence="E1", source="S1"),
                SolidGround(claim="C2", evidence="E2", source="S2"),
                SolidGround(claim="C3", evidence="E3", source="S3"),
                SolidGround(claim="C4", evidence="E4", source="S4")
            ]
        )
        # Total seria 110, mas é capped em 100
        assert model.calculate_solidez() == 100.0

    def test_realistic_evolution_scenario(self):
        """Cenário realista: solidez evolui durante conversa."""
        # Turno 1: Ideia vaga
        turno1 = CognitiveModel(
            claim="LLMs aumentam produtividade",
            premises=[],
            assumptions=["Produtividade é mensurável"],
            open_questions=["Como medir?", "Qual população?"]
        )

        # Turno 3: Mais estruturado
        turno3 = CognitiveModel(
            claim="Claude Code reduz tempo de sprint em equipes Python",
            premises=["Equipes usam Claude Code"],
            assumptions=["Qualidade mantida"],
            open_questions=["Tamanho ideal de equipe?"]
        )

        # Turno 5: Quase maduro
        turno5 = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min em equipes Python de 2-5 devs",
            premises=["Equipes usam Claude Code", "Tempo é métrica válida"],
            assumptions=[],
            open_questions=[]
        )

        # Solidez deve aumentar ao longo dos turnos
        assert turno1.calculate_solidez() < turno3.calculate_solidez()
        assert turno3.calculate_solidez() < turno5.calculate_solidez()

        # Valores aproximados esperados
        assert turno1.calculate_solidez() < 50  # Vago
        assert turno3.calculate_solidez() > 45  # Intermediário
        assert turno5.calculate_solidez() > 70  # Estruturado
