# Autonomous Dispatch

> **📌 Uso:** dispare o fluxo autônomo em [claude.ai/code](https://claude.ai/code) sobre o repositório `paper-agent` com uma frase em linguagem natural que identifique o **milestone** alvo.
> **📌 Pré-requisito:** o milestone alvo existe no ROADMAP do produto (seção `## 🎯 Milestones`). Épicos em `🌱 Visão`, `🧭 Jornada alinhada` ou `📐 Funcionalidades esboçadas` são refinados pela PM skill dentro da branch; épicos em `🔍 Detalhes definidos` seguem direto.
> **📌 Documentação completa:** `docs/process/autonomous/`

---

## COMO DISPARAR

O dispatch autônomo é **invocado em linguagem natural**. Não há template rígido. O dev escreve algo como:

- "implementa a POC do Ensaio"
- "roda POC-ENSAIO"
- "dispara o MVP-REVELAR"
- "executa PROTO-ENSAIO-ALPHA"
- "toca o milestone POC-ENSAIO"

Claude Code Web identifica o milestone pelo texto e carrega o fluxo correspondente.

---

## COMO CLAUDE CODE WEB INTERPRETA (parser informal)

Ao receber a frase de dispatch, seguir este parser:

### 1. Identificar o id do milestone

Procurar, em ordem de prioridade:

1. **Id literal** no formato `<ESTAGIO>-<PRODUTO>[-SUFIXO]` em caixa alta (ex.: `POC-ENSAIO`, `PROTO-REVELAR`, `MVP-ENSAIO`, `POC-ENSAIO-ALPHA`). Se encontrado, é o milestone alvo.
2. **Combinação estágio + produto** em prosa (ex.: "POC do Ensaio", "MVP do Revelar", "Protótipo do Ensaio"). Mapear:
   - "POC" → `POC`; "Protótipo"/"proto" → `PROTO`; "MVP" → `MVP`
   - Produto pelo nome em caixa baixa do diretório em `products/` (ex.: "Ensaio" → `ENSAIO`, "Revelar" → `REVELAR`)
   - Resultado: `<ESTAGIO>-<PRODUTO>` (ex.: `POC-ENSAIO`). Se o ROADMAP do produto tiver sufixos (`-ALPHA`, `-BETA`), perguntar qual, salvo se a frase identificar explicitamente.

Se o parser não conseguir identificar um id único, **abortar** e pedir ao dev para explicitar o id (ex.: "quis dizer `POC-ENSAIO` ou `POC-ENSAIO-ALPHA`?").

### 2. Localizar o milestone no ROADMAP

Buscar em `products/<produto>/ROADMAP.md` → seção `## 🎯 Milestones` → subseção `### <ID>`. Se não existir entrada para o id, **abortar** — milestone precisa estar declarado no ROADMAP antes do dispatch.

Extrair do bloco do milestone:
- **Objetivo:** (texto literal)
- **Épicos agrupados:** lista de ids (ex.: `E-POC-1, E-POC-2, E-POC-3`)
- **Estágio:** POC / Protótipo / MVP
- **Branch associada:** `milestone/<id-em-caixa-baixa>`
- **Status dos épicos:** resumo textual

### 3. Identificar estado inicial do fluxo

Com base nos épicos agrupados:

- Todos em `🔍 Detalhes definidos` → **PM skill é pulada**; fluxo começa em EM.
- Algum em `🌱 Visão`, `🧭 Jornada alinhada` ou `📐 Funcionalidades esboçadas` → **PM skill é obrigatória** antes de EM (refinamento tático dentro da branch).
- Algum em `📋 Critérios definidos` → PM skill também é obrigatória (leva de `📋` a `🔍`).
- Épico em `🏗️ Em andamento` ou `✅ Implementado` no meio do milestone → **abortar**, pedir ao dev confirmação (pode indicar milestone mal-sinalizado ou retomada de trabalho).

### 4. Preparar branch

- Checar se `milestone/<id-em-caixa-baixa>` já existe no remote. Se sim, usar; se não, criar a partir de `main`.
- `main` nunca recebe commits do fluxo; todos os commits caem na branch do milestone.

### 5. Carregar skills em sequência

Carregar `skill.md` na ordem aplicável, seguindo integralmente (não resumir, não adaptar):

```
PM (se aplicável) → EM → Scrum Master → Dev → QA → TL → PO → RTE
```

Protocolo detalhado em `skills/README.md`.

---

## CONTEXTO OBRIGATÓRIO QUE CLAUDE CODE WEB LÊ ANTES DE INICIAR

1. `docs/CONSTITUTION.md`
2. `docs/ARCHITECTURE.md`
3. `docs/process/refinement/planning_guidelines.md`
4. `products/<produto>/ROADMAP.md` — incluindo seção `## 🎯 Milestones`
5. `docs/process/autonomous/workflow.md`
6. `docs/process/autonomous/session_conventions.md`
7. `docs/process/implementation/` (guidelines reaproveitadas)
8. `docs/CONTEXT_INDEX.md`
9. `skills/README.md`
10. `docs/process/sizing/heuristic.md` (para a EM skill)
11. `docs/process/sizing/schema.md` (para a EM skill)

---

## RESTRIÇÕES DO FLUXO AUTÔNOMO

- **Escopo:** fluxo opera sobre o **milestone inteiro**. Commits vão para `milestone/<id>`; `main` recebe o milestone apenas após aval humano explícito.
- **Refinamento estratégico não acontece aqui.** Visão → milestones/épicos em `🌱`/`🧭`/`📐` é Claude Web, externo ao repo. Se o milestone alvo não existir no ROADMAP, abortar.
- **Refinamento tático acontece dentro da branch.** PM skill leva épicos `🌱`/`🧭`/`📐`/`📋` a `🔍` antes da EM rodar o sizing.
- **Sem novas decisões arquiteturais.** Se o fluxo topar decisão em aberto não coberta por refinamento, abortar e devolver.
- **Sem PR automático.** A RTE prepara a branch e comandos; o PR é criação humana.
- **Escalação:** 3 reprovações consecutivas no mesmo gate do mesmo épico abortam o milestone inteiro e notificam o dev (sem agregar entre épicos distintos).
- **Notificação única no fim.** Gates intermediários são silenciosos; a RTE consolida tudo em uma mensagem só quando o último épico fecha.

---

## ENTRADA VS SAÍDA

| Momento | Quem | Faz |
|---------|------|-----|
| Dispatch | Dev | Frase em linguagem natural identifica o milestone |
| Parsing | Claude Code Web | Extrai id, localiza no ROADMAP, escolhe ponto de entrada |
| PM (condicional) | skill | Refina épicos `🌱`/`🧭`/`📐`/`📋` até `🔍` dentro da branch |
| EM | skill | Sizing FIT/TIGHT/OVERFLOW; OVERFLOW devolve ao dev |
| Scrum Master | skill | Cria `docs/process/current_implementation.md` no shape aninhado do milestone |
| Loop por épico | Dev + QA + TL + PO | Implementa e valida funcionalidade por funcionalidade em cada épico |
| RTE | skill | Fecha o milestone, publica a branch, consolida relatório |
| Validação | Dev | Lê relatório, roda comandos de validação, cria PR se OK |

---

## CHECKLIST ANTES DE DISPARAR

- [ ] Milestone alvo existe no ROADMAP do produto (seção `## 🎯 Milestones`)
- [ ] Objetivo do milestone está preenchido (não vazio)
- [ ] Épicos agrupados estão listados pelo id e existem em `## 📋 Épicos Planejados` do mesmo ROADMAP
- [ ] Nenhum épico do milestone está em `✅ Implementado` (milestone não foi parcialmente consumido)
- [ ] `docs/process/current_implementation.md` **não existe** (milestone anterior finalizado)
- [ ] Dependências de core declaradas no milestone estão em `✅` no `docs/ROADMAP.md`

Se algum item falhar, resolver antes do dispatch — seja refinando o milestone no ROADMAP, fechando o milestone anterior, ou esperando a dependência de core.

---

## EXEMPLOS DE DISPATCH

**Exemplo 1 — milestone com todos os épicos em `🔍`:**

```
implementa a POC do Ensaio
```

Claude Code Web extrai `POC-ENSAIO`, vê que todos os épicos (E-POC-1, E-POC-2, E-POC-3) estão em `🔍 Detalhes definidos`, pula a PM skill e começa pela EM.

**Exemplo 2 — milestone com épicos em `🌱`/`🧭`/`📐`:**

```
roda PROTO-ENSAIO
```

Claude Code Web extrai `PROTO-ENSAIO`, vê épicos em `🌱 Visão`, dispara a PM skill para refinamento tático dentro da branch `milestone/proto-ensaio` antes de chegar à EM.

**Exemplo 3 — milestone com sufixo:**

```
dispara o POC-ENSAIO-ALPHA
```

Claude Code Web extrai `POC-ENSAIO-ALPHA` literal, valida no ROADMAP, segue o fluxo.

**Exemplo 4 — frase ambígua:**

```
implementa o Ensaio
```

Claude Code Web não consegue escolher entre `POC-ENSAIO`, `PROTO-ENSAIO`, `MVP-ENSAIO`. Responde pedindo id explícito.

---

**Ver também:**
- Quando usar autônomo vs manual → `docs/process/autonomous/overview.md`
- Detalhe dos gates e loop por épico → `docs/process/autonomous/workflow.md`
- Como o dev valida o milestone entregue → `docs/process/autonomous/delivery.md`
- Convenções operacionais (segredos, granularidade de commits) → `docs/process/autonomous/session_conventions.md`
- Glossário de milestone / épico / funcionalidade → `docs/CONSTITUTION.md` §9
