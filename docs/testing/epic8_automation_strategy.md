# ÉPICO 8: Análise Assistida de Qualidade - Ferramentas para Discussão

> **Objetivo:** Facilitar análise humana de qualidade conversacional através de ferramentas que estruturam dados para discussão eficiente com LLM.

---

## 📋 Visão Geral

**Dependência:** Épico 7 deve estar concluído

**Insight do Épico 7:**
O valor NÃO veio de automação, mas de **discussão contextualizada**:
- Investigação interativa ("me mostre os logs", "por que isso?")
- Decisões estratégicas debatidas (baseline opcional?)
- Planejamento adaptativo (pivotamos de manual → automatizado)
- **Humano + Claude analisando JUNTOS**

**Problema:**
- Validação manual (Épico 7) foi eficaz mas trabalhosa
- Precisamos reduzir tempo de setup
- MAS: Automação completa perde contexto e qualidade

**Solução:**
- Ferramentas que **estruturam dados** para análise
- Output formatado para **fácil discussão** com LLM
- Humano + Claude fazem análise (não script)
- **Mantém qualidade, reduz trabalho manual**

**Resultado Esperado:**
- Rodar cenário completo: 1 comando
- Gerar relatório estruturado: automático
- Colar no Claude e discutir: 30 segundos
- Identificar causa raiz: minutos (não horas)
- **Replicável:** Próxima vez é mais rápido

---

## 📚 Aprendizados do Épico 7 que Moldaram este Épico

### 1. Multi-Turn É Crítico, Não Opcional

**Problema identificado:**
- Cenários 3 e 6 (Épico 7) não foram validados completamente
- Script single-turn só testa primeiro turno
- Fluxos Orchestrator → Structurer → Methodologist não foram exercitados

**Impacto no Épico 8:**
- Multi-turn executor deve ser funcionalidade PRIORITÁRIA
- LLM-as-Judge sozinho não resolve (precisa de conversas completas)
- Framework deve suportar validação de fluxos end-to-end

### 2. Debug de Logs Foi Crítico para Troubleshooting

**Problema identificado:**
- Sem logs detalhados (`debug_scenario_2.py`), não achamos causa raiz
- Reasoning completo do LLM revelou decisões sutis
- Prompt bloqueava comportamento ("Turno 1: sempre explore")

**Impacto no Épico 8:**
- Debug mode deve estar embutido no framework
- Comparação antes/depois de mudanças no prompt
- Logs devem ser salvos automaticamente

### 3. Problemas São Sutis e Difíceis de Detectar

**Problema identificado:**
- "Observei que..." vs claim direto muda intent
- "Posso chamar X?" vs "Vou validar X" muda fluidez
- Baseline opcional vs obrigatório afeta transições

**Impacto no Épico 8:**
- LLM-as-Judge deve avaliar NUANCES (não só pass/fail)
- Critérios devem cobrir antipadrões específicos
- Validação de qualidade conversacional (não apenas estrutura)

### 4. Regressão Pode Acontecer Facilmente

**Problema identificado:**
- Corrigir Turno 1 poderia quebrar outros cenários
- Mudanças no prompt têm efeitos colaterais
- Precisamos baseline para comparar

**Impacto no Épico 8:**
- Regression detector (comparar antes/depois)
- Alertas de regressão (score cai, custo aumenta)
- Baseline de qualidade preservado

### 5. CI/CD É Prematuro Nesta Fase

**Decisão:**
- Não temos repositório público nem múltiplos desenvolvedores
- Não temos deploy contínuo
- Framework local é suficiente por enquanto

**Impacto no Épico 8:**
- CI/CD removido do escopo (postergar para Épico 10+)
- Foco em execução local e validação manual assistida

---

## 🎯 Filosofia: Assistir, Não Substituir

### O Que NÃO Fazer ❌

**Automação prematura:**
```python
# Script roda testes
score = llm_judge.evaluate(result)  # "4/5 - Boa fluidez"
print(f"Score: {score}")  # E daí? O que fazer com isso?
```

**Problema:** Você perde contexto, nuances, capacidade de adaptação.

### O Que Fazer ✅

**Análise assistida:**
```bash
# 1. Rodar cenário
python scripts/testing/run_scenario.py --scenario 2

# 2. Output estruturado
========================================
CENÁRIO 2: Análise Necessária
========================================
Input: "Claude Code reduz tempo..."
Esperado: suggest_agent
Observado: explore ❌

Logs:
  orchestrator_analysis: "Turno 1, sempre explore..."
  next_step: explore (PROBLEMA)

Pergunta sugerida:
Por que sistema não reconheceu contexto suficiente?
========================================

# 3. Você copia e cola no Claude
# 4. Claude analisa e sugere causa raiz
# 5. Você decide próximos passos
```

**Benefício:** Mantém qualidade da análise + reduz setup manual.

---

## 🎯 O Que Automatizar

**Princípio:** Automatizar validação de **problemas reais identificados no Épico 7** através de conversas completas end-to-end.

**Prioridade 1: Multi-Turn Validation** 🔴
- Cenários 3 e 6 requerem múltiplos turnos (não foram completamente validados)
- Fluxos Orchestrator → Agent → Orchestrator (curadoria)
- Preservação de contexto ao longo de 3-5 turnos
- Transições automáticas (sem pedir permissão)

**Prioridade 2: LLM-as-Judge para Qualidade** 🔴
- Fluidez conversacional (não pede permissão)
- Comportamento socrático (provocação genuína)
- Curadoria (não dump técnico)
- Decisões coerentes (critérios explícitos)

**Prioridade 3: Debug & Regression** 🟡
- Debug mode (logs detalhados para troubleshooting)
- Regression detector (detectar quebras após mudanças)
- Comparação antes/depois de alterações no prompt

**NÃO automatizar neste épico:**
- ❌ CI/CD (prematuro - postergar para Épico 10+)
- ❌ Problemas hipotéticos não encontrados no Épico 7
- ❌ Validação de estrutura (testes unitários já fazem isso)
- ❌ Testes determinísticos (usar testes de integração normais)

---

## 🔄 Multi-Turn Executor (PRIORIDADE #1)

### Objetivo
Executar conversas completas end-to-end para validar fluxos multi-agente que não foram testados no Épico 7.

### Motivação (Épico 7)
- **Cenário 3:** User vago → Orchestrator → Structurer → Methodologist → needs_refinement
- **Cenário 6:** User vago → Methodologist → pede clarificação → User responde → Methodologist valida
- **Cenário 7:** 5 turnos com evolução de focal_argument

Script single-turn só validou primeiro turno. Fluxos completos não foram exercitados.

### Componentes

#### 1. `ConversationScenario` (Data Class)

**Localização:** `utils/test_scenarios.py`

```python
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class ConversationScenario:
    """Define cenário de conversa multi-turn."""
    
    id: str
    description: str
    turns: List[Tuple[str, str]]  # [("user", "input"), ("system", "expected_action"), ...]
    expected_agents: List[str]    # Agentes que devem ser chamados
    expected_final_state: dict    # Estado esperado ao final
    
    @classmethod
    def from_epic7_scenario(cls, scenario_number: int) -> "ConversationScenario":
        """Cria cenário baseado em cenários do Épico 7."""
        scenarios = {
            3: cls(
                id="cenario_03_refinamento",
                description="Ideia vaga evolui para Structurer → Methodologist → needs_refinement",
                turns=[
                    ("user", "Método X melhora desenvolvimento"),
                    ("system", "explore"),  # Orchestrator pergunta sobre métrica
                    ("user", "Melhora velocidade de entrega"),
                    ("system", "suggest_agent"),  # Chama Structurer
                    ("structurer", "structured_question"),
                    ("system", "suggest_agent"),  # Chama Methodologist
                    ("methodologist", "needs_refinement"),
                    ("system", "curadoria")  # Apresenta feedback
                ],
                expected_agents=["orchestrator", "structurer", "methodologist"],
                expected_final_state={
                    "next_step": "explore",
                    "methodologist_output": {"status": "needs_refinement"}
                }
            ),
            # ... outros cenários
        }
        return scenarios[scenario_number]
```

#### 2. `MultiTurnExecutor` (Executor)

**Localização:** `utils/test_executor.py`

```python
from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage

class MultiTurnExecutor:
    """Executa cenários com múltiplos turnos."""
    
    def __init__(self, graph):
        self.graph = graph
        self.conversation_history = []
    
    def execute_scenario(self, scenario: ConversationScenario) -> Dict:
        """
        Executa cenário completo turn-by-turn.
        
        Returns:
            {
                "turns": [resultado de cada turno],
                "final_state": estado final,
                "agents_called": lista de agentes acionados,
                "metrics": {tokens, custo, duração},
                "success": bool
            }
        """
        state = create_initial_multi_agent_state(
            scenario.turns[0][1],  # Primeiro input do usuário
            session_id=f"test-{scenario.id}"
        )
        
        results = []
        agents_called = []
        
        for turn_type, content in scenario.turns:
            if turn_type == "user":
                # Adicionar input do usuário ao estado
                state["messages"].append(HumanMessage(content=content))
                
                # Executar grafo
                result = self.graph.invoke(state)
                
                # Rastrear agentes chamados
                if result.get("next_step") == "suggest_agent":
                    agent = result.get("agent_suggestion", {}).get("agent")
                    if agent:
                        agents_called.append(agent)
                
                # Salvar resultado do turno
                results.append({
                    "turn": len(results) + 1,
                    "user_input": content,
                    "system_response": result.get("messages", [])[-1].content if result.get("messages") else None,
                    "next_step": result.get("next_step"),
                    "focal_argument": result.get("focal_argument")
                })
                
                # Atualizar estado para próximo turno
                state = result
        
        return {
            "turns": results,
            "final_state": state,
            "agents_called": agents_called,
            "success": self._validate_scenario(scenario, agents_called, state)
        }
    
    def _validate_scenario(self, scenario: ConversationScenario, agents_called: List[str], final_state: Dict) -> bool:
        """Valida que cenário executou conforme esperado."""
        # Verificar que agentes esperados foram chamados
        if set(scenario.expected_agents) != set(agents_called):
            return False
        
        # Verificar estado final
        for key, expected_value in scenario.expected_final_state.items():
            if final_state.get(key) != expected_value:
                return False
        
        return True
    
    def generate_analysis_report(self, result: Dict) -> str:
        """
        Gera relatório formatado para análise humana.
        
        Output estruturado para fácil cópia e discussão com LLM:
        - Contexto do cenário
        - Comportamento esperado vs observado
        - Logs relevantes
        - Problemas detectados automaticamente
        - Perguntas sugeridas para Claude
        """
        report = []
        report.append("=" * 60)
        report.append(f"CENÁRIO: {result.get('scenario_id', 'Unknown')}")
        report.append("=" * 60)
        report.append("")
        report.append("## Contexto")
        report.append(f"Input inicial: {result.get('turns', [{}])[0].get('user_input', 'N/A')}")
        report.append(f"Agentes esperados: {', '.join(result.get('expected_agents', []))}")
        report.append(f"Agentes chamados: {', '.join(result.get('agents_called', []))}")
        report.append("")
        report.append("## Resultado")
        if result.get("success"):
            report.append("✅ Cenário executou conforme esperado")
        else:
            report.append("❌ Problemas detectados:")
            # Detectar problemas específicos
            if set(result.get('expected_agents', [])) != set(result.get('agents_called', [])):
                report.append(f"  - Agentes esperados não foram chamados")
            report.append("")
            report.append("## Logs Relevantes")
            for turn in result.get("turns", []):
                report.append(f"[Turn {turn.get('turn')}]")
                report.append(f"  Input: {turn.get('user_input')}")
                report.append(f"  next_step: {turn.get('next_step')}")
                if turn.get('focal_argument'):
                    report.append(f"  focal_argument: {turn.get('focal_argument')}")
                report.append("")
        report.append("=" * 60)
        report.append("Copie acima e pergunte ao Claude:")
        report.append('"Por que o sistema não executou conforme esperado?"')
        report.append("=" * 60)
        return "\n".join(report)
```

#### 3. Fixture `multi_turn_executor`

**Localização:** `tests/conftest.py`

```python
@pytest.fixture
def multi_turn_executor(multi_agent_graph):
    """Fixture para executor multi-turn."""
    from utils.test_executor import MultiTurnExecutor
    return MultiTurnExecutor(multi_agent_graph)
```

### Uso nos Testes

**Exemplo em `tests/integration/test_multi_turn_flows.py`:**

```python
@pytest.mark.integration
def test_cenario_3_refinement_flow(multi_turn_executor):
    """Valida fluxo completo do Cenário 3 (refinamento)."""
    from utils.test_scenarios import ConversationScenario
    
    scenario = ConversationScenario.from_epic7_scenario(3)
    result = multi_turn_executor.execute_scenario(scenario)
    
    # Validações estruturais
    assert result["success"], "Cenário não executou conforme esperado"
    assert "structurer" in result["agents_called"]
    assert "methodologist" in result["agents_called"]
    assert result["final_state"]["methodologist_output"]["status"] == "needs_refinement"

@pytest.mark.llm_judge
def test_cenario_3_quality(multi_turn_executor, llm_judge):
    """Valida qualidade conversacional do Cenário 3."""
    scenario = ConversationScenario.from_epic7_scenario(3)
    result = multi_turn_executor.execute_scenario(scenario)
    
    # Extrair mensagens ao usuário
    messages = [turn["system_response"] for turn in result["turns"] if turn["system_response"]]
    
    # Avaliar fluidez de cada mensagem
    for message in messages:
        evaluation = llm_judge.invoke(FLUENCY_PROMPT.format(message=message))
        score = extract_score(evaluation.content)
        assert score >= 4, f"Mensagem não fluida: {message[:50]}... (score: {score})"
```

### Uso via Script

```bash
python scripts/testing/run_scenario.py --scenario 3

# Output:
========================================
CENÁRIO 3: Refinamento Multi-Agente
========================================

## Contexto
Usuário: "Método X melhora desenvolvimento"
Esperado: Orchestrator → Structurer → Methodologist

## Resultado
✅ Orchestrator explorou métrica
✅ Structurer foi chamado
❌ Methodologist NÃO foi chamado (esperado)

## Logs Relevantes
[Turn 3 - após Structurer]
  next_step: explore (esperado: suggest_agent)
  orchestrator_analysis: "Aguardando mais contexto..."

## Problema Detectado
Sistema não chamou Methodologist após Structurer.
Possível causa: Critério de transição muito conservador.

## Sugestão de Análise
Copie este relatório e pergunte ao Claude:
"Por que o sistema não chamou Methodologist após 
o Structurer criar a questão estruturada?"
========================================
```

---

## 🐛 Debug Mode (PRIORIDADE #2)

### Objetivo
Facilitar troubleshooting de problemas sutis através de logs detalhados.

### Motivação (Épico 7)
- Debug script (`debug_scenario_2.py`) foi CRÍTICO para encontrar causa raiz
- Logs revelaram reasoning completo do LLM
- Mostrou onde decisão foi tomada ("Turno 1: sempre explore")

### Componentes

#### 1. `DebugExecutor`

**Localização:** `utils/test_executor.py` (adicionar ao arquivo existente)

```python
from pathlib import Path
from datetime import datetime
import json

class DebugExecutor(MultiTurnExecutor):
    """Executor com logging detalhado para troubleshooting."""
    
    def __init__(self, graph, debug_dir: str = "logs/debug"):
        super().__init__(graph)
        self.debug_dir = Path(debug_dir)
        self.debug_dir.mkdir(parents=True, exist_ok=True)
    
    def execute_with_debug(self, scenario: ConversationScenario) -> Dict:
        """
        Executa cenário com logging completo.
        
        Salva em arquivo:
        - Prompt completo enviado ao LLM
        - Resposta bruta antes de parsing
        - Reasoning do LLM
        - Decisões tomadas (next_step, agent_suggestion)
        - Estado antes/depois de cada turno
        """
        debug_log = {
            "scenario_id": scenario.id,
            "timestamp": datetime.now().isoformat(),
            "turns": []
        }
        
        # Executar com logging
        state = create_initial_multi_agent_state(
            scenario.turns[0][1],
            session_id=f"debug-{scenario.id}"
        )
        
        for turn_type, content in scenario.turns:
            if turn_type == "user":
                # Salvar estado antes
                turn_log = {
                    "turn": len(debug_log["turns"]) + 1,
                    "user_input": content,
                    "state_before": self._serialize_state(state),
                }
                
                # Executar
                state["messages"].append(HumanMessage(content=content))
                result = self.graph.invoke(state)
                
                # Salvar estado depois e reasoning
                turn_log["state_after"] = self._serialize_state(result)
                turn_log["llm_reasoning"] = result.get("orchestrator_analysis", "")
                turn_log["next_step"] = result.get("next_step")
                turn_log["agent_suggestion"] = result.get("agent_suggestion")
                
                debug_log["turns"].append(turn_log)
                state = result
        
        # Salvar log em arquivo
        log_file = self.debug_dir / f"{scenario.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(debug_log, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Debug log salvo: {log_file}")
        
        return {
            "scenario": scenario,
            "result": result,
            "log_file": str(log_file)
        }
    
    def _serialize_state(self, state: Dict) -> Dict:
        """Serializa estado para logging (remove objetos não serializáveis)."""
        return {
            "next_step": state.get("next_step"),
            "focal_argument": state.get("focal_argument"),
            "messages_count": len(state.get("messages", [])),
            "last_message": str(state.get("messages", [])[-1]) if state.get("messages") else None
        }
    
    def generate_debug_report(self, debug_result: Dict) -> str:
        """
        Gera relatório de debug formatado para análise.
        
        Inclui:
        - Prompt completo enviado ao LLM
        - Resposta bruta antes de parsing
        - Reasoning do LLM
        - Decisões tomadas step-by-step
        - Estado antes/depois de cada transição
        """
        report = []
        report.append("=" * 60)
        report.append(f"DEBUG REPORT: {debug_result['scenario'].id}")
        report.append("=" * 60)
        
        with open(debug_result["log_file"], "r", encoding="utf-8") as f:
            debug_log = json.load(f)
        
        for turn in debug_log["turns"]:
            report.append(f"\n[TURN {turn['turn']}]")
            report.append(f"Input: {turn['user_input']}")
            report.append(f"\n[LLM REASONING]")
            report.append(turn.get('llm_reasoning', 'N/A'))
            report.append(f"\n[DECISION]")
            report.append(f"next_step: {turn.get('next_step')}")
            if turn.get('agent_suggestion'):
                report.append(f"agent: {turn['agent_suggestion'].get('agent')}")
            report.append(f"\n{'-' * 60}")
        
        report.append("\n" + "=" * 60)
        report.append("Copie acima e pergunte ao Claude:")
        report.append('"Onde o reasoning levou à decisão errada?"')
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def compare_prompts(self, scenario: ConversationScenario, old_prompt: str, new_prompt: str) -> Dict:
        """
        Compara comportamento antes/depois de mudança no prompt.
        
        Returns:
            {
                "scenario_id": str,
                "changes_detected": bool,
                "before": {resultado com prompt antigo},
                "after": {resultado com prompt novo},
                "diff": {diferenças encontradas}
            }
        """
        # TODO: Implementar comparação de prompts
        # Requer salvar baseline antes de mudança
        pass
```

#### 2. Fixture `debug_executor`

**Localização:** `tests/conftest.py`

```python
@pytest.fixture
def debug_executor(multi_agent_graph):
    """Fixture para executor com debug mode."""
    from utils.test_executor import DebugExecutor
    return DebugExecutor(multi_agent_graph)
```

### Uso para Troubleshooting

```bash
# Via script
python scripts/testing/debug_scenario.py --scenario 2

# Gera debug report completo
# Mostra reasoning detalhado do LLM
# Pronto para colar no Claude e investigar
```

```python
# Em qualquer teste, adicionar --debug
pytest tests/integration/test_cenario_2.py --debug

# Ou programaticamente
def test_debug_cenario_2(debug_executor):
    """Debug do Cenário 2 (hipótese completa)."""
    from utils.test_scenarios import ConversationScenario
    
    scenario = ConversationScenario.from_epic7_scenario(2)
    result = debug_executor.execute_with_debug(scenario)
    
    # Log será salvo em logs/debug/cenario_02_*.json
    # Pode ser analisado manualmente
    
    report = debug_executor.generate_debug_report(result)
    print(report)
```

---

## 🛠️ Infraestrutura LLM-as-Judge (PRIORIDADE #3)

**Nota:** LLM-as-Judge é usado EM CONJUNTO com Multi-Turn Executor para validar qualidade conversacional após execução completa do cenário.

### 1. Fixture `llm_judge`

**Localização:** `tests/conftest.py`

**Especificação:**
```python
@pytest.fixture
def llm_judge():
    """
    Fixture para LLM-as-judge (avaliador de qualidade).
    
    Usa Claude Haiku para custo-benefício.
    Temperature=0 para determinismo.
    """
    import os
    from langchain_anthropic import ChatAnthropic
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("LLM-as-judge test skipped: ANTHROPIC_API_KEY not set")
    
    return ChatAnthropic(
        model="claude-3-5-haiku-20241022",
        temperature=0
    )
```

**Características:**
- Usa Haiku (custo-benefício)
- Temperature=0 (determinístico)
- Pula testes se API key não está definida (não falha)

---

### 2. Prompts de Avaliação

**Localização:** `utils/test_prompts.py`

**5 Prompts Necessários:**

#### 2.1 Fluidez Conversacional
```python
FLUENCY_PROMPT = """
Avalie a fluidez da mensagem do sistema:

1. Não pergunta permissão ("Posso chamar X?")
2. Integração natural de outputs de agentes
3. Tom conversacional (não burocrático)

Mensagem: {message}

Avalie de 1-5 (5 = completamente fluida):
Justificativa:
"""
```

#### 2.2 Integração Entre Agentes
```python
INTEGRATION_QUALITY_PROMPT = """
Avalie a qualidade da integração entre agentes:

1. Transições naturais (sem quebras)
2. Contexto preservado (referências a turnos anteriores)
3. Experiência coesa (não parece sistema desconexo)

Orquestrador: {orchestrator_output}
Estruturador: {structurer_output}
Metodologista: {methodologist_output}
Mensagens ao usuário: {messages}

Avalie de 1-5 (5 = integração excelente):
Justificativa:
"""
```

#### 2.3 Provocação Socrática
```python
SOCRATIC_BEHAVIOR_PROMPT = """
Avalie se a resposta do sistema demonstra comportamento socrático genuíno:

1. Provocação genuína (expõe assumptions, não coleta burocrática)
2. Timing natural (não regras fixas)
3. Parada inteligente (não insiste infinitamente)

Resposta: {response}
Reflection prompt: {reflection_prompt}

Avalie de 1-5 (5 = excelente comportamento socrático):
Justificativa:
"""
```

#### 2.4 Preservação de Contexto
```python
CONTEXT_PRESERVATION_PROMPT = """
Avalie se o contexto foi preservado entre transições de agentes:

1. Focal argument evolui coerentemente
2. Informações de turnos anteriores são referenciadas
3. Não há perda de contexto (agente não "esquece" informações)

Focal argument (antes): {focal_before}
Focal argument (depois): {focal_after}
Mensagens: {messages}

Avalie de 1-5 (5 = contexto perfeitamente preservado):
Justificativa:
"""
```

#### 2.5 Qualidade de Decisões
```python
DECISION_QUALITY_PROMPT = """
Avalie a qualidade da decisão do agente:

1. Decisão é coerente com contexto fornecido
2. Justificativa é clara e específica
3. Não é arbitrária (usa critérios explícitos)

Contexto: {context}
Decisão: {decision}
Justificativa: {justification}

Avalie de 1-5 (5 = decisão excelente):
Justificativa:
"""
```

---

### 3. Helper `extract_score`

**Localização:** `utils/test_helpers.py`

**Especificação:**
```python
import re

def extract_score(evaluation_content: str) -> int:
    """
    Extrai score (1-5) da avaliação do LLM-as-judge.
    
    Procura por padrões:
    - "Avalie de 1-5: 4"
    - "score: 3"
    - "4/5"
    - Apenas número na linha
    
    Args:
        evaluation_content: Conteúdo da avaliação do LLM
        
    Returns:
        int: Score de 1-5
        
    Raises:
        ValueError: Se não encontrar score válido
    """
    patterns = [
        r"Avalie de 1-5.*?(\d)",
        r"score.*?(\d)",
        r"(\d)\s*/\s*5",
        r"(\d)\s*=\s*(?:excelente|ótimo|bom)",
        r"^(\d)$"  # Apenas número na linha
    ]
    
    for pattern in patterns:
        match = re.search(pattern, evaluation_content, re.IGNORECASE | re.MULTILINE)
        if match:
            score = int(match.group(1))
            if 1 <= score <= 5:
                return score
    
    raise ValueError(f"Não foi possível extrair score válido de: {evaluation_content}")
```

---

### 4. Marker no `pytest.ini`

**Adicionar:**
```ini
[pytest]
markers =
    unit: Testes unitários (mocks)
    integration: Testes de integração (API real)
    llm_judge: Testes que usam LLM-as-judge (requer API key)
    slow: Testes lentos (opcional)
```

---

## 📝 Testes Automatizados

### Princípio: Adicionar Validação de Qualidade

**NÃO substituir testes existentes**  
**ADICIONAR** função de teste com `@pytest.mark.llm_judge`

**Exemplo:**
```python
# Teste existente (estrutura)
def test_multi_agent_flow(multi_agent_graph):
    result = multi_agent_graph.invoke(state)
    assert result["orchestrator_analysis"] is not None
    assert result["next_step"] in ["explore", "suggest_agent"]

# ADICIONAR: Teste de qualidade
@pytest.mark.llm_judge
def test_multi_agent_flow_quality(multi_agent_graph, llm_judge):
    """Valida qualidade da experiência conversacional."""
    result = multi_agent_graph.invoke(state)
    
    # Validação estrutural (mantém)
    assert result["orchestrator_analysis"] is not None
    
    # NOVO: Validação de qualidade
    evaluation = llm_judge.invoke(
        CONVERSATION_QUALITY_PROMPT.format(
            response=result.get("messages", [])[-1].content,
            history=result.get("conversation_history", [])
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Qualidade conversacional insuficiente (score: {score})"
```

---

### Arquivos a Adicionar Testes

Baseado no **Épico 7** (problemas identificados), adicionar testes em:

#### 1. `tests/integration/test_multi_agent_smoke.py`
**Validar:**
- Fluidez conversacional (sem "Posso chamar X?")
- Integração entre agentes (transições naturais)
- Preservação de contexto (focal_argument evolui)

**Exemplo:**
```python
@pytest.mark.llm_judge
def test_conversational_fluency(multi_agent_graph, llm_judge):
    """Valida que sistema não pede permissão para transições."""
    state = create_initial_multi_agent_state(
        "Observei que LLMs aumentam produtividade",
        session_id="test-fluency-1"
    )
    
    result = multi_agent_graph.invoke(state)
    
    # Extrair mensagens ao usuário
    user_messages = [
        msg.content for msg in result.get("messages", [])
        if isinstance(msg, AIMessage)
    ]
    
    # Validar cada mensagem
    for message in user_messages:
        evaluation = llm_judge.invoke(
            FLUENCY_PROMPT.format(message=message)
        )
        score = extract_score(evaluation.content)
        assert score >= 4, f"Mensagem não é fluida: {message[:50]}... (score: {score})"
```

---

#### 2. `tests/integration/test_methodologist_smoke.py`
**Validar:**
- Perguntas são socráticas (não burocráticas)
- Decisões têm critérios claros (não arbitrárias)

**Exemplo:**
```python
@pytest.mark.llm_judge
def test_socratic_questions_quality(methodologist_graph, llm_judge):
    """Valida que perguntas do Metodologista são socráticas."""
    state = create_initial_methodologist_state(
        "Café aumenta produtividade"
    )
    
    result = methodologist_graph.invoke(state)
    
    if result.get("status") == "pending":
        clarifications = result.get("clarifications", {})
        
        for question in clarifications.keys():
            evaluation = llm_judge.invoke(
                SOCRATIC_QUESTION_PROMPT.format(question=question)
            )
            score = extract_score(evaluation.content)
            assert score >= 4, f"Pergunta não é socrática: {question} (score: {score})"
```

---

#### 3. `scripts/flows/validate_socratic_behavior.py` → Converter para teste automatizado
**Validar:**
- Provocação socrática genuína (expõe assumptions)
- Timing natural (não regras fixas)
- Parada inteligente (não insiste infinitamente)

**Exemplo:**
```python
@pytest.mark.llm_judge
def test_socratic_provocation_quality(orchestrator_node, llm_judge):
    """Valida que provocação socrática é genuína."""
    state = create_state_with_vague_metric(
        "Quero medir produtividade"
    )
    
    result = orchestrator_node(state)
    
    reflection_prompt = result.get("reflection_prompt", "")
    response = result.get("messages", [])[-1].content
    
    evaluation = llm_judge.invoke(
        SOCRATIC_BEHAVIOR_PROMPT.format(
            response=response,
            reflection_prompt=reflection_prompt
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Provocação não é socrática (score: {score})"
```

---

#### 4. `scripts/flows/validate_conversation_flow.py` → Converter para teste automatizado
**Validar:**
- Fluidez conversacional end-to-end
- Não há quebras entre transições

---

#### 5. `scripts/flows/validate_multi_agent_flow.py` → Converter para teste automatizado
**Validar:**
- Integração natural entre agentes
- Contexto preservado durante transições

---

#### 6. `scripts/flows/validate_refinement_loop.py` → Converter para teste automatizado
**Validar:**
- Refinamentos endereçam gaps de forma significativa
- Evolução é coerente (não apenas mudança cosmética)

---

## 📊 Estratégia de Uso

### Fluxo Típico de Análise

#### 1. Rodar Cenário
```bash
python scripts/testing/run_scenario.py --scenario 3
```

#### 2. Revisar Output
Sistema printa relatório estruturado no terminal.

#### 3. Copiar para Claude (Se Necessário)
Se problema identificado, copiar relatório e colar no Claude.

#### 4. Discussão Contextualizada
Claude analisa, você discute, decidem próximos passos juntos.

#### 5. Investigar Mais Fundo (Se Necessário)
```bash
python scripts/testing/debug_scenario.py --scenario 3
```

Gera logs detalhados, copia para Claude, identifica causa raiz.

#### 6. Aplicar Correção
Claude sugere mudança no prompt → você decide → aplica via Cursor.

#### 7. Validar Correção
```bash
python scripts/testing/compare_results.py \
  --before baseline.json \
  --after current.json
```

Verifica se correção funcionou sem quebrar outros cenários.

---

### Execução Local (Única Forma Neste Épico)

```bash
# Rodar apenas testes LLM-as-Judge
pytest -m llm_judge

# Rodar testes LLM-as-Judge + estruturais
pytest tests/integration/ -m "integration or llm_judge"

# Rodar com debug mode
pytest tests/integration/test_cenario_2.py --debug

# Rodar multi-turn completo
pytest tests/integration/test_multi_turn_flows.py
```

**Nota:** CI/CD será considerado em épicos futuros (Épico 10+) quando houver contexto adequado (repositório público, múltiplos desenvolvedores, deploy contínuo).

---

### Quando Usar Cada Ferramenta

| Ferramenta | Quando Usar |
|------------|-------------|
| `run_scenario.py` | Validar cenário específico |
| `run_all_scenarios.py` | Validar suite completa |
| `debug_scenario.py` | Investigar problema específico |
| `compare_results.py` | Validar mudança no prompt |
| `interactive_analyzer.py` | Exploração geral / aprendizado |

---

## 💰 Custo Estimado (Atualizado)

- **Por teste LLM-as-Judge:** ~$0.001-0.002 (Haiku)
- **Por cenário multi-turn (3-5 turnos):** ~$0.005-0.010
- **Suite completa (10-15 testes single + 3-5 multi-turn):** ~$0.02-0.03
- **Execução semanal (desenvolvimento):** ~$0.10-0.15

**Nota:** Multi-turn aumenta custo mas é essencial para validar fluxos completos.

**Comparado:**
- Épico 7 manual: ~2-3h de trabalho
- Épico 8 assistido: ~30-45min de trabalho
- **Economia:** 60-75% do tempo, custo similar

---

## 🎯 Critérios de Aceite do Épico 8

### 8.1 Multi-Turn Executor Implementado (PRIORIDADE #1)
- [ ] `ConversationScenario` criado em `utils/test_scenarios.py`
- [ ] `MultiTurnExecutor` implementado em `utils/test_executor.py`
- [ ] Fixture `multi_turn_executor` criada em `tests/conftest.py`
- [ ] Cenários 3, 6, 7 do Épico 7 convertidos para multi-turn
- [ ] Testes em `tests/integration/test_multi_turn_flows.py` criados
- [ ] Validação estrutural + qualidade (LLM-as-Judge) funcionando

### 8.2 Debug Mode Implementado (PRIORIDADE #2)
- [ ] `DebugExecutor` implementado em `utils/test_executor.py`
- [ ] Fixture `debug_executor` criada em `tests/conftest.py`
- [ ] Logs salvos automaticamente em `logs/debug/`
- [ ] Comparação antes/depois de mudanças no prompt funcionando
- [ ] Flag `--debug` funciona em pytest

### 8.3 Infraestrutura LLM-as-Judge (PRIORIDADE #3)
- [ ] Fixture `llm_judge` criada em `tests/conftest.py`
- [ ] 5 prompts de avaliação criados em `utils/test_prompts.py`
- [ ] Função `extract_score` criada em `utils/test_helpers.py`
- [ ] Marker `@pytest.mark.llm_judge` adicionado em `pytest.ini`
- [ ] Testes pulam se `ANTHROPIC_API_KEY` não está definida

### 8.4 Testes Automatizados Criados
- [ ] Testes multi-turn em `test_multi_turn_flows.py` (cenários 3, 6, 7)
- [ ] Testes de qualidade em `test_multi_agent_smoke.py` (fluidez, integração)
- [ ] Testes de qualidade em `test_methodologist_smoke.py` (socrático, decisões)
- [ ] Scripts de validação convertidos para testes automatizados:
  - [ ] `validate_socratic_behavior.py`
  - [ ] `validate_conversation_flow.py`
  - [ ] `validate_multi_agent_flow.py`
- [ ] Cada teste valida qualidade (score >= 4) além de estrutura

### 8.5 Documentação Atualizada
- [ ] `docs/testing/epic8_automation_strategy.md` atualizado
- [ ] Aprendizados do Épico 7 documentados
- [ ] Custos estimados atualizados (~$0.02-0.03 por execução)
- [ ] Estratégia de execução local documentada
- [ ] Como adicionar novos testes documentado

**Removido do escopo:**
- ❌ CI/CD (postergar para Épico 10+)

---

## 📚 Referências

- `docs/testing/epic7_results/summary.md` - Aprendizados do Épico 7
- `docs/testing/epic7_validation_strategy.md` - Validação manual (Fase 1)
- `docs/roadmap_epic8_9_10.md` - Roadmap completo

---

**Versão:** 2.0 (Reformulado após Épico 7)  
**Data:** Dezembro 2025  
**Filosofia:** Assistir análise humana, não substituí-la
