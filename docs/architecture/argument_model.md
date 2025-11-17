# Argument Model - Estrutura de Dados

> **Nota:** Para entender o que é Argumento filosoficamente, consulte `docs/architecture/ontology.md`.
> Para evolução cognitiva (claim → premises), consulte `docs/product/cognitive_model.md`.

## Visão Geral
Argumento é estrutura lógica que defende/explora uma ideia. É a materialização técnica do modelo cognitivo.

## Schema de Dados
```python
Argument:
    id: UUID
    idea_id: UUID               # pertence a qual ideia
    
    # Estrutura lógica
    claim: str                  # afirmação principal
    premises: list[str]         # fundamentos assumidos verdadeiros
    assumptions: list[str]      # hipóteses não verificadas
    evidence: list[dict]        # evidências que sustentam
    
    # Metadados
    concepts: list[UUID]        # conceitos usados no argumento
    context: dict               # contexto específico do argumento
    created_at: datetime
    updated_at: datetime
```

### Campos Detalhados

**claim:**
Afirmação central que o argumento defende:
```python
claim: "Cooperação humana em massa depende de mitos compartilhados"
```

**premises:**
Fundamentos assumidos como verdadeiros:
```python
premises: [
    "Linguagem permite transmitir ficções",
    "Humanos acreditam em mitos, animais não"
]
```

**assumptions:**
Hipóteses não verificadas que precisam validação:
```python
assumptions: [
    "Causalidade é direta: mitos → cooperação (sem confundidores)",
    "Resultado generaliza para todas culturas"
]
```

**evidence:**
Evidências que sustentam o argumento:
```python
evidence: [
    {
        "type": "example",
        "description": "Católicos cooperam via crença em Deus",
        "source": "Sapiens, Cap 2"
    },
    {
        "type": "data",
        "description": "20% redução em turnover (empresas testadas)",
        "source": "Estudo XYZ, 2023"
    }
]
```

## Conexão com Modelo Cognitivo

> **Nota:** Para detalhes completos do modelo cognitivo, consulte `docs/product/cognitive_model.md`.

Argumento é estruturação técnica do modelo cognitivo:
```python
# Modelo cognitivo (como pensamento evolui)
cognitive_model = {
    "claim": "...",
    "premises": [...],
    "assumptions": [...],
    "open_questions": [...],
    "contradictions": [...],
    "solid_grounds": [...]
}

# Argumento (estrutura técnica persistida)
argument = Argument(
    claim=cognitive_model["claim"],
    premises=cognitive_model["premises"],
    assumptions=cognitive_model["assumptions"],
    evidence=cognitive_model["solid_grounds"]
)
```

**Diferença:**
- **cognitive_model:** Estado em memória durante conversa
- **argument:** Entidade persistida no banco

## Múltiplos Argumentos por Ideia

Uma ideia pode ter múltiplos argumentos (diferentes lentes):
```python
# Ideia: "Semana de 4 dias"

# Argumento 1 (lente: produtividade):
claim: "Semana de 4 dias aumenta produtividade"
premises: ["Descanso aumenta foco"]
evidence: ["Empresas X reportaram 15% aumento"]

# Argumento 2 (lente: retenção):
claim: "Semana de 4 dias reduz turnover em 20%"
premises: ["Satisfação aumenta retenção"]
evidence: ["Estudo Y com 1000 empresas"]
```

## Responsabilidades dos Agentes

> **Nota:** Para detalhes dos agentes, consulte `docs/orchestration/multi_agent_architecture.md`.

**Quem constrói cada campo:**

- **claim:** Orquestrador extrai da conversa
- **premises:** Estruturador organiza fundamentos
- **assumptions:** Orquestrador detecta suposições implícitas
- **evidence:** Pesquisador busca (futuro) ou usuário fornece
- **contradictions:** Metodologista valida lógica

## Evolução de Argumento (Conversas)

Durante conversa, argumento evolui conforme sistema refina:
```python
# V1 (vago)
claim: "LLMs aumentam produtividade"
premises: []
assumptions: []

# V2 (refinado)
claim: "LLMs aumentam produtividade em desenvolvimento"
premises: ["Desenvolvedores usam LLMs para codificar"]
assumptions: ["Produtividade é mensurável"]

# V3 (específico)
claim: "Claude Code reduz tempo de sprint em 30%"
premises: [
    "Equipes Python de 2-5 devs",
    "Produtividade medida por tempo de sprint"
]
assumptions: ["Qualidade não é comprometida"]
evidence: [
    {"description": "Dados da equipe X", "source": "interno"}
]
```

## Storage

**SQLite:**
```sql
CREATE TABLE arguments (
    id TEXT PRIMARY KEY,
    idea_id TEXT,
    claim TEXT,
    premises JSON,
    assumptions JSON,
    evidence JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (idea_id) REFERENCES ideas(id)
);

CREATE TABLE argument_concepts (
    argument_id TEXT,
    concept_id TEXT,
    PRIMARY KEY (argument_id, concept_id)
);
```

## Referências

- `docs/architecture/ontology.md` - Definição de Argumento
- `docs/product/cognitive_model.md` - Modelo cognitivo completo
- `docs/architecture/idea_model.md` - Como Ideia possui Argumentos
- `docs/orchestration/multi_agent_architecture.md` - Responsabilidades dos agentes

