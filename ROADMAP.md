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

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

#### Planejados (refinados)
- _Nenhum épico refinado pendente_

#### Planejados (não refinados)
- **ÉPICO 6**: Qualidade de Testes - LLM-as-Judge (não refinado)
- **ÉPICO 7**: Integração Backend↔Frontend (não refinado)
- **ÉPICO 8**: Conceitos (não refinado)
- **ÉPICO 9**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 10**: Pesquisador (não refinado)
- **ÉPICO 11**: Escritor (não refinado)

**Nota sobre Dependências:**
- Épicos 1, 2, 3, 4, 5 concluídos (independentes)
- Épico 6 depende do Épico 1 (valida comportamento de convergência) - Épico 1 já concluído
- Épicos 7-11 seguem sequência: Integração → Conceitos → Ontologia → Pesquisador → Escritor

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 5: UX Polish

**Objetivo:** Ajustes de experiência do usuário: custo em R$.

**Status:** ✅ Concluído

**Dependências:** Épicos 3-4 (métricas movidas para Contexto)

### Funcionalidades:

#### 5.1 Custo em R$ ✅

- **Descrição:** Exibir custos em reais (BRL) com formato brasileiro
- **Implementação:**
  - ✅ Criado `utils/currency.py` com `format_currency()` para conversão USD→BRL
  - ✅ Configs em `.env.example`: `CURRENCY=BRL`, `USD_TO_BRL_RATE=5.5`
  - ✅ Formato brasileiro: "R$ 0,02" (vírgula decimal)
  - ✅ Fallback para USD se `CURRENCY` não for `BRL`
  - ✅ Aplicado em: chat_history, backstage, dashboard
  - ✅ 22 testes unitários em `tests/unit/test_currency.py`

---

## ÉPICO 6: Melhorar Testes - Integração Real + Validação de Qualidade

**Objetivo:** Resolver débito técnico: adicionar testes de integração reais onde há mocks superficiais e validação de qualidade conversacional com LLM-as-Judge.

**Status:** ⏳ Planejado (não refinado)

**Problema:**
- Testes com mocks superficiais não validam comportamento real (`test_orchestrator.py`, `test_structurer.py`)
- Testes verificam apenas presença de campos, não qualidade
- Comportamento socrático impossível de testar deterministicamente
- Asserts fracos aceitam qualquer resultado válido

**Dependências:**
- Épico 1 (comportamento a ser testado precisa existir)

**Consulte:**
- `docs/testing/epic6_refactoring_plan.md` - **Plano detalhado** (ações específicas, código exemplo)
- `docs/analysis/llm_judge_strategy.md` - Análise completa de estratégia e candidatos prioritários
- `docs/testing/strategy.md` - Estratégia de testes e boas práticas

### Funcionalidades:

#### 6.1 Adicionar Testes de Integração Reais

- **Descrição:** Adicionar testes de integração com API real onde há mocks superficiais.
- **Critérios de Aceite:**
  - `test_orchestrator.py` - Adicionar testes de integração em `tests/integration/test_orchestrator_integration.py` (classificação real, routing real)
  - `test_structurer.py` - Adicionar testes de integração em `tests/integration/test_structurer_integration.py` (estruturação real)
  - Testes devem usar API real (não mocks)
  - Testes devem validar comportamento real (não apenas estrutura)
  - Manter testes unitários existentes (validam estrutura, mocks são OK para isso)

#### 6.2 Infraestrutura LLM-as-Judge

- **Descrição:** Criar infraestrutura base para testes com LLM-as-judge.
- **Critérios de Aceite:**
  - Deve criar fixture `llm_judge` em `tests/conftest.py` (modelo Haiku, temperature=0)
  - Deve criar prompts de avaliação em `utils/test_prompts.py` (5 prompts: socrático, conversação, fluidez, integração, refinamento)
  - Deve criar função `extract_score` em `utils/test_helpers.py` (extrai score 1-5 da avaliação)
  - Deve adicionar marker `@pytest.mark.llm_judge` em `pytest.ini`
  - Deve pular testes se `ANTHROPIC_API_KEY` não estiver definida

#### 6.3 Adicionar Validação de Qualidade (6 arquivos)

- **Descrição:** Adicionar validação LLM-as-judge nos testes críticos identificados.
- **Critérios de Aceite:**
  - `test_multi_agent_smoke.py` - Adicionar validação de qualidade conversacional (fluidez, integração)
  - `test_methodologist_smoke.py` - Adicionar validação de perguntas socráticas (não burocráticas)
  - `validate_socratic_behavior.py` - Adicionar validação de provocação socrática genuína
  - `validate_conversation_flow.py` - Adicionar validação de fluidez (sem "Posso chamar X?")
  - `validate_multi_agent_flow.py` - Adicionar validação de integração natural entre agentes
  - `validate_refinement_loop.py` - Adicionar validação de refinamento significativo
  - Cada teste deve validar qualidade (score >= 4) além de estrutura

#### 6.4 Documentação

- **Descrição:** Documentar estratégia e custos de testes melhorados.
- **Critérios de Aceite:**
  - Deve atualizar `docs/testing/strategy.md` com seção sobre testes de integração reais e LLM-as-Judge
  - Deve documentar custos estimados (~$0.01-0.02 por execução completa com LLM-as-Judge)
  - Deve documentar estratégia de execução (local: `pytest -m integration`, `pytest -m llm_judge`)

**Custo estimado:** ~$0.01-0.02 por execução completa (testes de integração + LLM-as-Judge)

---

## ÉPICO 7: Integração Backend↔Frontend

**Objetivo:** Integrar componentes de backend já implementados (SnapshotManager, ProgressTracker) com interface web para completar ciclo de persistência silenciosa e feedback visual de progresso.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Nenhuma (pode ser desenvolvido em paralelo com outros épicos)

**Consulte:**
- `docs/architecture/snapshot_strategy.md` - Estratégia de snapshots
- `docs/interface/web/components.md` (seção 3.6) - Painel Progress

### Funcionalidades sugeridas (não refinadas - requer sessão de refinamento):

#### 7.1 Integrar SnapshotManager no Orquestrador

- **Descrição:** Integrar SnapshotManager no fluxo conversacional para criar snapshots automáticos quando argumento amadurece.

#### 7.2 Exibir ProgressTracker como painel flutuante

- **Descrição:** Exibir ProgressTracker como painel flutuante/fixo na borda direita do chat, mostrando checklist de progresso sincronizado com modelo cognitivo.

#### 7.3 Sincronizar checklist com modelo cognitivo em tempo real

- **Descrição:** Sincronizar checklist do ProgressTracker com modelo cognitivo em tempo real, atualizando status conforme argumento evolui.

#### 7.4 Indicador de solidez na seção de contexto

- **Descrição:** Mostrar indicador de solidez da ideia na seção "💡 Contexto" do painel direito.
- **Critérios de Aceite:**
  - Deve calcular solidez baseado em modelo cognitivo (solid_grounds, evidências, etc)
  - Deve exibir indicador visual (ex: barra de progresso ou badge)
  - Deve atualizar em tempo real conforme argumento evolui
  - Deve estar integrado com SnapshotManager (quando argumento amadurece)

#### 7.5 Associação automática de ideia ao iniciar chat da página de ideia

- **Descrição:** Quando usuário clica "🔄 Continuar explorando" na página de detalhes da ideia, o chat deve iniciar automaticamente com a ideia associada e exibida na seção "💡 Contexto".
- **Critérios de Aceite:**
  - Deve preservar `active_idea_id` entre navegação de páginas (usar query params ou session_state persistente)
  - Deve exibir ideia na seção de contexto imediatamente ao carregar chat
  - Deve funcionar mesmo após refresh da página (persistência)
  - Deve limpar associação quando usuário cria nova conversa

#### 7.x Checklist de Progresso na UI

- **Descrição:** Exibir checklist visual no header do chat sincronizado com modelo cognitivo.
- **Critérios de Aceite:**
  - Deve mostrar bolinhas no header: [⚪⚪🟡⚪⚪] (clicável para expandir)
  - Deve usar status: ⚪ pendente 🟡 em progresso 🟢 completo
  - Deve adaptar checklist conforme tipo de artigo (empírico vs revisão vs teórico)
  - Deve sincronizar com modelo cognitivo (claim → escopo ✓, premises → população ✓, etc)
  - Deve mostrar minimizado por padrão (expandir ao clicar)

---

## ÉPICO 8: Conceitos

**Objetivo:** Criar entidade Concept com vetores semânticos para busca por similaridade ("produtividade" encontra "eficiência").

**Status:** ⏳ Planejado (não refinado)

> **📖 Filosofia:** Conceitos são essências globais (biblioteca única). Ideias referenciam conceitos, não os possuem. Ver `docs/architecture/ontology.md`.

**Dependências:**
- Épico 7

**Consulte:**
- `docs/architecture/concept_model.md` - Schema técnico de Concept
- `docs/architecture/tech_stack.md` - ChromaDB, embeddings, sentence-transformers
- `docs/architecture/ontology.md` - Filosofia: Conceitos como essências globais

### Funcionalidades:

#### 8.1 Setup ChromaDB Local [POC]

- **Descrição:** Configurar ChromaDB para armazenar vetores semânticos de conceitos (gratuito, local).
- **Critérios de Aceite:**
  - Deve instalar dependências: `chromadb`, `sentence-transformers`
  - Deve criar cliente persistente: `chromadb.PersistentClient(path="./data/chroma")`
  - Deve criar collection: `concepts` (metadata: label, essence, variations)
  - Deve usar modelo: `all-MiniLM-L6-v2` (384 dim, 80MB download)

#### 8.2 Schema SQLite de Concept [POC]

- **Descrição:** Criar tabelas `concepts` e `idea_concepts` para metadados estruturados e relacionamento N:N.
- **Critérios de Aceite:**
  - Deve criar tabela `concepts`: id, label, essence, variations JSON, chroma_id
  - Deve criar tabela `idea_concepts`: idea_id, concept_id (N:N, PK composta)
  - Campo `chroma_id` deve referenciar registro no ChromaDB
  - Deve criar índices: ON label, ON idea_id, ON concept_id
  - Conceitos são globais (biblioteca única), ideias referenciam via `idea_concepts`

#### 8.3 Pipeline de Detecção de Conceitos [POC]

- **Descrição:** LLM extrai conceitos-chave quando argumento amadurece (ao criar snapshot de Idea) e salva em ChromaDB + SQLite.
- **Critérios de Aceite:**
  - Deve disparar detecção ao criar snapshot de Idea (quando argumento amadurece)
  - Deve detectar conceitos via LLM (prompt: "Extrair conceitos-chave desta ideia/argumento")
  - Deve gerar embedding via sentence-transformers
  - Deve salvar no ChromaDB (vetor) + SQLite (metadata)
  - Deve criar registro em `idea_concepts` (linking N:N)
  - **Não** deve executar detecção a cada mensagem (apenas no snapshot)

#### 8.4 Busca Semântica [POC]

- **Descrição:** Buscar conceitos similares via embeddings (threshold > 0.80 = mesmo conceito).
- **Critérios de Aceite:**
  - Deve implementar: `find_similar_concepts(query: str, top_k: int) -> list[Concept]`
  - Deve calcular similaridade cosseno entre embeddings
  - Deve usar threshold 0.80 para deduplicação ("produtividade" = "eficiência")
  - Deve retornar lista ordenada por similaridade

#### 8.5 Variations Automáticas [Protótipo]

- **Descrição:** Sistema detecta variações linguísticas e adiciona ao Concept existente (colaboração = cooperação) com thresholds diferenciados.
- **Critérios de Aceite:**
  - Deve detectar variações via busca semântica durante detecção de conceitos
  - **Threshold > 0.90:** adicionar variation automaticamente ao Concept existente
  - **Threshold 0.80-0.90:** perguntar ao usuário: "São o mesmo conceito?" (colaboração = cooperação?)
  - Deve adicionar variation ao Concept existente se confirmado
  - Deve criar novo Concept se usuário rejeitar ou similaridade < 0.80

#### 8.6 Mostrar Conceitos na Interface [Protótipo]

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

## ÉPICO 9: Alinhamento de Ontologia

**Objetivo:** Migrar código atual (premises/assumptions como strings separadas) para nova ontologia (Proposição unificada com solidez derivada de Evidências).

**Status:** ⏳ Planejado (não refinado)

**Abordagem:** Evolução gradual, não refatoração big-bang.

**Dependências:**
- Épicos 7-8 concluídos

**Referências:**
- `docs/architecture/ontology.md` - Nova ontologia
- `docs/vision/epistemology.md` - Fundamentos epistemológicos

---

## ÉPICO 10: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 9

---

## ÉPICO 11: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 7

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
