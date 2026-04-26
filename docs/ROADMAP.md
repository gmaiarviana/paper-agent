# ROADMAP - Core Universal

Épicos e melhorias do sistema core que serve todos os produtos.

> **📖 Status Atual:** Para entender o estado atual do core, consulte [ARCHITECTURE.md](ARCHITECTURE.md) e [core/docs/](../core/docs/).

> **📖 Visão:** Para entender a filosofia do sistema, consulte [core/docs/vision/system_philosophy.md](../core/docs/vision/system_philosophy.md).

### 🧭 Estados dos Épicos

Cada épico percorre até sete estados. Os mesmos estados aplicam-se ao campo "Status" do milestone. Detalhes em [process/refinement/planning_guidelines.md](process/refinement/planning_guidelines.md).

- **`🌱 Visão`** — apenas objetivo definido. Aguarda refinamento.
- **`🧭 Jornada alinhada`** — objetivo refinado + rationale (o que é / o que não é) + glossário ancorado + acoplamentos sinalizados; jornada alvo e escopo declinados (para milestone). Funcionalidades ainda não esboçadas. Aguarda refinamento.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Pronto para fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist em [autonomous_readiness.md](process/refinement/autonomous_readiness.md) aplicado. Pronto para fluxo autônomo via Claude Code Web.
- **`🏗️ Em andamento`** — implementação em curso, até o ciclo de fechamento.
- **`✅ Implementado`** — ciclo de fechamento executado (ver [epic_completion.md](process/refinement/epic_completion.md)).

> **Retroatividade:** épicos concluídos antes da introdução do modelo de estados permanecem em formato simplificado (título ✅ + 1-2 linhas de resumo) e não são reclassificados retroativamente. O modelo aplica-se a épicos em andamento e futuros.

---

## 🎯 Épicos Core × Milestones de Produto

> **Nota:** O core não tem milestones próprios — seus épicos são consumidos pelos milestones dos produtos. Épicos motivados por produto (prefixo `C-<PRODUTO>-`) declaram aqui qual milestone de produto os consome, para que o dispatch do milestone saiba que precisa tê-los implementados como dependência. Convenção de id de milestone em [docs/CONSTITUTION.md §9](CONSTITUTION.md).

| Épico Core | Status | Milestone consumidor | Produto |
|------------|--------|----------------------|---------|
| ÉPICO 1 (Pesquisador) | 🌱 Visão | — (não vinculado) | — |
| C-ENSAIO-1 (Parametrização de Contexto) | 🌱 Visão | POC-ENSAIO | Ensaio |
| C-ENSAIO-2 (Writer versão inicial) | ✅ Implementado | POC-ENSAIO | Ensaio |
| C-ENSAIO-3 (Writer por seção) | 🔍 Detalhes definidos | PROTO-ENSAIO | Ensaio |
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

#### ÉPICO C-ENSAIO-2: Writer (Versão Inicial) ✅

**Status:** ✅ Implementado — PR #TBD

**Entregue:** Nó `writer_node` simples, stateless, em `core/agents/writer/` — recebe `{messages, focal_argument, previous_article, product_context}` e devolve `{article}` em markdown numa única passada. Prompt IMRaD em `core/prompts/writer.py` (`WRITER_PROMPT_V1`); config em `core/config/agents/writer.yaml`. Suporte a loop externo de refinamento (reinvocação com `previous_article`).

**Decisões permanentes:** ver [core/docs/agents/writer/design.md](../core/docs/agents/writer/design.md) (nasce no core, começa simples, estrutura vive no prompt, organização antecipa generalização para o Produtor Científico).

**Referências:** `tests/core/unit/test_writer.py`, `scripts/core/flows/validate_writer.py`, `docs/ARCHITECTURE.md` (padrões Core ↔ Produto).

---

#### ÉPICO C-ENSAIO-3: Writer Gera por Seção (Evolução)

**Objetivo:** Writer evolui para gerar artigo seção por seção em vez de bloco único, permitindo refinamento granular. Entrega dois artefatos: (1) o contrato `Article`/`Section` como estrutura serializável no core (princípio de viabilização §7 da visão do Ensaio), consumido pelo produto; (2) o nó `writer_section_node`, análogo stateless ao `writer_node` existente, que opera no escopo de uma única seção.

**Status:** 🔍 Detalhes definidos

**Dependências:**
- C-ENSAIO-2 (Writer versão inicial) — já entregue

### Funcionalidades:

#### C-ENSAIO-3.1: Contrato `Article` e `Section` no core

- **Descrição:** Define os tipos `Section` e `Article` em `core/agents/writer/models.py`. Estrutura serializável que vive no core e é consumida pelo produto Ensaio (e futuramente pelo Produtor Científico).
- **Critérios de Aceite:**
  - Deve definir `Section` como `TypedDict` com campos `title: str`, `body: str`, `status: Literal["empty", "draft", "edited"]`
  - Deve definir `Article = list[Section]`
  - Deve ser importável via `from core.agents.writer.models import Article, Section`
  - Deve serializar para JSON sem transformações adicionais (dict nativo do Python)
- **Detalhes de execução:**
  - **Arquivos a criar:** `core/agents/writer/models.py`
  - **Arquivos a modificar:** nenhum
  - **Contratos/Shapes:**
    ```python
    from typing import TypedDict, Literal
    class Section(TypedDict):
        title: str
        body: str
        status: Literal["empty", "draft", "edited"]

    Article = list[Section]
    ```
  - **Integração:** importado diretamente pelo produto via `from core.agents.writer.models import Article, Section`; não entra em nenhum grafo LangGraph
  - **Template de referência:** sem análogo no repositório (primeiro TypedDict de domínio no core)
  - **Acoplamentos verificados:** arquivo novo sem dependências internas além do `typing` da stdlib; nenhum produto afetado
  - **Dependências de ordem:** primeiro a executar — C-ENSAIO-3.2 depende deste contrato
  - **Escopo de teste:**
    - **Unit:** `tests/core/unit/agents/writer/test_article_models.py` — instanciar `Section` com campos válidos; verificar que `json.dumps` não lança exceção; verificar `Article` como lista de Sections

#### C-ENSAIO-3.2: `writer_section_node` no core

- **Descrição:** Novo nó stateless em `core/agents/writer/nodes.py` que gera ou regenera o corpo de uma seção individual dado o histórico conversacional, o argumento focal, o título da seção-alvo e o contexto do artigo já redigido (outras seções). Não modifica `writer_node`.
- **Critérios de Aceite:**
  - Deve aceitar `{messages, focal_argument, section_title, current_body, article_context, product_context}` e retornar `{section_content: str}`
  - `section_title` é o nome da seção a redigir (ex.: `"Metodologia"`)
  - `current_body` é `""` para geração inicial ou conteúdo existente para regeneração (modo refinamento)
  - `article_context` é um resumo em texto das outras seções já redigidas (pode ser `""` se nenhuma)
  - Em modo refinamento (`current_body` não-vazio), deve incorporar feedback da conversa recente sem devolver o cabeçalho da seção
  - Deve retornar apenas o corpo markdown da seção, sem o `## Título` repetido
  - `writer_node` existente deve passar seus testes sem modificação (não-regressão obrigatória)
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum (função adicionada ao fim de `core/agents/writer/nodes.py`)
  - **Arquivos a modificar:** `core/agents/writer/nodes.py` — adicionar `writer_section_node` ao final
  - **Contratos/Shapes:**
    ```python
    def writer_section_node(state: dict) -> dict:
        """
        Input (dict):
            messages:        list[BaseMessage] | list[dict]
            focal_argument:  dict | None
            section_title:   str
            current_body:    str   # "" = geração; não-vazio = refinamento
            article_context: str   # resumo das demais seções; "" se nenhuma
            product_context: str | None

        Output (dict):
            section_content: str   # corpo markdown da seção, sem cabeçalho
        """
    ```
  - **Integração:** invocado diretamente pelo produto (`writer_section_node({...})`), mesmo padrão do `writer_node`; não entra no grafo LangGraph
  - **Template de referência:** `writer_node` em `core/agents/writer/nodes.py` — mesma estrutura (stateless, prompt + invoke, retorno dict)
  - **Acoplamentos verificados:**
    - `core/agents/memory/config_loader.py` — reusar `get_agent_prompt`, `get_agent_model` (padrão existente no `writer_node`)
    - `core/utils/config.py` — reusar `create_anthropic_client`, `get_anthropic_model`
    - **Produto afetado:** Ensaio (consumidor direto — adição não quebra `writer_node`). Revelar não usa Writer.
  - **Dependências de ordem:** depende de C-ENSAIO-3.1 (tipos `Section`/`Article` para documentação de contrato); pode ser implementado em paralelo na prática
  - **Escopo de teste:**
    - **Unit:** `tests/core/unit/agents/writer/test_writer_section_node.py` — mock do LLM; verificar que `section_content` é string não-vazia; verificar que `current_body` não-vazio ativa instrução de refinamento no prompt; verificar não-regressão do `writer_node` (rodar testes existentes em `tests/core/unit/test_writer.py`)
    - **Validação manual via script:** `scripts/core/flows/validate_writer_section.py` — invocar `writer_section_node` com state mínimo (`section_title="Metodologia"`, 1 mensagem), verificar saída markdown coerente

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
