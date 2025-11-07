# ROADMAP - Paper Agent

## 📋 Status dos Épicos

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 1: Setup e Infraestrutura Base
- ÉPICO 2: Agente Metodologista Standalone
- ÉPICO 3: Orquestrador com Reasoning
- ÉPICO 4: Interface CLI e Streamlit

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 5: Integração com LangGraph State

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## ÉPICO 1: Setup e Infraestrutura Base

**Objetivo:** Ambiente Python funcional com LangGraph + Claude API, validando comunicação básica.

### ✅ 1.1 Configuração de Ambiente

**Status:** Concluído (commit: 684b87d)

**Descrição:** Setup inicial do projeto com dependências e estrutura de pastas

**Critérios de Aceite:**
- ✅ Repositório criado com `.gitignore`, `requirements.txt`, `README.md`
- ✅ Dependências instaladas: `langgraph`, `langchain-anthropic`, `streamlit`, `python-dotenv`
- ✅ Estrutura de pastas: `/agents`, `/orchestrator`, `/utils`, `/app`
- ✅ Arquivo `.env.example` com variável `ANTHROPIC_API_KEY`

---

### 1.2 Teste de Conexão com Claude API

**Descrição:** Script simples validando chamada à API Anthropic

**Critérios de Aceite:**
- Script `test_api.py` faz chamada de teste ao Claude
- Retorna resposta simples (ex: "Hello from Claude")
- Exibe tokens consumidos
- README documentado com comando para rodar teste

---

## ÉPICO 2: Agente Metodologista Standalone

**Objetivo:** Implementar Metodologista isoladamente para validar prompt engineering e reasoning antes de integrar orquestração.

### 2.1 Prompt do Metodologista

**Descrição:** System prompt que define comportamento, responsabilidades e formato de resposta

**Critérios de Aceite:**
- Prompt descreve papel do Metodologista (conforme `docs/agents/overview.md`)
- Define formato de output:
  ```json
  {
    "status": "approved|rejected",
    "justification": "...",
    "suggestions": [...]
  }
  ```
- Inclui exemplos de aprovação e rejeição
- Instrução clara: sempre retornar JSON válido

---

### 2.2 Implementação do Agente Metodologista

**Descrição:** Classe Python representando o agente com método `.analyze(hypothesis)`

**Critérios de Aceite:**
- Classe `Methodologist` em `/agents/methodologist.py`
- Método `analyze(hypothesis: str) -> dict` retorna JSON estruturado
- Lida com erros da API (timeout, rate limit, invalid JSON)
- Logs de debug mostram prompt enviado e resposta recebida

---

### 2.3 Teste Isolado do Metodologista

**Descrição:** Script de teste com casos de aprovação e rejeição

**Critérios de Aceite:**
- Script `test_methodologist.py` com 3+ casos de teste
- **Caso 1:** hipótese válida → deve aprovar
- **Caso 2:** hipótese falha metodológica → deve rejeitar com justificativa
- **Caso 3:** observação casual → deve rejeitar educadamente
- Output mostra reasoning completo do agente

---

## ÉPICO 3: Orquestrador com Reasoning

**Objetivo:** Implementar orquestrador que decide autonomamente quando chamar Metodologista.

### 3.1 Prompt do Orquestrador

**Descrição:** System prompt definindo papel de decisor e regras de roteamento

**Critérios de Aceite:**
- Prompt descreve papel do Orquestrador (conforme `docs/agents/overview.md`)
- Regras claras: quando chamar Metodologista vs responder direto
- Formato de output:
  ```json
  {
    "action": "call_agent|respond_direct",
    "agent": "methodologist|null",
    "message": "..."
  }
  ```
- Exemplos de decisão incluídos

---

### 3.2 Implementação do Orquestrador

**Descrição:** Classe Python que recebe input do usuário e decide próximo passo

**Critérios de Aceite:**
- Classe `Orchestrator` em `/orchestrator/orchestrator.py`
- Método `decide(user_input: str) -> dict` retorna decisão estruturada
- Se `action == "call_agent"`, chama agente correspondente
- Se `action == "respond_direct"`, retorna mensagem direto ao usuário
- Mantém histórico da conversa em memória

---

### 3.3 Integração Orquestrador → Metodologista

**Descrição:** Fluxo completo onde Orquestrador chama Metodologista quando apropriado

**Critérios de Aceite:**
- Script `test_orchestration.py` testa integração
- **Cenário 1:** "Olá" → Orquestrador responde direto (não chama Metodologista)
- **Cenário 2:** "Café aumenta produtividade" → Orquestrador chama Metodologista
- **Cenário 3:** Metodologista retorna resultado → Orquestrador formata resposta ao usuário
- Logs mostram decisão do Orquestrador antes de chamar agente

---

## ÉPICO 4: Interface CLI e Streamlit (Opcional)

**Objetivo:** CLI interativa como interface principal, permitindo Claude Code testar autonomamente via terminal. Streamlit opcional para visualização posterior.

### 4.1 CLI Interativa Básica

**Descrição:** Interface de conversa via terminal com input/output de texto

**Critérios de Aceite:**
- Script `cli.py` inicia conversa interativa no terminal
- Usuário digita mensagem → sistema responde via text output
- Loop de conversa contínuo (até comando `exit` ou `quit`)
- Claude Code consegue executar e testar sozinho sem browser
- README atualizado com comando `python cli.py`
- Erros exibidos claramente no terminal

---

### 4.2 Painel de Logs no Terminal

**Descrição:** Logs formatados em tempo real no terminal mostrando reasoning e decisões

**Critérios de Aceite:**
- Logs com cores/símbolos para destacar componentes:
  - `🎯 Orquestrador decidiu: call_methodologist`
  - `🧪 Metodologista analisando...`
  - `✅ Resultado: approved`
- Usa `colorama` ou similar para formatação
- Mostra decisões do orquestrador antes de chamar agentes
- Logs de debug podem ser ativados/desativados via flag `--verbose`
- Output estruturado em seções legíveis

---

### 4.3 Interface Streamlit

**Descrição:** Interface web para testes por humanos - será importante para validação e demonstração

**Status:** Importante (implementar após CLI básico funcionar)

**⚠️ NOTA:** Streamlit pode não funcionar no ambiente Claude Code (porta web). Priorizar CLI para desenvolvimento iterativo com Claude Code. Streamlit será testado pelo usuário localmente.

**Critérios de Aceite:**
- Página Streamlit com input de texto e histórico de mensagens
- Sidebar exibe logs em tempo real
- Mostra reasoning do Orquestrador e Metodologista
- Indicadores visuais: spinner, badges de agente ativo
- Mensagens do sistema visualmente distintas das do usuário
- Comando `streamlit run app.py` inicia interface
- Documentação em README com instruções para rodar localmente

---

## ÉPICO 5: Integração com LangGraph State

**Status:** ⚠️ NÃO-REFINADO (Requer aprofundamento em LangGraph antes da implementação)

**Objetivo:** Substituir implementação manual por LangGraph gerenciando estado e transições.

**Próximos Passos Antes da Implementação:**
- Estudar exemplos concretos de LangGraph State
- Definir estratégia de fallback em discussão
- Adicionar exemplos de código em `langgraph_examples.md`
- Refinar funcionalidades com base no aprendizado

### 5.1 Definição do State Schema

**Descrição:** Schema do LangGraph State representando conversa e decisões

**Critérios de Aceite:**
- Schema define: `messages`, `current_agent`, `history`, `last_decision`
- TypedDict ou Pydantic model documentado
- Estado inicializado corretamente ao começar sessão

---

### 5.2 Grafo de Orquestração

**Descrição:** LangGraph workflow conectando Orquestrador e Metodologista

**Critérios de Aceite:**
- Grafo define nós: `orchestrator`, `methodologist`, `user_response`
- Arestas condicionais baseadas em decisão do Orquestrador
- Estado atualizado automaticamente a cada transição
- Possível visualizar grafo (LangGraph debug)

---

### 5.3 Execução e Validação do Fluxo Completo

**Descrição:** Sistema rodando end-to-end via LangGraph

**Critérios de Aceite:**
- Interface Streamlit integrada com LangGraph
- Usuário envia mensagem → LangGraph executa workflow
- Logs mostram transições de estado
- Conversa completa: usuário → orquestrador → metodologista → resposta
- Performance aceitável (< 5s por interação)

---

## 💡 IDEIAS FUTURAS

- Adicionar **Pesquisador** (chamadas externas, web search)
- Adicionar **Estruturador** (planejamento de artigo)
- **Persistência:** salvar checkpoints em JSON
- **Vector DB:** histórico de conversas e artigos
- Outros agentes: **Escritor**, **Crítico**
- Interface melhorada: **React + FastAPI**
- **Métricas:** tempo de resposta, tokens consumidos, custo
- **Retry logic** e fallbacks para API failures
- Suporte a **múltiplas conversas simultâneas**
- **Export** de conversa (Markdown, PDF)
- **Hot reload na CLI:** recarregar agentes sem reiniciar sessão
- **Export de logs:** salvar logs em JSON ou TXT para análise posterior
- **CLI com argumentos:** modo não-interativo para testes automatizados (`python cli.py --input "..."` → output direto)

---

## 📝 Observações

### Cada épico:
- Pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo

### Ordem proposta:
1. **Setup** → valida ambiente
2. **Metodologista isolado** → valida um agente
3. **Orquestrador** → valida reasoning/decisão
4. **Interface** → valida transparência
5. **LangGraph** → valida arquitetura final