"""Testes do parser de ROADMAP."""

from pathlib import Path

import pytest

from tools.workflow_platform.models import EpicState
from tools.workflow_platform.parser import parse_roadmap


SYNTHETIC_ROADMAP = """# ROADMAP — Sintético

## 🎯 Milestones

### MILESTONE-A

- **Objetivo:** primeiro milestone de teste
- **Épicos agrupados:** S-A-1, S-A-2

### MILESTONE-B

- **Objetivo:** segundo milestone
- **Épicos agrupados:** S-B-1

## 📋 Épicos

#### ÉPICO S-A-1: épico em visão

**Milestone:** `MILESTONE-A`

**Status:** 🌱 Visão

---

#### ÉPICO S-A-2: épico alinhado

**Milestone:** `MILESTONE-A`

**Status:** 🧭 Jornada alinhada

---

#### ÉPICO S-B-1: épico em revisão

**Milestone:** `MILESTONE-B`

**Branch:** `milestone/foo-bar`

**Status:** 🔀 Em revisão — PR #93 (https://github.com/gmaiarviana/paper-agent/pull/93)

---

#### ÉPICO S-NOMS-1: épico sem milestone

**Status:** 📐 Funcionalidades esboçadas

---

#### ÉPICO S-DETAILED: épico detalhado

**Milestone:** `MILESTONE-A`

**Status:** 🔍 Detalhes definidos

---

#### ÉPICO S-CRITERIA: épico em critérios

**Milestone:** `MILESTONE-A`

**Status:** 📋 Critérios definidos

---

#### ÉPICO S-IN-PROGRESS: épico em andamento

**Milestone:** `MILESTONE-B`

**Branch:** `milestone/in-progress`

**Status:** 🏗️ Em andamento

---

#### ÉPICO S-DONE: épico concluído

**Milestone:** `MILESTONE-A`

**Status:** ✅ Implementado — PR #88 (merge `abc1234`, 2026-04-20)

corpo do épico — primeira linha
mais conteúdo aqui

---

#### ÉPICO S-MALFORMED: épico sem status

**Milestone:** `MILESTONE-A`
"""


@pytest.fixture
def synthetic(tmp_path: Path) -> Path:
    p = tmp_path / "ROADMAP.md"
    p.write_text(SYNTHETIC_ROADMAP, encoding="utf-8")
    return p


def test_parses_eight_states(synthetic: Path):
    pr = parse_roadmap(synthetic)
    by_id = {e.id: e for e in pr.epics}

    assert by_id["S-A-1"].state == EpicState.VISION
    assert by_id["S-A-2"].state == EpicState.ALIGNED
    assert by_id["S-NOMS-1"].state == EpicState.SKETCHED
    assert by_id["S-CRITERIA"].state == EpicState.CRITERIA
    assert by_id["S-DETAILED"].state == EpicState.DETAILED
    assert by_id["S-IN-PROGRESS"].state == EpicState.IN_PROGRESS
    assert by_id["S-B-1"].state == EpicState.IN_REVIEW
    assert by_id["S-DONE"].state == EpicState.DONE


def test_extracts_pr_number_and_url(synthetic: Path):
    pr = parse_roadmap(synthetic)
    by_id = {e.id: e for e in pr.epics}

    in_review = by_id["S-B-1"]
    assert in_review.pr_number == 93
    assert in_review.pr_url == "https://github.com/gmaiarviana/paper-agent/pull/93"


def test_milestone_id_field_extraction(synthetic: Path):
    pr = parse_roadmap(synthetic)
    by_id = {e.id: e for e in pr.epics}

    assert by_id["S-A-1"].milestone_id == "MILESTONE-A"
    assert by_id["S-NOMS-1"].milestone_id is None


def test_branch_field_extraction(synthetic: Path):
    pr = parse_roadmap(synthetic)
    by_id = {e.id: e for e in pr.epics}

    assert by_id["S-B-1"].branch == "milestone/foo-bar"
    assert by_id["S-IN-PROGRESS"].branch == "milestone/in-progress"
    assert by_id["S-A-1"].branch is None


def test_malformed_epic_produces_warning_no_exception(synthetic: Path):
    pr = parse_roadmap(synthetic)
    ids = {e.id for e in pr.epics}
    assert "S-MALFORMED" not in ids
    assert any("S-MALFORMED" in w for w in pr.warnings)


def test_milestones_section_parsed(synthetic: Path):
    pr = parse_roadmap(synthetic)
    by_id = {m.id: m for m in pr.milestones}

    assert "MILESTONE-A" in by_id
    assert "MILESTONE-B" in by_id
    assert by_id["MILESTONE-A"].objective == "primeiro milestone de teste"
    assert "S-A-1" in by_id["MILESTONE-A"].epic_ids
    assert "S-A-2" in by_id["MILESTONE-A"].epic_ids
    assert "S-B-1" in by_id["MILESTONE-B"].epic_ids


def test_roadmap_without_milestones_section_no_warning(tmp_path: Path):
    md = """# ROADMAP — Sem milestones

## 📋 Épicos

#### ÉPICO E-1: só épicos
**Status:** 📋 Critérios definidos
"""
    p = tmp_path / "ROADMAP.md"
    p.write_text(md, encoding="utf-8")
    pr = parse_roadmap(p)

    assert pr.milestones == []
    assert pr.warnings == []
    assert len(pr.epics) == 1


def test_missing_file_returns_warning(tmp_path: Path):
    pr = parse_roadmap(tmp_path / "ausente.md")
    assert pr.epics == []
    assert pr.milestones == []
    assert any("não encontrado" in w for w in pr.warnings)


def test_body_excerpt_captured_for_done_epic(synthetic: Path):
    pr = parse_roadmap(synthetic)
    by_id = {e.id: e for e in pr.epics}
    done = by_id["S-DONE"]
    assert "corpo do épico" in done.body_excerpt
    assert len(done.body_excerpt) <= 500


def test_real_workflow_roadmap_parses_without_error():
    """Smoke test no ROADMAP real do workflow."""
    repo_root = Path(__file__).resolve().parents[3]
    pr = parse_roadmap(repo_root / "docs" / "process" / "workflow" / "ROADMAP.md")

    epic_ids = {e.id for e in pr.epics}
    # Épicos forward-looking permanecem no ROADMAP; milestones fechados têm os
    # blocos de épico removidos (só a declaração do milestone sobrevive — ledger).
    assert "W-PILOTO-UX-1" in epic_ids

    ux1 = next(e for e in pr.epics if e.id == "W-PILOTO-UX-1")
    assert ux1.state in set(EpicState)
    assert ux1.milestone_id == "PILOTO-WORKFLOW-UX"
