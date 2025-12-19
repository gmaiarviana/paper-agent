# Message Model - Estrutura de Dados

> **Nota:** Para entender o que é Mensagem filosoficamente, consulte `core/docs/vision/communication_philosophy.md` (visão conceitual).
> Para entender as entidades fundamentais (Ideia, Argumento, Proposição), consulte `ontology.md`.

## Visão Geral

**Mensagem** é combinação intencional de proposições para transmitir **UMA ideia** através de vetor emocional específico.

### Diferença Fundamental

- **Ideia** = território (pensamento articulado)
- **Argumento** = lente (claim + fundamentos)
- **Mensagem** = seleção intencional (O QUE comunicar + vetor emocional)

**Características:**
- Mensagem seleciona proposições/argumentos baseado em similaridade vetorial emocional
- Permite customização de evidências dentro de argumentos
- Ilumina/apaga argumentos baseado em relevância ao vetor emocional
- Interface visual permite montagem intencional da comunicação

## Schema de Dados

```python
Message:
    id: UUID
    idea_id: UUID                    # De qual ideia vem
    
    # Núcleo da mensagem
    intencao: str                     # "Provocar questionamento sobre escolhas de vida"
    emocao_vetor: list[float]         # Vetor no espaço latente (128-512 dims)
                                      # MVP: dict com categorias fixas
                                      # Visão: vetor sem rótulos
    
    # Proposições selecionadas (grafo de relevância)
    proposicoes_centrais: list[ProposicaoRef]      # Alta aderência
    proposicoes_perifericas: list[ProposicaoRef]   # Média aderência
    proposicoes_omitidas: list[ProposicaoRef]      # Baixa aderência
    
    # Customização de componentes
    argumentos_selecionados: list[ArgumentoCustomizado]
    
    # Metadados
    created_at: datetime
    updated_at: datetime
```

### Campos Detalhados

**intencao:**
Objetivo comunicacional da mensagem:
```python
intencao: "Provocar questionamento sobre escolhas de vida"
```

**emocao_vetor:**
Vetor emocional que guia seleção de argumentos/proposições.

**MVP (determinístico):**
```python
emocao_vetor: {
    "empatia": 0.8,
    "urgência": 0.5,
    "confianca_racional": 0.3,
    "nostalgia": 0.7
}
```

**Visão (indeterminístico):**
```python
emocao_vetor: [0.23, -0.87, 0.45, ..., -0.34]  # 128-512 dimensões
```

**proposicoes_centrais:**
Proposições com alta similaridade vetorial ao vetor emocional da mensagem:
```python
proposicoes_centrais: [
    ProposicaoRef(id="prop-1"),  # Similaridade: 0.92
    ProposicaoRef(id="prop-2"),  # Similaridade: 0.88
]
```

**proposicoes_perifericas:**
Proposições com média similaridade (podem ser incluídas com menor ênfase):
```python
proposicoes_perifericas: [
    ProposicaoRef(id="prop-3"),  # Similaridade: 0.61
]
```

**proposicoes_omitidas:**
Proposições com baixa similaridade (não incluídas na mensagem):
```python
proposicoes_omitidas: [
    ProposicaoRef(id="prop-4"),  # Similaridade: 0.34
]
```

**argumentos_selecionados:**
Lista de argumentos customizados incluídos na mensagem:
```python
argumentos_selecionados: [
    ArgumentoCustomizado(
        argumento_id="arg-1",
        evidencias_selecionadas=["evid-3", "evid-2"],
        ordem=1,
        enfase=0.9
    ),
    ArgumentoCustomizado(
        argumento_id="arg-2",
        evidencias_selecionadas=["evid-5"],
        ordem=2,
        enfase=0.6
    )
]
```

### ArgumentoCustomizado

```python
ArgumentoCustomizado:
    argumento_id: UUID
    evidencias_selecionadas: list[UUID]  # Quais evidências incluir
    ordem: int                           # Posição na mensagem
    enfase: float                        # 0-1 (quanto destacar)
```

**evidencias_selecionadas:**
Subconjunto de evidências do argumento que serão incluídas na mensagem. Sistema sugere inicialmente baseado em similaridade vetorial, usuário pode customizar.

**ordem:**
Posição do argumento na sequência da mensagem (1 = primeiro, 2 = segundo, etc).

**enfase:**
Grau de destaque do argumento na mensagem (0.0 = mínimo, 1.0 = máximo).

## Customização de Evidências

Cada argumento pode ter múltiplos dados/evidências. Usuário pode customizar quais evidências incluir na mensagem.

### Exemplo Concreto

**Argumento:** "Afastamento natureza causa ansiedade"

Evidências disponíveis:
- Evidência 1: "Estudo Smith et al. (2023): correlação 0.8"
- Evidência 2: "Meta-análise de 15 estudos"
- Evidência 3: "Relato pessoal: mudei, ansiedade sumiu"
- Evidência 4: "Dados OMS sobre saúde mental urbana"

**Mensagem customizada:**
- ✓ Evidência 3 (relato pessoal) ← desperta empatia
- ✓ Evidência 2 (meta-análise) ← reforça confiança
- ✗ Evidência 1 (estudo isolado) ← omite (muito técnico)
- ✗ Evidência 4 (dados OMS) ← omite (muito genérico)

**Processo:**
1. Sistema sugere combinação inicial via similaridade vetorial
2. Usuário pode adicionar/remover/reordenar evidências
3. Preview atualiza em tempo real

## Grafo de Relevância

Mensagem ilumina/apaga argumentos baseado em similaridade vetorial:

```
    [💡 Ideia: "Cidades fazem mal"]
                |
    [🔵 Proposição: "Afastamento natureza"]
                |
    ┌───────────┼───────────┐
    |           |           |
[🟢 Arg A]  [⚪ Arg B]  [🟡 Arg C]
Vivencial   Científico  Evolutivo
Sim: 0.92   Sim: 0.34   Sim: 0.61
    |           |           |
[Evidências customizáveis]
✓ E1: Relato pessoal
✓ E2: Dados qualidade vida
✗ E3: Estatísticas técnicas
```

**Legenda:**
- 🟢 = Alta similaridade vetorial (iluminado, incluído)
- 🟡 = Média similaridade (periférico, opcional)
- ⚪ = Baixa similaridade (apagado, omitido)

### Cálculo de Similaridade

**MVP (determinístico):**
```python
# Categorias fixas
mensagem_vetor = {"empatia": 0.8, "urgência": 0.5}
argumento_vetor = {"empatia": 0.9, "confianca": 0.2}

# Similaridade manual (weighted overlap)
def weighted_overlap(v1, v2):
    # Soma dos produtos das dimensões comuns
    overlap = sum(v1[k] * v2[k] for k in v1 if k in v2)
    # Normalização
    norm1 = sum(v**2 for v in v1.values()) ** 0.5
    norm2 = sum(v**2 for v in v2.values()) ** 0.5
    return overlap / (norm1 * norm2)

similarity = weighted_overlap(mensagem_vetor, argumento_vetor)
```

**Visão (indeterminístico):**
```python
# Espaço latente
mensagem_vetor = [0.23, -0.87, 0.45, ..., -0.34]  # 128+ dims
argumento_vetor = [0.21, -0.82, 0.51, ..., -0.29]

# Similaridade cosseno
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(v1, v2):
    return dot(v1, v2) / (norm(v1) * norm(v2))

similarity = cosine_similarity(mensagem_vetor, argumento_vetor)
```

## Proposição → Múltiplos Argumentos (Lentes)

Uma proposição pode ser defendida por múltiplos argumentos (ângulos diferentes):

```python
Proposicao:
    id: "prop-1"
    enunciado: "Afastamento da natureza causa ansiedade"
    
    # Múltiplas lentes (argumentos)
    argumentos: [
        {
            id: "arg-cientifico",
            claim: "Estudos comprovam correlação",
            vetor_emocional: [0.12, 0.87, ...]  # Visão
            # MVP: {"confianca_racional": 0.9, "empatia": 0.2}
        },
        {
            id: "arg-vivencial",
            claim: "Relato pessoal de transformação",
            vetor_emocional: [0.78, -0.23, ...]  # Visão
            # MVP: {"empatia": 0.9, "nostalgia": 0.7}
        }
    ]
```

**Sistema escolhe qual argumento usar** baseado em similaridade entre:
- Vetor emocional da mensagem
- Vetor emocional do argumento

**Exemplo:**
- Mensagem com vetor `{"empatia": 0.9}` → escolhe `arg-vivencial`
- Mensagem com vetor `{"confianca_racional": 0.9}` → escolhe `arg-cientifico`

## Interface de Montagem (Conceitual)

Usuário monta mensagem visualmente através de interface iterativa:

### Fluxo de Montagem

1. **Define vetor emocional**
   - Conversação: "Como quer que pessoa se sinta?"
   - Sistema converte resposta em vetor (MVP: categorias fixas, Visão: espaço latente)

2. **Sistema sugere argumentos ranqueados**
   - Calcula similaridade vetorial para todos os argumentos da ideia
   - Apresenta ranqueados: 🟢 alta, 🟡 média, ⚪ baixa

3. **Usuário aceita/ajusta sugestões**
   - Pode incluir argumentos de média similaridade
   - Pode excluir argumentos de alta similaridade
   - Pode reordenar argumentos

4. **Para cada argumento, usuário customiza evidências**
   - Sistema sugere evidências baseado em similaridade
   - Usuário adiciona/remove/reordena evidências
   - Preview mostra impacto na mensagem

5. **Usuário reordena componentes**
   - Define ordem de argumentos na mensagem
   - Ajusta ênfase (enfase: 0-1)

6. **Preview atualiza em tempo real**
   - Mostra como mensagem ficará estruturada
   - Indica quais proposições estão iluminadas/apagadas
   - Permite ajustes iterativos

### Visualização Conceitual

```
┌─────────────────────────────────────────┐
│ Mensagem: "Provocar questionamento"      │
│ Vetor: {empatia: 0.8, urgência: 0.5}    │
├─────────────────────────────────────────┤
│                                         │
│ 🟢 Arg A: Vivencial (0.92)             │
│    ✓ Evidência 3: Relato pessoal        │
│    ✓ Evidência 2: Meta-análise          │
│    ✗ Evidência 1: Estudo isolado        │
│                                         │
│ 🟡 Arg C: Evolutivo (0.61)             │
│    ✓ Evidência 5: Dados evolutivos      │
│                                         │
│ ⚪ Arg B: Científico (0.34) [omitido]   │
│                                         │
└─────────────────────────────────────────┘
```

## Relacionamentos

### Message ↔ Idea (N:1)
```python
# Mensagem pertence a uma ideia
message.idea_id = idea_id

# Ideia pode ter múltiplas mensagens
idea.messages = [message_id_1, message_id_2]
```

### Message ↔ Argument (N:N via ArgumentoCustomizado)
```python
# Mensagem referencia argumentos customizados
message.argumentos_selecionados = [
    ArgumentoCustomizado(argumento_id="arg-1", ...),
    ArgumentoCustomizado(argumento_id="arg-2", ...)
]

# Argumento pode aparecer em múltiplas mensagens
argument.used_in_messages = [message_id_1, message_id_2]
```

### Message ↔ Proposição (N:N via grafo de relevância)
```python
# Mensagem referencia proposições por relevância
message.proposicoes_centrais = [ProposicaoRef(id="prop-1"), ...]
message.proposicoes_perifericas = [ProposicaoRef(id="prop-3"), ...]
message.proposicoes_omitidas = [ProposicaoRef(id="prop-4"), ...]

# Proposição pode aparecer em múltiplas mensagens
proposicao.used_in_messages = [message_id_1, message_id_2]
```

## Storage

**SQLite:**
```sql
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    idea_id TEXT,
    intencao TEXT,
    emocao_vetor JSON,              -- MVP: dict, Visão: array
    proposicoes_centrais JSON,      -- Lista de ProposicaoRef
    proposicoes_perifericas JSON,   -- Lista de ProposicaoRef
    proposicoes_omitidas JSON,      -- Lista de ProposicaoRef
    argumentos_selecionados JSON,   -- Lista de ArgumentoCustomizado
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (idea_id) REFERENCES ideas(id)
);

CREATE TABLE message_propositions (
    message_id TEXT,
    proposition_id TEXT,
    relevance_type TEXT,            -- "central" | "periferica" | "omitida"
    similarity_score REAL,         -- Similaridade vetorial calculada
    PRIMARY KEY (message_id, proposition_id, relevance_type),
    FOREIGN KEY (message_id) REFERENCES messages(id),
    FOREIGN KEY (proposition_id) REFERENCES propositions(id)
);
```

**Nota:** `argumentos_selecionados` armazena estrutura completa de `ArgumentoCustomizado` (incluindo evidências selecionadas), não apenas referências.

## Referências

- `ontology.md` - Definição de Ideia, Argumento, Proposição
- `argument_model.md` - Estrutura de dados técnica de Argumento
- `idea_model.md` - Estrutura de dados técnica de Ideia
- `core/docs/vision/communication_philosophy.md` - Base filosófica de Mensagem (visão conceitual)

