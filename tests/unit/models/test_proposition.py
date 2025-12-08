"""
Testes unitários para Proposicao e ProposicaoRef.

Testa:
- Criação e validação do modelo
- Métodos is_evaluated(), is_solid(), is_fragile()
- Serialização JSON
- Factory methods

Épico 11.1: Schema Unificado (Camada Modelo)
Data: 2025-12-08
"""

import pytest
from uuid import uuid4
from agents.models.proposition import Proposicao, ProposicaoRef


# =============================================================================
# TESTES DE CRIAÇÃO DO MODELO
# =============================================================================

class TestProposicaoCreation:
    """Testes de criação e validação da Proposicao."""

    def test_create_minimal_proposicao(self):
        """Proposição mínima (apenas texto) é válida."""
        prop = Proposicao(texto="Equipes usam LLMs para desenvolvimento")
        assert prop.texto == "Equipes usam LLMs para desenvolvimento"
        assert prop.solidez is None
        assert prop.evidencias == []
        assert prop.id is not None  # UUID gerado automaticamente

    def test_create_full_proposicao(self):
        """Proposição completa é criada corretamente."""
        prop = Proposicao(
            id="prop-123",
            texto="Linguagem permite transmitir ficções",
            solidez=0.85,
            evidencias=["evid-1", "evid-2"]
        )
        assert prop.id == "prop-123"
        assert prop.texto == "Linguagem permite transmitir ficções"
        assert prop.solidez == 0.85
        assert len(prop.evidencias) == 2

    def test_create_proposicao_with_zero_solidez(self):
        """Proposição com solidez zero é válida."""
        prop = Proposicao(texto="Hipótese refutada", solidez=0.0)
        assert prop.solidez == 0.0
        assert prop.is_evaluated() is True

    def test_id_is_auto_generated(self):
        """IDs são gerados automaticamente e únicos."""
        prop1 = Proposicao(texto="Teste 1")
        prop2 = Proposicao(texto="Teste 2")
        assert prop1.id != prop2.id
        assert len(prop1.id) > 10  # UUID tem formato longo

    def test_texto_cannot_be_empty(self):
        """Texto vazio deve falhar na validação."""
        with pytest.raises(ValueError):
            Proposicao(texto="")


# =============================================================================
# TESTES DE VALIDAÇÃO DE SOLIDEZ
# =============================================================================

class TestSolidezValidation:
    """Testes de validação do campo solidez."""

    def test_solidez_none_is_valid(self):
        """Solidez None (não avaliada) é válido."""
        prop = Proposicao(texto="Não avaliada")
        assert prop.solidez is None

    def test_solidez_in_range_is_valid(self):
        """Solidez entre 0 e 1 é válido."""
        for solidez in [0.0, 0.25, 0.5, 0.75, 1.0]:
            prop = Proposicao(texto="Teste", solidez=solidez)
            assert prop.solidez == solidez

    def test_solidez_above_one_fails(self):
        """Solidez > 1 deve falhar."""
        with pytest.raises(ValueError):
            Proposicao(texto="Teste", solidez=1.5)

    def test_solidez_negative_fails(self):
        """Solidez negativa deve falhar."""
        with pytest.raises(ValueError):
            Proposicao(texto="Teste", solidez=-0.1)


# =============================================================================
# TESTES DE is_evaluated()
# =============================================================================

class TestIsEvaluated:
    """Testes para o método is_evaluated()."""

    def test_none_solidez_is_not_evaluated(self):
        """Solidez None = não avaliada."""
        prop = Proposicao(texto="Teste")
        assert prop.is_evaluated() is False

    def test_zero_solidez_is_evaluated(self):
        """Solidez 0 = avaliada (proposição refutada)."""
        prop = Proposicao(texto="Teste", solidez=0.0)
        assert prop.is_evaluated() is True

    def test_positive_solidez_is_evaluated(self):
        """Solidez positiva = avaliada."""
        prop = Proposicao(texto="Teste", solidez=0.85)
        assert prop.is_evaluated() is True


# =============================================================================
# TESTES DE is_solid()
# =============================================================================

class TestIsSolid:
    """Testes para o método is_solid()."""

    def test_none_solidez_is_not_solid(self):
        """Proposição não avaliada não é sólida."""
        prop = Proposicao(texto="Teste")
        assert prop.is_solid() is False

    def test_high_solidez_is_solid(self):
        """Solidez alta (>= 0.6) é sólida."""
        prop = Proposicao(texto="Teste", solidez=0.85)
        assert prop.is_solid() is True

    def test_exactly_threshold_is_solid(self):
        """Solidez exatamente no threshold é sólida."""
        prop = Proposicao(texto="Teste", solidez=0.6)
        assert prop.is_solid() is True

    def test_below_threshold_is_not_solid(self):
        """Solidez abaixo do threshold não é sólida."""
        prop = Proposicao(texto="Teste", solidez=0.59)
        assert prop.is_solid() is False

    def test_custom_threshold(self):
        """Threshold customizado funciona."""
        prop = Proposicao(texto="Teste", solidez=0.8)
        assert prop.is_solid(threshold=0.9) is False
        assert prop.is_solid(threshold=0.7) is True


# =============================================================================
# TESTES DE is_fragile()
# =============================================================================

class TestIsFragile:
    """Testes para o método is_fragile()."""

    def test_none_solidez_is_not_fragile(self):
        """Proposição não avaliada não é frágil (ainda não sabemos)."""
        prop = Proposicao(texto="Teste")
        assert prop.is_fragile() is False

    def test_low_solidez_is_fragile(self):
        """Solidez baixa (< 0.4) é frágil."""
        prop = Proposicao(texto="Teste", solidez=0.2)
        assert prop.is_fragile() is True

    def test_exactly_threshold_is_not_fragile(self):
        """Solidez exatamente no threshold não é frágil."""
        prop = Proposicao(texto="Teste", solidez=0.4)
        assert prop.is_fragile() is False

    def test_above_threshold_is_not_fragile(self):
        """Solidez acima do threshold não é frágil."""
        prop = Proposicao(texto="Teste", solidez=0.5)
        assert prop.is_fragile() is False

    def test_custom_threshold(self):
        """Threshold customizado funciona."""
        prop = Proposicao(texto="Teste", solidez=0.45)
        assert prop.is_fragile(threshold=0.4) is False
        assert prop.is_fragile(threshold=0.5) is True


# =============================================================================
# TESTES DE SERIALIZAÇÃO
# =============================================================================

class TestSerialization:
    """Testes de serialização para JSON."""

    def test_to_dict_minimal(self):
        """Serializa proposição mínima para dict."""
        prop = Proposicao(id="test-id", texto="Teste")
        data = prop.to_dict()

        assert data["id"] == "test-id"
        assert data["texto"] == "Teste"
        assert data["solidez"] is None
        assert data["evidencias"] == []

    def test_to_dict_full(self):
        """Serializa proposição completa para dict."""
        prop = Proposicao(
            id="prop-123",
            texto="Linguagem permite transmitir ficções",
            solidez=0.85,
            evidencias=["evid-1", "evid-2"]
        )
        data = prop.to_dict()

        assert data["id"] == "prop-123"
        assert data["texto"] == "Linguagem permite transmitir ficções"
        assert data["solidez"] == 0.85
        assert data["evidencias"] == ["evid-1", "evid-2"]

    def test_from_dict(self):
        """Deserializa dict para proposição."""
        data = {
            "id": "prop-456",
            "texto": "Mitos permitem cooperação",
            "solidez": 0.75,
            "evidencias": []
        }
        prop = Proposicao.from_dict(data)

        assert prop.id == "prop-456"
        assert prop.texto == "Mitos permitem cooperação"
        assert prop.solidez == 0.75

    def test_round_trip(self):
        """Serializar e deserializar mantém dados."""
        original = Proposicao(
            id="test-roundtrip",
            texto="Teste de ida e volta",
            solidez=0.9,
            evidencias=["e1", "e2", "e3"]
        )
        data = original.to_dict()
        restored = Proposicao.from_dict(data)

        assert restored.id == original.id
        assert restored.texto == original.texto
        assert restored.solidez == original.solidez
        assert restored.evidencias == original.evidencias


# =============================================================================
# TESTES DE FACTORY METHODS
# =============================================================================

class TestFactoryMethods:
    """Testes para métodos de criação alternativos."""

    def test_from_text_minimal(self):
        """Cria proposição apenas com texto."""
        prop = Proposicao.from_text("Equipes existem")
        assert prop.texto == "Equipes existem"
        assert prop.solidez is None
        assert prop.id is not None

    def test_from_text_with_solidez(self):
        """Cria proposição com texto e solidez."""
        prop = Proposicao.from_text("Tempo é mensurável", solidez=0.9)
        assert prop.texto == "Tempo é mensurável"
        assert prop.solidez == 0.9


# =============================================================================
# TESTES DE ProposicaoRef
# =============================================================================

class TestProposicaoRef:
    """Testes para ProposicaoRef (referências)."""

    def test_create_minimal_ref(self):
        """Referência mínima (apenas ID) é válida."""
        ref = ProposicaoRef(id="prop-123")
        assert ref.id == "prop-123"
        assert ref.texto is None
        assert ref.solidez is None

    def test_create_full_ref(self):
        """Referência completa com caches."""
        ref = ProposicaoRef(
            id="prop-123",
            texto="Cache do texto",
            solidez=0.8
        )
        assert ref.id == "prop-123"
        assert ref.texto == "Cache do texto"
        assert ref.solidez == 0.8

    def test_from_proposicao(self):
        """Cria referência a partir de proposição."""
        prop = Proposicao(
            id="prop-original",
            texto="Texto original",
            solidez=0.95
        )
        ref = ProposicaoRef.from_proposicao(prop)

        assert ref.id == "prop-original"
        assert ref.texto == "Texto original"
        assert ref.solidez == 0.95


# =============================================================================
# TESTES DE CENÁRIOS DE USO
# =============================================================================

class TestUsageScenarios:
    """Testes de cenários reais de uso."""

    def test_migration_from_premise_string(self):
        """Cenário: Migrar premise (string) para proposição."""
        premise_text = "Equipes Python de 2-5 devs existem"
        prop = Proposicao.from_text(premise_text)

        assert prop.texto == premise_text
        assert prop.solidez is None  # Não avaliada inicialmente
        assert prop.is_evaluated() is False

    def test_migration_from_assumption_string(self):
        """Cenário: Migrar assumption (string) para proposição."""
        assumption_text = "Qualidade não é comprometida"
        prop = Proposicao.from_text(assumption_text)

        assert prop.texto == assumption_text
        assert prop.solidez is None  # Não avaliada inicialmente

    def test_evaluate_proposicao(self):
        """Cenário: Avaliar proposição (de None para valor)."""
        prop = Proposicao(texto="Hipótese inicial")
        assert prop.is_evaluated() is False

        # Simula avaliação pelo Observador/Orquestrador
        prop.solidez = 0.7
        assert prop.is_evaluated() is True
        assert prop.is_solid() is True

    def test_multiple_proposicoes_from_lists(self):
        """Cenário: Converter listas de premises + assumptions."""
        premises = ["Equipes usam Claude Code", "Tempo é mensurável"]
        assumptions = ["Qualidade mantida", "Resultado generalizável"]

        proposicoes = []
        for texto in premises:
            proposicoes.append(Proposicao.from_text(texto))
        for texto in assumptions:
            proposicoes.append(Proposicao.from_text(texto))

        assert len(proposicoes) == 4
        assert all(p.solidez is None for p in proposicoes)
        assert all(p.is_evaluated() is False for p in proposicoes)

    def test_solidez_evolution(self):
        """Cenário: Solidez evolui durante conversa."""
        prop = Proposicao(texto="Claude Code reduz tempo de sprint")

        # Início: não avaliada
        assert prop.solidez is None
        assert not prop.is_solid()
        assert not prop.is_fragile()

        # Após primeira avaliação: incerto
        prop.solidez = 0.5
        assert prop.is_evaluated()
        assert not prop.is_solid()
        assert not prop.is_fragile()

        # Após encontrar evidências: sólida
        prop.solidez = 0.85
        prop.evidencias.append("estudo-1")
        assert prop.is_solid()
        assert not prop.is_fragile()
