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
- **Status:** `🔍 Detalhes definidos`
- **Épicos agrupados:** E-PROTO2-1, E-PROTO2-2, E-PROTO2-3, E-PROTO2-4 — todos em `🔍 Detalhes definidos`
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

**Acoplamentos com core (verificados):**
- E-PROTO2-1: campo condicional `rationale` em `core/agents/structurer/nodes.py:217-227` (gated por `product_context`, mesmo padrão de `article_sections`). `core/prompts/structurer.py` **não é tocado** — `STRUCTURER_REFINEMENT_PROMPT_V1` só roda no fluxo de refinamento V2/V3 do Revelar; Ensaio nunca cai lá. Postura no `products/ensaio/config/product.yaml`.
- E-PROTO2-2: prompt em `core/prompts/methodologist_provocation.py`. **Verificado em `core/docs/agents/methodologist/responsibilities.md:41,68`:** `methodologist_provocation_node` é exclusivo do Ensaio; Revelar usa `decide_collaborative` em outro caminho. Mudança é segura para Revelar.
- E-PROTO2-3: contrato `change_summary` em `AIMessage.additional_kwargs` (aditivo, opcional, cruza core ↔ produto). Produtores: `core/agents/structurer/nodes.py:371-380` (já gated por `product_context` para Ensaio), `core/agents/methodologist/nodes.py:882-885` (Ensaio-only), `core/agents/orchestrator/nodes.py:1033` (compartilhado — só preenche quando `focal_argument` muda; Revelar não regride porque o campo é puramente aditivo).
- E-PROTO2-4: puro UI (`products/ensaio/app/components/article_panel.py`), sem acoplamento com core.

**Feedback do estágio anterior endereçado:**
- "Estruturador propôs sem expor racional nem pedir confirmação" (validação PROTO-ENSAIO) → E-PROTO2-1.
- "Mensagem do Estruturador longa sem sinalizar o que o sistema fez" → E-PROTO2-3.
- "'Vou estruturar essa nova questão de pesquisa' — usuário não entendeu o que mudou" → E-PROTO2-3.
- "Metodologista existe mas não aparece no chat" → E-PROTO2-2 (papel afiado torna a presença legível quando convocado).
- "Seções do artigo não podem ser colapsadas/expandidas" → E-PROTO2-4.

**Nota:** milestone em `🔍 Detalhes definidos` — apto ao fluxo autônomo. Checklist de `docs/process/refinement/autonomous_readiness.md` aplicado nas seis categorias; ajuste por estágio Protótipo respeitado. Sizing avaliado antes do dispatch.

**Ordem de execução entre épicos (sizing-friendly):**
1. E-PROTO2-2 primeiro — limpa territórios via prompt do Metodologista e `product.yaml`. Pré-requisito conceitual para E-PROTO2-1 (Estruturador só fica afiado depois do Metodologista assumir escopo/qualidade).
2. E-PROTO2-1 depois — co-decisão com proposta pendente, bubble especial, edição leve, `rationale` condicional. Integra naturalmente com E-PROTO2-3.3 (manchete "📐 Estrutura proposta").
3. E-PROTO2-3 em paralelo a E-PROTO2-1 — contrato e render do `change_summary`; três produtores cobertos no fim do milestone.
4. E-PROTO2-4 por último — accordion no painel é puro UI e não bloqueia o restante.

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

**Status:** 🔍 Detalhes definidos

**Objetivo:** Tornar a estrutura proposta pelo Estruturador um ato de co-decisão. O Estruturador propõe storytelling com racional curto; a proposta vira bubble especial e só comita em `current_article` após o Usuário aceitar (com possibilidade de edição leve antes).

### Funcionalidades:

#### E-PROTO2-1.1 Proposta sem commit
- **Descrição:** Estruturador deixa de comitar direto em `current_article`. Output passa a ser uma proposta pendente, mantida em campo separado do estado, aguardando ação do Usuário.
- **Critérios de Aceite:**
  - Quando o Estruturador entrega `article_sections` em `additional_kwargs`, o estado armazena em `pending_structure_proposal` (novo campo em `EnsaioState`) e **não** escreve em `current_article`
  - `current_article` só é atualizado quando o Usuário aceita (ou edita-e-aceita) a proposta
  - Re-proposições do Estruturador substituem a proposta pendente; não há fila de propostas
  - Painel direito continua refletindo `current_article` — fica vazio até o aceite
  - Não regredimos comportamento existente: aceite produz o mesmo `current_article` que o auto-commit atual produzia
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/state.py` (linhas 64-83 — adicionar campo; 159-194 — substituir lógica de auto-commit; novos event handlers).
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** `EnsaioState.pending_structure_proposal: dict | None`, formato `{"sections": list[str], "rationale": str}` ou `None`. Em `initialize`, valor inicial é `None`. Quando `current_article` é commitado, o pendente é zerado.
  - **Integração:** no event handler `send_message`, a partir da linha 159 (já existente), em vez de escrever em `article_sections_update` quando o Estruturador propõe, o código grava em `pending_structure_proposal_update` e **não** atualiza `current_article`. Dois novos event handlers `accept_structure_proposal()` e `reject_structure_proposal()` lidam com a transição (chamados pelos botões da bubble — E-PROTO2-1.2).
  - **Template de referência:** padrão de event handler em background atual em `state.py:115-210` (`send_message`); padrão de event handler síncrono em `state.py:266-280` (`start_editing_section`, `update_section_content`).
  - **Acoplamentos verificados:** state.py linha 165-173 é a única origem do auto-commit. Painel direito (`article_panel.py:99-130`) já lida graciosamente com `current_article` vazio, mostrando "Aguardando proposta de estrutura..." — mensagem permanece adequada enquanto a proposta está pendente.
  - **Dependências de ordem:** vem antes de E-PROTO2-1.2 (a bubble lê `pending_structure_proposal`).
  - **Escopo de teste:** unit em `state.py` (event handlers `accept_structure_proposal` / `reject_structure_proposal` produzem updates corretos); validação manual via sessão real (proposta vem, bubble aparece, aceitar comita, recusar limpa).

#### E-PROTO2-1.2 Bubble de proposta com ações
- **Descrição:** Proposta pendente é renderizada como bubble especial no chat, visualmente distinto de mensagem conversacional, com ações aceitar / editar / recusar.
- **Critérios de Aceite:**
  - Bubble especial mostra: lista das seções propostas, racional curto do Estruturador, três botões (Aceitar / Editar / Recusar)
  - **Aceitar** comita `pending_structure_proposal` em `current_article` e limpa o pendente
  - **Recusar** limpa `pending_structure_proposal` sem tocar `current_article`; bubble é substituído por nota curta no histórico
  - Bubble é distinguível dos bubbles de conversa por borda/fundo dedicado
  - Enquanto a proposta está pendente, o input do chat continua habilitado (não bloqueia conversa)
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/components/chat_panel.py` (renderização condicional acima do input ou intercalada com `messages` por timestamp).
  - **Arquivos a criar:** `products/ensaio/app/components/proposal_bubble.py` — componente `_proposal_bubble()` que recebe `EnsaioState.pending_structure_proposal` e renderiza lista + racional + botões.
  - **Contratos/Shapes:** componente lê `EnsaioState.pending_structure_proposal` e despacha `EnsaioState.accept_structure_proposal` / `EnsaioState.reject_structure_proposal` / `EnsaioState.start_editing_proposal` (este último delega para E-PROTO2-1.3).
  - **Integração:** `chat_panel.py` envolve a área de mensagens com `rx.cond(EnsaioState.pending_structure_proposal != None, _proposal_bubble(), rx.fragment())` posicionado logo acima do input do chat (após `_processing_indicator` ou junto a ele). Bubble persiste enquanto pendente, some no aceite/recusa.
  - **Template de referência:** estrutura visual em `chat_panel.py:14-50` (`_message_bubble`). Distinção visual via `border="2px solid var(--accent-9)"`, fundo `var(--accent-2)` e ícone `📐` no header.
  - **Acoplamentos verificados:** componente é puro de UI; só lê estado e despacha eventos. `_message_bubble` continua intacto.
  - **Dependências de ordem:** depende de E-PROTO2-1.1.
  - **Escopo de teste:** validação manual via sessão real (bubble aparece quando Estruturador propõe, três botões funcionam, distinguível de mensagens normais).

#### E-PROTO2-1.3 Edição leve da proposta
- **Descrição:** Antes de aceitar, Usuário pode editar a lista — renomear, reordenar, remover, adicionar seções.
- **Critérios de Aceite:**
  - Botão **Editar** abre a lista em modo editável: campo de texto por seção, controles de mover acima/abaixo, remover seção, adicionar seção ao final
  - Confirmar a edição comita a versão editada em `current_article`
  - Cancelar a edição volta à proposta original, ainda pendente
  - Lista editada vazia (todas removidas) bloqueia o aceite com mensagem inline
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/state.py` (campos e event handlers de edição), `products/ensaio/app/components/proposal_bubble.py` (criado em 1.2 — ganha modo editável).
  - **Arquivos a criar:** nenhum (compartilha `proposal_bubble.py` com 1.2).
  - **Contratos/Shapes:** novos campos no `EnsaioState`: `editing_proposal: bool = False`, `proposal_draft: list[str] = []` (cópia mutável das seções enquanto edita), `proposal_rationale_draft: str = ""`. Event handlers: `start_editing_proposal()`, `update_proposal_section(index: int, value: str)`, `move_proposal_section(index: int, direction: int)`, `remove_proposal_section(index: int)`, `add_proposal_section()`, `confirm_proposal_edit()`, `cancel_proposal_edit()`.
  - **Integração:** botão Editar em 1.2 chama `start_editing_proposal` → estado abre painel editável (textareas por seção + botões ⬆️ ⬇️ 🗑️ por linha + botão "+ Adicionar seção"). Reordenação via dois botões de seta (drag & drop em Reflex puro é caro; descarte explícito). `confirm_proposal_edit` valida `len(proposal_draft) > 0` e comita em `current_article`; `cancel_proposal_edit` zera os drafts e volta a 1.2 sem mudança.
  - **Template de referência:** padrão de edição inline já em `article_panel.py:24-65` (`_section_card` com botões). Botões mover/remover seguem padrão `rx.button(..., size="1", variant="soft")`.
  - **Acoplamentos verificados:** edição é local ao bubble; `current_article` só é tocado no `confirm_proposal_edit`.
  - **Dependências de ordem:** depende de E-PROTO2-1.1 e 1.2.
  - **Escopo de teste:** unit em event handlers de edição (mover, remover, adicionar produzem `proposal_draft` correto); validação manual (renomear, reordenar, remover, adicionar, confirmar, cancelar).

#### E-PROTO2-1.4 Estruturador afiado para storytelling (via product.yaml + campo condicional)
- **Descrição:** A especialização do Estruturador para storytelling do Ensaio acontece **na fronteira do produto**, não no core. Postura no `product.yaml` orienta cobertura exclusiva de ordem/sequência, e um campo `rationale` condicional ao `product_context` é adicionado ao prompt inline do `structurer_node` — mesmo padrão do `article_sections` existente, garantindo que Revelar não regrida.
- **Critérios de Aceite:**
  - `products/ensaio/config/product.yaml` (postura do Estruturador): redesenhada em E-PROTO2-2.2 para descrever **storytelling apenas**, sem cobrir contexto/problema/contribuição (que migra para o Metodologista)
  - `core/agents/structurer/nodes.py:217-227` ganha bloco condicional `rationale_field` análogo a `article_sections_field` — só presente quando `product_context` está setado (Ensaio); ausente para Revelar
  - `core/agents/structurer/nodes.py:287-296` parseia `rationale` da resposta JSON quando presente; `core/agents/structurer/nodes.py:371-380` propaga em `additional_kwargs["rationale"]`
  - **Não toca** `core/prompts/structurer.py` nem `core/config/agents/structurer.yaml` (esses moldam o fluxo Revelar; mudança ali quebraria o caminho `_refine_question`)
  - Estruturador no Ensaio entrega seções + racional curto; Estruturador no Revelar continua entregando context/problem/contribution/structured_question como hoje
- **Detalhes de execução:**
  - **Arquivos a modificar:** `core/agents/structurer/nodes.py` (linhas 217-227 — adicionar `rationale_field` e `rationale_note` condicionais; linhas 280-296 — parsear `rationale`; linhas 371-380 — propagar em `additional_kwargs`). `products/ensaio/config/product.yaml` (postura do Estruturador, ver E-PROTO2-2.2).
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** JSON do Estruturador ganha campo `"rationale": str` opcional (≤2 frases, pt-BR) quando `product_context` está presente. `additional_kwargs` ganha `rationale: str` quando o LLM o devolve, ausente caso contrário.
  - **Integração:** mesmo padrão de `article_sections` (linhas 217-227, 287-296, 371-380). Bloco `rationale_field` injeta em formato JSON; `rationale_note` instrui o LLM a preencher; parser respeita ausência (default `""`); propagação em `additional_kwargs` é gated por presença não-vazia.
  - **Template de referência:** o próprio `article_sections` em `nodes.py:217-227, 287-296, 371-380` — réplica direta do padrão.
  - **Acoplamentos verificados:** Revelar não passa `product_context` (verificado em `products/revelar/app/components/chat_input.py:23-25` — usa `create_multi_agent_graph` sem `configurable.product_context`). Logo, `article_sections_field` e o novo `rationale_field` ficam vazios para Revelar; comportamento legado preservado bit-a-bit. `STRUCTURER_REFINEMENT_PROMPT_V1` permanece intocado — caminho `_refine_question` é Revelar puro.
  - **Dependências de ordem:** acoplado a E-PROTO2-2.2 (postura no product.yaml). Independente das demais funcionalidades de E-PROTO2-1; `rationale` é consumido visualmente em E-PROTO2-1.2 (bubble).
  - **Escopo de teste:** unit em `structurer_node` validando que `additional_kwargs["rationale"]` aparece quando `product_context` está presente e o JSON traz o campo, e está ausente quando não há `product_context` (cobre não-regressão de Revelar). Validação manual via sessão real do Ensaio.

**Dependências:** PROTO-ENSAIO ✅. Acoplado a E-PROTO2-2 (limpeza de prompts é trabalho conjunto entre Estruturador e Metodologista; postura do Estruturador está em E-PROTO2-2.2).

---

#### ÉPICO E-PROTO2-2: Metodologista com escopo e qualidade afiados

**Status:** 🔍 Detalhes definidos

**Objetivo:** Dar ao Metodologista papel claro e único — escopo e qualidade da mensagem. Eliminar a sobreposição atual com o Estruturador, deixando o Metodologista provocar sobre tese central, evidência, afirmação sem suporte e intenção do artigo. Visibilidade emerge da clareza de papel quando o Orquestrador convoca, não de gatilhos determinísticos no grafo.

### Funcionalidades:

#### E-PROTO2-2.1 Prompt do Metodologista limpo
- **Descrição:** Prompt de provocação do Metodologista deixa de cobrir "Formato (IMRaD, etc)" e "Estrutura (seções)" — território do Estruturador. Ganha **Tese central** como dimensão própria.
- **Critérios de Aceite:**
  - `core/prompts/methodologist_provocation.py` remove os bullets "Formato" e "Estrutura" da seção "Dimensões do artigo"
  - Adiciona dimensão **Tese central** (afirmação principal que sustenta o artigo) — explícita, não só implícita em "afirmações sem suporte"
  - Preserva: métricas/evidências, rigor metodológico, afirmações sem suporte, contexto, intenção
  - Postura inalterada: uma pergunta por vez, seletivo, tom colaborativo, nunca retorna vazio, nunca menciona "Metodologista" em primeira pessoa
  - Output continua sendo uma única pergunta em pt-BR ou frase curta de aceite
- **Detalhes de execução:**
  - **Arquivos a modificar:** `core/prompts/methodologist_provocation.py` (linhas 30-34 da seção "Dimensões do artigo").
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** prompt é string. Output do nó é `AIMessage(content=str, additional_kwargs={"agent": "methodologist", ...})` — formato inalterado.
  - **Integração:** prompt é carregado em `core/agents/methodologist/nodes.py:803` (import) e usado em :854-858. Mudança é puramente textual; nenhuma alteração no `methodologist_provocation_node`.
  - **Template de referência:** estrutura atual do próprio prompt — manter postura, dimensões 1-3, sub-bullets de Contexto/Intenção; trocar Formato/Estrutura por **Tese central**.
  - **Acoplamentos verificados:** `methodologist_provocation_node` é exclusivo do Ensaio (`core/docs/agents/methodologist/responsibilities.md:41,68`). `decide_collaborative` (Revelar) está em outro nó e usa outros prompts (`METHODOLOGIST_DECIDE_PROMPT_V2`, `core/config/agents/methodologist.yaml`) — não tocado. Mudança não regride Revelar.
  - **Dependências de ordem:** independente; pré-requisito conceitual de E-PROTO2-1.4 e E-PROTO2-2.2 (territórios afiados primeiro).
  - **Escopo de teste:** validação manual via sessão real (Metodologista provoca sobre tese/evidência/intenção quando convocado, sem mencionar formato/estrutura). Sem teste automatizado de prompt — escopo de Protótipo aceita validação manual.

#### E-PROTO2-2.2 Postura do Orquestrador em `product.yaml` revisada
- **Descrição:** `products/ensaio/config/product.yaml` reescreve a postura do Orquestrador para refletir os papéis afiados — Estruturador = storytelling; Metodologista = escopo e qualidade da mensagem. Sem prescrever ordem entre eles.
- **Critérios de Aceite:**
  - Postura do Estruturador é descrita como **storytelling** (ordem e sequência de seções), explicitamente sem cobrir contexto/problema/contribuição (que migra para o Metodologista)
  - Trigger do Metodologista é alargado: "tese central sem suporte, evidência, intenção do artigo, afirmação não fundamentada", além de métricas/quantitativo
  - Nenhum texto prescreve ordem Metodologista→Estruturador ou Estruturador→Metodologista
  - Postura "anti-promessa-vazia" do Orquestrador permanece inalterada
  - Adiciona instrução para o Estruturador preencher campo `rationale` (≤2 frases) ao propor `article_sections` — habilita E-PROTO2-1.4
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/config/product.yaml` (linhas 25-46 — postura do Orquestrador e do Estruturador).
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** YAML continua tendo a única chave obrigatória `focus`. Texto da postura continua em prosa livre injetado via `config.configurable.product_context`.
  - **Integração:** `product_context` é injetado nos prompts do Orquestrador, Estruturador e Writer em runtime via `{product_context_section}` (E-POC-2.3). Nenhuma mudança em código consumidor.
  - **Template de referência:** estrutura atual do próprio `product.yaml:25-53` — preservar formato em prosa numerada com seções "POSTURA OBRIGATÓRIA DO ORQUESTRADOR" / "POSTURA DO ESTRUTURADOR".
  - **Acoplamentos verificados:** Revelar não passa `product_context` (verificado em `products/revelar/app/components/chat_input.py:23-25`); mudança no YAML não afeta Revelar. `core/prompts/orchestrator.py` e `core/prompts/structurer.py` (e o YAML do Estruturador) já têm o placeholder `{product_context_section}` que vira string vazia para Revelar.
  - **Dependências de ordem:** depende de E-PROTO2-2.1 (papéis afiados primeiro no prompt do Metodologista, depois traduzidos para a postura do produto).
  - **Escopo de teste:** validação manual via sessão real (Orquestrador sugere o Metodologista também em pontas de tese/intenção, não só métricas; Estruturador foca em ordem de seções; nenhuma sequência fixa entre os dois).

#### E-PROTO2-2.3 Sem gancho determinístico no grafo (aceite negativo)
- **Descrição:** Verificação de que o roteamento entre agentes permanece via Orquestrador, sem edges fixas no grafo. Não introduz código novo.
- **Critérios de Aceite:**
  - `products/ensaio/app/graph.py` mantém `route_from_orchestrator` como único decisor entre `structurer | methodologist | user`
  - Nenhuma edge nova é adicionada entre `methodologist` e `structurer`
  - Documentado na PR de fechamento que a restrição de fluidez do milestone foi respeitada
- **Detalhes de execução:**
  - **Arquivos a modificar:** nenhum (aceite negativo).
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** N/A — verificação documental.
  - **Integração:** confirmar visualmente em `products/ensaio/app/graph.py:65-82` que continuam existindo apenas:
    - `graph.add_node("structurer", structurer_node)`
    - `graph.add_node("methodologist", methodologist_provocation_node)`
    - `route_from_orchestrator` como condicional única
    - Edges `structurer → END` e `methodologist → END`
    - **Nenhuma** edge de `structurer → methodologist` ou `methodologist → structurer`
  - **Template de referência:** estado atual do próprio `graph.py` é o template — não regrir.
  - **Acoplamentos verificados:** `route_from_orchestrator` é Ensaio-only (definido em `products/ensaio/app/graph.py`); não compartilhado com Revelar.
  - **Dependências de ordem:** verificação no fim da implementação do milestone.
  - **Escopo de teste:** revisão de código na PR de fechamento. Sem teste automatizado adicional — verificação é documental.

**Dependências:** PROTO-ENSAIO ✅. Acoplado a E-PROTO2-1 (limpeza de prompts é trabalho conjunto).

---

#### ÉPICO E-PROTO2-3: Manchete "o que mudou" em mensagens de agente

**Status:** 🔍 Detalhes definidos

**Objetivo:** Cada mensagem de agente que toca estado passa a vir com manchete pequena acima do conteúdo, sumarizando qual estado foi tocado (estrutura proposta, foco atualizado, lacuna apontada). Usuário deixa de precisar ler parágrafo inteiro para descobrir o que aconteceu.

### Funcionalidades:

#### E-PROTO2-3.1 Contrato `change_summary` em `additional_kwargs`
- **Descrição:** Campo aditivo, opcional, em `AIMessage.additional_kwargs`. Agentes que tocam estado preenchem; agentes em turno conversacional puro não preenchem.
- **Critérios de Aceite:**
  - Tipo do campo: string curta em pt-BR, ≤80 caracteres
  - Quando ausente ou vazio, bubble renderiza como hoje (sem manchete)
  - Quando presente, manchete aparece acima do conteúdo do bubble
  - Campo é puramente aditivo — não substitui nem altera nenhum outro campo de `additional_kwargs`
  - Estado `messages` em `state.py` propaga o campo opcional do `AIMessage.additional_kwargs` para o dict serializado da mensagem
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/state.py:181-189` (event handler `send_message` — extrai `change_summary` do `additional_kwargs` e inclui no dict da mensagem). Nenhuma mudança em core nesta funcionalidade.
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:**
    - `AIMessage.additional_kwargs["change_summary"]: str` — pt-BR, ≤80 caracteres, opcional. Ausente significa turno conversacional puro.
    - `EnsaioState.messages[i]: dict` ganha chave opcional `"change_summary": str`. Quando ausente, a chave **pode** estar ausente do dict (não precisa default `""`).
  - **Integração:** em `state.py:181-189`, ao montar o dict da mensagem do assistente, adicionar `"change_summary": getattr(last, "additional_kwargs", {}).get("change_summary", "")` e renderização condicional cuida do resto.
  - **Template de referência:** padrão já presente em `state.py:154` (`agent_key = getattr(last, "additional_kwargs", {}).get("agent")`).
  - **Acoplamentos verificados:** campo é puramente aditivo em `additional_kwargs`. Revelar não consome o `messages` do Ensaio (estados isolados por produto). Outros agentes do core continuam funcionando sem preencher.
  - **Dependências de ordem:** vem antes de E-PROTO2-3.2 e 3.3.
  - **Escopo de teste:** unit em `send_message` (mensagem com `change_summary` no `additional_kwargs` aparece no dict; sem o campo, não aparece).

#### E-PROTO2-3.2 Renderização da manchete no bubble
- **Descrição:** `_message_bubble` em `chat_panel.py` lê `change_summary` do dict da mensagem e renderiza header curto acima do conteúdo.
- **Critérios de Aceite:**
  - Manchete aparece acima do label de agente, em peso/tamanho menor que o conteúdo principal
  - Quando `change_summary` é falsy/ausente, header não é renderizado (bubble fica como hoje)
  - Mensagens do usuário nunca mostram manchete (campo só faz sentido para `AIMessage`)
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/components/chat_panel.py:14-50` (`_message_bubble`).
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** lê `msg["change_summary"]` (string opcional, default ausente). Renderiza header acima do label de agente apenas quando truthy.
  - **Integração:** dentro de `_message_bubble`, antes do bloco do label, adicionar `rx.cond(msg.get("change_summary", ""), rx.text(msg["change_summary"], size="1", weight="medium", color_scheme="accent"), rx.fragment())`. Sem mudança no resto do bubble.
  - **Template de referência:** padrão `rx.cond(...)` já usado para `is_user` e `_processing_indicator` em `chat_panel.py:54-73`.
  - **Acoplamentos verificados:** componente é puro UI; só lê dict da mensagem.
  - **Dependências de ordem:** depende de E-PROTO2-3.1.
  - **Escopo de teste:** validação manual via sessão real (manchete aparece em mensagens de agente que tocam estado, não aparece em conversa pura, não aparece em mensagens do usuário).

#### E-PROTO2-3.3 Três casos cobertos no marco do milestone
- **Descrição:** Os três produtores de mudança de estado preenchem `change_summary` ao final do milestone. Outros agentes ou turnos puramente conversacionais não preenchem.
- **Critérios de Aceite:**
  - Estruturador propondo/atualizando estrutura (`structurer_node`) → manchete tipo "📐 Estrutura proposta"
  - Mudança de `focal_argument` no Orquestrador (`orchestrator_node`) → manchete tipo "🎯 Foco atualizado" — só quando o foco efetivamente muda em relação ao turno anterior
  - Metodologista apontando lacuna (`methodologist_provocation_node`) → manchete tipo "🔬 Lacuna apontada" — não preenche quando responde "contexto está bem descrito"
  - Orquestrador em turno conversacional puro (sem mudança de foco) **não** preenche o campo
- **Detalhes de execução:**
  - **Arquivos a modificar:** `core/agents/structurer/nodes.py:371-380` (preencher quando `article_sections` está presente — manchete "📐 Estrutura proposta"); `core/agents/methodologist/nodes.py:882-885` (preencher quando o conteúdo não é a frase curta de aceite — manchete "🔬 Lacuna apontada"); `core/agents/orchestrator/nodes.py:1033` (preencher quando `focal_argument` mudar em relação ao turno anterior — manchete "🎯 Foco atualizado").
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** três produtores; cada um adiciona `additional_kwargs["change_summary"]: str`. Strings ≤80 chars, em pt-BR, com emoji e prefixo curto.
  - **Integração:**
    - Estruturador: dentro do bloco onde `article_sections` é detectado (linha 372), também setar `ak["change_summary"] = "📐 Estrutura proposta"`.
    - Metodologista: detectar se `content` é a frase de aceite ("O contexto está bem descrito. Continue.") — se não for, preencher `additional_kwargs["change_summary"] = "🔬 Lacuna apontada"`.
    - Orquestrador: detectar mudança de `focal_argument` comparando com o anterior; quando muda em pelo menos um campo não-vazio, setar `additional_kwargs["change_summary"] = "🎯 Foco atualizado"`.
  - **Template de referência:** linha 371-373 do Estruturador (já popula `additional_kwargs` condicionalmente).
  - **Acoplamentos verificados:**
    - Mudança no Estruturador (`structurer/nodes.py`) é compartilhada com Revelar. Como `change_summary` só é setado quando `article_sections` está presente (e isso só acontece com `product_context` — Ensaio), Revelar não recebe o campo. ✅
    - Mudança no Metodologista (`methodologist/nodes.py`) é em `methodologist_provocation_node`, exclusivo do Ensaio (`responsibilities.md:41,68`). ✅
    - Mudança no Orquestrador (`orchestrator/nodes.py`) é compartilhada com Revelar. Campo é puramente aditivo — `additional_kwargs` aceita chaves arbitrárias; Revelar não lê `change_summary` (lê `agent`). Sem regressão. ✅
  - **Dependências de ordem:** depende de E-PROTO2-3.1 e 3.2 (contrato e render). Acoplado a E-PROTO2-1.1 — quando o Estruturador propõe e o estado vira `pending_structure_proposal`, a manchete "📐 Estrutura proposta" naturalmente acompanha o bubble especial.
  - **Escopo de teste:** unit nos três produtores (manchete presente nos casos esperados; ausente em conversa pura). Validação manual via sessão real.

**Dependências:** PROTO-ENSAIO ✅. Acoplado a E-PROTO2-1 (proposta de estrutura é um dos casos do 3.3).

---

#### ÉPICO E-PROTO2-4: Colapsar/expandir seções no painel

**Status:** 🔍 Detalhes definidos

**Objetivo:** Painel de seções deixa de renderizar tudo expandido. Toggle por seção, todas colapsadas por padrão no estado inicial. Usuário foca no que está trabalhando.

### Funcionalidades:

#### E-PROTO2-4.1 Accordion no painel
- **Descrição:** `article_panel.py` substitui `_section_card` (sempre expandido) por componente colapsável. Cada seção colapsa/expande individualmente.
- **Critérios de Aceite:**
  - Cada seção tem header clicável que alterna entre colapsado e expandido
  - Header colapsado mostra: título da seção, badge de status, indicador visual de expansão (ex.: chevron)
  - Conteúdo expandido mostra: corpo da seção (placeholder ou markdown) e botão Gerar/Regenerar
  - Toggle por seção é independente: expandir uma seção não afeta as outras
  - Edição inline (E-PROTO-2.3) continua funcionando dentro da seção expandida
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/components/article_panel.py:24-65` (substituir `_section_card` por componente accordion).
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** uso de `rx.accordion.root` + `rx.accordion.item` (Reflex 0.9 — `https://reflex.dev/docs/library/disclosure/accordion`). `type="multiple"` no root (várias seções podem estar abertas simultaneamente). Cada item tem `value=str(section["index"])` para identificação.
  - **Integração:** `_section_card(section)` retorna um `rx.accordion.item` em vez de `rx.box`. O `rx.foreach(EnsaioState.current_article, _section_card)` passa a estar dentro de um `rx.accordion.root(...)`. Header colapsado: `rx.accordion.header` com `title + badge + chevron` via `rx.accordion.trigger`. Conteúdo expandido: `rx.accordion.content` com placeholder/markdown + botões.
  - **Template de referência:** documentação oficial do Reflex em `https://reflex.dev/docs/library/disclosure/accordion`. Componente análogo no projeto: estrutura atual de `_section_card` em `article_panel.py:24-65` (preservar lógica interna, trocar invólucro).
  - **Acoplamentos verificados:** edição inline (E-PROTO-2.3) usa `EnsaioState.editing_section_index` — é independente do estado de expansão. Toggle de expansão é interno ao Radix; não vaza para `EnsaioState`.
  - **Dependências de ordem:** independente das demais funcionalidades. Pode ser implementado por último.
  - **Escopo de teste:** validação manual (toggle por seção independente, edição funciona dentro da seção expandida, regenerar funciona, badge atualiza).

#### E-PROTO2-4.2 Estado inicial colapsado
- **Descrição:** Todas as seções iniciam colapsadas no primeiro render. Sem persistência de preferência de expansão (sessão descartável até MVP-ENSAIO).
- **Critérios de Aceite:**
  - No primeiro render após aceite da proposta de estrutura, todas as seções estão colapsadas
  - Recarregar a página volta tudo a colapsado (consistente com sessão descartável)
  - Estado de expansão vive local ao componente do painel — não polui `EnsaioState`
- **Detalhes de execução:**
  - **Arquivos a modificar:** `products/ensaio/app/components/article_panel.py` (mesma área de E-PROTO2-4.1; configuração do `default_value=[]` no accordion root).
  - **Arquivos a criar:** nenhum.
  - **Contratos/Shapes:** `rx.accordion.root(default_value=[], type="multiple", collapsible=True)` — array vazio significa nenhum item aberto.
  - **Integração:** parâmetro `default_value=[]` no construtor do accordion root. Estado de expansão é gerenciado internamente pelo componente Radix; não persiste em `EnsaioState` nem em localStorage.
  - **Template de referência:** documentação do Reflex já citada em 4.1.
  - **Acoplamentos verificados:** sessão é descartável (declarado em PROTO-ENSAIO-2 e na vision). Sem persistência é consistente com o estágio.
  - **Dependências de ordem:** depende de E-PROTO2-4.1.
  - **Escopo de teste:** validação manual (após aceite da estrutura, todas seções iniciam colapsadas; recarregar a página volta tudo a colapsado).

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
