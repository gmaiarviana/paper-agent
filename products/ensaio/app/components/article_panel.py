"""
Painel do artigo do Ensaio (E-POC-1.5).

Renderiza o markdown gerado pelo Writer em `st.session_state.current_article`.
Quando não há artigo ainda, mostra um placeholder curto convidando à geração.
"""

from __future__ import annotations

import streamlit as st


def render_article_panel() -> None:
    """Renderiza o artigo atual na coluna direita."""
    st.markdown("### Artigo")

    article = st.session_state.get("current_article")
    if article:
        st.markdown(article)
    else:
        st.info(
            "Nenhum artigo gerado ainda. "
            'Converse sobre o experimento e clique em "Gerar artigo" quando quiser '
            "ver um primeiro rascunho."
        )
