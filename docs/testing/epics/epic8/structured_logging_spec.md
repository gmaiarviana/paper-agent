# Épico 8.5: Debug Workflow Expandido - Especificação Técnica

## Visão Geral

Sistema de observabilidade completo para debugging e análise de sessões multi-agente.

**Componentes:**
1. Structured Logging (logs JSON)
2. Debug Report (relatórios formatados)
3. Session Replay (reprodução passo a passo)

---

## 1. Structured Logging

### 1.1 Schema de Log

**Arquivo:** `utils/structured_logger.py`

**Schema JSON obrigatório:**
```json
{
  "timestamp": "2025-01-05T14:30:22.123Z",
  "trace_id": "session-abc123",
  "agent": "orchestrator",
  "node": "orchestrator_node",
  "event": "agent_started",
  "level": "INFO",
  "message": "Orchestrator analyzing context",
  "metadata": {
    "tokens_input": 100,
    "tokens_output": 50,
    "tokens_total": 150,
    "cost": 0.0012,
    "duration_ms": 1200,
    "custom_field": "value"
  }
}
```

**Eventos suportados:**
- `agent_started`: Agente iniciou execução
- `agent_completed`: Agente concluiu execução
- `decision_made`: Agente tomou decisão
- `tool_called`: Tool foi chamada
- `error`: Erro ocorreu

**Níveis de log:**
- `DEBUG`: Detalhes técnicos (prompts completos, estado)
- `INFO`: Eventos importantes (decisões, transições)
- `WARNING`: Situações anormais (retry, fallback)
- `ERROR`: Falhas críticas

### 1.2 Implementação do Logger

**Classe:** `StructuredLogger`
```python
from datetime import datetime
from pathlib import Path
import json
from typing import Optional, Dict, Any

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
    
    def read_logs(self, trace_id: str) -> list[dict]:
        """Lê todos os logs de uma sessão."""
        log_file = self.logs_dir / f"{trace_id}.jsonl"
        if not log_file.exists():
            return []
        
        logs = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                logs.append(json.loads(line))
        return logs
```

### 1.3 Integração com Nós do Grafo

**Exemplo de instrumentação:**
```python
# Em agents/orchestrator/nodes.py (orchestrator_node)
from utils.structured_logger import StructuredLogger

def orchestrator_node(state: MultiAgentState, config: RunnableConfig) -> MultiAgentState:
    """Nó do Orquestrador com logging estruturado."""
    
    # Extrair trace_id do config
    trace_id = config.get("configurable", {}).get("thread_id", "unknown")
    
    # Inicializar logger
    logger = StructuredLogger()
    
    # Log de início
    logger.log_agent_start(
        trace_id=trace_id,
        agent="orchestrator",
        node="orchestrator_node",
        metadata={"messages_count": len(state.get("messages", []))}
    )
    
    start_time = time.time()
    
    try:
        # ... lógica existente do nó ...
        
        # Log de decisão
        logger.log_decision(
            trace_id=trace_id,
            agent="orchestrator",
            node="orchestrator_node",
            decision={
                "next_step": result["next_step"],
                "agent_suggestion": result.get("agent_suggestion")
            },
            reasoning=result.get("orchestrator_analysis", ""),
            metadata={
                "tokens_input": response.usage_metadata.get("input_tokens"),
                "tokens_output": response.usage_metadata.get("output_tokens"),
                "cost": calculate_cost(...)
            }
        )
        
        # Log de conclusão
        duration_ms = (time.time() - start_time) * 1000
        logger.log_agent_complete(
            trace_id=trace_id,
            agent="orchestrator",
            node="orchestrator_node",
            metadata={"duration_ms": duration_ms}
        )
        
        return result
        
    except Exception as e:
        # Log de erro
        logger.log_error(
            trace_id=trace_id,
            agent="orchestrator",
            node="orchestrator_node",
            error=e
        )
        raise
```

**Nós a instrumentar:**
- `agents/orchestrator/nodes.py` → `orchestrator_node`
- `agents/structurer/nodes.py` → `structurer_node`
- `agents/methodologist/nodes.py` → `decide_collaborative`, `force_decision_collaborative`

---

## 2. Debug Report

### 2.1 Gerador de Relatórios

**Arquivo:** `utils/debug_reporter.py`
```python
from typing import List, Dict, Any

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
                icon = self.AGENT_ICONS.get(log["agent"], "🤖")
                lines.append(f"{icon} {log['agent'].title()} ({log['node']})")
                
                metadata = log.get("metadata", {})
                
                if "duration_ms" in metadata:
                    duration_s = metadata["duration_ms"] / 1000
                    lines.append(f"├─ Duration: {duration_s:.1f}s")
                
                if "cost" in metadata:
                    lines.append(f"├─ Cost: ${metadata['cost']:.4f}")
                
                if "tokens_total" in metadata:
                    tokens_in = metadata.get("tokens_input", 0)
                    tokens_out = metadata.get("tokens_output", 0)
                    tokens_total = metadata["tokens_total"]
                    lines.append(f"├─ Tokens: {tokens_total} ({tokens_in} in, {tokens_out} out)")
                
                if log["event"] == "decision_made":
                    lines.append("└─ Decision:")
                    decision = metadata.get("decision", {})
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
        
        total_cost = sum(log.get("metadata", {}).get("cost", 0) for log in logs)
        total_duration = sum(log.get("metadata", {}).get("duration_ms", 0) for log in logs)
        total_tokens = sum(log.get("metadata", {}).get("tokens_total", 0) for log in logs)
        
        lines.append(f"Duration: {total_duration / 1000:.1f}s")
        lines.append(f"Cost: ${total_cost:.4f}")
        lines.append(f"Tokens: {total_tokens}")
        
        agents_used = list(set(log["agent"] for log in logs))
        lines.append(f"Agents: {', '.join(agents_used)}")
        
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
            timestamp = log["timestamp"]
            
            # Se diferença > 5s, considera novo turno
            if last_timestamp:
                from datetime import datetime
                dt_last = datetime.fromisoformat(last_timestamp.replace("Z", "+00:00"))
                dt_current = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                diff_seconds = (dt_current - dt_last).total_seconds()
                
                if diff_seconds > 5:
                    turns.append(current_turn)
                    current_turn = []
            
            current_turn.append(log)
            last_timestamp = timestamp
        
        if current_turn:
            turns.append(current_turn)
        
        return turns
```

### 2.2 Aprimoramento de debug_scenario.py

**Modificar:** `scripts/testing/debug_scenario.py`

**Adicionar:**
- Integração com `StructuredLogger`
- Opção `--level` (basic, full, trace)
- Gerar debug report via `DebugReporter`
- Salvar report em `logs/debug/{scenario_id}_report.txt`

---

## 3. Session Replay

### 3.1 Script de Replay

**Arquivo:** `scripts/testing/replay_session.py`
```python
#!/usr/bin/env python3
"""
Script para reproduzir sessão passo a passo.

Uso:
    python scripts/testing/replay_session.py session-abc123
    python scripts/testing/replay_session.py session-abc123 --speed fast
    python scripts/testing/replay_session.py session-abc123 --turn 3
    python scripts/testing/replay_session.py session-abc123 --export report.md
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.structured_logger import StructuredLogger
from utils.debug_reporter import DebugReporter

def replay_session(trace_id: str, speed: str = "normal", start_turn: int = 1, export: str = None):
    """Reproduz sessão passo a passo."""
    
    # Ler logs
    logger = StructuredLogger()
    logs = logger.read_logs(trace_id)
    
    if not logs:
        print(f"❌ Nenhum log encontrado para trace_id: {trace_id}")
        return
    
    # Agrupar por turno
    reporter = DebugReporter()
    turns = reporter._group_by_turn(logs)
    
    print("=" * 60)
    print(f"SESSION REPLAY: {trace_id}")
    print("=" * 60)
    print(f"Total turns: {len(turns)}")
    print("")
    
    # Replay
    for turn_num, turn_logs in enumerate(turns, 1):
        if turn_num < start_turn:
            continue
        
        print(f"[TURN {turn_num}]")
        print("")
        
        for log in turn_logs:
            icon = reporter.AGENT_ICONS.get(log["agent"], "🤖")
            event = log["event"]
            message = log["message"]
            
            print(f"{icon} {log['agent'].title()}: {message}")
            
            if event == "decision_made":
                metadata = log.get("metadata", {})
                decision = metadata.get("decision", {})
                reasoning = metadata.get("reasoning", "")
                
                print(f"├─ Decision: {decision}")
                if reasoning:
                    print(f"└─ Reasoning: {reasoning[:100]}...")
            
            print("")
        
        print("-" * 60)
        
        if speed == "normal":
            user_input = input("\n[Pressione Enter para próximo turno ou 'q' para sair] ")
            if user_input.lower() == 'q':
                break
        
        print("")
    
    print("=" * 60)
    print("Replay completo!")
    print("=" * 60)
    
    # Exportar se solicitado
    if export:
        report = reporter.generate_debug_report(trace_id, logs)
        export_path = Path(export)
        export_path.write_text(report, encoding="utf-8")
        print(f"\n✅ Report exportado: {export}")

def main():
    parser = argparse.ArgumentParser(description="Reproduz sessão passo a passo")
    parser.add_argument("trace_id", help="ID da sessão (trace_id)")
    parser.add_argument("--speed", choices=["normal", "fast"], default="normal",
                       help="Velocidade do replay (normal=pausa, fast=sem pausa)")
    parser.add_argument("--turn", type=int, default=1,
                       help="Começar a partir do turno N")
    parser.add_argument("--export", help="Exportar replay como markdown (caminho do arquivo)")
    
    args = parser.parse_args()
    replay_session(args.trace_id, args.speed, args.turn, args.export)

if __name__ == "__main__":
    main()
```

---

## 4. Ordem de Implementação

### Task 8.5.1: StructuredLogger
- Criar `utils/structured_logger.py`
- Implementar classe `StructuredLogger`
- Testes unitários básicos

### Task 8.5.2: Instrumentar Grafo
- Adicionar logging em `orchestrator_node`
- Adicionar logging em `structurer_node`
- Adicionar logging em `decide_collaborative`
- Adicionar logging em `force_decision_collaborative`

### Task 8.5.3: DebugReporter
- Criar `utils/debug_reporter.py`
- Implementar classe `DebugReporter`
- Método `generate_debug_report()`

### Task 8.5.4: Aprimorar debug_scenario.py
- Integrar com `StructuredLogger`
- Adicionar `--level` (basic, full, trace)
- Gerar debug report via `DebugReporter`

### Task 8.5.5: Session Replay
- Criar `scripts/testing/replay_session.py`
- Implementar replay passo a passo
- Opções: `--speed`, `--turn`, `--export`

---

## 5. Comandos de Validação

### Task 8.5.1:
```powershell
# Teste unitário do logger
python -c "from utils.structured_logger import StructuredLogger; logger = StructuredLogger(); logger.log_agent_start('test-123', 'orchestrator', 'orchestrator_node', {'test': 'value'}); print('✅ Logger criado'); logs = logger.read_logs('test-123'); print(f'✅ {len(logs)} logs lidos')"

# Verificar arquivo criado
Get-Content logs/structured/test-123.jsonl
```

### Task 8.5.2:
```powershell
# Rodar cenário e verificar logs
python scripts/testing/execute_scenario.py --scenario 2

# Verificar logs estruturados gerados
Get-ChildItem logs/structured/*.jsonl | Select-Object -First 5
```

### Task 8.5.3:
```powershell
# Teste do reporter
python -c "from utils.structured_logger import StructuredLogger; from utils.debug_reporter import DebugReporter; logger = StructuredLogger(); logs = logger.read_logs('test-123'); reporter = DebugReporter(); report = reporter.generate_debug_report('test-123', logs); print(report)"
```

### Task 8.5.4:
```powershell
# Rodar debug com nível completo
python scripts/testing/debug_scenario.py --scenario 2 --level full

# Verificar report gerado
Get-Content logs/debug/cenario_02_*_report.txt
```

### Task 8.5.5:
```powershell
# Replay de sessão
python scripts/testing/replay_session.py test-123 --speed fast

# Replay com export
python scripts/testing/replay_session.py test-123 --export replay_report.md
```

