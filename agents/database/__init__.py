"""
Módulo de persistência para entidades do domínio.

Este módulo contém:
- Schema SQL das tabelas (ideas, arguments)
- DatabaseManager para operações CRUD (orquestrador)
- IdeasCRUD e ArgumentsCRUD para operações especializadas
- Helpers para versionamento e snapshots

Épico 11.2: Setup de Persistência e Schema SQLite
Data: 2025-11-17
Refatoração: Divisão em CRUD separados (ideas_crud.py, arguments_crud.py)
"""

from .manager import DatabaseManager, get_database_manager
from .schema import SCHEMA_SQL, DATABASE_VERSION
from .ideas_crud import IdeasCRUD
from .arguments_crud import ArgumentsCRUD

__all__ = [
    "DatabaseManager",
    "get_database_manager",
    "SCHEMA_SQL",
    "DATABASE_VERSION",
    "IdeasCRUD",
    "ArgumentsCRUD",
]
