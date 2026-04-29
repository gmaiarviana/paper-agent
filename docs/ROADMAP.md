# ROADMAP - Core Universal

Épicos e melhorias do sistema core que serve todos os produtos.

> **📖 Status Atual:** Para entender o estado atual do core, consulte [ARCHITECTURE.md](ARCHITECTURE.md) e [core/docs/](../core/docs/).

> **📖 Visão:** Para entender a filosofia do sistema, consulte [core/docs/vision/system_philosophy.md](../core/docs/vision/system_philosophy.md).

> **🧭 Estados dos épicos:** ver [planning_guidelines.md](process/refinement/planning_guidelines.md) para definições completas.

> **Retroatividade:** épicos concluídos antes da introdução do modelo de estados permanecem em formato simplificado (título ✅ + 1-2 linhas de resumo) e não são reclassificados retroativamente. O modelo aplica-se a épicos em andamento e futuros.

---

## 🎯 Épicos Core × Milestones de Produto

> **Nota:** O core não tem milestones próprios — seus épicos são consumidos pelos milestones dos produtos. Épicos motivados por produto (prefixo `C-<PRODUTO>-`) declaram aqui qual milestone de produto os consome, para que o dispatch do milestone saiba que precisa tê-los implementados como dependência. Convenção de id de milestone em [docs/CONSTITUTION.md §9](CONSTITUTION.md).

| Épico Core | Status | Milestone consumidor | Produto |
|------------|--------|----------------------|---------|
| ÉPICO 1 (Pesquisador) | 🌱 Visão | — (não vinculado) | — |
| ÉPICO 2 (Backend de Modelo Local nos Produtos/Core — OpenWebUI) | 🌱 Visão | — (não vinculado) | — |
| C-ENSAIO-1 (Parametrização de Contexto) | 🌱 Visão | POC-ENSAIO | Ensaio |
| C-ENSAIO-2 (Writer versão inicial) | ✅ Implementado | POC-ENSAIO | Ensaio |
| C-ENSAIO-3 (Writer por seção) | ✅ Implementado | PROTO-ENSAIO | Ensaio |
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

#### ÉPICO 2: Backend de Modelo Local nos Produtos/Core (OpenWebUI / Ollama)

**Escopo:** este épico é sobre o **runtime dos produtos e agentes do core do Paper Agent** — Writer, Estruturador, Metodologista e os apps Ensaio/Revelar passarem a chamar modelos locais servidos pelo OpenWebUI da Atlântico (`chat.alia.atlantico.com.br/api`) em vez da API Anthropic direta. **Não cobre** o uso do Claude Code CLI contra OpenWebUI — esse caminho é tooling de desenvolvimento e está tratado em [`docs/process/workflow/ROADMAP.md`](process/workflow/ROADMAP.md).

**Objetivo:** trocar o provedor de modelo dos agentes/produtos sem regressão funcional. Convivência com o backend Anthropic continua sendo requisito (CI, fallback, ambientes sem infra local).

**Status:** 🌱 Visão

**Motivação:**
- Soberania de modelo: produtos rodando contra infra Atlântico, sem chave Anthropic individual por dev.
- Tentativa anterior em `products/ensaio/` (2026-04-28) chegou a apontar `ANTHROPIC_BASE_URL` pro proxy LiteLLM local — abriu app mas as chamadas falharam, sem decisão arquitetural firme. Esta entrada captura o que já se sabe pra próxima tentativa não tropeçar igual.

**Certezas iniciais:**
- Env vars `OPENWEBUI_API_KEY` e `OPENWEBUI_BASE_URL` já existem.
- Modelos disponíveis hoje no backend: `ollama/ministral-3:14b` (default texto/instruções) e `ollama/llama3.2:3b` (rápido, leve).
- Params Anthropic-only (`context_management`, `cache_control`, `thinking`, `anthropic_beta`) precisam ser dropados quando o backend é OpenAI-compatible.

**Evidências empíricas (2026-04-28):**
- ✅ **Tool calling no `ollama/ministral-3:14b` em formato OpenAI cru funciona.** Teste batendo direto em `OPENWEBUI_BASE_URL/chat/completions` com 2 tools (`get_local_status`, `get_current_time_by_utc_offset`) — modelo escolheu a tool correta, montou args válidos, recebeu o tool result no histórico e gerou resposta final coerente. Invalida a hipótese inicial de que Ollama small models não suportariam tool calling.
- ✅ **Tool calling via proxy LiteLLM em formato Anthropic também é preservado** — debug Copilot ponta-a-ponta em 2026-04-28 mostrou `tools` chegando intacto nas 4 etapas do pipeline (pré-call → tradução Anthropic→OpenAI → POST outbound → resposta convertida de volta como `tool_use`). Cliente recebe `content=[ToolUseBlock(...)]` corretamente em casos simples (1 tool, prompt direto).
- ✅ **`validate_writer` passa ponta-a-ponta com `LLM_MODEL=ollama/llama3.2:3b` via proxy** (2026-04-28, após fix de aliases no `litellm-config.yaml` em commit `14bf827`). Writer node gerou artigo IMRaD coerente (~2.1k chars) com marcadores esperados. Prova empírica de que o caminho "Anthropic SDK (`ChatAnthropic`) + proxy + Ollama" é viável sem refator dos agentes.
- ⚠️ **Errata sobre evidência anterior:** um probe inicial (Anthropic SDK + tools=[ask_user] + pergunta vaga sem system prompt) retornou `blocks=['text']` e foi registrado como "proxy não preserva tool calling". Releitura indica que foi **falso negativo** por design fraco do probe — pergunta vaga + tool meta + sem nudge fizeram o modelo escolher texto. O proxy não estava quebrado; o modelo só optou por não usar a tool.

**Implicação arquitetural revisada:** o caminho "Anthropic SDK + proxy LiteLLM" **continua viável** em termos de fidelidade técnica de tool calling. A escolha entre proxy vs. cliente OpenAI-compatible direto vira decisão de **arquitetura/dependência**, não de capacidade técnica:
- *A favor do cliente OpenAI direto:* sem dependência de processo extra rodando, sem hops de tradução, sem versão de LiteLLM pinada, controle total sobre payloads.
- *A favor do proxy:* zero refator no código atual dos agentes (`ChatAnthropic` continua funcionando), troca de provider sem mexer em `core/`, observabilidade centralizada de chamadas LLM.
- *Variáveis ainda não medidas:* qualidade dos modelos locais para os agentes específicos (Writer, Estruturador, Metodologista) e perda de features Anthropic-only dropadas (`cache_control`, `thinking`, `anthropic_beta`).

**Lacunas que ainda exigem prova empírica:**
- JSON estruturado / output determinístico em `ollama/ministral-3:14b` para Writer e Estruturador.
- Comportamento dos agentes que dependem de prompt caching e thinking (perda de qualidade ainda não medida).
- Se há flag/versão do LiteLLM que preserve tool calling na tradução Anthropic→OpenAI (descartar definitivamente o caminho do proxy só depois disso).

**Decisões a tomar no refinamento:**
- Escolher entre **cliente OpenAI direto + abstração de provider** vs. **manter Anthropic SDK + apontar pro proxy LiteLLM**. Decisão agora é trade-off real, não forçada por bug.
- Onde mora o switch: `LLM_MODEL` puro ou abstração explícita em `core/utils/config.py` / camada de provider.
- Como `langchain_anthropic` (usado pelo Writer hoje) convive com a escolha: se for proxy, continua intocado; se for cliente direto, vira parte do refator.
- `core/utils/cost_tracker.py` precisa lidar com nomes de modelo não-Anthropic sem explodir.
- Piso de qualidade por agente: quais aceitam Ollama local sem regressão e quais ainda exigem Sonnet/Opus.

**Não autorizado neste épico:**
- Remover suporte ao backend Anthropic direto.
- Mexer em `infra/litellm-proxy/` (essa pasta é dev tooling do Claude Code CLI; ver workflow ROADMAP).

**Próximos Passos:**
- Sessão de refinamento para fechar a abstração de provider.
- Smoke tests por agente do core contra cada modelo disponível, registrando onde tool calling/JSON mode quebra.

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

#### ÉPICO C-ENSAIO-3: Writer Gera por Seção (Evolução) ✅

**Status:** ✅ Implementado — PR #97 (merge `1d592d0`, 2026-04-27)

**Entregue:** Contrato `Article = list[Section]` com `Section = TypedDict{title, body, status: empty|draft|edited}` em `core/agents/writer/models.py`, e nó stateless `writer_section_node` em `core/agents/writer/nodes.py` que gera/regenera o corpo de uma seção individual recebendo `{messages, focal_argument, section_title, current_body, article_context, product_context}` e devolvendo `{section_content}`. `writer_node` original preservado sem mudança (não-regressão).

**Decisões permanentes:** ver [core/docs/agents/writer/design.md](../core/docs/agents/writer/design.md) (modos de invocação: artigo inteiro vs. por seção; seleção pelo produto consumidor).

**Referências:** `core/agents/writer/models.py`, `core/agents/writer/nodes.py` (`writer_section_node`), `tests/core/unit/agents/test_writer_section_node.py`.

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

**Regra:** fluxo manual exige épico em `📋 Critérios definidos`; fluxo autônomo exige `🔍 Detalhes definidos`.

> Para o processo completo de refinamento, consulte [planning_guidelines.md](process/refinement/planning_guidelines.md). Para a prontidão ao fluxo autônomo (alvo `🔍`), consulte [autonomous_readiness.md](process/refinement/autonomous_readiness.md). Para o fechamento do épico (saída), consulte [epic_completion.md](process/refinement/epic_completion.md).

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos em `🌱 Visão` ou `📐 Funcionalidades esboçadas` passam por sessão de refinamento antes da implementação
