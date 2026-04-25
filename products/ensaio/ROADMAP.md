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

- **Status:** `📐 Funcionalidades esboçadas` (E-PROTO-1 em `🔍 Detalhes definidos`)
- **Objetivo:** elevar a **qualidade da experiência dentro de uma sessão** usando coerentemente capacidades que já temos (Metodologista parado no core, Writer evoluindo para por-seção) num chassi de stack adequado. Protótipo continua em sessão única e descartável (igual à POC) — persistência, pendências e fluxo assíncrono migram para o MVP por coerência de escopo (ver [vision.md §§3, 6, 10, 11](docs/vision.md)). Único artigo em andamento por vez; múltiplos artigos ficam em Ideias Futuras.
- **Estágio:** Protótipo — Usuário usa de verdade
- **Produto:** Ensaio
- **Épicos agrupados:** E-PROTO-1 (`🔍 Detalhes definidos`), E-PROTO-2, E-PROTO-3 (estes dois em `📐 Funcionalidades esboçadas`)
- **Dependências de core:** [C-ENSAIO-3](../../docs/ROADMAP.md) (Writer por seção) — pré-requisito de E-PROTO-2. **C-ENSAIO-3 precisa estar em `🔍 Detalhes definidos` antes de E-PROTO-2 ir para fluxo autônomo**, porque o contrato `Article` seccionado (estrutura serializável no core, princípio de viabilização §7) emerge do refinamento de C-ENSAIO-3 e é consumido por E-PROTO-2.
- **Decisão de stack (saída do refinamento de E-PROTO-1.1):** Reflex (Python full-stack). ADR registrada em [products/ensaio/docs/adr/001-stack-do-prototipo.md](docs/adr/001-stack-do-prototipo.md).
- **Branch associada:** `milestone/proto-ensaio`
- **Glossário do produto:** termos "Usuário" (jornada) e "Pesquisador" (persona) ancorados em [products/ensaio/docs/vision.md §13](docs/vision.md).
- **Jornada alvo (alta-nível):** Usuário abre o app → começa nova sessão sobre o experimento → conversa flui no chat com transparência sobre qual agente está falando (`🎯 Orquestrador`, `🔬 Metodologista`) e feedback de processamento decente → Metodologista provoca quando a conversa toca em metodologia (lacunas, métricas, evidências) → clica "Gerar artigo" / "Gerar seção X" / "Regenerar seção X" → painel seccionado mostra o artigo em construção com status por seção e edição inline do markdown → ao final, exporta/copia o artigo. Sessão é descartável (recarregar zera tudo); persistência fica para o MVP.
- **Feedback do POC endereçado por este milestone:**
  - Promessas vazias do Orquestrador/Estruturador ("vou validar...") → ajuste de prompt como **trabalho preparatório de entrada** do milestone (higiene pós-POC, commit antes do dispatch; não é épico).
  - Falta de transparência sobre qual agente está falando → detalhe dentro de **E-PROTO-1**: nova stack entrega bubble com label do agente.
  - Feedback de processamento (blur opaco do Streamlit) → resolvido por **E-PROTO-1** — stack nova substitui o mecanismo.
  - Relação chat ↔ evento de geração / histórico confuso → **E-PROTO-2** (painel seccionado com edição inline e geração por seção).
  - Carregamento inicial lento → **E-PROTO-1** — cold start aceitável vira critério da ADR da stack.
  - Artigo gerado raso ou pouco aderente ao contexto técnico → **E-PROTO-3** (Metodologista provocando lacunas, métricas e evidências antes da geração).
- **Escopo declinado:**
  - **Persistência do artigo entre sessões** e **Pendências entre sessões** foram movidas para o MVP-ENSAIO. Pendência sem persistência não atravessa nada (dependência conceitual dura), e juntar persistência + UI nova + stack nova + Metodologista neste milestone configuraria o anti-padrão milestone-balaio (ver [planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md)).
  - **Histórico/versões do artigo** sai do escopo do Protótipo. Re-geração sobrescreve o artigo focal; comparação entre estados anteriores fica para iteração futura quando houver demanda.
  - **Higiene de UX no Streamlit** continua declinada — stack nova substitui o mecanismo.
  - **Múltiplos artigos em paralelo** vai para Ideias Futuras.
- **Princípio de viabilização (do escopo declinado):** mesmo sem persistência, estado do artigo + conversa vivem em estruturas serializáveis no core (visão §7), para que o MVP troque a camada de armazenamento sem refazer o domínio.
- **Sizing:** avaliação real (e eventual quebra em sub-milestones `ALPHA`/`BETA`) fica para quando a EM skill avaliar, antes do dispatch.

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

#### ÉPICO E-PROTO-1: Migração de Stack da Interface (Reflex)

**Objetivo:** Substituir o Streamlit da POC por **Reflex** (Python full-stack, decisão registrada em ADR — funcionalidade 1.1) — exibição decente, transparência sobre qual agente está falando, feedback de processamento que não bloqueia a tela e cold start aceitável. Garante o princípio de viabilização (§7 vision): estado do artigo + conversa em estruturas serializáveis no backend, UI burra renderizando view.

**Status:** 🔍 Detalhes definidos

**Dependências:** nenhuma (épico de saída do milestone — destrava E-PROTO-2 e E-PROTO-3).

### Funcionalidades:

#### 1.1 ADR de Stack

- **Descrição:** Registra a decisão por **Reflex** com opções avaliadas, trade-offs e critérios atendidos. Saída textual; sem código.
- **Critérios de Aceite:**
  - Deve criar ADR em `products/ensaio/docs/adr/001-stack-do-prototipo.md` no formato canônico (Contexto, Opções avaliadas, Decisão, Consequências, Referências).
  - Deve listar pelo menos 4 opções avaliadas com trade-offs por critério: cold start, ergonomia (chat + painel lateral), princípio de viabilização §7 (UI burra, estado serializável), custo de manutenção. Opções: Streamlit melhorado, Chainlit, Reflex, Next.js + FastAPI.
  - Deve explicitar Reflex como decisão e justificar pelos critérios.
  - Deve referenciar `products/ensaio/docs/vision.md §7` e `docs/process/refinement/planning_guidelines.md` (definição de Protótipo).
- **Detalhes de execução:**
  - **Arquivos a criar:** `products/ensaio/docs/adr/001-stack-do-prototipo.md`
  - **Arquivos a modificar:** nenhum (ROADMAP já referencia o ADR no bloco PROTO-ENSAIO).
  - **Contratos/Shapes:** N/A (doc).
  - **Integração:** doc consultivo, sem integração executável.
  - **Template de referência:** formato ADR padrão (Contexto / Opções / Decisão / Consequências) — não há ADR prévio no repo; primeiro do produto.
  - **Acoplamentos verificados:** N/A.
  - **Dependências de ordem:** primeiro a executar (define alvo das demais funcionalidades).
  - **Escopo de teste:** revisão humana (doc).

#### 1.2 Esqueleto da Nova Stack (Reflex)

- **Descrição:** Substitui `products/ensaio/app/chat.py` (Streamlit) por entrypoint Reflex com layout chat + painel de artigo, mantendo o ciclo de sessão única descartável da POC e preservando o `product_config.py` (loader do `product.yaml`) e o `graph.py` (composição do grafo do Ensaio).
- **Critérios de Aceite:**
  - Deve haver entrypoint Reflex executável via `reflex run` a partir de `products/ensaio/`.
  - Deve renderizar layout de duas colunas: chat à esquerda (proporção ~3), painel do artigo à direita (proporção ~2), equivalente ao 60/40 do POC.
  - Deve carregar `products/ensaio/config/product.yaml` no boot da app via `load_product_context()` (preservado) e injetar `product_context` em toda invocação do grafo.
  - Deve manter sessão única descartável: recarregar a página zera todo o estado (mensagens, focal_argument, current_article).
  - Deve invocar `create_ensaio_graph()` (preservado) sem alterar contrato do core.
  - Deve invocar `writer_node` diretamente fora do grafo (preservado, padrão de `core/docs/agents/writer/design.md`).
  - Deve remover o app Streamlit completamente: `products/ensaio/app/chat.py`, `products/ensaio/app/components/article_panel.py`, `products/ensaio/app/components/chat_input.py`, `products/ensaio/app/components/generate_button.py`.
  - Não deve importar nada de `products/revelar/` (rompe acoplamento atual com `chat_history.py` do Revelar — ver `chat.py:37`).
  - Deve atualizar `products/ensaio/README.md` com instruções de execução (`reflex run`).
  - Deve adicionar `reflex>=0.6` (versão a fixar no momento da implementação) em `requirements.txt`.
- **Detalhes de execução:**
  - **Arquivos a criar:**
    - `products/ensaio/app/main.py` — entrypoint Reflex (define `rx.App` + página principal).
    - `products/ensaio/app/state.py` — `EnsaioState(rx.State)` com campos serializáveis.
    - `products/ensaio/app/components/chat_panel.py` — coluna esquerda (lista de mensagens + input).
    - `products/ensaio/app/components/article_panel.py` — coluna direita (markdown render + botão Gerar/Regenerar).
    - `products/ensaio/rxconfig.py` — config do Reflex (app_name="ensaio").
  - **Arquivos a modificar:**
    - `requirements.txt` — adicionar `reflex>=0.6`.
    - `products/ensaio/README.md` — substituir instruções `streamlit run` por `reflex run`.
  - **Arquivos a remover:**
    - `products/ensaio/app/chat.py`
    - `products/ensaio/app/components/article_panel.py`
    - `products/ensaio/app/components/chat_input.py`
    - `products/ensaio/app/components/generate_button.py`
  - **Arquivos preservados (sem mudança):**
    - `products/ensaio/app/graph.py`
    - `products/ensaio/app/product_config.py`
    - `products/ensaio/config/product.yaml`
  - **Contratos/Shapes — `EnsaioState`:**
    ```python
    class EnsaioState(rx.State):
        messages: list[dict]              # [{role, agent, content, timestamp}]
        langchain_history: list           # serializável (lista de dicts {type, content})
        focal_argument: dict | None       # output do Estruturador
        current_article: str | None       # markdown do Writer
        processing_agent: str | None      # nome do agente em execução (orchestrator/structurer/writer); None quando ocioso
        is_generating_article: bool       # toggle do botão Gerar/Regenerar
        thread_id: str                    # uuid da sessão (gerado no on_load)
        error_message: str | None         # erro do último turno (mostrado como bubble do assistente)
    ```
  - **Integração:**
    - Entrypoint: `reflex run` lê `rxconfig.py`; Reflex compila frontend e sobe backend FastAPI embutido.
    - Boot: `EnsaioState.on_load` carrega `product_context` via `load_product_context()` e gera `thread_id`.
    - Turno do chat: event handler `EnsaioState.send_message` invoca `create_ensaio_graph().invoke(state, config={"configurable": {"thread_id": ..., "product_context": ...}})` em background task; atualiza `messages` + `langchain_history` + `focal_argument` ao retornar.
    - Geração de artigo: event handler `EnsaioState.generate_article` invoca `writer_node({...})` direto, com `messages=langchain_history`, `focal_argument`, `previous_article=current_article`, `product_context=...`.
  - **Template de referência:** Reflex docs oficiais (chat app exemplo); não há análogo interno em Reflex.
  - **Acoplamentos verificados:**
    - `products/ensaio/app/graph.py` — usado via `create_ensaio_graph()`; sem mudança (POC validou contrato).
    - `products/ensaio/app/product_config.py` — usado via `load_product_context()`; sem mudança.
    - `core.agents.writer.nodes.writer_node` — invocação direta preservada.
    - `core.agents.orchestrator.state.MultiAgentState` — consumido como dict no `state` do grafo.
    - **Acoplamento removido:** `products/revelar/app/components/chat_history.py` (atualmente importado em `chat.py:37`) — Reflex tem componente próprio.
  - **Dependências de ordem:** depende de 1.1 (ADR confirma stack); 1.3 e 1.4 estendem este esqueleto.
  - **Escopo de teste:**
    - **Unit:** `tests/products/ensaio/unit/test_ensaio_state.py` — testa serialização do `EnsaioState`, acúmulo de `messages`, reset em on_load.
    - **Validação manual via script:** `scripts/ensaio/flows/validate_reflex_skeleton.py` — sobe app, abre browser headless (ou guia manual), envia mensagem, verifica que histórico aparece e que `focal_argument` atualiza no state.
    - **Smoke:** `tests/products/ensaio/integration/smoke/test_app_boots.py` — importa `main.py` e instancia `rx.App` sem erro (não roda servidor).

#### 1.3 Transparência de Agente no Chat

- **Descrição:** Cada bubble do chat exibe label de quem fala. Requer anexar metadata de agente nas `AIMessage` produzidas pelos nós do core.
- **Critérios de Aceite:**
  - Deve renderizar label visível em cada bubble: `🎯 Orquestrador`, `📐 Estruturador`, `🔬 Metodologista`, `✍️ Writer`, `👤 Você`.
  - Deve identificar o agente a partir de `AIMessage.additional_kwargs["agent"]` (string: `"orchestrator"`, `"structurer"`, `"methodologist"`, `"writer"`).
  - Deve exibir estilo distinto (cor de borda ou ícone) entre bubbles do usuário e dos agentes.
  - Deve mapear agente desconhecido (`additional_kwargs` ausente) para label genérico `🤖 Sistema` em vez de quebrar.
  - **Não deve** quebrar o Revelar: mensagens consumidas pelo Revelar continuam funcionais com `additional_kwargs` ignorados (campo extra é transparente no consumo atual via `chat_history.py`).
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum.
  - **Arquivos a modificar:**
    - `core/agents/orchestrator/nodes.py` — em `nodes.py:1033`, trocar `AIMessage(content=message)` por `AIMessage(content=message, additional_kwargs={"agent": "orchestrator"})`.
    - `core/agents/structurer/nodes.py` — `nodes.py:351` e `nodes.py:534`: anexar `additional_kwargs={"agent": "structurer"}` nos dois pontos.
    - `core/agents/methodologist/nodes.py` — anexar `additional_kwargs={"agent": "methodologist"}` nas `AIMessage` retornadas (inspecionar pontos exatos durante implementação).
    - `core/agents/writer/nodes.py` — Writer não retorna `messages` (retorna `{"article": ...}`), mas a representação no chat é gerada pelo produto. Documentar no painel do artigo o label `✍️ Writer` quando o artigo aparece/atualiza (sem alterar `nodes.py`).
    - `products/ensaio/app/components/chat_panel.py` — render lê `msg["agent"]` e mapeia para label.
    - `products/ensaio/app/state.py` — `send_message` lê `last_msg.additional_kwargs.get("agent")` e armazena em `messages[-1]["agent"]`.
  - **Contratos/Shapes:**
    - `AIMessage.additional_kwargs`: `{"agent": "orchestrator" | "structurer" | "methodologist"}`.
    - `EnsaioState.messages[i]`: `{role: "user"|"assistant", agent: str|None, content: str, timestamp: str}`.
    - Mapa label: `{"orchestrator": "🎯 Orquestrador", "structurer": "📐 Estruturador", "methodologist": "🔬 Metodologista", "writer": "✍️ Writer", None: "🤖 Sistema"}` em `products/ensaio/app/components/chat_panel.py`.
  - **Integração:** o produto consome `AIMessage.additional_kwargs["agent"]` ao processar `result["messages"]` do grafo; sem mudança no contrato do `MultiAgentState`.
  - **Template de referência:** padrão LangChain `AIMessage(content=..., additional_kwargs={...})` — uso oficial de metadados extras.
  - **Acoplamentos verificados — código compartilhado entre produtos:**
    - **Consumidor afetado: Revelar** (usa `core.agents.{orchestrator,structurer,methodologist}.nodes` via `core.agents.multi_agent_graph`).
    - **Como verificar regressão:** rodar suite atual de testes do core (`tests/core/`) sem modificações; `additional_kwargs` é campo opcional em LangChain — leitores que não consomem ignoram. Validação manual: subir Revelar, conduzir conversa de 3-5 turnos, confirmar que renderização e `chat_history.py` continuam idênticos.
    - **Refatoração prévia necessária:** nenhuma — `additional_kwargs` já é campo nativo de `AIMessage`.
  - **Dependências de ordem:** depende de 1.2 (esqueleto Reflex com `chat_panel`).
  - **Escopo de teste:**
    - **Unit:** `tests/core/unit/agents/orchestrator/test_orchestrator_emits_agent_metadata.py`, idem para structurer e methodologist — instanciar nó, invocar com state mínimo, asseverar `result["messages"][-1].additional_kwargs["agent"]` correto.
    - **Unit:** `tests/products/ensaio/unit/test_chat_panel_label.py` — mapeamento `agent → label` (incluindo fallback `None → 🤖 Sistema`).
    - **Integration (não-regressão Revelar):** rodar `tests/products/revelar/` existente sem modificações; deve passar 100%.
    - **Validação manual:** abrir Ensaio, enviar 3-5 mensagens, verificar labels corretos; abrir Revelar, fluxo equivalente, verificar ausência de regressão visual.

#### 1.4 Feedback de Processamento Decente

- **Descrição:** Indicador visual durante chamada de agente que não bloqueia o histórico nem cobre a tela com overlay opaco. Substitui o blur do Streamlit.
- **Critérios de Aceite:**
  - Deve exibir indicador "{ícone do agente} {nome} processando..." enquanto `EnsaioState.processing_agent` é não-nulo.
  - Deve identificar o agente em processamento (heurística inicial: rótulo do nó atual disparado, baseada na rota do grafo — Orquestrador é sempre o primeiro; Estruturador quando o Orquestrador roteia para ele; Writer quando botão Gerar é acionado).
  - Deve permitir scroll do histórico durante processamento (sem overlay modal).
  - Deve desabilitar input e botões de geração enquanto `processing_agent` não é nulo (evita disparo duplo), mas sem ocultar o histórico.
  - Não deve usar `rx.spinner` em overlay full-screen.
  - Deve limpar `processing_agent` ao final de cada turno (sucesso ou erro).
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum (componente vive em `chat_panel.py`).
  - **Arquivos a modificar:**
    - `products/ensaio/app/state.py` — campos `processing_agent: str | None`, `is_generating_article: bool`; event handlers `send_message` e `generate_article` setam/limpam o campo.
    - `products/ensaio/app/components/chat_panel.py` — exibe indicador inline abaixo da última mensagem quando `processing_agent` não é nulo.
    - `products/ensaio/app/components/article_panel.py` — exibe "✍️ Writer redigindo..." inline no painel quando `is_generating_article` é true.
  - **Contratos/Shapes:**
    - `processing_agent: Literal["orchestrator", "structurer", "methodologist", "writer"] | None`.
    - Mapa de labels reaproveitado de 1.3.
  - **Integração:**
    - `send_message`: setar `processing_agent="orchestrator"` antes do `graph.invoke`; após retorno, decidir entre limpar (rota terminou em `END` direto) ou setar `"structurer"` (não aplicável aqui — graph.invoke é síncrono no fim do turno; campo limpo no `finally`).
    - Para granularidade real (mostrar transição Orquestrador → Estruturador no mesmo turno), adicionar callback no grafo (`graph.invoke(..., config={"callbacks": [...]})`) — **simplificação aceita:** Protótipo mostra apenas o nome do "agente que iniciou o turno"; transição intra-turno fica para iteração futura. Registrar a simplificação no commit.
    - `generate_article`: setar `is_generating_article=True` + `processing_agent="writer"` antes; limpar no `finally`.
  - **Template de referência:** padrão `rx.cond` + `rx.background_task` em event handlers Reflex.
  - **Acoplamentos verificados:** somente `EnsaioState`; nenhum acoplamento com core.
  - **Dependências de ordem:** depende de 1.2 (esqueleto) e 1.3 (mapa de labels reusado).
  - **Escopo de teste:**
    - **Unit:** `tests/products/ensaio/unit/test_state_processing_lifecycle.py` — verifica que `processing_agent` é setado antes da chamada e limpo no finally (mock do `graph.invoke`).
    - **Validação manual:** subir app, enviar mensagem, confirmar indicador inline, scroll do histórico funcional, input desabilitado durante processamento, indicador some ao terminar.

---

#### ÉPICO E-PROTO-2: Rascunho Progressivo por Seção (Modo Híbrido)

**Objetivo:** Materializar o modo de escrita híbrido (visão §4) dentro de uma sessão — painel exibe o artigo seccionado, Usuário gera/regenera seções individualmente e edita o markdown inline. Rascunho evolui acompanhando a conversa, em vez de ser gerado de uma vez no final como na POC.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:**
- E-PROTO-1 (nova stack — sem ela não há painel decente)
- [C-ENSAIO-3](../../docs/ROADMAP.md) (Writer por seção no core) — **deve estar em `🔍 Detalhes definidos` antes de E-PROTO-2 ir para fluxo autônomo**, porque o contrato `Article` seccionado (estrutura serializável no core, princípio de viabilização §7 da vision) emerge do refinamento de C-ENSAIO-3 e é consumido pelo painel + state do Ensaio.

### Funcionalidades (esboço):
- 2.1 Painel Seccionado — substitui o markdown plano do POC; cada seção do artigo é renderizada como bloco individual, com título visível.
- 2.2 Geração e Regeneração por Seção — botões "Gerar seção X" / "Regenerar seção X" invocam Writer no escopo da seção, consumindo histórico conversacional + artigo focal + contexto de produto.
- 2.3 Edição Inline de Seção — Usuário edita o markdown de uma seção diretamente no painel, sem regenerar; alterações entram no estado e são preservadas em regenerações futuras de outras seções.
- 2.4 Status por Seção — sinalização visual leve do estado (vazia / rascunho gerado / editada pelo Usuário) para guiar onde focar.

---

#### ÉPICO E-PROTO-3: Metodologista Aplicado ao Ensaio

**Objetivo:** Trazer o Metodologista (agente do core existente, parado desde a POC) para o grafo do Ensaio, parametrizado via `product_context`, para provocar ativamente sobre lacunas de rigor — métricas ausentes, evidências faltantes, afirmações sem suporte. Endereça a expectativa de que ao final do Protótipo o sistema empurre o artigo para evoluir com qualidade, não só ajude a transcrever o que foi dito.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:**
- E-POC-2 (parametrização de contexto — já entregue)
- E-PROTO-1 (nova stack — para que a provocação tenha distinção visual no chat)

### Funcionalidades (esboço):
- 3.1 Inclusão do Metodologista no Grafo do Ensaio — atualizar `products/ensaio/app/graph.py` para compor Orquestrador + Estruturador + Metodologista; nó recebe `product_context` por configurable.
- 3.2 Postura de Provocação Seletiva — Metodologista não fala a cada turno; intervém quando a conversa toca em metodologia, resultados ou afirmações sem suporte (critério em prompt + integração no grafo). Evita ruído conversacional.
- 3.3 Provocação Ativa sobre Lacunas — produz perguntas/sugestões observáveis sobre métricas ausentes, evidências faltantes e afirmações sem suporte, ancoradas no que o Usuário disse na conversa e no contexto do produto.
- 3.4 Reforço da Coerência do Artigo com o Contexto — provocações do Metodologista entram como sinal para o Writer (via histórico + artigo focal), elevando a aderência do artigo gerado ao experimento descrito. Inclui ajuste fino dos prompts do Orquestrador/Estruturador/Writer no contexto Ensaio (qualidade conversacional dos agentes existentes).
- 3.5 Provocação sobre Dimensões do Artigo — Metodologista pergunta/recomenda quando alguma das 4 dimensões em que o Writer opera (contexto, intenção, formato, estrutura — ver [core/docs/agents/overview.md](../../core/docs/agents/overview.md)) não está declarada ou clara na conversa. Endereça `vision.md §4` ("provocação sobre dimensões do artigo" como central no Protótipo). Mesma postura seletiva de 3.2/3.3, escopo distinto (dimensões do Writer ↔ lacunas de rigor).

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
