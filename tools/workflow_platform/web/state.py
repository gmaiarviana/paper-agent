"""Estado Reflex da plataforma de workflow (W-PILOTO-UX-1).

``PlatformState`` substitui as chaves soltas de ``st.session_state`` da
versão Streamlit por um único ``rx.State`` no backend. O miolo
(``parser``, ``config_loader``, ``preferences``, ``job_queue/*``, ``prompts/*``,
``world_state``, ``presenters``) é consumido intocado — só a camada de
view/estado migra.

Objetos ricos (``Epic``, ``QueueItem``) não entram crus no ``rx.State``
(Reflex exige vars serializáveis); vivem como ``dict`` e são reconstruídos
sob demanda nos handlers, onde os builders de prompt precisam deles.
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import reflex as rx

from tools.workflow_platform.config_loader import load_config
from tools.workflow_platform.preferences import (
    Preferences,
    PreferencesLoadError,
    load_preferences,
    save_preferences,
)
from tools.workflow_platform.parser import parse_roadmap
from tools.workflow_platform.presenters import (
    STATE_LABELS,
    TYPE_HEADERS,
    KANBAN_COLUMN_ORDER,
    TYPE_ORDER,
    card_button_label,
    epic_from_dict,
    group_by_milestone,
    roadmap_from_dict,
    roadmap_to_dict,
)
from tools.workflow_platform.prompts.dispatch import build_dispatch_prompt
from tools.workflow_platform.prompts.queue_item import build_prompt_for_item
from tools.workflow_platform.prompts.refinement import (
    build_refinement_prompt,
    get_next_step,
)
from tools.workflow_platform.job_queue.detect import detect_all_items
from tools.workflow_platform.job_queue.load import (
    LOAD_STATE_COLORS,
    QUEUE_TARGET_LIMIT,
    QueueLoadState,
    compute_load_state,
)
from tools.workflow_platform.job_queue.models import (
    BranchPointer,
    EpicPointer,
    ItemType,
    PRPointer,
    RefinePointer,
)
from tools.workflow_platform.models import (
    Epic,
    EpicState,
    blocking_predecessors_of,
)
from tools.workflow_platform.world_state import build_world_state
from tools.workflow_platform.web.view_models import (
    DispatchWarning,
    EpicCard,
    KanbanColumn,
    KanbanDetail,
    KanbanGroup,
    QueueGroup,
    QueueItemView,
    SidebarRoadmap,
)


def github_branch_url(owner: str, repo: str, branch: str) -> str:
    return f"https://github.com/{owner}/{repo}/tree/{branch}"


def github_pr_url(owner: str, repo: str, pr_number: int) -> str:
    return f"https://github.com/{owner}/{repo}/pull/{pr_number}"


_PRE_EXECUTION_STATES = {
    EpicState.VISION,
    EpicState.ALIGNED,
    EpicState.SKETCHED,
    EpicState.CRITERIA,
}

# Estados em que uma ação (dispatch de 🔍 ou refino de 📐/📋) seria oferecida —
# só nesses o predecessor bloqueante importa (Fila oculta / selo no Kanban).
_BLOCKABLE_STATES = {
    EpicState.SKETCHED,
    EpicState.CRITERIA,
    EpicState.DETAILED,
}


class PlatformState(rx.State):
    """Estado único da plataforma — substitui ``st.session_state``."""

    # --- config (extraída no on_load) ---
    github_owner: str = ""
    github_repo: str = ""
    repo_root: str = ""

    # --- dados serializados ---
    roadmaps_all: list[dict] = []   # todos os ROADMAPs parseados (sidebar + kanban)
    queue_items: list[QueueItemView] = []   # visíveis, com prompt + pointer_md embutidos

    # --- preferências / filtro ---
    visible_roadmaps: list[str] = []   # rels visíveis (concreto; None de prefs → todos)
    stale_threshold_days: int = 7
    prefs_error: str = ""
    fetch_warning: str = ""
    parser_warnings: list[list[str]] = []   # [[nome_arquivo, aviso], ...]
    show_warnings: bool = False

    # --- navegação / seleção ---
    active_tab: str = "fila"
    selected_item_id: str = ""
    selected_epic_id: str = ""
    kanban_detail: KanbanDetail = KanbanDetail()

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------

    def on_load(self) -> None:
        """Carrega config, ROADMAPs, preferências e detecta a fila."""
        self._load(do_fetch=True)

    def reload(self) -> None:
        """Recarrega tudo do disco (botão 🔄)."""
        self._load(do_fetch=True)

    def _load(self, *, do_fetch: bool = True) -> None:
        config = load_config()
        self.github_owner = config.github_owner
        self.github_repo = config.github_repo
        self.repo_root = str(config.repo_root)

        parsed_all = [parse_roadmap(p) for p in config.roadmaps]
        self.roadmaps_all = [roadmap_to_dict(r, config.repo_root) for r in parsed_all]

        try:
            prefs = load_preferences(config.repo_root)
            self.prefs_error = ""
        except PreferencesLoadError as exc:
            prefs = Preferences()
            self.prefs_error = str(exc)

        self.stale_threshold_days = prefs.stale_branch_threshold_days
        all_rels = [d["rel"] for d in self.roadmaps_all]
        self.visible_roadmaps = (
            list(prefs.visible_roadmaps)
            if prefs.visible_roadmaps is not None
            else list(all_rels)
        )

        warns = [[Path(r.path).name, w] for r in parsed_all for w in r.warnings]
        if self.prefs_error:
            warns = [[".preferences.json", self.prefs_error], *warns]
        self.parser_warnings = warns

        self._recompute_queue(do_fetch=do_fetch)

    # ------------------------------------------------------------------
    # Detecção da fila
    # ------------------------------------------------------------------

    def _visible_parsed(self) -> list:
        visible = set(self.visible_roadmaps)
        return [
            roadmap_from_dict(d)
            for d in self.roadmaps_all
            if d["rel"] in visible
        ]

    def _visible_epic_maps(self) -> tuple[dict[str, Epic], dict[str, list[Epic]]]:
        """``(epics_by_id, epics_by_milestone)`` sobre os ROADMAPs visíveis.

        Insumo da regra compartilhada de predecessor bloqueante
        (``blocking_predecessors_of``), usada pelo Kanban (badge de bloqueio) e
        pelo painel de detalhe.
        """
        by_id: dict[str, Epic] = {}
        by_milestone: dict[str, list[Epic]] = {}
        for r in self._visible_parsed():
            for e in r.epics:
                by_id[e.id] = e
                if e.milestone_id:
                    by_milestone.setdefault(e.milestone_id, []).append(e)
        return by_id, by_milestone

    def _recompute_queue(self, *, do_fetch: bool = True) -> None:
        parsed = self._visible_parsed()

        epic_lookup: dict[str, Epic] = {}
        by_milestone: dict[str, list[Epic]] = {}
        for r in parsed:
            for e in r.epics:
                epic_lookup[e.id] = e
                if e.milestone_id:
                    by_milestone.setdefault(e.milestone_id, []).append(e)

        state, warning = build_world_state(
            parsed,
            threshold_days=self.stale_threshold_days,
            do_fetch=do_fetch,
        )
        items = detect_all_items(state, threshold_days=self.stale_threshold_days)
        self.fetch_warning = warning or ""
        self.queue_items = [
            self._item_view(
                it,
                build_prompt_for_item(
                    it,
                    all_epics_by_milestone=by_milestone,
                    epic_lookup=epic_lookup,
                ),
            )
            for it in items
        ]

    def _item_view(self, item, prompt: str) -> QueueItemView:
        emoji, label = TYPE_HEADERS[item.type]
        return QueueItemView(
            id=item.id,
            item_type=item.type.value,
            emoji=emoji,
            type_label=label,
            title=item.title,
            context=item.context,
            expected_action=item.expected_action,
            pointer_md=self._pointer_md(item),
            prompt=prompt,
            card_label=f"{emoji} {item.title}",
            title_label=f"{emoji} {item.title}",
            action_label=f"Ação esperada: {item.expected_action}",
            meta=f"Tipo: {label} · ID: {item.id}",
        )

    def _pointer_md(self, item) -> str:
        p = item.source_pointer
        if isinstance(p, PRPointer) and p.pr_url:
            return f"**PR:** [#{p.pr_number}]({p.pr_url})"
        if isinstance(p, BranchPointer):
            url = github_branch_url(self.github_owner, self.github_repo, p.branch_name)
            return f"**Branch:** [`{p.branch_name}`]({url}) · {p.days_stale} dias"
        if isinstance(p, EpicPointer):
            return (
                f"**Épico:** `{p.epic_id}` · Milestone `{p.milestone_id}` · "
                f"ROADMAP `{p.roadmap_path}`"
            )
        if isinstance(p, RefinePointer):
            return (
                f"**Épico:** `{p.epic_id}` · "
                f"{p.current_state.value} → {p.target_state.value}"
            )
        return ""

    # ------------------------------------------------------------------
    # Fila — computed vars + seleção
    # ------------------------------------------------------------------

    @rx.var
    def grouped_queue(self) -> list[QueueGroup]:
        """Agrupa itens por tipo na ordem fixa, só buckets não-vazios."""
        buckets: "OrderedDict[ItemType, list[QueueItemView]]" = OrderedDict(
            (t, []) for t in TYPE_ORDER
        )
        for it in self.queue_items:
            buckets[ItemType(it.item_type)].append(it)
        out: list[QueueGroup] = []
        for t in TYPE_ORDER:
            bucket = buckets[t]
            if not bucket:
                continue
            emoji, label = TYPE_HEADERS[t]
            out.append(
                QueueGroup(
                    emoji=emoji,
                    label=label,
                    count=len(bucket),
                    cards=bucket,
                    header=f"{emoji} {label} ({len(bucket)})",
                )
            )
        return out

    @rx.var
    def has_queue_items(self) -> bool:
        return len(self.queue_items) > 0

    @rx.var
    def selected_queue_item(self) -> QueueItemView:
        for it in self.queue_items:
            if it.id == self.selected_item_id:
                return it
        return QueueItemView()

    @rx.var
    def has_selected_item(self) -> bool:
        return self.selected_item_id != "" and self.selected_queue_item.id != ""

    @rx.var
    def queue_badge_text(self) -> str:
        n = len(self.queue_items)
        if n == 0:
            return f"📋 Fila: 0/{QUEUE_TARGET_LIMIT} — sem itens"
        return f"📋 Fila: {n}/{QUEUE_TARGET_LIMIT}"

    @rx.var
    def queue_badge_color(self) -> str:
        return LOAD_STATE_COLORS[compute_load_state(len(self.queue_items))]

    @rx.var
    def is_over_limit(self) -> bool:
        return compute_load_state(len(self.queue_items)) == QueueLoadState.OVER_LIMIT

    def select_item(self, item_id: str) -> None:
        self.selected_item_id = item_id

    def close_item(self) -> None:
        self.selected_item_id = ""

    # ------------------------------------------------------------------
    # Kanban — computed var + seleção/detalhe
    # ------------------------------------------------------------------

    @rx.var
    def kanban_columns(self) -> list[KanbanColumn]:
        visible = set(self.visible_roadmaps)
        epics = [
            epic_from_dict(e)
            for d in self.roadmaps_all
            if d["rel"] in visible
            for e in d["epics"]
        ]
        by_id: dict[str, Epic] = {e.id: e for e in epics}
        by_milestone: dict[str, list[Epic]] = {}
        for e in epics:
            if e.milestone_id:
                by_milestone.setdefault(e.milestone_id, []).append(e)
        columns: list[KanbanColumn] = []
        for state in KANBAN_COLUMN_ORDER:
            in_state = [e for e in epics if e.state == state]
            grouped = group_by_milestone(in_state)
            groups = [
                KanbanGroup(
                    milestone_id=mid,
                    epics=[
                        self._epic_card(e, by_id, by_milestone)
                        for e in es
                    ],
                )
                for mid, es in grouped.items()
            ]
            columns.append(
                KanbanColumn(
                    state_label=STATE_LABELS[state],
                    count=len(in_state),
                    count_label=f"{len(in_state)} épicos",
                    groups=groups,
                )
            )
        return columns

    def _epic_card(
        self,
        epic: Epic,
        by_id: dict[str, Epic],
        by_milestone: dict[str, list[Epic]],
    ) -> EpicCard:
        blocking = (
            blocking_predecessors_of(epic, by_id, by_milestone)
            if epic.state in _BLOCKABLE_STATES
            else []
        )
        label = card_button_label(epic, selected=(epic.id == self.selected_epic_id))
        if blocking:
            label = f"🔒 {label}"
        return EpicCard(
            id=epic.id,
            label=label,
            selected=epic.id == self.selected_epic_id,
            blocked=bool(blocking),
            blocked_note=(
                f"🔒 aguardando {', '.join(blocking)}" if blocking else ""
            ),
        )

    @rx.var
    def has_kanban_detail(self) -> bool:
        return self.kanban_detail.kind != ""

    def select_epic(self, epic_id: str) -> None:
        self.selected_epic_id = epic_id
        self.kanban_detail = self._build_kanban_detail(epic_id)

    def close_epic(self) -> None:
        self.selected_epic_id = ""
        self.kanban_detail = KanbanDetail()

    def _find_visible_epic(self, epic_id: str) -> Epic | None:
        for r in self._visible_parsed():
            for e in r.epics:
                if e.id == epic_id:
                    return e
        return None

    def _build_kanban_detail(self, epic_id: str) -> KanbanDetail:
        epic = self._find_visible_epic(epic_id)
        if epic is None:
            return KanbanDetail()

        milestone_label = epic.milestone_id or "(sem milestone)"
        detail = KanbanDetail(
            id=epic.id,
            title=epic.title,
            state_label=STATE_LABELS[epic.state],
            milestone=milestone_label,
            roadmap=epic.roadmap_path,
            header=f"{epic.id} — {epic.title}",
            meta=f"Estado: {STATE_LABELS[epic.state]} · Milestone: {milestone_label}",
        )

        by_id, by_milestone = self._visible_epic_maps()
        blocking = (
            blocking_predecessors_of(epic, by_id, by_milestone)
            if epic.state in _BLOCKABLE_STATES
            else []
        )
        if blocking:
            # Bloqueado: sem botão/prompt de ação — comunica o bloqueio.
            detail.kind = "blocked"
            detail.blocked_by = ", ".join(blocking)
            return detail

        if epic.state in _PRE_EXECUTION_STATES:
            detail.kind = "pre"
            info = get_next_step(epic)
            if info is not None:
                detail.guidance = info.guidance_text
                detail.show_readiness = info.readiness_checklist
            detail.refine_prompt = build_refinement_prompt(epic) or ""
        elif epic.state == EpicState.DETAILED:
            detail.kind = "dispatch"
            result = build_dispatch_prompt(epic, by_id, by_milestone)
            detail.dispatch_prompt = result.prompt_text or ""
            detail.dispatch_warnings = [
                DispatchWarning(text=w, blocked=result.blocked) for w in result.warnings
            ]
        elif epic.state == EpicState.IN_PROGRESS:
            detail.kind = "in_progress"
            if not epic.branch:
                detail.warn = "branch não declarada no ROADMAP — verifique campo `**Branch:**`"
            else:
                url = github_branch_url(self.github_owner, self.github_repo, epic.branch)
                detail.link_md = f"**Branch em andamento:** [`{epic.branch}`]({url})"
        elif epic.state == EpicState.IN_REVIEW:
            detail.kind = "in_review"
            url = epic.pr_url
            if not url and epic.pr_number is not None:
                url = github_pr_url(self.github_owner, self.github_repo, epic.pr_number)
            if not url:
                detail.warn = (
                    "PR não declarada no ROADMAP — verifique a linha "
                    "`**Status:** 🔀 ... PR #N (URL)`"
                )
            else:
                label = f"PR #{epic.pr_number}" if epic.pr_number else "PR"
                detail.link_md = f"**Em revisão:** [{label}]({url})"
        elif epic.state == EpicState.DONE:
            detail.kind = "done"
            detail.excerpt = epic.body_excerpt or "(sem resumo)"

        return detail

    # ------------------------------------------------------------------
    # Sidebar — filtro de visibilidade + avisos
    # ------------------------------------------------------------------

    @rx.var
    def sidebar_roadmaps(self) -> list[SidebarRoadmap]:
        visible = set(self.visible_roadmaps)
        return [
            SidebarRoadmap(
                rel=d["rel"],
                label=d["label"],
                count=len(d["epics"]),
                checked=d["rel"] in visible,
                display=f"{d['label']} ({len(d['epics'])})",
            )
            for d in self.roadmaps_all
        ]

    @rx.var
    def warnings_count(self) -> int:
        return len(self.parser_warnings)

    @rx.var
    def warning_lines(self) -> list[str]:
        return [f"• {name}: {msg}" for name, msg in self.parser_warnings]

    def set_active_tab(self, tab: str) -> None:
        self.active_tab = tab

    def toggle_warnings(self) -> None:
        self.show_warnings = not self.show_warnings

    def toggle_roadmap(self, rel: str) -> None:
        s = set(self.visible_roadmaps)
        if rel in s:
            s.discard(rel)
        else:
            s.add(rel)
        self.visible_roadmaps = sorted(s)
        self._persist_visibility()
        # Filtro só muda quais ROADMAPs estão visíveis — o estado da remote
        # (branches/PRs) não muda. Redetecção local (reparse + detect_all sobre
        # os visíveis) basta; o `git fetch` de rede fica só no on_load e no
        # botão 🔄 Recarregar (evita pausa de rede a cada clique de checkbox).
        self._recompute_queue(do_fetch=False)
        if self.selected_item_id and not any(
            i.id == self.selected_item_id for i in self.queue_items
        ):
            self.selected_item_id = ""
        if self.selected_epic_id and self._find_visible_epic(self.selected_epic_id) is None:
            self.selected_epic_id = ""
            self.kanban_detail = KanbanDetail()

    def _persist_visibility(self) -> None:
        all_rels = sorted(d["rel"] for d in self.roadmaps_all)
        new_value = (
            None if sorted(self.visible_roadmaps) == all_rels else list(self.visible_roadmaps)
        )
        save_preferences(
            Preferences(
                visible_roadmaps=new_value,
                stale_branch_threshold_days=self.stale_threshold_days,
            ),
            Path(self.repo_root),
        )
