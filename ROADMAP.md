# ROADMAP - Paper Agent

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [BACKLOG.md](BACKLOG.md).

## 📋 Status dos Épicos

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 5: Interface Conversacional e Transparência
- ÉPICO 6: Memória Dinâmica e Contexto por Agente
- ÉPICO 7: Orquestrador Conversacional Inteligente (POC ✅ implementado)

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 8: Pipeline Completo Ideia → Artigo
- ÉPICO 9: Debate Multi-Agente Mediado

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

#### 7.8: Handling de Contexto Longo ⚠️
- **Descrição:** Truncamento inteligente quando histórico excede limite de contexto
- **Status:** Não implementado (complexidade média-alta, baixa prioridade)
- **Razão:** Sistema funciona sem isso no Protótipo. Conversas curtas não atingem limite.
- **Planejamento:** Implementar depois de validar Protótipo em uso real

---

#### MVP (terceira entrega - ⚠️ NÃO REFINADO)

**Status:** Aguarda refinamento após Protótipo validado

**Funcionalidades planejadas:**

#### 7.9: Argumento Focal Explícito
- **Descrição:** Campo explícito no state para argumento focal da conversa (extraído do histórico)
- **Critérios de Aceite:**
  - Orquestrador extrai e atualiza argumento focal automaticamente
  - Campo `focal_argument` presente no state do Orquestrador
  - Usado como contexto prioritário nas decisões de roteamento
  - Persistido entre turnos da conversa

#### 7.10: Provocação de Reflexão
- **Descrição:** Orquestrador sugere ângulos não explorados ("Você pensou em X?")
- **Critérios de Aceite:**
  - Detecta quando usuário pode estar pensando de forma limitada
  - Sugere alternativas ou perspectivas não mencionadas
  - Integrado naturalmente no fluxo conversacional
  - Não interrompe fluxo se usuário quer focar em direção específica

#### 7.11: Detecção Emergente de Estágio
- **Descrição:** Orquestrador detecta transição natural de exploration → hypothesis
- **Critérios de Aceite:**
  - Identifica quando usuário convergiu para hipótese formada
  - Sugere mudança de estágio (exploration → hypothesis)
  - Usuário pode confirmar ou refutar detecção

#### 7.12: Reasoning Explícito das Decisões
- **Descrição:** Orquestrador expõe raciocínio detalhado por trás de cada decisão
- **Critérios de Aceite:**
  - Reasoning estruturado e legível
  - Exibido no Dashboard em tempo real
  - Disponível via flag `--verbose` na CLI
  - Ajuda usuário a entender "por quê" de cada sugestão

#### 7.13: Histórico de Decisões do Usuário
- **Descrição:** Sistema aprende padrões de preferências do usuário ao longo do tempo
- **Critérios de Aceite:**
  - Rastreia decisões do usuário (aceitou/refutou sugestões)
  - Identifica padrões de preferência
  - Adapta comportamento futuro baseado em histórico
  - Preferências persistidas entre sessões

#### 7.14: Argumento Focal Persistente
- **Descrição:** Integração com entidade Topic do Épico 8 para persistir argumento focal
- **Critérios de Aceite:**
  - Argumento focal vinculado a Topic persistente
  - Retomável entre sessões
  - Evolui com o tempo (versão V1, V2, etc.)
  - Integração com Épico 8 (dependência)

---

## ÉPICO 8: Entidade Tópico + Persistência Básica

**Objetivo:** Permitir pausar/retomar conversas com contexto completo preservado, suportando múltiplos tópicos em evolução.

**Status:** ⚠️ Não refinado

**Dependências:**
- Épico 7 POC concluído

**Consulte:** `docs/architecture/state_evolution.md` para detalhes de evolução de estado.

### Progressão POC → Protótipo → MVP

#### POC (persistência básica)
- 8.1: Modelo de dados Tópico (id, title, stage, artifacts)
- 8.2: Persistência em SqliteSaver (salva checkpoints LangGraph)
- 8.3: CLI: comandos `list`, `resume <id>`, `new`

**Critérios de aceite POC:**
- Usuário pode listar tópicos ativos
- Pode retomar conversa de ontem com contexto preservado
- Pode criar novo tópico a qualquer momento

#### Protótipo (artefatos e timeline)
- 8.4: Artefatos versionados (hypotheses V1/V2, research_notes, decisions)
- 8.5: Timeline de evolução do tópico

**Critérios de aceite Protótipo:**
- Sistema rastreia versões de hipóteses (V1 → V2 → V3)
- Usuário pode ver evolução temporal do tópico
- Artefatos são recuperáveis

#### MVP (gestão completa)
- 8.6: Múltiplos tópicos ativos (trabalha um por vez)
- 8.7: Busca por tópicos (título, stage, data)

**Critérios de aceite MVP:**
- Usuário gerencia vários tópicos simultaneamente
- Pode buscar "tópicos sobre LLMs"
- Dashboard mostra todos os tópicos em progresso

---

## ÉPICO 9: Finalizar Interface + Telemetria

**Objetivo:** Dashboard visual completo mostrando raciocínio do sistema em tempo real com métricas detalhadas.

**Status:** 🟡 Parcialmente refinado

**Dependências:**
- Épico 7 POC (para exibir decisões do Orquestrador)

### Funcionalidades (sem progressão - podem ser feitas em paralelo)

#### 9.1: Métricas de Tokens e Custo (ex-5.2)
- Exibir tokens_input, tokens_output, tokens_total por agente
- Calcular custo por agente e custo total da sessão
- Alerta quando custo ultrapassar limite configurável

#### 9.2: Resumo Sintético do Pensamento (ex-5.3)
- Feed com resumo curto (≤280 chars) do raciocínio de cada agente
- Botão para expandir e ver resposta completa
- Exportar feed em JSON

#### 9.3: Integração CLI com Telemetria (ex-5.4)
- CLI gera eventos estruturados consumidos pelo Streamlit
- Canal: arquivo JSONL em `runtime/streams/`
- Falhas no dashboard não bloqueiam CLI

#### 9.4: Reset Global de Sessão (ex-6.3)
- CLI oferece comando/flag `--reset` para limpar sessão
- Remove históricos dos agentes sem afetar logs emitidos
- Backlog: reset individual por agente

#### 9.5: Telemetria do Super-Grafo (ex-6.4)
- Cada nó registra tokens e resumo ao concluir
- MultiAgentState expõe estatísticas consolidadas
- Logs emitem alertas quando limites são ultrapassados

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
