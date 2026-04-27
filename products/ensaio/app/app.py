"""Entrypoint Reflex do produto Ensaio (E-PROTO-1.2).

Layout em duas colunas: chat à esquerda (60%), painel do artigo à direita (40%).
Sessão descartável — recarregar zera tudo (persistência fica para MVP-ENSAIO).

Executar (a partir de products/ensaio/):
    reflex run
"""

from __future__ import annotations

import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no path ao importar diretamente.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

import reflex as rx  # noqa: E402

from products.ensaio.app.components.article_panel import article_panel  # noqa: E402
from products.ensaio.app.components.chat_panel import chat_panel  # noqa: E402
from products.ensaio.app.state import EnsaioState  # noqa: E402


def index() -> rx.Component:
    return rx.box(
        rx.hstack(
            chat_panel(),
            article_panel(),
            spacing="0",
            width="100%",
            align="stretch",
        ),
        width="100vw",
        height="100vh",
        overflow="hidden",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="blue"),
)
app.add_page(index, on_load=EnsaioState.initialize, route="/")
