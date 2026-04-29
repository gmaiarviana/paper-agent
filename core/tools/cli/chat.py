#!/usr/bin/env python3
"""
CLI conversacional para sistema multi-agente Paper Agent.

Este script implementa um chat contínuo que:
1. Mantém conversa com múltiplos turnos
2. Preserva contexto ao longo da sessão
3. Executa sistema multi-agente (Orquestrador → Estruturador → Metodologista)
4. Transição fluida entre agentes (sem pedir confirmação)
5. Exibe transparência nos bastidores (quais agentes trabalharam)
6. Curadoria unificada pelo Orquestrador

"""

import os
import sys
import uuid
import logging
import argparse
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
# Caminho: core/tools/cli/chat.py -> parent.parent.parent.parent = project root (4 níveis)
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from core.agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state
from core.agents.memory.memory_manager import MemoryManager
from core.utils.event_bus import get_event_bus
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

def parse_args():
    """
    Parse dos argumentos da linha de comando.

    Returns:
        argparse.Namespace: Argumentos parseados
    """
    parser = argparse.ArgumentParser(
        description="CLI conversacional para Paper Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m core.tools.cli.chat              # Modo padrão (CLI limpa)
  python -m core.tools.cli.chat --verbose    # Exibe raciocínio do orquestrador
  python -m core.tools.cli.chat -v           # Atalho para --verbose
        """
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Exibir raciocínio do orquestrador inline (transparência)'
    )

    return parser.parse_args()

def print_header(verbose_mode=False):
    """
    Exibe o cabeçalho do CLI.

    Args:
        verbose_mode (bool): Se True, indica que modo verbose está ativo
    """
    print("=" * 70)
    print("CLI CONVERSACIONAL - PAPER AGENT")
    print("=" * 70)
    print("Chat contínuo com o sistema multi-agente.")
    print("Sistema: Orquestrador → Estruturador → Metodologista\n")

    if verbose_mode:
        print("🧠 Modo VERBOSE ativado - Raciocínio será exibido inline\n")

    print("Digite 'exit' a qualquer momento para sair.\n")

def print_separator():
    """Exibe separador visual."""
    print("-" * 70)

def run_cli(verbose=False):
    """
    Loop principal do CLI conversacional.

    Implementa chat contínuo com múltiplos turnos (Épico 7 Protótipo):
    1. Mantém thread_id único para toda a sessão
    2. Loop de conversa: Você → Sistema → Você → Sistema (N turnos)
    3. Preserva contexto ao longo da sessão
    4. Sistema para quando usuário aceita chamar agente ou digita 'exit'

    Args:
        verbose (bool): Se True, exibe raciocínio do orquestrador inline

    """
    print_header(verbose_mode=verbose)

    # Criar grafo uma vez
    print("🔧 Inicializando sistema multi-agente...")
    graph = create_multi_agent_graph()
    print("✅ Sistema pronto!")
    print(f"📁 Eventos salvos em: {event_bus.events_dir}\n")

    # Thread ID e Session ID únicos para toda a sessão conversacional
    session_uuid = uuid.uuid4()
    session_id = f"cli-session-{session_uuid}"
    session_short = str(session_uuid)[:8]
    thread_id = f"thread-{session_id}"

    config = {
        "configurable": {
            "thread_id": thread_id,
            "session_id": session_id,
            "memory_manager": memory_manager,
            "active_idea_id": None  # CLI não usa ideias persistidas (Épico 9.2)
        }
    }

    print(f"💬 Sessão iniciada: {session_short}")

    # Publicar evento de início de sessão
    try:
        event_bus.publish_session_started(
            session_id=session_id,
            user_input="[Sessão conversacional iniciada]"
        )
        logger.info(f"✅ Evento session_started publicado para {session_id}")
    except Exception as e:
        logger.warning(f"Aviso: Não foi possível publicar eventos: {e}")

    print_separator()
    print("Sistema: Olá! Me conte sobre sua ideia ou observação.")
    print_separator()

    # Loop conversacional contínuo
    while True:
        # Solicitar input do usuário
        user_input = input("\nVocê: ").strip()

        # Verificar comando exit
        if user_input.lower() in ['exit', 'sair']:
            print("\n👋 Encerrando CLI. Até logo!")

            # Publicar evento de conclusão
            try:
                totals = memory_manager.get_session_totals(session_id)
                event_bus.publish_session_completed(
                    session_id=session_id,
                    final_status="user_exit",
                    tokens_total=totals.get('total', 0)
                )
            except Exception:
                pass

            break

        # Validar input vazio
        if not user_input:
            print("\n⚠️  Mensagem vazia. Por favor, digite algo.")
            continue

        # Criar estado para este turno da conversa
        state = create_initial_multi_agent_state(user_input, session_id=session_id)

        try:
            # Invocar grafo com thread_id preservado
            graph.invoke(state, config=config)

            # Verificar estado após invocação
            snapshot = graph.get_state(config)

            # Processar resultado
            if not snapshot.next:
                # Grafo terminou - verificar tipo de término
                final_state = snapshot.values
                next_step = final_state.get('next_step')

                # CASO 1: Fim conversacional (Orquestrador quer continuar conversa)
                if next_step in ['explore', 'clarify']:
                    # Exibir raciocínio completo (se verbose)
                    if verbose and final_state.get('orchestrator_analysis'):
                        reasoning = final_state['orchestrator_analysis']
                        print(f"\n{'=' * 70}")
                        print("🧠 RACIOCÍNIO DO ORQUESTRADOR")
                        print(f"{'=' * 70}")
                        print(f"{reasoning}")
                        print(f"{'=' * 70}\n")

                    # Exibir argumento focal (se verbose)
                    if verbose and final_state.get('focal_argument'):
                        focal = final_state['focal_argument']
                        print("📌 ARGUMENTO FOCAL:")
                        print(f"   Intent: {focal.get('intent')}")
                        print(f"   Subject: {focal.get('subject')}")
                        print(f"   Population: {focal.get('population')}")
                        print(f"   Metrics: {focal.get('metrics')}")
                        print(f"   Type: {focal.get('article_type')}\n")

                    # Exibir transparência nos bastidores (Épico 1.1 - quais agentes trabalharam)
                    agents_worked = []
                    if final_state.get('structurer_output'):
                        agents_worked.append("📝 Estruturador")
                    if final_state.get('methodologist_output'):
                        agents_worked.append("🔬 Metodologista")

                    if agents_worked:
                        print(f"[Bastidores: {' → '.join(agents_worked)} trabalhou]")

                    # Exibir mensagem conversacional (curadoria do Orquestrador)
                    if final_state.get('messages'):
                        last_message = final_state['messages'][-1].content
                        print(f"\nSistema: {last_message}")

                    # Exibir provocação de reflexão (se existir - MVP 7.9)
                    if final_state.get('reflection_prompt'):
                        reflection = final_state['reflection_prompt']
                        print(f"\n💭 Reflexão: {reflection}")

                    # Exibir sugestão de estágio (se existir - MVP 7.10)
                    if final_state.get('stage_suggestion'):
                        stage_sug = final_state['stage_suggestion']
                        from_stage = stage_sug.get('from_stage')
                        to_stage = stage_sug.get('to_stage')
                        justif = stage_sug.get('justification')
                        print(f"\n🎯 Sugestão de Estágio: {from_stage} → {to_stage}")
                        print(f"   {justif}")

                    # Continuar loop (próximo turno)
                    continue

                # CASO 2: Transição para agente (Épico 1.1 - Transição Fluida)
                # NOTA: Este caso só ocorre se o grafo terminou antes do agente executar
                # (ex: agent_suggestion inválido). No fluxo normal, o agente executa
                # automaticamente e o Orquestrador faz curadoria antes de retornar.
                elif next_step == 'suggest_agent':
                    agent_suggestion = final_state.get('agent_suggestion', {})
                    suggested_agent = agent_suggestion.get('agent', 'N/A')

                    # Exibir raciocínio completo (se verbose)
                    if verbose and final_state.get('orchestrator_analysis'):
                        reasoning = final_state['orchestrator_analysis']
                        print(f"\n{'=' * 70}")
                        print("🧠 RACIOCÍNIO DO ORQUESTRADOR")
                        print(f"{'=' * 70}")
                        print(f"{reasoning}")
                        print(f"{'=' * 70}\n")

                    # Exibir argumento focal (se verbose)
                    if verbose and final_state.get('focal_argument'):
                        focal = final_state['focal_argument']
                        print("📌 ARGUMENTO FOCAL:")
                        print(f"   Intent: {focal.get('intent')}")
                        print(f"   Subject: {focal.get('subject')}")
                        print(f"   Population: {focal.get('population')}")
                        print(f"   Metrics: {focal.get('metrics')}")
                        print(f"   Type: {focal.get('article_type')}\n")

                    # Exibir transparência nos bastidores (quais agentes trabalharam)
                    agents_worked = []
                    if final_state.get('structurer_output'):
                        agents_worked.append("📝 Estruturador")
                    if final_state.get('methodologist_output'):
                        agents_worked.append("🔬 Metodologista")

                    if agents_worked:
                        print(f"\n[Bastidores: {' → '.join(agents_worked)} trabalhou]")

                    # Exibir mensagem do sistema (curadoria ou próxima ação)
                    if final_state.get('messages'):
                        last_message = final_state['messages'][-1].content
                        print(f"\nSistema: {last_message}")

                    # Exibir provocação de reflexão (se existir)
                    if final_state.get('reflection_prompt'):
                        reflection = final_state['reflection_prompt']
                        print(f"\n💭 Reflexão: {reflection}")

                    # Exibir sugestão de estágio (se existir)
                    if final_state.get('stage_suggestion'):
                        stage_sug = final_state['stage_suggestion']
                        from_stage = stage_sug.get('from_stage')
                        to_stage = stage_sug.get('to_stage')
                        justif_stage = stage_sug.get('justification')
                        print(f"\n🎯 Sugestão de Estágio: {from_stage} → {to_stage}")
                        print(f"   {justif_stage}")

                    # Continuar loop automaticamente (sem pedir confirmação)
                    # O grafo já executou o agente ou houve fallback
                    continue

                # CASO 3: Fim de sessão (agente processou e terminou)
                else:
                    # Exibir resultado final
                    print_separator()
                    print("📊 RESULTADO FINAL")
                    print_separator()

                    status = final_state.get('status', 'pending')
                    justification = final_state.get('justification', 'Sem justificativa.')

                    if status == 'approved':
                        print("✅ Status: APROVADA")
                    elif status == 'rejected':
                        print("❌ Status: REJEITADA")
                    else:
                        print(f"⏳ Status: {status.upper()}")

                    print(f"\n📝 Justificativa:\n{justification}\n")

                    # Métricas
                    print_separator()
                    print("📊 MÉTRICAS DE EXECUÇÃO")
                    print_separator()

                    totals = memory_manager.get_session_totals(session_id)
                    tokens_total = totals.get('total', 0)

                    if tokens_total > 0:
                        for agent_name, agent_total in totals.items():
                            if agent_name == 'total':
                                continue
                            print(f"  {agent_name:>15}: {agent_total:>6} tokens")
                        print(f"  {'TOTAL':>15}: {tokens_total:>6} tokens")
                    else:
                        print("  Nenhuma métrica registrada.")

                    # Publicar evento de conclusão
                    try:
                        event_bus.publish_session_completed(
                            session_id=session_id,
                            final_status=status,
                            tokens_total=tokens_total
                        )
                    except Exception:
                        pass

                    print()
                    break  # Sair do loop conversacional

        except KeyboardInterrupt:
            print("\n\n⚠️  Execução interrompida. Digite 'exit' para sair.\n")
            continue

        except Exception as e:
            print(f"\n❌ Erro: {e}")
            logger.exception("Erro detalhado:")
            print("Sistema: Desculpe, ocorreu um erro. Pode tentar novamente?\n")
            continue

if __name__ == "__main__":
    try:
        # Parse argumentos da linha de comando
        args = parse_args()

        # Executar CLI conversacional com configurações
        run_cli(verbose=args.verbose)
    except KeyboardInterrupt:
        print("\n\n👋 CLI encerrado. Até logo!")
        sys.exit(0)
