# BACKLOG - Paper Agent

## 📍 MÉDIO PRAZO

Melhorias importantes que expandem capacidades essenciais do sistema.

---

### Estruturador como Sub-Grafo
Transformar Estruturador de função simples para agente complexo com reasoning loop.

- Sub-grafo com 3 nós: `analyze_input` → `ask_context` → `structure_question`
- Tool `ask_user` para clarificações (similar ao Metodologista)
- Reasoning loop (pergunta até ter contexto suficiente)
- Estado próprio: `StructurerState` (TypedDict)
- Limite de iterações (max 3 perguntas)

---


## 🔜 PRÓXIMOS PASSOS

Funcionalidades técnicas que melhoram qualidade e manutenibilidade.

---

### ProgressTracker (Frontend - Interface Web)
Checklist adaptativo com status em tempo real no painel Contexto.

**Status:** Backend já implementado em `core/agents/checklist/progress_tracker.py` com `ProgressTracker.evaluate()`.

**Pendente (Frontend):**
- Componente renderiza checklist no painel Contexto (borda direita, flutuante/fixo)
- Atualiza em tempo real conforme cognitive_model evolui
- Mostra itens: ⚪ pendente, 🟡 em progresso, 🟢 completo
- Sincronização via polling ou SSE (conforme infraestrutura disponível)

**Contexto:** Originalmente planejado no Épico 9, mas movido para backlog devido à complexidade de expor cognitive_model em tempo real. Indicador de Solidez (9.4) resolve 80% do valor com 20% do esforço. ProgressTracker completo será implementado quando infraestrutura de eventos estiver madura.

**Referência técnica:** Ver `core/agents/checklist/progress_tracker.py` (backend já implementado) e `products/revelar/docs/interface/components.md` seção 3.6 (especificação completa da UI).

### RAG Infrastructure - Metodologista Knowledge Base
Metodologista consulta knowledge base via RAG ao invés de arquivo `.md` estático.

**Nota:** A infraestrutura base do ChromaDB será implementada no ÉPICO 10 (Observador) para catálogo de conceitos. Esta funcionalidade aproveitará essa infraestrutura para uso específico do Metodologista.

- Setup ChromaDB (vector store local, gratuito) - aproveitar infraestrutura do ÉPICO 10
- Tool `consult_methodology(query)` com busca semântica
- Popular KB inicial com `core/docs/agents/methodologist/knowledge.md`
- Integrar tool no grafo do Metodologista
- Embeddings: sentence-transformers (all-MiniLM-L6-v2) - mesmo modelo do ÉPICO 10
- CLI para gerenciar KB: `python -m core.tools.cli.kb_manager add/search/stats`

---


### Cost Controller (Budget Control)
Budget por sessão para evitar gastos inesperados.

**Status:** Cálculo de custos já implementado (`core/utils/cost_tracker.py`, `core/agents/memory/execution_tracker.py`). Métricas de custo já aparecem no dashboard.

**Pendente:**
- Budget configurável por sessão (default: $1, max: $10)
- Stop automático ao exceder budget
- Warning ao atingir 80% do budget
- Config em `.env`: `MAX_COST_PER_SESSION=1.0`
- Budget detalhado por tipo de artigo, alertas preventivos baseados em histórico

---

### Agent Development Kit
Documentação, templates e patterns para criar novos agentes.

- Documentação completa: `core/docs/agents/creating_new_agents.md`
- Template base comentado: `core/agents/_template/` (copiar e adaptar)
- Exemplos de referência: Metodologista (complexo), Estruturador (simples)
- Checklist de implementação completa
- Patterns comuns documentados: reasoning loop, tools, conditional routing
- Helpers opcionais para boilerplate (TypedDict, graph setup básico)

---

### Métricas Discretas (UX Polish)
Reduzir ruído visual escondendo métricas por padrão, mostrando sob demanda.

- Substituir `st.caption` inline por ícone (ℹ️) clicável
- `st.popover` com métricas ao clicar: "💰 R$ 0,02 · 215 tokens · 1.2s"
- Aplicar em: chat_history, backstage, dashboard
- Fallback: `st.expander` se `st.popover` não disponível

**Contexto:** Originalmente Épico 5.1, movido para backlog para simplificar escopo. Intenção: interface mais limpa e elegante, sem métricas sempre visíveis.

---

### Crítico
Agente para revisão final do artigo (essencial para garantir qualidade).

- Revisão final de rigor científico e coerência
- Identificação de contradições ou gaps argumentativos
- Validação de integridade do argumento completo
- Sugestões de melhorias de redação e clareza

---

### Gestão Avançada de Tópicos
Ferramentas para gerenciar múltiplos tópicos em progresso (essencial para fluxo real de trabalho).

- Arquivar tópicos concluídos
- Busca por tópicos (título, tipo, stage)
- Tags/labels customizáveis
- Estatísticas (tópicos por tipo, tempo médio por stage)

---

## 🌙 LONGO PRAZO (FUTURO DISTANTE)

Funcionalidades desejáveis mas não essenciais para MVP.

---

### SSE (Server-Sent Events) para Interface Web
Otimização de performance para streaming de eventos em tempo real na interface web.

- Implementar endpoint SSE: `/events/<session_id>` (FastAPI separado)
- Interface consome eventos via `EventSource` API (JavaScript)
- Substituir polling por SSE (elimina delay de 1s)
- **Indicador de novidade nos bastidores**: Mostrar indicador sutil (🔴 ou "(+2)") no header "📊 Bastidores" quando há atualização, desaparecendo quando usuário expande (requer SSE/WebSocket para eventos em tempo real)
- Fallback automático para polling se SSE falhar
- Reconnect automático em caso de desconexão
- Deploy: 2 processos (Streamlit :8501 + FastAPI :8000)

**Contexto:** Funcionalidade planejada originalmente para MVP do Épico 9, mas movida para Backlog. Sistema já funciona bem com polling (1s), SSE é otimização adicional quando/se delay se tornar problema na prática.

---

### Personas de Agentes
Permitir customização de agentes como "personas" (Sócrates, Aristóteles, Popper) com estilos de argumentação personalizados.

- Transformar agentes em "mentores" que usuário pode escolher
- Estilos de argumentação personalizados por persona
- Treinar personas com feedback do usuário

**Contexto:** Funcionalidade planejada originalmente como Épico 18, movida para Backlog por não ser essencial para MVP. Ver `products/produtor-cientifico/docs/vision/agent_personas.md`.

---

### Agentes em Paralelo (LangGraph Parallel Branches)
Permitir que múltiplos agentes trabalhem simultaneamente quando análises são independentes.

- Implementar parallel branches no LangGraph
- Exemplo: Estruturador e Metodologista analisam ao mesmo tempo
- Orquestrador sintetiza resultados de múltiplos agentes
- Reduz latência em fluxos complexos
- Requer: análise de dependências entre agentes

**Contexto:** Identificado durante refinamento do Épico 1 (Convergência Orgânica). Sistema atual usa fluxo sequencial que atende 95% dos casos. Paralelo é otimização para quando latência se tornar problema.

---

### Mediação de Divergências entre Agentes
Orquestrador media quando agentes têm opiniões conflitantes sobre mesmo input.

- Detectar divergências automáticamente (Metodologista rejeita, Estruturador aprova)
- Apresentar perspectivas lado a lado nos bastidores
- Orquestrador sintetiza: "Há perspectivas diferentes sobre isso..."
- Usuário tem contexto para decidir direção
- Requer: sistema de votação ou consenso entre agentes

**Contexto:** Identificado durante refinamento do Épico 1. Atualmente agentes trabalham em sequência e não divergem. Mediação será necessária quando sistema tiver mais agentes com opiniões independentes.

---

### Alertas de Custo
Avisos automáticos para evitar surpresas com gastos de API.

**Status:** Métricas de custo já implementadas (Épico 8.3). Dashboard já mostra custos acumulados por sessão.

**Pendente:**
- Alertas em tempo real na interface web
- Dashboard com histórico de gastos (últimos 30 dias)
- Ver também: "Cost Controller (Budget Control)" acima para funcionalidades de budget

**Contexto:** Funcionalidade planejada originalmente para MVP do Épico 8, mas movida para Backlog. Sistema já tem métricas consolidadas (Épico 8.3), alertas são otimização adicional.

---

### Session Replay (Debug)
Reproduzir sessões passo a passo para debugging avançado.

- Gravar todas interações (estado antes/depois, LLM calls, decisões)
- Storage: JSONL file por sessão em `runtime/recordings/`
- CLI: `python -m core.tools.cli.replay_session session-123`
- Breakpoints interativos (pause em nó específico)
- Step-by-step execution com inspeção de estado

---

### Export de Reasoning e Estatísticas
Exportar histórico completo de reasoning e estatísticas agregadas para análise offline.

- Export de histórico completo de reasoning (JSON, markdown)
- Estatísticas agregadas por sessão:
  - Agente mais usado
  - Custo total por tipo de agente
  - Distribuição de tokens (input vs output)
  - Tempo médio por agente
- Dados exportáveis para análise offline
- Visualização básica de padrões (opcional: gráficos com Plotly)
- Botão de export no Dashboard

**Contexto:** Funcionalidade planejada originalmente para MVP do Épico 8, mas movida para Backlog. Sistema já tem métricas consolidadas (Épico 8.3), export é funcionalidade adicional para análise avançada.

---

### Handling de Contexto Longo
Truncamento inteligente quando histórico exceder limite de contexto.

- Detectar quando histórico + input ultrapassa limite do modelo
- Estratégias de truncamento:
  - Manter argumento focal + últimos N turnos
  - Resumir turnos antigos via LLM
  - Priorizar turnos com decisões importantes
- Reconexão transparente (usuário não percebe truncamento)

---

### Provocação de Reflexão Avançada (RAG)
Versão avançada da provocação de reflexão usando RAG e análise de padrões.

- RAG para sugerir ângulos baseado em papers científicos
- Análise de vieses cognitivos recorrentes do usuário
- Adaptação de tom/frequência ao estilo do usuário
- Requer: RAG Infrastructure + Épico 10 (persistência)

**Nota:** Versão simples já implementada no Épico 7 MVP (análise via LLM do histórico atual).

---

### Migração para Banco de Dados
Avaliar migração de SqliteSaver para PostgreSQL quando escalar.

- Avaliar PostgreSQL vs SqliteSaver para produção
- Considerar replicação/backup de tópicos
- Performance: índices, queries otimizadas

---

### Exportação de Artefatos
Gerar documentos finais em múltiplos formatos.

- Gerar PDF/Word/LaTeX do artigo final
- Exportar outline, pesquisas, decisões separadamente
- Templates formatados por tipo de artigo

---

### Versionamento Completo
Sistema git-like para artefatos.

- Git-like para artefatos (diff, merge, rollback)
- Histórico de decisões do Orquestrador
- Timeline visual de evolução

---

### Reset Parcial por Agente
Limpar memória de um agente específico sem encerrar sessão.

- Permitir limpar memória de um agente específico
- Garantir que outros agentes mantenham histórico e referências consistentes

---

### Log de Parecer Individual no Debate
Registrar argumentos completos de cada agente.

- Registrar argumentos completos de cada agente antes do voto de minerva
- Disponibilizar comparação lado a lado na interface e export JSON

---

### Depuração Interativa
Ferramentas avançadas de debugging.

- Pausar execução e inspecionar `MultiAgentState`
- Métricas de performance por agente (tempo, tokens, custo, iterações)

---

### Estrutura de Projeto (src layout)
Migrar para estrutura de projeto padrão Python.

- Migrar para `src/paper_agent/` com `pyproject.toml`
- Remover hacks de `sys.path` via `pip install -e .`
- Facilita distribuição e testes isolados

---

### Consolidação de Configuração
Centralizar configurações em pyproject.toml.

- Migrar `pytest.ini` para `pyproject.toml`
- Centralizar configs de ferramentas (black, ruff, mypy)

---

### Dependency Management
Melhorar gestão de dependências.

- Avaliar migração para `pyproject.toml` + pip-tools/poetry
- Lock de versões para builds reproduzíveis

---

### Infraestrutura Avançada
RAG e persistência de longo prazo.

- RAG e Vector Database para memória de longo prazo entre artigos
- Persistência avançada em banco de dados relacional
- Sistema de versionamento de artigos (branches, merge, rollback)
- Cache inteligente de pesquisas e validações

---

### Integração e Colaboração
Sistema multi-usuário e integrações externas.

- Integração com gestores de referências (Zotero, Mendeley)
- Sistema multi-usuário com autenticação
- Compartilhamento e colaboração em tempo real
- Comentários e feedback inline

---

### Analytics e Melhorias
Dashboard de métricas e otimização contínua.

- Dashboard de métricas consolidadas (tokens, custos, tempo) com histórico temporal (últimos 7/30 dias)
- Análise de padrões de uso (quais agentes mais usados, prompts mais eficientes)
- Comparação entre sessões (métricas agregadas ao longo do tempo)
- Análise de qualidade de artigos gerados
- Sugestões automáticas de melhoria baseadas em patterns
- A/B testing de prompts de agentes

---

### Comparison Tool (Testes)
Comparar antes/depois de mudanças no prompt para detectar regressões.

- Implementar `compare_results()` em `core/utils/result_comparer.py`
- Implementar `detect_regressions()` para identificar regressões automaticamente
- Implementar `compare_results.py` com CLI
- Output deve incluir resumo de mudanças e lista de cenários que precisam atenção

---

### Exportação e Formatação Avançada
Suporte a múltiplos formatos e publicação.

- Múltiplos formatos de saída (PDF, LaTeX, Word, Markdown)
- Templates de revistas científicas específicas
- Submissão automática para repositórios de preprints (arXiv, bioRxiv)
- Geração de apresentações (slides) a partir do artigo

---

### Melhorias de Interface Web
Funcionalidades desejáveis para aprimorar experiência do usuário na interface web.

- Mobile responsivo (bastidores como modal/overlay)
- Export de conversas (markdown, PDF)
- Replay de sessão (ver conversa + reasoning passo a passo)
- Temas (claro/escuro)
- Atalhos de teclado

**Contexto:** Melhorias planejadas para o Épico 9 (Interface Web Conversacional), mas movidas para Backlog como funcionalidades não essenciais para MVP.

---

### Utilitários de Composição de Grafos Produto-Específicos
Quando o super-sistema tiver 2-3 produtos com grafos próprios (Ensaio + Produtor Científico + um terceiro), avaliar extração de utilitários comuns de composição para `core/agents/graph_builders/` (ou nome equivalente). Até lá, cada produto compõe manualmente em `products/<produto>/app/graph.py`.

**Origem:** decisão arquitetural em `docs/ARCHITECTURE.md` (composição de grafo por produto).

---

## 🛠️ Débito Técnico — Auditoria 2026-04-28

> **Origem:** varredura de `core/` e `products/ensaio/` em `claude/scan-core-technical-debt-zNlv2`. Itens curtos sem decisão já foram resolvidos no próprio branch (commits `979122f`..`12e9d75`). Os itens abaixo foram dimensionados mas não executados — exigem refator maior, decisão arquitetural ou janela de produto.
>
> **Análise anterior:** ver `docs/analysis/debitos_tecnicos.md` (2025-01) para registro histórico.
>
> **Tamanhos:** S = 1 PR pequeno (≤ 1 dia), M = 2-5 dias, L = épico (≥ 1 semana, exige refinamento).

---

### G1. Higienização da camada de LLM (core)

**Contexto:** o boilerplate de invocar LLM (`_get_llm` + `extract_json` + `register_execution` + try/except) está copiado ~13 vezes; a abstração de provider está bypassada (todos importam `ChatAnthropic` direto); três sistemas de logging convivem sem hierarquia. Pagar essa dívida desbloqueia trocar de modelo num lugar só, restaura provider abstraction e simplifica futuras integrações.

**Promovido a 🌱 Épico em `docs/ROADMAP.md` (ÉPICO 2)** — exige refinamento antes de implementar.

- **G1.1 — `core/utils/llm_runner.py`** [L, prioridade alta] — extrair `run_agent(agent_name, prompt, schema, config) -> (parsed, raw)` que encapsule provider selection, retry, parsing JSON, validação Pydantic e `register_execution`. Elimina ~13 cópias do boilerplate (`orchestrator/nodes.py:814`, `methodologist/nodes.py:105,289,453,474`, `structurer/nodes.py:281,481`, `observer/metrics.py:168,263,445`, `observer/clarification.py:197,304,399,600`, `persistence/snapshot_manager.py:172`).
- **G1.2 — Consolidar logging/observabilidade** [M] — `core/utils/structured_logger.py` + `debug_analyzer.py` + `debug_reporter.py` + `event_bus/publishers.py` (527 ln) + `cost_tracker.py` se sobrepõem. Decidir: `structured_logger` é a camada base e os outros são consumidores? Documentar e consolidar duplicações.
- **G1.3 — `core/config/agents/defaults.yaml` + override** [S] — `methodologist.yaml:63-74`, `structurer.yaml:61-72`, `observer.yaml:26-58`, `writer.yaml:42-53`, `orchestrator.yaml:24-37` repetem `context_limits` e `metadata`. Extrair defaults e deixar cada agente sobrescrever só o que difere.

**Ordem sugerida:** G1.1 → G1.3 (independentes; G1.2 entra junto se o llm_runner expor hooks de log).

---

### G2. Fronteira produto ↔ core

**Contexto:** o produto Ensaio reimplementa peças que vão ser necessárias no Produtor Científico (próximo produto) — sqlite checkpointer, mapeamento agent→label, lógica de mensagem/artigo. Pagar antes de PROTO-ENSAIO-2 evita amplificar a duplicação no próximo milestone.

- **G2.1 — `core/agents/persistence/sqlite_checkpointer.py`** [S] — extrair factory parametrizada por nome de DB. Hoje duplicado em `products/ensaio/app/graph.py:35-89` ↔ `core/agents/multi_agent_graph.py:450-476`.
- **G2.2 — `core/agents/labels.py`** [S] — mapeamento `agent → (emoji, label)` hoje em 3 cópias: `products/ensaio/app/state.py:24-30` (não-consumida), `products/ensaio/app/components/chat_panel.py:19-26`, `chat_panel.py:60-65`. Outros produtos vão precisar do mesmo.
- **G2.3 — Mover lógica de domínio do `EnsaioState` para `core/agents/writer/`** [M] — `_deserialize_messages` e `_build_article_context` (`products/ensaio/app/state.py:41-61`) são utilitários puros sem nada de Reflex. A regra "aceitar `article_sections` só quando artigo está vazio" (`state.py:159-173`) também é domínio. Hoje a "UI burra" prometida na vision §7 está vazada.

**Ordem sugerida:** G2.2 → G2.1 → G2.3 (do mais barato ao que mais paga juros).

---

### G3. Disciplina interna do core

**Contexto:** itens que exigem decisão arquitetural própria. Não juntar em épico único — cada um pede RFC/ADR curto.

- **G3.1 — Quebrar god functions** [M, incremental] — `core/agents/orchestrator/nodes.py` (1067 ln, `_build_context` ~100 ln), `core/agents/multi_agent_graph.py` (650 ln), `core/agents/observer/extractors.py` (860 ln). Refator gradual: cada vez que tocar o arquivo por outra razão, extrair 1-2 funções.
- **G3.2 — Decidir local único de prompts** [S, exige decisão] — hoje `core/prompts/*.py` coexiste com `core/agents/observer/prompts.py` (555 ln) e `core/agents/observer/clarification_prompts.py` (322 ln) sem critério. Decisão: tudo em `core/prompts/<agente>.py`, ou tudo em `core/agents/<agente>/prompts.py`?
- **G3.3 — Status de `writer`/`researcher`/`communicator`/`memory_agent`** [M, exige decisão] — `core/agents/writer/` existe mas não está cabeado em `multi_agent_graph.py`; `core/docs/agents/{researcher,communicator,memory_agent}/responsibilities.md` documentam agentes sem código. Decidir, por agente: implementar de fato, virar épico em `📐 Funcionalidades esboçadas` ou arquivar a doc.

---

### G4. Higiene do Ensaio (pós PROTO-ENSAIO-2)

**Contexto:** qualidade interna do produto. Faz sentido **depois** de PROTO-ENSAIO-2, porque a UI vai mexer e G4.1 pode mudar de forma.

- **G4.1 — Componentes UI genéricos** [M] — `products/ensaio/app/components/article_panel.py` e `chat_panel.py` referenciam `EnsaioState` direto (`article_panel.py:53,84,100`; `chat_panel.py:55,93,117`). Quando Produtor Científico chegar, terão de duplicar ou parametrizar. Esperar PROTO-ENSAIO-2 para ver a forma final.
- **G4.2 — Cobertura de testes do `EnsaioState`** [M] — `tests/products/ensaio/unit/` tem 2 arquivos. Zero cobertura para `state.py` (329 ln, async crítico), `_invoke_graph`, `_invoke_writer_section`, componentes Reflex.
- **G4.3 — `pyproject.toml` no Ensaio + remover `sys.path` hacks** [S] — `app/app.py:16-18` e `rxconfig.py:7-9` injetam raiz do projeto em runtime; `requirements.txt` tem 1 linha (`reflex==0.9.0`) e herda dependências da raiz. Migrar para instalação editável resolve ambos. Ver também `Estrutura de Projeto (src layout)` mais acima — pode subir no mesmo PR.

---

## 🛠️ Débito Técnico — Sessão de debug do chat Ensaio (2026-06-18)

> **Origem:** investigação do "chat trava no Windows" (resolvido na PR #125, branch `fix/ensaio-windows-chat-hang` — causa-raiz: `StructuredLogger` gravava `.jsonl` dentro da árvore observada pelo `reflex run`, disparando hot-reload que remontava a página). Dois itens surgiram no diagnóstico e ficaram **fora** do PR (escopo + decisão). Tamanhos: S/M/L como na auditoria de 2026-04-28.

---

### D1. Modelo descontinuado hardcoded (nada pode ficar hardcoded)

**Contexto:** `claude-3-5-haiku-20241022` (descontinuado pela Anthropic → **404**) está fixo em 6 lugares: `core/utils/config.py:25` (`DEFAULT_MODEL`) e os 5 YAMLs `core/config/agents/{orchestrator,structurer,methodologist,observer,writer}.yaml`. Hoje não quebra porque `get_agent_model`/`get_default_model` dão precedência a `ANTHROPIC_MODEL` do `.env` (`claude-haiku-4-5-20251001`); mas se o `.env` não carregar (clone novo, CI, var ausente) o fallback é um 404 críptico — foi exatamente a causa dos erros 404 vistos em logs antigos do Ensaio durante o debug.

- **D1.1 — Eliminar o nome de modelo hardcoded** [S, prioridade alta] — trocar as 6 ocorrências por um modelo atual válido **ou**, melhor, por fonte única resolvida em runtime, de modo que o *fallback* também seja seguro. Idealmente nenhum nome de modelo fica escrito fixo em mais de um lugar. Relacionado a **G1.1** ("trocar de modelo num lugar só") e **G1.3** (defaults dos YAMLs); pode ser pago antes do épico G1 como fix de segurança isolado.

---

### D2. Observabilidade do runtime de agentes (debug-ability)

**Contexto:** durante o hang, o log estruturado tinha **apenas** `agent_started` — sem modelo resolvido, sem fim, sem erro — o que tornou o diagnóstico caro (um hang ficou indistinguível de chamada lenta ou erro silencioso). O timeout leve (`asyncio.wait_for`, 45s) e a superfície de erro/timeout na UI **já entraram** na PR #125; o restante da instrumentação foi revertido por causar ruído/loop.

- **D2.1 — Instrumentar a chamada LLM** [S/M] — logar o **modelo resolvido** na hora da chamada; emitir `llm_call_start`/`llm_call_end` com duração; garantir que **sempre** saia `agent_completed` **ou** `agent_failed` (não só `agent_started`). Objetivo: próximo travamento vira diagnóstico de 2 min, não de horas. Relacionado a **G1.2** (consolidação de logging) — entra naturalmente junto se o `llm_runner` de **G1.1** expor hooks de log.

---

**Versão:** 1.0  
**Data:** 2025-11-14

