# Filosofia de Navegação - Paper Agent

## Visão Geral
Documento que estabelece a filosofia de navegação do sistema, separando três espaços distintos com propósitos diferentes.

## Três Espaços Distintos

### 1. Conversas (Sidebar - Processo)
**Propósito:** Continuar pensamento ativo, processo em andamento.

**Características:**
- Natureza: Volátil, dinâmica
- Localização: Sidebar sempre visível
- Duração: Temporária (conversas recentes)
- Ação: Clicar → retoma thread_id e continua conversa

**Exemplo:**
- "Conversa de 5min atrás" → voltar pra continuar pensando
- "Conversa de 2h atrás" → lembrar de algo dito

**Metáfora:** Rascunhos no bloco de notas (trabalho em progresso)

---

### 2. Meus Pensamentos (Página Dedicada - Cristalização)
**Propósito:** Contemplar ideias elaboradas com calma.

**Características:**
- Natureza: Permanente, refinada
- Localização: Página dedicada (`/pensamentos`)
- Duração: Persistente (arquivo de ideias)
- Ação: Clicar → página com detalhes completos

**Exemplo:**
- "LLMs em produtividade" → 3 argumentos, 5 conceitos
- "Semana de 4 dias" → ideia pausada, 2 argumentos

**Metáfora:** Artigos salvos na biblioteca (cristalização)

---

### 3. Catálogo (Página Dedicada - Biblioteca Técnica)
**Propósito:** Explorar conceitos técnicos reutilizáveis.

**Características:**
- Natureza: Biblioteca compartilhada
- Localização: Página dedicada (`/catalogo`)
- Duração: Permanente (conceitos universais)
- Ação: Clicar → mostra ideias que usam aquele conceito

**Exemplo:**
- "Cooperação" → usado em 5 ideias, 12 variações linguísticas
- "Produtividade" → usado em 3 ideias

**Metáfora:** Biblioteca técnica de termos (conhecimento reutilizável)

---

## Fluxos de Navegação

### Fluxo 1: Conversa → Ideia Cristalizada
```
[Sidebar] Conversa ativa
    ↓
[Chat] Sistema cristaliza ideia silenciosamente
    ↓
[Meus Pensamentos] Ideia aparece na biblioteca
```

### Fluxo 2: Explorar Ideia → Continuar Pensando
```
[Meus Pensamentos] Clicar em ideia
    ↓
[Página Dedicada] Ver detalhes (argumentos, conceitos)
    ↓
[Botão: Continuar explorando] → Volta pro chat com novo thread_id
```

### Fluxo 3: Conceito → Ideias Relacionadas
```
[Catálogo] Clicar em conceito
    ↓
[Página do Conceito] Ver ideias que usam
    ↓
[Clicar em ideia] → Página dedicada da ideia
```

---

## Princípios de Design

### 1. Separação de Contextos
- **Conversas:** Pensamento ativo, volátil
- **Ideias:** Pensamento cristalizado, permanente
- **Conceitos:** Conhecimento reutilizável, universal

### 2. Progressão Natural
```
Conversa (processo) → Ideia (cristalização) → Conceito (abstração)
```

### 3. Nomenclatura Intencional
- ❌ "Nova Ideia" (usuário não cria ideia explicitamente)
- ✅ "Nova Conversa" (sistema cristaliza ideia durante conversa)

### 4. Localização Justificada
- **Sidebar:** Acesso rápido (conversas recentes)
- **Página dedicada:** Contemplação calma (ideias, conceitos)

---

## Justificativa Arquitetural

### Por Que Separar Conversas de Ideias?

**Problema:** Sidebar única misturava processo (conversa) com cristalização (ideia).

**Solução:** Separação física reflete separação conceitual.

**Benefícios:**
- Clareza de propósito (cada espaço tem função específica)
- Fluxo natural (conversa → ideia → conceito)
- Escalabilidade (cada página pode crescer independentemente)

### Por Que Página Dedicada para Ideias?

**Justificativa:** Ideias cristalizadas merecem contemplação, não navegação rápida.

**Analogia:**
- Conversas = Inbox do email (rápido, efêmero)
- Ideias = Pasta de arquivados (organizado, permanente)

---

## Referências

- `docs/interface/web.md` - Implementação técnica
- `docs/vision/vision.md` - Visão de produto
- `docs/architecture/ontology.md` - Definição de Ideia vs Conceito

