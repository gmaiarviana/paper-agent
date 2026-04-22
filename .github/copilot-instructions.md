# Copilot Instructions — Paper Agent

Guia para o Copilot (VS Code) quando o dev disser "valida essa branch".

Objetivo único: **sincronizar, resumir o que mudou, subir a app**. O dev observa
e decide. Nada além disso sem pedido explícito.

---

## Regras duras

- **Não rode testes** (nem unit, nem integration). QA Skill e CI já rodaram.
- **Não crie PR, não mergeie, não dê push.**
- **Não invente critério de aceite.** Extrai do doc ou do ROADMAP; se não achar, pergunta.
- Se faltar informação pra algum passo → **pare e pergunte**. Não tente suprir.

---

## Dois modos de validação

### Modo A — Branch saiu do fluxo autônomo
Sinal: `docs/process/current_implementation.md` existe na branch.
Fonte de verdade: esse arquivo (tem gates, diff, critérios, comandos).

### Modo B — Validação avulsa (manual / sem fluxo autônomo)
Sinal: `current_implementation.md` NÃO existe.
Fonte de verdade: ROADMAP (`docs/ROADMAP.md` ou `products/<produto>/ROADMAP.md`)
— o dev precisa te dizer qual funcionalidade/épico (ex: "C-ENSAIO-2").
Se o dev não disser, **pergunte** antes de continuar.

---

## Fluxo (3 passos)

### 1. Sincronizar
```bash
git fetch origin
git checkout <branch>
git pull origin <branch>
```
Se `requirements.txt` ou `requirements-test.txt` mudaram vs `origin/main`:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Montar o resumo "o que mudou + o que observar"

**Modo A:** abrir `docs/process/current_implementation.md` e extrair:
- Funcionalidade/épico (cabeçalho)
- Arquivos modificados (seção "Resumo Final" da Validation Skill)
- Critérios de aceite declarados pelo PO

**Modo B:** localizar o épico/funcionalidade no ROADMAP correto e extrair:
- Título + objetivo
- Bloco "Critérios de Aceite" da(s) funcionalidade(s) implementada(s)

Complementar com `git diff --stat origin/main` pra listar áreas tocadas.

Em ambos os modos, filtrar os critérios em dois grupos:
- **Observável no uso da app** (ex: "ao clicar X aparece Y") → vai pro checklist do dev
- **Não deve** (ex: "não trava, não perde histórico") → vai pro checklist do dev

Critérios cobertos só por teste automatizado **não listar** — CI já cuida.

### 3. Subir a app afetada
Detectar produto pelo diff (`git diff --name-only origin/main | grep products/`):
- `products/revelar/app/**` → `streamlit run products/revelar/app/chat.py`
- `products/ensaio/app/**` → `streamlit run products/ensaio/app/chat.py`
- Outro produto → procurar `products/<nome>/app/chat.py`; se não existir, perguntar ao dev

Comando padrão:
```bash
streamlit run <path> --server.headless true --server.port <porta>
```
Subir em **foreground** e deixar rodando — o dev vai abrir no navegador.
Se o log mostrar traceback no start → parar, reportar o erro, não tentar consertar.

Se a branch mexeu em mais de um produto, perguntar ao dev qual subir primeiro.

Se a branch não mexeu em nenhum produto (só `core/` ou `docs/`):
avisar o dev que não há app pra subir e pular esta etapa.

---

## Output fixo

```
Branch: <nome>  |  Modo: <A (autônomo) | B (avulso - <épico>)>

O que mudou
  • <bullet extraído do current_implementation.md ou resumo do diff>
  • ...

Pra você observar na app (do ROADMAP / PO)
  [ ] <critério observável 1>
  [ ] <critério observável 2>
  [ ] <comportamento "não deve" 1>

App rodando em: http://localhost:<porta>  (ou: sem app afetada)

⚠️  <bloco opcional — só se algo travou o fluxo>
```

---

## Referências

- Fluxo autônomo: `docs/process/autonomous/workflow.md`
- Quem cria `current_implementation.md`: Planning Skill (início) →
  atualizada por cada gate → finalizada pela Validation Skill
- ROADMAPs: `docs/ROADMAP.md` (core) e `products/<produto>/ROADMAP.md`
