#!/usr/bin/env python3
"""
Script para reproduzir sessão passo a passo.

Usage:
    python scripts/testing/replay_session.py test-scenario-3-1764958744
    python scripts/testing/replay_session.py test-scenario-3-1764958744 --speed fast
    python scripts/testing/replay_session.py test-scenario-3-1764958744 --turn 2
    python scripts/testing/replay_session.py test-scenario-3-1764958744 --export report.md
"""

import sys
import argparse
from pathlib import Path

# Adicionar project root ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.structured_logger import StructuredLogger
from utils.debug_reporter import DebugReporter


def replay_session(trace_id: str, speed: str = "normal", start_turn: int = 1, export: str = None):
    """Reproduz sessão passo a passo."""
    
    # 1. Ler logs
    logger = StructuredLogger()
    logs = logger.read_logs(trace_id)
    
    if not logs:
        print(f"❌ Nenhum log encontrado para trace_id: {trace_id}")
        print(f"   Verifique se o arquivo existe: logs/structured/{trace_id}.jsonl")
        return
    
    # 2. Agrupar por turno (usar DebugReporter._group_by_turn)
    reporter = DebugReporter()
    turns = reporter._group_by_turn(logs)
    
    print("=" * 60)
    print(f"SESSION REPLAY: {trace_id}")
    print("=" * 60)
    print(f"Total de turnos: {len(turns)}")
    print(f"Total de logs: {len(logs)}")
    print("")
    
    # 3. Replay turno a turno
    for turn_num, turn_logs in enumerate(turns, 1):
        if turn_num < start_turn:
            continue
        
        print(f"[TURN {turn_num}]")
        print("")
        
        for log in turn_logs:
            agent = log.get("agent", "unknown")
            icon = reporter.AGENT_ICONS.get(agent, "🤖")
            event = log.get("event", "unknown")
            message = log.get("message", "No message")
            
            print(f"{icon} {agent.title()}: {message}")
            
            # Se decision_made, mostrar decision e reasoning (truncado)
            if event == "decision_made":
                metadata = log.get("metadata", {})
                decision = metadata.get("decision", {})
                reasoning = metadata.get("reasoning", "")
                
                if decision:
                    # Formatar decision dict de forma legível
                    decision_str = ", ".join([f"{k}={v}" for k, v in decision.items() if v])
                    if decision_str:
                        print(f"├─ Decision: {decision_str}")
                
                if reasoning:
                    # Truncar reasoning para 100 caracteres
                    reasoning_preview = reasoning[:100] + "..." if len(reasoning) > 100 else reasoning
                    print(f"└─ Reasoning: {reasoning_preview}")
            
            # Se agent_completed, mostrar métricas resumidas
            elif event == "agent_completed":
                metadata = log.get("metadata", {})
                duration_ms = metadata.get("duration_ms", 0)
                cost = metadata.get("cost", 0)
                tokens_total = metadata.get("tokens_total", 0)
                
                if duration_ms or cost or tokens_total:
                    metrics_parts = []
                    if duration_ms:
                        duration_s = duration_ms / 1000
                        metrics_parts.append(f"{duration_s:.1f}s")
                    if tokens_total:
                        metrics_parts.append(f"{tokens_total} tokens")
                    if cost:
                        metrics_parts.append(f"${cost:.4f}")
                    
                    if metrics_parts:
                        print(f"└─ Metrics: {', '.join(metrics_parts)}")
            
            # Se error, mostrar tipo e mensagem
            elif event == "error":
                metadata = log.get("metadata", {})
                error_type = metadata.get("error_type", "Unknown")
                error_message = metadata.get("error_message", "No error message")
                print(f"└─ Error: {error_type}: {error_message[:100]}")
            
            print("")
        
        print("-" * 60)
        
        # Pausa se speed == normal
        if speed == "normal":
            user_input = input("\n[Pressione Enter para próximo turno ou 'q' para sair] ")
            if user_input.lower() == 'q':
                print("\n⏹️  Replay interrompido pelo usuário.")
                break
        
        print("")
    
    print("=" * 60)
    print("Replay completo!")
    print("=" * 60)
    
    # 4. Exportar se solicitado
    if export:
        report = reporter.generate_debug_report(trace_id, logs)
        export_path = Path(export)
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(report, encoding="utf-8")
        print(f"\n✅ Report exportado: {export_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Reproduz sessão passo a passo a partir de logs estruturados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Replay interativo (pausa entre turnos)
  python scripts/testing/replay_session.py test-scenario-3-1764958744
  
  # Replay rápido (sem pausa)
  python scripts/testing/replay_session.py test-scenario-3-1764958744 --speed fast
  
  # Começar a partir do turno 2
  python scripts/testing/replay_session.py test-scenario-3-1764958744 --turn 2
  
  # Exportar replay como markdown
  python scripts/testing/replay_session.py test-scenario-3-1764958744 --export report.md
        """
    )
    parser.add_argument(
        "trace_id",
        help="ID da sessão (trace_id). Exemplo: test-scenario-3-1764958744"
    )
    parser.add_argument(
        "--speed",
        choices=["normal", "fast"],
        default="normal",
        help="Velocidade do replay (normal=pausa entre turnos, fast=sem pausa). Padrão: normal"
    )
    parser.add_argument(
        "--turn",
        type=int,
        default=1,
        help="Começar a partir do turno N (padrão: 1)"
    )
    parser.add_argument(
        "--export",
        help="Exportar replay como markdown (caminho do arquivo)"
    )
    
    args = parser.parse_args()
    replay_session(args.trace_id, args.speed, args.turn, args.export)


if __name__ == "__main__":
    main()

