# Validação Manual do Milestone <ID> — <nome>

> **📌 Público:** dev (revisor da PR final).
> **📌 Arquivo:** `docs/process/current_validation.md` — rotativo, sobrescrito a cada novo milestone (igual a `current_implementation.md`). Histórico fica nas PRs mergeadas.
> **📌 Quando usar:** ao receber notificação da sessão autônoma de "Milestone pronto", rodar este checklist antes de mergear.
> **📌 Estrutura:** um bloco por épico, com roteiro por funcionalidade. Cada roteiro tem **Critério**, **Gatilho**, **Resultado esperado** e **Sinal de falha** literais.
> **📌 Princípio anti-viés:** este arquivo valida critérios de aceite do ROADMAP, não a implementação. **Não há instruções de "abrir código", "checar diff" ou "inspecionar log de prompt"** — isso já foi feito pelo Copilot na PR e pelos gates QA/TL. Dev executa este arquivo sem precisar abrir nenhum `.py`.

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout milestone/<id-em-caixa-baixa>
git pull origin milestone/<id-em-caixa-baixa>

# 2. Ambiente
source venv/bin/activate              # Linux/Mac
# .\venv\Scripts\Activate.ps1         # Windows
pip install -r requirements.txt        # se deps mudaram no milestone

# 3. .env (uma única vez, fora desta sessão)
# Garantir que ANTHROPIC_API_KEY está preenchida em .env
```

**Pré-condição:** `ANTHROPIC_API_KEY` válida em `.env`. A sessão autônoma não toca nesse arquivo.

---

## Testes unitários (determinísticos)

```bash
pytest tests/<caminho-relevante> -v
pytest -m integration                  # se aplicável ao milestone
```

**Esperado:** todos passam. Se algum falha, parar e reportar — não seguir para validação manual.

---

## Épico <ID-EPICO-1> — <nome>

> Critérios em [<caminho do ROADMAP>](<link>), seção <ID-EPICO-1>.

### N.1 — <nome da funcionalidade>

**Critério de aceite:** <texto literal copiado do ROADMAP, sem parafrasear>

**Gatilho:**
1. <ação exata e copy-pasteável: comando, URL, clique em elemento nomeado>
2. (se chat) Cole exatamente este prompt:
   ```
   <texto literal do prompt, escrito pela RTE, com contexto fictício mas plausível>
   ```
3. <próxima ação literal>

**Resultado esperado:**
- <observação literal: texto/label/badge/seção que aparece na tela>
- <observação literal>

**Sinal de falha:**
- <o que se vê se quebrou: traceback, label ausente, badge errado, tela travada>

---

### N.2 — <nome da funcionalidade>

**Critério de aceite:** <texto literal>

**Gatilho:**
1. (continua a sessão de N.1) Clique no botão "<rótulo exato>" da seção "<nome exato>".

**Resultado esperado:**
- <texto literal que aparece na tela>

**Sinal de falha:**
- <o que indica quebra>

---

## Épico <ID-EPICO-2> — <nome>

### M.1 — <nome>

**Critério de aceite:** <texto literal>

**Gatilho:**
1. <ação literal>

**Resultado esperado:**
- <observação literal>

**Sinal de falha:**
- <quebra visível>

---

## Comportamentos "não deve" (regressão)

Validar de uma vez após executar os roteiros acima. Cada item do "não deve" do ROADMAP vira um roteiro com Gatilho/Resultado/Falha:

### Não deve: <comportamento que não pode ocorrer, copiado literal do ROADMAP>

**Gatilho:** <ação que dispararia o cenário ruim, ex.: "Pressione F5 na aba do navegador">

**Resultado esperado:**
- <comportamento que confirma a invariante, ex.: "Mensagens do chat somem; painel de seções zera; nenhum prompt 'restaurar sessão' aparece.">

**Sinal de falha:**
- <o oposto: ex.: "Aparece UI de 'continuar sessão anterior' ou mensagens persistem após F5.">

---

## Critérios de aprovação

Aprove o merge quando **todos**:

- [ ] Cada roteiro acima rodou e o **Resultado esperado** foi observado literalmente
- [ ] Nenhum **Sinal de falha** ocorreu em nenhum roteiro
- [ ] Comportamentos "não deve" do ROADMAP foram confirmados (não ocorreram)
- [ ] Tabela do Copilot na PR (Seção 🎯) sem ❌ sem justificativa

**Se algum critério falhar:** devolver com feedback para nova rodada autônoma (Claude Code Web) ou abrir sessão estratégica externa (Claude Web) se exigir decisão arquitetural.

---

**Ver também:**
- Skill da RTE → [skills/rte/skill.md](../skill.md)
- Validação geral do modo autônomo → [docs/process/autonomous/delivery.md](../../../docs/process/autonomous/delivery.md)
