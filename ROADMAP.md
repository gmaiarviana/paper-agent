# ROADMAP - Paper Agent

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [BACKLOG.md](BACKLOG.md).

## 📋 Status dos Épicos

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 5: Interface Conversacional e Transparência
- ÉPICO 6: Memória Dinâmica e Contexto por Agente
- ÉPICO 7: Orquestrador Conversacional Inteligente (POC refinado)

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 8: Pipeline Completo Ideia → Artigo
- ÉPICO 9: Debate Multi-Agente Mediado

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## ✅ ÉPICOS CONCLUÍDOS

**ÉPICO 4: Loop Colaborativo + Refinamento Iterativo** (12/11/2025)  
Sistema multi-agente conduz refinamentos sucessivos da hipótese com feedback estruturado, versionamento explícito e decisão forçada quando o limite de iterações é atingido.

**ÉPICO 3: Orquestrador + Estruturador (Base Multi-Agente)**  
Orquestrador coordena metodologista e estruturador, avaliando maturidade da ideia, integrando respostas e registrando justificativas.

**ÉPICO 5: Interface Conversacional e Transparência (parcial)** (13/11/2025)  
Funcionalidade 5.1 concluída: Dashboard Streamlit com timeline de eventos em tempo real.

**ÉPICO 6: Memória Dinâmica e Contexto por Agente (parcial)** (13/11/2025)  
Funcionalidade 6.1 concluída: Configuração externa de agentes via YAML. 

#### 6.2 Registro de Memória com Metadados
- **Status:** ✅ Concluído (13/11/2025)
- **Descrição:** Armazenar histórico leve por agente com tokens e resumo da última ação.
- **Entregue:**
  - Infraestrutura do `MemoryManager` com export, totais e API Python
  - Helper `register_execution()` para captura de tokens de AIMessage
  - Instrumentação completa dos nós: orchestrator, structurer, methodologist (decide_collaborative e force_decision)
  - MemoryManager passado via config do super-grafo (opcional)
  - Integração com CostTracker validada (custos calculados e registrados)
  - CLI atualizado para exibir métricas de tokens e custos por agente
  - Script de validação end-to-end: `scripts/flows/validate_memory_integration.py`
  - Versões atualizadas: orchestrator_node v2.1, structurer_node v3.1, methodologist nodes v3.1

---

## 📋 PRÓXIMAS FUNCIONALIDADES

## ÉPICO 7: Orquestrador Conversacional Inteligente

**Objetivo:** Transformar sistema de "trilho fixo" em diálogo adaptativo onde usuário e sistema decidem caminho juntos através de negociação contínua.

**Status:** 🟡 Parcialmente refinado - POC pronto, Protótipo e MVP aguardam refinamento

**Dependências:**
- Épico 6.2 concluído ✅

**Consulte:** 
- `docs/orchestration/conversational_orchestrator.md` - especificação técnica completa
- `docs/product/conversation_patterns.md` - padrões de conversa esperados

---

#### POC (primeira entrega - ✅ REFINADO)

**Status:** Pronto para implementação

**Funcionalidades:**

**7.1: Exploração com Perguntas Abertas**
- Orquestrador faz perguntas abertas para entender intenção
- Não classifica automaticamente (vague/semi_formed/complete)
- Remove lógica de classificação atual
- Exemplo: "Interessante! Você quer VER literatura ou TESTAR hipótese?"

**7.2: Análise Contextual**
- Analisa input + histórico completo da conversa
- Identifica o que está claro e o que falta
- Detecta padrões: crença vs observação vs hipótese
- Constrói "argumento focal" implícito (via histórico)

**7.3: Sugestão com Justificativa**
- Sugere próximos passos com razão clara
- Sempre apresenta opções, não decide sozinho
- Exemplo: "Posso chamar Metodologista porque você mencionou população e métricas"

**7.4: Detecção de Mudança de Direção**
- LLM compara novo input com histórico
- Detecta contradições ou mudanças de foco
- Adapta sem questionar mudanças
- Atualiza argumento focal implícito

**Critérios de aceite POC:**
- ✅ Sistema conversa antes de chamar agente
- ✅ Perguntas abertas (não classificação)
- ✅ Análise contextual (não garçom)
- ✅ Sugestões com justificativa
- ✅ Detecção de mudança via LLM
- ✅ Conversação natural (não números/keywords)

**Tarefas de implementação:**
- [ ] 7.1.1: Criar `ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1` em `utils/prompts.py`
- [ ] 7.1.2: Substituir `orchestrator_node` atual em `agents/orchestrator/nodes.py`
- [ ] 7.1.3: Implementar `_build_context()` para construir histórico completo
- [ ] 7.1.4: Adicionar parsing de JSON response com error handling
- [ ] 7.1.5: Atualizar `MultiAgentState` com campos: `orchestrator_analysis`, `next_step`, `agent_suggestion`
- [ ] 7.1.6: Remover `route_from_orchestrator` (não mais necessário)
- [ ] 7.1.7: Criar testes unitários: `tests/unit/test_orchestrator_conversational.py`
- [ ] 7.1.8: Criar script de validação: `scripts/flows/validate_conversational_orchestrator.py`
- [ ] 7.1.9: Atualizar CLI para exibir raciocínio do orquestrador
- [ ] 7.1.10: Atualizar Dashboard para exibir "argumento focal" implícito

**Limitações conhecidas do POC:**
- Argumento focal é implícito (via histórico) - será explícito no Protótipo
- Ignora limite de contexto do Claude - será tratado no Protótipo
- Raciocínio básico - será refinado no Protótipo

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

### Ordem proposta:
1. **Setup** → valida ambiente ✅
2. **Metodologista isolado** → valida um agente ✅ (falta 2.6-2.8)
3. **Orquestrador** → valida reasoning/decisão
4. **Interface** → valida transparência
5. **LangGraph avançado** → valida arquitetura final
