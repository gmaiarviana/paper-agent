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

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Planejados (refinados)
- **ÉPICO 5**: UX Polish (refinado)
- **ÉPICO 6**: Limpeza de Testes
- **ÉPICO 7**: Validação de Maturidade do Sistema - Fase Manual
- **ÉPICO 8**: Validação de Maturidade do Sistema - Automação

#### Planejados (não refinados)
- **ÉPICO 9**: Integração Backend↔Frontend (não refinado)
- **ÉPICO 10**: Conceitos (não refinado)
- **ÉPICO 11**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 12**: Pesquisador (não refinado)
- **ÉPICO 13**: Escritor (não refinado)

**Nota sobre Dependências:**
- Épicos 1, 2, 3, 4, 5 concluídos (independentes)
- Épicos 6, 7, 8 são independentes (podem começar imediatamente)
- Épico 8 depende do Épico 7 (precisa identificar problemas reais primeiro)
- Épicos 9-13 seguem sequência: Integração → Conceitos → Ontologia → Pesquisador → Escritor

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 5: UX Polish

**Objetivo:** Ajustes de experiência do usuário: custo em R$.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Épicos 3-4 (métricas movidas para Contexto)

### Funcionalidades:

#### 5.1 Custo em R$

- **Descrição:** Exibir custos em reais (BRL) com formato brasileiro
- **Critérios de Aceite:**
  - Deve adicionar configs em `.env`: `CURRENCY=BRL`, `USD_TO_BRL_RATE=5.5`
  - Deve converter USD → BRL usando taxa configurável
  - Deve exibir formato brasileiro: "R$ 0,02" (vírgula decimal)
  - Fallback: se `CURRENCY` não for `BRL`, mantém USD como hoje
  - Deve aplicar em todos os pontos: chat_history, backstage, dashboard

---

## ÉPICO 6: Limpeza de Testes

**Objetivo:** Remover testes burocráticos e adicionar testes de integração reais onde há mocks superficiais.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Nenhuma

**Duração estimada:** 1-2 dias

**Consulte:** `docs/testing/epic6_refactoring_plan.md` para plano detalhado

### Funcionalidades:

#### 6.1 Remover Testes Burocráticos

- **Descrição:** Remover testes que testam bibliotecas externas (Pydantic, YAML, etc.) sem lógica própria
- **Critérios de Aceite:**
  - Deve remover testes que validam apenas estrutura de dados (sem lógica)
  - Deve remover testes onde mock retorna exatamente o esperado
  - Deve remover testes com asserts fracos (`is not None`, sempre passa)
  - Deve documentar o que foi removido e por quê

#### 6.2 Adicionar Testes de Integração Reais

- **Descrição:** Adicionar testes de integração com API real onde há mocks superficiais
- **Critérios de Aceite:**
  - Deve criar `tests/integration/test_orchestrator_integration.py` com testes de classificação real
  - Deve criar `tests/integration/test_structurer_integration.py` com testes de estruturação real
  - Testes devem usar API real (não mocks)
  - Testes devem validar comportamento real (não apenas estrutura)
  - Manter testes unitários existentes (não remover)

#### 6.3 Atualizar Documentação de Testes

- **Descrição:** Atualizar documentação com novos padrões e estratégia
- **Critérios de Aceite:**
  - Deve atualizar `docs/testing/strategy.md` com seção sobre testes de integração reais
  - Deve documentar quando usar mocks vs API real
  - Deve atualizar `docs/testing/inventory.md` com testes removidos/adicionados

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

**Objetivo:** Integrar componentes de backend já implementados (SnapshotManager, ProgressTracker) com interface web para completar ciclo de persistência silenciosa e feedback visual de progresso.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Nenhuma (pode ser desenvolvido em paralelo com outros épicos)

**Consulte:**
- `docs/architecture/snapshot_strategy.md` - Estratégia de snapshots
- `docs/interface/web/components.md` (seção 3.6) - Painel Progress

### Funcionalidades sugeridas (não refinadas - requer sessão de refinamento):

#### 9.1 Integrar SnapshotManager no Orquestrador

- **Descrição:** Integrar SnapshotManager no fluxo conversacional para criar snapshots automáticos quando argumento amadurece.

#### 9.2 Exibir ProgressTracker como painel flutuante

- **Descrição:** Exibir ProgressTracker como painel flutuante/fixo na borda direita do chat, mostrando checklist de progresso sincronizado com modelo cognitivo.

#### 9.3 Sincronizar checklist com modelo cognitivo em tempo real

- **Descrição:** Sincronizar checklist do ProgressTracker com modelo cognitivo em tempo real, atualizando status conforme argumento evolui.

#### 9.4 Indicador de solidez na seção de contexto

- **Descrição:** Mostrar indicador de solidez da ideia na seção "💡 Contexto" do painel direito.
- **Critérios de Aceite:**
  - Deve calcular solidez baseado em modelo cognitivo (solid_grounds, evidências, etc)
  - Deve exibir indicador visual (ex: barra de progresso ou badge)
  - Deve atualizar em tempo real conforme argumento evolui
  - Deve estar integrado com SnapshotManager (quando argumento amadurece)

#### 9.5 Associação automática de ideia ao iniciar chat da página de ideia

- **Descrição:** Quando usuário clica "🔄 Continuar explorando" na página de detalhes da ideia, o chat deve iniciar automaticamente com a ideia associada e exibida na seção "💡 Contexto".
- **Critérios de Aceite:**
  - Deve preservar `active_idea_id` entre navegação de páginas (usar query params ou session_state persistente)
  - Deve exibir ideia na seção de contexto imediatamente ao carregar chat
  - Deve funcionar mesmo após refresh da página (persistência)
  - Deve limpar associação quando usuário cria nova conversa

#### 9.x Checklist de Progresso na UI

- **Descrição:** Exibir checklist visual no header do chat sincronizado com modelo cognitivo.
- **Critérios de Aceite:**
  - Deve mostrar bolinhas no header: [⚪⚪🟡⚪⚪] (clicável para expandir)
  - Deve usar status: ⚪ pendente 🟡 em progresso 🟢 completo
  - Deve adaptar checklist conforme tipo de artigo (empírico vs revisão vs teórico)
  - Deve sincronizar com modelo cognitivo (claim → escopo ✓, premises → população ✓, etc)
  - Deve mostrar minimizado por padrão (expandir ao clicar)

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
