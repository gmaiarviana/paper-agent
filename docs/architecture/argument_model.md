# Argument Model - Estrutura de Dados

> **Nota:** Para entender o que é Argumento filosoficamente, consulte `docs/architecture/ontology.md`.
> Para evolução cognitiva (claim → fundamentos), consulte `docs/vision/cognitive_model/evolution.md`.

## Visão Geral
Argumento é estrutura lógica que defende/explora uma ideia. É a materialização técnica do modelo cognitivo.

## Schema de Dados
```python
Argument:
    id: UUID
    idea_id: UUID                    # pertence a qual ideia
    
    # Estrutura lógica
    claim: str                        # afirmação principal
    fundamentos: list[ProposicaoRef]  # Proposições que sustentam
    evidencias: list[EvidenciaRef]    # Evidências diretas do argumento
    
    # Metadados
    concepts: list[UUID]              # conceitos usados no argumento
    context: dict                     # contexto específico do argumento
    created_at: datetime
    updated_at: datetime
```

### Campos Detalhados

**claim:**
Afirmação central que o argumento defende:
```python
claim: "Cooperação humana em massa depende de mitos compartilhados"
```

**fundamentos:**
Lista de referências a Proposições que sustentam o argumento:
```python
fundamentos: [
    ProposicaoRef(id="prop-1"),  # "Linguagem permite transmitir ficções" (solidez: 0.85)
    ProposicaoRef(id="prop-2"),  # "Humanos acreditam em mitos, animais não" (solidez: 0.90)
    ProposicaoRef(id="prop-3"),  # "Causalidade é direta: mitos → cooperação" (solidez: 0.35)
]
```

**Nota:** Não há mais distinção entre "premises" e "assumptions". Todas são Proposições com solidez variável:
- Proposições de alta solidez (> 0.7) = equivalente ao antigo "premise"
- Proposições de baixa solidez (< 0.4) = equivalente ao antigo "assumption"
- Solidez é derivada automaticamente das evidências (ver `docs/architecture/ontology.md`)

**evidencias:**
Lista de referências a Evidências diretas do argumento:
```python
evidencias: [
    EvidenciaRef(id="evid-1"),  # "Católicos cooperam via crença em Deus" (Sapiens, Cap 2)
    EvidenciaRef(id="evid-2"),  # "Estudo XYZ, 2023: 20% redução em turnover"
]
```

**Nota:** Evidências também podem estar vinculadas às Proposições (fundamentos). Ver seção "Relação com Evidências" abaixo.

## Relação com Proposições

Argumento referencia Proposições (não contém strings diretamente). Cada Proposição é uma entidade independente com sua própria solidez.

**Características:**
- **Argumento referencia Proposições**: `fundamentos` é lista de `ProposicaoRef`, não strings
- **Cada Proposição tem solidez própria**: Derivada automaticamente das evidências que a sustentam
- **Solidez do Argumento é derivada**: Calculada a partir da solidez dos fundamentos
- **Fragilidade se propaga**: Se um fundamento é frágil (solidez < 0.4), o argumento também é afetado

**Exemplo:**
```python
# Proposição independente
proposicao_1 = Proposicao(
    id="prop-1",
    enunciado="Linguagem permite transmitir ficções",
    solidez=0.85,  # Derivado de 3 evidências
    evidencias_apoiam=[...]
)

# Argumento referencia a proposição
argumento = Argument(
    claim="Cooperação humana depende de mitos",
    fundamentos=[ProposicaoRef(id="prop-1")]  # Referência, não cópia
)
```

**Benefícios:**
- Reutilização: mesma Proposição pode ser fundamento de múltiplos Argumentos
- Rastreabilidade: mudança na solidez de uma Proposição afeta todos os Argumentos que a usam
- Consistência: não há duplicação de conhecimento

## Relação com Evidências

Evidências podem ser vinculadas de duas formas:

**1. Evidências diretas do Argumento:**
```python
argumento = Argument(
    claim="Claude Code reduz tempo de sprint",
    evidencias=[
        EvidenciaRef(id="evid-1"),  # Estudo de Smith et al.
    ]
)
```

**2. Evidências vinculadas às Proposições (fundamentos):**
```python
# Evidência vinculada à Proposição
proposicao = Proposicao(
    id="prop-1",
    enunciado="Equipes Python existem",
    evidencias_apoiam=[
        EvidenciaRef(id="evid-2"),  # Dados do GitHub
    ]
)

# Argumento usa a Proposição (e indiretamente suas evidências)
argumento = Argument(
    fundamentos=[ProposicaoRef(id="prop-1")]
)
```

**Como evidências afetam solidez:**
- Evidências que apoiam aumentam solidez da Proposição
- Evidências que refutam diminuem solidez da Proposição
- Solidez é recalculada automaticamente quando novas evidências são adicionadas
- Ver `docs/architecture/ontology.md` para estrutura completa de Evidência

## Conexão com Modelo Cognitivo

> **Nota:** Para detalhes completos do modelo cognitivo, consulte `docs/vision/cognitive_model/core.md`.

Argumento é estruturação técnica do modelo cognitivo. Durante a conversa, o modelo cognitivo trabalha com proposições (strings) que são então persistidas como entidades Proposição e referenciadas pelo Argumento.

**Diferença:**
- **cognitive_model:** Estado em memória durante conversa (proposições como strings)
- **argument:** Entidade persistida no banco (referências a Proposições)

## Múltiplos Argumentos por Ideia

Uma ideia pode ter múltiplos argumentos (diferentes lentes):
```python
# Ideia: "Semana de 4 dias"

# Argumento 1 (lente: produtividade):
argument_1 = Argument(
    id="arg-1",
    idea_id="idea-semana-4-dias",
    claim="Semana de 4 dias aumenta produtividade",
    fundamentos=[
        ProposicaoRef(id="prop-descanso-foco"),  # "Descanso aumenta foco" (solidez: 0.75)
    ],
    evidencias=[
        EvidenciaRef(id="evid-empresas-x"),  # "Empresas X reportaram 15% aumento"
    ]
)

# Argumento 2 (lente: retenção):
argument_2 = Argument(
    id="arg-2",
    idea_id="idea-semana-4-dias",
    claim="Semana de 4 dias reduz turnover em 20%",
    fundamentos=[
        ProposicaoRef(id="prop-satisfacao-retencao"),  # "Satisfação aumenta retenção" (solidez: 0.80)
    ],
    evidencias=[
        EvidenciaRef(id="evid-estudo-y"),  # "Estudo Y com 1000 empresas"
    ]
)
```

## Responsabilidades dos Agentes

> **Nota:** Para detalhes dos agentes, consulte `docs/orchestration/multi_agent_architecture.md`.

**Quem constrói cada campo:**

- **claim:** Orquestrador extrai da conversa
- **fundamentos:** Estruturador identifica proposições e cria referências
- **evidencias:** Pesquisador busca (futuro) ou usuário fornece
- **Proposições:** Criadas pelo Estruturador ou Orquestrador durante refinamento
- **Solidez de Proposições:** Calculada automaticamente pelo sistema baseado em evidências

## Evolução de Argumento (Conversas)

Durante conversa, argumento evolui conforme sistema refina:
```python
# V1 (vago)
argument_v1 = Argument(
    id="arg-v1",
    claim="LLMs aumentam produtividade",
    fundamentos=[],
    evidencias=[]
)

# V2 (refinado)
argument_v2 = Argument(
    id="arg-v2",
    claim="LLMs aumentam produtividade em desenvolvimento",
    fundamentos=[
        ProposicaoRef(id="prop-dev-llms"),  # "Desenvolvedores usam LLMs" (solidez: 0.70)
        ProposicaoRef(id="prop-prod-mensuravel"),  # "Produtividade é mensurável" (solidez: 0.60)
    ],
    evidencias=[]
)

# V3 (específico)
argument_v3 = Argument(
    id="arg-v3",
    claim="Claude Code reduz tempo de sprint em 30%",
    fundamentos=[
        ProposicaoRef(id="prop-equipes-python"),  # "Equipes Python de 2-5 devs existem" (solidez: 0.85)
        ProposicaoRef(id="prop-tempo-sprint"),  # "Produtividade medida por tempo de sprint" (solidez: 0.70)
        ProposicaoRef(id="prop-qualidade-nao-comprometida"),  # "Qualidade não é comprometida" (solidez: 0.35)
    ],
    evidencias=[
        EvidenciaRef(id="evid-equipe-x"),  # "Dados da equipe X" (interno)
    ]
)
```

**Observação:** Proposição `prop-qualidade-nao-comprometida` tem solidez baixa (0.35), indicando fragilidade. Isso seria equivalente ao antigo "assumption" que precisava validação.

## Storage

**SQLite:**
```sql
CREATE TABLE arguments (
    id TEXT PRIMARY KEY,
    idea_id TEXT,
    claim TEXT,
    fundamentos JSON,  -- Lista de ProposicaoRef
    evidencias JSON,    -- Lista de EvidenciaRef
    context JSON,
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

**Nota:** `fundamentos` e `evidencias` armazenam referências (UUIDs), não dados completos. As entidades Proposição e Evidência são armazenadas em tabelas separadas (ver `docs/architecture/ontology.md`).

## Referências

- `docs/architecture/ontology.md` - Estrutura de Proposição e Evidência
- `docs/vision/epistemology.md` - Base filosófica (por que não há premises/assumptions)
- `docs/vision/cognitive_model/core.md` - Conceitos fundamentais do modelo cognitivo
- `docs/vision/cognitive_model/evolution.md` - Processo de evolução do pensamento
- `docs/architecture/idea_model.md` - Como Ideia possui Argumentos
- `docs/orchestration/multi_agent_architecture.md` - Responsabilidades dos agentes

