"""
Estruturas de dados para cenários de conversa multi-turn.

Este módulo define ConversationScenario, uma estrutura de dados para representar
cenários de conversa multi-turn que serão usados para validação no Épico 8.1
(Multi-Turn Executor).

"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

@dataclass
class ConversationScenario:
    """Define cenário de conversa multi-turn para validação.
    
    Um ConversationScenario representa uma sequência de turnos de conversa
    entre usuário e sistema, com expectativas sobre quais agentes devem ser
    chamados e qual estado final deve ser alcançado.
    
    Attributes:
        id: Identificador único do cenário (ex: "cenario_03_refinamento")
        description: Descrição do que o cenário valida
        turns: Lista de tuplas (role, content) representando cada turno.
               role pode ser "user" ou "system".
               content é o texto do input do usuário ou ação esperada do sistema.
        expected_agents: Lista de nomes de agentes que devem ser chamados
                        durante a execução (ex: ["orchestrator", "structurer"])
        expected_final_state: Dicionário com campos do estado que devem estar
                             presentes ao final da execução (ex: {"next_step": "explore"})
    
    Example:
        >>> scenario = ConversationScenario.from_epic7_scenario(3)
        >>> scenario.id
        'cenario_03_refinamento'
        >>> len(scenario.turns)
        7
        >>> scenario.expected_agents
        ['orchestrator', 'structurer', 'methodologist']
    """
    
    id: str
    description: str
    turns: List[Tuple[str, str]]
    expected_agents: List[str]
    expected_final_state: Dict[str, Any]
    
    @classmethod
    def from_epic7_scenario(cls, scenario_number: int) -> "ConversationScenario":
        """
        Cria cenário baseado em cenários do Épico 7.
        
        Converte os cenários 3, 6 e 7 do Épico 7 (que foram executados mas
        não completamente validados) para o formato ConversationScenario,
        permitindo validação multi-turn no Épico 8.1.
        
        Args:
            scenario_number: Número do cenário (3, 6 ou 7)
            
        Returns:
            ConversationScenario configurado com fluxo multi-turn esperado
            
        Raises:
            ValueError: Se scenario_number não é 3, 6 ou 7
            
        Example:
            >>> scenario = ConversationScenario.from_epic7_scenario(3)
            >>> scenario.id
            'cenario_03_refinamento'
        """
        scenarios = {
            3: cls(
                id="cenario_03_refinamento",
                description=(
                    "Ideia vaga evolui através de múltiplos turnos: "
                    "Orchestrator explora → Structurer cria V1 → "
                    "Methodologist retorna needs_refinement"
                ),
                turns=[
                    ("user", "Método X melhora desenvolvimento"),
                    ("system", "explore"),  # Orchestrator pede contexto sobre "melhora"
                    ("user", "Melhora velocidade de entrega"),
                    ("system", "suggest_agent:structurer"),  # Orchestrator chama Estruturador
                    ("system", "structurer:create_v1"),  # Structurer cria V1 estruturada
                    ("system", "suggest_agent:methodologist"),  # Orchestrator chama Metodologista
                    ("system", "methodologist:needs_refinement"),  # Methodologist retorna gaps
                ],
                expected_agents=["orchestrator", "structurer", "methodologist"],
                expected_final_state={
                    "next_step": "explore",  # Aguarda refinamento do usuário
                    "methodologist_output.status": "needs_refinement",
                    "hypothesis_versions": lambda v: len(v) > 0,  # Tem pelo menos V1
                }
            ),
            6: cls(
                id="cenario_06_reasoning_loop",
                description=(
                    "Hipótese vaga que requer clarificação: "
                    "Orchestrator explora → Methodologist entra em reasoning loop "
                    "(pede clarificação) → Methodologist decide com contexto suficiente"
                ),
                turns=[
                    ("user", "Hipótese vaga que requer clarificação: Método X melhora desenvolvimento de software"),
                    ("system", "explore"),  # Orchestrator explora
                    ("user", "Melhora velocidade de entrega em equipes pequenas"),
                    ("system", "suggest_agent:methodologist"),  # Orchestrator chama Metodologista
                    ("system", "methodologist:ask_clarification"),  # Methodologist entra em reasoning loop
                    ("user", "Equipes de 2-5 desenvolvedores, medindo tempo por sprint"),
                    ("system", "methodologist:decide"),  # Methodologist decide com contexto suficiente
                ],
                expected_agents=["orchestrator", "methodologist"],
                expected_final_state={
                    "methodologist_output.status": lambda s: s in ["approved", "needs_refinement"],
                    # Verificar que houve iterações (reasoning loop funcionou)
                    # Nota: iterations pode não estar no estado, mas podemos verificar
                    # que methodologist foi chamado múltiplas vezes
                }
            ),
            7: cls(
                id="cenario_07_contexto_longo",
                description=(
                    "Conversa longa (5 turnos) onde focal_argument evolui progressivamente: "
                    "Orchestrator explora múltiplas vezes, contexto se acumula, "
                    "focal_argument reflete evolução completa"
                ),
                turns=[
                    ("user", "Observei que LLMs aumentam produtividade"),
                    ("system", "explore"),  # Orchestrator pede contexto
                    ("user", "Em equipes de 2-5 desenvolvedores"),
                    ("system", "explore"),  # Orchestrator pede métrica
                    ("user", "Medindo tempo de sprint"),
                    ("system", "explore"),  # Orchestrator pede mais detalhes
                    ("user", "Redução de 2h para 1.4h"),
                    ("system", "explore"),  # Orchestrator pergunta sobre qualidade
                    ("user", "Qualidade do código também importa"),
                    ("system", "explore"),  # Orchestrator finaliza exploração
                ],
                expected_agents=["orchestrator"],  # Apenas Orchestrator (múltiplas vezes)
                expected_final_state={
                    "focal_argument.subject": "LLMs impact on sprint time and code quality",
                    "focal_argument.population": "teams of 2-5 developers",
                    "focal_argument.metrics": lambda m: "sprint time" in m and "code quality" in m.lower(),
                    # Verificar que messages tem 10 mensagens (5 turnos × 2 mensagens)
                    "messages": lambda msgs: len(msgs) >= 10,
                }
            ),
        }
        
        if scenario_number not in scenarios:
            raise ValueError(
                f"Cenário {scenario_number} não existe. "
                f"Disponíveis: {list(scenarios.keys())}"
            )
        
        return scenarios[scenario_number]

