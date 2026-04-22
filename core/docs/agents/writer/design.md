# Writer (Escritor) — Arquitetura

> **Status:** Planejado — primeiro agente motivado pelo Ensaio, compartilhado com o Produtor Científico.
> **Nota:** Para papel, responsabilidades e critérios de qualidade, ver `core/docs/agents/overview.md` (seção "Escritor").

## Decisão Arquitetural: Nasce no Core

O Writer **não nasce no produto Ensaio**. É um agente do core desde o início, mesmo sendo o Ensaio o primeiro produto a consumi-lo.

**Justificativa:**
- O Writer será reusado pelo Produtor Científico (ver `products/produtor-cientifico/docs/vision.md`).
- Colocá-lo inicialmente dentro do Ensaio exigiria promoção posterior ao core, repetindo o custo que a separação Core ↔ Produto existe justamente para evitar.
- Ver `core/docs/vision/super_system.md` para o princípio de desacoplamento.

## Decisão Arquitetural: Começa Simples

Primeira versão do Writer é **um nó simples**: recebe contexto (texto conversacional, argumento focal, estado da conversa) e devolve markdown.

- Sem sub-grafo, sem loop interno de refinamento.
- **Refinamento com feedback do usuário é loop externo**, orquestrado pelo produto consumidor via nova invocação do nó — não via loop interno do Writer. Cada feedback vira uma chamada nova com o contexto acumulado; o Writer não guarda estado entre invocações.
- Primeiro consumidor deste padrão é o **Ensaio na POC** (funcionalidade 3.4 do E-POC-3 — refinamento minimalista): pesquisador pede ajustes em linguagem natural no chat e o produto reinvoca o Writer passando o histórico conversacional acumulado + o artigo anterior; o Writer regera o artigo inteiro em uma passada.
- Evolução para **refinamento por seção** (Writer gera/revisa seção a seção, habilitando rascunho progressivo) é decisão arquitetural separada — escopo do épico core **C-ENSAIO-3 (Writer por seção)**, fora da V1.
- Sem pipeline de compilação multi-seção na V1 — a primeira versão gera o artigo em uma passada.
- Organização do código já antecipa generalização futura: inputs e outputs estruturados, prompt separado por responsabilidade, sem acoplamento com termos específicos do Ensaio.

## Decisão Arquitetural: Estruturas de Artigo no Prompt, Não em Enum

A **base de conhecimento sobre estruturas comuns de artigo vive no prompt do Writer**, não em um campo `article_type`, enum ou schema.

**Consequências:**
- Writer decide seções (Introdução, Metodologia, Resultados, Discussão...) com base no que foi conversado, não num tipo pré-declarado.
- Estruturas emergem da conversa — o produto consumidor não precisa classificar o artigo antes de escrever.
- Evolução da base de conhecimento sobre tipos de artigo = edição de prompt, não migração de dados.
- Produtos que já usam `article_type` no `focal_argument` (Revelar, Produtor Científico) continuam usando; o Writer **não depende** desse campo para decidir a estrutura.

**Contraste com Ensaio:** o Ensaio não mantém campo `article_type`. Ver `products/ensaio/docs/vision.md` seção sobre Estrutura do Artigo.

## Maturidade por Estágio

As 4 dimensões do Writer (contexto, intenção, formato, estrutura — ver `core/docs/agents/overview.md`) evoluem em como são coletadas e decididas ao longo dos estágios:

**V1 (POC do Ensaio):** Writer infere todas as dimensões da conversa. Se alguma dimensão não aparecer naturalmente, Writer adota defaults razoáveis. Refinamento externo via loop do produto (ver funcionalidade 3.4 do E-POC-3) compensa eventual genericidade do resultado.

**Estado-alvo:** Sistema provoca ativamente sobre dimensões faltantes. Propõe formato após conversa ("pelo que me contou, recomendo IMRaD — concorda?"), pergunta intenção quando não emerge da conversa, sugere estrutura narrativa e confirma com o usuário. Qual agente executa essa provocação (Writer, Orquestrador, Metodologista, ou combinação) é decisão de refinamento futuro.

O caminho V1 → estado-alvo passa pelo Protótipo e MVP do Ensaio. O épico E-PROTO-5 (Metodologista aplicado ao Ensaio) é candidato natural para abrigar parte dessa provocação ativa.

## Injeção de Contexto de Produto

Writer recebe contexto de domínio/foco via parâmetros, **sem conhecer o nome do produto consumidor**. Segue o padrão descrito em `core/docs/vision/super_system.md` (Injeção de Contexto de Produto).

## Referências

- `core/docs/agents/overview.md` — Responsabilidades do Escritor
- `core/docs/vision/super_system.md` — Desacoplamento Core ↔ Produto
- `docs/ROADMAP.md` — Épico Escritor (C-ENSAIO-2 V1; C-ENSAIO-3 refinamento por seção)
- `products/ensaio/docs/vision.md` — Primeiro produto consumidor
- `products/ensaio/ROADMAP.md` — Épico E-POC-3 (padrão de loop externo de refinamento na POC); Épico E-PROTO-5 (Metodologista aplicado ao Ensaio — candidato para provocação ativa)
- `products/produtor-cientifico/docs/vision.md` — Segundo produto consumidor (futuro)
