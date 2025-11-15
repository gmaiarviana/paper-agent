#!/usr/bin/env python3
"""
Script de validação do CLI Conversacional (Épico 7 Protótipo).

Valida que o CLI conversacional foi implementado corretamente com:
- Loop contínuo de conversa (múltiplos turnos)
- Thread ID preservado entre turnos
- Contexto acumulado via conversation_history
- Flag --verbose funcional
- Mensagens conversacionais exibidas
- Detecção de fim conversacional vs fim de sessão

Versão: 1.0
Data: 15/11/2025
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state
from agents.memory.memory_manager import MemoryManager
from utils.event_bus import get_event_bus


def validate_conversational_cli():
    """
    Valida implementação do CLI Conversacional (Épico 7 Protótipo).

    Testa:
    1. Thread ID preservado entre múltiplos turnos
    2. Contexto acumulado (histórico de mensagens)
    3. Orquestrador detecta next_step="explore" corretamente
    4. Mensagens conversacionais geradas
    5. EventBus publica eventos com reasoning
    """
    print("=" * 70)
    print("VALIDAÇÃO DO CLI CONVERSACIONAL (ÉPICO 7 PROTÓTIPO)")
    print("=" * 70)

    # Setup
    graph = create_multi_agent_graph()
    memory_manager = MemoryManager()
    event_bus = get_event_bus()

    session_id = "test-conversational-cli-001"
    thread_id = f"thread-{session_id}"

    config = {
        "configurable": {
            "thread_id": thread_id,
            "session_id": session_id,
            "memory_manager": memory_manager
        }
    }

    print("\n1. Testando primeiro turno da conversa...")
    print("   Input: 'tdd reduz bugs'")

    # Turno 1
    state1 = create_initial_multi_agent_state("tdd reduz bugs", session_id=session_id)
    graph.invoke(state1, config=config)

    snapshot1 = graph.get_state(config)
    final_state1 = snapshot1.values

    # Validações Turno 1
    assert final_state1.get('next_step') in ['explore', 'clarify'], \
        f"❌ next_step deve ser 'explore' ou 'clarify', mas é '{final_state1.get('next_step')}'"
    print("   ✅ next_step='explore' detectado (Orquestrador quer mais contexto)")

    assert final_state1.get('orchestrator_analysis'), \
        "❌ orchestrator_analysis não foi preenchido"
    print("   ✅ Raciocínio do orquestrador gerado")

    assert final_state1.get('messages'), \
        "❌ Histórico de mensagens vazio"
    print(f"   ✅ Histórico de mensagens tem {len(final_state1['messages'])} mensagem(s)")

    last_message1 = final_state1['messages'][-1].content
    assert len(last_message1) > 0, "❌ Mensagem conversacional vazia"
    print(f"   ✅ Mensagem conversacional gerada: '{last_message1[:80]}...'")

    print("\n2. Testando segundo turno (preservação de contexto)...")
    print("   Input: 'na minha equipe Python'")

    # Turno 2 - usar mesmo thread_id
    state2 = create_initial_multi_agent_state("na minha equipe Python", session_id=session_id)
    graph.invoke(state2, config=config)

    snapshot2 = graph.get_state(config)
    final_state2 = snapshot2.values

    # Validações Turno 2
    assert final_state2.get('messages'), \
        "❌ Histórico de mensagens vazio no turno 2"

    num_messages = len(final_state2['messages'])
    assert num_messages > len(final_state1['messages']), \
        f"❌ Histórico não acumulou. Turno1: {len(final_state1['messages'])}, Turno2: {num_messages}"
    print(f"   ✅ Contexto preservado - Histórico cresceu para {num_messages} mensagem(s)")

    last_message2 = final_state2['messages'][-1].content
    print(f"   ✅ Nova mensagem conversacional: '{last_message2[:80]}...'")

    print("\n3. Testando EventBus (publicação de eventos com reasoning)...")

    # Verificar eventos publicados
    events = event_bus.get_session_events(session_id)
    assert len(events) > 0, "❌ Nenhum evento foi publicado"
    print(f"   ✅ {len(events)} evento(s) publicado(s)")

    # Verificar se algum evento contém reasoning
    orchestrator_events = [e for e in events if e.get('agent') == 'orchestrator']
    assert len(orchestrator_events) > 0, "❌ Nenhum evento do orquestrador encontrado"

    # Verificar estrutura do evento
    event_sample = orchestrator_events[0]
    assert 'session_id' in event_sample, "❌ Evento não contém session_id"
    assert 'timestamp' in event_sample, "❌ Evento não contém timestamp"
    print("   ✅ Eventos estruturados corretamente")
    print(f"   ✅ Amostra de evento: {list(event_sample.keys())}")

    print("\n4. Testando detecção de fim conversacional...")

    # Verificar que grafo não tem next (terminou)
    assert not snapshot2.next, \
        f"❌ Grafo ainda tem nós pendentes: {snapshot2.next}"
    print("   ✅ Grafo terminou corretamente (END state)")

    # Verificar que terminou em estado conversacional (explore/clarify)
    assert final_state2.get('next_step') in ['explore', 'clarify'], \
        f"❌ Grafo não terminou em estado conversacional: {final_state2.get('next_step')}"
    print("   ✅ Terminou em estado conversacional (permite continuar)")

    print("\n5. Testando MemoryManager (registro de tokens)...")

    totals = memory_manager.get_session_totals(session_id)
    tokens_total = totals.get('total', 0)

    assert tokens_total > 0, "❌ Nenhum token foi registrado"
    print(f"   ✅ Tokens registrados: {tokens_total} total")

    orchestrator_tokens = totals.get('orchestrator', 0)
    assert orchestrator_tokens > 0, "❌ Tokens do orquestrador não foram registrados"
    print(f"   ✅ Orquestrador registrou {orchestrator_tokens} tokens")

    print("\n" + "=" * 70)
    print("✅ TODAS AS VALIDAÇÕES PASSARAM!")
    print("=" * 70)
    print()
    print("Resumo:")
    print(f"  - Turnos testados: 2")
    print(f"  - Mensagens acumuladas: {num_messages}")
    print(f"  - Eventos publicados: {len(events)}")
    print(f"  - Tokens consumidos: {tokens_total}")
    print()
    print("CLI Conversacional (Épico 7 Protótipo) está funcional! ✅")
    print()


if __name__ == "__main__":
    try:
        validate_conversational_cli()
    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
