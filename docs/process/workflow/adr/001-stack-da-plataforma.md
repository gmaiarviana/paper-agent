# ADR 001 — Stack da plataforma de workflow

- **Data:** 2026-06-19
- **Status:** Aceita
- **Saída de:** sessão de refinamento estratégico da fase Piloto (`docs/process/workflow/ROADMAP.md`, milestone `PILOTO-WORKFLOW-UX`)
- **Aplica-se a:** plataforma de workflow (`tools/workflow_platform/`), estágio Piloto em diante

## Contexto

A plataforma de workflow nasceu em Streamlit no Protótipo (W-PROTO-PLAT-1,
PR #106) como camada de leitura sobre markdown — kanban + fila reativa. O
estágio Piloto muda a natureza da plataforma em duas frentes declaradas na
vision (§"Eixo de Estágios", §"Forma da Plataforma"):

1. **UX de cockpit de uso diário** — "estrutura funciona bem, fricção
   operacional baixa". Em uso real (PR #121) apareceram frições estruturais:
   o painel de detalhe some abaixo da viewport quando a fila enche; não há
   co-visibilidade lista↔detalhe.
2. **Canal único** — a plataforma deixa de ser só leitura e passa a
   **disparar execução** do agente headless por baixo dos panos
   (`PILOTO-WORKFLOW-CANAL-UNICO`), lendo **progresso ao vivo** de um
   processo de segundo plano.

Ambas batem nos limites do modelo do Streamlit (rerun top-to-bottom, sem
long-running nativo, sem layout/sticky livre) — os mesmos limites que a
[ADR 001 do Ensaio](../../../products/ensaio/docs/adr/001-stack-do-prototipo.md)
documentou ao mover aquele produto de Streamlit→Reflex (cold start, feedback
de processamento bloqueante, ergonomia de layout rico).

A plataforma já segue, por construção, o princípio de "UI burra": toda a
lógica é stack-independente (`parser.py`, `models.py`, `queue/*`,
`prompts/*`, `config_loader.py`, `preferences.py`); só `app.py` e `views/*`
dependem de Streamlit. O custo de troca de stack está confinado à camada de
view.

## Critérios de avaliação

| Critério | Justificativa |
|---|---|
| **Execução de segundo plano + streaming** | Driver decisivo: o CANAL-UNICO dispara agente headless e lê progresso ao vivo. Rerun global do Streamlit não cobre long-running com feedback incremental. |
| **Ergonomia: co-visibilidade lista↔detalhe, layout livre** | Frição estrutural do Piloto (painel some abaixo da viewport); exige duas colunas / painel ancorado. |
| **Custo de migração confinado à view** | A lógica já é stack-independente; a stack escolhida deve preservar o miolo sem reescrita. |
| **Continuidade do ritmo Python** | Codebase e skills são Python ponta-a-ponta; operação de um único desenvolvedor. |
| **Maturidade já na casa** | Reusar aprendizado evita avaliar/operar stack do zero. |

## Opções avaliadas

### A. Streamlit melhorado

Continuar em Streamlit investindo em CSS/columns/componentes custom.

- **Background + streaming:** ❌ — rerun global colide com processo de
  segundo plano e progresso incremental (o bloqueio central do CANAL-UNICO).
- **Ergonomia:** ⚠️ limitada — sem sticky/scroll independente nativo.
- **Custo confinado:** ✅ — investimento já feito.
- **Ritmo Python / maturidade:** ✅.

**Veredicto:** descartada. Falha exatamente no driver decisivo (canal único)
e no atrito de UX que o Piloto precisa eliminar. Polir Streamlit agora vira
trabalho jogado fora na migração inevitável do CANAL-UNICO.

### B. Reflex (Python full-stack) — **escolhida**

Compila para React + FastAPI sob o capô; `rx.State` (backend) + componentes
(view) em Python puro.

- **Background + streaming:** ✅ — SPA real, `rx.State` com background tasks
  e atualização incremental de estado encaixam no disparo+progresso do
  canal único.
- **Ergonomia:** ✅ alta — layout livre, duas colunas, painel ancorado sem
  hack.
- **Custo confinado:** ✅ — só a view migra; o miolo (`parser`, `queue`,
  `prompts`, `config_loader`, `preferences`) é importado intocado.
- **Ritmo Python / maturidade:** ✅ **forte** — já roda no Ensaio
  (`reflex>=0.6`, `products/ensaio/rxconfig.py`); curva já paga uma vez.

**Veredicto:** escolhida. Resolve o driver decisivo, dissolve o risco de
framework do layout, e reusa maturidade já existente no repo.

### C. Next.js + FastAPI

Frontend dedicado consumindo API HTTP do backend Python.

- **Background + streaming / ergonomia:** ✅ máximos.
- **Custo de manutenção:** ❌ alto — duas stacks, dois ecossistemas, FE em
  TS/JS quebra o paradigma Python da operação.

**Veredicto:** descartada por sobre-engenharia para o estágio — mesmo
veredicto da ADR 001 do Ensaio. Reflex captura o benefício arquitetural
(separação backend/view, streaming) sem o custo de duas stacks. Volta à
mesa só se Reflex se mostrar limitante.

## Decisão

**Adotar Reflex como stack da plataforma de workflow, a partir do Piloto.**

A migração é a **fundação** do milestone `PILOTO-WORKFLOW-UX`
(épico W-PILOTO-UX-1): porta o esqueleto + a aba Fila como fatia fina que
valida a decisão no uso real, depois o Kanban; o miolo stack-independente é
preservado. É também pré-requisito de `PILOTO-WORKFLOW-CANAL-UNICO`, onde o
disparo+progresso ao vivo torna a escolha incontornável.

## Consequências

**Positivas:**

- Estado da plataforma migra de `st.session_state` para `rx.State`
  (backend), coerente com "markdown é fonte da verdade / plataforma é view
  derivada" — o estado da UI fica explícito e serializável.
- O CANAL-UNICO aterrissa disparo headless + streaming sem lutar contra o
  framework.
- O atrito de layout do Piloto (co-visibilidade, painel ancorado) some por
  capacidade nativa, não por hack.
- Uma stack única, Python puro; reusa o aprendizado de Reflex do Ensaio.

**Negativas / acoplamentos novos:**

- Dependência nova: `reflex>=0.6` no requirements da plataforma.
- Reescrita do view layer (`app.py`, `views/*.py`); o miolo não se mexe.
- Build do Reflex gera `.web/` e cache local — garantir `.gitignore`.

**Reversibilidade:**

- Trocar Reflex por Next.js + FastAPI exigiria reescrever a view, mas o
  `rx.State` mapeia direto para Pydantic + endpoints FastAPI. Custo
  proporcional ao tamanho da plataforma no momento.

**Gatilhos para revisão deste ADR:**

- Reflex limitar polish de UX avançado a ponto de virar gargalo.
- Release a colegas exigir deploy multi-tenant/auth real (pode favorecer
  Next.js + FastAPI — alinhado ao Horizonte da vision).
- Reflex apresentar instabilidade ou stagnação como projeto open-source.

## Referências

- `docs/process/workflow/vision.md` (§"Eixo de Estágios", §"Forma da
  Plataforma", §"Proatividade e execução em segundo plano")
- `docs/process/workflow/ROADMAP.md` (`PILOTO-WORKFLOW-UX`,
  `PILOTO-WORKFLOW-CANAL-UNICO`, §"Tooling > Dispatch headless via CLI")
- `products/ensaio/docs/adr/001-stack-do-prototipo.md` (precedente
  Streamlit→Reflex)
- `tools/workflow_platform/` (separação UI burra: view vs. miolo)
