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

### ÉPICO 4: Interface CLI e Streamlit

**Objetivo:** CLI interativa como interface principal.

#### 4.1 CLI Interativa Básica
- Script `cli.py` com conversa via terminal
- Loop até comando `exit`
- Claude Code consegue testar sem browser

#### 4.2 Painel de Logs no Terminal
- Logs com cores/símbolos: `🎯 Orquestrador`, `🧪 Metodologista`, `✅ Resultado`
- Flag `--verbose` para debug

#### 4.3 Interface Streamlit
- Página com input, histórico e sidebar com logs
- **Nota:** Testar localmente (porta web pode não funcionar no Claude Code)

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
