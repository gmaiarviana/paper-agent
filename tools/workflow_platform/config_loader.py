"""Carregamento de configuração da plataforma de workflow.

Lê ``tools/workflow_platform/config.yaml`` e resolve paths de ROADMAP
relativos ao repo root. Não acessa rede; GitHub `owner`/`repo` são apenas
strings usadas para montar URLs nos cards.
"""

from dataclasses import dataclass
from pathlib import Path

import yaml


REPO_ROOT_MARKER = "tools/workflow_platform"


@dataclass
class PlatformConfig:
    github_owner: str
    github_repo: str
    roadmaps: list[str]
    repo_root: Path


def _detect_repo_root(start: Path | None = None) -> Path:
    """Sobe diretórios a partir deste arquivo até encontrar o repo root.

    O repo root é identificado como o ancestral que contém ``tools/workflow_platform``.
    """
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / REPO_ROOT_MARKER).exists():
            return parent
    raise RuntimeError(
        f"Não foi possível detectar o repo root (procurando por {REPO_ROOT_MARKER})"
    )


def load_config(repo_root: Path | None = None, config_path: Path | None = None) -> PlatformConfig:
    """Carrega config.yaml e resolve roadmaps em paths absolutos.

    Args:
        repo_root: opcional, repo root para resolver paths relativos.
            Se None, é detectado a partir deste arquivo.
        config_path: opcional, caminho explícito do YAML. Default:
            ``<repo_root>/tools/workflow_platform/config.yaml``.
    """
    root = (repo_root or _detect_repo_root()).resolve()
    cfg_file = config_path or (root / "tools" / "workflow_platform" / "config.yaml")

    if not cfg_file.exists():
        raise FileNotFoundError(f"config.yaml não encontrado: {cfg_file}")

    with cfg_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    github = data.get("github") or {}
    roadmaps = data.get("roadmaps") or []

    missing: list[str] = []
    if not github.get("owner"):
        missing.append("github.owner")
    if not github.get("repo"):
        missing.append("github.repo")
    if not roadmaps:
        missing.append("roadmaps")
    if missing:
        raise ValueError(
            f"config.yaml faltando campos obrigatórios: {', '.join(missing)} (em {cfg_file})"
        )

    resolved = [str((root / r).resolve()) for r in roadmaps]

    return PlatformConfig(
        github_owner=github["owner"],
        github_repo=github["repo"],
        roadmaps=resolved,
        repo_root=root,
    )
