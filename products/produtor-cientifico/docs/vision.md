# Visão de Produto - Produtor Científico

> **Nota:** Para filosofia universal do sistema, consulte `core/docs/vision/system_philosophy.md`.

## 1. Visão Geral do Produto

- **O que é**: Sistema para transformar ideias estruturadas em manuscritos científicos publicáveis
- **Para quem**: Pesquisadores acadêmicos (mestrandos, doutorandos, professores)
- **Problema resolvido**: Distância entre ideia estruturada e artigo pronto
- **Diferencial**: Agentes especializados por tipo de artigo + validação metodológica

## 2. Tipos de Artigo Acadêmico

### 2.1 Empírico/Experimental

- **Características distintivas**: Testa hipóteses com dados coletados; foca em delineamentos experimentais ou quasi-experimentais (ex.: RCT, coorte, A/B tests).
- **Checkpoints mínimos**: Hipótese clara → Definição de população/métricas → Desenho metodológico → Plano de coleta/análise → Interpretação dos resultados.
- **Agentes relevantes**: Metodologista (define desenho), Estruturador (formaliza hipótese), Orquestrador (coordena etapas), Escritor (tradução para manuscrito).

### 2.2 Revisão Sistemática/Literatura

- **Características distintivas**: Sintetiza conhecimento existente com protocolos estruturados (ex.: systematic review, scoping review); foco em transparência e reprodutibilidade.
- **Checkpoints mínimos**: Questão de pesquisa (PICO/SPIDER) → Estratégia de busca → Critérios de inclusão/exclusão → Extração/síntese → Conclusões e lacunas.
- **Agentes relevantes**: Orquestrador (define fluxo), Estruturador (formaliza protocolo), Pesquisador (execução da busca externa), Escritor (compila síntese).

### 2.3 Teórico/Conceitual

- **Características distintivas**: Propõe frameworks, modelos ou argumentos conceituais (ex.: modelos teóricos, argumentação filosófica).
- **Checkpoints mínimos**: Problema conceitual → Revisão crítica → Construção lógica → Proposição de framework → Discussão de implicações/limitações.
- **Agentes relevantes**: Estruturador (arquitetura do argumento), Metodologista (validação lógica), Escritor (articulação textual), Orquestrador (mantém coerência global).

### 2.4 Estudo de Caso

- **Características distintivas**: Analisa casos específicos com profundidade contextual (ex.: case study, etnografia).
- **Checkpoints mínimos**: Seleção do caso → Contextualização → Coleta de evidências → Análise interpretativa → Extração de insights e generalizações prudentes.
- **Agentes relevantes**: Metodologista (define protocolo qualitativo), Estruturador (organiza narrativa), Orquestrador (sincroniza revisões), Escritor (relato final).

### 2.5 Meta-Análise

- **Características distintivas**: Combina quantitativamente resultados de múltiplos estudos (ex.: meta-analysis, meta-regression).
- **Checkpoints mínimos**: Questão quantitativa → Busca sistemática → Extração de dados → Análise estatística (modelos/heterogeneidade) → Interpretação dos efeitos.
- **Agentes relevantes**: Metodologista (modelos estatísticos), Orquestrador (governa rigor), Estruturador (estrutura protocolo), Escritor (relata resultados).

### 2.6 Metodológico

- **Características distintivas**: Propõe ou valida novos métodos, instrumentos ou pipelines (ex.: validation study, method comparison).
- **Checkpoints mínimos**: Definição do método → Critérios de avaliação → Coleta/benchmark → Análise comparativa → Discussão de limitações/aplicabilidade.
- **Agentes relevantes**: Metodologista (constrói validação), Estruturador (documenta passo a passo), Orquestrador (assegura cobertura), Escritor (formaliza resultados).

## 3. Jornada do Usuário

> **💡 Nota de Interface:** Todos os cenários abaixo ocorrem na interface web conversacional. CLI mantém mesma funcionalidade mas é ferramenta auxiliar para desenvolvimento.

### Cenário A: Ideia Vaga (Empírico)

```
Usuário: "Observei que LLMs aumentam produtividade"
↓
Orquestrador: "Interessante! Me conta mais: você quer VER o que já existe 
               sobre isso, ou quer TESTAR uma hipótese sua?"
↓
Usuário: "Testar uma hipótese"
↓
Orquestrador: "Legal! Me conta mais sobre essa observação..."
↓
[Conversa até ficar claro o contexto]
↓
Orquestrador: "Organizei sua ideia em uma questão de pesquisa: 
               'Como LLMs impactam produtividade?' Isso captura o que você quer explorar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
↓
Usuário: "Sim, mas preciso ser mais específico"
↓
Orquestrador: "Validei e refinei: 'Como LLMs (ex.: Claude Code) reduzem tempo 
               de desenvolvimento em 30%, medido por sprints, em equipes de 2-5 devs?' 
               Isso faz sentido?"
[Bastidores: 🔬 Metodologista validou → 📝 Estruturador refinou → 🎯 Orquestrador curou]
↓
Usuário: "Perfeito!"
↓
Orquestrador: "Ótimo! Podemos seguir com: 1) definir desenho experimental, 
               2) pesquisar literatura sobre métricas, ou 3) algo diferente?"
```

### Cenário B: Questão para Revisão

```
Usuário: "Quero entender o estado da arte em multi-agente para escrita acadêmica"
↓
Orquestrador: "Interessante! Você quer fazer uma REVISÃO de literatura ou 
               tem uma HIPÓTESE específica para testar?"
↓
Usuário: "Revisão de literatura"
↓
Orquestrador: "Perfeito! Organizei uma questão de pesquisa estruturada 
               (PICO/SPIDER): [resultado]. Isso direciona bem o que você quer buscar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
↓
Usuário: "Sim"
↓
Orquestrador: "Busquei papers relevantes e organizei uma síntese inicial: 
               [resumo dos papers encontrados]. Isso cobre o que você precisa?"
[Bastidores: 🔍 Pesquisador buscou → 🎯 Orquestrador curou]
↓
Usuário: "Perfeito! Agora quero compilar a revisão completa"
↓
Orquestrador: "Compilei a revisão estruturada: [revisão completa]. Isso captura 
               o que você queria explorar?"
[Bastidores: ✍️ Escritor compilou → 🎯 Orquestrador curou]
```

### Cenário C: Framework Teórico

```
Usuário: "Proponho modelo de governança para sistemas multi-agente"
↓
Orquestrador: "Fascinante! Você já tem o modelo estruturado ou está ainda 
               explorando a ideia?"
↓
Usuário: "Tenho uma ideia inicial, mas preciso validar a lógica"
↓
Orquestrador: "Validei a consistência lógica do framework: [resultado da validação]. 
               Faz sentido?"
[Bastidores: 🔬 Metodologista validou → 🎯 Orquestrador curou]
↓
Usuário: "Perfeito!"
↓
Orquestrador: "Ótimo! Agora podemos: 1) estruturar o argumento completo, 
               2) pesquisar frameworks similares, ou 3) começar a escrever. 
               O que prefere?"
↓
Usuário: "Estruturar o argumento"
↓
Orquestrador: "Estruturei o argumento completo do framework: [argumentação 
               organizada]. Isso captura a lógica que você quer apresentar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
↓
Usuário: "Sim, agora quero redigir o artigo"
↓
Orquestrador: "Redigi o artigo teórico completo: [artigo]. Isso reflete o que 
               você queria comunicar?"
[Bastidores: ✍️ Escritor redigiu → 🎯 Orquestrador curou]
```

### Cenário D: Exploração Gradual (Claim Evolui)

```
Usuário começa vago, sistema provoca, claim cristaliza:
Usuário: "É possível fazer levantamento de obra com tecnologia?"
↓
Sistema: "Interessante! 'Tecnologia' é amplo. Você está pensando em:
         - IA para análise de plantas/documentos?
         - Drones para medição física?
         - Software de gestão de projetos?
         Qual aspecto te intriga mais?"
↓
Usuário: "Drones para medir volumes"
↓
Sistema (detecta suposições): "Você assumiu que precisão de drones é suficiente 
         para levantamento oficial. Já considerou margem de erro?"
↓
Usuário: "Boa pergunta. Qual margem é aceitável?"
↓
Sistema: "Levantamento oficial exige < 2%. Pesquisei e encontrei que drones com 
         visão computacional conseguem < 1.5% de erro. Isso resolve sua questão?"
[Bastidores: 🔍 Pesquisador pesquisou → 🎯 Orquestrador curou]
↓
[Claim evoluiu: "Tecnologia ajuda obras" → "Drones com visão computacional 
 podem medir volumes com precisão suficiente para levantamento oficial"]
```

## 4. Da Ideia ao Manuscrito

Quando uma ideia atinge maturidade (fundamentos sólidos, poucas questões abertas):

1. Usuário acessa ideia e clica "Criar Conteúdo"
2. Abre chat para definir expectativas (formato, tom, ênfase)
3. Orquestrador chama Escritor
4. Conteúdo gerado a partir de metadados já elaborados (claim, fundamentos, evidências)

**Formatos possíveis:**
- Artigo acadêmico
- Post de blog/LinkedIn
- Thread de Twitter
- Apresentação

## 5. Casos de Uso Principais

- **UC1: Validar Hipótese Científica** – De uma observação vaga para uma hipótese testável ou descarte fundamentado.
- **UC2: Estruturar Revisão de Literatura** – Transformar questão de pesquisa em protocolo estruturado (PICO/SPIDER) e compilar síntese de literatura.
- **UC3: Escrever Artigo Teórico** – Construir framework conceitual com validação lógica e redigir manuscrito teórico completo.
- **UC4: Pesquisar Literatura** – Gerar síntese de papers relevantes com rastreabilidade das fontes e análise crítica.
- **UC5: Compilar Manuscrito** – Converter artefatos consolidados (hipótese, metodologia, resultados) em manuscrito científico no estilo do usuário.
- **UC6: Revisar Metodologia** – Analisar desenho metodológico e produzir feedback estruturado com ações recomendadas para rigor científico.

## 6. Entidades do Produto

Produtor Científico adiciona entidades específicas sobre o core universal para gerenciar artigos acadêmicos.

### 6.1 Article (Agregador de Ideias)

Article é a entidade central que agrega múltiplas ideias do core em um artigo científico estruturado:

```python
Article:
  id: UUID
  title: str                    # "Impacto de LLMs em Produtividade"
  ideas: list[UUID]             # Ideias que compõem o artigo
  
  # Metadados específicos
  article_type: str             # "empirical", "review", "theoretical"
  sections: list[Section]       # Introdução, Metodologia, ...
  status: str                   # "draft", "review", "complete"
  
  # Resumo compilado
  summary: str
  
  # Metadados de publicação
  authors: list[str]
  institution: str
  keywords: list[str]
```

### 6.2 Section (Parte do Artigo)

Section representa uma seção estruturada do artigo (Introdução, Metodologia, Resultados, etc.):

```python
Section:
  id: UUID
  article_id: UUID
  name: str                     # "Introdução", "Metodologia"
  ideas: list[UUID]             # Ideias usadas nesta seção
  content: str                  # Texto compilado
  status: str                   # "pending", "draft", "reviewed"
```

### 6.3 Como Article Consome Core

Produtor Científico consome o core universal via API para criar e gerenciar ideias, agregando-as em artigos:

```python
# Produtor Científico chama core via API
core_api = CoreAPI()

# Criar ideia via conversa
idea = core_api.create_idea_from_conversation(
  conversation_id=conv_id
)

# Adicionar ideia ao artigo
article = Article(
  title="Impacto de LLMs",
  ideas=[idea.id]
)

# Buscar ideias relacionadas (core fornece)
related_ideas = core_api.find_related_ideas(
  idea_id=idea.id,
  min_similarity=0.75
)
```

## 7. Interface: Gestão de Artigos

### 7.1 Sidebar: Gestão de Artigos

Interface permite gerenciar múltiplos artigos simultaneamente:

**Últimos 10 artigos:**
```
📄 Impacto de LLMs (ativo)
📄 Semana de 4 dias (pausado)
📄 Automação com IA (pausado)
...
```

**Funcionalidades:**
- Alternar entre artigos
- Pausar/retomar trabalho em artigos
- Criar novo artigo

### 7.2 Fluxo de Sessão de Trabalho

#### Início de Sessão

```
[Usuário abre Produtor Científico]

Sistema: "Olá! Quer continuar trabalhando no artigo 
         'Impacto de LLMs' ou começar algo novo?"

Usuário: "Continuar"

Sistema: [carrega contexto via core]
         "Você estava refinando argumento sobre métricas.
          Última sessão: discutimos throughput vs qualidade.
          Quer continuar daí?"
```

#### Durante Sessão

```
[Conversa fluida]
[Dashboard atualiza em tempo real]
[Sistema cristaliza ideias silenciosamente]
[Usuário pode ver bastidores se quiser]
```

#### Fim de Sessão

```
Usuário: "Quero encerrar sessão"

Sistema: "Resumo da sessão de hoje:
          - Refinamos métricas de produtividade
          - Validamos argumento 1 (aprovado pelo Metodologista)
          - Pendências: buscar evidências sobre turnover
          
          Status do artigo: 65% completo
          - Introdução: rascunho V2
          - Metodologia: 80% definida
          - Resultados: aguardando coleta
          
          Salvei tudo. Até a próxima!"
```

## 8. Integração com Core

### 8.1 O Que Produtor Científico NÃO Reimplementa

Produtor Científico consome as funcionalidades do core universal:

❌ Detecção de conceitos (core faz)  
❌ Extração de argumentos (core faz)  
❌ Validação lógica (agentes do core fazem)  
❌ Conversação socrática (orquestrador do core faz)  

### 8.2 O Que Produtor Científico ADICIONA

Produtor Científico adiciona funcionalidades específicas para produção acadêmica:

✅ Entidade `Article` (agregador)  
✅ Seções estruturadas (Intro, Metodo, ...)  
✅ Interface de chat + dashboard  
✅ Compilação de artigo final  
✅ Export (PDF, DOCX)  

## Referências

- `core/docs/vision/system_philosophy.md` - Filosofia universal
- `core/docs/vision/conversation_mechanics.md` - Mecânica de conversação
- `products/produtor-cientifico/docs/vision/agent_personas.md` - Customização de agentes

