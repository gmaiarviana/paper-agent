"""
Gerenciamento de snapshots e detecção de maturidade.

Este módulo implementa:
- Detecção de maturidade via LLM (não apenas heurística)
- Criação automática de snapshots quando argumento amadurece
- Integração entre MultiAgentState e DatabaseManager

Épico 11.5: Indicadores de Maturidade
Data: 2025-11-17
"""

import logging
import json
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic

from agents.models.cognitive_model import CognitiveModel
from agents.database.manager import DatabaseManager, get_database_manager
from utils.config import get_anthropic_model

logger = logging.getLogger(__name__)


class MaturityAssessment(BaseModel):
    """
    Avaliação de maturidade de um argumento via LLM.

    Campos:
    - is_mature: Se argumento atingiu maturidade
    - confidence: Confiança da avaliação (0-1)
    - justification: Por que sistema considera maduro/imaturo
    - missing_elements: Elementos que faltam (se não maduro)
    """

    is_mature: bool = Field(
        ...,
        description="Se argumento atingiu maturidade e está pronto para snapshot"
    )
    confidence: float = Field(
        ...,
        description="Confiança da avaliação (0-1)",
        ge=0.0,
        le=1.0
    )
    justification: str = Field(
        ...,
        description="Justificativa da avaliação de maturidade"
    )
    missing_elements: list[str] = Field(
        default_factory=list,
        description="Elementos que faltam para argumento amadurecer (se não maduro)"
    )


MATURITY_DETECTION_PROMPT = """
Você é um avaliador de maturidade de argumentos científicos.

Analise o modelo cognitivo abaixo e determine se o argumento atingiu maturidade para ser persistido como snapshot.

MODELO COGNITIVO:
{cognitive_model_json}

CRITÉRIOS DE MATURIDADE:
1. **Claim estável e específico**: Afirmação clara (>20 chars), não vaga
2. **Premises sólidas**: Fundamentos claros e verificáveis (>= 2)
3. **Assumptions baixas**: Poucas hipóteses não verificadas (<= 2)
4. **Open_questions respondidas**: Lista vazia ou apenas questões secundárias (<= 1)
5. **Contradictions resolvidas**: Nenhuma contradição detectada
6. **Context completo**: Domínio, tecnologia, população definidos

IMPORTANTE:
- Argumento maduro = pronto para persistir (usuário pode pausar conversa sem perder progresso)
- Argumento imaturo = ainda explorando, claim muda muito, lacunas significativas
- Use confiança alta (>0.8) apenas quando critérios estão claramente atendidos

RETORNE JSON:
{{
    "is_mature": boolean,
    "confidence": float (0-1),
    "justification": "string explicando por que maduro/imaturo",
    "missing_elements": ["lista de elementos faltando (se imaturo)"]
}}
"""


class SnapshotManager:
    """
    Gerenciador de snapshots e detecção de maturidade.

    Responsabilidades:
    - Avaliar maturidade de CognitiveModel via LLM
    - Criar snapshots automaticamente quando detecta maturidade
    - Integrar com DatabaseManager para persistência

    Example:
        >>> manager = SnapshotManager()
        >>> assessment = manager.assess_maturity(cognitive_model)
        >>> if assessment.is_mature:
        ...     snapshot_id = manager.create_snapshot(idea_id, cognitive_model)
    """

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        Inicializa SnapshotManager.

        Args:
            db_manager: DatabaseManager customizado (opcional).
                        Se None, usa singleton global via get_database_manager()
        """
        self.db = db_manager or get_database_manager()
        self.llm = get_anthropic_model("claude-3-5-haiku-20241022")  # Haiku para custo-benefício

    def assess_maturity(
        self,
        cognitive_model: CognitiveModel,
        claim_history: Optional[list] = None
    ) -> MaturityAssessment:
        """
        Avalia maturidade de um argumento via LLM.

        Args:
            cognitive_model: CognitiveModel a ser avaliado
            claim_history: Histórico de claims (opcional) para detectar estabilidade

        Returns:
            MaturityAssessment: Avaliação completa de maturidade

        Example:
            >>> assessment = manager.assess_maturity(cognitive_model)
            >>> if assessment.is_mature and assessment.confidence > 0.8:
            ...     print("Argumento maduro!")
        """
        # Preparar dados para LLM
        model_dict = cognitive_model.to_dict()

        # Adicionar claim_history se disponível (para detectar estabilidade)
        if claim_history:
            model_dict["claim_history"] = claim_history

        model_json = json.dumps(model_dict, indent=2, ensure_ascii=False)

        # Preparar prompt
        prompt = MATURITY_DETECTION_PROMPT.format(cognitive_model_json=model_json)

        try:
            # Invocar LLM
            message = HumanMessage(content=prompt)
            response = self.llm.invoke([message])

            # Parsear JSON da resposta
            response_text = response.content.strip()

            # Remover markdown code blocks se presentes
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])  # Remove primeira e última linha

            assessment_dict = json.loads(response_text)

            # Validar com Pydantic
            assessment = MaturityAssessment(**assessment_dict)

            logger.info(
                f"Maturidade avaliada: is_mature={assessment.is_mature}, "
                f"confidence={assessment.confidence:.2f}"
            )

            return assessment

        except Exception as e:
            logger.error(f"Erro ao avaliar maturidade via LLM: {e}")

            # Fallback: usar heurística simplificada
            logger.warning("Usando fallback heurístico para detecção de maturidade")
            is_mature = cognitive_model.is_mature()

            return MaturityAssessment(
                is_mature=is_mature,
                confidence=0.6,  # Confiança baixa (fallback)
                justification="Avaliação via heurística (LLM falhou)",
                missing_elements=[] if is_mature else ["Avaliação LLM não disponível"]
            )

    def create_snapshot(
        self,
        idea_id: str,
        cognitive_model: CognitiveModel,
        update_current_argument: bool = True
    ) -> str:
        """
        Cria snapshot de argumento no banco de dados.

        Args:
            idea_id: UUID da ideia proprietária
            cognitive_model: CognitiveModel a ser persistido
            update_current_argument: Se deve atualizar current_argument_id da idea

        Returns:
            str: UUID do argumento criado (snapshot)

        Example:
            >>> snapshot_id = manager.create_snapshot(idea_id, cognitive_model)
        """
        # Criar argumento versionado (version auto-incrementa)
        argument_id = self.db.create_argument(idea_id, cognitive_model)

        # Atualizar argumento focal da ideia (se solicitado)
        if update_current_argument:
            self.db.update_idea_current_argument(idea_id, argument_id)

        logger.info(f"Snapshot criado: {argument_id} (idea={idea_id})")

        return argument_id

    def create_snapshot_if_mature(
        self,
        idea_id: str,
        cognitive_model: CognitiveModel,
        claim_history: Optional[list] = None,
        confidence_threshold: float = 0.8
    ) -> Optional[str]:
        """
        Avalia maturidade e cria snapshot automaticamente se maduro.

        Este é o método principal para integração com fluxo conversacional.
        Combina assess_maturity + create_snapshot em uma operação.

        Args:
            idea_id: UUID da ideia
            cognitive_model: CognitiveModel a avaliar
            claim_history: Histórico de claims (opcional)
            confidence_threshold: Mínimo de confiança para criar snapshot (padrão: 0.8)

        Returns:
            str: UUID do snapshot criado, ou None se não maduro

        Example:
            >>> snapshot_id = manager.create_snapshot_if_mature(idea_id, model)
            >>> if snapshot_id:
            ...     print(f"Snapshot automático criado: {snapshot_id}")
        """
        # Avaliar maturidade
        assessment = self.assess_maturity(cognitive_model, claim_history)

        # Criar snapshot apenas se maduro E confiança alta
        if assessment.is_mature and assessment.confidence >= confidence_threshold:
            logger.info(
                f"Argumento amadureceu (confiança={assessment.confidence:.2f})! "
                f"Criando snapshot automático..."
            )

            snapshot_id = self.create_snapshot(idea_id, cognitive_model)

            return snapshot_id

        else:
            logger.debug(
                f"Argumento não maduro ou confiança baixa "
                f"(is_mature={assessment.is_mature}, confidence={assessment.confidence:.2f})"
            )
            return None


# =========================================================================
# FUNÇÕES HELPERS GLOBAIS
# =========================================================================

def detect_argument_maturity(
    cognitive_model: CognitiveModel,
    claim_history: Optional[list] = None
) -> MaturityAssessment:
    """
    Helper global para detectar maturidade de argumento.

    Args:
        cognitive_model: CognitiveModel a avaliar
        claim_history: Histórico de claims (opcional)

    Returns:
        MaturityAssessment: Avaliação de maturidade

    Example:
        >>> from agents.persistence import detect_argument_maturity
        >>> assessment = detect_argument_maturity(cognitive_model)
        >>> if assessment.is_mature:
        ...     print("Pronto para snapshot!")
    """
    manager = SnapshotManager()
    return manager.assess_maturity(cognitive_model, claim_history)


def create_snapshot_if_mature(
    idea_id: str,
    cognitive_model: CognitiveModel,
    claim_history: Optional[list] = None
) -> Optional[str]:
    """
    Helper global para criar snapshot automático se argumento maduro.

    Args:
        idea_id: UUID da ideia
        cognitive_model: CognitiveModel a avaliar
        claim_history: Histórico de claims (opcional)

    Returns:
        str: UUID do snapshot criado, ou None se não maduro

    Example:
        >>> from agents.persistence import create_snapshot_if_mature
        >>> snapshot_id = create_snapshot_if_mature(idea_id, cognitive_model)
        >>> if snapshot_id:
        ...     print(f"Argumento amadureceu! Snapshot V{version} criado")
    """
    manager = SnapshotManager()
    return manager.create_snapshot_if_mature(idea_id, cognitive_model, claim_history)
