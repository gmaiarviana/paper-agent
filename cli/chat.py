#!/usr/bin/env python3
"""
CLI para sistema multi-agente Paper Agent.

Este script implementa um loop interativo que:
1. Recebe uma hipótese ou ideia do usuário
2. Executa sistema multi-agente (Orquestrador → Estruturador → Metodologista)
3. Exibe timeline de execução e decisão final
4. Publica eventos em tempo real para o Dashboard

Versão: 2.0 (Épico 5.1 - Sistema Multi-Agente Completo)
Data: 13/11/2025
"""

import os
import sys
import uuid
import logging
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state
from agents.memory.memory_manager import MemoryManager
from utils.event_bus import get_event_bus
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,  # INFO para ver mensagens do EventBus
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Instância global do MemoryManager (Épico 6)
memory_manager = MemoryManager()

# Instância global do EventBus (Épico 5.1)
event_bus = get_event_bus()


def print_header():
    """Exibe o cabeçalho do CLI."""
    print("=" * 70)
    print("CLI - SISTEMA MULTI-AGENTE PAPER AGENT")
    print("=" * 70)
    print("Digite sua hipótese para avaliação metodológica.")
    print("Sistema: Orquestrador → Estruturador → Metodologista\n")
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
    3. Executa sistema multi-agente completo
    4. Exibe resultado final
    """
    print_header()

    # Criar grafo uma vez
    print("🔧 Inicializando sistema multi-agente...")
    graph = create_multi_agent_graph()
    print("✅ Sistema pronto!")
    print(f"📁 Eventos salvos em: {event_bus.events_dir}\n")

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
        session_uuid = uuid.uuid4()
        session_id = f"cli-session-{session_uuid}"
        session_short = str(session_uuid)[:8]  # Primeiros 8 chars para identificação
        thread_id = f"thread-{session_id}"
        config = {
            "configurable": {
                "thread_id": thread_id,
                "session_id": session_id,  # Épico 5.1 - EventBus
                "memory_manager": memory_manager  # Épico 6.2 - MemoryManager
            }
        }

        print(f"\n🔬 Analisando hipótese... (Session: {session_short})\n")

        # Publicar evento de início de sessão (Épico 5.1)
        try:
            event_bus.publish_session_started(
                session_id=session_id,
                user_input=hypothesis
            )
            logger.info(f"✅ Evento session_started publicado para {session_id}")
        except Exception as e:
            print(f"⚠️  Aviso: Não foi possível publicar eventos: {e}")
            logger.exception("Erro ao publicar session_started:")

        # Criar estado inicial (com session_id para EventBus - Épico 5.1)
        state = create_initial_multi_agent_state(hypothesis, session_id=session_id)

        # Executar sistema multi-agente
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
                    print("🧠 RACIOCÍNIO DO ORQUESTRADOR")
                    print_separator()

                    # Exibir análise do orquestrador conversacional (Épico 7)
                    orchestrator_analysis = final_state.get('orchestrator_analysis')
                    next_step = final_state.get('next_step')
                    agent_suggestion = final_state.get('agent_suggestion')

                    if orchestrator_analysis:
                        print(f"Análise contextual:")
                        # Limitar a 200 chars para não poluir
                        analysis_preview = orchestrator_analysis[:200]
                        if len(orchestrator_analysis) > 200:
                            analysis_preview += "..."
                        print(f"  {analysis_preview}\n")

                    if next_step:
                        next_step_display = {
                            "explore": "🔍 Explorar contexto (mais perguntas)",
                            "clarify": "❓ Clarificar ambiguidade",
                            "suggest_agent": "🤖 Sugerir agente especializado"
                        }.get(next_step, next_step)
                        print(f"Próximo passo: {next_step_display}")

                    if agent_suggestion:
                        agent_name = agent_suggestion.get('agent', 'N/A')
                        justification_agent = agent_suggestion.get('justification', 'N/A')
                        print(f"Agente sugerido: {agent_name}")
                        print(f"Justificativa: {justification_agent[:150]}...")

                    print()

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

                    # Mostrar estatísticas detalhadas da análise (Épico 6.2)
                    print_separator()
                    print("📊 MÉTRICAS DE EXECUÇÃO")
                    print_separator()

                    totals = memory_manager.get_session_totals(session_id)
                    tokens_total = totals.get('total', 0)
                    if tokens_total > 0:
                        # Exibir por agente
                        for agent_name, agent_total in totals.items():
                            if agent_name == 'total':
                                continue
                            print(f"  {agent_name:>15}: {agent_total:>6} tokens")

                        print(f"  {'TOTAL':>15}: {tokens_total:>6} tokens")

                        # Calcular custo total estimado
                        # Buscar execuções de todos os agentes para calcular custo total
                        total_cost = 0.0
                        for agent_name in ["orchestrator", "structurer", "methodologist"]:
                            history = memory_manager.get_session_history(session_id, agent_name)
                            for execution in history:
                                if execution.metadata and "cost_usd" in execution.metadata:
                                    total_cost += execution.metadata["cost_usd"]

                        if total_cost > 0:
                            print(f"  {'Custo estimado':>15}: ${total_cost:.6f}")
                    else:
                        print("  Nenhuma métrica registrada nesta execução.")

                    # Publicar evento de conclusão de sessão (Épico 5.1)
                    try:
                        event_bus.publish_session_completed(
                            session_id=session_id,
                            final_status=status,
                            tokens_total=tokens_total
                        )
                        logger.info(f"✅ Evento session_completed publicado para {session_id}")
                    except Exception as e:
                        print(f"⚠️  Aviso: Não foi possível publicar evento de conclusão: {e}")
                        logger.exception("Erro ao publicar session_completed:")

                    print()
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
            print(f"\n❌ Erro ao executar sistema multi-agente: {e}")
            logging.exception("Erro detalhado:")
            continue


if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\n👋 CLI encerrado. Até logo!")
        sys.exit(0)
