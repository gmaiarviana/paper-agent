"""Nó do agente Escritor (C-ENSAIO-2).

O Writer é um nó simples, isolado, que recebe contexto conversacional e
devolve markdown de um artigo técnico-científico em uma única passada.

Contrato:
    Input (dict, passado como state):
        - messages:          list de BaseMessage (LangChain) — histórico conversacional
        - focal_argument:    dict ou None — output estruturado do Estruturador
        - previous_article:  str ou None — artigo anterior (modo refinamento)
        - product_context:   str ou None — foco/domínio do produto consumidor
    Output (dict):
        - article: str — markdown do artigo gerado

O nó NÃO mantém estado entre invocações e NÃO tem loop interno de refinamento;
o refinamento vira loop externo orquestrado pelo produto (nova invocação com
`previous_article` preenchido).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from langchain_core.messages import BaseMessage, HumanMessage

from core.agents.memory.config_loader import (
    ConfigLoadError,
    get_agent_model,
    get_agent_prompt,
)
from core.prompts import WRITER_PROMPT_V1
from core.utils.config import create_anthropic_client, get_anthropic_model

logger = logging.getLogger(__name__)


def _format_messages(messages: Optional[list]) -> str:
    if not messages:
        return "(nenhuma mensagem na conversa ainda)"

    lines = []
    for msg in messages:
        if isinstance(msg, BaseMessage):
            role = getattr(msg, "type", "message")
            content = msg.content or ""
        elif isinstance(msg, dict):
            role = msg.get("role") or msg.get("type") or "message"
            content = msg.get("content", "")
        else:
            role = "message"
            content = str(msg)
        lines.append(f"[{role}]\n{content}")
    return "\n\n".join(lines)


def _format_focal_argument(focal_argument: Optional[Dict[str, Any]]) -> str:
    if not focal_argument:
        return ""

    rendered = []
    for key in ("intent", "subject", "population", "metrics", "article_type"):
        value = focal_argument.get(key)
        if value and value not in ("not specified", "unclear"):
            rendered.append(f"- **{key}**: {value}")

    if not rendered:
        return ""

    body = "\n".join(rendered)
    return (
        "## ARGUMENTO FOCAL (do Estruturador)\n\n"
        f"{body}\n\n---\n"
    )


def _format_previous_article(previous_article: Optional[str]) -> str:
    if not previous_article:
        return ""
    return (
        "## ARTIGO ANTERIOR (modo refinamento)\n\n"
        "Este é o artigo gerado na passada anterior. O histórico conversacional\n"
        "mais recente contém o feedback do pesquisador. Regenere o artigo inteiro\n"
        "incorporando o feedback.\n\n"
        "```markdown\n"
        f"{previous_article}\n"
        "```\n\n---\n"
    )


def _format_product_context(product_context: Optional[str]) -> str:
    if not product_context or not product_context.strip():
        return ""
    return (
        "## CONTEXTO DO PRODUTO\n\n"
        f"{product_context.strip()}\n\n---\n"
    )


def _format_conversation(messages: Optional[list]) -> str:
    return (
        "## HISTÓRICO DA CONVERSA\n\n"
        f"{_format_messages(messages)}\n"
    )


def _load_model_name() -> str:
    try:
        return get_agent_model("writer")
    except ConfigLoadError:
        logger.warning(
            "Config YAML do writer não encontrada — usando modelo padrão do sistema."
        )
        return get_anthropic_model()


def _load_system_prompt() -> str:
    try:
        prompt = get_agent_prompt("writer")
        if "{product_context_section}" in prompt:
            return prompt
    except ConfigLoadError:
        logger.warning("Config YAML do writer não encontrada — usando WRITER_PROMPT_V1.")
    return WRITER_PROMPT_V1


def writer_node(
    state: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Gera um artigo em markdown a partir do contexto conversacional.

    Args:
        state: dict com as chaves ``messages``, ``focal_argument``,
            ``previous_article``, ``product_context``. Chaves ausentes são
            tratadas como None.
        config: ignorado na V1 (presente apenas para compatibilidade com a
            assinatura de nós LangGraph). ``product_context`` via
            ``config.configurable`` é aceito como fallback quando não vem no
            ``state`` — útil quando o produto invoca o Writer dentro de um grafo.

    Returns:
        dict com a chave ``article`` (str) contendo o markdown do artigo.
    """
    messages = state.get("messages")
    focal_argument = state.get("focal_argument")
    previous_article = state.get("previous_article")
    product_context = state.get("product_context")

    if product_context is None and config:
        product_context = config.get("configurable", {}).get("product_context")

    logger.info(
        "=== NÓ WRITER: gerando artigo (previous=%s, focal=%s, product_context=%s) ===",
        "sim" if previous_article else "não",
        "sim" if focal_argument else "não",
        "sim" if product_context else "não",
    )

    system_prompt = _load_system_prompt()
    model_name = _load_model_name()

    filled_prompt = (
        system_prompt
        .replace("{product_context_section}", _format_product_context(product_context))
        .replace("{focal_argument_section}", _format_focal_argument(focal_argument))
        .replace("{previous_article_section}", _format_previous_article(previous_article))
        .replace("{conversation_section}", _format_conversation(messages))
    )

    llm = create_anthropic_client(model=model_name, temperature=0.2)
    response = llm.invoke([HumanMessage(content=filled_prompt)])

    article = response.content if hasattr(response, "content") else str(response)
    if isinstance(article, list):
        article = "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in article
        )
    article = (article or "").strip()

    logger.info("=== NÓ WRITER: artigo gerado (%d chars) ===", len(article))

    return {"article": article}


# ---------------------------------------------------------------------------
# writer_section_node — C-ENSAIO-3.2
# ---------------------------------------------------------------------------

_SECTION_PROMPT = """\
Você é o Escritor, especialista em artigos técnico-científicos em markdown.

{product_context_section}

## TAREFA

Redigir o corpo da seção **{section_title}** do artigo.

Regras:
- Retorne APENAS o corpo markdown da seção, sem repetir o cabeçalho `## {section_title}`.
- Tom técnico e sóbrio; parágrafos curtos; português do Brasil.
- Preserve blocos de código, tabelas e saídas de terminal em fences markdown.
- Nunca invente números, resultados quantitativos ou citações não fornecidas.
{refinement_instruction}

{focal_argument_section}

{article_context_section}

{conversation_section}
"""


def _format_article_context(article_context: Optional[str]) -> str:
    if not article_context or not article_context.strip():
        return ""
    return (
        "## OUTRAS SEÇÕES JÁ REDIGIDAS\n\n"
        f"{article_context.strip()}\n\n---\n"
    )


def _format_refinement_instruction(current_body: str) -> str:
    if not current_body or not current_body.strip():
        return ""
    return (
        "- Esta é uma REGENERAÇÃO: o rascunho anterior está no histórico "
        "conversacional. Incorpore o feedback do pesquisador sem repetir "
        "o conteúdo anterior literalmente."
    )


def writer_section_node(
    state: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Gera ou regenera o corpo de uma seção individual do artigo.

    Args:
        state: dict com as chaves ``messages``, ``focal_argument``,
            ``section_title``, ``current_body``, ``article_context``,
            ``product_context``. Chaves ausentes são tratadas como None/"".
        config: ignorado na V1 (compatibilidade com assinatura LangGraph).
            ``product_context`` via ``config.configurable`` é aceito como
            fallback quando não vem no ``state``.

    Returns:
        dict com a chave ``section_content`` (str) — corpo markdown da seção,
        sem cabeçalho ``## Título``.
    """
    messages = state.get("messages")
    focal_argument = state.get("focal_argument")
    section_title = state.get("section_title", "Seção")
    current_body = state.get("current_body", "")
    article_context = state.get("article_context", "")
    product_context = state.get("product_context")

    if product_context is None and config:
        product_context = config.get("configurable", {}).get("product_context")

    logger.info(
        "=== NÓ WRITER_SECTION: seção='%s' modo=%s ===",
        section_title,
        "refinamento" if current_body else "geração",
    )

    model_name = _load_model_name()

    filled_prompt = (
        _SECTION_PROMPT
        .replace("{product_context_section}", _format_product_context(product_context))
        .replace("{section_title}", section_title)
        .replace("{refinement_instruction}", _format_refinement_instruction(current_body))
        .replace("{focal_argument_section}", _format_focal_argument(focal_argument))
        .replace("{article_context_section}", _format_article_context(article_context))
        .replace("{conversation_section}", _format_conversation(messages))
    )

    llm = create_anthropic_client(model=model_name, temperature=0.2)
    response = llm.invoke([HumanMessage(content=filled_prompt)])

    content = response.content if hasattr(response, "content") else str(response)
    if isinstance(content, list):
        content = "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    content = (content or "").strip()

    logger.info(
        "=== NÓ WRITER_SECTION: seção '%s' gerada (%d chars) ===",
        section_title,
        len(content),
    )

    return {"section_content": content}
