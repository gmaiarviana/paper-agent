# Workflow Autônomo: Scrum Master → Dev → QA → TL → PO → RTE

> **📌 Localização:** `docs/process/autonomous/`
> **📌 Público:** Claude Code Web operando em modo autônomo.
> **📌 Princípio:** cada skill é um gate. Reprovou → volta para a etapa anterior antes de avançar.
> **📌 Obrigatório:** antes de executar cada gate, abrir e seguir o `skill.md` correspondente (prompt operacional). Este arquivo descreve o fluxo geral; o `skill.md` de cada gate é a spec executável — não substituir um pelo outro.

---

## FLUXO GERAL

```
Dispatch → Scrum Master Skill → Dev → QA Skill → TL Skill → PO Skill → RTE Skill → Dev valida
                ↑              ↑       ↑         ↑          ↑
                └──── reprovou? volta para a etapa anterior ────┘
```

---

## 1. SCRUM MASTER SKILL

> **📌 Spec executável obrigatória:** `skills/scrum-master/skill.md` — carregar antes de iniciar este gate.

**Objetivo:** transformar funcionalidade do ROADMAP em plano de implementação executável.

**Verificação inicial (gate de entrada):**
- ✅ Abrir ROADMAP indicado no dispatch e localizar a funcionalidade X.Y
- ✅ Confirmar que o épico pai está marcado como **`🔍 Detalhes definidos`**
- ✅ Confirmar que a funcionalidade traz os detalhes de execução produzidos por sessão de refinamento com alvo `🔍` (arquivos-alvo, contratos/shapes, mecanismo de integração, template de referência, acoplamentos, escopo de teste)

**Se a verificação falhar — abortar imediatamente:**
- Se o épico está em `🌱 Visão` ou `📐 Funcionalidades esboçadas` → devolver ao dev com mensagem: "Épico precisa de sessão de refinamento antes do dispatch autônomo. Ver `docs/process/refinement/planning_guidelines.md`."
- Se o épico está em `📋 Critérios definidos` → devolver ao dev com mensagem: "Épico em `📋 Critérios definidos`. Sessão de refinamento com alvo `🔍 Detalhes definidos` é feita manualmente via Claude Web, aplicando o checklist de `docs/process/refinement/autonomous_readiness.md`, antes de redispachar."
- Em todos os casos, a skill **não tenta suprir a lacuna inventando detalhes**.

**Deve (após gate de entrada aprovado):**
- ✅ Ler `docs/ARCHITECTURE.md` e docs técnicas relevantes (via `docs/CONTEXT_INDEX.md`)
- ✅ Quebrar a funcionalidade em tarefas ordenadas por dependência, respeitando a sequência declarada no épico
- ✅ Identificar dúvidas técnicas remanescentes e **resolvê-las consultando docs antes de assumir**
- ✅ Documentar plano em `docs/process/current_implementation.md` (mesmo arquivo do fluxo manual)
- ✅ Reutilizar arquivos esperados e template de referência declarados no épico; não redefinir por conta própria

**Não deve:**
- ❌ Tomar decisões arquiteturais novas (se necessário, abortar e devolver ao dev)
- ❌ Refinar épico (refinamento em qualquer alvo — `📋` ou `🔍` — é manual, via Claude Web)
- ❌ Avançar para Dev se a funcionalidade não estiver em épico `🔍 Detalhes definidos`

**Saída:** plano em `current_implementation.md` + lista de tarefas.

---

## 2. DEV (Implementação)

**Objetivo:** implementar tarefas do plano seguindo `docs/process/implementation/`.

**Deve:**
- ✅ Seguir [implementation.md](../development/implementation.md) (TDD pragmático, ciclo Red-Green-Refactor)
- ✅ Seguir [quality_rules.md](../development/quality_rules.md) (anti-redundância, padrões)
- ✅ Atualizar docs estruturais quando alterar estrutura
- ✅ Commits incrementais e descritivos

**Não deve:**
- ❌ Inventar funcionalidades fora do plano
- ❌ Criar docs extras sem necessidade (ver anti-padrões em CONSTITUTION)

**Saída:** código + testes + docs atualizadas, prontos para QA.

---

## 3. QA SKILL

> **📌 Spec executável obrigatória:** `skills/qa/skill.md` — carregar antes de iniciar este gate.

**Objetivo:** validar qualidade técnica antes de seguir.

**Deve verificar:**
- ✅ Suite de testes passa (unit + integration aplicáveis)
- ✅ Sintaxe Python OK em todos os arquivos modificados
- ✅ Imports resolvem sem erro circular
- ✅ Comportamento esperado coberto (smoke / behavior conforme `docs/testing/strategy.md`)
- ✅ Sem warnings críticos no console
- ✅ Markers `integration` / `slow` aplicados corretamente

**Reprova quando:**
- ❌ Algum teste falha ou foi pulado sem justificativa
- ❌ Imports quebram em arquivos impactados (busca por chamadas a funções modificadas)
- ❌ Falta cobertura em lógica crítica nova

**Ação ao reprovar:** retornar ao Dev com lista de problemas + arquivos afetados.

**Saída:** relatório de validação técnica.

---

## 4. TL SKILL (Tech Lead)

> **📌 Spec executável obrigatória:** `skills/tl/skill.md` — carregar antes de iniciar este gate.

**Objetivo:** validar arquitetura, padrões e aderência ao ROADMAP técnico.

**Deve verificar:**
- ✅ Implementação alinhada com `docs/ARCHITECTURE.md`
- ✅ Padrões dos agentes/módulos similares preservados
- ✅ Sem duplicação de informação entre docs (ver `.claudecode.md` e CONSTITUTION §6)
- ✅ Estrutura de pastas e nomenclatura coerente com convenções existentes
- ✅ Decisões técnicas documentadas onde apropriado

**Reprova quando:**
- ❌ Introduziu padrão divergente sem justificativa
- ❌ Quebrou decisões arquiteturais documentadas
- ❌ Documentação estrutural desalinhada do código

**Ação ao reprovar:** retornar ao Dev com pontos de divergência arquitetural.

**Saída:** parecer arquitetural (aprovado / aprovado com observações / reprovado).

---

## 5. PO SKILL (Product Owner)

> **📌 Spec executável obrigatória:** `skills/po/skill.md` — carregar antes de iniciar este gate.

**Objetivo:** validar critérios de aceite da funcionalidade.

**Deve verificar:**
- ✅ Cada critério de aceite do ROADMAP está atendido (mapear 1-a-1)
- ✅ Comportamentos "deve / não deve" cobertos por teste OU script de validação
- ✅ Funcionalidade entrega valor incremental (mesmo isolada)
- ✅ ROADMAP marcado como concluído quando aplicável

**Reprova quando:**
- ❌ Algum critério de aceite não está coberto/observável
- ❌ Comportamento "não deve" não foi validado

**Ação ao reprovar:** retornar ao Scrum Master ou Dev (dependendo se é gap de plano ou de implementação).

**Saída:** checklist de aceite com status por critério.

---

## 6. RTE SKILL

> **📌 Spec executável obrigatória:** `skills/rte/skill.md` — carregar antes de iniciar este gate.

**Objetivo:** preparar entrega para o dev validar manualmente.

**Deve:**
- ✅ Garantir branch `feature/X.Y-nome` com push realizado
- ✅ Atualizar `docs/process/current_implementation.md` (marcar checkpoints concluídos)
- ✅ Gerar mensagem final no formato definido em [delivery.md](delivery.md)
- ✅ Listar comandos de validação local prontos para copiar/colar (com nome real da branch)
- ✅ Listar critérios de aceite + validações esperadas (o que dev deve observar)
- ✅ Notificar o dev (canal acordado: notificação Claude Code Web)

**Não deve:**
- ❌ Criar PR automaticamente
- ❌ Mergear sem aprovação explícita do dev
- ❌ Pular gates anteriores ainda que considere "trivial"

**Saída:** branch pronta + mensagem final + notificação ao dev.

---

## TRANSIÇÃO DE ESTADO DO ÉPICO

O fluxo autônomo manipula dois estados de execução do épico no ROADMAP:

- **`🏗️ Em andamento`** — marcado assim que a Scrum Master Skill conclui (a partir daí o épico está sob implementação pelas skills). Permanece neste estado durante Dev → QA → TL → PO → RTE e até o ciclo de fechamento ser concluído.
- **`✅ Implementado`** — **não é acionado pelo fluxo autônomo.** A transição exige a execução do ciclo de fechamento descrito em `docs/process/refinement/epic_completion.md` (extração de conhecimento permanente + poda do ROADMAP) e é feita pelo dev após validar o resultado final.

Mesmo com código mergeado e validado, o épico permanece em `🏗️ Em andamento` até o dev aplicar `epic_completion.md`.

---

## REGRAS DE REPROVAÇÃO E LOOP

- Cada gate registra reprovações em `current_implementation.md`
- Após **3 reprovações consecutivas** no mesmo gate → aplicar regra de bloqueio de [blockers.md](../development/blockers.md) e devolver ao dev
- Reprovação de TL ou PO **nunca** é resolvida pulando o gate; sempre volta ao Dev (ou Scrum Master, conforme natureza)

---

**Ver também:**
- Como o dev dispara e valida → [delivery.md](delivery.md)
- Visão geral e quando usar → [overview.md](overview.md)
- Convenções operacionais (segredos, granularidade de commits) → [session_conventions.md](session_conventions.md)
- Guidelines de implementação reaproveitadas → `docs/process/implementation/`
