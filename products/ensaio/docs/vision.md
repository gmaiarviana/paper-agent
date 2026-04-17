# Visão de Produto - Ensaio

> **Nota:** Para filosofia universal do sistema, consulte `core/docs/vision/system_philosophy.md`.
> Para arquitetura do super-sistema, consulte `core/docs/architecture/vision/super_system.md`.

## 1. Visão Geral do Produto Ensaio

- **O que é**: Sistema conversacional para transformar experimentos de código em artigos técnico-científicos publicáveis
- **Para quem**: Pesquisadores de uma ICT (uso institucional) que produzem PoCs e experimentos em desenvolvimento de software, IA agêntica e tecnologias de TRL 3-6
- **Problema resolvido**: O ritmo de experimentos supera a capacidade de produção de artigos. Experimentos acontecem, código fica no repositório, aprendizados se perdem. Falta processo que transforme o que foi feito em conhecimento estruturado e comunicável
- **Diferencial**: Sistema proativo que provoca o pesquisador — identifica lacunas no argumento e solicita métricas, evidências e informações que o artigo precisará
- **Destino**: Publicação técnico-científica formal. Saída pode ser artigo completo ou one-pager para divulgação rápida

### Output do Ensaio
- ✅ Artigo técnico-científico estruturado (pronto para publicação)
- ✅ One-pager para divulgação rápida (saída alternativa)
- ✅ Rastreamento de lacunas, métricas e evidências coletadas ao longo do experimento
- ❌ NÃO produz o experimento em si (parte do trabalho do pesquisador)
- ❌ NÃO substitui revisão humana final (pesquisador mantém autoria)

**Metáfora:** Ensaio é o "laboratório de escrita" onde experimentos viram artigos. O experimento acontece no código; o artigo emerge da conversa entre pesquisador e sistema.

## 2. Posição no Super-Sistema

Ensaio é produto **paralelo ao Revelar**, não sequencial. Usa os mesmos agentes core (Orquestrador, Estruturador, Metodologista) e adicionará o Writer quando implementado — agente que pertencerá ao core e será compartilhado com Produtor Científico. No futuro, também usará Researcher (busca web de papers) e Curator (fichamento — base do Prisma Verbal).

**Relação com outros produtos:**
- **Revelar:** Clareza de pensamento (entrada conversacional genérica)
- **Ensaio:** Documentação de experimentos de código (entrada técnico-científica)
- **Prisma Verbal (futuro):** Extração de proposições de literatura (alimenta Ensaio com referências)
- **Produtor Científico (futuro):** Produção de conteúdo genérico (compartilha Writer com Ensaio)

**Diagrama:**
```
┌─────────────┐     ┌─────────────┐
│   REVELAR   │     │   ENSAIO    │
│  (diálogo)  │     │(experimentos)│
└─────────────┘     └─────────────┘
      │                    │
      └────────┬───────────┘
               ▼
        ┌─────────────────┐
        │  MOTOR VETORIAL │
        │   (biblioteca)  │
        └─────────────────┘
               ▲
┌─────────────┐│
│   PRISMA    │┘
│   VERBAL    │ (futuro)
└─────────────┘
```

**Agentes core compartilhados:**
- Orquestrador: facilitador conversacional
- Estruturador: organiza ideias e refina questões
- Metodologista: valida rigor científico
- Writer (futuro): compilação de texto — primeiro agente motivado por Ensaio
- Researcher (futuro): busca web de papers
- Curator (futuro): fichamento — base do Prisma Verbal

## 3. Fluxo Assíncrono

**Diferencial central do produto em relação ao Revelar.**

O processo de produção de um artigo pode durar semanas. Pesquisador não precisa estar presente o tempo todo — sistema trabalha entre sessões.

**Fluxo esperado:**
1. Pesquisador chega ao sistema e vê pendências (perguntas abertas, sugestões dos agentes)
2. Responde ao que lhe é apresentado; fornece novas informações do experimento
3. Sistema avança em background: estrutura trechos, identifica lacunas, sugere evidências a coletar
4. Na próxima sessão, novas atualizações aguardam — rascunhos evoluídos, perguntas refinadas
5. Ciclo se repete até o artigo amadurecer

**Contraste com Revelar:**
- **Revelar:** Sessão síncrona, clareza emerge na conversa
- **Ensaio:** Sessões múltiplas ao longo de semanas, artigo emerge entre sessões

**Implicação arquitetural:** Sistema precisa manter estado persistente do artigo em construção, pendências abertas e decisões já tomadas.

## 4. Modo de Escrita Híbrido

Sistema e pesquisador **co-produzem o artigo progressivamente**. Não há separação rígida entre fase de conversa e fase de escrita.

**Como funciona:**
- Sistema escreve rascunhos de partes técnicas (metodologia, estrutura de resultados) à medida que informações chegam
- Não espera acumular tudo para escrever no final
- Pesquisador escreve a narrativa (motivação, interpretação, discussão) e revisa rascunhos do sistema
- Ao final, sistema gera primeira versão completa para revisão e publicação

**Divisão de responsabilidades:**
- **Sistema (via Writer):** Metodologia, estrutura de resultados, formatação, referências, consistência
- **Pesquisador:** Narrativa, contextualização, interpretação, decisões editoriais finais

**Benefício:** Pesquisador nunca enfrenta página em branco — sempre há rascunho parcial para editar.

## 5. Calibração Institucional (Visão Futura)

Organização possui artigos de referência e pesquisadores experientes. Práticas consolidadas de escrita técnica existem, mas estão distribuídas informalmente entre indivíduos.

**Visão futura:** Sistema aprende com artigos já publicados e práticas consolidadas da instituição — tornando as boas práticas um ativo compartilhado entre pesquisadores.

**O que a calibração institucional traz:**
- Estilo e tom condizentes com publicações anteriores da ICT
- Estruturas de artigo recorrentes na instituição
- Padrões de rigor e profundidade esperados
- Referências recorrentes já conhecidas

**Não previsto para POC.** Entrará em iterações posteriores, após validação do fluxo básico.

## 6. Casos de Uso Principais

- **UC1 (dominante): Artigo Técnico Completo** – Desenvolvo PoC que valida hipótese → quero registrar como artigo técnico completo (metodologia, resultados, discussão, referências).
- **UC2: One-pager para Divulgação** – Faço experimento rápido → quero one-pager para divulgação interna ou externa (resumo executivo com contexto, resultados e próximos passos).

## 7. Escopo do POC

POC foca em validar o fluxo básico ponta a ponta:

**Incluído:**
- Conversa sobre o experimento (Orquestrador + Estruturador + Metodologista)
- Estruturação do artigo (identificação de lacunas, perguntas provocativas)
- Writer gera primeira versão do artigo

**Fora do escopo do POC:**
- ❌ Pesquisa web de papers (Researcher — iteração futura)
- ❌ Calibração com artigos de referência da instituição (iteração futura)
- ❌ Fichamento automatizado de literatura (Curator/Prisma Verbal — iteração futura)

**Objetivo do POC:** Validar que o fluxo assíncrono + modo híbrido de escrita efetivamente transforma experimento em artigo, antes de investir em recursos avançados.

> **Nota:** Para refinamento dos épicos, ver `products/ensaio/ROADMAP.md`.

## 8. Estrutura do Artigo Emerge da Conversa

Ensaio **não mantém campo `article_type`** nem enum fixo de tipos de artigo. Estruturas (Introdução, Metodologia, Resultados, Discussão, one-pager...) emergem do que foi conversado; o Writer decide seções em tempo de escrita com base no contexto.

- **Sem schema:** não há classificação prévia de "artigo empírico vs one-pager vs ...".
- **Base de conhecimento no prompt do Writer:** estruturas comuns de artigo técnico-científico vivem no prompt, não em código do Ensaio.
- **Consequência:** pesquisador não precisa declarar o tipo de artigo. O sistema descobre a estrutura pelo conteúdo do experimento e pela conversa.

Decisão arquitetural registrada em `core/docs/architecture/agents/writer.md`.

## 9. Entidade "Pendência"

Item que permanece aberto entre sessões (pergunta sem resposta, evidência a coletar, rascunho esperando revisão, sugestão de agente aguardando decisão do pesquisador).

- **Nasce no Ensaio.** É o que viabiliza o fluxo assíncrono descrito na seção 3 — cada sessão abre, trabalha e fecha pendências.
- **Status: entidade em incubação.** Vive no Ensaio por enquanto; será promovida ao core quando o segundo produto precisar dela (provavelmente Produtor Científico, que herda a natureza multi-sessão).
- **Critério de promoção:** quando outro produto do super-sistema modelar algo equivalente, extrair Pendência para `core/docs/architecture/data-models/`.

Registro no core: `core/docs/architecture/data-models/ontology.md` (seção "Entidades em Incubação").

## 10. Stack da Interface

Interface do Ensaio é explicitamente **descartável na POC** e **migrável no Protótipo**. Isso é viabilizado mantendo toda a lógica de domínio no core, com a UI apenas consumindo.

**POC:** Streamlit como atalho. Sem investimento em UI, sem preocupação com design. Serve para validar o fluxo assíncrono e o modo híbrido de escrita (ver seções 3 e 4).

**Protótipo:** migração de stack é **frente de trabalho explícita** do refinamento do Protótipo. A stack definitiva (web app dedicada, IDE plugin, desktop, etc.) é decisão desse refinamento, não desta visão.

**Princípio de viabilização:**
- Lógica de domínio (estado do artigo, pendências, decisões dos agentes) vive toda no core.
- UI do Ensaio é **burra** — só renderiza e chama a API do core.
- Trocar stack = trocar camada de apresentação, sem tocar em regra de negócio.

Definições de POC / Protótipo / MVP neste projeto: ver `docs/process/refinement/planning_guidelines.md`.

## Referências

- `core/docs/vision/system_philosophy.md` - Filosofia universal
- `core/docs/architecture/vision/super_system.md` - Arquitetura do super-sistema
- `products/revelar/docs/vision.md` - Produto paralelo (entrada conversacional)
- `products/prisma-verbal/docs/vision.md` - Produto futuro (fichamento de literatura)
- `products/produtor-cientifico/docs/vision.md` - Produto futuro (compartilha Writer)
