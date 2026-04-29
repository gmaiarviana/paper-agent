# Relatório de Entrega — Milestone <ID> — <nome>

> **Template usado pela RTE Skill.** Copiar para o relatório final substituindo todos os placeholders. Output final **não pode** conter `<...>`.

---

## Identificação

- **Milestone:** <ID> — <nome conforme ROADMAP>
- **Roadmap:** <docs/process/workflow/ROADMAP.md | products/<produto>/ROADMAP.md>
- **Branch:** milestone/<id-em-caixa-baixa>
- **Épicos entregues:** <N> (<IDs separados por vírgula>)
- **Modo:** Autônomo
- **Dispatch recebido em:** YYYY-MM-DD
- **Entrega gerada em:** YYYY-MM-DD HH:MM

---

## Status dos Gates por Épico

### Épico <ID-1> — <nome>

| Funcionalidade | Dev | QA | TL | PO |
|----------------|-----|----|----|-----|
| N.1 — <nome> | ✅ | ✅ | ✅ | ✅ |
| N.2 — <nome> | ✅ | ✅ | ✅ | ✅ |

### Épico <ID-2> — <nome>

| Funcionalidade | Dev | QA | TL | PO |
|----------------|-----|----|----|-----|
| M.1 — <nome> | ✅ | ✅ | ✅ | ✅ |

---

## Resumo Executivo

- **Implementou:** <descrição em 1-2 linhas do que foi entregue no milestone>
- **Épicos entregues:** <N> (<IDs>)
- **Arquivos modificados:** <N total> (<X> código, <Y> testes, <Z> docs)
- **Linhas alteradas:** +<add> / -<del>
- **Commits:** <N>
- **Testes:** <N novos> | <total rodado>
- **Custo aproximado dos gates (se aplicável):** <USD>

**Por épico:**
- <ID-1>: <resumo em 1 linha do que foi entregue>
- <ID-2>: <resumo em 1 linha do que foi entregue>

---

## Critérios de Aceite (do ROADMAP)

### Épico <ID-1> — <nome>

| # | Critério | Cobertura | Onde validar |
|---|---------|-----------|-------------|
| 1 | <critério literal> | ✅ Teste | tests/core/unit/<arquivo>:<linha> |
| 2 | <critério literal> | ✅ Manual | <comando ou rota> |
| 3 | <critério literal> | ✅ Teste + Manual | <ambos> |

### Épico <ID-2> — <nome>

| # | Critério | Cobertura | Onde validar |
|---|---------|-----------|-------------|
| 1 | <critério literal> | ✅ Teste | tests/core/unit/<arquivo>:<linha> |

---

## Notas Técnicas (do TL)

### Épico <ID-1>

- <observação arquitetural relevante, se houve>
- <decisão técnica documentada e onde está documentada>
- <ponto de atenção para review humano>

(omitir épico sem observações)

---

## Histórico de Reprovações Durante o Ciclo

(transcrever do `current_implementation.md`; vazio se ciclo limpo)

- <YYYY-MM-DD HH:MM> — <Gate> reprovou (<épico ID> / func. N.M): <motivo>. Resolvido por: <ação>.

---

## Comandos de Validação Local (Copy-Paste)

```bash
# 1. Baixar branch
git fetch origin
git checkout milestone/<id-em-caixa-baixa>
git pull origin milestone/<id-em-caixa-baixa>

# 2. Preparar ambiente
source .venv/bin/activate
pip install -r requirements.txt   # se deps mudaram

# 3. Rodar testes
pytest tests/core/unit/<caminho> -v
pytest -m integration             # se aplicável

# 4. Rodar aplicação (se mudou interface)
<comando específico do produto>
```

---

## Critérios Go/No-Go

**Fluxo primário — revisão via Copilot na PR (W-PROTO-5):**
- [ ] Abrir a PR e copiar a Seção 🎯 Validação do body
- [ ] Enviar ao GitHub Copilot e colar a tabela de retorno como comentário na PR
- [ ] Nenhum ❌ sem justificativa no retorno do Copilot

**Fluxo opcional — validação local:**
- [ ] Comandos de validação rodaram sem erro
- [ ] Comportamentos "não deve" do ROADMAP não ocorreram
- [ ] Sem warnings críticos no console

**Aprovação final:**
- [ ] Documentação estrutural atualizada (se aplicável)
- Aprovar e mergear pela interface do GitHub quando os critérios acima forem ✅

**Caso algum critério falhe:**
- ❌ Não mergeie.
- ❌ Devolva via Claude Code Web (nova rodada autônoma) OU traga para Cursor (fluxo manual) se exigir decisão arquitetural.

---

## Seção 🎯 Validação (copy-paste para o body da PR)

> **Bloco fixo introduzido por W-PROTO-5.** A RTE preenche os placeholders varrendo `current_implementation.md` (critérios PO ✅) e o ROADMAP (lista de épicos do milestone), copia para o body da PR criada via `mcp__github__create_pull_request` e referencia esse mesmo body na mensagem final ao dev. O `current_validation.md` (rotativo) acompanha como detalhe opcional para o dev rodar localmente.

```markdown
## 🎯 Validação (copie tudo abaixo e envie ao Copilot)

Você é revisor técnico desta PR. Valide o diff (`main...HEAD`) contra os
critérios abaixo. Para cada critério: ✅ (atende), ⚠️ (atende com
ressalva — justifique), ❌ (não atende — aponte arquivo/linha).
Reporte em markdown.

### Contexto
- Milestone: <ID> — <nome>
- Épicos entregues: <lista com IDs>
- Arquivo detalhado de validação: `docs/process/current_validation.md` (rotativo)

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

▶️ **Dev revisa a PR** — colar a Seção 🎯 no GitHub Copilot, avaliar o retorno e mergear pela interface do GitHub se OK. RTE **não mergeia**.
