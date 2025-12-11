"""
Testes unitários para CognitiveModel.

Testa:
- Criação e validação do modelo
- Método is_mature()
- Método calculate_solidez()

Épico 11.3: Migração para proposicoes unificadas

"""

import pytest
from pydantic import ValidationError
from core.agents.models.cognitive_model import CognitiveModel, Contradiction, SolidGround
from core.agents.models.proposition import Proposicao

# =============================================================================
# TESTES DE CRIAÇÃO DO MODELO
# =============================================================================

class TestCognitiveModelCreation:
    """Testes de criação e validação do CognitiveModel."""

    def test_cognitive_model_creation_and_validation(self):
        """
        Testa criação de CognitiveModel (vazio e completo) e validações customizadas.
        
        Consolidates:
        - test_create_empty_model: Valida defaults
        - test_create_full_model: Valida criação completa
        - Adds: Testa validação de contradictions (confidence >= 0.80)
        """
        # Test 1: Empty model (defaults)
        empty_model = CognitiveModel()
        assert empty_model.claim == ""
        assert empty_model.proposicoes == []
        assert empty_model.contradictions == []
        assert empty_model.open_questions == []
        assert empty_model.solid_grounds == []
        assert empty_model.context == {}
        
        # Test 2: Full model (all fields)
        prop1 = Proposicao(texto="Proposição 1", solidez=0.8)
        prop2 = Proposicao(texto="Proposição 2", solidez=0.6)
        
        full_model = CognitiveModel(
            claim="Claim principal",
            proposicoes=[prop1, prop2],
            open_questions=["Questão 1", "Questão 2"],
            contradictions=[],
            solid_grounds=[],
            context={"domain": "software"}
        )
        assert full_model.claim == "Claim principal"
        assert len(full_model.proposicoes) == 2
        assert full_model.proposicoes[0].texto == "Proposição 1"
        assert len(full_model.open_questions) == 2
        
        # Test 3: Contradiction validation (custom @field_validator)
        # Valid contradiction (confidence >= 0.80)
        valid_contradiction = Contradiction(
            description="Tensão entre Claim A e Claim B",
            confidence=0.85,
        )
        model_with_valid_contradiction = CognitiveModel(
            claim="Test",
            contradictions=[valid_contradiction]
        )
        assert len(model_with_valid_contradiction.contradictions) == 1
        
        # Invalid contradiction (confidence < 0.80) should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            invalid_contradiction = Contradiction(
                description="Contradição fraca",
                confidence=0.75,  # Below threshold
            )
            CognitiveModel(
                claim="Test",
                contradictions=[invalid_contradiction]
            )
        
        # Verify error message mentions confidence threshold
        assert "confidence" in str(exc_info.value).lower() or "0.80" in str(exc_info.value)

    def test_create_model_with_proposicoes_from_dict(self):
        """Modelo pode ser criado com proposicoes em formato dict."""
        model = CognitiveModel(
            claim="Teste",
            proposicoes=[
                {"texto": "Prop 1", "solidez": 0.8},
                {"texto": "Prop 2", "solidez": 0.6},
            ]
        )
        assert len(model.proposicoes) == 2
        assert isinstance(model.proposicoes[0], Proposicao)

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
            proposicoes=[
                Proposicao(texto="Premissa 1", solidez=0.8),
                Proposicao(texto="Premissa 2", solidez=0.7),
            ],
            open_questions=[],
            contradictions=[],
        )
        assert model.is_mature() is True

    def test_low_solidez_is_not_mature(self):
        """Solidez média baixa = não maduro."""
        model = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min",
            proposicoes=[
                Proposicao(texto="Prop 1", solidez=0.3),
                Proposicao(texto="Prop 2", solidez=0.4),
            ],
            open_questions=[],
            contradictions=[]
        )
        assert model.is_mature() is False  # Média 0.35 < 0.6

    def test_few_propositions_is_not_mature(self):
        """Poucas proposições = não maduro."""
        model = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min",
            proposicoes=[
                Proposicao(texto="Prop 1", solidez=0.9),
            ],
            open_questions=[],
            contradictions=[]
        )
        assert model.is_mature() is False  # < 2 proposições

# =============================================================================
# TESTES DE calculate_solidez()
# =============================================================================

class TestCalculateSolidez:
    """Testes para o método calculate_solidez()."""

    def test_empty_model_has_low_solidez(self):
        """Modelo vazio tem solidez baixa."""
        model = CognitiveModel()
        solidez = model.calculate_solidez()
        # 0 claim + 0 proposições + 20 questions + 15 contradictions = 35
        assert solidez == 35.0

    def test_complete_model_has_high_solidez(self):
        """Modelo completo com proposições sólidas tem solidez alta."""
        model = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min em equipes Python",
            proposicoes=[
                Proposicao(texto="Prop 1", solidez=1.0),
                Proposicao(texto="Prop 2", solidez=1.0),
                Proposicao(texto="Prop 3", solidez=1.0),
            ],
            open_questions=[],
            contradictions=[],
        )
        solidez = model.calculate_solidez()
        # 20 (claim) + 30 (solidez média 1.0) + 15 (3 props) + 20 (0 questions) + 15 (0 contradictions) = 100
        assert solidez == 100.0

    def test_claim_length_affects_solidez(self):
        """Tamanho do claim afeta solidez."""
        short = CognitiveModel(claim="LLMs são bons")
        medium = CognitiveModel(claim="LLMs aumentam produtividade em equipes")
        long = CognitiveModel(claim="Claude Code reduz tempo de sprint de 2h para 30min em equipes Python de 2-5 desenvolvedores")

        assert short.calculate_solidez() < medium.calculate_solidez()
        assert medium.calculate_solidez() < long.calculate_solidez()

    def test_proposicoes_solidez_affects_score(self):
        """Solidez das proposições afeta score."""
        low = CognitiveModel(
            claim="X" * 60,
            proposicoes=[Proposicao(texto="P1", solidez=0.3)]
        )
        high = CognitiveModel(
            claim="X" * 60,
            proposicoes=[Proposicao(texto="P1", solidez=0.9)]
        )

        assert low.calculate_solidez() < high.calculate_solidez()

    def test_proposicoes_count_affects_score(self):
        """Quantidade de proposições afeta score."""
        one = CognitiveModel(
            claim="X" * 60,
            proposicoes=[Proposicao(texto="P1", solidez=0.8)]
        )
        three = CognitiveModel(
            claim="X" * 60,
            proposicoes=[
                Proposicao(texto="P1", solidez=0.8),
                Proposicao(texto="P2", solidez=0.8),
                Proposicao(texto="P3", solidez=0.8),
            ]
        )

        assert one.calculate_solidez() < three.calculate_solidez()

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
            claim="X" * 100,
            proposicoes=[
                Proposicao(texto="P1", solidez=1.0),
                Proposicao(texto="P2", solidez=1.0),
                Proposicao(texto="P3", solidez=1.0),
            ],
            open_questions=[],
            contradictions=[],
            solid_grounds=[
                SolidGround(claim="C1", evidence="E1", source="S1"),
                SolidGround(claim="C2", evidence="E2", source="S2"),
                SolidGround(claim="C3", evidence="E3", source="S3"),
                SolidGround(claim="C4", evidence="E4", source="S4")
            ]
        )
        assert model.calculate_solidez() == 100.0

    def test_realistic_evolution_scenario(self):
        """Cenário realista: solidez evolui durante conversa."""
        # Turno 1: Ideia vaga
        turno1 = CognitiveModel(
            claim="LLMs aumentam produtividade",
            proposicoes=[
                Proposicao(texto="Produtividade é mensurável", solidez=0.3),
            ],
            open_questions=["Como medir?", "Qual população?"]
        )

        # Turno 3: Mais estruturado
        turno3 = CognitiveModel(
            claim="Claude Code reduz tempo de sprint em equipes Python",
            proposicoes=[
                Proposicao(texto="Equipes usam Claude Code", solidez=0.7),
                Proposicao(texto="Qualidade mantida", solidez=0.5),
            ],
            open_questions=["Tamanho ideal de equipe?"]
        )

        # Turno 5: Quase maduro
        turno5 = CognitiveModel(
            claim="Claude Code reduz tempo de sprint de 2h para 30min em equipes Python de 2-5 devs",
            proposicoes=[
                Proposicao(texto="Equipes usam Claude Code", solidez=0.9),
                Proposicao(texto="Tempo é métrica válida", solidez=0.85),
            ],
            open_questions=[]
        )

        # Solidez deve aumentar ao longo dos turnos
        assert turno1.calculate_solidez() < turno3.calculate_solidez()
        assert turno3.calculate_solidez() < turno5.calculate_solidez()

# =============================================================================
# TESTES DE MÉTODOS AUXILIARES
# =============================================================================

class TestHelperMethods:
    """Testes para métodos auxiliares do CognitiveModel."""

    def test_get_solid_propositions(self):
        """Filtra proposições sólidas."""
        model = CognitiveModel(
            claim="Teste",
            proposicoes=[
                Proposicao(texto="Sólida 1", solidez=0.9),
                Proposicao(texto="Frágil 1", solidez=0.3),
                Proposicao(texto="Sólida 2", solidez=0.7),
            ]
        )
        solid = model.get_solid_propositions()
        assert len(solid) == 2
        assert all(p.solidez >= 0.6 for p in solid)

    def test_get_fragile_propositions(self):
        """Filtra proposições frágeis."""
        model = CognitiveModel(
            claim="Teste",
            proposicoes=[
                Proposicao(texto="Sólida 1", solidez=0.9),
                Proposicao(texto="Frágil 1", solidez=0.3),
                Proposicao(texto="Frágil 2", solidez=0.2),
            ]
        )
        fragile = model.get_fragile_propositions()
        assert len(fragile) == 2
        assert all(p.solidez < 0.4 for p in fragile)

    def test_to_dict_and_from_dict(self):
        """Serialização e deserialização funcionam."""
        original = CognitiveModel(
            claim="Teste de serialização",
            proposicoes=[
                Proposicao(texto="Prop 1", solidez=0.8),
            ],
            open_questions=["Q1"],
            context={"domain": "test"}
        )

        data = original.to_dict()
        restored = CognitiveModel.from_dict(data)

        assert restored.claim == original.claim
        assert len(restored.proposicoes) == 1
        assert restored.proposicoes[0].texto == "Prop 1"
