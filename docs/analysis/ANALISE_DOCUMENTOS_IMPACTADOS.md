# Análise de Documentos Impactados pelas Mudanças Planejadas

## Mudanças Planejadas

### Sidebar
- Navegação limpa (só links: Pensamentos, Catálogo)
- Sem listar conversas
- Minimalista, inspirado no Claude

### Painel Direito - Nova estrutura
- **Contexto** (seção acima): Ideia ativa, status, entidades, evolução em tempo real
- **Bastidores** (seção abaixo): Cards de pensamento do agente + timeline expansível

### Bastidores
- Cards: pensamento atual + timeline de contribuições
- Atualização em tempo real
- Timeline expansível → modal para histórico completo
- Indicador sutil de novidade (sem expandir automaticamente)

### Métricas
- Discretas (hover ou ícone expandível, não sempre visíveis)
- Custo acumulado no "Contexto" ou topo do chat
- Suporte a R$ (configurável)

### Comportamento
- Enter envia mensagem (não pula linha)
- Toggle "Ver raciocínio" removido (raciocínio integrado aos Bastidores)

---

## Tabela de Análise

| Documento | Impactado? | Seções a Atualizar | Conflitos Identificados |
|-----------|------------|-------------------|------------------------|
| `docs/interface/web/` | ✅ **SIM - ALTO IMPACTO** | **3.1 Estrutura Geral (Desktop)**: Layout precisa refletir nova estrutura (Contexto + Bastidores no painel direito)<br><br>**3.2 Componentes Detalhados**:<br>- **A) Menu Principal**: Remover lista de conversas, manter apenas links (Pensamentos, Catálogo)<br>- **E) Bastidores**: Reescrever completamente - remover toggle, adicionar estrutura de cards + timeline expansível<br>- **D) Chat Principal**: Atualizar para mencionar métricas discretas<br><br>**3.5 Mostrar Status da Ideia**: Integrar na seção "Contexto" do painel direito<br><br>**4.2 Fluxo de Bastidores**: Atualizar para refletir nova estrutura (sem toggle, sempre visível)<br><br>**5.1 Componentes Streamlit**: Atualizar `backstage.py` para nova estrutura<br><br>**5.2 Polling de Eventos**: Manter, mas ajustar para atualização de cards | **CONFLITO 1**: Seção 3.1 mostra menu com "Histórico" e lista de conversas - precisa remover<br><br>**CONFLITO 2**: Seção 3.2 E mostra Bastidores com toggle "🔍 Ver raciocínio" - precisa remover toggle e integrar sempre visível<br><br>**CONFLITO 3**: Seção 3.5 descreve status da ideia no "topo" dos Bastidores - precisa mover para seção "Contexto" acima<br><br>**CONFLITO 4**: Seção 4.2 descreve fluxo com toggle - precisa reescrever para cards + timeline<br><br>**CONFLITO 5**: Métricas inline no chat (seção 3.2 D) - precisa tornar discretas (hover/ícone) |
| `docs/interface/navigation_philosophy.md` | ✅ **SIM - MÉDIO IMPACTO** | **Princípios de Design - Item 4. Menu Minimalista**: Atualizar para refletir remoção de lista de conversas<br><br>**Seção "Quatro Espaços Distintos"**: Verificar se "Histórico" ainda é mencionado como espaço secundário - pode precisar ajuste | **CONFLITO 1**: Item 4 menciona "Menu colapsável" com acesso a ideias, histórico, biblioteca - precisa remover histórico da navegação principal<br><br>**CONFLITO 2**: Seção "2. Histórico (Secundário - Processo)" ainda descreve histórico como espaço de navegação - pode precisar ajuste ou remoção |
| `docs/vision/vision.md` (seção 5.2) | ✅ **SIM - MÉDIO IMPACTO** | **5.2 Interface Web: Chat + Bastidores**:<br>- Atualizar layout consolidado para remover lista de conversas da sidebar<br>- Atualizar descrição de Bastidores para refletir nova estrutura (cards + timeline)<br>- Remover menção a toggle "Ver raciocínio"<br>- Atualizar descrição de métricas para discretas | **CONFLITO 1**: Layout consolidado (linha 358-369) mostra sidebar com "💬 Conversas" e lista - precisa remover<br><br>**CONFLITO 2**: Descrição de "Painel 'Bastidores' opcional" - precisa mudar para sempre visível (sem toggle)<br><br>**CONFLITO 3**: Menção a "Ver raciocínio" como opcional - precisa remover |
| `ARCHITECTURE.md` (seção Interfaces Mantidas) | ✅ **SIM - BAIXO IMPACTO** | **Seção "Interfaces Mantidas" - Chat Web**:<br>- Atualizar descrição da sidebar para mencionar apenas links (Pensamentos, Catálogo)<br>- Remover menção a "últimas 5 conversas" | **CONFLITO 1**: Linha 113 menciona "Sidebar com últimas 5 conversas" - precisa remover ou atualizar |
| `docs/vision/conversation_patterns.md` | ⚠️ **PARCIAL - BAIXO IMPACTO** | **Seção 3 - Padrões de Transição Fluida**: Verificar menções a "Bastidores" e atualizar se necessário para refletir nova estrutura (cards sempre visíveis) | **POSSÍVEL CONFLITO**: Menções a "Bastidores" podem assumir toggle - verificar e ajustar se necessário |
| `docs/vision/cognitive_model.md` | ❌ **NÃO IMPACTADO** | Nenhuma seção específica - documento foca em modelo de dados, não em interface | Nenhum conflito identificado |

---

## Resumo Executivo

### Documentos com ALTO IMPACTO (requerem reescrita significativa):
1. **`docs/interface/web/`** - Documento principal de especificação da interface (dividido em overview.md, components.md, flows.md). Precisa de atualizações extensivas em múltiplas seções.

### Documentos com MÉDIO IMPACTO (requerem ajustes pontuais):
2. **`docs/interface/navigation_philosophy.md`** - Filosofia de navegação precisa alinhar com remoção de histórico da sidebar
3. **`docs/vision/vision.md` (seção 5.2)** - Descrição da interface web precisa atualizar layout e comportamento

### Documentos com BAIXO IMPACTO (ajustes menores):
4. **`ARCHITECTURE.md`** - Apenas menção à sidebar precisa atualização
5. **`docs/vision/conversation_patterns.md`** - Verificação pontual de menções a Bastidores

### Documentos NÃO IMPACTADOS:
6. **`docs/vision/cognitive_model.md`** - Foca em modelo de dados, não em interface

---

## Conflitos Críticos a Resolver

1. **Sidebar com lista de conversas**: Múltiplos documentos descrevem sidebar listando conversas - precisa remover de todos
2. **Toggle "Ver raciocínio"**: Documentado como opcional/collapsible - precisa mudar para sempre visível
3. **Estrutura de Bastidores**: Atualmente descrito como painel colapsável - precisa reescrever para cards + timeline
4. **Métricas inline**: Descritas como sempre visíveis - precisa tornar discretas (hover/ícone)
5. **Status da Ideia**: Descrito no "topo dos Bastidores" - precisa mover para seção "Contexto" acima

---

## Recomendações

1. **Prioridade 1**: Atualizar `docs/interface/web/` completamente - é a especificação técnica principal (dividido em overview.md, components.md, flows.md)
2. **Prioridade 2**: Alinhar `docs/interface/navigation_philosophy.md` com nova filosofia (sem histórico na sidebar)
3. **Prioridade 3**: Atualizar `docs/vision/vision.md` seção 5.2 para refletir novo layout
4. **Prioridade 4**: Ajustes menores em `ARCHITECTURE.md` e verificação em `conversation_patterns.md`

