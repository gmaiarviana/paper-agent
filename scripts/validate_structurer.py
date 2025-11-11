"""
Script de validação manual do agente Estruturador.

Este script permite testar manualmente o Estruturador implementado no Épico 3.2:
- structurer_node: Organiza ideias vagas em questões estruturadas

IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic.
Certifique-se de ter configurado ANTHROPIC_API_KEY no arquivo .env

Uso:
    python scripts/validate_structurer.py
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.orchestrator import create_initial_multi_agent_state
from agents.structurer import structurer_node

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


def print_structurer_output(output):
    """Imprime o output do estruturador de forma formatada."""
    print("\n📋 Output estruturado:")
    print(f"  Questão de pesquisa: {output['structured_question']}")
    print(f"\n  Elementos extraídos:")
    print(f"    • Contexto: {output['elements']['context']}")
    print(f"    • Problema: {output['elements']['problem']}")
    print(f"    • Contribuição: {output['elements']['contribution']}")


def test_vague_observation_tech():
    """Testa estruturação de observação vaga sobre tecnologia."""
    print_separator("TESTE 1: OBSERVAÇÃO VAGA - TECNOLOGIA")

    user_input = "Observei que desenvolver com Claude Code é mais rápido que métodos tradicionais"

    print(f"Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    # Exibir resultados
    print_structurer_output(result['structurer_output'])
    print(f"\nPróximo estágio: {result['current_stage']}")
    print(f"Mensagens adicionadas: {len(result['messages'])}")

    # Validações
    output = result['structurer_output']
    assert 'structured_question' in output, "❌ Falta structured_question"
    assert 'elements' in output, "❌ Falta elements"
    assert 'context' in output['elements'], "❌ Falta context"
    assert 'problem' in output['elements'], "❌ Falta problem"
    assert 'contribution' in output['elements'], "❌ Falta contribution"
    assert result['current_stage'] == "validating", "❌ current_stage deveria ser 'validating'"
    assert len(result['messages']) == 1, "❌ Deveria ter 1 mensagem"

    print("\n✅ Teste 1 passou!")


def test_vague_observation_education():
    """Testa estruturação de observação vaga sobre educação."""
    print_separator("TESTE 2: OBSERVAÇÃO VAGA - EDUCAÇÃO")

    user_input = "Notei que alunos se engajam mais em aulas com elementos interativos"

    print(f"Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    # Exibir resultados
    print_structurer_output(result['structurer_output'])
    print(f"\nPróximo estágio: {result['current_stage']}")

    # Validações
    output = result['structurer_output']
    assert len(output['structured_question']) > 10, "❌ Questão muito curta"
    assert output['structured_question'] != user_input, "❌ Questão igual ao input"
    assert result['current_stage'] == "validating", "❌ Estágio incorreto"

    print("\n✅ Teste 2 passou!")


def test_very_vague_observation():
    """Testa estruturação de observação muito vaga."""
    print_separator("TESTE 3: OBSERVAÇÃO MUITO VAGA")

    user_input = "Algumas coisas funcionam melhor do que outras em certos contextos"

    print(f"Input do usuário: {user_input}\n")
    print("⚠️  Este input é propositalmente muito vago para testar robustez do Estruturador\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    # Exibir resultados
    print_structurer_output(result['structurer_output'])
    print(f"\nPróximo estágio: {result['current_stage']}")

    # Validações - Deve estruturar mesmo input muito vago (comportamento colaborativo)
    output = result['structurer_output']
    assert output['structured_question'] is not None, "❌ Falta questão estruturada"
    assert len(output['structured_question']) > 0, "❌ Questão vazia"

    # Não deve ter linguagem de rejeição
    message_content = result['messages'][0].content.lower()
    assert "rejeita" not in message_content, "❌ Estruturador não deve rejeitar"
    assert "inválid" not in message_content, "❌ Estruturador não deve invalidar"

    print("\n✅ Teste 3 passou! (Estruturador foi colaborativo, não rejeitou)")


def test_output_structure():
    """Testa estrutura consistente do output."""
    print_separator("TESTE 4: ESTRUTURA DO OUTPUT")

    user_input = "Percebo que equipes pequenas entregam mais rápido"

    print(f"Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do estruturador
    result = structurer_node(state)

    print("Validando estrutura do output...")

    # Validar estrutura completa
    assert 'structurer_output' in result, "❌ Falta structurer_output no result"
    assert 'current_stage' in result, "❌ Falta current_stage no result"
    assert 'messages' in result, "❌ Falta messages no result"

    output = result['structurer_output']
    assert isinstance(output, dict), "❌ structurer_output deve ser dict"
    assert isinstance(output['elements'], dict), "❌ elements deve ser dict"
    assert isinstance(output['structured_question'], str), "❌ structured_question deve ser str"
    assert isinstance(output['elements']['context'], str), "❌ context deve ser str"
    assert isinstance(output['elements']['problem'], str), "❌ problem deve ser str"
    assert isinstance(output['elements']['contribution'], str), "❌ contribution deve ser str"

    print("\n📊 Estrutura validada:")
    print("  ✓ structurer_output: dict")
    print("  ✓ structured_question: str")
    print("  ✓ elements: dict")
    print("    ✓ context: str")
    print("    ✓ problem: str")
    print("    ✓ contribution: str")
    print("  ✓ current_stage: str")
    print("  ✓ messages: list")

    print("\n✅ Teste 4 passou!")


def main():
    """Executa todos os testes de validação."""
    # Carregar variáveis de ambiente
    load_dotenv()

    # Verificar se API key está configurada
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ERRO: ANTHROPIC_API_KEY não está configurada no arquivo .env")
        print("   Configure a chave antes de executar este script.")
        sys.exit(1)

    print("\n" + "="*80)
    print("  VALIDAÇÃO MANUAL DO ESTRUTURADOR - ÉPICO 3.2")
    print("="*80)
    print("\nEste script valida o componente implementado na funcionalidade 3.2:")
    print("  • structurer_node - Nó que organiza ideias vagas em questões estruturadas")
    print("\nComportamento esperado:")
    print("  ✓ Extrai: contexto, problema, contribuição potencial")
    print("  ✓ Gera questão de pesquisa estruturada")
    print("  ✓ Colaborativo (não rejeita ideias)")
    print("  ✓ Não valida rigor científico (responsabilidade do Metodologista)")
    print("\n⚠️  IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic")
    print("   e irá consumir tokens. Custo estimado: ~$0.005-0.01\n")

    input("Pressione ENTER para continuar ou Ctrl+C para cancelar...")

    try:
        # Executar testes
        test_vague_observation_tech()
        test_vague_observation_education()
        test_very_vague_observation()
        test_output_structure()

        # Resumo final
        print_separator("VALIDAÇÃO CONCLUÍDA")
        print("✅ Todos os testes de validação manual foram executados com sucesso!")
        print("\nResumo dos componentes testados:")
        print("  ✅ structurer_node: Estruturação de 3 tipos de inputs vagas")
        print("  ✅ Extração de elementos: contexto, problema, contribuição")
        print("  ✅ Geração de questões estruturadas")
        print("  ✅ Comportamento colaborativo (não rejeita)")
        print("  ✅ Estrutura consistente do output")
        print("\nPróximos passos:")
        print("  1. Execute os testes unitários: pytest tests/unit/test_structurer.py -v")
        print("  2. Prossiga para a funcionalidade 3.3 (Super-grafo Multi-Agente)")
        print("  3. Integre Estruturador com Orquestrador e Metodologista")

    except KeyboardInterrupt:
        print("\n\n⚠️  Validação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRO durante validação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
