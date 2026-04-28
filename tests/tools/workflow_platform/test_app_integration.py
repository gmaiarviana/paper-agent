"""Testes de integração da plataforma Streamlit via ``streamlit.testing.v1.AppTest``.

Cobertura: clique num card do kanban → painel de detalhe é renderizado
no topo da página (acima do kanban), com o conteúdo correto para cada
grupo de estado (🔍, 🏗️, 🔀, ✅, pré-execução).

Os helpers puros já são cobertos por ``test_kanban``,
``test_dispatch_prompt`` e ``test_refinement_prompt``. Este módulo cobre
o caminho que vai do ``st.button`` em ``views/kanban.py`` ao
``render_card_detail`` em ``views/card_detail.py`` via session_state.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest
from streamlit.testing.v1 import AppTest

REPO_ROOT = Path(__file__).resolve().parents[3]
APP_PATH = REPO_ROOT / "tools" / "workflow_platform" / "app.py"


SYNTHETIC_ROADMAP_FOR_INTEGRATION = dedent(
    """
    # ROADMAP — Sintético

    ## 🎯 Milestones

    ### M-CLEAN

    - **Objetivo:** milestone limpo (todos em 🔍) para testar dispatch sem bloqueio
    - **Épicos agrupados:** SYNTH-DETAILED

    ### M-MIXED

    - **Objetivo:** milestone com épicos em vários estados de execução
    - **Épicos agrupados:** SYNTH-VISION, SYNTH-PROGRESS, SYNTH-REVIEW, SYNTH-DONE

    ## 📋 Épicos

    #### ÉPICO SYNTH-VISION: épico sintético em visão
    **Milestone:** `M-MIXED`
    **Status:** 🌱 Visão
    ---
    #### ÉPICO SYNTH-DETAILED: épico sintético em detalhes
    **Milestone:** `M-CLEAN`
    **Status:** 🔍 Detalhes definidos
    ---
    #### ÉPICO SYNTH-PROGRESS: épico sintético em andamento
    **Milestone:** `M-MIXED`
    **Branch:** `milestone/sintetico`
    **Status:** 🏗️ Em andamento
    ---
    #### ÉPICO SYNTH-REVIEW: épico sintético em revisão
    **Milestone:** `M-MIXED`
    **Status:** 🔀 Em revisão — PR #999 (https://github.com/foo/bar/pull/999)
    ---
    #### ÉPICO SYNTH-DONE: épico sintético implementado
    **Milestone:** `M-MIXED`
    **Status:** ✅ Implementado — PR #100 (merge `abc1234`, 2026-01-01)

    Resumo do bloco do épico SYNTH-DONE para o painel de detalhe.
    """
).strip()


@pytest.fixture
def synthetic_app(tmp_path: Path, monkeypatch):
    """Aponta o app para um config.yaml temporário com 1 ROADMAP sintético.

    Permite testar todos os estados (incluindo 🏗️/🔀/✅) sem depender do
    estado dos ROADMAPs reais do repo.
    """
    fake_repo = tmp_path / "repo"
    (fake_repo / "tools" / "workflow_platform").mkdir(parents=True)
    (fake_repo / "docs").mkdir()

    roadmap = fake_repo / "docs" / "ROADMAP.md"
    roadmap.write_text(SYNTHETIC_ROADMAP_FOR_INTEGRATION, encoding="utf-8")

    config = fake_repo / "tools" / "workflow_platform" / "config.yaml"
    config.write_text(
        dedent(
            """
            github:
              owner: foo
              repo: bar
            roadmaps:
              - docs/ROADMAP.md
            """
        ).strip(),
        encoding="utf-8",
    )

    monkeypatch.setenv("WORKFLOW_PLATFORM_REPO_ROOT", str(fake_repo))
    return fake_repo


def _make_app(repo_root: Path) -> AppTest:
    """Constrói AppTest pulando o auto-detect de repo_root via patch."""
    from tools.workflow_platform import config_loader as cl

    original = cl._detect_repo_root
    cl._detect_repo_root = lambda start=None: repo_root

    at = AppTest.from_file(str(APP_PATH), default_timeout=20)
    at.run()

    cl._detect_repo_root = original
    return at


def _click_card(at: AppTest, epic_id: str) -> AppTest:
    button = next((b for b in at.button if b.key and epic_id in b.key), None)
    assert button is not None, f"botão de {epic_id} não encontrado em {[b.key for b in at.button]}"
    button.click()
    at.run()
    return at


def _all_text(at: AppTest) -> str:
    parts: list[str] = []
    parts.extend(m.body or "" for m in at.markdown)
    parts.extend(getattr(c, "value", "") or "" for c in at.code)
    parts.extend(i.body or "" for i in at.info)
    parts.extend(s.body or "" for s in at.success)
    parts.extend(w.body or "" for w in at.warning)
    return "\n".join(parts)


def _detail_above_kanban(at: AppTest, epic_id: str) -> bool:
    """O header do detail (`## <ID>`) precisa vir antes da primeira coluna do kanban."""
    md = [m.body or "" for m in at.markdown]
    header_idx = next((i for i, b in enumerate(md) if b.startswith(f"## {epic_id}")), None)
    kanban_idx = next((i for i, b in enumerate(md) if b.startswith("### 🌱")), None)
    return header_idx is not None and kanban_idx is not None and header_idx < kanban_idx


def test_click_in_review_card_shows_pr_link(synthetic_app: Path):
    at = _make_app(synthetic_app)
    _click_card(at, "SYNTH-REVIEW")

    assert at.session_state["selected_epic_id"] == "SYNTH-REVIEW"
    assert _detail_above_kanban(at, "SYNTH-REVIEW")
    text = _all_text(at)
    assert "PR #999" in text
    assert "https://github.com/foo/bar/pull/999" in text


def test_click_in_progress_card_shows_branch_link(synthetic_app: Path):
    at = _make_app(synthetic_app)
    _click_card(at, "SYNTH-PROGRESS")

    assert at.session_state["selected_epic_id"] == "SYNTH-PROGRESS"
    assert _detail_above_kanban(at, "SYNTH-PROGRESS")
    text = _all_text(at)
    assert "milestone/sintetico" in text
    assert "https://github.com/foo/bar/tree/milestone/sintetico" in text


def test_click_detailed_card_shows_dispatch_prompt(synthetic_app: Path):
    at = _make_app(synthetic_app)
    _click_card(at, "SYNTH-DETAILED")

    assert at.session_state["selected_epic_id"] == "SYNTH-DETAILED"
    assert _detail_above_kanban(at, "SYNTH-DETAILED")
    code_values = [getattr(c, "value", "") or "" for c in at.code]
    assert any("implementa o M-CLEAN" in v for v in code_values)


def test_click_pre_execution_card_shows_refinement_prompt(synthetic_app: Path):
    at = _make_app(synthetic_app)
    _click_card(at, "SYNTH-VISION")

    assert at.session_state["selected_epic_id"] == "SYNTH-VISION"
    assert _detail_above_kanban(at, "SYNTH-VISION")
    code_values = [getattr(c, "value", "") or "" for c in at.code]
    assert any("Refinar o épico SYNTH-VISION" in v for v in code_values)


def test_click_done_card_shows_summary_no_actions(synthetic_app: Path):
    at = _make_app(synthetic_app)
    _click_card(at, "SYNTH-DONE")

    assert at.session_state["selected_epic_id"] == "SYNTH-DONE"
    assert _detail_above_kanban(at, "SYNTH-DONE")
    text = _all_text(at)
    assert "Épico implementado" in text
    code_values = [getattr(c, "value", "") or "" for c in at.code]
    # Para ✅, nenhum prompt clipboard-ready (só resumo)
    assert not any("implementa o " in v for v in code_values)
    assert not any("Refinar o épico" in v for v in code_values)


def test_close_button_clears_selection(synthetic_app: Path):
    at = _make_app(synthetic_app)
    _click_card(at, "SYNTH-DETAILED")
    assert at.session_state["selected_epic_id"] == "SYNTH-DETAILED"

    close = next((b for b in at.button if b.key == "close-detail"), None)
    assert close is not None, "botão Fechar não está visível com épico selecionado"
    close.click()
    at.run()

    assert "selected_epic_id" not in at.session_state
    md = [m.body or "" for m in at.markdown]
    assert not any(b.startswith("## SYNTH-DETAILED") for b in md)


def test_no_selection_no_detail_panel(synthetic_app: Path):
    at = _make_app(synthetic_app)
    md = [m.body or "" for m in at.markdown]
    # Sem clique, painel de detalhe não existe
    assert not any(b.startswith("## SYNTH-") for b in md)
    # Botão Fechar tampouco
    assert not any(b.key == "close-detail" for b in at.button)
