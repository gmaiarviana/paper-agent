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

### ÉPICO 2: Agente Metodologista com LangGraph (MVP)

**Status Atual:** Funcionalidades core implementadas (2.1-2.5). Faltam system prompt, CLI e testes.

### 🔜 Próximas Funcionalidades

#### 2.7 CLI Minimalista
Interface de linha de comando básica para testar o agente.

**Critérios de Aceite:**
- Arquivo `cli/chat.py` com loop: entrada → execução → handling de `interrupt()` → decisão
- CLI gera thread ID único por sessão
- Comando `exit` encerra sem exceções
- README inclui `python cli/chat.py`

---

#### 2.8 Teste de Fumaça
Teste básico validando fluxo completo do agente.

**Critérios de Aceite:**
- Arquivo `tests/integration/test_methodologist_smoke.py`
- Usa API real (marcar com `@pytest.mark.integration`)
- Simula: hipótese vaga → pergunta → resposta → decisão final
- Valida `status != "pending"` e `justification` preenchida
- Comando: `pytest tests/integration/test_methodologist_smoke.py -v`

---

## 📋 PRÓXIMAS FUNCIONALIDADES

### ÉPICO 3: Orquestrador com Reasoning

**Objetivo:** Orquestrador que decide autonomamente quando chamar Metodologista.

#### 3.1 Prompt do Orquestrador
- System prompt com papel de decisor
- Regras: quando chamar Metodologista vs responder direto
- Output JSON: `{"action": "call_agent|respond_direct", "agent": "methodologist|null", "message": "..."}`

#### 3.2 Implementação do Orquestrador
- Classe `Orchestrator` em `/orchestrator/orchestrator.py`
- Método `decide(user_input: str) -> dict`
- Mantém histórico da conversa

#### 3.3 Integração Orquestrador → Metodologista
- Script `test_orchestration.py` testa integração completa
- Cenários: saudação, hipótese, formatação de resposta

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

## ✅ CONCLUÍDO (Resumido)

### ÉPICO 1: Setup e Infraestrutura Base ✅
- 1.1 Configuração de Ambiente (commit: 684b87d)
- 1.2 Teste de Conexão com Claude API (commit: 909f30f)

### ÉPICO 2: Agente Metodologista MVP ✅
- 2.1 Setup LangGraph State ✅
- 2.2 Knowledge Base Micro ✅
- 2.3 Tool `ask_user` ✅
- 2.4 Nós do Grafo ✅
- 2.5 Construção do Grafo ✅
- 2.6 System Prompt ✅

**Arquitetura Atual:**
```
agents/
└── methodologist/
    ├── __init__.py      # API pública
    ├── state.py         # MethodologistState
    ├── tools.py         # ask_user
    ├── nodes.py         # analyze, ask_clarification, decide
    ├── router.py        # route_after_analyze
    └── graph.py         # create_methodologist_graph

utils/
├── json_parser.py       # extract_json_from_llm_response
└── prompts.py           # METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1

scripts/
└── validate_system_prompt.py  # Validação do system prompt
```

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
