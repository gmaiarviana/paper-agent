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

### ✅ Recém Concluídos
- **ÉPICO 14**: Observer - Consultas Inteligentes - Sistema faz perguntas contextuais para esclarecer contradições e gaps. Integrado ao Orquestrador via `_consult_observer()`. Timeline visual com seção de esclarecimentos. 40+ testes.

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

#### 13.6 Testes de Integração

- **Descrição:** Validação em cenários reais de conversa.
- **Critérios de Aceite:**
  - Testes multi-turn com variations e mudanças
  - Validação: Orquestrador intervém naturalmente (não roboticamente)
  - Validação: variations não interrompem
  - Validação: confusão gera perguntas contextuais
  - Script: `scripts/validate_direction_change.py`

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
