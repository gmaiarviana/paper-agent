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
| ÉPICO 2 (Camada Compartilhada de Invocação de LLM) | 🌱 Visão | — (higiene técnica, não vinculado a produto) | — |
| ÉPICO 3 (Backend de Modelo Local nos Produtos/Core — OpenWebUI) | 🌱 Visão | — (não vinculado) | — |
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

#### ÉPICO 2: Camada Compartilhada de Invocação de LLM

**Objetivo:** Eliminar a duplicação do boilerplate de chamada a LLM espalhado pelos agentes do core. Hoje cada agente reimplementa `_get_llm` + `extract_json_from_llm_response` + `register_execution` + try/except (~13 cópias), bypassa a abstração de provider importando `ChatAnthropic` direto, e mascara erros com `except Exception:` genéricos. Consolidar numa única camada (`core/utils/llm_runner.py`) que encapsule provider selection, retry, parsing JSON, validação Pydantic e tracking de execução — tornando troca de modelo, mudança de provider e mudança de instrumentação um fix em um lugar só.

**Status:** 🌱 Visão

**Origem:** auditoria técnica em `claude/scan-core-technical-debt-zNlv2` (2026-04-28), recomendação prioritária. Detalhes técnicos e itens relacionados em [docs/backlog.md §G1](backlog.md#g1-higienização-da-camada-de-llm-core).

**Escopo provisório (a refinar):**
- Função `run_agent(agent_name, prompt, schema, config) -> (parsed, raw)` consumida por todos os nós que chamam LLM hoje.
- Restaurar `_detect_provider` como ponto único de seleção de cliente (parar de importar `ChatAnthropic` direto nos agentes).
- Hooks padronizados de logging/tracking que tornem `G1.2` (consolidação de logging) e `G1.3` (defaults YAML) cabíveis no mesmo épico ou em sequência imediata.

**Dependências:** nenhuma (refator interno do core).

**Sinergia com ÉPICO 3:** a abstração de provider definida aqui é o ponto natural pra adicionar OpenWebUI/Ollama como provider alternativo. Refinar este épico antes do ÉPICO 3 reduz custo do segundo (ÉPICO 3 vira "adicionar provider novo" em vez de "abstrair + adicionar").

**Próximos Passos:**
- Sessão de refinamento para definir contrato exato de `run_agent`, estratégia de migração agente-a-agente e critério de "feito".
- Decidir se G1.2 (logging) e G1.3 (YAML defaults) entram no mesmo épico ou ficam em épicos separados subsequentes.

---

#### ÉPICO 3: Backend de Modelo Local nos Produtos/Core (OpenWebUI / Ollama)

**Escopo:** este épico é sobre o **runtime dos produtos e agentes do core do Paper Agent** — Writer, Estruturador, Metodologista e os apps Ensaio/Revelar passarem a chamar modelos locais servidos pelo OpenWebUI da Atlântico (`chat.alia.atlantico.com.br/api`) em vez da API Anthropic direta. **Não cobre** o uso do Claude Code CLI contra OpenWebUI — esse caminho é tooling de desenvolvimento e está tratado em [`docs/process/workflow/ROADMAP.md`](process/workflow/ROADMAP.md).

**Objetivo:** trocar o provedor de modelo dos agentes/produtos sem regressão funcional. Convivência com o backend Anthropic continua sendo requisito (CI, fallback, ambientes sem infra local).

**Status:** 🌱 Visão

**Dependência preferencial:** ÉPICO 2 (Camada Compartilhada de Invocação de LLM). Se a camada compartilhada já existir, este épico vira "adicionar provider OpenWebUI à camada"; se não, este épico carrega o custo da abstração junto.

**Motivação:**
- Soberania de modelo: produtos rodando contra infra Atlântico, sem chave Anthropic individual por dev.
- Tentativa anterior em `products/ensaio/` (2026-04-28) chegou a apontar `ANTHROPIC_BASE_URL` pro proxy LiteLLM local — abriu app mas as chamadas falharam, sem decisão arquitetural firme. Esta entrada captura o que já se sabe pra próxima tentativa não tropeçar igual.

**Certezas:**
- Env vars `OPENWEBUI_API_KEY` e `OPENWEBUI_BASE_URL` já existem.
- Modelos disponíveis hoje no backend: `ollama/ministral-3:14b` e `ollama/llama3.2:3b`. Modelos maiores (30B+) ainda não confirmados — vale checar com a Atlântico.
- Params Anthropic-only (`context_management`, `cache_control`, `thinking`, `anthropic_beta`) precisam ser dropados quando o backend é OpenAI-compatible.
- Tool calling em `ollama/ministral-3:14b` funciona — validado em formato OpenAI cru e via proxy LiteLLM em formato Anthropic (debug ponta-a-ponta, 2026-04-28).
- `validate_writer` rodou com `LLM_MODEL=ollama/llama3.2:3b` via proxy gerando artigo IMRaD coerente — prova empírica de que o caminho "Anthropic SDK + proxy + Ollama" é viável sem refator dos agentes (commit `14bf827` no `litellm-config.yaml` adicionou os aliases necessários).

**Decisão arquitetural a tomar no refinamento — proxy LiteLLM vs. cliente OpenAI direto:**
- *Cliente OpenAI direto:* sem processo extra rodando, sem hops de tradução, sem versão de LiteLLM pinada, controle total sobre payloads. Custo: refator de `core/` pra abstrair provider (resolvido pelo ÉPICO 2 se ele preceder).
- *Proxy LiteLLM:* zero refator nos agentes (`ChatAnthropic` continua funcionando), troca de provider sem mexer em `core/`, observabilidade centralizada. Custo: dependência runtime do proxy, manutenção de aliases no yaml.

**Lacunas que ainda exigem medição:**
- Qualidade dos modelos locais nos agentes específicos (Writer, Estruturador, Metodologista) — testado apenas no Writer até aqui.
- Perda de features Anthropic-only dropadas (`cache_control`, `thinking`) na qualidade percebida.
- Comportamento de `core/utils/cost_tracker.py` com nomes de modelo não-Anthropic.
- Piso de qualidade por agente: quais aceitam Ollama local sem regressão e quais ainda exigem Sonnet/Opus.

**Não autorizado neste épico:**
- Remover suporte ao backend Anthropic direto.

**Próximos Passos:**
- Sessão de refinamento para escolher caminho técnico (idealmente após o ÉPICO 2).
- Smoke tests por agente contra cada modelo disponível, registrando onde tool calling/JSON mode regride.

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
