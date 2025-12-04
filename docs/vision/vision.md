## Visão de Produto

## 1. Visão Geral do Produto
- **O que é**: Paper Agent é um sistema multi-agente que ajuda pesquisadores a transformar ideias em artigos publicáveis por meio de ciclos colaborativos de refinamento.
- **Para quem**: Destinado a pesquisadores acadêmicos (mestrandos, doutorandos, coordenadores de grupo) que precisam estruturar produção científica de forma consistente.
- **Problema resolvido**: Reduz a distância entre uma ideia inicial e um manuscrito publicável, guiando definição de problema, metodologia, estrutura e redação.
- **Diferencial**: Orquestra agentes inteligentes e adaptáveis que ajustam o fluxo conforme tipo de artigo e maturidade da pesquisa; não segue scripts rígidos nem respostas determinísticas.

### Filosofia Epistemológica
Paper Agent é guiado por uma epistemologia específica: não existe verdade absoluta, apenas narrativas com diferentes graus de sustentação. Isso significa:
- Sistema não julga verdade, mapeia sustentação
- Proposições têm solidez (não são "verdadeiras" ou "falsas")
- Pesquisa fortalece/enfraquece, não valida/refuta
- Ver detalhes em `docs/vision/epistemology.md`

### 1.1 Posicionamento e Diferencial

Paper Agent não compete com LLMs generalistas. É um sistema especializado para **organização de pensamentos** e **construção de argumentos sólidos**.

**O que fazemos:**
- Lapidar UMA ideia por conversa (não responder curiosidades gerais)
- Fortalecer argumentos identificando premissas e suposições ocultas
- Provocar reflexão sobre aspectos não contemplados no primeiro momento
- Conectar dúvidas com pesquisas direcionadas (quando Pesquisador estiver implementado)
- Colocar à prova o que usuário acha que sabe

**O que NÃO fazemos:**
- Responder curiosidades sobre conhecimento geral da internet
- Fornecer informação enciclopédica
- Ser assistente genérico para tarefas diversas

**Como funciona (dialética):**
Sistema atua como mestre socrático: faz perguntas que expõem suposições não examinadas, oferece contra-exemplos, provoca refinamento. Usuário articula melhor à medida que sistema estrutura e valida.

### Equipe de Especialistas Visível

Diferente de LLMs generalistas (caixa preta), Paper Agent expõe 
sua "equipe interna" de especialistas:

- **Orquestrador:** Provoca reflexão, expõe suposições implícitas
- **Estruturador:** Organiza ideias, cristaliza argumentos
- **Metodologista:** Valida rigor científico

Cada agente tem papel claro. Usuário vê QUEM está trabalhando 
e POR QUÊ, não apenas o resultado final.

**Visão futura (Épico 18+):** Agentes customizáveis como "personas" 
(Sócrates, Aristóteles, Popper) com estilos de argumentação 
personalizados. Ver: docs/vision/agent_personas.md

**Resultado esperado:**
"Flecha penetrante" / "Ideia irresistível" - argumento sólido com respaldo bibliográfico, sem premissas frágeis, sem dúvidas não examinadas. Às vezes o usuário nem sabe onde quer chegar, mas ao elaborar, a clareza aparece.

**Ver detalhes sobre evolução cognitiva em:** `docs/product/cognitive_model.md`

### 1.2 Super-Sistema: Core Universal

> **Nota:** Para arquitetura completa do super-sistema, consulte `docs/architecture/super_system_vision.md`.

Paper Agent não é apenas um produto isolado. É a **primeira aplicação** de um super-sistema com core universal que serve múltiplos produtos.

**Produtos planejados:**
- **Paper-agent:** Auxílio em produção científica (atual)
- **Fichamento:** Catálogo de livros com ideias extraídas (futuro próximo)
- **Rede Social:** Conexão por cosmovisões compartilhadas (futuro distante)

**Core compartilhado:**
- Ontologia (Conceito, Ideia, Argumento)
- Modelo cognitivo (claim → fundamentos (com solidez variável))
- Agentes (Orquestrador, Estruturador, Metodologista, Pesquisador)
- Infraestrutura (LangGraph, ChromaDB, embeddings)

Produtos são **serviços desacoplados** que consomem core via APIs.

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
Orquestrador: "Para buscar papers, preciso fazer chamadas de API que podem ter 
               custo. Quer que eu chame o Pesquisador agora?"
↓
Usuário: "Sim"
↓
Pesquisador: busca papers, realiza síntese
↓
Orquestrador: "Temos uma boa base de papers. Para compilar a revisão completa, 
               preciso fazer chamadas de API que podem ter custo. Quer que eu 
               chame o Escritor para compilar agora, ou prefere revisar os papers primeiro?"
↓
Usuário: "Compilar"
↓
Escritor: compila revisão
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
Estruturador: organiza argumentação
↓
Orquestrador: "Argumento estruturado! Quer que eu chame o Escritor para 
               redigir o artigo teórico?"
↓
Usuário: "Sim"
↓
Escritor: redige artigo teórico
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
Sistema: "Levantamento oficial exige < 2%. Quer que eu pesquise se drones conseguem?"
↓
[Claim evoluiu: "Tecnologia ajuda obras" → "Drones com visão computacional 
 podem medir volumes com precisão suficiente para levantamento oficial"]
```

## 4. Entidade Central: Ideia

> **Nota:** Para estrutura de dados completa, consulte `docs/architecture/idea_model.md`.
> Para ontologia (O que é Ideia?), consulte `docs/architecture/ontology.md`.

A unidade de trabalho que atravessa todo o fluxo é a **Ideia** (anteriormente chamada "Tópico").

```python
Ideia:
  - id: UUID
  - title: "Cooperação humana via mitos"
  - concepts: [concept_ids]        # Conceitos que usa
  - arguments: [argument_ids]      # Argumentos que possui
  - context: {source_type, source, ...}
  - status: "exploring" | "structured" | "validated"
```

**Evolução fluida:**
- Usuário pode retroceder/avançar etapas
- Status evolui organicamente (não imposto)
- Ideia pode ter múltiplos argumentos (diferentes lentes)

**Para paper-agent:**
- Artigo agrega múltiplas ideias
- Cada ideia tem seus próprios argumentos
- Dashboard mostra evolução em tempo real

### Ideia Madura → Conteúdo
Quando uma ideia atinge maturidade (fundamentos sólidos, poucas questões abertas):
1. Usuário acessa ideia e clica "Criar Conteúdo"
2. Abre chat para definir expectativas (formato, tom, ênfase)
3. Orquestrador chama Escritor
4. Conteúdo gerado a partir de metadados já elaborados (claim, fundamentos, evidências)

Formatos possíveis:
- Artigo acadêmico
- Post de blog/LinkedIn
- Thread de Twitter
- Apresentação

## 5. Interação com Usuário
- **Interface web conversacional** como experiência principal (Streamlit)
- Conversação em linguagem natural; sistema **negocia necessidades** sem impor classificações determinísticas
- CLI mantido como ferramenta auxiliar para desenvolvimento e automação
- Sistema **não detecta tipo de artigo automaticamente** no início; tipo emerge da conversa.
- Perguntas dinâmicas e abertas para co-construir entendimento do que usuário precisa.
- Transparência: interface exibe agentes acionados e suas justificativas (video reasoning ou logs resumidos).
- Sessões vinculadas a uma única ideia; o usuário pode pausar e retomar posteriormente.
- Suporte a múltiplas ideias ativas, processadas uma por vez para preservar contexto.
- Usuário mantém voto de minerva: pode aceitar, ajustar ou rejeitar recomendações; preferências alimentam o Orquestrador.

### 5.1 Princípios de Conversação

**Sistema começa sem suposições:**
- Não classifica tipo de artigo automaticamente no início
- Não detecta estágio upfront
- Começa com perguntas abertas para entender contexto

**Negociação contínua:**
- Sistema sugere próximos passos mas usuário decide
- "Posso chamar o Metodologista para validar?" vs "Vou chamar o Metodologista"
- Oferece opções: "Podemos A, B ou C. O que prefere?"

**Detecção emergente:**
- Tipo de artigo emerge da conversa (não é classificado upfront)
- Estágio evolui organicamente conforme artefatos acumulam
- Sistema infere contexto mas não impõe classificações rígidas

**Mudança de direção é natural:**
- Usuário pode voltar/avançar livremente
- "Na verdade, quero fazer revisão de literatura" → sistema adapta
- Decisões anteriores não prendem o fluxo

**Perguntas esclarecedoras >> classificações:**
- "O que você quer entender sobre X?" >> "Detectei que é empírico"
- "Como você imagina investigar isso?" >> "Classifiquei como semi_formed"
- Conversa guia, não rotula

**Exemplo de início de conversa:**
```
❌ Sistema: "Detectei que seu input é vago. Vou estruturar."
✅ Sistema: "Interessante! Me conta mais: você quer VER o que já existe 
           sobre isso, ou quer TESTAR uma hipótese sua?"
```

### 5.2 Interface Web: Chat + Bastidores

**Experiência principal:**
- Interface web (Streamlit) como ponto de entrada do sistema
- Chat limpo e focado (similar ao Claude)
- Painel "Bastidores" opcional para ver reasoning dos agentes

**Navegação: Ideias como Centro**

> **Nota:** Para filosofia completa de navegação, consulte `docs/interface/navigation_philosophy.md`.

**Estrutura principal:**
- **Minhas Ideias** = navegação principal (destaque)
- **Histórico** = conversas passadas (secundário)
- **Biblioteca** = conceitos (acessível via menu)
- **Suposições** = proposições de baixa solidez (futuro)

**Menu minimalista (fechado por padrão):**
```
[Menu ☰]              [Chat Principal]
```

Menu expandido:
```
├── 💡 Minhas Ideias (principal)
├── 🕐 Histórico de conversas
├── 📚 Biblioteca de conceitos
└── ❓ Suposições (futuro)
```

**Dentro de cada Ideia:**
- Iniciar novo chat
- Ver conversas passadas associadas
- Criar conteúdo (se ideia madura)
- Ver fundamentos e sua solidez

**Feedback Visual Forte:**
- Input desabilitado durante processamento (opacidade 50%)
- Barra inline: "🤖 Sistema pensando..."
- Texto dinâmico conforme agente ativo:
  - "⚡ Analisando sua mensagem..."
  - "🎯 Orquestrador pensando..."
  - "📝 Estruturador organizando..."
  - "🔬 Metodologista validando..."
- Animação suave ao habilitar/desabilitar input

**Layout consolidado:**
```
┌─────────────────────────────────────────────────┐
│  [Sidebar]           [Chat Principal]           │
│                                                 │
│  💬 Conversas         Você: "..."               │
│  • Conv 1 (ativa)     💰 $0.0012                │
│  • Conv 2 (2h atrás)                            │
│                       Sistema: "..."            │
│  [+ Nova Conversa]    [digitando...]            │
│  [📖 Pensamentos]                               │
│  [🏷️ Catálogo]       [🔍 Bastidores →]         │
└─────────────────────────────────────────────────┘
```

**Transparência diferencial:**
- Ver agentes pensando: Reasoning inline ou modal
- Tempo real: Eventos via polling (1s)
- 3 níveis: Inline (discreto) → Resumido (280 chars) → Completo (modal)

**Agentes Visíveis:**
- Sistema mostra qual agente está ativo
- Raciocínio resumido por agente
- Diferencial: usuário entende QUE tipo de análise está sendo feita

### 5.3 CLI: Ferramenta de Desenvolvimento

**Papel secundário:**
- Interface de linha de comando mantida para desenvolvimento e automação
- Útil para testes, debugging, scripts automatizados
- Funcionalidade congelada (não recebe features novas)
- Backend compartilhado com interface web (LangGraph + EventBus)

**Quando usar CLI:**
- ✅ Testes automatizados (CI/CD)
- ✅ Debugging de agentes
- ✅ Validação rápida de prompts
- ✅ Scripts de automação
- ❌ Uso interativo por usuários finais (usar web)

**Documentação:** Ver `docs/interface/cli.md` e `docs/interface/web.md`

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
- **Epistemologicamente honesto**: não existe verdade absoluta; sistema mapeia graus de sustentação baseados em evidências, não julgamentos binários de verdade/falsidade.

## Referências Adicionais

- `docs/architecture/super_system_vision.md` - Arquitetura do super-sistema
- `docs/architecture/ontology.md` - O que é Conceito, Ideia, Argumento
- `docs/product/cognitive_model.md` - Como pensamento evolui
- `docs/products/paper_agent.md` - Produto específico paper-agent
- `docs/vision/epistemology.md` - Filosofia epistemológica do sistema

