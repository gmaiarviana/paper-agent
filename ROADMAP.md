# ROADMAP - Paper Agent

📌 **Nota de Renumeração (15/11/2025):** Épicos foram renumerados para refletir ordem lógica de implementação: Telemetria (8) → Interface Web (9) → Persistência (10).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [BACKLOG.md](BACKLOG.md).

## 📋 Status dos Épicos

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 5: Interface Conversacional e Transparência (Dashboard)
- ÉPICO 6: Memória Dinâmica e Contexto por Agente (Config YAML + MemoryManager)
- ÉPICO 7: Orquestrador Conversacional Inteligente (POC completo)
- ÉPICO 8: Telemetria e Observabilidade (parcialmente refinado)
- ÉPICO 9: Interface Web Conversacional (refinado)

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 10: Entidade Tópico e Persistência
- ÉPICO 11+: Agentes Avançados (Pesquisador, Escritor, Crítico)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## ✅ ÉPICOS CONCLUÍDOS

- **ÉPICO 3:** Orquestrador + Estruturador (Base Multi-Agente)
- **ÉPICO 4:** Loop Colaborativo + Refinamento Iterativo
- **ÉPICO 5:** Interface Conversacional e Transparência (parcial - Dashboard implementado)
- **ÉPICO 6:** Memória Dinâmica e Contexto por Agente (parcial - Config YAML + MemoryManager)
- **ÉPICO 7:** Orquestrador Conversacional Inteligente (POC completo)

---

## 📋 PRÓXIMAS FUNCIONALIDADES

## ÉPICO 7: Orquestrador Conversacional Inteligente

**Status:** ✅ POC implementado | ⚠️ Protótipo e MVP aguardam refinamento

**POC (concluído):**
- ✅ Exploração com perguntas abertas
- ✅ Análise contextual com histórico completo
- ✅ Sugestão com justificativa
- ✅ Detecção de mudança de direção

**Limitações conhecidas do POC:**
- Argumento focal implícito (via histórico) - será explícito no MVP
- Ignora limite de contexto - será tratado no Protótipo (baixa prioridade)
- Raciocínio básico - será refinado no Protótipo (transparência do raciocínio)

**Consulte:** 
- `docs/orchestration/conversational_orchestrator.md` - especificação técnica completa
- `docs/product/conversation_patterns.md` - padrões de conversa esperados

---

#### Protótipo (segunda entrega - ✅ IMPLEMENTADO)

**Status:** ✅ Implementado (15/11/2025)

✅ **Foco: Experiência conversacional real na CLI**

**Funcionalidades implementadas:**

#### 7.5: CLI Conversacional Contínua ✅
- **Descrição:** Transformar CLI de loop único em chat contínuo com múltiplos turnos
- **Implementação:**
  - ✅ CLI mantém conversa sem voltar para "Digite sua hipótese" após cada resposta
  - ✅ Thread ID preservado ao longo da sessão
  - ✅ Contexto acumulado (histórico completo) usado pelo Orquestrador
  - ✅ Loop conversacional: Você → Sistema → Você → Sistema (N turnos)
  - ✅ Sistema para quando usuário decide chamar agente ou digita 'exit'

#### 7.6: Detecção Inteligente de Momento Certo ✅
- **Descrição:** Orquestrador detecta quando tem informação suficiente para sugerir chamar agente (não determinístico)
- **Implementação:**
  - ✅ Usa LLM para julgar "momento certo" (não regras fixas)
  - ✅ Considera quantidade e qualidade de informação acumulada
  - ✅ Sugere agente quando chamar agregaria valor (não apenas "protocolo")
  - ✅ next_step: "explore" → continua perguntando
  - ✅ next_step: "suggest_agent" → sugere chamar agente específico

#### 7.7: Transparência do Raciocínio ✅
- **Descrição:** Expor reasoning do Orquestrador de forma acessível sem poluir CLI
- **Implementação:**
  - ✅ CLI exibe apenas mensagem limpa por padrão
  - ✅ Flag `--verbose` opcional exibe reasoning inline
  - ✅ EventBus emite eventos com reasoning completo
  - ⚠️ Dashboard Streamlit consome e exibe reasoning em tempo real (validar manualmente)
  - ✅ Usa infraestrutura existente do Épico 5 (eventos)

---

#### MVP (terceira entrega - ✅ Concluído)

**Funcionalidades mantidas no MVP:**

#### 7.8: Argumento Focal Explícito ✅
- **Descrição:** Campo `focal_argument` no MultiAgentState
- **Implementação:**
  - ✅ Orquestrador extrai e atualiza argumento focal explicitamente a cada turno
  - ✅ Campo armazena: intent, subject, population, metrics, article_type
  - ✅ Detecção de mudança de direção (compara focal atual vs novo input)
  - ✅ Fundação para Épico 10 (persistência)
  - ✅ CLI exibe argumento focal no modo --verbose

#### 7.9: Provocação de Reflexão (versão simples) ✅

**Descrição:** Orquestrador faz perguntas inteligentes que ajudam usuário a refletir sobre aspectos não explorados da conversa.

**Implementação:**
- ✅ Baseado em análise contextual do LLM (não precisa de RAG ou histórico entre sessões)
- ✅ Identifica lacunas na conversa através do histórico de mensagens
- ✅ Faz perguntas sobre aspectos importantes mas não mencionados
- ✅ Integrado naturalmente no fluxo conversacional
- ✅ Campo `reflection_prompt` no output do Orquestrador
- ✅ CLI exibe provocações quando geradas

**Exemplos de provocação:**

**Exemplo 1: Lacuna de métricas**
```
Usuário: "Observei que método X é mais rápido"
[conversa sobre velocidade]
Usuário: "Medindo tempo de sprint"

Orquestrador: "Você mencionou tempo de sprint, mas e QUALIDADE 
               do código? Isso importa para sua pesquisa?"
```

**Exemplo 2: Lacuna de contexto**
```
Usuário: "TDD reduz bugs"
[conversa sobre redução]

Orquestrador: "Interessante! E em que TIPO de projeto você observou 
               isso? Web, mobile, backend? Pode fazer diferença."
```

**Exemplo 3: Lacuna de população**
```
Usuário: "LLMs aumentam produtividade em 30%"

Orquestrador: "30% é significativo! Mas produtividade DE QUEM? 
               Desenvolvedores júnior, sênior, times específicos?"
```

**Prompt do Orquestrador (atualizado):**
```
Além de responder o usuário, IDENTIFIQUE LACUNAS na conversa:

Aspectos importantes MAS NÃO EXPLORADOS:
- População mencionada mas não especificada?
- Métrica mencionada mas não operacionalizada?
- Contexto vago (onde, quando, com quem)?
- Comparações sem baseline (mais rápido que o quê?)?
- Causalidade assumida sem evidência?

Se identificar lacuna, QUESTIONE naturalmente:
"Você mencionou X, mas e Y? Isso importa para sua pesquisa?"

NÃO force provocação se conversa está completa.
NÃO faça múltiplas perguntas de uma vez.
```

**Critérios de aceite:**
- Orquestrador identifica lacunas no histórico da conversa
- Faz perguntas que ajudam usuário a pensar melhor
- Perguntas são contextuais e relevantes
- Não força provocação se conversa está completa
- Integrado no fluxo (não interrompe conversa)

**Limitações conhecidas (versão simples):**
- Não usa RAG (não consulta literatura científica)
- Não analisa padrões entre sessões (memória curta)
- Não aprende preferências do usuário ao longo do tempo
- Baseado apenas no histórico da conversa atual

**Evolução futura (versão complexa):**
- RAG: Sugerir ângulos baseado em papers relacionados
- Memória longa: Identificar vieses cognitivos recorrentes do usuário
- Preferências: Adaptar provocações ao estilo do usuário
- [Backlog - não refinado]

#### 7.10: Detecção Emergente de Estágio ✅
- **Descrição:** Orquestrador infere quando usuário convergiu naturalmente
- **Implementação:**
  - ✅ Sistema detecta quando conversa evoluiu (exploration → hypothesis)
  - ✅ Sugere mudança de estágio: "Parece que temos hipótese formada. Quer validar com Metodologista?"
  - ✅ Não classifica upfront (detecta emergência durante conversa)
  - ✅ Usuário pode confirmar ou refutar inferência
  - ✅ Campo `stage_suggestion` no output do Orquestrador (from_stage, to_stage, justification)
  - ✅ CLI exibe sugestões de estágio quando detectadas

---

**Funcionalidades MOVIDAS para outros Épicos:**

As funcionalidades abaixo foram planejadas para o MVP do Épico 7, mas movidas para outros épicos por dependência ou escopo:

**7.12: Reasoning Explícito das Decisões** → **Épico 9.6/9.7** (Interface Web)
- **Razão:** Funcionalidade de INTERFACE (exibir reasoning), não do Orquestrador
- Orquestrador já captura reasoning
- Web precisa exibir de forma elegante (bastidores + modal)

**7.13: Histórico de Decisões (aprende preferências)** → **Épico 10.7** (Persistência)
- **Razão:** Requer persistência entre sessões
- Precisa de banco de dados ou filesystem
- Não faz sentido implementar antes do Épico 10

**7.14: Argumento Focal Persistente** → **Épico 10.2** (Persistência)
- **Razão:** Depende da entidade Topic (Épico 10)
- Precisa de persistência em banco/filesystem
- Vinculado ao POC do Épico 10

---

## ÉPICO 8: Telemetria e Observabilidade

**Objetivo:** Instrumentar todos os agentes para capturar reasoning, decisões e métricas, e implementar streaming de eventos em tempo real.

**Status:** 🟡 Parcialmente refinado

**Dependências:**
- Épico 7 concluído (Orquestrador Conversacional)

### Progressão POC → Protótipo → MVP

#### POC (instrumentação básica)

**8.1: Instrumentar Estruturador**
- Adicionar campo reasoning no output do Estruturador
- Reasoning simples: "Estruturando V1 com base em: [contexto, problema, contribuição]"
- EventBus publica reasoning do Estruturador

**Critérios de aceite POC:**
- Estruturador emite evento com reasoning
- Dashboard pode exibir reasoning do Estruturador
- Formato consistente com outros agentes

#### Protótipo (streaming e métricas)

**8.2: Instrumentar Metodologista**
- Adicionar campo reasoning no output (além da justification existente)
- Reasoning detalha processo: "Analisei testabilidade, falseabilidade, especificidade..."
- justification mantém conclusão resumida

**8.3: SSE (Server-Sent Events)**
- Implementar endpoint SSE para streaming de eventos
- Dashboard consome eventos em tempo real (não polling)
- Fallback para polling se SSE falhar

**8.4: Métricas consolidadas**
- Tokens e custo por agente
- Tokens e custo total da sessão
- Tempo de execução por agente

**Critérios de aceite Protótipo:**
- Todos os agentes emitem reasoning estruturado
- Dashboard recebe eventos em tempo real via SSE
- Métricas exibidas corretamente

#### MVP (alertas e otimizações)

**8.5: Alertas de custo**
- Alerta quando custo da sessão ultrapassar threshold ($0.50, $1.00)
- Exibir custo acumulado do dia
- Warning ao atingir 80% do budget configurado

**Critérios de aceite MVP:**
- Sistema alerta usuário sobre custos
- Budget configurável via .env
- Logs estruturados de custos

**Melhorias futuras (Backlog):**
- Replay de sessão (ver reasoning passo a passo)
- Export de reasoning (JSON, markdown)
- Análise de padrões (quais agentes mais usados)

---

## ÉPICO 9: Interface Web Conversacional

**Objetivo:** Criar interface web como experiência principal do sistema, com chat fluido, visualização de reasoning dos agentes ("bastidores"), e métricas de custo inline.

**Status:** 🟡 Refinado

**Dependências:**
- Épico 8 POC concluído (reasoning instrumentado)
- Épico 7 concluído (Orquestrador Conversacional)

**Consulte:** `docs/interface/web.md` para especificação técnica completa

### Progressão POC → Protótipo → MVP

#### POC (chat básico funcionando)

**9.1: Input de chat na interface Streamlit**
- Campo de texto para enviar mensagens
- Botão "Enviar" ou Enter para submeter
- Estado de "digitando..." enquanto processa

**9.2: Backend conversacional integrado**
- Mensagens enviadas para LangGraph (mesmo backend do CLI)
- Orquestrador processa via thread_id único por sessão
- Resposta retorna para interface

**9.3: Histórico de conversa visível**
- Exibir mensagens anteriores (Você: / Sistema:)
- Scroll automático para última mensagem
- Layout limpo e legível

**9.4: Métricas inline discretas**
- Custo e tokens por mensagem (pequeno, após resposta)
- Formato: "💰 $0.0012 · 215 tokens · 1.2s"
- Não distrai da conversa

**9.5: Polling de eventos (1s)**
- EventBus publica eventos em arquivos JSON (infraestrutura existente)
- Interface faz polling a cada 1 segundo para buscar novos eventos
- Atualiza bastidores e timeline quando eventos chegam
- Simples e funcional para POC

**Critérios de aceite POC:**
- Usuário pode conversar via web (input → output)
- Histórico preservado durante sessão
- Métricas visíveis mas discretas
- Backend compartilhado com CLI (LangGraph + EventBus)
- Bastidores atualizam via polling (delay de ~1s aceitável)

#### Protótipo (bastidores e transparência)

**9.6: Painel "Bastidores" (collapsible)**
- Sidebar ou painel lateral (40% da tela)
- Botão "🔍 Ver raciocínio" (fechado por padrão)
- Abre/fecha com toggle

**9.7: Reasoning resumido dos agentes**
- Mostra agente ativo (Orquestrador, Estruturador, Metodologista)
- Reasoning resumido (~280 chars)
- Tempo, tokens, custo do agente
- *Nota: Implementa funcionalidade 7.12 do Épico 7 (Reasoning Explícito das Decisões)*

**9.8: Timeline de agentes (histórico)**
- Lista de agentes executados (colapsado)
- Expandir para ver reasoning de passos anteriores
- Ordenado cronologicamente

**9.9: Reasoning completo (modal)**
- Botão "📄 Ver raciocínio completo" ao lado do resumo
- Modal/dialog com JSON estruturado
- Mostra todos os campos do agente
- *Nota: Implementa funcionalidade 7.12 do Épico 7 (Reasoning Explícito das Decisões)*

**Critérios de aceite Protótipo:**
- Bastidores exibem reasoning via polling (1s)
- Timeline preserva histórico de raciocínio
- Usuário pode expandir para ver detalhes
- Experiência fluida apesar do delay do polling

#### MVP (experiência completa)

**9.10: SSE (Server-Sent Events) para streaming**
- Implementar endpoint SSE: `/events/<session_id>`
- Interface consome eventos em tempo real (não polling)
- Fallback para polling se SSE falhar
- Reconnect automático em caso de falha
- Melhora experiência (sem delay de 1s do polling)

**9.11: Sidebar com lista de sessões**
- Lista de conversas anteriores (título, data)
- Criar nova sessão
- Alternar entre sessões (não simultâneo)

**9.12: Métricas consolidadas**
- Total de tokens e custo da sessão
- Breakdown por agente (Orquestrador: X tokens, Metodologista: Y tokens)
- Exibido em painel ou tooltip

**Critérios de aceite MVP:**
- SSE funciona (streaming em tempo real, sem delay)
- Múltiplas sessões gerenciadas pela sidebar
- Sessões NÃO persistem entre reloads (temporárias)
- Métricas consolidadas visíveis
- Fallback para polling se SSE falhar

**Melhorias futuras (Backlog):**
- Mobile responsivo (bastidores como modal/overlay)
- Export de conversas (markdown, PDF)
- Replay de sessão (ver conversa + reasoning passo a passo)
- Temas (claro/escuro)
- Atalhos de teclado

---

## ÉPICO 10: Entidade Tópico e Persistência

**Objetivo:** Permitir pausar/retomar conversas com contexto completo preservado, suportando múltiplos tópicos em evolução e persistência entre sessões.

**Status:** ⚠️ Não refinado

**Dependências:**
- Épico 9 concluído (Interface Web)

**Consulte:** `docs/architecture/state_evolution.md` para detalhes de evolução de estado.

### Progressão POC → Protótipo → MVP

#### POC (persistência básica)

**10.1: Persistência básica de sessões (movido do Épico 9.10)**
- Sessões sobrevivem reload da página
- Implementação inicial: localStorage (navegador) OU SqliteSaver (backend)
- Thread_id vinculado à sessão
- Sidebar recupera lista de sessões ao recarregar

**10.2: Argumento Focal Persistente (movido do Épico 7.14)**
- Campo `focal_argument` salvo junto com sessão
- Recuperado ao retomar conversa
- Permite sistema entender contexto mesmo após dias

**10.3: Pausar e retomar sessão**
- Usuário pode fechar navegador e voltar depois
- Histórico completo preservado (mensagens + bastidores)
- State do LangGraph recuperado via thread_id

**Critérios de aceite POC:**
- Usuário pode fechar navegador e retomar sessão depois
- Histórico de mensagens preservado
- Argumento focal recuperado corretamente
- Sistema continua conversa de onde parou

#### Protótipo (múltiplas sessões)

**10.4: Múltiplas sessões persistidas**
- Sidebar exibe lista de todas as sessões salvas
- Usuário pode criar nova sessão a qualquer momento
- Alternar entre sessões (não simultâneo)

**10.5: Busca de sessões**
- Buscar por título da conversa
- Buscar por data (últimos 7 dias, último mês)
- Filtrar por estágio (se argumento focal incluir estágio)

**10.6: Artefatos versionados**
- Sistema salva versões de hipóteses (V1, V2, V3)
- Timeline mostra evolução de artefatos
- Usuário pode ver "como era antes" de cada refinamento

**10.7: Histórico de decisões do usuário (movido do Épico 7.13)**
- Sistema rastreia decisões: aceitou/refutou sugestões de agentes
- Identifica padrões de preferência (ex: usuário sempre prefere refinar antes de pesquisar)
- Adapta sugestões futuras baseado em histórico

**Critérios de aceite Protótipo:**
- Usuário gerencia múltiplas sessões
- Busca funciona corretamente
- Versões de hipóteses rastreadas
- Preferências do usuário influenciam sugestões

#### MVP (gestão completa)

**10.8: Export de conversas**
- Exportar conversa completa em markdown
- Incluir: mensagens + reasoning dos agentes + métricas
- Formato: `conversa_YYYYMMDD.md`

**10.9: Arquivar sessões concluídas**
- Marcar sessão como "concluída"
- Sessões concluídas movem para seção "Arquivadas"
- Não aparecem na lista principal (reduz poluição visual)

**10.10: Tags/labels customizáveis**
- Usuário pode adicionar tags (ex: "urgente", "revisão", "tese")
- Filtrar sessões por tags
- Busca inclui tags

**Critérios de aceite MVP:**
- Export funciona (markdown legível)
- Arquivamento organiza sessões
- Tags facilitam organização

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
