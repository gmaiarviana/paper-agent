#!/usr/bin/env python3
"""
Script de diagnóstico para verificar onde eventos estão sendo salvos.

Este script ajuda a debugar problemas com EventBus, especialmente no Windows
onde o caminho /tmp pode não funcionar como esperado.
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.event_bus import get_event_bus
import json


def main():
    print("=" * 70)
    print("DIAGNÓSTICO DE EVENTOS - EventBus")
    print("=" * 70)
    print()

    # Obter EventBus
    bus = get_event_bus()

    # Mostrar diretório de eventos
    print(f"📁 Diretório de eventos: {bus.events_dir}")
    print(f"   Existe? {bus.events_dir.exists()}")
    print()

    # Listar arquivos de eventos
    if bus.events_dir.exists():
        event_files = list(bus.events_dir.glob("events-*.json"))
        print(f"📋 Total de arquivos de eventos: {len(event_files)}")
        print()

        if event_files:
            print("Arquivos encontrados:")
            for file in sorted(event_files, key=lambda f: f.stat().st_mtime, reverse=True):
                # Ler arquivo
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                session_id = data.get('session_id', 'unknown')
                events = data.get('events', [])

                # Timestamp do último evento
                last_event_time = events[-1]['timestamp'] if events else 'N/A'

                print(f"   • {file.name}")
                print(f"     Session ID: {session_id}")
                print(f"     Eventos: {len(events)}")
                print(f"     Último evento: {last_event_time}")
                print()
        else:
            print("⚠️  Nenhum arquivo de evento encontrado!")
            print()
            print("Isso pode significar que:")
            print("   1. O CLI não está publicando eventos")
            print("   2. Os eventos estão sendo salvos em outro lugar")
            print("   3. Há problema de permissões de escrita")
            print()
    else:
        print("❌ Diretório de eventos não existe!")
        print()
        print(f"Tentando criar: {bus.events_dir}")
        try:
            bus.events_dir.mkdir(parents=True, exist_ok=True)
            print("✅ Diretório criado com sucesso!")
        except Exception as e:
            print(f"❌ Falha ao criar diretório: {e}")
        print()

    # Testar publicação de evento
    print("=" * 70)
    print("TESTE DE PUBLICAÇÃO")
    print("=" * 70)
    print()

    test_session = "diagnostic-test-session"
    print(f"Testando publicação de evento para sessão: {test_session}")

    try:
        bus.publish_session_started(test_session, "Teste de diagnóstico")
        print("✅ Evento publicado com sucesso!")

        # Verificar se arquivo foi criado
        test_file = bus.events_dir / f"events-{test_session}.json"
        if test_file.exists():
            print(f"✅ Arquivo criado: {test_file}")

            # Ler conteúdo
            with open(test_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"   Eventos no arquivo: {len(data.get('events', []))}")
        else:
            print(f"❌ Arquivo não foi criado: {test_file}")
    except Exception as e:
        print(f"❌ Erro ao publicar evento: {e}")
        import traceback
        traceback.print_exc()

    print()
    print("=" * 70)
    print("FIM DO DIAGNÓSTICO")
    print("=" * 70)


if __name__ == "__main__":
    main()
