"""
Teste unitário simples para validar que HumanMessage está sendo adicionada ao estado inicial.

Este teste não requer ANTHROPIC_API_KEY.

"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.agents.orchestrator.state import create_initial_multi_agent_state
from langchain_core.messages import HumanMessage

def test_initial_state_includes_human_message():
    """
    Testa que create_initial_multi_agent_state adiciona HumanMessage ao campo messages.

    Bugfix: Anteriormente, messages=[] estava vazio, causando falha na restauração
    de contexto porque SqliteSaver não persistia mensagens do usuário.

    Validação:
    - Estado inicial deve ter 1 mensagem
    - Mensagem deve ser HumanMessage
    - Conteúdo deve bater com user_input
    """
    user_input = "Teste de mensagem inicial"
    state = create_initial_multi_agent_state(user_input=user_input, session_id="test-123")

    # Verificar que messages não está vazio
    assert len(state["messages"]) > 0, \
        "Estado inicial deveria ter pelo menos 1 mensagem"

    # Verificar que primeira mensagem é HumanMessage
    first_msg = state["messages"][0]
    assert isinstance(first_msg, HumanMessage), \
        f"Primeira mensagem deveria ser HumanMessage, mas é {type(first_msg)}"

    # Verificar que conteúdo bate
    assert first_msg.content == user_input, \
        f"Conteúdo da mensagem deveria ser '{user_input}', mas é '{first_msg.content}'"

    print("✅ Teste passou! HumanMessage está sendo adicionada corretamente ao estado inicial.")

if __name__ == "__main__":
    try:
        test_initial_state_includes_human_message()
    except AssertionError as e:
        print(f"❌ Teste falhou: {e}")
        sys.exit(1)
