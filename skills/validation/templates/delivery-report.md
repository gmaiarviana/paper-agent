# Relatório de Entrega — Funcionalidade <X.Y> - <nome>

> **Template usado pela Validation Skill.** Copiar para o relatório final substituindo todos os placeholders. Output final **não pode** conter `<...>`.

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
| Planning | ✅ | YYYY-MM-DD | <ex: 1 esclarecimento devolvido ao dev e respondido> |
| Dev | ✅ | YYYY-MM-DD | <N commits, N tasks concluídas> |
| QA | ✅ | YYYY-MM-DD | <N testes rodados, 0 falhas> |
| TL | ✅ | YYYY-MM-DD | <aprovado / aprovado com observações> |
| PO | ✅ | YYYY-MM-DD | <N/N critérios cobertos> |
| Validation | ✅ | YYYY-MM-DD | (esta etapa) |

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
| 1 | <critério literal> | ✅ Teste | tests/unit/<arquivo>:<linha> |
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
pytest tests/unit/<caminho> -v
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

## Próximo Passo

▶️ **Dev cria o PR pela interface do GitHub.** Template é aplicado automaticamente. Validation **não cria PR** e **não mergeia** — sempre exige aprovação humana.
