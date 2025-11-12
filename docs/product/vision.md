## Visão de Produto

## 1. Visão Geral do Produto
- **O que é**: Paper Agent é um sistema multi-agente que ajuda pesquisadores a transformar ideias em artigos publicáveis por meio de ciclos colaborativos de refinamento.
- **Para quem**: Destinado a pesquisadores acadêmicos (mestrandos, doutorandos, coordenadores de grupo) que precisam estruturar produção científica de forma consistente.
- **Problema resolvido**: Reduz a distância entre uma ideia inicial e um manuscrito publicável, guiando definição de problema, metodologia, estrutura e redação.
- **Diferencial**: Orquestra agentes inteligentes e adaptáveis que ajustam o fluxo conforme tipo de artigo e maturidade da pesquisa; não segue scripts rígidos nem respostas determinísticas.

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
### Cenário A: Ideia Vaga (Empírico)
```
Usuário: "Observei que LLMs aumentam produtividade"
↓
Sistema detecta: tipo empírico, maturidade baixa
↓
Estruturador V1: "Como LLMs impactam produtividade?"
↓
Metodologista: needs_refinement (falta população, métricas)
↓
Estruturador V2: "Como LLMs (ex.: Claude Code) reduzem tempo de desenvolvimento em 30%, medido por sprints, em equipes de 2-5 devs?"
↓
Metodologista: approved
↓
[Sistema sugere] Próximo passo: definir desenho experimental
```

### Cenário B: Questão para Revisão
```
Usuário: "Quero entender o estado da arte em multi-agente para escrita acadêmica"
↓
Sistema detecta: tipo revisão, maturidade média
↓
Orquestrador: "Vou estruturar protocolo de revisão"
↓
Estruturador: define questão PICO/SPIDER
↓
Pesquisador: busca papers, realiza síntese
↓
Escritor: compila revisão
```

### Cenário C: Framework Teórico
```
Usuário: "Proponho modelo de governança para sistemas multi-agente"
↓
Sistema detecta: tipo teórico, maturidade alta
↓
Orquestrador: "Vou validar lógica e estrutura do framework"
↓
Metodologista: valida consistência lógica
↓
Estruturador: organiza argumentação
↓
Escritor: redige artigo teórico
```

## 4. Entidade Central: Tópico/Ideia
- Representa a unidade de trabalho que atravessa todo o fluxo de pesquisa e escrita.
- Serve como contêiner de contexto para agentes e para persistência de sessão.
- Pode ser criado pelo usuário ou inferido pelo sistema a partir da primeira interação.

```
Tópico:
  - id: UUID
  - title: "Impacto de LLMs em produtividade"
  - article_type: "empirical" | "review" | "theoretical" | "case_study" | "meta_analysis" | "methodological"
  - stage: "ideation" | "hypothesis" | "methodology" | "research" | "writing" | "review" | "done"
  - created_at: timestamp
  - updated_at: timestamp
  - artifacts: [outline, papers, drafts, decisions]
  - thread_id: LangGraph thread (para recuperar sessão)
```

- **Evolução fluida**: o usuário pode retroceder etapas; o tipo pode ser inferido ou ajustado; estágio é detectado pelo Orquestrador com base em artefatos e interações.

## 5. Interação com Usuário
- Conversação em linguagem natural; sistema infere necessidades sem depender de comandos explícitos.
- Perguntas dinâmicas para definir tipo de artigo, maturidade e lacunas.
- Transparência: interface exibe agentes acionados e suas justificativas (video reasoning ou logs resumidos).
- Sessões vinculadas a um único tópico; o usuário pode pausar e retomar posteriormente.
- Suporte a múltiplos tópicos ativos, processados um por vez para preservar contexto.
- Usuário mantém voto de minerva: pode aceitar, ajustar ou rejeitar recomendações; preferências alimentam o Orquestrador.

## 6. Casos de Uso Principais
- **UC1: Validar Ideia** – De uma observação vaga para uma hipótese testável ou descarte fundamentado.
- **UC2: Estruturar Argumentação** – Transformar ideia parcial em outline coerente com checkpoints revisados.
- **UC3: Pesquisar Literatura** – Gerar síntese de papers relevantes com rastreabilidade das fontes.
- **UC4: Escrever Artigo** – Converter artefatos consolidados em manuscrito no estilo do usuário.
- **UC5: Revisar Artigo** – Analisar rascunho e produzir feedback estruturado com ações recomendadas.

## 7. Princípios de Design
- **Inteligente, não determinístico**: adapta fluxos e respostas conforme contexto em vez de seguir roteiros fixos.
- **Colaborativo**: agentes constroem junto ao pesquisador, estimulando coautoria e reflexão crítica.
- **Transparente**: reasoning dos agentes exposto, integrando explicações curtas ou links para aprofundamento.
- **Incremental**: começa com entregáveis mínimos e expande funcionalidades à medida que aprende com o uso.
- **Escalável**: arquitetura previsa integração de novos tipos de artigo, agentes e extensões (ver `ARCHITECTURE.md` para detalhes técnicos).

