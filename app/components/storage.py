"""
Componente de persistência localStorage para sessões (Épico 9.9).

Implementa armazenamento no navegador para:
- Histórico de mensagens por sessão
- Metadados de sessões (título, data, etc)
- Timeline de eventos (reasoning dos agentes)

Características:
- Persistência: Sessões sobrevivem reload da página
- Limitação: Armazenamento por device/navegador (não compartilhado)
- Implementação: JavaScript via st.components.v1.html (~20 linhas)
- Migração: Será substituído por SqliteSaver no MVP (9.10)

Versão: 1.0
Data: 16/11/2025
Status: Funcional (Épico 9.9 - Protótipo)
"""

import json
import streamlit.components.v1 as components
from typing import Any, Optional, Dict, List
from datetime import datetime


# === FUNÇÕES PÚBLICAS ===

def save_to_localstorage(key: str, data: Any) -> None:
    """
    Salva dados no localStorage do navegador.

    Args:
        key: Chave para identificar os dados (ex: "session_abc123")
        data: Dados a salvar (será convertido para JSON)

    Exemplos:
        >>> save_to_localstorage("session_123", {"messages": [...]})
        >>> save_to_localstorage("sessions_list", ["id1", "id2", "id3"])

    Nota:
        - Dados são serializados para JSON automaticamente
        - Limite de ~5-10MB por domínio (varia por navegador)
        - Dados persistem até serem manualmente deletados
    """
    # Serializar dados para JSON
    json_data = json.dumps(data, ensure_ascii=False, default=str)

    # JavaScript para salvar no localStorage
    js_code = f"""
    <script>
        try {{
            localStorage.setItem('{key}', {json.dumps(json_data)});
            console.log('LocalStorage: Saved key "{key}"');
        }} catch (e) {{
            console.error('LocalStorage: Error saving key "{key}":', e);
        }}
    </script>
    """

    # Renderizar (altura 0 = invisível)
    components.html(js_code, height=0)


def load_from_localstorage(key: str, default: Any = None) -> Any:
    """
    Carrega dados do localStorage do navegador.

    Args:
        key: Chave dos dados a carregar
        default: Valor padrão se chave não existir

    Returns:
        Dados deserializados ou valor padrão

    Exemplos:
        >>> messages = load_from_localstorage("session_123", default=[])
        >>> sessions = load_from_localstorage("sessions_list", default=[])

    Nota:
        - Esta função usa comunicação bidirecional com JavaScript
        - Streamlit pode reexecutar múltiplas vezes durante render
        - Considere cachear resultado em st.session_state
    """
    # JavaScript para carregar do localStorage
    js_code = f"""
    <script>
        try {{
            const data = localStorage.getItem('{key}');
            if (data !== null) {{
                // Enviar dados de volta para Streamlit
                const parsedData = JSON.parse(data);
                window.parent.postMessage({{
                    type: 'localStorage',
                    key: '{key}',
                    value: parsedData
                }}, '*');
                console.log('LocalStorage: Loaded key "{key}"');
            }} else {{
                console.log('LocalStorage: Key "{key}" not found');
                window.parent.postMessage({{
                    type: 'localStorage',
                    key: '{key}',
                    value: null
                }}, '*');
            }}
        }} catch (e) {{
            console.error('LocalStorage: Error loading key "{key}":', e);
            window.parent.postMessage({{
                type: 'localStorage',
                key: '{key}',
                value: null
            }}, '*');
        }}
    </script>
    """

    # Renderizar e capturar resposta
    result = components.html(js_code, height=0)

    # Se não recebeu dados, retornar default
    if result is None:
        return default

    # Parse JSON se for string
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return default

    return result if result is not None else default


def remove_from_localstorage(key: str) -> None:
    """
    Remove dados do localStorage.

    Args:
        key: Chave a remover

    Exemplo:
        >>> remove_from_localstorage("session_old_id")
    """
    js_code = f"""
    <script>
        try {{
            localStorage.removeItem('{key}');
            console.log('LocalStorage: Removed key "{key}"');
        }} catch (e) {{
            console.error('LocalStorage: Error removing key "{key}":', e);
        }}
    </script>
    """

    components.html(js_code, height=0)


def clear_all_localstorage() -> None:
    """
    Limpa TODOS os dados do localStorage (use com cuidado!).

    Útil para:
        - Desenvolvimento/debug (resetar estado)
        - Botão "Limpar todos os dados" na interface
    """
    js_code = """
    <script>
        try {
            localStorage.clear();
            console.log('LocalStorage: Cleared all data');
        } catch (e) {
            console.error('LocalStorage: Error clearing data:', e);
        }
    </script>
    """

    components.html(js_code, height=0)


# === FUNÇÕES AUXILIARES ===

def save_session_messages(session_id: str, messages: List[Dict[str, Any]]) -> None:
    """
    Salva histórico de mensagens de uma sessão.

    Args:
        session_id: ID da sessão
        messages: Lista de mensagens (formato chat_history)

    Exemplo:
        >>> messages = [
        ...     {"role": "user", "content": "Hello", "tokens": {...}},
        ...     {"role": "assistant", "content": "Hi!", "tokens": {...}}
        ... ]
        >>> save_session_messages("session_123", messages)
    """
    key = f"messages_{session_id}"
    save_to_localstorage(key, messages)


def load_session_messages(session_id: str) -> List[Dict[str, Any]]:
    """
    Carrega histórico de mensagens de uma sessão.

    Args:
        session_id: ID da sessão

    Returns:
        Lista de mensagens ou lista vazia se não existir

    Exemplo:
        >>> messages = load_session_messages("session_123")
        >>> print(len(messages))
        5
    """
    key = f"messages_{session_id}"
    return load_from_localstorage(key, default=[])


def save_session_metadata(session_id: str, metadata: Dict[str, Any]) -> None:
    """
    Salva metadados de uma sessão.

    Args:
        session_id: ID da sessão
        metadata: {
            "title": str,
            "created_at": str (ISO),
            "last_activity": str (ISO),
            "message_count": int,
            ...
        }

    Exemplo:
        >>> metadata = {
        ...     "title": "Discussão sobre TDD",
        ...     "created_at": "2025-11-16T10:00:00Z",
        ...     "last_activity": "2025-11-16T10:30:00Z",
        ...     "message_count": 10
        ... }
        >>> save_session_metadata("session_123", metadata)
    """
    key = f"metadata_{session_id}"
    save_to_localstorage(key, metadata)


def load_session_metadata(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Carrega metadados de uma sessão.

    Args:
        session_id: ID da sessão

    Returns:
        Metadados ou None se não existir
    """
    key = f"metadata_{session_id}"
    return load_from_localstorage(key, default=None)


def list_all_sessions() -> List[str]:
    """
    Lista IDs de todas as sessões armazenadas.

    Returns:
        Lista de session_ids

    Exemplo:
        >>> sessions = list_all_sessions()
        >>> print(sessions)
        ['session_123', 'session_456', 'session_789']

    Nota:
        Esta função retorna lista mantida em "sessions_list" no localStorage.
        Lembre-se de atualizar esta lista ao criar/deletar sessões.
    """
    return load_from_localstorage("sessions_list", default=[])


def add_session_to_list(session_id: str) -> None:
    """
    Adiciona sessão à lista de sessões armazenadas.

    Args:
        session_id: ID da sessão a adicionar

    Nota:
        Evita duplicatas automaticamente
    """
    sessions = list_all_sessions()

    if session_id not in sessions:
        sessions.append(session_id)
        save_to_localstorage("sessions_list", sessions)


def remove_session_from_list(session_id: str) -> None:
    """
    Remove sessão da lista e seus dados associados.

    Args:
        session_id: ID da sessão a remover

    Remove:
        - Sessão da lista principal
        - Histórico de mensagens
        - Metadados
        - Timeline de eventos (se existir)
    """
    # Remover da lista
    sessions = list_all_sessions()
    if session_id in sessions:
        sessions.remove(session_id)
        save_to_localstorage("sessions_list", sessions)

    # Remover dados associados
    remove_from_localstorage(f"messages_{session_id}")
    remove_from_localstorage(f"metadata_{session_id}")
    remove_from_localstorage(f"timeline_{session_id}")


