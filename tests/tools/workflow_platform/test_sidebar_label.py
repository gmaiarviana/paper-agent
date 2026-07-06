"""Testes do helper de label da sidebar (W-PROTO-FILA-4.3)."""

from pathlib import Path

from tools.workflow_platform.presenters import LABEL_OVERRIDES, label_for_roadmap


def test_core_roadmap_maps_to_core(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    p = repo / "docs" / "ROADMAP.md"
    assert label_for_roadmap(str(p), repo) == "Core"


def test_workflow_roadmap_maps_to_workflow(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    p = repo / "docs" / "process" / "workflow" / "ROADMAP.md"
    assert label_for_roadmap(str(p), repo) == "Workflow"


def test_product_roadmap_maps_to_capitalized_name(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    p = repo / "products" / "revelar" / "ROADMAP.md"
    assert label_for_roadmap(str(p), repo) == "Revelar"


def test_product_with_dash_in_name_uses_title_case(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    p = repo / "products" / "prisma-verbal" / "ROADMAP.md"
    assert label_for_roadmap(str(p), repo) == "Prisma Verbal"


def test_label_overrides_includes_core_and_workflow():
    assert "docs/ROADMAP.md" in LABEL_OVERRIDES
    assert "docs/process/workflow/ROADMAP.md" in LABEL_OVERRIDES


def test_path_outside_repo_falls_back_to_stem(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    outside = tmp_path / "other" / "thing.md"
    label = label_for_roadmap(str(outside), repo)
    # Stem é "thing"; título-case = "Thing"
    assert label == "Thing"


def test_unknown_path_inside_repo_falls_back_to_parent_dir_name(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    p = repo / "weird" / "place" / "ROADMAP.md"
    label = label_for_roadmap(str(p), repo)
    # parent.name = "place" → "Place"
    assert label == "Place"
