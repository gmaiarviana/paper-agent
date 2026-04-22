"""
Entrypoint Streamlit do Ensaio (E-POC-1.2).

Uso:
    streamlit run products/ensaio/app/chat.py

Layout (E-POC-1.2):
    ┌──────────────────────────┬──────────────────┐
    │ Conversa (3/5)          │ Artigo (2/5)     │
    │                          │ [Gerar/Regenerar]│
    │ histórico + input        │ markdown         │
    └──────────────────────────┴──────────────────┘

Estado (E-POC-1.6):
- Tudo vive em `st.session_state` - recarregar a página zera tudo.
- Checkpoints do LangGraph em `data/ensaio_checkpoints.db` persistem entre
  reloads mas são descartáveis (basta apagar o arquivo).
"""

from __future__ import annotations

import logging
import sys
import uuid
from pathlib import Path
from typing import Optional

# Garante que o project root está no PYTHONPATH quando rodado via `streamlit run`.
_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st  # noqa: E402
from langchain_core.messages import AIMessage, HumanMessage  # noqa: E402

from products.ensaio.app.components import (  # noqa: E402
    render_article_panel,
    render_chat_input,
    render_generate_button,
)
from products.ensaio.app.product_config import (  # noqa: E402
    ProductConfigError,
    load_product_context,
)

logger = logging.getLogger(__name__)


def _init_session_state() -> None:
    """Inicializa as chaves de estado usadas pelo Ensaio (E-POC-1.6)."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "focal_argument" not in st.session_state:
        st.session_state.focal_argument = None
    if "current_article" not in st.session_state:
        st.session_state.current_article = None
    if "generating" not in st.session_state:
        st.session_state.generating = False
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"ensaio-{uuid.uuid4()}"
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = st.session_state.session_id


def _load_product_context_safe() -> Optional[str]:
    """Carrega product_context com fallback amigável ao usuário (E-POC-2.4)."""
    try:
        return load_product_context()
    except ProductConfigError as exc:
        st.warning(
            "Falha ao carregar contexto do produto (products/ensaio/config/product.yaml). "
            f"Detalhe: {exc}. O chat continua funcionando, mas sem injeção de contexto."
        )
        return None


def _render_chat_history() -> None:
    """Renderiza o histórico de mensagens (mais simples que o do Revelar)."""
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="🧑"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg.content)


def main() -> None:
    st.set_page_config(
        page_title="Ensaio - Paper Agent",
        page_icon="📝",
        layout="wide",
    )
    _init_session_state()

    st.title("Ensaio")
    st.caption(
        "Converse sobre seu experimento e gere um artigo markdown em IMRaD quando quiser."
    )

    product_context = _load_product_context_safe()

    col_chat, col_article = st.columns([3, 2])

    with col_chat:
        st.markdown("### Conversa")
        _render_chat_history()
        render_chat_input(product_context=product_context)

    with col_article:
        render_generate_button(product_context=product_context)
        render_article_panel()


if __name__ == "__main__":
    main()
