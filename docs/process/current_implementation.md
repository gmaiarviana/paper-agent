# Implementação Atual: REFATORA-FLUXO-MILESTONE

**Branch:** refactor/fluxo-milestone
**Modo:** Reforma do processo (fora do fluxo autônomo padrão)
**Iniciada em:** 2026-04-22

> **Nota:** Este arquivo é a **âncora de estado** da reforma que introduz "milestone" como unidade de entrega. Ele segue o shape novo definido pela reforma (arquivo único com blocos aninhados por milestone → épicos → funcionalidades → gates), mas é consumido manualmente entre sessões — não passa pelos gates automáticos porque a própria reforma cria esses gates. Depois que a reforma fechar, este arquivo é removido e o shape passa a ser produzido pelas skills.

---

## Escopo da reforma

Trocar a unidade de entrega do fluxo autônomo de **funcionalidade** para **milestone** (agrupamento de épicos dentro de um estágio POC/Protótipo/MVP). Introduzir skills PM e EM, renomear Planning→Scrum Master e Validation→RTE, tornar dispatch em linguagem natural, silenciar gates intermediários, consolidar notificação no fim do milestone inteiro.

## Plano aprovado

- **M1** — Vocabulário e princípio da CONSTITUTION
- **M2** — Camada de milestone nos ROADMAPs
- **M3a** — Renomeações de skills (planning→scrum-master, validation→rte) + atualização de referências cruzadas
- **M3b** — Criação das skills PM e EM + infra `docs/process/sizing/`
- **M4** — Reescrita do fluxo autônomo por milestone (`docs/process/autonomous/`)
- **M5** — Refinamento autônomo dentro da branch (`docs/process/refinement/`)
- **M6** — Integrações e cross-references (CONTEXT_INDEX, copilot-instructions, ARCHITECTURE tree, varredura final)

## Decisões fixadas

1. Shape de `current_implementation.md` novo: **arquivo único com blocos aninhados** (milestone → épicos → funcionalidades → gates).
2. Escalação com gates silenciosos: **3 reprovações consecutivas no mesmo gate do mesmo épico → aborta milestone inteiro e notifica** (sem agregar entre épicos).
3. Fluxo manual via Cursor continua como está; ganha apenas nota de escopo no topo de `docs/process/implementation/overview.md` em M6.
4. EM não aceita OVERFLOW: sempre devolve ao dev pedindo quebra em 2 milestones. TIGHT segue sem aval.
5. POC do Ensaio espera a reforma fechar e estreia o fluxo novo (milestone `POC-ENSAIO`). Nada implementado no fluxo antigo em paralelo.
6. Id de milestone: formato `<ESTAGIO>-<PRODUTO>` em caixa alta com hífen (ex.: `POC-ENSAIO`, `PROTO-REVELAR`). Sufixo quando múltiplo: `POC-ENSAIO-ALPHA`, `POC-ENSAIO-BETA`. Branch em caixa baixa: `milestone/poc-ensaio`.
7. Skills: manter acrônimos. Diretórios: `skills/pm/`, `skills/em/`, `skills/scrum-master/`, `skills/qa/`, `skills/tl/`, `skills/po/`, `skills/rte/`.

---

## Épicos da reforma

### Épico M1 — Vocabulário e princípio da CONSTITUTION

**Status:** ✅ Concluído em 2026-04-22

**Objetivo:** introduzir "milestone" como unidade de entrega no texto fundador do projeto e trocar o princípio "Claude Code não refina épicos" pelo princípio novo, sem criar nenhum dos skills/ arquivos operacionais ainda.

#### Funcionalidades

##### M1.1 Introduzir "milestone" em CONSTITUTION §1 ✅

- **Descrição:** §1 "Princípios de Trabalho" ganha menção explícita a milestone como unidade de entrega do fluxo autônomo.
- **Arquivo tocado:** `docs/CONSTITUTION.md` (nova subseção "Unidade de Entrega" no topo de §1, mais ajustes em "Como Refinamos" e "Como Implementamos" para mencionar milestone, branch própria e aval humano).

##### M1.2 Trocar princípio de refinamento em CONSTITUTION §2 ✅

- **Descrição:** remover proibição absoluta "Claude Code não refina épicos" e substituir pelo princípio novo.
- **Arquivo tocado:** `docs/CONSTITUTION.md` — seção "Claude Code (Implementador)" reescrita. "Não deve: refinar épicos" foi removido; "Deve: no fluxo autônomo, refinar épicos de um milestone..." adicionado; bloco "Princípio de refinamento na reforma" explicitado com estratégico vs tático e regra de main.

##### M1.3 Atualizar CONSTITUTION §3 (output esperado) ✅

- **Descrição:** o modelo "PROMPT 1..N para Cursor" vira caso particular do fluxo manual.
- **Arquivo tocado:** `docs/CONSTITUTION.md` — §3 "Output Esperado" agora distingue dois formatos: (A) sessão estratégica (lista de milestones/épicos, sem prompts) e (B) sessão de preparação para fluxo manual (prompts por arquivo). Nota final explicita que refinamento tático não passa por Claude Web nem por Cursor.

##### M1.4 Adicionar Glossário em CONSTITUTION ✅

- **Descrição:** nova subseção com 4 termos.
- **Arquivo tocado:** `docs/CONSTITUTION.md` — §9 "Glossário" criada com Estágio, Milestone (incluindo convenção de id e nome de branch), Épico e Funcionalidade. Atualizada linha de versão/data.

##### M1.5 Nota sobre refinamento dentro da branch em planning_guidelines.md ✅

- **Descrição:** seção "Seis Estados" ganha nota sobre refinamento tático dentro da branch.
- **Arquivo tocado:** `docs/process/refinement/planning_guidelines.md` — callout logo abaixo do cabeçalho "Seis Estados de Refinamento" explicando as duas modalidades (preparação antecipada via Claude Web vs PM skill dentro da branch) e que ambas usam o mesmo checklist.

##### M1.6 Distinguir refinamento estratégico vs tático em planning_guidelines.md ✅

- **Descrição:** seção "Claude Web Deve" ganha nota separando estratégico vs tático.
- **Arquivo tocado:** `docs/process/refinement/planning_guidelines.md` — callout logo abaixo do cabeçalho "Claude Web Deve" distinguindo estratégico (externo ao repo) de tático (PM skill). PM skill referenciada explicitamente como "a ser criada em M3b da reforma do fluxo".

#### Gates do épico M1

Não aplicáveis nesta reforma. A execução foi manual pelo dev, revisada fora do ciclo de skills.

- [x] Três arquivos tocados em total (1 novo + 2 modificados)
- [x] Nenhum arquivo fora do escopo declarado foi tocado
- [x] Typo "refinar epicamente ainda pendentes" → "refinar épicos ainda pendentes" corrigido antes do commit

#### Critério de aceite do épico M1 — conferência final

- [x] CONSTITUTION menciona "milestone" como unidade de entrega em §1 (subseção "Unidade de Entrega").
- [x] CONSTITUTION §2 não contém mais a proibição absoluta "Claude Code não refina épicos".
- [x] CONSTITUTION tem subseção Glossário (§9) com 4 termos.
- [x] planning_guidelines.md distingue refinamento estratégico vs tático, referenciando PM skill como "a ser criada em M3b".

#### Inconsistências observadas (não corrigidas em M1 — escopo de milestones posteriores)

1. **CONSTITUTION §1 "Fluxos Disponíveis"** (linha ~35) ainda descreve o fluxo autônomo como "Dev dispara pela manhã e valida à noite; skills automáticas (Planning → Dev → QA → TL → PO → Validation)". Isso contradiz o princípio novo de gates silenciosos/notificação por milestone e usa os nomes antigos das skills. **Escopo:** M3a (renomeações) e M4 (reescrita do fluxo autônomo).

2. **CONSTITUTION §8 "Estrutura do Projeto"** ainda lista `skills/planning/` e `skills/validation/` na árvore. **Escopo:** M3a (renomeações) e M6 (varredura final de cross-refs).

3. **Comentários "Fluxo manual descrito nas seções 2-7 deste documento"** (linha ~34): as seções 2-7 falam principalmente do papel do Claude Web + Cursor; com a reforma, a separação entre manual e autônomo vai mais no lado do fluxo autônomo do que do manual. Texto coerente por ora; revisita em M5/M6 se necessário.

4. **`docs/process/refinement/planning_guidelines.md` linha 32** ainda fala em "5 arquivos essenciais" pelo nome, enquanto `starter.md` define o pack com 6. Inconsistência anterior à reforma. **Escopo:** M5 ou M6 (não entra em M1).

---

### Épicos pendentes da reforma

- **M2** — ⬜ pendente
- **M3a** — ⬜ pendente
- **M3b** — ⬜ pendente
- **M4** — ⬜ pendente
- **M5** — ⬜ pendente
- **M6** — ⬜ pendente

---

## Histórico de sessões

### Sessão 1 — 2026-04-22 — M1

**Executado:** M1 completo em 1 commit.

**Arquivos tocados:**
- Criado: `docs/process/current_implementation.md` (este arquivo — âncora da reforma)
- Modificado: `docs/CONSTITUTION.md` (§1 Unidade de Entrega, §2 Claude Code, §3 Output Esperado, §9 Glossário novo)
- Modificado: `docs/process/refinement/planning_guidelines.md` (2 callouts: "Claude Web Deve" e "Seis Estados de Refinamento")

**Observações:**
- Reforma continua pronta para disparar M2 na próxima sessão.
- Branch local `refactor/fluxo-milestone` sem push (instrução do dev).
- Inconsistências herdadas detectadas e registradas para M3a/M4/M5/M6 (ver bloco "Inconsistências observadas" em M1 acima).
