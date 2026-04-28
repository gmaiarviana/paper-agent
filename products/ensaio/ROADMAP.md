# ROADMAP - Ensaio

Épicos e melhorias do produto Ensaio (transformar experimentos de código em artigos técnico-científicos).

> **📖 Visão:** Para entender a visão do produto, consulte [products/ensaio/docs/vision.md](docs/vision.md).

> **📖 Status Atual:** Para entender o estado técnico do sistema, consulte [ARCHITECTURE.md](../../docs/ARCHITECTURE.md).

> **🧭 Estados dos épicos:** ver [planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md) para definições completas.

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

- **Objetivo:** elevar a qualidade da experiência dentro de uma sessão usando coerentemente capacidades que já temos (Metodologista parado no core, Writer evoluindo para por-seção) num chassi de stack adequado. Protótipo continua em sessão única e descartável; persistência, pendências e fluxo assíncrono migram para o MVP.
- **Estágio:** Protótipo — Usuário usa de verdade
- **Produto:** Ensaio
- **Épicos agrupados:** E-PROTO-1, E-PROTO-2, E-PROTO-3
- **Dependências de core:** [C-ENSAIO-3](../../docs/ROADMAP.md) (Writer por seção) — pré-requisito de E-PROTO-2
- **Stack adotada:** Reflex (Python full-stack). ADR em [products/ensaio/docs/adr/001-stack-do-prototipo.md](docs/adr/001-stack-do-prototipo.md).
- **Branch associada:** `claude/implement-essay-prototype-uFkkP`
- **Status dos épicos:** ✅ Implementados (E-PROTO-1, E-PROTO-2, E-PROTO-3) — PR #97 (merge `1d592d0`, 2026-04-27), validação manual executada

### PROTO-ENSAIO-2

- **Objetivo:** Tornar visível o raciocínio dos agentes e dar ao Usuário voz antes que decisões dos agentes virem estado. Ataca pontos em que o PROTO-ENSAIO produziu sessão funcional mas opaca: Estruturador decidindo sozinho, Metodologista com papel embolado e por isso ausente, mensagens longas que escondem o que mudou, painel de seções sem accordion.
- **Estágio:** Protótipo
- **Produto:** Ensaio
- **Status:** `🧭 Jornada alinhada`
- **Épicos agrupados:** E-PROTO2-1, E-PROTO2-2, E-PROTO2-3, E-PROTO2-4
- **Dependências:** PROTO-ENSAIO ✅
- **Branch associada:** `milestone/proto-ensaio-2` (a criar)

**Jornada alvo (sessão ideal pós-milestone):**

Usuário descreve experimento. Em algum momento — emergente da conversa, não em ordem fixa — o Metodologista provoca sobre escopo e qualidade da mensagem: tese central, evidência, intenção do artigo. Em outro momento, o Estruturador **propõe** storytelling com racional curto; a proposta aparece como bubble especial com aceitar / editar leve / recusar, e só vira `current_article` após o aceite. Mensagens dos agentes que tocam estado vêm com manchete pequena ("📐 Estrutura proposta", "🎯 Foco atualizado", "🔬 Lacuna apontada") acima do texto, deixando claro o que aconteceu antes do Usuário ler tudo. No painel direito, seções ficam colapsadas por padrão; o Usuário expande aquelas em que está trabalhando.

**O que é:**
- Co-decisão da estrutura (proposta → confirmação/edição → estado).
- Limpeza dos prompts do core: Estruturador cobre storytelling; Metodologista cobre escopo + qualidade. Sobreposição atual (Metodologista falando de estrutura/formato) é eliminada.
- Manchete de "o que mudou" em mensagens de agentes que tocam estado.
- Colapsar/expandir seções, colapsado por padrão.

**O que não é:**
- Persistência entre sessões (MVP-ENSAIO).
- Loop de refinamento por seção / guardrails de contexto / ordem de geração de seção (PROTO-ENSAIO-3).
- Histórico ou diff entre versões da estrutura (Ideias Futuras).
- Gatilhos determinísticos de invocação dos agentes (ver restrição de fluidez abaixo).

**Restrição dura — conversa fluida:**

A conversa entre Usuário e agentes permanece fluida. O Orquestrador continua decidindo *quando* convocar quem; o milestone **não impõe ordem mandatória entre Metodologista e Estruturador**. O milestone entrega clareza de papéis e gatilhos legíveis, não máquina de passos. Esta restrição é não-negociável: implementação que amarre sequência fixa Metodologista→Estruturador no grafo viola o escopo.

**Glossário ancorado:**
- **Storytelling (Estruturador):** decisão sobre ordem e sequência do que será dito. *Como* contar.
- **Escopo / qualidade da mensagem (Metodologista):** decisão sobre tese central, evidência, intenção do artigo. *O que* é dito e se sustenta.
- **Co-decisão de estrutura:** ciclo proposta → aceitar/editar/recusar → commit no estado. Substitui o commit automático atual em `products/ensaio/app/state.py:159-173`.
- **Manchete de mudança ("what changed"):** linha curta no bubble que sumariza qual estado foi tocado, antes do conteúdo livre. Campo aditivo em `AIMessage.additional_kwargs`.

**Acoplamentos com core:**
- E-PROTO2-1: prompt e contrato de saída do Estruturador (`core/agents/structurer/`).
- E-PROTO2-2: prompt do Metodologista (`core/prompts/methodologist_provocation.py`); postura do Orquestrador em `products/ensaio/config/product.yaml`.
- E-PROTO2-3: contrato `change_summary` em `AIMessage.additional_kwargs` (aditivo, opcional, cruza core ↔ produto).
- E-PROTO2-4: puro UI (`products/ensaio/app/components/article_panel.py`), sem acoplamento com core.

**Feedback do estágio anterior endereçado:**
- "Estruturador propôs sem expor racional nem pedir confirmação" (validação PROTO-ENSAIO) → E-PROTO2-1.
- "Mensagem do Estruturador longa sem sinalizar o que o sistema fez" → E-PROTO2-3.
- "'Vou estruturar essa nova questão de pesquisa' — usuário não entendeu o que mudou" → E-PROTO2-3.
- "Metodologista existe mas não aparece no chat" → E-PROTO2-2 (papel afiado torna a presença legível quando convocado).
- "Seções do artigo não podem ser colapsadas/expandidas" → E-PROTO2-4.

**Nota:** milestone em `🧭 Jornada alinhada` — épicos individualmente em `📐 Funcionalidades esboçadas`. Critérios de aceite ficam para refinamento tático pela PM skill dentro da branch. Sizing avaliado antes do dispatch.

### PROTO-ENSAIO-3 (stub)

- **Objetivo:** Garantir qualidade antes de gerar, não depois. Endereça: Writer que gera sem contexto suficiente; ausência de ordem de geração; loop de refinamento por seção inexistente.
- **Estágio:** Protótipo
- **Produto:** Ensaio
- **Status:** `🌱 Visão`
- **Feedback capturado (validação PROTO-ENSAIO):**
  - Sistema não verifica se tem contexto suficiente antes de gerar uma seção
  - Não há ordenamento (conclusão deveria vir por último)
  - Usuário não tem como indicar o que está bom/ruim em cada seção para refinar
  - Favorecer qualidade sobre quantidade
- **Épicos planejados (a detalhar no refinamento):** E-PROTO3-1 Guardrails de contexto por seção, E-PROTO3-2 Ordem de geração guiada, E-PROTO3-3 Loop de refinamento por seção
- **Dependências:** PROTO-ENSAIO-2 (transparência deve estar resolvida antes de trabalhar qualidade)
- **Branch associada:** `milestone/proto-ensaio-3` (a criar)

### MVP-ENSAIO (stub)

- **Objetivo:** habilitar uso por colegas próximos sem o desenvolvedor do lado, em fluxo assíncrono real — persistência do artigo entre sessões, pendências como entidade que atravessa o tempo, upload de artefatos do experimento e preparação mínima para outro rodar.
- **Estágio:** MVP — Colegas Usam
- **Produto:** Ensaio
- **Épicos agrupados:** E-MVP-1 (Persistência), E-MVP-2 (Pendências entre sessões), E-MVP-3 (Upload de artefatos), E-MVP-4 (Preparação mínima para outro rodar)
- **Dependências de core:** [C-ENSAIO-4](../../docs/ROADMAP.md) (Ingestão de arquivos anexados) — pré-requisito de E-MVP-3
- **Branch associada:** `milestone/mvp-ensaio`
- **Status dos épicos:** todos em `🌱 Visão`
- **Re-escopo (2026-04):** persistência (antigo E-PROTO-3) e pendências entre sessões (antigo E-PROTO-2) migraram do Protótipo para cá, por dependência conceitual entre si e por coerência com o critério de saída do MVP (outros usam, em sessões múltiplas). O antigo "E-MVP-2: Experiência de Refinamento *ongoing*" foi dissolvido — persistência e pendências viraram épicos próprios; histórico detalhado entre sessões foi para Ideias Futuras.
- **Nota:** milestone declarativo. Critérios e detalhamento ficam para refinamento próprio quando o Protótipo amadurecer. Avaliação de sizing e quebra acontecem antes do dispatch.

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

#### ÉPICO E-PROTO-1: Migração de Stack da Interface (Reflex) ✅

**Status:** ✅ Implementado — PR #97 (merge `1d592d0`, 2026-04-27)

**Entregue:** Substituição do Streamlit por Reflex (Python full-stack) com layout chat + painel seccionado, transparência de agente nos bubbles via `AIMessage.additional_kwargs["agent"]` (Orquestrador, Estruturador, Metodologista, Writer), feedback de processamento inline (sem overlay opaco) e estado serializável em `EnsaioState` no backend.

**Referências:** `products/ensaio/app/` (entrypoint Reflex, `state.py`, `chat_panel.py`, `article_panel.py`), `products/ensaio/docs/adr/001-stack-do-prototipo.md` (decisão de stack), `core/agents/{orchestrator,structurer,methodologist}/nodes.py` (metadata `agent` em `additional_kwargs`).

---

#### ÉPICO E-PROTO-2: Rascunho Progressivo por Seção (Modo Híbrido) ✅

**Status:** ✅ Implementado — PR #97 (merge `1d592d0`, 2026-04-27)

**Entregue:** Modo de escrita híbrido dentro da sessão. Estruturador propõe estrutura do artigo no chat (lista de seções via `additional_kwargs["article_sections"]`), painel renderiza cada `Section` como bloco com badge de status (`empty`/`draft`/`edited`), botões "Gerar"/"Regenerar" por seção invocam `writer_section_node` com `article_context` montado a partir das demais seções, edição inline via `rx.textarea` preserva o conteúdo das outras seções.

**Referências:** `products/ensaio/app/components/article_panel.py`, `products/ensaio/app/state.py` (event handlers `generate_section`, `update_section_content`), `core/agents/writer/nodes.py` (`writer_section_node`), `core/agents/writer/models.py` (`Article`/`Section`).

---

#### ÉPICO E-PROTO-3: Metodologista Aplicado ao Ensaio ✅

**Status:** ✅ Implementado — PR #97 (merge `1d592d0`, 2026-04-27)

**Entregue:** Novo nó `methodologist_provocation_node` no core (separado e independente do `decide_collaborative` existente, que permanece inalterado), registrado como nó `"methodologist"` no grafo do Ensaio. Postura seletiva via instrução no `product.yaml` — Orquestrador sugere o Metodologista quando a conversa toca em metodologia, métricas ou afirmações sem suporte. Prompt cobre lacunas de rigor + as 4 dimensões do Writer (contexto, intenção, formato, estrutura).

**Referências:** `core/agents/methodologist/nodes.py` (`methodologist_provocation_node`), `core/prompts/methodologist_provocation.py` (`METHODOLOGIST_PROVOCATION_PROMPT_V1`), `products/ensaio/app/graph.py` (registro do nó), `products/ensaio/config/product.yaml` (postura seletiva + anti-promessa-vazia).

---

#### ÉPICO E-PROTO2-1: Co-decisão da Estrutura (storytelling)

**Status:** 📐 Funcionalidades esboçadas

**Objetivo:** Tornar a estrutura proposta pelo Estruturador um ato de co-decisão. O Estruturador propõe storytelling com racional curto; a proposta vira bubble especial e só comita em `current_article` após o Usuário aceitar (com possibilidade de edição leve antes).

### Funcionalidades (esboço):
- E-PROTO2-1.1 Proposta sem commit — Estruturador entrega seções e racional via `additional_kwargs`; `state.py` deixa de escrever direto em `current_article`, passa a manter uma proposta pendente.
- E-PROTO2-1.2 Bubble de proposta pendente com ações aceitar / editar / recusar.
- E-PROTO2-1.3 Edição leve da proposta antes do aceite — renomear, reordenar, remover, adicionar seções.
- E-PROTO2-1.4 Prompt do Estruturador afiado para storytelling apenas — sai cobertura de métricas/evidências/intenção (migra para E-PROTO2-2).

**Dependências:** PROTO-ENSAIO ✅. Acoplado a E-PROTO2-2 (limpeza de prompts é trabalho conjunto entre Estruturador e Metodologista).

---

#### ÉPICO E-PROTO2-2: Metodologista com escopo e qualidade afiados

**Status:** 📐 Funcionalidades esboçadas

**Objetivo:** Dar ao Metodologista papel claro e único — escopo e qualidade da mensagem. Eliminar a sobreposição atual com o Estruturador, deixando o Metodologista provocar sobre tese central, evidência, afirmação sem suporte e intenção do artigo. Visibilidade emerge da clareza de papel quando o Orquestrador convoca, não de gatilhos determinísticos no grafo.

### Funcionalidades (esboço):
- E-PROTO2-2.1 Prompt do Metodologista limpo — cobre só escopo + qualidade da mensagem (sai "estrutura" e "formato"; entra ênfase em tese, evidência, intenção do artigo).
- E-PROTO2-2.2 Postura do Orquestrador em `product.yaml` revisada para refletir os papéis novos — sem amarrar ordem entre Metodologista e Estruturador.
- E-PROTO2-2.3 Sem gancho determinístico no grafo — roteamento permanece via Orquestrador. Restrição de fluidez do milestone respeitada.

**Dependências:** PROTO-ENSAIO ✅. Acoplado a E-PROTO2-1 (limpeza de prompts é trabalho conjunto).

---

#### ÉPICO E-PROTO2-3: Manchete "o que mudou" em mensagens de agente

**Status:** 📐 Funcionalidades esboçadas

**Objetivo:** Cada mensagem de agente que toca estado passa a vir com manchete pequena acima do conteúdo, sumarizando qual estado foi tocado (estrutura proposta, foco atualizado, lacuna apontada). Usuário deixa de precisar ler parágrafo inteiro para descobrir o que aconteceu.

### Funcionalidades (esboço):
- E-PROTO2-3.1 Contrato `change_summary` em `AIMessage.additional_kwargs` — campo aditivo, opcional. Agentes que mudam estado preenchem; agentes em turno conversacional puro não preenchem.
- E-PROTO2-3.2 Renderização da manchete no bubble — header curto + conteúdo abaixo. Quando o campo está ausente, bubble fica como hoje.
- E-PROTO2-3.3 Casos cobertos no marco do milestone — Estruturador propondo/atualizando estrutura, mudança de `focal_argument`, Metodologista apontando lacuna.

**Dependências:** PROTO-ENSAIO ✅.

---

#### ÉPICO E-PROTO2-4: Colapsar/expandir seções no painel

**Status:** 📐 Funcionalidades esboçadas

**Objetivo:** Painel de seções deixa de renderizar tudo expandido. Toggle por seção, todas colapsadas por padrão no estado inicial. Usuário foca no que está trabalhando.

### Funcionalidades (esboço):
- E-PROTO2-4.1 Accordion no painel — cada seção colapsa/expande individualmente.
- E-PROTO2-4.2 Estado inicial — todas colapsadas. Sem persistir preferência (sessão é descartável até MVP-ENSAIO).

**Dependências:** PROTO-ENSAIO ✅. Puro UI, sem acoplamento com core.

---

### ⏳ Fase MVP — Colegas Usam

#### ÉPICO E-MVP-1: Persistência do Artigo entre Sessões

**Objetivo:** Artigo (e estado mínimo da conversa associado) sobrevive ao fim da sessão. Usuário fecha o app e, na próxima abertura, retoma o artigo de onde parou. Origem: re-escopo de 2026-04 — antes era E-PROTO-3 no Protótipo, migrado para o MVP por dependência conceitual com pendências e por coerência com o critério de saída ("outros usam, em sessões múltiplas").

**Status:** 🌱 Visão

**Dependências:**
- E-PROTO-2 (estado do artigo já estruturado por seção)

---

#### ÉPICO E-MVP-2: Pendências entre Sessões como Entidade Central

**Objetivo:** Pendência (item aberto entre sessões — pergunta sem resposta, evidência a coletar, rascunho esperando revisão, sugestão de agente aguardando decisão) vira superfície principal da tela inicial. Sistema e Usuário podem criar; Usuário fecha pendências ao longo das sessões. Viabiliza o fluxo assíncrono real (visão §3, §6). Origem: re-escopo de 2026-04 — antes era E-PROTO-2 no Protótipo.

**Status:** 🌱 Visão

**Nota:** Pendência é **entidade em incubação** — vive no Ensaio até que outro produto precise dela (ver [core/docs/architecture/data-models/ontology.md](../../core/docs/architecture/data-models/ontology.md), seção "Entidades em Incubação").

**Dependências:**
- E-MVP-1 (persistência — pendência sem persistência não atravessa nada)
- E-PROTO-3 (Metodologista — principal produtor sistêmico de pendências de rigor)

---

#### ÉPICO E-MVP-3: Upload de Arquivos do Experimento

**Objetivo:** Usuário anexa notebook, README, CSV, imagens de gráfico. Agentes leem e usam esses artefatos como contexto para a conversa e para o Writer.

**Status:** 🌱 Visão

**Dependências:**
- [C-ENSAIO-4](../../docs/ROADMAP.md) (Ingestão de arquivos anexados no core)

---

#### ÉPICO E-MVP-4: Preparação Mínima para Outro Rodar

**Objetivo:** Setup suficiente para colega próximo usar o Ensaio sem desenvolvedor do lado — instruções de execução, mensagens de erro inteligíveis, estado previsível. Sem polish: onboarding gamificado, deploy hospedado real, telemetria e mensagens de erro elaboradas ficam para Ideias Futuras / pós-MVP. Forma exata (rodagem local + Tailscale, empacotamento simples, etc.) é decidida no refinamento deste épico.

**Status:** 🌱 Visão

---

## 💡 Ideias Futuras

Backlog sem compromisso. Entram em planejamento quando fizer sentido, geralmente após o MVP.

- **Múltiplos artigos em paralelo:** Usuário trabalha em vários artigos simultaneamente, alterna entre eles, vê dashboard de progresso por artigo. (Re-escopo 2026-04: explicitamente fora do Protótipo e do MVP — único artigo em andamento por vez basta para validar uso por colega próximo.)
- **Histórico detalhado de mudanças entre sessões:** "o que mudou desde minha última sessão" — diff conversacional, histórico de versões do artigo por seção, log de pendências fechadas/abertas. (Re-escopo 2026-04: extraído do antigo E-MVP-2 "Refinamento *ongoing*"; estado atual + última pendência aberta basta para o MVP.)
- **Versões/rollback do artigo:** comparação entre estados anteriores do artigo, voltar para uma versão anterior de uma seção. (Re-escopo 2026-04: re-geração sobrescreve o artigo focal no Protótipo e no MVP; histórico estruturado de versões só quando houver demanda real.)
- **Deploy hospedado, multi-tenant, autenticação real:** Ensaio rodando como serviço, sem o colega precisar instalar nada localmente. (Re-escopo 2026-04: explicitamente pós-MVP — para o MVP, rodagem local + Tailscale ou similar basta.)
- **Polish de produto (UX/onboarding/telemetria):** onboarding gamificado, mensagens de erro elaboradas, telemetria de uso, tutoriais embutidos. (Re-escopo 2026-04: explicitamente pós-MVP — para o MVP basta sistema previsível e mensagens de erro inteligíveis.)
- **Integração com Git:** leitura direta do repositório do experimento (código, histórico de commits, arquivos) para alimentar conversa e Writer sem uploads manuais.
- **One-pager como formato de saída alternativo:** suporte explícito ao UC2 (divulgação rápida) — formato compacto ao lado do artigo completo.
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
