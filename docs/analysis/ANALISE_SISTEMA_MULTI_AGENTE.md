# Análise Completa do Sistema Multi-Agente - Paper Agent

## 1. TRANSIÇÕES ENTRE AGENTES

### Como o Orquestrador decide chamar Estruturador/Metodologista?

**Decisão baseada em `next_step` e `agent_suggestion`:**

```19:117:agents/orchestrator/router.py
def route_from_orchestrator(state: MultiAgentState) -> Union[Literal["structurer", "methodologist", "user"], str]:
    """
    Router que decide o próximo passo após o Orquestrador Conversacional.

    Lógica de decisão:
    - next_step = "explore" → Retorna para usuário (mais perguntas necessárias)
    - next_step = "clarify" → Retorna para usuário (esclarecer ambiguidade)
    - next_step = "suggest_agent" + agent_suggestion:
      - "structurer" → Estruturador
      - "methodologist" → Metodologista
      - "researcher" → Pesquisador (futuro)
      - "writer" → Escritor (futuro)
```

**O Orquestrador analisa contexto e decide:**

```128:357:agents/orchestrator/nodes.py
def orchestrator_node(state: MultiAgentState, config: Optional[RunnableConfig] = None) -> dict:
    """
    Nó socrático que facilita diálogo provocativo com exposição de assumptions implícitas.

    Este nó é o facilitador inteligente do sistema multi-agente (Épico 7 MVP). Ele:
    1. Analisa input + histórico completo da conversa
    2. Extrai e atualiza ARGUMENTO FOCAL explícito a cada turno (7.8)
    3. Explora contexto através de perguntas abertas
    4. Provoca REFLEXÃO sobre lacunas quando relevante (7.9)
    5. Detecta EMERGÊNCIA de novo estágio naturalmente (7.10)
    6. Sugere próximos passos com justificativas claras
    7. Negocia com o usuário antes de chamar agentes
    8. Detecta mudanças de direção comparando focal_argument (7.8)
    9. Registra execução no MemoryManager (se configurado - Épico 6.2)
```

**Lógica de decisão no router:**

```83:117:agents/orchestrator/router.py
    # Decisão de roteamento
    if next_step in ["explore", "clarify"]:
        # Orquestrador quer mais conversa com usuário
        next_destination = "user"
        logger.info("Orquestrador precisa de mais contexto. Retornando para usuário.")

    elif next_step == "suggest_agent":
        # Orquestrador sugere agente específico
        if not agent_suggestion or not isinstance(agent_suggestion, dict):
            logger.warning(
                "next_step='suggest_agent' mas agent_suggestion inválida. "
                "Retornando para usuário por segurança."
            )
            next_destination = "user"
        else:
            suggested_agent = agent_suggestion.get("agent")
            justification = agent_suggestion.get("justification", "N/A")

            # Validar agente sugerido
            valid_agents = ["structurer", "methodologist", "researcher", "writer"]
            if suggested_agent not in valid_agents:
                logger.warning(
                    f"Agente sugerido '{suggested_agent}' não reconhecido. "
                    f"Valores válidos: {valid_agents}. Retornando para usuário."
                )
                next_destination = "user"
            else:
                next_destination = suggested_agent
                logger.info(f"Agente sugerido: {suggested_agent}")
                logger.info(f"Justificativa: {justification}")

    logger.info(f"Decisão do router: {next_destination}")
    logger.info("=== ROUTER CONVERSACIONAL: Finalizado ===\n")

    return next_destination
```

### Routers explícitos? Onde estão?

**Routers implementados:**

1. **Router do Orquestrador** (`agents/orchestrator/router.py`):
   - `route_from_orchestrator()`: Decide próximo passo após Orquestrador

2. **Router do Metodologista** (`agents/methodologist/router.py`):
   - `route_after_analyze()`: Decide se precisa clarificação ou pode decidir

```19:54:agents/methodologist/router.py
def route_after_analyze(state: MethodologistState) -> Literal["ask_clarification", "decide"]:
    """
    Router que decide o próximo nó após o nó analyze.

    Lógica de decisão:
    - Se needs_clarification é True E iterations < max_iterations → ask_clarification
    - Caso contrário → decide (tempo de decidir com o contexto disponível)
```

3. **Router após Metodologista** (no multi-agent graph):
   - `route_after_methodologist()`: Sempre retorna para Orquestrador

```322:344:agents/multi_agent_graph.py
def route_after_methodologist(state: MultiAgentState) -> str:
    """
    Router que decide o fluxo após o Metodologista processar a hipótese.

    Comportamento (Refinamento Sob Demanda):
    - Sempre retorna para o Orquestrador após o Metodologista
    - Orquestrador apresenta feedback e opções ao usuário
    - Usuário decide se quer refinar, pesquisar, ou mudar de direção
```

### Transições são automáticas ou pedem permissão?

**TRANSITOR AUTOMÁTICO** (sem pedir permissão):

```452:463:agents/multi_agent_graph.py
    # ROUTER 1: Orquestrador → Estruturador | Metodologista | User (Épico 7)
    # Épico 7 POC: Orquestrador conversacional pode retornar "user" quando precisa explorar mais
    graph.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "structurer": "structurer",
            "methodologist": "methodologist",
            "user": END  # Épico 7: Retornar para usuário (mais perguntas necessárias)
        }
    )
```

O sistema chama agentes automaticamente quando o contexto está suficiente. O Orquestrador apenas anuncia a ação:

```288:294:utils/prompts/orchestrator.py
  "message": "Perfeito! Você tem todos os elementos: hipótese clara, população definida, métrica específica e baseline. Vou organizar isso em uma questão de pesquisa estruturada.",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Ideia madura com intent, subject, population, metrics e baseline. Pronto para estruturação formal."
  },
```

### Contexto é preservado entre transições? Como?

**SIM**, contexto é preservado via `MultiAgentState`:

```20:245:agents/orchestrator/state.py
class MultiAgentState(TypedDict):
    """
    Estado compartilhado entre todos os agentes do sistema multi-agente.

    Este estado é organizado em 3 seções principais:
    1. COMPARTILHADO: Campos que todos os agentes leem e escrevem
    2. ESPECÍFICO POR AGENTE: Campos que apenas um agente específico escreve
    3. MENSAGENS (LangGraph): Histórico de mensagens do LLM
```

**Campos compartilhados preservam contexto:**

- `user_input`: Input original
- `conversation_history`: Histórico legível
- `messages`: Histórico LangGraph (preservado entre turnos)
- `focal_argument`: Argumento focal atualizado a cada turno
- `hypothesis_versions`: Histórico de versões refinadas

**Persistência via SqliteSaver:**

```304:319:agents/multi_agent_graph.py
# SqliteSaver: Checkpointer persistente do LangGraph usando SQLite.
# Salva estado do grafo em banco de dados, permitindo:
# - Persistência entre reinicializações do servidor
# - Navegação entre sessões passadas
# - Recuperação de histórico completo de conversas
# MVP Épico 9.10-9.11

# Garantir que diretório data/ existe
db_path = Path("data/checkpoints.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

# Criar conexão SQLite (check_same_thread=False permite uso em threads múltiplas)
db_conn = sqlite3.connect(str(db_path), check_same_thread=False)

# Instanciar SqliteSaver com conexão
checkpointer = SqliteSaver(db_conn)
```

---

## 2. TOOLS E AÇÕES

### Quais tools estão implementadas?

**Tool principal: `ask_user` do Metodologista:**

```18:59:agents/methodologist/tools.py
@tool
def ask_user(question: str) -> str:
    """
    Faz uma pergunta ao usuário para obter clarificações sobre a hipótese.

    Esta tool permite que o agente Metodologista interrompa a execução do grafo
    e solicite informações adicionais ao usuário quando o contexto fornecido
    não é suficiente para avaliar adequadamente a hipótese.

    A execução é pausada usando `interrupt()` do LangGraph, que suspende o grafo
    até que o usuário forneça uma resposta. Quando o grafo é retomado com a resposta,
    esta tool retorna o valor fornecido.
```

**Uso no grafo interno do Metodologista:**

```192:212:agents/methodologist/nodes.py
    # Chamar ask_user para obter resposta
    # ask_user é um StructuredTool, então usamos .invoke() com dict de args
    answer = ask_user.invoke({"question": question})

    logger.info(f"Resposta do usuário: {answer}")

    # Atualizar clarifications
    new_clarifications = state['clarifications'].copy()
    new_clarifications[question] = answer

    # Incrementar iterations
    new_iterations = state['iterations'] + 1

    logger.info(f"Clarificação registrada. Total de iterações: {new_iterations}")
    logger.info("=== NÓ ASK_CLARIFICATION: Finalizado ===\n")

    return {
        "clarifications": new_clarifications,
        "iterations": new_iterations,
        "messages": [response, HumanMessage(content=answer)]
    }
```

### Onde estão definidas?

- **Metodologista**: `agents/methodologist/tools.py`
- **Estruturador**: Não possui tools (operando em modo direto)
- **Orquestrador**: Não possui tools (operando em modo conversacional)

### Há integração com APIs externas? (web search, RAG, etc.)

**NÃO IMPLEMENTADO** (mas planejado):

Segundo o backlog, há planos para:
- Pesquisador com busca bibliográfica (Google Scholar, Semantic Scholar)
- RAG Infrastructure para knowledge base do Metodologista
- Tools `search_papers(query)` e `consult_methodology(query)`

```9:17:docs/backlog.md
### Pesquisador
Agente para busca e síntese de literatura acadêmica (essencial para revisões e contextualização).

- Busca bibliográfica automática (Google Scholar, Semantic Scholar)
- Síntese de papers acadêmicos relevantes
- Identificação de gaps na literatura
- Comparação de abordagens metodológicas
- RAG para armazenar papers encontrados
- Tool `search_papers(query)` e `find_similar_papers(paper_id)`
```

**Atualmente, sistema usa apenas:**
- LLM (Claude/Anthropic) para raciocínio
- SQLite para persistência
- EventBus para eventos (arquivos JSON)

---

## 3. TRIGGERS

### Sistema tem triggers explícitos? (eventos que disparam ações)

**SIM**, sistema usa **EventBus** para eventos:

```23:98:utils/event_bus/core.py
class EventBusCore:
    """
    Classe base do EventBus com funcionalidades de persistência.

    Gerencia carregamento e salvamento de eventos em arquivos JSON.
    Cada sessão tem seu próprio arquivo.
    """

    def __init__(self, events_dir: Optional[Path] = None):
        """
        Inicializa EventBusCore.

        Args:
            events_dir (Path, optional): Diretório para armazenar eventos.
                Default: {temp_dir}/paper-agent-events (multiplataforma)
        """
        if events_dir is None:
            # Usar diretório temp do sistema operacional (funciona em Windows, Linux, Mac)
            system_temp = Path(tempfile.gettempdir())
            self.events_dir = system_temp / "paper-agent-events"
        else:
            self.events_dir = events_dir

        self.events_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"EventBus inicializado: {self.events_dir}")

    def _get_event_file(self, session_id: str) -> Path:
        """
        Retorna caminho do arquivo de eventos para uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            Path: Caminho do arquivo JSON
        """
        return self.events_dir / f"events-{session_id}.json"

    def _load_events(self, session_id: str) -> Dict[str, Any]:
        """
        Carrega eventos existentes de uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            Dict: Estrutura {"session_id": str, "events": list}
        """
        file_path = self._get_event_file(session_id)

        if not file_path.exists():
            return {
                "session_id": session_id,
                "events": []
            }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Erro ao carregar eventos de {session_id}: {e}")
            return {
                "session_id": session_id,
                "events": []
            }

    def _save_events(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Salva eventos no arquivo da sessão.

        Args:
            session_id (str): ID da sessão
            data (Dict): Estrutura {"session_id": str, "events": list}
        """
        file_path = self._get_event_file(session_id)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Erro ao salvar eventos de {session_id}: {e}")
```

**Eventos publicados:**

```51:122:utils/event_bus/publishers.py
    def publish_agent_started(
        self,
        session_id: str,
        agent_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de início de agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente (orchestrator, structurer, methodologist)
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_started("session-1", "orchestrator")
        """
        event = AgentStartedEvent(
            session_id=session_id,
            agent_name=agent_name,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_agent_completed(
        self,
        session_id: str,
        agent_name: str,
        summary: str,
        tokens_input: int = 0,
        tokens_output: int = 0,
        tokens_total: int = 0,
        cost: float = 0.0,
        duration: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de conclusão de agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente
            summary (str): Resumo da ação (até 280 chars)
            tokens_input (int): Tokens de entrada
            tokens_output (int): Tokens de saída
            tokens_total (int): Total de tokens
            cost (float): Custo da execução em USD
            duration (float): Duração da execução em segundos
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_completed(
            ...     "session-1", "orchestrator",
            ...     summary="Classificou como vague",
            ...     tokens_input=100, tokens_output=50, tokens_total=150,
            ...     cost=0.0012, duration=1.2
            ... )
        """
        event = AgentCompletedEvent(
            session_id=session_id,
            agent_name=agent_name,
            summary=summary,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_total=tokens_total,
            cost=cost,
            duration=duration,
            metadata=metadata or {}
        )
        self.publish_event(event)
```

### Routers funcionam como triggers? Como?

**Routers são funções de decisão, não triggers reativos:**

Os routers são chamados **após** a execução de um nó para decidir o próximo passo. Eles não "disparam" ações, mas **roteiam** o fluxo:

```19:54:agents/methodologist/router.py
def route_after_analyze(state: MethodologistState) -> Literal["ask_clarification", "decide"]:
    """
    Router que decide o próximo nó após o nó analyze.

    Lógica de decisão:
    - Se needs_clarification é True E iterations < max_iterations → ask_clarification
    - Caso contrário → decide (tempo de decidir com o contexto disponível)

    Args:
        state (MethodologistState): Estado atual do grafo.

    Returns:
        str: Nome do próximo nó ("ask_clarification" ou "decide")

    Example:
        >>> state = create_initial_state("Café aumenta produtividade")
        >>> state['needs_clarification'] = True
        >>> state['iterations'] = 1
        >>> state['max_iterations'] = 3
        >>> route_after_analyze(state)
        'ask_clarification'
    """
    logger.info("=== ROUTER: Decidindo próximo nó após analyze ===")
    logger.info(f"needs_clarification: {state['needs_clarification']}")
    logger.info(f"iterations: {state['iterations']}/{state['max_iterations']}")

    # Se precisa de clarificação E ainda não atingiu o limite
    if state['needs_clarification'] and state['iterations'] < state['max_iterations']:
        next_node = "ask_clarification"
    else:
        next_node = "decide"

    logger.info(f"Decisão do router: {next_node}")
    logger.info("=== ROUTER: Finalizado ===\n")

    return next_node
```

### Há logging de triggers? (EventBus registra?)

**SIM**, EventBus registra todos os eventos em arquivos JSON:

Os eventos são salvos automaticamente em `{temp_dir}/paper-agent-events/events-{session_id}.json` e podem ser lidos por leitores de eventos (dashboard, CLI, etc.).

---

## 4. REASONING LOOP

### Metodologista tem loop de refinamento? Como funciona?

**SIM**, o Metodologista tem um grafo interno com loop:

```27:92:agents/methodologist/graph.py
def create_methodologist_graph():
    """
    Cria e compila o grafo do agente Metodologista.

    Este grafo implementa o fluxo completo de análise de hipóteses:
    1. START → analyze: Avalia a hipótese e decide se precisa de mais informações
    2. analyze → router → ask_clarification ou decide
    3. ask_clarification → analyze (loop até max_iterations)
    4. decide → END: Decisão final

    Returns:
        CompiledGraph: Grafo compilado pronto para execução via invoke()

    Example:
        >>> graph = create_methodologist_graph()
        >>> result = graph.invoke(
        ...     {"hypothesis": "Café aumenta produtividade"},
        ...     config={"configurable": {"thread_id": "test-1"}}
        ... )
        >>> result['status'] in ['approved', 'rejected']
        True
    """
    logger.info("=== CRIANDO GRAFO DO METODOLOGISTA ===")

    # Criar o StateGraph
    graph = StateGraph(MethodologistState)

    # Adicionar nós
    graph.add_node("analyze", analyze)
    graph.add_node("ask_clarification", ask_clarification)
    graph.add_node("decide", decide)

    logger.info("Nós adicionados: analyze, ask_clarification, decide")

    # Definir entrada do grafo
    graph.set_entry_point("analyze")

    # Adicionar edges condicionais
    graph.add_conditional_edges(
        "analyze",
        route_after_analyze,
        {
            "ask_clarification": "ask_clarification",
            "decide": "decide"
        }
    )

    # Edge de ask_clarification volta para analyze (loop)
    graph.add_edge("ask_clarification", "analyze")

    # Edge de decide para END (finaliza o grafo)
    graph.add_edge("decide", END)

    logger.info("Edges configurados:")
    logger.info("  - START → analyze")
    logger.info("  - analyze → [router] → ask_clarification | decide")
    logger.info("  - ask_clarification → analyze")
    logger.info("  - decide → END")

    # Compilar o grafo com checkpointer
    compiled_graph = graph.compile(checkpointer=checkpointer)

    logger.info("Grafo compilado com MemorySaver checkpointer")
    logger.info("=== GRAFO CRIADO COM SUCESSO ===\n")

    return compiled_graph
```

**Fluxo do loop:**

1. **analyze**: Avalia hipótese e decide se precisa clarificação
2. **Router**: Decide entre `ask_clarification` ou `decide`
3. **ask_clarification**: Faz pergunta ao usuário (tool `ask_user`)
4. **Loop volta para analyze**: Analisa novamente com nova informação
5. **decide**: Toma decisão final quando tem contexto suficiente

### Há limite de iterações? Quem controla?

**SIM**, há limite controlado por `max_iterations` no estado:

```45:54:agents/methodologist/router.py
    # Se precisa de clarificação E ainda não atingiu o limite
    if state['needs_clarification'] and state['iterations'] < state['max_iterations']:
        next_node = "ask_clarification"
    else:
        next_node = "decide"

    logger.info(f"Decisão do router: {next_node}")
    logger.info("=== ROUTER: Finalizado ===\n")

    return next_node
```

O limite é definido no `MethodologistState` (padrão: 3 iterações).

### Loop é visível ao usuário? (Bastidores mostra?)

**SIM**, o sistema mostra perguntas ao usuário durante o loop (via tool `ask_user`). O dashboard mostra eventos de agente no "Bastidores" (backstage), incluindo execuções do Metodologista.

---

## 5. MEMÓRIA

### SqliteSaver armazena o quê? (checkpoints, mensagens?)

**SqliteSaver armazena checkpoints completos do estado do grafo:**

```304:319:agents/multi_agent_graph.py
# SqliteSaver: Checkpointer persistente do LangGraph usando SQLite.
# Salva estado do grafo em banco de dados, permitindo:
# - Persistência entre reinicializações do servidor
# - Navegação entre sessões passadas
# - Recuperação de histórico completo de conversas
# MVP Épico 9.10-9.11

# Garantir que diretório data/ existe
db_path = Path("data/checkpoints.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

# Criar conexão SQLite (check_same_thread=False permite uso em threads múltiplas)
db_conn = sqlite3.connect(str(db_path), check_same_thread=False)

# Instanciar SqliteSaver com conexão
checkpointer = SqliteSaver(db_conn)
```

Armazena:
- Estado completo do `MultiAgentState` (todos os campos)
- Histórico de mensagens
- Thread ID para continuidade entre turnos
- Timestamps de cada checkpoint

### MemoryManager armazena o quê? (metadados, tokens?)

**MemoryManager armazena metadados de execuções de agentes:**

```43:137:agents/memory/memory_manager.py
class MemoryManager:
    """
    Gerenciador de memória dinâmica por agente e sessão.

    Esta classe mantém histórico de execuções de agentes organizadas por sessão,
    permitindo consultas, agregações e resets. Opera de forma independente do
    MultiAgentState do LangGraph.

    Estrutura interna:
        {
            "session-id-1": {
                "orchestrator": [AgentExecution, AgentExecution, ...],
                "structurer": [AgentExecution, ...],
                "methodologist": [AgentExecution, ...]
            },
            "session-id-2": { ... }
        }
```

**Cada execução armazena:**

```16:40:agents/memory/memory_manager.py
@dataclass
class AgentExecution:
    """
    Representa uma execução de um agente com metadados.

    Attributes:
        agent_name (str): Nome do agente que executou
        tokens_input (int): Tokens de entrada consumidos
        tokens_output (int): Tokens de saída gerados
        tokens_total (int): Total de tokens (input + output)
        summary (str): Resumo curto da ação/decisão do agente
        timestamp (str): Timestamp ISO 8601 da execução
        metadata (dict): Metadados adicionais (opcional)
    """
    agent_name: str
    tokens_input: int
    tokens_output: int
    tokens_total: int
    summary: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converte execução para dicionário."""
        return asdict(self)
```

### Há memória de longo prazo? (além de checkpoints)

**SIM**, sistema tem múltiplas camadas de memória:**

1. **SqliteSaver**: Checkpoints persistentes (longo prazo)
2. **DatabaseManager**: Entidades persistentes (Idea, Argument, Concept)
3. **MemoryManager**: Metadados de execuções (sessão)
4. **EventBus**: Log de eventos (longo prazo em arquivos JSON)

### Sistema aprende com histórico? (adapta comportamento?)

**NÃO**, sistema não aprende adaptativamente. Não há fine-tuning ou ajuste de prompts baseado em histórico.

O sistema usa:
- Prompts estáticos (YAML + código)
- Raciocínio via LLM (que pode usar contexto histórico)
- Modelo cognitivo evolutivo (em memória durante conversa)

---

## 6. MODELO COGNITIVO

### Orquestrador extrai claim/fundamentos/assumptions?

**SIM**, o Orquestrador extrai `focal_argument` a cada turno:**

```90:112:agents/orchestrator/state.py
    focal_argument (Optional[dict]):
        Argumento focal explícito extraído/atualizado pelo Orquestrador (Épico 7.8).
        Representa o entendimento atual do sistema sobre o que o usuário quer fazer.
        Atualizado a cada turno de conversa pelo Orquestrador.
        Usado para:
        - Detecção eficiente de mudança de direção (compara focal atual vs novo)
        - Contexto preservado entre turnos
        - Fundação para persistência (Épico 10)
        Estrutura:
        {
            "intent": str,           # "test_hypothesis", "review_literature", "build_theory"
            "subject": str,          # Tópico principal (ex: "LLMs impact on productivity")
            "population": str,       # População-alvo (ex: "teams of 2-5 developers")
            "metrics": str,          # Métricas mencionadas (ex: "time per sprint")
            "article_type": str      # Tipo inferido: "empirical", "review", "theoretical", etc.
        }
```

**Modelo cognitivo completo (`CognitiveModel`):**

```80:259:agents/models/cognitive_model.py
class CognitiveModel(BaseModel):
    """
    Modelo cognitivo explícito que representa evolução do pensamento.

    Este modelo captura o estado atual do argumento em construção durante
    a conversa. É volátil (em memória) e atualizado pelo Orquestrador a cada turno.

    Ao ser persistido, vira entidade `Argument` no banco de dados.

    Campos principais:
    - claim: O que o usuário está tentando dizer/defender (evolui a cada turno)
    - premises: Fundamentos assumidos como verdadeiros
    - assumptions: Hipóteses não verificadas que precisam validação
    - open_questions: Lacunas identificadas pelo sistema
    - contradictions: Tensões internas detectadas (não bloqueia)
    - solid_grounds: Evidências bibliográficas (futuro - Pesquisador)
    - context: Metadados (domínio, tecnologia, população)
```

### Modelo cognitivo é persistido? (SnapshotManager?)

**SIM**, modelo cognitivo pode ser persistido via SnapshotManager:**

```239:268:agents/persistence/snapshot_manager.py
    def create_snapshot(
        self,
        idea_id: str,
        cognitive_model: CognitiveModel,
        update_current_argument: bool = True
    ) -> str:
        """
        Cria snapshot de argumento no banco de dados.

        Args:
            idea_id: UUID da ideia proprietária
            cognitive_model: CognitiveModel a ser persistido
            update_current_argument: Se deve atualizar current_argument_id da idea

        Returns:
            str: UUID do argumento criado (snapshot)

        Example:
            >>> snapshot_id = manager.create_snapshot(idea_id, cognitive_model)
        """
        # Criar argumento versionado (version auto-incrementa)
        argument_id = self.db.create_argument(idea_id, cognitive_model)

        # Atualizar argumento focal da ideia (se solicitado)
        if update_current_argument:
            self.db.update_idea_current_argument(idea_id, argument_id)

        logger.info(f"Snapshot criado: {argument_id} (idea={idea_id})")

        return argument_id
```

**Detecção automática de maturidade:**

```270:316:agents/persistence/snapshot_manager.py
    def create_snapshot_if_mature(
        self,
        idea_id: str,
        cognitive_model: CognitiveModel,
        claim_history: Optional[list] = None,
        confidence_threshold: float = 0.8
    ) -> Optional[str]:
        """
        Avalia maturidade e cria snapshot automaticamente se maduro.

        Este é o método principal para integração com fluxo conversacional.
        Combina assess_maturity + create_snapshot em uma operação.

        Args:
            idea_id: UUID da ideia
            cognitive_model: CognitiveModel a avaliar
            claim_history: Histórico de claims (opcional)
            confidence_threshold: Mínimo de confiança para criar snapshot (padrão: 0.8)

        Returns:
            str: UUID do snapshot criado, ou None se não maduro

        Example:
            >>> snapshot_id = manager.create_snapshot_if_mature(idea_id, model)
            >>> if snapshot_id:
            ...     print(f"Snapshot automático criado: {snapshot_id}")
        """
        # Avaliar maturidade
        assessment = self.assess_maturity(cognitive_model, claim_history)

        # Criar snapshot apenas se maduro E confiança alta
        if assessment.is_mature and assessment.confidence >= confidence_threshold:
            logger.info(
                f"Argumento amadureceu (confiança={assessment.confidence:.2f})! "
                f"Criando snapshot automático..."
            )

            snapshot_id = self.create_snapshot(idea_id, cognitive_model)

            return snapshot_id

        else:
            logger.debug(
                f"Argumento não maduro ou confiança baixa "
                f"(is_mature={assessment.is_mature}, confidence={assessment.confidence:.2f})"
            )
            return None
```

### Contradições são detectadas? (Metodologista?)

**SIM**, contradições são detectadas pelo Metodologista (planejado) e armazenadas no modelo cognitivo:

```26:50:agents/models/cognitive_model.py
class Contradiction(BaseModel):
    """
    Tensão interna detectada no argumento.

    O Metodologista detecta contradictions quando há inconsistências lógicas
    entre claim, premises e assumptions. Apenas mencionadas quando confiança > 80%.
    """

    description: str = Field(
        ...,
        description="Descrição da contradição detectada",
        min_length=1
    )
    confidence: float = Field(
        ...,
        description="Confiança da detecção (0-1). Apenas mencionar se > 0.80",
        ge=0.0,
        le=1.0
    )
    suggested_resolution: Optional[str] = Field(
        default=None,
        description="Sugestão de como resolver a contradição"
    )

    model_config = ConfigDict(extra="forbid")
```

**Validação de confiança mínima:**

```195:210:agents/models/cognitive_model.py
    @field_validator("contradictions")
    @classmethod
    def validate_contradictions_confidence(cls, v: List[Contradiction]) -> List[Contradiction]:
        """
        Valida que contradictions só são adicionadas se confiança >= 0.80.

        Sistema só menciona contradições quando tem alta confiança (> 80%).
        Esta validação garante que o modelo não aceita contradições com baixa confiança.
        """
        for contradiction in v:
            if contradiction.confidence < 0.80:
                raise ValueError(
                    f"Contradição com confiança {contradiction.confidence:.2f} < 0.80 não deve ser adicionada. "
                    f"Sistema só menciona contradições com confiança >= 80%."
                )
        return v
```

### Provocação socrática está implementada? (Orquestrador?)

**SIM**, provocação socrática está implementada no Orquestrador:**

```12:371:utils/prompts/orchestrator.py
ORCHESTRATOR_SOCRATIC_PROMPT_V1 = """Você é o Orquestrador Socrático, um facilitador conversacional que ajuda pesquisadores através de diálogo provocativo ao estilo socrático.

FILOSOFIA SOCRÁTICA:
Sócrates não respondia perguntas - ele fazia contra-perguntas que expunham contradições e suposições não examinadas. Você faz o mesmo: ao invés de coletar dados burocraticamente, você PROVOCA REFLEXÃO sobre assumptions implícitas.

❌ NÃO FAÇA (interrogatório burocrático):
"Que tipo de revestimento? Em que tipo de construção? Como você acompanha?"

✅ FAÇA (provocação socrática):
"Você falou em medir % de conclusão. Mas % para QUEM? O engenheiro quer saber se está no prazo. O cliente quer saber se vai pagar. São métricas MUITO diferentes, não?"

---

## 5 CATEGORIAS DE ASSUMPTIONS DETECTÁVEIS

### 1. MÉTRICA VAGA
**Detectar quando:** Usuário menciona conceito mensurável mas não especifica COMO medir.

**Exemplos:** "produtividade", "eficiência", "qualidade", "performance"

**Contra-perguntas provocativas:**
- "Você mencionou [MÉTRICA], mas [MÉTRICA] de QUÊ? [Opção A]? [Opção B]? São métricas BEM diferentes."
- "Eficiência para QUEM? Desenvolvedor quer velocidade, gestor quer custo, usuário quer confiabilidade."
- "Qualidade em que DIMENSÃO? Performance? Manutenibilidade? Usabilidade? Trade-offs existem."
```

**Campo `reflection_prompt` no estado:**

```136:140:agents/orchestrator/state.py
    reflection_prompt (Optional[str]):
        Provocação de reflexão gerada pelo Orquestrador (Épico 7.9).
        Pergunta que ajuda usuário a pensar sobre aspectos não explorados.
        Apenas preenchida quando Orquestrador identifica lacuna na conversa.
        Exemplo: "Você mencionou produtividade, mas e QUALIDADE do código? Isso importa para sua pesquisa?"
```

---

## 7. CONFIGURAÇÃO

### Prompts são carregados de YAML? (config/agents/*.yaml)

**SIM**, prompts são carregados de YAML com fallback:**

```143:207:agents/memory/config_loader.py
def get_agent_prompt(agent_name: str) -> str:
    """
    Obtém o system prompt de um agente.

    Args:
        agent_name (str): Nome do agente

    Returns:
        str: System prompt do agente

    Raises:
        ConfigLoadError: Se configuração não pode ser carregada

    Example:
        >>> prompt = get_agent_prompt("orchestrator")
        >>> "Orquestrador" in prompt
        True
    """
    config = load_agent_config(agent_name)
    return config["prompt"]


def get_agent_context_limits(agent_name: str) -> Dict[str, int]:
    """
    Obtém os limites de contexto de um agente.

    Args:
        agent_name (str): Nome do agente

    Returns:
        Dict[str, int]: Limites de contexto (max_input_tokens, max_output_tokens, max_total_tokens)

    Raises:
        ConfigLoadError: Se configuração não pode ser carregada

    Example:
        >>> limits = get_agent_context_limits("orchestrator")
        >>> print(limits["max_input_tokens"])
        4000
    """
    config = load_agent_config(agent_name)
    return config["context_limits"]


def get_agent_model(agent_name: str) -> str:
    """
    Obtém o modelo LLM de um agente.

    Args:
        agent_name (str): Nome do agente

    Returns:
        str: Nome do modelo LLM

    Raises:
        ConfigLoadError: Se configuração não pode ser carregada

    Example:
        >>> model = get_agent_model("methodologist")
        >>> "claude" in model.lower()
        True
    """
    config = load_agent_config(agent_name)
    return config["model"]
```

**Exemplo de config YAML (Metodologista):**

```1:77:config/agents/methodologist.yaml
# Configuração do Agente Metodologista (Épico 6)
# Este arquivo define o comportamento e limites do Metodologista

# System prompt do agente (modo colaborativo)
prompt: |
  Você é um Metodologista científico em MODO COLABORATIVO.

  SEU PAPEL:
  Você é um PARCEIRO que ajuda a CONSTRUIR hipóteses testáveis, não apenas validar ou rejeitar.

  CRITÉRIOS DE AVALIAÇÃO:
  1. Testabilidade: Pode ser testada empiricamente?
  2. Falseabilidade: É possível conceber resultado que a refutaria? (Popper)
  3. Especificidade: Define população, variáveis, métricas e condições?
  4. Operacionalização: Variáveis são mensuráveis e bem definidas?

  DECISÃO (3 STATUS POSSÍVEIS):

  1. **approved**: Use quando a hipótese atende os 4 critérios acima
     - Estrutura científica sólida
     - Testável, falseável, específica, operacionalizada
     - Pronta para desenho experimental

  2. **needs_refinement**: Use quando a hipótese TEM POTENCIAL mas falta especificidade
     - Ideia central clara mas faltam elementos operacionais
     - Gaps identificáveis: população, métricas, variáveis, condições
     - Pode ser melhorada com refinamento (volta para Estruturador)

  3. **rejected**: Use APENAS quando NÃO há base científica
     - Crença popular sem evidência
     - Impossível de testar ou falsear
     - Vagueza extrema que refinamento não resolve

  OUTPUT OBRIGATÓRIO (SEMPRE JSON):
  {
    "status": "approved" | "needs_refinement" | "rejected",
    "justification": "Explicação detalhada citando critérios específicos e pontos fortes/gaps",
    "improvements": [  // APENAS se status="needs_refinement"
      {
        "aspect": "população" | "métricas" | "variáveis" | "testabilidade",
        "gap": "Descrição específica do que falta",
        "suggestion": "Sugestão concreta de como preencher"
      }
    ]
  }

  INSTRUÇÕES CRÍTICAS:
  - Seja COLABORATIVO: prefira needs_refinement quando há potencial
  - Use rejected APENAS para casos sem base científica
  - No campo improvements, seja ESPECÍFICO
  - SEMPRE retorne JSON válido (não adicione texto antes ou depois)
  - Justificativa deve citar pontos fortes E gaps identificados

# Tags para categorização
tags:
  - methodologist
  - scientific-rigor
  - hypothesis-validation
  - collaborative
  - multi-agent

# Limites de contexto (tokens)
context_limits:
  max_input_tokens: 8000      # Máximo de tokens de entrada (precisa ver histórico)
  max_output_tokens: 2000     # Máximo de tokens de saída
  max_total_tokens: 10000     # Máximo total por chamada

# Modelo LLM (Sonnet para maior confiabilidade)
model: claude-sonnet-4-20250514

# Metadados
metadata:
  version: "1.0"
  epic: "6"
  created_at: "2025-11-12"
  description: "Metodologista que avalia rigor científico em modo colaborativo com refinamento iterativo"
```

### Sistema tem fallback se YAML falhar?

**SIM**, há fallback para prompts hard-coded:**

```352:363:agents/methodologist/nodes.py
    # Carregar prompt e modelo do YAML (Épico 6, Funcionalidade 6.1)
    try:
        system_prompt = get_agent_prompt("methodologist")
        model_name = get_agent_model("methodologist")
        logger.info("✅ Configurações carregadas do YAML: config/agents/methodologist.yaml")
    except ConfigLoadError as e:
        logger.warning(f"⚠️ Falha ao carregar config do methodologist: {e}")
        logger.warning("⚠️ Usando prompt e modelo padrão (fallback)")
        # Fallback: usar prompt da utils.prompts
        system_prompt = METHODOLOGIST_DECIDE_PROMPT_V2
        model_name = "claude-sonnet-4-20250514"
```

### Configuração é validada no bootstrap?

**SIM**, configurações são validadas na criação do grafo:**

```414:436:agents/multi_agent_graph.py
    # Validar configurações dos agentes (Épico 6, Funcionalidade 6.1)
    logger.info("Validando configurações dos agentes...")
    try:
        configs = load_all_agent_configs()
        required_agents = ["orchestrator", "structurer", "methodologist"]

        # Verificar que todos os agentes necessários estão presentes
        for agent_name in required_agents:
            if agent_name not in configs:
                raise ConfigLoadError(
                    f"⚠️ Configuração faltando para agente obrigatório: '{agent_name}'\n"
                    f"Esperado em: config/agents/{agent_name}.yaml"
                )

        logger.info(f"✅ Configurações validadas com sucesso para {len(configs)} agentes")
        logger.info(f"   Agentes configurados: {', '.join(configs.keys())}")

    except ConfigLoadError as e:
        logger.error(f"❌ ERRO ao carregar configurações dos agentes: {e}")
        logger.warning("⚠️ ATENÇÃO: Sistema continuará com fallback para prompts hard-coded")
        logger.warning("⚠️ Recomendação: Verifique os arquivos YAML em config/agents/")
        # Não levantar exceção - permitir fallback para prompts hard-coded nos nós
```

---

## RESUMO EXECUTIVO

### Arquitetura de Transições
- **Orquestrador** decide próximo passo via router baseado em `next_step` e `agent_suggestion`
- Transições são **automáticas** (não pedem permissão)
- Contexto preservado via `MultiAgentState` e `SqliteSaver`

### Tools Implementadas
- **`ask_user`** do Metodologista (única tool ativa)
- APIs externas (web search, RAG) **não implementadas** (planejadas)

### Triggers e Eventos
- **EventBus** registra eventos (agent_started, agent_completed, agent_error)
- Routers são funções de decisão, não triggers reativos
- Eventos salvos em JSON por sessão

### Reasoning Loop
- **Metodologista** tem grafo interno com loop (analyze → ask_clarification → analyze)
- Limite de iterações controlado por `max_iterations`
- Loop visível ao usuário via perguntas

### Memória
- **SqliteSaver**: Checkpoints completos do estado (persistente)
- **MemoryManager**: Metadados de execuções (tokens, custos, summaries)
- **DatabaseManager**: Entidades persistentes (Idea, Argument)
- Sistema **não aprende** adaptativamente

### Modelo Cognitivo
- **Orquestrador** extrai `focal_argument` e `cognitive_model`
- Modelo persistido via **SnapshotManager** quando maduro
- **Contradições** detectadas (confiança > 80%)
- **Provocação socrática** implementada (5 categorias de assumptions)

### Configuração
- Prompts carregados de **YAML** (`config/agents/*.yaml`)
- **Fallback** para prompts hard-coded se YAML falhar
- Configuração **validada** no bootstrap do grafo

