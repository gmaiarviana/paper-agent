"""Fixture de WorldState sintético para testes de determinismo.

Cria 2 ROADMAPs sintéticos (1 com milestone apto a DISPATCH, 1 com
épicos em 🔀 pareados a PR) + 4 branches mockadas (2 stale, 1 ativa,
1 referenciada por épico em 🏗️) + ``now`` cravado.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from tools.workflow_platform.models import (
    Epic,
    EpicState,
    Milestone,
    ParsedRoadmap,
)
from tools.workflow_platform.job_queue.detect import WorldState
from tools.workflow_platform.job_queue.git_helper import RemoteBranch


SNAPSHOT_NOW = datetime(2026, 4, 29, 12, 0, 0)
SNAPSHOT_THRESHOLD_DAYS = 7


def make_world_state_fixture() -> WorldState:
    """Estado fixo, reproduzível, com 3 itens esperados na fila.

    Itens esperados produzidos por ``detect_all_items``:
        1. DISPATCH em ``MIL-DISPATCH`` (3 épicos em 🔍)
        2. REVIEW para PR #91 (2 épicos em 🔀 pareados)
        3. STALE_BRANCH para ``claude/abandoned`` (10 dias sem commit)
    """
    roadmap_a_path = "synthetic/roadmap-a.md"
    roadmap_b_path = "synthetic/roadmap-b.md"

    # ROADMAP A — milestone apto a DISPATCH
    epics_a = [
        Epic(
            id="S-DISPATCH-1",
            title="primeiro épico apto",
            state=EpicState.DETAILED,
            roadmap_path=roadmap_a_path,
            milestone_id="MIL-DISPATCH",
        ),
        Epic(
            id="S-DISPATCH-2",
            title="segundo épico apto",
            state=EpicState.DETAILED,
            roadmap_path=roadmap_a_path,
            milestone_id="MIL-DISPATCH",
        ),
        Epic(
            id="S-DISPATCH-3",
            title="terceiro épico apto",
            state=EpicState.DETAILED,
            roadmap_path=roadmap_a_path,
            milestone_id="MIL-DISPATCH",
        ),
    ]
    roadmap_a = ParsedRoadmap(
        path=roadmap_a_path,
        epics=epics_a,
        milestones=[
            Milestone(
                id="MIL-DISPATCH",
                roadmap_path=roadmap_a_path,
                objective="milestone apto a dispatch",
                epic_ids=["S-DISPATCH-1", "S-DISPATCH-2", "S-DISPATCH-3"],
            ),
        ],
    )

    # ROADMAP B — milestone com 2 épicos em 🔀 pareados a PR #91 + 1 épico
    # em 🏗️ que referencia uma branch (deve excluir essa branch do STALE).
    pr_url = "https://github.com/example/paper-agent/pull/91"
    epics_b = [
        Epic(
            id="S-REVIEW-1",
            title="primeiro em revisão",
            state=EpicState.IN_REVIEW,
            roadmap_path=roadmap_b_path,
            milestone_id="MIL-REVIEW",
            pr_number=91,
            pr_url=pr_url,
        ),
        Epic(
            id="S-REVIEW-2",
            title="segundo em revisão",
            state=EpicState.IN_REVIEW,
            roadmap_path=roadmap_b_path,
            milestone_id="MIL-REVIEW",
            pr_number=91,
            pr_url=pr_url,
        ),
        Epic(
            id="S-WORKING",
            title="em andamento",
            state=EpicState.IN_PROGRESS,
            roadmap_path=roadmap_b_path,
            milestone_id="MIL-WORKING",
            branch="claude/active-work",
        ),
    ]
    roadmap_b = ParsedRoadmap(
        path=roadmap_b_path,
        epics=epics_b,
        milestones=[
            Milestone(
                id="MIL-REVIEW",
                roadmap_path=roadmap_b_path,
                objective="milestone em revisão",
                epic_ids=["S-REVIEW-1", "S-REVIEW-2"],
            ),
            Milestone(
                id="MIL-WORKING",
                roadmap_path=roadmap_b_path,
                objective="milestone em andamento",
                epic_ids=["S-WORKING"],
            ),
        ],
    )

    # Branches:
    #   - claude/abandoned: 10 dias atrás → STALE
    #   - claude/old-orphan: 30 dias atrás → STALE (mas só verificamos o
    #     primeiro no snapshot pra simplificar o expected — manter ele só
    #     na variação de testes ad hoc; aqui deixamos fora para ter
    #     exatamente 1 STALE no snapshot)
    #   - claude/recent: 3 dias atrás → ativa, não-stale
    #   - claude/active-work: 20 dias atrás MAS referenciada por S-WORKING
    #     em 🏗️ → excluída
    #   - main: sempre excluída
    branches = [
        RemoteBranch(
            name="claude/abandoned",
            last_commit_at=SNAPSHOT_NOW - timedelta(days=10),
        ),
        RemoteBranch(
            name="claude/recent",
            last_commit_at=SNAPSHOT_NOW - timedelta(days=3),
        ),
        RemoteBranch(
            name="claude/active-work",
            last_commit_at=SNAPSHOT_NOW - timedelta(days=20),
        ),
        RemoteBranch(
            name="main",
            last_commit_at=SNAPSHOT_NOW - timedelta(days=999),
        ),
    ]

    return WorldState(
        roadmaps=[roadmap_a, roadmap_b],
        remote_branches=branches,
        now=SNAPSHOT_NOW,
    )
