# Ontologia do Sistema

## Visão Geral

Este documento é o **Single Source of Truth (SSoT)** que define a ontologia do super-sistema. Ele estabelece o que são Conceito, Ideia, Argumento, Proposição e Evidência do ponto de vista filosófico, e como essas entidades se relacionam entre si.

A ontologia reflete uma filosofia epistemológica onde não existe distinção binária entre "fato" e "suposição", mas sim proposições com diferentes graus de solidez baseados em evidências. Para entender a base filosófica completa, consulte `docs/vision/epistemology.md`.

Outros documentos de arquitetura referenciam este documento como base para entender as entidades fundamentais do sistema.

---

## Observador e CognitiveModel

### Responsável pela Atualização

O **Observador (Mente Analítica)** é o agente responsável por monitorar conversa e atualizar o `CognitiveModel` a cada turno.

**Processo:**
1. Usuário envia mensagem
2. Orquestrador processa (decide next_step)
3. **Observador processa em paralelo** (silencioso):
   - Extrai claims emergentes
   - Identifica fundamentos
   - Detecta contradições
   - Cataloga conceitos (ChromaDB + SQLite)
   - Identifica open_questions
   - Atualiza context (domínio, população, tecnologia)
   - Calcula métricas (solidez, completude)
4. CognitiveModel atualizado

**Timing:** Todo turno, sempre (não apenas snapshots).

**Características:**
- ✅ Silencioso (não interfere no fluxo)
- ✅ Automático (não precisa ser chamado)
- ✅ Completo (processa todos os turnos)
- ✅ Consultável (Orquestrador pode pedir insights)

### Estrutura do CognitiveModel

```python
CognitiveModel:
  # Proposições centrais
  claims: list[str]
  
  # Argumentos de suporte
  fundamentos: list[str]
  
  # Inconsistências detectadas
  contradictions: list[dict]
  
  # Conceitos semânticos (biblioteca global)
  conceitos: list[UUID]  # Referências a Concept
  
  # Lacunas a investigar
  open_questions: list[str]
  
  # Contexto evolutivo
  context: dict  # {domain, population, technology}
  
  # Métricas calculadas
  solidez_geral: float  # 0-1
  completude: float     # 0-1
```

---

## Entidades Fundamentais

### Conceito (Abstrato, Reutilizável, Atemporal)

**O que é:** Núcleo semântico abstrato que pode assumir diferentes formas linguísticas.

**Natureza:** Entidade **GLOBAL** (biblioteca única, não pertence a uma ideia específica).

**Filosofia:**
- Conceitos são **essências compartilhadas** entre múltiplas ideias
- Uma ideia **referencia** conceitos, não os **possui**
- Biblioteca cresce continuamente (conceitos de todas as conversas)
- Deduplicação automática (threshold 0.80) garante catálogo limpo

**Características:**
- Transcende palavras específicas
- Reutilizável entre diferentes ideias
- Tem variações linguísticas (produtividade, eficiência, performance = mesma essência)
- **Atemporal**: Conceitos existem independentemente de tempo, contexto ou usuário
- **Não possui solidez**: Conceitos são rótulos semânticos, não afirmações sobre o mundo
- **Origem flexível**: Podem vir de usuário, literatura, múltiplos usuários ou emergir do sistema

#### Biblioteca Global de Conceitos

**Natureza independente:**
- Conceitos existem independentemente de ideias
- Sistema mantém vocabulário compartilhado (dicionário universal)
- Múltiplas ideias referenciam o mesmo conceito da biblioteca global
- Conceito existe uma vez na biblioteca, usado por N ideias
- **Conceitos são atemporais**: Existem independente de quem os usa ou quando foram criados
- **Conceitos não têm "solidez"**: São rótulos semânticos, não afirmações que podem ser verdadeiras ou falsas

**Exemplo:**
```
Ideia 1: "LLMs aumentam produtividade"
  → referencia: [Concept: "LLMs", Concept: "Produtividade"]

Ideia 2: "Produtividade depende de métricas claras"
  → referencia: [Concept: "Produtividade", Concept: "Métricas"]

Biblioteca global:
  • LLMs (usado por: Ideia 1)
  • Produtividade (usado por: Ideia 1, Ideia 2)
  • Métricas (usado por: Ideia 2)
```

**Atualizado por:** Observador (a cada turno)

**Schema:**
```python
Concept:
  id: UUID
  label: str                    # "LLMs", "Produtividade"
  essence: str                  # Definição curta (opcional)
  variations: list[str]         # ["Language Models", "Large Language Models"]
  embedding: vector[384]        # ChromaDB (sentence-transformers)
  
  # Metadados
  created_at: datetime
  usage_count: int              # Quantas ideias usam este conceito
```

**Relacionamento N:N:**
```sql
idea_concepts:
  idea_id: UUID → ideas(id)
  concept_id: UUID → concepts(id)
```

**Deduplicação:**
- Similaridade > 0.80: variation do conceito existente
- Similaridade < 0.80: conceito novo

**Exemplos de globalidade:**

Conceito "Cooperação" (global, único na biblioteca):
- Essência: Ação coordenada de múltiplos agentes
- Variações linguísticas: cooperação, colaboração, teamwork, coopération (francês)
- Referenciado por Ideia 1: "Cooperação via mitos" (Sapiens)
- Referenciado por Ideia 2: "Cooperação tribal" (Clastres)
- Referenciado por Ideia 3: "Cooperação cívica" (Putnam)

### Ideia (Território, Contextual)

**O que é:** Pensamento articulado que reúne conceitos e argumentos em contexto específico.

**Características:**
- Usa múltiplos conceitos
- Pode ter múltiplos argumentos (diferentes lentes)
- Evolui ao longo de conversa
- Contextual (não necessariamente universal)

**Exemplos:**
- Ideia: "Cooperação humana via mitos compartilhados"
  - Conceitos usados: [Cooperação, Ficção, Linguagem]
  - Argumentos: [Religião permite cooperação, Nacionalismo permite cooperação]

### Proposição (Unidade Base de Conhecimento)

**O que é:** Afirmação sobre o mundo que pode ser sustentada ou refutada por evidências. É a unidade base de conhecimento no sistema.

**Estrutura:**
```python
Proposição:
  id: UUID
  texto: str                        # "Qualidade de código é mensurável"
  solidez: Optional[float]          # 0-1, DERIVADO (não definido manualmente)
                                    # None = proposição ainda não avaliada pelo sistema
  evidencias: list[Evidência]       # Lista de evidências (inicialmente vazia)
  usos: [ArgumentoRef]              # Onde é usada como fundamento
```

**Solidez inicial:**
- Proposições nascem com `solidez: None` (não avaliada)
- Observador ou Orquestrador avaliam via LLM e atualizam para valor numérico (0-1)
- Pesquisador (futuro) adiciona evidências que recalculam solidez
- Cálculos de maturidade ignoram proposições com `solidez=None`

**Características fundamentais:**
- **Não existe "fato" vs "suposição"**: Todas são proposições com diferentes graus de solidez
- **Solidez é calculada**: Derivada automaticamente das evidências (quantidade, qualidade, fonte)
- **Reutilizável**: Uma proposição pode ser usada como fundamento em múltiplos argumentos
- **Evolutiva**: Solidez muda conforme novas evidências são adicionadas

**Exemplos:**
- Proposição: "Linguagem permite transmitir ficções"
  - Solidez: 0.85 (múltiplas evidências de estudos linguísticos)
  - Usada em: Argumento sobre cooperação via mitos
  
- Proposição: "Qualidade de código é mensurável"
  - Solidez: 0.60 (algumas evidências, mas debate metodológico)
  - Usada em: Argumento sobre métricas de produtividade

**Importante:** "Premissa" agora é um **PAPEL**, não um tipo. Premissa = proposição sendo usada como fundamento de um argumento específico. Não há mais distinção entre premise/assumption - apenas proposições com solidez diferente.

### Evidência (Sustentação de Proposições)

**O que é:** Informação que apoia ou refuta uma proposição.

**Estrutura:**
```python
Evidência:
  id: UUID
  descricao: str                    # "Estudo de Smith et al. (2023)"
  fonte: str                        # DOI, URL, referência
  forca: str                        # "forte", "moderada", "fraca"
  tipo: str                         # "estudo", "exemplo", "autoridade", "experiência"
  contexto: str                     # Em que contexto essa evidência se aplica
```

**Características:**
- **Pode apoiar ou refutar**: Uma evidência pode fortalecer ou enfraquecer uma proposição
- **Força variável**: Evidências têm diferentes graus de força (forte, moderada, fraca)
- **Tipos diversos**: Estudos empíricos, exemplos, autoridade, experiência pessoal
- **Contexto importa**: Evidências são válidas em contextos específicos

**Exemplos:**
- Evidência (apoia): "Estudo de Smith et al. (2023) com 1000 desenvolvedores mostra correlação entre TDD e redução de bugs"
  - Tipo: estudo
  - Força: forte
  - Fonte: DOI: 10.1234/example

- Evidência (refuta): "Experiência pessoal: TDD aumentou tempo de desenvolvimento em 30%"
  - Tipo: experiência
  - Força: fraca
  - Contexto: equipe pequena, projeto específico

### Argumento (Lente, Estrutura Lógica)

**O que é:** Uma forma de ver/defender uma ideia através de estrutura lógica (claim + fundamentos).

**Características:**
- Estrutura: claim → fundamentos (proposições) → evidências
- Múltiplos argumentos podem defender mesma ideia (diferentes ângulos)
- Argumento = mapa, Ideia = território
- **Fundamentos são proposições**: Não há mais distinção entre premises/assumptions

**Nota de migração (Épico 11):**
O código atual ainda usa `premises`/`assumptions` como strings separadas.
O Épico 11 migrará para estrutura de `proposicoes: List[Proposicao]`.

**Estrutura atualizada:**
```python
Argumento:
  id: UUID
  idea_id: UUID
  claim: str                        # Afirmação principal (campo separado, não é proposição)
  fundamentos: [ProposicaoRef]      # Proposições que sustentam o argumento
  evidencias: [EvidenciaRef]        # Evidências diretas do argumento
```

**Exemplos:**
- Ideia: "Semana de 4 dias"
  - Argumento 1 (lente produtividade): 
    - Claim: "Aumenta produtividade via descanso"
    - Fundamentos: [Proposição: "Descanso aumenta foco", Proposição: "Foco aumenta produtividade"]
  - Argumento 2 (lente retenção):
    - Claim: "Reduz turnover em 20%"
    - Fundamentos: [Proposição: "Satisfação aumenta retenção"]

---

## Fluxo de Detecção de Conceitos

### Pipeline (Observador)

```
Usuário: "LLMs aumentam produtividade"
    ↓
Observador: Processa turno
    ↓
1. LLM extrai conceitos: ["LLMs", "Produtividade"]
    ↓
2. Para cada conceito:
    ↓
   Gera embedding (sentence-transformers)
    ↓
   Busca similares no catálogo (ChromaDB)
    ↓
   Similaridade > 0.80?
     ├─ SIM → Adiciona como variation
     └─ NÃO → Cria novo conceito
    ↓
   Salva metadados (SQLite)
    ↓
3. Atualiza CognitiveModel.conceitos
    ↓
4. Publica evento: ConceptsDetectedEvent
```

### Exemplo Completo

**Turno 1:**
```
Input: "LLMs aumentam produtividade"
Detecta: ["LLMs", "Produtividade"]
Salva ambos (conceitos novos)

Biblioteca:
• LLMs
• Produtividade
```

**Turno 3:**
```
Input: "Language models são eficientes"
Detecta: ["Language models", "Eficiência"]

"Language models" similar a "LLMs" (0.92)
→ Adiciona como variation de "LLMs"

"Eficiência" similar a "Produtividade" (0.85)
→ Adiciona como variation de "Produtividade"

Biblioteca:
• LLMs (variations: ["Language models"])
• Produtividade (variations: ["Eficiência"])
```

**Turno 5:**
```
Input: "Bugs afetam qualidade"
Detecta: ["Bugs", "Qualidade"]

Ambos novos (similaridade < 0.80)
→ Cria 2 novos conceitos

Biblioteca:
• LLMs (variations: ["Language models"])
• Produtividade (variations: ["Eficiência"])
• Bugs
• Qualidade
```

---

## Relações Entre Entidades

### Ideia ↔ Conceito (N:N)
- **Relacionamento é referência, não posse**: Ideia referencia múltiplos conceitos da biblioteca global
- Ideia não possui conceitos, apenas referencia entidades globais existentes
- Mesmo conceito da biblioteca aparece em múltiplas ideias (reutilização)
- Sistema detecta conceitos compartilhados via vetor semântico
- Conceito existe independentemente: mesmo que todas as ideias que o referenciam sejam removidas, o conceito permanece na biblioteca global

### Ideia ↔ Argumento (1:N)
- Ideia pode ter múltiplos argumentos (diferentes lentes)
- Argumento pertence a uma ideia

### Argumento ↔ Conceito (N:N)
- Argumento usa conceitos nos fundamentos (proposições contêm conceitos)

### Argumento ↔ Proposição (N:N)
- Argumento usa proposições como fundamentos
- Uma proposição pode ser usada em múltiplos argumentos

### Proposição ↔ Evidência (N:N)
- Proposição tem evidências que apoiam e evidências que refutam
- Evidência pode apoiar ou refutar múltiplas proposições

## Exemplo Completo: Sapiens (Harari)

**Texto original:**
"Cooperação humana em massa depende de mitos compartilhados. Dois católicos que nunca se encontraram podem embarcar juntos numa cruzada porque ambos acreditam que Deus encarnou num corpo humano."

**Sistema cristaliza:**

```python
Ideia: "Cooperação humana via mitos compartilhados"

Conceitos centrais:
- Ficção/Mito (vetor semântico)
- Cooperação (vetor semântico)
- Linguagem (vetor semântico)

Proposições:
- P1: "Linguagem permite transmitir ficções" (solidez: 0.85)
- P2: "Mitos compartilhados permitem cooperação em massa" (solidez: 0.75)

Evidências:
- E1: "Católicos cooperam via crença em Deus" (apoia P2, tipo: exemplo, força: moderada)
- E2: "Sérvios cooperam via crença em nação" (apoia P2, tipo: exemplo, força: moderada)
- E3: "Estudos linguísticos mostram capacidade de transmitir abstrações" (apoia P1, tipo: estudo, força: forte)

Argumento principal:
claim: "Cooperação em massa depende de mitos compartilhados"
fundamentos: [P1, P2]  # Proposições usadas como fundamentos
evidências: [E1, E2, E3]
```

## Hierarquia (Ideias dentro de Ideias)

Livros/textos complexos podem ter estrutura hierárquica:

```
Ideia macro: "Revoluções que transformaram Sapiens"
├─ Sub-ideia 1: "Revolução Cognitiva"
│   └─ Ideia específica: "Cooperação via mitos"
├─ Sub-ideia 2: "Revolução Agrícola"
│   └─ Ideia específica: "Agricultura como armadilha"
```

Sistema identifica hierarquia automaticamente processando conteúdo.

---

## Observador e Snapshots

### Complementaridade

**Observador:** Processa TODOS os turnos (monitoramento contínuo)
**Snapshots:** Marcos importantes quando argumento amadurece

**Fluxo:**
```
Turno 1-5: Observador cataloga conceitos continuamente
    ↓
Turno 5: Argumento amadurece → Snapshot criado
    ↓
Snapshot referencia conceitos catalogados pelo Observador
    ↓
Turno 6-10: Observador continua catalogando
    ↓
Turno 10: Novo snapshot → referencia conceitos novos
```

**Vantagem:**
- Snapshots não precisam reprocessar para detectar conceitos
- Conceitos já estão catalogados pelo Observador
- Snapshot apenas cria links (idea_concepts)

---

## Rastreabilidade

### Propagação de Solidez

Quando uma proposição é usada como fundamento em múltiplos argumentos, sua solidez afeta todos eles:

- **Fragilidade se propaga**: Se uma proposição base tem baixa solidez, todos os argumentos que dependem dela são afetados
- **Fortalecimento se propaga**: Fortalecer uma proposição fortalece todos os argumentos que dependem dela
- **Alertas automáticos**: Sistema pode alertar: "3 argumentos dependem de proposição com baixa solidez (0.35)"

**Exemplo:**
```
Proposição P: "Qualidade de código é mensurável" (solidez: 0.40)
  └─ Usada em Argumento A1: "Métricas de qualidade validam TDD"
  └─ Usada em Argumento A2: "Code review reduz bugs"
  └─ Usada em Argumento A3: "Refactoring melhora manutenibilidade"

Sistema alerta: "3 argumentos dependem de proposição com baixa solidez. 
Fortalecer P fortaleceria A1, A2 e A3."
```

### Dependências Explícitas

O sistema mantém rastreabilidade clara de:
- Quais argumentos dependem de cada proposição
- Quais proposições são fundamentais (usadas em muitos argumentos)
- Como fragilidades em proposições base afetam a solidez geral do conhecimento

### Estratégia de Fortalecimento

Quando uma proposição é identificada como frágil:
1. Sistema identifica todos os argumentos que dependem dela
2. Sugere buscar evidências para fortalecer a proposição
3. Mostra impacto: "Fortalecer esta proposição afetaria 5 argumentos"

## Referências

- `docs/vision/epistemology.md` - Fundamento filosófico da ontologia (proposições, solidez, evidências)
- `docs/architecture/concept_model.md` - Schema detalhado de Concept
- `docs/architecture/idea_model.md` - Estrutura de dados técnica de Ideia
- `docs/architecture/argument_model.md` - Estrutura de dados técnica de Argumento
- `docs/vision/cognitive_model/core.md` - Conceitos fundamentais (artefatos, solidez)
- `docs/vision/cognitive_model/evolution.md` - Como pensamento evolui e solidez é calculada
- `docs/agents/observer.md` - Documentação completa do Observador
- `ROADMAP.md` - Épicos 10, 12, 13 (Observador e Conceitos)

