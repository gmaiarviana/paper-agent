"""
Módulo sidebar para navegação (Épico 2.1).

Responsável por:
- Renderizar sidebar minimalista com links de navegação
- Botão "+ Nova conversa"
- Links para páginas dedicadas:
  - 📖 Pensamentos → /pensamentos
  - 🏷️ Catálogo → /catalogo (desabilitado)
  - 💬 Conversas → /historico

Status: Épico 2.1 - Sidebar com Links de Navegação
"""

from products.revelar.app.components.sidebar.navigation import render_sidebar

__all__ = ["render_sidebar"]
