"""Configuração do Reflex para o produto Ensaio (E-PROTO-1.2)."""

import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no Python path ao iniciar o Reflex.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import reflex as rx  # noqa: E402

config = rx.Config(
    app_name="app",
    backend_port=8000,
    frontend_port=3000,
)
