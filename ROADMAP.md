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
- Argumento focal implícito (via histórico) - será explícito no Protótipo
- Ignora limite de contexto - será tratado no Protótipo
- Raciocínio básico - será refinado no Protótipo

**Consulte:** 
- `docs/orchestration/conversational_orchestrator.md` - especificação técnica completa
- `docs/product/conversation_patterns.md` - padrões de conversa esperados

---

#### Protótipo (segunda entrega - ⚠️ NÃO REFINADO)

**Status:** Aguarda refinamento após POC validado

**Funcionalidades planejadas:**
- 7.5: Argumento focal explícito (campo no state)
- 7.6: Detecção inteligente avançada
- 7.7: Provocação de reflexão ("Você pensou em X?")
- 7.8: Handling de contexto longo (truncamento inteligente)

---

#### MVP (terceira entrega - ⚠️ NÃO REFINADO)

**Status:** Aguarda refinamento após Protótipo validado

**Funcionalidades planejadas:**
- 7.9: Detecção emergente de estágio (exploration → hypothesis)
- 7.10: Reasoning explícito das decisões
- 7.11: Histórico de decisões do usuário (aprende preferências)
- 7.12: Argumento focal persistente (entidade Topic - integração com Épico 8)

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
