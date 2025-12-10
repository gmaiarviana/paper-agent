"""
Executor para cenários multi-turn de validação do sistema multi-agente.

Este módulo implementa MultiTurnExecutor, que executa cenários de conversa
multi-turn end-to-end, rastreando agentes chamados, preservando estado entre
turnos e validando comportamento esperado vs observado.

Versão: 1.1 (Épico 13.6 - Validação de Detecções do Observer)
Data: 2025-12-10
"""

from typing import Dict, List, Any, Callable
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage

# Imports do projeto
from agents.orchestrator.state import create_initial_multi_agent_state
from core.utils.test_scenarios import ConversationScenario
from core.utils.event_bus.singleton import get_event_bus

class MultiTurnExecutor:
    """
    Executa cenários multi-turn e rastreia comportamento do sistema.
    
    Responsabilidades:
    - Executar conversa turn-by-turn
    - Rastrear agentes chamados em cada turno
    - Preservar estado entre turnos
    - Coletar métricas (tokens, custo, duração)
    - Validar comportamento esperado vs observado
    
    Example:
        >>> from agents.multi_agent_graph import create_multi_agent_graph
        >>> from core.utils.test_scenarios import ConversationScenario
        >>> 
        >>> graph = create_multi_agent_graph()
        >>> executor = MultiTurnExecutor(graph)
        >>> scenario = ConversationScenario.from_epic7_scenario(3)
        >>> result = executor.execute_scenario(scenario)
        >>> print(result["success"])  # True/False
    """
    
    def __init__(self, graph):
        """
        Inicializa executor com grafo multi-agente.
        
        Args:
            graph: Grafo compilado (resultado de create_multi_agent_graph())
        """
        self.graph = graph
        self.event_bus = get_event_bus()
    
    def execute_scenario(self, scenario: ConversationScenario) -> Dict[str, Any]:
        """
        Executa cenário completo turn-by-turn.
        
        Args:
            scenario: Cenário a executar (ConversationScenario)
            
        Returns:
            Dict com:
                - scenario_id: str
                - session_id: str
                - turns: List[Dict] - resultado de cada turno
                - final_state: Dict - estado final do sistema
                - agents_called: List[str] - agentes acionados
                - metrics: Dict - tokens, custo, duração
                - success: bool - validação passou?
                - validation_errors: List[str] - erros encontrados
        
        Example:
            >>> result = executor.execute_scenario(scenario)
            >>> print(f"Success: {result['success']}")
            >>> print(f"Agents: {result['agents_called']}")
            >>> for turn in result['turns']:
            ...     print(f"Turn {turn['turn']}: {turn['user_input']}")
        """
        session_id = f"test-{scenario.id}-{int(datetime.now().timestamp())}"
        
        # Criar estado inicial com primeiro input do usuário
        first_user_input = None
        for turn_type, content in scenario.turns:
            if turn_type == "user":
                first_user_input = content
                break
        
        if not first_user_input:
            raise ValueError(f"Cenário {scenario.id} não tem input de usuário")
        
        state = create_initial_multi_agent_state(
            user_input=first_user_input,
            session_id=session_id
        )
        
        # Configuração do grafo (thread_id para persistência)
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }
        
        # Executar turnos
        turns_result = []
        agents_called = []
        current_turn = 0
        
        for turn_type, content in scenario.turns:
            if turn_type == "user":
                current_turn += 1
                
                # Se não é o primeiro turno, adicionar input ao estado
                if current_turn > 1:
                    state["messages"].append(HumanMessage(content=content))
                    state["user_input"] = content
                    state["conversation_history"].append(f"Usuário: {content}")
                
                # Capturar eventos antes do turno (para rastrear novos eventos)
                events_before = self._get_all_events(session_id)
                events_before_keys = {
                    (e.get("timestamp", ""), e.get("event_type", ""), e.get("agent_name", ""))
                    for e in events_before
                }
                
                # Executar grafo
                start_time = datetime.now()
                result = self.graph.invoke(state, config=config)
                duration = (datetime.now() - start_time).total_seconds()
                
                # Rastrear agentes chamados neste turno (novos eventos)
                events_after = self._get_all_events(session_id)
                new_events = [
                    e for e in events_after
                    if (e.get("timestamp", ""), e.get("event_type", ""), e.get("agent_name", ""))
                    not in events_before_keys
                ]
                
                turn_agents = [
                    e.get("agent_name") 
                    for e in new_events 
                    if e.get("event_type") == "agent_started" and e.get("agent_name")
                ]
                agents_called.extend(turn_agents)
                
                # Extrair última mensagem do sistema
                system_response = None
                if result.get("messages"):
                    last_msg = result["messages"][-1]
                    if isinstance(last_msg, AIMessage):
                        system_response = last_msg.content
                
                # Salvar resultado do turno
                turns_result.append({
                    "turn": current_turn,
                    "user_input": content,
                    "system_response": system_response,
                    "next_step": result.get("next_step"),
                    "focal_argument": result.get("focal_argument"),
                    "agents_called": turn_agents,
                    "duration": duration
                })
                
                # Atualizar estado para próximo turno
                state = result
        
        # Coletar métricas finais
        metrics = self._collect_metrics(session_id)
        
        # Validar comportamento esperado
        validation_errors = self._validate_scenario(
            scenario, 
            agents_called, 
            state
        )
        
        return {
            "scenario_id": scenario.id,
            "session_id": session_id,
            "turns": turns_result,
            "final_state": state,
            "agents_called": list(set(agents_called)),  # Únicos
            "metrics": metrics,
            "success": len(validation_errors) == 0,
            "validation_errors": validation_errors
        }
    
    def _get_all_events(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Obtém todos os eventos de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Lista de eventos
        """
        return self.event_bus.get_session_events(session_id)
    
    def _get_agents_from_events(
        self, 
        session_id: str, 
        turn: int
    ) -> List[str]:
        """
        Extrai agentes chamados em um turno específico via EventBus.
        
        Args:
            session_id: ID da sessão
            turn: Número do turno atual
            
        Returns:
            Lista de nomes de agentes chamados
        """
        events = self._get_all_events(session_id)
        
        agents = []
        for event in events:
            if event.get("event_type") == "agent_started":
                agents.append(event.get("agent_name"))
        
        return agents
    
    def _collect_metrics(self, session_id: str) -> Dict[str, Any]:
        """
        Coleta métricas agregadas da execução.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Dict com total_tokens, total_cost, total_duration
        """
        events = self._get_all_events(session_id)
        
        total_tokens = 0
        total_cost = 0.0
        total_duration = 0.0
        
        for event in events:
            if event.get("event_type") == "agent_completed":
                total_tokens += event.get("tokens_total", 0)
                total_cost += event.get("cost", 0.0)
                total_duration += event.get("duration", 0.0)
        
        return {
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "total_duration": total_duration
        }
    
    def _validate_scenario(
        self,
        scenario: ConversationScenario,
        agents_called: List[str],
        final_state: Dict
    ) -> List[str]:
        """
        Valida que cenário executou conforme esperado.
        
        Args:
            scenario: Cenário executado
            agents_called: Lista de agentes que foram chamados
            final_state: Estado final do sistema
            
        Returns:
            Lista de erros encontrados (vazia se tudo OK)
        """
        errors = []
        
        # Validar agentes esperados foram chamados
        expected_agents = set(scenario.expected_agents)
        actual_agents = set(agents_called)
        
        if expected_agents != actual_agents:
            missing = expected_agents - actual_agents
            extra = actual_agents - expected_agents
            
            if missing:
                errors.append(
                    f"Agentes esperados não foram chamados: {sorted(missing)}"
                )
            if extra:
                errors.append(
                    f"Agentes não esperados foram chamados: {sorted(extra)}"
                )
        
        # Validar estado final esperado
        for key, expected_value in scenario.expected_final_state.items():
            actual_value = self._get_nested_value(final_state, key)
            
            # Se expected_value é uma função (lambda), usar como validador
            if callable(expected_value):
                try:
                    if not expected_value(actual_value):
                        errors.append(
                            f"Validação falhou para {key}: "
                            f"valor obtido não passou no validador"
                        )
                except Exception as e:
                    errors.append(
                        f"Erro ao validar {key} com função: {e}"
                    )
            else:
                # Comparação direta
                if actual_value != expected_value:
                    errors.append(
                        f"Estado final divergente: {key} "
                        f"(esperado: {expected_value}, obtido: {actual_value})"
                    )
        
        return errors
    
    def _get_nested_value(self, state: Dict, key: str) -> Any:
        """
        Extrai valor de campo aninhado do estado.
        
        Suporta notação de ponto para campos aninhados:
        - "next_step" → state["next_step"]
        - "methodologist_output.status" → state["methodologist_output"]["status"]
        
        Args:
            state: Estado do sistema
            key: Chave (pode ser aninhada com ".")
            
        Returns:
            Valor do campo ou None se não existir
        """
        if "." not in key:
            return state.get(key)
        
        parts = key.split(".")
        value = state
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
            
            if value is None:
                return None
        
        return value

    # ========================================================================
    # Épico 13.6 - Validação de Detecções do Observer
    # ========================================================================

    def validate_observer_detections(
        self,
        session_id: str,
        expected_events: List[str] = None,
        expected_checkpoint: bool = None,
        expected_classification: str = None
    ) -> Dict[str, Any]:
        """
        Valida detecções do Observer para uma sessão (Épico 13.6).

        Este método analisa os eventos publicados pelo Observer durante
        a execução de um cenário e valida se correspondem às expectativas.

        Tipos de eventos de detecção:
        - variation_detected: Variação identificada (mesma essência)
        - direction_change_confirmed: Mudança real de direção
        - clarity_checkpoint: Checkpoint de clareza solicitado

        Args:
            session_id: ID da sessão a validar
            expected_events: Lista de event_types esperados (opcional)
            expected_checkpoint: Se espera checkpoint (opcional)
            expected_classification: Classificação esperada (variation/real_change)

        Returns:
            Dict com resultado da validação:
                - valid: bool - True se todas validações passaram
                - errors: List[str] - Erros encontrados
                - events_found: List[str] - Tipos de eventos encontrados
                - checkpoint_found: bool - Se checkpoint foi detectado
                - classification_found: str - Classificação encontrada

        Example:
            >>> result = executor.execute_scenario(scenario)
            >>> validation = executor.validate_observer_detections(
            ...     result["session_id"],
            ...     expected_events=["variation_detected"],
            ...     expected_checkpoint=False
            ... )
            >>> print(f"Valid: {validation['valid']}")
            >>> if not validation['valid']:
            ...     print(f"Errors: {validation['errors']}")
        """
        events = self._get_all_events(session_id)

        # Filtrar apenas eventos de detecção do Observer
        detection_events = [
            e for e in events
            if e.get("event_type") in [
                "variation_detected",
                "direction_change_confirmed",
                "clarity_checkpoint"
            ]
        ]

        # Extrair informações dos eventos
        event_types = [e.get("event_type") for e in detection_events]

        checkpoint_found = any(
            et in ["direction_change_confirmed", "clarity_checkpoint"]
            for et in event_types
        )

        classification_found = None
        for e in detection_events:
            if e.get("classification"):
                classification_found = e.get("classification")
                break

        # Validações
        errors = []

        # Validar eventos esperados
        if expected_events is not None:
            for expected in expected_events:
                if expected not in event_types:
                    errors.append(
                        f"Evento esperado '{expected}' não encontrado. "
                        f"Eventos encontrados: {event_types}"
                    )

        # Validar checkpoint
        if expected_checkpoint is not None:
            if expected_checkpoint and not checkpoint_found:
                errors.append(
                    "Checkpoint esperado mas NÃO encontrado. "
                    f"Eventos: {event_types}"
                )
            elif not expected_checkpoint and checkpoint_found:
                errors.append(
                    "Checkpoint NÃO esperado mas encontrado. "
                    f"Eventos: {event_types}"
                )

        # Validar classificação
        if expected_classification is not None and classification_found:
            if expected_classification != classification_found:
                errors.append(
                    f"Classificação esperada '{expected_classification}', "
                    f"obtida '{classification_found}'"
                )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "events_found": event_types,
            "detection_events": detection_events,
            "checkpoint_found": checkpoint_found,
            "classification_found": classification_found
        }

    def get_detection_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Retorna resumo das detecções do Observer para uma sessão.

        Útil para debugging e relatórios de validação.

        Args:
            session_id: ID da sessão

        Returns:
            Dict com resumo:
                - total_detections: int
                - variations: int
                - direction_changes: int
                - clarity_checkpoints: int
                - events: List[Dict] - Eventos detalhados
        """
        events = self._get_all_events(session_id)

        detection_events = [
            e for e in events
            if e.get("event_type") in [
                "variation_detected",
                "direction_change_confirmed",
                "clarity_checkpoint"
            ]
        ]

        variations = len([
            e for e in detection_events
            if e.get("event_type") == "variation_detected"
        ])
        direction_changes = len([
            e for e in detection_events
            if e.get("event_type") == "direction_change_confirmed"
        ])
        clarity_checkpoints = len([
            e for e in detection_events
            if e.get("event_type") == "clarity_checkpoint"
        ])

        return {
            "total_detections": len(detection_events),
            "variations": variations,
            "direction_changes": direction_changes,
            "clarity_checkpoints": clarity_checkpoints,
            "events": detection_events
        }

