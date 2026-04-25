# Relatório de Entrega — Funcionalidade <X.Y> - <nome>

> **Template usado pela RTE Skill.** Copiar para o relatório final substituindo todos os placeholders. Output final **não pode** conter `<...>`.
>
> **Dívida W-PROTO-3:** este template ainda reflete o shape anterior à reforma de milestone (uma funcionalidade isolada). W-PROTO-5 acrescentou a Seção 🎯 Validação como bloco copy-paste pro body da PR. W-PROTO-3 reescreverá o template inteiro para shape de milestone (N épicos em sub-seções) e poderá consolidar a Seção 🎯 ali — por ora, o bloco abaixo é o ponto de verdade.

---

## Identificação

- **Funcionalidade:** X.Y - <nome conforme ROADMAP>
- **Roadmap:** <docs/ROADMAP.md | products/<produto>/ROADMAP.md>
- **Branch:** feature/X.Y-nome
- **Modo:** Autônomo
- **Dispatch recebido em:** YYYY-MM-DD
- **Entrega gerada em:** YYYY-MM-DD HH:MM

---

## Status dos Gates

| Gate | Status | Data | Observações |
|------|--------|------|-------------|
| Scrum Master | ✅ | YYYY-MM-DD | <ex: 1 esclarecimento devolvido ao dev e respondido> |
| Dev | ✅ | YYYY-MM-DD | <N commits, N tasks concluídas> |
| QA | ✅ | YYYY-MM-DD | <N testes rodados, 0 falhas> |
| TL | ✅ | YYYY-MM-DD | <aprovado / aprovado com observações> |
| PO | ✅ | YYYY-MM-DD | <N/N critérios cobertos> |
| RTE | ✅ | YYYY-MM-DD | (esta etapa) |

---

## Resumo Executivo

- **Implementou:** <descrição em 1-2 linhas do que foi entregue>
- **Arquivos modificados:** <N total> (<X> código, <Y> testes, <Z> docs)
- **Linhas alteradas:** +<add> / -<del>
- **Commits:** <N>
- **Testes:** <N novos> | <total rodado>
- **Custo aproximado dos gates (se aplicável):** <USD>

---

## Critérios de Aceite (do ROADMAP)

| # | Critério | Cobertura | Onde validar |
|---|---------|-----------|-------------|
| 1 | <critério literal> | ✅ Teste | tests/core/unit/<arquivo>:<linha> |
| 2 | <critério literal> | ✅ Manual | <comando ou rota> |
| 3 | <critério literal> | ✅ Teste + Manual | <ambos> |

---

## Notas Técnicas (do TL)

- <observação arquitetural relevante, se houve>
- <decisão técnica documentada e onde está documentada>
- <ponto de atenção para review humano>

(remover seção se não houve observações)

---

## Histórico de Reprovações Durante o Ciclo

(transcrever do `current_implementation.md`; vazio se ciclo limpo)

- <YYYY-MM-DD HH:MM> — <Gate> reprovou: <motivo>. Resolvido por: <ação>.

---

## Comandos de Validação Local (Copy-Paste)

```bash
# 1. Baixar branch
git fetch origin
git checkout feature/X.Y-nome
git pull origin feature/X.Y-nome

# 2. Preparar ambiente
source venv/bin/activate
pip install -r requirements.txt   # se deps mudaram

# 3. Rodar testes
pytest tests/core/unit/<caminho> -v
pytest -m integration             # se aplicável

# 4. Rodar aplicação (se mudou interface)
<comando específico do produto>
```

---

## Critérios Go/No-Go

**Aprovar merge quando TODOS os itens forem ✅:**

- [ ] Comandos de validação rodaram sem erro
- [ ] Critério 1 observado manualmente
- [ ] Critério 2 observado manualmente
- [ ] Critério 3 observado manualmente
- [ ] Comportamentos "não deve" do ROADMAP não ocorreram
- [ ] Sem warnings críticos no console
- [ ] Documentação estrutural atualizada (se aplicável)

**Caso algum item falhe:**
- ❌ Não mergeie.
- ❌ Devolva via Claude Code Web (nova rodada autônoma) OU traga para Cursor (fluxo manual) se exigir decisão arquitetural.

---

## Seção 🎯 Validação (copy-paste para o body da PR)

> **Bloco fixo introduzido por W-PROTO-5.** A RTE preenche os placeholders varrendo `current_implementation.md` (critérios PO ✅) e o ROADMAP (lista de épicos do milestone), copia para o body da PR criada via `mcp__github__create_pull_request` e referencia esse mesmo body na mensagem final ao dev.

```markdown
## 🎯 Validação (copie tudo abaixo e envie ao Copilot)

Você é revisor técnico desta PR. Valide o diff (`main...HEAD`) contra os
critérios abaixo. Para cada critério: ✅ (atende), ⚠️ (atende com
ressalva — justifique), ❌ (não atende — aponte arquivo/linha).
Reporte em markdown.

### Contexto
- Milestone: <ID> — <nome>
- Épicos entregues: <lista com IDs>
- Arquivo detalhado de validação: `<caminho>/validation-<id>.md`

### Critérios de aceite (consolidados do ROADMAP)

**Épico <ID-1>:**
1. <critério>
2. <critério>

**Épico <ID-2>:**
1. <critério>

### Comportamentos "não deve"
- <item>

### Formato de retorno esperado
- Tabela `Critério | Status | Observação`
- Seção "Riscos adicionais" (opcional)
```

---

## Próximo Passo

▶️ **RTE cria a PR via `mcp__github__create_pull_request`** com o body acima já preenchido (Seção 🎯 + checklist de gates + links). Dev revisa colando a Seção 🎯 no GitHub Copilot, aprova e mergeia pela interface — RTE **não mergeia**.
