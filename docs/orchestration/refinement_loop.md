# Refinement Loop - Especificação Técnica

## Visão Geral

Loop de refinamento colaborativo que permite ao sistema multi-agente melhorar ideias vagas até ficarem testáveis, ao invés de apenas validar ou rejeitar.

**Decisão arquitetural:** Loop implementado no super-grafo (não criar grafo interno no Estruturador).

---

## Componentes

### 1. MultiAgentState (atualizado)

**Campos novos:**

```python
class MultiAgentState(TypedDict):
    # ... campos existentes ...
    
    # NOVOS (Épico 4):
    refinement_iteration: int  # Contador de refinamentos (0, 1, 2)
    max_refinements: int       # Limite padrão: 2
    hypothesis_versions: list  # Histórico de versões
```

**Estrutura de hypothesis_versions:**

```python
hypothesis_versions: [
    {
        "version": 1,
        "question": "Como X impacta Y?",
        "feedback": {
            "status": "needs_refinement",
            "improvements": [
                {
                    "aspect": "população",
                    "gap": "Não especificada",
                    "suggestion": "Definir: adultos 18-40 anos"
                }
            ]
        }
    },
    {
        "version": 2,
        "question": "Como X impacta Y em adultos 18-40 anos?",
        "feedback": {
            "status": "approved",
            "improvements": []
        }
    }
]
```

### 2. Metodologista - Modo Colaborativo

**Output atualizado:**

```python
{
    "status": "approved" | "needs_refinement" | "rejected",
    "justification": str,
    "improvements": [  # Apenas se needs_refinement
        {
            "aspect": "população" | "métricas" | "variáveis" | "testabilidade",
            "gap": str,
            "suggestion": str
        }
    ],
    "clarifications": dict  # Mantido do Épico 2
}
```

**Lógica de decisão:**

1. **approved:**
   - Hipótese testável, falseável, específica, operacionalizada
   - Pode ter pequenas lacunas, mas estrutura sólida
   - Pronta para desenho experimental
2. **needs_refinement:**
   - Tem potencial científico
   - Faltam elementos específicos (população, métricas, variáveis)
   - Pode ser melhorada com refinamento
   - Campo `improvements` preenchido com gaps
3. **rejected:**
   - Sem potencial científico (crença popular, impossível testar)
   - Antropomorfização sem base
   - Vagueza extrema que refinamento não resolve

**Prompt do Metodologista (atualizado):**

Adicionar ao prompt existente:

```
MODO COLABORATIVO (Épico 4):

Você é um PARCEIRO que ajuda a CONSTRUIR hipóteses, não apenas validar
Use "needs_refinement" quando a ideia tem potencial mas falta especificidade
Use "rejected" APENAS quando não há base científica
Campo "improvements": seja ESPECÍFICO sobre o que falta e como preencher

EXEMPLOS DE "needs_refinement":
Input: "Método X melhora Y"
Output: {
"status": "needs_refinement",
"justification": "Ideia central clara, mas falta operacionalização",
"improvements": [
{
"aspect": "população",
"gap": "Não especificada",
"suggestion": "Definir população-alvo (ex: desenvolvedores 2-5 anos experiência)"
},
{
"aspect": "métricas",
"gap": "Y não mensurável",
"suggestion": "Operacionalizar Y (ex: bugs/sprint, tempo de debug)"
}
]
}
```

### 3. Estruturador - Processamento de Feedback

**Input no refinamento (V2+):**

```python
{
    "user_input": str,  # Input original
    "previous_question": str,  # Questão V1
    "methodologist_feedback": {
        "status": "needs_refinement",
        "improvements": [...]
    },
    "version": int  # 2, 3
}
```

**Lógica de refinamento:**

1. Ler gaps do Metodologista
2. Para cada gap, adicionar elemento faltante na questão
3. Manter essência da ideia original
4. Gerar V2 que endereça todos os gaps

**Prompt do Estruturador (atualizado):**

Adicionar ao prompt existente:

```
REFINAMENTO (Épico 4):
Quando receber feedback do Metodologista:

Identifique gaps específicos
Adicione elementos faltantes SEM mudar a essência
Endereçe TODOS os gaps listados

EXEMPLO:
Input original: "Método X é mais rápido"
Feedback: falta população, métricas
V2: "Método X reduz tempo em 30%, medido por sprints, em equipes de 2-5 devs"
Gaps endereçados:

População: "equipes de 2-5 devs"
Métricas: "tempo em 30%", "sprints"
```

### 4. Router do Super-Grafo

**Após Metodologista, decidir próximo nó:**

```python
def route_after_methodologist(state: MultiAgentState) -> str:
    """
    Router que decide fluxo após Metodologista processar hipótese.
    
    Lógica:
    1. Se approved → END
    2. Se rejected → END
    3. Se needs_refinement:
       - Se iteration < max_refinements → "structurer"
       - Se iteration >= max_refinements → forçar decisão final
    """
    methodologist_output = state['methodologist_output']
    status = methodologist_output['status']
    iteration = state['refinement_iteration']
    max_iter = state['max_refinements']
    
    if status == "approved":
        return END
    
    if status == "rejected":
        return END
    
    if status == "needs_refinement":
        if iteration < max_iter:
            # Ainda pode refinar
            return "structurer"
        else:
            # Limite atingido, forçar decisão
            return "methodologist_force_decision"
    
    # Fallback
    return END
```

---

## Fluxo Completo

### Cenário 1: Ideia vaga + 1 refinamento → aprovada

1. User: "Método incremental é mais rápido"
2. Orquestrador: classifica "vague"
3. Estruturador V1: "Como método incremental impacta velocidade?"
4. Metodologista: "needs_refinement" (falta população, métricas)
   - refinement_iteration: 0 → 1
5. Estruturador V2: "Método incremental reduz tempo em 30%, medido por sprints, em equipes 2-5 devs"
6. Metodologista: "approved"
7. END (usuário recebe V2 aprovada)

### Cenário 2: Ideia vaga + 2 refinamentos → aprovada

1. User: "Observei X"
2. Estruturador V1: "Como X se manifesta?"
3. Metodologista: "needs_refinement" (falta contexto, problema)
   - refinement_iteration: 0 → 1
4. Estruturador V2: "Em que contexto X ocorre com maior frequência?"
5. Metodologista: "needs_refinement" (falta métricas)
   - refinement_iteration: 1 → 2
6. Estruturador V3: "Em que contexto X (medido por Y) ocorre com maior frequência em população Z?"
7. Metodologista: "approved"
8. END

### Cenário 3: Limite atingido → decisão forçada

1. User: "Z melhora W"
2. Estruturador V1: "Como Z impacta W?"
3. Metodologista: "needs_refinement" (falta tudo)
   - refinement_iteration: 0 → 1
4. Estruturador V2: "Como Z impacta W em contexto Y?"
5. Metodologista: "needs_refinement" (ainda falta métricas)
   - refinement_iteration: 1 → 2
6. Estruturador V3: "Como Z (medido por M) impacta W em contexto Y?"
7. Metodologista (decisão forçada): "approved" ou "rejected"
   - Prompt: "Esta é a última iteração. Decida com contexto disponível."
8. END

---

## Implementação

**Arquivos a modificar:**

1. `agents/orchestrator/state.py`
   - Adicionar campos: `refinement_iteration`, `max_refinements`, `hypothesis_versions`
2. `agents/methodologist/nodes.py`
   - Atualizar nó `decide`: nova lógica com 3 status
   - Adicionar nó `force_decision`: decisão forçada após limite
3. `agents/structurer/nodes.py`
   - Adicionar lógica de refinamento: processar feedback
4. `agents/multi_agent_graph.py`
   - Adicionar router `route_after_methodologist`
   - Configurar loop: Metodologista → Estruturador
5. `utils/prompts.py`
   - Prompt do Metodologista V2 (modo colaborativo)
   - Prompt do Estruturador V2 (handling de feedback)

---

## Testes

**Testes unitários (mocks):**

- `test_methodologist_collaborative_mode.py`
- `test_structurer_refinement.py`
- `test_refinement_router.py`

**Testes de integração (API real):**

- `test_refinement_loop_smoke.py`

**Scripts de validação manual:**

- `scripts/validate_refinement_loop.py`

---

## Metadados

- **Versão:** 1.0 (Épico 4)
- **Data:** 11/11/2025
- **Status:** Especificação completa para implementação


