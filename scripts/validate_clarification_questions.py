#!/usr/bin/env python
"""
Script de validação das Consultas Inteligentes (Épico 14).

Este script verifica se todos os componentes do Épico 14 estão funcionando:
1. Identificação de necessidades de esclarecimento (14.1)
2. Geração de perguntas sobre contradições (14.3)
3. Sugestão de perguntas sobre gaps (14.4)
4. Decisão de timing de intervenção (14.5)
5. Análise de resposta de esclarecimento (14.6)

Uso:
    python scripts/validate_clarification_questions.py

Saída esperada:
    ✅ Todos os testes passaram!

Nota:
    Este script requer dependências do projeto. Para executar em ambiente limpo,
    instale as dependências primeiro: pip install -r requirements.txt
"""

import sys
import time
import logging
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Flag para verificar se dependências estão disponíveis
DEPS_AVAILABLE = True
try:
    from unittest.mock import patch, MagicMock
    import pydantic
except ImportError:
    DEPS_AVAILABLE = False
    logger.warning("⚠️ Dependências não disponíveis. Executando validação estrutural apenas.")

def validate_imports():
    """Valida que todos os módulos podem ser importados."""
    logger.info("\n📦 Validando imports...")

    errors = []

    # Funções de clarification
    try:
        from agents.observer.clarification import (
            identify_clarification_needs,
            generate_contradiction_question,
            suggest_question_for_gap,
            should_ask_clarification,
            analyze_clarification_response,
            update_clarification_persistence,
            get_clarification_summary_for_timeline
        )
        logger.info("  ✅ Funções de clarification importadas")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar funções de clarification: {e}")

    # Modelos Pydantic
    try:
        from agents.models.clarification import (
            ClarificationNeed,
            ClarificationContext,
            ClarificationTimingDecision,
            ClarificationResponse,
            ClarificationUpdates,
            QuestionSuggestion
        )
        logger.info("  ✅ Modelos Pydantic de clarification importados")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar modelos de clarification: {e}")

    # Eventos
    try:
        from core.utils.event_models import (
            ClarificationRequestedEvent,
            ClarificationResolvedEvent
        )
        logger.info("  ✅ Eventos de clarification importados")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar eventos de clarification: {e}")

    # Prompts
    try:
        from agents.observer.clarification_prompts import (
            IDENTIFY_CLARIFICATION_NEEDS_PROMPT,
            CONTRADICTION_QUESTION_PROMPT,
            GAP_QUESTION_PROMPT,
            ANALYZE_CLARIFICATION_RESPONSE_PROMPT
        )
        logger.info("  ✅ Prompts de clarification importados")
    except ImportError as e:
        errors.append(f"  ❌ Falha ao importar prompts de clarification: {e}")

    if errors:
        for err in errors:
            logger.error(err)
        return False

    return True

def validate_models():
    """Valida criação e serialização dos modelos Pydantic."""
    logger.info("\n📋 Validando modelos Pydantic...")

    from agents.models.clarification import (
        ClarificationNeed,
        ClarificationContext,
        ClarificationTimingDecision,
        ClarificationResponse,
        ClarificationUpdates,
        QuestionSuggestion
    )

    errors = []

    # ClarificationNeed
    try:
        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Tensão entre proposições X e Y",
            suggested_approach="Explorar contextos diferentes",
            priority="high",
            turn_detected=5,
            turns_persisted=2
        )
        assert need.id is not None  # UUID gerado
        assert need.needs_clarification is True
        assert need.priority == "high"

        # Testar serialização
        data = need.to_dict()
        need_restored = ClarificationNeed.from_dict(data)
        assert need_restored.clarification_type == "contradiction"
        logger.info("  ✅ ClarificationNeed: criação e serialização OK")
    except Exception as e:
        errors.append(f"  ❌ ClarificationNeed: {e}")

    # ClarificationContext
    try:
        context = ClarificationContext(
            proposicoes=["LLMs aumentam produtividade", "LLMs aumentam bugs"],
            contradictions=["Produtividade vs bugs"],
            open_questions=["Em que contexto?"],
            claim_excerpt="LLMs impactam desenvolvimento"
        )
        assert len(context.proposicoes) == 2
        logger.info("  ✅ ClarificationContext: criação OK")
    except Exception as e:
        errors.append(f"  ❌ ClarificationContext: {e}")

    # ClarificationTimingDecision
    try:
        decision = ClarificationTimingDecision(
            should_ask=True,
            reason="Contradição persiste há 3 turnos",
            delay_turns=0,
            urgency="high"
        )
        assert decision.should_ask is True
        logger.info("  ✅ ClarificationTimingDecision: criação OK")
    except Exception as e:
        errors.append(f"  ❌ ClarificationTimingDecision: {e}")

    # ClarificationResponse
    try:
        updates = ClarificationUpdates(
            proposicoes_to_add=["Nova proposição"],
            contradictions_to_resolve=[0],
            open_questions_to_close=[1]
        )
        response = ClarificationResponse(
            resolution_status="resolved",
            summary="Usuário esclareceu os contextos",
            updates=updates,
            needs_followup=False
        )
        assert response.resolution_status == "resolved"
        logger.info("  ✅ ClarificationResponse: criação OK")
    except Exception as e:
        errors.append(f"  ❌ ClarificationResponse: {e}")

    # QuestionSuggestion
    try:
        suggestion = QuestionSuggestion(
            question_text="Você mencionou X e Y. Eles se aplicam em situações diferentes?",
            target_type="contradiction",
            related_proposicoes=["X", "Y"],
            expected_outcome="Esclarecimento do contexto",
            tone_guidance="Curiosidade genuína"
        )
        assert suggestion.target_type == "contradiction"
        logger.info("  ✅ QuestionSuggestion: criação OK")
    except Exception as e:
        errors.append(f"  ❌ QuestionSuggestion: {e}")

    if errors:
        for err in errors:
            logger.error(err)
        return False

    return True

def validate_timing_logic():
    """Valida lógica de timing de intervenção (14.5)."""
    logger.info("\n⏱️ Validando lógica de timing (14.5)...")

    from agents.observer.clarification import should_ask_clarification
    from agents.models.clarification import ClarificationNeed

    checks = []

    # Cenário 1: Sem necessidade de esclarecimento
    need_none = ClarificationNeed(
        needs_clarification=False,
        clarification_type="confusion",
        description="Conversa fluindo bem"
    )
    decision = should_ask_clarification(need_none, [], current_turn=5)
    checks.append(("Sem necessidade → não perguntar", decision.should_ask is False))

    # Cenário 2: Prioridade alta sempre pergunta
    need_high = ClarificationNeed(
        needs_clarification=True,
        clarification_type="contradiction",
        description="Contradição crítica",
        suggested_approach="Perguntar",
        priority="high"
    )
    decision = should_ask_clarification(need_high, [], current_turn=5, turns_since_last_question=3)
    checks.append(("Prioridade alta → perguntar", decision.should_ask is True))
    checks.append(("Prioridade alta → urgência high", decision.urgency == "high"))

    # Cenário 3: Contradição persistente (2+ turnos)
    need_persist = ClarificationNeed(
        needs_clarification=True,
        clarification_type="contradiction",
        description="Contradição entre X e Y",
        suggested_approach="Explorar",
        priority="medium",
        turns_persisted=3
    )
    decision = should_ask_clarification(need_persist, [], current_turn=5, turns_since_last_question=5)
    checks.append(("Contradição persistente → perguntar", decision.should_ask is True))

    # Cenário 4: Pergunta recente - deve esperar
    need_recent = ClarificationNeed(
        needs_clarification=True,
        clarification_type="gap",
        description="Gap",
        suggested_approach="Perguntar",
        priority="medium"
    )
    decision = should_ask_clarification(need_recent, [], current_turn=5, turns_since_last_question=1)
    checks.append(("Pergunta recente → esperar", decision.should_ask is False))
    checks.append(("Pergunta recente → delay > 0", decision.delay_turns > 0))

    # Cenário 5: Usuário fluindo bem - não interromper
    need_flow = ClarificationNeed(
        needs_clarification=True,
        clarification_type="gap",
        description="Gap menor",
        suggested_approach="Eventualmente",
        priority="low",
        turns_persisted=1
    )
    decision = should_ask_clarification(
        need_flow, [], current_turn=5,
        turns_since_last_question=5, is_user_flowing=True
    )
    checks.append(("Usuário fluindo → não interromper", decision.should_ask is False))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def validate_persistence_update():
    """Valida atualização de persistência de necessidade (14.5)."""
    logger.info("\n🔄 Validando atualização de persistência...")

    from agents.observer.clarification import update_clarification_persistence
    from agents.models.clarification import ClarificationNeed

    checks = []

    # Incrementar persistência
    need = ClarificationNeed(
        needs_clarification=True,
        clarification_type="contradiction",
        description="Contradição",
        suggested_approach="Perguntar",
        turns_persisted=2
    )
    updated = update_clarification_persistence(need, still_relevant=True)
    checks.append(("Incrementar persistência", updated.turns_persisted == 3))

    # Resetar quando não relevante
    need2 = ClarificationNeed(
        needs_clarification=True,
        clarification_type="contradiction",
        description="Contradição",
        suggested_approach="Perguntar",
        turns_persisted=5
    )
    updated2 = update_clarification_persistence(need2, still_relevant=False)
    checks.append(("Reset quando não relevante", updated2.turns_persisted == 0))
    checks.append(("Marcar como não necessário", updated2.needs_clarification is False))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def validate_timeline_summary():
    """Valida geração de resumo para timeline (14.6)."""
    logger.info("\n📜 Validando resumo para timeline...")

    from agents.observer.clarification import get_clarification_summary_for_timeline
    from agents.models.clarification import ClarificationResponse, ClarificationUpdates

    checks = []

    # Esclarecimento resolvido
    response_resolved = ClarificationResponse(
        resolution_status="resolved",
        summary="Usuário explicou os contextos diferentes",
        updates=ClarificationUpdates(),
        needs_followup=False
    )
    summary = get_clarification_summary_for_timeline(response_resolved, "contradiction")
    checks.append(("Resolved → emoji ✅", "✅" in summary))
    checks.append(("Resolved → 'esclarecida'", "esclarecida" in summary.lower()))

    # Parcialmente resolvido
    response_partial = ClarificationResponse(
        resolution_status="partially_resolved",
        summary="Algumas dúvidas permanecem",
        updates=ClarificationUpdates(),
        needs_followup=True
    )
    summary = get_clarification_summary_for_timeline(response_partial, "gap")
    checks.append(("Partial → 'parcialmente'", "parcialmente" in summary.lower()))

    # Não resolvido
    response_unresolved = ClarificationResponse(
        resolution_status="unresolved",
        summary="Resposta tangencial",
        updates=ClarificationUpdates(),
        needs_followup=False
    )
    summary = get_clarification_summary_for_timeline(response_unresolved, "confusion")
    checks.append(("Unresolved → 'pendente'", "pendente" in summary.lower()))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def validate_events():
    """Valida criação de eventos de clarification."""
    logger.info("\n📡 Validando eventos de clarification...")

    from core.utils.event_models import ClarificationRequestedEvent, ClarificationResolvedEvent

    checks = []

    # ClarificationRequestedEvent
    try:
        event_req = ClarificationRequestedEvent(
            session_id="test-session",
            turn_number=5,
            clarification_type="contradiction",
            question="Você mencionou X e Y. Eles se aplicam em contextos diferentes?",
            priority="medium",
            related_context={"proposicoes": ["X", "Y"]}
        )
        checks.append(("ClarificationRequestedEvent criado", True))
        checks.append(("event_type correto", event_req.event_type == "clarification_requested"))
        checks.append(("turn_number correto", event_req.turn_number == 5))
    except Exception as e:
        checks.append((f"ClarificationRequestedEvent: {e}", False))

    # ClarificationResolvedEvent
    try:
        event_res = ClarificationResolvedEvent(
            session_id="test-session",
            turn_number=6,
            clarification_type="contradiction",
            resolution_status="resolved",
            summary="Usuário esclareceu os contextos",
            updates_made={"contradictions_resolved": 1}
        )
        checks.append(("ClarificationResolvedEvent criado", True))
        checks.append(("event_type correto", event_res.event_type == "clarification_resolved"))
        checks.append(("resolution_status correto", event_res.resolution_status == "resolved"))
    except Exception as e:
        checks.append((f"ClarificationResolvedEvent: {e}", False))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

@patch('agents.observer.clarification.invoke_with_retry')
@patch('agents.observer.clarification._get_llm')
def validate_identify_needs_with_mock(mock_get_llm, mock_invoke):
    """Valida identify_clarification_needs com mock do LLM (14.1)."""
    logger.info("\n🔍 Validando identificação de necessidades com mock (14.1)...")

    from agents.observer.clarification import identify_clarification_needs

    checks = []

    # Mock da resposta do LLM para contradição
    mock_response = MagicMock()
    mock_response.content = '''```json
    {
        "needs_clarification": true,
        "clarification_type": "contradiction",
        "description": "Usuário disse X e Y que parecem contraditórios",
        "relevant_context": {
            "proposicoes": ["X", "Y"],
            "contradictions": ["X vs Y"]
        },
        "suggested_approach": "Explorar contextos diferentes",
        "priority": "high"
    }
    ```'''
    mock_invoke.return_value = mock_response

    cognitive_model = {
        "claim": "LLMs impactam desenvolvimento",
        "proposicoes": [
            {"texto": "LLMs aumentam produtividade", "solidez": 0.7},
            {"texto": "LLMs aumentam bugs", "solidez": 0.6}
        ],
        "contradictions": [{"description": "Produtividade vs bugs", "confidence": 0.85}],
        "open_questions": []
    }

    need = identify_clarification_needs(cognitive_model, turn_number=5)

    checks.append(("Retorna ClarificationNeed", hasattr(need, 'needs_clarification')))
    checks.append(("needs_clarification=True", need.needs_clarification is True))
    checks.append(("clarification_type=contradiction", need.clarification_type == "contradiction"))
    checks.append(("priority=high", need.priority == "high"))
    checks.append(("turn_detected=5", need.turn_detected == 5))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

@patch('agents.observer.clarification.invoke_with_retry')
@patch('agents.observer.clarification._get_llm')
def validate_contradiction_question_with_mock(mock_get_llm, mock_invoke):
    """Valida generate_contradiction_question com mock do LLM (14.3)."""
    logger.info("\n❓ Validando geração de pergunta sobre contradição com mock (14.3)...")

    from agents.observer.clarification import generate_contradiction_question

    checks = []

    # Mock da resposta do LLM
    mock_response = MagicMock()
    mock_response.content = '''```json
    {
        "question": "Você mencionou que LLMs aumentam produtividade e também aumentam bugs. Esses efeitos acontecem em contextos diferentes?",
        "expected_outcomes": [
            "Esclarecimento sobre contextos específicos",
            "Diferenciação de cenários"
        ],
        "tone_check": "Curiosidade genuína, sem julgamento"
    }
    ```'''
    mock_invoke.return_value = mock_response

    contradiction = {
        "description": "LLMs aumentam produtividade vs LLMs aumentam bugs",
        "confidence": 0.85
    }
    propositions = [
        {"texto": "LLMs aumentam produtividade em 30%", "solidez": 0.7},
        {"texto": "LLMs aumentam quantidade de bugs", "solidez": 0.6}
    ]
    context = "Usuário está desenvolvendo argumento sobre impacto de LLMs"

    suggestion = generate_contradiction_question(contradiction, propositions, context)

    checks.append(("Retorna QuestionSuggestion", hasattr(suggestion, 'question_text')))
    checks.append(("question_text não vazio", len(suggestion.question_text) > 0))
    checks.append(("target_type=contradiction", suggestion.target_type == "contradiction"))
    checks.append(("tone_guidance presente", len(suggestion.tone_guidance) > 0))

    # Validar que pergunta é contextual (menciona conceitos da conversa)
    question_lower = suggestion.question_text.lower()
    is_contextual = "produtividade" in question_lower or "bugs" in question_lower or "llm" in question_lower
    checks.append(("Pergunta é contextual", is_contextual))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

@patch('agents.observer.clarification.invoke_with_retry')
@patch('agents.observer.clarification._get_llm')
def validate_gap_question_with_mock(mock_get_llm, mock_invoke):
    """Valida suggest_question_for_gap com mock do LLM (14.4)."""
    logger.info("\n🕳️ Validando sugestão de pergunta sobre gap com mock (14.4)...")

    from agents.observer.clarification import suggest_question_for_gap

    checks = []

    # Mock da resposta do LLM
    mock_response = MagicMock()
    mock_response.content = '''```json
    {
        "question": "Você tem algum dado ou experiência que demonstre esse aumento de produtividade?",
        "connection_to_claim": "Evidência empírica fortaleceria o argumento central"
    }
    ```'''
    mock_invoke.return_value = mock_response

    cognitive_model = {
        "claim": "LLMs aumentam produtividade em 30%",
        "proposicoes": [{"texto": "Equipes de tech usam LLMs", "solidez": 0.6}],
        "open_questions": [
            "Qual baseline de comparação?",
            "Qual a metodologia de medição?"
        ],
        "contradictions": []
    }

    suggestion = suggest_question_for_gap(cognitive_model, gap_index=0, conversation_context="Discussão sobre impacto de LLMs")

    checks.append(("Retorna QuestionSuggestion", suggestion is not None))
    if suggestion:
        checks.append(("question_text não vazio", len(suggestion.question_text) > 0))
        checks.append(("target_type=gap", suggestion.target_type == "gap"))
        checks.append(("expected_outcome presente", len(suggestion.expected_outcome) > 0))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

@patch('agents.observer.clarification.invoke_with_retry')
@patch('agents.observer.clarification._get_llm')
def validate_analyze_response_with_mock(mock_get_llm, mock_invoke):
    """Valida analyze_clarification_response com mock do LLM (14.6)."""
    logger.info("\n📊 Validando análise de resposta com mock (14.6)...")

    from agents.observer.clarification import analyze_clarification_response
    from agents.models.clarification import ClarificationNeed

    checks = []

    # Mock da resposta do LLM
    mock_response = MagicMock()
    mock_response.content = '''```json
    {
        "resolution_status": "resolved",
        "summary": "Usuário esclareceu que produtividade aumenta em tarefas simples enquanto bugs aumentam em tarefas complexas",
        "updates": {
            "proposicoes_to_add": ["Produtividade aumenta em tarefas simples", "Bugs aumentam em tarefas complexas"],
            "contradictions_to_resolve": [0],
            "context_to_add": {"task_complexity": "fator diferenciador"}
        },
        "needs_followup": false
    }
    ```'''
    mock_invoke.return_value = mock_response

    original_need = ClarificationNeed(
        needs_clarification=True,
        clarification_type="contradiction",
        description="Produtividade vs bugs"
    )

    cognitive_model = {
        "claim": "LLMs impactam desenvolvimento",
        "proposicoes": [],
        "contradictions": [{"description": "Produtividade vs bugs"}],
        "open_questions": []
    }

    response = analyze_clarification_response(
        user_response="Na verdade, produtividade aumenta em tarefas simples, mas bugs aumentam quando a tarefa é complexa",
        question_asked="Esses efeitos acontecem em contextos diferentes?",
        original_need=original_need,
        cognitive_model=cognitive_model
    )

    checks.append(("Retorna ClarificationResponse", hasattr(response, 'resolution_status')))
    checks.append(("resolution_status=resolved", response.resolution_status == "resolved"))
    checks.append(("summary não vazio", len(response.summary) > 0))
    checks.append(("updates presente", response.updates is not None))
    checks.append(("needs_followup=False", response.needs_followup is False))

    # Verificar updates
    if response.updates:
        checks.append(("proposicoes_to_add populado", len(response.updates.proposicoes_to_add) > 0))
        checks.append(("contradictions_to_resolve populado", len(response.updates.contradictions_to_resolve) > 0))

    all_passed = True
    for name, passed in checks:
        if passed:
            logger.info(f"  ✅ {name}")
        else:
            logger.error(f"  ❌ {name}")
            all_passed = False

    return all_passed

def run_unit_tests():
    """Executa testes unitários relacionados ao Épico 14."""
    logger.info("\n🧪 Executando testes unitários...")

    import subprocess

    test_file = "tests/unit/test_clarification.py"

    if Path(test_file).exists():
        result = subprocess.run(
            ["python", "-m", "pytest", test_file, "-v", "--tb=short", "-q"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # Contar testes passados
            output = result.stdout
            logger.info(f"  ✅ {test_file}")
            # Extrair resumo
            for line in output.split('\n'):
                if 'passed' in line:
                    logger.info(f"     {line.strip()}")
            return True
        else:
            logger.error(f"  ❌ {test_file}")
            logger.error(f"     {result.stdout[-500:] if result.stdout else result.stderr[-500:]}")
            return False
    else:
        logger.warning(f"  ⚠️ {test_file} não encontrado")
        return True  # Não falhar se arquivo não existe

def validate_file_structure():
    """Valida que todos os arquivos necessários existem."""
    logger.info("\n📁 Validando estrutura de arquivos...")

    required_files = [
        "agents/observer/clarification.py",
        "agents/observer/clarification_prompts.py",
        "agents/models/clarification.py",
        "utils/event_models.py",
        "tests/unit/test_clarification.py",
        "app/components/backstage/timeline.py"  # Timeline com seção de clarification
    ]

    base_path = Path(__file__).parent.parent
    all_exist = True

    for file in required_files:
        path = base_path / file
        if path.exists():
            logger.info(f"  ✅ {file}")
        else:
            logger.error(f"  ❌ {file} não encontrado")
            all_exist = False

    return all_exist

def main():
    """Executa todas as validações."""
    logger.info("=" * 60)
    logger.info("🔍 VALIDAÇÃO DO ÉPICO 14 - Observer Consultas Inteligentes")
    logger.info("=" * 60)

    # Sempre validar estrutura de arquivos
    results = {
        "file_structure": validate_file_structure()
    }

    # Se dependências estão disponíveis, executar validações completas
    if DEPS_AVAILABLE:
        results.update({
            "imports": validate_imports(),
            "models": validate_models(),
            "timing_logic": validate_timing_logic(),
            "persistence_update": validate_persistence_update(),
            "timeline_summary": validate_timeline_summary(),
            "events": validate_events(),
            "identify_needs_mock": validate_identify_needs_with_mock(),
            "contradiction_question_mock": validate_contradiction_question_with_mock(),
            "gap_question_mock": validate_gap_question_with_mock(),
            "analyze_response_mock": validate_analyze_response_with_mock(),
            "unit_tests": run_unit_tests()
        })
    else:
        logger.info("\n⚠️ Validação estrutural apenas (dependências não disponíveis)")
        logger.info("   Para validação completa, instale: pip install -r requirements.txt")

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
        if DEPS_AVAILABLE:
            logger.info("Épico 14 - Componentes validados:")
            logger.info("  - 14.1: Identificação de necessidades ✅")
            logger.info("  - 14.3: Perguntas sobre contradições ✅")
            logger.info("  - 14.4: Perguntas sobre gaps ✅")
            logger.info("  - 14.5: Timing de intervenção ✅")
            logger.info("  - 14.6: Análise de resposta ✅")
            logger.info("")
            logger.info("⚠️ Pendente (depende do Épico 13):")
            logger.info("  - 14.2: Integração com Orquestrador")
        else:
            logger.info("Épico 14 - Estrutura validada:")
            logger.info("  - Todos os arquivos necessários existem ✅")
        return 0
    else:
        logger.error(f"⚠️ FALHA: {total - passed} de {total} testes falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())
