"""Parser defensivo de ROADMAP markdown.

Reconhece blocos de épico (``#### ÉPICO <id>: <title>``) e milestones
declarados sob ``## 🎯 Milestones``. Tolera malformação: épico sem
``**Status:**`` vira warning e é ignorado; ROADMAP sem seção de
milestones devolve ``milestones=[]`` sem warning.
"""

import re
from pathlib import Path

from .models import Epic, EpicState, Milestone, ParsedRoadmap


_STATE_BY_EMOJI: dict[str, EpicState] = {s.value: s for s in EpicState}

# 🏗️ é "🏗" + "️" (variation selector). Aceitar ambas as formas.
_STATE_ALIASES: dict[str, EpicState] = {
    "🏗": EpicState.IN_PROGRESS,
    "🏗️": EpicState.IN_PROGRESS,
}

_EPIC_HEADER_RE = re.compile(
    r"^#{2,4}\s*(?:✅\s+)?ÉPICO\s+(?P<id>[A-Za-z0-9][A-Za-z0-9-]*):\s*(?P<title>.+?)\s*$"
)
_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s+(?P<rest>.+?)\s*$")
_MILESTONE_FIELD_RE = re.compile(r"^\*\*Milestone:\*\*\s+`?(?P<id>[A-Za-z0-9][A-Za-z0-9-]*)`?")
_BRANCH_FIELD_RE = re.compile(r"^\*\*Branch:\*\*\s+`?(?P<branch>[^`\n]+?)`?\s*$")
_PR_NUMBER_RE = re.compile(r"PR\s+#(?P<n>\d+)")
_PR_URL_RE = re.compile(r"(?P<url>https?://[^\s)\]]+)")

_MILESTONES_HEADING_RE = re.compile(r"^##\s+🎯\s+Milestones\s*$")
_TOP_LEVEL_HEADING_RE = re.compile(r"^##\s+(?!#)")
_MILESTONE_BLOCK_RE = re.compile(
    r"^###\s+(?P<id>[A-Z][A-Z0-9-]*)\s*$"
)
_MILESTONE_OBJECTIVE_RE = re.compile(r"^-\s*\*\*Objetivo:\*\*\s*(?P<text>.+?)\s*$")
_MILESTONE_EPICS_FIELD_RE = re.compile(r"\*\*Épicos agrupados:\*\*\s*(?P<list>.+)$")
_EPIC_ID_TOKEN_RE = re.compile(r"[A-Z][A-Z0-9-]*-\d+(?:[A-Z]+(?:-\d+)?)?|[CWE]-[A-Z]+-\d+")


def _classify_status(rest: str) -> EpicState | None:
    """Pega o emoji do estado a partir da linha **Status:**."""
    stripped = rest.lstrip()
    for emoji, state in _STATE_BY_EMOJI.items():
        if stripped.startswith(emoji):
            return state
    for alias, state in _STATE_ALIASES.items():
        if stripped.startswith(alias):
            return state
    return None


def _extract_pr(rest: str) -> tuple[int | None, str | None]:
    n_match = _PR_NUMBER_RE.search(rest)
    pr_number = int(n_match.group("n")) if n_match else None
    url_match = _PR_URL_RE.search(rest)
    pr_url = url_match.group("url") if url_match else None
    return pr_number, pr_url


def _parse_milestones(lines: list[str]) -> tuple[list[Milestone], dict[str, str]]:
    """Lê blocos sob ``## 🎯 Milestones``. Devolve milestones e mapa
    ``epic_id -> milestone_id`` declarado via campo ``**Épicos agrupados:**``.
    """
    milestones: list[Milestone] = []
    epic_to_milestone: dict[str, str] = {}

    in_section = False
    current: Milestone | None = None
    objective_pending = True

    for line in lines:
        if _MILESTONES_HEADING_RE.match(line):
            in_section = True
            continue
        if not in_section:
            continue
        if _TOP_LEVEL_HEADING_RE.match(line):
            break

        m = _MILESTONE_BLOCK_RE.match(line)
        if m:
            current = Milestone(id=m.group("id"), roadmap_path="")
            milestones.append(current)
            objective_pending = True
            continue

        if current is None:
            continue

        if objective_pending:
            obj = _MILESTONE_OBJECTIVE_RE.match(line)
            if obj:
                current.objective = obj.group("text").rstrip()
                objective_pending = False

        epics_field = _MILESTONE_EPICS_FIELD_RE.search(line)
        if epics_field:
            for token in _EPIC_ID_TOKEN_RE.findall(epics_field.group("list")):
                if token not in current.epic_ids:
                    current.epic_ids.append(token)
                epic_to_milestone.setdefault(token, current.id)

    return milestones, epic_to_milestone


def _parse_epics(
    lines: list[str],
    roadmap_path: str,
    epic_to_milestone: dict[str, str],
    warnings: list[str],
) -> list[Epic]:
    """Lê blocos `#### ÉPICO <id>: <title>` e campos seguintes."""
    epics: list[Epic] = []

    n = len(lines)
    i = 0
    while i < n:
        line = lines[i]
        m = _EPIC_HEADER_RE.match(line)
        if not m:
            i += 1
            continue

        epic_id = m.group("id")
        title = m.group("title").rstrip(" ✅").strip()
        block_start = i + 1

        # Bloco do épico vai até o próximo épico/milestone-section ou separador
        # Estes ROADMAPs usam `---` como separador de épico.
        block_end = n
        for j in range(block_start, n):
            ln = lines[j]
            if (
                _EPIC_HEADER_RE.match(ln)
                or _TOP_LEVEL_HEADING_RE.match(ln)
                or ln.strip() == "---"
            ):
                block_end = j
                break

        body_lines = lines[block_start:block_end]

        status_state: EpicState | None = None
        raw_status = ""
        milestone_id: str | None = None
        branch: str | None = None
        pr_number: int | None = None
        pr_url: str | None = None

        for bl in body_lines:
            if not raw_status:
                sm = _STATUS_RE.match(bl)
                if sm:
                    raw_status = bl.rstrip()
                    rest = sm.group("rest")
                    status_state = _classify_status(rest)
                    pr_number, pr_url = _extract_pr(rest)
                    continue
            if milestone_id is None:
                mm = _MILESTONE_FIELD_RE.match(bl)
                if mm:
                    milestone_id = mm.group("id")
                    continue
            if branch is None:
                bm = _BRANCH_FIELD_RE.match(bl)
                if bm:
                    branch = bm.group("branch").strip()

        if status_state is None:
            warnings.append(
                f"épico sem **Status:** reconhecido em {roadmap_path}: ÉPICO {epic_id}"
            )
            i = block_end
            continue

        if milestone_id is None:
            milestone_id = epic_to_milestone.get(epic_id)

        body_excerpt = "\n".join(body_lines).strip()[:500]

        epics.append(
            Epic(
                id=epic_id,
                title=title,
                state=status_state,
                roadmap_path=roadmap_path,
                milestone_id=milestone_id,
                branch=branch,
                pr_number=pr_number,
                pr_url=pr_url,
                raw_status_line=raw_status,
                body_excerpt=body_excerpt,
            )
        )

        i = block_end

    return epics


def parse_roadmap(path: str | Path) -> ParsedRoadmap:
    """Lê um ROADMAP markdown e devolve épicos + milestones encontrados.

    Tolera arquivo ausente: devolve ParsedRoadmap vazio com warning.
    """
    path_str = str(path)
    p = Path(path)

    if not p.exists():
        return ParsedRoadmap(
            path=path_str,
            warnings=[f"ROADMAP não encontrado: {path_str}"],
        )

    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        return ParsedRoadmap(
            path=path_str,
            warnings=[f"falha ao ler ROADMAP {path_str}: {exc}"],
        )

    lines = text.splitlines()
    warnings: list[str] = []

    milestones, epic_to_milestone = _parse_milestones(lines)
    for ms in milestones:
        ms.roadmap_path = path_str

    epics = _parse_epics(lines, path_str, epic_to_milestone, warnings)

    return ParsedRoadmap(
        path=path_str,
        epics=epics,
        milestones=milestones,
        warnings=warnings,
    )
