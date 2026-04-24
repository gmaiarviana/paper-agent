"""Entrypoint Streamlit do produto Ensaio (E-POC-1.2, 1.6, 3.5).

Layout 60/40: chat à esquerda, painel do artigo à direita. Todo o estado vive
em ``st.session_state`` — recarregar a página zera tudo (POC descartável por
design).

Executar:
    streamlit run products/ensaio/app/chat.py

Depende apenas de ``ANTHROPIC_API_KEY`` no ``.env``.
"""

from __future__ import annotations

import logging
import sys
import uuid
from pathlib import Path

import streamlit as st

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

from products.ensaio.app.components.article_panel import render_article_panel  # noqa: E402
from products.ensaio.app.components.chat_input import render_chat_input  # noqa: E402
from products.ensaio.app.components.generate_button import render_generate_button  # noqa: E402
from products.ensaio.app.product_config import (  # noqa: E402
    ProductConfigError,
    load_product_context,
)
from products.revelar.app.components.chat_history import render_chat_history  # noqa: E402

logger = logging.getLogger(__name__)


def _init_session_state() -> None:
    """Inicializa todas as chaves de session_state usadas pelo Ensaio (E-POC-1.6)."""
    defaults = {
        "messages": [],
        "langchain_history": [],
        "focal_argument": None,
        "current_article": None,
        "generating": False,
        "session_id": str(uuid.uuid4()),
        "thread_id": None,
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default
    if st.session_state.thread_id is None:
        st.session_state.thread_id = st.session_state.session_id


def main() -> None:
    st.set_page_config(
        page_title="Ensaio — Experimento vira artigo",
        page_icon="🧪",
        layout="wide",
    )

    _init_session_state()

    try:
        product_context = load_product_context()
    except ProductConfigError as exc:
        st.error(f"❌ Erro ao carregar product.yaml do Ensaio: {exc}")
        st.stop()
        return

    st.title("🧪 Ensaio")
    st.caption(
        "Laboratório de escrita: transforma seu experimento em artigo "
        "técnico-científico via conversa."
    )

    col_chat, col_article = st.columns([3, 2])

    with col_chat:
        st.subheader("💬 Conversa sobre o experimento")
        render_chat_history(st.session_state.session_id)
        render_chat_input(st.session_state.session_id, product_context)

    with col_article:
        render_generate_button(product_context)
        render_article_panel()


main()
