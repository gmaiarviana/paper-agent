#!/usr/bin/env python3
"""
Script para executar cenários de validação automaticamente.

Este script executa cenários programaticamente (sem Streamlit), coleta logs
e gera relatório formatado em markdown.

Uso:
    python scripts/testing/execute_scenario.py --scenario 1
"""

import argparse
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Adicionar diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph
from agents.orchestrator.state import create_initial_multi_agent_state
from core.utils.event_bus.singleton import get_event_bus
from langchain_core.messages import AIMessage, HumanMessage

# Mapeamento de cenários (baseado em docs/testing/epic7_validation_strategy.md)
SCENARIOS = {
    1: {
        "name": "Usuário Começa Vago",
        "input": "Observei que LLMs aumentam produtividade",
        "expected_behavior": [
            "Orquestrador classifica como vago (next_step: 'explore')",
            "Sistema pergunta contexto (não estrutura automaticamente)",
            "Estruturador é chamado automaticamente quando contexto suficiente",
            "focal_argument é atualizado (intent, subject, population, metrics)"
        ]
    },
    2: {
        "name": "Usuário Fornece Hipótese Completa",
        "input": "Claude Code reduz tempo de sprint em 30% em equipes de 2-5 devs",
        "expected_behavior": [
            "Orquestrador reconhece contexto completo (next_step: 'suggest_agent')",
            "Sistema chama Metodologista diretamente (não pede mais contexto)",
            "Metodologista valida hipótese (approved/needs_refinement/rejected)",
            "Sistema apresenta feedback de forma fluida"
        ]
    },
    3: {
        "name": "Metodologista Sugere Refinamento",
        "input": "Método X melhora desenvolvimento",
        "expected_behavior": [
            "Orquestrador chama Estruturador (V1)",
            "Estruturador cria V1 com claim",
            "Orquestrador chama Metodologista",
            "Metodologista retorna 'needs_refinement' com gaps específicos",
            "Sistema apresenta feedback ao usuário (não refina automaticamente)"
        ]
    },
    4: {
        "name": "Provocação Socrática - Métrica Vaga",
        "input": "Quero medir produtividade de desenvolvedores",
        "expected_behavior": [
            "Orquestrador detecta métrica vaga",
            "Sistema gera reflection_prompt provocando sobre COMO medir",
            "Provocação expõe assumptions (não coleta burocrática)",
            "Mensagem é socrática (contra-pergunta, não coleta)"
        ]
    },
    5: {
        "name": "Mudança de Direção",
        "inputs": [
            "Quero testar hipótese sobre LLMs",
            "Na verdade, quero fazer revisão de literatura"
        ],
        "expected_behavior": [
            "Sistema aceita mudança sem questionar",
            "focal_argument é resetado (intent muda de 'test_hypothesis' para 'review_literature')",
            "Sistema adapta fluxo imediatamente",
            "Contexto anterior não prende usuário"
        ]
    },
    6: {
        "name": "Reasoning Loop do Metodologista",
        "input": "Hipótese vaga que requer clarificação: Método X melhora desenvolvimento de software",
        "expected_behavior": [
            "Metodologista entra em modo analyze",
            "Detecta que precisa clarificação (needs_clarification: True)",
            "Router envia para ask_clarification",
            "Tool ask_user é chamada (faz pergunta ao usuário)",
            "Loop funciona (analyze → ask → analyze)",
            "Sistema não fica em loop infinito (respeita limite)"
        ]
    },
    7: {
        "name": "Preservação de Contexto em Conversa Longa",
        "inputs": [
            "Observei que LLMs aumentam produtividade",
            "Especificamente em equipes pequenas de 2-5 desenvolvedores",
            "Quero medir tempo de sprint",
            "Comparando com desenvolvimento tradicional",
            "Focando em qualidade do código também"
        ],
        "expected_behavior": [
            "focal_argument evolui a cada turno",
            "messages preserva histórico completo",
            "Contexto não se perde (agentes têm acesso ao histórico)",
            "Sistema referencia informações de turnos anteriores"
        ]
    },
    8: {
        "name": "Transição Fluida (Sem 'Posso Chamar X?')",
        "input": "LLMs reduzem tempo de sprint em equipes de 2-5 desenvolvedores",
        "expected_behavior": [
            "Orquestrador reconhece contexto completo (next_step: 'suggest_agent')",
            "Sistema chama Metodologista diretamente (não pede mais contexto)",
            "Sistema NÃO pergunta: 'Posso chamar o Metodologista?'",
            "Sistema anuncia ação automaticamente",
            "Transição é automática",
            "Bastidores mostram qual agente está trabalhando"
        ]
    },
    9: {
        "name": "Validação Científica com Critérios",
        "input": "Método X melhora desenvolvimento de software em equipes pequenas",
        "expected_behavior": [
            "Metodologista valida usando 4 critérios (testabilidade, falseabilidade, especificidade, operacionalização)",
            "Retorna 'needs_refinement' com gaps específicos",
            "Justificativa cita critérios aplicados",
            "Sugestões são concretas (não genéricas)"
        ]
    },
    10: {
        "name": "Bastidores Mostra Reasoning",
        "input": "Observei que LLMs aumentam produtividade",
        "expected_behavior": [
            "Painel 'Bastidores' mostra qual agente está trabalhando",
            "Reasoning do agente é exibido (card de pensamento)",
            "Eventos aparecem em timeline",
            "Métricas são exibidas (tokens, custo, duração)"
        ]
    }
}

def extract_final_message(result: Dict[str, Any]) -> str:
    """
    Extrai mensagem final do sistema do resultado.
    
    Args:
        result: Estado final do grafo
        
    Returns:
        str: Mensagem final ou fallback
    """
    messages = result.get("messages", [])
    if messages:
        # Pegar última mensagem (AIMessage)
        last_message = messages[-1]
        if hasattr(last_message, 'content'):
            return last_message.content
        elif isinstance(last_message, dict):
            return last_message.get('content', str(last_message))
        else:
            return str(last_message)
    
    # Fallback: tentar orchestrator_analysis
    analysis = result.get("orchestrator_analysis")
    if analysis:
        return f"[Análise do Orquestrador]\n{analysis}"
    
    return "[Nenhuma mensagem encontrada no resultado]"

def list_agents_called(events: List[Dict[str, Any]]) -> List[str]:
    """
    Lista agentes que foram chamados baseado nos eventos.
    
    Args:
        events: Lista de eventos do EventBus
        
    Returns:
        List[str]: Lista de nomes de agentes chamados
    """
    agents = set()
    for event in events:
        if event.get("event_type") == "agent_started":
            agent_name = event.get("agent_name")
            if agent_name:
                agents.add(agent_name)
    
    return sorted(list(agents))

def detect_issues(execution: Dict[str, Any]) -> List[str]:
    """
    Detecta problemas óbvios na execução.
    
    Args:
        execution: Dicionário com resultado da execução
        
    Returns:
        List[str]: Lista de problemas detectados
    """
    issues = []
    result = execution.get("result", {})
    events = execution.get("events", [])
    
    # Verificar se houve exceção
    if execution.get("error"):
        issues.append(f"❌ **ERRO CRÍTICO**: {execution['error']}")
    
    # Verificar se algum agente foi chamado
    agents_called = list_agents_called(events)
    if not agents_called:
        issues.append("⚠️ **AVISO**: Nenhum agente foi chamado (apenas Orquestrador?)")
    
    # Verificar se next_step está definido
    next_step = result.get("next_step")
    if not next_step:
        issues.append("⚠️ **AVISO**: next_step não foi definido pelo Orquestrador")
    
    # Verificar se há mensagens
    messages = result.get("messages", [])
    if not messages:
        issues.append("⚠️ **AVISO**: Nenhuma mensagem foi gerada")
    elif len(messages) < 2:  # Deve ter pelo menos HumanMessage inicial + AIMessage
        issues.append("⚠️ **AVISO**: Poucas mensagens no histórico (esperado: 2+)")
    
    # Verificar se focal_argument foi atualizado (para cenários que esperam isso)
    focal_argument = result.get("focal_argument")
    if not focal_argument:
        issues.append("ℹ️ **INFO**: focal_argument não foi atualizado (pode ser esperado para alguns cenários)")
    
    # Verificar se há eventos de erro
    error_events = [e for e in events if e.get("event_type") == "agent_error"]
    if error_events:
        for error_event in error_events:
            issues.append(f"❌ **ERRO**: {error_event.get('agent_name', 'unknown')} - {error_event.get('error_message', 'unknown error')}")
    
    if not issues:
        issues.append("✅ Nenhum problema óbvio detectado automaticamente")
    
    return issues

def format_checklist(items: List[str]) -> str:
    """
    Formata lista de itens como checklist markdown.
    
    Args:
        items: Lista de itens
        
    Returns:
        str: Checklist formatado
    """
    return "\n".join([f"- [ ] {item}" for item in items])

def format_report(execution: Dict[str, Any]) -> str:
    """
    Formata resultados em markdown legível.
    
    Args:
        execution: Dicionário com resultado da execução
        
    Returns:
        str: Relatório formatado em markdown
    """
    scenario = execution["scenario"]
    result = execution.get("result", {})
    events = execution.get("events", [])
    session_id = execution.get("session_id", "unknown")
    
    # Extrair informações
    final_message = extract_final_message(result)
    agents_called = list_agents_called(events)
    issues = detect_issues(execution)
    
    # Formatar focal_argument
    focal_argument = result.get("focal_argument")
    focal_str = "N/A"
    if focal_argument:
        focal_str = json.dumps(focal_argument, indent=2, ensure_ascii=False)
    
    # Formatar next_step
    next_step = result.get("next_step", "N/A")
    
    # Formatar orchestrator_analysis (truncado)
    analysis = result.get("orchestrator_analysis", "N/A")
    if analysis and len(analysis) > 500:
        analysis = analysis[:500] + "... [truncado]"
    
    # Calcular métricas totais
    total_tokens = 0
    total_cost = 0.0
    total_duration = 0.0
    for event in events:
        if event.get("event_type") == "agent_completed":
            total_tokens += event.get("tokens_total", 0)
            total_cost += event.get("cost", 0.0)
            total_duration += event.get("duration", 0.0)
    
    # Formatar eventos (resumo)
    events_summary = []
    for event in events:
        event_type = event.get("event_type", "unknown")
        agent_name = event.get("agent_name", "unknown")
        timestamp = event.get("timestamp", "unknown")
        events_summary.append(f"- `{event_type}`: {agent_name} @ {timestamp}")
    
    report = f"""# Cenário {execution.get('scenario_num', '?')}: {scenario['name']}

## 📥 Input Fornecido

```
{scenario.get('input', scenario.get('inputs', ['N/A'])[0] if scenario.get('inputs') else 'N/A')}
```

## 📤 Output do Sistema

```
{final_message}
```

## 📊 Agentes Acionados

{', '.join(agents_called) if agents_called else 'Nenhum agente foi chamado (apenas Orquestrador?)'}

## 🔍 Estado Final

### next_step
```
{next_step}
```

### focal_argument
```json
{focal_str}
```

### orchestrator_analysis (truncado)
```
{analysis}
```

## 📈 Métricas Consolidadas

- **Total de tokens**: {total_tokens:,}
- **Custo total**: ${total_cost:.4f}
- **Duração total**: {total_duration:.2f}s
- **Total de eventos**: {len(events)}

## 📋 Eventos do EventBus

{chr(10).join(events_summary[:20]) if events_summary else 'Nenhum evento encontrado'}
{f'... e mais {len(events_summary) - 20} eventos' if len(events_summary) > 20 else ''}

## ⚠️ Problemas Detectados Automaticamente

{chr(10).join(issues)}

## ✅ Comportamento Esperado (Checklist)

{format_checklist(scenario.get('expected_behavior', []))}

## 📝 Metadados

- **Session ID**: `{session_id}`
- **Timestamp da execução**: {execution.get('timestamp', datetime.now().isoformat())}
- **Duração da execução**: {execution.get('execution_duration', 0):.2f}s

---

**Nota**: Este relatório foi gerado automaticamente. Revise manualmente para análise completa.
"""
    
    return report

def execute_scenario(scenario_num: int) -> Dict[str, Any]:
    """
    Executa cenário e retorna resultados.
    
    Args:
        scenario_num: Número do cenário (1-10)
        
    Returns:
        dict: Resultados da execução
    """
    if scenario_num not in SCENARIOS:
        raise ValueError(f"Cenário {scenario_num} não encontrado. Cenários disponíveis: {list(SCENARIOS.keys())}")
    
    scenario = SCENARIOS[scenario_num]
    session_id = f"test-scenario-{scenario_num}-{int(time.time())}"
    
    print(f"🚀 Executando Cenário {scenario_num}: {scenario['name']}")
    print(f"   Session ID: {session_id}")
    print()
    
    start_time = time.time()
    error = None
    result = None
    
    try:
        # Criar grafo
        print("📋 Criando grafo multi-agente...")
        graph = create_multi_agent_graph()
        
        # Determinar input(s)
        if "inputs" in scenario:
            # Cenários com múltiplos inputs (ex: cenário 5, 7)
            inputs = scenario["inputs"]
            print(f"📋 Cenário tem {len(inputs)} inputs. Executando sequencialmente...")
            
            # Executar primeiro input
            first_input = inputs[0]
            state = create_initial_multi_agent_state(
                first_input,
                session_id=session_id
            )
            
            config = {
                "configurable": {
                    "thread_id": session_id
                }
            }
            
            result = graph.invoke(state, config=config)
            
            # Executar inputs subsequentes (usando mesmo thread_id para preservar contexto)
            for i, next_input in enumerate(inputs[1:], start=2):
                print(f"📋 Executando input {i}/{len(inputs)}...")
                next_state = create_initial_multi_agent_state(
                    next_input,
                    session_id=session_id
                )
                # Preservar contexto: adicionar mensagens anteriores
                if result and "messages" in result:
                    next_state["messages"] = result["messages"] + [HumanMessage(content=next_input)]
                
                result = graph.invoke(next_state, config=config)
        else:
            # Cenário com input único
            user_input = scenario["input"]
            print(f"📋 Input: {user_input[:80]}...")
            
            # Criar estado inicial
            state = create_initial_multi_agent_state(
                user_input,
                session_id=session_id
            )
            
            # Configuração com thread_id
            config = {
                "configurable": {
                    "thread_id": session_id
                }
            }
            
            # Executar grafo
            print("📋 Executando grafo...")
            result = graph.invoke(state, config=config)
        
        print("✅ Execução concluída com sucesso!")
        
    except Exception as e:
        error = str(e)
        print(f"❌ Erro durante execução: {e}")
        traceback.print_exc()
        result = {}
    
    execution_duration = time.time() - start_time
    
    # Coletar eventos do EventBus
    print("📋 Coletando eventos do EventBus...")
    try:
        event_bus = get_event_bus()
        events = event_bus.get_session_events(session_id)
        print(f"✅ {len(events)} eventos coletados")
    except Exception as e:
        print(f"⚠️  Erro ao coletar eventos: {e}")
        events = []
    
    return {
        "scenario": scenario,
        "scenario_num": scenario_num,
        "result": result,
        "events": events,
        "session_id": session_id,
        "error": error,
        "execution_duration": execution_duration,
        "timestamp": datetime.now().isoformat()
    }

def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Executar cenário de validação automaticamente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplo de uso:
  python scripts/testing/execute_scenario.py --scenario 1
        """
    )
    
    parser.add_argument(
        "--scenario",
        type=int,
        required=True,
        choices=list(SCENARIOS.keys()),
        help="Número do cenário (1-10)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Diretório de saída (padrão: docs/testing/epic7_results/cenario_XX_*/)"
    )
    
    args = parser.parse_args()
    
    # Executar cenário
    print("=" * 70)
    print("EXECUÇÃO AUTOMATIZADA DE CENÁRIO - ÉPICO 7.2")
    print("=" * 70)
    print()
    
    execution = execute_scenario(args.scenario)
    
    # Gerar relatório
    print()
    print("📋 Gerando relatório...")
    report = format_report(execution)
    
    # Determinar diretório de saída
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        # Tentar encontrar diretório do cenário
        scenario_name = SCENARIOS[args.scenario]["name"].lower().replace(" ", "_")
        scenario_name = scenario_name.replace("(", "").replace(")", "").replace("'", "")
        scenario_dir_pattern = f"cenario_{args.scenario:02d}_*"
        
        results_dir = project_root / "docs" / "testing" / "epic7_results"
        matching_dirs = list(results_dir.glob(scenario_dir_pattern))
        
        if matching_dirs:
            output_dir = matching_dirs[0]
        else:
            # Criar diretório padrão
            output_dir = results_dir / f"cenario_{args.scenario:02d}_{scenario_name}"
            output_dir.mkdir(parents=True, exist_ok=True)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "execution_report.md"
    
    # Salvar relatório
    try:
        output_file.write_text(report, encoding="utf-8")
        print(f"✅ Relatório salvo em: {output_file}")
    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {e}")
        print("📋 Imprimindo relatório no console...")
        print()
    
    # Imprimir para console
    print()
    print("=" * 70)
    print("RELATÓRIO GERADO")
    print("=" * 70)
    print()
    print(report)
    print()
    print("=" * 70)
    print(f"✅ Relatório salvo em: {output_file}")
    print("📋 Copie o relatório acima e cole para análise")
    print("=" * 70)

if __name__ == "__main__":
    main()

