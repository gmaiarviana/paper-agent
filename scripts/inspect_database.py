"""
Script para inspecionar o banco de dados do Paper Agent.

Este script permite:
- Verificar status do banco de dados
- Consultar dados (ideias e argumentos)
- Limpar dados (com confirmação)

Uso:
    python scripts/inspect_database.py [--clean]
"""

import sys
import sqlite3
import argparse
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Adicionar raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.database.manager import get_database_manager
from agents.database.schema import DATABASE_VERSION


def check_database_status(db_path: str = "data/data.db") -> Dict[str, Any]:
    """
    Verifica status do banco de dados.
    
    Returns:
        Dict com informações sobre o banco:
        - exists: bool
        - active: bool
        - tables: List[str]
        - schema_version: str
        - file_size: int (bytes)
    """
    db_file = Path(db_path)
    result = {
        "exists": db_file.exists(),
        "active": False,
        "tables": [],
        "schema_version": None,
        "file_size": 0
    }
    
    if not result["exists"]:
        return result
    
    result["file_size"] = db_file.stat().st_size
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Verificar se banco está acessível
        cursor.execute("SELECT 1")
        result["active"] = True
        
        # Listar tabelas
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        result["tables"] = [row[0] for row in cursor.fetchall()]
        
        # Verificar versão do schema
        try:
            cursor.execute("SELECT value FROM metadata WHERE key = 'schema_version' LIMIT 1")
            row = cursor.fetchone()
            if row:
                result["schema_version"] = row[0]
        except sqlite3.OperationalError:
            # Tabela metadata pode não existir ainda
            pass
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar banco: {e}")
        result["active"] = False
    
    return result


def get_database_stats(db_path: str = "data/data.db") -> Dict[str, Any]:
    """
    Obtém estatísticas do banco de dados.
    
    Returns:
        Dict com contagens e estatísticas
    """
    stats = {
        "ideas_count": 0,
        "arguments_count": 0,
        "ideas_by_status": {},
        "arguments_by_idea": {}
    }
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Contar ideias
        cursor.execute("SELECT COUNT(*) FROM ideas")
        stats["ideas_count"] = cursor.fetchone()[0]
        
        # Contar argumentos
        cursor.execute("SELECT COUNT(*) FROM arguments")
        stats["arguments_count"] = cursor.fetchone()[0]
        
        # Ideias por status
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM ideas 
            GROUP BY status
        """)
        stats["ideas_by_status"] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Argumentos por ideia
        cursor.execute("""
            SELECT idea_id, COUNT(*) as count
            FROM arguments
            GROUP BY idea_id
        """)
        stats["arguments_by_idea"] = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
    
    return stats


def list_all_data(db_path: str = "data/data.db") -> None:
    """Lista todos os dados do banco de dados."""
    try:
        db = get_database_manager(db_path)
        
        print("\n" + "="*80)
        print("📋 IDEIAS NO BANCO DE DADOS")
        print("="*80)
        
        ideas = db.list_ideas(limit=1000)  # Listar todas
        
        if not ideas:
            print("  (nenhuma ideia encontrada)")
        else:
            for i, idea in enumerate(ideas, 1):
                print(f"\n{i}. {idea['title']}")
                print(f"   ID: {idea['id']}")
                print(f"   Status: {idea['status']}")
                print(f"   Criada em: {idea['created_at']}")
                print(f"   Atualizada em: {idea['updated_at']}")
                if idea['current_argument_id']:
                    print(f"   Argumento focal: {idea['current_argument_id']}")
                if idea['thread_id']:
                    print(f"   Thread ID: {idea['thread_id']}")
                
                # Listar argumentos desta ideia
                arguments = db.get_arguments_by_idea(idea['id'])
                if arguments:
                    print(f"   Argumentos ({len(arguments)} versões):")
                    for arg in arguments:
                        print(f"      - V{arg['version']}: {arg['claim'][:60]}...")
        
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"❌ Erro ao listar dados: {e}")


def clean_database(db_path: str = "data/data.db", confirm: bool = False) -> None:
    """
    Limpa todos os dados do banco de dados.
    
    Args:
        db_path: Caminho do banco
        confirm: Se True, limpa sem pedir confirmação
    """
    if not confirm:
        print("\n⚠️  ATENÇÃO: Esta operação irá DELETAR TODOS os dados!")
        print("   - Todas as ideias serão removidas")
        print("   - Todos os argumentos serão removidos")
        print("   - O schema será mantido (tabelas não serão deletadas)")
        
        response = input("\n   Deseja continuar? (digite 'SIM' para confirmar): ")
        if response != "SIM":
            print("❌ Operação cancelada.")
            return
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Deletar dados (mas manter schema)
        cursor.execute("DELETE FROM arguments")
        cursor.execute("DELETE FROM ideas")
        
        # Resetar sequências se houver
        cursor.execute("DELETE FROM sqlite_sequence")
        
        conn.commit()
        conn.close()
        
        print("✅ Banco de dados limpo com sucesso!")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao limpar banco: {e}")


def check_checkpoints_db() -> Dict[str, Any]:
    """Verifica status do banco de checkpoints (LangGraph)."""
    db_path = "data/checkpoints.db"
    db_file = Path(db_path)
    
    result = {
        "exists": db_file.exists(),
        "active": False,
        "checkpoints_count": 0,
        "threads_count": 0,
        "file_size": 0
    }
    
    if not result["exists"]:
        return result
    
    result["file_size"] = db_file.stat().st_size
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Verificar se tabela existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='checkpoints'
        """)
        if cursor.fetchone():
            result["active"] = True
            
            # Contar checkpoints
            cursor.execute("SELECT COUNT(*) FROM checkpoints")
            result["checkpoints_count"] = cursor.fetchone()[0]
            
            # Contar threads únicos
            cursor.execute("SELECT COUNT(DISTINCT thread_id) FROM checkpoints")
            result["threads_count"] = cursor.fetchone()[0]
        
        conn.close()
        
    except sqlite3.Error:
        pass
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Inspecionar banco de dados do Paper Agent")
    parser.add_argument("--clean", action="store_true", help="Limpar todos os dados do banco")
    parser.add_argument("--list", action="store_true", help="Listar todos os dados")
    parser.add_argument("--checkpoints", action="store_true", help="Verificar banco de checkpoints também")
    
    args = parser.parse_args()
    
    print("="*80)
    print("🔍 INSPEÇÃO DO BANCO DE DADOS - PAPER AGENT")
    print("="*80)
    
    # Verificar banco principal (data.db)
    print("\n📊 BANCO PRINCIPAL (data/data.db)")
    print("-" * 80)
    
    status = check_database_status()
    
    if not status["exists"]:
        print("❌ Banco de dados não existe ainda")
        print("   (será criado automaticamente na primeira execução)")
        return
    
    if not status["active"]:
        print("❌ Banco de dados existe mas não está acessível")
        return
    
    print(f"✅ Banco ativo")
    print(f"   Tamanho: {status['file_size']:,} bytes ({status['file_size'] / 1024:.2f} KB)")
    print(f"   Tabelas: {', '.join(status['tables']) if status['tables'] else 'nenhuma'}")
    if status["schema_version"]:
        print(f"   Versão do schema: {status['schema_version']}")
    
    # Estatísticas
    print("\n📈 ESTATÍSTICAS")
    print("-" * 80)
    
    stats = get_database_stats()
    print(f"   Ideias: {stats['ideas_count']}")
    print(f"   Argumentos: {stats['arguments_count']}")
    
    if stats['ideas_by_status']:
        print(f"\n   Ideias por status:")
        for status_name, count in stats['ideas_by_status'].items():
            print(f"      - {status_name}: {count}")
    
    if stats['arguments_by_idea']:
        print(f"\n   Argumentos por ideia:")
        for idea_id, count in list(stats['arguments_by_idea'].items())[:5]:
            print(f"      - {idea_id[:8]}...: {count} versões")
        if len(stats['arguments_by_idea']) > 5:
            print(f"      ... e mais {len(stats['arguments_by_idea']) - 5} ideias")
    
    # Verificar banco de checkpoints se solicitado
    if args.checkpoints:
        print("\n📊 BANCO DE CHECKPOINTS (data/checkpoints.db)")
        print("-" * 80)
        
        checkpoints = check_checkpoints_db()
        if checkpoints["exists"]:
            if checkpoints["active"]:
                print(f"✅ Banco ativo")
                print(f"   Tamanho: {checkpoints['file_size']:,} bytes ({checkpoints['file_size'] / 1024:.2f} KB)")
                print(f"   Checkpoints: {checkpoints['checkpoints_count']}")
                print(f"   Threads: {checkpoints['threads_count']}")
            else:
                print("⚠️  Banco existe mas tabela 'checkpoints' não encontrada")
        else:
            print("ℹ️  Banco de checkpoints não existe ainda")
    
    # Listar dados se solicitado
    if args.list:
        list_all_data()
    
    # Limpar se solicitado
    if args.clean:
        clean_database()
    
    print("\n" + "="*80)
    print("✅ Inspeção concluída")
    print("="*80)


if __name__ == "__main__":
    main()

