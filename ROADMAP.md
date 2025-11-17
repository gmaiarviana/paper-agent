# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/vision/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Concluídos
- **ÉPICO 9**: Interface Web Conversacional - Interface web com chat conversacional, painel Bastidores em tempo real e integração com LangGraph SqliteSaver.
- **ÉPICO 10**: Orquestrador Socrático - Orquestrador que usa diálogo socrático para explorar e estruturar ideias, gerenciando transições entre agentes.

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados
- **ÉPICO 11**: Modelagem Cognitiva (refinado)
- **ÉPICO 12**: Gestão de Ideias (não refinado)
- **ÉPICO 13**: Entidade Concept (não refinado)
- **ÉPICO 14**: Melhorias de UX (não refinado)
- **ÉPICO 15**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)
- **ÉPICO 16**: Personas de Agentes (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 11: Modelagem Cognitiva

**Objetivo:** Implementar modelo cognitivo explícito (Argument como entidade) com persistência, versionamento e indicadores de maturidade (backend).

**Status:** ✅ Refinado

**Dependências:**
- ✅ Épico 10 concluído (Orquestrador Socrático)
- ✅ Épico 9 concluído (Interface Web + SqliteSaver)

**Consulte:**
- `docs/architecture/argument_model.md` - Schema técnico de Argument
- `docs/vision/cognitive_model.md` - Modelo cognitivo completo

### Funcionalidades:

#### 11.1 Schema Explícito de Argument

- **Descrição:** Criar dataclass/Pydantic `Argument` substituindo dict livre no `MultiAgentState`, com validação automática de campos.
- **Critérios de Aceite:**
  - Deve criar dataclass `Argument` com campos: claim, premises, assumptions, open_questions, contradictions, solid_grounds, context
  - Deve validar campos via Pydantic (type hints + validação)
  - Deve substituir `cognitive_model: dict` por `cognitive_model: Argument` no MultiAgentState
  - SqliteSaver deve continuar salvando no checkpoint (Pydantic serializa automaticamente)

#### 11.2 Setup de Persistência e Schema SQLite

- **Descrição:** Configurar SqliteSaver do LangGraph para checkpoints de conversa + criar schema SQLite completo com tabelas ideas e arguments.
- **Critérios de Aceite:**
  - Deve configurar SqliteSaver do LangGraph (arquivo checkpoints.db)
  - Deve criar tabela ideas: id (UUID PK), title, status, current_argument_id (FK NULLABLE), created_at, updated_at
  - Deve criar tabela arguments: id (UUID PK), idea_id (FK), claim, premises (JSON), assumptions (JSON), open_questions (JSON), contradictions (JSON), solid_grounds (JSON), context (JSON), version (INT), created_at, updated_at
  - Deve criar constraint: FOREIGN KEY (current_argument_id) REFERENCES arguments(id)
  - Deve salvar snapshot quando usuário pausa sessão manualmente

#### 11.3 Versionamento de Argumentos

- **Descrição:** Detectar mudanças significativas de claim e criar nova versão de argumento (V1, V2, V3) automaticamente.
- **Critérios de Aceite:**
  - Deve adicionar campo `version` na tabela arguments (INT, auto-incrementa por idea_id)
  - Deve detectar mudança significativa via LLM (confiança > 80%)
  - Deve criar novo registro ao detectar mudança (não sobrescrever V1)
  - Deve listar histórico de versões: `SELECT * FROM arguments WHERE idea_id = ? ORDER BY version`

#### 11.4 Argumento Focal

- **Descrição:** Gerenciar argumento focal como FK na tabela ideas (já criado na funcionalidade 11.2).
- **Critérios de Aceite:**
  - Campo current_argument_id já existe na tabela ideas (criado na 11.2)
  - Deve UPDATE ideas SET current_argument_id ao criar nova versão de argumento
  - Deve carregar argumento focal via FK simples: SELECT * FROM arguments WHERE id = idea.current_argument_id
  - Deve permitir NULL (idea sem argumento ainda)

#### 11.5 Indicadores de Maturidade

- **Descrição:** Sistema detecta maturidade do argumento (não determinístico) e cria snapshot automaticamente.
- **Critérios de Aceite:**
  - Deve avaliar maturidade a cada turno via LLM
  - Deve usar critérios: claim estável (3+ turnos), premises sólidas (>2), assumptions baixas (<2), open_questions vazias
  - Deve criar snapshot automaticamente ao detectar maturidade (além de pausar manual)
  - Deve notificar usuário: "Argumento amadureceu! Criando V{n}..."

---

## ÉPICO 12: Gestão de Ideias

**Objetivo:** Permitir usuário gerenciar ideias criadas pelo sistema (listar, alternar, buscar, criar nova).

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 11 concluído (Argument existe como entidade)

**Consulte:**
- `docs/interface/web.md` - Especificação de interface completa

### Funcionalidades:

#### 12.1: Mostrar Status da Ideia na Interface

- **Descrição:** Exibir ideia ativa no painel Bastidores com badge visual.
- **Critérios de Aceite:**
  - Deve mostrar: "💡 Ideia Atual: {title}"
  - Deve exibir badge de status: 🔍 Explorando | 📝 Estruturada | ✅ Validada
  - Deve inferir status do modelo cognitivo (não manual)
  - Deve atualizar status em tempo real conforme conversa evolui

#### 12.2: Listar Ideias na Sidebar

- **Descrição:** Sidebar com últimas 10 ideias ordenadas por updated_at DESC.
- **Critérios de Aceite:**
  - Deve listar últimas 10 ideias (ORDER BY updated_at DESC)
  - Deve exibir: título, status badge, # argumentos
  - Deve destacar ideia ativa (bold, background diferente)
  - Deve ser colapsável (toggle on/off)

#### 12.3: Alternar Entre Ideias

- **Descrição:** Clicar em Idea na sidebar carrega contexto completo (thread_id + argumento focal).
- **Critérios de Aceite:**
  - Deve carregar thread_id do LangGraph (SqliteSaver)
  - Deve restaurar argumento focal (current_argument_id)
  - Deve exibir histórico de mensagens da ideia selecionada
  - Deve atualizar Bastidores com contexto da ideia

#### 12.4: Criar Nova Ideia

- **Descrição:** Botão "[+ Nova Ideia]" cria registro vazio e inicia conversa nova.
- **Critérios de Aceite:**
  - Deve criar registro vazio em ideas (título = "Nova Ideia {timestamp}")
  - Deve gerar novo thread_id (LangGraph)
  - Deve redirecionar para chat da nova ideia
  - Deve limpar histórico de mensagens (conversa limpa)

#### 12.5: Explorador de Argumentos (Preview)

- **Descrição:** Ao clicar em Idea na sidebar, expandir e mostrar argumentos versionados (V1, V2, V3).
- **Critérios de Aceite:**
  - Deve expandir argumentos ao clicar em idea
  - Deve listar V1, V2, V3 (versionamento histórico)
  - Deve destacar argumento focal com badge [focal]
  - Deve ter botão "Ver detalhes" → modal com claim, premises, assumptions

#### 12.6: Busca de Ideias

- **Descrição:** Implementar busca de ideias por título ou status.
- **Critérios de Aceite:**
  - Deve buscar por título (LIKE query, case-insensitive)
  - Deve buscar por status (exploring, structured, validated)
  - Deve permitir filtros combinados (título + status)

---

## ÉPICO 13: Entidade Concept

**Objetivo:** Criar entidade Concept com vetores semânticos para busca por similaridade ("produtividade" encontra "eficiência").

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 12 concluído (Gestão de Ideias)

**Consulte:**
- `docs/architecture/concept_model.md` - Schema técnico de Concept
- `docs/architecture/tech_stack.md` - ChromaDB, embeddings, sentence-transformers

### Funcionalidades:

#### 13.1 Setup ChromaDB Local

- **Descrição:** Configurar ChromaDB para armazenar vetores semânticos de conceitos (gratuito, local).
- **Critérios de Aceite:**
  - Deve instalar dependências: `chromadb`, `sentence-transformers`
  - Deve criar cliente persistente: `chromadb.PersistentClient(path="./data/chroma")`
  - Deve criar collection: `concepts` (metadata: label, essence, variations)
  - Deve usar modelo: `all-MiniLM-L6-v2` (384 dim, 80MB download)

#### 13.2 Schema SQLite de Concept

- **Descrição:** Criar tabelas `concepts` e `idea_concepts` para metadados estruturados e relacionamento N:N.
- **Critérios de Aceite:**
  - Deve criar tabela `concepts`: id, label, essence, variations JSON, chroma_id
  - Deve criar tabela `idea_concepts`: idea_id, concept_id (N:N, PK composta)
  - Campo `chroma_id` deve referenciar registro no ChromaDB
  - Deve criar índices: ON label, ON idea_id, ON concept_id

#### 13.3 Pipeline de Detecção de Conceitos

- **Descrição:** LLM extrai conceitos-chave mencionados na conversa e salva em ChromaDB + SQLite.
- **Critérios de Aceite:**
  - Deve detectar conceitos via LLM (prompt: "Extrair conceitos-chave desta conversa")
  - Deve gerar embedding via sentence-transformers
  - Deve salvar no ChromaDB (vetor) + SQLite (metadata)
  - Deve criar registro em idea_concepts (linking)

#### 13.4 Busca Semântica

- **Descrição:** Buscar conceitos similares via embeddings (threshold > 0.80 = mesmo conceito).
- **Critérios de Aceite:**
  - Deve implementar: `find_similar_concepts(query: str, top_k: int) -> list[Concept]`
  - Deve calcular similaridade cosseno entre embeddings
  - Deve usar threshold 0.80 para deduplicação ("produtividade" = "eficiência")
  - Deve retornar lista ordenada por similaridade

#### 13.5 Variations Automáticas

- **Descrição:** Sistema detecta variações linguísticas e adiciona ao Concept existente (colaboração = cooperação).
- **Critérios de Aceite:**
  - Deve detectar variações via busca semântica (similaridade > 0.80)
  - Deve perguntar ao usuário: "São o mesmo conceito?"
  - Deve adicionar variation ao Concept existente se confirmado
  - Deve criar novo Concept se usuário rejeitar

#### 13.6 Mostrar Conceitos na Interface

- **Descrição:** Exibir conceitos detectados no painel Bastidores com busca interativa.
- **Critérios de Aceite:**
  - Deve mostrar seção: "🏷️ Conceitos" (lista de concepts detectados)
  - Deve permitir clicar em conceito → ver ideias que usam
  - Deve implementar busca: digitar conceito → sugerir similares
  - Deve exibir variations como tags secundárias

---

## ÉPICO 14: Melhorias de UX

**Objetivo:** Polimento de interface web baseado em feedbacks do usuário (Enter envia, custo em R$, métricas discretas).

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)

**Consulte:**
- `docs/interface/web.md` - Especificação de interface completa

### Funcionalidades:

#### 14.1 Enter Envia, Ctrl+Enter Pula Linha

- **Descrição:** Textarea com comportamento padrão (Enter envia, Ctrl+Enter pula linha).
- **Critérios de Aceite:**
  - Enter deve submeter form (enviar mensagem)
  - Ctrl+Enter deve inserir `\n` (pular linha)
  - Deve seguir padrão Claude.ai/ChatGPT
  - Deve funcionar cross-browser (Chrome, Firefox, Safari)

#### 14.2 Custo em R$

- **Descrição:** Exibir custos em reais (BRL) ao invés de dólares (USD).
- **Critérios de Aceite:**
  - Deve converter USD → BRL (taxa fixa ou API de câmbio)
  - Deve exibir: "R$ 0,02" ao invés de "$0.0039"
  - Deve adicionar config em `.env`: `CURRENCY=BRL`, `USD_TO_BRL_RATE=5.2`
  - Deve permitir fallback para USD se conversão falhar

#### 14.3 Métricas Inline Mais Discretas

- **Descrição:** Tornar métricas inline (tokens, custo, tempo) mais discretas visualmente.
- **Critérios de Aceite:**
  - Deve reduzir tamanho fonte para 0.75rem
  - Deve usar cor cinza claro (#94a3b8)
  - Deve posicionar no canto inferior direito da mensagem
  - Deve manter formato: "💰 R$0.02 · 215 tokens · 1.2s"

#### 14.4 Timeline Colapsada por Padrão

- **Descrição:** Bastidores com timeline de agentes anteriores colapsada inicialmente.
- **Critérios de Aceite:**
  - Deve mostrar seção "📈 Timeline" colapsada por padrão
  - Deve ter ícone: ▶ (colapsado) / ▼ (expandido)
  - Deve expandir ao clicar (mostrar histórico de agentes)
  - Deve persistir estado (colapsado/expandido) durante sessão

#### 14.5 Botão "Copiar Raciocínio"

- **Descrição:** Modal de raciocínio completo com botão para copiar texto.
- **Critérios de Aceite:**
  - Deve adicionar botão "📋 Copiar" no modal de raciocínio
  - Deve copiar texto markdown para clipboard
  - Deve mostrar feedback visual: "✓ Copiado!" (2s)
  - Deve funcionar cross-browser (clipboard API)

#### 14.6 Checklist de Progresso no Header

- **Descrição:** Exibir checklist visual no header do chat sincronizado com modelo cognitivo.
- **Critérios de Aceite:**
  - Deve mostrar bolinhas no header: [⚪⚪🟡⚪⚪] (clicável para expandir)
  - Deve usar status: ⚪ pendente 🟡 em progresso 🟢 completo
  - Deve adaptar checklist conforme tipo de artigo (empírico vs revisão vs teórico)
  - Deve sincronizar com modelo cognitivo (claim → escopo ✓, premises → população ✓, etc)
  - Deve mostrar minimizado por padrão (expandir ao clicar)

---

## ÉPICO 15: Agentes Avançados

**Objetivo:** Expandir sistema com agentes especializados para pesquisa, redação e revisão de artigos científicos.

**Status:** ⏳ Planejado (não refinado)

**Agentes Planejados:**
- **Pesquisador**: Busca e análise de literatura científica
- **Escritor**: Redação de seções do artigo
- **Crítico**: Revisão e feedback construtivo

**Consulte:** `docs/agents/overview.md` para mapa completo de agentes planejados.

---

## ÉPICO 16: Personas de Agentes

**Objetivo:** Permitir customização de agentes como "personas" (Sócrates, Aristóteles, Popper) com estilos de argumentação personalizados, transformando agentes em "mentores" que usuário pode escolher e treinar.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)
- ⏳ Épicos 11-14 concluídos (modelo de dados + gestão de ideias + UX)
- Agentes visíveis na interface (implementado no Épico 11+)

**Consulte:** 
- `docs/vision/agent_personas.md` - Visão completa de customização
- `docs/vision/vision.md` (Seção 1.1) - Agentes como diferencial

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
