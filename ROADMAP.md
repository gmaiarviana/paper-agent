# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/vision/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Concluídos
- Infraestrutura base completa

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

#### Planejados (refinados)
- **ÉPICO 1**: Convergência Orgânica (refinado)
- **ÉPICO 2**: Sidebar (refinado)
- **ÉPICO 3**: Bastidores (refinado)
- **ÉPICO 4**: Contexto (refinado)
- **ÉPICO 5**: UX Polish (refinado)

#### Planejados (não refinados)
- **ÉPICO 6**: Qualidade de Testes - LLM-as-Judge (não refinado)
- **ÉPICO 7**: Integração Backend↔Frontend (não refinado)
- **ÉPICO 8**: Conceitos (não refinado)
- **ÉPICO 9**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 10**: Pesquisador (não refinado)
- **ÉPICO 11**: Escritor (não refinado)

**Nota sobre Dependências:**
- Épicos 1, 2, 3, 4 podem ser desenvolvidos em paralelo (independentes)
- Épico 5 depende dos Épicos 3-4 (usa nova estrutura de Contexto/Bastidores)
- Épico 6 depende do Épico 1 (valida comportamento de convergência)
- Épicos 7-11 seguem sequência: Integração → Conceitos → Ontologia → Pesquisador → Escritor

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 1: Convergência Orgânica

**Objetivo:** Sistema transiciona entre agentes de forma fluida, sem pedir permissão. Orquestrador atua como "mente observadora" que sintetiza trabalho dos agentes em resposta coesa.

**Status:** ⏳ Planejado (refinado)

**Problema atual:**
- Orquestrador pergunta "Posso chamar X?" e aguarda confirmação
- CLI bloqueia fluxo pedindo input do usuário
- Usuário não vê valor do sistema multi-agente

**Comportamento desejado:**
- Agentes trabalham automaticamente quando contexto suficiente
- Orquestrador faz curadoria da resposta final (tom único)
- Transparência nos bastidores (quem trabalhou), não na conversa principal
- Usuário confirma entendimento, não permissão

**Dependências:**
- Nenhuma

**Consulte:**
- `docs/vision/conversation_patterns.md` - Padrões de conversação
- `docs/orchestration/conversational_orchestrator/` - Spec do Orquestrador
- `docs/analysis/transicao_fluida_impacto.md` - Análise de impacto completa

### Funcionalidades:

#### 1.1 Ajustar Prompts do Orquestrador

**Descrição:** Modificar `ORCHESTRATOR_MVP_PROMPT_V1` e `ORCHESTRATOR_SOCRATIC_PROMPT_V1` para chamar agentes automaticamente.

**Critérios de Aceite:**
- Deve remover instruções de "sugerir agente e aguardar confirmação"
- Deve adicionar instrução: "Quando contexto suficiente, CHAME o agente automaticamente"
- Deve adicionar instrução de curadoria: "Apresente resultado como se fosse você, em tom coeso"
- Deve manter comportamento socrático (provocação, detecção de suposições)
- Deve atualizar exemplos de output para mostrar transição fluida

#### 1.2 Remover Confirmação Manual no CLI

**Descrição:** Remover bloco de confirmação em `cli/chat.py` (linhas 288-298) que bloqueia transições automáticas.

**Critérios de Aceite:**
- Deve remover prompt "Você quer que eu chame este agente? (sim/não)"
- Deve chamar agente automaticamente quando `next_step == "suggest_agent"`
- Deve exibir transparência nos bastidores: "[Bastidores: Estruturador trabalhou]"
- Deve exibir resposta curada do Orquestrador

#### 1.3 Garantir Curadoria Funciona

**Descrição:** Verificar que Orquestrador recebe resultado do agente e apresenta resposta sintetizada.

**Critérios de Aceite:**
- Após agente trabalhar, Orquestrador deve receber estado atualizado
- Orquestrador deve apresentar resultado em tom único (não "O Estruturador disse X")
- Deve confirmar entendimento: "Organizei sua ideia: [resultado]. Isso captura o que você quer?"
- Fluxo: Orquestrador → Agente → Orquestrador (curadoria) → Usuário

#### 1.4 Atualizar Testes

**Descrição:** Atualizar testes para verificar transição automática.

**Critérios de Aceite:**
- Deve atualizar `tests/unit/test_orchestrator.py` (remover asserts de "Posso chamar")
- Deve atualizar `scripts/flows/validate_conversation_flow.py`
- Deve adicionar teste que verifica chamada automática quando contexto suficiente
- Deve adicionar teste que verifica curadoria

---

## ÉPICO 2: Sidebar

**Objetivo:** Simplificar sidebar para navegação limpa, apenas links para páginas.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Nenhuma

### Funcionalidades:

#### 2.1 Links de navegação

- **Descrição:** Sidebar com links para páginas dedicadas e botão de nova conversa
- **Critérios de Aceite:**
  - Deve exibir link "📖 Pensamentos" → `/pensamentos`
  - Deve exibir link "🏷️ Catálogo" → `/catalogo` (desabilitado se não implementado)
  - Deve exibir link "💬 Conversas" → `/historico` (página de histórico)
  - Deve exibir botão "+ Nova conversa" → inicia chat novo
  - Links com ícones, sem header/logo

---

## ÉPICO 3: Bastidores

**Objetivo:** Reorganizar bastidores com cards de pensamento e timeline, atualizando em tempo real.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Nenhuma

### Funcionalidades:

#### 3.1 Remover toggle "Ver raciocínio"

- **Descrição:** Bastidores sempre visíveis como seção colapsável, sem toggle separado
- **Critérios de Aceite:**
  - Deve remover toggle "🔍 Ver raciocínio"
  - Bastidores visíveis como seção colapsável (header clicável)
  - Usuário expande/colapsa clicando no header "📊 Bastidores"

#### 3.2 Card de pensamento atual

- **Descrição:** Card mostrando output user-friendly do agente ativo
- **Critérios de Aceite:**
  - Deve mostrar emoji + nome do agente (🎯 Orquestrador, 📝 Estruturador, 🔬 Metodologista)
  - Deve mostrar pensamento resumido (~280 chars)
  - Deve ter link "Ver completo" → abre modal com raciocínio completo
  - Estado vazio: mostrar 🤖 + "Aguardando..." centralizado

#### 3.3 Card de timeline

- **Descrição:** Card mostrando histórico de contribuições dos agentes
- **Critérios de Aceite:**
  - Deve mostrar últimos 3 agentes (atual + 2 anteriores)
  - Formato: lista simples com emoji + nome + resumo + horário
  - Deve ter link "Ver histórico" → abre modal com lista completa
  - MVP: lista simples. Timeline visual é evolução futura.

#### 3.4 Indicador de novidade

- **Descrição:** Indicador sutil quando há atualização nos bastidores
- **Critérios de Aceite:**
  - Deve mostrar indicador no header quando há novidade (🔴 ou "(+2)")
  - Indicador some quando usuário expande bastidores
  - Não expande automaticamente (não distrai usuário)

---

## ÉPICO 4: Contexto

**Objetivo:** Nova seção acima dos bastidores mostrando ideia ativa e informações da conversa.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Nenhuma (pode ser paralelo aos Épicos 2 e 3)

### Funcionalidades:

#### 4.1 Seção de contexto

- **Descrição:** Seção colapsável acima dos bastidores no painel direito
- **Critérios de Aceite:**
  - Deve ter header "💡 Contexto" clicável para expandir/colapsar
  - Posicionada acima dos Bastidores no painel direito

#### 4.2 Ideia ativa

- **Descrição:** Mostrar informações da ideia sendo trabalhada
- **Critérios de Aceite:**
  - Deve mostrar título da ideia
  - Deve mostrar status (🔍 Explorando | 📝 Estruturada | ✅ Validada)
  - Deve mostrar indicador de solidez (quando disponível)
  - Estado vazio: seção em branco (não mostrar nada até ter ideia)
  - Atualiza em tempo real quando ideia é associada/atualizada
  - Se chat iniciado a partir de página de ideia → já começa com ideia associada

#### 4.3 Custo acumulado

- **Descrição:** Mostrar custo total da conversa na seção de contexto
- **Critérios de Aceite:**
  - Deve mostrar custo acumulado (ex: "💰 R$ 0,15 total")
  - Clicável para ver detalhes (tokens, modelo usado)
  - Atualiza a cada mensagem

#### 4.4 Modal de detalhes

- **Descrição:** Modal para ver detalhes expandidos do contexto
- **Critérios de Aceite:**
  - Abre ao clicar no custo ou botão "expandir"
  - Deve mostrar: ideia completa, custo detalhado por mensagem, modelo usado, total de tokens

---

## ÉPICO 5: UX Polish

**Objetivo:** Ajustes de experiência do usuário: input de chat, métricas discretas, custo em R$.

**Status:** ⏳ Planejado (refinado)

**Dependências:** Épicos 3-4 (métricas movidas para Contexto)

### Funcionalidades:

#### 5.1 Enter envia mensagem

- **Descrição:** Usar componente nativo do Streamlit para input de chat
- **Critérios de Aceite:**
  - Deve usar `st.chat_input` (componente nativo)
  - Enter envia mensagem (comportamento padrão)

#### 5.2 Métricas discretas

- **Descrição:** Métricas por mensagem discretas, visíveis sob demanda
- **Critérios de Aceite:**
  - Deve mostrar ícone pequeno (ℹ️) após cada mensagem do sistema
  - Clique no ícone abre popover/tooltip com métricas
  - Formato: "💰 R$0,02 · 215 tokens · 1.2s"
  - Não mostra métricas sempre visíveis (reduz ruído visual)

#### 5.3 Custo em R$

- **Descrição:** Exibir custos em reais (BRL) ao invés de dólares
- **Critérios de Aceite:**
  - Deve converter USD → BRL usando taxa configurável
  - Deve adicionar config em `.env`: `CURRENCY=BRL`, `USD_TO_BRL_RATE=5.5`
  - Deve exibir: "R$ 0,02" ao invés de "$0.0039"
  - Fallback para USD se config não existir

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
