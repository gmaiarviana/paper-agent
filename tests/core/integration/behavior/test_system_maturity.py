"""
Validação de Maturidade do Sistema Multi-Agente

Este script valida se o sistema está funcionando como esperado segundo a visão:
1. Reasoning Loop: Orquestrador analisa contexto e decide próximos passos
2. Fluxo Multi-Agente: Colaboração entre agentes via negociação
3. Tools: ask_user funciona corretamente
4. Qualidade das Respostas: Fluidas e conversacionais (não rígidas)

IMPORTANTE: Faz chamadas REAIS à API Anthropic.
Custo estimado: ~$0.10-0.20

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

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.orchestrator.nodes import orchestrator_node
from core.agents.orchestrator.router import route_from_orchestrator
from core.agents.structurer.nodes import structurer_node
from core.agents.methodologist.nodes import decide_collaborative

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def print_separator(title=""):
    if title:
        print(f"\n{'='*80}\n  {title}\n{'='*80}\n")
    else:
        print(f"\n{'-'*80}\n")

def print_response_quality(message: str, reflection: str = None):
    """Analisa qualidade da resposta."""
    print("\n📊 ANÁLISE DE QUALIDADE:")
    
    # Indicadores de resposta fluida
    fluent_indicators = [
        '?',  # Pergunta
        'interessante', 'fascinante', 'ótimo',  # Engajamento
        'me conta', 'você quer', 'o que',  # Diálogo
        'posso', 'quer que eu',  # Oferece opções
    ]
    
    # Indicadores de resposta rígida
    rigid_indicators = [
        'detectei', 'classificando', 'automático',
        'processando', 'analisando input',
        'fase 1', 'etapa', 'pipeline'
    ]
    
    message_lower = message.lower()
    
    fluent_count = sum(1 for ind in fluent_indicators if ind in message_lower)
    rigid_count = sum(1 for ind in rigid_indicators if ind in message_lower)
    
    print(f"   Indicadores fluidos: {fluent_count}")
    print(f"   Indicadores rígidos: {rigid_count}")
    
    if fluent_count > rigid_count:
        print("   ✅ Resposta FLUIDA (conversacional)")
        return True
    elif rigid_count > fluent_count:
        print("   ⚠️ Resposta RÍGIDA (pipeline)")
        return False
    else:
        print("   ℹ️ Resposta neutra")
        return True

# =============================================================================
# TESTE 1: REASONING LOOP DO ORQUESTRADOR
# =============================================================================

def test_reasoning_loop():
    """
    Valida que o Orquestrador:
    - Analisa contexto antes de decidir
    - Detecta assumptions implícitas
    - Decide próximo passo baseado em análise
    - Gera provocação quando apropriado
    """
    print_separator("TESTE 1: REASONING LOOP DO ORQUESTRADOR")
    
    inputs_to_test = [
        ("Observei que LLMs aumentam produtividade", "vago - deve explorar"),
        ("Quero testar se Claude Code reduz bugs em 30%", "mais específico - pode sugerir agente"),
        ("Me ajuda a entender metodologia científica", "fora de escopo - deve redirecionar"),
    ]
    
    results = []
    
    for user_input, expected_behavior in inputs_to_test:
        print(f"\n📝 Input: '{user_input}'")
        print(f"   Esperado: {expected_behavior}")
        
        state = create_initial_multi_agent_state(user_input, session_id=f"test-reasoning-{len(results)}")
        result = orchestrator_node(state)
        
        # Verificar campos do reasoning
        has_reasoning = bool(result.get('orchestrator_analysis'))
        has_focal_argument = bool(result.get('focal_argument'))
        has_next_step = bool(result.get('next_step'))
        has_message = bool(result.get('message'))
        has_reflection = bool(result.get('reflection_prompt'))
        
        print(f"\n   ✓ Reasoning: {has_reasoning}")
        print(f"   ✓ Focal argument: {has_focal_argument}")
        print(f"   ✓ Next step: {result.get('next_step')}")
        print(f"   ✓ Reflection: {has_reflection}")
        
        # Análise de qualidade
        message = result.get('message', '')
        is_fluent = print_response_quality(message, result.get('reflection_prompt'))
        
        results.append({
            "input": user_input,
            "has_reasoning": has_reasoning,
            "has_focal_argument": has_focal_argument,
            "next_step": result.get('next_step'),
            "is_fluent": is_fluent
        })
    
    # Resumo
    print("\n📋 RESUMO DO REASONING LOOP:")
    all_have_reasoning = all(r["has_reasoning"] for r in results)
    all_have_focal = all(r["has_focal_argument"] for r in results)
    all_fluent = all(r["is_fluent"] for r in results)
    
    print(f"   {'✅' if all_have_reasoning else '❌'} Todos têm reasoning")
    print(f"   {'✅' if all_have_focal else '❌'} Todos têm focal argument")
    print(f"   {'✅' if all_fluent else '⚠️'} Todas respostas fluidas")
    
    return all_have_reasoning and all_have_focal

# =============================================================================
# TESTE 2: FLUXO MULTI-AGENTE COMPLETO
# =============================================================================

def test_multi_agent_flow():
    """
    Valida fluxo: Orquestrador → (negociação) → Estruturador → Metodologista
    
    Simula cenário onde usuário aceita sugestão de chamar agentes.
    """
    print_separator("TESTE 2: FLUXO MULTI-AGENTE COMPLETO")
    
    # Turno 1: Input inicial
    print("--- Turno 1: Input inicial ---")
    user_input = "Quero investigar se pair programming com IA reduz bugs"
    print(f"📝 Input: '{user_input}'")
    
    state = create_initial_multi_agent_state(user_input, session_id="test-multi-agent-1")
    result_1 = orchestrator_node(state)
    
    print(f"   Next step: {result_1.get('next_step')}")
    print(f"   Suggestion: {result_1.get('agent_suggestion')}")
    print(f"   Message: {result_1.get('message', '')[:100]}...")
    
    # Turno 2: Usuário fornece mais contexto
    print("\n--- Turno 2: Usuário fornece contexto ---")
    user_input_2 = "Em equipes de 3-5 desenvolvedores Python, medindo bugs por sprint"
    print(f"📝 Input: '{user_input_2}'")
    
    # Atualizar state
    state['messages'].append(AIMessage(content=result_1.get('message', '')))
    state['messages'].append(HumanMessage(content=user_input_2))
    state['user_input'] = user_input_2
    state['focal_argument'] = result_1.get('focal_argument')
    
    result_2 = orchestrator_node(state)
    
    print(f"   Next step: {result_2.get('next_step')}")
    print(f"   Suggestion: {result_2.get('agent_suggestion')}")
    
    # Turno 3: Simular aceite do usuário para chamar Estruturador
    print("\n--- Turno 3: Simulando chamada ao Estruturador ---")
    
    # Chamar Estruturador diretamente (simulando aceite)
    state['messages'].append(AIMessage(content=result_2.get('message', '')))
    state['messages'].append(HumanMessage(content="Sim, pode estruturar"))
    
    result_structurer = structurer_node(state)
    
    structurer_output = result_structurer.get('structurer_output')
    if structurer_output:
        print(f"   ✅ Estruturador gerou output")
        print(f"   Questão: {structurer_output.get('structured_question', '')[:80]}...")
    else:
        print("   ❌ Estruturador não gerou output")
        return False
    
    # Turno 4: Metodologista avalia
    print("\n--- Turno 4: Metodologista avalia ---")
    
    state['structurer_output'] = structurer_output
    result_methodologist = decide_collaborative(state)
    
    methodologist_output = result_methodologist.get('methodologist_output')
    if methodologist_output:
        status = methodologist_output.get('status')
        print(f"   ✅ Metodologista decidiu: {status}")
        print(f"   Justificativa: {methodologist_output.get('justification', '')[:100]}...")
        
        if status == 'needs_refinement':
            improvements = methodologist_output.get('improvements', [])
            print(f"   Gaps identificados: {len(improvements)}")
            for imp in improvements[:2]:
                print(f"      - {imp.get('aspect')}: {imp.get('gap', '')[:50]}...")
    else:
        print("   ❌ Metodologista não gerou output")
        return False
    
    print("\n✅ Fluxo multi-agente executado com sucesso")
    return True

# =============================================================================
# TESTE 3: QUALIDADE DAS RESPOSTAS
# =============================================================================

def test_response_quality():
    """
    Valida que respostas são conversacionais, não rígidas.
    
    Critérios:
    - Usa linguagem natural
    - Faz perguntas abertas
    - Oferece opções
    - Não usa termos de pipeline/automação
    """
    print_separator("TESTE 3: QUALIDADE DAS RESPOSTAS")
    
    test_cases = [
        "Quero escrever um artigo sobre IA",
        "Na verdade, mudei de ideia, quero fazer revisão de literatura",
        "Algo sobre produtividade em desenvolvimento",
    ]
    
    fluent_count = 0
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"\n--- Caso {i} ---")
        print(f"📝 Input: '{user_input}'")
        
        state = create_initial_multi_agent_state(user_input, session_id=f"test-quality-{i}")
        result = orchestrator_node(state)
        
        message = result.get('message', '')
        reflection = result.get('reflection_prompt', '')
        
        print(f"\n💬 Resposta: {message[:150]}...")
        if reflection:
            print(f"💭 Reflexão: {reflection[:100]}...")
        
        is_fluent = print_response_quality(message, reflection)
        if is_fluent:
            fluent_count += 1
    
    print(f"\n📋 RESUMO: {fluent_count}/{len(test_cases)} respostas fluidas")
    
    return fluent_count >= len(test_cases) * 0.7  # 70% threshold

# =============================================================================
# TESTE 4: DETECÇÃO DE MUDANÇA DE DIREÇÃO
# =============================================================================

def test_direction_change():
    """
    Valida que sistema adapta quando usuário muda de direção.
    """
    print_separator("TESTE 4: DETECÇÃO DE MUDANÇA DE DIREÇÃO")
    
    # Turno 1: Direção inicial
    print("--- Turno 1: Direção inicial ---")
    state = create_initial_multi_agent_state(
        "Quero testar hipótese sobre LLMs",
        session_id="test-direction-1"
    )
    result_1 = orchestrator_node(state)
    
    focal_1 = result_1.get('focal_argument', {})
    intent_1 = focal_1.get('intent', 'unknown')
    print(f"   Intent inicial: {intent_1}")
    
    # Turno 2: Mudança de direção
    print("\n--- Turno 2: Mudança de direção ---")
    user_input_2 = "Na verdade, prefiro fazer revisão de literatura primeiro"
    
    state['messages'].append(AIMessage(content=result_1.get('message', '')))
    state['messages'].append(HumanMessage(content=user_input_2))
    state['user_input'] = user_input_2
    state['focal_argument'] = focal_1
    
    result_2 = orchestrator_node(state)
    
    focal_2 = result_2.get('focal_argument', {})
    intent_2 = focal_2.get('intent', 'unknown')
    print(f"   Intent após mudança: {intent_2}")
    
    # Verificar adaptação
    message = result_2.get('message', '')
    
    # Não deve questionar a mudança
    questioning_words = ['por que mudou', 'por que você mudou', 'não posso mudar']
    is_questioning = any(word in message.lower() for word in questioning_words)
    
    # Deve adaptar ao novo contexto
    adapting_words = ['revisão', 'literatura', 'sem problema', 'claro']
    is_adapting = any(word in message.lower() for word in adapting_words)
    
    print(f"\n   Questionou mudança: {'❌ Sim' if is_questioning else '✅ Não'}")
    print(f"   Adaptou ao contexto: {'✅ Sim' if is_adapting else '⚠️ Não claramente'}")
    
    return not is_questioning

# =============================================================================
# TESTE 5: ROUTER FUNCIONA CORRETAMENTE
# =============================================================================

def test_router_decisions():
    """
    Valida que router roteia corretamente baseado em next_step.
    """
    print_separator("TESTE 5: ROUTER DECISIONS")
    
    test_cases = [
        {"next_step": "explore", "agent_suggestion": None, "expected": "user"},
        {"next_step": "clarify", "agent_suggestion": None, "expected": "user"},
        {"next_step": "suggest_agent", "agent_suggestion": {"agent": "structurer", "justification": "test"}, "expected": "structurer"},
        {"next_step": "suggest_agent", "agent_suggestion": {"agent": "methodologist", "justification": "test"}, "expected": "methodologist"},
        {"next_step": "suggest_agent", "agent_suggestion": None, "expected": "user"},  # Fallback
    ]
    
    all_passed = True
    
    for case in test_cases:
        state = create_initial_multi_agent_state("test", session_id="test-router")
        state['next_step'] = case['next_step']
        state['agent_suggestion'] = case['agent_suggestion']
        
        destination = route_from_orchestrator(state)
        
        passed = destination == case['expected']
        status = "✅" if passed else "❌"
        print(f"{status} next_step={case['next_step']}, suggestion={case['agent_suggestion']} → {destination} (expected: {case['expected']})")
        
        if not passed:
            all_passed = False
    
    return all_passed

# =============================================================================
# MAIN
# =============================================================================

def main():
    print_separator("VALIDAÇÃO DE MATURIDADE DO SISTEMA")
    
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRO: ANTHROPIC_API_KEY não configurada no .env")
        sys.exit(1)
    
    results = {}
    
    try:
        # Teste 1: Reasoning Loop
        results['reasoning_loop'] = test_reasoning_loop()
        
        # Teste 2: Multi-Agent Flow
        results['multi_agent_flow'] = test_multi_agent_flow()
        
        # Teste 3: Response Quality
        results['response_quality'] = test_response_quality()
        
        # Teste 4: Direction Change
        results['direction_change'] = test_direction_change()
        
        # Teste 5: Router
        results['router'] = test_router_decisions()
        
        # Resumo final
        print_separator("RESUMO FINAL")
        
        all_passed = all(results.values())
        
        for test_name, passed in results.items():
            status = "✅" if passed else "❌"
            print(f"{status} {test_name.replace('_', ' ').title()}")
        
        print()
        if all_passed:
            print("🎉 SISTEMA MADURO - Todos os testes passaram!")
        else:
            failed = [k for k, v in results.items() if not v]
            print(f"⚠️ ATENÇÃO: {len(failed)} teste(s) precisam de revisão: {failed}")
        
        return 0 if all_passed else 1
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

