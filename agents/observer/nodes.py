"""
Nós do grafo do agente Observador.

Este módulo implementa os nós que o Observador usa para processar turnos
de conversa e atualizar o CognitiveModel.

No Épico 10.1 (POC), os nós usam heurísticas simples.
No Épico 10.2+, integrarão com LLM para extração real.

Épico 10.1: Mitose do Orquestrador
Data: 05/12/2025
"""

import logging
from typing import Dict, Any, List, Optional
from uuid import uuid4

from .state import ObserverState, create_initial_observer_state
from .metrics import calculate_solidez, calculate_completude

logger = logging.getLogger(__name__)


def process_turn(state: ObserverState) -> Dict[str, Any]:
    """
    Nó principal: processa turno completo e atualiza estado.

    Este nó é chamado pelo Observador para processar cada turno de conversa.
    Ele extrai informações, calcula métricas e retorna o estado atualizado.

    Pipeline (POC com heurísticas):
    1. Extrai claims do input (heurística)
    2. Extrai conceitos do input (heurística)
    3. Identifica contradições (heurística)
    4. Identifica open_questions (heurística)
    5. Calcula métricas (solidez, completude)
    6. Compara com turno anterior para detectar mudanças

    Args:
        state: ObserverState com input e histórico.

    Returns:
        Dict com estado atualizado + flags de novidades.

    Example:
        >>> state = create_initial_observer_state(
        ...     user_input="LLMs aumentam produtividade",
        ...     conversation_history=[]
        ... )
        >>> result = process_turn(state)
        >>> result['extracted_concepts']
        ['LLMs', 'produtividade']

    Notes:
        No Épico 10.1 (POC), usa heurísticas simples baseadas em palavras-chave.
        No Épico 10.2+, usará LLM (Haiku) para extração real.
    """
    logger.info("=== OBSERVADOR: Processando turno ===")
    user_input = state["user_input"]
    history = state["conversation_history"]
    previous_model = state.get("previous_cognitive_model")

    logger.debug(f"Input: {user_input[:100]}...")
    logger.debug(f"Histórico: {len(history)} mensagens")

    # 1. Extrai claims (POC: heurística simples)
    claims = _extract_claims_heuristic(user_input, history)
    logger.info(f"Claims extraídos: {len(claims)}")

    # 2. Extrai conceitos (POC: heurística simples)
    concepts = _extract_concepts_heuristic(user_input)
    logger.info(f"Conceitos extraídos: {len(concepts)} - {concepts[:3]}...")

    # 3. Extrai fundamentos (POC: placeholder)
    fundamentos = _extract_fundamentos_heuristic(user_input, history)
    logger.info(f"Fundamentos extraídos: {len(fundamentos)}")

    # 4. Identifica contradições (POC: heurística)
    contradictions = _detect_contradictions_heuristic(claims, history)
    logger.info(f"Contradições detectadas: {len(contradictions)}")

    # 5. Identifica open_questions (POC: heurística)
    open_questions = _identify_gaps_heuristic(user_input, claims)
    logger.info(f"Questões abertas: {len(open_questions)}")

    # 6. Calcula métricas
    # Criar dados temporários para cálculo
    temp_data = {
        "claim": claims[0] if claims else "",
        "premises": fundamentos,
        "assumptions": [],  # Placeholder
        "open_questions": open_questions,
        "contradictions": contradictions,
        "solid_grounds": [],
    }
    solidez = calculate_solidez(temp_data)
    completude = calculate_completude(temp_data)
    logger.info(f"Métricas: solidez={solidez:.2f}, completude={completude:.2f}")

    # 7. Detectar mudanças significativas
    previous_solidez = 0.0
    if previous_model:
        previous_solidez = previous_model.get("solidez_geral", 0.0)

    solidez_changed = abs(solidez - previous_solidez) > 0.15

    # 8. Construir resultado
    result = {
        # Extração
        "extracted_claims": claims,
        "extracted_concepts": concepts,
        "extracted_fundamentos": fundamentos,
        "extracted_contradictions": contradictions,
        "extracted_open_questions": open_questions,

        # Métricas
        "solidez_calculated": solidez,
        "completude_calculated": completude,

        # Flags
        "has_new_concepts": len(concepts) > 0,
        "has_new_contradictions": len(contradictions) > 0,
        "solidez_changed_significantly": solidez_changed,
    }

    logger.info("=== OBSERVADOR: Turno processado ===")
    return result


def _extract_claims_heuristic(user_input: str, history: List[Dict]) -> List[str]:
    """
    Extrai claims usando heurísticas simples (POC).

    Claims são afirmações centrais que o usuário está fazendo.
    No Épico 10.2+, será feito via LLM.

    Heurísticas aplicadas:
    - Procura padrões de afirmação (verbo + objeto)
    - Identifica frases declarativas (não interrogativas)
    - Limita a 3 claims por turno

    Args:
        user_input: Input atual do usuário.
        history: Histórico da conversa.

    Returns:
        Lista de strings com claims identificados.
    """
    claims = []

    # Heurística 1: Se input é longo e declarativo, considera como claim
    if len(user_input) > 20 and "?" not in user_input:
        # Limpa e adiciona como claim principal
        claim = user_input.strip()
        if len(claim) > 200:
            claim = claim[:200] + "..."
        claims.append(claim)

    # Heurística 2: Procura padrões comuns de afirmação
    patterns = [
        "aumenta", "reduz", "melhora", "piora",
        "é melhor", "é pior", "causa", "permite",
        "depende", "requer", "necessita"
    ]

    input_lower = user_input.lower()
    for pattern in patterns:
        if pattern in input_lower and user_input not in claims:
            claims.append(user_input.strip()[:200])
            break

    return claims[:3]  # Máximo 3 claims


def _extract_concepts_heuristic(user_input: str) -> List[str]:
    """
    Extrai conceitos usando heurísticas simples (POC).

    Conceitos são entidades semânticas reutilizáveis.
    No Épico 10.2+, será feito via LLM + embeddings.

    Heurísticas aplicadas:
    - Procura siglas (palavras em maiúsculas)
    - Procura substantivos capitalizados
    - Procura termos técnicos conhecidos
    - Remove stopwords comuns

    Args:
        user_input: Input atual do usuário.

    Returns:
        Lista de strings com conceitos identificados.
    """
    concepts = []

    # Stopwords para ignorar
    stopwords = {
        "o", "a", "os", "as", "um", "uma", "uns", "umas",
        "de", "da", "do", "das", "dos", "em", "na", "no",
        "para", "por", "com", "sem", "que", "como", "quando",
        "se", "mas", "ou", "e", "eu", "você", "ele", "ela",
        "isso", "isto", "esse", "esta", "aquele", "muito",
        "mais", "menos", "bem", "mal", "aqui", "ali", "onde"
    }

    # Termos técnicos conhecidos (biblioteca base)
    known_terms = {
        "llm", "llms", "ia", "ai", "ml", "tdd", "api", "sdk",
        "produtividade", "qualidade", "métricas", "metodologia",
        "hipótese", "argumento", "evidência", "pesquisa",
        "desenvolvimento", "software", "código", "teste",
        "claude", "gpt", "chatgpt", "copilot"
    }

    # Tokenização simples
    words = user_input.replace(",", " ").replace(".", " ").replace("?", " ").split()

    for word in words:
        word_clean = word.strip().lower()

        # Ignora stopwords
        if word_clean in stopwords:
            continue

        # Heurística 1: Siglas (palavras em maiúsculas) - aceita 2+ caracteres
        if word.isupper() and len(word) >= 2:
            concepts.append(word)
            continue

        # Ignora palavras muito curtas (exceto siglas já processadas acima)
        if len(word_clean) < 3:
            continue

        # Heurística 2: Termos técnicos conhecidos
        if word_clean in known_terms:
            # Preserva siglas (maiúsculas), senão capitaliza
            if word.isupper() or word_clean in {"llm", "llms", "ia", "ai", "ml", "tdd", "api", "sdk"}:
                concepts.append(word.upper() if word_clean in {"llm", "llms", "ia", "ai", "ml", "tdd", "api", "sdk"} else word)
            else:
                concepts.append(word.capitalize())
            continue

        # Heurística 3: Palavras capitalizadas (possíveis nomes/termos)
        if word[0].isupper() and word_clean not in stopwords:
            concepts.append(word)

    # Remove duplicatas preservando ordem
    seen = set()
    unique_concepts = []
    for c in concepts:
        c_lower = c.lower()
        if c_lower not in seen:
            seen.add(c_lower)
            unique_concepts.append(c)

    return unique_concepts[:10]  # Máximo 10 conceitos


def _extract_fundamentos_heuristic(user_input: str, history: List[Dict]) -> List[str]:
    """
    Extrai fundamentos usando heurísticas simples (POC).

    Fundamentos são argumentos de suporte para claims.
    No Épico 10.2+, será feito via LLM.

    Args:
        user_input: Input atual do usuário.
        history: Histórico da conversa.

    Returns:
        Lista de strings com fundamentos identificados.
    """
    fundamentos = []

    # Heurística: Procura padrões de justificativa
    patterns = [
        "porque", "pois", "já que", "uma vez que",
        "dado que", "considerando", "baseado em",
        "segundo", "de acordo com"
    ]

    input_lower = user_input.lower()

    for pattern in patterns:
        if pattern in input_lower:
            # Extrai texto após o padrão como fundamento
            idx = input_lower.find(pattern)
            fundamento = user_input[idx:].strip()
            if len(fundamento) > 10:
                fundamentos.append(fundamento[:150])

    return fundamentos[:5]  # Máximo 5 fundamentos


def _detect_contradictions_heuristic(
    claims: List[str],
    history: List[Dict]
) -> List[Dict[str, Any]]:
    """
    Detecta contradições usando heurísticas simples (POC).

    Contradições são inconsistências entre claims/fundamentos.
    No Épico 10.2+, será feito via LLM.

    Args:
        claims: Claims extraídos do turno atual.
        history: Histórico da conversa.

    Returns:
        Lista de dicts com contradições detectadas.
    """
    # POC: Não detecta contradições automaticamente
    # Requer análise semântica mais sofisticada (LLM)
    return []


def _identify_gaps_heuristic(user_input: str, claims: List[str]) -> List[str]:
    """
    Identifica lacunas/questões abertas usando heurísticas (POC).

    Lacunas são aspectos não explorados do argumento.
    No Épico 10.2+, será feito via LLM.

    Args:
        user_input: Input atual do usuário.
        claims: Claims extraídos.

    Returns:
        Lista de strings com questões abertas.
    """
    open_questions = []

    # Heurística 1: Se usuário fez pergunta, adiciona como questão aberta
    if "?" in user_input:
        # Extrai a pergunta
        parts = user_input.split("?")
        for part in parts[:-1]:  # Ignora última parte (vazia após ?)
            question = part.strip() + "?"
            if len(question) > 5:
                open_questions.append(question)

    # Heurística 2: Padrões de incerteza
    uncertainty_patterns = [
        ("não sei", "O que exatamente você quer descobrir?"),
        ("talvez", "Qual é a hipótese principal?"),
        ("acho que", "O que sustenta essa intuição?"),
        ("pode ser", "Quais são as alternativas?"),
    ]

    input_lower = user_input.lower()
    for pattern, question in uncertainty_patterns:
        if pattern in input_lower:
            open_questions.append(question)

    return open_questions[:5]  # Máximo 5 questões


def update_cognitive_model_from_observation(
    observation_result: Dict[str, Any],
    existing_model: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Atualiza CognitiveModel com resultados da observação.

    Esta função helper converte o resultado do process_turn
    para o formato esperado pelo CognitiveModel.

    Args:
        observation_result: Resultado de process_turn().
        existing_model: CognitiveModel existente (para merge).

    Returns:
        Dict com CognitiveModel atualizado.

    Example:
        >>> result = process_turn(state)
        >>> model = update_cognitive_model_from_observation(result)
        >>> model['solidez_geral']
        0.65
    """
    # Base: modelo existente ou vazio
    if existing_model:
        model = existing_model.copy()
    else:
        model = {
            "claim": "",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {},
            "conceitos": [],
            "solidez_geral": 0.0,
            "completude": 0.0,
        }

    # Atualiza com dados extraídos
    claims = observation_result.get("extracted_claims", [])
    if claims:
        model["claim"] = claims[0]  # Claim principal

    # Merge de conceitos (adiciona novos, não duplica)
    new_concepts = observation_result.get("extracted_concepts", [])
    existing_concepts = set(c.lower() for c in model.get("conceitos", []))
    for concept in new_concepts:
        if concept.lower() not in existing_concepts:
            model["conceitos"].append(concept)
            existing_concepts.add(concept.lower())

    # Merge de open_questions
    new_questions = observation_result.get("extracted_open_questions", [])
    existing_questions = set(model.get("open_questions", []))
    for q in new_questions:
        if q not in existing_questions:
            model["open_questions"].append(q)

    # Atualiza métricas
    model["solidez_geral"] = observation_result.get("solidez_calculated", 0.0)
    model["completude"] = observation_result.get("completude_calculated", 0.0)

    return model
