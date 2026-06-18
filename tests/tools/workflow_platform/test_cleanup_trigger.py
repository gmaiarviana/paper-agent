"""Testes do trigger de cleanup (W-PROTO-17.1) — resolução do milestone via ROADMAP."""

import pytest

from tools.workflow_platform.cleanup_trigger import (
    PendingCleanup,
    list_pending_cleanups,
    main,
    resolve_milestone_for_merged_pr,
)


def _roadmap(*epic_blocks: str) -> str:
    return "# ROADMAP — Sintético\n\n## 📋 Épicos\n\n" + "\n\n".join(epic_blocks) + "\n"


def _epic(epic_id: str, milestone: str, status: str) -> str:
    return (
        f"#### ÉPICO {epic_id}: épico de teste\n\n"
        f"**Milestone:** `{milestone}`\n\n"
        f"**Status:** {status}"
    )


IN_REVIEW = "🔀 Em revisão — PR #{n} (https://github.com/o/r/pull/{n})"
DONE = "✅ Implementado"


def _write(tmp_path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_resolve_returns_milestone_when_epics_in_review_match_pr(tmp_path):
    """AC1: ≥1 épico em 🔀 com pr_number == N e milestone_id concordante."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(
            _epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42)),
            _epic("W-X-2", "MILESTONE-X", IN_REVIEW.format(n=42)),
        ),
    )
    assert resolve_milestone_for_merged_pr(42, [path]) == "MILESTONE-X"


def test_resolve_returns_none_when_no_epic_matches_pr(tmp_path):
    """AC2: nenhum épico em 🔀 casa o número → None (PR fora do fluxo)."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42))),
    )
    assert resolve_milestone_for_merged_pr(99, [path]) is None


def test_resolve_raises_when_milestones_diverge(tmp_path):
    """AC3: épicos casados em milestones distintos → ValueError."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(
            _epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42)),
            _epic("W-Y-1", "MILESTONE-Y", IN_REVIEW.format(n=42)),
        ),
    )
    with pytest.raises(ValueError):
        resolve_milestone_for_merged_pr(42, [path])


def test_resolve_raises_when_matched_epic_lacks_milestone(tmp_path):
    """AC3 (segundo ramo): épico em 🔀 casado mas sem **Milestone:** → ValueError."""
    epic_sem_milestone = (
        "#### ÉPICO W-Z-1: épico sem campo de milestone\n\n"
        f"**Status:** {IN_REVIEW.format(n=55)}"
    )
    path = _write(tmp_path, "ROADMAP.md", _roadmap(epic_sem_milestone))
    with pytest.raises(ValueError):
        resolve_milestone_for_merged_pr(55, [path])


def test_resolve_ignores_done_epics_with_same_pr(tmp_path):
    """AC4: épico já em ✅ com o mesmo PR #N não casa → idempotência."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(
            _epic("W-X-1", "MILESTONE-X", DONE),
            _epic("W-X-2", "MILESTONE-X", DONE),
        ),
    )
    # PR #42 já foi limpa (épicos em ✅); o status ✅ não carrega pr_number,
    # então nada casa e o re-trigger não re-limpa.
    assert resolve_milestone_for_merged_pr(42, [path]) is None


def test_resolve_scans_multiple_roadmaps(tmp_path):
    """O join varre todos os ROADMAPs configurados; ausente vira no-op."""
    present = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=7))),
    )
    missing = str(tmp_path / "inexistente" / "ROADMAP.md")
    assert resolve_milestone_for_merged_pr(7, [missing, present]) == "MILESTONE-X"


def test_cli_prints_milestone_and_exits_zero(tmp_path, monkeypatch, capsys):
    """AC5: CLI imprime milestone_id em stdout e sai 0."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42))),
    )

    class _Cfg:
        roadmaps = [path]

    monkeypatch.setattr(
        "tools.workflow_platform.cleanup_trigger.load_config", lambda: _Cfg()
    )
    assert main(["42"]) == 0
    assert capsys.readouterr().out.strip() == "MILESTONE-X"


def test_cli_prints_empty_when_no_match(tmp_path, monkeypatch, capsys):
    """AC5: CLI imprime string vazia quando a PR não é de milestone."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42))),
    )

    class _Cfg:
        roadmaps = [path]

    monkeypatch.setattr(
        "tools.workflow_platform.cleanup_trigger.load_config", lambda: _Cfg()
    )
    assert main(["99"]) == 0
    assert capsys.readouterr().out.strip() == ""


def test_cli_rejects_bad_args():
    """CLI valida argumentos: número errado de args ou pr_number inválido."""
    assert main([]) == 2
    assert main(["a", "b"]) == 2
    assert main(["nao-numero"]) == 2


# ----- list_pending_cleanups (fold-in) -----

def test_list_pending_returns_one_per_milestone_in_review(tmp_path):
    """Faxina pendente = milestone com épicos em 🔀 (PR mergeada, por invariante)."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(
            _epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42)),
            _epic("W-X-2", "MILESTONE-X", IN_REVIEW.format(n=42)),
            _epic("W-Y-1", "MILESTONE-Y", IN_REVIEW.format(n=7)),
        ),
    )
    pending = list_pending_cleanups([path])
    assert pending == [
        PendingCleanup(
            milestone_id="MILESTONE-Y",
            pr_number=7,
            pr_url="https://github.com/o/r/pull/7",
        ),
        PendingCleanup(
            milestone_id="MILESTONE-X",
            pr_number=42,
            pr_url="https://github.com/o/r/pull/42",
        ),
    ]


def test_list_pending_excludes_done_epics(tmp_path):
    """Épico já enxuto (✅) não reaparece — idempotência do fold-in."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(
            _epic("W-X-1", "MILESTONE-X", DONE),
            _epic("W-Y-1", "MILESTONE-Y", IN_REVIEW.format(n=7)),
        ),
    )
    pending = list_pending_cleanups([path])
    assert [p.milestone_id for p in pending] == ["MILESTONE-Y"]


def test_list_pending_empty_when_nothing_in_review(tmp_path):
    """Sem épicos em 🔀 → nenhuma faxina pendente."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", DONE)),
    )
    assert list_pending_cleanups([path]) == []


def test_list_pending_scans_multiple_roadmaps(tmp_path):
    """Varre todos os ROADMAPs configurados; ausente vira no-op."""
    present = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42))),
    )
    missing = str(tmp_path / "inexistente" / "ROADMAP.md")
    pending = list_pending_cleanups([missing, present])
    assert [p.milestone_id for p in pending] == ["MILESTONE-X"]


def test_list_pending_propagates_inconsistent_milestone(tmp_path):
    """Mesma PR casando milestones distintos → ValueError (não adivinha)."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(
            _epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42)),
            _epic("W-Y-1", "MILESTONE-Y", IN_REVIEW.format(n=42)),
        ),
    )
    with pytest.raises(ValueError):
        list_pending_cleanups([path])


def test_cli_list_prints_pending(tmp_path, monkeypatch, capsys):
    """`--list` imprime uma linha por faxina pendente e sai 0."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", IN_REVIEW.format(n=42))),
    )

    class _Cfg:
        roadmaps = [path]

    monkeypatch.setattr(
        "tools.workflow_platform.cleanup_trigger.load_config", lambda: _Cfg()
    )
    assert main(["--list"]) == 0
    out = capsys.readouterr().out.strip()
    assert out == "MILESTONE-X\t42\thttps://github.com/o/r/pull/42"


def test_cli_list_empty_prints_nothing(tmp_path, monkeypatch, capsys):
    """`--list` sem faxinas pendentes imprime nada e sai 0."""
    path = _write(
        tmp_path,
        "ROADMAP.md",
        _roadmap(_epic("W-X-1", "MILESTONE-X", DONE)),
    )

    class _Cfg:
        roadmaps = [path]

    monkeypatch.setattr(
        "tools.workflow_platform.cleanup_trigger.load_config", lambda: _Cfg()
    )
    assert main(["--list"]) == 0
    assert capsys.readouterr().out.strip() == ""
