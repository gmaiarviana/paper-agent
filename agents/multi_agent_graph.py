"""
Super-grafo multi-agente que integra Orquestrador, Estruturador e Metodologista.

Este módulo implementa o grafo principal do sistema Paper Agent, conectando
múltiplos agentes especializados em uma arquitetura de super-grafo.

Fluxo do sistema (Épico 7 - Orquestrador Conversacional):
1. Orquestrador Conversacional: Analisa input + histórico e decide próximo passo
   - next_step = "explore" → Retorna para usuário (END) - mais perguntas necessárias
   - next_step = "clarify" → Retorna para usuário (END) - esclarecer ambiguidade
   - next_step = "suggest_agent" → Roteia para agente sugerido
2. Router 1: Decide destino baseado em next_step
   - "user" → END (retorna para usuário)
   - "structurer" → Estruturador → Metodologista
   - "methodologist" → Metodologista direto
3. Estruturador (se chamado): Organiza ideia vaga em questão estruturada
4. Metodologista (se chamado): Valida rigor científico (3 status: approved, needs_refinement, rejected)
5. Router 2: Metodologista sempre retorna para Orquestrador (apresenta feedback ao usuário)

Versão: 4.0 (Épico 7 POC - Orquestrador Conversacional + integração com Épico 5.1/6)
Data: 14/11/2025
"""

import logging
import time
import sqlite3
from pathlib import Path
from typing import Callable, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node
from agents.orchestrator.router import route_from_orchestrator
from agents.structurer.nodes import structurer_node
from agents.methodologist.nodes import decide_collaborative
from agents.memory.config_loader import load_all_agent_configs, ConfigLoadError

# Import EventBus para emitir eventos (Épico 5.1)
try:
    from utils.event_bus import get_event_bus
    EVENT_BUS_AVAILABLE = True
except ImportError:
    EVENT_BUS_AVAILABLE = False

logger = logging.getLogger(__name__)


# === INSTRUMENTAÇÃO COM EVENTBUS (Épico 5.1) ===

def _get_session_id_from_config(config: Any) -> str:
    """
    Extrai session_id do config do LangGraph.

    Args:
        config: Configuração do LangGraph

    Returns:
        str: Session ID ou fallback para thread_id
    """
    if not config:
        logger.debug("_get_session_id_from_config: config é None/vazio")
        return "unknown-session"

    configurable = config.get("configurable", {})
    session_id = configurable.get("session_id")

    if session_id:
        logger.debug(f"_get_session_id_from_config: session_id extraído = {session_id}")
        return session_id

    # Fallback: usar thread_id como session_id
    thread_id = configurable.get("thread_id", "unknown-session")
    logger.debug(f"_get_session_id_from_config: fallback para thread_id = {thread_id}")
    return thread_id


def instrument_node(node_func: Callable, agent_name: str) -> Callable:
    """
    Instrumenta um nó do grafo para emitir eventos via EventBus (Épico 5.1).

    Wrapper que:
    1. Emite evento agent_started antes da execução
    2. Executa o nó original
    3. Emite evento agent_completed após sucesso
    4. Emite evento agent_error em caso de falha

    Args:
        node_func (Callable): Função do nó original
        agent_name (str): Nome do agente (orchestrator, structurer, methodologist)

    Returns:
        Callable: Nó instrumentado

    Example:
        >>> instrumented_node = instrument_node(orchestrator_node, "orchestrator")
    """
    def wrapper(state: MultiAgentState, config: Any = None) -> MultiAgentState:
        """Wrapper instrumentado que emite eventos."""
        # Extrair session_id do state (método confiável - Épico 5.1)
        # Config não é passado aos nodes pelo LangGraph, então usamos state
        session_id = state.get("session_id", "unknown-session")
        logger.debug(f"Wrapper {agent_name}: session_id do state = {session_id}")

        # Capturar tempo de início (Épico 8.3)
        start_time = time.time()

        # Emitir evento de início
        if EVENT_BUS_AVAILABLE:
            try:
                bus = get_event_bus()
                bus.publish_agent_started(
                    session_id=session_id,
                    agent_name=agent_name,
                    metadata={
                        "stage": state.get("current_stage", "unknown"),
                        "reasoning": f"Iniciando processamento do agente {agent_name}"  # Épico 8.1
                    }
                )
                logger.info(f"✅ Evento agent_started publicado para {agent_name} (session: {session_id})")
            except Exception as e:
                logger.warning(f"Falha ao publicar agent_started para {agent_name}: {e}")

        # Executar nó original (passando config para nodes que precisam - Épico 6.2 MemoryManager)
        try:
            result = node_func(state, config)

            # Capturar tempo de fim e calcular duração (Épico 8.3)
            end_time = time.time()
            duration = end_time - start_time

            # Emitir evento de conclusão
            if EVENT_BUS_AVAILABLE:
                try:
                    bus = get_event_bus()

                    # Extrair summary baseado no agente
                    summary = _extract_summary(agent_name, result)

                    # Extrair reasoning para metadata (Épico 8.1)
                    reasoning = _extract_reasoning(agent_name, result)

                    # Extrair tokens e custo do state retornado pelo nó (Épico 8.3)
                    # IMPORTANTE: Config não é passado aos wrappers pelo LangGraph (ver linha 99)
                    # Solução: Cada nó extrai seus tokens via token_extractor e retorna no state
                    tokens_input = result.get("last_agent_tokens_input", 0)
                    tokens_output = result.get("last_agent_tokens_output", 0)
                    tokens_total = tokens_input + tokens_output
                    cost = result.get("last_agent_cost", 0.0)

                    logger.debug(f"   Tokens extraídos do state: input={tokens_input}, output={tokens_output}, total={tokens_total}, cost=${cost:.4f}")

                    bus.publish_agent_completed(
                        session_id=session_id,
                        agent_name=agent_name,
                        summary=summary,
                        tokens_input=tokens_input,
                        tokens_output=tokens_output,
                        tokens_total=tokens_total,
                        cost=cost,
                        duration=duration,
                        metadata={"reasoning": reasoning}  # Épico 8.1: reasoning em metadata
                    )
                    logger.info(f"✅ Evento agent_completed publicado para {agent_name} (session: {session_id})")
                    logger.debug(f"   Reasoning: {reasoning[:100]}...")
                    logger.debug(f"   Métricas: {tokens_total} tokens, ${cost:.4f}, {duration:.2f}s")
                except Exception as e:
                    logger.warning(f"Falha ao publicar agent_completed para {agent_name}: {e}")

            return result

        except Exception as error:
            # Capturar duração mesmo em caso de erro
            end_time = time.time()
            duration = end_time - start_time

            # Emitir evento de erro
            if EVENT_BUS_AVAILABLE:
                try:
                    bus = get_event_bus()
                    bus.publish_agent_error(
                        session_id=session_id,
                        agent_name=agent_name,
                        error_message=str(error),
                        error_type=type(error).__name__,
                        metadata={"duration": duration}
                    )
                except Exception as e:
                    logger.warning(f"Falha ao publicar agent_error para {agent_name}: {e}")

            # Re-lançar exceção original
            raise

    return wrapper


def _extract_summary(agent_name: str, state: MultiAgentState) -> str:
    """
    Extrai resumo da ação do agente baseado no resultado.

    Args:
        agent_name (str): Nome do agente
        state (MultiAgentState): Estado após execução

    Returns:
        str: Resumo curto da ação
    """
    if agent_name == "orchestrator":
        # Épico 7: Orquestrador conversacional (novos campos)
        next_step = state.get("next_step")
        if next_step:
            return f"Próximo passo: {next_step}"
        # Fallback: Épico 3 (campos antigos - para compatibilidade)
        classification = state.get("orchestrator_classification", "unknown")
        return f"Classificou input como '{classification}'"

    elif agent_name == "structurer":
        output = state.get("structurer_output", {})
        version = output.get("version", "unknown")
        return f"Estruturou questão de pesquisa (V{version})"

    elif agent_name in ["methodologist", "force_decision"]:
        output = state.get("methodologist_output", {})
        status = output.get("status", "unknown")
        return f"Decisão metodológica: {status}"

    else:
        return f"Executou {agent_name}"


def _extract_reasoning(agent_name: str, state: MultiAgentState) -> str:
    """
    Extrai reasoning detalhado da ação do agente (Épico 8.1).

    Este reasoning é texto livre que explica o processo de pensamento do agente,
    permitindo transparência completa do sistema para o usuário.

    Args:
        agent_name (str): Nome do agente
        state (MultiAgentState): Estado após execução

    Returns:
        str: Reasoning detalhado em texto livre
    """
    if agent_name == "orchestrator":
        # Épico 7 MVP: Orquestrador conversacional tem analysis completo
        analysis = state.get("orchestrator_analysis", "")
        if analysis:
            return analysis
        # Fallback para compatibilidade
        return "Análise contextual do input do usuário"

    elif agent_name == "structurer":
        # Épico 8.1: Estruturador reasoning baseado em modo
        output = state.get("structurer_output", {})

        # Detectar modo: estruturação inicial ou refinamento
        methodologist_feedback = state.get('methodologist_output')
        is_refinement = (
            methodologist_feedback is not None and
            methodologist_feedback.get('status') == 'needs_refinement'
        )

        if is_refinement:
            # Modo refinamento
            version = output.get("version", 2)
            addressed_gaps = output.get("addressed_gaps", [])
            gaps_count = len(addressed_gaps)
            gaps_str = ", ".join(addressed_gaps) if addressed_gaps else "nenhum gap específico"

            return (
                f"Refinando questão para V{version}. "
                f"Endereçando {gaps_count} gap(s) do Metodologista: {gaps_str}. "
                f"Mantendo essência da ideia original enquanto incorpora feedback científico."
            )
        else:
            # Modo estruturação inicial
            elements = output.get("elements", {})
            context = elements.get("context", "N/A")[:50]
            problem = elements.get("problem", "N/A")[:50]
            contribution = elements.get("contribution", "N/A")[:50]

            return (
                f"Estruturando V1 com base em: "
                f"contexto ({context}...), "
                f"problema ({problem}...), "
                f"contribuição potencial ({contribution}...)."
            )

    elif agent_name in ["methodologist", "force_decision"]:
        # Épico 8: Metodologista reasoning
        output = state.get("methodologist_output", {})
        status = output.get("status", "unknown")
        justification = output.get("justification", "")

        if justification:
            return f"Decisão: {status}. Justificativa: {justification}"
        else:
            return f"Validação metodológica resultou em: {status}"

    else:
        return f"Processamento do agente {agent_name}"


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


def route_after_methodologist(state: MultiAgentState) -> str:
    """
    Router que decide o fluxo após o Metodologista processar a hipótese (Épico 4).

    NOVO COMPORTAMENTO (Refinamento Sob Demanda):
    - Sempre retorna para o Orquestrador após o Metodologista
    - Orquestrador apresenta feedback e opções ao usuário
    - Usuário decide se quer refinar, pesquisar, ou mudar de direção

    Args:
        state (MultiAgentState): Estado do sistema multi-agente.

    Returns:
        str: Sempre "orchestrator" (para negociação com usuário)
    """
    methodologist_output = state.get('methodologist_output')

    if not methodologist_output:
        logger.warning("methodologist_output não encontrado. Retornando para Orquestrador.")
        return "orchestrator"

    status = methodologist_output.get('status')
    logger.info(f"=== ROUTER APÓS METODOLOGISTA ===")
    logger.info(f"Status: {status}")
    logger.info("Retornando para Orquestrador (negociação com usuário)")

    # Sempre retorna para Orquestrador (que negocia com usuário)
    return "orchestrator"


def create_multi_agent_graph():
    """
    Cria e compila o super-grafo multi-agente do sistema Paper Agent.

    Este grafo implementa o fluxo completo com loop de refinamento colaborativo (Épico 4):

    Fluxo 1 - Ideia vaga + refinamento:
        START → Orquestrador (classifica: "vague")
              → Estruturador (gera V1)
              → Metodologista (valida: "needs_refinement")
              → Estruturador (gera V2 refinada)
              → Metodologista (valida: "approved")
              → END

    Fluxo 2 - Hipótese → Metodologista direto:
        START → Orquestrador (classifica: "semi_formed" ou "complete")
              → Metodologista (valida: "approved" ou "rejected")
              → END

    Fluxo 3 - Refinamento sob demanda:
        ...  → Metodologista (valida: "needs_refinement")
             → Orquestrador (apresenta opções ao usuário)
             → [usuário decide próximo passo]

    Estrutura do grafo (Épico 4 - Refinamento Sob Demanda):
        - Nós:
            * orchestrator: Classifica maturidade do input e negocia com usuário
            * structurer: Organiza/refina questões (V1, V2, V3)
            * methodologist: Valida rigor (modo colaborativo)

        - Edges:
            * START → orchestrator
            * orchestrator → [router 1] → structurer | methodologist
            * structurer → methodologist
            * methodologist → orchestrator (sempre - para negociação com usuário)

        - State: MultiAgentState com hypothesis_versions (histórico de versões)

    Registro de Memória (Épico 6.2):
        Para habilitar registro de tokens e custos, passe MemoryManager no config:

        >>> from agents.memory.memory_manager import MemoryManager
        >>> memory_manager = MemoryManager()
        >>> config = {
        ...     "configurable": {
        ...         "thread_id": "session-123",
        ...         "memory_manager": memory_manager  # Opcional (Épico 6.2)
        ...     }
        ... }
        >>> result = graph.invoke(state, config=config)
        >>> totals = memory_manager.get_session_totals("session-123")
        >>> print(f"Total: {totals['total']} tokens")

    Returns:
        CompiledGraph: Super-grafo compilado pronto para execução via invoke()

    Example:
        >>> graph = create_multi_agent_graph()
        >>> state = create_initial_multi_agent_state("Método X é rápido")
        >>> result = graph.invoke(state, config={"configurable": {"thread_id": "1"}})
        >>> result['methodologist_output']['status']
        'approved'  # Após 1-2 refinamentos
        >>> len(result['hypothesis_versions'])
        2  # V1 + V2
    """
    logger.info("=== CRIANDO SUPER-GRAFO MULTI-AGENTE COM LOOP DE REFINAMENTO ===")

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

    # Criar o StateGraph com MultiAgentState
    graph = StateGraph(MultiAgentState)
    logger.info("StateGraph criado com MultiAgentState")

    # Adicionar nós do sistema (Épico 4 + 5.1 com instrumentação)
    # Instrumentar nós para emitir eventos via EventBus (Épico 5.1)
    graph.add_node("orchestrator", instrument_node(orchestrator_node, "orchestrator"))
    graph.add_node("structurer", instrument_node(structurer_node, "structurer"))
    graph.add_node("methodologist", instrument_node(decide_collaborative, "methodologist"))  # Modo colaborativo
    logger.info("Nós adicionados (instrumentados): orchestrator, structurer, methodologist")

    # Definir entry point
    graph.set_entry_point("orchestrator")
    logger.info("Entry point: orchestrator")

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
    logger.info("Edge condicional: orchestrator → [router1] → structurer | methodologist | user (END)")

    # Estruturador → Metodologista (sempre)
    graph.add_edge("structurer", "methodologist")
    logger.info("Edge fixo: structurer → methodologist")

    # ROUTER 2: Metodologista → Orquestrador (sempre - para negociação com usuário)
    graph.add_conditional_edges(
        "methodologist",
        route_after_methodologist,
        {
            "orchestrator": "orchestrator"  # Sempre retorna para Orquestrador
        }
    )
    logger.info("Edge condicional: methodologist → orchestrator (negociação com usuário)")

    # Compilar o grafo com checkpointer
    compiled_graph = graph.compile(checkpointer=checkpointer)
    logger.info("Super-grafo compilado com SqliteSaver checkpointer (persistente)")

    logger.info("=== SUPER-GRAFO COM LOOP DE REFINAMENTO CRIADO COM SUCESSO ===")
    logger.info("")
    logger.info("Fluxos disponíveis (Épico 4 - Refinamento Sob Demanda):")
    logger.info("  1. Ideia vaga → Orquestrador → Estruturador (V1) → Metodologista")
    logger.info("     → Orquestrador (apresenta feedback) → [usuário decide próximo passo]")
    logger.info("  2. Hipótese → Orquestrador → Metodologista → Orquestrador")
    logger.info("  3. Refinamento: controlado pelo usuário (sem limite fixo)")
    logger.info("")

    return compiled_graph


# Exportar função helper para criar estado inicial
__all__ = ['create_multi_agent_graph', 'create_initial_multi_agent_state']
