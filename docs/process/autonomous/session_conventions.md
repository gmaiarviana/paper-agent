# Convenções de Sessão Autônoma

> **📌 Localização:** `docs/process/autonomous/`
> **📌 Público:** Claude Code Web (executor autônomo) e dev (operador).
> **📌 Escopo:** Convenções operacionais aplicáveis a qualquer sessão autônoma. Complementa `overview.md` (o que é o modo) e `delivery.md` (como validar).

---

## 1. POLÍTICA DE SEGREDOS E `.env`

**Regra:** a sessão autônoma **não recebe segredos em tempo de implementação**. O `.env` é responsabilidade exclusiva do dev, carregado localmente durante a validação final.

### O que a sessão autônoma pode fazer

- ✅ Ler `.env.example` como referência das variáveis esperadas
- ✅ Escrever código que consome `os.getenv(...)` normalmente
- ✅ Criar unit tests com mocks do LLM (padrão `monkeypatch`/`unittest.mock`)
- ✅ Criar testes que validam **a string do prompt montado** (sem invocar LLM)
- ✅ Criar scripts de validação manual em `scripts/<produto>/flows/validate_*.py` — mas sem rodá-los contra API real

### O que a sessão autônoma NÃO faz

- ❌ Receber `ANTHROPIC_API_KEY` ou qualquer outro secret via prompt
- ❌ Criar `.env` real no repositório
- ❌ Invocar API da Anthropic durante a implementação (custo descontrolado + risco de loops de debug)
- ❌ Commitar qualquer arquivo que contenha secret mesmo que ofuscado

### Consequência

Erros que só aparecem com LLM real (qualidade da saída, aderência a instrução sutil do prompt) só emergem na validação final pelo dev. A compensação é cobrir **shape e contrato** com testes determinísticos:

- Prompt montado contém a seção esperada (ex: `## CONTEXTO DO PRODUTO`)?
- Função retorna dict com as chaves esperadas?
- Integração com o grafo passa o config correto?

Se a validação final do dev revelar bug, segue em follow-up (nova sessão autônoma ou fluxo manual).

---

## 2. GRANULARIDADE DE COMMITS

**Regra:** **um commit por épico** na branch da sessão autônoma. Nem mais, nem menos.

### Por quê um por épico

- **Épico = unidade de valor incremental** no ROADMAP. Cada épico entrega algo testável isoladamente.
- **Revertibilidade:** se o épico N+1 quebra algo, o N fica intacto no histórico.
- **Revisão:** dev revisa commits em ordem; 4 commits em uma POC grande é legível, 20 não é.

### Por que não mais granular

Commits por funcionalidade (1.1, 1.2, 1.3...) explodem o histórico e raramente ficam coerentes sozinhos — funcionalidades de um mesmo épico co-dependem (ex: `graph.py` sem `chat.py` não faz sentido).

### Por que não menos granular

Commit único da POC inteira apaga o limite entre épicos e impede rollback parcial. Mata o princípio "valor incremental" declarado no próprio ROADMAP.

### Formato da mensagem

Seguir padrão já usado no repo (`git log --oneline`):

```
<tipo>(<escopo>): resumo do épico em 1 linha

- funcionalidade X.Y: o que foi feito
- funcionalidade X.Z: o que foi feito
- ...

Épico <ID> do ROADMAP.
```

**Exemplo:**
```
feat(workflow/encerramento): fechar ciclo de encerramento autônomo (W-PROTO-5)

- 5.1: estado terminal "PR aberta" em skills/rte/skill.md
- 5.2: Seção 🎯 Validação adicionada ao body da PR
- 5.3: postura async documentada em docs/process/autonomous/workflow.md

Épico W-PROTO-5 do docs/process/workflow/ROADMAP.md.
```

### Atualização do ROADMAP

Mudar status do épico para `🏗️ Em andamento` no **início** da implementação e para `✅ Implementado` no commit final do épico. Pode entrar no mesmo commit do épico ou em um commit de docs separado — fica a critério da sessão, desde que o status esteja correto ao final.

---

## 3. CHECKLIST PRÉ-IMPLEMENTAÇÃO

Antes de começar a codar, a sessão confirma que tem:

- [ ] Épico(s) em `🔍 Detalhes definidos` no ROADMAP
- [ ] Templates de referência apontados nos "Detalhes de execução" de cada funcionalidade
- [ ] Dependências de core já implementadas (ou serão implementadas nesta sessão em ordem correta)
- [ ] Branch `milestone/<id-em-caixa-baixa>` criada e ativa
- [ ] Plano de validação (arquivo `<produto>/docs/poc_validation.md` ou equivalente) com esqueleto pronto

Se algum item falhar → reportar ao dev e **parar** antes de começar a implementação.

---

**Ver também:**
- Visão geral do modo autônomo → [overview.md](overview.md)
- Fluxo das skills → [workflow.md](workflow.md)
- Disparo e validação final → [delivery.md](delivery.md)
