"""
Teste de fumaça (smoke test) do agente Metodologista.

Este teste valida o fluxo completo do agente em um cenário real:
1. Recebe uma hipótese vaga
2. Faz perguntas de clarificação
3. Toma decisão final (aprovada/rejeitada)

Marcado como @pytest.mark.integration porque usa API real da Anthropic.

"""

import os
import uuid
from pathlib import Path

import pytest
from dotenv import load_dotenv
from langgraph.types import Command

from agents.methodologist import (
    create_methodologist_graph,
    create_initial_state,
)

# Carregar variáveis de ambiente do .env
# Busca o .env na raiz do projeto (2 níveis acima deste arquivo)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

requires_anthropic = pytest.mark.skipif(
    not ANTHROPIC_API_KEY,
    reason="Integration test skipped: ANTHROPIC_API_KEY not set (requires real API)",
)

@pytest.mark.smoke
@pytest.mark.integration
@requires_anthropic
def test_methodologist_complete_flow_with_clarifications():
    """
    Teste de fumaça que simula o fluxo completo do agente Metodologista.

    Cenário:
    - Hipótese vaga: "Café aumenta produtividade"
    - Agente deve fazer perguntas para clarificar
    - Usuário responde (simulado)
    - Agente toma decisão final

    Validações:
    - status deve ser "approved" ou "rejected" (não "pending")
    - justification deve estar preenchida
    - Pelo menos 1 clarificação deve ter sido coletada
    """
    # 1. Criar grafo e estado inicial com hipótese vaga
    graph = create_methodologist_graph()
    hypothesis = "Café aumenta produtividade"
    state = create_initial_state(hypothesis, max_iterations=2)

    # 2. Gerar thread ID único para esta sessão de teste
    thread_id = f"test-smoke-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}

    print(f"\n🧪 Iniciando teste de fumaça com hipótese: '{hypothesis}'")

    # 3. Primeira invocação do grafo
    graph.invoke(state, config=config)

    # 4. Loop para processar interrupts (perguntas do agente)
    iteration_count = 0
    max_iterations = 5  # Limite de segurança para evitar loop infinito

    while iteration_count < max_iterations:
        # Verificar estado atual do grafo
        snapshot = graph.get_state(config)

        # Se não há mais nós pendentes, o grafo terminou
        if not snapshot.next:
            print("✅ Grafo finalizou execução")
            break

        # Processar interrupts (perguntas do agente)
        interrupt_found = False
        if snapshot.tasks:
            for task in snapshot.tasks:
                if task.interrupts:
                    for interrupt_data in task.interrupts:
                        question = interrupt_data.value
                        interrupt_found = True

                        print(f"❓ Agente perguntou: {question}")

                        # Simular resposta do usuário baseada na pergunta
                        if "população" in question.lower() or "amostra" in question.lower():
                            simulated_answer = "Adultos de 18 a 40 anos, trabalhadores de escritório"
                        elif "produtividade" in question.lower() or "medid" in question.lower():
                            simulated_answer = "Número de tarefas completadas por hora em software de gestão"
                        elif "variável" in question.lower():
                            simulated_answer = "Variável independente: consumo de café (mg de cafeína). Variável dependente: tarefas completadas/hora"
                        elif "condições" in question.lower() or "experimental" in question.lower():
                            simulated_answer = "Grupo controle sem cafeína vs grupo experimental com 200mg de cafeína"
                        else:
                            simulated_answer = "Estudo controlado randomizado com medições antes e depois"

                        print(f"💬 Resposta simulada: {simulated_answer}")

                        # Retomar execução com a resposta usando Command(resume=...)
                        graph.invoke(
                            Command(resume=simulated_answer),
                            config=config
                        )

                        iteration_count += 1
                        break

                if interrupt_found:
                    break

        # Se não encontrou interrupts mas há next, algo inesperado
        if not interrupt_found and snapshot.next:
            pytest.fail(f"Estado inesperado: next={snapshot.next} mas sem interrupts")

    # 5. Obter estado final
    final_snapshot = graph.get_state(config)
    final_state = final_snapshot.values

    print("\n📊 RESULTADO FINAL:")
    print(f"Status: {final_state.get('status')}")
    print(f"Clarificações coletadas: {len(final_state.get('clarifications', {}))}")
    print(f"Iterações realizadas: {final_state.get('iterations')}")
    print(f"Justificativa: {final_state.get('justification')[:100]}...")

    # 6. VALIDAÇÕES DO TESTE DE FUMAÇA

    # Validação 1: Status deve ser final (não pending)
    status = final_state.get('status')
    assert status in ['approved', 'rejected'], (
        f"Status deve ser 'approved' ou 'rejected', mas foi '{status}'"
    )

    # Validação 2: Justificativa deve estar preenchida
    justification = final_state.get('justification', '')
    assert justification != '', "Justificativa não pode estar vazia"
    assert len(justification) > 20, (
        f"Justificativa muito curta ({len(justification)} chars). "
        "Esperado explicação detalhada."
    )

    # Validação 3: Pelo menos 1 clarificação deve ter sido coletada
    # (hipótese vaga deve gerar perguntas)
    clarifications = final_state.get('clarifications', {})
    assert len(clarifications) >= 1, (
        f"Esperado pelo menos 1 clarificação, mas foram coletadas {len(clarifications)}"
    )

    print("\n✅ Teste de fumaça passou! Fluxo completo validado.")

@pytest.mark.smoke
@pytest.mark.integration
@requires_anthropic
def test_methodologist_respects_max_iterations():
    """
    Testa que o agente respeita o limite de max_iterations.

    Mesmo com hipótese vaga, após atingir max_iterations,
    o agente deve decidir com as informações disponíveis.
    """
    # Criar grafo com max_iterations baixo
    graph = create_methodologist_graph()
    hypothesis = "Plantas crescem mais rápido"  # Hipótese muito vaga
    state = create_initial_state(hypothesis, max_iterations=1)  # Apenas 1 pergunta permitida

    thread_id = f"test-max-iter-{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}

    print(f"\n🧪 Testando limite de iterações com max_iterations=1")

    # Primeira invocação
    graph.invoke(state, config=config)

    # Loop para processar interrupts
    questions_asked = 0
    max_loop_iterations = 5

    for _ in range(max_loop_iterations):
        snapshot = graph.get_state(config)

        if not snapshot.next:
            break

        # Processar interrupts
        if snapshot.tasks:
            for task in snapshot.tasks:
                if task.interrupts:
                    for interrupt_data in task.interrupts:
                        questions_asked += 1
                        print(f"❓ Pergunta {questions_asked}: {interrupt_data.value}")

                        # Responder com informação mínima
                        graph.invoke(
                            Command(resume="Informação genérica"),
                            config=config
                        )
                        break
                    break

    # Obter estado final
    final_snapshot = graph.get_state(config)
    final_state = final_snapshot.values

    print(f"\n📊 Perguntas feitas: {questions_asked}")
    print(f"Status final: {final_state.get('status')}")

    # Validações
    assert questions_asked <= 1, (
        f"Esperado no máximo 1 pergunta, mas foram feitas {questions_asked}"
    )

    assert final_state.get('status') in ['approved', 'rejected'], (
        "Agente deve decidir mesmo com poucas informações após atingir max_iterations"
    )

    print("✅ Limite de iterações respeitado!")
