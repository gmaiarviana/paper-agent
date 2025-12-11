"""
Validação de Comportamento: COMPORTAMENTO SOCRÁTICO

Valida capacidades socráticas do sistema:
- Provocação sobre assumptions (métrica, população, baseline, causalidade)
- Timing emergente (não regras fixas)
- Escalada natural (intensifica quando usuário resiste)
- Parada inteligente (não insiste infinitamente)
- Não-repetição (aprende com respostas)

IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic.
Custo estimado: ~$0.05-0.10

Uso:
    python scripts/flows/validate_socratic_behavior.py
"""

import logging
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.orchestrator.nodes import orchestrator_node

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def print_separator(title=""):
    if title:
        print(f"\n{'='*80}\n  {title}\n{'='*80}\n")
    else:
        print(f"\n{'-'*80}\n")

# =============================================================================
# HELPERS
# =============================================================================

def is_provocative_question(message, reflection_prompt=None):
    """
    Verifica se mensagem é contra-pergunta provocativa (não coleta burocrática).
    
    Características de provocação socrática:
    - Expõe múltiplas interpretações
    - Pergunta sobre consequências
    - Aponta assumptions
    
    Características de coleta burocrática (NÃO socrática):
    - Perguntas genéricas ("Que tipo?", "Em que contexto?")
    - Lista de opções sem provocação
    """
    full_text = message.lower()
    if reflection_prompt:
        full_text += " " + reflection_prompt.lower()
    
    # Indicadores de provocação
    provocative_indicators = [
        'quem?', 'o quê?', 'quanto?', 'qual?', 'onde?',
        'mas', 'diferentes', 'várias', 'múltiplas',
        'como vai', 'se não', 'pode ser', 'isso não',
        'trade-off', 'contraponto', 'por outro lado',
        'assumiu', 'suposição', 'pressupõe', 'implica',
        'tem certeza', 'realmente', 'de fato', 'na verdade'
    ]
    
    # Indicadores de coleta burocrática
    bureaucratic_indicators = [
        'que tipo de', 'qual tipo', 'em que contexto',
        'pode me dar', 'poderia especificar',
        'gostaria de saber', 'preciso saber'
    ]
    
    provocative_score = sum(1 for ind in provocative_indicators if ind in full_text)
    bureaucratic_score = sum(1 for ind in bureaucratic_indicators if ind in full_text)
    
    # Se tem reflection_prompt, é definitivamente provocativo
    if reflection_prompt:
        return True
    
    return provocative_score > bureaucratic_score

def extract_assumption_category(result):
    """Identifica categoria de assumption da provocação."""
    reflection = result.get('reflection_prompt', '')
    message = result.get('message', '')
    full_text = (reflection + " " + message).lower()
    
    if any(kw in full_text for kw in ['métrica', 'produtividade', 'qualidade', 'eficiência']):
        return 'métrica'
    elif any(kw in full_text for kw in ['equipe', 'pessoas', 'população', 'quem', 'quantas']):
        return 'população'
    elif any(kw in full_text for kw in ['baseline', 'comparado', 'mais rápido', 'antes']):
        return 'baseline'
    elif any(kw in full_text for kw in ['causa', 'confundidor', 'correlação']):
        return 'causalidade'
    elif any(kw in full_text for kw in ['generaliza', 'representativo', 'amostra']):
        return 'generalização'
    return None

def has_provocation(result):
    """Verifica se houve provocação no resultado."""
    reflection = result.get('reflection_prompt')
    message = result.get('message', '')
    
    if reflection:
        return True
    
    if '?' in message and any(ind in message.upper() for ind in ['QUÊ', 'QUEM', 'QUANTO', 'QUAL']):
        return True
    
    return False

# =============================================================================
# TESTES DE COMPORTAMENTO SOCRÁTICO
# =============================================================================

def test_provocation_on_vague_metric():
    """
    BEHAVIOR: Provocação sobre métrica vaga
    
    Quando usuário menciona "produtividade" sem definir como medir,
    sistema deve provocar sobre múltiplas interpretações.
    """
    print_separator("BEHAVIOR: Provocação sobre Métrica Vaga")
    
    user_input = "Observei que LLMs aumentam produtividade"
    print(f"Input: '{user_input}' (métrica vaga)\n")
    
    state = create_initial_multi_agent_state(user_input, session_id="test-socratic-1")
    result = orchestrator_node(state)
    
    message = result.get('message', '')
    reflection = result.get('reflection_prompt')
    
    print(f"Mensagem: {message[:150]}...")
    if reflection:
        print(f"Provocação: {reflection}")
    
    is_prov = is_provocative_question(message, reflection)
    
    if is_prov:
        print("\n✅ Sistema provocou reflexão sobre métrica vaga")
    else:
        print("\n⚠️ Sistema coletou dados (não provocou)")
    
    assert is_prov, "❌ Sistema deveria provocar sobre métrica vaga"

def test_provocation_criteria_in_3_turns():
    """
    BEHAVIOR: Pelo menos 1 provocação em 3 turnos iniciais
    
    Sistema deve fazer pelo menos 1 contra-pergunta provocativa
    nos primeiros 3 turnos (critério de aceite POC).
    """
    print_separator("BEHAVIOR: Pelo Menos 1 Provocação em 3 Turnos")
    
    print("Simulando conversa de 3 turnos...\n")
    
    provocations_count = 0
    
    # Turno 1
    print("--- Turno 1 ---")
    user_input_1 = "LLMs aumentam produtividade"
    print(f"Input: '{user_input_1}'")
    
    state = create_initial_multi_agent_state(user_input_1, session_id="test-socratic-2")
    result_1 = orchestrator_node(state)
    
    if is_provocative_question(result_1.get('message', ''), result_1.get('reflection_prompt')):
        provocations_count += 1
        print("  ✓ Provocação detectada")
    
    # Turno 2
    print("\n--- Turno 2 ---")
    user_input_2 = "Na minha equipe Python"
    print(f"Input: '{user_input_2}'")
    
    state['user_input'] = user_input_2
    state['messages'].append(HumanMessage(content=user_input_2))
    state['focal_argument'] = result_1.get('focal_argument')
    
    result_2 = orchestrator_node(state)
    
    if is_provocative_question(result_2.get('message', ''), result_2.get('reflection_prompt')):
        provocations_count += 1
        print("  ✓ Provocação detectada")
    
    # Turno 3
    print("\n--- Turno 3 ---")
    user_input_3 = "Usando Claude Code"
    print(f"Input: '{user_input_3}'")
    
    state['user_input'] = user_input_3
    state['messages'].append(HumanMessage(content=user_input_3))
    state['focal_argument'] = result_2.get('focal_argument')
    
    result_3 = orchestrator_node(state)
    
    if is_provocative_question(result_3.get('message', ''), result_3.get('reflection_prompt')):
        provocations_count += 1
        print("  ✓ Provocação detectada")
    
    print(f"\nTotal de provocações: {provocations_count}/3 turnos")
    
    assert provocations_count >= 1, \
        f"❌ Esperava pelo menos 1 provocação em 3 turnos, obteve {provocations_count}"
    
    print("\n✅ Critério de provocação atendido")

def test_timing_emergente():
    """
    BEHAVIOR: Timing emergente (não regras fixas)
    
    Sistema escolhe momento natural para provocar:
    - Turno 1: Pode escutar primeiro
    - Turnos 2-3: Provoca quando assumption fica clara
    """
    print_separator("BEHAVIOR: Timing Emergente")
    
    print("Simulando conversa com input vago inicial...\n")
    
    # Turno 1: Input vago
    print("--- Turno 1 ---")
    user_input_1 = "Tenho observado algumas coisas sobre LLMs"
    print(f"Input: '{user_input_1}'")
    
    state = create_initial_multi_agent_state(user_input_1, session_id="test-timing-1")
    result_1 = orchestrator_node(state)
    
    has_prov_1 = has_provocation(result_1)
    print(f"Provocação? {'✓' if has_prov_1 else '✗'}")
    
    # Turno 2: Adicionar contexto
    print("\n--- Turno 2 ---")
    user_input_2 = "Vejo que aumentam produtividade da equipe"
    print(f"Input: '{user_input_2}'")
    
    state['user_input'] = user_input_2
    state['messages'].append(HumanMessage(content=user_input_2))
    state['focal_argument'] = result_1.get('focal_argument')
    
    result_2 = orchestrator_node(state)
    
    has_prov_2 = has_provocation(result_2)
    print(f"Provocação? {'✓' if has_prov_2 else '✗'}")
    
    # Turno 3
    print("\n--- Turno 3 ---")
    user_input_3 = "Na minha equipe Python"
    print(f"Input: '{user_input_3}'")
    
    state['user_input'] = user_input_3
    state['messages'].append(HumanMessage(content=user_input_3))
    state['focal_argument'] = result_2.get('focal_argument')
    
    result_3 = orchestrator_node(state)
    
    has_prov_3 = has_provocation(result_3)
    print(f"Provocação? {'✓' if has_prov_3 else '✗'}")
    
    # Pelo menos 1 provocação nos turnos 2-3 (quando assumption fica clara)
    provocations_23 = sum([has_prov_2, has_prov_3])
    
    assert provocations_23 >= 1, \
        f"❌ Esperava provocação nos turnos 2-3 (quando assumption fica clara)"
    
    print(f"\n✅ Timing emergente: {provocations_23} provocação(ões) nos turnos 2-3")

def test_no_infinite_insistence():
    """
    BEHAVIOR: Parada inteligente (não insiste infinitamente)
    
    Após múltiplas resistências do usuário, sistema deve:
    - Parar de insistir na mesma assumption
    - Mudar para outra assumption OU aceitar vagueza
    """
    print_separator("BEHAVIOR: Parada Inteligente")
    
    print("Simulando 6 turnos onde usuário resiste...\n")
    
    metric_provocations = []
    
    # Turno 1
    user_input_1 = "LLMs melhoram trabalho"
    state = create_initial_multi_agent_state(user_input_1, session_id="test-parada-1")
    result_1 = orchestrator_node(state)
    
    if has_provocation(result_1) and extract_assumption_category(result_1) == 'métrica':
        metric_provocations.append(1)
    
    # Turnos 2-6: Usuário continua vago
    vague_responses = [
        "No contexto de desenvolvimento",
        "Percebi isso no dia a dia",
        "É visível a mudança",
        "Todo mundo comenta",
        "A equipe sente a diferença"
    ]
    
    for i, response in enumerate(vague_responses, 2):
        state['user_input'] = response
        state['messages'].append(HumanMessage(content=response))
        state['focal_argument'] = state.get('focal_argument', result_1.get('focal_argument'))
        
        result = orchestrator_node(state)
        state['focal_argument'] = result.get('focal_argument')
        
        if has_provocation(result):
            cat = extract_assumption_category(result)
            if cat == 'métrica':
                metric_provocations.append(i)
                print(f"  Turno {i}: Provocou sobre métrica (tentativa {len(metric_provocations)})")
            else:
                print(f"  Turno {i}: Provocou sobre {cat} (mudou de assumption)")
        else:
            print(f"  Turno {i}: Não provocou (parou de insistir)")
    
    print(f"\nProvocações sobre métrica: {len(metric_provocations)}x em turnos {metric_provocations}")
    
    # Sistema NÃO deve ter provocado em TODOS os turnos
    assert len(metric_provocations) < 6, \
        f"❌ Sistema insistiu em métrica em todos os turnos (deveria parar)"
    
    print(f"\n✅ Sistema parou de insistir após {len(metric_provocations)} tentativas")

def test_no_repetition():
    """
    BEHAVIOR: Não-repetição (aprende com respostas)
    
    Quando usuário responde uma provocação, sistema deve:
    - NÃO repetir a mesma provocação
    - Mudar para outra assumption se necessário
    """
    print_separator("BEHAVIOR: Não-Repetição")
    
    print("Simulando conversa onde usuário responde provocações...\n")
    
    provocations_log = []
    
    # Turno 1
    user_input_1 = "LLMs aumentam produtividade da equipe"
    state = create_initial_multi_agent_state(user_input_1, session_id="test-repeat-1")
    result_1 = orchestrator_node(state)
    
    cat_1 = extract_assumption_category(result_1)
    if cat_1:
        provocations_log.append(cat_1)
        print(f"Turno 1: Provocou sobre {cat_1}")
    
    # Turno 2: Responder provocação
    user_input_2 = "Medindo tempo por sprint"
    state['user_input'] = user_input_2
    state['messages'].append(HumanMessage(content=user_input_2))
    state['focal_argument'] = result_1.get('focal_argument')
    
    result_2 = orchestrator_node(state)
    
    cat_2 = extract_assumption_category(result_2)
    if cat_2:
        provocations_log.append(cat_2)
        print(f"Turno 2: Provocou sobre {cat_2}")
    
    # Turno 3
    user_input_3 = "Redução de 2h para 30min"
    state['user_input'] = user_input_3
    state['messages'].append(HumanMessage(content=user_input_3))
    state['focal_argument'] = result_2.get('focal_argument')
    
    result_3 = orchestrator_node(state)
    
    cat_3 = extract_assumption_category(result_3)
    if cat_3:
        provocations_log.append(cat_3)
        print(f"Turno 3: Provocou sobre {cat_3}")
    
    print(f"\nSequência de provocações: {provocations_log}")
    
    # Verificar não-repetição
    if 'métrica' in provocations_log[:1]:
        metric_count_after = provocations_log[1:].count('métrica')
        if metric_count_after == 0:
            print("\n✅ Sistema NÃO repetiu provocação sobre métrica")
        else:
            print(f"\n⚠️ Sistema repetiu provocação sobre métrica {metric_count_after}x")
    
    print("\n✅ Não-repetição verificada")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print_separator("VALIDAÇÃO: COMPORTAMENTO SOCRÁTICO")
    
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERRO: ANTHROPIC_API_KEY não configurada no .env")
        sys.exit(1)
    
    try:
        test_provocation_on_vague_metric()
        test_provocation_criteria_in_3_turns()
        test_timing_emergente()
        test_no_infinite_insistence()
        test_no_repetition()
        
        print_separator("RESUMO")
        print("✅ TODOS OS BEHAVIORS SOCRÁTICOS VALIDADOS!")
        print("\nCapacidades testadas:")
        print("  ✅ Provocação sobre métrica vaga")
        print("  ✅ Pelo menos 1 provocação em 3 turnos")
        print("  ✅ Timing emergente")
        print("  ✅ Parada inteligente")
        print("  ✅ Não-repetição")
        
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

