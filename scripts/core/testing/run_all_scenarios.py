"""
Executa todos os cenários de validação multi-turn (3, 6, 7).

Usage:
    python scripts/testing/run_all_scenarios.py
    python scripts/testing/run_all_scenarios.py --save
"""

import argparse
import sys
from pathlib import Path
import json
from datetime import datetime

# Adicionar raiz ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.agents.multi_agent_graph import create_multi_agent_graph
from core.utils.test_executor import MultiTurnExecutor
from core.utils.test_scenarios import ConversationScenario

def main():
    parser = argparse.ArgumentParser(
        description="Executa todos os cenários de validação multi-turn"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Salvar resultados em arquivo JSON"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="logs/multi_turn",
        help="Diretório para salvar resultados (padrão: logs/multi_turn)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("EXECUTANDO SUITE COMPLETA DE CENÁRIOS MULTI-TURN")
    print("=" * 70)
    
    # Criar grafo e executor (reutilizar para todos cenários)
    print("\n📦 Criando grafo multi-agente...")
    graph = create_multi_agent_graph()
    executor = MultiTurnExecutor(graph)
    
    scenarios = [3, 6, 7]
    results = []
    
    for scenario_num in scenarios:
        print(f"\n🚀 Executando Cenário {scenario_num}...")
        
        # Carregar e executar
        scenario = ConversationScenario.from_epic7_scenario(scenario_num)
        result = executor.execute_scenario(scenario)
        results.append(result)
        
        # Exibir sumário
        status_icon = "✅" if result['success'] else "❌"
        print(f"   {status_icon} {result['scenario_id']}: {'SUCESSO' if result['success'] else 'FALHA'}")
        print(f"      Turnos: {len(result['turns'])}, Agentes: {', '.join(result['agents_called'])}")
        print(f"      Tokens: {result['metrics']['total_tokens']}, Custo: ${result['metrics']['total_cost']:.4f}")
    
    # Sumário final
    print("\n" + "=" * 70)
    print("SUMÁRIO FINAL")
    print("=" * 70)
    
    total_success = sum(1 for r in results if r['success'])
    total_scenarios = len(results)
    
    print(f"\nSucesso: {total_success}/{total_scenarios} cenários")
    
    # Métricas agregadas
    total_tokens = sum(r['metrics']['total_tokens'] for r in results)
    total_cost = sum(r['metrics']['total_cost'] for r in results)
    total_duration = sum(r['metrics']['total_duration'] for r in results)
    
    print(f"\nMétricas agregadas:")
    print(f"  Total de tokens: {total_tokens}")
    print(f"  Custo total: ${total_cost:.4f}")
    print(f"  Duração total: {total_duration:.2f}s")
    
    # Listar falhas
    failures = [r for r in results if not r['success']]
    if failures:
        print(f"\n❌ Cenários com falha:")
        for r in failures:
            print(f"  - {r['scenario_id']}")
            for error in r['validation_errors']:
                print(f"    • {error}")
    
    print("\n" + "=" * 70)
    
    # Salvar se solicitado
    if args.save:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"suite_completa_{timestamp}.json"
        filepath = output_dir / filename
        
        # Preparar dados serializáveis
        summary = {
            "timestamp": timestamp,
            "total_scenarios": total_scenarios,
            "success_count": total_success,
            "failure_count": total_scenarios - total_success,
            "metrics": {
                "total_tokens": total_tokens,
                "total_cost": total_cost,
                "total_duration": total_duration
            },
            "results": [
                {
                    "scenario_id": r["scenario_id"],
                    "success": r["success"],
                    "agents_called": r["agents_called"],
                    "metrics": r["metrics"],
                    "validation_errors": r["validation_errors"]
                }
                for r in results
            ]
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados salvos: {filepath}")
    
    # Exit code baseado em sucesso total
    sys.exit(0 if total_success == total_scenarios else 1)

if __name__ == "__main__":
    main()

