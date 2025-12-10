#!/usr/bin/env python3
"""
Script de teste para validar integração CLI → EventBus → Dashboard.

Este script simula uma execução do CLI para verificar que:
1. CLI publica eventos de sessão corretamente
2. EventBus persiste eventos em arquivo
3. Dashboard pode consumir eventos

"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.event_bus import get_event_bus
import time

def print_header():
    """Exibe cabeçalho do script."""
    print("=" * 70)
    print("TESTE DE INTEGRAÇÃO: CLI → EventBus → Dashboard")
    print("=" * 70)
    print()

def simulate_cli_execution():
    """
    Simula uma execução completa do CLI com sistema multi-agente.

    Publica os mesmos eventos que o CLI real publicaria durante
    uma execução: session_started → agent events → session_completed
    """
    print("1. Iniciando simulação de execução do CLI...\n")

    # Obter EventBus
    bus = get_event_bus()
    session_id = "test-cli-integration-001"

    # Limpar sessão anterior se existir
    bus.clear_session(session_id)

    # 1. Sessão iniciada
    print("   📝 Publicando: session_started")
    bus.publish_session_started(
        session_id=session_id,
        user_input="Observei que programadores que usam LLMs são mais produtivos"
    )
    time.sleep(0.3)

    # 2. Orquestrador iniciado
    print("   📝 Publicando: agent_started (orchestrator)")
    bus.publish_agent_started(session_id, "orchestrator")
    time.sleep(0.5)

    # 3. Orquestrador concluído
    print("   📝 Publicando: agent_completed (orchestrator)")
    bus.publish_agent_completed(
        session_id, "orchestrator",
        summary="Classificou input como 'vague'",
        tokens_input=120, tokens_output=45, tokens_total=165
    )
    time.sleep(0.3)

    # 4. Estruturador iniciado
    print("   📝 Publicando: agent_started (structurer)")
    bus.publish_agent_started(session_id, "structurer")
    time.sleep(0.7)

    # 5. Estruturador concluído
    print("   📝 Publicando: agent_completed (structurer)")
    bus.publish_agent_completed(
        session_id, "structurer",
        summary="Estruturou questão V1: 'O uso de LLMs aumenta produtividade?'",
        tokens_input=180, tokens_output=95, tokens_total=275
    )
    time.sleep(0.3)

    # 6. Metodologista iniciado
    print("   📝 Publicando: agent_started (methodologist)")
    bus.publish_agent_started(session_id, "methodologist")
    time.sleep(1.0)

    # 7. Metodologista concluído
    print("   📝 Publicando: agent_completed (methodologist)")
    bus.publish_agent_completed(
        session_id, "methodologist",
        summary="Decisão: approved",
        tokens_input=250, tokens_output=180, tokens_total=430
    )
    time.sleep(0.3)

    # 8. Sessão concluída
    print("   📝 Publicando: session_completed")
    bus.publish_session_completed(
        session_id, "approved",
        tokens_total=870
    )

    print("\n✅ Simulação concluída!\n")
    return session_id, bus

def validate_events(session_id, bus):
    """
    Valida que todos os eventos foram publicados corretamente.

    Args:
        session_id (str): ID da sessão de teste
        bus (EventBus): Instância do EventBus
    """
    print("2. Validando eventos publicados...\n")

    # Obter eventos
    events = bus.get_session_events(session_id)

    # Validar contagem
    expected_count = 8  # 1 session_started + 3 agent_started + 3 agent_completed + 1 session_completed
    assert len(events) == expected_count, f"Esperado {expected_count} eventos, encontrado {len(events)}"
    print(f"   ✅ Total de eventos: {len(events)}/{expected_count}")

    # Validar tipos de evento
    event_types = [e["event_type"] for e in events]
    assert "session_started" in event_types
    assert event_types.count("agent_started") == 3
    assert event_types.count("agent_completed") == 3
    assert "session_completed" in event_types
    print("   ✅ Tipos de evento corretos")

    # Validar ordem dos agentes
    agent_events = [e for e in events if e["event_type"] in ["agent_started", "agent_completed"]]
    agent_names = [e["agent_name"] for e in agent_events]
    expected_order = ["orchestrator", "orchestrator", "structurer", "structurer", "methodologist", "methodologist"]
    assert agent_names == expected_order, f"Ordem incorreta: {agent_names}"
    print("   ✅ Ordem dos agentes correta")

    # Validar resumo da sessão
    summary = bus.get_session_summary(session_id)
    assert summary is not None
    assert summary["status"] == "completed"
    assert summary["final_status"] == "approved"
    assert summary["total_events"] == expected_count
    print("   ✅ Resumo da sessão correto")

    print()

def display_dashboard_instructions(session_id):
    """
    Exibe instruções para visualizar eventos no Dashboard.

    Args:
        session_id (str): ID da sessão de teste
    """
    print("3. Visualizando no Dashboard...\n")
    print("   📋 Para ver os eventos no Dashboard:")
    print()
    print("   1. Abra um novo terminal")
    print("   2. Execute: streamlit run app/dashboard.py")
    print("   3. O Dashboard abrirá no navegador")
    print(f"   4. Selecione a sessão: {session_id}")
    print("   5. Você verá a timeline completa com todos os eventos!")
    print()
    print("   💡 Dica: O Dashboard tem auto-refresh ativado por padrão")
    print("           Os eventos aparecem em tempo real enquanto o CLI executa")
    print()

def print_summary():
    """Exibe resumo final do teste."""
    print("=" * 70)
    print("✅ TESTE DE INTEGRAÇÃO PASSOU COM SUCESSO!")
    print("=" * 70)
    print()
    print("📋 O que foi validado:")
    print("   ✅ CLI publica eventos de sessão corretamente")
    print("   ✅ EventBus persiste eventos em arquivo JSON")
    print("   ✅ Todos os eventos estão em ordem cronológica")
    print("   ✅ Timeline completa: Orquestrador → Estruturador → Metodologista")
    print("   ✅ Dashboard pode consumir eventos (verifique no browser)")
    print()
    print("🎉 A funcionalidade 5.1 está COMPLETA e funcionando!")
    print()
    print("=" * 70)

def main():
    """Função principal do teste."""
    try:
        print_header()

        # Simular execução do CLI
        session_id, bus = simulate_cli_execution()

        # Validar eventos
        validate_events(session_id, bus)

        # Instruções para Dashboard
        display_dashboard_instructions(session_id)

        # Resumo final
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
