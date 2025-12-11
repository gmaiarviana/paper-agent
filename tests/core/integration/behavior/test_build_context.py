"""
Script de validação manual para _build_context().

Este script valida a implementação da função helper _build_context()
implementada no Épico 7, Tarefa 7.1.3.

A função reconstrói o "argumento focal" implícito da conversa analisando
todo o histórico de mensagens (user_input + messages).

IMPORTANTE: Este script NÃO faz chamadas à API (testes locais, sem custo).

Uso:
    python scripts/flows/validate_build_context.py

Valida que _build_context():
1. Constrói contexto com apenas input inicial (sem histórico)
2. Inclui mensagens do usuário (HumanMessage)
3. Inclui mensagens do assistente (AIMessage)
4. Preserva ordem cronológica das mensagens
5. Formato é adequado para análise pelo LLM
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from langchain_core.messages import HumanMessage, AIMessage
from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.orchestrator.nodes import _build_context

def print_separator(title=""):
    """Imprime separador visual."""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'-'*80}\n")

def test_build_context_only_initial_input():
    """Testa construção de contexto com apenas input inicial (sem histórico)."""
    print_separator("TESTE 1: CONTEXTO COM APENAS INPUT INICIAL")

    # Arrange
    state = create_initial_multi_agent_state(
        user_input="Observei que LLMs aumentam produtividade",
        session_id="session-123"
    )

    # Act
    context = _build_context(state)

    # Assert
    print("Contexto construído:")
    print(context)
    print()

    assert "INPUT INICIAL DO USUÁRIO:" in context, "❌ Faltou seção de input inicial"
    assert "Observei que LLMs aumentam produtividade" in context, "❌ Faltou o input do usuário"
    assert "HISTÓRICO DA CONVERSA:" not in context, "❌ Não deveria ter histórico (sem mensagens)"

    print("✅ TESTE 1 PASSOU: Contexto construído corretamente com apenas input inicial")

def test_build_context_with_human_messages():
    """Testa construção de contexto com mensagens do usuário."""
    print_separator("TESTE 2: CONTEXTO COM MENSAGENS DO USUÁRIO")

    # Arrange
    state = create_initial_multi_agent_state(
        user_input="Observei que LLMs aumentam produtividade",
        session_id="session-123"
    )
    state['messages'] = [
        HumanMessage(content="Na minha equipe, usando Claude Code"),
        HumanMessage(content="Tarefas que levavam 2h agora levam 30min")
    ]

    # Act
    context = _build_context(state)

    # Assert
    print("Contexto construído:")
    print(context)
    print()

    assert "HISTÓRICO DA CONVERSA:" in context, "❌ Faltou seção de histórico"
    assert "[Usuário]: Na minha equipe, usando Claude Code" in context, "❌ Faltou mensagem 1"
    assert "[Usuário]: Tarefas que levavam 2h agora levam 30min" in context, "❌ Faltou mensagem 2"

    print("✅ TESTE 2 PASSOU: Mensagens do usuário incluídas corretamente")

def test_build_context_with_ai_messages():
    """Testa construção de contexto com mensagens do assistente."""
    print_separator("TESTE 3: CONTEXTO COM MENSAGENS DO ASSISTENTE")

    # Arrange
    state = create_initial_multi_agent_state(
        user_input="Observei que LLMs aumentam produtividade",
        session_id="session-123"
    )
    state['messages'] = [
        AIMessage(content="Interessante! Me conta mais sobre isso."),
        AIMessage(content="Você mediu isso de alguma forma?")
    ]

    # Act
    context = _build_context(state)

    # Assert
    print("Contexto construído:")
    print(context)
    print()

    assert "HISTÓRICO DA CONVERSA:" in context, "❌ Faltou seção de histórico"
    assert "[Assistente]: Interessante! Me conta mais sobre isso." in context, "❌ Faltou mensagem do AI 1"
    assert "[Assistente]: Você mediu isso de alguma forma?" in context, "❌ Faltou mensagem do AI 2"

    print("✅ TESTE 3 PASSOU: Mensagens do assistente incluídas corretamente")

def test_build_context_with_mixed_messages():
    """Testa construção de contexto com mix de mensagens (usuário + assistente)."""
    print_separator("TESTE 4: CONTEXTO COM MENSAGENS MISTAS")

    # Arrange
    state = create_initial_multi_agent_state(
        user_input="Observei que LLMs aumentam produtividade",
        session_id="session-123"
    )
    state['messages'] = [
        AIMessage(content="Interessante! Me conta mais."),
        HumanMessage(content="Vi na minha equipe, usando Claude Code"),
        AIMessage(content="Você mediu isso?"),
        HumanMessage(content="Tarefas que levavam 2h agora levam 30min")
    ]

    # Act
    context = _build_context(state)

    # Assert
    print("Contexto construído:")
    print(context)
    print()

    assert "[Assistente]: Interessante! Me conta mais." in context, "❌ Faltou AI msg 1"
    assert "[Usuário]: Vi na minha equipe, usando Claude Code" in context, "❌ Faltou Human msg 1"
    assert "[Assistente]: Você mediu isso?" in context, "❌ Faltou AI msg 2"
    assert "[Usuário]: Tarefas que levavam 2h agora levam 30min" in context, "❌ Faltou Human msg 2"

    print("✅ TESTE 4 PASSOU: Mensagens mistas incluídas corretamente")

def test_build_context_preserves_chronological_order():
    """Testa que contexto preserva ordem cronológica das mensagens."""
    print_separator("TESTE 5: ORDEM CRONOLÓGICA PRESERVADA")

    # Arrange
    state = create_initial_multi_agent_state(
        user_input="Input inicial",
        session_id="session-123"
    )
    state['messages'] = [
        HumanMessage(content="Mensagem 1"),
        AIMessage(content="Resposta 1"),
        HumanMessage(content="Mensagem 2"),
        AIMessage(content="Resposta 2")
    ]

    # Act
    context = _build_context(state)
    lines = context.split("\n")

    # Assert
    print("Contexto construído:")
    print(context)
    print()

    # Encontrar índices das mensagens
    msg1_idx = next(i for i, line in enumerate(lines) if "Mensagem 1" in line)
    resp1_idx = next(i for i, line in enumerate(lines) if "Resposta 1" in line)
    msg2_idx = next(i for i, line in enumerate(lines) if "Mensagem 2" in line)
    resp2_idx = next(i for i, line in enumerate(lines) if "Resposta 2" in line)

    print(f"Índices das mensagens: {msg1_idx} < {resp1_idx} < {msg2_idx} < {resp2_idx}")

    assert msg1_idx < resp1_idx < msg2_idx < resp2_idx, "❌ Ordem cronológica não preservada"

    print("✅ TESTE 5 PASSOU: Ordem cronológica preservada corretamente")

def test_build_context_detects_change_in_direction():
    """
    Testa que contexto construído permite detecção de mudança de direção.

    Este teste valida que o histórico completo é preservado,
    permitindo ao LLM detectar contradições ou mudanças de foco.
    """
    print_separator("TESTE 6: DETECÇÃO DE MUDANÇA DE DIREÇÃO")

    # Arrange
    state = create_initial_multi_agent_state(
        user_input="Quero estudar impacto de LLMs em produtividade",
        session_id="session-123"
    )
    state['messages'] = [
        AIMessage(content="Vamos explorar produtividade então"),
        HumanMessage(content="Na verdade, quero focar em qualidade de código")
    ]

    # Act
    context = _build_context(state)

    # Assert
    print("Contexto construído:")
    print(context)
    print()

    assert "produtividade" in context, "❌ Faltou menção a 'produtividade'"
    assert "qualidade de código" in context, "❌ Faltou menção a 'qualidade de código'"

    print("✅ TESTE 6 PASSOU: Ambas direções presentes (LLM pode detectar mudança)")

def validate_build_context():
    """Executa todos os testes de validação."""
    print_separator("VALIDAÇÃO DE _build_context() - Épico 7, Tarefa 7.1.3")

    print("""
Esta validação testa a função helper _build_context() que:
- Reconstrói o "argumento focal" implícito da conversa
- Analisa todo o histórico de mensagens (user_input + messages)
- Formata contexto para análise contextual pelo LLM

IMPORTANTE: Testes locais (sem chamadas à API, sem custo)
""")

    try:
        # Executar todos os testes
        test_build_context_only_initial_input()
        test_build_context_with_human_messages()
        test_build_context_with_ai_messages()
        test_build_context_with_mixed_messages()
        test_build_context_preserves_chronological_order()
        test_build_context_detects_change_in_direction()

        # Resumo final
        print_separator("RESULTADO FINAL")
        print("✅ TODOS OS TESTES PASSARAM!")
        print()
        print("A função _build_context() foi implementada corretamente e está pronta para uso.")
        print()
        print("Próximos passos:")
        print("  1. Implementar ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1 (Tarefa 7.1.1)")
        print("  2. Substituir orchestrator_node atual (Tarefa 7.1.2)")
        print("  3. Adicionar parsing de JSON response (Tarefa 7.1.4)")
        print()

    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    validate_build_context()
