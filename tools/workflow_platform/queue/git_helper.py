"""Helper para listar branches do remote local.

Encapsula ``git for-each-ref`` em refs/remotes/origin/. Falhas de
subprocess são propagadas — caller (view) decide como tratar.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RemoteBranch:
    name: str
    last_commit_at: datetime


_FORMAT = "%(refname:short)|%(committerdate:iso8601)"


def _parse_iso(ts: str) -> datetime:
    """``git for-each-ref --format=...iso8601`` produz '2026-04-30 12:00:00 +0000'.

    Converte para datetime aware via ``fromisoformat`` após normalizar o
    espaço entre data e hora.
    """
    s = ts.strip().replace(" ", "T", 1)
    return datetime.fromisoformat(s)


def _strip_origin_prefix(name: str) -> str:
    if name.startswith("origin/"):
        return name[len("origin/") :]
    return name


def list_remote_branches() -> list[RemoteBranch]:
    """Lista branches do remote local via ``git for-each-ref``.

    Exclui ``origin/HEAD`` (alias). Falha de subprocess é propagada.
    """
    result = subprocess.run(
        [
            "git",
            "for-each-ref",
            f"--format={_FORMAT}",
            "refs/remotes/origin/",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    branches: list[RemoteBranch] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            raw_name, raw_ts = line.split("|", 1)
        except ValueError:
            continue
        name = _strip_origin_prefix(raw_name.strip())
        if name == "HEAD":
            continue
        try:
            ts = _parse_iso(raw_ts)
        except ValueError:
            continue
        branches.append(RemoteBranch(name=name, last_commit_at=ts))

    return branches
