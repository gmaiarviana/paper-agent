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
- **ÉPICO 1**: Integração Backend↔Frontend (não refinado)
- **ÉPICO 2**: Conceitos (não refinado)
- **ÉPICO 3**: UX Polish (não refinado)
- **ÉPICO 4**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 5**: Pesquisador (não refinado)
- **ÉPICO 6**: Escritor (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 1: Integração Backend↔Frontend

**Objetivo:** Integrar componentes de backend já implementados (SnapshotManager, ProgressTracker) com interface web para completar ciclo de persistência silenciosa e feedback visual de progresso.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Nenhuma

**Consulte:**
- `docs/architecture/snapshot_strategy.md` - Estratégia de snapshots
- `docs/interface/web.md` (seção 3.4) - Painel Progress

### Funcionalidades sugeridas (não refinadas - requer sessão de refinamento):

#### 1.1 Integrar SnapshotManager no Orquestrador

- **Descrição:** Integrar SnapshotManager no fluxo conversacional para criar snapshots automáticos quando argumento amadurece.

#### 1.2 Exibir ProgressTracker como painel flutuante

- **Descrição:** Exibir ProgressTracker como painel flutuante/fixo na borda direita do chat, mostrando checklist de progresso sincronizado com modelo cognitivo.

#### 1.3 Sincronizar checklist com modelo cognitivo em tempo real

- **Descrição:** Sincronizar checklist do ProgressTracker com modelo cognitivo em tempo real, atualizando status conforme argumento evolui.

#### 1.x Checklist de Progresso na UI

- **Descrição:** Exibir checklist visual no header do chat sincronizado com modelo cognitivo.
- **Critérios de Aceite:**
  - Deve mostrar bolinhas no header: [⚪⚪🟡⚪⚪] (clicável para expandir)
  - Deve usar status: ⚪ pendente 🟡 em progresso 🟢 completo
  - Deve adaptar checklist conforme tipo de artigo (empírico vs revisão vs teórico)
  - Deve sincronizar com modelo cognitivo (claim → escopo ✓, premises → população ✓, etc)
  - Deve mostrar minimizado por padrão (expandir ao clicar)

---

## ÉPICO 2: Conceitos

**Objetivo:** Criar entidade Concept com vetores semânticos para busca por similaridade ("produtividade" encontra "eficiência").

**Status:** ⏳ Planejado (não refinado)

> **📖 Filosofia:** Conceitos são essências globais (biblioteca única). Ideias referenciam conceitos, não os possuem. Ver `docs/architecture/ontology.md`.

**Dependências:**
- Épico 1

**Consulte:**
- `docs/architecture/concept_model.md` - Schema técnico de Concept
- `docs/architecture/tech_stack.md` - ChromaDB, embeddings, sentence-transformers
- `docs/architecture/ontology.md` - Filosofia: Conceitos como essências globais

### Funcionalidades:

#### 2.1 Setup ChromaDB Local [POC]

- **Descrição:** Configurar ChromaDB para armazenar vetores semânticos de conceitos (gratuito, local).
- **Critérios de Aceite:**
  - Deve instalar dependências: `chromadb`, `sentence-transformers`
  - Deve criar cliente persistente: `chromadb.PersistentClient(path="./data/chroma")`
  - Deve criar collection: `concepts` (metadata: label, essence, variations)
  - Deve usar modelo: `all-MiniLM-L6-v2` (384 dim, 80MB download)

#### 2.2 Schema SQLite de Concept [POC]

- **Descrição:** Criar tabelas `concepts` e `idea_concepts` para metadados estruturados e relacionamento N:N.
- **Critérios de Aceite:**
  - Deve criar tabela `concepts`: id, label, essence, variations JSON, chroma_id
  - Deve criar tabela `idea_concepts`: idea_id, concept_id (N:N, PK composta)
  - Campo `chroma_id` deve referenciar registro no ChromaDB
  - Deve criar índices: ON label, ON idea_id, ON concept_id
  - Conceitos são globais (biblioteca única), ideias referenciam via `idea_concepts`

#### 2.3 Pipeline de Detecção de Conceitos [POC]

- **Descrição:** LLM extrai conceitos-chave quando argumento amadurece (ao criar snapshot de Idea) e salva em ChromaDB + SQLite.
- **Critérios de Aceite:**
  - Deve disparar detecção ao criar snapshot de Idea (quando argumento amadurece)
  - Deve detectar conceitos via LLM (prompt: "Extrair conceitos-chave desta ideia/argumento")
  - Deve gerar embedding via sentence-transformers
  - Deve salvar no ChromaDB (vetor) + SQLite (metadata)
  - Deve criar registro em `idea_concepts` (linking N:N)
  - **Não** deve executar detecção a cada mensagem (apenas no snapshot)

#### 2.4 Busca Semântica [POC]

- **Descrição:** Buscar conceitos similares via embeddings (threshold > 0.80 = mesmo conceito).
- **Critérios de Aceite:**
  - Deve implementar: `find_similar_concepts(query: str, top_k: int) -> list[Concept]`
  - Deve calcular similaridade cosseno entre embeddings
  - Deve usar threshold 0.80 para deduplicação ("produtividade" = "eficiência")
  - Deve retornar lista ordenada por similaridade

#### 2.5 Variations Automáticas [Protótipo]

- **Descrição:** Sistema detecta variações linguísticas e adiciona ao Concept existente (colaboração = cooperação) com thresholds diferenciados.
- **Critérios de Aceite:**
  - Deve detectar variações via busca semântica durante detecção de conceitos
  - **Threshold > 0.90:** adicionar variation automaticamente ao Concept existente
  - **Threshold 0.80-0.90:** perguntar ao usuário: "São o mesmo conceito?" (colaboração = cooperação?)
  - Deve adicionar variation ao Concept existente se confirmado
  - Deve criar novo Concept se usuário rejeitar ou similaridade < 0.80

#### 2.6 Mostrar Conceitos na Interface [Protótipo]

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

## ÉPICO 3: UX Polish

**Objetivo:** Polimento de interface web baseado em feedbacks do usuário (Enter envia, custo em R$, métricas discretas).

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Nenhuma

**Consulte:**
- `docs/interface/web.md` - Especificação de interface completa

### Funcionalidades:

#### 3.1 Enter Envia, Ctrl+Enter Pula Linha

- **Descrição:** Textarea com comportamento padrão (Enter envia, Ctrl+Enter pula linha).
- **Critérios de Aceite:**
  - Enter deve submeter form (enviar mensagem)
  - Ctrl+Enter deve inserir `\n` (pular linha)
  - Deve seguir padrão Claude.ai/ChatGPT
  - Deve funcionar cross-browser (Chrome, Firefox, Safari)

#### 3.2 Custo em R$

- **Descrição:** Exibir custos em reais (BRL) ao invés de dólares (USD).
- **Critérios de Aceite:**
  - Deve converter USD → BRL (taxa fixa ou API de câmbio)
  - Deve exibir: "R$ 0,02" ao invés de "$0.0039"
  - Deve adicionar config em `.env`: `CURRENCY=BRL`, `USD_TO_BRL_RATE=5.2`
  - Deve permitir fallback para USD se conversão falhar

#### 3.3 Métricas Inline Mais Discretas

- **Descrição:** Tornar métricas inline (tokens, custo, tempo) mais discretas visualmente.
- **Critérios de Aceite:**
  - Deve reduzir tamanho fonte para 0.75rem
  - Deve usar cor cinza claro (#94a3b8)
  - Deve posicionar no canto inferior direito da mensagem
  - Deve manter formato: "💰 R$0.02 · 215 tokens · 1.2s"

#### 3.4 Timeline Colapsada por Padrão

- **Descrição:** Bastidores com timeline de agentes anteriores colapsada inicialmente.
- **Critérios de Aceite:**
  - Deve mostrar seção "📈 Timeline" colapsada por padrão
  - Deve ter ícone: ▶ (colapsado) / ▼ (expandido)
  - Deve expandir ao clicar (mostrar histórico de agentes)
  - Deve persistir estado (colapsado/expandido) durante sessão

#### 3.5 Botão "Copiar Raciocínio"

- **Descrição:** Modal de raciocínio completo com botão para copiar texto.
- **Critérios de Aceite:**
  - Deve adicionar botão "📋 Copiar" no modal de raciocínio
  - Deve copiar texto markdown para clipboard
  - Deve mostrar feedback visual: "✓ Copiado!" (2s)
  - Deve funcionar cross-browser (clipboard API)

---

## ÉPICO 4: Alinhamento de Ontologia

**Objetivo:** Migrar código atual (premises/assumptions como strings separadas) para nova ontologia (Proposição unificada com solidez derivada de Evidências).

**Status:** ⏳ Planejado (não refinado)

**Abordagem:** Evolução gradual, não refatoração big-bang.

**Dependências:**
- Épicos 1-3 concluídos

**Referências:**
- `docs/architecture/ontology.md` - Nova ontologia
- `docs/vision/epistemology.md` - Fundamentos epistemológicos

---

## ÉPICO 5: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 4

---

## ÉPICO 6: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 5

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
