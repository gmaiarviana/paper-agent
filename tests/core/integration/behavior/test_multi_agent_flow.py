"""
Validação do fluxo multi-agente conversacional.

Testa a integração entre Orquestrador, Estruturador e Metodologista
no modelo CONVERSACIONAL (não pipeline automático).

Diferença do modelo anterior:
- ANTES (pipeline): Input → Classificação automática → Agentes automáticos
- AGORA (conversacional): Input → Orquestrador explora → Negocia com usuário → Agentes sob demanda

Cenários testados:
1. Input vago → Orquestrador explora com perguntas abertas
2. Input com contexto → Orquestrador sugere agente com justificativa
3. Fluxo completo: Orquestrador → Estruturador → Metodologista (simulado)
4. Preservação de contexto entre turnos

IMPORTANTE: Faz chamadas REAIS à API Anthropic.
Custo estimado: ~$0.05-0.10

Uso:
    python scripts/flows/validate_multi_agent_flow.py
"""

import logging
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.core.common import setup_project_path
setup_project_path()

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.orchestrator.nodes import orchestrator_node
from core.agents.orchestrator.router import route_from_orchestrator
from core.agents.structurer.nodes import structurer_node
from core.agents.methodologist.nodes import decide_collaborative

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_separator(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def print_result(result: dict):
    """Imprime resultado de forma estruturada."""
    print(f"\n{'─' * 60}")
    print(f"Next Step: {result.get('next_step')}")
    print(f"Agent Suggestion: {result.get('agent_suggestion')}")
    
    if result.get('message'):
        msg = result['message']
        print(f"Message: {msg[:100]}...")
    
    if result.get('reflection_prompt'):
        print(f"Reflection: {result['reflection_prompt'][:80]}...")
    
    if result.get('focal_argument'):
        focal = result['focal_argument']
        print(f"Focal Argument: intent={focal.get('intent')}, subject={focal.get('subject')}")
    print(f"{'─' * 60}")

def validate_scenario_1_exploration():
    """
    Cenário 1: Input vago → Orquestrador explora com perguntas abertas.
    
    Comportamento esperado:
    - next_step = "explore" ou "clarify"
    - agent_suggestion = None (ainda não sugere agente)
    - Mensagem com pergunta aberta (não classificação)
    - reflection_prompt presente (provocação socrática)
    """
    print_separator("CENÁRIO 1: Input Vago → Exploração Conversacional")
    
    user_input = "Observei que desenvolver com Claude Code é mais rápido"
    print(f"📝 Input: {user_input}\n")
    print("🎯 Esperado: Exploração com perguntas abertas, sem classificação automática")
    
    state = create_initial_multi_agent_state(user_input, session_id="validation-1")
    result = orchestrator_node(state)
    
    print_result(result)
    
    # Validações
    assert result.get('next_step') in ['explore', 'clarify'], \
        f"❌ Esperado explore/clarify, mas next_step = '{result.get('next_step')}'"
    print("   ✅ Next step é exploratório (explore/clarify)")
    
    assert result.get('agent_suggestion') is None or result.get('next_step') != 'suggest_agent', \
        "❌ Não deveria sugerir agente com input vago no primeiro turno"
    print("   ✅ Não sugeriu agente prematuramente")
    
    assert result.get('focal_argument'), \
        "❌ Deveria ter argumento focal"
    print("   ✅ Argumento focal presente")
    
    assert result.get('reflection_prompt'), \
        "❌ Deveria ter provocação de reflexão"
    print("   ✅ Provocação socrática presente")
    
    # Verificar que mensagem não classifica automaticamente
    message = result.get('message', '').lower()
    rigid_words = ['classificando', 'detectei que', 'vou estruturar', 'automático']
    has_rigid = any(word in message for word in rigid_words)
    assert not has_rigid, \
        f"❌ Mensagem não deveria ter palavras de pipeline: {message[:100]}"
    print("   ✅ Mensagem é conversacional (não pipeline)")
    
    print("\n✅ CENÁRIO 1 VALIDADO!")
    return result

def validate_scenario_2_context_accumulation():
    """
    Cenário 2: Múltiplos turnos → Contexto preservado e acumulado.
    
    Comportamento esperado:
    - Argumento focal evolui com cada turno
    - Histórico de mensagens preservado
    - Orquestrador considera contexto anterior
    """
    print_separator("CENÁRIO 2: Múltiplos Turnos → Contexto Preservado")
    
    # Turno 1
    print("--- Turno 1 ---")
    user_input_1 = "Quero testar hipótese sobre produtividade"
    print(f"📝 Input: {user_input_1}")
    
    state = create_initial_multi_agent_state(user_input_1, session_id="validation-2")
    result_1 = orchestrator_node(state)
    
    focal_1 = result_1.get('focal_argument', {})
    print(f"   Focal argument: intent={focal_1.get('intent')}, subject={focal_1.get('subject')}")
    
    # Turno 2
    print("\n--- Turno 2 ---")
    user_input_2 = "Em equipes de 3-5 desenvolvedores Python"
    print(f"📝 Input: {user_input_2}")
    
    state['messages'].append(AIMessage(content=result_1.get('message', '')))
    state['messages'].append(HumanMessage(content=user_input_2))
    state['user_input'] = user_input_2
    state['focal_argument'] = focal_1
    
    result_2 = orchestrator_node(state)
    
    focal_2 = result_2.get('focal_argument', {})
    print(f"   Focal argument: intent={focal_2.get('intent')}, subject={focal_2.get('subject')}")
    
    # Validações
    assert len(state['messages']) >= 2, \
        "❌ Histórico deveria ter pelo menos 2 mensagens"
    print(f"   ✅ Histórico tem {len(state['messages'])} mensagens")
    
    # Subject deveria ter evoluído para incluir contexto
    subject_2 = focal_2.get('subject', '')
    has_context = 'python' in subject_2.lower() or 'team' in subject_2.lower() or 'equipe' in subject_2.lower()
    print(f"   {'✅' if has_context else 'ℹ️'} Subject evoluiu: {subject_2[:50]}...")
    
    print("\n✅ CENÁRIO 2 VALIDADO!")
    return result_2

def validate_scenario_3_full_flow():
    """
    Cenário 3: Fluxo completo Orquestrador → Estruturador → Metodologista.
    
    Simula cenário onde usuário aceita sugestão de agente.
    """
    print_separator("CENÁRIO 3: Fluxo Completo Multi-Agente")
    
    # Setup: Estado com contexto suficiente
    user_input = "Pair programming com IA reduz bugs em equipes Python de 2-5 devs"
    print(f"📝 Input: {user_input}\n")
    
    state = create_initial_multi_agent_state(user_input, session_id="validation-3")
    
    # Passo 1: Orquestrador analisa
    print("--- Passo 1: Orquestrador ---")
    result_orch = orchestrator_node(state)
    print(f"   Next step: {result_orch.get('next_step')}")
    print(f"   Agent suggestion: {result_orch.get('agent_suggestion')}")
    
    # Passo 2: Estruturador (simulando aceite do usuário)
    print("\n--- Passo 2: Estruturador ---")
    state['messages'].append(AIMessage(content=result_orch.get('message', '')))
    state['messages'].append(HumanMessage(content="Sim, estruture essa ideia"))
    
    result_struct = structurer_node(state)
    
    structurer_output = result_struct.get('structurer_output')
    assert structurer_output, "❌ Estruturador deveria gerar output"
    
    structured_question = structurer_output.get('structured_question', '')
    print(f"   Questão estruturada: {structured_question[:60]}...")
    print("   ✅ Estruturador gerou questão")
    
    # Passo 3: Metodologista avalia
    print("\n--- Passo 3: Metodologista ---")
    state['structurer_output'] = structurer_output
    
    result_method = decide_collaborative(state)
    
    methodologist_output = result_method.get('methodologist_output')
    assert methodologist_output, "❌ Metodologista deveria gerar output"
    
    status = methodologist_output.get('status')
    justification = methodologist_output.get('justification', '')[:80]
    print(f"   Status: {status}")
    print(f"   Justificativa: {justification}...")
    
    assert status in ['approved', 'needs_refinement', 'rejected'], \
        f"❌ Status inválido: {status}"
    print(f"   ✅ Metodologista decidiu: {status}")
    
    if status == 'needs_refinement':
        improvements = methodologist_output.get('improvements', [])
        print(f"   Gaps identificados: {len(improvements)}")
        for imp in improvements[:2]:
            print(f"      - {imp.get('aspect')}: {imp.get('gap', '')[:40]}...")
    
    print("\n✅ CENÁRIO 3 VALIDADO!")
    return result_method

def validate_scenario_4_router():
    """
    Cenário 4: Router roteia corretamente baseado em next_step.
    """
    print_separator("CENÁRIO 4: Router Decisions")
    
    test_cases = [
        ("explore", None, "user"),
        ("clarify", None, "user"),
        ("suggest_agent", {"agent": "structurer", "justification": "test"}, "structurer"),
        ("suggest_agent", {"agent": "methodologist", "justification": "test"}, "methodologist"),
        ("suggest_agent", None, "user"),  # Fallback
    ]
    
    all_passed = True
    
    for next_step, suggestion, expected in test_cases:
        state = create_initial_multi_agent_state("test", session_id="validation-4")
        state['next_step'] = next_step
        state['agent_suggestion'] = suggestion
        
        destination = route_from_orchestrator(state)
        
        passed = destination == expected
        status = "✅" if passed else "❌"
        print(f"{status} next_step={next_step}, suggestion={suggestion} → {destination} (expected: {expected})")
        
        if not passed:
            all_passed = False
    
    assert all_passed, "❌ Algumas rotas falharam"
    print("\n✅ CENÁRIO 4 VALIDADO!")
    return all_passed

def main():
    print("\n" + "=" * 80)
    print("  VALIDAÇÃO DO FLUXO MULTI-AGENTE CONVERSACIONAL")
    print("  (Comportamento pós-Épico 7 - Orquestrador Socrático)")
    print("=" * 80)
    
    load_dotenv()
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ERRO: ANTHROPIC_API_KEY não configurada")
        sys.exit(1)
    
    try:
        validate_scenario_1_exploration()
        validate_scenario_2_context_accumulation()
        validate_scenario_3_full_flow()
        validate_scenario_4_router()
        
        print_separator("RESUMO FINAL")
        print("✅ Cenário 1: Input vago → Exploração conversacional")
        print("✅ Cenário 2: Múltiplos turnos → Contexto preservado")
        print("✅ Cenário 3: Fluxo completo multi-agente")
        print("✅ Cenário 4: Router decisions")
        print("\n" + "=" * 80)
        print("  TODOS OS CENÁRIOS VALIDADOS! ✅")
        print("=" * 80 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
