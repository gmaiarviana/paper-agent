# Overview: Modo Autônomo

> **📌 Localização:** `docs/process/autonomous/`
> **📌 Público:** Dev (operador) e Claude Code Web (executor autônomo).
> **📌 Pré-requisito:** Funcionalidade pertence a épico refinado no ROADMAP.

---

## 1. O QUE É O MODO AUTÔNOMO

Modo de operação onde o dev **dispara uma funcionalidade pela manhã** via Claude Code Web e **valida o resultado à noite**, com skills automáticas conduzindo Planning → Dev → QA → TL → PO → Validation.

**Diferencial:** o dev não acompanha cada checkpoint. As skills atuam como gates de qualidade no lugar das aprovações explícitas do fluxo manual.

---

## 2. PAPÉIS

### Dev (Operador)
**Pela manhã:**
- ✅ Escolher funcionalidade do ROADMAP (épico refinado)
- ✅ Disparar via `docs/process/autonomous/dispatch.md` em claude.ai/code
- ✅ Garantir que branch alvo segue padrão `feature/X.Y-nome`

**À noite (ao receber notificação):**
- ✅ Rodar comandos de validação local fornecidos pelo Validation Skill
- ✅ Validar critérios de aceite manualmente
- ✅ Aprovar merge OU devolver com feedback para nova rodada

**Não faz:**
- ❌ Acompanhar checkpoints intermediários
- ❌ Aprovar cada decisão arquitetural pequena
- ❌ Criar PR manualmente (o fluxo autônomo já entrega branch pronta)

### Skills Automáticas (Gates)
- **Planning Skill:** lê ROADMAP, quebra a funcionalidade em tarefas, esclarece dúvidas técnicas (consulta docs antes de assumir).
- **QA Skill:** valida testes, sintaxe, imports, comportamento esperado.
- **TL Skill:** valida arquitetura, padrões, aderência ao ROADMAP e a `docs/ARCHITECTURE.md`.
- **PO Skill:** valida critérios de aceite contra o ROADMAP.
- **Validation Skill:** prepara branch + comandos de validação para o dev.

Cada skill é um gate: se reprovar, devolve para a etapa anterior antes de avançar.

---

## 3. DIFERENÇAS DO FLUXO MANUAL

| Aspecto | Fluxo Manual (Cursor) | Fluxo Autônomo (Claude Code Web) |
|---------|----------------------|----------------------------------|
| **Refinamento** | Claude Web → prompts → Cursor | Planning Skill (autônomo, com ROADMAP) |
| **Aprovação por checkpoint** | Explícita do dev | Gates QA/TL/PO automáticos |
| **Validação intermediária** | Dev valida a cada checkpoint | Skills validam; dev só valida no final |
| **PR** | Dev cria pela interface | Branch pronta + comandos para dev validar |
| **Quando usar** | Épicos novos, decisões arquiteturais | Funcionalidades já refinadas e claras |

---

## 4. QUANDO USAR CADA MODO

### Use o Fluxo Manual quando...
- Épico ainda não foi refinado
- Há decisões arquiteturais em aberto
- Funcionalidade exige discussão de trade-offs
- Mudança impacta múltiplos sistemas / docs estruturais

### Use o Modo Autônomo quando...
- Funcionalidade já refinada com critérios de aceite claros
- Dependências técnicas validadas
- Padrão de implementação conhecido (segue épicos anteriores)
- Dev quer disparar e validar depois (sem acompanhamento ativo)

---

## 5. ESCOPO E LIMITES

**O modo autônomo NÃO substitui:**
- CONSTITUTION (princípios continuam valendo)
- `docs/process/implementation/` (guidelines de implementação seguem aplicáveis)
- `docs/process/refinement/planning_guidelines.md` (refinamento de épicos continua manual via Claude Web)

**O modo autônomo COMPLEMENTA:**
- Adiciona uma alternativa ao Cursor para disparar funcionalidades já refinadas
- Reaproveita ROADMAP, ARCHITECTURE, docs/agents existentes
- Usa skills como substitutas das aprovações explícitas do dev

---

**Ver também:**
- Fluxo detalhado das skills → [workflow.md](workflow.md)
- Como disparar e validar → [delivery.md](delivery.md)
- Template de dispatch → `docs/process/autonomous/dispatch.md`
