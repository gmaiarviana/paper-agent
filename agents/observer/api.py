"""
Interface de consulta do Observador (Mente Analitica).

Este modulo define a ObservadorAPI, interface nao-deterministica que permite
ao Orquestrador consultar o estado do raciocinio sem impor decisoes.

Filosofia:
- NaO e command & control (Observador nao da ordens)
- E dialogo contextual (Observador da insights)
- Orquestrador decide autonomamente baseado em insights

Quando usar:
- Mudanca de direcao detectada pelo Orquestrador
- Contradicao aparente no raciocinio
- Incerteza sobre profundidade do argumento
- Checagem de completude antes de sugerir agente

Versao: 2.0 (Epico 10.2 - Processamento via LLM)
Data: 05/12/2025
"""

import logging
from typing import Optional, Dict, Any, List, TYPE_CHECKING

from .state import ObserverInsight

if TYPE_CHECKING:
    from agents.models.cognitive_model import CognitiveModel

logger = logging.getLogger(__name__)


class ObservadorAPI:
    """
    Interface de consulta nao-deterministica do Observador.

    O Orquestrador usa esta API para obter insights sobre o estado atual
    do raciocinio sem que o Observador imponha decisoes.

    Principio fundamental:
    - Observador OBSERVA e INFORMA
    - Orquestrador DECIDE e AGE

    Attributes:
        _cognitive_model: Referencia ao CognitiveModel atual (em memoria).
        _concepts: Lista de conceitos detectados na conversa atual.
        _turn_count: Numero de turnos processados.

    Example:
        >>> api = ObservadorAPI()
        >>> api.update_cognitive_model(cognitive_model_dict)
        >>> insight = api.what_do_you_see(
        ...     context="Usuario mudou de LLMs para bugs",
        ...     question="Conceitos anteriores ainda relevantes?"
        ... )
        >>> print(insight.insight)
        'Parcial - LLMs ainda central, bugs e novo foco'

    Notes:
        - Versao 2.0 (Epico 10.2): Processamento via LLM implementado
        - Integracao com ChromaDB em 10.3
    """

    def __init__(
        self,
        cognitive_model: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ):
        """
        Inicializa API do Observador.

        Args:
            cognitive_model: CognitiveModel inicial (opcional).
                Se None, usa modelo vazio.
            session_id: ID da sessao (para eventos - opcional).
        """
        self._cognitive_model: Dict[str, Any] = cognitive_model or self._create_empty_model()
        self._concepts: List[str] = []
        self._turn_count: int = 0
        self._session_id: Optional[str] = session_id
        self._conversation_history: List[Dict[str, Any]] = []

        logger.info(f"ObservadorAPI inicializada (session={session_id})")

    def _create_empty_model(self) -> Dict[str, Any]:
        """Cria CognitiveModel vazio."""
        return {
            "claim": "",
            "proposicoes": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {}
        }

    # =========================================================================
    # METODOS DE ATUALIZACAO (usados pelo Observador internamente)
    # =========================================================================

    def update_cognitive_model(self, cognitive_model: Dict[str, Any]) -> None:
        """
        Atualiza CognitiveModel interno.

        Chamado pelo Observador apos processar cada turno.

        Args:
            cognitive_model: Novo estado do CognitiveModel.

        Example:
            >>> api.update_cognitive_model({
            ...     "claim": "LLMs aumentam produtividade",
            ...     "proposicoes": [{"texto": "Equipes usam LLMs", "solidez": 0.8}],
            ...     ...
            ... })
        """
        self._cognitive_model = cognitive_model
        self._turn_count += 1
        logger.debug(f"CognitiveModel atualizado (turno {self._turn_count})")

    def add_concepts(self, concepts: List[str]) -> None:
        """
        Adiciona conceitos detectados.

        Args:
            concepts: Lista de conceitos extraidos do turno.

        Example:
            >>> api.add_concepts(["LLMs", "produtividade", "desenvolvedores"])
        """
        for concept in concepts:
            if concept not in self._concepts:
                self._concepts.append(concept)
        logger.debug(f"Conceitos adicionados: {concepts}")

    def process_turn(self, user_input: str) -> Dict[str, Any]:
        """
        Processa um turno via LLM e atualiza CognitiveModel (Epico 10.2).

        Esta funcao e chamada a cada mensagem do usuario para extrair
        informacoes semanticas e atualizar o modelo cognitivo.

        IMPORTANTE: Esta funcao e SILENCIOSA - nao interfere no fluxo
        conversacional do Orquestrador.

        Args:
            user_input: Mensagem do usuario.

        Returns:
            Dict com:
            - cognitive_model: CognitiveModel atualizado
            - extracted: Informacoes extraidas neste turno
            - metrics: Metricas calculadas (solidez, completude)
            - maturity: Avaliacao de maturidade

        Example:
            >>> result = api.process_turn("LLMs aumentam produtividade em 30%")
            >>> print(result['metrics']['solidez'])
            0.35
        """
        from .nodes import process_turn as _process_turn

        # Adicionar ao historico interno
        self._conversation_history.append({
            "role": "user",
            "content": user_input
        })

        self._turn_count += 1

        # Processar via nodes.py
        result = _process_turn(
            user_input=user_input,
            conversation_history=self._conversation_history,
            previous_cognitive_model=self._cognitive_model,
            session_id=self._session_id,
            turn_number=self._turn_count
        )

        # Atualizar estado interno
        self._cognitive_model = result["cognitive_model"]
        self._concepts = self._cognitive_model.get("concepts_detected", [])

        return result

    def add_assistant_message(self, content: str) -> None:
        """
        Adiciona mensagem do assistente ao historico interno.

        Deve ser chamado apos cada resposta do Orquestrador
        para manter o historico completo.

        Args:
            content: Conteudo da mensagem do assistente.

        Example:
            >>> api.add_assistant_message("Interessante! Me conte mais...")
        """
        self._conversation_history.append({
            "role": "assistant",
            "content": content
        })

    # =========================================================================
    # METODOS DE CONSULTA (usados pelo Orquestrador)
    # =========================================================================

    def what_do_you_see(
        self,
        context: str,
        question: str
    ) -> ObserverInsight:
        """
        Responde consulta contextual do Orquestrador.

        Este e o metodo principal de interacao entre Orquestrador e Observador.
        O Orquestrador descreve o contexto e faz uma pergunta especifica.
        O Observador analisa o CognitiveModel e retorna um insight.

        IMPORTANTE: O Observador NAO da ordens. Ele oferece perspectiva
        que o Orquestrador pode usar para tomar decisoes autonomamente.

        Args:
            context: Contexto da consulta (ex: "Usuario mudou de direcao").
            question: Pergunta especifica (ex: "Conceitos ainda relevantes?").

        Returns:
            ObserverInsight: Insight com observacao, sugestao opcional,
                confianca e evidencias do CognitiveModel.

        Example:
            >>> insight = api.what_do_you_see(
            ...     context="Usuario mudou de LLMs para bugs",
            ...     question="Conceitos anteriores ainda relevantes?"
            ... )
            >>> print(insight.insight)
            'Parcial - LLMs ainda central, bugs e novo foco'
            >>> print(insight.confidence)
            0.8

        Notes:
            - Versao POC (10.1): Retorna insight baseado em heuristica simples
            - Versao completa (10.2): Usara LLM para analise contextual
        """
        logger.info(f"Consulta recebida: context='{context[:50]}...', question='{question[:50]}...'")

        # POC: Analise baseada em heuristica simples
        # Em 10.2, sera substituido por chamada LLM
        insight = self._analyze_with_heuristics(context, question)

        logger.info(f"Insight gerado: confidence={insight.confidence:.2f}")
        return insight

    def _analyze_with_heuristics(self, context: str, question: str) -> ObserverInsight:
        """
        Analise POC usando heuristicas simples (sem LLM).

        Esta implementacao sera substituida por analise via LLM em 10.2.

        Args:
            context: Contexto da consulta.
            question: Pergunta especifica.

        Returns:
            ObserverInsight: Insight baseado em heuristicas.
        """
        claim = self._cognitive_model.get("claim", "")
        proposicoes = self._cognitive_model.get("proposicoes", [])
        open_questions = self._cognitive_model.get("open_questions", [])
        contradictions = self._cognitive_model.get("contradictions", [])

        # Heuristica: Calcular solidez e completude
        solidez = self.get_solidez()
        completude = 1.0 - (len(open_questions) / max(1, len(open_questions) + len(proposicoes)))

        # Construir insight baseado no contexto
        if "mudanca" in context.lower() or "direcao" in context.lower():
            insight_text = f"Detectei {'mudanca significativa' if len(self._concepts) > 3 else 'evolucao natural'} no foco. "
            insight_text += f"Conceitos acumulados: {len(self._concepts)}."
            suggestion = "Considere verificar se conceitos anteriores ainda sao relevantes."
            confidence = 0.7
        elif "contradicao" in context.lower():
            if contradictions:
                insight_text = f"Ha {len(contradictions)} contradicao(oes) detectada(s) no raciocinio."
                suggestion = "Recomendo esclarecer antes de prosseguir."
                confidence = 0.85
            else:
                insight_text = "Nao detectei contradicoes significativas no raciocinio atual."
                suggestion = None
                confidence = 0.8
        elif "completude" in context.lower() or "solidez" in context.lower():
            insight_text = f"Solidez atual: {solidez:.0%}. "
            if solidez >= 0.7:
                insight_text += "Argumento parece bem fundamentado."
                suggestion = "Pode ser momento de sugerir validacao metodologica."
            elif solidez >= 0.4:
                insight_text += "Argumento em construcao, faltam alguns fundamentos."
                suggestion = "Explorar mais o contexto pode fortalecer o argumento."
            else:
                insight_text += "Argumento ainda vago, precisa mais desenvolvimento."
                suggestion = "Perguntas abertas podem ajudar a clarificar."
            confidence = 0.75
        else:
            # Fallback generico
            # Conta proposições sólidas (solidez >= 0.6) e frágeis (solidez < 0.6 ou None)
            solid_count = sum(1 for p in proposicoes if isinstance(p, dict) and p.get("solidez") is not None and p.get("solidez") >= 0.6)
            fragile_count = len(proposicoes) - solid_count
            insight_text = f"Estado atual: claim definido={'sim' if claim else 'nao'}, "
            insight_text += f"{solid_count} proposicoes solidas, {fragile_count} frageis, "
            insight_text += f"{len(open_questions)} questoes abertas."
            suggestion = None
            confidence = 0.6

        return ObserverInsight(
            insight=insight_text,
            suggestion=suggestion,
            confidence=confidence,
            evidence={
                "claim_defined": bool(claim),
                "proposicoes_count": len(proposicoes),
                "open_questions_count": len(open_questions),
                "contradictions_count": len(contradictions),
                "concepts_detected": self._concepts[:5],  # Primeiros 5
                "solidez": solidez
            }
        )

    def get_current_state(self) -> Dict[str, Any]:
        """
        Retorna estado atual completo do CognitiveModel.

        Usado quando Orquestrador precisa de visao geral,
        nao apenas insight especifico.

        Returns:
            Dict[str, Any]: CognitiveModel completo como dict.

        Example:
            >>> state = api.get_current_state()
            >>> print(state['claim'])
            'LLMs aumentam produtividade'
        """
        return self._cognitive_model.copy()

    def has_contradiction(self) -> bool:
        """
        Check rapido: ha contradicoes detectadas?

        Atalho para verificar se existem contradicoes no CognitiveModel
        sem precisar analisar o modelo completo.

        Returns:
            bool: True se ha pelo menos uma contradicao detectada.

        Example:
            >>> if api.has_contradiction():
            ...     print("Atencao: contradicoes detectadas!")
        """
        contradictions = self._cognitive_model.get("contradictions", [])
        return len(contradictions) > 0

    def get_solidez(self) -> float:
        """
        Check rapido: solidez geral atual.

        Calcula solidez do argumento baseado na estrutura do CognitiveModel.
        Solidez alta indica argumento bem fundamentado.

        Formula simplificada (POC):
        - Premises sao positivos (+)
        - Assumptions sao negativos (-)
        - Open questions sao negativos (-)
        - Contradictions sao muito negativos (--)

        Returns:
            float: Solidez entre 0.0 e 1.0.

        Example:
            >>> solidez = api.get_solidez()
            >>> print(f"Solidez: {solidez:.0%}")
            Solidez: 65%

        Notes:
            - Versao POC usa formula simplificada baseada em proposicoes
            - Proposicoes solidas (solidez >= 0.6) contribuem positivamente
            - Proposicoes frageis (solidez < 0.6) contribuem negativamente
        """
        claim = self._cognitive_model.get("claim", "")
        proposicoes = self._cognitive_model.get("proposicoes", [])
        open_questions = self._cognitive_model.get("open_questions", [])
        contradictions = self._cognitive_model.get("contradictions", [])

        # Se nao tem claim, solidez = 0
        if not claim:
            return 0.0

        # Separar proposicoes por solidez
        solid_props = []
        fragile_props = []
        for p in proposicoes:
            if isinstance(p, dict):
                solidez = p.get("solidez")
                if solidez is not None and solidez >= 0.6:
                    solid_props.append(p)
                elif solidez is not None and solidez < 0.6:
                    fragile_props.append(p)

        # Calcular score
        score = 0.0

        # Claim definido: base 20%
        score += 0.20

        # Proposicoes solidas: cada uma adiciona ate 15% (max 45%)
        score += min(0.45, len(solid_props) * 0.15)

        # Proposicoes frageis: cada uma subtrai 5% (max -25%)
        score -= min(0.25, len(fragile_props) * 0.05)

        # Open questions: cada uma subtrai 5% (max -15%)
        score -= min(0.15, len(open_questions) * 0.05)

        # Contradictions: cada uma subtrai 10% (max -30%)
        score -= min(0.30, len(contradictions) * 0.10)

        # Bonus: claim longo (> 50 chars) adiciona 5%
        if len(claim) > 50:
            score += 0.05

        # Garantir range 0-1
        return max(0.0, min(1.0, score))

    def get_completude(self) -> float:
        """
        Check rapido: completude atual.

        Completude indica o quanto do argumento esta desenvolvido.
        Baseia-se na proporcao de proposicoes solidas vs questoes abertas.

        Returns:
            float: Completude entre 0.0 e 1.0.

        Example:
            >>> completude = api.get_completude()
            >>> print(f"Completude: {completude:.0%}")
            Completude: 80%
        """
        proposicoes = self._cognitive_model.get("proposicoes", [])
        open_questions = self._cognitive_model.get("open_questions", [])

        # Contar proposicoes solidas (solidez >= 0.6)
        solid_count = sum(
            1 for p in proposicoes
            if isinstance(p, dict) and p.get("solidez") is not None and p.get("solidez") >= 0.6
        )

        total_elements = solid_count + len(open_questions)
        if total_elements == 0:
            return 0.0

        # Completude = proposicoes solidas / total elementos
        return solid_count / total_elements

    def get_concepts(self) -> list[str]:
        """
        Retorna lista de conceitos detectados.

        Returns:
            list[str]: Conceitos detectados na conversa.

        Example:
            >>> concepts = api.get_concepts()
            >>> print(concepts)
            ['LLMs', 'produtividade', 'desenvolvedores']
        """
        return self._concepts.copy()

    def get_turn_count(self) -> int:
        """
        Retorna numero de turnos processados.

        Returns:
            int: Numero de turnos desde a inicializacao.
        """
        return self._turn_count

    # =========================================================================
    # METODOS DE RESET
    # =========================================================================

    def reset(self) -> None:
        """
        Reseta estado do Observador para nova conversa.

        Limpa CognitiveModel, conceitos e contador de turnos.
        Usado quando uma nova conversa e iniciada.
        """
        self._cognitive_model = self._create_empty_model()
        self._concepts = []
        self._turn_count = 0
        logger.info("ObservadorAPI resetada para nova conversa")
