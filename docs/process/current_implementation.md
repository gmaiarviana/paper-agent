# Implementação Atual: Milestone PROTO-ENSAIO-2

**Milestone:** PROTO-ENSAIO-2 — transparência do raciocínio dos agentes + voz do usuário antes de decisões virarem estado
**Produto:** Ensaio
**Estágio:** Protótipo
**Branch:** `claude/implement-product-essay-dHnbU` (harness-assigned; equivalente a `milestone/proto-ensaio-2` no fluxo manual)
**Modo:** Autônomo (disparo manual + execução em chunks)
**Dispatch recebido em:** 2026-04-30

---

## Contexto do Milestone

**Objetivo:** Tornar visível o raciocínio dos agentes do Ensaio e dar ao usuário voz antes que decisões virem estado. Ataca pontos do PROTO-ENSAIO original que produziram sessão funcional mas opaca: Estruturador decidindo sozinho (auto-commit em `current_article`), Metodologista com papel embolado (cobrindo formato/estrutura — território do Estruturador) e por isso convocado raramente, mensagens longas que escondem o que mudou, painel de seções sem accordion.

**Épicos agrupados:** E-PROTO2-2, E-PROTO2-1, E-PROTO2-3, E-PROTO2-4 (ordem de execução interna — papéis afiados antes da co-decisão; manchete em paralelo com co-decisão; accordion por último).

**Dependências de core:** nenhuma nova. Toca arquivos do core (Estruturador, Metodologista, Orquestrador) com mudanças aditivas e gated por `product_context` — Revelar não regride.

---

## Restrições de escopo (não-negociáveis do milestone)

- **Conversa fluida:** o Orquestrador continua decidindo *quando* convocar Estruturador ou Metodologista. Sem ordem fixa entre eles. Implementação não pode amarrar sequência no grafo.
- **Sessão descartável:** persistência fica para MVP-ENSAIO; recarregar zera tudo.
- **Sem regressão Revelar:** mudanças no core são gated por `product_context` (presente apenas no Ensaio) ou puramente aditivas em `additional_kwargs` (Revelar não lê os campos novos).

---

## Status dos Gates (nível milestone)

> **Nota:** este milestone foi disparado manualmente; gates de Scrum Master/EM/PM não foram preenchidos pelo fluxo autônomo ortodoxo. Os gates Dev/QA/TL/PO foram cumpridos pela execução in-session (validação por testes unitários + smoke import + iteração com fix do React Hooks violation). RTE roda manualmente para abrir a PR.

- [➖] PM (skipped — milestone já estava em `🔍 Detalhes definidos`)
- [➖] EM (sizing skipped — milestone manual)
- [➖] Scrum Master (skipped — disparo manual)
- [x] Loop por épico concluído (todas as funcionalidades dos 4 épicos implementadas, testadas e commitadas)
- [x] RTE (gera `current_validation.md`, abre PR, atualiza ROADMAP)

---

## Épicos

### Épico E-PROTO2-2 — Metodologista com escopo e qualidade afiados

**Status:** ✅ Implementado

**Funcionalidades entregues:**
- **2.1** Prompt do Metodologista limpo (`core/prompts/methodologist_provocation.py`): adicionada dimensão **Tese central**; removidas dimensões **Formato** e **Estrutura** (território do Estruturador). Postura inalterada.
- **2.2** Postura do Orquestrador/Estruturador em `products/ensaio/config/product.yaml` reescrita: Estruturador foca storytelling com `rationale` obrigatório; Metodologista cobre tese/intenção/afirmação sem suporte. Sem ordem fixa.
- **2.3** Aceite negativo: `products/ensaio/app/graph.py` mantém `route_from_orchestrator` como único decisor (sem edges fixas methodologist↔structurer).

**Gates por funcionalidade:**

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 2.1 Prompt limpo | ✅ | ✅ (revisão visual) | ✅ | ✅ |
| 2.2 Postura YAML | ✅ | ✅ (revisão visual) | ✅ | ✅ |
| 2.3 Aceite negativo grafo | ✅ | ✅ (verificação documental) | ✅ | ✅ |

---

### Épico E-PROTO2-1 — Co-decisão da Estrutura

**Status:** ✅ Implementado

**Funcionalidades entregues:**
- **1.1** Proposta sem auto-commit: `EnsaioState.pending_structure_proposal` recebe a proposta; `current_article` só é tocado após aceite explícito.
- **1.2** Bubble especial com aceitar/editar/recusar: `products/ensaio/app/components/proposal_bubble.py` novo, integrado acima do input do chat.
- **1.3** Edição leve: renomear (input), mover (↑/↓), remover (🗑️), adicionar (+ Adicionar seção); confirmar/cancelar; lista vazia bloqueia aceite.
- **1.4** Campo condicional `rationale` em `core/agents/structurer/nodes.py` gated por `product_context` (mesmo padrão de `article_sections`); Revelar não regride.

**Gates por funcionalidade:**

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 1.1 Proposta sem commit | ✅ | ✅ (4 testes unit) | ✅ | ✅ |
| 1.2 Bubble com ações | ✅ | ✅ (smoke render) | ✅ | ✅ |
| 1.3 Edição leve | ✅ | ✅ (7 testes unit) | ✅ | ✅ |
| 1.4 Rationale gated | ✅ | ✅ (3 testes unit) | ✅ | ✅ |

---

### Épico E-PROTO2-3 — Manchete "o que mudou"

**Status:** ✅ Implementado

**Funcionalidades entregues:**
- **3.1** Contrato `change_summary` em `AIMessage.additional_kwargs` (≤80 chars, pt-BR, opcional, puramente aditivo). `state.py:send_message` propaga para o dict de mensagem; chave sempre presente (mesmo vazia) para shape estável no `rx.foreach` do Reflex.
- **3.2** Renderização da manchete: `chat_panel._message_bubble` exibe Box sempre montado com `display=cond(...)` para não disparar React Hooks violation.
- **3.3** Três produtores cobertos:
  - Estruturador: `📐 Estrutura proposta` quando `article_sections` presente.
  - Metodologista: `🔬 Lacuna apontada` quando não é frase de aceite ("o contexto está bem descrito").
  - Orquestrador: `🎯 Foco atualizado` quando `focal_argument` muda em campo relevante (intent/subject/population/metrics/article_type).

**Gates por funcionalidade:**

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 3.1 Contrato change_summary | ✅ | ✅ (smoke render) | ✅ | ✅ |
| 3.2 Render manchete | ✅ | ✅ (smoke render) | ✅ | ✅ |
| 3.3 Três produtores | ✅ | ✅ (10 testes unit) | ✅ | ✅ |

---

### Épico E-PROTO2-4 — Accordion no painel

**Status:** ✅ Implementado

**Funcionalidades entregues:**
- **4.1** Accordion no painel: `article_panel.py` substitui `_section_card` por `rx.accordion.root(type="multiple", collapsible=True)`. Cada seção é um `rx.accordion.item` com header (título + badge) e conteúdo (placeholder/markdown + botão Gerar/Regenerar).
- **4.2** Estado inicial colapsado: `default_value=[]` no accordion root. Estado de expansão fica interno ao Radix (não polui `EnsaioState`); recarregar zera (consistente com sessão descartável).

**Gates por funcionalidade:**

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 4.1 Accordion | ✅ | ✅ (smoke render) | ✅ | ✅ |
| 4.2 Default colapsado | ✅ | ✅ (smoke render) | ✅ | ✅ |

---

## Histórico de Reprovações

**Iteração 1 (commit `79b5e6a`):** entrega inicial de todos os 4 épicos. Smoke import OK; suíte unitária 245/245 + 4 falhas pré-existentes em `test_ensaio_graph_methodologist.py` (MagicMock checkpointer rejeitado por langgraph >= 0.2 — não causado pelo milestone).

**Reprovação 1 (validação manual via `reflex run`):** dev hit React Hooks violation no console do navegador. Causa: padrão `rx.cond(condition, Component, rx.fragment())` em vários pontos compila JSX que monta/desmonta componentes de tipo diferente entre renders; React contabiliza hooks por posição/tipo, então essa troca dispara "Rendered fewer/more hooks than during the previous render".

**Iteração 2 (commit `e184401`):** fix sistemático — sempre montar o mesmo componente, controlar visibilidade via `display=rx.cond(condition, "block", "none")`. Pontos fixados:
- `chat_panel._message_bubble` headline (foreach das mensagens — maior risco)
- `chat_panel._processing_indicator` e callout de erro
- `proposal_bubble` (outer + view/edit toggle + rationale + error message)
- `article_panel._section_body` (placeholder vs markdown)
- `article_panel` (Writer indicator, accordion vs empty-state)
- `_section_item` agora usa índice do foreach em vez de `section["index"].to_string()`

Pré-requisito de estado: `state.py` agora garante `change_summary` sempre presente em todos os dicts de mensagem (mesmo vazio).

**Iteração 3 (este commit):** merge de 68 commits do main; fix bônus dos 4 testes pré-existentes (`test_ensaio_graph_methodologist.py`: MagicMock → InMemorySaver). Suíte total: **249/249 passing, 2 skipped**. Smoke render do app OK.

---

## Extração pendente

(vazio — não foram identificados padrões arquiteturais novos ou conhecimento permanente neste milestone que mereçam extração para `core/docs/` ou `.claudecode.md`. As decisões deste milestone estão capturadas no ROADMAP do Ensaio e nos commits.)

---

## Resumo Final do Milestone

- **Branch:** `claude/implement-product-essay-dHnbU`
- **Commits do milestone (relativos a `main` antes do merge):**
  - `79b5e6a` feat(proto-ensaio-2): implementa milestone PROTO-ENSAIO-2
  - `e184401` fix(proto-ensaio-2): elimina React Hooks violation via display em vez de cond/fragment
  - `a59b12a` fix(test): troca MagicMock por InMemorySaver em test_ensaio_graph_methodologist
  - `90cde19` Merge remote-tracking branch 'origin/main' into claude/implement-product-essay-dHnbU
- **Arquivos modificados (excluindo merge):** 14 arquivos, ~1180 linhas inseridas, ~99 removidas.
- **Testes adicionados:** 24 testes novos.
  - `tests/core/unit/agents/test_structurer_rationale.py` — 3 testes (rationale gated por product_context).
  - `tests/core/unit/agents/test_change_summary_producers.py` — 10 testes (Metodologista + Orquestrador change_summary).
  - `tests/products/ensaio/unit/test_pending_proposal.py` — 11 testes (event handlers de proposta pendente).
- **Testes corrigidos:** 4 (`test_ensaio_graph_methodologist.py`).
- **Suíte total:** 249 passed, 2 skipped (`tests/core/unit/agents/` + `tests/products/ensaio/`).
- **Validação manual via `reflex run`:** delegada ao dev no fluxo da PR (script em `docs/process/current_validation.md`).

---

## Notas técnicas (TL)

**Padrão anti-hooks-violation no Reflex.** Toda vez que se quer renderização condicional de componente que está dentro de `rx.foreach` (ou de outra estrutura que React precisa diff-ar entre renders), preferir `rx.box(componente, display=rx.cond(...))` em vez de `rx.cond(condition, componente, rx.fragment())`. O segundo padrão monta/desmonta componentes de tipo diferente, e o React compila hooks por posição/tipo — qualquer troca dispara violação. Este aprendizado é **contextual ao Reflex 0.9** e fica registrado aqui (não em `.claudecode.md`) porque ainda não há segundo produto Reflex que precise reusar; promover quando segundo consumidor aparecer.

**Shape estável de dicts em `rx.foreach`.** Quando `foreach` itera uma lista de dicts e o componente filho lê chaves opcionais (`msg.get("change_summary", "")`), Reflex compila a leitura como acesso direto no JSX gerado. Garantir a chave sempre presente (mesmo com valor vazio) no produtor evita undefined no compile-time. Aplicado em `state.py:send_message`, `state.py` recusa de proposta, e mensagem de erro de backend.

---

## Evidências de carregamento de skill

(Únicas por milestone)
- [RTE] skill executada manualmente: 2026-04-30 (gera `current_validation.md`, atualiza este arquivo, abre PR, transita ROADMAP)
