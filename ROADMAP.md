# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/vision/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Concluídos
- Infraestrutura base completa
- **ÉPICO 1**: Convergência Orgânica
- **ÉPICO 2**: Sidebar
- **ÉPICO 3**: Bastidores
- **ÉPICO 4**: Contexto
- **ÉPICO 5**: UX Polish - Custos exibidos em reais (BRL) com formato brasileiro
- **ÉPICO 6**: Limpeza de Testes - Suite de testes limpa e focada com testes de integração reais
- **ÉPICO 7**: Validação de Maturidade do Sistema - Validação manual com 10 cenários críticos executados
- **ÉPICO 8**: Análise Assistida de Qualidade - Ferramentas para execução multi-turn, relatórios estruturados, sistema de observabilidade completo e migração da estrutura de testes (226 unit tests, 11 smoke tests, estrutura modular por categoria)
- **ÉPICO 9**: Integração Backend↔Frontend - Persistência silenciosa e feedback visual de progresso completos

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Planejados (refinados)
- **ÉPICO 10**: Observador - Mente Analítica (POC)

#### Planejados (não refinados)
- **ÉPICO 11**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 12**: Observador Integrado ao Fluxo (não refinado)
- **ÉPICO 13**: Catálogo de Conceitos - Interface Web (não refinado)
- **ÉPICO 14**: Pesquisador (não refinado)
- **ÉPICO 15**: Escritor (não refinado)


**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ✅ ÉPICO 8: Análise Assistida de Qualidade

Ferramentas para execução multi-turn, relatórios estruturados, sistema de observabilidade completo e migração da estrutura de testes. Implementado: Multi-Turn Executor (8.1), Debug Mode (8.2), logging estruturado (JSONL), debug reports, session replay e reorganização completa dos testes em estrutura modular (unit/smoke/behavior/e2e). Resultado: 226 unit tests e 11 smoke tests passando, 0 falhas.

---

## ÉPICO 10: Observador - Mente Analítica (POC)

**Objetivo:** Sistema monitora conversa e cataloga conceitos automaticamente. Foundation para inteligência semântica.

**Status:** ✅ Refinado (pronto para implementação)

> **📖 Filosofia:** Observador trabalha silenciosamente em paralelo ao Orquestrador, atualizando CognitiveModel e extraindo conceitos sem interferir no fluxo conversacional.

**Dependências:**
- Épico 9 (Integração Backend↔Frontend)

**Consulte:**
- `docs/agents/observer.md` - Documentação completa do Observador
- `docs/architecture/observer_architecture.md` - Arquitetura técnica
- `docs/architecture/concept_model.md` - Schema técnico de Concept
- `docs/architecture/ontology.md` - CognitiveModel e Conceitos

### Funcionalidades:

#### 10.1 Mitose do Orquestrador

- **Descrição:** Separar responsabilidades de facilitar conversa (Orquestrador) de observar raciocínio (Observador).
- **Critérios de Aceite:**
  - Deve criar novo agente: `Observador` em `agents/observer/`
  - Orquestrador mantém: facilitar conversa, negociar, decidir fluxo
  - Observador recebe: atualizar CognitiveModel, extrair conceitos, calcular métricas
  - Deve definir interface de consulta: `ObservadorAPI` em `agents/observer/api.py`
  - Métodos: `what_do_you_see()`, `get_current_state()`, `has_contradiction()`, `get_solidez()`
  - Consultas são não-determinísticas (Orquestrador consulta quando incerto)

#### 10.2 Observador - CognitiveModel Básico

- **Descrição:** Observador processa TODOS os turnos e atualiza CognitiveModel completo.
- **Critérios de Aceite:**
  - Deve processar cada turno automaticamente (não depende de snapshots)
  - Deve extrair: claims, fundamentos, contradições, conceitos, open_questions
  - Deve atualizar: `CognitiveModel` em memória (ainda não persistido)
  - Deve calcular métricas: solidez (0-1), completude (0-1)
  - Deve publicar eventos: `CognitiveModelUpdatedEvent` para Dashboard
  - **Não** deve interferir no fluxo conversacional (silencioso)

#### 10.3 Setup ChromaDB + Schema SQLite

- **Descrição:** Configurar ChromaDB para vetores semânticos e SQLite para metadados estruturados.
- **Critérios de Aceite:**
  - Deve instalar: `chromadb`, `sentence-transformers`
  - Deve criar cliente: `chromadb.PersistentClient(path="./data/chroma")`
  - Deve criar collection: `concepts` (metadata: label, essence, variations)
  - Deve usar modelo: `all-MiniLM-L6-v2` (384 dim, 80MB)
  - **SQLite:**
    - Tabela `concepts`: id, label, essence, variations JSON, chroma_id
    - Tabela `concept_variations`: concept_id, variation
    - Tabela `idea_concepts`: idea_id, concept_id (N:N)
  - Deve criar índices: ON label, ON idea_id, ON concept_id

#### 10.4 Pipeline de Detecção de Conceitos

- **Descrição:** LLM extrai conceitos a cada turno e salva em ChromaDB + SQLite.
- **Critérios de Aceite:**
  - Deve extrair conceitos via LLM (prompt: "Extrair conceitos-chave deste turno")
  - Deve gerar embedding via sentence-transformers (all-MiniLM-L6-v2)
  - Deve salvar no ChromaDB (vetor) + SQLite (metadados)
  - Deve buscar similares (threshold 0.80 = mesmo conceito)
  - **Deduplicação:**
    - Similaridade > 0.80: adiciona como variation do conceito existente
    - Similaridade < 0.80: cria novo conceito
  - Deve criar registro em `idea_concepts` (link N:N) quando snapshot é criado
  - **Não** deve executar a cada mensagem (apenas quando processando turno)

#### 10.5 Busca Semântica Básica

- **Descrição:** Buscar conceitos similares via embeddings.
- **Critérios de Aceite:**
  - Deve implementar: `find_similar_concepts(query: str, top_k: int) -> list[Concept]`
  - Deve calcular similaridade cosseno entre embeddings
  - Deve usar threshold 0.80 para deduplicação
  - Deve retornar lista ordenada por similaridade (descendente)
  - Deve incluir metadados: label, essence, variations, similarity_score

#### 10.6 Testes POC

- **Descrição:** Testes unitários para validar Observador isolado.
- **Critérios de Aceite:**
  - Deve criar mocks do Observador (não chamadas LLM reais)
  - Deve testar extração de conceitos com inputs fixos
  - Deve validar schema SQLite (criar tabelas, índices)
  - Deve testar busca semântica com vetores fixos (não embeddings reais)
  - Deve validar deduplicação (threshold 0.80)
  - **Não** deve integrar ao grafo ainda (teste isolado)
  - **Não** deve usar API real (mocks apenas)

---

## ÉPICO 11: Alinhamento de Ontologia

**Objetivo:** Migrar código atual (premises/assumptions como strings separadas) para nova ontologia (Proposição unificada com solidez derivada de Evidências).

**Status:** ⏳ Planejado (não refinado)

**Abordagem:** Evolução gradual, não refatoração big-bang.

**Dependências:**
- Épicos 9-10 concluídos

**Referências:**
- `docs/architecture/ontology.md` - Nova ontologia
- `docs/vision/epistemology.md` - Fundamentos epistemológicos

---

## ÉPICO 12: Observador Integrado ao Fluxo

**Objetivo:** Orquestrador consulta Observador para decisões contextuais. Conversas mais inteligentes.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épicos 10-11

**Consulte:**
- `docs/agents/observer.md` - Comunicação Observador ↔ Orquestrador
- `docs/architecture/observer_architecture.md` - Integração com grafo

### Funcionalidades Planejadas:

#### 12.1 Integrar Observador ao Grafo (Paralelo)

- Observador roda em paralelo a cada turno
- Investigar: LangGraph suporta paralelismo? Se não, usar callback
- Não bloqueia fluxo principal

#### 12.2 Interface de Consulta Não-Determinística

- Orquestrador consulta quando incerto
- Gatilhos naturais: mudança direção, contradição, completude
- Observador responde com insights, não comandos

#### 12.3 Detecção de Variations Automática

- Threshold > 0.90: adiciona variation automaticamente
- Threshold 0.80-0.90: pergunta ao usuário
- Threshold < 0.80: conceito novo

#### 12.4 Visualização nos Bastidores

- Timeline (colapsável): ações de todos agentes
- Painel Observador (colapsável): CognitiveModel em tempo real
- Ambos colapsados por padrão
- Mostra Observador na timeline apenas quando relevante

#### 12.5 Testes de Integração

- Cenários multi-turn com Observador ativo
- Validar que não interfere no fluxo
- LLM-as-Judge para qualidade de insights

---

## ÉPICO 13: Catálogo de Conceitos - Interface Web

**Objetivo:** Usuário explora biblioteca de conceitos via web. Transparência sobre o que sistema aprendeu.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12

**Consulte:**
- `docs/products/paper_agent.md` - Interface web conversacional
- `docs/interface/web/components.md` - Componentes Streamlit

### Funcionalidades Planejadas:

#### 13.1 Página Catálogo (`/catalogo`)

- Lista todos conceitos da biblioteca
- Busca por nome (fuzzy search)
- Filtros: por ideia, por frequência, por data
- Visualização: cards com conceito + variations + ideias relacionadas

#### 13.2 Preview na Página da Ideia

- Mostra discretamente: "Usa 3 conceitos: [X] [Y] [Z]"
- Tags clicáveis → redireciona para catálogo
- Não polui interface

#### 13.3 Analytics de Conceitos

- Conceitos mais mencionados (gráfico)
- Conceitos por ideia/artigo
- Evolução temporal
- Export em JSON
- Sistema detecta padrões: "5+ usuários adicionaram conceito X" → atualiza biblioteca base

#### 13.4 Testes E2E

- Fluxo completo: conversa → conceitos → catálogo
- Validar UX (não quebra experiência)
- Performance (biblioteca com 100+ conceitos)

---

## ÉPICO 14: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 13

**Adição:** Pesquisador pode usar catálogo de conceitos para buscar papers relacionados.

---

## ÉPICO 15: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 14

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
