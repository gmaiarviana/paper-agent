"""Estado Reflex do produto Ensaio (E-PROTO-1.2, 1.4, 2.0, 2.2, 2.3).

EnsaioState centraliza todo o estado da sessão. A sessão é descartável:
recarregar a página zera tudo (persistência fica para MVP-ENSAIO).

Campos serializáveis por design (princípio de viabilização §7 da vision):
estado do artigo e conversa vivem em estruturas dict/list — trocar a camada
de armazenamento no MVP não requer refatorar o domínio.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any

import reflex as rx
from langchain_core.messages import AIMessage, HumanMessage

logger = logging.getLogger(__name__)

_AGENT_LABELS: dict[str, str] = {
    "orchestrator": "🎯 Orquestrador",
    "structurer": "📐 Estruturador",
    "methodologist": "🔬 Metodologista",
    "writer": "✍️ Writer",
    "user": "👤 Você",
}


def _agent_label(agent: str | None) -> str:
    return _AGENT_LABELS.get(agent or "", "🤖 Sistema")


def _now() -> str:
    return datetime.now().isoformat()


def _deserialize_messages(history: list[dict]) -> list:
    result = []
    for m in history:
        t = m.get("type", "")
        c = m.get("content", "")
        if t == "human":
            result.append(HumanMessage(content=c))
        elif t == "ai":
            result.append(AIMessage(content=c))
    return result


def _build_article_context(article: list[dict], exclude_index: int) -> str:
    parts = []
    for i, sec in enumerate(article):
        if i == exclude_index:
            continue
        body = sec.get("body", "")
        if body:
            parts.append(f"### {sec.get('title', f'Seção {i+1}')}\n{body}")
    return "\n\n".join(parts)


class EnsaioState(rx.State):
    """Estado da sessão do Ensaio."""

    # Chat
    messages: list[dict] = []
    langchain_history: list[dict] = []
    user_input_field: str = ""

    # Agentes
    focal_argument: dict = {}
    processing_agent: str = ""      # "" = ocioso
    error_message: str = ""

    # Artigo seccionado
    current_article: list[dict] = []   # list[Section]
    editing_section_index: int = -1    # -1 = nenhuma seção em edição

    # Produto
    product_context: str = ""
    thread_id: str = ""

    # ---------------------------------------------------------------------------
    # Ciclo de vida
    # ---------------------------------------------------------------------------

    def initialize(self) -> None:
        """Carrega product_context e gera thread_id ao abrir a página."""
        from products.ensaio.app.product_config import ProductConfigError, load_product_context

        self.thread_id = str(uuid.uuid4())
        self.messages = []
        self.langchain_history = []
        self.focal_argument = {}
        self.current_article = []
        self.processing_agent = ""
        self.error_message = ""
        self.editing_section_index = -1

        try:
            self.product_context = load_product_context()
        except ProductConfigError as exc:
            logger.error("Erro ao carregar product.yaml: %s", exc)
            self.error_message = str(exc)

    # ---------------------------------------------------------------------------
    # Input do chat
    # ---------------------------------------------------------------------------

    def set_user_input_field(self, value: str) -> None:
        self.user_input_field = value

    @rx.event(background=True)
    async def send_message(self) -> None:
        """Processa mensagem do usuário: invoca o grafo e atualiza o estado."""
        async with self:
            user_text = self.user_input_field.strip()
            if not user_text or self.processing_agent:
                return
            self.user_input_field = ""
            self.processing_agent = "orchestrator"
            self.error_message = ""
            self.messages = [
                *self.messages,
                {
                    "role": "user",
                    "agent": "user",
                    "content": user_text,
                    "timestamp": _now(),
                },
            ]
            thread_id = self.thread_id
            product_context = self.product_context
            langchain_history = list(self.langchain_history)
            current_article = list(self.current_article)

        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: _invoke_graph(
                    user_text, thread_id, product_context, langchain_history
                ),
            )

            out_messages = result.get("messages", [])
            content = "Entendi. Pode me contar mais sobre o experimento?"
            agent_key: str | None = None

            if out_messages:
                last = out_messages[-1]
                content = last.content if hasattr(last, "content") else str(last)
                agent_key = getattr(last, "additional_kwargs", {}).get("agent")

            new_focal = result.get("focal_argument") or {}
            article_sections_update: list[dict] | None = None

            structurer_msgs = [
                m for m in out_messages
                if isinstance(m, AIMessage)
                and m.additional_kwargs.get("agent") == "structurer"
            ]
            if structurer_msgs:
                secs = structurer_msgs[-1].additional_kwargs.get("article_sections", [])
                if secs and (
                    not current_article
                    or all(s.get("status") == "empty" for s in current_article)
                ):
                    article_sections_update = [
                        {"title": t, "body": "", "status": "empty", "index": i}
                        for i, t in enumerate(secs)
                    ]

            new_lh = langchain_history + [
                {"type": "human", "content": user_text},
                {"type": "ai", "content": content},
            ]

            async with self:
                self.messages = [
                    *self.messages,
                    {
                        "role": "assistant",
                        "agent": agent_key,
                        "content": content,
                        "timestamp": _now(),
                    },
                ]
                self.langchain_history = new_lh
                if new_focal:
                    self.focal_argument = new_focal
                if article_sections_update is not None:
                    self.current_article = article_sections_update
                self.processing_agent = ""

        except Exception as exc:
            logger.error("Erro ao invocar grafo: %s", exc, exc_info=True)
            async with self:
                self.messages = [
                    *self.messages,
                    {
                        "role": "assistant",
                        "agent": None,
                        "content": f"❌ Não consegui processar sua mensagem: {exc}",
                        "timestamp": _now(),
                    },
                ]
                self.processing_agent = ""
                self.error_message = str(exc)

    # ---------------------------------------------------------------------------
    # Geração de seção (E-PROTO-2.2)
    # ---------------------------------------------------------------------------

    @rx.event(background=True)
    async def generate_section(self, section_index: int) -> None:
        """Gera ou regenera o conteúdo de uma seção individual."""
        async with self:
            if self.processing_agent:
                return
            self.processing_agent = "writer"
            article = list(self.current_article)
            langchain_history = list(self.langchain_history)
            focal_argument = dict(self.focal_argument)
            product_context = self.product_context

        try:
            section = article[section_index]
            article_context = _build_article_context(article, exclude_index=section_index)

            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: _invoke_writer_section(
                    messages=_deserialize_messages(langchain_history),
                    focal_argument=focal_argument or None,
                    section_title=section.get("title", f"Seção {section_index + 1}"),
                    current_body=section.get("body", ""),
                    article_context=article_context,
                    product_context=product_context,
                ),
            )

            new_body = result.get("section_content", "").strip()
            updated_article = [dict(s) for s in article]
            updated_article[section_index] = {
                **updated_article[section_index],
                "body": new_body,
                "status": "draft",
            }

            async with self:
                self.current_article = updated_article
                self.processing_agent = ""

        except Exception as exc:
            logger.error("Erro ao gerar seção %d: %s", section_index, exc, exc_info=True)
            async with self:
                self.processing_agent = ""
                self.error_message = str(exc)

    # ---------------------------------------------------------------------------
    # Edição inline de seção (E-PROTO-2.3)
    # ---------------------------------------------------------------------------

    def start_editing_section(self, section_index: int) -> None:
        self.editing_section_index = section_index

    def update_section_content(self, section_index: int, content: str) -> None:
        updated = [dict(s) for s in self.current_article]
        updated[section_index] = {
            **updated[section_index],
            "body": content,
            "status": "edited",
        }
        self.current_article = updated
        self.editing_section_index = -1

    def cancel_editing(self) -> None:
        self.editing_section_index = -1


# ---------------------------------------------------------------------------
# Helpers de invocação (funções puras fora do State, para uso em executor)
# ---------------------------------------------------------------------------

def _invoke_graph(
    user_text: str,
    thread_id: str,
    product_context: str,
    langchain_history: list[dict],
) -> dict:
    from products.ensaio.app.graph import create_ensaio_graph

    graph = create_ensaio_graph()
    prior_msgs = _deserialize_messages(langchain_history)
    state: dict[str, Any] = {
        "user_input": user_text,
        "messages": [*prior_msgs, HumanMessage(content=user_text)],
    }
    config = {
        "configurable": {
            "thread_id": thread_id,
            "product_context": product_context,
        }
    }
    return graph.invoke(state, config=config)


def _invoke_writer_section(
    messages: list,
    focal_argument: dict | None,
    section_title: str,
    current_body: str,
    article_context: str,
    product_context: str,
) -> dict:
    from core.agents.writer.nodes import writer_section_node

    return writer_section_node(
        {
            "messages": messages,
            "focal_argument": focal_argument,
            "section_title": section_title,
            "current_body": current_body,
            "article_context": article_context,
            "product_context": product_context,
        }
    )
