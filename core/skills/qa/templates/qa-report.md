# Relatório QA — Funcionalidade <X.Y>

> **Template usado pela QA Skill.** Preencher integralmente. Output final **não pode** conter `<...>`.

---

## Identificação

- **Funcionalidade:** X.Y - <nome>
- **Branch:** feature/X.Y-nome
- **Executado em:** YYYY-MM-DD HH:MM
- **Tentativa nº:** <N> (esta funcionalidade já passou por QA <N-1> vezes)

---

## Decisão

**[ APROVA | REJEITA | BLOQUEADO POR AMBIENTE ]**

---

## Inventário do Diff

- Arquivos modificados: <N>
  - Código (`*.py` fora de `tests/`): <N>
  - Testes (`tests/`): <N>
  - Docs (`*.md`): <N>
- Linhas: +<add> / -<del>

---

## Verificações

| Verificação | Status | Detalhe |
|-------------|--------|---------|
| Sintaxe Python | ✅/❌ | <N arquivos compilados sem erro> |
| Imports | ✅/❌ | <N arquivos OK; impactados verificados> |
| Cobertura de lógica nova | ✅/❌ | <funções novas têm teste? listar> |
| Suite unit | ✅/❌ | passed=<N> failed=<N> error=<N> skipped=<N> |
| Suite integration | ✅/❌ | passed=<N> failed=<N> error=<N> skipped=<N> |
| Markers (`integration`/`slow`) | ✅/❌ | <observação> |
| Skips justificados | ✅/❌ | <listar skips e justificativa> |
| Warnings críticos | ✅/❌ | <0 ou listar> |

---

## Problemas Encontrados (se REJEITA)

### 1. [TIPO] Localização
```
<saída literal do erro / stack trace relevante>
```
**Ação esperada do Dev:** <o que precisa mudar>

### 2. [TIPO] Localização
...

(remover seção se APROVA)

---

## Resumo Executivo

- **Tempo total da execução:** <Xs>
- **Comandos rodados:**
  ```bash
  pytest tests/unit/ -v
  pytest -m integration -v   # se aplicável
  ```
- **Saída completa:** anexada em commit/log do gate (não embutir no relatório)

---

## Próximo Passo

- **Aprovado:** seguir para TL Skill.
- **Rejeitado:** devolver ao Dev com lista acima. Incrementar contador de rejeições em `current_implementation.md`. Após 3ª rejeição consecutiva, acionar `docs/process/implementation/blockers.md`.
- **Bloqueado por ambiente:** devolver ao dev humano com comandos sugeridos. **Não conta** como rejeição.
