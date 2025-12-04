"""
Métodos de leitura de eventos do EventBus.

Este módulo contém todos os métodos get_* e list_* que leem eventos
do barramento de eventos.
"""

import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class EventBusReaders:
    """
    Mixin com métodos de leitura de eventos.

    Adiciona métodos get_* e list_* à classe EventBus.
    """

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

