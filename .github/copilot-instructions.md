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
— o dev precisa te dizer qual funcionalidade/épico (ex: "POC-ENSAIO").
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
- Milestone e épicos entregues (cabeçalho + blocos `### Épico`)
- Arquivos modificados (seção "Resumo Final do Milestone")
- Critérios de aceite por épico (células PO ✅ nas tabelas de gates)

**Modo B:** localizar o épico/funcionalidade no ROADMAP correto e extrair:
- Título + objetivo
- Bloco "Critérios de Aceite" da(s) funcionalidade(s) implementada(s)

Complementar com `git diff --stat origin/main` pra listar áreas tocadas.

Em ambos os modos, filtrar os critérios em dois grupos:
- **Observável no uso da app** (ex: "ao clicar X aparece Y") → vai pro checklist do dev
- **Não deve** (ex: "não trava, não perde histórico") → vai pro checklist do dev

Critérios cobertos só por teste automatizado **não listar** — CI já cuida.

### 3. Subir a app afetada

**Antes de qualquer coisa:** liberar as portas 8501–8503 matando apenas quem está escutando nelas (não mate python/streamlit em geral — pode ser Jupyter, outro projeto, outra branch):

```powershell
# Windows (PowerShell) — cirúrgico por porta
foreach ($port in 8501..8503) {
    Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}
```

```bash
# Linux/Mac — filtra pelo chat.py do projeto
pkill -f "streamlit.*products/.*/app/chat.py" 2>/dev/null || true
```

Detectar produto pelo diff (`git diff --name-only origin/main | grep products/`):
- `products/revelar/app/**` → `streamlit run products/revelar/app/chat.py`
- `products/ensaio/app/**` → `streamlit run products/ensaio/app/chat.py`
- Outro produto → procurar `products/<nome>/app/chat.py`; se não existir, perguntar ao dev

Comando padrão:
```bash
python -m streamlit run <path> --server.headless true --server.port 8501
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

## Operação Windows / macOS / Linux

Regras que evitam retrabalho quando a validação roda fora de Linux:

- **.venv:** o projeto usa `.venv/` (com ponto) como diretório de ambiente virtual. Ativar com:
  - Linux/Mac: `source .venv/bin/activate`
  - Windows: `.\.venv\Scripts\Activate.ps1`
  
  Se `venv/` (sem ponto) existir, é obsoleto — use `.venv` de preferência.
  
- **Streamlit:** prefira `python -m streamlit run <path>` em vez de
  `streamlit run <path>`. O primeiro garante que está usando o binário do
  venv ativo (especialmente no Windows, onde `streamlit.exe` pode estar
  no PATH errado). Se a porta 8501 estiver ocupada, **não troque
  silenciosamente** — avise o dev e pergunte qual porta usar.
- **Foreground:** sempre em foreground, sem `--server.headless true` salvo
  pedido explícito do dev. Se o log no start mostrar traceback, **pare e
  reporte o traceback**. Não tente consertar.

---

## Quando o dev disser "deu erro" ou "travou"

1. Primeiro passo **obrigatório:** coletar o log do terminal do Streamlit
   (últimas 50 linhas). Não especular sobre UX sem traceback.
2. Identificar a causa raiz no traceback antes de propor qualquer
   mudança de código.
3. Erros típicos e orientação:
   - `404 Not Found` ou `model_not_found` no cliente Anthropic: o modelo
     configurado foi descontinuado. Oriente o dev a trocar `LLM_MODEL` no
     `.env` e reiniciar o Streamlit. Não edite código.
   - `CircuitBreakerOpenError`: erros consecutivos abriram o circuit
     breaker. Reiniciar o processo zera o breaker — peça ao dev.
   - `ModuleNotFoundError: streamlit`: venv errado ou não ativado. Rode
     `python -m pip install -r requirements.txt` no venv que está usando.
   - `ValueError: Model 'X' not supported` vindo do cost tracker: bug já
     corrigido (hoje o tracker só loga warning e retorna 0). Se aparecer,
     é sinal de branch desatualizada — oriente rebase.

---

## Checklist mínimo de POC do Ensaio (Modo B, épico POC-ENSAIO)

Quando subir o Ensaio para validação manual:

- [ ] App abre sem traceback (chat à esquerda, painel à direita).
- [ ] Enviar uma mensagem curta no chat → sistema responde (Orquestrador).
- [ ] Colar um bloco de código em fences markdown → formatação preservada no histórico.
- [ ] Clicar "Gerar artigo" → markdown aparece no painel direito.
- [ ] Pedir refinamento ("deixa mais conciso") e clicar "Regenerar" → artigo muda.
- [ ] Recarregar a página (F5) → tudo zera, nenhuma tentativa de restaurar sessão.
- [ ] **Não deve ocorrer:** mensagem do usuário sumir do histórico em caso de erro
      de backend — hoje o erro vira bubble do assistente e a mensagem permanece.

Se algo do checklist falhar, reportar o traceback/observação e parar — não editar.

---

## Referências

- Fluxo autônomo: `docs/process/autonomous/workflow.md`
- Quem cria `current_implementation.md`: Scrum Master Skill (início) →
  atualizada por cada gate → finalizada pela RTE Skill
- ROADMAPs: `docs/ROADMAP.md` (core) e `products/<produto>/ROADMAP.md`
- POC-ENSAIO: `products/ensaio/docs/poc_validation.md`
