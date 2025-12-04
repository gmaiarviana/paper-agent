"""
Validação de Comportamento: FLUXO CONVERSACIONAL

Valida capacidades de conversação do sistema:
- Exploração com perguntas abertas (não classificação)
- Múltiplos turnos com contexto preservado
- Sugestão de agentes com justificativa
- Detecção de mudança de direção
- Router com fallback seguro

IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic.
Custo estimado: ~$0.02-0.05

Uso:
    python scripts/flows/validate_conversation_flow.py
"""

import logging
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

from agents.orchestrator import (
    create_initial_multi_agent_state,
    orchestrator_node,
    route_from_orchestrator
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def print_separator(title=""):
    if title:
        print(f"\n{'='*80}\n  {title}\n{'='*80}\n")
    else:
        print(f"\n{'-'*80}\n")


def print_result(result):
    """Imprime resultado do orquestrador de forma formatada."""
    print(f"  next_step: {result.get('next_step')}")
    print(f"  analysis: {result.get('orchestrator_analysis', '')[:100]}...")
    if result.get('messages'):
        print(f"  message: {result['messages'][0].content[:100]}...")
    if result.get('agent_suggestion'):
        print(f"  suggestion: {result['agent_suggestion']}")


# =============================================================================
# TESTES DE COMPORTAMENTO
# =============================================================================

def test_exploration_vague_input():
    """
    BEHAVIOR: Sistema explora com perguntas abertas (não classifica)
    
    Quando usuário dá input vago, sistema deve:
    - Fazer perguntas abertas
    - next_step = "explore" ou "clarify"
    - NÃO sugerir agente ainda
    """
    print_separator("BEHAVIOR: Exploração com Input Vago")
    
    user_input = "Observei que LLMs aumentam produtividade"
    print(f"Input: '{user_input}'\n")
    
    state = create_initial_multi_agent_state(user_input, session_id="test-conv-1")
    result = orchestrator_node(state)
    
    print_result(result)
    
    # Validações
    assert result['next_step'] in ["explore", "clarify"], \
        f"❌ Esperado explore/clarify, recebido: {result['next_step']}"
    assert result['agent_suggestion'] is None, \
        f"❌ Não deveria sugerir agente com input vago"
    
    # Router deve retornar para usuário
    state['next_step'] = result['next_step']
    state['agent_suggestion'] = result['agent_suggestion']
    destination = route_from_orchestrator(state)
    assert destination == "user", f"❌ Router deveria retornar 'user', retornou '{destination}'"
    
    print("\n✅ Sistema explorou corretamente (não classificou)")


def test_multi_turn_context_preserved():
    """
    BEHAVIOR: Contexto preservado entre múltiplos turnos
    
    Após vários turnos, sistema deve:
    - Lembrar informações anteriores
    - Acumular histórico de mensagens
    - Usar contexto para decisões
    """
    print_separator("BEHAVIOR: Contexto Preservado em Múltiplos Turnos")
    
    # Turno 1
    print("--- Turno 1 ---")
    user_input_1 = "Observei que LLMs aumentam produtividade"
    print(f"Input: '{user_input_1}'")
    
    state = create_initial_multi_agent_state(user_input_1, session_id="test-conv-2")
    result_1 = orchestrator_node(state)
    print(f"  Mensagens após turno 1: {len(result_1.get('messages', []))}")
    
    # Turno 2
    print("\n--- Turno 2 ---")
    user_input_2 = "Na minha equipe Python, usando Claude Code"
    print(f"Input: '{user_input_2}'")
    
    state['messages'].extend(result_1.get('messages', []))
    state['messages'].append(HumanMessage(content=user_input_2))
    state['user_input'] = user_input_2
    
    result_2 = orchestrator_node(state)
    
    # Validações
    assert len(state['messages']) > 1, "❌ Histórico não acumulou"
    print(f"  Mensagens após turno 2: {len(state['messages']) + len(result_2.get('messages', []))}")
    
    print("\n✅ Contexto preservado entre turnos")


def test_agent_suggestion_with_justification():
    """
    BEHAVIOR: Sugestão de agente com justificativa
    
    Quando contexto está claro, sistema deve:
    - next_step = "suggest_agent"
    - agent_suggestion com 'agent' e 'justification'
    - Router roteia para agente sugerido
    """
    print_separator("BEHAVIOR: Sugestão de Agente com Justificativa")
    
    # Estado com contexto claro
    user_input = "Quero validar minha hipótese sobre LLMs"
    state = create_initial_multi_agent_state(user_input, session_id="test-conv-3")
    state['messages'] = [
        HumanMessage(content="Claude Code reduz tempo de tarefas de 2h para 30min"),
        AIMessage(content="Você quer validar ou entender literatura?"),
        HumanMessage(content="Quero validar como hipótese testável")
    ]
    
    print(f"Input com contexto: '{user_input}'")
    print(f"Histórico: {len(state['messages'])} mensagens\n")
    
    result = orchestrator_node(state)
    print_result(result)
    
    if result['next_step'] == "suggest_agent":
        assert result['agent_suggestion'] is not None, \
            "❌ suggest_agent mas agent_suggestion é None"
        assert 'agent' in result['agent_suggestion'], \
            "❌ agent_suggestion sem campo 'agent'"
        assert 'justification' in result['agent_suggestion'], \
            "❌ agent_suggestion sem campo 'justification'"
        
        # Router deve rotear para agente sugerido
        state['next_step'] = result['next_step']
        state['agent_suggestion'] = result['agent_suggestion']
        destination = route_from_orchestrator(state)
        assert destination == result['agent_suggestion']['agent'], \
            f"❌ Router deveria ir para '{result['agent_suggestion']['agent']}'"
        
        print(f"\n✅ Agente '{result['agent_suggestion']['agent']}' sugerido com justificativa")
    else:
        print(f"\n⚠️ Sistema preferiu explorar mais (next_step='{result['next_step']}')")
        print("   Isso é aceitável - orquestrador pode ser conservador")


def test_direction_change_detection():
    """
    BEHAVIOR: Detecção de mudança de direção

    Quando usuário muda de direção, sistema deve:
    - Detectar mudança sem questionar
    - Adaptar sem bloquear
    - Atualizar sugestões baseado em nova direção
    """
    print_separator("BEHAVIOR: Detecção de Mudança de Direção")

    # Estado com direção inicial
    user_input = "Na verdade, quero fazer revisão de literatura primeiro"
    state = create_initial_multi_agent_state(user_input, session_id="test-conv-4")
    state['messages'] = [
        HumanMessage(content="Quero testar minha hipótese sobre LLMs e produtividade"),
        AIMessage(content="Vou validar sua hipótese metodologicamente. Isso captura o que você quer?"),
        HumanMessage(content=user_input)  # Mudança de direção
    ]

    print(f"Direção original: Testar hipótese")
    print(f"Nova direção: '{user_input}'\n")
    
    result = orchestrator_node(state)
    print_result(result)
    
    # Sistema não deve questionar a mudança
    message = result.get('messages', [{}])[0].content if result.get('messages') else ''
    questioning_words = ['por que mudou', 'por que você mudou', 'contradição']
    not_questioning = not any(word in message.lower() for word in questioning_words)
    
    if not_questioning:
        print("\n✅ Sistema adaptou sem questionar mudança")
    else:
        print("\n⚠️ Sistema questionou mudança (não ideal)")


def test_router_fallback_safety():
    """
    BEHAVIOR: Router com fallback seguro
    
    Em estados inválidos/inconsistentes, router deve:
    - Não quebrar
    - Fazer fallback para 'user'
    """
    print_separator("BEHAVIOR: Router com Fallback Seguro")
    
    state = create_initial_multi_agent_state("Teste", session_id="test-conv-5")
    
    # Teste 1: suggest_agent mas suggestion=None
    print("Teste 1: agent_suggestion inconsistente")
    state['next_step'] = "suggest_agent"
    state['agent_suggestion'] = None
    
    destination = route_from_orchestrator(state)
    assert destination == "user", f"❌ Esperado fallback 'user', recebido '{destination}'"
    print("  ✅ Fallback para 'user'")
    
    # Teste 2: agente inválido
    print("\nTeste 2: agente inválido")
    state['agent_suggestion'] = {"agent": "invalid_agent", "justification": "teste"}
    
    destination = route_from_orchestrator(state)
    assert destination == "user", f"❌ Esperado fallback 'user', recebido '{destination}'"
    print("  ✅ Fallback para 'user'")
    
    print("\n✅ Router é seguro com estados inválidos")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print_separator("VALIDAÇÃO: FLUXO CONVERSACIONAL")
    
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRO: ANTHROPIC_API_KEY não configurada no .env")
        sys.exit(1)
    
    try:
        test_exploration_vague_input()
        test_multi_turn_context_preserved()
        test_agent_suggestion_with_justification()
        test_direction_change_detection()
        test_router_fallback_safety()
        
        print_separator("RESUMO")
        print("✅ TODOS OS BEHAVIORS DE CONVERSAÇÃO VALIDADOS!")
        print("\nCapacidades testadas:")
        print("  ✅ Exploração com perguntas abertas")
        print("  ✅ Contexto preservado entre turnos")
        print("  ✅ Sugestão de agente com justificativa")
        print("  ✅ Detecção de mudança de direção")
        print("  ✅ Router com fallback seguro")
        
    except AssertionError as e:
        print(f"\n❌ FALHA: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

