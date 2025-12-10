#!/usr/bin/env python
"""
Script de validação da integração do Observer (Épico 12).

Este script verifica se todos os componentes do Épico 12 estão funcionando:
1. Callback assíncrono do Observer (12.1)
2. CognitiveModel no prompt do Orquestrador (12.2)
3. Timeline visual do Observer (12.3)

Uso:
    python scripts/validate_observer_integration.py

Saída esperada:
    ✅ Todos os testes passaram!
"""

import sys
import time
import logging
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def validate_imports():
    """Valida que todos os módulos podem ser importados."""
    logger.info("\n📦 Validando imports...")

    errors = []

    # 12.1: Callback do Observer
    try:
        from agents.multi_agent_graph import _create_observer_callback, OBSERVER_AVAILABLE
        logger.info(f"  ✅ _create_observer_callback importado (OBSERVER_AVAILABLE={OBSERVER_AVAILABLE})")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar _create_observer_callback: {e}")

    # 12.2: Contexto do CognitiveModel
    try:
        from agents.orchestrator.nodes import _build_cognitive_model_context
        logger.info("  ✅ _build_cognitive_model_context importado")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar _build_cognitive_model_context: {e}")

    # 12.3: Timeline do Observer
    try:
        from app.components.backstage.timeline import render_observer_section
        logger.info("  ✅ render_observer_section importado")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar render_observer_section: {e}")

    # Observer nodes
    try:
        from agents.observer.nodes import process_turn
        logger.info("  ✅ process_turn (Observer) importado")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar process_turn: {e}")

    # EventBus
    try:
        from utils.event_bus import get_event_bus
        logger.info("  ✅ EventBus importado")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar EventBus: {e}")

    if errors:
        for err in errors:
            logger.error(err)
        return False

    return True

def validate_cognitive_model_context():
    """Valida formatação do cognitive_model no contexto (12.2)."""
    logger.info("\n🧠 Validando contexto do CognitiveModel (12.2)...")

    from agents.orchestrator.nodes import _build_cognitive_model_context

    test_cm = {
        "claim": "LLMs aumentam produtividade em 30%",
        "proposicoes": [
            {"texto": "Estudo X demonstrou ganho significativo", "solidez": 0.85},
            {"texto": "Contexto: empresas de tecnologia", "solidez": 0.60}
        ],
        "concepts_detected": ["LLM", "produtividade", "automação"],
        "contradictions": [
            {"description": "Conflito entre estudos", "confidence": 0.80}
        ],
        "open_questions": [
            "Qual o contexto específico?",
            "Qual a metodologia?"
        ],
        "overall_solidez": 0.72,
        "overall_completude": 0.55
    }

    result = _build_cognitive_model_context(test_cm)

    checks = [
        ("Header presente", "COGNITIVE MODEL DISPONÍVEL" in result),
        ("Claim incluído", "LLMs aumentam produtividade" in result),
        ("Proposição incluída", "Estudo X demonstrou" in result),
        ("Solidez formatada", "solidez: 0.85" in result),
        ("Conceitos incluídos", "LLM" in result),
        ("Contradição incluída", "Conflito entre estudos" in result),
        ("Questão incluída", "Qual o contexto" in result),
        ("Métrica solidez", "72%" in result),
        ("Métrica completude", "55%" in result),
        ("Instruções de uso", "Use este modelo" in result)
    ]

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def validate_context_integration():
    """Valida integração do cognitive_model no _build_context (12.2)."""
    logger.info("\n📝 Validando integração no _build_context (12.2)...")

    from agents.orchestrator.nodes import _build_context
    from agents.orchestrator.state import create_initial_multi_agent_state

    # Criar estado com cognitive_model
    state = create_initial_multi_agent_state(
        user_input="Testar integração",
        session_id="validation-test"
    )
    state["cognitive_model"] = {
        "claim": "Afirmação de teste",
        "proposicoes": [{"texto": "Fundamento", "solidez": 0.7}]
    }

    context = _build_context(state)

    checks = [
        ("Input do usuário presente", "Testar integração" in context),
        ("Seção cognitive_model presente", "COGNITIVE MODEL DISPONÍVEL" in context),
        ("Claim no contexto", "Afirmação de teste" in context)
    ]

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def validate_event_bus_integration():
    """Valida publicação de eventos no EventBus (12.1)."""
    logger.info("\n📡 Validando EventBus (12.1)...")

    from utils.event_bus import get_event_bus

    bus = get_event_bus()
    test_session = f"validation-{time.time()}"

    # Publicar evento
    bus.publish_cognitive_model_updated(
        session_id=test_session,
        turn_number=1,
        solidez=0.65,
        completude=0.45,
        claims_count=1,
        proposicoes_count=2,
        concepts_count=3,
        open_questions_count=1,
        contradictions_count=0,
        is_mature=False,
        metadata={"processing_time_ms": 1000, "observer_version": "12.1"}
    )

    # Recuperar eventos
    events = bus.get_session_events(test_session)
    cm_events = [e for e in events if e.get("event_type") == "cognitive_model_updated"]

    checks = [
        ("Evento publicado", len(cm_events) >= 1),
        ("Session_id correto", cm_events[0].get("session_id") == test_session if cm_events else False),
        ("Turn_number correto", cm_events[0].get("turn_number") == 1 if cm_events else False),
        ("Solidez correta", cm_events[0].get("solidez") == 0.65 if cm_events else False),
        ("Metadata presente", cm_events[0].get("metadata", {}).get("observer_version") == "12.1" if cm_events else False)
    ]

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def validate_observer_callback():
    """Valida callback do Observer (12.1)."""
    logger.info("\n👁️ Validando callback do Observer (12.1)...")

    from agents.multi_agent_graph import _create_observer_callback, OBSERVER_AVAILABLE
    from langchain_core.messages import HumanMessage, AIMessage

    if not OBSERVER_AVAILABLE:
        logger.warning("  ⚠️ Observer não disponível - pulando validação de callback")
        return True

    # Mock state e result
    state = {
        "session_id": f"callback-validation-{time.time()}",
        "user_input": "Testar callback do Observer",
        "turn_count": 1,
        "messages": [HumanMessage(content="Olá")],
        "cognitive_model": None,
        "idea_id": None
    }

    result = {
        "messages": [AIMessage(content="Resposta do orquestrador")],
        "next_step": "explore"
    }

    # Executar callback (não deve lançar exceção)
    try:
        _create_observer_callback(state, result)
        logger.info("  ✅ Callback executado sem exceção")
        logger.info("  ℹ️ Observer processa em background (não bloqueante)")
        return True
    except Exception as e:
        logger.error(f"  ❌ Callback falhou: {e}")
        return False

def validate_timeline_section():
    """Valida seção do Observer na timeline (12.3)."""
    logger.info("\n📊 Validando seção da Timeline (12.3)...")

    # Verificar que a função existe e aceita parâmetros corretos
    from app.components.backstage.timeline import render_observer_section, _show_observer_modal

    # Verificar assinaturas
    import inspect

    # render_observer_section
    sig = inspect.signature(render_observer_section)
    params = list(sig.parameters.keys())

    checks = [
        ("render_observer_section existe", callable(render_observer_section)),
        ("Parâmetro observer_events", "observer_events" in params),
        ("_show_observer_modal existe", callable(_show_observer_modal))
    ]

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def run_unit_tests():
    """Executa testes unitários relacionados ao Épico 12."""
    logger.info("\n🧪 Executando testes unitários...")

    import subprocess

    test_files = [
        "tests/unit/agents/orchestrator/test_cognitive_context.py",
        "tests/unit/test_observer_callback.py"
    ]

    all_passed = True
    for test_file in test_files:
        if Path(test_file).exists():
            result = subprocess.run(
                ["python", "-m", "pytest", test_file, "-v", "--tb=short"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info(f"  ✅ {test_file}")
            else:
                logger.error(f"  ❌ {test_file}")
                logger.error(f"     {result.stdout[-500:] if result.stdout else result.stderr[-500:]}")
                all_passed = False
        else:
            logger.warning(f"  ⚠️ {test_file} não encontrado")

    return all_passed

def main():
    """Executa todas as validações."""
    logger.info("=" * 60)
    logger.info("🔍 VALIDAÇÃO DO ÉPICO 12 - Observer Integração Básica (MVP)")
    logger.info("=" * 60)

    results = {
        "imports": validate_imports(),
        "cognitive_model_context": validate_cognitive_model_context(),
        "context_integration": validate_context_integration(),
        "event_bus": validate_event_bus_integration(),
        "observer_callback": validate_observer_callback(),
        "timeline_section": validate_timeline_section()
    }

    # Resumo
    logger.info("\n" + "=" * 60)
    logger.info("📋 RESUMO DA VALIDAÇÃO")
    logger.info("=" * 60)

    passed = sum(results.values())
    total = len(results)

    for name, result in results.items():
        status = "✅" if result else "❌"
        logger.info(f"  {status} {name}")

    logger.info("")

    if passed == total:
        logger.info(f"🎉 SUCESSO: Todos os {total} testes passaram!")
        logger.info("")
        logger.info("Épico 12 está pronto para uso:")
        logger.info("  - 12.1: Callback assíncrono do Observer ✅")
        logger.info("  - 12.2: CognitiveModel no prompt do Orquestrador ✅")
        logger.info("  - 12.3: Timeline visual do Observer ✅")
        return 0
    else:
        logger.error(f"⚠️ FALHA: {total - passed} de {total} testes falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())
