# ROADMAP - Paper Agent

## 📋 Status dos Épicos

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 5: Interface Conversacional e Transparência
- ÉPICO 6: Memória Dinâmica e Contexto por Agente

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 7: Modelo de Dados e Persistência Durável
- ÉPICO 8: Pipeline Completo Ideia → Artigo
- ÉPICO 9: Debate Multi-Agente Mediado

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## ✅ ÉPICOS CONCLUÍDOS

**ÉPICO 4: Loop Colaborativo + Refinamento Iterativo** (12/11/2025)  
Sistema multi-agente conduz refinamentos sucessivos da hipótese com feedback estruturado, versionamento explícito e decisão forçada quando o limite de iterações é atingido.

**ÉPICO 3: Orquestrador + Estruturador (Base Multi-Agente)**  
Orquestrador coordena metodologista e estruturador, avaliando maturidade da ideia, integrando respostas e registrando justificativas.

---

## 📋 PRÓXIMAS FUNCIONALIDADES

## ÉPICO 5: Interface Conversacional e Transparência

**Objetivo:** Proporcionar experiência visual que torne a execução multi-agente transparente e acompanhável em tempo real, destacando custos, decisões e evolução da sessão.
Consulte `docs/product/vision.md` (Seção 5) para princípios de interação com usuário.

**Status:** 🟡 Em andamento (infraestrutura pronta, integrações pendentes)

**Dependências:**
- Épico 3 concluído (multi-agente base)
- Épico 4 concluído (loop colaborativo)

### Funcionalidades:

#### ✅ 5.1 Dashboard Streamlit com Timeline (CONCLUÍDO - 13/11/2025)
- **Descrição:** Entregar interface Streamlit que exibe timeline cronológica de eventos de cada sessão ativa.
- **Critérios de Aceite:**
  - ✅ Página principal lista sessões em andamento e permite abrir detalhes em tempo real.
  - ✅ Timeline mostra início e término de cada agente com timestamps e status (executando, concluído, erro).
  - ✅ Painel atualiza automaticamente (polling) sem recarregar a página manualmente.
- **Implementado:**
  - EventBus para comunicação entre CLI/Graph e Dashboard via arquivos JSON temporários
  - Models Pydantic para eventos (SessionStarted, AgentStarted, AgentCompleted, AgentError, SessionCompleted)
  - Instrumentação do multi_agent_graph.py para emitir eventos em cada nó
  - Dashboard Streamlit com timeline visual, status coloridos por agente, e estatísticas
  - Auto-refresh configurável (1-10s, padrão: 2s)
  - Testes unitários completos (test_event_models.py, test_event_bus.py)
  - Script de validação (scripts/validate_dashboard.py)
- **Como usar:**
  - Terminal 1: `streamlit run app/dashboard.py`
  - Terminal 2: `python cli/chat.py`
  - Veja eventos em tempo real no Dashboard!

#### 5.2 Métricas de Tokens e Custo
- **Descrição:** Expor tokens e custo estimado por agente e o acumulado da sessão.
- **Critérios de Aceite:**
  - Para cada evento exibido, apresentar `tokens_input`, `tokens_output` e `tokens_total`.
  - Calcular e exibir custo por agente e custo total da sessão usando tabela de preços configurável.
  - Exibir alerta quando custo total ultrapassar limite configurado.

#### 5.3 Resumo Sintético do Pensamento
- **Descrição:** Mostrar resumo curto da ação ou raciocínio entregue por cada agente.
- **Critérios de Aceite:**
  - Feed apresenta resumo textual (até 280 caracteres) do output/pensamento do agente, com indicação do tipo de ação.
  - Usuário pode expandir um evento para ver a resposta completa do agente diretamente na interface.
  - Disponibilizar botão para exportar o feed atual em JSON com os mesmos campos exibidos.

#### 5.4 Integração com CLI Existente
- **Descrição:** Adaptar CLI para publicar eventos consumidos pelo dashboard sem interromper o fluxo existente.
- **Critérios de Aceite:**
  - CLI gera eventos estruturados (`agent`, `action`, `started_at`, `finished_at`, `tokens`, `summary`) acessíveis ao Streamlit.
  - Canal de comunicação pode ser arquivo temporário ou endpoint local, com abordagem documentada no código.
  - Falhas no dashboard não bloqueiam a execução principal; CLI registra aviso em PT-BR quando não conseguir notificar a interface.

**Fora de escopo:** Persistência durável das sessões (disco/DB) — mover para backlog.

---

## ÉPICO 6: Memória Dinâmica e Contexto por Agente

**Objetivo:** Controlar o contexto de cada agente de forma configurável, registrando metadados de execução e permitindo resets confiáveis por sessão.
Consulte `docs/product/vision.md` (Seção 4) para modelo conceitual de Tópico e artefatos.

**Status:** ✅ Refinado (Pronto para implementação)

**Dependências:**
- Épico 3 concluído (multi-agente base)
- Épico 4 concluído (loop colaborativo)
- Instrumentação do Épico 5 para exibir metadados (recomendado)

### Progresso atual

#### Entregas concluídas
- Motor de memória dinâmica implementado (`MemoryManager` + `AgentExecution`) com cobertura de testes unitários (`tests/unit/test_memory_manager.py`).
- Loader e validador de YAML para configurar prompts/limites (`load_agent_config`, `validate_agent_config_schema`) com testes de regressão.

#### Pendências principais
- Integrar `config/agents/*.yaml` ao runtime dos agentes (prompts e limites ainda hard-coded em `agents/orchestrator/nodes.py`, `agents/methodologist/nodes.py`, etc.).
- Conectar `MemoryManager` ao `MultiAgentState`/super-grafo para registrar tokens reais e expor dados para a interface do Épico 5.
- Adicionar comando/flag de reset na CLI preservando logs já emitidos.

### Funcionalidades

#### 6.1 Configuração Externa de Agentes
- **Status:** ✅ Concluído (13/11/2025)
- **Descrição:** Definir prompts e parâmetros de memória em arquivos `config/agents/<papel>.yaml`.
- **Entregue:**
  - Arquivos YAML por agente + loader/validador com testes (`load_agent_config`, `load_all_agent_configs`)
  - Integração runtime em todos os nós: `orchestrator_node`, `structurer_node`, `decide_collaborative`, `force_decision_collaborative`
  - Fallback automático para prompts hard-coded quando YAML não está disponível
  - Mensagens de erro em PT-BR em todos os nós e no bootstrap
  - Validação de configs no bootstrap do super-grafo (`create_multi_agent_graph`)
  - Scripts de validação: `scripts/validate_runtime_config_simple.py`, `scripts/validate_syntax.py`
  - Versões atualizadas: Orquestrador (v2.0), Estruturador (v3.0), Metodologista (v3.0), Super-grafo (v3.0)

#### 6.2 Registro de Memória com Metadados
- **Status:** ✅ Concluído (13/11/2025)
- **Descrição:** Armazenar histórico leve por agente com tokens e resumo da última ação.
- **Entregue:**
  - Infraestrutura do `MemoryManager` com export, totais e API Python
  - Helper `register_execution()` para captura de tokens de AIMessage
  - Instrumentação completa dos nós: orchestrator, structurer, methodologist (decide_collaborative e force_decision)
  - MemoryManager passado via config do super-grafo (opcional)
  - Integração com CostTracker validada (custos calculados e registrados)
  - CLI atualizado para exibir métricas de tokens e custos por agente
  - Script de validação end-to-end: `scripts/validate_memory_integration.py`
  - Versões atualizadas: orchestrator_node v2.1, structurer_node v3.1, methodologist nodes v3.1

#### 6.3 Reset Global de Sessão
- **Status:** ⛔ Não iniciado
- **Descrição:** Implementar reset que limpa memórias e estado compartilhado de uma sessão.
- **Critérios de Aceite Ajustados:**
  - CLI oferece comando/flag (`--reset` ou equivalente) para iniciar sessão limpa ou resetar sessão ativa durante execução.
  - Reset remove históricos dos agentes sem afetar logs já emitidos na interface.
  - Registro em backlog dedicado para reset individual por agente (fora do escopo deste épico).

#### 6.4 Telemetria do Super-Grafo
- **Status:** ⛔ Não iniciado
- **Descrição:** Expor métricas de tokens/custos e resumo mais recente para cada agente diretamente a partir do super-grafo.
- **Critérios de Aceite:**
  - Cada nó registra tokens de entrada/saída e resumo em `MemoryManager` ao concluir.
  - `MultiAgentState` fornece acesso a estatísticas consolidadas para consumo pelo Épico 5.
  - Logs emitidos incluem alertas quando limites configurados são ultrapassados.

**Fora de escopo:** Reset parcial por agente e persistência durável da memória — adicionar ao backlog.

---

## ÉPICO 7: Modelo de Dados e Persistência Durável

**Objetivo:** Implementar modelo de dados "Tópico/Ideia" que persiste entre sessões, suportando múltiplos tipos de artigo e evolução fluida (ideação → artigo).

**Status:** ⚠️ Não refinado (Requer discussão madura)

**Dependências identificadas:**
- Épico 5 (Interface) para exibir lista de tópicos
- Épico 6 (Memória) para contexto e RAG por tópico
- `docs/product/vision.md` para tipos de artigo e fluxos adaptativos

### Pontos a definir na próxima sessão:

#### 7.1 Entidade "Tópico"
- Definir modelo de dados completo (ver Seção 4 de `docs/product/vision.md`)
- Campos: id, title, article_type, stage, created_at, updated_at, artifacts, thread_id
- Tipos de artigo suportados: empirical, review, theoretical, case_study, meta_analysis, methodological
- Estágios de maturidade: ideation, hypothesis, methodology, research, writing, review, done

#### 7.2 Persistência Durável
- Estratégia de persistência: SqliteSaver (LangGraph) vs PostgreSQL
- Estrutura de diretórios: `/data/topics/{topic_id}/`
- Checkpointer vinculado a thread_id do LangGraph
- Migração de MemorySaver atual para persistência durável

#### 7.3 Gestão de Sessões
- Comandos CLI: `list` (listar tópicos), `resume ` (retomar), `new` (criar)
- Retomar sessão semana depois (carregar contexto completo)
- Trabalhar em múltiplos tópicos (mas um por vez)
- Índice de tópicos em progresso (ordenado por updated_at)

#### 7.4 Artefatos Versionados
- Tipos de artefato: outline, papers (pesquisas), drafts (rascunhos), decisions (metodológicas)
- Versionamento explícito (V1, V2, V3) vs apenas última versão
- Estrutura de Artifact: type, content, created_at, version
- Exportação futura (PDF, Word, LaTeX) - adicionar ao backlog

#### 7.5 Detecção de Tipo de Artigo
- Orquestrador infere tipo na conversa inicial (ver Seção 2 de `docs/product/vision.md`)
- Perguntas dinâmicas para confirmar tipo quando ambíguo
- Permitir mudança de tipo ao longo da conversa (começa observacional, vira empírico)
- Adaptar fluxo de agentes conforme tipo detectado

#### 7.6 Estágios de Maturidade
- Sistema detecta stage automaticamente (não pergunta diretamente)
- Transições fluidas e não-lineares (pode voltar de "methodology" para "hypothesis")
- Orquestrador decide stage com base em artefatos presentes
- Logs registram mudanças de stage para rastreabilidade

### Observações de paralelização:
- Implementação pode começar após Épicos 5 e 6 estarem estáveis
- Funcionalidades 7.1 e 7.2 são base (fazer primeiro)
- Funcionalidades 7.3-7.6 podem ser incrementais
- Interface (Épico 5) precisará integrar lista de tópicos depois

---

## ÉPICO 8: Pipeline Completo Ideia → Artigo

**Dependências:**
- Épico 7 (Modelo de Dados) para tipos de artigo e fluxos adaptativos
- Épico 5 para visualizar a evolução dos checkpoints
- Épico 6 para manter contexto e resumos entre etapas
- Ver `docs/product/vision.md` (Seções 2 e 3) para fluxos por tipo

**Objetivo:** Estruturar a evolução de uma sessão desde a ideia inicial até a preparação do artigo, articulando checkpoints obrigatórios e artefatos intermediários.

**Status:** ⚠️ Não refinado (Requer definição arquitetural)

### Pontos em aberto:
- Representação dos checkpoints mínimos (ideia, hipótese, metodologia, testes, outline) e respectivas transições.
- Onde armazenar os artefatos intermediários (log compartilhado ou store dedicado).
- Momento de entrada do Escritor e artefatos esperados em cada etapa (ex.: outline consolidado).
- Estratégia para retomar sessões sem persistência durável, garantindo consistência das etapas concluídas.

### Observação de paralelização:
- Assim que a arquitetura da entidade for definida, o design do pipeline pode avançar em paralelo ao refinamento do debate (Épico 9), reutilizando componentes da interface e memória.

---

## ÉPICO 9: Debate Multi-Agente Mediado

**Objetivo:** Permitir que o orquestrador conduza debates estruturados entre Estruturador e Metodologista, consolidando uma decisão final com voto de minerva e transparência sobre o processo.

**Status:** ⚠️ Não refinado (Requer discussão madura)

**Dependências identificadas:**
- Épico 5 (interface) para expor o debate em tempo real.
- Épico 6 (memória) para compartilhar contexto e resumos das contribuições.

### Pontos a definir na próxima sessão:
- Fluxo detalhado do debate (ordem das falas, número de rodadas, condições de parada).
- Ajuste dinâmico do prompt do orquestrador (runtime versus edição de arquivos de configuração).
- Critérios para o voto de minerva e como documentar a decisão final.
- Escopo inicial de logging: registrar apenas decisão final e justificativa, mantendo logs individualizados como backlog.

### Observação de paralelização:
- Após a entrega dos épicos 5 e 6, a modelagem do fluxo de debate e prompts pode avançar em paralelo à evolução da interface, desde que compartilhem os metadados definidos na memória.

---

## 📋 BACKLOG

### 🗂️ PERSISTÊNCIA E DADOS (Épico 7 detalhado)

**Migração para Banco de Dados:**
- Avaliar migração de SqliteSaver para PostgreSQL (quando escalar)
- Considerar replicação/backup de tópicos
- Performance: índices, queries otimizadas

**Exportação de Artefatos:**
- Gerar PDF/Word/LaTeX do artigo final
- Exportar outline, pesquisas, decisões separadamente
- Templates formatados por tipo de artigo

**Gestão Avançada de Tópicos:**
- Arquivar tópicos concluídos
- Busca por tópicos (título, tipo, stage)
- Tags/labels customizáveis
- Estatísticas (tópicos por tipo, tempo médio por stage)

**Versionamento Completo:**
- Git-like para artefatos (diff, merge, rollback)
- Histórico de decisões do Orquestrador
- Timeline visual de evolução

### 🔜 PRÓXIMOS PASSOS

Funcionalidades que agregarão valor, mas dependem do sistema multi-agente core (Épicos 3-5) estar validado e sólido.

**Reset Parcial por Agente:**
- Permitir limpar memória de um agente específico sem encerrar a sessão inteira
- Garantir que outros agentes mantenham histórico e referências consistentes

**Log de Parecer Individual no Debate:**
- Registrar argumentos completos de cada agente antes do voto de minerva
- Disponibilizar comparação lado a lado na interface e export JSON

**Modelo de Dados Sessão → Ideia → Hipótese → Artigo:**
- Definir entidade única que evolui ao longo do pipeline com versionamento
- Mapear requisitos de armazenamento para suportar RAG e futura persistência durável

**Estruturador Avançado (Evolução do 3.2):**
- Transformar Estruturador em grafo próprio (similar ao Metodologista)
- Adicionar tool `ask_user` para clarificações durante estruturação
- Loop interno de refinamento da questão de pesquisa
- State próprio: `StructurerState`

**Depuração Interativa:**
- Pausar execução e inspecionar `MultiAgentState`
- Métricas de performance por agente (tempo, tokens, custo, iterações)

**Pesquisador:**
- Busca bibliográfica automática (Google Scholar, Semantic Scholar)
- Síntese de papers acadêmicos relevantes
- Identificação de gaps na literatura
- Comparação de abordagens metodológicas

**Escritor:**
- Compilação de seções do artigo baseado em outline
- Formatação acadêmica (ABNT, APA, Chicago, etc)
- Geração de rascunhos com estilo consistente
- Integração com pesquisas e validações anteriores

**Crítico:**
- Revisão final de rigor científico e coerência
- Identificação de contradições ou gaps argumentativos
- Validação de integridade do argumento completo
- Sugestões de melhorias de redação e clareza

---

### 🔧 MELHORIAS ESTRUTURAIS (Quando Necessário)

Refatorações de qualidade de código e infraestrutura. Não bloqueiam funcionalidades, mas facilitam colaboração e manutenção. Considerar quando houver contribuidores externos, projeto crescer significativamente, ou precisar publicar como pacote.

**Estrutura de Projeto (src layout):**
- Migrar para `src/paper_agent/` com `pyproject.toml`
- Remover hacks de `sys.path` via `pip install -e .`
- Facilita distribuição e testes isolados

**Consolidação de Configuração:**
- Migrar `pytest.ini` para `pyproject.toml`
- Centralizar configs de ferramentas (black, ruff, mypy)

**Dependency Management:**
- Avaliar migração para `pyproject.toml` + pip-tools/poetry
- Lock de versões para builds reproduzíveis

---

### 🌙 FUTURO DISTANTE

Funcionalidades avançadas que não são prioridade no momento, mas podem ser valiosas no longo prazo.

**Infraestrutura Avançada:**
- RAG e Vector Database para memória de longo prazo entre artigos
- Persistência avançada em banco de dados relacional
- Sistema de versionamento de artigos (branches, merge, rollback)
- Cache inteligente de pesquisas e validações

**Integração e Colaboração:**
- Integração com gestores de referências (Zotero, Mendeley)
- Sistema multi-usuário com autenticação
- Compartilhamento e colaboração em tempo real
- Comentários e feedback inline

**Analytics e Melhorias:**
- Dashboard de métricas de uso (tokens, custos, tempo)
- Análise de qualidade de artigos gerados
- Sugestões automáticas de melhoria baseadas em patterns
- A/B testing de prompts de agentes

**Exportação e Formatação:**
- Múltiplos formatos de saída (PDF, LaTeX, Word, Markdown)
- Templates de revistas científicas específicas
- Submissão automática para repositórios de preprints (arXiv, bioRxiv)
- Geração de apresentações (slides) a partir do artigo

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo

### Ordem proposta:
1. **Setup** → valida ambiente ✅
2. **Metodologista isolado** → valida um agente ✅ (falta 2.6-2.8)
3. **Orquestrador** → valida reasoning/decisão
4. **Interface** → valida transparência
5. **LangGraph avançado** → valida arquitetura final
