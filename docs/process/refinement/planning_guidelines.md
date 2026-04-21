# Planning Guidelines

> **📌 Localização:** `docs/process/refinement/planning_guidelines.md`.
> **📌 Público:** Claude Web (refinamento) e desenvolvedores (governança).
> **📌 Envio em sessão de refinamento:** junto com `docs/CONSTITUTION.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md` e o ROADMAP do produto em foco.
> **📌 Checklist da segunda passada:** `docs/process/refinement/autonomous_readiness.md`.

## Filosofia de Desenvolvimento

Este projeto segue mentalidade **incremental e pragmática**:

### Progressão por Estágios

Definições trabalhadas para este projeto, no eixo **"quem usa"** (complementa o eixo técnico):

- **POC (Proof of Concept):** prova que a ideia faz sentido. Pode ser tosco, rodar só no ambiente do desenvolvedor, ter atalhos explícitos. Critério de saída: a ideia se sustenta o suficiente para justificar investimento em estabilidade.
- **Protótipo:** a ideia funciona e o **próprio desenvolvedor usa de verdade** — no fluxo real dele, não só em cenário de teste. Critério de saída: o desenvolvedor consegue usar sem se apoiar em conhecimento interno do código.
- **MVP:** **outros** (colegas próximos) usam **sem o desenvolvedor do lado**. Critério de saída: valor validado fora do autor.
- **Melhorias:** Expansão gradual baseada em feedback de uso real.

**Implicação prática:** decisões de stack, UX e robustez devem ser proporcionais ao estágio. POC tolera Streamlit e gambiarras; Protótipo exige fluxo navegável pelo próprio dev; MVP exige que outro ser humano consiga usar sem tutorial ao vivo.

## Processo de Refinamento com Claude Web

Este projeto usa Claude Web como consultor estratégico para refinar épicos e discutir comportamentos. O processo é documentado aqui para garantir consistência.

### Input Esperado
Você fornece ao Claude Web:
- Comportamento desejado OU problema existente
- Contexto: épico novo, ajuste de funcionalidade, ou discussão arquitetural
- 5 arquivos essenciais: docs/CONSTITUTION.md, docs/ROADMAP.md, products/revelar/ROADMAP.md, docs/ARCHITECTURE.md, planning_guidelines (este)

### Claude Web Deve
1. **Análise Contextual:** Consultar vision.md, docs/ROADMAP.md ou products/revelar/ROADMAP.md (épicos anteriores), specs técnicas via mapa
2. **Clarificação:** Fazer perguntas específicas, validar entendimento, apontar trade-offs
3. **Recomendação:** Oferecer opções + recomendação balizada por vision.md e guidelines
4. **Gerar Prompts:** Múltiplos prompts (1 por arquivo), instruções enxutas, manter padrões
5. **Validação:** Confirmar que prompts fazem sentido

### Output Gerado
Claude Web gera prompts separados para Cursor executar:
- PROMPT 1: docs/ROADMAP.md ou products/revelar/ROADMAP.md (dependendo do épico)
- PROMPT 2: docs/[spec técnica]
- PROMPT 3: docs/ARCHITECTURE.md (se necessário)

Cada prompt é enxuto mas claro, deixando Cursor pensar também.

### Otimização do Workflow: Usando Cursor para Análises

**Ao invés de enviar todos os arquivos de contexto ao Claude Web**, você pode solicitar ao Cursor para fazer análises do código e gerar insights que facilitam o refinamento:

**Estratégia:**
- **Antes de ir ao Claude Web:** Use o Cursor para escanear o repositório e fazer análises específicas
- **Envie ao Claude Web:** Os insights gerados pelo Cursor + os 4 arquivos essenciais (CONSTITUTION, ROADMAP, ARCHITECTURE, planning_guidelines)

**Exemplos de prompts para o Cursor:**
- "Analise a estrutura atual do sistema de persistência e identifique pontos de extensão para suportar pausar/retomar conversas"
- "Escanee o código do orquestrador e identifique como ele gerencia estado atualmente"
- "Analise os padrões de implementação dos agentes existentes para manter consistência no novo épico"
- "Revise a arquitetura de eventos e sugira como integrar nova funcionalidade X"

**Benefícios:**
- ✅ Reduz o volume de arquivos enviados ao Claude Web
- ✅ Cursor tem acesso completo ao código e pode fazer análises profundas
- ✅ Insights técnicos específicos facilitam decisões no refinamento
- ✅ Claude Web recebe contexto já processado e focado

**Fluxo recomendado:**
1. Cursor faz análise técnica do código relevante
2. Claude Web recebe insights + documentos essenciais para refinamento estratégico
3. Claude Web gera prompts para Cursor implementar

### Exemplo de Refinamento Bem Feito

**Cenário:** Refinar Épico 10 - Persistência

**Input do usuário:**
"Vamos refinar Épico 10. Quero pausar/retomar conversas com contexto preservado."

**Claude Web:**
1. Consulta vision.md (entidade Tópico), ROADMAP (padrão de épicos anteriores)
2. Pergunta: "Persistência local (SqliteSaver) ou remota (PostgreSQL)? Trade-off: simplicidade vs escalabilidade"
3. Recomenda: "Começar com SqliteSaver (POC), migrar pra PostgreSQL (MVP se necessário)"
4. Propõe funcionalidades 10.1-10.5 com critérios de aceite claros
5. Gera prompts pra Cursor atualizar ROADMAP + criar `docs/architecture/persistence.md` (arquivo será criado durante refinamento, não existe ainda)

> **📌 Nota:** Este é um exemplo hipotético de refinamento. O arquivo `docs/architecture/persistence.md` será criado quando o Épico 10 for refinado.

**Resultado:** Épico em `📋 Critérios definidos`, specs criadas, pronto para implementação via fluxo manual. Antes do dispatch autônomo, rodar a segunda passada (`autonomous_readiness.md`) para promover o épico a `✅ Detalhes definidos`.

---

### Princípios de Planejamento
1. **Refinar apenas o que está claro**
   - Épicos só são refinados quando se tornam prioritários
   - Refinamento requer compreensão técnica do estado atual do sistema
   - Funcionalidades detalhadas só após sessão de refinamento dedicada

2. **Fazer > Planejar demais**
   - Implementar POC mínimo e validar antes de expandir
   - Aprender com código real, não especulação
   - Ajustar plano baseado em implementação, não o contrário

3. **Validar > Assumir**
   - Cada estágio (POC/Protótipo/MVP) deve ser validado antes do próximo
   - Validação = rodar sistema com cenários reais, não apenas testes passando
   - Feedback de validação informa refinamento do próximo estágio

4. **Iterar > Acertar de primeira**
   - Versão 1.0 de qualquer funcionalidade será imperfeita
   - Sistema evolui através de iterações sucessivas
   - Aceitamos limitações conhecidas em versões iniciais

5. **Funcionalidade mínima > Feature completa**
   - Entregar valor incremental cedo e frequentemente
   - Preferir funcionalidade simples que funciona a feature complexa incompleta
   - Expandir apenas quando mínimo está sólido

### Gestão do Backlog
- **Backlog = Desejo, não compromisso**
- Ideias vão para backlog sem serem épicos formais
- Épicos em `⏳ Planejado` aguardam priorização + clareza técnica
- Remover do backlog é tão válido quanto adicionar (não há apego)

### Três Estados de Refinamento

Um épico percorre três estados no ROADMAP. Cada estado marca um nível de maturidade do refinamento e habilita um fluxo de execução específico.

**`⏳ Planejado`** — só objetivo definido.
Estado inicial de qualquer épico promovido a partir do backlog. Captura intenção e valor de negócio, sem funcionalidades detalhadas. Não é executável por nenhum fluxo.

**`📋 Critérios definidos`** — funcionalidades com critérios de aceite.
Produto da primeira passada de refinamento. Épico tem funcionalidades delimitadas, critérios de aceite observáveis, trade-offs discutidos. **Suficiente para o fluxo manual via Cursor**, onde o desenvolvedor resolve ambiguidades de execução à medida que aparecem.

**`✅ Detalhes definidos`** — passou pelo checklist de `autonomous_readiness.md`.
Produto da segunda passada de refinamento. Além dos critérios de aceite, tem contratos de dados explicitados, arquivos-alvo listados, mecanismo de integração descrito, acoplamentos verificados e escopo de testes definido. **Pré-requisito para o fluxo autônomo via Claude Code Web**, onde o agente não deve tomar decisões arquiteturais em tempo de implementação.

### Duas Passadas de Refinamento

A transição `⏳ Planejado → 📋 Critérios definidos` é a **primeira passada**. Responde "isso faz sentido e gera valor?" — produz funcionalidades e critérios.

A transição `📋 Critérios definidos → ✅ Detalhes definidos` é a **segunda passada**. Responde "um agente sem contexto do problema consegue executar isto sem inventar?" — produz decisões de execução. Guiada pelo checklist em `docs/process/refinement/autonomous_readiness.md`.

### Quando Aplicar Cada Passada

**Primeira passada** — quando o épico se torna prioritário (próximo na fila), dependências técnicas foram implementadas e validadas, e há clareza sobre valor e viabilidade.

**Segunda passada** — sob demanda, para o épico específico que vai ser disparado no fluxo autônomo. Aplicar preventivamente em todos os épicos é desperdício: o trabalho perde-se se o épico for repriorizado antes da implementação.

---

## Princípio Fundamental

**Roadmap = FUTURO** (próximos passos + ideias)
**Documentação Técnica = PRESENTE** (estado atual do sistema)

---

## Categorias de Épicos

### `✅ Detalhes definidos` (Prontos para Fluxo Autônomo)
Épicos que passaram pela segunda passada e estão aptos a dispatch autônomo via Claude Code Web.

### `📋 Critérios definidos` (Prontos para Fluxo Manual)
Épicos com funcionalidades e critérios de aceite, prontos para implementação manual via Cursor. Precisam da segunda passada antes do dispatch autônomo.

### `⏳ Planejado` (Requer Primeira Passada)
Épicos com objetivo, ainda sem funcionalidades delimitadas. Aguardam sessão de refinamento.

**Claude Code só implementa funcionalidades de épicos em `📋 Critérios definidos` (fluxo manual) ou `✅ Detalhes definidos` (fluxo autônomo).**

---

## Estrutura do Roadmap

### 💡 IDEIAS FUTURAS
Ideias abstratas que ainda não viraram épicos. Aguardando maturação.

### 📍 PRÓXIMOS PASSOS

**Épicos percorrem três estados:**

- **`⏳ Planejado`** — apenas objetivo definido. Aguardando primeira passada de refinamento.
- **`📋 Critérios definidos`** — funcionalidades e critérios de aceite. Pronto para fluxo manual via Cursor.
- **`✅ Detalhes definidos`** — contratos, arquivos-alvo e integração explicitados. Pronto para fluxo autônomo via Claude Code Web.

**Fluxo:**
```
Ideia → Épico (⏳ Planejado)
      → 1ª passada de refinamento
      → Épico (📋 Critérios definidos) — executável em fluxo manual
      → 2ª passada de refinamento (autonomous_readiness)
      → Épico (✅ Detalhes definidos) — executável em fluxo autônomo
      → Implementação
```

### ✅ CONCLUÍDO RECENTEMENTE
Resumo enxuto (1-2 linhas) dos últimos épicos. Remove manualmente quando acumular.

---

## Template: Épico em Três Estados

### Estado `⏳ Planejado` — ao promover ideia para épico:

```markdown
## ÉPICO X: Nome Descritivo
**Status:** ⏳ Planejado

**Objetivo:** [O que queremos alcançar com este épico. Foco no valor de negócio.]
```

### Estado `📋 Critérios definidos` — após primeira passada de refinamento:

```markdown
## ÉPICO X: Nome Descritivo
**Status:** 📋 Critérios definidos

**Objetivo:** [O que queremos alcançar com este épico. Foco no valor de negócio.]

### Funcionalidades:
#### X.1 Nome da Funcionalidade
- **Descrição:** [1-2 frases]
- **Critérios de Aceite:**
  - Deve [comportamento observável]
  - Deve [comportamento observável]

#### X.2 Nome da Funcionalidade
[...]
```

### Estado `✅ Detalhes definidos` — após segunda passada de refinamento:

Todo o conteúdo do estado anterior, acrescido de uma seção de detalhes de execução para cada funcionalidade (resultado do checklist em `autonomous_readiness.md`):

```markdown
## ÉPICO X: Nome Descritivo
**Status:** ✅ Detalhes definidos

**Objetivo:** [...]

### Funcionalidades:
#### X.1 Nome da Funcionalidade
- **Descrição:** [...]
- **Critérios de Aceite:** [...]
- **Detalhes de execução:**
  - **Arquivos a criar:** `<caminho/completo>`
  - **Arquivos a modificar:** `<caminho/completo>`
  - **Contratos/Shapes:** [estados compartilhados, inputs/outputs relevantes]
  - **Integração:** [onde o código entra, como é carregado, como é invocado]
  - **Template de referência:** [agente/componente análogo existente]
  - **Acoplamentos verificados:** [imports, dependências; refatorações prévias se houver]
  - **Dependências de ordem:** [funcionalidades/épicos que precisam vir antes]
  - **Escopo de teste:** [unit / integration / validação manual]
```

**Quando fazer cada passada?** Ver seção "Três Estados de Refinamento" acima.

---

## Exemplo de Épico

```markdown
## ÉPICO 3: Autenticação Google

**Objetivo:** Simplificar acesso ao sistema substituindo email/senha por autenticação Google, melhorando segurança e experiência do usuário.

### Funcionalidades:
#### 3.1 Implementação de Google OAuth
#### 3.2 Controle de Acesso via Gestores Cadastrados
#### 3.3 Preparação da Estrutura de Dados
```

---

## Critérios de Qualidade para Épicos

✅ Objetivo claro: Foca no valor de negócio, não em implementação técnica
✅ Coeso: Funcionalidades relacionadas que fazem sentido juntas
✅ Tamanho adequado: 2-5 funcionalidades (nem muito pequeno, nem gigante)
✅ Incremental: Entrega valor mesmo se parar no meio

---

## Template: Funcionalidade

```markdown
#### X.Y Nome Específico da Funcionalidade

- **Descrição:** [O que é esta funcionalidade em 1-2 frases]
- **Critérios de Aceite:**
  - Deve [comportamento esperado específico e testável]
  - Deve [comportamento esperado específico e testável]
  - Não deve [comportamento indesejado se relevante]
```

---

## Exemplo de Funcionalidade

```markdown
#### 3.1 Implementação de Google OAuth

- **Descrição:** Configurar autenticação via Google OAuth no backend e frontend
- **Critérios de Aceite:**
  - Página de login deve ter apenas botão "Entrar com Google"
  - Após autenticação Google, verificar se email está na lista autorizada
  - Se email autorizado: criar/atualizar usuário e gerar JWT
  - Se email não autorizado: exibir mensagem de acesso negado
```

---

## Critérios de Qualidade para Funcionalidades

✅ Testável: Critérios de aceite observáveis e validáveis
✅ Incremental: Entrega valor sozinha
✅ Específica: Escopo claro
✅ Valor claro: Benefício concreto
✅ Única: Não se sobrepõe a outras funcionalidades

---

## Manutenção do Roadmap

Quando épico/funcionalidade for concluído:
1. Marque ✅ no título do épico
2. Resuma em 1-2 linhas o que foi entregue
3. Remova detalhes (objetivo, critérios, sub-funcionalidades)
4. Mova para "✅ Concluído Recentemente"

Exemplo:

```markdown
## ✅ ÉPICO 2: Padronização da Interface de Resumos
Sistema com layout consistente entre páginas de resumo, exibindo dados completos do projeto via API.
```

---

## Tarefas

Uma tarefa é um conjunto incremental de atividades relacionadas que:
- ✅ É curta e focada
- ✅ Agrega valor imediatamente
- ✅ É testável
- ✅ Pode ser comitada independentemente
- ✅ Permite rollback fácil

### Mentalidade Incremental
Progresso contínuo: **POC → Protótipo → MVP → Melhorias**

Processo: Fazer → Validar → Commit → Iterar

---

## Workflow do Claude Code

### Antes de Começar
1. Verifique dúvidas ou decisões em aberto
2. Confirme o estado do épico no ROADMAP:
   - **Fluxo manual via Cursor:** mínimo `📋 Critérios definidos`
   - **Fluxo autônomo via Claude Code Web:** exige `✅ Detalhes definidos` (checklist `autonomous_readiness.md` aplicado)
3. Alinhe o escopo com o usuário

### Durante Implementação
- Trabalhe em funcionalidades (não épicos inteiros)
- Commits incrementais
- PR/merge só ao final da funcionalidade

### Comunicação
- Pergunte quando algo não estiver claro
- Evite assumir decisões de arquitetura

---

## Quando Parar e Perguntar
- Falta de informação
- Decisões arquiteturais abertas
- Múltiplas abordagens possíveis
- Épico em `⏳ Planejado` (exige primeira passada de refinamento)
- Fluxo autônomo disparado sobre épico em `📋 Critérios definidos` (exige segunda passada via `autonomous_readiness.md`)

---

## Git Workflow
- Branches flexíveis no início
- Commits frequentes e descritivos
- Uma funcionalidade por PR
- Conflitos resolvidos com apoio do usuário

---

## Estratégia de Testes
- TDD pragmático (lógica crítica primeiro)
- Reavalie a estratégia conforme o projeto evolui
- **Detalhes técnicos**: `docs/testing/README.md` (pirâmide de testes, mocks vs API real, estrutura)

---

## Retrospectiva de Sessão
- Documente bloqueios, perdas de eficiência e melhorias sugeridas
- Sempre alinhe antes de atualizar documentação compartilhada

