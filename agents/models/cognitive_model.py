"""
Schema Pydantic do Modelo Cognitivo.

Este módulo define a estrutura do modelo cognitivo que representa
a evolução do pensamento do usuário durante a conversa.

O modelo cognitivo é volátil (em memória) e captura:
- claim: O que o usuário está tentando dizer/defender
- premises: O que assumimos como verdadeiro
- assumptions: Hipóteses não verificadas
- open_questions: O que não sabemos ainda
- contradictions: Tensões internas detectadas
- solid_grounds: Argumentos com base bibliográfica
- context: Domínio, tecnologia, população inferidos
- conceitos: Conceitos semânticos catalogados (Épico 10.1)
- solidez_geral: Métrica de solidez do argumento (Épico 10.1)
- completude: Métrica de completude do argumento (Épico 10.1)

Ver docs/vision/cognitive_model/core.md para detalhes completos.

Épico 11.1: Schema Explícito de CognitiveModel
Épico 10.1: Adição de campos do Observador
Data: 2025-12-05
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator


class Contradiction(BaseModel):
    """
    Tensão interna detectada no argumento.

    O Metodologista detecta contradictions quando há inconsistências lógicas
    entre claim, premises e assumptions. Apenas mencionadas quando confiança > 80%.
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
    - premises: Fundamentos assumidos como verdadeiros
    - assumptions: Hipóteses não verificadas que precisam validação
    - open_questions: Lacunas identificadas pelo sistema
    - contradictions: Tensões internas detectadas (não bloqueia)
    - solid_grounds: Evidências bibliográficas (futuro - Pesquisador)
    - context: Metadados (domínio, tecnologia, população)

    Responsabilidades dos agentes:
    - Orquestrador: Atualiza claim, assumptions, open_questions, context
    - Estruturador: Organiza premises
    - Metodologista: Detecta contradictions
    - Pesquisador (futuro): Preenche solid_grounds

    Example:
        >>> model = CognitiveModel(
        ...     claim="LLMs aumentam produtividade",
        ...     premises=["Equipes usam LLMs para desenvolvimento"],
        ...     assumptions=["Produtividade é mensurável"],
        ...     open_questions=["Como medir produtividade?"],
        ...     contradictions=[],
        ...     solid_grounds=[],
        ...     context={"domain": "software development"}
        ... )
        >>> model.claim
        'LLMs aumentam produtividade'
        >>> len(model.premises)
        1

    Ver docs/vision/cognitive_model/core.md para modelo completo.
    """

    claim: str = Field(
        default="",
        description="Afirmação central que o usuário está tentando defender ou explorar. "
                    "Evolui a cada turno conforme conversa se refina."
    )

    premises: List[str] = Field(
        default_factory=list,
        description="Fundamentos assumidos como verdadeiros para o argumento fazer sentido. "
                    "Organizado pelo Estruturador."
    )

    assumptions: List[str] = Field(
        default_factory=list,
        description="Hipóteses não verificadas que sustentam o argumento. "
                    "Diferente de premises: assumptions precisam validação. "
                    "Detectadas pelo Orquestrador."
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

    # === CAMPOS DO OBSERVADOR (Épico 10.1) ===

    conceitos: List[str] = Field(
        default_factory=list,
        description="Conceitos semânticos catalogados pelo Observador. "
                    "Lista de labels (ex: ['LLMs', 'Produtividade']). "
                    "Serão UUIDs referenciando ChromaDB no Épico 10.3."
    )

    solidez_geral: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Métrica de solidez do argumento (0-1). "
                    "Calculada pelo Observador baseada em premissas, "
                    "suposições e evidências."
    )

    completude: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Métrica de completude do argumento (0-1). "
                    "Calculada pelo Observador baseada em questões abertas "
                    "e lacunas identificadas."
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "claim": "Claude Code reduz tempo de sprint em 30%",
                "premises": [
                    "Equipes Python de 2-5 devs existem",
                    "Tempo de sprint é métrica válida de produtividade"
                ],
                "assumptions": [
                    "Qualidade não é comprometida",
                    "Resultado é generalizável para outras linguagens"
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
                },
                "conceitos": ["LLMs", "Produtividade", "Claude Code"],
                "solidez_geral": 0.65,
                "completude": 0.70
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
        - premises sólidas (>= 2)
        - assumptions baixas (<= 2)
        - open_questions vazias ou poucas (<= 1)
        - contradictions resolvidas (vazio)

        Returns:
            bool: True se argumento é maduro, False caso contrário

        Notes:
            Esta é uma heurística simplificada. Na implementação completa (11.5),
            a detecção de maturidade será feita via LLM com análise contextual.
        """
        return (
            len(self.claim) > 20 and
            len(self.premises) >= 2 and
            len(self.assumptions) <= 2 and
            len(self.open_questions) <= 1 and
            len(self.contradictions) == 0
        )

    def calculate_solidez(self) -> float:
        """
        Calcula solidez do argumento focal (0-100%).

        Solidez é uma medida composta da força/fundação do argumento baseado em:
        - Especificidade do claim (0-20 pontos)
        - Força dos fundamentos/premises (0-25 pontos)
        - Fraqueza das suposições não verificadas (0-20 pontos)
        - Questões respondidas (0-20 pontos)
        - Ausência de contradições (0-15 pontos)
        - Presença de evidências bibliográficas (0-10 pontos bonus)

        Total máximo: 110 pontos, normalizado para 100%.

        Returns:
            float: Solidez (0-100)

        Example:
            >>> model = CognitiveModel(
            ...     claim="Claude Code reduz tempo de sprint em 30%",
            ...     premises=["Equipes usam Claude Code", "Tempo é mensurável"],
            ...     assumptions=[],
            ...     open_questions=[],
            ...     contradictions=[],
            ...     solid_grounds=[]
            ... )
            >>> solidez = model.calculate_solidez()
            >>> print(f"Solidez: {solidez:.0f}%")
            Solidez: 80%
        """
        score = 0.0

        # 1. Especificidade do claim (0-20)
        claim_len = len(self.claim)
        if claim_len > 50:
            score += 20
        elif claim_len > 20:
            score += 10 + min(10, (claim_len - 20) / 3)

        # 2. Força dos fundamentos (0-25)
        premises_count = len(self.premises)
        if premises_count >= 3:
            score += 25
        elif premises_count == 2:
            score += 20
        elif premises_count == 1:
            score += 10

        # 3. Fraqueza das suposições (0-20) - menos é melhor
        assumptions_count = len(self.assumptions)
        if assumptions_count == 0:
            score += 20
        elif assumptions_count == 1:
            score += 15
        elif assumptions_count == 2:
            score += 10
        elif assumptions_count <= 5:
            score += max(0, 10 - assumptions_count)

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

    def calculate_completude(self) -> float:
        """
        Calcula completude do argumento (0-100%).

        Completude mede quanto do argumento está desenvolvido baseado em:
        - Presença de claim (0-30 pontos)
        - Presença de premissas (0-25 pontos)
        - Poucas questões abertas (0-25 pontos)
        - Poucas suposições não verificadas (0-20 pontos)

        Total máximo: 100 pontos.

        Returns:
            float: Completude (0-100)

        Example:
            >>> model = CognitiveModel(
            ...     claim="Claude Code reduz tempo de sprint em 30%",
            ...     premises=["Equipes usam Claude Code", "Tempo é mensurável"],
            ...     assumptions=[],
            ...     open_questions=[]
            ... )
            >>> completude = model.calculate_completude()
            >>> print(f"Completude: {completude:.0f}%")
            Completude: 100%
        """
        score = 0.0

        # 1. Presença de claim (0-30)
        claim_len = len(self.claim)
        if claim_len > 50:
            score += 30
        elif claim_len > 20:
            score += 20
        elif claim_len > 0:
            score += 10

        # 2. Presença de premissas (0-25)
        premises_count = len(self.premises)
        if premises_count >= 3:
            score += 25
        elif premises_count == 2:
            score += 20
        elif premises_count == 1:
            score += 10

        # 3. Poucas questões abertas (0-25) - menos é melhor
        questions_count = len(self.open_questions)
        if questions_count == 0:
            score += 25
        elif questions_count == 1:
            score += 15
        elif questions_count == 2:
            score += 10
        elif questions_count <= 4:
            score += 5

        # 4. Poucas suposições (0-20) - menos é melhor
        assumptions_count = len(self.assumptions)
        if assumptions_count == 0:
            score += 20
        elif assumptions_count == 1:
            score += 15
        elif assumptions_count == 2:
            score += 10
        elif assumptions_count <= 4:
            score += 5

        return min(100.0, score)

    def update_metrics(self) -> None:
        """
        Atualiza campos solidez_geral e completude com valores calculados.

        Este método deve ser chamado pelo Observador após processar um turno
        para manter as métricas atualizadas no modelo.

        As métricas são normalizadas para 0-1 (ao invés de 0-100).

        Example:
            >>> model = CognitiveModel(claim="LLMs aumentam produtividade")
            >>> model.update_metrics()
            >>> model.solidez_geral
            0.25  # Exemplo: baixa solidez pois faltam premissas
        """
        # Calcula e normaliza para 0-1
        self.solidez_geral = self.calculate_solidez() / 100.0
        self.completude = self.calculate_completude() / 100.0

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
