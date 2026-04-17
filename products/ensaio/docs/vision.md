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

Ensaio é **produto próprio, com app próprio**. Não é modo, página ou extensão do Revelar: roda como aplicação separada, com sua própria interface, seu próprio estado e sua própria jornada. O que compartilha com os outros produtos do super-sistema são **os agentes do core**, não a UI.

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

**Fluxo esperado (estado-alvo):**
1. Pesquisador chega ao sistema e vê pendências (perguntas abertas, sugestões dos agentes)
2. Responde ao que lhe é apresentado; fornece novas informações do experimento
3. Sistema avança em background: estrutura trechos, identifica lacunas, sugere evidências a coletar
4. Na próxima sessão, novas atualizações aguardam — rascunhos evoluídos, perguntas refinadas
5. Ciclo se repete até o artigo amadurecer

**Contraste com Revelar:**
- **Revelar:** Sessão síncrona, clareza emerge na conversa
- **Ensaio:** Sessões múltiplas ao longo de semanas, artigo emerge entre sessões

**Quando esse fluxo aparece:**
- **POC:** ainda não existe (POC roda em sessão única e descartável).
- **Protótipo:** é onde o fluxo assíncrono nasce de verdade — persistência, pendências e rascunhos acumulados entre sessões.
- **MVP:** o fluxo já está maduro para outros pesquisadores usarem sem tutoria do desenvolvedor.

## 4. Modo de Escrita Híbrido

Sistema e pesquisador **co-produzem o artigo progressivamente**. Não há separação rígida entre fase de conversa e fase de escrita.

**Como funciona (estado-alvo):**
- Sistema escreve rascunhos de partes técnicas (metodologia, estrutura de resultados) à medida que informações chegam
- Não espera acumular tudo para escrever no final
- Pesquisador escreve a narrativa (motivação, interpretação, discussão) e revisa rascunhos do sistema
- Ao final, sistema gera primeira versão completa para revisão e publicação

**Divisão de responsabilidades:**
- **Sistema (via Writer):** Metodologia, estrutura de resultados, formatação, referências, consistência
- **Pesquisador:** Narrativa, contextualização, interpretação, decisões editoriais finais

**Benefício:** Pesquisador nunca enfrenta página em branco — sempre há rascunho parcial para editar.

**Quando esse modo aparece:**
- **POC:** não se aplica. Writer gera o artigo inteiro em uma passada, ao final da conversa.
- **Protótipo:** rascunho evolui por seção, acompanhando a conversa.
- **MVP:** o modo híbrido é a forma padrão de uso.

## 5. Estrutura do Artigo Emerge da Conversa

Ensaio **não mantém campo `article_type`** nem enum fixo de tipos de artigo (empírico, revisão, teórico, estudo de caso, meta-análise, metodológico...). A estrutura emerge do que foi conversado; o Writer decide seções em tempo de escrita com base no contexto.

- **Sem classificação prévia:** pesquisador não precisa declarar o tipo de artigo antes de começar.
- **Base de conhecimento no prompt do Writer:** o sistema tem conhecimento sobre estruturas comuns de artigo técnico-científico, mas **não impõe** — sugere e adapta com base na conversa.
- **Sem schema de seções:** Introdução, Metodologia, Resultados, Discussão, one-pager... são resultados, não entradas. O Writer combina conforme o conteúdo pedir.
- **Consequência:** o mesmo sistema serve artigo completo, one-pager ou variações híbridas sem código específico por formato.

Decisão arquitetural registrada em `core/docs/architecture/agents/writer.md`.

## 6. Pendências como Entidade Central

Pendência = item que permanece aberto entre sessões: pergunta sem resposta, evidência a coletar, rascunho esperando revisão, sugestão de agente aguardando decisão do pesquisador.

- **Viabiliza o fluxo assíncrono (seção 3):** cada sessão abre, trabalha e fecha pendências; é o estado que atravessa o tempo entre sessões.
- **Entidade central no Protótipo e MVP:** é onde o pesquisador para a sessão, é onde o sistema retoma na próxima, é a superfície principal da tela inicial.
- **Não existe na POC:** POC roda em sessão única, sem persistência — não há entre-sessões onde pendência faria sentido.
- **Status: em incubação no Ensaio.** Vive no produto por enquanto; será promovida ao core quando o segundo produto do super-sistema precisar dela (provavelmente Produtor Científico, que herda a natureza multi-sessão).

Registro no core: `core/docs/architecture/data-models/ontology.md` (seção "Entidades em Incubação").

## 7. Stack da Interface

Ensaio tem **app próprio** (ponto já estabelecido em §2). A decisão sobre *qual* stack usar é explicitamente faseada:

**POC:** Streamlit como **atalho descartável**. Sem investimento em UI, sem preocupação com design. Serve para validar conversa + geração de artigo antes de qualquer decisão de stack.

**Protótipo:** migração de stack é **frente de trabalho explícita** do refinamento do Protótipo. Stack definitiva (web app dedicada, IDE plugin, desktop, etc.) é decisão desse refinamento — não desta visão.

**MVP:** consolida a stack escolhida no Protótipo, com refinamentos necessários para uso por outros pesquisadores sem o desenvolvedor do lado.

**Princípio de viabilização (vale em todos os estágios):**
- Lógica de domínio (estado do artigo, pendências, decisões dos agentes) vive toda no core.
- UI do Ensaio é **burra** — só renderiza e chama a API do core.
- Trocar stack = trocar camada de apresentação, sem tocar em regra de negócio.

Definições operacionais de POC / Protótipo / MVP neste projeto: ver `docs/process/refinement/planning_guidelines.md`.

## 8. Casos de Uso Principais

- **UC1 (dominante): Artigo Técnico Completo** – Desenvolvo PoC que valida hipótese → quero registrar como artigo técnico completo (metodologia, resultados, discussão, referências).
- **UC2: One-pager para Divulgação** – Faço experimento rápido → quero one-pager para divulgação interna ou externa (resumo executivo com contexto, resultados e próximos passos).

Os dois casos de uso são servidos pelo mesmo sistema — a diferença está no que emerge da conversa e no que o Writer escolhe compor (ver §5), não em modos ou configurações pré-declaradas.

## 9. Escopo POC

**Objetivo:** provar que a ideia faz sentido — conversa sobre experimento → markdown.

**Incluído:**
- Conversa sobre o experimento com Orquestrador + Estruturador do core, em postura conversacional **ativo-leve**: escutam, organizam o que foi dito e perguntam só quando algo está vago (sem Metodologista, sem provocação ativa sobre lacunas)
- **Geração sob demanda:** pesquisador pede "gerar artigo" quando quiser — mesmo cedo na conversa — e o Writer devolve o markdown completo em uma única passada
- **Refinamento minimalista por feedback no chat:** pesquisador pede ajustes em linguagem natural ("deixa mais conciso", "adiciona uma seção sobre X") e o Writer regera o artigo inteiro a partir da conversa acumulada + artigo anterior
- **Sessão única descartável (sem persistência):** estado da conversa e do artigo vive só na memória do navegador; recarregar a página recomeça do zero

**Fora do escopo do POC:**
- ❌ Upload de artefatos (notebook, README, CSV, imagens)
- ❌ Pendências entre sessões
- ❌ Rascunho progressivo por seção
- ❌ Metodologista provocando lacunas no Ensaio
- ❌ Pesquisa web de papers (Researcher)
- ❌ Calibração com artigos de referência da instituição
- ❌ Fichamento automatizado de literatura (Curator / Prisma Verbal)
- ❌ Integração com repositórios Git

**Critério de saída do POC:** a conversa + o markdown gerado convencem que vale investir em estabilidade e nas frentes do Protótipo.

> Critérios de aceite operacionais dessas decisões vivem no ROADMAP do Ensaio, épico E-POC-3 (ver `products/ensaio/ROADMAP.md`).

## 10. Escopo Protótipo

**Objetivo:** a ideia funciona e o próprio desenvolvedor usa de verdade no fluxo real dele.

**Adiciona ao POC:**
- Persistência do artigo entre sessões
- Rascunho progressivo por seção (modo de escrita híbrido real — §4)
- Pendências entre sessões como entidade central (§6)
- Metodologista aplicado ao Ensaio (provocação sobre lacunas, métricas, evidências)
- Migração de stack da interface (decidida no refinamento do Protótipo — §7)

**Ainda fora:**
- ❌ Upload de artefatos (continua no MVP)
- ❌ Calibração institucional (pós-MVP)
- ❌ Integração Git (pós-MVP)
- ❌ Researcher / Curator (iterações futuras)

**Critério de saída do Protótipo:** o desenvolvedor consegue transformar seus próprios experimentos em artigos sem depender de conhecimento interno do código.

## 11. Escopo MVP

**Objetivo:** outros pesquisadores (colegas próximos) usam sem o desenvolvedor do lado.

**Adiciona ao Protótipo:**
- Upload de artefatos do experimento: notebook, README, CSV, imagens de gráfico
- Experiência de refinamento *ongoing* madura (pendências, rascunhos e conversa em fluxo estável)
- Preparação mínima para uso por outros: onboarding básico, mensagens de erro claras, estado previsível

**Critério de saída do MVP:** colega próximo consegue usar o Ensaio sem tutorial ao vivo do desenvolvedor.

## 12. Melhorias Pós-MVP

Frentes que dependem de validação do MVP antes de entrar em roadmap:

- **Calibração institucional:** sistema aprende com artigos publicados e práticas consolidadas da ICT — estilo, estruturas recorrentes, padrões de rigor, referências conhecidas. Torna boas práticas ativo compartilhado.
- **Integração com Git:** leitura direta do repositório do experimento (código, histórico de commits, arquivos) para alimentar a conversa e o Writer sem uploads manuais.
- **Researcher no Ensaio:** busca web de papers para fundamentar o artigo.
- **Curator / Prisma Verbal no Ensaio:** fichamento automatizado de literatura relevante.

Essas frentes entram em iterações posteriores, após validação do fluxo básico ponta a ponta com pesquisadores reais.

> **Nota:** Para refinamento dos épicos, ver `products/ensaio/ROADMAP.md`.

## Referências

- `core/docs/vision/system_philosophy.md` - Filosofia universal
- `core/docs/architecture/vision/super_system.md` - Arquitetura do super-sistema
- `core/docs/architecture/agents/writer.md` - Decisões arquiteturais do Writer
- `core/docs/architecture/data-models/ontology.md` - Entidades do core (inclui "Entidades em Incubação")
- `docs/process/refinement/planning_guidelines.md` - Definições de POC / Protótipo / MVP
- `products/revelar/docs/vision.md` - Produto paralelo (entrada conversacional)
- `products/prisma-verbal/docs/vision.md` - Produto futuro (fichamento de literatura)
- `products/produtor-cientifico/docs/vision.md` - Produto futuro (compartilha Writer)
