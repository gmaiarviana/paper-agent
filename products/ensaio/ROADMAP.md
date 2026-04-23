# ROADMAP - Ensaio

Épicos e melhorias do produto Ensaio (transformar experimentos de código em artigos técnico-científicos).

> **📖 Visão:** Para entender a visão do produto, consulte [products/ensaio/docs/vision.md](docs/vision.md).

> **📖 Status Atual:** Para entender o estado técnico do sistema, consulte [ARCHITECTURE.md](../../docs/ARCHITECTURE.md).

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

- **Objetivo:** entregar a primeira versão funcional do Ensaio como app próprio — o pesquisador conversa sobre o experimento num chat simples e, sob demanda, aciona o Writer do core para gerar e refinar o artigo em markdown. Valida a hipótese de que agentes do core parametrizados por contexto de produto servem a um fluxo diferente do Revelar.
- **Estágio:** POC — Prova de Conceito
- **Produto:** Ensaio
- **Épicos agrupados:** E-POC-1, E-POC-2, E-POC-3
- **Dependências de core:** [C-ENSAIO-2](../../docs/ROADMAP.md) (Writer versão inicial) — pré-requisito de E-POC-3
- **Branch associada:** `milestone/poc-ensaio`
- **Status dos épicos:** todos em `🏗️ Em andamento` (sessão autônoma entregou — aguarda validação manual via [poc_validation.md](docs/poc_validation.md) e merge)

### PROTO-ENSAIO (stub)

- **Objetivo:** a definir quando o milestone for refinado. Direção provável: fazer o Ensaio virar ferramenta de uso real do próprio desenvolvedor — substituir Streamlit por stack navegável, introduzir persistência do artigo com versões, painel de artigo em construção e pendências entre sessões.
- **Estágio:** Protótipo — Desenvolvedor Usa
- **Produto:** Ensaio
- **Épicos agrupados:** E-PROTO-1, E-PROTO-2, E-PROTO-3, E-PROTO-4, E-PROTO-5
- **Dependências de core:** [C-ENSAIO-3](../../docs/ROADMAP.md) (Writer por seção)
- **Branch associada:** `milestone/proto-ensaio`
- **Status dos épicos:** todos em `🌱 Visão`
- **Nota:** milestone declarativo. Sizing real (quebra em sub-milestones `ALPHA`/`BETA` etc.) fica para quando a EM skill avaliar, antes do dispatch.

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

#### ÉPICO E-POC-1: App Streamlit Mínimo do Ensaio

**Objetivo:** Esqueleto de app próprio para o produto Ensaio, reusando componentes do Revelar onde couber. UI descartável — Streamlit como atalho, sem investimento em design.

**Status:** 🏗️ Em andamento (entregue pela sessão autônoma do milestone POC-ENSAIO — aguardando validação manual do dev via `products/ensaio/docs/poc_validation.md`)

### Funcionalidades:

#### 1.1 Estrutura de pastas do produto

- **Descrição:** Esqueleto de diretórios e arquivos do app do Ensaio seguindo convenção do super-sistema. App próprio, não modo do Revelar.
- **Critérios de Aceite:**
  - Deve criar products/ensaio/app/ com __init__.py
  - Deve criar products/ensaio/config/ para product.yaml (E-POC-2)
  - Deve criar products/ensaio/app/components/ para componentes específicos do Ensaio (article_panel.py, generate_button.py)
  - Não deve criar estrutura sobreposta ao Revelar
- **Detalhes de execução:**
  - **Arquivos a criar:** `products/ensaio/app/__init__.py`, `products/ensaio/app/components/__init__.py`, `products/ensaio/config/` (diretório)
  - **Template de referência:** estrutura de `products/revelar/app/`
  - **Escopo de teste:** validação manual (diretórios existem)

#### 1.2 Entrypoint Streamlit

- **Descrição:** Arquivo chat.py como entrypoint do app do Ensaio, rodável via `streamlit run products/ensaio/app/chat.py`.
- **Critérios de Aceite:**
  - Deve existir products/ensaio/app/chat.py como entrypoint
  - Deve rodar sem erros em setup limpo (após instalar requirements)
  - Deve renderizar layout 60/40 (chat à esquerda, painel do artigo à direita)
  - Não deve exigir configuração adicional além da ANTHROPIC_API_KEY
- **Detalhes de execução:**
  - **Arquivos a criar:** `products/ensaio/app/chat.py`
  - **Contratos/Shapes:** script executável via `streamlit run products/ensaio/app/chat.py`; layout `st.columns([3, 2])` (chat esquerda, painel direita)
  - **Template de referência:** `products/revelar/app/chat.py`
  - **Acoplamentos verificados:** depende apenas de `ANTHROPIC_API_KEY` em `.env`
  - **Dependências de ordem:** depois de 1.1
  - **Escopo de teste:** validação manual (rodar app, conferir layout)

#### 1.3 Grafo LangGraph do Ensaio

- **Descrição:** Grafo conversacional com Orquestrador e Estruturador do core, em postura ativo-leve. Writer fica separado do grafo conversacional e é invocado sob demanda.
- **Critérios de Aceite:**
  - Deve existir products/ensaio/app/graph.py
  - Grafo conversacional deve incluir Orquestrador + Estruturador
  - Writer não deve fazer parte do grafo conversacional automático
  - Writer deve ser invocado diretamente pelo app quando usuário clicar "Gerar artigo"
  - Não deve incluir Metodologista neste épico
- **Detalhes de execução:**
  - **Arquivos a criar:** `products/ensaio/app/graph.py`
  - **Contratos/Shapes:** expõe função `create_ensaio_graph()` que retorna `StateGraph` compilado; grafo compõe apenas `orchestrator_node` e `structurer_node` importados do core; Writer fica fora do grafo
  - **Integração:** usa `MultiAgentState` do core (`core/agents/orchestrator/state.py`) como state; usa `route_from_orchestrator` do core para routing; `SqliteSaver` próprio em `data/ensaio_checkpoints.db`
  - **Template de referência:** `core/agents/multi_agent_graph.py` (para entender padrão de composição — Ensaio não reusa a função, compõe próprio grafo a partir dos nós)
  - **Acoplamentos verificados:** nós do core (`orchestrator_node`, `structurer_node`) são importáveis isoladamente e não dependem de Metodologista estar presente; `route_from_orchestrator` aceita estado sem metodologista no grafo (documentar comportamento esperado se rotear para methodologist)
  - **Decisão arquitetural:** produto compõe próprio grafo a partir dos nós do core — princípio do super-sistema (ver `docs/ARCHITECTURE.md` seção a ser adicionada no PROMPT 3)
  - **Dependências de ordem:** depois de 1.1
  - **Escopo de teste:** validação manual via `scripts/ensaio/flows/validate_graph.py` invocando o grafo com input fixo

#### 1.4 Reuso de componentes do Revelar

- **Descrição:** Componentes de UI genéricos (chat_input, chat_history) são reusados do Revelar via import direto, sem duplicação.
- **Critérios de Aceite:**
  - Deve importar chat_input e chat_history de products/revelar/app/components/
  - Não deve duplicar código desses componentes
  - Se padrão de reuso se consolidar, promover componentes para core/ui_components/ (ver docs/backlog.md)
- **Detalhes de execução:**
  - **Reuso direto via import:** `products/revelar/app/components/chat_history.py` (componente burro, sem acoplamento ao grafo)
  - **Arquivos a criar:** `products/ensaio/app/components/chat_input.py` (versão própria — o `chat_input` do Revelar está acoplado ao grafo do Revelar e ao `EventBus`; Ensaio precisa invocar seu próprio grafo)
  - **Template de referência para o chat_input do Ensaio:** `products/revelar/app/components/chat_input.py` (estrutura do form Streamlit e gestão de processing); simplificar removendo dependência de `EventBus` (POC sem métricas inline) e adaptar invocação para o grafo do Ensaio
  - **Acoplamentos verificados:** `chat_history.py` do Revelar lê apenas `st.session_state.messages` e não importa do core — reuso direto é seguro
  - **Dependências de ordem:** depois de 1.3
  - **Escopo de teste:** validação manual (mensagens renderizam no histórico após envio)

#### 1.5 Painel do artigo e botão de geração

- **Descrição:** Coluna direita exibe o artigo markdown gerado (quando existe) e botão "Gerar artigo" / "Regenerar" no topo.
- **Critérios de Aceite:**
  - Botão "Gerar artigo" deve estar visível desde o início da conversa (conforme 3.3)
  - Quando existe artigo em st.session_state, botão deve virar "Regenerar"
  - Artigo deve ser renderizado com st.markdown
  - Painel deve permanecer com artigo anterior até usuário clicar "Regenerar"
- **Detalhes de execução:**
  - **Arquivos a criar:** `products/ensaio/app/components/article_panel.py`, `products/ensaio/app/components/generate_button.py`
  - **Contratos/Shapes:** `article_panel` renderiza `st.session_state.current_article` com `st.markdown` quando existe; `generate_button` exibe "Gerar artigo" quando `current_article is None`, "Regenerar" caso contrário
  - **Integração:** botão invoca handler que chama Writer diretamente (detalhado em 3.3)
  - **Template de referência:** componentes de `products/revelar/app/components/` para padrão de componente Streamlit
  - **Dependências de ordem:** depois de 1.2
  - **Escopo de teste:** validação manual

#### 1.6 Gestão de estado em sessão

- **Descrição:** Todo estado (conversa, artigo, focal_argument) vive em st.session_state. Refresh da página zera tudo, conforme 3.5.
- **Critérios de Aceite:**
  - Deve usar st.session_state para: messages, focal_argument, current_article, generating
  - Não deve gravar em disco, banco ou qualquer persistência
  - Recarregar a página deve recomeçar do zero
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/chat.py`
  - **Contratos/Shapes:** chaves em `st.session_state` — `messages` (list), `focal_argument` (dict ou None), `current_article` (str ou None), `generating` (bool), `session_id` (str), `thread_id` (str)
  - **Integração:** inicialização em `chat.py` na primeira execução
  - **Acoplamentos verificados:** recarregar página zera `st.session_state` por padrão Streamlit — comportamento desejado
  - **Dependências de ordem:** depois de 1.2
  - **Escopo de teste:** validação manual (recarregar página recomeça do zero)

**Simplificações POC declaradas:**
- Sem persistência em disco além de checkpoints do LangGraph (sessão descartável por design)
- Sem testes automatizados de UI
- Sem métricas inline no chat (EventBus fora do escopo da POC)

---

#### ÉPICO E-POC-2: Configuração de Contexto de Produto para Agentes do Core

**Objetivo:** YAML do Ensaio define foco/domínio que é injetado nos agentes do core sem que o core conheça o produto. Primeira aplicação concreta do padrão de injeção de contexto.

**Status:** 🏗️ Em andamento (entregue pela sessão autônoma do milestone POC-ENSAIO — aguardando validação manual do dev via `products/ensaio/docs/poc_validation.md`)

**Dependências:**
- Padrão de injeção de contexto (ver core/docs/vision/super_system.md)

**Sequência:** Depende de C-ENSAIO-2 já implementado (Writer nasce com parâmetro `product_context`). Escopo efetivo deste épico é estender o padrão a Orquestrador e Estruturador.

### Funcionalidades:

#### 2.1 YAML de configuração do produto

- **Descrição:** Arquivo YAML no produto Ensaio descreve o foco do produto em prosa livre, sem schema rígido.
- **Critérios de Aceite:**
  - Deve existir products/ensaio/config/product.yaml
  - YAML deve conter campo `focus` com string descrevendo o produto Ensaio (pesquisador transformando experimento em artigo IMRaD)
  - YAML não deve conter nomes técnicos internos do super-sistema
  - Campo `focus` deve ser a única chave obrigatória
- **Detalhes de execução:**
  - **Arquivos a criar:** `products/ensaio/config/product.yaml`
  - **Contratos/Shapes:** YAML com único campo obrigatório `focus` (string descrevendo o produto Ensaio em prosa livre)
  - **Template de referência:** estrutura YAML simples (sem template específico; não replicar schema de `core/config/agents/*.yaml`)
  - **Escopo de teste:** validação manual

#### 2.2 Loader no produto

- **Descrição:** Função do app do Ensaio lê o YAML e retorna a string do foco pronta para ser injetada nos agentes do core.
- **Critérios de Aceite:**
  - Deve existir products/ensaio/app/product_config.py
  - Deve expor função que retorna a string do campo `focus`
  - Deve tratar YAML ausente ou malformado com erro claro
  - Não deve fazer import de nada do core
- **Detalhes de execução:**
  - **Arquivos a criar:** `products/ensaio/app/product_config.py`
  - **Contratos/Shapes:** expõe função `load_product_context() -> str` que lê o YAML e retorna o valor de `focus`; lança exceção com mensagem clara em PT-BR quando YAML ausente ou malformado
  - **Acoplamentos verificados:** módulo não importa nada de `core/`
  - **Template de referência:** `core/agents/memory/config_loader.py` (padrão de loader YAML com PyYAML)
  - **Dependências de ordem:** depois de 2.1
  - **Escopo de teste:** 1 unit test em `tests/products/ensaio/unit/test_product_config.py` cobrindo YAML válido, ausente e malformado

#### 2.3 Parâmetro opcional nos agentes do core

- **Descrição:** Agentes do core (Orquestrador, Estruturador, Writer) aceitam product_context como parâmetro opcional sem conhecer o produto consumidor.
- **Critérios de Aceite:**
  - Nós do core devem aceitar product_context opcional na invocação
  - Quando product_context vier preenchido, prompt do agente ganha seção "## CONTEXTO DO PRODUTO" populada com a string
  - Quando product_context vier vazio ou ausente, seção não aparece e comportamento atual é preservado
  - Core não deve importar nada de products/ensaio/
  - Nenhum agente do core deve conhecer nome de produtos
- **Detalhes de execução:**
  - **Arquivos a modificar:** `core/agents/orchestrator/nodes.py` (aceitar `product_context` via config do LangGraph), `core/agents/structurer/nodes.py` (idem), `core/prompts/orchestrator.py` (adicionar placeholder `{product_context}` em seção opcional), `core/prompts/structurer.py` (idem)
  - **Contratos/Shapes:** `product_context` chega via `config.configurable.product_context` do LangGraph; quando presente e não-vazio, prompt ganha seção "## CONTEXTO DO PRODUTO" populada com a string; quando ausente, seção some e comportamento é idêntico ao atual
  - **Integração:** Writer já aceita `product_context` por C-ENSAIO-2 — nada a modificar no Writer
  - **Acoplamentos verificados:** Revelar continua invocando sem passar `product_context` no config; prompts sem placeholder preenchido ficam sem a seção (validar via grep nos prompts e rodar o Revelar)
  - **Template de referência:** padrão atual de uso de `config.configurable` nos nós (ex: `active_idea_id` no `orchestrator_node`)
  - **Dependências de ordem:** depois de C-ENSAIO-2 implementado
  - **Escopo de teste:** validação manual rodando Revelar (sem `product_context`) e Ensaio (com `product_context`)

#### 2.4 Injeção no fluxo do Ensaio

- **Descrição:** App do Ensaio carrega o YAML uma vez e injeta a string em toda invocação dos agentes do core.
- **Critérios de Aceite:**
  - App deve carregar product_config na inicialização
  - Toda invocação de Orquestrador, Estruturador e Writer deve passar product_context
  - Revelar continua funcionando sem passar product_context (backward compatibility)
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/chat.py` (carregar `product_config` na inicialização), `products/ensaio/app/graph.py` (passar `product_context` no config ao invocar o grafo)
  - **Contratos/Shapes:** `product_context` carregado uma vez e injetado em toda invocação do grafo via `config={"configurable": {"product_context": ..., "thread_id": ...}}`
  - **Dependências de ordem:** depois de 2.2 e 2.3
  - **Escopo de teste:** validação manual (logs dos agentes devem mostrar seção "CONTEXTO DO PRODUTO" no prompt montado)

**Simplificações POC declaradas:**
- YAML com único campo (`focus`); sem schema validator dedicado
- Sem versionamento do YAML

---

#### ÉPICO E-POC-3: Fluxo Conversacional do Ensaio

**Objetivo:** Pesquisador conversa sobre experimento, pede geração de artigo, recebe markdown, pede ajustes, Writer refaz. Artigo vive só na sessão — sem persistência, sem pendências, sem rascunho progressivo.

**Status:** 🏗️ Em andamento (entregue pela sessão autônoma do milestone POC-ENSAIO — aguardando validação manual do dev via `products/ensaio/docs/poc_validation.md`)

**Dependências:**
- Core [C-ENSAIO-2](../../docs/ROADMAP.md) (Writer versão inicial)
- [E-POC-1](#épico-e-poc-1-app-streamlit-mínimo-do-ensaio) (App Streamlit mínimo do Ensaio)
- [E-POC-2](#épico-e-poc-2-configuração-de-contexto-de-produto-para-agentes-do-core) (Configuração de contexto de produto)

### Funcionalidades:

#### 3.1 Entrada livre no chat

- **Descrição:** Usuário descreve o experimento em prosa e cola blocos livres (trechos de código, tabelas, notas, saídas de terminal) em qualquer ordem, sem wizard nem campos obrigatórios.
- **Critérios de Aceite:**
  - Deve aceitar mensagens de texto livre no chat sem campos obrigatórios e sem wizard de preenchimento
  - Deve aceitar blocos markdown (código, tabelas, logs) colados em qualquer ordem na conversa
  - Deve preservar a formatação original de blocos markdown ao renderizar a mensagem (code fences, tabelas, indentação)
  - Não deve impor sequência predefinida (resumo → método → resultados) nem exigir identificação prévia do tipo de conteúdo colado
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/components/chat_input.py` (garantir `st.text_area` sem parsing especial)
  - **Contratos/Shapes:** mensagens do usuário vão cruas para `st.session_state.messages` como `HumanMessage`
  - **Dependências de ordem:** depois de E-POC-1
  - **Escopo de teste:** validação manual (colar bloco de código markdown preserva formatação)

#### 3.2 Conversa com Orquestrador + Estruturador

- **Descrição:** Reusar o Orquestrador Conversacional e o Estruturador do core no fluxo do Ensaio sem modificação comportamental, em postura ativo-leve — escutam, organizam e perguntam apenas quando algo está vago.
- **Critérios de Aceite:**
  - Deve invocar o Orquestrador Conversacional e o Estruturador existentes no core sem alterar o código desses agentes
  - Deve injetar o contexto de produto do Ensaio conforme E-POC-2 (foco/domínio via YAML)
  - Deve manter os agentes em postura ativo-leve: organizam o que foi dito e perguntam somente quando algo está vago
  - Não deve invocar o Metodologista neste épico (identificação de lacunas de produção é reservada a E-PROTO-5)
  - Não deve duplicar lógica de agentes no app do Ensaio — qualquer ajuste de comportamento é feito via parametrização de contexto
- **Detalhes de execução:**
  - **Arquivos a modificar:** nenhum código do core (reuso puro via grafo do Ensaio)
  - **Integração:** `chat_input.py` do Ensaio invoca `ensaio_graph` passando `product_context` no config
  - **Acoplamentos verificados:** Orquestrador e Estruturador operam sobre `MultiAgentState` do core sem modificação
  - **Dependências de ordem:** depois de E-POC-1 e E-POC-2
  - **Escopo de teste:** validação manual via conversa real

#### 3.3 Geração sob demanda

- **Descrição:** Comando e/ou botão "Gerar artigo" acionável a qualquer momento da conversa, que invoca o Writer com o histórico conversacional e o argumento focal do Estruturador e retorna o artigo completo em markdown em uma única invocação.
- **Critérios de Aceite:**
  - Deve oferecer comando e/ou botão "Gerar artigo" disponível em qualquer ponto da conversa, inclusive cedo
  - Deve invocar o Writer (C-ENSAIO-2) passando o histórico conversacional acumulado + o argumento focal do Estruturador
  - Deve receber do Writer o artigo completo em markdown em uma única invocação e exibi-lo no chat
  - Deve aceitar gerações prematuras sem bloquear — entender a qualidade dessas saídas faz parte da validação da POC
  - Não deve gerar o artigo por seções nem em streaming parcial (rascunho progressivo é escopo do Protótipo)
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/components/generate_button.py` (handler do clique)
  - **Contratos/Shapes:** handler importa `writer_node` diretamente de `core/agents/writer/nodes.py` e invoca como função Python (fora do grafo); input montado a partir de `st.session_state.messages`, `st.session_state.focal_argument`, `product_context`, `previous_article=None` (primeira geração)
  - **Integração:** resultado do Writer (`article`) salvo em `st.session_state.current_article`; `st.session_state.generating` controla feedback visual durante a chamada
  - **Template de referência:** padrão de invocação direta de nó (sem precedente no código atual — declarar como primeira aplicação)
  - **Dependências de ordem:** depois de C-ENSAIO-2 (Writer existe) e E-POC-1.5 (botão existe)
  - **Escopo de teste:** validação manual (clicar "Gerar artigo" em qualquer momento produz markdown no painel direito)

#### 3.4 Refinamento minimalista via feedback

- **Descrição:** Usuário pede mudanças ao artigo em linguagem natural no chat ("deixa mais conciso", "adiciona uma seção sobre X"); o Writer é reinvocado com o histórico conversacional acumulado + o artigo anterior e regenera o artigo inteiro.
- **Critérios de Aceite:**
  - Deve aceitar feedback em linguagem natural no próprio chat, sem formulário ou UI especializada
  - Deve reinvocar o Writer passando o histórico conversacional acumulado + o artigo anterior como entrada
  - Deve substituir o artigo vigente pela versão regenerada e mantê-la visível no chat
  - Não deve refinar o artigo por seção isoladamente (reservado a C-ENSAIO-3 / fase Protótipo)
  - Não deve versionar nem persistir versões anteriores do artigo (reservado a E-PROTO-3)
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/components/generate_button.py` (mesmo handler; muda label do botão baseado em `current_article`)
  - **Contratos/Shapes:** quando `current_article` preenchido, handler invoca `writer_node` com `previous_article=current_article` e `messages` atualizadas (feedback do usuário já está no histórico)
  - **Integração:** Writer regenera o artigo inteiro; substitui `st.session_state.current_article`
  - **Dependências de ordem:** depois de 3.3
  - **Escopo de teste:** validação manual (pedir "deixa mais conciso" no chat, clicar "Regenerar", conferir que artigo muda)

#### 3.5 Sessão única descartável

- **Descrição:** Estado da conversa e do artigo vive apenas em memória da sessão do navegador (Streamlit `st.session_state`); recarregar a página recomeça do zero.
- **Critérios de Aceite:**
  - Deve armazenar conversa e artigo gerado em `st.session_state` (ou equivalente em memória da sessão do navegador)
  - Deve recomeçar do zero ao recarregar a página, sem tentativa de restaurar estado anterior
  - Não deve gravar conversa ou artigo em disco, banco ou qualquer armazenamento persistente
  - Não deve expor UI de "salvar sessão", "retomar" ou "histórico" (persistência real entra em E-PROTO-3)
- **Detalhes de execução:**
  - **Coberto por E-POC-1.6**
  - **Acoplamentos verificados:** checkpoints do LangGraph são volumosos mas aceitos na POC (limpar manualmente `data/ensaio_checkpoints.db` quando quiser zerar)
  - **Escopo de teste:** validação manual

**Simplificações POC declaradas:**
- Sem indicadores de progresso por agente (sem EventBus)
- Sem versionamento do artigo entre regenerações (só o mais recente vive em `current_article`)
- Sem guardrail se usuário gera sem conversa prévia (Writer lida com defaults do prompt)

---

### ⏳ Fase Protótipo — Desenvolvedor Usa

#### ÉPICO E-PROTO-1: Migração de Stack da Interface

**Objetivo:** Decidir e implementar nova stack da interface do Ensaio, substituindo Streamlit. Primeira frente do Protótipo — a escolha exata de stack é parte do refinamento deste épico.

**Status:** 🌱 Visão

---

#### ÉPICO E-PROTO-2: Entidade Pendência no Produto

**Objetivo:** Item que fica aberto entre sessões. Sistema e pesquisador podem criar. Pendências aparecem quando pesquisador volta ao Ensaio, viabilizando o fluxo assíncrono.

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

**Objetivo:** Pesquisador anexa notebook, README, CSV, imagens de gráfico. Agentes leem e usam esses artefatos como contexto para a conversa e para o Writer.

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
