# Validação Manual da POC do Ensaio

> ⚠️ **Documento histórico.** Esta validação foi escrita sobre a stack
> Streamlit anterior (entrypoint `chat.py`). A stack atual é Reflex —
> ver `docs/adr/001-stack-do-prototipo.md`. Mantido como registro do
> processo de POC; instruções de execução não refletem o produto atual.

> **📌 Público:** dev (revisor da PR final).
> **📌 Quando usar:** ao receber notificação da sessão autônoma de "POC pronta", rodar este checklist antes de mergear.
> **📌 Estrutura:** um bloco por épico da POC (C-ENSAIO-2, E-POC-1, E-POC-2, E-POC-3), com "o que rodar" e "o que observar" por funcionalidade.

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout claude/implement-testing-poc-N7ecQ
git pull origin claude/implement-testing-poc-N7ecQ

# 2. Ambiente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Editar .env e adicionar ANTHROPIC_API_KEY
```

**Pré-condição:** `ANTHROPIC_API_KEY` válida em `.env`. A sessão autônoma não toca nesse arquivo — ele é responsabilidade exclusiva do dev (ver [docs/process/autonomous/session_conventions.md](../../../docs/process/autonomous/session_conventions.md)).

---

## Testes unitários (determinísticos)

Rodar antes da validação manual com API:

```bash
pytest tests/core/unit/test_writer.py -v
pytest tests/products/ensaio/unit/test_product_config.py -v
pytest tests/ -v --ignore=tests/integration
```

**O que observar:** todos os testes passam. Se algum falhar, parar e reportar — não seguir para validação com API.

---

## Épico C-ENSAIO-2: Writer (versão inicial)

> Critérios de aceite completos em [docs/ROADMAP.md](../../../docs/ROADMAP.md), seção C-ENSAIO-2.

### 2.1 — `writer_node` isolado

**O que rodar:**
```bash
python scripts/core/flows/validate_writer.py
```
*(script de validação manual — nome e path definitivos preenchidos durante a implementação)*

**O que observar:**
- Script invoca `writer_node` com input mínimo (apenas `messages` com 1 mensagem fictícia) e imprime o markdown retornado
- Output tem seções IMRaD (Introdução, Métodos, Resultados, Discussão, Conclusão, Referências)
- Nenhum erro de import ou chave de dict ausente

### 2.2 — Prompt IMRaD + defaults

**O que rodar:** mesmo script de 2.1, agora com `focal_argument=None` e `messages=[]`.

**O que observar:**
- Writer ainda produz artigo (não falha por falta de contexto)
- Seções IMRaD aparecem com conteúdo placeholder coerente
- Nenhum nome de produto (Ensaio, Revelar) aparece no output (prompt não deve vazar)

### 2.3 — YAML carregável

**O que rodar:**
```bash
python -c "from core.agents.memory.config_loader import load_agent_config; print(load_agent_config('writer'))"
```

**O que observar:**
- Retorna dict com chaves `prompt`, `model`, `context_limits`, `metadata`
- Modelo é `claude-3-5-haiku-20241022`
- Nenhuma exceção de schema validator

### 2.4 — Loop externo de refinamento

**O que rodar:**
```bash
python scripts/core/flows/validate_writer.py --refinement
```

**O que observar:**
- Script invoca `writer_node` duas vezes: primeira com `previous_article=None`, segunda com artigo anterior + nova mensagem "deixa mais conciso"
- Segundo artigo é visivelmente mais curto que o primeiro
- Writer regenerou artigo inteiro (não fez edit pontual)

---

## Épico E-POC-1: App Streamlit mínimo

> Critérios em [products/ensaio/ROADMAP.md](../ROADMAP.md), seção E-POC-1.

### 1.1 — Estrutura de pastas

**O que rodar:**
```bash
ls products/ensaio/app/ products/ensaio/app/components/ products/ensaio/config/
```

**O que observar:**
- `products/ensaio/app/__init__.py` existe
- `products/ensaio/app/components/__init__.py` existe
- `products/ensaio/config/` existe como diretório
- Nenhuma sobreposição com `products/revelar/app/`

### 1.2 — Entrypoint Streamlit

**O que rodar:**
```bash
streamlit run products/ensaio/app/chat.py
```

**O que observar:**
- App abre em `http://localhost:8501` sem erro
- Layout 60/40 (chat à esquerda, painel do artigo à direita)
- Nenhum erro no console ao carregar
- Nenhum prompt por variável além de `ANTHROPIC_API_KEY`

### 1.3 — Grafo LangGraph do Ensaio

**O que rodar:**
```bash
python scripts/ensaio/flows/validate_graph.py
```

**O que observar:**
- Script invoca o grafo com input fixo e imprime o output
- Grafo compõe apenas `orchestrator_node` + `structurer_node` (confirmar por inspeção do log)
- Writer **não** é executado automaticamente
- `SqliteSaver` criou `data/ensaio_checkpoints.db`

### 1.4 — Reuso de componentes do Revelar

**O que rodar:** observar no código.

**O que observar:**
- `products/ensaio/app/chat.py` importa `chat_history` de `products/revelar/app/components/`
- `products/ensaio/app/components/chat_input.py` é versão própria (não importa `EventBus`)
- Nenhuma duplicação de código de `chat_history`

### 1.5 — Painel do artigo e botão

**O que rodar:** mesma sessão do 1.2 (Streamlit aberto).

**O que observar:**
- Botão "Gerar artigo" visível desde o primeiro load (antes de qualquer mensagem)
- Antes de gerar: coluna direita vazia (ou com placeholder discreto)
- Depois de gerar (se conseguir testar com API): botão vira "Regenerar"

### 1.6 — Estado em sessão

**O que rodar:** na sessão do Streamlit, enviar mensagens, recarregar a página (F5).

**O que observar:**
- Mensagens somem após F5 (comportamento desejado)
- Artigo some após F5
- Nenhum arquivo novo em disco além de `data/ensaio_checkpoints.db` (aceito)

---

## Épico E-POC-2: Injeção de contexto de produto

> Critérios em [products/ensaio/ROADMAP.md](../ROADMAP.md), seção E-POC-2.

### 2.1 — YAML de configuração

**O que rodar:**
```bash
cat products/ensaio/config/product.yaml
```

**O que observar:**
- Campo `focus` presente como única chave obrigatória
- Descrição em prosa livre sobre o produto Ensaio
- Nenhum termo técnico interno do super-sistema (nomes de classe, schemas)

### 2.2 — Loader no produto

**O que rodar:**
```bash
pytest tests/products/ensaio/unit/test_product_config.py -v
```

**O que observar:**
- Teste cobre: YAML válido, ausente, malformado
- `load_product_context()` retorna string
- `grep -r "from core" products/ensaio/app/product_config.py` retorna vazio (sem import de core)

### 2.3 — Parâmetro opcional nos agentes do core

**O que rodar:** iniciar o Revelar normalmente:
```bash
streamlit run products/revelar/app/chat.py
```

**O que observar:**
- Revelar funciona igual ao antes (backward compat mantido)
- Inspecionar `core/prompts/orchestrator.py` e `core/prompts/structurer.py`: placeholder `{product_context}` em seção opcional `## CONTEXTO DO PRODUTO`
- Quando `product_context` ausente, seção some do prompt montado

### 2.4 — Injeção no fluxo do Ensaio

**O que rodar:** iniciar o Ensaio com log habilitado e enviar uma mensagem. Procurar nos logs o prompt montado do Orquestrador.

**O que observar:**
- Prompt montado contém `## CONTEXTO DO PRODUTO` com a string do `product.yaml`
- Orquestrador e Estruturador ambos recebem o contexto (não só o Writer)

---

## Épico E-POC-3: Fluxo conversacional

> Critérios em [products/ensaio/ROADMAP.md](../ROADMAP.md), seção E-POC-3.

### 3.1 — Entrada livre no chat

**O que rodar:** no Streamlit, colar bloco de código markdown no chat:
```
Aqui está meu experimento:
```python
def hello():
    print("hi")
```
```

**O que observar:**
- Sistema aceita sem parsing especial
- Bloco renderiza com code fence preservado no histórico
- Nenhum campo obrigatório adicional apareceu

### 3.2 — Conversa com Orquestrador + Estruturador

**O que rodar:** no Streamlit, conversar sobre um experimento fictício por 3-4 mensagens.

**O que observar:**
- Orquestrador e Estruturador reagem em postura ativo-leve (perguntam apenas quando algo está vago)
- Metodologista **não** é invocado
- Ajuste de comportamento vem só da injeção de contexto (não de código novo nos agentes — confirmar em `git diff` que `core/agents/orchestrator/nodes.py` só mudou na assinatura, não na lógica)

### 3.3 — Geração sob demanda

**O que rodar:** no Streamlit, clicar "Gerar artigo" logo na primeira mensagem.

**O que observar:**
- Sistema aceita sem bloquear (geração prematura permitida)
- Writer retorna artigo em uma passada (sem streaming, sem por-seção)
- Markdown aparece no painel direito
- Nenhum erro se `focal_argument` vier vazio

### 3.4 — Refinamento minimalista

**O que rodar:** após gerar um artigo, no chat escrever "deixa mais conciso", clicar "Regenerar".

**O que observar:**
- Writer é reinvocado com `previous_article` preenchido
- Artigo novo substitui o anterior (versão antiga some)
- Nenhuma UI de versionamento aparece

### 3.5 — Sessão descartável

**O que rodar:** F5 na página.

**O que observar:**
- Tudo zera (mensagens, artigo, focal_argument)
- Nenhuma UI de "restaurar" aparece
- `data/ensaio_checkpoints.db` pode crescer — aceitável na POC (apagar manualmente quando quiser zerar)

---

## Critérios de aprovação

Aprove o merge quando:

- [ ] Todos os unit tests passam
- [ ] Os 4 blocos acima (C-ENSAIO-2, E-POC-1, E-POC-2, E-POC-3) rodam sem erro
- [ ] Comportamentos "não deve" do ROADMAP **não** ocorrem (ex: Writer por seção, Metodologista invocado, persistência em disco)
- [ ] ROADMAPs (core + ensaio) marcam os 4 épicos como `✅ Implementado`

**Se algum critério falhar:** devolver com feedback para nova rodada autônoma, ou trazer para fluxo manual se exigir decisão arquitetural.

---

**Ver também:**
- Convenções da sessão autônoma → [docs/process/autonomous/session_conventions.md](../../../docs/process/autonomous/session_conventions.md)
- Validação geral do modo autônomo → [docs/process/autonomous/delivery.md](../../../docs/process/autonomous/delivery.md)
- ROADMAPs → [docs/ROADMAP.md](../../../docs/ROADMAP.md), [products/ensaio/ROADMAP.md](../ROADMAP.md)
