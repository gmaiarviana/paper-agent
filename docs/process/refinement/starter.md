# Refinement Starter Pack

> **📌 Objetivo:** Lista autoritativa de arquivos para arrastar ao Claude Web ao iniciar refinamento de qualquer épico, de qualquer produto.

O Claude Web não tem acesso ao repositório. Esse pack dá a ele o mínimo necessário para entender princípios, arquitetura, épicos e — via mapa temático — saber onde pedir o resto.

## 📋 Pack Inicial (6 arquivos)

### Genéricos (sempre) — 4 arquivos

1. **`docs/CONSTITUTION.md`** — Princípios, responsabilidades, processo, mapa de decisão, estrutura do projeto.
2. **`docs/ARCHITECTURE.md`** — Estado técnico atual consolidado.
3. **`docs/ROADMAP.md`** — Épicos e melhorias do core compartilhado (inclui épicos motivados por produtos — prefixo `C-<PRODUTO>-`).
4. **`docs/CONTEXT_INDEX.md`** — **Mapa temático código↔doc.** Claude Web usa para saber **onde** pedir cada doc adicional (orquestração, agentes, dados, interface, config, testes etc.).

### Específicos do produto em refinamento — 2 arquivos

5. **`products/<produto>/ROADMAP.md`** — Épicos do produto.
6. **`products/<produto>/docs/vision.md`** — Visão do produto (o "por quê", escopo POC / Protótipo / MVP, casos de uso).

### Produtos hoje

| Produto | ROADMAP | Vision |
|---------|---------|--------|
| Revelar (atual) | `products/revelar/ROADMAP.md` | `products/revelar/docs/vision.md` |
| Ensaio (próximo) | `products/ensaio/ROADMAP.md` | `products/ensaio/docs/vision.md` |
| Prisma Verbal (futuro) | `products/prisma-verbal/ROADMAP.md` | `products/prisma-verbal/docs/vision.md` |
| Camadas da Linguagem (futuro) | — | `products/camadas-da-linguagem/docs/vision.md` |
| Expressão (futuro) | — | `products/expressao/docs/vision.md` |
| Produtor Científico (futuro) | `products/produtor-cientifico/ROADMAP.md` | `products/produtor-cientifico/docs/vision.md` |

## 🎯 Alvos de Refinamento

Toda sessão de refinamento começa com um **alvo declarado** — o estado ao qual o épico (ou conjunto de épicos) deve chegar ao fim da sessão. Sessões se dividem em dois tipos conforme o alvo:

- **Refinamento em massa** — alvo `🌱 Visão` ou `📐 Funcionalidades esboçadas`, aplicado a múltiplos épicos de uma vez. Produz várias entradas no ROADMAP a partir de uma visão.
- **Refinamento profundo** — alvo `📋 Critérios definidos` ou `🔍 Detalhes definidos`, aplicado a um épico específico que se aproxima da implementação.

O pack inicial acima é suficiente para alvos até `📋 Critérios definidos`. O alvo `🔍 Detalhes definidos` exige contexto adicional — inspeção de código relevante + checklist específico. O modelo completo dos seis estados de um épico vive em [`planning_guidelines.md`](planning_guidelines.md).

### Alvo `🌱 Visão` (refinamento em massa — nível título)

- **Pergunta:** quais são os principais épicos desta visão?
- **Produto:** N épicos com título e objetivo. Sem lista de funcionalidades ainda.
- **Contexto enviado ao Claude Web:** pack inicial de 6 arquivos.
- **Quando acontece:** ao abrir um ROADMAP novo e querer apenas registrar os próximos movimentos em alto nível.

### Alvo `📐 Funcionalidades esboçadas` (refinamento em massa — nível esboço)

- **Pergunta:** como essa visão se quebra em épicos trabalháveis, e o que cada um entrega?
- **Produto:** N épicos com objetivo e lista curta de funcionalidades (descrição de 1 frase cada), sem critérios de aceite.
- **Contexto enviado ao Claude Web:** pack inicial de 6 arquivos.
- **Quando acontece:** ao quebrar uma visão de produto em itens trabalháveis com um pouco mais de granularidade que `🌱 Visão`.

### Alvo `📋 Critérios definidos` (refinamento profundo — critérios)

- **Pergunta:** isso faz sentido e gera valor?
- **Produto:** funcionalidades delimitadas, critérios de aceite observáveis, trade-offs discutidos.
- **Contexto enviado ao Claude Web:** pack inicial de 6 arquivos.
- **Quando acontece:** quando o épico se torna prioritário.
- **Estado resultante do épico:** `📋 Critérios definidos` — apto ao fluxo manual via Cursor.

### Alvo `🔍 Detalhes definidos` (refinamento profundo — detalhes)

- **Pergunta:** um agente sem contexto do problema consegue executar isto sem inventar?
- **Produto:** arquivos-alvo com caminho completo, contratos/shapes, mecanismo de integração, acoplamentos verificados, escopo de testes.
- **Contexto enviado ao Claude Web:** pack inicial de 6 arquivos + **inspeção de código relevante** (via Cursor, ou como trechos específicos pedidos ao Claude Web) + checklist em [`autonomous_readiness.md`](autonomous_readiness.md). A inspeção de código é parte obrigatória deste alvo, não opcional.
- **Quando acontece:** sob demanda, pouco antes de disparar o fluxo autônomo para o épico específico. Aplicar preventivamente em todos os épicos é desperdício — o trabalho perde-se se o épico for repriorizado.
- **Estado resultante do épico:** `🔍 Detalhes definidos` — apto ao fluxo autônomo via Claude Code Web ([`dispatch.md`](../autonomous/dispatch.md)).

> Atalho permitido: uma única sessão pode ir direto de `🌱 Visão` para `📋` ou `🔍`, desde que o alvo declarado seja esse e o contexto correspondente seja enviado.

## 📚 Documentos Consultados Sob Demanda

Tudo que não está no pack inicial está mapeado em `docs/CONTEXT_INDEX.md` — que já está no pack. Durante o refinamento, Claude Web identifica o tema relevante no CONTEXT_INDEX (seção `## TEMA: ...` ou tabela `🎯 MAPA RÁPIDO DE DECISÃO`) e pede os paths listados ali.

## ⚠️ Fora do Pack Inicial

- **`README.md`** — Útil para setup humano, não para refinamento estratégico.
- **Docs de arquitetura/agentes** — Pedir sob demanda via `CONTEXT_INDEX.md` (senão explode o contexto inicial).

---

**Versão:** 2.0
**Substitui:** Listas inconsistentes em CONSTITUTION §7, planning_guidelines, CONTEXT_INDEX.
