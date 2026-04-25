# ADR 001 — Stack da interface do Protótipo do Ensaio

- **Data:** 2026-04-25
- **Status:** Aceita
- **Saída de:** sessão de refinamento estratégico de E-PROTO-1.1 (`products/ensaio/ROADMAP.md`)
- **Aplica-se a:** Protótipo do Ensaio (PROTO-ENSAIO)

## Contexto

O POC do Ensaio foi entregue em Streamlit como **atalho descartável** (vision §7), assumido em comum acordo. A POC validou conversa + geração de artigo, mas a validação manual evidenciou três limites concretos do Streamlit incompatíveis com o critério de saída do Protótipo (desenvolvedor usando de verdade, no fluxo real):

1. **Cold start lento** — abrir o app demora segundos perceptíveis em hardware modesto.
2. **Blur opaco como feedback de processamento** — cobre o histórico inteiro, impede leitura durante a chamada do agente.
3. **Falta de transparência sobre quem está falando** — bubbles do chat não distinguem Orquestrador, Estruturador, Metodologista e Writer.

Vision §7 declara explicitamente que a stack do Protótipo é **decisão deste refinamento** (não da visão), mas exige princípio de viabilização:

> Lógica de domínio (estado do artigo, pendências, decisões dos agentes) vive toda no core. UI do Ensaio é **burra** — só renderiza e chama a API do core. Trocar stack = trocar camada de apresentação, sem tocar em regra de negócio.

Esse princípio é a restrição dura: o estado do artigo + conversa precisa ficar serializável e morar no backend, não na UI, para que o MVP troque a camada de armazenamento sem refazer o domínio (vision §7, §10).

## Critérios de avaliação

| Critério | Justificativa |
|---|---|
| **Cold start aceitável** | Crítico para o desenvolvedor abrir o app no fluxo real (não esperar 5+ segundos). |
| **Ergonomia: chat + painel lateral com edição inline** | E-PROTO-2 vai materializar painel seccionado com edição; stack chat-only não cabe. |
| **Princípio de viabilização §7 (UI burra, estado serializável no backend)** | Restrição dura da vision; afeta a passagem para o MVP. |
| **Custo de manutenção** | Operação de um único desenvolvedor; duas stacks (FE + BE separados) dobra custo. |
| **Continuidade do ritmo Python** | Codebase é Python ponta-a-ponta (LangGraph, agentes, testes); mudar paradigma é overhead. |

Critérios secundários (não decisivos isoladamente, registrados para rastreabilidade): suporte a streaming, ecossistema de componentes, latência de hot reload em dev.

## Opções avaliadas

### A. Streamlit melhorado

Continuar em Streamlit investindo em customização (CSS, componentes custom, columns).

- **Cold start:** ❌ ruim — característica do framework (warm-up + reruns globais).
- **Ergonomia:** ⚠️ limitada — modelo de "rerun completo a cada interação" colide com edição inline e indicadores não-bloqueantes.
- **Princípio §7:** ❌ vaza — `st.session_state` é estado da UI, não do backend; já é sintoma no POC (`focal_argument`, `current_article` em session_state).
- **Custo de manutenção:** ✅ baixo — investimento já feito.
- **Ritmo Python:** ✅ mantido.

**Veredicto:** descartada. Falha em três limites concretos da POC (cold start, blur, princípio §7) — manter Streamlit não tira o Protótipo do estágio anterior.

### B. Chainlit

Framework Python chat-first com suporte a "elements" laterais e streaming nativo.

- **Cold start:** ✅ bom — SPA real.
- **Ergonomia:** ⚠️ chat-first — painel lateral existe via `cl.Element`, mas edição inline de markdown estruturado por seção (alvo de E-PROTO-2) foge do padrão idiomático.
- **Princípio §7:** ✅ OK — backend mantém estado.
- **Custo de manutenção:** ✅ baixo.
- **Ritmo Python:** ✅ mantido.

**Veredicto:** plausível, descartada por margem. Forçar painel seccionado com edição inline em framework chat-first acumula dívida de UX que cresce em E-PROTO-2.

### C. Reflex (Python full-stack) — **escolhida**

Framework Python que compila para React + FastAPI sob o capô; desenvolvedor escreve `rx.State` (backend) e componentes (frontend) em Python puro.

- **Cold start:** ✅ bom — SPA real, frontend pré-compilado.
- **Ergonomia:** ✅ alta — componentes arbitrários, layouts livres, edição inline natural.
- **Princípio §7:** ✅ **forte** — separação `rx.State` (backend) ↔ componentes (view) é arquitetural; UI não tem estado próprio, força lógica no backend. Encaixa exatamente com vision §7.
- **Custo de manutenção:** ⚠️ médio — uma stack só, mas curva inicial maior que Streamlit/Chainlit.
- **Ritmo Python:** ✅ mantido.

**Veredicto:** escolhida. Único framework avaliado em que o princípio §7 deixa de ser disciplina (que precisa ser fiscalizada em revisão) e vira **modelo do framework** (estado vive no backend por construção). Custo de aprendizado é absorvido porque o Protótipo é frente de migração de stack assumida — não é overhead inesperado.

### D. Next.js + FastAPI

Stack canônica de web app moderna: frontend dedicado (Next.js/SvelteKit/equivalente) consumindo API HTTP do backend Python (FastAPI).

- **Cold start:** ✅ ótimo.
- **Ergonomia:** ✅ máxima — controle total sobre UX.
- **Princípio §7:** ✅ limpo — separação física entre FE e BE.
- **Custo de manutenção:** ❌ alto — duas stacks, dois ecossistemas de dependência, dois fluxos de build, dois testes.
- **Ritmo Python:** ⚠️ parcial — FE em TS/JS quebra o paradigma da operação.

**Veredicto:** descartada por sobre-engenharia para o estágio. Reflex captura o mesmo benefício arquitetural (separação backend/view) sem o custo de duas stacks. Next.js + FastAPI volta para mesa apenas se Reflex se mostrar limitante ou se polish de UX virar gargalo no MVP/pós-MVP — registrado como gatilho de revisão deste ADR.

## Decisão

**Adotar Reflex como stack da interface do Protótipo do Ensaio.**

Critério decisivo: Reflex é a única opção avaliada em que o princípio de viabilização §7 (estado serializável no backend, UI burra) é **modelo do framework**, não disciplina externa a ser fiscalizada. Resolve os três limites concretos do Streamlit (cold start, feedback não-bloqueante, transparência de agente) e prepara a passagem para o MVP sem refazer domínio.

## Consequências

**Positivas:**

- Estado do artigo + conversa fica em `rx.State` (backend, serializável); E-PROTO-2 (rascunho seccionado) aterrisa no contrato `Article` produzido por C-ENSAIO-3 sem conflito de "onde mora o estado".
- Migração para o MVP pode trocar persistência (in-memory → SQLite) editando apenas a camada de state, sem alterar componentes.
- Uma stack única, Python puro — operação de um único desenvolvedor mantém ritmo.
- Componentes Reflex permitem indicadores de processamento inline (E-PROTO-1.4) e labels por bubble (E-PROTO-1.3) sem hacks.

**Negativas / acoplamentos novos:**

- Dependência nova: `reflex>=0.6` em `requirements.txt`. Curva de aprendizado inicial absorvida em E-PROTO-1.2.
- Acoplamento com `products/revelar/app/components/chat_history.py` (importado em `products/ensaio/app/chat.py:37`) é **rompido** — Reflex tem componente próprio. Revelar não é afetado (continua em Streamlit por enquanto; futura migração do Revelar é decisão fora do escopo deste ADR).
- Build do Reflex gera `.web/` e cache local; precisa entrar no `.gitignore` se ainda não estiver.

**Reversibilidade:**

- Trocar de Reflex para outra stack (Next.js + FastAPI no extremo) exigiria reescrever os componentes da view, mas o `rx.State` mapeia direto para um modelo Pydantic + endpoints FastAPI. Decisão é reversível com custo proporcional ao tamanho do produto no momento.

**Gatilhos para revisão deste ADR:**

- Polish de UX virar gargalo no MVP ou pós-MVP (Reflex limita customização avançada).
- Outra ICT/parceiro requerer deploy multi-tenant ou autenticação real — pode favorecer separação Next.js + FastAPI.
- Reflex apresentar instabilidade ou stagnação como projeto open-source.

## Referências

- `products/ensaio/docs/vision.md` §7 (Stack da Interface), §10 (Escopo Protótipo)
- `products/ensaio/ROADMAP.md` (E-PROTO-1)
- `docs/process/refinement/planning_guidelines.md` (definição de Protótipo)
- `core/docs/vision/super_system.md` (princípio de UI burra)
