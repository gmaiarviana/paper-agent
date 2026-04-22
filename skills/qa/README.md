# QA Skill

> **📌 Localização:** `skills/qa/`
> **📌 Etapa do fluxo:** terceira (após Dev) — `docs/process/autonomous/workflow.md` §3
> **📌 Pré-requisito:** Dev concluiu todas as tasks do plano.

---

## 1. PAPEL

A QA Skill é o **primeiro gate técnico** após implementação. Decide **binariamente** se a entrega tem qualidade técnica suficiente para seguir para TL.

**Princípio:** falha de teste = rejeição automática. Sem tolerância. Sem "pequenos deslizes". Sem decisão humana no meio.

---

## 2. CRITÉRIOS DE APROVAÇÃO

Aprova **APENAS** quando **TODOS** os itens forem verdadeiros:

- ✅ Suite completa passa (`pytest tests/unit/`) — 0 falhas, 0 erros
- ✅ Integration tests aplicáveis passam (`pytest -m integration`)
- ✅ Sintaxe Python OK em todos os arquivos modificados (parser sem erro)
- ✅ Imports resolvem (sem `ImportError`, sem ciclo)
- ✅ Markers `integration` / `slow` aplicados onde corresponde (`docs/testing/strategy.md`)
- ✅ Testes novos foram criados para lógica nova (TDD pragmático: lógica crítica obrigatória)
- ✅ Nenhum teste foi pulado (`@pytest.mark.skip`) sem justificativa documentada
- ✅ Nenhum warning crítico no console durante execução

---

## 3. CRITÉRIOS DE REJEIÇÃO

Rejeita **automaticamente** se **qualquer** item ocorrer:

- ❌ ≥1 teste falhando ou com erro
- ❌ Erro de sintaxe em arquivo modificado
- ❌ Import quebrado (cobertura: testes + arquivos impactados)
- ❌ Lógica nova sem teste correspondente
- ❌ Teste pulado/comentado sem justificativa
- ❌ Cobertura caiu em arquivo crítico modificado
- ❌ Warning crítico (DeprecationWarning relevante, RuntimeError silencioso, etc)

---

## 4. INPUT ESPERADO

- Branch `feature/X.Y-nome` com commits da implementação
- `docs/process/current_implementation.md` com Dev marcado ✅
- Acesso ao ambiente para rodar `pytest`

---

## 5. OUTPUT PRODUZIDO

- ✅ Relatório no formato [templates/qa-report.md](templates/qa-report.md)
- ✅ Atualização em `current_implementation.md`:
  - Aprovou: marca `QA ✅ <data>` + sumário
  - Rejeitou: registra `QA ❌ <data>` + lista específica + incrementa contador de reprovações
- ✅ Decisão clara: **APROVA** ou **REJEITA** (nunca "aprovado com observações")

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Próxima ação |
|---------|--------------|
| Aprovou | Fluxo segue para **TL Skill** |
| Rejeitou | Fluxo volta para **Dev** com lista de problemas |
| 3 rejeições consecutivas | Aplicar `docs/process/implementation/blockers.md` e devolver ao dev humano |

QA **não** corrige código. Devolve com diagnóstico.

---

## 7. DIFERENÇAS DA VALIDATION SKILL

QA **roda testes** para decidir aprovação/rejeição.
Validation **não roda testes** — só prepara entrega humana.

São complementares: QA garante que o código funciona; Validation entrega a confirmação ao dev.

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Template do relatório → [templates/qa-report.md](templates/qa-report.md)
- Estratégia de testes → `docs/testing/strategy.md`
- Próximo gate → `skills/tl/README.md`
