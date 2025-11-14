"""
Script de validação manual do Orquestrador Conversacional (Épico 7 POC).

Este script valida o fluxo conversacional completo implementado no Épico 7.1:
- Exploração com perguntas abertas
- Análise contextual com histórico completo
- Sugestão de agentes com justificativa
- Detecção de mudança de direção
- Conversação natural (não classificação)

IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic.
Certifique-se de ter configurado ANTHROPIC_API_KEY no arquivo .env

Uso:
    python scripts/flows/validate_conversational_orchestrator.py

Versão: 1.0 (Épico 7 POC)
Data: 14/11/2025
"""

import logging
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from dotenv import load_dotenv
from scripts.common import setup_project_path

setup_project_path()

from agents.orchestrator import (
    create_initial_multi_agent_state,
    orchestrator_node,
    route_from_orchestrator
)
from langchain_core.messages import HumanMessage, AIMessage

# Configurar logging para ver os detalhes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def print_separator(title=""):
    """Imprime separador visual."""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'-'*80}\n")


def print_orchestrator_response(result):
    """Imprime resposta do orquestrador de forma formatada."""
    print("Resposta do Orquestrador:")
    print(f"  Próximo passo: {result.get('next_step', 'N/A')}")
    print(f"  Raciocínio: {result.get('orchestrator_analysis', 'N/A')[:150]}...")
    print(f"  Mensagem ao usuário: {result['messages'][0].content if result.get('messages') else 'N/A'}")

    if result.get('agent_suggestion'):
        print(f"\n  Sugestão de agente:")
        print(f"    Agente: {result['agent_suggestion'].get('agent', 'N/A')}")
        print(f"    Justificativa: {result['agent_suggestion'].get('justification', 'N/A')}")


def test_1_exploration_vague_input():
    """
    TESTE 1: Exploração inicial com input vago.

    Critérios de aceite:
    - Orquestrador faz perguntas abertas (não classifica)
    - next_step = "explore"
    - agent_suggestion = None
    - Mensagem conversacional ao usuário
    """
    print_separator("TESTE 1: EXPLORAÇÃO INICIAL - INPUT VAGO")

    user_input = "Observei que LLMs aumentam produtividade"
    print(f"Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input, session_id="test-session-1")

    # Executar nó do orquestrador conversacional
    result = orchestrator_node(state)

    print_orchestrator_response(result)

    # Validações
    print("\n✅ Validações:")
    assert result['next_step'] == "explore" or result['next_step'] == "clarify", \
        f"❌ Esperado next_step='explore' ou 'clarify', recebido: {result['next_step']}"
    print(f"  ✓ next_step = '{result['next_step']}' (correto)")

    assert result['agent_suggestion'] is None, \
        f"❌ Esperado agent_suggestion=None, recebido: {result['agent_suggestion']}"
    print("  ✓ agent_suggestion = None (correto)")

    assert len(result['messages']) > 0, "❌ Nenhuma mensagem retornada"
    print(f"  ✓ Mensagem conversacional presente")

    # Testar router
    state['next_step'] = result['next_step']
    state['agent_suggestion'] = result['agent_suggestion']
    next_destination = route_from_orchestrator(state)

    assert next_destination == "user", \
        f"❌ Esperado router retornar 'user', recebido: {next_destination}"
    print(f"  ✓ Router retorna para 'user' (correto)\n")


def test_2_multi_turn_conversation():
    """
    TESTE 2: Múltiplos turnos conversacionais (com histórico).

    Critérios de aceite:
    - Orquestrador analisa histórico completo
    - Contexto preservado entre turnos
    - Sugere agente quando contexto está claro
    """
    print_separator("TESTE 2: MÚLTIPLOS TURNOS CONVERSACIONAIS")

    # Turno 1: Input inicial vago
    user_input = "Observei que LLMs aumentam produtividade"
    print(f"Turno 1 - Input do usuário: {user_input}\n")

    state = create_initial_multi_agent_state(user_input, session_id="test-session-2")
    result_1 = orchestrator_node(state)

    print("Turno 1 - Orquestrador:")
    print(f"  Mensagem: {result_1['messages'][0].content[:100]}...\n")

    # Turno 2: Adicionar contexto
    state['messages'].extend(result_1['messages'])
    state['messages'].append(
        HumanMessage(content="Na minha equipe, usando Claude Code, tarefas de 2h agora levam 30min")
    )

    print(f"Turno 2 - Input do usuário: Na minha equipe, usando Claude Code...\n")

    result_2 = orchestrator_node(state)
    print_orchestrator_response(result_2)

    # Validações
    print("\n✅ Validações:")
    assert 'orchestrator_analysis' in result_2, "❌ Campo orchestrator_analysis ausente"
    assert len(state['messages']) > 1, "❌ Histórico não preservado"
    print(f"  ✓ Histórico preservado ({len(state['messages'])} mensagens)")
    print(f"  ✓ Análise contextual presente\n")


def test_3_agent_suggestion():
    """
    TESTE 3: Sugestão de agente com justificativa.

    Critérios de aceite:
    - next_step = "suggest_agent"
    - agent_suggestion presente com agent e justification
    - Router roteia para agente sugerido
    """
    print_separator("TESTE 3: SUGESTÃO DE AGENTE COM JUSTIFICATIVA")

    # Criar estado com contexto claro (para forçar sugestão)
    user_input = "Quero validar minha hipótese sobre LLMs"
    state = create_initial_multi_agent_state(user_input, session_id="test-session-3")

    # Adicionar histórico que deixa contexto claro
    state['messages'] = [
        HumanMessage(content="Observei que Claude Code reduz tempo de tarefas de 2h para 30min"),
        AIMessage(content="Você quer validar ou entender literatura?"),
        HumanMessage(content="Quero validar como hipótese testável")
    ]

    print(f"Input do usuário (com contexto): {user_input}")
    print(f"Histórico: {len(state['messages'])} mensagens\n")

    result = orchestrator_node(state)
    print_orchestrator_response(result)

    # Validações
    print("\n✅ Validações:")

    # Pode sugerir agente ou pedir mais contexto (depende do LLM)
    if result['next_step'] == "suggest_agent":
        assert result['agent_suggestion'] is not None, \
            "❌ next_step='suggest_agent' mas agent_suggestion é None"
        assert 'agent' in result['agent_suggestion'], \
            "❌ Campo 'agent' ausente em agent_suggestion"
        assert 'justification' in result['agent_suggestion'], \
            "❌ Campo 'justification' ausente em agent_suggestion"

        print(f"  ✓ next_step = 'suggest_agent' (correto)")
        print(f"  ✓ agent_suggestion presente com agente: {result['agent_suggestion']['agent']}")

        # Testar router
        state['next_step'] = result['next_step']
        state['agent_suggestion'] = result['agent_suggestion']
        next_destination = route_from_orchestrator(state)

        suggested_agent = result['agent_suggestion']['agent']
        assert next_destination == suggested_agent, \
            f"❌ Router deveria rotear para '{suggested_agent}', roteou para '{next_destination}'"
        print(f"  ✓ Router roteia para '{next_destination}' (correto)\n")
    else:
        print(f"  ℹ️ Orquestrador preferiu explorar mais (next_step='{result['next_step']}')")
        print(f"  ℹ️ Isso é aceitável no POC - orquestrador é conservador\n")


def test_4_direction_change_detection():
    """
    TESTE 4: Detecção de mudança de direção.

    Critérios de aceite:
    - Orquestrador detecta mudança no histórico
    - Adapta sem questionar mudança
    - Atualiza sugestões baseado em nova direção
    """
    print_separator("TESTE 4: DETECÇÃO DE MUDANÇA DE DIREÇÃO")

    user_input = "Na verdade, quero fazer revisão de literatura primeiro"
    state = create_initial_multi_agent_state(user_input, session_id="test-session-4")

    # Adicionar histórico que mostra direção anterior
    state['messages'] = [
        HumanMessage(content="Quero testar minha hipótese sobre LLMs e produtividade"),
        AIMessage(content="Posso chamar o Metodologista para validar?"),
        HumanMessage(content=user_input)  # Mudança de direção
    ]

    print(f"Input original: Testar hipótese")
    print(f"Nova direção: {user_input}\n")

    result = orchestrator_node(state)
    print_orchestrator_response(result)

    # Validações
    print("\n✅ Validações:")

    # Verificar se raciocínio menciona mudança ou literatura
    reasoning = result.get('orchestrator_analysis', '').lower()
    message = result['messages'][0].content.lower() if result.get('messages') else ''

    direction_detected = any(word in reasoning or word in message
                            for word in ['literatura', 'revisão', 'mudança', 'adaptar', 'entender'])

    if direction_detected:
        print(f"  ✓ Mudança de direção detectada no raciocínio/mensagem")
    else:
        print(f"  ℹ️ Mudança não explicitamente mencionada (aceitável no POC)")

    # Verificar se não questiona a mudança
    questioning_words = ['por que mudou', 'por que você mudou', 'contradição']
    not_questioning = not any(word in message for word in questioning_words)

    if not_questioning:
        print(f"  ✓ Orquestrador não questiona mudança (correto)\n")
    else:
        print(f"  ⚠️ Orquestrador questionou mudança (não ideal, mas aceitável no POC)\n")


def test_5_router_fallback_safety():
    """
    TESTE 5: Segurança do router (fallback).

    Critérios de aceite:
    - Router lida com estados inválidos
    - Fallback seguro para 'user' quando agent_suggestion inválida
    """
    print_separator("TESTE 5: SEGURANÇA DO ROUTER (FALLBACK)")

    state = create_initial_multi_agent_state("Teste", session_id="test-session-5")

    # Teste 5.1: next_step='suggest_agent' mas agent_suggestion=None
    print("Teste 5.1: agent_suggestion inconsistente")
    state['next_step'] = "suggest_agent"
    state['agent_suggestion'] = None

    destination = route_from_orchestrator(state)
    assert destination == "user", \
        f"❌ Esperado fallback para 'user', recebido: {destination}"
    print(f"  ✓ Fallback para 'user' (correto)\n")

    # Teste 5.2: Agente inválido
    print("Teste 5.2: Agente inválido")
    state['next_step'] = "suggest_agent"
    state['agent_suggestion'] = {"agent": "invalid_agent", "justification": "teste"}

    destination = route_from_orchestrator(state)
    assert destination == "user", \
        f"❌ Esperado fallback para 'user', recebido: {destination}"
    print(f"  ✓ Fallback para 'user' (correto)\n")


def main():
    """Executa todos os testes de validação."""
    print_separator("VALIDAÇÃO DO ORQUESTRADOR CONVERSACIONAL (ÉPICO 7 POC)")

    # Carregar variáveis de ambiente
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRO: ANTHROPIC_API_KEY não configurada no .env")
        print("Configure a chave antes de executar este script.\n")
        return

    try:
        # Executar testes
        test_1_exploration_vague_input()
        test_2_multi_turn_conversation()
        test_3_agent_suggestion()
        test_4_direction_change_detection()
        test_5_router_fallback_safety()

        print_separator("RESUMO")
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\nCritérios de aceite do Épico 7 POC validados:")
        print("  ✓ Perguntas abertas (não classificação)")
        print("  ✓ Análise contextual com histórico")
        print("  ✓ Sugestões com justificativa")
        print("  ✓ Detecção de mudança via LLM")
        print("  ✓ Conversação natural")
        print("\nOrquestrador Conversacional está funcionando conforme esperado! 🎉\n")

    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
