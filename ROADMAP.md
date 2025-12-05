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

## ÉPICO 8: Análise Assistida de Qualidade

**Status:** ✅ Concluído (8.1 e 8.2 implementados; 8.3-8.5 opcionais e não priorizados)

Ferramentas para execução multi-turn e relatórios estruturados implementadas. Funcionalidades 8.3-8.5 planejadas mas não implementadas (prioridade reduzida).

### Funcionalidades Planejadas (não implementadas)

#### 8.3 Comparison Tool ⏳

- **Status:** ⏳ Planejado (prioridade baixa)
- **Objetivo:** Comparar antes/depois de mudanças no prompt para detectar regressões
- **Descrição:** Implementar ferramenta que compara resultados de execução antes/depois de mudanças no código/prompt, identifica regressões automaticamente, e gera relatório de impacto estruturado para discussão
- **Critérios de Aceite:**
  - Deve implementar `compare_results()` em `utils/result_comparer.py`
  - Deve implementar `detect_regressions()` para identificar regressões automaticamente
  - Deve implementar `compare_results.py` com CLI
  - Output deve incluir resumo de mudanças e lista de cenários que precisam atenção

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
