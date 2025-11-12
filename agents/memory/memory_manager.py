"""
Gerenciador de memória dinâmica e contexto por agente (Épico 6).

Este módulo gerencia histórico de execuções de agentes com metadados
(tokens, summary, timestamp) de forma paralela ao MultiAgentState.

Versão: 1.0
Data: 12/11/2025
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict


@dataclass
class AgentExecution:
    """
    Representa uma execução de um agente com metadados.

    Attributes:
        agent_name (str): Nome do agente que executou
        tokens_input (int): Tokens de entrada consumidos
        tokens_output (int): Tokens de saída gerados
        tokens_total (int): Total de tokens (input + output)
        summary (str): Resumo curto da ação/decisão do agente
        timestamp (str): Timestamp ISO 8601 da execução
        metadata (dict): Metadados adicionais (opcional)
    """
    agent_name: str
    tokens_input: int
    tokens_output: int
    tokens_total: int
    summary: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converte execução para dicionário."""
        return asdict(self)


class MemoryManager:
    """
    Gerenciador de memória dinâmica por agente e sessão.

    Esta classe mantém histórico de execuções de agentes organizadas por sessão,
    permitindo consultas, agregações e resets. Opera de forma independente do
    MultiAgentState do LangGraph.

    Estrutura interna:
        {
            "session-id-1": {
                "orchestrator": [AgentExecution, AgentExecution, ...],
                "structurer": [AgentExecution, ...],
                "methodologist": [AgentExecution, ...]
            },
            "session-id-2": { ... }
        }

    Example:
        >>> manager = MemoryManager()
        >>> manager.add_execution(
        ...     session_id="session-1",
        ...     agent_name="orchestrator",
        ...     tokens_input=100,
        ...     tokens_output=50,
        ...     summary="Classificou input como 'vague'"
        ... )
        >>> history = manager.get_agent_history("session-1", "orchestrator")
        >>> len(history)
        1
        >>> history[0].summary
        "Classificou input como 'vague'"
    """

    def __init__(self):
        """Inicializa MemoryManager com histórico vazio."""
        self._memory: Dict[str, Dict[str, List[AgentExecution]]] = {}

    def add_execution(
        self,
        session_id: str,
        agent_name: str,
        tokens_input: int,
        tokens_output: int,
        summary: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentExecution:
        """
        Adiciona registro de execução de um agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente
            tokens_input (int): Tokens de entrada
            tokens_output (int): Tokens de saída
            summary (str): Resumo da ação (até 280 chars recomendado)
            metadata (dict, optional): Metadados adicionais

        Returns:
            AgentExecution: Objeto de execução criado

        Example:
            >>> manager = MemoryManager()
            >>> execution = manager.add_execution(
            ...     session_id="test-session",
            ...     agent_name="methodologist",
            ...     tokens_input=500,
            ...     tokens_output=200,
            ...     summary="Aprovou hipótese com rigor científico adequado"
            ... )
            >>> execution.tokens_total
            700
        """
        # Criar registro de execução
        execution = AgentExecution(
            agent_name=agent_name,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_total=tokens_input + tokens_output,
            summary=summary,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            metadata=metadata or {}
        )

        # Inicializar estrutura se necessário
        if session_id not in self._memory:
            self._memory[session_id] = {}

        if agent_name not in self._memory[session_id]:
            self._memory[session_id][agent_name] = []

        # Adicionar execução ao histórico
        self._memory[session_id][agent_name].append(execution)

        return execution

    def get_agent_history(
        self,
        session_id: str,
        agent_name: str
    ) -> List[AgentExecution]:
        """
        Obtém histórico de execuções de um agente específico em uma sessão.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente

        Returns:
            List[AgentExecution]: Lista de execuções (vazia se não houver)

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "Ação 1")
            >>> manager.add_execution("s1", "orchestrator", 150, 75, "Ação 2")
            >>> history = manager.get_agent_history("s1", "orchestrator")
            >>> len(history)
            2
        """
        if session_id not in self._memory:
            return []

        if agent_name not in self._memory[session_id]:
            return []

        return self._memory[session_id][agent_name]

    def get_session_history(self, session_id: str) -> Dict[str, List[AgentExecution]]:
        """
        Obtém histórico completo de uma sessão (todos os agentes).

        Args:
            session_id (str): ID da sessão

        Returns:
            Dict[str, List[AgentExecution]]: Dicionário mapeando agente para execuções

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "Classificou")
            >>> manager.add_execution("s1", "methodologist", 200, 100, "Aprovou")
            >>> history = manager.get_session_history("s1")
            >>> len(history)
            2
            >>> "orchestrator" in history
            True
        """
        if session_id not in self._memory:
            return {}

        return self._memory[session_id]

    def get_session_totals(self, session_id: str) -> Dict[str, int]:
        """
        Calcula totais de tokens por agente e total geral de uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            Dict[str, int]: Totais de tokens por agente + "total"

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "A1")
            >>> manager.add_execution("s1", "orchestrator", 200, 100, "A2")
            >>> manager.add_execution("s1", "methodologist", 300, 150, "A3")
            >>> totals = manager.get_session_totals("s1")
            >>> totals["orchestrator"]
            450
            >>> totals["methodologist"]
            450
            >>> totals["total"]
            900
        """
        if session_id not in self._memory:
            return {"total": 0}

        totals: Dict[str, int] = {}
        grand_total = 0

        for agent_name, executions in self._memory[session_id].items():
            agent_total = sum(ex.tokens_total for ex in executions)
            totals[agent_name] = agent_total
            grand_total += agent_total

        totals["total"] = grand_total
        return totals

    def reset_session(self, session_id: str) -> bool:
        """
        Limpa histórico de uma sessão específica.

        Args:
            session_id (str): ID da sessão a ser limpa

        Returns:
            bool: True se sessão foi limpa, False se não existia

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "Ação")
            >>> manager.reset_session("s1")
            True
            >>> manager.get_session_history("s1")
            {}
        """
        if session_id in self._memory:
            del self._memory[session_id]
            return True
        return False

    def reset_all(self) -> int:
        """
        Limpa histórico de todas as sessões.

        Returns:
            int: Número de sessões que foram limpas

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "A1")
            >>> manager.add_execution("s2", "methodologist", 200, 100, "A2")
            >>> count = manager.reset_all()
            >>> count
            2
            >>> len(manager._memory)
            0
        """
        count = len(self._memory)
        self._memory.clear()
        return count

    def get_latest_execution(
        self,
        session_id: str,
        agent_name: str
    ) -> Optional[AgentExecution]:
        """
        Obtém a execução mais recente de um agente em uma sessão.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente

        Returns:
            AgentExecution | None: Última execução ou None se não houver

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "Primeira")
            >>> manager.add_execution("s1", "orchestrator", 200, 100, "Segunda")
            >>> latest = manager.get_latest_execution("s1", "orchestrator")
            >>> latest.summary
            'Segunda'
        """
        history = self.get_agent_history(session_id, agent_name)
        if not history:
            return None
        return history[-1]

    def list_sessions(self) -> List[str]:
        """
        Lista IDs de todas as sessões ativas.

        Returns:
            List[str]: Lista de session IDs

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "A1")
            >>> manager.add_execution("s2", "methodologist", 200, 100, "A2")
            >>> sessions = manager.list_sessions()
            >>> len(sessions)
            2
            >>> "s1" in sessions
            True
        """
        return list(self._memory.keys())

    def export_session_as_dict(self, session_id: str) -> Dict[str, Any]:
        """
        Exporta histórico de uma sessão como dicionário JSON-serializável.

        Args:
            session_id (str): ID da sessão

        Returns:
            Dict[str, Any]: Histórico completo da sessão

        Example:
            >>> manager = MemoryManager()
            >>> manager.add_execution("s1", "orchestrator", 100, 50, "Classificou")
            >>> export = manager.export_session_as_dict("s1")
            >>> export["session_id"]
            's1'
            >>> "orchestrator" in export["agents"]
            True
        """
        if session_id not in self._memory:
            return {
                "session_id": session_id,
                "agents": {},
                "totals": {"total": 0}
            }

        # Converter execuções para dicts
        agents = {}
        for agent_name, executions in self._memory[session_id].items():
            agents[agent_name] = [ex.to_dict() for ex in executions]

        return {
            "session_id": session_id,
            "agents": agents,
            "totals": self.get_session_totals(session_id)
        }
