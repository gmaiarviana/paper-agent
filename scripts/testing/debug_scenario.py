"""
Debug detalhado de cenário específico.

Usage:
    python scripts/testing/debug_scenario.py --scenario 3
    python scripts/testing/debug_scenario.py --scenario 7
    python scripts/testing/debug_scenario.py --scenario 3 --save
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Adicionar raiz ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph
from utils.debug_analyzer import DebugAnalyzer
from utils.test_scenarios import ConversationScenario


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
        "--save",
        action="store_true",
        help="Salvar relatório em arquivo"
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
    
    # Analisar
    report = analyzer.analyze_scenario(scenario)
    
    # Exibir
    print(report)
    
    # Salvar se solicitado
    if args.save:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_{scenario.id}_{timestamp}.txt"
        filepath = output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n💾 Relatório salvo: {filepath}")


if __name__ == "__main__":
    main()

