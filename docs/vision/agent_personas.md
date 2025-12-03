# Agent Personas - Visão Futura

> **Status:** Épico 18 (Planejado - Não Refinado)
> **Dependências:** Épicos 11-16 concluídos, agentes visíveis na interface

## Conceito

Agentes como "colegas de trabalho" especializados que usuário 
pode conhecer, confiar e eventualmente customizar.

## Por Que Agentes Visíveis?

**Transparência autêntica:**
- Usuário entende QUE tipo de análise está sendo feita
- "Orquestrador provocando" ≠ "Metodologista validando"
- Cada agente tem papel e expertise clara

**Educativo:**
- Usuário aprende tipos de pensamento científico
- Orquestrador = exploração socrática
- Estruturador = organização aristotélica
- Metodologista = validação popperiana

**Diferencial de produto:**
- LLMs generalistas = caixa preta opaca
- Paper-agent = equipe de especialistas visível
- "Trabalhe com Sócrates" > "Use IA genérica"

## Agentes Padrão (Épicos 11-14)

### Orquestrador
**Papel:** Facilitador socrático, provocador de reflexão
**Estilo:** Questionador, expõe suposições implícitas
**Aparência:** 🎯 Orquestrador

### Estruturador
**Papel:** Organizador lógico de argumentos
**Estilo:** Sistemático, cristaliza ideias vagas
**Aparência:** 📝 Estruturador

### Metodologista
**Papel:** Validador de rigor científico
**Estilo:** Cético, falsificacionista
**Aparência:** 🔬 Metodologista

### Pesquisador (Futuro)
**Papel:** Buscador de evidências bibliográficas
**Estilo:** Analítico, sintético
**Aparência:** 📚 Pesquisador

### Escritor (Futuro)
**Papel:** Compilador de artigo final
**Estilo:** Acadêmico, estruturado
**Aparência:** ✍️ Escritor

## Customização de Personas (Épico 18)

### Biblioteca de Personas Pré-Definidas

**Orquestrador:**
- **Sócrates:** Provocativo, maiêutico, questiona suposições
- **Feynman:** Didático, busca simplicidade, contra jargões
- **Customizado:** Usuário define estilo via referências

**Estruturador:**
- **Aristóteles:** Lógico formal, silogismos, categorias claras
- **Descartes:** Cartesiano, fundamentos sólidos, dúvida metódica
- **Customizado:** Usuário define estilo via referências

**Metodologista:**
- **Karl Popper:** Falsificacionista, cético, rigor refutacionista
- **Thomas Kuhn:** Paradigmas, contextualiza validação científica
- **Customizado:** Usuário define estilo via referências

### Como Funciona a Customização

**Passo 1: Escolher base**
Orquestrador: [Sócrates ▼] [Customizar ⚙️]

**Passo 2: Fornecer referências**
- Upload PDFs (artigos modelo, textos do autor preferido)
- Sistema extrai estilo de argumentação
- Fine-tuning via RAG (retrieval de exemplos)

**Passo 3: Treinar persona**
- Sistema aprende padrões linguísticos
- Imita estrutura argumentativa
- Preserva essência do agente (papel não muda)

**Passo 4: Usar na conversa**
💬 Sócrates (Orquestrador customizado):
"Me diga, caro amigo: quando mencionas 'visão computacional',
falas de qual aspecto? Há tantos caminhos possíveis..."

### Benefícios da Customização

**Para o usuário:**
- Trabalha com "mentores" que admira
- Estilo de argumentação familiar
- Aprendizado por modelagem

**Para o sistema:**
- Diferencial competitivo único
- Engajamento emocional (trabalhar com Sócrates!)
- Fidelização (persona customizada = investimento do usuário)

## UX: Como Mostrar Agentes

### Interface Padrão (Épicos 11-14)

**Bastidores (painel direito):**
┌─────────────────────────────────┐
│ 🎯 Orquestrador (agora):        │
│ "Turno inicial. Escopo vago.    │
│  Necessário provocar..."        │
│                                 │
│ [Ver raciocínio completo ↗]     │
└─────────────────────────────────┘

### Interface com Personas (Épico 18)

**Bastidores com persona customizada:**
┌─────────────────────────────────┐
│ 💬 Sócrates (Orquestrador):     │
│ "Me diga: quando mencionas      │
│  'visão computacional', falas   │
│  de qual aspecto?"              │
│                                 │
│ [Ver raciocínio completo ↗]     │
│ [Customizar persona ⚙️]         │
└─────────────────────────────────┘

**Configurações (modal):**
⚙️ Configurar Agentes

Orquestrador:
  Persona: [Sócrates ▼]
  [ ] Sócrates (maiêutico)
  [ ] Feynman (didático)
  [x] Customizado
  
  Referências customizadas:
  📄 artigo_modelo_1.pdf
  📄 diálogos_platão.pdf
  [+ Adicionar PDF]
  
  [Salvar] [Resetar para padrão]

## Implementação Técnica (Épico 18)

**Stack:**
- ChromaDB para armazenar exemplos de argumentação
- sentence-transformers para embeddings
- Retrieval de exemplos similares ao contexto atual
- Prompt engineering para imitar estilo da persona

**Fluxo:**
1. Usuário escolhe persona (ex: Sócrates)
2. Sistema carrega exemplos de argumentação socrática (pré-treinados)
3. Se customizado: sistema indexa PDFs fornecidos
4. A cada turno: retrieval de exemplos similares
5. Prompt: "Responda como Sócrates responderia, seguindo estes exemplos: {retrieved_examples}"

**Desafios:**
- Preservar funcionalidade do agente (não pode perder eficácia)
- Balance: estilo da persona vs. precisão técnica
- Evitar "teatro" (persona não pode atrapalhar clareza)

## Referências

- `docs/vision/vision.md` - Visão de produto
- `docs/vision/cognitive_model.md` - Modelo cognitivo
- `docs/agents/` - Especificações técnicas de cada agente

