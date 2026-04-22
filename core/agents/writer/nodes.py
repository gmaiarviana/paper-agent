"""
Nó Writer (C-ENSAIO-2.1 + 2.4).

Writer simples em uma passada:
- Recebe dict com messages, focal_argument, previous_article, product_context
- Retorna dict com chave `article` contendo markdown completo

Contratos (ver docs/ROADMAP.md :: C-ENSAIO-2.1):
- messages: list de mensagens LangChain (HumanMessage/AIMessage) representando a conversa
- focal_argument: dict com intent/subject/population/metrics/article_type (ou None)
- previous_article: str com artigo anterior (ou None para primeira geração)
- product_context: str com foco do produto consumidor (ou None) - permite produto do core-agnostic

Saída: {"article": str_markdown}

Não mantém estado entre invocações. Não tem loop interno de refinamento.
Refinamento é pilotado pelo app consumidor, que acumula messages e passa previous_article.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from langchain_core.messages import HumanMessage

from core.agents.memory.config_loader import (
    ConfigLoadError,
    get_agent_model,
    get_agent_prompt,
)
from core.prompts import WRITER_PROMPT_V1
from core.utils.config import create_anthropic_client, get_anthropic_model
from core.utils.token_extractor import extract_tokens_and_cost

logger = logging.getLogger(__name__)


def _format_messages_for_prompt(messages: List[Any]) -> str:
    """
    Formata o histórico de mensagens LangChain como texto legível para o prompt.

    Preserva o conteúdo bruto (incluindo code fences e tabelas markdown).
    Retorna string vazia quando não há mensagens.
    """
    if not messages:
        return "(Nenhuma conversa prévia fornecida.)"

    rendered: List[str] = []
    for msg in messages:
        msg_type = msg.__class__.__name__ if hasattr(msg, "__class__") else "Unknown"
        content = getattr(msg, "content", None)
        if content is None:
            continue
        if msg_type == "HumanMessage":
            role = "Pesquisador"
        elif msg_type == "AIMessage":
            role = "Sistema"
        else:
            role = msg_type
        rendered.append(f"[{role}]\n{content}")

    return "\n\n".join(rendered)


def _format_focal_argument(focal_argument: Optional[Dict[str, Any]]) -> str:
    """Formata o argumento focal como JSON legível; indica ausência quando None/vazio."""
    if not focal_argument:
        return "(Argumento focal não foi definido durante a conversa - use defaults da IMRaD e infira o que puder.)"
    return json.dumps(focal_argument, ensure_ascii=False, indent=2)


def _build_user_prompt(
    messages: List[Any],
    focal_argument: Optional[Dict[str, Any]],
    previous_article: Optional[str],
    product_context: Optional[str],
) -> str:
    """Monta o bloco de contexto que acompanha o system prompt do Writer."""
    parts: List[str] = []

    if product_context and product_context.strip():
        parts.append("## CONTEXTO DO PRODUTO")
        parts.append(product_context.strip())
        parts.append("")

    parts.append("## ARGUMENTO FOCAL")
    parts.append(_format_focal_argument(focal_argument))
    parts.append("")

    parts.append("## HISTÓRICO DA CONVERSA")
    parts.append(_format_messages_for_prompt(messages))
    parts.append("")

    if previous_article and previous_article.strip():
        parts.append("## ARTIGO ANTERIOR (para refinamento)")
        parts.append(
            "Regenere o artigo INTEIRO incorporando o feedback mais recente presente no histórico. "
            "Não edite pontualmente; produza uma nova versão completa e coerente."
        )
        parts.append("")
        parts.append(previous_article.strip())
        parts.append("")

    parts.append("## TAREFA")
    parts.append(
        "Produza o artigo completo em markdown. "
        "Retorne APENAS o markdown do artigo (sem code fences externos, sem comentários, sem JSON)."
    )
    return "\n".join(parts)


def writer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera (ou regenera) um artigo em markdown.

    Args:
        state: Dict com as chaves:
            - messages: list de mensagens LangChain (obrigatório; pode ser vazia)
            - focal_argument: dict ou None
            - previous_article: str ou None (primeira geração quando None)
            - product_context: str ou None (injeção de contexto de produto)

    Returns:
        Dict com:
            - article: str com markdown do artigo
            - last_agent_tokens_input, last_agent_tokens_output, last_agent_cost:
              métricas consistentes com os demais nós do core.

    Raises:
        TypeError: Se `state` não for dict.
    """
    if not isinstance(state, dict):
        raise TypeError(
            f"writer_node espera um dict como entrada, recebeu {type(state).__name__}"
        )

    messages = state.get("messages") or []
    focal_argument = state.get("focal_argument")
    previous_article = state.get("previous_article")
    product_context = state.get("product_context")

    # Prompt oficial vive em código (core/prompts/writer.py).
    # O YAML carrega apenas o modelo e a descrição curta (referência).
    system_prompt = WRITER_PROMPT_V1
    try:
        model_name = get_agent_model("writer")
        # Validar que YAML carrega (também valida schema); prompt referência não é usado.
        _ = get_agent_prompt("writer")
        logger.info("Writer: config YAML carregado (modelo=%s)", model_name)
    except ConfigLoadError as exc:
        logger.warning("Writer: falha ao carregar YAML (%s). Usando modelo padrão.", exc)
        model_name = get_anthropic_model()

    user_prompt = _build_user_prompt(
        messages=messages,
        focal_argument=focal_argument,
        previous_article=previous_article,
        product_context=product_context,
    )

    full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

    logger.info(
        "Writer invocado (messages=%d, has_focal=%s, has_previous_article=%s, has_product_context=%s)",
        len(messages),
        focal_argument is not None,
        bool(previous_article),
        bool(product_context),
    )

    llm = create_anthropic_client(model=model_name, temperature=0)
    response = llm.invoke([HumanMessage(content=full_prompt)])

    article = getattr(response, "content", None)
    if not isinstance(article, str) or not article.strip():
        logger.warning("Writer: resposta do LLM vazia ou inválida; retornando placeholder.")
        article = "# Artigo\n\n(Não foi possível gerar o artigo nesta invocação.)"

    # Métricas (consistentes com structurer_node / orchestrator_node).
    try:
        metrics = extract_tokens_and_cost(response, model_name)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Writer: falha ao extrair métricas (%s); usando zeros.", exc)
        metrics = {"tokens_input": 0, "tokens_output": 0, "tokens_total": 0, "cost": 0.0}

    return {
        "article": article,
        "last_agent_tokens_input": metrics.get("tokens_input", 0),
        "last_agent_tokens_output": metrics.get("tokens_output", 0),
        "last_agent_cost": metrics.get("cost", 0.0),
    }
