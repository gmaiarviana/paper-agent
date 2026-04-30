"""Preferências persistidas localmente (W-PROTO-FILA-4.1 + 4.2).

JSON git-ignored em ``tools/workflow_platform/.preferences.json``.
Falha de leitura cai pra defaults; falha de parsing levanta
``PreferencesLoadError`` para o caller decidir warning + fallback.

Premissa: 1 operador por projeto. Cross-clone fica fora do Protótipo.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from tools.workflow_platform.models import ParsedRoadmap


PREFERENCES_FILENAME = ".preferences.json"
DEFAULT_STALE_THRESHOLD_DAYS = 7


class PreferencesLoadError(Exception):
    """Levantada quando o arquivo existe mas é malformado."""


@dataclass(frozen=True)
class Preferences:
    visible_roadmaps: list[str] | None = None
    stale_branch_threshold_days: int = DEFAULT_STALE_THRESHOLD_DAYS


def _preferences_path(repo_root: Path) -> Path:
    return repo_root / "tools" / "workflow_platform" / PREFERENCES_FILENAME


def load_preferences(repo_root: Path) -> Preferences:
    """Lê preferences.json. Arquivo ausente ⇒ defaults sem warning.

    Arquivo presente mas malformado ⇒ levanta ``PreferencesLoadError``.
    Caller (app.py) captura, cai pra defaults e exibe aviso.
    """
    path = _preferences_path(repo_root)
    if not path.exists():
        return Preferences()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise PreferencesLoadError(f"falha ao ler {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PreferencesLoadError(
            f"{path}: esperado objeto JSON, recebido {type(data).__name__}"
        )

    vr = data.get("visible_roadmaps")
    if vr is not None and not (
        isinstance(vr, list) and all(isinstance(x, str) for x in vr)
    ):
        raise PreferencesLoadError(
            f"{path}: visible_roadmaps deve ser lista de strings ou null"
        )

    td = data.get("stale_branch_threshold_days", DEFAULT_STALE_THRESHOLD_DAYS)
    if not isinstance(td, int) or isinstance(td, bool) or td < 1:
        raise PreferencesLoadError(
            f"{path}: stale_branch_threshold_days deve ser int >= 1"
        )

    return Preferences(visible_roadmaps=vr, stale_branch_threshold_days=td)


def save_preferences(prefs: Preferences, repo_root: Path) -> None:
    """Grava prefs atomicamente (tmp + os.replace)."""
    path = _preferences_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    serialized = json.dumps(asdict(prefs), indent=2, sort_keys=True)
    tmp.write_text(serialized, encoding="utf-8")
    os.replace(tmp, path)


def apply_visibility_filter(
    roadmaps: list[ParsedRoadmap],
    prefs: Preferences,
    repo_root: Path,
) -> list[ParsedRoadmap]:
    """Filtra roadmaps conforme ``prefs.visible_roadmaps``.

    - ``None`` ⇒ retorna lista intacta (compatibilidade com sem-prefs).
    - lista ⇒ filtra por path relativo ao ``repo_root``.
    - lista vazia ⇒ retorna ``[]`` (operador desmarcou tudo).
    - paths fora do ``repo_root`` são ignorados silenciosamente.
    """
    if prefs.visible_roadmaps is None:
        return roadmaps
    visible = set(prefs.visible_roadmaps)
    result: list[ParsedRoadmap] = []
    for r in roadmaps:
        try:
            rel = str(Path(r.path).relative_to(repo_root))
        except ValueError:
            continue
        if rel in visible:
            result.append(r)
    return result
