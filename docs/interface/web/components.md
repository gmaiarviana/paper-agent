# Interface Web Conversacional - Componentes

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação para Épico 9 (POC → Protótipo → MVP)

> **📌 Documentação dividida:** Este documento contém componentes da interface.  
> Ver também: [`overview.md`](./overview.md) e [`flows.md`](./flows.md)

---

## 3. Layout da Interface

### 3.1 Estrutura Geral (Desktop)
```
┌─────────────────────────────────────────────────────────────────┐
│  [Sidebar]              [Chat]                      [Direita]   │
│                                                                 │
│  📖 Pensamentos         Conversa...           ┌───────────────┐ │
│  🏷️ Catálogo                                 │ 💡 Contexto   │ │
│  💬 Conversas                                 │ (ideia ativa) │ │
│  [+ Nova conversa]                            └───────────────┘ │
│                                               ┌───────────────┐ │
│                                               │📊 Bastidores  │ │
│                                               │ (pensamento)  │ │
│                                               │ (timeline)    │ │
│                                               └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Layout com 3 elementos:**
- **Sidebar:** Links de navegação (sem lista de conversas)
- **Chat (50-60%):** Conversação principal
- **Painel Direito:** Dividido em Contexto (acima) + Bastidores (abaixo)

### 3.2 Componentes Detalhados

**A) Sidebar (Links de Navegação)**

```
┌─────────────────────────┐
│ 📖 Pensamentos          │ → /pensamentos
│ 🏷️ Catálogo            │ → /catalogo (desabilitado)
│ 💬 Conversas            │ → /historico
│                         │
│ [+ Nova conversa]       │ → inicia chat novo
└─────────────────────────┘
```

**Funcionalidades:**
- Links com ícones para páginas dedicadas
- Botão "+ Nova conversa" inicia chat novo
- Sem lista de conversas recentes (histórico em página dedicada)
- Sem header/logo (minimalista)

**B) Página: Minhas Ideias**

**Localização:** `/pensamentos` (URL mantida para compatibilidade, mas interface mostra "Minhas Ideias")

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ 💡 Minhas Ideias                                 │
│                                                 │
│ [🔍 Buscar ideias...]                           │
│ [Status ▼] [Conceitos ▼]                        │
│                                                 │
│ ┌─────────────────────┐ ┌─────────────────────┐│
│ │💡 LLMs em produtiv. │ │💡 Semana 4 dias     ││
│ │                     │ │                     ││
│ │ 📝 Estruturada      │ │ ✅ Validada         │
│ │ 3 argumentos        │ │ 2 argumentos        │
│ │ 5 conceitos         │ │ 4 conceitos         │
│ │                     │ │                     ││
│ │ 2h atrás            │ │ 1 dia atrás         │
│ │ [Ver detalhes →]    │ │ [Ver detalhes →]    │
│ └─────────────────────┘ └─────────────────────┘│
└─────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Grid de cards (2 colunas, responsivo)
- Busca por título (LIKE query, case-insensitive)
- Filtros: status (exploring, structured, validated)
- Card clicável → redireciona pra `/pensamentos/{idea_id}`

**Badges de Status:**
- 🔍 Explorando (amarelo)
- 📝 Estruturada (azul)
- ✅ Validada (verde)

**C) Página: Detalhes da Ideia**

**Localização:** `/pensamentos/{idea_id}`

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ [← Voltar] 💡 LLMs em produtividade             │
│                                                 │
│ Solidez geral: ██████░░ 65%                     │
│                                                 │
│ ─────────────────────────────────────────────   │
│                                                 │
│ 📊 Fundamentos:                                 │
│   • "LLMs reduzem tempo de código"              │
│     Solidez: ████████ 80% (3 evidências)        │
│   • "Qualidade não é afetada"                   │
│     Solidez: ███░░░░░ 35% (1 evidência fraca)   │ ← alerta visual
│     [🔍 Fortalecer com pesquisa]                │
│                                                 │
│ 💬 Conversas associadas:                        │
│   • Conversa 1 (18/11, 14:56)                   │
│   • Conversa 2 (19/11, 10:30)                   │
│                                                 │
│ ─────────────────────────────────────────────   │
│                                                 │
│ [💬 Continuar elaborando]  ← novo chat          │
│ [📝 Criar conteúdo]        ← se madura          │
└─────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Mostra solidez geral da ideia (barra de progresso)
- Lista fundamentos (proposições) com suas solidezes individuais
- Alertas visuais para fundamentos frágeis (< 40%)
- Botão "Fortalecer com pesquisa" para fundamentos frágeis
- Contador: "2 fundamentos precisam fortalecimento"
- Conversas associadas à ideia
- Botão "Continuar elaborando" → cria novo thread_id e volta pro chat
- Botão "Criar conteúdo" → disponível quando ideia tem solidez >= 60%

**D) Chat Principal (50-60% largura)**
```
┌──────────────────────────────────────┐
│  Você: "Observei que TDD reduz bugs" │
│  ℹ️                                  │ ← ícone pequeno (clicável)
│                                      │
│  Sistema: "Interessante! Em que...  │
│  ℹ️                                  │ ← ícone pequeno (clicável)
│                                      │
│  [Input de texto aqui]               │ ← st.chat_input (nativo)
└──────────────────────────────────────┘
```

**Métricas por mensagem:**
- Ícone pequeno (ℹ️) após cada mensagem do sistema
- Clique no ícone abre popover com métricas
- Formato: "💰 R$0,02 · 215 tokens · 1.2s"
- Métricas NÃO ficam sempre visíveis (reduz ruído)

**Input de chat:**
- Usar `st.chat_input` (componente nativo Streamlit)
- Enter envia mensagem

**E) Bastidores (Painel Direito - Abaixo)**

**Propósito:** Mostrar o sistema pensando (reasoning dos agentes).

**Estrutura:**
```
┌──────────────────────────────┐
│ 📊 Bastidores            🔴  │ ← header clicável + indicador
├──────────────────────────────┤
│                              │
│ ┌──────────────────────────┐ │
│ │ 🎯 Orquestrador          │ │ ← Card de pensamento
│ │ "Analisando contexto..." │ │
│ │ [Ver completo]           │ │
│ └──────────────────────────┘ │
│                              │
│ ┌──────────────────────────┐ │
│ │ 📜 Timeline              │ │ ← Card de timeline
│ │ ● 🎯 Orq. - 10:32        │ │
│ │ ● 📝 Est. - 10:31        │ │
│ │ ● 🎯 Orq. - 10:30        │ │
│ │ [Ver histórico]          │ │
│ └──────────────────────────┘ │
└──────────────────────────────┘
```

**Comportamento:**
- Header clicável para expandir/colapsar seção inteira
- Indicador de novidade (🔴 ou "+2") quando há atualizações
- Indicador some ao expandir
- Não expande automaticamente (não distrai usuário)

**Estado vazio:**
```
┌──────────────────────────────┐
│ 📊 Bastidores                │
│                              │
│           🤖                 │
│       Aguardando...          │
│                              │
└──────────────────────────────┘
```

**Card de Pensamento:**
- Emoji + nome do agente ativo
- Pensamento resumido (~280 chars)
- Link "Ver completo" → modal com raciocínio completo

**Card de Timeline:**
- Últimos 3 agentes (atual + 2 anteriores)
- Formato: emoji + nome + resumo curto + horário
- Link "Ver histórico" → modal com lista completa

**Modal de Timeline:**
- Lista completa de todos os agentes que trabalharam
- Mesmo formato: emoji + nome + resumo + horário
- Ordenado por mais recente primeiro

**Futuro (Épico 18):**
- Agentes customizáveis como personas (Sócrates, Aristóteles, Popper)
- Botão "Customizar persona" ao lado de cada agente
- Ver: `docs/vision/agent_personas.md`

**F) Contexto (Painel Direito - Acima)**

**Propósito:** Mostrar informações sobre a ideia e conversa ativa.

**Estrutura:**
```
┌──────────────────────────────┐
│ 💡 Contexto              [↗] │ ← header clicável
├──────────────────────────────┤
│ 📝 "LLMs e produtividade"    │ ← título da ideia
│ Status: Estruturada          │
│ Solidez: ██████░░ 65%        │
│                              │
│ 💰 R$ 0,15 total             │ ← custo acumulado (clicável)
└──────────────────────────────┘
```

**Comportamento:**
- Header clicável para expandir/colapsar
- Clique no custo abre modal com detalhes
- Atualiza em tempo real

**Estado vazio (sem ideia associada):**
- Seção em branco ou não aparece
- Só mostra custo acumulado

**Modal de detalhes:**
- Ideia completa (título, status, argumentos)
- Custo detalhado por mensagem
- Modelo usado
- Total de tokens

**Chat iniciado de página de ideia:**
- Já começa com ideia associada no Contexto

---

### 3.3 Fluxo "Criar Conteúdo"

**Trigger:** Botão "Criar conteúdo" disponível quando ideia tem solidez >= 60%

**Fluxo:**

```
Usuário clica "Criar conteúdo"
↓
Abre chat com prompt inicial:
Sistema: "Vamos criar conteúdo a partir dessa ideia!
Que formato você prefere?

• Artigo acadêmico
• Post de blog
• Thread de Twitter
• Outro"
↓
Conversa curta para definir:

• Formato
• Tom/estilo
• Ênfase (qual fundamento destacar)
• Público-alvo
↓
Orquestrador chama Escritor
↓
Conteúdo gerado baseado em:

• Claim da ideia
• Fundamentos (proposições)
• Evidências
• Preferências definidas na conversa
```

**Implementação:**
- Botão "Criar conteúdo" aparece condicionalmente (solidez >= 60%)
- Abre novo chat com contexto pré-carregado da ideia
- Orquestrador detecta intenção de criar conteúdo e chama Escritor
- Escritor gera conteúdo usando metadados já elaborados (claim, fundamentos, evidências)
- Usuário pode revisar e ajustar antes de exportar

---

### 3.4 Indicadores Visuais

**A) Solidez (novo)**

- Barra de progresso colorida
- Verde (>70%): sólido
- Amarelo (40-70%): moderado
- Vermelho (<40%): frágil

**Visual:**
```
Solidez geral: ████████░░ 80%  ← verde
Solidez: ██████░░ 65%            ← amarelo
Solidez: ███░░░░░ 35%            ← vermelho
```

**B) Alertas de Fragilidade**

- Fundamentos com solidez < 40% mostram alerta visual
- Botão "Fortalecer com pesquisa" disponível
- Contador: "2 fundamentos precisam fortalecimento"

**Visual:**
```
📊 Fundamentos:
  • "LLMs reduzem tempo de código"
    Solidez: ████████ 80% (3 evidências)  ← verde
    
  ⚠️ • "Qualidade não é afetada"
    Solidez: ███░░░░░ 35% (1 evidência fraca)  ← vermelho + alerta
    [🔍 Fortalecer com pesquisa]
    
  ⚠️ • "Custo-benefício é positivo"
    Solidez: ██░░░░░░ 25% (0 evidências)  ← vermelho + alerta
    [🔍 Fortalecer com pesquisa]
    
[2 fundamentos precisam fortalecimento]
```

---

### 3.5 Status da Ideia

**Nota:** Conteúdo movido para seção "Contexto" (3.2 F). Ver detalhes acima.

---

### 3.6 Painel Progress (Checklist)

> **📌 Status atual:** Backend implementado, frontend NÃO integrado.  
> **Integração:** Épico 15.  
> **Referência:** `agents/checklist/progress_tracker.py`

> **🔍 DIFERENÇA CHAVE:** Progress mostra **onde o usuário está na jornada** (estado atual do argumento).  
> Bastidores mostra o **sistema pensando** (reasoning em tempo real).

**Localização:** Borda direita do chat, flutuante/fixo

**Visual:**
```
┌──────────────────────┐
│ 📊 Progresso         │
│                      │
│ ⚪ 1. Escopo definido │
│ ⚪ 2. População       │
│ 🟡 3. Métricas        │ ← em progresso
│ ⚪ 4. Metodologia     │
│ ⚪ 5. Baseline        │
│                      │
│ [🔄 Atualizar]       │
└──────────────────────┘
```

**Comportamento:**
- Lista vertical de itens com status (⚪ pendente, 🟡 em progresso, 🟢 completo)
- Acompanha scroll da conversa (fixo/flutuante na borda direita)
- Adapta conforme tipo de artigo detectado (empírico, revisão, teórico)
- Sincroniza com modelo cognitivo (`CognitiveModel`) em tempo real
- Atualiza automaticamente conforme argumento evolui

**Checklists Adaptativos:**

**Artigo Empírico:**
- ⚪ Escopo definido (claim específico)
- ⚪ População identificada
- ⚪ Métricas definidas
- ⚪ Metodologia estruturada
- ⚪ Baseline definido

**Artigo de Revisão:**
- ⚪ Questão de pesquisa (PICO/SPIDER)
- ⚪ Estratégia de busca
- ⚪ Critérios de inclusão/exclusão
- ⚪ Síntese de evidências
- ⚪ Lacunas identificadas

**Artigo Teórico:**
- ⚪ Problema conceitual
- ⚪ Framework proposto
- ⚪ Consistência lógica
- ⚪ Contribuições claras
- ⚪ Implicações discutidas

**Artigo Genérico (padrão):**
- ⚪ Afirmação clara
- ⚪ Contexto definido
- ⚪ Fundamentos sólidos
- ⚪ Suposições baixas
- ⚪ Lacunas respondidas

**Implementação Técnica:**
- Backend: `ProgressTracker` avalia `CognitiveModel` e retorna `List[ChecklistItem]`
- Status inferido de campos do modelo (claim, fundamentos, context, etc.)
- Frontend: Componente Streamlit que consome checklist do backend
- Atualização: Polling ou SSE (conforme implementação de eventos)

---

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação completa para implementação

