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

- **Status:** `✅ Implementado` — validação manual executada (2026-04), app sobe e funciona, seções geradas, labels de agente visíveis
- **Objetivo:** elevar a **qualidade da experiência dentro de uma sessão** usando coerentemente capacidades que já temos (Metodologista parado no core, Writer evoluindo para por-seção) num chassi de stack adequado. Protótipo continua em sessão única e descartável (igual à POC) — persistência, pendências e fluxo assíncrono migram para o MVP por coerência de escopo (ver [vision.md §§3, 6, 10, 11](docs/vision.md)). Único artigo em andamento por vez; múltiplos artigos ficam em Ideias Futuras.
- **Estágio:** Protótipo — Usuário usa de verdade
- **Produto:** Ensaio
- **Épicos agrupados:** E-PROTO-1, E-PROTO-2, E-PROTO-3 (todos em `🔍 Detalhes definidos`)
- **Dependências de core:** [C-ENSAIO-3](../../docs/ROADMAP.md) (Writer por seção) — pré-requisito de E-PROTO-2; já em `🔍 Detalhes definidos`.
- **Decisão de stack (saída do refinamento de E-PROTO-1.1):** Reflex (Python full-stack). ADR registrada em [products/ensaio/docs/adr/001-stack-do-prototipo.md](docs/adr/001-stack-do-prototipo.md).
- **Branch associada:** `claude/implement-essay-prototype-uFkkP`
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

### PROTO-ENSAIO-2 (stub)

- **Objetivo:** Tornar o raciocínio dos agentes visível e dar ao Usuário voz antes que decisões virem estado. Endereça: Metodologista invisível; Estruturador que decidiu sozinho sem expor racional; mensagens que não deixam claro o que mudou; impossibilidade de colapsar seções.
- **Estágio:** Protótipo
- **Produto:** Ensaio
- **Status:** `🌱 Visão`
- **Feedback capturado (validação PROTO-ENSAIO):**
  - Metodologista existe mas não aparece no chat
  - Estruturador propôs seções sem expor racional nem pedir confirmação
  - "Vou estruturar essa nova questão de pesquisa" — usuário não entendeu o que mudou
  - Mensagem do Estruturador longa sem sinalizar o que o sistema fez
  - Seções do artigo não podem ser colapsadas/expandidas
- **Épicos planejados (a detalhar no refinamento):** E-PROTO2-1 Co-decisão da Estrutura, E-PROTO2-2 Visibilidade do Metodologista, E-PROTO2-3 Mensagens com "o que mudou", E-PROTO2-4 Colapsar/expandir seções
- **Dependências:** PROTO-ENSAIO ✅
- **Branch associada:** `milestone/proto-ensaio-2` (a criar)

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

#### ÉPICO E-PROTO-1: Migração de Stack da Interface (Reflex)

**Objetivo:** Substituir o Streamlit da POC por **Reflex** (Python full-stack, decisão registrada em ADR — funcionalidade 1.1) — exibição decente, transparência sobre qual agente está falando, feedback de processamento que não bloqueia a tela e cold start aceitável. Garante o princípio de viabilização (§7 vision): estado do artigo + conversa em estruturas serializáveis no backend, UI burra renderizando view.

**Status:** ✅ Implementado — branch `claude/implement-essay-prototype-uFkkP`

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

**Objetivo:** Materializar o modo de escrita híbrido (visão §4) dentro de uma sessão — o Estruturador propõe a estrutura do artigo no chat, o painel exibe as seções propostas, e o Usuário gera/regenera o conteúdo de cada seção individualmente e edita inline. Rascunho evolui acompanhando a conversa, em vez de ser gerado de uma vez no final.

**Status:** ✅ Implementado — branch `claude/implement-essay-prototype-uFkkP`

**Dependências:**
- E-PROTO-1 (nova stack Reflex — `EnsaioState` e `article_panel.py` existem)
- [C-ENSAIO-3](../../docs/ROADMAP.md) (Writer por seção — `writer_section_node` e tipos `Article`/`Section` disponíveis)

### Funcionalidades:

#### 2.0 Proposta de Estrutura pelo Estruturador

- **Descrição:** Quando o contexto conversacional é suficiente, o Estruturador propõe a estrutura do artigo (lista de títulos de seções) no chat, em linguagem natural. A proposta é extraída pelo produto e popula o painel de artigo com seções vazias. Aprovação é implícita: o Usuário continua a conversa ou pede ajustes via chat (Estruturador re-propõe).
- **Critérios de Aceite:**
  - Deve atualizar `EnsaioState.current_article` com lista de `Section` vazias (`body=""`, `status="empty"`) quando o Estruturador inclui `article_sections` na sua resposta
  - Deve preservar o `current_article` existente se o Estruturador não incluir `article_sections` no turno (nem todo turno do Estruturador propõe estrutura)
  - Deve sobrescrever `current_article` quando o Estruturador re-propõe estrutura (somente se todas as seções ainda estiverem em `status="empty"` — preserva trabalho já feito)
  - Não deve exibir botão "Gerar estrutura" — a proposta emerge da conversa
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:**
    - `core/agents/structurer/nodes.py` — quando `product_context` sinaliza contexto Ensaio e o Estruturador produz outline, incluir `additional_kwargs={"agent": "structurer", "article_sections": ["Título 1", "Título 2", ...]}` na `AIMessage` retornada. Seções somente incluídas quando o LLM decidir propor estrutura (instrução via `product_context`); turnos sem proposta retornam `additional_kwargs={"agent": "structurer"}` sem `article_sections`.
    - `products/ensaio/config/product.yaml` — adicionar instrução ao `focus`: Estruturador deve propor estrutura de seções (em português) quando tiver contexto suficiente do experimento.
    - `products/ensaio/app/state.py` — em `send_message`, após `graph.invoke`, inspecionar `result["messages"]`; se última AIMessage do structurer tiver `additional_kwargs.get("article_sections")` e `current_article` estiver vazio ou todo `"empty"`, popular `current_article`.
  - **Contratos/Shapes:**
    ```python
    # core/agents/structurer/nodes.py — AIMessage com outline:
    AIMessage(
        content="Proposta de estrutura: ...",
        additional_kwargs={
            "agent": "structurer",
            "article_sections": ["Introdução", "Metodologia", "Resultados", "Discussão", "Conclusão"]
        }
    )

    # products/ensaio/app/state.py — extração em send_message:
    last_structurer_msg = next(
        (m for m in reversed(result["messages"])
         if isinstance(m, AIMessage) and m.additional_kwargs.get("agent") == "structurer"),
        None
    )
    if last_structurer_msg:
        sections = last_structurer_msg.additional_kwargs.get("article_sections", [])
        all_empty = all(s["status"] == "empty" for s in (self.current_article or []))
        if sections and (not self.current_article or all_empty):
            self.current_article = [
                {"title": t, "body": "", "status": "empty"} for t in sections
            ]
    ```
  - **Integração:** `additional_kwargs` no Structurer segue o padrão estabelecido em E-PROTO-1.3 (`agent`); Revelar ignora `article_sections` (campo extra é transparente — verificado em E-PROTO-1.3)
  - **Template de referência:** E-PROTO-1.3 (padrão `additional_kwargs` no Structurer)
  - **Acoplamentos verificados:**
    - `core/agents/structurer/nodes.py` — arquivo compartilhado com Revelar. Adição de `article_sections` em `additional_kwargs` é transparente para o Revelar (não lê o campo). **Não-regressão:** rodar `tests/products/revelar/` deve passar 100%.
    - `products/ensaio/config/product.yaml` — instrução adicional ao Orquestrador/Estruturador no contexto Ensaio; sem impacto em Revelar.
  - **Dependências de ordem:** primeiro a executar — 2.1 renderiza o que 2.0 popula
  - **Escopo de teste:**
    - **Unit:** `tests/products/ensaio/unit/test_state_structurer_outline.py` — mock de `graph.invoke` retornando AIMessage com `article_sections`; verificar que `current_article` é populado; verificar que turno sem `article_sections` não sobrescreve `current_article` existente; verificar que re-proposta só sobrescreve se tudo `"empty"`
    - **Não-regressão Revelar:** rodar `tests/products/revelar/` sem modificações; deve passar 100%
    - **Validação manual:** conduzir conversa sobre experimento; verificar que painel se popula quando Estruturador propõe estrutura; pedir ajuste ("use seção de Limitações"); verificar re-proposta; iniciar geração de seção; verificar que nova proposta não sobrescreve

#### 2.1 Painel Seccionado

- **Descrição:** Substitui o markdown plano da POC por um painel que renderiza cada seção do artigo como bloco individual com cabeçalho visível e indicador de status. Seções chegam via 2.0 (proposta do Estruturador); painel é vazio até a primeira proposta.
- **Critérios de Aceite:**
  - Deve renderizar cada `Section` de `EnsaioState.current_article` como bloco separado: `title` como cabeçalho, `body` como markdown
  - Deve exibir indicador de status por seção: `"empty"` → placeholder "Clique em Gerar"; `"draft"` → badge "Rascunho"; `"edited"` → badge "Editado"
  - Deve exibir mensagem "Aguardando proposta de estrutura..." quando `current_article` é `None` ou lista vazia (orienta o Usuário a continuar a conversa)
  - Deve manter proporção ~2/5 do layout (coluna direita)
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:** `products/ensaio/app/components/article_panel.py` — refatorar render de markdown plano para iteração sobre lista de `Section` via `rx.foreach`
  - **Contratos/Shapes:**
    - `EnsaioState.current_article: list[Section] | None` — substitui `str | None` do E-PROTO-1.2
    - `Section` importado de `core.agents.writer.models`
    - Mapa de status → label: `{"empty": "Clique em Gerar", "draft": "Rascunho", "edited": "Editado"}`
  - **Integração:** `article_panel.py` lê `EnsaioState.current_article` via `rx.State`; renderiza com `rx.foreach`
  - **Template de referência:** padrão `rx.foreach` da documentação Reflex
  - **Acoplamentos verificados:** mudança de `str` para `list[Section]` em `current_article` requer remover o event handler `generate_article` herdado de E-PROTO-1.2 (substituído por `generate_section` de 2.2)
  - **Dependências de ordem:** depende de 2.0 (que popula o state) — 2.2, 2.3 e 2.4 estendem este painel
  - **Escopo de teste:**
    - **Unit:** `tests/products/ensaio/unit/test_article_panel_sections.py` — renderizar lista com 0, 1 e N sections; verificar badge correto para cada status; verificar mensagem de estado vazio
    - **Validação manual:** painel exibe "Aguardando..." antes da proposta; exibe seções após 2.0; badges corretos

#### 2.2 Geração e Regeneração por Seção

- **Descrição:** Botões "Gerar" / "Regenerar" por seção invocam `writer_section_node` no escopo daquela seção. As seções já existem no painel (propostas pelo Estruturador em 2.0); estes botões preenchem o conteúdo de cada uma.
- **Critérios de Aceite:**
  - Deve exibir botão "Gerar" por seção quando `body == ""`; botão "Regenerar" quando `body != ""`
  - Deve invocar `writer_section_node({messages, focal_argument, section_title, current_body, article_context, product_context})`
  - `article_context` deve ser construído a partir das demais seções já redigidas (resumo em texto simples, excluindo a seção-alvo)
  - Deve atualizar `current_article[i]["body"]` e setar `status="draft"` ao retornar
  - Deve exibir indicador de processamento inline para a seção em geração (reaproveitando `processing_agent="writer"` de E-PROTO-1.4)
  - Deve preservar edições das outras seções durante regeneração de uma seção específica
  - Deve desabilitar todos os botões de geração enquanto `processing_agent` não é nulo (evita disparo duplo)
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:**
    - `products/ensaio/app/state.py` — event handler `generate_section(section_index: int)`; helper `_build_article_context(article, exclude_index)` (função privada no módulo)
    - `products/ensaio/app/components/article_panel.py` — botões por seção que disparam `EnsaioState.generate_section(i)`
  - **Contratos/Shapes:**
    ```python
    async def generate_section(self, section_index: int):
        section = self.current_article[section_index]
        article_context = _build_article_context(self.current_article, exclude_index=section_index)
        self.processing_agent = "writer"
        try:
            result = writer_section_node({
                "messages": self.langchain_history,
                "focal_argument": self.focal_argument,
                "section_title": section["title"],
                "current_body": section["body"],
                "article_context": article_context,
                "product_context": self._product_context,
            })
            self.current_article[section_index]["body"] = result["section_content"]
            self.current_article[section_index]["status"] = "draft"
        finally:
            self.processing_agent = None
    ```
  - **Integração:** `writer_section_node` importado diretamente (mesmo padrão do `writer_node` na POC)
  - **Template de referência:** event handler `generate_article` em `state.py` (E-PROTO-1.2)
  - **Acoplamentos verificados:**
    - `writer_section_node` de C-ENSAIO-3.2
    - `processing_agent` de E-PROTO-1.4 (reaproveitado sem mudança de contrato)
  - **Dependências de ordem:** depende de 2.1 (painel) e C-ENSAIO-3.2 (`writer_section_node`)
  - **Escopo de teste:**
    - **Unit:** `tests/products/ensaio/unit/test_state_generate_section.py` — mock de `writer_section_node`; verificar que índice correto é atualizado; que outras seções não mudam; que `processing_agent` é limpo no finally; que disparo duplo é bloqueado
    - **Validação manual:** gerar seção 1; verificar que seção 2 não muda; regenerar seção 1; verificar atualização correta

#### 2.3 Edição Inline de Seção

- **Descrição:** Usuário edita o markdown de uma seção diretamente no painel, sem regenerar; alteração entra no estado com status `"edited"`.
- **Critérios de Aceite:**
  - Deve permitir edição do corpo de uma seção via `rx.textarea` inline (toggle entre modo view e modo edição)
  - Deve atualizar `current_article[i]["body"]` ao sair do campo (on_blur)
  - Deve setar `current_article[i]["status"] = "edited"` na primeira edição manual
  - Edição manual deve ser preservada quando outras seções são regeneradas
  - Não deve triggerar regeneração automática — edição é ação exclusiva do Usuário
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:**
    - `products/ensaio/app/state.py` — event handler `update_section_content(section_index: int, content: str)`; campo auxiliar `editing_section_index: int | None` para controle de toggle
    - `products/ensaio/app/components/article_panel.py` — renderizar `rx.textarea` quando `editing_section_index == i`, caso contrário renderizar markdown
  - **Contratos/Shapes:**
    ```python
    def update_section_content(self, section_index: int, content: str):
        self.current_article[section_index]["body"] = content
        self.current_article[section_index]["status"] = "edited"
        self.editing_section_index = None
    ```
  - **Integração:** event handler simples, sem chamada ao core
  - **Template de referência:** padrão `rx.textarea` com `on_blur` em Reflex
  - **Acoplamentos verificados:** somente `EnsaioState`; nenhum acoplamento com core
  - **Dependências de ordem:** depende de 2.1 (painel seccionado)
  - **Escopo de teste:**
    - **Unit:** `tests/products/ensaio/unit/test_state_section_edit.py` — verificar que `status` vira `"edited"`; que conteúdo é atualizado; que outras seções não são tocadas
    - **Validação manual:** editar seção 2; regenerar seção 1; verificar que edição da seção 2 persiste com badge "Editado"

#### 2.4 Status por Seção

- **Descrição:** Sinalização visual inline do estado de cada seção (vazia / rascunho / editada) para guiar o Usuário sobre onde focar.
- **Critérios de Aceite:**
  - Deve exibir badge inline no cabeçalho de cada seção baseado em `Section.status`
  - Badge deve ser visível sem hover
  - Não deve interferir com botões de geração ou campo de edição
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:** `products/ensaio/app/components/article_panel.py` — badge junto ao título (implementado como parte de 2.1; listado separadamente por ser comportamento distinto)
  - **Contratos/Shapes:** mapa `{"empty": "—", "draft": "Rascunho", "edited": "Editado"}` (mesmo de 2.1)
  - **Integração:** puramente visual; lê `Section.status` do estado
  - **Template de referência:** mapa de labels de agente em `chat_panel.py` (E-PROTO-1.3)
  - **Acoplamentos verificados:** somente `EnsaioState.current_article`
  - **Dependências de ordem:** implementado junto com 2.1
  - **Escopo de teste:** coberto pelos testes de 2.1

---

#### ÉPICO E-PROTO-3: Metodologista Aplicado ao Ensaio

**Objetivo:** Trazer o Metodologista (agente do core existente, parado desde a POC) para o grafo do Ensaio, num modo conversacional de provocação — métricas ausentes, evidências faltantes, afirmações sem suporte, dimensões do artigo não declaradas. Endereça a expectativa de que ao final do Protótipo o sistema empurre o artigo para evoluir com qualidade, não só ajude a transcrever o que foi dito.

**Nota arquitetural:** o Metodologista existente opera em modo de decisão pontual (`decide_collaborative` → `approved/needs_refinement/rejected`). Para o Ensaio é criado um nó separado, `methodologist_provocation_node`, com prompt próprio focado em provocação contínua ao longo da conversa. O `decide_collaborative` permanece inalterado.

**Status:** ✅ Implementado — branch `claude/implement-essay-prototype-uFkkP`

**Dependências:**
- E-POC-2 (parametrização de contexto — já entregue)
- E-PROTO-1 (nova stack — para que a provocação tenha distinção visual no chat via `additional_kwargs["agent"]`)

### Funcionalidades:

#### 3.1 `methodologist_provocation_node` no core

- **Descrição:** Novo nó stateless em `core/agents/methodologist/nodes.py`, separado do `decide_collaborative` existente. Opera em modo conversacional: dado o histórico e o argumento focal, produz uma provocação (pergunta ou sugestão) sobre lacunas metodológicas, métricas ausentes, afirmações sem suporte ou dimensões do artigo não declaradas.
- **Critérios de Aceite:**
  - Deve aceitar `MultiAgentState` (via dict) com `messages` e `focal_argument`; respeitar `product_context` via `config.configurable.product_context`
  - Deve retornar `{"messages": [AIMessage(content=provocação, additional_kwargs={"agent": "methodologist"})]}`
  - Deve produzir provocação conversacional em linguagem natural quando identifica lacuna
  - Quando não há lacuna identificável, deve retornar mensagem neutra curta (ex.: "Parece que o contexto está bem descrito. Continue.") — nunca retornar vazio ou erro
  - Não deve retornar veredito (`aprovado`/`rejeitado`) — apenas perguntas ou sugestões
  - Não deve modificar `decide_collaborative` nem nenhuma função existente em `nodes.py`
- **Detalhes de execução:**
  - **Arquivos a criar:** `core/prompts/methodologist_provocation.py` — prompt `METHODOLOGIST_PROVOCATION_PROMPT_V1`
  - **Arquivos a modificar:** `core/agents/methodologist/nodes.py` — adicionar `methodologist_provocation_node` ao final
  - **Contratos/Shapes:**
    ```python
    def methodologist_provocation_node(state: dict, config: RunnableConfig | None = None) -> dict:
        """
        Input (campos de MultiAgentState usados):
            messages:       list[BaseMessage]
            focal_argument: dict | None
            product_context via config.configurable

        Output:
            messages: [AIMessage(content=..., additional_kwargs={"agent": "methodologist"})]
        """
    ```
  - **Integração:** registrado como nó `"methodologist"` no grafo do Ensaio por 3.2; invocado quando `route_from_orchestrator` retorna `"methodologist"`
  - **Template de referência:** estrutura do `writer_section_node` de C-ENSAIO-3.2 (stateless, prompt + invoke, retorno dict de messages)
  - **Acoplamentos verificados:**
    - `decide_collaborative` — não tocado; nós independentes no mesmo arquivo
    - **Consumidores do arquivo `methodologist/nodes.py`:** core multi-agent graph (Revelar usa `decide_collaborative`); adição ao final do arquivo não quebra imports existentes
    - **Não-regressão Revelar:** `decide_collaborative` permanece inalterado; rodar `tests/products/revelar/` deve passar 100%
  - **Dependências de ordem:** primeiro a executar em E-PROTO-3 — 3.2 registra este nó no grafo
  - **Escopo de teste:**
    - **Unit:** `tests/core/unit/agents/methodologist/test_methodologist_provocation_node.py` — mock do LLM; verificar `additional_kwargs["agent"] == "methodologist"`; verificar que output é lista com 1 AIMessage; rodar testes existentes do methodologist (não-regressão do `decide_collaborative`)
    - **Não-regressão Revelar:** rodar `tests/products/revelar/` sem modificações; deve passar 100%

#### 3.2 Inclusão do Metodologista no Grafo do Ensaio

- **Descrição:** Atualizar `products/ensaio/app/graph.py` para registrar `methodologist_provocation_node` como nó `"methodologist"` e remover o bloqueio que desviava essa rota para o usuário.
- **Critérios de Aceite:**
  - Deve registrar `methodologist_provocation_node` como nó `"methodologist"` no grafo
  - Deve remover o bloco `if destination == "methodologist": return "user"` de `_route`
  - Após execução do nó, deve rotear para END (Metodologista fala e devolve ao Usuário, sem loop)
  - Deve preservar a rota `"structurer" → END` existente sem alteração
  - `create_ensaio_graph()` deve manter assinatura e contrato inalterados
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:** `products/ensaio/app/graph.py`
  - **Contratos/Shapes:**
    ```python
    # _route após mudança — sem bloqueio:
    def _route(state: MultiAgentState) -> str:
        return route_from_orchestrator(state)  # "structurer", "methodologist" ou "user"

    # no grafo:
    graph.add_node("methodologist", methodologist_provocation_node)
    graph.add_edge("methodologist", END)
    ```
  - **Integração:** `route_from_orchestrator` já retorna `"methodologist"` quando o Orquestrador sugere o agente; o grafo só precisava desbloquear o caminho
  - **Template de referência:** registro de `structurer_node` no mesmo `graph.py`
  - **Acoplamentos verificados:**
    - `route_from_orchestrator` em `core/agents/orchestrator/router.py` — sem mudança; já suporta `"methodologist"` no retorno
    - `methodologist_provocation_node` de 3.1 — dependência direta
  - **Dependências de ordem:** depende de 3.1
  - **Escopo de teste:**
    - **Unit:** `tests/products/ensaio/unit/test_ensaio_graph_methodologist.py` — instanciar grafo; verificar que nó `"methodologist"` existe; verificar que a rota `"methodologist"` não vai diretamente para END sem passar pelo nó
    - **Validação manual via script:** adaptar `scripts/ensaio/flows/validate_graph.py` para verificar que grafo compila com o nó Metodologista

#### 3.3 Postura de Provocação Seletiva

- **Descrição:** O Orquestrador é orientado a sugerir o Metodologista seletivamente — apenas quando a conversa toca em metodologia, resultados ou afirmações sem suporte — via ajuste do `product_context` do Ensaio.
- **Critérios de Aceite:**
  - Deve ajustar `products/ensaio/config/product.yaml` para instruir o Orquestrador a sugerir o Metodologista apenas em turnos com conteúdo metodológico
  - O Orquestrador não deve sugerir o Metodologista em turnos puramente descritivos ou de contexto geral
  - Deve produzir ao menos 1 provocação por sessão quando o Usuário descreve experimento com resultados quantitativos (critério de validação manual)
  - Não deve modificar o prompt base do Orquestrador em `core/prompts/` — apenas o conteúdo do `product.yaml`
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:** `products/ensaio/config/product.yaml` — expandir campo `focus` com instrução de roteamento seletivo para Metodologista
  - **Contratos/Shapes:** campo `focus` é string livre injetada via `{product_context_section}` no prompt do Orquestrador; sem schema formal
  - **Integração:** `load_product_context()` lê o YAML e injeta na invocação do grafo — sem mudança de código, só conteúdo do YAML
  - **Template de referência:** `products/ensaio/config/product.yaml` atual
  - **Acoplamentos verificados:** `products/ensaio/app/product_config.py` — sem mudança; lê YAML e devolve string. Revelar tem YAML próprio sem acoplamento.
  - **Dependências de ordem:** depende de 3.2 (Metodologista no grafo)
  - **Escopo de teste:**
    - **Validação manual:** conduzir sessão sobre experimento com resultado quantitativo; verificar que Metodologista aparece perguntando sobre métricas; verificar que não aparece em turno de contexto geral puro
    - Comportamento conversacional não tem teste automatizado neste nível (aceitável no Protótipo)

#### 3.4 Reforço da Coerência do Artigo com o Contexto

- **Descrição:** Provocações do Metodologista entram no histórico conversacional e automaticamente informam o Writer na próxima geração. Complementar: ajuste fino do `product_context` para reduzir promessas vazias do Orquestrador identificadas na POC ("vou validar...", "verificarei...").
- **Critérios de Aceite:**
  - Deve verificar em validação manual que artigo gerado após provocação do Metodologista incorpora a resposta do Usuário
  - Deve ajustar `product_context` para reduzir promessas vazias do Orquestrador (feedback da validação da POC)
  - O Writer não precisa de mudança de código — já consome o histórico integralmente
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum
  - **Arquivos a modificar:** `products/ensaio/config/product.yaml` — acrescentar instrução anti-promessa-vazia ao `focus` (junto com 3.3, no mesmo arquivo)
  - **Contratos/Shapes:** mesmo que 3.3 (campo `focus` no YAML)
  - **Integração:** histórico conversacional já é passado ao Writer integralmente; nenhuma mudança de código
  - **Acoplamentos verificados:** nenhum novo
  - **Dependências de ordem:** implementado junto com 3.3
  - **Escopo de teste:**
    - **Validação manual:** gerar artigo antes e depois de turno com Metodologista; verificar que versão posterior é mais densa em metodologia

#### 3.5 Provocação sobre Dimensões do Artigo

- **Descrição:** O prompt do `methodologist_provocation_node` cobre também as 4 dimensões em que o Writer opera (contexto, intenção, formato, estrutura — ver `core/docs/agents/overview.md`): quando alguma não está clara na conversa, o Metodologista pergunta. Mesma postura seletiva de 3.3.
- **Critérios de Aceite:**
  - O prompt `METHODOLOGIST_PROVOCATION_PROMPT_V1` deve cobrir as 4 dimensões do Writer além das lacunas de rigor
  - Quando intenção do artigo não está declarada, deve perguntar (ex.: "Este artigo é para informar resultados ou propor uma abordagem?")
  - Mesma postura seletiva — não provoca sobre dimensões a cada turno
  - Não requer nó ou arquivo adicional (coberto no prompt de 3.1)
- **Detalhes de execução:**
  - **Arquivos a criar:** nenhum além do prompt de 3.1
  - **Arquivos a modificar:** `core/prompts/methodologist_provocation.py` — garantir que `METHODOLOGIST_PROVOCATION_PROMPT_V1` cobre as 4 dimensões além das lacunas de rigor; dimensões referenciadas de `core/docs/agents/overview.md`
  - **Contratos/Shapes:** coberto pelo contrato de 3.1
  - **Integração:** mesma que 3.1
  - **Acoplamentos verificados:** `core/docs/agents/overview.md` consultado durante escrita do prompt (referência documental)
  - **Dependências de ordem:** implementado junto com 3.1
  - **Escopo de teste:** coberto pela validação manual de 3.3 (verificar provocação sobre intenção quando não declarada)

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
