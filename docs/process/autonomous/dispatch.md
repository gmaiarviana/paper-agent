# Autonomous Dispatch

> **📌 Uso:** copie o template abaixo, substitua os placeholders e cole no [claude.ai/code](https://claude.ai/code) sobre o repositório `paper-agent`.
> **📌 Pré-requisito:** funcionalidade pertence a épico em **`🔍 Detalhes definidos`** no ROADMAP (checklist `docs/process/refinement/autonomous_readiness.md` aplicado). Épicos em `📋 Critérios definidos` usam o fluxo manual via Cursor; em `🌱 Visão` ou `📐 Funcionalidades esboçadas`, passam por sessão de refinamento antes.
> **📌 Documentação completa:** `docs/process/autonomous/`

---

## TEMPLATE DE DISPATCH

```
Dispatch Autônomo - [Funcionalidade X.Y]

Funcionalidade: [X.Y - nome da funcionalidade conforme ROADMAP]
Roadmap: [docs/ROADMAP.md OU products/<produto>/ROADMAP.md]
Branch: feature/X.Y-nome
Modo: Autônomo (Planning → Dev → QA → TL → PO → Validation)

Implementar a funcionalidade X.Y seguindo o fluxo autônomo definido em
docs/process/autonomous/ (overview.md, workflow.md, delivery.md).

Contexto obrigatório a ler antes de iniciar:
- docs/CONSTITUTION.md
- docs/ARCHITECTURE.md
- docs/process/refinement/planning_guidelines.md
- [Roadmap acima]
- docs/process/autonomous/workflow.md
- docs/process/autonomous/session_conventions.md (política de segredos e granularidade de commits)
- docs/process/implementation/ (guidelines de implementação reaproveitadas)
- docs/CONTEXT_INDEX.md (para localizar specs técnicas relevantes)
- skills/README.md (índice das skills + ordem de carregamento)

OBRIGATÓRIO — Carregamento de skill por gate:
Antes de executar CADA gate do fluxo, abrir e seguir integralmente o skill.md
correspondente. O skill.md é o prompt operacional do gate — não resumir, não
adaptar, não pular passos. Sequência:

  1. Antes do Planning:  abrir skills/planning/skill.md  e seguir na íntegra
  2. Antes do QA:        abrir skills/qa/skill.md        e seguir na íntegra
  3. Antes do TL:        abrir skills/tl/skill.md        e seguir na íntegra
  4. Antes do PO:        abrir skills/po/skill.md        e seguir na íntegra
  5. Antes do Validation: abrir skills/validation/skill.md e seguir na íntegra

Ao concluir cada gate, registrar em docs/process/current_implementation.md
(seção "Status dos Gates") uma linha de evidência no formato:
  "[GATE] skill carregada: skills/<gate>/skill.md ✅ <YYYY-MM-DD HH:MM>"

Restrições:
- Não refinar épico (refinamento é manual via Claude Web)
- Não tomar decisões arquiteturais novas (abortar e devolver ao dev se necessário)
- Não criar PR; entregar branch pronta + comandos de validação
- Cada gate (QA/TL/PO) é obrigatório; reprovação volta para etapa anterior
- Nenhum gate pode começar sem antes carregar seu skill.md e sem a evidência do gate anterior registrada em current_implementation.md

Entrega esperada (Validation Skill):
- Branch feature/X.Y-nome com push realizado
- docs/process/current_implementation.md atualizado
- Mensagem final no formato de docs/process/implementation/delivery.md
- Notificação ao dev com comandos prontos para validação local
```

---

## CHECKLIST ANTES DE DISPARAR

- [ ] Funcionalidade X.Y está em épico marcado como **`🔍 Detalhes definidos`** no ROADMAP
- [ ] Refinamento com alvo `🔍 Detalhes definidos` aplicado — itens de `docs/process/refinement/autonomous_readiness.md` cobertos (termos, contratos, arquivos-alvo, integração, acoplamentos, testes)
- [ ] Critérios de aceite estão claros e testáveis
- [ ] Dependências técnicas implementadas e validadas
- [ ] Sem decisões arquiteturais em aberto (caso contrário → fluxo manual via Cursor)
- [ ] Nome da branch segue padrão `feature/X.Y-nome`
- [ ] `docs/process/current_implementation.md` **não existe** (épico anterior finalizado)

---

## EXEMPLO PREENCHIDO

```
Dispatch Autônomo - Funcionalidade 11.3

Funcionalidade: 11.3 - Detecção de Maturidade via Snapshots
Roadmap: docs/ROADMAP.md
Branch: feature/11.3-snapshot-detection
Modo: Autônomo (Planning → Dev → QA → TL → PO → Validation)

Implementar a funcionalidade 11.3 seguindo o fluxo autônomo definido em
docs/process/autonomous/.

[... resto do template ...]
```

---

**Ver também:**
- Quando usar autônomo vs manual → `docs/process/autonomous/overview.md`
- Detalhe dos gates → `docs/process/autonomous/workflow.md`
- Como validar o resultado → `docs/process/autonomous/delivery.md`
- Convenções operacionais (segredos, granularidade de commits) → `docs/process/autonomous/session_conventions.md`
