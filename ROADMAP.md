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

**ÉPICO 5: Interface Conversacional e Transparência (parcial)** (13/11/2025)  
Funcionalidade 5.1 concluída: Dashboard Streamlit com timeline de eventos em tempo real.

**ÉPICO 6: Memória Dinâmica e Contexto por Agente (parcial)** (13/11/2025)  
Funcionalidade 6.1 concluída: Configuração externa de agentes via YAML. Funcionalidade 6.2 em andamento: Registro de memória com metadados.

---

## 📋 PRÓXIMAS FUNCIONALIDADES

## ÉPICO 7: Orquestrador Conversacional Inteligente

**Objetivo:** Transformar sistema de "trilho fixo" em diálogo adaptativo onde usuário e sistema decidem caminho juntos através de negociação contínua.

**Status:** 🟡 Em refinamento

**Dependências:**
- Épico 6.2 concluído (registro de memória)

**Consulte:** `docs/orchestration/conversational_orchestrator.md` para especificação detalhada.

### Progressão POC → Protótipo → MVP

#### POC (primeira entrega - foco mínimo viável)
- 7.1: Orquestrador mantém diálogo fluido (não apenas roteia)
- 7.2: Oferece opções ao usuário (não impõe caminho)
- 7.3: Chama agentes sob demanda (quando usuário concorda)

**Critérios de aceite POC:**
- Sistema conversa antes de chamar agente
- Usuário pode escolher entre opções (A, B ou C)
- Agentes só executam após confirmação

#### Protótipo (segunda entrega - inteligência básica)
- 7.4: Detecção inteligente de quando agente faz sentido
- 7.5: Provocação de reflexão ("Você pensou em X?")
- 7.6: Handling de mudança de direção

**Critérios de aceite Protótipo:**
- Sistema sugere agente apropriado no momento certo
- Faz perguntas esclarecedoras que ajudam usuário
- Adapta quando usuário muda de ideia

#### MVP (terceira entrega - sistema completo)
- 7.7: Detecção emergente de estágio (exploration → hypothesis)
- 7.8: Reasoning explícito das decisões
- 7.9: Histórico de decisões do usuário (aprende preferências)

**Critérios de aceite MVP:**
- Sistema infere estágio sem classificar explicitamente
- Explica por que sugeriu determinada ação
- Adapta sugestões baseado em padrões do usuário

---

## ÉPICO 8: Entidade Tópico + Persistência Básica

**Objetivo:** Permitir pausar/retomar conversas com contexto completo preservado, suportando múltiplos tópicos em evolução.

**Status:** ⚠️ Não refinado

**Dependências:**
- Épico 7 POC concluído

**Consulte:** `docs/architecture/state_evolution.md` para detalhes de evolução de estado.

### Progressão POC → Protótipo → MVP

#### POC (persistência básica)
- 8.1: Modelo de dados Tópico (id, title, stage, artifacts)
- 8.2: Persistência em SqliteSaver (salva checkpoints LangGraph)
- 8.3: CLI: comandos `list`, `resume <id>`, `new`

**Critérios de aceite POC:**
- Usuário pode listar tópicos ativos
- Pode retomar conversa de ontem com contexto preservado
- Pode criar novo tópico a qualquer momento

#### Protótipo (artefatos e timeline)
- 8.4: Artefatos versionados (hypotheses V1/V2, research_notes, decisions)
- 8.5: Timeline de evolução do tópico

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

**Critérios de aceite Protótipo:**
- Sistema rastreia versões de hipóteses (V1 → V2 → V3)
- Usuário pode ver evolução temporal do tópico
- Artefatos são recuperáveis

#### MVP (gestão completa)
- 8.6: Múltiplos tópicos ativos (trabalha um por vez)
- 8.7: Busca por tópicos (título, stage, data)

**Critérios de aceite MVP:**
- Usuário gerencia vários tópicos simultaneamente
- Pode buscar "tópicos sobre LLMs"
- Dashboard mostra todos os tópicos em progresso

---

## ÉPICO 9: Finalizar Interface + Telemetria

**Objetivo:** Dashboard visual completo mostrando raciocínio do sistema em tempo real com métricas detalhadas.

**Status:** 🟡 Parcialmente refinado

**Dependências:**
- Épico 7 POC (para exibir decisões do Orquestrador)

### Funcionalidades (sem progressão - podem ser feitas em paralelo)

#### 9.1: Métricas de Tokens e Custo (ex-5.2)
- Exibir tokens_input, tokens_output, tokens_total por agente
- Calcular custo por agente e custo total da sessão
- Alerta quando custo ultrapassar limite configurável

#### 9.2: Resumo Sintético do Pensamento (ex-5.3)
- Feed com resumo curto (≤280 chars) do raciocínio de cada agente
- Botão para expandir e ver resposta completa
- Exportar feed em JSON

#### 9.3: Integração CLI com Telemetria (ex-5.4)
- CLI gera eventos estruturados consumidos pelo Streamlit
- Canal: arquivo JSONL em `runtime/streams/`
- Falhas no dashboard não bloqueiam CLI

#### 9.4: Reset Global de Sessão (ex-6.3)
- CLI oferece comando/flag `--reset` para limpar sessão
- Remove históricos dos agentes sem afetar logs emitidos
- Backlog: reset individual por agente

#### 9.5: Telemetria do Super-Grafo (ex-6.4)
- Cada nó registra tokens e resumo ao concluir
- MultiAgentState expõe estatísticas consolidadas
- Logs emitem alertas quando limites são ultrapassados

---

## 📋 BACKLOG

### Movido do Roadmap Principal (não alinha com visão adaptativa)

**Pipeline Completo Ideia → Artigo (antigo Épico 8):**
- Checkpoints obrigatórios são muito prescritivos
- Contradiz fluxo adaptativo onde usuário decide o caminho
- Depende de Orquestrador inteligente funcionar primeiro

**Debate Multi-Agente Mediado (antigo Épico 9):**
- Assume fluxo de debates estruturados
- Depende de Orquestrador conversacional estar maduro
- Pode ser retomado quando sistema tiver conversas ricas

**Detecção Automática de Tipo de Artigo:**
- Sistema não deve classificar automaticamente no início
- Tipo emerge da conversa (princípio de conversação)
- Pode ser feature do Épico 7 MVP (detecção emergente)

---

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
