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
- **ÉPICO 5**: UX Polish - Custos exibidos em reais (BRL) com formato brasileiro
- **ÉPICO 6**: Limpeza de Testes - Suite de testes limpa e focada com testes de integração reais
- **ÉPICO 7**: Validação de Maturidade do Sistema - Validação manual com 10 cenários críticos executados
- **ÉPICO 8**: Análise Assistida de Qualidade - Ferramentas para execução multi-turn, relatórios estruturados, sistema de observabilidade completo e migração da estrutura de testes (226 unit tests, 11 smoke tests, estrutura modular por categoria)
- **ÉPICO 9**: Integração Backend↔Frontend - Persistência silenciosa e feedback visual de progresso completos
- **ÉPICO 10**: Observador - Mente Analítica (POC) - ChromaDB + SQLite para catálogo de conceitos, pipeline de persistência, busca semântica e 22 testes unitários
- **ÉPICO 11**: Alinhamento de Ontologia - Migração completa de premises/assumptions para Proposições unificadas com solidez. Sistema usa `proposicoes` em todas as camadas (modelo, orquestrador, observador, interface). Schema SQLite atualizado, testes migrados, documentação alinhada.
- **ÉPICO 12**: Observer - Integração Básica (MVP) - Observer integrado ao fluxo multi-agente via callback assíncrono. Processa turnos em background após Orchestrator, publica eventos cognitive_model_updated, e exibe atividade na Timeline. Orquestrador acessa cognitive_model via prompt context. 28 testes passando.

### 🟡 Épicos Em Andamento
- **ÉPICO 13**: Observer - Detecção de Mudanças (Não-Determinística) - Features 13.1-13.4 implementadas (66 testes), pendente: 13.5 Timeline Visual, 13.6 Testes E2E
- **ÉPICO 14**: Observer - Consultas Inteligentes - Base implementada (14.1-14.3), Observer identifica pontos de esclarecimento e sugere abordagens

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Refinados (prontos para implementação)
- **ÉPICO 15**: Observer - Painel Visual Dedicado

#### Planejados (não refinados)
- **ÉPICO 16**: Catálogo de Conceitos - Interface Web (não refinado)
- **ÉPICO 17**: Pesquisador (não refinado)
- **ÉPICO 18**: Escritor (não refinado)


**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ✅ ÉPICO 8: Análise Assistida de Qualidade

Ferramentas para execução multi-turn, relatórios estruturados, sistema de observabilidade completo e migração da estrutura de testes. Implementado: Multi-Turn Executor (8.1), Debug Mode (8.2), logging estruturado (JSONL), debug reports, session replay e reorganização completa dos testes em estrutura modular (unit/smoke/behavior/e2e). Resultado: 226 unit tests e 11 smoke tests passando, 0 falhas.

---

## ✅ ÉPICO 10: Observador - Mente Analítica (POC)

Observador implementado com ChromaDB + SQLite para catálogo de conceitos. Inclui pipeline de persistência com deduplicação automática (threshold 0.80), busca semântica via embeddings (all-MiniLM-L6-v2), e 22 testes unitários. Preparado para Agentic RAG (Epic 12) com parâmetros opcionais em `process_turn()`.

**Consulte:** `docs/agents/observer.md` - Documentação completa do Observador

---

## ✅ ÉPICO 11: Alinhamento de Ontologia

Migração completa de premises/assumptions (strings separadas) para Proposições unificadas com solidez. Sistema usa `proposicoes` em todas as camadas: modelo (Proposicao Pydantic), orquestrador (validação e fallbacks), observador (extração e mesclagem), interface (renderização com indicadores de solidez). Schema SQLite atualizado, testes migrados (377 testes Proposicao, 330 testes CognitiveModel), documentação técnica alinhada.

**Consulte:**
- `docs/architecture/ontology.md` - Nova ontologia (Proposição)
- `docs/vision/epistemology.md` - Base filosófica
- `docs/vision/cognitive_model/core.md` - Evolução de solidez

---

## ✅ ÉPICO 12: Observer - Integração Básica (MVP)

Observer integrado ao fluxo multi-agente via callback assíncrono em background thread. Processa turnos após Orchestrator sem aumentar latência, atualiza cognitive_model no estado, publica eventos cognitive_model_updated no EventBus, e exibe atividade na Timeline. Orquestrador acessa cognitive_model via prompt context com seção "COGNITIVE MODEL DISPONÍVEL". 28 testes passando.

**Consulte:**
- `docs/epics/epic-12-observer-integration.md` - Especificação técnica completa
- `docs/agents/observer.md` - Comunicação Observador ↔ Orquestrador
- `docs/architecture/observer_architecture.md` - Integração com grafo

---

## ÉPICO 13: Observer - Detecção de Mudanças (Não-Determinística)

**Objetivo:** Sistema detecta automaticamente variations vs mudanças reais usando análise contextual do LLM, sem métricas fixas ou thresholds.

**Status:** ✅ Refinado (pronto para implementação)

**Dependências:**
- Épico 12 (Observer integrado ao grafo)

**Filosofia:**
- LLM analisa contexto completo e decide se é variation ou mudança real
- Sem thresholds (0.8, 0.3, etc) - decisão 100% contextual
- Observador detecta silenciosamente, Orquestrador decide quando intervir
- "Grau de confusão" é avaliação qualitativa, não número

### Funcionalidades:

#### 13.1 Detecção de Variations vs Mudanças Reais (✅ Implementado)

- **Descrição:** Observador detecta se mudança de texto é variation (mesma essência) ou mudança real (essência diferente), consultando LLM com contexto completo.
- **Implementação:** `detect_variation()` em `agents/observer/extractors.py`
- **Critérios de Aceite:**
  - Quando subject/claim muda, Observador consulta LLM passando texto anterior, novo texto, e CognitiveModel completo
  - LLM analisa: "são variations do mesmo conceito ou mudança real?"
  - LLM responde naturalmente (sem forçar estrutura fixa)
  - Resultado disponível via `detect_variation(prev_text, new_text) -> dict`
  - Retorna análise do LLM (não booleano simples)
  - Observador NÃO decide automaticamente se interromper - apenas detecta

#### 13.2 Avaliação de Clareza da Conversa (✅ Implementado)

- **Descrição:** Observador analisa CognitiveModel e retorna avaliação de clareza da conversa via LLM.
- **Critérios de Aceite:**
  - Escala qualitativa: "cristalina" → "clara" → "nebulosa" → "confusa"
  - Score numérico 1-5 para parametrização
  - Flag `needs_checkpoint` para controle de fluxo
  - Factors: claim_definition, coherence, direction_stability
  - Orquestrador lê essa análise e decide (não é automático)
- **Implementação:** `evaluate_conversation_clarity()` em `agents/observer/extractors.py`

#### 13.3 Detecção Aprimorada de Mudança de Direção (✅ Implementado)

- **Descrição:** Orquestrador consulta Observador quando percebe mudança potencial, sem análise multi-dimensional automática.
- **Implementação:** `_consult_observer()` em `agents/orchestrator/nodes.py`
- **Critérios de Aceite:**
  - Orquestrador consulta `detect_variation()` do Observador a cada turno
  - Observador retorna análise contextual (classification: "variation" ou "real_change")
  - Orquestrador lê análise e decide se ajustar next_step
  - Logs informativos mostram detecção sem classificação rígida

#### 13.4 Checkpoints Contextuais (✅ Implementado)

- **Descrição:** Orquestrador usa análises do Observador para decidir quando solicitar esclarecimentos.
- **Implementação:** Campos `clarity_evaluation` e `variation_analysis` no state
- **Critérios de Aceite:**
  - Se `needs_checkpoint=True`, Orquestrador ajusta `next_step` para "clarify"
  - Clareza "cristalina"/"clara": continua sem intervenção
  - Clareza "nebulosa"/"confusa": sugere checkpoint
  - Mudança real detectada: trigger checkpoint para confirmação

#### 13.5 Timeline Visual de Mudanças

- **Descrição:** Timeline registra mudanças detectadas de forma discreta.
- **Critérios de Aceite:**
  - Eventos aparecem na timeline (colapsada por padrão): "🔄 Mudança de foco confirmada com usuário", "↪️ Variation identificada (não interrompeu fluxo)", "⚠️ Tensões detectadas, esclarecimento solicitado"
  - Variations: registro discreto (sem alerta)
  - Mudanças confirmadas: destaque suave
  - Não mostra métricas ou thresholds

**Sub-tarefas:**
- [ ] **13.5.1** Criar modelos de eventos em `utils/event_models.py`:
  - `VariationDetectedEvent` (classification, essence_previous, essence_new, shared_concepts, new_concepts)
  - `DirectionChangeConfirmedEvent` (classification, user_confirmed, previous_claim, new_claim)
  - `ClarityCheckpointEvent` (clarity_level, checkpoint_reason)
- [ ] **13.5.2** Adicionar métodos publish em `utils/event_bus/publishers.py`:
  - `publish_variation_detected()`
  - `publish_direction_change_confirmed()`
  - `publish_clarity_checkpoint()`
- [ ] **13.5.3** Publicar eventos em `agents/orchestrator/nodes.py`:
  - Publicar `VariationDetectedEvent` quando variação detectada
  - Publicar `DirectionChangeConfirmedEvent` quando mudança real
  - Publicar `ClarityCheckpointEvent` quando `needs_checkpoint=True`
- [ ] **13.5.4** Renderizar eventos em `app/components/backstage/timeline.py`:
  - Nova função `render_observer_detection_events()`
  - Exibir eventos com emojis discretos, seção colapsada
- [ ] **13.5.5** Testes unitários em `tests/unit/utils/test_event_bus_observer.py`

#### 13.6 Testes de Integração

- **Descrição:** Validação em cenários reais de conversa.
- **Critérios de Aceite:**
  - Testes multi-turn com variations e mudanças
  - Validação: Orquestrador intervém naturalmente (não roboticamente)
  - Validação: variations não interrompem
  - Validação: confusão gera perguntas contextuais
  - Script: `scripts/validate_direction_change.py`

**Sub-tarefas:**
- [ ] **13.6.1** Criar cenários de teste em `tests/integration/e2e/test_direction_change.py`:
  - Cenário A: Variação simples (não interrompe fluxo)
  - Cenário B: Mudança real (checkpoint solicitado)
  - Cenário C: Clareza nebulosa (needs_checkpoint=True)
  - Cenário D: Conversa clara (needs_checkpoint=False)
- [ ] **13.6.2** Criar script `scripts/validate_direction_change.py`:
  - Executa cenários A-D automaticamente
  - Gera relatório com eventos publicados e decisões
  - Modo verbose para debug
- [ ] **13.6.3** Implementar testes específicos:
  - `test_variation_does_not_interrupt_flow()`
  - `test_real_change_triggers_checkpoint()`
  - `test_confusion_triggers_clarification()`
  - `test_orchestrator_intervention_is_natural()`
- [ ] **13.6.4** Integrar validação em `utils/test_executor.py`:
  - Método `validate_observer_detections(scenario_result)`

---

## ÉPICO 14: Observer - Consultas Inteligentes

**Objetivo:** Quando Observer detecta confusão, sistema faz perguntas contextuais para esclarecer, ao invés de apenas apontar problemas.

**Status:** 🟡 Em Andamento - Base implementada (14.1-14.3)

**Dependências:**
- Épico 13 (detecção de variations e confusão)

**Filosofia:**
- Observer identifica o que precisa ser esclarecido
- Orquestrador formula perguntas naturais (não robóticas)
- Perguntas ajudam a avançar, não apenas apontam problemas
- Sistema age como parceiro pensante, não como fiscalizador

### Funcionalidades:

#### 14.1 Identificação de Pontos que Precisam Esclarecimento

- **Descrição:** Observer analisa CognitiveModel e identifica especificamente o que está confuso ou precisa ser esclarecido.
- **Critérios de Aceite:**
  - Método `identify_clarification_needs() -> dict` retorna: descrição textual do que precisa esclarecimento, contexto relevante (quais proposições, contradições, etc), sugestão de como perguntar
  - LLM analisa: contradições, open_questions, proposições frágeis, mudanças de claim
  - Resposta natural (não lista estruturada fixa)
  - Foca em avançar conversa, não apenas apontar problemas

#### 14.2 Geração de Perguntas Contextuais

- **Descrição:** Orquestrador usa análise do Observer para formular perguntas naturais e contextuais.
- **Critérios de Aceite:**
  - Quando Observer identifica necessidade de esclarecimento, Orquestrador lê sugestão do Observer
  - Formula pergunta em linguagem natural (não copia texto do Observer)
  - Pergunta é específica ao contexto (menciona conceitos da conversa)
  - Pergunta ajuda a avançar (não apenas aponta problema)
  - Exemplos de boas perguntas: "Você mencionou que LLMs aumentam produtividade, mas também aumentam bugs. Esses dois pontos se aplicam em contextos diferentes?"
  - Evita perguntas robóticas ou vagas

#### 14.3 Perguntas sobre Contradições (Tensões, não Erros)

- **Descrição:** Quando Observer detecta contradições, sistema pergunta sobre contextos diferentes ao invés de apontar erro.
- **Critérios de Aceite:**
  - Observer identifica contradições (já existe no Épico 12)
  - Orquestrador formula pergunta explorando possíveis contextos: "Esses dois pontos se aplicam em situações diferentes?"
  - Tom epistemológico: tensão entre proposições, não erro lógico
  - Permite usuário esclarecer contexto sem sentir que "errou"
  - Referência a `docs/vision/epistemology.md` (boa-fé epistemológica)

#### 14.4 Perguntas sobre Open Questions

- **Descrição:** Observer sugere perguntas para preencher gaps naturais na conversa.
- **Critérios de Aceite:**
  - Observer identifica open_questions (já existe)
  - Método `suggest_question_for_gap() -> Optional[str]` sugere pergunta para preencher gap
  - Orquestrador decide quando fazer pergunta (não automático)
  - Perguntas focam em avançar claim, não apenas coletar info
  - Exemplo: se claim é "LLMs aumentam produtividade" e falta evidência: "Você tem algum dado ou experiência que mostre esse aumento de produtividade?"

#### 14.5 Timing de Intervenção (Quando Perguntar)

- **Descrição:** Sistema decide quando fazer perguntas de esclarecimento sem interromper fluxo natural.
- **Critérios de Aceite:**
  - Orquestrador NÃO pergunta imediatamente após cada input
  - Pergunta quando: confusão se acumula (múltiplos sinais), usuário pausa ou muda tópico abruptamente, contradição aparece e persiste por 2+ turns, open question importante fica sem resposta
  - NÃO pergunta quando: usuário está fluindo bem (adicionando proposições consistentes), variation simples detectada, gap menor que não impacta claim
  - Observer sugere timing, Orquestrador decide

#### 14.6 Feedback Loop (Aprender com Respostas)

- **Descrição:** Observer analisa resposta do usuário a pergunta de esclarecimento e atualiza CognitiveModel.
- **Critérios de Aceite:**
  - Após usuário responder pergunta de esclarecimento, Observer analisa resposta
  - Atualiza proposições, contradictions, ou open_questions
  - Marca esclarecimento como "resolvido" ou "parcialmente resolvido"
  - Timeline mostra: "✅ Esclarecimento obtido: [resumo]"
  - Se resposta não esclarece: Observer identifica necessidade de nova pergunta
  - Ciclo continua até confusão resolver

#### 14.7 Testes de Integração

- **Descrição:** Validação de perguntas contextuais em cenários reais.
- **Critérios de Aceite:**
  - Testes multi-turn com contradições, gaps, mudanças
  - Validação: perguntas são contextuais (mencionam conceitos específicos)
  - Validação: perguntas ajudam a avançar (não apenas apontam problemas)
  - Validação: tom é de parceiro, não fiscalizador
  - Validação: timing apropriado (não interrompe fluxo)
  - Script: `scripts/validate_clarification_questions.py`

---

## ÉPICO 15: Observer - Painel Visual Dedicado

**Objetivo:** Interface visual mostrando estado do Observer de forma transparente e não-intrusiva.

**Status:** ✅ Refinado (pronto para implementação)

**Dependências:**
- Épico 13 (detecção de mudanças)
- Épico 14 (consultas inteligentes)

**Filosofia:**
- Transparência: usuário vê como sistema pensa
- Não-intrusivo: painel colapsado por padrão
- Útil: mostra informação acionável, não apenas diagnóstico
- Educativo: ajuda usuário entender conversa melhor

### Funcionalidades:

#### 15.1 Painel Principal (Colapsável)

- **Descrição:** Seção dedicada "Observer" nos Bastidores, entre "Contexto" e "Raciocínio".
- **Critérios de Aceite:**
  - Nova seção "🔍 Observer" em `app/components/backstage/`
  - Localização: entre `st.expander("Contexto")` e `st.expander("Bastidores")`
  - Padrão: colapsado (`st.expander(default_expanded=False)`)
  - Ao expandir: mostra estado atual do CognitiveModel
  - Design consistente com outras seções dos Bastidores
  - Componente: `app/components/backstage/observer_panel.py`

#### 15.2 Métricas Visuais (Qualitativas)

- **Descrição:** Visualização do estado da conversa sem números fixos.
- **Critérios de Aceite:**
  - Grid com indicadores: solidez da conversa (barra de progresso verde/amarelo/vermelho), completude do argumento (barra de progresso), tensões identificadas (contador + badge ⚠️ se > 0), gaps abertos (contador + badge)
  - Barras são visuais (não mostram percentual exato)
  - Cores indicam saúde geral (verde = bem, amarelo = atenção, vermelho = problemas)
  - Badge "🟢 Madura" ou "🟡 Em desenvolvimento" baseado em análise qualitativa

#### 15.3 Claim Atual e Proposições

- **Descrição:** Visualização clara do claim e principais proposições.
- **Critérios de Aceite:**
  - Claim atual em destaque (`st.info` ou `st.markdown` com fundo)
  - Lista de proposições principais (top 5 por solidez)
  - Cada proposição mostra: texto da proposição, indicador visual de solidez (emoji: 🟢 sólida, 🟡 moderada, 🔴 frágil)
  - NÃO mostra número exato
  - Proposições ordenadas por relevância (solidez)

#### 15.4 Tensões e Open Questions

- **Descrição:** Visualização de contradições (tensões) e gaps identificados.
- **Critérios de Aceite:**
  - Seção "⚠️ Tensões" (se existirem): lista contradições identificadas, não usa linguagem de "erro" (usa "tensão entre proposições"), mostra contexto (quais proposições estão em tensão)
  - Seção "❓ Gaps Abertos" (se existirem): lista open_questions, indica se são gaps críticos ou menores
  - Se não há tensões/gaps: mensagem positiva "✅ Nenhuma tensão identificada"

#### 15.5 Modal Detalhado (3 Abas)

- **Descrição:** Botão "Ver detalhes" abre modal com visão completa do Observer.
- **Critérios de Aceite:**
  - Botão no painel principal: "Ver detalhes completos"
  - Modal com 3 abas (padrão dos Bastidores): Aba 1 - Estado Atual (claim completo, todas proposições, todas tensões e gaps, análise de confusão), Aba 2 - Evolução (timeline visual de mudanças no claim, gráfico de solidez/completude ao longo do tempo (Plotly), eventos importantes), Aba 3 - JSON (CognitiveModel completo em JSON formatado, permite usuário copiar/exportar)
  - Modal usa `st.dialog` (API Streamlit 1.31+)

#### 15.6 Integração com EventBus

- **Descrição:** Painel Observer consome eventos e atualiza em tempo real.
- **Critérios de Aceite:**
  - Observer publica eventos: `COGNITIVE_MODEL_UPDATED`, `VARIATION_DETECTED`, `DIRECTION_CHANGE`, `CLARIFICATION_REQUESTED`
  - Painel consome eventos via EventBus (já existe)
  - Atualização automática sem refresh manual
  - Segue padrão de `app/components/backstage/reasoning.py`

#### 15.7 Testes de Interface

- **Descrição:** Validação da UI do painel Observer.
- **Critérios de Aceite:**
  - Testes visuais: painel renderiza corretamente
  - Testes de interação: modal abre/fecha
  - Testes de eventos: painel atualiza com novos eventos
  - Testes de responsividade: funciona em diferentes tamanhos de tela
  - Script: `scripts/test_observer_panel_ui.py`

---

## ÉPICO 16: Catálogo de Conceitos - Interface Web

**Objetivo:** Usuário explora biblioteca de conceitos via web. Transparência sobre o que sistema aprendeu.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 15

**Consulte:**
- `docs/products/paper_agent.md` - Interface web conversacional
- `docs/interface/web/components.md` - Componentes Streamlit

### Funcionalidades Planejadas:

#### 16.1 Página Catálogo (`/catalogo`)

- Lista todos conceitos da biblioteca
- Busca por nome (fuzzy search)
- Filtros: por ideia, por frequência, por data
- Visualização: cards com conceito + variations + ideias relacionadas

#### 16.2 Preview na Página da Ideia

- Mostra discretamente: "Usa 3 conceitos: [X] [Y] [Z]"
- Tags clicáveis → redireciona para catálogo
- Não polui interface

#### 16.3 Analytics de Conceitos

- Conceitos mais mencionados (gráfico)
- Conceitos por ideia/artigo
- Evolução temporal
- Export em JSON
- Sistema detecta padrões: "5+ usuários adicionaram conceito X" → atualiza biblioteca base

#### 16.4 Testes E2E

- Fluxo completo: conversa → conceitos → catálogo
- Validar UX (não quebra experiência)
- Performance (biblioteca com 100+ conceitos)

---

## ÉPICO 17: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 16

**Adição:** Pesquisador pode usar catálogo de conceitos para buscar papers relacionados.

---

## ÉPICO 18: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 17

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
