# Sistema Multi-Agente para Produção de Artigos Científicos

> Visão de longo prazo: descreve todos os agentes planejados para a plataforma colaborativa com IA.
> **Status da POC:** apenas Orquestrador e Metodologista estão em implementação inicial.

## Arquitetura Geral

**Fluxo:** Semi-linear com loops controlados  
**Comunicação:** Estado compartilhado via LangGraph  
**Resolução de conflitos:** Voto de Minerva (usuário decide)

---

## 0. OBSERVADOR (Mente Analítica)

### Responsabilidades
- **Monitorar TODA conversa** (cada turno automaticamente)
- Atualizar CognitiveModel completo:
  - Claims emergentes
  - Fundamentos
  - Contradições
  - Conceitos (ChromaDB + SQLite)
  - Open questions
  - Context (domínio, população, tecnologia)
- **Avaliar evolução** de ideias e argumentos
- **Detectar lacunas** e inconsistências
- **Calcular métricas** (solidez, completude)
- **Responder consultas** do Orquestrador (insights contextuais)
- **Publicar eventos** para Dashboard (silencioso)

### PODE fazer
- Processar cada turno automaticamente
- Extrair conceitos via LLM e gerar embeddings
- Salvar conceitos no catálogo (ChromaDB + SQLite)
- Consultar biblioteca para deduplicação (threshold 0.80)
- Responder consultas contextuais do Orquestrador
- Calcular solidez e completude do raciocínio

### NÃO PODE fazer
- **Decidir next_step** (quem decide: Orquestrador)
- **Falar com usuário** (quem fala: Orquestrador)
- **Negociar caminhos** (quem negocia: Orquestrador)
- Interromper fluxo conversacional
- Dar comandos ao Orquestrador (apenas insights)

### Input esperado
- De cada turno: user_input, conversation_history
- De Orquestrador: consultas contextuais (quando incerto)

### Output esperado
**Silenciosamente (todo turno):**
- CognitiveModel atualizado
- Conceitos salvos no catálogo
- Eventos publicados (Dashboard)

**Quando consultado (não-determinístico):**
- Insights contextuais: {insight, suggestion, confidence, evidence}
- Estado completo: CognitiveModel.to_dict()

### Critérios de qualidade
- Conceitos relevantes extraídos (não ruído)
- Deduplicação precisa (threshold 0.80)
- Insights úteis (não genéricos)
- Não interfere no fluxo (silencioso)
- Sempre responde consultas rapidamente

### Timing
**Todo turno, sempre:**
- Processa cada turno automaticamente
- Não depende de snapshots ou eventos externos
- Garante que nada é perdido

### Interface de Consulta

**Filosofia:** Insights, não comandos

```python
# Consultas contextuais (não-determinísticas)
insight = observador.what_do_you_see(
    context="Usuário mudou de direção",
    question="Conceitos anteriores ainda relevantes?"
)

# Estado completo
state = observador.get_current_state()

# Checks rápidos
has_issues = observador.has_contradiction()
solidez = observador.get_solidez()
```

**Gatilhos naturais para consulta:**
- Mudança de direção detectada
- Contradição aparente
- Incerteza sobre profundidade
- Checagem de completude

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
- **Provocar reflexão** sobre aspectos não explorados: "Você assumiu X. Quer examinar?"
- **Consultar Observador** quando incerto (gatilhos naturais)

### PODE fazer
- **Perguntar ao usuário** antes de chamar agentes
- **Apresentar opções** claras e contextuais
- Chamar qualquer agente (após negociação)
- Solicitar re-trabalho de qualquer etapa
- Pedir esclarecimentos ao usuário
- Salvar checkpoints do progresso
- **Adaptar fluxo** quando usuário muda de direção
- Encerrar processo (com aprovação do usuário)
- **Consultar Observador** para insights contextuais
- Usar insights para decisões mais inteligentes

### NÃO PODE fazer
- **Decidir sozinho** qual agente chamar (deve negociar)
- **Classificar automaticamente** sem explorar intenção
- Avaliar conteúdo científico
- Escrever ou editar texto
- Tomar decisões sobre metodologia
- Ignorar feedback de agentes especialistas
- **Forçar fluxo rígido** (deve ser adaptativo)
- **Detectar proposições não examinadas** (responsabilidade do Observador)
- **Extrair claims** (responsabilidade do Observador)
- **Atualizar CognitiveModel** (responsabilidade do Observador)

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

### Mitose: Observador Separado (05/12/2025)

**EVOLUÇÃO:**
- Orquestrador tinha 2 responsabilidades conflitantes
- Separamos em 2 agentes especializados:
  - **Orquestrador:** Facilitar conversa, negociar, decidir fluxo
  - **Observador:** Atualizar CognitiveModel, extrair conceitos, calcular métricas

**Como se comunicam:**
- Orquestrador consulta Observador quando incerto (não-determinístico)
- Observador responde com insights, não comandos
- Orquestrador mantém autonomia sobre decisões

**Exemplo de consulta:**
```
Orquestrador detecta mudança de direção
↓
Consulta Observador: "Conceitos anteriores ainda relevantes?"
↓
Observador responde: {relevance: "Parcial", suggestion: "...", confidence: 0.8}
↓
Orquestrador decide baseado em insight + própria análise
```

---

## 2. METODOLOGISTA

### Responsabilidades
- Avaliar **coerência lógica** de hipóteses/constatações (qualquer domínio)
- Validar se argumentação é sólida (não necessariamente científica)
- Identificar **contradições** entre proposições
- Apontar **lacunas** no raciocínio
- Sugerir fortalecimento de fundamentos frágeis
- **Validar se fundamentos têm solidez suficiente** (têm base?)
- **Identificar fundamentos com baixa solidez** (precisam evidências?)
- **Apontar contradictions** na lógica
- **Sugerir evidências necessárias**: "Fundamento X precisa de evidência" (adiciona open_question)

### PODE fazer
- Rejeitar hipótese com justificativa (lógica falha)
- Pedir mais informações ao usuário (via Orquestrador)
- Sugerir ajustes na formulação (clareza)
- Apontar inconsistências lógicas
- Validar coerência entre proposições
- Avaliar solidez de fundamentos (baseado em coerência, não apenas método científico)

### NÃO PODE fazer
- Criar o outline do artigo (responsabilidade de outro produto)
- Fazer pesquisa bibliográfica (responsabilidade do Pesquisador)
- Escrever conteúdo (responsabilidade de outro produto)
- Estruturar argumentação (isso é do Estruturador)
- **Impor formato acadêmico** (Revelar não exige isso)
- **Validar metodologia científica específica** (só se contexto pedir)

### Input esperado
- Hipótese/constatação/observação do usuário (qualquer domínio)
- Contexto da área/domínio
- (Opcional) Evidências prévias (pesquisa ou experiência)

### Output esperado
**Se aprovado:**
- Validação com justificativa
- Pontos fortes da argumentação
- Recomendações de fortalecimento

**Se rejeitado:**
- Inconsistências específicas identificadas
- Sugestões concretas de correção
- Alternativas lógicas

### Critérios de qualidade
- Justificativas baseadas em **lógica e coerência**
- Apontamentos específicos, não genéricos
- Sugestões acionáveis
- Sem viés de domínio (funciona para negócio, pesquisa, vida pessoal)
- **Adapta rigor ao contexto** (hipótese de negócio ≠ hipótese científica)

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

### Dimensões de Operação

O Writer opera em 4 dimensões ao produzir um artigo:

- **Contexto:** matéria-prima — o que foi feito, dados, detalhes.
- **Intenção:** o que o autor quer provocar no leitor (informar, posicionar-se, propor, desafiar).
- **Formato:** molde do artigo (IMRaD, one-pager, ensaio, relato técnico).
- **Estrutura:** narrativa e ordem dentro do formato.

Nenhuma dessas dimensões é imposta por classificação externa prévia. Todas emergem da conversa, alinhadas à filosofia de "estrutura emerge da conversa" (ver products/ensaio/docs/vision.md §5).

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

### Observador (Mente Analítica)

O Observador monitora toda conversa e atualiza o CognitiveModel automaticamente:

- **Monitora cada turno:** Processa TODO input do usuário (não apenas snapshots)
- **Extrai claims:** Captura proposições centrais emergentes
- **Identifica fundamentos:** Mapeia argumentos de suporte
- **Detecta contradições:** Encontra inconsistências lógicas
- **Cataloga conceitos:** Extrai essências semânticas (ChromaDB)
- **Identifica open_questions:** Mapeia lacunas a investigar
- **Atualiza context:** Enriquece domínio, população, tecnologia
- **Calcula métricas:** Solidez e completude do raciocínio

**Integração com fluxo:**
- Trabalha silenciosamente em paralelo
- Não interfere na conversa
- Responde consultas do Orquestrador
- Publica eventos para Dashboard

### Orquestrador (Facilitador)

O Orquestrador facilita a conversa e consulta o Observador:

- **Provoca reflexão** baseado em insights do Observador
- **Consulta Observador** quando incerto (mudança direção, contradição, completude)
- **Usa insights** para decisões contextuais (não segue comandos)
- **Mantém autonomia** sobre next_step

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

### Observador nos Bastidores

**Quando aparece na timeline:**
- Conceito novo detectado: "👁️ Observador detectou: LLMs, Produtividade"
- Contradição: "👁️ Observador detectou contradição entre X e Y"
- Solidez muda: "👁️ Solidez aumentou: 0.65 → 0.80"

**Quando NÃO aparece:**
- Atualização rotineira sem novidades
- Trabalho silencioso é transparente ao usuário

### Ações Baratas vs Caras

O sistema diferencia ações que podem ser proativas (baratas) daquelas que requerem permissão (caras):

**Ações Baratas (proativas)**:
- Estruturador organizar fundamentos
- Observador processar turno e atualizar CognitiveModel
- Metodologista apontar lacuna

**Ações Caras (pedir permissão)**:
- Pesquisador buscar papers
- Escritor gerar rascunho
- Análise profunda que consome muitos tokens

**Referências**: Ver `core/docs/vision/cognitive_model/core.md` para detalhes sobre a estrutura do modelo cognitivo.

---

## Fluxo e Estado Compartilhado

Ver fluxo técnico completo em `../docs/architecture/agents/multi_agent/flows.md`.

Ver `MultiAgentState` em `../docs/architecture/agents/multi_agent/state.md`.

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

**Versão:** 3.0  
**Data:** 05/12/2025  
**Status:** Atualizado - Observador separado do Orquestrador (mitose), arquitetura especializada

