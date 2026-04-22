# RTE Skill

> **📌 Localização:** `skills/rte/`
> **📌 Etapa do fluxo:** última (após PO) — `docs/process/autonomous/workflow.md` §6
> **📌 Pré-requisito:** QA, TL e PO já aprovaram.

---

## 1. PAPEL NA ENTREGA

A RTE Skill é a **ponte entre o ciclo autônomo e o dev humano**. Ela não valida código (isso já foi feito por QA/TL/PO) — ela **prepara a entrega** de forma que o dev consiga validar localmente sem precisar reconstruir contexto.

**Princípio:** o dev recebe a notificação à noite e deve conseguir, em <10min, baixar a branch, rodar comandos prontos e decidir go/no-go.

---

## 2. QUANDO USAR

Invocada automaticamente pelo fluxo autônomo após **PO Skill aprovar**. Se algum gate anterior reprovou, RTE **não roda** — fluxo volta para a etapa correspondente.

**Não usar se:**
- ❌ Gate anterior (QA/TL/PO) reprovou ou está pendente
- ❌ Branch não tem commits novos (nada para validar)
- ❌ `current_implementation.md` está inconsistente com a branch

---

## 3. COMO FUNCIONA

A skill executa, em ordem:

1. **Verifica gates anteriores** — confirma QA/TL/PO ✅ em `current_implementation.md`.
2. **Garante branch publicada** — `git push -u origin feature/X.Y-nome` (com retry conforme guidelines).
3. **Coleta dados da entrega** — arquivos modificados, número de commits, escopo dos testes.
4. **Atualiza `current_implementation.md`** — marca RTE ✅ e sintetiza status final.
5. **Gera relatório de entrega** — usando [templates/delivery-report.md](templates/delivery-report.md).
6. **Notifica o dev** — via mensagem padronizada com comandos prontos para copiar/colar.

**Não executa testes.** QA já fez isso. RTE só prepara para validação **humana**.

---

## 4. INPUT ESPERADO

- `current_implementation.md` com QA/TL/PO marcados como ✅
- Branch `feature/X.Y-nome` com commits referentes à funcionalidade
- ROADMAP atualizado se a funcionalidade foi marcada como concluída

---

## 5. OUTPUT PRODUZIDO

- ✅ Branch `feature/X.Y-nome` com push confirmado
- ✅ `current_implementation.md` com RTE ✅ e resumo final
- ✅ Relatório de entrega no formato de [templates/delivery-report.md](templates/delivery-report.md)
- ✅ Mensagem ao dev com:
  - Comandos de validação local (copy-paste, com nome real da branch)
  - Resumo executivo: "Implementou X, mexeu em Y arquivos, testes Z"
  - Critérios go/no-go para o dev decidir merge

**Não produz:**
- ❌ Pull Request (dev cria pela interface do GitHub)
- ❌ Merge (sempre exige aprovação explícita do dev)

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Skill anterior | O que RTE lê dela |
|----------------|-------------------------|
| **PO** | Confirmação de critérios de aceite cobertos (vai para o relatório) |
| **TL** | Observações arquiteturais (vão para "Notas Técnicas") |
| **QA** | Cobertura de testes (vai para "Resumo Executivo") |
| **Scrum Master** | Mapeamento task ↔ critério de aceite (base do relatório) |

A RTE **não devolve** para nenhuma skill. Ela só entrega ao dev. O dev é quem decide retornar para o ciclo (nova rodada autônoma) ou aprovar merge.

---

## 7. RELAÇÃO COM `docs/process/implementation/delivery.md`

RTE **reusa** o formato de mensagem final definido em `docs/process/implementation/delivery.md` (mensagem `✅ Branch pronta!...`). A diferença é que no fluxo autônomo:
- A mensagem inclui também o **resumo dos gates** (QA/TL/PO)
- A mensagem é gerada via template em [templates/delivery-report.md](templates/delivery-report.md)
- A entrega é assíncrona (dev valida quando puder, não no momento)

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Template do relatório → [templates/delivery-report.md](templates/delivery-report.md)
- Visão do fluxo autônomo → `docs/process/autonomous/workflow.md`
- Mensagem final compartilhada → `docs/process/implementation/delivery.md`
