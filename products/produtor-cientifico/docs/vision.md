# Visão de Produto - Produtor Científico

> **Nota:** Para filosofia universal do sistema, consulte `core/docs/vision/system_philosophy.md`.

## 1. Visão Geral do Produto

- **O que é**: Especialização de Expressão para produção de artigos acadêmicos
- **Para quem**: Pesquisadores acadêmicos (mestrandos, doutorandos, professores)
- **Problema resolvido**: Transformar mensagem estruturada em artigo científico publicável
- **Diferencial**: Agentes especializados por tipo de artigo + validação metodológica + estrutura acadêmica
- **Input**: Mensagem (de Camadas da Linguagem)
- **Output**: Artigo acadêmico

## 2. Posição no Pipeline

Produtor Científico é uma **especialização de Expressão** para artigos acadêmicos.

```
┌─────────────┐     ┌─────────────────────────┐     ┌───────────────────────┐
│   Revelar   │────▶│  Camadas da Linguagem   │────▶│      Expressão        │
└─────────────┘     └─────────────────────────┘     └───────────────────────┘
      │                        │                              │
      ▼                        ▼                    ┌─────────┴─────────┐
    IDEIA                  MENSAGEM                 ▼                   ▼
                                               (genérico)    Produtor Científico
                                                                    │
                                                                    ▼
                                                            ARTIGO ACADÊMICO
```

### O Que Herda de Expressão

- Recebe Mensagem estruturada
- Transforma em conteúdo com forma

### O Que Adiciona

- Estrutura específica de artigo (Introdução, Metodologia, Resultados...)
- Validação metodológica integrada
- Tipos de artigo acadêmico (empírico, revisão, teórico...)
- Formatação para publicação

## 3. Tipos de Artigo Acadêmico

### 3.1 Empírico/Experimental

- **Características distintivas**: Testa hipóteses com dados coletados; foca em delineamentos experimentais ou quasi-experimentais (ex.: RCT, coorte, A/B tests).
- **Checkpoints mínimos**: Hipótese clara → Definição de população/métricas → Desenho metodológico → Plano de coleta/análise → Interpretação dos resultados.
- **Agentes relevantes**: Metodologista (define desenho), Estruturador (formaliza hipótese), Orquestrador (coordena etapas), Escritor (tradução para manuscrito).

### 3.2 Revisão Sistemática/Literatura

- **Características distintivas**: Sintetiza conhecimento existente com protocolos estruturados (ex.: systematic review, scoping review); foco em transparência e reprodutibilidade.
- **Checkpoints mínimos**: Questão de pesquisa (PICO/SPIDER) → Estratégia de busca → Critérios de inclusão/exclusão → Extração/síntese → Conclusões e lacunas.
- **Agentes relevantes**: Orquestrador (define fluxo), Estruturador (formaliza protocolo), Pesquisador (execução da busca externa), Escritor (compila síntese).

### 3.3 Teórico/Conceitual

- **Características distintivas**: Propõe frameworks, modelos ou argumentos conceituais (ex.: modelos teóricos, argumentação filosófica).
- **Checkpoints mínimos**: Problema conceitual → Revisão crítica → Construção lógica → Proposição de framework → Discussão de implicações/limitações.
- **Agentes relevantes**: Estruturador (arquitetura do argumento), Metodologista (validação lógica), Escritor (articulação textual), Orquestrador (mantém coerência global).

### 3.4 Estudo de Caso

- **Características distintivas**: Analisa casos específicos com profundidade contextual (ex.: case study, etnografia).
- **Checkpoints mínimos**: Seleção do caso → Contextualização → Coleta de evidências → Análise interpretativa → Extração de insights e generalizações prudentes.
- **Agentes relevantes**: Metodologista (define protocolo qualitativo), Estruturador (organiza narrativa), Orquestrador (sincroniza revisões), Escritor (relato final).

### 3.5 Meta-Análise

- **Características distintivas**: Combina quantitativamente resultados de múltiplos estudos (ex.: meta-analysis, meta-regression).
- **Checkpoints mínimos**: Questão quantitativa → Busca sistemática → Extração de dados → Análise estatística (modelos/heterogeneidade) → Interpretação dos efeitos.
- **Agentes relevantes**: Metodologista (modelos estatísticos), Orquestrador (governa rigor), Estruturador (estrutura protocolo), Escritor (relata resultados).

### 3.6 Metodológico

- **Características distintivas**: Propõe ou valida novos métodos, instrumentos ou pipelines (ex.: validation study, method comparison).
- **Checkpoints mínimos**: Definição do método → Critérios de avaliação → Coleta/benchmark → Análise comparativa → Discussão de limitações/aplicabilidade.
- **Agentes relevantes**: Metodologista (constrói validação), Estruturador (documenta passo a passo), Orquestrador (assegura cobertura), Escritor (formaliza resultados).

## 4. Jornada do Usuário

> **💡 Nota de Interface:** Todos os cenários abaixo ocorrem na interface web conversacional. CLI mantém mesma funcionalidade mas é ferramenta auxiliar para desenvolvimento.

### Cenário: Produzir Artigo

```
[Usuário vem de Camadas da Linguagem com Mensagem pronta]

Usuário: "Quero transformar essa mensagem em artigo acadêmico"
↓
Sistema: "Ótimo! Que tipo de artigo?
         - Empírico/Experimental
         - Revisão de Literatura
         - Teórico/Conceitual
         - Estudo de Caso
         - Meta-Análise
         - Metodológico"
↓
Usuário: "Empírico"
↓
Sistema: "Para artigo empírico, vou estruturar:
         - Introdução (contexto + hipótese)
         - Metodologia (desenho + métricas)
         - Resultados (dados + análise)
         - Discussão (interpretação + limitações)
         
         Sua mensagem já tem os argumentos organizados.
         Vou distribuí-los nas seções. Quer revisar?"
[Bastidores: 📝 Estruturador distribuiu argumentos → 🔬 Metodologista validou estrutura]
↓
Usuário: "Sim, mas preciso ajustar a metodologia"
↓
Sistema: "Ajustei a metodologia conforme suas especificações: [nova metodologia].
         A estrutura agora reflete seu desenho experimental. Quer gerar o manuscrito?"
[Bastidores: 🔬 Metodologista ajustou → 🎯 Orquestrador curou]
↓
Usuário: "Sim"
↓
Sistema: "Gerado artigo completo: [artigo estruturado]. Quer exportar em PDF, DOCX ou LaTeX?"
[Bastidores: ✍️ Escritor compilou → 🎯 Orquestrador curou]
```

## 5. Da Mensagem ao Manuscrito

Quando usuário chega com Mensagem estruturada (de Camadas da Linguagem):

1. Usuário escolhe tipo de artigo
2. Sistema propõe estrutura de seções
3. Sistema distribui argumentos/evidências nas seções
4. Usuário revisa e ajusta
5. Sistema gera manuscrito
6. Export (PDF, DOCX, LaTeX)

## 6. Casos de Uso Principais

- **UC1: Produzir Artigo de Revisão** – Transformar mensagem em artigo de revisão de literatura com protocolo estruturado (PICO/SPIDER) e síntese.
- **UC2: Escrever Artigo Teórico** – Compilar mensagem em manuscrito teórico completo com validação lógica.
- **UC3: Compilar Manuscrito Empírico** – Distribuir argumentos da mensagem em estrutura empírica (Introdução, Metodologia, Resultados, Discussão).
- **UC4: Revisar Metodologia** – Analisar desenho metodológico proposto e produzir feedback estruturado com ações recomendadas para rigor científico.

## 7. Entidades do Produto

Produtor Científico adiciona entidades específicas sobre o core universal para gerenciar artigos acadêmicos. Essas entidades especializam a produção de conteúdo da Expressão para o formato acadêmico.

### 7.1 Article (Estrutura de Artigo)

Article é a entidade central que estrutura uma Mensagem em artigo científico:

```python
Article:
  id: UUID
  title: str                    # "Impacto de LLMs em Produtividade"
  message_id: UUID              # Mensagem (de Camadas da Linguagem) que originou o artigo
  
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

### 7.2 Section (Parte do Artigo)

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

### 7.3 Como Article Consome Mensagem

Produtor Científico recebe Mensagem do core (gerada por Camadas da Linguagem) e estrutura em artigo:

```python
# Produtor Científico recebe mensagem de Camadas da Linguagem
message = core_api.get_message(message_id)

# Criar artigo a partir da mensagem
article = Article(
  title="Impacto de LLMs",
  message_id=message.id,  # Referência à mensagem
  article_type="empirical"
)

# Distribuir argumentos da mensagem nas seções
sections = structure_message_to_sections(
  message=message,
  article_type="empirical"
)
```

## 8. Interface: Gestão de Artigos

### 8.1 Sidebar: Gestão de Artigos

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

### 8.2 Fluxo de Sessão de Trabalho

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

## 9. Integração com Pipeline

### 9.1 Relação com Expressão

Produtor Científico é especialização de Expressão:
- Herda capacidade de receber Mensagem e produzir conteúdo
- Adiciona lógica específica para artigos acadêmicos
- Compartilha infraestrutura com Expressão

### 9.2 O Que Produtor Científico NÃO Faz

❌ Criar clareza de ideias (isso é Revelar)  
❌ Extrair conceitos de textos (isso é Prisma Verbal)  
❌ Estruturar argumentos em mensagem (isso é Camadas da Linguagem)  
❌ Produzir outros formatos como post/email (isso é Expressão genérico)

### 9.3 O Que Produtor Científico ADICIONA sobre Expressão

✅ Tipos de artigo acadêmico (empírico, revisão, teórico...)  
✅ Estrutura de seções (Introdução, Metodologia, Resultados...)  
✅ Validação metodológica integrada  
✅ Formatação para publicação (ABNT, APA, Vancouver...)  
✅ Export especializado (LaTeX, templates de journals)  

## Referências

- `core/docs/vision/system_philosophy.md` - Filosofia universal
- `core/docs/vision/super_system.md` - Arquitetura do super-sistema
- `products/camadas-da-linguagem/docs/vision.md` - Produto anterior no pipeline
- `products/expressao/docs/vision.md` - Produto base (Produtor Científico é especialização)
- `products/revelar/docs/vision.md` - Produto de clareza (etapa anterior)
- `products/produtor-cientifico/docs/vision/agent_personas.md` - Customização de agentes

