"""
Teste de integração para restauração de contexto ao alternar conversas (Épico 14.5).

Valida que ao alternar entre conversas (thread_ids), o histórico de mensagens
é restaurado corretamente do SqliteSaver.

Bug identificado:
- Função _switch_idea() em sidebar.py limpa mensagens mas não restaura do SqliteSaver
- Resultado: chat fica branco após alternar conversa

Solução:
- Restaurar mensagens do estado do LangGraph (graph.get_state(config))
- Converter mensagens do formato LangChain para formato Streamlit

Status: Épico 14.5 - Bugfix Crítico
"""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente do .env
load_dotenv()

from core.agents.multi_agent_graph import create_multi_agent_graph
from core.agents.orchestrator.state import create_initial_multi_agent_state
from langchain_core.messages import HumanMessage, AIMessage

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

requires_anthropic = pytest.mark.skipif(
    not ANTHROPIC_API_KEY,
    reason="Integration test skipped: ANTHROPIC_API_KEY not set (requires real API)",
)

# Todos os testes deste módulo são de integração que usam API real
pytestmark = [pytest.mark.integration, requires_anthropic]

def test_conversation_switching_restores_messages(multi_agent_graph):
    """
    Testa que alternar entre conversas restaura histórico de mensagens corretamente.

    Fluxo:
    1. Criar conversa A (thread_id_a) com 2 mensagens
    2. Criar conversa B (thread_id_b) com 1 mensagem
    3. "Alternar" de volta para conversa A
    4. Validar que histórico de A foi restaurado (2 mensagens)

    Valida:
    - graph.get_state() retorna mensagens corretas do SqliteSaver
    - Mensagens podem ser convertidas para formato Streamlit
    - Histórico completo é preservado (user + assistant)
    """
    # === ARRANGE ===
    thread_id_a = "test-conversation-a"
    thread_id_b = "test-conversation-b"

    # Conversa A: 2 turnos (2 user + 2 assistant = 4 mensagens)
    user_input_a1 = "Observei que TDD reduz bugs"
    user_input_a2 = "Como posso medir isso?"

    # Conversa B: 1 turno (1 user + 1 assistant = 2 mensagens)
    user_input_b1 = "Drones podem monitorar obras?"

    # === ACT 1: Criar conversa A com 2 turnos ===

    # Turno 1 de A
    state_a1 = create_initial_multi_agent_state(
        user_input=user_input_a1,
        session_id=thread_id_a
    )
    result_a1 = multi_agent_graph.invoke(
        state_a1,
        config={"configurable": {"thread_id": thread_id_a}}
    )

    # Turno 2 de A (continuação da conversa)
    state_a2 = create_initial_multi_agent_state(
        user_input=user_input_a2,
        session_id=thread_id_a
    )
    result_a2 = multi_agent_graph.invoke(
        state_a2,
        config={"configurable": {"thread_id": thread_id_a}}
    )

    # === ACT 2: Criar conversa B com 1 turno ===

    state_b1 = create_initial_multi_agent_state(
        user_input=user_input_b1,
        session_id=thread_id_b
    )
    result_b1 = multi_agent_graph.invoke(
        state_b1,
        config={"configurable": {"thread_id": thread_id_b}}
    )

    # === ACT 3: "Alternar" de volta para conversa A ===

    # Simular o que _switch_conversation() deve fazer:
    # Carregar estado da conversa A do SqliteSaver
    config_a = {"configurable": {"thread_id": thread_id_a}}
    restored_state_a = multi_agent_graph.get_state(config_a)

    # === ASSERT ===

    # 1. Estado deve existir
    assert restored_state_a is not None, "Estado restaurado não deveria ser None"

    # 2. Estado deve ter mensagens
    assert "messages" in restored_state_a.values, "Estado restaurado deveria ter campo 'messages'"

    messages_a = restored_state_a.values["messages"]

    # 3. Deve ter exatamente 4 mensagens (2 user + 2 assistant)
    # Nota: Dependendo de como o grafo funciona, pode ter mais mensagens internas
    # Vamos validar pelo menos 4 mensagens (2 turnos completos)
    assert len(messages_a) >= 4, \
        f"Conversa A deveria ter pelo menos 4 mensagens (2 turnos), mas tem {len(messages_a)}"

    # 4. Buscar mensagens do usuário (HumanMessage)
    # Nota: LangGraph pode ter outras mensagens (SystemMessage, etc) no array
    # então não podemos assumir que messages[0] é HumanMessage
    user_messages = [m for m in messages_a if isinstance(m, HumanMessage)]
    assert len(user_messages) >= 2, \
        f"Deveria ter pelo menos 2 mensagens do usuário, mas tem {len(user_messages)}"

    # 5. Validar que primeira mensagem do usuário contém o primeiro input
    first_user_msg = user_messages[0]
    assert user_input_a1 in first_user_msg.content, \
        f"Primeira mensagem do usuário deveria conter '{user_input_a1}', mas contém: {first_user_msg.content[:100]}"

    # 6. Validar que segunda mensagem do usuário também está presente
    second_user_msg = user_messages[1]
    assert user_input_a2 in second_user_msg.content, \
        f"Segunda mensagem do usuário deveria conter '{user_input_a2}', mas contém: {second_user_msg.content[:100]}"

    # 7. Validar que conversa B tem mensagens diferentes
    config_b = {"configurable": {"thread_id": thread_id_b}}
    restored_state_b = multi_agent_graph.get_state(config_b)

    messages_b = restored_state_b.values["messages"]
    user_messages_b = [m for m in messages_b if isinstance(m, HumanMessage)]

    assert len(user_messages_b) >= 1, "Conversa B deveria ter pelo menos 1 mensagem do usuário"
    assert user_input_b1 in user_messages_b[0].content, \
        "Primeira mensagem de B deveria ser diferente de A"

def test_convert_messages_to_streamlit_format(multi_agent_graph):
    """
    Testa conversão de mensagens do LangGraph para formato do Streamlit.

    Formato LangGraph:
        messages = [
            HumanMessage(content="..."),
            AIMessage(content="..."),
            ...
        ]

    Formato Streamlit esperado:
        messages = [
            {"role": "user", "content": "...", "tokens": None, "cost": None, "duration": None},
            {"role": "assistant", "content": "...", "tokens": None, "cost": None, "duration": None},
            ...
        ]

    Valida:
    - HumanMessage → role="user"
    - AIMessage → role="assistant"
    - Conteúdo preservado
    """
    # === ARRANGE ===
    thread_id = "test-conversion"
    user_input = "Teste de conversão de mensagens"

    # Criar conversa com 1 turno
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id=thread_id
    )
    result = multi_agent_graph.invoke(
        state,
        config={"configurable": {"thread_id": thread_id}}
    )

    # Carregar estado
    config = {"configurable": {"thread_id": thread_id}}
    restored_state = multi_agent_graph.get_state(config)
    messages = restored_state.values["messages"]

    # === ACT: Converter para formato Streamlit ===

    streamlit_messages = []
    for msg in messages:
        # Determinar role baseado no tipo
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            # Ignorar outros tipos (SystemMessage, etc)
            continue

        streamlit_messages.append({
            "role": role,
            "content": msg.content,
            "tokens": None,
            "cost": None,
            "duration": None,
            "timestamp": None
        })

    # === ASSERT ===

    # 1. Deve ter pelo menos 2 mensagens (1 user + 1 assistant)
    assert len(streamlit_messages) >= 2, \
        f"Deveria ter pelo menos 2 mensagens convertidas, mas tem {len(streamlit_messages)}"

    # 2. Buscar mensagens do usuário e do assistant
    # Nota: Ordem pode variar, não podemos assumir que messages[0] é user
    user_messages = [m for m in streamlit_messages if m["role"] == "user"]
    assistant_messages = [m for m in streamlit_messages if m["role"] == "assistant"]

    assert len(user_messages) >= 1, \
        "Deveria ter pelo menos 1 mensagem do usuário"

    assert len(assistant_messages) >= 1, \
        "Deveria ter pelo menos 1 mensagem do assistant"

    # 3. Conteúdo da primeira mensagem do usuário deve bater
    first_user_msg = user_messages[0]
    assert user_input in first_user_msg["content"], \
        f"Conteúdo da primeira mensagem do usuário deveria conter '{user_input}'"

    # 4. Mensagem do assistant deve ter conteúdo não vazio
    assert assistant_messages[0]["content"], \
        "Mensagem do assistant não deveria estar vazia"

    # 5. Validar estrutura dos dicts
    for msg in streamlit_messages:
        assert "role" in msg, "Mensagem deveria ter campo 'role'"
        assert "content" in msg, "Mensagem deveria ter campo 'content'"
        assert "tokens" in msg, "Mensagem deveria ter campo 'tokens'"
        assert "cost" in msg, "Mensagem deveria ter campo 'cost'"
        assert "duration" in msg, "Mensagem deveria ter campo 'duration'"
        assert msg["role"] in ["user", "assistant"], \
            f"Role deveria ser 'user' ou 'assistant', não '{msg['role']}'"

def test_empty_conversation_switching(multi_agent_graph):
    """
    Testa restauração de conversa que não existe ainda (thread_id novo).

    Valida:
    - get_state() de thread_id inexistente não causa erro
    - Retorna estado vazio ou inicial
    - Aplicação deve lidar graciosamente com conversas vazias
    """
    # === ARRANGE ===
    thread_id_novo = "test-nonexistent-conversation"

    # === ACT ===
    config = {"configurable": {"thread_id": thread_id_novo}}
    restored_state = multi_agent_graph.get_state(config)

    # === ASSERT ===

    # 1. Estado não deve ser None (LangGraph retorna estado vazio)
    assert restored_state is not None, \
        "get_state() não deveria retornar None para thread_id inexistente"

    # 2. Se houver mensagens, devem estar vazias ou ser lista vazia
    messages = restored_state.values.get("messages", [])
    assert isinstance(messages, list), \
        "Campo 'messages' deveria ser uma lista"

    # 3. Lista deve estar vazia (conversa nova)
    assert len(messages) == 0, \
        f"Conversa nova não deveria ter mensagens, mas tem {len(messages)}"
