# Workflow Autônomo: Planning → Dev → QA → TL → PO → Validation

> **📌 Localização:** `docs/process/autonomous/`
> **📌 Público:** Claude Code Web operando em modo autônomo.
> **📌 Princípio:** cada skill é um gate. Reprovou → volta para a etapa anterior antes de avançar.

---

## FLUXO GERAL

```
Dispatch → Planning Skill → Dev → QA Skill → TL Skill → PO Skill → Validation Skill → Dev valida
                ↑              ↑       ↑         ↑          ↑
                └──── reprovou? volta para a etapa anterior ────┘
```

---

## 1. PLANNING SKILL

**Objetivo:** transformar funcionalidade do ROADMAP em plano de implementação executável.

**Deve:**
- ✅ Ler ROADMAP (core ou produto) e localizar funcionalidade X.Y
- ✅ Ler ARCHITECTURE.md e docs técnicas relevantes (via `docs/CONTEXT_INDEX.md`)
- ✅ Quebrar a funcionalidade em tarefas ordenadas por dependência
- ✅ Identificar dúvidas técnicas e **resolvê-las consultando docs antes de assumir**
- ✅ Documentar plano em `docs/process/current_implementation.md` (mesmo arquivo do fluxo manual)
- ✅ Listar arquivos esperados (criados/modificados) e padrões a seguir

**Não deve:**
- ❌ Tomar decisões arquiteturais novas (se necessário, abortar e devolver ao dev)
- ❌ Refinar épico (refinamento é manual, via Claude Web)
- ❌ Avançar para Dev se funcionalidade não estiver em épico refinado

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

**Objetivo:** validar arquitetura, padrões e aderência ao ROADMAP técnico.

**Deve verificar:**
- ✅ Implementação alinhada com `ARCHITECTURE.md`
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

**Objetivo:** validar critérios de aceite da funcionalidade.

**Deve verificar:**
- ✅ Cada critério de aceite do ROADMAP está atendido (mapear 1-a-1)
- ✅ Comportamentos "deve / não deve" cobertos por teste OU script de validação
- ✅ Funcionalidade entrega valor incremental (mesmo isolada)
- ✅ ROADMAP marcado como concluído quando aplicável

**Reprova quando:**
- ❌ Algum critério de aceite não está coberto/observável
- ❌ Comportamento "não deve" não foi validado

**Ação ao reprovar:** retornar ao Planning ou Dev (dependendo se é gap de plano ou de implementação).

**Saída:** checklist de aceite com status por critério.

---

## 6. VALIDATION SKILL

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

## REGRAS DE REPROVAÇÃO E LOOP

- Cada gate registra reprovações em `current_implementation.md`
- Após **3 reprovações consecutivas** no mesmo gate → aplicar regra de bloqueio de [blockers.md](../development/blockers.md) e devolver ao dev
- Reprovação de TL ou PO **nunca** é resolvida pulando o gate; sempre volta ao Dev (ou Planning, conforme natureza)

---

**Ver também:**
- Como o dev dispara e valida → [delivery.md](delivery.md)
- Visão geral e quando usar → [overview.md](overview.md)
- Guidelines de implementação reaproveitadas → `docs/process/implementation/`
