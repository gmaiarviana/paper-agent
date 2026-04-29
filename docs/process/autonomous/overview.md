# Overview: Modo Autônomo

> **📌 Localização:** `docs/process/autonomous/`
> **📌 Público:** Dev (operador) e Claude Code Web (executor autônomo).
> **📌 Pré-requisito:** Funcionalidade pertence a épico em `🔍 Detalhes definidos` no ROADMAP (checklist `docs/process/refinement/autonomous_readiness.md` aplicado).

---

## 1. O QUE É O MODO AUTÔNOMO

Modo de operação onde o dev **dispara um milestone pela manhã** via Claude Code Web e **valida o resultado à noite**, com skills automáticas conduzindo Scrum Master → Dev → QA → TL → PO → RTE.

**Diferencial:** o dev não acompanha cada checkpoint. As skills atuam como gates de qualidade — gates QA/TL/PO/RTE substituem o acompanhamento checkpoint-a-checkpoint.

---

## 2. PAPÉIS

### Dev (Operador)
**Pela manhã:**
- ✅ Escolher funcionalidade do ROADMAP (épico em `🔍 Detalhes definidos`)
- ✅ Disparar via `docs/process/autonomous/dispatch.md` em claude.ai/code
- ✅ Garantir que branch alvo segue padrão `milestone/<id-em-caixa-baixa>`

**À noite (ao receber notificação):**
- ✅ Rodar comandos de validação local fornecidos pelo RTE Skill
- ✅ Validar critérios de aceite manualmente
- ✅ Aprovar merge OU devolver com feedback para nova rodada

**Não faz:**
- ❌ Acompanhar checkpoints intermediários
- ❌ Aprovar cada decisão arquitetural pequena
- ❌ Criar PR (a RTE cria automaticamente via `mcp__github__create_pull_request`)

### Skills Automáticas (Gates)
- **Scrum Master Skill:** lê ROADMAP, quebra a funcionalidade em tarefas, esclarece dúvidas técnicas (consulta docs antes de assumir).
- **QA Skill:** valida testes, sintaxe, imports, comportamento esperado.
- **TL Skill:** valida arquitetura, padrões, aderência ao ROADMAP e a `docs/ARCHITECTURE.md`.
- **PO Skill:** valida critérios de aceite contra o ROADMAP.
- **RTE Skill:** prepara branch + comandos de validação para o dev.

Cada skill é um gate: se reprovar, devolve para a etapa anterior antes de avançar.

---

## 3. ESTADO MÍNIMO DO ÉPICO

| Aspecto | Requisito |
|---------|-----------|
| **Estado mínimo do épico** | `🔍 Detalhes definidos` (sessão de refinamento com alvo `🔍` aplicada — ver `docs/process/refinement/autonomous_readiness.md`) |
| **Refinamento** | PM skill (dentro da branch do milestone, leva épicos `🌱`/`📐`/`📋` até `🔍`); refinamento estratégico em sessão externa com Claude Web é caminho secundário, antes do dispatch |
| **Aprovação por checkpoint** | Gates QA/TL/PO automáticos (sem acompanhamento explícito do dev) |
| **Validação intermediária** | Skills validam; dev só valida no final |
| **PR** | RTE abre PR com Seção 🎯 Validação; dev revisa colando no Copilot e mergeia |

`📋 Critérios definidos` é **passo intermediário** até `🔍` — o fluxo único de execução exige `🔍`.

---

## 4. QUANDO USAR

### Use o Modo Autônomo quando...
- Épico está em `🔍 Detalhes definidos` — sessão de refinamento com alvo `🔍` concluída, checklist de `docs/process/refinement/autonomous_readiness.md` coberto
- Dependências técnicas validadas
- Padrão de implementação conhecido (template apontado; segue épicos anteriores)
- Dev quer disparar e validar depois (sem acompanhamento ativo)

### Quando o épico ainda não está em `🔍`
- Épicos em `🌱 Visão`, `📐 Funcionalidades esboçadas` ou `📋 Critérios definidos` precisam de refinamento antes de qualquer dispatch.
- Caminho principal: PM skill via Claude Code Web (dentro da branch do milestone).
- Caminho secundário: sessão estratégica externa (Claude Web ou equivalente) — usada quando há decisão de alto nível que exige alinhamento com o operador antes de aterrissar no repo.
- Ver `docs/process/refinement/planning_guidelines.md` §"Modalidades de Refinamento".

---

## 5. ESCOPO E LIMITES

**O modo autônomo NÃO substitui:**
- CONSTITUTION (princípios continuam valendo)
- `docs/process/implementation/` (guidelines de implementação seguem aplicáveis)
- `docs/process/refinement/planning_guidelines.md` (processo de refinamento — caminho principal é PM skill via Claude Code Web; sessão estratégica é caminho secundário)

**O modo autônomo COMPLEMENTA:**
- Reaproveita ROADMAP, ARCHITECTURE, docs/agents existentes
- Usa skills como substitutas das aprovações explícitas do dev

---

**Ver também:**
- Fluxo detalhado das skills → [workflow.md](workflow.md)
- Como disparar e validar → [delivery.md](delivery.md)
- Template de dispatch → `docs/process/autonomous/dispatch.md`
- Convenções operacionais (segredos, granularidade de commits) → [session_conventions.md](session_conventions.md)
