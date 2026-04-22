"""
Componentes específicos do app do Ensaio.

- chat_input: form Streamlit que envia mensagens ao grafo do Ensaio
- article_panel: renderiza o artigo markdown na coluna direita
- generate_button: botão "Gerar artigo" / "Regenerar" que invoca o Writer diretamente
"""

from products.ensaio.app.components.chat_input import render_chat_input
from products.ensaio.app.components.article_panel import render_article_panel
from products.ensaio.app.components.generate_button import render_generate_button

__all__ = [
    "render_chat_input",
    "render_article_panel",
    "render_generate_button",
]
