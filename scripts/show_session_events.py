#!/usr/bin/env python3
"""Script rápido para mostrar eventos de uma sessão."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.event_bus import get_event_bus

def main():
    bus = get_event_bus()

    print("=" * 70)
    print("SESSÕES DISPONÍVEIS")
    print("=" * 70)

    # Listar todas as sessões (sem filtro de idade)
    all_sessions = []
    if bus.events_dir.exists():
        for file_path in bus.events_dir.glob("events-*.json"):
            session_id = file_path.stem.replace("events-", "")
            all_sessions.append(session_id)

    if not all_sessions:
        print("Nenhuma sessão encontrada.")
        return

    print(f"Total: {len(all_sessions)} sessões\n")

    # Mostrar resumo de cada sessão
    for idx, session_id in enumerate(all_sessions, 1):
        summary = bus.get_session_summary(session_id)
        events = bus.get_session_events(session_id)

        short_id = session_id.replace('cli-session-', '')[:8]
        user_input = summary.get('user_input', 'N/A')[:50]

        print(f"{idx}. Session: {short_id}")
        print(f"   Input: {user_input}")
        print(f"   Eventos: {len(events)}")
        print(f"   Status: {summary.get('status', 'unknown')}")

        # Contar tipos de evento
        event_types = {}
        for event in events:
            event_type = event.get('event_type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1

        print(f"   Breakdown: {event_types}")
        print()

if __name__ == "__main__":
    main()
