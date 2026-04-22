# ROADMAP - Revelar

Épicos e melhorias do produto Revelar (chat para clareza de pensamento).

> **📖 Status Atual:** Para entender o estado atual do Revelar, consulte [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) e [products/revelar/docs/](docs/).

> **📖 Visão:** Para entender a visão do produto, consulte [products/revelar/docs/vision.md](docs/vision.md).

### 🧭 Estados dos Épicos

Cada épico percorre até seis estados. Detalhes em [docs/process/refinement/planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md).

- **`🌱 Visão`** — apenas objetivo definido. Aguarda refinamento.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Pronto para fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist em [autonomous_readiness.md](../../docs/process/refinement/autonomous_readiness.md) aplicado. Pronto para fluxo autônomo via Claude Code Web.
- **`🏗️ Em andamento`** — implementação em curso, até o ciclo de fechamento.
- **`✅ Implementado`** — ciclo de fechamento executado (ver [epic_completion.md](../../docs/process/refinement/epic_completion.md)).

> **Retroatividade:** épicos concluídos antes da introdução do modelo de 6 estados permanecem em formato simplificado (título ✅ + 1-2 linhas de resumo) e não são reclassificados retroativamente. O modelo aplica-se a épicos em andamento e futuros.

---

## 🎯 Milestones

> **Convenção:** id no formato `<ESTAGIO>-<PRODUTO>` em caixa alta, com hífen (ver glossário em [docs/CONSTITUTION.md §9](../../docs/CONSTITUTION.md)). Branch associada em caixa baixa: `milestone/<id>`. Quando um estágio precisa de mais de um milestone, adicionar sufixo: `MVP-REVELAR-ALPHA`, `MVP-REVELAR-BETA`.

Milestone agrupa épicos relacionados dentro de um estágio. É a unidade de entrega do fluxo autônomo (`docs/process/autonomous/`) — disparo por linguagem natural ("implementa o MVP do Revelar"), execução na branch do milestone, merge em main apenas com aval humano.

### MVP-REVELAR

- **Objetivo:** fechar a interface do MVP do Revelar em duas frentes complementares — painel visual do Observer nos Bastidores (transparência de como o sistema pensa: claim, proposições, tensões e gaps) e catálogo navegável dos conceitos acumulados. Habilita colegas a usar o Revelar sem o desenvolvedor do lado.
- **Estágio:** MVP — Colegas Usam (Revelar está em MVP em desenvolvimento, conforme `products/revelar/README.md`)
- **Produto:** Revelar
- **Épicos agrupados:** ÉPICO 1 (Observer - Painel Visual Dedicado), ÉPICO 2 (Catálogo de Conceitos - Interface Web)
- **Dependências de core:** nenhuma pendente (Observer core já implementado; Catálogo depende de Painel Observer — dependência interna ao milestone)
- **Branch associada:** `milestone/mvp-revelar`
- **Status dos épicos:** ÉPICO 1 em `📋 Critérios definidos`, ÉPICO 2 em `📐 Funcionalidades esboçadas`
- **Nota:** com ÉPICO 2 ainda em `📐`, o refinamento tático para `🔍` acontece dentro da branch do milestone via PM skill antes da implementação (ver [docs/process/refinement/planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md)). Avaliação de sizing e possível quebra em sub-milestones acontecem antes do dispatch.

> Épicos concluídos anteriores ao modelo de seis estados não são agrupados retroativamente — seguem a regra de retroatividade declarada acima.

---

## 📋 Épicos Planejados

### 📋 Épicos em `Critérios definidos` (prontos para fluxo manual via Cursor)

#### ÉPICO 1: Observer - Painel Visual Dedicado

**Objetivo:** Interface visual mostrando estado do Observer de forma transparente e não-intrusiva.

**Status:** 📋 Critérios definidos

**Dependências:**
- Observer core já implementado (Épico 10-14 concluídos)

**Filosofia:**
- Transparência: usuário vê como sistema pensa
- Não-intrusivo: painel colapsado por padrão
- Útil: mostra informação acionável, não apenas diagnóstico
- Educativo: ajuda usuário entender conversa melhor

### Funcionalidades:

#### 1.1 Painel Principal (Colapsável)

- **Descrição:** Seção dedicada "Observer" nos Bastidores, entre "Contexto" e "Raciocínio".
- **Critérios de Aceite:**
  - Nova seção "🔍 Observer" em `app/components/backstage/`
  - Localização: entre `st.expander("Contexto")` e `st.expander("Bastidores")`
  - Padrão: colapsado (`st.expander(default_expanded=False)`)
  - Ao expandir: mostra estado atual do CognitiveModel
  - Design consistente com outras seções dos Bastidores
  - Componente: `app/components/backstage/observer_panel.py`

#### 1.2 Métricas Visuais (Qualitativas)

- **Descrição:** Visualização do estado da conversa sem números fixos.
- **Critérios de Aceite:**
  - Grid com indicadores: solidez da conversa (barra de progresso verde/amarelo/vermelho), completude do argumento (barra de progresso), tensões identificadas (contador + badge ⚠️ se > 0), gaps abertos (contador + badge)
  - Barras são visuais (não mostram percentual exato)
  - Cores indicam saúde geral (verde = bem, amarelo = atenção, vermelho = problemas)
  - Badge "🟢 Madura" ou "🟡 Em desenvolvimento" baseado em análise qualitativa

#### 1.3 Claim Atual e Proposições

- **Descrição:** Visualização clara do claim e principais proposições.
- **Critérios de Aceite:**
  - Claim atual em destaque (`st.info` ou `st.markdown` com fundo)
  - Lista de proposições principais (top 5 por solidez)
  - Cada proposição mostra: texto da proposição, indicador visual de solidez (emoji: 🟢 sólida, 🟡 moderada, 🔴 frágil)
  - NÃO mostra número exato
  - Proposições ordenadas por relevância (solidez)

#### 1.4 Tensões e Open Questions

- **Descrição:** Visualização de contradições (tensões) e gaps identificados.
- **Critérios de Aceite:**
  - Seção "⚠️ Tensões" (se existirem): lista contradições identificadas, não usa linguagem de "erro" (usa "tensão entre proposições"), mostra contexto (quais proposições estão em tensão)
  - Seção "❓ Gaps Abertos" (se existirem): lista open_questions, indica se são gaps críticos ou menores
  - Se não há tensões/gaps: mensagem positiva "✅ Nenhuma tensão identificada"

#### 1.5 Modal Detalhado (3 Abas)

- **Descrição:** Botão "Ver detalhes" abre modal com visão completa do Observer.
- **Critérios de Aceite:**
  - Botão no painel principal: "Ver detalhes completos"
  - Modal com 3 abas (padrão dos Bastidores): Aba 1 - Estado Atual (claim completo, todas proposições, todas tensões e gaps, análise de confusão), Aba 2 - Evolução (timeline visual de mudanças no claim, gráfico de solidez/completude ao longo do tempo (Plotly), eventos importantes), Aba 3 - JSON (CognitiveModel completo em JSON formatado, permite usuário copiar/exportar)
  - Modal usa `st.dialog` (API Streamlit 1.31+)

#### 1.6 Integração com EventBus

- **Descrição:** Painel Observer consome eventos e atualiza em tempo real.
- **Critérios de Aceite:**
  - Observer publica eventos: `COGNITIVE_MODEL_UPDATED`, `VARIATION_DETECTED`, `DIRECTION_CHANGE`, `CLARIFICATION_REQUESTED`
  - Painel consome eventos via EventBus (já existe)
  - Atualização automática sem refresh manual
  - Segue padrão de `products/revelar/app/components/backstage/reasoning.py`

#### 1.7 Testes de Interface

- **Descrição:** Validação da UI do painel Observer.
- **Critérios de Aceite:**
  - Testes visuais: painel renderiza corretamente
  - Testes de interação: modal abre/fecha
  - Testes de eventos: painel atualiza com novos eventos
  - Testes de responsividade: funciona em diferentes tamanhos de tela

---

### 📐 Épicos em Funcionalidades esboçadas

#### ÉPICO 2: Catálogo de Conceitos - Interface Web

**Objetivo:** Usuário explora biblioteca de conceitos via web. Transparência sobre o que sistema aprendeu.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:**
- ÉPICO 1 (Painel Observer)

**Consulte:**
- `products/revelar/docs/interface/components.md` - Componentes Streamlit

### Funcionalidades Planejadas:

#### 2.1 Página Catálogo (`/catalogo`)

- Lista todos conceitos da biblioteca
- Busca por nome (fuzzy search)
- Filtros: por ideia, por frequência, por data
- Visualização: cards com conceito + variations + ideias relacionadas

#### 2.2 Preview na Página da Ideia

- Mostra discretamente: "Usa 3 conceitos: [X] [Y] [Z]"
- Tags clicáveis → redireciona para catálogo
- Não polui interface

#### 2.3 Analytics de Conceitos

- Conceitos mais mencionados (gráfico)
- Conceitos por ideia/artigo
- Evolução temporal
- Export em JSON
- Sistema detecta padrões: "5+ usuários adicionaram conceito X" → atualiza biblioteca base

#### 2.4 Testes E2E

- Fluxo completo: conversa → conceitos → catálogo
- Validar UX (não quebra experiência)
- Performance (biblioteca com 100+ conceitos)

---

> **📖 Melhorias Técnicas:** Para melhorias técnicas não vinculadas a épicos, consulte [docs/backlog.md](../../docs/backlog.md).

---

## 📚 Documentação

- `products/revelar/docs/vision.md` - Visão do produto
- `products/revelar/docs/interface/` - Especificações de interface

---

## 📝 Observações

**Regra:** fluxo manual via Cursor exige épico em `📋 Critérios definidos`; fluxo autônomo via Claude Code Web exige `🔍 Detalhes definidos`.

> Para o processo completo de refinamento, consulte [planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md). Para a prontidão ao fluxo autônomo (alvo `🔍`), consulte [autonomous_readiness.md](../../docs/process/refinement/autonomous_readiness.md). Para o fechamento do épico (saída), consulte [epic_completion.md](../../docs/process/refinement/epic_completion.md).

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos em `🌱 Visão` ou `📐 Funcionalidades esboçadas` passam por sessão de refinamento antes da implementação
