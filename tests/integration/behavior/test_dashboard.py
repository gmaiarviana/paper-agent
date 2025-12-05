#!/usr/bin/env python3
"""
Script de validação manual para Dashboard Streamlit (Épico 5.1).

Valida que o fluxo completo de eventos foi implementado corretamente:
- EventBus publica eventos
- Eventos são salvos em arquivos temporários
- Dashboard pode consumir eventos

Versão: 1.0
Data: 13/11/2025
"""

import sys
import time
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.event_bus import EventBus
from datetime import datetime


def print_header():
    """Exibe cabeçalho do script."""
    print("=" * 70)
    print("VALIDAÇÃO DO DASHBOARD STREAMLIT (Épico 5.1)")
    print("=" * 70)
    print()


def validate_event_bus():
    """Valida publicação básica de eventos."""
    print("1. Testando EventBus...")

    bus = EventBus()
    session_id = "test-validation-session"

    # Limpar sessão antiga se existir
    bus.clear_session(session_id)

    # Publicar eventos de teste
    bus.publish_session_started(session_id, "Test hypothesis for validation")
    bus.publish_agent_started(session_id, "orchestrator")
    time.sleep(0.5)
    bus.publish_agent_completed(
        session_id, "orchestrator",
        summary="Classificou como vague",
        tokens_input=100, tokens_output=50, tokens_total=150
    )
    bus.publish_agent_started(session_id, "structurer")
    time.sleep(0.5)
    bus.publish_agent_completed(
        session_id, "structurer",
        summary="Estruturou questão V1",
        tokens_total=200
    )
    bus.publish_agent_started(session_id, "methodologist")
    time.sleep(0.5)
    bus.publish_agent_completed(
        session_id, "methodologist",
        summary="Decisão: approved",
        tokens_total=300
    )
    bus.publish_session_completed(session_id, "approved", tokens_total=650)

    # Validar eventos
    events = bus.get_session_events(session_id)
    assert len(events) == 8, f"Esperado 8 eventos, encontrado {len(events)}"

    print("   ✅ EventBus funcionando corretamente")
    print(f"   ✅ {len(events)} eventos publicados com sucesso\n")

    return session_id, bus


def validate_session_summary(session_id, bus):
    """Valida resumo de sessão."""
    print("2. Testando resumo de sessão...")

    summary = bus.get_session_summary(session_id)

    assert summary is not None, "Summary não deve ser None"
    assert summary["session_id"] == session_id
    assert summary["status"] == "completed"
    assert summary["final_status"] == "approved"
    assert summary["total_events"] == 8
    assert summary["user_input"] == "Test hypothesis for validation"

    print("   ✅ Resumo de sessão correto")
    print(f"   ✅ Status: {summary['status']}")
    print(f"   ✅ Resultado final: {summary['final_status']}")
    print(f"   ✅ Total de eventos: {summary['total_events']}\n")


def validate_active_sessions(bus):
    """Valida listagem de sessões ativas."""
    print("3. Testando listagem de sessões ativas...")

    sessions = bus.list_active_sessions()

    assert len(sessions) > 0, "Deve haver pelo menos 1 sessão ativa"
    print(f"   ✅ {len(sessions)} sessão(ões) ativa(s) encontrada(s)")

    for sess_id in sessions:
        print(f"   📋 {sess_id}")

    print()


def validate_event_types(session_id, bus):
    """Valida que todos os tipos de evento foram criados."""
    print("4. Testando tipos de eventos...")

    events = bus.get_session_events(session_id)
    event_types = set(e["event_type"] for e in events)

    expected_types = {
        "session_started",
        "agent_started",
        "agent_completed",
        "session_completed"
    }

    assert expected_types.issubset(event_types), f"Tipos faltando: {expected_types - event_types}"

    print("   ✅ Todos os tipos de evento presentes:")
    for event_type in sorted(event_types):
        count = sum(1 for e in events if e["event_type"] == event_type)
        print(f"      - {event_type}: {count}")

    print()


def validate_timeline_ordering(session_id, bus):
    """Valida que eventos estão em ordem cronológica."""
    print("5. Testando ordenação da timeline...")

    events = bus.get_session_events(session_id)

    timestamps = [e["timestamp"] for e in events]

    # Verificar ordem crescente
    for i in range(len(timestamps) - 1):
        assert timestamps[i] <= timestamps[i+1], f"Eventos fora de ordem: {timestamps[i]} > {timestamps[i+1]}"

    print("   ✅ Eventos em ordem cronológica correta")
    print(f"   ✅ Primeiro: {timestamps[0]}")
    print(f"   ✅ Último: {timestamps[-1]}\n")


def validate_file_persistence(session_id, bus):
    """Valida que eventos persistem em arquivo."""
    print("6. Testando persistência em arquivo...")

    # Verificar que arquivo existe
    file_path = bus._get_event_file(session_id)
    assert file_path.exists(), f"Arquivo não encontrado: {file_path}"

    print(f"   ✅ Arquivo criado: {file_path}")

    # Criar nova instância do EventBus
    bus2 = EventBus(events_dir=bus.events_dir)
    events2 = bus2.get_session_events(session_id)

    assert len(events2) == 8, "Eventos não persistiram corretamente"

    print("   ✅ Eventos persistem entre instâncias do EventBus\n")


def validate_dashboard_integration():
    """Valida que Dashboard pode ser importado."""
    print("7. Testando importação do Dashboard...")

    try:
        # Tentar importar módulo do dashboard
        sys.path.insert(0, str(project_root / "app"))
        import dashboard
        print("   ✅ Dashboard importado com sucesso\n")
    except ImportError as e:
        print(f"   ❌ Erro ao importar Dashboard: {e}\n")
        raise


def print_summary():
    """Exibe resumo final."""
    print("=" * 70)
    print("✅ TODAS AS VALIDAÇÕES PASSARAM!")
    print("=" * 70)
    print()
    print("📋 O que foi validado:")
    print("   ✅ EventBus publica e consome eventos corretamente")
    print("   ✅ Resumo de sessão funciona")
    print("   ✅ Listagem de sessões ativas funciona")
    print("   ✅ Todos os tipos de evento são suportados")
    print("   ✅ Timeline mantém ordem cronológica")
    print("   ✅ Eventos persistem em arquivo")
    print("   ✅ Dashboard pode ser importado")
    print()
    print("🚀 Próximos passos:")
    print("   1. Execute o Dashboard: streamlit run app/dashboard.py")
    print("   2. Execute o CLI em outro terminal: python cli/chat.py")
    print("   3. Veja os eventos aparecerem em tempo real no Dashboard!")
    print()
    print("=" * 70)


def main():
    """Função principal de validação."""
    try:
        print_header()

        session_id, bus = validate_event_bus()
        validate_session_summary(session_id, bus)
        validate_active_sessions(bus)
        validate_event_types(session_id, bus)
        validate_timeline_ordering(session_id, bus)
        validate_file_persistence(session_id, bus)
        validate_dashboard_integration()

        print_summary()

    except AssertionError as e:
        print(f"\n❌ ERRO: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
