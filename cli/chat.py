#!/usr/bin/env python3
"""
CLI Minimalista para testar o agente Metodologista.

Este script implementa um loop interativo que:
1. Recebe uma hipótese do usuário
2. Executa o agente Metodologista
3. Lida com interrupções (quando o agente precisa de clarificações)
4. Exibe a decisão final

Versão: 1.0
Data: 10/11/2025
"""

import os
import sys
import uuid
import logging
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.methodologist import create_methodologist_graph, create_initial_state
from agents.memory.memory_manager import MemoryManager
from dotenv import load_dotenv
from langgraph.types import Command

# Configurar logging
logging.basicConfig(
    level=logging.WARNING,  # Apenas warnings e erros por padrão
    format='%(levelname)s: %(message)s'
)

# Carregar variáveis de ambiente
load_dotenv()

# Instância global do MemoryManager (Épico 6)
memory_manager = MemoryManager()


def print_header():
    """Exibe o cabeçalho do CLI."""
    print("=" * 70)
    print("CLI MINIMALISTA - AGENTE METODOLOGISTA")
    print("=" * 70)
    print("Digite sua hipótese para avaliação metodológica.")
    print("Cada análise começa com contexto limpo.\n")
    print("Digite 'exit' a qualquer momento para sair.\n")


def print_separator():
    """Exibe separador visual."""
    print("-" * 70)


def run_cli():
    """
    Loop principal do CLI.

    Implementa o fluxo completo:
    1. Solicita hipótese do usuário
    2. Cria thread ID único para sessão
    3. Executa grafo do Metodologista
    4. Lida com interrupts (perguntas do agente)
    5. Exibe resultado final
    """
    print_header()

    # Criar grafo uma vez
    print("🔧 Inicializando agente Metodologista...")
    graph = create_methodologist_graph()
    print("✅ Agente pronto!\n")

    while True:
        print_separator()

        # Solicitar hipótese
        hypothesis = input("📝 Digite sua hipótese (ou 'exit'): ").strip()

        # Verificar comando exit
        if hypothesis.lower() == 'exit':
            print("\n👋 Encerrando CLI. Até logo!")
            break

        # Validar input vazio
        if not hypothesis:
            print("⚠️  Hipótese vazia. Por favor, digite algo.")
            continue

        # Nova sessão a cada hipótese (Épico 6 - contexto limpo automático)
        session_id = f"cli-session-{uuid.uuid4()}"
        thread_id = f"thread-{session_id}"
        config = {"configurable": {"thread_id": thread_id}}

        print(f"\n🔬 Analisando hipótese...\n")

        # Criar estado inicial
        state = create_initial_state(hypothesis)

        # Registrar início da execução no MemoryManager (Épico 6)
        memory_manager.add_execution(
            session_id=session_id,
            agent_name="methodologist",
            tokens_input=0,  # Será atualizado após execução
            tokens_output=0,
            summary=f"Analisando: {hypothesis[:50]}..."
        )

        # Loop de execução: continua enquanto houver interrupts
        try:
            # Primeira invocação do grafo
            graph.invoke(state, config=config)

            # Loop para processar interrupts até o grafo terminar
            while True:
                # Verificar estado atual do grafo
                snapshot = graph.get_state(config)

                # Se não há mais nós pendentes (next vazio), o grafo terminou
                if not snapshot.next:
                    # Grafo finalizou - exibir resultado
                    final_state = snapshot.values

                    print_separator()
                    print("📊 RESULTADO DA ANÁLISE")
                    print_separator()

                    status = final_state.get('status', 'pending')
                    justification = final_state.get('justification', 'Sem justificativa.')

                    # Formatar status
                    if status == 'approved':
                        print("✅ Status: APROVADA")
                    elif status == 'rejected':
                        print("❌ Status: REJEITADA")
                    else:
                        print(f"⏳ Status: {status.upper()}")

                    print(f"\n📝 Justificativa:\n{justification}\n")

                    # Mostrar estatísticas da análise (Épico 6)
                    totals = memory_manager.get_session_totals(session_id)
                    if totals.get('total', 0) > 0:
                        print(f"📊 Tokens utilizados: {totals['total']}\n")

                    break

                # Se há tasks com interrupts, processar
                interrupt_found = False
                if snapshot.tasks:
                    for task in snapshot.tasks:
                        if task.interrupts:
                            for interrupt_data in task.interrupts:
                                question = interrupt_data.value
                                interrupt_found = True

                                # Exibir pergunta do agente
                                print(f"❓ Agente pergunta: {question}")

                                # Solicitar resposta do usuário
                                user_answer = input("💬 Sua resposta: ").strip()

                                # Verificar se usuário quer sair
                                if user_answer.lower() == 'exit':
                                    print("\n👋 Encerrando CLI. Até logo!")
                                    return

                                # Validar resposta vazia
                                if not user_answer:
                                    user_answer = "Sem resposta fornecida."

                                print()  # Linha em branco para separar

                                # Continuar execução com a resposta
                                # Usamos Command para retomar após interrupt
                                graph.invoke(
                                    Command(resume=user_answer),
                                    config=config
                                )

                                # Continuar loop para verificar próximo estado
                                break

                            if interrupt_found:
                                break

                # Se não encontrou interrupts mas há next, algo inesperado
                if not interrupt_found and snapshot.next:
                    print("⚠️  Estado inesperado do grafo. Encerrando.")
                    break

        except KeyboardInterrupt:
            print("\n\n⚠️  Execução interrompida pelo usuário.")
            print("Digite 'exit' para sair ou continue com uma nova hipótese.\n")
            continue

        except Exception as e:
            print(f"\n❌ Erro ao executar agente: {e}")
            logging.exception("Erro detalhado:")
            continue


if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\n👋 CLI encerrado. Até logo!")
        sys.exit(0)
