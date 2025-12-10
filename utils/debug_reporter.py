from typing import List, Dict, Any
from datetime import datetime

class DebugReporter:
    """Gera relatórios de debug formatados."""
    
    AGENT_ICONS = {
        "orchestrator": "🎯",
        "structurer": "📝",
        "methodologist": "🔬"
    }
    
    STATUS_ICONS = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    def generate_debug_report(
        self,
        scenario_id: str,
        logs: List[Dict[str, Any]]
    ) -> str:
        """Gera relatório de debug formatado."""
        
        # Tratamento de logs vazios
        if not logs:
            lines = []
            lines.append("=" * 60)
            lines.append(f"DEBUG REPORT: {scenario_id}")
            lines.append("=" * 60)
            lines.append("")
            lines.append("No logs found for this scenario.")
            lines.append("=" * 60)
            return "\n".join(lines)
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"DEBUG REPORT: {scenario_id}")
        lines.append("=" * 60)
        lines.append("")
        
        # Agrupar logs por turno (aproximação por timestamp)
        turns = self._group_by_turn(logs)
        
        for turn_num, turn_logs in enumerate(turns, 1):
            lines.append(f"[TURN {turn_num}]")
            lines.append("")
            
            for log in turn_logs:
                # Tratamento de campos ausentes
                agent = log.get("agent", "unknown")
                node = log.get("node", "unknown_node")
                icon = self.AGENT_ICONS.get(agent, "🤖")
                lines.append(f"{icon} {agent.title()} ({node})")
                
                metadata = log.get("metadata", {})
                
                # Duration
                if "duration_ms" in metadata:
                    try:
                        duration_s = metadata["duration_ms"] / 1000
                        lines.append(f"├─ Duration: {duration_s:.1f}s")
                    except (TypeError, ValueError):
                        pass
                
                # Cost
                if "cost" in metadata:
                    try:
                        cost = float(metadata["cost"])
                        lines.append(f"├─ Cost: ${cost:.4f}")
                    except (TypeError, ValueError):
                        pass
                
                # Tokens
                if "tokens_total" in metadata:
                    try:
                        tokens_in = metadata.get("tokens_input", 0)
                        tokens_out = metadata.get("tokens_output", 0)
                        tokens_total = metadata["tokens_total"]
                        lines.append(f"├─ Tokens: {tokens_total} ({tokens_in} in, {tokens_out} out)")
                    except (TypeError, ValueError):
                        pass
                
                # Decision (se evento for decision_made)
                event = log.get("event", "")
                if event == "decision_made":
                    lines.append("└─ Decision:")
                    decision = metadata.get("decision", {})
                    if isinstance(decision, dict):
                        for key, value in decision.items():
                            lines.append(f"   {key}: {value}")
                    reasoning = metadata.get("reasoning", "")
                    if reasoning:
                        lines.append(f"   reasoning: {reasoning[:100]}...")
                
                lines.append("")
            
            lines.append("-" * 60)
            lines.append("")
        
        # Sumário final
        lines.append("=" * 60)
        lines.append("TOTAL")
        lines.append("=" * 60)
        
        # Calcular totais com tratamento de erros
        total_cost = 0.0
        total_duration = 0.0
        total_tokens = 0
        agents_used = set()
        
        for log in logs:
            metadata = log.get("metadata", {})
            
            # Cost
            try:
                cost = metadata.get("cost", 0) or 0
                total_cost += float(cost)
            except (TypeError, ValueError):
                pass
            
            # Duration
            try:
                duration_ms = metadata.get("duration_ms", 0) or 0
                total_duration += float(duration_ms)
            except (TypeError, ValueError):
                pass
            
            # Tokens
            try:
                tokens_total = metadata.get("tokens_total", 0) or 0
                total_tokens += int(tokens_total)
            except (TypeError, ValueError):
                pass
            
            # Agents
            agent = log.get("agent")
            if agent:
                agents_used.add(agent)
        
        lines.append(f"Duration: {total_duration / 1000:.1f}s")
        lines.append(f"Cost: ${total_cost:.4f}")
        lines.append(f"Tokens: {total_tokens}")
        lines.append(f"Agents: {', '.join(sorted(agents_used))}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _group_by_turn(self, logs: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Agrupa logs por turno (aproximação por timestamp)."""
        if not logs:
            return []
        
        turns = []
        current_turn = []
        last_timestamp = None
        
        for log in logs:
            timestamp = log.get("timestamp")
            
            # Se timestamp ausente, adiciona ao turno atual
            if not timestamp:
                current_turn.append(log)
                continue
            
            # Se diferença > 5s, considera novo turno
            if last_timestamp:
                try:
                    # Parse timestamp (formato ISO com Z)
                    dt_last = datetime.fromisoformat(last_timestamp.replace("Z", "+00:00"))
                    dt_current = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    diff_seconds = (dt_current - dt_last).total_seconds()
                    
                    if diff_seconds > 5:
                        turns.append(current_turn)
                        current_turn = []
                except (ValueError, AttributeError):
                    # Se parsing falhar, continua no turno atual
                    pass
            
            current_turn.append(log)
            last_timestamp = timestamp
        
        if current_turn:
            turns.append(current_turn)
        
        return turns

