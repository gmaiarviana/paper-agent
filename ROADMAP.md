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
- **ÉPICO 13**: Entidade Concept (não refinado)
- **ÉPICO 15**: Polimentos de UX (não refinado)
- **ÉPICO 16**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)
- **ÉPICO 17**: Personas de Agentes (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 13: Entidade Concept

**Objetivo:** Criar entidade Concept com vetores semânticos para busca por similaridade ("produtividade" encontra "eficiência").

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 12 concluído (Idea existe como entidade)

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

## ÉPICO 14: Navegação em Três Espaços

**Objetivo:** Separar navegação em três espaços distintos (Conversas, Meus Pensamentos, Catálogo) com feedback visual forte durante processamento.

**Status:** ✅ Concluído

**Dependências:**
- ✅ Épico 12 concluído (entidades Idea + Argument existem)

**Consulte:**
- `docs/interface/navigation_philosophy.md` - Filosofia de navegação
- `docs/interface/web.md` - Especificação técnica completa

### Funcionalidades:

#### 14.1 Sidebar: Conversas Recentes (Ajuste)
- **Descrição:** Ajustar sidebar para mostrar apenas conversas (não ideias). Adicionar botões de navegação para páginas dedicadas.
- **Critérios de Aceite:**
  - Remover listagem de ideias da sidebar
  - Mostrar apenas últimas 5 conversas (reduzir de 10 para 5)
  - Formato: "Título da conversa · Timestamp relativo" ("5min atrás", "2h atrás")
  - Conversa ativa destacada (bold, background diferente)
  - Adicionar botão [📖 Meus Pensamentos] que redireciona para `/pensamentos`
  - Adicionar botão [🏷️ Catálogo] que redireciona para `/catalogo` (desabilitado até Épico 13)
  - Botão [+ Nova Conversa] mantido

#### 14.2 Página: Meus Pensamentos
- **Descrição:** Criar página dedicada (`/pensamentos`) com grid de cards mostrando ideias cristalizadas durante conversas.
- **Critérios de Aceite:**
  - URL: `/pensamentos`
  - Grid de cards (2 colunas, responsivo) com preview de cada ideia
  - Card mostra: título, badge de status, # argumentos, # conceitos, timestamp relativo
  - Badges de status: 🔍 Explorando (amarelo), 📝 Estruturada (azul), ✅ Validada (verde)
  - Busca por título (LIKE query, case-insensitive)
  - Filtros: status (exploring, structured, validated)
  - Card clicável → redireciona para `/pensamentos/{idea_id}`

#### 14.3 Página: Detalhes da Ideia
- **Descrição:** Criar página dedicada (`/pensamentos/{idea_id}`) mostrando detalhes completos de uma ideia com argumentos, conceitos e conversas relacionadas.
- **Critérios de Aceite:**
  - URL única: `/pensamentos/{idea_id}`
  - Mostra: título da ideia, badge de status, timestamp de última atualização
  - Seção "Argumentos": lista versões (V1, V2, V3) com argumento focal destacado
  - Cada argumento mostra: claim (preview 100 chars), # premises, # assumptions
  - Link "Ver detalhes de V{n}" → expande argumento completo (claim, premises, assumptions)
  - Seção "Conceitos": lista conceitos usados (texto simples - navegação será adicionada no Épico 13)
  - Seção "Conversas relacionadas": lista threads com timestamp ("18/11, 14:56")
  - Botão [🔄 Continuar explorando] → cria novo thread_id e redireciona pro chat
  - Botão [📝 Editar título] → permite editar título inline (save on blur)

#### 14.4 Feedback Visual Forte
- **Descrição:** Input desabilitado + barra inline "Sistema pensando..." com texto dinâmico durante processamento.
- **Critérios de Aceite:**
  - Ao enviar mensagem: input desabilita imediatamente (opacidade 50%, cursor not-allowed)
  - Barra inline aparece abaixo da última mensagem: "🤖 Sistema pensando..." com animação suave
  - Texto dinâmico muda conforme agente ativo:
    - "⚡ Analisando sua mensagem..."
    - "🎯 Orquestrador pensando..."
    - "📝 Estruturador organizando..."
    - "🔬 Metodologista validando..."
  - Ao receber resposta: barra some com fade-out + input habilita
  - Implementação: `st.spinner()` customizado ou CSS + st.session_state["processing"]

#### 14.5 Bugfix: Restaurar Contexto ao Alternar Conversa (CRÍTICO)
- **Descrição:** Corrigir bug onde clicar em conversa na sidebar não restaura histórico de mensagens (chat fica branco).
- **Critérios de Aceite:**
  - Função `switch_idea()` ou equivalente deve carregar `thread_id` correto
  - Deve usar `SqliteSaver` para restaurar checkpoints da conversa selecionada
  - Deve restaurar histórico de mensagens completo (`st.session_state["messages"]`)
  - Deve restaurar argumento focal (`current_argument_id`) se existir
  - Chat deve exibir histórico completo após clicar em conversa
  - Bastidores deve atualizar com contexto da conversa (status, argumento focal)
  - Adicionar logs DEBUG para rastrear: `thread_id` carregado, # checkpoints encontrados, # mensagens restauradas
  - Validação: clicar em conversa → chat mostra histórico, não branco

---

## ÉPICO 15: Polimentos de UX

**Objetivo:** Polimento de interface web baseado em feedbacks do usuário (Enter envia, custo em R$, métricas discretas).

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)
- ✅ Épico 14 concluído (Navegação em Três Espaços)

**Consulte:**
- `docs/interface/web.md` - Especificação de interface completa

### Funcionalidades:

#### 15.1 Enter Envia, Ctrl+Enter Pula Linha

- **Descrição:** Textarea com comportamento padrão (Enter envia, Ctrl+Enter pula linha).
- **Critérios de Aceite:**
  - Enter deve submeter form (enviar mensagem)
  - Ctrl+Enter deve inserir `\n` (pular linha)
  - Deve seguir padrão Claude.ai/ChatGPT
  - Deve funcionar cross-browser (Chrome, Firefox, Safari)

#### 15.2 Custo em R$

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

#### 15.4 Timeline Colapsada por Padrão

- **Descrição:** Bastidores com timeline de agentes anteriores colapsada inicialmente.
- **Critérios de Aceite:**
  - Deve mostrar seção "📈 Timeline" colapsada por padrão
  - Deve ter ícone: ▶ (colapsado) / ▼ (expandido)
  - Deve expandir ao clicar (mostrar histórico de agentes)
  - Deve persistir estado (colapsado/expandido) durante sessão

#### 15.5 Botão "Copiar Raciocínio"

- **Descrição:** Modal de raciocínio completo com botão para copiar texto.
- **Critérios de Aceite:**
  - Deve adicionar botão "📋 Copiar" no modal de raciocínio
  - Deve copiar texto markdown para clipboard
  - Deve mostrar feedback visual: "✓ Copiado!" (2s)
  - Deve funcionar cross-browser (clipboard API)

#### 15.6 Checklist de Progresso no Header

- **Descrição:** Exibir checklist visual no header do chat sincronizado com modelo cognitivo.
- **Critérios de Aceite:**
  - Deve mostrar bolinhas no header: [⚪⚪🟡⚪⚪] (clicável para expandir)
  - Deve usar status: ⚪ pendente 🟡 em progresso 🟢 completo
  - Deve adaptar checklist conforme tipo de artigo (empírico vs revisão vs teórico)
  - Deve sincronizar com modelo cognitivo (claim → escopo ✓, premises → população ✓, etc)
  - Deve mostrar minimizado por padrão (expandir ao clicar)

---

## ÉPICO 16: Agentes Avançados

**Objetivo:** Expandir sistema com agentes especializados para pesquisa, redação e revisão de artigos científicos.

**Status:** ⏳ Planejado (não refinado)

**Agentes Planejados:**
- **Pesquisador**: Busca e análise de literatura científica
- **Escritor**: Redação de seções do artigo
- **Crítico**: Revisão e feedback construtivo

**Consulte:** `docs/agents/overview.md` para mapa completo de agentes planejados.

---

## ÉPICO 17: Personas de Agentes

**Objetivo:** Permitir customização de agentes como "personas" (Sócrates, Aristóteles, Popper) com estilos de argumentação personalizados, transformando agentes em "mentores" que usuário pode escolher e treinar.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)
- ⏳ Épicos 11-15 concluídos (modelo de dados + gestão de ideias + navegação + UX)

**Consulte:** 
- `docs/vision/agent_personas.md` - Visão completa de customização
- `docs/vision/vision.md` (Seção 1.1) - Agentes como diferencial

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
