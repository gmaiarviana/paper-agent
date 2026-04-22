# Visão de Produto - Revelar

> **Nota:** Para filosofia universal do sistema, consulte `core/docs/vision/system_philosophy.md`.

## 1. Visão Geral do Produto Revelar

- **O que é**: Sistema conversacional para estruturar pensamentos nebulosos em conceitos claros
- **Para quem**: Pessoas que precisam clareza sobre hipóteses, ideias, constatações (qualquer domínio)
- **Problema resolvido**: Transformar confusão mental em entendimento estruturado
- **Diferencial**: Chat conversacional com agentes visíveis, foco na jornada de clareza

### Output do Revelar
- ✅ Clareza mental sobre o que você realmente quer dizer
- ✅ Ideia estruturada (conjunto de argumentos)
- ✅ Rede de conceitos conectados
- ✅ Fundamentos com solidez avaliada
- ❌ NÃO estrutura mensagens (isso é Camadas da Linguagem)
- ❌ NÃO produz conteúdo final (isso é Expressão)

**Próximo passo:** Usuário pode levar Ideia para Camadas da Linguagem para estruturar comunicação.

**Metáfora:** Revelar é o "ateliê de lapidação" onde você refina ideias brutas até ficarem cristalinas. A produção de conteúdo final (artigos, posts, relatórios) acontece em outros produtos.

### 1.1 Posição no Pipeline

Revelar é a **Etapa 1 do pipeline** - responsável por clareza.

```
┌─────────────┐     ┌─────────────────────────┐     ┌───────────┐
│   REVELAR   │────▶│  Camadas da Linguagem   │────▶│ Expressão │
│  (clareza)  │     │    (estruturação)       │     │  (forma)  │
└─────────────┘     └─────────────────────────┘     └───────────┘
      │                        │                          │
      ▼                        ▼                          ▼
    IDEIA                  MENSAGEM                   CONTEÚDO
```

**Entradas:**
- Usuário com pensamento confuso ou ideia vaga
- Diálogo socrático para chegar na clareza

**Saídas:**
- Ideia estruturada (conjunto de argumentos)
- Conceitos identificados (alimentam biblioteca global)
- Pronto para ir a Camadas da Linguagem (se usuário quiser comunicar)

## 2. Posicionamento e Diferencial

Revelar não compete com LLMs generalistas. É um sistema especializado para **organização de pensamentos** e **construção de clareza conceitual**.

**O que fazemos:**
- Foco em uma coisa por vez (não responder curiosidades gerais)
- Fortalecer argumentos identificando premissas e suposições ocultas
- Provocar reflexão sobre aspectos não contemplados no primeiro momento
- Conectar dúvidas com conceitos relacionados
- Colocar à prova o que usuário acha que sabe

**Sobre "foco em uma coisa por vez":**
O usuário pode estar explorando uma ideia central, mas naturalmente diverge em sub-tópicos e depois converge novamente para aprofundar. O sistema ajuda a identificar quando há múltiplos tópicos simultâneos e sugere organizar, mas não força - respeita o ritmo do usuário. Preferência por trabalhar uma coisa de cada vez, mas sem rigidez. Metáfora: "Como lapidar um diamante - divergir para explorar facetas, convergir para aprofundar o corte"

**O que NÃO fazemos:**
- Responder curiosidades sobre conhecimento geral da internet
- Fornecer informação enciclopédica
- Ser assistente genérico para tarefas diversas
- Produzir artigos científicos (isso é papel do Produtor Científico)

**Como funciona (dialética):**
Sistema atua como mestre socrático: faz perguntas que expõem suposições não examinadas, oferece contra-exemplos, provoca refinamento. Usuário articula melhor à medida que sistema estrutura e valida.

### 2.1 Relevância Multidimensional

Relevância de uma ideia não é binária - é avaliada em múltiplas dimensões:

**Valor Social:**
- Esta ideia agrega valor para sociedade?
- Resolve problema real ou é curiosidade acadêmica?

**Viabilidade de Investimento:**
- Vale a pena investir recursos (tempo, dinheiro) em testar?
- Potencial de impacto justifica esforço?

**Saturação na Literatura:**
- Há muito material relacionado (saturação) ou lacuna clara?
- Se saturada: reformular ângulo ou abandonar
- Se lacuna: oportunidade de contribuição

**Fundamentação:**
- Bases/suposições estão bem sustentadas?
- Proposições têm solidez suficiente?

**Papel do Sistema:**
- Sistema **detecta** e apresenta informações objetivas (ex: "50+ papers nos últimos 2 anos")
- Usuário **julga** relevância final baseado em informações apresentadas
- Sistema pode **alertar** sobre problemas (saturação, bases frágeis) mas não **bloqueia**

**Exemplo:**
Sistema: "Encontrei 50+ papers sobre LLMs em produtividade nos últimos 2 anos.
Literatura está saturada. Quer reformular ângulo (ex: foco em Python)
ou explorar outra ideia?"
Usuário: [julga se vale reformular ou abandonar]

## 3. Equipe de Especialistas Visível

Diferente de LLMs generalistas (caixa preta), Revelar expõe 
sua "equipe interna" de especialistas:

- **Orquestrador:** Provoca reflexão, expõe suposições implícitas
- **Estruturador:** Organiza ideias, cristaliza argumentos

Cada agente tem papel claro. Usuário vê QUEM está trabalhando 
e POR QUÊ, não apenas o resultado final.

**Visão futura (Épico 18+):** Agentes customizáveis como "personas" 
(Sócrates, Aristóteles, Popper) com estilos de argumentação 
personalizados. Ver: `products/produtor-cientifico/docs/vision/agent_personas.md`

## 4. Como Ideias São Gerenciadas

> **Nota:** Para estrutura de dados completa, consulte `core/docs/architecture/data-models/idea_model.md`.
> Para ontologia (O que é Ideia?), consulte `core/docs/architecture/data-models/ontology.md`.

A unidade de trabalho que atravessa todo o fluxo é a **Ideia**.

**Evolução fluida:**
- Usuário pode retroceder/avançar etapas
- Status evolui organicamente (não imposto)
- Ideia pode ter múltiplos argumentos (diferentes lentes)
- Foco na conversa e clareza, não em estrutura formal complexa

**Para Revelar:**
- Cada ideia é uma conversa sobre clareza de pensamento
- Sistema ajuda a identificar conceitos relacionados
- Argumentos informais são estruturados através do diálogo
- Dashboard mostra evolução em tempo real

**Ideia Madura = Clareza Alcançada**
Quando uma ideia atinge clareza suficiente:
1. Usuário vê resumo estruturado (claim, fundamentos, solidez)
2. Pode exportar estrutura simples (markdown, texto)
3. Pode passar para Camadas da Linguagem para estruturar comunicação
4. Foco permanece na clareza, não em formato final

**Fluxo de saída:**
Revelar (clareza) → Camadas da Linguagem (estruturação) → Expressão (forma)

## 5. Interação com Usuário

- **Interface web conversacional** como experiência principal (Streamlit)
- Conversação em linguagem natural; sistema **negocia necessidades** sem impor classificações determinísticas
- CLI mantido como ferramenta auxiliar para desenvolvimento e automação
- Sistema **não detecta tipo de ideia automaticamente** no início; tipo emerge da conversa.
- Perguntas dinâmicas e abertas para co-construir entendimento do que usuário precisa.
- Transparência: interface exibe agentes acionados e suas justificativas (video reasoning ou logs resumidos).
- Sessões vinculadas a uma única ideia; o usuário pode pausar e retomar posteriormente.
- Suporte a múltiplas ideias ativas, processadas uma por vez para preservar contexto.
- Usuário mantém voto de minerva: pode aceitar, ajustar ou rejeitar recomendações; preferências alimentam o Orquestrador.

### 5.1 Princípios de Conversação

**Sistema começa sem suposições:**
- Não classifica tipo de ideia automaticamente no início
- Não detecta estágio upfront
- Começa com perguntas abertas para entender contexto

**Negociação contínua:**
- Agentes trabalham automaticamente quando há contexto suficiente
- Orquestrador faz curadoria da resposta e confirma entendimento: "Isso captura o que você quer?"
- Transparência nos bastidores: usuário vê quem trabalhou (indicadores [Bastidores: ...])
- Usuário pode ajustar/refazer se resultado não capturar intenção
- Sistema ainda oferece opções quando há múltiplos caminhos: "Podemos A, B ou C. O que prefere?"

**Detecção emergente:**
- Tipo de ideia emerge da conversa (não é classificado upfront)
- Estágio evolui organicamente conforme artefatos acumulam
- Sistema infere contexto mas não impõe classificações rígidas

**Mudança de direção é natural:**
- Usuário pode voltar/avançar livremente
- "Na verdade, quero explorar outro aspecto" → sistema adapta
- Decisões anteriores não prendem o fluxo

**Perguntas esclarecedoras >> classificações:**
- "O que você quer entender sobre X?" >> "Detectei que é empírico"
- "Como você imagina investigar isso?" >> "Classifiquei como semi_formed"
- Conversa guia, não rotula

**Exemplo de início de conversa:**
```
❌ Sistema: "Detectei que seu input é vago. Vou estruturar."
✅ Sistema: "Interessante! Me conta mais: você quer entender melhor 
           essa ideia, ou quer explorar conexões com outros conceitos?"
```

### 5.2 Interface Web: Chat + Bastidores

**Experiência principal:**
- Interface web (Streamlit) como ponto de entrada do sistema
- Chat limpo e focado (similar ao Claude)
- Painel "Bastidores" opcional para ver reasoning dos agentes

**Navegação: Ideias como Centro**

> **Nota:** Para filosofia completa de navegação, consulte `products/revelar/docs/interface/navigation_philosophy.md`.

**Estrutura principal:**
- **Minhas Ideias** = navegação principal (destaque)
- **Catálogo** = conceitos reutilizáveis (referência)
- **Histórico** = conversas passadas (secundário)

**Sidebar minimalista:**
```
├── 📖 Pensamentos
├── 🏷️ Catálogo
├── 💬 Conversas
└── [+ Nova conversa]
```

**Dentro de cada Ideia:**
- Iniciar novo chat
- Ver conversas passadas associadas
- Ver fundamentos e sua solidez
- Exportar resumo (se ideia madura)

**Feedback Visual Forte:**
- Input desabilitado durante processamento (opacidade 50%)
- Barra inline: "🤖 Sistema pensando..."
- Texto dinâmico conforme agente ativo:
  - "⚡ Analisando sua mensagem..."
  - "🎯 Orquestrador pensando..."
  - "📝 Estruturador organizando..."
- Animação suave ao habilitar/desabilitar input

**Layout consolidado:**
```
┌─────────────────────────────────────────────────────────────────┐
│  [Sidebar]              [Chat]                      [Direita]   │
│                                                                 │
│  📖 Pensamentos         Conversa...           ┌───────────────┐ │
│  🏷️ Catálogo                                 │ 💡 Contexto   │ │
│  💬 Conversas                                 └───────────────┘ │
│  [+ Nova conversa]                            ┌───────────────┐ │
│                                               │📊 Bastidores  │ │
│                                               └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Transparência diferencial:**
- **Contexto:** Informações sobre ideia e conversa (painel direito, acima)
- **Bastidores:** Pensamento dos agentes em tempo real (painel direito, abaixo)
- Ambos são seções colapsáveis, sem toggle separado
- Tempo real: Eventos via polling (1s)

**Agentes Visíveis:**
- Sistema mostra qual agente está ativo nos Bastidores
- Cards de pensamento e timeline exibem raciocínio por agente
- Diferencial: usuário entende QUE tipo de análise está sendo feita

### Bastidores Transparentes

**Diferencial do produto:** mostrar como o sistema pensa, não apenas o resultado final.

**Funcionalidade opt-in:**
- Por padrão, não distrai - chat limpo e focado
- Usuário pode ativar visualização dos bastidores quando quiser entender o raciocínio

**O que mostra:**
- Detecções do Observador (conceitos identificados, conexões encontradas)
- Consultas a Memory (quais informações foram recuperadas e por quê)
- Decisões do Orquestrador (por que determinado agente foi acionado, que caminho foi escolhido)

**Formato:**
- Resumo legível por padrão (não JSON/técnico)
- Opção para aprofundamento técnico quando necessário
- Timeline visual de eventos e raciocínio

**Objetivo:**
Transparência sobre origem de informações e raciocínio do sistema, permitindo ao usuário entender e validar como o sistema chegou às suas conclusões.

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

**Documentação:** Ver `core/docs/tools/cli.md` e `products/revelar/docs/interface/` (overview.md, components.md, flows.md)

## 6. Casos de Uso Principais (Revelar)

- **UC1: Esclarecer Pensamento Confuso** – De uma confusão mental para uma ideia clara e estruturada através do diálogo. Qualquer domínio (negócio, postagem, pesquisa).
- **UC2: Identificar Conceitos Relacionados** – Descobrir conexões entre ideias e conceitos que o usuário não havia percebido.
- **UC3: Estruturar Argumento Informal** – Transformar pensamento parcial em argumento coerente, independente do domínio.
- **UC4: Preparar Hipótese para Próxima Etapa** – Refinar hipótese até estar madura para ser usada em outra ferramenta/processo (ver `use_cases.md` para exemplos específicos).

### 6.3 Convergência com Prisma Verbal

**Infraestrutura Compartilhada:**

Revelar e Prisma Verbal fazem parte do mesmo super-sistema, compartilhando:
- ✅ **Conceitos globais:** Biblioteca única (ChromaDB)
- ✅ **Detecção de solidez:** Coerência, fundamentação, dependências
- ✅ **Rastreamento de proposições:** Genealogia de afirmações

**Diferença de Contexto:**
- **Prisma Verbal:** Extrai proposições de textos estáticos (livros, papers)
- **Revelar:** Co-constrói proposições com usuário (conversa dinâmica)

**Como Funcionam Juntos:**

**Exemplo:**
Usuário articula ideia no Revelar: "Reuniões síncronas aumentam alinhamento"
↓
Revelar detecta conceito: "Coordenação" (biblioteca global)
↓
Sistema sugere: "Isso parece relacionado ao conceito 'Coordenação'
na biblioteca, usado em:
- March & Simon (Teoria Organizacional)
- Scrum/XP (Desenvolvimento Ágil)
- Rosenberg (Comunicação Não-Violenta)
Quer explorar como esses autores abordam coordenação?"
↓
Usuário confirma interesse
↓
Pesquisador aciona Prisma para processar textos relevantes
↓
Revelar apresenta proposições extraídas que fortalecem/enfraquecem ideia do usuário

**Benefício:**
Usuário não está "inventando a roda" - há conhecimento acumulado sob nomenclaturas diferentes.
Sistema conecta o que usuário está articulando com o que já foi dito antes (por outros autores, em outras palavras).

**Essências Transcendem Palavras:**
- "Alinhamento", "coordenação", "sincronização" → mesma essência
- Sistema detecta similaridade semântica via vetores (ChromaDB)
- Biblioteca global cresce com contribuições de Prisma (textos processados) e Revelar (conversas)

**Pipeline Completo:**

Revelar e Prisma Verbal alimentam o mesmo Motor Vetorial:

```
REVELAR ──────┐
(diálogo)     │
              ▼
        ┌─────────────────┐
        │  MOTOR VETORIAL │
        │   (biblioteca)  │
        └─────────────────┘
              ▲
PRISMA  ──────┘
VERBAL
(texto)
              │
              ▼
    CAMADAS DA LINGUAGEM
       (estruturação)
              │
              ▼
         EXPRESSÃO
          (forma)
```

Ambos os produtos:
- Alimentam a biblioteca de conceitos
- Criam Ideias e Argumentos
- Preparam material para Camadas da Linguagem

### Vetorização Futura e Diálogo Socrático

**Clareza Emerge Progressivamente:**

O diálogo socrático do Revelar tem uma implicação direta para vetorização: a clareza conceitual não existe no início - ela é **construída** através da conversa. Isso significa que vetorizar o input inicial seria capturar confusão, não conhecimento.

**Quando Vetorizar:**
- ❌ Input inicial: "Acho que LLMs aumentam produtividade" (nebuloso)
- ❌ Durante refinamento: ideia ainda em transformação
- ✅ Snapshot maduro: argumento refinado com claim, fundamentos, solidez

**Exemplo de Evolução:**
```
Início:     "LLMs aumentam produtividade" 
            → vago, sem contexto, sem métricas
            → NÃO vetorizar

Meio:       "Ferramentas de código com IA parecem acelerar desenvolvimento"
            → mais específico, ainda impreciso
            → NÃO vetorizar

Snapshot:   "Claude Code reduz tempo de sprint em 30% para tarefas de 
            refatoração em equipes Python (baseado em métricas internas Q4/2024)"
            → claim específico, contexto claro, mensurável
            → VETORIZAR
```

**Benefício para Busca Semântica:**

Vetores que refletem clareza conceitual real (não confusão inicial) produzem:
- **Matches mais precisos:** busca encontra ideias relacionadas, não ruído
- **Biblioteca de qualidade:** apenas essências refinadas entram no catálogo
- **Conexões significativas:** similaridade semântica entre conceitos maduros

**Arquitetura Já Preparada:**

O sistema de snapshots automáticos do Revelar já fornece a estrutura necessária:
- Snapshots capturam momentos de estabilidade cognitiva
- Cada snapshot representa ideia em estado de maturidade
- Vetorização pode ser trigger automático em snapshots marcados como "maduros"

**Implicação Futura:**
```
Conversa → Snapshots automáticos → Detecção de maturidade → Vetorização seletiva
                                                              ↓
                                            Biblioteca global (ChromaDB)
```

Usuário não precisa gerenciar isso - sistema identifica quando argumento atingiu clareza suficiente para ser persistido como vetor semântico.

## Referências

- `core/docs/vision/system_philosophy.md` - Filosofia universal
- `core/docs/vision/super_system.md` - Arquitetura do super-sistema
- `core/docs/vision/conversation_mechanics.md` - Mecânica de conversação
- `core/docs/vision/cognitive_model/` - Como pensamento evolui
- `products/camadas-da-linguagem/docs/vision.md` - Próximo produto no pipeline
- `products/prisma-verbal/docs/vision.md` - Produto irmão (entrada alternativa)

