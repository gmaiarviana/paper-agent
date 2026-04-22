# Heurística de Sizing — EM Skill

> **📌 Localização:** `docs/process/sizing/`
> **📌 Consumido por:** [skills/em/skill.md](../../../skills/em/skill.md) (programa executável da EM Skill)
> **📌 Histórico:** [history.jsonl](history.jsonl) | **Schema:** [schema.md](schema.md)

---

## Princípio

A heurística é **deliberadamente simples** no início. A intenção não é prever LOC com precisão — é dar à EM Skill um critério reproduzível para decidir entre **FIT** (cabe na sessão), **TIGHT** (aperta mas segue) e **OVERFLOW** (estoura, devolve ao dev).

A heurística **evolui com os dados**. Cada milestone executado deixa uma linha em `history.jsonl` com o LOC estimado e — depois que RTE fecha — o LOC real. A média móvel desses dados ajusta o `LOC_média_por_funcionalidade` ao longo do tempo. Os thresholds (FIT/TIGHT/OVERFLOW) também devem ser revisados após os 5 primeiros milestones concluídos.

---

## Fórmula de Estimativa

```
LOC_estimado = Σ (para cada épico no milestone) (
    funcionalidades_do_épico
  × LOC_média_por_funcionalidade
  × fator_de_risco_do_épico
)
```

Os três fatores e como obter cada um estão descritos abaixo.

### `funcionalidades_do_épico`

Número de funcionalidades listadas no épico (`X.1`, `X.2`, `X.3`, ...) no ROADMAP de produto ou em `docs/ROADMAP.md` (se for épico core). Pré-requisito: épico em `🔍 Detalhes definidos` — sem isso, a contagem não é confiável e EM aborta.

### `LOC_média_por_funcionalidade`

- **Bootstrap (default, sem histórico):** `200` LOC por funcionalidade.
- **Calibrado:** quando `history.jsonl` tem **≥ 3** linhas com `decision = FIT` E `session_outcome = completed` E `loc_actual` preenchido, usar a **média móvel** de `loc_actual / features_count` dessas linhas FIT concluídas.
  - Janela da média: até as 10 mais recentes (ou todas, se forem menos).
- **Justificativa do default 200:** chute inicial calibrado para o tipo de mudança típico do paper-agent (modificação focada em agente do core ou interface Streamlit). Será corrigido pelos primeiros milestones reais.

### `fator_de_risco_do_épico`

Parte de `1.0` e recebe incrementos:

| Sinal | Incremento | Como detectar |
|-------|-----------|----------------|
| Épico declara "refatora X existente" | `+0.3` | Buscar `refatora` ou `refactor` no objetivo / descrição das funcionalidades |
| Épico declara "integra com Y já implementado" | `+0.3` | Buscar `integra com` ou `integration` no texto |
| Épico tem dependência de core ainda não-`✅` | `+0.2` | Olhar campo "Dependências" do épico e verificar status na tabela de `docs/ROADMAP.md` |

Os incrementos somam, mas o fator máximo razoável é `2.0` — se passar disso, EM declara "épico precisa ser quebrado em sub-épicos antes do milestone seguir" e devolve ao dev.

`fator_de_risco_milestone` = média aritmética dos fatores por épico, usado apenas para reportar no bloco de sizing em `current_implementation.md` e na linha do `history.jsonl`. A fórmula real aplica o fator **por épico**, não a média.

---

## Thresholds de Decisão

Aplicados sobre o `LOC_estimado` calculado pela fórmula:

| Decisão | Condição | Ação |
|---------|----------|------|
| **FIT** | `LOC_estimado ≤ 3000` | Segue para Scrum Master sem alarde |
| **TIGHT** | `3000 < LOC_estimado ≤ 6000` | Segue para Scrum Master; alerta registrado em `current_implementation.md` para entrega final mostrar ao dev |
| **OVERFLOW** | `LOC_estimado > 6000` | PARA, devolve ao dev com proposta de quebra em sub-milestones (`<ID>-ALPHA`/`<ID>-BETA`) |

Esses números são **chute inicial** — devem ser revisados após os 5 primeiros milestones concluídos, comparando `LOC_estimado` vs `loc_actual` reais. Se a estimativa estiver consistentemente acima ou abaixo do real por >30%, recalibrar o `LOC_média_por_funcionalidade` default antes dos thresholds.

---

## Critério de Quebra (apenas como sugestão para o OVERFLOW)

Quando EM precisa propor quebra de milestone, aplicar nesta ordem:

1. **Separar épicos com dependência de core não-`✅` do resto.** Tipicamente o sub-milestone com dependências externas vai antes (`-ALPHA`).
2. **Separar por subsistema.** Ex.: UI separada de backend; dados separados de orquestração.
3. **Manter cada metade abaixo do TIGHT threshold (6000 LOC estimado).**

Se nenhuma quebra natural existe (todos os épicos são interdependentes e tocam o mesmo subsistema), declarar isso explicitamente em vez de inventar uma divisão arbitrária. O dev decide o caminho — pode optar por aceitar OVERFLOW conscientemente (e criar duas sessões manualmente) ou refatorar o milestone via Claude Web.

---

## Bootstrap e Evolução

| Estado de `history.jsonl` | Comportamento da EM |
|----------------------------|---------------------|
| Vazio (0 linhas) | Defaults integrais. Decisão baseada apenas na fórmula. |
| `< 3` linhas FIT concluídas | Defaults integrais. EM grava nova linha; calibragem ainda não ativa. |
| `≥ 3` linhas FIT concluídas | `LOC_média_por_funcionalidade` ajustado por média móvel; thresholds permanecem nos defaults até revisão explícita do dev. |
| ≥ 5 milestones concluídos (qualquer veredicto) | Revisar thresholds explicitamente. Se `LOC_estimado` desviou consistentemente do `loc_actual`, ajustar este arquivo. |

A revisão dos thresholds é **trabalho explícito do dev** — não automatizada. Mudanças neste arquivo entram via commit normal na branch da reforma de fluxo correspondente.

---

## Defaults consolidados

Para referência rápida da EM Skill:

| Parâmetro | Valor inicial |
|-----------|---------------|
| `LOC_média_por_funcionalidade` | `200` |
| `fator_de_risco_inicial` | `1.0` |
| Incremento por refatoração declarada | `+0.3` |
| Incremento por integração com sistema existente declarado | `+0.3` |
| Incremento por dependência de core não-`✅` | `+0.2` |
| Fator máximo razoável por épico | `2.0` |
| Janela da média móvel (calibragem) | últimas 10 linhas FIT concluídas |
| Threshold FIT (≤) | `3000` LOC |
| Threshold TIGHT (≤) | `6000` LOC |
| Acima de `6000` | OVERFLOW |
