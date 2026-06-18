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
from typing import Any, Literal

SectionStatus = Literal["empty", "draft", "edited"]

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


def _render_markdown(content: str) -> str:
    """Pré-renderiza markdown→HTML no servidor.

    Saída usada por ``chat_panel`` via ``rx.html``. Mantém o ``rx.markdown``
    (e seu ``useContext`` interno) fora do ``rx.foreach``, eliminando a
    "change in order of Hooks" que o ``react-markdown`` dispara quando é
    montado pela primeira vez dentro de uma lista reativa.
    """
    if not content:
        return ""
    from markdown_it import MarkdownIt

    md = MarkdownIt("commonmark", {"breaks": True, "html": False, "linkify": True})
    return md.render(content)


def _extract_pending_proposal(out_messages: list) -> dict | None:
    """Detecta proposta de estrutura na última mensagem do Estruturador.

    Reusado por ``send_message`` (delta normal) e pela rehidratação do
    checkpoint (recovery de delta perdido na reconexão de socket).
    Retorna ``None`` quando não há proposta no histórico.
    """
    structurer_msgs = [
        m for m in out_messages
        if isinstance(m, AIMessage)
        and m.additional_kwargs.get("agent") == "structurer"
    ]
    if not structurer_msgs:
        return None
    ak = structurer_msgs[-1].additional_kwargs
    secs = ak.get("article_sections", [])
    if not secs:
        return None
    return {
        "sections": list(secs),
        "rationale": (ak.get("rationale") or "").strip(),
    }


def _message_to_ui_entry(msg) -> dict | None:
    """Converte ``HumanMessage``/``AIMessage`` do LangGraph para dict de UI.

    Devolve ``None`` para tipos de mensagem que a UI do Ensaio não
    renderiza (SystemMessage, ToolMessage, etc.). Mantém shape estável
    do dict (todas as chaves presentes) para o ``rx.foreach`` do Reflex.
    """
    if isinstance(msg, HumanMessage):
        content = msg.content if isinstance(msg.content, str) else str(msg.content)
        return {
            "role": "user",
            "agent": "user",
            "content": content,
            "content_html": _render_markdown(content),
            "timestamp": _now(),
            "change_summary": "",
        }
    if isinstance(msg, AIMessage):
        content = msg.content if isinstance(msg.content, str) else str(msg.content)
        ak = msg.additional_kwargs or {}
        return {
            "role": "assistant",
            "agent": ak.get("agent"),
            "content": content,
            "content_html": _render_markdown(content),
            "timestamp": _now(),
            "change_summary": ak.get("change_summary", "") or "",
        }
    return None


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

    # Co-decisão da estrutura (E-PROTO2-1)
    # Quando o Estruturador propõe uma estrutura, fica aqui aguardando
    # aceite/recusa do Usuário em vez de comitar direto em current_article.
    # Formato: {"sections": list[str], "rationale": str} ou {} (sem proposta).
    pending_structure_proposal: dict = {}

    # Edição leve da proposta (E-PROTO2-1.3)
    editing_proposal: bool = False
    proposal_draft: list[str] = []
    proposal_rationale_draft: str = ""
    proposal_edit_error: str = ""

    # Produto
    product_context: str = ""
    thread_id: str = ""

    # ---------------------------------------------------------------------------
    # Ciclo de vida
    # ---------------------------------------------------------------------------

    def initialize(self) -> None:
        """Carrega product_context e gera thread_id ao abrir a página.

        **Idempotente durante turno em voo.** Reflex re-executa ``on_load``
        em toda reconexão do websocket. Se o turno do Orquestrador segura
        o evento background tempo suficiente para o socket cair, a
        reconexão dispararia este handler novamente e zeraria
        ``messages``/``thread_id`` — a conversa sumiria da tela. O guard
        abaixo preserva a sessão em voo; recarregar tudo ainda zera
        (página recarregada vem sem turno ativo, ``processing_agent``
        está vazio).

        **Recovery de delta perdido.** Quando o socket cai durante o
        turno, o backend pode completar o evento ``background`` e tentar
        emitir o delta final na conexão antiga, que já não existe. O
        cliente reconectado fica com ``processing_agent`` preso e a
        resposta do agente nunca aparece. Para cobrir esse caso, dentro
        do guard consultamos o checkpointer do LangGraph: se há
        ``AIMessage`` no backend que a UI não tem, rehidratamos
        ``messages``/``langchain_history``/``focal_argument`` do
        checkpoint e limpamos ``processing_agent``.
        """
        if self.processing_agent:
            try:
                self._sync_with_checkpoint_if_completed()
            except Exception as exc:
                logger.warning("Falha ao sincronizar com checkpoint: %s", exc, exc_info=True)
            return

        from products.ensaio.app.product_config import ProductConfigError, load_product_context

        self.thread_id = str(uuid.uuid4())
        self.messages = []
        self.langchain_history = []
        self.focal_argument = {}
        self.current_article = []
        self.processing_agent = ""
        self.error_message = ""
        self.editing_section_index = -1
        self.pending_structure_proposal = {}
        self.editing_proposal = False
        self.proposal_draft = []
        self.proposal_rationale_draft = ""
        self.proposal_edit_error = ""

        try:
            self.product_context = load_product_context()
        except ProductConfigError as exc:
            logger.error("Erro ao carregar product.yaml: %s", exc)
            self.error_message = str(exc)

    def _sync_with_checkpoint_if_completed(self) -> None:
        """Rehidrata UI do checkpointer quando o backend terminou turno.

        Detecção: ``len(AIMessages no backend) > len(assistant messages na UI)``
        indica que o evento ``background`` produziu resposta mas o delta
        não chegou ao cliente (provavelmente porque o socket caiu durante
        o turno e reconectou). Quando isso acontece, reconstrói
        ``messages``/``langchain_history`` a partir das mensagens do
        checkpoint e limpa ``processing_agent`` para destravar a UI.

        Não toca em ``current_article``, ``pending_structure_proposal``,
        ``editing_*`` — esses são estado de produto que não vive no
        checkpoint do LangGraph. Para a proposta de estrutura, aplicamos
        ``_extract_pending_proposal`` para detectar nova proposta vinda
        do turno cujo delta se perdeu.
        """
        if not self.thread_id:
            return

        # Importa lazy para evitar custo de import quando o método não roda.
        from products.ensaio.app.graph import create_ensaio_graph

        graph = create_ensaio_graph()
        config = {
            "configurable": {
                "thread_id": self.thread_id,
                "product_context": self.product_context,
            }
        }
        snapshot = graph.get_state(config)
        if not snapshot or not snapshot.values:
            return

        graph_messages = snapshot.values.get("messages") or []
        backend_ai_count = sum(1 for m in graph_messages if isinstance(m, AIMessage))
        ui_ai_count = sum(1 for m in self.messages if m.get("role") == "assistant")
        if backend_ai_count <= ui_ai_count:
            # Backend ainda não terminou ou já estava sincronizado.
            return

        new_messages: list[dict] = []
        new_lh: list[dict] = []
        for m in graph_messages:
            entry = _message_to_ui_entry(m)
            if entry is None:
                continue
            new_messages.append(entry)
            if entry["role"] == "user":
                new_lh.append({"type": "human", "content": entry["content"]})
            else:
                new_lh.append({"type": "ai", "content": entry["content"]})

        self.messages = new_messages
        self.langchain_history = new_lh

        focal = snapshot.values.get("focal_argument")
        if focal:
            self.focal_argument = focal

        # Se o último estruturador do turno trouxe proposta de estrutura,
        # propaga (sem isso, bubble de proposta sumiria com a reconexão).
        new_proposal = _extract_pending_proposal(graph_messages)
        if new_proposal is not None:
            self.pending_structure_proposal = new_proposal
            self.editing_proposal = False
            self.proposal_draft = []
            self.proposal_rationale_draft = ""
            self.proposal_edit_error = ""

        self.processing_agent = ""
        logger.info(
            "Rehidratado do checkpoint (delta perdido na reconexão): "
            "%d msgs do backend, processing_agent zerado",
            backend_ai_count,
        )

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
                    "content_html": _render_markdown(user_text),
                    "timestamp": _now(),
                    "change_summary": "",
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
            change_summary: str = ""

            if out_messages:
                last = out_messages[-1]
                content = last.content if hasattr(last, "content") else str(last)
                last_ak = getattr(last, "additional_kwargs", {}) or {}
                agent_key = last_ak.get("agent")
                change_summary = last_ak.get("change_summary", "") or ""

            new_focal = result.get("focal_argument") or {}

            # E-PROTO2-1.1: estrutura proposta pelo Estruturador vira pendente,
            # não comita direto em current_article. Aceitar/Recusar é decisão
            # explícita do Usuário (event handlers abaixo).
            pending_proposal_update = _extract_pending_proposal(out_messages)

            new_lh = langchain_history + [
                {"type": "human", "content": user_text},
                {"type": "ai", "content": content},
            ]

            async with self:
                # change_summary sempre presente no dict (string vazia quando
                # ausente) para manter shape estável do msg ao longo do
                # foreach do Reflex — evita React Hooks violation.
                msg_entry = {
                    "role": "assistant",
                    "agent": agent_key,
                    "content": content,
                    "content_html": _render_markdown(content),
                    "timestamp": _now(),
                    "change_summary": change_summary,
                }
                self.messages = [*self.messages, msg_entry]
                self.langchain_history = new_lh
                if new_focal:
                    self.focal_argument = new_focal
                # Re-proposições substituem a proposta pendente; não há fila.
                if pending_proposal_update is not None:
                    self.pending_structure_proposal = pending_proposal_update
                    # Sair do modo de edição se o Usuário tinha começado a
                    # editar a proposta anterior.
                    self.editing_proposal = False
                    self.proposal_draft = []
                    self.proposal_rationale_draft = ""
                    self.proposal_edit_error = ""
                self.processing_agent = ""

        except Exception as exc:
            logger.error("Erro ao invocar grafo: %s", exc, exc_info=True)
            async with self:
                err_content = f"❌ Não consegui processar sua mensagem: {exc}"
                self.messages = [
                    *self.messages,
                    {
                        "role": "assistant",
                        "agent": None,
                        "content": err_content,
                        "content_html": _render_markdown(err_content),
                        "timestamp": _now(),
                        "change_summary": "",
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
    # Computed vars (evitam acesso a chaves opcionais em dicts vazios na UI)
    # ---------------------------------------------------------------------------

    @rx.var
    def has_pending_proposal(self) -> bool:
        proposal = self.pending_structure_proposal or {}
        return bool(proposal.get("sections"))

    @rx.var
    def proposal_sections(self) -> list[str]:
        proposal = self.pending_structure_proposal or {}
        secs = proposal.get("sections") or []
        return list(secs)

    @rx.var
    def proposal_rationale(self) -> str:
        proposal = self.pending_structure_proposal or {}
        return proposal.get("rationale", "") or ""

    # ---------------------------------------------------------------------------
    # Co-decisão da estrutura (E-PROTO2-1.1, 1.2, 1.3)
    # ---------------------------------------------------------------------------

    def _commit_proposal(self, sections: list[str]) -> None:
        """Comita uma lista de títulos como current_article e limpa o pendente."""
        self.current_article = [
            {"title": t, "body": "", "status": "empty", "index": i}
            for i, t in enumerate(sections)
        ]
        self.pending_structure_proposal = {}
        self.editing_proposal = False
        self.proposal_draft = []
        self.proposal_rationale_draft = ""
        self.proposal_edit_error = ""

    def accept_structure_proposal(self) -> None:
        """Aceita a proposta pendente (sem edição) e comita em current_article."""
        proposal = self.pending_structure_proposal or {}
        sections = list(proposal.get("sections") or [])
        if not sections:
            return
        self._commit_proposal(sections)

    def reject_structure_proposal(self) -> None:
        """Recusa a proposta pendente; current_article permanece intocado."""
        if not self.pending_structure_proposal:
            return
        self.pending_structure_proposal = {}
        self.editing_proposal = False
        self.proposal_draft = []
        self.proposal_rationale_draft = ""
        self.proposal_edit_error = ""
        reject_content = "_Proposta de estrutura recusada._"
        self.messages = [
            *self.messages,
            {
                "role": "assistant",
                "agent": None,
                "content": reject_content,
                "content_html": _render_markdown(reject_content),
                "timestamp": _now(),
                "change_summary": "",
            },
        ]

    def start_editing_proposal(self) -> None:
        """Abre a proposta pendente em modo editável."""
        proposal = self.pending_structure_proposal or {}
        sections = list(proposal.get("sections") or [])
        if not sections:
            return
        self.proposal_draft = list(sections)
        self.proposal_rationale_draft = proposal.get("rationale", "")
        self.editing_proposal = True
        self.proposal_edit_error = ""

    def update_proposal_section(self, index: int, value: str) -> None:
        if not self.editing_proposal:
            return
        if index < 0 or index >= len(self.proposal_draft):
            return
        new_draft = list(self.proposal_draft)
        new_draft[index] = value
        self.proposal_draft = new_draft

    def move_proposal_section(self, index: int, direction: int) -> None:
        """direction: -1 sobe, +1 desce."""
        if not self.editing_proposal:
            return
        target = index + direction
        if (
            index < 0 or index >= len(self.proposal_draft)
            or target < 0 or target >= len(self.proposal_draft)
        ):
            return
        new_draft = list(self.proposal_draft)
        new_draft[index], new_draft[target] = new_draft[target], new_draft[index]
        self.proposal_draft = new_draft

    def remove_proposal_section(self, index: int) -> None:
        if not self.editing_proposal:
            return
        if index < 0 or index >= len(self.proposal_draft):
            return
        new_draft = list(self.proposal_draft)
        new_draft.pop(index)
        self.proposal_draft = new_draft

    def add_proposal_section(self) -> None:
        if not self.editing_proposal:
            return
        self.proposal_draft = [*self.proposal_draft, "Nova seção"]

    def confirm_proposal_edit(self) -> None:
        if not self.editing_proposal:
            return
        cleaned = [s.strip() for s in self.proposal_draft if s and s.strip()]
        if not cleaned:
            self.proposal_edit_error = "A estrutura precisa de pelo menos uma seção."
            return
        self._commit_proposal(cleaned)

    def cancel_proposal_edit(self) -> None:
        self.editing_proposal = False
        self.proposal_draft = []
        self.proposal_rationale_draft = ""
        self.proposal_edit_error = ""

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
