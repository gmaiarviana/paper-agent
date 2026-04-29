# Copilot Instructions — Paper Agent

Guia para o Copilot (VS Code) quando o dev disser "valida essa branch".

Objetivo único: **sincronizar, resumir o que mudou, subir a app**. O dev observa
e decide. Nada além disso sem pedido explícito.

---

## Regras duras

- **Não rode testes** (nem unit, nem integration). QA Skill e CI já rodaram.
- **Não crie PR, não mergeie, não dê push.**
- **Não invente critério de aceite.** Extrai do `current_implementation.md` da branch.
- **Não pergunte qual épico, qual produto, qual modo.** A informação está no repo. Se faltar, **pare e reporte inconsistência** — não improvise.

---

## Pré-condição: branch saiu do fluxo autônomo

Toda branch validada por aqui tem `docs/process/current_implementation.md` (criado pela Scrum Master Skill, atualizado pelos gates, fechado pela RTE) e `docs/process/current_validation.md` (gerado pela RTE no commit de abertura da PR).

Se algum desses arquivos **não existir** na branch:

```
⛔ Branch inconsistente — current_implementation.md ou current_validation.md ausente.
RTE não fechou ou Scrum Master não rodou. Investigue antes de validar.
Não tente improvisar a partir do ROADMAP.
```

Pare. Não siga.

---

## Stacks por produto

A validação por aqui detecta o produto pelo diff e usa a stack correspondente.
Se a branch toca produto fora desta tabela, **pare e reporte** — não improvise.

| Produto | Caminho-gatilho        | Stack     | Entrypoint                                  | Portas      |
|---------|------------------------|-----------|---------------------------------------------|-------------|
| Revelar | products/revelar/app/  | Streamlit | products/revelar/app/chat.py (ou dashboard) | 8501-8503   |
| Ensaio  | products/ensaio/app/   | Reflex    | products/ensaio/ (reflex run a partir daí) | 3000, 8000  |

Se a branch mexe em mais de um produto, perguntar ao dev qual subir primeiro.
Se a branch só mexe em `core/` ou `docs/`, não há app para subir — pular §3.

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
source .venv/bin/activate              # Linux/Mac
# .\.venv\Scripts\Activate.ps1         # Windows
pip install -r requirements.txt
```

### 2. Montar o resumo "o que mudou + o que observar"

Abrir `docs/process/current_implementation.md` e extrair:
- Milestone e épicos entregues (cabeçalho + blocos `### Épico`)
- Arquivos modificados (seção "Resumo Final do Milestone")
- Critérios de aceite por épico (células PO ✅ nas tabelas de gates)

Abrir `docs/process/current_validation.md` e extrair:
- Roteiros por funcionalidade (Critério/Gatilho/Resultado/Falha) — esses são os pontos de observação literal pro dev.

Complementar com `git diff --stat origin/main` para listar áreas tocadas.

Filtrar os critérios em dois grupos:
- **Observável no uso da app** (ex: "ao clicar X aparece Y") → vai pro checklist do dev
- **"Não deve"** (ex: "não trava, não perde histórico") → vai pro checklist do dev

Critérios cobertos só por teste automatizado **não listar** — CI já cuida.

### 3. Subir a app afetada

Antes de qualquer coisa, libere as portas da stack detectada (ver §"Stacks
por produto" + §"Liberação de portas" abaixo). Não mate processos em geral —
mate apenas quem está escutando nas portas-alvo.

Detectar produto pelo diff (`git diff --name-only origin/main | grep products/`):
- `products/<produto>/app/**` → subir a stack do produto
- Se a branch mexeu em mais de um produto, perguntar ao dev qual subir primeiro
- Se a branch não mexeu em nenhum produto: avisar e pular esta etapa.

#### Liberação de portas

**Antes de qualquer coisa:** liberar as portas da stack detectada matando
apenas quem está escutando nelas.

Para Streamlit (Revelar): portas 8501-8503.
Para Reflex (Ensaio): portas 3000 (frontend) e 8000 (backend).

```powershell
# Windows (PowerShell) — cirúrgico por porta. Adapte $ports à stack detectada.
$ports = @(8501, 8502, 8503)         # Streamlit (Revelar)
# $ports = @(3000, 8000)             # Reflex (Ensaio)
foreach ($port in $ports) {
    Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}
```

```bash
# Linux/Mac — filtra pelo entrypoint do projeto
pkill -f "streamlit.*products/revelar/app/" 2>/dev/null || true   # Revelar
pkill -f "reflex.*products/ensaio" 2>/dev/null || true            # Ensaio
```

#### Subir

**Streamlit (Revelar):**

```bash
python -m streamlit run <entrypoint>     # ex: products/revelar/app/chat.py
```

**Reflex (Ensaio):**

```bash
cd products/ensaio
reflex run                               # backend :8000, frontend :3000
```

Subir em **foreground** e deixar rodando — o dev vai abrir no navegador.
Se o log mostrar traceback no start → parar, reportar o erro, não tentar consertar.

---

## Output fixo

```
Branch: <nome>  |  Milestone: <ID>

O que mudou
  • <bullet extraído do current_implementation.md>
  • ...

Pra você observar na app (do current_validation.md)
  [ ] <critério observável 1>
  [ ] <critério observável 2>
  [ ] <comportamento "não deve" 1>

App rodando em: http://localhost:<porta>  (ou: sem app afetada)

⚠️  <bloco opcional — só se algo travou o fluxo>
```

---

## Quando o dev disser "deu erro"

1. Coletar o log do terminal (últimas 50 linhas) antes de qualquer coisa. Não especular sobre UX sem traceback.
2. Identificar a causa raiz no traceback antes de propor mudança.
3. Erros típicos de ambiente (modelo descontinuado, venv errado, deps faltando) → orientar o dev a ajustar `.env` ou venv. **Não edite código.**

---

## Referências

- Fluxo autônomo: `docs/process/autonomous/workflow.md`
- Quem cria os `current_*.md`: Scrum Master (início) → gates atualizam → RTE finaliza
- ROADMAPs: `docs/ROADMAP.md` (core), `docs/process/workflow/ROADMAP.md`, `products/<produto>/ROADMAP.md`
