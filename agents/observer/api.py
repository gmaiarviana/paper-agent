"""
Interface de consulta do Observador (ObservadorAPI).

Este módulo implementa a API não-determinística que o Orquestrador usa
para consultar o Observador sobre o estado do raciocínio.

Filosofia da API:
- NÃO é command & control (Observador não dá ordens)
- É diálogo contextual (Observador dá insights)
- Orquestrador consulta quando incerto, decide autonomamente

Épico 10.1: Mitose do Orquestrador
Data: 05/12/2025
"""

import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


@dataclass
class ObserverInsight:
    """
    Insight contextual retornado pelo Observador.

    Representa a resposta do Observador a uma consulta do Orquestrador.
    Contém observação principal, sugestão opcional, confiança e evidências.

    Attributes:
        insight: Observação principal sobre o estado atual.
        suggestion: Sugestão de ação (opcional, não é comando).
        confidence: Confiança do insight (0-1).
        evidence: Dados do CognitiveModel que sustentam o insight.

    Example:
        >>> insight = ObserverInsight(
        ...     insight="Parcial - LLMs ainda central, mas bugs é novo foco",
        ...     suggestion="Pode conectar: bugs como métrica de produtividade",
        ...     confidence=0.8,
        ...     evidence={"concepts": ["LLMs", "bugs"], "claims": [...]}
        ... )
    """

    insight: str
    suggestion: Optional[str]
    confidence: float
    evidence: Dict[str, Any]


class ObservadorAPI:
    """
    Interface de consulta não-determinística do Observador.

    O Orquestrador usa esta API para consultar o estado do raciocínio
    quando precisa de contexto adicional para tomar decisões.

    Características da API:
    - Consultas são contextuais (não apenas getters de dados)
    - Respostas são insights (não comandos)
    - Orquestrador decide autonomamente baseado em insights

    Gatilhos naturais para consulta:
    1. Mudança de direção detectada pelo Orquestrador
    2. Contradição aparente entre inputs do usuário
    3. Incerteza sobre profundidade do argumento
    4. Checagem de completude antes de sugerir próximo agente

    Example:
        >>> api = ObservadorAPI(cognitive_model_dict)
        >>> insight = api.what_do_you_see(
        ...     context="Usuário mudou de LLMs para bugs",
        ...     question="Conceitos anteriores ainda relevantes?"
        ... )
        >>> print(insight.suggestion)
        'Pode conectar: bugs como métrica de produtividade'

    Attributes:
        _cognitive_model: Dict com estado atual do CognitiveModel.

    Notes:
        No Épico 10.1 (POC), esta API trabalha com dados em memória.
        No Épico 10.2+, integrará com LLM para análises contextuais.
    """

    def __init__(self, cognitive_model: Optional[Dict[str, Any]] = None):
        """
        Inicializa ObservadorAPI com CognitiveModel.

        Args:
            cognitive_model: Dict representando CognitiveModel atual.
                Se None, inicializa com modelo vazio.

        Example:
            >>> api = ObservadorAPI({"claim": "LLMs...", "premises": []})
        """
        self._cognitive_model = cognitive_model or self._create_empty_model()
        logger.debug(f"ObservadorAPI inicializada com claim: {self._cognitive_model.get('claim', 'N/A')[:50]}...")

    def _create_empty_model(self) -> Dict[str, Any]:
        """Cria CognitiveModel vazio com estrutura padrão."""
        return {
            "claim": "",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {},
            # Novos campos do Observador (Épico 10.1)
            "conceitos": [],
            "solidez_geral": 0.0,
            "completude": 0.0,
        }

    def update_cognitive_model(self, cognitive_model: Dict[str, Any]) -> None:
        """
        Atualiza CognitiveModel interno.

        Chamado pelo Observador após processar um turno.

        Args:
            cognitive_model: Novo estado do CognitiveModel.
        """
        self._cognitive_model = cognitive_model
        logger.debug(f"CognitiveModel atualizado: claim={cognitive_model.get('claim', 'N/A')[:50]}...")

    def what_do_you_see(
        self,
        context: str,
        question: str
    ) -> ObserverInsight:
        """
        Responde consulta contextual do Orquestrador.

        Esta é a principal interface de diálogo entre Orquestrador e Observador.
        Orquestrador fornece contexto + pergunta, Observador responde com insight.

        Args:
            context: Contexto da consulta (ex: "mudança de direção", "contradição").
            question: Pergunta específica (ex: "conceitos ainda relevantes?").

        Returns:
            ObserverInsight com:
                - insight: Observação principal
                - suggestion: Sugestão de ação (opcional)
                - confidence: Confiança (0-1)
                - evidence: Dados que sustentam

        Example:
            >>> insight = api.what_do_you_see(
            ...     context="Usuário mudou de LLMs para bugs",
            ...     question="Conceitos anteriores ainda relevantes?"
            ... )
            >>> insight.insight
            'Parcial - LLMs ainda central, bugs é novo foco'

        Notes:
            No Épico 10.1 (POC), usa heurísticas simples.
            No Épico 10.2+, usará LLM para análise contextual.
        """
        logger.info(f"ObservadorAPI.what_do_you_see: context='{context[:50]}...', question='{question[:50]}...'")

        # Analisar contexto e gerar insight (POC: heurísticas simples)
        insight_text, suggestion, confidence = self._analyze_context(context, question)

        # Construir evidência a partir do CognitiveModel
        evidence = {
            "claim": self._cognitive_model.get("claim", ""),
            "concepts": self._cognitive_model.get("conceitos", []),
            "open_questions": self._cognitive_model.get("open_questions", []),
            "contradictions_count": len(self._cognitive_model.get("contradictions", [])),
            "solidez": self._cognitive_model.get("solidez_geral", 0.0),
            "completude": self._cognitive_model.get("completude", 0.0),
        }

        return ObserverInsight(
            insight=insight_text,
            suggestion=suggestion,
            confidence=confidence,
            evidence=evidence,
        )

    def _analyze_context(
        self,
        context: str,
        question: str
    ) -> tuple[str, Optional[str], float]:
        """
        Analisa contexto e gera insight (heurísticas POC).

        No Épico 10.2+, esta análise será feita via LLM.
        Por enquanto, usa heurísticas baseadas em palavras-chave.

        Args:
            context: Contexto da consulta.
            question: Pergunta específica.

        Returns:
            Tuple (insight, suggestion, confidence)
        """
        context_lower = context.lower()
        question_lower = question.lower()

        # Heurística 1: Mudança de direção
        if "mud" in context_lower or "direção" in context_lower or "changed" in context_lower:
            concepts = self._cognitive_model.get("conceitos", [])
            if concepts:
                return (
                    f"Detectei {len(concepts)} conceitos na conversa: {', '.join(concepts[:3])}. "
                    "Mudança de direção pode ser natural se conceitos se conectam.",
                    "Considere perguntar como os novos conceitos se relacionam com os anteriores.",
                    0.7,
                )
            return (
                "Ainda não há conceitos catalogados para comparar.",
                "Continue explorando para construir base de conceitos.",
                0.5,
            )

        # Heurística 2: Contradição
        if "contradiç" in context_lower or "inconsist" in context_lower or "contradiction" in context_lower:
            contradictions = self._cognitive_model.get("contradictions", [])
            if contradictions:
                return (
                    f"Existem {len(contradictions)} contradição(ões) registrada(s).",
                    "Pode ser útil esclarecer a tensão antes de prosseguir.",
                    0.85,
                )
            return (
                "Não há contradições explícitas registradas ainda.",
                None,
                0.6,
            )

        # Heurística 3: Completude / profundidade
        if "complet" in question_lower or "profund" in context_lower or "depth" in context_lower:
            completude = self._cognitive_model.get("completude", 0.0)
            open_questions = self._cognitive_model.get("open_questions", [])
            if completude > 0.7:
                return (
                    f"Argumento está {completude*100:.0f}% completo. "
                    f"Restam {len(open_questions)} questão(ões) aberta(s).",
                    "Pode ser bom momento para sugerir validação metodológica.",
                    0.8,
                )
            return (
                f"Argumento ainda em desenvolvimento ({completude*100:.0f}%). "
                f"Há {len(open_questions)} questão(ões) a explorar.",
                "Continue explorando antes de sugerir validação.",
                0.75,
            )

        # Heurística 4: Solidez
        if "solidez" in question_lower or "solid" in context_lower or "strength" in context_lower:
            solidez = self._cognitive_model.get("solidez_geral", 0.0)
            premises = self._cognitive_model.get("premises", [])
            assumptions = self._cognitive_model.get("assumptions", [])
            return (
                f"Solidez atual: {solidez*100:.0f}%. "
                f"{len(premises)} premissa(s), {len(assumptions)} suposição(ões).",
                "Solidez aumenta com mais premissas e menos suposições não verificadas.",
                0.8,
            )

        # Fallback: resposta genérica
        claim = self._cognitive_model.get("claim", "")
        return (
            f"Argumento em construção sobre: '{claim[:100]}...'",
            "Continue o diálogo para enriquecer o modelo cognitivo.",
            0.5,
        )

    def get_current_state(self) -> Dict[str, Any]:
        """
        Retorna estado atual completo do CognitiveModel.

        Usado quando Orquestrador precisa de visão geral completa,
        não apenas insight específico.

        Returns:
            Dict com CognitiveModel completo.

        Example:
            >>> state = api.get_current_state()
            >>> state['claim']
            'LLMs aumentam produtividade'
        """
        return self._cognitive_model.copy()

    def has_contradiction(self) -> bool:
        """
        Check rápido: há contradições detectadas?

        Útil para Orquestrador decidir se deve abordar contradições.

        Returns:
            True se há ao menos uma contradição.

        Example:
            >>> if api.has_contradiction():
            ...     print("Há contradições a resolver")
        """
        contradictions = self._cognitive_model.get("contradictions", [])
        return len(contradictions) > 0

    def get_solidez(self) -> float:
        """
        Check rápido: solidez geral atual (0-1).

        Mede força da argumentação baseada em premissas,
        suposições e evidências.

        Returns:
            Float entre 0 e 1 representando solidez.

        Example:
            >>> solidez = api.get_solidez()
            >>> if solidez < 0.5:
            ...     print("Argumento ainda frágil")
        """
        return self._cognitive_model.get("solidez_geral", 0.0)

    def get_completude(self) -> float:
        """
        Check rápido: completude atual (0-1).

        Mede quanto do argumento está desenvolvido baseado
        em questões abertas e lacunas.

        Returns:
            Float entre 0 e 1 representando completude.

        Example:
            >>> completude = api.get_completude()
            >>> if completude > 0.8:
            ...     print("Argumento bem desenvolvido")
        """
        return self._cognitive_model.get("completude", 0.0)

    def get_concepts(self) -> List[str]:
        """
        Retorna lista de conceitos catalogados.

        Útil para Orquestrador entender vocabulário da conversa.

        Returns:
            Lista de strings com labels dos conceitos.

        Example:
            >>> concepts = api.get_concepts()
            >>> print(f"Conceitos: {', '.join(concepts)}")
        """
        return self._cognitive_model.get("conceitos", [])

    def get_open_questions(self) -> List[str]:
        """
        Retorna lista de questões abertas.

        Útil para Orquestrador decidir o que explorar.

        Returns:
            Lista de strings com questões abertas.

        Example:
            >>> questions = api.get_open_questions()
            >>> for q in questions:
            ...     print(f"- {q}")
        """
        return self._cognitive_model.get("open_questions", [])
