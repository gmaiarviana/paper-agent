"""
Executa cenário específico de validação multi-turn.

Usage:
    python scripts/testing/run_scenario.py --scenario 3
    python scripts/testing/run_scenario.py --scenario 6
    python scripts/testing/run_scenario.py --scenario 7
    python scripts/testing/run_scenario.py --scenario 3 --save
"""

import argparse
import sys
from pathlib import Path
import json
from datetime import datetime

# Adicionar raiz ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph
from utils.test_executor import MultiTurnExecutor
from utils.test_scenarios import ConversationScenario


def format_result_for_terminal(result: dict) -> str:
    """
    Formata resultado para exibição no terminal.
    
    Args:
        result: Resultado do execute_scenario()
        
    Returns:
        String formatada para print
    """
    lines = []
    lines.append("=" * 70)
    lines.append(f"CENÁRIO: {result['scenario_id']}")
    lines.append("=" * 70)
    lines.append("")
    
    # Status
    status_icon = "✅" if result['success'] else "❌"
    lines.append(f"Status: {status_icon} {'SUCESSO' if result['success'] else 'FALHA'}")
    lines.append("")
    
    # Agentes
    lines.append(f"Agentes chamados: {', '.join(result['agents_called'])}")
    lines.append("")
    
    # Turnos
    lines.append(f"Total de turnos: {len(result['turns'])}")
    for turn in result['turns']:
        lines.append(f"\n[Turno {turn['turn']}]")
        lines.append(f"  Input: {turn['user_input'][:60]}...")
        lines.append(f"  next_step: {turn['next_step']}")
        if turn['agents_called']:
            lines.append(f"  Agentes: {', '.join(turn['agents_called'])}")
    
    lines.append("")
    lines.append("=" * 70)
    
    # Métricas
    metrics = result['metrics']
    lines.append("MÉTRICAS:")
    lines.append(f"  Tokens: {metrics['total_tokens']}")
    lines.append(f"  Custo: ${metrics['total_cost']:.4f}")
    lines.append(f"  Duração: {metrics['total_duration']:.2f}s")
    lines.append("=" * 70)
    
    # Erros de validação (se houver)
    if result['validation_errors']:
        lines.append("")
        lines.append("⚠️ ERROS DE VALIDAÇÃO:")
        for error in result['validation_errors']:
            lines.append(f"  - {error}")
        lines.append("=" * 70)
    
    return "\n".join(lines)


def save_result_to_file(result: dict, output_dir: Path):
    """
    Salva resultado em arquivo JSON com timestamp.
    
    Args:
        result: Resultado do execute_scenario()
        output_dir: Diretório de saída
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{result['scenario_id']}_{timestamp}.json"
    filepath = output_dir / filename
    
    # Serializar (remover objetos não-serializáveis)
    serializable_result = {
        "scenario_id": result["scenario_id"],
        "session_id": result["session_id"],
        "turns": result["turns"],
        "agents_called": result["agents_called"],
        "metrics": result["metrics"],
        "success": result["success"],
        "validation_errors": result["validation_errors"],
        # final_state pode ter objetos LangChain, omitir
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultado salvo: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Executa cenário específico de validação multi-turn"
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
        help="Salvar resultado em arquivo JSON"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="logs/multi_turn",
        help="Diretório para salvar resultados (padrão: logs/multi_turn)"
    )
    
    args = parser.parse_args()
    
    print(f"\n🚀 Executando Cenário {args.scenario}...\n")
    
    # Criar grafo e executor
    graph = create_multi_agent_graph()
    executor = MultiTurnExecutor(graph)
    
    # Carregar cenário
    scenario = ConversationScenario.from_epic7_scenario(args.scenario)
    
    # Executar
    result = executor.execute_scenario(scenario)
    
    # Exibir resultado
    formatted = format_result_for_terminal(result)
    print(formatted)
    
    # Salvar se solicitado
    if args.save:
        output_dir = Path(args.output_dir)
        save_result_to_file(result, output_dir)
    
    # Exit code baseado em sucesso
    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()

