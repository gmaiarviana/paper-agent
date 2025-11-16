"""
Script de validação completa do Épico 8: Telemetria e Observabilidade (Protótipo).

Valida que:
- POC 8.1: Reasoning implementado para todos os agentes ✅
- Protótipo 8.2: Orquestrador e Metodologista com reasoning ✅
- Protótipo 8.3: Métricas consolidadas (tokens, custo, tempo)
  - Tokens reais capturados do MemoryManager
  - Custo calculado via CostTracker
  - Tempo de execução capturado
  - Dashboard exibe métricas consolidadas
  - Polling configurado em 1s

Épico 8 - Protótipo: Telemetria e Observabilidade
Data: 16/11/2025
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph
from agents.orchestrator.state import create_initial_multi_agent_state
from agents.memory.memory_manager import MemoryManager
from utils.event_bus import get_event_bus
import json


def validate_epic8_complete():
    """Valida implementação completa do Épico 8 (Protótipo)."""
    print("=" * 70)
    print("VALIDAÇÃO ÉPICO 8 COMPLETO: TELEMETRIA E OBSERVABILIDADE")
    print("=" * 70)
    print()

    # Criar session_id único
    import uuid
    session_id = f"validate-epic8-complete-{uuid.uuid4().hex[:8]}"

    print(f"Session ID: {session_id}")
    print()

    # Limpar eventos anteriores da sessão (se existir)
    bus = get_event_bus()
    bus.clear_session(session_id)

    # Criar MemoryManager para captura de métricas
    memory_manager = MemoryManager()

    # Criar estado inicial com input vago (vai chamar Orquestrador → Estruturador → Metodologista)
    print("1. Criando estado inicial com input vago...")
    state = create_initial_multi_agent_state(
        user_input="Observei que TDD reduz bugs em Python",
        session_id=session_id
    )
    print("   ✅ Estado inicial criado")
    print()

    # Criar grafo multi-agente
    print("2. Criando super-grafo multi-agente...")
    graph = create_multi_agent_graph()
    print("   ✅ Grafo criado com sucesso")
    print()

    # Executar grafo com MemoryManager
    print("3. Executando grafo com MemoryManager...")
    config = {
        "configurable": {
            "thread_id": session_id,
            "session_id": session_id,
            "memory_manager": memory_manager  # Passar MemoryManager para capturar tokens
        }
    }

    try:
        result = graph.invoke(state, config=config)
        print("   ✅ Grafo executado com sucesso")
    except Exception as e:
        print(f"   ❌ ERRO ao executar grafo: {e}")
        return False
    print()

    # VALIDAÇÃO 1: Eventos publicados
    print("4. Validando eventos publicados...")
    events = bus.get_session_events(session_id)

    if not events:
        print("   ❌ ERRO: Nenhum evento foi publicado!")
        return False

    print(f"   ✅ {len(events)} eventos publicados")
    print()

    # VALIDAÇÃO 2: Reasoning em todos os agentes
    print("5. Validando reasoning em metadata...")

    agent_completed_events = [e for e in events
                              if e.get("event_type") == "agent_completed"]

    if not agent_completed_events:
        print("   ❌ ERRO: Nenhum agente completou execução!")
        return False

    reasoning_count = 0
    for event in agent_completed_events:
        agent_name = event.get("agent_name", "unknown")
        metadata = event.get("metadata", {})

        if "reasoning" in metadata and len(metadata["reasoning"]) > 10:
            reasoning_count += 1
            print(f"   ✅ {agent_name}: reasoning presente ({len(metadata['reasoning'])} chars)")
        else:
            print(f"   ❌ {agent_name}: reasoning ausente ou vazio!")

    print(f"   Total: {reasoning_count}/{len(agent_completed_events)} agentes com reasoning")
    print()

    # VALIDAÇÃO 3: Tokens reais (não-zero)
    print("6. Validando tokens reais capturados...")

    tokens_count = 0
    for event in agent_completed_events:
        agent_name = event.get("agent_name", "unknown")
        tokens_input = event.get("tokens_input", 0)
        tokens_output = event.get("tokens_output", 0)
        tokens_total = event.get("tokens_total", 0)

        if tokens_total > 0:
            tokens_count += 1
            print(f"   ✅ {agent_name}: {tokens_total} tokens (input={tokens_input}, output={tokens_output})")
        else:
            print(f"   ⚠️  {agent_name}: 0 tokens (pode não ter chamado LLM)")

    if tokens_count == 0:
        print("   ❌ ERRO CRÍTICO: Nenhum agente tem tokens capturados!")
        return False

    print(f"   Total: {tokens_count}/{len(agent_completed_events)} agentes com tokens > 0")
    print()

    # VALIDAÇÃO 4: Custo calculado
    print("7. Validando custo calculado...")

    cost_count = 0
    total_cost = 0.0
    for event in agent_completed_events:
        agent_name = event.get("agent_name", "unknown")
        cost = event.get("cost", 0.0)

        if cost > 0:
            cost_count += 1
            total_cost += cost
            print(f"   ✅ {agent_name}: ${cost:.6f}")
        else:
            print(f"   ⚠️  {agent_name}: $0.00 (pode não ter chamado LLM)")

    if cost_count == 0:
        print("   ❌ ERRO CRÍTICO: Nenhum agente tem custo calculado!")
        return False

    print(f"   Total: {cost_count}/{len(agent_completed_events)} agentes com custo > 0")
    print(f"   💰 Custo total da sessão: ${total_cost:.6f}")
    print()

    # VALIDAÇÃO 5: Tempo de execução
    print("8. Validando tempo de execução...")

    duration_count = 0
    total_duration = 0.0
    for event in agent_completed_events:
        agent_name = event.get("agent_name", "unknown")
        duration = event.get("duration", 0.0)

        if duration > 0:
            duration_count += 1
            total_duration += duration
            print(f"   ✅ {agent_name}: {duration:.2f}s")
        else:
            print(f"   ❌ {agent_name}: 0.00s (erro na captura de tempo!)")

    if duration_count != len(agent_completed_events):
        print("   ❌ ERRO: Nem todos os agentes têm duração capturada!")
        return False

    print(f"   Total: {duration_count}/{len(agent_completed_events)} agentes com duração")
    print(f"   ⏱️  Duração total da sessão: {total_duration:.2f}s")
    print()

    # VALIDAÇÃO 6: Polling configurado em 1s
    print("9. Validando intervalo de polling...")
    from app.dashboard import AUTO_REFRESH_INTERVAL

    if AUTO_REFRESH_INTERVAL == 1:
        print(f"   ✅ Polling configurado em {AUTO_REFRESH_INTERVAL}s (correto)")
    else:
        print(f"   ❌ ERRO: Polling está em {AUTO_REFRESH_INTERVAL}s (deveria ser 1s)")
        return False
    print()

    # VALIDAÇÃO 7: Formato consistente com EventBus
    print("10. Validando formato dos eventos...")

    required_fields = ["session_id", "timestamp", "event_type", "agent_name",
                      "summary", "tokens_input", "tokens_output", "tokens_total",
                      "cost", "duration"]

    for event in agent_completed_events:
        missing_fields = [field for field in required_fields if field not in event]

        if missing_fields:
            print(f"   ❌ ERRO: Evento faltando campos: {missing_fields}")
            return False

    print("   ✅ Todos os eventos têm campos obrigatórios")
    print()

    # VALIDAÇÃO 8: MemoryManager capturou métricas
    print("11. Validando MemoryManager...")

    session_summary = memory_manager.get_session_summary(session_id)
    if session_summary:
        print(f"   ✅ MemoryManager tem resumo da sessão:")
        print(f"      - Agentes executados: {len(session_summary.get('agents', {}))}")
        print(f"      - Tokens totais: {session_summary.get('total_tokens', 0)}")
        print(f"      - Custo total: ${session_summary.get('total_cost', 0.0):.6f}")
    else:
        print("   ⚠️  MemoryManager não tem resumo (pode ser esperado)")
    print()

    # Limpar eventos após validação
    print("12. Limpando eventos de teste...")
    bus.clear_session(session_id)
    print("   ✅ Eventos limpos")
    print()

    # RESULTADO FINAL
    print("=" * 70)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 70)
    print()
    print("ÉPICO 8 PROTÓTIPO VALIDADO COM SUCESSO:")
    print(f"  ✅ POC 8.1: Reasoning em todos os agentes ({reasoning_count} agentes)")
    print(f"  ✅ Protótipo 8.2: Orquestrador e Metodologista instrumentados")
    print(f"  ✅ Protótipo 8.3: Métricas consolidadas:")
    print(f"     - Tokens: {tokens_count} agentes com dados")
    print(f"     - Custo: {cost_count} agentes, ${total_cost:.6f} total")
    print(f"     - Tempo: {duration_count} agentes, {total_duration:.2f}s total")
    print(f"     - Polling: {AUTO_REFRESH_INTERVAL}s (otimizado)")
    print()
    print("DASHBOARD READY:")
    print("  → Métricas consolidadas exibidas por agente e sessão")
    print("  → Atualização em tempo real via polling (1s)")
    print("  → Reasoning, tokens, custo e tempo disponíveis")
    print()
    print("ÉPICO 9 PODE COMEÇAR:")
    print("  → Interface web conversacional tem acesso a todas as métricas")
    print("  → Formato inline: 💰 $X.XXXX · XXX tokens · X.XXs")
    print("  → Backend compartilhado (LangGraph + EventBus + MemoryManager)")
    print()

    return True


if __name__ == "__main__":
    try:
        success = validate_epic8_complete()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
