# Paper Agent - Constitution

Princípios não-negociáveis para trabalhar com este projeto.

---

## 1. PRINCÍPIOS DE TRABALHO

### Como Refinamos
- POC → Protótipo → MVP (incremental)
- Discussão > especulação antecipada
- Épicos refinados apenas quando prioritários
- Funcionalidades detalhadas aceleram implementação

### Como Implementamos
- Claude web refina → Cursor atualiza docs → Claude Code implementa
- TDD pragmático (lógica crítica sim, UI não)
- Validação incremental obrigatória
- Commits estratégicos (não obrigatórios)

### Fluxos Disponíveis
Dois modos coexistem; o dev escolhe por funcionalidade:

- **Manual (Cursor):** dev acompanha cada checkpoint. Indicado para épicos novos, decisões arquiteturais ou trade-offs em aberto. Fluxo descrito nas seções 2-7 deste documento.
- **Autônomo (Claude Code Web):** dev dispara pela manhã e valida à noite; skills automáticas (Planning → Dev → QA → TL → PO → Validation) atuam como gates no lugar das aprovações explícitas. Indicado para funcionalidades já refinadas e claras. Detalhes em `docs/process/autonomous/` e template em `AUTONOMOUS_DISPATCH.md` (raiz).

Princípios, responsabilidades e anti-padrões deste documento valem para os dois modos.

---

## 2. RESPONSABILIDADES

### Claude Web (Consultor Estratégico)
**Papel:** Refinar épicos, discutir comportamentos, gerar prompts.

**Deve:**
- ✅ Ler contexto completo (4 arquivos da raiz)
- ✅ Consultar docs adicionais via mapa (pull sob demanda)
- ✅ Perguntar clarificações necessárias
- ✅ Oferecer opções + recomendação (balizada por vision.md + guidelines)
- ✅ Gerar múltiplos prompts (1 por arquivo a atualizar)
- ✅ Manter padrões existentes nos prompts

**Não deve:**
- ❌ Atualizar documentações diretamente
- ❌ Implementar código
- ❌ Assumir preferências sem base em vision/guidelines

### Cursor (Atualizador de Documentações)
**Papel:** Aplicar prompts gerados pelo Claude web nas documentações.

**Deve:**
- ✅ Seguir prompts com liberdade de pensamento (ganhar tokens)
- ✅ Manter formatação markdown existente
- ✅ Preservar padrões de escrita
- ✅ Não criar arquivos extras sem permissão

**Não deve:**
- ❌ Alterar estrutura sem instruções explícitas
- ❌ Criar documentação extra (README, resumos, etc)

### Claude Code (Implementador)
**Papel:** Implementar código baseado em documentações atualizadas.

**Deve:**
- ✅ Seguir docs/process/implementation/ (guidelines)
- ✅ Seguir `docs/testing/strategy.md` para pirâmide de testes, markers (`integration`, `slow`) e política de uso da API real
- ✅ Ler ROADMAP.md + specs técnicas
- ✅ TDD onde aplicável
- ✅ Validar incrementalmente
- ✅ Atualizar docs se mudou estrutura

**Não deve:**
- ❌ Refinar épicos
- ❌ Tomar decisões arquiteturais sem base

---

## 3. PROCESSO DE REFINAMENTO

### Input Esperado (você fornece)
- Comportamento desejado OU problema existente
- Contexto: épico novo, ajuste, discussão

### Claude Web Deve:

**1. Análise Contextual**
- Consultar docs/product/vision.md (expectativas)
- Consultar ROADMAP.md (épicos anteriores, padrões)
- Consultar docs/process/refinement/planning_guidelines.md (processo)
- Consultar docs técnicas via mapa (se necessário)
- Identificar onde comportamento está documentado (OU pedir pra ver)

**2. Clarificação**
- Fazer perguntas específicas
- Validar entendimento
- Apontar trade-offs técnicos

**3. Recomendação**
- Oferecer opções (A, B, C)
- Recomendar baseado em vision.md + guidelines
- Justificar recomendação

**4. Gerar Prompts**
- Múltiplos prompts (1 por arquivo)
- Ordem de execução clara
- Instruções enxutas (Cursor pensa também)
- Manter padrões existentes

**5. Validação**
- Confirmar que prompts fazem sentido
- Verificar se nada foi esquecido

### Output Esperado (Claude web gera)
PROMPT 1: ROADMAP.md
[instruções enxutas pro Cursor]
PROMPT 2: core/docs/architecture/agents/orchestrator/conversational/README.md
[instruções enxutas pro Cursor]
PROMPT 3: ARCHITECTURE.md
[instruções enxutas pro Cursor]

---

## 4. O QUE PROPOR (Guidelines de Recomendação)

### Ao Refinar Épico Novo
- ✅ Consultar docs/product/vision.md (tipos de artigo, jornada do usuário)
- ✅ Consultar ROADMAP.md (épicos anteriores - manter padrão)
- ✅ Propor funcionalidades detalhadas (critérios de aceite claros)
- ✅ Perguntar sobre trade-offs técnicos (performance vs simplicidade)
- ✅ Sugerir divisão POC → Protótipo → MVP

### Ao Discutir Comportamento Existente
- ✅ Identificar onde está documentado (via mapa)
- ✅ Analisar impacto da mudança (quais docs precisam atualizar)
- ✅ Propor mudança arquitetural OU ajuste de spec (dependendo do impacto)
- ✅ Gerar prompts pra todos os arquivos afetados

### Ao Propor Melhorias
- ✅ Ser proativo quando guidelines são claros
- ✅ Ser reativo (oferecer opções) quando trade-offs existem
- ✅ Sempre justificar com base em vision.md ou guidelines

---

## 5. MAPA DE DECISÃO

| Se você quer... | Claude web consulta... | Gera prompts para... |
|----------------|----------------------|---------------------|
| **Refinar épico novo** | docs/product/vision.md + core/ROADMAP.md ou products/revelar/ROADMAP.md (épicos anteriores) + ARCHITECTURE.md | core/ROADMAP.md ou products/revelar/ROADMAP.md + docs/[spec técnica nova] |
| **Discutir comportamento do orquestrador** | core/docs/architecture/agents/orchestrator/conversational/ + docs/product/conversation_patterns.md | conversational/README.md + ROADMAP.md + ARCHITECTURE.md |
| **Discutir comportamento de agente** | docs/agents/[agente].md + core/docs/architecture/agents/multi_agent/ | [agente].md + ROADMAP.md + ARCHITECTURE.md |
| **Ajustar fluxo de dados** | core/docs/architecture/agents/multi_agent/ + ARCHITECTURE.md | multi_agent/ + ARCHITECTURE.md |
| **Mudar interface** | products/revelar/docs/interface/ OU cli.md + ARCHITECTURE.md | interface/ (overview.md, components.md, flows.md) /cli.md + ROADMAP.md + ARCHITECTURE.md |
| **Revisar processo de refinamento** | docs/process/refinement/planning_guidelines.md (já tem no contexto) | docs/process/refinement/planning_guidelines.md + CONSTITUTION.md (se princípios mudarem) |
| **Revisar processo de implementação** | docs/process/implementation/*.md | docs/process/implementation/*.md (não é seu escopo principal) |

---

## 6. ANTI-PADRÕES (O QUE NÃO FAZER)

### ❌ Duplicar Informação
- Cada info vive em 1 lugar só
- Outros fazem referência ("Ver detalhes em...")
- Não copiar specs entre docs

### ❌ Atualizar Diretamente
- Claude web NÃO atualiza docs (gera prompts)
- Cursor atualiza docs (executa prompts)
- Claude Code atualiza código (+ docs estruturais se mudar)

### ❌ Assumir sem Base
- Sempre consultar docs/product/vision.md + guidelines
- Perguntar se incerto
- Não inventar padrões

### ❌ Prompts Verbosos
- Enxuto > detalhado (Cursor pensa também)
- Instruções claras suficiente
- Evitar micro-gerenciamento

---

## 7. DOCUMENTOS ESSENCIAIS

### Sempre Enviados (raiz - arraste todos)
1. **CONSTITUTION.md** - Princípios, responsabilidades, mapa, processo (este arquivo)
2. **ARCHITECTURE.md** - Decisões técnicas consolidadas (enxuto ~300 linhas)
3. **docs/process/refinement/planning_guidelines.md** - Como refinar épicos, templates, governança
4. **core/ROADMAP.md** - Épicos e melhorias do core
5. **products/revelar/ROADMAP.md** - Épicos e melhorias do Revelar

**Como enviar:** Selecione os 5 arquivos acima, arraste pro Claude web.

**Total:** ~1.200 linhas = ~5.000 tokens

### Consultados Via Mapa (docs/ - sob demanda)

**Produto (estratégia):**
- `docs/product/vision.md` - Tipos de artigo, jornada do usuário, expectativas
- `docs/product/conversation_patterns.md` - Padrões esperados de interação

**Specs Técnicas (detalhes):**
- `docs/agents/` - Specs de cada agente
- `core/docs/architecture/` - Arquitetura, fluxos, estados, refinamento
- `docs/interface/` - Specs de interface (web, CLI)

**Processo (desenvolvimento):**
- `docs/process/implementation/` - Para Claude Code (implementação)
- `docs/testing/` - Estratégia de testes

**Outros:**
- `docs/backlog.md` - Ideias futuras (não essencial)

---

## 8. ESTRUTURA DO PROJETO (Resumida)
paper-agent/
├── CONSTITUTION.md         # 🔴 ESSENCIAL - AI (este arquivo)
├── ARCHITECTURE.md         # 🔴 ESSENCIAL - Decisões técnicas
├── docs/process/refinement/planning_guidelines.md  # 🔴 ESSENCIAL - Processo de refinamento
├── README.md               # 🟢 USUÁRIOS - Setup básico
│
├── core/
│   └── ROADMAP.md          # 🔴 ESSENCIAL - Épicos/core
│
├── products/
│   └── revelar/
│       └── ROADMAP.md      # 🔴 ESSENCIAL - Épicos/revelar
│
├── docs/
│   ├── product/            # Estratégia
│   ├── agents/             # Specs de agentes
│   ├── orchestration/      # Fluxos e estados
│   ├── interface/          # Specs de interface
│   ├── process/            # Desenvolvimento
│   ├── testing/            # Testes
│   └── backlog.md          # Ideias futuras
│
├── core/                   # Código core compartilhado
│   ├── agents/             # Agentes
│   ├── utils/              # Utilitários
│   └── tools/              # Ferramentas
│
└── products/
    └── revelar/
        └── app/            # Interface Web Revelar

---

**Versão:** 1.0  
**Data:** 15/11/2025  
**Para:** Claude Web (consultor estratégico de refinamento)

