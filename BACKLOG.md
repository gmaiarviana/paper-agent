# BACKLOG - Paper Agent

## 🔜 PRÓXIMOS PASSOS

Funcionalidades essenciais para alcançar a visão de produto.

---

### Error Handling e Retry Logic
Sistema robusto que não quebra com erros de API ou parsing.

- Retry com backoff exponencial (3 tentativas: 2s → 4s → 8s)
- JSON parsing defensivo com fallback (extract_json quando parsing falhar)
- Validação Pydantic em outputs de todos os agentes
- Circuit breaker para API (stop após 5 falhas seguidas)
- Logging estruturado de erros e retries

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

### Estruturador como Sub-Grafo
Transformar Estruturador de função simples para agente complexo com reasoning loop.

- Sub-grafo com 3 nós: `analyze_input` → `ask_context` → `structure_question`
- Tool `ask_user` para clarificações (similar ao Metodologista)
- Reasoning loop (pergunta até ter contexto suficiente)
- Estado próprio: `StructurerState` (TypedDict)
- Limite de iterações (max 3 perguntas)

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
- Métricas de custo no dashboard Streamlit
- Config em `.env`: `MAX_COST_PER_SESSION=1.0`

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

### Pesquisador
Agente para busca e síntese de literatura acadêmica (essencial para revisões e contextualização).

- Busca bibliográfica automática (Google Scholar, Semantic Scholar)
- Síntese de papers acadêmicos relevantes
- Identificação de gaps na literatura
- Comparação de abordagens metodológicas
- RAG para armazenar papers encontrados
- Tool `search_papers(query)` e `find_similar_papers(paper_id)`

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

## 🌙 FUTURO DISTANTE

Funcionalidades desejáveis mas não essenciais para MVP.

---

### Session Replay (Debug)
Reproduzir sessões passo a passo para debugging avançado.

- Gravar todas interações (estado antes/depois, LLM calls, decisões)
- Storage: JSONL file por sessão em `runtime/recordings/`
- CLI: `python cli/replay_session.py session-123`
- Breakpoints interativos (pause em nó específico)
- Step-by-step execution com inspeção de estado

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

- Dashboard de métricas de uso (tokens, custos, tempo)
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

**Versão:** 1.0  
**Data:** 2025-11-14

