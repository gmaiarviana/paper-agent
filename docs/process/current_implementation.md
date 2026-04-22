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

1. **CONSTITUTION §1 "Fluxos Disponíveis"** (linha ~35) ainda descreve o fluxo autônomo como "Dev dispara pela manhã e valida à noite; skills automáticas (Planning → Dev → QA → TL → PO → Validation)". Isso contradiz o princípio novo de gates silenciosos/notificação por milestone e usa os nomes antigos das skills. **Escopo:** M3a (renomeações) e M4 (reescrita do fluxo autônomo). — _Nomes atualizados em M3a; reescrita do fluxo (pela-manhã/à-noite, gates silenciosos) fica em M4._

2. **CONSTITUTION §8 "Estrutura do Projeto"** ainda lista `skills/planning/` e `skills/validation/` na árvore. **Escopo:** M3a (renomeações) e M6 (varredura final de cross-refs). — _Resolvido em M3a._

3. **Comentários "Fluxo manual descrito nas seções 2-7 deste documento"** (linha ~34): as seções 2-7 falam principalmente do papel do Claude Web + Cursor; com a reforma, a separação entre manual e autônomo vai mais no lado do fluxo autônomo do que do manual. Texto coerente por ora; revisita em M5/M6 se necessário.

4. **`docs/process/refinement/planning_guidelines.md` linha 32** ainda fala em "5 arquivos essenciais" pelo nome, enquanto `starter.md` define o pack com 6. Inconsistência anterior à reforma. **Escopo:** M5 ou M6 (não entra em M1).

---

### Épico M2 — Camada de milestone nos ROADMAPs

**Status:** ✅ Concluído em 2026-04-22

**Objetivo:** criar a camada de milestone nos ROADMAPs existentes, agrupando épicos já escritos sob milestones dentro de cada estágio. Sem criar épicos novos, sem mudar conteúdo de épicos existentes.

#### Arquivos tocados

- `products/ensaio/ROADMAP.md` — seção `## 🎯 Milestones` nova antes de `## 📋 Épicos Planejados`. Milestones criados: **POC-ENSAIO** (E-POC-1, E-POC-2, E-POC-3; dep core C-ENSAIO-2), **PROTO-ENSAIO** stub (E-PROTO-1..5; dep core C-ENSAIO-3), **MVP-ENSAIO** stub (E-MVP-1..3; dep core C-ENSAIO-4).
- `products/revelar/ROADMAP.md` — seção `## 🎯 Milestones` nova. Milestone criado: **MVP-REVELAR** (ÉPICO 1 Observer, ÉPICO 2 Catálogo). Estágio identificado como MVP via `products/revelar/README.md` linha 21 ("MVP em desenvolvimento"). Épicos concluídos anteriores ao modelo de seis estados não são agrupados (regra de retroatividade).
- `products/produtor-cientifico/ROADMAP.md` — seção `## 🎯 Milestones` stub com placeholder citando nomenclatura esperada. Nenhum milestone criado.
- `products/prisma-verbal/ROADMAP.md` — seção `## 🎯 Milestones` stub com placeholder citando nomenclatura esperada. Nenhum milestone criado.
- `docs/ROADMAP.md` (core) — seção nova `## 🎯 Épicos Core × Milestones de Produto` com tabela mapeando: C-ENSAIO-1 → POC-ENSAIO (base de E-POC-2); C-ENSAIO-2 → POC-ENSAIO; C-ENSAIO-3 → PROTO-ENSAIO; C-ENSAIO-4 → MVP-ENSAIO; C-ENSAIO-5 e C-ENSAIO-6 sem milestone (condicionais). ÉPICO 1 Pesquisador sem vínculo.
- `docs/process/refinement/planning_guidelines.md` — na seção `## Estrutura do Roadmap`, bloco novo `### 🎯 MILESTONES` com definição (referenciando CONSTITUTION §9), convenção de id, regra de quebra por sizing (OVERFLOW do EM skill sempre quebra), template `### <ID>` com campos mínimos, e nota sobre onde vive a seção em cada ROADMAP.

#### Milestones criados (índice)

- **Ensaio:** POC-ENSAIO, PROTO-ENSAIO (stub), MVP-ENSAIO (stub)
- **Revelar:** MVP-REVELAR
- **Core:** nenhum (core não tem milestones próprios; tem tabela de vínculo)
- **Produtor Científico, Prisma Verbal:** nenhum (stubs de seção apenas)

#### Decisões tomadas durante a execução

1. **Estágio atual do Revelar = MVP** — identificado via `products/revelar/README.md` linha 21 ("MVP em desenvolvimento (Épicos 1-16)"). ÉPICO 1 e ÉPICO 2 do Revelar foram agrupados sob MVP-REVELAR.
2. **Revelar sem épicos concluídos para agrupar retroativamente** — o ROADMAP atual não lista épicos concluídos (foram podados antes da reforma). A nota de retroatividade foi preservada no milestone MVP-REVELAR.
3. **ÉPICO 2 do Revelar (Catálogo) em `📐 Funcionalidades esboçadas`** entra no milestone mesmo sem estar pronto para `🔍` — alinhado com o princípio de que PM skill (M3b) refina tático dentro da branch.
4. **Core não tem milestones próprios** — traduzido como tabela de vínculo `Épico Core × Milestone consumidor`. Alternativa rejeitada: criar "milestones core" sintéticos, porque violaria a convenção `<ESTAGIO>-<PRODUTO>` (não existe estágio de core isolado).
5. **Stubs de produto-futuro** (Produtor Científico e Prisma Verbal) usam placeholder textual, não tabela com milestones inventados — alinhado com a restrição "não inventar milestones que ainda não existem como intenção".
6. **C-ENSAIO-1 mapeado para POC-ENSAIO** — baseado na observação de que E-POC-2 do Ensaio já é consumidor concreto desse padrão (seu título é "Configuração de Contexto de Produto para Agentes do Core"). Se houver intenção diferente, essa entrada da tabela pode ser corrigida em sessão futura.

#### Inconsistências observadas (não corrigidas em M2 — escopo de milestones posteriores)

1. **`products/revelar/README.md` linha 21** fala em "Épicos 1-16" mas o ROADMAP só tem ÉPICO 1 e ÉPICO 2 ativos. Os demais (3-16) foram podados sem deixar resumo no ROADMAP. Não afeta M2 nem nenhum milestone da reforma, mas vale eventual saneamento do README do Revelar fora da reforma.
2. **ÉPICO 1 Pesquisador no core ROADMAP** tem dependência declarada "Revelar ÉPICO 2 (Catálogo de Conceitos)" mas permanece em `🌱 Visão` sem milestone consumidor. Consistente — Pesquisador só vira milestone quando virar consumidor de algum produto. Ficou registrado na tabela como "— (não vinculado)".
3. **ÉPICO 2 do Revelar (Catálogo)** depende internamente de ÉPICO 1 (Painel Observer). Ambos caem no mesmo milestone MVP-REVELAR — a dependência interna é resolvida como ordem de execução dentro do milestone, não como quebra em milestones separados. Se EM skill em M3b decidir quebrar (MVP-REVELAR-ALPHA/BETA), cada um fica com 1 épico.

---

### Épico M3a — Renomeações de skills + referências cruzadas

**Status:** ✅ Concluído em 2026-04-22

**Objetivo:** renomear `skills/planning/` → `skills/scrum-master/` e `skills/validation/` → `skills/rte/`, e atualizar todas as referências cruzadas no repo. Mecânico. Sem criar conteúdo novo.

#### Renomeações (git mv)

- `skills/planning/` → `skills/scrum-master/` (preservando histórico; 3 arquivos: README.md, skill.md, examples/clarification-example.md)
- `skills/validation/` → `skills/rte/` (preservando histórico; 3 arquivos: README.md, skill.md, templates/delivery-report.md)

#### Arquivos com referências atualizadas (12)

- `skills/scrum-master/skill.md` — cabeçalho, papel, markers `[PLANNING]` → `[SCRUM-MASTER]`, `[VALIDATION]` → `[RTE]`, status dos gates, bloco de bloqueio
- `skills/scrum-master/README.md` — cabeçalho, localização, autorreferências
- `skills/scrum-master/examples/clarification-example.md` — menções a "Planning Skill" e "🛑 Planning bloqueado"
- `skills/rte/skill.md` — cabeçalho, papel, status dos gates, markers, mensagens de abort/avançar
- `skills/rte/README.md` — cabeçalho, localização, referência a "Planning" na tabela de skills anteriores
- `skills/rte/templates/delivery-report.md` — linha "Template usado por RTE Skill", tabela de status, mensagem de próximo passo
- `skills/qa/README.md` — seção "Diferenças da RTE Skill"
- `skills/qa/skill.md` — markers no gate de entrada
- `skills/tl/skill.md` — markers + referência a plano de tasks
- `skills/po/README.md` — referências a "Planning" como roteamento de rejeição e próximo gate
- `skills/po/skill.md` — referências em gate de entrada, roteamento, próximo gate
- `skills/po/templates/acceptance-criteria.md` — roteamento e próximo passo
- `skills/README.md` — tabelas de skills (ordem + links), protocolo de carregamento, comunicação por artefatos
- `docs/process/autonomous/dispatch.md` — lista de skill.md a carregar, modo autônomo descritivo, entrega esperada
- `docs/process/autonomous/workflow.md` — cabeçalho, diagrama do fluxo, seção "1. Scrum Master Skill" e "6. RTE Skill", referências a `skills/<nome>/skill.md`
- `docs/process/autonomous/overview.md` — resumo do fluxo, responsabilidades das skills, tabela manual×autônomo
- `docs/process/autonomous/delivery.md` — referências ao nome da skill que notifica
- `docs/CONSTITUTION.md` — §1 "Fluxos Disponíveis" (nomes no pipeline) e §8 árvore de pastas
- `.github/copilot-instructions.md` — menção a quem cria e finaliza `current_implementation.md`

#### Arquivos fora da lista inicial do usuário onde o grep acusou

- `skills/po/templates/acceptance-criteria.md` — não estava listado explicitamente na instrução, mas o grep acusou e o arquivo é template consumido pela PO Skill. Atualizado.
- `skills/scrum-master/examples/clarification-example.md` — idem (conteúdo do example usa o nome antigo). Atualizado.
- `skills/rte/templates/delivery-report.md` — idem. Atualizado.

#### NÃO foi tocado (dentro do princípio mecânico)

- Descrição do fluxo "disparar pela manhã / validar à noite" em `docs/CONSTITUTION.md:35` e `docs/process/autonomous/overview.md` — mantida como está; reescrita é escopo de M4.
- `docs/process/autonomous/session_conventions.md` — grep inicial listou, mas os hits eram "validação" (substantivo em português) em contexto não-skill. Zero alteração necessária.
- Seções do fluxo que descrevem gates per-funcionalidade — mantidas; reescrita é escopo de M4.

#### Verificação final

`grep -rn "Planning Skill\|Validation Skill\|skills/planning\|skills/validation" docs/ skills/ .github/`:
- 0 hits em `docs/`, `skills/`, `.github/` fora de `current_implementation.md`.
- 1 hit em `docs/process/current_implementation.md:96` — nota histórica de M1 que registra o trabalho de M3a; deliberada, conforme combinado.

#### Inconsistências observadas durante a execução

1. `skills/po/templates/acceptance-criteria.md` e `skills/scrum-master/examples/clarification-example.md` não estavam na lista inicial do usuário mas tinham refs. Atualizados para consistência.
2. Markers literais `[PLANNING]` e `[VALIDATION]` no campo "Evidências de carregamento de skill" foram atualizados para `[SCRUM-MASTER]` e `[RTE]` em todos os `skill.md` para manter consistência entre o nome da skill e o marker que ela grava. Decisão mecânica, não arquitetural — segue o nome do cargo.

---

### Épicos pendentes da reforma

- **M3b** — ⬜ pendente (criar skills/pm/, skills/em/, docs/process/sizing/)
- **M4** — ⬜ pendente (reescrita de docs/process/autonomous/ para milestone, incluindo descrição "pela manhã/à noite" e gates silenciosos)
- **M5** — ⬜ pendente (atualização de docs/process/refinement/)
- **M6** — ⬜ pendente (integrações e cross-refs finais)

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

### Sessão 2 — 2026-04-22 — M2

**Executado:** M2 completo em 1 commit.

**Arquivos tocados:**
- Modificado: `products/ensaio/ROADMAP.md` (seção 🎯 Milestones com POC-ENSAIO + stubs PROTO-ENSAIO, MVP-ENSAIO)
- Modificado: `products/revelar/ROADMAP.md` (seção 🎯 Milestones com MVP-REVELAR)
- Modificado: `products/produtor-cientifico/ROADMAP.md` (seção 🎯 Milestones stub)
- Modificado: `products/prisma-verbal/ROADMAP.md` (seção 🎯 Milestones stub)
- Modificado: `docs/ROADMAP.md` (seção 🎯 Épicos Core × Milestones de Produto com tabela de vínculo)
- Modificado: `docs/process/refinement/planning_guidelines.md` (bloco 🎯 MILESTONES em `## Estrutura do Roadmap` com convenção, regra de quebra e template)

**Observações:**
- Reforma pronta para disparar M3a na próxima sessão.
- Inconsistências observadas registradas no bloco M2 acima (README do Revelar, dep interna MVP-REVELAR). Nenhuma bloqueia M3a+.
- Mapeamento C-ENSAIO-1 → POC-ENSAIO foi inferido via consumidor (E-POC-2); revisar se a intenção for diferente.

### Sessão 2.1 — 2026-04-22 — Ajuste pós-validação de M2

**Executado:** ajuste cirúrgico do M2 em 1 commit, após review do Copilot.

**Motivo:** template de milestone em `planning_guidelines.md` e os 4 milestones criados (POC-ENSAIO, PROTO-ENSAIO, MVP-ENSAIO, MVP-REVELAR) não tinham campo `Objetivo`. Sem ele, milestone vira lista de épicos sem propósito declarado.

**Arquivos tocados (4):**
- Modificado: `docs/process/refinement/planning_guidelines.md` (campo `Objetivo` como primeiro item do template `### <ID>`)
- Modificado: `products/ensaio/ROADMAP.md` (objetivos em POC-ENSAIO, PROTO-ENSAIO, MVP-ENSAIO — stubs com direção provável marcada como "a definir")
- Modificado: `products/revelar/ROADMAP.md` (objetivo em MVP-REVELAR)
- Modificado: `docs/process/current_implementation.md` (esta seção)

**Observações:**
- Stubs de `produtor-cientifico` e `prisma-verbal` não foram tocados (ainda sem milestones reais, só placeholder).
- Nenhum outro campo dos milestones foi alterado. Nenhum conteúdo de épico foi alterado.

### Sessão 3 — 2026-04-22 — M3a

**Executado:** M3a completo em 1 commit único (renames + edições fizeram sentido juntos porque os arquivos renomeados também foram editados — git trata como RM).

**Escopo atacado:**
- Renomear `skills/planning/` → `skills/scrum-master/` e `skills/validation/` → `skills/rte/` via `git mv` (histórico preservado).
- Atualizar todas as referências cruzadas em skills/, docs/process/autonomous/, docs/CONSTITUTION.md e .github/copilot-instructions.md.
- Atualizar markers `[PLANNING]`/`[VALIDATION]` → `[SCRUM-MASTER]`/`[RTE]` e status `Planning ✅`/`Validation ✅` → `Scrum Master ✅`/`RTE ✅` para consistência com o nome novo.

**Arquivos tocados:** 6 renomeados + 12 modificados (total 18 paths no diff). Ver bloco do épico M3a para detalhes.

**Observações:**
- Branch pronta para disparar M3b na próxima sessão.
- Conteúdo operacional dos skill.md NÃO foi reescrito (ainda fala em "funcionalidade X.Y" e gates per-funcionalidade — escopo de M4).
- Descrição "disparar pela manhã e validar à noite" mantida — reescrita em M4.
- Grep final limpo exceto pela nota histórica em `current_implementation.md:96`, que é registro deliberado.
