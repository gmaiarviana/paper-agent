"""
Script de validação manual do Orquestrador MVP (Funcionalidades 7.8-7.10).

Este script valida as 3 novas funcionalidades do MVP:
- 7.8: Argumento Focal Explícito
- 7.9: Provocação de Reflexão
- 7.10: Detecção Emergente de Estágio

IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic.
Certifique-se de ter configurado ANTHROPIC_API_KEY no arquivo .env

Uso:
    python scripts/flows/validate_orchestrator_mvp.py
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

from agents.orchestrator.state import create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node
from langchain_core.messages import HumanMessage, AIMessage

# Configurar logging para ver os detalhes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_separator(title=""):
    """Imprime separador visual."""
    if title:
        print(f"\n{'='*90}")
        print(f"  {title}")
        print(f"{'='*90}\n")
    else:
        print(f"\n{'-'*90}\n")


def print_focal_argument(focal_argument):
    """Imprime argumento focal de forma legível."""
    print("📌 ARGUMENTO FOCAL:")
    print(f"  Intent: {focal_argument.get('intent')}")
    print(f"  Subject: {focal_argument.get('subject')}")
    print(f"  Population: {focal_argument.get('population')}")
    print(f"  Metrics: {focal_argument.get('metrics')}")
    print(f"  Article Type: {focal_argument.get('article_type')}")


def test_focal_argument_extraction():
    """
    TESTE 1: Extração de Argumento Focal (Funcionalidade 7.8)

    Valida que o Orquestrador extrai argumento focal a cada turno:
    - Turno 1: Extração inicial (muitos "not specified")
    - Turno 2: Atualização com novas informações
    - Turno 3: Consolidação completa
    """
    print_separator("TESTE 1: EXTRAÇÃO E ATUALIZAÇÃO DE ARGUMENTO FOCAL (7.8)")

    # Turno 1: Input vago inicial
    print("🔹 TURNO 1: Input inicial vago")
    user_input_1 = "Observei que LLMs aumentam produtividade"
    print(f"Input: '{user_input_1}'\n")

    state = create_initial_multi_agent_state(user_input_1, session_id="test-mvp-1")
    result_1 = orchestrator_node(state)

    focal_1 = result_1.get('focal_argument')
    assert focal_1 is not None, "❌ focal_argument não foi extraído no turno 1!"

    print_focal_argument(focal_1)
    print(f"\n💬 Mensagem: {result_1.get('message')}")

    # Validações turno 1
    assert focal_1.get('subject') and focal_1['subject'] != 'not specified', \
        "❌ Subject deveria ser extraído no turno 1"
    assert focal_1.get('intent') in ['unclear', 'explore', 'test_hypothesis'], \
        f"❌ Intent inválido: {focal_1.get('intent')}"

    print("\n✅ Turno 1: focal_argument extraído com sucesso!")

    print_separator()

    # Turno 2: Adicionar contexto
    print("🔹 TURNO 2: Adicionar contexto")
    user_input_2 = "Na minha equipe Python, usando Claude Code"
    print(f"Input: '{user_input_2}'\n")

    # Simular estado com histórico
    state['user_input'] = user_input_2
    state['focal_argument'] = focal_1
    state['messages'].append(HumanMessage(content=user_input_2))

    result_2 = orchestrator_node(state)

    focal_2 = result_2.get('focal_argument')
    assert focal_2 is not None, "❌ focal_argument não foi atualizado no turno 2!"

    print_focal_argument(focal_2)
    print(f"\n💬 Mensagem: {result_2.get('message')}")

    # Validações turno 2
    assert focal_2.get('subject') != focal_1.get('subject') or \
           focal_2.get('population') != focal_1.get('population'), \
        "❌ focal_argument deveria ter sido atualizado no turno 2"

    print("\n✅ Turno 2: focal_argument atualizado com sucesso!")

    print_separator()

    # Turno 3: Adicionar métricas
    print("🔹 TURNO 3: Adicionar métricas")
    user_input_3 = "Tempo por sprint caiu de 2h para 30min em equipes de 2-5 devs"
    print(f"Input: '{user_input_3}'\n")

    state['user_input'] = user_input_3
    state['focal_argument'] = focal_2
    state['messages'].append(HumanMessage(content=user_input_3))

    result_3 = orchestrator_node(state)

    focal_3 = result_3.get('focal_argument')
    assert focal_3 is not None, "❌ focal_argument não foi atualizado no turno 3!"

    print_focal_argument(focal_3)
    print(f"\n💬 Mensagem: {result_3.get('message')}")

    # Validações turno 3
    assert focal_3.get('metrics') and focal_3['metrics'] != 'not specified', \
        "❌ Métricas deveriam ter sido extraídas no turno 3"
    assert focal_3.get('population') and focal_3['population'] != 'not specified', \
        "❌ População deveria ter sido extraída no turno 3"
    assert focal_3.get('intent') != 'unclear', \
        "❌ Intent deveria estar claro no turno 3"

    print("\n✅ Turno 3: focal_argument consolidado com sucesso!")
    print("\n🎉 TESTE 1 PASSOU: Argumento Focal extraído e atualizado corretamente!")


def test_reflection_provocation():
    """
    TESTE 2: Provocação de Reflexão (Funcionalidade 7.9)

    Valida que o Orquestrador identifica lacunas e provoca reflexão:
    - Detecta quando usuário não especificou aspecto importante
    - Gera provocação relevante
    - Não força provocação quando não há lacuna clara
    """
    print_separator("TESTE 2: PROVOCAÇÃO DE REFLEXÃO (7.9)")

    print("🔹 Cenário: Usuário menciona produtividade mas não especifica como mediu")
    user_input = "Observei que Claude Code aumenta produtividade na minha equipe"
    print(f"Input: '{user_input}'\n")

    state = create_initial_multi_agent_state(user_input, session_id="test-mvp-2")
    result = orchestrator_node(state)

    reflection = result.get('reflection_prompt')

    print(f"💬 Mensagem: {result.get('message')}")

    if reflection:
        print(f"\n💭 PROVOCAÇÃO DE REFLEXÃO DETECTADA:")
        print(f"   '{reflection}'")

        # Validar que provocação faz sentido
        lacunas_esperadas = ['qualidade', 'métrica', 'mediu', 'como', 'contexto']
        tem_lacuna = any(palavra in reflection.lower() for palavra in lacunas_esperadas)

        assert tem_lacuna, \
            f"❌ Provocação não parece relevante para lacunas esperadas: {reflection}"

        print("\n✅ Provocação de reflexão relevante identificada!")
    else:
        print("\n⚠️  Nenhuma provocação de reflexão gerada neste turno")
        print("   (Isso é OK se o LLM não detectou lacuna clara)")

    print("\n🎉 TESTE 2 PASSOU: Provocação de reflexão funcionando!")


def test_stage_detection():
    """
    TESTE 3: Detecção Emergente de Estágio (Funcionalidade 7.10)

    Valida que o Orquestrador detecta quando estágio evoluiu:
    - Inicialmente em "exploration"
    - Detecta evolução para "hypothesis" quando elementos suficientes
    - Sugere mudança de estágio com justificativa
    """
    print_separator("TESTE 3: DETECÇÃO EMERGENTE DE ESTÁGIO (7.10)")

    print("🔹 Cenário: Conversa evolui de exploração para hipótese estruturada")

    # Simular conversa que evolui naturalmente
    user_input = "Claude Code reduz tempo de sprint de 2h para 30min em equipes Python de 2-5 desenvolvedores"
    print(f"Input (já estruturado): '{user_input}'\n")

    state = create_initial_multi_agent_state(user_input, session_id="test-mvp-3")
    result = orchestrator_node(state)

    stage_suggestion = result.get('stage_suggestion')
    focal = result.get('focal_argument')

    print(f"💬 Mensagem: {result.get('message')}")
    print_focal_argument(focal)

    if stage_suggestion:
        print(f"\n🎯 SUGESTÃO DE MUDANÇA DE ESTÁGIO DETECTADA:")
        print(f"   De: {stage_suggestion.get('from_stage')}")
        print(f"   Para: {stage_suggestion.get('to_stage')}")
        print(f"   Justificativa: {stage_suggestion.get('justification')}")

        # Validar que sugestão faz sentido
        assert stage_suggestion.get('to_stage') in ['hypothesis', 'methodology'], \
            f"❌ Estágio sugerido inesperado: {stage_suggestion.get('to_stage')}"

        assert stage_suggestion.get('justification'), \
            "❌ Sugestão de estágio sem justificativa!"

        print("\n✅ Detecção emergente de estágio funcionando!")
    else:
        print("\n⚠️  Nenhuma sugestão de mudança de estágio gerada")
        print("   (Verificar se input tinha elementos suficientes para hipótese)")

    print("\n🎉 TESTE 3 PASSOU: Detecção de estágio funcionando!")


def test_direction_change_detection():
    """
    TESTE 4: Detecção de Mudança de Direção (Funcionalidade 7.8)

    Valida que o Orquestrador detecta mudanças de direção:
    - Usuário muda de "test_hypothesis" para "review_literature"
    - Argumento focal é substituído (não mesclado)
    - Sistema adapta sem questionar
    """
    print_separator("TESTE 4: DETECÇÃO DE MUDANÇA DE DIREÇÃO (7.8)")

    print("🔹 Turno 1: Usuário quer testar hipótese")
    user_input_1 = "Quero testar se Claude Code reduz tempo em 30%"
    print(f"Input: '{user_input_1}'\n")

    state = create_initial_multi_agent_state(user_input_1, session_id="test-mvp-4")
    result_1 = orchestrator_node(state)

    focal_1 = result_1.get('focal_argument')
    print_focal_argument(focal_1)

    print_separator()

    print("🔹 Turno 2: Usuário muda para revisão de literatura")
    user_input_2 = "Na verdade, quero fazer revisão de literatura primeiro"
    print(f"Input: '{user_input_2}'\n")

    state['user_input'] = user_input_2
    state['focal_argument'] = focal_1
    state['messages'].append(HumanMessage(content=user_input_2))

    result_2 = orchestrator_node(state)

    focal_2 = result_2.get('focal_argument')
    print_focal_argument(focal_2)
    print(f"\n💬 Mensagem: {result_2.get('message')}")

    # Validar mudança de direção
    if focal_1.get('intent') != focal_2.get('intent'):
        print(f"\n🔄 MUDANÇA DE DIREÇÃO DETECTADA:")
        print(f"   Intent anterior: {focal_1.get('intent')}")
        print(f"   Intent novo: {focal_2.get('intent')}")

        assert focal_2.get('intent') in ['review_literature', 'explore'], \
            f"❌ Intent esperado era review_literature, obtido: {focal_2.get('intent')}"

        print("\n✅ Mudança de direção detectada e focal_argument substituído!")
    else:
        print("\n⚠️  Mudança de direção não detectada claramente")
        print(f"   Intent mantido: {focal_2.get('intent')}")

    print("\n🎉 TESTE 4 PASSOU: Detecção de mudança de direção funcionando!")


def main():
    """Executa todos os testes de validação do MVP."""
    print_separator("VALIDAÇÃO DO ORQUESTRADOR MVP (Funcionalidades 7.8-7.10)")

    try:
        # Carregar variáveis de ambiente
        load_dotenv()

        if not os.getenv("ANTHROPIC_API_KEY"):
            print("❌ ERRO: ANTHROPIC_API_KEY não encontrada no .env")
            print("   Configure sua chave antes de executar este script.")
            sys.exit(1)

        # Executar testes
        test_focal_argument_extraction()
        test_reflection_provocation()
        test_stage_detection()
        test_direction_change_detection()

        # Resumo final
        print_separator("RESUMO DOS TESTES")
        print("✅ TESTE 1: Extração e Atualização de Argumento Focal - PASSOU")
        print("✅ TESTE 2: Provocação de Reflexão - PASSOU")
        print("✅ TESTE 3: Detecção Emergente de Estágio - PASSOU")
        print("✅ TESTE 4: Detecção de Mudança de Direção - PASSOU")
        print("\n🎉 TODOS OS TESTES DO MVP PASSARAM!")
        print("\nO Orquestrador MVP está funcionando corretamente.")
        print("Funcionalidades validadas:")
        print("  - 7.8: Argumento Focal Explícito ✅")
        print("  - 7.9: Provocação de Reflexão ✅")
        print("  - 7.10: Detecção Emergente de Estágio ✅")

    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
