# Filosofia de Navegação - Paper Agent

## Visão Geral
Documento que estabelece a filosofia de navegação do sistema, organizando três espaços de navegação com propósitos diferentes, com ideias como centro da experiência.

## Três Espaços de Navegação

### 1. Minhas Ideias (Principal)
**Propósito:** Navegar e elaborar ideias.

**Características:**
- Natureza: Permanente, refinável
- Acesso: Link "📖 Pensamentos" na sidebar
- Ação principal: Ver ideias, continuar elaboração, criar conteúdo

**Dentro de cada Ideia:**
- Iniciar novo chat (continuar elaboração)
- Ver conversas passadas associadas
- Ver fundamentos e solidez de cada um
- Criar conteúdo (se madura)

**Metáfora:** Portfolio de pensamentos em construção

---

### 2. Catálogo (Referência)
**Propósito:** Explorar conceitos reutilizáveis.

**Características:**
- Natureza: Atemporal, compartilhável
- Acesso: Link "🏷️ Catálogo" na sidebar
- Origem: Usuário, literatura, múltiplos usuários

**Metáfora:** Dicionário universal de termos

---

### 3. Histórico (Secundário)
**Propósito:** Acessar conversas passadas.

**Características:**
- Natureza: Registro de interações
- Acesso: Link "💬 Conversas" na sidebar → página dedicada
- Ação: Retomar conversa específica

**Nota:** Não aparece listado na sidebar, apenas link para página dedicada.

**Metáfora:** Logs de trabalho (valioso mas não é o foco)

**Nota:** O valioso é o resultado (ideia elaborada), não a conversa em si.

---

## Fluxos de Navegação

### Fluxo 1: Conversa → Ideia Cristalizada
```
[Chat] Conversa ativa
    ↓
[Sistema] Sistema cristaliza ideia silenciosamente
    ↓
[Minhas Ideias] Ideia aparece na biblioteca
```

### Fluxo 2: Explorar Ideia → Continuar Pensando
```
[Minhas Ideias] Clicar em ideia
    ↓
[Página Dedicada] Ver detalhes (fundamentos, solidez, conversas)
    ↓
[Botão: Continuar elaborando] → Volta pro chat com novo thread_id
```

### Fluxo 3: Conceito → Ideias Relacionadas
```
[Catálogo] Clicar em conceito
    ↓
[Página do Conceito] Ver ideias que usam
    ↓
[Clicar em ideia] → Página dedicada da ideia
```

### Fluxo 4: Ideia → Criar Conteúdo
```
[Minhas Ideias] Ver ideia madura
    ↓
[Botão: Criar Conteúdo]
    ↓
[Chat] Definir expectativas (formato, tom, ênfase)
    ↓
[Escritor] Gera conteúdo baseado em metadados
```

### Fluxo 5: Retomar Assunto Anterior
```
[Novo Chat] Usuário menciona tema já discutido
    ↓
[Sistema] Detecta similaridade com ideia existente
    ↓
[Sistema] Provoca: "Isso parece relacionado à ideia X. Quer evoluir ela?"
    ↓
[Usuário] Confirma ou inicia nova ideia
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

### 3. Ideias > Conversas
- Conversas são meio, não fim
- O valioso é a ideia elaborada com seus fundamentos
- Histórico é acessível mas não proeminente

### 4. Menu Minimalista
- Não distrair com navegação durante conversa
- Sidebar minimalista com links para páginas dedicadas (sem listar conversas)
- Foco no chat durante elaboração

### 5. Nomenclatura Intencional
- ❌ "Nova Ideia" (usuário não cria ideia explicitamente)
- ✅ "Nova Conversa" (sistema cristaliza ideia durante conversa)

### 6. Sidebar como Navegação Pura
- Sidebar contém apenas links para páginas
- Não lista conversas ou ideias inline
- Histórico acessível via página dedicada
- Inspirado no padrão Claude/ChatGPT

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
- `docs/vision/epistemology.md` - Por que proposições têm solidez

