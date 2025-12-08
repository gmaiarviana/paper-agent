"""
Schema Pydantic do Modelo Cognitivo.

Este módulo define a estrutura do modelo cognitivo que representa
a evolução do pensamento do usuário durante a conversa.

O modelo cognitivo é volátil (em memória) e captura:
- claim: O que o usuário está tentando dizer/defender
- proposicoes: Fundamentos do argumento (unifica premise/assumption)
- open_questions: O que não sabemos ainda
- contradictions: Tensões internas detectadas
- solid_grounds: Argumentos com base bibliográfica
- context: Domínio, tecnologia, população inferidos

Ver docs/vision/cognitive_model/core.md para detalhes completos.

Épico 11.1: Schema Explícito de CognitiveModel
Épico 11.3: Migração para proposicoes unificadas
Data: 2025-12-08
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .proposition import Proposicao


class Contradiction(BaseModel):
    """
    Tensão interna detectada no argumento.

    O Metodologista detecta contradictions quando há inconsistências lógicas
    entre claim e proposicoes. Apenas mencionadas quando confiança > 80%.
    """

    description: str = Field(
        ...,
        description="Descrição da contradição detectada",
        min_length=1
    )
    confidence: float = Field(
        ...,
        description="Confiança da detecção (0-1). Apenas mencionar se > 0.80",
        ge=0.0,
        le=1.0
    )
    suggested_resolution: Optional[str] = Field(
        default=None,
        description="Sugestão de como resolver a contradição"
    )

    model_config = ConfigDict(extra="forbid")


class SolidGround(BaseModel):
    """
    Argumento fundamentado com evidência bibliográfica.

    Preenchido pelo Pesquisador (futuro) após busca na literatura.
    Diferencia argumento de opinião vs. argumento fundamentado.
    """

    claim: str = Field(
        ...,
        description="Afirmação específica com respaldo bibliográfico",
        min_length=1
    )
    evidence: str = Field(
        ...,
        description="Evidência encontrada na literatura",
        min_length=1
    )
    source: str = Field(
        ...,
        description="Fonte da evidência (DOI, URL, citação)",
        min_length=1
    )

    model_config = ConfigDict(extra="forbid")


class CognitiveModel(BaseModel):
    """
    Modelo cognitivo explícito que representa evolução do pensamento.

    Este modelo captura o estado atual do argumento em construção durante
    a conversa. É volátil (em memória) e atualizado pelo Orquestrador a cada turno.

    Ao ser persistido, vira entidade `Argument` no banco de dados.

    Campos principais:
    - claim: O que o usuário está tentando dizer/defender (evolui a cada turno)
    - proposicoes: Fundamentos do argumento com solidez variável (unifica premise/assumption)
    - open_questions: Lacunas identificadas pelo sistema
    - contradictions: Tensões internas detectadas (não bloqueia)
    - solid_grounds: Evidências bibliográficas (futuro - Pesquisador)
    - context: Metadados (domínio, tecnologia, população)

    Responsabilidades dos agentes:
    - Orquestrador: Atualiza claim, proposicoes, open_questions, context
    - Estruturador: Organiza proposicoes
    - Metodologista: Detecta contradictions
    - Pesquisador (futuro): Preenche solid_grounds

    Example:
        >>> from agents.models.proposition import Proposicao
        >>> model = CognitiveModel(
        ...     claim="LLMs aumentam produtividade",
        ...     proposicoes=[
        ...         Proposicao(texto="Equipes usam LLMs", solidez=0.9),
        ...         Proposicao(texto="Produtividade é mensurável", solidez=0.5),
        ...     ],
        ...     open_questions=["Como medir produtividade?"],
        ...     context={"domain": "software development"}
        ... )
        >>> model.claim
        'LLMs aumentam produtividade'
        >>> len(model.proposicoes)
        2

    Ver docs/vision/cognitive_model/core.md para modelo completo.
    """

    claim: str = Field(
        default="",
        description="Afirmação central que o usuário está tentando defender ou explorar. "
                    "Evolui a cada turno conforme conversa se refina."
    )

    proposicoes: List[Proposicao] = Field(
        default_factory=list,
        description="Fundamentos do argumento. Cada proposição tem solidez variável (0-1). "
                    "Solidez alta = fundamento sólido, solidez baixa = hipótese a validar."
    )

    open_questions: List[str] = Field(
        default_factory=list,
        description="Lacunas identificadas pelo sistema que são relevantes para o argumento. "
                    "Orquestrador/Metodologista provocam para preencher."
    )

    contradictions: List[Contradiction] = Field(
        default_factory=list,
        description="Tensões internas do argumento detectadas pelo Metodologista. "
                    "Apenas mencionadas se confiança > 80%. Não bloqueiam fluxo."
    )

    solid_grounds: List[SolidGround] = Field(
        default_factory=list,
        description="Argumentos com base bibliográfica. Preenchido pelo Pesquisador (futuro). "
                    "Diferencia opinião de argumento fundamentado."
    )

    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados inferidos pelo Orquestrador: domínio, tecnologia, "
                    "população, métricas, tipo de artigo."
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "claim": "Claude Code reduz tempo de sprint em 30%",
                "proposicoes": [
                    {"texto": "Equipes Python de 2-5 devs existem", "solidez": 0.95},
                    {"texto": "Tempo de sprint é métrica válida", "solidez": 0.8},
                    {"texto": "Qualidade não é comprometida", "solidez": 0.4},
                ],
                "open_questions": [
                    "Qual é o baseline de tempo sem Claude Code?",
                    "Como medir qualidade do código?"
                ],
                "contradictions": [],
                "solid_grounds": [],
                "context": {
                    "domain": "software development",
                    "technology": "Python, Claude Code",
                    "population": "teams of 2-5 developers",
                    "metrics": "time per sprint",
                    "article_type": "empirical"
                }
            }
        }
    )

    @field_validator("contradictions")
    @classmethod
    def validate_contradictions_confidence(cls, v: List[Contradiction]) -> List[Contradiction]:
        """
        Valida que contradictions só são adicionadas se confiança >= 0.80.

        Sistema só menciona contradições quando tem alta confiança (> 80%).
        Esta validação garante que o modelo não aceita contradições com baixa confiança.
        """
        for contradiction in v:
            if contradiction.confidence < 0.80:
                raise ValueError(
                    f"Contradição com confiança {contradiction.confidence:.2f} < 0.80 não deve ser adicionada. "
                    f"Sistema só menciona contradições com confiança >= 80%."
                )
        return v

    def is_mature(self) -> bool:
        """
        Verifica se argumento atingiu maturidade (heurística simplificada).

        Critérios de maturidade:
        - claim não vazio e específico (> 20 chars)
        - proposicoes suficientes (>= 2) com solidez média alta (>= 0.6)
        - open_questions vazias ou poucas (<= 1)
        - contradictions resolvidas (vazio)

        Returns:
            bool: True se argumento é maduro, False caso contrário

        Notes:
            Esta é uma heurística simplificada. Na implementação completa (11.5),
            a detecção de maturidade será feita via LLM com análise contextual.
        """
        # Calcula solidez média das proposições avaliadas
        evaluated = [p for p in self.proposicoes if p.is_evaluated()]
        avg_solidez = sum(p.solidez for p in evaluated) / len(evaluated) if evaluated else 0

        return (
            len(self.claim) > 20 and
            len(self.proposicoes) >= 2 and
            avg_solidez >= 0.6 and
            len(self.open_questions) <= 1 and
            len(self.contradictions) == 0
        )

    def calculate_solidez(self) -> float:
        """
        Calcula solidez do argumento focal (0-100%).

        Solidez é uma medida composta da força/fundação do argumento baseado em:
        - Especificidade do claim (0-20 pontos)
        - Solidez média das proposições avaliadas (0-30 pontos)
        - Quantidade de proposições (0-15 pontos)
        - Questões respondidas (0-20 pontos)
        - Ausência de contradições (0-15 pontos)
        - Presença de evidências bibliográficas (0-10 pontos bonus)

        Total máximo: 110 pontos, normalizado para 100%.

        Returns:
            float: Solidez (0-100)

        Example:
            >>> model = CognitiveModel(
            ...     claim="Claude Code reduz tempo de sprint em 30%",
            ...     proposicoes=[
            ...         Proposicao(texto="Equipes usam Claude Code", solidez=0.9),
            ...         Proposicao(texto="Tempo é mensurável", solidez=0.85),
            ...     ],
            ...     open_questions=[],
            ...     contradictions=[],
            ... )
            >>> solidez = model.calculate_solidez()
            >>> print(f"Solidez: {solidez:.0f}%")
            Solidez: 95%
        """
        score = 0.0

        # 1. Especificidade do claim (0-20)
        claim_len = len(self.claim)
        if claim_len > 50:
            score += 20
        elif claim_len > 20:
            score += 10 + min(10, (claim_len - 20) / 3)

        # 2. Solidez média das proposições (0-30)
        evaluated = [p for p in self.proposicoes if p.is_evaluated()]
        if evaluated:
            avg_solidez = sum(p.solidez for p in evaluated) / len(evaluated)
            score += avg_solidez * 30  # 0.0-1.0 → 0-30 pontos

        # 3. Quantidade de proposições (0-15)
        prop_count = len(self.proposicoes)
        if prop_count >= 3:
            score += 15
        elif prop_count == 2:
            score += 10
        elif prop_count == 1:
            score += 5

        # 4. Questões respondidas (0-20) - menos é melhor
        questions_count = len(self.open_questions)
        if questions_count == 0:
            score += 20
        elif questions_count == 1:
            score += 10

        # 5. Contradições resolvidas (0-15)
        if len(self.contradictions) == 0:
            score += 15
        elif len(self.contradictions) == 1:
            score += 5

        # 6. Evidências presentes (0-10 bonus)
        if len(self.solid_grounds) > 0:
            score += min(10, len(self.solid_grounds) * 3)

        return min(100.0, score)

    def get_solid_propositions(self, threshold: float = 0.6) -> List[Proposicao]:
        """
        Retorna proposições com solidez alta (>= threshold).

        Args:
            threshold: Limite mínimo de solidez (padrão: 0.6)

        Returns:
            List[Proposicao]: Proposições sólidas
        """
        return [p for p in self.proposicoes if p.is_solid(threshold)]

    def get_fragile_propositions(self, threshold: float = 0.4) -> List[Proposicao]:
        """
        Retorna proposições com solidez baixa (< threshold).

        Args:
            threshold: Limite máximo para ser considerada frágil (padrão: 0.4)

        Returns:
            List[Proposicao]: Proposições frágeis que precisam validação
        """
        return [p for p in self.proposicoes if p.is_fragile(threshold)]

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa modelo para dict (útil para persistência).

        Returns:
            Dict[str, Any]: Representação em dict do modelo
        """
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CognitiveModel":
        """
        Cria instância a partir de dict.

        Args:
            data: Dict com campos do modelo

        Returns:
            CognitiveModel: Instância validada
        """
        return cls(**data)
