"""Configuração do Reflex para a plataforma de workflow (W-PILOTO-UX-1).

Espelha ``products/ensaio/rxconfig.py``. Portas distintas das do Ensaio
(3000/8000) para as duas apps Reflex coexistirem em dev.

Executar (a partir de ``tools/workflow_platform/``):
    reflex run
"""

import sys
from pathlib import Path

# Garante o repo root no Python path ao iniciar o Reflex.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import reflex as rx  # noqa: E402

config = rx.Config(
    app_name="web",
    backend_port=8001,
    frontend_port=3001,
)
