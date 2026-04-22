# ROADMAP - Core Universal

Épicos e melhorias do sistema core que serve todos os produtos.

> **📖 Status Atual:** Para entender o estado atual do core, consulte [ARCHITECTURE.md](ARCHITECTURE.md) e [core/docs/](../core/docs/).

> **📖 Visão:** Para entender a filosofia do sistema, consulte [core/docs/vision/system_philosophy.md](../core/docs/vision/system_philosophy.md).

### 🧭 Estados dos Épicos

Cada épico percorre até seis estados. Detalhes em [process/refinement/planning_guidelines.md](process/refinement/planning_guidelines.md).

- **`🌱 Visão`** — apenas objetivo definido. Aguarda refinamento.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Pronto para fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist em [autonomous_readiness.md](process/refinement/autonomous_readiness.md) aplicado. Pronto para fluxo autônomo via Claude Code Web.
- **`🏗️ Em andamento`** — implementação em curso, até o ciclo de fechamento.
- **`✅ Implementado`** — ciclo de fechamento executado (ver [epic_completion.md](process/refinement/epic_completion.md)).

> **Retroatividade:** épicos concluídos antes da introdução do modelo de 6 estados permanecem em formato simplificado (título ✅ + 1-2 linhas de resumo) e não são reclassificados retroativamente. O modelo aplica-se a épicos em andamento e futuros.

---

## 🎯 Épicos Core × Milestones de Produto

> **Nota:** O core não tem milestones próprios — seus épicos são consumidos pelos milestones dos produtos. Épicos motivados por produto (prefixo `C-<PRODUTO>-`) declaram aqui qual milestone de produto os consome, para que o dispatch do milestone saiba que precisa tê-los implementados como dependência. Convenção de id de milestone em [docs/CONSTITUTION.md §9](CONSTITUTION.md).

| Épico Core | Status | Milestone consumidor | Produto |
|------------|--------|----------------------|---------|
| ÉPICO 1 (Pesquisador) | 🌱 Visão | — (não vinculado) | — |
| C-ENSAIO-1 (Parametrização de Contexto) | 🌱 Visão | POC-ENSAIO | Ensaio |
| C-ENSAIO-2 (Writer versão inicial) | 🔍 Detalhes definidos | POC-ENSAIO | Ensaio |
| C-ENSAIO-3 (Writer por seção) | 🌱 Visão | PROTO-ENSAIO | Ensaio |
| C-ENSAIO-4 (Ingestão de arquivos anexados) | 🌱 Visão | MVP-ENSAIO | Ensaio |
| C-ENSAIO-5 (Pendência — condicional) | 🌱 Visão (condicional) | — (sem milestone até segundo consumidor aparecer) | — |
| C-ENSAIO-6 (Componentes de UI — condicional) | 🌱 Visão (condicional) | — (sem milestone até gatilho de ativação) | — |

Épicos sem coluna "Milestone consumidor" preenchida não entram em nenhum milestone de produto até que um gatilho apareça. Mudanças de vínculo são feitas editando esta tabela.

---

## 📋 Épicos Planejados

### 🌱 Épicos em Visão

#### ÉPICO 1: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** 🌱 Visão

**Dependências:**
- Revelar ÉPICO 2 (Catálogo de Conceitos)

**Nota:** Pesquisador pode usar catálogo de conceitos para buscar papers relacionados.

**Próximos Passos:**
- Discutir comportamento e interface antes do refinamento
- Definir integração com Observer e catálogo de conceitos

---

### 🌱 Épicos Motivados pelo Ensaio (em Visão)

> **Nota:** Estes épicos são **motivados pelo produto Ensaio** (primeiro produto com necessidades além das do Revelar) mas **pertencem ao core** — serão reusados por outros produtos, especialmente Produtor Científico. O prefixo `C-ENSAIO-` identifica a motivação; o código fica no core e respeita o desacoplamento descrito em [core/docs/vision/super_system.md](../core/docs/vision/super_system.md).

#### ÉPICO C-ENSAIO-1: Parametrização de Contexto de Produto nos Agentes

**Objetivo:** Agentes do core (Orquestrador e futuros) aceitam foco/domínio passado por produtos externos sem que o core conheça os produtos. Mecanismo de configuração a definir no refinamento.

**Status:** 🌱 Visão

**Consulte:** [core/docs/vision/super_system.md](../core/docs/vision/super_system.md) (seção "Injeção de Contexto de Produto")

---

#### ÉPICO C-ENSAIO-2: Writer (Versão Inicial)

**Objetivo:** Novo agente no core que recebe contexto conversacional e cognitive_model, devolve markdown estruturado. Nasce simples. Organizado para generalização futura (Produtor Científico reusará).

**Status:** 🔍 Detalhes definidos

**Decisões arquiteturais já tomadas:** ver [core/docs/agents/writer/design.md](../core/docs/agents/writer/design.md)
- Nasce no core (não no Ensaio)
- Começa simples: nó que recebe contexto e devolve markdown
- Estruturas de artigo vivem no prompt do Writer (não em enum/schema)
- Organização inicial antecipa generalização para o Produtor Científico

**Simplificações POC declaradas:**
- Sem testes de integração (cobertura por validação manual via script)
- Sem streaming ou geração por seção (escopo do épico C-ENSAIO-3)
- Sem versionamento de output (estado no consumidor)

### Funcionalidades:

#### C-ENSAIO-2.1 Nó Writer simples em uma passada

- **Descrição:** Nó LangGraph que recebe contexto e devolve markdown do artigo em uma única invocação. Sem loop interno, sem estado entre invocações.
- **Critérios de Aceite:**
  - Deve existir módulo core/agents/writer/ seguindo padrão dos outros agentes (__init__.py, nodes.py)
  - Deve expor função writer_node invocável isoladamente
  - Deve receber dict com as chaves: messages, focal_argument, previous_article, product_context
  - Deve retornar dict contendo string markdown em uma chave (ex: "article")
  - Não deve manter estado entre invocações
  - Não deve ter loop interno de refinamento
- **Detalhes de execução:**
  - **Arquivos a criar:** `core/agents/writer/__init__.py`, `core/agents/writer/nodes.py`
  - **Arquivos a modificar:** nenhum
  - **Contratos/Shapes:** input é dict com chaves `messages` (lista de mensagens LangChain), `focal_argument` (dict ou None), `previous_article` (str ou None), `product_context` (str ou None); output é dict com chave `article` (str com markdown do artigo)
  - **Integração:** nó isolado invocado diretamente por produtos — sem integração com `core/agents/multi_agent_graph.py` nesta versão
  - **Template de referência:** `core/agents/structurer/nodes.py` (também é nó simples, mesma estrutura)
  - **Acoplamentos verificados:** LLM via `langchain_anthropic.ChatAnthropic` como o `structurer_node`; sem dependência de `MultiAgentState` ou `EventBus` nesta versão
  - **Dependências de ordem:** nenhuma (primeiro da sequência da POC)
  - **Escopo de teste:** 1 unit test em `tests/core/unit/test_writer.py` validando que `writer_node` retorna dict com chave `article` quando invocado com input mínimo (mock do LLM)

#### C-ENSAIO-2.2 Prompt com IMRaD e defaults

- **Descrição:** Prompt do Writer contém base de conhecimento sobre estrutura IMRaD. Writer infere intenção e narrativa da conversa, com defaults razoáveis quando não há pistas claras.
- **Critérios de Aceite:**
  - Prompt em core/prompts/writer.py como WRITER_PROMPT_V1
  - Prompt descreve estrutura IMRaD (abstract, introdução, métodos, resultados, discussão, conclusão, referências)
  - Prompt orienta Writer a inferir intenção da conversa
  - Prompt define default "informar" quando intenção não emergir
  - Prompt não contém nome de produto específico (Ensaio, etc)
- **Detalhes de execução:**
  - **Arquivos a criar:** `core/prompts/writer.py`
  - **Contratos/Shapes:** expõe constante `WRITER_PROMPT_V1` (string) com placeholders para `focal_argument`, `previous_article`, `product_context`
  - **Integração:** importado por `core/agents/writer/nodes.py`
  - **Template de referência:** `core/prompts/structurer.py` (estrutura de prompt com placeholders)
  - **Comportamento com `focal_argument` vazio ou parcial:** prompt orienta Writer a usar defaults IMRaD (abstract, introdução, métodos, resultados, discussão, conclusão, referências) e inferir da conversa o que puder
  - **Escopo de teste:** validação manual via script (ver 2.1)

#### C-ENSAIO-2.3 Configuração YAML

- **Descrição:** Configuração externa do Writer via YAML, seguindo padrão dos outros agentes do core.
- **Critérios de Aceite:**
  - Arquivo core/config/agents/writer.yaml com campos: prompt (referência), model, context_limits, metadata
  - Modelo padrão: claude-3-5-haiku-20241022
  - Deve ser carregável pelo config_loader existente
  - Deve validar com config_validator existente
- **Detalhes de execução:**
  - **Arquivos a criar:** `core/config/agents/writer.yaml`
  - **Arquivos a modificar:** nenhum (reusa `config_loader` existente)
  - **Contratos/Shapes:** YAML com campos `prompt` (referência a `WRITER_PROMPT_V1`), `model` (`claude-3-5-haiku-20241022`), `context_limits` (`max_input_tokens`, `max_output_tokens`, `max_total_tokens`), `metadata`
  - **Template de referência:** `core/config/agents/structurer.yaml`
  - **Acoplamentos verificados:** `core/agents/memory/config_loader.py` carrega via padrão existente sem modificação; `core/agents/memory/config_validator.py` valida schema sem mudança
  - **Escopo de teste:** validação manual carregando o YAML pelo `config_loader` em script

#### C-ENSAIO-2.4 Suporte a loop externo de refinamento

- **Descrição:** Contrato do nó permite reinvocação com previous_article preenchido. Writer regenera artigo inteiro incorporando o feedback presente no histórico de mensagens.
- **Critérios de Aceite:**
  - Quando previous_article for None, Writer gera artigo pela primeira vez
  - Quando previous_article vier preenchido, Writer regenera considerando feedback presente nas messages mais recentes
  - Writer não tenta editar o previous_article pontualmente; sempre regenera inteiro
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum (comportamento absorvido em 2.1)
  - **Contratos/Shapes:** quando `previous_article` é None, Writer gera pela primeira vez; quando preenchido, Writer regenera inteiro considerando feedback presente em `messages`
  - **Integração:** quem invoca (app do produto) é responsável por acumular `messages` e passar `previous_article`
  - **Template de referência:** padrão declarado em `core/docs/agents/writer/design.md` seção "Decisão Arquitetural: Começa Simples"
  - **Escopo de teste:** validação manual via script que invoca `writer_node` duas vezes (primeira com `previous_article=None`, segunda com o artigo anterior e nova mensagem no histórico)

---

#### ÉPICO C-ENSAIO-3: Writer Gera por Seção (Evolução)

**Objetivo:** Writer evolui para gerar artigo seção por seção em vez de bloco único, permitindo refinamento granular.

**Status:** 🌱 Visão

**Dependências:**
- C-ENSAIO-2 (Writer versão inicial)

---

#### ÉPICO C-ENSAIO-4: Ingestão de Arquivos Anexados (Core)

**Objetivo:** Mecanismo genérico para agentes do core consumirem conteúdo de arquivos anexados (notebook, markdown, CSV, imagens). Detalhes de parsing/extração a definir no refinamento.

**Status:** 🌱 Visão

---

#### ÉPICO C-ENSAIO-5: Promoção de Entidade Pendência para o Core (Condicional)

**Objetivo:** Pendência nasce no produto Ensaio; promover para o core quando segundo produto precisar (provavelmente Produtor Científico). Épico condicionado à existência de segundo caso de uso.

**Status:** 🌱 Visão (condicional)

**Consulte:** [core/docs/architecture/data-models/ontology.md](docs/architecture/data-models/ontology.md) (seção "Entidades em Incubação")

---

#### ÉPICO C-ENSAIO-6: Promoção de Componentes de UI para o Core (Condicional)

**Objetivo:** Componentes de UI conversacional (chat_input, chat_history e similares) hoje vivem em products/revelar/app/components/ e são reusados por outros produtos via import direto. Quando um terceiro produto consumir os mesmos componentes, ou quando surgir atrito concreto com o import cross-produto, promover os componentes compartilhados para core/ui_components/ (nome a definir no refinamento).

**Status:** 🌱 Visão (condicional)

**Dependências:**
- POC do Ensaio (E-POC-1) em produção como primeiro consumidor externo
- Segundo consumidor externo (Ensaio na POC é o primeiro)

**Gatilho de ativação:**
- Terceiro produto com UI conversacional entrando no super-sistema, OU
- Atrito concreto no import cross-produto atual (manutenção, testes, circularidade, etc.)

**Consulte:** [core/docs/vision/super_system.md](../core/docs/vision/super_system.md) (seção sobre componentes compartilhados entre produtos)

---

> **📖 Melhorias Técnicas:** Para melhorias técnicas não vinculadas a épicos, consulte [docs/backlog.md](../../docs/backlog.md).

---

## 📚 Documentação

- `core/docs/vision/system_philosophy.md` - Filosofia do sistema
- `core/docs/architecture/` - Estrutura técnica
- `core/docs/agents/` - Especificações dos agentes

---

## 📝 Observações

**Regra:** fluxo manual via Cursor exige épico em `📋 Critérios definidos`; fluxo autônomo via Claude Code Web exige `🔍 Detalhes definidos`.

> Para o processo completo de refinamento, consulte [planning_guidelines.md](process/refinement/planning_guidelines.md). Para a prontidão ao fluxo autônomo (alvo `🔍`), consulte [autonomous_readiness.md](process/refinement/autonomous_readiness.md). Para o fechamento do épico (saída), consulte [epic_completion.md](process/refinement/epic_completion.md).

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos em `🌱 Visão` ou `📐 Funcionalidades esboçadas` passam por sessão de refinamento antes da implementação
