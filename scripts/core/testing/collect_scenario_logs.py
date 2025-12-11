#!/usr/bin/env python3
"""
Script para coletar logs de validação manual do Épico 7.

Este script facilita a coleta automática de logs após executar cada cenário
de validação manualmente. Copia EventBus JSON e tenta extrair MultiAgentState
do checkpoints.db.

Uso:
    python scripts/testing/collect_scenario_logs.py \
        --scenario "cenario_01_usuario_vago" \
        --session-id "session-20251204-215447-662"
"""

import argparse
import json
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Adicionar diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import tempfile

def get_events_file_path(session_id: str) -> Path:
    """
    Retorna caminho do arquivo de eventos do EventBus.
    
    Args:
        session_id: ID da sessão
        
    Returns:
        Path: Caminho do arquivo JSON de eventos
    """
    system_temp = Path(tempfile.gettempdir())
    events_dir = system_temp / "paper-agent-events"
    return events_dir / f"events-{session_id}.json"

def copy_eventbus_json(session_id: str, dest_dir: Path) -> bool:
    """
    Copia arquivo JSON do EventBus para diretório de destino.
    
    Args:
        session_id: ID da sessão
        dest_dir: Diretório de destino (logs/)
        
    Returns:
        bool: True se copiou com sucesso, False caso contrário
    """
    source_file = get_events_file_path(session_id)
    dest_file = dest_dir / "events.json"
    
    if not source_file.exists():
        print(f"⚠️  Arquivo de eventos não encontrado: {source_file}")
        return False
    
    try:
        shutil.copy2(source_file, dest_file)
        print(f"✅ EventBus JSON copiado: {dest_file}")
        return True
    except (IOError, PermissionError) as e:
        print(f"❌ Erro ao copiar EventBus JSON: {e}")
        return False

def extract_state_from_checkpoints(session_id: str, dest_dir: Path) -> bool:
    """
    Tenta extrair MultiAgentState do checkpoints.db.
    
    NOTA: Esta função é experimental. O LangGraph SqliteSaver armazena
    checkpoints em formato binário (pickle), então a extração pode ser
    complexa. Se não conseguir, apenas avisa mas não falha.
    
    Args:
        session_id: ID da sessão (thread_id no checkpoints.db)
        dest_dir: Diretório de destino (logs/)
        
    Returns:
        bool: True se extraiu com sucesso, False caso contrário
    """
    db_path = project_root / "data" / "checkpoints.db"
    
    if not db_path.exists():
        print(f"⚠️  Banco de checkpoints não encontrado: {db_path}")
        return False
    
    try:
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            
            # Verificar se thread_id existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM checkpoints 
                WHERE thread_id = ?
            """, (session_id,))
            
            count = cursor.fetchone()[0]
            
            if count == 0:
                print(f"⚠️  Nenhum checkpoint encontrado para thread_id: {session_id}")
                return False
            
            # Buscar último checkpoint desta thread
            cursor.execute("""
                SELECT checkpoint_ns, checkpoint 
                FROM checkpoints 
                WHERE thread_id = ? 
                ORDER BY checkpoint_ns DESC 
                LIMIT 1
            """, (session_id,))
            
            row = cursor.fetchone()
            
            if not row:
                print(f"⚠️  Não foi possível ler checkpoint para thread_id: {session_id}")
                return False
            
            checkpoint_ns, checkpoint_blob = row
            
            # O checkpoint_blob é um objeto serializado (pickle) do LangGraph
            # Tentar extrair informações básicas
            # NOTA: Deserializar pode ser complexo, então vamos apenas salvar
            # informações básicas por enquanto
            
            state_info = {
                "thread_id": session_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_size_bytes": len(checkpoint_blob) if checkpoint_blob else 0,
                "note": "Checkpoint armazenado em formato binário (pickle) pelo LangGraph. "
                        "Para extrair MultiAgentState completo, use ferramentas do LangGraph.",
                "extraction_status": "partial"
            }
            
            # Tentar buscar informações adicionais da tabela (se existir)
            try:
                cursor.execute("""
                    SELECT checkpoint_ns, checkpoint 
                    FROM checkpoints 
                    WHERE thread_id = ? 
                    ORDER BY checkpoint_ns
                """, (session_id,))
                
                all_checkpoints = cursor.fetchall()
                state_info["total_checkpoints"] = len(all_checkpoints)
                state_info["checkpoints_timeline"] = [
                    {"checkpoint_ns": cp[0], "size_bytes": len(cp[1]) if cp[1] else 0}
                    for cp in all_checkpoints
                ]
            except sqlite3.Error:
                pass
            
            # Salvar informações extraídas
            dest_file = dest_dir / "state.json"
            with open(dest_file, 'w', encoding='utf-8') as f:
                json.dump(state_info, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Informações de estado extraídas: {dest_file}")
            print(f"   ⚠️  Estado completo requer deserialização do LangGraph (TODO)")
            return True
            
    except sqlite3.Error as e:
        print(f"⚠️  Erro ao acessar checkpoints.db: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Erro inesperado ao extrair estado: {e}")
        return False

def create_metadata(
    session_id: str,
    scenario: str,
    dest_dir: Path,
    events_copied: bool,
    state_extracted: bool
) -> None:
    """
    Cria arquivo metadata.txt com informações da coleta.
    
    Args:
        session_id: ID da sessão
        scenario: Nome do cenário
        dest_dir: Diretório de destino (logs/)
        events_copied: Se EventBus foi copiado
        state_extracted: Se estado foi extraído
    """
    metadata_file = dest_dir / "metadata.txt"
    
    status = "sucesso" if events_copied else "parcial"
    if not events_copied:
        status = "falha"
    elif not state_extracted:
        status = "parcial"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    command = f"python scripts/testing/collect_scenario_logs.py --scenario {scenario} --session-id {session_id}"
    
    content = f"""METADADOS DA COLETA DE LOGS
=====================================

Timestamp da Coleta: {timestamp}
Session ID: {session_id}
Cenário: {scenario}
Status da Coleta: {status}

Comando Executado:
{command}

Arquivos Coletados:
- events.json: {'✅ Sim' if events_copied else '❌ Não'}
- state.json: {'✅ Sim' if state_extracted else '⚠️  Parcial/Não'}

Próximos Passos:
1. Preencher input.md com input do usuário
2. Preencher output.md com output observado
3. Preencher analysis.md com análise do comportamento
4. Adicionar screenshots ou logs adicionais em logs/ se necessário
"""
    
    try:
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Metadata criado: {metadata_file}")
    except IOError as e:
        print(f"❌ Erro ao criar metadata: {e}")

def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Coletar logs de validação manual do Épico 7",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplo de uso:
  python scripts/testing/collect_scenario_logs.py \\
      --scenario "cenario_01_usuario_vago" \\
      --session-id "session-20251204-215447-662"
        """
    )
    
    parser.add_argument(
        "--scenario",
        type=str,
        required=True,
        help="Nome do cenário (ex: cenario_01_usuario_vago)"
    )
    
    parser.add_argument(
        "--session-id",
        type=str,
        required=True,
        help="ID da sessão do EventBus (ex: session-20251204-215447-662)"
    )
    
    args = parser.parse_args()
    
    # Validar cenário
    scenario_dir = project_root / "docs" / "testing" / "epic7_results" / args.scenario
    if not scenario_dir.exists():
        print(f"❌ Diretório do cenário não encontrado: {scenario_dir}")
        print(f"   Cenários disponíveis:")
        results_dir = project_root / "docs" / "testing" / "epic7_results"
        if results_dir.exists():
            for item in sorted(results_dir.iterdir()):
                if item.is_dir() and item.name.startswith("cenario_"):
                    print(f"     - {item.name}")
        sys.exit(1)
    
    logs_dir = scenario_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("COLETA DE LOGS - ÉPICO 7")
    print("=" * 70)
    print(f"Cenário: {args.scenario}")
    print(f"Session ID: {args.session_id}")
    print(f"Diretório de destino: {logs_dir}")
    print()
    
    # 1. Copiar EventBus JSON
    print("📋 Copiando EventBus JSON...")
    events_copied = copy_eventbus_json(args.session_id, logs_dir)
    print()
    
    # 2. Tentar extrair MultiAgentState (opcional)
    print("📋 Extraindo MultiAgentState do checkpoints.db...")
    state_extracted = extract_state_from_checkpoints(args.session_id, logs_dir)
    print()
    
    # 3. Criar metadata
    print("📋 Criando metadata...")
    create_metadata(
        args.session_id,
        args.scenario,
        logs_dir,
        events_copied,
        state_extracted
    )
    print()
    
    # 4. Resumo final
    print("=" * 70)
    print("RESUMO DA COLETA")
    print("=" * 70)
    print(f"✅ EventBus JSON: {'Copiado' if events_copied else 'Não encontrado'}")
    print(f"{'✅' if state_extracted else '⚠️ '} MultiAgentState: {'Extraído' if state_extracted else 'Parcial/Não disponível'}")
    print()
    
    print("📁 Arquivos criados em:", logs_dir)
    for file in sorted(logs_dir.iterdir()):
        if file.is_file():
            size = file.stat().st_size
            print(f"   - {file.name} ({size} bytes)")
    print()
    
    print("📝 PRÓXIMOS PASSOS:")
    print("   1. Preencher input.md com input do usuário")
    print("   2. Preencher output.md com output observado")
    print("   3. Preencher analysis.md com análise do comportamento")
    print("   4. Adicionar screenshots ou logs adicionais em logs/ se necessário")
    print()
    
    if not events_copied:
        print("⚠️  ATENÇÃO: EventBus JSON não foi encontrado.")
        print(f"   Verifique se o arquivo existe: {get_events_file_path(args.session_id)}")
        sys.exit(1)
    
    print("✅ Coleta concluída com sucesso!")

if __name__ == "__main__":
    main()

