# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/vision/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Concluídos
- **ÉPICO 9**: Interface Web Conversacional - Chat conversacional, painel Bastidores em tempo real, integração LangGraph SqliteSaver
- **ÉPICO 10**: Orquestrador Socrático - Diálogo socrático para explorar e estruturar ideias, gerenciamento de transições entre agentes
- **ÉPICO 11**: Modelagem Cognitiva - Modelo cognitivo explícito (Argument), persistência SQLite, versionamento automático, detecção de maturidade via LLM
- **ÉPICO 12**: Gestão de Ideias - Sistema completo de gestão de ideias com listagem, alternância, busca, criação, explorador de argumentos e inferência automática de status
- **ÉPICO 14**: Navegação em Três Espaços - Separação de conversas/pensamentos/catálogo, páginas dedicadas, restauração de contexto, feedback visual forte

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados
- **ÉPICO 13**: Entidade Concept (refinado)
- **ÉPICO 15**: Integração Backend↔Frontend (não refinado)
- **ÉPICO 16**: Polimentos de UX (não refinado)
- **ÉPICO 17**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)
- **ÉPICO 18**: Personas de Agentes (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 13: Entidade Concept

**Objetivo:** Criar entidade Concept com vetores semânticos para busca por similaridade ("produtividade" encontra "eficiência").

**Status:** ⏳ Planejado (refinado)

> **📖 Filosofia:** Conceitos são essências globais (biblioteca única). Ideias referenciam conceitos, não os possuem. Ver `docs/architecture/ontology.md`.

**Dependências:**
- ✅ Épico 12 concluído (Idea existe como entidade)

**Consulte:**
- `docs/architecture/concept_model.md` - Schema técnico de Concept
- `docs/architecture/tech_stack.md` - ChromaDB, embeddings, sentence-transformers
- `docs/architecture/ontology.md` - Filosofia: Conceitos como essências globais

### Funcionalidades:

#### 13.1 Setup ChromaDB Local [POC]

- **Descrição:** Configurar ChromaDB para armazenar vetores semânticos de conceitos (gratuito, local).
- **Critérios de Aceite:**
  - Deve instalar dependências: `chromadb`, `sentence-transformers`
  - Deve criar cliente persistente: `chromadb.PersistentClient(path="./data/chroma")`
  - Deve criar collection: `concepts` (metadata: label, essence, variations)
  - Deve usar modelo: `all-MiniLM-L6-v2` (384 dim, 80MB download)

#### 13.2 Schema SQLite de Concept [POC]

- **Descrição:** Criar tabelas `concepts` e `idea_concepts` para metadados estruturados e relacionamento N:N.
- **Critérios de Aceite:**
  - Deve criar tabela `concepts`: id, label, essence, variations JSON, chroma_id
  - Deve criar tabela `idea_concepts`: idea_id, concept_id (N:N, PK composta)
  - Campo `chroma_id` deve referenciar registro no ChromaDB
  - Deve criar índices: ON label, ON idea_id, ON concept_id
  - Conceitos são globais (biblioteca única), ideias referenciam via `idea_concepts`

#### 13.3 Pipeline de Detecção de Conceitos [POC]

- **Descrição:** LLM extrai conceitos-chave quando argumento amadurece (ao criar snapshot de Idea) e salva em ChromaDB + SQLite.
- **Critérios de Aceite:**
  - Deve disparar detecção ao criar snapshot de Idea (quando argumento amadurece)
  - Deve detectar conceitos via LLM (prompt: "Extrair conceitos-chave desta ideia/argumento")
  - Deve gerar embedding via sentence-transformers
  - Deve salvar no ChromaDB (vetor) + SQLite (metadata)
  - Deve criar registro em `idea_concepts` (linking N:N)
  - **Não** deve executar detecção a cada mensagem (apenas no snapshot)

#### 13.4 Busca Semântica [POC]

- **Descrição:** Buscar conceitos similares via embeddings (threshold > 0.80 = mesmo conceito).
- **Critérios de Aceite:**
  - Deve implementar: `find_similar_concepts(query: str, top_k: int) -> list[Concept]`
  - Deve calcular similaridade cosseno entre embeddings
  - Deve usar threshold 0.80 para deduplicação ("produtividade" = "eficiência")
  - Deve retornar lista ordenada por similaridade

#### 13.5 Variations Automáticas [Protótipo]

- **Descrição:** Sistema detecta variações linguísticas e adiciona ao Concept existente (colaboração = cooperação) com thresholds diferenciados.
- **Critérios de Aceite:**
  - Deve detectar variações via busca semântica durante detecção de conceitos
  - **Threshold > 0.90:** adicionar variation automaticamente ao Concept existente
  - **Threshold 0.80-0.90:** perguntar ao usuário: "São o mesmo conceito?" (colaboração = cooperação?)
  - Deve adicionar variation ao Concept existente se confirmado
  - Deve criar novo Concept se usuário rejeitar ou similaridade < 0.80

#### 13.6 Mostrar Conceitos na Interface [Protótipo]

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

## ÉPICO 14: Navegação em Três Espaços

**Objetivo:** Separar navegação em três espaços distintos (Conversas, Meus Pensamentos, Catálogo) com feedback visual forte durante processamento.

**Status:** ✅ Concluído

**Dependências:**
- ✅ Épico 12 concluído (entidades Idea + Argument existem)

**Consulte:**
- `docs/interface/navigation_philosophy.md` - Filosofia de navegação
- `docs/interface/web.md` - Especificação técnica completa

**Funcionalidades Implementadas:**
- ✅ Sidebar com conversas recentes (últimas 5) e botões de navegação
- ✅ Página `/pensamentos` com grid de cards de ideias cristalizadas
- ✅ Página `/pensamentos/{idea_id}` com detalhes completos (argumentos, conceitos, conversas)
- ✅ Feedback visual forte durante processamento (input desabilitado + barra inline dinâmica)
- ✅ Restauração de contexto ao alternar conversas (bugfix crítico)

---

## ÉPICO 15: Integração Backend↔Frontend

**Objetivo:** Integrar componentes de backend já implementados (SnapshotManager, ProgressTracker) com interface web para completar ciclo de persistência silenciosa e feedback visual de progresso.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 11 concluído (SnapshotManager implementado)
- ✅ Épico 14 concluído (Interface web existe)

**Consulte:**
- `docs/architecture/snapshot_strategy.md` - Estratégia de snapshots
- `docs/interface/web.md` (seção 3.4) - Painel Progress

### Funcionalidades sugeridas (não refinadas - requer sessão de refinamento):

#### 15.1 Integrar SnapshotManager no Orquestrador

- **Descrição:** Integrar SnapshotManager no fluxo conversacional para criar snapshots automáticos quando argumento amadurece.

#### 15.2 Exibir ProgressTracker como painel flutuante

- **Descrição:** Exibir ProgressTracker como painel flutuante/fixo na borda direita do chat, mostrando checklist de progresso sincronizado com modelo cognitivo.

#### 15.3 Sincronizar checklist com modelo cognitivo em tempo real

- **Descrição:** Sincronizar checklist do ProgressTracker com modelo cognitivo em tempo real, atualizando status conforme argumento evolui.

---

## ÉPICO 16: Polimentos de UX

**Objetivo:** Polimento de interface web baseado em feedbacks do usuário (Enter envia, custo em R$, métricas discretas).

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)
- ✅ Épico 14 concluído (Navegação em Três Espaços)

**Consulte:**
- `docs/interface/web.md` - Especificação de interface completa

### Funcionalidades:

#### 16.1 Enter Envia, Ctrl+Enter Pula Linha

- **Descrição:** Textarea com comportamento padrão (Enter envia, Ctrl+Enter pula linha).
- **Critérios de Aceite:**
  - Enter deve submeter form (enviar mensagem)
  - Ctrl+Enter deve inserir `\n` (pular linha)
  - Deve seguir padrão Claude.ai/ChatGPT
  - Deve funcionar cross-browser (Chrome, Firefox, Safari)

#### 16.2 Custo em R$

- **Descrição:** Exibir custos em reais (BRL) ao invés de dólares (USD).
- **Critérios de Aceite:**
  - Deve converter USD → BRL (taxa fixa ou API de câmbio)
  - Deve exibir: "R$ 0,02" ao invés de "$0.0039"
  - Deve adicionar config em `.env`: `CURRENCY=BRL`, `USD_TO_BRL_RATE=5.2`
  - Deve permitir fallback para USD se conversão falhar

#### 15.3 Métricas Inline Mais Discretas

- **Descrição:** Tornar métricas inline (tokens, custo, tempo) mais discretas visualmente.
- **Critérios de Aceite:**
  - Deve reduzir tamanho fonte para 0.75rem
  - Deve usar cor cinza claro (#94a3b8)
  - Deve posicionar no canto inferior direito da mensagem
  - Deve manter formato: "💰 R$0.02 · 215 tokens · 1.2s"

#### 16.4 Timeline Colapsada por Padrão

- **Descrição:** Bastidores com timeline de agentes anteriores colapsada inicialmente.
- **Critérios de Aceite:**
  - Deve mostrar seção "📈 Timeline" colapsada por padrão
  - Deve ter ícone: ▶ (colapsado) / ▼ (expandido)
  - Deve expandir ao clicar (mostrar histórico de agentes)
  - Deve persistir estado (colapsado/expandido) durante sessão

#### 16.5 Botão "Copiar Raciocínio"

- **Descrição:** Modal de raciocínio completo com botão para copiar texto.
- **Critérios de Aceite:**
  - Deve adicionar botão "📋 Copiar" no modal de raciocínio
  - Deve copiar texto markdown para clipboard
  - Deve mostrar feedback visual: "✓ Copiado!" (2s)
  - Deve funcionar cross-browser (clipboard API)

#### 16.6 Checklist de Progresso no Header

- **Descrição:** Exibir checklist visual no header do chat sincronizado com modelo cognitivo.
- **Critérios de Aceite:**
  - Deve mostrar bolinhas no header: [⚪⚪🟡⚪⚪] (clicável para expandir)
  - Deve usar status: ⚪ pendente 🟡 em progresso 🟢 completo
  - Deve adaptar checklist conforme tipo de artigo (empírico vs revisão vs teórico)
  - Deve sincronizar com modelo cognitivo (claim → escopo ✓, premises → população ✓, etc)
  - Deve mostrar minimizado por padrão (expandir ao clicar)

---

## ÉPICO 17: Agentes Avançados

**Objetivo:** Expandir sistema com agentes especializados para pesquisa, redação e revisão de artigos científicos.

**Status:** ⏳ Planejado (não refinado)

**Agentes Planejados:**
- **Pesquisador**: Busca e análise de literatura científica
- **Escritor**: Redação de seções do artigo
- **Crítico**: Revisão e feedback construtivo

**Consulte:** `docs/agents/overview.md` para mapa completo de agentes planejados.

---

## ÉPICO 18: Personas de Agentes

**Objetivo:** Permitir customização de agentes como "personas" (Sócrates, Aristóteles, Popper) com estilos de argumentação personalizados, transformando agentes em "mentores" que usuário pode escolher e treinar.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)
- ⏳ Épicos 11-16 concluídos (modelo de dados + gestão de ideias + navegação + UX + integração)

**Consulte:** 
- `docs/vision/agent_personas.md` - Visão completa de customização
- `docs/vision/vision.md` (Seção 1.1) - Agentes como diferencial

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
