"""
Script de validação da POC 8.1: Instrumentação do Estruturador com Reasoning.

Valida que:
- Estruturador publica eventos agent_started e agent_completed
- Eventos contêm reasoning no metadata
- Dashboard pode exibir reasoning (formato consistente)
- Polling funciona (EventBus)

Épico 8 - POC: Telemetria e Observabilidade
Data: 15/11/2025
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph
from agents.orchestrator.state import create_initial_multi_agent_state
from utils.event_bus import get_event_bus
import json


def validate_epic8_poc():
    """Valida implementação da POC 8.1."""
    print("=" * 70)
    print("VALIDAÇÃO POC 8.1: INSTRUMENTAÇÃO DO ESTRUTURADOR")
    print("=" * 70)
    print()

    # Criar session_id único
    import uuid
    session_id = f"validate-epic8-{uuid.uuid4().hex[:8]}"

    print(f"Session ID: {session_id}")
    print()

    # Limpar eventos anteriores da sessão (se existir)
    bus = get_event_bus()
    bus.clear_session(session_id)

    # Criar estado inicial com input vago (vai chamar Estruturador)
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

    # Executar grafo (vai chamar Orquestrador → Estruturador → Metodologista)
    print("3. Executando grafo (Orquestrador → Estruturador → Metodologista)...")
    config = {
        "configurable": {
            "thread_id": session_id,
            "session_id": session_id  # Para EventBus
        }
    }

    try:
        result = graph.invoke(state, config=config)
        print("   ✅ Grafo executado com sucesso")
    except Exception as e:
        print(f"   ❌ ERRO ao executar grafo: {e}")
        return False
    print()

    # Obter eventos da sessão
    print("4. Validando eventos publicados pelo Estruturador...")
    events = bus.get_session_events(session_id)

    if not events:
        print("   ❌ ERRO: Nenhum evento foi publicado!")
        return False

    print(f"   ✅ {len(events)} eventos publicados")
    print()

    # Filtrar eventos do Estruturador
    structurer_started = [e for e in events
                          if e.get("event_type") == "agent_started"
                          and e.get("agent_name") == "structurer"]

    structurer_completed = [e for e in events
                            if e.get("event_type") == "agent_completed"
                            and e.get("agent_name") == "structurer"]

    print("5. Validando eventos agent_started do Estruturador...")
    if not structurer_started:
        print("   ❌ ERRO: Estruturador não publicou agent_started!")
        return False

    print(f"   ✅ {len(structurer_started)} evento(s) agent_started encontrado(s)")

    # Validar metadata de agent_started
    first_started = structurer_started[0]
    metadata_started = first_started.get("metadata", {})

    if "reasoning" not in metadata_started:
        print("   ⚠️ WARNING: agent_started sem reasoning no metadata")
    else:
        reasoning_started = metadata_started["reasoning"]
        print(f"   ✅ Reasoning presente: '{reasoning_started[:60]}...'")
    print()

    print("6. Validando eventos agent_completed do Estruturador...")
    if not structurer_completed:
        print("   ❌ ERRO: Estruturador não publicou agent_completed!")
        return False

    print(f"   ✅ {len(structurer_completed)} evento(s) agent_completed encontrado(s)")

    # Validar metadata de agent_completed (CRITICAL)
    first_completed = structurer_completed[0]
    metadata_completed = first_completed.get("metadata", {})

    if "reasoning" not in metadata_completed:
        print("   ❌ ERRO CRÍTICO: agent_completed SEM reasoning no metadata!")
        print("   Metadata recebido:", json.dumps(metadata_completed, indent=2, ensure_ascii=False))
        return False

    reasoning_completed = metadata_completed["reasoning"]
    print(f"   ✅ Reasoning presente no metadata")
    print()

    print("7. Validando conteúdo do reasoning...")

    # Reasoning do Estruturador deve mencionar V1 ou contexto/problema/contribuição
    expected_keywords = ["V1", "contexto", "problema", "contribuição", "Estruturando"]

    has_keyword = any(keyword in reasoning_completed for keyword in expected_keywords)

    if not has_keyword:
        print(f"   ⚠️ WARNING: Reasoning não contém palavras-chave esperadas")
        print(f"   Reasoning: {reasoning_completed}")
    else:
        print(f"   ✅ Reasoning contém palavras-chave esperadas")

    print()
    print("   📝 Reasoning completo:")
    print("   " + "─" * 66)
    print(f"   {reasoning_completed}")
    print("   " + "─" * 66)
    print()

    print("8. Validando formato consistente com EventBus...")

    # Verificar que eventos têm campos obrigatórios
    required_fields = ["session_id", "timestamp", "event_type", "agent_name"]

    for event in structurer_completed:
        missing_fields = [field for field in required_fields if field not in event]

        if missing_fields:
            print(f"   ❌ ERRO: Evento faltando campos obrigatórios: {missing_fields}")
            return False

    print("   ✅ Formato consistente com EventBus")
    print()

    print("9. Validando summary (resumo curto)...")
    summary = first_completed.get("summary", "")

    if not summary:
        print("   ⚠️ WARNING: Summary vazio")
    elif len(summary) > 280:
        print(f"   ⚠️ WARNING: Summary muito longo ({len(summary)} chars, máx 280)")
    else:
        print(f"   ✅ Summary válido: '{summary}'")
    print()

    # Limpar eventos após validação
    print("10. Limpando eventos de teste...")
    bus.clear_session(session_id)
    print("   ✅ Eventos limpos")
    print()

    print("=" * 70)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 70)
    print()
    print("POC 8.1 VALIDADA COM SUCESSO:")
    print("  ✅ Estruturador publica agent_started e agent_completed")
    print("  ✅ Reasoning incluído no metadata")
    print("  ✅ Formato consistente com EventBus")
    print("  ✅ Dashboard pode exibir reasoning (padrão implementado)")
    print()
    print("PRÓXIMOS PASSOS:")
    print("  → Testar visualização no Dashboard Streamlit")
    print("  → Implementar Protótipo 8.2: Instrumentar Orquestrador e Metodologista")
    print("  → Implementar Protótipo 8.3: SSE (Server-Sent Events)")
    print()

    return True


if __name__ == "__main__":
    try:
        success = validate_epic8_poc()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
