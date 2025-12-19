# Message Builder - Experiência do Usuário

## 1. Visão Geral

**Propósito:** Permitir que usuário construa mensagens (combinações de proposições/argumentos) de forma visual e conversacional.

**Diferencial:**
- NÃO é editor de texto (Word, Google Docs)
- É construtor de ESTRUTURA que gera conteúdo
- Combina chat (definir intenção) + grafo visual (customizar componentes)

**Metáfora:** Montar um "esqueleto" da mensagem antes de gerar o "corpo" (texto final).

---

## 2. Fluxo Principal (3 Etapas)

### Etapa 1: Selecionar Ideia

Usuário escolhe qual ideia quer comunicar.

```
┌─────────────────────────────────────────┐
│ 💡 Minhas Ideias                        │
│                                         │
│ [Card] Cidades fazem mal à saúde mental │
│        5 argumentos | Solidez: 72%      │
│        [Criar mensagem →]               │
│                                         │
│ [Card] LLMs aumentam produtividade      │
│        3 argumentos | Solidez: 65%      │
│        [Criar mensagem →]               │
└─────────────────────────────────────────┘
```

### Etapa 2: Definir Intenção (Chat)

Conversa para capturar vetor emocional.

```
┌─────────────────────────────────────────┐
│ 💬 Definir Intenção                     │
│                                         │
│ Sistema: "Você quer criar uma mensagem  │
│ sobre 'Cidades fazem mal à saúde        │
│ mental'. Como você quer que a pessoa    │
│ SE SINTA ao ler?"                       │
│                                         │
│ Usuário: "Quero que ela pare e          │
│ questione se a vida que leva faz        │
│ sentido. Um incômodo silencioso."       │
│                                         │
│ Sistema: "Entendi. Baseado nisso,       │
│ organizei os argumentos mais            │
│ alinhados. Veja o grafo ao lado."       │
│                                         │
│ [Input: Digite sua resposta...]         │
└─────────────────────────────────────────┘
```

### Etapa 3: Customizar no Grafo

Visualização + customização de componentes.

```
┌───────────────────────────────────────────────────────────┐
│ Chat (30%)              │ Grafo Visual (70%)              │
│                         │                                 │
│ [Conversa anterior]     │      [💡 Cidades fazem mal]     │
│                         │              |                  │
│                         │    ┌─────────┴─────────┐        │
│                         │    |                   |        │
│                         │ [🟢 Prop A]       [🟡 Prop B]   │
│                         │ Afastamento       Ritmo         │
│                         │ natureza          urbano        │
│                         │    |                   |        │
│                         │ [Argumentos]     [Argumentos]   │
│                         │ 🟢 Vivencial     ⚪ Científico  │
│                         │ ⚪ Científico    🟡 Evolutivo   │
│                         │    |                            │
│                         │ [Evidências]                    │
│                         │ ✓ Relato pessoal                │
│                         │ ✓ Dados qualidade               │
│                         │ ✗ Estatísticas                  │
└───────────────────────────────────────────────────────────┘
```

---

## 3. Componentes do Grafo

### Nó: Ideia (Raiz)

- Sempre visível no topo
- Mostra título + solidez geral
- Clicável para ver detalhes

### Nó: Proposição

- Conectado à ideia
- Mostra enunciado resumido
- Cor indica aderência: 🟢 alta, 🟡 média, ⚪ baixa
- Clicável para expandir argumentos

### Nó: Argumento

- Conectado à proposição
- Mostra claim resumido
- Cor indica similaridade com vetor emocional
- Toggle: incluir/excluir da mensagem
- Clicável para ver evidências

### Nó: Evidência

- Conectado ao argumento
- Checkbox: selecionar/deselecionar
- Mostra texto resumido
- Hover para ver texto completo

### Conexões (Arestas)

- Linha sólida = incluído na mensagem
- Linha pontilhada = disponível mas não incluído
- Espessura = relevância para vetor emocional

---

## 4. Interações

### Expandir/Colapsar

- Clique em nó expande filhos
- Segundo clique colapsa
- Estado inicial: proposições visíveis, argumentos colapsados

### Incluir/Excluir

- Toggle em argumento: adiciona/remove da mensagem
- Sistema recalcula estrutura em tempo real
- Feedback visual imediato (cor muda)

### Customizar Evidências

- Dentro de argumento expandido
- Checkboxes para cada evidência
- Pode selecionar qualquer combinação
- Sistema sugere combinação inicial

### Reordenar

- Drag-and-drop de argumentos
- Define ordem de aparição na mensagem final
- Indicador visual de posição (1, 2, 3...)

### Chat Contínuo

- Usuário pode refinar intenção a qualquer momento
- "Na verdade, quero mais urgência e menos empatia"
- Sistema recalcula similaridades e atualiza grafo

---

## 5. Estados do Sistema

### Estado Inicial

- Grafo mostra todos argumentos
- Cores indicam sugestão inicial (baseado em vetor emocional)
- Nenhum argumento selecionado ainda

### Estado Durante Customização

- Argumentos selecionados destacados (borda + cor)
- Contador: "3 argumentos selecionados"
- Preview parcial atualiza em tempo real

### Estado Pronto

- Todos argumentos escolhidos
- Evidências customizadas
- Ordem definida
- Botão "Gerar Conteúdo" habilitado

---

## 6. Preview da Mensagem

Painel lateral (ou modal) mostra estrutura resultante:

```
┌─────────────────────────────────────────┐
│ 📄 Preview da Mensagem                  │
│                                         │
│ Estrutura:                              │
│ 1. Proposição: Afastamento natureza     │
│    └─ Argumento: Vivencial              │
│       └─ Evidência: Relato pessoal      │
│       └─ Evidência: Dados qualidade     │
│                                         │
│ 2. Proposição: Ritmo urbano             │
│    └─ Argumento: Evolutivo              │
│       └─ Evidência: Ciclo circadiano    │
│                                         │
│ Vetor emocional:                        │
│ Empatia ████████░░ 0.82                 │
│ Reflexão ██████░░░░ 0.65                │
│                                         │
│ [Gerar Conteúdo →]                      │
└─────────────────────────────────────────┘
```

---

## 7. Próxima Etapa: Escolher Forma

Após mensagem pronta, usuário escolhe forma:

```
┌─────────────────────────────────────────┐
│ 📝 Escolher Forma                       │
│                                         │
│ Para quem é essa mensagem?              │
│ [Profissionais urbanos 25-40 anos]      │
│                                         │
│ Qual formato?                           │
│ ○ Artigo LinkedIn (500-800 palavras)    │
│ ○ Thread Twitter (5-10 tweets)          │
│ ○ Post blog/Medium (1000-1500 palavras) │
│ ○ Texto curto (150-300 palavras)        │
│                                         │
│ Tom desejado?                           │
│ ○ Pessoal e vulnerável                  │
│ ○ Profissional e direto                 │
│ ○ Reflexivo e filosófico                │
│                                         │
│ [Gerar →]                               │
└─────────────────────────────────────────┘
```

---

## 8. Responsividade

### Desktop (>1024px)

- Layout lado-a-lado: Chat (30%) | Grafo (70%)
- Preview como sidebar colapsável

### Tablet (768-1024px)

- Chat em cima, Grafo embaixo
- Scroll vertical
- Preview como modal

### Mobile (<768px)

- Telas separadas (wizard)
- Etapa 1: Chat
- Etapa 2: Grafo (simplificado, lista ao invés de grafo)
- Etapa 3: Preview + Forma

---

## 9. MVP vs Visão

### MVP (Protótipo Lovable)

- Chat simples (categorias fixas de emoção)
- Grafo como árvore clicável (não visual complexo)
- Seleção binária (incluir/excluir)
- Preview como lista estruturada

### Visão (Produção)

- Chat com LLM (vetor emocional latente)
- Grafo visual interativo (D3.js ou similar)
- Similaridade vetorial em tempo real
- Preview com geração parcial

---

## Referências

- `core/docs/vision/communication_philosophy.md` - Filosofia de Mensagem
- `core/docs/architecture/data-models/message_model.md` - Schema técnico
- `products/revelar/docs/interface/` - Padrões de interface existentes

