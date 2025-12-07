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
- **ÉPICO 8**: Análise Assistida de Qualidade - Ferramentas para execução multi-turn e relatórios estruturados (8.1 e 8.2 implementados)
- **ÉPICO 9**: Integração Backend↔Frontend - Persistência silenciosa e feedback visual de progresso completos
- **ÉPICO 10**: Observador - Mente Analítica (POC) - ChromaDB + SQLite para catálogo de conceitos, pipeline de persistência, busca semântica e 22 testes unitários

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Planejados (não refinados)
- **ÉPICO 11**: Alinhamento de Ontologia (não refinado)
- **ÉPICO 12**: Observador Integrado ao Fluxo (não refinado) - Próximo candidato
- **ÉPICO 13**: Catálogo de Conceitos - Interface Web (não refinado)
- **ÉPICO 14**: Pesquisador (não refinado)
- **ÉPICO 15**: Escritor (não refinado)


**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 8: Análise Assistida de Qualidade

**Status:** ✅ Concluído (8.1 e 8.2 implementados; 8.3 movido para backlog)

Ferramentas para execução multi-turn e relatórios estruturados implementadas. Funcionalidade 8.3 (Comparison Tool) movida para backlog. Funcionalidades 8.4-8.5 planejadas mas não implementadas (prioridade reduzida).

### Funcionalidades Planejadas (não implementadas)

#### 8.4 Interactive Analysis Mode ⏳

- **Status:** ⏳ Planejado (prioridade baixa)
- **Objetivo:** Guiar fluxo de investigação de forma interativa
- **Descrição:** Implementar modo interativo que apresenta menu de opções, executa ações conforme escolha do usuário, e gera outputs estruturados para discussão
- **Critérios de Aceite:**
  - Deve implementar `interactive_analyzer.py` em `scripts/testing/`
  - Menu inicial deve listar cenários disponíveis
  - Após executar cenário, deve oferecer opções de análise
  - Deve ser intuitivo (não requer documentação para usar)

#### 8.5 Debug Workflow ⏳

- **Status:** ⏳ Parcialmente implementado
- **Objetivo:** Facilitar troubleshooting de problemas sutis com logs detalhados
- **Descrição:** Implementar workflow de debug que gera logs completos (prompt enviado, resposta bruta, reasoning do LLM, decisões step-by-step) quando problema é identificado
- **Critérios de Aceite:**
  - ✅ `scripts/testing/debug_scenario.py` criado (debug mode com logs detalhados)
  - ⏳ `generate_debug_report()` em `utils/debug_reporter.py` (parcial)
  - ⏳ Logs formatados com marcadores visuais completos
  - ⏳ Comparação antes/depois de mudanças no prompt (futuro)

---

## ✅ ÉPICO 10: Observador - Mente Analítica (POC)

Observador implementado com ChromaDB + SQLite para catálogo de conceitos. Inclui pipeline de persistência com deduplicação automática (threshold 0.80), busca semântica via embeddings (all-MiniLM-L6-v2), e 22 testes unitários. Preparado para Agentic RAG (Epic 12) com parâmetros opcionais em `process_turn()`.

**Consulte:** `docs/agents/observer.md` - Documentação completa do Observador

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

## ÉPICO 12: Observador Integrado ao Fluxo

**Objetivo:** Orquestrador consulta Observador para decisões contextuais. Conversas mais inteligentes.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épicos 10-11

**Consulte:**
- `docs/agents/observer.md` - Comunicação Observador ↔ Orquestrador
- `docs/architecture/observer_architecture.md` - Integração com grafo

### Funcionalidades Planejadas:

#### 12.1 Integrar Observador ao Grafo (Paralelo)

- Observador roda em paralelo a cada turno
- Investigar: LangGraph suporta paralelismo? Se não, usar callback
- Não bloqueia fluxo principal

#### 12.2 Interface de Consulta Não-Determinística

- Orquestrador consulta quando incerto
- Gatilhos naturais: mudança direção, contradição, completude
- Observador responde com insights, não comandos

#### 12.3 Detecção de Variations Automática

- Threshold > 0.90: adiciona variation automaticamente
- Threshold 0.80-0.90: pergunta ao usuário
- Threshold < 0.80: conceito novo

#### 12.4 Visualização nos Bastidores

- Timeline (colapsável): ações de todos agentes
- Painel Observador (colapsável): CognitiveModel em tempo real
- Ambos colapsados por padrão
- Mostra Observador na timeline apenas quando relevante

#### 12.5 Testes de Integração

- Cenários multi-turn com Observador ativo
- Validar que não interfere no fluxo
- LLM-as-Judge para qualidade de insights

---

## ÉPICO 13: Catálogo de Conceitos - Interface Web

**Objetivo:** Usuário explora biblioteca de conceitos via web. Transparência sobre o que sistema aprendeu.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12

**Consulte:**
- `docs/products/paper_agent.md` - Interface web conversacional
- `docs/interface/web/components.md` - Componentes Streamlit

### Funcionalidades Planejadas:

#### 13.1 Página Catálogo (`/catalogo`)

- Lista todos conceitos da biblioteca
- Busca por nome (fuzzy search)
- Filtros: por ideia, por frequência, por data
- Visualização: cards com conceito + variations + ideias relacionadas

#### 13.2 Preview na Página da Ideia

- Mostra discretamente: "Usa 3 conceitos: [X] [Y] [Z]"
- Tags clicáveis → redireciona para catálogo
- Não polui interface

#### 13.3 Analytics de Conceitos

- Conceitos mais mencionados (gráfico)
- Conceitos por ideia/artigo
- Evolução temporal
- Export em JSON
- Sistema detecta padrões: "5+ usuários adicionaram conceito X" → atualiza biblioteca base

#### 13.4 Testes E2E

- Fluxo completo: conversa → conceitos → catálogo
- Validar UX (não quebra experiência)
- Performance (biblioteca com 100+ conceitos)

---

## ÉPICO 14: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 13

**Adição:** Pesquisador pode usar catálogo de conceitos para buscar papers relacionados.

---

## ÉPICO 15: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 14

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
