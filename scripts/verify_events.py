#!/usr/bin/env python3
"""Script para verificar se eventos foram salvos corretamente."""

import sys
from pathlib import Path
import json

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.event_bus import get_event_bus

def main():
    bus = get_event_bus()

    print("=" * 70)
    print("VERIFICAÇÃO DE EVENTOS SALVOS")
    print("=" * 70)
    print()

    print(f"📁 Diretório de eventos: {bus.events_dir}")
    print(f"   Existe? {bus.events_dir.exists()}")
    print()

    if not bus.events_dir.exists():
        print("❌ Diretório não existe!")
        return

    # Listar arquivos
    event_files = list(bus.events_dir.glob("events-*.json"))
    print(f"📋 Total de arquivos: {len(event_files)}")
    print()

    if not event_files:
        print("⚠️  Nenhum arquivo de evento encontrado!")
        print()
        print("Possíveis causas:")
        print("1. CLI não está salvando eventos")
        print("2. Eventos estão em outro diretório")
        print("3. Dashboard está lendo de diretório diferente")
        return

    # Mostrar detalhes de cada sessão
    print("SESSÕES ENCONTRADAS:")
    print("-" * 70)

    for idx, file_path in enumerate(sorted(event_files, key=lambda f: f.stat().st_mtime, reverse=True), 1):
        session_id = file_path.stem.replace("events-", "")
        short_id = session_id.replace('cli-session-', '')[:8]

        # Ler arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        events = data.get('events', [])

        # Obter user_input do primeiro evento
        user_input = "N/A"
        for event in events:
            if event.get('event_type') == 'session_started':
                user_input = event.get('user_input', 'N/A')
                break

        # Contar tipos
        event_types = {}
        for event in events:
            et = event.get('event_type', 'unknown')
            event_types[et] = event_types.get(et, 0) + 1

        # Exibir
        print(f"{idx}. Session: {short_id}")
        print(f"   Input: {user_input[:60]}")
        print(f"   Total eventos: {len(events)}")
        print(f"   Breakdown:")
        for et, count in sorted(event_types.items()):
            print(f"      - {et}: {count}")
        print()

    print("=" * 70)

if __name__ == "__main__":
    main()
