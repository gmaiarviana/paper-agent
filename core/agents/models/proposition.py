"""
Schema Pydantic de Proposição.

Proposição é afirmação sobre o mundo que pode ser sustentada ou refutada
por evidências. É a unidade base de conhecimento no sistema.

Na ontologia do Paper Agent:
- Proposições substituem a distinção binária "premise" vs "assumption"
- Todas são proposições com diferentes graus de solidez (0-1)
- Solidez é derivada de evidências, não definida manualmente
- Proposições podem ser reutilizadas como fundamentos em múltiplos argumentos

Ver core/docs/architecture/data-models/ontology.md para ontologia completa.
Ver docs/vision/epistemology.md para base filosófica.

Épico 11.1: Schema Unificado (Camada Modelo)

"""

from typing import Optional, List
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict

class Proposicao(BaseModel):
    """
    Afirmação sobre o mundo com solidez derivada de evidências.

    Proposição é a unidade base de conhecimento no sistema. Substitui a
    distinção binária entre "premise" (verdadeiro) e "assumption" (hipótese).
    Agora todas são proposições com diferentes graus de solidez.

    Attributes:
        id: UUID único da proposição
        texto: Enunciado da proposição (ex: "Linguagem permite transmitir ficções")
        solidez: Grau de sustentação (0-1). None = não avaliada pelo sistema
        evidencias: Lista de IDs de evidências (inicialmente vazia)

    Solidez inicial:
        - Proposições nascem com solidez=None (não avaliada)
        - Observador ou Orquestrador avaliam via LLM e atualizam para valor numérico
        - Pesquisador (futuro) adiciona evidências que recalculam solidez
        - Cálculos de maturidade ignoram proposições com solidez=None

    Example:
        >>> prop = Proposicao(texto="Equipes Python de 2-5 devs existem")
        >>> prop.solidez is None
        True
        >>> prop.is_evaluated()
        False
        >>> prop.solidez = 0.85
        >>> prop.is_solid()
        True

    Ver core/docs/architecture/data-models/ontology.md para definição filosófica completa.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="UUID único da proposição"
    )

    texto: str = Field(
        ...,
        description="Enunciado da proposição (afirmação sobre o mundo)",
        min_length=1
    )

    solidez: Optional[float] = Field(
        default=None,
        description="Grau de sustentação (0-1). None = não avaliada. "
                    "Derivado de evidências, não definido manualmente.",
        ge=0.0,
        le=1.0
    )

    evidencias: List[str] = Field(
        default_factory=list,
        description="IDs de evidências que apoiam/refutam esta proposição. "
                    "Inicialmente vazio. Preenchido pelo Pesquisador (Épico 14)."
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "id": "prop-550e8400-e29b-41d4-a716-446655440000",
                "texto": "Equipes Python de 2-5 devs existem",
                "solidez": 0.85,
                "evidencias": []
            }
        }
    )

    def is_evaluated(self) -> bool:
        """
        Verifica se proposição foi avaliada pelo sistema.

        Returns:
            bool: True se solidez foi definida (não é None)

        Example:
            >>> prop = Proposicao(texto="Teste")
            >>> prop.is_evaluated()
            False
            >>> prop.solidez = 0.7
            >>> prop.is_evaluated()
            True
        """
        return self.solidez is not None

    def is_solid(self, threshold: float = 0.6) -> bool:
        """
        Verifica se proposição tem solidez suficiente.

        Args:
            threshold: Limite mínimo de solidez (padrão: 0.6)

        Returns:
            bool: True se solidez >= threshold. False se não avaliada.

        Example:
            >>> prop = Proposicao(texto="Teste", solidez=0.85)
            >>> prop.is_solid()
            True
            >>> prop.is_solid(threshold=0.9)
            False
        """
        if not self.is_evaluated():
            return False
        return self.solidez >= threshold  # type: ignore

    def is_fragile(self, threshold: float = 0.4) -> bool:
        """
        Verifica se proposição tem solidez baixa (frágil).

        Args:
            threshold: Limite máximo para ser considerada frágil (padrão: 0.4)

        Returns:
            bool: True se solidez < threshold. False se não avaliada.

        Example:
            >>> prop = Proposicao(texto="Teste", solidez=0.3)
            >>> prop.is_fragile()
            True
            >>> prop = Proposicao(texto="Teste", solidez=0.5)
            >>> prop.is_fragile()
            False
        """
        if not self.is_evaluated():
            return False
        return self.solidez < threshold  # type: ignore

    def to_dict(self) -> dict:
        """
        Serializa proposição para dict (útil para persistência JSON).

        Returns:
            dict: Representação em dict da proposição
        """
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "Proposicao":
        """
        Cria instância a partir de dict.

        Args:
            data: Dict com campos da proposição

        Returns:
            Proposicao: Instância validada
        """
        return cls(**data)

    @classmethod
    def from_text(cls, texto: str, solidez: Optional[float] = None) -> "Proposicao":
        """
        Cria proposição a partir de texto simples.

        Útil para migração de premises/assumptions (strings) para proposições.

        Args:
            texto: Enunciado da proposição
            solidez: Solidez inicial (padrão: None = não avaliada)

        Returns:
            Proposicao: Nova instância com ID gerado automaticamente

        Example:
            >>> prop = Proposicao.from_text("Equipes usam LLMs")
            >>> prop.texto
            'Equipes usam LLMs'
            >>> prop.solidez is None
            True
        """
        return cls(texto=texto, solidez=solidez)

class ProposicaoRef(BaseModel):
    """
    Referência a uma Proposição (para relações N:N).

    Usado quando um Argumento referencia proposições como fundamentos,
    evitando circular imports e permitindo cache de dados frequentes.

    Attributes:
        id: ID da proposição referenciada
        texto: Cache do texto (opcional, para performance em listagens)
        solidez: Cache da solidez (opcional, para exibição rápida)

    Example:
        >>> ref = ProposicaoRef(id="prop-123", texto="Equipes existem", solidez=0.85)
        >>> ref.id
        'prop-123'
    """

    id: str = Field(
        ...,
        description="ID da proposição referenciada"
    )

    texto: Optional[str] = Field(
        default=None,
        description="Cache do texto da proposição (opcional, para performance)"
    )

    solidez: Optional[float] = Field(
        default=None,
        description="Cache da solidez (opcional, para exibição rápida)",
        ge=0.0,
        le=1.0
    )

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def from_proposicao(cls, prop: Proposicao) -> "ProposicaoRef":
        """
        Cria referência a partir de uma Proposicao completa.

        Args:
            prop: Proposição completa

        Returns:
            ProposicaoRef: Referência com caches preenchidos
        """
        return cls(
            id=prop.id,
            texto=prop.texto,
            solidez=prop.solidez
        )
