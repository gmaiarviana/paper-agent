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

### Épico M3b — Criar PM, EM e infra de sizing

**Status:** ✅ Concluído em 2026-04-22

**Objetivo:** criar a PM Skill (refinamento tático dentro da branch), a EM Skill (sizing antes do Scrum Master) e a infra `docs/process/sizing/` (heurística + schema do histórico + arquivo JSONL vazio). Sem mexer em skills existentes nem em outros docs.

#### Artefatos criados (7 arquivos)

- `skills/pm/README.md` — papel, quando usar, como funciona, input/output, interação com outras skills, relação com Claude Web (complementar, não substituto).
- `skills/pm/skill.md` — prompt operacional. 10 regras não-negociáveis, 9 passos da sequência (pré-checagens; identificar épicos; leitura de contexto; aplicar checklist por épico nas 5 categorias; ajuste por estágio; detecção e resolução; bloco único de perguntas; atualizar ROADMAPs; commit). Critérios de sucesso e falha. Marker `[PM] skill carregada: skills/pm/skill.md ✅ <timestamp>`.
- `skills/em/README.md` — papel, quando usar, como funciona, input/output, interação com outras skills, calibração com histórico, relação com Claude Web.
- `skills/em/skill.md` — prompt operacional. 7 regras não-negociáveis, 9 passos da sequência (pré-checagens; coleta de dados; carregar heurística; calcular fator de risco; estimar LOC; decidir veredicto; PARA se OVERFLOW com proposta de quebra; persistir em history.jsonl; atualizar current_implementation.md). Critérios de sucesso e falha. Marker `[EM] skill carregada: skills/em/skill.md ✅ <timestamp>`.
- `docs/process/sizing/heuristic.md` — fórmula `LOC_estimado = Σ (funcionalidades × LOC_média_por_funcionalidade × fator_de_risco)`. Defaults consolidados (ver tabela ao fim do arquivo). Bootstrap e evolução com histórico. Critério de quebra para OVERFLOW.
- `docs/process/sizing/schema.md` — schema das linhas do JSONL (campos, tipos, origem EM ou RTE). Política de duas linhas por milestone (decisão pela EM com `session_outcome=pending`; fechamento pela RTE com `loc_actual` preenchido e `session_outcome` final). Append-only. Exemplo de ciclo completo.
- `docs/process/sizing/history.jsonl` — arquivo realmente vazio (JSONL não suporta comentários; schema vive em `schema.md`).

#### Decisões tomadas durante a execução

1. **Ordem de fluxo PM → EM** (não estava explícita no plano). PM precisa rodar antes do EM porque sem épicos em `🔍`, EM não tem `features_count` para a fórmula. EM aborta com mensagem clara se encontrar épico pré-`🔍`. PM é condicional (só roda se há pendente).
2. **JSONL realmente vazio.** JSONL não suporta comentários; schema vive em `schema.md`. Padrão consistente com formatos de log estruturado.
3. **Duas linhas por milestone no `history.jsonl`.** EM grava linha `pending` no início; RTE grava linha de fechamento com `loc_actual` real. Append-only preservado. Cada linha é autocontida (repete campos de identificação) para que filtros de calibragem rodem sem join.
4. **Markers `[PM]` e `[EM]` no `current_implementation.md`.** O template atual em `scrum-master/skill.md` ainda lista só os 5 markers antigos. PM e EM declaram o formato esperado; reescrita do template é trabalho de M4. Anotado nos `skill.md` como nota explícita.
5. **Defaults da heurística** (registrados em `heuristic.md`):
   - `LOC_média_por_funcionalidade` inicial = 200
   - `fator_de_risco_inicial` = 1.0; +0.3 por refatoração declarada; +0.3 por integração com sistema existente; +0.2 por dependência de core não-`✅`; máximo razoável por épico = 2.0
   - Threshold FIT ≤ 3000; TIGHT ≤ 6000; OVERFLOW > 6000
   - Bootstrap: defaults até `≥ 3` linhas FIT concluídas em `history.jsonl`
   - Janela da média móvel: últimas 10 linhas FIT concluídas
6. **`loc_actual` definido como `git diff --shortstat origin/main..HEAD` na branch do milestone, contando código + testes (excluindo docs e configs puras).** Detalhamento exato fica a cargo de M4 quando a RTE for reescrita; declarado no `schema.md` como ponto a fechar.
7. **PM commita na branch do milestone, não em main.** RTE faz o push do milestone inteiro depois. PM atualiza ROADMAPs locais; sem push automático.
8. **PM só toca em ROADMAPs e current_implementation.md.** EM só toca em history.jsonl e current_implementation.md. Restrito por design para evitar escopo creeping.

#### Inconsistências observadas (registradas, não tocadas em M3b)

1. **Template de `current_implementation.md` em `skills/scrum-master/skill.md` lista só 5 markers** (`[SCRUM-MASTER]`, `[QA]`, `[TL]`, `[PO]`, `[RTE]`). PM e EM precisam aparecer lá para o protocolo de carregamento ser completo. **Escopo:** M4 (reescrita do fluxo autônomo).
2. **`docs/process/autonomous/workflow.md`** ainda descreve o fluxo como `Scrum Master → Dev → QA → TL → PO → RTE`. PM e EM não estão no diagrama. **Escopo:** M4.
3. **Tabela em `skills/README.md`** lista 5 skills; PM e EM não aparecem. **Escopo:** M4 quando o orquestrador do fluxo for reescrito.
4. **`skills/scrum-master/skill.md` regra 5** ainda diz "refinamento em qualquer alvo é manual, via Claude Web; não é seu papel". Com a PM existindo, essa regra precisa ser atualizada para "refinamento tático é da PM Skill; Scrum Master só recebe épicos já em `🔍`". **Escopo:** M4.

#### Confirmação explícita

**PM e EM descrevem complementaridade com Claude Web, não substituição.** Verificado em:
- `skills/pm/README.md` §1 "Papel": "PM **não substitui Claude Web**. As duas modalidades de refinamento são complementares, com escopos distintos: Claude Web — refinamento estratégico ... PM Skill — refinamento tático ..."
- `skills/pm/README.md` §7 "Relação com Claude Web": reforço explícito.
- `skills/pm/skill.md` "Seu Papel": "Você **não substitui o Claude Web**. Refinamento estratégico ... continua exclusivo do Claude Web ..."
- `skills/em/README.md` §8 "Relação com Claude Web": "Claude Web decide o que entra no milestone (escopo, prioridade, divisão estratégica). EM decide se o milestone, como definido, cabe na sessão."
- `skills/em/skill.md` "Seu Papel": "Você **não substitui o Claude Web**. Claude Web decide o que entra no milestone ...; você decide se o que entrou cabe na sessão."

---

### Wrap-up — mínimo para deixar main consistente com PM/EM existindo

**Status:** ✅ Concluído em 2026-04-22

**Objetivo:** deixar a branch pronta para merge em main com consistência mínima (PM e EM referenciados onde o fluxo é definido) sem executar M4 completo. O restante (M4-restante, M5, M6) vira dívida documentada em `docs/process/refactor-backlog.md`.

**Ações executadas (5 + atualização desta âncora):**

1. **`skills/README.md`** — tabela de skills na §2 ganhou linhas PM (condicional, antes do EM) e EM (antes do Scrum Master). Protocolo de carregamento atualizado para citar PM → EM → Scrum Master → ... Tabela §5 "SKILLS DISPONÍVEIS" idem.
2. **`skills/scrum-master/skill.md`** — regra 5 reescrita: "Não refinar épicos. Refinamento tático dentro da branch é responsabilidade da PM skill (executada antes). Refinamento estratégico é do Claude Web (antes do dispatch). Scrum Master assume épicos em `🔍 Detalhes definidos` — se encontrar algum fora desse estado, abortar com mensagem dizendo que PM Skill deveria ter rodado."
3. **`skills/scrum-master/skill.md`** (template) — "Status dos Gates" e "Evidências de carregamento de skill" ganharam `[PM]` (primeiro) e `[EM]` (segundo). Nota de fechamento atualizada para explicar que PM é condicional.
4. **`docs/process/autonomous/workflow.md`** — cabeçalho e diagrama ASCII atualizados para `PM (condicional) → EM → Scrum Master → Dev → QA → TL → PO → RTE`. Parágrafos curtos abaixo do diagrama explicam a condicionalidade do PM e o papel do EM. Nota explícita de que o resto do arquivo (descrição operacional dos gates) ainda reflete o modelo per-funcionalidade e é dívida registrada em `refactor-backlog.md`.
5. **`docs/process/refactor-backlog.md`** (novo) — documenta a dívida aberta com 3 blocos (M4-restante, M5, M6), micro-dívidas detectadas, e seção vazia "Outras melhorias" para absorver ideias futuras de processo.
6. **`docs/process/current_implementation.md`** (esta seção) — registra o wrap-up e explicita que a reforma está pausada para merge.

**O que NÃO foi tocado (virou dívida em `refactor-backlog.md`):**

- `docs/process/autonomous/dispatch.md`, `overview.md`, `delivery.md`, `session_conventions.md` — corpo principal continua per-funcionalidade.
- Conteúdo operacional de `skills/scrum-master/skill.md` (além da regra 5 e do template), `skills/qa/skill.md`, `skills/tl/skill.md`, `skills/po/skill.md`, `skills/rte/skill.md` — continuam falando em "funcionalidade X.Y".
- `docs/process/refinement/*.md` — callouts de M1 permanecem como único tratamento do refinamento tático.
- `docs/CONTEXT_INDEX.md`, `docs/ARCHITECTURE.md`, `.github/copilot-instructions.md`, `README.md` — não mencionam PM/EM/sizing no mapa/árvore.
- Typo `IImplementado` — permanece; será resolvido em M6.

### Branch pronta para merge em main

- ✅ Reforma pausada após M3b + wrap-up.
- ✅ Dívida aberta migrada para `docs/process/refactor-backlog.md` (M4-restante, M5, M6 + micro-dívidas).
- ✅ `main` fica consistente: PM e EM existem como skills, estão citadas onde o fluxo é declarado (skills/README.md, workflow.md, template do scrum-master), e o backlog aponta exatamente o que falta.

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

### Sessão 4 — 2026-04-22 — M3b

**Executado:** M3b completo em 1 commit único (PM + EM + sizing infra são interdependentes na revisão e não fazem sentido isolados; commit único deixa o diff legível e reversível como bloco).

**Escopo atacado:**
- Criar `skills/pm/` (README.md + skill.md)
- Criar `skills/em/` (README.md + skill.md)
- Criar `docs/process/sizing/` (heuristic.md + schema.md + history.jsonl vazio)

**Arquivos criados:** 7 (todos novos; nenhum modificado fora dessa lista).

**Observações:**
- Branch pronta para disparar M4 na próxima sessão.
- PM e EM ainda não estão integrados ao fluxo descrito em `docs/process/autonomous/workflow.md` nem ao template em `skills/scrum-master/skill.md`. Integração é escopo de M4.
- Defaults da heurística são chute inicial e devem ser revisados após os 5 primeiros milestones reais (declarado em `heuristic.md`).
- Confirmação explícita de complementaridade Claude Web ↔ PM/EM registrada no bloco do épico M3b acima.

### Sessão 5 — 2026-04-22 — Wrap-up antes do merge em main

**Executado:** 5 ações cirúrgicas + atualização desta âncora, em 1 commit único para deixar `main` consistente com PM e EM existindo. M4-restante, M5, M6 pausados e migrados para `docs/process/refactor-backlog.md`.

**Arquivos tocados (5 modificados + 1 criado):**
- Modificado: `skills/README.md` (tabelas §2 e §5 + protocolo de carregamento com PM/EM)
- Modificado: `skills/scrum-master/skill.md` (regra 5 reescrita + template ganha `[PM]`/`[EM]` em Status dos Gates e Evidências)
- Modificado: `docs/process/autonomous/workflow.md` (cabeçalho + diagrama + parágrafos PM condicional / EM primeiro gate + nota sobre dívida do resto)
- Criado: `docs/process/refactor-backlog.md` (dívida aberta M4-restante/M5/M6 + micro-dívidas + seção "Outras melhorias")
- Modificado: `docs/process/current_implementation.md` (wrap-up registrado; bloco "branch pronta para merge")

**Observações:**
- Branch `refactor/fluxo-milestone` pronta para merge em `main` (decisão do dev; esta sessão não faz merge nem PR).
- Reforma PAUSADA após M3b + wrap-up. Retomar com M4-restante conforme bloco em `refactor-backlog.md`.
- Nada fora do escopo cirúrgico foi tocado: dispatch/overview/delivery/session_conventions continuam per-funcionalidade; conteúdo operacional dos demais skill.md intacto; refinement/ intacto; CONTEXT_INDEX/ARCHITECTURE/copilot-instructions/README intactos.
