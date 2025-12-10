#!/usr/bin/env python3
"""
Script de validacao para deteccao de mudancas do Observer (Epico 13.6).

Executa cenarios de teste A-D automaticamente e gera relatorio
com eventos publicados e decisoes do sistema.

Uso:
    python scripts/validate_direction_change.py [--verbose] [--scenario A|B|C|D|all]

Cenarios:
    A: Variacao simples (nao interrompe fluxo)
    B: Mudanca real (checkpoint solicitado)
    C: Clareza nebulosa (needs_checkpoint=True)
    D: Conversa clara (needs_checkpoint=False)

Versao: 1.0 (Epico 13.6)
Data: 10/12/2025
"""

import sys
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, List

# Adicionar path do projeto
sys.path.insert(0, ".")

from core.agents.multi_agent_graph import create_multi_agent_graph
from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.utils.event_bus import get_event_bus


# ============================================================================
# Configuracao de Logging
# ============================================================================


def setup_logging(verbose: bool = False):
    """Configura logging baseado no nivel de verbosidade."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    return logging.getLogger(__name__)


# ============================================================================
# Definicao dos Cenarios
# ============================================================================


SCENARIOS = {
    "A": {
        "id": "cenario_A_variacao",
        "name": "Variacao Simples",
        "description": "Variacao do mesmo conceito - NAO deve interromper fluxo",
        "turns": [
            "LLMs aumentam produtividade de desenvolvedores",
            "IA generativa melhora eficiencia no desenvolvimento de software",
        ],
        "expected_checkpoint": False,
        "expected_classification": "variation",
    },
    "B": {
        "id": "cenario_B_mudanca_real",
        "name": "Mudanca Real",
        "description": "Mudanca completa de topico - DEVE triggerar checkpoint",
        "turns": [
            "LLMs aumentam produtividade de desenvolvedores",
            "Quero falar sobre blockchain e criptomoedas",
        ],
        "expected_checkpoint": True,
        "expected_classification": "real_change",
    },
    "C": {
        "id": "cenario_C_nebuloso",
        "name": "Clareza Nebulosa",
        "description": "Conversa confusa - DEVE triggerar checkpoint de clareza",
        "turns": [
            "Quero pesquisar sobre IA, mas tambem blockchain, e talvez machine learning",
            "Na verdade acho que produtividade e importante, ou seria qualidade?",
        ],
        "expected_checkpoint": True,
        "expected_classification": None,
    },
    "D": {
        "id": "cenario_D_claro",
        "name": "Conversa Clara",
        "description": "Conversa consistente - NAO deve triggerar checkpoint",
        "turns": [
            "LLMs aumentam produtividade de desenvolvedores em 30%",
            "Especificamente em equipes de 5-10 pessoas usando pair programming",
        ],
        "expected_checkpoint": False,
        "expected_classification": "variation",
    },
}


# ============================================================================
# Executor de Cenarios
# ============================================================================


def execute_scenario(
    graph,
    scenario: Dict[str, Any],
    logger: logging.Logger
) -> Dict[str, Any]:
    """
    Executa um cenario e retorna resultado.

    Args:
        graph: Grafo multi-agente
        scenario: Definicao do cenario
        logger: Logger para output

    Returns:
        Dict com resultado da execucao
    """
    session_id = f"validate-{scenario['id']}-{int(datetime.now().timestamp())}"
    event_bus = get_event_bus()

    logger.info(f"\n{'='*60}")
    logger.info(f"Executando: {scenario['name']}")
    logger.info(f"Descricao: {scenario['description']}")
    logger.info(f"Session ID: {session_id}")
    logger.info(f"{'='*60}")

    # Limpar eventos anteriores
    event_bus.clear_session(session_id)

    # Executar turnos
    state = None
    for i, turn_input in enumerate(scenario["turns"]):
        logger.info(f"\n[Turno {i+1}] User: {turn_input[:60]}...")

        if state is None:
            state = create_initial_multi_agent_state(
                user_input=turn_input,
                session_id=session_id
            )
        else:
            state["user_input"] = turn_input

        config = {"configurable": {"thread_id": session_id}}

        try:
            state = graph.invoke(state, config)
            logger.info(f"  -> next_step: {state.get('next_step')}")
            logger.debug(f"  -> message: {state.get('orchestrator_message', '')[:100]}...")
        except Exception as e:
            logger.error(f"  -> ERRO: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }

    # Coletar eventos de deteccao
    events = event_bus.get_session_events(session_id)
    detection_events = [
        e for e in events
        if e.get("event_type") in [
            "variation_detected",
            "direction_change_confirmed",
            "clarity_checkpoint"
        ]
    ]

    # Analisar resultados
    event_types = [e.get("event_type") for e in detection_events]
    checkpoint_triggered = any(
        et in ["direction_change_confirmed", "clarity_checkpoint"]
        for et in event_types
    )

    classification = None
    for e in detection_events:
        if e.get("classification"):
            classification = e.get("classification")
            break

    return {
        "success": True,
        "session_id": session_id,
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "final_state": state,
        "detection_events": detection_events,
        "event_types": event_types,
        "checkpoint_triggered": checkpoint_triggered,
        "classification": classification,
        "expected_checkpoint": scenario["expected_checkpoint"],
        "expected_classification": scenario["expected_classification"],
    }


def validate_result(result: Dict[str, Any], logger: logging.Logger) -> bool:
    """
    Valida resultado de um cenario.

    Args:
        result: Resultado da execucao
        logger: Logger para output

    Returns:
        True se validacao passou, False caso contrario
    """
    if not result.get("success"):
        logger.error(f"FALHA: Execucao falhou - {result.get('error')}")
        return False

    errors = []

    # Validar checkpoint
    expected_cp = result["expected_checkpoint"]
    actual_cp = result["checkpoint_triggered"]

    if expected_cp and not actual_cp:
        errors.append("Checkpoint esperado mas NAO encontrado")
    elif not expected_cp and actual_cp:
        errors.append("Checkpoint NAO esperado mas encontrado")

    # Validar classificacao (se esperada)
    expected_class = result["expected_classification"]
    actual_class = result["classification"]

    if expected_class and actual_class and expected_class != actual_class:
        errors.append(f"Classificacao esperada '{expected_class}', obtida '{actual_class}'")

    # Reportar resultado
    logger.info(f"\n--- Resultado ---")
    logger.info(f"Eventos detectados: {result['event_types']}")
    logger.info(f"Checkpoint triggered: {actual_cp} (esperado: {expected_cp})")
    logger.info(f"Classificacao: {actual_class} (esperada: {expected_class})")

    if errors:
        logger.error(f"VALIDACAO FALHOU:")
        for error in errors:
            logger.error(f"  - {error}")
        return False
    else:
        logger.info(f"VALIDACAO OK")
        return True


# ============================================================================
# Relatorio
# ============================================================================


def generate_report(results: List[Dict[str, Any]], logger: logging.Logger) -> None:
    """
    Gera relatorio consolidado dos cenarios executados.

    Args:
        results: Lista de resultados
        logger: Logger para output
    """
    logger.info(f"\n{'='*60}")
    logger.info("RELATORIO CONSOLIDADO")
    logger.info(f"{'='*60}")

    total = len(results)
    passed = sum(1 for r in results if r.get("validation_passed"))
    failed = total - passed

    logger.info(f"\nTotal de cenarios: {total}")
    logger.info(f"Passaram: {passed}")
    logger.info(f"Falharam: {failed}")

    logger.info(f"\n--- Detalhes por Cenario ---\n")

    for r in results:
        status = "PASS" if r.get("validation_passed") else "FAIL"
        logger.info(f"[{status}] {r.get('scenario_name', 'N/A')}")
        logger.info(f"       Eventos: {r.get('event_types', [])}")
        logger.info(f"       Checkpoint: {r.get('checkpoint_triggered')} (esperado: {r.get('expected_checkpoint')})")
        logger.info("")

    # Resumo final
    if failed == 0:
        logger.info("TODOS OS CENARIOS PASSARAM!")
    else:
        logger.warning(f"ATENCAO: {failed} cenario(s) falharam!")


# ============================================================================
# Main
# ============================================================================


def main():
    """Ponto de entrada do script."""
    parser = argparse.ArgumentParser(
        description="Valida deteccao de mudancas do Observer"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Modo verbose com logs detalhados"
    )
    parser.add_argument(
        "--scenario", "-s",
        choices=["A", "B", "C", "D", "all"],
        default="all",
        help="Cenario especifico a executar (default: all)"
    )

    args = parser.parse_args()
    logger = setup_logging(args.verbose)

    logger.info("Iniciando validacao de deteccao de mudancas do Observer")
    logger.info(f"Data: {datetime.now().isoformat()}")

    # Criar grafo
    logger.info("\nCriando grafo multi-agente...")
    try:
        graph = create_multi_agent_graph()
        logger.info("Grafo criado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar grafo: {e}")
        sys.exit(1)

    # Selecionar cenarios
    if args.scenario == "all":
        scenarios_to_run = list(SCENARIOS.keys())
    else:
        scenarios_to_run = [args.scenario]

    # Executar cenarios
    results = []
    for scenario_key in scenarios_to_run:
        scenario = SCENARIOS[scenario_key]
        result = execute_scenario(graph, scenario, logger)
        result["validation_passed"] = validate_result(result, logger)
        results.append(result)

    # Gerar relatorio
    generate_report(results, logger)

    # Exit code
    all_passed = all(r.get("validation_passed") for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
