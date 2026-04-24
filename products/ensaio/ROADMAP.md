# ROADMAP - Ensaio

Épicos e melhorias do produto Ensaio (transformar experimentos de código em artigos técnico-científicos).

> **📖 Visão:** Para entender a visão do produto, consulte [products/ensaio/docs/vision.md](docs/vision.md).

> **📖 Status Atual:** Para entender o estado técnico do sistema, consulte [ARCHITECTURE.md](../../docs/ARCHITECTURE.md).

### 🧭 Estados dos Épicos

Cada épico percorre até sete estados. Os mesmos estados aplicam-se ao campo "Status" do milestone. Detalhes em [docs/process/refinement/planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md).

- **`🌱 Visão`** — apenas objetivo definido. Aguarda refinamento.
- **`🧭 Jornada alinhada`** — objetivo refinado + rationale (o que é / o que não é) + glossário ancorado + acoplamentos sinalizados; jornada alvo e escopo declinados (para milestone). Funcionalidades ainda não esboçadas. Aguarda refinamento.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Pronto para fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist em [autonomous_readiness.md](../../docs/process/refinement/autonomous_readiness.md) aplicado. Pronto para fluxo autônomo via Claude Code Web.
- **`🏗️ Em andamento`** — implementação em curso, até o ciclo de fechamento.
- **`✅ Implementado`** — ciclo de fechamento executado (ver [epic_completion.md](../../docs/process/refinement/epic_completion.md)).

> **Retroatividade:** épicos concluídos antes da introdução do modelo de estados permanecem em formato simplificado (título ✅ + 1-2 linhas de resumo) e não são reclassificados retroativamente. O modelo aplica-se a épicos em andamento e futuros.

---

## 🧭 Filosofia de Estágios

Ensaio adota a progressão **POC → Protótipo → MVP** no eixo *quem usa* (ver [docs/process/refinement/planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md)):

- **POC:** prova que a ideia faz sentido. Pode ser tosco, rodar só no ambiente do desenvolvedor, ter atalhos explícitos.
- **Protótipo:** a ideia funciona e o **próprio desenvolvedor usa de verdade** no fluxo real dele.
- **MVP:** **outros** (colegas próximos) usam **sem o desenvolvedor do lado**.

Decisões de stack, UX e robustez são proporcionais ao estágio. Calibração institucional e integração com Git são **pós-MVP** (ver seção "Ideias Futuras").

---

## 🔗 Dependências do Core

Alguns épicos do Ensaio dependem de épicos do core. Ver [docs/ROADMAP.md](../../docs/ROADMAP.md):

- **Writer** (core C-ENSAIO-2): necessário desde a POC do Ensaio. Primeiro agente core motivado pelo Ensaio.
- **Ingestão de arquivos anexados** (core C-ENSAIO-4): necessário para o MVP do Ensaio.
- **Writer por seção** (core C-ENSAIO-3): necessário para o Protótipo (rascunho progressivo).
- **Parametrização de contexto de produto**: padrão pelo qual agentes do core recebem foco/domínio sem conhecer o produto consumidor (ver [core/docs/vision/super_system.md](../../core/docs/vision/super_system.md), seção "Injeção de Contexto de Produto").

---

## 🎯 Milestones

> **Convenção:** id no formato `<ESTAGIO>-<PRODUTO>` em caixa alta, com hífen (ver glossário em [docs/CONSTITUTION.md §9](../../docs/CONSTITUTION.md)). Branch associada em caixa baixa: `milestone/<id>`. Quando um estágio precisa de mais de um milestone, adicionar sufixo: `POC-ENSAIO-ALPHA`, `POC-ENSAIO-BETA`.

Milestone agrupa épicos relacionados dentro de um estágio. É a unidade de entrega do fluxo autônomo (`docs/process/autonomous/`) — disparo por linguagem natural ("implementa a POC do Ensaio"), execução na branch do milestone, merge em main apenas com aval humano.

### POC-ENSAIO

- **Objetivo:** entregar a primeira versão funcional do Ensaio como app próprio — o Usuário conversa sobre o experimento num chat simples e, sob demanda, aciona o Writer do core para gerar e refinar o artigo em markdown. Valida a hipótese de que agentes do core parametrizados por contexto de produto servem a um fluxo diferente do Revelar.
- **Estágio:** POC — Prova de Conceito
- **Produto:** Ensaio
- **Épicos agrupados:** E-POC-1, E-POC-2, E-POC-3
- **Dependências de core:** [C-ENSAIO-2](../../docs/ROADMAP.md) (Writer versão inicial) — pré-requisito de E-POC-3
- **Branch associada:** `milestone/poc-ensaio`
- **Status dos épicos:** ✅ Implementados (C-ENSAIO-2, E-POC-1, E-POC-2, E-POC-3) — validação manual executada, PR #TBD

### PROTO-ENSAIO

- **Status:** `🧭 Jornada alinhada`
- **Objetivo:** elevar a **qualidade** do POC usando coerentemente capacidades que já temos (Metodologista parado no core, Writer evoluindo para por-seção, persistência do LangGraph) num chassi de stack adequado. Protótipo **não inventa features novas** — usa melhor o que existe. Único artigo em andamento por vez; múltiplos projetos ficam para MVP/depois.
- **Estágio:** Protótipo — Usuário usa de verdade
- **Produto:** Ensaio
- **Épicos agrupados:** E-PROTO-1, E-PROTO-2, E-PROTO-3, E-PROTO-4, E-PROTO-5 (todos em `🌱 Visão` — funcionalidades e critérios para próxima sessão de refinamento)
- **Dependências de core:** [C-ENSAIO-3](../../docs/ROADMAP.md) (Writer por seção) — pré-requisito de E-PROTO-4.
- **Branch associada:** `milestone/proto-ensaio`
- **Glossário do produto:** termos "Usuário" (jornada) e "Pesquisador" (persona) ancorados em [products/ensaio/docs/vision.md §13](docs/vision.md).
- **Jornada alvo (alta-nível):** Usuário abre o app → continua no mesmo artigo, vê a última conversa e perguntas do sistema ainda em aberto → responde → Orquestrador/Estruturador organizam; Metodologista provoca quando a conversa toca em metodologia → clica "Gerar" ou "Regenerar seção X" → painel mostra artigo seccionado com edição inline → fecha e volta depois no mesmo ponto.
- **Feedback do POC endereçado por este milestone:**
  - Promessas vazias do Orquestrador/Estruturador ("vou validar...") → ajuste de prompt como **trabalho preparatório de entrada** do milestone (higiene pós-POC, commit antes do dispatch; não é épico).
  - Falta de transparência sobre qual agente está falando → detalhe dentro de **E-PROTO-1**: nova stack entrega bubble com label do agente (`🎯 Orquestrador`, `🔬 Metodologista`).
  - Feedback de processamento (blur opaco do Streamlit) → resolvido por **E-PROTO-1** — stack nova substitui o mecanismo.
  - Relação chat ↔ evento de geração / histórico confuso → **E-PROTO-3** (versões visíveis) + **E-PROTO-4** (painel seccionado com edição).
  - Carregamento inicial lento → **E-PROTO-1** — cold start aceitável vira critério da ADR da stack.
- **Escopo declinado:** proposta de E-PROTO-6 (higiene de UX no Streamlit) foi declinada — trabalho transitório que morreria com E-PROTO-1 (migração de stack). Único item que sobrevive à stack nova é o ajuste de prompt acima, listado como trabalho preparatório.
- **Sizing:** avaliação real (e eventual quebra em sub-milestones `ALPHA`/`BETA`) fica para quando a EM skill avaliar, antes do dispatch.

### MVP-ENSAIO (stub)

- **Objetivo:** a definir quando o milestone for refinado. Direção provável: habilitar uso por colegas próximos sem o desenvolvedor do lado — upload de artefatos do experimento, experiência de refinamento *ongoing* entre sessões longas e preparação mínima para compartilhamento.
- **Estágio:** MVP — Colegas Usam
- **Produto:** Ensaio
- **Épicos agrupados:** E-MVP-1, E-MVP-2, E-MVP-3
- **Dependências de core:** [C-ENSAIO-4](../../docs/ROADMAP.md) (Ingestão de arquivos anexados)
- **Branch associada:** `milestone/mvp-ensaio`
- **Status dos épicos:** todos em `🌱 Visão`
- **Nota:** milestone declarativo. Avaliação de sizing e quebra acontecem antes do dispatch.

---

## 📋 Épicos Planejados

### ⏳ Fase POC — Prova de Conceito

#### ÉPICO E-POC-1: App Streamlit Mínimo do Ensaio ✅

**Status:** ✅ Implementado — PR #TBD

**Entregue:** Esqueleto do app próprio do Ensaio em `products/ensaio/app/` (entrypoint `chat.py` com layout 60/40, grafo próprio em `graph.py` compondo Orquestrador + Estruturador, componentes `article_panel.py`, `generate_button.py`, `chat_input.py`; reuso de `chat_history.py` do Revelar via import direto; estado 100% em `st.session_state`).

**Referências:** `products/ensaio/app/`, `scripts/ensaio/flows/validate_graph.py`, `docs/ARCHITECTURE.md` (seção "Padrões de composição Core ↔ Produto").

---

#### ÉPICO E-POC-2: Configuração de Contexto de Produto para Agentes do Core ✅

**Status:** ✅ Implementado — PR #TBD

**Entregue:** YAML do produto (`products/ensaio/config/product.yaml`, campo único `focus`) + loader (`products/ensaio/app/product_config.py`) + injeção via `config.configurable.product_context` nos nós do core (Orquestrador, Estruturador, Writer). Revelar continua funcionando sem product_context (backward compatible).

**Referências:** `docs/ARCHITECTURE.md` (padrão "Injeção de contexto de produto"), `core/prompts/{orchestrator,structurer,writer}.py` (placeholder `{product_context_section}`), `tests/products/ensaio/unit/test_product_config.py`.

---

#### ÉPICO E-POC-3: Fluxo Conversacional do Ensaio ✅

**Status:** ✅ Implementado — PR #TBD

**Entregue:** Fluxo completo chat → gerar → refinar → regenerar. Entrada livre no chat (markdown preservado), conversa com Orquestrador + Estruturador em postura ativo-leve (sem Metodologista nesta fase), botão "Gerar artigo" / "Regenerar" invoca `writer_node` diretamente com histórico conversacional, artigo focal e `previous_article` em modo refinamento. Sessão 100% descartável — recarregar zera tudo.

**Refinamento pós-validação:** correção da perda da mensagem do usuário em erro de backend (bubble de erro mantém histórico), `cost_tracker` defensivo e precedência `LLM_MODEL > YAML`. Ver commit `04018e3`.

---

### ⏳ Fase Protótipo — Desenvolvedor Usa

#### ÉPICO E-PROTO-1: Migração de Stack da Interface

**Objetivo:** Decidir e implementar nova stack da interface do Ensaio, substituindo Streamlit. Primeira frente do Protótipo — a escolha exata de stack é parte do refinamento deste épico.

**Status:** 🌱 Visão

---

#### ÉPICO E-PROTO-2: Entidade Pendência no Produto

**Objetivo:** Item que fica aberto entre sessões. Sistema e Usuário podem criar. Pendências aparecem quando Usuário volta ao Ensaio, viabilizando o fluxo assíncrono.

**Status:** 🌱 Visão

**Nota:** Pendência é **entidade em incubação** — vive no Ensaio até que outro produto precise dela (ver [core/docs/architecture/data-models/ontology.md](../../core/docs/architecture/data-models/ontology.md), seção "Entidades em Incubação").

---

#### ÉPICO E-PROTO-3: Persistência do Artigo com Versões

**Objetivo:** Artigo sobrevive ao fim da sessão. Versões permitem rollback e comparação entre estados anteriores.

**Status:** 🌱 Visão

---

#### ÉPICO E-PROTO-4: UI de Artigo em Construção

**Objetivo:** Painel com seções do artigo, status por seção, edição inline do markdown. Viabiliza o modo de escrita híbrido (rascunho progressivo que evolui com a conversa).

**Status:** 🌱 Visão

**Dependências:**
- E-PROTO-1 (nova stack), E-PROTO-3 (persistência)

---

#### ÉPICO E-PROTO-5: Metodologista Aplicado ao Ensaio

**Objetivo:** Metodologista (agente do core existente) passa a identificar lacunas de produção no contexto do Ensaio — métricas ausentes, evidências faltantes, afirmações sem suporte — via parametrização de contexto, sem código específico por produto.

**Status:** 🌱 Visão

**Dependências:**
- E-POC-2 (parametrização de contexto)

---

### ⏳ Fase MVP — Colegas Usam

#### ÉPICO E-MVP-1: Upload de Arquivos do Experimento

**Objetivo:** Usuário anexa notebook, README, CSV, imagens de gráfico. Agentes leem e usam esses artefatos como contexto para a conversa e para o Writer.

**Status:** 🌱 Visão

---

#### ÉPICO E-MVP-2: Experiência de Refinamento *Ongoing*

**Objetivo:** Sessões longas maduras — pendências persistentes, rascunhos atuais, histórico do que mudou entre sessões. Refinamento contínuo do artigo ao longo de semanas.

**Status:** 🌱 Visão

**Dependências:**
- E-PROTO-2 (pendências), E-PROTO-3 (persistência), E-PROTO-4 (UI de artigo)

---

#### ÉPICO E-MVP-3: Preparação para Compartilhamento com Colegas

**Objetivo:** Setup mínimo para outra pessoa usar o Ensaio sem o desenvolvedor do lado. Forma exata (deploy, empacotamento local, etc.) é decidida no refinamento deste épico.

**Status:** 🌱 Visão

---

## 💡 Ideias Futuras

Backlog sem compromisso. Entram em planejamento quando fizer sentido, geralmente após o MVP.

- **Integração com Git:** leitura direta do repositório do experimento (código, histórico de commits, arquivos) para alimentar conversa e Writer sem uploads manuais.
- **One-pager como formato de saída alternativo:** suporte explícito ao UC2 (divulgação rápida) — formato compacto ao lado do artigo completo.
- **Múltiplas sessões de trabalho:** navegar entre vários artigos em construção simultaneamente.
- **Formatos além de markdown:** exportação para LaTeX, Word e outros formatos de publicação.
- **Calibração institucional:** sistema aprende com artigos de referência e práticas consolidadas da ICT — estilo, estruturas recorrentes, padrões de rigor, referências conhecidas.
- **Hub navegando entre Revelar e Ensaio:** ponto de entrada unificado do super-sistema, com transição entre produtos preservando contexto.
- **Compartilhamento / colaboração entre pesquisadores:** múltiplos pesquisadores trabalhando no mesmo artigo; comentários, revisão e autoria compartilhada.

---

> **📖 Melhorias Técnicas:** Para melhorias técnicas não vinculadas a épicos, consulte [docs/backlog.md](../../docs/backlog.md).

---

## 📚 Documentação

- `products/ensaio/docs/vision.md` - Visão do produto
- `products/ensaio/docs/poc_validation.md` - Checklist de validação manual da POC
- `core/docs/agents/writer/design.md` - Decisões arquiteturais do Writer
- `core/docs/vision/super_system.md` - Desacoplamento core ↔ produto

---

## 📝 Observações

**Regra:** fluxo manual via Cursor exige épico em `📋 Critérios definidos`; fluxo autônomo via Claude Code Web exige `🔍 Detalhes definidos`.

> Para o processo completo de refinamento, consulte [planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md). Para a prontidão ao fluxo autônomo (alvo `🔍`), consulte [autonomous_readiness.md](../../docs/process/refinement/autonomous_readiness.md). Para o fechamento do épico (saída), consulte [epic_completion.md](../../docs/process/refinement/epic_completion.md).

- Cada épico pode ser desenvolvido **isoladamente** dentro de sua fase
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos em `🌱 Visão` ou `📐 Funcionalidades esboçadas` passam por sessão de refinamento antes da implementação
