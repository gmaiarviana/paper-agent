# Super-Sistema: Core Universal → Múltiplos Produtos

## Visão Geral

O sistema não é apenas "paper-agent". É um **super-sistema** com core universal que serve múltiplos produtos desacoplados via APIs.

**Produtos atuais/futuros:**
- **Revelar:** Clareza de ideias via diálogo
- **Prisma Verbal:** Extração de conceitos de textos
- **Camadas da Linguagem:** Estruturação de mensagens
- **Expressão:** Produção de conteúdo em formas diversas
- **Produtor Científico:** Artigos acadêmicos (especialização de Expressão)

## Arquitetura: Core → Products

```
         REVELAR                    PRISMA VERBAL
        (diálogo)                  (texto estático)
             │                            │
             │                            │
             ▼                            ▼
        ┌─────────────────────────────────────┐
        │                                     │
        │      MOTOR VETORIAL COMUM           │
        │                                     │
        │  ┌─────────┐  ┌───────────┐  ┌────┐│
        │  │CONCEITOS│  │ARGUMENTOS │  │IDEIAS│
        │  │(padrões)│  │(emergem)  │  │    ││
        │  └─────────┘  └───────────┘  └────┘│
        │                                     │
        └─────────────────────────────────────┘
                         │
                         ▼
               CAMADAS DA LINGUAGEM
                   (estruturação)
                         │
                         ▼
                    EXPRESSÃO
                  (dar forma)
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      PRODUTOR CIENTÍFICO      (outros formatos)
        (artigo acadêmico)      (post, email, etc)
```

## Core Universal (Compartilhado)

### O Que é Core

Tudo que é **independente de produto específico**:

✅ **Motor Vetorial:** Espaço vetorial compartilhado para conceitos, argumentos, ideias  
✅ **Inferências Vetoriais:** Similaridade, composição, analogia via operações vetoriais  
✅ **Ontologia:** Conceito, Ideia, Argumento, Mensagem, MemoryLayer, BackstageContext  
✅ **Modelo Cognitivo:** claim → fundamentos (com solidez variável)  
✅ **Agentes:** Orquestrador, Observador, Estruturador, Metodologista, Memory Agent, Comunicador (futuro)  
✅ **Infraestrutura:** LangGraph (state), ChromaDB (vetores), SQLite (metadados)  
✅ **Conversação:** Diálogo socrático, provocação, refinamento

**Entidades Core:**
```
Core Universal (compartilhado):
├─ Ontologia (Conceito, Ideia, Argumento, Proposição, Evidência)
├─ Mensagem (combinação intencional para comunicação)
├─ Modelo Cognitivo (claim → fundamentos)
├─ Agentes (Orquestrador, Estruturador, ...)
└─ Infraestrutura (LangGraph, ChromaDB, SQLite)
```

**Fluxo Completo:**
```
Conversa → Ideia → Argumento → Mensagem → Forma (artigo/post/etc)
|         |         |            |          |
Revelar   Revelar   Revelar    Camadas    Expressão/
                              Linguagem   Produtor
                                            Científico
```  

### O Que NÃO é Core

Tudo que é **específico de produto**:

❌ Formatos de conteúdo específicos (artigo, post, email)  
❌ Interfaces específicas (dashboard, chat, upload)  
❌ Lógica de estruturação de mensagem (Camadas da Linguagem)  
❌ Lógica de expressão em formato (Expressão)  

## Agentes do Core

### Orquestrador (Coordenação Lógica)
Responsável por coordenar o fluxo de trabalho entre agentes, decidindo qual agente deve ser acionado em cada etapa do processo. Gerencia o estado global da execução e garante que as transições entre agentes ocorram de forma coerente.

**Visão futura:** Orquestrador evolui para gerenciar múltiplos produtos simultaneamente, roteando requisições de diferentes serviços para os agentes apropriados do core.

### Observador (Processamento Interno)
Processa e analisa o conteúdo gerado pelos outros agentes, extraindo conceitos, identificando padrões e mantendo a consistência ontológica. Trabalha de forma transparente, sem interação direta com o usuário.

**Visão futura:** Observador se torna o "olho" do core, monitorando qualidade, consistência e evolução do conhecimento em todos os produtos.

### Memory Agent (Memória de Longo Prazo)
Gerencia as camadas de memória (superficial, intermediária, profunda) do sistema. Responsável por armazenar, recuperar e compactar memórias de longo prazo, garantindo escalabilidade temporal e degradação controlada.

**Responsabilidades:**
- Gerenciar snapshots de estado
- Compactação periódica de memórias antigas
- Busca otimizada por camada (recente = rápido, antigo = lento)
- Configuração de memória por produto

### Comunicador (Interface Linguística - Futuro)
Agente responsável por traduzir entre a linguagem natural do usuário e as operações do core. Abstrai a complexidade dos agentes internos, oferecendo uma interface conversacional unificada para todos os produtos.

**Status:** Planejado para futuro, permitirá que produtos diferentes compartilhem a mesma capacidade de diálogo socrático e refinamento.

## Produtos como Serviços Desacoplados

### Produtos Consomem Core via API

**Exemplo: Revelar**
```python
# Revelar chama core via API para criar ideia
response = core_api.create_idea(
    title="LLMs aumentam produtividade",
    context={"source_type": "conversation"}
)

idea_id = response.idea_id

# Revelar trabalha com ideias até alcançar clareza
```

**Exemplo: Prisma Verbal**
```python
# Prisma Verbal processa texto via core
response = core_api.process_text(
    text=pdf_content,
    context={"source_type": "book", "source": "Sapiens"}
)

# Core retorna conceitos e argumentos extraídos
concepts = response.concepts
arguments = response.arguments
```

**Exemplo: Camadas da Linguagem**
```python
# Camadas da Linguagem estrutura mensagem via core
response = core_api.create_message(
    idea_id=idea_id,
    emotional_vector=user_described_vector,
    context={"intent": "persuade"}
)

message_id = response.message_id
```

**Exemplo: Expressão**
```python
# Expressão consome mensagem para gerar conteúdo
response = core_api.generate_content(
    message_id=message_id,
    format="post",
    context={"platform": "linkedin"}
)

content = response.content
```

### Configuração de Memory por Produto

Cada produto configura as camadas de memória de acordo com suas necessidades específicas:

#### Revelar: Memory de Sessão
- **Superficial (10 turnos):** Últimas interações da conversa atual, acesso instantâneo
- **Intermediária (snapshots):** Estados importantes da sessão, pontos de decisão, ideias geradas
- **Profunda (50 turnos):** Histórico completo da sessão, contexto de longo prazo para continuidade

**Uso:** Manter contexto conversacional, permitir retomada de sessões, rastrear evolução de ideias.

#### Prisma Verbal: Memory de Documento
- **Superficial (capítulos):** Estrutura do documento, navegação rápida entre seções
- **Intermediária (conceitos):** Conceitos extraídos, relações entre ideias do documento
- **Profunda (citações):** Citações completas, contexto original, referências cruzadas

**Uso:** Catálogo de livros, busca por conceitos, análise comparativa entre documentos.

#### Camadas da Linguagem: Memory de Estruturação
- **Superficial (mensagem atual):** Estrutura da mensagem sendo criada, argumentos selecionados
- **Intermediária (padrões):** Padrões de estruturação, históricos de mensagens similares
- **Profunda (biblioteca):** Biblioteca completa de mensagens estruturadas, referências para reuso

**Uso:** Manter contexto de estruturação, aprender padrões eficazes, reutilizar estruturas.

#### Expressão / Produtor Científico: Memory de Formato
- **Superficial (conteúdo atual):** Rascunho sendo gerado, formatação aplicada
- **Intermediária (templates):** Templates de formato, estilos aplicados anteriormente
- **Profunda (arquivo):** Biblioteca de conteúdos gerados, histórico de formatações

**Uso:** Manter consistência de formato, aprender preferências do usuário, reutilizar estruturas eficazes.

## Mensagem no Super-Sistema

### O Que É Mensagem

**Mensagem** = Seleção intencional de proposições/argumentos para transmitir ideia através de vetor emocional específico.

**Diferença fundamental:**
- **Ideia** = território (pensamento articulado)
- **Argumento** = lente (claim + fundamentos)
- **Mensagem** = O QUE comunicar (combinação + vetor emocional)
- **Forma** = COMO expressar (artigo, post, poema)

### Onde Vive

**Core Universal:**
- Entidade Mensagem (schema, vetor emocional)
- Lógica de similaridade vetorial
- Grafo de relevância (argumentos iluminados/apagados)

**Produtos Específicos:**
- Revelar: NÃO cria mensagens (foco em clareza de ideia)
- Prisma Verbal: NÃO cria mensagens (foco em extração de conhecimento)
- Camadas da Linguagem: SIM, cria mensagens (estruturação de argumentos)
- Expressão / Produtor Científico: SIM, consome mensagens (dar forma ao conteúdo)

### Como Produtos Usam

**Camadas da Linguagem (cria mensagens):**

1. Recebe Ideia madura (de Revelar ou Prisma Verbal)
2. Sistema identifica argumentos relevantes no Motor Vetorial
3. Usuário descreve intenção: "Que sentimento quer despertar no leitor?"
4. Sistema gera vetor emocional
5. Sistema sugere argumentos ranqueados por similaridade
6. Usuário customiza (adiciona/remove evidências)
7. Sistema compila Mensagem (argumentos organizados + vetor emocional)

**Expressão / Produtor Científico (consome mensagens):**

1. Recebe Mensagem (de Camadas da Linguagem)
2. Usuário escolhe Forma (artigo, post, email, thread)
3. Sistema gera conteúdo final aplicando formato

**Revelar (NÃO usa):**
- Foco: clareza de pensamento (Ideia + Argumentos)
- Output: Ideia estruturada (pode ser passada para Camadas da Linguagem)
- NÃO cria mensagens (não é escopo)

**Prisma Verbal (NÃO usa):**
- Foco: extração de conhecimento de textos
- Output: Conceitos + Argumentos extraídos (alimenta Motor Vetorial)
- NÃO cria mensagens (não é escopo)

### Fluxo Entre Produtos

```
┌─────────────┐
│  Revelar    │ → Ideia estruturada
└──────┬──────┘
       │
       ↓
┌──────────────────────┐
│ Camadas da Linguagem │ → Mensagem (argumentos organizados + vetor emocional)
└──────┬───────────────┘
       │
       ↓
┌──────────────┐
│  Expressão   │ → Conteúdo (post, email, thread...)
└──────┬───────┘
       │
       ├── Produtor Científico → Artigo acadêmico
       └── (outros formatos futuros)
```

Usuário pode:
- Usar Revelar até Ideia ficar madura
- Passar para Camadas da Linguagem para estruturar mensagem
- Passar mensagem para Expressão / Produtor Científico para criar conteúdo
- OU parar em qualquer etapa (se só quer clareza, não conteúdo)

### Diferencial Competitivo

**Vetor Emocional Indeterminístico:**
- Usuário descreve subjetivamente sentimento desejado
- Sistema gera vetor no espaço latente (não categorias)
- Busca argumentos por similaridade emocional via Motor Vetorial
- Diferencial: transcende categorização racional de emoções

Ver: `core/docs/vision/communication_philosophy.md` para fundamento filosófico.

## Camadas da Linguagem

### O Que É

- Produto responsável por estruturar uma Ideia em Mensagem
- Input: Ideia (conjunto de argumentos, vindos de Revelar ou Prisma Verbal)
- Output: Mensagem (argumentos organizados + vetor emocional)

### O Que Faz

✅ Organiza argumentos e evidências para a intenção desejada  
✅ Define vetor emocional da mensagem  
✅ Seleciona quais argumentos usar, quais omitir  
✅ Prepara estrutura para ser "materializada" em forma  

### O Que NÃO Faz

❌ Não produz conteúdo final (isso é Expressão)  
❌ Não define formato (artigo, post, email)

## Expressão

### O Que É

- Produto responsável por transformar Mensagem em Conteúdo
- Input: Mensagem (estrutura + vetor emocional)
- Output: Conteúdo em forma específica

### Formas Possíveis

- Post de LinkedIn
- Email
- Thread de Twitter
- Apresentação
- (outros formatos futuros)

### Especializações

**Produtor Científico:**
- Fork de Expressão otimizado para artigos acadêmicos
- Mantém estrutura específica (Introdução, Metodologia, Resultados...)
- Validação metodológica integrada

### Vantagens do Desacoplamento

✅ **Independência:** Produtos evoluem sem quebrar outros  
✅ **Reuso:** Core evolui, todos produtos se beneficiam  
✅ **Escalabilidade:** Novos produtos consomem core existente  
✅ **Manutenção:** Bugs no core fixados uma vez, todos produtos se beneficiam  
✅ **Escalabilidade da Memory configurável por produto:** Cada produto define suas próprias camadas de memória (superficial, intermediária, profunda) de acordo com suas necessidades específicas  
✅ **Bastidores transparentes como diferencial:** O BackstageContext permite que produtos exponham (ou ocultem) o processo interno de geração de conhecimento, oferecendo transparência como feature

## Escalabilidade da Memory

A arquitetura de memória em camadas permite escalabilidade temporal através de degradação controlada e compactação periódica.

### Degradação Temporal

Memórias mais recentes são acessadas mais rapidamente, enquanto memórias antigas podem ter latência maior:

```python
# Exemplo de tempos de busca por camada
def search_memory(query: str, product: str) -> dict:
    """
    Busca em memória com degradação temporal.
    Retorna resultados ordenados por relevância e velocidade de acesso.
    """
    results = {
        "superficial": {
            "data": search_superficial(query, product),
            "latency_ms": 10,  # Acesso instantâneo
            "scope": "últimos 10 turnos/capítulos/semana"
        },
        "intermediaria": {
            "data": search_intermediaria(query, product),
            "latency_ms": 50,  # Acesso rápido
            "scope": "snapshots/conceitos/evolução"
        },
        "profunda": {
            "data": search_profunda(query, product),
            "latency_ms": 200,  # Acesso mais lento
            "scope": "50 turnos/citações/anos arquivados"
        }
    }
    return results
```

**Estratégia:** Busca começa pela camada superficial e expande para camadas mais profundas apenas quando necessário, otimizando performance.

### Compactação Periódica

Memórias antigas são compactadas para reduzir custo de armazenamento e manter performance:

- **Compactação mensal:** Memórias intermediárias de mais de 30 dias são comprimidas
- **Compactação anual:** Memórias profundas de mais de 1 ano são arquivadas em formato otimizado
- **Recuperação sob demanda:** Memórias compactadas podem ser restauradas quando necessário, com latência maior

**Benefício:** Sistema mantém performance constante mesmo com crescimento exponencial de dados históricos.

## Migração: Sistema Atual → Super-Sistema

Sistema migrou de entidade `Topic` para ontologia completa (`Idea`, `Concept`, `Argument`). Fundação técnica já implementada (Idea e Argument como entidades separadas). Próximos passos: Motor Vetorial (conceitos, argumentos, ideias) e produtos futuros (Camadas da Linguagem, Expressão, Produtor Científico).

## APIs do Core (Futuro)

### Endpoints Planejados

**Ideias:**
```
POST   /ideas              # Criar nova ideia
GET    /ideas/:id          # Obter ideia
PATCH  /ideas/:id          # Atualizar ideia
GET    /ideas/search       # Buscar ideias por conceito/título
```

**Conceitos:**
```
POST   /concepts           # Criar conceito
GET    /concepts/:id       # Obter conceito
GET    /concepts/similar   # Buscar conceitos similares
```

**Argumentos:**
```
POST   /arguments          # Criar argumento
GET    /arguments/:id      # Obter argumento
PATCH  /arguments/:id      # Atualizar (refinar)
```

**Conversação:**
```
POST   /conversations      # Iniciar conversa
POST   /conversations/:id/messages  # Enviar mensagem
GET    /conversations/:id/ideas     # Ideias geradas na conversa
```

**Memória:**
```
GET    /memory/search      # Buscar em memória (com degradação temporal)
GET    /memory/layers      # Obter configuração de camadas por produto
POST   /memory/compact     # Compactar memórias antigas (admin)
```

## Referências

- `../data-models/ontology.md` - Ontologia base (Core) - Definição de Mensagem na ontologia
- `../data-models/message_model.md` - Schema técnico de Mensagem
- `core/docs/vision/communication_philosophy.md` - Filosofia de Mensagem (emoção como espaço latente)
- `products/produtor-cientifico/docs/vision.md` - Produto específico
- `products/prisma-verbal/docs/vision.md` - Produto específico
- `core/docs/vision/epistemology.md` - Epistemologia do sistema (fundamentos com solidez)
- `ROADMAP.md` - Épicos 11+ (migração)

