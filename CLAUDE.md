# CLAUDE.md — Instruções duráveis para Claude Code

> **Público:** Claude Code (CLI, Web, IDE) operando neste repositório.
> **Princípio:** estas instruções têm precedência sobre defaults do harness para
> os comportamentos abaixo. Demais regras (segurança, anti-redundância, processo)
> continuam vindo de `docs/`, `.claudecode.md` e `.cursorrules`.

---

## Autorização durável: modo autônomo abre a PR ao final do milestone

Sessões em modo autônomo deste repositório seguem o fluxo descrito em
[`docs/process/autonomous/`](docs/process/autonomous/). O **estado terminal da
fase de implementação é PR aberta** — a [RTE skill](skills/rte/skill.md) tem
como último passo obrigatório:

1. Atualizar `docs/process/current_implementation.md` (parte obrigatória do pacote de entrega)
2. Gerar `docs/process/current_validation.md` (rotativo — sobrescrito a cada novo milestone)
3. Commitar e fazer push da branch
4. **Abrir a PR via `mcp__github__create_pull_request`** com Seção 🎯 Validação
5. Transitar épicos para `🔀 Em revisão` no(s) ROADMAP(s) com link da PR

**Esta autorização é durável.** Quando o operador dispara um milestone autônomo
("implementa o `<MILESTONE>`", "vamos seguir na implementação de X", "roda
`<MILESTONE>`"), Claude Code está autorizado a executar o ciclo inteiro até a
abertura da PR sem pedir confirmação adicional. O default do harness ("não
abrir PR sem pedido explícito") **não se aplica** neste fluxo — o pedido foi
feito de forma durável aqui.

**Limite explícito (NÃO autorizado):**
- ❌ **Merge automático.** Aprovação humana segue obrigatória — dev revisa via
  Copilot na PR e mergeia pela interface do GitHub.
- ❌ **Force push** em qualquer branch.
- ❌ **Push direto em `main`.**
- ❌ **Mudanças em `.env`, segredos, configurações de CI** sem pedido explícito.

**Quando confirmar mesmo assim:**
- Disparo ambíguo (id de milestone não identificável) — perguntar antes.
- Fluxo manual (Cursor, sessão de refinamento) — defaults restritos do harness
  e do `.cursorrules` continuam valendo. Esta autorização cobre apenas o modo
  autônomo descrito em `docs/process/autonomous/`.

---

## Regra durável: sempre trazer sugestão com trade-offs

Quando uma decisão estrutural surgir no meio de uma sessão (estratégica, de
refinamento ou de implementação) e houver mais de um caminho razoável, **não
pergunte sem opinião**. Traga uma sugestão explícita com trade-offs.

**Forma esperada:**

1. **Recomendação direta** — qual caminho você acha que faz sentido.
2. **Por quê** — 1-3 razões objetivas, ancoradas no contexto do repo (acoplamento
   entre épicos, sinal real de atrito, princípios da vision/CONSTITUTION).
3. **Tradeoff principal** — o que se perde com a recomendação ou em que cenário
   ela falha. Tabela curta quando ajudar a comparar opções.
4. **Pergunta final** — "topa por aí ou queres ajustar antes?"

O operador decide. A regra não força aceitar a sugestão — força a sessão a
não desperdiçar bandwidth com perguntas abertas tipo "o que você prefere?"
sem material pra decidir em cima.

**Quando não aplica:**

- Decisões puramente operacionais (qual nome de variável, qual comando shell)
  — basta agir.
- Decisões já cobertas por instrução durável neste arquivo, em
  `docs/process/`, ou em skill carregada — seguir a instrução, não propor
  alternativa.
- Disparo ambíguo de milestone — perguntar identificação antes de agir
  (limite já declarado na seção anterior).

---

## Referências canônicas

- Workflow autônomo completo → [`docs/process/autonomous/workflow.md`](docs/process/autonomous/workflow.md)
- Como o operador dispara → [`docs/process/autonomous/dispatch.md`](docs/process/autonomous/dispatch.md)
- Como o operador valida → [`docs/process/autonomous/delivery.md`](docs/process/autonomous/delivery.md)
- Spec executável da RTE skill → [`skills/rte/skill.md`](skills/rte/skill.md)
- Descobertas de dev (ambiente, armadilhas) → [`.claudecode.md`](.claudecode.md)
- Regras do fluxo manual (Cursor) → [`.cursorrules`](.cursorrules)
