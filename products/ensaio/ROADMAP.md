# ROADMAP - Ensaio

Épicos e melhorias do produto Ensaio (transformar experimentos de código em artigos técnico-científicos).

> **📖 Visão:** Para entender a visão do produto, consulte [products/ensaio/docs/vision.md](docs/vision.md).

> **📖 Status Atual:** Para entender o estado técnico do sistema, consulte [ARCHITECTURE.md](../../ARCHITECTURE.md).

---

## 🧭 Filosofia de Estágios

Ensaio adota a progressão **POC → Protótipo → MVP** no eixo *quem usa* (ver [docs/process/refinement/planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md)):

- **POC:** prova que a ideia faz sentido. Pode ser tosco, rodar só no ambiente do desenvolvedor, ter atalhos explícitos.
- **Protótipo:** a ideia funciona e o **próprio desenvolvedor usa de verdade** no fluxo real dele.
- **MVP:** **outros** (colegas próximos) usam **sem o desenvolvedor do lado**.

Decisões de stack, UX e robustez são proporcionais ao estágio. Calibração institucional e integração com Git são **pós-MVP** (ver seção "Ideias Futuras").

---

## 🔗 Dependências do Core

Alguns épicos do Ensaio dependem de épicos do core. Ver [core/ROADMAP.md](../../core/ROADMAP.md):

- **Writer** (core C-ENSAIO-2): necessário desde a POC do Ensaio. Primeiro agente core motivado pelo Ensaio.
- **Ingestão de arquivos anexados** (core C-ENSAIO-4): necessário para o MVP do Ensaio.
- **Writer por seção** (core C-ENSAIO-3): necessário para o Protótipo (rascunho progressivo).
- **Parametrização de contexto de produto**: padrão pelo qual agentes do core recebem foco/domínio sem conhecer o produto consumidor (ver [core/docs/architecture/vision/super_system.md](../../core/docs/architecture/vision/super_system.md), seção "Injeção de Contexto de Produto").

---

## 📋 Épicos Planejados

### ⏳ Fase POC — Prova de Conceito

#### ÉPICO E-POC-1: App Streamlit Mínimo do Ensaio

**Objetivo:** Esqueleto de app próprio para o produto Ensaio, reusando componentes do Revelar onde couber. UI descartável — Streamlit como atalho, sem investimento em design.

**Status:** ⏳ Planejado (não refinado)

---

#### ÉPICO E-POC-2: Configuração de Contexto de Produto para Agentes do Core

**Objetivo:** YAML do Ensaio define foco/domínio que é injetado nos agentes do core sem que o core conheça o produto. Primeira aplicação concreta do padrão de injeção de contexto.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Padrão de injeção de contexto (ver core/docs/architecture/vision/super_system.md)

---

#### ÉPICO E-POC-3: Fluxo Conversacional do Ensaio

**Objetivo:** Pesquisador conversa sobre experimento, pede geração de artigo, recebe markdown, pede ajustes, Writer refaz. Artigo vive só na sessão — sem persistência, sem pendências, sem rascunho progressivo.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Core C-ENSAIO-2 (Writer versão inicial)
- E-POC-1, E-POC-2

---

### ⏳ Fase Protótipo — Desenvolvedor Usa

#### ÉPICO E-PROTO-1: Migração de Stack da Interface

**Objetivo:** Decidir e implementar nova stack da interface do Ensaio, substituindo Streamlit. Primeira frente do Protótipo — a escolha exata de stack é parte do refinamento deste épico.

**Status:** ⏳ Planejado (não refinado)

---

#### ÉPICO E-PROTO-2: Entidade Pendência no Produto

**Objetivo:** Item que fica aberto entre sessões. Sistema e pesquisador podem criar. Pendências aparecem quando pesquisador volta ao Ensaio, viabilizando o fluxo assíncrono.

**Status:** ⏳ Planejado (não refinado)

**Nota:** Pendência é **entidade em incubação** — vive no Ensaio até que outro produto precise dela (ver [core/docs/architecture/data-models/ontology.md](../../core/docs/architecture/data-models/ontology.md), seção "Entidades em Incubação").

---

#### ÉPICO E-PROTO-3: Persistência do Artigo com Versões

**Objetivo:** Artigo sobrevive ao fim da sessão. Versões permitem rollback e comparação entre estados anteriores.

**Status:** ⏳ Planejado (não refinado)

---

#### ÉPICO E-PROTO-4: UI de Artigo em Construção

**Objetivo:** Painel com seções do artigo, status por seção, edição inline do markdown. Viabiliza o modo de escrita híbrido (rascunho progressivo que evolui com a conversa).

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- E-PROTO-1 (nova stack), E-PROTO-3 (persistência)

---

#### ÉPICO E-PROTO-5: Metodologista Aplicado ao Ensaio

**Objetivo:** Metodologista (agente do core existente) passa a identificar lacunas de produção no contexto do Ensaio — métricas ausentes, evidências faltantes, afirmações sem suporte — via parametrização de contexto, sem código específico por produto.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- E-POC-2 (parametrização de contexto)

---

### ⏳ Fase MVP — Colegas Usam

#### ÉPICO E-MVP-1: Upload de Arquivos do Experimento

**Objetivo:** Pesquisador anexa notebook, README, CSV, imagens de gráfico. Agentes leem e usam esses artefatos como contexto para a conversa e para o Writer.

**Status:** ⏳ Planejado (não refinado)

---

#### ÉPICO E-MVP-2: Experiência de Refinamento *Ongoing*

**Objetivo:** Sessões longas maduras — pendências persistentes, rascunhos atuais, histórico do que mudou entre sessões. Refinamento contínuo do artigo ao longo de semanas.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- E-PROTO-2 (pendências), E-PROTO-3 (persistência), E-PROTO-4 (UI de artigo)

---

#### ÉPICO E-MVP-3: Preparação para Compartilhamento com Colegas

**Objetivo:** Setup mínimo para outra pessoa usar o Ensaio sem o desenvolvedor do lado. Forma exata (deploy, empacotamento local, etc.) é decidida no refinamento deste épico.

**Status:** ⏳ Planejado (não refinado)

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
- `core/docs/architecture/agents/writer.md` - Decisões arquiteturais do Writer
- `core/docs/architecture/vision/super_system.md` - Desacoplamento core ↔ produto

---

## 📝 Observações

**Regra:** Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte [planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md).

- Cada épico pode ser desenvolvido **isoladamente** dentro de sua fase
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem sessão de refinamento dedicada antes da implementação
