"""Painel de detalhe do card selecionado no kanban.

Roteia por ``epic.state``:
    - 🌱/🧭/📐/📋 → guidance + prompt de refinamento (W-PROTO-PLAT-4)
    - 🔍 → prompt de dispatch do milestone (W-PROTO-PLAT-3.1)
    - 🏗️ → link para a branch no GitHub (W-PROTO-PLAT-3.2)
    - 🔀 → link para a PR no GitHub (W-PROTO-PLAT-3.2)
    - ✅ → resumo enxuto sem ações (W-PROTO-PLAT-3.2)
"""

from __future__ import annotations

import streamlit as st

from tools.workflow_platform.config_loader import PlatformConfig
from tools.workflow_platform.models import Epic, EpicState
from tools.workflow_platform.prompts.dispatch import build_dispatch_prompt
from tools.workflow_platform.prompts.refinement import (
    build_refinement_prompt,
    get_next_step,
)


def github_branch_url(owner: str, repo: str, branch: str) -> str:
    return f"https://github.com/{owner}/{repo}/tree/{branch}"


def github_pr_url(owner: str, repo: str, pr_number: int) -> str:
    return f"https://github.com/{owner}/{repo}/pull/{pr_number}"


def _render_header(epic: Epic) -> None:
    st.markdown(f"## {epic.id} — {epic.title}")
    milestone_label = epic.milestone_id or "_(sem milestone)_"
    st.caption(f"Estado: **{epic.state.value}** · Milestone: **{milestone_label}** · ROADMAP: `{epic.roadmap_path}`")


def _render_pre_execution(epic: Epic) -> None:
    info = get_next_step(epic)
    if info is None:
        return
    st.info(info.guidance_text)
    if info.readiness_checklist:
        st.markdown(
            "Checklist do alvo `🔍`: "
            "[`docs/process/refinement/autonomous_readiness.md`]"
            "(../../docs/process/refinement/autonomous_readiness.md)"
        )

    prompt = build_refinement_prompt(epic)
    if prompt is None:
        return

    st.markdown("**Prompt de refinamento (clipboard-ready):**")
    st.code(prompt, language="text")


def _render_dispatch(epic: Epic, all_epics_in_milestone: list[Epic]) -> None:
    result = build_dispatch_prompt(epic, all_epics_in_milestone)

    for warning in result.warnings:
        if result.blocked:
            st.warning(warning)
        else:
            st.info(warning)

    if result.blocked or result.prompt_text is None:
        return

    st.markdown("**Prompt de dispatch (clipboard-ready):**")
    st.code(result.prompt_text, language="text")


def _render_in_progress(epic: Epic, config: PlatformConfig) -> None:
    if not epic.branch:
        st.warning("branch não declarada no ROADMAP — verifique campo `**Branch:**`")
        return
    url = github_branch_url(config.github_owner, config.github_repo, epic.branch)
    st.markdown(f"**Branch em andamento:** [`{epic.branch}`]({url})")


def _render_in_review(epic: Epic, config: PlatformConfig) -> None:
    url = epic.pr_url
    if not url and epic.pr_number is not None:
        url = github_pr_url(config.github_owner, config.github_repo, epic.pr_number)

    if not url:
        st.warning(
            "PR não declarada no ROADMAP — verifique a linha `**Status:** 🔀 ... PR #N (URL)`"
        )
        return

    label = f"PR #{epic.pr_number}" if epic.pr_number else "PR"
    st.markdown(f"**Em revisão:** [{label}]({url})")


def _render_done(epic: Epic) -> None:
    st.success("Épico implementado.")
    excerpt = epic.body_excerpt or "(sem resumo)"
    st.markdown("**Resumo do bloco:**")
    st.markdown(f"```text\n{excerpt}\n```")


def render_card_detail(
    epic: Epic,
    all_epics_in_milestone: list[Epic],
    config: PlatformConfig,
) -> None:
    """Roteia por ``epic.state`` e delega para o renderer apropriado."""
    _render_header(epic)

    if epic.state in {EpicState.VISION, EpicState.ALIGNED, EpicState.SKETCHED, EpicState.CRITERIA}:
        _render_pre_execution(epic)
    elif epic.state == EpicState.DETAILED:
        _render_dispatch(epic, all_epics_in_milestone)
    elif epic.state == EpicState.IN_PROGRESS:
        _render_in_progress(epic, config)
    elif epic.state == EpicState.IN_REVIEW:
        _render_in_review(epic, config)
    elif epic.state == EpicState.DONE:
        _render_done(epic)
