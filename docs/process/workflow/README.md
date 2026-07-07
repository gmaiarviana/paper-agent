# Workflow

> **O que é:** o processo/plataforma pelo qual o paper-agent é construído.
> Hoje, uma plataforma de gestão human-in-the-loop cujo primeiro agente
> provado é o de **desenvolvimento de software** — uma face conversa com o
> operador enquanto agentes especializados trabalham por baixo (visão
> completa em [vision.md](vision.md)).
>
> **Onde vive:** `docs/process/workflow/`. Quando o operador fala "o
> workflow", é aqui que o contexto mora.
>
> **Não confundir:** workflow **é processo/plataforma, não produto**
> (atualmente) — não é um dos produtos do super-sistema (Revelar, Ensaio,
> Prisma Verbal, ...); é o que os constrói. (A própria plataforma pode um
> dia se separar do agente de dev em produtos distintos — ver "Horizonte"
> na visão.)

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
