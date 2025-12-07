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

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Planejados (refinados)
- **ÉPICO 11**: Alinhamento de Ontologia

#### Planejados (não refinados)
- **ÉPICO 12**: Observador Integrado ao Fluxo (não refinado) - Próximo candidato
- **ÉPICO 13**: Catálogo de Conceitos - Interface Web (não refinado)
- **ÉPICO 14**: Pesquisador (não refinado)
- **ÉPICO 15**: Escritor (não refinado)


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

## ÉPICO 11: Alinhamento de Ontologia

**Objetivo:** Migrar código de premises/assumptions (strings separadas) para Proposições unificadas com solidez. Simplificar o sistema para refletir a realidade epistemológica.

**Status:** ✅ Refinado (aguardando conclusão do Épico 10)

**Dependências:**
- Épico 10 concluído

**Consulte:**
- `docs/architecture/ontology.md` - Nova ontologia (Proposição)
- `docs/vision/epistemology.md` - Base filosófica
- `docs/vision/cognitive_model/core.md` - Evolução de solidez

### Funcionalidades:

#### 11.1 Schema Unificado (Camada Modelo)

- **Descrição:** Criar estrutura `Proposicao` e migrar schema SQLite.
- **Critérios de Aceite:**
  - Deve criar modelo Pydantic `Proposicao` com: `id`, `texto`, `solidez` (Optional[float]), `evidencias` (lista vazia)
  - Deve atualizar schema SQLite: substituir colunas `premises`, `assumptions` por `proposicoes` (JSON)
  - Deve criar script de migração que converte dados existentes (premises → proposicoes com solidez=None, assumptions → proposicoes com solidez=None)
  - Deve manter `solid_grounds` temporariamente (migra para `evidencias` no Épico 14)
  - Claim continua como campo separado (não vira proposição)

#### 11.2 Adapter de Compatibilidade

- **Descrição:** Criar adapter que traduz estrutura nova ↔ antiga durante transição.
- **Critérios de Aceite:**
  - Deve criar `ProposicaoAdapter` em `agents/models/adapters.py`
  - Deve implementar `to_legacy()`: proposicoes → premises/assumptions (para código não migrado)
  - Deve implementar `from_legacy()`: premises/assumptions → proposicoes
  - Deve ser removido ao final do Épico 11 (código temporário)

#### 11.3 Migrar CognitiveModel

- **Descrição:** Atualizar `CognitiveModel` para usar `proposicoes`.
- **Critérios de Aceite:**
  - Deve substituir campos `premises` e `assumptions` por `proposicoes: List[Proposicao]`
  - Deve atualizar `is_mature()` para usar solidez média das proposições avaliadas (ignorar None)
  - Deve atualizar `calculate_solidez()` para derivar de solidez das proposições
  - Deve manter compatibilidade via Adapter durante transição
  - Proposições com `solidez=None` não contam para cálculos

#### 11.4 Migrar Observador

- **Descrição:** Atualizar Observador para extrair/armazenar proposições.
- **Critérios de Aceite:**
  - Deve atualizar `extract_fundamentos()` para retornar `List[Proposicao]` (com solidez=None inicial)
  - Deve atualizar `_merge_cognitive_model()` para mesclar proposições (por similaridade de texto)
  - Deve atualizar `metrics.py` para calcular solidez a partir de proposições avaliadas
  - Deve remover referências a `premises`/`assumptions`
  - Avaliação de solidez via LLM continua funcionando (atualiza solidez de None → valor)

#### 11.5 Migrar Orquestrador e Estruturador

- **Descrição:** Atualizar nós que leem/escrevem cognitive_model.
- **Critérios de Aceite:**
  - Deve atualizar `orchestrator/nodes.py` para usar `proposicoes`
  - Deve atualizar `structurer/nodes.py` para usar `proposicoes`
  - Deve atualizar prompts em `utils/prompts/` para nova estrutura JSON
  - Deve atualizar fallbacks e validações

#### 11.6 Migrar Interface

- **Descrição:** Atualizar componentes Streamlit para exibir proposições.
- **Critérios de Aceite:**
  - Deve atualizar `_ideia_detalhes.py` para renderizar proposições com solidez
  - Deve atualizar `sidebar/ideas.py` para exibir proposições
  - Deve atualizar `backstage.py` para inferir status a partir de solidez média
  - Deve mostrar indicador visual de solidez (cor: verde >0.7, amarelo 0.4-0.7, vermelho <0.4, cinza None)
  - Não deve exibir "Premises" e "Assumptions" separados

#### 11.7 Migrar Testes

- **Descrição:** Atualizar testes para nova estrutura.
- **Critérios de Aceite:**
  - Deve atualizar `test_cognitive_model.py` para testar `Proposicao`
  - Deve atualizar `test_orchestrator_logic.py` para usar `proposicoes`
  - Deve atualizar `test_database_manager.py` para testar migração e nova estrutura
  - Todos os 237 testes devem passar após migração

#### 11.8 Limpeza Final

- **Descrição:** Remover código legado e Adapter.
- **Critérios de Aceite:**
  - Deve remover `ProposicaoAdapter` após todas as camadas migradas
  - Deve remover referências a `premises`/`assumptions` do código
  - Deve atualizar documentação técnica (`ARCHITECTURE.md`, docstrings)
  - Deve garantir que nenhum arquivo Python referencia estrutura antiga
  - Documentação de visão já está alinhada (não precisa mudar)

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
