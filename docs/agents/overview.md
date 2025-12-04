# Sistema Multi-Agente para Produção de Artigos Científicos

> Visão de longo prazo: descreve todos os agentes planejados para a plataforma colaborativa com IA.
> **Status da POC:** apenas Orquestrador e Metodologista estão em implementação inicial.

## Arquitetura Geral

**Fluxo:** Semi-linear com loops controlados  
**Comunicação:** Estado compartilhado via LangGraph  
**Resolução de conflitos:** Voto de Minerva (usuário decide)

---

## 1. ORQUESTRADOR

### Responsabilidades
- **Facilitar conversação** entre usuário e sistema (não apenas classificar)
- Gerenciar estado da conversa e progresso do artigo
- **Negociar caminhos** com o usuário (apresentar opções, não decidir sozinho)
- Detectar quando há conflito entre agentes
- Apresentar conflitos para o usuário resolver
- Determinar quando o artigo está completo
- **Adaptar fluxo** conforme decisões do usuário
- **Detectar proposições não examinadas** no discurso do usuário
- **Extrair claim** do que o usuário está dizendo
- **Atualizar context** (domínio, tecnologia, população) do modelo cognitivo
- **Provocar reflexão** sobre aspectos não explorados: "Você assumiu X. Quer examinar?"
- **Identificar open_questions** iniciais que precisam ser respondidas
- **Observador integrado (POC)**: Atualiza CognitiveModel a cada turno

### PODE fazer
- **Perguntar ao usuário** antes de chamar agentes
- **Apresentar opções** claras e contextuais
- Chamar qualquer agente (após negociação)
- Solicitar re-trabalho de qualquer etapa
- Pedir esclarecimentos ao usuário
- Salvar checkpoints do progresso
- **Adaptar fluxo** quando usuário muda de direção
- Encerrar processo (com aprovação do usuário)

### NÃO PODE fazer
- **Decidir sozinho** qual agente chamar (deve negociar)
- **Classificar automaticamente** sem explorar intenção
- Avaliar conteúdo científico
- Escrever ou editar texto
- Tomar decisões sobre metodologia
- Ignorar feedback de agentes especialistas
- **Forçar fluxo rígido** (deve ser adaptativo)

### Input esperado
- Do usuário: hipótese inicial, observação, constatação, **decisões sobre caminhos**
- De agentes: outputs validados ou rejeitados

### Output esperado
- **Perguntas e opções** para o usuário
- Comandos para próximo agente (após negociação)
- Resumos de progresso para usuário
- Apresentação de conflitos com argumentos

### Critérios de qualidade
- **Sempre pergunta antes de agir**
- **Opções claras e contextuais** apresentadas
- Fluxo lógico mantido (mas adaptativo)
- Nenhum agente chamado fora de contexto
- Conflitos sempre escalados para usuário
- Estado sempre consistente
- **Mudanças de direção aceitas sem questionar**

### Mudança de Papel (13/11/2025)

**ANTES (classificador):**
- Orquestrador classificava input automaticamente
- Router decidia próximo agente sem consultar usuário
- Fluxo rígido e determinístico

**AGORA (facilitador):**
- Orquestrador explora intenção com perguntas abertas
- Apresenta opções e negocia caminhos
- Fluxo adaptativo e conversacional
- Usuário mantém controle sobre decisões

**Exemplo de mudança:**
```
❌ ANTES: "Detectei que seu input é vago. Chamando Estruturador automaticamente."
✅ AGORA: "Interessante! Você quer testar uma hipótese ou verificar literatura?"
```

---

## 2. METODOLOGISTA

### Responsabilidades
- Avaliar rigor científico da hipótese/constatação
- Validar se a lógica proposta é sólida
- Identificar falhas metodológicas
- Sugerir melhorias no método
- Validar se as conclusões são suportadas pelos argumentos
- **Validar se fundamentos têm solidez suficiente** (têm base?)
- **Identificar fundamentos com baixa solidez** (precisam pesquisar?)
- **Apontar contradictions** na lógica
- **Sugerir evidências necessárias**: "Fundamento X precisa de evidência" (adiciona open_question)

### PODE fazer
- Rejeitar hipótese com justificativa
- Pedir mais informações ao usuário (via Orquestrador)
- Sugerir ajustes na formulação
- Apontar vieses metodológicos
- Validar coerência lógica

### NÃO PODE fazer
- Criar o outline do artigo
- Fazer pesquisa bibliográfica
- Escrever conteúdo
- Estruturar argumentação (isso é do Estruturador)

### Input esperado
- Hipótese/constatação/observação do usuário
- Contexto da área de conhecimento
- (Opcional) Pesquisas prévias do Pesquisador

### Output esperado
**Se aprovado:**
- Validação com justificativa
- Pontos fortes da hipótese
- Recomendações metodológicas

**Se rejeitado:**
- Falhas específicas identificadas
- Sugestões concretas de correção
- Alternativas metodológicas

### Critérios de qualidade
- Justificativas baseadas em método científico
- Apontamentos específicos, não genéricos
- Sugestões acionáveis
- Sem viés pessoal, apenas rigor metodológico

---

## 3. ESTRUTURADOR

### Responsabilidades
- Criar outline completo do artigo
- Definir seções e subseções
- Planejar fluxo argumentativo
- Determinar o que precisa ser pesquisado
- Organizar lógica de apresentação
- **Organizar fundamentos de forma lógica**
- **Tornar explícito o que era implícito**
- **Dividir conceito em sub-conceitos**
- **Proativo quando**: Contexto claro, múltiplos conceitos desconexos
- **Pergunta quando**: Primeira interação, mudança de direção

### PODE fazer
- Criar estrutura de seções (Introdução, Metodologia, etc.)
- Definir ordem de argumentos
- Especificar o que cada seção deve conter
- Solicitar pesquisas específicas ao Pesquisador
- Ajustar estrutura baseado em feedback

### NÃO PODE fazer
- Validar metodologia científica
- Fazer a pesquisa bibliográfica
- Escrever o conteúdo
- Avaliar qualidade final

### Input esperado
- Hipótese validada pelo Metodologista
- Recomendações metodológicas
- (Opcional) Pesquisas já feitas

### Output esperado
- Outline estruturado com seções
- Para cada seção: objetivo, conteúdo esperado
- Lista de gaps que precisam de pesquisa
- Fluxo lógico da argumentação

### Critérios de qualidade
- Estrutura segue padrão de artigo científico
- Fluxo argumentativo coerente
- Cada seção tem propósito claro
- Gaps de conhecimento identificados

---

## 4. PESQUISADOR

### Responsabilidades
- Buscar papers acadêmicos relevantes
- Buscar informações complementares na web
- **Sintetizar** achados (não apenas listar)
- Validar se fontes são confiáveis
- Identificar consensos e divergências na literatura
- **Transformar open_questions em evidências**
- **Buscar evidências para fundamentos com baixa solidez**
- **Adicionar referências bibliográficas**

### PODE fazer
- Buscar em múltiplas fontes (Google Scholar, Semantic Scholar, web)
- Fazer múltiplas buscas iterativas
- Comparar fontes diferentes
- Sintetizar: "Autor X diz Y, isso suporta/contradiz hipótese porque Z"
- Indicar qualidade da fonte

### NÃO PODE fazer
- Decidir se a pesquisa é suficiente (quem decide: Estruturador ou Crítico)
- Interpretar achados fora do escopo da pergunta
- Criar argumentação própria
- Validar metodologia

### Input esperado
- Questão específica de pesquisa
- Contexto do artigo
- Palavras-chave sugeridas

### Output esperado
**Para cada busca:**
- Fonte (paper, site, etc.)
- Resumo do achado
- Relevância para hipótese (suporta/contradiz/neutro)
- Qualidade da fonte (alto/médio/baixo)
- Citação formatada

**Síntese final:**
- Principais achados consolidados
- Consensos identificados
- Divergências identificadas
- Gaps que ainda existem

### Critérios de qualidade
- Fontes primárias priorizadas
- Sintetização clara e objetiva
- Relevância demonstrada
- Múltiplas perspectivas quando relevante
- Citações corretas

---

## 5. ESCRITOR

### Responsabilidades
- Escrever o artigo seguindo o outline
- Usar o estilo de escrita do usuário
- Incorporar pesquisas do Pesquisador
- Formatar como artigo científico
- Manter coerência e fluidez

### PODE fazer
- Escrever todas as seções
- Adaptar tom mantendo rigor
- Reformular frases para melhor fluidez
- Adicionar transições entre seções
- Formatar citações e referências

### NÃO PODE fazer
- Mudar estrutura definida pelo Estruturador
- Adicionar argumentos não validados
- Inventar dados ou pesquisas
- Avaliar qualidade científica
- Questionar metodologia

### Input esperado
- Outline completo do Estruturador
- Pesquisas sintetizadas do Pesquisador
- Referência de estilo de escrita do usuário
- Validações do Metodologista

### Output esperado
- Artigo completo em formato científico
- Introdução, desenvolvimento, conclusão
- Citações formatadas corretamente
- Referências bibliográficas
- Texto fluido e coerente

### Critérios de qualidade
- Segue outline rigorosamente
- Estilo consistente com referência do usuário
- Todas as afirmações têm suporte (pesquisa ou lógica)
- Formatação acadêmica correta
- Zero contradições internas
- Transições suaves entre seções

---

## 6. CRÍTICO

### Responsabilidades
- Revisar artigo completo com olhar cético
- Identificar furos na argumentação
- Apontar contradições
- Detectar vieses não declarados
- Questionar se conclusões são suportadas
- Validar integridade científica

### PODE fazer
- Rejeitar artigo com justificativas específicas
- Questionar qualquer afirmação
- Solicitar mais pesquisas
- Pedir reescrita de seções
- Identificar o que está faltando
- Apontar exageros ou generalizações

### NÃO PODE fazer
- Reescrever o texto
- Fazer novas pesquisas
- Aprovar com ressalvas (só aprova ou rejeita)
- Mudar estrutura

### Input esperado
- Artigo completo do Escritor
- Outline original
- Pesquisas utilizadas
- Validações do Metodologista

### Output esperado
**Se aprovado:**
- Confirmação de aprovação
- Pontos fortes destacados
- (Opcional) Sugestões menores de polimento

**Se rejeitado:**
- Lista específica de problemas
- Qual seção tem problema
- O que está errado (contradição/furo/viés)
- Sugestão de correção
- Prioridade (crítico/importante/menor)

### Critérios de qualidade
- Críticas específicas, nunca genéricas
- Sempre com exemplo concreto
- Sugestões acionáveis
- Priorização clara
- Imparcialidade (sem preferências pessoais)

---

## Relação Agentes ↔ Modelo Cognitivo

O sistema multi-agente interage com um modelo cognitivo que representa o entendimento progressivo do que o usuário está construindo. Cada agente contribui de forma específica para atualizar e enriquecer este modelo.

### Orquestrador

O Orquestrador atua como observador integrado do modelo cognitivo, atualizando-o a cada turno da conversa:

- **Detecta proposições não examinadas**: Identifica o que o usuário assume mas não declara explicitamente
- **Extrai claim do que usuário está dizendo**: Captura a afirmação central de cada input
- **Atualiza context (domínio, tecnologia, população)**: Enriquece o contexto do modelo cognitivo com informações novas
- **Provoca reflexão**: Quando detecta lacunas, pergunta "Você assumiu X. Quer examinar?"
- **Identifica open_questions iniciais**: Mapeia questões que precisam ser respondidas para avançar
- **Observador integrado (POC)**: Atualiza CognitiveModel a cada turno automaticamente

**Futuro**: Pode virar agente separado se houver conflito de responsabilidades entre facilitar conversa e observar modelo cognitivo.

### Estruturador

O Estruturador organiza o conhecimento do modelo cognitivo de forma lógica:

- **Organiza fundamentos de forma lógica**: Estrutura os fundamentos em ordem coerente
- **Torna explícito o que era implícito**: Revela suposições que estavam ocultas
- **Divide conceito em sub-conceitos**: Quebra ideias complexas em componentes menores

**Comportamento adaptativo**:
- **Proativo quando**: Contexto claro, múltiplos conceitos desconexos que precisam organização
- **Pergunta quando**: Primeira interação, mudança de direção que requer esclarecimento

### Metodologista

O Metodologista valida a solidez dos fundamentos no modelo cognitivo:

- **Valida se fundamentos têm solidez suficiente (têm base?)**: Verifica se cada fundamento tem base sólida
- **Identifica fundamentos com baixa solidez (precisam pesquisar?)**: Detecta fundamentos que carecem de evidência
- **Aponta contradictions na lógica**: Encontra inconsistências entre fundamentos
- **Sugere evidências necessárias**: "Fundamento X precisa de evidência" (adiciona open_question ao modelo)

### Pesquisador (Futuro - Épico 13)

O Pesquisador transforma questões abertas em conhecimento sólido:

- **Transforma open_questions em evidências**: Responde questões pendentes com evidências
- **Busca evidências para fundamentos com baixa solidez**: Fortalece fundamentos identificados como frágeis pelo Metodologista
- **Adiciona referências bibliográficas**: Incorpora fontes acadêmicas ao modelo cognitivo

### Transições

As transições entre agentes são projetadas para serem:

- **Suaves e naturais**: O usuário não percebe a troca de agente
- **Transparentes nos bastidores**: Quem está falando só é visível nos bastidores (para debugging)
- **Sem interrupções**: Sem mensagens como "Chamando X..." → A conversa flui naturalmente
- **Contextuais**: Cada agente continua a conversa de forma natural, como em "Hmm, esse fundamento parece frágil..." (natural)

### Ações Baratas vs Caras

O sistema diferencia ações que podem ser proativas (baratas) daquelas que requerem permissão (caras):

**Ações Baratas (proativas)**:
- Estruturador organizar fundamentos
- Orquestrador detectar proposições não examinadas
- Metodologista apontar lacuna

**Ações Caras (pedir permissão)**:
- Pesquisador buscar papers
- Escritor gerar rascunho
- Análise profunda que consome muitos tokens

**Referências**: Ver `docs/vision/cognitive_model/core.md` para detalhes sobre a estrutura do modelo cognitivo.

---

## Fluxo e Estado Compartilhado

Ver fluxo técnico completo em `docs/orchestration/multi_agent_architecture/flows.md`.

Ver `MultiAgentState` em `docs/orchestration/multi_agent_architecture/state.md`.

---

## Pontos Críticos a Resolver na POC

1. Formato exato de prompt para cada agente
2. Schema de validação dos outputs
3. Handling de erros (o que fazer se agente "trava")
4. Referência de estilo do usuário (como capturar e usar)
5. Integração com APIs de busca (Google Scholar, Semantic Scholar)
6. Custo estimado por artigo (tokens)

---

## Princípios de Design

1. Separação de responsabilidades: cada agente tem função clara e limitada
2. Fail-safe: conflitos sempre sobem para usuário
3. Transparência: todo output é auditável
4. Iteração controlada: limites claros para evitar loops infinitos
5. Escalabilidade: estrutura permite adicionar novos agentes sem quebrar o sistema

---

**Versão:** 2.0  
**Data:** 13/11/2025  
**Status:** Atualizado - Orquestrador como facilitador, fluxo adaptativo e conversacional

