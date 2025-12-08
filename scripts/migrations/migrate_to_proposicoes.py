#!/usr/bin/env python3
"""
Script de Migração: premises/assumptions → proposicoes

Este script migra o banco de dados da versão 1.0.0 (premises/assumptions separados)
para a versão 2.0.0 (proposicoes unificadas).

Processo de migração:
1. Verifica versão atual do schema
2. Cria backup automático do banco
3. Adiciona coluna 'proposicoes' à tabela arguments
4. Para cada argumento:
   - Lê premises (list[str]) e assumptions (list[str])
   - Converte cada string para Proposicao com solidez=None
   - Combina em lista única de proposicoes
5. Remove colunas premises e assumptions
6. Atualiza versão do schema para 2.0.0
7. Recria views afetadas

Uso:
    python scripts/migrations/migrate_to_proposicoes.py [--dry-run] [--force]

Flags:
    --dry-run: Simula migração sem alterar banco
    --force: Força migração mesmo se versão já é 2.0.0

Épico 11.1: Schema Unificado (Camada Modelo)
Data: 2025-12-08
"""

import json
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

# Adiciona raiz do projeto ao path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.database.schema import DATABASE_VERSION

# Caminhos
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "data.db"
BACKUP_DIR = DATA_DIR / "backups"


def get_schema_version(conn: sqlite3.Connection) -> str | None:
    """Obtém versão atual do schema do banco."""
    try:
        cursor = conn.execute(
            "SELECT value FROM metadata WHERE key = 'schema_version' LIMIT 1"
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except sqlite3.OperationalError:
        # Tabela metadata não existe
        return None


def create_backup(db_path: Path) -> Path:
    """Cria backup do banco de dados."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"data_backup_{timestamp}.db"
    backup_path = BACKUP_DIR / backup_name

    shutil.copy2(db_path, backup_path)
    print(f"✅ Backup criado: {backup_path}")

    return backup_path


def convert_to_proposicoes(premises: list[str], assumptions: list[str]) -> list[dict]:
    """
    Converte premises e assumptions em lista de proposições.

    Cada proposição recebe:
    - id: UUID único
    - texto: conteúdo original (premise ou assumption)
    - solidez: None (não avaliada)
    - evidencias: [] (vazio)
    """
    proposicoes = []

    for texto in premises:
        if texto.strip():  # Ignora strings vazias
            proposicoes.append({
                "id": str(uuid4()),
                "texto": texto.strip(),
                "solidez": None,
                "evidencias": []
            })

    for texto in assumptions:
        if texto.strip():  # Ignora strings vazias
            proposicoes.append({
                "id": str(uuid4()),
                "texto": texto.strip(),
                "solidez": None,
                "evidencias": []
            })

    return proposicoes


def migrate_arguments(conn: sqlite3.Connection, dry_run: bool = False) -> int:
    """
    Migra argumentos de premises/assumptions para proposicoes.

    Returns:
        int: Número de argumentos migrados
    """
    # Verifica se colunas antigas existem
    cursor = conn.execute("PRAGMA table_info(arguments)")
    columns = {row[1] for row in cursor.fetchall()}

    has_old_columns = "premises" in columns and "assumptions" in columns
    has_new_column = "proposicoes" in columns

    if not has_old_columns and has_new_column:
        print("ℹ️  Banco já está no formato novo (proposicoes)")
        return 0

    if not has_old_columns and not has_new_column:
        print("❌ Erro: Banco em estado inconsistente")
        return -1

    # Lê todos os argumentos existentes
    cursor = conn.execute("""
        SELECT id, premises, assumptions
        FROM arguments
    """)
    arguments = cursor.fetchall()

    print(f"📊 Encontrados {len(arguments)} argumentos para migrar")

    if dry_run:
        print("\n🔍 [DRY-RUN] Simulando migração:")
        for arg_id, premises_json, assumptions_json in arguments:
            premises = json.loads(premises_json)
            assumptions = json.loads(assumptions_json)
            proposicoes = convert_to_proposicoes(premises, assumptions)
            print(f"   - {arg_id[:8]}...: {len(premises)} premises + {len(assumptions)} assumptions → {len(proposicoes)} proposições")
        return len(arguments)

    # Adiciona nova coluna se não existe
    if not has_new_column:
        print("➕ Adicionando coluna 'proposicoes'...")
        conn.execute("""
            ALTER TABLE arguments
            ADD COLUMN proposicoes TEXT NOT NULL DEFAULT '[]'
        """)

    # Migra cada argumento
    migrated_count = 0
    for arg_id, premises_json, assumptions_json in arguments:
        premises = json.loads(premises_json)
        assumptions = json.loads(assumptions_json)

        proposicoes = convert_to_proposicoes(premises, assumptions)
        proposicoes_json = json.dumps(proposicoes, ensure_ascii=False)

        conn.execute("""
            UPDATE arguments
            SET proposicoes = ?
            WHERE id = ?
        """, (proposicoes_json, arg_id))

        migrated_count += 1
        print(f"   ✅ {arg_id[:8]}...: {len(proposicoes)} proposições")

    return migrated_count


def remove_old_columns(conn: sqlite3.Connection, dry_run: bool = False) -> None:
    """
    Remove colunas premises e assumptions.

    SQLite não suporta DROP COLUMN diretamente (antes do 3.35.0),
    então recriamos a tabela sem as colunas.
    """
    if dry_run:
        print("\n🔍 [DRY-RUN] Removeria colunas: premises, assumptions")
        return

    print("\n🗑️  Removendo colunas antigas...")

    # SQLite 3.35.0+ suporta ALTER TABLE DROP COLUMN
    # Mas para compatibilidade, usamos método de recriação

    # 1. Cria tabela temporária com novo schema
    conn.execute("""
        CREATE TABLE arguments_new (
            id TEXT PRIMARY KEY,
            idea_id TEXT NOT NULL,
            claim TEXT NOT NULL,
            proposicoes TEXT NOT NULL DEFAULT '[]',
            open_questions TEXT NOT NULL DEFAULT '[]',
            contradictions TEXT NOT NULL DEFAULT '[]',
            solid_grounds TEXT NOT NULL DEFAULT '[]',
            context TEXT NOT NULL DEFAULT '{}',
            version INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idea_id) REFERENCES ideas(id) ON DELETE CASCADE,
            UNIQUE (idea_id, version)
        )
    """)

    # 2. Copia dados para nova tabela
    conn.execute("""
        INSERT INTO arguments_new
        SELECT id, idea_id, claim, proposicoes, open_questions,
               contradictions, solid_grounds, context, version,
               created_at, updated_at
        FROM arguments
    """)

    # 3. Remove tabela antiga
    conn.execute("DROP TABLE arguments")

    # 4. Renomeia nova tabela
    conn.execute("ALTER TABLE arguments_new RENAME TO arguments")

    # 5. Recria índices
    conn.execute("CREATE INDEX IF NOT EXISTS idx_arguments_idea_id ON arguments(idea_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_arguments_version ON arguments(idea_id, version DESC)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_arguments_created_at ON arguments(created_at DESC)")

    # 6. Recria trigger
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS update_arguments_timestamp
        AFTER UPDATE ON arguments
        FOR EACH ROW
        BEGIN
            UPDATE arguments SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END
    """)

    print("✅ Colunas antigas removidas")


def recreate_views(conn: sqlite3.Connection, dry_run: bool = False) -> None:
    """Recria views com novo schema."""
    if dry_run:
        print("\n🔍 [DRY-RUN] Recriaria views: ideas_with_current_argument")
        return

    print("\n🔄 Recriando views...")

    # Drop e recria view
    conn.execute("DROP VIEW IF EXISTS ideas_with_current_argument")
    conn.execute("""
        CREATE VIEW ideas_with_current_argument AS
        SELECT
            i.id as idea_id,
            i.title,
            i.status,
            i.created_at as idea_created_at,
            i.updated_at as idea_updated_at,
            a.id as argument_id,
            a.claim,
            a.proposicoes,
            a.open_questions,
            a.contradictions,
            a.solid_grounds,
            a.context,
            a.version,
            a.created_at as argument_created_at
        FROM ideas i
        LEFT JOIN arguments a ON i.current_argument_id = a.id
    """)

    print("✅ Views recriadas")


def update_schema_version(conn: sqlite3.Connection, version: str, dry_run: bool = False) -> None:
    """Atualiza versão do schema na tabela metadata."""
    if dry_run:
        print(f"\n🔍 [DRY-RUN] Atualizaria versão para: {version}")
        return

    # Garante que tabela metadata existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        INSERT OR REPLACE INTO metadata (key, value, updated_at)
        VALUES ('schema_version', ?, CURRENT_TIMESTAMP)
    """, (version,))

    print(f"✅ Versão do schema atualizada para: {version}")


def run_migration(dry_run: bool = False, force: bool = False) -> bool:
    """
    Executa migração completa.

    Returns:
        bool: True se migração foi bem-sucedida
    """
    print("=" * 60)
    print("🔄 Migração: premises/assumptions → proposicoes")
    print("=" * 60)

    if not DB_PATH.exists():
        print(f"❌ Banco não encontrado: {DB_PATH}")
        print("   Execute a aplicação primeiro para criar o banco.")
        return False

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        # Verifica versão atual
        current_version = get_schema_version(conn)
        print(f"\n📌 Versão atual: {current_version or 'não definida'}")
        print(f"📌 Versão alvo: {DATABASE_VERSION}")

        if current_version == DATABASE_VERSION and not force:
            print("\n✅ Banco já está na versão mais recente!")
            print("   Use --force para forçar migração.")
            return True

        # Backup (exceto em dry-run)
        if not dry_run:
            print("\n📦 Criando backup...")
            create_backup(DB_PATH)
        else:
            print("\n🔍 [DRY-RUN] Pulando backup")

        # Migra argumentos
        print("\n🔄 Migrando argumentos...")
        migrated = migrate_arguments(conn, dry_run)

        if migrated < 0:
            print("❌ Migração abortada devido a erro")
            return False

        # Remove colunas antigas
        if migrated > 0 or force:
            remove_old_columns(conn, dry_run)

        # Recria views
        recreate_views(conn, dry_run)

        # Atualiza versão
        update_schema_version(conn, DATABASE_VERSION, dry_run)

        if not dry_run:
            conn.commit()
            print("\n✅ Migração concluída com sucesso!")
        else:
            print("\n✅ [DRY-RUN] Simulação concluída")
            print("   Execute sem --dry-run para aplicar mudanças")

        return True

    except Exception as e:
        print(f"\n❌ Erro durante migração: {e}")
        conn.rollback()
        raise

    finally:
        conn.close()


def main():
    """Entry point do script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Migra banco de premises/assumptions para proposicoes"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula migração sem alterar banco"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Força migração mesmo se versão já é 2.0.0"
    )

    args = parser.parse_args()

    success = run_migration(dry_run=args.dry_run, force=args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
