"""
Debug detalhado de cenário específico.

Usage:
    python scripts/testing/debug_scenario.py --scenario 3
    python scripts/testing/debug_scenario.py --scenario 7
    python scripts/testing/debug_scenario.py --scenario 3 --level full
    python scripts/testing/debug_scenario.py --scenario 3 --level trace
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Adicionar raiz ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.agents.multi_agent_graph import create_multi_agent_graph
from core.utils.debug_analyzer import DebugAnalyzer
from core.utils.test_scenarios import ConversationScenario
from core.utils.structured_logger import StructuredLogger
from core.utils.debug_reporter import DebugReporter

def main():
    parser = argparse.ArgumentParser(
        description="Debug detalhado de cenário multi-turn"
    )
    parser.add_argument(
        "--scenario",
        type=int,
        required=True,
        choices=[3, 6, 7],
        help="Número do cenário (3, 6 ou 7)"
    )
    parser.add_argument(
        "--level",
        choices=["basic", "full", "trace"],
        default="basic",
        help="Nível de detalhe do debug (padrão: basic)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="logs/debug",
        help="Diretório para salvar relatório (padrão: logs/debug)"
    )
    
    args = parser.parse_args()
    
    print(f"\n🔍 Iniciando debug do Cenário {args.scenario}...\n")
    
    # Criar grafo e analyzer
    graph = create_multi_agent_graph()
    analyzer = DebugAnalyzer(graph)
    
    # Carregar cenário
    scenario = ConversationScenario.from_epic7_scenario(args.scenario)
    
    # Executar cenário e obter resultado completo (para acessar session_id)
    result = analyzer.executor.execute_scenario(scenario)
    trace_id = result['session_id']  # trace_id é o mesmo que session_id
    
    print(f"📋 Trace ID: {trace_id}\n")
    
    # Gerar relatório tradicional do analyzer
    analyzer_report = analyzer._generate_debug_report(result, scenario)
    print(analyzer_report)
    
    # Ler logs estruturados
    logger = StructuredLogger()
    logs = logger.read_logs(trace_id)
    
    # Gerar debug report estruturado se houver logs
    if logs:
        print("\n" + "="*60)
        print("DEBUG REPORT ESTRUTURADO")
        print("="*60)
        
        reporter = DebugReporter()
        debug_report = reporter.generate_debug_report(trace_id, logs)
        
        # Exibir conforme nível
        if args.level == "basic":
            # Extrair só sumário final (últimas 10 linhas)
            summary_lines = debug_report.split("\n")[-10:]
            print("\n" + "\n".join(summary_lines))
        elif args.level == "full":
            print("\n" + debug_report)
        elif args.level == "trace":
            print("\n" + debug_report)
            print("\n" + "="*60)
            print("RAW JSONL LOGS:")
            print("="*60)
            for log in logs:
                print(json.dumps(log, indent=2, ensure_ascii=False))
        
        # Sempre salvar report estruturado
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_{scenario.id}_{trace_id}_{timestamp}.txt"
        filepath = output_dir / filename
        
        # Combinar relatórios: analyzer + structured
        full_report = f"{analyzer_report}\n\n{'='*60}\nDEBUG REPORT ESTRUTURADO\n{'='*60}\n\n{debug_report}"
        
        if args.level == "trace":
            # Adicionar logs raw no modo trace
            full_report += f"\n\n{'='*60}\nRAW JSONL LOGS\n{'='*60}\n\n"
            for log in logs:
                full_report += json.dumps(log, indent=2, ensure_ascii=False) + "\n\n"
        
        filepath.write_text(full_report, encoding="utf-8")
        print(f"\n✅ Debug report salvo em: {filepath}")
    else:
        print(f"\n⚠️  Nenhum log estruturado encontrado para trace_id: {trace_id}")
        print(f"    Verifique se os agentes foram instrumentados corretamente.")
        
        # Salvar apenas relatório do analyzer se não houver logs estruturados
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_{scenario.id}_{trace_id}_{timestamp}.txt"
        filepath = output_dir / filename
        
        filepath.write_text(analyzer_report, encoding="utf-8")
        print(f"✅ Relatório do analyzer salvo em: {filepath}")

if __name__ == "__main__":
    main()

