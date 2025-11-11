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

Nenhum épico em progresso no momento.

---

## 📋 PRÓXIMAS FUNCIONALIDADES

### ÉPICO 3: Orquestrador + Estruturador (Base Multi-Agente)

**Objetivo:** Sistema com múltiplos agentes especializados (Metodologista + Estruturador) e orquestração inteligente que detecta maturidade da ideia e roteia para o agente correto.

**Documentação técnica:** `docs/orchestration/multi_agent_architecture.md`

### Funcionalidades:

#### 3.1 Orquestrador com Detecção de Maturidade
- **Descrição:** Nó do grafo (LangGraph) que analisa input do usuário e classifica maturidade: "vague" (ideia não estruturada) → Estruturador, "semi_formed" ou "complete" (hipótese) → Metodologista
- **Critérios de Aceite:**
  - Deve classificar corretamente 3 tipos de input usando LLM
  - Deve rotear para agente apropriado baseado na classificação
  - Deve registrar reasoning da decisão (por quê escolheu X)
  - Output estruturado em MultiAgentState
  - Router condicional funciona corretamente

#### 3.2 Estruturador - Organizador de Ideias (POC)
- **Descrição:** Nó simples que recebe observações vagas e transforma em questões de pesquisa estruturadas, identificando contexto, problema e possível contribuição acadêmica
- **Critérios de Aceite:**
  - Deve extrair: contexto, problema, contribuição potencial
  - Deve gerar questão de pesquisa estruturada
  - Output JSON estruturado (`structurer_output` no state)
  - Não rejeita ideias (comportamento colaborativo)
  - Não valida rigor científico (isso é do Metodologista)

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

**Scripts de validação (criar em `scripts/`):**
- `validate_orchestrator.py`: Testa classificação de inputs
- `validate_structurer.py`: Testa organização de ideias vagas
- `validate_multi_agent_flow.py`: Testa fluxo completo end-to-end

**Testes automatizados:**
- Testes unitários para cada nó (orchestrator, structurer, integration)
- Teste de integração: fluxo completo com API real

**Comandos:**
```bash
# Testes unitários
python -m pytest tests/unit/test_orchestrator.py -v
python -m pytest tests/unit/test_structurer.py -v

# Validação manual
python scripts/validate_multi_agent_flow.py

# Teste de integração
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

## 💡 IDEIAS FUTURAS

### Melhorias do Metodologista (após MVP)
- **Documentação técnica completa** em `docs/agents/methodologist.md`
- **Tool `consult_methodology`** para busca em knowledge base
- **Knowledge base completa** (10+ páginas)
- **Testes completos** (unit + integration)
- **Métricas**: tempo, tokens, custos

### Infraestrutura e Qualidade
- **Pre-commit hooks** (`.pre-commit-config.yaml`)
- **Badge de coverage** no README
- **CI/CD** (GitHub Actions)
- **Retry logic** para API failures
- **Hot reload na CLI**
- **Export de logs** (JSON/TXT)

### Novos Agentes
- **Pesquisador** (web search)
- **Estruturador** (planejamento de artigo)
- **Escritor**, **Crítico**

### Persistência
- **Checkpoints em JSON**
- **Vector DB** para histórico

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
