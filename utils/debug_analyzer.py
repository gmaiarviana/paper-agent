"""
Ferramenta de debug para análise detalhada de cenários multi-turn.

Mostra:
- Reasoning completo do Orquestrador em cada turno
- Decisões tomadas (next_step, agent_suggestion)
- Estado antes/depois de cada transição
- Focal argument em cada turno
"""

from typing import Dict, List, Any
from pathlib import Path

from utils.test_executor import MultiTurnExecutor
from utils.event_bus.singleton import get_event_bus


class DebugAnalyzer:
    """
    Analisa execução de cenário com logs detalhados para troubleshooting.
    
    Example:
        >>> from agents.multi_agent_graph import create_multi_agent_graph
        >>> from utils.test_scenarios import ConversationScenario
        >>> 
        >>> graph = create_multi_agent_graph()
        >>> analyzer = DebugAnalyzer(graph)
        >>> scenario = ConversationScenario.from_epic7_scenario(3)
        >>> report = analyzer.analyze_scenario(scenario)
        >>> print(report)
    """
    
    def __init__(self, graph):
        """
        Args:
            graph: Grafo multi-agente compilado
        """
        self.executor = MultiTurnExecutor(graph)
        self.event_bus = get_event_bus()
    
    def analyze_scenario(self, scenario) -> str:
        """
        Executa cenário e gera relatório de debug detalhado.
        
        Args:
            scenario: ConversationScenario a analisar
            
        Returns:
            String formatada com análise completa
        """
        # Executar cenário
        result = self.executor.execute_scenario(scenario)
        
        # Gerar relatório
        return self._generate_debug_report(result, scenario)
    
    def _generate_debug_report(self, result: Dict, scenario) -> str:
        """
        Gera relatório de debug formatado.
        
        Args:
            result: Resultado do execute_scenario()
            scenario: Cenário executado
            
        Returns:
            String formatada para análise
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"DEBUG REPORT: {result['scenario_id']}")
        lines.append("=" * 80)
        lines.append("")
        
        # Status geral
        status_icon = "✅" if result['success'] else "❌"
        lines.append(f"Status: {status_icon} {'SUCESSO' if result['success'] else 'FALHA'}")
        lines.append("")
        
        # Erros de validação (se houver)
        if result['validation_errors']:
            lines.append("⚠️ ERROS DE VALIDAÇÃO:")
            for error in result['validation_errors']:
                lines.append(f"  - {error}")
            lines.append("")
        
        lines.append("-" * 80)
        lines.append("ANÁLISE TURN-BY-TURN")
        lines.append("-" * 80)
        
        # Analisar cada turno
        session_id = result['session_id']
        final_state = result['final_state']
        
        for turn in result['turns']:
            turn_num = turn['turn']
            lines.append("")
            lines.append(f"{'=' * 40} TURNO {turn_num} {'=' * 40}")
            lines.append("")
            
            # Input do usuário
            lines.append(f"[INPUT DO USUÁRIO]")
            lines.append(f"{turn['user_input']}")
            lines.append("")
            
            # Obter reasoning do Orquestrador via EventBus
            reasoning = self._get_orchestrator_reasoning(session_id, turn_num)
            if reasoning:
                lines.append(f"[REASONING DO ORQUESTRADOR]")
                lines.append(reasoning)
                lines.append("")
            
            # Decisão tomada
            lines.append(f"[DECISÃO]")
            lines.append(f"  next_step: {turn['next_step']}")
            lines.append(f"  agentes chamados: {', '.join(turn['agents_called']) if turn['agents_called'] else 'nenhum'}")
            lines.append("")
            
            # Focal argument neste turno
            focal_arg = turn.get('focal_argument', {})
            if focal_arg:
                lines.append(f"[FOCAL ARGUMENT]")
                lines.append(f"  intent: {focal_arg.get('intent', 'N/A')}")
                lines.append(f"  subject: {focal_arg.get('subject', 'N/A')}")
                lines.append(f"  population: {focal_arg.get('population', 'N/A')}")
                lines.append(f"  metrics: {focal_arg.get('metrics', 'N/A')}")
                lines.append("")
            
            # Resposta ao usuário
            if turn['system_response']:
                lines.append(f"[RESPOSTA AO USUÁRIO]")
                lines.append(f"{turn['system_response'][:200]}...")
                lines.append("")
        
        # Estado final completo
        lines.append("")
        lines.append("=" * 80)
        lines.append("ESTADO FINAL COMPLETO")
        lines.append("=" * 80)
        lines.append("")
        
        # Focal argument final
        final_focal = final_state.get('focal_argument', {})
        lines.append("[FOCAL ARGUMENT FINAL]")
        for key, value in final_focal.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        # Hypothesis versions
        hyp_versions = final_state.get('hypothesis_versions', [])
        if hyp_versions:
            lines.append(f"[HYPOTHESIS VERSIONS] ({len(hyp_versions)} versões)")
            for i, version in enumerate(hyp_versions, 1):
                lines.append(f"  V{i}: {version.get('hypothesis', 'N/A')[:80]}...")
        else:
            lines.append("[HYPOTHESIS VERSIONS] Nenhuma versão criada")
        lines.append("")
        
        # Methodologist output
        method_output = final_state.get('methodologist_output')
        if method_output:
            lines.append("[METHODOLOGIST OUTPUT]")
            lines.append(f"  status: {method_output.get('status', 'N/A')}")
            lines.append(f"  justification: {method_output.get('justification', 'N/A')[:80]}...")
        lines.append("")
        
        # Métricas
        lines.append("=" * 80)
        lines.append("MÉTRICAS")
        lines.append("=" * 80)
        metrics = result['metrics']
        lines.append(f"Total de tokens: {metrics['total_tokens']}")
        lines.append(f"Custo total: ${metrics['total_cost']:.4f}")
        lines.append(f"Duração total: {metrics['total_duration']:.2f}s")
        lines.append("")
        
        # Questões para análise
        lines.append("=" * 80)
        lines.append("PERGUNTAS PARA ANÁLISE")
        lines.append("=" * 80)
        lines.append("")
        
        if not result['success']:
            lines.append("Copie este relatório e pergunte ao Claude:")
            lines.append("")
            
            if "structurer" not in result['agents_called'] and "structurer" in scenario.expected_agents:
                lines.append("1. Por que o Orquestrador não chamou o Estruturador?")
                lines.append("   - Qual foi o reasoning em cada turno?")
                lines.append("   - O que faltou para considerar contexto suficiente?")
                lines.append("")
            
            if "methodologist" not in result['agents_called'] and "methodologist" in scenario.expected_agents:
                lines.append("2. Por que o Orquestrador não chamou o Metodologista?")
                lines.append("   - Focal argument tinha informação suficiente?")
                lines.append("   - Há alguma regra bloqueando transição?")
                lines.append("")
            
            # Questões sobre focal_argument
            # Verificar campos aninhados no expected_final_state
            for key, expected_val in scenario.expected_final_state.items():
                if key.startswith('focal_argument.'):
                    # Extrair nome do campo (ex: "focal_argument.subject" -> "subject")
                    field_name = key.split('.', 1)[1]
                    actual_focal = final_state.get('focal_argument', {})
                    actual_val = actual_focal.get(field_name) if isinstance(actual_focal, dict) else None
                    
                    # Pular se for função lambda (validador)
                    if callable(expected_val):
                        continue
                    
                    if expected_val and expected_val != actual_val:
                        lines.append(f"3. Por que focal_argument.{field_name} divergiu?")
                        lines.append(f"   - Esperado: {expected_val}")
                        lines.append(f"   - Obtido: {actual_val}")
                        lines.append(f"   - Como o reasoning do Orquestrador extraiu isso?")
                        lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _get_orchestrator_reasoning(self, session_id: str, turn: int) -> str:
        """
        Extrai reasoning do Orquestrador para um turno específico.
        
        Args:
            session_id: ID da sessão
            turn: Número do turno
            
        Returns:
            Reasoning formatado ou string vazia se não encontrado
        """
        events = self.event_bus.get_session_events(session_id)
        
        # Encontrar eventos agent_completed do orchestrator
        # Ordenar por timestamp para garantir ordem correta
        orchestrator_events = [
            e for e in events 
            if e.get('event_type') == 'agent_completed' 
            and e.get('agent_name') == 'orchestrator'
        ]
        
        # Ordenar por timestamp (mais antigo primeiro)
        orchestrator_events.sort(key=lambda e: e.get('timestamp', ''))
        
        # Pegar evento correspondente ao turno (0-indexed)
        if turn - 1 < len(orchestrator_events):
            event = orchestrator_events[turn - 1]
            # Reasoning está em metadata.reasoning
            metadata = event.get('metadata', {})
            reasoning = metadata.get('reasoning', '')
            
            # Fallback para summary se reasoning não estiver disponível
            if not reasoning:
                reasoning = event.get('summary', 'N/A')
            
            return reasoning
        
        return ""

