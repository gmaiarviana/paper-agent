# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/vision/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Concluídos
- Infraestrutura base completa
- **ÉPICO 1**: Convergência Orgânica
- **ÉPICO 2**: Sidebar
- **ÉPICO 3**: Bastidores
- **ÉPICO 4**: Contexto
- **ÉPICO 5**: UX Polish
- **ÉPICO 6**: Limpeza de Testes
- **ÉPICO 7**: Validação de Maturidade do Sistema - Fase Manual
- **ÉPICO 8**: Análise Assistida de Qualidade - Ferramentas para Discussão
- **ÉPICO 9**: Integração Backend↔Frontend

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Planejados (refinados)
- _Nenhum épico refinado planejado no momento_

#### Planejados (não refinados)
- **ÉPICO 10**: Conceitos (não refinado)
- **ÉPICO 11**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 12**: Pesquisador (não refinado)
- **ÉPICO 13**: Escritor (não refinado)


**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 5: UX Polish

**Objetivo:** Ajustes de experiência do usuário: custo em R$.

**Status:** ✅ Concluído

Custos exibidos em reais (BRL) com formato brasileiro, aplicado em toda interface (chat, backstage, dashboard).

---

## ÉPICO 6: Limpeza de Testes

**Objetivo:** Remover testes burocráticos e adicionar testes de integração reais onde há mocks superficiais.

**Status:** ✅ Concluído

Suite de testes limpa e focada: testes burocráticos removidos, testes de integração reais adicionados para validar comportamento do LLM, documentação atualizada com novos padrões.

---

## ÉPICO 7: Validação de Maturidade do Sistema - Fase Manual

**Objetivo:** Validar que sistema multi-agente funciona como deveria através de roteiro de cenários críticos executados manualmente.

**Status:** ✅ Concluído

**Dependências:** Nenhuma (pode começar imediatamente)

**Duração estimada:** 1-2 dias (criação do roteiro) + 2-3 horas (execução)

**Consulte:** `docs/testing/epic7_validation_strategy.md` para estratégia completa

### Funcionalidades:

#### 7.1 Criar Roteiro de Validação Manual ✅

- **Status:** ✅ Concluído
- **Descrição:** Criar roteiro estruturado com 10-15 cenários críticos que validam comportamento do sistema multi-agente
- **Critérios de Aceite:**
  - ✅ `docs/testing/epic7_validation_strategy.md` criado com estratégia completa
  - ✅ 10 cenários críticos definidos cobrindo:
    - Transições entre agentes (Orquestrador → Estruturador → Metodologista)
    - Preservação de contexto (focal_argument, messages)
    - Decisões coerentes (next_step, agent_suggestion)
    - Fluidez conversacional (sem quebras)
    - Provocação socrática (reflection_prompt)
    - Reasoning loop (Metodologista)
  - ✅ Cada cenário especifica input, comportamento esperado, logs necessários e critérios de sucesso/falha

#### 7.2 Executar Cenários e Coletar Logs ✅

- **Status:** ✅ Concluído
- **Descrição:** Executar cenários manualmente e coletar logs estruturados
- **Critérios de Aceite:**
  - ✅ 10/10 cenários executados no sistema real
  - ✅ Logs estruturados coletados (EventBus JSON + outputs) em `docs/testing/epic7_results/`
  - ✅ Comportamento observado anotado (sucesso/falha/parcial) em cada `execution_report.md`
  - ✅ 1 problema crítico identificado e corrigido (Turno 1 bloqueando chamada de agente)

#### 7.3 Analisar Resultados e Gerar Relatório de Maturidade ✅

- **Status:** ✅ Concluído
- **Descrição:** Analisar logs e gerar relatório de maturidade do sistema
- **Critérios de Aceite:**
  - ✅ Todos os logs analisados
  - ✅ Problemas classificados (1 crítico corrigido, sistema maduro)
  - ✅ Relatório de maturidade gerado em `docs/testing/epic7_results/summary.md` com:
    - Sumário executivo (sistema maduro após correção)
    - Problemas por categoria (transições, contexto, decisões, fluidez)
    - Recomendações de correções (aplicadas)
    - Priorização de correções (crítico resolvido)
  - ✅ Documentado o que funciona bem (10/10 cenários bem-sucedidos após correção)

---

## ÉPICO 8: Análise Assistida de Qualidade - Ferramentas para Discussão

**Objetivo:** Facilitar análise humana de qualidade conversacional através de ferramentas que estruturam dados para discussão eficiente com LLM.

**Status:** ✅ Concluído (8.1 e 8.2 implementados; 8.3-8.5 opcionais e não priorizados)

**Dependências:** Épico 7 (precisa identificar problemas reais primeiro)

**Duração estimada:** 6 dias (planejado) / 2-3 dias (executado - apenas 8.1 e 8.2)

**Custo estimado:** ~$0.10-0.20 por execução completa (discussão com Claude)

**Filosofia:** Análise assistida (humano + LLM) > Automação completa (perde contexto e qualidade)

**Consulte:** `docs/testing/epic8_automation_strategy.md` para estratégia completa

### Motivação

**Insight do Épico 7:**
O valor NÃO veio de automação, mas de **discussão contextualizada**:
- Investigação interativa ("me mostre os logs", "por que isso?")
- Decisões estratégicas debatidas (baseline opcional?)
- Planejamento adaptativo (pivotamos de manual → automatizado)
- **Humano + Claude analisando JUNTOS**

**Problema:**
- Validação manual (Épico 7) foi eficaz mas trabalhosa (~2-3h)
- Precisamos reduzir tempo de setup
- MAS: Automação completa perde contexto e qualidade

**Solução:**
- Ferramentas que **estruturam dados** para análise
- Output formatado para **fácil discussão** com LLM
- Humano + Claude fazem análise (não script)
- **Mantém qualidade, reduz trabalho manual**

**Resultado Esperado:**
- Rodar cenário completo: 1 comando
- Gerar relatório estruturado: automático
- Colar no Claude e discutir: 30 segundos
- Identificar causa raiz: minutos (não horas)
- **60-75% mais rápido que manual, mantém qualidade**

---

### Funcionalidades (8.1 - 8.5)

#### 8.1 Multi-Turn Executor ✅

- **Status:** ✅ Implementado
- **Objetivo:** Rodar cenários completos end-to-end (3-5 turnos)
- **Descrição:** Executar conversas completas end-to-end para validar fluxos multi-agente
- **Critérios de Aceite:**
  - ✅ `MultiTurnExecutor` criado em `utils/test_executor.py`
  - ✅ `ConversationScenario` criado em `utils/test_scenarios.py`
  - ✅ Fixture `multi_turn_executor` disponível em `tests/conftest.py`
  - ✅ Suporta execução de cenários multi-turn (3-5 turnos)
  - ✅ Rastreia agentes chamados, preserva estado entre turnos
  - ✅ Coleta métricas (tokens, custo, duração)
  - ✅ `scripts/testing/run_scenario.py` criado (executa cenário específico via CLI)
  - ✅ `scripts/testing/run_all_scenarios.py` criado (executa todos os cenários)
  - ✅ Testes de integração em `tests/integration/test_multi_turn_flows.py`
- **Tempo estimado:** 2 dias
- **Tempo real:** ~2 dias

#### 8.2 Scripts de Execução e Relatórios Estruturados ✅

- **Status:** ✅ Implementado
- **Objetivo:** Formatar dados de forma otimizada para análise com LLM
- **Descrição:** Scripts que executam cenários e geram relatórios estruturados para análise humana
- **Critérios de Aceite:**
  - ✅ `scripts/testing/run_scenario.py` criado (executa cenário específico via CLI)
  - ✅ `scripts/testing/run_all_scenarios.py` criado (executa todos os cenários)
  - ✅ `scripts/testing/debug_scenario.py` criado (debug mode com logs detalhados)
  - ✅ `scripts/testing/collect_scenario_logs.py` criado (coleta logs estruturados)
  - ✅ Relatórios formatados para terminal (comportamento esperado vs observado)
  - ✅ Suporte a salvar resultados em JSON (`--save`)
- **Tempo estimado:** 1 dia
- **Tempo real:** ~1 dia

#### 8.3 Comparison Tool ⏳

- **Status:** ⏳ Planejado (prioridade baixa)
- **Objetivo:** Comparar antes/depois de mudanças no prompt para detectar regressões
- **Descrição:** Implementar ferramenta que compara resultados de execução antes/depois de mudanças no código/prompt, identifica regressões automaticamente, e gera relatório de impacto estruturado para discussão
- **Critérios de Aceite:**
  - Deve implementar `compare_results()` em `utils/result_comparer.py`
  - Deve implementar `detect_regressions()` para identificar regressões automaticamente
  - Deve implementar `compare_results.py` com CLI
  - Output deve incluir resumo de mudanças e lista de cenários que precisam atenção
- **Tempo estimado:** 1 dia
- **Prioridade:** 🟡 ALTA (mas não implementado)

#### 8.4 Interactive Analysis Mode ⏳

- **Status:** ⏳ Planejado (prioridade baixa)
- **Objetivo:** Guiar fluxo de investigação de forma interativa
- **Descrição:** Implementar modo interativo que apresenta menu de opções, executa ações conforme escolha do usuário, e gera outputs estruturados para discussão
- **Critérios de Aceite:**
  - Deve implementar `interactive_analyzer.py` em `scripts/testing/`
  - Menu inicial deve listar cenários disponíveis
  - Após executar cenário, deve oferecer opções de análise
  - Deve ser intuitivo (não requer documentação para usar)
- **Tempo estimado:** 1 dia
- **Prioridade:** 🟡 ALTA (mas não implementado)

#### 8.5 Debug Workflow ⏳

- **Status:** ⏳ Parcialmente implementado
- **Objetivo:** Facilitar troubleshooting de problemas sutis com logs detalhados
- **Descrição:** Implementar workflow de debug que gera logs completos (prompt enviado, resposta bruta, reasoning do LLM, decisões step-by-step) quando problema é identificado
- **Critérios de Aceite:**
  - ✅ `scripts/testing/debug_scenario.py` criado (debug mode com logs detalhados)
  - ⏳ `generate_debug_report()` em `utils/debug_reporter.py` (parcial)
  - ⏳ Logs formatados com marcadores visuais completos
  - ⏳ Comparação antes/depois de mudanças no prompt (futuro)
- **Tempo estimado:** 1 dia
- **Prioridade:** 🟡 ALTA (parcialmente implementado)

---

### Cronograma Épico 8 (Planejado vs Executado)

| Funcionalidade | Duração Planejada | Duração Real | Dependências | Prioridade | Status |
|----------------|-------------------|--------------|--------------|------------|--------|
| 8.1: Multi-Turn Executor | 2 dias | ~2 dias | - | 🔴 CRÍTICA | ✅ Concluído |
| 8.2: Scripts e Relatórios | 1 dia | ~1 dia | 8.1 | 🔴 CRÍTICA | ✅ Concluído |
| 8.3: Comparison Tool | 1 dia | - | 8.1 | 🟡 ALTA | ⏳ Não implementado |
| 8.4: Interactive Mode | 1 dia | - | 8.1, 8.2 | 🟡 ALTA | ⏳ Não implementado |
| 8.5: Debug Workflow | 1 dia | ~0.5 dia | 8.1 | 🟡 ALTA | ⏳ Parcial |
| **Total** | **6 dias** | **~3.5 dias** | | | |

**Mudanças em relação à proposta original:**
- ✅ 8.1 e 8.2 implementados conforme planejado
- ⏳ 8.3-8.5 não implementados (prioridade reduzida após validação de que 8.1+8.2 são suficientes)
- ✅ Decisão estratégica: focar em ferramentas essenciais primeiro

---

### Custo Estimado

**Uso das Ferramentas (Sem Custo LLM):**
- Rodar cenário: $0 (apenas execução local)
- Gerar relatório: $0 (formatação de dados)
- Debug logs: $0 (extração de logs)
- Comparação: $0 (diff de arquivos JSON)

**Discussão com Claude (Custo LLM):**
- Por problema investigado: ~$0.01-0.02 (5-10 mensagens)
- Suite completa (10 cenários): ~$0.10-0.20 (se todos tiverem problemas)
- Execução semanal: ~$0.10-0.15 (desenvolvimento típico)

**Comparado com Épico 7:**
- Épico 7 manual: ~2-3h de trabalho, $0.13
- Épico 8 assistido: ~30-45min de trabalho, $0.10-0.20
- **Economia:** 60-75% do tempo, custo similar

---

### Aprendizados do Épico 7 que Moldaram este Épico

#### 1. Discussão Contextualizada Gera Mais Valor

**O que funcionou:**
- Investigação interativa com Claude
- Análise de logs detalhados
- Decisões estratégicas debatidas

**O que NÃO teria funcionado:**
- LLM-as-Judge: "Score: 4/5"
- Automação superficial sem contexto

#### 2. Multi-Turn É Crítico

**Problema:** Cenários 3 e 6 ficaram incompletos (script single-turn)
**Solução:** Multi-turn executor é funcionalidade #1

#### 3. Debug Detalhado Foi Essencial

**Problema:** `debug_scenario_2.py` revelou causa raiz
**Solução:** Debug mode embutido no framework

#### 4. Humano Toma Decisões Estratégicas

**Exemplos:** Baseline opcional? Cenário mal definido?
**Solução:** LLM assiste, humano decide

#### 5. CI/CD É Prematuro

**Decisão:** Postergar para Épico 10+ (se necessário)

---

### Documentação

Após implementação, deve atualizar:
- ✅ `docs/testing/epic8_automation_strategy.md` (já reformulado)
- ⏳ `docs/testing/strategy.md` (adicionar seção sobre análise assistida)
- ⏳ `README.md` (adicionar seção sobre ferramentas de análise)

Cada ferramenta deve ter:
- ✅ Exemplos de uso em comentários do código
- ✅ Output de exemplo em docstrings
- ⏳ Seção no README com comandos principais

---

## ÉPICO 9: Integração Backend↔Frontend

**Objetivo:** Completar ciclo de persistência silenciosa e feedback visual de progresso.

**Status:** ✅ Concluído

**Dependências:** Nenhuma

**Duração estimada:** 2-3 dias

### Funcionalidades:

#### 9.1 Atualização de cognitive_model no Orchestrator ✅

- **Status:** Concluído
- **Descrição:** Implementar atualização do cognitive_model no orchestrator_node a cada turno
- **Critérios de Aceite:**
  - Prompt do orchestrator solicita `cognitive_model` no JSON de saída
  - Orchestrator extrai `cognitive_model` da resposta LLM
  - Orchestrator retorna `cognitive_model` no state update
  - Schema `CognitiveModel` usado para validação (Pydantic)
  - Campos: claim, premises, assumptions, open_questions, contradictions, solid_grounds, context

#### 9.2 Passar active_idea_id via Config ✅

- **Status:** Concluído
- **Descrição:** Disponibilizar active_idea_id no config do LangGraph (agnóstico de framework)
- **Critérios de Aceite:**
  - Streamlit adiciona `active_idea_id` ao config ao invocar grafo
  - Orchestrator acessa `active_idea_id` via `config.get("configurable", {})`
  - Funciona mesmo sem active_idea_id (opcional, não quebra fluxo)

#### 9.3 SnapshotManager no Orquestrador ✅

- **Status:** Concluído
- **Descrição:** Integrar avaliação de maturidade via LLM no orchestrator_node
- **Critérios de Aceite:**
  - Orchestrator chama `create_snapshot_if_mature()` após processar turno
  - Usa `SnapshotManager.assess_maturity()` existente (LLM avalia maturidade)
  - Threshold de confiança configurável (padrão: 0.8)
  - Silencioso: sem logs visíveis ao usuário, sem notificações
  - Depende de 9.1 (cognitive_model) e 9.2 (active_idea_id)

#### 9.4 Indicador de Solidez no Contexto ✅

- **Status:** Concluído
- **Descrição:** Exibir barra de progresso de solidez do argumento focal
- **Critérios de Aceite:**
  - Backend: Método reutilizável calcula solidez (ex: `CognitiveModel.calculate_solidez()`)
  - Frontend: Exibe barra de progresso (0-100%) no painel Contexto
  - Atualiza quando argumento focal muda
  - Agnóstico de framework (cálculo no backend, UI apenas exibe)

**Ordem de implementação:** 9.1 → 9.2 → 9.3 → 9.4 ✅

---

## ÉPICO 10: Conceitos

**Objetivo:** Criar entidade Concept com vetores semânticos para busca por similaridade ("produtividade" encontra "eficiência").

**Status:** ⏳ Planejado (não refinado)

> **📖 Filosofia:** Conceitos são essências globais (biblioteca única). Ideias referenciam conceitos, não os possuem. Ver `docs/architecture/ontology.md`.

**Dependências:**
- Épico 9

**Consulte:**
- `docs/architecture/concept_model.md` - Schema técnico de Concept
- `docs/architecture/tech_stack.md` - ChromaDB, embeddings, sentence-transformers
- `docs/architecture/ontology.md` - Filosofia: Conceitos como essências globais

### Funcionalidades:

#### 10.1 Setup ChromaDB Local [POC]

- **Descrição:** Configurar ChromaDB para armazenar vetores semânticos de conceitos (gratuito, local).
- **Critérios de Aceite:**
  - Deve instalar dependências: `chromadb`, `sentence-transformers`
  - Deve criar cliente persistente: `chromadb.PersistentClient(path="./data/chroma")`
  - Deve criar collection: `concepts` (metadata: label, essence, variations)
  - Deve usar modelo: `all-MiniLM-L6-v2` (384 dim, 80MB download)

#### 10.2 Schema SQLite de Concept [POC]

- **Descrição:** Criar tabelas `concepts` e `idea_concepts` para metadados estruturados e relacionamento N:N.
- **Critérios de Aceite:**
  - Deve criar tabela `concepts`: id, label, essence, variations JSON, chroma_id
  - Deve criar tabela `idea_concepts`: idea_id, concept_id (N:N, PK composta)
  - Campo `chroma_id` deve referenciar registro no ChromaDB
  - Deve criar índices: ON label, ON idea_id, ON concept_id
  - Conceitos são globais (biblioteca única), ideias referenciam via `idea_concepts`

#### 10.3 Pipeline de Detecção de Conceitos [POC]

- **Descrição:** LLM extrai conceitos-chave quando argumento amadurece (ao criar snapshot de Idea) e salva em ChromaDB + SQLite.
- **Critérios de Aceite:**
  - Deve disparar detecção ao criar snapshot de Idea (quando argumento amadurece)
  - Deve detectar conceitos via LLM (prompt: "Extrair conceitos-chave desta ideia/argumento")
  - Deve gerar embedding via sentence-transformers
  - Deve salvar no ChromaDB (vetor) + SQLite (metadata)
  - Deve criar registro em `idea_concepts` (linking N:N)
  - **Não** deve executar detecção a cada mensagem (apenas no snapshot)

#### 10.4 Busca Semântica [POC]

- **Descrição:** Buscar conceitos similares via embeddings (threshold > 0.80 = mesmo conceito).
- **Critérios de Aceite:**
  - Deve implementar: `find_similar_concepts(query: str, top_k: int) -> list[Concept]`
  - Deve calcular similaridade cosseno entre embeddings
  - Deve usar threshold 0.80 para deduplicação ("produtividade" = "eficiência")
  - Deve retornar lista ordenada por similaridade

#### 10.5 Variations Automáticas [Protótipo]

- **Descrição:** Sistema detecta variações linguísticas e adiciona ao Concept existente (colaboração = cooperação) com thresholds diferenciados.
- **Critérios de Aceite:**
  - Deve detectar variações via busca semântica durante detecção de conceitos
  - **Threshold > 0.90:** adicionar variation automaticamente ao Concept existente
  - **Threshold 0.80-0.90:** perguntar ao usuário: "São o mesmo conceito?" (colaboração = cooperação?)
  - Deve adicionar variation ao Concept existente se confirmado
  - Deve criar novo Concept se usuário rejeitar ou similaridade < 0.80

#### 10.6 Mostrar Conceitos na Interface [Protótipo]

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

## ÉPICO 11: Alinhamento de Ontologia

**Objetivo:** Migrar código atual (premises/assumptions como strings separadas) para nova ontologia (Proposição unificada com solidez derivada de Evidências).

**Status:** ⏳ Planejado (não refinado)

**Abordagem:** Evolução gradual, não refatoração big-bang.

**Dependências:**
- Épicos 9-10 concluídos

**Referências:**
- `docs/architecture/ontology.md` - Nova ontologia
- `docs/vision/epistemology.md` - Fundamentos epistemológicos

---

## ÉPICO 12: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 11

---

## ÉPICO 13: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
