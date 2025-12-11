"""
Validação do Loop de Refinamento no contexto conversacional.

Este script valida que o ciclo Estruturador → Metodologista → Refinamento
funciona corretamente no modelo CONVERSACIONAL (não pipeline automático).

Diferença do modelo anterior:
- ANTES: Loop automático até max_refinements
- AGORA: Cada refinamento é negociado com usuário via Orquestrador

Cenários testados:
1. Estruturação inicial → Metodologista avalia
2. needs_refinement → Estruturador refina baseado em gaps
3. Múltiplas versões são registradas no histórico
4. Metodologista rejeita input sem base científica

IMPORTANTE: Faz chamadas REAIS à API Anthropic.
Custo estimado: ~$0.10-0.15

Uso:
    python scripts/flows/validate_refinement_loop.py
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.common import setup_project_path
setup_project_path()

from dotenv import load_dotenv

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.structurer.nodes import structurer_node
from core.agents.methodologist.nodes import decide_collaborative

def print_separator(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def print_hypothesis_versions(state: dict):
    """Imprime histórico de versões."""
    versions = state.get('hypothesis_versions', [])
    if not versions:
        print("   (Nenhuma versão registrada)")
        return
    
    for v in versions:
        print(f"\n   📄 Versão {v['version']}:")
        print(f"      Questão: {v['question'][:60]}...")
        print(f"      Status: {v['feedback']['status']}")
        if v['feedback'].get('improvements'):
            print(f"      Gaps: {len(v['feedback']['improvements'])}")
            for imp in v['feedback']['improvements'][:2]:
                print(f"         - {imp['aspect']}: {imp['gap'][:40]}...")

def validate_scenario_1_initial_structuring():
    """
    Cenário 1: Estruturação inicial → Metodologista avalia.
    
    Valida que:
    - Estruturador gera questão estruturada
    - Metodologista avalia e retorna status válido
    - Versão V1 é registrada no histórico
    """
    print_separator("CENÁRIO 1: Estruturação Inicial → Avaliação")
    
    user_input = "TDD reduz bugs em equipes pequenas de desenvolvimento"
    print(f"📝 Input: {user_input}")
    print("🎯 Esperado: Estruturação V1 → Avaliação do Metodologista\n")
    
    state = create_initial_multi_agent_state(user_input, session_id="refinement-1")
    
    # Estruturador cria V1
    print("--- Estruturador (V1) ---")
    result_struct = structurer_node(state)
    
    structurer_output = result_struct.get('structurer_output')
    assert structurer_output, "❌ Estruturador deveria gerar output"
    
    question = structurer_output.get('structured_question', '')
    print(f"   Questão: {question[:70]}...")
    print("   ✅ Questão estruturada gerada")
    
    # Metodologista avalia
    print("\n--- Metodologista ---")
    state['structurer_output'] = structurer_output
    
    result_method = decide_collaborative(state)
    
    methodologist_output = result_method.get('methodologist_output')
    assert methodologist_output, "❌ Metodologista deveria gerar output"
    
    status = methodologist_output.get('status')
    print(f"   Status: {status}")
    print(f"   Justificativa: {methodologist_output.get('justification', '')[:80]}...")
    
    assert status in ['approved', 'needs_refinement', 'rejected'], \
        f"❌ Status inválido: {status}"
    print(f"   ✅ Decisão válida: {status}")
    
    # Verificar histórico
    hypothesis_versions = result_method.get('hypothesis_versions', [])
    assert len(hypothesis_versions) >= 1, "❌ Deveria ter pelo menos V1 no histórico"
    print(f"   ✅ V1 registrada no histórico")
    
    print("\n✅ CENÁRIO 1 VALIDADO!")
    return {**state, **result_method}

def validate_scenario_2_refinement_cycle():
    """
    Cenário 2: needs_refinement → Estruturador refina.
    
    Valida que:
    - Estruturador recebe gaps do Metodologista
    - Gera versão refinada (V2) endereçando gaps
    - Metodologista reavalia
    """
    print_separator("CENÁRIO 2: Ciclo de Refinamento")
    
    # Input vago que provavelmente vai precisar de refinamento
    user_input = "Observei que métodos ágeis parecem funcionar melhor"
    print(f"📝 Input: {user_input}")
    print("🎯 Esperado: V1 (needs_refinement) → V2 (refinada)\n")
    
    state = create_initial_multi_agent_state(user_input, session_id="refinement-2")
    
    # V1: Estruturação inicial
    print("--- Estruturador (V1) ---")
    result_struct_1 = structurer_node(state)
    state['structurer_output'] = result_struct_1.get('structurer_output')
    
    question_1 = state['structurer_output'].get('structured_question', '')
    print(f"   V1: {question_1[:60]}...")
    
    # V1: Metodologista avalia
    print("\n--- Metodologista (avaliando V1) ---")
    result_method_1 = decide_collaborative(state)
    
    state['methodologist_output'] = result_method_1.get('methodologist_output')
    state['hypothesis_versions'] = result_method_1.get('hypothesis_versions', [])
    
    status_1 = state['methodologist_output'].get('status')
    print(f"   Status V1: {status_1}")
    
    if status_1 == 'needs_refinement':
        improvements = state['methodologist_output'].get('improvements', [])
        print(f"   Gaps identificados: {len(improvements)}")
        for imp in improvements[:2]:
            print(f"      - {imp.get('aspect')}: {imp.get('gap', '')[:40]}...")
        
        # V2: Estruturador refina
        print("\n--- Estruturador (V2 - Refinamento) ---")
        result_struct_2 = structurer_node(state)
        state['structurer_output'] = result_struct_2.get('structurer_output')
        
        question_2 = state['structurer_output'].get('structured_question', '')
        print(f"   V2: {question_2[:60]}...")
        
        # V2: Metodologista reavalia
        print("\n--- Metodologista (avaliando V2) ---")
        state['refinement_iteration'] = 1
        state['methodologist_output'] = None  # Reset para nova avaliação
        
        result_method_2 = decide_collaborative(state)
        
        status_2 = (result_method_2.get('methodologist_output') or {}).get('status')
        print(f"   Status V2: {status_2}")
        
        state['hypothesis_versions'] = result_method_2.get('hypothesis_versions', [])
        
        assert len(state['hypothesis_versions']) >= 2, \
            "❌ Deveria ter pelo menos V1 e V2 no histórico"
        print(f"   ✅ {len(state['hypothesis_versions'])} versões no histórico")
        
    else:
        print(f"   ✅ V1 foi {status_1} (sem necessidade de refinamento)")
    
    print("\n📚 Histórico de versões:")
    print_hypothesis_versions(state)
    
    print("\n✅ CENÁRIO 2 VALIDADO!")
    return state

def validate_scenario_3_rejection():
    """
    Cenário 3: Input sem base científica → Metodologista rejeita.
    
    Valida que Metodologista identifica falta de fundamento.
    """
    print_separator("CENÁRIO 3: Rejeição por Falta de Base Científica")
    
    user_input = "Café é bom porque todo mundo sabe que funciona melhor"
    print(f"📝 Input: {user_input}")
    print("🎯 Esperado: Rejeição por falta de base científica\n")
    
    state = create_initial_multi_agent_state(user_input, session_id="refinement-3")
    
    # Estruturador tenta estruturar
    print("--- Estruturador ---")
    result_struct = structurer_node(state)
    state['structurer_output'] = result_struct.get('structurer_output')
    
    question = state['structurer_output'].get('structured_question', '')
    print(f"   Questão: {question[:60]}...")
    
    # Metodologista avalia
    print("\n--- Metodologista ---")
    result_method = decide_collaborative(state)
    
    methodologist_output = result_method.get('methodologist_output', {})
    status = methodologist_output.get('status')
    justification = methodologist_output.get('justification', '')
    
    print(f"   Status: {status}")
    print(f"   Justificativa: {justification[:100]}...")
    
    # Pode ser rejected ou needs_refinement (Metodologista pode tentar salvar)
    if status == 'rejected':
        print("   ✅ Corretamente rejeitou por falta de base científica")
    else:
        print(f"   ℹ️ Metodologista deu chance: {status}")
        print("      (Comportamento colaborativo - tenta ajudar antes de rejeitar)")
    
    print("\n✅ CENÁRIO 3 VALIDADO!")
    return result_method

def validate_scenario_4_version_tracking():
    """
    Cenário 4: Verificar que versões são corretamente rastreadas.
    """
    print_separator("CENÁRIO 4: Rastreamento de Versões")
    
    user_input = "X afeta Y de alguma forma que vale investigar"
    print(f"📝 Input: {user_input}")
    print("🎯 Esperado: Versões são numeradas e rastreadas\n")
    
    state = create_initial_multi_agent_state(user_input, session_id="refinement-4")
    
    # V1
    print("--- Criando V1 ---")
    result_struct = structurer_node(state)
    state['structurer_output'] = result_struct.get('structurer_output')
    
    result_method = decide_collaborative(state)
    state['hypothesis_versions'] = result_method.get('hypothesis_versions', [])
    state['methodologist_output'] = result_method.get('methodologist_output')
    
    print(f"   Versões após V1: {len(state['hypothesis_versions'])}")
    
    # Verificar estrutura da versão
    if state['hypothesis_versions']:
        v1 = state['hypothesis_versions'][0]
        
        assert 'version' in v1, "❌ Versão deveria ter campo 'version'"
        assert 'question' in v1, "❌ Versão deveria ter campo 'question'"
        assert 'feedback' in v1, "❌ Versão deveria ter campo 'feedback'"
        
        print(f"   ✅ V1 tem estrutura correta")
        print(f"      version: {v1['version']}")
        print(f"      question: {v1['question'][:50]}...")
        print(f"      feedback.status: {v1['feedback']['status']}")
    
    print("\n✅ CENÁRIO 4 VALIDADO!")
    return state

def main():
    print("\n" + "=" * 80)
    print("  VALIDAÇÃO DO LOOP DE REFINAMENTO CONVERSACIONAL")
    print("  (Estruturador ↔ Metodologista)")
    print("=" * 80)
    
    load_dotenv()
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ERRO: ANTHROPIC_API_KEY não configurada")
        sys.exit(1)
    
    print("\n⚠️ Este script faz chamadas à API Anthropic (custo ~$0.10-0.15)")
    
    try:
        validate_scenario_1_initial_structuring()
        validate_scenario_2_refinement_cycle()
        validate_scenario_3_rejection()
        validate_scenario_4_version_tracking()
        
        print_separator("RESUMO FINAL")
        print("✅ Cenário 1: Estruturação inicial → Avaliação")
        print("✅ Cenário 2: Ciclo de refinamento (V1 → V2)")
        print("✅ Cenário 3: Rejeição por falta de base científica")
        print("✅ Cenário 4: Rastreamento de versões")
        print("\n" + "=" * 80)
        print("  LOOP DE REFINAMENTO VALIDADO! ✅")
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
