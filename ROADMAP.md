# ROADMAP - Paper Agent

## 📋 Status dos Épicos

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 1: Setup e Infraestrutura Base
- ÉPICO 2: Agente Metodologista com LangGraph (MVP)
- ÉPICO 3: Orquestrador com Reasoning
- ÉPICO 4: Interface CLI e Streamlit

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 5: Multi-Agente e Persistência Avançada

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

### ✅ 1.2 Teste de Conexão com Claude API

**Status:** Concluído (commit: 909f30f)

**Descrição:** Script simples validando chamada à API Anthropic

**Critérios de Aceite:**
- ✅ Script `test_api.py` faz chamada de teste ao Claude
- ✅ Retorna resposta simples (ex: "Hello from Claude")
- ✅ Exibe tokens consumidos
- ✅ README documentado com comando para rodar teste

---

## ÉPICO 2: Agente Metodologista com LangGraph (MVP)

**Objetivo:** Implementar Metodologista como agente autônomo mínimo usando LangGraph, capaz de fazer perguntas ao usuário e tomar decisões com raciocínio explícito.

**Escopo do MVP:** Agente standalone (sem Orquestrador), 1 tool (`ask_user`), knowledge base micro, fluxo básico analyze → ask_clarification → decide.

---

### ✅ 2.1 Setup LangGraph State

**Descrição:** Definir schema do estado do agente usando `TypedDict` e configurar checkpointer para persistência de sessão.

**Critérios de Aceite:**
- Arquivo `agents/methodologist.py` criado com `TypedDict MethodologistState` e todos os campos obrigatórios
- MemorySaver configurado como checkpointer padrão
- Função `create_initial_state()` para criar estado com valores padrão
- Testes unitários validando todos os campos e tipos
- Script de validação manual

---

### ✅ 2.2 Knowledge Base Micro

**Descrição:** Criar versão minimalista da base de conhecimento com conceitos essenciais de método científico.

**Critérios de Aceite:**
- Diferença entre lei, teoria e hipótese (2-3 parágrafos cada)
- Critérios de testabilidade e falseabilidade (critério de Popper)
- 2 exemplos práticos contrastando hipóteses boas vs ruins
- Formatação markdown limpa em português brasileiro

---

### ✅ 2.3 Tool `ask_user`

**Descrição:** Implementar tool que permite agente fazer perguntas ao usuário usando `interrupt()` do LangGraph.

**Critérios de Aceite:**
- Função `ask_user(question: str) -> str` decorada com `@tool` e type hints corretos
- Docstring completa com Args, Returns, Example e Observações
- Chamada a `interrupt()` do `langgraph.types` para pausar a execução do grafo
- Logging estruturado informando pergunta enviada e resposta recebida
- Testes unitários completos
- Script de validação manual

**Observação:** O controle de `iterations` e bloqueio de perguntas é implementado no nó `ask_clarification` (Task 2.4).

---

### ✅ 2.4 Nós do Grafo

**Descrição:** Implementar 3 nós que compõem o raciocínio do agente.

**Critérios de Aceite:**
- **Nó `analyze`:** usa LLM para avaliar hipótese, define se há necessidade de clarificação e atualiza `messages` e `needs_clarification` no estado
- **Nó `ask_clarification`:** chama `ask_user`, registra pergunta/resposta em `clarifications` e incrementa `iterations`
- **Nó `decide`:** define `status` (`approved` ou `rejected`) e gera `justification` explicita
- Cada nó retorna dicionário com updates incrementais do estado
- Logs nível INFO registram entrada, saída e decisão em cada nó

---

### 2.5 Construção do Grafo

**Descrição:** Montar `StateGraph` conectando os 3 nós com lógica de roteamento condicional.

**Critérios de Aceite:**
- **Modelo LLM:** `claude-3-5-haiku-20241022` (custo-efetivo para MVP)
- **Tool binding:** LLM configurado com `.bind_tools([ask_user])` para tool calling nativo
- **Mecanismo de decisão:** Router verifica `response.tool_calls`:
  - Se `tool_calls` não vazio → próximo nó é `ToolNode` (executa ask_user)
  - Se `tool_calls` vazio e `iterations < max_iterations` → nó `decide`
  - Se `iterations >= max_iterations` → força nó `decide`
- `StateGraph(MethodologistState)` instanciado.
- Nós `analyze`, `ask_clarification` e `decide` adicionados e registrados.
- Edges implementados:
  - START → `analyze`
  - `analyze` → `ask_clarification` (quando precisa de mais contexto)
  - `analyze` → `decide` (quando já pode deliberar)
  - `ask_clarification` → `analyze`
  - `decide` → END
- Router function decide próximo nó com base em estado (`iterations`, necessidade de contexto, status).
- Se `iterations >= max_iterations`, fluxo força `decide`.
- Grafo compilado com `MemorySaver` e invocável via `graph.invoke({"hypothesis": "..."})`.

---

### 2.6 System Prompt

**Descrição:** Criar prompt do agente com instruções de comportamento e uso de tools.

- **Critérios de Aceite:**
- Constante `METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1` criada em `utils/prompts.py`.
- **Tool calling explícito:** Prompt instrui LLM a usar tool `ask_user` quando precisar de clarificação ("Se falta contexto essencial, USE a tool ask_user com pergunta específica").
- **Output sem tool call:** Prompt instrui que quando tiver contexto suficiente, responder diretamente SEM chamar tools, apenas com raciocínio final.
- Prompt descreve papel do Metodologista, processo analyze → ask → decide e limite de 3 perguntas.
- Explica quando usar a tool `ask_user` e como registrar hipóteses insuficientes.
- Define output final em JSON com campos obrigatórios: `{"status": "approved|rejected", "justification": "string detalhada"}`.
- Instruções explícitas sobre quando aprovar vs rejeitar hipóteses.
- Linguagem direta, <= 500 palavras.
- Histórico do arquivo registra versão V1 (comentário ou docstring curta).

---

### 2.7 CLI Minimalista

**Descrição:** Interface de linha de comando básica para testar o agente.

**Critérios de Aceite:**
- Arquivo `cli/chat.py` implementa loop: entrada de hipótese → execução do agente → handling de `interrupt()` → exibição da decisão.
- CLI gera thread ID único por sessão (UUID ou timestamp).
- Comando `exit` encerra a aplicação sem exceções.
- Saída em texto puro, sem dependências adicionais.
- Erros e perguntas exibidos claramente.
- README inclui comando de execução `python cli/chat.py`.

---

### 2.8 Teste de Fumaça

**Descrição:** Um teste básico que valida o fluxo completo do agente.

**Critérios de Aceite:**
- Arquivo `tests/integration/test_methodologist_smoke.py` criado.
- Uso da API real do Anthropic (marcar com `@pytest.mark.integration`).
- Teste simula: hipótese vaga → agente pergunta uma vez → resposta mockada → decisão final.
- Valida que estado final tem `status != "pending"` e `justification` preenchida.
- Comando de execução documentado: `pytest tests/integration/test_methodologist_smoke.py -v`.

---

### Ideias Futuras (Fora do MVP)

- Tool `consult_methodology` para busca na knowledge base ampliada.
- Knowledge base completa com referências detalhadas.
- Integração com Orquestrador (ÉPICO 3).
- Interface Streamlit e logs enriquecidos.
- Suite completa de testes unitários e integrações.

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

### Melhorias do Metodologista (após MVP)
- **Documentação técnica completa**: criar `docs/agents/methodologist.md` com arquitetura do grafo, fluxo de decisão, exemplos de uso e diagramas
- **Tool `consult_methodology`**: buscar em knowledge base completa
- **Knowledge base completa**: 10+ páginas com exemplos detalhados
- **Nó `consult_knowledge`**: usar LLM para interpretar knowledge base
- **Testes completos**: unit (mocks) + integration (múltiplos cenários)
- **Logs estruturados**: JSON com timestamps e níveis
- **Métricas**: tempo de resposta, tokens consumidos por análise

### Infraestrutura e Qualidade
- **Pre-commit hooks**: rodar testes automaticamente antes de cada commit usando `.pre-commit-config.yaml`
- **Badge de coverage**: adicionar badge no README mostrando % de cobertura de testes
- **CI/CD**: GitHub Actions para rodar testes em cada PR
- **Retry logic** e fallbacks para API failures
- **Hot reload na CLI:** recarregar agentes sem reiniciar sessão
- **Export de logs:** salvar logs em JSON ou TXT para análise posterior
- **CLI com argumentos:** modo não-interativo para testes automatizados (`python cli.py --input "..."` → output direto)

### Novos Agentes e Funcionalidades
- Adicionar **Pesquisador** (chamadas externas, web search)
- Adicionar **Estruturador** (planejamento de artigo)
- Outros agentes: **Escritor**, **Crítico**
- Interface melhorada: **React + FastAPI**
- Suporte a **múltiplas conversas simultâneas**
- **Export** de conversa (Markdown, PDF)

### Persistência e Memória
- **Persistência:** salvar checkpoints em JSON
- **Vector DB:** histórico de conversas e artigos para busca semântica

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