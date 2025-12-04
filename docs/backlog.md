# BACKLOG - Paper Agent

## 📍 MÉDIO PRAZO

Melhorias importantes que expandem capacidades essenciais do sistema.

---

### Pesquisador
Agente para busca e síntese de literatura acadêmica (essencial para revisões e contextualização).

- Busca bibliográfica automática (Google Scholar, Semantic Scholar)
- Síntese de papers acadêmicos relevantes
- Identificação de gaps na literatura
- Comparação de abordagens metodológicas
- RAG para armazenar papers encontrados
- Tool `search_papers(query)` e `find_similar_papers(paper_id)`

---

### Estruturador como Sub-Grafo
Transformar Estruturador de função simples para agente complexo com reasoning loop.

- Sub-grafo com 3 nós: `analyze_input` → `ask_context` → `structure_question`
- Tool `ask_user` para clarificações (similar ao Metodologista)
- Reasoning loop (pergunta até ter contexto suficiente)
- Estado próprio: `StructurerState` (TypedDict)
- Limite de iterações (max 3 perguntas)

---

### Error Handling e Retry Logic
Sistema robusto que não quebra com erros de API ou parsing.

- Retry com backoff exponencial (3 tentativas: 2s → 4s → 8s)
- JSON parsing defensivo com fallback (extract_json quando parsing falhar)
- Validação Pydantic em outputs de todos os agentes
- Circuit breaker para API (stop após 5 falhas seguidas)
- Logging estruturado de erros e retries

---

## 🔜 PRÓXIMOS PASSOS

Funcionalidades técnicas que melhoram qualidade e manutenibilidade.

---

### RAG Infrastructure - Metodologista Knowledge Base
Metodologista consulta knowledge base via RAG ao invés de arquivo `.md` estático.

- Setup ChromaDB (vector store local, gratuito)
- Tool `consult_methodology(query)` com busca semântica
- Popular KB inicial com `docs/agents/methodologist_knowledge.md`
- Integrar tool no grafo do Metodologista
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- CLI para gerenciar KB: `python cli/kb_manager.py add/search/stats`

---

### Structured Logging
Logs estruturados em JSON para debugging e observabilidade.

- Logger JSON estruturado (trace_id, agent, node, event, tokens, cost, duration_ms)
- Instrumentar todos os nós (orchestrator, structurer, methodologist)
- Rastreamento completo de sessões (trace_id único por sessão)
- Logs exportáveis em JSONL (um arquivo por sessão)
- Níveis: DEBUG (prompts completos), INFO (decisões), ERROR (falhas)

---

### Cost Controller
Budget por sessão para evitar gastos inesperados.

- Budget configurável por sessão (default: $1, max: $10)
- Stop automático ao exceder budget
- Warning ao atingir 80% do budget
- Métricas de custo no dashboard
- Config em `.env`: `MAX_COST_PER_SESSION=1.0`

**Pendente:** Budget detalhado por tipo de artigo, alertas preventivos baseados em histórico.

---

### Agent Development Kit
Documentação, templates e patterns para criar novos agentes.

- Documentação completa: `docs/agents/creating_new_agents.md`
- Template base comentado: `agents/_template/` (copiar e adaptar)
- Exemplos de referência: Metodologista (complexo), Estruturador (simples)
- Checklist de implementação completa
- Patterns comuns documentados: reasoning loop, tools, conditional routing
- Helpers opcionais para boilerplate (TypedDict, graph setup básico)

---

### Escritor
Agente para compilação do artigo final (essencial para entregar artigo completo).

- Compilação de seções do artigo baseado em outline
- Formatação acadêmica (ABNT, APA, Chicago, etc)
- Geração de rascunhos com estilo consistente
- Integração com pesquisas e validações anteriores
- RAG sobre textos anteriores do usuário (aprender estilo)

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

**Contexto:** Funcionalidade planejada originalmente como Épico 18, movida para Backlog por não ser essencial para MVP. Ver `docs/vision/agent_personas.md`.

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

- Budget configurável por sessão (default: $1, max: $10)
- Stop automático ao exceder budget
- Warning ao atingir 80% do budget
- Alertas em tempo real na interface web
- Config em `.env`: `MAX_COST_PER_SESSION=1.0`
- Dashboard com histórico de gastos (últimos 30 dias)

**Contexto:** Funcionalidade planejada originalmente para MVP do Épico 8, mas movida para Backlog. Sistema já tem métricas consolidadas (Épico 8.3), alertas são otimização adicional.

---

### Session Replay (Debug)
Reproduzir sessões passo a passo para debugging avançado.

- Gravar todas interações (estado antes/depois, LLM calls, decisões)
- Storage: JSONL file por sessão em `runtime/recordings/`
- CLI: `python cli/replay_session.py session-123`
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

**Versão:** 1.0  
**Data:** 2025-11-14

