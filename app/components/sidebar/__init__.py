"""
Módulo sidebar para navegação (Épico 2.1).

Responsável por:
- Renderizar sidebar minimalista com links de navegação
- Botão "+ Nova conversa"
- Links para páginas dedicadas:
  - 📖 Pensamentos → /pensamentos
  - 🏷️ Catálogo → /catalogo (desabilitado)
  - 💬 Conversas → /historico

Versão: 2.0
Data: 04/12/2025
Status: Épico 2.1 - Sidebar com Links de Navegação
"""

from app.components.sidebar.navigation import render_sidebar

__all__ = ["render_sidebar"]
