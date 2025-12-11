# Paper-Agent - Produto

> **Nota:** Este documento descreve o produto paper-agent especificamente.
> Para core universal compartilhado, consulte `core/docs/architecture/vision/super_system.md`.
> Para ontologia base, consulte `core/docs/architecture/data-models/ontology.md`.

## Visão Geral

Paper-agent é **serviço desacoplado** que consome core universal para auxiliar em produção científica.

**O que faz:**
- Converte ideias vagas em hipóteses testáveis
- Organiza argumentos com rigor científico
- Compila artigos estruturados

**O que NÃO faz:**
- Não é assistente genérico (não responde curiosidades)
- Foco: lapidar UMA ideia por conversa

## Entidades Específicas do Paper-Agent

### Article (Agregador de Ideias)

Paper-agent adiciona entidade `Article` sobre core:

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

### Section (Parte do Artigo)

```python
Section:
  id: UUID
  article_id: UUID
  name: str                     # "Introdução", "Metodologia"
  ideas: list[UUID]             # Ideias usadas nesta seção
  content: str                  # Texto compilado
  status: str                   # "pending", "draft", "reviewed"
```

### Como Article Consome Core

```python
# Paper-agent chama core via API
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

## Interface: Chat + Dashboard + Bastidores

### Chat Principal (60% tela)

**Experiência:**
- Conversa fluida (como Claude)
- Sistema cristaliza ideias silenciosamente
- Métricas inline discretas (tokens, custo, tempo)

```
Você: "Observei que LLMs aumentam produtividade"
💰 $0.0012 · 215 tokens · 1.2s

Sistema: "Interessante! Me conta mais: você quer VER 
         o que já existe ou TESTAR uma hipótese?"
[digitando...]
```

### Dashboard em Tempo Real (40% tela - collapsible)

**O que mostra:**

```
Ideias identificadas (até agora):
  
  1. Impacto de LLMs em produtividade [85% confiança]
     ├─ Conceitos: LLMs, Produtividade
     ├─ Argumentos: 1 identificado
     └─ Status: Estruturando...
     
Conceitos mencionados:
  - LLMs (central)
  - Produtividade (central)
  - Desenvolvimento (periférico)
```

### Bastidores (Modal)

**3 abas:**
1. **Raciocínio:** Reasoning completo dos agentes
2. **Timeline:** Histórico de eventos
3. **Métricas:** Tokens, custos, tempo

## Fluxo: Sessão de Trabalho

### Início de Sessão

```
[Usuário abre paper-agent]

Sistema: "Olá! Quer continuar trabalhando no artigo 
         'Impacto de LLMs' ou começar algo novo?"

Usuário: "Continuar"

Sistema: [carrega contexto via core]
         "Você estava refinando argumento sobre métricas.
          Última sessão: discutimos throughput vs qualidade.
          Quer continuar daí?"
```

### Durante Sessão

```
[Conversa fluida]
[Dashboard atualiza em tempo real]
[Sistema cristaliza ideias silenciosamente]
[Usuário pode ver bastidores se quiser]
```

### Fim de Sessão

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

## Sidebar: Gestão de Artigos

**Últimos 10 artigos:**

```
📄 Impacto de LLMs (ativo)
📄 Semana de 4 dias (pausado)
📄 Automação com IA (pausado)
...
```

**Usuário pode:**
- Alternar entre artigos
- Pausar/retomar
- Criar novo artigo

## Integração com Core

### Paper-Agent NÃO reimplementa:

❌ Detecção de conceitos (core faz)  
❌ Extração de argumentos (core faz)  
❌ Validação lógica (agentes do core fazem)  
❌ Conversação socrática (orquestrador do core faz)  

### Paper-Agent ADICIONA:

✅ Entidade `Article` (agregador)  
✅ Seções estruturadas (Intro, Metodo, ...)  
✅ Interface de chat + dashboard  
✅ Compilação de artigo final  
✅ Export (PDF, DOCX)  

## Referências

- `core/docs/architecture/vision/super_system.md` - Arquitetura core → produtos
- `core/docs/architecture/data-models/idea_model.md` - Ideias que Article agrega
- `products/revelar/docs/vision.md` - Visão geral do produto
- `docs/interface/web/` - Especificação técnica da interface (overview.md, components.md, flows.md)

