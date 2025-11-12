# ROADMAP - Paper Agent

## 📋 Status dos Épicos

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 1: Setup e Infraestrutura Base ✅ **CONCLUÍDO**
- ÉPICO 2: Agente Metodologista com LangGraph (MVP) ✅ **CONCLUÍDO**
- ÉPICO 3: Orquestrador com Reasoning ✅ **CONCLUÍDO**
- ÉPICO 4: Loop Colaborativo + Refinamento Iterativo ✅ **CONCLUÍDO**

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 5: Multi-Agente e Persistência Avançada

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## ✅ ÉPICOS CONCLUÍDOS

**ÉPICO 4: Loop Colaborativo + Refinamento Iterativo** (12/11/2025)
- ✅ 4.1 Metodologista em Modo Colaborativo
- ✅ 4.2 Loop de Refinamento (Super-Grafo)
- ✅ 4.3 Estruturador Processa Feedback
- ✅ 4.4 Versionamento e Rastreamento
- ✅ 4.5 Limite de Iterações e Decisão Forçada

**ÉPICO 3: Orquestrador + Estruturador (Base Multi-Agente)**
- ✅ 3.1 Orquestrador com Detecção de Maturidade
- ✅ 3.2 Estruturador - Organizador de Ideias
- ✅ 3.3 Integração Multi-Agente

Ver detalhes das funcionalidades na seção "PRÓXIMAS FUNCIONALIDADES" abaixo.

---

## 📋 PRÓXIMAS FUNCIONALIDADES

## ÉPICO 4: Loop Colaborativo + Refinamento Iterativo

**Objetivo:** Sistema parceiro que ajuda o usuário a CONSTRUIR e REFINAR ideias até ficarem testáveis, ao invés de apenas validar ou rejeitar.

**Status:** ✅ **CONCLUÍDO** (12/11/2025)

**Dependências:** 
- Épico 3 concluído (sistema multi-agente base funcionando)

### Funcionalidades:

#### 4.1 Metodologista em Modo Colaborativo
**Descrição:** Metodologista nunca rejeita sem dar caminhos de melhoria. Opera em 3 modos: approved, needs_refinement (novo), rejected (apenas casos extremos).

**Critérios de Aceite:**
- [x] Output estruturado com 3 status possíveis:
  - "approved": Hipótese testável, específica, operacionalizada
  - "needs_refinement": Tem potencial mas faltam elementos (população, métricas, variáveis)
  - "rejected": Apenas para casos sem potencial científico (crenças populares, impossível testar)
- [x] Campo `improvements` quando status="needs_refinement":
```python
"improvements": [
  {
    "aspect": "população" | "métricas" | "variáveis" | "testabilidade",
    "gap": "Descrição do que falta",
    "suggestion": "Sugestão específica de como preencher"
  }
]
```
- [x] Prompt atualizado: instruções de modo colaborativo
- [x] Justificativa sempre construtiva (cita pontos fortes + gaps)
- [x] Status "rejected" usado apenas quando ideia não tem base científica

**Arquivos:**
- `agents/methodologist/nodes.py`: atualizar nó `decide` com nova lógica
- `utils/prompts.py`: novo prompt colaborativo (V2)
- `agents/orchestrator/state.py`: output do Metodologista permite "needs_refinement"

#### 4.2 Loop de Refinamento (Super-Grafo)
**Descrição:** Super-grafo permite loop: Estruturador → Metodologista → (se needs_refinement) → Estruturador novamente, até 2 iterações.

**Critérios de Aceite:**
- [x] MultiAgentState rastreia iterações:
```python
refinement_iteration: int  # 0, 1, 2
max_refinements: int  # default: 2
```
- [x] Router após Metodologista:
  - Se status="approved" → END
  - Se status="needs_refinement" AND iteration < max → volta Estruturador
  - Se status="needs_refinement" AND iteration >= max → força decisão (approved/rejected)
  - Se status="rejected" → END
- [x] Estruturador recebe feedback do Metodologista no input
- [x] Loop termina quando: aprovado, rejeitado, ou atingiu limite
- [x] Logs registram: versão atual (V1, V2, V3), gaps identificados, refinamentos aplicados

**Arquivos:**
- `agents/multi_agent_graph.py`: adicionar router após Metodologista
- `agents/orchestrator/state.py`: adicionar campos de rastreamento
- `agents/structurer/nodes.py`: processar feedback do Metodologista

#### 4.3 Estruturador Processa Feedback
**Descrição:** Estruturador recebe feedback do Metodologista (gaps identificados) e gera versão refinada da questão de pesquisa.

**Critérios de Aceite:**
- [x] Input do Estruturador inclui:
  - `user_input`: input original do usuário
  - `previous_question`: questão estruturada V1
  - `methodologist_feedback`: output do Metodologista (improvements)
- [x] Prompt atualizado: instruções para processar feedback
- [x] Output V2 endereça gaps específicos do Metodologista:
  - Se gap="população" → adiciona população específica
  - Se gap="métricas" → adiciona métricas mensuráveis
  - Se gap="variáveis" → define variáveis dep/indep
- [x] Mantém essência da ideia original (não muda direção)
- [x] Registra no output: `version: 2`, `addressed_gaps: ["população", "métricas"]`

**Arquivos:**
- `agents/structurer/nodes.py`: lógica de refinamento
- `utils/prompts.py`: prompt do Estruturador V2 (com handling de feedback)

#### 4.4 Versionamento e Rastreamento
**Descrição:** Sistema rastreia evolução da hipótese (V1 → V2 → V3) e decisões de cada iteração.

**Critérios de Aceite:**
- [x] Cada versão registrada no state:
```python
hypothesis_versions: [
  {"version": 1, "question": "...", "feedback": "..."},
  {"version": 2, "question": "...", "feedback": "..."}
]
```
- [x] Logs estruturados mostram:
  - Versão atual (V1, V2, V3)
  - Gaps identificados pelo Metodologista
  - Refinamentos aplicados pelo Estruturador
  - Reasoning de decisões
- [x] Output final inclui histórico de evolução
- [x] Usuário pode ver: o que mudou e por quê

**Arquivos:**
- `agents/orchestrator/state.py`: campo `hypothesis_versions`
- `agents/multi_agent_graph.py`: logging estruturado

#### 4.5 Limite de Iterações e Decisão Forçada
**Descrição:** Após 2 refinamentos sem aprovação, sistema força decisão final (approved/rejected) com base no contexto disponível.

**Critérios de Aceite:**
- [x] Limite padrão: `max_refinements = 2`
- [x] Na 3ª tentativa: Metodologista DEVE decidir (approved ou rejected)
- [x] Prompt da 3ª tentativa: "Esta é a última iteração, decida com o contexto disponível"
- [x] Justificativa clara se rejeitar após limite (o que falta para aprovar)
- [x] Logs indicam: "Limite de refinamentos atingido, forçando decisão final"

**Arquivos:**
- `agents/methodologist/nodes.py`: lógica de decisão forçada
- `agents/multi_agent_graph.py`: router verifica limite

### Validação

**Comandos:**
```bash
Teste manual com casos reais
python scripts/validate_refinement_loop.py
Testes unitários
pytest tests/unit/test_refinement_loop.py -v
Teste de integração (API real)
pytest tests/integration/test_refinement_smoke.py -v
```

**Cenários de teste:**
1. **Ideia vaga + 1 refinamento → aprovada**
   - Input: "Método X é mais rápido"
   - V1: needs_refinement (falta população, métricas)
   - V2: approved (população e métricas adicionadas)

2. **Ideia vaga + 2 refinamentos → aprovada**
   - Input: "Observei Y"
   - V1: needs_refinement (falta contexto, problema)
   - V2: needs_refinement (falta métricas)
   - V3: approved (todas métricas adicionadas)

3. **Ideia sem potencial → rejeitada imediatamente**
   - Input: "Café é bom porque todo mundo sabe"
   - V1: rejected (apelo à crença popular, não-testável)

4. **Limite atingido → decisão forçada**
   - Input: "Z melhora W"
   - V1: needs_refinement
   - V2: needs_refinement
   - V3: rejected (ainda não testável após 2 refinamentos)

### Valor Esperado

- ✅ Usuário não fica travado com ideias vagas
- ✅ Sistema ajuda a CONSTRUIR, não apenas criticar
- ✅ Conversação fluida: ideia → refinamento → hipótese testável
- ✅ Transparência: usuário vê evolução da ideia
- ✅ Eficiência: loop automático sem interrupções desnecessárias

---

## ÉPICO 5: Interface Conversacional

**Objetivo:** Experiência de usuário natural, transparente e demonstrável. Conversação fluida ao invés de formulário rígido.

**Status:** ⚠️ Não refinado - aguardando validação dos Épicos 3 e 4

**Dependências:**
- Épico 3 concluído (multi-agente base)
- Épico 4 concluído (loop colaborativo)

**Funcionalidades planejadas (alto nível):**
- CLI conversacional com feed de eventos em tempo real
- Logs estruturados com rastreabilidade e export em JSON
- Transparência: reasoning visível e histórico navegável

**Melhorias previstas:**
- Streamlit dashboard para demonstrações
- Replay de execuções via CLI (`python cli/chat.py --replay <session-id>`)
- Visualização de grafo com destaque do nó ativo

**Valor esperado:**
- Usuário tem experiência conversacional, não formulário
- Total transparência de decisões do sistema
- Possível demonstrar sistema para outras pessoas
- Rastrear como ideias evoluem (histórico completo)

**Nota:** Este épico será refinado após conclusão dos Épicos 3 e 4. Interface depende do backend multi-agente estar sólido.

---

## 📋 BACKLOG

### 🔜 PRÓXIMOS PASSOS

Funcionalidades que agregarão valor, mas dependem do sistema multi-agente core (Épicos 3-5) estar validado e sólido.

**Estruturador Avançado (Evolução do 3.2):**
- Transformar Estruturador em grafo próprio (similar ao Metodologista)
- Adicionar tool `ask_user` para clarificações durante estruturação
- Loop interno de refinamento da questão de pesquisa
- State próprio: `StructurerState`

**Depuração Interativa:**
- Pausar execução e inspecionar `MultiAgentState`
- Métricas de performance por agente (tempo, tokens, custo, iterações)

**Pesquisador:**
- Busca bibliográfica automática (Google Scholar, Semantic Scholar)
- Síntese de papers acadêmicos relevantes
- Identificação de gaps na literatura
- Comparação de abordagens metodológicas

**Escritor:**
- Compilação de seções do artigo baseado em outline
- Formatação acadêmica (ABNT, APA, Chicago, etc)
- Geração de rascunhos com estilo consistente
- Integração com pesquisas e validações anteriores

**Crítico:**
- Revisão final de rigor científico e coerência
- Identificação de contradições ou gaps argumentativos
- Validação de integridade do argumento completo
- Sugestões de melhorias de redação e clareza

---

### 🔧 MELHORIAS ESTRUTURAIS (Quando Necessário)

Refatorações de qualidade de código e infraestrutura. Não bloqueiam funcionalidades, mas facilitam colaboração e manutenção. Considerar quando houver contribuidores externos, projeto crescer significativamente, ou precisar publicar como pacote.

**Estrutura de Projeto (src layout):**
- Migrar para `src/paper_agent/` com `pyproject.toml`
- Remover hacks de `sys.path` via `pip install -e .`
- Facilita distribuição e testes isolados

**Consolidação de Configuração:**
- Migrar `pytest.ini` para `pyproject.toml`
- Centralizar configs de ferramentas (black, ruff, mypy)

**Dependency Management:**
- Avaliar migração para `pyproject.toml` + pip-tools/poetry
- Lock de versões para builds reproduzíveis

---

### 🌙 FUTURO DISTANTE

Funcionalidades avançadas que não são prioridade no momento, mas podem ser valiosas no longo prazo.

**Infraestrutura Avançada:**
- RAG e Vector Database para memória de longo prazo entre artigos
- Persistência avançada em banco de dados relacional
- Sistema de versionamento de artigos (branches, merge, rollback)
- Cache inteligente de pesquisas e validações

**Integração e Colaboração:**
- Integração com gestores de referências (Zotero, Mendeley)
- Sistema multi-usuário com autenticação
- Compartilhamento e colaboração em tempo real
- Comentários e feedback inline

**Analytics e Melhorias:**
- Dashboard de métricas de uso (tokens, custos, tempo)
- Análise de qualidade de artigos gerados
- Sugestões automáticas de melhoria baseadas em patterns
- A/B testing de prompts de agentes

**Exportação e Formatação:**
- Múltiplos formatos de saída (PDF, LaTeX, Word, Markdown)
- Templates de revistas científicas específicas
- Submissão automática para repositórios de preprints (arXiv, bioRxiv)
- Geração de apresentações (slides) a partir do artigo

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
