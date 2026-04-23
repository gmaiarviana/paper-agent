"""Painel do artigo do Ensaio (E-POC-1.5).

Renderiza o markdown do artigo gerado (quando existe) na coluna direita do
layout 60/40. Mantém o artigo anterior visível até que o pesquisador peça
regeneração — não renderiza placeholders de "em construção" fora dessa
semântica.
"""

from __future__ import annotations

import streamlit as st


def render_article_panel() -> None:
    """Exibe o artigo atual em ``st.session_state.current_article``.

    Quando ``current_article`` é ``None``, mostra um placeholder discreto
    (texto, sem skeleton animado) convidando à geração. Quando existe,
    renderiza o markdown completo.
    """
    st.subheader("📄 Artigo")

    current_article = st.session_state.get("current_article")

    if not current_article:
        st.caption(
            "O artigo aparece aqui quando você clicar em **Gerar artigo**. "
            "Você pode pedir ajustes em linguagem natural no chat e regenerar "
            "a qualquer momento."
        )
        return

    st.markdown(current_article)
