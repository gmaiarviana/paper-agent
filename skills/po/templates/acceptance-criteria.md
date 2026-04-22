# Aceite de Funcionalidade — <X.Y> - <nome>

> **Template usado pela PO Skill.** Preencher integralmente. Output final **não pode** conter `<...>`.

---

## Identificação

- **Funcionalidade:** X.Y - <nome literal do ROADMAP>
- **Roadmap:** <docs/ROADMAP.md | products/<produto>/ROADMAP.md>
- **Branch:** feature/X.Y-nome
- **Avaliado em:** YYYY-MM-DD HH:MM
- **Tentativa nº:** <N>

---

## Decisão

**[ APROVA | REJEITA ]**

Tipo de rejeição (se aplicável): `gap de implementação | gap de plano | gold plating`

---

## Mapeamento Crítério ↔ Implementação

| # | Tipo | Critério (literal do ROADMAP) | Cobertura | Status | Evidência |
|---|------|-------------------------------|-----------|--------|-----------|
| 1 | deve | <texto literal> | teste | ✅/❌ | tests/core/unit/<arquivo>:<linha> |
| 2 | deve | <texto literal> | manual | ✅/❌ | comando: `<...>` ou rota: `<...>` |
| 3 | não deve | <texto literal> | teste | ✅/❌ | tests/core/unit/<arquivo>:<linha> |
| 4 | deve | <texto literal> | script | ✅/❌ | scripts/core/<categoria>/validate_<x>.py |

**Resumo:** <N>/<N> critérios atendidos.

---

## Detecção de Gold Plating

Funcionalidades observáveis na entrega (rotas, comandos, comportamentos novos):
- <item 1> → ✅ corresponde ao critério #X
- <item 2> → ✅ corresponde ao critério #Y
- <item 3> → ⚠️ **sem critério correspondente** = gold plating

**Resultado:** <nenhum gold plating | <N> itens fora do escopo>

---

## Utilizabilidade

- [ ] Funcionalidade acessível pelo usuário final sem etapa escondida
- [ ] Setup necessário (envvars, migrations) documentado em README ou aplicado automaticamente
- [ ] Sem dependência de input não-validado

---

## Atualização do ROADMAP

- [ ] Funcionalidade marcada como concluída (✅) com resumo de 1-2 linhas
- [ ] Épico fechado (se for a última funcionalidade do épico)
- [ ] Texto reflete a entrega real (não promessas)

---

## Problemas (se REJEITA)

### 1. [TIPO: <CRITÉRIO NÃO ATENDIDO | GOLD PLATING | ROADMAP NÃO ATUALIZADO>]
- **Critério/Item:** <texto>
- **Detalhe:** <o que falta ou o que sobra>
- **Roteamento:** <Dev | Scrum Master>

### 2. ...

(remover seção se APROVA)

---

## Próximo Passo

- **Aprovado:** seguir para RTE Skill.
- **Rejeitado (gap de implementação):** devolver ao Dev. Incrementar contador.
- **Rejeitado (gap de plano):** devolver ao Scrum Master. Incrementar contador.
- **Rejeitado (gold plating):** devolver ao Dev para remover excesso. Incrementar contador.
- Após 3 rejeições consecutivas, acionar `docs/process/implementation/blockers.md`.
