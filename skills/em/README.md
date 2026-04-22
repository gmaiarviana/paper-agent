# EM Skill (Engineering Manager)

> **📌 Localização:** `skills/em/`
> **📌 Etapa do fluxo:** primeiro gate avaliativo, **após** PM (se PM rodou) e **antes** do Scrum Master — `docs/process/autonomous/workflow.md` (a ser reescrito em M4 da reforma do fluxo)
> **📌 Pré-requisito:** todos os épicos do milestone estão em `🔍 Detalhes definidos` (ou superior). Se algum estiver pré-`🔍`, EM aborta sinalizando que PM deveria ter rodado.

---

## 1. PAPEL

A EM Skill faz **sizing** do milestone antes de a implementação começar. Lê o milestone, conta funcionalidades por épico, aplica o fator de risco declarado em `docs/process/sizing/heuristic.md` e gera uma estimativa de LOC. Decide entre três veredictos:

- **FIT** — cabe numa sessão. Fluxo segue para Scrum Master sem alarde.
- **TIGHT** — aperta mas segue. Registra alerta em `current_implementation.md` para o dev ficar atento; fluxo segue.
- **OVERFLOW** — estoura. PARA e devolve ao dev com proposta de quebra do milestone em sub-milestones (`<ID>-ALPHA`/`<ID>-BETA`).

EM persiste a decisão (entrada + estimativa + veredicto) em `docs/process/sizing/history.jsonl`. RTE complementa essa linha (ou adiciona uma segunda linha) no fim do milestone com `loc_actual` real e `session_outcome`. Esse histórico calibra a heurística ao longo do tempo.

---

## 2. QUANDO USAR

Use quando todas as condições abaixo forem verdadeiras:

- Milestone disparado tem todos os épicos em `🔍 Detalhes definidos` ou superior (PM já rodou ou foi pulado por já estarem refinados).
- Branch `milestone/<id-em-caixa-baixa>` ativa.
- `docs/process/sizing/heuristic.md` e `docs/process/sizing/history.jsonl` existem e são acessíveis.

**Não usar se:**
- ❌ Algum épico do milestone está em `🌱`, `📐` ou `📋` — PM precisa rodar antes (ou ser chamado a rodar).
- ❌ Milestone é stub puro sem épicos agrupados — sizing não faz sentido; devolver ao dev.

---

## 3. COMO FUNCIONA

A skill executa, em ordem:

1. **Pré-checagens** — branch, milestone, todos os épicos em `🔍`+, heurística carregável.
2. **Coleta de dados** — épicos do milestone, número de funcionalidades por épico, dependências de core ainda não em `✅`, presença de termos de risco ("refatora", "integra com", etc).
3. **Carrega heurística** — lê `docs/process/sizing/heuristic.md` e a calibragem corrente em `docs/process/sizing/history.jsonl`.
4. **Aplica fórmula** — `LOC_estimado = Σ (épicos) (funcionalidades × LOC_média_por_funcionalidade × fator_de_risco)`.
5. **Decide veredicto** — FIT / TIGHT / OVERFLOW segundo os thresholds da heurística.
6. **Persistência** — append de uma linha em `history.jsonl` no formato definido em `docs/process/sizing/schema.md`.
7. **Atualiza `current_implementation.md`** — registra evidência de carregamento, decisão e estimativa.
8. **Resultado** — FIT/TIGHT seguem para Scrum Master; OVERFLOW PARA com proposta de quebra.

---

## 4. INPUT ESPERADO

- `<id do milestone>` (ex.: `POC-ENSAIO`)
- ROADMAP de produto + `docs/ROADMAP.md` (para épicos core)
- `docs/process/sizing/heuristic.md` (algoritmo)
- `docs/process/sizing/history.jsonl` (calibragem com base em milestones anteriores)
- `docs/process/current_implementation.md` (para escrever a evidência e a decisão)

---

## 5. OUTPUT PRODUZIDO

- ✅ Linha nova em `docs/process/sizing/history.jsonl` no schema declarado, com `loc_actual: null` e `session_outcome: pending` (a ser completado pela RTE no fim do milestone)
- ✅ Bloco em `current_implementation.md` registrando: épicos avaliados, número de funcionalidades, fator de risco aplicado, LOC estimado, decisão, alerta (se TIGHT) ou proposta de quebra (se OVERFLOW)
- ✅ Decisão clara: **FIT** | **TIGHT** | **OVERFLOW**

**Não produz:**
- ❌ Plano de tasks (escopo do Scrum Master)
- ❌ Decisão de quebra automática do milestone (sempre devolve ao humano)
- ❌ Alteração de ROADMAP

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Próxima ação |
|---------|--------------|
| FIT | Fluxo segue para **Scrum Master** sem aval do dev |
| TIGHT | Fluxo segue para **Scrum Master**; alerta registrado para o dev ler na entrega |
| OVERFLOW | PARA e devolve ao dev com proposta `<ID>-ALPHA`/`<ID>-BETA`. Não tenta emendar sessões. |
| Algum épico pré-`🔍` | ABORTA — PM precisa rodar ou ser chamado |

EM **não corrige milestone**. Não quebra automaticamente. Não força execução em pedaços. Devolve ao dev para decisão humana.

---

## 7. CALIBRAÇÃO COM O HISTÓRICO

A heurística começa simples (defaults em `heuristic.md`) e calibra ao longo do tempo lendo `history.jsonl`. Bootstrap: enquanto `history.jsonl` tem menos de 3 linhas FIT concluídas, EM usa os defaults. A partir da 3ª linha FIT concluída, EM calcula a média móvel de `LOC_actual / features_count` dos milestones FIT e usa como `LOC_média_por_funcionalidade` ajustado.

Os thresholds (FIT/TIGHT/OVERFLOW) também devem ser revisados após os 5 primeiros milestones — esse é trabalho explícito de calibração registrado em `heuristic.md`.

---

## 8. RELAÇÃO COM CLAUDE WEB

EM **não substitui o Claude Web**. As decisões são complementares:

- Claude Web decide **o que entra no milestone** (escopo, prioridade, divisão estratégica).
- EM decide **se o milestone, como definido, cabe na sessão**.

Quando EM retorna OVERFLOW, é o dev humano (apoiado por Claude Web se quiser) que decide como quebrar — não a skill.

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Heurística → [docs/process/sizing/heuristic.md](../../docs/process/sizing/heuristic.md)
- Schema do histórico → [docs/process/sizing/schema.md](../../docs/process/sizing/schema.md)
- Próximo gate (Scrum Master) → [skills/scrum-master/README.md](../scrum-master/README.md)
