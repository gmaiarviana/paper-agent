# Validação Local — PROTO-ENSAIO-2

> **📌 Público:** dev (revisor da PR final).
> **📌 Arquivo rotativo:** sobrescrito a cada novo milestone. Histórico fica nas PRs mergeadas.
> **📌 Quando usar:** opcional, depois que o Copilot rodou na Seção 🎯 do body. A Seção 🎯 da PR é a porta principal de revisão; este arquivo é checagem manual extra antes do merge.
> **📌 Princípio anti-viés:** os roteiros abaixo só validam comportamento observável extraído dos critérios de aceite **PO ✅** do ROADMAP. Não pedem para abrir código-fonte, rodar `git diff` ou inspecionar logs.

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout claude/implement-product-essay-dHnbU
git pull origin claude/implement-product-essay-dHnbU

# 2. Ambiente
source .venv/bin/activate              # Linux/Mac
# .\.venv\Scripts\Activate.ps1         # Windows
pip install -r requirements.txt
pip install -r products/ensaio/requirements.txt

# 3. .env
# Garantir que ANTHROPIC_API_KEY (ou LITELLM_API_KEY) está preenchida em .env
```

---

## Testes unitários (determinísticos)

```bash
pytest tests/core/unit/agents/ tests/products/ensaio/ -v
```

**Esperado:** 249 passed, 2 skipped. Se algum falha, parar e reportar — não seguir para validação manual.

Subset focado nas funcionalidades novas do milestone:

```bash
pytest \
  tests/core/unit/agents/test_structurer_rationale.py \
  tests/core/unit/agents/test_change_summary_producers.py \
  tests/products/ensaio/unit/test_pending_proposal.py \
  -v
```

**Esperado:** 24 passed.

---

## Subir o app do Ensaio

```bash
cd products/ensaio
reflex run
```

Aguardar mensagem `App running at http://localhost:3000`. Abrir essa URL no navegador.

> **📌 Sessão descartável.** Recarregar a página zera tudo.

---

## Épico E-PROTO2-2 — Metodologista com escopo e qualidade afiados

> Critérios em [products/ensaio/ROADMAP.md](../../products/ensaio/ROADMAP.md), seção E-PROTO2-2.

### 2.1 — Prompt do Metodologista limpo (Tese central, sem Formato/Estrutura)

**Critério de aceite:** Metodologista provoca sobre tese central, métricas, evidência, rigor, contexto e intenção. **Não** menciona formato (IMRaD, revisão etc.) nem ordem/sequência das seções.

**Gatilho:**
1. (sessão limpa, recarregue a página) Cole exatamente este prompt no chat:
   ```
   Estou escrevendo um artigo sobre o uso de Claude Code no meu fluxo. Acho que ele "deixa o desenvolvedor mais produtivo". Que estrutura você sugere?
   ```
2. Aguarde a resposta. Se o Orquestrador responder sem chamar o Metodologista, mande:
   ```
   Pode chamar o Metodologista pra olhar isso?
   ```

**Resultado esperado:**
- Aparece bolha do `🔬 Metodologista` com **uma única pergunta** sobre **um destes temas**: a defensibilidade da tese ("deixa mais produtivo" sem critério/baseline), evidência/métrica que sustenta a afirmação, ou a intenção do artigo (informar / propor / demonstrar).
- A pergunta termina com `?` e está em pt-BR.

**Sinal de falha:**
- A pergunta menciona "IMRaD", "formato do artigo", "qual a estrutura", "ordem das seções", ou similar.
- A bolha vem com mais de uma pergunta numerada.
- A bolha começa com "Como Metodologista, eu..." ou retorna vazio.

### 2.2 — Postura do Estruturador focada em storytelling

**Critério de aceite:** Estruturador é convocado quando há material para propor ordem/sequência de seções; entrega proposta com **racional curto** (1-2 frases). Não cobre contexto/problema/contribuição (território do Metodologista).

**Gatilho:**
1. (sessão limpa) Cole exatamente:
   ```
   Fiz um experimento comparando Claude Code com Cursor pra implementar um endpoint REST. Medi tempo total: Claude 18min, Cursor 25min, sem diferença visível na qualidade do código. Quero virar isso em artigo curto.
   ```
2. Se o Orquestrador não convocar o Estruturador no primeiro turno, mande:
   ```
   Pode pedir pro Estruturador organizar isso em seções?
   ```

**Resultado esperado:**
- Bolha do `📐 Estruturador` aparece com a manchete `📐 Estrutura proposta` acima do label de agente (ver E-PROTO2-3.3).
- Bubble especial de proposta (azul, com borda) surge logo acima do input do chat (não dentro do histórico). Mostra: lista numerada de seções (ex.: "1. Introdução / 2. Métodos / 3. Resultados / 4. Discussão"), uma frase ou duas em itálico explicando por que essa ordem, e três botões: **Aceitar** (verde), **Editar** (azul soft), **Recusar** (cinza soft).

**Sinal de falha:**
- Bubble especial não aparece — a proposta vem só como bolha de chat normal, sem ações.
- Bubble aparece mas sem racional (linha em itálico ausente).
- Estruturador entrega texto longo discutindo o problema/contribuição em vez da ordem das seções.

### 2.3 — Sem ordem fixa entre Metodologista e Estruturador

**Critério de aceite:** Orquestrador continua decidindo *quando* convocar quem. Não há sequência mandatória Metodologista → Estruturador nem Estruturador → Metodologista.

**Gatilho:**
1. (sessão limpa) Cole exatamente:
   ```
   Quero estruturar um artigo sobre meu experimento com agentes LangGraph.
   ```
2. Aguarde a primeira resposta de agente (≠ Orquestrador).
3. Anote qual agente apareceu primeiro: Metodologista 🔬 ou Estruturador 📐.
4. Recarregue a página (F5) — sessão zera.
5. Repita o passo 1 e o passo 2.

**Resultado esperado:**
- Em ambas as execuções, *algum* especialista aparece (📐 ou 🔬), e a escolha pode variar entre as duas execuções *ou* dentro de uma mesma sessão estendida. Nenhuma das duas é forçada a vir antes da outra.
- Em particular: é aceitável Estruturador vir primeiro, Metodologista vir primeiro, ou só um dos dois aparecer no primeiro turno.

**Sinal de falha:**
- Toda sessão sempre inicia com o mesmo agente especialista forçado, independente do conteúdo do prompt.
- Aparece uma sequência rígida tipo "Metodologista provoca → Estruturador propõe" sempre na mesma ordem.

---

## Épico E-PROTO2-1 — Co-decisão da Estrutura

> Critérios em [products/ensaio/ROADMAP.md](../../products/ensaio/ROADMAP.md), seção E-PROTO2-1.

### 1.1 — Proposta sem auto-commit

**Critério de aceite:** Quando o Estruturador propõe seções, elas ficam pendentes aguardando aceite. O painel direito do artigo **não** é populado automaticamente.

**Gatilho:**
1. (sessão limpa, recarregue a página) Cole exatamente:
   ```
   Fiz um experimento medindo o tempo de geração de testes com e sem Claude Code. Coletei dados de 10 endpoints. Pode propor a estrutura do artigo?
   ```
2. Aguarde a resposta do `📐 Estruturador`.

**Resultado esperado:**
- Bubble especial de proposta aparece acima do input do chat (caixa azul com borda).
- Painel direito (40% da tela) continua mostrando exatamente: `Aguardando proposta de estrutura...` com o ícone de documento e o texto "Continue conversando sobre seu experimento...".
- Input do chat continua habilitado (cursor pisca, dá pra digitar).

**Sinal de falha:**
- Painel direito aparece populado com seções sem o usuário ter clicado em **Aceitar**.
- Bubble de proposta não aparece — só uma bolha de chat normal.
- Input do chat fica desabilitado/cinza enquanto a proposta está pendente.

### 1.2 — Aceitar a proposta

**Critério de aceite:** Clicar em **Aceitar** comita a proposta em `current_article` e zera o pendente. O bubble especial some, o painel direito popula com as seções (todas em estado `empty`/badge "—").

**Gatilho:**
1. (continuação de 1.1, com bubble especial visível) Clique no botão verde **Aceitar** dentro do bubble.

**Resultado esperado:**
- O bubble especial de proposta desaparece da tela.
- O painel direito deixa de mostrar "Aguardando proposta..." e renderiza um accordion com pelo menos 3 seções.
- Cada item do accordion mostra: título da seção, badge cinza com `—`, e (quando expandido) o texto `Clique em Gerar para redigir esta seção.` + botão **Gerar**.

**Sinal de falha:**
- Bubble continua visível depois de clicar **Aceitar**.
- Painel direito segue vazio.
- Aparece traceback/erro vermelho no chat.

### 1.3 — Recusar a proposta

**Critério de aceite:** Clicar em **Recusar** limpa o pendente sem tocar em `current_article`. Uma nota curta no histórico marca a recusa.

**Gatilho:**
1. (sessão limpa) Repita o gatilho de 1.1 até o bubble aparecer.
2. Clique no botão cinza **Recusar** dentro do bubble.

**Resultado esperado:**
- O bubble especial desaparece.
- Aparece no histórico de chat uma bolha curta com texto exatamente: `Proposta de estrutura recusada.` (em itálico).
- Painel direito continua mostrando `Aguardando proposta de estrutura...`.

**Sinal de falha:**
- Painel direito ganha seções (não deveria — recusa não comita).
- Bubble continua aparecendo após clicar **Recusar**.
- Nenhuma nota aparece no histórico.

### 1.4 — Editar a proposta antes de aceitar

**Critério de aceite:** Clicar em **Editar** abre a lista em modo editável (renomear, mover, remover, adicionar). Confirmar comita a versão editada; cancelar volta à proposta original.

**Gatilho:**
1. (sessão limpa) Repita o gatilho de 1.1 até o bubble aparecer.
2. Clique no botão azul soft **Editar** dentro do bubble.
3. No primeiro campo de input, troque o texto por: `Introdução modificada`.
4. Clique no botão **↑** da segunda linha (move a segunda seção para o topo).
5. Clique no botão **🗑️** da última linha (remove a última seção).
6. Clique no botão **+ Adicionar seção**.
7. Clique no botão verde **Confirmar edição**.

**Resultado esperado:**
- Modo de edição: cada linha tem um campo de input + botões `↑`, `↓`, `🗑️`. Há um botão `+ Adicionar seção` ao final e dois botões finais: **Confirmar edição** (verde) e **Cancelar** (cinza soft).
- Após **Confirmar edição**: bubble desaparece. Painel direito popula com a lista editada — primeira seção é a que era a segunda originalmente, depois `Introdução modificada`, depois as restantes minus a última, mais uma seção chamada `Nova seção` no final.

**Sinal de falha:**
- Edição não persiste depois de Confirmar.
- Botões `↑/↓/🗑️/+` não respondem ao clique.
- Cancelar comita as edições (não deveria).

### 1.4-edge — Lista vazia bloqueia o aceite

**Critério de aceite:** Se o usuário remover todas as seções no modo de edição, o aceite fica bloqueado com mensagem inline.

**Gatilho:**
1. (sessão limpa) Faça o gatilho 1.1 até o bubble.
2. Clique em **Editar**.
3. Clique em **🗑️** em todas as linhas até a lista ficar vazia.
4. Clique em **Confirmar edição**.

**Resultado esperado:**
- Aparece mensagem em vermelho dentro do bubble: `A estrutura precisa de pelo menos uma seção.`
- O bubble continua em modo edição.
- Painel direito continua vazio (`Aguardando proposta...`).

**Sinal de falha:**
- Confirma a edição vazia e comita um `current_article` sem seções.
- Mensagem inline não aparece.

### 1.5 — Re-proposição substitui a pendente

**Critério de aceite:** Quando o Estruturador propõe uma nova estrutura enquanto há uma pendente, a nova substitui a anterior. Não há fila.

**Gatilho:**
1. (sessão limpa) Faça o gatilho 1.1 até o bubble aparecer com a primeira proposta.
2. **Sem aceitar nem recusar**, mande no chat:
   ```
   Na verdade, é mais um relato de experiência do que um estudo empírico. Pode repropor?
   ```
3. Aguarde a nova resposta do `📐 Estruturador`.

**Resultado esperado:**
- O bubble especial é atualizado para mostrar a nova lista de seções (provavelmente diferente — relato de experiência tende a ter "Contexto / Experiência / Aprendizados" ou similar).
- Não há dois bubbles empilhados.

**Sinal de falha:**
- Aparecem dois bubbles especiais ao mesmo tempo.
- O bubble continua mostrando a proposta antiga.

---

## Épico E-PROTO2-3 — Manchete "o que mudou" em mensagens de agente

> Critérios em [products/ensaio/ROADMAP.md](../../products/ensaio/ROADMAP.md), seção E-PROTO2-3.

### 3.1 — Manchete do Estruturador

**Critério de aceite:** Toda mensagem do Estruturador que vem com proposta de estrutura traz manchete `📐 Estrutura proposta` acima do label de agente, em fonte menor que o conteúdo.

**Gatilho:**
1. Use a sessão de E-PROTO2-1.1 (Estruturador acabou de propor) ou rode aquele gatilho de novo.

**Resultado esperado:**
- A bolha do `📐 Estruturador` mostra, na ordem de cima para baixo:
  1. Linha curta `📐 Estrutura proposta` em fonte pequena, cor azul/accent.
  2. Label `📐 Estruturador` em cinza pequeno bold.
  3. Conteúdo da mensagem.

**Sinal de falha:**
- Manchete ausente, ou aparece embaixo do label.
- Manchete com texto diferente (ex.: "Estrutura sugerida", "Proposta").

### 3.2 — Manchete do Metodologista

**Critério de aceite:** Quando o Metodologista responde com pergunta/provocação, vem com manchete `🔬 Lacuna apontada`. Quando responde com a frase de aceite curta ("O contexto está bem descrito. Continue."), **não** vem com manchete.

**Gatilho A (provocação → manchete presente):**
1. (sessão limpa) Cole exatamente:
   ```
   Implementei um pipeline de extração de embeddings que ficou 3x mais rápido. Quero descrever isso num artigo.
   ```
2. Se Metodologista não vier no primeiro turno, mande:
   ```
   Pode chamar o Metodologista pra olhar?
   ```

**Resultado esperado A:**
- Bolha do `🔬 Metodologista` aparece com manchete `🔬 Lacuna apontada` em cima.

**Gatilho B (aceite → sem manchete):**
1. (continuando a mesma sessão, depois de responder a provocação) Mande detalhes:
   ```
   Comparei o pipeline com a versão anterior em 100 textos, mediu tempo médio. Antes: 2.4s/texto. Depois: 0.8s/texto. Mesma máquina, mesmo modelo de embedding.
   ```
2. Se o Metodologista voltar a aparecer, observe a próxima resposta dele.

**Resultado esperado B:**
- Se a resposta dele for exatamente ou começar com "O contexto está bem descrito.", a manchete `🔬 Lacuna apontada` **não** aparece nessa bolha — só o label `🔬 Metodologista`.

**Sinal de falha:**
- Manchete `🔬 Lacuna apontada` aparece em uma bolha que diz "O contexto está bem descrito".
- Manchete não aparece em uma bolha onde o Metodologista faz pergunta legítima.

### 3.3 — Manchete do Orquestrador (mudança de foco)

**Critério de aceite:** Orquestrador preenche manchete `🎯 Foco atualizado` apenas quando o `focal_argument` muda em algum campo relevante (intent, subject, population, metrics, article_type) em relação ao turno anterior. Conversa puramente reconhecimento/clarificação **não** preenche.

**Gatilho A (primeira menção de foco):**
1. (sessão limpa) Cole exatamente:
   ```
   Quero escrever sobre o uso de Claude Code em pesquisa. População: pesquisadores juniores. Intenção: demonstrar ganho de produtividade.
   ```

**Resultado esperado A:**
- A bolha do `🎯 Orquestrador` (a primeira que tocar foco) traz a manchete `🎯 Foco atualizado` em cima.

**Gatilho B (turno conversacional sem mudança):**
1. (continuação) Mande:
   ```
   Sim, é isso mesmo.
   ```

**Resultado esperado B:**
- A próxima bolha do `🎯 Orquestrador` **não** traz manchete (só o label).

**Sinal de falha:**
- Manchete `🎯 Foco atualizado` aparece em bolha de mero reconhecimento ("Entendi.", "Pode me contar mais...").
- Manchete não aparece quando o usuário trouxe novo intent/subject/população/métricas.

### 3.4 — Mensagens do usuário nunca mostram manchete

**Critério de aceite:** Bolhas do `👤 Você` nunca exibem manchete (campo só faz sentido para mensagens de agente).

**Gatilho:**
1. (qualquer sessão) Olhe todas as bolhas com label `👤 Você` ao longo da sessão.

**Resultado esperado:**
- Nenhuma bolha do usuário tem texto pequeno azul acima do label.

**Sinal de falha:**
- Aparece manchete em bolha do usuário.

---

## Épico E-PROTO2-4 — Colapsar/expandir seções no painel

> Critérios em [products/ensaio/ROADMAP.md](../../products/ensaio/ROADMAP.md), seção E-PROTO2-4.

### 4.1 — Estado inicial colapsado

**Critério de aceite:** Após aceitar a proposta de estrutura, todas as seções aparecem no painel direito **colapsadas por padrão**. Recarregar a página volta tudo a colapsado.

**Gatilho:**
1. Use a sessão de E-PROTO2-1.2 (proposta aceita, painel populado), ou rode aquele gatilho até clicar **Aceitar**.

**Resultado esperado:**
- Painel direito mostra a lista de seções como itens de accordion (cada item é uma caixa com borda, fundo branco).
- Cada item exibe **apenas** o título da seção + badge cinza `—`. **Não** mostra o texto `Clique em Gerar para redigir esta seção.` nem o botão **Gerar** (esses só aparecem quando expandido).
- Recarregar a página (F5) volta o painel a `Aguardando proposta de estrutura...` (sessão descartável).

**Sinal de falha:**
- Logo após o aceite, alguma seção já vem expandida mostrando o botão **Gerar**.
- Recarregar mantém estado anterior (a sessão deveria zerar).

### 4.2 — Toggle por seção é independente

**Critério de aceite:** Clicar no header de uma seção alterna apenas aquela; expandir uma não afeta as outras (pode ter várias abertas ao mesmo tempo).

**Gatilho:**
1. (continuação de 4.1, painel com seções colapsadas) Clique no título da primeira seção (ex.: "Introdução").
2. Clique no título da terceira seção (ex.: "Resultados").
3. Clique de novo no título da primeira seção.

**Resultado esperado:**
- Após passo 1: primeira seção expande, mostra placeholder + botão **Gerar**. Outras continuam colapsadas.
- Após passo 2: primeira **e** terceira seções estão expandidas simultaneamente. Segunda permanece colapsada.
- Após passo 3: primeira fecha; terceira continua aberta.

**Sinal de falha:**
- Expandir uma fecha a outra (comportamento de "single open").
- Clicar no header não responde.
- Botões dentro do conteúdo expandido (Gerar/Regenerar) não funcionam.

### 4.3 — Edição inline funciona dentro da seção expandida

**Critério de aceite:** Edição inline de markdown (E-PROTO-2.3) continua funcionando dentro da seção expandida.

**Gatilho:**
1. (continuação de 4.2, primeira seção expandida) Clique no botão **Gerar** da primeira seção.
2. Aguarde o ✍️ Writer redigir (indicador no topo do painel).
3. Quando o conteúdo aparecer com badge `Rascunho` (laranja), clique sobre o markdown — modo de edição abre.

**Resultado esperado:**
- Após **Gerar**: badge passa de `—` para `Rascunho` (laranja); o corpo da seção mostra texto markdown gerado pelo Writer.
- Clicar no corpo abre uma textarea com o markdown editável; após salvar, badge vira `Editado` (verde).

**Sinal de falha:**
- Botão **Gerar** não responde, ou indicador de Writer não aparece.
- Badge não atualiza após geração ou edição.
- Edição não persiste o conteúdo na seção.

---

---

## Critérios de aprovação

Marcar **go** se todos os itens abaixo passam:

- [ ] Suite unitária em verde (249 passed)
- [ ] E-PROTO2-1: bubble especial aparece, aceite/recusa/edição funcionam, não há auto-commit
- [ ] E-PROTO2-2: Metodologista provoca sobre tese/intenção (não sobre formato/estrutura); Estruturador foca storytelling com racional
- [ ] E-PROTO2-3: manchetes "📐 Estrutura proposta", "🔬 Lacuna apontada", "🎯 Foco atualizado" aparecem nos turnos certos
- [ ] E-PROTO2-4: seções iniciam colapsadas no painel direito; toggle por seção é independente
- [ ] Nenhum erro "React Hooks violation" no console do navegador durante a sessão inteira

Marcar **no-go** se qualquer roteiro abaixo falha em **Sinal de falha**.

---

## Pós-merge

Cleanup skill apaga `current_implementation.md` e move este arquivo para o histórico (mantido na PR mergeada). O próximo milestone sobrescreve `current_validation.md`.
