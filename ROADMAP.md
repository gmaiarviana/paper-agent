# ROADMAP - Paper Agent

## 📋 Status dos Épicos

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 1: Setup e Infraestrutura Base ✅
- ÉPICO 2: Agente Metodologista com LangGraph (MVP) ✅
- ÉPICO 3: Orquestrador com Reasoning
- ÉPICO 4: Interface CLI e Streamlit

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 5: Multi-Agente e Persistência Avançada

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## 🎯 EM PROGRESSO

**ÉPICO 3: Orquestrador + Estruturador (Base Multi-Agente)**
- ✅ 3.1 Orquestrador com Detecção de Maturidade (concluída)
- ✅ 3.2 Estruturador - Organizador de Ideias (concluída)
- 🔄 3.3 Integração Multi-Agente (próxima)

---

## 📋 PRÓXIMAS FUNCIONALIDADES

### ÉPICO 3: Orquestrador + Estruturador (Base Multi-Agente)

**Objetivo:** Sistema com múltiplos agentes especializados (Metodologista + Estruturador) e orquestração inteligente que detecta maturidade da ideia e roteia para o agente correto.

**Documentação técnica:** `docs/orchestration/multi_agent_architecture.md`

### Funcionalidades:

#### ✅ 3.1 Orquestrador com Detecção de Maturidade (CONCLUÍDA)
- **Descrição:** Nó do grafo (LangGraph) que analisa input do usuário e classifica maturidade: "vague" (ideia não estruturada) → Estruturador, "semi_formed" ou "complete" (hipótese) → Metodologista
- **Status:** ✅ Implementada, testada e merged (PR #16)
- **Critérios de Aceite:** ✅ Todos atendidos
  - ✅ Classifica corretamente 3 tipos de input usando LLM
  - ✅ Roteia para agente apropriado baseado na classificação
  - ✅ Registra reasoning da decisão (por quê escolheu X)
  - ✅ Output estruturado em MultiAgentState
  - ✅ Router condicional funciona corretamente
- **Arquivos:**
  - `agents/orchestrator/state.py`: MultiAgentState
  - `agents/orchestrator/nodes.py`: orchestrator_node
  - `agents/orchestrator/router.py`: route_from_orchestrator
  - `tests/unit/test_orchestrator.py`: 8 testes unitários
  - `scripts/validate_orchestrator.py`: validação manual

#### ✅ 3.2 Estruturador - Organizador de Ideias (CONCLUÍDA)
- **Descrição:** Nó simples que recebe observações vagas e transforma em questões de pesquisa estruturadas, identificando contexto, problema e possível contribuição acadêmica
- **Status:** ✅ Implementada e testada (aguardando merge)
- **Critérios de Aceite:** ✅ Todos atendidos
  - ✅ Extrai: contexto, problema, contribuição potencial
  - ✅ Gera questão de pesquisa estruturada
  - ✅ Output JSON estruturado (`structurer_output` no state)
  - ✅ Não rejeita ideias (comportamento colaborativo)
  - ✅ Não valida rigor científico (isso é do Metodologista)
- **Arquivos:**
  - `agents/structurer/nodes.py`: structurer_node
  - `tests/unit/test_structurer.py`: 8 testes unitários
  - `scripts/validate_structurer.py`: validação manual

**Nota:** Estruturador é nó simples neste épico (POC). Evolução para grafo próprio com `ask_user` e loops vai para backlog "PRÓXIMOS".

#### 3.3 Integração Multi-Agente
- **Descrição:** Super-grafo (LangGraph) que conecta Orquestrador, Estruturador e Metodologista com passagem de contexto via MultiAgentState híbrido
- **Critérios de Aceite:**
  - Super-grafo compilado com MemorySaver checkpointer
  - Fluxo completo funciona: input vago → Orquestrador → Estruturador → Metodologista → resultado
  - Fluxo direto funciona: hipótese → Orquestrador → Metodologista → resultado
  - Contexto preservado entre chamadas (structurer_output passa para Metodologista)
  - Metodologista integrado corretamente (reusa grafo existente)
  - Logs mostram decisões e transições

### 📋 Validação

**Scripts de validação:**
- ✅ `validate_orchestrator.py`: Testa classificação de inputs (criado)
- ✅ `validate_structurer.py`: Testa organização de ideias vagas (criado)
- ⏳ `validate_multi_agent_flow.py`: Testa fluxo completo end-to-end (pendente - funcionalidade 3.3)

**Testes automatizados:**
- ✅ Testes unitários: orchestrator, structurer (16 testes, todos passando)
- ⏳ Teste de integração: fluxo completo com API real (pendente - funcionalidade 3.3)

**Comandos:**
```bash
# Testes unitários (funcionando)
python -m pytest tests/unit/test_orchestrator.py -v    # 8 testes
python -m pytest tests/unit/test_structurer.py -v      # 8 testes

# Validação manual (funcionando)
python scripts/validate_orchestrator.py
python scripts/validate_structurer.py

# Teste de integração (pendente - funcionalidade 3.3)
python scripts/validate_multi_agent_flow.py
python -m pytest tests/integration/test_multi_agent_smoke.py -v
```

---

## ÉPICO 4: Loop Colaborativo + Refinamento

**Objetivo:** Sistema que refina ideias iterativamente até ficarem testáveis, ao invés de rejeitar prematuramente. Metodologista colabora ativamente na melhoria da hipótese.

**Status:** ⚠️ Não refinado - aguardando validação do Épico 3

**Dependências:** 
- Épico 3 concluído (sistema multi-agente base funcionando)

**Funcionalidades planejadas (alto nível):**
- Metodologista em modo colaborativo (sugere melhorias específicas sem rejeitar)
- Loop Estruturador ↔ Metodologista (até 2 iterações de refinamento)
- Memória de contexto entre iterações (rastreamento de evolução)
- Versionamento de hipótese (V1 vaga → V2 refinada → V3 aprovada)

**Valor esperado:**
- Resolve problema atual: sistema não rejeita mais ideias vagas, colabora na construção
- Conversação fluida: usuário sente que está sendo ajudado, não julgado
- Transparência: usuário vê como ideia evolui

**Nota:** Este épico será refinado após conclusão e validação do Épico 3. Refinamento incluirá critérios de aceite detalhados, arquitetura técnica e estratégia de implementação.

---

## ÉPICO 5: Interface Conversacional

**Objetivo:** Experiência de usuário natural, transparente e demonstrável. Conversação fluida ao invés de formulário rígido.

**Status:** ⚠️ Não refinado - aguardando validação dos Épicos 3 e 4

**Dependências:**
- Épico 3 concluído (multi-agente base)
- Épico 4 concluído (loop colaborativo)

**Funcionalidades planejadas (alto nível):**
- CLI conversacional: Input natural ("Me conte sua ideia" vs "Digite hipótese")
- Logs estruturados: Rastreabilidade completa de decisões do sistema
- Transparência: Visualização de reasoning e fluxo entre agentes
- Streamlit opcional: Interface gráfica para demonstrações

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
