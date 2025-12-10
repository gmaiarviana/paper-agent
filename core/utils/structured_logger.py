from datetime import datetime
from pathlib import Path
import json
from typing import Optional, Dict, Any, List

class StructuredLogger:
    """Logger estruturado em JSON para debugging."""
    
    def __init__(self, logs_dir: str = "logs/structured"):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def _write_log(self, trace_id: str, log_entry: dict):
        """Escreve log em arquivo JSONL (append-only)."""
        log_file = self.logs_dir / f"{trace_id}.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def log_agent_start(
        self,
        trace_id: str,
        agent: str,
        node: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Registra início de execução de agente."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": trace_id,
            "agent": agent,
            "node": node,
            "event": "agent_started",
            "level": "INFO",
            "message": f"{agent} started execution",
            "metadata": metadata or {}
        }
        self._write_log(trace_id, log_entry)
    
    def log_agent_complete(
        self,
        trace_id: str,
        agent: str,
        node: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Registra conclusão de execução de agente."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": trace_id,
            "agent": agent,
            "node": node,
            "event": "agent_completed",
            "level": "INFO",
            "message": f"{agent} completed execution",
            "metadata": metadata or {}
        }
        self._write_log(trace_id, log_entry)
    
    def log_decision(
        self,
        trace_id: str,
        agent: str,
        node: str,
        decision: Dict[str, Any],
        reasoning: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Registra decisão de agente."""
        full_metadata = metadata or {}
        full_metadata.update({
            "decision": decision,
            "reasoning": reasoning
        })
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": trace_id,
            "agent": agent,
            "node": node,
            "event": "decision_made",
            "level": "INFO",
            "message": f"{agent} made decision",
            "metadata": full_metadata
        }
        self._write_log(trace_id, log_entry)
    
    def log_error(
        self,
        trace_id: str,
        agent: str,
        node: str,
        error: Exception,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Registra erro durante execução."""
        full_metadata = metadata or {}
        full_metadata.update({
            "error_type": type(error).__name__,
            "error_message": str(error)
        })
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": trace_id,
            "agent": agent,
            "node": node,
            "event": "error",
            "level": "ERROR",
            "message": f"{agent} encountered error",
            "metadata": full_metadata
        }
        self._write_log(trace_id, log_entry)
    
    def read_logs(self, trace_id: str) -> List[Dict[str, Any]]:
        """Lê todos os logs de uma sessão."""
        log_file = self.logs_dir / f"{trace_id}.jsonl"
        if not log_file.exists():
            return []
        
        logs = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                logs.append(json.loads(line))
        return logs

