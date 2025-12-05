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
- **ÉPICO 5**: UX Polish
- **ÉPICO 6**: Limpeza de Testes

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Planejados (refinados)
- **ÉPICO 7**: Validação de Maturidade do Sistema - Fase Manual
- **ÉPICO 8**: Validação de Maturidade do Sistema - Automação
- **ÉPICO 9**: Integração Backend↔Frontend

#### Planejados (não refinados)
- **ÉPICO 10**: Conceitos (não refinado)
- **ÉPICO 11**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 12**: Pesquisador (não refinado)
- **ÉPICO 13**: Escritor (não refinado)


**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 5: UX Polish

**Objetivo:** Ajustes de experiência do usuário: custo em R$.

**Status:** ✅ Concluído

Custos exibidos em reais (BRL) com formato brasileiro, aplicado em toda interface (chat, backstage, dashboard).

---

## ÉPICO 6: Limpeza de Testes

**Objetivo:** Remover testes burocráticos e adicionar testes de integração reais onde há mocks superficiais.

**Status:** ✅ Concluído

Suite de testes limpa e focada: testes burocráticos removidos, testes de integração reais adicionados para validar comportamento do LLM, documentação atualizada com novos padrões.

---

## ÉPICO 7: Validação de Maturidade do Sistema - Fase Manual

**Objetivo:** Validar que sistema multi-agente funciona como deveria através de roteiro de cenários críticos executados manualmente.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Nenhuma (pode começar imediatamente)

**Duração estimada:** 1-2 dias (criação do roteiro) + 2-3 horas (execução)

**Consulte:** `docs/testing/epic7_validation_strategy.md` para estratégia completa

### Funcionalidades:

#### 7.1 Criar Roteiro de Validação Manual

- **Descrição:** Criar roteiro estruturado com 10-15 cenários críticos que validam comportamento do sistema multi-agente
- **Critérios de Aceite:**
  - Deve criar `docs/testing/epic7_validation_strategy.md` com estratégia completa
  - Deve definir 10-15 cenários críticos cobrindo:
    - Transições entre agentes (Orquestrador → Estruturador → Metodologista)
    - Preservação de contexto (focal_argument, messages)
    - Decisões coerentes (next_step, agent_suggestion)
    - Fluidez conversacional (sem quebras)
    - Provocação socrática (reflection_prompt)
    - Reasoning loop (Metodologista)
  - Cada cenário deve especificar:
    - Input do usuário
    - Comportamento esperado (checklist)
    - Logs necessários (EventBus, MultiAgentState)
    - Critérios de sucesso/falha

#### 7.2 Executar Cenários e Coletar Logs

- **Descrição:** Executar cenários manualmente e coletar logs estruturados
- **Critérios de Aceite:**
  - Deve executar todos os cenários no sistema real
  - Deve coletar logs estruturados (EventBus JSON + outputs)
  - Deve anotar comportamento observado (sucesso/falha/parcial)
  - Deve identificar problemas críticos, médios e baixos

#### 7.3 Analisar Resultados e Gerar Relatório de Maturidade

- **Descrição:** Analisar logs e gerar relatório de maturidade do sistema
- **Critérios de Aceite:**
  - Deve analisar todos os logs coletados
  - Deve classificar problemas encontrados (crítico/médio/baixo)
  - Deve gerar relatório de maturidade com:
    - Sumário executivo (sistema maduro? O que falta?)
    - Problemas por categoria (transições, contexto, decisões, fluidez)
    - Recomendações de correções
    - Priorização de correções
  - Deve documentar o que funciona bem (não apenas problemas)

---

## ÉPICO 8: Validação de Maturidade do Sistema - Automação

**Objetivo:** Automatizar validação de qualidade conversacional com LLM-as-Judge para prevenir regressões futuras.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Épico 7 (precisa identificar problemas reais primeiro)

**Duração estimada:** 2-3 dias

**Custo estimado:** ~$0.01-0.02 por execução completa

**Consulte:** `docs/testing/epic8_automation_strategy.md` para estratégia completa

### Funcionalidades:

#### 8.1 Implementar Infraestrutura LLM-as-Judge

- **Descrição:** Criar infraestrutura base para testes com LLM-as-judge
- **Critérios de Aceite:**
  - Deve criar fixture `llm_judge` em `tests/conftest.py` (modelo Haiku, temperature=0)
  - Deve criar prompts de avaliação em `utils/test_prompts.py`:
    - Prompt de fluidez conversacional
    - Prompt de integração entre agentes
    - Prompt de provocação socrática
    - Prompt de preservação de contexto
    - Prompt de qualidade de decisões
  - Deve criar função `extract_score` em `utils/test_helpers.py` (extrai score 1-5)
  - Deve adicionar marker `@pytest.mark.llm_judge` em `pytest.ini`
  - Deve pular testes se `ANTHROPIC_API_KEY` não estiver definida

#### 8.2 Criar Testes Automatizados para Problemas Identificados

- **Descrição:** Criar testes automatizados com LLM-as-Judge para problemas identificados no Épico 7
- **Critérios de Aceite:**
  - Deve criar testes para cada problema crítico/médio identificado no Épico 7
  - Cada teste deve validar qualidade (score >= 4) além de estrutura
  - Testes devem usar LLM-as-Judge para avaliar:
    - Fluidez conversacional (sem "Posso chamar X?")
    - Integração natural entre agentes
    - Provocação socrática genuína (não burocrática)
    - Preservação de contexto entre transições
    - Qualidade de decisões (coerentes com contexto)
  - Deve adicionar testes em arquivos apropriados:
    - `tests/integration/test_multi_agent_smoke.py` (fluidez, integração)
    - `tests/integration/test_methodologist_smoke.py` (provocação socrática)
    - Novos arquivos conforme necessário

#### 8.3 Documentar Estratégia e Custos

- **Descrição:** Documentar estratégia de testes automatizados e custos estimados
- **Critérios de Aceite:**
  - Deve atualizar `docs/testing/strategy.md` com seção sobre LLM-as-Judge
  - Deve documentar custos estimados (~$0.01-0.02 por execução completa)
  - Deve documentar estratégia de execução:
    - Local: `pytest -m llm_judge` (seletivo)
    - CI: rodar em PRs relevantes (quando implementado)
  - Deve documentar como adicionar novos testes LLM-as-Judge

---

## ÉPICO 9: Integração Backend↔Frontend

**Objetivo:** Completar ciclo de persistência silenciosa e feedback visual de progresso.

**Status:** 🔄 Em progresso (9.1 concluído)

**Dependências:** Nenhuma

**Duração estimada:** 2-3 dias

### Funcionalidades:

#### 9.1 Atualização de cognitive_model no Orchestrator ✅

- **Status:** Concluído
- **Descrição:** Implementar atualização do cognitive_model no orchestrator_node a cada turno
- **Critérios de Aceite:**
  - Prompt do orchestrator solicita `cognitive_model` no JSON de saída
  - Orchestrator extrai `cognitive_model` da resposta LLM
  - Orchestrator retorna `cognitive_model` no state update
  - Schema `CognitiveModel` usado para validação (Pydantic)
  - Campos: claim, premises, assumptions, open_questions, contradictions, solid_grounds, context

#### 9.2 Passar active_idea_id via Config

- **Descrição:** Disponibilizar active_idea_id no config do LangGraph (agnóstico de framework)
- **Critérios de Aceite:**
  - Streamlit adiciona `active_idea_id` ao config ao invocar grafo
  - Orchestrator acessa `active_idea_id` via `config.get("configurable", {})`
  - Funciona mesmo sem active_idea_id (opcional, não quebra fluxo)

#### 9.3 SnapshotManager no Orquestrador

- **Descrição:** Integrar avaliação de maturidade via LLM no orchestrator_node
- **Critérios de Aceite:**
  - Orchestrator chama `create_snapshot_if_mature()` após processar turno
  - Usa `SnapshotManager.assess_maturity()` existente (LLM avalia maturidade)
  - Threshold de confiança configurável (padrão: 0.8)
  - Silencioso: sem logs visíveis ao usuário, sem notificações
  - Depende de 9.1 (cognitive_model) e 9.2 (active_idea_id)

#### 9.4 Indicador de Solidez no Contexto

- **Descrição:** Exibir barra de progresso de solidez do argumento focal
- **Critérios de Aceite:**
  - Backend: Método reutilizável calcula solidez (ex: `CognitiveModel.calculate_solidez()`)
  - Frontend: Exibe barra de progresso (0-100%) no painel Contexto
  - Atualiza quando argumento focal muda
  - Agnóstico de framework (cálculo no backend, UI apenas exibe)

**Ordem de implementação:** 9.1 → 9.2 → 9.3 → 9.4

---

## ÉPICO 10: Conceitos

**Objetivo:** Criar entidade Concept com vetores semânticos para busca por similaridade ("produtividade" encontra "eficiência").

**Status:** ⏳ Planejado (não refinado)

> **📖 Filosofia:** Conceitos são essências globais (biblioteca única). Ideias referenciam conceitos, não os possuem. Ver `docs/architecture/ontology.md`.

**Dependências:**
- Épico 9

**Consulte:**
- `docs/architecture/concept_model.md` - Schema técnico de Concept
- `docs/architecture/tech_stack.md` - ChromaDB, embeddings, sentence-transformers
- `docs/architecture/ontology.md` - Filosofia: Conceitos como essências globais

### Funcionalidades:

#### 10.1 Setup ChromaDB Local [POC]

- **Descrição:** Configurar ChromaDB para armazenar vetores semânticos de conceitos (gratuito, local).
- **Critérios de Aceite:**
  - Deve instalar dependências: `chromadb`, `sentence-transformers`
  - Deve criar cliente persistente: `chromadb.PersistentClient(path="./data/chroma")`
  - Deve criar collection: `concepts` (metadata: label, essence, variations)
  - Deve usar modelo: `all-MiniLM-L6-v2` (384 dim, 80MB download)

#### 10.2 Schema SQLite de Concept [POC]

- **Descrição:** Criar tabelas `concepts` e `idea_concepts` para metadados estruturados e relacionamento N:N.
- **Critérios de Aceite:**
  - Deve criar tabela `concepts`: id, label, essence, variations JSON, chroma_id
  - Deve criar tabela `idea_concepts`: idea_id, concept_id (N:N, PK composta)
  - Campo `chroma_id` deve referenciar registro no ChromaDB
  - Deve criar índices: ON label, ON idea_id, ON concept_id
  - Conceitos são globais (biblioteca única), ideias referenciam via `idea_concepts`

#### 10.3 Pipeline de Detecção de Conceitos [POC]

- **Descrição:** LLM extrai conceitos-chave quando argumento amadurece (ao criar snapshot de Idea) e salva em ChromaDB + SQLite.
- **Critérios de Aceite:**
  - Deve disparar detecção ao criar snapshot de Idea (quando argumento amadurece)
  - Deve detectar conceitos via LLM (prompt: "Extrair conceitos-chave desta ideia/argumento")
  - Deve gerar embedding via sentence-transformers
  - Deve salvar no ChromaDB (vetor) + SQLite (metadata)
  - Deve criar registro em `idea_concepts` (linking N:N)
  - **Não** deve executar detecção a cada mensagem (apenas no snapshot)

#### 10.4 Busca Semântica [POC]

- **Descrição:** Buscar conceitos similares via embeddings (threshold > 0.80 = mesmo conceito).
- **Critérios de Aceite:**
  - Deve implementar: `find_similar_concepts(query: str, top_k: int) -> list[Concept]`
  - Deve calcular similaridade cosseno entre embeddings
  - Deve usar threshold 0.80 para deduplicação ("produtividade" = "eficiência")
  - Deve retornar lista ordenada por similaridade

#### 10.5 Variations Automáticas [Protótipo]

- **Descrição:** Sistema detecta variações linguísticas e adiciona ao Concept existente (colaboração = cooperação) com thresholds diferenciados.
- **Critérios de Aceite:**
  - Deve detectar variações via busca semântica durante detecção de conceitos
  - **Threshold > 0.90:** adicionar variation automaticamente ao Concept existente
  - **Threshold 0.80-0.90:** perguntar ao usuário: "São o mesmo conceito?" (colaboração = cooperação?)
  - Deve adicionar variation ao Concept existente se confirmado
  - Deve criar novo Concept se usuário rejeitar ou similaridade < 0.80

#### 10.6 Mostrar Conceitos na Interface [Protótipo]

- **Descrição:** Exibir conceitos detectados em dois níveis: preview discreto na página da ideia + exploração completa no Catálogo.
- **Critérios de Aceite:**
  - **Preview na página da ideia** (`/pensamentos/{idea_id}`):
    - Deve mostrar texto discreto: "Usa 3 conceitos: [Cooperação] [Ficção] [Linguagem]"
    - Tags clicáveis → redireciona para `/catalogo?concept={concept_id}`
  - **Exploração completa no Catálogo** (`/catalogo`):
    - Deve implementar busca por nome de conceito (LIKE query)
    - Deve implementar filtros: por ideias relacionadas, por variations
    - Deve mostrar lista de ideias que usam o conceito
    - Deve exibir variations como tags secundárias
    - Deve permitir navegação: conceito → ideias relacionadas → detalhes da ideia

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

## ÉPICO 12: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 11

---

## ÉPICO 13: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
