# ROADMAP - Core Universal

Épicos e melhorias do sistema core que serve todos os produtos.

> **📖 Status Atual:** Para entender o estado atual do core, consulte [ARCHITECTURE.md](ARCHITECTURE.md) e [core/docs/](../core/docs/).

> **📖 Visão:** Para entender a filosofia do sistema, consulte [core/docs/vision/system_philosophy.md](../core/docs/vision/system_philosophy.md).

---

## 📋 Épicos Planejados

### ⏳ Épicos Planejados

#### ÉPICO 1: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado

**Dependências:**
- Revelar ÉPICO 2 (Catálogo de Conceitos)

**Nota:** Pesquisador pode usar catálogo de conceitos para buscar papers relacionados.

**Próximos Passos:**
- Discutir comportamento e interface antes do refinamento
- Definir integração com Observer e catálogo de conceitos

---

### ⏳ Épicos Motivados pelo Ensaio

> **Nota:** Estes épicos são **motivados pelo produto Ensaio** (primeiro produto com necessidades além das do Revelar) mas **pertencem ao core** — serão reusados por outros produtos, especialmente Produtor Científico. O prefixo `C-ENSAIO-` identifica a motivação; o código fica no core e respeita o desacoplamento descrito em [core/docs/vision/super_system.md](../core/docs/vision/super_system.md).

#### ÉPICO C-ENSAIO-1: Parametrização de Contexto de Produto nos Agentes

**Objetivo:** Agentes do core (Orquestrador e futuros) aceitam foco/domínio passado por produtos externos sem que o core conheça os produtos. Mecanismo de configuração a definir no refinamento.

**Status:** ⏳ Planejado

**Consulte:** [core/docs/vision/super_system.md](../core/docs/vision/super_system.md) (seção "Injeção de Contexto de Produto")

---

#### ÉPICO C-ENSAIO-2: Writer (Versão Inicial)

**Objetivo:** Novo agente no core que recebe contexto conversacional e cognitive_model, devolve markdown estruturado. Nasce simples. Organizado para generalização futura (Produtor Científico reusará).

**Status:** 📋 Critérios definidos

**Decisões arquiteturais já tomadas:** ver [core/docs/agents/writer/design.md](../core/docs/agents/writer/design.md)
- Nasce no core (não no Ensaio)
- Começa simples: nó que recebe contexto e devolve markdown
- Estruturas de artigo vivem no prompt do Writer (não em enum/schema)
- Organização inicial antecipa generalização para o Produtor Científico

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

#### C-ENSAIO-2.2 Prompt com IMRaD e defaults

- **Descrição:** Prompt do Writer contém base de conhecimento sobre estrutura IMRaD. Writer infere intenção e narrativa da conversa, com defaults razoáveis quando não há pistas claras.
- **Critérios de Aceite:**
  - Prompt em core/prompts/writer.py como WRITER_PROMPT_V1
  - Prompt descreve estrutura IMRaD (abstract, introdução, métodos, resultados, discussão, conclusão, referências)
  - Prompt orienta Writer a inferir intenção da conversa
  - Prompt define default "informar" quando intenção não emergir
  - Prompt não contém nome de produto específico (Ensaio, etc)

#### C-ENSAIO-2.3 Configuração YAML

- **Descrição:** Configuração externa do Writer via YAML, seguindo padrão dos outros agentes do core.
- **Critérios de Aceite:**
  - Arquivo core/config/agents/writer.yaml com campos: prompt (referência), model, context_limits, metadata
  - Modelo padrão: claude-3-5-haiku-20241022
  - Deve ser carregável pelo config_loader existente
  - Deve validar com config_validator existente

#### C-ENSAIO-2.4 Suporte a loop externo de refinamento

- **Descrição:** Contrato do nó permite reinvocação com previous_article preenchido. Writer regenera artigo inteiro incorporando o feedback presente no histórico de mensagens.
- **Critérios de Aceite:**
  - Quando previous_article for None, Writer gera artigo pela primeira vez
  - Quando previous_article vier preenchido, Writer regenera considerando feedback presente nas messages mais recentes
  - Writer não tenta editar o previous_article pontualmente; sempre regenera inteiro

---

#### ÉPICO C-ENSAIO-3: Writer Gera por Seção (Evolução)

**Objetivo:** Writer evolui para gerar artigo seção por seção em vez de bloco único, permitindo refinamento granular.

**Status:** ⏳ Planejado

**Dependências:**
- C-ENSAIO-2 (Writer versão inicial)

---

#### ÉPICO C-ENSAIO-4: Ingestão de Arquivos Anexados (Core)

**Objetivo:** Mecanismo genérico para agentes do core consumirem conteúdo de arquivos anexados (notebook, markdown, CSV, imagens). Detalhes de parsing/extração a definir no refinamento.

**Status:** ⏳ Planejado

---

#### ÉPICO C-ENSAIO-5: Promoção de Entidade Pendência para o Core (Condicional)

**Objetivo:** Pendência nasce no produto Ensaio; promover para o core quando segundo produto precisar (provavelmente Produtor Científico). Épico condicionado à existência de segundo caso de uso.

**Status:** ⏳ Planejado (condicional)

**Consulte:** [core/docs/architecture/data-models/ontology.md](docs/architecture/data-models/ontology.md) (seção "Entidades em Incubação")

---

#### ÉPICO C-ENSAIO-6: Promoção de Componentes de UI para o Core (Condicional)

**Objetivo:** Componentes de UI conversacional (chat_input, chat_history e similares) hoje vivem em products/revelar/app/components/ e são reusados por outros produtos via import direto. Quando um terceiro produto consumir os mesmos componentes, ou quando surgir atrito concreto com o import cross-produto, promover os componentes compartilhados para core/ui_components/ (nome a definir no refinamento).

**Status:** ⏳ Planejado (condicional)

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

**Regra:** fluxo manual via Cursor exige épico em `📋 Critérios definidos`; fluxo autônomo via Claude Code Web exige `✅ Detalhes definidos`.

> Para o processo completo de refinamento, consulte [planning_guidelines.md](process/refinement/planning_guidelines.md). Para a 2ª passada (prontidão para autônomo), consulte [autonomous_readiness.md](process/refinement/autonomous_readiness.md).

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos em `⏳ Planejado` passam pela 1ª passada de refinamento antes da implementação
