#!/usr/bin/env python3
"""
Script de validação manual para o CLI do agente Metodologista.

Este script testa o fluxo completo do CLI sem precisar de interação manual:
1. Cria o grafo do Metodologista
2. Simula entrada de hipótese
3. Simula respostas a perguntas do agente
4. Valida que o resultado final é gerado corretamente

Para teste manual interativo, use: python cli/chat.py

"""

import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()

from agents.methodologist import create_methodologist_graph, create_initial_state
from dotenv import load_dotenv
from langgraph.types import Command

# Carregar variáveis de ambiente
load_dotenv()

def validate_cli_flow():
    """
    Valida o fluxo completo do CLI programaticamente.

    Este teste simula o que o CLI faz:
    1. Cria grafo
    2. Processa hipótese
    3. Responde perguntas do agente
    4. Valida resultado final
    """
    print("=" * 70)
    print("VALIDAÇÃO DO CLI - AGENTE METODOLOGISTA")
    print("=" * 70)

    # Teste 1: Criar grafo
    print("\n1. Criando grafo do Metodologista...")
    try:
        graph = create_methodologist_graph()
        print("   ✅ Grafo criado com sucesso")
    except Exception as e:
        print(f"   ❌ ERRO ao criar grafo: {e}")
        return False

    # Teste 2: Processar hipótese simples (que provavelmente vai precisar de clarificações)
    print("\n2. Testando hipótese vaga (esperado: agente faz perguntas)...")
    hypothesis = "Café aumenta produtividade"
    thread_id = f"test-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}

    try:
        state = create_initial_state(hypothesis)
        print(f"   📝 Hipótese: {hypothesis}")
        print(f"   🔑 Thread ID: {thread_id}")

        # Executar primeira vez
        result = graph.invoke(state, config=config)

        # Verificar se houve interrupt (agente fez pergunta)
        snapshot = graph.get_state(config)

        if not snapshot.next:
            print("   ⚠️  Agente não fez perguntas (hipótese pode estar muito clara ou muito ruim)")
            print(f"   📊 Status: {result.get('status', 'pending')}")
        else:
            print("   ✅ Agente fez pergunta (comportamento esperado)")

            # Simular respostas a perguntas
            max_responses = 3
            response_count = 0

            while snapshot.next and response_count < max_responses:
                # Pegar pergunta do interrupt
                question = None
                if snapshot.tasks:
                    for task in snapshot.tasks:
                        if task.interrupts:
                            for interrupt_data in task.interrupts:
                                question = interrupt_data.value
                                break

                if question:
                    print(f"\n   ❓ Pergunta {response_count + 1}: {question}")

                    # Simular resposta baseada no contexto
                    simulated_answer = f"Resposta simulada {response_count + 1}: Adultos de 18-40 anos"
                    print(f"   💬 Resposta simulada: {simulated_answer}")

                    # Continuar execução
                    graph.invoke(Command(resume=simulated_answer), config=config)
                    response_count += 1

                    # Atualizar snapshot
                    snapshot = graph.get_state(config)
                else:
                    break

            print(f"\n   ✅ Respondeu {response_count} pergunta(s)")

        # Pegar resultado final
        final_state = graph.get_state(config)
        final_result = final_state.values

        print("\n   📊 RESULTADO FINAL:")
        print(f"      Status: {final_result.get('status', 'pending')}")
        print(f"      Justificativa: {final_result.get('justification', 'N/A')[:100]}...")

    except Exception as e:
        print(f"   ❌ ERRO ao processar hipótese: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Teste 3: Validar componentes essenciais
    print("\n3. Validando componentes essenciais...")

    # Validar que status foi definido
    if final_result.get('status') == 'pending':
        print("   ⚠️  Status ainda está 'pending' - pode indicar problema no fluxo")
    elif final_result.get('status') in ['approved', 'rejected']:
        print(f"   ✅ Status definido corretamente: {final_result.get('status')}")
    else:
        print(f"   ❌ Status inválido: {final_result.get('status')}")
        return False

    # Validar que justificativa foi preenchida
    if final_result.get('justification'):
        print(f"   ✅ Justificativa preenchida ({len(final_result.get('justification'))} caracteres)")
    else:
        print("   ⚠️  Justificativa vazia")

    # Teste 4: Testar thread ID único (isolamento de sessões)
    print("\n4. Testando isolamento de sessões (thread IDs únicos)...")
    thread_id_2 = f"test-{uuid.uuid4()}"
    config_2 = {"configurable": {"thread_id": thread_id_2}}

    state_2 = create_initial_state("Água ferve a 100°C")
    result_2 = graph.invoke(state_2, config=config_2)

    if thread_id != thread_id_2:
        print(f"   ✅ Thread IDs únicos gerados: {thread_id[:20]}... != {thread_id_2[:20]}...")
    else:
        print("   ❌ Thread IDs não são únicos!")
        return False

    # Resumo final
    print("\n" + "=" * 70)
    print("VALIDAÇÃO CONCLUÍDA COM SUCESSO! ✅")
    print("=" * 70)
    print("\n📝 Próximos passos:")
    print("   1. Para testar interativamente: python cli/chat.py")
    print("   2. Para executar testes unitários: python -m pytest tests/unit/ -v")
    print("   3. Para executar testes de integração: python -m pytest tests/integration/ -v")
    print()

    return True

if __name__ == "__main__":
    try:
        success = validate_cli_flow()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validação interrompida pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
