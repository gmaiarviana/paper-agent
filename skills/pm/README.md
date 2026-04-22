# PM Skill (Product Manager)

> **📌 Localização:** `skills/pm/`
> **📌 Etapa do fluxo:** condicional, antes do EM — `docs/process/autonomous/workflow.md` (a ser reescrito em M4 da reforma do fluxo)
> **📌 Pré-requisito:** milestone disparado tem ao menos um épico em `🌱 Visão` ou `📐 Funcionalidades esboçadas`. Se todos os épicos do milestone já estão em `🔍 Detalhes definidos` (ou estado posterior), PM é **pulado** — fluxo segue direto para EM.

---

## 1. PAPEL

A PM Skill faz **refinamento tático** dentro da branch do milestone: leva épicos do milestone que ainda estão em `🌱` ou `📐` até `🔍 Detalhes definidos`, aplicando o checklist de [docs/process/refinement/autonomous_readiness.md](../../docs/process/refinement/autonomous_readiness.md) como programa executável.

PM **não substitui Claude Web**. As duas modalidades de refinamento são complementares, com escopos distintos:

- **Claude Web — refinamento estratégico:** quebra visão em milestones e/ou épicos em `🌱`/`📐` antes de qualquer execução. Decide o que entra na próxima onda de trabalho. Acontece **fora** da branch do milestone.
- **PM Skill — refinamento tático:** dentro da branch do milestone já disparado, fecha os detalhes de execução de épicos pendentes para que o fluxo autônomo possa proceder sem inventar. Não decide escopo nem prioridade — só amadurece o que já foi escolhido.

A regra prática: se o milestone disparado tem todos os épicos em `🔍` ou superior, PM é pulado. Se algum está em `🌱`/`📐`, PM roda nele antes de o EM medir o sizing.

---

## 2. QUANDO USAR

Use quando todas as condições abaixo forem verdadeiras:

- Milestone disparado existe em algum ROADMAP de produto (`products/<produto>/ROADMAP.md`).
- Branch `milestone/<id-em-caixa-baixa>` existe e está ativa.
- Pelo menos um épico do milestone (no produto OU em `docs/ROADMAP.md` via tabela "Épicos Core × Milestones de Produto") está em `🌱 Visão` ou `📐 Funcionalidades esboçadas`.

**Não usar se:**
- ❌ Todos os épicos do milestone já estão em `🔍 Detalhes definidos` ou superior — pular para EM.
- ❌ Milestone ainda não existe no ROADMAP — refinamento estratégico via Claude Web é pré-requisito.
- ❌ Há decisão arquitetural em aberto que PM não pode resolver consultando docs — devolver ao dev.

---

## 3. COMO FUNCIONA

A skill executa, em ordem:

1. **Pré-checagens** — branch correta, milestone existe, há ao menos um épico pré-`🔍` no milestone.
2. **Identificar épicos a refinar** — listar do ROADMAP do produto + épicos core consumidos pelo milestone (via tabela em `docs/ROADMAP.md`).
3. **Aplicar o checklist por épico** — para cada épico pendente, percorrer as 5 categorias de [autonomous_readiness.md](../../docs/process/refinement/autonomous_readiness.md): termos e conceitos; dados e contratos; código-alvo e integração; acoplamentos; sequência e testes.
4. **Ajustar profundidade pelo estágio** — POC tolera simplificações declaradas; Protótipo e MVP exigem o checklist integral.
5. **Detectar ambiguidades e resolver via consulta** — antes de perguntar ao dev, buscar nos docs (CONTEXT_INDEX → tema → spec) e em código análogo.
6. **Bloco único de perguntas** — se sobrar ambiguidade real após consulta, PARAR e devolver ao dev em formato único, sem fragmentar.
7. **Atualizar ROADMAPs** — escrever os detalhes de execução em cada épico refinado, marcar como `🔍 Detalhes definidos`.
8. **Commitar na branch do milestone** — um commit (ou poucos) cobrindo as atualizações de ROADMAP. Atualizar `current_implementation.md` com evidência de carregamento e o que foi refinado.

**Princípio:** PM **não implementa código**, **não cria épicos novos**, **não decide escopo**. Só amadurece os épicos que já estão no milestone.

---

## 4. INPUT ESPERADO

- `<id do milestone>` (ex.: `POC-ENSAIO`) e o ROADMAP de produto correspondente
- Branch `milestone/<id-em-caixa-baixa>` ativa
- `docs/process/refinement/autonomous_readiness.md` como spec do checklist
- Acesso aos arquivos do repo via Claude Code Web

---

## 5. OUTPUT PRODUZIDO

- ✅ Cada épico do milestone que estava em `🌱`/`📐` agora está em `🔍 Detalhes definidos` (ou foi devolvido ao dev como bloqueio explícito)
- ✅ ROADMAPs atualizados com os detalhes de execução por funcionalidade (arquivos-alvo, contratos, integração, acoplamentos, escopo de teste)
- ✅ `current_implementation.md` atualizado com evidência de carregamento PM e resumo do refinamento
- ✅ Commit na branch do milestone documentando o trabalho

**Não produz:**
- ❌ Código (escopo do Dev)
- ❌ Plano de tasks (escopo do Scrum Master)
- ❌ Decisão de sizing (escopo do EM)
- ❌ Épicos novos ou mudança de escopo do milestone

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Próxima ação |
|---------|--------------|
| Todos os épicos refinados a `🔍` | Fluxo segue para **EM Skill** (sizing) |
| Sobraram dúvidas após consulta | PARA e devolve ao dev em bloco único |
| 3 rejeições consecutivas no mesmo épico | Aplicar `docs/process/implementation/blockers.md` |

PM **não devolve** para Claude Web. Se um épico não puder ser refinado por falta de visão, PM marca como bloqueio e devolve ao dev humano — que pode reabrir refinamento estratégico via Claude Web.

---

## 7. RELAÇÃO COM CLAUDE WEB

Reforço explícito: **PM e Claude Web são complementares, não excludentes**.

- Claude Web continua sendo a única origem de quebrar visão em milestones e de propor mudança de escopo.
- PM aceita o escopo dado e fecha os detalhes que faltam para a execução autônoma proceder.
- O dev humano pode optar por refinar manualmente via Claude Web mesmo que PM pudesse refinar — fica a critério. Mas se o dispatch autônomo pediu execução com épicos pré-`🔍`, PM atua.

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Checklist consumido → [docs/process/refinement/autonomous_readiness.md](../../docs/process/refinement/autonomous_readiness.md)
- Princípio constitucional → [docs/CONSTITUTION.md §2 e §9](../../docs/CONSTITUTION.md)
- Próximo gate → [skills/em/README.md](../em/README.md)
