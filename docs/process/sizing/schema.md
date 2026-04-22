# Schema de `history.jsonl`

> **📌 Localização:** `docs/process/sizing/`
> **📌 Arquivo:** [history.jsonl](history.jsonl)
> **📌 Escrito por:** [skills/em/skill.md](../../../skills/em/skill.md) (linha de decisão) e [skills/rte/skill.md](../../../skills/rte/skill.md) (linha de fechamento)

---

## Princípio

`history.jsonl` é **append-only**. Cada milestone gera **duas linhas** ao longo do ciclo:

1. **Linha de decisão** — escrita pela EM Skill no início, com a estimativa e o veredicto.
2. **Linha de fechamento** — escrita pela RTE Skill no fim, com `loc_actual` real e o `session_outcome` definitivo.

Linhas são identificadas pelo par (`milestone_id`, `session_outcome`):
- `session_outcome = pending` → linha da EM, ainda em curso
- `session_outcome ≠ pending` → linha da RTE, milestone fechado

A calibragem da heurística (média móvel) consome as linhas de **fechamento** com `decision = FIT` e `loc_actual` preenchido.

JSONL não suporta comentários; o arquivo começa vazio. Este `schema.md` é a fonte da verdade do formato.

---

## Schema (uma linha por evento)

| Campo | Tipo | Origem | Obrigatório | Descrição |
|-------|------|--------|------------|-----------|
| `timestamp` | string (ISO 8601) | EM ou RTE | sim | Momento em que a linha foi escrita. |
| `milestone_id` | string | EM ou RTE | sim | Id do milestone, formato `<ESTAGIO>-<PRODUTO>` (ex.: `POC-ENSAIO`). |
| `product` | string | EM ou RTE | sim | Slug do produto em caixa baixa (ex.: `ensaio`, `revelar`). |
| `stage` | string | EM ou RTE | sim | `POC` \| `Protótipo` \| `MVP`. |
| `epics_count` | int | EM | sim | Número de épicos agrupados pelo milestone. |
| `features_count` | int | EM | sim | Soma das funcionalidades em todos os épicos do milestone. |
| `risk_factor_applied` | float | EM | sim | Fator de risco médio aplicado (ver `heuristic.md` §"Fator de risco"). |
| `loc_estimated` | int | EM | sim | LOC estimado pela fórmula da heurística no momento da decisão. |
| `loc_actual` | int \| null | RTE | sim na linha de fechamento | LOC real ao final do milestone (somatório do diff vs `main`). `null` na linha da EM. |
| `decision` | string | EM | sim | `FIT` \| `TIGHT` \| `OVERFLOW`. |
| `session_outcome` | string | EM e RTE | sim | Estado do milestone — ver tabela abaixo. |
| `notes` | string | EM ou RTE | opcional | Texto livre para contexto (ex.: "alerta TIGHT registrado", "OVERFLOW devolvido com proposta ALPHA/BETA", "milestone concluído com 1 reprovação de QA resolvida"). |

### Valores possíveis de `session_outcome`

| Valor | Quando é gravado | Significado |
|-------|------------------|-------------|
| `pending` | EM grava na linha de decisão se `decision ∈ {FIT, TIGHT}` | Sizing aprovado; aguarda RTE fechar. |
| `overflow_rejected` | EM grava na linha de decisão se `decision = OVERFLOW` | Devolvido ao dev; sem linha de RTE futura. |
| `completed` | RTE grava na linha de fechamento | Milestone executado e validado pelo humano. |
| `aborted_by_gate_reprovation` | RTE grava na linha de fechamento | Algum gate reprovou 3× consecutivas no mesmo épico, milestone abortado conforme decisão fixada da reforma. |
| `aborted_by_dev` | RTE grava na linha de fechamento | Dev interveio e abortou manualmente antes do fim. |

---

## Exemplo de Ciclo Completo

Milestone `POC-ENSAIO` que executou e fechou normalmente teria duas linhas:

```jsonl
{"timestamp":"2026-04-22T08:30:00Z","milestone_id":"POC-ENSAIO","product":"ensaio","stage":"POC","epics_count":3,"features_count":13,"risk_factor_applied":1.06,"loc_estimated":2756,"loc_actual":null,"decision":"FIT","session_outcome":"pending","notes":""}
{"timestamp":"2026-04-22T17:14:00Z","milestone_id":"POC-ENSAIO","product":"ensaio","stage":"POC","epics_count":3,"features_count":13,"risk_factor_applied":1.06,"loc_estimated":2756,"loc_actual":2419,"decision":"FIT","session_outcome":"completed","notes":"3 épicos entregues sem reprovação"}
```

A linha de fechamento repete os campos da linha de decisão para que cada linha seja autocontida — não é necessário fazer join.

Milestone que estourou no sizing teria apenas uma linha:

```jsonl
{"timestamp":"2026-04-22T08:30:00Z","milestone_id":"PROTO-REVELAR","product":"revelar","stage":"Protótipo","epics_count":7,"features_count":31,"risk_factor_applied":1.42,"loc_estimated":8804,"loc_actual":null,"decision":"OVERFLOW","session_outcome":"overflow_rejected","notes":"devolvido com proposta ALPHA (4 épicos) + BETA (3 épicos)"}
```

---

## Regras de Escrita

- **Append-only.** Skills nunca editam linha existente. Se uma linha precisa ser corrigida (ex.: humano descobre erro post-mortem), corrigir manualmente em commit explícito documentando a razão.
- **Uma linha por evento.** EM grava 1 linha; RTE grava no máximo 1 linha por milestone.
- **Repetir campos.** Cada linha é autocontida; não economizar campos contando que outra linha tem.
- **Timestamps em UTC** (sufixo `Z`).
- **`loc_actual`** é o resultado de `git diff --shortstat origin/main..HEAD` (linhas adicionadas + removidas) na branch do milestone, somando código + testes (excluindo docs e configs puras). Detalhamento da regra exata fica a cargo da RTE Skill em `skills/rte/skill.md`.

---

## Calibragem

A EM Skill consome este arquivo para calibrar `LOC_média_por_funcionalidade`. Filtro:

```
linhas onde session_outcome = "completed" AND decision = "FIT" AND loc_actual IS NOT NULL
```

Ordenado por `timestamp` desc, pegar até 10 linhas. Calcular `loc_actual / features_count` para cada uma. Média = novo `LOC_média_por_funcionalidade` ajustado.

Se filtro retorna `< 3` linhas, EM usa o default da heurística. Detalhes em `heuristic.md` §"Bootstrap e Evolução".
