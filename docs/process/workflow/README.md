# Workflow

> Plataforma de gestão human-in-the-loop. O primeiro agente provado é o de
> **desenvolvimento de software** — construir o próprio paper-agent —, mas a
> missão é genérica: uma face conversa com o operador enquanto agentes
> especializados trabalham por baixo (ver [vision.md](vision.md)). Vive em
> `docs/process/workflow/`. Não confundir com produtos do super-sistema —
> workflow orquestra a construção, não é um produto entregue ao usuário final.

## Documentos

- [vision.md](vision.md) — missão, princípios, forma da plataforma e horizonte do workflow
- [ROADMAP.md](ROADMAP.md) — milestones e épicos do processo

## Relação com outras pastas

- `docs/process/refinement/` — subdomínio operacional: como refinamento acontece
- `docs/process/implementation/` — subdomínio operacional: guidelines de implementação aplicáveis ao fluxo único de execução
- `docs/process/autonomous/` — subdomínio operacional: fluxo único de execução via Claude Code Web
- `docs/process/sizing/` — heurística e histórico de sizing da EM Skill

Este diretório (`workflow/`) é o "meta" — missão e roadmap do processo como um todo. Dívida técnica do workflow é rastreada como épicos dentro do `ROADMAP.md` acima, não em arquivo separado.
As pastas-irmãs são as subáreas operacionais.
