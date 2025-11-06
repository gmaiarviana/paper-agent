# ARCHITECTURE.md

## Stack Técnico

**Backend:**
- Python 3.11+
- LangGraph (orquestração de agentes)
- LangChain Anthropic (integração Claude API)
- Pydantic (validação de schemas)

**Interface:**
- CLI (interface principal para desenvolvimento e testes)
- Streamlit (opcional - visualização posterior)

**LLM:**
- Claude Sonnet 4 (Anthropic API)

**Sem (por enquanto):**
- Banco de dados
- Vector database
- Persistência em disco
- APIs REST
- Docker

---

## Estrutura de Pastas

```
paper-agent/
├── .env                    # API keys (não commitado)
├── .env.example           # Template de variáveis
├── requirements.txt       # Dependências Python
├── README.md             # Como rodar
├── ROADMAP.md           # Funcionalidades
├── ARCHITECTURE.md      # Este arquivo
├── .cursorrules          # Regras do Cursor
│
├── cli/
│   ├── __init__.py
│   ├── chat.py          # Conversa via terminal
│   └── interactive.py   # REPL interativo
│
├── app.py               # Entrypoint Streamlit (opcional)
│
├── agents/
│   ├── __init__.py
│   ├── base.py          # Classe base para agentes
│   └── methodologist.py # Agente Metodologista
│
├── orchestrator/
│   ├── __init__.py
│   ├── orchestrator.py  # Lógica de decisão
│   └── state.py         # Schema do LangGraph State
│
├── utils/
│   ├── __init__.py
│   ├── prompts.py       # System prompts centralizados
│   └── logger.py        # Logging estruturado
│
└── tests/
    ├── test_api.py
    ├── test_methodologist.py
    └── test_orchestration.py
```

---

## Componentes Principais

### 1. CLI (`/cli`)

**Responsabilidade:** Interface de desenvolvimento e testes autônoma.

**Arquivos:**
- `chat.py`: Conversa interativa via terminal
- `interactive.py`: REPL para testes rápidos

**Características:**
- Input/output via stdin/stdout
- Logs formatados com cores/símbolos
- Histórico de conversa visível
- Claude Code consegue executar e validar

**Prioridade:** ALTA (interface principal da POC)

---

### 2. Agentes (`/agents`)

**Responsabilidade:** Especialistas que executam tarefas específicas.

**Estrutura comum:**
```python
class BaseAgent:
    def __init__(self, api_key: str, model: str)
    def execute(self, input: dict) -> dict
    def _build_prompt(self, input: dict) -> str
    def _parse_response(self, response: str) -> dict
```

**Agentes na POC:**
- `Methodologist`: Valida rigor científico de hipóteses

**Comunicação:**
- Input: JSON estruturado
- Output: JSON estruturado (`{"status": "...", "data": {...}}`)

**Princípios:**
- Cada agente é independente
- Não conhece outros agentes
- Comunica apenas via Orquestrador

---

### 3. Orquestrador (`/orchestrator`)

**Responsabilidade:** Decidir fluxo de execução e chamar agentes.

**Decisões que toma:**
- User input é casual? → Responde direto
- User input é hipótese? → Chama Metodologista
- Resultado válido? → Formata e retorna ao usuário

**Não faz:**
- Não avalia conteúdo científico (delega ao agente)
- Não escreve texto (delega ao agente)
- Não persiste dados (apenas mantém estado em memória)

**Reasoning:**
- Usa Claude API para decidir próximo passo
- Baseado em system prompt com regras claras
- Output estruturado: `{"action": "...", "agent": "...", "message": "..."}`

---

### 4. State (`/orchestrator/state.py`)

**Gerenciado por:** LangGraph

**Schema:**
```python
class ConversationState(TypedDict):
    messages: list[dict]           # Histórico completo
    current_agent: str | None      # Agente ativo no momento
    last_decision: dict | None     # Última decisão do Orquestrador
    metadata: dict                 # Tokens, timing, etc.
```

**Características:**
- Imutável (LangGraph gerencia updates)
- Apenas em memória durante sessão
- Sem persistência em disco na POC

**Acessível por:**
- Todos os agentes (leitura)
- Orquestrador (escrita via LangGraph)

---

### 5. Interface Streamlit (`app.py`)

**Status:** OPCIONAL (não prioritário na POC)

**Framework:** Streamlit

**Estrutura:**
- **Main panel:** Chat (usuário ↔ sistema)
- **Sidebar:** Logs e decisões em tempo real
- **State:** Session state do Streamlit mantém histórico

**Uso:**
- Usuário roda localmente quando quiser visualização gráfica
- Não é necessário para desenvolvimento/testes
- Claude Code não depende disso

---

## Fluxo de Dados (POC)

### Fluxo Principal:

```
Usuário (CLI)
    ↓
    [Input: texto]
    ↓
Orquestrador (reasoning)
    ↓
    [Decisão: chamar agente ou responder direto?]
    ↓
    ├─→ Resposta direta → Usuário (CLI)
    │
    └─→ Chama Metodologista
            ↓
            [Análise de hipótese]
            ↓
        Retorna JSON estruturado
            ↓
        Orquestrador formata resposta
            ↓
        Usuário (CLI)
```

### Exemplo de execução:

```bash
$ python cli/chat.py

🤖 Paper Agent POC
Digite sua mensagem (ou 'sair' para encerrar):

> Olá, como você está?

[Orquestrador] Analisando input...
[Orquestrador] Decisão: responder direto (casual)

Olá! Estou funcionando bem. Como posso ajudar com seu artigo científico?

> Café aumenta produtividade cognitiva

[Orquestrador] Analisando input...
[Orquestrador] Decisão: chamar Metodologista (hipótese detectada)
[Metodologista] Analisando hipótese...
[Metodologista] Status: REJEITADO

Sua hipótese "Café aumenta produtividade cognitiva" foi rejeitada pelo Metodologista.

**Motivos:**
- Hipótese muito genérica (falta especificar dose, população, tipo de tarefa)
- Não considera variáveis confundidoras (tolerância, horário, etc)

**Sugestões:**
- Reformule especificando: "Consumo de 200mg de cafeína aumenta velocidade de processamento em tarefas de atenção sustentada em adultos não-habituados"
```

---

## Padrões de Código

### Prompts

**Localização:** `utils/prompts.py`

**Formato:**
```python
METHODOLOGIST_PROMPT_V1 = """
Você é um Metodologista científico rigoroso.

RESPONSABILIDADES:
- Avaliar rigor científico de hipóteses
- Identificar falhas metodológicas
- Sugerir melhorias concretas

FORMATO DE OUTPUT (JSON):
{
  "status": "approved" | "rejected",
  "justification": "...",
  "suggestions": [...]
}

EXEMPLOS:
...
"""
```

**Princípios:**
- Versionados (V1, V2, etc)
- Documentados (quando usar cada versão)
- Exemplos incluídos no prompt

---

### Logs

**Estrutura:**
```python
{
  "timestamp": "2025-11-06T10:30:00",
  "level": "INFO",
  "component": "orchestrator",
  "action": "decision",
  "data": {
    "input": "...",
    "decision": "call_agent",
    "agent": "methodologist"
  }
}
```

**Níveis:**
- `DEBUG`: Reasoning interno, prompts completos
- `INFO`: Decisões, chamadas de agentes
- `WARNING`: Retries, fallbacks
- `ERROR`: Falhas de API, erros críticos

**Output:**
- Console (formatado para leitura humana)
- Arquivo (JSON estruturado para análise posterior - futuro)

---

### Error Handling

**Estratégia:**
```python
try:
    response = agent.execute(input)
except APIError as e:
    # Retry com backoff exponencial (3 tentativas)
    retry_with_backoff(agent.execute, input)
except ValidationError as e:
    # Log erro + retorna mensagem clara ao usuário
    log_error(e)
    return {"status": "error", "message": "Resposta inválida do agente"}
```

**Regras:**
- Sempre capturar exceções de API
- Retry automático (3 tentativas, backoff exponencial)
- Fallback: mensagem clara ao usuário
- Nunca deixar sistema travar silenciosamente

---

### Validação

**Input do usuário:**
- Sanitizar antes de enviar para LLM
- Limite de caracteres (ex: 5000)
- Remover caracteres especiais problemáticos

**Output de agentes:**
- Validar JSON estruturado (Pydantic)
- Verificar campos obrigatórios presentes
- Retry se formato inválido

**Economia de tokens:**
- Validar localmente antes de chamar API quando possível
- Cache de respostas comuns (futuro)

---

## Decisões Técnicas (POC)

### Por que LangGraph?

✅ **Vantagens:**
- Gerencia estado automaticamente
- Workflow explícito (fácil debugar)
- Facilita adicionar novos agentes
- Visualização de grafo (debugging)

⚠️ **Trade-offs:**
- Curva de aprendizado inicial
- Overhead para POC simples

**Decisão:** Vale a pena - facilita escalar depois

---

### Por que CLI prioritária?

✅ **Vantagens:**
- Claude Code consegue rodar e testar
- Desenvolvimento autônomo (sem depender de browser)
- Logs claros no terminal
- Iteração rápida

⚠️ **Trade-offs:**
- Menos visual que interface web

**Decisão:** POC prioriza validação técnica, não UX visual

---

### Por que Claude Sonnet 4?

✅ **Vantagens:**
- System prompts robustos (agentes seguem instruções melhor)
- Reasoning superior para orquestração
- Output estruturado confiável (JSON válido)

⚠️ **Trade-offs:**
- Mais caro que modelos menores

**Decisão:** Custo justificado - POC precisa validar reasoning complexo

---

### Por que sem persistência?

✅ **Vantagens:**
- Menos código na POC
- Foco em validar fluxo, não durabilidade
- Mais rápido para iterar

⚠️ **Trade-offs:**
- Estado some ao reiniciar

**Decisão:** Adicionar persistência é incremental depois (épico futuro)

---

### Por que sem Docker?

✅ **Vantagens:**
- Python + venv é suficiente para POC
- Claude Code provavelmente já roda em container
- Menos fricção para desenvolvimento
- Hot reload nativo do Python

⚠️ **Trade-offs:**
- Sem isolamento total de dependências

**Decisão:** Adicionar Docker depois quando for deploy (épico futuro)

---

## Limitações Conhecidas (POC)

### Funcionalidades ausentes (por design):

- ❌ Sem histórico entre sessões
- ❌ Apenas 1 usuário por vez
- ❌ Sem retry inteligente (só 3 tentativas brutas)
- ❌ Sem métricas de custo/tokens em tempo real
- ❌ Sem testes automatizados (só scripts manuais)
- ❌ Sem validação de input avançada (XSS, injection, etc)
- ❌ Sem rate limiting

### Resolução planejada:

**Épicos futuros no ROADMAP.md** tratam dessas limitações gradualmente.

---

## Escalabilidade Futura

### Fácil adicionar:

- ✅ Novos agentes (herdam `BaseAgent`)
- ✅ Novas decisões no Orquestrador (apenas lógica)
- ✅ Persistência (adicionar save/load no State)
- ✅ Métricas (interceptar chamadas de API)
- ✅ Testes automatizados (estrutura já modular)

### Difícil adicionar (requer refactor):

- ⚠️ Múltiplos usuários simultâneos (precisa de sessões isoladas)
- ⚠️ Interface complexa (migrar de CLI/Streamlit para React)
- ⚠️ Processamento distribuído (agentes em máquinas diferentes)
- ⚠️ Webhooks/eventos assíncronos

---

## Comandos Principais

### Setup inicial:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis
cp .env.example .env
# Editar .env com ANTHROPIC_API_KEY=sua-chave
```

### Testes:

```bash
# Testar conexão API
python tests/test_api.py

# Testar Metodologista isolado
python tests/test_methodologist.py

# Testar orquestração completa
python tests/test_orchestration.py
```

### Rodar aplicação:

```bash
# CLI (interface principal)
python cli/chat.py

# Streamlit (opcional - visualização gráfica)
streamlit run app.py
```

---

## Ambiente de Desenvolvimento

### Claude Code Web:

**Características assumidas:**
- Python disponível
- Acesso ao PyPI (`pip install`)
- Consegue executar scripts e ver output
- Terminal interativo funcional

**Workflow esperado:**
1. Claude Code cria/edita arquivos
2. Claude Code roda testes via CLI
3. Claude Code valida output no terminal
4. Itera até funcionar

**Sem necessidade de:**
- Docker
- Expor portas web
- Browser para validação

---

## Dependências Principais

### requirements.txt (inicial):

```
langgraph>=0.0.40
langchain-anthropic>=0.1.0
anthropic>=0.18.0
pydantic>=2.0.0
python-dotenv>=1.0.0
streamlit>=1.30.0  # opcional
rich>=13.0.0       # formatação CLI
```

### Instalação gradual:

- **Épico 1:** langgraph, langchain-anthropic, python-dotenv
- **Épico 2:** anthropic, pydantic
- **Épico 3:** (sem novas)
- **Épico 4:** rich (para CLI formatada)
- **Épico 5:** (sem novas)

---

## Princípios de Design

### 1. Separação de responsabilidades
- Cada agente tem função clara e limitada
- Orquestrador não avalia conteúdo
- State é apenas container de dados

### 2. Fail-safe
- Erros não travam sistema
- Mensagens claras ao usuário
- Logs detalhados para debug

### 3. Transparência
- Todo output é auditável
- Decisões do Orquestrador visíveis
- Reasoning dos agentes rastreável

### 4. Iteração controlada
- Limites claros para evitar loops infinitos
- Escalação para usuário quando necessário

### 5. Escalabilidade
- Estrutura permite adicionar agentes sem quebrar
- State pode evoluir incrementalmente
- Interface pode ser trocada sem afetar lógica

---

## Próximos Passos (Pós-POC)

Quando POC estiver funcionando, avaliar:

1. **Performance:** Tempo de resposta aceitável? Precisa otimizar?
2. **Custo:** Tokens gastos por interação? Precisa cache?
3. **UX:** CLI é suficiente ou precisa interface gráfica?
4. **Arquitetura:** LangGraph atende necessidades? Ou precisa ajustar?

**Decisões arquiteturais futuras baseadas em dados reais da POC.**

---

**Versão:** 1.0  
**Data:** 06/11/2025  
**Status:** Documentação inicial - POC em planejamento