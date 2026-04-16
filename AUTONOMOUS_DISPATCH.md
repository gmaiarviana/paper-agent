# AUTONOMOUS_DISPATCH.md

> **📌 Uso:** copie o template abaixo, substitua os placeholders e cole no [claude.ai/code](https://claude.ai/code) sobre o repositório `paper-agent`.
> **📌 Pré-requisito:** funcionalidade pertence a épico **refinado** no ROADMAP. Caso contrário, use o fluxo manual.
> **📌 Documentação completa:** `docs/process/autonomous/`

---

## TEMPLATE DE DISPATCH

```
Dispatch Autônomo - [Funcionalidade X.Y]

Funcionalidade: [X.Y - nome da funcionalidade conforme ROADMAP]
Roadmap: [core/ROADMAP.md OU products/<produto>/ROADMAP.md]
Branch: feature/X.Y-nome
Modo: Autônomo (Planning → Dev → QA → TL → PO → Validation)

Implementar a funcionalidade X.Y seguindo o fluxo autônomo definido em
docs/process/autonomous/ (overview.md, workflow.md, delivery.md).

Contexto obrigatório a ler antes de iniciar:
- CONSTITUTION.md
- ARCHITECTURE.md
- planning_guidelines.md
- [Roadmap acima]
- docs/process/autonomous/workflow.md
- docs/process/development/ (guidelines de implementação reaproveitadas)
- docs/CONTEXT_INDEX.md (para localizar specs técnicas relevantes)

Restrições:
- Não refinar épico (refinamento é manual via Claude Web)
- Não tomar decisões arquiteturais novas (abortar e devolver ao dev se necessário)
- Não criar PR; entregar branch pronta + comandos de validação
- Cada gate (QA/TL/PO) é obrigatório; reprovação volta para etapa anterior

Entrega esperada (Validation Skill):
- Branch feature/X.Y-nome com push realizado
- docs/process/current_implementation.md atualizado
- Mensagem final no formato de docs/process/development/delivery.md
- Notificação ao dev com comandos prontos para validação local
```

---

## CHECKLIST ANTES DE DISPARAR

- [ ] Funcionalidade X.Y está em épico **refinado** no ROADMAP
- [ ] Critérios de aceite estão claros e testáveis
- [ ] Dependências técnicas implementadas e validadas
- [ ] Sem decisões arquiteturais em aberto (caso contrário → fluxo manual)
- [ ] Nome da branch segue padrão `feature/X.Y-nome`
- [ ] `docs/process/current_implementation.md` **não existe** (épico anterior finalizado)

---

## EXEMPLO PREENCHIDO

```
Dispatch Autônomo - Funcionalidade 11.3

Funcionalidade: 11.3 - Detecção de Maturidade via Snapshots
Roadmap: core/ROADMAP.md
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
