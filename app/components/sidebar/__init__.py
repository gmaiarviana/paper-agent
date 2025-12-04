"""
Módulo sidebar para navegação de conversas (Épico 14.1).

Responsável por:
- Listar conversas recentes (últimas 5 - reduzido de 10)
- Destacar conversa ativa
- Botão "+ Nova Conversa"
- Alternar entre conversas (restaura contexto completo - Épico 14.5)
- Botões de navegação para páginas dedicadas:
  - [📖 Meus Pensamentos] → /pensamentos
  - [🏷️ Catálogo] → /catalogo (desabilitado até Épico 13)

Versão: 4.0
Data: 19/11/2025
Status: Épico 14.1 - Navegação em Três Espaços
"""

from app.components.sidebar.navigation import render_sidebar

__all__ = ["render_sidebar"]

