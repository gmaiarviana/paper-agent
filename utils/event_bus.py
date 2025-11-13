"""
EventBus para comunicação entre CLI/Graph e Dashboard (Épico 5.1).

Este módulo gerencia publicação e consumo de eventos usando arquivos JSON
temporários. Fornece canal de comunicação entre processo principal (CLI/Graph)
e Dashboard Streamlit.

Versão: 1.0
Data: 13/11/2025
"""

import json
import logging
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from utils.event_models import (
    EventType,
    AgentStartedEvent,
    AgentCompletedEvent,
    AgentErrorEvent,
    SessionStartedEvent,
    SessionCompletedEvent
)

logger = logging.getLogger(__name__)


class EventBus:
    r"""
    Barramento de eventos baseado em arquivos temporários.

    Publica eventos em arquivos JSON temporários que podem ser lidos pelo
    Dashboard Streamlit em tempo real. Cada sessão tem seu próprio arquivo.

    Estrutura do arquivo:
        {temp_dir}/paper-agent-events/events-{session_id}.json
        Onde {temp_dir} é:
        - Windows: C:\Users\{user}\AppData\Local\Temp\
        - Linux: /tmp/
        - Mac: /var/folders/.../

        Conteúdo:
        {
            "session_id": "cli-session-abc123",
            "events": [
                {...},  # AgentStartedEvent
                {...},  # AgentCompletedEvent
                ...
            ]
        }

    Example:
        >>> bus = EventBus()
        >>> bus.publish_agent_started("session-1", "orchestrator")
        >>> bus.publish_agent_completed(
        ...     "session-1", "orchestrator",
        ...     summary="Classificou como vague",
        ...     tokens_input=100, tokens_output=50
        ... )
        >>> events = bus.get_session_events("session-1")
        >>> len(events)
        2
    """

    def __init__(self, events_dir: Optional[Path] = None):
        """
        Inicializa EventBus.

        Args:
            events_dir (Path, optional): Diretório para armazenar eventos.
                Default: {temp_dir}/paper-agent-events (multiplataforma)
        """
        if events_dir is None:
            # Usar diretório temp do sistema operacional (funciona em Windows, Linux, Mac)
            system_temp = Path(tempfile.gettempdir())
            self.events_dir = system_temp / "paper-agent-events"
        else:
            self.events_dir = events_dir

        self.events_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"EventBus inicializado: {self.events_dir}")

    def _get_event_file(self, session_id: str) -> Path:
        """
        Retorna caminho do arquivo de eventos para uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            Path: Caminho do arquivo JSON
        """
        return self.events_dir / f"events-{session_id}.json"

    def _load_events(self, session_id: str) -> Dict[str, Any]:
        """
        Carrega eventos existentes de uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            Dict: Estrutura {"session_id": str, "events": list}
        """
        file_path = self._get_event_file(session_id)

        if not file_path.exists():
            return {
                "session_id": session_id,
                "events": []
            }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Erro ao carregar eventos de {session_id}: {e}")
            return {
                "session_id": session_id,
                "events": []
            }

    def _save_events(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Salva eventos no arquivo da sessão.

        Args:
            session_id (str): ID da sessão
            data (Dict): Estrutura {"session_id": str, "events": list}
        """
        file_path = self._get_event_file(session_id)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Erro ao salvar eventos de {session_id}: {e}")

    def publish_event(self, event: EventType) -> None:
        """
        Publica um evento genérico.

        Args:
            event (EventType): Evento Pydantic a ser publicado

        Example:
            >>> bus = EventBus()
            >>> event = AgentStartedEvent(
            ...     session_id="session-1",
            ...     agent_name="orchestrator"
            ... )
            >>> bus.publish_event(event)
        """
        session_id = event.session_id
        data = self._load_events(session_id)
        data["events"].append(event.model_dump())
        self._save_events(session_id, data)
        logger.debug(f"Evento publicado: {event.event_type} para {session_id}")

    def publish_agent_started(
        self,
        session_id: str,
        agent_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de início de agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente (orchestrator, structurer, methodologist)
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_started("session-1", "orchestrator")
        """
        event = AgentStartedEvent(
            session_id=session_id,
            agent_name=agent_name,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_agent_completed(
        self,
        session_id: str,
        agent_name: str,
        summary: str,
        tokens_input: int = 0,
        tokens_output: int = 0,
        tokens_total: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de conclusão de agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente
            summary (str): Resumo da ação (até 280 chars)
            tokens_input (int): Tokens de entrada
            tokens_output (int): Tokens de saída
            tokens_total (int): Total de tokens
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_completed(
            ...     "session-1", "orchestrator",
            ...     summary="Classificou como vague",
            ...     tokens_input=100, tokens_output=50, tokens_total=150
            ... )
        """
        event = AgentCompletedEvent(
            session_id=session_id,
            agent_name=agent_name,
            summary=summary,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_total=tokens_total,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_agent_error(
        self,
        session_id: str,
        agent_name: str,
        error_message: str,
        error_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de erro em agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente
            error_message (str): Mensagem de erro
            error_type (str, optional): Tipo do erro
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_error(
            ...     "session-1", "methodologist",
            ...     error_message="API timeout",
            ...     error_type="TimeoutError"
            ... )
        """
        event = AgentErrorEvent(
            session_id=session_id,
            agent_name=agent_name,
            error_message=error_message,
            error_type=error_type,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_session_started(
        self,
        session_id: str,
        user_input: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de início de sessão.

        Args:
            session_id (str): ID da sessão
            user_input (str): Input inicial do usuário
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_session_started(
            ...     "session-1",
            ...     "Observei que LLMs aumentam produtividade"
            ... )
        """
        event = SessionStartedEvent(
            session_id=session_id,
            user_input=user_input,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_session_completed(
        self,
        session_id: str,
        final_status: str,
        tokens_total: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de conclusão de sessão.

        Args:
            session_id (str): ID da sessão
            final_status (str): Status final (approved, rejected, etc)
            tokens_total (int): Total de tokens consumidos
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_session_completed(
            ...     "session-1", "approved",
            ...     tokens_total=850
            ... )
        """
        event = SessionCompletedEvent(
            session_id=session_id,
            final_status=final_status,
            tokens_total=tokens_total,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def get_session_events(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Obtém lista de eventos de uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            List[Dict]: Lista de eventos em formato dict

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_started("session-1", "orchestrator")
            >>> events = bus.get_session_events("session-1")
            >>> len(events)
            1
            >>> events[0]["event_type"]
            'agent_started'
        """
        data = self._load_events(session_id)
        return data.get("events", [])

    def list_active_sessions(self, max_age_minutes: Optional[int] = 60) -> List[str]:
        """
        Lista IDs de sessões ativas (com eventos recentes).

        Args:
            max_age_minutes (int, optional): Idade máxima em minutos para considerar
                sessão como ativa. None = listar todas. Default: 60 minutos.

        Returns:
            List[str]: Lista de session IDs ordenados do mais recente para o mais antigo

        Example:
            >>> bus = EventBus()
            >>> bus.publish_session_started("session-1", "Test 1")
            >>> bus.publish_session_started("session-2", "Test 2")
            >>> sessions = bus.list_active_sessions(max_age_minutes=10)
            >>> "session-1" in sessions
            True
        """
        if not self.events_dir.exists():
            return []

        sessions_with_time = []
        now = datetime.now(timezone.utc)

        for file_path in self.events_dir.glob("events-*.json"):
            # Extrair session_id do nome do arquivo: events-{session_id}.json
            session_id = file_path.stem.replace("events-", "")

            # Obter timestamp do último evento
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                events = data.get('events', [])
                if not events:
                    continue

                # Último evento
                last_event = events[-1]
                last_time_str = last_event.get('timestamp', '')
                last_time = datetime.fromisoformat(last_time_str.replace('Z', '+00:00'))

                # Calcular idade em minutos
                age_minutes = (now - last_time).total_seconds() / 60

                # Filtrar por idade se especificado
                if max_age_minutes is None or age_minutes <= max_age_minutes:
                    sessions_with_time.append((session_id, last_time))

            except Exception as e:
                logger.warning(f"Erro ao ler sessão {session_id}: {e}")
                continue

        # Ordenar do mais recente para o mais antigo
        sessions_with_time.sort(key=lambda x: x[1], reverse=True)

        # Retornar apenas os IDs
        return [session_id for session_id, _ in sessions_with_time]

    def clear_session(self, session_id: str) -> bool:
        """
        Remove arquivo de eventos de uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            bool: True se arquivo foi removido, False se não existia

        Example:
            >>> bus = EventBus()
            >>> bus.publish_session_started("session-1", "Test")
            >>> bus.clear_session("session-1")
            True
            >>> bus.clear_session("session-1")
            False
        """
        file_path = self._get_event_file(session_id)

        if file_path.exists():
            file_path.unlink()
            logger.debug(f"Arquivo de eventos removido: {session_id}")
            return True

        return False

    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém resumo de uma sessão (primeiro e último evento, total de eventos).

        Args:
            session_id (str): ID da sessão

        Returns:
            Dict | None: Resumo da sessão ou None se não existir

        Example:
            >>> bus = EventBus()
            >>> bus.publish_session_started("s1", "Test")
            >>> bus.publish_session_completed("s1", "approved", 500)
            >>> summary = bus.get_session_summary("s1")
            >>> summary["total_events"]
            2
            >>> summary["status"]
            'active'
        """
        events = self.get_session_events(session_id)

        if not events:
            return None

        first_event = events[0]
        last_event = events[-1]

        # Determinar status da sessão
        if last_event.get("event_type") == "session_completed":
            status = "completed"
            final_status = last_event.get("final_status", "unknown")
        else:
            status = "active"
            final_status = None

        return {
            "session_id": session_id,
            "total_events": len(events),
            "status": status,
            "final_status": final_status,
            "started_at": first_event.get("timestamp"),
            "last_event_at": last_event.get("timestamp"),
            "user_input": first_event.get("user_input") if first_event.get("event_type") == "session_started" else None
        }


# Instância global do EventBus (singleton pattern)
_event_bus_instance: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """
    Retorna instância global do EventBus (singleton).

    Returns:
        EventBus: Instância única do EventBus

    Example:
        >>> bus1 = get_event_bus()
        >>> bus2 = get_event_bus()
        >>> bus1 is bus2
        True
    """
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = EventBus()
    return _event_bus_instance
